# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\forkserver.py
import errno, os, selectors, signal, socket, struct, sys, threading, warnings
from . import connection
from . import process
from .context import reduction
from . import resource_tracker
from . import spawn
from . import util
__all__ = [
 'ensure_running', 'get_inherited_fds', 'connect_to_new_process',
 'set_forkserver_preload']
MAXFDS_TO_SEND = 256
SIGNED_STRUCT = struct.Struct('q')

class ForkServer(object):

    def __init__(self):
        self._forkserver_address = None
        self._forkserver_alive_fd = None
        self._forkserver_pid = None
        self._inherited_fds = None
        self._lock = threading.Lock()
        self._preload_modules = ['__main__']

    def _stop(self):
        with self._lock:
            self._stop_unlocked()

    def _stop_unlocked(self):
        if self._forkserver_pid is None:
            return
        os.close(self._forkserver_alive_fd)
        self._forkserver_alive_fd = None
        os.waitpid(self._forkserver_pid, 0)
        self._forkserver_pid = None
        os.unlink(self._forkserver_address)
        self._forkserver_address = None

    def set_forkserver_preload(self, modules_names):
        """Set list of module names to try to load in forkserver process."""
        if not all((type(mod) is str for mod in self._preload_modules)):
            raise TypeError('module_names must be a list of strings')
        self._preload_modules = modules_names

    def get_inherited_fds(self):
        """Return list of fds inherited from parent process.

        This returns None if the current process was not started by fork
        server.
        """
        return self._inherited_fds

    def connect_to_new_process--- This code section failed: ---

 L.  83         0  LOAD_FAST                'self'
                2  LOAD_METHOD              ensure_running
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  84         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'fds'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               4
               16  BINARY_ADD       
               18  LOAD_GLOBAL              MAXFDS_TO_SEND
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.  85        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'too many fds'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  86        32  LOAD_GLOBAL              socket
               34  LOAD_METHOD              socket
               36  LOAD_GLOBAL              socket
               38  LOAD_ATTR                AF_UNIX
               40  CALL_METHOD_1         1  ''
               42  SETUP_WITH          214  'to 214'
               44  STORE_FAST               'client'

 L.  87        46  LOAD_FAST                'client'
               48  LOAD_METHOD              connect
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _forkserver_address
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  88        58  LOAD_GLOBAL              os
               60  LOAD_METHOD              pipe
               62  CALL_METHOD_0         0  ''
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'parent_r'
               68  STORE_FAST               'child_w'

 L.  89        70  LOAD_GLOBAL              os
               72  LOAD_METHOD              pipe
               74  CALL_METHOD_0         0  ''
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'child_r'
               80  STORE_FAST               'parent_w'

 L.  90        82  LOAD_FAST                'child_r'
               84  LOAD_FAST                'child_w'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _forkserver_alive_fd

 L.  91        90  LOAD_GLOBAL              resource_tracker
               92  LOAD_METHOD              getfd
               94  CALL_METHOD_0         0  ''

 L.  90        96  BUILD_LIST_4          4 
               98  STORE_FAST               'allfds'

 L.  92       100  LOAD_FAST                'allfds'
              102  LOAD_FAST                'fds'
              104  INPLACE_ADD      
              106  STORE_FAST               'allfds'

 L.  93       108  SETUP_FINALLY       188  'to 188'
              110  SETUP_FINALLY       150  'to 150'

 L.  94       112  LOAD_GLOBAL              reduction
              114  LOAD_METHOD              sendfds
              116  LOAD_FAST                'client'
              118  LOAD_FAST                'allfds'
              120  CALL_METHOD_2         2  ''
              122  POP_TOP          

 L.  95       124  LOAD_FAST                'parent_r'
              126  LOAD_FAST                'parent_w'
              128  BUILD_TUPLE_2         2 
              130  POP_BLOCK        
              132  POP_BLOCK        
              134  CALL_FINALLY        188  'to 188'
              136  POP_BLOCK        
              138  ROT_TWO          
              140  BEGIN_FINALLY    
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  POP_FINALLY           0  ''
              148  RETURN_VALUE     
            150_0  COME_FROM_FINALLY   110  '110'

 L.  96       150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L.  97       156  LOAD_GLOBAL              os
              158  LOAD_METHOD              close
              160  LOAD_FAST                'parent_r'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L.  98       166  LOAD_GLOBAL              os
              168  LOAD_METHOD              close
              170  LOAD_FAST                'parent_w'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L.  99       176  RAISE_VARARGS_0       0  'reraise'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM           134  '134'
            188_1  COME_FROM_FINALLY   108  '108'

 L. 101       188  LOAD_GLOBAL              os
              190  LOAD_METHOD              close
              192  LOAD_FAST                'child_r'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 102       198  LOAD_GLOBAL              os
              200  LOAD_METHOD              close
              202  LOAD_FAST                'child_w'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
              208  END_FINALLY      
              210  POP_BLOCK        
              212  BEGIN_FINALLY    
            214_0  COME_FROM_WITH       42  '42'
              214  WITH_CLEANUP_START
              216  WITH_CLEANUP_FINISH
              218  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 132

    def ensure_running--- This code section failed: ---

 L. 111         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
              4_6  SETUP_WITH          380  'to 380'
                8  POP_TOP          

 L. 112        10  LOAD_GLOBAL              resource_tracker
               12  LOAD_METHOD              ensure_running
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 113        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _forkserver_pid
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE    96  'to 96'

 L. 115        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              waitpid
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _forkserver_pid
               36  LOAD_GLOBAL              os
               38  LOAD_ATTR                WNOHANG
               40  CALL_METHOD_2         2  ''
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'pid'
               46  STORE_FAST               'status'

 L. 116        48  LOAD_FAST                'pid'
               50  POP_JUMP_IF_TRUE     66  'to 66'

 L. 118        52  POP_BLOCK        
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM            50  '50'

 L. 120        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              close
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _forkserver_alive_fd
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 121        78  LOAD_CONST               None
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _forkserver_address

 L. 122        84  LOAD_CONST               None
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _forkserver_alive_fd

 L. 123        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _forkserver_pid
             96_0  COME_FROM            26  '26'

 L. 125        96  LOAD_STR                 'from multiprocessing.forkserver import main; main(%d, %d, %r, **%r)'
               98  STORE_FAST               'cmd'

 L. 128       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _preload_modules
              104  POP_JUMP_IF_FALSE   148  'to 148'

 L. 129       106  LOAD_STR                 'main_path'
              108  LOAD_STR                 'sys_path'
              110  BUILD_SET_2           2 
              112  STORE_DEREF              'desired_keys'

 L. 130       114  LOAD_GLOBAL              spawn
              116  LOAD_METHOD              get_preparation_data
              118  LOAD_STR                 'ignore'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'data'

 L. 131       124  LOAD_CLOSURE             'desired_keys'
              126  BUILD_TUPLE_1         1 
              128  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              130  LOAD_STR                 'ForkServer.ensure_running.<locals>.<dictcomp>'
              132  MAKE_FUNCTION_8          'closure'
              134  LOAD_FAST                'data'
              136  LOAD_METHOD              items
              138  CALL_METHOD_0         0  ''
              140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'data'
              146  JUMP_FORWARD        152  'to 152'
            148_0  COME_FROM           104  '104'

 L. 133       148  BUILD_MAP_0           0 
              150  STORE_FAST               'data'
            152_0  COME_FROM           146  '146'

 L. 135       152  LOAD_GLOBAL              socket
              154  LOAD_METHOD              socket
              156  LOAD_GLOBAL              socket
              158  LOAD_ATTR                AF_UNIX
              160  CALL_METHOD_1         1  ''
              162  SETUP_WITH          370  'to 370'
              164  STORE_FAST               'listener'

 L. 136       166  LOAD_GLOBAL              connection
              168  LOAD_METHOD              arbitrary_address
              170  LOAD_STR                 'AF_UNIX'
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'address'

 L. 137       176  LOAD_FAST                'listener'
              178  LOAD_METHOD              bind
              180  LOAD_FAST                'address'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 138       186  LOAD_GLOBAL              os
              188  LOAD_METHOD              chmod
              190  LOAD_FAST                'address'
              192  LOAD_CONST               384
              194  CALL_METHOD_2         2  ''
              196  POP_TOP          

 L. 139       198  LOAD_FAST                'listener'
              200  LOAD_METHOD              listen
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          

 L. 143       206  LOAD_GLOBAL              os
              208  LOAD_METHOD              pipe
              210  CALL_METHOD_0         0  ''
              212  UNPACK_SEQUENCE_2     2 
              214  STORE_FAST               'alive_r'
              216  STORE_FAST               'alive_w'

 L. 144       218  SETUP_FINALLY       336  'to 336'
              220  SETUP_FINALLY       308  'to 308'

 L. 145       222  LOAD_FAST                'listener'
              224  LOAD_METHOD              fileno
              226  CALL_METHOD_0         0  ''
              228  LOAD_FAST                'alive_r'
              230  BUILD_LIST_2          2 
              232  STORE_FAST               'fds_to_pass'

 L. 146       234  LOAD_FAST                'cmd'
              236  LOAD_FAST                'listener'
              238  LOAD_METHOD              fileno
              240  CALL_METHOD_0         0  ''
              242  LOAD_FAST                'alive_r'
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                _preload_modules

 L. 147       248  LOAD_FAST                'data'

 L. 146       250  BUILD_TUPLE_4         4 
              252  INPLACE_MODULO   
              254  STORE_FAST               'cmd'

 L. 148       256  LOAD_GLOBAL              spawn
              258  LOAD_METHOD              get_executable
              260  CALL_METHOD_0         0  ''
              262  STORE_FAST               'exe'

 L. 149       264  LOAD_FAST                'exe'
              266  BUILD_LIST_1          1 
              268  LOAD_GLOBAL              util
              270  LOAD_METHOD              _args_from_interpreter_flags
              272  CALL_METHOD_0         0  ''
              274  BINARY_ADD       
              276  STORE_FAST               'args'

 L. 150       278  LOAD_FAST                'args'
              280  LOAD_STR                 '-c'
              282  LOAD_FAST                'cmd'
              284  BUILD_LIST_2          2 
              286  INPLACE_ADD      
              288  STORE_FAST               'args'

 L. 151       290  LOAD_GLOBAL              util
              292  LOAD_METHOD              spawnv_passfds
              294  LOAD_FAST                'exe'
              296  LOAD_FAST                'args'
              298  LOAD_FAST                'fds_to_pass'
              300  CALL_METHOD_3         3  ''
              302  STORE_FAST               'pid'
              304  POP_BLOCK        
              306  JUMP_FORWARD        332  'to 332'
            308_0  COME_FROM_FINALLY   220  '220'

 L. 152       308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 153       314  LOAD_GLOBAL              os
              316  LOAD_METHOD              close
              318  LOAD_FAST                'alive_w'
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L. 154       324  RAISE_VARARGS_0       0  'reraise'
              326  POP_EXCEPT       
              328  JUMP_FORWARD        332  'to 332'
              330  END_FINALLY      
            332_0  COME_FROM           328  '328'
            332_1  COME_FROM           306  '306'
              332  POP_BLOCK        
              334  BEGIN_FINALLY    
            336_0  COME_FROM_FINALLY   218  '218'

 L. 156       336  LOAD_GLOBAL              os
              338  LOAD_METHOD              close
              340  LOAD_FAST                'alive_r'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          
              346  END_FINALLY      

 L. 157       348  LOAD_FAST                'address'
              350  LOAD_FAST                'self'
              352  STORE_ATTR               _forkserver_address

 L. 158       354  LOAD_FAST                'alive_w'
              356  LOAD_FAST                'self'
              358  STORE_ATTR               _forkserver_alive_fd

 L. 159       360  LOAD_FAST                'pid'
              362  LOAD_FAST                'self'
              364  STORE_ATTR               _forkserver_pid
              366  POP_BLOCK        
              368  BEGIN_FINALLY    
            370_0  COME_FROM_WITH      162  '162'
              370  WITH_CLEANUP_START
              372  WITH_CLEANUP_FINISH
              374  END_FINALLY      
              376  POP_BLOCK        
              378  BEGIN_FINALLY    
            380_0  COME_FROM_WITH        4  '4'
              380  WITH_CLEANUP_START
              382  WITH_CLEANUP_FINISH
              384  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 54


def main--- This code section failed: ---

 L. 167         0  LOAD_FAST                'preload'
                2  POP_JUMP_IF_FALSE   100  'to 100'

 L. 168         4  LOAD_STR                 '__main__'
                6  LOAD_FAST                'preload'
                8  COMPARE_OP               in
               10  POP_JUMP_IF_FALSE    56  'to 56'
               12  LOAD_FAST                'main_path'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 169        20  LOAD_CONST               True
               22  LOAD_GLOBAL              process
               24  LOAD_METHOD              current_process
               26  CALL_METHOD_0         0  ''
               28  STORE_ATTR               _inheriting

 L. 170        30  SETUP_FINALLY        46  'to 46'

 L. 171        32  LOAD_GLOBAL              spawn
               34  LOAD_METHOD              import_main_path
               36  LOAD_FAST                'main_path'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  BEGIN_FINALLY    
             46_0  COME_FROM_FINALLY    30  '30'

 L. 173        46  LOAD_GLOBAL              process
               48  LOAD_METHOD              current_process
               50  CALL_METHOD_0         0  ''
               52  DELETE_ATTR              _inheriting
               54  END_FINALLY      
             56_0  COME_FROM            18  '18'
             56_1  COME_FROM            10  '10'

 L. 174        56  LOAD_FAST                'preload'
               58  GET_ITER         
               60  FOR_ITER            100  'to 100'
               62  STORE_FAST               'modname'

 L. 175        64  SETUP_FINALLY        78  'to 78'

 L. 176        66  LOAD_GLOBAL              __import__
               68  LOAD_FAST                'modname'
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_BACK            60  'to 60'
             78_0  COME_FROM_FINALLY    64  '64'

 L. 177        78  DUP_TOP          
               80  LOAD_GLOBAL              ImportError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE    96  'to 96'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 178        92  POP_EXCEPT       
               94  JUMP_BACK            60  'to 60'
             96_0  COME_FROM            84  '84'
               96  END_FINALLY      
               98  JUMP_BACK            60  'to 60'
            100_0  COME_FROM             2  '2'

 L. 180       100  LOAD_GLOBAL              util
              102  LOAD_METHOD              _close_stdin
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          

 L. 182       108  LOAD_GLOBAL              os
              110  LOAD_METHOD              pipe
              112  CALL_METHOD_0         0  ''
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'sig_r'
              118  STORE_FAST               'sig_w'

 L. 183       120  LOAD_GLOBAL              os
              122  LOAD_METHOD              set_blocking
              124  LOAD_FAST                'sig_r'
              126  LOAD_CONST               False
              128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L. 184       132  LOAD_GLOBAL              os
              134  LOAD_METHOD              set_blocking
              136  LOAD_FAST                'sig_w'
              138  LOAD_CONST               False
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L. 186       144  LOAD_CODE                <code_object sigchld_handler>
              146  LOAD_STR                 'main.<locals>.sigchld_handler'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  STORE_FAST               'sigchld_handler'

 L. 192       152  LOAD_GLOBAL              signal
              154  LOAD_ATTR                SIGCHLD

 L. 192       156  LOAD_FAST                'sigchld_handler'

 L. 194       158  LOAD_GLOBAL              signal
              160  LOAD_ATTR                SIGINT

 L. 194       162  LOAD_GLOBAL              signal
              164  LOAD_ATTR                SIG_IGN

 L. 190       166  BUILD_MAP_2           2 
              168  STORE_FAST               'handlers'

 L. 196       170  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              172  LOAD_STR                 'main.<locals>.<dictcomp>'
              174  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 197       176  LOAD_FAST                'handlers'
              178  LOAD_METHOD              items
              180  CALL_METHOD_0         0  ''

 L. 196       182  GET_ITER         
              184  CALL_FUNCTION_1       1  ''
              186  STORE_FAST               'old_handlers'

 L. 200       188  LOAD_GLOBAL              signal
              190  LOAD_METHOD              set_wakeup_fd
              192  LOAD_FAST                'sig_w'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 203       198  BUILD_MAP_0           0 
              200  STORE_FAST               'pid_to_fd'

 L. 205       202  LOAD_GLOBAL              socket
              204  LOAD_ATTR                socket
              206  LOAD_GLOBAL              socket
              208  LOAD_ATTR                AF_UNIX
              210  LOAD_FAST                'listener_fd'
              212  LOAD_CONST               ('fileno',)
              214  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
          216_218  SETUP_WITH         1008  'to 1008'
              220  STORE_FAST               'listener'

 L. 206       222  LOAD_GLOBAL              selectors
              224  LOAD_METHOD              DefaultSelector
              226  CALL_METHOD_0         0  ''

 L. 205   228_230  SETUP_WITH          998  'to 998'

 L. 206       232  STORE_FAST               'selector'

 L. 207       234  LOAD_FAST                'listener'
              236  LOAD_METHOD              getsockname
              238  CALL_METHOD_0         0  ''
              240  LOAD_GLOBAL              _forkserver
              242  STORE_ATTR               _forkserver_address

 L. 209       244  LOAD_FAST                'selector'
              246  LOAD_METHOD              register
              248  LOAD_FAST                'listener'
              250  LOAD_GLOBAL              selectors
              252  LOAD_ATTR                EVENT_READ
              254  CALL_METHOD_2         2  ''
              256  POP_TOP          

 L. 210       258  LOAD_FAST                'selector'
              260  LOAD_METHOD              register
              262  LOAD_FAST                'alive_r'
              264  LOAD_GLOBAL              selectors
              266  LOAD_ATTR                EVENT_READ
              268  CALL_METHOD_2         2  ''
              270  POP_TOP          

 L. 211       272  LOAD_FAST                'selector'
              274  LOAD_METHOD              register
              276  LOAD_FAST                'sig_r'
              278  LOAD_GLOBAL              selectors
              280  LOAD_ATTR                EVENT_READ
              282  CALL_METHOD_2         2  ''
              284  POP_TOP          

 L. 214   286_288  SETUP_FINALLY       938  'to 938'
            290_0  COME_FROM           310  '310'

 L. 216       290  LOAD_LISTCOMP            '<code_object <listcomp>>'
              292  LOAD_STR                 'main.<locals>.<listcomp>'
              294  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              296  LOAD_FAST                'selector'
              298  LOAD_METHOD              select
              300  CALL_METHOD_0         0  ''
              302  GET_ITER         
              304  CALL_FUNCTION_1       1  ''
              306  STORE_FAST               'rfds'

 L. 217       308  LOAD_FAST                'rfds'
          310_312  POP_JUMP_IF_FALSE   290  'to 290'

 L. 218   314_316  BREAK_LOOP          322  'to 322'
          318_320  JUMP_BACK           290  'to 290'

 L. 220       322  LOAD_FAST                'alive_r'
              324  LOAD_FAST                'rfds'
              326  COMPARE_OP               in
          328_330  POP_JUMP_IF_FALSE   362  'to 362'

 L. 222       332  LOAD_GLOBAL              os
              334  LOAD_METHOD              read
              336  LOAD_FAST                'alive_r'
              338  LOAD_CONST               1
              340  CALL_METHOD_2         2  ''
              342  LOAD_CONST               b''
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_TRUE    358  'to 358'
              350  LOAD_ASSERT              AssertionError
              352  LOAD_STR                 'Not at EOF?'
              354  CALL_FUNCTION_1       1  ''
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           346  '346'

 L. 223       358  LOAD_GLOBAL              SystemExit
              360  RAISE_VARARGS_1       1  'exception instance'
            362_0  COME_FROM           328  '328'

 L. 225       362  LOAD_FAST                'sig_r'
              364  LOAD_FAST                'rfds'
              366  COMPARE_OP               in
          368_370  POP_JUMP_IF_FALSE   604  'to 604'

 L. 227       372  LOAD_GLOBAL              os
              374  LOAD_METHOD              read
              376  LOAD_FAST                'sig_r'
              378  LOAD_CONST               65536
              380  CALL_METHOD_2         2  ''
              382  POP_TOP          

 L. 230       384  SETUP_FINALLY       408  'to 408'

 L. 231       386  LOAD_GLOBAL              os
              388  LOAD_METHOD              waitpid
              390  LOAD_CONST               -1
              392  LOAD_GLOBAL              os
              394  LOAD_ATTR                WNOHANG
              396  CALL_METHOD_2         2  ''
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'pid'
              402  STORE_FAST               'sts'
              404  POP_BLOCK        
              406  JUMP_FORWARD        436  'to 436'
            408_0  COME_FROM_FINALLY   384  '384'

 L. 232       408  DUP_TOP          
              410  LOAD_GLOBAL              ChildProcessError
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   434  'to 434'
              418  POP_TOP          
              420  POP_TOP          
              422  POP_TOP          

 L. 233       424  POP_EXCEPT       
          426_428  JUMP_ABSOLUTE       604  'to 604'
              430  POP_EXCEPT       
              432  JUMP_FORWARD        436  'to 436'
            434_0  COME_FROM           414  '414'
              434  END_FINALLY      
            436_0  COME_FROM           432  '432'
            436_1  COME_FROM           406  '406'

 L. 234       436  LOAD_FAST                'pid'
              438  LOAD_CONST               0
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   450  'to 450'

 L. 235   446_448  BREAK_LOOP          604  'to 604'
            450_0  COME_FROM           442  '442'

 L. 236       450  LOAD_FAST                'pid_to_fd'
              452  LOAD_METHOD              pop
              454  LOAD_FAST                'pid'
              456  LOAD_CONST               None
              458  CALL_METHOD_2         2  ''
              460  STORE_FAST               'child_w'

 L. 237       462  LOAD_FAST                'child_w'
              464  LOAD_CONST               None
              466  COMPARE_OP               is-not
          468_470  POP_JUMP_IF_FALSE   586  'to 586'

 L. 238       472  LOAD_GLOBAL              os
              474  LOAD_METHOD              WIFSIGNALED
              476  LOAD_FAST                'sts'
              478  CALL_METHOD_1         1  ''
          480_482  POP_JUMP_IF_FALSE   498  'to 498'

 L. 239       484  LOAD_GLOBAL              os
              486  LOAD_METHOD              WTERMSIG
              488  LOAD_FAST                'sts'
              490  CALL_METHOD_1         1  ''
              492  UNARY_NEGATIVE   
              494  STORE_FAST               'returncode'
              496  JUMP_FORWARD        536  'to 536'
            498_0  COME_FROM           480  '480'

 L. 241       498  LOAD_GLOBAL              os
              500  LOAD_METHOD              WIFEXITED
              502  LOAD_FAST                'sts'
              504  CALL_METHOD_1         1  ''
          506_508  POP_JUMP_IF_TRUE    526  'to 526'

 L. 242       510  LOAD_ASSERT              AssertionError

 L. 243       512  LOAD_STR                 'Child {0:n} status is {1:n}'
              514  LOAD_METHOD              format

 L. 244       516  LOAD_FAST                'pid'

 L. 244       518  LOAD_FAST                'sts'

 L. 243       520  CALL_METHOD_2         2  ''

 L. 242       522  CALL_FUNCTION_1       1  ''
              524  RAISE_VARARGS_1       1  'exception instance'
            526_0  COME_FROM           506  '506'

 L. 245       526  LOAD_GLOBAL              os
              528  LOAD_METHOD              WEXITSTATUS
              530  LOAD_FAST                'sts'
              532  CALL_METHOD_1         1  ''
              534  STORE_FAST               'returncode'
            536_0  COME_FROM           496  '496'

 L. 247       536  SETUP_FINALLY       552  'to 552'

 L. 248       538  LOAD_GLOBAL              write_signed
              540  LOAD_FAST                'child_w'
              542  LOAD_FAST                'returncode'
              544  CALL_FUNCTION_2       2  ''
              546  POP_TOP          
              548  POP_BLOCK        
              550  JUMP_FORWARD        574  'to 574'
            552_0  COME_FROM_FINALLY   536  '536'

 L. 249       552  DUP_TOP          
              554  LOAD_GLOBAL              BrokenPipeError
              556  COMPARE_OP               exception-match
          558_560  POP_JUMP_IF_FALSE   572  'to 572'
              562  POP_TOP          
              564  POP_TOP          
              566  POP_TOP          

 L. 251       568  POP_EXCEPT       
              570  JUMP_FORWARD        574  'to 574'
            572_0  COME_FROM           558  '558'
              572  END_FINALLY      
            574_0  COME_FROM           570  '570'
            574_1  COME_FROM           550  '550'

 L. 252       574  LOAD_GLOBAL              os
              576  LOAD_METHOD              close
              578  LOAD_FAST                'child_w'
              580  CALL_METHOD_1         1  ''
              582  POP_TOP          
              584  JUMP_BACK           384  'to 384'
            586_0  COME_FROM           468  '468'

 L. 255       586  LOAD_GLOBAL              warnings
              588  LOAD_METHOD              warn
              590  LOAD_STR                 'forkserver: waitpid returned unexpected pid %d'

 L. 256       592  LOAD_FAST                'pid'

 L. 255       594  BINARY_MODULO    
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          
          600_602  JUMP_BACK           384  'to 384'
            604_0  COME_FROM           368  '368'

 L. 258       604  LOAD_FAST                'listener'
              606  LOAD_FAST                'rfds'
              608  COMPARE_OP               in
          610_612  POP_JUMP_IF_FALSE   934  'to 934'

 L. 260       614  LOAD_FAST                'listener'
              616  LOAD_METHOD              accept
              618  CALL_METHOD_0         0  ''
              620  LOAD_CONST               0
              622  BINARY_SUBSCR    
          624_626  SETUP_WITH          928  'to 928'
              628  STORE_FAST               's'

 L. 262       630  LOAD_GLOBAL              reduction
              632  LOAD_METHOD              recvfds
              634  LOAD_FAST                's'
              636  LOAD_GLOBAL              MAXFDS_TO_SEND
              638  LOAD_CONST               1
              640  BINARY_ADD       
              642  CALL_METHOD_2         2  ''
              644  STORE_FAST               'fds'

 L. 263       646  LOAD_GLOBAL              len
              648  LOAD_FAST                'fds'
              650  CALL_FUNCTION_1       1  ''
              652  LOAD_GLOBAL              MAXFDS_TO_SEND
              654  COMPARE_OP               >
          656_658  POP_JUMP_IF_FALSE   678  'to 678'

 L. 264       660  LOAD_GLOBAL              RuntimeError

 L. 265       662  LOAD_STR                 'Too many ({0:n}) fds to send'
              664  LOAD_METHOD              format

 L. 266       666  LOAD_GLOBAL              len
              668  LOAD_FAST                'fds'
              670  CALL_FUNCTION_1       1  ''

 L. 265       672  CALL_METHOD_1         1  ''

 L. 264       674  CALL_FUNCTION_1       1  ''
              676  RAISE_VARARGS_1       1  'exception instance'
            678_0  COME_FROM           656  '656'

 L. 267       678  LOAD_FAST                'fds'
              680  UNPACK_EX_2+0           
              682  STORE_FAST               'child_r'
              684  STORE_FAST               'child_w'
              686  STORE_FAST               'fds'

 L. 268       688  LOAD_FAST                's'
              690  LOAD_METHOD              close
              692  CALL_METHOD_0         0  ''
              694  POP_TOP          

 L. 269       696  LOAD_GLOBAL              os
              698  LOAD_METHOD              fork
              700  CALL_METHOD_0         0  ''
              702  STORE_FAST               'pid'

 L. 270       704  LOAD_FAST                'pid'
              706  LOAD_CONST               0
              708  COMPARE_OP               ==
          710_712  POP_JUMP_IF_FALSE   846  'to 846'

 L. 272       714  LOAD_CONST               1
              716  STORE_FAST               'code'

 L. 273       718  SETUP_FINALLY       832  'to 832'
              720  SETUP_FINALLY       782  'to 782'

 L. 274       722  LOAD_FAST                'listener'
              724  LOAD_METHOD              close
              726  CALL_METHOD_0         0  ''
              728  POP_TOP          

 L. 275       730  LOAD_FAST                'selector'
              732  LOAD_METHOD              close
              734  CALL_METHOD_0         0  ''
              736  POP_TOP          

 L. 276       738  LOAD_FAST                'alive_r'
              740  LOAD_FAST                'child_w'
              742  LOAD_FAST                'sig_r'
              744  LOAD_FAST                'sig_w'
              746  BUILD_LIST_4          4 
              748  STORE_FAST               'unused_fds'

 L. 277       750  LOAD_FAST                'unused_fds'
              752  LOAD_METHOD              extend
              754  LOAD_FAST                'pid_to_fd'
              756  LOAD_METHOD              values
              758  CALL_METHOD_0         0  ''
              760  CALL_METHOD_1         1  ''
              762  POP_TOP          

 L. 278       764  LOAD_GLOBAL              _serve_one
              766  LOAD_FAST                'child_r'
              768  LOAD_FAST                'fds'

 L. 279       770  LOAD_FAST                'unused_fds'

 L. 280       772  LOAD_FAST                'old_handlers'

 L. 278       774  CALL_FUNCTION_4       4  ''
              776  STORE_FAST               'code'
              778  POP_BLOCK        
              780  JUMP_FORWARD        828  'to 828'
            782_0  COME_FROM_FINALLY   720  '720'

 L. 281       782  DUP_TOP          
              784  LOAD_GLOBAL              Exception
              786  COMPARE_OP               exception-match
          788_790  POP_JUMP_IF_FALSE   826  'to 826'
              792  POP_TOP          
              794  POP_TOP          
              796  POP_TOP          

 L. 282       798  LOAD_GLOBAL              sys
              800  LOAD_ATTR                excepthook
              802  LOAD_GLOBAL              sys
              804  LOAD_METHOD              exc_info
              806  CALL_METHOD_0         0  ''
              808  CALL_FUNCTION_EX      0  'positional arguments only'
              810  POP_TOP          

 L. 283       812  LOAD_GLOBAL              sys
              814  LOAD_ATTR                stderr
              816  LOAD_METHOD              flush
              818  CALL_METHOD_0         0  ''
              820  POP_TOP          
              822  POP_EXCEPT       
              824  JUMP_FORWARD        828  'to 828'
            826_0  COME_FROM           788  '788'
              826  END_FINALLY      
            828_0  COME_FROM           824  '824'
            828_1  COME_FROM           780  '780'
              828  POP_BLOCK        
              830  BEGIN_FINALLY    
            832_0  COME_FROM_FINALLY   718  '718'

 L. 285       832  LOAD_GLOBAL              os
              834  LOAD_METHOD              _exit
              836  LOAD_FAST                'code'
              838  CALL_METHOD_1         1  ''
              840  POP_TOP          
              842  END_FINALLY      
              844  JUMP_FORWARD        924  'to 924'
            846_0  COME_FROM           710  '710'

 L. 288       846  SETUP_FINALLY       862  'to 862'

 L. 289       848  LOAD_GLOBAL              write_signed
              850  LOAD_FAST                'child_w'
              852  LOAD_FAST                'pid'
              854  CALL_FUNCTION_2       2  ''
              856  POP_TOP          
              858  POP_BLOCK        
              860  JUMP_FORWARD        884  'to 884'
            862_0  COME_FROM_FINALLY   846  '846'

 L. 290       862  DUP_TOP          
              864  LOAD_GLOBAL              BrokenPipeError
              866  COMPARE_OP               exception-match
          868_870  POP_JUMP_IF_FALSE   882  'to 882'
              872  POP_TOP          
              874  POP_TOP          
              876  POP_TOP          

 L. 292       878  POP_EXCEPT       
              880  JUMP_FORWARD        884  'to 884'
            882_0  COME_FROM           868  '868'
              882  END_FINALLY      
            884_0  COME_FROM           880  '880'
            884_1  COME_FROM           860  '860'

 L. 293       884  LOAD_FAST                'child_w'
              886  LOAD_FAST                'pid_to_fd'
              888  LOAD_FAST                'pid'
              890  STORE_SUBSCR     

 L. 294       892  LOAD_GLOBAL              os
              894  LOAD_METHOD              close
              896  LOAD_FAST                'child_r'
              898  CALL_METHOD_1         1  ''
              900  POP_TOP          

 L. 295       902  LOAD_FAST                'fds'
              904  GET_ITER         
              906  FOR_ITER            924  'to 924'
              908  STORE_FAST               'fd'

 L. 296       910  LOAD_GLOBAL              os
              912  LOAD_METHOD              close
              914  LOAD_FAST                'fd'
              916  CALL_METHOD_1         1  ''
              918  POP_TOP          
          920_922  JUMP_BACK           906  'to 906'
            924_0  COME_FROM           844  '844'
              924  POP_BLOCK        
              926  BEGIN_FINALLY    
            928_0  COME_FROM_WITH      624  '624'
              928  WITH_CLEANUP_START
              930  WITH_CLEANUP_FINISH
              932  END_FINALLY      
            934_0  COME_FROM           610  '610'
              934  POP_BLOCK        
              936  JUMP_BACK           286  'to 286'
            938_0  COME_FROM_FINALLY   286  '286'

 L. 298       938  DUP_TOP          
              940  LOAD_GLOBAL              OSError
              942  COMPARE_OP               exception-match
          944_946  POP_JUMP_IF_FALSE   988  'to 988'
              948  POP_TOP          
              950  STORE_FAST               'e'
              952  POP_TOP          
              954  SETUP_FINALLY       976  'to 976'

 L. 299       956  LOAD_FAST                'e'
              958  LOAD_ATTR                errno
              960  LOAD_GLOBAL              errno
              962  LOAD_ATTR                ECONNABORTED
              964  COMPARE_OP               !=
          966_968  POP_JUMP_IF_FALSE   972  'to 972'

 L. 300       970  RAISE_VARARGS_0       0  'reraise'
            972_0  COME_FROM           966  '966'
              972  POP_BLOCK        
              974  BEGIN_FINALLY    
            976_0  COME_FROM_FINALLY   954  '954'
              976  LOAD_CONST               None
              978  STORE_FAST               'e'
              980  DELETE_FAST              'e'
              982  END_FINALLY      
              984  POP_EXCEPT       
              986  JUMP_BACK           286  'to 286'
            988_0  COME_FROM           944  '944'
              988  END_FINALLY      
          990_992  JUMP_BACK           286  'to 286'
              994  POP_BLOCK        
              996  BEGIN_FINALLY    
            998_0  COME_FROM_WITH      228  '228'
              998  WITH_CLEANUP_START
             1000  WITH_CLEANUP_FINISH
             1002  END_FINALLY      
             1004  POP_BLOCK        
             1006  BEGIN_FINALLY    
           1008_0  COME_FROM_WITH      216  '216'
             1008  WITH_CLEANUP_START
             1010  WITH_CLEANUP_FINISH
             1012  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 430


def _serve_one(child_r, fds, unused_fds, handlers):
    signal.set_wakeup_fd(-1)
    for sig, val in handlers.items():
        signal.signal(sig, val)
    else:
        for fd in unused_fds:
            os.close(fd)
        else:
            _forkserver._forkserver_alive_fd, resource_tracker._resource_tracker._fd, *_forkserver._inherited_fds = fds
            parent_sentinel = os.dup(child_r)
            code = spawn._main(child_r, parent_sentinel)
            return code


def read_signed(fd):
    data = b''
    length = SIGNED_STRUCT.size
    while len(data) < length:
        s = os.read(fd, length - len(data))
        if not s:
            raise EOFError('unexpected EOF')
        data += s

    return SIGNED_STRUCT.unpack(data)[0]


def write_signed(fd, n):
    msg = SIGNED_STRUCT.pack(n)
    while msg:
        nbytes = os.write(fd, msg)
        if nbytes == 0:
            raise RuntimeError('should not get here')
        msg = msg[nbytes:]


_forkserver = ForkServer()
ensure_running = _forkserver.ensure_running
get_inherited_fds = _forkserver.get_inherited_fds
connect_to_new_process = _forkserver.connect_to_new_process
set_forkserver_preload = _forkserver.set_forkserver_preload