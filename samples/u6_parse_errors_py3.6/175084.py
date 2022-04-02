# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: electrum\interface.py
import os, re, ssl, sys, traceback, asyncio
from typing import Tuple, Union, List, TYPE_CHECKING, Optional
from collections import defaultdict
import aiorpcx
from aiorpcx import RPCSession, Notification
import certifi
from .util import PrintError, ignore_exceptions, log_exceptions, bfh, SilentTaskGroup
from . import util
from . import x509
from . import pem
from . import version
from . import blockchain
from .blockchain import Blockchain
from . import constants
from .i18n import _
if TYPE_CHECKING:
    from .network import Network
ca_path = certifi.where()

class NetworkTimeout:

    class Generic:
        NORMAL = 30
        RELAXED = 45
        MOST_RELAXED = 180

    class Urgent(Generic):
        NORMAL = 10
        RELAXED = 20
        MOST_RELAXED = 60


class NotificationSession(RPCSession):

    def __init__(self, *args, **kwargs):
        (super(NotificationSession, self).__init__)(*args, **kwargs)
        self.subscriptions = defaultdict(list)
        self.cache = {}
        self.in_flight_requests_semaphore = asyncio.Semaphore(100)
        self.default_timeout = NetworkTimeout.Generic.NORMAL
        self._msg_counter = 0
        self.interface = None

    def _get_and_inc_msg_counter(self):
        self._msg_counter += 1
        return self._msg_counter

    async def handle_request(self, request):
        self.maybe_log(f"--> {request}")
        if isinstance(request, Notification):
            params, result = request.args[:-1], request.args[(-1)]
            key = self.get_hashable_key_for_rpc_call(request.method, params)
            if key in self.subscriptions:
                self.cache[key] = result
                for queue in self.subscriptions[key]:
                    await queue.put(request.args)

            else:
                raise Exception('unexpected request: {}'.format(repr(request)))

    async def send_request(self, *args, timeout=None, **kwargs):
        if timeout is None:
            timeout = self.default_timeout
        async with self.in_flight_requests_semaphore:
            msg_id = self._get_and_inc_msg_counter()
            self.maybe_log(f"<-- {args} {kwargs} (id: {msg_id})")
            try:
                response = await asyncio.wait_for((super().send_request)(*args, **kwargs), timeout)
            except asyncio.TimeoutError as e:
                raise RequestTimedOut(f"request timed out: {args} (id: {msg_id})") from e
            else:
                self.maybe_log(f"--> {response} (id: {msg_id})")
                return response

    async def subscribe(self, method: str, params: List, queue: asyncio.Queue):
        key = self.get_hashable_key_for_rpc_call(method, params)
        self.subscriptions[key].append(queue)
        if key in self.cache:
            result = self.cache[key]
        else:
            result = await self.send_request(method, params)
            self.cache[key] = result
        await queue.put(params + [result])

    def unsubscribe(self, queue):
        """Unsubscribe a callback to free object references to enable GC."""
        for v in self.subscriptions.values():
            if queue in v:
                v.remove(queue)

    @classmethod
    def get_hashable_key_for_rpc_call(cls, method, params):
        """Hashable index for subscriptions and cache"""
        return str(method) + repr(params)

    def maybe_log(self, msg: str) -> None:
        if not self.interface:
            return
        if self.interface.debug or self.interface.network.debug:
            self.interface.print_error(msg)


class GracefulDisconnect(Exception):
    pass


class RequestTimedOut(GracefulDisconnect):

    def __str__(self):
        return _('Network request timed out.')


class ErrorParsingSSLCert(Exception):
    pass


class ErrorGettingSSLCertFromServer(Exception):
    pass


def deserialize_server(server_str: str) -> Tuple[(str, str, str)]:
    host, port, protocol = str(server_str).rsplit(':', 2)
    if not host:
        raise ValueError('host must not be empty')
    if protocol not in ('s', 't'):
        raise ValueError('invalid network protocol: {}'.format(protocol))
    int(port)
    if not 0 < int(port) < 65536:
        raise ValueError('port {} is out of valid range'.format(port))
    return (
     host, port, protocol)


def serialize_server(host: str, port: Union[(str, int)], protocol: str) -> str:
    return str(':'.join([host, str(port), protocol]))


class Interface(PrintError):
    verbosity_filter = 'i'

    def __init__(self, network: 'Network', server: str, proxy: Optional[dict]):
        self.ready = asyncio.Future()
        self.got_disconnected = asyncio.Future()
        self.server = server
        self.host, self.port, self.protocol = deserialize_server(self.server)
        self.port = int(self.port)
        assert network.config.path
        self.cert_path = os.path.join(network.config.path, 'certs', self.host)
        self.blockchain = None
        self._requested_chunks = set()
        self.network = network
        self._set_proxy(proxy)
        self.session = None
        self.tip_header = None
        self.tip = 0
        self.debug = False
        asyncio.run_coroutine_threadsafe(self.network.main_taskgroup.spawn(self.run()), self.network.asyncio_loop)
        self.group = SilentTaskGroup()

    def diagnostic_name(self):
        return self.host

    def _set_proxy(self, proxy: dict):
        if proxy:
            username, pw = proxy.get('user'), proxy.get('password')
            if not username or not pw:
                auth = None
            else:
                auth = aiorpcx.socks.SOCKSUserAuth(username, pw)
            if proxy['mode'] == 'socks4':
                self.proxy = aiorpcx.socks.SOCKSProxy((proxy['host'], int(proxy['port'])), aiorpcx.socks.SOCKS4a, auth)
            else:
                if proxy['mode'] == 'socks5':
                    self.proxy = aiorpcx.socks.SOCKSProxy((proxy['host'], int(proxy['port'])), aiorpcx.socks.SOCKS5, auth)
                else:
                    raise NotImplementedError
        else:
            self.proxy = None

    async def is_server_ca_signed(self, sslc):
        try:
            await self.open_session(sslc, exit_early=True)
        except ssl.SSLError as e:
            assert e.reason == 'CERTIFICATE_VERIFY_FAILED'
            return False

        return True

    async def _try_saving_ssl_cert_for_first_time(self, ca_ssl_context):
        try:
            ca_signed = await self.is_server_ca_signed(ca_ssl_context)
        except (OSError, aiorpcx.socks.SOCKSError) as e:
            raise ErrorGettingSSLCertFromServer(e) from e

        if ca_signed:
            with open(self.cert_path, 'w') as (f):
                f.write('')
        else:
            await self.save_certificate()

    def _is_saved_ssl_cert_available(self):
        if not os.path.exists(self.cert_path):
            return False
        else:
            with open(self.cert_path, 'r') as (f):
                contents = f.read()
            if contents == '':
                return True
            try:
                b = pem.dePem(contents, 'CERTIFICATE')
            except SyntaxError as e:
                self.print_error('error parsing already saved cert:', e)
                raise ErrorParsingSSLCert(e) from e

        try:
            x = x509.X509(b)
        except Exception as e:
            self.print_error('error parsing already saved cert:', e)
            raise ErrorParsingSSLCert(e) from e

        try:
            x.check_date()
            return True
        except x509.CertificateError as e:
            self.print_error('certificate has expired:', e)
            os.unlink(self.cert_path)
            return False

    async def _get_ssl_context(self):
        if self.protocol != 's':
            return
        else:
            ca_sslc = ssl.create_default_context(purpose=(ssl.Purpose.SERVER_AUTH), cafile=ca_path)
            if not self._is_saved_ssl_cert_available():
                await self._try_saving_ssl_cert_for_first_time(ca_sslc)
            siz = os.stat(self.cert_path).st_size
            if siz == 0:
                sslc = ca_sslc
            else:
                sslc = ssl.create_default_context((ssl.Purpose.SERVER_AUTH), cafile=(self.cert_path))
                sslc.check_hostname = 0
            return sslc

    def handle_disconnect(func):

        async def wrapper_func(self, *args, **kwargs):
            try:
                try:
                    return await func(self, *args, **kwargs)
                except GracefulDisconnect as e:
                    self.print_error('disconnecting gracefully. {}'.format(repr(e)))

            finally:
                await self.network.connection_down(self)
                self.got_disconnected.set_result(1)

        return wrapper_func

    @ignore_exceptions
    @log_exceptions
    @handle_disconnect
    async def run(self):
        try:
            ssl_context = await self._get_ssl_context()
        except (ErrorParsingSSLCert, ErrorGettingSSLCertFromServer) as e:
            self.print_error('disconnecting due to: {}'.format(repr(e)))
            return

        try:
            await self.open_session(ssl_context)
        except (asyncio.CancelledError, OSError, aiorpcx.socks.SOCKSError) as e:
            self.print_error('disconnecting due to: {}'.format(repr(e)))
            return

    def mark_ready(self):
        if self.ready.cancelled():
            raise GracefulDisconnect('conn establishment was too slow; *ready* future was cancelled')
        else:
            if self.ready.done():
                return
            else:
                assert self.tip_header
                chain = blockchain.check_header(self.tip_header)
                if not chain:
                    self.blockchain = blockchain.get_best_chain()
                else:
                    self.blockchain = chain
            assert self.blockchain is not None
        self.print_error('set blockchain with height', self.blockchain.height())
        self.ready.set_result(1)

    async def save_certificate(self):
        if not os.path.exists(self.cert_path):
            for _ in range(10):
                dercert = await self.get_certificate()
                if dercert:
                    self.print_error('succeeded in getting cert')
                    with open(self.cert_path, 'w') as (f):
                        cert = ssl.DER_cert_to_PEM_cert(dercert)
                        cert = re.sub('([^\n])-----END CERTIFICATE-----', '\\1\n-----END CERTIFICATE-----', cert)
                        f.write(cert)
                        f.flush()
                        os.fsync(f.fileno())
                    break
                await asyncio.sleep(1)
            else:
                raise Exception('could not get certificate')

    async def get_certificate--- This code section failed: ---

 L. 353         0  LOAD_GLOBAL              ssl
                2  LOAD_ATTR                SSLContext
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'sslc'

 L. 354         8  SETUP_EXCEPT         80  'to 80'

 L. 355        10  LOAD_GLOBAL              aiorpcx
               12  LOAD_ATTR                Connector
               14  LOAD_GLOBAL              RPCSession

 L. 356        16  LOAD_FAST                'self'
               18  LOAD_ATTR                host
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                port

 L. 357        24  LOAD_FAST                'sslc'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                proxy
               30  LOAD_CONST               ('host', 'port', 'ssl', 'proxy')
               32  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               34  BEFORE_ASYNC_WITH
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  SETUP_ASYNC_WITH     64  'to 64'
               44  STORE_FAST               'session'

 L. 358        46  LOAD_FAST                'session'
               48  LOAD_ATTR                transport
               50  LOAD_ATTR                _ssl_protocol
               52  LOAD_ATTR                _sslpipe
               54  LOAD_ATTR                _sslobj
               56  LOAD_ATTR                getpeercert
               58  LOAD_CONST               True
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RETURN_VALUE     
             64_0  COME_FROM_ASYNC_WITH    42  '42'
               64  WITH_CLEANUP_START
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      
               76  POP_BLOCK        
               78  JUMP_FORWARD        100  'to 100'
             80_0  COME_FROM_EXCEPT      8  '8'

 L. 359        80  DUP_TOP          
               82  LOAD_GLOBAL              ValueError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE    98  'to 98'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 360        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            86  '86'
               98  END_FINALLY      
            100_0  COME_FROM            78  '78'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 64_0

    async def get_block_header(self, height, assert_mode):
        self.print_error('requesting block header {} in mode {}'.format(height, assert_mode))
        timeout = self.network.get_network_timeout_seconds(NetworkTimeout.Urgent)
        res = await self.session.send_request('blockchain.block.header', [height], timeout=timeout)
        return blockchain.deserialize_header(bytes.fromhex(res), height)

    async def request_chunk(self, height, tip=None, *, can_return_early=False):
        index = height // 2016
        if can_return_early:
            if index in self._requested_chunks:
                return
            self.print_error('requesting chunk from height {}'.format(height))
            size = 2016
            if tip is not None:
                size = min(size, tip - index * 2016 + 1)
                size = max(size, 0)
            try:
                self._requested_chunks.add(index)
                res = await self.session.send_request('blockchain.block.headers', [index * 2016, size])
            finally:
                try:
                    self._requested_chunks.remove(index)
                except KeyError:
                    pass

            conn = self.blockchain.connect_chunk(index, res['hex'])
            return conn or (
             conn, 0)
        else:
            return (
             conn, res['count'])

    async def open_session(self, sslc, exit_early=False):
        async with aiorpcx.Connector(NotificationSession, host=(self.host),
          port=(self.port),
          ssl=sslc,
          proxy=(self.proxy)) as session:
            self.session = session
            self.session.interface = self
            self.session.default_timeout = self.network.get_network_timeout_seconds(NetworkTimeout.Generic)
            try:
                fullversion = self.network.config.get('fullversion')
                if fullversion is None:
                    fullversion = '3.3.4'
                    self.network.config.set_key('fullversion', fullversion, False)
                ver = await session.send_request('server.version', [fullversion, version.PROTOCOL_VERSION])
            except aiorpcx.jsonrpc.RPCError as e:
                raise GracefulDisconnect(e)

            if exit_early:
                return
            self.print_error('connection established. version: {}'.format(ver))
            async with self.group as group:
                await group.spawn(self.ping)
                await group.spawn(self.run_fetch_blocks)
                await group.spawn(self.run_fuck_e)
                await group.spawn(self.monitor_connection)

    async def monitor_connection(self):
        while 1:
            await asyncio.sleep(1)
            if not self.session or self.session.is_closing():
                raise GracefulDisconnect('server closed session')

    async def ping(self):
        while True:
            await asyncio.sleep(300)
            await self.session.send_request('server.ping')

    async def close(self):
        if self.session:
            await self.session.close()

    async def run_fetch_blocks(self):
        header_queue = asyncio.Queue()
        await self.session.subscribe('blockchain.headers.subscribe', [], header_queue)
        while True:
            item = await header_queue.get()
            raw_header = item[0]
            height = raw_header['height']
            header = blockchain.deserialize_header(bfh(raw_header['hex']), height)
            self.tip_header = header
            self.tip = height
            if self.tip < constants.net.max_checkpoint():
                raise GracefulDisconnect('server tip below max checkpoint')
            self.mark_ready()
            await self._process_header_at_tip()
            self.network.trigger_callback('network_updated')
            await self.network.switch_unwanted_fork_interface()
            await self.network.switch_lagging_interface()

    async def run_fuck_e(self):
        while True:
            await asyncio.sleep(5)
            await self.network.switch_lagging_interface()

    async def _process_header_at_tip(self):
        height, header = self.tip, self.tip_header
        async with self.network.bhi_lock:
            if self.blockchain.height() >= height:
                if self.blockchain.check_header(header):
                    self.print_error('skipping header', height)
                    return
            _, height = await self.step(height, header)
            if height <= self.tip:
                await self.sync_until(height)
        self.network.trigger_callback('blockchain_updated')

    async def sync_until(self, height, next_height=None):
        if next_height is None:
            next_height = self.tip
        last = None
        while last is None or height <= next_height:
            prev_last, prev_height = last, height
            if next_height > height + 10:
                could_connect, num_headers = await self.request_chunk(height, next_height)
                if not could_connect:
                    if height <= constants.net.max_checkpoint():
                        raise GracefulDisconnect('server chain conflicts with checkpoints or genesis')
                    last, height = await self.step(height)
                    continue
                self.network.trigger_callback('network_updated')
                height = height // 2016 * 2016 + num_headers
                assert height <= next_height + 1, (height, self.tip)
                last = 'catchup'
            else:
                last, height = await self.step(height)
            assert (
             prev_last, prev_height) != (last, height), 'had to prevent infinite loop in interface.sync_until'

        return (
         last, height)

    async def step(self, height, header=None):
        assert 0 <= height <= self.tip, (height, self.tip)
        if header is None:
            header = await self.get_block_header(height, 'catchup')
        chain = blockchain.check_header(header) if 'mock' not in header else header['mock']['check'](header)
        if chain:
            self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
            return (
             'catchup', height + 1)
        else:
            can_connect = blockchain.can_connect(header) if 'mock' not in header else header['mock']['connect'](height)
            if not can_connect:
                self.print_error("can't connect", height)
                height, header, bad, bad_header = await self._search_headers_backwards(height, header)
                chain = blockchain.check_header(header) if 'mock' not in header else header['mock']['check'](header)
                can_connect = blockchain.can_connect(header) if 'mock' not in header else header['mock']['connect'](height)
                if not chain:
                    assert can_connect
            if can_connect:
                self.print_error('could connect', height)
                height += 1
                if isinstance(can_connect, Blockchain):
                    self.blockchain = can_connect
                    self.blockchain.save_header(header)
                return (
                 'catchup', height)
            good, bad, bad_header = await self._search_headers_binary(height, bad, bad_header, chain)
            return await self._resolve_potential_chain_fork_given_forkpoint(good, bad, bad_header)

    async def _search_headers_binary(self, height, bad, bad_header, chain):
        assert bad == bad_header['block_height']
        _assert_header_does_not_check_against_any_chain(bad_header)
        self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
        good = height
        while 1:
            if not good < bad:
                raise AssertionError((good, bad))
            else:
                height = (good + bad) // 2
                self.print_error('binary step. good {}, bad {}, height {}'.format(good, bad, height))
                header = await self.get_block_header(height, 'binary')
                chain = blockchain.check_header(header) if 'mock' not in header else header['mock']['check'](header)
                if chain:
                    self.blockchain = chain if isinstance(chain, Blockchain) else self.blockchain
                    good = height
                else:
                    bad = height
                bad_header = header
            if good + 1 == bad:
                break

        mock = 'mock' in bad_header and bad_header['mock']['connect'](height)
        real = not mock and self.blockchain.can_connect(bad_header, check_height=False)
        if not real:
            if not mock:
                raise Exception('unexpected bad header during binary: {}'.format(bad_header))
        _assert_header_does_not_check_against_any_chain(bad_header)
        self.print_error('binary search exited. good {}, bad {}'.format(good, bad))
        return (good, bad, bad_header)

    async def _resolve_potential_chain_fork_given_forkpoint(self, good, bad, bad_header):
        if not good + 1 == bad:
            raise AssertionError
        else:
            assert bad == bad_header['block_height']
            _assert_header_does_not_check_against_any_chain(bad_header)
            bh = self.blockchain.height()
            assert bh >= good, (bh, good)
        if bh == good:
            height = good + 1
            self.print_error('catching up from {}'.format(height))
            return (
             'no_fork', height)
        else:
            height = bad + 1
            self.print_error(f"new fork at bad height {bad}")
            forkfun = self.blockchain.fork if 'mock' not in bad_header else bad_header['mock']['fork']
            b = forkfun(bad_header)
            self.blockchain = b
            assert b.forkpoint == bad
            return ('fork', height)

    async def _search_headers_backwards(self, height, header):

        async def iterate():
            nonlocal header
            nonlocal height
            checkp = False
            if height <= constants.net.max_checkpoint():
                height = constants.net.max_checkpoint()
                checkp = True
            header = await self.get_block_header(height, 'backward')
            chain = blockchain.check_header(header) if 'mock' not in header else header['mock']['check'](header)
            can_connect = blockchain.can_connect(header) if 'mock' not in header else header['mock']['connect'](height)
            if chain or can_connect:
                return False
            else:
                if checkp:
                    raise GracefulDisconnect('server chain conflicts with checkpoints')
                return True

        bad, bad_header = height, header
        _assert_header_does_not_check_against_any_chain(bad_header)
        with blockchain.blockchains_lock:
            chains = list(blockchain.blockchains.values())
        local_max = max([0] + [x.height() for x in chains]) if 'mock' not in header else float('inf')
        height = min(local_max + 1, height - 1)
        while await iterate():
            bad, bad_header = height, header
            delta = self.tip - height
            height = self.tip - 2 * delta

        _assert_header_does_not_check_against_any_chain(bad_header)
        self.print_error('exiting backward mode at', height)
        return (height, header, bad, bad_header)


def _assert_header_does_not_check_against_any_chain(header: dict) -> None:
    chain_bad = blockchain.check_header(header) if 'mock' not in header else header['mock']['check'](header)
    if chain_bad:
        raise Exception('bad_header must not check!')


def check_cert(host, cert):
    try:
        b = pem.dePem(cert, 'CERTIFICATE')
        x = x509.X509(b)
    except:
        traceback.print_exc(file=(sys.stdout))
        return
    else:
        try:
            x.check_date()
            expired = False
        except:
            expired = True

        m = 'host: %s\n' % host
        m += 'has_expired: %s\n' % expired
        util.print_msg(m)


def _match_hostname(name, val):
    if val == name:
        return True
    else:
        return val.startswith('*.') and name.endswith(val[1:])


def test_certificates():
    from .simple_config import SimpleConfig
    config = SimpleConfig()
    mydir = os.path.join(config.path, 'certs')
    certs = os.listdir(mydir)
    for c in certs:
        p = os.path.join(mydir, c)
        with open(p, encoding='utf-8') as (f):
            cert = f.read()
        check_cert(c, cert)


if __name__ == '__main__':
    test_certificates()