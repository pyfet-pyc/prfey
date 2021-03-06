# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\reduction.py
from abc import ABCMeta
import copyreg, functools, io, os, pickle, socket, sys
from . import context
__all__ = [
 'send_handle', 'recv_handle', 'ForkingPickler', 'register', 'dump']
HAVE_SEND_HANDLE = sys.platform == 'win32' or hasattr(socket, 'CMSG_LEN') and hasattr(socket, 'SCM_RIGHTS') and hasattr(socket.socket, 'sendmsg')

class ForkingPickler(pickle.Pickler):
    __doc__ = 'Pickler subclass used by multiprocessing.'
    _extra_reducers = {}
    _copyreg_dispatch_table = copyreg.dispatch_table

    def __init__(self, *args):
        (super().__init__)(*args)
        self.dispatch_table = self._copyreg_dispatch_table.copy()
        self.dispatch_table.update(self._extra_reducers)

    @classmethod
    def register(cls, type, reduce):
        """Register a reduce function for a type."""
        cls._extra_reducers[type] = reduce

    @classmethod
    def dumps(cls, obj, protocol=None):
        buf = io.BytesIO()
        cls(buf, protocol).dump(obj)
        return buf.getbuffer()

    loads = pickle.loads


register = ForkingPickler.register

def dump(obj, file, protocol=None):
    """Replacement for pickle.dump() using ForkingPickler."""
    ForkingPickler(file, protocol).dump(obj)


if sys.platform == 'win32':
    __all__ += ['DupHandle', 'duplicate', 'steal_handle']
    import _winapi

    def duplicate(handle, target_process=None, inheritable=False, *, source_process=None):
        """Duplicate a handle.  (target_process is a handle not a pid!)"""
        current_process = _winapi.GetCurrentProcess()
        if source_process is None:
            source_process = current_process
        if target_process is None:
            target_process = current_process
        return _winapi.DuplicateHandle(source_process, handle, target_process, 0, inheritable, _winapi.DUPLICATE_SAME_ACCESS)


    def steal_handle(source_pid, handle):
        """Steal a handle from process identified by source_pid."""
        source_process_handle = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, source_pid)
        try:
            return _winapi.DuplicateHandle(source_process_handle, handle, _winapi.GetCurrentProcess(), 0, False, _winapi.DUPLICATE_SAME_ACCESS | _winapi.DUPLICATE_CLOSE_SOURCE)
        finally:
            _winapi.CloseHandle(source_process_handle)


    def send_handle(conn, handle, destination_pid):
        """Send a handle over a local connection."""
        dh = DupHandle(handle, _winapi.DUPLICATE_SAME_ACCESS, destination_pid)
        conn.send(dh)


    def recv_handle(conn):
        """Receive a handle over a local connection."""
        return conn.recv().detach()


    class DupHandle(object):
        __doc__ = 'Picklable wrapper for a handle.'

        def __init__(self, handle, access, pid=None):
            if pid is None:
                pid = os.getpid()
            proc = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, pid)
            try:
                self._handle = _winapi.DuplicateHandle(_winapi.GetCurrentProcess(), handle, proc, access, False, 0)
            finally:
                _winapi.CloseHandle(proc)

            self._access = access
            self._pid = pid

        def detach(self):
            """Get the handle.  This should only be called once."""
            if self._pid == os.getpid():
                return self._handle
            proc = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, self._pid)
            try:
                return _winapi.DuplicateHandle(proc, self._handle, _winapi.GetCurrentProcess(), self._access, False, _winapi.DUPLICATE_CLOSE_SOURCE)
            finally:
                _winapi.CloseHandle(proc)


else:
    __all__ += ['DupFd', 'sendfds', 'recvfds']
    import array
    ACKNOWLEDGE = sys.platform == 'darwin'

    def sendfds(sock, fds):
        """Send an array of fds over an AF_UNIX socket."""
        fds = array.array('i', fds)
        msg = bytes([len(fds) % 256])
        sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)])
        if ACKNOWLEDGE:
            if sock.recv(1) != b'A':
                raise RuntimeError('did not receive acknowledgement of fd')


    def recvfds(sock, size):
        """Receive an array of fds over an AF_UNIX socket."""
        a = array.array('i')
        bytes_size = a.itemsize * size
        msg, ancdata, flags, addr = sock.recvmsg(1, socket.CMSG_SPACE(bytes_size))
        if not msg:
            if not ancdata:
                raise EOFError
        try:
            if ACKNOWLEDGE:
                sock.send(b'A')
            else:
                if len(ancdata) != 1:
                    raise RuntimeError('received %d items of ancdata' % len(ancdata))
                cmsg_level, cmsg_type, cmsg_data = ancdata[0]
                if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                    if len(cmsg_data) % a.itemsize != 0:
                        raise ValueError
                    a.frombytes(cmsg_data)
                    if len(a) % 256 != msg[0]:
                        raise AssertionError('Len is {0:n} but msg[0] is {1!r}'.format(len(a), msg[0]))
                    return list(a)
        except (ValueError, IndexError):
            pass
        else:
            raise RuntimeError('Invalid data received')


    def send_handle(conn, handle, destination_pid):
        """Send a handle over a local connection."""
        with socket.fromfd(conn.fileno(), socket.AF_UNIX, socket.SOCK_STREAM) as (s):
            sendfds(s, [handle])


    def recv_handle--- This code section failed: ---

 L. 188         0  LOAD_GLOBAL              socket
                2  LOAD_METHOD              fromfd
                4  LOAD_FAST                'conn'
                6  LOAD_METHOD              fileno
                8  CALL_METHOD_0         0  ''
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                AF_UNIX
               14  LOAD_GLOBAL              socket
               16  LOAD_ATTR                SOCK_STREAM
               18  CALL_METHOD_3         3  ''
               20  SETUP_WITH           50  'to 50'
               22  STORE_FAST               's'

 L. 189        24  LOAD_GLOBAL              recvfds
               26  LOAD_FAST                's'
               28  LOAD_CONST               1
               30  CALL_FUNCTION_2       2  ''
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH       20  '20'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38


    def DupFd(fd):
        """Return a wrapper for an fd."""
        popen_obj = context.get_spawning_popen()
        if popen_obj is not None:
            return popen_obj.DupFd(popen_obj.duplicate_for_child(fd))
        if HAVE_SEND_HANDLE:
            from . import resource_sharer
            return resource_sharer.DupFd(fd)
        raise ValueError('SCM_RIGHTS appears not to be available')


def _reduce_method(m):
    if m.__self__ is None:
        return (
         getattr, (m.__class__, m.__func__.__name__))
    return (getattr, (m.__self__, m.__func__.__name__))


class _C:

    def f(self):
        pass


register(type(_C().f), _reduce_method)

def _reduce_method_descriptor(m):
    return (
     getattr, (m.__objclass__, m.__name__))


register(type(list.append), _reduce_method_descriptor)
register(type(int.__add__), _reduce_method_descriptor)

def _reduce_partial(p):
    return (
     _rebuild_partial, (p.func, p.args, p.keywords or {}))


def _rebuild_partial(func, args, keywords):
    return (functools.partial)(func, *args, **keywords)


register(functools.partial, _reduce_partial)
if sys.platform == 'win32':

    def _reduce_socket(s):
        from .resource_sharer import DupSocket
        return (
         _rebuild_socket, (DupSocket(s),))


    def _rebuild_socket(ds):
        return ds.detach()


    register(socket.socket, _reduce_socket)
else:

    def _reduce_socket(s):
        df = DupFd(s.fileno())
        return (_rebuild_socket, (df, s.family, s.type, s.proto))


    def _rebuild_socket(df, family, type, proto):
        fd = df.detach()
        return socket.socket(family, type, proto, fileno=fd)


    register(socket.socket, _reduce_socket)

class AbstractReducer(metaclass=ABCMeta):
    __doc__ = 'Abstract base class for use in implementing a Reduction class\n    suitable for use in replacing the standard reduction mechanism\n    used in multiprocessing.'
    ForkingPickler = ForkingPickler
    register = register
    dump = dump
    send_handle = send_handle
    recv_handle = recv_handle
    if sys.platform == 'win32':
        steal_handle = steal_handle
        duplicate = duplicate
        DupHandle = DupHandle
    else:
        sendfds = sendfds
        recvfds = recvfds
        DupFd = DupFd
    _reduce_method = _reduce_method
    _reduce_method_descriptor = _reduce_method_descriptor
    _rebuild_partial = _rebuild_partial
    _reduce_socket = _reduce_socket
    _rebuild_socket = _rebuild_socket

    def __init__(self, *args):
        register(type(_C().f), _reduce_method)
        register(type(list.append), _reduce_method_descriptor)
        register(type(int.__add__), _reduce_method_descriptor)
        register(functools.partial, _reduce_partial)
        register(socket.socket, _reduce_socket)