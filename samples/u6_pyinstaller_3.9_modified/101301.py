# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImtImagePlugin.py
import re
from . import Image, ImageFile
field = re.compile(b'([a-z]*) ([^ \\r\\n]*)')

class ImtImageFile(ImageFile.ImageFile):
    format = 'IMT'
    format_description = 'IM Tools'

    def _open--- This code section failed: ---

 L.  42         0  LOAD_CONST               b'\n'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               100
               10  CALL_METHOD_1         1  ''
               12  <118>                 1  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  43        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not an IM file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L.  44        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              seek
               30  LOAD_CONST               0
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L.  46        36  LOAD_CONST               0
               38  DUP_TOP          
               40  STORE_FAST               'xsize'
               42  STORE_FAST               'ysize'
             44_0  COME_FROM           280  '280'
             44_1  COME_FROM           272  '272'

 L.  50        44  LOAD_FAST                'self'
               46  LOAD_ATTR                fp
               48  LOAD_METHOD              read
               50  LOAD_CONST               1
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               's'

 L.  51        56  LOAD_FAST                's'
               58  POP_JUMP_IF_TRUE     64  'to 64'

 L.  52     60_62  BREAK_LOOP          290  'to 290'
             64_0  COME_FROM            58  '58'

 L.  54        64  LOAD_FAST                's'
               66  LOAD_CONST               b'\x0c'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   114  'to 114'

 L.  58        72  LOAD_STR                 'raw'
               74  LOAD_CONST               (0, 0)
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                size
               80  BINARY_ADD       
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                fp
               86  LOAD_METHOD              tell
               88  CALL_METHOD_0         0  ''
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                mode
               94  LOAD_CONST               0
               96  LOAD_CONST               1
               98  BUILD_TUPLE_3         3 
              100  BUILD_TUPLE_4         4 

 L.  57       102  BUILD_LIST_1          1 
              104  LOAD_FAST                'self'
              106  STORE_ATTR               tile

 L.  61   108_110  BREAK_LOOP          290  'to 290'
              112  JUMP_BACK            44  'to 44'
            114_0  COME_FROM            70  '70'

 L.  67       114  LOAD_FAST                's'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                fp
              120  LOAD_METHOD              readline
              122  CALL_METHOD_0         0  ''
              124  BINARY_ADD       
              126  STORE_FAST               's'

 L.  68       128  LOAD_GLOBAL              len
              130  LOAD_FAST                's'
              132  CALL_FUNCTION_1       1  ''
              134  LOAD_CONST               1
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_TRUE    152  'to 152'
              140  LOAD_GLOBAL              len
              142  LOAD_FAST                's'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_CONST               100
              148  COMPARE_OP               >
              150  POP_JUMP_IF_FALSE   156  'to 156'
            152_0  COME_FROM           138  '138'

 L.  69   152_154  BREAK_LOOP          290  'to 290'
            156_0  COME_FROM           150  '150'

 L.  70       156  LOAD_FAST                's'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  LOAD_GLOBAL              ord
              164  LOAD_CONST               b'*'
              166  CALL_FUNCTION_1       1  ''
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   174  'to 174'

 L.  71       172  JUMP_BACK            44  'to 44'
            174_0  COME_FROM           170  '170'

 L.  73       174  LOAD_GLOBAL              field
              176  LOAD_METHOD              match
              178  LOAD_FAST                's'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'm'

 L.  74       184  LOAD_FAST                'm'
              186  POP_JUMP_IF_TRUE    192  'to 192'

 L.  75   188_190  BREAK_LOOP          290  'to 290'
            192_0  COME_FROM           186  '186'

 L.  76       192  LOAD_FAST                'm'
              194  LOAD_METHOD              group
              196  LOAD_CONST               1
              198  LOAD_CONST               2
              200  CALL_METHOD_2         2  ''
              202  UNPACK_SEQUENCE_2     2 
              204  STORE_FAST               'k'
              206  STORE_FAST               'v'

 L.  77       208  LOAD_FAST                'k'
              210  LOAD_STR                 'width'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   236  'to 236'

 L.  78       216  LOAD_GLOBAL              int
              218  LOAD_FAST                'v'
              220  CALL_FUNCTION_1       1  ''
              222  STORE_FAST               'xsize'

 L.  79       224  LOAD_FAST                'xsize'
              226  LOAD_FAST                'ysize'
              228  BUILD_TUPLE_2         2 
              230  LOAD_FAST                'self'
              232  STORE_ATTR               _size
              234  JUMP_BACK            44  'to 44'
            236_0  COME_FROM           214  '214'

 L.  80       236  LOAD_FAST                'k'
              238  LOAD_STR                 'height'
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   266  'to 266'

 L.  81       246  LOAD_GLOBAL              int
              248  LOAD_FAST                'v'
              250  CALL_FUNCTION_1       1  ''
              252  STORE_FAST               'ysize'

 L.  82       254  LOAD_FAST                'xsize'
              256  LOAD_FAST                'ysize'
              258  BUILD_TUPLE_2         2 
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _size
              264  JUMP_BACK            44  'to 44'
            266_0  COME_FROM           242  '242'

 L.  83       266  LOAD_FAST                'k'
              268  LOAD_STR                 'pixel'
              270  COMPARE_OP               ==
              272  POP_JUMP_IF_FALSE    44  'to 44'
              274  LOAD_FAST                'v'
              276  LOAD_STR                 'n8'
              278  COMPARE_OP               ==
              280  POP_JUMP_IF_FALSE    44  'to 44'

 L.  84       282  LOAD_STR                 'L'
              284  LOAD_FAST                'self'
              286  STORE_ATTR               mode
              288  JUMP_BACK            44  'to 44'

Parse error at or near `None' instruction at offset -1


Image.register_open(ImtImageFile.format, ImtImageFile)