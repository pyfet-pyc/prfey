# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\etree\ElementInclude.py
import copy
from . import ElementTree
from urllib.parse import urljoin
XINCLUDE = '{http://www.w3.org/2001/XInclude}'
XINCLUDE_INCLUDE = XINCLUDE + 'include'
XINCLUDE_FALLBACK = XINCLUDE + 'fallback'
DEFAULT_MAX_INCLUSION_DEPTH = 6

class FatalIncludeError(SyntaxError):
    pass


class LimitedRecursiveIncludeError(FatalIncludeError):
    pass


def default_loader--- This code section failed: ---

 L.  88         0  LOAD_FAST                'parse'
                2  LOAD_STR                 'xml'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    66  'to 66'

 L.  89         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'href'
               12  LOAD_STR                 'rb'
               14  CALL_FUNCTION_2       2  ''
               16  SETUP_WITH           48  'to 48'
               18  STORE_FAST               'file'

 L.  90        20  LOAD_GLOBAL              ElementTree
               22  LOAD_METHOD              parse
               24  LOAD_FAST                'file'
               26  CALL_METHOD_1         1  ''
               28  LOAD_METHOD              getroot
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'data'
               34  POP_BLOCK        
               36  LOAD_CONST               None
               38  DUP_TOP          
               40  DUP_TOP          
               42  CALL_FUNCTION_3       3  ''
               44  POP_TOP          
               46  JUMP_FORWARD        128  'to 128'
             48_0  COME_FROM_WITH       16  '16'
               48  <49>             
               50  POP_JUMP_IF_TRUE     54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          
               60  POP_EXCEPT       
               62  POP_TOP          
               64  JUMP_FORWARD        128  'to 128'
             66_0  COME_FROM             6  '6'

 L.  92        66  LOAD_FAST                'encoding'
               68  POP_JUMP_IF_TRUE     74  'to 74'

 L.  93        70  LOAD_STR                 'UTF-8'
               72  STORE_FAST               'encoding'
             74_0  COME_FROM            68  '68'

 L.  94        74  LOAD_GLOBAL              open
               76  LOAD_FAST                'href'
               78  LOAD_STR                 'r'
               80  LOAD_FAST                'encoding'
               82  LOAD_CONST               ('encoding',)
               84  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               86  SETUP_WITH          112  'to 112'
               88  STORE_FAST               'file'

 L.  95        90  LOAD_FAST                'file'
               92  LOAD_METHOD              read
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'data'
               98  POP_BLOCK        
              100  LOAD_CONST               None
              102  DUP_TOP          
              104  DUP_TOP          
              106  CALL_FUNCTION_3       3  ''
              108  POP_TOP          
              110  JUMP_FORWARD        128  'to 128'
            112_0  COME_FROM_WITH       86  '86'
              112  <49>             
              114  POP_JUMP_IF_TRUE    118  'to 118'
              116  <48>             
            118_0  COME_FROM           114  '114'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          
              124  POP_EXCEPT       
              126  POP_TOP          
            128_0  COME_FROM           110  '110'
            128_1  COME_FROM            64  '64'
            128_2  COME_FROM            46  '46'

 L.  96       128  LOAD_FAST                'data'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 38


def include--- This code section failed: ---

 L. 118         0  LOAD_FAST                'max_depth'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 119         8  LOAD_CONST               -1
               10  STORE_FAST               'max_depth'
               12  JUMP_FORWARD         34  'to 34'
             14_0  COME_FROM             6  '6'

 L. 120        14  LOAD_FAST                'max_depth'
               16  LOAD_CONST               0
               18  COMPARE_OP               <
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L. 121        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 "expected non-negative depth or None for 'max_depth', got %r"
               26  LOAD_FAST                'max_depth'
               28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            20  '20'
             34_1  COME_FROM            12  '12'

 L. 123        34  LOAD_GLOBAL              hasattr
               36  LOAD_FAST                'elem'
               38  LOAD_STR                 'getroot'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 124        44  LOAD_FAST                'elem'
               46  LOAD_METHOD              getroot
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'elem'
             52_0  COME_FROM            42  '42'

 L. 125        52  LOAD_FAST                'loader'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L. 126        60  LOAD_GLOBAL              default_loader
               62  STORE_FAST               'loader'
             64_0  COME_FROM            58  '58'

 L. 128        64  LOAD_GLOBAL              _include
               66  LOAD_FAST                'elem'
               68  LOAD_FAST                'loader'
               70  LOAD_FAST                'base_url'
               72  LOAD_FAST                'max_depth'
               74  LOAD_GLOBAL              set
               76  CALL_FUNCTION_0       0  ''
               78  CALL_FUNCTION_5       5  ''
               80  POP_TOP          

Parse error at or near `None' instruction at offset -1


def _include--- This code section failed: ---

 L. 133         0  LOAD_CONST               0
                2  STORE_FAST               'i'
              4_0  COME_FROM           444  '444'
              4_1  COME_FROM           374  '374'

 L. 134         4  LOAD_FAST                'i'
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'elem'
               10  CALL_FUNCTION_1       1  ''
               12  COMPARE_OP               <
            14_16  POP_JUMP_IF_FALSE   446  'to 446'

 L. 135        18  LOAD_FAST                'elem'
               20  LOAD_FAST                'i'
               22  BINARY_SUBSCR    
               24  STORE_FAST               'e'

 L. 136        26  LOAD_FAST                'e'
               28  LOAD_ATTR                tag
               30  LOAD_GLOBAL              XINCLUDE_INCLUDE
               32  COMPARE_OP               ==
            34_36  POP_JUMP_IF_FALSE   392  'to 392'

 L. 138        38  LOAD_FAST                'e'
               40  LOAD_METHOD              get
               42  LOAD_STR                 'href'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'href'

 L. 139        48  LOAD_FAST                'base_url'
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 140        52  LOAD_GLOBAL              urljoin
               54  LOAD_FAST                'base_url'
               56  LOAD_FAST                'href'
               58  CALL_FUNCTION_2       2  ''
               60  STORE_FAST               'href'
             62_0  COME_FROM            50  '50'

 L. 141        62  LOAD_FAST                'e'
               64  LOAD_METHOD              get
               66  LOAD_STR                 'parse'
               68  LOAD_STR                 'xml'
               70  CALL_METHOD_2         2  ''
               72  STORE_FAST               'parse'

 L. 142        74  LOAD_FAST                'parse'
               76  LOAD_STR                 'xml'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   240  'to 240'

 L. 143        82  LOAD_FAST                'href'
               84  LOAD_FAST                '_parent_hrefs'
               86  <118>                 0  ''
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L. 144        90  LOAD_GLOBAL              FatalIncludeError
               92  LOAD_STR                 'recursive include of %s'
               94  LOAD_FAST                'href'
               96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            88  '88'

 L. 145       102  LOAD_FAST                'max_depth'
              104  LOAD_CONST               0
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 146       110  LOAD_GLOBAL              LimitedRecursiveIncludeError

 L. 147       112  LOAD_STR                 'maximum xinclude depth reached when including file %s'
              114  LOAD_FAST                'href'
              116  BINARY_MODULO    

 L. 146       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           108  '108'

 L. 148       122  LOAD_FAST                '_parent_hrefs'
              124  LOAD_METHOD              add
              126  LOAD_FAST                'href'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 149       132  LOAD_FAST                'loader'
              134  LOAD_FAST                'href'
              136  LOAD_FAST                'parse'
              138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'node'

 L. 150       142  LOAD_FAST                'node'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   166  'to 166'

 L. 151       150  LOAD_GLOBAL              FatalIncludeError

 L. 152       152  LOAD_STR                 'cannot load %r as %r'
              154  LOAD_FAST                'href'
              156  LOAD_FAST                'parse'
              158  BUILD_TUPLE_2         2 
              160  BINARY_MODULO    

 L. 151       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           148  '148'

 L. 154       166  LOAD_GLOBAL              copy
              168  LOAD_METHOD              copy
              170  LOAD_FAST                'node'
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'node'

 L. 155       176  LOAD_GLOBAL              _include
              178  LOAD_FAST                'node'
              180  LOAD_FAST                'loader'
              182  LOAD_FAST                'href'
              184  LOAD_FAST                'max_depth'
              186  LOAD_CONST               1
              188  BINARY_SUBTRACT  
              190  LOAD_FAST                '_parent_hrefs'
              192  CALL_FUNCTION_5       5  ''
              194  POP_TOP          

 L. 156       196  LOAD_FAST                '_parent_hrefs'
              198  LOAD_METHOD              remove
              200  LOAD_FAST                'href'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 157       206  LOAD_FAST                'e'
              208  LOAD_ATTR                tail
              210  POP_JUMP_IF_FALSE   230  'to 230'

 L. 158       212  LOAD_FAST                'node'
              214  LOAD_ATTR                tail
              216  JUMP_IF_TRUE_OR_POP   220  'to 220'
              218  LOAD_STR                 ''
            220_0  COME_FROM           216  '216'
              220  LOAD_FAST                'e'
              222  LOAD_ATTR                tail
              224  BINARY_ADD       
              226  LOAD_FAST                'node'
              228  STORE_ATTR               tail
            230_0  COME_FROM           210  '210'

 L. 159       230  LOAD_FAST                'node'
              232  LOAD_FAST                'elem'
              234  LOAD_FAST                'i'
              236  STORE_SUBSCR     
              238  JUMP_FORWARD        390  'to 390'
            240_0  COME_FROM            80  '80'

 L. 160       240  LOAD_FAST                'parse'
              242  LOAD_STR                 'text'
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   378  'to 378'

 L. 161       250  LOAD_FAST                'loader'
              252  LOAD_FAST                'href'
              254  LOAD_FAST                'parse'
              256  LOAD_FAST                'e'
              258  LOAD_METHOD              get
              260  LOAD_STR                 'encoding'
              262  CALL_METHOD_1         1  ''
              264  CALL_FUNCTION_3       3  ''
              266  STORE_FAST               'text'

 L. 162       268  LOAD_FAST                'text'
              270  LOAD_CONST               None
              272  <117>                 0  ''
          274_276  POP_JUMP_IF_FALSE   294  'to 294'

 L. 163       278  LOAD_GLOBAL              FatalIncludeError

 L. 164       280  LOAD_STR                 'cannot load %r as %r'
              282  LOAD_FAST                'href'
              284  LOAD_FAST                'parse'
              286  BUILD_TUPLE_2         2 
              288  BINARY_MODULO    

 L. 163       290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           274  '274'

 L. 166       294  LOAD_FAST                'e'
              296  LOAD_ATTR                tail
          298_300  POP_JUMP_IF_FALSE   312  'to 312'

 L. 167       302  LOAD_FAST                'text'
              304  LOAD_FAST                'e'
              306  LOAD_ATTR                tail
              308  INPLACE_ADD      
              310  STORE_FAST               'text'
            312_0  COME_FROM           298  '298'

 L. 168       312  LOAD_FAST                'i'
          314_316  POP_JUMP_IF_FALSE   350  'to 350'

 L. 169       318  LOAD_FAST                'elem'
              320  LOAD_FAST                'i'
              322  LOAD_CONST               1
              324  BINARY_SUBTRACT  
              326  BINARY_SUBSCR    
              328  STORE_FAST               'node'

 L. 170       330  LOAD_FAST                'node'
              332  LOAD_ATTR                tail
          334_336  JUMP_IF_TRUE_OR_POP   340  'to 340'
              338  LOAD_STR                 ''
            340_0  COME_FROM           334  '334'
              340  LOAD_FAST                'text'
              342  BINARY_ADD       
              344  LOAD_FAST                'node'
              346  STORE_ATTR               tail
              348  JUMP_FORWARD        368  'to 368'
            350_0  COME_FROM           314  '314'

 L. 172       350  LOAD_FAST                'elem'
              352  LOAD_ATTR                text
          354_356  JUMP_IF_TRUE_OR_POP   360  'to 360'
              358  LOAD_STR                 ''
            360_0  COME_FROM           354  '354'
              360  LOAD_FAST                'text'
              362  BINARY_ADD       
              364  LOAD_FAST                'elem'
              366  STORE_ATTR               text
            368_0  COME_FROM           348  '348'

 L. 173       368  LOAD_FAST                'elem'
              370  LOAD_FAST                'i'
              372  DELETE_SUBSCR    

 L. 174       374  JUMP_BACK             4  'to 4'
              376  BREAK_LOOP          390  'to 390'
            378_0  COME_FROM           246  '246'

 L. 176       378  LOAD_GLOBAL              FatalIncludeError

 L. 177       380  LOAD_STR                 'unknown parse type in xi:include tag (%r)'
              382  LOAD_FAST                'parse'
              384  BINARY_MODULO    

 L. 176       386  CALL_FUNCTION_1       1  ''
              388  RAISE_VARARGS_1       1  'exception instance'
            390_0  COME_FROM           376  '376'
            390_1  COME_FROM           238  '238'
              390  JUMP_FORWARD        436  'to 436'
            392_0  COME_FROM            34  '34'

 L. 179       392  LOAD_FAST                'e'
              394  LOAD_ATTR                tag
              396  LOAD_GLOBAL              XINCLUDE_FALLBACK
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   420  'to 420'

 L. 180       404  LOAD_GLOBAL              FatalIncludeError

 L. 181       406  LOAD_STR                 'xi:fallback tag must be child of xi:include (%r)'
              408  LOAD_FAST                'e'
              410  LOAD_ATTR                tag
              412  BINARY_MODULO    

 L. 180       414  CALL_FUNCTION_1       1  ''
              416  RAISE_VARARGS_1       1  'exception instance'
              418  JUMP_FORWARD        436  'to 436'
            420_0  COME_FROM           400  '400'

 L. 184       420  LOAD_GLOBAL              _include
              422  LOAD_FAST                'e'
              424  LOAD_FAST                'loader'
              426  LOAD_FAST                'base_url'
              428  LOAD_FAST                'max_depth'
              430  LOAD_FAST                '_parent_hrefs'
              432  CALL_FUNCTION_5       5  ''
              434  POP_TOP          
            436_0  COME_FROM           418  '418'
            436_1  COME_FROM           390  '390'

 L. 185       436  LOAD_FAST                'i'
              438  LOAD_CONST               1
              440  INPLACE_ADD      
              442  STORE_FAST               'i'
              444  JUMP_BACK             4  'to 4'
            446_0  COME_FROM            14  '14'

Parse error at or near `<118>' instruction at offset 86