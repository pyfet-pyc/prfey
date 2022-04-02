# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\client_reqrep.py
import asyncio, codecs, io, re, sys, traceback, warnings
from hashlib import md5, sha1, sha256
from http.cookies import CookieError, Morsel, SimpleCookie
from types import MappingProxyType, TracebackType
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Mapping, Optional, Tuple, Type, Union, cast
import attr
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy
from yarl import URL
from . import hdrs, helpers, http, multipart, payload
from .abc import AbstractStreamWriter
from .client_exceptions import ClientConnectionError, ClientOSError, ClientResponseError, ContentTypeError, InvalidURL, ServerFingerprintMismatch
from .formdata import FormData
from .helpers import PY_36, BaseTimerContext, BasicAuth, HeadersMixin, TimerNoop, noop, reify, set_result
from .http import SERVER_SOFTWARE, HttpVersion10, HttpVersion11, StreamWriter
from .log import client_logger
from .streams import StreamReader
from .typedefs import DEFAULT_JSON_DECODER, JSONDecoder, LooseCookies, LooseHeaders, RawHeaders
try:
    import ssl
    from ssl import SSLContext
except ImportError:
    ssl = None
    SSLContext = object
else:
    try:
        import cchardet as chardet
    except ImportError:
        import chardet
    else:
        __all__ = ('ClientRequest', 'ClientResponse', 'RequestInfo', 'Fingerprint')
        if TYPE_CHECKING:
            from .client import ClientSession
            from .connector import Connection
            from .tracing import Trace
        else:
            json_re = re.compile('^application/(?:[\\w.+-]+?\\+)?json')

            @attr.s(frozen=True, slots=True)
            class ContentDisposition:
                type = attr.ib(type=str)
                parameters = attr.ib(type=MappingProxyType)
                filename = attr.ib(type=str)


            @attr.s(frozen=True, slots=True)
            class RequestInfo:
                url = attr.ib(type=URL)
                method = attr.ib(type=str)
                headers = attr.ib(type=CIMultiDictProxy)
                real_url = attr.ib(type=URL)

                @real_url.default
                def real_url_default(self) -> URL:
                    return self.url


            class Fingerprint:
                HASHFUNC_BY_DIGESTLEN = {16:md5, 
                 20:sha1, 
                 32:sha256}

                def __init__(self, fingerprint: bytes) -> None:
                    digestlen = len(fingerprint)
                    hashfunc = self.HASHFUNC_BY_DIGESTLEN.get(digestlen)
                    if not hashfunc:
                        raise ValueError('fingerprint has invalid length')
                    else:
                        if hashfunc is md5 or hashfunc is sha1:
                            raise ValueError('md5 and sha1 are insecure and not supported. Use sha256.')
                    self._hashfunc = hashfunc
                    self._fingerprint = fingerprint

                @property
                def fingerprint(self) -> bytes:
                    return self._fingerprint

                def check(self, transport: asyncio.Transport) -> None:
                    if not transport.get_extra_info('sslcontext'):
                        return
                    sslobj = transport.get_extra_info('ssl_object')
                    cert = sslobj.getpeercert(binary_form=True)
                    got = self._hashfunc(cert).digest()
                    if got != self._fingerprint:
                        host, port, *_ = transport.get_extra_info('peername')
                        raise ServerFingerprintMismatch(self._fingerprint, got, host, port)


            if ssl is not None:
                SSL_ALLOWED_TYPES = (
                 ssl.SSLContext, bool, Fingerprint, type(None))
            else:
                SSL_ALLOWED_TYPES = type(None)

        def _merge_ssl_params(ssl: Union[('SSLContext', bool, Fingerprint, None)], verify_ssl: Optional[bool], ssl_context: Optional['SSLContext'], fingerprint: Optional[bytes]) -> Union[('SSLContext', bool, Fingerprint, None)]:
            if verify_ssl is not None:
                if not verify_ssl:
                    warnings.warn('verify_ssl is deprecated, use ssl=False instead', DeprecationWarning,
                      stacklevel=3)
                    if ssl is not None:
                        raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
                    else:
                        ssl = False
            else:
                if ssl_context is not None:
                    warnings.warn('ssl_context is deprecated, use ssl=context instead', DeprecationWarning,
                      stacklevel=3)
                    if ssl is not None:
                        raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
                    else:
                        ssl = ssl_context
                elif fingerprint is not None:
                    warnings.warn('fingerprint is deprecated, use ssl=Fingerprint(fingerprint) instead', DeprecationWarning,
                      stacklevel=3)
                    if ssl is not None:
                        raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
                    else:
                        ssl = Fingerprint(fingerprint)
                assert isinstance(ssl, SSL_ALLOWED_TYPES), 'ssl should be SSLContext, bool, Fingerprint or None, got {!r} instead.'.format(ssl)
            return ssl


        @attr.s(slots=True, frozen=True)
        class ConnectionKey:
            host = attr.ib(type=str)
            port = attr.ib(type=int)
            is_ssl = attr.ib(type=bool)
            ssl = attr.ib()
            proxy = attr.ib()
            proxy_auth = attr.ib()
            proxy_headers_hash = attr.ib(type=int)


        def _is_expected_content_type(response_content_type: str, expected_content_type: str) -> bool:
            if expected_content_type == 'application/json':
                return json_re.match(response_content_type) is not None
            return expected_content_type in response_content_type


        class ClientRequest:
            GET_METHODS = {
             hdrs.METH_GET,
             hdrs.METH_HEAD,
             hdrs.METH_OPTIONS,
             hdrs.METH_TRACE}
            POST_METHODS = {
             hdrs.METH_PATCH, hdrs.METH_POST, hdrs.METH_PUT}
            ALL_METHODS = GET_METHODS.union(POST_METHODS).union({hdrs.METH_DELETE})
            DEFAULT_HEADERS = {hdrs.ACCEPT: '*/*', 
             hdrs.ACCEPT_ENCODING: 'gzip, deflate'}
            body = b''
            auth = None
            response = None
            _writer = None
            _continue = None

            def __init__(self, method: str, url: URL, *, params: Optional[Mapping[(str, str)]]=None, headers: Optional[LooseHeaders]=None, skip_auto_headers: Iterable[str]=frozenset(), data: Any=None, cookies: Optional[LooseCookies]=None, auth: Optional[BasicAuth]=None, version: http.HttpVersion=http.HttpVersion11, compress: Optional[str]=None, chunked: Optional[bool]=None, expect100: bool=False, loop: Optional[asyncio.AbstractEventLoop]=None, response_class: Optional[Type['ClientResponse']]=None, proxy: Optional[URL]=None, proxy_auth: Optional[BasicAuth]=None, timer: Optional[BaseTimerContext]=None, session: Optional['ClientSession']=None, ssl: Union[(SSLContext, bool, Fingerprint, None)]=None, proxy_headers: Optional[LooseHeaders]=None, traces: Optional[List['Trace']]=None):
                if loop is None:
                    loop = asyncio.get_event_loop()
                else:
                    assert isinstance(url, URL), url
                    assert isinstance(proxy, (URL, type(None))), proxy
                    self._session = cast('ClientSession', session)
                    if params:
                        q = MultiDict(url.query)
                        url2 = url.with_query(params)
                        q.extend(url2.query)
                        url = url.with_query(q)
                    self.original_url = url
                    self.url = url.with_fragment(None)
                    self.method = method.upper()
                    self.chunked = chunked
                    self.compress = compress
                    self.loop = loop
                    self.length = None
                    if response_class is None:
                        real_response_class = ClientResponse
                    else:
                        real_response_class = response_class
                self.response_class = real_response_class
                self._timer = timer if timer is not None else TimerNoop()
                self._ssl = ssl
                if loop.get_debug():
                    self._source_traceback = traceback.extract_stack(sys._getframe(1))
                self.update_version(version)
                self.update_host(url)
                self.update_headers(headers)
                self.update_auto_headers(skip_auto_headers)
                self.update_cookies(cookies)
                self.update_content_encoding(data)
                self.update_auth(auth)
                self.update_proxy(proxy, proxy_auth, proxy_headers)
                self.update_body_from_data(data)
                if data or self.method not in self.GET_METHODS:
                    self.update_transfer_encoding()
                self.update_expect_continue(expect100)
                if traces is None:
                    traces = []
                self._traces = traces

            def is_ssl(self) -> bool:
                return self.url.scheme in ('https', 'wss')

            @property
            def ssl(self) -> Union[('SSLContext', None, bool, Fingerprint)]:
                return self._ssl

            @property
            def connection_key(self) -> ConnectionKey:
                proxy_headers = self.proxy_headers
                if proxy_headers:
                    h = hash(tuple(((k, v) for k, v in proxy_headers.items())))
                else:
                    h = None
                return ConnectionKey(self.host, self.port, self.is_ssl(), self.ssl, self.proxy, self.proxy_auth, h)

            @property
            def host(self) -> str:
                ret = self.url.host
                assert ret is not None
                return ret

            @property
            def port(self) -> Optional[int]:
                return self.url.port

            @property
            def request_info(self) -> RequestInfo:
                headers = CIMultiDictProxy(self.headers)
                return RequestInfo(self.url, self.method, headers, self.original_url)

            def update_host(self, url: URL) -> None:
                """Update destination host, port and connection type (ssl)."""
                if not url.host:
                    raise InvalidURL(url)
                username, password = url.user, url.password
                if username:
                    self.auth = helpers.BasicAuth(username, password or '')

            def update_version(self, version: Union[(http.HttpVersion, str)]) -> None:
                """Convert request version to two elements tuple.

        parser HTTP version '1.1' => (1, 1)
        """
                if isinstance(version, str):
                    v = [l.strip() for l in version.split('.', 1)]
                    try:
                        version = http.HttpVersion(int(v[0]), int(v[1]))
                    except ValueError:
                        raise ValueError('Can not parse http version number: {}'.format(version)) from None

                self.version = version

            def update_headers(self, headers: Optional[LooseHeaders]) -> None:
                """Update request headers."""
                self.headers = CIMultiDict()
                netloc = cast(str, self.url.raw_host)
                if helpers.is_ipv6_address(netloc):
                    netloc = '[{}]'.format(netloc)
                if self.url.port is not None:
                    if not self.url.is_default_port():
                        netloc += ':' + str(self.url.port)
                self.headers[hdrs.HOST] = netloc
                if headers:
                    if isinstance(headers, (dict, MultiDictProxy, MultiDict)):
                        headers = headers.items()
                    for key, value in headers:
                        if key.lower() == 'host':
                            self.headers[key] = value
                        else:
                            self.headers.add(key, value)

            def update_auto_headers(self, skip_auto_headers: Iterable[str]) -> None:
                self.skip_auto_headers = CIMultiDict(((
                 hdr, None) for hdr in sorted(skip_auto_headers)))
                used_headers = self.headers.copy()
                used_headers.extend(self.skip_auto_headers)
                for hdr, val in self.DEFAULT_HEADERS.items():
                    if hdr not in used_headers:
                        self.headers.add(hdr, val)
                else:
                    if hdrs.USER_AGENT not in used_headers:
                        self.headers[hdrs.USER_AGENT] = SERVER_SOFTWARE

            def update_cookies(self, cookies: Optional[LooseCookies]) -> None:
                """Update request cookies header."""
                if not cookies:
                    return
                else:
                    c = SimpleCookie()
                    if hdrs.COOKIE in self.headers:
                        c.load(self.headers.get(hdrs.COOKIE, ''))
                        del self.headers[hdrs.COOKIE]
                    if isinstance(cookies, Mapping):
                        iter_cookies = cookies.items()
                    else:
                        iter_cookies = cookies
                for name, value in iter_cookies:
                    if isinstance(value, Morsel):
                        mrsl_val = value.get(value.key, Morsel())
                        mrsl_val.set(value.key, value.value, value.coded_value)
                        c[name] = mrsl_val
                    else:
                        c[name] = value
                else:
                    self.headers[hdrs.COOKIE] = c.output(header='', sep=';').strip()

            def update_content_encoding(self, data: Any) -> None:
                """Set request content encoding."""
                if not data:
                    return
                    enc = self.headers.get(hdrs.CONTENT_ENCODING, '').lower()
                    if enc:
                        if self.compress:
                            raise ValueError('compress can not be set if Content-Encoding header is set')
                elif self.compress:
                    if not isinstance(self.compress, str):
                        self.compress = 'deflate'
                    self.headers[hdrs.CONTENT_ENCODING] = self.compress
                    self.chunked = True

            def update_transfer_encoding(self) -> None:
                """Analyze transfer-encoding header."""
                te = self.headers.get(hdrs.TRANSFER_ENCODING, '').lower()
                if 'chunked' in te:
                    if self.chunked:
                        raise ValueError('chunked can not be set if "Transfer-Encoding: chunked" header is set')
                elif self.chunked:
                    if hdrs.CONTENT_LENGTH in self.headers:
                        raise ValueError('chunked can not be set if Content-Length header is set')
                    self.headers[hdrs.TRANSFER_ENCODING] = 'chunked'
                else:
                    if hdrs.CONTENT_LENGTH not in self.headers:
                        self.headers[hdrs.CONTENT_LENGTH] = str(len(self.body))

            def update_auth(self, auth: Optional[BasicAuth]) -> None:
                """Set basic auth."""
                if auth is None:
                    auth = self.auth
                else:
                    if auth is None:
                        return
                    assert isinstance(auth, helpers.BasicAuth), 'BasicAuth() tuple is required instead'
                self.headers[hdrs.AUTHORIZATION] = auth.encode()

            def update_body_from_data(self, body: Any) -> None:
                if not body:
                    return
                if isinstance(body, FormData):
                    body = body()
                try:
                    body = payload.PAYLOAD_REGISTRY.get(body, disposition=None)
                except payload.LookupError:
                    body = FormData(body)()
                else:
                    self.body = body
                    if not self.chunked:
                        if hdrs.CONTENT_LENGTH not in self.headers:
                            size = body.size
                            if size is None:
                                self.chunked = True
                            else:
                                if hdrs.CONTENT_LENGTH not in self.headers:
                                    self.headers[hdrs.CONTENT_LENGTH] = str(size)
                    assert body.headers
                    for key, value in body.headers.items():
                        if key in self.headers:
                            pass
                        elif key in self.skip_auto_headers:
                            pass
                        else:
                            self.headers[key] = value

            def update_expect_continue(self, expect: bool=False) -> None:
                if expect:
                    self.headers[hdrs.EXPECT] = '100-continue'
                else:
                    if self.headers.get(hdrs.EXPECT, '').lower() == '100-continue':
                        expect = True
                if expect:
                    self._continue = self.loop.create_future()

            def update_proxy(self, proxy: Optional[URL], proxy_auth: Optional[BasicAuth], proxy_headers: Optional[LooseHeaders]) -> None:
                if proxy:
                    if not proxy.scheme == 'http':
                        raise ValueError('Only http proxies are supported')
                if proxy_auth:
                    if not isinstance(proxy_auth, helpers.BasicAuth):
                        raise ValueError('proxy_auth must be None or BasicAuth() tuple')
                self.proxy = proxy
                self.proxy_auth = proxy_auth
                self.proxy_headers = proxy_headers

            def keep_alive(self) -> bool:
                if self.version < HttpVersion10:
                    return False
                elif self.version == HttpVersion10:
                    if self.headers.get(hdrs.CONNECTION) == 'keep-alive':
                        return True
                    return False
                else:
                    if self.headers.get(hdrs.CONNECTION) == 'close':
                        return False
                return True

            async def write_bytes(self, writer: AbstractStreamWriter, conn: 'Connection') -> None:
                """Support coroutines that yields bytes objects."""
                if self._continue is not None:
                    await writer.drain()
                    await self._continue
                protocol = conn.protocol
                assert protocol is not None
                try:
                    try:
                        if isinstance(self.body, payload.Payload):
                            await self.body.write(writer)
                        else:
                            if isinstance(self.body, (bytes, bytearray)):
                                self.body = (
                                 self.body,)
                            for chunk in self.body:
                                await writer.write(chunk)
                            else:
                                await writer.write_eof()

                    except OSError as exc:
                        try:
                            new_exc = ClientOSError(exc.errno, 'Can not write request body for %s' % self.url)
                            new_exc.__context__ = exc
                            new_exc.__cause__ = exc
                            protocol.set_exception(new_exc)
                        finally:
                            exc = None
                            del exc

                    except asyncio.CancelledError as exc:
                        try:
                            if not conn.closed:
                                protocol.set_exception(exc)
                        finally:
                            exc = None
                            del exc

                    except Exception as exc:
                        try:
                            protocol.set_exception(exc)
                        finally:
                            exc = None
                            del exc

                finally:
                    self._writer = None

            async def send(self, conn: 'Connection') -> 'ClientResponse':
                if self.method == hdrs.METH_CONNECT:
                    connect_host = self.url.raw_host
                    assert connect_host is not None
                    if helpers.is_ipv6_address(connect_host):
                        connect_host = '[{}]'.format(connect_host)
                    path = '{}:{}'.format(connect_host, self.url.port)
                else:
                    if self.proxy:
                        path = self.is_ssl() or str(self.url)
                    else:
                        path = self.url.raw_path
                        if self.url.raw_query_string:
                            path += '?' + self.url.raw_query_string
                        else:
                            protocol = conn.protocol
                            assert protocol is not None
                            writer = StreamWriter(protocol,
                              (self.loop), on_chunk_sent=(self._on_chunk_request_sent))
                            if self.compress:
                                writer.enable_compression(self.compress)
                            if self.chunked is not None:
                                writer.enable_chunking()
                            if self.method in self.POST_METHODS:
                                if hdrs.CONTENT_TYPE not in self.skip_auto_headers:
                                    if hdrs.CONTENT_TYPE not in self.headers:
                                        self.headers[hdrs.CONTENT_TYPE] = 'application/octet-stream'
                            connection = self.headers.get(hdrs.CONNECTION)
                            if not connection:
                                if self.keep_alive():
                                    if self.version == HttpVersion10:
                                        connection = 'keep-alive'
                            elif self.version == HttpVersion11:
                                connection = 'close'
                        if connection is not None:
                            self.headers[hdrs.CONNECTION] = connection
                        status_line = '{0} {1} HTTP/{2[0]}.{2[1]}'.format(self.method, path, self.version)
                        await writer.write_headers(status_line, self.headers)
                        self._writer = self.loop.create_task(self.write_bytes(writer, conn))
                        response_class = self.response_class
                        assert response_class is not None
                        self.response = response_class((self.method),
                          (self.original_url), writer=(self._writer),
                          continue100=(self._continue),
                          timer=(self._timer),
                          request_info=(self.request_info),
                          traces=(self._traces),
                          loop=(self.loop),
                          session=(self._session))
                        return self.response

            async def close(self) -> None:
                if self._writer is not None:
                    try:
                        await self._writer
                    finally:
                        self._writer = None

            def terminate(self) -> None:
                if self._writer is not None:
                    if not self.loop.is_closed():
                        self._writer.cancel()
                    self._writer = None

            async def _on_chunk_request_sent(self, chunk: bytes) -> None:
                for trace in self._traces:
                    await trace.send_request_chunk_sent(chunk)


        class ClientResponse(HeadersMixin):
            version = None
            status = None
            reason = None
            content = None
            _headers = None
            _raw_headers = None
            _connection = None
            _source_traceback = None
            _closed = True
            _released = False

            def __init__(self, method: str, url: URL, *, writer: 'asyncio.Task[None]', continue100: Optional['asyncio.Future[bool]'], timer: BaseTimerContext, request_info: RequestInfo, traces: List['Trace'], loop: asyncio.AbstractEventLoop, session: 'ClientSession') -> None:
                assert isinstance(url, URL)
                self.method = method
                self.cookies = SimpleCookie()
                self._real_url = url
                self._url = url.with_fragment(None)
                self._body = None
                self._writer = writer
                self._continue = continue100
                self._closed = True
                self._history = ()
                self._request_info = request_info
                self._timer = timer if timer is not None else TimerNoop()
                self._cache = {}
                self._traces = traces
                self._loop = loop
                self._session = session
                if loop.get_debug():
                    self._source_traceback = traceback.extract_stack(sys._getframe(1))

            @reify
            def url(self) -> URL:
                return self._url

            @reify
            def url_obj(self) -> URL:
                warnings.warn('Deprecated, use .url #1654',
                  DeprecationWarning, stacklevel=2)
                return self._url

            @reify
            def real_url(self) -> URL:
                return self._real_url

            @reify
            def host(self) -> str:
                assert self._url.host is not None
                return self._url.host

            @reify
            def headers(self) -> 'CIMultiDictProxy[str]':
                return self._headers

            @reify
            def raw_headers(self) -> RawHeaders:
                return self._raw_headers

            @reify
            def request_info(self) -> RequestInfo:
                return self._request_info

            @reify
            def content_disposition(self) -> Optional[ContentDisposition]:
                raw = self._headers.get(hdrs.CONTENT_DISPOSITION)
                if raw is None:
                    return
                disposition_type, params_dct = multipart.parse_content_disposition(raw)
                params = MappingProxyType(params_dct)
                filename = multipart.content_disposition_filename(params)
                return ContentDisposition(disposition_type, params, filename)

            def __del__(self, _warnings: Any=warnings) -> None:
                if self._closed:
                    return
                if self._connection is not None:
                    self._connection.release()
                    self._cleanup_writer()
                    if self._loop.get_debug():
                        if PY_36:
                            kwargs = {'source': self}
                        else:
                            kwargs = {}
                        (_warnings.warn)(('Unclosed response {!r}'.format(self)), 
                         ResourceWarning, **kwargs)
                        context = {'client_response':self,  'message':'Unclosed response'}
                        if self._source_traceback:
                            context['source_traceback'] = self._source_traceback
                        self._loop.call_exception_handler(context)

            def __repr__(self) -> str:
                out = io.StringIO()
                ascii_encodable_url = str(self.url)
                if self.reason:
                    ascii_encodable_reason = self.reason.encode('ascii', 'backslashreplace').decode('ascii')
                else:
                    ascii_encodable_reason = self.reason
                print(('<ClientResponse({}) [{} {}]>'.format(ascii_encodable_url, self.status, ascii_encodable_reason)),
                  file=out)
                print((self.headers), file=out)
                return out.getvalue()

            @property
            def connection(self) -> Optional['Connection']:
                return self._connection

            @reify
            def history(self) -> Tuple[('ClientResponse', Ellipsis)]:
                """A sequence of of responses, if redirects occurred."""
                return self._history

            @reify
            def links(self) -> 'MultiDictProxy[MultiDictProxy[Union[str, URL]]]':
                links_str = ', '.join(self.headers.getall('link', []))
                if not links_str:
                    return MultiDictProxy(MultiDict())
                links = MultiDict()
                for val in re.split(',(?=\\s*<)', links_str):
                    match = re.match('\\s*<(.*)>(.*)', val)
                    if match is None:
                        pass
                    else:
                        url, params_str = match.groups()
                        params = params_str.split(';')[1:]
                        link = MultiDict()
                        for param in params:
                            match = re.match('^\\s*(\\S*)\\s*=\\s*([\'\\"]?)(.*?)(\\2)\\s*$', param, re.M)
                            if match is None:
                                pass
                            else:
                                key, _, value, _ = match.groups()
                                link.add(key, value)
                        else:
                            key = link.get('rel', url)
                            link.add('url', self.url.join(URL(url)))
                            links.add(key, MultiDictProxy(link))

                else:
                    return MultiDictProxy(links)

            async def start--- This code section failed: ---

 L. 839         0  LOAD_CONST               False
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _closed

 L. 840         6  LOAD_FAST                'connection'
                8  LOAD_ATTR                protocol
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _protocol

 L. 841        14  LOAD_FAST                'connection'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _connection

 L. 843        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _timer
               24  SETUP_WITH          186  'to 186'
               26  POP_TOP          
             28_0  COME_FROM           160  '160'

 L. 846        28  SETUP_FINALLY        54  'to 54'

 L. 847        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _protocol
               34  LOAD_METHOD              read
               36  CALL_METHOD_0         0  ''
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'message'
               48  STORE_FAST               'payload'
               50  POP_BLOCK        
               52  JUMP_FORWARD        120  'to 120'
             54_0  COME_FROM_FINALLY    28  '28'

 L. 848        54  DUP_TOP          
               56  LOAD_GLOBAL              http
               58  LOAD_ATTR                HttpProcessingError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   118  'to 118'
               64  POP_TOP          
               66  STORE_FAST               'exc'
               68  POP_TOP          
               70  SETUP_FINALLY       106  'to 106'

 L. 849        72  LOAD_GLOBAL              ClientResponseError

 L. 850        74  LOAD_FAST                'self'
               76  LOAD_ATTR                request_info

 L. 850        78  LOAD_FAST                'self'
               80  LOAD_ATTR                history

 L. 851        82  LOAD_FAST                'exc'
               84  LOAD_ATTR                code

 L. 852        86  LOAD_FAST                'exc'
               88  LOAD_ATTR                message

 L. 852        90  LOAD_FAST                'exc'
               92  LOAD_ATTR                headers

 L. 849        94  LOAD_CONST               ('status', 'message', 'headers')
               96  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L. 852        98  LOAD_FAST                'exc'

 L. 849       100  RAISE_VARARGS_2       2  'exception instance with __cause__'
              102  POP_BLOCK        
              104  BEGIN_FINALLY    
            106_0  COME_FROM_FINALLY    70  '70'
              106  LOAD_CONST               None
              108  STORE_FAST               'exc'
              110  DELETE_FAST              'exc'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            62  '62'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            52  '52'

 L. 854       120  LOAD_FAST                'message'
              122  LOAD_ATTR                code
              124  LOAD_CONST               100
              126  COMPARE_OP               <
              128  POP_JUMP_IF_TRUE    182  'to 182'

 L. 855       130  LOAD_FAST                'message'
              132  LOAD_ATTR                code
              134  LOAD_CONST               199
              136  COMPARE_OP               >

 L. 854       138  POP_JUMP_IF_TRUE    182  'to 182'

 L. 855       140  LOAD_FAST                'message'
              142  LOAD_ATTR                code
              144  LOAD_CONST               101
              146  COMPARE_OP               ==

 L. 854       148  POP_JUMP_IF_FALSE   152  'to 152'

 L. 856       150  BREAK_LOOP          182  'to 182'
            152_0  COME_FROM           148  '148'

 L. 858       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _continue
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE    28  'to 28'

 L. 859       162  LOAD_GLOBAL              set_result
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _continue
              168  LOAD_CONST               True
              170  CALL_FUNCTION_2       2  ''
              172  POP_TOP          

 L. 860       174  LOAD_CONST               None
              176  LOAD_FAST                'self'
              178  STORE_ATTR               _continue
              180  JUMP_BACK            28  'to 28'
            182_0  COME_FROM           138  '138'
            182_1  COME_FROM           128  '128'
              182  POP_BLOCK        
              184  BEGIN_FINALLY    
            186_0  COME_FROM_WITH       24  '24'
              186  WITH_CLEANUP_START
              188  WITH_CLEANUP_FINISH
              190  END_FINALLY      

 L. 863       192  LOAD_FAST                'payload'
              194  LOAD_METHOD              on_eof
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                _response_eof
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L. 866       204  LOAD_FAST                'message'
              206  LOAD_ATTR                version
              208  LOAD_FAST                'self'
              210  STORE_ATTR               version

 L. 867       212  LOAD_FAST                'message'
              214  LOAD_ATTR                code
              216  LOAD_FAST                'self'
              218  STORE_ATTR               status

 L. 868       220  LOAD_FAST                'message'
              222  LOAD_ATTR                reason
              224  LOAD_FAST                'self'
              226  STORE_ATTR               reason

 L. 871       228  LOAD_FAST                'message'
              230  LOAD_ATTR                headers
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _headers

 L. 872       236  LOAD_FAST                'message'
              238  LOAD_ATTR                raw_headers
              240  LOAD_FAST                'self'
              242  STORE_ATTR               _raw_headers

 L. 875       244  LOAD_FAST                'payload'
              246  LOAD_FAST                'self'
              248  STORE_ATTR               content

 L. 878       250  LOAD_FAST                'self'
              252  LOAD_ATTR                headers
              254  LOAD_METHOD              getall
              256  LOAD_GLOBAL              hdrs
              258  LOAD_ATTR                SET_COOKIE
              260  LOAD_CONST               ()
              262  CALL_METHOD_2         2  ''
              264  GET_ITER         
              266  FOR_ITER            340  'to 340'
              268  STORE_FAST               'hdr'

 L. 879       270  SETUP_FINALLY       288  'to 288'

 L. 880       272  LOAD_FAST                'self'
              274  LOAD_ATTR                cookies
              276  LOAD_METHOD              load
              278  LOAD_FAST                'hdr'
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          
              284  POP_BLOCK        
              286  JUMP_BACK           266  'to 266'
            288_0  COME_FROM_FINALLY   270  '270'

 L. 881       288  DUP_TOP          
              290  LOAD_GLOBAL              CookieError
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   334  'to 334'
              298  POP_TOP          
              300  STORE_FAST               'exc'
              302  POP_TOP          
              304  SETUP_FINALLY       322  'to 322'

 L. 882       306  LOAD_GLOBAL              client_logger
              308  LOAD_METHOD              warning

 L. 883       310  LOAD_STR                 'Can not load response cookies: %s'

 L. 883       312  LOAD_FAST                'exc'

 L. 882       314  CALL_METHOD_2         2  ''
              316  POP_TOP          
              318  POP_BLOCK        
              320  BEGIN_FINALLY    
            322_0  COME_FROM_FINALLY   304  '304'
              322  LOAD_CONST               None
              324  STORE_FAST               'exc'
              326  DELETE_FAST              'exc'
              328  END_FINALLY      
              330  POP_EXCEPT       
              332  JUMP_BACK           266  'to 266'
            334_0  COME_FROM           294  '294'
              334  END_FINALLY      
          336_338  JUMP_BACK           266  'to 266'

 L. 884       340  LOAD_FAST                'self'
              342  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 184

            def _response_eof(self) -> None:
                if self._closed:
                    return
                if self._connection is not None:
                    if self._connection.protocol is not None:
                        if self._connection.protocol.upgraded:
                            return
                    self._connection.release()
                    self._connection = None
                self._closed = True
                self._cleanup_writer()

            @property
            def closed(self) -> bool:
                return self._closed

            def close(self) -> None:
                if not self._released:
                    self._notify_content()
                if self._closed:
                    return
                self._closed = True
                if self._loop is None or self._loop.is_closed():
                    return
                if self._connection is not None:
                    self._connection.close()
                    self._connection = None
                self._cleanup_writer()

            def release(self) -> Any:
                if not self._released:
                    self._notify_content()
                if self._closed:
                    return noop()
                self._closed = True
                if self._connection is not None:
                    self._connection.release()
                    self._connection = None
                self._cleanup_writer()
                return noop()

            def raise_for_status(self) -> None:
                if 400 <= self.status:
                    assert self.reason is not None
                    self.release()
                    raise ClientResponseError((self.request_info),
                      (self.history),
                      status=(self.status),
                      message=(self.reason),
                      headers=(self.headers))

            def _cleanup_writer(self) -> None:
                if self._writer is not None:
                    self._writer.cancel()
                self._writer = None
                self._session = None

            def _notify_content(self) -> None:
                content = self.content
                if content:
                    if content.exception() is None:
                        content.set_exception(ClientConnectionError('Connection closed'))
                self._released = True

            async def wait_for_close(self) -> None:
                if self._writer is not None:
                    try:
                        await self._writer
                    finally:
                        self._writer = None

                self.release()

            async def read(self) -> bytes:
                """Read response payload."""
                if self._body is None:
                    try:
                        self._body = await self.content.read()
                        for trace in self._traces:
                            await trace.send_response_chunk_received(self._body)

                    except BaseException:
                        self.close()
                        raise

                else:
                    if self._released:
                        raise ClientConnectionError('Connection closed')
                return self._body

            def get_encoding(self) -> str:
                ctype = self.headers.get(hdrs.CONTENT_TYPE, '').lower()
                mimetype = helpers.parse_mimetype(ctype)
                encoding = mimetype.parameters.get('charset')
                if encoding:
                    try:
                        codecs.lookup(encoding)
                    except LookupError:
                        encoding = None
                    else:
                        if not encoding:
                            if mimetype.type == 'application' and mimetype.subtype == 'json':
                                encoding = 'utf-8'
                else:
                    encoding = chardet.detect(self._body)['encoding']
                if not encoding:
                    encoding = 'utf-8'
                return encoding

            async def text(self, encoding: Optional[str]=None, errors: str='strict') -> str:
                """Read response payload and decode."""
                if self._body is None:
                    await self.read()
                if encoding is None:
                    encoding = self.get_encoding()
                return self._body.decode(encoding, errors=errors)

            async def json(self, *, encoding: str=None, loads: JSONDecoder=DEFAULT_JSON_DECODER, content_type: Optional[str]='application/json') -> Any:
                """Read and decodes JSON response."""
                if self._body is None:
                    await self.read()
                else:
                    if content_type:
                        ctype = self.headers.get(hdrs.CONTENT_TYPE, '').lower()
                        if not _is_expected_content_type(ctype, content_type):
                            raise ContentTypeError((self.request_info),
                              (self.history),
                              message=('Attempt to decode JSON with unexpected mimetype: %s' % ctype),
                              headers=(self.headers))
                    stripped = self._body.strip()
                    return stripped or None
                if encoding is None:
                    encoding = self.get_encoding()
                return loads(stripped.decode(encoding))

            async def __aenter__(self) -> 'ClientResponse':
                return self

            async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
                self.release()