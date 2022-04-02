# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\connection.py
__all__ = [
 'Client', 'Listener', 'Pipe', 'wait']
import io, os, sys, socket, struct, time, tempfile, itertools, _multiprocessing
from . import util
from . import AuthenticationError, BufferTooShort
from .context import reduction
_ForkingPickler = reduction.ForkingPickler
try:
    import _winapi
    from _winapi import WAIT_OBJECT_0, WAIT_ABANDONED_0, WAIT_TIMEOUT, INFINITE
except ImportError:
    if sys.platform == 'win32':
        raise
    else:
        _winapi = None
else:
    BUFSIZE = 8192
    CONNECTION_TIMEOUT = 20.0
    _mmap_counter = itertools.count()
    default_family = 'AF_INET'
    families = ['AF_INET']
    if hasattr(socket, 'AF_UNIX'):
        default_family = 'AF_UNIX'
        families += ['AF_UNIX']
    if sys.platform == 'win32':
        default_family = 'AF_PIPE'
        families += ['AF_PIPE']

    def _init_timeout(timeout=CONNECTION_TIMEOUT):
        return time.monotonic() + timeout


    def _check_timeout(t):
        return time.monotonic() > t


    def arbitrary_address(family):
        """
    Return an arbitrary free address for the given family
    """
        if family == 'AF_INET':
            return ('localhost', 0)
        if family == 'AF_UNIX':
            return tempfile.mktemp(prefix='listener-', dir=(util.get_temp_dir()))
        if family == 'AF_PIPE':
            return tempfile.mktemp(prefix=('\\\\.\\pipe\\pyc-%d-%d-' % (
             os.getpid(), next(_mmap_counter))),
              dir='')
        raise ValueError('unrecognized family')


    def _validate_family(family):
        """
    Checks if the family is valid for the current environment.
    """
        if sys.platform != 'win32':
            if family == 'AF_PIPE':
                raise ValueError('Family %s is not recognized.' % family)
        if not sys.platform == 'win32' or family == 'AF_UNIX':
            if not hasattr(socket, family):
                raise ValueError('Family %s is not recognized.' % family)


    def address_type(address):
        """
    Return the types of the address

    This can be 'AF_INET', 'AF_UNIX', or 'AF_PIPE'
    """
        if type(address) == tuple:
            return 'AF_INET'
        if type(address) is str:
            if address.startswith('\\\\'):
                return 'AF_PIPE'
        if type(address) is str:
            return 'AF_UNIX'
        raise ValueError('address type of %r unrecognized' % address)


    class _ConnectionBase:
        _handle = None

        def __init__(self, handle, readable=True, writable=True):
            handle = handle.__index__()
            if handle < 0:
                raise ValueError('invalid handle')
            if not readable:
                if not writable:
                    raise ValueError('at least one of `readable` and `writable` must be True')
            self._handle = handle
            self._readable = readable
            self._writable = writable

        def __del__(self):
            if self._handle is not None:
                self._close()

        def _check_closed(self):
            if self._handle is None:
                raise OSError('handle is closed')

        def _check_readable(self):
            if not self._readable:
                raise OSError('connection is write-only')

        def _check_writable(self):
            if not self._writable:
                raise OSError('connection is read-only')

        def _bad_message_length(self):
            if self._writable:
                self._readable = False
            else:
                self.close()
            raise OSError('bad message length')

        @property
        def closed(self):
            """True if the connection is closed"""
            return self._handle is None

        @property
        def readable(self):
            """True if the connection is readable"""
            return self._readable

        @property
        def writable(self):
            """True if the connection is writable"""
            return self._writable

        def fileno(self):
            """File descriptor or handle of the connection"""
            self._check_closed()
            return self._handle

        def close(self):
            """Close the connection"""
            if self._handle is not None:
                try:
                    self._close()
                finally:
                    self._handle = None

        def send_bytes(self, buf, offset=0, size=None):
            """Send the bytes data from a bytes-like object"""
            self._check_closed()
            self._check_writable()
            m = memoryview(buf)
            if m.itemsize > 1:
                m = memoryview(bytes(m))
            n = len(m)
            if offset < 0:
                raise ValueError('offset is negative')
            if n < offset:
                raise ValueError('buffer length < offset')
            if size is None:
                size = n - offset
            elif size < 0:
                raise ValueError('size is negative')
            elif offset + size > n:
                raise ValueError('buffer length < offset + size')
            self._send_bytes(m[offset:offset + size])

        def send(self, obj):
            """Send a (picklable) object"""
            self._check_closed()
            self._check_writable()
            self._send_bytes(_ForkingPickler.dumps(obj))

        def recv_bytes(self, maxlength=None):
            """
        Receive bytes data as a bytes object.
        """
            self._check_closed()
            self._check_readable()
            if maxlength is not None:
                if maxlength < 0:
                    raise ValueError('negative maxlength')
            buf = self._recv_bytes(maxlength)
            if buf is None:
                self._bad_message_length()
            return buf.getvalue()

        def recv_bytes_into(self, buf, offset=0):
            """
        Receive bytes data into a writeable bytes-like object.
        Return the number of bytes read.
        """
            self._check_closed()
            self._check_readable()
            with memoryview(buf) as m:
                itemsize = m.itemsize
                bytesize = itemsize * len(m)
                if offset < 0:
                    raise ValueError('negative offset')
                elif offset > bytesize:
                    raise ValueError('offset too large')
                result = self._recv_bytes()
                size = result.tell()
                if bytesize < offset + size:
                    raise BufferTooShort(result.getvalue())
                result.seek(0)
                result.readinto(m[offset // itemsize:(offset + size) // itemsize])
                return size

        def recv(self):
            """Receive a (picklable) object"""
            self._check_closed()
            self._check_readable()
            buf = self._recv_bytes()
            return _ForkingPickler.loads(buf.getbuffer())

        def poll(self, timeout=0.0):
            """Whether there is any input available to be read"""
            self._check_closed()
            self._check_readable()
            return self._poll(timeout)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.close()


    if _winapi:

        class PipeConnection(_ConnectionBase):
            __doc__ = '\n        Connection class based on a Windows named pipe.\n        Overlapped I/O is used, so the handles must have been created\n        with FILE_FLAG_OVERLAPPED.\n        '
            _got_empty_message = False

            def _close(self, _CloseHandle=_winapi.CloseHandle):
                _CloseHandle(self._handle)

            def _send_bytes(self, buf):
                ov, err = _winapi.WriteFile((self._handle), buf, overlapped=True)
                try:
                    try:
                        if err == _winapi.ERROR_IO_PENDING:
                            waitres = _winapi.WaitForMultipleObjects([
                             ov.event], False, INFINITE)
                            assert waitres == WAIT_OBJECT_0
                    except:
                        ov.cancel()
                        raise

                finally:
                    nwritten, err = ov.GetOverlappedResult(True)

                assert err == 0
                assert nwritten == len(buf)

            def _recv_bytes--- This code section failed: ---

 L. 295         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _got_empty_message
                4  POP_JUMP_IF_FALSE    20  'to 20'

 L. 296         6  LOAD_CONST               False
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _got_empty_message

 L. 297        12  LOAD_GLOBAL              io
               14  LOAD_METHOD              BytesIO
               16  CALL_METHOD_0         0  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             4  '4'

 L. 299        20  LOAD_FAST                'maxsize'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    32  'to 32'
               28  LOAD_CONST               128
               30  JUMP_FORWARD         40  'to 40'
             32_0  COME_FROM            26  '26'
               32  LOAD_GLOBAL              min
               34  LOAD_FAST                'maxsize'
               36  LOAD_CONST               128
               38  CALL_FUNCTION_2       2  ''
             40_0  COME_FROM            30  '30'
               40  STORE_FAST               'bsize'

 L. 300        42  SETUP_FINALLY       236  'to 236'

 L. 301        44  LOAD_GLOBAL              _winapi
               46  LOAD_ATTR                ReadFile
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _handle
               52  LOAD_FAST                'bsize'

 L. 302        54  LOAD_CONST               True

 L. 301        56  LOAD_CONST               ('overlapped',)
               58  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'ov'
               64  STORE_FAST               'err'

 L. 303        66  LOAD_CONST               None
               68  SETUP_FINALLY       142  'to 142'
               70  SETUP_FINALLY       116  'to 116'

 L. 304        72  LOAD_FAST                'err'
               74  LOAD_GLOBAL              _winapi
               76  LOAD_ATTR                ERROR_IO_PENDING
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   112  'to 112'

 L. 305        82  LOAD_GLOBAL              _winapi
               84  LOAD_METHOD              WaitForMultipleObjects

 L. 306        86  LOAD_FAST                'ov'
               88  LOAD_ATTR                event
               90  BUILD_LIST_1          1 

 L. 306        92  LOAD_CONST               False

 L. 306        94  LOAD_GLOBAL              INFINITE

 L. 305        96  CALL_METHOD_3         3  ''
               98  STORE_FAST               'waitres'

 L. 307       100  LOAD_FAST                'waitres'
              102  LOAD_GLOBAL              WAIT_OBJECT_0
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_TRUE    112  'to 112'
              108  LOAD_ASSERT              AssertionError
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            80  '80'
              112  POP_BLOCK        
              114  JUMP_FORWARD        138  'to 138'
            116_0  COME_FROM_FINALLY    70  '70'

 L. 308       116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 309       122  LOAD_FAST                'ov'
              124  LOAD_METHOD              cancel
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          

 L. 310       130  RAISE_VARARGS_0       0  'reraise'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           114  '114'
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_FINALLY    68  '68'

 L. 312       142  LOAD_FAST                'ov'
              144  LOAD_METHOD              GetOverlappedResult
              146  LOAD_CONST               True
              148  CALL_METHOD_1         1  ''
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'nread'
              154  STORE_FAST               'err'

 L. 313       156  LOAD_FAST                'err'
              158  LOAD_CONST               0
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   198  'to 198'

 L. 314       164  LOAD_GLOBAL              io
              166  LOAD_METHOD              BytesIO
              168  CALL_METHOD_0         0  ''
              170  STORE_FAST               'f'

 L. 315       172  LOAD_FAST                'f'
              174  LOAD_METHOD              write
              176  LOAD_FAST                'ov'
              178  LOAD_METHOD              getbuffer
              180  CALL_METHOD_0         0  ''
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

 L. 316       186  LOAD_FAST                'f'
              188  POP_FINALLY           1  ''
              190  ROT_TWO          
              192  POP_TOP          
              194  POP_BLOCK        
              196  RETURN_VALUE     
            198_0  COME_FROM           162  '162'

 L. 317       198  LOAD_FAST                'err'
              200  LOAD_GLOBAL              _winapi
              202  LOAD_ATTR                ERROR_MORE_DATA
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   228  'to 228'

 L. 318       208  LOAD_FAST                'self'
              210  LOAD_METHOD              _get_more_data
              212  LOAD_FAST                'ov'
              214  LOAD_FAST                'maxsize'
              216  CALL_METHOD_2         2  ''
              218  POP_FINALLY           1  ''
              220  ROT_TWO          
              222  POP_TOP          
              224  POP_BLOCK        
              226  RETURN_VALUE     
            228_0  COME_FROM           206  '206'
              228  END_FINALLY      
              230  POP_TOP          
              232  POP_BLOCK        
              234  JUMP_FORWARD        294  'to 294'
            236_0  COME_FROM_FINALLY    42  '42'

 L. 319       236  DUP_TOP          
              238  LOAD_GLOBAL              OSError
              240  COMPARE_OP               exception-match
          242_244  POP_JUMP_IF_FALSE   292  'to 292'
              246  POP_TOP          
              248  STORE_FAST               'e'
              250  POP_TOP          
              252  SETUP_FINALLY       280  'to 280'

 L. 320       254  LOAD_FAST                'e'
              256  LOAD_ATTR                winerror
              258  LOAD_GLOBAL              _winapi
              260  LOAD_ATTR                ERROR_BROKEN_PIPE
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   274  'to 274'

 L. 321       268  LOAD_GLOBAL              EOFError
              270  RAISE_VARARGS_1       1  'exception instance'
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           264  '264'

 L. 323       274  RAISE_VARARGS_0       0  'reraise'
            276_0  COME_FROM           272  '272'
              276  POP_BLOCK        
              278  BEGIN_FINALLY    
            280_0  COME_FROM_FINALLY   252  '252'
              280  LOAD_CONST               None
              282  STORE_FAST               'e'
              284  DELETE_FAST              'e'
              286  END_FINALLY      
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
            292_0  COME_FROM           242  '242'
              292  END_FINALLY      
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           234  '234'

 L. 324       294  LOAD_GLOBAL              RuntimeError
              296  LOAD_STR                 "shouldn't get here; expected KeyboardInterrupt"
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `LOAD_FAST' instruction at offset 142

            def _poll(self, timeout):
                if self._got_empty_message or (_winapi.PeekNamedPipe(self._handle)[0] != 0):
                    return True
                return bool(wait([self], timeout))

            def _get_more_data(self, ov, maxsize):
                buf = ov.getbuffer()
                f = io.BytesIO()
                f.write(buf)
                left = _winapi.PeekNamedPipe(self._handle)[1]
                assert left > 0
                if maxsize is not None:
                    if len(buf) + left > maxsize:
                        self._bad_message_length()
                ov, err = _winapi.ReadFile((self._handle), left, overlapped=True)
                rbytes, err = ov.GetOverlappedResult(True)
                assert err == 0
                assert rbytes == left
                f.write(ov.getbuffer())
                return f


    class Connection(_ConnectionBase):
        __doc__ = '\n    Connection class based on an arbitrary file descriptor (Unix only), or\n    a socket handle (Windows).\n    '
        if _winapi:

            def _close(self, _close=_multiprocessing.closesocket):
                _close(self._handle)

            _write = _multiprocessing.send
            _read = _multiprocessing.recv
        else:

            def _close(self, _close=os.close):
                _close(self._handle)

            _write = os.write
            _read = os.read

        def _send(self, buf, write=_write):
            remaining = len(buf)
            while True:
                n = write(self._handle, buf)
                remaining -= n
                if remaining == 0:
                    pass
                else:
                    buf = buf[n:]

        def _recv(self, size, read=_read):
            buf = io.BytesIO()
            handle = self._handle
            remaining = size
            while True:
                if remaining > 0:
                    chunk = read(handle, remaining)
                    n = len(chunk)
                    if n == 0:
                        if remaining == size:
                            raise EOFError
                        else:
                            raise OSError('got end of file during message')
                    buf.write(chunk)
                    remaining -= n

            return buf

        def _send_bytes(self, buf):
            n = len(buf)
            if n > 2147483647:
                pre_header = struct.pack('!i', -1)
                header = struct.pack('!Q', n)
                self._send(pre_header)
                self._send(header)
                self._send(buf)
            else:
                header = struct.pack('!i', n)
                if n > 16384:
                    self._send(header)
                    self._send(buf)
                else:
                    self._send(header + buf)

        def _recv_bytes(self, maxsize=None):
            buf = self._recv(4)
            size, = struct.unpack('!i', buf.getvalue())
            if size == -1:
                buf = self._recv(8)
                size, = struct.unpack('!Q', buf.getvalue())
            if maxsize is not None:
                if size > maxsize:
                    return
            return self._recv(size)

        def _poll(self, timeout):
            r = wait([self], timeout)
            return bool(r)


    class Listener(object):
        __doc__ = "\n    Returns a listener object.\n\n    This is a wrapper for a bound socket which is 'listening' for\n    connections, or for a Windows named pipe.\n    "

        def __init__(self, address=None, family=None, backlog=1, authkey=None):
            family = family or address and (address_type(address)) or default_family
            address = address or arbitrary_address(family)
            _validate_family(family)
            if family == 'AF_PIPE':
                self._listener = PipeListener(address, backlog)
            else:
                self._listener = SocketListener(address, family, backlog)
            if authkey is not None:
                if not isinstance(authkey, bytes):
                    raise TypeError('authkey should be a byte string')
            self._authkey = authkey

        def accept(self):
            """
        Accept a connection on the bound socket or named pipe of `self`.

        Returns a `Connection` object.
        """
            if self._listener is None:
                raise OSError('listener is closed')
            c = self._listener.accept()
            if self._authkey:
                deliver_challenge(c, self._authkey)
                answer_challenge(c, self._authkey)
            return c

        def close(self):
            """
        Close the bound socket or named pipe of `self`.
        """
            listener = self._listener
            if listener is not None:
                self._listener = None
                listener.close()

        @property
        def address(self):
            return self._listener._address

        @property
        def last_accepted(self):
            return self._listener._last_accepted

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):
            self.close()


    def Client(address, family=None, authkey=None):
        """
    Returns a connection to the address of a `Listener`
    """
        family = family or address_type(address)
        _validate_family(family)
        if family == 'AF_PIPE':
            c = PipeClient(address)
        else:
            c = SocketClient(address)
        if authkey is not None:
            if not isinstance(authkey, bytes):
                raise TypeError('authkey should be a byte string')
            if authkey is not None:
                answer_challenge(c, authkey)
                deliver_challenge(c, authkey)
            return c


    if sys.platform != 'win32':

        def Pipe(duplex=True):
            """
        Returns pair of connection objects at either end of a pipe
        """
            if duplex:
                s1, s2 = socket.socketpair()
                s1.setblocking(True)
                s2.setblocking(True)
                c1 = Connection(s1.detach())
                c2 = Connection(s2.detach())
            else:
                fd1, fd2 = os.pipe()
                c1 = Connection(fd1, writable=False)
                c2 = Connection(fd2, readable=False)
            return (
             c1, c2)


    else:

        def Pipe(duplex=True):
            """
        Returns pair of connection objects at either end of a pipe
        """
            address = arbitrary_address('AF_PIPE')
            if duplex:
                openmode = _winapi.PIPE_ACCESS_DUPLEX
                access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
                obsize, ibsize = BUFSIZE, BUFSIZE
            else:
                openmode = _winapi.PIPE_ACCESS_INBOUND
                access = _winapi.GENERIC_WRITE
                obsize, ibsize = 0, BUFSIZE
            h1 = _winapi.CreateNamedPipe(address, openmode | _winapi.FILE_FLAG_OVERLAPPED | _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, 1, obsize, ibsize, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
            h2 = _winapi.CreateFile(address, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
            _winapi.SetNamedPipeHandleState(h2, _winapi.PIPE_READMODE_MESSAGE, None, None)
            overlapped = _winapi.ConnectNamedPipe(h1, overlapped=True)
            _, err = overlapped.GetOverlappedResult(True)
            assert err == 0
            c1 = PipeConnection(h1, writable=duplex)
            c2 = PipeConnection(h2, readable=duplex)
            return (
             c1, c2)


    class SocketListener(object):
        __doc__ = '\n    Representation of a socket which is bound to an address and listening\n    '

        def __init__(self, address, family, backlog=1):
            self._socket = socket.socket(getattr(socket, family))
            try:
                if os.name == 'posix':
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self._socket.setblocking(True)
                self._socket.bind(address)
                self._socket.listen(backlog)
                self._address = self._socket.getsockname()
            except OSError:
                self._socket.close()
                raise
            else:
                self._family = family
                self._last_accepted = None
            if family == 'AF_UNIX':
                self._unlink = util.Finalize(self,
                  (os.unlink), args=(address,), exitpriority=0)
            else:
                self._unlink = None

        def accept(self):
            s, self._last_accepted = self._socket.accept()
            s.setblocking(True)
            return Connection(s.detach())

        def close(self):
            try:
                self._socket.close()
            finally:
                unlink = self._unlink
                if unlink is not None:
                    self._unlink = None
                    unlink()


    def SocketClient(address):
        """
    Return a connection object connected to the socket given by `address`
    """
        family = address_type(address)
        with socket.socket(getattr(socket, family)) as s:
            s.setblocking(True)
            s.connect(address)
            return Connection(s.detach())


    if sys.platform == 'win32':

        class PipeListener(object):
            __doc__ = '\n        Representation of a named pipe\n        '

            def __init__(self, address, backlog=None):
                self._address = address
                self._handle_queue = [self._new_handle(first=True)]
                self._last_accepted = None
                util.sub_debug('listener created with address=%r', self._address)
                self.close = util.Finalize(self,
                  (PipeListener._finalize_pipe_listener), args=(
                 self._handle_queue, self._address),
                  exitpriority=0)

            def _new_handle(self, first=False):
                flags = _winapi.PIPE_ACCESS_DUPLEX | _winapi.FILE_FLAG_OVERLAPPED
                if first:
                    flags |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
                return _winapi.CreateNamedPipe(self._address, flags, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, _winapi.PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)

            def accept(self):
                self._handle_queue.append(self._new_handle())
                handle = self._handle_queue.pop(0)
                try:
                    ov = _winapi.ConnectNamedPipe(handle, overlapped=True)
                except OSError as e:
                    try:
                        if e.winerror != _winapi.ERROR_NO_DATA:
                            raise
                    finally:
                        e = None
                        del e

                else:
                    try:
                        try:
                            res = _winapi.WaitForMultipleObjects([
                             ov.event], False, INFINITE)
                        except:
                            ov.cancel()
                            _winapi.CloseHandle(handle)
                            raise

                    finally:
                        _, err = ov.GetOverlappedResult(True)
                        assert err == 0

                return PipeConnection(handle)

            @staticmethod
            def _finalize_pipe_listener(queue, address):
                util.sub_debug('closing listener with address=%r', address)
                for handle in queue:
                    _winapi.CloseHandle(handle)


        def PipeClient--- This code section failed: ---

 L. 698         0  LOAD_GLOBAL              _init_timeout
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               't'
              6_0  COME_FROM           126  '126'
              6_1  COME_FROM           120  '120'

 L. 700         6  SETUP_FINALLY        62  'to 62'

 L. 701         8  LOAD_GLOBAL              _winapi
               10  LOAD_METHOD              WaitNamedPipe
               12  LOAD_FAST                'address'
               14  LOAD_CONST               1000
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L. 702        20  LOAD_GLOBAL              _winapi
               22  LOAD_METHOD              CreateFile

 L. 703        24  LOAD_FAST                'address'

 L. 703        26  LOAD_GLOBAL              _winapi
               28  LOAD_ATTR                GENERIC_READ
               30  LOAD_GLOBAL              _winapi
               32  LOAD_ATTR                GENERIC_WRITE
               34  BINARY_OR        

 L. 704        36  LOAD_CONST               0

 L. 704        38  LOAD_GLOBAL              _winapi
               40  LOAD_ATTR                NULL

 L. 704        42  LOAD_GLOBAL              _winapi
               44  LOAD_ATTR                OPEN_EXISTING

 L. 705        46  LOAD_GLOBAL              _winapi
               48  LOAD_ATTR                FILE_FLAG_OVERLAPPED

 L. 705        50  LOAD_GLOBAL              _winapi
               52  LOAD_ATTR                NULL

 L. 702        54  CALL_METHOD_7         7  ''
               56  STORE_FAST               'h'
               58  POP_BLOCK        
               60  JUMP_FORWARD        130  'to 130'
             62_0  COME_FROM_FINALLY     6  '6'

 L. 707        62  DUP_TOP          
               64  LOAD_GLOBAL              OSError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE   122  'to 122'
               70  POP_TOP          
               72  STORE_FAST               'e'
               74  POP_TOP          
               76  SETUP_FINALLY       110  'to 110'

 L. 708        78  LOAD_FAST                'e'
               80  LOAD_ATTR                winerror
               82  LOAD_GLOBAL              _winapi
               84  LOAD_ATTR                ERROR_SEM_TIMEOUT

 L. 709        86  LOAD_GLOBAL              _winapi
               88  LOAD_ATTR                ERROR_PIPE_BUSY

 L. 708        90  BUILD_TUPLE_2         2 
               92  COMPARE_OP               not-in
               94  POP_JUMP_IF_TRUE    104  'to 104'

 L. 709        96  LOAD_GLOBAL              _check_timeout
               98  LOAD_FAST                't'
              100  CALL_FUNCTION_1       1  ''

 L. 708       102  POP_JUMP_IF_FALSE   106  'to 106'
            104_0  COME_FROM            94  '94'

 L. 710       104  RAISE_VARARGS_0       0  'reraise'
            106_0  COME_FROM           102  '102'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM_FINALLY    76  '76'
              110  LOAD_CONST               None
              112  STORE_FAST               'e'
              114  DELETE_FAST              'e'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_BACK             6  'to 6'
            122_0  COME_FROM            68  '68'
              122  END_FINALLY      

 L. 712       124  JUMP_FORWARD        130  'to 130'
              126  JUMP_BACK             6  'to 6'

 L. 714       128  RAISE_VARARGS_0       0  'reraise'
            130_0  COME_FROM           124  '124'
            130_1  COME_FROM            60  '60'

 L. 716       130  LOAD_GLOBAL              _winapi
              132  LOAD_METHOD              SetNamedPipeHandleState

 L. 717       134  LOAD_FAST                'h'

 L. 717       136  LOAD_GLOBAL              _winapi
              138  LOAD_ATTR                PIPE_READMODE_MESSAGE

 L. 717       140  LOAD_CONST               None

 L. 717       142  LOAD_CONST               None

 L. 716       144  CALL_METHOD_4         4  ''
              146  POP_TOP          

 L. 719       148  LOAD_GLOBAL              PipeConnection
              150  LOAD_FAST                'h'
              152  CALL_FUNCTION_1       1  ''
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 124


    MESSAGE_LENGTH = 20
    CHALLENGE = b'#CHALLENGE#'
    WELCOME = b'#WELCOME#'
    FAILURE = b'#FAILURE#'

    def deliver_challenge(connection, authkey):
        import hmac
        if not isinstance(authkey, bytes):
            raise ValueError('Authkey must be bytes, not {0!s}'.format(type(authkey)))
        message = os.urandom(MESSAGE_LENGTH)
        connection.send_bytes(CHALLENGE + message)
        digest = hmac.new(authkey, message, 'md5').digest()
        response = connection.recv_bytes(256)
        if response == digest:
            connection.send_bytes(WELCOME)
        else:
            connection.send_bytes(FAILURE)
            raise AuthenticationError('digest received was wrong')


    def answer_challenge(connection, authkey):
        import hmac
        if not isinstance(authkey, bytes):
            raise ValueError('Authkey must be bytes, not {0!s}'.format(type(authkey)))
        message = connection.recv_bytes(256)
        assert message[:len(CHALLENGE)] == CHALLENGE, 'message = %r' % message
        message = message[len(CHALLENGE):]
        digest = hmac.new(authkey, message, 'md5').digest()
        connection.send_bytes(digest)
        response = connection.recv_bytes(256)
        if response != WELCOME:
            raise AuthenticationError('digest sent was rejected')


    class ConnectionWrapper(object):

        def __init__(self, conn, dumps, loads):
            self._conn = conn
            self._dumps = dumps
            self._loads = loads
            for attr in ('fileno', 'close', 'poll', 'recv_bytes', 'send_bytes'):
                obj = getattr(conn, attr)
                setattr(self, attr, obj)

        def send(self, obj):
            s = self._dumps(obj)
            self._conn.send_bytes(s)

        def recv(self):
            s = self._conn.recv_bytes()
            return self._loads(s)


    def _xml_dumps(obj):
        return xmlrpclib.dumps((obj,), None, None, None, 1).encode('utf-8')


    def _xml_loads(s):
        (obj,), method = xmlrpclib.loads(s.decode('utf-8'))
        return obj


    class XmlListener(Listener):

        def accept(self):
            global xmlrpclib
            import xmlrpc.client as xmlrpclib
            obj = Listener.accept(self)
            return ConnectionWrapper(obj, _xml_dumps, _xml_loads)


    def XmlClient(*args, **kwds):
        global xmlrpclib
        import xmlrpc.client as xmlrpclib
        return ConnectionWrapper(Client(*args, **kwds), _xml_dumps, _xml_loads)


if sys.platform == 'win32':

    def _exhaustive_wait--- This code section failed: ---

 L. 807         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'handles'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'L'

 L. 808         8  BUILD_LIST_0          0 
               10  STORE_FAST               'ready'
             12_0  COME_FROM           168  '168'

 L. 809        12  LOAD_FAST                'L'
               14  POP_JUMP_IF_FALSE   170  'to 170'

 L. 810        16  LOAD_GLOBAL              _winapi
               18  LOAD_METHOD              WaitForMultipleObjects
               20  LOAD_FAST                'L'
               22  LOAD_CONST               False
               24  LOAD_FAST                'timeout'
               26  CALL_METHOD_3         3  ''
               28  STORE_FAST               'res'

 L. 811        30  LOAD_FAST                'res'
               32  LOAD_GLOBAL              WAIT_TIMEOUT
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 812        38  JUMP_FORWARD        170  'to 170'
               40  BREAK_LOOP          134  'to 134'
             42_0  COME_FROM            36  '36'

 L. 813        42  LOAD_GLOBAL              WAIT_OBJECT_0
               44  LOAD_FAST                'res'
               46  DUP_TOP          
               48  ROT_THREE        
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  LOAD_GLOBAL              WAIT_OBJECT_0
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'L'
               60  CALL_FUNCTION_1       1  ''
               62  BINARY_ADD       
               64  COMPARE_OP               <
               66  POP_JUMP_IF_FALSE    84  'to 84'
               68  JUMP_FORWARD         74  'to 74'
             70_0  COME_FROM            52  '52'
               70  POP_TOP          
               72  JUMP_FORWARD         84  'to 84'
             74_0  COME_FROM            68  '68'

 L. 814        74  LOAD_FAST                'res'
               76  LOAD_GLOBAL              WAIT_OBJECT_0
               78  INPLACE_SUBTRACT 
               80  STORE_FAST               'res'
               82  JUMP_FORWARD        134  'to 134'
             84_0  COME_FROM            72  '72'
             84_1  COME_FROM            66  '66'

 L. 815        84  LOAD_GLOBAL              WAIT_ABANDONED_0
               86  LOAD_FAST                'res'
               88  DUP_TOP          
               90  ROT_THREE        
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_FALSE   112  'to 112'
               96  LOAD_GLOBAL              WAIT_ABANDONED_0
               98  LOAD_GLOBAL              len
              100  LOAD_FAST                'L'
              102  CALL_FUNCTION_1       1  ''
              104  BINARY_ADD       
              106  COMPARE_OP               <
              108  POP_JUMP_IF_FALSE   126  'to 126'
              110  JUMP_FORWARD        116  'to 116'
            112_0  COME_FROM            94  '94'
              112  POP_TOP          
              114  JUMP_FORWARD        126  'to 126'
            116_0  COME_FROM           110  '110'

 L. 816       116  LOAD_FAST                'res'
              118  LOAD_GLOBAL              WAIT_ABANDONED_0
              120  INPLACE_SUBTRACT 
              122  STORE_FAST               'res'
              124  JUMP_FORWARD        134  'to 134'
            126_0  COME_FROM           114  '114'
            126_1  COME_FROM           108  '108'

 L. 818       126  LOAD_GLOBAL              RuntimeError
              128  LOAD_STR                 'Should not get here'
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           124  '124'
            134_1  COME_FROM            82  '82'
            134_2  COME_FROM            40  '40'

 L. 819       134  LOAD_FAST                'ready'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'L'
              140  LOAD_FAST                'res'
              142  BINARY_SUBSCR    
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L. 820       148  LOAD_FAST                'L'
              150  LOAD_FAST                'res'
              152  LOAD_CONST               1
              154  BINARY_ADD       
              156  LOAD_CONST               None
              158  BUILD_SLICE_2         2 
              160  BINARY_SUBSCR    
              162  STORE_FAST               'L'

 L. 821       164  LOAD_CONST               0
              166  STORE_FAST               'timeout'
              168  JUMP_BACK            12  'to 12'
            170_0  COME_FROM            38  '38'
            170_1  COME_FROM            14  '14'

 L. 822       170  LOAD_FAST                'ready'
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 170


    _ready_errors = {
     _winapi.ERROR_BROKEN_PIPE, _winapi.ERROR_NETNAME_DELETED}

    def wait(object_list, timeout=None):
        """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
        if timeout is None:
            timeout = INFINITE
        elif timeout < 0:
            timeout = 0
        else:
            timeout = int(timeout * 1000 + 0.5)
        object_list = list(object_list)
        waithandle_to_obj = {}
        ov_list = []
        ready_objects = set()
        ready_handles = set()
        try:
            for o in object_list:
                try:
                    fileno = getattr(o, 'fileno')
                except AttributeError:
                    waithandle_to_obj[o.__index__()] = o
                else:
                    try:
                        ov, err = _winapi.ReadFile(fileno(), 0, True)
                    except OSError as e:
                        try:
                            ov, err = None, e.winerror
                            if err not in _ready_errors:
                                raise
                        finally:
                            e = None
                            del e

                    else:
                        if err == _winapi.ERROR_IO_PENDING:
                            ov_list.append(ov)
                            waithandle_to_obj[ov.event] = o
                        elif not ov or sys.getwindowsversion()[:2] >= (6, 2):
                            try:
                                _, err = ov.GetOverlappedResult(False)
                            except OSError as e:
                                try:
                                    err = e.winerror
                                finally:
                                    e = None
                                    del e

                            else:
                                if not err:
                                    if hasattr(o, '_got_empty_message'):
                                        o._got_empty_message = True
                                ready_objects.add(o)
                                timeout = 0
            else:
                ready_handles = _exhaustive_wait(waithandle_to_obj.keys(), timeout)

        finally:
            for ov in ov_list:
                ov.cancel()
            else:
                for ov in ov_list:
                    try:
                        _, err = ov.GetOverlappedResult(True)
                    except OSError as e:
                        try:
                            err = e.winerror
                            if err not in _ready_errors:
                                raise
                        finally:
                            e = None
                            del e

                    else:
                        if err != _winapi.ERROR_OPERATION_ABORTED:
                            o = waithandle_to_obj[ov.event]
                            ready_objects.add(o)
                            if err == 0:
                                if hasattr(o, '_got_empty_message'):
                                    o._got_empty_message = True

        ready_objects.update((waithandle_to_obj[h] for h in ready_handles))
        return [o for o in object_list if o in ready_objects]


else:
    import selectors
    if hasattr(selectors, 'PollSelector'):
        _WaitSelector = selectors.PollSelector
    else:
        _WaitSelector = selectors.SelectSelector

    def wait(object_list, timeout=None):
        """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
        with _WaitSelector() as selector:
            for obj in object_list:
                selector.register(obj, selectors.EVENT_READ)
            else:
                if timeout is not None:
                    deadline = time.monotonic() + timeout
                while True:
                    ready = selector.select(timeout)
                    if ready:
                        return [key.fileobj for key, events in ready]
                    if timeout is not None:
                        timeout = deadline - time.monotonic()
                        if timeout < 0:
                            return ready


if sys.platform == 'win32':

    def reduce_connection(conn):
        handle = conn.fileno()
        with socket.fromfd(handle, socket.AF_INET, socket.SOCK_STREAM) as s:
            from . import resource_sharer
            ds = resource_sharer.DupSocket(s)
            return (
             rebuild_connection, (ds, conn.readable, conn.writable))


    def rebuild_connection(ds, readable, writable):
        sock = ds.detach()
        return Connection(sock.detach(), readable, writable)


    reduction.register(Connection, reduce_connection)

    def reduce_pipe_connection(conn):
        access = (_winapi.FILE_GENERIC_READ if conn.readable else 0) | (_winapi.FILE_GENERIC_WRITE if conn.writable else 0)
        dh = reduction.DupHandle(conn.fileno(), access)
        return (
         rebuild_pipe_connection, (dh, conn.readable, conn.writable))


    def rebuild_pipe_connection(dh, readable, writable):
        handle = dh.detach()
        return PipeConnection(handle, readable, writable)


    reduction.register(PipeConnection, reduce_pipe_connection)
else:

    def reduce_connection(conn):
        df = reduction.DupFd(conn.fileno())
        return (
         rebuild_connection, (df, conn.readable, conn.writable))


    def rebuild_connection(df, readable, writable):
        fd = df.detach()
        return Connection(fd, readable, writable)


    reduction.register(Connection, reduce_connection)