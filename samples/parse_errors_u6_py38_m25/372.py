# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE   146  'to 146'

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
               32  JUMP_FORWARD         74  'to 74'
             34_0  COME_FROM_FINALLY    10  '10'

 L.  28        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    72  'to 72'
               42  POP_TOP          
               44  STORE_FAST               'e'
               46  POP_TOP          
               48  SETUP_FINALLY        60  'to 60'

 L.  31        50  POP_BLOCK        
               52  POP_EXCEPT       
               54  CALL_FINALLY         60  'to 60'
               56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'
             60_1  COME_FROM_FINALLY    48  '48'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            40  '40'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            32  '32'

 L.  32        74  LOAD_FAST                'pid'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                pid
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   146  'to 146'

 L.  33        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              WIFSIGNALED
               88  LOAD_FAST                'sts'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE   110  'to 110'

 L.  34        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              WTERMSIG
               98  LOAD_FAST                'sts'
              100  CALL_METHOD_1         1  ''
              102  UNARY_NEGATIVE   
              104  LOAD_FAST                'self'
              106  STORE_ATTR               returncode
              108  JUMP_FORWARD        146  'to 146'
            110_0  COME_FROM            92  '92'

 L.  36       110  LOAD_GLOBAL              os
              112  LOAD_METHOD              WIFEXITED
              114  LOAD_FAST                'sts'
              116  CALL_METHOD_1         1  ''
              118  POP_JUMP_IF_TRUE    134  'to 134'
              120  LOAD_ASSERT              AssertionError
              122  LOAD_STR                 'Status is {:n}'
              124  LOAD_METHOD              format
              126  LOAD_FAST                'sts'
              128  CALL_METHOD_1         1  ''
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           118  '118'

 L.  37       134  LOAD_GLOBAL              os
              136  LOAD_METHOD              WEXITSTATUS
              138  LOAD_FAST                'sts'
              140  CALL_METHOD_1         1  ''
              142  LOAD_FAST                'self'
              144  STORE_ATTR               returncode
            146_0  COME_FROM           108  '108'
            146_1  COME_FROM            82  '82'
            146_2  COME_FROM             8  '8'

 L.  38       146  LOAD_FAST                'self'
              148  LOAD_ATTR                returncode
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 54

    def wait(self, timeout=None):
        if self.returncode is None:
            if timeout is not None:
                from multiprocessing.connection import wait
                if not wait([self.sentinel], timeout):
                    return
            return self.poll(os.WNOHANG if timeout == 0.0 else 0)
        return self.returncode

    def _send_signal(self, sig):
        if self.returncode is None:
            try:
                os.killself.pidsig
            except ProcessLookupError:
                pass
            except OSError:
                if self.wait(timeout=0.1) is None:
                    raise

    def terminate(self):
        self._send_signal(signal.SIGTERM)

    def kill(self):
        self._send_signal(signal.SIGKILL)

    def _launch(self, process_obj):
        code = 1
        parent_r, child_w = os.pipe()
        child_r, parent_w = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            try:
                os.close(parent_r)
                os.close(parent_w)
                code = process_obj._bootstrap(parent_sentinel=child_r)
            finally:
                os._exit(code)

        else:
            os.close(child_w)
            os.close(child_r)
            self.finalizer = util.Finalize(self, util.close_fds, (
             parent_r, parent_w))
            self.sentinel = parent_r

    def close(self):
        if self.finalizer is not None:
            self.finalizer()