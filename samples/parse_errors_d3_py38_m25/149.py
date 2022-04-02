# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\resource_sharer.py
import os, signal, socket, sys, threading
from . import process
from .context import reduction
from . import util
__all__ = [
 'stop']
if sys.platform == 'win32':
    __all__ += ['DupSocket']

    class DupSocket(object):
        __doc__ = 'Picklable wrapper for a socket.'

        def __init__(self, sock):
            new_sock = sock.dup()

            def send(conn, pid):
                share = new_sock.share(pid)
                conn.send_bytes(share)

            self._id = _resource_sharer.register(send, new_sock.close)

        def detach(self):
            """Get the socket.  This should only be called once."""
            with _resource_sharer.get_connection(self._id) as conn:
                share = conn.recv_bytes()
                return socket.fromshare(share)


else:
    __all__ += ['DupFd']

    class DupFd(object):
        __doc__ = 'Wrapper for fd which can be used at any time.'

        def __init__(self, fd):
            new_fd = os.dup(fd)

            def send(conn, pid):
                reduction.send_handle(conn, new_fd, pid)

            def close():
                os.close(new_fd)

            self._id = _resource_sharer.register(send, close)

        def detach(self):
            """Get the fd.  This should only be called once."""
            with _resource_sharer.get_connection(self._id) as conn:
                return reduction.recv_handle(conn)


class _ResourceSharer(object):
    __doc__ = 'Manager for resources using background thread.'

    def __init__(self):
        self._key = 0
        self._cache = {}
        self._old_locks = []
        self._lock = threading.Lock()
        self._listener = None
        self._address = None
        self._thread = None
        util.register_after_fork(self, _ResourceSharer._afterfork)

    def register(self, send, close):
        """Register resource, returning an identifier."""
        with self._lock:
            if self._address is None:
                self._start()
            self._key += 1
            self._cache[self._key] = (send, close)
            return (
             self._address, self._key)

    @staticmethod
    def get_connection(ident):
        """Return connection from which to receive identified resource."""
        from .connection import Client
        address, key = ident
        c = Client(address, authkey=(process.current_process().authkey))
        c.send((key, os.getpid()))
        return c

    def stop(self, timeout=None):
        """Stop the background thread and clear registered resources."""
        from .connection import Client
        with self._lock:
            if self._address is not None:
                c = Client((self._address), authkey=(process.current_process().authkey))
                c.send(None)
                c.close()
                self._thread.join(timeout)
                if self._thread.is_alive():
                    util.sub_warning('_ResourceSharer thread did not stop when asked')
                self._listener.close()
                self._thread = None
                self._address = None
                self._listener = None
                for key, (send, close) in self._cache.items():
                    close()
                else:
                    self._cache.clear()

    def _afterfork(self):
        for key, (send, close) in self._cache.items():
            close()
        else:
            self._cache.clear()
            self._old_locks.append(self._lock)
            self._lock = threading.Lock()
            if self._listener is not None:
                self._listener.close()
            self._listener = None
            self._address = None
            self._thread = None

    def _start(self):
        from .connection import Listener
        assert self._listener is None, 'Already have Listener'
        util.debug('starting listener and thread for sending handles')
        self._listener = Listener(authkey=(process.current_process().authkey))
        self._address = self._listener.address
        t = threading.Thread(target=(self._serve))
        t.daemon = True
        t.start()
        self._thread = t

    def _serve--- This code section failed: ---

 L. 138         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              signal
                4  LOAD_STR                 'pthread_sigmask'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 139        10  LOAD_GLOBAL              signal
               12  LOAD_METHOD              pthread_sigmask
               14  LOAD_GLOBAL              signal
               16  LOAD_ATTR                SIG_BLOCK
               18  LOAD_GLOBAL              signal
               20  LOAD_METHOD              valid_signals
               22  CALL_METHOD_0         0  ''
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          
             28_0  COME_FROM           168  '168'
             28_1  COME_FROM           164  '164'
             28_2  COME_FROM           132  '132'
             28_3  COME_FROM             8  '8'

 L. 141        28  SETUP_FINALLY       134  'to 134'

 L. 142        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _listener
               34  LOAD_METHOD              accept
               36  CALL_METHOD_0         0  ''
               38  SETUP_WITH          124  'to 124'
               40  STORE_FAST               'conn'

 L. 143        42  LOAD_FAST                'conn'
               44  LOAD_METHOD              recv
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'msg'

 L. 144        50  LOAD_FAST                'msg'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    72  'to 72'

 L. 145        58  POP_BLOCK        
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  POP_BLOCK        
               70  JUMP_FORWARD        170  'to 170'
             72_0  COME_FROM            56  '56'

 L. 146        72  LOAD_FAST                'msg'
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'key'
               78  STORE_FAST               'destination_pid'

 L. 147        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _cache
               84  LOAD_METHOD              pop
               86  LOAD_FAST                'key'
               88  CALL_METHOD_1         1  ''
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'send'
               94  STORE_FAST               'close'

 L. 148        96  SETUP_FINALLY       112  'to 112'

 L. 149        98  LOAD_FAST                'send'
              100  LOAD_FAST                'conn'
              102  LOAD_FAST                'destination_pid'
              104  CALL_FUNCTION_2       2  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  BEGIN_FINALLY    
            112_0  COME_FROM_FINALLY    96  '96'

 L. 151       112  LOAD_FAST                'close'
              114  CALL_FUNCTION_0       0  ''
              116  POP_TOP          
              118  END_FINALLY      
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM_WITH       38  '38'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      
              130  POP_BLOCK        
              132  JUMP_BACK            28  'to 28'
            134_0  COME_FROM_FINALLY    28  '28'

 L. 152       134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 153       140  LOAD_GLOBAL              util
              142  LOAD_METHOD              is_exiting
              144  CALL_METHOD_0         0  ''
              146  POP_JUMP_IF_TRUE    162  'to 162'

 L. 154       148  LOAD_GLOBAL              sys
              150  LOAD_ATTR                excepthook
              152  LOAD_GLOBAL              sys
              154  LOAD_METHOD              exc_info
              156  CALL_METHOD_0         0  ''
              158  CALL_FUNCTION_EX      0  'positional arguments only'
              160  POP_TOP          
            162_0  COME_FROM           146  '146'
              162  POP_EXCEPT       
              164  JUMP_BACK            28  'to 28'
              166  END_FINALLY      
              168  JUMP_BACK            28  'to 28'
            170_0  COME_FROM            70  '70'

Parse error at or near `BEGIN_FINALLY' instruction at offset 60


_resource_sharer = _ResourceSharer()
stop = _resource_sharer.stop