# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\web_ws.py
import asyncio, base64, binascii, hashlib, json
from typing import Any, Iterable, Optional, Tuple
import async_timeout, attr
from multidict import CIMultiDict
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import call_later, set_result
from .http import WS_CLOSED_MESSAGE, WS_CLOSING_MESSAGE, WS_KEY, WebSocketError, WebSocketReader, WebSocketWriter, WSMessage
from .http import WSMsgType
from .http import ws_ext_gen, ws_ext_parse
from .log import ws_logger
from .streams import EofStream, FlowControlDataQueue
from .typedefs import JSONDecoder, JSONEncoder
from .web_exceptions import HTTPBadRequest, HTTPException
from .web_request import BaseRequest
from .web_response import StreamResponse
__all__ = ('WebSocketResponse', 'WebSocketReady', 'WSMsgType')
THRESHOLD_CONNLOST_ACCESS = 5

@attr.s(frozen=True, slots=True)
class WebSocketReady:
    ok = attr.ib(type=bool)
    protocol = attr.ib(type=(Optional[str]))

    def __bool__(self) -> bool:
        return self.ok


class WebSocketResponse(StreamResponse):
    _length_check = False

    def __init__(self, *, timeout=10.0, receive_timeout=None, autoclose=True, autoping=True, heartbeat=None, protocols=(), compress=True, max_msg_size=4194304):
        super().__init__(status=101)
        self._protocols = protocols
        self._ws_protocol = None
        self._writer = None
        self._reader = None
        self._closed = False
        self._closing = False
        self._conn_lost = 0
        self._close_code = None
        self._loop = None
        self._waiting = None
        self._exception = None
        self._timeout = timeout
        self._receive_timeout = receive_timeout
        self._autoclose = autoclose
        self._autoping = autoping
        self._heartbeat = heartbeat
        self._heartbeat_cb = None
        if heartbeat is not None:
            self._pong_heartbeat = heartbeat / 2.0
        self._pong_response_cb = None
        self._compress = compress
        self._max_msg_size = max_msg_size

    def _cancel_heartbeat(self) -> None:
        if self._pong_response_cb is not None:
            self._pong_response_cb.cancel()
            self._pong_response_cb = None
        if self._heartbeat_cb is not None:
            self._heartbeat_cb.cancel()
            self._heartbeat_cb = None

    def _reset_heartbeat(self) -> None:
        self._cancel_heartbeat()
        if self._heartbeat is not None:
            self._heartbeat_cb = call_later(self._send_heartbeat, self._heartbeat, self._loop)

    def _send_heartbeat(self) -> None:
        if self._heartbeat is not None:
            if not self._closed:
                self._loop.create_task(self._writer.ping())
                if self._pong_response_cb is not None:
                    self._pong_response_cb.cancel()
                self._pong_response_cb = call_later(self._pong_not_received, self._pong_heartbeat, self._loop)

    def _pong_not_received(self) -> None:
        if self._req is not None:
            if self._req.transport is not None:
                self._closed = True
                self._close_code = 1006
                self._exception = asyncio.TimeoutError()
                self._req.transport.close()

    async def prepare(self, request):
        if self._payload_writer is not None:
            return self._payload_writer
        protocol, writer = self._pre_start(request)
        payload_writer = await super().prepare(request)
        assert payload_writer is not None
        self._post_start(request, protocol, writer)
        await payload_writer.drain()
        return payload_writer

    def _handshake(self, request: BaseRequest) -> Tuple[('CIMultiDict[str]',
 str,
 bool,
 bool)]:
        headers = request.headers
        if 'websocket' != headers.get(hdrs.UPGRADE, '').lower().strip():
            raise HTTPBadRequest(text=('No WebSocket UPGRADE hdr: {}\n Can "Upgrade" only to "WebSocket".'.format(headers.get(hdrs.UPGRADE))))
        if 'upgrade' not in headers.get(hdrs.CONNECTION, '').lower():
            raise HTTPBadRequest(text=('No CONNECTION upgrade hdr: {}'.format(headers.get(hdrs.CONNECTION))))
        protocol = None
        if hdrs.SEC_WEBSOCKET_PROTOCOL in headers:
            req_protocols = [str(proto.strip()) for proto in headers[hdrs.SEC_WEBSOCKET_PROTOCOL].split(',')]
            for proto in req_protocols:
                if proto in self._protocols:
                    protocol = proto
                    break
            else:
                ws_logger.warning('Client protocols %r don’t overlap server-known ones %r', req_protocols, self._protocols)

        version = headers.get(hdrs.SEC_WEBSOCKET_VERSION, '')
        if version not in ('13', '8', '7'):
            raise HTTPBadRequest(text=('Unsupported version: {}'.format(version)))
        key = headers.get(hdrs.SEC_WEBSOCKET_KEY)
        try:
            if not key or len(base64.b64decode(key)) != 16:
                raise HTTPBadRequest(text=('Handshake error: {!r}'.format(key)))
        except binascii.Error:
            raise HTTPBadRequest(text=('Handshake error: {!r}'.format(key))) from None
        else:
            accept_val = base64.b64encode(hashlib.sha1(key.encode() + WS_KEY).digest()).decode()
            response_headers = CIMultiDict({hdrs.UPGRADE: 'websocket', 
             hdrs.CONNECTION: 'upgrade', 
             hdrs.SEC_WEBSOCKET_ACCEPT: accept_val})
            notakeover = False
            compress = 0
            if self._compress:
                extensions = headers.get(hdrs.SEC_WEBSOCKET_EXTENSIONS)
                compress, notakeover = ws_ext_parse(extensions, isserver=True)
                if compress:
                    enabledext = ws_ext_gen(compress=compress, isserver=True, server_notakeover=notakeover)
                    response_headers[hdrs.SEC_WEBSOCKET_EXTENSIONS] = enabledext
            if protocol:
                response_headers[hdrs.SEC_WEBSOCKET_PROTOCOL] = protocol
            else:
                return (
                 response_headers,
                 protocol,
                 compress,
                 notakeover)

    def _pre_start(self, request: BaseRequest) -> Tuple[(str, WebSocketWriter)]:
        self._loop = request._loop
        headers, protocol, compress, notakeover = self._handshake(request)
        self._reset_heartbeat()
        self.set_status(101)
        self.headers.update(headers)
        self.force_close()
        self._compress = compress
        transport = request._protocol.transport
        assert transport is not None
        writer = WebSocketWriter((request._protocol), transport,
          compress=compress,
          notakeover=notakeover)
        return (
         protocol, writer)

    def _post_start(self, request: BaseRequest, protocol: str, writer: WebSocketWriter) -> None:
        self._ws_protocol = protocol
        self._writer = writer
        loop = self._loop
        assert loop is not None
        self._reader = FlowControlDataQueue((request._protocol),
          limit=65536, loop=loop)
        request.protocol.set_parser(WebSocketReader((self._reader),
          (self._max_msg_size), compress=(self._compress)))
        request.protocol.keep_alive(False)

    def can_prepare(self, request: BaseRequest) -> WebSocketReady:
        if self._writer is not None:
            raise RuntimeError('Already started')
        try:
            _, protocol, _, _ = self._handshake(request)
        except HTTPException:
            return WebSocketReady(False, None)
        else:
            return WebSocketReady(True, protocol)

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def close_code(self) -> Optional[int]:
        return self._close_code

    @property
    def ws_protocol(self) -> Optional[str]:
        return self._ws_protocol

    @property
    def compress(self) -> bool:
        return self._compress

    def exception(self) -> Optional[BaseException]:
        return self._exception

    async def ping(self, message: bytes=b'') -> None:
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        await self._writer.ping(message)

    async def pong(self, message: bytes=b'') -> None:
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        await self._writer.pong(message)

    async def send_str(self, data: str, compress: Optional[bool]=None) -> None:
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        if not isinstance(data, str):
            raise TypeError('data argument must be str (%r)' % type(data))
        await self._writer.send(data, binary=False, compress=compress)

    async def send_bytes(self, data: bytes, compress: Optional[bool]=None) -> None:
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be byte-ish (%r)' % type(data))
        await self._writer.send(data, binary=True, compress=compress)

    async def send_json(self, data: Any, compress: Optional[bool]=None, *, dumps: JSONEncoder=json.dumps) -> None:
        await self.send_str((dumps(data)), compress=compress)

    async def write_eof(self) -> None:
        if self._eof_sent:
            return
        if self._payload_writer is None:
            raise RuntimeError('Response has not been started')
        await self.close()
        self._eof_sent = True

    async def close--- This code section failed: ---

 L. 306         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 307        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 309        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _cancel_heartbeat
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          

 L. 310        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _reader
               30  STORE_FAST               'reader'

 L. 311        32  LOAD_FAST                'reader'
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  LOAD_ASSERT              AssertionError
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 315        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _waiting
               48  LOAD_CONST               None
               50  COMPARE_OP               is-not
               52  POP_JUMP_IF_FALSE    84  'to 84'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _closed
               58  POP_JUMP_IF_TRUE     84  'to 84'

 L. 316        60  LOAD_FAST                'reader'
               62  LOAD_METHOD              feed_data
               64  LOAD_GLOBAL              WS_CLOSING_MESSAGE
               66  LOAD_CONST               0
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          

 L. 317        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _waiting
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  POP_TOP          
             84_0  COME_FROM            58  '58'
             84_1  COME_FROM            52  '52'

 L. 319        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _closed
            88_90  POP_JUMP_IF_TRUE    454  'to 454'

 L. 320        92  LOAD_CONST               True
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _closed

 L. 321        98  SETUP_FINALLY       156  'to 156'

 L. 322       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _writer
              104  LOAD_METHOD              close
              106  LOAD_FAST                'code'
              108  LOAD_FAST                'message'
              110  CALL_METHOD_2         2  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_TOP          

 L. 323       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _payload_writer
              124  STORE_FAST               'writer'

 L. 324       126  LOAD_FAST                'writer'
              128  LOAD_CONST               None
              130  COMPARE_OP               is-not
              132  POP_JUMP_IF_TRUE    138  'to 138'
              134  LOAD_ASSERT              AssertionError
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           132  '132'

 L. 325       138  LOAD_FAST                'writer'
              140  LOAD_METHOD              drain
              142  CALL_METHOD_0         0  ''
              144  GET_AWAITABLE    
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  POP_TOP          
              152  POP_BLOCK        
              154  JUMP_FORWARD        242  'to 242'
            156_0  COME_FROM_FINALLY    98  '98'

 L. 326       156  DUP_TOP          
              158  LOAD_GLOBAL              asyncio
              160  LOAD_ATTR                CancelledError
              162  LOAD_GLOBAL              asyncio
              164  LOAD_ATTR                TimeoutError
              166  BUILD_TUPLE_2         2 
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   190  'to 190'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 327       178  LOAD_CONST               1006
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _close_code

 L. 328       184  RAISE_VARARGS_0       0  'reraise'
              186  POP_EXCEPT       
              188  JUMP_FORWARD        242  'to 242'
            190_0  COME_FROM           170  '170'

 L. 329       190  DUP_TOP          
              192  LOAD_GLOBAL              Exception
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   240  'to 240'
              198  POP_TOP          
              200  STORE_FAST               'exc'
              202  POP_TOP          
              204  SETUP_FINALLY       228  'to 228'

 L. 330       206  LOAD_CONST               1006
              208  LOAD_FAST                'self'
              210  STORE_ATTR               _close_code

 L. 331       212  LOAD_FAST                'exc'
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _exception

 L. 332       218  POP_BLOCK        
              220  POP_EXCEPT       
              222  CALL_FINALLY        228  'to 228'
              224  LOAD_CONST               True
              226  RETURN_VALUE     
            228_0  COME_FROM           222  '222'
            228_1  COME_FROM_FINALLY   204  '204'
              228  LOAD_CONST               None
              230  STORE_FAST               'exc'
              232  DELETE_FAST              'exc'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           196  '196'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           188  '188'
            242_2  COME_FROM           154  '154'

 L. 334       242  LOAD_FAST                'self'
              244  LOAD_ATTR                _closing
          246_248  POP_JUMP_IF_FALSE   254  'to 254'

 L. 335       250  LOAD_CONST               True
              252  RETURN_VALUE     
            254_0  COME_FROM           246  '246'

 L. 337       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _reader
              258  STORE_FAST               'reader'

 L. 338       260  LOAD_FAST                'reader'
              262  LOAD_CONST               None
              264  COMPARE_OP               is-not
          266_268  POP_JUMP_IF_TRUE    274  'to 274'
              270  LOAD_ASSERT              AssertionError
              272  RAISE_VARARGS_1       1  'exception instance'
            274_0  COME_FROM           266  '266'

 L. 339       274  SETUP_FINALLY       324  'to 324'

 L. 340       276  LOAD_GLOBAL              async_timeout
              278  LOAD_ATTR                timeout
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                _timeout
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                _loop
              288  LOAD_CONST               ('loop',)
              290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              292  SETUP_WITH          314  'to 314'
              294  POP_TOP          

 L. 341       296  LOAD_FAST                'reader'
              298  LOAD_METHOD              read
              300  CALL_METHOD_0         0  ''
              302  GET_AWAITABLE    
              304  LOAD_CONST               None
              306  YIELD_FROM       
              308  STORE_FAST               'msg'
              310  POP_BLOCK        
              312  BEGIN_FINALLY    
            314_0  COME_FROM_WITH      292  '292'
              314  WITH_CLEANUP_START
              316  WITH_CLEANUP_FINISH
              318  END_FINALLY      
              320  POP_BLOCK        
              322  JUMP_FORWARD        408  'to 408'
            324_0  COME_FROM_FINALLY   274  '274'

 L. 342       324  DUP_TOP          
              326  LOAD_GLOBAL              asyncio
              328  LOAD_ATTR                CancelledError
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   354  'to 354'
              336  POP_TOP          
              338  POP_TOP          
              340  POP_TOP          

 L. 343       342  LOAD_CONST               1006
              344  LOAD_FAST                'self'
              346  STORE_ATTR               _close_code

 L. 344       348  RAISE_VARARGS_0       0  'reraise'
              350  POP_EXCEPT       
              352  JUMP_FORWARD        408  'to 408'
            354_0  COME_FROM           332  '332'

 L. 345       354  DUP_TOP          
              356  LOAD_GLOBAL              Exception
              358  COMPARE_OP               exception-match
          360_362  POP_JUMP_IF_FALSE   406  'to 406'
              364  POP_TOP          
              366  STORE_FAST               'exc'
              368  POP_TOP          
              370  SETUP_FINALLY       394  'to 394'

 L. 346       372  LOAD_CONST               1006
              374  LOAD_FAST                'self'
              376  STORE_ATTR               _close_code

 L. 347       378  LOAD_FAST                'exc'
              380  LOAD_FAST                'self'
              382  STORE_ATTR               _exception

 L. 348       384  POP_BLOCK        
              386  POP_EXCEPT       
              388  CALL_FINALLY        394  'to 394'
              390  LOAD_CONST               True
              392  RETURN_VALUE     
            394_0  COME_FROM           388  '388'
            394_1  COME_FROM_FINALLY   370  '370'
              394  LOAD_CONST               None
              396  STORE_FAST               'exc'
              398  DELETE_FAST              'exc'
              400  END_FINALLY      
              402  POP_EXCEPT       
              404  JUMP_FORWARD        408  'to 408'
            406_0  COME_FROM           360  '360'
              406  END_FINALLY      
            408_0  COME_FROM           404  '404'
            408_1  COME_FROM           352  '352'
            408_2  COME_FROM           322  '322'

 L. 350       408  LOAD_FAST                'msg'
              410  LOAD_ATTR                type
              412  LOAD_GLOBAL              WSMsgType
              414  LOAD_ATTR                CLOSE
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   434  'to 434'

 L. 351       422  LOAD_FAST                'msg'
              424  LOAD_ATTR                data
              426  LOAD_FAST                'self'
              428  STORE_ATTR               _close_code

 L. 352       430  LOAD_CONST               True
              432  RETURN_VALUE     
            434_0  COME_FROM           418  '418'

 L. 354       434  LOAD_CONST               1006
              436  LOAD_FAST                'self'
              438  STORE_ATTR               _close_code

 L. 355       440  LOAD_GLOBAL              asyncio
              442  LOAD_METHOD              TimeoutError
              444  CALL_METHOD_0         0  ''
              446  LOAD_FAST                'self'
              448  STORE_ATTR               _exception

 L. 356       450  LOAD_CONST               True
              452  RETURN_VALUE     
            454_0  COME_FROM            88  '88'

 L. 358       454  LOAD_CONST               False
              456  RETURN_VALUE     

Parse error at or near `CALL_FINALLY' instruction at offset 222

    async def receive--- This code section failed: ---

 L. 361         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reader
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 362        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 364        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  STORE_FAST               'loop'

 L. 365        24  LOAD_FAST                'loop'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  LOAD_ASSERT              AssertionError
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM           614  '614'
             36_1  COME_FROM           588  '588'
             36_2  COME_FROM            30  '30'

 L. 367        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _waiting
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 368        46  LOAD_GLOBAL              RuntimeError

 L. 369        48  LOAD_STR                 'Concurrent call to receive() is not allowed'

 L. 368        50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 371        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _closed
               58  POP_JUMP_IF_FALSE    96  'to 96'

 L. 372        60  LOAD_FAST                'self'
               62  DUP_TOP          
               64  LOAD_ATTR                _conn_lost
               66  LOAD_CONST               1
               68  INPLACE_ADD      
               70  ROT_TWO          
               72  STORE_ATTR               _conn_lost

 L. 373        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _conn_lost
               78  LOAD_GLOBAL              THRESHOLD_CONNLOST_ACCESS
               80  COMPARE_OP               >=
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 374        84  LOAD_GLOBAL              RuntimeError
               86  LOAD_STR                 'WebSocket connection is closed.'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 375        92  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               94  RETURN_VALUE     
             96_0  COME_FROM            58  '58'

 L. 376        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _closing
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 377       102  LOAD_GLOBAL              WS_CLOSING_MESSAGE
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 379       106  SETUP_FINALLY       212  'to 212'

 L. 380       108  LOAD_FAST                'loop'
              110  LOAD_METHOD              create_future
              112  CALL_METHOD_0         0  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _waiting

 L. 381       118  SETUP_FINALLY       182  'to 182'

 L. 382       120  LOAD_GLOBAL              async_timeout
              122  LOAD_ATTR                timeout

 L. 383       124  LOAD_FAST                'timeout'
              126  JUMP_IF_TRUE_OR_POP   132  'to 132'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _receive_timeout
            132_0  COME_FROM           126  '126'

 L. 383       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _loop

 L. 382       136  LOAD_CONST               ('loop',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  SETUP_WITH          164  'to 164'
              142  POP_TOP          

 L. 384       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _reader
              148  LOAD_METHOD              read
              150  CALL_METHOD_0         0  ''
              152  GET_AWAITABLE    
              154  LOAD_CONST               None
              156  YIELD_FROM       
              158  STORE_FAST               'msg'
              160  POP_BLOCK        
              162  BEGIN_FINALLY    
            164_0  COME_FROM_WITH      140  '140'
              164  WITH_CLEANUP_START
              166  WITH_CLEANUP_FINISH
              168  END_FINALLY      

 L. 385       170  LOAD_FAST                'self'
              172  LOAD_METHOD              _reset_heartbeat
              174  CALL_METHOD_0         0  ''
              176  POP_TOP          
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_FINALLY   118  '118'

 L. 387       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _waiting
              186  STORE_FAST               'waiter'

 L. 388       188  LOAD_GLOBAL              set_result
              190  LOAD_FAST                'waiter'
              192  LOAD_CONST               True
              194  CALL_FUNCTION_2       2  ''
              196  POP_TOP          

 L. 389       198  LOAD_CONST               None
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _waiting
              204  END_FINALLY      
              206  POP_BLOCK        
          208_210  JUMP_FORWARD        466  'to 466'
            212_0  COME_FROM_FINALLY   106  '106'

 L. 390       212  DUP_TOP          
              214  LOAD_GLOBAL              asyncio
              216  LOAD_ATTR                CancelledError
              218  LOAD_GLOBAL              asyncio
              220  LOAD_ATTR                TimeoutError
              222  BUILD_TUPLE_2         2 
              224  COMPARE_OP               exception-match
              226  POP_JUMP_IF_FALSE   246  'to 246'
              228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L. 391       234  LOAD_CONST               1006
              236  LOAD_FAST                'self'
              238  STORE_ATTR               _close_code

 L. 392       240  RAISE_VARARGS_0       0  'reraise'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        466  'to 466'
            246_0  COME_FROM           226  '226'

 L. 393       246  DUP_TOP          
              248  LOAD_GLOBAL              EofStream
              250  COMPARE_OP               exception-match
          252_254  POP_JUMP_IF_FALSE   300  'to 300'
              256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L. 394       262  LOAD_CONST               1000
              264  LOAD_FAST                'self'
              266  STORE_ATTR               _close_code

 L. 395       268  LOAD_FAST                'self'
              270  LOAD_METHOD              close
              272  CALL_METHOD_0         0  ''
              274  GET_AWAITABLE    
              276  LOAD_CONST               None
              278  YIELD_FROM       
              280  POP_TOP          

 L. 396       282  LOAD_GLOBAL              WSMessage
              284  LOAD_GLOBAL              WSMsgType
              286  LOAD_ATTR                CLOSED
              288  LOAD_CONST               None
              290  LOAD_CONST               None
              292  CALL_FUNCTION_3       3  ''
              294  ROT_FOUR         
              296  POP_EXCEPT       
              298  RETURN_VALUE     
            300_0  COME_FROM           252  '252'

 L. 397       300  DUP_TOP          
              302  LOAD_GLOBAL              WebSocketError
              304  COMPARE_OP               exception-match
          306_308  POP_JUMP_IF_FALSE   380  'to 380'
              310  POP_TOP          
              312  STORE_FAST               'exc'
              314  POP_TOP          
              316  SETUP_FINALLY       368  'to 368'

 L. 398       318  LOAD_FAST                'exc'
              320  LOAD_ATTR                code
              322  LOAD_FAST                'self'
              324  STORE_ATTR               _close_code

 L. 399       326  LOAD_FAST                'self'
              328  LOAD_ATTR                close
              330  LOAD_FAST                'exc'
              332  LOAD_ATTR                code
              334  LOAD_CONST               ('code',)
              336  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              338  GET_AWAITABLE    
              340  LOAD_CONST               None
              342  YIELD_FROM       
              344  POP_TOP          

 L. 400       346  LOAD_GLOBAL              WSMessage
              348  LOAD_GLOBAL              WSMsgType
              350  LOAD_ATTR                ERROR
              352  LOAD_FAST                'exc'
              354  LOAD_CONST               None
              356  CALL_FUNCTION_3       3  ''
              358  ROT_FOUR         
              360  POP_BLOCK        
              362  POP_EXCEPT       
              364  CALL_FINALLY        368  'to 368'
              366  RETURN_VALUE     
            368_0  COME_FROM           364  '364'
            368_1  COME_FROM_FINALLY   316  '316'
              368  LOAD_CONST               None
              370  STORE_FAST               'exc'
              372  DELETE_FAST              'exc'
              374  END_FINALLY      
              376  POP_EXCEPT       
              378  JUMP_FORWARD        466  'to 466'
            380_0  COME_FROM           306  '306'

 L. 401       380  DUP_TOP          
              382  LOAD_GLOBAL              Exception
              384  COMPARE_OP               exception-match
          386_388  POP_JUMP_IF_FALSE   464  'to 464'
              390  POP_TOP          
              392  STORE_FAST               'exc'
              394  POP_TOP          
              396  SETUP_FINALLY       452  'to 452'

 L. 402       398  LOAD_FAST                'exc'
              400  LOAD_FAST                'self'
              402  STORE_ATTR               _exception

 L. 403       404  LOAD_CONST               True
              406  LOAD_FAST                'self'
              408  STORE_ATTR               _closing

 L. 404       410  LOAD_CONST               1006
              412  LOAD_FAST                'self'
              414  STORE_ATTR               _close_code

 L. 405       416  LOAD_FAST                'self'
              418  LOAD_METHOD              close
              420  CALL_METHOD_0         0  ''
              422  GET_AWAITABLE    
              424  LOAD_CONST               None
              426  YIELD_FROM       
              428  POP_TOP          

 L. 406       430  LOAD_GLOBAL              WSMessage
              432  LOAD_GLOBAL              WSMsgType
              434  LOAD_ATTR                ERROR
              436  LOAD_FAST                'exc'
              438  LOAD_CONST               None
              440  CALL_FUNCTION_3       3  ''
              442  ROT_FOUR         
              444  POP_BLOCK        
              446  POP_EXCEPT       
              448  CALL_FINALLY        452  'to 452'
              450  RETURN_VALUE     
            452_0  COME_FROM           448  '448'
            452_1  COME_FROM_FINALLY   396  '396'
              452  LOAD_CONST               None
              454  STORE_FAST               'exc'
              456  DELETE_FAST              'exc'
              458  END_FINALLY      
              460  POP_EXCEPT       
              462  JUMP_FORWARD        466  'to 466'
            464_0  COME_FROM           386  '386'
              464  END_FINALLY      
            466_0  COME_FROM           462  '462'
            466_1  COME_FROM           378  '378'
            466_2  COME_FROM           244  '244'
            466_3  COME_FROM           208  '208'

 L. 408       466  LOAD_FAST                'msg'
              468  LOAD_ATTR                type
              470  LOAD_GLOBAL              WSMsgType
              472  LOAD_ATTR                CLOSE
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   526  'to 526'

 L. 409       480  LOAD_CONST               True
              482  LOAD_FAST                'self'
              484  STORE_ATTR               _closing

 L. 410       486  LOAD_FAST                'msg'
              488  LOAD_ATTR                data
              490  LOAD_FAST                'self'
              492  STORE_ATTR               _close_code

 L. 411       494  LOAD_FAST                'self'
              496  LOAD_ATTR                _closed
          498_500  POP_JUMP_IF_TRUE    616  'to 616'
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                _autoclose
          506_508  POP_JUMP_IF_FALSE   616  'to 616'

 L. 412       510  LOAD_FAST                'self'
              512  LOAD_METHOD              close
              514  CALL_METHOD_0         0  ''
              516  GET_AWAITABLE    
              518  LOAD_CONST               None
              520  YIELD_FROM       
              522  POP_TOP          
              524  JUMP_FORWARD        616  'to 616'
            526_0  COME_FROM           476  '476'

 L. 413       526  LOAD_FAST                'msg'
              528  LOAD_ATTR                type
              530  LOAD_GLOBAL              WSMsgType
              532  LOAD_ATTR                CLOSING
              534  COMPARE_OP               ==
          536_538  POP_JUMP_IF_FALSE   548  'to 548'

 L. 414       540  LOAD_CONST               True
              542  LOAD_FAST                'self'
              544  STORE_ATTR               _closing
              546  JUMP_FORWARD        616  'to 616'
            548_0  COME_FROM           536  '536'

 L. 415       548  LOAD_FAST                'msg'
              550  LOAD_ATTR                type
              552  LOAD_GLOBAL              WSMsgType
              554  LOAD_ATTR                PING
              556  COMPARE_OP               ==
          558_560  POP_JUMP_IF_FALSE   592  'to 592'
              562  LOAD_FAST                'self'
              564  LOAD_ATTR                _autoping
          566_568  POP_JUMP_IF_FALSE   592  'to 592'

 L. 416       570  LOAD_FAST                'self'
              572  LOAD_METHOD              pong
              574  LOAD_FAST                'msg'
              576  LOAD_ATTR                data
              578  CALL_METHOD_1         1  ''
              580  GET_AWAITABLE    
              582  LOAD_CONST               None
              584  YIELD_FROM       
              586  POP_TOP          

 L. 417       588  JUMP_BACK            36  'to 36'
              590  BREAK_LOOP          616  'to 616'
            592_0  COME_FROM           566  '566'
            592_1  COME_FROM           558  '558'

 L. 418       592  LOAD_FAST                'msg'
              594  LOAD_ATTR                type
              596  LOAD_GLOBAL              WSMsgType
              598  LOAD_ATTR                PONG
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   616  'to 616'
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                _autoping
          610_612  POP_JUMP_IF_FALSE   616  'to 616'

 L. 419       614  JUMP_BACK            36  'to 36'
            616_0  COME_FROM           610  '610'
            616_1  COME_FROM           602  '602'
            616_2  COME_FROM           590  '590'
            616_3  COME_FROM           546  '546'
            616_4  COME_FROM           524  '524'
            616_5  COME_FROM           506  '506'
            616_6  COME_FROM           498  '498'

 L. 421       616  LOAD_FAST                'msg'
              618  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 360

    async def receive_str(self, *, timeout: Optional[float]=None) -> str:
        msg = await self.receive(timeout)
        if msg.type != WSMsgType.TEXT:
            raise TypeError('Received message {}:{!r} is not WSMsgType.TEXT'.format(msg.type, msg.data))
        return msg.data

    async def receive_bytes(self, *, timeout: Optional[float]=None) -> bytes:
        msg = await self.receive(timeout)
        if msg.type != WSMsgType.BINARY:
            raise TypeError('Received message {}:{!r} is not bytes'.format(msg.type, msg.data))
        return msg.data

    async def receive_json(self, *, loads: JSONDecoder=json.loads, timeout: Optional[float]=None) -> Any:
        data = await self.receive_str(timeout=timeout)
        return loads(data)

    async def write(self, data: bytes) -> None:
        raise RuntimeError('Cannot call .write() for websocket')

    def __aiter__(self) -> 'WebSocketResponse':
        return self

    async def __anext__(self) -> WSMessage:
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE,
         WSMsgType.CLOSING,
         WSMsgType.CLOSED):
            raise StopAsyncIteration
        return msg