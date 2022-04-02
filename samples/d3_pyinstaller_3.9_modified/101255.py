# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\popen_spawn_win32.py
import os, msvcrt, signal, sys, _winapi
from .context import reduction, get_spawning_popen, set_spawning_popen
from . import spawn
from . import util
__all__ = [
 'Popen']
TERMINATE = 65536
WINEXE = sys.platform == 'win32' and getattr(sys, 'frozen', False)
WINSERVICE = sys.executable.lower().endswith('pythonservice.exe')

def _path_eq(p1, p2):
    return p1 == p2 or os.path.normcase(p1) == os.path.normcase(p2)


WINENV = not _path_eq(sys.executable, sys._base_executable)

def _close_handles(*handles):
    for handle in handles:
        _winapi.CloseHandle(handle)


class Popen(object):
    __doc__ = '\n    Start a subprocess to run the code of a process object\n    '
    method = 'spawn'

    def __init__--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              spawn
                2  LOAD_METHOD              get_preparation_data
                4  LOAD_FAST                'process_obj'
                6  LOAD_ATTR                _name
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'prep_data'

 L.  53        12  LOAD_GLOBAL              _winapi
               14  LOAD_METHOD              CreatePipe
               16  LOAD_CONST               None
               18  LOAD_CONST               0
               20  CALL_METHOD_2         2  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'rhandle'
               26  STORE_FAST               'whandle'

 L.  54        28  LOAD_GLOBAL              msvcrt
               30  LOAD_METHOD              open_osfhandle
               32  LOAD_FAST                'whandle'
               34  LOAD_CONST               0
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'wfd'

 L.  55        40  LOAD_GLOBAL              spawn
               42  LOAD_ATTR                get_command_line
               44  LOAD_GLOBAL              os
               46  LOAD_METHOD              getpid
               48  CALL_METHOD_0         0  ''

 L.  56        50  LOAD_FAST                'rhandle'

 L.  55        52  LOAD_CONST               ('parent_pid', 'pipe_handle')
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'cmd'

 L.  57        58  LOAD_STR                 ' '
               60  LOAD_METHOD              join
               62  LOAD_GENEXPR             '<code_object <genexpr>>'
               64  LOAD_STR                 'Popen.__init__.<locals>.<genexpr>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_FAST                'cmd'
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'cmd'

 L.  59        78  LOAD_GLOBAL              spawn
               80  LOAD_METHOD              get_executable
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'python_exe'

 L.  63        86  LOAD_GLOBAL              WINENV
               88  POP_JUMP_IF_FALSE   130  'to 130'
               90  LOAD_GLOBAL              _path_eq
               92  LOAD_FAST                'python_exe'
               94  LOAD_GLOBAL              sys
               96  LOAD_ATTR                executable
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_FALSE   130  'to 130'

 L.  64       102  LOAD_GLOBAL              sys
              104  LOAD_ATTR                _base_executable
              106  STORE_FAST               'python_exe'

 L.  65       108  LOAD_GLOBAL              os
              110  LOAD_ATTR                environ
              112  LOAD_METHOD              copy
              114  CALL_METHOD_0         0  ''
              116  STORE_FAST               'env'

 L.  66       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                executable
              122  LOAD_FAST                'env'
              124  LOAD_STR                 '__PYVENV_LAUNCHER__'
              126  STORE_SUBSCR     
              128  JUMP_FORWARD        134  'to 134'
            130_0  COME_FROM           100  '100'
            130_1  COME_FROM            88  '88'

 L.  68       130  LOAD_CONST               None
              132  STORE_FAST               'env'
            134_0  COME_FROM           128  '128'

 L.  70       134  LOAD_GLOBAL              open
              136  LOAD_FAST                'wfd'
              138  LOAD_STR                 'wb'
              140  LOAD_CONST               True
              142  LOAD_CONST               ('closefd',)
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  SETUP_WITH          348  'to 348'
              148  STORE_FAST               'to_child'

 L.  72       150  SETUP_FINALLY       200  'to 200'

 L.  73       152  LOAD_GLOBAL              _winapi
              154  LOAD_METHOD              CreateProcess

 L.  74       156  LOAD_FAST                'python_exe'
              158  LOAD_FAST                'cmd'

 L.  75       160  LOAD_CONST               None
              162  LOAD_CONST               None
              164  LOAD_CONST               False
              166  LOAD_CONST               0
              168  LOAD_FAST                'env'
              170  LOAD_CONST               None
              172  LOAD_CONST               None

 L.  73       174  CALL_METHOD_9         9  ''
              176  UNPACK_SEQUENCE_4     4 
              178  STORE_FAST               'hp'
              180  STORE_FAST               'ht'
              182  STORE_FAST               'pid'
              184  STORE_FAST               'tid'

 L.  76       186  LOAD_GLOBAL              _winapi
              188  LOAD_METHOD              CloseHandle
              190  LOAD_FAST                'ht'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_FORWARD        224  'to 224'
            200_0  COME_FROM_FINALLY   150  '150'

 L.  77       200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L.  78       206  LOAD_GLOBAL              _winapi
              208  LOAD_METHOD              CloseHandle
              210  LOAD_FAST                'rhandle'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L.  79       216  RAISE_VARARGS_0       0  'reraise'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           198  '198'

 L.  82       224  LOAD_FAST                'pid'
              226  LOAD_FAST                'self'
              228  STORE_ATTR               pid

 L.  83       230  LOAD_CONST               None
              232  LOAD_FAST                'self'
              234  STORE_ATTR               returncode

 L.  84       236  LOAD_FAST                'hp'
              238  LOAD_FAST                'self'
              240  STORE_ATTR               _handle

 L.  85       242  LOAD_GLOBAL              int
              244  LOAD_FAST                'hp'
              246  CALL_FUNCTION_1       1  ''
              248  LOAD_FAST                'self'
              250  STORE_ATTR               sentinel

 L.  86       252  LOAD_GLOBAL              util
              254  LOAD_METHOD              Finalize
              256  LOAD_FAST                'self'
              258  LOAD_GLOBAL              _close_handles

 L.  87       260  LOAD_FAST                'self'
              262  LOAD_ATTR                sentinel
              264  LOAD_GLOBAL              int
              266  LOAD_FAST                'rhandle'
              268  CALL_FUNCTION_1       1  ''
              270  BUILD_TUPLE_2         2 

 L.  86       272  CALL_METHOD_3         3  ''
              274  LOAD_FAST                'self'
              276  STORE_ATTR               finalizer

 L.  90       278  LOAD_GLOBAL              set_spawning_popen
              280  LOAD_FAST                'self'
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          

 L.  91       286  SETUP_FINALLY       324  'to 324'

 L.  92       288  LOAD_GLOBAL              reduction
              290  LOAD_METHOD              dump
              292  LOAD_FAST                'prep_data'
              294  LOAD_FAST                'to_child'
              296  CALL_METHOD_2         2  ''
              298  POP_TOP          

 L.  93       300  LOAD_GLOBAL              reduction
              302  LOAD_METHOD              dump
              304  LOAD_FAST                'process_obj'
              306  LOAD_FAST                'to_child'
              308  CALL_METHOD_2         2  ''
              310  POP_TOP          
              312  POP_BLOCK        

 L.  95       314  LOAD_GLOBAL              set_spawning_popen
              316  LOAD_CONST               None
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          
              322  JUMP_FORWARD        334  'to 334'
            324_0  COME_FROM_FINALLY   286  '286'
              324  LOAD_GLOBAL              set_spawning_popen
              326  LOAD_CONST               None
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          
              332  <48>             
            334_0  COME_FROM           322  '322'
              334  POP_BLOCK        
              336  LOAD_CONST               None
              338  DUP_TOP          
              340  DUP_TOP          
              342  CALL_FUNCTION_3       3  ''
              344  POP_TOP          
              346  JUMP_FORWARD        366  'to 366'
            348_0  COME_FROM_WITH      146  '146'
              348  <49>             
          350_352  POP_JUMP_IF_TRUE    356  'to 356'
              354  <48>             
            356_0  COME_FROM           350  '350'
              356  POP_TOP          
              358  POP_TOP          
              360  POP_TOP          
              362  POP_EXCEPT       
              364  POP_TOP          
            366_0  COME_FROM           346  '346'

Parse error at or near `<48>' instruction at offset 222

    def duplicate_for_child--- This code section failed: ---

 L.  98         0  LOAD_FAST                'self'
                2  LOAD_GLOBAL              get_spawning_popen
                4  CALL_FUNCTION_0       0  ''
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.  99        14  LOAD_GLOBAL              reduction
               16  LOAD_METHOD              duplicate
               18  LOAD_FAST                'handle'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                sentinel
               24  CALL_METHOD_2         2  ''
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def wait--- This code section failed: ---

 L. 102         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE   110  'to 110'

 L. 103        10  LOAD_FAST                'timeout'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 104        18  LOAD_GLOBAL              _winapi
               20  LOAD_ATTR                INFINITE
               22  STORE_FAST               'msecs'
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM            16  '16'

 L. 106        26  LOAD_GLOBAL              max
               28  LOAD_CONST               0
               30  LOAD_GLOBAL              int
               32  LOAD_FAST                'timeout'
               34  LOAD_CONST               1000
               36  BINARY_MULTIPLY  
               38  LOAD_CONST               0.5
               40  BINARY_ADD       
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_2       2  ''
               46  STORE_FAST               'msecs'
             48_0  COME_FROM            24  '24'

 L. 108        48  LOAD_GLOBAL              _winapi
               50  LOAD_METHOD              WaitForSingleObject
               52  LOAD_GLOBAL              int
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _handle
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'msecs'
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'res'

 L. 109        66  LOAD_FAST                'res'
               68  LOAD_GLOBAL              _winapi
               70  LOAD_ATTR                WAIT_OBJECT_0
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L. 110        76  LOAD_GLOBAL              _winapi
               78  LOAD_METHOD              GetExitCodeProcess
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _handle
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'code'

 L. 111        88  LOAD_FAST                'code'
               90  LOAD_GLOBAL              TERMINATE
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 112        96  LOAD_GLOBAL              signal
               98  LOAD_ATTR                SIGTERM
              100  UNARY_NEGATIVE   
              102  STORE_FAST               'code'
            104_0  COME_FROM            94  '94'

 L. 113       104  LOAD_FAST                'code'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               returncode
            110_0  COME_FROM            74  '74'
            110_1  COME_FROM             8  '8'

 L. 115       110  LOAD_FAST                'self'
              112  LOAD_ATTR                returncode
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def poll(self):
        return self.wait(timeout=0)

    def terminate--- This code section failed: ---

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L. 122        10  SETUP_FINALLY        34  'to 34'

 L. 123        12  LOAD_GLOBAL              _winapi
               14  LOAD_METHOD              TerminateProcess
               16  LOAD_GLOBAL              int
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _handle
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_GLOBAL              TERMINATE
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          
               30  POP_BLOCK        
               32  JUMP_FORWARD         70  'to 70'
             34_0  COME_FROM_FINALLY    10  '10'

 L. 124        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  <121>                68  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 125        46  LOAD_FAST                'self'
               48  LOAD_ATTR                wait
               50  LOAD_CONST               1.0
               52  LOAD_CONST               ('timeout',)
               54  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               56  LOAD_CONST               None
               58  <117>                 0  ''
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L. 126        62  RAISE_VARARGS_0       0  'reraise'
             64_0  COME_FROM            60  '60'
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
               68  <48>             
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            32  '32'
             70_2  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    kill = terminate

    def close(self):
        self.finalizer()