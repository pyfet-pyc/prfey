# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\topology.py
"""Internal class to monitor a topology of one or more servers."""
import os, random, threading, warnings, weakref
from bson.py3compat import itervalues, PY3
if PY3:
    import queue as Queue
else:
    import Queue
from pymongo import common
from pymongo import periodic_executor
from pymongo.pool import PoolOptions
from pymongo.topology_description import updated_topology_description, _updated_topology_description_srv_polling, TopologyDescription, SRV_POLLING_TOPOLOGIES, TOPOLOGY_TYPE
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from pymongo.monitor import SrvMonitor
import pymongo.monotonic as _time
from pymongo.server import Server
from pymongo.server_selectors import any_server_selector, arbiter_server_selector, secondary_server_selector, readable_server_selector, writable_server_selector, Selection
from pymongo.client_session import _ServerSessionPool

def process_events_queue(queue_ref):
    q = queue_ref()
    if not q:
        return False
        while True:
            try:
                event = q.get_nowait()
            except Queue.Empty:
                break
            else:
                fn, args = event
                fn(*args)

        return True


class Topology(object):
    __doc__ = 'Monitor a topology of one or more servers.'

    def __init__(self, topology_settings):
        self._topology_id = topology_settings._topology_id
        self._listeners = topology_settings._pool_options.event_listeners
        pub = self._listeners is not None
        self._publish_server = pub and self._listeners.enabled_for_server
        self._publish_tp = pub and self._listeners.enabled_for_topology
        self._events = None
        self._Topology__events_executor = None
        if self._publish_server or (self._publish_tp):
            self._events = Queue.Queue(maxsize=100)
        if self._publish_tp:
            self._events.put((self._listeners.publish_topology_opened,
             (
              self._topology_id,)))
        self._settings = topology_settings
        topology_description = TopologyDescription(topology_settings.get_topology_type(), topology_settings.get_server_descriptions(), topology_settings.replica_set_name, None, None, topology_settings)
        self._description = topology_description
        if self._publish_tp:
            initial_td = TopologyDescription(TOPOLOGY_TYPE.Unknown, {}, None, None, None, self._settings)
            self._events.put((
             self._listeners.publish_topology_description_changed,
             (
              initial_td, self._description, self._topology_id)))
        for seed in topology_settings.seeds:
            if self._publish_server:
                self._events.put((self._listeners.publish_server_opened,
                 (
                  seed, self._topology_id)))
        else:
            self._seed_addresses = list(topology_description.server_descriptions())
            self._opened = False
            self._lock = threading.Lock()
            self._condition = self._settings.condition_class(self._lock)
            self._servers = {}
            self._pid = None
            self._max_cluster_time = None
            self._session_pool = _ServerSessionPool()
            if self._publish_server or (self._publish_tp):

                def target():
                    return process_events_queue(weak)

                executor = periodic_executor.PeriodicExecutor(interval=(common.EVENTS_QUEUE_FREQUENCY),
                  min_interval=0.5,
                  target=target,
                  name='pymongo_events_thread')
                weak = weakref.ref(self._events, executor.close)
                self._Topology__events_executor = executor
                executor.open()
            self._srv_monitor = None
            if self._settings.fqdn is not None:
                self._srv_monitor = SrvMonitor(self, self._settings)

    def open(self):
        """Start monitoring, or restart after a fork.

        No effect if called multiple times.

        .. warning:: Topology is shared among multiple threads and is protected
          by mutual exclusion. Using Topology from a process other than the one
          that initialized it will emit a warning and may result in deadlock. To
          prevent this from happening, MongoClient must be created after any
          forking.

        """
        if self._pid is None:
            self._pid = os.getpid()
        elif os.getpid() != self._pid:
            warnings.warn("MongoClient opened before fork. Create MongoClient only after forking. See PyMongo's documentation for details: http://api.mongodb.org/python/current/faq.html#is-pymongo-fork-safe")
            with self._lock:
                self._session_pool.reset()
        with self._lock:
            self._ensure_opened()

    def select_servers(self, selector, server_selection_timeout=None, address=None):
        """Return a list of Servers matching selector, or time out.

        :Parameters:
          - `selector`: function that takes a list of Servers and returns
            a subset of them.
          - `server_selection_timeout` (optional): maximum seconds to wait.
            If not provided, the default value common.SERVER_SELECTION_TIMEOUT
            is used.
          - `address`: optional server address to select.

        Calls self.open() if needed.

        Raises exc:`ServerSelectionTimeoutError` after
        `server_selection_timeout` if no matching servers are found.
        """
        if server_selection_timeout is None:
            server_timeout = self._settings.server_selection_timeout
        else:
            server_timeout = server_selection_timeout
        with self._lock:
            server_descriptions = self._select_servers_loop(selector, server_timeout, address)
            return [self.get_server_by_address(sd.address) for sd in server_descriptions]

    def _select_servers_loop(self, selector, timeout, address):
        """select_servers() guts. Hold the lock when calling this."""
        now = _time()
        end_time = now + timeout
        server_descriptions = self._description.apply_selector(selector,
          address, custom_selector=(self._settings.server_selector))
        while True:
            if not server_descriptions:
                if timeout == 0 or now > end_time:
                    raise ServerSelectionTimeoutError(self._error_message(selector))
                else:
                    self._ensure_opened()
                    self._request_check_all()
                    self._condition.wait(common.MIN_HEARTBEAT_INTERVAL)
                    self._description.check_compatible()
                    now = _time()
                    server_descriptions = self._description.apply_selector(selector,
                      address, custom_selector=(self._settings.server_selector))

        self._description.check_compatible()
        return server_descriptions

    def select_server(self, selector, server_selection_timeout=None, address=None):
        """Like select_servers, but choose a random server if several match."""
        return random.choice(self.select_servers(selector, server_selection_timeout, address))

    def select_server_by_address(self, address, server_selection_timeout=None):
        """Return a Server for "address", reconnecting if necessary.

        If the server's type is not known, request an immediate check of all
        servers. Time out after "server_selection_timeout" if the server
        cannot be reached.

        :Parameters:
          - `address`: A (host, port) pair.
          - `server_selection_timeout` (optional): maximum seconds to wait.
            If not provided, the default value
            common.SERVER_SELECTION_TIMEOUT is used.

        Calls self.open() if needed.

        Raises exc:`ServerSelectionTimeoutError` after
        `server_selection_timeout` if no matching servers are found.
        """
        return self.select_server(any_server_selector, server_selection_timeout, address)

    def _process_change(self, server_description):
        """Process a new ServerDescription on an opened topology.

        Hold the lock when calling this.
        """
        td_old = self._description
        if self._publish_server:
            old_server_description = td_old._server_descriptions[server_description.address]
            self._events.put((
             self._listeners.publish_server_description_changed,
             (
              old_server_description, server_description,
              server_description.address, self._topology_id)))
        self._description = updated_topology_description(self._description, server_description)
        self._update_servers()
        self._receive_cluster_time_no_lock(server_description.cluster_time)
        if self._publish_tp:
            self._events.put((
             self._listeners.publish_topology_description_changed,
             (
              td_old, self._description, self._topology_id)))
        if self._srv_monitor:
            if td_old.topology_type == TOPOLOGY_TYPE.Unknown:
                if self._description.topology_type not in SRV_POLLING_TOPOLOGIES:
                    self._srv_monitor.close()
        self._condition.notify_all()

    def on_change(self, server_description):
        """Process a new ServerDescription after an ismaster call completes."""
        with self._lock:
            if self._opened:
                if self._description.has_server(server_description.address):
                    self._process_change(server_description)

    def _process_srv_update(self, seedlist):
        """Process a new seedlist on an opened topology.
        Hold the lock when calling this.
        """
        td_old = self._description
        self._description = _updated_topology_description_srv_polling(self._description, seedlist)
        self._update_servers()
        if self._publish_tp:
            self._events.put((
             self._listeners.publish_topology_description_changed,
             (
              td_old, self._description, self._topology_id)))

    def on_srv_update(self, seedlist):
        """Process a new list of nodes obtained from scanning SRV records."""
        with self._lock:
            if self._opened:
                self._process_srv_update(seedlist)

    def get_server_by_address(self, address):
        """Get a Server or None.

        Returns the current version of the server immediately, even if it's
        Unknown or absent from the topology. Only use this in unittests.
        In driver code, use select_server_by_address, since then you're
        assured a recent view of the server's type and wire protocol version.
        """
        return self._servers.get(address)

    def has_server(self, address):
        return address in self._servers

    def get_primary--- This code section failed: ---

 L. 350         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           70  'to 70'
                6  POP_TOP          

 L. 351         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _description
               12  LOAD_ATTR                topology_type
               14  STORE_FAST               'topology_type'

 L. 352        16  LOAD_FAST                'topology_type'
               18  LOAD_GLOBAL              TOPOLOGY_TYPE
               20  LOAD_ATTR                ReplicaSetWithPrimary
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L. 353        26  POP_BLOCK        
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'

 L. 355        40  LOAD_GLOBAL              writable_server_selector
               42  LOAD_FAST                'self'
               44  LOAD_METHOD              _new_selection
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  LOAD_ATTR                address
               56  POP_BLOCK        
               58  ROT_TWO          
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH        4  '4'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 28

    def _get_replica_set_members(self, selector):
        """Return set of replica set member addresses."""
        with self._lock:
            topology_type = self._description.topology_type
            if topology_type not in (TOPOLOGY_TYPE.ReplicaSetWithPrimary,
             TOPOLOGY_TYPE.ReplicaSetNoPrimary):
                return set()
            return set([sd.address for sd in selector(self._new_selection())])

    def get_secondaries(self):
        """Return set of secondary addresses."""
        return self._get_replica_set_members(secondary_server_selector)

    def get_arbiters(self):
        """Return set of arbiter addresses."""
        return self._get_replica_set_members(arbiter_server_selector)

    def max_cluster_time(self):
        """Return a document, the highest seen $clusterTime."""
        return self._max_cluster_time

    def _receive_cluster_time_no_lock(self, cluster_time):
        if cluster_time:
            if not self._max_cluster_time or cluster_time['clusterTime'] > self._max_cluster_time['clusterTime']:
                self._max_cluster_time = cluster_time

    def receive_cluster_time(self, cluster_time):
        with self._lock:
            self._receive_cluster_time_no_lock(cluster_time)

    def request_check_all(self, wait_time=5):
        """Wake all monitors, wait for at least one to check its server."""
        with self._lock:
            self._request_check_all()
            self._condition.wait(wait_time)

    def reset_pool(self, address):
        with self._lock:
            server = self._servers.get(address)
            if server:
                server.pool.reset()

    def reset_server(self, address):
        """Clear our pool for a server and mark it Unknown.

        Do *not* request an immediate check.
        """
        with self._lock:
            self._reset_server(address, reset_pool=True)

    def reset_server_and_request_check(self, address):
        """Clear our pool for a server, mark it Unknown, and check it soon."""
        with self._lock:
            self._reset_server(address, reset_pool=True)
            self._request_check(address)

    def mark_server_unknown_and_request_check(self, address):
        """Mark a server Unknown, and check it soon."""
        with self._lock:
            self._reset_server(address, reset_pool=False)
            self._request_check(address)

    def update_pool(self):
        servers = []
        with self._lock:
            for server in self._servers.values():
                servers.append((server, server._pool.pool_id))

        for server, pool_id in servers:
            server._pool.remove_stale_sockets(pool_id)

    def close(self):
        """Clear pools and terminate monitors. Topology reopens on demand."""
        with self._lock:
            for server in self._servers.values():
                server.close()
            else:
                self._description = self._description.reset()
                for address, sd in self._description.server_descriptions().items():
                    if address in self._servers:
                        self._servers[address].description = sd
                else:
                    if self._srv_monitor:
                        self._srv_monitor.close()
                    self._opened = False

        if self._publish_tp:
            self._events.put((self._listeners.publish_topology_closed,
             (
              self._topology_id,)))
        if self._publish_server or (self._publish_tp):
            self._Topology__events_executor.close()

    @property
    def description(self):
        return self._description

    def pop_all_sessions(self):
        """Pop all session ids from the pool."""
        with self._lock:
            return self._session_pool.pop_all()

    def get_server_session(self):
        """Start or resume a server session, or raise ConfigurationError."""
        with self._lock:
            session_timeout = self._description.logical_session_timeout_minutes
            if session_timeout is None:
                if self._description.topology_type == TOPOLOGY_TYPE.Single:
                    self._description.has_known_servers or self._select_servers_loop(any_server_selector, self._settings.server_selection_timeout, None)
                elif not self._description.readable_servers:
                    self._select_servers_loop(readable_server_selector, self._settings.server_selection_timeout, None)
                session_timeout = self._description.logical_session_timeout_minutes
                if session_timeout is None:
                    raise ConfigurationError('Sessions are not supported by this MongoDB deployment')
                return self._session_pool.get_server_session(session_timeout)

    def return_server_session(self, server_session, lock):
        if lock:
            with self._lock:
                session_timeout = self._description.logical_session_timeout_minutes
                if session_timeout is not None:
                    self._session_pool.return_server_session(server_session, session_timeout)
        else:
            self._session_pool.return_server_session_no_lock(server_session)

    def _new_selection(self):
        """A Selection object, initially including all known servers.

        Hold the lock when calling this.
        """
        return Selection.from_topology_description(self._description)

    def _ensure_opened(self):
        """Start monitors, or restart after a fork.

        Hold the lock when calling this.
        """
        if not self._opened:
            self._opened = True
            self._update_servers()
            if self._publish_tp or (self._publish_server):
                self._Topology__events_executor.open()
            if self._srv_monitor:
                if self.description.topology_type in SRV_POLLING_TOPOLOGIES:
                    self._srv_monitor.open()
        for server in itervalues(self._servers):
            server.open()

    def _reset_server(self, address, reset_pool):
        """Mark a server Unknown and optionally reset it's pool.

        Hold the lock when calling this. Does *not* request an immediate check.
        """
        server = self._servers.get(address)
        if server:
            if reset_pool:
                server.reset()
            self._description = self._description.reset_server(address)
            self._update_servers()

    def _request_check(self, address):
        """Wake one monitor. Hold the lock when calling this."""
        server = self._servers.get(address)
        if server:
            server.request_check()

    def _request_check_all(self):
        """Wake all monitors. Hold the lock when calling this."""
        for server in self._servers.values():
            server.request_check()

    def _update_servers(self):
        """Sync our Servers from TopologyDescription.server_descriptions.

        Hold the lock while calling this.
        """
        for address, sd in self._description.server_descriptions().items():
            if address not in self._servers:
                monitor = self._settings.monitor_class(server_description=sd,
                  topology=self,
                  pool=(self._create_pool_for_monitor(address)),
                  topology_settings=(self._settings))
                weak = None
                if self._publish_server:
                    weak = weakref.ref(self._events)
                else:
                    server = Server(server_description=sd,
                      pool=(self._create_pool_for_server(address)),
                      monitor=monitor,
                      topology_id=(self._topology_id),
                      listeners=(self._listeners),
                      events=weak)
                    self._servers[address] = server
                    server.open()
            else:
                was_writable = self._servers[address].description.is_writable
                self._servers[address].description = sd
                if was_writable != sd.is_writable:
                    self._servers[address].pool.update_is_writable(sd.is_writable)
        else:
            for address, server in list(self._servers.items()):
                if not self._description.has_server(address):
                    server.close()
                    self._servers.pop(address)

    def _create_pool_for_server(self, address):
        return self._settings.pool_class(address, self._settings.pool_options)

    def _create_pool_for_monitor(self, address):
        options = self._settings.pool_options
        monitor_pool_options = PoolOptions(connect_timeout=(options.connect_timeout),
          socket_timeout=(options.connect_timeout),
          ssl_context=(options.ssl_context),
          ssl_match_hostname=(options.ssl_match_hostname),
          event_listeners=(options.event_listeners),
          appname=(options.appname),
          driver=(options.driver))
        return self._settings.pool_class(address, monitor_pool_options, handshake=False)

    def _error_message(self, selector):
        """Format an error message if server selection fails.

        Hold the lock when calling this.
        """
        is_replica_set = self._description.topology_type in (
         TOPOLOGY_TYPE.ReplicaSetWithPrimary,
         TOPOLOGY_TYPE.ReplicaSetNoPrimary)
        if is_replica_set:
            server_plural = 'replica set members'
        elif self._description.topology_type == TOPOLOGY_TYPE.Sharded:
            server_plural = 'mongoses'
        else:
            server_plural = 'servers'
        if self._description.known_servers:
            if selector is writable_server_selector:
                if is_replica_set:
                    return 'No primary available for writes'
                return 'No %s available for writes' % server_plural
            else:
                return 'No %s match selector "%s"' % (server_plural, selector)
        else:
            addresses = list(self._description.server_descriptions())
            servers = list(self._description.server_descriptions().values())
            if not servers:
                if is_replica_set:
                    return 'No %s available for replica set name "%s"' % (
                     server_plural, self._settings.replica_set_name)
                return 'No %s available' % server_plural
            error = servers[0].error
            same = all((server.error == error for server in servers[1:]))
            if same:
                if error is None:
                    return 'No %s found yet' % server_plural
                if is_replica_set:
                    if not set(addresses).intersection(self._seed_addresses):
                        return 'Could not reach any servers in %s. Replica set is configured with internal hostnames or IPs?' % addresses
                    return str(error)
            return ','.join((str(server.error) for server in servers if server.error))