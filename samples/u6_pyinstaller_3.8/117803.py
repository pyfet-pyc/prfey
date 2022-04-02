# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\http_parser.py
import abc, asyncio, collections, re, string, zlib
from enum import IntEnum
from typing import Any, List, Optional, Tuple, Type, Union
from multidict import CIMultiDict, CIMultiDictProxy, istr
from yarl import URL
from . import hdrs
from .base_protocol import BaseProtocol
from .helpers import NO_EXTENSIONS, BaseTimerContext
from .http_exceptions import BadStatusLine, ContentEncodingError, ContentLengthError, InvalidHeader, LineTooLong, TransferEncodingError
from .http_writer import HttpVersion, HttpVersion10
from .log import internal_logger
from .streams import EMPTY_PAYLOAD, StreamReader
from .typedefs import RawHeaders
try:
    import brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False
else:
    __all__ = ('HeadersParser', 'HttpParser', 'HttpRequestParser', 'HttpResponseParser',
               'RawRequestMessage', 'RawResponseMessage')
    ASCIISET = set(string.printable)
    METHRE = re.compile("[!#$%&'*+\\-.^_`|~0-9A-Za-z]+")
    VERSRE = re.compile('HTTP/(\\d+).(\\d+)')
    HDRRE = re.compile(b'[\\x00-\\x1F\\x7F()<>@,;:\\[\\]={} \\t\\\\\\\\\\"]')
    RawRequestMessage = collections.namedtuple('RawRequestMessage', [
     'method', 'path', 'version', 'headers', 'raw_headers',
     'should_close', 'compression', 'upgrade', 'chunked', 'url'])
    RawResponseMessage = collections.namedtuple('RawResponseMessage', [
     'version', 'code', 'reason', 'headers', 'raw_headers',
     'should_close', 'compression', 'upgrade', 'chunked'])

    class ParseState(IntEnum):
        PARSE_NONE = 0
        PARSE_LENGTH = 1
        PARSE_CHUNKED = 2
        PARSE_UNTIL_EOF = 3


    class ChunkState(IntEnum):
        PARSE_CHUNKED_SIZE = 0
        PARSE_CHUNKED_CHUNK = 1
        PARSE_CHUNKED_CHUNK_EOF = 2
        PARSE_MAYBE_TRAILERS = 3
        PARSE_TRAILERS = 4


    class HeadersParser:

        def __init__(self, max_line_size: int=8190, max_headers: int=32768, max_field_size: int=8190) -> None:
            self.max_line_size = max_line_size
            self.max_headers = max_headers
            self.max_field_size = max_field_size

        def parse_headers(self, lines: List[bytes]) -> Tuple[('CIMultiDictProxy[str]', RawHeaders)]:
            headers = CIMultiDict()
            raw_headers = []
            lines_idx = 1
            line = lines[1]
            line_count = len(lines)
            while line:
                try:
                    bname, bvalue = line.split(b':', 1)
                except ValueError:
                    raise InvalidHeader(line) from None
                else:
                    bname = bname.strip(b' \t')
                    bvalue = bvalue.lstrip()
                    if HDRRE.search(bname):
                        raise InvalidHeader(bname)
                    else:
                        if len(bname) > self.max_field_size:
                            raise LineTooLong('request header name {}'.format(bname.decode('utf8', 'xmlcharrefreplace')), str(self.max_field_size), str(len(bname)))
                        header_length = len(bvalue)
                        lines_idx += 1
                        line = lines[lines_idx]
                        continuation = line and line[0] in (32, 9)
                        if continuation:
                            bvalue_lst = [
                             bvalue]
                            if continuation:
                                header_length += len(line)
                                if header_length > self.max_field_size:
                                    raise LineTooLong('request header field {}'.format(bname.decode('utf8', 'xmlcharrefreplace')), str(self.max_field_size), str(header_length))
                                bvalue_lst.append(line)
                                lines_idx += 1
                                if lines_idx < line_count:
                                    line = lines[lines_idx]
                                    if line:
                                        continuation = line[0] in (32, 9)
                                else:
                                    line = b''
                                    break
                            else:
                                bvalue = (b'').join(bvalue_lst)
                        elif header_length > self.max_field_size:
                            raise LineTooLong('request header field {}'.format(bname.decode('utf8', 'xmlcharrefreplace')), str(self.max_field_size), str(header_length))
                    bvalue = bvalue.strip()
                    name = bname.decode('utf-8', 'surrogateescape')
                    value = bvalue.decode('utf-8', 'surrogateescape')
                    headers.add(name, value)
                    raw_headers.append((bname, bvalue))

            return (
             CIMultiDictProxy(headers), tuple(raw_headers))


    class HttpParser(abc.ABC):

        def __init__(self, protocol: Optional[BaseProtocol]=None, loop: Optional[asyncio.AbstractEventLoop]=None, max_line_size: int=8190, max_headers: int=32768, max_field_size: int=8190, timer: Optional[BaseTimerContext]=None, code: Optional[int]=None, method: Optional[str]=None, readall: bool=False, payload_exception: Optional[Type[BaseException]]=None, response_with_body: bool=True, read_until_eof: bool=False, auto_decompress: bool=True) -> None:
            self.protocol = protocol
            self.loop = loop
            self.max_line_size = max_line_size
            self.max_headers = max_headers
            self.max_field_size = max_field_size
            self.timer = timer
            self.code = code
            self.method = method
            self.readall = readall
            self.payload_exception = payload_exception
            self.response_with_body = response_with_body
            self.read_until_eof = read_until_eof
            self._lines = []
            self._tail = b''
            self._upgraded = False
            self._payload = None
            self._payload_parser = None
            self._auto_decompress = auto_decompress
            self._headers_parser = HeadersParser(max_line_size, max_headers, max_field_size)

        @abc.abstractmethod
        def parse_message(self, lines: List[bytes]) -> Any:
            pass

        def feed_eof--- This code section failed: ---

 L. 210         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _payload_parser
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 211        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _payload_parser
               14  LOAD_METHOD              feed_eof
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 212        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _payload_parser
               26  JUMP_FORWARD        118  'to 118'
             28_0  COME_FROM             8  '8'

 L. 215        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _tail
               32  POP_JUMP_IF_FALSE    48  'to 48'

 L. 216        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _lines
               38  LOAD_METHOD              append
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _tail
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            32  '32'

 L. 218        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _lines
               52  POP_JUMP_IF_FALSE   118  'to 118'

 L. 219        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _lines
               58  LOAD_CONST               -1
               60  BINARY_SUBSCR    
               62  LOAD_STR                 '\r\n'
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 220        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _lines
               72  LOAD_METHOD              append
               74  LOAD_CONST               b''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            66  '66'

 L. 221        80  SETUP_FINALLY        96  'to 96'

 L. 222        82  LOAD_FAST                'self'
               84  LOAD_METHOD              parse_message
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _lines
               90  CALL_METHOD_1         1  ''
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY    80  '80'

 L. 223        96  DUP_TOP          
               98  LOAD_GLOBAL              Exception
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   116  'to 116'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 224       110  POP_EXCEPT       
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM           102  '102'
              116  END_FINALLY      
            118_0  COME_FROM            52  '52'
            118_1  COME_FROM            26  '26'

Parse error at or near `POP_TOP' instruction at offset 106

        def feed_data--- This code section failed: ---

 L. 236         0  BUILD_LIST_0          0 
                2  STORE_FAST               'messages'

 L. 238         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _tail
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 239        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _tail
               14  LOAD_FAST                'data'
               16  BINARY_ADD       
               18  LOAD_CONST               b''
               20  ROT_TWO          
               22  STORE_FAST               'data'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _tail
             28_0  COME_FROM             8  '8'

 L. 241        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'data'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'data_len'

 L. 242        36  LOAD_CONST               0
               38  STORE_FAST               'start_pos'

 L. 243        40  LOAD_FAST                'self'
               42  LOAD_ATTR                loop
               44  STORE_FAST               'loop'

 L. 245        46  LOAD_FAST                'start_pos'
               48  LOAD_FAST                'data_len'
               50  COMPARE_OP               <
            52_54  POP_JUMP_IF_FALSE   900  'to 900'

 L. 249        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _payload_parser
               60  LOAD_CONST               None
               62  COMPARE_OP               is
            64_66  POP_JUMP_IF_FALSE   658  'to 658'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _upgraded
            72_74  POP_JUMP_IF_TRUE    658  'to 658'

 L. 250        76  LOAD_FAST                'data'
               78  LOAD_METHOD              find
               80  LOAD_FAST                'SEP'
               82  LOAD_FAST                'start_pos'
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'pos'

 L. 252        88  LOAD_FAST                'pos'
               90  LOAD_FAST                'start_pos'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   112  'to 112'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _lines
              100  POP_JUMP_IF_TRUE    112  'to 112'

 L. 253       102  LOAD_FAST                'pos'
              104  LOAD_CONST               2
              106  BINARY_ADD       
              108  STORE_FAST               'start_pos'

 L. 254       110  JUMP_BACK            46  'to 46'
            112_0  COME_FROM           100  '100'
            112_1  COME_FROM            94  '94'

 L. 256       112  LOAD_FAST                'pos'
              114  LOAD_FAST                'start_pos'
              116  COMPARE_OP               >=
          118_120  POP_JUMP_IF_FALSE   634  'to 634'

 L. 258       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _lines
              126  LOAD_METHOD              append
              128  LOAD_FAST                'data'
              130  LOAD_FAST                'start_pos'
              132  LOAD_FAST                'pos'
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 259       142  LOAD_FAST                'pos'
              144  LOAD_CONST               2
              146  BINARY_ADD       
              148  STORE_FAST               'start_pos'

 L. 262       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _lines
              154  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'EMPTY'
              160  COMPARE_OP               ==
          162_164  POP_JUMP_IF_FALSE   656  'to 656'

 L. 263       166  SETUP_FINALLY       184  'to 184'

 L. 264       168  LOAD_FAST                'self'
              170  LOAD_METHOD              parse_message
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _lines
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'msg'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM_FINALLY   166  '166'

 L. 266       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _lines
              188  LOAD_METHOD              clear
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          
              194  END_FINALLY      

 L. 269       196  LOAD_FAST                'msg'
              198  LOAD_ATTR                headers
              200  LOAD_METHOD              get
              202  LOAD_FAST                'CONTENT_LENGTH'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'length'

 L. 270       208  LOAD_FAST                'length'
              210  LOAD_CONST               None
              212  COMPARE_OP               is-not
          214_216  POP_JUMP_IF_FALSE   280  'to 280'

 L. 271       218  SETUP_FINALLY       232  'to 232'

 L. 272       220  LOAD_GLOBAL              int
              222  LOAD_FAST                'length'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'length'
              228  POP_BLOCK        
              230  JUMP_FORWARD        262  'to 262'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 273       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   260  'to 260'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 274       248  LOAD_GLOBAL              InvalidHeader
              250  LOAD_FAST                'CONTENT_LENGTH'
              252  CALL_FUNCTION_1       1  ''
              254  RAISE_VARARGS_1       1  'exception instance'
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           238  '238'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM           230  '230'

 L. 275       262  LOAD_FAST                'length'
              264  LOAD_CONST               0
              266  COMPARE_OP               <
          268_270  POP_JUMP_IF_FALSE   280  'to 280'

 L. 276       272  LOAD_GLOBAL              InvalidHeader
              274  LOAD_FAST                'CONTENT_LENGTH'
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
            280_0  COME_FROM           268  '268'
            280_1  COME_FROM           214  '214'

 L. 279       280  LOAD_FAST                'SEC_WEBSOCKET_KEY1'
              282  LOAD_FAST                'msg'
              284  LOAD_ATTR                headers
              286  COMPARE_OP               in
          288_290  POP_JUMP_IF_FALSE   300  'to 300'

 L. 280       292  LOAD_GLOBAL              InvalidHeader
              294  LOAD_FAST                'SEC_WEBSOCKET_KEY1'
              296  CALL_FUNCTION_1       1  ''
              298  RAISE_VARARGS_1       1  'exception instance'
            300_0  COME_FROM           288  '288'

 L. 282       300  LOAD_FAST                'msg'
              302  LOAD_ATTR                upgrade
              304  LOAD_FAST                'self'
              306  STORE_ATTR               _upgraded

 L. 284       308  LOAD_GLOBAL              getattr
              310  LOAD_FAST                'msg'
              312  LOAD_STR                 'method'
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                method
              318  CALL_FUNCTION_3       3  ''
              320  STORE_FAST               'method'

 L. 286       322  LOAD_FAST                'self'
              324  LOAD_ATTR                protocol
              326  LOAD_CONST               None
              328  COMPARE_OP               is-not
          330_332  POP_JUMP_IF_TRUE    338  'to 338'
              334  LOAD_ASSERT              AssertionError
              336  RAISE_VARARGS_1       1  'exception instance'
            338_0  COME_FROM           330  '330'

 L. 288       338  LOAD_FAST                'length'
              340  LOAD_CONST               None
              342  COMPARE_OP               is-not
          344_346  POP_JUMP_IF_FALSE   358  'to 358'
              348  LOAD_FAST                'length'
              350  LOAD_CONST               0
              352  COMPARE_OP               >
          354_356  POP_JUMP_IF_TRUE    374  'to 374'
            358_0  COME_FROM           344  '344'

 L. 289       358  LOAD_FAST                'msg'
              360  LOAD_ATTR                chunked

 L. 288   362_364  POP_JUMP_IF_FALSE   446  'to 446'

 L. 289       366  LOAD_FAST                'msg'
              368  LOAD_ATTR                upgrade

 L. 288   370_372  POP_JUMP_IF_TRUE    446  'to 446'
            374_0  COME_FROM           354  '354'

 L. 290       374  LOAD_GLOBAL              StreamReader

 L. 291       376  LOAD_FAST                'self'
              378  LOAD_ATTR                protocol

 L. 291       380  LOAD_FAST                'self'
              382  LOAD_ATTR                timer

 L. 291       384  LOAD_FAST                'loop'

 L. 290       386  LOAD_CONST               ('timer', 'loop')
              388  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              390  STORE_FAST               'payload'

 L. 292       392  LOAD_GLOBAL              HttpPayloadParser

 L. 293       394  LOAD_FAST                'payload'

 L. 293       396  LOAD_FAST                'length'

 L. 294       398  LOAD_FAST                'msg'
              400  LOAD_ATTR                chunked

 L. 294       402  LOAD_FAST                'method'

 L. 295       404  LOAD_FAST                'msg'
              406  LOAD_ATTR                compression

 L. 296       408  LOAD_FAST                'self'
              410  LOAD_ATTR                code

 L. 296       412  LOAD_FAST                'self'
              414  LOAD_ATTR                readall

 L. 297       416  LOAD_FAST                'self'
              418  LOAD_ATTR                response_with_body

 L. 298       420  LOAD_FAST                'self'
              422  LOAD_ATTR                _auto_decompress

 L. 292       424  LOAD_CONST               ('length', 'chunked', 'method', 'compression', 'code', 'readall', 'response_with_body', 'auto_decompress')
              426  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              428  STORE_FAST               'payload_parser'

 L. 299       430  LOAD_FAST                'payload_parser'
              432  LOAD_ATTR                done
          434_436  POP_JUMP_IF_TRUE    618  'to 618'

 L. 300       438  LOAD_FAST                'payload_parser'
              440  LOAD_FAST                'self'
              442  STORE_ATTR               _payload_parser
              444  JUMP_FORWARD        618  'to 618'
            446_0  COME_FROM           370  '370'
            446_1  COME_FROM           362  '362'

 L. 301       446  LOAD_FAST                'method'
              448  LOAD_FAST                'METH_CONNECT'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   508  'to 508'

 L. 302       456  LOAD_GLOBAL              StreamReader

 L. 303       458  LOAD_FAST                'self'
              460  LOAD_ATTR                protocol

 L. 303       462  LOAD_FAST                'self'
              464  LOAD_ATTR                timer

 L. 303       466  LOAD_FAST                'loop'

 L. 302       468  LOAD_CONST               ('timer', 'loop')
              470  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              472  STORE_FAST               'payload'

 L. 304       474  LOAD_CONST               True
              476  LOAD_FAST                'self'
              478  STORE_ATTR               _upgraded

 L. 305       480  LOAD_GLOBAL              HttpPayloadParser

 L. 306       482  LOAD_FAST                'payload'

 L. 306       484  LOAD_FAST                'msg'
              486  LOAD_ATTR                method

 L. 307       488  LOAD_FAST                'msg'
              490  LOAD_ATTR                compression

 L. 307       492  LOAD_CONST               True

 L. 308       494  LOAD_FAST                'self'
              496  LOAD_ATTR                _auto_decompress

 L. 305       498  LOAD_CONST               ('method', 'compression', 'readall', 'auto_decompress')
              500  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              502  LOAD_FAST                'self'
              504  STORE_ATTR               _payload_parser
              506  JUMP_FORWARD        618  'to 618'
            508_0  COME_FROM           452  '452'

 L. 310       508  LOAD_GLOBAL              getattr
              510  LOAD_FAST                'msg'
              512  LOAD_STR                 'code'
              514  LOAD_CONST               100
              516  CALL_FUNCTION_3       3  ''
              518  LOAD_CONST               199
              520  COMPARE_OP               >=
          522_524  POP_JUMP_IF_FALSE   614  'to 614'

 L. 311       526  LOAD_FAST                'length'
              528  LOAD_CONST               None
              530  COMPARE_OP               is

 L. 310   532_534  POP_JUMP_IF_FALSE   614  'to 614'

 L. 311       536  LOAD_FAST                'self'
              538  LOAD_ATTR                read_until_eof

 L. 310   540_542  POP_JUMP_IF_FALSE   614  'to 614'

 L. 312       544  LOAD_GLOBAL              StreamReader

 L. 313       546  LOAD_FAST                'self'
              548  LOAD_ATTR                protocol

 L. 313       550  LOAD_FAST                'self'
              552  LOAD_ATTR                timer

 L. 313       554  LOAD_FAST                'loop'

 L. 312       556  LOAD_CONST               ('timer', 'loop')
              558  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              560  STORE_FAST               'payload'

 L. 314       562  LOAD_GLOBAL              HttpPayloadParser

 L. 315       564  LOAD_FAST                'payload'

 L. 315       566  LOAD_FAST                'length'

 L. 316       568  LOAD_FAST                'msg'
              570  LOAD_ATTR                chunked

 L. 316       572  LOAD_FAST                'method'

 L. 317       574  LOAD_FAST                'msg'
              576  LOAD_ATTR                compression

 L. 318       578  LOAD_FAST                'self'
              580  LOAD_ATTR                code

 L. 318       582  LOAD_CONST               True

 L. 319       584  LOAD_FAST                'self'
              586  LOAD_ATTR                response_with_body

 L. 320       588  LOAD_FAST                'self'
              590  LOAD_ATTR                _auto_decompress

 L. 314       592  LOAD_CONST               ('length', 'chunked', 'method', 'compression', 'code', 'readall', 'response_with_body', 'auto_decompress')
              594  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              596  STORE_FAST               'payload_parser'

 L. 321       598  LOAD_FAST                'payload_parser'
              600  LOAD_ATTR                done
          602_604  POP_JUMP_IF_TRUE    618  'to 618'

 L. 322       606  LOAD_FAST                'payload_parser'
              608  LOAD_FAST                'self'
              610  STORE_ATTR               _payload_parser
              612  JUMP_FORWARD        618  'to 618'
            614_0  COME_FROM           540  '540'
            614_1  COME_FROM           532  '532'
            614_2  COME_FROM           522  '522'

 L. 324       614  LOAD_GLOBAL              EMPTY_PAYLOAD
              616  STORE_FAST               'payload'
            618_0  COME_FROM           612  '612'
            618_1  COME_FROM           602  '602'
            618_2  COME_FROM           506  '506'
            618_3  COME_FROM           444  '444'
            618_4  COME_FROM           434  '434'

 L. 326       618  LOAD_FAST                'messages'
              620  LOAD_METHOD              append
              622  LOAD_FAST                'msg'
              624  LOAD_FAST                'payload'
              626  BUILD_TUPLE_2         2 
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
              632  JUMP_FORWARD        656  'to 656'
            634_0  COME_FROM           118  '118'

 L. 328       634  LOAD_FAST                'data'
              636  LOAD_FAST                'start_pos'
              638  LOAD_CONST               None
              640  BUILD_SLICE_2         2 
              642  BINARY_SUBSCR    
              644  LOAD_FAST                'self'
              646  STORE_ATTR               _tail

 L. 329       648  LOAD_FAST                'EMPTY'
              650  STORE_FAST               'data'

 L. 330   652_654  BREAK_LOOP          900  'to 900'
            656_0  COME_FROM           632  '632'
            656_1  COME_FROM           162  '162'
              656  JUMP_BACK            46  'to 46'
            658_0  COME_FROM            72  '72'
            658_1  COME_FROM            64  '64'

 L. 333       658  LOAD_FAST                'self'
              660  LOAD_ATTR                _payload_parser
              662  LOAD_CONST               None
              664  COMPARE_OP               is
          666_668  POP_JUMP_IF_FALSE   696  'to 696'
              670  LOAD_FAST                'self'
              672  LOAD_ATTR                _upgraded
          674_676  POP_JUMP_IF_FALSE   696  'to 696'

 L. 334       678  LOAD_FAST                'self'
              680  LOAD_ATTR                _lines
          682_684  POP_JUMP_IF_FALSE   900  'to 900'
              686  LOAD_GLOBAL              AssertionError
              688  RAISE_VARARGS_1       1  'exception instance'

 L. 335   690_692  BREAK_LOOP          900  'to 900'
              694  JUMP_BACK            46  'to 46'
            696_0  COME_FROM           674  '674'
            696_1  COME_FROM           666  '666'

 L. 338       696  LOAD_FAST                'data'
          698_700  POP_JUMP_IF_FALSE   900  'to 900'
              702  LOAD_FAST                'start_pos'
              704  LOAD_FAST                'data_len'
              706  COMPARE_OP               <
          708_710  POP_JUMP_IF_FALSE   900  'to 900'

 L. 339       712  LOAD_FAST                'self'
              714  LOAD_ATTR                _lines
          716_718  POP_JUMP_IF_FALSE   724  'to 724'
              720  LOAD_GLOBAL              AssertionError
              722  RAISE_VARARGS_1       1  'exception instance'
            724_0  COME_FROM           716  '716'

 L. 340       724  LOAD_FAST                'self'
              726  LOAD_ATTR                _payload_parser
              728  LOAD_CONST               None
              730  COMPARE_OP               is-not
          732_734  POP_JUMP_IF_TRUE    740  'to 740'
              736  LOAD_ASSERT              AssertionError
              738  RAISE_VARARGS_1       1  'exception instance'
            740_0  COME_FROM           732  '732'

 L. 341       740  SETUP_FINALLY       770  'to 770'

 L. 342       742  LOAD_FAST                'self'
              744  LOAD_ATTR                _payload_parser
              746  LOAD_METHOD              feed_data

 L. 343       748  LOAD_FAST                'data'
              750  LOAD_FAST                'start_pos'
              752  LOAD_CONST               None
              754  BUILD_SLICE_2         2 
              756  BINARY_SUBSCR    

 L. 342       758  CALL_METHOD_1         1  ''
              760  UNPACK_SEQUENCE_2     2 
              762  STORE_FAST               'eof'
              764  STORE_FAST               'data'
              766  POP_BLOCK        
              768  JUMP_FORWARD        866  'to 866'
            770_0  COME_FROM_FINALLY   740  '740'

 L. 344       770  DUP_TOP          
              772  LOAD_GLOBAL              BaseException
              774  COMPARE_OP               exception-match
          776_778  POP_JUMP_IF_FALSE   864  'to 864'
              780  POP_TOP          
              782  STORE_FAST               'exc'
              784  POP_TOP          
              786  SETUP_FINALLY       852  'to 852'

 L. 345       788  LOAD_FAST                'self'
              790  LOAD_ATTR                payload_exception
              792  LOAD_CONST               None
              794  COMPARE_OP               is-not
          796_798  POP_JUMP_IF_FALSE   826  'to 826'

 L. 346       800  LOAD_FAST                'self'
              802  LOAD_ATTR                _payload_parser
              804  LOAD_ATTR                payload
              806  LOAD_METHOD              set_exception

 L. 347       808  LOAD_FAST                'self'
              810  LOAD_METHOD              payload_exception
              812  LOAD_GLOBAL              str
              814  LOAD_FAST                'exc'
              816  CALL_FUNCTION_1       1  ''
              818  CALL_METHOD_1         1  ''

 L. 346       820  CALL_METHOD_1         1  ''
              822  POP_TOP          
              824  JUMP_FORWARD        840  'to 840'
            826_0  COME_FROM           796  '796'

 L. 349       826  LOAD_FAST                'self'
              828  LOAD_ATTR                _payload_parser
              830  LOAD_ATTR                payload
              832  LOAD_METHOD              set_exception
              834  LOAD_FAST                'exc'
              836  CALL_METHOD_1         1  ''
              838  POP_TOP          
            840_0  COME_FROM           824  '824'

 L. 351       840  LOAD_CONST               True
              842  STORE_FAST               'eof'

 L. 352       844  LOAD_CONST               b''
              846  STORE_FAST               'data'
              848  POP_BLOCK        
              850  BEGIN_FINALLY    
            852_0  COME_FROM_FINALLY   786  '786'
              852  LOAD_CONST               None
              854  STORE_FAST               'exc'
              856  DELETE_FAST              'exc'
              858  END_FINALLY      
              860  POP_EXCEPT       
              862  JUMP_FORWARD        866  'to 866'
            864_0  COME_FROM           776  '776'
              864  END_FINALLY      
            866_0  COME_FROM           862  '862'
            866_1  COME_FROM           768  '768'

 L. 354       866  LOAD_FAST                'eof'
          868_870  POP_JUMP_IF_FALSE   898  'to 898'

 L. 355       872  LOAD_CONST               0
              874  STORE_FAST               'start_pos'

 L. 356       876  LOAD_GLOBAL              len
              878  LOAD_FAST                'data'
              880  CALL_FUNCTION_1       1  ''
              882  STORE_FAST               'data_len'

 L. 357       884  LOAD_CONST               None
              886  LOAD_FAST                'self'
              888  STORE_ATTR               _payload_parser

 L. 358       890  CONTINUE             46  'to 46'
              892  JUMP_BACK            46  'to 46'

 L. 360   894_896  BREAK_LOOP          900  'to 900'
            898_0  COME_FROM           868  '868'
              898  JUMP_BACK            46  'to 46'
            900_0  COME_FROM           708  '708'
            900_1  COME_FROM           698  '698'
            900_2  COME_FROM           682  '682'
            900_3  COME_FROM            52  '52'

 L. 362       900  LOAD_FAST                'data'
          902_904  POP_JUMP_IF_FALSE   930  'to 930'
              906  LOAD_FAST                'start_pos'
              908  LOAD_FAST                'data_len'
              910  COMPARE_OP               <
          912_914  POP_JUMP_IF_FALSE   930  'to 930'

 L. 363       916  LOAD_FAST                'data'
              918  LOAD_FAST                'start_pos'
              920  LOAD_CONST               None
              922  BUILD_SLICE_2         2 
              924  BINARY_SUBSCR    
              926  STORE_FAST               'data'
              928  JUMP_FORWARD        934  'to 934'
            930_0  COME_FROM           912  '912'
            930_1  COME_FROM           902  '902'

 L. 365       930  LOAD_FAST                'EMPTY'
              932  STORE_FAST               'data'
            934_0  COME_FROM           928  '928'

 L. 367       934  LOAD_FAST                'messages'
              936  LOAD_FAST                'self'
              938  LOAD_ATTR                _upgraded
              940  LOAD_FAST                'data'
              942  BUILD_TUPLE_3         3 
              944  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 900_0

        def parse_headers(self, lines: List[bytes]) -> Tuple[('CIMultiDictProxy[str]',
 RawHeaders,
 Optional[bool],
 Optional[str],
 bool,
 bool)]:
            """Parses RFC 5322 headers from a stream.

        Line continuations are supported. Returns list of header name
        and value pairs. Header name is in upper case.
        """
            headers, raw_headers = self._headers_parser.parse_headers(lines)
            close_conn = None
            encoding = None
            upgrade = False
            chunked = False
            conn = headers.get(hdrs.CONNECTION)
            if conn:
                v = conn.lower()
                if v == 'close':
                    close_conn = True
                else:
                    if v == 'keep-alive':
                        close_conn = False
                    else:
                        if v == 'upgrade':
                            upgrade = True
            enc = headers.get(hdrs.CONTENT_ENCODING)
            if enc:
                enc = enc.lower()
                if enc in ('gzip', 'deflate', 'br'):
                    encoding = enc
            te = headers.get(hdrs.TRANSFER_ENCODING)
            if te:
                if 'chunked' in te.lower():
                    chunked = True
            return (
             headers, raw_headers, close_conn, encoding, upgrade, chunked)


    class HttpRequestParser(HttpParser):
        __doc__ = 'Read request status line. Exception .http_exceptions.BadStatusLine\n    could be raised in case of any errors in status line.\n    Returns RawRequestMessage.\n    '

        def parse_message(self, lines: List[bytes]) -> Any:
            line = lines[0].decode('utf-8', 'surrogateescape')
            try:
                method, path, version = line.split(None, 2)
            except ValueError:
                raise BadStatusLine(line) from None
            else:
                if len(path) > self.max_line_size:
                    raise LineTooLong('Status line is too long', str(self.max_line_size), str(len(path)))
                if not METHRE.match(method):
                    raise BadStatusLine(method)
                try:
                    if version.startswith('HTTP/'):
                        n1, n2 = version[5:].split('.', 1)
                        version_o = HttpVersion(int(n1), int(n2))
                    else:
                        raise BadStatusLine(version)
                except Exception:
                    raise BadStatusLine(version)
                else:
                    headers, raw_headers, close, compression, upgrade, chunked = self.parse_headers(lines)
                    if close is None:
                        if version_o <= HttpVersion10:
                            close = True
                        else:
                            close = False
                    return RawRequestMessage(method, path, version_o, headers, raw_headers, close, compression, upgrade, chunked, URL(path))


    class HttpResponseParser(HttpParser):
        __doc__ = 'Read response status line and headers.\n\n    BadStatusLine could be raised in case of any errors in status line.\n    Returns RawResponseMessage'

        def parse_message(self, lines: List[bytes]) -> Any:
            line = lines[0].decode('utf-8', 'surrogateescape')
            try:
                version, status = line.split(None, 1)
            except ValueError:
                raise BadStatusLine(line) from None
            else:
                try:
                    status, reason = status.split(None, 1)
                except ValueError:
                    reason = ''
                else:
                    if len(reason) > self.max_line_size:
                        raise LineTooLong('Status line is too long', str(self.max_line_size), str(len(reason)))
                    match = VERSRE.match(version)
                    if match is None:
                        raise BadStatusLine(line)
                    version_o = HttpVersion(int(match.group(1)), int(match.group(2)))
            try:
                status_i = int(status)
            except ValueError:
                raise BadStatusLine(line) from None
            else:
                if status_i > 999:
                    raise BadStatusLine(line)
                headers, raw_headers, close, compression, upgrade, chunked = self.parse_headers(lines)
                if close is None:
                    close = version_o <= HttpVersion10
                return RawResponseMessage(version_o, status_i, reason.strip(), headers, raw_headers, close, compression, upgrade, chunked)


    class HttpPayloadParser:

        def __init__(self, payload: StreamReader, length: Optional[int]=None, chunked: bool=False, compression: Optional[str]=None, code: Optional[int]=None, method: Optional[str]=None, readall: bool=False, response_with_body: bool=True, auto_decompress: bool=True) -> None:
            self._length = 0
            self._type = ParseState.PARSE_NONE
            self._chunk = ChunkState.PARSE_CHUNKED_SIZE
            self._chunk_size = 0
            self._chunk_tail = b''
            self._auto_decompress = auto_decompress
            self.done = False
            if response_with_body:
                if compression and self._auto_decompress:
                    real_payload = DeflateBuffer(payload, compression)
                else:
                    real_payload = payload
                self._type = response_with_body or ParseState.PARSE_NONE
                real_payload.feed_eof()
                self.done = True
            else:
                if chunked:
                    self._type = ParseState.PARSE_CHUNKED
                else:
                    if length is not None:
                        self._type = ParseState.PARSE_LENGTH
                        self._length = length
                        if self._length == 0:
                            real_payload.feed_eof()
                            self.done = True
                    elif readall and code != 204:
                        self._type = ParseState.PARSE_UNTIL_EOF
                    else:
                        if method in ('PUT', 'POST'):
                            internal_logger.warning('Content-Length or Transfer-Encoding header is required')
                            self._type = ParseState.PARSE_NONE
                            real_payload.feed_eof()
                            self.done = True
            self.payload = real_payload

        def feed_eof(self) -> None:
            if self._type == ParseState.PARSE_UNTIL_EOF:
                self.payload.feed_eof()
            else:
                if self._type == ParseState.PARSE_LENGTH:
                    raise ContentLengthError('Not enough data for satisfy content length header.')
                else:
                    if self._type == ParseState.PARSE_CHUNKED:
                        raise TransferEncodingError('Not enough data for satisfy transfer length header.')

        def feed_data--- This code section failed: ---

 L. 582         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _type
                4  LOAD_GLOBAL              ParseState
                6  LOAD_ATTR                PARSE_LENGTH
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE   142  'to 142'

 L. 583        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _length
               16  STORE_FAST               'required'

 L. 584        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'chunk'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'chunk_len'

 L. 586        26  LOAD_FAST                'required'
               28  LOAD_FAST                'chunk_len'
               30  COMPARE_OP               >=
               32  POP_JUMP_IF_FALSE    84  'to 84'

 L. 587        34  LOAD_FAST                'required'
               36  LOAD_FAST                'chunk_len'
               38  BINARY_SUBTRACT  
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _length

 L. 588        44  LOAD_FAST                'self'
               46  LOAD_ATTR                payload
               48  LOAD_METHOD              feed_data
               50  LOAD_FAST                'chunk'
               52  LOAD_FAST                'chunk_len'
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          

 L. 589        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _length
               62  LOAD_CONST               0
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   138  'to 138'

 L. 590        68  LOAD_FAST                'self'
               70  LOAD_ATTR                payload
               72  LOAD_METHOD              feed_eof
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          

 L. 591        78  LOAD_CONST               (True, b'')
               80  RETURN_VALUE     
               82  JUMP_FORWARD        780  'to 780'
             84_0  COME_FROM            32  '32'

 L. 593        84  LOAD_CONST               0
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _length

 L. 594        90  LOAD_FAST                'self'
               92  LOAD_ATTR                payload
               94  LOAD_METHOD              feed_data
               96  LOAD_FAST                'chunk'
               98  LOAD_CONST               None
              100  LOAD_FAST                'required'
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'required'
              108  CALL_METHOD_2         2  ''
              110  POP_TOP          

 L. 595       112  LOAD_FAST                'self'
              114  LOAD_ATTR                payload
              116  LOAD_METHOD              feed_eof
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          

 L. 596       122  LOAD_CONST               True
              124  LOAD_FAST                'chunk'
              126  LOAD_FAST                'required'
              128  LOAD_CONST               None
              130  BUILD_SLICE_2         2 
              132  BINARY_SUBSCR    
              134  BUILD_TUPLE_2         2 
              136  RETURN_VALUE     
            138_0  COME_FROM            66  '66'
          138_140  JUMP_FORWARD        780  'to 780'
            142_0  COME_FROM            10  '10'

 L. 599       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _type
              146  LOAD_GLOBAL              ParseState
              148  LOAD_ATTR                PARSE_CHUNKED
              150  COMPARE_OP               ==
          152_154  POP_JUMP_IF_FALSE   748  'to 748'

 L. 600       156  LOAD_FAST                'self'
              158  LOAD_ATTR                _chunk_tail
              160  POP_JUMP_IF_FALSE   178  'to 178'

 L. 601       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _chunk_tail
              166  LOAD_FAST                'chunk'
              168  BINARY_ADD       
              170  STORE_FAST               'chunk'

 L. 602       172  LOAD_CONST               b''
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _chunk_tail
            178_0  COME_FROM           686  '686'
            178_1  COME_FROM           160  '160'

 L. 604       178  LOAD_FAST                'chunk'
          180_182  POP_JUMP_IF_FALSE   780  'to 780'

 L. 607       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _chunk
              188  LOAD_GLOBAL              ChunkState
              190  LOAD_ATTR                PARSE_CHUNKED_SIZE
              192  COMPARE_OP               ==
          194_196  POP_JUMP_IF_FALSE   422  'to 422'

 L. 608       198  LOAD_FAST                'chunk'
              200  LOAD_METHOD              find
              202  LOAD_FAST                'SEP'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'pos'

 L. 609       208  LOAD_FAST                'pos'
              210  LOAD_CONST               0
              212  COMPARE_OP               >=
          214_216  POP_JUMP_IF_FALSE   412  'to 412'

 L. 610       218  LOAD_FAST                'chunk'
              220  LOAD_METHOD              find
              222  LOAD_FAST                'CHUNK_EXT'
              224  LOAD_CONST               0
              226  LOAD_FAST                'pos'
              228  CALL_METHOD_3         3  ''
              230  STORE_FAST               'i'

 L. 611       232  LOAD_FAST                'i'
              234  LOAD_CONST               0
              236  COMPARE_OP               >=
              238  POP_JUMP_IF_FALSE   254  'to 254'

 L. 612       240  LOAD_FAST                'chunk'
              242  LOAD_CONST               None
              244  LOAD_FAST                'i'
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    
              250  STORE_FAST               'size_b'
              252  JUMP_FORWARD        266  'to 266'
            254_0  COME_FROM           238  '238'

 L. 614       254  LOAD_FAST                'chunk'
              256  LOAD_CONST               None
              258  LOAD_FAST                'pos'
              260  BUILD_SLICE_2         2 
              262  BINARY_SUBSCR    
              264  STORE_FAST               'size_b'
            266_0  COME_FROM           252  '252'

 L. 616       266  SETUP_FINALLY       286  'to 286'

 L. 617       268  LOAD_GLOBAL              int
              270  LOAD_GLOBAL              bytes
              272  LOAD_FAST                'size_b'
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_CONST               16
              278  CALL_FUNCTION_2       2  ''
              280  STORE_FAST               'size'
              282  POP_BLOCK        
              284  JUMP_FORWARD        350  'to 350'
            286_0  COME_FROM_FINALLY   266  '266'

 L. 618       286  DUP_TOP          
              288  LOAD_GLOBAL              ValueError
              290  COMPARE_OP               exception-match
          292_294  POP_JUMP_IF_FALSE   348  'to 348'
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 619       302  LOAD_GLOBAL              TransferEncodingError

 L. 620       304  LOAD_FAST                'chunk'
              306  LOAD_CONST               None
              308  LOAD_FAST                'pos'
              310  BUILD_SLICE_2         2 
              312  BINARY_SUBSCR    
              314  LOAD_METHOD              decode
              316  LOAD_STR                 'ascii'
              318  LOAD_STR                 'surrogateescape'
              320  CALL_METHOD_2         2  ''

 L. 619       322  CALL_FUNCTION_1       1  ''
              324  STORE_FAST               'exc'

 L. 621       326  LOAD_FAST                'self'
              328  LOAD_ATTR                payload
              330  LOAD_METHOD              set_exception
              332  LOAD_FAST                'exc'
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          

 L. 622       338  LOAD_FAST                'exc'
              340  LOAD_CONST               None
              342  RAISE_VARARGS_2       2  'exception instance with __cause__'
              344  POP_EXCEPT       
              346  JUMP_FORWARD        350  'to 350'
            348_0  COME_FROM           292  '292'
              348  END_FINALLY      
            350_0  COME_FROM           346  '346'
            350_1  COME_FROM           284  '284'

 L. 624       350  LOAD_FAST                'chunk'
              352  LOAD_FAST                'pos'
              354  LOAD_CONST               2
              356  BINARY_ADD       
              358  LOAD_CONST               None
              360  BUILD_SLICE_2         2 
              362  BINARY_SUBSCR    
              364  STORE_FAST               'chunk'

 L. 625       366  LOAD_FAST                'size'
              368  LOAD_CONST               0
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   386  'to 386'

 L. 626       376  LOAD_GLOBAL              ChunkState
              378  LOAD_ATTR                PARSE_MAYBE_TRAILERS
              380  LOAD_FAST                'self'
              382  STORE_ATTR               _chunk
              384  JUMP_FORWARD        410  'to 410'
            386_0  COME_FROM           372  '372'

 L. 628       386  LOAD_GLOBAL              ChunkState
              388  LOAD_ATTR                PARSE_CHUNKED_CHUNK
              390  LOAD_FAST                'self'
              392  STORE_ATTR               _chunk

 L. 629       394  LOAD_FAST                'size'
              396  LOAD_FAST                'self'
              398  STORE_ATTR               _chunk_size

 L. 630       400  LOAD_FAST                'self'
              402  LOAD_ATTR                payload
              404  LOAD_METHOD              begin_http_chunk_receiving
              406  CALL_METHOD_0         0  ''
              408  POP_TOP          
            410_0  COME_FROM           384  '384'
              410  JUMP_FORWARD        422  'to 422'
            412_0  COME_FROM           214  '214'

 L. 632       412  LOAD_FAST                'chunk'
              414  LOAD_FAST                'self'
              416  STORE_ATTR               _chunk_tail

 L. 633       418  LOAD_CONST               (False, b'')
              420  RETURN_VALUE     
            422_0  COME_FROM           410  '410'
            422_1  COME_FROM           194  '194'

 L. 636       422  LOAD_FAST                'self'
              424  LOAD_ATTR                _chunk
              426  LOAD_GLOBAL              ChunkState
              428  LOAD_ATTR                PARSE_CHUNKED_CHUNK
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   546  'to 546'

 L. 637       436  LOAD_FAST                'self'
              438  LOAD_ATTR                _chunk_size
              440  STORE_FAST               'required'

 L. 638       442  LOAD_GLOBAL              len
              444  LOAD_FAST                'chunk'
              446  CALL_FUNCTION_1       1  ''
              448  STORE_FAST               'chunk_len'

 L. 640       450  LOAD_FAST                'required'
              452  LOAD_FAST                'chunk_len'
              454  COMPARE_OP               >
          456_458  POP_JUMP_IF_FALSE   488  'to 488'

 L. 641       460  LOAD_FAST                'required'
              462  LOAD_FAST                'chunk_len'
              464  BINARY_SUBTRACT  
              466  LOAD_FAST                'self'
              468  STORE_ATTR               _chunk_size

 L. 642       470  LOAD_FAST                'self'
              472  LOAD_ATTR                payload
              474  LOAD_METHOD              feed_data
              476  LOAD_FAST                'chunk'
              478  LOAD_FAST                'chunk_len'
              480  CALL_METHOD_2         2  ''
              482  POP_TOP          

 L. 643       484  LOAD_CONST               (False, b'')
              486  RETURN_VALUE     
            488_0  COME_FROM           456  '456'

 L. 645       488  LOAD_CONST               0
              490  LOAD_FAST                'self'
              492  STORE_ATTR               _chunk_size

 L. 646       494  LOAD_FAST                'self'
              496  LOAD_ATTR                payload
              498  LOAD_METHOD              feed_data
              500  LOAD_FAST                'chunk'
              502  LOAD_CONST               None
              504  LOAD_FAST                'required'
              506  BUILD_SLICE_2         2 
              508  BINARY_SUBSCR    
              510  LOAD_FAST                'required'
              512  CALL_METHOD_2         2  ''
              514  POP_TOP          

 L. 647       516  LOAD_FAST                'chunk'
              518  LOAD_FAST                'required'
              520  LOAD_CONST               None
              522  BUILD_SLICE_2         2 
              524  BINARY_SUBSCR    
              526  STORE_FAST               'chunk'

 L. 648       528  LOAD_GLOBAL              ChunkState
              530  LOAD_ATTR                PARSE_CHUNKED_CHUNK_EOF
              532  LOAD_FAST                'self'
              534  STORE_ATTR               _chunk

 L. 649       536  LOAD_FAST                'self'
              538  LOAD_ATTR                payload
              540  LOAD_METHOD              end_http_chunk_receiving
              542  CALL_METHOD_0         0  ''
              544  POP_TOP          
            546_0  COME_FROM           432  '432'

 L. 652       546  LOAD_FAST                'self'
              548  LOAD_ATTR                _chunk
              550  LOAD_GLOBAL              ChunkState
              552  LOAD_ATTR                PARSE_CHUNKED_CHUNK_EOF
              554  COMPARE_OP               ==
          556_558  POP_JUMP_IF_FALSE   610  'to 610'

 L. 653       560  LOAD_FAST                'chunk'
              562  LOAD_CONST               None
              564  LOAD_CONST               2
              566  BUILD_SLICE_2         2 
              568  BINARY_SUBSCR    
              570  LOAD_FAST                'SEP'
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   600  'to 600'

 L. 654       578  LOAD_FAST                'chunk'
              580  LOAD_CONST               2
              582  LOAD_CONST               None
              584  BUILD_SLICE_2         2 
              586  BINARY_SUBSCR    
              588  STORE_FAST               'chunk'

 L. 655       590  LOAD_GLOBAL              ChunkState
              592  LOAD_ATTR                PARSE_CHUNKED_SIZE
              594  LOAD_FAST                'self'
              596  STORE_ATTR               _chunk
              598  JUMP_FORWARD        610  'to 610'
            600_0  COME_FROM           574  '574'

 L. 657       600  LOAD_FAST                'chunk'
              602  LOAD_FAST                'self'
              604  STORE_ATTR               _chunk_tail

 L. 658       606  LOAD_CONST               (False, b'')
              608  RETURN_VALUE     
            610_0  COME_FROM           598  '598'
            610_1  COME_FROM           556  '556'

 L. 663       610  LOAD_FAST                'self'
              612  LOAD_ATTR                _chunk
              614  LOAD_GLOBAL              ChunkState
              616  LOAD_ATTR                PARSE_MAYBE_TRAILERS
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_FALSE   676  'to 676'

 L. 664       624  LOAD_FAST                'chunk'
              626  LOAD_CONST               None
              628  LOAD_CONST               2
              630  BUILD_SLICE_2         2 
              632  BINARY_SUBSCR    
              634  LOAD_FAST                'SEP'
              636  COMPARE_OP               ==
          638_640  POP_JUMP_IF_FALSE   668  'to 668'

 L. 666       642  LOAD_FAST                'self'
              644  LOAD_ATTR                payload
              646  LOAD_METHOD              feed_eof
              648  CALL_METHOD_0         0  ''
              650  POP_TOP          

 L. 667       652  LOAD_CONST               True
              654  LOAD_FAST                'chunk'
              656  LOAD_CONST               2
              658  LOAD_CONST               None
              660  BUILD_SLICE_2         2 
              662  BINARY_SUBSCR    
              664  BUILD_TUPLE_2         2 
              666  RETURN_VALUE     
            668_0  COME_FROM           638  '638'

 L. 669       668  LOAD_GLOBAL              ChunkState
              670  LOAD_ATTR                PARSE_TRAILERS
              672  LOAD_FAST                'self'
              674  STORE_ATTR               _chunk
            676_0  COME_FROM           620  '620'

 L. 672       676  LOAD_FAST                'self'
              678  LOAD_ATTR                _chunk
              680  LOAD_GLOBAL              ChunkState
              682  LOAD_ATTR                PARSE_TRAILERS
              684  COMPARE_OP               ==
              686  POP_JUMP_IF_FALSE   178  'to 178'

 L. 673       688  LOAD_FAST                'chunk'
              690  LOAD_METHOD              find
              692  LOAD_FAST                'SEP'
              694  CALL_METHOD_1         1  ''
              696  STORE_FAST               'pos'

 L. 674       698  LOAD_FAST                'pos'
              700  LOAD_CONST               0
              702  COMPARE_OP               >=
          704_706  POP_JUMP_IF_FALSE   734  'to 734'

 L. 675       708  LOAD_FAST                'chunk'
              710  LOAD_FAST                'pos'
              712  LOAD_CONST               2
              714  BINARY_ADD       
              716  LOAD_CONST               None
              718  BUILD_SLICE_2         2 
              720  BINARY_SUBSCR    
            722_0  COME_FROM            82  '82'
              722  STORE_FAST               'chunk'

 L. 676       724  LOAD_GLOBAL              ChunkState
              726  LOAD_ATTR                PARSE_MAYBE_TRAILERS
              728  LOAD_FAST                'self'
              730  STORE_ATTR               _chunk
              732  JUMP_BACK           178  'to 178'
            734_0  COME_FROM           704  '704'

 L. 678       734  LOAD_FAST                'chunk'
              736  LOAD_FAST                'self'
              738  STORE_ATTR               _chunk_tail

 L. 679       740  LOAD_CONST               (False, b'')
              742  RETURN_VALUE     
              744  JUMP_BACK           178  'to 178'
              746  JUMP_FORWARD        780  'to 780'
            748_0  COME_FROM           152  '152'

 L. 682       748  LOAD_FAST                'self'
              750  LOAD_ATTR                _type
              752  LOAD_GLOBAL              ParseState
              754  LOAD_ATTR                PARSE_UNTIL_EOF
              756  COMPARE_OP               ==
          758_760  POP_JUMP_IF_FALSE   780  'to 780'

 L. 683       762  LOAD_FAST                'self'
              764  LOAD_ATTR                payload
              766  LOAD_METHOD              feed_data
              768  LOAD_FAST                'chunk'
              770  LOAD_GLOBAL              len
              772  LOAD_FAST                'chunk'
              774  CALL_FUNCTION_1       1  ''
              776  CALL_METHOD_2         2  ''
              778  POP_TOP          
            780_0  COME_FROM           758  '758'
            780_1  COME_FROM           746  '746'
            780_2  COME_FROM           180  '180'
            780_3  COME_FROM           138  '138'

 L. 685       780  LOAD_CONST               (False, b'')
              782  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 722


    class DeflateBuffer:
        __doc__ = 'DeflateStream decompress stream and feed data into specified stream.'

        def __init__(self, out: StreamReader, encoding: Optional[str]) -> None:
            self.out = out
            self.size = 0
            self.encoding = encoding
            self._started_decoding = False
            if encoding == 'br':
                if not HAS_BROTLI:
                    raise ContentEncodingError('Can not decode content-encoding: brotli (br). Please install `brotlipy`')
                self.decompressor = brotli.Decompressor()
            else:
                zlib_mode = 16 + zlib.MAX_WBITS if encoding == 'gzip' else -zlib.MAX_WBITS
                self.decompressor = zlib.decompressobj(wbits=zlib_mode)

        def set_exception(self, exc: BaseException) -> None:
            self.out.set_exception(exc)

        def feed_data(self, chunk: bytes, size: int) -> None:
            self.size += size
            try:
                chunk = self.decompressor.decompress(chunk)
            except Exception:
                if (self._started_decoding or self.encoding) == 'deflate':
                    self.decompressor = zlib.decompressobj()
                    try:
                        chunk = self.decompressor.decompress(chunk)
                    except Exception:
                        raise ContentEncodingError('Can not decode content-encoding: %s' % self.encoding)

                else:
                    raise ContentEncodingError('Can not decode content-encoding: %s' % self.encoding)
            else:
                if chunk:
                    self._started_decoding = True
                    self.out.feed_data(chunk, len(chunk))

        def feed_eof(self) -> None:
            chunk = self.decompressor.flush()
            if chunk or self.size > 0:
                self.out.feed_data(chunk, len(chunk))
                if self.encoding == 'deflate':
                    if not self.decompressor.eof:
                        raise ContentEncodingError('deflate')
            self.out.feed_eof()

        def begin_http_chunk_receiving(self) -> None:
            self.out.begin_http_chunk_receiving()

        def end_http_chunk_receiving(self) -> None:
            self.out.end_http_chunk_receiving()


    HttpRequestParserPy = HttpRequestParser
    HttpResponseParserPy = HttpResponseParser
    RawRequestMessagePy = RawRequestMessage
    RawResponseMessagePy = RawResponseMessage
try:
    if not NO_EXTENSIONS:
        from ._http_parser import HttpRequestParser, HttpResponseParser, RawRequestMessage, RawResponseMessage
        HttpRequestParserC = HttpRequestParser
        HttpResponseParserC = HttpResponseParser
        RawRequestMessageC = RawRequestMessage
        RawResponseMessageC = RawResponseMessage
except ImportError:
    pass