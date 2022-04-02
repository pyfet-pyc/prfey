# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: nturl2path.py
"""Convert a NT pathname to a file URL and vice versa.

This module only exists to provide OS-specific code
for urllib.requests, thus do not use directly.
"""

def url2pathname--- This code section failed: ---

 L.  17         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              string
                6  STORE_FAST               'string'
                8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME_ATTR         urllib.parse
               14  STORE_FAST               'urllib'

 L.  19        16  LOAD_FAST                'url'
               18  LOAD_METHOD              replace
               20  LOAD_STR                 ':'
               22  LOAD_STR                 '|'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'url'

 L.  20        28  LOAD_STR                 '|'
               30  LOAD_FAST                'url'
               32  <118>                 1  ''
               34  POP_JUMP_IF_FALSE    92  'to 92'

 L.  22        36  LOAD_FAST                'url'
               38  LOAD_CONST               None
               40  LOAD_CONST               4
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_STR                 '////'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    64  'to 64'

 L.  26        52  LOAD_FAST                'url'
               54  LOAD_CONST               2
               56  LOAD_CONST               None
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  STORE_FAST               'url'
             64_0  COME_FROM            50  '50'

 L.  27        64  LOAD_FAST                'url'
               66  LOAD_METHOD              split
               68  LOAD_STR                 '/'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'components'

 L.  29        74  LOAD_FAST                'urllib'
               76  LOAD_ATTR                parse
               78  LOAD_METHOD              unquote
               80  LOAD_STR                 '\\'
               82  LOAD_METHOD              join
               84  LOAD_FAST                'components'
               86  CALL_METHOD_1         1  ''
               88  CALL_METHOD_1         1  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            34  '34'

 L.  30        92  LOAD_FAST                'url'
               94  LOAD_METHOD              split
               96  LOAD_STR                 '|'
               98  CALL_METHOD_1         1  ''
              100  STORE_FAST               'comp'

 L.  31       102  LOAD_GLOBAL              len
              104  LOAD_FAST                'comp'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               2
              110  COMPARE_OP               !=
              112  POP_JUMP_IF_TRUE    132  'to 132'
              114  LOAD_FAST                'comp'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  LOAD_CONST               -1
              122  BINARY_SUBSCR    
              124  LOAD_FAST                'string'
              126  LOAD_ATTR                ascii_letters
              128  <118>                 1  ''
              130  POP_JUMP_IF_FALSE   148  'to 148'
            132_0  COME_FROM           112  '112'

 L.  32       132  LOAD_STR                 'Bad URL: '
              134  LOAD_FAST                'url'
              136  BINARY_ADD       
              138  STORE_FAST               'error'

 L.  33       140  LOAD_GLOBAL              OSError
              142  LOAD_FAST                'error'
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           130  '130'

 L.  34       148  LOAD_FAST                'comp'
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              upper
              160  CALL_METHOD_0         0  ''
              162  STORE_FAST               'drive'

 L.  35       164  LOAD_FAST                'comp'
              166  LOAD_CONST               1
              168  BINARY_SUBSCR    
              170  LOAD_METHOD              split
              172  LOAD_STR                 '/'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'components'

 L.  36       178  LOAD_FAST                'drive'
              180  LOAD_STR                 ':'
              182  BINARY_ADD       
              184  STORE_FAST               'path'

 L.  37       186  LOAD_FAST                'components'
              188  GET_ITER         
            190_0  COME_FROM           196  '196'
              190  FOR_ITER            220  'to 220'
              192  STORE_FAST               'comp'

 L.  38       194  LOAD_FAST                'comp'
              196  POP_JUMP_IF_FALSE   190  'to 190'

 L.  39       198  LOAD_FAST                'path'
              200  LOAD_STR                 '\\'
              202  BINARY_ADD       
              204  LOAD_FAST                'urllib'
              206  LOAD_ATTR                parse
              208  LOAD_METHOD              unquote
              210  LOAD_FAST                'comp'
              212  CALL_METHOD_1         1  ''
              214  BINARY_ADD       
              216  STORE_FAST               'path'
              218  JUMP_BACK           190  'to 190'

 L.  41       220  LOAD_FAST                'path'
              222  LOAD_METHOD              endswith
              224  LOAD_STR                 ':'
              226  CALL_METHOD_1         1  ''
              228  POP_JUMP_IF_FALSE   248  'to 248'
              230  LOAD_FAST                'url'
              232  LOAD_METHOD              endswith
              234  LOAD_STR                 '/'
              236  CALL_METHOD_1         1  ''
              238  POP_JUMP_IF_FALSE   248  'to 248'

 L.  42       240  LOAD_FAST                'path'
              242  LOAD_STR                 '\\'
              244  INPLACE_ADD      
              246  STORE_FAST               'path'
            248_0  COME_FROM           238  '238'
            248_1  COME_FROM           228  '228'

 L.  43       248  LOAD_FAST                'path'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 32


def pathname2url--- This code section failed: ---

 L.  52         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         urllib.parse
                6  STORE_FAST               'urllib'

 L.  55         8  LOAD_FAST                'p'
               10  LOAD_CONST               None
               12  LOAD_CONST               4
               14  BUILD_SLICE_2         2 
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '\\\\?\\'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE   102  'to 102'

 L.  56        24  LOAD_FAST                'p'
               26  LOAD_CONST               4
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  STORE_FAST               'p'

 L.  57        36  LOAD_FAST                'p'
               38  LOAD_CONST               None
               40  LOAD_CONST               4
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_METHOD              upper
               48  CALL_METHOD_0         0  ''
               50  LOAD_STR                 'UNC\\'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    74  'to 74'

 L.  58        56  LOAD_STR                 '\\'
               58  LOAD_FAST                'p'
               60  LOAD_CONST               4
               62  LOAD_CONST               None
               64  BUILD_SLICE_2         2 
               66  BINARY_SUBSCR    
               68  BINARY_ADD       
               70  STORE_FAST               'p'
               72  JUMP_FORWARD        102  'to 102'
             74_0  COME_FROM            54  '54'

 L.  59        74  LOAD_FAST                'p'
               76  LOAD_CONST               1
               78  LOAD_CONST               2
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  LOAD_STR                 ':'
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L.  60        90  LOAD_GLOBAL              OSError
               92  LOAD_STR                 'Bad path: '
               94  LOAD_FAST                'p'
               96  BINARY_ADD       
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            88  '88'
            102_1  COME_FROM            72  '72'
            102_2  COME_FROM            22  '22'

 L.  61       102  LOAD_STR                 ':'
              104  LOAD_FAST                'p'
              106  <118>                 1  ''
              108  POP_JUMP_IF_FALSE   162  'to 162'

 L.  63       110  LOAD_FAST                'p'
              112  LOAD_CONST               None
              114  LOAD_CONST               2
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  LOAD_STR                 '\\\\'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L.  67       126  LOAD_STR                 '\\\\'
              128  LOAD_FAST                'p'
              130  BINARY_ADD       
              132  STORE_FAST               'p'
            134_0  COME_FROM           124  '124'

 L.  68       134  LOAD_FAST                'p'
              136  LOAD_METHOD              split
              138  LOAD_STR                 '\\'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'components'

 L.  69       144  LOAD_FAST                'urllib'
              146  LOAD_ATTR                parse
              148  LOAD_METHOD              quote
              150  LOAD_STR                 '/'
              152  LOAD_METHOD              join
              154  LOAD_FAST                'components'
              156  CALL_METHOD_1         1  ''
              158  CALL_METHOD_1         1  ''
              160  RETURN_VALUE     
            162_0  COME_FROM           108  '108'

 L.  70       162  LOAD_FAST                'p'
              164  LOAD_ATTR                split
              166  LOAD_STR                 ':'
              168  LOAD_CONST               2
              170  LOAD_CONST               ('maxsplit',)
              172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              174  STORE_FAST               'comp'

 L.  71       176  LOAD_GLOBAL              len
              178  LOAD_FAST                'comp'
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_CONST               2
              184  COMPARE_OP               !=
              186  POP_JUMP_IF_TRUE    204  'to 204'
              188  LOAD_GLOBAL              len
              190  LOAD_FAST                'comp'
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_CONST               1
              200  COMPARE_OP               >
              202  POP_JUMP_IF_FALSE   220  'to 220'
            204_0  COME_FROM           186  '186'

 L.  72       204  LOAD_STR                 'Bad path: '
              206  LOAD_FAST                'p'
              208  BINARY_ADD       
              210  STORE_FAST               'error'

 L.  73       212  LOAD_GLOBAL              OSError
              214  LOAD_FAST                'error'
              216  CALL_FUNCTION_1       1  ''
              218  RAISE_VARARGS_1       1  'exception instance'
            220_0  COME_FROM           202  '202'

 L.  75       220  LOAD_FAST                'urllib'
              222  LOAD_ATTR                parse
              224  LOAD_METHOD              quote
              226  LOAD_FAST                'comp'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  LOAD_METHOD              upper
              234  CALL_METHOD_0         0  ''
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'drive'

 L.  76       240  LOAD_FAST                'comp'
              242  LOAD_CONST               1
              244  BINARY_SUBSCR    
              246  LOAD_METHOD              split
              248  LOAD_STR                 '\\'
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'components'

 L.  77       254  LOAD_STR                 '///'
              256  LOAD_FAST                'drive'
              258  BINARY_ADD       
              260  LOAD_STR                 ':'
              262  BINARY_ADD       
              264  STORE_FAST               'path'

 L.  78       266  LOAD_FAST                'components'
              268  GET_ITER         
            270_0  COME_FROM           276  '276'
              270  FOR_ITER            304  'to 304'
              272  STORE_FAST               'comp'

 L.  79       274  LOAD_FAST                'comp'
          276_278  POP_JUMP_IF_FALSE   270  'to 270'

 L.  80       280  LOAD_FAST                'path'
              282  LOAD_STR                 '/'
              284  BINARY_ADD       
              286  LOAD_FAST                'urllib'
              288  LOAD_ATTR                parse
              290  LOAD_METHOD              quote
              292  LOAD_FAST                'comp'
              294  CALL_METHOD_1         1  ''
              296  BINARY_ADD       
              298  STORE_FAST               'path'
          300_302  JUMP_BACK           270  'to 270'

 L.  81       304  LOAD_FAST                'path'
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 106