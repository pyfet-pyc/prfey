# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\popen_fork.py
import os, signal
from . import util
__all__ = [
 'Popen']

class Popen(object):
    method = 'fork'

    def __init__(self, process_obj):
        util._flush_std_streams()
        self.returncode = None
        self.finalizer = None
        self._launch(process_obj)

    def duplicate_for_child(self, fd):
        return fd

    def poll--- This code section failed: ---

 L.  25         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    76  'to 76'

 L.  26        10  SETUP_FINALLY        34  'to 34'

 L.  27        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              waitpid
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                pid
               20  LOAD_FAST                'flag'
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'pid'
               28  STORE_FAST               'sts'
               30  POP_BLOCK        
               32  JUMP_FORWARD         54  'to 54'
             34_0  COME_FROM_FINALLY    10  '10'

 L.  28        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  <121>                52  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  31        46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  RETURN_VALUE     
               52  <48>             
             54_0  COME_FROM            32  '32'

 L.  32        54  LOAD_FAST                'pid'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                pid
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L.  33        64  LOAD_GLOBAL              os
               66  LOAD_METHOD              waitstatus_to_exitcode
               68  LOAD_FAST                'sts'
               70  CALL_METHOD_1         1  ''
               72  LOAD_FAST                'self'
               74  STORE_ATTR               returncode
             76_0  COME_FROM            62  '62'
             76_1  COME_FROM             8  '8'

 L.  34        76  LOAD_FAST                'self'
               78  LOAD_ATTR                returncode
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def wait--- This code section failed: ---

 L.  37         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    72  'to 72'

 L.  38        10  LOAD_FAST                'timeout'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    48  'to 48'

 L.  39        18  LOAD_CONST               0
               20  LOAD_CONST               ('wait',)
               22  IMPORT_NAME_ATTR         multiprocessing.connection
               24  IMPORT_FROM              wait
               26  STORE_FAST               'wait'
               28  POP_TOP          

 L.  40        30  LOAD_FAST                'wait'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                sentinel
               36  BUILD_LIST_1          1 
               38  LOAD_FAST                'timeout'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_TRUE     48  'to 48'

 L.  41        44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'
             48_1  COME_FROM            16  '16'

 L.  43        48  LOAD_FAST                'self'
               50  LOAD_METHOD              poll
               52  LOAD_FAST                'timeout'
               54  LOAD_CONST               0.0
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    66  'to 66'
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                WNOHANG
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            58  '58'
               66  LOAD_CONST               0
             68_0  COME_FROM            64  '64'
               68  CALL_METHOD_1         1  ''
               70  RETURN_VALUE     
             72_0  COME_FROM             8  '8'

 L.  44        72  LOAD_FAST                'self'
               74  LOAD_ATTR                returncode
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _send_signal--- This code section failed: ---

 L.  47         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    82  'to 82'

 L.  48        10  SETUP_FINALLY        30  'to 30'

 L.  49        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              kill
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                pid
               20  LOAD_FAST                'sig'
               22  CALL_METHOD_2         2  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD         82  'to 82'
             30_0  COME_FROM_FINALLY    10  '10'

 L.  50        30  DUP_TOP          
               32  LOAD_GLOBAL              ProcessLookupError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  51        42  POP_EXCEPT       
               44  JUMP_FORWARD         82  'to 82'

 L.  52        46  DUP_TOP          
               48  LOAD_GLOBAL              OSError
               50  <121>                80  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  53        58  LOAD_FAST                'self'
               60  LOAD_ATTR                wait
               62  LOAD_CONST               0.1
               64  LOAD_CONST               ('timeout',)
               66  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               68  LOAD_CONST               None
               70  <117>                 0  ''
               72  POP_JUMP_IF_FALSE    76  'to 76'

 L.  54        74  RAISE_VARARGS_0       0  'reraise'
             76_0  COME_FROM            72  '72'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            44  '44'
             82_2  COME_FROM            28  '28'
             82_3  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def terminate(self):
        self._send_signal(signal.SIGTERM)

    def kill(self):
        self._send_signal(signal.SIGKILL)

    def _launch--- This code section failed: ---

 L.  63         0  LOAD_CONST               1
                2  STORE_FAST               'code'

 L.  64         4  LOAD_GLOBAL              os
                6  LOAD_METHOD              pipe
                8  CALL_METHOD_0         0  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'parent_r'
               14  STORE_FAST               'child_w'

 L.  65        16  LOAD_GLOBAL              os
               18  LOAD_METHOD              pipe
               20  CALL_METHOD_0         0  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'child_r'
               26  STORE_FAST               'parent_w'

 L.  66        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              fork
               32  CALL_METHOD_0         0  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               pid

 L.  67        38  LOAD_FAST                'self'
               40  LOAD_ATTR                pid
               42  LOAD_CONST               0
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE   110  'to 110'

 L.  68        48  SETUP_FINALLY        96  'to 96'

 L.  69        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              close
               54  LOAD_FAST                'parent_r'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  70        60  LOAD_GLOBAL              os
               62  LOAD_METHOD              close
               64  LOAD_FAST                'parent_w'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.  71        70  LOAD_FAST                'process_obj'
               72  LOAD_ATTR                _bootstrap
               74  LOAD_FAST                'child_r'
               76  LOAD_CONST               ('parent_sentinel',)
               78  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               80  STORE_FAST               'code'
               82  POP_BLOCK        

 L.  73        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              _exit
               88  LOAD_FAST                'code'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  JUMP_FORWARD        158  'to 158'
             96_0  COME_FROM_FINALLY    48  '48'
               96  LOAD_GLOBAL              os
               98  LOAD_METHOD              _exit
              100  LOAD_FAST                'code'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  <48>             
              108  JUMP_FORWARD        158  'to 158'
            110_0  COME_FROM            46  '46'

 L.  75       110  LOAD_GLOBAL              os
              112  LOAD_METHOD              close
              114  LOAD_FAST                'child_w'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L.  76       120  LOAD_GLOBAL              os
              122  LOAD_METHOD              close
              124  LOAD_FAST                'child_r'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L.  77       130  LOAD_GLOBAL              util
              132  LOAD_METHOD              Finalize
              134  LOAD_FAST                'self'
              136  LOAD_GLOBAL              util
              138  LOAD_ATTR                close_fds

 L.  78       140  LOAD_FAST                'parent_r'
              142  LOAD_FAST                'parent_w'
              144  BUILD_TUPLE_2         2 

 L.  77       146  CALL_METHOD_3         3  ''
              148  LOAD_FAST                'self'
              150  STORE_ATTR               finalizer

 L.  79       152  LOAD_FAST                'parent_r'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               sentinel
            158_0  COME_FROM           108  '108'
            158_1  COME_FROM            94  '94'

Parse error at or near `POP_TOP' instruction at offset 92

    def close--- This code section failed: ---

 L.  82         0  LOAD_FAST                'self'
                2  LOAD_ATTR                finalizer
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  83        10  LOAD_FAST                'self'
               12  LOAD_METHOD              finalizer
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1