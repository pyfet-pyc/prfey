# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: simplejson\decoder.py
"""Implementation of JSONDecoder
"""
from __future__ import absolute_import
import re, sys, struct
from .compat import PY3, unichr
from .scanner import make_scanner, JSONDecodeError

def _import_c_scanstring--- This code section failed: ---

 L.  11         0  SETUP_FINALLY        20  'to 20'

 L.  12         2  LOAD_CONST               1
                4  LOAD_CONST               ('scanstring',)
                6  IMPORT_NAME              _speedups
                8  IMPORT_FROM              scanstring
               10  STORE_FAST               'scanstring'
               12  POP_TOP          

 L.  13        14  LOAD_FAST                'scanstring'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  14        20  DUP_TOP          
               22  LOAD_GLOBAL              ImportError
               24  <121>                38  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  15        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
               38  <48>             

Parse error at or near `<121>' instruction at offset 24


c_scanstring = _import_c_scanstring()
__all__ = [
 'JSONDecoder']
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL

def _floatconstants():
    if sys.version_info < (2, 6):
        _BYTES = '7FF80000000000007FF0000000000000'.decode('hex')
        nan, inf = struct.unpack('>dd', _BYTES)
    else:
        nan = float('nan')
        inf = float('inf')
    return (nan, inf, -inf)


NaN, PosInf, NegInf = _floatconstants()
_CONSTANTS = {'-Infinity':NegInf, 
 'Infinity':PosInf, 
 'NaN':NaN}
STRINGCHUNK = re.compile('(.*?)(["\\\\\\x00-\\x1f])', FLAGS)
BACKSLASH = {'"':'"', 
 '\\':'\\',  '/':'/',  'b':'\x08', 
 'f':'\x0c',  'n':'\n',  'r':'\r',  't':'\t'}
DEFAULT_ENCODING = 'utf-8'

def py_scanstring--- This code section failed: ---

 L.  60         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  61         8  LOAD_GLOBAL              DEFAULT_ENCODING
               10  STORE_FAST               'encoding'
             12_0  COME_FROM             6  '6'

 L.  62        12  BUILD_LIST_0          0 
               14  STORE_FAST               'chunks'

 L.  63        16  LOAD_FAST                'chunks'
               18  LOAD_ATTR                append
               20  STORE_FAST               '_append'

 L.  64        22  LOAD_FAST                'end'
               24  LOAD_CONST               1
               26  BINARY_SUBTRACT  
               28  STORE_FAST               'begin'
             30_0  COME_FROM           654  '654'
             30_1  COME_FROM           168  '168'

 L.  66        30  LOAD_FAST                '_m'
               32  LOAD_FAST                's'
               34  LOAD_FAST                'end'
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'chunk'

 L.  67        40  LOAD_FAST                'chunk'
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.  68        48  LOAD_GLOBAL              JSONDecodeError

 L.  69        50  LOAD_STR                 'Unterminated string starting at'
               52  LOAD_FAST                's'
               54  LOAD_FAST                'begin'

 L.  68        56  CALL_FUNCTION_3       3  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            46  '46'

 L.  70        60  LOAD_FAST                'chunk'
               62  LOAD_METHOD              end
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'end'

 L.  71        68  LOAD_FAST                'chunk'
               70  LOAD_METHOD              groups
               72  CALL_METHOD_0         0  ''
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'content'
               78  STORE_FAST               'terminator'

 L.  73        80  LOAD_FAST                'content'
               82  POP_JUMP_IF_FALSE   116  'to 116'

 L.  74        84  LOAD_FAST                '_PY3'
               86  POP_JUMP_IF_TRUE    108  'to 108'
               88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'content'
               92  LOAD_GLOBAL              unicode
               94  CALL_FUNCTION_2       2  ''
               96  POP_JUMP_IF_TRUE    108  'to 108'

 L.  75        98  LOAD_GLOBAL              unicode
              100  LOAD_FAST                'content'
              102  LOAD_FAST                'encoding'
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'content'
            108_0  COME_FROM            96  '96'
            108_1  COME_FROM            86  '86'

 L.  76       108  LOAD_FAST                '_append'
              110  LOAD_FAST                'content'
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          
            116_0  COME_FROM            82  '82'

 L.  79       116  LOAD_FAST                'terminator'
              118  LOAD_STR                 '"'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   130  'to 130'

 L.  80   124_126  JUMP_FORWARD        656  'to 656'
              128  BREAK_LOOP          170  'to 170'
            130_0  COME_FROM           122  '122'

 L.  81       130  LOAD_FAST                'terminator'
              132  LOAD_STR                 '\\'
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_FALSE   170  'to 170'

 L.  82       138  LOAD_FAST                'strict'
              140  POP_JUMP_IF_FALSE   160  'to 160'

 L.  83       142  LOAD_STR                 'Invalid control character %r at'
              144  STORE_FAST               'msg'

 L.  84       146  LOAD_GLOBAL              JSONDecodeError
              148  LOAD_FAST                'msg'
              150  LOAD_FAST                's'
              152  LOAD_FAST                'end'
              154  CALL_FUNCTION_3       3  ''
              156  RAISE_VARARGS_1       1  'exception instance'
              158  JUMP_FORWARD        170  'to 170'
            160_0  COME_FROM           140  '140'

 L.  86       160  LOAD_FAST                '_append'
              162  LOAD_FAST                'terminator'
              164  CALL_FUNCTION_1       1  ''
              166  POP_TOP          

 L.  87       168  JUMP_BACK            30  'to 30'
            170_0  COME_FROM           158  '158'
            170_1  COME_FROM           136  '136'
            170_2  COME_FROM           128  '128'

 L.  88       170  SETUP_FINALLY       184  'to 184'

 L.  89       172  LOAD_FAST                's'
              174  LOAD_FAST                'end'
              176  BINARY_SUBSCR    
              178  STORE_FAST               'esc'
              180  POP_BLOCK        
              182  JUMP_FORWARD        214  'to 214'
            184_0  COME_FROM_FINALLY   170  '170'

 L.  90       184  DUP_TOP          
              186  LOAD_GLOBAL              IndexError
              188  <121>               212  ''
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L.  91       196  LOAD_GLOBAL              JSONDecodeError

 L.  92       198  LOAD_STR                 'Unterminated string starting at'
              200  LOAD_FAST                's'
              202  LOAD_FAST                'begin'

 L.  91       204  CALL_FUNCTION_3       3  ''
              206  RAISE_VARARGS_1       1  'exception instance'
              208  POP_EXCEPT       
              210  JUMP_FORWARD        214  'to 214'
              212  <48>             
            214_0  COME_FROM           210  '210'
            214_1  COME_FROM           182  '182'

 L.  94       214  LOAD_FAST                'esc'
              216  LOAD_STR                 'u'
              218  COMPARE_OP               !=
          220_222  POP_JUMP_IF_FALSE   286  'to 286'

 L.  95       224  SETUP_FINALLY       238  'to 238'

 L.  96       226  LOAD_FAST                '_b'
              228  LOAD_FAST                'esc'
              230  BINARY_SUBSCR    
              232  STORE_FAST               'char'
              234  POP_BLOCK        
              236  JUMP_FORWARD        274  'to 274'
            238_0  COME_FROM_FINALLY   224  '224'

 L.  97       238  DUP_TOP          
              240  LOAD_GLOBAL              KeyError
          242_244  <121>               272  ''
              246  POP_TOP          
              248  POP_TOP          
              250  POP_TOP          

 L.  98       252  LOAD_STR                 'Invalid \\X escape sequence %r'
              254  STORE_FAST               'msg'

 L.  99       256  LOAD_GLOBAL              JSONDecodeError
              258  LOAD_FAST                'msg'
              260  LOAD_FAST                's'
              262  LOAD_FAST                'end'
              264  CALL_FUNCTION_3       3  ''
              266  RAISE_VARARGS_1       1  'exception instance'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
              272  <48>             
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           236  '236'

 L. 100       274  LOAD_FAST                'end'
              276  LOAD_CONST               1
              278  INPLACE_ADD      
              280  STORE_FAST               'end'
          282_284  JUMP_FORWARD        646  'to 646'
            286_0  COME_FROM           220  '220'

 L. 103       286  LOAD_STR                 'Invalid \\uXXXX escape sequence'
              288  STORE_FAST               'msg'

 L. 104       290  LOAD_FAST                's'
              292  LOAD_FAST                'end'
              294  LOAD_CONST               1
              296  BINARY_ADD       
              298  LOAD_FAST                'end'
              300  LOAD_CONST               5
              302  BINARY_ADD       
              304  BUILD_SLICE_2         2 
              306  BINARY_SUBSCR    
              308  STORE_FAST               'esc'

 L. 105       310  LOAD_FAST                'esc'
              312  LOAD_CONST               1
              314  LOAD_CONST               2
              316  BUILD_SLICE_2         2 
              318  BINARY_SUBSCR    
              320  STORE_FAST               'escX'

 L. 106       322  LOAD_GLOBAL              len
              324  LOAD_FAST                'esc'
              326  CALL_FUNCTION_1       1  ''
              328  LOAD_CONST               4
              330  COMPARE_OP               !=
          332_334  POP_JUMP_IF_TRUE    356  'to 356'
              336  LOAD_FAST                'escX'
              338  LOAD_STR                 'x'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_TRUE    356  'to 356'
              346  LOAD_FAST                'escX'
              348  LOAD_STR                 'X'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   372  'to 372'
            356_0  COME_FROM           342  '342'
            356_1  COME_FROM           332  '332'

 L. 107       356  LOAD_GLOBAL              JSONDecodeError
              358  LOAD_FAST                'msg'
              360  LOAD_FAST                's'
              362  LOAD_FAST                'end'
              364  LOAD_CONST               1
              366  BINARY_SUBTRACT  
              368  CALL_FUNCTION_3       3  ''
              370  RAISE_VARARGS_1       1  'exception instance'
            372_0  COME_FROM           352  '352'

 L. 108       372  SETUP_FINALLY       388  'to 388'

 L. 109       374  LOAD_GLOBAL              int
              376  LOAD_FAST                'esc'
              378  LOAD_CONST               16
              380  CALL_FUNCTION_2       2  ''
              382  STORE_FAST               'uni'
              384  POP_BLOCK        
              386  JUMP_FORWARD        424  'to 424'
            388_0  COME_FROM_FINALLY   372  '372'

 L. 110       388  DUP_TOP          
              390  LOAD_GLOBAL              ValueError
          392_394  <121>               422  ''
              396  POP_TOP          
              398  POP_TOP          
              400  POP_TOP          

 L. 111       402  LOAD_GLOBAL              JSONDecodeError
              404  LOAD_FAST                'msg'
              406  LOAD_FAST                's'
              408  LOAD_FAST                'end'
              410  LOAD_CONST               1
              412  BINARY_SUBTRACT  
              414  CALL_FUNCTION_3       3  ''
              416  RAISE_VARARGS_1       1  'exception instance'
              418  POP_EXCEPT       
              420  JUMP_FORWARD        424  'to 424'
              422  <48>             
            424_0  COME_FROM           420  '420'
            424_1  COME_FROM           386  '386'

 L. 112       424  LOAD_FAST                'end'
              426  LOAD_CONST               5
              428  INPLACE_ADD      
              430  STORE_FAST               'end'

 L. 116       432  LOAD_FAST                '_maxunicode'
              434  LOAD_CONST               65535
              436  COMPARE_OP               >
          438_440  POP_JUMP_IF_FALSE   638  'to 638'

 L. 117       442  LOAD_FAST                'uni'
              444  LOAD_CONST               64512
              446  BINARY_AND       
              448  LOAD_CONST               55296
              450  COMPARE_OP               ==

 L. 116   452_454  POP_JUMP_IF_FALSE   638  'to 638'

 L. 118       456  LOAD_FAST                's'
              458  LOAD_FAST                'end'
              460  LOAD_FAST                'end'
              462  LOAD_CONST               2
              464  BINARY_ADD       
              466  BUILD_SLICE_2         2 
              468  BINARY_SUBSCR    
              470  LOAD_STR                 '\\u'
              472  COMPARE_OP               ==

 L. 116   474_476  POP_JUMP_IF_FALSE   638  'to 638'

 L. 119       478  LOAD_FAST                's'
              480  LOAD_FAST                'end'
              482  LOAD_CONST               2
              484  BINARY_ADD       
              486  LOAD_FAST                'end'
              488  LOAD_CONST               6
              490  BINARY_ADD       
              492  BUILD_SLICE_2         2 
              494  BINARY_SUBSCR    
              496  STORE_FAST               'esc2'

 L. 120       498  LOAD_FAST                'esc2'
              500  LOAD_CONST               1
              502  LOAD_CONST               2
              504  BUILD_SLICE_2         2 
              506  BINARY_SUBSCR    
              508  STORE_FAST               'escX'

 L. 121       510  LOAD_GLOBAL              len
              512  LOAD_FAST                'esc2'
              514  CALL_FUNCTION_1       1  ''
              516  LOAD_CONST               4
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   638  'to 638'
              524  LOAD_FAST                'escX'
              526  LOAD_STR                 'x'
              528  COMPARE_OP               ==
          530_532  POP_JUMP_IF_TRUE    638  'to 638'
              534  LOAD_FAST                'escX'
              536  LOAD_STR                 'X'
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_TRUE    638  'to 638'

 L. 122       544  SETUP_FINALLY       560  'to 560'

 L. 123       546  LOAD_GLOBAL              int
              548  LOAD_FAST                'esc2'
              550  LOAD_CONST               16
              552  CALL_FUNCTION_2       2  ''
              554  STORE_FAST               'uni2'
              556  POP_BLOCK        
              558  JUMP_FORWARD        592  'to 592'
            560_0  COME_FROM_FINALLY   544  '544'

 L. 124       560  DUP_TOP          
              562  LOAD_GLOBAL              ValueError
          564_566  <121>               590  ''
              568  POP_TOP          
              570  POP_TOP          
              572  POP_TOP          

 L. 125       574  LOAD_GLOBAL              JSONDecodeError
              576  LOAD_FAST                'msg'
              578  LOAD_FAST                's'
              580  LOAD_FAST                'end'
              582  CALL_FUNCTION_3       3  ''
              584  RAISE_VARARGS_1       1  'exception instance'
              586  POP_EXCEPT       
              588  JUMP_FORWARD        592  'to 592'
              590  <48>             
            592_0  COME_FROM           588  '588'
            592_1  COME_FROM           558  '558'

 L. 126       592  LOAD_FAST                'uni2'
              594  LOAD_CONST               64512
              596  BINARY_AND       
              598  LOAD_CONST               56320
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   638  'to 638'

 L. 127       606  LOAD_CONST               65536
              608  LOAD_FAST                'uni'
              610  LOAD_CONST               55296
              612  BINARY_SUBTRACT  
              614  LOAD_CONST               10
              616  BINARY_LSHIFT    

 L. 128       618  LOAD_FAST                'uni2'
              620  LOAD_CONST               56320
              622  BINARY_SUBTRACT  

 L. 127       624  BINARY_OR        
              626  BINARY_ADD       
              628  STORE_FAST               'uni'

 L. 129       630  LOAD_FAST                'end'
              632  LOAD_CONST               6
              634  INPLACE_ADD      
              636  STORE_FAST               'end'
            638_0  COME_FROM           602  '602'
            638_1  COME_FROM           540  '540'
            638_2  COME_FROM           530  '530'
            638_3  COME_FROM           520  '520'
            638_4  COME_FROM           474  '474'
            638_5  COME_FROM           452  '452'
            638_6  COME_FROM           438  '438'

 L. 130       638  LOAD_GLOBAL              unichr
              640  LOAD_FAST                'uni'
              642  CALL_FUNCTION_1       1  ''
              644  STORE_FAST               'char'
            646_0  COME_FROM           282  '282'

 L. 132       646  LOAD_FAST                '_append'
              648  LOAD_FAST                'char'
              650  CALL_FUNCTION_1       1  ''
              652  POP_TOP          
              654  JUMP_BACK            30  'to 30'
            656_0  COME_FROM           124  '124'

 L. 133       656  LOAD_FAST                '_join'
              658  LOAD_FAST                'chunks'
              660  CALL_FUNCTION_1       1  ''
              662  LOAD_FAST                'end'
              664  BUILD_TUPLE_2         2 
              666  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


scanstring = c_scanstring or py_scanstring
WHITESPACE = re.compile('[ \\t\\n\\r]*', FLAGS)
WHITESPACE_STR = ' \t\n\r'

def JSONObject--- This code section failed: ---

 L. 145         0  LOAD_FAST                'state'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               's'
                6  STORE_FAST               'end'

 L. 147         8  LOAD_FAST                'memo'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 148        16  BUILD_MAP_0           0 
               18  STORE_FAST               'memo'
             20_0  COME_FROM            14  '14'

 L. 149        20  LOAD_FAST                'memo'
               22  LOAD_ATTR                setdefault
               24  STORE_FAST               'memo_get'

 L. 150        26  BUILD_LIST_0          0 
               28  STORE_FAST               'pairs'

 L. 153        30  LOAD_FAST                's'
               32  LOAD_FAST                'end'
               34  LOAD_FAST                'end'
               36  LOAD_CONST               1
               38  BINARY_ADD       
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  STORE_FAST               'nextchar'

 L. 155        46  LOAD_FAST                'nextchar'
               48  LOAD_STR                 '"'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE   180  'to 180'

 L. 156        54  LOAD_FAST                'nextchar'
               56  LOAD_FAST                '_ws'
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    92  'to 92'

 L. 157        62  LOAD_FAST                '_w'
               64  LOAD_FAST                's'
               66  LOAD_FAST                'end'
               68  CALL_FUNCTION_2       2  ''
               70  LOAD_METHOD              end
               72  CALL_METHOD_0         0  ''
               74  STORE_FAST               'end'

 L. 158        76  LOAD_FAST                's'
               78  LOAD_FAST                'end'
               80  LOAD_FAST                'end'
               82  LOAD_CONST               1
               84  BINARY_ADD       
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  STORE_FAST               'nextchar'
             92_0  COME_FROM            60  '60'

 L. 160        92  LOAD_FAST                'nextchar'
               94  LOAD_STR                 '}'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   160  'to 160'

 L. 161       100  LOAD_FAST                'object_pairs_hook'
              102  LOAD_CONST               None
              104  <117>                 1  ''
              106  POP_JUMP_IF_FALSE   128  'to 128'

 L. 162       108  LOAD_FAST                'object_pairs_hook'
              110  LOAD_FAST                'pairs'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'result'

 L. 163       116  LOAD_FAST                'result'
              118  LOAD_FAST                'end'
              120  LOAD_CONST               1
              122  BINARY_ADD       
              124  BUILD_TUPLE_2         2 
              126  RETURN_VALUE     
            128_0  COME_FROM           106  '106'

 L. 164       128  BUILD_MAP_0           0 
              130  STORE_FAST               'pairs'

 L. 165       132  LOAD_FAST                'object_hook'
              134  LOAD_CONST               None
              136  <117>                 1  ''
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L. 166       140  LOAD_FAST                'object_hook'
              142  LOAD_FAST                'pairs'
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'pairs'
            148_0  COME_FROM           138  '138'

 L. 167       148  LOAD_FAST                'pairs'
              150  LOAD_FAST                'end'
              152  LOAD_CONST               1
              154  BINARY_ADD       
              156  BUILD_TUPLE_2         2 
              158  RETURN_VALUE     
            160_0  COME_FROM            98  '98'

 L. 168       160  LOAD_FAST                'nextchar'
              162  LOAD_STR                 '"'
              164  COMPARE_OP               !=
              166  POP_JUMP_IF_FALSE   180  'to 180'

 L. 169       168  LOAD_GLOBAL              JSONDecodeError

 L. 170       170  LOAD_STR                 'Expecting property name enclosed in double quotes'

 L. 171       172  LOAD_FAST                's'
              174  LOAD_FAST                'end'

 L. 169       176  CALL_FUNCTION_3       3  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           166  '166'
            180_1  COME_FROM            52  '52'

 L. 172       180  LOAD_FAST                'end'
              182  LOAD_CONST               1
              184  INPLACE_ADD      
              186  STORE_FAST               'end'
            188_0  COME_FROM           658  '658'
            188_1  COME_FROM           640  '640'

 L. 174       188  LOAD_GLOBAL              scanstring
              190  LOAD_FAST                's'
              192  LOAD_FAST                'end'
              194  LOAD_FAST                'encoding'
              196  LOAD_FAST                'strict'
              198  CALL_FUNCTION_4       4  ''
              200  UNPACK_SEQUENCE_2     2 
              202  STORE_FAST               'key'
              204  STORE_FAST               'end'

 L. 175       206  LOAD_FAST                'memo_get'
              208  LOAD_FAST                'key'
              210  LOAD_FAST                'key'
              212  CALL_FUNCTION_2       2  ''
              214  STORE_FAST               'key'

 L. 179       216  LOAD_FAST                's'
              218  LOAD_FAST                'end'
              220  LOAD_FAST                'end'
              222  LOAD_CONST               1
              224  BINARY_ADD       
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  LOAD_STR                 ':'
              232  COMPARE_OP               !=
          234_236  POP_JUMP_IF_FALSE   286  'to 286'

 L. 180       238  LOAD_FAST                '_w'
              240  LOAD_FAST                's'
              242  LOAD_FAST                'end'
              244  CALL_FUNCTION_2       2  ''
              246  LOAD_METHOD              end
              248  CALL_METHOD_0         0  ''
              250  STORE_FAST               'end'

 L. 181       252  LOAD_FAST                's'
              254  LOAD_FAST                'end'
              256  LOAD_FAST                'end'
              258  LOAD_CONST               1
              260  BINARY_ADD       
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  LOAD_STR                 ':'
              268  COMPARE_OP               !=
          270_272  POP_JUMP_IF_FALSE   286  'to 286'

 L. 182       274  LOAD_GLOBAL              JSONDecodeError
              276  LOAD_STR                 "Expecting ':' delimiter"
              278  LOAD_FAST                's'
              280  LOAD_FAST                'end'
              282  CALL_FUNCTION_3       3  ''
              284  RAISE_VARARGS_1       1  'exception instance'
            286_0  COME_FROM           270  '270'
            286_1  COME_FROM           234  '234'

 L. 184       286  LOAD_FAST                'end'
              288  LOAD_CONST               1
              290  INPLACE_ADD      
              292  STORE_FAST               'end'

 L. 186       294  SETUP_FINALLY       354  'to 354'

 L. 187       296  LOAD_FAST                's'
              298  LOAD_FAST                'end'
              300  BINARY_SUBSCR    
              302  LOAD_FAST                '_ws'
              304  <118>                 0  ''
          306_308  POP_JUMP_IF_FALSE   350  'to 350'

 L. 188       310  LOAD_FAST                'end'
              312  LOAD_CONST               1
              314  INPLACE_ADD      
              316  STORE_FAST               'end'

 L. 189       318  LOAD_FAST                's'
              320  LOAD_FAST                'end'
              322  BINARY_SUBSCR    
              324  LOAD_FAST                '_ws'
              326  <118>                 0  ''
          328_330  POP_JUMP_IF_FALSE   350  'to 350'

 L. 190       332  LOAD_FAST                '_w'
              334  LOAD_FAST                's'
              336  LOAD_FAST                'end'
              338  LOAD_CONST               1
              340  BINARY_ADD       
              342  CALL_FUNCTION_2       2  ''
              344  LOAD_METHOD              end
              346  CALL_METHOD_0         0  ''
              348  STORE_FAST               'end'
            350_0  COME_FROM           328  '328'
            350_1  COME_FROM           306  '306'
              350  POP_BLOCK        
              352  JUMP_FORWARD        374  'to 374'
            354_0  COME_FROM_FINALLY   294  '294'

 L. 191       354  DUP_TOP          
              356  LOAD_GLOBAL              IndexError
          358_360  <121>               372  ''
              362  POP_TOP          
              364  POP_TOP          
              366  POP_TOP          

 L. 192       368  POP_EXCEPT       
              370  BREAK_LOOP          374  'to 374'
              372  <48>             
            374_0  COME_FROM           370  '370'
            374_1  COME_FROM           352  '352'

 L. 194       374  LOAD_FAST                'scan_once'
              376  LOAD_FAST                's'
              378  LOAD_FAST                'end'
              380  CALL_FUNCTION_2       2  ''
              382  UNPACK_SEQUENCE_2     2 
              384  STORE_FAST               'value'
              386  STORE_FAST               'end'

 L. 195       388  LOAD_FAST                'pairs'
              390  LOAD_METHOD              append
              392  LOAD_FAST                'key'
              394  LOAD_FAST                'value'
              396  BUILD_TUPLE_2         2 
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          

 L. 197       402  SETUP_FINALLY       452  'to 452'

 L. 198       404  LOAD_FAST                's'
              406  LOAD_FAST                'end'
              408  BINARY_SUBSCR    
              410  STORE_FAST               'nextchar'

 L. 199       412  LOAD_FAST                'nextchar'
              414  LOAD_FAST                '_ws'
              416  <118>                 0  ''
          418_420  POP_JUMP_IF_FALSE   448  'to 448'

 L. 200       422  LOAD_FAST                '_w'
              424  LOAD_FAST                's'
              426  LOAD_FAST                'end'
              428  LOAD_CONST               1
              430  BINARY_ADD       
              432  CALL_FUNCTION_2       2  ''
              434  LOAD_METHOD              end
              436  CALL_METHOD_0         0  ''
              438  STORE_FAST               'end'

 L. 201       440  LOAD_FAST                's'
              442  LOAD_FAST                'end'
              444  BINARY_SUBSCR    
              446  STORE_FAST               'nextchar'
            448_0  COME_FROM           418  '418'
              448  POP_BLOCK        
              450  JUMP_FORWARD        476  'to 476'
            452_0  COME_FROM_FINALLY   402  '402'

 L. 202       452  DUP_TOP          
              454  LOAD_GLOBAL              IndexError
          456_458  <121>               474  ''
              460  POP_TOP          
              462  POP_TOP          
              464  POP_TOP          

 L. 203       466  LOAD_STR                 ''
              468  STORE_FAST               'nextchar'
              470  POP_EXCEPT       
              472  JUMP_FORWARD        476  'to 476'
              474  <48>             
            476_0  COME_FROM           472  '472'
            476_1  COME_FROM           450  '450'

 L. 204       476  LOAD_FAST                'end'
              478  LOAD_CONST               1
              480  INPLACE_ADD      
              482  STORE_FAST               'end'

 L. 206       484  LOAD_FAST                'nextchar'
              486  LOAD_STR                 '}'
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   500  'to 500'

 L. 207   494_496  JUMP_FORWARD        660  'to 660'
              498  BREAK_LOOP          526  'to 526'
            500_0  COME_FROM           490  '490'

 L. 208       500  LOAD_FAST                'nextchar'
              502  LOAD_STR                 ','
              504  COMPARE_OP               !=
          506_508  POP_JUMP_IF_FALSE   526  'to 526'

 L. 209       510  LOAD_GLOBAL              JSONDecodeError
              512  LOAD_STR                 "Expecting ',' delimiter or '}'"
              514  LOAD_FAST                's'
              516  LOAD_FAST                'end'
              518  LOAD_CONST               1
              520  BINARY_SUBTRACT  
              522  CALL_FUNCTION_3       3  ''
              524  RAISE_VARARGS_1       1  'exception instance'
            526_0  COME_FROM           506  '506'
            526_1  COME_FROM           498  '498'

 L. 211       526  SETUP_FINALLY       602  'to 602'

 L. 212       528  LOAD_FAST                's'
              530  LOAD_FAST                'end'
              532  BINARY_SUBSCR    
              534  STORE_FAST               'nextchar'

 L. 213       536  LOAD_FAST                'nextchar'
              538  LOAD_FAST                '_ws'
              540  <118>                 0  ''
          542_544  POP_JUMP_IF_FALSE   598  'to 598'

 L. 214       546  LOAD_FAST                'end'
              548  LOAD_CONST               1
              550  INPLACE_ADD      
              552  STORE_FAST               'end'

 L. 215       554  LOAD_FAST                's'
              556  LOAD_FAST                'end'
              558  BINARY_SUBSCR    
              560  STORE_FAST               'nextchar'

 L. 216       562  LOAD_FAST                'nextchar'
              564  LOAD_FAST                '_ws'
              566  <118>                 0  ''
          568_570  POP_JUMP_IF_FALSE   598  'to 598'

 L. 217       572  LOAD_FAST                '_w'
              574  LOAD_FAST                's'
              576  LOAD_FAST                'end'
              578  LOAD_CONST               1
              580  BINARY_ADD       
              582  CALL_FUNCTION_2       2  ''
              584  LOAD_METHOD              end
              586  CALL_METHOD_0         0  ''
              588  STORE_FAST               'end'

 L. 218       590  LOAD_FAST                's'
              592  LOAD_FAST                'end'
              594  BINARY_SUBSCR    
              596  STORE_FAST               'nextchar'
            598_0  COME_FROM           568  '568'
            598_1  COME_FROM           542  '542'
              598  POP_BLOCK        
              600  JUMP_FORWARD        626  'to 626'
            602_0  COME_FROM_FINALLY   526  '526'

 L. 219       602  DUP_TOP          
              604  LOAD_GLOBAL              IndexError
          606_608  <121>               624  ''
              610  POP_TOP          
              612  POP_TOP          
              614  POP_TOP          

 L. 220       616  LOAD_STR                 ''
              618  STORE_FAST               'nextchar'
              620  POP_EXCEPT       
              622  JUMP_FORWARD        626  'to 626'
              624  <48>             
            626_0  COME_FROM           622  '622'
            626_1  COME_FROM           600  '600'

 L. 222       626  LOAD_FAST                'end'
              628  LOAD_CONST               1
              630  INPLACE_ADD      
              632  STORE_FAST               'end'

 L. 223       634  LOAD_FAST                'nextchar'
              636  LOAD_STR                 '"'
              638  COMPARE_OP               !=
              640  POP_JUMP_IF_FALSE_BACK   188  'to 188'

 L. 224       642  LOAD_GLOBAL              JSONDecodeError

 L. 225       644  LOAD_STR                 'Expecting property name enclosed in double quotes'

 L. 226       646  LOAD_FAST                's'
              648  LOAD_FAST                'end'
              650  LOAD_CONST               1
              652  BINARY_SUBTRACT  

 L. 224       654  CALL_FUNCTION_3       3  ''
              656  RAISE_VARARGS_1       1  'exception instance'
              658  JUMP_BACK           188  'to 188'
            660_0  COME_FROM           494  '494'

 L. 228       660  LOAD_FAST                'object_pairs_hook'
              662  LOAD_CONST               None
              664  <117>                 1  ''
          666_668  POP_JUMP_IF_FALSE   686  'to 686'

 L. 229       670  LOAD_FAST                'object_pairs_hook'
              672  LOAD_FAST                'pairs'
              674  CALL_FUNCTION_1       1  ''
              676  STORE_FAST               'result'

 L. 230       678  LOAD_FAST                'result'
              680  LOAD_FAST                'end'
              682  BUILD_TUPLE_2         2 
              684  RETURN_VALUE     
            686_0  COME_FROM           666  '666'

 L. 231       686  LOAD_GLOBAL              dict
              688  LOAD_FAST                'pairs'
              690  CALL_FUNCTION_1       1  ''
              692  STORE_FAST               'pairs'

 L. 232       694  LOAD_FAST                'object_hook'
              696  LOAD_CONST               None
              698  <117>                 1  ''
          700_702  POP_JUMP_IF_FALSE   712  'to 712'

 L. 233       704  LOAD_FAST                'object_hook'
              706  LOAD_FAST                'pairs'
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'pairs'
            712_0  COME_FROM           700  '700'

 L. 234       712  LOAD_FAST                'pairs'
              714  LOAD_FAST                'end'
              716  BUILD_TUPLE_2         2 
              718  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12


def JSONArray--- This code section failed: ---

 L. 237         0  LOAD_FAST                'state'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               's'
                6  STORE_FAST               'end'

 L. 238         8  BUILD_LIST_0          0 
               10  STORE_FAST               'values'

 L. 239        12  LOAD_FAST                's'
               14  LOAD_FAST                'end'
               16  LOAD_FAST                'end'
               18  LOAD_CONST               1
               20  BINARY_ADD       
               22  BUILD_SLICE_2         2 
               24  BINARY_SUBSCR    
               26  STORE_FAST               'nextchar'

 L. 240        28  LOAD_FAST                'nextchar'
               30  LOAD_FAST                '_ws'
               32  <118>                 0  ''
               34  POP_JUMP_IF_FALSE    70  'to 70'

 L. 241        36  LOAD_FAST                '_w'
               38  LOAD_FAST                's'
               40  LOAD_FAST                'end'
               42  LOAD_CONST               1
               44  BINARY_ADD       
               46  CALL_FUNCTION_2       2  ''
               48  LOAD_METHOD              end
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'end'

 L. 242        54  LOAD_FAST                's'
               56  LOAD_FAST                'end'
               58  LOAD_FAST                'end'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  BUILD_SLICE_2         2 
               66  BINARY_SUBSCR    
               68  STORE_FAST               'nextchar'
             70_0  COME_FROM            34  '34'

 L. 244        70  LOAD_FAST                'nextchar'
               72  LOAD_STR                 ']'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 245        78  LOAD_FAST                'values'
               80  LOAD_FAST                'end'
               82  LOAD_CONST               1
               84  BINARY_ADD       
               86  BUILD_TUPLE_2         2 
               88  RETURN_VALUE     
             90_0  COME_FROM            76  '76'

 L. 246        90  LOAD_FAST                'nextchar'
               92  LOAD_STR                 ''
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 247        98  LOAD_GLOBAL              JSONDecodeError
              100  LOAD_STR                 "Expecting value or ']'"
              102  LOAD_FAST                's'
              104  LOAD_FAST                'end'
              106  CALL_FUNCTION_3       3  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            96  '96'

 L. 248       110  LOAD_FAST                'values'
              112  LOAD_ATTR                append
              114  STORE_FAST               '_append'
            116_0  COME_FROM           322  '322'
            116_1  COME_FROM           318  '318'
            116_2  COME_FROM           300  '300'

 L. 250       116  LOAD_FAST                'scan_once'
              118  LOAD_FAST                's'
              120  LOAD_FAST                'end'
              122  CALL_FUNCTION_2       2  ''
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'value'
              128  STORE_FAST               'end'

 L. 251       130  LOAD_FAST                '_append'
              132  LOAD_FAST                'value'
              134  CALL_FUNCTION_1       1  ''
              136  POP_TOP          

 L. 252       138  LOAD_FAST                's'
              140  LOAD_FAST                'end'
              142  LOAD_FAST                'end'
              144  LOAD_CONST               1
              146  BINARY_ADD       
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  STORE_FAST               'nextchar'

 L. 253       154  LOAD_FAST                'nextchar'
              156  LOAD_FAST                '_ws'
              158  <118>                 0  ''
              160  POP_JUMP_IF_FALSE   196  'to 196'

 L. 254       162  LOAD_FAST                '_w'
              164  LOAD_FAST                's'
              166  LOAD_FAST                'end'
              168  LOAD_CONST               1
              170  BINARY_ADD       
              172  CALL_FUNCTION_2       2  ''
              174  LOAD_METHOD              end
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'end'

 L. 255       180  LOAD_FAST                's'
              182  LOAD_FAST                'end'
              184  LOAD_FAST                'end'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  STORE_FAST               'nextchar'
            196_0  COME_FROM           160  '160'

 L. 256       196  LOAD_FAST                'end'
              198  LOAD_CONST               1
              200  INPLACE_ADD      
              202  STORE_FAST               'end'

 L. 257       204  LOAD_FAST                'nextchar'
              206  LOAD_STR                 ']'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   218  'to 218'

 L. 258   212_214  JUMP_FORWARD        324  'to 324'
              216  BREAK_LOOP          242  'to 242'
            218_0  COME_FROM           210  '210'

 L. 259       218  LOAD_FAST                'nextchar'
              220  LOAD_STR                 ','
              222  COMPARE_OP               !=
              224  POP_JUMP_IF_FALSE   242  'to 242'

 L. 260       226  LOAD_GLOBAL              JSONDecodeError
              228  LOAD_STR                 "Expecting ',' delimiter or ']'"
              230  LOAD_FAST                's'
              232  LOAD_FAST                'end'
              234  LOAD_CONST               1
              236  BINARY_SUBTRACT  
              238  CALL_FUNCTION_3       3  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           224  '224'
            242_1  COME_FROM           216  '216'

 L. 262       242  SETUP_FINALLY       302  'to 302'

 L. 263       244  LOAD_FAST                's'
              246  LOAD_FAST                'end'
              248  BINARY_SUBSCR    
              250  LOAD_FAST                '_ws'
              252  <118>                 0  ''
          254_256  POP_JUMP_IF_FALSE   298  'to 298'

 L. 264       258  LOAD_FAST                'end'
              260  LOAD_CONST               1
              262  INPLACE_ADD      
              264  STORE_FAST               'end'

 L. 265       266  LOAD_FAST                's'
              268  LOAD_FAST                'end'
              270  BINARY_SUBSCR    
              272  LOAD_FAST                '_ws'
              274  <118>                 0  ''
          276_278  POP_JUMP_IF_FALSE   298  'to 298'

 L. 266       280  LOAD_FAST                '_w'
              282  LOAD_FAST                's'
              284  LOAD_FAST                'end'
              286  LOAD_CONST               1
              288  BINARY_ADD       
              290  CALL_FUNCTION_2       2  ''
              292  LOAD_METHOD              end
              294  CALL_METHOD_0         0  ''
              296  STORE_FAST               'end'
            298_0  COME_FROM           276  '276'
            298_1  COME_FROM           254  '254'
              298  POP_BLOCK        
              300  JUMP_BACK           116  'to 116'
            302_0  COME_FROM_FINALLY   242  '242'

 L. 267       302  DUP_TOP          
              304  LOAD_GLOBAL              IndexError
          306_308  <121>               320  ''
              310  POP_TOP          
              312  POP_TOP          
              314  POP_TOP          

 L. 268       316  POP_EXCEPT       
              318  JUMP_BACK           116  'to 116'
              320  <48>             
              322  JUMP_BACK           116  'to 116'
            324_0  COME_FROM           212  '212'

 L. 270       324  LOAD_FAST                'values'
              326  LOAD_FAST                'end'
              328  BUILD_TUPLE_2         2 
              330  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 32


class JSONDecoder(object):
    __doc__ = 'Simple JSON <http://json.org> decoder\n\n    Performs the following translations in decoding by default:\n\n    +---------------+-------------------+\n    | JSON          | Python            |\n    +===============+===================+\n    | object        | dict              |\n    +---------------+-------------------+\n    | array         | list              |\n    +---------------+-------------------+\n    | string        | str, unicode      |\n    +---------------+-------------------+\n    | number (int)  | int, long         |\n    +---------------+-------------------+\n    | number (real) | float             |\n    +---------------+-------------------+\n    | true          | True              |\n    +---------------+-------------------+\n    | false         | False             |\n    +---------------+-------------------+\n    | null          | None              |\n    +---------------+-------------------+\n\n    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as\n    their corresponding ``float`` values, which is outside the JSON spec.\n\n    '

    def __init__--- This code section failed: ---

 L. 348         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 349         8  LOAD_GLOBAL              DEFAULT_ENCODING
               10  STORE_FAST               'encoding'
             12_0  COME_FROM             6  '6'

 L. 350        12  LOAD_FAST                'encoding'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               encoding

 L. 351        18  LOAD_FAST                'object_hook'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               object_hook

 L. 352        24  LOAD_FAST                'object_pairs_hook'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               object_pairs_hook

 L. 353        30  LOAD_FAST                'parse_float'
               32  JUMP_IF_TRUE_OR_POP    36  'to 36'
               34  LOAD_GLOBAL              float
             36_0  COME_FROM            32  '32'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               parse_float

 L. 354        40  LOAD_FAST                'parse_int'
               42  JUMP_IF_TRUE_OR_POP    46  'to 46'
               44  LOAD_GLOBAL              int
             46_0  COME_FROM            42  '42'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               parse_int

 L. 355        50  LOAD_FAST                'parse_constant'
               52  JUMP_IF_TRUE_OR_POP    58  'to 58'
               54  LOAD_GLOBAL              _CONSTANTS
               56  LOAD_ATTR                __getitem__
             58_0  COME_FROM            52  '52'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               parse_constant

 L. 356        62  LOAD_FAST                'strict'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               strict

 L. 357        68  LOAD_GLOBAL              JSONObject
               70  LOAD_FAST                'self'
               72  STORE_ATTR               parse_object

 L. 358        74  LOAD_GLOBAL              JSONArray
               76  LOAD_FAST                'self'
               78  STORE_ATTR               parse_array

 L. 359        80  LOAD_GLOBAL              scanstring
               82  LOAD_FAST                'self'
               84  STORE_ATTR               parse_string

 L. 360        86  BUILD_MAP_0           0 
               88  LOAD_FAST                'self'
               90  STORE_ATTR               memo

 L. 361        92  LOAD_GLOBAL              make_scanner
               94  LOAD_FAST                'self'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_FAST                'self'
              100  STORE_ATTR               scan_once

Parse error at or near `None' instruction at offset -1

    def decode(self, s, _w=WHITESPACE.match, _PY3=PY3):
        """Return the Python representation of ``s`` (a ``str`` or ``unicode``
        instance containing a JSON document)

        """
        if _PY3:
            if isinstancesbytes:
                s = strsself.encoding
        obj, end = self.raw_decode(s)
        end = _wsend.end
        if end != len(s):
            raise JSONDecodeError'Extra data'sendlen(s)
        return obj

    def raw_decode(self, s, idx=0, _w=WHITESPACE.match, _PY3=PY3):
        """Decode a JSON document from ``s`` (a ``str`` or ``unicode``
        beginning with a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
        Optionally, ``idx`` can be used to specify an offset in ``s`` where
        the JSON document begins.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.

        """
        if idx < 0:
            raise JSONDecodeError('Expecting value', s, idx)
        if _PY3:
            if not isinstancesstr:
                raise TypeError('Input string must be text, not bytes')
            if len(s) > idx:
                ord0 = ord(s[idx])
                if ord0 == 65279:
                    idx += 1
                elif ord0 == 239:
                    if s[idx:idx + 3] == 'ï»¿':
                        idx += 3
            return self.scan_once(s, idx=(_wsidx.end))