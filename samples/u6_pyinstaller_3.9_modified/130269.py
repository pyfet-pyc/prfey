# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: C:\Users\win10\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_multiprocessing.py
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
               12  POP_JUMP_IF_FALSE    94  'to 94'

 L.  38        14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                argv
               18  LOAD_CONST               -2
               20  BINARY_SUBSCR    
               22  LOAD_STR                 '-c'
               24  COMPARE_OP               ==

 L.  37        26  POP_JUMP_IF_FALSE    94  'to 94'

 L.  39        28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                argv
               32  LOAD_CONST               -1
               34  BINARY_SUBSCR    
               36  LOAD_METHOD              startswith

 L.  40        38  LOAD_CONST               ('from multiprocessing.semaphore_tracker import main', 'from multiprocessing.resource_tracker import main', 'from multiprocessing.forkserver import main')

 L.  39        40  CALL_METHOD_1         1  ''

 L.  37        42  POP_JUMP_IF_FALSE    94  'to 94'

 L.  43        44  LOAD_GLOBAL              set
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                argv
               50  LOAD_CONST               1
               52  LOAD_CONST               -2
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_GLOBAL              set
               62  LOAD_GLOBAL              _args_from_interpreter_flags
               64  CALL_FUNCTION_0       0  ''
               66  CALL_FUNCTION_1       1  ''
               68  COMPARE_OP               ==

 L.  37        70  POP_JUMP_IF_FALSE    94  'to 94'

 L.  44        72  LOAD_GLOBAL              exec
               74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                argv
               78  LOAD_CONST               -1
               80  BINARY_SUBSCR    
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          

 L.  45        86  LOAD_GLOBAL              sys
               88  LOAD_METHOD              exit
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          
             94_0  COME_FROM            70  '70'
             94_1  COME_FROM            42  '42'
             94_2  COME_FROM            26  '26'
             94_3  COME_FROM            12  '12'

 L.  47        94  LOAD_GLOBAL              spawn
               96  LOAD_METHOD              is_forking
               98  LOAD_GLOBAL              sys
              100  LOAD_ATTR                argv
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   198  'to 198'

 L.  48       106  BUILD_MAP_0           0 
              108  STORE_FAST               'kwds'

 L.  49       110  LOAD_GLOBAL              sys
              112  LOAD_ATTR                argv
              114  LOAD_CONST               2
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  GET_ITER         
              124  FOR_ITER            174  'to 174'
              126  STORE_FAST               'arg'

 L.  50       128  LOAD_FAST                'arg'
              130  LOAD_METHOD              split
              132  LOAD_STR                 '='
              134  CALL_METHOD_1         1  ''
              136  UNPACK_SEQUENCE_2     2 
              138  STORE_FAST               'name'
              140  STORE_FAST               'value'

 L.  51       142  LOAD_FAST                'value'
              144  LOAD_STR                 'None'
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L.  52       150  LOAD_CONST               None
              152  LOAD_FAST                'kwds'
              154  LOAD_FAST                'name'
              156  STORE_SUBSCR     
              158  JUMP_BACK           124  'to 124'
            160_0  COME_FROM           148  '148'

 L.  54       160  LOAD_GLOBAL              int
              162  LOAD_FAST                'value'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_FAST                'kwds'
              168  LOAD_FAST                'name'
              170  STORE_SUBSCR     
              172  JUMP_BACK           124  'to 124'

 L.  55       174  LOAD_GLOBAL              spawn
              176  LOAD_ATTR                spawn_main
              178  BUILD_TUPLE_0         0 
              180  BUILD_MAP_0           0 
              182  LOAD_FAST                'kwds'
              184  <164>                 1  ''
              186  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              188  POP_TOP          

 L.  56       190  LOAD_GLOBAL              sys
              192  LOAD_METHOD              exit
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          
            198_0  COME_FROM           104  '104'

Parse error at or near `<164>' instruction at offset 184


multiprocessing.freeze_support = spawn.freeze_support = _freeze_support
if sys.platform.startswith('win'):
    import multiprocessing.popen_spawn_win32 as forking
else:
    import multiprocessing.popen_fork as forking
    import multiprocessing.popen_spawn_posix as spawning

class FrozenSupportMixIn:

    def __init__--- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              sys
                4  LOAD_STR                 'frozen'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  79        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              putenv
               14  LOAD_STR                 '_MEIPASS2'
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                _MEIPASS
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L.  80        24  SETUP_FINALLY        92  'to 92'

 L.  81        26  LOAD_GLOBAL              super
               28  CALL_FUNCTION_0       0  ''
               30  LOAD_ATTR                __init__
               32  LOAD_FAST                'args'
               34  BUILD_MAP_0           0 
               36  LOAD_FAST                'kw'
               38  <164>                 1  ''
               40  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               42  POP_TOP          
               44  POP_BLOCK        

 L.  83        46  LOAD_GLOBAL              hasattr
               48  LOAD_GLOBAL              sys
               50  LOAD_STR                 'frozen'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE   138  'to 138'

 L.  88        56  LOAD_GLOBAL              hasattr
               58  LOAD_GLOBAL              os
               60  LOAD_STR                 'unsetenv'
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L.  89        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              unsetenv
               70  LOAD_STR                 '_MEIPASS2'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  JUMP_ABSOLUTE       138  'to 138'
             78_0  COME_FROM            64  '64'

 L.  91        78  LOAD_GLOBAL              os
               80  LOAD_METHOD              putenv
               82  LOAD_STR                 '_MEIPASS2'
               84  LOAD_STR                 ''
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          
               90  JUMP_FORWARD        138  'to 138'
             92_0  COME_FROM_FINALLY    24  '24'

 L.  83        92  LOAD_GLOBAL              hasattr
               94  LOAD_GLOBAL              sys
               96  LOAD_STR                 'frozen'
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_FALSE   136  'to 136'

 L.  88       102  LOAD_GLOBAL              hasattr
              104  LOAD_GLOBAL              os
              106  LOAD_STR                 'unsetenv'
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L.  89       112  LOAD_GLOBAL              os
              114  LOAD_METHOD              unsetenv
              116  LOAD_STR                 '_MEIPASS2'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  JUMP_FORWARD        136  'to 136'
            124_0  COME_FROM           110  '110'

 L.  91       124  LOAD_GLOBAL              os
              126  LOAD_METHOD              putenv
              128  LOAD_STR                 '_MEIPASS2'
              130  LOAD_STR                 ''
              132  CALL_METHOD_2         2  ''
              134  POP_TOP          
            136_0  COME_FROM           122  '122'
            136_1  COME_FROM           100  '100'
              136  <48>             
            138_0  COME_FROM            90  '90'
            138_1  COME_FROM            54  '54'

Parse error at or near `<164>' instruction at offset 38


class _Popen(FrozenSupportMixIn, forking.Popen):
    pass


forking.Popen = _Popen
if not sys.platform.startswith('win'):

    class _Spawning_Popen(FrozenSupportMixIn, spawning.Popen):
        pass


    spawning.Popen = _Spawning_Popen