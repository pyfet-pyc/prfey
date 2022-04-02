# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\monitor.py
"""Class to monitor a MongoDB server on a background thread."""
import weakref
from pymongo import common, periodic_executor
from pymongo.errors import OperationFailure
import pymongo.monotonic as _time
from pymongo.read_preferences import MovingAverage
from pymongo.server_description import ServerDescription
from pymongo.server_type import SERVER_TYPE
from pymongo.srv_resolver import _SrvResolver

class MonitorBase(object):

    def __init__(self, *args, **kwargs):
        """Override this method to create an executor."""
        raise NotImplementedError

    def open(self):
        """Start monitoring, or restart after a fork.

        Multiple calls have no effect.
        """
        self._executor.open()

    def close(self):
        """Close and stop monitoring.

        open() restarts the monitor after closing.
        """
        self._executor.close()

    def join(self, timeout=None):
        """Wait for the monitor to stop."""
        self._executor.join(timeout)

    def request_check(self):
        """If the monitor is sleeping, wake it soon."""
        self._executor.wake()


class Monitor(MonitorBase):

    def __init__(self, server_description, topology, pool, topology_settings):
        """Class to monitor a MongoDB server on a background thread.

        Pass an initial ServerDescription, a Topology, a Pool, and
        TopologySettings.

        The Topology is weakly referenced. The Pool must be exclusive to this
        Monitor.
        """
        self._server_description = server_description
        self._pool = pool
        self._settings = topology_settings
        self._avg_round_trip_time = MovingAverage()
        self._listeners = self._settings._pool_options.event_listeners
        pub = self._listeners is not None
        self._publish = pub and self._listeners.enabled_for_server_heartbeat

        def target():
            monitor = self_ref()
            if monitor is None:
                return False
            Monitor._run(monitor)
            return True

        executor = periodic_executor.PeriodicExecutor(interval=(self._settings.heartbeat_frequency),
          min_interval=(common.MIN_HEARTBEAT_INTERVAL),
          target=target,
          name='pymongo_server_monitor_thread')
        self._executor = executor
        self_ref = weakref.ref(self, executor.close)
        self._topology = weakref.proxy(topology, executor.close)

    def close(self):
        super(Monitor, self).close()
        self._pool.reset()

    def _run(self):
        try:
            self._server_description = self._check_with_retry()
            self._topology.on_change(self._server_description)
        except ReferenceError:
            self.close()

    def _check_with_retry--- This code section failed: ---

 L. 123         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _server_description
                4  LOAD_ATTR                address
                6  STORE_FAST               'address'

 L. 124         8  LOAD_CONST               True
               10  STORE_FAST               'retry'

 L. 125        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _server_description
               16  LOAD_ATTR                server_type
               18  LOAD_GLOBAL              SERVER_TYPE
               20  LOAD_ATTR                Unknown
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 126        26  LOAD_CONST               False
               28  STORE_FAST               'retry'
             30_0  COME_FROM            24  '24'

 L. 128        30  LOAD_GLOBAL              _time
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'start'

 L. 129        36  SETUP_FINALLY        48  'to 48'

 L. 130        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _check_once
               42  CALL_METHOD_0         0  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    36  '36'

 L. 131        48  DUP_TOP          
               50  LOAD_GLOBAL              ReferenceError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    70  'to 70'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 132        62  RAISE_VARARGS_0       0  'reraise'
               64  POP_EXCEPT       
            66_68  JUMP_FORWARD        330  'to 330'
             70_0  COME_FROM            54  '54'

 L. 133        70  DUP_TOP          
               72  LOAD_GLOBAL              Exception
               74  COMPARE_OP               exception-match
            76_78  POP_JUMP_IF_FALSE   328  'to 328'
               80  POP_TOP          
               82  STORE_FAST               'error'
               84  POP_TOP          
               86  SETUP_FINALLY       316  'to 316'

 L. 134        88  LOAD_GLOBAL              _time
               90  CALL_FUNCTION_0       0  ''
               92  LOAD_FAST                'start'
               94  BINARY_SUBTRACT  
               96  STORE_FAST               'error_time'

 L. 135        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _publish
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L. 136       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _listeners
              108  LOAD_METHOD              publish_server_heartbeat_failed

 L. 137       110  LOAD_FAST                'address'

 L. 137       112  LOAD_FAST                'error_time'

 L. 137       114  LOAD_FAST                'error'

 L. 136       116  CALL_METHOD_3         3  ''
              118  POP_TOP          
            120_0  COME_FROM           102  '102'

 L. 138       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _topology
              124  LOAD_METHOD              reset_pool
              126  LOAD_FAST                'address'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 139       132  LOAD_GLOBAL              ServerDescription
              134  LOAD_FAST                'address'
              136  LOAD_FAST                'error'
              138  LOAD_CONST               ('error',)
              140  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              142  STORE_FAST               'default'

 L. 140       144  LOAD_FAST                'retry'
              146  POP_JUMP_IF_TRUE    170  'to 170'

 L. 141       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _avg_round_trip_time
              152  LOAD_METHOD              reset
              154  CALL_METHOD_0         0  ''
              156  POP_TOP          

 L. 143       158  LOAD_FAST                'default'
              160  ROT_FOUR         
              162  POP_BLOCK        
              164  POP_EXCEPT       
              166  CALL_FINALLY        316  'to 316'
              168  RETURN_VALUE     
            170_0  COME_FROM           146  '146'

 L. 147       170  LOAD_GLOBAL              _time
              172  CALL_FUNCTION_0       0  ''
              174  STORE_FAST               'start'

 L. 148       176  SETUP_FINALLY       196  'to 196'

 L. 149       178  LOAD_FAST                'self'
              180  LOAD_METHOD              _check_once
              182  CALL_METHOD_0         0  ''
              184  POP_BLOCK        
              186  ROT_FOUR         
              188  POP_BLOCK        
              190  POP_EXCEPT       
              192  CALL_FINALLY        316  'to 316'
              194  RETURN_VALUE     
            196_0  COME_FROM_FINALLY   176  '176'

 L. 150       196  DUP_TOP          
              198  LOAD_GLOBAL              ReferenceError
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   216  'to 216'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 151       210  RAISE_VARARGS_0       0  'reraise'
              212  POP_EXCEPT       
              214  JUMP_FORWARD        312  'to 312'
            216_0  COME_FROM           202  '202'

 L. 152       216  DUP_TOP          
              218  LOAD_GLOBAL              Exception
              220  COMPARE_OP               exception-match
          222_224  POP_JUMP_IF_FALSE   310  'to 310'
              226  POP_TOP          
              228  STORE_FAST               'error'
              230  POP_TOP          
              232  SETUP_FINALLY       298  'to 298'

 L. 153       234  LOAD_GLOBAL              _time
              236  CALL_FUNCTION_0       0  ''
              238  LOAD_FAST                'start'
              240  BINARY_SUBTRACT  
              242  STORE_FAST               'error_time'

 L. 154       244  LOAD_FAST                'self'
              246  LOAD_ATTR                _publish
          248_250  POP_JUMP_IF_FALSE   268  'to 268'

 L. 155       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _listeners
              256  LOAD_METHOD              publish_server_heartbeat_failed

 L. 156       258  LOAD_FAST                'address'

 L. 156       260  LOAD_FAST                'error_time'

 L. 156       262  LOAD_FAST                'error'

 L. 155       264  CALL_METHOD_3         3  ''
              266  POP_TOP          
            268_0  COME_FROM           248  '248'

 L. 157       268  LOAD_FAST                'self'
              270  LOAD_ATTR                _avg_round_trip_time
              272  LOAD_METHOD              reset
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          

 L. 158       278  LOAD_FAST                'default'
              280  ROT_FOUR         
              282  POP_BLOCK        
              284  POP_EXCEPT       
              286  CALL_FINALLY        298  'to 298'
              288  ROT_FOUR         
              290  POP_BLOCK        
              292  POP_EXCEPT       
              294  CALL_FINALLY        316  'to 316'
              296  RETURN_VALUE     
            298_0  COME_FROM           286  '286'
            298_1  COME_FROM_FINALLY   232  '232'
              298  LOAD_CONST               None
              300  STORE_FAST               'error'
              302  DELETE_FAST              'error'
              304  END_FINALLY      
              306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           222  '222'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           214  '214'
              312  POP_BLOCK        
              314  BEGIN_FINALLY    
            316_0  COME_FROM           294  '294'
            316_1  COME_FROM           192  '192'
            316_2  COME_FROM           166  '166'
            316_3  COME_FROM_FINALLY    86  '86'
              316  LOAD_CONST               None
              318  STORE_FAST               'error'
              320  DELETE_FAST              'error'
              322  END_FINALLY      
              324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM            76  '76'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM            66  '66'

Parse error at or near `DUP_TOP' instruction at offset 70

    def _check_once(self):
        """A single attempt to call ismaster.

        Returns a ServerDescription, or raises an exception.
        """
        address = self._server_description.address
        if self._publish:
            self._listeners.publish_server_heartbeat_started(address)
        with self._pool.get_socket({}) as sock_info:
            response, round_trip_time = self._check_with_socket(sock_info)
            self._avg_round_trip_time.add_sample(round_trip_time)
            sd = ServerDescription(address=address,
              ismaster=response,
              round_trip_time=(self._avg_round_trip_time.get()))
            if self._publish:
                self._listeners.publish_server_heartbeat_succeededaddressround_trip_timeresponse
            return sd

    def _check_with_socket(self, sock_info):
        """Return (IsMaster, round_trip_time).

        Can raise ConnectionFailure or OperationFailure.
        """
        start = _time()
        try:
            return (sock_info.ismaster(self._pool.opts.metadata, self._topology.max_cluster_time()),
             _time() - start)
            except OperationFailure as exc:
            try:
                self._topology.receive_cluster_time(exc.details.get('$clusterTime'))
                raise
            finally:
                exc = None
                del exc


class SrvMonitor(MonitorBase):

    def __init__(self, topology, topology_settings):
        """Class to poll SRV records on a background thread.

        Pass a Topology and a TopologySettings.

        The Topology is weakly referenced.
        """
        self._settings = topology_settings
        self._seedlist = self._settings._seeds
        self._fqdn = self._settings.fqdn

        def target():
            monitor = self_ref()
            if monitor is None:
                return False
            SrvMonitor._run(monitor)
            return True

        executor = periodic_executor.PeriodicExecutor(interval=(common.MIN_SRV_RESCAN_INTERVAL),
          min_interval=(self._settings.heartbeat_frequency),
          target=target,
          name='pymongo_srv_polling_thread')
        self._executor = executor
        self_ref = weakref.ref(self, executor.close)
        self._topology = weakref.proxy(topology, executor.close)

    def _run(self):
        seedlist = self._get_seedlist()
        if seedlist:
            self._seedlist = seedlist
            try:
                self._topology.on_srv_update(self._seedlist)
            except ReferenceError:
                self.close()

    def _get_seedlist--- This code section failed: ---

 L. 246         0  SETUP_FINALLY        40  'to 40'

 L. 247         2  LOAD_GLOBAL              _SrvResolver
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _fqdn
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_METHOD              get_hosts_and_min_ttl
               12  CALL_METHOD_0         0  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'seedlist'
               18  STORE_FAST               'ttl'

 L. 248        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'seedlist'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L. 250        32  LOAD_GLOBAL              Exception
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'
               36  POP_BLOCK        
               38  JUMP_FORWARD         70  'to 70'
             40_0  COME_FROM_FINALLY     0  '0'

 L. 251        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    68  'to 68'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 256        54  LOAD_FAST                'self'
               56  LOAD_METHOD              request_check
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 257        62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            46  '46'
               68  END_FINALLY      
             70_0  COME_FROM            38  '38'

 L. 259        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _executor
               74  LOAD_METHOD              update_interval

 L. 260        76  LOAD_GLOBAL              max
               78  LOAD_FAST                'ttl'
               80  LOAD_GLOBAL              common
               82  LOAD_ATTR                MIN_SRV_RESCAN_INTERVAL
               84  CALL_FUNCTION_2       2  ''

 L. 259        86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 261        90  LOAD_FAST                'seedlist'
               92  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 64