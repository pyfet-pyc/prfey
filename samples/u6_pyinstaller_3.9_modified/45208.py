# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\packages\backports\makefile.py
"""
backports.makefile
~~~~~~~~~~~~~~~~~~

Backports the Python 3 ``socket.makefile`` method for use with anything that
wants to create a "fake" socket object.
"""
import io
from socket import SocketIO

def backport_makefile--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              set
                2  LOAD_FAST                'mode'
                4  CALL_FUNCTION_1       1  ''
                6  BUILD_SET_0           0 
                8  LOAD_CONST               frozenset({'r', 'w', 'b'})
               10  POP_FINALLY           1  ''
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_TRUE     30  'to 30'

 L.  20        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'invalid mode %r (only r, w, b allowed)'
               20  LOAD_FAST                'mode'
               22  BUILD_TUPLE_1         1 
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            14  '14'

 L.  21        30  LOAD_STR                 'w'
               32  LOAD_FAST                'mode'
               34  <118>                 0  ''
               36  STORE_FAST               'writing'

 L.  22        38  LOAD_STR                 'r'
               40  LOAD_FAST                'mode'
               42  <118>                 0  ''
               44  JUMP_IF_TRUE_OR_POP    50  'to 50'
               46  LOAD_FAST                'writing'
               48  UNARY_NOT        
             50_0  COME_FROM            44  '44'
               50  STORE_FAST               'reading'

 L.  23        52  LOAD_FAST                'reading'
               54  POP_JUMP_IF_TRUE     64  'to 64'
               56  LOAD_FAST                'writing'
               58  POP_JUMP_IF_TRUE     64  'to 64'
               60  <74>             
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            54  '54'

 L.  24        64  LOAD_STR                 'b'
               66  LOAD_FAST                'mode'
               68  <118>                 0  ''
               70  STORE_FAST               'binary'

 L.  25        72  LOAD_STR                 ''
               74  STORE_FAST               'rawmode'

 L.  26        76  LOAD_FAST                'reading'
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.  27        80  LOAD_FAST                'rawmode'
               82  LOAD_STR                 'r'
               84  INPLACE_ADD      
               86  STORE_FAST               'rawmode'
             88_0  COME_FROM            78  '78'

 L.  28        88  LOAD_FAST                'writing'
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.  29        92  LOAD_FAST                'rawmode'
               94  LOAD_STR                 'w'
               96  INPLACE_ADD      
               98  STORE_FAST               'rawmode'
            100_0  COME_FROM            90  '90'

 L.  30       100  LOAD_GLOBAL              SocketIO
              102  LOAD_FAST                'self'
              104  LOAD_FAST                'rawmode'
              106  CALL_FUNCTION_2       2  ''
              108  STORE_FAST               'raw'

 L.  31       110  LOAD_FAST                'self'
              112  DUP_TOP          
              114  LOAD_ATTR                _makefile_refs
              116  LOAD_CONST               1
              118  INPLACE_ADD      
              120  ROT_TWO          
              122  STORE_ATTR               _makefile_refs

 L.  32       124  LOAD_FAST                'buffering'
              126  LOAD_CONST               None
              128  <117>                 0  ''
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L.  33       132  LOAD_CONST               -1
              134  STORE_FAST               'buffering'
            136_0  COME_FROM           130  '130'

 L.  34       136  LOAD_FAST                'buffering'
              138  LOAD_CONST               0
              140  COMPARE_OP               <
              142  POP_JUMP_IF_FALSE   150  'to 150'

 L.  35       144  LOAD_GLOBAL              io
              146  LOAD_ATTR                DEFAULT_BUFFER_SIZE
              148  STORE_FAST               'buffering'
            150_0  COME_FROM           142  '142'

 L.  36       150  LOAD_FAST                'buffering'
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   174  'to 174'

 L.  37       158  LOAD_FAST                'binary'
              160  POP_JUMP_IF_TRUE    170  'to 170'

 L.  38       162  LOAD_GLOBAL              ValueError
              164  LOAD_STR                 'unbuffered streams must be binary'
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           160  '160'

 L.  39       170  LOAD_FAST                'raw'
              172  RETURN_VALUE     
            174_0  COME_FROM           156  '156'

 L.  40       174  LOAD_FAST                'reading'
              176  POP_JUMP_IF_FALSE   198  'to 198'
              178  LOAD_FAST                'writing'
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L.  41       182  LOAD_GLOBAL              io
              184  LOAD_METHOD              BufferedRWPair
              186  LOAD_FAST                'raw'
              188  LOAD_FAST                'raw'
              190  LOAD_FAST                'buffering'
              192  CALL_METHOD_3         3  ''
              194  STORE_FAST               'buffer'
              196  JUMP_FORWARD        236  'to 236'
            198_0  COME_FROM           180  '180'
            198_1  COME_FROM           176  '176'

 L.  42       198  LOAD_FAST                'reading'
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.  43       202  LOAD_GLOBAL              io
              204  LOAD_METHOD              BufferedReader
              206  LOAD_FAST                'raw'
              208  LOAD_FAST                'buffering'
              210  CALL_METHOD_2         2  ''
              212  STORE_FAST               'buffer'
              214  JUMP_FORWARD        236  'to 236'
            216_0  COME_FROM           200  '200'

 L.  45       216  LOAD_FAST                'writing'
              218  POP_JUMP_IF_TRUE    224  'to 224'
              220  <74>             
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           218  '218'

 L.  46       224  LOAD_GLOBAL              io
              226  LOAD_METHOD              BufferedWriter
              228  LOAD_FAST                'raw'
              230  LOAD_FAST                'buffering'
              232  CALL_METHOD_2         2  ''
              234  STORE_FAST               'buffer'
            236_0  COME_FROM           214  '214'
            236_1  COME_FROM           196  '196'

 L.  47       236  LOAD_FAST                'binary'
              238  POP_JUMP_IF_FALSE   244  'to 244'

 L.  48       240  LOAD_FAST                'buffer'
              242  RETURN_VALUE     
            244_0  COME_FROM           238  '238'

 L.  49       244  LOAD_GLOBAL              io
              246  LOAD_METHOD              TextIOWrapper
              248  LOAD_FAST                'buffer'
              250  LOAD_FAST                'encoding'
              252  LOAD_FAST                'errors'
              254  LOAD_FAST                'newline'
              256  CALL_METHOD_4         4  ''
              258  STORE_FAST               'text'

 L.  50       260  LOAD_FAST                'mode'
              262  LOAD_FAST                'text'
              264  STORE_ATTR               mode

 L.  51       266  LOAD_FAST                'text'
              268  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1