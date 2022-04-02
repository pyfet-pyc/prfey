# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\payload.py
import asyncio, enum, io, json, mimetypes, os, warnings
from abc import ABC, abstractmethod
from itertools import chain
from typing import IO, TYPE_CHECKING, Any, ByteString, Dict, Iterable, Optional, Text, TextIO, Tuple, Type, Union
from multidict import CIMultiDict
from . import hdrs
from .abc import AbstractStreamWriter
from .helpers import PY_36, content_disposition_header, guess_filename, parse_mimetype, sentinel
from .streams import StreamReader
from .typedefs import JSONEncoder, _CIMultiDict
__all__ = ('PAYLOAD_REGISTRY', 'get_payload', 'payload_type', 'Payload', 'BytesPayload',
           'StringPayload', 'IOBasePayload', 'BytesIOPayload', 'BufferedReaderPayload',
           'TextIOPayload', 'StringIOPayload', 'JsonPayload', 'AsyncIterablePayload')
TOO_LARGE_BYTES_BODY = 1048576
if TYPE_CHECKING:
    from typing import List
else:

    class LookupError(Exception):
        pass


    class Order(str, enum.Enum):
        normal = 'normal'
        try_first = 'try_first'
        try_last = 'try_last'


    def get_payload--- This code section failed: ---

 L.  73         0  LOAD_GLOBAL              PAYLOAD_REGISTRY
                2  LOAD_ATTR                get
                4  LOAD_FAST                'data'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


    def register_payload(factory: Type['Payload'], type: Any, *, order: Order=Order.normal) -> None:
        PAYLOAD_REGISTRY.register(factory, type, order=order)


    class payload_type:

        def __init__(self, type: Any, *, order: Order=Order.normal) -> None:
            self.type = type
            self.order = order

        def __call__(self, factory: Type['Payload']) -> Type['Payload']:
            register_payload(factory, (self.type), order=(self.order))
            return factory


    class PayloadRegistry:
        __doc__ = 'Payload registry.\n\n    note: we need zope.interface for more efficient adapter search\n    '

        def __init__(self) -> None:
            self._first = []
            self._normal = []
            self._last = []

        def get--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              Payload
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 107        10  LOAD_FAST                'data'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 108        14  LOAD_FAST                '_CHAIN'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _first
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _normal
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _last
               28  CALL_FUNCTION_3       3  ''
               30  GET_ITER         
             32_0  COME_FROM            48  '48'
               32  FOR_ITER             78  'to 78'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'factory'
               38  STORE_FAST               'type'

 L. 109        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'data'
               44  LOAD_FAST                'type'
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    32  'to 32'

 L. 110        50  LOAD_FAST                'factory'
               52  LOAD_FAST                'data'
               54  BUILD_LIST_1          1 
               56  LOAD_FAST                'args'
               58  CALL_FINALLY         61  'to 61'
               60  WITH_CLEANUP_FINISH
               62  BUILD_MAP_0           0 
               64  LOAD_FAST                'kwargs'
               66  <164>                 1  ''
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  ROT_TWO          
               72  POP_TOP          
               74  RETURN_VALUE     
               76  JUMP_BACK            32  'to 32'

 L. 112        78  LOAD_GLOBAL              LookupError
               80  CALL_FUNCTION_0       0  ''
               82  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FINALLY' instruction at offset 58

        def register--- This code section failed: ---

 L. 117         0  LOAD_FAST                'order'
                2  LOAD_GLOBAL              Order
                4  LOAD_ATTR                try_first
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 118        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _first
               14  LOAD_METHOD              append
               16  LOAD_FAST                'factory'
               18  LOAD_FAST                'type'
               20  BUILD_TUPLE_2         2 
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_FORWARD         98  'to 98'
             28_0  COME_FROM             8  '8'

 L. 119        28  LOAD_FAST                'order'
               30  LOAD_GLOBAL              Order
               32  LOAD_ATTR                normal
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    56  'to 56'

 L. 120        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _normal
               42  LOAD_METHOD              append
               44  LOAD_FAST                'factory'
               46  LOAD_FAST                'type'
               48  BUILD_TUPLE_2         2 
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
               54  JUMP_FORWARD         98  'to 98'
             56_0  COME_FROM            36  '36'

 L. 121        56  LOAD_FAST                'order'
               58  LOAD_GLOBAL              Order
               60  LOAD_ATTR                try_last
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L. 122        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _last
               70  LOAD_METHOD              append
               72  LOAD_FAST                'factory'
               74  LOAD_FAST                'type'
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         98  'to 98'
             84_0  COME_FROM            64  '64'

 L. 124        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Unsupported order '
               88  LOAD_FAST                'order'
               90  FORMAT_VALUE          2  '!r'
               92  BUILD_STRING_2        2 
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            82  '82'
             98_1  COME_FROM            54  '54'
             98_2  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1


    class Payload(ABC):
        _default_content_type = 'application/octet-stream'
        _size = None

        def __init__--- This code section failed: ---

 L. 143         0  LOAD_FAST                'encoding'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _encoding

 L. 144         6  LOAD_FAST                'filename'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _filename

 L. 145        12  LOAD_GLOBAL              CIMultiDict
               14  CALL_FUNCTION_0       0  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _headers

 L. 146        20  LOAD_FAST                'value'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _value

 L. 147        26  LOAD_FAST                'content_type'
               28  LOAD_GLOBAL              sentinel
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    56  'to 56'
               34  LOAD_FAST                'content_type'
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    56  'to 56'

 L. 148        42  LOAD_FAST                'content_type'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _headers
               48  LOAD_GLOBAL              hdrs
               50  LOAD_ATTR                CONTENT_TYPE
               52  STORE_SUBSCR     
               54  JUMP_FORWARD        124  'to 124'
             56_0  COME_FROM            40  '40'
             56_1  COME_FROM            32  '32'

 L. 149        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _filename
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE   110  'to 110'

 L. 150        66  LOAD_GLOBAL              mimetypes
               68  LOAD_METHOD              guess_type
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _filename
               74  CALL_METHOD_1         1  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  STORE_FAST               'content_type'

 L. 151        82  LOAD_FAST                'content_type'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L. 152        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _default_content_type
               94  STORE_FAST               'content_type'
             96_0  COME_FROM            88  '88'

 L. 153        96  LOAD_FAST                'content_type'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                _headers
              102  LOAD_GLOBAL              hdrs
              104  LOAD_ATTR                CONTENT_TYPE
              106  STORE_SUBSCR     
              108  JUMP_FORWARD        124  'to 124'
            110_0  COME_FROM            64  '64'

 L. 155       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _default_content_type
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _headers
              118  LOAD_GLOBAL              hdrs
              120  LOAD_ATTR                CONTENT_TYPE
              122  STORE_SUBSCR     
            124_0  COME_FROM           108  '108'
            124_1  COME_FROM            54  '54'

 L. 156       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _headers
              128  LOAD_METHOD              update
              130  LOAD_FAST                'headers'
              132  JUMP_IF_TRUE_OR_POP   136  'to 136'
              134  BUILD_MAP_0           0 
            136_0  COME_FROM           132  '132'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

Parse error at or near `<117>' instruction at offset 30

        @property
        def size(self) -> Optional[int]:
            """Size of the payload."""
            return self._size

        @property
        def filename(self) -> Optional[str]:
            """Filename of the payload."""
            return self._filename

        @property
        def headers(self) -> _CIMultiDict:
            """Custom item headers"""
            return self._headers

        @property
        def _binary_headers(self) -> bytes:
            return ''.join[k + ': ' + v + '\r\n' for k, v in self.headers.items()].encode'utf-8' + b'\r\n'

        @property
        def encoding(self) -> Optional[str]:
            """Payload encoding"""
            return self._encoding

        @property
        def content_type(self) -> str:
            """Content type"""
            return self._headers[hdrs.CONTENT_TYPE]

        def set_content_disposition--- This code section failed: ---

 L. 196         0  LOAD_GLOBAL              content_disposition_header

 L. 197         2  LOAD_FAST                'disptype'

 L. 196         4  BUILD_TUPLE_1         1 
                6  LOAD_STR                 'quote_fields'

 L. 197         8  LOAD_FAST                'quote_fields'

 L. 196        10  BUILD_MAP_1           1 

 L. 197        12  LOAD_FAST                'params'

 L. 196        14  <164>                 1  ''
               16  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _headers
               22  LOAD_GLOBAL              hdrs
               24  LOAD_ATTR                CONTENT_DISPOSITION
               26  STORE_SUBSCR     

Parse error at or near `<164>' instruction at offset 14

        @abstractmethod
        async def write(self, writer: AbstractStreamWriter) -> None:
            """Write payload.

        writer is an AbstractStreamWriter instance:
        """
            pass


    class BytesPayload(Payload):

        def __init__--- This code section failed: ---

 L. 210         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     34  'to 34'

 L. 211        16  LOAD_GLOBAL              TypeError

 L. 212        18  LOAD_STR                 'value argument must be byte-ish, not {!r}'
               20  LOAD_METHOD              format
               22  LOAD_GLOBAL              type
               24  LOAD_FAST                'value'
               26  CALL_FUNCTION_1       1  ''
               28  CALL_METHOD_1         1  ''

 L. 211        30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'

 L. 215        34  LOAD_STR                 'content_type'
               36  LOAD_FAST                'kwargs'
               38  <118>                 1  ''
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 216        42  LOAD_STR                 'application/octet-stream'
               44  LOAD_FAST                'kwargs'
               46  LOAD_STR                 'content_type'
               48  STORE_SUBSCR     
             50_0  COME_FROM            40  '40'

 L. 218        50  LOAD_GLOBAL              super
               52  CALL_FUNCTION_0       0  ''
               54  LOAD_ATTR                __init__
               56  LOAD_FAST                'value'
               58  BUILD_LIST_1          1 
               60  LOAD_FAST                'args'
               62  CALL_FINALLY         65  'to 65'
               64  WITH_CLEANUP_FINISH
               66  BUILD_MAP_0           0 
               68  LOAD_FAST                'kwargs'
               70  <164>                 1  ''
               72  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               74  POP_TOP          

 L. 220        76  LOAD_GLOBAL              isinstance
               78  LOAD_FAST                'value'
               80  LOAD_GLOBAL              memoryview
               82  CALL_FUNCTION_2       2  ''
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L. 221        86  LOAD_FAST                'value'
               88  LOAD_ATTR                nbytes
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _size
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM            84  '84'

 L. 223        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'value'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _size
            106_0  COME_FROM            94  '94'

 L. 225       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _size
              110  LOAD_GLOBAL              TOO_LARGE_BYTES_BODY
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   154  'to 154'

 L. 226       116  LOAD_GLOBAL              PY_36
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 227       120  LOAD_STR                 'source'
              122  LOAD_FAST                'self'
              124  BUILD_MAP_1           1 
              126  STORE_FAST               'kwargs'
              128  JUMP_FORWARD        134  'to 134'
            130_0  COME_FROM           118  '118'

 L. 229       130  BUILD_MAP_0           0 
              132  STORE_FAST               'kwargs'
            134_0  COME_FROM           128  '128'

 L. 230       134  LOAD_GLOBAL              warnings
              136  LOAD_ATTR                warn

 L. 231       138  LOAD_STR                 'Sending a large body directly with raw bytes might lock the event loop. You should probably pass an io.BytesIO object instead'

 L. 234       140  LOAD_GLOBAL              ResourceWarning

 L. 230       142  BUILD_TUPLE_2         2 
              144  BUILD_MAP_0           0 

 L. 235       146  LOAD_FAST                'kwargs'

 L. 230       148  <164>                 1  ''
              150  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              152  POP_TOP          
            154_0  COME_FROM           114  '114'

Parse error at or near `<118>' instruction at offset 38

        async def write(self, writer: AbstractStreamWriter) -> None:
            await writer.writeself._value


    class StringPayload(BytesPayload):

        def __init__--- This code section failed: ---

 L. 252         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    50  'to 50'

 L. 253         8  LOAD_FAST                'content_type'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 254        16  LOAD_STR                 'utf-8'
               18  STORE_FAST               'real_encoding'

 L. 255        20  LOAD_STR                 'text/plain; charset=utf-8'
               22  STORE_FAST               'content_type'
               24  JUMP_ABSOLUTE        70  'to 70'
             26_0  COME_FROM            14  '14'

 L. 257        26  LOAD_GLOBAL              parse_mimetype
               28  LOAD_FAST                'content_type'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'mimetype'

 L. 258        34  LOAD_FAST                'mimetype'
               36  LOAD_ATTR                parameters
               38  LOAD_METHOD              get
               40  LOAD_STR                 'charset'
               42  LOAD_STR                 'utf-8'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'real_encoding'
               48  JUMP_FORWARD         70  'to 70'
             50_0  COME_FROM             6  '6'

 L. 260        50  LOAD_FAST                'content_type'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 261        58  LOAD_STR                 'text/plain; charset=%s'
               60  LOAD_FAST                'encoding'
               62  BINARY_MODULO    
               64  STORE_FAST               'content_type'
             66_0  COME_FROM            56  '56'

 L. 262        66  LOAD_FAST                'encoding'
               68  STORE_FAST               'real_encoding'
             70_0  COME_FROM            48  '48'

 L. 264        70  LOAD_GLOBAL              super
               72  CALL_FUNCTION_0       0  ''
               74  LOAD_ATTR                __init__

 L. 265        76  LOAD_FAST                'value'
               78  LOAD_METHOD              encode
               80  LOAD_FAST                'real_encoding'
               82  CALL_METHOD_1         1  ''

 L. 264        84  BUILD_LIST_1          1 

 L. 268        86  LOAD_FAST                'args'

 L. 264        88  CALL_FINALLY         91  'to 91'
               90  WITH_CLEANUP_FINISH

 L. 266        92  LOAD_FAST                'real_encoding'

 L. 267        94  LOAD_FAST                'content_type'

 L. 264        96  LOAD_CONST               ('encoding', 'content_type')
               98  BUILD_CONST_KEY_MAP_2     2 

 L. 269       100  LOAD_FAST                'kwargs'

 L. 264       102  <164>                 1  ''
              104  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              106  POP_TOP          

Parse error at or near `None' instruction at offset -1


    class StringIOPayload(StringPayload):

        def __init__--- This code section failed: ---

 L. 275         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'value'
                8  LOAD_METHOD              read
               10  CALL_METHOD_0         0  ''
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_TOP          

Parse error at or near `None' instruction at offset -1


    class IOBasePayload(Payload):

        def __init__--- This code section failed: ---

 L. 282         0  LOAD_STR                 'filename'
                2  LOAD_FAST                'kwargs'
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 283         8  LOAD_GLOBAL              guess_filename
               10  LOAD_FAST                'value'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_FAST                'kwargs'
               16  LOAD_STR                 'filename'
               18  STORE_SUBSCR     
             20_0  COME_FROM             6  '6'

 L. 285        20  LOAD_GLOBAL              super
               22  CALL_FUNCTION_0       0  ''
               24  LOAD_ATTR                __init__
               26  LOAD_FAST                'value'
               28  BUILD_LIST_1          1 
               30  LOAD_FAST                'args'
               32  CALL_FINALLY         35  'to 35'
               34  WITH_CLEANUP_FINISH
               36  BUILD_MAP_0           0 
               38  LOAD_FAST                'kwargs'
               40  <164>                 1  ''
               42  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               44  POP_TOP          

 L. 287        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _filename
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    92  'to 92'
               56  LOAD_FAST                'disposition'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    92  'to 92'

 L. 288        64  LOAD_GLOBAL              hdrs
               66  LOAD_ATTR                CONTENT_DISPOSITION
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                headers
               72  <118>                 1  ''
               74  POP_JUMP_IF_FALSE    92  'to 92'

 L. 289        76  LOAD_FAST                'self'
               78  LOAD_ATTR                set_content_disposition
               80  LOAD_FAST                'disposition'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _filename
               86  LOAD_CONST               ('filename',)
               88  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               90  POP_TOP          
             92_0  COME_FROM            74  '74'
             92_1  COME_FROM            62  '62'
             92_2  COME_FROM            54  '54'

Parse error at or near `None' instruction at offset -1

        async def write--- This code section failed: ---

 L. 292         0  LOAD_GLOBAL              asyncio
                2  LOAD_METHOD              get_event_loop
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loop'

 L. 293         8  SETUP_FINALLY       106  'to 106'

 L. 294        10  LOAD_FAST                'loop'
               12  LOAD_METHOD              run_in_executor
               14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _value
               20  LOAD_ATTR                read
               22  LOAD_CONST               65536
               24  CALL_METHOD_3         3  ''
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  STORE_FAST               'chunk'

 L. 295        34  LOAD_FAST                'chunk'
               36  POP_JUMP_IF_FALSE    80  'to 80'

 L. 296        38  LOAD_FAST                'writer'
               40  LOAD_METHOD              write
               42  LOAD_FAST                'chunk'
               44  CALL_METHOD_1         1  ''
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  POP_TOP          

 L. 297        54  LOAD_FAST                'loop'
               56  LOAD_METHOD              run_in_executor
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _value
               64  LOAD_ATTR                read
               66  LOAD_CONST               65536
               68  CALL_METHOD_3         3  ''
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  STORE_FAST               'chunk'
               78  JUMP_BACK            34  'to 34'
             80_0  COME_FROM            36  '36'
               80  POP_BLOCK        

 L. 299        82  LOAD_FAST                'loop'
               84  LOAD_METHOD              run_in_executor
               86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _value
               92  LOAD_ATTR                close
               94  CALL_METHOD_2         2  ''
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  POP_TOP          
              104  JUMP_FORWARD        130  'to 130'
            106_0  COME_FROM_FINALLY     8  '8'
              106  LOAD_FAST                'loop'
              108  LOAD_METHOD              run_in_executor
              110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _value
              116  LOAD_ATTR                close
              118  CALL_METHOD_2         2  ''
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  POP_TOP          
              128  <48>             
            130_0  COME_FROM           104  '104'

Parse error at or near `LOAD_FAST' instruction at offset 82


    class TextIOPayload(IOBasePayload):

        def __init__--- This code section failed: ---

 L. 312         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    50  'to 50'

 L. 313         8  LOAD_FAST                'content_type'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 314        16  LOAD_STR                 'utf-8'
               18  STORE_FAST               'encoding'

 L. 315        20  LOAD_STR                 'text/plain; charset=utf-8'
               22  STORE_FAST               'content_type'
               24  JUMP_ABSOLUTE        66  'to 66'
             26_0  COME_FROM            14  '14'

 L. 317        26  LOAD_GLOBAL              parse_mimetype
               28  LOAD_FAST                'content_type'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'mimetype'

 L. 318        34  LOAD_FAST                'mimetype'
               36  LOAD_ATTR                parameters
               38  LOAD_METHOD              get
               40  LOAD_STR                 'charset'
               42  LOAD_STR                 'utf-8'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'encoding'
               48  JUMP_FORWARD         66  'to 66'
             50_0  COME_FROM             6  '6'

 L. 320        50  LOAD_FAST                'content_type'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 321        58  LOAD_STR                 'text/plain; charset=%s'
               60  LOAD_FAST                'encoding'
               62  BINARY_MODULO    
               64  STORE_FAST               'content_type'
             66_0  COME_FROM            56  '56'
             66_1  COME_FROM            48  '48'

 L. 323        66  LOAD_GLOBAL              super
               68  CALL_FUNCTION_0       0  ''
               70  LOAD_ATTR                __init__

 L. 324        72  LOAD_FAST                'value'

 L. 323        74  BUILD_LIST_1          1 

 L. 327        76  LOAD_FAST                'args'

 L. 323        78  CALL_FINALLY         81  'to 81'
               80  WITH_CLEANUP_FINISH

 L. 325        82  LOAD_FAST                'content_type'

 L. 326        84  LOAD_FAST                'encoding'

 L. 323        86  LOAD_CONST               ('content_type', 'encoding')
               88  BUILD_CONST_KEY_MAP_2     2 

 L. 328        90  LOAD_FAST                'kwargs'

 L. 323        92  <164>                 1  ''
               94  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               96  POP_TOP          

Parse error at or near `None' instruction at offset -1

        @property
        def size--- This code section failed: ---

 L. 333         0  SETUP_FINALLY        32  'to 32'

 L. 334         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              fstat
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _value
               10  LOAD_METHOD              fileno
               12  CALL_METHOD_0         0  ''
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                st_size
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _value
               22  LOAD_METHOD              tell
               24  CALL_METHOD_0         0  ''
               26  BINARY_SUBTRACT  
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 335        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  <121>                50  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 336        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
               50  <48>             

Parse error at or near `<121>' instruction at offset 36

        async def write--- This code section failed: ---

 L. 339         0  LOAD_GLOBAL              asyncio
                2  LOAD_METHOD              get_event_loop
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loop'

 L. 340         8  SETUP_FINALLY       114  'to 114'

 L. 341        10  LOAD_FAST                'loop'
               12  LOAD_METHOD              run_in_executor
               14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _value
               20  LOAD_ATTR                read
               22  LOAD_CONST               65536
               24  CALL_METHOD_3         3  ''
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  STORE_FAST               'chunk'

 L. 342        34  LOAD_FAST                'chunk'
               36  POP_JUMP_IF_FALSE    88  'to 88'

 L. 343        38  LOAD_FAST                'writer'
               40  LOAD_METHOD              write
               42  LOAD_FAST                'chunk'
               44  LOAD_METHOD              encode
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _encoding
               50  CALL_METHOD_1         1  ''
               52  CALL_METHOD_1         1  ''
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  POP_TOP          

 L. 344        62  LOAD_FAST                'loop'
               64  LOAD_METHOD              run_in_executor
               66  LOAD_CONST               None
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _value
               72  LOAD_ATTR                read
               74  LOAD_CONST               65536
               76  CALL_METHOD_3         3  ''
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  STORE_FAST               'chunk'
               86  JUMP_BACK            34  'to 34'
             88_0  COME_FROM            36  '36'
               88  POP_BLOCK        

 L. 346        90  LOAD_FAST                'loop'
               92  LOAD_METHOD              run_in_executor
               94  LOAD_CONST               None
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _value
              100  LOAD_ATTR                close
              102  CALL_METHOD_2         2  ''
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  POP_TOP          
              112  JUMP_FORWARD        138  'to 138'
            114_0  COME_FROM_FINALLY     8  '8'
              114  LOAD_FAST                'loop'
              116  LOAD_METHOD              run_in_executor
              118  LOAD_CONST               None
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _value
              124  LOAD_ATTR                close
              126  CALL_METHOD_2         2  ''
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  POP_TOP          
              136  <48>             
            138_0  COME_FROM           112  '112'

Parse error at or near `LOAD_FAST' instruction at offset 90


    class BytesIOPayload(IOBasePayload):

        @property
        def size(self) -> int:
            position = self._value.tell()
            end = self._value.seek(0, os.SEEK_END)
            self._value.seekposition
            return end - position


    class BufferedReaderPayload(IOBasePayload):

        @property
        def size--- This code section failed: ---

 L. 361         0  SETUP_FINALLY        32  'to 32'

 L. 362         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              fstat
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _value
               10  LOAD_METHOD              fileno
               12  CALL_METHOD_0         0  ''
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                st_size
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _value
               22  LOAD_METHOD              tell
               24  CALL_METHOD_0         0  ''
               26  BINARY_SUBTRACT  
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L. 363        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  <121>                50  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 366        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
               50  <48>             

Parse error at or near `<121>' instruction at offset 36


    class JsonPayload(BytesPayload):

        def __init__--- This code section failed: ---

 L. 380         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__

 L. 381         6  LOAD_FAST                'dumps'
                8  LOAD_FAST                'value'
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_METHOD              encode
               14  LOAD_FAST                'encoding'
               16  CALL_METHOD_1         1  ''

 L. 380        18  BUILD_LIST_1          1 

 L. 384        20  LOAD_FAST                'args'

 L. 380        22  CALL_FINALLY         25  'to 25'
               24  WITH_CLEANUP_FINISH

 L. 382        26  LOAD_FAST                'content_type'

 L. 383        28  LOAD_FAST                'encoding'

 L. 380        30  LOAD_CONST               ('content_type', 'encoding')
               32  BUILD_CONST_KEY_MAP_2     2 

 L. 385        34  LOAD_FAST                'kwargs'

 L. 380        36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 22


    if TYPE_CHECKING:
        from typing import AsyncIterable, AsyncIterator
        _AsyncIterator = AsyncIterator[bytes]
        _AsyncIterable = AsyncIterable[bytes]
    else:
        from collections.abc import AsyncIterable, AsyncIterator
    _AsyncIterator = AsyncIterator
    _AsyncIterable = AsyncIterable

class AsyncIterablePayload(Payload):
    _iter = None

    def __init__--- This code section failed: ---

 L. 406         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              AsyncIterable
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     28  'to 28'

 L. 407        10  LOAD_GLOBAL              TypeError

 L. 408        12  LOAD_STR                 'value argument must support collections.abc.AsyncIterablebe interface, got {!r}'
               14  LOAD_METHOD              format

 L. 410        16  LOAD_GLOBAL              type
               18  LOAD_FAST                'value'
               20  CALL_FUNCTION_1       1  ''

 L. 408        22  CALL_METHOD_1         1  ''

 L. 407        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM             8  '8'

 L. 413        28  LOAD_STR                 'content_type'
               30  LOAD_FAST                'kwargs'
               32  <118>                 1  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 414        36  LOAD_STR                 'application/octet-stream'
               38  LOAD_FAST                'kwargs'
               40  LOAD_STR                 'content_type'
               42  STORE_SUBSCR     
             44_0  COME_FROM            34  '34'

 L. 416        44  LOAD_GLOBAL              super
               46  CALL_FUNCTION_0       0  ''
               48  LOAD_ATTR                __init__
               50  LOAD_FAST                'value'
               52  BUILD_LIST_1          1 
               54  LOAD_FAST                'args'
               56  CALL_FINALLY         59  'to 59'
               58  WITH_CLEANUP_FINISH
               60  BUILD_MAP_0           0 
               62  LOAD_FAST                'kwargs'
               64  <164>                 1  ''
               66  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               68  POP_TOP          

 L. 418        70  LOAD_FAST                'value'
               72  LOAD_METHOD              __aiter__
               74  CALL_METHOD_0         0  ''
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _iter

Parse error at or near `<118>' instruction at offset 32

    async def write--- This code section failed: ---

 L. 421         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _iter
                4  POP_JUMP_IF_FALSE    70  'to 70'

 L. 422         6  SETUP_FINALLY        46  'to 46'

 L. 426         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _iter
               12  LOAD_METHOD              __anext__
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  STORE_FAST               'chunk'

 L. 427        24  LOAD_FAST                'writer'
               26  LOAD_METHOD              write
               28  LOAD_FAST                'chunk'
               30  CALL_METHOD_1         1  ''
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  POP_TOP          
               40  JUMP_BACK             8  'to 8'
               42  POP_BLOCK        
               44  JUMP_FORWARD         70  'to 70'
             46_0  COME_FROM_FINALLY     6  '6'

 L. 428        46  DUP_TOP          
               48  LOAD_GLOBAL              StopAsyncIteration
               50  <121>                68  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 429        58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _iter
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
               68  <48>             
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            44  '44'
             70_2  COME_FROM             4  '4'

Parse error at or near `<121>' instruction at offset 50


class StreamReaderPayload(AsyncIterablePayload):

    def __init__--- This code section failed: ---

 L. 434         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'value'
                8  LOAD_METHOD              iter_any
               10  CALL_METHOD_0         0  ''
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_TOP          

Parse error at or near `None' instruction at offset -1


PAYLOAD_REGISTRY = PayloadRegistry()
PAYLOAD_REGISTRY.register(BytesPayload, (bytes, bytearray, memoryview))
PAYLOAD_REGISTRY.register(StringPayload, str)
PAYLOAD_REGISTRY.register(StringIOPayload, io.StringIO)
PAYLOAD_REGISTRY.register(TextIOPayload, io.TextIOBase)
PAYLOAD_REGISTRY.register(BytesIOPayload, io.BytesIO)
PAYLOAD_REGISTRY.register(BufferedReaderPayload, (io.BufferedReader, io.BufferedRandom))
PAYLOAD_REGISTRY.register(IOBasePayload, io.IOBase)
PAYLOAD_REGISTRY.register(StreamReaderPayload, StreamReader)
PAYLOAD_REGISTRY.register(AsyncIterablePayload, AsyncIterable, order=(Order.try_last))