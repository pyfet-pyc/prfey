# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\http_websocket.py
"""WebSocket protocol versions 13 and 8."""
import asyncio, collections, json, random, re, sys, zlib
from enum import IntEnum
from struct import Struct
from typing import Any, Callable, List, Optional, Tuple, Union
from .base_protocol import BaseProtocol
from .helpers import NO_EXTENSIONS
from .log import ws_logger
from .streams import DataQueue
__all__ = ('WS_CLOSED_MESSAGE', 'WS_CLOSING_MESSAGE', 'WS_KEY', 'WebSocketReader',
           'WebSocketWriter', 'WSMessage', 'WebSocketError', 'WSMsgType', 'WSCloseCode')

class WSCloseCode(IntEnum):
    OK = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    INVALID_TEXT = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXTENSION = 1010
    INTERNAL_ERROR = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013


ALLOWED_CLOSE_CODES = {int(i) for i in WSCloseCode}

class WSMsgType(IntEnum):
    CONTINUATION = 0
    TEXT = 1
    BINARY = 2
    PING = 9
    PONG = 10
    CLOSE = 8
    CLOSING = 256
    CLOSED = 257
    ERROR = 258
    text = TEXT
    binary = BINARY
    ping = PING
    pong = PONG
    close = CLOSE
    closing = CLOSING
    closed = CLOSED
    error = ERROR


WS_KEY = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
UNPACK_LEN2 = Struct('!H').unpack_from
UNPACK_LEN3 = Struct('!Q').unpack_from
UNPACK_CLOSE_CODE = Struct('!H').unpack
PACK_LEN1 = Struct('!BB').pack
PACK_LEN2 = Struct('!BBH').pack
PACK_LEN3 = Struct('!BBQ').pack
PACK_CLOSE_CODE = Struct('!H').pack
MSG_SIZE = 16384
DEFAULT_LIMIT = 65536
_WSMessageBase = collections.namedtuple('_WSMessageBase', [
 'type', 'data', 'extra'])

class WSMessage(_WSMessageBase):

    def json(self, *, loads: Callable[([Any], Any)]=json.loads) -> Any:
        """Return parsed JSON data.

        .. versionadded:: 0.22
        """
        return loads(self.data)


WS_CLOSED_MESSAGE = WSMessage(WSMsgType.CLOSED, None, None)
WS_CLOSING_MESSAGE = WSMessage(WSMsgType.CLOSING, None, None)

class WebSocketError(Exception):
    __doc__ = 'WebSocket protocol parser error.'

    def __init__(self, code, message):
        self.code = code
        super().__init__(code, message)

    def __str__(self) -> str:
        return self.args[1]


class WSHandshakeError(Exception):
    __doc__ = 'WebSocket protocol handshake error.'


native_byteorder = sys.byteorder
_XOR_TABLE = [bytes((a ^ b for a in range(256))) for b in range(256)]

def _websocket_mask_python(mask: bytes, data: bytearray) -> None:
    """Websocket masking function.

    `mask` is a `bytes` object of length 4; `data` is a `bytearray`
    object of any length. The contents of `data` are masked with `mask`,
    as specified in section 5.3 of RFC 6455.

    Note that this function mutates the `data` argument.

    This pure-python implementation may be replaced by an optimized
    version when available.

    """
    assert isinstance(data, bytearray), data
    assert len(mask) == 4, mask
    if data:
        a, b, c, d = (_XOR_TABLE[n] for n in mask)
        data[::4] = data[::4].translate(a)
        data[1::4] = data[1::4].translate(b)
        data[2::4] = data[2::4].translate(c)
        data[3::4] = data[3::4].translate(d)


if NO_EXTENSIONS:
    _websocket_mask = _websocket_mask_python
else:
    pass
try:
    from ._websocket import _websocket_mask_cython
    _websocket_mask = _websocket_mask_cython
except ImportError:
    _websocket_mask = _websocket_mask_python
else:
    _WS_DEFLATE_TRAILING = bytes([0, 0, 255, 255])
    _WS_EXT_RE = re.compile('^(?:;\\s*(?:(server_no_context_takeover)|(client_no_context_takeover)|(server_max_window_bits(?:=(\\d+))?)|(client_max_window_bits(?:=(\\d+))?)))*$')
    _WS_EXT_RE_SPLIT = re.compile('permessage-deflate([^,]+)?')

    def ws_ext_parse--- This code section failed: ---

 L. 166         0  LOAD_FAST                'extstr'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 167         4  LOAD_CONST               (0, False)
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 169         8  LOAD_CONST               0
               10  STORE_FAST               'compress'

 L. 170        12  LOAD_CONST               False
               14  STORE_FAST               'notakeover'

 L. 171        16  LOAD_GLOBAL              _WS_EXT_RE_SPLIT
               18  LOAD_METHOD              finditer
               20  LOAD_FAST                'extstr'
               22  CALL_METHOD_1         1  ''
               24  GET_ITER         
             26_0  COME_FROM           230  '230'
             26_1  COME_FROM           210  '210'
             26_2  COME_FROM           206  '206'
             26_3  COME_FROM           118  '118'
               26  FOR_ITER            232  'to 232'
               28  STORE_FAST               'ext'

 L. 172        30  LOAD_FAST                'ext'
               32  LOAD_METHOD              group
               34  LOAD_CONST               1
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'defext'

 L. 174        40  LOAD_FAST                'defext'
               42  POP_JUMP_IF_TRUE     52  'to 52'

 L. 175        44  LOAD_CONST               15
               46  STORE_FAST               'compress'

 L. 176        48  POP_TOP          
               50  BREAK_LOOP          232  'to 232'
             52_0  COME_FROM            42  '42'

 L. 177        52  LOAD_GLOBAL              _WS_EXT_RE
               54  LOAD_METHOD              match
               56  LOAD_FAST                'defext'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'match'

 L. 178        62  LOAD_FAST                'match'
               64  POP_JUMP_IF_FALSE   208  'to 208'

 L. 179        66  LOAD_CONST               15
               68  STORE_FAST               'compress'

 L. 180        70  LOAD_FAST                'isserver'
               72  POP_JUMP_IF_FALSE   140  'to 140'

 L. 183        74  LOAD_FAST                'match'
               76  LOAD_METHOD              group
               78  LOAD_CONST               4
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE   120  'to 120'

 L. 184        84  LOAD_GLOBAL              int
               86  LOAD_FAST                'match'
               88  LOAD_METHOD              group
               90  LOAD_CONST               4
               92  CALL_METHOD_1         1  ''
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'compress'

 L. 189        98  LOAD_FAST                'compress'
              100  LOAD_CONST               15
              102  COMPARE_OP               >
              104  POP_JUMP_IF_TRUE    114  'to 114'
              106  LOAD_FAST                'compress'
              108  LOAD_CONST               9
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   120  'to 120'
            114_0  COME_FROM           104  '104'

 L. 190       114  LOAD_CONST               0
              116  STORE_FAST               'compress'

 L. 191       118  JUMP_BACK            26  'to 26'
            120_0  COME_FROM           112  '112'
            120_1  COME_FROM            82  '82'

 L. 192       120  LOAD_FAST                'match'
              122  LOAD_METHOD              group
              124  LOAD_CONST               1
              126  CALL_METHOD_1         1  ''
              128  POP_JUMP_IF_FALSE   134  'to 134'

 L. 193       130  LOAD_CONST               True
              132  STORE_FAST               'notakeover'
            134_0  COME_FROM           128  '128'

 L. 195       134  POP_TOP          
              136  BREAK_LOOP          232  'to 232'
              138  JUMP_FORWARD        230  'to 230'
            140_0  COME_FROM            72  '72'

 L. 197       140  LOAD_FAST                'match'
              142  LOAD_METHOD              group
              144  LOAD_CONST               6
              146  CALL_METHOD_1         1  ''
              148  POP_JUMP_IF_FALSE   188  'to 188'

 L. 198       150  LOAD_GLOBAL              int
              152  LOAD_FAST                'match'
              154  LOAD_METHOD              group
              156  LOAD_CONST               6
              158  CALL_METHOD_1         1  ''
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'compress'

 L. 203       164  LOAD_FAST                'compress'
              166  LOAD_CONST               15
              168  COMPARE_OP               >
              170  POP_JUMP_IF_TRUE    180  'to 180'
              172  LOAD_FAST                'compress'
              174  LOAD_CONST               9
              176  COMPARE_OP               <
              178  POP_JUMP_IF_FALSE   188  'to 188'
            180_0  COME_FROM           170  '170'

 L. 204       180  LOAD_GLOBAL              WSHandshakeError
              182  LOAD_STR                 'Invalid window size'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           148  '148'

 L. 205       188  LOAD_FAST                'match'
              190  LOAD_METHOD              group
              192  LOAD_CONST               2
              194  CALL_METHOD_1         1  ''
              196  POP_JUMP_IF_FALSE   202  'to 202'

 L. 206       198  LOAD_CONST               True
              200  STORE_FAST               'notakeover'
            202_0  COME_FROM           196  '196'

 L. 208       202  POP_TOP          
              204  BREAK_LOOP          232  'to 232'
              206  JUMP_BACK            26  'to 26'
            208_0  COME_FROM            64  '64'

 L. 210       208  LOAD_FAST                'isserver'
              210  POP_JUMP_IF_TRUE_BACK    26  'to 26'

 L. 211       212  LOAD_GLOBAL              WSHandshakeError
              214  LOAD_STR                 'Extension for deflate not supported'

 L. 212       216  LOAD_FAST                'ext'
              218  LOAD_METHOD              group
              220  LOAD_CONST               1
              222  CALL_METHOD_1         1  ''

 L. 211       224  BINARY_ADD       
              226  CALL_FUNCTION_1       1  ''
              228  RAISE_VARARGS_1       1  'exception instance'
            230_0  COME_FROM           138  '138'
              230  JUMP_BACK            26  'to 26'
            232_0  COME_FROM           204  '204'
            232_1  COME_FROM           136  '136'
            232_2  COME_FROM            50  '50'
            232_3  COME_FROM            26  '26'

 L. 214       232  LOAD_FAST                'compress'
              234  LOAD_FAST                'notakeover'
              236  BUILD_TUPLE_2         2 
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 232


    def ws_ext_gen(compress: int=15, isserver: bool=False, server_notakeover: bool=False) -> str:
        if compress < 9 or (compress > 15):
            raise ValueError('Compress wbits must between 9 and 15, zlib does not support wbits=8')
        enabledext = ['permessage-deflate']
        if not isserver:
            enabledext.append('client_max_window_bits')
        if compress < 15:
            enabledext.append('server_max_window_bits=' + str(compress))
        if server_notakeover:
            enabledext.append('server_no_context_takeover')
        return '; '.join(enabledext)


    class WSParserState(IntEnum):
        READ_HEADER = 1
        READ_PAYLOAD_LENGTH = 2
        READ_PAYLOAD_MASK = 3
        READ_PAYLOAD = 4


    class WebSocketReader:

        def __init__(self, queue: DataQueue[WSMessage], max_msg_size: int, compress: bool=True) -> None:
            self.queue = queue
            self._max_msg_size = max_msg_size
            self._exc = None
            self._partial = bytearray()
            self._state = WSParserState.READ_HEADER
            self._opcode = None
            self._frame_fin = False
            self._frame_opcode = None
            self._frame_payload = bytearray()
            self._tail = b''
            self._has_mask = False
            self._frame_mask = None
            self._payload_length = 0
            self._payload_length_flag = 0
            self._compressed = None
            self._decompressobj = None
            self._compress = compress

        def feed_eof(self) -> None:
            self.queue.feed_eof()

        def feed_data--- This code section failed: ---

 L. 273         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _exc
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 274         6  LOAD_CONST               True
                8  LOAD_FAST                'data'
               10  BUILD_TUPLE_2         2 
               12  RETURN_VALUE     
             14_0  COME_FROM             4  '4'

 L. 276        14  SETUP_FINALLY        28  'to 28'

 L. 277        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _feed_data
               20  LOAD_FAST                'data'
               22  CALL_METHOD_1         1  ''
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    14  '14'

 L. 278        28  DUP_TOP          
               30  LOAD_GLOBAL              Exception
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    84  'to 84'
               36  POP_TOP          
               38  STORE_FAST               'exc'
               40  POP_TOP          
               42  SETUP_FINALLY        72  'to 72'

 L. 279        44  LOAD_FAST                'exc'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _exc

 L. 280        50  LOAD_FAST                'self'
               52  LOAD_ATTR                queue
               54  LOAD_METHOD              set_exception
               56  LOAD_FAST                'exc'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 281        62  POP_BLOCK        
               64  POP_EXCEPT       
               66  CALL_FINALLY         72  'to 72'
               68  LOAD_CONST               (True, b'')
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'
             72_1  COME_FROM_FINALLY    42  '42'
               72  LOAD_CONST               None
               74  STORE_FAST               'exc'
               76  DELETE_FAST              'exc'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            34  '34'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'

Parse error at or near `POP_EXCEPT' instruction at offset 64

        def _feed_data--- This code section failed: ---

 L. 284         0  LOAD_FAST                'self'
                2  LOAD_METHOD              parse_frame
                4  LOAD_FAST                'data'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM           890  '890'
             10_1  COME_FROM           860  '860'
             10_2  COME_FROM           500  '500'
             10_3  COME_FROM           408  '408'
             10_4  COME_FROM           358  '358'
             10_5  COME_FROM           316  '316'
             10_6  COME_FROM           274  '274'
            10_12  FOR_ITER            892  'to 892'
               14  UNPACK_SEQUENCE_4     4 
               16  STORE_FAST               'fin'
               18  STORE_FAST               'opcode'
               20  STORE_FAST               'payload'
               22  STORE_FAST               'compressed'

 L. 285        24  LOAD_FAST                'compressed'
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _decompressobj
               32  POP_JUMP_IF_TRUE     52  'to 52'

 L. 286        34  LOAD_GLOBAL              zlib
               36  LOAD_ATTR                decompressobj
               38  LOAD_GLOBAL              zlib
               40  LOAD_ATTR                MAX_WBITS
               42  UNARY_NEGATIVE   
               44  LOAD_CONST               ('wbits',)
               46  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _decompressobj
             52_0  COME_FROM            32  '32'
             52_1  COME_FROM            26  '26'

 L. 287        52  LOAD_FAST                'opcode'
               54  LOAD_GLOBAL              WSMsgType
               56  LOAD_ATTR                CLOSE
               58  COMPARE_OP               ==
            60_62  POP_JUMP_IF_FALSE   276  'to 276'

 L. 288        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'payload'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               2
               72  COMPARE_OP               >=
               74  POP_JUMP_IF_FALSE   218  'to 218'

 L. 289        76  LOAD_GLOBAL              UNPACK_CLOSE_CODE
               78  LOAD_FAST                'payload'
               80  LOAD_CONST               None
               82  LOAD_CONST               2
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  STORE_FAST               'close_code'

 L. 290        96  LOAD_FAST                'close_code'
               98  LOAD_CONST               3000
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   130  'to 130'

 L. 291       104  LOAD_FAST                'close_code'
              106  LOAD_GLOBAL              ALLOWED_CLOSE_CODES
              108  COMPARE_OP               not-in

 L. 290       110  POP_JUMP_IF_FALSE   130  'to 130'

 L. 292       112  LOAD_GLOBAL              WebSocketError

 L. 293       114  LOAD_GLOBAL              WSCloseCode
              116  LOAD_ATTR                PROTOCOL_ERROR

 L. 294       118  LOAD_STR                 'Invalid close code: {}'
              120  LOAD_METHOD              format
              122  LOAD_FAST                'close_code'
              124  CALL_METHOD_1         1  ''

 L. 292       126  CALL_FUNCTION_2       2  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           110  '110'
            130_1  COME_FROM           102  '102'

 L. 295       130  SETUP_FINALLY       154  'to 154'

 L. 296       132  LOAD_FAST                'payload'
              134  LOAD_CONST               2
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  LOAD_METHOD              decode
              144  LOAD_STR                 'utf-8'
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'close_message'
              150  POP_BLOCK        
              152  JUMP_FORWARD        202  'to 202'
            154_0  COME_FROM_FINALLY   130  '130'

 L. 297       154  DUP_TOP          
              156  LOAD_GLOBAL              UnicodeDecodeError
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   200  'to 200'
              162  POP_TOP          
              164  STORE_FAST               'exc'
              166  POP_TOP          
              168  SETUP_FINALLY       188  'to 188'

 L. 298       170  LOAD_GLOBAL              WebSocketError

 L. 299       172  LOAD_GLOBAL              WSCloseCode
              174  LOAD_ATTR                INVALID_TEXT

 L. 300       176  LOAD_STR                 'Invalid UTF-8 text message'

 L. 298       178  CALL_FUNCTION_2       2  ''

 L. 300       180  LOAD_FAST                'exc'

 L. 298       182  RAISE_VARARGS_2       2  'exception instance with __cause__'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM_FINALLY   168  '168'
              188  LOAD_CONST               None
              190  STORE_FAST               'exc'
              192  DELETE_FAST              'exc'
              194  END_FINALLY      
              196  POP_EXCEPT       
              198  JUMP_FORWARD        202  'to 202'
            200_0  COME_FROM           160  '160'
              200  END_FINALLY      
            202_0  COME_FROM           198  '198'
            202_1  COME_FROM           152  '152'

 L. 301       202  LOAD_GLOBAL              WSMessage
              204  LOAD_GLOBAL              WSMsgType
              206  LOAD_ATTR                CLOSE
              208  LOAD_FAST                'close_code'
              210  LOAD_FAST                'close_message'
              212  CALL_FUNCTION_3       3  ''
              214  STORE_FAST               'msg'
              216  JUMP_FORWARD        260  'to 260'
            218_0  COME_FROM            74  '74'

 L. 302       218  LOAD_FAST                'payload'
              220  POP_JUMP_IF_FALSE   246  'to 246'

 L. 303       222  LOAD_GLOBAL              WebSocketError

 L. 304       224  LOAD_GLOBAL              WSCloseCode
              226  LOAD_ATTR                PROTOCOL_ERROR

 L. 305       228  LOAD_STR                 'Invalid close frame: {} {} {!r}'
              230  LOAD_METHOD              format

 L. 306       232  LOAD_FAST                'fin'

 L. 306       234  LOAD_FAST                'opcode'

 L. 306       236  LOAD_FAST                'payload'

 L. 305       238  CALL_METHOD_3         3  ''

 L. 303       240  CALL_FUNCTION_2       2  ''
              242  RAISE_VARARGS_1       1  'exception instance'
              244  JUMP_FORWARD        260  'to 260'
            246_0  COME_FROM           220  '220'

 L. 308       246  LOAD_GLOBAL              WSMessage
              248  LOAD_GLOBAL              WSMsgType
              250  LOAD_ATTR                CLOSE
              252  LOAD_CONST               0
              254  LOAD_STR                 ''
              256  CALL_FUNCTION_3       3  ''
              258  STORE_FAST               'msg'
            260_0  COME_FROM           244  '244'
            260_1  COME_FROM           216  '216'

 L. 310       260  LOAD_FAST                'self'
              262  LOAD_ATTR                queue
              264  LOAD_METHOD              feed_data
              266  LOAD_FAST                'msg'
              268  LOAD_CONST               0
              270  CALL_METHOD_2         2  ''
              272  POP_TOP          
              274  JUMP_BACK            10  'to 10'
            276_0  COME_FROM            60  '60'

 L. 312       276  LOAD_FAST                'opcode'
              278  LOAD_GLOBAL              WSMsgType
              280  LOAD_ATTR                PING
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   318  'to 318'

 L. 313       288  LOAD_FAST                'self'
              290  LOAD_ATTR                queue
              292  LOAD_METHOD              feed_data

 L. 314       294  LOAD_GLOBAL              WSMessage
              296  LOAD_GLOBAL              WSMsgType
              298  LOAD_ATTR                PING
              300  LOAD_FAST                'payload'
              302  LOAD_STR                 ''
              304  CALL_FUNCTION_3       3  ''

 L. 314       306  LOAD_GLOBAL              len
              308  LOAD_FAST                'payload'
              310  CALL_FUNCTION_1       1  ''

 L. 313       312  CALL_METHOD_2         2  ''
              314  POP_TOP          
              316  JUMP_BACK            10  'to 10'
            318_0  COME_FROM           284  '284'

 L. 316       318  LOAD_FAST                'opcode'
              320  LOAD_GLOBAL              WSMsgType
              322  LOAD_ATTR                PONG
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   360  'to 360'

 L. 317       330  LOAD_FAST                'self'
              332  LOAD_ATTR                queue
              334  LOAD_METHOD              feed_data

 L. 318       336  LOAD_GLOBAL              WSMessage
              338  LOAD_GLOBAL              WSMsgType
              340  LOAD_ATTR                PONG
              342  LOAD_FAST                'payload'
              344  LOAD_STR                 ''
              346  CALL_FUNCTION_3       3  ''

 L. 318       348  LOAD_GLOBAL              len
              350  LOAD_FAST                'payload'
              352  CALL_FUNCTION_1       1  ''

 L. 317       354  CALL_METHOD_2         2  ''
              356  POP_TOP          
              358  JUMP_BACK            10  'to 10'
            360_0  COME_FROM           326  '326'

 L. 320       360  LOAD_FAST                'opcode'

 L. 321       362  LOAD_GLOBAL              WSMsgType
              364  LOAD_ATTR                TEXT

 L. 321       366  LOAD_GLOBAL              WSMsgType
              368  LOAD_ATTR                BINARY

 L. 320       370  BUILD_TUPLE_2         2 
              372  COMPARE_OP               not-in
          374_376  POP_JUMP_IF_FALSE   410  'to 410'

 L. 321       378  LOAD_FAST                'self'
              380  LOAD_ATTR                _opcode
              382  LOAD_CONST               None
              384  COMPARE_OP               is

 L. 320   386_388  POP_JUMP_IF_FALSE   410  'to 410'

 L. 322       390  LOAD_GLOBAL              WebSocketError

 L. 323       392  LOAD_GLOBAL              WSCloseCode
              394  LOAD_ATTR                PROTOCOL_ERROR

 L. 324       396  LOAD_STR                 'Unexpected opcode={!r}'
              398  LOAD_METHOD              format
              400  LOAD_FAST                'opcode'
              402  CALL_METHOD_1         1  ''

 L. 322       404  CALL_FUNCTION_2       2  ''
              406  RAISE_VARARGS_1       1  'exception instance'
              408  JUMP_BACK            10  'to 10'
            410_0  COME_FROM           386  '386'
            410_1  COME_FROM           374  '374'

 L. 327       410  LOAD_FAST                'fin'
          412_414  POP_JUMP_IF_TRUE    502  'to 502'

 L. 329       416  LOAD_FAST                'opcode'
              418  LOAD_GLOBAL              WSMsgType
              420  LOAD_ATTR                CONTINUATION
              422  COMPARE_OP               !=
          424_426  POP_JUMP_IF_FALSE   434  'to 434'

 L. 330       428  LOAD_FAST                'opcode'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               _opcode
            434_0  COME_FROM           424  '424'

 L. 331       434  LOAD_FAST                'self'
              436  LOAD_ATTR                _partial
              438  LOAD_METHOD              extend
              440  LOAD_FAST                'payload'
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          

 L. 332       446  LOAD_FAST                'self'
              448  LOAD_ATTR                _max_msg_size
          450_452  POP_JUMP_IF_FALSE   890  'to 890'

 L. 333       454  LOAD_GLOBAL              len
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                _partial
              460  CALL_FUNCTION_1       1  ''
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                _max_msg_size
              466  COMPARE_OP               >=

 L. 332   468_470  POP_JUMP_IF_FALSE   890  'to 890'

 L. 334       472  LOAD_GLOBAL              WebSocketError

 L. 335       474  LOAD_GLOBAL              WSCloseCode
              476  LOAD_ATTR                MESSAGE_TOO_BIG

 L. 336       478  LOAD_STR                 'Message size {} exceeds limit {}'
              480  LOAD_METHOD              format

 L. 337       482  LOAD_GLOBAL              len
              484  LOAD_FAST                'self'
              486  LOAD_ATTR                _partial
              488  CALL_FUNCTION_1       1  ''

 L. 337       490  LOAD_FAST                'self'
              492  LOAD_ATTR                _max_msg_size

 L. 336       494  CALL_METHOD_2         2  ''

 L. 334       496  CALL_FUNCTION_2       2  ''
              498  RAISE_VARARGS_1       1  'exception instance'
              500  JUMP_BACK            10  'to 10'
            502_0  COME_FROM           412  '412'

 L. 341       502  LOAD_FAST                'self'
              504  LOAD_ATTR                _partial
          506_508  POP_JUMP_IF_FALSE   540  'to 540'

 L. 342       510  LOAD_FAST                'opcode'
              512  LOAD_GLOBAL              WSMsgType
              514  LOAD_ATTR                CONTINUATION
              516  COMPARE_OP               !=
          518_520  POP_JUMP_IF_FALSE   540  'to 540'

 L. 343       522  LOAD_GLOBAL              WebSocketError

 L. 344       524  LOAD_GLOBAL              WSCloseCode
              526  LOAD_ATTR                PROTOCOL_ERROR

 L. 345       528  LOAD_STR                 'The opcode in non-fin frame is expected to be zero, got {!r}'
              530  LOAD_METHOD              format

 L. 346       532  LOAD_FAST                'opcode'

 L. 345       534  CALL_METHOD_1         1  ''

 L. 343       536  CALL_FUNCTION_2       2  ''
              538  RAISE_VARARGS_1       1  'exception instance'
            540_0  COME_FROM           518  '518'
            540_1  COME_FROM           506  '506'

 L. 348       540  LOAD_FAST                'opcode'
              542  LOAD_GLOBAL              WSMsgType
              544  LOAD_ATTR                CONTINUATION
              546  COMPARE_OP               ==
          548_550  POP_JUMP_IF_FALSE   580  'to 580'

 L. 349       552  LOAD_FAST                'self'
              554  LOAD_ATTR                _opcode
              556  LOAD_CONST               None
              558  COMPARE_OP               is-not
          560_562  POP_JUMP_IF_TRUE    568  'to 568'
              564  LOAD_ASSERT              AssertionError
              566  RAISE_VARARGS_1       1  'exception instance'
            568_0  COME_FROM           560  '560'

 L. 350       568  LOAD_FAST                'self'
              570  LOAD_ATTR                _opcode
              572  STORE_FAST               'opcode'

 L. 351       574  LOAD_CONST               None
              576  LOAD_FAST                'self'
              578  STORE_ATTR               _opcode
            580_0  COME_FROM           548  '548'

 L. 353       580  LOAD_FAST                'self'
              582  LOAD_ATTR                _partial
              584  LOAD_METHOD              extend
              586  LOAD_FAST                'payload'
              588  CALL_METHOD_1         1  ''
              590  POP_TOP          

 L. 354       592  LOAD_FAST                'self'
              594  LOAD_ATTR                _max_msg_size
          596_598  POP_JUMP_IF_FALSE   646  'to 646'

 L. 355       600  LOAD_GLOBAL              len
              602  LOAD_FAST                'self'
              604  LOAD_ATTR                _partial
              606  CALL_FUNCTION_1       1  ''
              608  LOAD_FAST                'self'
              610  LOAD_ATTR                _max_msg_size
              612  COMPARE_OP               >=

 L. 354   614_616  POP_JUMP_IF_FALSE   646  'to 646'

 L. 356       618  LOAD_GLOBAL              WebSocketError

 L. 357       620  LOAD_GLOBAL              WSCloseCode
              622  LOAD_ATTR                MESSAGE_TOO_BIG

 L. 358       624  LOAD_STR                 'Message size {} exceeds limit {}'
              626  LOAD_METHOD              format

 L. 359       628  LOAD_GLOBAL              len
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                _partial
              634  CALL_FUNCTION_1       1  ''

 L. 359       636  LOAD_FAST                'self'
              638  LOAD_ATTR                _max_msg_size

 L. 358       640  CALL_METHOD_2         2  ''

 L. 356       642  CALL_FUNCTION_2       2  ''
              644  RAISE_VARARGS_1       1  'exception instance'
            646_0  COME_FROM           614  '614'
            646_1  COME_FROM           596  '596'

 L. 363       646  LOAD_FAST                'compressed'
          648_650  POP_JUMP_IF_FALSE   734  'to 734'

 L. 364       652  LOAD_FAST                'self'
              654  LOAD_ATTR                _partial
              656  LOAD_METHOD              extend
              658  LOAD_GLOBAL              _WS_DEFLATE_TRAILING
              660  CALL_METHOD_1         1  ''
              662  POP_TOP          

 L. 365       664  LOAD_FAST                'self'
              666  LOAD_ATTR                _decompressobj
              668  LOAD_METHOD              decompress

 L. 366       670  LOAD_FAST                'self'
              672  LOAD_ATTR                _partial

 L. 366       674  LOAD_FAST                'self'
              676  LOAD_ATTR                _max_msg_size

 L. 365       678  CALL_METHOD_2         2  ''
              680  STORE_FAST               'payload_merged'

 L. 367       682  LOAD_FAST                'self'
              684  LOAD_ATTR                _decompressobj
              686  LOAD_ATTR                unconsumed_tail
          688_690  POP_JUMP_IF_FALSE   744  'to 744'

 L. 368       692  LOAD_GLOBAL              len
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                _decompressobj
              698  LOAD_ATTR                unconsumed_tail
              700  CALL_FUNCTION_1       1  ''
              702  STORE_FAST               'left'

 L. 369       704  LOAD_GLOBAL              WebSocketError

 L. 370       706  LOAD_GLOBAL              WSCloseCode
              708  LOAD_ATTR                MESSAGE_TOO_BIG

 L. 371       710  LOAD_STR                 'Decompressed message size {} exceeds limit {}'
              712  LOAD_METHOD              format

 L. 373       714  LOAD_FAST                'self'
              716  LOAD_ATTR                _max_msg_size
              718  LOAD_FAST                'left'
              720  BINARY_ADD       

 L. 374       722  LOAD_FAST                'self'
              724  LOAD_ATTR                _max_msg_size

 L. 371       726  CALL_METHOD_2         2  ''

 L. 369       728  CALL_FUNCTION_2       2  ''
              730  RAISE_VARARGS_1       1  'exception instance'
              732  JUMP_FORWARD        744  'to 744'
            734_0  COME_FROM           648  '648'

 L. 378       734  LOAD_GLOBAL              bytes
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                _partial
              740  CALL_FUNCTION_1       1  ''
              742  STORE_FAST               'payload_merged'
            744_0  COME_FROM           732  '732'
            744_1  COME_FROM           688  '688'

 L. 380       744  LOAD_FAST                'self'
              746  LOAD_ATTR                _partial
              748  LOAD_METHOD              clear
              750  CALL_METHOD_0         0  ''
              752  POP_TOP          

 L. 382       754  LOAD_FAST                'opcode'
              756  LOAD_GLOBAL              WSMsgType
              758  LOAD_ATTR                TEXT
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_FALSE   862  'to 862'

 L. 383       766  SETUP_FINALLY       810  'to 810'

 L. 384       768  LOAD_FAST                'payload_merged'
              770  LOAD_METHOD              decode
              772  LOAD_STR                 'utf-8'
              774  CALL_METHOD_1         1  ''
              776  STORE_FAST               'text'

 L. 385       778  LOAD_FAST                'self'
              780  LOAD_ATTR                queue
              782  LOAD_METHOD              feed_data

 L. 386       784  LOAD_GLOBAL              WSMessage
              786  LOAD_GLOBAL              WSMsgType
              788  LOAD_ATTR                TEXT
              790  LOAD_FAST                'text'
              792  LOAD_STR                 ''
              794  CALL_FUNCTION_3       3  ''

 L. 386       796  LOAD_GLOBAL              len
              798  LOAD_FAST                'text'
              800  CALL_FUNCTION_1       1  ''

 L. 385       802  CALL_METHOD_2         2  ''
              804  POP_TOP          
              806  POP_BLOCK        
              808  JUMP_FORWARD        860  'to 860'
            810_0  COME_FROM_FINALLY   766  '766'

 L. 387       810  DUP_TOP          
              812  LOAD_GLOBAL              UnicodeDecodeError
              814  COMPARE_OP               exception-match
          816_818  POP_JUMP_IF_FALSE   858  'to 858'
              820  POP_TOP          
              822  STORE_FAST               'exc'
              824  POP_TOP          
              826  SETUP_FINALLY       846  'to 846'

 L. 388       828  LOAD_GLOBAL              WebSocketError

 L. 389       830  LOAD_GLOBAL              WSCloseCode
              832  LOAD_ATTR                INVALID_TEXT

 L. 390       834  LOAD_STR                 'Invalid UTF-8 text message'

 L. 388       836  CALL_FUNCTION_2       2  ''

 L. 390       838  LOAD_FAST                'exc'

 L. 388       840  RAISE_VARARGS_2       2  'exception instance with __cause__'
              842  POP_BLOCK        
              844  BEGIN_FINALLY    
            846_0  COME_FROM_FINALLY   826  '826'
              846  LOAD_CONST               None
              848  STORE_FAST               'exc'
              850  DELETE_FAST              'exc'
              852  END_FINALLY      
              854  POP_EXCEPT       
              856  JUMP_FORWARD        860  'to 860'
            858_0  COME_FROM           816  '816'
              858  END_FINALLY      
            860_0  COME_FROM           856  '856'
            860_1  COME_FROM           808  '808'
              860  JUMP_BACK            10  'to 10'
            862_0  COME_FROM           762  '762'

 L. 392       862  LOAD_FAST                'self'
              864  LOAD_ATTR                queue
              866  LOAD_METHOD              feed_data

 L. 393       868  LOAD_GLOBAL              WSMessage
              870  LOAD_GLOBAL              WSMsgType
              872  LOAD_ATTR                BINARY
              874  LOAD_FAST                'payload_merged'
              876  LOAD_STR                 ''
              878  CALL_FUNCTION_3       3  ''

 L. 394       880  LOAD_GLOBAL              len
              882  LOAD_FAST                'payload_merged'
              884  CALL_FUNCTION_1       1  ''

 L. 392       886  CALL_METHOD_2         2  ''
              888  POP_TOP          
            890_0  COME_FROM           468  '468'
            890_1  COME_FROM           450  '450'
              890  JUMP_BACK            10  'to 10'
            892_0  COME_FROM            10  '10'

 L. 396       892  LOAD_CONST               (False, b'')
              894  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 894

        def parse_frame--- This code section failed: ---

 L. 402         0  BUILD_LIST_0          0 
                2  STORE_FAST               'frames'

 L. 403         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _tail
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 404        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _tail
               14  LOAD_FAST                'buf'
               16  BINARY_ADD       
               18  LOAD_CONST               b''
               20  ROT_TWO          
               22  STORE_FAST               'buf'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _tail
             28_0  COME_FROM             8  '8'

 L. 406        28  LOAD_CONST               0
               30  STORE_FAST               'start_pos'

 L. 407        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'buf'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'buf_length'
             40_0  COME_FROM           882  '882'
             40_1  COME_FROM           876  '876'
             40_2  COME_FROM           686  '686'

 L. 411        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _state
               44  LOAD_GLOBAL              WSParserState
               46  LOAD_ATTR                READ_HEADER
               48  COMPARE_OP               ==
            50_52  POP_JUMP_IF_FALSE   368  'to 368'

 L. 412        54  LOAD_FAST                'buf_length'
               56  LOAD_FAST                'start_pos'
               58  BINARY_SUBTRACT  
               60  LOAD_CONST               2
               62  COMPARE_OP               >=
            64_66  POP_JUMP_IF_FALSE   884  'to 884'

 L. 413        68  LOAD_FAST                'buf'
               70  LOAD_FAST                'start_pos'
               72  LOAD_FAST                'start_pos'
               74  LOAD_CONST               2
               76  BINARY_ADD       
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'data'

 L. 414        84  LOAD_FAST                'start_pos'
               86  LOAD_CONST               2
               88  INPLACE_ADD      
               90  STORE_FAST               'start_pos'

 L. 415        92  LOAD_FAST                'data'
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'first_byte'
               98  STORE_FAST               'second_byte'

 L. 417       100  LOAD_FAST                'first_byte'
              102  LOAD_CONST               7
              104  BINARY_RSHIFT    
              106  LOAD_CONST               1
              108  BINARY_AND       
              110  STORE_FAST               'fin'

 L. 418       112  LOAD_FAST                'first_byte'
              114  LOAD_CONST               6
              116  BINARY_RSHIFT    
              118  LOAD_CONST               1
              120  BINARY_AND       
              122  STORE_FAST               'rsv1'

 L. 419       124  LOAD_FAST                'first_byte'
              126  LOAD_CONST               5
              128  BINARY_RSHIFT    
              130  LOAD_CONST               1
              132  BINARY_AND       
              134  STORE_FAST               'rsv2'

 L. 420       136  LOAD_FAST                'first_byte'
              138  LOAD_CONST               4
              140  BINARY_RSHIFT    
              142  LOAD_CONST               1
              144  BINARY_AND       
              146  STORE_FAST               'rsv3'

 L. 421       148  LOAD_FAST                'first_byte'
              150  LOAD_CONST               15
              152  BINARY_AND       
              154  STORE_FAST               'opcode'

 L. 433       156  LOAD_FAST                'rsv2'
              158  POP_JUMP_IF_TRUE    174  'to 174'
              160  LOAD_FAST                'rsv3'
              162  POP_JUMP_IF_TRUE    174  'to 174'
              164  LOAD_FAST                'rsv1'
              166  POP_JUMP_IF_FALSE   186  'to 186'
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _compress
              172  POP_JUMP_IF_TRUE    186  'to 186'
            174_0  COME_FROM           162  '162'
            174_1  COME_FROM           158  '158'

 L. 434       174  LOAD_GLOBAL              WebSocketError

 L. 435       176  LOAD_GLOBAL              WSCloseCode
              178  LOAD_ATTR                PROTOCOL_ERROR

 L. 436       180  LOAD_STR                 'Received frame with non-zero reserved bits'

 L. 434       182  CALL_FUNCTION_2       2  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           172  '172'
            186_1  COME_FROM           166  '166'

 L. 438       186  LOAD_FAST                'opcode'
              188  LOAD_CONST               7
              190  COMPARE_OP               >
              192  POP_JUMP_IF_FALSE   214  'to 214'
              194  LOAD_FAST                'fin'
              196  LOAD_CONST               0
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 439       202  LOAD_GLOBAL              WebSocketError

 L. 440       204  LOAD_GLOBAL              WSCloseCode
              206  LOAD_ATTR                PROTOCOL_ERROR

 L. 441       208  LOAD_STR                 'Received fragmented control frame'

 L. 439       210  CALL_FUNCTION_2       2  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           200  '200'
            214_1  COME_FROM           192  '192'

 L. 443       214  LOAD_FAST                'second_byte'
              216  LOAD_CONST               7
              218  BINARY_RSHIFT    
              220  LOAD_CONST               1
              222  BINARY_AND       
              224  STORE_FAST               'has_mask'

 L. 444       226  LOAD_FAST                'second_byte'
              228  LOAD_CONST               127
              230  BINARY_AND       
              232  STORE_FAST               'length'

 L. 448       234  LOAD_FAST                'opcode'
              236  LOAD_CONST               7
              238  COMPARE_OP               >
          240_242  POP_JUMP_IF_FALSE   266  'to 266'
              244  LOAD_FAST                'length'
              246  LOAD_CONST               125
              248  COMPARE_OP               >
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L. 449       254  LOAD_GLOBAL              WebSocketError

 L. 450       256  LOAD_GLOBAL              WSCloseCode
              258  LOAD_ATTR                PROTOCOL_ERROR

 L. 451       260  LOAD_STR                 'Control frame payload cannot be larger than 125 bytes'

 L. 449       262  CALL_FUNCTION_2       2  ''
              264  RAISE_VARARGS_1       1  'exception instance'
            266_0  COME_FROM           250  '250'
            266_1  COME_FROM           240  '240'

 L. 457       266  LOAD_FAST                'self'
              268  LOAD_ATTR                _frame_fin
          270_272  POP_JUMP_IF_TRUE    286  'to 286'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                _compressed
              278  LOAD_CONST               None
              280  COMPARE_OP               is
          282_284  POP_JUMP_IF_FALSE   304  'to 304'
            286_0  COME_FROM           270  '270'

 L. 458       286  LOAD_FAST                'rsv1'
          288_290  POP_JUMP_IF_FALSE   296  'to 296'
              292  LOAD_CONST               True
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           288  '288'
              296  LOAD_CONST               False
            298_0  COME_FROM           294  '294'
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _compressed
              302  JUMP_FORWARD        322  'to 322'
            304_0  COME_FROM           282  '282'

 L. 459       304  LOAD_FAST                'rsv1'
          306_308  POP_JUMP_IF_FALSE   322  'to 322'

 L. 460       310  LOAD_GLOBAL              WebSocketError

 L. 461       312  LOAD_GLOBAL              WSCloseCode
              314  LOAD_ATTR                PROTOCOL_ERROR

 L. 462       316  LOAD_STR                 'Received frame with non-zero reserved bits'

 L. 460       318  CALL_FUNCTION_2       2  ''
              320  RAISE_VARARGS_1       1  'exception instance'
            322_0  COME_FROM           306  '306'
            322_1  COME_FROM           302  '302'

 L. 464       322  LOAD_GLOBAL              bool
              324  LOAD_FAST                'fin'
              326  CALL_FUNCTION_1       1  ''
              328  LOAD_FAST                'self'
              330  STORE_ATTR               _frame_fin

 L. 465       332  LOAD_FAST                'opcode'
              334  LOAD_FAST                'self'
              336  STORE_ATTR               _frame_opcode

 L. 466       338  LOAD_GLOBAL              bool
              340  LOAD_FAST                'has_mask'
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_FAST                'self'
              346  STORE_ATTR               _has_mask

 L. 467       348  LOAD_FAST                'length'
              350  LOAD_FAST                'self'
              352  STORE_ATTR               _payload_length_flag

 L. 468       354  LOAD_GLOBAL              WSParserState
              356  LOAD_ATTR                READ_PAYLOAD_LENGTH
              358  LOAD_FAST                'self'
              360  STORE_ATTR               _state
              362  JUMP_FORWARD        368  'to 368'

 L. 470   364_366  JUMP_FORWARD        884  'to 884'
            368_0  COME_FROM           362  '362'
            368_1  COME_FROM            50  '50'

 L. 473       368  LOAD_FAST                'self'
              370  LOAD_ATTR                _state
              372  LOAD_GLOBAL              WSParserState
              374  LOAD_ATTR                READ_PAYLOAD_LENGTH
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   608  'to 608'

 L. 474       382  LOAD_FAST                'self'
              384  LOAD_ATTR                _payload_length_flag
              386  STORE_FAST               'length'

 L. 475       388  LOAD_FAST                'length'
              390  LOAD_CONST               126
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   484  'to 484'

 L. 476       398  LOAD_FAST                'buf_length'
              400  LOAD_FAST                'start_pos'
              402  BINARY_SUBTRACT  
              404  LOAD_CONST               2
              406  COMPARE_OP               >=
          408_410  POP_JUMP_IF_FALSE   884  'to 884'

 L. 477       412  LOAD_FAST                'buf'
              414  LOAD_FAST                'start_pos'
              416  LOAD_FAST                'start_pos'
              418  LOAD_CONST               2
              420  BINARY_ADD       
              422  BUILD_SLICE_2         2 
              424  BINARY_SUBSCR    
              426  STORE_FAST               'data'

 L. 478       428  LOAD_FAST                'start_pos'
              430  LOAD_CONST               2
              432  INPLACE_ADD      
              434  STORE_FAST               'start_pos'

 L. 479       436  LOAD_GLOBAL              UNPACK_LEN2
              438  LOAD_FAST                'data'
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_CONST               0
              444  BINARY_SUBSCR    
              446  STORE_FAST               'length'

 L. 480       448  LOAD_FAST                'length'
              450  LOAD_FAST                'self'
              452  STORE_ATTR               _payload_length

 L. 483       454  LOAD_FAST                'self'
              456  LOAD_ATTR                _has_mask

 L. 482   458_460  POP_JUMP_IF_FALSE   468  'to 468'
              462  LOAD_GLOBAL              WSParserState
              464  LOAD_ATTR                READ_PAYLOAD_MASK
              466  JUMP_FORWARD        472  'to 472'
            468_0  COME_FROM           458  '458'

 L. 484       468  LOAD_GLOBAL              WSParserState
              470  LOAD_ATTR                READ_PAYLOAD
            472_0  COME_FROM           466  '466'

 L. 481       472  LOAD_FAST                'self'
              474  STORE_ATTR               _state
              476  JUMP_FORWARD        482  'to 482'

 L. 486   478_480  JUMP_FORWARD        884  'to 884'
            482_0  COME_FROM           476  '476'
              482  BREAK_LOOP          608  'to 608'
            484_0  COME_FROM           394  '394'

 L. 487       484  LOAD_FAST                'length'
              486  LOAD_CONST               126
              488  COMPARE_OP               >
          490_492  POP_JUMP_IF_FALSE   580  'to 580'

 L. 488       494  LOAD_FAST                'buf_length'
              496  LOAD_FAST                'start_pos'
              498  BINARY_SUBTRACT  
              500  LOAD_CONST               8
              502  COMPARE_OP               >=
          504_506  POP_JUMP_IF_FALSE   884  'to 884'

 L. 489       508  LOAD_FAST                'buf'
              510  LOAD_FAST                'start_pos'
              512  LOAD_FAST                'start_pos'
              514  LOAD_CONST               8
              516  BINARY_ADD       
              518  BUILD_SLICE_2         2 
              520  BINARY_SUBSCR    
              522  STORE_FAST               'data'

 L. 490       524  LOAD_FAST                'start_pos'
              526  LOAD_CONST               8
              528  INPLACE_ADD      
              530  STORE_FAST               'start_pos'

 L. 491       532  LOAD_GLOBAL              UNPACK_LEN3
              534  LOAD_FAST                'data'
              536  CALL_FUNCTION_1       1  ''
              538  LOAD_CONST               0
              540  BINARY_SUBSCR    
              542  STORE_FAST               'length'

 L. 492       544  LOAD_FAST                'length'
              546  LOAD_FAST                'self'
              548  STORE_ATTR               _payload_length

 L. 495       550  LOAD_FAST                'self'
              552  LOAD_ATTR                _has_mask

 L. 494   554_556  POP_JUMP_IF_FALSE   564  'to 564'
              558  LOAD_GLOBAL              WSParserState
              560  LOAD_ATTR                READ_PAYLOAD_MASK
              562  JUMP_FORWARD        568  'to 568'
            564_0  COME_FROM           554  '554'

 L. 496       564  LOAD_GLOBAL              WSParserState
              566  LOAD_ATTR                READ_PAYLOAD
            568_0  COME_FROM           562  '562'

 L. 493       568  LOAD_FAST                'self'
              570  STORE_ATTR               _state
              572  JUMP_FORWARD        578  'to 578'

 L. 498   574_576  JUMP_FORWARD        884  'to 884'
            578_0  COME_FROM           572  '572'
              578  BREAK_LOOP          608  'to 608'
            580_0  COME_FROM           490  '490'

 L. 500       580  LOAD_FAST                'length'
              582  LOAD_FAST                'self'
              584  STORE_ATTR               _payload_length

 L. 503       586  LOAD_FAST                'self'
              588  LOAD_ATTR                _has_mask

 L. 502   590_592  POP_JUMP_IF_FALSE   600  'to 600'
              594  LOAD_GLOBAL              WSParserState
              596  LOAD_ATTR                READ_PAYLOAD_MASK
              598  JUMP_FORWARD        604  'to 604'
            600_0  COME_FROM           590  '590'

 L. 504       600  LOAD_GLOBAL              WSParserState
              602  LOAD_ATTR                READ_PAYLOAD
            604_0  COME_FROM           598  '598'

 L. 501       604  LOAD_FAST                'self'
              606  STORE_ATTR               _state
            608_0  COME_FROM           578  '578'
            608_1  COME_FROM           482  '482'
            608_2  COME_FROM           378  '378'

 L. 507       608  LOAD_FAST                'self'
              610  LOAD_ATTR                _state
              612  LOAD_GLOBAL              WSParserState
              614  LOAD_ATTR                READ_PAYLOAD_MASK
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   676  'to 676'

 L. 508       622  LOAD_FAST                'buf_length'
              624  LOAD_FAST                'start_pos'
              626  BINARY_SUBTRACT  
              628  LOAD_CONST               4
              630  COMPARE_OP               >=
          632_634  POP_JUMP_IF_FALSE   884  'to 884'

 L. 509       636  LOAD_FAST                'buf'
              638  LOAD_FAST                'start_pos'
              640  LOAD_FAST                'start_pos'
              642  LOAD_CONST               4
              644  BINARY_ADD       
              646  BUILD_SLICE_2         2 
              648  BINARY_SUBSCR    
              650  LOAD_FAST                'self'
              652  STORE_ATTR               _frame_mask

 L. 510       654  LOAD_FAST                'start_pos'
              656  LOAD_CONST               4
              658  INPLACE_ADD      
              660  STORE_FAST               'start_pos'

 L. 511       662  LOAD_GLOBAL              WSParserState
              664  LOAD_ATTR                READ_PAYLOAD
              666  LOAD_FAST                'self'
              668  STORE_ATTR               _state
              670  JUMP_FORWARD        676  'to 676'

 L. 513   672_674  JUMP_FORWARD        884  'to 884'
            676_0  COME_FROM           670  '670'
            676_1  COME_FROM           618  '618'

 L. 515       676  LOAD_FAST                'self'
              678  LOAD_ATTR                _state
              680  LOAD_GLOBAL              WSParserState
              682  LOAD_ATTR                READ_PAYLOAD
              684  COMPARE_OP               ==
              686  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L. 516       688  LOAD_FAST                'self'
              690  LOAD_ATTR                _payload_length
              692  STORE_FAST               'length'

 L. 517       694  LOAD_FAST                'self'
              696  LOAD_ATTR                _frame_payload
              698  STORE_FAST               'payload'

 L. 519       700  LOAD_FAST                'buf_length'
              702  LOAD_FAST                'start_pos'
              704  BINARY_SUBTRACT  
              706  STORE_FAST               'chunk_len'

 L. 520       708  LOAD_FAST                'length'
              710  LOAD_FAST                'chunk_len'
              712  COMPARE_OP               >=
          714_716  POP_JUMP_IF_FALSE   752  'to 752'

 L. 521       718  LOAD_FAST                'length'
              720  LOAD_FAST                'chunk_len'
              722  BINARY_SUBTRACT  
              724  LOAD_FAST                'self'
              726  STORE_ATTR               _payload_length

 L. 522       728  LOAD_FAST                'payload'
              730  LOAD_METHOD              extend
              732  LOAD_FAST                'buf'
              734  LOAD_FAST                'start_pos'
              736  LOAD_CONST               None
              738  BUILD_SLICE_2         2 
              740  BINARY_SUBSCR    
              742  CALL_METHOD_1         1  ''
              744  POP_TOP          

 L. 523       746  LOAD_FAST                'buf_length'
              748  STORE_FAST               'start_pos'
              750  JUMP_FORWARD        788  'to 788'
            752_0  COME_FROM           714  '714'

 L. 525       752  LOAD_CONST               0
              754  LOAD_FAST                'self'
              756  STORE_ATTR               _payload_length

 L. 526       758  LOAD_FAST                'payload'
              760  LOAD_METHOD              extend
              762  LOAD_FAST                'buf'
              764  LOAD_FAST                'start_pos'
              766  LOAD_FAST                'start_pos'
              768  LOAD_FAST                'length'
              770  BINARY_ADD       
              772  BUILD_SLICE_2         2 
              774  BINARY_SUBSCR    
              776  CALL_METHOD_1         1  ''
              778  POP_TOP          

 L. 527       780  LOAD_FAST                'start_pos'
              782  LOAD_FAST                'length'
              784  BINARY_ADD       
              786  STORE_FAST               'start_pos'
            788_0  COME_FROM           750  '750'

 L. 529       788  LOAD_FAST                'self'
              790  LOAD_ATTR                _payload_length
              792  LOAD_CONST               0
              794  COMPARE_OP               ==
          796_798  POP_JUMP_IF_FALSE   884  'to 884'

 L. 530       800  LOAD_FAST                'self'
              802  LOAD_ATTR                _has_mask
          804_806  POP_JUMP_IF_FALSE   836  'to 836'

 L. 531       808  LOAD_FAST                'self'
              810  LOAD_ATTR                _frame_mask
              812  LOAD_CONST               None
              814  COMPARE_OP               is-not
          816_818  POP_JUMP_IF_TRUE    824  'to 824'
              820  LOAD_ASSERT              AssertionError
              822  RAISE_VARARGS_1       1  'exception instance'
            824_0  COME_FROM           816  '816'

 L. 532       824  LOAD_GLOBAL              _websocket_mask
              826  LOAD_FAST                'self'
              828  LOAD_ATTR                _frame_mask
              830  LOAD_FAST                'payload'
              832  CALL_FUNCTION_2       2  ''
              834  POP_TOP          
            836_0  COME_FROM           804  '804'

 L. 534       836  LOAD_FAST                'frames'
              838  LOAD_METHOD              append

 L. 535       840  LOAD_FAST                'self'
              842  LOAD_ATTR                _frame_fin

 L. 536       844  LOAD_FAST                'self'
              846  LOAD_ATTR                _frame_opcode

 L. 537       848  LOAD_FAST                'payload'

 L. 538       850  LOAD_FAST                'self'
              852  LOAD_ATTR                _compressed

 L. 534       854  BUILD_TUPLE_4         4 
              856  CALL_METHOD_1         1  ''
              858  POP_TOP          

 L. 540       860  LOAD_GLOBAL              bytearray
              862  CALL_FUNCTION_0       0  ''
              864  LOAD_FAST                'self'
              866  STORE_ATTR               _frame_payload

 L. 541       868  LOAD_GLOBAL              WSParserState
              870  LOAD_ATTR                READ_HEADER
              872  LOAD_FAST                'self'
              874  STORE_ATTR               _state
              876  JUMP_BACK            40  'to 40'

 L. 543   878_880  JUMP_FORWARD        884  'to 884'
              882  JUMP_BACK            40  'to 40'
            884_0  COME_FROM           878  '878'
            884_1  COME_FROM           796  '796'
            884_2  COME_FROM           672  '672'
            884_3  COME_FROM           632  '632'
            884_4  COME_FROM           574  '574'
            884_5  COME_FROM           504  '504'
            884_6  COME_FROM           478  '478'
            884_7  COME_FROM           408  '408'
            884_8  COME_FROM           364  '364'
            884_9  COME_FROM            64  '64'

 L. 545       884  LOAD_FAST                'buf'
              886  LOAD_FAST                'start_pos'
              888  LOAD_CONST               None
              890  BUILD_SLICE_2         2 
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'self'
              896  STORE_ATTR               _tail

 L. 547       898  LOAD_FAST                'frames'
              900  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 878_880


    class WebSocketWriter:

        def __init__(self, protocol: BaseProtocol, transport: asyncio.Transport, *, use_mask: bool=False, limit: int=DEFAULT_LIMIT, random: Any=random.Random(), compress: int=0, notakeover: bool=False) -> None:
            self.protocol = protocol
            self.transport = transport
            self.use_mask = use_mask
            self.randrange = random.randrange
            self.compress = compress
            self.notakeover = notakeover
            self._closing = False
            self._limit = limit
            self._output_size = 0
            self._compressobj = None

        async def _send_frame(self, message: bytes, opcode: int, compress: Optional[int]=None) -> None:
            """Send a frame over the websocket with message as its payload."""
            if self._closing:
                ws_logger.warning('websocket connection is closing.')
            rsv = 0
            if compress or (self.compress):
                if opcode < 8:
                    if compress:
                        compressobj = zlib.compressobj(wbits=(-compress))
                    else:
                        if not self._compressobj:
                            self._compressobj = zlib.compressobj(wbits=(-self.compress))
                        compressobj = self._compressobj
                    message = compressobj.compress(message)
                    message = message + compressobj.flush(zlib.Z_FULL_FLUSH if self.notakeover else zlib.Z_SYNC_FLUSH)
                    if message.endswith(_WS_DEFLATE_TRAILING):
                        message = message[:-4]
                    rsv = rsv | 64
            msg_length = len(message)
            use_mask = self.use_mask
            if use_mask:
                mask_bit = 128
            else:
                mask_bit = 0
            if msg_length < 126:
                header = PACK_LEN1(128 | rsv | opcode, msg_length | mask_bit)
            elif msg_length < 65536:
                header = PACK_LEN2(128 | rsv | opcode, 126 | mask_bit, msg_length)
            else:
                header = PACK_LEN3(128 | rsv | opcode, 127 | mask_bit, msg_length)
            if use_mask:
                mask = self.randrange(0, 4294967295)
                mask = mask.to_bytes(4, 'big')
                message = bytearray(message)
                _websocket_mask(mask, message)
                self.transport.write(header + mask + message)
                self._output_size += len(header) + len(mask) + len(message)
            else:
                if len(message) > MSG_SIZE:
                    self.transport.write(header)
                    self.transport.write(message)
                else:
                    self.transport.write(header + message)
                self._output_size += len(header) + len(message)
            if self._output_size > self._limit:
                self._output_size = 0
                await self.protocol._drain_helper()

        async def pong(self, message: bytes=b'') -> None:
            """Send pong message."""
            if isinstance(message, str):
                message = message.encode('utf-8')
            await self._send_frame(message, WSMsgType.PONG)

        async def ping(self, message: bytes=b'') -> None:
            """Send ping message."""
            if isinstance(message, str):
                message = message.encode('utf-8')
            await self._send_frame(message, WSMsgType.PING)

        async def send(self, message: Union[(str, bytes)], binary: bool=False, compress: Optional[int]=None) -> None:
            """Send a frame over the websocket with message as its payload."""
            if isinstance(message, str):
                message = message.encode('utf-8')
            if binary:
                await self._send_framemessageWSMsgType.BINARYcompress
            else:
                await self._send_framemessageWSMsgType.TEXTcompress

        async def close(self, code: int=1000, message: bytes=b'') -> None:
            """Close the websocket, sending the specified code and message."""
            if isinstance(message, str):
                message = message.encode('utf-8')
            try:
                await self._send_frame((PACK_CLOSE_CODE(code) + message),
                  opcode=(WSMsgType.CLOSE))
            finally:
                self._closing = True