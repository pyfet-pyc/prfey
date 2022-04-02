# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\multipart.py
import base64, binascii, json, re, uuid, warnings, zlib
from collections import deque
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, Union
from urllib.parse import parse_qsl, unquote, urlencode
from multidict import CIMultiDict, CIMultiDictProxy, MultiMapping
from .hdrs import CONTENT_DISPOSITION, CONTENT_ENCODING, CONTENT_LENGTH, CONTENT_TRANSFER_ENCODING, CONTENT_TYPE
from .helpers import CHAR, TOKEN, parse_mimetype, reify
from .http import HeadersParser
from .payload import JsonPayload, LookupError, Order, Payload, StringPayload, get_payload, payload_type
from .streams import StreamReader
__all__ = ('MultipartReader', 'MultipartWriter', 'BodyPartReader', 'BadContentDispositionHeader',
           'BadContentDispositionParam', 'parse_content_disposition', 'content_disposition_filename')
if TYPE_CHECKING:
    from .client_reqrep import ClientResponse

class BadContentDispositionHeader(RuntimeWarning):
    pass


class BadContentDispositionParam(RuntimeWarning):
    pass


def parse_content_disposition--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              str
                2  LOAD_GLOBAL              bool
                4  LOAD_CONST               ('string', 'return')
                6  BUILD_CONST_KEY_MAP_2     2 
                8  LOAD_CODE                <code_object is_token>
               10  LOAD_STR                 'parse_content_disposition.<locals>.is_token'
               12  MAKE_FUNCTION_4          'annotation'
               14  STORE_DEREF              'is_token'

 L.  70        16  LOAD_GLOBAL              str
               18  LOAD_GLOBAL              bool
               20  LOAD_CONST               ('string', 'return')
               22  BUILD_CONST_KEY_MAP_2     2 
               24  LOAD_CODE                <code_object is_quoted>
               26  LOAD_STR                 'parse_content_disposition.<locals>.is_quoted'
               28  MAKE_FUNCTION_4          'annotation'
               30  STORE_FAST               'is_quoted'

 L.  73        32  LOAD_GLOBAL              str
               34  LOAD_GLOBAL              bool
               36  LOAD_CONST               ('string', 'return')
               38  BUILD_CONST_KEY_MAP_2     2 
               40  LOAD_CLOSURE             'is_token'
               42  BUILD_TUPLE_1         1 
               44  LOAD_CODE                <code_object is_rfc5987>
               46  LOAD_STR                 'parse_content_disposition.<locals>.is_rfc5987'
               48  MAKE_FUNCTION_12         'annotation, closure'
               50  STORE_FAST               'is_rfc5987'

 L.  76        52  LOAD_GLOBAL              str
               54  LOAD_GLOBAL              bool
               56  LOAD_CONST               ('string', 'return')
               58  BUILD_CONST_KEY_MAP_2     2 
               60  LOAD_CODE                <code_object is_extended_param>
               62  LOAD_STR                 'parse_content_disposition.<locals>.is_extended_param'
               64  MAKE_FUNCTION_4          'annotation'
               66  STORE_FAST               'is_extended_param'

 L.  79        68  LOAD_GLOBAL              str
               70  LOAD_GLOBAL              bool
               72  LOAD_CONST               ('string', 'return')
               74  BUILD_CONST_KEY_MAP_2     2 
               76  LOAD_CODE                <code_object is_continuous_param>
               78  LOAD_STR                 'parse_content_disposition.<locals>.is_continuous_param'
               80  MAKE_FUNCTION_4          'annotation'
               82  STORE_FAST               'is_continuous_param'

 L.  87        84  LOAD_STR                 ''
               86  LOAD_METHOD              join
               88  LOAD_GLOBAL              map
               90  LOAD_GLOBAL              re
               92  LOAD_ATTR                escape
               94  LOAD_GLOBAL              CHAR
               96  CALL_FUNCTION_2       2  ''
               98  CALL_METHOD_1         1  ''

 L.  86       100  LOAD_CONST               ('chars',)
              102  BUILD_CONST_KEY_MAP_1     1 
              104  LOAD_GLOBAL              str

 L.  87       106  LOAD_GLOBAL              str

 L.  87       108  LOAD_GLOBAL              str

 L.  86       110  LOAD_CONST               ('text', 'chars', 'return')
              112  BUILD_CONST_KEY_MAP_3     3 
              114  LOAD_CODE                <code_object unescape>
              116  LOAD_STR                 'parse_content_disposition.<locals>.unescape'
              118  MAKE_FUNCTION_6          'keyword-only, annotation'
              120  STORE_FAST               'unescape'

 L.  90       122  LOAD_FAST                'header'
              124  POP_JUMP_IF_TRUE    134  'to 134'

 L.  91       126  LOAD_CONST               None
              128  BUILD_MAP_0           0 
              130  BUILD_TUPLE_2         2 
              132  RETURN_VALUE     
            134_0  COME_FROM           124  '124'

 L.  93       134  LOAD_FAST                'header'
              136  LOAD_METHOD              split
              138  LOAD_STR                 ';'
              140  CALL_METHOD_1         1  ''
              142  UNPACK_EX_1+0           
              144  STORE_FAST               'disptype'
              146  STORE_FAST               'parts'

 L.  94       148  LOAD_DEREF               'is_token'
              150  LOAD_FAST                'disptype'
              152  CALL_FUNCTION_1       1  ''
              154  POP_JUMP_IF_TRUE    178  'to 178'

 L.  95       156  LOAD_GLOBAL              warnings
              158  LOAD_METHOD              warn
              160  LOAD_GLOBAL              BadContentDispositionHeader
              162  LOAD_FAST                'header'
              164  CALL_FUNCTION_1       1  ''
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.  96       170  LOAD_CONST               None
              172  BUILD_MAP_0           0 
              174  BUILD_TUPLE_2         2 
              176  RETURN_VALUE     
            178_0  COME_FROM           154  '154'

 L.  98       178  BUILD_MAP_0           0 
              180  STORE_FAST               'params'
            182_0  COME_FROM           682  '682'
            182_1  COME_FROM           510  '510'
            182_2  COME_FROM           458  '458'
            182_3  COME_FROM           388  '388'
            182_4  COME_FROM           320  '320'

 L.  99       182  LOAD_FAST                'parts'
          184_186  POP_JUMP_IF_FALSE   684  'to 684'

 L. 100       188  LOAD_FAST                'parts'
              190  LOAD_METHOD              pop
              192  LOAD_CONST               0
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'item'

 L. 102       198  LOAD_STR                 '='
              200  LOAD_FAST                'item'
              202  COMPARE_OP               not-in
              204  POP_JUMP_IF_FALSE   228  'to 228'

 L. 103       206  LOAD_GLOBAL              warnings
              208  LOAD_METHOD              warn
              210  LOAD_GLOBAL              BadContentDispositionHeader
              212  LOAD_FAST                'header'
              214  CALL_FUNCTION_1       1  ''
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 104       220  LOAD_CONST               None
              222  BUILD_MAP_0           0 
              224  BUILD_TUPLE_2         2 
              226  RETURN_VALUE     
            228_0  COME_FROM           204  '204'

 L. 106       228  LOAD_FAST                'item'
              230  LOAD_METHOD              split
              232  LOAD_STR                 '='
              234  LOAD_CONST               1
              236  CALL_METHOD_2         2  ''
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'key'
              242  STORE_FAST               'value'

 L. 107       244  LOAD_FAST                'key'
              246  LOAD_METHOD              lower
              248  CALL_METHOD_0         0  ''
              250  LOAD_METHOD              strip
              252  CALL_METHOD_0         0  ''
              254  STORE_FAST               'key'

 L. 108       256  LOAD_FAST                'value'
              258  LOAD_METHOD              lstrip
              260  CALL_METHOD_0         0  ''
              262  STORE_FAST               'value'

 L. 110       264  LOAD_FAST                'key'
              266  LOAD_FAST                'params'
              268  COMPARE_OP               in
          270_272  POP_JUMP_IF_FALSE   296  'to 296'

 L. 111       274  LOAD_GLOBAL              warnings
              276  LOAD_METHOD              warn
              278  LOAD_GLOBAL              BadContentDispositionHeader
              280  LOAD_FAST                'header'
              282  CALL_FUNCTION_1       1  ''
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 112       288  LOAD_CONST               None
              290  BUILD_MAP_0           0 
              292  BUILD_TUPLE_2         2 
              294  RETURN_VALUE     
            296_0  COME_FROM           270  '270'

 L. 114       296  LOAD_DEREF               'is_token'
              298  LOAD_FAST                'key'
              300  CALL_FUNCTION_1       1  ''
          302_304  POP_JUMP_IF_TRUE    326  'to 326'

 L. 115       306  LOAD_GLOBAL              warnings
              308  LOAD_METHOD              warn
              310  LOAD_GLOBAL              BadContentDispositionParam
              312  LOAD_FAST                'item'
              314  CALL_FUNCTION_1       1  ''
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 116       320  JUMP_BACK           182  'to 182'
          322_324  BREAK_LOOP          674  'to 674'
            326_0  COME_FROM           302  '302'

 L. 118       326  LOAD_FAST                'is_continuous_param'
              328  LOAD_FAST                'key'
              330  CALL_FUNCTION_1       1  ''
          332_334  POP_JUMP_IF_FALSE   394  'to 394'

 L. 119       336  LOAD_FAST                'is_quoted'
              338  LOAD_FAST                'value'
              340  CALL_FUNCTION_1       1  ''
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L. 120       346  LOAD_FAST                'unescape'
              348  LOAD_FAST                'value'
              350  LOAD_CONST               1
              352  LOAD_CONST               -1
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  CALL_FUNCTION_1       1  ''
              360  STORE_FAST               'value'
              362  JUMP_FORWARD        674  'to 674'
            364_0  COME_FROM           342  '342'

 L. 121       364  LOAD_DEREF               'is_token'
              366  LOAD_FAST                'value'
              368  CALL_FUNCTION_1       1  ''
          370_372  POP_JUMP_IF_TRUE    674  'to 674'

 L. 122       374  LOAD_GLOBAL              warnings
              376  LOAD_METHOD              warn
              378  LOAD_GLOBAL              BadContentDispositionParam
              380  LOAD_FAST                'item'
              382  CALL_FUNCTION_1       1  ''
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          

 L. 123       388  JUMP_BACK           182  'to 182'
          390_392  BREAK_LOOP          674  'to 674'
            394_0  COME_FROM           332  '332'

 L. 125       394  LOAD_FAST                'is_extended_param'
              396  LOAD_FAST                'key'
              398  CALL_FUNCTION_1       1  ''
          400_402  POP_JUMP_IF_FALSE   520  'to 520'

 L. 126       404  LOAD_FAST                'is_rfc5987'
              406  LOAD_FAST                'value'
              408  CALL_FUNCTION_1       1  ''
          410_412  POP_JUMP_IF_FALSE   444  'to 444'

 L. 127       414  LOAD_FAST                'value'
              416  LOAD_METHOD              split
              418  LOAD_STR                 "'"
              420  LOAD_CONST               2
              422  CALL_METHOD_2         2  ''
              424  UNPACK_SEQUENCE_3     3 
              426  STORE_FAST               'encoding'
              428  STORE_FAST               '_'
              430  STORE_FAST               'value'

 L. 128       432  LOAD_FAST                'encoding'
          434_436  JUMP_IF_TRUE_OR_POP   440  'to 440'
              438  LOAD_STR                 'utf-8'
            440_0  COME_FROM           434  '434'
              440  STORE_FAST               'encoding'
              442  JUMP_FORWARD        460  'to 460'
            444_0  COME_FROM           410  '410'

 L. 130       444  LOAD_GLOBAL              warnings
              446  LOAD_METHOD              warn
              448  LOAD_GLOBAL              BadContentDispositionParam
              450  LOAD_FAST                'item'
              452  CALL_FUNCTION_1       1  ''
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          

 L. 131       458  JUMP_BACK           182  'to 182'
            460_0  COME_FROM           442  '442'

 L. 133       460  SETUP_FINALLY       478  'to 478'

 L. 134       462  LOAD_GLOBAL              unquote
              464  LOAD_FAST                'value'
              466  LOAD_FAST                'encoding'
              468  LOAD_STR                 'strict'
              470  CALL_FUNCTION_3       3  ''
              472  STORE_FAST               'value'
              474  POP_BLOCK        
              476  JUMP_FORWARD        518  'to 518'
            478_0  COME_FROM_FINALLY   460  '460'

 L. 135       478  DUP_TOP          
              480  LOAD_GLOBAL              UnicodeDecodeError
              482  COMPARE_OP               exception-match
          484_486  POP_JUMP_IF_FALSE   516  'to 516'
              488  POP_TOP          
              490  POP_TOP          
              492  POP_TOP          

 L. 136       494  LOAD_GLOBAL              warnings
              496  LOAD_METHOD              warn
              498  LOAD_GLOBAL              BadContentDispositionParam
              500  LOAD_FAST                'item'
              502  CALL_FUNCTION_1       1  ''
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          

 L. 137       508  POP_EXCEPT       
              510  JUMP_BACK           182  'to 182'
              512  POP_EXCEPT       
              514  JUMP_FORWARD        518  'to 518'
            516_0  COME_FROM           484  '484'
              516  END_FINALLY      
            518_0  COME_FROM           514  '514'
            518_1  COME_FROM           476  '476'
              518  JUMP_FORWARD        674  'to 674'
            520_0  COME_FROM           400  '400'

 L. 140       520  LOAD_CONST               True
              522  STORE_FAST               'failed'

 L. 141       524  LOAD_FAST                'is_quoted'
              526  LOAD_FAST                'value'
              528  CALL_FUNCTION_1       1  ''
          530_532  POP_JUMP_IF_FALSE   562  'to 562'

 L. 142       534  LOAD_CONST               False
              536  STORE_FAST               'failed'

 L. 143       538  LOAD_FAST                'unescape'
              540  LOAD_FAST                'value'
              542  LOAD_CONST               1
              544  LOAD_CONST               -1
              546  BUILD_SLICE_2         2 
              548  BINARY_SUBSCR    
              550  LOAD_METHOD              lstrip
              552  LOAD_STR                 '\\/'
              554  CALL_METHOD_1         1  ''
              556  CALL_FUNCTION_1       1  ''
              558  STORE_FAST               'value'
              560  JUMP_FORWARD        646  'to 646'
            562_0  COME_FROM           530  '530'

 L. 144       562  LOAD_DEREF               'is_token'
              564  LOAD_FAST                'value'
              566  CALL_FUNCTION_1       1  ''
          568_570  POP_JUMP_IF_FALSE   578  'to 578'

 L. 145       572  LOAD_CONST               False
              574  STORE_FAST               'failed'
              576  JUMP_FORWARD        646  'to 646'
            578_0  COME_FROM           568  '568'

 L. 146       578  LOAD_FAST                'parts'
          580_582  POP_JUMP_IF_FALSE   646  'to 646'

 L. 149       584  LOAD_STR                 '%s;%s'
              586  LOAD_FAST                'value'
              588  LOAD_FAST                'parts'
              590  LOAD_CONST               0
              592  BINARY_SUBSCR    
              594  BUILD_TUPLE_2         2 
              596  BINARY_MODULO    
              598  STORE_FAST               '_value'

 L. 150       600  LOAD_FAST                'is_quoted'
              602  LOAD_FAST                '_value'
              604  CALL_FUNCTION_1       1  ''
          606_608  POP_JUMP_IF_FALSE   646  'to 646'

 L. 151       610  LOAD_FAST                'parts'
              612  LOAD_METHOD              pop
              614  LOAD_CONST               0
              616  CALL_METHOD_1         1  ''
              618  POP_TOP          

 L. 152       620  LOAD_FAST                'unescape'
              622  LOAD_FAST                '_value'
              624  LOAD_CONST               1
              626  LOAD_CONST               -1
              628  BUILD_SLICE_2         2 
              630  BINARY_SUBSCR    
              632  LOAD_METHOD              lstrip
              634  LOAD_STR                 '\\/'
              636  CALL_METHOD_1         1  ''
              638  CALL_FUNCTION_1       1  ''
              640  STORE_FAST               'value'

 L. 153       642  LOAD_CONST               False
              644  STORE_FAST               'failed'
            646_0  COME_FROM           606  '606'
            646_1  COME_FROM           580  '580'
            646_2  COME_FROM           576  '576'
            646_3  COME_FROM           560  '560'

 L. 155       646  LOAD_FAST                'failed'
          648_650  POP_JUMP_IF_FALSE   674  'to 674'

 L. 156       652  LOAD_GLOBAL              warnings
              654  LOAD_METHOD              warn
              656  LOAD_GLOBAL              BadContentDispositionHeader
              658  LOAD_FAST                'header'
              660  CALL_FUNCTION_1       1  ''
              662  CALL_METHOD_1         1  ''
              664  POP_TOP          

 L. 157       666  LOAD_CONST               None
              668  BUILD_MAP_0           0 
              670  BUILD_TUPLE_2         2 
              672  RETURN_VALUE     
            674_0  COME_FROM           648  '648'
            674_1  COME_FROM           518  '518'
            674_2  COME_FROM           390  '390'
            674_3  COME_FROM           370  '370'
            674_4  COME_FROM           362  '362'
            674_5  COME_FROM           322  '322'

 L. 159       674  LOAD_FAST                'value'
              676  LOAD_FAST                'params'
              678  LOAD_FAST                'key'
              680  STORE_SUBSCR     
              682  JUMP_BACK           182  'to 182'
            684_0  COME_FROM           184  '184'

 L. 161       684  LOAD_FAST                'disptype'
              686  LOAD_METHOD              lower
              688  CALL_METHOD_0         0  ''
              690  LOAD_FAST                'params'
              692  BUILD_TUPLE_2         2 
              694  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 516_0


def content_disposition_filename(params: Mapping[(str, str)], name: str='filename') -> Optional[str]:
    name_suf = '%s*' % name
    if not params:
        return
    if name_suf in params:
        return params[name_suf]
    if name in params:
        return params[name]
    parts = []
    fnparams = sorted(((key, value) for key, value in params.items if key.startswithname_suf))
    for num, (key, value) in enumerate(fnparams):
        _, tail = key.split'*'1
        if tail.endswith'*':
            tail = tail[:-1]
        if tail == str(num):
            parts.appendvalue
        else:
            break
    else:
        if not parts:
            return
        value = ''.joinparts
        if "'" in value:
            encoding, _, value = value.split"'"2
            encoding = encoding or 'utf-8'
            return unquote(value, encoding, 'strict')
        return value


class MultipartResponseWrapper:
    __doc__ = 'Wrapper around the MultipartReader.\n\n    It takes care about\n    underlying connection and close it when it needs in.\n    '

    def __init__(self, resp: 'ClientResponse', stream: 'MultipartReader') -> None:
        self.resp = resp
        self.stream = stream

    def __aiter__(self) -> 'MultipartResponseWrapper':
        return self

    async def __anext__(self) -> Union[('MultipartReader', 'BodyPartReader')]:
        part = await self.next
        if part is None:
            raise StopAsyncIteration
        return part

    def at_eof(self) -> bool:
        """Returns True when all response data had been read."""
        return self.resp.content.at_eof

    async def next(self) -> Optional[Union[('MultipartReader', 'BodyPartReader')]]:
        """Emits next multipart reader object."""
        item = await self.stream.next
        if self.stream.at_eof:
            await self.release
        return item

    async def release(self) -> None:
        """Releases the connection gracefully, reading all the content
        to the void."""
        await self.resp.release


class BodyPartReader:
    __doc__ = 'Multipart reader for single body part.'
    chunk_size = 8192

    def __init__(self, boundary: bytes, headers: 'CIMultiDictProxy[str]', content: StreamReader) -> None:
        self.headers = headers
        self._boundary = boundary
        self._content = content
        self._at_eof = False
        length = self.headers.getCONTENT_LENGTHNone
        self._length = int(length) if length is not None else None
        self._read_bytes = 0
        self._unread = deque()
        self._prev_chunk = None
        self._content_eof = 0
        self._cache = {}

    def __aiter__(self) -> 'BodyPartReader':
        return self

    async def __anext__(self) -> bytes:
        part = await self.next
        if part is None:
            raise StopAsyncIteration
        return part

    async def next(self) -> Optional[bytes]:
        item = await self.read
        if not item:
            return
        return item

    async def read(self, *, decode: bool=False) -> bytes:
        """Reads body part data.

        decode: Decodes data following by encoding
                method from Content-Encoding header. If it missed
                data remains untouched
        """
        if self._at_eof:
            return b''
        data = bytearray()
        while True:
            self._at_eof or data.extend(await self.read_chunkself.chunk_size)

        if decode:
            return self.decodedata
        return data

    async def read_chunk(self, size: int=chunk_size) -> bytes:
        """Reads body part content chunk of the specified size.

        size: chunk size
        """
        if self._at_eof:
            return b''
        if self._length:
            chunk = await self._read_chunk_from_lengthsize
        else:
            chunk = await self._read_chunk_from_streamsize
        self._read_bytes += len(chunk)
        if self._read_bytes == self._length:
            self._at_eof = True
        if self._at_eof:
            clrf = await self._content.readline
            assert b'\r\n' == clrf, 'reader did not read all the data or it is malformed'
            return chunk

    async def _read_chunk_from_length(self, size: int) -> bytes:
        assert self._length is not None, 'Content-Length required for chunked read'
        chunk_size = min(size, self._length - self._read_bytes)
        chunk = await self._content.readchunk_size
        return chunk

    async def _read_chunk_from_stream(self, size: int) -> bytes:
        assert size >= len(self._boundary) + 2, 'Chunk size must be greater or equal than boundary length + 2'
        first_chunk = self._prev_chunk is None
        if first_chunk:
            self._prev_chunk = await self._content.readsize
        chunk = await self._content.readsize
        self._content_eof += int(self._content.at_eof)
        assert self._content_eof < 3, 'Reading after EOF'
        assert self._prev_chunk is not None
        window = self._prev_chunk + chunk
        sub = b'\r\n' + self._boundary
        if first_chunk:
            idx = window.findsub
        else:
            idx = window.findsubmax(0, len(self._prev_chunk) - len(sub))
        if idx >= 0:
            with warnings.catch_warnings:
                warnings.filterwarnings('ignore', category=DeprecationWarning)
                self._content.unread_datawindow[idx:]
            if size > idx:
                self._prev_chunk = self._prev_chunk[:idx]
            chunk = window[len(self._prev_chunk):idx]
            if not chunk:
                self._at_eof = True
            result = self._prev_chunk
            self._prev_chunk = chunk
            return result

    async def readline(self) -> bytes:
        """Reads body part by line by line."""
        if self._at_eof:
            return b''
        if self._unread:
            line = self._unread.popleft
        else:
            line = await self._content.readline
        if line.startswithself._boundary:
            sline = line.rstripb'\r\n'
            boundary = self._boundary
            last_boundary = self._boundary + b'--'
            if sline == boundary or sline == last_boundary:
                self._at_eof = True
                self._unread.appendline
                return b''
        else:
            next_line = await self._content.readline
            if next_line.startswithself._boundary:
                line = line[:-2]
            self._unread.appendnext_line
        return line

    async def release(self) -> None:
        """Like read(), but reads all the data to the void."""
        if self._at_eof:
            return
            while True:
                await (self._at_eof or self.read_chunkself.chunk_size)

    async def text(self, *, encoding: Optional[str]=None) -> str:
        """Like read(), but assumes that body part contains text data."""
        data = await self.read(decode=True)
        encoding = encoding or self.get_charset(default='utf-8')
        return data.decodeencoding

    async def json(self, *, encoding: Optional[str]=None) -> Optional[Dict[(str, Any)]]:
        """Like read(), but assumes that body parts contains JSON data."""
        data = await self.read(decode=True)
        if not data:
            return
        encoding = encoding or self.get_charset(default='utf-8')
        return json.loadsdata.decodeencoding

    async def form(self, *, encoding: Optional[str]=None) -> List[Tuple[(str, str)]]:
        """Like read(), but assumes that body parts contains form
        urlencoded data.
        """
        data = await self.read(decode=True)
        if not data:
            return []
        if encoding is not None:
            real_encoding = encoding
        else:
            real_encoding = self.get_charset(default='utf-8')
        return parse_qsl((data.rstrip.decodereal_encoding), keep_blank_values=True,
          encoding=real_encoding)

    def at_eof(self) -> bool:
        """Returns True if the boundary was reached or False otherwise."""
        return self._at_eof

    def decode(self, data: bytes) -> bytes:
        """Decodes data according the specified Content-Encoding
        or Content-Transfer-Encoding headers value.
        """
        if CONTENT_TRANSFER_ENCODING in self.headers:
            data = self._decode_content_transferdata
        if CONTENT_ENCODING in self.headers:
            return self._decode_contentdata
        return data

    def _decode_content(self, data: bytes) -> bytes:
        encoding = self.headers.getCONTENT_ENCODING''.lower
        if encoding == 'deflate':
            return zlib.decompressdata(-zlib.MAX_WBITS)
        if encoding == 'gzip':
            return zlib.decompressdata(16 + zlib.MAX_WBITS)
        if encoding == 'identity':
            return data
        raise RuntimeError('unknown content encoding: {}'.formatencoding)

    def _decode_content_transfer(self, data: bytes) -> bytes:
        encoding = self.headers.getCONTENT_TRANSFER_ENCODING''.lower
        if encoding == 'base64':
            return base64.b64decodedata
        if encoding == 'quoted-printable':
            return binascii.a2b_qpdata
        if encoding in ('binary', '8bit', '7bit'):
            return data
        raise RuntimeError('unknown content transfer encoding: {}'.formatencoding)

    def get_charset(self, default: str) -> str:
        """Returns charset parameter from Content-Type header or default."""
        ctype = self.headers.getCONTENT_TYPE''
        mimetype = parse_mimetype(ctype)
        return mimetype.parameters.get'charset'default

    @reify
    def name(self) -> Optional[str]:
        """Returns name specified in Content-Disposition header or None
        if missed or header is malformed.
        """
        _, params = parse_content_disposition(self.headers.getCONTENT_DISPOSITION)
        return content_disposition_filename(params, 'name')

    @reify
    def filename(self) -> Optional[str]:
        """Returns filename specified in Content-Disposition header or None
        if missed or header is malformed.
        """
        _, params = parse_content_disposition(self.headers.getCONTENT_DISPOSITION)
        return content_disposition_filename(params, 'filename')


@payload_type(BodyPartReader, order=(Order.try_first))
class BodyPartReaderPayload(Payload):

    def __init__(self, value, *args, **kwargs):
        (super().__init__)(value, *args, **kwargs)
        params = {}
        if value.name is not None:
            params['name'] = value.name
        if value.filename is not None:
            params['filename'] = value.filename
        if params:
            (self.set_content_disposition)(*('attachment', True), **params)

    async def write(self, writer: Any) -> None:
        field = self._value
        chunk = await field.read_chunk(size=65536)
        while True:
            if chunk:
                await writer.writefield.decodechunk
                chunk = await field.read_chunk(size=65536)


class MultipartReader:
    __doc__ = 'Multipart body reader.'
    response_wrapper_cls = MultipartResponseWrapper
    multipart_reader_cls = None
    part_reader_cls = BodyPartReader

    def __init__(self, headers: Mapping[(str, str)], content: StreamReader) -> None:
        self.headers = headers
        self._boundary = ('--' + self._get_boundary).encode
        self._content = content
        self._last_part = None
        self._at_eof = False
        self._at_bof = True
        self._unread = []

    def __aiter__(self) -> 'MultipartReader':
        return self

    async def __anext__(self) -> Union[('MultipartReader', BodyPartReader)]:
        part = await self.next
        if part is None:
            raise StopAsyncIteration
        return part

    @classmethod
    def from_response(cls, response: 'ClientResponse') -> MultipartResponseWrapper:
        """Constructs reader instance from HTTP response.

        :param response: :class:`~aiohttp.client.ClientResponse` instance
        """
        obj = cls.response_wrapper_clsresponsecls(response.headers, response.content)
        return obj

    def at_eof(self) -> bool:
        """Returns True if the final boundary was reached or
        False otherwise.
        """
        return self._at_eof

    async def next(self) -> Optional[Union[('MultipartReader', BodyPartReader)]]:
        """Emits the next multipart body part."""
        if self._at_eof:
            return
        await self._maybe_release_last_part
        if self._at_bof:
            await self._read_until_first_boundary
            self._at_bof = False
        else:
            await self._read_boundary
        if self._at_eof:
            return
        self._last_part = await self.fetch_next_part
        return self._last_part

    async def release(self) -> None:
        """Reads all the body parts to the void till the final boundary."""
        while True:
            item = await (self._at_eof or self.next)
            if item is None:
                pass
            else:
                await item.release

    async def fetch_next_part(self) -> Union[('MultipartReader', BodyPartReader)]:
        """Returns the next body part reader."""
        headers = await self._read_headers
        return self._get_part_readerheaders

    def _get_part_reader(self, headers: 'CIMultiDictProxy[str]') -> Union[('MultipartReader', BodyPartReader)]:
        """Dispatches the response by the `Content-Type` header, returning
        suitable reader instance.

        :param dict headers: Response headers
        """
        ctype = headers.getCONTENT_TYPE''
        mimetype = parse_mimetype(ctype)
        if mimetype.type == 'multipart':
            if self.multipart_reader_cls is None:
                return type(self)(headers, self._content)
            return self.multipart_reader_clsheadersself._content
        return self.part_reader_cls(self._boundary, headers, self._content)

    def _get_boundary(self) -> str:
        mimetype = parse_mimetype(self.headers[CONTENT_TYPE])
        assert mimetype.type == 'multipart', 'multipart/* content type expected'
        if 'boundary' not in mimetype.parameters:
            raise ValueError('boundary missed for Content-Type: %s' % self.headers[CONTENT_TYPE])
        boundary = mimetype.parameters['boundary']
        if len(boundary) > 70:
            raise ValueError('boundary %r is too long (70 chars max)' % boundary)
        return boundary

    async def _readline(self) -> bytes:
        if self._unread:
            return self._unread.pop
        return await self._content.readline

    async def _read_until_first_boundary(self) -> None:
        while True:
            chunk = await self._readline
            if chunk == b'':
                raise ValueError('Could not find starting boundary %r' % self._boundary)
            chunk = chunk.rstrip
            if chunk == self._boundary:
                return
            if chunk == self._boundary + b'--':
                self._at_eof = True
                return

    async def _read_boundary(self) -> None:
        chunk = (await self._readline).rstrip
        if chunk == self._boundary:
            pass
        elif chunk == self._boundary + b'--':
            self._at_eof = True
            epilogue = await self._readline
            next_line = await self._readline
            if next_line[:2] == b'--':
                self._unread.appendnext_line
            else:
                self._unread.extend[next_line, epilogue]
        else:
            raise ValueError('Invalid boundary %r, expected %r' % (
             chunk, self._boundary))

    async def _read_headers--- This code section failed: ---

 L. 680         0  LOAD_CONST               b''
                2  BUILD_LIST_1          1 
                4  STORE_FAST               'lines'
              6_0  COME_FROM            46  '46'
              6_1  COME_FROM            42  '42'

 L. 682         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _content
               10  LOAD_METHOD              readline
               12  CALL_METHOD_0         0  ''
               14  GET_AWAITABLE    
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  STORE_FAST               'chunk'

 L. 683        22  LOAD_FAST                'chunk'
               24  LOAD_METHOD              strip
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'chunk'

 L. 684        30  LOAD_FAST                'lines'
               32  LOAD_METHOD              append
               34  LOAD_FAST                'chunk'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 685        40  LOAD_FAST                'chunk'
               42  POP_JUMP_IF_TRUE_BACK     6  'to 6'

 L. 686        44  JUMP_FORWARD         48  'to 48'
               46  JUMP_BACK             6  'to 6'
             48_0  COME_FROM            44  '44'

 L. 687        48  LOAD_GLOBAL              HeadersParser
               50  CALL_FUNCTION_0       0  ''
               52  STORE_FAST               'parser'

 L. 688        54  LOAD_FAST                'parser'
               56  LOAD_METHOD              parse_headers
               58  LOAD_FAST                'lines'
               60  CALL_METHOD_1         1  ''
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'headers'
               66  STORE_FAST               'raw_headers'

 L. 689        68  LOAD_FAST                'headers'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 46

    async def _maybe_release_last_part(self) -> None:
        """Ensures that the last read body part is read completely."""
        if self._last_part is not None:
            if not self._last_part.at_eof:
                await self._last_part.release
            self._unread.extendself._last_part._unread
            self._last_part = None


_Part = Tuple[(Payload, str, str)]

class MultipartWriter(Payload):
    __doc__ = 'Multipart body writer.'

    def __init__(self, subtype='mixed', boundary=None):
        boundary = boundary if boundary is not None else uuid.uuid4.hex
        try:
            self._boundary = boundary.encode'ascii'
        except UnicodeEncodeError:
            raise ValueError('boundary should contain ASCII only chars') from None
        else:
            ctype = 'multipart/{}; boundary={}'.formatsubtypeself._boundary_value
            super().__init__(None, content_type=ctype)
            self._parts = []

    def __enter__(self) -> 'MultipartWriter':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        pass

    def __iter__(self) -> Iterator[_Part]:
        return iter(self._parts)

    def __len__(self) -> int:
        return len(self._parts)

    def __bool__(self) -> bool:
        return True

    _valid_tchar_regex = re.compileb"\\A[!#$%&'*+\\-.^_`|~\\w]+\\Z"
    _invalid_qdtext_char_regex = re.compileb'[\\x00-\\x08\\x0A-\\x1F\\x7F]'

    @property
    def _boundary_value(self) -> str:
        """Wrap boundary parameter value in quotes, if necessary.

        Reads self.boundary and returns a unicode sting.
        """
        value = self._boundary
        if re.matchself._valid_tchar_regexvalue:
            return value.decode'ascii'
        if re.searchself._invalid_qdtext_char_regexvalue:
            raise ValueError('boundary value contains invalid characters')
        quoted_value_content = value.replaceb'\\'b'\\\\'
        quoted_value_content = quoted_value_content.replaceb'"'b'\\"'
        return '"' + quoted_value_content.decode'ascii' + '"'

    @property
    def boundary(self) -> str:
        return self._boundary.decode'ascii'

    def append(self, obj: Any, headers: Optional[MultiMapping[str]]=None) -> Payload:
        if headers is None:
            headers = CIMultiDict()
        if isinstance(obj, Payload):
            obj.headers.updateheaders
            return self.append_payloadobj
        try:
            payload = get_payload(obj, headers=headers)
        except LookupError:
            raise TypeError('Cannot create payload from %r' % obj)
        else:
            return self.append_payloadpayload

    def append_payload(self, payload: Payload) -> Payload:
        """Adds a new body part to multipart writer."""
        encoding = payload.headers.getCONTENT_ENCODING''.lower
        if encoding:
            if encoding not in ('deflate', 'gzip', 'identity'):
                raise RuntimeError('unknown content encoding: {}'.formatencoding)
        if encoding == 'identity':
            encoding = None
        te_encoding = payload.headers.getCONTENT_TRANSFER_ENCODING''.lower
        if te_encoding not in ('', 'base64', 'quoted-printable', 'binary'):
            raise RuntimeError('unknown content transfer encoding: {}'.formatte_encoding)
        if te_encoding == 'binary':
            te_encoding = None
        size = payload.size
        if size is not None:
            if not encoding:
                if not te_encoding:
                    payload.headers[CONTENT_LENGTH] = str(size)
            self._parts.append(payload, encoding, te_encoding)
            return payload

    def append_json(self, obj: Any, headers: Optional[MultiMapping[str]]=None) -> Payload:
        """Helper to append JSON part."""
        if headers is None:
            headers = CIMultiDict()
        return self.append_payloadJsonPayload(obj, headers=headers)

    def append_form(self, obj: Union[(Sequence[Tuple[(str, str)]],
 Mapping[(str, str)])], headers: Optional[MultiMapping[str]]=None) -> Payload:
        """Helper to append form urlencoded part."""
        assert isinstance(obj, (Sequence, Mapping))
        if headers is None:
            headers = CIMultiDict()
        if isinstance(obj, Mapping):
            obj = list(obj.items)
        data = urlencode(obj, doseq=True)
        return self.append_payloadStringPayload(data, headers=headers, content_type='application/x-www-form-urlencoded')

    @property
    def size(self) -> Optional[int]:
        """Size of the payload."""
        total = 0
        for part, encoding, te_encoding in self._parts:
            if encoding or te_encoding or part.size is None:
                return None
            else:
                total += int(2 + len(self._boundary) + 2 + part.size + len(part._binary_headers) + 2)
        else:
            total += 2 + len(self._boundary) + 4
            return total

    async def write(self, writer: Any, close_boundary: bool=True) -> None:
        """Write body."""
        for part, encoding, te_encoding in self._parts:
            await writer.write(b'--' + self._boundary + b'\r\n')
            await writer.writepart._binary_headers
            if encoding or te_encoding:
                w = MultipartPayloadWriter(writer)
                if encoding:
                    w.enable_compressionencoding
                if te_encoding:
                    w.enable_encodingte_encoding
                await part.writew
                await w.write_eof
            else:
                await part.writewriter
            await writer.writeb'\r\n'
        else:
            if close_boundary:
                await writer.write(b'--' + self._boundary + b'--\r\n')


class MultipartPayloadWriter:

    def __init__(self, writer: Any) -> None:
        self._writer = writer
        self._encoding = None
        self._compress = None
        self._encoding_buffer = None

    def enable_encoding(self, encoding: str) -> None:
        if encoding == 'base64':
            self._encoding = encoding
            self._encoding_buffer = bytearray()
        elif encoding == 'quoted-printable':
            self._encoding = 'quoted-printable'

    def enable_compression(self, encoding: str='deflate') -> None:
        zlib_mode = 16 + zlib.MAX_WBITS if encoding == 'gzip' else -zlib.MAX_WBITS
        self._compress = zlib.compressobj(wbits=zlib_mode)

    async def write_eof(self) -> None:
        if self._compress is not None:
            chunk = self._compress.flush
            if chunk:
                self._compress = None
                await self.writechunk
        if self._encoding == 'base64':
            if self._encoding_buffer:
                await self._writer.writebase64.b64encodeself._encoding_buffer

    async def write(self, chunk: bytes) -> None:
        if not self._compress is not None or chunk:
            chunk = self._compress.compresschunk
            if not chunk:
                return
        if self._encoding == 'base64':
            buf = self._encoding_buffer
            assert buf is not None
            buf.extendchunk
            if buf:
                div, mod = divmod(len(buf), 3)
                enc_chunk, self._encoding_buffer = buf[:div * 3], buf[div * 3:]
                if enc_chunk:
                    b64chunk = base64.b64encodeenc_chunk
                    await self._writer.writeb64chunk
        elif self._encoding == 'quoted-printable':
            await self._writer.writebinascii.b2a_qpchunk
        else:
            await self._writer.writechunk