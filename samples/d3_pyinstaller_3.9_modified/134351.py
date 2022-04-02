# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_response.py
import asyncio, collections.abc, datetime, enum, json, math, time, warnings, zlib
from concurrent.futures import Executor
from email.utils import parsedate
from http.cookies import Morsel, SimpleCookie
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, MutableMapping, Optional, Tuple, Union, cast
from multidict import CIMultiDict, istr
from . import hdrs, payload
from .abc import AbstractStreamWriter
from .helpers import PY_38, HeadersMixin, rfc822_formatted_time, sentinel
from .http import RESPONSES, SERVER_SOFTWARE, HttpVersion10, HttpVersion11
from .payload import Payload
from .typedefs import JSONEncoder, LooseHeaders
__all__ = ('ContentCoding', 'StreamResponse', 'Response', 'json_response')
if TYPE_CHECKING:
    from .web_request import BaseRequest
    BaseClass = MutableMapping[(str, Any)]
else:
    BaseClass = collections.abc.MutableMapping
if not PY_38:
    Morsel._reserved['samesite'] = 'SameSite'

class ContentCoding(enum.Enum):
    deflate = 'deflate'
    gzip = 'gzip'
    identity = 'identity'


class StreamResponse(BaseClass, HeadersMixin):
    _length_check = True

    def __init__--- This code section failed: ---

 L.  78         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _body

 L.  79         6  LOAD_CONST               None
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _keep_alive

 L.  80        12  LOAD_CONST               False
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _chunked

 L.  81        18  LOAD_CONST               False
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _compression

 L.  82        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _compression_force

 L.  83        30  LOAD_GLOBAL              SimpleCookie
               32  CALL_FUNCTION_0       0  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _cookies

 L.  85        38  LOAD_CONST               None
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _req

 L.  86        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _payload_writer

 L.  87        50  LOAD_CONST               False
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _eof_sent

 L.  88        56  LOAD_CONST               0
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _body_length

 L.  89        62  BUILD_MAP_0           0 
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _state

 L.  91        68  LOAD_FAST                'headers'
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    88  'to 88'

 L.  92        76  LOAD_GLOBAL              CIMultiDict
               78  LOAD_FAST                'headers'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _headers
               86  JUMP_FORWARD         96  'to 96'
             88_0  COME_FROM            74  '74'

 L.  94        88  LOAD_GLOBAL              CIMultiDict
               90  CALL_FUNCTION_0       0  ''
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _headers
             96_0  COME_FROM            86  '86'

 L.  96        96  LOAD_FAST                'self'
               98  LOAD_METHOD              set_status
              100  LOAD_FAST                'status'
              102  LOAD_FAST                'reason'
              104  CALL_METHOD_2         2  ''
              106  POP_TOP          

Parse error at or near `<117>' instruction at offset 72

    @property
    def prepared--- This code section failed: ---

 L. 100         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload_writer
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def task(self) -> 'asyncio.Task[None]':
        return getattr(self._req, 'task', None)

    @property
    def status(self) -> int:
        return self._status

    @property
    def chunked(self) -> bool:
        return self._chunked

    @property
    def compression(self) -> bool:
        return self._compression

    @property
    def reason(self) -> str:
        return self._reason

    def set_status--- This code section failed: ---

 L. 128         0  LOAD_FAST                'self'
                2  LOAD_ATTR                prepared
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  <74>             

 L. 129         8  LOAD_STR                 'Cannot change the response status code after the headers have been sent'

 L. 128        10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 131        14  LOAD_GLOBAL              int
               16  LOAD_FAST                'status'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _status

 L. 132        24  LOAD_FAST                'reason'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    74  'to 74'

 L. 133        32  SETUP_FINALLY        52  'to 52'

 L. 134        34  LOAD_FAST                '_RESPONSES'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _status
               40  BINARY_SUBSCR    
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  STORE_FAST               'reason'
               48  POP_BLOCK        
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM_FINALLY    32  '32'

 L. 135        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  <121>                72  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 136        64  LOAD_STR                 ''
               66  STORE_FAST               'reason'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            50  '50'
             74_2  COME_FROM            30  '30'

 L. 137        74  LOAD_FAST                'reason'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _reason

Parse error at or near `None' instruction at offset -1

    @property
    def keep_alive(self) -> Optional[bool]:
        return self._keep_alive

    def force_close(self) -> None:
        self._keep_alive = False

    @property
    def body_length(self) -> int:
        return self._body_length

    @property
    def output_length--- This code section failed: ---

 L. 152         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn
                4  LOAD_STR                 'output_length is deprecated'
                6  LOAD_GLOBAL              DeprecationWarning
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 153        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _payload_writer
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'

 L. 154        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _payload_writer
               26  LOAD_ATTR                buffer_size
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 18

    def enable_chunked_encoding--- This code section failed: ---

 L. 158         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _chunked

 L. 160         6  LOAD_GLOBAL              hdrs
                8  LOAD_ATTR                CONTENT_LENGTH
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _headers
               14  <118>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 161        18  LOAD_GLOBAL              RuntimeError

 L. 162        20  LOAD_STR                 "You can't enable chunked encoding when a content length is set"

 L. 161        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 164        26  LOAD_FAST                'chunk_size'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 165        34  LOAD_GLOBAL              warnings
               36  LOAD_METHOD              warn
               38  LOAD_STR                 'Chunk size is deprecated #1615'
               40  LOAD_GLOBAL              DeprecationWarning
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          
             46_0  COME_FROM            32  '32'

Parse error at or near `<118>' instruction at offset 14

    def enable_compression--- This code section failed: ---

 L. 172         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'force'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              bool
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    42  'to 42'

 L. 173        12  LOAD_FAST                'force'
               14  POP_JUMP_IF_FALSE    22  'to 22'
               16  LOAD_GLOBAL              ContentCoding
               18  LOAD_ATTR                deflate
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM            14  '14'
               22  LOAD_GLOBAL              ContentCoding
               24  LOAD_ATTR                identity
             26_0  COME_FROM            20  '20'
               26  STORE_FAST               'force'

 L. 174        28  LOAD_GLOBAL              warnings
               30  LOAD_METHOD              warn

 L. 175        32  LOAD_STR                 'Using boolean for force is deprecated #3318'
               34  LOAD_GLOBAL              DeprecationWarning

 L. 174        36  CALL_METHOD_2         2  ''
               38  POP_TOP          
               40  JUMP_FORWARD         68  'to 68'
             42_0  COME_FROM            10  '10'

 L. 177        42  LOAD_FAST                'force'
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE    68  'to 68'

 L. 178        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'force'
               54  LOAD_GLOBAL              ContentCoding
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_TRUE     68  'to 68'
               60  <74>             

 L. 179        62  LOAD_STR                 'force should one of None, bool or ContentEncoding'

 L. 178        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'
             68_1  COME_FROM            48  '48'
             68_2  COME_FROM            40  '40'

 L. 182        68  LOAD_CONST               True
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _compression

 L. 183        74  LOAD_FAST                'force'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _compression_force

Parse error at or near `<117>' instruction at offset 46

    @property
    def headers(self) -> 'CIMultiDict[str]':
        return self._headers

    @property
    def cookies(self) -> 'SimpleCookie[str]':
        return self._cookies

    def set_cookie--- This code section failed: ---

 L. 213         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cookies
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'old'

 L. 214        12  LOAD_FAST                'old'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'
               20  LOAD_FAST                'old'
               22  LOAD_ATTR                coded_value
               24  LOAD_STR                 ''
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 216        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _cookies
               34  LOAD_METHOD              pop
               36  LOAD_FAST                'name'
               38  LOAD_CONST               None
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
             44_0  COME_FROM            28  '28'
             44_1  COME_FROM            18  '18'

 L. 218        44  LOAD_FAST                'value'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _cookies
               50  LOAD_FAST                'name'
               52  STORE_SUBSCR     

 L. 219        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _cookies
               58  LOAD_FAST                'name'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'c'

 L. 221        64  LOAD_FAST                'expires'
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L. 222        72  LOAD_FAST                'expires'
               74  LOAD_FAST                'c'
               76  LOAD_STR                 'expires'
               78  STORE_SUBSCR     
               80  JUMP_FORWARD        102  'to 102'
             82_0  COME_FROM            70  '70'

 L. 223        82  LOAD_FAST                'c'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'expires'
               88  CALL_METHOD_1         1  ''
               90  LOAD_STR                 'Thu, 01 Jan 1970 00:00:00 GMT'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L. 224        96  LOAD_FAST                'c'
               98  LOAD_STR                 'expires'
              100  DELETE_SUBSCR    
            102_0  COME_FROM            94  '94'
            102_1  COME_FROM            80  '80'

 L. 226       102  LOAD_FAST                'domain'
              104  LOAD_CONST               None
              106  <117>                 1  ''
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 227       110  LOAD_FAST                'domain'
              112  LOAD_FAST                'c'
              114  LOAD_STR                 'domain'
              116  STORE_SUBSCR     
            118_0  COME_FROM           108  '108'

 L. 229       118  LOAD_FAST                'max_age'
              120  LOAD_CONST               None
              122  <117>                 1  ''
              124  POP_JUMP_IF_FALSE   140  'to 140'

 L. 230       126  LOAD_GLOBAL              str
              128  LOAD_FAST                'max_age'
              130  CALL_FUNCTION_1       1  ''
              132  LOAD_FAST                'c'
              134  LOAD_STR                 'max-age'
              136  STORE_SUBSCR     
              138  JUMP_FORWARD        154  'to 154'
            140_0  COME_FROM           124  '124'

 L. 231       140  LOAD_STR                 'max-age'
              142  LOAD_FAST                'c'
              144  <118>                 0  ''
              146  POP_JUMP_IF_FALSE   154  'to 154'

 L. 232       148  LOAD_FAST                'c'
              150  LOAD_STR                 'max-age'
              152  DELETE_SUBSCR    
            154_0  COME_FROM           146  '146'
            154_1  COME_FROM           138  '138'

 L. 234       154  LOAD_FAST                'path'
              156  LOAD_FAST                'c'
              158  LOAD_STR                 'path'
              160  STORE_SUBSCR     

 L. 236       162  LOAD_FAST                'secure'
              164  LOAD_CONST               None
              166  <117>                 1  ''
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L. 237       170  LOAD_FAST                'secure'
              172  LOAD_FAST                'c'
              174  LOAD_STR                 'secure'
              176  STORE_SUBSCR     
            178_0  COME_FROM           168  '168'

 L. 238       178  LOAD_FAST                'httponly'
              180  LOAD_CONST               None
              182  <117>                 1  ''
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 239       186  LOAD_FAST                'httponly'
              188  LOAD_FAST                'c'
              190  LOAD_STR                 'httponly'
              192  STORE_SUBSCR     
            194_0  COME_FROM           184  '184'

 L. 240       194  LOAD_FAST                'version'
              196  LOAD_CONST               None
              198  <117>                 1  ''
              200  POP_JUMP_IF_FALSE   210  'to 210'

 L. 241       202  LOAD_FAST                'version'
              204  LOAD_FAST                'c'
              206  LOAD_STR                 'version'
              208  STORE_SUBSCR     
            210_0  COME_FROM           200  '200'

 L. 242       210  LOAD_FAST                'samesite'
              212  LOAD_CONST               None
              214  <117>                 1  ''
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 243       218  LOAD_FAST                'samesite'
              220  LOAD_FAST                'c'
              222  LOAD_STR                 'samesite'
              224  STORE_SUBSCR     
            226_0  COME_FROM           216  '216'

Parse error at or near `<117>' instruction at offset 16

    def del_cookie(self, name: str, *, domain: Optional[str]=None, path: str='/') -> None:
        """Delete cookie.

        Creates new empty expired cookie.
        """
        self._cookies.popnameNone
        self.set_cookie(name,
          '',
          max_age=0,
          expires='Thu, 01 Jan 1970 00:00:00 GMT',
          domain=domain,
          path=path)

    @property
    def content_length(self):
        return super.content_length

    @content_length.setter
    def content_length--- This code section failed: ---

 L. 270         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    48  'to 48'

 L. 271         8  LOAD_GLOBAL              int
               10  LOAD_FAST                'value'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'value'

 L. 272        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _chunked
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 273        22  LOAD_GLOBAL              RuntimeError

 L. 274        24  LOAD_STR                 "You can't set content length when chunked encoding is enable"

 L. 273        26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L. 276        30  LOAD_GLOBAL              str
               32  LOAD_FAST                'value'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _headers
               40  LOAD_GLOBAL              hdrs
               42  LOAD_ATTR                CONTENT_LENGTH
               44  STORE_SUBSCR     
               46  JUMP_FORWARD         64  'to 64'
             48_0  COME_FROM             6  '6'

 L. 278        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _headers
               52  LOAD_METHOD              pop
               54  LOAD_GLOBAL              hdrs
               56  LOAD_ATTR                CONTENT_LENGTH
               58  LOAD_CONST               None
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          
             64_0  COME_FROM            46  '46'

Parse error at or near `None' instruction at offset -1

    @property
    def content_type(self):
        return super.content_type

    @content_type.setter
    def content_type(self, value: str) -> None:
        self.content_type
        self._content_type = str(value)
        self._generate_content_type_header()

    @property
    def charset(self):
        return super.charset

    @charset.setter
    def charset--- This code section failed: ---

 L. 298         0  LOAD_FAST                'self'
                2  LOAD_ATTR                content_type
                4  STORE_FAST               'ctype'

 L. 299         6  LOAD_FAST                'ctype'
                8  LOAD_STR                 'application/octet-stream'
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 300        14  LOAD_GLOBAL              RuntimeError

 L. 301        16  LOAD_STR                 "Setting charset for application/octet-stream doesn't make sense, setup content_type first"

 L. 300        18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 304        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _content_dict
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 305        36  LOAD_FAST                'value'
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 306        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _content_dict
               48  LOAD_METHOD              pop
               50  LOAD_STR                 'charset'
               52  LOAD_CONST               None
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          
               58  JUMP_FORWARD         78  'to 78'
             60_0  COME_FROM            42  '42'

 L. 308        60  LOAD_GLOBAL              str
               62  LOAD_FAST                'value'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_METHOD              lower
               68  CALL_METHOD_0         0  ''
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _content_dict
               74  LOAD_STR                 'charset'
               76  STORE_SUBSCR     
             78_0  COME_FROM            58  '58'

 L. 309        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _generate_content_type_header
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

Parse error at or near `<117>' instruction at offset 28

    @property
    def last_modified--- This code section failed: ---

 L. 317         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _headers
                4  LOAD_METHOD              get
                6  LOAD_GLOBAL              hdrs
                8  LOAD_ATTR                LAST_MODIFIED
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'httpdate'

 L. 318        14  LOAD_FAST                'httpdate'
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    66  'to 66'

 L. 319        22  LOAD_GLOBAL              parsedate
               24  LOAD_FAST                'httpdate'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'timetuple'

 L. 320        30  LOAD_FAST                'timetuple'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    66  'to 66'

 L. 321        38  LOAD_GLOBAL              datetime
               40  LOAD_ATTR                datetime
               42  LOAD_FAST                'timetuple'
               44  LOAD_CONST               None
               46  LOAD_CONST               6
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  LOAD_STR                 'tzinfo'
               54  LOAD_GLOBAL              datetime
               56  LOAD_ATTR                timezone
               58  LOAD_ATTR                utc
               60  BUILD_MAP_1           1 
               62  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               64  RETURN_VALUE     
             66_0  COME_FROM            36  '36'
             66_1  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    @last_modified.setter
    def last_modified--- This code section failed: ---

 L. 328         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L. 329         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _headers
               12  LOAD_METHOD              pop
               14  LOAD_GLOBAL              hdrs
               16  LOAD_ATTR                LAST_MODIFIED
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
               24  JUMP_FORWARD        134  'to 134'
             26_0  COME_FROM             6  '6'

 L. 330        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'value'
               30  LOAD_GLOBAL              int
               32  LOAD_GLOBAL              float
               34  BUILD_TUPLE_2         2 
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    74  'to 74'

 L. 331        40  LOAD_GLOBAL              time
               42  LOAD_METHOD              strftime

 L. 332        44  LOAD_STR                 '%a, %d %b %Y %H:%M:%S GMT'
               46  LOAD_GLOBAL              time
               48  LOAD_METHOD              gmtime
               50  LOAD_GLOBAL              math
               52  LOAD_METHOD              ceil
               54  LOAD_FAST                'value'
               56  CALL_METHOD_1         1  ''
               58  CALL_METHOD_1         1  ''

 L. 331        60  CALL_METHOD_2         2  ''
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _headers
               66  LOAD_GLOBAL              hdrs
               68  LOAD_ATTR                LAST_MODIFIED
               70  STORE_SUBSCR     
               72  JUMP_FORWARD        134  'to 134'
             74_0  COME_FROM            38  '38'

 L. 334        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'value'
               78  LOAD_GLOBAL              datetime
               80  LOAD_ATTR                datetime
               82  CALL_FUNCTION_2       2  ''
               84  POP_JUMP_IF_FALSE   112  'to 112'

 L. 335        86  LOAD_GLOBAL              time
               88  LOAD_METHOD              strftime

 L. 336        90  LOAD_STR                 '%a, %d %b %Y %H:%M:%S GMT'
               92  LOAD_FAST                'value'
               94  LOAD_METHOD              utctimetuple
               96  CALL_METHOD_0         0  ''

 L. 335        98  CALL_METHOD_2         2  ''
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _headers
              104  LOAD_GLOBAL              hdrs
              106  LOAD_ATTR                LAST_MODIFIED
              108  STORE_SUBSCR     
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM            84  '84'

 L. 338       112  LOAD_GLOBAL              isinstance
              114  LOAD_FAST                'value'
              116  LOAD_GLOBAL              str
              118  CALL_FUNCTION_2       2  ''
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L. 339       122  LOAD_FAST                'value'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _headers
              128  LOAD_GLOBAL              hdrs
              130  LOAD_ATTR                LAST_MODIFIED
              132  STORE_SUBSCR     
            134_0  COME_FROM           120  '120'
            134_1  COME_FROM           110  '110'
            134_2  COME_FROM            72  '72'
            134_3  COME_FROM            24  '24'

Parse error at or near `None' instruction at offset -1

    def _generate_content_type_header--- This code section failed: ---

 L. 344         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _content_dict
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 345        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _content_type
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L. 346        28  LOAD_STR                 '; '
               30  LOAD_METHOD              join
               32  LOAD_GENEXPR             '<code_object <genexpr>>'
               34  LOAD_STR                 'StreamResponse._generate_content_type_header.<locals>.<genexpr>'
               36  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _content_dict
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  ''
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'params'

 L. 347        54  LOAD_FAST                'params'
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 348        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _content_type
               62  LOAD_STR                 '; '
               64  BINARY_ADD       
               66  LOAD_FAST                'params'
               68  BINARY_ADD       
               70  STORE_FAST               'ctype'
               72  JUMP_FORWARD         80  'to 80'
             74_0  COME_FROM            56  '56'

 L. 350        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _content_type
               78  STORE_FAST               'ctype'
             80_0  COME_FROM            72  '72'

 L. 351        80  LOAD_FAST                'ctype'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _headers
               86  LOAD_FAST                'CONTENT_TYPE'
               88  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    async def _do_start_compression--- This code section failed: ---

 L. 354         0  LOAD_FAST                'coding'
                2  LOAD_GLOBAL              ContentCoding
                4  LOAD_ATTR                identity
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_FALSE    68  'to 68'

 L. 355        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload_writer
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 356        24  LOAD_FAST                'coding'
               26  LOAD_ATTR                value
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _headers
               32  LOAD_GLOBAL              hdrs
               34  LOAD_ATTR                CONTENT_ENCODING
               36  STORE_SUBSCR     

 L. 357        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _payload_writer
               42  LOAD_METHOD              enable_compression
               44  LOAD_FAST                'coding'
               46  LOAD_ATTR                value
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 360        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _headers
               56  LOAD_METHOD              popall
               58  LOAD_GLOBAL              hdrs
               60  LOAD_ATTR                CONTENT_LENGTH
               62  LOAD_CONST               None
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
             68_0  COME_FROM             8  '8'

Parse error at or near `<117>' instruction at offset 16

    async def _start_compression--- This code section failed: ---

 L. 363         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _compression_force
                4  POP_JUMP_IF_FALSE    26  'to 26'

 L. 364         6  LOAD_FAST                'self'
                8  LOAD_METHOD              _do_start_compression
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _compression_force
               14  CALL_METHOD_1         1  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
               24  JUMP_FORWARD         88  'to 88'
             26_0  COME_FROM             4  '4'

 L. 366        26  LOAD_FAST                'request'
               28  LOAD_ATTR                headers
               30  LOAD_METHOD              get
               32  LOAD_GLOBAL              hdrs
               34  LOAD_ATTR                ACCEPT_ENCODING
               36  LOAD_STR                 ''
               38  CALL_METHOD_2         2  ''
               40  LOAD_METHOD              lower
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'accept_encoding'

 L. 367        46  LOAD_GLOBAL              ContentCoding
               48  GET_ITER         
             50_0  COME_FROM            86  '86'
             50_1  COME_FROM            62  '62'
               50  FOR_ITER             88  'to 88'
               52  STORE_FAST               'coding'

 L. 368        54  LOAD_FAST                'coding'
               56  LOAD_ATTR                value
               58  LOAD_FAST                'accept_encoding'
               60  <118>                 0  ''
               62  POP_JUMP_IF_FALSE_BACK    50  'to 50'

 L. 369        64  LOAD_FAST                'self'
               66  LOAD_METHOD              _do_start_compression
               68  LOAD_FAST                'coding'
               70  CALL_METHOD_1         1  ''
               72  GET_AWAITABLE    
               74  LOAD_CONST               None
               76  YIELD_FROM       
               78  POP_TOP          

 L. 370        80  POP_TOP          
               82  LOAD_CONST               None
               84  RETURN_VALUE     
               86  JUMP_BACK            50  'to 50'
             88_0  COME_FROM            50  '50'
             88_1  COME_FROM            24  '24'

Parse error at or near `<118>' instruction at offset 60

    async def prepare--- This code section failed: ---

 L. 373         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof_sent
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 374         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 375        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload_writer
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 376        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _payload_writer
               24  RETURN_VALUE     
             26_0  COME_FROM            18  '18'

 L. 378        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _start
               30  LOAD_FAST                'request'
               32  CALL_METHOD_1         1  ''
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    async def _start(self, request: 'BaseRequest') -> AbstractStreamWriter:
        self._req = request
        writer = self._payload_writer = request._payload_writer
        await self._prepare_headers()
        await request._prepare_hookself
        await self._write_headers()
        return writer

    async def _prepare_headers--- This code section failed: ---

 L. 391         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _req
                4  STORE_FAST               'request'

 L. 392         6  LOAD_FAST                'request'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 393        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _payload_writer
               22  STORE_FAST               'writer'

 L. 394        24  LOAD_FAST                'writer'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 395        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _keep_alive
               40  STORE_FAST               'keep_alive'

 L. 396        42  LOAD_FAST                'keep_alive'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    56  'to 56'

 L. 397        50  LOAD_FAST                'request'
               52  LOAD_ATTR                keep_alive
               54  STORE_FAST               'keep_alive'
             56_0  COME_FROM            48  '48'

 L. 398        56  LOAD_FAST                'keep_alive'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _keep_alive

 L. 400        62  LOAD_FAST                'request'
               64  LOAD_ATTR                version
               66  STORE_FAST               'version'

 L. 402        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _headers
               72  STORE_FAST               'headers'

 L. 403        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _cookies
               78  LOAD_METHOD              values
               80  CALL_METHOD_0         0  ''
               82  GET_ITER         
             84_0  COME_FROM           122  '122'
               84  FOR_ITER            124  'to 124'
               86  STORE_FAST               'cookie'

 L. 404        88  LOAD_FAST                'cookie'
               90  LOAD_ATTR                output
               92  LOAD_STR                 ''
               94  LOAD_CONST               ('header',)
               96  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               98  LOAD_CONST               1
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  STORE_FAST               'value'

 L. 405       108  LOAD_FAST                'headers'
              110  LOAD_METHOD              add
              112  LOAD_GLOBAL              hdrs
              114  LOAD_ATTR                SET_COOKIE
              116  LOAD_FAST                'value'
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          
              122  JUMP_BACK            84  'to 84'
            124_0  COME_FROM            84  '84'

 L. 407       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _compression
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L. 408       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _start_compression
              134  LOAD_FAST                'request'
              136  CALL_METHOD_1         1  ''
              138  GET_AWAITABLE    
              140  LOAD_CONST               None
              142  YIELD_FROM       
              144  POP_TOP          
            146_0  COME_FROM           128  '128'

 L. 410       146  LOAD_FAST                'self'
              148  LOAD_ATTR                _chunked
              150  POP_JUMP_IF_FALSE   214  'to 214'

 L. 411       152  LOAD_FAST                'version'
              154  LOAD_GLOBAL              HttpVersion11
              156  COMPARE_OP               !=
              158  POP_JUMP_IF_FALSE   176  'to 176'

 L. 412       160  LOAD_GLOBAL              RuntimeError

 L. 413       162  LOAD_STR                 'Using chunked encoding is forbidden for HTTP/{0.major}.{0.minor}'
              164  LOAD_METHOD              format

 L. 414       166  LOAD_FAST                'request'
              168  LOAD_ATTR                version

 L. 413       170  CALL_METHOD_1         1  ''

 L. 412       172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           158  '158'

 L. 416       176  LOAD_FAST                'writer'
              178  LOAD_METHOD              enable_chunking
              180  CALL_METHOD_0         0  ''
              182  POP_TOP          

 L. 417       184  LOAD_STR                 'chunked'
              186  LOAD_FAST                'headers'
              188  LOAD_GLOBAL              hdrs
              190  LOAD_ATTR                TRANSFER_ENCODING
              192  STORE_SUBSCR     

 L. 418       194  LOAD_GLOBAL              hdrs
              196  LOAD_ATTR                CONTENT_LENGTH
              198  LOAD_FAST                'headers'
              200  <118>                 0  ''
              202  POP_JUMP_IF_FALSE   212  'to 212'

 L. 419       204  LOAD_FAST                'headers'
              206  LOAD_GLOBAL              hdrs
              208  LOAD_ATTR                CONTENT_LENGTH
              210  DELETE_SUBSCR    
            212_0  COME_FROM           202  '202'
              212  JUMP_FORWARD        328  'to 328'
            214_0  COME_FROM           150  '150'

 L. 420       214  LOAD_FAST                'self'
              216  LOAD_ATTR                _length_check
          218_220  POP_JUMP_IF_FALSE   328  'to 328'

 L. 421       222  LOAD_FAST                'self'
              224  LOAD_ATTR                content_length
              226  LOAD_FAST                'writer'
              228  STORE_ATTR               length

 L. 422       230  LOAD_FAST                'writer'
              232  LOAD_ATTR                length
              234  LOAD_CONST               None
              236  <117>                 0  ''
          238_240  POP_JUMP_IF_FALSE   298  'to 298'

 L. 423       242  LOAD_FAST                'version'
              244  LOAD_GLOBAL              HttpVersion11
              246  COMPARE_OP               >=
          248_250  POP_JUMP_IF_FALSE   292  'to 292'

 L. 424       252  LOAD_FAST                'writer'
              254  LOAD_METHOD              enable_chunking
              256  CALL_METHOD_0         0  ''
              258  POP_TOP          

 L. 425       260  LOAD_STR                 'chunked'
              262  LOAD_FAST                'headers'
              264  LOAD_GLOBAL              hdrs
              266  LOAD_ATTR                TRANSFER_ENCODING
              268  STORE_SUBSCR     

 L. 426       270  LOAD_GLOBAL              hdrs
              272  LOAD_ATTR                CONTENT_LENGTH
              274  LOAD_FAST                'headers'
              276  <118>                 0  ''
          278_280  POP_JUMP_IF_FALSE   296  'to 296'

 L. 427       282  LOAD_FAST                'headers'
              284  LOAD_GLOBAL              hdrs
              286  LOAD_ATTR                CONTENT_LENGTH
              288  DELETE_SUBSCR    
              290  JUMP_FORWARD        296  'to 296'
            292_0  COME_FROM           248  '248'

 L. 429       292  LOAD_CONST               False
              294  STORE_FAST               'keep_alive'
            296_0  COME_FROM           290  '290'
            296_1  COME_FROM           278  '278'
              296  JUMP_FORWARD        328  'to 328'
            298_0  COME_FROM           238  '238'

 L. 432       298  LOAD_FAST                'version'
              300  LOAD_GLOBAL              HttpVersion11
              302  COMPARE_OP               >=
          304_306  POP_JUMP_IF_FALSE   328  'to 328'
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                status
              312  LOAD_CONST               (100, 101, 102, 103, 204)
              314  <118>                 0  ''
          316_318  POP_JUMP_IF_FALSE   328  'to 328'

 L. 433       320  LOAD_FAST                'headers'
              322  LOAD_GLOBAL              hdrs
              324  LOAD_ATTR                CONTENT_LENGTH
              326  DELETE_SUBSCR    
            328_0  COME_FROM           316  '316'
            328_1  COME_FROM           304  '304'
            328_2  COME_FROM           296  '296'
            328_3  COME_FROM           218  '218'
            328_4  COME_FROM           212  '212'

 L. 435       328  LOAD_FAST                'headers'
              330  LOAD_METHOD              setdefault
              332  LOAD_GLOBAL              hdrs
              334  LOAD_ATTR                CONTENT_TYPE
              336  LOAD_STR                 'application/octet-stream'
              338  CALL_METHOD_2         2  ''
              340  POP_TOP          

 L. 436       342  LOAD_FAST                'headers'
              344  LOAD_METHOD              setdefault
              346  LOAD_GLOBAL              hdrs
              348  LOAD_ATTR                DATE
              350  LOAD_GLOBAL              rfc822_formatted_time
              352  CALL_FUNCTION_0       0  ''
              354  CALL_METHOD_2         2  ''
              356  POP_TOP          

 L. 437       358  LOAD_FAST                'headers'
              360  LOAD_METHOD              setdefault
              362  LOAD_GLOBAL              hdrs
              364  LOAD_ATTR                SERVER
              366  LOAD_GLOBAL              SERVER_SOFTWARE
              368  CALL_METHOD_2         2  ''
              370  POP_TOP          

 L. 440       372  LOAD_GLOBAL              hdrs
              374  LOAD_ATTR                CONNECTION
              376  LOAD_FAST                'headers'
              378  <118>                 1  ''
          380_382  POP_JUMP_IF_FALSE   432  'to 432'

 L. 441       384  LOAD_FAST                'keep_alive'
          386_388  POP_JUMP_IF_FALSE   412  'to 412'

 L. 442       390  LOAD_FAST                'version'
              392  LOAD_GLOBAL              HttpVersion10
              394  COMPARE_OP               ==
          396_398  POP_JUMP_IF_FALSE   432  'to 432'

 L. 443       400  LOAD_STR                 'keep-alive'
              402  LOAD_FAST                'headers'
              404  LOAD_GLOBAL              hdrs
              406  LOAD_ATTR                CONNECTION
              408  STORE_SUBSCR     
              410  JUMP_FORWARD        432  'to 432'
            412_0  COME_FROM           386  '386'

 L. 445       412  LOAD_FAST                'version'
              414  LOAD_GLOBAL              HttpVersion11
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   432  'to 432'

 L. 446       422  LOAD_STR                 'close'
              424  LOAD_FAST                'headers'
              426  LOAD_GLOBAL              hdrs
              428  LOAD_ATTR                CONNECTION
              430  STORE_SUBSCR     
            432_0  COME_FROM           418  '418'
            432_1  COME_FROM           410  '410'
            432_2  COME_FROM           396  '396'
            432_3  COME_FROM           380  '380'

Parse error at or near `<117>' instruction at offset 10

    async def _write_headers--- This code section failed: ---

 L. 449         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _req
                4  STORE_FAST               'request'

 L. 450         6  LOAD_FAST                'request'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 451        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _payload_writer
               22  STORE_FAST               'writer'

 L. 452        24  LOAD_FAST                'writer'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 454        36  LOAD_FAST                'request'
               38  LOAD_ATTR                version
               40  STORE_FAST               'version'

 L. 455        42  LOAD_STR                 'HTTP/{}.{} {} {}'
               44  LOAD_METHOD              format

 L. 456        46  LOAD_FAST                'version'
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  LOAD_FAST                'version'
               54  LOAD_CONST               1
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _status
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _reason

 L. 455        66  CALL_METHOD_4         4  ''
               68  STORE_FAST               'status_line'

 L. 458        70  LOAD_FAST                'writer'
               72  LOAD_METHOD              write_headers
               74  LOAD_FAST                'status_line'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _headers
               80  CALL_METHOD_2         2  ''
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  POP_TOP          

Parse error at or near `<117>' instruction at offset 10

    async def write--- This code section failed: ---

 L. 461         0  LOAD_GLOBAL              isinstance

 L. 462         2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 

 L. 461        12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  <74>             

 L. 463        18  LOAD_STR                 'data argument must be byte-ish (%r)'
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  BINARY_MODULO    

 L. 461        28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            14  '14'

 L. 465        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _eof_sent
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 466        38  LOAD_GLOBAL              RuntimeError
               40  LOAD_STR                 'Cannot call write() after write_eof()'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 467        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _payload_writer
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L. 468        56  LOAD_GLOBAL              RuntimeError
               58  LOAD_STR                 'Cannot call write() before prepare()'
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 470        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _payload_writer
               68  LOAD_METHOD              write
               70  LOAD_FAST                'data'
               72  CALL_METHOD_1         1  ''
               74  GET_AWAITABLE    
               76  LOAD_CONST               None
               78  YIELD_FROM       
               80  POP_TOP          

Parse error at or near `<74>' instruction at offset 16

    async def drain--- This code section failed: ---

 L. 473         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof_sent
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  <74>             
                8  LOAD_STR                 'EOF has already been sent'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 474        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _payload_writer
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  <74>             
               26  LOAD_STR                 'Response has not been started'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 475        32  LOAD_GLOBAL              warnings
               34  LOAD_ATTR                warn

 L. 476        36  LOAD_STR                 'drain method is deprecated, use await resp.write()'

 L. 477        38  LOAD_GLOBAL              DeprecationWarning

 L. 478        40  LOAD_CONST               2

 L. 475        42  LOAD_CONST               ('stacklevel',)
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  POP_TOP          

 L. 480        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _payload_writer
               52  LOAD_METHOD              drain
               54  CALL_METHOD_0         0  ''
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  POP_TOP          

Parse error at or near `None' instruction at offset -1

    async def write_eof--- This code section failed: ---

 L. 483         0  LOAD_GLOBAL              isinstance

 L. 484         2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 

 L. 483        12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  <74>             

 L. 485        18  LOAD_STR                 'data argument must be byte-ish (%r)'
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'data'
               24  CALL_FUNCTION_1       1  ''
               26  BINARY_MODULO    

 L. 483        28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            14  '14'

 L. 487        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _eof_sent
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 488        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'

 L. 490        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _payload_writer
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_TRUE     60  'to 60'
               52  <74>             
               54  LOAD_STR                 'Response has not been started'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 492        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _payload_writer
               64  LOAD_METHOD              write_eof
               66  LOAD_FAST                'data'
               68  CALL_METHOD_1         1  ''
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  POP_TOP          

 L. 493        78  LOAD_CONST               True
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _eof_sent

 L. 494        84  LOAD_CONST               None
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _req

 L. 495        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _payload_writer
               94  LOAD_ATTR                output_size
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _body_length

 L. 496       100  LOAD_CONST               None
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _payload_writer

Parse error at or near `<74>' instruction at offset 16

    def __repr__--- This code section failed: ---

 L. 499         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof_sent
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 500         6  LOAD_STR                 'eof'
                8  STORE_FAST               'info'
               10  JUMP_FORWARD         62  'to 62'
             12_0  COME_FROM             4  '4'

 L. 501        12  LOAD_FAST                'self'
               14  LOAD_ATTR                prepared
               16  POP_JUMP_IF_FALSE    58  'to 58'

 L. 502        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _req
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_TRUE     32  'to 32'
               28  <74>             
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'

 L. 503        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _req
               36  LOAD_ATTR                method
               38  FORMAT_VALUE          0  ''
               40  LOAD_STR                 ' '
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _req
               46  LOAD_ATTR                path
               48  FORMAT_VALUE          0  ''
               50  LOAD_STR                 ' '
               52  BUILD_STRING_4        4 
               54  STORE_FAST               'info'
               56  JUMP_FORWARD         62  'to 62'
             58_0  COME_FROM            16  '16'

 L. 505        58  LOAD_STR                 'not prepared'
               60  STORE_FAST               'info'
             62_0  COME_FROM            56  '56'
             62_1  COME_FROM            10  '10'

 L. 506        62  LOAD_STR                 '<'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                __class__
               68  LOAD_ATTR                __name__
               70  FORMAT_VALUE          0  ''
               72  LOAD_STR                 ' '
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                reason
               78  FORMAT_VALUE          0  ''
               80  LOAD_STR                 ' '
               82  LOAD_FAST                'info'
               84  FORMAT_VALUE          0  ''
               86  LOAD_STR                 '>'
               88  BUILD_STRING_7        7 
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def __getitem__(self, key: str) -> Any:
        return self._state[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._state[key] = value

    def __delitem__(self, key: str) -> None:
        del self._state[key]

    def __len__(self) -> int:
        return len(self._state)

    def __iter__(self) -> Iterator[str]:
        return iter(self._state)

    def __hash__(self) -> int:
        return hash(id(self))

    def __eq__--- This code section failed: ---

 L. 527         0  LOAD_FAST                'self'
                2  LOAD_FAST                'other'
                4  <117>                 0  ''
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class Response(StreamResponse):

    def __init__--- This code section failed: ---

 L. 544         0  LOAD_FAST                'body'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_FAST                'text'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 545        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'body and text are not allowed together'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 547        24  LOAD_FAST                'headers'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 548        32  LOAD_GLOBAL              CIMultiDict
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'real_headers'
               38  JUMP_FORWARD         64  'to 64'
             40_0  COME_FROM            30  '30'

 L. 549        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'headers'
               44  LOAD_GLOBAL              CIMultiDict
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_TRUE     60  'to 60'

 L. 550        50  LOAD_GLOBAL              CIMultiDict
               52  LOAD_FAST                'headers'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'real_headers'
               58  JUMP_FORWARD         64  'to 64'
             60_0  COME_FROM            48  '48'

 L. 552        60  LOAD_FAST                'headers'
               62  STORE_FAST               'real_headers'
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            38  '38'

 L. 554        64  LOAD_FAST                'content_type'
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    88  'to 88'
               72  LOAD_STR                 'charset'
               74  LOAD_FAST                'content_type'
               76  <118>                 0  ''
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L. 555        80  LOAD_GLOBAL              ValueError
               82  LOAD_STR                 'charset must not be in content_type argument'
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'
             88_1  COME_FROM            70  '70'

 L. 557        88  LOAD_FAST                'text'
               90  LOAD_CONST               None
               92  <117>                 1  ''
               94  POP_JUMP_IF_FALSE   208  'to 208'

 L. 558        96  LOAD_GLOBAL              hdrs
               98  LOAD_ATTR                CONTENT_TYPE
              100  LOAD_FAST                'real_headers'
              102  <118>                 0  ''
              104  POP_JUMP_IF_FALSE   124  'to 124'

 L. 559       106  LOAD_FAST                'content_type'
              108  POP_JUMP_IF_TRUE    114  'to 114'
              110  LOAD_FAST                'charset'
              112  POP_JUMP_IF_FALSE   206  'to 206'
            114_0  COME_FROM           108  '108'

 L. 560       114  LOAD_GLOBAL              ValueError

 L. 561       116  LOAD_STR                 'passing both Content-Type header and content_type or charset params is forbidden'

 L. 560       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  JUMP_FORWARD        206  'to 206'
            124_0  COME_FROM           104  '104'

 L. 567       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'text'
              128  LOAD_GLOBAL              str
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_TRUE    150  'to 150'

 L. 568       134  LOAD_GLOBAL              TypeError
              136  LOAD_STR                 'text argument must be str (%r)'
              138  LOAD_GLOBAL              type
              140  LOAD_FAST                'text'
              142  CALL_FUNCTION_1       1  ''
              144  BINARY_MODULO    
              146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           132  '132'

 L. 569       150  LOAD_FAST                'content_type'
              152  LOAD_CONST               None
              154  <117>                 0  ''
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 570       158  LOAD_STR                 'text/plain'
              160  STORE_FAST               'content_type'
            162_0  COME_FROM           156  '156'

 L. 571       162  LOAD_FAST                'charset'
              164  LOAD_CONST               None
              166  <117>                 0  ''
              168  POP_JUMP_IF_FALSE   174  'to 174'

 L. 572       170  LOAD_STR                 'utf-8'
              172  STORE_FAST               'charset'
            174_0  COME_FROM           168  '168'

 L. 573       174  LOAD_FAST                'content_type'
              176  LOAD_STR                 '; charset='
              178  BINARY_ADD       
              180  LOAD_FAST                'charset'
              182  BINARY_ADD       
              184  LOAD_FAST                'real_headers'
              186  LOAD_GLOBAL              hdrs
              188  LOAD_ATTR                CONTENT_TYPE
              190  STORE_SUBSCR     

 L. 574       192  LOAD_FAST                'text'
              194  LOAD_METHOD              encode
              196  LOAD_FAST                'charset'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'body'

 L. 575       202  LOAD_CONST               None
              204  STORE_FAST               'text'
            206_0  COME_FROM           122  '122'
            206_1  COME_FROM           112  '112'
              206  JUMP_FORWARD        286  'to 286'
            208_0  COME_FROM            94  '94'

 L. 577       208  LOAD_GLOBAL              hdrs
              210  LOAD_ATTR                CONTENT_TYPE
              212  LOAD_FAST                'real_headers'
              214  <118>                 0  ''
              216  POP_JUMP_IF_FALSE   244  'to 244'

 L. 578       218  LOAD_FAST                'content_type'
              220  LOAD_CONST               None
              222  <117>                 1  ''
              224  POP_JUMP_IF_TRUE    234  'to 234'
              226  LOAD_FAST                'charset'
              228  LOAD_CONST               None
              230  <117>                 1  ''
              232  POP_JUMP_IF_FALSE   242  'to 242'
            234_0  COME_FROM           224  '224'

 L. 579       234  LOAD_GLOBAL              ValueError

 L. 580       236  LOAD_STR                 'passing both Content-Type header and content_type or charset params is forbidden'

 L. 579       238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           232  '232'
              242  JUMP_FORWARD        286  'to 286'
            244_0  COME_FROM           216  '216'

 L. 585       244  LOAD_FAST                'content_type'
              246  LOAD_CONST               None
              248  <117>                 1  ''
          250_252  POP_JUMP_IF_FALSE   286  'to 286'

 L. 586       254  LOAD_FAST                'charset'
              256  LOAD_CONST               None
              258  <117>                 1  ''
          260_262  POP_JUMP_IF_FALSE   276  'to 276'

 L. 587       264  LOAD_FAST                'content_type'
              266  LOAD_STR                 '; charset='
              268  LOAD_FAST                'charset'
              270  BINARY_ADD       
              272  INPLACE_ADD      
              274  STORE_FAST               'content_type'
            276_0  COME_FROM           260  '260'

 L. 588       276  LOAD_FAST                'content_type'
              278  LOAD_FAST                'real_headers'
              280  LOAD_GLOBAL              hdrs
              282  LOAD_ATTR                CONTENT_TYPE
              284  STORE_SUBSCR     
            286_0  COME_FROM           250  '250'
            286_1  COME_FROM           242  '242'
            286_2  COME_FROM           206  '206'

 L. 590       286  LOAD_GLOBAL              super
              288  CALL_FUNCTION_0       0  ''
              290  LOAD_ATTR                __init__
              292  LOAD_FAST                'status'
              294  LOAD_FAST                'reason'
              296  LOAD_FAST                'real_headers'
              298  LOAD_CONST               ('status', 'reason', 'headers')
              300  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              302  POP_TOP          

 L. 592       304  LOAD_FAST                'text'
              306  LOAD_CONST               None
              308  <117>                 1  ''
          310_312  POP_JUMP_IF_FALSE   322  'to 322'

 L. 593       314  LOAD_FAST                'text'
              316  LOAD_FAST                'self'
              318  STORE_ATTR               text
              320  JUMP_FORWARD        328  'to 328'
            322_0  COME_FROM           310  '310'

 L. 595       322  LOAD_FAST                'body'
              324  LOAD_FAST                'self'
              326  STORE_ATTR               body
            328_0  COME_FROM           320  '320'

 L. 597       328  LOAD_CONST               None
              330  LOAD_FAST                'self'
              332  STORE_ATTR               _compressed_body

 L. 598       334  LOAD_FAST                'zlib_executor_size'
              336  LOAD_FAST                'self'
              338  STORE_ATTR               _zlib_executor_size

 L. 599       340  LOAD_FAST                'zlib_executor'
              342  LOAD_FAST                'self'
              344  STORE_ATTR               _zlib_executor

Parse error at or near `None' instruction at offset -1

    @property
    def body(self) -> Optional[Union[(bytes, Payload)]]:
        return self._body

    @body.setter
    def body--- This code section failed: ---

 L. 612         0  LOAD_FAST                'body'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 613         8  LOAD_CONST               None
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _body

 L. 614        14  LOAD_CONST               False
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _body_payload
               20  JUMP_FORWARD        222  'to 222'
             22_0  COME_FROM             6  '6'

 L. 615        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'body'
               26  LOAD_GLOBAL              bytes
               28  LOAD_GLOBAL              bytearray
               30  BUILD_TUPLE_2         2 
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L. 616        36  LOAD_FAST                'body'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _body

 L. 617        42  LOAD_CONST               False
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _body_payload
               48  JUMP_FORWARD        222  'to 222'
             50_0  COME_FROM            34  '34'

 L. 619        50  SETUP_FINALLY        74  'to 74'

 L. 620        52  LOAD_GLOBAL              payload
               54  LOAD_ATTR                PAYLOAD_REGISTRY
               56  LOAD_METHOD              get
               58  LOAD_FAST                'body'
               60  CALL_METHOD_1         1  ''
               62  DUP_TOP          
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _body
               68  STORE_FAST               'body'
               70  POP_BLOCK        
               72  JUMP_FORWARD        110  'to 110'
             74_0  COME_FROM_FINALLY    50  '50'

 L. 621        74  DUP_TOP          
               76  LOAD_GLOBAL              payload
               78  LOAD_ATTR                LookupError
               80  <121>               108  ''
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 622        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'Unsupported body type %r'
               92  LOAD_GLOBAL              type
               94  LOAD_FAST                'body'
               96  CALL_FUNCTION_1       1  ''
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
              108  <48>             
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            72  '72'

 L. 624       110  LOAD_CONST               True
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _body_payload

 L. 626       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _headers
              120  STORE_FAST               'headers'

 L. 629       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _chunked
              126  POP_JUMP_IF_TRUE    162  'to 162'
              128  LOAD_FAST                'CONTENT_LENGTH'
              130  LOAD_FAST                'headers'
              132  <118>                 1  ''
              134  POP_JUMP_IF_FALSE   162  'to 162'

 L. 630       136  LOAD_FAST                'body'
              138  LOAD_ATTR                size
              140  STORE_FAST               'size'

 L. 631       142  LOAD_FAST                'size'
              144  LOAD_CONST               None
              146  <117>                 1  ''
              148  POP_JUMP_IF_FALSE   162  'to 162'

 L. 632       150  LOAD_GLOBAL              str
              152  LOAD_FAST                'size'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_FAST                'headers'
              158  LOAD_FAST                'CONTENT_LENGTH'
              160  STORE_SUBSCR     
            162_0  COME_FROM           148  '148'
            162_1  COME_FROM           134  '134'
            162_2  COME_FROM           126  '126'

 L. 635       162  LOAD_FAST                'CONTENT_TYPE'
              164  LOAD_FAST                'headers'
              166  <118>                 1  ''
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L. 636       170  LOAD_FAST                'body'
              172  LOAD_ATTR                content_type
              174  LOAD_FAST                'headers'
              176  LOAD_FAST                'CONTENT_TYPE'
              178  STORE_SUBSCR     
            180_0  COME_FROM           168  '168'

 L. 639       180  LOAD_FAST                'body'
              182  LOAD_ATTR                headers
              184  POP_JUMP_IF_FALSE   222  'to 222'

 L. 640       186  LOAD_FAST                'body'
              188  LOAD_ATTR                headers
              190  LOAD_METHOD              items
              192  CALL_METHOD_0         0  ''
              194  GET_ITER         
            196_0  COME_FROM           220  '220'
            196_1  COME_FROM           210  '210'
              196  FOR_ITER            222  'to 222'
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'key'
              202  STORE_FAST               'value'

 L. 641       204  LOAD_FAST                'key'
              206  LOAD_FAST                'headers'
              208  <118>                 1  ''
              210  POP_JUMP_IF_FALSE_BACK   196  'to 196'

 L. 642       212  LOAD_FAST                'value'
              214  LOAD_FAST                'headers'
              216  LOAD_FAST                'key'
              218  STORE_SUBSCR     
              220  JUMP_BACK           196  'to 196'
            222_0  COME_FROM           196  '196'
            222_1  COME_FROM           184  '184'
            222_2  COME_FROM            48  '48'
            222_3  COME_FROM            20  '20'

 L. 644       222  LOAD_CONST               None
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _compressed_body

Parse error at or near `None' instruction at offset -1

    @property
    def text--- This code section failed: ---

 L. 648         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _body
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 649        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 650        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _body
               18  LOAD_METHOD              decode
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                charset
               24  JUMP_IF_TRUE_OR_POP    28  'to 28'
               26  LOAD_STR                 'utf-8'
             28_0  COME_FROM            24  '24'
               28  CALL_METHOD_1         1  ''
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @text.setter
    def text--- This code section failed: ---

 L. 654         0  LOAD_FAST                'text'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     34  'to 34'
                8  LOAD_GLOBAL              isinstance

 L. 655        10  LOAD_FAST                'text'
               12  LOAD_GLOBAL              str

 L. 654        14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     34  'to 34'
               18  <74>             

 L. 656        20  LOAD_STR                 'text argument must be str (%r)'
               22  LOAD_GLOBAL              type
               24  LOAD_FAST                'text'
               26  CALL_FUNCTION_1       1  ''
               28  BINARY_MODULO    

 L. 654        30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            16  '16'
             34_1  COME_FROM             6  '6'

 L. 658        34  LOAD_FAST                'self'
               36  LOAD_ATTR                content_type
               38  LOAD_STR                 'application/octet-stream'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L. 659        44  LOAD_STR                 'text/plain'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               content_type
             50_0  COME_FROM            42  '42'

 L. 660        50  LOAD_FAST                'self'
               52  LOAD_ATTR                charset
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 661        60  LOAD_STR                 'utf-8'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               charset
             66_0  COME_FROM            58  '58'

 L. 663        66  LOAD_FAST                'text'
               68  LOAD_METHOD              encode
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                charset
               74  CALL_METHOD_1         1  ''
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _body

 L. 664        80  LOAD_CONST               False
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _body_payload

 L. 665        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _compressed_body

Parse error at or near `None' instruction at offset -1

    @property
    def content_length--- This code section failed: ---

 L. 669         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _chunked
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 670         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 672        10  LOAD_GLOBAL              hdrs
               12  LOAD_ATTR                CONTENT_LENGTH
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _headers
               18  <118>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 673        22  LOAD_GLOBAL              super
               24  CALL_FUNCTION_0       0  ''
               26  LOAD_ATTR                content_length
               28  RETURN_VALUE     
             30_0  COME_FROM            20  '20'

 L. 675        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _compressed_body
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    50  'to 50'

 L. 677        40  LOAD_GLOBAL              len
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _compressed_body
               46  CALL_FUNCTION_1       1  ''
               48  RETURN_VALUE     
             50_0  COME_FROM            38  '38'

 L. 678        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _body_payload
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 680        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 681        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _body
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 682        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _body
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            68  '68'

 L. 684        80  LOAD_CONST               0
               82  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 18

    @content_length.setter
    def content_length(self, value: Optional[int]) -> None:
        raise RuntimeError('Content length is set automatically')

    async def write_eof--- This code section failed: ---

 L. 691         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _eof_sent
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 692         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 693        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _compressed_body
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 694        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _body
               24  STORE_FAST               'body'
               26  JUMP_FORWARD         34  'to 34'
             28_0  COME_FROM            18  '18'

 L. 696        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _compressed_body
               32  STORE_FAST               'body'
             34_0  COME_FROM            26  '26'

 L. 697        34  LOAD_FAST                'data'
               36  POP_JUMP_IF_FALSE    52  'to 52'
               38  <74>             
               40  LOAD_STR                 'data arg is not supported, got '
               42  LOAD_FAST                'data'
               44  FORMAT_VALUE          2  '!r'
               46  BUILD_STRING_2        2 
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            36  '36'

 L. 698        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _req
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L. 699        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _payload_writer
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_TRUE     80  'to 80'
               76  <74>             
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            74  '74'

 L. 700        80  LOAD_FAST                'body'
               82  LOAD_CONST               None
               84  <117>                 1  ''
               86  POP_JUMP_IF_FALSE   208  'to 208'

 L. 701        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _req
               92  LOAD_ATTR                _method
               94  LOAD_GLOBAL              hdrs
               96  LOAD_ATTR                METH_HEAD
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    112  'to 112'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _status
              106  LOAD_CONST               (204, 304)
              108  <118>                 0  ''
              110  POP_JUMP_IF_FALSE   130  'to 130'
            112_0  COME_FROM           100  '100'

 L. 702       112  LOAD_GLOBAL              super
              114  CALL_FUNCTION_0       0  ''
              116  LOAD_METHOD              write_eof
              118  CALL_METHOD_0         0  ''
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  POP_TOP          
              128  JUMP_FORWARD        224  'to 224'
            130_0  COME_FROM           110  '110'

 L. 703       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _body_payload
              134  POP_JUMP_IF_FALSE   182  'to 182'

 L. 704       136  LOAD_GLOBAL              cast
              138  LOAD_GLOBAL              Payload
              140  LOAD_FAST                'body'
              142  CALL_FUNCTION_2       2  ''
              144  STORE_FAST               'payload'

 L. 705       146  LOAD_FAST                'payload'
              148  LOAD_METHOD              write
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _payload_writer
              154  CALL_METHOD_1         1  ''
              156  GET_AWAITABLE    
              158  LOAD_CONST               None
              160  YIELD_FROM       
              162  POP_TOP          

 L. 706       164  LOAD_GLOBAL              super
              166  CALL_FUNCTION_0       0  ''
              168  LOAD_METHOD              write_eof
              170  CALL_METHOD_0         0  ''
              172  GET_AWAITABLE    
              174  LOAD_CONST               None
              176  YIELD_FROM       
              178  POP_TOP          
              180  JUMP_FORWARD        224  'to 224'
            182_0  COME_FROM           134  '134'

 L. 708       182  LOAD_GLOBAL              super
              184  CALL_FUNCTION_0       0  ''
              186  LOAD_METHOD              write_eof
              188  LOAD_GLOBAL              cast
              190  LOAD_GLOBAL              bytes
              192  LOAD_FAST                'body'
              194  CALL_FUNCTION_2       2  ''
              196  CALL_METHOD_1         1  ''
              198  GET_AWAITABLE    
              200  LOAD_CONST               None
              202  YIELD_FROM       
              204  POP_TOP          
              206  JUMP_FORWARD        224  'to 224'
            208_0  COME_FROM            86  '86'

 L. 710       208  LOAD_GLOBAL              super
              210  CALL_FUNCTION_0       0  ''
              212  LOAD_METHOD              write_eof
              214  CALL_METHOD_0         0  ''
              216  GET_AWAITABLE    
              218  LOAD_CONST               None
              220  YIELD_FROM       
              222  POP_TOP          
            224_0  COME_FROM           206  '206'
            224_1  COME_FROM           180  '180'
            224_2  COME_FROM           128  '128'

Parse error at or near `<117>' instruction at offset 16

    async def _start--- This code section failed: ---

 L. 713         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _chunked
                4  POP_JUMP_IF_TRUE     70  'to 70'
                6  LOAD_GLOBAL              hdrs
                8  LOAD_ATTR                CONTENT_LENGTH
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _headers
               14  <118>                 1  ''
               16  POP_JUMP_IF_FALSE    70  'to 70'

 L. 714        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _body_payload
               22  POP_JUMP_IF_TRUE     70  'to 70'

 L. 715        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _body
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    58  'to 58'

 L. 716        34  LOAD_GLOBAL              str
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _body
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _headers
               50  LOAD_GLOBAL              hdrs
               52  LOAD_ATTR                CONTENT_LENGTH
               54  STORE_SUBSCR     
               56  JUMP_FORWARD         70  'to 70'
             58_0  COME_FROM            32  '32'

 L. 718        58  LOAD_STR                 '0'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _headers
               64  LOAD_GLOBAL              hdrs
               66  LOAD_ATTR                CONTENT_LENGTH
               68  STORE_SUBSCR     
             70_0  COME_FROM            56  '56'
             70_1  COME_FROM            22  '22'
             70_2  COME_FROM            16  '16'
             70_3  COME_FROM             4  '4'

 L. 720        70  LOAD_GLOBAL              super
               72  CALL_FUNCTION_0       0  ''
               74  LOAD_METHOD              _start
               76  LOAD_FAST                'request'
               78  CALL_METHOD_1         1  ''
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _compress_body--- This code section failed: ---

 L. 723         0  LOAD_FAST                'zlib_mode'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 724        12  LOAD_GLOBAL              zlib
               14  LOAD_ATTR                compressobj
               16  LOAD_FAST                'zlib_mode'
               18  LOAD_CONST               ('wbits',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  STORE_FAST               'compressobj'

 L. 725        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _body
               28  STORE_FAST               'body_in'

 L. 726        30  LOAD_FAST                'body_in'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L. 727        42  LOAD_FAST                'compressobj'
               44  LOAD_METHOD              compress
               46  LOAD_FAST                'body_in'
               48  CALL_METHOD_1         1  ''
               50  LOAD_FAST                'compressobj'
               52  LOAD_METHOD              flush
               54  CALL_METHOD_0         0  ''
               56  BINARY_ADD       
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _compressed_body

Parse error at or near `None' instruction at offset -1

    async def _do_start_compression--- This code section failed: ---

 L. 730         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _body_payload
                4  POP_JUMP_IF_TRUE     12  'to 12'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _chunked
               10  POP_JUMP_IF_FALSE    30  'to 30'
             12_0  COME_FROM             4  '4'

 L. 731        12  LOAD_GLOBAL              super
               14  CALL_FUNCTION_0       0  ''
               16  LOAD_METHOD              _do_start_compression
               18  LOAD_FAST                'coding'
               20  CALL_METHOD_1         1  ''
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  RETURN_VALUE     
             30_0  COME_FROM            10  '10'

 L. 733        30  LOAD_FAST                'coding'
               32  LOAD_GLOBAL              ContentCoding
               34  LOAD_ATTR                identity
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE   200  'to 200'

 L. 737        40  LOAD_FAST                'coding'
               42  LOAD_GLOBAL              ContentCoding
               44  LOAD_ATTR                gzip
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    60  'to 60'
               50  LOAD_CONST               16
               52  LOAD_GLOBAL              zlib
               54  LOAD_ATTR                MAX_WBITS
               56  BINARY_ADD       
               58  JUMP_FORWARD         64  'to 64'
             60_0  COME_FROM            48  '48'
               60  LOAD_GLOBAL              zlib
               62  LOAD_ATTR                MAX_WBITS
             64_0  COME_FROM            58  '58'

 L. 736        64  STORE_FAST               'zlib_mode'

 L. 739        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _body
               70  STORE_FAST               'body_in'

 L. 740        72  LOAD_FAST                'body_in'
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  <74>             
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 742        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _zlib_executor_size
               88  LOAD_CONST               None
               90  <117>                 1  ''

 L. 741        92  POP_JUMP_IF_FALSE   138  'to 138'

 L. 743        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'body_in'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _zlib_executor_size
              104  COMPARE_OP               >

 L. 741       106  POP_JUMP_IF_FALSE   138  'to 138'

 L. 745       108  LOAD_GLOBAL              asyncio
              110  LOAD_METHOD              get_event_loop
              112  CALL_METHOD_0         0  ''
              114  LOAD_METHOD              run_in_executor

 L. 746       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _zlib_executor
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _compress_body
              124  LOAD_FAST                'zlib_mode'

 L. 745       126  CALL_METHOD_3         3  ''
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  POP_TOP          
              136  JUMP_FORWARD        148  'to 148'
            138_0  COME_FROM           106  '106'
            138_1  COME_FROM            92  '92'

 L. 749       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _compress_body
              142  LOAD_FAST                'zlib_mode'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
            148_0  COME_FROM           136  '136'

 L. 751       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _compressed_body
              152  STORE_FAST               'body_out'

 L. 752       154  LOAD_FAST                'body_out'
              156  LOAD_CONST               None
              158  <117>                 1  ''
              160  POP_JUMP_IF_TRUE    166  'to 166'
              162  <74>             
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           160  '160'

 L. 754       166  LOAD_FAST                'coding'
              168  LOAD_ATTR                value
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _headers
              174  LOAD_GLOBAL              hdrs
              176  LOAD_ATTR                CONTENT_ENCODING
              178  STORE_SUBSCR     

 L. 755       180  LOAD_GLOBAL              str
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'body_out'
              186  CALL_FUNCTION_1       1  ''
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                _headers
              194  LOAD_GLOBAL              hdrs
              196  LOAD_ATTR                CONTENT_LENGTH
              198  STORE_SUBSCR     
            200_0  COME_FROM            38  '38'

Parse error at or near `<117>' instruction at offset 76


def json_response--- This code section failed: ---

 L. 769         0  LOAD_FAST                'data'
                2  LOAD_GLOBAL              sentinel
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    34  'to 34'

 L. 770         8  LOAD_FAST                'text'
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  LOAD_FAST                'body'
               14  POP_JUMP_IF_FALSE    26  'to 26'
             16_0  COME_FROM            10  '10'

 L. 771        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'only one of data, text, or body should be specified'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
               24  JUMP_FORWARD         34  'to 34'
             26_0  COME_FROM            14  '14'

 L. 773        26  LOAD_FAST                'dumps'
               28  LOAD_FAST                'data'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'text'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM             6  '6'

 L. 774        34  LOAD_GLOBAL              Response

 L. 775        36  LOAD_FAST                'text'

 L. 776        38  LOAD_FAST                'body'

 L. 777        40  LOAD_FAST                'status'

 L. 778        42  LOAD_FAST                'reason'

 L. 779        44  LOAD_FAST                'headers'

 L. 780        46  LOAD_FAST                'content_type'

 L. 774        48  LOAD_CONST               ('text', 'body', 'status', 'reason', 'headers', 'content_type')
               50  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1