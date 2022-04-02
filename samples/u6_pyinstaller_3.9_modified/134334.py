# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\multipart.py
import base64, binascii, json, re, uuid, warnings, zlib
from collections import deque
from types import TracebackType
from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, Union
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

 L.  74         0  LOAD_GLOBAL              str
                2  LOAD_GLOBAL              bool
                4  LOAD_CONST               ('string', 'return')
                6  BUILD_CONST_KEY_MAP_2     2 
                8  LOAD_CODE                <code_object is_token>
               10  LOAD_STR                 'parse_content_disposition.<locals>.is_token'
               12  MAKE_FUNCTION_4          'annotation'
               14  STORE_DEREF              'is_token'

 L.  77        16  LOAD_GLOBAL              str
               18  LOAD_GLOBAL              bool
               20  LOAD_CONST               ('string', 'return')
               22  BUILD_CONST_KEY_MAP_2     2 
               24  LOAD_CODE                <code_object is_quoted>
               26  LOAD_STR                 'parse_content_disposition.<locals>.is_quoted'
               28  MAKE_FUNCTION_4          'annotation'
               30  STORE_FAST               'is_quoted'

 L.  80        32  LOAD_GLOBAL              str
               34  LOAD_GLOBAL              bool
               36  LOAD_CONST               ('string', 'return')
               38  BUILD_CONST_KEY_MAP_2     2 
               40  LOAD_CLOSURE             'is_token'
               42  BUILD_TUPLE_1         1 
               44  LOAD_CODE                <code_object is_rfc5987>
               46  LOAD_STR                 'parse_content_disposition.<locals>.is_rfc5987'
               48  MAKE_FUNCTION_12         'annotation, closure'
               50  STORE_FAST               'is_rfc5987'

 L.  83        52  LOAD_GLOBAL              str
               54  LOAD_GLOBAL              bool
               56  LOAD_CONST               ('string', 'return')
               58  BUILD_CONST_KEY_MAP_2     2 
               60  LOAD_CODE                <code_object is_extended_param>
               62  LOAD_STR                 'parse_content_disposition.<locals>.is_extended_param'
               64  MAKE_FUNCTION_4          'annotation'
               66  STORE_FAST               'is_extended_param'

 L.  86        68  LOAD_GLOBAL              str
               70  LOAD_GLOBAL              bool
               72  LOAD_CONST               ('string', 'return')
               74  BUILD_CONST_KEY_MAP_2     2 
               76  LOAD_CODE                <code_object is_continuous_param>
               78  LOAD_STR                 'parse_content_disposition.<locals>.is_continuous_param'
               80  MAKE_FUNCTION_4          'annotation'
               82  STORE_FAST               'is_continuous_param'

 L.  93        84  LOAD_STR                 ''
               86  LOAD_METHOD              join
               88  LOAD_GLOBAL              map
               90  LOAD_GLOBAL              re
               92  LOAD_ATTR                escape
               94  LOAD_GLOBAL              CHAR
               96  CALL_FUNCTION_2       2  ''
               98  CALL_METHOD_1         1  ''
              100  LOAD_CONST               ('chars',)
              102  BUILD_CONST_KEY_MAP_1     1 
              104  LOAD_GLOBAL              str
              106  LOAD_GLOBAL              str
              108  LOAD_GLOBAL              str
              110  LOAD_CONST               ('text', 'chars', 'return')
              112  BUILD_CONST_KEY_MAP_3     3 
              114  LOAD_CODE                <code_object unescape>
              116  LOAD_STR                 'parse_content_disposition.<locals>.unescape'
              118  MAKE_FUNCTION_6          'keyword-only, annotation'
              120  STORE_FAST               'unescape'

 L.  96       122  LOAD_FAST                'header'
              124  POP_JUMP_IF_TRUE    134  'to 134'

 L.  97       126  LOAD_CONST               None
              128  BUILD_MAP_0           0 
              130  BUILD_TUPLE_2         2 
              132  RETURN_VALUE     
            134_0  COME_FROM           124  '124'

 L.  99       134  LOAD_FAST                'header'
              136  LOAD_METHOD              split
              138  LOAD_STR                 ';'
              140  CALL_METHOD_1         1  ''
              142  UNPACK_EX_1+0           
              144  STORE_FAST               'disptype'
              146  STORE_FAST               'parts'

 L. 100       148  LOAD_DEREF               'is_token'
              150  LOAD_FAST                'disptype'
              152  CALL_FUNCTION_1       1  ''
              154  POP_JUMP_IF_TRUE    178  'to 178'

 L. 101       156  LOAD_GLOBAL              warnings
              158  LOAD_METHOD              warn
              160  LOAD_GLOBAL              BadContentDispositionHeader
              162  LOAD_FAST                'header'
              164  CALL_FUNCTION_1       1  ''
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 102       170  LOAD_CONST               None
              172  BUILD_MAP_0           0 
              174  BUILD_TUPLE_2         2 
              176  RETURN_VALUE     
            178_0  COME_FROM           154  '154'

 L. 104       178  BUILD_MAP_0           0 
              180  STORE_FAST               'params'

 L. 105       182  LOAD_FAST                'parts'
          184_186  POP_JUMP_IF_FALSE   682  'to 682'

 L. 106       188  LOAD_FAST                'parts'
              190  LOAD_METHOD              pop
              192  LOAD_CONST               0
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'item'

 L. 108       198  LOAD_STR                 '='
              200  LOAD_FAST                'item'
              202  <118>                 1  ''
              204  POP_JUMP_IF_FALSE   228  'to 228'

 L. 109       206  LOAD_GLOBAL              warnings
              208  LOAD_METHOD              warn
              210  LOAD_GLOBAL              BadContentDispositionHeader
              212  LOAD_FAST                'header'
              214  CALL_FUNCTION_1       1  ''
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 110       220  LOAD_CONST               None
              222  BUILD_MAP_0           0 
              224  BUILD_TUPLE_2         2 
              226  RETURN_VALUE     
            228_0  COME_FROM           204  '204'

 L. 112       228  LOAD_FAST                'item'
              230  LOAD_METHOD              split
              232  LOAD_STR                 '='
              234  LOAD_CONST               1
              236  CALL_METHOD_2         2  ''
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'key'
              242  STORE_FAST               'value'

 L. 113       244  LOAD_FAST                'key'
              246  LOAD_METHOD              lower
              248  CALL_METHOD_0         0  ''
              250  LOAD_METHOD              strip
              252  CALL_METHOD_0         0  ''
              254  STORE_FAST               'key'

 L. 114       256  LOAD_FAST                'value'
              258  LOAD_METHOD              lstrip
              260  CALL_METHOD_0         0  ''
              262  STORE_FAST               'value'

 L. 116       264  LOAD_FAST                'key'
              266  LOAD_FAST                'params'
              268  <118>                 0  ''
          270_272  POP_JUMP_IF_FALSE   296  'to 296'

 L. 117       274  LOAD_GLOBAL              warnings
              276  LOAD_METHOD              warn
              278  LOAD_GLOBAL              BadContentDispositionHeader
              280  LOAD_FAST                'header'
              282  CALL_FUNCTION_1       1  ''
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 118       288  LOAD_CONST               None
              290  BUILD_MAP_0           0 
              292  BUILD_TUPLE_2         2 
              294  RETURN_VALUE     
            296_0  COME_FROM           270  '270'

 L. 120       296  LOAD_DEREF               'is_token'
              298  LOAD_FAST                'key'
              300  CALL_FUNCTION_1       1  ''
          302_304  POP_JUMP_IF_TRUE    326  'to 326'

 L. 121       306  LOAD_GLOBAL              warnings
              308  LOAD_METHOD              warn
              310  LOAD_GLOBAL              BadContentDispositionParam
              312  LOAD_FAST                'item'
              314  CALL_FUNCTION_1       1  ''
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 122       320  JUMP_BACK           182  'to 182'
          322_324  JUMP_FORWARD        672  'to 672'
            326_0  COME_FROM           302  '302'

 L. 124       326  LOAD_FAST                'is_continuous_param'
              328  LOAD_FAST                'key'
              330  CALL_FUNCTION_1       1  ''
          332_334  POP_JUMP_IF_FALSE   394  'to 394'

 L. 125       336  LOAD_FAST                'is_quoted'
              338  LOAD_FAST                'value'
              340  CALL_FUNCTION_1       1  ''
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L. 126       346  LOAD_FAST                'unescape'
              348  LOAD_FAST                'value'
              350  LOAD_CONST               1
              352  LOAD_CONST               -1
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  CALL_FUNCTION_1       1  ''
              360  STORE_FAST               'value'
              362  JUMP_FORWARD        672  'to 672'
            364_0  COME_FROM           342  '342'

 L. 127       364  LOAD_DEREF               'is_token'
              366  LOAD_FAST                'value'
              368  CALL_FUNCTION_1       1  ''
          370_372  POP_JUMP_IF_TRUE    672  'to 672'

 L. 128       374  LOAD_GLOBAL              warnings
              376  LOAD_METHOD              warn
              378  LOAD_GLOBAL              BadContentDispositionParam
              380  LOAD_FAST                'item'
              382  CALL_FUNCTION_1       1  ''
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          

 L. 129       388  JUMP_BACK           182  'to 182'
          390_392  JUMP_FORWARD        672  'to 672'
            394_0  COME_FROM           332  '332'

 L. 131       394  LOAD_FAST                'is_extended_param'
              396  LOAD_FAST                'key'
              398  CALL_FUNCTION_1       1  ''
          400_402  POP_JUMP_IF_FALSE   518  'to 518'

 L. 132       404  LOAD_FAST                'is_rfc5987'
              406  LOAD_FAST                'value'
              408  CALL_FUNCTION_1       1  ''
          410_412  POP_JUMP_IF_FALSE   444  'to 444'

 L. 133       414  LOAD_FAST                'value'
              416  LOAD_METHOD              split
              418  LOAD_STR                 "'"
              420  LOAD_CONST               2
              422  CALL_METHOD_2         2  ''
              424  UNPACK_SEQUENCE_3     3 
              426  STORE_FAST               'encoding'
              428  STORE_FAST               '_'
              430  STORE_FAST               'value'

 L. 134       432  LOAD_FAST                'encoding'
          434_436  JUMP_IF_TRUE_OR_POP   440  'to 440'
              438  LOAD_STR                 'utf-8'
            440_0  COME_FROM           434  '434'
              440  STORE_FAST               'encoding'
              442  JUMP_FORWARD        460  'to 460'
            444_0  COME_FROM           410  '410'

 L. 136       444  LOAD_GLOBAL              warnings
              446  LOAD_METHOD              warn
              448  LOAD_GLOBAL              BadContentDispositionParam
              450  LOAD_FAST                'item'
              452  CALL_FUNCTION_1       1  ''
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          

 L. 137       458  JUMP_BACK           182  'to 182'
            460_0  COME_FROM           442  '442'

 L. 139       460  SETUP_FINALLY       478  'to 478'

 L. 140       462  LOAD_GLOBAL              unquote
              464  LOAD_FAST                'value'
              466  LOAD_FAST                'encoding'
              468  LOAD_STR                 'strict'
              470  CALL_FUNCTION_3       3  ''
              472  STORE_FAST               'value'
              474  POP_BLOCK        
              476  JUMP_FORWARD        516  'to 516'
            478_0  COME_FROM_FINALLY   460  '460'

 L. 141       478  DUP_TOP          
              480  LOAD_GLOBAL              UnicodeDecodeError
          482_484  <121>               514  ''
              486  POP_TOP          
              488  POP_TOP          
              490  POP_TOP          

 L. 142       492  LOAD_GLOBAL              warnings
              494  LOAD_METHOD              warn
              496  LOAD_GLOBAL              BadContentDispositionParam
              498  LOAD_FAST                'item'
              500  CALL_FUNCTION_1       1  ''
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          

 L. 143       506  POP_EXCEPT       
              508  JUMP_BACK           182  'to 182'
              510  POP_EXCEPT       
              512  JUMP_FORWARD        516  'to 516'
              514  <48>             
            516_0  COME_FROM           512  '512'
            516_1  COME_FROM           476  '476'
              516  JUMP_FORWARD        672  'to 672'
            518_0  COME_FROM           400  '400'

 L. 146       518  LOAD_CONST               True
              520  STORE_FAST               'failed'

 L. 147       522  LOAD_FAST                'is_quoted'
              524  LOAD_FAST                'value'
              526  CALL_FUNCTION_1       1  ''
          528_530  POP_JUMP_IF_FALSE   560  'to 560'

 L. 148       532  LOAD_CONST               False
              534  STORE_FAST               'failed'

 L. 149       536  LOAD_FAST                'unescape'
              538  LOAD_FAST                'value'
              540  LOAD_CONST               1
              542  LOAD_CONST               -1
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  LOAD_METHOD              lstrip
              550  LOAD_STR                 '\\/'
              552  CALL_METHOD_1         1  ''
              554  CALL_FUNCTION_1       1  ''
              556  STORE_FAST               'value'
              558  JUMP_FORWARD        644  'to 644'
            560_0  COME_FROM           528  '528'

 L. 150       560  LOAD_DEREF               'is_token'
              562  LOAD_FAST                'value'
              564  CALL_FUNCTION_1       1  ''
          566_568  POP_JUMP_IF_FALSE   576  'to 576'

 L. 151       570  LOAD_CONST               False
              572  STORE_FAST               'failed'
              574  JUMP_FORWARD        644  'to 644'
            576_0  COME_FROM           566  '566'

 L. 152       576  LOAD_FAST                'parts'
          578_580  POP_JUMP_IF_FALSE   644  'to 644'

 L. 155       582  LOAD_STR                 '{};{}'
              584  LOAD_METHOD              format
              586  LOAD_FAST                'value'
              588  LOAD_FAST                'parts'
              590  LOAD_CONST               0
              592  BINARY_SUBSCR    
              594  CALL_METHOD_2         2  ''
              596  STORE_FAST               '_value'

 L. 156       598  LOAD_FAST                'is_quoted'
              600  LOAD_FAST                '_value'
              602  CALL_FUNCTION_1       1  ''
          604_606  POP_JUMP_IF_FALSE   644  'to 644'

 L. 157       608  LOAD_FAST                'parts'
              610  LOAD_METHOD              pop
              612  LOAD_CONST               0
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          

 L. 158       618  LOAD_FAST                'unescape'
              620  LOAD_FAST                '_value'
              622  LOAD_CONST               1
              624  LOAD_CONST               -1
              626  BUILD_SLICE_2         2 
              628  BINARY_SUBSCR    
              630  LOAD_METHOD              lstrip
              632  LOAD_STR                 '\\/'
              634  CALL_METHOD_1         1  ''
              636  CALL_FUNCTION_1       1  ''
              638  STORE_FAST               'value'

 L. 159       640  LOAD_CONST               False
            642_0  COME_FROM           362  '362'
              642  STORE_FAST               'failed'
            644_0  COME_FROM           604  '604'
            644_1  COME_FROM           578  '578'
            644_2  COME_FROM           574  '574'
            644_3  COME_FROM           558  '558'

 L. 161       644  LOAD_FAST                'failed'
          646_648  POP_JUMP_IF_FALSE   672  'to 672'

 L. 162       650  LOAD_GLOBAL              warnings
              652  LOAD_METHOD              warn
              654  LOAD_GLOBAL              BadContentDispositionHeader
              656  LOAD_FAST                'header'
              658  CALL_FUNCTION_1       1  ''
              660  CALL_METHOD_1         1  ''
              662  POP_TOP          

 L. 163       664  LOAD_CONST               None
              666  BUILD_MAP_0           0 
              668  BUILD_TUPLE_2         2 
              670  RETURN_VALUE     
            672_0  COME_FROM           646  '646'
            672_1  COME_FROM           516  '516'
            672_2  COME_FROM           390  '390'
            672_3  COME_FROM           370  '370'
            672_4  COME_FROM           322  '322'

 L. 165       672  LOAD_FAST                'value'
              674  LOAD_FAST                'params'
              676  LOAD_FAST                'key'
              678  STORE_SUBSCR     
              680  JUMP_BACK           182  'to 182'
            682_0  COME_FROM           184  '184'

 L. 167       682  LOAD_FAST                'disptype'
              684  LOAD_METHOD              lower
              686  CALL_METHOD_0         0  ''
              688  LOAD_FAST                'params'
              690  BUILD_TUPLE_2         2 
              692  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 202


def content_disposition_filename--- This code section failed: ---

 L. 173         0  LOAD_STR                 '%s*'
                2  LOAD_FAST                'name'
                4  BINARY_MODULO    
                6  STORE_DEREF              'name_suf'

 L. 174         8  LOAD_FAST                'params'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L. 175        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 176        16  LOAD_DEREF               'name_suf'
               18  LOAD_FAST                'params'
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 177        24  LOAD_FAST                'params'
               26  LOAD_DEREF               'name_suf'
               28  BINARY_SUBSCR    
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L. 178        32  LOAD_FAST                'name'
               34  LOAD_FAST                'params'
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 179        40  LOAD_FAST                'params'
               42  LOAD_FAST                'name'
               44  BINARY_SUBSCR    
               46  RETURN_VALUE     
             48_0  COME_FROM            38  '38'

 L. 181        48  BUILD_LIST_0          0 
               50  STORE_FAST               'parts'

 L. 182        52  LOAD_GLOBAL              sorted
               54  LOAD_CLOSURE             'name_suf'
               56  BUILD_TUPLE_1         1 
               58  LOAD_GENEXPR             '<code_object <genexpr>>'
               60  LOAD_STR                 'content_disposition_filename.<locals>.<genexpr>'
               62  MAKE_FUNCTION_8          'closure'

 L. 183        64  LOAD_FAST                'params'
               66  LOAD_METHOD              items
               68  CALL_METHOD_0         0  ''

 L. 182        70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'fnparams'

 L. 185        78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'fnparams'
               82  CALL_FUNCTION_1       1  ''
               84  GET_ITER         
               86  FOR_ITER            166  'to 166'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'num'
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'key'
               96  STORE_FAST               'value'

 L. 186        98  LOAD_FAST                'key'
              100  LOAD_METHOD              split
              102  LOAD_STR                 '*'
              104  LOAD_CONST               1
              106  CALL_METHOD_2         2  ''
              108  UNPACK_SEQUENCE_2     2 
              110  STORE_FAST               '_'
              112  STORE_FAST               'tail'

 L. 187       114  LOAD_FAST                'tail'
              116  LOAD_METHOD              endswith
              118  LOAD_STR                 '*'
              120  CALL_METHOD_1         1  ''
              122  POP_JUMP_IF_FALSE   136  'to 136'

 L. 188       124  LOAD_FAST                'tail'
              126  LOAD_CONST               None
              128  LOAD_CONST               -1
              130  BUILD_SLICE_2         2 
              132  BINARY_SUBSCR    
              134  STORE_FAST               'tail'
            136_0  COME_FROM           122  '122'

 L. 189       136  LOAD_FAST                'tail'
              138  LOAD_GLOBAL              str
              140  LOAD_FAST                'num'
              142  CALL_FUNCTION_1       1  ''
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   160  'to 160'

 L. 190       148  LOAD_FAST                'parts'
              150  LOAD_METHOD              append
              152  LOAD_FAST                'value'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  JUMP_BACK            86  'to 86'
            160_0  COME_FROM           146  '146'

 L. 192       160  POP_TOP          
              162  BREAK_LOOP          166  'to 166'
              164  JUMP_BACK            86  'to 86'

 L. 193       166  LOAD_FAST                'parts'
              168  POP_JUMP_IF_TRUE    174  'to 174'

 L. 194       170  LOAD_CONST               None
              172  RETURN_VALUE     
            174_0  COME_FROM           168  '168'

 L. 195       174  LOAD_STR                 ''
              176  LOAD_METHOD              join
              178  LOAD_FAST                'parts'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'value'

 L. 196       184  LOAD_STR                 "'"
              186  LOAD_FAST                'value'
              188  <118>                 0  ''
              190  POP_JUMP_IF_FALSE   230  'to 230'

 L. 197       192  LOAD_FAST                'value'
              194  LOAD_METHOD              split
              196  LOAD_STR                 "'"
              198  LOAD_CONST               2
              200  CALL_METHOD_2         2  ''
              202  UNPACK_SEQUENCE_3     3 
              204  STORE_FAST               'encoding'
              206  STORE_FAST               '_'
              208  STORE_FAST               'value'

 L. 198       210  LOAD_FAST                'encoding'
              212  JUMP_IF_TRUE_OR_POP   216  'to 216'
              214  LOAD_STR                 'utf-8'
            216_0  COME_FROM           212  '212'
              216  STORE_FAST               'encoding'

 L. 199       218  LOAD_GLOBAL              unquote
              220  LOAD_FAST                'value'
              222  LOAD_FAST                'encoding'
              224  LOAD_STR                 'strict'
              226  CALL_FUNCTION_3       3  ''
              228  RETURN_VALUE     
            230_0  COME_FROM           190  '190'

 L. 200       230  LOAD_FAST                'value'
              232  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 20


class MultipartResponseWrapper:
    __doc__ = 'Wrapper around the MultipartReader.\n\n    It takes care about\n    underlying connection and close it when it needs in.\n    '

    def __init__(self, resp: 'ClientResponse', stream: 'MultipartReader') -> None:
        self.resp = resp
        self.stream = stream

    def __aiter__(self) -> 'MultipartResponseWrapper':
        return self

    async def __anext__--- This code section failed: ---

 L. 224         0  LOAD_FAST                'self'
                2  LOAD_METHOD              next
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'part'

 L. 225        14  LOAD_FAST                'part'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 226        22  LOAD_GLOBAL              StopAsyncIteration
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 227        26  LOAD_FAST                'part'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

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

    def __init__--- This code section failed: ---

 L. 256         0  LOAD_FAST                'headers'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               headers

 L. 257         6  LOAD_FAST                'boundary'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _boundary

 L. 258        12  LOAD_FAST                'content'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _content

 L. 259        18  LOAD_CONST               False
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _at_eof

 L. 260        24  LOAD_FAST                'self'
               26  LOAD_ATTR                headers
               28  LOAD_METHOD              get
               30  LOAD_GLOBAL              CONTENT_LENGTH
               32  LOAD_CONST               None
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'length'

 L. 261        38  LOAD_FAST                'length'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'
               46  LOAD_GLOBAL              int
               48  LOAD_FAST                'length'
               50  CALL_FUNCTION_1       1  ''
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            44  '44'
               54  LOAD_CONST               None
             56_0  COME_FROM            52  '52'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _length

 L. 262        60  LOAD_CONST               0
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _read_bytes

 L. 264        66  LOAD_GLOBAL              deque
               68  CALL_FUNCTION_0       0  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _unread

 L. 265        74  LOAD_CONST               None
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _prev_chunk

 L. 266        80  LOAD_CONST               0
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _content_eof

 L. 267        86  BUILD_MAP_0           0 
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _cache

Parse error at or near `<117>' instruction at offset 42

    def __aiter__(self) -> AsyncIterator['BodyPartReader']:
        return self

    async def __anext__--- This code section failed: ---

 L. 273         0  LOAD_FAST                'self'
                2  LOAD_METHOD              next
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'part'

 L. 274        14  LOAD_FAST                'part'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 275        22  LOAD_GLOBAL              StopAsyncIteration
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 276        26  LOAD_FAST                'part'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

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
        else:
            data = bytearray
            while True:
                if not self._at_eof:
                    data.extend(await self.read_chunkself.chunk_size)

        if decode:
            return self.decodedata
        return data

    async def read_chunk--- This code section failed: ---

 L. 305         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _at_eof
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 306         6  LOAD_CONST               b''
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 307        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _length
               14  POP_JUMP_IF_FALSE    34  'to 34'

 L. 308        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _read_chunk_from_length
               20  LOAD_FAST                'size'
               22  CALL_METHOD_1         1  ''
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  STORE_FAST               'chunk'
               32  JUMP_FORWARD         50  'to 50'
             34_0  COME_FROM            14  '14'

 L. 310        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _read_chunk_from_stream
               38  LOAD_FAST                'size'
               40  CALL_METHOD_1         1  ''
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  STORE_FAST               'chunk'
             50_0  COME_FROM            32  '32'

 L. 312        50  LOAD_FAST                'self'
               52  DUP_TOP          
               54  LOAD_ATTR                _read_bytes
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'chunk'
               60  CALL_FUNCTION_1       1  ''
               62  INPLACE_ADD      
               64  ROT_TWO          
               66  STORE_ATTR               _read_bytes

 L. 313        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _read_bytes
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _length
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    86  'to 86'

 L. 314        80  LOAD_CONST               True
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _at_eof
             86_0  COME_FROM            78  '78'

 L. 315        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _at_eof
               90  POP_JUMP_IF_FALSE   124  'to 124'

 L. 316        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _content
               96  LOAD_METHOD              readline
               98  CALL_METHOD_0         0  ''
              100  GET_AWAITABLE    
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  STORE_FAST               'clrf'

 L. 318       108  LOAD_CONST               b'\r\n'
              110  LOAD_FAST                'clrf'
              112  COMPARE_OP               ==

 L. 317       114  POP_JUMP_IF_TRUE    124  'to 124'
              116  <74>             

 L. 319       118  LOAD_STR                 'reader did not read all the data or it is malformed'

 L. 317       120  CALL_FUNCTION_1       1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           114  '114'
            124_1  COME_FROM            90  '90'

 L. 320       124  LOAD_FAST                'chunk'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 116

    async def _read_chunk_from_length--- This code section failed: ---

 L. 325         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _length
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  <74>             
               12  LOAD_STR                 'Content-Length required for chunked read'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 326        18  LOAD_GLOBAL              min
               20  LOAD_FAST                'size'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _length
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _read_bytes
               30  BINARY_SUBTRACT  
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'chunk_size'

 L. 327        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _content
               40  LOAD_METHOD              read
               42  LOAD_FAST                'chunk_size'
               44  CALL_METHOD_1         1  ''
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  STORE_FAST               'chunk'

 L. 328        54  LOAD_FAST                'chunk'
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    async def _read_chunk_from_stream--- This code section failed: ---

 L. 334         0  LOAD_FAST                'size'
                2  LOAD_GLOBAL              len
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _boundary
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_CONST               2
               12  BINARY_ADD       
               14  COMPARE_OP               >=

 L. 333        16  POP_JUMP_IF_TRUE     26  'to 26'
               18  <74>             

 L. 335        20  LOAD_STR                 'Chunk size must be greater or equal than boundary length + 2'

 L. 333        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 336        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _prev_chunk
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  STORE_FAST               'first_chunk'

 L. 337        36  LOAD_FAST                'first_chunk'
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L. 338        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _content
               44  LOAD_METHOD              read
               46  LOAD_FAST                'size'
               48  CALL_METHOD_1         1  ''
               50  GET_AWAITABLE    
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _prev_chunk
             60_0  COME_FROM            38  '38'

 L. 340        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _content
               64  LOAD_METHOD              read
               66  LOAD_FAST                'size'
               68  CALL_METHOD_1         1  ''
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  STORE_FAST               'chunk'

 L. 341        78  LOAD_FAST                'self'
               80  DUP_TOP          
               82  LOAD_ATTR                _content_eof
               84  LOAD_GLOBAL              int
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _content
               90  LOAD_METHOD              at_eof
               92  CALL_METHOD_0         0  ''
               94  CALL_FUNCTION_1       1  ''
               96  INPLACE_ADD      
               98  ROT_TWO          
              100  STORE_ATTR               _content_eof

 L. 342       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _content_eof
              106  LOAD_CONST               3
              108  COMPARE_OP               <
              110  POP_JUMP_IF_TRUE    120  'to 120'
              112  <74>             
              114  LOAD_STR                 'Reading after EOF'
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           110  '110'

 L. 343       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _prev_chunk
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_TRUE    134  'to 134'
              130  <74>             
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           128  '128'

 L. 344       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _prev_chunk
              138  LOAD_FAST                'chunk'
              140  BINARY_ADD       
              142  STORE_FAST               'window'

 L. 345       144  LOAD_CONST               b'\r\n'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _boundary
              150  BINARY_ADD       
              152  STORE_FAST               'sub'

 L. 346       154  LOAD_FAST                'first_chunk'
              156  POP_JUMP_IF_FALSE   170  'to 170'

 L. 347       158  LOAD_FAST                'window'
              160  LOAD_METHOD              find
              162  LOAD_FAST                'sub'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'idx'
              168  JUMP_FORWARD        202  'to 202'
            170_0  COME_FROM           156  '156'

 L. 349       170  LOAD_FAST                'window'
              172  LOAD_METHOD              find
              174  LOAD_FAST                'sub'
              176  LOAD_GLOBAL              max
              178  LOAD_CONST               0
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _prev_chunk
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_GLOBAL              len
              190  LOAD_FAST                'sub'
              192  CALL_FUNCTION_1       1  ''
              194  BINARY_SUBTRACT  
              196  CALL_FUNCTION_2       2  ''
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'idx'
            202_0  COME_FROM           168  '168'

 L. 350       202  LOAD_FAST                'idx'
              204  LOAD_CONST               0
              206  COMPARE_OP               >=
          208_210  POP_JUMP_IF_FALSE   344  'to 344'

 L. 352       212  LOAD_GLOBAL              warnings
              214  LOAD_METHOD              catch_warnings
              216  CALL_METHOD_0         0  ''
              218  SETUP_WITH          270  'to 270'
              220  POP_TOP          

 L. 353       222  LOAD_GLOBAL              warnings
              224  LOAD_ATTR                filterwarnings
              226  LOAD_STR                 'ignore'
              228  LOAD_GLOBAL              DeprecationWarning
              230  LOAD_CONST               ('category',)
              232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              234  POP_TOP          

 L. 354       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _content
              240  LOAD_METHOD              unread_data
              242  LOAD_FAST                'window'
              244  LOAD_FAST                'idx'
              246  LOAD_CONST               None
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  POP_BLOCK        
              258  LOAD_CONST               None
              260  DUP_TOP          
              262  DUP_TOP          
              264  CALL_FUNCTION_3       3  ''
              266  POP_TOP          
              268  JUMP_FORWARD        288  'to 288'
            270_0  COME_FROM_WITH      218  '218'
              270  <49>             
          272_274  POP_JUMP_IF_TRUE    278  'to 278'
              276  <48>             
            278_0  COME_FROM           272  '272'
              278  POP_TOP          
              280  POP_TOP          
              282  POP_TOP          
              284  POP_EXCEPT       
              286  POP_TOP          
            288_0  COME_FROM           268  '268'

 L. 355       288  LOAD_FAST                'size'
              290  LOAD_FAST                'idx'
              292  COMPARE_OP               >
          294_296  POP_JUMP_IF_FALSE   314  'to 314'

 L. 356       298  LOAD_FAST                'self'
              300  LOAD_ATTR                _prev_chunk
              302  LOAD_CONST               None
              304  LOAD_FAST                'idx'
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_FAST                'self'
              312  STORE_ATTR               _prev_chunk
            314_0  COME_FROM           294  '294'

 L. 357       314  LOAD_FAST                'window'
              316  LOAD_GLOBAL              len
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _prev_chunk
              322  CALL_FUNCTION_1       1  ''
              324  LOAD_FAST                'idx'
              326  BUILD_SLICE_2         2 
              328  BINARY_SUBSCR    
              330  STORE_FAST               'chunk'

 L. 358       332  LOAD_FAST                'chunk'
          334_336  POP_JUMP_IF_TRUE    344  'to 344'

 L. 359       338  LOAD_CONST               True
              340  LOAD_FAST                'self'
              342  STORE_ATTR               _at_eof
            344_0  COME_FROM           334  '334'
            344_1  COME_FROM           208  '208'

 L. 360       344  LOAD_FAST                'self'
              346  LOAD_ATTR                _prev_chunk
              348  STORE_FAST               'result'

 L. 361       350  LOAD_FAST                'chunk'
              352  LOAD_FAST                'self'
              354  STORE_ATTR               _prev_chunk

 L. 362       356  LOAD_FAST                'result'
              358  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 18

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
        else:
            while True:
                if not self._at_eof:
                    await self.read_chunkself.chunk_size

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

    async def form--- This code section failed: ---

 L. 420         0  LOAD_FAST                'self'
                2  LOAD_ATTR                read
                4  LOAD_CONST               True
                6  LOAD_CONST               ('decode',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  STORE_FAST               'data'

 L. 421        18  LOAD_FAST                'data'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 422        22  BUILD_LIST_0          0 
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 423        26  LOAD_FAST                'encoding'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 424        34  LOAD_FAST                'encoding'
               36  STORE_FAST               'real_encoding'
               38  JUMP_FORWARD         52  'to 52'
             40_0  COME_FROM            32  '32'

 L. 426        40  LOAD_FAST                'self'
               42  LOAD_ATTR                get_charset
               44  LOAD_STR                 'utf-8'
               46  LOAD_CONST               ('default',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  STORE_FAST               'real_encoding'
             52_0  COME_FROM            38  '38'

 L. 427        52  LOAD_GLOBAL              parse_qsl

 L. 428        54  LOAD_FAST                'data'
               56  LOAD_METHOD              rstrip
               58  CALL_METHOD_0         0  ''
               60  LOAD_METHOD              decode
               62  LOAD_FAST                'real_encoding'
               64  CALL_METHOD_1         1  ''

 L. 429        66  LOAD_CONST               True

 L. 430        68  LOAD_FAST                'real_encoding'

 L. 427        70  LOAD_CONST               ('keep_blank_values', 'encoding')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30

    def at_eof(self) -> bool:
        """Returns True if the boundary was reached or False otherwise."""
        return self._at_eof

    def decode--- This code section failed: ---

 L. 441         0  LOAD_GLOBAL              CONTENT_TRANSFER_ENCODING
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                headers
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 442        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _decode_content_transfer
               14  LOAD_FAST                'data'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'data'
             20_0  COME_FROM             8  '8'

 L. 443        20  LOAD_GLOBAL              CONTENT_ENCODING
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                headers
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 444        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _decode_content
               34  LOAD_FAST                'data'
               36  CALL_METHOD_1         1  ''
               38  RETURN_VALUE     
             40_0  COME_FROM            28  '28'

 L. 445        40  LOAD_FAST                'data'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _decode_content(self, data: bytes) -> bytes:
        encoding = self.headers.getCONTENT_ENCODING''.lower
        if encoding == 'deflate':
            return zlib.decompressdata(-zlib.MAX_WBITS)
        if encoding == 'gzip':
            return zlib.decompressdata(16 + zlib.MAX_WBITS)
        if encoding == 'identity':
            return data
        raise RuntimeError(f"unknown content encoding: {encoding}")

    def _decode_content_transfer--- This code section failed: ---

 L. 460         0  LOAD_FAST                'self'
                2  LOAD_ATTR                headers
                4  LOAD_METHOD              get
                6  LOAD_GLOBAL              CONTENT_TRANSFER_ENCODING
                8  LOAD_STR                 ''
               10  CALL_METHOD_2         2  ''
               12  LOAD_METHOD              lower
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'encoding'

 L. 462        18  LOAD_FAST                'encoding'
               20  LOAD_STR                 'base64'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    36  'to 36'

 L. 463        26  LOAD_GLOBAL              base64
               28  LOAD_METHOD              b64decode
               30  LOAD_FAST                'data'
               32  CALL_METHOD_1         1  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            24  '24'

 L. 464        36  LOAD_FAST                'encoding'
               38  LOAD_STR                 'quoted-printable'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L. 465        44  LOAD_GLOBAL              binascii
               46  LOAD_METHOD              a2b_qp
               48  LOAD_FAST                'data'
               50  CALL_METHOD_1         1  ''
               52  RETURN_VALUE     
             54_0  COME_FROM            42  '42'

 L. 466        54  LOAD_FAST                'encoding'
               56  LOAD_CONST               ('binary', '8bit', '7bit')
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 467        62  LOAD_FAST                'data'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 469        66  LOAD_GLOBAL              RuntimeError

 L. 470        68  LOAD_STR                 'unknown content transfer encoding: {}'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'encoding'
               74  CALL_METHOD_1         1  ''

 L. 469        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 58

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

    def __init__--- This code section failed: ---

 L. 500         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'value'
                8  BUILD_LIST_1          1 
               10  LOAD_FAST                'args'
               12  CALL_FINALLY         15  'to 15'
               14  WITH_CLEANUP_FINISH
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kwargs'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  POP_TOP          

 L. 502        26  BUILD_MAP_0           0 
               28  STORE_FAST               'params'

 L. 503        30  LOAD_FAST                'value'
               32  LOAD_ATTR                name
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    50  'to 50'

 L. 504        40  LOAD_FAST                'value'
               42  LOAD_ATTR                name
               44  LOAD_FAST                'params'
               46  LOAD_STR                 'name'
               48  STORE_SUBSCR     
             50_0  COME_FROM            38  '38'

 L. 505        50  LOAD_FAST                'value'
               52  LOAD_ATTR                filename
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 506        60  LOAD_FAST                'value'
               62  LOAD_ATTR                filename
               64  LOAD_FAST                'params'
               66  LOAD_STR                 'filename'
               68  STORE_SUBSCR     
             70_0  COME_FROM            58  '58'

 L. 508        70  LOAD_FAST                'params'
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 509        74  LOAD_FAST                'self'
               76  LOAD_ATTR                set_content_disposition
               78  LOAD_CONST               ('attachment', True)
               80  BUILD_MAP_0           0 
               82  LOAD_FAST                'params'
               84  <164>                 1  ''
               86  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               88  POP_TOP          
             90_0  COME_FROM            72  '72'

Parse error at or near `None' instruction at offset -1

    async def write(self, writer: Any) -> None:
        field = self._value
        chunk = await field.read_chunk(size=65536)
        while chunk:
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

    def __aiter__(self) -> AsyncIterator['BodyPartReader']:
        return self

    async def __anext__--- This code section failed: ---

 L. 549         0  LOAD_FAST                'self'
                2  LOAD_METHOD              next
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'part'

 L. 550        14  LOAD_FAST                'part'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 551        22  LOAD_GLOBAL              StopAsyncIteration
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 552        26  LOAD_FAST                'part'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

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
        else:
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

    async def release--- This code section failed: ---

 L. 594         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _at_eof
                4  POP_JUMP_IF_TRUE     46  'to 46'

 L. 595         6  LOAD_FAST                'self'
                8  LOAD_METHOD              next
               10  CALL_METHOD_0         0  ''
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  STORE_FAST               'item'

 L. 596        20  LOAD_FAST                'item'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    30  'to 30'

 L. 597        28  BREAK_LOOP           46  'to 46'
             30_0  COME_FROM            26  '26'

 L. 598        30  LOAD_FAST                'item'
               32  LOAD_METHOD              release
               34  CALL_METHOD_0         0  ''
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 24

    async def fetch_next_part(self) -> Union[('MultipartReader', BodyPartReader)]:
        """Returns the next body part reader."""
        headers = await self._read_headers
        return self._get_part_readerheaders

    def _get_part_reader--- This code section failed: ---

 L. 616         0  LOAD_FAST                'headers'
                2  LOAD_METHOD              get
                4  LOAD_GLOBAL              CONTENT_TYPE
                6  LOAD_STR                 ''
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'ctype'

 L. 617        12  LOAD_GLOBAL              parse_mimetype
               14  LOAD_FAST                'ctype'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'mimetype'

 L. 619        20  LOAD_FAST                'mimetype'
               22  LOAD_ATTR                type
               24  LOAD_STR                 'multipart'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    70  'to 70'

 L. 620        30  LOAD_FAST                'self'
               32  LOAD_ATTR                multipart_reader_cls
               34  LOAD_CONST               None
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L. 621        40  LOAD_GLOBAL              type
               42  LOAD_FAST                'self'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_FAST                'headers'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _content
               52  CALL_FUNCTION_2       2  ''
               54  RETURN_VALUE     
             56_0  COME_FROM            38  '38'

 L. 622        56  LOAD_FAST                'self'
               58  LOAD_METHOD              multipart_reader_cls
               60  LOAD_FAST                'headers'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _content
               66  CALL_METHOD_2         2  ''
               68  RETURN_VALUE     
             70_0  COME_FROM            28  '28'

 L. 624        70  LOAD_FAST                'self'
               72  LOAD_METHOD              part_reader_cls
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _boundary
               78  LOAD_FAST                'headers'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _content
               84  CALL_METHOD_3         3  ''
               86  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 36

    def _get_boundary--- This code section failed: ---

 L. 627         0  LOAD_GLOBAL              parse_mimetype
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                headers
                6  LOAD_GLOBAL              CONTENT_TYPE
                8  BINARY_SUBSCR    
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'mimetype'

 L. 629        14  LOAD_FAST                'mimetype'
               16  LOAD_ATTR                type
               18  LOAD_STR                 'multipart'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  <74>             
               26  LOAD_STR                 'multipart/* content type expected'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 631        32  LOAD_STR                 'boundary'
               34  LOAD_FAST                'mimetype'
               36  LOAD_ATTR                parameters
               38  <118>                 1  ''
               40  POP_JUMP_IF_FALSE    60  'to 60'

 L. 632        42  LOAD_GLOBAL              ValueError

 L. 633        44  LOAD_STR                 'boundary missed for Content-Type: %s'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                headers
               50  LOAD_GLOBAL              CONTENT_TYPE
               52  BINARY_SUBSCR    
               54  BINARY_MODULO    

 L. 632        56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            40  '40'

 L. 636        60  LOAD_FAST                'mimetype'
               62  LOAD_ATTR                parameters
               64  LOAD_STR                 'boundary'
               66  BINARY_SUBSCR    
               68  STORE_FAST               'boundary'

 L. 637        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'boundary'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               70
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L. 638        82  LOAD_GLOBAL              ValueError
               84  LOAD_STR                 'boundary %r is too long (70 chars max)'
               86  LOAD_FAST                'boundary'
               88  BINARY_MODULO    
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            80  '80'

 L. 640        94  LOAD_FAST                'boundary'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 24

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
            raise ValueError(f"Invalid boundary {chunk!r}, expected {self._boundary!r}")

    async def _read_headers(self) -> 'CIMultiDictProxy[str]':
        lines = [b'']
        while True:
            chunk = await self._content.readline
            chunk = chunk.strip
            lines.appendchunk
            if not chunk:
                break

        parser = HeadersParser
        headers, raw_headers = parser.parse_headerslines
        return headers

    async def _maybe_release_last_part--- This code section failed: ---

 L. 698         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _last_part
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 699        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _last_part
               14  LOAD_METHOD              at_eof
               16  CALL_METHOD_0         0  ''
               18  POP_JUMP_IF_TRUE     36  'to 36'

 L. 700        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _last_part
               24  LOAD_METHOD              release
               26  CALL_METHOD_0         0  ''
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  POP_TOP          
             36_0  COME_FROM            18  '18'

 L. 701        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _unread
               40  LOAD_METHOD              extend
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _last_part
               46  LOAD_ATTR                _unread
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 702        52  LOAD_CONST               None
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _last_part
             58_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


_Part = Tuple[(Payload, str, str)]

class MultipartWriter(Payload):
    __doc__ = 'Multipart body writer.'

    def __init__--- This code section failed: ---

 L. 712         0  LOAD_FAST                'boundary'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_FAST                'boundary'
               10  JUMP_FORWARD         20  'to 20'
             12_0  COME_FROM             6  '6'
               12  LOAD_GLOBAL              uuid
               14  LOAD_METHOD              uuid4
               16  CALL_METHOD_0         0  ''
               18  LOAD_ATTR                hex
             20_0  COME_FROM            10  '10'
               20  STORE_FAST               'boundary'

 L. 718        22  SETUP_FINALLY        40  'to 40'

 L. 719        24  LOAD_FAST                'boundary'
               26  LOAD_METHOD              encode
               28  LOAD_STR                 'ascii'
               30  CALL_METHOD_1         1  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _boundary
               36  POP_BLOCK        
               38  JUMP_FORWARD         68  'to 68'
             40_0  COME_FROM_FINALLY    22  '22'

 L. 720        40  DUP_TOP          
               42  LOAD_GLOBAL              UnicodeEncodeError
               44  <121>                66  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 721        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'boundary should contain ASCII only chars'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_CONST               None
               60  RAISE_VARARGS_2       2  'exception instance with __cause__'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
               66  <48>             
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            38  '38'

 L. 722        68  LOAD_STR                 'multipart/'
               70  LOAD_FAST                'subtype'
               72  FORMAT_VALUE          0  ''
               74  LOAD_STR                 '; boundary='
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _boundary_value
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_4        4 
               84  STORE_FAST               'ctype'

 L. 724        86  LOAD_GLOBAL              super
               88  CALL_FUNCTION_0       0  ''
               90  LOAD_ATTR                __init__
               92  LOAD_CONST               None
               94  LOAD_FAST                'ctype'
               96  LOAD_CONST               ('content_type',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  POP_TOP          

 L. 726       102  BUILD_LIST_0          0 
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _parts

Parse error at or near `None' instruction at offset -1

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

    def append--- This code section failed: ---

 L. 788         0  LOAD_FAST                'headers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 789         8  LOAD_GLOBAL              CIMultiDict
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'headers'
             14_0  COME_FROM             6  '6'

 L. 791        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'obj'
               18  LOAD_GLOBAL              Payload
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    46  'to 46'

 L. 792        24  LOAD_FAST                'obj'
               26  LOAD_ATTR                headers
               28  LOAD_METHOD              update
               30  LOAD_FAST                'headers'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 793        36  LOAD_FAST                'self'
               38  LOAD_METHOD              append_payload
               40  LOAD_FAST                'obj'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            22  '22'

 L. 795        46  SETUP_FINALLY        64  'to 64'

 L. 796        48  LOAD_GLOBAL              get_payload
               50  LOAD_FAST                'obj'
               52  LOAD_FAST                'headers'
               54  LOAD_CONST               ('headers',)
               56  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               58  STORE_FAST               'payload'
               60  POP_BLOCK        
               62  JUMP_FORWARD         94  'to 94'
             64_0  COME_FROM_FINALLY    46  '46'

 L. 797        64  DUP_TOP          
               66  LOAD_GLOBAL              LookupError
               68  <121>                92  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 798        76  LOAD_GLOBAL              TypeError
               78  LOAD_STR                 'Cannot create payload from %r'
               80  LOAD_FAST                'obj'
               82  BINARY_MODULO    
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
               88  POP_EXCEPT       
               90  JUMP_FORWARD        104  'to 104'
               92  <48>             
             94_0  COME_FROM            62  '62'

 L. 800        94  LOAD_FAST                'self'
               96  LOAD_METHOD              append_payload
               98  LOAD_FAST                'payload'
              100  CALL_METHOD_1         1  ''
              102  RETURN_VALUE     
            104_0  COME_FROM            90  '90'

Parse error at or near `None' instruction at offset -1

    def append_payload--- This code section failed: ---

 L. 805         0  LOAD_FAST                'payload'
                2  LOAD_ATTR                headers
                4  LOAD_METHOD              get

 L. 806         6  LOAD_GLOBAL              CONTENT_ENCODING

 L. 807         8  LOAD_STR                 ''

 L. 805        10  CALL_METHOD_2         2  ''
               12  LOAD_METHOD              lower
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'encoding'

 L. 809        18  LOAD_FAST                'encoding'
               20  POP_JUMP_IF_FALSE    44  'to 44'
               22  LOAD_FAST                'encoding'
               24  LOAD_CONST               ('deflate', 'gzip', 'identity')
               26  <118>                 1  ''
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 810        30  LOAD_GLOBAL              RuntimeError
               32  LOAD_STR                 'unknown content encoding: '
               34  LOAD_FAST                'encoding'
               36  FORMAT_VALUE          0  ''
               38  BUILD_STRING_2        2 
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            28  '28'
             44_1  COME_FROM            20  '20'

 L. 811        44  LOAD_FAST                'encoding'
               46  LOAD_STR                 'identity'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 812        52  LOAD_CONST               None
               54  STORE_FAST               'encoding'
             56_0  COME_FROM            50  '50'

 L. 815        56  LOAD_FAST                'payload'
               58  LOAD_ATTR                headers
               60  LOAD_METHOD              get

 L. 816        62  LOAD_GLOBAL              CONTENT_TRANSFER_ENCODING

 L. 817        64  LOAD_STR                 ''

 L. 815        66  CALL_METHOD_2         2  ''
               68  LOAD_METHOD              lower
               70  CALL_METHOD_0         0  ''
               72  STORE_FAST               'te_encoding'

 L. 819        74  LOAD_FAST                'te_encoding'
               76  LOAD_CONST               ('', 'base64', 'quoted-printable', 'binary')
               78  <118>                 1  ''
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L. 820        82  LOAD_GLOBAL              RuntimeError

 L. 821        84  LOAD_STR                 'unknown content transfer encoding: {}'
               86  LOAD_METHOD              format
               88  LOAD_FAST                'te_encoding'
               90  CALL_METHOD_1         1  ''

 L. 820        92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            80  '80'

 L. 823        96  LOAD_FAST                'te_encoding'
               98  LOAD_STR                 'binary'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   108  'to 108'

 L. 824       104  LOAD_CONST               None
              106  STORE_FAST               'te_encoding'
            108_0  COME_FROM           102  '102'

 L. 827       108  LOAD_FAST                'payload'
              110  LOAD_ATTR                size
              112  STORE_FAST               'size'

 L. 828       114  LOAD_FAST                'size'
              116  LOAD_CONST               None
              118  <117>                 1  ''
              120  POP_JUMP_IF_FALSE   144  'to 144'
              122  LOAD_FAST                'encoding'
              124  POP_JUMP_IF_TRUE    144  'to 144'
              126  LOAD_FAST                'te_encoding'
              128  POP_JUMP_IF_TRUE    144  'to 144'

 L. 829       130  LOAD_GLOBAL              str
              132  LOAD_FAST                'size'
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_FAST                'payload'
              138  LOAD_ATTR                headers
              140  LOAD_GLOBAL              CONTENT_LENGTH
              142  STORE_SUBSCR     
            144_0  COME_FROM           128  '128'
            144_1  COME_FROM           124  '124'
            144_2  COME_FROM           120  '120'

 L. 831       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _parts
              148  LOAD_METHOD              append
              150  LOAD_FAST                'payload'
              152  LOAD_FAST                'encoding'
              154  LOAD_FAST                'te_encoding'
              156  BUILD_TUPLE_3         3 
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 832       162  LOAD_FAST                'payload'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 26

    def append_json--- This code section failed: ---

 L. 838         0  LOAD_FAST                'headers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 839         8  LOAD_GLOBAL              CIMultiDict
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'headers'
             14_0  COME_FROM             6  '6'

 L. 841        14  LOAD_FAST                'self'
               16  LOAD_METHOD              append_payload
               18  LOAD_GLOBAL              JsonPayload
               20  LOAD_FAST                'obj'
               22  LOAD_FAST                'headers'
               24  LOAD_CONST               ('headers',)
               26  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               28  CALL_METHOD_1         1  ''
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def append_form--- This code section failed: ---

 L. 849         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              Sequence
                6  LOAD_GLOBAL              Mapping
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 851        18  LOAD_FAST                'headers'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L. 852        26  LOAD_GLOBAL              CIMultiDict
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'headers'
             32_0  COME_FROM            24  '24'

 L. 854        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'obj'
               36  LOAD_GLOBAL              Mapping
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L. 855        42  LOAD_GLOBAL              list
               44  LOAD_FAST                'obj'
               46  LOAD_METHOD              items
               48  CALL_METHOD_0         0  ''
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'obj'
             54_0  COME_FROM            40  '40'

 L. 856        54  LOAD_GLOBAL              urlencode
               56  LOAD_FAST                'obj'
               58  LOAD_CONST               True
               60  LOAD_CONST               ('doseq',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  STORE_FAST               'data'

 L. 858        66  LOAD_FAST                'self'
               68  LOAD_METHOD              append_payload

 L. 859        70  LOAD_GLOBAL              StringPayload

 L. 860        72  LOAD_FAST                'data'
               74  LOAD_FAST                'headers'
               76  LOAD_STR                 'application/x-www-form-urlencoded'

 L. 859        78  LOAD_CONST               ('headers', 'content_type')
               80  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 858        82  CALL_METHOD_1         1  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def size--- This code section failed: ---

 L. 867         0  LOAD_CONST               0
                2  STORE_FAST               'total'

 L. 868         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _parts
                8  GET_ITER         
               10  FOR_ITER             92  'to 92'
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'part'
               16  STORE_FAST               'encoding'
               18  STORE_FAST               'te_encoding'

 L. 869        20  LOAD_FAST                'encoding'
               22  POP_JUMP_IF_TRUE     38  'to 38'
               24  LOAD_FAST                'te_encoding'
               26  POP_JUMP_IF_TRUE     38  'to 38'
               28  LOAD_FAST                'part'
               30  LOAD_ATTR                size
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            22  '22'

 L. 870        38  POP_TOP          
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 872        44  LOAD_FAST                'total'
               46  LOAD_GLOBAL              int

 L. 873        48  LOAD_CONST               2

 L. 874        50  LOAD_GLOBAL              len
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _boundary
               56  CALL_FUNCTION_1       1  ''

 L. 873        58  BINARY_ADD       

 L. 875        60  LOAD_CONST               2

 L. 873        62  BINARY_ADD       

 L. 876        64  LOAD_FAST                'part'
               66  LOAD_ATTR                size

 L. 873        68  BINARY_ADD       

 L. 877        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'part'
               74  LOAD_ATTR                _binary_headers
               76  CALL_FUNCTION_1       1  ''

 L. 873        78  BINARY_ADD       

 L. 878        80  LOAD_CONST               2

 L. 873        82  BINARY_ADD       

 L. 872        84  CALL_FUNCTION_1       1  ''
               86  INPLACE_ADD      
               88  STORE_FAST               'total'
               90  JUMP_BACK            10  'to 10'

 L. 881        92  LOAD_FAST                'total'
               94  LOAD_CONST               2
               96  LOAD_GLOBAL              len
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                _boundary
              102  CALL_FUNCTION_1       1  ''
              104  BINARY_ADD       
              106  LOAD_CONST               4
              108  BINARY_ADD       
              110  INPLACE_ADD      
              112  STORE_FAST               'total'

 L. 882       114  LOAD_FAST                'total'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34

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
            self._encoding_buffer = bytearray
        else:
            if encoding == 'quoted-printable':
                self._encoding = 'quoted-printable'

    def enable_compression(self, encoding: str='deflate') -> None:
        zlib_mode = 16 + zlib.MAX_WBITS if encoding == 'gzip' else -zlib.MAX_WBITS
        self._compress = zlib.compressobj(wbits=zlib_mode)

    async def write_eof--- This code section failed: ---

 L. 926         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _compress
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    46  'to 46'

 L. 927        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _compress
               14  LOAD_METHOD              flush
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'chunk'

 L. 928        20  LOAD_FAST                'chunk'
               22  POP_JUMP_IF_FALSE    46  'to 46'

 L. 929        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _compress

 L. 930        30  LOAD_FAST                'self'
               32  LOAD_METHOD              write
               34  LOAD_FAST                'chunk'
               36  CALL_METHOD_1         1  ''
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  POP_TOP          
             46_0  COME_FROM            22  '22'
             46_1  COME_FROM             8  '8'

 L. 932        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _encoding
               50  LOAD_STR                 'base64'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    88  'to 88'

 L. 933        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _encoding_buffer
               60  POP_JUMP_IF_FALSE    88  'to 88'

 L. 934        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _writer
               66  LOAD_METHOD              write
               68  LOAD_GLOBAL              base64
               70  LOAD_METHOD              b64encode
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _encoding_buffer
               76  CALL_METHOD_1         1  ''
               78  CALL_METHOD_1         1  ''
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  POP_TOP          
             88_0  COME_FROM            60  '60'
             88_1  COME_FROM            54  '54'

Parse error at or near `None' instruction at offset -1

    async def write--- This code section failed: ---

 L. 937         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _compress
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 938        10  LOAD_FAST                'chunk'
               12  POP_JUMP_IF_FALSE    34  'to 34'

 L. 939        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _compress
               18  LOAD_METHOD              compress
               20  LOAD_FAST                'chunk'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'chunk'

 L. 940        26  LOAD_FAST                'chunk'
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L. 941        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            12  '12'
             34_2  COME_FROM             8  '8'

 L. 943        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _encoding
               38  LOAD_STR                 'base64'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE   164  'to 164'

 L. 944        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _encoding_buffer
               48  STORE_FAST               'buf'

 L. 945        50  LOAD_FAST                'buf'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  <74>             
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            56  '56'

 L. 946        62  LOAD_FAST                'buf'
               64  LOAD_METHOD              extend
               66  LOAD_FAST                'chunk'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 948        72  LOAD_FAST                'buf'
               74  POP_JUMP_IF_FALSE   218  'to 218'

 L. 949        76  LOAD_GLOBAL              divmod
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'buf'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_CONST               3
               86  CALL_FUNCTION_2       2  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'div'
               92  STORE_FAST               'mod'

 L. 950        94  LOAD_FAST                'buf'
               96  LOAD_CONST               None
               98  LOAD_FAST                'div'
              100  LOAD_CONST               3
              102  BINARY_MULTIPLY  
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'buf'
              110  LOAD_FAST                'div'
              112  LOAD_CONST               3
              114  BINARY_MULTIPLY  
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  ROT_TWO          
              124  STORE_FAST               'enc_chunk'
              126  LOAD_FAST                'self'
              128  STORE_ATTR               _encoding_buffer

 L. 951       130  LOAD_FAST                'enc_chunk'
              132  POP_JUMP_IF_FALSE   218  'to 218'

 L. 952       134  LOAD_GLOBAL              base64
              136  LOAD_METHOD              b64encode
              138  LOAD_FAST                'enc_chunk'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'b64chunk'

 L. 953       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _writer
              148  LOAD_METHOD              write
              150  LOAD_FAST                'b64chunk'
              152  CALL_METHOD_1         1  ''
              154  GET_AWAITABLE    
              156  LOAD_CONST               None
              158  YIELD_FROM       
              160  POP_TOP          
              162  JUMP_FORWARD        218  'to 218'
            164_0  COME_FROM            42  '42'

 L. 954       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _encoding
              168  LOAD_STR                 'quoted-printable'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   200  'to 200'

 L. 955       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _writer
              178  LOAD_METHOD              write
              180  LOAD_GLOBAL              binascii
              182  LOAD_METHOD              b2a_qp
              184  LOAD_FAST                'chunk'
              186  CALL_METHOD_1         1  ''
              188  CALL_METHOD_1         1  ''
              190  GET_AWAITABLE    
              192  LOAD_CONST               None
              194  YIELD_FROM       
              196  POP_TOP          
              198  JUMP_FORWARD        218  'to 218'
            200_0  COME_FROM           172  '172'

 L. 957       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _writer
              204  LOAD_METHOD              write
              206  LOAD_FAST                'chunk'
              208  CALL_METHOD_1         1  ''
              210  GET_AWAITABLE    
              212  LOAD_CONST               None
              214  YIELD_FROM       
              216  POP_TOP          
            218_0  COME_FROM           198  '198'
            218_1  COME_FROM           162  '162'
            218_2  COME_FROM           132  '132'
            218_3  COME_FROM            74  '74'

Parse error at or near `None' instruction at offset -1