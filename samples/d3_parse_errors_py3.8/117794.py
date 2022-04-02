# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\client_ws.py
"""WebSocket client for asyncio."""
import asyncio
from typing import Any, Optional
import async_timeout
from .client_exceptions import ClientError
from .client_reqrep import ClientResponse
from .helpers import call_later, set_result
from .http import WS_CLOSED_MESSAGE, WS_CLOSING_MESSAGE, WebSocketError, WSMessage, WSMsgType
from .http_websocket import WebSocketWriter
from .streams import EofStream, FlowControlDataQueue
from .typedefs import DEFAULT_JSON_DECODER, DEFAULT_JSON_ENCODER, JSONDecoder, JSONEncoder

class ClientWebSocketResponse:

    def __init__(self, reader: 'FlowControlDataQueue[WSMessage]', writer: WebSocketWriter, protocol: Optional[str], response: ClientResponse, timeout: float, autoclose: bool, autoping: bool, loop: asyncio.AbstractEventLoop, *, receive_timeout: Optional[float]=None, heartbeat: Optional[float]=None, compress: int=0, client_notakeover: bool=False) -> None:
        self._response = response
        self._conn = response.connection
        self._writer = writer
        self._reader = reader
        self._protocol = protocol
        self._closed = False
        self._closing = False
        self._close_code = None
        self._timeout = timeout
        self._receive_timeout = receive_timeout
        self._autoclose = autoclose
        self._autoping = autoping
        self._heartbeat = heartbeat
        self._heartbeat_cb = None
        if heartbeat is not None:
            self._pong_heartbeat = heartbeat / 2.0
        self._pong_response_cb = None
        self._loop = loop
        self._waiting = None
        self._exception = None
        self._compress = compress
        self._client_notakeover = client_notakeover
        self._reset_heartbeat()

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
        if not self._closed:
            self._closed = True
            self._close_code = 1006
            self._exception = asyncio.TimeoutError()
            self._response.close()

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def close_code(self) -> Optional[int]:
        return self._close_code

    @property
    def protocol(self) -> Optional[str]:
        return self._protocol

    @property
    def compress(self) -> int:
        return self._compress

    @property
    def client_notakeover(self) -> bool:
        return self._client_notakeover

    def get_extra_info(self, name: str, default: Any=None) -> Any:
        """extra info from connection transport"""
        conn = self._response.connection
        if conn is None:
            return default
        transport = conn.transport
        if transport is None:
            return default
        return transport.get_extra_info(name, default)

    def exception(self) -> Optional[BaseException]:
        return self._exception

    async def ping(self, message: bytes=b'') -> None:
        await self._writer.ping(message)

    async def pong(self, message: bytes=b'') -> None:
        await self._writer.pong(message)

    async def send_str(self, data: str, compress: Optional[int]=None) -> None:
        if not isinstance(data, str):
            raise TypeError('data argument must be str (%r)' % type(data))
        await self._writer.send(data, binary=False, compress=compress)

    async def send_bytes(self, data: bytes, compress: Optional[int]=None) -> None:
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be byte-ish (%r)' % type(data))
        await self._writer.send(data, binary=True, compress=compress)

    async def send_json(self, data: Any, compress: Optional[int]=None, *, dumps: JSONEncoder=DEFAULT_JSON_ENCODER) -> None:
        await self.send_str((dumps(data)), compress=compress)

    async def close--- This code section failed: ---

 L. 165         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiting
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    42  'to 42'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_TRUE     42  'to 42'

 L. 166        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _reader
               20  LOAD_METHOD              feed_data
               22  LOAD_GLOBAL              WS_CLOSING_MESSAGE
               24  LOAD_CONST               0
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L. 167        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _waiting
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
             42_0  COME_FROM            14  '14'
             42_1  COME_FROM             8  '8'

 L. 169        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _closed
            46_48  POP_JUMP_IF_TRUE    404  'to 404'

 L. 170        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _cancel_heartbeat
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          

 L. 171        58  LOAD_CONST               True
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _closed

 L. 172        64  SETUP_FINALLY        90  'to 90'

 L. 173        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _writer
               70  LOAD_METHOD              close
               72  LOAD_FAST                'code'
               74  LOAD_FAST                'message'
               76  CALL_METHOD_2         2  ''
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_FORWARD        190  'to 190'
             90_0  COME_FROM_FINALLY    64  '64'

 L. 174        90  DUP_TOP          
               92  LOAD_GLOBAL              asyncio
               94  LOAD_ATTR                CancelledError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   128  'to 128'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 175       106  LOAD_CONST               1006
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _close_code

 L. 176       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _response
              116  LOAD_METHOD              close
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          

 L. 177       122  RAISE_VARARGS_0       0  'reraise'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        190  'to 190'
            128_0  COME_FROM            98  '98'

 L. 178       128  DUP_TOP          
              130  LOAD_GLOBAL              Exception
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   188  'to 188'
              136  POP_TOP          
              138  STORE_FAST               'exc'
              140  POP_TOP          
              142  SETUP_FINALLY       176  'to 176'

 L. 179       144  LOAD_CONST               1006
              146  LOAD_FAST                'self'
              148  STORE_ATTR               _close_code

 L. 180       150  LOAD_FAST                'exc'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _exception

 L. 181       156  LOAD_FAST                'self'
              158  LOAD_ATTR                _response
              160  LOAD_METHOD              close
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L. 182       166  POP_BLOCK        
              168  POP_EXCEPT       
              170  CALL_FINALLY        176  'to 176'
              172  LOAD_CONST               True
              174  RETURN_VALUE     
            176_0  COME_FROM           170  '170'
            176_1  COME_FROM_FINALLY   142  '142'
              176  LOAD_CONST               None
              178  STORE_FAST               'exc'
              180  DELETE_FAST              'exc'
              182  END_FINALLY      
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           134  '134'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           126  '126'
            190_2  COME_FROM            88  '88'

 L. 184       190  LOAD_FAST                'self'
              192  LOAD_ATTR                _closing
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 185       196  LOAD_FAST                'self'
              198  LOAD_ATTR                _response
              200  LOAD_METHOD              close
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          

 L. 186       206  LOAD_CONST               True
              208  RETURN_VALUE     
            210_0  COME_FROM           400  '400'
            210_1  COME_FROM           376  '376'
            210_2  COME_FROM           194  '194'

 L. 189       210  SETUP_FINALLY       262  'to 262'

 L. 190       212  LOAD_GLOBAL              async_timeout
              214  LOAD_ATTR                timeout
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _timeout
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _loop
              224  LOAD_CONST               ('loop',)
              226  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              228  SETUP_WITH          252  'to 252'
              230  POP_TOP          

 L. 191       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _reader
              236  LOAD_METHOD              read
              238  CALL_METHOD_0         0  ''
              240  GET_AWAITABLE    
              242  LOAD_CONST               None
              244  YIELD_FROM       
              246  STORE_FAST               'msg'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_WITH      228  '228'
              252  WITH_CLEANUP_START
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      
              258  POP_BLOCK        
              260  JUMP_FORWARD        366  'to 366'
            262_0  COME_FROM_FINALLY   210  '210'

 L. 192       262  DUP_TOP          
              264  LOAD_GLOBAL              asyncio
              266  LOAD_ATTR                CancelledError
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   302  'to 302'
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          

 L. 193       280  LOAD_CONST               1006
              282  LOAD_FAST                'self'
              284  STORE_ATTR               _close_code

 L. 194       286  LOAD_FAST                'self'
              288  LOAD_ATTR                _response
              290  LOAD_METHOD              close
              292  CALL_METHOD_0         0  ''
              294  POP_TOP          

 L. 195       296  RAISE_VARARGS_0       0  'reraise'
              298  POP_EXCEPT       
              300  JUMP_FORWARD        366  'to 366'
            302_0  COME_FROM           270  '270'

 L. 196       302  DUP_TOP          
              304  LOAD_GLOBAL              Exception
              306  COMPARE_OP               exception-match
          308_310  POP_JUMP_IF_FALSE   364  'to 364'
              312  POP_TOP          
              314  STORE_FAST               'exc'
              316  POP_TOP          
              318  SETUP_FINALLY       352  'to 352'

 L. 197       320  LOAD_CONST               1006
              322  LOAD_FAST                'self'
              324  STORE_ATTR               _close_code

 L. 198       326  LOAD_FAST                'exc'
              328  LOAD_FAST                'self'
              330  STORE_ATTR               _exception

 L. 199       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _response
              336  LOAD_METHOD              close
              338  CALL_METHOD_0         0  ''
              340  POP_TOP          

 L. 200       342  POP_BLOCK        
              344  POP_EXCEPT       
              346  CALL_FINALLY        352  'to 352'
              348  LOAD_CONST               True
              350  RETURN_VALUE     
            352_0  COME_FROM           346  '346'
            352_1  COME_FROM_FINALLY   318  '318'
              352  LOAD_CONST               None
              354  STORE_FAST               'exc'
              356  DELETE_FAST              'exc'
              358  END_FINALLY      
              360  POP_EXCEPT       
              362  JUMP_FORWARD        366  'to 366'
            364_0  COME_FROM           308  '308'
              364  END_FINALLY      
            366_0  COME_FROM           362  '362'
            366_1  COME_FROM           300  '300'
            366_2  COME_FROM           260  '260'

 L. 202       366  LOAD_FAST                'msg'
              368  LOAD_ATTR                type
              370  LOAD_GLOBAL              WSMsgType
              372  LOAD_ATTR                CLOSE
              374  COMPARE_OP               ==
              376  POP_JUMP_IF_FALSE_BACK   210  'to 210'

 L. 203       378  LOAD_FAST                'msg'
              380  LOAD_ATTR                data
              382  LOAD_FAST                'self'
              384  STORE_ATTR               _close_code

 L. 204       386  LOAD_FAST                'self'
              388  LOAD_ATTR                _response
              390  LOAD_METHOD              close
              392  CALL_METHOD_0         0  ''
              394  POP_TOP          

 L. 205       396  LOAD_CONST               True
              398  RETURN_VALUE     
              400  JUMP_BACK           210  'to 210'
              402  JUMP_FORWARD        408  'to 408'
            404_0  COME_FROM            46  '46'

 L. 207       404  LOAD_CONST               False
              406  RETURN_VALUE     
            408_0  COME_FROM           402  '402'

Parse error at or near `CALL_FINALLY' instruction at offset 170

    async def receive--- This code section failed: ---
              0_0  COME_FROM           598  '598'
              0_1  COME_FROM           572  '572'

 L. 211         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiting
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 212        10  LOAD_GLOBAL              RuntimeError

 L. 213        12  LOAD_STR                 'Concurrent call to receive() is not allowed'

 L. 212        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 215        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _closed
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 216        24  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 217        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _closing
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 218        34  LOAD_FAST                'self'
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  POP_TOP          

 L. 219        48  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               50  RETURN_VALUE     
             52_0  COME_FROM            32  '32'

 L. 221        52  SETUP_FINALLY       160  'to 160'

 L. 222        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _loop
               58  LOAD_METHOD              create_future
               60  CALL_METHOD_0         0  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _waiting

 L. 223        66  SETUP_FINALLY       130  'to 130'

 L. 224        68  LOAD_GLOBAL              async_timeout
               70  LOAD_ATTR                timeout

 L. 225        72  LOAD_FAST                'timeout'
               74  JUMP_IF_TRUE_OR_POP    80  'to 80'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _receive_timeout
             80_0  COME_FROM            74  '74'

 L. 226        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _loop

 L. 224        84  LOAD_CONST               ('loop',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  SETUP_WITH          112  'to 112'
               90  POP_TOP          

 L. 227        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _reader
               96  LOAD_METHOD              read
               98  CALL_METHOD_0         0  ''
              100  GET_AWAITABLE    
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  STORE_FAST               'msg'
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_WITH       88  '88'
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  END_FINALLY      

 L. 228       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _reset_heartbeat
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_FINALLY    66  '66'

 L. 230       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _waiting
              134  STORE_FAST               'waiter'

 L. 231       136  LOAD_CONST               None
              138  LOAD_FAST                'self'
              140  STORE_ATTR               _waiting

 L. 232       142  LOAD_GLOBAL              set_result
              144  LOAD_FAST                'waiter'
              146  LOAD_CONST               True
              148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          
              152  END_FINALLY      
              154  POP_BLOCK        
          156_158  JUMP_FORWARD        450  'to 450'
            160_0  COME_FROM_FINALLY    52  '52'

 L. 233       160  DUP_TOP          
              162  LOAD_GLOBAL              asyncio
              164  LOAD_ATTR                CancelledError
              166  LOAD_GLOBAL              asyncio
              168  LOAD_ATTR                TimeoutError
              170  BUILD_TUPLE_2         2 
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   196  'to 196'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 234       182  LOAD_CONST               1006
              184  LOAD_FAST                'self'
              186  STORE_ATTR               _close_code

 L. 235       188  RAISE_VARARGS_0       0  'reraise'
              190  POP_EXCEPT       
          192_194  JUMP_FORWARD        450  'to 450'
            196_0  COME_FROM           174  '174'

 L. 236       196  DUP_TOP          
              198  LOAD_GLOBAL              EofStream
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   248  'to 248'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 237       210  LOAD_CONST               1000
              212  LOAD_FAST                'self'
              214  STORE_ATTR               _close_code

 L. 238       216  LOAD_FAST                'self'
              218  LOAD_METHOD              close
              220  CALL_METHOD_0         0  ''
              222  GET_AWAITABLE    
              224  LOAD_CONST               None
              226  YIELD_FROM       
              228  POP_TOP          

 L. 239       230  LOAD_GLOBAL              WSMessage
              232  LOAD_GLOBAL              WSMsgType
              234  LOAD_ATTR                CLOSED
              236  LOAD_CONST               None
              238  LOAD_CONST               None
              240  CALL_FUNCTION_3       3  ''
              242  ROT_FOUR         
              244  POP_EXCEPT       
              246  RETURN_VALUE     
            248_0  COME_FROM           202  '202'

 L. 240       248  DUP_TOP          
              250  LOAD_GLOBAL              ClientError
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   284  'to 284'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 241       264  LOAD_CONST               True
              266  LOAD_FAST                'self'
              268  STORE_ATTR               _closed

 L. 242       270  LOAD_CONST               1006
              272  LOAD_FAST                'self'
              274  STORE_ATTR               _close_code

 L. 243       276  LOAD_GLOBAL              WS_CLOSED_MESSAGE
              278  ROT_FOUR         
              280  POP_EXCEPT       
              282  RETURN_VALUE     
            284_0  COME_FROM           254  '254'

 L. 244       284  DUP_TOP          
              286  LOAD_GLOBAL              WebSocketError
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   364  'to 364'
              294  POP_TOP          
              296  STORE_FAST               'exc'
              298  POP_TOP          
              300  SETUP_FINALLY       352  'to 352'

 L. 245       302  LOAD_FAST                'exc'
              304  LOAD_ATTR                code
              306  LOAD_FAST                'self'
              308  STORE_ATTR               _close_code

 L. 246       310  LOAD_FAST                'self'
              312  LOAD_ATTR                close
              314  LOAD_FAST                'exc'
              316  LOAD_ATTR                code
              318  LOAD_CONST               ('code',)
              320  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              322  GET_AWAITABLE    
              324  LOAD_CONST               None
              326  YIELD_FROM       
              328  POP_TOP          

 L. 247       330  LOAD_GLOBAL              WSMessage
              332  LOAD_GLOBAL              WSMsgType
              334  LOAD_ATTR                ERROR
              336  LOAD_FAST                'exc'
              338  LOAD_CONST               None
              340  CALL_FUNCTION_3       3  ''
              342  ROT_FOUR         
              344  POP_BLOCK        
              346  POP_EXCEPT       
              348  CALL_FINALLY        352  'to 352'
              350  RETURN_VALUE     
            352_0  COME_FROM           348  '348'
            352_1  COME_FROM_FINALLY   300  '300'
              352  LOAD_CONST               None
              354  STORE_FAST               'exc'
              356  DELETE_FAST              'exc'
              358  END_FINALLY      
              360  POP_EXCEPT       
              362  JUMP_FORWARD        450  'to 450'
            364_0  COME_FROM           290  '290'

 L. 248       364  DUP_TOP          
              366  LOAD_GLOBAL              Exception
              368  COMPARE_OP               exception-match
          370_372  POP_JUMP_IF_FALSE   448  'to 448'
              374  POP_TOP          
              376  STORE_FAST               'exc'
              378  POP_TOP          
              380  SETUP_FINALLY       436  'to 436'

 L. 249       382  LOAD_FAST                'exc'
              384  LOAD_FAST                'self'
              386  STORE_ATTR               _exception

 L. 250       388  LOAD_CONST               True
              390  LOAD_FAST                'self'
              392  STORE_ATTR               _closing

 L. 251       394  LOAD_CONST               1006
              396  LOAD_FAST                'self'
              398  STORE_ATTR               _close_code

 L. 252       400  LOAD_FAST                'self'
              402  LOAD_METHOD              close
              404  CALL_METHOD_0         0  ''
              406  GET_AWAITABLE    
              408  LOAD_CONST               None
              410  YIELD_FROM       
              412  POP_TOP          

 L. 253       414  LOAD_GLOBAL              WSMessage
              416  LOAD_GLOBAL              WSMsgType
              418  LOAD_ATTR                ERROR
              420  LOAD_FAST                'exc'
              422  LOAD_CONST               None
              424  CALL_FUNCTION_3       3  ''
              426  ROT_FOUR         
              428  POP_BLOCK        
              430  POP_EXCEPT       
              432  CALL_FINALLY        436  'to 436'
              434  RETURN_VALUE     
            436_0  COME_FROM           432  '432'
            436_1  COME_FROM_FINALLY   380  '380'
              436  LOAD_CONST               None
              438  STORE_FAST               'exc'
              440  DELETE_FAST              'exc'
              442  END_FINALLY      
              444  POP_EXCEPT       
              446  JUMP_FORWARD        450  'to 450'
            448_0  COME_FROM           370  '370'
              448  END_FINALLY      
            450_0  COME_FROM           446  '446'
            450_1  COME_FROM           362  '362'
            450_2  COME_FROM           192  '192'
            450_3  COME_FROM           156  '156'

 L. 255       450  LOAD_FAST                'msg'
              452  LOAD_ATTR                type
              454  LOAD_GLOBAL              WSMsgType
              456  LOAD_ATTR                CLOSE
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_FALSE   510  'to 510'

 L. 256       464  LOAD_CONST               True
              466  LOAD_FAST                'self'
              468  STORE_ATTR               _closing

 L. 257       470  LOAD_FAST                'msg'
              472  LOAD_ATTR                data
              474  LOAD_FAST                'self'
              476  STORE_ATTR               _close_code

 L. 258       478  LOAD_FAST                'self'
              480  LOAD_ATTR                _closed
          482_484  POP_JUMP_IF_TRUE    600  'to 600'
              486  LOAD_FAST                'self'
              488  LOAD_ATTR                _autoclose
          490_492  POP_JUMP_IF_FALSE   600  'to 600'

 L. 259       494  LOAD_FAST                'self'
              496  LOAD_METHOD              close
              498  CALL_METHOD_0         0  ''
              500  GET_AWAITABLE    
              502  LOAD_CONST               None
              504  YIELD_FROM       
              506  POP_TOP          
              508  JUMP_FORWARD        600  'to 600'
            510_0  COME_FROM           460  '460'

 L. 260       510  LOAD_FAST                'msg'
              512  LOAD_ATTR                type
              514  LOAD_GLOBAL              WSMsgType
              516  LOAD_ATTR                CLOSING
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   532  'to 532'

 L. 261       524  LOAD_CONST               True
              526  LOAD_FAST                'self'
              528  STORE_ATTR               _closing
              530  JUMP_FORWARD        600  'to 600'
            532_0  COME_FROM           520  '520'

 L. 262       532  LOAD_FAST                'msg'
              534  LOAD_ATTR                type
              536  LOAD_GLOBAL              WSMsgType
              538  LOAD_ATTR                PING
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   576  'to 576'
              546  LOAD_FAST                'self'
              548  LOAD_ATTR                _autoping
          550_552  POP_JUMP_IF_FALSE   576  'to 576'

 L. 263       554  LOAD_FAST                'self'
              556  LOAD_METHOD              pong
              558  LOAD_FAST                'msg'
              560  LOAD_ATTR                data
              562  CALL_METHOD_1         1  ''
              564  GET_AWAITABLE    
              566  LOAD_CONST               None
              568  YIELD_FROM       
              570  POP_TOP          

 L. 264       572  JUMP_BACK             0  'to 0'
              574  BREAK_LOOP          600  'to 600'
            576_0  COME_FROM           550  '550'
            576_1  COME_FROM           542  '542'

 L. 265       576  LOAD_FAST                'msg'
              578  LOAD_ATTR                type
              580  LOAD_GLOBAL              WSMsgType
              582  LOAD_ATTR                PONG
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   600  'to 600'
              590  LOAD_FAST                'self'
              592  LOAD_ATTR                _autoping
          594_596  POP_JUMP_IF_FALSE   600  'to 600'

 L. 266       598  JUMP_BACK             0  'to 0'
            600_0  COME_FROM           594  '594'
            600_1  COME_FROM           586  '586'
            600_2  COME_FROM           574  '574'
            600_3  COME_FROM           530  '530'
            600_4  COME_FROM           508  '508'
            600_5  COME_FROM           490  '490'
            600_6  COME_FROM           482  '482'

 L. 268       600  LOAD_FAST                'msg'
              602  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 344

    async def receive_str(self, *, timeout: Optional[float]=None) -> str:
        msg = await self.receive(timeout)
        if msg.type != WSMsgType.TEXT:
            raise TypeError('Received message {}:{!r} is not str'.format(msg.type, msg.data))
        return msg.data

    async def receive_bytes(self, *, timeout: Optional[float]=None) -> bytes:
        msg = await self.receive(timeout)
        if msg.type != WSMsgType.BINARY:
            raise TypeError('Received message {}:{!r} is not bytes'.format(msg.type, msg.data))
        return msg.data

    async def receive_json(self, *, loads: JSONDecoder=DEFAULT_JSON_DECODER, timeout: Optional[float]=None) -> Any:
        data = await self.receive_str(timeout=timeout)
        return loads(data)

    def __aiter__(self) -> 'ClientWebSocketResponse':
        return self

    async def __anext__(self) -> WSMessage:
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE,
         WSMsgType.CLOSING,
         WSMsgType.CLOSED):
            raise StopAsyncIteration
        return msg