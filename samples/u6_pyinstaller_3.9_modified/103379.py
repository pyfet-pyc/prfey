# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: C:\Users\lolke\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_multiprocessing.py
import sys, os, re, multiprocessing
import multiprocessing.spawn as spawn
from subprocess import _args_from_interpreter_flags
multiprocessing.process.ORIGINAL_DIR = None

def _freeze_support--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              len
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                argv
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               2
               10  COMPARE_OP               >=
               12  POP_JUMP_IF_FALSE   110  'to 110'

 L.  38        14  LOAD_GLOBAL              set
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                argv
               20  LOAD_CONST               1
               22  LOAD_CONST               -2
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_GLOBAL              set
               32  LOAD_GLOBAL              _args_from_interpreter_flags
               34  CALL_FUNCTION_0       0  ''
               36  CALL_FUNCTION_1       1  ''
               38  COMPARE_OP               ==

 L.  37        40  POP_JUMP_IF_FALSE   110  'to 110'

 L.  39        42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                argv
               46  LOAD_CONST               -2
               48  BINARY_SUBSCR    
               50  LOAD_STR                 '-c'
               52  COMPARE_OP               ==

 L.  37        54  POP_JUMP_IF_FALSE   110  'to 110'

 L.  40        56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                argv
               60  LOAD_CONST               -1
               62  BINARY_SUBSCR    
               64  LOAD_METHOD              startswith
               66  LOAD_STR                 'from multiprocessing.semaphore_tracker import main'
               68  CALL_METHOD_1         1  ''

 L.  37        70  POP_JUMP_IF_TRUE     88  'to 88'

 L.  41        72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                argv
               76  LOAD_CONST               -1
               78  BINARY_SUBSCR    
               80  LOAD_METHOD              startswith
               82  LOAD_STR                 'from multiprocessing.forkserver import main'
               84  CALL_METHOD_1         1  ''

 L.  37        86  POP_JUMP_IF_FALSE   110  'to 110'
             88_0  COME_FROM            70  '70'

 L.  42        88  LOAD_GLOBAL              exec
               90  LOAD_GLOBAL              sys
               92  LOAD_ATTR                argv
               94  LOAD_CONST               -1
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          

 L.  43       102  LOAD_GLOBAL              sys
              104  LOAD_METHOD              exit
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          
            110_0  COME_FROM            86  '86'
            110_1  COME_FROM            54  '54'
            110_2  COME_FROM            40  '40'
            110_3  COME_FROM            12  '12'

 L.  45       110  LOAD_GLOBAL              spawn
              112  LOAD_METHOD              is_forking
              114  LOAD_GLOBAL              sys
              116  LOAD_ATTR                argv
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_FALSE   214  'to 214'

 L.  46       122  BUILD_MAP_0           0 
              124  STORE_FAST               'kwds'

 L.  47       126  LOAD_GLOBAL              sys
              128  LOAD_ATTR                argv
              130  LOAD_CONST               2
              132  LOAD_CONST               None
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  GET_ITER         
              140  FOR_ITER            190  'to 190'
              142  STORE_FAST               'arg'

 L.  48       144  LOAD_FAST                'arg'
              146  LOAD_METHOD              split
              148  LOAD_STR                 '='
              150  CALL_METHOD_1         1  ''
              152  UNPACK_SEQUENCE_2     2 
              154  STORE_FAST               'name'
              156  STORE_FAST               'value'

 L.  49       158  LOAD_FAST                'value'
              160  LOAD_STR                 'None'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   176  'to 176'

 L.  50       166  LOAD_CONST               None
              168  LOAD_FAST                'kwds'
              170  LOAD_FAST                'name'
              172  STORE_SUBSCR     
              174  JUMP_BACK           140  'to 140'
            176_0  COME_FROM           164  '164'

 L.  52       176  LOAD_GLOBAL              int
              178  LOAD_FAST                'value'
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_FAST                'kwds'
              184  LOAD_FAST                'name'
              186  STORE_SUBSCR     
              188  JUMP_BACK           140  'to 140'

 L.  53       190  LOAD_GLOBAL              spawn
              192  LOAD_ATTR                spawn_main
              194  BUILD_TUPLE_0         0 
              196  BUILD_MAP_0           0 
              198  LOAD_FAST                'kwds'
              200  <164>                 1  ''
              202  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              204  POP_TOP          

 L.  54       206  LOAD_GLOBAL              sys
              208  LOAD_METHOD              exit
              210  CALL_METHOD_0         0  ''
              212  POP_TOP          
            214_0  COME_FROM           120  '120'

Parse error at or near `<164>' instruction at offset 200


multiprocessing.freeze_support = spawn.freeze_support = _freeze_support
if sys.platform.startswith('win'):
    import multiprocessing.popen_spawn_win32 as forking
else:
    import multiprocessing.popen_fork as forking

class _Popen(forking.Popen):

    def __init__--- This code section failed: ---

 L.  71         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              sys
                4  LOAD_STR                 'frozen'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  74        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              putenv
               14  LOAD_STR                 '_MEIPASS2'
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                _MEIPASS
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L.  75        24  SETUP_FINALLY        96  'to 96'

 L.  76        26  LOAD_GLOBAL              super
               28  LOAD_GLOBAL              _Popen
               30  LOAD_FAST                'self'
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_ATTR                __init__
               36  LOAD_FAST                'args'
               38  BUILD_MAP_0           0 
               40  LOAD_FAST                'kw'
               42  <164>                 1  ''
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  POP_TOP          
               48  POP_BLOCK        

 L.  78        50  LOAD_GLOBAL              hasattr
               52  LOAD_GLOBAL              sys
               54  LOAD_STR                 'frozen'
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE   142  'to 142'

 L.  83        60  LOAD_GLOBAL              hasattr
               62  LOAD_GLOBAL              os
               64  LOAD_STR                 'unsetenv'
               66  CALL_FUNCTION_2       2  ''
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L.  84        70  LOAD_GLOBAL              os
               72  LOAD_METHOD              unsetenv
               74  LOAD_STR                 '_MEIPASS2'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_ABSOLUTE       142  'to 142'
             82_0  COME_FROM            68  '68'

 L.  86        82  LOAD_GLOBAL              os
               84  LOAD_METHOD              putenv
               86  LOAD_STR                 '_MEIPASS2'
               88  LOAD_STR                 ''
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          
               94  JUMP_FORWARD        142  'to 142'
             96_0  COME_FROM_FINALLY    24  '24'

 L.  78        96  LOAD_GLOBAL              hasattr
               98  LOAD_GLOBAL              sys
              100  LOAD_STR                 'frozen'
              102  CALL_FUNCTION_2       2  ''
              104  POP_JUMP_IF_FALSE   140  'to 140'

 L.  83       106  LOAD_GLOBAL              hasattr
              108  LOAD_GLOBAL              os
              110  LOAD_STR                 'unsetenv'
              112  CALL_FUNCTION_2       2  ''
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.  84       116  LOAD_GLOBAL              os
              118  LOAD_METHOD              unsetenv
              120  LOAD_STR                 '_MEIPASS2'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  JUMP_FORWARD        140  'to 140'
            128_0  COME_FROM           114  '114'

 L.  86       128  LOAD_GLOBAL              os
              130  LOAD_METHOD              putenv
              132  LOAD_STR                 '_MEIPASS2'
              134  LOAD_STR                 ''
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          
            140_0  COME_FROM           126  '126'
            140_1  COME_FROM           104  '104'
              140  <48>             
            142_0  COME_FROM            94  '94'
            142_1  COME_FROM            58  '58'

Parse error at or near `<164>' instruction at offset 42


forking.Popen = _Popen