# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\client_ws.py
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

    def __init__--- This code section failed: ---

 L.  45         0  LOAD_FAST                'response'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _response

 L.  46         6  LOAD_FAST                'response'
                8  LOAD_ATTR                connection
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _conn

 L.  48        14  LOAD_FAST                'writer'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _writer

 L.  49        20  LOAD_FAST                'reader'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _reader

 L.  50        26  LOAD_FAST                'protocol'
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _protocol

 L.  51        32  LOAD_CONST               False
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _closed

 L.  52        38  LOAD_CONST               False
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _closing

 L.  53        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _close_code

 L.  54        50  LOAD_FAST                'timeout'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _timeout

 L.  55        56  LOAD_FAST                'receive_timeout'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _receive_timeout

 L.  56        62  LOAD_FAST                'autoclose'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _autoclose

 L.  57        68  LOAD_FAST                'autoping'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _autoping

 L.  58        74  LOAD_FAST                'heartbeat'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _heartbeat

 L.  59        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _heartbeat_cb

 L.  60        86  LOAD_FAST                'heartbeat'
               88  LOAD_CONST               None
               90  <117>                 1  ''
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L.  61        94  LOAD_FAST                'heartbeat'
               96  LOAD_CONST               2.0
               98  BINARY_TRUE_DIVIDE
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _pong_heartbeat
            104_0  COME_FROM            92  '92'

 L.  62       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _pong_response_cb

 L.  63       110  LOAD_FAST                'loop'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _loop

 L.  64       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _waiting

 L.  65       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _exception

 L.  66       128  LOAD_FAST                'compress'
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _compress

 L.  67       134  LOAD_FAST                'client_notakeover'
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _client_notakeover

 L.  69       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _reset_heartbeat
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

Parse error at or near `<117>' instruction at offset 90

    def _cancel_heartbeat--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pong_response_cb
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  73        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pong_response_cb
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L.  74        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _pong_response_cb
             26_0  COME_FROM             8  '8'

 L.  76        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _heartbeat_cb
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L.  77        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _heartbeat_cb
               40  LOAD_METHOD              cancel
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L.  78        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _heartbeat_cb
             52_0  COME_FROM            34  '34'

Parse error at or near `None' instruction at offset -1

    def _reset_heartbeat--- This code section failed: ---

 L.  81         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cancel_heartbeat
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  83         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _heartbeat
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L.  84        18  LOAD_GLOBAL              call_later

 L.  85        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _send_heartbeat
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _heartbeat
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _loop

 L.  84        32  CALL_FUNCTION_3       3  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _heartbeat_cb
             38_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14

    def _send_heartbeat--- This code section failed: ---

 L.  89         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _heartbeat
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    74  'to 74'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_TRUE     74  'to 74'

 L.  93        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              create_task
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _writer
               26  LOAD_METHOD              ping
               28  CALL_METHOD_0         0  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L.  95        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _pong_response_cb
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L.  96        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _pong_response_cb
               48  LOAD_METHOD              cancel
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
             54_0  COME_FROM            42  '42'

 L.  97        54  LOAD_GLOBAL              call_later

 L.  98        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pong_not_received
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _pong_heartbeat
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _loop

 L.  97        68  CALL_FUNCTION_3       3  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _pong_response_cb
             74_0  COME_FROM            14  '14'
             74_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _pong_not_received(self) -> None:
        if not self._closed:
            self._closed = True
            self._close_code = 1006
            self._exception = asyncio.TimeoutError
            self._response.close

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

    def get_extra_info--- This code section failed: ---

 L. 130         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _response
                4  LOAD_ATTR                connection
                6  STORE_FAST               'conn'

 L. 131         8  LOAD_FAST                'conn'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 132        16  LOAD_FAST                'default'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 133        20  LOAD_FAST                'conn'
               22  LOAD_ATTR                transport
               24  STORE_FAST               'transport'

 L. 134        26  LOAD_FAST                'transport'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 135        34  LOAD_FAST                'default'
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 136        38  LOAD_FAST                'transport'
               40  LOAD_METHOD              get_extra_info
               42  LOAD_FAST                'name'
               44  LOAD_FAST                'default'
               46  CALL_METHOD_2         2  ''
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12

    def exception(self) -> Optional[BaseException]:
        return self._exception

    async def ping(self, message: bytes=b'') -> None:
        await self._writer.pingmessage

    async def pong(self, message: bytes=b'') -> None:
        await self._writer.pongmessage

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

 L. 169         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiting
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    42  'to 42'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_TRUE     42  'to 42'

 L. 170        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _reader
               20  LOAD_METHOD              feed_data
               22  LOAD_GLOBAL              WS_CLOSING_MESSAGE
               24  LOAD_CONST               0
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L. 171        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _waiting
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
             42_0  COME_FROM            14  '14'
             42_1  COME_FROM             8  '8'

 L. 173        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _closed
            46_48  POP_JUMP_IF_TRUE    418  'to 418'

 L. 174        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _cancel_heartbeat
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          

 L. 175        58  LOAD_CONST               True
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _closed

 L. 176        64  SETUP_FINALLY        90  'to 90'

 L. 177        66  LOAD_FAST                'self'
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
               88  JUMP_FORWARD        186  'to 186'
             90_0  COME_FROM_FINALLY    64  '64'

 L. 178        90  DUP_TOP          
               92  LOAD_GLOBAL              asyncio
               94  LOAD_ATTR                CancelledError
               96  <121>               126  ''
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 179       104  LOAD_CONST               1006
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _close_code

 L. 180       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _response
              114  LOAD_METHOD              close
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          

 L. 181       120  RAISE_VARARGS_0       0  'reraise'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        186  'to 186'

 L. 182       126  DUP_TOP          
              128  LOAD_GLOBAL              Exception
              130  <121>               184  ''
              132  POP_TOP          
              134  STORE_FAST               'exc'
              136  POP_TOP          
              138  SETUP_FINALLY       176  'to 176'

 L. 183       140  LOAD_CONST               1006
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _close_code

 L. 184       146  LOAD_FAST                'exc'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _exception

 L. 185       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _response
              156  LOAD_METHOD              close
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          

 L. 186       162  POP_BLOCK        
              164  POP_EXCEPT       
              166  LOAD_CONST               None
              168  STORE_FAST               'exc'
              170  DELETE_FAST              'exc'
              172  LOAD_CONST               True
              174  RETURN_VALUE     
            176_0  COME_FROM_FINALLY   138  '138'
              176  LOAD_CONST               None
              178  STORE_FAST               'exc'
              180  DELETE_FAST              'exc'
              182  <48>             
              184  <48>             
            186_0  COME_FROM           124  '124'
            186_1  COME_FROM            88  '88'

 L. 188       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _closing
              190  POP_JUMP_IF_FALSE   206  'to 206'

 L. 189       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _response
              196  LOAD_METHOD              close
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          

 L. 190       202  LOAD_CONST               True
              204  RETURN_VALUE     
            206_0  COME_FROM           414  '414'
            206_1  COME_FROM           390  '390'
            206_2  COME_FROM           190  '190'

 L. 193       206  SETUP_FINALLY       280  'to 280'

 L. 194       208  LOAD_GLOBAL              async_timeout
              210  LOAD_ATTR                timeout
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                _timeout
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _loop
              220  LOAD_CONST               ('loop',)
              222  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              224  SETUP_WITH          258  'to 258'
              226  POP_TOP          

 L. 195       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _reader
              232  LOAD_METHOD              read
              234  CALL_METHOD_0         0  ''
              236  GET_AWAITABLE    
              238  LOAD_CONST               None
              240  YIELD_FROM       
              242  STORE_FAST               'msg'
              244  POP_BLOCK        
              246  LOAD_CONST               None
              248  DUP_TOP          
              250  DUP_TOP          
              252  CALL_FUNCTION_3       3  ''
              254  POP_TOP          
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM_WITH      224  '224'
              258  <49>             
          260_262  POP_JUMP_IF_TRUE    266  'to 266'
              264  <48>             
            266_0  COME_FROM           260  '260'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          
              272  POP_EXCEPT       
              274  POP_TOP          
            276_0  COME_FROM           256  '256'
              276  POP_BLOCK        
              278  JUMP_FORWARD        380  'to 380'
            280_0  COME_FROM_FINALLY   206  '206'

 L. 196       280  DUP_TOP          
              282  LOAD_GLOBAL              asyncio
              284  LOAD_ATTR                CancelledError
          286_288  <121>               318  ''
              290  POP_TOP          
              292  POP_TOP          
              294  POP_TOP          

 L. 197       296  LOAD_CONST               1006
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _close_code

 L. 198       302  LOAD_FAST                'self'
              304  LOAD_ATTR                _response
              306  LOAD_METHOD              close
              308  CALL_METHOD_0         0  ''
              310  POP_TOP          

 L. 199       312  RAISE_VARARGS_0       0  'reraise'
              314  POP_EXCEPT       
              316  JUMP_FORWARD        380  'to 380'

 L. 200       318  DUP_TOP          
              320  LOAD_GLOBAL              Exception
          322_324  <121>               378  ''
              326  POP_TOP          
              328  STORE_FAST               'exc'
              330  POP_TOP          
              332  SETUP_FINALLY       370  'to 370'

 L. 201       334  LOAD_CONST               1006
              336  LOAD_FAST                'self'
              338  STORE_ATTR               _close_code

 L. 202       340  LOAD_FAST                'exc'
              342  LOAD_FAST                'self'
              344  STORE_ATTR               _exception

 L. 203       346  LOAD_FAST                'self'
              348  LOAD_ATTR                _response
              350  LOAD_METHOD              close
              352  CALL_METHOD_0         0  ''
              354  POP_TOP          

 L. 204       356  POP_BLOCK        
              358  POP_EXCEPT       
              360  LOAD_CONST               None
              362  STORE_FAST               'exc'
              364  DELETE_FAST              'exc'
              366  LOAD_CONST               True
              368  RETURN_VALUE     
            370_0  COME_FROM_FINALLY   332  '332'
              370  LOAD_CONST               None
              372  STORE_FAST               'exc'
              374  DELETE_FAST              'exc'
              376  <48>             
              378  <48>             
            380_0  COME_FROM           316  '316'
            380_1  COME_FROM           278  '278'

 L. 206       380  LOAD_FAST                'msg'
              382  LOAD_ATTR                type
              384  LOAD_GLOBAL              WSMsgType
              386  LOAD_ATTR                CLOSE
              388  COMPARE_OP               ==
              390  POP_JUMP_IF_FALSE_BACK   206  'to 206'

 L. 207       392  LOAD_FAST                'msg'
              394  LOAD_ATTR                data
              396  LOAD_FAST                'self'
              398  STORE_ATTR               _close_code

 L. 208       400  LOAD_FAST                'self'
              402  LOAD_ATTR                _response
              404  LOAD_METHOD              close
              406  CALL_METHOD_0         0  ''
              408  POP_TOP          

 L. 209       410  LOAD_CONST               True
              412  RETURN_VALUE     
              414  JUMP_BACK           206  'to 206'
              416  JUMP_FORWARD        422  'to 422'
            418_0  COME_FROM            46  '46'

 L. 211       418  LOAD_CONST               False
              420  RETURN_VALUE     
            422_0  COME_FROM           416  '416'

Parse error at or near `None' instruction at offset -1

    async def receive--- This code section failed: ---
              0_0  COME_FROM           632  '632'
              0_1  COME_FROM           606  '606'

 L. 215         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _waiting
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 216        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Concurrent call to receive() is not allowed'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 218        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _closed
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 219        24  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 220        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _closing
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 221        34  LOAD_FAST                'self'
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  POP_TOP          

 L. 222        48  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               50  RETURN_VALUE     
             52_0  COME_FROM            32  '32'

 L. 224        52  SETUP_FINALLY       202  'to 202'

 L. 225        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _loop
               58  LOAD_METHOD              create_future
               60  CALL_METHOD_0         0  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _waiting

 L. 226        66  SETUP_FINALLY       172  'to 172'

 L. 227        68  LOAD_GLOBAL              async_timeout
               70  LOAD_ATTR                timeout

 L. 228        72  LOAD_FAST                'timeout'
               74  JUMP_IF_TRUE_OR_POP    80  'to 80'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _receive_timeout
             80_0  COME_FROM            74  '74'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _loop

 L. 227        84  LOAD_CONST               ('loop',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  SETUP_WITH          122  'to 122'
               90  POP_TOP          

 L. 230        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _reader
               96  LOAD_METHOD              read
               98  CALL_METHOD_0         0  ''
              100  GET_AWAITABLE    
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  STORE_FAST               'msg'
              108  POP_BLOCK        
              110  LOAD_CONST               None
              112  DUP_TOP          
              114  DUP_TOP          
              116  CALL_FUNCTION_3       3  ''
              118  POP_TOP          
              120  JUMP_FORWARD        138  'to 138'
            122_0  COME_FROM_WITH       88  '88'
              122  <49>             
              124  POP_JUMP_IF_TRUE    128  'to 128'
              126  <48>             
            128_0  COME_FROM           124  '124'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          
              134  POP_EXCEPT       
              136  POP_TOP          
            138_0  COME_FROM           120  '120'

 L. 231       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _reset_heartbeat
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          
              146  POP_BLOCK        

 L. 233       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _waiting
              152  STORE_FAST               'waiter'

 L. 234       154  LOAD_CONST               None
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _waiting

 L. 235       160  LOAD_GLOBAL              set_result
              162  LOAD_FAST                'waiter'
              164  LOAD_CONST               True
              166  CALL_FUNCTION_2       2  ''
              168  POP_TOP          
              170  JUMP_FORWARD        196  'to 196'
            172_0  COME_FROM_FINALLY    66  '66'

 L. 233       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _waiting
              176  STORE_FAST               'waiter'

 L. 234       178  LOAD_CONST               None
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _waiting

 L. 235       184  LOAD_GLOBAL              set_result
              186  LOAD_FAST                'waiter'
              188  LOAD_CONST               True
              190  CALL_FUNCTION_2       2  ''
              192  POP_TOP          
              194  <48>             
            196_0  COME_FROM           170  '170'
              196  POP_BLOCK        
          198_200  JUMP_FORWARD        484  'to 484'
            202_0  COME_FROM_FINALLY    52  '52'

 L. 236       202  DUP_TOP          
              204  LOAD_GLOBAL              asyncio
              206  LOAD_ATTR                CancelledError
              208  LOAD_GLOBAL              asyncio
              210  LOAD_ATTR                TimeoutError
              212  BUILD_TUPLE_2         2 
              214  <121>               236  ''
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 237       222  LOAD_CONST               1006
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _close_code

 L. 238       228  RAISE_VARARGS_0       0  'reraise'
              230  POP_EXCEPT       
          232_234  JUMP_FORWARD        484  'to 484'

 L. 239       236  DUP_TOP          
              238  LOAD_GLOBAL              EofStream
          240_242  <121>               288  ''
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 240       250  LOAD_CONST               1000
              252  LOAD_FAST                'self'
              254  STORE_ATTR               _close_code

 L. 241       256  LOAD_FAST                'self'
              258  LOAD_METHOD              close
              260  CALL_METHOD_0         0  ''
              262  GET_AWAITABLE    
              264  LOAD_CONST               None
              266  YIELD_FROM       
              268  POP_TOP          

 L. 242       270  LOAD_GLOBAL              WSMessage
              272  LOAD_GLOBAL              WSMsgType
              274  LOAD_ATTR                CLOSED
              276  LOAD_CONST               None
              278  LOAD_CONST               None
              280  CALL_FUNCTION_3       3  ''
              282  ROT_FOUR         
              284  POP_EXCEPT       
              286  RETURN_VALUE     

 L. 243       288  DUP_TOP          
              290  LOAD_GLOBAL              ClientError
          292_294  <121>               322  ''
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 244       302  LOAD_CONST               True
              304  LOAD_FAST                'self'
              306  STORE_ATTR               _closed

 L. 245       308  LOAD_CONST               1006
              310  LOAD_FAST                'self'
              312  STORE_ATTR               _close_code

 L. 246       314  LOAD_GLOBAL              WS_CLOSED_MESSAGE
              316  ROT_FOUR         
              318  POP_EXCEPT       
              320  RETURN_VALUE     

 L. 247       322  DUP_TOP          
              324  LOAD_GLOBAL              WebSocketError
          326_328  <121>               400  ''
              330  POP_TOP          
              332  STORE_FAST               'exc'
              334  POP_TOP          
              336  SETUP_FINALLY       392  'to 392'

 L. 248       338  LOAD_FAST                'exc'
              340  LOAD_ATTR                code
              342  LOAD_FAST                'self'
              344  STORE_ATTR               _close_code

 L. 249       346  LOAD_FAST                'self'
              348  LOAD_ATTR                close
              350  LOAD_FAST                'exc'
              352  LOAD_ATTR                code
              354  LOAD_CONST               ('code',)
              356  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              358  GET_AWAITABLE    
              360  LOAD_CONST               None
              362  YIELD_FROM       
              364  POP_TOP          

 L. 250       366  LOAD_GLOBAL              WSMessage
              368  LOAD_GLOBAL              WSMsgType
              370  LOAD_ATTR                ERROR
              372  LOAD_FAST                'exc'
              374  LOAD_CONST               None
              376  CALL_FUNCTION_3       3  ''
              378  POP_BLOCK        
              380  ROT_FOUR         
              382  POP_EXCEPT       
              384  LOAD_CONST               None
              386  STORE_FAST               'exc'
              388  DELETE_FAST              'exc'
              390  RETURN_VALUE     
            392_0  COME_FROM_FINALLY   336  '336'
              392  LOAD_CONST               None
              394  STORE_FAST               'exc'
              396  DELETE_FAST              'exc'
              398  <48>             

 L. 251       400  DUP_TOP          
              402  LOAD_GLOBAL              Exception
          404_406  <121>               482  ''
              408  POP_TOP          
              410  STORE_FAST               'exc'
              412  POP_TOP          
              414  SETUP_FINALLY       474  'to 474'

 L. 252       416  LOAD_FAST                'exc'
              418  LOAD_FAST                'self'
              420  STORE_ATTR               _exception

 L. 253       422  LOAD_CONST               True
              424  LOAD_FAST                'self'
              426  STORE_ATTR               _closing

 L. 254       428  LOAD_CONST               1006
              430  LOAD_FAST                'self'
              432  STORE_ATTR               _close_code

 L. 255       434  LOAD_FAST                'self'
              436  LOAD_METHOD              close
              438  CALL_METHOD_0         0  ''
              440  GET_AWAITABLE    
              442  LOAD_CONST               None
              444  YIELD_FROM       
              446  POP_TOP          

 L. 256       448  LOAD_GLOBAL              WSMessage
              450  LOAD_GLOBAL              WSMsgType
              452  LOAD_ATTR                ERROR
              454  LOAD_FAST                'exc'
              456  LOAD_CONST               None
              458  CALL_FUNCTION_3       3  ''
              460  POP_BLOCK        
              462  ROT_FOUR         
              464  POP_EXCEPT       
              466  LOAD_CONST               None
              468  STORE_FAST               'exc'
              470  DELETE_FAST              'exc'
              472  RETURN_VALUE     
            474_0  COME_FROM_FINALLY   414  '414'
              474  LOAD_CONST               None
              476  STORE_FAST               'exc'
              478  DELETE_FAST              'exc'
              480  <48>             
              482  <48>             
            484_0  COME_FROM           232  '232'
            484_1  COME_FROM           198  '198'

 L. 258       484  LOAD_FAST                'msg'
              486  LOAD_ATTR                type
              488  LOAD_GLOBAL              WSMsgType
              490  LOAD_ATTR                CLOSE
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   544  'to 544'

 L. 259       498  LOAD_CONST               True
              500  LOAD_FAST                'self'
              502  STORE_ATTR               _closing

 L. 260       504  LOAD_FAST                'msg'
              506  LOAD_ATTR                data
              508  LOAD_FAST                'self'
              510  STORE_ATTR               _close_code

 L. 261       512  LOAD_FAST                'self'
              514  LOAD_ATTR                _closed
          516_518  POP_JUMP_IF_TRUE    634  'to 634'
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                _autoclose
          524_526  POP_JUMP_IF_FALSE   634  'to 634'

 L. 262       528  LOAD_FAST                'self'
              530  LOAD_METHOD              close
              532  CALL_METHOD_0         0  ''
              534  GET_AWAITABLE    
              536  LOAD_CONST               None
              538  YIELD_FROM       
              540  POP_TOP          
              542  JUMP_FORWARD        634  'to 634'
            544_0  COME_FROM           494  '494'

 L. 263       544  LOAD_FAST                'msg'
              546  LOAD_ATTR                type
              548  LOAD_GLOBAL              WSMsgType
              550  LOAD_ATTR                CLOSING
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   566  'to 566'

 L. 264       558  LOAD_CONST               True
              560  LOAD_FAST                'self'
              562  STORE_ATTR               _closing
              564  JUMP_FORWARD        634  'to 634'
            566_0  COME_FROM           554  '554'

 L. 265       566  LOAD_FAST                'msg'
              568  LOAD_ATTR                type
              570  LOAD_GLOBAL              WSMsgType
              572  LOAD_ATTR                PING
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   610  'to 610'
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                _autoping
          584_586  POP_JUMP_IF_FALSE   610  'to 610'

 L. 266       588  LOAD_FAST                'self'
              590  LOAD_METHOD              pong
              592  LOAD_FAST                'msg'
              594  LOAD_ATTR                data
              596  CALL_METHOD_1         1  ''
              598  GET_AWAITABLE    
              600  LOAD_CONST               None
              602  YIELD_FROM       
              604  POP_TOP          

 L. 267       606  JUMP_BACK             0  'to 0'
              608  BREAK_LOOP          634  'to 634'
            610_0  COME_FROM           584  '584'
            610_1  COME_FROM           576  '576'

 L. 268       610  LOAD_FAST                'msg'
              612  LOAD_ATTR                type
              614  LOAD_GLOBAL              WSMsgType
              616  LOAD_ATTR                PONG
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_FALSE   634  'to 634'
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                _autoping
          628_630  POP_JUMP_IF_FALSE   634  'to 634'

 L. 269       632  JUMP_BACK             0  'to 0'
            634_0  COME_FROM           628  '628'
            634_1  COME_FROM           620  '620'
            634_2  COME_FROM           608  '608'
            634_3  COME_FROM           564  '564'
            634_4  COME_FROM           542  '542'
            634_5  COME_FROM           524  '524'
            634_6  COME_FROM           516  '516'

 L. 271       634  LOAD_FAST                'msg'
              636  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 6

    async def receive_str(self, *, timeout: Optional[float]=None) -> str:
        msg = await self.receivetimeout
        if msg.type != WSMsgType.TEXT:
            raise TypeError(f"Received message {msg.type}:{msg.data!r} is not str")
        return msg.data

    async def receive_bytes(self, *, timeout: Optional[float]=None) -> bytes:
        msg = await self.receivetimeout
        if msg.type != WSMsgType.BINARY:
            raise TypeError(f"Received message {msg.type}:{msg.data!r} is not bytes")
        return msg.data

    async def receive_json(self, *, loads: JSONDecoder=DEFAULT_JSON_DECODER, timeout: Optional[float]=None) -> Any:
        data = await self.receive_str(timeout=timeout)
        return loads(data)

    def __aiter__(self) -> 'ClientWebSocketResponse':
        return self

    async def __anext__--- This code section failed: ---

 L. 298         0  LOAD_FAST                'self'
                2  LOAD_METHOD              receive
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'msg'

 L. 299        14  LOAD_FAST                'msg'
               16  LOAD_ATTR                type
               18  LOAD_GLOBAL              WSMsgType
               20  LOAD_ATTR                CLOSE
               22  LOAD_GLOBAL              WSMsgType
               24  LOAD_ATTR                CLOSING
               26  LOAD_GLOBAL              WSMsgType
               28  LOAD_ATTR                CLOSED
               30  BUILD_TUPLE_3         3 
               32  <118>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 300        36  LOAD_GLOBAL              StopAsyncIteration
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 301        40  LOAD_FAST                'msg'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 32