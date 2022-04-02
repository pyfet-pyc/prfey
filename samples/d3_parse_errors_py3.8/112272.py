# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\resource_tracker.py
import os, signal, sys, threading, warnings
from . import spawn
from . import util
__all__ = [
 'ensure_running', 'register', 'unregister']
_HAVE_SIGMASK = hasattr(signal, 'pthread_sigmask')
_IGNORED_SIGNALS = (signal.SIGINT, signal.SIGTERM)
_CLEANUP_FUNCS = {'noop': lambda: None}
if os.name == 'posix':
    import _multiprocessing, _posixshmem
    _CLEANUP_FUNCS.update({'semaphore':_multiprocessing.sem_unlink, 
     'shared_memory':_posixshmem.shm_unlink})

class ResourceTracker(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._fd = None
        self._pid = None

    def getfd(self):
        self.ensure_running()
        return self._fd

    def ensure_running--- This code section failed: ---

 L.  62         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
              4_6  SETUP_WITH          362  'to 362'
                8  POP_TOP          

 L.  63        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _fd
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE   126  'to 126'

 L.  65        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _check_alive
               24  CALL_METHOD_0         0  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.  67        28  POP_BLOCK        
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'

 L.  69        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              close
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _fd
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  72        54  SETUP_FINALLY        84  'to 84'

 L.  75        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pid
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L.  76        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              waitpid
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _pid
               74  LOAD_CONST               0
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          
             80_0  COME_FROM            64  '64'
               80  POP_BLOCK        
               82  JUMP_FORWARD        104  'to 104'
             84_0  COME_FROM_FINALLY    54  '54'

 L.  77        84  DUP_TOP          
               86  LOAD_GLOBAL              ChildProcessError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  79        98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            90  '90'
              102  END_FINALLY      
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            82  '82'

 L.  80       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _fd

 L.  81       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _pid

 L.  83       116  LOAD_GLOBAL              warnings
              118  LOAD_METHOD              warn
              120  LOAD_STR                 'resource_tracker: process died unexpectedly, relaunching.  Some resources might leak.'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM            18  '18'

 L.  86       126  BUILD_LIST_0          0 
              128  STORE_FAST               'fds_to_pass'

 L.  87       130  SETUP_FINALLY       152  'to 152'

 L.  88       132  LOAD_FAST                'fds_to_pass'
              134  LOAD_METHOD              append
              136  LOAD_GLOBAL              sys
              138  LOAD_ATTR                stderr
              140  LOAD_METHOD              fileno
              142  CALL_METHOD_0         0  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  POP_BLOCK        
              150  JUMP_FORWARD        172  'to 172'
            152_0  COME_FROM_FINALLY   130  '130'

 L.  89       152  DUP_TOP          
              154  LOAD_GLOBAL              Exception
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L.  90       166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           158  '158'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           150  '150'

 L.  91       172  LOAD_STR                 'from multiprocessing.resource_tracker import main;main(%d)'
              174  STORE_FAST               'cmd'

 L.  92       176  LOAD_GLOBAL              os
              178  LOAD_METHOD              pipe
              180  CALL_METHOD_0         0  ''
              182  UNPACK_SEQUENCE_2     2 
              184  STORE_FAST               'r'
              186  STORE_FAST               'w'

 L.  93       188  SETUP_FINALLY       346  'to 346'
              190  SETUP_FINALLY       306  'to 306'

 L.  94       192  LOAD_FAST                'fds_to_pass'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'r'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L.  96       202  LOAD_GLOBAL              spawn
              204  LOAD_METHOD              get_executable
              206  CALL_METHOD_0         0  ''
              208  STORE_FAST               'exe'

 L.  97       210  LOAD_FAST                'exe'
              212  BUILD_LIST_1          1 
              214  LOAD_GLOBAL              util
              216  LOAD_METHOD              _args_from_interpreter_flags
              218  CALL_METHOD_0         0  ''
              220  BINARY_ADD       
              222  STORE_FAST               'args'

 L.  98       224  LOAD_FAST                'args'
              226  LOAD_STR                 '-c'
              228  LOAD_FAST                'cmd'
              230  LOAD_FAST                'r'
              232  BINARY_MODULO    
              234  BUILD_LIST_2          2 
              236  INPLACE_ADD      
              238  STORE_FAST               'args'

 L. 105       240  SETUP_FINALLY       280  'to 280'

 L. 106       242  LOAD_GLOBAL              _HAVE_SIGMASK
          244_246  POP_JUMP_IF_FALSE   262  'to 262'

 L. 107       248  LOAD_GLOBAL              signal
              250  LOAD_METHOD              pthread_sigmask
              252  LOAD_GLOBAL              signal
              254  LOAD_ATTR                SIG_BLOCK
              256  LOAD_GLOBAL              _IGNORED_SIGNALS
              258  CALL_METHOD_2         2  ''
              260  POP_TOP          
            262_0  COME_FROM           244  '244'

 L. 108       262  LOAD_GLOBAL              util
              264  LOAD_METHOD              spawnv_passfds
              266  LOAD_FAST                'exe'
              268  LOAD_FAST                'args'
              270  LOAD_FAST                'fds_to_pass'
              272  CALL_METHOD_3         3  ''
              274  STORE_FAST               'pid'
              276  POP_BLOCK        
              278  BEGIN_FINALLY    
            280_0  COME_FROM_FINALLY   240  '240'

 L. 110       280  LOAD_GLOBAL              _HAVE_SIGMASK
          282_284  POP_JUMP_IF_FALSE   300  'to 300'

 L. 111       286  LOAD_GLOBAL              signal
              288  LOAD_METHOD              pthread_sigmask
              290  LOAD_GLOBAL              signal
              292  LOAD_ATTR                SIG_UNBLOCK
              294  LOAD_GLOBAL              _IGNORED_SIGNALS
              296  CALL_METHOD_2         2  ''
              298  POP_TOP          
            300_0  COME_FROM           282  '282'
              300  END_FINALLY      
              302  POP_BLOCK        
              304  JUMP_FORWARD        330  'to 330'
            306_0  COME_FROM_FINALLY   190  '190'

 L. 112       306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 113       312  LOAD_GLOBAL              os
              314  LOAD_METHOD              close
              316  LOAD_FAST                'w'
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 114       322  RAISE_VARARGS_0       0  'reraise'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        342  'to 342'
              328  END_FINALLY      
            330_0  COME_FROM           304  '304'

 L. 116       330  LOAD_FAST                'w'
              332  LOAD_FAST                'self'
              334  STORE_ATTR               _fd

 L. 117       336  LOAD_FAST                'pid'
              338  LOAD_FAST                'self'
              340  STORE_ATTR               _pid
            342_0  COME_FROM           326  '326'
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM_FINALLY   188  '188'

 L. 119       346  LOAD_GLOBAL              os
              348  LOAD_METHOD              close
              350  LOAD_FAST                'r'
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
              356  END_FINALLY      
              358  POP_BLOCK        
              360  BEGIN_FINALLY    
            362_0  COME_FROM_WITH        4  '4'
              362  WITH_CLEANUP_START
              364  WITH_CLEANUP_FINISH
              366  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30

    def _check_alive(self):
        """Check that the pipe has not been closed by sending a probe."""
        try:
            os.writeself._fdb'PROBE:0:noop\n'
        except OSError:
            return False
        else:
            return True

    def register(self, name, rtype):
        """Register name of resource with resource tracker."""
        self._send'REGISTER'namertype

    def unregister(self, name, rtype):
        """Unregister name of resource with resource tracker."""
        self._send'UNREGISTER'namertype

    def _send(self, cmd, name, rtype):
        self.ensure_running()
        msg = '{0}:{1}:{2}\n'.formatcmdnamertype.encode('ascii')
        if len(name) > 512:
            raise ValueError('name too long')
        nbytes = os.writeself._fdmsg
        assert nbytes == len(msg), 'nbytes {0:n} but len(msg) {1:n}'.formatnbyteslen(msg)


_resource_tracker = ResourceTracker()
ensure_running = _resource_tracker.ensure_running
register = _resource_tracker.register
unregister = _resource_tracker.unregister
getfd = _resource_tracker.getfd

def main--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              signal
                2  LOAD_METHOD              signal
                4  LOAD_GLOBAL              signal
                6  LOAD_ATTR                SIGINT
                8  LOAD_GLOBAL              signal
               10  LOAD_ATTR                SIG_IGN
               12  CALL_METHOD_2         2  ''
               14  POP_TOP          

 L. 162        16  LOAD_GLOBAL              signal
               18  LOAD_METHOD              signal
               20  LOAD_GLOBAL              signal
               22  LOAD_ATTR                SIGTERM
               24  LOAD_GLOBAL              signal
               26  LOAD_ATTR                SIG_IGN
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L. 163        32  LOAD_GLOBAL              _HAVE_SIGMASK
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L. 164        36  LOAD_GLOBAL              signal
               38  LOAD_METHOD              pthread_sigmask
               40  LOAD_GLOBAL              signal
               42  LOAD_ATTR                SIG_UNBLOCK
               44  LOAD_GLOBAL              _IGNORED_SIGNALS
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          
             50_0  COME_FROM            34  '34'

 L. 166        50  LOAD_GLOBAL              sys
               52  LOAD_ATTR                stdin
               54  LOAD_GLOBAL              sys
               56  LOAD_ATTR                stdout
               58  BUILD_TUPLE_2         2 
               60  GET_ITER         
             62_0  COME_FROM           100  '100'
             62_1  COME_FROM            96  '96'
             62_2  COME_FROM            78  '78'
               62  FOR_ITER            102  'to 102'
               64  STORE_FAST               'f'

 L. 167        66  SETUP_FINALLY        80  'to 80'

 L. 168        68  LOAD_FAST                'f'
               70  LOAD_METHOD              close
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  JUMP_BACK            62  'to 62'
             80_0  COME_FROM_FINALLY    66  '66'

 L. 169        80  DUP_TOP          
               82  LOAD_GLOBAL              Exception
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE    98  'to 98'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 170        94  POP_EXCEPT       
               96  JUMP_BACK            62  'to 62'
             98_0  COME_FROM            86  '86'
               98  END_FINALLY      
              100  JUMP_BACK            62  'to 62'
            102_0  COME_FROM            62  '62'

 L. 172       102  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              104  LOAD_STR                 'main.<locals>.<dictcomp>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  LOAD_GLOBAL              _CLEANUP_FUNCS
              110  LOAD_METHOD              keys
              112  CALL_METHOD_0         0  ''
              114  GET_ITER         
              116  CALL_FUNCTION_1       1  ''
              118  STORE_FAST               'cache'

 L. 173       120  SETUP_FINALLY       358  'to 358'

 L. 175       122  LOAD_GLOBAL              open
              124  LOAD_FAST                'fd'
              126  LOAD_STR                 'rb'
              128  CALL_FUNCTION_2       2  ''
              130  SETUP_WITH          348  'to 348'
              132  STORE_FAST               'f'

 L. 176       134  LOAD_FAST                'f'
              136  GET_ITER         
            138_0  COME_FROM           342  '342'
            138_1  COME_FROM           338  '338'
            138_2  COME_FROM           286  '286'
              138  FOR_ITER            344  'to 344'
              140  STORE_FAST               'line'

 L. 177       142  SETUP_FINALLY       288  'to 288'

 L. 178       144  LOAD_FAST                'line'
              146  LOAD_METHOD              strip
              148  CALL_METHOD_0         0  ''
              150  LOAD_METHOD              decode
              152  LOAD_STR                 'ascii'
              154  CALL_METHOD_1         1  ''
              156  LOAD_METHOD              split
              158  LOAD_STR                 ':'
              160  CALL_METHOD_1         1  ''
              162  UNPACK_SEQUENCE_3     3 
              164  STORE_FAST               'cmd'
              166  STORE_FAST               'name'
              168  STORE_FAST               'rtype'

 L. 179       170  LOAD_GLOBAL              _CLEANUP_FUNCS
              172  LOAD_METHOD              get
              174  LOAD_FAST                'rtype'
              176  LOAD_CONST               None
              178  CALL_METHOD_2         2  ''
              180  STORE_FAST               'cleanup_func'

 L. 180       182  LOAD_FAST                'cleanup_func'
              184  LOAD_CONST               None
              186  COMPARE_OP               is
              188  POP_JUMP_IF_FALSE   210  'to 210'

 L. 181       190  LOAD_GLOBAL              ValueError

 L. 182       192  LOAD_STR                 'Cannot register '
              194  LOAD_FAST                'name'
              196  FORMAT_VALUE          0  ''
              198  LOAD_STR                 ' for automatic cleanup: unknown resource type '
              200  LOAD_FAST                'rtype'
              202  FORMAT_VALUE          0  ''
              204  BUILD_STRING_4        4 

 L. 181       206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           188  '188'

 L. 185       210  LOAD_FAST                'cmd'
              212  LOAD_STR                 'REGISTER'
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   234  'to 234'

 L. 186       218  LOAD_FAST                'cache'
              220  LOAD_FAST                'rtype'
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              add
              226  LOAD_FAST                'name'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  JUMP_FORWARD        284  'to 284'
            234_0  COME_FROM           216  '216'

 L. 187       234  LOAD_FAST                'cmd'
              236  LOAD_STR                 'UNREGISTER'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   260  'to 260'

 L. 188       244  LOAD_FAST                'cache'
              246  LOAD_FAST                'rtype'
              248  BINARY_SUBSCR    
              250  LOAD_METHOD              remove
              252  LOAD_FAST                'name'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_FORWARD        284  'to 284'
            260_0  COME_FROM           240  '240'

 L. 189       260  LOAD_FAST                'cmd'
              262  LOAD_STR                 'PROBE'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   272  'to 272'

 L. 190       270  JUMP_FORWARD        284  'to 284'
            272_0  COME_FROM           266  '266'

 L. 192       272  LOAD_GLOBAL              RuntimeError
              274  LOAD_STR                 'unrecognized command %r'
              276  LOAD_FAST                'cmd'
              278  BINARY_MODULO    
              280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
            284_0  COME_FROM           270  '270'
            284_1  COME_FROM           258  '258'
            284_2  COME_FROM           232  '232'
              284  POP_BLOCK        
              286  JUMP_BACK           138  'to 138'
            288_0  COME_FROM_FINALLY   142  '142'

 L. 193       288  DUP_TOP          
              290  LOAD_GLOBAL              Exception
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   340  'to 340'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L. 194       304  SETUP_FINALLY       324  'to 324'

 L. 195       306  LOAD_GLOBAL              sys
              308  LOAD_ATTR                excepthook
              310  LOAD_GLOBAL              sys
              312  LOAD_METHOD              exc_info
              314  CALL_METHOD_0         0  ''
              316  CALL_FUNCTION_EX      0  'positional arguments only'
              318  POP_TOP          
              320  POP_BLOCK        
              322  JUMP_FORWARD        336  'to 336'
            324_0  COME_FROM_FINALLY   304  '304'

 L. 196       324  POP_TOP          
              326  POP_TOP          
              328  POP_TOP          

 L. 197       330  POP_EXCEPT       
              332  BREAK_LOOP          336  'to 336'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           322  '322'
              336  POP_EXCEPT       
              338  JUMP_BACK           138  'to 138'
            340_0  COME_FROM           294  '294'
              340  END_FINALLY      
              342  JUMP_BACK           138  'to 138'
            344_0  COME_FROM           138  '138'
              344  POP_BLOCK        
              346  BEGIN_FINALLY    
            348_0  COME_FROM_WITH      130  '130'
              348  WITH_CLEANUP_START
              350  WITH_CLEANUP_FINISH
              352  END_FINALLY      
              354  POP_BLOCK        
              356  BEGIN_FINALLY    
            358_0  COME_FROM_FINALLY   120  '120'

 L. 200       358  LOAD_FAST                'cache'
              360  LOAD_METHOD              items
              362  CALL_METHOD_0         0  ''
              364  GET_ITER         
            366_0  COME_FROM           522  '522'
              366  FOR_ITER            526  'to 526'
              368  UNPACK_SEQUENCE_2     2 
              370  STORE_FAST               'rtype'
              372  STORE_FAST               'rtype_cache'

 L. 201       374  LOAD_FAST                'rtype_cache'
          376_378  POP_JUMP_IF_FALSE   430  'to 430'

 L. 202       380  SETUP_FINALLY       408  'to 408'

 L. 203       382  LOAD_GLOBAL              warnings
              384  LOAD_METHOD              warn
              386  LOAD_STR                 'resource_tracker: There appear to be %d leaked %s objects to clean up at shutdown'

 L. 205       388  LOAD_GLOBAL              len
              390  LOAD_FAST                'rtype_cache'
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_FAST                'rtype'
              396  BUILD_TUPLE_2         2 

 L. 203       398  BINARY_MODULO    
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
              404  POP_BLOCK        
              406  JUMP_FORWARD        430  'to 430'
            408_0  COME_FROM_FINALLY   380  '380'

 L. 206       408  DUP_TOP          
              410  LOAD_GLOBAL              Exception
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   428  'to 428'
              418  POP_TOP          
              420  POP_TOP          
              422  POP_TOP          

 L. 207       424  POP_EXCEPT       
              426  BREAK_LOOP          430  'to 430'
            428_0  COME_FROM           414  '414'
              428  END_FINALLY      
            430_0  COME_FROM           426  '426'
            430_1  COME_FROM           406  '406'
            430_2  COME_FROM           376  '376'

 L. 208       430  LOAD_FAST                'rtype_cache'
              432  GET_ITER         
            434_0  COME_FROM           518  '518'
              434  FOR_ITER            522  'to 522'
              436  STORE_FAST               'name'

 L. 212       438  SETUP_FINALLY       516  'to 516'

 L. 213       440  SETUP_FINALLY       458  'to 458'

 L. 214       442  LOAD_GLOBAL              _CLEANUP_FUNCS
              444  LOAD_FAST                'rtype'
              446  BINARY_SUBSCR    
              448  LOAD_FAST                'name'
              450  CALL_FUNCTION_1       1  ''
              452  POP_TOP          
              454  POP_BLOCK        
              456  JUMP_FORWARD        512  'to 512'
            458_0  COME_FROM_FINALLY   440  '440'

 L. 215       458  DUP_TOP          
              460  LOAD_GLOBAL              Exception
              462  COMPARE_OP               exception-match
          464_466  POP_JUMP_IF_FALSE   510  'to 510'
              468  POP_TOP          
              470  STORE_FAST               'e'
              472  POP_TOP          
              474  SETUP_FINALLY       498  'to 498'

 L. 216       476  LOAD_GLOBAL              warnings
              478  LOAD_METHOD              warn
              480  LOAD_STR                 'resource_tracker: %r: %s'
              482  LOAD_FAST                'name'
              484  LOAD_FAST                'e'
              486  BUILD_TUPLE_2         2 
              488  BINARY_MODULO    
              490  CALL_METHOD_1         1  ''
              492  POP_TOP          
              494  POP_BLOCK        
              496  BEGIN_FINALLY    
            498_0  COME_FROM_FINALLY   474  '474'
              498  LOAD_CONST               None
              500  STORE_FAST               'e'
              502  DELETE_FAST              'e'
              504  END_FINALLY      
              506  POP_EXCEPT       
              508  JUMP_FORWARD        512  'to 512'
            510_0  COME_FROM           464  '464'
              510  END_FINALLY      
            512_0  COME_FROM           508  '508'
            512_1  COME_FROM           456  '456'
              512  POP_BLOCK        
              514  BEGIN_FINALLY    
            516_0  COME_FROM_FINALLY   438  '438'

 L. 218       516  END_FINALLY      
          518_520  JUMP_BACK           434  'to 434'
            522_0  COME_FROM           434  '434'
          522_524  JUMP_BACK           366  'to 366'
            526_0  COME_FROM           366  '366'
              526  END_FINALLY      

Parse error at or near `END_FINALLY' instruction at offset 334