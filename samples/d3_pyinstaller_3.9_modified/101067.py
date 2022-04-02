# decompyle3 version 3.7.5
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
            190_0  COME_FROM           218  '218'
            190_1  COME_FROM           196  '196'
              190  FOR_ITER            220  'to 220'
              192  STORE_FAST               'comp'

 L.  38       194  LOAD_FAST                'comp'
              196  POP_JUMP_IF_FALSE_BACK   190  'to 190'

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
            220_0  COME_FROM           190  '190'

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

 L.  53         8  LOAD_STR                 ':'
               10  LOAD_FAST                'p'
               12  <118>                 1  ''
               14  POP_JUMP_IF_FALSE    68  'to 68'

 L.  55        16  LOAD_FAST                'p'
               18  LOAD_CONST               None
               20  LOAD_CONST               2
               22  BUILD_SLICE_2         2 
               24  BINARY_SUBSCR    
               26  LOAD_STR                 '\\\\'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.  59        32  LOAD_STR                 '\\\\'
               34  LOAD_FAST                'p'
               36  BINARY_ADD       
               38  STORE_FAST               'p'
             40_0  COME_FROM            30  '30'

 L.  60        40  LOAD_FAST                'p'
               42  LOAD_METHOD              split
               44  LOAD_STR                 '\\'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'components'

 L.  61        50  LOAD_FAST                'urllib'
               52  LOAD_ATTR                parse
               54  LOAD_METHOD              quote
               56  LOAD_STR                 '/'
               58  LOAD_METHOD              join
               60  LOAD_FAST                'components'
               62  CALL_METHOD_1         1  ''
               64  CALL_METHOD_1         1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            14  '14'

 L.  62        68  LOAD_FAST                'p'
               70  LOAD_METHOD              split
               72  LOAD_STR                 ':'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'comp'

 L.  63        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'comp'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_CONST               2
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_TRUE    106  'to 106'
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'comp'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               1
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   122  'to 122'
            106_0  COME_FROM            88  '88'

 L.  64       106  LOAD_STR                 'Bad path: '
              108  LOAD_FAST                'p'
              110  BINARY_ADD       
              112  STORE_FAST               'error'

 L.  65       114  LOAD_GLOBAL              OSError
              116  LOAD_FAST                'error'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           104  '104'

 L.  67       122  LOAD_FAST                'urllib'
              124  LOAD_ATTR                parse
              126  LOAD_METHOD              quote
              128  LOAD_FAST                'comp'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  LOAD_METHOD              upper
              136  CALL_METHOD_0         0  ''
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'drive'

 L.  68       142  LOAD_FAST                'comp'
              144  LOAD_CONST               1
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              split
              150  LOAD_STR                 '\\'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'components'

 L.  69       156  LOAD_STR                 '///'
              158  LOAD_FAST                'drive'
              160  BINARY_ADD       
              162  LOAD_STR                 ':'
              164  BINARY_ADD       
              166  STORE_FAST               'path'

 L.  70       168  LOAD_FAST                'components'
              170  GET_ITER         
            172_0  COME_FROM           200  '200'
            172_1  COME_FROM           178  '178'
              172  FOR_ITER            202  'to 202'
              174  STORE_FAST               'comp'

 L.  71       176  LOAD_FAST                'comp'
              178  POP_JUMP_IF_FALSE_BACK   172  'to 172'

 L.  72       180  LOAD_FAST                'path'
              182  LOAD_STR                 '/'
              184  BINARY_ADD       
              186  LOAD_FAST                'urllib'
              188  LOAD_ATTR                parse
              190  LOAD_METHOD              quote
              192  LOAD_FAST                'comp'
              194  CALL_METHOD_1         1  ''
              196  BINARY_ADD       
              198  STORE_FAST               'path'
              200  JUMP_BACK           172  'to 172'
            202_0  COME_FROM           172  '172'

 L.  73       202  LOAD_FAST                'path'
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 12