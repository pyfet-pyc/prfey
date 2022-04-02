# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\connector.py
import asyncio, functools, random, sys, traceback, warnings
from collections import defaultdict, deque
from contextlib import suppress
from http.cookies import SimpleCookie
from itertools import cycle, islice
from time import monotonic
from types import TracebackType
from typing import TYPE_CHECKING, Any, Awaitable, Callable, DefaultDict, Dict, Iterator, List, Optional, Set, Tuple, Type, Union, cast
import attr
from . import hdrs, helpers
from .abc import AbstractResolver
from .client_exceptions import ClientConnectionError, ClientConnectorCertificateError, ClientConnectorError, ClientConnectorSSLError, ClientHttpProxyError, ClientProxyConnectionError, ServerFingerprintMismatch, cert_errors, ssl_errors
from .client_proto import ResponseHandler
from .client_reqrep import ClientRequest, Fingerprint, _merge_ssl_params
from .helpers import PY_36, CeilTimeout, get_running_loop, is_ip_address, noop2, sentinel
from .http import RESPONSES
from .locks import EventResultOrError
from .resolver import DefaultResolver
try:
    import ssl
    SSLContext = ssl.SSLContext
except ImportError:
    ssl = None
    SSLContext = object
else:
    __all__ = ('BaseConnector', 'TCPConnector', 'UnixConnector', 'NamedPipeConnector')
    if TYPE_CHECKING:
        from .client import ClientTimeout
        from .client_reqrep import ConnectionKey
        from .tracing import Trace

    class _DeprecationWaiter:
        __slots__ = ('_awaitable', '_awaited')

        def __init__(self, awaitable: Awaitable[Any]) -> None:
            self._awaitable = awaitable
            self._awaited = False

        def __await__(self) -> Any:
            self._awaited = True
            return self._awaitable.__await__()

        def __del__(self) -> None:
            if not self._awaited:
                warnings.warn('Connector.close() is a coroutine, please use await connector.close()', DeprecationWarning)


    class Connection:
        _source_traceback = None
        _transport = None

        def __init__(self, connector: 'BaseConnector', key: 'ConnectionKey', protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
            self._key = key
            self._connector = connector
            self._loop = loop
            self._protocol = protocol
            self._callbacks = []
            if loop.get_debug():
                self._source_traceback = traceback.extract_stack(sys._getframe(1))

        def __repr__(self) -> str:
            return 'Connection<{}>'.format(self._key)

        def __del__(self, _warnings: Any=warnings) -> None:
            if self._protocol is not None:
                if PY_36:
                    kwargs = {'source': self}
                else:
                    kwargs = {}
                (_warnings.warn)(('Unclosed connection {!r}'.format(self)), 
                 ResourceWarning, **kwargs)
                if self._loop.is_closed():
                    return
                self._connector._release((self._key),
                  (self._protocol), should_close=True)
                context = {'client_connection':self, 
                 'message':'Unclosed connection'}
                if self._source_traceback is not None:
                    context['source_traceback'] = self._source_traceback
                self._loop.call_exception_handler(context)

        @property
        def loop(self) -> asyncio.AbstractEventLoop:
            warnings.warn('connector.loop property is deprecated', DeprecationWarning,
              stacklevel=2)
            return self._loop

        @property
        def transport(self) -> Optional[asyncio.Transport]:
            if self._protocol is None:
                return
            return self._protocol.transport

        @property
        def protocol(self) -> Optional[ResponseHandler]:
            return self._protocol

        def add_callback(self, callback: Callable[([], None)]) -> None:
            if callback is not None:
                self._callbacks.append(callback)

        def _notify_release(self) -> None:
            callbacks, self._callbacks = self._callbacks[:], []
            for cb in callbacks:
                with suppress(Exception):
                    cb()

        def close(self) -> None:
            self._notify_release()
            if self._protocol is not None:
                self._connector._release((self._key),
                  (self._protocol), should_close=True)
                self._protocol = None

        def release(self) -> None:
            self._notify_release()
            if self._protocol is not None:
                self._connector._release((self._key),
                  (self._protocol), should_close=(self._protocol.should_close))
                self._protocol = None

        @property
        def closed(self) -> bool:
            return self._protocol is None or not self._protocol.is_connected()


    class _TransportPlaceholder:
        __doc__ = ' placeholder for BaseConnector.connect function '

        def close(self) -> None:
            pass


    class BaseConnector:
        __doc__ = 'Base connector class.\n\n    keepalive_timeout - (optional) Keep-alive timeout.\n    force_close - Set to True to force close and do reconnect\n        after each request (and between redirects).\n    limit - The total number of simultaneous connections.\n    limit_per_host - Number of simultaneous connections to one host.\n    enable_cleanup_closed - Enables clean-up closed ssl transports.\n                            Disabled by default.\n    loop - Optional event loop.\n    '
        _closed = True
        _source_traceback = None
        _cleanup_closed_period = 2.0

        def __init__(self, *, keepalive_timeout: Union[(object, None, float)]=sentinel, force_close: bool=False, limit: int=100, limit_per_host: int=0, enable_cleanup_closed: bool=False, loop: Optional[asyncio.AbstractEventLoop]=None) -> None:
            if force_close:
                if not keepalive_timeout is not None or keepalive_timeout is not sentinel:
                    raise ValueError('keepalive_timeout cannot be set if force_close is True')
            elif keepalive_timeout is sentinel:
                keepalive_timeout = 15.0
            loop = get_running_loop(loop)
            self._closed = False
            if loop.get_debug():
                self._source_traceback = traceback.extract_stack(sys._getframe(1))
            self._conns = {}
            self._limit = limit
            self._limit_per_host = limit_per_host
            self._acquired = set()
            self._acquired_per_host = defaultdict(set)
            self._keepalive_timeout = cast(float, keepalive_timeout)
            self._force_close = force_close
            self._waiters = defaultdict(deque)
            self._loop = loop
            self._factory = functools.partial(ResponseHandler, loop=loop)
            self.cookies = SimpleCookie()
            self._cleanup_handle = None
            self._cleanup_closed_handle = None
            self._cleanup_closed_disabled = not enable_cleanup_closed
            self._cleanup_closed_transports = []
            self._cleanup_closed()

        def __del__(self, _warnings: Any=warnings) -> None:
            if self._closed:
                return
            if not self._conns:
                return
            conns = [repr(c) for c in self._conns.values()]
            self._close()
            if PY_36:
                kwargs = {'source': self}
            else:
                kwargs = {}
            (_warnings.warn)(('Unclosed connector {!r}'.format(self)), 
             ResourceWarning, **kwargs)
            context = {'connector':self,  'connections':conns, 
             'message':'Unclosed connector'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)

        def __enter__(self) -> 'BaseConnector':
            warnings.warn('"witn Connector():" is deprecated, use "async with Connector():" instead', DeprecationWarning)
            return self

        def __exit__(self, *exc: Any) -> None:
            self.close()

        async def __aenter__(self) -> 'BaseConnector':
            return self

        async def __aexit__(self, exc_type: Optional[Type[BaseException]]=None, exc_value: Optional[BaseException]=None, exc_traceback: Optional[TracebackType]=None) -> None:
            await self.close()

        @property
        def force_close(self) -> bool:
            """Ultimately close connection on releasing if True."""
            return self._force_close

        @property
        def limit(self) -> int:
            """The total number for simultaneous connections.

        If limit is 0 the connector has no limit.
        The default limit size is 100.
        """
            return self._limit

        @property
        def limit_per_host(self) -> int:
            """The limit_per_host for simultaneous connections
        to the same endpoint.

        Endpoints are the same if they are have equal
        (host, port, is_ssl) triple.

        """
            return self._limit_per_host

        def _cleanup(self) -> None:
            """Cleanup unused transports."""
            if self._cleanup_handle:
                self._cleanup_handle.cancel()
            now = self._loop.time()
            timeout = self._keepalive_timeout
            if self._conns:
                connections = {}
                deadline = now - timeout
                for key, conns in self._conns.items():
                    alive = []
                    for proto, use_time in conns:
                        if proto.is_connected():
                            if use_time - deadline < 0:
                                transport = proto.transport
                                proto.close()
                                if key.is_ssl:
                                    self._cleanup_closed_disabled or self._cleanup_closed_transports.append(transport)
                            else:
                                alive.append((proto, use_time))

                    if alive:
                        connections[key] = alive
                    self._conns = connections

                if self._conns:
                    self._cleanup_handle = helpers.weakref_handle(self, '_cleanup', timeout, self._loop)

        def _drop_acquired_per_host(self, key: 'ConnectionKey', val: ResponseHandler) -> None:
            acquired_per_host = self._acquired_per_host
            if key not in acquired_per_host:
                return
            conns = acquired_per_host[key]
            conns.remove(val)
            if not conns:
                del self._acquired_per_host[key]

        def _cleanup_closed(self) -> None:
            """Double confirmation for transport close.
        Some broken ssl servers may leave socket open without proper close.
        """
            if self._cleanup_closed_handle:
                self._cleanup_closed_handle.cancel()
            for transport in self._cleanup_closed_transports:
                if transport is not None:
                    transport.abort()
            else:
                self._cleanup_closed_transports = []
                if not self._cleanup_closed_disabled:
                    self._cleanup_closed_handle = helpers.weakref_handle(self, '_cleanup_closed', self._cleanup_closed_period, self._loop)

        def close(self) -> Awaitable[None]:
            """Close all opened transports."""
            self._close()
            return _DeprecationWaiter(noop2())

        def _close--- This code section failed: ---

 L. 396         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closed
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 397         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 399        10  LOAD_CONST               True
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _closed

 L. 401        16  SETUP_FINALLY       158  'to 158'

 L. 402        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  LOAD_METHOD              is_closed
               24  CALL_METHOD_0         0  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 403        28  POP_BLOCK        
               30  CALL_FINALLY        158  'to 158'
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 406        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _cleanup_handle
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 407        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _cleanup_handle
               46  LOAD_METHOD              cancel
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            40  '40'

 L. 410        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _cleanup_closed_handle
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 411        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _cleanup_closed_handle
               62  LOAD_METHOD              cancel
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            56  '56'

 L. 413        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _conns
               72  LOAD_METHOD              values
               74  CALL_METHOD_0         0  ''
               76  GET_ITER         
             78_0  COME_FROM           104  '104'
               78  FOR_ITER            106  'to 106'
               80  STORE_FAST               'data'

 L. 414        82  LOAD_FAST                'data'
               84  GET_ITER         
             86_0  COME_FROM           102  '102'
               86  FOR_ITER            104  'to 104'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'proto'
               92  STORE_FAST               't0'

 L. 415        94  LOAD_FAST                'proto'
               96  LOAD_METHOD              close
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
              102  JUMP_BACK            86  'to 86'
            104_0  COME_FROM            86  '86'
              104  JUMP_BACK            78  'to 78'
            106_0  COME_FROM            78  '78'

 L. 417       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _acquired
              110  GET_ITER         
            112_0  COME_FROM           124  '124'
              112  FOR_ITER            126  'to 126'
              114  STORE_FAST               'proto'

 L. 418       116  LOAD_FAST                'proto'
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          
              124  JUMP_BACK           112  'to 112'
            126_0  COME_FROM           112  '112'

 L. 420       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _cleanup_closed_transports
              130  GET_ITER         
            132_0  COME_FROM           152  '152'
            132_1  COME_FROM           142  '142'
              132  FOR_ITER            154  'to 154'
              134  STORE_FAST               'transport'

 L. 421       136  LOAD_FAST                'transport'
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE_BACK   132  'to 132'

 L. 422       144  LOAD_FAST                'transport'
              146  LOAD_METHOD              abort
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          
              152  JUMP_BACK           132  'to 132'
            154_0  COME_FROM           132  '132'
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM            30  '30'
            158_1  COME_FROM_FINALLY    16  '16'

 L. 425       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _conns
              162  LOAD_METHOD              clear
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          

 L. 426       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _acquired
              172  LOAD_METHOD              clear
              174  CALL_METHOD_0         0  ''
              176  POP_TOP          

 L. 427       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _waiters
              182  LOAD_METHOD              clear
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          

 L. 428       188  LOAD_CONST               None
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _cleanup_handle

 L. 429       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _cleanup_closed_transports
              198  LOAD_METHOD              clear
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

 L. 430       204  LOAD_CONST               None
              206  LOAD_FAST                'self'
              208  STORE_ATTR               _cleanup_closed_handle
              210  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 30

        @property
        def closed(self) -> bool:
            """Is connector closed.

        A readonly property.
        """
            return self._closed

        def _available_connections(self, key: 'ConnectionKey') -> int:
            """
        Return number of available connections taking into account
        the limit, limit_per_host and the connection key.

        If it returns less than 1 means that there is no connections
        availables.
        """
            if self._limit:
                available = self._limit - len(self._acquired)
                if self._limit_per_host:
                    if not available > 0 or key in self._acquired_per_host:
                        acquired = self._acquired_per_host.get(key)
                        assert acquired is not None
                        available = self._limit_per_host - len(acquired)
            elif self._limit_per_host and key in self._acquired_per_host:
                acquired = self._acquired_per_host.get(key)
                assert acquired is not None
                available = self._limit_per_host - len(acquired)
            else:
                available = 1
            return available

        async def connect(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> Connection:
            """Get from pool or create new connection."""
            key = req.connection_key
            available = self._available_connections(key)
            if available <= 0:
                fut = self._loop.create_future()
                waiters = self._waiters[key]
                waiters.append(fut)
                if traces:
                    for trace in traces:
                        await trace.send_connection_queued_start()
                    else:
                        try:
                            try:
                                await fut
                            except BaseException as e:
                                try:
                                    try:
                                        waiters.remove(fut)
                                    except ValueError:
                                        pass
                                    else:
                                        raise e
                                finally:
                                    e = None
                                    del e

                        finally:
                            if not waiters:
                                try:
                                    del self._waiters[key]
                                except KeyError:
                                    pass

                        if traces:
                            for trace in traces:
                                await trace.send_connection_queued_end()

            proto = self._get(key)
            if proto is None:
                placeholder = cast(ResponseHandler, _TransportPlaceholder())
                self._acquired.add(placeholder)
                self._acquired_per_host[key].add(placeholder)
                if traces:
                    for trace in traces:
                        await trace.send_connection_create_start()
                    else:
                        try:
                            proto = await self._create_connection(req, traces, timeout)
                            if self._closed:
                                proto.close()
                                raise ClientConnectionError('Connector is closed.')
                        except BaseException:
                            if not self._closed:
                                self._acquired.remove(placeholder)
                                self._drop_acquired_per_host(key, placeholder)
                                self._release_waiter()
                            else:
                                raise
                        else:
                            if not self._closed:
                                self._acquired.remove(placeholder)
                                self._drop_acquired_per_host(key, placeholder)
                            if traces:
                                for trace in traces:
                                    await trace.send_connection_create_end()

                        if traces:
                            for trace in traces:
                                await trace.send_connection_reuseconn()

                self._acquired.add(proto)
                self._acquired_per_host[key].add(proto)
                return Connection(self, key, proto, self._loop)

        def _get(self, key: 'ConnectionKey') -> Optional[ResponseHandler]:
            try:
                conns = self._conns[key]
            except KeyError:
                return
            else:
                t1 = self._loop.time()
                while conns:
                    proto, t0 = conns.pop()
                    if proto.is_connected():
                        if t1 - t0 > self._keepalive_timeout:
                            transport = proto.transport
                            proto.close()
                            if key.is_ssl:
                                self._cleanup_closed_disabled or self._cleanup_closed_transports.append(transport)
                        else:
                            if not conns:
                                del self._conns[key]
                            return proto

                del self._conns[key]

        def _release_waiter(self) -> None:
            """
        Iterates over all waiters till found one that is not finsihed and
        belongs to a host that has available connections.
        """
            if not self._waiters:
                return
            queues = list(self._waiters.keys())
            random.shuffle(queues)
            for key in queues:
                if self._available_connections(key) < 1:
                    pass
                else:
                    waiters = self._waiters[key]
                    while True:
                        if waiters:
                            waiter = waiters.popleft()
                            if not waiter.done():
                                waiter.set_result(None)
                            return None

        def _release_acquired(self, key: 'ConnectionKey', proto: ResponseHandler) -> None:
            if self._closed:
                return
            try:
                self._acquired.remove(proto)
                self._drop_acquired_per_host(key, proto)
            except KeyError:
                pass
            else:
                self._release_waiter()

        def _release(self, key: 'ConnectionKey', protocol: ResponseHandler, *, should_close: bool=False) -> None:
            if self._closed:
                return
            self._release_acquired(key, protocol)
            if self._force_close:
                should_close = True
            if should_close or (protocol.should_close):
                transport = protocol.transport
                protocol.close()
                if key.is_ssl and not self._cleanup_closed_disabled:
                    self._cleanup_closed_transports.append(transport)
                else:
                    conns = self._conns.get(key)
                    if conns is None:
                        conns = self._conns[key] = []
                    conns.append((protocol, self._loop.time()))
                    if self._cleanup_handle is None:
                        self._cleanup_handle = helpers.weakref_handle(self, '_cleanup', self._keepalive_timeout, self._loop)

        async def _create_connection(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> ResponseHandler:
            raise NotImplementedError()


    class _DNSCacheTable:

        def __init__(self, ttl: Optional[float]=None) -> None:
            self._addrs_rr = {}
            self._timestamps = {}
            self._ttl = ttl

        def __contains__(self, host: object) -> bool:
            return host in self._addrs_rr

        def add(self, key: Tuple[(str, int)], addrs: List[Dict[(str, Any)]]) -> None:
            self._addrs_rr[key] = (cycle(addrs), len(addrs))
            if self._ttl:
                self._timestamps[key] = monotonic()

        def remove(self, key: Tuple[(str, int)]) -> None:
            self._addrs_rr.pop(key, None)
            if self._ttl:
                self._timestamps.pop(key, None)

        def clear(self) -> None:
            self._addrs_rr.clear()
            self._timestamps.clear()

        def next_addrs(self, key: Tuple[(str, int)]) -> List[Dict[(str, Any)]]:
            loop, length = self._addrs_rr[key]
            addrs = list(islice(loop, length))
            next(loop)
            return addrs

        def expired(self, key: Tuple[(str, int)]) -> bool:
            if self._ttl is None:
                return False
            return self._timestamps[key] + self._ttl < monotonic()


    class TCPConnector(BaseConnector):
        __doc__ = 'TCP connector.\n\n    verify_ssl - Set to True to check ssl certifications.\n    fingerprint - Pass the binary sha256\n        digest of the expected certificate in DER format to verify\n        that the certificate the server presents matches. See also\n        https://en.wikipedia.org/wiki/Transport_Layer_Security#Certificate_pinning\n    resolver - Enable DNS lookups and use this\n        resolver\n    use_dns_cache - Use memory cache for DNS lookups.\n    ttl_dns_cache - Max seconds having cached a DNS entry, None forever.\n    family - socket address family\n    local_addr - local tuple of (host, port) to bind socket to\n\n    keepalive_timeout - (optional) Keep-alive timeout.\n    force_close - Set to True to force close and do reconnect\n        after each request (and between redirects).\n    limit - The total number of simultaneous connections.\n    limit_per_host - Number of simultaneous connections to one host.\n    enable_cleanup_closed - Enables clean-up closed ssl transports.\n                            Disabled by default.\n    loop - Optional event loop.\n    '

        def __init__(self, *, verify_ssl=True, fingerprint=None, use_dns_cache=True, ttl_dns_cache=10, family=0, ssl_context=None, ssl=None, local_addr=None, resolver=None, keepalive_timeout=sentinel, force_close=False, limit=100, limit_per_host=0, enable_cleanup_closed=False, loop=None):
            super().__init__(keepalive_timeout=keepalive_timeout, force_close=force_close,
              limit=limit,
              limit_per_host=limit_per_host,
              enable_cleanup_closed=enable_cleanup_closed,
              loop=loop)
            self._ssl = _merge_ssl_params(ssl, verify_ssl, ssl_context, fingerprint)
            if resolver is None:
                resolver = DefaultResolver(loop=(self._loop))
            self._resolver = resolver
            self._use_dns_cache = use_dns_cache
            self._cached_hosts = _DNSCacheTable(ttl=ttl_dns_cache)
            self._throttle_dns_events = {}
            self._family = family
            self._local_addr = local_addr

        def close(self):
            """Close all ongoing DNS calls."""
            for ev in self._throttle_dns_events.values():
                ev.cancel()
            else:
                return super().close()

        @property
        def family(self) -> int:
            """Socket family like AF_INET."""
            return self._family

        @property
        def use_dns_cache(self) -> bool:
            """True if local DNS caching is enabled."""
            return self._use_dns_cache

        def clear_dns_cache(self, host: Optional[str]=None, port: Optional[int]=None) -> None:
            """Remove specified host/port or clear all dns local cache."""
            if host is not None and port is not None:
                self._cached_hosts.remove((host, port))
            elif host is not None or port is not None:
                raise ValueError('either both host and port or none of them are allowed')
            else:
                self._cached_hosts.clear()

        async def _resolve_host(self, host: str, port: int, traces: Optional[List['Trace']]=None) -> List[Dict[(str, Any)]]:
            if is_ip_address(host):
                return [
                 {'hostname':host,  'host':host,  'port':port,  'family':self._family, 
                  'proto':0,  'flags':0}]
            if not self._use_dns_cache:
                if traces:
                    for trace in traces:
                        await trace.send_dns_resolvehost_start(host)
                    else:
                        res = await self._resolver.resolve(host,
                          port, family=(self._family))
                        if traces:
                            for trace in traces:
                                await trace.send_dns_resolvehost_end(host)

                    return res
            key = (
             host, port)
            if key in self._cached_hosts:
                if not self._cached_hosts.expired(key):
                    result = self._cached_hosts.next_addrs(key)
                    if traces:
                        for trace in traces:
                            await trace.send_dns_cache_hit(host)

                        return result
                if key in self._throttle_dns_events:
                    event = self._throttle_dns_events[key]
                    if traces:
                        for trace in traces:
                            await trace.send_dns_cache_hit(host)

                    await event.wait()
                else:
                    self._throttle_dns_events[key] = EventResultOrError(self._loop)
                    if traces:
                        for trace in traces:
                            await trace.send_dns_cache_miss(host)

                    try:
                        try:
                            if traces:
                                for trace in traces:
                                    await trace.send_dns_resolvehost_start(host)
                                else:
                                    addrs = await self._resolver.resolve(host, port, family=(self._family))
                                    if traces:
                                        for trace in traces:
                                            await trace.send_dns_resolvehost_end(host)

                            self._cached_hosts.add(key, addrs)
                            self._throttle_dns_events[key].set()
                        except BaseException as e:
                            try:
                                self._throttle_dns_events[key].set(exc=e)
                                raise
                            finally:
                                e = None
                                del e

                    finally:
                        self._throttle_dns_events.pop(key)

                return self._cached_hosts.next_addrs(key)

        async def _create_connection(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> ResponseHandler:
            """Create connection.

        Has same keyword arguments as BaseEventLoop.create_connection.
        """
            if req.proxy:
                _, proto = await self._create_proxy_connection(req, traces, timeout)
            else:
                _, proto = await self._create_direct_connection(req, traces, timeout)
            return proto

        @staticmethod
        @functools.lru_cache(None)
        def _make_ssl_context(verified: bool) -> SSLContext:
            if verified:
                return ssl.create_default_context()
            sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslcontext.options |= ssl.OP_NO_SSLv2
            sslcontext.options |= ssl.OP_NO_SSLv3
            try:
                sslcontext.options |= ssl.OP_NO_COMPRESSION
            except AttributeError as attr_err:
                try:
                    warnings.warn('{!s}: The Python interpreter is compiled against OpenSSL < 1.0.0. Ref: https://docs.python.org/3/library/ssl.html#ssl.OP_NO_COMPRESSION'.format(attr_err))
                finally:
                    attr_err = None
                    del attr_err

            else:
                sslcontext.set_default_verify_paths()
                return sslcontext

        def _get_ssl_context(self, req: 'ClientRequest') -> Optional[SSLContext]:
            """Logic to get the correct SSL context

        0. if req.ssl is false, return None

        1. if ssl_context is specified in req, use it
        2. if _ssl_context is specified in self, use it
        3. otherwise:
            1. if verify_ssl is not specified in req, use self.ssl_context
               (will generate a default context according to self.verify_ssl)
            2. if verify_ssl is True in req, generate a default SSL context
            3. if verify_ssl is False in req, generate a SSL context that
               won't verify
        """
            if req.is_ssl():
                if ssl is None:
                    raise RuntimeError('SSL is not supported.')
                sslcontext = req.ssl
                if isinstance(sslcontext, ssl.SSLContext):
                    return sslcontext
                if sslcontext is not None:
                    return self._make_ssl_context(False)
                sslcontext = self._ssl
                if isinstance(sslcontext, ssl.SSLContext):
                    return sslcontext
                if sslcontext is not None:
                    return self._make_ssl_context(False)
                return self._make_ssl_context(True)
            return

        def _get_fingerprint(self, req: 'ClientRequest') -> Optional['Fingerprint']:
            ret = req.ssl
            if isinstance(ret, Fingerprint):
                return ret
            ret = self._ssl
            if isinstance(ret, Fingerprint):
                return ret

        async def _wrap_create_connection--- This code section failed: ---

 L. 934         0  SETUP_FINALLY        58  'to 58'

 L. 935         2  LOAD_GLOBAL              CeilTimeout
                4  LOAD_FAST                'timeout'
                6  LOAD_ATTR                sock_connect
                8  CALL_FUNCTION_1       1  ''
               10  SETUP_WITH           48  'to 48'
               12  POP_TOP          

 L. 936        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _loop
               18  LOAD_ATTR                create_connection
               20  LOAD_FAST                'args'
               22  LOAD_FAST                'kwargs'
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH       10  '10'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      
               54  POP_BLOCK        
               56  JUMP_FORWARD        198  'to 198'
             58_0  COME_FROM_FINALLY     0  '0'

 L. 937        58  DUP_TOP          
               60  LOAD_GLOBAL              cert_errors
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   104  'to 104'
               66  POP_TOP          
               68  STORE_FAST               'exc'
               70  POP_TOP          
               72  SETUP_FINALLY        92  'to 92'

 L. 938        74  LOAD_GLOBAL              ClientConnectorCertificateError

 L. 939        76  LOAD_FAST                'req'
               78  LOAD_ATTR                connection_key

 L. 939        80  LOAD_FAST                'exc'

 L. 938        82  CALL_FUNCTION_2       2  ''

 L. 939        84  LOAD_FAST                'exc'

 L. 938        86  RAISE_VARARGS_2       2  'exception instance with __cause__'
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_FINALLY    72  '72'
               92  LOAD_CONST               None
               94  STORE_FAST               'exc'
               96  DELETE_FAST              'exc'
               98  END_FINALLY      
              100  POP_EXCEPT       
              102  JUMP_FORWARD        198  'to 198'
            104_0  COME_FROM            64  '64'

 L. 940       104  DUP_TOP          
              106  LOAD_GLOBAL              ssl_errors
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   150  'to 150'
              112  POP_TOP          
              114  STORE_FAST               'exc'
              116  POP_TOP          
              118  SETUP_FINALLY       138  'to 138'

 L. 941       120  LOAD_GLOBAL              ClientConnectorSSLError
              122  LOAD_FAST                'req'
              124  LOAD_ATTR                connection_key
              126  LOAD_FAST                'exc'
              128  CALL_FUNCTION_2       2  ''
              130  LOAD_FAST                'exc'
              132  RAISE_VARARGS_2       2  'exception instance with __cause__'
              134  POP_BLOCK        
              136  BEGIN_FINALLY    
            138_0  COME_FROM_FINALLY   118  '118'
              138  LOAD_CONST               None
              140  STORE_FAST               'exc'
              142  DELETE_FAST              'exc'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_FORWARD        198  'to 198'
            150_0  COME_FROM           110  '110'

 L. 942       150  DUP_TOP          
              152  LOAD_GLOBAL              OSError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   196  'to 196'
              158  POP_TOP          
              160  STORE_FAST               'exc'
              162  POP_TOP          
              164  SETUP_FINALLY       184  'to 184'

 L. 943       166  LOAD_FAST                'client_error'
              168  LOAD_FAST                'req'
              170  LOAD_ATTR                connection_key
              172  LOAD_FAST                'exc'
              174  CALL_FUNCTION_2       2  ''
              176  LOAD_FAST                'exc'
              178  RAISE_VARARGS_2       2  'exception instance with __cause__'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM_FINALLY   164  '164'
              184  LOAD_CONST               None
              186  STORE_FAST               'exc'
              188  DELETE_FAST              'exc'
              190  END_FINALLY      
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           156  '156'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           148  '148'
            198_2  COME_FROM           102  '102'
            198_3  COME_FROM            56  '56'

Parse error at or near `POP_BLOCK' instruction at offset 44

        async def _create_direct_connection--- This code section failed: ---

 L. 953         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_ssl_context
                4  LOAD_FAST                'req'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'sslcontext'

 L. 954        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _get_fingerprint
               14  LOAD_FAST                'req'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'fingerprint'

 L. 956        20  SETUP_FINALLY        98  'to 98'

 L. 960        22  LOAD_FAST                'req'
               24  LOAD_ATTR                url
               26  LOAD_ATTR                raw_host
               28  STORE_FAST               'host'

 L. 961        30  LOAD_FAST                'host'
               32  LOAD_CONST               None
               34  COMPARE_OP               is-not
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  LOAD_ASSERT              AssertionError
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L. 962        42  LOAD_FAST                'req'
               44  LOAD_ATTR                port
               46  STORE_FAST               'port'

 L. 963        48  LOAD_FAST                'port'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_TRUE     60  'to 60'
               56  LOAD_ASSERT              AssertionError
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            54  '54'

 L. 964        60  LOAD_GLOBAL              asyncio
               62  LOAD_ATTR                shield
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _resolve_host

 L. 965        68  LOAD_FAST                'host'

 L. 966        70  LOAD_FAST                'port'

 L. 967        72  LOAD_FAST                'traces'

 L. 964        74  LOAD_CONST               ('traces',)
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 967        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _loop

 L. 964        82  LOAD_CONST               ('loop',)
               84  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  STORE_FAST               'hosts'
               94  POP_BLOCK        
               96  JUMP_FORWARD        146  'to 146'
             98_0  COME_FROM_FINALLY    20  '20'

 L. 968        98  DUP_TOP          
              100  LOAD_GLOBAL              OSError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   144  'to 144'
              106  POP_TOP          
              108  STORE_FAST               'exc'
              110  POP_TOP          
              112  SETUP_FINALLY       132  'to 132'

 L. 971       114  LOAD_GLOBAL              ClientConnectorError
              116  LOAD_FAST                'req'
              118  LOAD_ATTR                connection_key
              120  LOAD_FAST                'exc'
              122  CALL_FUNCTION_2       2  ''
              124  LOAD_FAST                'exc'
              126  RAISE_VARARGS_2       2  'exception instance with __cause__'
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_FINALLY   112  '112'
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  END_FINALLY      
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           104  '104'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM            96  '96'

 L. 973       146  LOAD_CONST               None
              148  STORE_FAST               'last_exc'

 L. 975       150  LOAD_FAST                'hosts'
              152  GET_ITER         
            154_0  COME_FROM           390  '390'
            154_1  COME_FROM           282  '282'
          154_156  FOR_ITER            422  'to 422'
              158  STORE_FAST               'hinfo'

 L. 976       160  LOAD_FAST                'hinfo'
              162  LOAD_STR                 'host'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'host'

 L. 977       168  LOAD_FAST                'hinfo'
              170  LOAD_STR                 'port'
              172  BINARY_SUBSCR    
              174  STORE_FAST               'port'

 L. 979       176  SETUP_FINALLY       254  'to 254'

 L. 980       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _wrap_create_connection

 L. 981       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _factory

 L. 981       186  LOAD_FAST                'host'

 L. 981       188  LOAD_FAST                'port'

 L. 981       190  LOAD_FAST                'timeout'

 L. 982       192  LOAD_FAST                'sslcontext'

 L. 982       194  LOAD_FAST                'hinfo'
              196  LOAD_STR                 'family'
              198  BINARY_SUBSCR    

 L. 983       200  LOAD_FAST                'hinfo'
              202  LOAD_STR                 'proto'
              204  BINARY_SUBSCR    

 L. 983       206  LOAD_FAST                'hinfo'
              208  LOAD_STR                 'flags'
              210  BINARY_SUBSCR    

 L. 984       212  LOAD_FAST                'sslcontext'
              214  POP_JUMP_IF_FALSE   224  'to 224'
              216  LOAD_FAST                'hinfo'
              218  LOAD_STR                 'hostname'
              220  BINARY_SUBSCR    
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           214  '214'
              224  LOAD_CONST               None
            226_0  COME_FROM           222  '222'

 L. 985       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _local_addr

 L. 986       230  LOAD_FAST                'req'

 L. 986       232  LOAD_FAST                'client_error'

 L. 980       234  LOAD_CONST               ('timeout', 'ssl', 'family', 'proto', 'flags', 'server_hostname', 'local_addr', 'req', 'client_error')
              236  CALL_FUNCTION_KW_12    12  '12 total positional and keyword args'
              238  GET_AWAITABLE    
              240  LOAD_CONST               None
              242  YIELD_FROM       
              244  UNPACK_SEQUENCE_2     2 
              246  STORE_FAST               'transp'
              248  STORE_FAST               'proto'
              250  POP_BLOCK        
              252  JUMP_FORWARD        302  'to 302'
            254_0  COME_FROM_FINALLY   176  '176'

 L. 987       254  DUP_TOP          
              256  LOAD_GLOBAL              ClientConnectorError
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   300  'to 300'
              264  POP_TOP          
              266  STORE_FAST               'exc'
              268  POP_TOP          
              270  SETUP_FINALLY       288  'to 288'

 L. 988       272  LOAD_FAST                'exc'
              274  STORE_FAST               'last_exc'

 L. 989       276  POP_BLOCK        
              278  POP_EXCEPT       
              280  CALL_FINALLY        288  'to 288'
              282  JUMP_BACK           154  'to 154'
              284  POP_BLOCK        
              286  BEGIN_FINALLY    
            288_0  COME_FROM           280  '280'
            288_1  COME_FROM_FINALLY   270  '270'
              288  LOAD_CONST               None
              290  STORE_FAST               'exc'
              292  DELETE_FAST              'exc'
              294  END_FINALLY      
              296  POP_EXCEPT       
              298  JUMP_FORWARD        302  'to 302'
            300_0  COME_FROM           260  '260'
              300  END_FINALLY      
            302_0  COME_FROM           298  '298'
            302_1  COME_FROM           252  '252'

 L. 991       302  LOAD_FAST                'req'
              304  LOAD_METHOD              is_ssl
              306  CALL_METHOD_0         0  ''
          308_310  POP_JUMP_IF_FALSE   410  'to 410'
              312  LOAD_FAST                'fingerprint'
          314_316  POP_JUMP_IF_FALSE   410  'to 410'

 L. 992       318  SETUP_FINALLY       334  'to 334'

 L. 993       320  LOAD_FAST                'fingerprint'
              322  LOAD_METHOD              check
              324  LOAD_FAST                'transp'
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
              330  POP_BLOCK        
              332  JUMP_FORWARD        410  'to 410'
            334_0  COME_FROM_FINALLY   318  '318'

 L. 994       334  DUP_TOP          
              336  LOAD_GLOBAL              ServerFingerprintMismatch
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   408  'to 408'
              344  POP_TOP          
              346  STORE_FAST               'exc'
              348  POP_TOP          
              350  SETUP_FINALLY       396  'to 396'

 L. 995       352  LOAD_FAST                'transp'
              354  LOAD_METHOD              close
              356  CALL_METHOD_0         0  ''
              358  POP_TOP          

 L. 996       360  LOAD_FAST                'self'
              362  LOAD_ATTR                _cleanup_closed_disabled
          364_366  POP_JUMP_IF_TRUE    380  'to 380'

 L. 997       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _cleanup_closed_transports
              372  LOAD_METHOD              append
              374  LOAD_FAST                'transp'
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          
            380_0  COME_FROM           364  '364'

 L. 998       380  LOAD_FAST                'exc'
              382  STORE_FAST               'last_exc'

 L. 999       384  POP_BLOCK        
              386  POP_EXCEPT       
              388  CALL_FINALLY        396  'to 396'
              390  JUMP_BACK           154  'to 154'
              392  POP_BLOCK        
              394  BEGIN_FINALLY    
            396_0  COME_FROM           388  '388'
            396_1  COME_FROM_FINALLY   350  '350'
              396  LOAD_CONST               None
              398  STORE_FAST               'exc'
              400  DELETE_FAST              'exc'
              402  END_FINALLY      
              404  POP_EXCEPT       
              406  JUMP_FORWARD        410  'to 410'
            408_0  COME_FROM           340  '340'
              408  END_FINALLY      
            410_0  COME_FROM           406  '406'
            410_1  COME_FROM           332  '332'
            410_2  COME_FROM           314  '314'
            410_3  COME_FROM           308  '308'

 L.1001       410  LOAD_FAST                'transp'
              412  LOAD_FAST                'proto'
              414  BUILD_TUPLE_2         2 
              416  ROT_TWO          
              418  POP_TOP          
              420  RETURN_VALUE     
            422_0  COME_FROM           154  '154'

 L.1003       422  LOAD_FAST                'last_exc'
              424  LOAD_CONST               None
              426  COMPARE_OP               is-not
          428_430  POP_JUMP_IF_TRUE    436  'to 436'
              432  LOAD_ASSERT              AssertionError
              434  RAISE_VARARGS_1       1  'exception instance'
            436_0  COME_FROM           428  '428'

 L.1004       436  LOAD_FAST                'last_exc'
              438  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FINALLY' instruction at offset 280

        async def _create_proxy_connection(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> Tuple[(asyncio.Transport, ResponseHandler)]:
            headers = {}
            if req.proxy_headers is not None:
                headers = req.proxy_headers
            headers[hdrs.HOST] = req.headers[hdrs.HOST]
            url = req.proxy
            assert url is not None
            proxy_req = ClientRequest((hdrs.METH_GET),
              url, headers=headers,
              auth=(req.proxy_auth),
              loop=(self._loop),
              ssl=(req.ssl))
            transport, proto = await self._create_direct_connection(proxy_req,
              [], timeout, client_error=ClientProxyConnectionError)
            proto.force_close()
            auth = proxy_req.headers.pop(hdrs.AUTHORIZATION, None)
            if auth is not None:
                if not req.is_ssl():
                    req.headers[hdrs.PROXY_AUTHORIZATION] = auth
                else:
                    proxy_req.headers[hdrs.PROXY_AUTHORIZATION] = auth
            if req.is_ssl():
                sslcontext = self._get_ssl_context(req)
                proxy_req.method = hdrs.METH_CONNECT
                proxy_req.url = req.url
                key = attr.evolve((req.connection_key), proxy=None,
                  proxy_auth=None,
                  proxy_headers_hash=None)
                conn = Connection(self, key, proto, self._loop)
                proxy_resp = await proxy_req.send(conn)
                try:
                    try:
                        protocol = conn._protocol
                        assert protocol is not None
                        protocol.set_response_params()
                        resp = await proxy_resp.start(conn)
                    except BaseException:
                        proxy_resp.close()
                        conn.close()
                        raise
                    else:
                        conn._protocol = None
                        conn._transport = None
                        try:
                            if resp.status != 200:
                                message = resp.reason
                                if message is None:
                                    message = RESPONSES[resp.status][0]
                                raise ClientHttpProxyError((proxy_resp.request_info),
                                  (resp.history),
                                  status=(resp.status),
                                  message=message,
                                  headers=(resp.headers))
                            rawsock = transport.get_extra_info('socket', default=None)
                            if rawsock is None:
                                raise RuntimeError('Transport does not expose socket instance')
                            rawsock = rawsock.dup()
                        finally:
                            transport.close()

                        transport, proto = await self._wrap_create_connection((self._factory),
                          timeout=timeout, ssl=sslcontext,
                          sock=rawsock,
                          server_hostname=(req.host),
                          req=req)
                finally:
                    proxy_resp.close()

            return (transport, proto)


    class UnixConnector(BaseConnector):
        __doc__ = 'Unix socket connector.\n\n    path - Unix socket path.\n    keepalive_timeout - (optional) Keep-alive timeout.\n    force_close - Set to True to force close and do reconnect\n        after each request (and between redirects).\n    limit - The total number of simultaneous connections.\n    limit_per_host - Number of simultaneous connections to one host.\n    loop - Optional event loop.\n    '

        def __init__(self, path, force_close=False, keepalive_timeout=sentinel, limit=100, limit_per_host=0, loop=None):
            super().__init__(force_close=force_close, keepalive_timeout=keepalive_timeout,
              limit=limit,
              limit_per_host=limit_per_host,
              loop=loop)
            self._path = path

        @property
        def path(self) -> str:
            """Path to unix socket."""
            return self._path

        async def _create_connection(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> ResponseHandler:
            try:
                with CeilTimeout(timeout.sock_connect):
                    _, proto = await self._loop.create_unix_connection(self._factory, self._path)
            except OSError as exc:
                try:
                    raise ClientConnectorError(req.connection_key, exc) from exc
                finally:
                    exc = None
                    del exc

            else:
                return cast(ResponseHandler, proto)


    class NamedPipeConnector(BaseConnector):
        __doc__ = 'Named pipe connector.\n\n    Only supported by the proactor event loop.\n    See also: https://docs.python.org/3.7/library/asyncio-eventloop.html\n\n    path - Windows named pipe path.\n    keepalive_timeout - (optional) Keep-alive timeout.\n    force_close - Set to True to force close and do reconnect\n        after each request (and between redirects).\n    limit - The total number of simultaneous connections.\n    limit_per_host - Number of simultaneous connections to one host.\n    loop - Optional event loop.\n    '

        def __init__(self, path, force_close=False, keepalive_timeout=sentinel, limit=100, limit_per_host=0, loop=None):
            super().__init__(force_close=force_close, keepalive_timeout=keepalive_timeout,
              limit=limit,
              limit_per_host=limit_per_host,
              loop=loop)
            if not isinstance(self._loop, asyncio.ProactorEventLoop):
                raise RuntimeError('Named Pipes only available in proactor loop under windows')
            self._path = path

        @property
        def path(self) -> str:
            """Path to the named pipe."""
            return self._path

        async def _create_connection(self, req: 'ClientRequest', traces: List['Trace'], timeout: 'ClientTimeout') -> ResponseHandler:
            try:
                with CeilTimeout(timeout.sock_connect):
                    _, proto = await self._loop.create_pipe_connection(self._factory, self._path)
                    await asyncio.sleep(0)
            except OSError as exc:
                try:
                    raise ClientConnectorError(req.connection_key, exc) from exc
                finally:
                    exc = None
                    del exc

            else:
                return cast(ResponseHandler, proto)