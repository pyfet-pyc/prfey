# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\client.py
"""
:mod:`websockets.client` defines the WebSocket client APIs.

"""
import asyncio, collections.abc, functools, logging, warnings
from types import TracebackType
from typing import Any, Generator, List, Optional, Sequence, Tuple, Type, cast
from .exceptions import InvalidHandshake, InvalidHeader, InvalidMessage, InvalidStatusCode, NegotiationError, RedirectHandshake, SecurityError
from extensions.base import ClientExtensionFactory, Extension
from extensions.permessage_deflate import ClientPerMessageDeflateFactory
from .handshake import build_request, check_response
from .headers import build_authorization_basic, build_extension, build_subprotocol, parse_extension, parse_subprotocol
from .http import USER_AGENT, Headers, HeadersLike, read_response
from .protocol import WebSocketCommonProtocol
from .typing import ExtensionHeader, Origin, Subprotocol
from .uri import WebSocketURI, parse_uri
__all__ = [
 'connect', 'unix_connect', 'WebSocketClientProtocol']
logger = logging.getLogger(__name__)

class WebSocketClientProtocol(WebSocketCommonProtocol):
    __doc__ = '\n    :class:`~asyncio.Protocol` subclass implementing a WebSocket client.\n\n    This class inherits most of its methods from\n    :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    '
    is_client = True
    side = 'client'

    def __init__(self, *, origin=None, extensions=None, subprotocols=None, extra_headers=None, **kwargs):
        self.origin = origin
        self.available_extensions = extensions
        self.available_subprotocols = subprotocols
        self.extra_headers = extra_headers
        (super().__init__)(**kwargs)

    def write_http_request(self, path: str, headers: Headers) -> None:
        """
        Write request line and headers to the HTTP request.

        """
        self.path = path
        self.request_headers = headers
        logger.debug('%s > GET %s HTTP/1.1', self.side, path)
        logger.debug('%s > %r', self.side, headers)
        request = f"GET {path} HTTP/1.1\r\n"
        request += str(headers)
        self.transport.write(request.encode())

    async def read_http_response(self) -> Tuple[(int, Headers)]:
        """
        Read status line and headers from the HTTP response.

        If the response contains a body, it may be read from ``self.reader``
        after this coroutine returns.

        :raises ~websockets.exceptions.InvalidMessage: if the HTTP message is
            malformed or isn't an HTTP/1.1 GET response

        """
        try:
            status_code, reason, headers = await read_response(self.reader)
        except Exception as exc:
            try:
                raise InvalidMessage('did not receive a valid HTTP response') from exc
            finally:
                exc = None
                del exc

        else:
            logger.debug('%s < HTTP/1.1 %d %s', self.side, status_code, reason)
            logger.debug('%s < %r', self.side, headers)
            self.response_headers = headers
            return (
             status_code, self.response_headers)

    @staticmethod
    def process_extensions--- This code section failed: ---

 L. 143         0  BUILD_LIST_0          0 
                2  STORE_FAST               'accepted_extensions'

 L. 145         4  LOAD_FAST                'headers'
                6  LOAD_METHOD              get_all
                8  LOAD_STR                 'Sec-WebSocket-Extensions'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'header_values'

 L. 147        14  LOAD_FAST                'header_values'
               16  POP_JUMP_IF_FALSE   166  'to 166'

 L. 149        18  LOAD_FAST                'available_extensions'
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 150        26  LOAD_GLOBAL              InvalidHandshake
               28  LOAD_STR                 'no extensions supported'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 152        34  LOAD_GLOBAL              sum

 L. 153        36  LOAD_LISTCOMP            '<code_object <listcomp>>'
               38  LOAD_STR                 'WebSocketClientProtocol.process_extensions.<locals>.<listcomp>'
               40  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               42  LOAD_FAST                'header_values'
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''

 L. 153        48  BUILD_LIST_0          0 

 L. 152        50  CALL_FUNCTION_2       2  ''
               52  STORE_FAST               'parsed_header_values'

 L. 156        54  LOAD_FAST                'parsed_header_values'
               56  GET_ITER         
               58  FOR_ITER            166  'to 166'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'name'
               64  STORE_FAST               'response_params'

 L. 158        66  LOAD_FAST                'available_extensions'
               68  GET_ITER         
               70  FOR_ITER            144  'to 144'
               72  STORE_FAST               'extension_factory'

 L. 161        74  LOAD_FAST                'extension_factory'
               76  LOAD_ATTR                name
               78  LOAD_FAST                'name'
               80  COMPARE_OP               !=
               82  POP_JUMP_IF_FALSE    86  'to 86'

 L. 162        84  JUMP_BACK            70  'to 70'
             86_0  COME_FROM            82  '82'

 L. 165        86  SETUP_FINALLY       104  'to 104'

 L. 166        88  LOAD_FAST                'extension_factory'
               90  LOAD_METHOD              process_response_params

 L. 167        92  LOAD_FAST                'response_params'

 L. 167        94  LOAD_FAST                'accepted_extensions'

 L. 166        96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'extension'
              100  POP_BLOCK        
              102  JUMP_FORWARD        128  'to 128'
            104_0  COME_FROM_FINALLY    86  '86'

 L. 169       104  DUP_TOP          
              106  LOAD_GLOBAL              NegotiationError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   126  'to 126'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 170       118  POP_EXCEPT       
              120  JUMP_BACK            70  'to 70'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           110  '110'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM           102  '102'

 L. 173       128  LOAD_FAST                'accepted_extensions'
              130  LOAD_METHOD              append
              132  LOAD_FAST                'extension'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L. 176       138  POP_TOP          
              140  CONTINUE             58  'to 58'
              142  JUMP_BACK            70  'to 70'

 L. 181       144  LOAD_GLOBAL              NegotiationError

 L. 182       146  LOAD_STR                 'Unsupported extension: name = '
              148  LOAD_FAST                'name'
              150  FORMAT_VALUE          0  ''
              152  LOAD_STR                 ', params = '
              154  LOAD_FAST                'response_params'
              156  FORMAT_VALUE          0  ''
              158  BUILD_STRING_4        4 

 L. 181       160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
              164  JUMP_BACK            58  'to 58'
            166_0  COME_FROM            16  '16'

 L. 186       166  LOAD_FAST                'accepted_extensions'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 122

    @staticmethod
    def process_subprotocol(headers: Headers, available_subprotocols: Optional[Sequence[Subprotocol]]) -> Optional[Subprotocol]:
        """
        Handle the Sec-WebSocket-Protocol HTTP response header.

        Check that it contains exactly one supported subprotocol.

        Return the selected subprotocol.

        """
        subprotocol = None
        header_values = headers.get_all('Sec-WebSocket-Protocol')
        if header_values:
            if available_subprotocols is None:
                raise InvalidHandshake('no subprotocols supported')
            parsed_header_values = sum([parse_subprotocol(header_value) for header_value in header_values], [])
            if len(parsed_header_values) > 1:
                subprotocols = ', '.join(parsed_header_values)
                raise InvalidHandshake(f"multiple subprotocols: {subprotocols}")
            subprotocol = parsed_header_values[0]
            if subprotocol not in available_subprotocols:
                raise NegotiationError(f"unsupported subprotocol: {subprotocol}")
        return subprotocol

    async def handshake(self, wsuri: WebSocketURI, origin: Optional[Origin]=None, available_extensions: Optional[Sequence[ClientExtensionFactory]]=None, available_subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLike]=None) -> None:
        """
        Perform the client side of the opening handshake.

        :param origin: sets the Origin HTTP header
        :param available_extensions: list of supported extensions in the order
            in which they should be used
        :param available_subprotocols: list of supported subprotocols in order
            of decreasing preference
        :param extra_headers: sets additional HTTP request headers; it must be
            a :class:`~websockets.http.Headers` instance, a
            :class:`~collections.abc.Mapping`, or an iterable of ``(name,
            value)`` pairs
        :raises ~websockets.exceptions.InvalidHandshake: if the handshake
            fails

        """
        request_headers = Headers()
        if wsuri.port == (443 if wsuri.secure else 80):
            request_headers['Host'] = wsuri.host
        else:
            request_headers['Host'] = f"{wsuri.host}:{wsuri.port}"
        if wsuri.user_info:
            request_headers['Authorization'] = build_authorization_basic(*wsuri.user_info)
        if origin is not None:
            request_headers['Origin'] = origin
        key = build_request(request_headers)
        if available_extensions is not None:
            extensions_header = build_extension([(
             extension_factory.name, extension_factory.get_request_params()) for extension_factory in available_extensions])
            request_headers['Sec-WebSocket-Extensions'] = extensions_header
        if available_subprotocols is not None:
            protocol_header = build_subprotocol(available_subprotocols)
            request_headers['Sec-WebSocket-Protocol'] = protocol_header
        if extra_headers is not None:
            if isinstance(extra_headers, Headers):
                extra_headers = extra_headers.raw_items()
            else:
                if isinstance(extra_headers, collections.abc.Mapping):
                    extra_headers = extra_headers.items()
            for name, value in extra_headers:
                request_headers[name] = value

        request_headers.setdefault'User-Agent'USER_AGENT
        self.write_http_requestwsuri.resource_namerequest_headers
        status_code, response_headers = await self.read_http_response()
        if status_code in (301, 302, 303, 307, 308):
            if 'Location' not in response_headers:
                raise InvalidHeader('Location')
            raise RedirectHandshake(response_headers['Location'])
        else:
            if status_code != 101:
                raise InvalidStatusCode(status_code)
            check_response(response_headers, key)
            self.extensions = self.process_extensionsresponse_headersavailable_extensions
            self.subprotocol = self.process_subprotocolresponse_headersavailable_subprotocols
            self.connection_open()


class Connect:
    __doc__ = '\n    Connect to the WebSocket server at the given ``uri``.\n\n    Awaiting :func:`connect` yields a :class:`WebSocketClientProtocol` which\n    can then be used to send and receive messages.\n\n    :func:`connect` can also be used as a asynchronous context manager. In\n    that case, the connection is closed when exiting the context.\n\n    :func:`connect` is a wrapper around the event loop\'s\n    :meth:`~asyncio.loop.create_connection` method. Unknown keyword arguments\n    are passed to :meth:`~asyncio.loop.create_connection`.\n\n    For example, you can set the ``ssl`` keyword argument to a\n    :class:`~ssl.SSLContext` to enforce some TLS settings. When connecting to\n    a ``wss://`` URI, if this argument isn\'t provided explicitly,\n    :func:`ssl.create_default_context` is called to create a context.\n\n    You can connect to a different host and port from those found in ``uri``\n    by setting ``host`` and ``port`` keyword arguments. This only changes the\n    destination of the TCP connection. The host name from ``uri`` is still\n    used in the TLS handshake for secure connections and in the ``Host`` HTTP\n    header.\n\n    The ``create_protocol`` parameter allows customizing the\n    :class:`~asyncio.Protocol` that manages the connection. It should be a\n    callable or class accepting the same arguments as\n    :class:`WebSocketClientProtocol` and returning an instance of\n    :class:`WebSocketClientProtocol` or a subclass. It defaults to\n    :class:`WebSocketClientProtocol`.\n\n    The behavior of ``ping_interval``, ``ping_timeout``, ``close_timeout``,\n    ``max_size``, ``max_queue``, ``read_limit``, and ``write_limit`` is\n    described in :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    :func:`connect` also accepts the following optional arguments:\n\n    * ``compression`` is a shortcut to configure compression extensions;\n      by default it enables the "permessage-deflate" extension; set it to\n      ``None`` to disable compression\n    * ``origin`` sets the Origin HTTP header\n    * ``extensions`` is a list of supported extensions in order of\n      decreasing preference\n    * ``subprotocols`` is a list of supported subprotocols in order of\n      decreasing preference\n    * ``extra_headers`` sets additional HTTP request headers; it can be a\n      :class:`~websockets.http.Headers` instance, a\n      :class:`~collections.abc.Mapping`, or an iterable of ``(name, value)``\n      pairs\n\n    :raises ~websockets.uri.InvalidURI: if ``uri`` is invalid\n    :raises ~websockets.handshake.InvalidHandshake: if the opening handshake\n        fails\n\n    '
    MAX_REDIRECTS_ALLOWED = 10

    def __init__(self, uri: str, *, path: Optional[str]=None, create_protocol: Optional[Type[WebSocketClientProtocol]]=None, ping_interval: float=20, ping_timeout: float=20, close_timeout: Optional[float]=None, max_size: int=1048576, max_queue: int=32, read_limit: int=65536, write_limit: int=65536, loop: Optional[asyncio.AbstractEventLoop]=None, legacy_recv: bool=False, klass: Optional[Type[WebSocketClientProtocol]]=None, timeout: Optional[float]=None, compression: Optional[str]='deflate', origin: Optional[Origin]=None, extensions: Optional[Sequence[ClientExtensionFactory]]=None, subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLike]=None, **kwargs: Any) -> None:
        if timeout is None:
            timeout = 10
        else:
            warnings.warn'rename timeout to close_timeout'DeprecationWarning
        if close_timeout is None:
            close_timeout = timeout
        else:
            if klass is None:
                klass = WebSocketClientProtocol
            else:
                warnings.warn'rename klass to create_protocol'DeprecationWarning
            if create_protocol is None:
                create_protocol = klass
            if loop is None:
                loop = asyncio.get_event_loop()
            wsuri = parse_uri(uri)
            if wsuri.secure:
                kwargs.setdefault'ssl'True
            else:
                if kwargs.get('ssl') is not None:
                    raise ValueError('connect() received a ssl argument for a ws:// URI, use a wss:// URI to enable TLS')
        if compression == 'deflate':
            if extensions is None:
                extensions = []
            extensions = any((extension_factory.name == ClientPerMessageDeflateFactory.name for extension_factory in extensions)) or list(extensions) + [
             ClientPerMessageDeflateFactory(client_max_window_bits=True)]
        else:
            if compression is not None:
                raise ValueError(f"unsupported compression: {compression}")
            else:
                factory = functools.partial(create_protocol,
                  ping_interval=ping_interval,
                  ping_timeout=ping_timeout,
                  close_timeout=close_timeout,
                  max_size=max_size,
                  max_queue=max_queue,
                  read_limit=read_limit,
                  write_limit=write_limit,
                  loop=loop,
                  host=(wsuri.host),
                  port=(wsuri.port),
                  secure=(wsuri.secure),
                  legacy_recv=legacy_recv,
                  origin=origin,
                  extensions=extensions,
                  subprotocols=subprotocols,
                  extra_headers=extra_headers)
                if path is None:
                    if kwargs.get('sock') is None:
                        host, port = wsuri.host, wsuri.port
                    else:
                        host, port = (None, None)
                    host = kwargs.pop'host'host
                    port = kwargs.pop'port'port
                    create_connection = (functools.partial)(
                     (loop.create_connection), factory, host, port, **kwargs)
                else:
                    create_connection = (functools.partial)(
                     (loop.create_unix_connection), factory, path, **kwargs)
            self._create_connection = create_connection
            self._wsuri = wsuri

    def handle_redirect(self, uri: str) -> None:
        old_wsuri = self._wsuri
        new_wsuri = parse_uri(uri)
        if old_wsuri.secure:
            if not new_wsuri.secure:
                raise SecurityError('redirect from WSS to WS')
        same_origin = old_wsuri.host == new_wsuri.host and old_wsuri.port == new_wsuri.port
        if not same_origin:
            factory = self._create_connection.args[0]
            factory = (functools.partial)(
 factory.func, *(factory.args), **dict((factory.keywords), host=(new_wsuri.host), port=(new_wsuri.port)))
            self._create_connection = (functools.partial)(
 self._create_connection.func, *(
             factory, new_wsuri.host, new_wsuri.port), **(self._create_connection).keywords)
        self._wsuri = new_wsuri

    async def __aenter__(self) -> WebSocketClientProtocol:
        return await self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        await self.ws_client.close()

    def __await__(self) -> Generator[(Any, None, WebSocketClientProtocol)]:
        return self.__await_impl__().__await__()

    async def __await_impl__--- This code section failed: ---

 L. 534         0  LOAD_GLOBAL              range
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                MAX_REDIRECTS_ALLOWED
                6  CALL_FUNCTION_1       1  ''
                8  GET_ITER         
               10  FOR_ITER            210  'to 210'
               12  STORE_FAST               'redirects'

 L. 535        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _create_connection
               18  CALL_METHOD_0         0  ''
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'transport'
               30  STORE_FAST               'protocol'

 L. 537        32  LOAD_GLOBAL              cast
               34  LOAD_GLOBAL              asyncio
               36  LOAD_ATTR                Transport
               38  LOAD_FAST                'transport'
               40  CALL_FUNCTION_2       2  ''
               42  STORE_FAST               'transport'

 L. 538        44  LOAD_GLOBAL              cast
               46  LOAD_GLOBAL              WebSocketClientProtocol
               48  LOAD_FAST                'protocol'
               50  CALL_FUNCTION_2       2  ''
               52  STORE_FAST               'protocol'

 L. 540        54  SETUP_FINALLY       162  'to 162'

 L. 541        56  SETUP_FINALLY        98  'to 98'

 L. 542        58  LOAD_FAST                'protocol'
               60  LOAD_ATTR                handshake

 L. 543        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _wsuri

 L. 544        66  LOAD_FAST                'protocol'
               68  LOAD_ATTR                origin

 L. 545        70  LOAD_FAST                'protocol'
               72  LOAD_ATTR                available_extensions

 L. 546        74  LOAD_FAST                'protocol'
               76  LOAD_ATTR                available_subprotocols

 L. 547        78  LOAD_FAST                'protocol'
               80  LOAD_ATTR                extra_headers

 L. 542        82  LOAD_CONST               ('origin', 'available_extensions', 'available_subprotocols', 'extra_headers')
               84  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  POP_TOP          
               94  POP_BLOCK        
               96  JUMP_FORWARD        142  'to 142'
             98_0  COME_FROM_FINALLY    56  '56'

 L. 549        98  DUP_TOP          
              100  LOAD_GLOBAL              Exception
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   140  'to 140'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 550       112  LOAD_FAST                'protocol'
              114  LOAD_METHOD              fail_connection
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          

 L. 551       120  LOAD_FAST                'protocol'
              122  LOAD_METHOD              wait_closed
              124  CALL_METHOD_0         0  ''
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  POP_TOP          

 L. 552       134  RAISE_VARARGS_0       0  'reraise'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        158  'to 158'
            140_0  COME_FROM           104  '104'
              140  END_FINALLY      
            142_0  COME_FROM            96  '96'

 L. 554       142  LOAD_FAST                'protocol'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               ws_client

 L. 555       148  LOAD_FAST                'protocol'
              150  POP_BLOCK        
              152  ROT_TWO          
              154  POP_TOP          
              156  RETURN_VALUE     
            158_0  COME_FROM           138  '138'
              158  POP_BLOCK        
              160  JUMP_BACK            10  'to 10'
            162_0  COME_FROM_FINALLY    54  '54'

 L. 556       162  DUP_TOP          
              164  LOAD_GLOBAL              RedirectHandshake
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   206  'to 206'
              170  POP_TOP          
              172  STORE_FAST               'exc'
              174  POP_TOP          
              176  SETUP_FINALLY       194  'to 194'

 L. 557       178  LOAD_FAST                'self'
              180  LOAD_METHOD              handle_redirect
              182  LOAD_FAST                'exc'
              184  LOAD_ATTR                uri
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  BEGIN_FINALLY    
            194_0  COME_FROM_FINALLY   176  '176'
              194  LOAD_CONST               None
              196  STORE_FAST               'exc'
              198  DELETE_FAST              'exc'
              200  END_FINALLY      
              202  POP_EXCEPT       
              204  JUMP_BACK            10  'to 10'
            206_0  COME_FROM           168  '168'
              206  END_FINALLY      
              208  JUMP_BACK            10  'to 10'

 L. 559       210  LOAD_GLOBAL              SecurityError
              212  LOAD_STR                 'too many redirects'
              214  CALL_FUNCTION_1       1  ''
              216  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 152

    __iter__ = __await__


connect = Connect

def unix_connect(path: str, uri: str='ws://localhost/', **kwargs: Any) -> Connect:
    """
    Similar to :func:`connect`, but for connecting to a Unix socket.

    This function calls the event loop's
    :meth:`~asyncio.loop.create_unix_connection` method.

    It is only available on Unix.

    It's mainly useful for debugging servers listening on Unix sockets.

    :param path: file system path to the Unix socket
    :param uri: WebSocket URI

    """
    return connect(uri=uri, path=path, **kwargs)