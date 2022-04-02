# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\resource_tracker.py
import os, signal, sys, threading, warnings
from . import spawn
from . import util
__all__ = [
 'ensure_running', 'register', 'unregister']
_HAVE_SIGMASK = hasattr(signal, 'pthread_sigmask')
_IGNORED_SIGNALS = (signal.SIGINT, signal.SIGTERM)
_CLEANUP_FUNCS = {'noop': lambda : None}
if os.name == 'posix':
    import _multiprocessing, _posixshmem
    _CLEANUP_FUNCS.update({'semaphore':_multiprocessing.sem_unlink, 
     'shared_memory':_posixshmem.shm_unlink})

class ResourceTracker(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._fd = None
        self._pid = None

    def _stop--- This code section failed: ---

 L.  54         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           74  'to 74'
                6  POP_TOP          

 L.  55         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _fd
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L.  57        18  POP_BLOCK        
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            16  '16'

 L.  60        32  LOAD_GLOBAL              os
               34  LOAD_METHOD              close
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _fd
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  61        44  LOAD_CONST               None
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _fd

 L.  63        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              waitpid
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _pid
               58  LOAD_CONST               0
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          

 L.  64        64  LOAD_CONST               None
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _pid
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
             74_0  COME_FROM_WITH        4  '4'
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 20

    def getfd(self):
        self.ensure_running()
        return self._fd

    def ensure_running--- This code section failed: ---

 L.  75         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
              4_6  SETUP_WITH          362  'to 362'
                8  POP_TOP          

 L.  76        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _fd
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE   126  'to 126'

 L.  78        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _check_alive
               24  CALL_METHOD_0         0  ''
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.  80        28  POP_BLOCK        
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'

 L.  82        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              close
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _fd
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  85        54  SETUP_FINALLY        84  'to 84'

 L.  88        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pid
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L.  89        66  LOAD_GLOBAL              os
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

 L.  90        84  DUP_TOP          
               86  LOAD_GLOBAL              ChildProcessError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  92        98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            90  '90'
              102  END_FINALLY      
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            82  '82'

 L.  93       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _fd

 L.  94       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _pid

 L.  96       116  LOAD_GLOBAL              warnings
              118  LOAD_METHOD              warn
              120  LOAD_STR                 'resource_tracker: process died unexpectedly, relaunching.  Some resources might leak.'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM            18  '18'

 L.  99       126  BUILD_LIST_0          0 
              128  STORE_FAST               'fds_to_pass'

 L. 100       130  SETUP_FINALLY       152  'to 152'

 L. 101       132  LOAD_FAST                'fds_to_pass'
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

 L. 102       152  DUP_TOP          
              154  LOAD_GLOBAL              Exception
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 103       166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           158  '158'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           150  '150'

 L. 104       172  LOAD_STR                 'from multiprocessing.resource_tracker import main;main(%d)'
              174  STORE_FAST               'cmd'

 L. 105       176  LOAD_GLOBAL              os
              178  LOAD_METHOD              pipe
              180  CALL_METHOD_0         0  ''
              182  UNPACK_SEQUENCE_2     2 
              184  STORE_FAST               'r'
              186  STORE_FAST               'w'

 L. 106       188  SETUP_FINALLY       346  'to 346'
              190  SETUP_FINALLY       306  'to 306'

 L. 107       192  LOAD_FAST                'fds_to_pass'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'r'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 109       202  LOAD_GLOBAL              spawn
              204  LOAD_METHOD              get_executable
              206  CALL_METHOD_0         0  ''
              208  STORE_FAST               'exe'

 L. 110       210  LOAD_FAST                'exe'
              212  BUILD_LIST_1          1 
              214  LOAD_GLOBAL              util
              216  LOAD_METHOD              _args_from_interpreter_flags
              218  CALL_METHOD_0         0  ''
              220  BINARY_ADD       
              222  STORE_FAST               'args'

 L. 111       224  LOAD_FAST                'args'
              226  LOAD_STR                 '-c'
              228  LOAD_FAST                'cmd'
              230  LOAD_FAST                'r'
              232  BINARY_MODULO    
              234  BUILD_LIST_2          2 
              236  INPLACE_ADD      
              238  STORE_FAST               'args'

 L. 118       240  SETUP_FINALLY       280  'to 280'

 L. 119       242  LOAD_GLOBAL              _HAVE_SIGMASK
          244_246  POP_JUMP_IF_FALSE   262  'to 262'

 L. 120       248  LOAD_GLOBAL              signal
              250  LOAD_METHOD              pthread_sigmask
              252  LOAD_GLOBAL              signal
              254  LOAD_ATTR                SIG_BLOCK
              256  LOAD_GLOBAL              _IGNORED_SIGNALS
              258  CALL_METHOD_2         2  ''
              260  POP_TOP          
            262_0  COME_FROM           244  '244'

 L. 121       262  LOAD_GLOBAL              util
              264  LOAD_METHOD              spawnv_passfds
              266  LOAD_FAST                'exe'
              268  LOAD_FAST                'args'
              270  LOAD_FAST                'fds_to_pass'
              272  CALL_METHOD_3         3  ''
              274  STORE_FAST               'pid'
              276  POP_BLOCK        
              278  BEGIN_FINALLY    
            280_0  COME_FROM_FINALLY   240  '240'

 L. 123       280  LOAD_GLOBAL              _HAVE_SIGMASK
          282_284  POP_JUMP_IF_FALSE   300  'to 300'

 L. 124       286  LOAD_GLOBAL              signal
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

 L. 125       306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 126       312  LOAD_GLOBAL              os
              314  LOAD_METHOD              close
              316  LOAD_FAST                'w'
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 127       322  RAISE_VARARGS_0       0  'reraise'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        342  'to 342'
              328  END_FINALLY      
            330_0  COME_FROM           304  '304'

 L. 129       330  LOAD_FAST                'w'
              332  LOAD_FAST                'self'
              334  STORE_ATTR               _fd

 L. 130       336  LOAD_FAST                'pid'
              338  LOAD_FAST                'self'
              340  STORE_ATTR               _pid
            342_0  COME_FROM           326  '326'
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM_FINALLY   188  '188'

 L. 132       346  LOAD_GLOBAL              os
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

def main(fd):
    """Run resource tracker."""
    signal.signalsignal.SIGINTsignal.SIG_IGN
    signal.signalsignal.SIGTERMsignal.SIG_IGN
    if _HAVE_SIGMASK:
        signal.pthread_sigmasksignal.SIG_UNBLOCK_IGNORED_SIGNALS
    for f in (sys.stdin, sys.stdout):
        try:
            f.close()
        except Exception:
            pass

    else:
        cache = {set():rtype for rtype in _CLEANUP_FUNCS.keys()}
        try:
            with open(fd, 'rb') as (f):
                for line in f:
                    try:
                        cmd, name, rtype = line.strip().decode('ascii').split(':')
                        cleanup_func = _CLEANUP_FUNCS.getrtypeNone
                        if cleanup_func is None:
                            raise ValueError(f"Cannot register {name} for automatic cleanup: unknown resource type {rtype}")
                        elif cmd == 'REGISTER':
                            cache[rtype].add(name)
                        else:
                            if cmd == 'UNREGISTER':
                                cache[rtype].remove(name)
                            else:
                                if cmd == 'PROBE':
                                    break
                                else:
                                    raise RuntimeError('unrecognized command %r' % cmd)
                    except Exception:
                        try:
                            (sys.excepthook)(*sys.exc_info())
                        except:
                            pass

        finally:
            for rtype, rtype_cache in cache.items():
                if rtype_cache:
                    try:
                        warnings.warn('resource_tracker: There appear to be %d leaked %s objects to clean up at shutdown' % (
                         len(rtype_cache), rtype))
                    except Exception:
                        pass

                for name in rtype_cache:
                    try:
                        try:
                            _CLEANUP_FUNCS[rtype](name)
                        except Exception as e:
                            try:
                                warnings.warn('resource_tracker: %r: %s' % (name, e))
                            finally:
                                e = None
                                del e

                    finally:
                        pass