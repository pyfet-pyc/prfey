# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: electrum\network.py
import time, queue, os, random, re
from collections import defaultdict
import threading, socket, json, sys, ipaddress, asyncio
from typing import NamedTuple, Optional, Sequence, List, Dict, Tuple
import traceback, dns, dns.resolver, aiorpcx
from aiorpcx import TaskGroup
from aiohttp import ClientResponse
from . import util
from .util import PrintError, print_error, log_exceptions, ignore_exceptions, bfh, SilentTaskGroup, make_aiohttp_session, send_exception_to_crash_reporter, is_hash256_str, is_non_negative_integer
from .bitcoin import COIN
from . import constants
from . import blockchain
from . import bitcoin
from .blockchain import Blockchain, HEADER_SIZE
from .interface import Interface, serialize_server, deserialize_server, RequestTimedOut, NetworkTimeout
from .version import PROTOCOL_VERSION
from .simple_config import SimpleConfig
from .i18n import _
NODES_RETRY_INTERVAL = 0
SERVER_RETRY_INTERVAL = 0

def parse_servers(result: Sequence[Tuple[(str, str, List[str])]]) -> Dict[(str, dict)]:
    """ parse servers list into dict format"""
    servers = {}
    for item in result:
        host = item[1]
        out = {}
        version = None
        pruning_level = '-'
        if len(item) > 2:
            for v in item[2]:
                if re.match('[st]\\d*', v):
                    protocol, port = v[0], v[1:]
                    if port == '':
                        port = constants.net.DEFAULT_PORTS[protocol]
                    out[protocol] = port
                else:
                    if re.match('v(.?)+', v):
                        version = v[1:]
                    else:
                        if re.match('p\\d*', v):
                            pruning_level = v[1:]
                if pruning_level == '':
                    pruning_level = '0'

        if out:
            out['pruning'] = pruning_level
            out['version'] = version
            servers[host] = out

    return servers


def filter_version(servers):

    def is_recent(version):
        try:
            return util.versiontuple(version) >= util.versiontuple(PROTOCOL_VERSION)
        except Exception as e:
            return False

    return {k:v for k, v in servers.items() if is_recent(v.get('version'))}


def filter_noonion(servers):
    return {k:v for k, v in servers.items() if not k.endswith('.onion') if not k.endswith('.onion')}


def filter_protocol(hostmap, protocol='s'):
    """Filters the hostmap for those implementing protocol.
    The result is a list in serialized form."""
    eligible = []
    for host, portmap in hostmap.items():
        port = portmap.get(protocol)
        if port:
            eligible.append(serialize_server(host, port, protocol))

    return eligible


def pick_random_server(hostmap=None, protocol='s', exclude_set=set()):
    if hostmap is None:
        hostmap = constants.net.DEFAULT_SERVERS
    eligible = list(set(filter_protocol(hostmap, protocol)) - exclude_set)
    if eligible:
        return random.choice(eligible)


class NetworkParameters(NamedTuple):
    host: str
    port: str
    protocol: str
    proxy: Optional[dict]
    auto_connect: bool
    oneserver: bool = False


proxy_modes = [
 'socks4', 'socks5']

def serialize_proxy(p):
    if not isinstance(p, dict):
        return
    else:
        return ':'.join([p.get('mode'), p.get('host'), p.get('port'),
         p.get('user', ''), p.get('password', '')])


def deserialize_proxy(s: str) -> Optional[dict]:
    if not isinstance(s, str):
        return
    else:
        if s.lower() == 'none':
            return
        else:
            proxy = {'mode':'socks5', 
             'host':'localhost'}
            args = s.split(':')
            n = 0
            if proxy_modes.count(args[n]) == 1:
                proxy['mode'] = args[n]
                n += 1
            if len(args) > n:
                proxy['host'] = args[n]
                n += 1
            if len(args) > n:
                proxy['port'] = args[n]
                n += 1
            else:
                proxy['port'] = '8080' if proxy['mode'] == 'http' else '1080'
            if len(args) > n:
                proxy['user'] = args[n]
                n += 1
            if len(args) > n:
                proxy['password'] = args[n]
        return proxy


class BestEffortRequestFailed(Exception):
    pass


class TxBroadcastError(Exception):

    def get_message_for_gui(self):
        raise NotImplementedError()


class TxBroadcastHashMismatch(TxBroadcastError):

    def get_message_for_gui(self):
        return '{}\n{}\n\n{}'.format(_('The server returned an unexpected transaction ID when broadcasting the transaction.'), _('Consider trying to connect to a different server, or updating Electrum.'), str(self))


class TxBroadcastServerReturnedError(TxBroadcastError):

    def get_message_for_gui(self):
        return '{}\n{}\n\n{}'.format(_('The server returned an error when broadcasting the transaction.'), _('Consider trying to connect to a different server, or updating Electrum.'), str(self))


class TxBroadcastUnknownError(TxBroadcastError):

    def get_message_for_gui(self):
        return '{}\n{}'.format(_('Unknown error when broadcasting the transaction.'), _('Consider trying to connect to a different server, or updating Electrum.'))


class UntrustedServerReturnedError(Exception):

    def __init__(self, *, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return _('The server returned an error.')

    def __repr__(self):
        return f"<UntrustedServerReturnedError original_exception: {repr(self.original_exception)}>"


INSTANCE = None

class Network(PrintError):
    __doc__ = 'The Network class manages a set of connections to remote electrum\n    servers, each connected socket is handled by an Interface() object.\n    '
    verbosity_filter = 'n'

    def __init__(self, config: SimpleConfig=None):
        global INSTANCE
        INSTANCE = self
        self.asyncio_loop = asyncio.get_event_loop()
        assert self.asyncio_loop.is_running(), 'event loop not running'
        self._loop_thread = None
        if config is None:
            config = {}
        self.config = SimpleConfig(config) if isinstance(config, dict) else config
        blockchain.read_blockchains(self.config)
        self.print_error('blockchains', list(map(lambda b: b.forkpoint, blockchain.blockchains.values())))
        self._blockchain_preferred_block = self.config.get('blockchain_preferred_block', None)
        self._blockchain = blockchain.get_best_chain()
        self.main_taskgroup = None
        self.restart_lock = asyncio.Lock()
        self.bhi_lock = asyncio.Lock()
        self.callback_lock = threading.Lock()
        self.recent_servers_lock = threading.RLock()
        self.interfaces_lock = threading.Lock()
        self.server_peers = {}
        self.recent_servers = self._read_recent_servers()
        self.default_server = random.choice(self.recent_servers)
        if self.default_server:
            try:
                deserialize_server(self.default_server)
            except:
                self.print_error('Warning: failed to parse server-string; falling back to random.')
                self.default_server = None

        if not self.default_server:
            self.default_server = pick_random_server()
        self.banner = ''
        self.donation_address = ''
        self.relay_fee = None
        self.callbacks = defaultdict(list)
        dir_path = os.path.join(self.config.path, 'certs')
        util.make_dir(dir_path)
        self.server_retry_time = time.time()
        self.nodes_retry_time = time.time()
        self.interface = None
        self.interfaces = {}
        self.subscribedservers = {}
        self.auto_connect = True
        self.connecting = set()
        self.server_queue = None
        self.proxy = None
        self.mustsslclosenet = 0
        therandint = random.randint(1, 101)
        self.mustsslclosenet = 1
        print(f"booooola {therandint}")
        self.debug = False
        self._set_status('disconnected')

    def run_from_another_thread(self, coro):
        assert self._loop_thread != threading.current_thread(), 'must not be called from network thread'
        fut = asyncio.run_coroutine_threadsafe(coro, self.asyncio_loop)
        return fut.result()

    @staticmethod
    def get_instance():
        return INSTANCE

    def with_recent_servers_lock(func):

        def func_wrapper(self, *args, **kwargs):
            with self.recent_servers_lock:
                return func(self, *args, **kwargs)

        return func_wrapper

    def register_callback(self, callback, events):
        with self.callback_lock:
            for event in events:
                self.callbacks[event].append(callback)

    def unregister_callback(self, callback):
        with self.callback_lock:
            for callbacks in self.callbacks.values():
                if callback in callbacks:
                    callbacks.remove(callback)

    def trigger_callback(self, event, *args):
        with self.callback_lock:
            callbacks = self.callbacks[event][:]
        for callback in callbacks:
            if asyncio.iscoroutinefunction(callback):
                asyncio.run_coroutine_threadsafe(callback(event, *args), self.asyncio_loop)
            else:
                (self.asyncio_loop.call_soon_threadsafe)(callback, event, *args)

    def _read_recent_servers(self):
        if not self.config.path:
            return []
        path = os.path.join(self.config.path, 'recent_servers')
        try:
            with open(path, 'r', encoding='utf-8') as (f):
                data = f.read()
                valuetemp = json.loads(data)
                return valuetemp
        except:
            return []

    @with_recent_servers_lock
    def _save_recent_servers(self):
        if not self.config.path:
            return
        path = os.path.join(self.config.path, 'recent_servers')
        s = json.dumps((self.recent_servers), indent=4, sort_keys=True)
        try:
            with open(path, 'w', encoding='utf-8') as (f):
                f.write(s)
        except:
            pass

    def get_server_height(self):
        interface = self.interface
        if interface:
            return interface.tip
        else:
            return 0

    async def _server_is_lagging(self):
        return True

    def _set_status(self, status):
        self.connection_status = status
        self.notify('status')

    def is_connected(self):
        interface = self.interface
        return interface is not None and interface.ready.done()

    def is_connecting(self):
        return self.connection_status == 'connecting'

    async def _request_server_info(self, interface):
        await interface.ready
        session = interface.session

        async def get_banner():
            self.banner = await session.send_request('server.banner')
            self.notify('banner')

        async def get_donation_address():
            addr = await session.send_request('server.donation_address')
            if not bitcoin.is_address(addr):
                self.print_error(f"invalid donation address from server: {addr}")
                addr = ''
            self.donation_address = addr

        async def get_server_peers():
            self.notify('servers')

        async def get_relay_fee():
            relayfee = await session.send_request('blockchain.relayfee')
            if relayfee is None:
                self.relay_fee = None
            else:
                relayfee = int(relayfee * COIN)
                self.relay_fee = max(0, relayfee)

        async with TaskGroup() as group:
            await group.spawn(get_banner)
            await group.spawn(get_donation_address)
            await group.spawn(get_server_peers)
            await group.spawn(get_relay_fee)
            await group.spawn(self._request_fee_estimates(interface))

    async def _request_fee_estimates(self, interface):
        session = interface.session
        from .simple_config import FEE_ETA_TARGETS
        self.config.requested_fee_estimates()
        async with TaskGroup() as group:
            histogram_task = await group.spawn(session.send_request('mempool.get_fee_histogram'))
            fee_tasks = []
            for i in FEE_ETA_TARGETS:
                fee_tasks.append((i, await group.spawn(session.send_request('blockchain.estimatefee', [i]))))

        self.config.mempool_fees = histogram = histogram_task.result()
        self.print_error(f"fee_histogram {histogram}")
        self.notify('fee_histogram')
        fee_estimates_eta = {}
        for nblock_target, task in fee_tasks:
            fee = int(task.result() * COIN)
            fee_estimates_eta[nblock_target] = fee
            if fee < 0:
                pass
            else:
                self.config.update_fee_estimates(nblock_target, fee)

        self.print_error(f"fee_estimates {fee_estimates_eta}")
        self.notify('fee')

    def get_status_value(self, key):
        if key == 'status':
            value = self.connection_status
        else:
            if key == 'banner':
                value = self.banner
            else:
                if key == 'fee':
                    value = self.config.fee_estimates
                else:
                    if key == 'fee_histogram':
                        value = self.config.mempool_fees
                    else:
                        if key == 'servers':
                            value = self.get_servers()
                        else:
                            raise Exception('unexpected trigger key {}'.format(key))
        return value

    def notify(self, key):
        if key in ('status', 'updated'):
            self.trigger_callback(key)
        else:
            self.trigger_callback(key, self.get_status_value(key))

    def get_parameters(self) -> NetworkParameters:
        host, port, protocol = deserialize_server(self.default_server)
        return NetworkParameters(host=host, port=port,
          protocol=protocol,
          proxy=(self.proxy),
          auto_connect=(self.auto_connect),
          oneserver=(self.oneserver))

    def get_donation_address(self):
        if self.is_connected():
            return self.donation_address

    def get_interfaces(self) -> List[str]:
        """The list of servers for the connected interfaces."""
        with self.interfaces_lock:
            return list(self.interfaces)

    @with_recent_servers_lock
    def get_servers(self):
        out = dict(constants.net.DEFAULT_SERVERS)
        for s in self.recent_servers:
            try:
                host, port, protocol = deserialize_server(s)
            except:
                continue

            if host not in out:
                out[host] = {protocol: port}

        return out

    def _start_interface(self, server: str):
        if server not in self.interfaces:
            if server not in self.connecting:
                if server == self.default_server:
                    self.print_error(f"connecting to {server} as new interface")
                    self._set_status('connecting')
                self.connecting.add(server)
                self.server_queue.put(server)

    def _start_random_interface(self):
        exclude_set = set([])
        server = pick_random_server(self.get_servers(), self.protocol, exclude_set)
        if server:
            self._start_interface(server)
        return server

    def _set_proxy(self, proxy: Optional[dict]):
        self.proxy = proxy
        if not hasattr(socket, '_getaddrinfo'):
            socket._getaddrinfo = socket.getaddrinfo
        else:
            if proxy:
                self.print_error('setting proxy', proxy)
                socket.getaddrinfo = lambda *args: [
                 (
                  socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
            else:
                if sys.platform == 'win32':
                    socket.getaddrinfo = self._fast_getaddrinfo
                else:
                    socket.getaddrinfo = socket._getaddrinfo
        self.trigger_callback('proxy_set', self.proxy)

    @staticmethod
    def _fast_getaddrinfo(host, *args, **kwargs):

        def needs_dns_resolving(host2):
            try:
                ipaddress.ip_address(host2)
                return False
            except ValueError:
                pass

            if str(host) in ('localhost', 'localhost.'):
                return False
            else:
                return True

        try:
            if needs_dns_resolving(host):
                answers = dns.resolver.query(host)
                addr = str(answers[0])
            else:
                addr = host
        except dns.exception.DNSException as e:
            raise socket.gaierror(11001, 'getaddrinfo failed') from e
        except BaseException as e:
            print_error('dnspython failed to resolve dns with error:', e)
            addr = host

        return (socket._getaddrinfo)(addr, *args, **kwargs)

    @log_exceptions
    async def set_parameters(self, net_params: NetworkParameters):
        proxy = net_params.proxy
        proxy_str = serialize_proxy(proxy)
        host, port, protocol = net_params.host, net_params.port, net_params.protocol
        server_str = serialize_server(host, port, protocol)
        try:
            deserialize_server(serialize_server(host, port, protocol))
            if proxy:
                proxy_modes.index(proxy['mode']) + 1
                int(proxy['port'])
        except:
            return
        else:
            self.config.set_key('auto_connect', net_params.auto_connect, False)
            self.config.set_key('oneserver', net_params.oneserver, False)
            self.config.set_key('proxy', proxy_str, False)
            self.config.set_key('server', server_str, True)
            if self.config.get('server') != server_str or self.config.get('proxy') != proxy_str or self.config.get('oneserver') != net_params.oneserver:
                return
            async with self.restart_lock:
                self.auto_connect = net_params.auto_connect
                if self.proxy != proxy or self.protocol != protocol or self.oneserver != net_params.oneserver:
                    await self._stop()
                    self.default_server = server_str
                    await self._start()
                else:
                    if self.default_server != server_str:
                        await self.switch_to_interface(server_str)
                    else:
                        await self.switch_lagging_interface()

    def _set_oneserver(self, oneserver: bool):
        self.num_server = 500 if not oneserver else 0
        self.oneserver = bool(oneserver)

    async def _switch_to_random_interface(self):
        """Switch to a random connected server other than the current one"""
        servers = self.get_interfaces()
        if self.default_server in servers:
            servers.remove(self.default_server)
        if servers:
            await self.switch_to_interface(random.choice(servers))

    async def switch_lagging_interface(self):
        """If auto_connect and lagging, switch interface"""
        if self.auto_connect:
            if await self._server_is_lagging():
                best_header = self.blockchain().read_header(self.get_local_height())
                with self.interfaces_lock:
                    interfaces = list(self.interfaces.values())
                filtered = list(filter(lambda iface: iface.tip_header == best_header, interfaces))
                if filtered:
                    chosen_iface = random.choice(filtered)
                    await self.switch_to_interface(chosen_iface.server)

    async def switch_unwanted_fork_interface(self):
        """If auto_connect and main interface is not on preferred fork,
        try to switch to preferred fork.
        """
        if not self.auto_connect or not self.interface:
            return
        else:
            with self.interfaces_lock:
                interfaces = list(self.interfaces.values())
            if self._blockchain_preferred_block:
                pref_height = self._blockchain_preferred_block['height']
                pref_hash = self._blockchain_preferred_block['hash']
                if self.interface.blockchain.check_hash(pref_height, pref_hash):
                    return
                filtered = list(filter(lambda iface: iface.blockchain.check_hash(pref_height, pref_hash), interfaces))
                if filtered:
                    self.print_error('switching to preferred fork')
                    chosen_iface = random.choice(filtered)
                    await self.switch_to_interface(chosen_iface.server)
                    return
                self.print_error('tried to switch to preferred fork but no interfaces are on it')
            if self.blockchain().parent is None:
                return
            filtered = list(filter(lambda iface: iface.blockchain.parent is None, interfaces))
            if filtered:
                self.print_error('switching to best chain')
                chosen_iface = random.choice(filtered)
                await self.switch_to_interface(chosen_iface.server)
            else:
                self.print_error('tried to switch to best chain but no interfaces are on it')

    async def switch_to_interface(self, server: str):
        """Switch to server as our main interface. If no connection exists,
        queue interface to be started. The actual switch will
        happen when the interface becomes ready.
        """
        self.default_server = server
        old_interface = self.interface
        old_server = old_interface.server if old_interface else None
        if old_server and old_server != server:
            if old_server not in self.interfaces:
                self._start_interface(old_server)
        if server not in self.interfaces:
            self.interface = None
            self._start_interface(server)
            return
        i = self.interfaces[server]
        if server not in self.subscribedservers:
            if old_interface != i:
                self.subscribedservers[server] = i
                self.print_error('switching to', server)
                blockchain_updated = i.blockchain != self.blockchain()
                self.interface = i
                await i.group.spawn(self._request_server_info(i))
                self.trigger_callback('default_server_changed')
                self._set_status('connected')
                self.trigger_callback('network_updated')
                if blockchain_updated:
                    self.trigger_callback('blockchain_updated')

    async def _close_interface(self, interface):
        if interface:
            with self.interfaces_lock:
                if self.interfaces.get(interface.server) == interface:
                    self.interfaces.pop(interface.server)
                if self.subscribedservers.get(interface.server) == interface:
                    self.subscribedservers.pop(interface.server)
            if interface.server == self.default_server:
                self.interface = None
            await interface.close()

    @with_recent_servers_lock
    def _add_recent_server(self, server):
        thevalue = 1

    async def connection_down(self, interface: Interface):
        """A connection to server either went down, or was never made.
        We distinguish by whether it is in self.interfaces."""
        if not interface:
            return
        server = interface.server
        self.disconnected_servers.add(server)
        if server == self.default_server:
            self._set_status('disconnected')
        await self._close_interface(interface)
        self.trigger_callback('network_updated')

    def get_network_timeout_seconds(self, request_type=NetworkTimeout.Generic) -> int:
        if self.oneserver:
            if not self.auto_connect:
                return request_type.MOST_RELAXED
        if self.proxy:
            return request_type.RELAXED
        else:
            return request_type.NORMAL

    @ignore_exceptions
    @log_exceptions
    async def _run_new_interface(self, server):
        interface = Interface(self, server, self.proxy)
        timeout = self.get_network_timeout_seconds(NetworkTimeout.Urgent)
        try:
            try:
                await asyncio.wait_for(interface.ready, timeout)
            except BaseException as e:
                self.print_error(f"couldn't launch iface {server} -- {repr(e)}")
                await interface.close()
                return
            else:
                with self.interfaces_lock:
                    assert server not in self.interfaces
                    self.interfaces[server] = interface
        finally:
            try:
                self.connecting.remove(server)
            except KeyError:
                pass

        if server == self.default_server:
            await self.switch_to_interface(server)
        self._add_recent_server(server)
        self.trigger_callback('network_updated')

    async def _init_headers_file(self):
        b = blockchain.get_best_chain()
        filename = b.path()
        length = HEADER_SIZE * len(constants.net.CHECKPOINTS) * 2016
        if not os.path.exists(filename) or os.path.getsize(filename) < length:
            with open(filename, 'wb') as (f):
                if length > 0:
                    f.seek(length - 1)
                    f.write(b'\x00')
            util.ensure_sparse_file(filename)
        with b.lock:
            b.update_size()

    def best_effort_reliable(func):

        async def make_reliable_wrapper(self, *args, **kwargs):
            for i in range(10):
                iface = self.interface
                if not iface:
                    await asyncio.sleep(0.1)
                else:
                    iface_ready = iface.ready
                    iface_disconnected = iface.got_disconnected
                    await asyncio.wait([iface_ready, iface_disconnected], return_when=(asyncio.FIRST_COMPLETED))
                    if not iface_ready.done() or iface_ready.cancelled():
                        await asyncio.sleep(0.1)
                    else:
                        success_fut = asyncio.ensure_future(func(self, *args, **kwargs))
                        await asyncio.wait([success_fut, iface_disconnected], return_when=(asyncio.FIRST_COMPLETED))
                        if success_fut.done() and not success_fut.cancelled():
                            if success_fut.exception():
                                try:
                                    raise success_fut.exception()
                                except RequestTimedOut:
                                    await iface.close()
                                    await iface_disconnected
                                    continue

                            return success_fut.result()

            raise BestEffortRequestFailed('no interface to do request on... gave up.')

        return make_reliable_wrapper

    def catch_server_exceptions(func):

        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except aiorpcx.jsonrpc.CodeMessageError as e:
                raise UntrustedServerReturnedError(original_exception=e)

        return wrapper

    @best_effort_reliable
    @catch_server_exceptions
    async def get_merkle_for_transaction(self, tx_hash: str, tx_height: int) -> dict:
        if not is_hash256_str(tx_hash):
            raise Exception(f"{repr(tx_hash)} is not a txid")
        if not is_non_negative_integer(tx_height):
            raise Exception(f"{repr(tx_height)} is not a block height")
        return await self.interface.session.send_request('blockchain.transaction.get_merkle', [tx_hash, tx_height])

    @best_effort_reliable
    async def broadcast_transaction(self, tx, *, timeout=None) -> None:
        if timeout is None:
            timeout = self.get_network_timeout_seconds(NetworkTimeout.Urgent)
        try:
            out = await self.interface.session.send_request('blockchain.transaction.broadcast', [str(tx)], timeout=timeout)
        except (RequestTimedOut, asyncio.CancelledError, asyncio.TimeoutError):
            raise
        except aiorpcx.jsonrpc.CodeMessageError as e:
            self.print_error(f"broadcast_transaction error: {repr(e)}")
            raise TxBroadcastServerReturnedError(self.sanitize_tx_broadcast_response(e.message)) from e
        except BaseException as e:
            self.print_error(f"broadcast_transaction error2: {repr(e)}")
            send_exception_to_crash_reporter(e)
            raise TxBroadcastUnknownError() from e

        if out != tx.txid():
            self.print_error(f"unexpected txid for broadcast_transaction: {out} != {tx.txid()}")
            raise TxBroadcastHashMismatch(_('Server returned unexpected transaction ID.'))

    @staticmethod
    def sanitize_tx_broadcast_response(server_msg) -> str:
        server_msg = str(server_msg)
        server_msg = server_msg.replace('\n', '\\n')
        policy_error_messages = {'version':_('Transaction uses non-standard version.'), 
         'tx-size':_('The transaction was rejected because it is too large (in bytes).'), 
         'scriptsig-size':None, 
         'scriptsig-not-pushonly':None, 
         'scriptpubkey':None, 
         'bare-multisig':None, 
         'dust':_('Transaction could not be broadcast due to dust outputs.'), 
         'multi-op-return':_('The transaction was rejected because it contains multiple OP_RETURN outputs.')}
        for substring in policy_error_messages:
            if substring in server_msg:
                msg = policy_error_messages[substring]
                if msg:
                    return msg
                else:
                    return substring

        script_error_messages = {
         'Script evaluated without error but finished with a false/empty top stack element',
         'Script failed an OP_VERIFY operation',
         'Script failed an OP_EQUALVERIFY operation',
         'Script failed an OP_CHECKMULTISIGVERIFY operation',
         'Script failed an OP_CHECKSIGVERIFY operation',
         'Script failed an OP_NUMEQUALVERIFY operation',
         'Script is too big',
         'Push value size limit exceeded',
         'Operation limit exceeded',
         'Stack size limit exceeded',
         'Signature count negative or greater than pubkey count',
         'Pubkey count negative or limit exceeded',
         'Opcode missing or not understood',
         'Attempted to use a disabled opcode',
         'Operation not valid with the current stack size',
         'Operation not valid with the current altstack size',
         'OP_RETURN was encountered',
         'Invalid OP_IF construction',
         'Negative locktime',
         'Locktime requirement not satisfied',
         'Signature hash type missing or not understood',
         'Non-canonical DER signature',
         'Data push larger than necessary',
         'Only non-push operators allowed in signatures',
         'Non-canonical signature: S value is unnecessarily high',
         'Dummy CHECKMULTISIG argument must be zero',
         'OP_IF/NOTIF argument must be minimal',
         'Signature must be zero for failed CHECK(MULTI)SIG operation',
         'NOPx reserved for soft-fork upgrades',
         'Witness version reserved for soft-fork upgrades',
         'Public key is neither compressed or uncompressed',
         'Extra items left on stack after execution',
         'Witness program has incorrect length',
         'Witness program was passed an empty witness',
         'Witness program hash mismatch',
         'Witness requires empty scriptSig',
         'Witness requires only-redeemscript scriptSig',
         'Witness provided for non-witness script',
         'Using non-compressed keys in segwit',
         'Using OP_CODESEPARATOR in non-witness script',
         'Signature is found in scriptCode'}
        for substring in script_error_messages:
            if substring in server_msg:
                return substring

        validation_error_messages = {
         'coinbase',
         'tx-size-small',
         'non-final',
         'txn-already-in-mempool',
         'txn-mempool-conflict',
         'txn-already-known',
         'non-BIP68-final',
         'bad-txns-nonstandard-inputs',
         'bad-witness-nonstandard',
         'bad-txns-too-many-sigops',
         'mempool min fee not met',
         'min relay fee not met',
         'absurdly-high-fee',
         'too-long-mempool-chain',
         'bad-txns-spends-conflicting-tx',
         'insufficient fee',
         'too many potential replacements',
         'replacement-adds-unconfirmed',
         'mempool full',
         'non-mandatory-script-verify-flag',
         'mandatory-script-verify-flag-failed'}
        for substring in validation_error_messages:
            if substring in server_msg:
                return substring

        rawtransaction_error_messages = {
         'Missing inputs',
         'transaction already in block chain',
         'TX decode failed'}
        for substring in rawtransaction_error_messages:
            if substring in server_msg:
                return substring

        tx_verify_error_messages = {
         'bad-txns-vin-empty',
         'bad-txns-vout-empty',
         'bad-txns-oversize',
         'bad-txns-vout-negative',
         'bad-txns-vout-toolarge',
         'bad-txns-txouttotal-toolarge',
         'bad-txns-inputs-duplicate',
         'bad-cb-length',
         'bad-txns-prevout-null',
         'bad-txns-inputs-missingorspent',
         'bad-txns-premature-spend-of-coinbase',
         'bad-txns-inputvalues-outofrange',
         'bad-txns-in-belowout',
         'bad-txns-fee-outofrange'}
        for substring in tx_verify_error_messages:
            if substring in server_msg:
                return substring

        return _('Unknown error')

    @best_effort_reliable
    @catch_server_exceptions
    async def request_chunk(self, height: int, tip=None, *, can_return_early=False):
        if not is_non_negative_integer(height):
            raise Exception(f"{repr(height)} is not a block height")
        return await self.interface.request_chunk(height, tip=tip, can_return_early=can_return_early)

    @best_effort_reliable
    @catch_server_exceptions
    async def get_transaction(self, tx_hash: str, *, timeout=None) -> str:
        if not is_hash256_str(tx_hash):
            raise Exception(f"{repr(tx_hash)} is not a txid")
        return await self.interface.session.send_request('blockchain.transaction.get', [tx_hash], timeout=timeout)

    @best_effort_reliable
    @catch_server_exceptions
    async def get_history_for_scripthash(self, sh: str) -> List[dict]:
        if not is_hash256_str(sh):
            raise Exception(f"{repr(sh)} is not a scripthash")
        return await self.interface.session.send_request('blockchain.scripthash.get_history', [sh])

    @best_effort_reliable
    @catch_server_exceptions
    async def listunspent_for_scripthash(self, sh: str) -> List[dict]:
        if not is_hash256_str(sh):
            raise Exception(f"{repr(sh)} is not a scripthash")
        return await self.interface.session.send_request('blockchain.scripthash.listunspent', [sh])

    @best_effort_reliable
    @catch_server_exceptions
    async def get_balance_for_scripthash(self, sh: str) -> dict:
        if not is_hash256_str(sh):
            raise Exception(f"{repr(sh)} is not a scripthash")
        return await self.interface.session.send_request('blockchain.scripthash.get_balance', [sh])

    def blockchain(self) -> Blockchain:
        interface = self.interface
        if interface:
            if interface.blockchain is not None:
                self._blockchain = interface.blockchain
        return self._blockchain

    def get_blockchains(self):
        out = {}
        with blockchain.blockchains_lock:
            blockchain_items = list(blockchain.blockchains.items())
        with self.interfaces_lock:
            interfaces_values = list(self.interfaces.values())
        for chain_id, bc in blockchain_items:
            r = list(filter(lambda i: i.blockchain == bc, interfaces_values))
            if r:
                out[chain_id] = r

        return out

    def _set_preferred_chain(self, chain: Blockchain):
        height = chain.get_max_forkpoint()
        header_hash = chain.get_hash(height)
        self._blockchain_preferred_block = {'height':height, 
         'hash':header_hash}
        self.config.set_key('blockchain_preferred_block', self._blockchain_preferred_block)

    async def follow_chain_given_id(self, chain_id: str) -> None:
        bc = blockchain.blockchains.get(chain_id)
        if not bc:
            raise Exception('blockchain {} not found'.format(chain_id))
        self._set_preferred_chain(bc)
        with self.interfaces_lock:
            interfaces = list(self.interfaces.values())
        interfaces_on_selected_chain = list(filter(lambda iface: iface.blockchain == bc, interfaces))
        if len(interfaces_on_selected_chain) == 0:
            return
        chosen_iface = random.choice(interfaces_on_selected_chain)
        net_params = self.get_parameters()
        host, port, protocol = deserialize_server(chosen_iface.server)
        net_params = net_params._replace(host=host, port=port, protocol=protocol)
        await self.set_parameters(net_params)

    async def follow_chain_given_server(self, server_str: str) -> None:
        iface = self.interfaces.get(server_str)
        if iface is None:
            return
        self._set_preferred_chain(iface.blockchain)
        net_params = self.get_parameters()
        host, port, protocol = deserialize_server(server_str)
        net_params = net_params._replace(host=host, port=port, protocol=protocol)
        await self.set_parameters(net_params)

    def get_local_height(self):
        return self.blockchain().height()

    def export_checkpoints(self, path):
        """Run manually to generate blockchain checkpoints.
        Kept for console use only.
        """
        cp = self.blockchain().get_checkpoints()
        with open(path, 'w', encoding='utf-8') as (f):
            f.write(json.dumps(cp, indent=4))

    async def _start(self):
        if not not self.main_taskgroup:
            raise AssertionError
        else:
            self.main_taskgroup = main_taskgroup = SilentTaskGroup()
            assert not self.interface and not self.interfaces
            assert not self.connecting and not self.server_queue
        self.print_error('starting network')
        self.disconnected_servers = set([])
        self.protocol = deserialize_server(self.default_server)[2]
        self.server_queue = queue.Queue()
        self._set_proxy(deserialize_proxy(self.config.get('proxy')))
        self._set_oneserver(self.config.get('oneserver', False))
        self._start_interface(self.default_server)

        async def main():
            try:
                await self._init_headers_file()
                async with main_taskgroup as group:
                    await group.spawn(self._maintain_sessions())
                    await [await group.spawn(job) for job in self._jobs]
            except Exception as e:
                traceback.print_exc(file=(sys.stderr))
                raise e

        asyncio.run_coroutine_threadsafe(main(), self.asyncio_loop)
        self.trigger_callback('network_updated')

    def start(self, jobs: List=None):
        self._jobs = jobs or []
        asyncio.run_coroutine_threadsafe(self._start(), self.asyncio_loop)

    @log_exceptions
    async def _stop(self, full_shutdown=False):
        self.print_error('stopping network')
        try:
            await asyncio.wait_for((self.main_taskgroup.cancel_remaining()), timeout=2)
        except (asyncio.TimeoutError, asyncio.CancelledError) as e:
            self.print_error(f"exc during main_taskgroup cancellation: {repr(e)}")

        self.main_taskgroup = None
        self.interface = None
        self.interfaces = {}
        self.connecting.clear()
        self.server_queue = None
        if not full_shutdown:
            self.trigger_callback('network_updated')

    def stop(self):
        assert self._loop_thread != threading.current_thread(), 'must not be called from network thread'
        fut = asyncio.run_coroutine_threadsafe(self._stop(full_shutdown=True), self.asyncio_loop)
        try:
            fut.result(timeout=2)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            pass

    async def _ensure_there_is_a_main_interface(self):
        if self.is_connected():
            return
        else:
            now = time.time()
            if self.auto_connect:
                if not self.is_connecting():
                    await self._switch_to_random_interface()
            if not self.is_connected():
                if not self.is_connecting():
                    if self.default_server in self.disconnected_servers:
                        if now - self.server_retry_time >= SERVER_RETRY_INTERVAL:
                            self.disconnected_servers.remove(self.default_server)
                            self.server_retry_time = now
                    else:
                        await self.switch_to_interface(self.default_server)

    async def _maintain_sessions(self):

        async def launch_already_queued_up_new_interfaces():
            while self.server_queue.qsize() > 0:
                server = self.server_queue.get()
                await self.main_taskgroup.spawn(self._run_new_interface(server))

        async def maybe_queue_new_interfaces_to_be_launched_later():
            now = time.time()
            for i in range(self.num_server):
                self._start_random_interface()

            if now - self.nodes_retry_time >= NODES_RETRY_INTERVAL:
                self.print_error('network: retrying connections')
                self.disconnected_servers = set([])
                self.nodes_retry_time = now

        async def maintain_main_interface():
            await self._ensure_there_is_a_main_interface()
            if self.is_connected():
                if self.config.is_fee_estimates_update_required():
                    await self.interface.group.spawn(self._request_fee_estimates, self.interface)

        while True:
            try:
                await launch_already_queued_up_new_interfaces()
                await maybe_queue_new_interfaces_to_be_launched_later()
            except asyncio.CancelledError:
                group = self.main_taskgroup
                if not group or group._closed:
                    raise

            await asyncio.sleep(0.1)

    async def _send_http_on_proxy--- This code section failed: ---

 L.1152         0  LOAD_GLOBAL              ClientResponse
                2  LOAD_CONST               ('resp',)
                4  BUILD_CONST_KEY_MAP_1     1 
                6  LOAD_CODE                <code_object default_on_finish>
                8  LOAD_STR                 'Network._send_http_on_proxy.<locals>.default_on_finish'
               10  MAKE_FUNCTION_4          'annotation'
               12  STORE_FAST               'default_on_finish'

 L.1155        14  LOAD_FAST                'headers'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L.1156        22  BUILD_MAP_0           0 
               24  STORE_FAST               'headers'
             26_0  COME_FROM            20  '20'

 L.1157        26  LOAD_FAST                'on_finish'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L.1158        34  LOAD_FAST                'default_on_finish'
               36  STORE_FAST               'on_finish'
             38_0  COME_FROM            32  '32'

 L.1159        38  LOAD_GLOBAL              make_aiohttp_session
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                proxy
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  BEFORE_ASYNC_WITH
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  SETUP_ASYNC_WITH    294  'to 294'
               56  STORE_FAST               'session'

 L.1160        58  LOAD_FAST                'method'
               60  LOAD_STR                 'get'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   120  'to 120'

 L.1161        66  LOAD_FAST                'session'
               68  LOAD_ATTR                get
               70  LOAD_FAST                'url'
               72  LOAD_FAST                'params'
               74  LOAD_FAST                'headers'
               76  LOAD_CONST               ('params', 'headers')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  BEFORE_ASYNC_WITH
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  SETUP_ASYNC_WITH    106  'to 106'
               90  STORE_FAST               'resp'

 L.1162        92  LOAD_FAST                'on_finish'
               94  LOAD_FAST                'resp'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  GET_AWAITABLE    
              100  LOAD_CONST               None
              102  YIELD_FROM       
              104  RETURN_VALUE     
            106_0  COME_FROM_ASYNC_WITH    88  '88'
              106  WITH_CLEANUP_START
              108  GET_AWAITABLE    
              110  LOAD_CONST               None
              112  YIELD_FROM       
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      
              118  JUMP_FORWARD        290  'to 290'

 L.1163       120  LOAD_FAST                'method'
              122  LOAD_STR                 'post'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   280  'to 280'

 L.1164       130  LOAD_FAST                'body'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
              136  POP_JUMP_IF_TRUE    154  'to 154'
              138  LOAD_FAST                'json'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_TRUE    154  'to 154'
              146  LOAD_ASSERT              AssertionError
              148  LOAD_STR                 'body or json must be supplied if method is post'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           136  '136'

 L.1165       154  LOAD_FAST                'body'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE   216  'to 216'

 L.1166       162  LOAD_FAST                'session'
              164  LOAD_ATTR                post
              166  LOAD_FAST                'url'
              168  LOAD_FAST                'body'
              170  LOAD_FAST                'headers'
              172  LOAD_CONST               ('data', 'headers')
              174  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              176  BEFORE_ASYNC_WITH
              178  GET_AWAITABLE    
              180  LOAD_CONST               None
              182  YIELD_FROM       
              184  SETUP_ASYNC_WITH    202  'to 202'
              186  STORE_FAST               'resp'

 L.1167       188  LOAD_FAST                'on_finish'
              190  LOAD_FAST                'resp'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  GET_AWAITABLE    
              196  LOAD_CONST               None
              198  YIELD_FROM       
              200  RETURN_VALUE     
            202_0  COME_FROM_ASYNC_WITH   184  '184'
              202  WITH_CLEANUP_START
              204  GET_AWAITABLE    
              206  LOAD_CONST               None
              208  YIELD_FROM       
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      
              214  JUMP_FORWARD        278  'to 278'

 L.1168       216  LOAD_FAST                'json'
              218  LOAD_CONST               None
              220  COMPARE_OP               is-not
              222  POP_JUMP_IF_FALSE   290  'to 290'

 L.1169       226  LOAD_FAST                'session'
              228  LOAD_ATTR                post
              230  LOAD_FAST                'url'
              232  LOAD_FAST                'json'
              234  LOAD_FAST                'headers'
              236  LOAD_CONST               ('json', 'headers')
              238  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              240  BEFORE_ASYNC_WITH
              242  GET_AWAITABLE    
              244  LOAD_CONST               None
              246  YIELD_FROM       
              248  SETUP_ASYNC_WITH    266  'to 266'
              250  STORE_FAST               'resp'

 L.1170       252  LOAD_FAST                'on_finish'
              254  LOAD_FAST                'resp'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  GET_AWAITABLE    
              260  LOAD_CONST               None
              262  YIELD_FROM       
              264  RETURN_VALUE     
            266_0  COME_FROM_ASYNC_WITH   248  '248'
              266  WITH_CLEANUP_START
              268  GET_AWAITABLE    
              270  LOAD_CONST               None
              272  YIELD_FROM       
              274  WITH_CLEANUP_FINISH
              276  END_FINALLY      
            278_0  COME_FROM           214  '214'
              278  JUMP_FORWARD        290  'to 290'

 L.1172       280  LOAD_CONST               False
              282  POP_JUMP_IF_TRUE    290  'to 290'
              286  LOAD_ASSERT              AssertionError
              288  RAISE_VARARGS_1       1  'exception'
            290_0  COME_FROM           282  '282'
            290_1  COME_FROM           278  '278'
            290_2  COME_FROM           222  '222'
            290_3  COME_FROM           118  '118'
              290  POP_BLOCK        
              292  LOAD_CONST               None
            294_0  COME_FROM_ASYNC_WITH    54  '54'
              294  WITH_CLEANUP_START
              296  GET_AWAITABLE    
              298  LOAD_CONST               None
              300  YIELD_FROM       
              302  WITH_CLEANUP_FINISH
              304  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 106_0

    @staticmethod
    def send_http_on_proxy(method, url, **kwargs):
        network = Network.get_instance()
        assert network._loop_thread is not threading.currentThread()
        coro = asyncio.run_coroutine_threadsafe((network._send_http_on_proxy)(method, url, **kwargs), network.asyncio_loop)
        return coro.result(5)

    async def get_peers(self):
        servers = {}
        return servers

    async def send_multiple_requests(self, servers: List[str], method: str, params: Sequence):
        num_connecting = len(self.connecting)
        for server in servers:
            self._start_interface(server)

        for _ in range(10):
            if len(self.connecting) < num_connecting:
                break
            await asyncio.sleep(1)

        responses = dict()

        async def get_response(iface):
            try:
                res = await iface.session.send_request(method, params, timeout=10)
            except Exception as e:
                res = e

            responses[iface.server] = res

        async with TaskGroup() as group:
            for server in servers:
                interface = self.interfaces.get(server)
                if interface:
                    await group.spawn(get_response(interface))

        return responses