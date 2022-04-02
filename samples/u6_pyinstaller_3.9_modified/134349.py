# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_protocol.py
import asyncio, asyncio.streams, traceback, warnings
from collections import deque
from contextlib import suppress
from html import escape as html_escape
from http import HTTPStatus
from logging import Logger
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Tuple, Type, cast
import yarl
from .abc import AbstractAccessLogger, AbstractStreamWriter
from .base_protocol import BaseProtocol
from .helpers import CeilTimeout, current_task
from .http import HttpProcessingError, HttpRequestParser, HttpVersion10, RawRequestMessage, StreamWriter
from .log import access_logger, server_logger
from .streams import EMPTY_PAYLOAD, StreamReader
from .tcp_helpers import tcp_keepalive
from .web_exceptions import HTTPException
from .web_log import AccessLogger
from .web_request import BaseRequest
from .web_response import Response, StreamResponse
__all__ = ('RequestHandler', 'RequestPayloadError', 'PayloadAccessError')
if TYPE_CHECKING:
    from .web_server import Server
_RequestFactory = Callable[(
 [
  RawRequestMessage,
  StreamReader,
  'RequestHandler',
  AbstractStreamWriter,
  'asyncio.Task[None]'],
 BaseRequest)]
_RequestHandler = Callable[([BaseRequest], Awaitable[StreamResponse])]
ERROR = RawRequestMessage('UNKNOWN', '/', HttpVersion10, {}, {}, True, False, False, False, yarl.URL('/'))

class RequestPayloadError(Exception):
    __doc__ = 'Payload parsing error.'


class PayloadAccessError(Exception):
    __doc__ = 'Payload was accessed after response was sent.'


class RequestHandler(BaseProtocol):
    __doc__ = 'HTTP protocol implementation.\n\n    RequestHandler handles incoming HTTP request. It reads request line,\n    request headers and request payload and calls handle_request() method.\n    By default it always returns with 404 response.\n\n    RequestHandler handles errors in incoming request, like bad\n    status line, bad headers or incomplete payload. If any error occurs,\n    connection gets closed.\n\n    :param keepalive_timeout: number of seconds before closing\n                              keep-alive connection\n    :type keepalive_timeout: int or None\n\n    :param bool tcp_keepalive: TCP keep-alive is on, default is on\n\n    :param bool debug: enable debug mode\n\n    :param logger: custom logger object\n    :type logger: aiohttp.log.server_logger\n\n    :param access_log_class: custom class for access_logger\n    :type access_log_class: aiohttp.abc.AbstractAccessLogger\n\n    :param access_log: custom logging object\n    :type access_log: aiohttp.log.server_logger\n\n    :param str access_log_format: access log format string\n\n    :param loop: Optional event loop\n\n    :param int max_line_size: Optional maximum header line size\n\n    :param int max_field_size: Optional maximum header field size\n\n    :param int max_headers: Optional maximum header size\n\n    '
    KEEPALIVE_RESCHEDULE_DELAY = 1
    __slots__ = ('_request_count', '_keepalive', '_manager', '_request_handler', '_request_factory',
                 '_tcp_keepalive', '_keepalive_time', '_keepalive_handle', '_keepalive_timeout',
                 '_lingering_time', '_messages', '_message_tail', '_waiter', '_error_handler',
                 '_task_handler', '_upgrade', '_payload_parser', '_request_parser',
                 '_reading_paused', 'logger', 'debug', 'access_log', 'access_logger',
                 '_close', '_force_close', '_current_request')

    def __init__(self, manager, *, loop, keepalive_timeout=75.0, tcp_keepalive=True, logger=server_logger, access_log_class=AccessLogger, access_log=access_logger, access_log_format=AccessLogger.LOG_FORMAT, debug=False, max_line_size=8190, max_headers=32768, max_field_size=8190, lingering_time=10.0, read_bufsize=65536):
        super().__init__(loop)
        self._request_count = 0
        self._keepalive = False
        self._current_request = None
        self._manager = manager
        self._request_handler = manager.request_handler
        self._request_factory = manager.request_factory
        self._tcp_keepalive = tcp_keepalive
        self._keepalive_time = 0.0
        self._keepalive_handle = None
        self._keepalive_timeout = keepalive_timeout
        self._lingering_time = float(lingering_time)
        self._messages = deque()
        self._message_tail = b''
        self._waiter = None
        self._error_handler = None
        self._task_handler = None
        self._upgrade = False
        self._payload_parser = None
        self._request_parser = HttpRequestParser(self,
          loop,
          read_bufsize,
          max_line_size=max_line_size,
          max_field_size=max_field_size,
          max_headers=max_headers,
          payload_exception=RequestPayloadError)
        self.logger = logger
        self.debug = debug
        self.access_log = access_log
        if access_log:
            self.access_logger = access_log_class(access_log, access_log_format)
        else:
            self.access_logger = None
        self._close = False
        self._force_close = False

    def __repr__--- This code section failed: ---

 L. 208         0  LOAD_STR                 '<{} {}>'
                2  LOAD_METHOD              format

 L. 209         4  LOAD_FAST                'self'
                6  LOAD_ATTR                __class__
                8  LOAD_ATTR                __name__

 L. 210        10  LOAD_FAST                'self'
               12  LOAD_ATTR                transport
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'
               20  LOAD_STR                 'connected'
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM            18  '18'
               24  LOAD_STR                 'disconnected'
             26_0  COME_FROM            22  '22'

 L. 208        26  CALL_METHOD_2         2  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    @property
    def keepalive_timeout(self) -> float:
        return self._keepalive_timeout

    async def shutdown--- This code section failed: ---

 L. 221         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _force_close

 L. 223         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _keepalive_handle
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 224        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _keepalive_handle
               20  LOAD_METHOD              cancel
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L. 226        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _waiter
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L. 227        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _waiter
               36  LOAD_METHOD              cancel
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          
             42_0  COME_FROM            30  '30'

 L. 230        42  LOAD_GLOBAL              suppress
               44  LOAD_GLOBAL              asyncio
               46  LOAD_ATTR                CancelledError
               48  LOAD_GLOBAL              asyncio
               50  LOAD_ATTR                TimeoutError
               52  CALL_FUNCTION_2       2  ''
               54  SETUP_WITH          208  'to 208'
               56  POP_TOP          

 L. 231        58  LOAD_GLOBAL              CeilTimeout
               60  LOAD_FAST                'timeout'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _loop
               66  LOAD_CONST               ('loop',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  SETUP_WITH          178  'to 178'
               72  POP_TOP          

 L. 232        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _error_handler
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_FALSE   106  'to 106'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _error_handler
               88  LOAD_METHOD              done
               90  CALL_METHOD_0         0  ''
               92  POP_JUMP_IF_TRUE    106  'to 106'

 L. 233        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _error_handler
               98  GET_AWAITABLE    
              100  LOAD_CONST               None
              102  YIELD_FROM       
              104  POP_TOP          
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            82  '82'

 L. 235       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _current_request
              110  LOAD_CONST               None
              112  <117>                 1  ''
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L. 236       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _current_request
              120  LOAD_METHOD              _cancel
              122  LOAD_GLOBAL              asyncio
              124  LOAD_METHOD              CancelledError
              126  CALL_METHOD_0         0  ''
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L. 238       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _task_handler
              136  LOAD_CONST               None
              138  <117>                 1  ''
              140  POP_JUMP_IF_FALSE   164  'to 164'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _task_handler
              146  LOAD_METHOD              done
              148  CALL_METHOD_0         0  ''
              150  POP_JUMP_IF_TRUE    164  'to 164'

 L. 239       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _task_handler
              156  GET_AWAITABLE    
              158  LOAD_CONST               None
              160  YIELD_FROM       
              162  POP_TOP          
            164_0  COME_FROM           150  '150'
            164_1  COME_FROM           140  '140'
              164  POP_BLOCK        
              166  LOAD_CONST               None
              168  DUP_TOP          
              170  DUP_TOP          
              172  CALL_FUNCTION_3       3  ''
              174  POP_TOP          
              176  JUMP_FORWARD        194  'to 194'
            178_0  COME_FROM_WITH       70  '70'
              178  <49>             
              180  POP_JUMP_IF_TRUE    184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          
              190  POP_EXCEPT       
              192  POP_TOP          
            194_0  COME_FROM           176  '176'
              194  POP_BLOCK        
              196  LOAD_CONST               None
              198  DUP_TOP          
              200  DUP_TOP          
              202  CALL_FUNCTION_3       3  ''
              204  POP_TOP          
              206  JUMP_FORWARD        224  'to 224'
            208_0  COME_FROM_WITH       54  '54'
              208  <49>             
              210  POP_JUMP_IF_TRUE    214  'to 214'
              212  <48>             
            214_0  COME_FROM           210  '210'
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          
              220  POP_EXCEPT       
              222  POP_TOP          
            224_0  COME_FROM           206  '206'

 L. 242       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _task_handler
              228  LOAD_CONST               None
              230  <117>                 1  ''
              232  POP_JUMP_IF_FALSE   244  'to 244'

 L. 243       234  LOAD_FAST                'self'
              236  LOAD_ATTR                _task_handler
              238  LOAD_METHOD              cancel
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          
            244_0  COME_FROM           232  '232'

 L. 245       244  LOAD_FAST                'self'
              246  LOAD_ATTR                transport
              248  LOAD_CONST               None
              250  <117>                 1  ''
          252_254  POP_JUMP_IF_FALSE   272  'to 272'

 L. 246       256  LOAD_FAST                'self'
              258  LOAD_ATTR                transport
              260  LOAD_METHOD              close
              262  CALL_METHOD_0         0  ''
              264  POP_TOP          

 L. 247       266  LOAD_CONST               None
              268  LOAD_FAST                'self'
              270  STORE_ATTR               transport
            272_0  COME_FROM           252  '252'

Parse error at or near `<117>' instruction at offset 12

    def connection_made--- This code section failed: ---

 L. 250         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              connection_made
                6  LOAD_FAST                'transport'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 252        12  LOAD_GLOBAL              cast
               14  LOAD_GLOBAL              asyncio
               16  LOAD_ATTR                Transport
               18  LOAD_FAST                'transport'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'real_transport'

 L. 253        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _tcp_keepalive
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 254        30  LOAD_GLOBAL              tcp_keepalive
               32  LOAD_FAST                'real_transport'
               34  CALL_FUNCTION_1       1  ''
               36  POP_TOP          
             38_0  COME_FROM            28  '28'

 L. 256        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _loop
               42  LOAD_METHOD              create_task
               44  LOAD_FAST                'self'
               46  LOAD_METHOD              start
               48  CALL_METHOD_0         0  ''
               50  CALL_METHOD_1         1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _task_handler

 L. 257        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _manager
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_TRUE     70  'to 70'
               66  <74>             
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            64  '64'

 L. 258        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _manager
               74  LOAD_METHOD              connection_made
               76  LOAD_FAST                'self'
               78  LOAD_FAST                'real_transport'
               80  CALL_METHOD_2         2  ''
               82  POP_TOP          

Parse error at or near `<117>' instruction at offset 62

    def connection_lost--- This code section failed: ---

 L. 261         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _manager
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 262        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 263        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _manager
               18  LOAD_METHOD              connection_lost
               20  LOAD_FAST                'self'
               22  LOAD_FAST                'exc'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

 L. 265        28  LOAD_GLOBAL              super
               30  CALL_FUNCTION_0       0  ''
               32  LOAD_METHOD              connection_lost
               34  LOAD_FAST                'exc'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 267        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _manager

 L. 268        46  LOAD_CONST               True
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _force_close

 L. 269        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _request_factory

 L. 270        58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _request_handler

 L. 271        64  LOAD_CONST               None
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _request_parser

 L. 273        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _keepalive_handle
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L. 274        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _keepalive_handle
               84  LOAD_METHOD              cancel
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          
             90_0  COME_FROM            78  '78'

 L. 276        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _current_request
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   128  'to 128'

 L. 277       100  LOAD_FAST                'exc'
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L. 278       108  LOAD_GLOBAL              ConnectionResetError
              110  LOAD_STR                 'Connection lost'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'exc'
            116_0  COME_FROM           106  '106'

 L. 279       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _current_request
              120  LOAD_METHOD              _cancel
              122  LOAD_FAST                'exc'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
            128_0  COME_FROM            98  '98'

 L. 281       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _error_handler
              132  LOAD_CONST               None
              134  <117>                 1  ''
              136  POP_JUMP_IF_FALSE   148  'to 148'

 L. 282       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _error_handler
              142  LOAD_METHOD              cancel
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          
            148_0  COME_FROM           136  '136'

 L. 283       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _task_handler
              152  LOAD_CONST               None
              154  <117>                 1  ''
              156  POP_JUMP_IF_FALSE   168  'to 168'

 L. 284       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _task_handler
              162  LOAD_METHOD              cancel
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM           156  '156'

 L. 285       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _waiter
              172  LOAD_CONST               None
              174  <117>                 1  ''
              176  POP_JUMP_IF_FALSE   188  'to 188'

 L. 286       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _waiter
              182  LOAD_METHOD              cancel
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          
            188_0  COME_FROM           176  '176'

 L. 288       188  LOAD_CONST               None
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _task_handler

 L. 290       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _payload_parser
              198  LOAD_CONST               None
              200  <117>                 1  ''
              202  POP_JUMP_IF_FALSE   220  'to 220'

 L. 291       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _payload_parser
              208  LOAD_METHOD              feed_eof
              210  CALL_METHOD_0         0  ''
              212  POP_TOP          

 L. 292       214  LOAD_CONST               None
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _payload_parser
            220_0  COME_FROM           202  '202'

Parse error at or near `None' instruction at offset -1

    def set_parser--- This code section failed: ---

 L. 296         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload_parser
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 298        14  LOAD_FAST                'parser'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _payload_parser

 L. 300        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _message_tail
               24  POP_JUMP_IF_FALSE    46  'to 46'

 L. 301        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _payload_parser
               30  LOAD_METHOD              feed_data
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _message_tail
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 302        40  LOAD_CONST               b''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _message_tail
             46_0  COME_FROM            24  '24'

Parse error at or near `None' instruction at offset -1

    def eof_received(self) -> None:
        pass

    def data_received--- This code section failed: ---

 L. 308         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _force_close
                4  POP_JUMP_IF_TRUE     12  'to 12'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _close
               10  POP_JUMP_IF_FALSE    16  'to 16'
             12_0  COME_FROM             4  '4'

 L. 309        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 311        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _payload_parser
               20  LOAD_CONST               None
               22  <117>                 0  ''
            24_26  POP_JUMP_IF_FALSE   340  'to 340'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _upgrade
            32_34  POP_JUMP_IF_TRUE    340  'to 340'

 L. 312        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _request_parser
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  <74>             
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'

 L. 313        50  SETUP_FINALLY        74  'to 74'

 L. 314        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _request_parser
               56  LOAD_METHOD              feed_data
               58  LOAD_FAST                'data'
               60  CALL_METHOD_1         1  ''
               62  UNPACK_SEQUENCE_3     3 
               64  STORE_FAST               'messages'
               66  STORE_FAST               'upgraded'
               68  STORE_FAST               'tail'
               70  POP_BLOCK        
               72  JUMP_FORWARD        228  'to 228'
             74_0  COME_FROM_FINALLY    50  '50'

 L. 315        74  DUP_TOP          
               76  LOAD_GLOBAL              HttpProcessingError
               78  <121>               152  ''
               80  POP_TOP          
               82  STORE_FAST               'exc'
               84  POP_TOP          
               86  SETUP_FINALLY       144  'to 144'

 L. 317        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _loop
               92  LOAD_METHOD              create_task

 L. 318        94  LOAD_FAST                'self'
               96  LOAD_METHOD              handle_parse_error

 L. 319        98  LOAD_GLOBAL              StreamWriter
              100  LOAD_FAST                'self'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _loop
              106  CALL_FUNCTION_2       2  ''
              108  LOAD_CONST               400
              110  LOAD_FAST                'exc'
              112  LOAD_FAST                'exc'
              114  LOAD_ATTR                message

 L. 318       116  CALL_METHOD_4         4  ''

 L. 317       118  CALL_METHOD_1         1  ''
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _error_handler

 L. 322       124  LOAD_FAST                'self'
              126  LOAD_METHOD              close
              128  CALL_METHOD_0         0  ''
              130  POP_TOP          
              132  POP_BLOCK        
              134  POP_EXCEPT       
              136  LOAD_CONST               None
              138  STORE_FAST               'exc'
              140  DELETE_FAST              'exc'
              142  JUMP_FORWARD        338  'to 338'
            144_0  COME_FROM_FINALLY    86  '86'
              144  LOAD_CONST               None
              146  STORE_FAST               'exc'
              148  DELETE_FAST              'exc'
              150  <48>             

 L. 323       152  DUP_TOP          
              154  LOAD_GLOBAL              Exception
              156  <121>               226  ''
              158  POP_TOP          
              160  STORE_FAST               'exc'
              162  POP_TOP          
              164  SETUP_FINALLY       218  'to 218'

 L. 325       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _loop
              170  LOAD_METHOD              create_task

 L. 326       172  LOAD_FAST                'self'
              174  LOAD_METHOD              handle_parse_error
              176  LOAD_GLOBAL              StreamWriter
              178  LOAD_FAST                'self'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                _loop
              184  CALL_FUNCTION_2       2  ''
              186  LOAD_CONST               500
              188  LOAD_FAST                'exc'
              190  CALL_METHOD_3         3  ''

 L. 325       192  CALL_METHOD_1         1  ''
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _error_handler

 L. 328       198  LOAD_FAST                'self'
              200  LOAD_METHOD              close
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          
              206  POP_BLOCK        
              208  POP_EXCEPT       
              210  LOAD_CONST               None
              212  STORE_FAST               'exc'
              214  DELETE_FAST              'exc'
              216  JUMP_FORWARD        338  'to 338'
            218_0  COME_FROM_FINALLY   164  '164'
              218  LOAD_CONST               None
              220  STORE_FAST               'exc'
              222  DELETE_FAST              'exc'
              224  <48>             
              226  <48>             
            228_0  COME_FROM            72  '72'

 L. 330       228  LOAD_FAST                'messages'
          230_232  POP_JUMP_IF_FALSE   314  'to 314'

 L. 332       234  LOAD_FAST                'messages'
              236  GET_ITER         
              238  FOR_ITER            278  'to 278'
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               'msg'
              244  STORE_FAST               'payload'

 L. 333       246  LOAD_FAST                'self'
              248  DUP_TOP          
              250  LOAD_ATTR                _request_count
              252  LOAD_CONST               1
              254  INPLACE_ADD      
              256  ROT_TWO          
              258  STORE_ATTR               _request_count

 L. 334       260  LOAD_FAST                'self'
              262  LOAD_ATTR                _messages
              264  LOAD_METHOD              append
              266  LOAD_FAST                'msg'
              268  LOAD_FAST                'payload'
              270  BUILD_TUPLE_2         2 
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK           238  'to 238'

 L. 336       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _waiter
              282  STORE_FAST               'waiter'

 L. 337       284  LOAD_FAST                'waiter'
              286  LOAD_CONST               None
              288  <117>                 1  ''
          290_292  POP_JUMP_IF_FALSE   314  'to 314'

 L. 338       294  LOAD_FAST                'waiter'
              296  LOAD_METHOD              done
              298  CALL_METHOD_0         0  ''
          300_302  POP_JUMP_IF_TRUE    314  'to 314'

 L. 340       304  LOAD_FAST                'waiter'
              306  LOAD_METHOD              set_result
              308  LOAD_CONST               None
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
            314_0  COME_FROM           300  '300'
            314_1  COME_FROM           290  '290'
            314_2  COME_FROM           230  '230'

 L. 342       314  LOAD_FAST                'upgraded'
              316  LOAD_FAST                'self'
              318  STORE_ATTR               _upgrade

 L. 343       320  LOAD_FAST                'upgraded'
          322_324  POP_JUMP_IF_FALSE   418  'to 418'
              326  LOAD_FAST                'tail'
          328_330  POP_JUMP_IF_FALSE   418  'to 418'

 L. 344       332  LOAD_FAST                'tail'
              334  LOAD_FAST                'self'
              336  STORE_ATTR               _message_tail
            338_0  COME_FROM           216  '216'
            338_1  COME_FROM           142  '142'
              338  JUMP_FORWARD        418  'to 418'
            340_0  COME_FROM            32  '32'
            340_1  COME_FROM            24  '24'

 L. 347       340  LOAD_FAST                'self'
              342  LOAD_ATTR                _payload_parser
              344  LOAD_CONST               None
              346  <117>                 0  ''
          348_350  POP_JUMP_IF_FALSE   382  'to 382'
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                _upgrade
          356_358  POP_JUMP_IF_FALSE   382  'to 382'
              360  LOAD_FAST                'data'
          362_364  POP_JUMP_IF_FALSE   382  'to 382'

 L. 348       366  LOAD_FAST                'self'
              368  DUP_TOP          
              370  LOAD_ATTR                _message_tail
              372  LOAD_FAST                'data'
              374  INPLACE_ADD      
              376  ROT_TWO          
              378  STORE_ATTR               _message_tail
              380  JUMP_FORWARD        418  'to 418'
            382_0  COME_FROM           362  '362'
            382_1  COME_FROM           356  '356'
            382_2  COME_FROM           348  '348'

 L. 351       382  LOAD_FAST                'data'
          384_386  POP_JUMP_IF_FALSE   418  'to 418'

 L. 352       388  LOAD_FAST                'self'
              390  LOAD_ATTR                _payload_parser
              392  LOAD_METHOD              feed_data
              394  LOAD_FAST                'data'
              396  CALL_METHOD_1         1  ''
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'eof'
              402  STORE_FAST               'tail'

 L. 353       404  LOAD_FAST                'eof'
          406_408  POP_JUMP_IF_FALSE   418  'to 418'

 L. 354       410  LOAD_FAST                'self'
              412  LOAD_METHOD              close
              414  CALL_METHOD_0         0  ''
              416  POP_TOP          
            418_0  COME_FROM           406  '406'
            418_1  COME_FROM           384  '384'
            418_2  COME_FROM           380  '380'
            418_3  COME_FROM           338  '338'
            418_4  COME_FROM           328  '328'
            418_5  COME_FROM           322  '322'

Parse error at or near `<117>' instruction at offset 22

    def keep_alive(self, val: bool) -> None:
        """Set keep-alive connection mode.

        :param bool val: new state.
        """
        self._keepalive = val
        if self._keepalive_handle:
            self._keepalive_handle.cancel
            self._keepalive_handle = None

    def close(self) -> None:
        """Stop accepting new pipelinig messages and close
        connection when handlers done processing messages"""
        self._close = True
        if self._waiter:
            self._waiter.cancel

    def force_close--- This code section failed: ---

 L. 375         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _force_close

 L. 376         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _waiter
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L. 377        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _waiter
               16  LOAD_METHOD              cancel
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          
             22_0  COME_FROM            10  '10'

 L. 378        22  LOAD_FAST                'self'
               24  LOAD_ATTR                transport
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L. 379        32  LOAD_FAST                'self'
               34  LOAD_ATTR                transport
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 380        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               transport
             48_0  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 28

    def log_access--- This code section failed: ---

 L. 385         0  LOAD_FAST                'self'
                2  LOAD_ATTR                access_logger
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    36  'to 36'

 L. 386        10  LOAD_FAST                'self'
               12  LOAD_ATTR                access_logger
               14  LOAD_METHOD              log
               16  LOAD_FAST                'request'
               18  LOAD_FAST                'response'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _loop
               24  LOAD_METHOD              time
               26  CALL_METHOD_0         0  ''
               28  LOAD_FAST                'time'
               30  BINARY_SUBTRACT  
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          
             36_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def log_debug--- This code section failed: ---

 L. 389         0  LOAD_FAST                'self'
                2  LOAD_ATTR                debug
                4  POP_JUMP_IF_FALSE    24  'to 24'

 L. 390         6  LOAD_FAST                'self'
                8  LOAD_ATTR                logger
               10  LOAD_ATTR                debug
               12  LOAD_FAST                'args'
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kw'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_TOP          
             24_0  COME_FROM             4  '4'

Parse error at or near `<164>' instruction at offset 18

    def log_exception--- This code section failed: ---

 L. 393         0  LOAD_FAST                'self'
                2  LOAD_ATTR                logger
                4  LOAD_ATTR                exception
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _process_keepalive(self) -> None:
        return self._force_close or self._keepalive or None
        next = self._keepalive_time + self._keepalive_timeout
        if self._waiter:
            if self._loop.time > next:
                self.force_close
                return None
        self._keepalive_handle = self._loop.call_laterself.KEEPALIVE_RESCHEDULE_DELAYself._process_keepalive

    async def _handle_request--- This code section failed: ---

 L. 418         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _request_handler
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 419        14  SETUP_FINALLY        62  'to 62'

 L. 420        16  SETUP_FINALLY        50  'to 50'

 L. 421        18  LOAD_FAST                'request'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _current_request

 L. 422        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _request_handler
               28  LOAD_FAST                'request'
               30  CALL_METHOD_1         1  ''
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  STORE_FAST               'resp'
               40  POP_BLOCK        

 L. 424        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _current_request
               48  JUMP_FORWARD         58  'to 58'
             50_0  COME_FROM_FINALLY    16  '16'
               50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _current_request
               56  <48>             
             58_0  COME_FROM            48  '48'
               58  POP_BLOCK        
               60  JUMP_FORWARD        314  'to 314'
             62_0  COME_FROM_FINALLY    14  '14'

 L. 425        62  DUP_TOP          
               64  LOAD_GLOBAL              HTTPException
               66  <121>               140  ''
               68  POP_TOP          
               70  STORE_FAST               'exc'
               72  POP_TOP          
               74  SETUP_FINALLY       132  'to 132'

 L. 426        76  LOAD_GLOBAL              Response

 L. 427        78  LOAD_FAST                'exc'
               80  LOAD_ATTR                status
               82  LOAD_FAST                'exc'
               84  LOAD_ATTR                reason
               86  LOAD_FAST                'exc'
               88  LOAD_ATTR                text
               90  LOAD_FAST                'exc'
               92  LOAD_ATTR                headers

 L. 426        94  LOAD_CONST               ('status', 'reason', 'text', 'headers')
               96  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               98  STORE_FAST               'resp'

 L. 429       100  LOAD_FAST                'self'
              102  LOAD_METHOD              finish_response
              104  LOAD_FAST                'request'
              106  LOAD_FAST                'resp'
              108  LOAD_FAST                'start_time'
              110  CALL_METHOD_3         3  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  STORE_FAST               'reset'
              120  POP_BLOCK        
              122  POP_EXCEPT       
              124  LOAD_CONST               None
              126  STORE_FAST               'exc'
              128  DELETE_FAST              'exc'
              130  JUMP_FORWARD        334  'to 334'
            132_0  COME_FROM_FINALLY    74  '74'
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  <48>             

 L. 430       140  DUP_TOP          
              142  LOAD_GLOBAL              asyncio
              144  LOAD_ATTR                CancelledError
              146  <121>               160  ''
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 431       154  RAISE_VARARGS_0       0  'reraise'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        334  'to 334'

 L. 432       160  DUP_TOP          
              162  LOAD_GLOBAL              asyncio
              164  LOAD_ATTR                TimeoutError
              166  <121>               242  ''
              168  POP_TOP          
              170  STORE_FAST               'exc'
              172  POP_TOP          
              174  SETUP_FINALLY       234  'to 234'

 L. 433       176  LOAD_FAST                'self'
              178  LOAD_ATTR                log_debug
              180  LOAD_STR                 'Request handler timed out.'
              182  LOAD_FAST                'exc'
              184  LOAD_CONST               ('exc_info',)
              186  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              188  POP_TOP          

 L. 434       190  LOAD_FAST                'self'
              192  LOAD_METHOD              handle_error
              194  LOAD_FAST                'request'
              196  LOAD_CONST               504
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'resp'

 L. 435       202  LOAD_FAST                'self'
              204  LOAD_METHOD              finish_response
              206  LOAD_FAST                'request'
              208  LOAD_FAST                'resp'
              210  LOAD_FAST                'start_time'
              212  CALL_METHOD_3         3  ''
              214  GET_AWAITABLE    
              216  LOAD_CONST               None
              218  YIELD_FROM       
              220  STORE_FAST               'reset'
              222  POP_BLOCK        
              224  POP_EXCEPT       
              226  LOAD_CONST               None
              228  STORE_FAST               'exc'
              230  DELETE_FAST              'exc'
              232  JUMP_FORWARD        334  'to 334'
            234_0  COME_FROM_FINALLY   174  '174'
              234  LOAD_CONST               None
              236  STORE_FAST               'exc'
              238  DELETE_FAST              'exc'
              240  <48>             

 L. 436       242  DUP_TOP          
              244  LOAD_GLOBAL              Exception
          246_248  <121>               312  ''
              250  POP_TOP          
              252  STORE_FAST               'exc'
              254  POP_TOP          
              256  SETUP_FINALLY       304  'to 304'

 L. 437       258  LOAD_FAST                'self'
              260  LOAD_METHOD              handle_error
              262  LOAD_FAST                'request'
              264  LOAD_CONST               500
              266  LOAD_FAST                'exc'
              268  CALL_METHOD_3         3  ''
              270  STORE_FAST               'resp'

 L. 438       272  LOAD_FAST                'self'
              274  LOAD_METHOD              finish_response
              276  LOAD_FAST                'request'
              278  LOAD_FAST                'resp'
              280  LOAD_FAST                'start_time'
              282  CALL_METHOD_3         3  ''
              284  GET_AWAITABLE    
              286  LOAD_CONST               None
              288  YIELD_FROM       
              290  STORE_FAST               'reset'
              292  POP_BLOCK        
              294  POP_EXCEPT       
              296  LOAD_CONST               None
              298  STORE_FAST               'exc'
              300  DELETE_FAST              'exc'
              302  JUMP_FORWARD        334  'to 334'
            304_0  COME_FROM_FINALLY   256  '256'
              304  LOAD_CONST               None
              306  STORE_FAST               'exc'
              308  DELETE_FAST              'exc'
              310  <48>             
              312  <48>             
            314_0  COME_FROM            60  '60'

 L. 440       314  LOAD_FAST                'self'
              316  LOAD_METHOD              finish_response
              318  LOAD_FAST                'request'
              320  LOAD_FAST                'resp'
              322  LOAD_FAST                'start_time'
              324  CALL_METHOD_3         3  ''
              326  GET_AWAITABLE    
              328  LOAD_CONST               None
              330  YIELD_FROM       
              332  STORE_FAST               'reset'
            334_0  COME_FROM           302  '302'
            334_1  COME_FROM           232  '232'
            334_2  COME_FROM           158  '158'
            334_3  COME_FROM           130  '130'

 L. 442       334  LOAD_FAST                'resp'
              336  LOAD_FAST                'reset'
              338  BUILD_TUPLE_2         2 
              340  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    async def start--- This code section failed: ---

 L. 453         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  STORE_FAST               'loop'

 L. 454         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _task_handler
               10  STORE_FAST               'handler'

 L. 455        12  LOAD_FAST                'handler'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 456        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _manager
               28  STORE_FAST               'manager'

 L. 457        30  LOAD_FAST                'manager'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L. 458        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _keepalive_timeout
               46  STORE_FAST               'keepalive_timeout'

 L. 459        48  LOAD_CONST               None
               50  STORE_FAST               'resp'

 L. 460        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _request_factory
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L. 461        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _request_handler
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_TRUE     80  'to 80'
               76  <74>             
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            74  '74'

 L. 463        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _force_close
            84_86  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 464        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _messages
               92  POP_JUMP_IF_TRUE    176  'to 176'

 L. 465        94  SETUP_FINALLY       168  'to 168'
               96  SETUP_FINALLY       124  'to 124'

 L. 467        98  LOAD_FAST                'loop'
              100  LOAD_METHOD              create_future
              102  CALL_METHOD_0         0  ''
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _waiter

 L. 468       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _waiter
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        158  'to 158'
            124_0  COME_FROM_FINALLY    96  '96'

 L. 469       124  DUP_TOP          
              126  LOAD_GLOBAL              asyncio
              128  LOAD_ATTR                CancelledError
              130  <121>               156  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 470       138  POP_EXCEPT       
              140  POP_BLOCK        

 L. 472       142  LOAD_CONST               None
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _waiter

 L. 470   148_150  BREAK_LOOP         1444  'to 1444'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
              156  <48>             
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           122  '122'
              158  POP_BLOCK        

 L. 472       160  LOAD_CONST               None
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _waiter
              166  JUMP_FORWARD        176  'to 176'
            168_0  COME_FROM_FINALLY    94  '94'
              168  LOAD_CONST               None
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _waiter
              174  <48>             
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM            92  '92'

 L. 474       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _messages
              180  LOAD_METHOD              popleft
              182  CALL_METHOD_0         0  ''
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               'message'
              188  STORE_FAST               'payload'

 L. 476       190  LOAD_FAST                'loop'
              192  LOAD_METHOD              time
              194  CALL_METHOD_0         0  ''
              196  STORE_FAST               'start'

 L. 478       198  LOAD_FAST                'manager'
              200  DUP_TOP          
              202  LOAD_ATTR                requests_count
              204  LOAD_CONST               1
              206  INPLACE_ADD      
              208  ROT_TWO          
              210  STORE_ATTR               requests_count

 L. 479       212  LOAD_GLOBAL              StreamWriter
              214  LOAD_FAST                'self'
              216  LOAD_FAST                'loop'
              218  CALL_FUNCTION_2       2  ''
              220  STORE_FAST               'writer'

 L. 480       222  LOAD_FAST                'self'
              224  LOAD_METHOD              _request_factory
              226  LOAD_FAST                'message'
              228  LOAD_FAST                'payload'
              230  LOAD_FAST                'self'
              232  LOAD_FAST                'writer'
              234  LOAD_FAST                'handler'
              236  CALL_METHOD_5         5  ''
              238  STORE_FAST               'request'

 L. 481   240_242  SETUP_FINALLY      1310  'to 1310'
          244_246  SETUP_FINALLY       898  'to 898'

 L. 483       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _loop
              252  LOAD_METHOD              create_task
              254  LOAD_FAST                'self'
              256  LOAD_METHOD              _handle_request
              258  LOAD_FAST                'request'
              260  LOAD_FAST                'start'
              262  CALL_METHOD_2         2  ''
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'task'

 L. 484       268  SETUP_FINALLY       288  'to 288'

 L. 485       270  LOAD_FAST                'task'
              272  GET_AWAITABLE    
              274  LOAD_CONST               None
              276  YIELD_FROM       
              278  UNPACK_SEQUENCE_2     2 
              280  STORE_FAST               'resp'
              282  STORE_FAST               'reset'
              284  POP_BLOCK        
              286  JUMP_FORWARD        456  'to 456'
            288_0  COME_FROM_FINALLY   268  '268'

 L. 486       288  DUP_TOP          
              290  LOAD_GLOBAL              asyncio
              292  LOAD_ATTR                CancelledError
              294  LOAD_GLOBAL              ConnectionError
              296  BUILD_TUPLE_2         2 
          298_300  <121>               454  ''
              302  POP_TOP          
              304  POP_TOP          
              306  POP_TOP          

 L. 487       308  LOAD_FAST                'self'
              310  LOAD_METHOD              log_debug
              312  LOAD_STR                 'Ignored premature client disconnection'
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          

 L. 488       318  POP_EXCEPT       
              320  POP_BLOCK        
              322  POP_BLOCK        

 L. 543       324  LOAD_FAST                'self'
              326  LOAD_ATTR                transport
              328  LOAD_CONST               None
              330  <117>                 0  ''
          332_334  POP_JUMP_IF_FALSE   358  'to 358'
              336  LOAD_FAST                'resp'
              338  LOAD_CONST               None
              340  <117>                 1  ''
          342_344  POP_JUMP_IF_FALSE   358  'to 358'

 L. 544       346  LOAD_FAST                'self'
              348  LOAD_METHOD              log_debug
              350  LOAD_STR                 'Ignored premature client disconnection.'
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
              356  JUMP_ABSOLUTE      1444  'to 1444'
            358_0  COME_FROM           342  '342'
            358_1  COME_FROM           332  '332'

 L. 545       358  LOAD_FAST                'self'
              360  LOAD_ATTR                _force_close
          362_364  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 546       366  LOAD_FAST                'self'
              368  LOAD_ATTR                _keepalive
          370_372  POP_JUMP_IF_FALSE  1444  'to 1444'
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                _close
          378_380  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 548       382  LOAD_FAST                'keepalive_timeout'
              384  LOAD_CONST               None
              386  <117>                 1  ''
          388_390  POP_JUMP_IF_FALSE   446  'to 446'

 L. 549       392  LOAD_FAST                'self'
              394  LOAD_ATTR                _loop
              396  LOAD_METHOD              time
              398  CALL_METHOD_0         0  ''
              400  STORE_FAST               'now'

 L. 550       402  LOAD_FAST                'now'
              404  LOAD_FAST                'self'
              406  STORE_ATTR               _keepalive_time

 L. 551       408  LOAD_FAST                'self'
              410  LOAD_ATTR                _keepalive_handle
              412  LOAD_CONST               None
              414  <117>                 0  ''
          416_418  POP_JUMP_IF_FALSE   446  'to 446'

 L. 552       420  LOAD_FAST                'loop'
              422  LOAD_METHOD              call_at

 L. 553       424  LOAD_FAST                'now'
              426  LOAD_FAST                'keepalive_timeout'
              428  BINARY_ADD       
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                _process_keepalive

 L. 552       434  CALL_METHOD_2         2  ''
              436  LOAD_FAST                'self'
              438  STORE_ATTR               _keepalive_handle
              440  JUMP_ABSOLUTE      1444  'to 1444'

 L. 556   442_444  BREAK_LOOP         1444  'to 1444'
            446_0  COME_FROM           416  '416'
            446_1  COME_FROM           388  '388'

 L. 488   446_448  BREAK_LOOP         1444  'to 1444'
              450  POP_EXCEPT       
              452  JUMP_FORWARD        456  'to 456'
              454  <48>             
            456_0  COME_FROM           452  '452'
            456_1  COME_FROM           286  '286'

 L. 490       456  LOAD_GLOBAL              getattr
              458  LOAD_FAST                'resp'
              460  LOAD_STR                 '__http_exception__'
              462  LOAD_CONST               False
              464  CALL_FUNCTION_3       3  ''
          466_468  POP_JUMP_IF_FALSE   482  'to 482'

 L. 491       470  LOAD_GLOBAL              warnings
              472  LOAD_METHOD              warn

 L. 492       474  LOAD_STR                 'returning HTTPException object is deprecated (#2415) and will be removed, please raise the exception instead'

 L. 495       476  LOAD_GLOBAL              DeprecationWarning

 L. 491       478  CALL_METHOD_2         2  ''
              480  POP_TOP          
            482_0  COME_FROM           466  '466'

 L. 499       482  DELETE_FAST              'task'

 L. 500       484  LOAD_FAST                'reset'
          486_488  POP_JUMP_IF_FALSE   630  'to 630'

 L. 501       490  LOAD_FAST                'self'
              492  LOAD_METHOD              log_debug
              494  LOAD_STR                 'Ignored premature client disconnection 2'
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          

 L. 502       500  POP_BLOCK        
              502  POP_BLOCK        

 L. 543       504  LOAD_FAST                'self'
              506  LOAD_ATTR                transport
              508  LOAD_CONST               None
              510  <117>                 0  ''
          512_514  POP_JUMP_IF_FALSE   538  'to 538'
              516  LOAD_FAST                'resp'
              518  LOAD_CONST               None
              520  <117>                 1  ''
          522_524  POP_JUMP_IF_FALSE   538  'to 538'

 L. 544       526  LOAD_FAST                'self'
              528  LOAD_METHOD              log_debug
              530  LOAD_STR                 'Ignored premature client disconnection.'
              532  CALL_METHOD_1         1  ''
              534  POP_TOP          
              536  JUMP_ABSOLUTE      1444  'to 1444'
            538_0  COME_FROM           522  '522'
            538_1  COME_FROM           512  '512'

 L. 545       538  LOAD_FAST                'self'
              540  LOAD_ATTR                _force_close
          542_544  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 546       546  LOAD_FAST                'self'
              548  LOAD_ATTR                _keepalive
          550_552  POP_JUMP_IF_FALSE  1444  'to 1444'
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                _close
          558_560  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 548       562  LOAD_FAST                'keepalive_timeout'
              564  LOAD_CONST               None
              566  <117>                 1  ''
          568_570  POP_JUMP_IF_FALSE   626  'to 626'

 L. 549       572  LOAD_FAST                'self'
              574  LOAD_ATTR                _loop
              576  LOAD_METHOD              time
              578  CALL_METHOD_0         0  ''
              580  STORE_FAST               'now'

 L. 550       582  LOAD_FAST                'now'
              584  LOAD_FAST                'self'
              586  STORE_ATTR               _keepalive_time

 L. 551       588  LOAD_FAST                'self'
              590  LOAD_ATTR                _keepalive_handle
              592  LOAD_CONST               None
              594  <117>                 0  ''
          596_598  POP_JUMP_IF_FALSE   626  'to 626'

 L. 552       600  LOAD_FAST                'loop'
              602  LOAD_METHOD              call_at

 L. 553       604  LOAD_FAST                'now'
              606  LOAD_FAST                'keepalive_timeout'
              608  BINARY_ADD       
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                _process_keepalive

 L. 552       614  CALL_METHOD_2         2  ''
              616  LOAD_FAST                'self'
              618  STORE_ATTR               _keepalive_handle
              620  JUMP_ABSOLUTE      1444  'to 1444'

 L. 556   622_624  BREAK_LOOP         1444  'to 1444'
            626_0  COME_FROM           596  '596'
            626_1  COME_FROM           568  '568'

 L. 502   626_628  BREAK_LOOP         1444  'to 1444'
            630_0  COME_FROM           486  '486'

 L. 505       630  LOAD_GLOBAL              bool
              632  LOAD_FAST                'resp'
              634  LOAD_ATTR                keep_alive
              636  CALL_FUNCTION_1       1  ''
              638  LOAD_FAST                'self'
              640  STORE_ATTR               _keepalive

 L. 508       642  LOAD_FAST                'payload'
              644  LOAD_METHOD              is_eof
              646  CALL_METHOD_0         0  ''
          648_650  POP_JUMP_IF_TRUE    880  'to 880'

 L. 509       652  LOAD_FAST                'self'
              654  LOAD_ATTR                _lingering_time
              656  STORE_FAST               'lingering_time'

 L. 510       658  LOAD_FAST                'self'
              660  LOAD_ATTR                _force_close
          662_664  POP_JUMP_IF_TRUE    844  'to 844'
              666  LOAD_FAST                'lingering_time'
          668_670  POP_JUMP_IF_FALSE   844  'to 844'

 L. 511       672  LOAD_FAST                'self'
              674  LOAD_METHOD              log_debug

 L. 512       676  LOAD_STR                 'Start lingering close timer for %s sec.'
              678  LOAD_FAST                'lingering_time'

 L. 511       680  CALL_METHOD_2         2  ''
              682  POP_TOP          

 L. 515       684  LOAD_FAST                'loop'
              686  LOAD_METHOD              time
              688  CALL_METHOD_0         0  ''
              690  STORE_FAST               'now'

 L. 516       692  LOAD_FAST                'now'
              694  LOAD_FAST                'lingering_time'
              696  BINARY_ADD       
              698  STORE_FAST               'end_t'

 L. 518       700  LOAD_GLOBAL              suppress
              702  LOAD_GLOBAL              asyncio
              704  LOAD_ATTR                TimeoutError
              706  LOAD_GLOBAL              asyncio
              708  LOAD_ATTR                CancelledError
              710  CALL_FUNCTION_2       2  ''
              712  SETUP_WITH          826  'to 826'
              714  POP_TOP          

 L. 519       716  LOAD_FAST                'payload'
              718  LOAD_METHOD              is_eof
              720  CALL_METHOD_0         0  ''
          722_724  POP_JUMP_IF_TRUE    812  'to 812'
              726  LOAD_FAST                'now'
              728  LOAD_FAST                'end_t'
              730  COMPARE_OP               <
          732_734  POP_JUMP_IF_FALSE   812  'to 812'

 L. 520       736  LOAD_GLOBAL              CeilTimeout
              738  LOAD_FAST                'end_t'
              740  LOAD_FAST                'now'
              742  BINARY_SUBTRACT  
              744  LOAD_FAST                'loop'
              746  LOAD_CONST               ('loop',)
              748  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              750  SETUP_WITH          782  'to 782'
              752  POP_TOP          

 L. 522       754  LOAD_FAST                'payload'
              756  LOAD_METHOD              readany
              758  CALL_METHOD_0         0  ''
              760  GET_AWAITABLE    
              762  LOAD_CONST               None
              764  YIELD_FROM       
              766  POP_TOP          
              768  POP_BLOCK        
              770  LOAD_CONST               None
              772  DUP_TOP          
              774  DUP_TOP          
              776  CALL_FUNCTION_3       3  ''
              778  POP_TOP          
              780  JUMP_FORWARD        800  'to 800'
            782_0  COME_FROM_WITH      750  '750'
              782  <49>             
          784_786  POP_JUMP_IF_TRUE    790  'to 790'
              788  <48>             
            790_0  COME_FROM           784  '784'
              790  POP_TOP          
              792  POP_TOP          
              794  POP_TOP          
              796  POP_EXCEPT       
              798  POP_TOP          
            800_0  COME_FROM           780  '780'

 L. 523       800  LOAD_FAST                'loop'
              802  LOAD_METHOD              time
              804  CALL_METHOD_0         0  ''
              806  STORE_FAST               'now'
          808_810  JUMP_BACK           716  'to 716'
            812_0  COME_FROM           732  '732'
            812_1  COME_FROM           722  '722'
              812  POP_BLOCK        
              814  LOAD_CONST               None
              816  DUP_TOP          
              818  DUP_TOP          
              820  CALL_FUNCTION_3       3  ''
              822  POP_TOP          
              824  JUMP_FORWARD        844  'to 844'
            826_0  COME_FROM_WITH      712  '712'
              826  <49>             
          828_830  POP_JUMP_IF_TRUE    834  'to 834'
              832  <48>             
            834_0  COME_FROM           828  '828'
              834  POP_TOP          
              836  POP_TOP          
              838  POP_TOP          
              840  POP_EXCEPT       
              842  POP_TOP          
            844_0  COME_FROM           824  '824'
            844_1  COME_FROM           668  '668'
            844_2  COME_FROM           662  '662'

 L. 526       844  LOAD_FAST                'payload'
              846  LOAD_METHOD              is_eof
              848  CALL_METHOD_0         0  ''
          850_852  POP_JUMP_IF_TRUE    880  'to 880'
              854  LOAD_FAST                'self'
              856  LOAD_ATTR                _force_close
          858_860  POP_JUMP_IF_TRUE    880  'to 880'

 L. 527       862  LOAD_FAST                'self'
              864  LOAD_METHOD              log_debug
              866  LOAD_STR                 'Uncompleted request.'
              868  CALL_METHOD_1         1  ''
              870  POP_TOP          

 L. 528       872  LOAD_FAST                'self'
              874  LOAD_METHOD              close
              876  CALL_METHOD_0         0  ''
              878  POP_TOP          
            880_0  COME_FROM           858  '858'
            880_1  COME_FROM           850  '850'
            880_2  COME_FROM           648  '648'

 L. 530       880  LOAD_FAST                'payload'
              882  LOAD_METHOD              set_exception
              884  LOAD_GLOBAL              PayloadAccessError
              886  CALL_FUNCTION_0       0  ''
              888  CALL_METHOD_1         1  ''
              890  POP_TOP          
              892  POP_BLOCK        
          894_896  JUMP_FORWARD       1184  'to 1184'
            898_0  COME_FROM_FINALLY   244  '244'

 L. 532       898  DUP_TOP          
              900  LOAD_GLOBAL              asyncio
              902  LOAD_ATTR                CancelledError
          904_906  <121>              1058  ''
              908  POP_TOP          
              910  POP_TOP          
              912  POP_TOP          

 L. 533       914  LOAD_FAST                'self'
              916  LOAD_METHOD              log_debug
              918  LOAD_STR                 'Ignored premature client disconnection '
              920  CALL_METHOD_1         1  ''
              922  POP_TOP          

 L. 534       924  POP_EXCEPT       
              926  POP_BLOCK        

 L. 543       928  LOAD_FAST                'self'
              930  LOAD_ATTR                transport
              932  LOAD_CONST               None
              934  <117>                 0  ''
          936_938  POP_JUMP_IF_FALSE   962  'to 962'
              940  LOAD_FAST                'resp'
              942  LOAD_CONST               None
              944  <117>                 1  ''
          946_948  POP_JUMP_IF_FALSE   962  'to 962'

 L. 544       950  LOAD_FAST                'self'
              952  LOAD_METHOD              log_debug
              954  LOAD_STR                 'Ignored premature client disconnection.'
              956  CALL_METHOD_1         1  ''
              958  POP_TOP          
              960  JUMP_ABSOLUTE      1444  'to 1444'
            962_0  COME_FROM           946  '946'
            962_1  COME_FROM           936  '936'

 L. 545       962  LOAD_FAST                'self'
              964  LOAD_ATTR                _force_close
          966_968  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 546       970  LOAD_FAST                'self'
              972  LOAD_ATTR                _keepalive
          974_976  POP_JUMP_IF_FALSE  1444  'to 1444'
              978  LOAD_FAST                'self'
              980  LOAD_ATTR                _close
          982_984  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 548       986  LOAD_FAST                'keepalive_timeout'
              988  LOAD_CONST               None
              990  <117>                 1  ''
          992_994  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 549       996  LOAD_FAST                'self'
              998  LOAD_ATTR                _loop
             1000  LOAD_METHOD              time
             1002  CALL_METHOD_0         0  ''
             1004  STORE_FAST               'now'

 L. 550      1006  LOAD_FAST                'now'
             1008  LOAD_FAST                'self'
             1010  STORE_ATTR               _keepalive_time

 L. 551      1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                _keepalive_handle
             1016  LOAD_CONST               None
             1018  <117>                 0  ''
         1020_1022  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 552      1024  LOAD_FAST                'loop'
             1026  LOAD_METHOD              call_at

 L. 553      1028  LOAD_FAST                'now'
             1030  LOAD_FAST                'keepalive_timeout'
             1032  BINARY_ADD       
             1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                _process_keepalive

 L. 552      1038  CALL_METHOD_2         2  ''
             1040  LOAD_FAST                'self'
             1042  STORE_ATTR               _keepalive_handle
             1044  JUMP_ABSOLUTE      1444  'to 1444'

 L. 556  1046_1048  BREAK_LOOP         1444  'to 1444'
           1050_0  COME_FROM          1020  '1020'
           1050_1  COME_FROM           992  '992'

 L. 534  1050_1052  BREAK_LOOP         1444  'to 1444'
             1054  POP_EXCEPT       
             1056  JUMP_FORWARD       1184  'to 1184'

 L. 535      1058  DUP_TOP          
             1060  LOAD_GLOBAL              RuntimeError
         1062_1064  <121>              1124  ''
             1066  POP_TOP          
             1068  STORE_FAST               'exc'
             1070  POP_TOP          
             1072  SETUP_FINALLY      1116  'to 1116'

 L. 536      1074  LOAD_FAST                'self'
             1076  LOAD_ATTR                debug
         1078_1080  POP_JUMP_IF_FALSE  1096  'to 1096'

 L. 537      1082  LOAD_FAST                'self'
             1084  LOAD_ATTR                log_exception
             1086  LOAD_STR                 'Unhandled runtime exception'
             1088  LOAD_FAST                'exc'
             1090  LOAD_CONST               ('exc_info',)
             1092  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1094  POP_TOP          
           1096_0  COME_FROM          1078  '1078'

 L. 538      1096  LOAD_FAST                'self'
             1098  LOAD_METHOD              force_close
             1100  CALL_METHOD_0         0  ''
             1102  POP_TOP          
             1104  POP_BLOCK        
             1106  POP_EXCEPT       
             1108  LOAD_CONST               None
             1110  STORE_FAST               'exc'
             1112  DELETE_FAST              'exc'
             1114  JUMP_FORWARD       1184  'to 1184'
           1116_0  COME_FROM_FINALLY  1072  '1072'
             1116  LOAD_CONST               None
             1118  STORE_FAST               'exc'
             1120  DELETE_FAST              'exc'
             1122  <48>             

 L. 539      1124  DUP_TOP          
             1126  LOAD_GLOBAL              Exception
         1128_1130  <121>              1182  ''
             1132  POP_TOP          
             1134  STORE_FAST               'exc'
             1136  POP_TOP          
             1138  SETUP_FINALLY      1174  'to 1174'

 L. 540      1140  LOAD_FAST                'self'
             1142  LOAD_ATTR                log_exception
             1144  LOAD_STR                 'Unhandled exception'
             1146  LOAD_FAST                'exc'
             1148  LOAD_CONST               ('exc_info',)
             1150  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1152  POP_TOP          

 L. 541      1154  LOAD_FAST                'self'
             1156  LOAD_METHOD              force_close
             1158  CALL_METHOD_0         0  ''
             1160  POP_TOP          
             1162  POP_BLOCK        
             1164  POP_EXCEPT       
             1166  LOAD_CONST               None
             1168  STORE_FAST               'exc'
             1170  DELETE_FAST              'exc'
             1172  JUMP_FORWARD       1184  'to 1184'
           1174_0  COME_FROM_FINALLY  1138  '1138'
             1174  LOAD_CONST               None
             1176  STORE_FAST               'exc'
             1178  DELETE_FAST              'exc'
             1180  <48>             
             1182  <48>             
           1184_0  COME_FROM          1172  '1172'
           1184_1  COME_FROM          1114  '1114'
           1184_2  COME_FROM          1056  '1056'
           1184_3  COME_FROM           894  '894'
             1184  POP_BLOCK        

 L. 543      1186  LOAD_FAST                'self'
             1188  LOAD_ATTR                transport
             1190  LOAD_CONST               None
             1192  <117>                 0  ''
         1194_1196  POP_JUMP_IF_FALSE  1220  'to 1220'
             1198  LOAD_FAST                'resp'
             1200  LOAD_CONST               None
             1202  <117>                 1  ''
         1204_1206  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 544      1208  LOAD_FAST                'self'
             1210  LOAD_METHOD              log_debug
             1212  LOAD_STR                 'Ignored premature client disconnection.'
             1214  CALL_METHOD_1         1  ''
             1216  POP_TOP          
             1218  JUMP_FORWARD       1308  'to 1308'
           1220_0  COME_FROM          1204  '1204'
           1220_1  COME_FROM          1194  '1194'

 L. 545      1220  LOAD_FAST                'self'
             1222  LOAD_ATTR                _force_close
         1224_1226  POP_JUMP_IF_TRUE   1442  'to 1442'

 L. 546      1228  LOAD_FAST                'self'
             1230  LOAD_ATTR                _keepalive
         1232_1234  POP_JUMP_IF_FALSE  1444  'to 1444'
             1236  LOAD_FAST                'self'
             1238  LOAD_ATTR                _close
         1240_1242  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 548      1244  LOAD_FAST                'keepalive_timeout'
             1246  LOAD_CONST               None
             1248  <117>                 1  ''
         1250_1252  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 549      1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                _loop
             1258  LOAD_METHOD              time
             1260  CALL_METHOD_0         0  ''
             1262  STORE_FAST               'now'

 L. 550      1264  LOAD_FAST                'now'
             1266  LOAD_FAST                'self'
             1268  STORE_ATTR               _keepalive_time

 L. 551      1270  LOAD_FAST                'self'
             1272  LOAD_ATTR                _keepalive_handle
             1274  LOAD_CONST               None
             1276  <117>                 0  ''
         1278_1280  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 552      1282  LOAD_FAST                'loop'
             1284  LOAD_METHOD              call_at

 L. 553      1286  LOAD_FAST                'now'
             1288  LOAD_FAST                'keepalive_timeout'
             1290  BINARY_ADD       
             1292  LOAD_FAST                'self'
             1294  LOAD_ATTR                _process_keepalive

 L. 552      1296  CALL_METHOD_2         2  ''
             1298  LOAD_FAST                'self'
             1300  STORE_ATTR               _keepalive_handle
             1302  JUMP_FORWARD       1308  'to 1308'

 L. 556  1304_1306  BREAK_LOOP         1444  'to 1444'
           1308_0  COME_FROM          1302  '1302'
           1308_1  COME_FROM          1278  '1278'
           1308_2  COME_FROM          1250  '1250'
           1308_3  COME_FROM          1218  '1218'
             1308  JUMP_BACK            80  'to 80'
           1310_0  COME_FROM_FINALLY   240  '240'

 L. 543      1310  LOAD_FAST                'self'
             1312  LOAD_ATTR                transport
             1314  LOAD_CONST               None
             1316  <117>                 0  ''
         1318_1320  POP_JUMP_IF_FALSE  1344  'to 1344'
             1322  LOAD_FAST                'resp'
             1324  LOAD_CONST               None
             1326  <117>                 1  ''
         1328_1330  POP_JUMP_IF_FALSE  1344  'to 1344'

 L. 544      1332  LOAD_FAST                'self'
             1334  LOAD_METHOD              log_debug
             1336  LOAD_STR                 'Ignored premature client disconnection.'
             1338  CALL_METHOD_1         1  ''
             1340  POP_TOP          
             1342  JUMP_FORWARD       1440  'to 1440'
           1344_0  COME_FROM          1328  '1328'
           1344_1  COME_FROM          1318  '1318'

 L. 545      1344  LOAD_FAST                'self'
             1346  LOAD_ATTR                _force_close
         1348_1350  POP_JUMP_IF_TRUE   1440  'to 1440'

 L. 546      1352  LOAD_FAST                'self'
             1354  LOAD_ATTR                _keepalive
         1356_1358  POP_JUMP_IF_FALSE  1428  'to 1428'
             1360  LOAD_FAST                'self'
             1362  LOAD_ATTR                _close
         1364_1366  POP_JUMP_IF_TRUE   1428  'to 1428'

 L. 548      1368  LOAD_FAST                'keepalive_timeout'
             1370  LOAD_CONST               None
             1372  <117>                 1  ''
         1374_1376  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 549      1378  LOAD_FAST                'self'
             1380  LOAD_ATTR                _loop
             1382  LOAD_METHOD              time
             1384  CALL_METHOD_0         0  ''
             1386  STORE_FAST               'now'

 L. 550      1388  LOAD_FAST                'now'
             1390  LOAD_FAST                'self'
             1392  STORE_ATTR               _keepalive_time

 L. 551      1394  LOAD_FAST                'self'
             1396  LOAD_ATTR                _keepalive_handle
             1398  LOAD_CONST               None
             1400  <117>                 0  ''
         1402_1404  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 552      1406  LOAD_FAST                'loop'
             1408  LOAD_METHOD              call_at

 L. 553      1410  LOAD_FAST                'now'
             1412  LOAD_FAST                'keepalive_timeout'
             1414  BINARY_ADD       
             1416  LOAD_FAST                'self'
             1418  LOAD_ATTR                _process_keepalive

 L. 552      1420  CALL_METHOD_2         2  ''
             1422  LOAD_FAST                'self'
             1424  STORE_ATTR               _keepalive_handle
             1426  JUMP_FORWARD       1440  'to 1440'
           1428_0  COME_FROM          1364  '1364'
           1428_1  COME_FROM          1356  '1356'

 L. 556      1428  POP_TOP          
             1430  POP_TOP          
             1432  POP_TOP          
             1434  POP_EXCEPT       
         1436_1438  JUMP_ABSOLUTE      1444  'to 1444'
           1440_0  COME_FROM          1426  '1426'
           1440_1  COME_FROM          1402  '1402'
           1440_2  COME_FROM          1374  '1374'
           1440_3  COME_FROM          1348  '1348'
           1440_4  COME_FROM          1342  '1342'
             1440  <48>             
           1442_0  COME_FROM          1224  '1224'
             1442  JUMP_BACK            80  'to 80'
           1444_0  COME_FROM          1240  '1240'
           1444_1  COME_FROM          1232  '1232'
           1444_2  COME_FROM           982  '982'
           1444_3  COME_FROM           974  '974'
           1444_4  COME_FROM           966  '966'
           1444_5  COME_FROM           558  '558'
           1444_6  COME_FROM           550  '550'
           1444_7  COME_FROM           542  '542'
           1444_8  COME_FROM           378  '378'
           1444_9  COME_FROM           370  '370'
          1444_10  COME_FROM           362  '362'
          1444_11  COME_FROM            84  '84'

 L. 559      1444  LOAD_FAST                'self'
             1446  LOAD_ATTR                _force_close
         1448_1450  POP_JUMP_IF_TRUE   1492  'to 1492'

 L. 560      1452  LOAD_CONST               None
             1454  LOAD_FAST                'self'
             1456  STORE_ATTR               _task_handler

 L. 561      1458  LOAD_FAST                'self'
             1460  LOAD_ATTR                transport
             1462  LOAD_CONST               None
             1464  <117>                 1  ''
         1466_1468  POP_JUMP_IF_FALSE  1492  'to 1492'
             1470  LOAD_FAST                'self'
             1472  LOAD_ATTR                _error_handler
             1474  LOAD_CONST               None
             1476  <117>                 0  ''
         1478_1480  POP_JUMP_IF_FALSE  1492  'to 1492'

 L. 562      1482  LOAD_FAST                'self'
             1484  LOAD_ATTR                transport
             1486  LOAD_METHOD              close
             1488  CALL_METHOD_0         0  ''
             1490  POP_TOP          
           1492_0  COME_FROM          1478  '1478'
           1492_1  COME_FROM          1466  '1466'
           1492_2  COME_FROM          1448  '1448'

Parse error at or near `<117>' instruction at offset 16

    async def finish_response--- This code section failed: ---

 L. 573         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _request_parser
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'

 L. 574        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _request_parser
               14  LOAD_METHOD              set_upgraded
               16  LOAD_CONST               False
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 575        22  LOAD_CONST               False
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _upgrade

 L. 576        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _message_tail
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 577        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _request_parser
               38  LOAD_METHOD              feed_data
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _message_tail
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 578        48  LOAD_CONST               b''
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _message_tail
             54_0  COME_FROM            32  '32'
             54_1  COME_FROM             8  '8'

 L. 579        54  SETUP_FINALLY        66  'to 66'

 L. 580        56  LOAD_FAST                'resp'
               58  LOAD_ATTR                prepare
               60  STORE_FAST               'prepare_meth'
               62  POP_BLOCK        
               64  JUMP_FORWARD        116  'to 116'
             66_0  COME_FROM_FINALLY    54  '54'

 L. 581        66  DUP_TOP          
               68  LOAD_GLOBAL              AttributeError
               70  <121>               114  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 582        78  LOAD_FAST                'resp'
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L. 583        86  LOAD_GLOBAL              RuntimeError
               88  LOAD_STR                 'Missing return statement on request handler'
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
               94  JUMP_FORWARD        110  'to 110'
             96_0  COME_FROM            84  '84'

 L. 585        96  LOAD_GLOBAL              RuntimeError

 L. 586        98  LOAD_STR                 'Web-handler should return a response instance, got {!r}'
              100  LOAD_METHOD              format

 L. 588       102  LOAD_FAST                'resp'

 L. 586       104  CALL_METHOD_1         1  ''

 L. 585       106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            94  '94'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            64  '64'

 L. 590       116  SETUP_FINALLY       150  'to 150'

 L. 591       118  LOAD_FAST                'prepare_meth'
              120  LOAD_FAST                'request'
              122  CALL_FUNCTION_1       1  ''
              124  GET_AWAITABLE    
              126  LOAD_CONST               None
              128  YIELD_FROM       
              130  POP_TOP          

 L. 592       132  LOAD_FAST                'resp'
              134  LOAD_METHOD              write_eof
              136  CALL_METHOD_0         0  ''
              138  GET_AWAITABLE    
              140  LOAD_CONST               None
              142  YIELD_FROM       
              144  POP_TOP          
              146  POP_BLOCK        
              148  JUMP_FORWARD        184  'to 184'
            150_0  COME_FROM_FINALLY   116  '116'

 L. 593       150  DUP_TOP          
              152  LOAD_GLOBAL              ConnectionError
              154  <121>               182  ''
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 594       162  LOAD_FAST                'self'
              164  LOAD_METHOD              log_access
              166  LOAD_FAST                'request'
              168  LOAD_FAST                'resp'
              170  LOAD_FAST                'start_time'
              172  CALL_METHOD_3         3  ''
              174  POP_TOP          

 L. 595       176  POP_EXCEPT       
              178  LOAD_CONST               True
              180  RETURN_VALUE     
              182  <48>             
            184_0  COME_FROM           148  '148'

 L. 597       184  LOAD_FAST                'self'
              186  LOAD_METHOD              log_access
              188  LOAD_FAST                'request'
              190  LOAD_FAST                'resp'
              192  LOAD_FAST                'start_time'
              194  CALL_METHOD_3         3  ''
              196  POP_TOP          

 L. 598       198  LOAD_CONST               False
              200  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def handle_error--- This code section failed: ---

 L. 611         0  LOAD_FAST                'self'
                2  LOAD_ATTR                log_exception
                4  LOAD_STR                 'Error handling request'
                6  LOAD_FAST                'exc'
                8  LOAD_CONST               ('exc_info',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  POP_TOP          

 L. 613        14  LOAD_STR                 'text/plain'
               16  STORE_FAST               'ct'

 L. 614        18  LOAD_FAST                'status'
               20  LOAD_GLOBAL              HTTPStatus
               22  LOAD_ATTR                INTERNAL_SERVER_ERROR
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE   188  'to 188'

 L. 615        28  LOAD_STR                 '{0.value} {0.phrase}'
               30  LOAD_METHOD              format
               32  LOAD_GLOBAL              HTTPStatus
               34  LOAD_ATTR                INTERNAL_SERVER_ERROR
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'title'

 L. 616        40  LOAD_GLOBAL              HTTPStatus
               42  LOAD_ATTR                INTERNAL_SERVER_ERROR
               44  LOAD_ATTR                description
               46  STORE_FAST               'msg'

 L. 617        48  LOAD_CONST               None
               50  STORE_FAST               'tb'

 L. 618        52  LOAD_FAST                'self'
               54  LOAD_ATTR                debug
               56  POP_JUMP_IF_FALSE   106  'to 106'

 L. 619        58  LOAD_GLOBAL              suppress
               60  LOAD_GLOBAL              Exception
               62  CALL_FUNCTION_1       1  ''
               64  SETUP_WITH           90  'to 90'
               66  POP_TOP          

 L. 620        68  LOAD_GLOBAL              traceback
               70  LOAD_METHOD              format_exc
               72  CALL_METHOD_0         0  ''
               74  STORE_FAST               'tb'
               76  POP_BLOCK        
               78  LOAD_CONST               None
               80  DUP_TOP          
               82  DUP_TOP          
               84  CALL_FUNCTION_3       3  ''
               86  POP_TOP          
               88  JUMP_FORWARD        106  'to 106'
             90_0  COME_FROM_WITH       64  '64'
               90  <49>             
               92  POP_JUMP_IF_TRUE     96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          
              102  POP_EXCEPT       
              104  POP_TOP          
            106_0  COME_FROM            88  '88'
            106_1  COME_FROM            56  '56'

 L. 622       106  LOAD_STR                 'text/html'
              108  LOAD_FAST                'request'
              110  LOAD_ATTR                headers
              112  LOAD_METHOD              get
              114  LOAD_STR                 'Accept'
              116  LOAD_STR                 ''
              118  CALL_METHOD_2         2  ''
              120  <118>                 0  ''
              122  POP_JUMP_IF_FALSE   168  'to 168'

 L. 623       124  LOAD_FAST                'tb'
              126  POP_JUMP_IF_FALSE   148  'to 148'

 L. 624       128  LOAD_GLOBAL              html_escape
              130  LOAD_FAST                'tb'
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'tb'

 L. 625       136  LOAD_STR                 '<h2>Traceback:</h2>\n<pre>'
              138  LOAD_FAST                'tb'
              140  FORMAT_VALUE          0  ''
              142  LOAD_STR                 '</pre>'
              144  BUILD_STRING_3        3 
              146  STORE_FAST               'msg'
            148_0  COME_FROM           126  '126'

 L. 627       148  LOAD_STR                 '<html><head><title>{title}</title></head><body>\n<h1>{title}</h1>\n{msg}\n</body></html>\n'

 L. 626       150  LOAD_ATTR                format

 L. 631       152  LOAD_FAST                'title'
              154  LOAD_FAST                'msg'

 L. 626       156  LOAD_CONST               ('title', 'msg')
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  STORE_FAST               'message'

 L. 632       162  LOAD_STR                 'text/html'
              164  STORE_FAST               'ct'
              166  JUMP_FORWARD        188  'to 188'
            168_0  COME_FROM           122  '122'

 L. 634       168  LOAD_FAST                'tb'
              170  POP_JUMP_IF_FALSE   176  'to 176'

 L. 635       172  LOAD_FAST                'tb'
              174  STORE_FAST               'msg'
            176_0  COME_FROM           170  '170'

 L. 636       176  LOAD_FAST                'title'
              178  LOAD_STR                 '\n\n'
              180  BINARY_ADD       
              182  LOAD_FAST                'msg'
              184  BINARY_ADD       
              186  STORE_FAST               'message'
            188_0  COME_FROM           166  '166'
            188_1  COME_FROM            26  '26'

 L. 638       188  LOAD_GLOBAL              Response
              190  LOAD_FAST                'status'
              192  LOAD_FAST                'message'
              194  LOAD_FAST                'ct'
              196  LOAD_CONST               ('status', 'text', 'content_type')
              198  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              200  STORE_FAST               'resp'

 L. 639       202  LOAD_FAST                'resp'
              204  LOAD_METHOD              force_close
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          

 L. 642       210  LOAD_FAST                'request'
              212  LOAD_ATTR                writer
              214  LOAD_ATTR                output_size
              216  LOAD_CONST               0
              218  COMPARE_OP               >
              220  POP_JUMP_IF_TRUE    232  'to 232'
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                transport
              226  LOAD_CONST               None
              228  <117>                 0  ''
              230  POP_JUMP_IF_FALSE   240  'to 240'
            232_0  COME_FROM           220  '220'

 L. 643       232  LOAD_FAST                'self'
              234  LOAD_METHOD              force_close
              236  CALL_METHOD_0         0  ''
              238  POP_TOP          
            240_0  COME_FROM           230  '230'

 L. 645       240  LOAD_FAST                'resp'
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 80

    async def handle_parse_error--- This code section failed: ---

 L. 654         0  LOAD_GLOBAL              current_task
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'task'

 L. 655         6  LOAD_FAST                'task'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 656        18  LOAD_GLOBAL              BaseRequest

 L. 657        20  LOAD_GLOBAL              ERROR
               22  LOAD_GLOBAL              EMPTY_PAYLOAD
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'writer'
               28  LOAD_FAST                'task'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _loop

 L. 656        34  CALL_FUNCTION_6       6  ''
               36  STORE_FAST               'request'

 L. 660        38  LOAD_FAST                'self'
               40  LOAD_METHOD              handle_error
               42  LOAD_FAST                'request'
               44  LOAD_FAST                'status'
               46  LOAD_FAST                'exc'
               48  LOAD_FAST                'message'
               50  CALL_METHOD_4         4  ''
               52  STORE_FAST               'resp'

 L. 661        54  LOAD_FAST                'resp'
               56  LOAD_METHOD              prepare
               58  LOAD_FAST                'request'
               60  CALL_METHOD_1         1  ''
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  POP_TOP          

 L. 662        70  LOAD_FAST                'resp'
               72  LOAD_METHOD              write_eof
               74  CALL_METHOD_0         0  ''
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  POP_TOP          

 L. 664        84  LOAD_FAST                'self'
               86  LOAD_ATTR                transport
               88  LOAD_CONST               None
               90  <117>                 1  ''
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 665        94  LOAD_FAST                'self'
               96  LOAD_ATTR                transport
               98  LOAD_METHOD              close
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          
            104_0  COME_FROM            92  '92'

 L. 667       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _error_handler

Parse error at or near `<117>' instruction at offset 10