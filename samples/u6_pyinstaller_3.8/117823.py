# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\web_protocol.py
import asyncio, asyncio.streams, traceback, warnings
from collections import deque
from contextlib import suppress
from html import escape as html_escape
from http import HTTPStatus
from logging import Logger
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Type, cast
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
 [RawRequestMessage,
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
                 '_close', '_force_close')

    def __init__(self, manager, *, loop, keepalive_timeout=75.0, tcp_keepalive=True, logger=server_logger, access_log_class=AccessLogger, access_log=access_logger, access_log_format=AccessLogger.LOG_FORMAT, debug=False, max_line_size=8190, max_headers=32768, max_field_size=8190, lingering_time=10.0):
        super().__init__(loop)
        self._request_count = 0
        self._keepalive = False
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
          loop, max_line_size=max_line_size,
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

    def __repr__(self) -> str:
        return '<{} {}>'.format(self.__class__.__name__, 'connected' if self.transport is not None else 'disconnected')

    @property
    def keepalive_timeout(self) -> float:
        return self._keepalive_timeout

    async def shutdown(self, timeout: Optional[float]=15.0) -> None:
        """Worker process is about to exit, we need cleanup everything and
        stop accepting requests. It is especially important for keep-alive
        connections."""
        self._force_close = True
        if self._keepalive_handle is not None:
            self._keepalive_handle.cancel()
        if self._waiter:
            self._waiter.cancel()
        with suppress(asyncio.CancelledError, asyncio.TimeoutError):
            with CeilTimeout(timeout, loop=(self._loop)):
                if self._error_handler is not None:
                    if not self._error_handler.done():
                        await self._error_handler
                if self._task_handler is not None:
                    if not self._task_handler.done():
                        await self._task_handler
        if self._task_handler is not None:
            self._task_handler.cancel()
        if self.transport is not None:
            self.transport.close()
            self.transport = None

    def connection_made(self, transport):
        super().connection_made(transport)
        real_transport = cast(asyncio.Transport, transport)
        if self._tcp_keepalive:
            tcp_keepalive(real_transport)
        self._task_handler = self._loop.create_task(self.start())
        assert self._manager is not None
        self._manager.connection_made(self, real_transport)

    def connection_lost(self, exc):
        if self._manager is None:
            return
        self._manager.connection_lost(self, exc)
        super().connection_lost(exc)
        self._manager = None
        self._force_close = True
        self._request_factory = None
        self._request_handler = None
        self._request_parser = None
        if self._keepalive_handle is not None:
            self._keepalive_handle.cancel()
        if self._task_handler is not None:
            self._task_handler.cancel()
        if self._error_handler is not None:
            self._error_handler.cancel()
        self._task_handler = None
        if self._payload_parser is not None:
            self._payload_parser.feed_eof()
            self._payload_parser = None

    def set_parser(self, parser: Any) -> None:
        assert self._payload_parser is None
        self._payload_parser = parser
        if self._message_tail:
            self._payload_parser.feed_data(self._message_tail)
            self._message_tail = b''

    def eof_received(self) -> None:
        pass

    def data_received(self, data: bytes) -> None:
        if not self._force_close:
            if self._close:
                return
            if self._payload_parser is None and not self._upgrade:
                assert self._request_parser is not None
                try:
                    messages, upgraded, tail = self._request_parser.feed_data(data)
                except HttpProcessingError as exc:
                    try:
                        self._error_handler = self._loop.create_task(self.handle_parse_error(StreamWriter(self, self._loop), 400, exc, exc.message))
                        self.close()
                    finally:
                        exc = None
                        del exc

                except Exception as exc:
                    try:
                        self._error_handler = self._loop.create_task(self.handle_parse_error(StreamWriter(self, self._loop), 500, exc))
                        self.close()
                    finally:
                        exc = None
                        del exc

                else:
                    if messages:
                        for msg, payload in messages:
                            self._request_count += 1
                            self._messages.append((msg, payload))
                        else:
                            waiter = self._waiter

                        if waiter is not None:
                            if not waiter.done():
                                waiter.set_result(None)
                    self._upgrade = upgraded
                if upgraded:
                    if tail:
                        self._message_tail = tail
        elif self._payload_parser is None and self._upgrade and data:
            self._message_tail += data
        else:
            if data:
                eof, tail = self._payload_parser.feed_data(data)
                if eof:
                    self.close()

    def keep_alive(self, val: bool) -> None:
        """Set keep-alive connection mode.

        :param bool val: new state.
        """
        self._keepalive = val
        if self._keepalive_handle:
            self._keepalive_handle.cancel()
            self._keepalive_handle = None

    def close(self) -> None:
        """Stop accepting new pipelinig messages and close
        connection when handlers done processing messages"""
        self._close = True
        if self._waiter:
            self._waiter.cancel()

    def force_close(self) -> None:
        """Force close connection"""
        self._force_close = True
        if self._waiter:
            self._waiter.cancel()
        if self.transport is not None:
            self.transport.close()
            self.transport = None

    def log_access(self, request: BaseRequest, response: StreamResponse, time: float) -> None:
        if self.access_logger is not None:
            self.access_logger.log(request, response, time)

    def log_debug(self, *args: Any, **kw: Any) -> None:
        if self.debug:
            (self.logger.debug)(*args, **kw)

    def log_exception(self, *args: Any, **kw: Any) -> None:
        (self.logger.exception)(*args, **kw)

    def _process_keepalive(self) -> None:
        return self._force_close or self._keepalive or None
        next = self._keepalive_time + self._keepalive_timeout
        if self._waiter:
            if self._loop.time() > next:
                self.force_close()
                return None
        self._keepalive_handle = self._loop.call_later(self.KEEPALIVE_RESCHEDULE_DELAY, self._process_keepalive)

    async def start--- This code section failed: ---

 L. 383         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  STORE_FAST               'loop'

 L. 384         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _task_handler
               10  STORE_FAST               'handler'

 L. 385        12  LOAD_FAST                'handler'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  LOAD_ASSERT              AssertionError
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 386        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _manager
               28  STORE_FAST               'manager'

 L. 387        30  LOAD_FAST                'manager'
               32  LOAD_CONST               None
               34  COMPARE_OP               is-not
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  LOAD_ASSERT              AssertionError
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L. 388        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _keepalive_timeout
               46  STORE_FAST               'keepalive_timeout'

 L. 389        48  LOAD_CONST               None
               50  STORE_FAST               'resp'

 L. 390        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _request_factory
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  LOAD_ASSERT              AssertionError
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L. 391        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _request_handler
               70  LOAD_CONST               None
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_TRUE     80  'to 80'
               76  LOAD_ASSERT              AssertionError
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            74  '74'

 L. 393        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _force_close
            84_86  POP_JUMP_IF_TRUE   1270  'to 1270'

 L. 394        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _messages
               92  POP_JUMP_IF_TRUE    168  'to 168'

 L. 395        94  SETUP_FINALLY       160  'to 160'
               96  SETUP_FINALLY       124  'to 124'

 L. 397        98  LOAD_FAST                'loop'
              100  LOAD_METHOD              create_future
              102  CALL_METHOD_0         0  ''
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _waiter

 L. 398       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _waiter
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        156  'to 156'
            124_0  COME_FROM_FINALLY    96  '96'

 L. 399       124  DUP_TOP          
              126  LOAD_GLOBAL              asyncio
              128  LOAD_ATTR                CancelledError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   154  'to 154'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 400       140  POP_EXCEPT       
              142  POP_BLOCK        
              144  CALL_FINALLY        160  'to 160'
          146_148  JUMP_ABSOLUTE      1270  'to 1270'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           132  '132'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           122  '122'
              156  POP_BLOCK        
              158  BEGIN_FINALLY    
            160_0  COME_FROM           144  '144'
            160_1  COME_FROM_FINALLY    94  '94'

 L. 402       160  LOAD_CONST               None
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _waiter
              166  END_FINALLY      
            168_0  COME_FROM            92  '92'

 L. 404       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _messages
              172  LOAD_METHOD              popleft
              174  CALL_METHOD_0         0  ''
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'message'
              180  STORE_FAST               'payload'

 L. 406       182  LOAD_FAST                'self'
              184  LOAD_ATTR                access_log
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L. 407       188  LOAD_FAST                'loop'
              190  LOAD_METHOD              time
              192  CALL_METHOD_0         0  ''
              194  STORE_FAST               'now'
            196_0  COME_FROM           186  '186'

 L. 409       196  LOAD_FAST                'manager'
              198  DUP_TOP          
              200  LOAD_ATTR                requests_count
              202  LOAD_CONST               1
              204  INPLACE_ADD      
              206  ROT_TWO          
              208  STORE_ATTR               requests_count

 L. 410       210  LOAD_GLOBAL              StreamWriter
              212  LOAD_FAST                'self'
              214  LOAD_FAST                'loop'
              216  CALL_FUNCTION_2       2  ''
              218  STORE_FAST               'writer'

 L. 411       220  LOAD_FAST                'self'
              222  LOAD_METHOD              _request_factory

 L. 412       224  LOAD_FAST                'message'

 L. 412       226  LOAD_FAST                'payload'

 L. 412       228  LOAD_FAST                'self'

 L. 412       230  LOAD_FAST                'writer'

 L. 412       232  LOAD_FAST                'handler'

 L. 411       234  CALL_METHOD_5         5  ''
              236  STORE_FAST               'request'

 L. 413       238  LOAD_CONST               None
          240_242  SETUP_FINALLY      1138  'to 1138'
          244_246  SETUP_FINALLY       968  'to 968'

 L. 415       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _loop
              252  LOAD_METHOD              create_task

 L. 416       254  LOAD_FAST                'self'
              256  LOAD_METHOD              _request_handler
              258  LOAD_FAST                'request'
              260  CALL_METHOD_1         1  ''

 L. 415       262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'task'

 L. 417       266  SETUP_FINALLY       282  'to 282'

 L. 418       268  LOAD_FAST                'task'
              270  GET_AWAITABLE    
              272  LOAD_CONST               None
              274  YIELD_FROM       
              276  STORE_FAST               'resp'
              278  POP_BLOCK        
              280  JUMP_FORWARD        484  'to 484'
            282_0  COME_FROM_FINALLY   266  '266'

 L. 419       282  DUP_TOP          
              284  LOAD_GLOBAL              HTTPException
              286  COMPARE_OP               exception-match
          288_290  POP_JUMP_IF_FALSE   320  'to 320'
              292  POP_TOP          
              294  STORE_FAST               'exc'
              296  POP_TOP          
              298  SETUP_FINALLY       308  'to 308'

 L. 420       300  LOAD_FAST                'exc'
              302  STORE_FAST               'resp'
              304  POP_BLOCK        
              306  BEGIN_FINALLY    
            308_0  COME_FROM_FINALLY   298  '298'
              308  LOAD_CONST               None
              310  STORE_FAST               'exc'
              312  DELETE_FAST              'exc'
              314  END_FINALLY      
              316  POP_EXCEPT       
              318  JUMP_FORWARD        510  'to 510'
            320_0  COME_FROM           288  '288'

 L. 421       320  DUP_TOP          
              322  LOAD_GLOBAL              asyncio
              324  LOAD_ATTR                CancelledError
              326  LOAD_GLOBAL              ConnectionError
              328  BUILD_TUPLE_2         2 
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   372  'to 372'
              336  POP_TOP          
              338  POP_TOP          
              340  POP_TOP          

 L. 422       342  LOAD_FAST                'self'
              344  LOAD_METHOD              log_debug
              346  LOAD_STR                 'Ignored premature client disconnection'
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          

 L. 423       352  POP_EXCEPT       
              354  POP_BLOCK        
              356  POP_BLOCK        
          358_360  CALL_FINALLY       1138  'to 1138'
              362  POP_TOP          
          364_366  JUMP_ABSOLUTE      1270  'to 1270'
              368  POP_EXCEPT       
              370  JUMP_FORWARD        510  'to 510'
            372_0  COME_FROM           332  '332'

 L. 424       372  DUP_TOP          
              374  LOAD_GLOBAL              asyncio
              376  LOAD_ATTR                TimeoutError
              378  COMPARE_OP               exception-match
          380_382  POP_JUMP_IF_FALSE   434  'to 434'
              384  POP_TOP          
              386  STORE_FAST               'exc'
              388  POP_TOP          
              390  SETUP_FINALLY       422  'to 422'

 L. 425       392  LOAD_FAST                'self'
              394  LOAD_ATTR                log_debug
              396  LOAD_STR                 'Request handler timed out.'
              398  LOAD_FAST                'exc'
              400  LOAD_CONST               ('exc_info',)
              402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              404  POP_TOP          

 L. 426       406  LOAD_FAST                'self'
              408  LOAD_METHOD              handle_error
              410  LOAD_FAST                'request'
              412  LOAD_CONST               504
              414  CALL_METHOD_2         2  ''
              416  STORE_FAST               'resp'
              418  POP_BLOCK        
              420  BEGIN_FINALLY    
            422_0  COME_FROM_FINALLY   390  '390'
              422  LOAD_CONST               None
              424  STORE_FAST               'exc'
              426  DELETE_FAST              'exc'
              428  END_FINALLY      
              430  POP_EXCEPT       
              432  JUMP_FORWARD        510  'to 510'
            434_0  COME_FROM           380  '380'

 L. 427       434  DUP_TOP          
              436  LOAD_GLOBAL              Exception
              438  COMPARE_OP               exception-match
          440_442  POP_JUMP_IF_FALSE   482  'to 482'
              444  POP_TOP          
              446  STORE_FAST               'exc'
              448  POP_TOP          
              450  SETUP_FINALLY       470  'to 470'

 L. 428       452  LOAD_FAST                'self'
              454  LOAD_METHOD              handle_error
              456  LOAD_FAST                'request'
              458  LOAD_CONST               500
              460  LOAD_FAST                'exc'
              462  CALL_METHOD_3         3  ''
              464  STORE_FAST               'resp'
              466  POP_BLOCK        
              468  BEGIN_FINALLY    
            470_0  COME_FROM_FINALLY   450  '450'
              470  LOAD_CONST               None
              472  STORE_FAST               'exc'
              474  DELETE_FAST              'exc'
              476  END_FINALLY      
              478  POP_EXCEPT       
              480  JUMP_FORWARD        510  'to 510'
            482_0  COME_FROM           440  '440'
              482  END_FINALLY      
            484_0  COME_FROM           280  '280'

 L. 431       484  LOAD_GLOBAL              getattr
              486  LOAD_FAST                'resp'
              488  LOAD_STR                 '__http_exception__'
              490  LOAD_CONST               False
              492  CALL_FUNCTION_3       3  ''
          494_496  POP_JUMP_IF_FALSE   510  'to 510'

 L. 432       498  LOAD_GLOBAL              warnings
              500  LOAD_METHOD              warn

 L. 433       502  LOAD_STR                 'returning HTTPException object is deprecated (#2415) and will be removed, please raise the exception instead'

 L. 436       504  LOAD_GLOBAL              DeprecationWarning

 L. 432       506  CALL_METHOD_2         2  ''
              508  POP_TOP          
            510_0  COME_FROM           494  '494'
            510_1  COME_FROM           480  '480'
            510_2  COME_FROM           432  '432'
            510_3  COME_FROM           370  '370'
            510_4  COME_FROM           318  '318'

 L. 439       510  DELETE_FAST              'task'

 L. 441       512  LOAD_FAST                'self'
              514  LOAD_ATTR                debug
          516_518  POP_JUMP_IF_FALSE   566  'to 566'

 L. 442       520  LOAD_GLOBAL              isinstance
              522  LOAD_FAST                'resp'
              524  LOAD_GLOBAL              StreamResponse
              526  CALL_FUNCTION_2       2  ''
          528_530  POP_JUMP_IF_TRUE    566  'to 566'

 L. 443       532  LOAD_FAST                'resp'
              534  LOAD_CONST               None
              536  COMPARE_OP               is
          538_540  POP_JUMP_IF_FALSE   552  'to 552'

 L. 444       542  LOAD_GLOBAL              RuntimeError
              544  LOAD_STR                 'Missing return statement on request handler'
              546  CALL_FUNCTION_1       1  ''
              548  RAISE_VARARGS_1       1  'exception instance'
              550  JUMP_FORWARD        566  'to 566'
            552_0  COME_FROM           538  '538'

 L. 447       552  LOAD_GLOBAL              RuntimeError
              554  LOAD_STR                 'Web-handler should return a response instance, got {!r}'
              556  LOAD_METHOD              format

 L. 449       558  LOAD_FAST                'resp'

 L. 447       560  CALL_METHOD_1         1  ''
              562  CALL_FUNCTION_1       1  ''
              564  RAISE_VARARGS_1       1  'exception instance'
            566_0  COME_FROM           550  '550'
            566_1  COME_FROM           528  '528'
            566_2  COME_FROM           516  '516'

 L. 450       566  SETUP_FINALLY       578  'to 578'

 L. 451       568  LOAD_FAST                'resp'
              570  LOAD_ATTR                prepare
              572  STORE_FAST               'prepare_meth'
              574  POP_BLOCK        
              576  JUMP_FORWARD        634  'to 634'
            578_0  COME_FROM_FINALLY   566  '566'

 L. 452       578  DUP_TOP          
              580  LOAD_GLOBAL              AttributeError
              582  COMPARE_OP               exception-match
          584_586  POP_JUMP_IF_FALSE   632  'to 632'
              588  POP_TOP          
              590  POP_TOP          
              592  POP_TOP          

 L. 453       594  LOAD_FAST                'resp'
              596  LOAD_CONST               None
              598  COMPARE_OP               is
          600_602  POP_JUMP_IF_FALSE   614  'to 614'

 L. 454       604  LOAD_GLOBAL              RuntimeError
              606  LOAD_STR                 'Missing return statement on request handler'
              608  CALL_FUNCTION_1       1  ''
              610  RAISE_VARARGS_1       1  'exception instance'
              612  JUMP_FORWARD        628  'to 628'
            614_0  COME_FROM           600  '600'

 L. 457       614  LOAD_GLOBAL              RuntimeError
              616  LOAD_STR                 'Web-handler should return a response instance, got {!r}'
              618  LOAD_METHOD              format

 L. 459       620  LOAD_FAST                'resp'

 L. 457       622  CALL_METHOD_1         1  ''
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           612  '612'
              628  POP_EXCEPT       
              630  JUMP_FORWARD        634  'to 634'
            632_0  COME_FROM           584  '584'
              632  END_FINALLY      
            634_0  COME_FROM           630  '630'
            634_1  COME_FROM           576  '576'

 L. 460       634  SETUP_FINALLY       668  'to 668'

 L. 461       636  LOAD_FAST                'prepare_meth'
              638  LOAD_FAST                'request'
              640  CALL_FUNCTION_1       1  ''
              642  GET_AWAITABLE    
              644  LOAD_CONST               None
              646  YIELD_FROM       
              648  POP_TOP          

 L. 462       650  LOAD_FAST                'resp'
              652  LOAD_METHOD              write_eof
              654  CALL_METHOD_0         0  ''
              656  GET_AWAITABLE    
              658  LOAD_CONST               None
              660  YIELD_FROM       
              662  POP_TOP          
              664  POP_BLOCK        
              666  JUMP_FORWARD        716  'to 716'
            668_0  COME_FROM_FINALLY   634  '634'

 L. 463       668  DUP_TOP          
              670  LOAD_GLOBAL              ConnectionError
              672  COMPARE_OP               exception-match
          674_676  POP_JUMP_IF_FALSE   714  'to 714'
              678  POP_TOP          
              680  POP_TOP          
              682  POP_TOP          

 L. 464       684  LOAD_FAST                'self'
              686  LOAD_METHOD              log_debug
              688  LOAD_STR                 'Ignored premature client disconnection 2'
              690  CALL_METHOD_1         1  ''
              692  POP_TOP          

 L. 465       694  POP_EXCEPT       
              696  POP_BLOCK        
              698  POP_BLOCK        
          700_702  CALL_FINALLY       1138  'to 1138'
              704  POP_TOP          
          706_708  JUMP_ABSOLUTE      1270  'to 1270'
              710  POP_EXCEPT       
              712  JUMP_FORWARD        716  'to 716'
            714_0  COME_FROM           674  '674'
              714  END_FINALLY      
            716_0  COME_FROM           712  '712'
            716_1  COME_FROM           666  '666'

 L. 468       716  LOAD_GLOBAL              bool
              718  LOAD_FAST                'resp'
              720  LOAD_ATTR                keep_alive
              722  CALL_FUNCTION_1       1  ''
              724  LOAD_FAST                'self'
              726  STORE_ATTR               _keepalive

 L. 471       728  LOAD_FAST                'self'
              730  LOAD_ATTR                access_log
          732_734  POP_JUMP_IF_FALSE   758  'to 758'

 L. 472       736  LOAD_FAST                'self'
              738  LOAD_METHOD              log_access
              740  LOAD_FAST                'request'
              742  LOAD_FAST                'resp'
              744  LOAD_FAST                'loop'
              746  LOAD_METHOD              time
              748  CALL_METHOD_0         0  ''
              750  LOAD_FAST                'now'
              752  BINARY_SUBTRACT  
              754  CALL_METHOD_3         3  ''
              756  POP_TOP          
            758_0  COME_FROM           732  '732'

 L. 475       758  LOAD_FAST                'payload'
              760  LOAD_METHOD              is_eof
              762  CALL_METHOD_0         0  ''
          764_766  POP_JUMP_IF_TRUE    952  'to 952'

 L. 476       768  LOAD_FAST                'self'
              770  LOAD_ATTR                _lingering_time
              772  STORE_FAST               'lingering_time'

 L. 477       774  LOAD_FAST                'self'
              776  LOAD_ATTR                _force_close
          778_780  POP_JUMP_IF_TRUE    916  'to 916'
              782  LOAD_FAST                'lingering_time'
          784_786  POP_JUMP_IF_FALSE   916  'to 916'

 L. 478       788  LOAD_FAST                'self'
              790  LOAD_METHOD              log_debug

 L. 479       792  LOAD_STR                 'Start lingering close timer for %s sec.'

 L. 480       794  LOAD_FAST                'lingering_time'

 L. 478       796  CALL_METHOD_2         2  ''
              798  POP_TOP          

 L. 482       800  LOAD_FAST                'loop'
              802  LOAD_METHOD              time
              804  CALL_METHOD_0         0  ''
              806  STORE_FAST               'now'

 L. 483       808  LOAD_FAST                'now'
              810  LOAD_FAST                'lingering_time'
              812  BINARY_ADD       
              814  STORE_FAST               'end_t'

 L. 485       816  LOAD_GLOBAL              suppress

 L. 486       818  LOAD_GLOBAL              asyncio
              820  LOAD_ATTR                TimeoutError

 L. 486       822  LOAD_GLOBAL              asyncio
              824  LOAD_ATTR                CancelledError

 L. 485       826  CALL_FUNCTION_2       2  ''
              828  SETUP_WITH          910  'to 910'
              830  POP_TOP          

 L. 487       832  LOAD_FAST                'payload'
              834  LOAD_METHOD              is_eof
              836  CALL_METHOD_0         0  ''
          838_840  POP_JUMP_IF_TRUE    906  'to 906'
              842  LOAD_FAST                'now'
              844  LOAD_FAST                'end_t'
              846  COMPARE_OP               <
          848_850  POP_JUMP_IF_FALSE   906  'to 906'

 L. 488       852  LOAD_GLOBAL              CeilTimeout
              854  LOAD_FAST                'end_t'
              856  LOAD_FAST                'now'
              858  BINARY_SUBTRACT  
              860  LOAD_FAST                'loop'
              862  LOAD_CONST               ('loop',)
              864  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              866  SETUP_WITH          888  'to 888'
              868  POP_TOP          

 L. 490       870  LOAD_FAST                'payload'
              872  LOAD_METHOD              readany
              874  CALL_METHOD_0         0  ''
              876  GET_AWAITABLE    
              878  LOAD_CONST               None
              880  YIELD_FROM       
              882  POP_TOP          
              884  POP_BLOCK        
              886  BEGIN_FINALLY    
            888_0  COME_FROM_WITH      866  '866'
              888  WITH_CLEANUP_START
              890  WITH_CLEANUP_FINISH
              892  END_FINALLY      

 L. 491       894  LOAD_FAST                'loop'
              896  LOAD_METHOD              time
              898  CALL_METHOD_0         0  ''
              900  STORE_FAST               'now'
          902_904  JUMP_BACK           832  'to 832'
            906_0  COME_FROM           848  '848'
            906_1  COME_FROM           838  '838'
              906  POP_BLOCK        
              908  BEGIN_FINALLY    
            910_0  COME_FROM_WITH      828  '828'
              910  WITH_CLEANUP_START
              912  WITH_CLEANUP_FINISH
              914  END_FINALLY      
            916_0  COME_FROM           784  '784'
            916_1  COME_FROM           778  '778'

 L. 494       916  LOAD_FAST                'payload'
              918  LOAD_METHOD              is_eof
              920  CALL_METHOD_0         0  ''
          922_924  POP_JUMP_IF_TRUE    952  'to 952'
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                _force_close
          930_932  POP_JUMP_IF_TRUE    952  'to 952'

 L. 495       934  LOAD_FAST                'self'
              936  LOAD_METHOD              log_debug
              938  LOAD_STR                 'Uncompleted request.'
              940  CALL_METHOD_1         1  ''
              942  POP_TOP          

 L. 496       944  LOAD_FAST                'self'
              946  LOAD_METHOD              close
              948  CALL_METHOD_0         0  ''
              950  POP_TOP          
            952_0  COME_FROM           930  '930'
            952_1  COME_FROM           922  '922'
            952_2  COME_FROM           764  '764'

 L. 498       952  LOAD_FAST                'payload'
              954  LOAD_METHOD              set_exception
              956  LOAD_GLOBAL              PayloadAccessError
              958  CALL_FUNCTION_0       0  ''
              960  CALL_METHOD_1         1  ''
              962  POP_TOP          
              964  POP_BLOCK        
              966  JUMP_FORWARD       1134  'to 1134'
            968_0  COME_FROM_FINALLY   244  '244'

 L. 500       968  DUP_TOP          
              970  LOAD_GLOBAL              asyncio
              972  LOAD_ATTR                CancelledError
              974  COMPARE_OP               exception-match
          976_978  POP_JUMP_IF_FALSE  1012  'to 1012'
              980  POP_TOP          
              982  POP_TOP          
              984  POP_TOP          

 L. 501       986  LOAD_FAST                'self'
              988  LOAD_METHOD              log_debug
              990  LOAD_STR                 'Ignored premature client disconnection '
              992  CALL_METHOD_1         1  ''
              994  POP_TOP          

 L. 502       996  POP_EXCEPT       
              998  POP_BLOCK        
             1000  CALL_FINALLY       1138  'to 1138'
             1002  POP_TOP          
         1004_1006  JUMP_ABSOLUTE      1270  'to 1270'
             1008  POP_EXCEPT       
             1010  JUMP_FORWARD       1134  'to 1134'
           1012_0  COME_FROM           976  '976'

 L. 503      1012  DUP_TOP          
             1014  LOAD_GLOBAL              RuntimeError
             1016  COMPARE_OP               exception-match
         1018_1020  POP_JUMP_IF_FALSE  1076  'to 1076'
             1022  POP_TOP          
             1024  STORE_FAST               'exc'
             1026  POP_TOP          
             1028  SETUP_FINALLY      1064  'to 1064'

 L. 504      1030  LOAD_FAST                'self'
             1032  LOAD_ATTR                debug
         1034_1036  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 505      1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                log_exception

 L. 506      1042  LOAD_STR                 'Unhandled runtime exception'

 L. 506      1044  LOAD_FAST                'exc'

 L. 505      1046  LOAD_CONST               ('exc_info',)
             1048  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1050  POP_TOP          
           1052_0  COME_FROM          1034  '1034'

 L. 507      1052  LOAD_FAST                'self'
             1054  LOAD_METHOD              force_close
             1056  CALL_METHOD_0         0  ''
             1058  POP_TOP          
             1060  POP_BLOCK        
             1062  BEGIN_FINALLY    
           1064_0  COME_FROM_FINALLY  1028  '1028'
             1064  LOAD_CONST               None
             1066  STORE_FAST               'exc'
             1068  DELETE_FAST              'exc'
             1070  END_FINALLY      
             1072  POP_EXCEPT       
             1074  JUMP_FORWARD       1134  'to 1134'
           1076_0  COME_FROM          1018  '1018'

 L. 508      1076  DUP_TOP          
             1078  LOAD_GLOBAL              Exception
             1080  COMPARE_OP               exception-match
         1082_1084  POP_JUMP_IF_FALSE  1132  'to 1132'
             1086  POP_TOP          
             1088  STORE_FAST               'exc'
             1090  POP_TOP          
             1092  SETUP_FINALLY      1120  'to 1120'

 L. 509      1094  LOAD_FAST                'self'
             1096  LOAD_ATTR                log_exception
             1098  LOAD_STR                 'Unhandled exception'
             1100  LOAD_FAST                'exc'
             1102  LOAD_CONST               ('exc_info',)
             1104  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1106  POP_TOP          

 L. 510      1108  LOAD_FAST                'self'
             1110  LOAD_METHOD              force_close
             1112  CALL_METHOD_0         0  ''
             1114  POP_TOP          
             1116  POP_BLOCK        
             1118  BEGIN_FINALLY    
           1120_0  COME_FROM_FINALLY  1092  '1092'
             1120  LOAD_CONST               None
             1122  STORE_FAST               'exc'
             1124  DELETE_FAST              'exc'
             1126  END_FINALLY      
             1128  POP_EXCEPT       
             1130  JUMP_FORWARD       1134  'to 1134'
           1132_0  COME_FROM          1082  '1082'
             1132  END_FINALLY      
           1134_0  COME_FROM          1130  '1130'
           1134_1  COME_FROM          1074  '1074'
           1134_2  COME_FROM          1010  '1010'
           1134_3  COME_FROM           966  '966'
             1134  POP_BLOCK        
             1136  BEGIN_FINALLY    
           1138_0  COME_FROM          1000  '1000'
           1138_1  COME_FROM           700  '700'
           1138_2  COME_FROM           358  '358'
           1138_3  COME_FROM_FINALLY   240  '240'

 L. 512      1138  LOAD_FAST                'self'
             1140  LOAD_ATTR                transport
             1142  LOAD_CONST               None
             1144  COMPARE_OP               is
         1146_1148  POP_JUMP_IF_FALSE  1172  'to 1172'
             1150  LOAD_FAST                'resp'
             1152  LOAD_CONST               None
             1154  COMPARE_OP               is-not
         1156_1158  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 513      1160  LOAD_FAST                'self'
             1162  LOAD_METHOD              log_debug
             1164  LOAD_STR                 'Ignored premature client disconnection.'
             1166  CALL_METHOD_1         1  ''
             1168  POP_TOP          
             1170  JUMP_FORWARD       1264  'to 1264'
           1172_0  COME_FROM          1156  '1156'
           1172_1  COME_FROM          1146  '1146'

 L. 514      1172  LOAD_FAST                'self'
             1174  LOAD_ATTR                _force_close
         1176_1178  POP_JUMP_IF_TRUE   1264  'to 1264'

 L. 515      1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                _keepalive
         1184_1186  POP_JUMP_IF_FALSE  1256  'to 1256'
             1188  LOAD_FAST                'self'
             1190  LOAD_ATTR                _close
         1192_1194  POP_JUMP_IF_TRUE   1256  'to 1256'

 L. 517      1196  LOAD_FAST                'keepalive_timeout'
             1198  LOAD_CONST               None
             1200  COMPARE_OP               is-not
         1202_1204  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 518      1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                _loop
             1210  LOAD_METHOD              time
             1212  CALL_METHOD_0         0  ''
             1214  STORE_FAST               'now'

 L. 519      1216  LOAD_FAST                'now'
             1218  LOAD_FAST                'self'
             1220  STORE_ATTR               _keepalive_time

 L. 520      1222  LOAD_FAST                'self'
             1224  LOAD_ATTR                _keepalive_handle
             1226  LOAD_CONST               None
             1228  COMPARE_OP               is
         1230_1232  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 521      1234  LOAD_FAST                'loop'
             1236  LOAD_METHOD              call_at

 L. 522      1238  LOAD_FAST                'now'
             1240  LOAD_FAST                'keepalive_timeout'
             1242  BINARY_ADD       

 L. 523      1244  LOAD_FAST                'self'
             1246  LOAD_ATTR                _process_keepalive

 L. 521      1248  CALL_METHOD_2         2  ''
             1250  LOAD_FAST                'self'
             1252  STORE_ATTR               _keepalive_handle
             1254  JUMP_FORWARD       1264  'to 1264'
           1256_0  COME_FROM          1192  '1192'
           1256_1  COME_FROM          1184  '1184'

 L. 525      1256  POP_FINALLY           0  ''
             1258  POP_TOP          
         1260_1262  JUMP_ABSOLUTE      1270  'to 1270'
           1264_0  COME_FROM          1254  '1254'
           1264_1  COME_FROM          1230  '1230'
           1264_2  COME_FROM          1202  '1202'
           1264_3  COME_FROM          1176  '1176'
           1264_4  COME_FROM          1170  '1170'
             1264  END_FINALLY      
             1266  POP_TOP          
             1268  JUMP_BACK            80  'to 80'
           1270_0  COME_FROM            84  '84'

 L. 528      1270  LOAD_FAST                'self'
             1272  LOAD_ATTR                _force_close
         1274_1276  POP_JUMP_IF_TRUE   1318  'to 1318'

 L. 529      1278  LOAD_CONST               None
             1280  LOAD_FAST                'self'
             1282  STORE_ATTR               _task_handler

 L. 530      1284  LOAD_FAST                'self'
             1286  LOAD_ATTR                transport
             1288  LOAD_CONST               None
             1290  COMPARE_OP               is-not
         1292_1294  POP_JUMP_IF_FALSE  1318  'to 1318'
             1296  LOAD_FAST                'self'
             1298  LOAD_ATTR                _error_handler
             1300  LOAD_CONST               None
             1302  COMPARE_OP               is
         1304_1306  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 531      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                transport
             1312  LOAD_METHOD              close
             1314  CALL_METHOD_0         0  ''
             1316  POP_TOP          
           1318_0  COME_FROM          1304  '1304'
           1318_1  COME_FROM          1292  '1292'
           1318_2  COME_FROM          1274  '1274'

Parse error at or near `CALL_FINALLY' instruction at offset 144

    def handle_error(self, request: BaseRequest, status: int=500, exc: Optional[BaseException]=None, message: Optional[str]=None) -> StreamResponse:
        """Handle errors.

        Returns HTTP response with specific status code. Logs additional
        information. It always closes current connection."""
        self.log_exception('Error handling request', exc_info=exc)
        ct = 'text/plain'
        if status == HTTPStatus.INTERNAL_SERVER_ERROR:
            title = '{0.value} {0.phrase}'.format(HTTPStatus.INTERNAL_SERVER_ERROR)
            msg = HTTPStatus.INTERNAL_SERVER_ERROR.description
            tb = None
            if self.debug:
                with suppress(Exception):
                    tb = traceback.format_exc()
            elif 'text/html' in request.headers.get('Accept', ''):
                if tb:
                    tb = html_escape(tb)
                    msg = '<h2>Traceback:</h2>\n<pre>{}</pre>'.format(tb)
                message = '<html><head><title>{title}</title></head><body>\n<h1>{title}</h1>\n{msg}\n</body></html>\n'.format(title=title,
                  msg=msg)
                ct = 'text/html'
            else:
                if tb:
                    msg = tb
                message = title + '\n\n' + msg
        resp = Response(status=status, text=message, content_type=ct)
        resp.force_close()
        if request.writer.output_size > 0 or self.transport is None:
            self.force_close()
        return resp

    async def handle_parse_error(self, writer: AbstractStreamWriter, status: int, exc: Optional[BaseException]=None, message: Optional[str]=None) -> None:
        request = BaseRequest(ERROR, EMPTY_PAYLOAD, self, writer, current_task(), self._loop)
        resp = self.handle_error(request, status, exc, message)
        await resp.prepare(request)
        await resp.write_eof()
        if self.transport is not None:
            self.transport.close()
        self._error_handler = None