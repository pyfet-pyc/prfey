# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\client_proto.py
import asyncio
from contextlib import suppress
from typing import Any, Optional, Tuple
from .base_protocol import BaseProtocol
from .client_exceptions import ClientOSError, ClientPayloadError, ServerDisconnectedError, ServerTimeoutError
from .helpers import BaseTimerContext
from .http import HttpResponseParser, RawResponseMessage
from .streams import EMPTY_PAYLOAD, DataQueue, StreamReader

class ResponseHandler(BaseProtocol, DataQueue[Tuple[(RawResponseMessage, StreamReader)]]):
    __doc__ = 'Helper class to adapt between Protocol and StreamReader.'

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        BaseProtocol.__init__(self, loop=loop)
        DataQueue.__init__(self, loop)
        self._should_close = False
        self._payload = None
        self._skip_payload = False
        self._payload_parser = None
        self._timer = None
        self._tail = b''
        self._upgraded = False
        self._parser = None
        self._read_timeout = None
        self._read_timeout_handle = None

    @property
    def upgraded(self) -> bool:
        return self._upgraded

    @property
    def should_close--- This code section failed: ---

 L.  45         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload
               14  LOAD_METHOD              is_eof
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'
             20_0  COME_FROM             8  '8'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _upgraded
               24  POP_JUMP_IF_FALSE    30  'to 30'
             26_0  COME_FROM            18  '18'

 L.  46        26  LOAD_CONST               True
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  49        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _should_close
               34  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  50        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _upgraded

 L.  49        40  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  51        42  LOAD_FAST                'self'
               44  LOAD_METHOD              exception
               46  CALL_METHOD_0         0  ''
               48  LOAD_CONST               None
               50  <117>                 1  ''

 L.  49        52  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  52        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _payload_parser
               58  LOAD_CONST               None
               60  <117>                 1  ''

 L.  49        62  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  53        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'self'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               0
               72  COMPARE_OP               >

 L.  49        74  JUMP_IF_TRUE_OR_POP    84  'to 84'

 L.  54        76  LOAD_GLOBAL              bool
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _tail
               82  CALL_FUNCTION_1       1  ''
             84_0  COME_FROM            74  '74'
             84_1  COME_FROM            62  '62'
             84_2  COME_FROM            52  '52'
             84_3  COME_FROM            40  '40'
             84_4  COME_FROM            34  '34'

 L.  48        84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def force_close(self) -> None:
        self._should_close = True

    def close--- This code section failed: ---

 L.  61         0  LOAD_FAST                'self'
                2  LOAD_ATTR                transport
                4  STORE_FAST               'transport'

 L.  62         6  LOAD_FAST                'transport'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    42  'to 42'

 L.  63        14  LOAD_FAST                'transport'
               16  LOAD_METHOD              close
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L.  64        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               transport

 L.  65        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _payload

 L.  66        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _drop_timeout
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          
             42_0  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 10

    def is_connected--- This code section failed: ---

 L.  69         0  LOAD_FAST                'self'
                2  LOAD_ATTR                transport
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  JUMP_IF_FALSE_OR_POP    20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                transport
               14  LOAD_METHOD              is_closing
               16  CALL_METHOD_0         0  ''
               18  UNARY_NOT        
             20_0  COME_FROM             8  '8'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def connection_lost--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _drop_timeout
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  74         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _payload_parser
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    68  'to 68'

 L.  75        18  LOAD_GLOBAL              suppress
               20  LOAD_GLOBAL              Exception
               22  CALL_FUNCTION_1       1  ''
               24  SETUP_WITH           52  'to 52'
               26  POP_TOP          

 L.  76        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _payload_parser
               32  LOAD_METHOD              feed_eof
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
               38  POP_BLOCK        
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_WITH       24  '24'
               52  <49>             
               54  POP_JUMP_IF_TRUE     58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          
               64  POP_EXCEPT       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'
             68_1  COME_FROM            16  '16'

 L.  78        68  LOAD_CONST               None
               70  STORE_FAST               'uncompleted'

 L.  79        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _parser
               76  LOAD_CONST               None
               78  <117>                 1  ''
               80  POP_JUMP_IF_FALSE   142  'to 142'

 L.  80        82  SETUP_FINALLY        98  'to 98'

 L.  81        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _parser
               88  LOAD_METHOD              feed_eof
               90  CALL_METHOD_0         0  ''
               92  STORE_FAST               'uncompleted'
               94  POP_BLOCK        
               96  JUMP_FORWARD        142  'to 142'
             98_0  COME_FROM_FINALLY    82  '82'

 L.  82        98  DUP_TOP          
              100  LOAD_GLOBAL              Exception
              102  <121>               140  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L.  83       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _payload
              114  LOAD_CONST               None
              116  <117>                 1  ''
              118  POP_JUMP_IF_FALSE   136  'to 136'

 L.  84       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _payload
              124  LOAD_METHOD              set_exception

 L.  85       126  LOAD_GLOBAL              ClientPayloadError
              128  LOAD_STR                 'Response payload is not completed'
              130  CALL_FUNCTION_1       1  ''

 L.  84       132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM           118  '118'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM            96  '96'
            142_2  COME_FROM            80  '80'

 L.  88       142  LOAD_FAST                'self'
              144  LOAD_METHOD              is_eof
              146  CALL_METHOD_0         0  ''
              148  POP_JUMP_IF_TRUE    196  'to 196'

 L.  89       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'exc'
              154  LOAD_GLOBAL              OSError
              156  CALL_FUNCTION_2       2  ''
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L.  90       160  LOAD_GLOBAL              ClientOSError
              162  LOAD_FAST                'exc'
              164  LOAD_ATTR                args
              166  CALL_FUNCTION_EX      0  'positional arguments only'
              168  STORE_FAST               'exc'
            170_0  COME_FROM           158  '158'

 L.  91       170  LOAD_FAST                'exc'
              172  LOAD_CONST               None
              174  <117>                 0  ''
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L.  92       178  LOAD_GLOBAL              ServerDisconnectedError
              180  LOAD_FAST                'uncompleted'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'exc'
            186_0  COME_FROM           176  '176'

 L.  95       186  LOAD_FAST                'self'
              188  LOAD_METHOD              set_exception
              190  LOAD_FAST                'exc'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           148  '148'

 L.  97       196  LOAD_CONST               True
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _should_close

 L.  98       202  LOAD_CONST               None
              204  LOAD_FAST                'self'
              206  STORE_ATTR               _parser

 L.  99       208  LOAD_CONST               None
              210  LOAD_FAST                'self'
              212  STORE_ATTR               _payload

 L. 100       214  LOAD_CONST               None
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _payload_parser

 L. 101       220  LOAD_CONST               False
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _reading_paused

 L. 103       226  LOAD_GLOBAL              super
              228  CALL_FUNCTION_0       0  ''
              230  LOAD_METHOD              connection_lost
              232  LOAD_FAST                'exc'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          

Parse error at or near `<117>' instruction at offset 14

    def eof_received(self) -> None:
        self._drop_timeout

    def pause_reading(self):
        super.pause_reading
        self._drop_timeout

    def resume_reading(self):
        super.resume_reading
        self._reschedule_timeout

    def set_exception(self, exc):
        self._should_close = True
        self._drop_timeout
        super.set_exceptionexc

    def set_parser(self, parser: Any, payload: Any) -> None:
        self._payload = payload
        self._payload_parser = parser
        self._drop_timeout
        if self._tail:
            data, self._tail = self._tail, b''
            self.data_receiveddata

    def set_response_params(self, *, timer: Optional[BaseTimerContext]=None, skip_payload: bool=False, read_until_eof: bool=False, auto_decompress: bool=True, read_timeout: Optional[float]=None, read_bufsize: int=65536) -> None:
        self._skip_payload = skip_payload
        self._read_timeout = read_timeout
        self._reschedule_timeout
        self._parser = HttpResponseParser(self,
          (self._loop),
          read_bufsize,
          timer=timer,
          payload_exception=ClientPayloadError,
          response_with_body=(not skip_payload),
          read_until_eof=read_until_eof,
          auto_decompress=auto_decompress)
        if self._tail:
            data, self._tail = self._tail, b''
            self.data_receiveddata

    def _drop_timeout--- This code section failed: ---

 L. 168         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _read_timeout_handle
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 169        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _read_timeout_handle
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 170        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _read_timeout_handle
             26_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _reschedule_timeout--- This code section failed: ---

 L. 173         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _read_timeout
                4  STORE_FAST               'timeout'

 L. 174         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _read_timeout_handle
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 175        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _read_timeout_handle
               20  LOAD_METHOD              cancel
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L. 177        26  LOAD_FAST                'timeout'
               28  POP_JUMP_IF_FALSE    50  'to 50'

 L. 178        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _loop
               34  LOAD_METHOD              call_later

 L. 179        36  LOAD_FAST                'timeout'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _on_read_timeout

 L. 178        42  CALL_METHOD_2         2  ''
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _read_timeout_handle
               48  JUMP_FORWARD         56  'to 56'
             50_0  COME_FROM            28  '28'

 L. 182        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _read_timeout_handle
             56_0  COME_FROM            48  '48'

Parse error at or near `<117>' instruction at offset 12

    def _on_read_timeout--- This code section failed: ---

 L. 185         0  LOAD_GLOBAL              ServerTimeoutError
                2  LOAD_STR                 'Timeout on reading data from socket'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'exc'

 L. 186         8  LOAD_FAST                'self'
               10  LOAD_METHOD              set_exception
               12  LOAD_FAST                'exc'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 187        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _payload
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 188        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _payload
               32  LOAD_METHOD              set_exception
               34  LOAD_FAST                'exc'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
             40_0  COME_FROM            26  '26'

Parse error at or near `<117>' instruction at offset 24

    def data_received--- This code section failed: ---

 L. 191         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _reschedule_timeout
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 193         8  LOAD_FAST                'data'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 194        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 197        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _payload_parser
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    76  'to 76'

 L. 198        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _payload_parser
               30  LOAD_METHOD              feed_data
               32  LOAD_FAST                'data'
               34  CALL_METHOD_1         1  ''
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'eof'
               40  STORE_FAST               'tail'

 L. 199        42  LOAD_FAST                'eof'
               44  POP_JUMP_IF_FALSE    72  'to 72'

 L. 200        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _payload

 L. 201        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _payload_parser

 L. 203        58  LOAD_FAST                'tail'
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 204        62  LOAD_FAST                'self'
               64  LOAD_METHOD              data_received
               66  LOAD_FAST                'tail'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
             72_0  COME_FROM            60  '60'
             72_1  COME_FROM            44  '44'

 L. 205        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            24  '24'

 L. 207        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _upgraded
               80  POP_JUMP_IF_TRUE     92  'to 92'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _parser
               86  LOAD_CONST               None
               88  <117>                 0  ''
               90  POP_JUMP_IF_FALSE   110  'to 110'
             92_0  COME_FROM            80  '80'

 L. 209        92  LOAD_FAST                'self'
               94  DUP_TOP          
               96  LOAD_ATTR                _tail
               98  LOAD_FAST                'data'
              100  INPLACE_ADD      
              102  ROT_TWO          
              104  STORE_ATTR               _tail
          106_108  JUMP_FORWARD        370  'to 370'
            110_0  COME_FROM            90  '90'

 L. 212       110  SETUP_FINALLY       134  'to 134'

 L. 213       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _parser
              116  LOAD_METHOD              feed_data
              118  LOAD_FAST                'data'
              120  CALL_METHOD_1         1  ''
              122  UNPACK_SEQUENCE_3     3 
              124  STORE_FAST               'messages'
              126  STORE_FAST               'upgraded'
              128  STORE_FAST               'tail'
              130  POP_BLOCK        
              132  JUMP_FORWARD        202  'to 202'
            134_0  COME_FROM_FINALLY   110  '110'

 L. 214       134  DUP_TOP          
              136  LOAD_GLOBAL              BaseException
              138  <121>               200  ''
              140  POP_TOP          
              142  STORE_FAST               'exc'
              144  POP_TOP          
              146  SETUP_FINALLY       192  'to 192'

 L. 215       148  LOAD_FAST                'self'
              150  LOAD_ATTR                transport
              152  LOAD_CONST               None
              154  <117>                 1  ''
              156  POP_JUMP_IF_FALSE   168  'to 168'

 L. 219       158  LOAD_FAST                'self'
              160  LOAD_ATTR                transport
              162  LOAD_METHOD              close
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
            168_0  COME_FROM           156  '156'

 L. 221       168  LOAD_FAST                'self'
              170  LOAD_METHOD              set_exception
              172  LOAD_FAST                'exc'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 222       178  POP_BLOCK        
              180  POP_EXCEPT       
              182  LOAD_CONST               None
              184  STORE_FAST               'exc'
              186  DELETE_FAST              'exc'
              188  LOAD_CONST               None
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY   146  '146'
              192  LOAD_CONST               None
              194  STORE_FAST               'exc'
              196  DELETE_FAST              'exc'
              198  <48>             
              200  <48>             
            202_0  COME_FROM           132  '132'

 L. 224       202  LOAD_FAST                'upgraded'
              204  LOAD_FAST                'self'
              206  STORE_ATTR               _upgraded

 L. 226       208  LOAD_CONST               None
              210  STORE_FAST               'payload'

 L. 227       212  LOAD_FAST                'messages'
              214  GET_ITER         
            216_0  COME_FROM           296  '296'
            216_1  COME_FROM           278  '278'
              216  FOR_ITER            298  'to 298'
              218  UNPACK_SEQUENCE_2     2 
              220  STORE_FAST               'message'
              222  STORE_FAST               'payload'

 L. 228       224  LOAD_FAST                'message'
              226  LOAD_ATTR                should_close
              228  POP_JUMP_IF_FALSE   236  'to 236'

 L. 229       230  LOAD_CONST               True
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _should_close
            236_0  COME_FROM           228  '228'

 L. 231       236  LOAD_FAST                'payload'
              238  LOAD_FAST                'self'
              240  STORE_ATTR               _payload

 L. 233       242  LOAD_FAST                'self'
              244  LOAD_ATTR                _skip_payload
          246_248  POP_JUMP_IF_TRUE    262  'to 262'
              250  LOAD_FAST                'message'
              252  LOAD_ATTR                code
              254  LOAD_CONST               (204, 304)
              256  <118>                 0  ''
          258_260  POP_JUMP_IF_FALSE   280  'to 280'
            262_0  COME_FROM           246  '246'

 L. 234       262  LOAD_FAST                'self'
              264  LOAD_METHOD              feed_data
              266  LOAD_FAST                'message'
              268  LOAD_GLOBAL              EMPTY_PAYLOAD
              270  BUILD_TUPLE_2         2 
              272  LOAD_CONST               0
              274  CALL_METHOD_2         2  ''
              276  POP_TOP          
              278  JUMP_BACK           216  'to 216'
            280_0  COME_FROM           258  '258'

 L. 236       280  LOAD_FAST                'self'
              282  LOAD_METHOD              feed_data
              284  LOAD_FAST                'message'
              286  LOAD_FAST                'payload'
              288  BUILD_TUPLE_2         2 
              290  LOAD_CONST               0
              292  CALL_METHOD_2         2  ''
              294  POP_TOP          
              296  JUMP_BACK           216  'to 216'
            298_0  COME_FROM           216  '216'

 L. 237       298  LOAD_FAST                'payload'
              300  LOAD_CONST               None
              302  <117>                 1  ''
          304_306  POP_JUMP_IF_FALSE   340  'to 340'

 L. 242       308  LOAD_FAST                'payload'
              310  LOAD_GLOBAL              EMPTY_PAYLOAD
              312  <117>                 1  ''
          314_316  POP_JUMP_IF_FALSE   332  'to 332'

 L. 243       318  LOAD_FAST                'payload'
              320  LOAD_METHOD              on_eof
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                _drop_timeout
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          
              330  JUMP_FORWARD        340  'to 340'
            332_0  COME_FROM           314  '314'

 L. 245       332  LOAD_FAST                'self'
              334  LOAD_METHOD              _drop_timeout
              336  CALL_METHOD_0         0  ''
              338  POP_TOP          
            340_0  COME_FROM           330  '330'
            340_1  COME_FROM           304  '304'

 L. 247       340  LOAD_FAST                'tail'
          342_344  POP_JUMP_IF_FALSE   370  'to 370'

 L. 248       346  LOAD_FAST                'upgraded'
          348_350  POP_JUMP_IF_FALSE   364  'to 364'

 L. 249       352  LOAD_FAST                'self'
              354  LOAD_METHOD              data_received
              356  LOAD_FAST                'tail'
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
              362  JUMP_FORWARD        370  'to 370'
            364_0  COME_FROM           348  '348'

 L. 251       364  LOAD_FAST                'tail'
              366  LOAD_FAST                'self'
              368  STORE_ATTR               _tail
            370_0  COME_FROM           362  '362'
            370_1  COME_FROM           342  '342'
            370_2  COME_FROM           106  '106'

Parse error at or near `<117>' instruction at offset 22