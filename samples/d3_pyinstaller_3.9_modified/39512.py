# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_ws.py
import asyncio, base64, binascii, hashlib, json
from typing import Any, Iterable, Optional, Tuple
import async_timeout, attr
from multidict import CIMultiDict
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import call_later, set_result
from .http import WS_CLOSED_MESSAGE, WS_CLOSING_MESSAGE, WS_KEY, WebSocketError, WebSocketReader, WebSocketWriter, WSMessage, WSMsgType, ws_ext_gen, ws_ext_parse
from .log import ws_logger
from .streams import EofStream, FlowControlDataQueue
from .typedefs import JSONDecoder, JSONEncoder
from .web_exceptions import HTTPBadRequest, HTTPException
from .web_request import BaseRequest
from .web_response import StreamResponse
__all__ = ('WebSocketResponse', 'WebSocketReady', 'WSMsgType')
THRESHOLD_CONNLOST_ACCESS = 5

@attr.s(auto_attribs=True, frozen=True, slots=True)
class WebSocketReady:
    ok: bool
    protocol: Optional[str]

    def __bool__(self) -> bool:
        return self.ok


class WebSocketResponse(StreamResponse):
    _length_check = False

    def __init__--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_CONST               101
                8  LOAD_CONST               ('status',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          

 L.  69        14  LOAD_FAST                'protocols'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _protocols

 L.  70        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _ws_protocol

 L.  71        26  LOAD_CONST               None
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _writer

 L.  72        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _reader

 L.  73        38  LOAD_CONST               False
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _closed

 L.  74        44  LOAD_CONST               False
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _closing

 L.  75        50  LOAD_CONST               0
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _conn_lost

 L.  76        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _close_code

 L.  77        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _loop

 L.  78        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _waiting

 L.  79        74  LOAD_CONST               None
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _exception

 L.  80        80  LOAD_FAST                'timeout'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _timeout

 L.  81        86  LOAD_FAST                'receive_timeout'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _receive_timeout

 L.  82        92  LOAD_FAST                'autoclose'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _autoclose

 L.  83        98  LOAD_FAST                'autoping'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _autoping

 L.  84       104  LOAD_FAST                'heartbeat'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _heartbeat

 L.  85       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _heartbeat_cb

 L.  86       116  LOAD_FAST                'heartbeat'
              118  LOAD_CONST               None
              120  <117>                 1  ''
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L.  87       124  LOAD_FAST                'heartbeat'
              126  LOAD_CONST               2.0
              128  BINARY_TRUE_DIVIDE
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _pong_heartbeat
            134_0  COME_FROM           122  '122'

 L.  88       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _pong_response_cb

 L.  89       140  LOAD_FAST                'compress'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _compress

 L.  90       146  LOAD_FAST                'max_msg_size'
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _max_msg_size

Parse error at or near `<117>' instruction at offset 120

    def _cancel_heartbeat--- This code section failed: ---

 L.  93         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pong_response_cb
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  94        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pong_response_cb
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L.  95        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _pong_response_cb
             26_0  COME_FROM             8  '8'

 L.  97        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _heartbeat_cb
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L.  98        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _heartbeat_cb
               40  LOAD_METHOD              cancel
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L.  99        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _heartbeat_cb
             52_0  COME_FROM            34  '34'

Parse error at or near `None' instruction at offset -1

    def _reset_heartbeat--- This code section failed: ---

 L. 102         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cancel_heartbeat
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 104         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _heartbeat
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L. 105        18  LOAD_GLOBAL              call_later

 L. 106        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _send_heartbeat
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _heartbeat
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _loop

 L. 105        32  CALL_FUNCTION_3       3  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _heartbeat_cb
             38_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14

    def _send_heartbeat--- This code section failed: ---

 L. 110         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _heartbeat
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    74  'to 74'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_TRUE     74  'to 74'

 L. 114        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              create_task
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _writer
               26  LOAD_METHOD              ping
               28  CALL_METHOD_0         0  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 116        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _pong_response_cb
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 117        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _pong_response_cb
               48  LOAD_METHOD              cancel
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
             54_0  COME_FROM            42  '42'

 L. 118        54  LOAD_GLOBAL              call_later

 L. 119        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pong_not_received
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _pong_heartbeat
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _loop

 L. 118        68  CALL_FUNCTION_3       3  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _pong_response_cb
             74_0  COME_FROM            14  '14'
             74_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _pong_not_received--- This code section failed: ---

 L. 123         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _req
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    56  'to 56'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _req
               14  LOAD_ATTR                transport
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    56  'to 56'

 L. 124        22  LOAD_CONST               True
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _closed

 L. 125        28  LOAD_CONST               1006
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _close_code

 L. 126        34  LOAD_GLOBAL              asyncio
               36  LOAD_METHOD              TimeoutError
               38  CALL_METHOD_0         0  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _exception

 L. 127        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _req
               48  LOAD_ATTR                transport
               50  LOAD_METHOD              close
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          
             56_0  COME_FROM            20  '20'
             56_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    async def prepare--- This code section failed: ---

 L. 131         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload_writer
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 132        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload_writer
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 134        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _pre_start
               20  LOAD_FAST                'request'
               22  CALL_METHOD_1         1  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'protocol'
               28  STORE_FAST               'writer'

 L. 135        30  LOAD_GLOBAL              super
               32  CALL_FUNCTION_0       0  ''
               34  LOAD_METHOD              prepare
               36  LOAD_FAST                'request'
               38  CALL_METHOD_1         1  ''
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  STORE_FAST               'payload_writer'

 L. 136        48  LOAD_FAST                'payload_writer'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_TRUE     60  'to 60'
               56  <74>             
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            54  '54'

 L. 137        60  LOAD_FAST                'self'
               62  LOAD_METHOD              _post_start
               64  LOAD_FAST                'request'
               66  LOAD_FAST                'protocol'
               68  LOAD_FAST                'writer'
               70  CALL_METHOD_3         3  ''
               72  POP_TOP          

 L. 138        74  LOAD_FAST                'payload_writer'
               76  LOAD_METHOD              drain
               78  CALL_METHOD_0         0  ''
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  POP_TOP          

 L. 139        88  LOAD_FAST                'payload_writer'
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _handshake--- This code section failed: ---

 L. 144         0  LOAD_FAST                'request'
                2  LOAD_ATTR                headers
                4  STORE_FAST               'headers'

 L. 145         6  LOAD_STR                 'websocket'
                8  LOAD_FAST                'headers'
               10  LOAD_METHOD              get
               12  LOAD_GLOBAL              hdrs
               14  LOAD_ATTR                UPGRADE
               16  LOAD_STR                 ''
               18  CALL_METHOD_2         2  ''
               20  LOAD_METHOD              lower
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              strip
               26  CALL_METHOD_0         0  ''
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 146        32  LOAD_GLOBAL              HTTPBadRequest

 L. 148        34  LOAD_STR                 'No WebSocket UPGRADE hdr: {}\n Can "Upgrade" only to "WebSocket".'

 L. 147        36  LOAD_METHOD              format

 L. 150        38  LOAD_FAST                'headers'
               40  LOAD_METHOD              get
               42  LOAD_GLOBAL              hdrs
               44  LOAD_ATTR                UPGRADE
               46  CALL_METHOD_1         1  ''

 L. 147        48  CALL_METHOD_1         1  ''

 L. 146        50  LOAD_CONST               ('text',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            30  '30'

 L. 153        56  LOAD_STR                 'upgrade'
               58  LOAD_FAST                'headers'
               60  LOAD_METHOD              get
               62  LOAD_GLOBAL              hdrs
               64  LOAD_ATTR                CONNECTION
               66  LOAD_STR                 ''
               68  CALL_METHOD_2         2  ''
               70  LOAD_METHOD              lower
               72  CALL_METHOD_0         0  ''
               74  <118>                 1  ''
               76  POP_JUMP_IF_FALSE   102  'to 102'

 L. 154        78  LOAD_GLOBAL              HTTPBadRequest

 L. 155        80  LOAD_STR                 'No CONNECTION upgrade hdr: {}'
               82  LOAD_METHOD              format

 L. 156        84  LOAD_FAST                'headers'
               86  LOAD_METHOD              get
               88  LOAD_GLOBAL              hdrs
               90  LOAD_ATTR                CONNECTION
               92  CALL_METHOD_1         1  ''

 L. 155        94  CALL_METHOD_1         1  ''

 L. 154        96  LOAD_CONST               ('text',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            76  '76'

 L. 161       102  LOAD_CONST               None
              104  STORE_FAST               'protocol'

 L. 162       106  LOAD_GLOBAL              hdrs
              108  LOAD_ATTR                SEC_WEBSOCKET_PROTOCOL
              110  LOAD_FAST                'headers'
              112  <118>                 0  ''
              114  POP_JUMP_IF_FALSE   186  'to 186'

 L. 163       116  LOAD_LISTCOMP            '<code_object <listcomp>>'
              118  LOAD_STR                 'WebSocketResponse._handshake.<locals>.<listcomp>'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 165       122  LOAD_FAST                'headers'
              124  LOAD_GLOBAL              hdrs
              126  LOAD_ATTR                SEC_WEBSOCKET_PROTOCOL
              128  BINARY_SUBSCR    
              130  LOAD_METHOD              split
              132  LOAD_STR                 ','
              134  CALL_METHOD_1         1  ''

 L. 163       136  GET_ITER         
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'req_protocols'

 L. 168       142  LOAD_FAST                'req_protocols'
              144  GET_ITER         
            146_0  COME_FROM           168  '168'
            146_1  COME_FROM           158  '158'
              146  FOR_ITER            170  'to 170'
              148  STORE_FAST               'proto'

 L. 169       150  LOAD_FAST                'proto'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _protocols
              156  <118>                 0  ''
              158  POP_JUMP_IF_FALSE_BACK   146  'to 146'

 L. 170       160  LOAD_FAST                'proto'
              162  STORE_FAST               'protocol'

 L. 171       164  POP_TOP          
              166  BREAK_LOOP          186  'to 186'
              168  JUMP_BACK           146  'to 146'
            170_0  COME_FROM           146  '146'

 L. 174       170  LOAD_GLOBAL              ws_logger
              172  LOAD_METHOD              warning

 L. 175       174  LOAD_STR                 'Client protocols %r don’t overlap server-known ones %r'

 L. 176       176  LOAD_FAST                'req_protocols'

 L. 177       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _protocols

 L. 174       182  CALL_METHOD_3         3  ''
              184  POP_TOP          
            186_0  COME_FROM           166  '166'
            186_1  COME_FROM           114  '114'

 L. 181       186  LOAD_FAST                'headers'
              188  LOAD_METHOD              get
              190  LOAD_GLOBAL              hdrs
              192  LOAD_ATTR                SEC_WEBSOCKET_VERSION
              194  LOAD_STR                 ''
              196  CALL_METHOD_2         2  ''
              198  STORE_FAST               'version'

 L. 182       200  LOAD_FAST                'version'
              202  LOAD_CONST               ('13', '8', '7')
              204  <118>                 1  ''
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 183       208  LOAD_GLOBAL              HTTPBadRequest
              210  LOAD_STR                 'Unsupported version: '
              212  LOAD_FAST                'version'
              214  FORMAT_VALUE          0  ''
              216  BUILD_STRING_2        2 
              218  LOAD_CONST               ('text',)
              220  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           206  '206'

 L. 186       224  LOAD_FAST                'headers'
              226  LOAD_METHOD              get
              228  LOAD_GLOBAL              hdrs
              230  LOAD_ATTR                SEC_WEBSOCKET_KEY
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'key'

 L. 187       236  SETUP_FINALLY       284  'to 284'

 L. 188       238  LOAD_FAST                'key'
          240_242  POP_JUMP_IF_FALSE   264  'to 264'
              244  LOAD_GLOBAL              len
              246  LOAD_GLOBAL              base64
              248  LOAD_METHOD              b64decode
              250  LOAD_FAST                'key'
              252  CALL_METHOD_1         1  ''
              254  CALL_FUNCTION_1       1  ''
              256  LOAD_CONST               16
              258  COMPARE_OP               !=
          260_262  POP_JUMP_IF_FALSE   280  'to 280'
            264_0  COME_FROM           240  '240'

 L. 189       264  LOAD_GLOBAL              HTTPBadRequest
              266  LOAD_STR                 'Handshake error: '
              268  LOAD_FAST                'key'
              270  FORMAT_VALUE          2  '!r'
              272  BUILD_STRING_2        2 
              274  LOAD_CONST               ('text',)
              276  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              278  RAISE_VARARGS_1       1  'exception instance'
            280_0  COME_FROM           260  '260'
              280  POP_BLOCK        
              282  JUMP_FORWARD        324  'to 324'
            284_0  COME_FROM_FINALLY   236  '236'

 L. 190       284  DUP_TOP          
              286  LOAD_GLOBAL              binascii
              288  LOAD_ATTR                Error
          290_292  <121>               322  ''
              294  POP_TOP          
              296  POP_TOP          
              298  POP_TOP          

 L. 191       300  LOAD_GLOBAL              HTTPBadRequest
              302  LOAD_STR                 'Handshake error: '
              304  LOAD_FAST                'key'
              306  FORMAT_VALUE          2  '!r'
              308  BUILD_STRING_2        2 
              310  LOAD_CONST               ('text',)
              312  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              314  LOAD_CONST               None
              316  RAISE_VARARGS_2       2  'exception instance with __cause__'
              318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
              322  <48>             
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           282  '282'

 L. 193       324  LOAD_GLOBAL              base64
              326  LOAD_METHOD              b64encode

 L. 194       328  LOAD_GLOBAL              hashlib
              330  LOAD_METHOD              sha1
              332  LOAD_FAST                'key'
              334  LOAD_METHOD              encode
              336  CALL_METHOD_0         0  ''
              338  LOAD_GLOBAL              WS_KEY
              340  BINARY_ADD       
              342  CALL_METHOD_1         1  ''
              344  LOAD_METHOD              digest
              346  CALL_METHOD_0         0  ''

 L. 193       348  CALL_METHOD_1         1  ''
              350  LOAD_METHOD              decode
              352  CALL_METHOD_0         0  ''
              354  STORE_FAST               'accept_val'

 L. 196       356  LOAD_GLOBAL              CIMultiDict

 L. 198       358  LOAD_GLOBAL              hdrs
              360  LOAD_ATTR                UPGRADE
              362  LOAD_STR                 'websocket'

 L. 199       364  LOAD_GLOBAL              hdrs
              366  LOAD_ATTR                CONNECTION
              368  LOAD_STR                 'upgrade'

 L. 200       370  LOAD_GLOBAL              hdrs
              372  LOAD_ATTR                SEC_WEBSOCKET_ACCEPT
              374  LOAD_FAST                'accept_val'

 L. 197       376  BUILD_MAP_3           3 

 L. 196       378  CALL_FUNCTION_1       1  ''
              380  STORE_FAST               'response_headers'

 L. 204       382  LOAD_CONST               False
              384  STORE_FAST               'notakeover'

 L. 205       386  LOAD_CONST               0
              388  STORE_FAST               'compress'

 L. 206       390  LOAD_FAST                'self'
              392  LOAD_ATTR                _compress
          394_396  POP_JUMP_IF_FALSE   456  'to 456'

 L. 207       398  LOAD_FAST                'headers'
              400  LOAD_METHOD              get
              402  LOAD_GLOBAL              hdrs
              404  LOAD_ATTR                SEC_WEBSOCKET_EXTENSIONS
              406  CALL_METHOD_1         1  ''
              408  STORE_FAST               'extensions'

 L. 210       410  LOAD_GLOBAL              ws_ext_parse
              412  LOAD_FAST                'extensions'
              414  LOAD_CONST               True
              416  LOAD_CONST               ('isserver',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  UNPACK_SEQUENCE_2     2 
              422  STORE_FAST               'compress'
              424  STORE_FAST               'notakeover'

 L. 211       426  LOAD_FAST                'compress'
          428_430  POP_JUMP_IF_FALSE   456  'to 456'

 L. 212       432  LOAD_GLOBAL              ws_ext_gen

 L. 213       434  LOAD_FAST                'compress'
              436  LOAD_CONST               True
              438  LOAD_FAST                'notakeover'

 L. 212       440  LOAD_CONST               ('compress', 'isserver', 'server_notakeover')
              442  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              444  STORE_FAST               'enabledext'

 L. 215       446  LOAD_FAST                'enabledext'
              448  LOAD_FAST                'response_headers'
              450  LOAD_GLOBAL              hdrs
              452  LOAD_ATTR                SEC_WEBSOCKET_EXTENSIONS
              454  STORE_SUBSCR     
            456_0  COME_FROM           428  '428'
            456_1  COME_FROM           394  '394'

 L. 217       456  LOAD_FAST                'protocol'
          458_460  POP_JUMP_IF_FALSE   472  'to 472'

 L. 218       462  LOAD_FAST                'protocol'
              464  LOAD_FAST                'response_headers'
              466  LOAD_GLOBAL              hdrs
              468  LOAD_ATTR                SEC_WEBSOCKET_PROTOCOL
              470  STORE_SUBSCR     
            472_0  COME_FROM           458  '458'

 L. 219       472  LOAD_FAST                'response_headers'
              474  LOAD_FAST                'protocol'
              476  LOAD_FAST                'compress'
              478  LOAD_FAST                'notakeover'
              480  BUILD_TUPLE_4         4 
              482  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 74

    def _pre_start--- This code section failed: ---

 L. 222         0  LOAD_FAST                'request'
                2  LOAD_ATTR                _loop
                4  LOAD_FAST                'self'
                6  STORE_ATTR               _loop

 L. 224         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _handshake
               12  LOAD_FAST                'request'
               14  CALL_METHOD_1         1  ''
               16  UNPACK_SEQUENCE_4     4 
               18  STORE_FAST               'headers'
               20  STORE_FAST               'protocol'
               22  STORE_FAST               'compress'
               24  STORE_FAST               'notakeover'

 L. 226        26  LOAD_FAST                'self'
               28  LOAD_METHOD              set_status
               30  LOAD_CONST               101
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 227        36  LOAD_FAST                'self'
               38  LOAD_ATTR                headers
               40  LOAD_METHOD              update
               42  LOAD_FAST                'headers'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 228        48  LOAD_FAST                'self'
               50  LOAD_METHOD              force_close
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L. 229        56  LOAD_FAST                'compress'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _compress

 L. 230        62  LOAD_FAST                'request'
               64  LOAD_ATTR                _protocol
               66  LOAD_ATTR                transport
               68  STORE_FAST               'transport'

 L. 231        70  LOAD_FAST                'transport'
               72  LOAD_CONST               None
               74  <117>                 1  ''
               76  POP_JUMP_IF_TRUE     82  'to 82'
               78  <74>             
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            76  '76'

 L. 232        82  LOAD_GLOBAL              WebSocketWriter

 L. 233        84  LOAD_FAST                'request'
               86  LOAD_ATTR                _protocol
               88  LOAD_FAST                'transport'
               90  LOAD_FAST                'compress'
               92  LOAD_FAST                'notakeover'

 L. 232        94  LOAD_CONST               ('compress', 'notakeover')
               96  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               98  STORE_FAST               'writer'

 L. 236       100  LOAD_FAST                'protocol'
              102  LOAD_FAST                'writer'
              104  BUILD_TUPLE_2         2 
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 74

    def _post_start--- This code section failed: ---

 L. 241         0  LOAD_FAST                'protocol'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _ws_protocol

 L. 242         6  LOAD_FAST                'writer'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _writer

 L. 244        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _reset_heartbeat
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 246        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _loop
               24  STORE_FAST               'loop'

 L. 247        26  LOAD_FAST                'loop'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 248        38  LOAD_GLOBAL              FlowControlDataQueue
               40  LOAD_FAST                'request'
               42  LOAD_ATTR                _protocol
               44  LOAD_CONST               65536
               46  LOAD_FAST                'loop'
               48  LOAD_CONST               ('loop',)
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _reader

 L. 249        56  LOAD_FAST                'request'
               58  LOAD_ATTR                protocol
               60  LOAD_METHOD              set_parser

 L. 250        62  LOAD_GLOBAL              WebSocketReader
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _reader
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _max_msg_size
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _compress
               76  LOAD_CONST               ('compress',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 249        80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 253        84  LOAD_FAST                'request'
               86  LOAD_ATTR                protocol
               88  LOAD_METHOD              keep_alive
               90  LOAD_CONST               False
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

Parse error at or near `<117>' instruction at offset 30

    def can_prepare--- This code section failed: ---

 L. 256         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 257        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Already started'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 258        18  SETUP_FINALLY        42  'to 42'

 L. 259        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _handshake
               24  LOAD_FAST                'request'
               26  CALL_METHOD_1         1  ''
               28  UNPACK_SEQUENCE_4     4 
               30  STORE_FAST               '_'
               32  STORE_FAST               'protocol'
               34  STORE_FAST               '_'
               36  STORE_FAST               '_'
               38  POP_BLOCK        
               40  JUMP_FORWARD         70  'to 70'
             42_0  COME_FROM_FINALLY    18  '18'

 L. 260        42  DUP_TOP          
               44  LOAD_GLOBAL              HTTPException
               46  <121>                68  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 261        54  LOAD_GLOBAL              WebSocketReady
               56  LOAD_CONST               False
               58  LOAD_CONST               None
               60  CALL_FUNCTION_2       2  ''
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
               68  <48>             
             70_0  COME_FROM            40  '40'

 L. 263        70  LOAD_GLOBAL              WebSocketReady
               72  LOAD_CONST               True
               74  LOAD_FAST                'protocol'
               76  CALL_FUNCTION_2       2  ''
               78  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

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

    async def ping--- This code section failed: ---

 L. 285         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 286        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 287        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _writer
               22  LOAD_METHOD              ping
               24  LOAD_FAST                'message'
               26  CALL_METHOD_1         1  ''
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def pong--- This code section failed: ---

 L. 291         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 292        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 293        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _writer
               22  LOAD_METHOD              pong
               24  LOAD_FAST                'message'
               26  CALL_METHOD_1         1  ''
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def send_str--- This code section failed: ---

 L. 296         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 297        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 298        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'data'
               22  LOAD_GLOBAL              str
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     44  'to 44'

 L. 299        28  LOAD_GLOBAL              TypeError
               30  LOAD_STR                 'data argument must be str (%r)'
               32  LOAD_GLOBAL              type
               34  LOAD_FAST                'data'
               36  CALL_FUNCTION_1       1  ''
               38  BINARY_MODULO    
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            26  '26'

 L. 300        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _writer
               48  LOAD_ATTR                send
               50  LOAD_FAST                'data'
               52  LOAD_CONST               False
               54  LOAD_FAST                'compress'
               56  LOAD_CONST               ('binary', 'compress')
               58  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               60  GET_AWAITABLE    
               62  LOAD_CONST               None
               64  YIELD_FROM       
               66  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def send_bytes--- This code section failed: ---

 L. 303         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 304        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 305        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'data'
               22  LOAD_GLOBAL              bytes
               24  LOAD_GLOBAL              bytearray
               26  LOAD_GLOBAL              memoryview
               28  BUILD_TUPLE_3         3 
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_TRUE     50  'to 50'

 L. 306        34  LOAD_GLOBAL              TypeError
               36  LOAD_STR                 'data argument must be byte-ish (%r)'
               38  LOAD_GLOBAL              type
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            32  '32'

 L. 307        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _writer
               54  LOAD_ATTR                send
               56  LOAD_FAST                'data'
               58  LOAD_CONST               True
               60  LOAD_FAST                'compress'
               62  LOAD_CONST               ('binary', 'compress')
               64  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def send_json(self, data: Any, compress: Optional[bool]=None, *, dumps: JSONEncoder=json.dumps) -> None:
        await self.send_str((dumps(data)), compress=compress)

    async def write_eof--- This code section failed: ---

 L. 319         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof_sent
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 320         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 321        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload_writer
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 322        20  LOAD_GLOBAL              RuntimeError
               22  LOAD_STR                 'Response has not been started'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 324        28  LOAD_FAST                'self'
               30  LOAD_METHOD              close
               32  CALL_METHOD_0         0  ''
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          

 L. 325        42  LOAD_CONST               True
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _eof_sent

Parse error at or near `<117>' instruction at offset 16

    async def close--- This code section failed: ---

 L. 328         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _writer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 329        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 331        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _cancel_heartbeat
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          

 L. 332        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _reader
               30  STORE_FAST               'reader'

 L. 333        32  LOAD_FAST                'reader'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 337        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _waiting
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    84  'to 84'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _closed
               58  POP_JUMP_IF_TRUE     84  'to 84'

 L. 338        60  LOAD_FAST                'reader'
               62  LOAD_METHOD              feed_data
               64  LOAD_GLOBAL              WS_CLOSING_MESSAGE
               66  LOAD_CONST               0
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          

 L. 339        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _waiting
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  POP_TOP          
             84_0  COME_FROM            58  '58'
             84_1  COME_FROM            52  '52'

 L. 341        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _closed
            88_90  POP_JUMP_IF_TRUE    468  'to 468'

 L. 342        92  LOAD_CONST               True
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _closed

 L. 343        98  SETUP_FINALLY       156  'to 156'

 L. 344       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _writer
              104  LOAD_METHOD              close
              106  LOAD_FAST                'code'
              108  LOAD_FAST                'message'
              110  CALL_METHOD_2         2  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_TOP          

 L. 345       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _payload_writer
              124  STORE_FAST               'writer'

 L. 346       126  LOAD_FAST                'writer'
              128  LOAD_CONST               None
              130  <117>                 1  ''
              132  POP_JUMP_IF_TRUE    138  'to 138'
              134  <74>             
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           132  '132'

 L. 347       138  LOAD_FAST                'writer'
              140  LOAD_METHOD              drain
              142  CALL_METHOD_0         0  ''
              144  GET_AWAITABLE    
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  POP_TOP          
              152  POP_BLOCK        
              154  JUMP_FORWARD        238  'to 238'
            156_0  COME_FROM_FINALLY    98  '98'

 L. 348       156  DUP_TOP          
              158  LOAD_GLOBAL              asyncio
              160  LOAD_ATTR                CancelledError
              162  LOAD_GLOBAL              asyncio
              164  LOAD_ATTR                TimeoutError
              166  BUILD_TUPLE_2         2 
              168  <121>               188  ''
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 349       176  LOAD_CONST               1006
              178  LOAD_FAST                'self'
              180  STORE_ATTR               _close_code

 L. 350       182  RAISE_VARARGS_0       0  'reraise'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        238  'to 238'

 L. 351       188  DUP_TOP          
              190  LOAD_GLOBAL              Exception
              192  <121>               236  ''
              194  POP_TOP          
              196  STORE_FAST               'exc'
              198  POP_TOP          
              200  SETUP_FINALLY       228  'to 228'

 L. 352       202  LOAD_CONST               1006
              204  LOAD_FAST                'self'
              206  STORE_ATTR               _close_code

 L. 353       208  LOAD_FAST                'exc'
              210  LOAD_FAST                'self'
              212  STORE_ATTR               _exception

 L. 354       214  POP_BLOCK        
              216  POP_EXCEPT       
              218  LOAD_CONST               None
              220  STORE_FAST               'exc'
              222  DELETE_FAST              'exc'
              224  LOAD_CONST               True
              226  RETURN_VALUE     
            228_0  COME_FROM_FINALLY   200  '200'
              228  LOAD_CONST               None
              230  STORE_FAST               'exc'
              232  DELETE_FAST              'exc'
              234  <48>             
              236  <48>             
            238_0  COME_FROM           186  '186'
            238_1  COME_FROM           154  '154'

 L. 356       238  LOAD_FAST                'self'
              240  LOAD_ATTR                _closing
          242_244  POP_JUMP_IF_FALSE   250  'to 250'

 L. 357       246  LOAD_CONST               True
              248  RETURN_VALUE     
            250_0  COME_FROM           242  '242'

 L. 359       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _reader
              254  STORE_FAST               'reader'

 L. 360       256  LOAD_FAST                'reader'
              258  LOAD_CONST               None
              260  <117>                 1  ''
          262_264  POP_JUMP_IF_TRUE    270  'to 270'
              266  <74>             
              268  RAISE_VARARGS_1       1  'exception instance'
            270_0  COME_FROM           262  '262'

 L. 361       270  SETUP_FINALLY       342  'to 342'

 L. 362       272  LOAD_GLOBAL              async_timeout
              274  LOAD_ATTR                timeout
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                _timeout
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                _loop
              284  LOAD_CONST               ('loop',)
              286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              288  SETUP_WITH          320  'to 320'
              290  POP_TOP          

 L. 363       292  LOAD_FAST                'reader'
              294  LOAD_METHOD              read
              296  CALL_METHOD_0         0  ''
              298  GET_AWAITABLE    
              300  LOAD_CONST               None
              302  YIELD_FROM       
              304  STORE_FAST               'msg'
              306  POP_BLOCK        
              308  LOAD_CONST               None
              310  DUP_TOP          
              312  DUP_TOP          
              314  CALL_FUNCTION_3       3  ''
              316  POP_TOP          
              318  JUMP_FORWARD        338  'to 338'
            320_0  COME_FROM_WITH      288  '288'
              320  <49>             
          322_324  POP_JUMP_IF_TRUE    328  'to 328'
              326  <48>             
            328_0  COME_FROM           322  '322'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          
              334  POP_EXCEPT       
              336  POP_TOP          
            338_0  COME_FROM           318  '318'
              338  POP_BLOCK        
              340  JUMP_FORWARD        422  'to 422'
            342_0  COME_FROM_FINALLY   270  '270'

 L. 364       342  DUP_TOP          
              344  LOAD_GLOBAL              asyncio
              346  LOAD_ATTR                CancelledError
          348_350  <121>               370  ''
              352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L. 365       358  LOAD_CONST               1006
              360  LOAD_FAST                'self'
              362  STORE_ATTR               _close_code

 L. 366       364  RAISE_VARARGS_0       0  'reraise'
              366  POP_EXCEPT       
              368  JUMP_FORWARD        422  'to 422'

 L. 367       370  DUP_TOP          
              372  LOAD_GLOBAL              Exception
          374_376  <121>               420  ''
              378  POP_TOP          
              380  STORE_FAST               'exc'
              382  POP_TOP          
              384  SETUP_FINALLY       412  'to 412'

 L. 368       386  LOAD_CONST               1006
              388  LOAD_FAST                'self'
              390  STORE_ATTR               _close_code

 L. 369       392  LOAD_FAST                'exc'
              394  LOAD_FAST                'self'
              396  STORE_ATTR               _exception

 L. 370       398  POP_BLOCK        
              400  POP_EXCEPT       
              402  LOAD_CONST               None
              404  STORE_FAST               'exc'
              406  DELETE_FAST              'exc'
              408  LOAD_CONST               True
              410  RETURN_VALUE     
            412_0  COME_FROM_FINALLY   384  '384'
              412  LOAD_CONST               None
              414  STORE_FAST               'exc'
              416  DELETE_FAST              'exc'
              418  <48>             
              420  <48>             
            422_0  COME_FROM           368  '368'
            422_1  COME_FROM           340  '340'

 L. 372       422  LOAD_FAST                'msg'
              424  LOAD_ATTR                type
              426  LOAD_GLOBAL              WSMsgType
              428  LOAD_ATTR                CLOSE
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   448  'to 448'

 L. 373       436  LOAD_FAST                'msg'
              438  LOAD_ATTR                data
              440  LOAD_FAST                'self'
              442  STORE_ATTR               _close_code

 L. 374       444  LOAD_CONST               True
              446  RETURN_VALUE     
            448_0  COME_FROM           432  '432'

 L. 376       448  LOAD_CONST               1006
              450  LOAD_FAST                'self'
              452  STORE_ATTR               _close_code

 L. 377       454  LOAD_GLOBAL              asyncio
              456  LOAD_METHOD              TimeoutError
              458  CALL_METHOD_0         0  ''
              460  LOAD_FAST                'self'
              462  STORE_ATTR               _exception

 L. 378       464  LOAD_CONST               True
              466  RETURN_VALUE     
            468_0  COME_FROM            88  '88'

 L. 380       468  LOAD_CONST               False
              470  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    async def receive--- This code section failed: ---

 L. 383         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reader
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 384        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Call .prepare() first'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 386        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  STORE_FAST               'loop'

 L. 387        24  LOAD_FAST                'loop'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM           650  '650'
             36_1  COME_FROM           624  '624'
             36_2  COME_FROM            30  '30'

 L. 389        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _waiting
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 390        46  LOAD_GLOBAL              RuntimeError
               48  LOAD_STR                 'Concurrent call to receive() is not allowed'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L. 392        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _closed
               58  POP_JUMP_IF_FALSE    96  'to 96'

 L. 393        60  LOAD_FAST                'self'
               62  DUP_TOP          
               64  LOAD_ATTR                _conn_lost
               66  LOAD_CONST               1
               68  INPLACE_ADD      
               70  ROT_TWO          
               72  STORE_ATTR               _conn_lost

 L. 394        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _conn_lost
               78  LOAD_GLOBAL              THRESHOLD_CONNLOST_ACCESS
               80  COMPARE_OP               >=
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 395        84  LOAD_GLOBAL              RuntimeError
               86  LOAD_STR                 'WebSocket connection is closed.'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 396        92  LOAD_GLOBAL              WS_CLOSED_MESSAGE
               94  RETURN_VALUE     
             96_0  COME_FROM            58  '58'

 L. 397        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _closing
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 398       102  LOAD_GLOBAL              WS_CLOSING_MESSAGE
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 400       106  SETUP_FINALLY       254  'to 254'

 L. 401       108  LOAD_FAST                'loop'
              110  LOAD_METHOD              create_future
              112  CALL_METHOD_0         0  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _waiting

 L. 402       118  SETUP_FINALLY       224  'to 224'

 L. 403       120  LOAD_GLOBAL              async_timeout
              122  LOAD_ATTR                timeout

 L. 404       124  LOAD_FAST                'timeout'
              126  JUMP_IF_TRUE_OR_POP   132  'to 132'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _receive_timeout
            132_0  COME_FROM           126  '126'
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _loop

 L. 403       136  LOAD_CONST               ('loop',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  SETUP_WITH          174  'to 174'
              142  POP_TOP          

 L. 406       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _reader
              148  LOAD_METHOD              read
              150  CALL_METHOD_0         0  ''
              152  GET_AWAITABLE    
              154  LOAD_CONST               None
              156  YIELD_FROM       
              158  STORE_FAST               'msg'
              160  POP_BLOCK        
              162  LOAD_CONST               None
              164  DUP_TOP          
              166  DUP_TOP          
              168  CALL_FUNCTION_3       3  ''
              170  POP_TOP          
              172  JUMP_FORWARD        190  'to 190'
            174_0  COME_FROM_WITH      140  '140'
              174  <49>             
              176  POP_JUMP_IF_TRUE    180  'to 180'
              178  <48>             
            180_0  COME_FROM           176  '176'
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          
              186  POP_EXCEPT       
              188  POP_TOP          
            190_0  COME_FROM           172  '172'

 L. 407       190  LOAD_FAST                'self'
              192  LOAD_METHOD              _reset_heartbeat
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
              198  POP_BLOCK        

 L. 409       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _waiting
              204  STORE_FAST               'waiter'

 L. 410       206  LOAD_GLOBAL              set_result
              208  LOAD_FAST                'waiter'
              210  LOAD_CONST               True
              212  CALL_FUNCTION_2       2  ''
              214  POP_TOP          

 L. 411       216  LOAD_CONST               None
              218  LOAD_FAST                'self'
              220  STORE_ATTR               _waiting
              222  JUMP_FORWARD        248  'to 248'
            224_0  COME_FROM_FINALLY   118  '118'

 L. 409       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _waiting
              228  STORE_FAST               'waiter'

 L. 410       230  LOAD_GLOBAL              set_result
              232  LOAD_FAST                'waiter'
              234  LOAD_CONST               True
              236  CALL_FUNCTION_2       2  ''
              238  POP_TOP          

 L. 411       240  LOAD_CONST               None
              242  LOAD_FAST                'self'
              244  STORE_ATTR               _waiting
              246  <48>             
            248_0  COME_FROM           222  '222'
              248  POP_BLOCK        
          250_252  JUMP_FORWARD        502  'to 502'
            254_0  COME_FROM_FINALLY   106  '106'

 L. 412       254  DUP_TOP          
              256  LOAD_GLOBAL              asyncio
              258  LOAD_ATTR                CancelledError
              260  LOAD_GLOBAL              asyncio
              262  LOAD_ATTR                TimeoutError
              264  BUILD_TUPLE_2         2 
          266_268  <121>               288  ''
              270  POP_TOP          
              272  POP_TOP          
              274  POP_TOP          

 L. 413       276  LOAD_CONST               1006
              278  LOAD_FAST                'self'
              280  STORE_ATTR               _close_code

 L. 414       282  RAISE_VARARGS_0       0  'reraise'
              284  POP_EXCEPT       
              286  JUMP_FORWARD        502  'to 502'

 L. 415       288  DUP_TOP          
              290  LOAD_GLOBAL              EofStream
          292_294  <121>               340  ''
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 416       302  LOAD_CONST               1000
              304  LOAD_FAST                'self'
              306  STORE_ATTR               _close_code

 L. 417       308  LOAD_FAST                'self'
              310  LOAD_METHOD              close
              312  CALL_METHOD_0         0  ''
              314  GET_AWAITABLE    
              316  LOAD_CONST               None
              318  YIELD_FROM       
              320  POP_TOP          

 L. 418       322  LOAD_GLOBAL              WSMessage
              324  LOAD_GLOBAL              WSMsgType
              326  LOAD_ATTR                CLOSED
              328  LOAD_CONST               None
              330  LOAD_CONST               None
              332  CALL_FUNCTION_3       3  ''
              334  ROT_FOUR         
              336  POP_EXCEPT       
              338  RETURN_VALUE     

 L. 419       340  DUP_TOP          
              342  LOAD_GLOBAL              WebSocketError
          344_346  <121>               418  ''
              348  POP_TOP          
              350  STORE_FAST               'exc'
              352  POP_TOP          
              354  SETUP_FINALLY       410  'to 410'

 L. 420       356  LOAD_FAST                'exc'
              358  LOAD_ATTR                code
              360  LOAD_FAST                'self'
              362  STORE_ATTR               _close_code

 L. 421       364  LOAD_FAST                'self'
              366  LOAD_ATTR                close
              368  LOAD_FAST                'exc'
              370  LOAD_ATTR                code
              372  LOAD_CONST               ('code',)
              374  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              376  GET_AWAITABLE    
              378  LOAD_CONST               None
              380  YIELD_FROM       
              382  POP_TOP          

 L. 422       384  LOAD_GLOBAL              WSMessage
              386  LOAD_GLOBAL              WSMsgType
              388  LOAD_ATTR                ERROR
              390  LOAD_FAST                'exc'
              392  LOAD_CONST               None
              394  CALL_FUNCTION_3       3  ''
              396  POP_BLOCK        
              398  ROT_FOUR         
              400  POP_EXCEPT       
              402  LOAD_CONST               None
              404  STORE_FAST               'exc'
              406  DELETE_FAST              'exc'
              408  RETURN_VALUE     
            410_0  COME_FROM_FINALLY   354  '354'
              410  LOAD_CONST               None
              412  STORE_FAST               'exc'
              414  DELETE_FAST              'exc'
              416  <48>             

 L. 423       418  DUP_TOP          
              420  LOAD_GLOBAL              Exception
          422_424  <121>               500  ''
              426  POP_TOP          
              428  STORE_FAST               'exc'
              430  POP_TOP          
              432  SETUP_FINALLY       492  'to 492'

 L. 424       434  LOAD_FAST                'exc'
              436  LOAD_FAST                'self'
              438  STORE_ATTR               _exception

 L. 425       440  LOAD_CONST               True
              442  LOAD_FAST                'self'
              444  STORE_ATTR               _closing

 L. 426       446  LOAD_CONST               1006
              448  LOAD_FAST                'self'
              450  STORE_ATTR               _close_code

 L. 427       452  LOAD_FAST                'self'
              454  LOAD_METHOD              close
              456  CALL_METHOD_0         0  ''
              458  GET_AWAITABLE    
              460  LOAD_CONST               None
              462  YIELD_FROM       
              464  POP_TOP          

 L. 428       466  LOAD_GLOBAL              WSMessage
              468  LOAD_GLOBAL              WSMsgType
              470  LOAD_ATTR                ERROR
              472  LOAD_FAST                'exc'
              474  LOAD_CONST               None
              476  CALL_FUNCTION_3       3  ''
              478  POP_BLOCK        
              480  ROT_FOUR         
              482  POP_EXCEPT       
              484  LOAD_CONST               None
              486  STORE_FAST               'exc'
              488  DELETE_FAST              'exc'
              490  RETURN_VALUE     
            492_0  COME_FROM_FINALLY   432  '432'
              492  LOAD_CONST               None
              494  STORE_FAST               'exc'
              496  DELETE_FAST              'exc'
              498  <48>             
              500  <48>             
            502_0  COME_FROM           286  '286'
            502_1  COME_FROM           250  '250'

 L. 430       502  LOAD_FAST                'msg'
              504  LOAD_ATTR                type
              506  LOAD_GLOBAL              WSMsgType
              508  LOAD_ATTR                CLOSE
              510  COMPARE_OP               ==
          512_514  POP_JUMP_IF_FALSE   562  'to 562'

 L. 431       516  LOAD_CONST               True
              518  LOAD_FAST                'self'
              520  STORE_ATTR               _closing

 L. 432       522  LOAD_FAST                'msg'
              524  LOAD_ATTR                data
              526  LOAD_FAST                'self'
              528  STORE_ATTR               _close_code

 L. 433       530  LOAD_FAST                'self'
              532  LOAD_ATTR                _closed
          534_536  POP_JUMP_IF_TRUE    652  'to 652'
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                _autoclose
          542_544  POP_JUMP_IF_FALSE   652  'to 652'

 L. 434       546  LOAD_FAST                'self'
              548  LOAD_METHOD              close
              550  CALL_METHOD_0         0  ''
              552  GET_AWAITABLE    
              554  LOAD_CONST               None
              556  YIELD_FROM       
              558  POP_TOP          
              560  JUMP_FORWARD        652  'to 652'
            562_0  COME_FROM           512  '512'

 L. 435       562  LOAD_FAST                'msg'
              564  LOAD_ATTR                type
              566  LOAD_GLOBAL              WSMsgType
              568  LOAD_ATTR                CLOSING
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   584  'to 584'

 L. 436       576  LOAD_CONST               True
              578  LOAD_FAST                'self'
              580  STORE_ATTR               _closing
              582  JUMP_FORWARD        652  'to 652'
            584_0  COME_FROM           572  '572'

 L. 437       584  LOAD_FAST                'msg'
              586  LOAD_ATTR                type
              588  LOAD_GLOBAL              WSMsgType
              590  LOAD_ATTR                PING
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   628  'to 628'
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                _autoping
          602_604  POP_JUMP_IF_FALSE   628  'to 628'

 L. 438       606  LOAD_FAST                'self'
              608  LOAD_METHOD              pong
              610  LOAD_FAST                'msg'
              612  LOAD_ATTR                data
              614  CALL_METHOD_1         1  ''
              616  GET_AWAITABLE    
              618  LOAD_CONST               None
              620  YIELD_FROM       
              622  POP_TOP          

 L. 439       624  JUMP_BACK            36  'to 36'
              626  BREAK_LOOP          652  'to 652'
            628_0  COME_FROM           602  '602'
            628_1  COME_FROM           594  '594'

 L. 440       628  LOAD_FAST                'msg'
              630  LOAD_ATTR                type
              632  LOAD_GLOBAL              WSMsgType
              634  LOAD_ATTR                PONG
              636  COMPARE_OP               ==
          638_640  POP_JUMP_IF_FALSE   652  'to 652'
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                _autoping
          646_648  POP_JUMP_IF_FALSE   652  'to 652'

 L. 441       650  JUMP_BACK            36  'to 36'
            652_0  COME_FROM           646  '646'
            652_1  COME_FROM           638  '638'
            652_2  COME_FROM           626  '626'
            652_3  COME_FROM           582  '582'
            652_4  COME_FROM           560  '560'
            652_5  COME_FROM           542  '542'
            652_6  COME_FROM           534  '534'

 L. 443       652  LOAD_FAST                'msg'
              654  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    async def receive_str(self, *, timeout: Optional[float]=None) -> str:
        msg = await self.receivetimeout
        if msg.type != WSMsgType.TEXT:
            raise TypeError('Received message {}:{!r} is not WSMsgType.TEXT'.formatmsg.typemsg.data)
        return msg.data

    async def receive_bytes(self, *, timeout: Optional[float]=None) -> bytes:
        msg = await self.receivetimeout
        if msg.type != WSMsgType.BINARY:
            raise TypeError(f"Received message {msg.type}:{msg.data!r} is not bytes")
        return msg.data

    async def receive_json(self, *, loads: JSONDecoder=json.loads, timeout: Optional[float]=None) -> Any:
        data = await self.receive_str(timeout=timeout)
        return loads(data)

    async def write(self, data: bytes) -> None:
        raise RuntimeError('Cannot call .write() for websocket')

    def __aiter__(self) -> 'WebSocketResponse':
        return self

    async def __anext__--- This code section failed: ---

 L. 474         0  LOAD_FAST                'self'
                2  LOAD_METHOD              receive
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'msg'

 L. 475        14  LOAD_FAST                'msg'
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

 L. 476        36  LOAD_GLOBAL              StopAsyncIteration
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 477        40  LOAD_FAST                'msg'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 32

    def _cancel--- This code section failed: ---

 L. 480         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _reader
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 481        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _reader
               14  LOAD_METHOD              set_exception
               16  LOAD_FAST                'exc'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1