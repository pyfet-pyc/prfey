# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
    else:
        if sys.platform == 'win32':
            default_family = 'AF_PIPE'
            families += ['AF_PIPE']
        else:

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
                if sys.platform == 'win32':
                    if family == 'AF_UNIX':
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
                if type(address) is str or util.is_abstract_socket_namespace(address):
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
                    else:
                        n = len(m)
                        if offset < 0:
                            raise ValueError('offset is negative')
                        else:
                            if n < offset:
                                raise ValueError('buffer length < offset')
                            if size is None:
                                size = n - offset
                            else:
                                if size < 0:
                                    raise ValueError('size is negative')
                                else:
                                    if offset + size > n:
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

                def recv_bytes_into--- This code section failed: ---

 L. 226         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 227         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_readable
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 228        16  LOAD_GLOBAL              memoryview
               18  LOAD_FAST                'buf'
               20  CALL_FUNCTION_1       1  ''
               22  SETUP_WITH          174  'to 174'
               24  STORE_FAST               'm'

 L. 230        26  LOAD_FAST                'm'
               28  LOAD_ATTR                itemsize
               30  STORE_FAST               'itemsize'

 L. 231        32  LOAD_FAST                'itemsize'
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'm'
               38  CALL_FUNCTION_1       1  ''
               40  BINARY_MULTIPLY  
               42  STORE_FAST               'bytesize'

 L. 232        44  LOAD_FAST                'offset'
               46  LOAD_CONST               0
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 233        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'negative offset'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  JUMP_FORWARD         78  'to 78'
             62_0  COME_FROM            50  '50'

 L. 234        62  LOAD_FAST                'offset'
               64  LOAD_FAST                'bytesize'
               66  COMPARE_OP               >
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L. 235        70  LOAD_GLOBAL              ValueError
               72  LOAD_STR                 'offset too large'
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            68  '68'
             78_1  COME_FROM            60  '60'

 L. 236        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _recv_bytes
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'result'

 L. 237        86  LOAD_FAST                'result'
               88  LOAD_METHOD              tell
               90  CALL_METHOD_0         0  ''
               92  STORE_FAST               'size'

 L. 238        94  LOAD_FAST                'bytesize'
               96  LOAD_FAST                'offset'
               98  LOAD_FAST                'size'
              100  BINARY_ADD       
              102  COMPARE_OP               <
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 239       106  LOAD_GLOBAL              BufferTooShort
              108  LOAD_FAST                'result'
              110  LOAD_METHOD              getvalue
              112  CALL_METHOD_0         0  ''
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           104  '104'

 L. 241       118  LOAD_FAST                'result'
              120  LOAD_METHOD              seek
              122  LOAD_CONST               0
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 242       128  LOAD_FAST                'result'
              130  LOAD_METHOD              readinto
              132  LOAD_FAST                'm'
              134  LOAD_FAST                'offset'
              136  LOAD_FAST                'itemsize'
              138  BINARY_FLOOR_DIVIDE

 L. 243       140  LOAD_FAST                'offset'
              142  LOAD_FAST                'size'
              144  BINARY_ADD       
              146  LOAD_FAST                'itemsize'
              148  BINARY_FLOOR_DIVIDE

 L. 242       150  BUILD_SLICE_2         2 
              152  BINARY_SUBSCR    
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 244       158  LOAD_FAST                'size'
              160  POP_BLOCK        
              162  ROT_TWO          
              164  BEGIN_FINALLY    
              166  WITH_CLEANUP_START
              168  WITH_CLEANUP_FINISH
              170  POP_FINALLY           0  ''
              172  RETURN_VALUE     
            174_0  COME_FROM_WITH       22  '22'
              174  WITH_CLEANUP_START
              176  WITH_CLEANUP_FINISH
              178  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 162

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
                        if self._got_empty_message or _winapi.PeekNamedPipe(self._handle)[0] != 0:
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


            else:

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
                                break
                            buf = buf[n:]

                    def _recv(self, size, read=_read):
                        buf = io.BytesIO()
                        handle = self._handle
                        remaining = size
                        while remaining > 0:
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
                        family = family or address and address_type(address) or default_family
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
                        return (c1, c2)


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
                                self._unlink = util.is_abstract_socket_namespace(address) or util.Finalize(self,
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


                def SocketClient--- This code section failed: ---

 L. 627         0  LOAD_GLOBAL              address_type
                2  LOAD_FAST                'address'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'family'

 L. 628         8  LOAD_GLOBAL              socket
               10  LOAD_METHOD              socket
               12  LOAD_GLOBAL              getattr
               14  LOAD_GLOBAL              socket
               16  LOAD_FAST                'family'
               18  CALL_FUNCTION_2       2  ''
               20  CALL_METHOD_1         1  ''
               22  SETUP_WITH           70  'to 70'
               24  STORE_FAST               's'

 L. 629        26  LOAD_FAST                's'
               28  LOAD_METHOD              setblocking
               30  LOAD_CONST               True
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 630        36  LOAD_FAST                's'
               38  LOAD_METHOD              connect
               40  LOAD_FAST                'address'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 631        46  LOAD_GLOBAL              Connection
               48  LOAD_FAST                's'
               50  LOAD_METHOD              detach
               52  CALL_METHOD_0         0  ''
               54  CALL_FUNCTION_1       1  ''
               56  POP_BLOCK        
               58  ROT_TWO          
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH       22  '22'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 58


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


                    def PipeClient(address):
                        """
        Return a connection object connected to the pipe given by `address`
        """
                        t = _init_timeout()
                        while True:
                            try:
                                _winapi.WaitNamedPipe(address, 1000)
                                h = _winapi.CreateFile(address, _winapi.GENERIC_READ | _winapi.GENERIC_WRITE, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
                            except OSError as e:
                                try:
                                    if e.winerror not in (_winapi.ERROR_SEM_TIMEOUT,
                                     _winapi.ERROR_PIPE_BUSY) or _check_timeout(t):
                                        raise
                                finally:
                                    e = None
                                    del e

                            break

                        raise
                        _winapi.SetNamedPipeHandleState(h, _winapi.PIPE_READMODE_MESSAGE, None, None)
                        return PipeConnection(h)


                MESSAGE_LENGTH = 20
                CHALLENGE = b'#CHALLENGE#'
                WELCOME = b'#WELCOME#'
                FAILURE = b'#FAILURE#'

                def deliver_challenge(connection, authkey):
                    import hmac
                    if not isinstance(authkey, bytes):
                        raise ValueError('Authkey must be bytes, not {0!s}'.format(type(authkey)))
                    else:
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

                    def _exhaustive_wait(handles, timeout):
                        L = list(handles)
                        ready = []
                        while L:
                            res = _winapi.WaitForMultipleObjects(L, False, timeout)
                            if res == WAIT_TIMEOUT:
                                break
                            else:
                                if WAIT_OBJECT_0 <= res < WAIT_OBJECT_0 + len(L):
                                    res -= WAIT_OBJECT_0
                                else:
                                    if WAIT_ABANDONED_0 <= res < WAIT_ABANDONED_0 + len(L):
                                        res -= WAIT_ABANDONED_0
                                    else:
                                        raise RuntimeError('Should not get here')
                            ready.append(L[res])
                            L = L[res + 1:]
                            timeout = 0

                        return ready


                    _ready_errors = {
                     _winapi.ERROR_BROKEN_PIPE, _winapi.ERROR_NETNAME_DELETED}

                    def wait(object_list, timeout=None):
                        """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
                        if timeout is None:
                            timeout = INFINITE
                        else:
                            if timeout < 0:
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
                                        else:
                                            if ov:
                                                if sys.getwindowsversion()[:2] >= (6,
                                                                                   2):
                                                    try:
                                                        _, err = ov.GetOverlappedResult(False)
                                                    except OSError as e:
                                                        try:
                                                            err = e.winerror
                                                        finally:
                                                            e = None
                                                            del e

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

                                if err != _winapi.ERROR_OPERATION_ABORTED:
                                    o = waithandle_to_obj[ov.event]
                                    ready_objects.add(o)
                                    if err == 0 and hasattr(o, '_got_empty_message'):
                                        o._got_empty_message = True

                        ready_objects.update((waithandle_to_obj[h] for h in ready_handles))
                        return [o for o in object_list if o in ready_objects]


                else:
                    import selectors
                    if hasattr(selectors, 'PollSelector'):
                        _WaitSelector = selectors.PollSelector
                    else:
                        _WaitSelector = selectors.SelectSelector

            def wait--- This code section failed: ---

 L. 923         0  LOAD_GLOBAL              _WaitSelector
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH          142  'to 142'
                6  STORE_FAST               'selector'

 L. 924         8  LOAD_FAST                'object_list'
               10  GET_ITER         
               12  FOR_ITER             32  'to 32'
               14  STORE_FAST               'obj'

 L. 925        16  LOAD_FAST                'selector'
               18  LOAD_METHOD              register
               20  LOAD_FAST                'obj'
               22  LOAD_GLOBAL              selectors
               24  LOAD_ATTR                EVENT_READ
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          
               30  JUMP_BACK            12  'to 12'

 L. 927        32  LOAD_FAST                'timeout'
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 928        40  LOAD_GLOBAL              time
               42  LOAD_METHOD              monotonic
               44  CALL_METHOD_0         0  ''
               46  LOAD_FAST                'timeout'
               48  BINARY_ADD       
               50  STORE_FAST               'deadline'
             52_0  COME_FROM           118  '118'
             52_1  COME_FROM            98  '98'
             52_2  COME_FROM            38  '38'

 L. 931        52  LOAD_FAST                'selector'
               54  LOAD_METHOD              select
               56  LOAD_FAST                'timeout'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'ready'

 L. 932        62  LOAD_FAST                'ready'
               64  POP_JUMP_IF_FALSE    92  'to 92'

 L. 933        66  LOAD_LISTCOMP            '<code_object <listcomp>>'
               68  LOAD_STR                 'wait.<locals>.<listcomp>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_FAST                'ready'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  POP_BLOCK        
               80  ROT_TWO          
               82  BEGIN_FINALLY    
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  POP_FINALLY           0  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            64  '64'

 L. 935        92  LOAD_FAST                'timeout'
               94  LOAD_CONST               None
               96  COMPARE_OP               is-not
               98  POP_JUMP_IF_FALSE    52  'to 52'

 L. 936       100  LOAD_FAST                'deadline'
              102  LOAD_GLOBAL              time
              104  LOAD_METHOD              monotonic
              106  CALL_METHOD_0         0  ''
              108  BINARY_SUBTRACT  
              110  STORE_FAST               'timeout'

 L. 937       112  LOAD_FAST                'timeout'
              114  LOAD_CONST               0
              116  COMPARE_OP               <
              118  POP_JUMP_IF_FALSE    52  'to 52'

 L. 938       120  LOAD_FAST                'ready'
              122  POP_BLOCK        
              124  ROT_TWO          
              126  BEGIN_FINALLY    
              128  WITH_CLEANUP_START
              130  WITH_CLEANUP_FINISH
              132  POP_FINALLY           0  ''
              134  RETURN_VALUE     
              136  JUMP_BACK            52  'to 52'
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_WITH        4  '4'
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 80


        if sys.platform == 'win32':

            def reduce_connection--- This code section failed: ---

 L. 946         0  LOAD_FAST                'conn'
                2  LOAD_METHOD              fileno
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'handle'

 L. 947         8  LOAD_GLOBAL              socket
               10  LOAD_METHOD              fromfd
               12  LOAD_FAST                'handle'
               14  LOAD_GLOBAL              socket
               16  LOAD_ATTR                AF_INET
               18  LOAD_GLOBAL              socket
               20  LOAD_ATTR                SOCK_STREAM
               22  CALL_METHOD_3         3  ''
               24  SETUP_WITH           80  'to 80'
               26  STORE_FAST               's'

 L. 948        28  LOAD_CONST               1
               30  LOAD_CONST               ('resource_sharer',)
               32  IMPORT_NAME              
               34  IMPORT_FROM              resource_sharer
               36  STORE_FAST               'resource_sharer'
               38  POP_TOP          

 L. 949        40  LOAD_FAST                'resource_sharer'
               42  LOAD_METHOD              DupSocket
               44  LOAD_FAST                's'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'ds'

 L. 950        50  LOAD_GLOBAL              rebuild_connection
               52  LOAD_FAST                'ds'
               54  LOAD_FAST                'conn'
               56  LOAD_ATTR                readable
               58  LOAD_FAST                'conn'
               60  LOAD_ATTR                writable
               62  BUILD_TUPLE_3         3 
               64  BUILD_TUPLE_2         2 
               66  POP_BLOCK        
               68  ROT_TWO          
               70  BEGIN_FINALLY    
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  POP_FINALLY           0  ''
               78  RETURN_VALUE     
             80_0  COME_FROM_WITH       24  '24'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 68


            def rebuild_connection(ds, readable, writable):
                sock = ds.detach()
                return Connection(sock.detach(), readable, writable)


            reduction.register(Connection, reduce_connection)

            def reduce_pipe_connection(conn):
                access = (_winapi.FILE_GENERIC_READ if conn.readable else 0) | (_winapi.FILE_GENERIC_WRITE if conn.writable else 0)
                dh = reduction.DupHandle(conn.fileno(), access)
                return (rebuild_pipe_connection, (dh, conn.readable, conn.writable))


            def rebuild_pipe_connection(dh, readable, writable):
                handle = dh.detach()
                return PipeConnection(handle, readable, writable)


            reduction.register(PipeConnection, reduce_pipe_connection)
        else:

            def reduce_connection(conn):
                df = reduction.DupFd(conn.fileno())
                return (rebuild_connection, (df, conn.readable, conn.writable))


        def rebuild_connection(df, readable, writable):
            fd = df.detach()
            return Connection(fd, readable, writable)


        reduction.register(Connection, reduce_connection)