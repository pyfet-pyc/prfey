# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\server.py
"""
:mod:`websockets.server` defines the WebSocket server APIs.

"""
import asyncio, collections.abc, email.utils, functools, http, logging, socket, sys, warnings
from types import TracebackType
from typing import Any, Awaitable, Callable, Generator, List, Optional, Sequence, Set, Tuple, Type, Union, cast
from .exceptions import AbortHandshake, InvalidHandshake, InvalidHeader, InvalidMessage, InvalidOrigin, InvalidUpgrade, NegotiationError
from extensions.base import Extension, ServerExtensionFactory
from extensions.permessage_deflate import ServerPerMessageDeflateFactory
from .handshake import build_response, check_request
from .headers import build_extension, parse_extension, parse_subprotocol
from .http import USER_AGENT, Headers, HeadersLike, MultipleValuesError, read_request
from .protocol import WebSocketCommonProtocol
from .typing import ExtensionHeader, Origin, Subprotocol
__all__ = [
 'serve', 'unix_serve', 'WebSocketServerProtocol', 'WebSocketServer']
logger = logging.getLogger(__name__)
HeadersLikeOrCallable = Union[(HeadersLike, Callable[([str, Headers], HeadersLike)])]
HTTPResponse = Tuple[(http.HTTPStatus, HeadersLike, bytes)]

class WebSocketServerProtocol(WebSocketCommonProtocol):
    __doc__ = "\n    :class:`~asyncio.Protocol` subclass implementing a WebSocket server.\n\n    This class inherits most of its methods from\n    :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    For the sake of simplicity, it doesn't rely on a full HTTP implementation.\n    Its support for HTTP responses is very limited.\n\n    "
    is_client = False
    side = 'server'

    def __init__(self, ws_handler, ws_server, *, origins=None, extensions=None, subprotocols=None, extra_headers=None, process_request=None, select_subprotocol=None, **kwargs):
        if origins is not None:
            if '' in origins:
                warnings.warn("use None instead of '' in origins", DeprecationWarning)
                origins = [None if origin == '' else origin for origin in origins]
        self.ws_handler = ws_handler
        self.ws_server = ws_server
        self.origins = origins
        self.available_extensions = extensions
        self.available_subprotocols = subprotocols
        self.extra_headers = extra_headers
        self._process_request = process_request
        self._select_subprotocol = select_subprotocol
        (super().__init__)(**kwargs)

    def connection_made(self, transport):
        """
        Register connection and initialize a task to handle it.

        """
        super().connection_made(transport)
        self.ws_server.register(self)
        self.handler_task = self.loop.create_task(self.handler())

    async def handler--- This code section failed: ---

 L. 127       0_2  SETUP_FINALLY       750  'to 750'
              4_6  SETUP_FINALLY       686  'to 686'

 L. 129         8  SETUP_FINALLY        48  'to 48'

 L. 130        10  LOAD_FAST                'self'
               12  LOAD_ATTR                handshake

 L. 131        14  LOAD_FAST                'self'
               16  LOAD_ATTR                origins

 L. 132        18  LOAD_FAST                'self'
               20  LOAD_ATTR                available_extensions

 L. 133        22  LOAD_FAST                'self'
               24  LOAD_ATTR                available_subprotocols

 L. 134        26  LOAD_FAST                'self'
               28  LOAD_ATTR                extra_headers

 L. 130        30  LOAD_CONST               ('origins', 'available_extensions', 'available_subprotocols', 'extra_headers')
               32  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  STORE_FAST               'path'
               42  POP_BLOCK        
            44_46  JUMP_FORWARD        508  'to 508'
             48_0  COME_FROM_FINALLY     8  '8'

 L. 136        48  DUP_TOP          
               50  LOAD_GLOBAL              ConnectionError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    84  'to 84'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 137        62  LOAD_GLOBAL              logger
               64  LOAD_ATTR                debug
               66  LOAD_STR                 'Connection error in opening handshake'
               68  LOAD_CONST               True
               70  LOAD_CONST               ('exc_info',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  POP_TOP          

 L. 138        76  RAISE_VARARGS_0       0  'reraise'
               78  POP_EXCEPT       
            80_82  JUMP_FORWARD        508  'to 508'
             84_0  COME_FROM            54  '54'

 L. 139        84  DUP_TOP          
               86  LOAD_GLOBAL              Exception
               88  COMPARE_OP               exception-match
            90_92  POP_JUMP_IF_FALSE   506  'to 506'
               94  POP_TOP          
               96  STORE_FAST               'exc'
               98  POP_TOP          
          100_102  SETUP_FINALLY       494  'to 494'

 L. 140       104  LOAD_GLOBAL              isinstance
              106  LOAD_FAST                'exc'
              108  LOAD_GLOBAL              AbortHandshake
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   138  'to 138'

 L. 141       114  LOAD_FAST                'exc'
              116  LOAD_ATTR                status
              118  LOAD_FAST                'exc'
              120  LOAD_ATTR                headers
              122  LOAD_FAST                'exc'
              124  LOAD_ATTR                body
              126  ROT_THREE        
              128  ROT_TWO          
              130  STORE_FAST               'status'
              132  STORE_FAST               'headers'
              134  STORE_FAST               'body'
              136  JUMP_FORWARD        362  'to 362'
            138_0  COME_FROM           112  '112'

 L. 142       138  LOAD_GLOBAL              isinstance
              140  LOAD_FAST                'exc'
              142  LOAD_GLOBAL              InvalidOrigin
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   198  'to 198'

 L. 143       148  LOAD_GLOBAL              logger
              150  LOAD_ATTR                debug
              152  LOAD_STR                 'Invalid origin'
              154  LOAD_CONST               True
              156  LOAD_CONST               ('exc_info',)
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  POP_TOP          

 L. 145       162  LOAD_GLOBAL              http
              164  LOAD_ATTR                HTTPStatus
              166  LOAD_ATTR                FORBIDDEN

 L. 146       168  LOAD_GLOBAL              Headers
              170  CALL_FUNCTION_0       0  ''

 L. 147       172  LOAD_STR                 'Failed to open a WebSocket connection: '
              174  LOAD_FAST                'exc'
              176  FORMAT_VALUE          0  ''
              178  LOAD_STR                 '.\n'
              180  BUILD_STRING_3        3 
              182  LOAD_METHOD              encode
              184  CALL_METHOD_0         0  ''

 L. 144       186  ROT_THREE        
              188  ROT_TWO          
              190  STORE_FAST               'status'
              192  STORE_FAST               'headers'
              194  STORE_FAST               'body'
              196  JUMP_FORWARD        362  'to 362'
            198_0  COME_FROM           146  '146'

 L. 149       198  LOAD_GLOBAL              isinstance
              200  LOAD_FAST                'exc'
              202  LOAD_GLOBAL              InvalidUpgrade
              204  CALL_FUNCTION_2       2  ''
          206_208  POP_JUMP_IF_FALSE   264  'to 264'

 L. 150       210  LOAD_GLOBAL              logger
              212  LOAD_ATTR                debug
              214  LOAD_STR                 'Invalid upgrade'
              216  LOAD_CONST               True
              218  LOAD_CONST               ('exc_info',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  POP_TOP          

 L. 152       224  LOAD_GLOBAL              http
              226  LOAD_ATTR                HTTPStatus
              228  LOAD_ATTR                UPGRADE_REQUIRED

 L. 153       230  LOAD_GLOBAL              Headers
              232  LOAD_CONST               ('Upgrade', 'websocket')
              234  BUILD_LIST_1          1 
              236  CALL_FUNCTION_1       1  ''

 L. 155       238  LOAD_STR                 'Failed to open a WebSocket connection: '
              240  LOAD_FAST                'exc'
              242  FORMAT_VALUE          0  ''
              244  LOAD_STR                 '.\n\nYou cannot access a WebSocket server directly with a browser. You need a WebSocket client.\n'
              246  BUILD_STRING_3        3 

 L. 154       248  LOAD_METHOD              encode
              250  CALL_METHOD_0         0  ''

 L. 151       252  ROT_THREE        
              254  ROT_TWO          
              256  STORE_FAST               'status'
              258  STORE_FAST               'headers'
              260  STORE_FAST               'body'
              262  JUMP_FORWARD        362  'to 362'
            264_0  COME_FROM           206  '206'

 L. 161       264  LOAD_GLOBAL              isinstance
              266  LOAD_FAST                'exc'
              268  LOAD_GLOBAL              InvalidHandshake
              270  CALL_FUNCTION_2       2  ''
          272_274  POP_JUMP_IF_FALSE   326  'to 326'

 L. 162       276  LOAD_GLOBAL              logger
              278  LOAD_ATTR                debug
              280  LOAD_STR                 'Invalid handshake'
              282  LOAD_CONST               True
              284  LOAD_CONST               ('exc_info',)
              286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              288  POP_TOP          

 L. 164       290  LOAD_GLOBAL              http
              292  LOAD_ATTR                HTTPStatus
              294  LOAD_ATTR                BAD_REQUEST

 L. 165       296  LOAD_GLOBAL              Headers
              298  CALL_FUNCTION_0       0  ''

 L. 166       300  LOAD_STR                 'Failed to open a WebSocket connection: '
              302  LOAD_FAST                'exc'
              304  FORMAT_VALUE          0  ''
              306  LOAD_STR                 '.\n'
              308  BUILD_STRING_3        3 
              310  LOAD_METHOD              encode
              312  CALL_METHOD_0         0  ''

 L. 163       314  ROT_THREE        
              316  ROT_TWO          
              318  STORE_FAST               'status'
              320  STORE_FAST               'headers'
              322  STORE_FAST               'body'
              324  JUMP_FORWARD        362  'to 362'
            326_0  COME_FROM           272  '272'

 L. 169       326  LOAD_GLOBAL              logger
              328  LOAD_ATTR                warning
              330  LOAD_STR                 'Error in opening handshake'
              332  LOAD_CONST               True
              334  LOAD_CONST               ('exc_info',)
              336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              338  POP_TOP          

 L. 171       340  LOAD_GLOBAL              http
              342  LOAD_ATTR                HTTPStatus
              344  LOAD_ATTR                INTERNAL_SERVER_ERROR

 L. 172       346  LOAD_GLOBAL              Headers
              348  CALL_FUNCTION_0       0  ''

 L. 174       350  LOAD_CONST               b'Failed to open a WebSocket connection.\nSee server log for more information.\n'

 L. 170       352  ROT_THREE        
              354  ROT_TWO          
              356  STORE_FAST               'status'
              358  STORE_FAST               'headers'
              360  STORE_FAST               'body'
            362_0  COME_FROM           324  '324'
            362_1  COME_FROM           262  '262'
            362_2  COME_FROM           196  '196'
            362_3  COME_FROM           136  '136'

 L. 179       362  LOAD_FAST                'headers'
              364  LOAD_METHOD              setdefault
              366  LOAD_STR                 'Date'
              368  LOAD_GLOBAL              email
              370  LOAD_ATTR                utils
              372  LOAD_ATTR                formatdate
              374  LOAD_CONST               True
              376  LOAD_CONST               ('usegmt',)
              378  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              380  CALL_METHOD_2         2  ''
              382  POP_TOP          

 L. 180       384  LOAD_FAST                'headers'
              386  LOAD_METHOD              setdefault
              388  LOAD_STR                 'Server'
              390  LOAD_GLOBAL              USER_AGENT
              392  CALL_METHOD_2         2  ''
              394  POP_TOP          

 L. 181       396  LOAD_FAST                'headers'
              398  LOAD_METHOD              setdefault
              400  LOAD_STR                 'Content-Length'
              402  LOAD_GLOBAL              str
              404  LOAD_GLOBAL              len
              406  LOAD_FAST                'body'
              408  CALL_FUNCTION_1       1  ''
              410  CALL_FUNCTION_1       1  ''
              412  CALL_METHOD_2         2  ''
              414  POP_TOP          

 L. 182       416  LOAD_FAST                'headers'
              418  LOAD_METHOD              setdefault
              420  LOAD_STR                 'Content-Type'
              422  LOAD_STR                 'text/plain'
              424  CALL_METHOD_2         2  ''
              426  POP_TOP          

 L. 183       428  LOAD_FAST                'headers'
              430  LOAD_METHOD              setdefault
              432  LOAD_STR                 'Connection'
              434  LOAD_STR                 'close'
              436  CALL_METHOD_2         2  ''
              438  POP_TOP          

 L. 185       440  LOAD_FAST                'self'
              442  LOAD_METHOD              write_http_response
              444  LOAD_FAST                'status'
              446  LOAD_FAST                'headers'
              448  LOAD_FAST                'body'
              450  CALL_METHOD_3         3  ''
              452  POP_TOP          

 L. 186       454  LOAD_FAST                'self'
              456  LOAD_METHOD              fail_connection
              458  CALL_METHOD_0         0  ''
              460  POP_TOP          

 L. 187       462  LOAD_FAST                'self'
              464  LOAD_METHOD              wait_closed
              466  CALL_METHOD_0         0  ''
              468  GET_AWAITABLE    
              470  LOAD_CONST               None
              472  YIELD_FROM       
              474  POP_TOP          

 L. 188       476  POP_BLOCK        
              478  POP_EXCEPT       
              480  CALL_FINALLY        494  'to 494'
              482  POP_BLOCK        
              484  POP_BLOCK        
          486_488  CALL_FINALLY        750  'to 750'
              490  LOAD_CONST               None
              492  RETURN_VALUE     
            494_0  COME_FROM           480  '480'
            494_1  COME_FROM_FINALLY   100  '100'
              494  LOAD_CONST               None
              496  STORE_FAST               'exc'
              498  DELETE_FAST              'exc'
              500  END_FINALLY      
              502  POP_EXCEPT       
              504  JUMP_FORWARD        508  'to 508'
            506_0  COME_FROM            90  '90'
              506  END_FINALLY      
            508_0  COME_FROM           504  '504'
            508_1  COME_FROM            80  '80'
            508_2  COME_FROM            44  '44'

 L. 190       508  SETUP_FINALLY       532  'to 532'

 L. 191       510  LOAD_FAST                'self'
              512  LOAD_METHOD              ws_handler
              514  LOAD_FAST                'self'
              516  LOAD_FAST                'path'
              518  CALL_METHOD_2         2  ''
              520  GET_AWAITABLE    
              522  LOAD_CONST               None
              524  YIELD_FROM       
              526  POP_TOP          
              528  POP_BLOCK        
              530  JUMP_FORWARD        588  'to 588'
            532_0  COME_FROM_FINALLY   508  '508'

 L. 192       532  DUP_TOP          
              534  LOAD_GLOBAL              Exception
              536  COMPARE_OP               exception-match
          538_540  POP_JUMP_IF_FALSE   586  'to 586'
              542  POP_TOP          
              544  POP_TOP          
              546  POP_TOP          

 L. 193       548  LOAD_GLOBAL              logger
              550  LOAD_ATTR                error
              552  LOAD_STR                 'Error in connection handler'
              554  LOAD_CONST               True
              556  LOAD_CONST               ('exc_info',)
              558  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              560  POP_TOP          

 L. 194       562  LOAD_FAST                'self'
              564  LOAD_ATTR                closed
          566_568  POP_JUMP_IF_TRUE    580  'to 580'

 L. 195       570  LOAD_FAST                'self'
              572  LOAD_METHOD              fail_connection
              574  LOAD_CONST               1011
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
            580_0  COME_FROM           566  '566'

 L. 196       580  RAISE_VARARGS_0       0  'reraise'
              582  POP_EXCEPT       
              584  JUMP_FORWARD        588  'to 588'
            586_0  COME_FROM           538  '538'
              586  END_FINALLY      
            588_0  COME_FROM           584  '584'
            588_1  COME_FROM           530  '530'

 L. 198       588  SETUP_FINALLY       608  'to 608'

 L. 199       590  LOAD_FAST                'self'
              592  LOAD_METHOD              close
              594  CALL_METHOD_0         0  ''
              596  GET_AWAITABLE    
              598  LOAD_CONST               None
              600  YIELD_FROM       
              602  POP_TOP          
              604  POP_BLOCK        
              606  JUMP_FORWARD        682  'to 682'
            608_0  COME_FROM_FINALLY   588  '588'

 L. 200       608  DUP_TOP          
              610  LOAD_GLOBAL              ConnectionError
              612  COMPARE_OP               exception-match
          614_616  POP_JUMP_IF_FALSE   644  'to 644'
              618  POP_TOP          
              620  POP_TOP          
              622  POP_TOP          

 L. 201       624  LOAD_GLOBAL              logger
              626  LOAD_ATTR                debug
              628  LOAD_STR                 'Connection error in closing handshake'
              630  LOAD_CONST               True
              632  LOAD_CONST               ('exc_info',)
              634  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              636  POP_TOP          

 L. 202       638  RAISE_VARARGS_0       0  'reraise'
              640  POP_EXCEPT       
              642  JUMP_FORWARD        682  'to 682'
            644_0  COME_FROM           614  '614'

 L. 203       644  DUP_TOP          
              646  LOAD_GLOBAL              Exception
              648  COMPARE_OP               exception-match
          650_652  POP_JUMP_IF_FALSE   680  'to 680'
              654  POP_TOP          
              656  POP_TOP          
              658  POP_TOP          

 L. 204       660  LOAD_GLOBAL              logger
              662  LOAD_ATTR                warning
              664  LOAD_STR                 'Error in closing handshake'
              666  LOAD_CONST               True
              668  LOAD_CONST               ('exc_info',)
              670  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              672  POP_TOP          

 L. 205       674  RAISE_VARARGS_0       0  'reraise'
              676  POP_EXCEPT       
              678  JUMP_FORWARD        682  'to 682'
            680_0  COME_FROM           650  '650'
              680  END_FINALLY      
            682_0  COME_FROM           678  '678'
            682_1  COME_FROM           642  '642'
            682_2  COME_FROM           606  '606'
              682  POP_BLOCK        
              684  JUMP_FORWARD        746  'to 746'
            686_0  COME_FROM_FINALLY     4  '4'

 L. 207       686  DUP_TOP          
              688  LOAD_GLOBAL              Exception
              690  COMPARE_OP               exception-match
          692_694  POP_JUMP_IF_FALSE   744  'to 744'
              696  POP_TOP          
              698  POP_TOP          
              700  POP_TOP          

 L. 209       702  SETUP_FINALLY       718  'to 718'

 L. 210       704  LOAD_FAST                'self'
              706  LOAD_ATTR                transport
              708  LOAD_METHOD              close
              710  CALL_METHOD_0         0  ''
              712  POP_TOP          
              714  POP_BLOCK        
              716  JUMP_FORWARD        740  'to 740'
            718_0  COME_FROM_FINALLY   702  '702'

 L. 211       718  DUP_TOP          
              720  LOAD_GLOBAL              Exception
              722  COMPARE_OP               exception-match
          724_726  POP_JUMP_IF_FALSE   738  'to 738'
              728  POP_TOP          
              730  POP_TOP          
              732  POP_TOP          

 L. 212       734  POP_EXCEPT       
              736  JUMP_FORWARD        740  'to 740'
            738_0  COME_FROM           724  '724'
              738  END_FINALLY      
            740_0  COME_FROM           736  '736'
            740_1  COME_FROM           716  '716'
              740  POP_EXCEPT       
              742  JUMP_FORWARD        746  'to 746'
            744_0  COME_FROM           692  '692'
              744  END_FINALLY      
            746_0  COME_FROM           742  '742'
            746_1  COME_FROM           684  '684'
              746  POP_BLOCK        
              748  BEGIN_FINALLY    
            750_0  COME_FROM           486  '486'
            750_1  COME_FROM_FINALLY     0  '0'

 L. 219       750  LOAD_FAST                'self'
              752  LOAD_ATTR                ws_server
              754  LOAD_METHOD              unregister
              756  LOAD_FAST                'self'
              758  CALL_METHOD_1         1  ''
              760  POP_TOP          
              762  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 480

    async def read_http_request(self) -> Tuple[(str, Headers)]:
        """
        Read request line and headers from the HTTP request.

        If the request contains a body, it may be read from ``self.reader``
        after this coroutine returns.

        :raises ~websockets.exceptions.InvalidMessage: if the HTTP message is
            malformed or isn't an HTTP/1.1 GET request

        """
        try:
            path, headers = await read_request(self.reader)
        except Exception as exc:
            try:
                raise InvalidMessage('did not receive a valid HTTP request') from exc
            finally:
                exc = None
                del exc

        else:
            logger.debug'%s < GET %s HTTP/1.1'self.sidepath
            logger.debug'%s < %r'self.sideheaders
            self.path = path
            self.request_headers = headers
            return (
             path, headers)

    def write_http_response(self, status: http.HTTPStatus, headers: Headers, body: Optional[bytes]=None) -> None:
        """
        Write status line and headers to the HTTP response.

        This coroutine is also able to write a response body.

        """
        self.response_headers = headers
        logger.debug('%s > HTTP/1.1 %d %s', self.side, status.value, status.phrase)
        logger.debug'%s > %r'self.sideheaders
        response = f"HTTP/1.1 {status.value} {status.phrase}\r\n"
        response += str(headers)
        self.transport.write(response.encode())
        if body is not None:
            logger.debug'%s > body (%d bytes)'self.sidelen(body)
            self.transport.write(body)

    async def process_request(self, path: str, request_headers: Headers) -> Optional[HTTPResponse]:
        """
        Intercept the HTTP request and return an HTTP response if appropriate.

        If ``process_request`` returns ``None``, the WebSocket handshake
        continues. If it returns 3-uple containing a status code, response
        headers and a response body, that HTTP response is sent and the
        connection is closed. In that case:

        * The HTTP status must be a :class:`~http.HTTPStatus`.
        * HTTP headers must be a :class:`~websockets.http.Headers` instance, a
          :class:`~collections.abc.Mapping`, or an iterable of ``(name,
          value)`` pairs.
        * The HTTP response body must be :class:`bytes`. It may be empty.

        This coroutine may be overridden in a :class:`WebSocketServerProtocol`
        subclass, for example:

        * to return a HTTP 200 OK response on a given path; then a load
          balancer can use this path for a health check;
        * to authenticate the request and return a HTTP 401 Unauthorized or a
          HTTP 403 Forbidden when authentication fails.

        Instead of subclassing, it is possible to override this method by
        passing a ``process_request`` argument to the :func:`serve` function
        or the :class:`WebSocketServerProtocol` constructor. This is
        equivalent, except ``process_request`` won't have access to the
        protocol instance, so it can't store information for later use.

        ``process_request`` is expected to complete quickly. If it may run for
        a long time, then it should await :meth:`wait_closed` and exit if
        :meth:`wait_closed` completes, or else it could prevent the server
        from shutting down.

        :param path: request path, including optional query string
        :param request_headers: request headers

        """
        if self._process_request is not None:
            response = self._process_request(path, request_headers)
            if isinstance(response, Awaitable):
                return await response
            warnings.warn('declare process_request as a coroutine', DeprecationWarning)
            return response

    @staticmethod
    def process_origin(headers: Headers, origins: Optional[Sequence[Optional[Origin]]]=None) -> Optional[Origin]:
        """
        Handle the Origin HTTP request header.

        :param headers: request headers
        :param origins: optional list of acceptable origins
        :raises ~websockets.exceptions.InvalidOrigin: if the origin isn't
            acceptable

        """
        try:
            origin = cast(Origin, headers.get('Origin'))
        except MultipleValuesError:
            raise InvalidHeader('Origin', 'more than one Origin header found')
        else:
            if origins is not None:
                if origin not in origins:
                    raise InvalidOrigin(origin)
            return origin

    @staticmethod
    def process_extensions--- This code section failed: ---

 L. 384         0  LOAD_CONST               None
                2  STORE_FAST               'response_header_value'

 L. 386         4  BUILD_LIST_0          0 
                6  STORE_FAST               'extension_headers'

 L. 387         8  BUILD_LIST_0          0 
               10  STORE_FAST               'accepted_extensions'

 L. 389        12  LOAD_FAST                'headers'
               14  LOAD_METHOD              get_all
               16  LOAD_STR                 'Sec-WebSocket-Extensions'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'header_values'

 L. 391        22  LOAD_FAST                'header_values'
               24  POP_JUMP_IF_FALSE   160  'to 160'
               26  LOAD_FAST                'available_extensions'
               28  POP_JUMP_IF_FALSE   160  'to 160'

 L. 393        30  LOAD_GLOBAL              sum

 L. 394        32  LOAD_LISTCOMP            '<code_object <listcomp>>'
               34  LOAD_STR                 'WebSocketServerProtocol.process_extensions.<locals>.<listcomp>'
               36  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               38  LOAD_FAST                'header_values'
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''

 L. 394        44  BUILD_LIST_0          0 

 L. 393        46  CALL_FUNCTION_2       2  ''
               48  STORE_FAST               'parsed_header_values'

 L. 397        50  LOAD_FAST                'parsed_header_values'
               52  GET_ITER         
               54  FOR_ITER            160  'to 160'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'name'
               60  STORE_FAST               'request_params'

 L. 399        62  LOAD_FAST                'available_extensions'
               64  GET_ITER         
               66  FOR_ITER            158  'to 158'
               68  STORE_FAST               'ext_factory'

 L. 402        70  LOAD_FAST                'ext_factory'
               72  LOAD_ATTR                name
               74  LOAD_FAST                'name'
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_FALSE    82  'to 82'

 L. 403        80  JUMP_BACK            66  'to 66'
             82_0  COME_FROM            78  '78'

 L. 406        82  SETUP_FINALLY       104  'to 104'

 L. 407        84  LOAD_FAST                'ext_factory'
               86  LOAD_METHOD              process_request_params

 L. 408        88  LOAD_FAST                'request_params'

 L. 408        90  LOAD_FAST                'accepted_extensions'

 L. 407        92  CALL_METHOD_2         2  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'response_params'
               98  STORE_FAST               'extension'
              100  POP_BLOCK        
              102  JUMP_FORWARD        128  'to 128'
            104_0  COME_FROM_FINALLY    82  '82'

 L. 410       104  DUP_TOP          
              106  LOAD_GLOBAL              NegotiationError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   126  'to 126'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 411       118  POP_EXCEPT       
              120  JUMP_BACK            66  'to 66'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           110  '110'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM           102  '102'

 L. 414       128  LOAD_FAST                'extension_headers'
              130  LOAD_METHOD              append
              132  LOAD_FAST                'name'
              134  LOAD_FAST                'response_params'
              136  BUILD_TUPLE_2         2 
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 415       142  LOAD_FAST                'accepted_extensions'
              144  LOAD_METHOD              append
              146  LOAD_FAST                'extension'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L. 418       152  POP_TOP          
              154  CONTINUE             54  'to 54'
              156  JUMP_BACK            66  'to 66'
              158  JUMP_BACK            54  'to 54'
            160_0  COME_FROM            28  '28'
            160_1  COME_FROM            24  '24'

 L. 424       160  LOAD_FAST                'extension_headers'
              162  POP_JUMP_IF_FALSE   172  'to 172'

 L. 425       164  LOAD_GLOBAL              build_extension
              166  LOAD_FAST                'extension_headers'
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'response_header_value'
            172_0  COME_FROM           162  '162'

 L. 427       172  LOAD_FAST                'response_header_value'
              174  LOAD_FAST                'accepted_extensions'
              176  BUILD_TUPLE_2         2 
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 122

    def process_subprotocol(self, headers: Headers, available_subprotocols: Optional[Sequence[Subprotocol]]) -> Optional[Subprotocol]:
        """
        Handle the Sec-WebSocket-Protocol HTTP request header.

        Return Sec-WebSocket-Protocol HTTP response header, which is the same
        as the selected subprotocol.

        :param headers: request headers
        :param available_subprotocols: optional list of supported subprotocols
        :raises ~websockets.exceptions.InvalidHandshake: to abort the
            handshake with an HTTP 400 error code

        """
        subprotocol = None
        header_values = headers.get_all('Sec-WebSocket-Protocol')
        if header_values:
            if available_subprotocols:
                parsed_header_values = sum([parse_subprotocol(header_value) for header_value in header_values], [])
                subprotocol = self.select_subprotocol(parsed_header_values, available_subprotocols)
        return subprotocol

    def select_subprotocol(self, client_subprotocols: Sequence[Subprotocol], server_subprotocols: Sequence[Subprotocol]) -> Optional[Subprotocol]:
        """
        Pick a subprotocol among those offered by the client.

        If several subprotocols are supported by the client and the server,
        the default implementation selects the preferred subprotocols by
        giving equal value to the priorities of the client and the server.

        If no subprotocol is supported by the client and the server, it
        proceeds without a subprotocol.

        This is unlikely to be the most useful implementation in practice, as
        many servers providing a subprotocol will require that the client uses
        that subprotocol. Such rules can be implemented in a subclass.

        Instead of subclassing, it is possible to override this method by
        passing a ``select_subprotocol`` argument to the :func:`serve`
        function or the :class:`WebSocketServerProtocol` constructor

        :param client_subprotocols: list of subprotocols offered by the client
        :param server_subprotocols: list of subprotocols available on the server

        """
        if self._select_subprotocol is not None:
            return self._select_subprotocol(client_subprotocols, server_subprotocols)
        else:
            subprotocols = set(client_subprotocols) & set(server_subprotocols)
            return subprotocols or None
        priority = lambda p: client_subprotocols.index(p) + server_subprotocols.index(p)
        return sorted(subprotocols, key=priority)[0]

    async def handshake(self, origins: Optional[Sequence[Optional[Origin]]]=None, available_extensions: Optional[Sequence[ServerExtensionFactory]]=None, available_subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLikeOrCallable]=None) -> str:
        """
        Perform the server side of the opening handshake.

        Return the path of the URI of the request.

        :param origins: list of acceptable values of the Origin HTTP header;
            include ``None`` if the lack of an origin is acceptable
        :param available_extensions: list of supported extensions in the order
            in which they should be used
        :param available_subprotocols: list of supported subprotocols in order
            of decreasing preference
        :param extra_headers: sets additional HTTP response headers when the
            handshake succeeds; it can be a :class:`~websockets.http.Headers`
            instance, a :class:`~collections.abc.Mapping`, an iterable of
            ``(name, value)`` pairs, or a callable taking the request path and
            headers in arguments and returning one of the above.
        :raises ~websockets.exceptions.InvalidHandshake: if the handshake
            fails

        """
        path, request_headers = await self.read_http_request()
        early_response_awaitable = self.process_request(path, request_headers)
        if isinstance(early_response_awaitable, Awaitable):
            early_response = await early_response_awaitable
        else:
            warnings.warn('declare process_request as a coroutine', DeprecationWarning)
            early_response = early_response_awaitable
        if not self.ws_server.is_serving():
            early_response = (http.HTTPStatus.SERVICE_UNAVAILABLE, [],
             b'Server is shutting down.\n')
        if early_response is not None:
            raise AbortHandshake(*early_response)
        key = check_request(request_headers)
        self.origin = self.process_origin(request_headers, origins)
        extensions_header, self.extensions = self.process_extensions(request_headers, available_extensions)
        protocol_header = self.subprotocol = self.process_subprotocol(request_headers, available_subprotocols)
        response_headers = Headers()
        build_response(response_headers, key)
        if extensions_header is not None:
            response_headers['Sec-WebSocket-Extensions'] = extensions_header
        if protocol_header is not None:
            response_headers['Sec-WebSocket-Protocol'] = protocol_header
        if callable(extra_headers):
            extra_headers = extra_headers(path, self.request_headers)
        if extra_headers is not None:
            if isinstance(extra_headers, Headers):
                extra_headers = extra_headers.raw_items()
            else:
                if isinstance(extra_headers, collections.abc.Mapping):
                    extra_headers = extra_headers.items()
                for name, value in extra_headers:
                    response_headers[name] = value

        response_headers.setdefault('Date', email.utils.formatdate(usegmt=True))
        response_headers.setdefault('Server', USER_AGENT)
        self.write_http_response(http.HTTPStatus.SWITCHING_PROTOCOLS, response_headers)
        self.connection_open()
        return path


class WebSocketServer:
    __doc__ = "\n    WebSocket server returned by :func:`~websockets.server.serve`.\n\n    This class provides the same interface as\n    :class:`~asyncio.AbstractServer`, namely the\n    :meth:`~asyncio.AbstractServer.close` and\n    :meth:`~asyncio.AbstractServer.wait_closed` methods.\n\n    It keeps track of WebSocket connections in order to close them properly\n    when shutting down.\n\n    Instances of this class store a reference to the :class:`~asyncio.Server`\n    object returned by :meth:`~asyncio.loop.create_server` rather than inherit\n    from :class:`~asyncio.Server` in part because\n    :meth:`~asyncio.loop.create_server` doesn't support passing a custom\n    :class:`~asyncio.Server` class.\n\n    "

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.websockets = set()
        self.close_task = None
        self.closed_waiter = loop.create_future()

    def wrap(self, server: asyncio.AbstractServer) -> None:
        """
        Attach to a given :class:`~asyncio.Server`.

        Since :meth:`~asyncio.loop.create_server` doesn't support injecting a
        custom ``Server`` class, the easiest solution that doesn't rely on
        private :mod:`asyncio` APIs is to:

        - instantiate a :class:`WebSocketServer`
        - give the protocol factory a reference to that instance
        - call :meth:`~asyncio.loop.create_server` with the factory
        - attach the resulting :class:`~asyncio.Server` with this method

        """
        self.server = server

    def register(self, protocol: WebSocketServerProtocol) -> None:
        """
        Register a connection with this server.

        """
        self.websockets.add(protocol)

    def unregister(self, protocol: WebSocketServerProtocol) -> None:
        """
        Unregister a connection with this server.

        """
        self.websockets.remove(protocol)

    def is_serving--- This code section failed: ---

 L. 659         0  SETUP_FINALLY        14  'to 14'

 L. 661         2  LOAD_FAST                'self'
                4  LOAD_ATTR                server
                6  LOAD_METHOD              is_serving
                8  CALL_METHOD_0         0  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 662        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    44  'to 44'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 664        28  LOAD_FAST                'self'
               30  LOAD_ATTR                server
               32  LOAD_ATTR                sockets
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            20  '20'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24

    def close(self) -> None:
        """
        Close the server.

        This method:

        * closes the underlying :class:`~asyncio.Server`;
        * rejects new WebSocket connections with an HTTP 503 (service
          unavailable) error; this happens when the server accepted the TCP
          connection but didn't complete the WebSocket opening handshake prior
          to closing;
        * closes open WebSocket connections with close code 1001 (going away).

        :meth:`close` is idempotent.

        """
        if self.close_task is None:
            self.close_task = self.loop.create_task(self._close())

    async def _close(self) -> None:
        """
        Implementation of :meth:`close`.

        This calls :meth:`~asyncio.Server.close` on the underlying
        :class:`~asyncio.Server` object to stop accepting new connections and
        then closes open connections with close code 1001.

        """
        self.server.close()
        await self.server.wait_closed()
        await asyncio.sleep(0,
          loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        if self.websockets:
            await asyncio.wait([websocket.close(1001) for websocket in self.websockets],
              loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        if self.websockets:
            await asyncio.wait([websocket.handler_task for websocket in self.websockets],
              loop=(self.loop if sys.version_info[:2] < (3, 8) else None))
        self.closed_waiter.set_result(None)

    async def wait_closed(self) -> None:
        """
        Wait until the server is closed.

        When :meth:`wait_closed` returns, all TCP connections are closed and
        all connection handlers have returned.

        """
        await asyncio.shield(self.closed_waiter)

    @property
    def sockets(self) -> Optional[List[socket.socket]]:
        """
        List of :class:`~socket.socket` objects the server is listening to.

        ``None`` if the server is closed.

        """
        return self.server.sockets


class Serve:
    __doc__ = '\n\n    Create, start, and return a WebSocket server on ``host`` and ``port``.\n\n    Whenever a client connects, the server accepts the connection, creates a\n    :class:`WebSocketServerProtocol`, performs the opening handshake, and\n    delegates to the connection handler defined by ``ws_handler``. Once the\n    handler completes, either normally or with an exception, the server\n    performs the closing handshake and closes the connection.\n\n    Awaiting :func:`serve` yields a :class:`WebSocketServer`. This instance\n    provides :meth:`~websockets.server.WebSocketServer.close` and\n    :meth:`~websockets.server.WebSocketServer.wait_closed` methods for\n    terminating the server and cleaning up its resources.\n\n    When a server is closed with :meth:`~WebSocketServer.close`, it closes all\n    connections with close code 1001 (going away). Connections handlers, which\n    are running the ``ws_handler`` coroutine, will receive a\n    :exc:`~websockets.exceptions.ConnectionClosedOK` exception on their\n    current or next interaction with the WebSocket connection.\n\n    :func:`serve` can also be used as an asynchronous context manager. In\n    this case, the server is shut down when exiting the context.\n\n    :func:`serve` is a wrapper around the event loop\'s\n    :meth:`~asyncio.loop.create_server` method. It creates and starts a\n    :class:`~asyncio.Server` with :meth:`~asyncio.loop.create_server`. Then it\n    wraps the :class:`~asyncio.Server` in a :class:`WebSocketServer`  and\n    returns the :class:`WebSocketServer`.\n\n    The ``ws_handler`` argument is the WebSocket handler. It must be a\n    coroutine accepting two arguments: a :class:`WebSocketServerProtocol` and\n    the request URI.\n\n    The ``host`` and ``port`` arguments, as well as unrecognized keyword\n    arguments, are passed along to :meth:`~asyncio.loop.create_server`.\n\n    For example, you can set the ``ssl`` keyword argument to a\n    :class:`~ssl.SSLContext` to enable TLS.\n\n    The ``create_protocol`` parameter allows customizing the\n    :class:`~asyncio.Protocol` that manages the connection. It should be a\n    callable or class accepting the same arguments as\n    :class:`WebSocketServerProtocol` and returning an instance of\n    :class:`WebSocketServerProtocol` or a subclass. It defaults to\n    :class:`WebSocketServerProtocol`.\n\n    The behavior of ``ping_interval``, ``ping_timeout``, ``close_timeout``,\n    ``max_size``, ``max_queue``, ``read_limit``, and ``write_limit`` is\n    described in :class:`~websockets.protocol.WebSocketCommonProtocol`.\n\n    :func:`serve` also accepts the following optional arguments:\n\n    * ``compression`` is a shortcut to configure compression extensions;\n      by default it enables the "permessage-deflate" extension; set it to\n      ``None`` to disable compression\n    * ``origins`` defines acceptable Origin HTTP headers; include ``None`` if\n      the lack of an origin is acceptable\n    * ``extensions`` is a list of supported extensions in order of\n      decreasing preference\n    * ``subprotocols`` is a list of supported subprotocols in order of\n      decreasing preference\n    * ``extra_headers`` sets additional HTTP response headers  when the\n      handshake succeeds; it can be a :class:`~websockets.http.Headers`\n      instance, a :class:`~collections.abc.Mapping`, an iterable of ``(name,\n      value)`` pairs, or a callable taking the request path and headers in\n      arguments and returning one of the above\n    * ``process_request`` allows intercepting the HTTP request; it must be a\n      coroutine taking the request path and headers in argument; see\n      :meth:`~WebSocketServerProtocol.process_request` for details\n    * ``select_subprotocol`` allows customizing the logic for selecting a\n      subprotocol; it must be a callable taking the subprotocols offered by\n      the client and available on the server in argument; see\n      :meth:`~WebSocketServerProtocol.select_subprotocol` for details\n\n    Since there\'s no useful way to propagate exceptions triggered in handlers,\n    they\'re sent to the ``\'websockets.server\'`` logger instead. Debugging is\n    much easier if you configure logging to print them::\n\n        import logging\n        logger = logging.getLogger(\'websockets.server\')\n        logger.setLevel(logging.ERROR)\n        logger.addHandler(logging.StreamHandler())\n\n    '

    def __init__(self, ws_handler: Callable[([WebSocketServerProtocol, str], Awaitable[Any])], host: Optional[Union[(str, Sequence[str])]]=None, port: Optional[int]=None, *, path: Optional[str]=None, create_protocol: Optional[Type[WebSocketServerProtocol]]=None, ping_interval: float=20, ping_timeout: float=20, close_timeout: Optional[float]=None, max_size: int=1048576, max_queue: int=32, read_limit: int=65536, write_limit: int=65536, loop: Optional[asyncio.AbstractEventLoop]=None, legacy_recv: bool=False, klass: Optional[Type[WebSocketServerProtocol]]=None, timeout: Optional[float]=None, compression: Optional[str]='deflate', origins: Optional[Sequence[Optional[Origin]]]=None, extensions: Optional[Sequence[ServerExtensionFactory]]=None, subprotocols: Optional[Sequence[Subprotocol]]=None, extra_headers: Optional[HeadersLikeOrCallable]=None, process_request: Optional[Callable[([str, Headers], Awaitable[Optional[HTTPResponse]])]]=None, select_subprotocol: Optional[Callable[([Sequence[Subprotocol], Sequence[Subprotocol]], Subprotocol)]]=None, **kwargs: Any) -> None:
        if timeout is None:
            timeout = 10
        else:
            warnings.warn('rename timeout to close_timeout', DeprecationWarning)
        if close_timeout is None:
            close_timeout = timeout
        elif klass is None:
            klass = WebSocketServerProtocol
        else:
            warnings.warn('rename klass to create_protocol', DeprecationWarning)
        if create_protocol is None:
            create_protocol = klass
        if loop is None:
            loop = asyncio.get_event_loop()
        ws_server = WebSocketServer(loop)
        secure = kwargs.get('ssl') is not None
        if compression == 'deflate':
            if extensions is None:
                extensions = []
            extensions = any((ext_factory.name == ServerPerMessageDeflateFactory.name for ext_factory in extensions)) or list(extensions) + [ServerPerMessageDeflateFactory()]
        else:
            if compression is not None:
                raise ValueError(f"unsupported compression: {compression}")
            else:
                factory = functools.partial(create_protocol,
                  ws_handler,
                  ws_server,
                  host=host,
                  port=port,
                  secure=secure,
                  ping_interval=ping_interval,
                  ping_timeout=ping_timeout,
                  close_timeout=close_timeout,
                  max_size=max_size,
                  max_queue=max_queue,
                  read_limit=read_limit,
                  write_limit=write_limit,
                  loop=loop,
                  legacy_recv=legacy_recv,
                  origins=origins,
                  extensions=extensions,
                  subprotocols=subprotocols,
                  extra_headers=extra_headers,
                  process_request=process_request,
                  select_subprotocol=select_subprotocol)
                if path is None:
                    create_server = (functools.partial)(
                     (loop.create_server), factory, host, port, **kwargs)
                else:
                    if not (host is None and port is None):
                        raise AssertionError
                create_server = (functools.partial)(
                 (loop.create_unix_server), factory, path, **kwargs)
            self._create_server = create_server
            self.ws_server = ws_server

    async def __aenter__(self) -> WebSocketServer:
        return await self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        self.ws_server.close()
        await self.ws_server.wait_closed()

    def __await__(self) -> Generator[(Any, None, WebSocketServer)]:
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> WebSocketServer:
        server = await self._create_server()
        self.ws_server.wrap(server)
        return self.ws_server

    __iter__ = __await__


serve = Serve

def unix_serve(ws_handler: Callable[([WebSocketServerProtocol, str], Awaitable[Any])], path: str, **kwargs: Any) -> Serve:
    """
    Similar to :func:`serve`, but for listening on Unix sockets.

    This function calls the event loop's
    :meth:`~asyncio.loop.create_unix_server` method.

    It is only available on Unix.

    It's useful for deploying a server behind a reverse proxy such as nginx.

    :param path: file system path to the Unix socket

    """
    return serve(ws_handler, path=path, **kwargs)