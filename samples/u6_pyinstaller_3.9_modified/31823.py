# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: simplejson\scanner.py
"""JSON token scanner
"""
import re
from .errors import JSONDecodeError

def _import_c_make_scanner--- This code section failed: ---

 L.   6         0  SETUP_FINALLY        20  'to 20'

 L.   7         2  LOAD_CONST               1
                4  LOAD_CONST               ('make_scanner',)
                6  IMPORT_NAME              _speedups
                8  IMPORT_FROM              make_scanner
               10  STORE_FAST               'make_scanner'
               12  POP_TOP          

 L.   8        14  LOAD_FAST                'make_scanner'
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.   9        20  DUP_TOP          
               22  LOAD_GLOBAL              ImportError
               24  <121>                38  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  10        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
               38  <48>             

Parse error at or near `<121>' instruction at offset 24


c_make_scanner = _import_c_make_scanner()
__all__ = [
 'make_scanner', 'JSONDecodeError']
NUMBER_RE = re.compile('(-?(?:0|[1-9]\\d*))(\\.\\d+)?([eE][-+]?\\d+)?', re.VERBOSE | re.MULTILINE | re.DOTALL)

def py_make_scanner(context):
    parse_object = context.parse_object
    parse_array = context.parse_array
    parse_string = context.parse_string
    match_number = NUMBER_RE.match
    encoding = context.encoding
    strict = context.strict
    parse_float = context.parse_float
    parse_int = context.parse_int
    parse_constant = context.parse_constant
    object_hook = context.object_hook
    object_pairs_hook = context.object_pairs_hook
    memo = context.memo

    def _scan_once--- This code section failed: ---

 L.  35         0  LOAD_STR                 'Expecting value'
                2  STORE_FAST               'errmsg'

 L.  36         4  SETUP_FINALLY        18  'to 18'

 L.  37         6  LOAD_FAST                'string'
                8  LOAD_FAST                'idx'
               10  BINARY_SUBSCR    
               12  STORE_FAST               'nextchar'
               14  POP_BLOCK        
               16  JUMP_FORWARD         48  'to 48'
             18_0  COME_FROM_FINALLY     4  '4'

 L.  38        18  DUP_TOP          
               20  LOAD_GLOBAL              IndexError
               22  <121>                46  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  39        30  LOAD_GLOBAL              JSONDecodeError
               32  LOAD_FAST                'errmsg'
               34  LOAD_FAST                'string'
               36  LOAD_FAST                'idx'
               38  CALL_FUNCTION_3       3  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            16  '16'

 L.  41        48  LOAD_FAST                'nextchar'
               50  LOAD_STR                 '"'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    74  'to 74'

 L.  42        56  LOAD_DEREF               'parse_string'
               58  LOAD_FAST                'string'
               60  LOAD_FAST                'idx'
               62  LOAD_CONST               1
               64  BINARY_ADD       
               66  LOAD_DEREF               'encoding'
               68  LOAD_DEREF               'strict'
               70  CALL_FUNCTION_4       4  ''
               72  RETURN_VALUE     
             74_0  COME_FROM            54  '54'

 L.  43        74  LOAD_FAST                'nextchar'
               76  LOAD_STR                 '{'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   110  'to 110'

 L.  44        82  LOAD_DEREF               'parse_object'
               84  LOAD_FAST                'string'
               86  LOAD_FAST                'idx'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  BUILD_TUPLE_2         2 
               94  LOAD_DEREF               'encoding'
               96  LOAD_DEREF               'strict'

 L.  45        98  LOAD_DEREF               '_scan_once'
              100  LOAD_DEREF               'object_hook'
              102  LOAD_DEREF               'object_pairs_hook'
              104  LOAD_DEREF               'memo'

 L.  44       106  CALL_FUNCTION_7       7  ''
              108  RETURN_VALUE     
            110_0  COME_FROM            80  '80'

 L.  46       110  LOAD_FAST                'nextchar'
              112  LOAD_STR                 '['
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L.  47       118  LOAD_DEREF               'parse_array'
              120  LOAD_FAST                'string'
              122  LOAD_FAST                'idx'
              124  LOAD_CONST               1
              126  BINARY_ADD       
              128  BUILD_TUPLE_2         2 
              130  LOAD_DEREF               '_scan_once'
              132  CALL_FUNCTION_2       2  ''
              134  RETURN_VALUE     
            136_0  COME_FROM           116  '116'

 L.  48       136  LOAD_FAST                'nextchar'
              138  LOAD_STR                 'n'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   176  'to 176'
              144  LOAD_FAST                'string'
              146  LOAD_FAST                'idx'
              148  LOAD_FAST                'idx'
              150  LOAD_CONST               4
              152  BINARY_ADD       
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  LOAD_STR                 'null'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   176  'to 176'

 L.  49       164  LOAD_CONST               None
              166  LOAD_FAST                'idx'
              168  LOAD_CONST               4
              170  BINARY_ADD       
              172  BUILD_TUPLE_2         2 
              174  RETURN_VALUE     
            176_0  COME_FROM           162  '162'
            176_1  COME_FROM           142  '142'

 L.  50       176  LOAD_FAST                'nextchar'
              178  LOAD_STR                 't'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   216  'to 216'
              184  LOAD_FAST                'string'
              186  LOAD_FAST                'idx'
              188  LOAD_FAST                'idx'
              190  LOAD_CONST               4
              192  BINARY_ADD       
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  LOAD_STR                 'true'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   216  'to 216'

 L.  51       204  LOAD_CONST               True
              206  LOAD_FAST                'idx'
              208  LOAD_CONST               4
              210  BINARY_ADD       
              212  BUILD_TUPLE_2         2 
              214  RETURN_VALUE     
            216_0  COME_FROM           202  '202'
            216_1  COME_FROM           182  '182'

 L.  52       216  LOAD_FAST                'nextchar'
              218  LOAD_STR                 'f'
              220  COMPARE_OP               ==
          222_224  POP_JUMP_IF_FALSE   260  'to 260'
              226  LOAD_FAST                'string'
              228  LOAD_FAST                'idx'
              230  LOAD_FAST                'idx'
              232  LOAD_CONST               5
              234  BINARY_ADD       
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  LOAD_STR                 'false'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L.  53       248  LOAD_CONST               False
              250  LOAD_FAST                'idx'
              252  LOAD_CONST               5
              254  BINARY_ADD       
              256  BUILD_TUPLE_2         2 
              258  RETURN_VALUE     
            260_0  COME_FROM           244  '244'
            260_1  COME_FROM           222  '222'

 L.  55       260  LOAD_DEREF               'match_number'
              262  LOAD_FAST                'string'
              264  LOAD_FAST                'idx'
              266  CALL_FUNCTION_2       2  ''
              268  STORE_FAST               'm'

 L.  56       270  LOAD_FAST                'm'
              272  LOAD_CONST               None
              274  <117>                 1  ''
          276_278  POP_JUMP_IF_FALSE   356  'to 356'

 L.  57       280  LOAD_FAST                'm'
              282  LOAD_METHOD              groups
              284  CALL_METHOD_0         0  ''
              286  UNPACK_SEQUENCE_3     3 
              288  STORE_FAST               'integer'
              290  STORE_FAST               'frac'
              292  STORE_FAST               'exp'

 L.  58       294  LOAD_FAST                'frac'
          296_298  POP_JUMP_IF_TRUE    306  'to 306'
              300  LOAD_FAST                'exp'
          302_304  POP_JUMP_IF_FALSE   336  'to 336'
            306_0  COME_FROM           296  '296'

 L.  59       306  LOAD_DEREF               'parse_float'
              308  LOAD_FAST                'integer'
              310  LOAD_FAST                'frac'
          312_314  JUMP_IF_TRUE_OR_POP   318  'to 318'
              316  LOAD_STR                 ''
            318_0  COME_FROM           312  '312'
              318  BINARY_ADD       
              320  LOAD_FAST                'exp'
          322_324  JUMP_IF_TRUE_OR_POP   328  'to 328'
              326  LOAD_STR                 ''
            328_0  COME_FROM           322  '322'
              328  BINARY_ADD       
              330  CALL_FUNCTION_1       1  ''
              332  STORE_FAST               'res'
              334  JUMP_FORWARD        344  'to 344'
            336_0  COME_FROM           302  '302'

 L.  61       336  LOAD_DEREF               'parse_int'
              338  LOAD_FAST                'integer'
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'res'
            344_0  COME_FROM           334  '334'

 L.  62       344  LOAD_FAST                'res'
              346  LOAD_FAST                'm'
              348  LOAD_METHOD              end
              350  CALL_METHOD_0         0  ''
              352  BUILD_TUPLE_2         2 
              354  RETURN_VALUE     
            356_0  COME_FROM           276  '276'

 L.  63       356  LOAD_FAST                'nextchar'
              358  LOAD_STR                 'N'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   404  'to 404'
              366  LOAD_FAST                'string'
              368  LOAD_FAST                'idx'
              370  LOAD_FAST                'idx'
              372  LOAD_CONST               3
              374  BINARY_ADD       
              376  BUILD_SLICE_2         2 
              378  BINARY_SUBSCR    
              380  LOAD_STR                 'NaN'
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   404  'to 404'

 L.  64       388  LOAD_DEREF               'parse_constant'
              390  LOAD_STR                 'NaN'
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_FAST                'idx'
              396  LOAD_CONST               3
              398  BINARY_ADD       
              400  BUILD_TUPLE_2         2 
              402  RETURN_VALUE     
            404_0  COME_FROM           384  '384'
            404_1  COME_FROM           362  '362'

 L.  65       404  LOAD_FAST                'nextchar'
              406  LOAD_STR                 'I'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   452  'to 452'
              414  LOAD_FAST                'string'
              416  LOAD_FAST                'idx'
              418  LOAD_FAST                'idx'
              420  LOAD_CONST               8
              422  BINARY_ADD       
              424  BUILD_SLICE_2         2 
              426  BINARY_SUBSCR    
              428  LOAD_STR                 'Infinity'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   452  'to 452'

 L.  66       436  LOAD_DEREF               'parse_constant'
              438  LOAD_STR                 'Infinity'
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_FAST                'idx'
              444  LOAD_CONST               8
              446  BINARY_ADD       
              448  BUILD_TUPLE_2         2 
              450  RETURN_VALUE     
            452_0  COME_FROM           432  '432'
            452_1  COME_FROM           410  '410'

 L.  67       452  LOAD_FAST                'nextchar'
              454  LOAD_STR                 '-'
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   500  'to 500'
              462  LOAD_FAST                'string'
              464  LOAD_FAST                'idx'
              466  LOAD_FAST                'idx'
              468  LOAD_CONST               9
              470  BINARY_ADD       
              472  BUILD_SLICE_2         2 
              474  BINARY_SUBSCR    
              476  LOAD_STR                 '-Infinity'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   500  'to 500'

 L.  68       484  LOAD_DEREF               'parse_constant'
              486  LOAD_STR                 '-Infinity'
              488  CALL_FUNCTION_1       1  ''
              490  LOAD_FAST                'idx'
              492  LOAD_CONST               9
              494  BINARY_ADD       
              496  BUILD_TUPLE_2         2 
              498  RETURN_VALUE     
            500_0  COME_FROM           480  '480'
            500_1  COME_FROM           458  '458'

 L.  70       500  LOAD_GLOBAL              JSONDecodeError
              502  LOAD_FAST                'errmsg'
              504  LOAD_FAST                'string'
              506  LOAD_FAST                'idx'
              508  CALL_FUNCTION_3       3  ''
              510  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 22

    def scan_once--- This code section failed: ---

 L.  73         0  LOAD_FAST                'idx'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  77         8  LOAD_GLOBAL              JSONDecodeError
               10  LOAD_STR                 'Expecting value'
               12  LOAD_FAST                'string'
               14  LOAD_FAST                'idx'
               16  CALL_FUNCTION_3       3  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             6  '6'

 L.  78        20  SETUP_FINALLY        42  'to 42'

 L.  79        22  LOAD_DEREF               '_scan_once'
               24  LOAD_FAST                'string'
               26  LOAD_FAST                'idx'
               28  CALL_FUNCTION_2       2  ''
               30  POP_BLOCK        

 L.  81        32  LOAD_DEREF               'memo'
               34  LOAD_METHOD              clear
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L.  79        40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    20  '20'

 L.  81        42  LOAD_DEREF               'memo'
               44  LOAD_METHOD              clear
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
               50  <48>             

Parse error at or near `LOAD_DEREF' instruction at offset 32

    return scan_once


make_scanner = c_make_scanner or py_make_scanner