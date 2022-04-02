# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
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
    __doc__ = 'Manager for resouces using background thread.'

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

                self._cache.clear()

    def _afterfork(self):
        for key, (send, close) in self._cache.items():
            close()

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
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 139        10  LOAD_GLOBAL              signal
               12  LOAD_METHOD              pthread_sigmask
               14  LOAD_GLOBAL              signal
               16  LOAD_ATTR                SIG_BLOCK
               18  LOAD_GLOBAL              range
               20  LOAD_CONST               1
               22  LOAD_GLOBAL              signal
               24  LOAD_ATTR                NSIG
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  CALL_METHOD_2         2  '2 positional arguments'
               30  POP_TOP          
             32_0  COME_FROM             8  '8'

 L. 140        32  SETUP_LOOP          166  'to 166'
             34_0  COME_FROM           162  '162'
             34_1  COME_FROM           158  '158'
             34_2  COME_FROM           126  '126'

 L. 141        34  SETUP_EXCEPT        128  'to 128'

 L. 142        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _listener
               40  LOAD_METHOD              accept
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  SETUP_WITH          118  'to 118'
               46  STORE_FAST               'conn'

 L. 143        48  LOAD_FAST                'conn'
               50  LOAD_METHOD              recv
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  STORE_FAST               'msg'

 L. 144        56  LOAD_FAST                'msg'
               58  LOAD_CONST               None
               60  COMPARE_OP               is
               62  POP_JUMP_IF_FALSE    66  'to 66'

 L. 145        64  BREAK_LOOP       
             66_0  COME_FROM            62  '62'

 L. 146        66  LOAD_FAST                'msg'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'key'
               72  STORE_FAST               'destination_pid'

 L. 147        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _cache
               78  LOAD_METHOD              pop
               80  LOAD_FAST                'key'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'send'
               88  STORE_FAST               'close'

 L. 148        90  SETUP_FINALLY       106  'to 106'

 L. 149        92  LOAD_FAST                'send'
               94  LOAD_FAST                'conn'
               96  LOAD_FAST                'destination_pid'
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  POP_TOP          
              102  POP_BLOCK        
              104  LOAD_CONST               None
            106_0  COME_FROM_FINALLY    90  '90'

 L. 151       106  LOAD_FAST                'close'
              108  CALL_FUNCTION_0       0  '0 positional arguments'
              110  POP_TOP          
              112  END_FINALLY      
              114  POP_BLOCK        
              116  LOAD_CONST               None
            118_0  COME_FROM_WITH       44  '44'
              118  WITH_CLEANUP_START
              120  WITH_CLEANUP_FINISH
              122  END_FINALLY      
              124  POP_BLOCK        
              126  JUMP_BACK            34  'to 34'
            128_0  COME_FROM_EXCEPT     34  '34'

 L. 152       128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 153       134  LOAD_GLOBAL              util
              136  LOAD_METHOD              is_exiting
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  POP_JUMP_IF_TRUE    156  'to 156'

 L. 154       142  LOAD_GLOBAL              sys
              144  LOAD_ATTR                excepthook
              146  LOAD_GLOBAL              sys
              148  LOAD_METHOD              exc_info
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  CALL_FUNCTION_EX      0  'positional arguments only'
              154  POP_TOP          
            156_0  COME_FROM           140  '140'
              156  POP_EXCEPT       
              158  JUMP_BACK            34  'to 34'
              160  END_FINALLY      
              162  JUMP_BACK            34  'to 34'
              164  POP_BLOCK        
            166_0  COME_FROM_LOOP       32  '32'

Parse error at or near `BREAK_LOOP' instruction at offset 64


_resource_sharer = _ResourceSharer()
stop = _resource_sharer.stop