# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: socket.py
"""This module provides socket operations and some related functions.
On Unix, it supports IP (Internet Protocol) and Unix domain sockets.
On other systems, it only supports IP. Functions specific for a
socket are available as methods of the socket object.

Functions:

socket() -- create a new socket object
socketpair() -- create a pair of new socket objects [*]
fromfd() -- create a socket object from an open file descriptor [*]
fromshare() -- create a socket object from data received from socket.share() [*]
gethostname() -- return the current hostname
gethostbyname() -- map a hostname to its IP number
gethostbyaddr() -- map an IP number or hostname to DNS info
getservbyname() -- map a service name and a protocol name to a port number
getprotobyname() -- map a protocol name (e.g. 'tcp') to a number
ntohs(), ntohl() -- convert 16, 32 bit int from network to host byte order
htons(), htonl() -- convert 16, 32 bit int from host to network byte order
inet_aton() -- convert IP addr string (123.45.67.89) to 32-bit packed format
inet_ntoa() -- convert 32-bit packed format IP to string (123.45.67.89)
socket.getdefaulttimeout() -- get the default timeout value
socket.setdefaulttimeout() -- set the default timeout value
create_connection() -- connects to an address, with an optional timeout and
                       optional source address.

 [*] not available on all platforms!

Special objects:

SocketType -- type object for socket objects
error -- exception raised for I/O errors
has_ipv6 -- boolean value indicating if IPv6 is supported

IntEnum constants:

AF_INET, AF_UNIX -- socket domains (first argument to socket() call)
SOCK_STREAM, SOCK_DGRAM, SOCK_RAW -- socket types (second argument)

Integer constants:

Many other constants may be defined; these may be used in calls to
the setsockopt() and getsockopt() methods.
"""
import _socket
from _socket import *
import os, sys, io, selectors
from enum import IntEnum, IntFlag
try:
    import errno
except ImportError:
    errno = None
else:
    EBADF = getattr(errno, 'EBADF', 9)
    EAGAIN = getattr(errno, 'EAGAIN', 11)
    EWOULDBLOCK = getattr(errno, 'EWOULDBLOCK', 11)
    __all__ = [
     'fromfd', 'getfqdn', 'create_connection', 'create_server',
     'has_dualstack_ipv6', 'AddressFamily', 'SocketKind']
    __all__.extend(os._get_exports_list(_socket))
    IntEnum._convert_('AddressFamily', __name__, lambda C: C.isupper() and C.startswith('AF_'))
    IntEnum._convert_('SocketKind', __name__, lambda C: C.isupper() and C.startswith('SOCK_'))
    IntFlag._convert_('MsgFlag', __name__, lambda C: C.isupper() and C.startswith('MSG_'))
    IntFlag._convert_('AddressInfo', __name__, lambda C: C.isupper() and C.startswith('AI_'))
    _LOCALHOST = '127.0.0.1'
    _LOCALHOST_V6 = '::1'

    def _intenum_converter(value, enum_klass):
        """Convert a numeric family value to an IntEnum member.

    If it's not a known member, return the numeric value itself.
    """
        try:
            return enum_klass(value)
        except ValueError:
            return value


    _realsocket = socket
    if sys.platform.lower().startswith('win'):
        errorTab = {}
        errorTab[6] = 'Specified event object handle is invalid.'
        errorTab[8] = 'Insufficient memory available.'
        errorTab[87] = 'One or more parameters are invalid.'
        errorTab[995] = 'Overlapped operation aborted.'
        errorTab[996] = 'Overlapped I/O event object not in signaled state.'
        errorTab[997] = 'Overlapped operation will complete later.'
        errorTab[10004] = 'The operation was interrupted.'
        errorTab[10009] = 'A bad file handle was passed.'
        errorTab[10013] = 'Permission denied.'
        errorTab[10014] = 'A fault occurred on the network??'
        errorTab[10022] = 'An invalid operation was attempted.'
        errorTab[10024] = 'Too many open files.'
        errorTab[10035] = 'The socket operation would block'
        errorTab[10036] = 'A blocking operation is already in progress.'
        errorTab[10037] = 'Operation already in progress.'
        errorTab[10038] = 'Socket operation on nonsocket.'
        errorTab[10039] = 'Destination address required.'
        errorTab[10040] = 'Message too long.'
        errorTab[10041] = 'Protocol wrong type for socket.'
        errorTab[10042] = 'Bad protocol option.'
        errorTab[10043] = 'Protocol not supported.'
        errorTab[10044] = 'Socket type not supported.'
        errorTab[10045] = 'Operation not supported.'
        errorTab[10046] = 'Protocol family not supported.'
        errorTab[10047] = 'Address family not supported by protocol family.'
        errorTab[10048] = 'The network address is in use.'
        errorTab[10049] = 'Cannot assign requested address.'
        errorTab[10050] = 'Network is down.'
        errorTab[10051] = 'Network is unreachable.'
        errorTab[10052] = 'Network dropped connection on reset.'
        errorTab[10053] = 'Software caused connection abort.'
        errorTab[10054] = 'The connection has been reset.'
        errorTab[10055] = 'No buffer space available.'
        errorTab[10056] = 'Socket is already connected.'
        errorTab[10057] = 'Socket is not connected.'
        errorTab[10058] = 'The network has been shut down.'
        errorTab[10059] = 'Too many references.'
        errorTab[10060] = 'The operation timed out.'
        errorTab[10061] = 'Connection refused.'
        errorTab[10062] = 'Cannot translate name.'
        errorTab[10063] = 'The name is too long.'
        errorTab[10064] = 'The host is down.'
        errorTab[10065] = 'The host is unreachable.'
        errorTab[10066] = 'Directory not empty.'
        errorTab[10067] = 'Too many processes.'
        errorTab[10068] = 'User quota exceeded.'
        errorTab[10069] = 'Disk quota exceeded.'
        errorTab[10070] = 'Stale file handle reference.'
        errorTab[10071] = 'Item is remote.'
        errorTab[10091] = 'Network subsystem is unavailable.'
        errorTab[10092] = 'Winsock.dll version out of range.'
        errorTab[10093] = 'Successful WSAStartup not yet performed.'
        errorTab[10101] = 'Graceful shutdown in progress.'
        errorTab[10102] = 'No more results from WSALookupServiceNext.'
        errorTab[10103] = 'Call has been canceled.'
        errorTab[10104] = 'Procedure call table is invalid.'
        errorTab[10105] = 'Service provider is invalid.'
        errorTab[10106] = 'Service provider failed to initialize.'
        errorTab[10107] = 'System call failure.'
        errorTab[10108] = 'Service not found.'
        errorTab[10109] = 'Class type not found.'
        errorTab[10110] = 'No more results from WSALookupServiceNext.'
        errorTab[10111] = 'Call was canceled.'
        errorTab[10112] = 'Database query was refused.'
        errorTab[11001] = 'Host not found.'
        errorTab[11002] = 'Nonauthoritative host not found.'
        errorTab[11003] = 'This is a nonrecoverable error.'
        errorTab[11004] = 'Valid name, no data record requested type.'
        errorTab[11005] = 'QoS receivers.'
        errorTab[11006] = 'QoS senders.'
        errorTab[11007] = 'No QoS senders.'
        errorTab[11008] = 'QoS no receivers.'
        errorTab[11009] = 'QoS request confirmed.'
        errorTab[11010] = 'QoS admission error.'
        errorTab[11011] = 'QoS policy failure.'
        errorTab[11012] = 'QoS bad style.'
        errorTab[11013] = 'QoS bad object.'
        errorTab[11014] = 'QoS traffic control error.'
        errorTab[11015] = 'QoS generic error.'
        errorTab[11016] = 'QoS service type error.'
        errorTab[11017] = 'QoS flowspec error.'
        errorTab[11018] = 'Invalid QoS provider buffer.'
        errorTab[11019] = 'Invalid QoS filter style.'
        errorTab[11020] = 'Invalid QoS filter style.'
        errorTab[11021] = 'Incorrect QoS filter count.'
        errorTab[11022] = 'Invalid QoS object length.'
        errorTab[11023] = 'Incorrect QoS flow count.'
        errorTab[11024] = 'Unrecognized QoS object.'
        errorTab[11025] = 'Invalid QoS policy object.'
        errorTab[11026] = 'Invalid QoS flow descriptor.'
        errorTab[11027] = 'Invalid QoS provider-specific flowspec.'
        errorTab[11028] = 'Invalid QoS provider-specific filterspec.'
        errorTab[11029] = 'Invalid QoS shape discard mode object.'
        errorTab[11030] = 'Invalid QoS shaping rate object.'
        errorTab[11031] = 'Reserved policy QoS element type.'
        __all__.append('errorTab')

    class _GiveupOnSendfile(Exception):
        pass


    class socket(_socket.socket):
        __doc__ = 'A subclass of _socket.socket adding the makefile() method.'
        __slots__ = [
         '__weakref__', '_io_refs', '_closed']

        def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
            if fileno is None:
                if family == -1:
                    family = AF_INET
                if type == -1:
                    type = SOCK_STREAM
                if proto == -1:
                    proto = 0
            _socket.socket.__init__(self, family, type, proto, fileno)
            self._io_refs = 0
            self._closed = False

        def __enter__(self):
            return self

        def __exit__(self, *args):
            if not self._closed:
                self.close()

        def __repr__(self):
            """Wrap __repr__() to reveal the real class name and socket
        address(es).
        """
            closed = getattr(self, '_closed', False)
            s = '<%s.%s%s fd=%i, family=%s, type=%s, proto=%i' % (
             self.__class__.__module__,
             self.__class__.__qualname__,
             ' [closed]' if closed else '',
             self.fileno(),
             self.family,
             self.type,
             self.proto)
            if not closed:
                try:
                    laddr = self.getsockname()
                    if laddr:
                        s += ', laddr=%s' % str(laddr)
                except error:
                    pass
                else:
                    try:
                        raddr = self.getpeername()
                        if raddr:
                            s += ', raddr=%s' % str(raddr)
                    except error:
                        pass
                    else:
                        s += '>'
                return s

        def __getstate__(self):
            raise TypeError(f"cannot pickle {self.__class__.__name__!r} object")

        def dup(self):
            """dup() -> socket object

        Duplicate the socket. Return a new socket object connected to the same
        system resource. The new socket is non-inheritable.
        """
            fd = dup(self.fileno())
            sock = self.__class__((self.family), (self.type), (self.proto), fileno=fd)
            sock.settimeout(self.gettimeout())
            return sock

        def accept(self):
            """accept() -> (socket object, address info)

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
            fd, addr = self._accept()
            sock = socket((self.family), (self.type), (self.proto), fileno=fd)
            if getdefaulttimeout() is None:
                if self.gettimeout():
                    sock.setblocking(True)
            return (
             sock, addr)

        def makefile(self, mode='r', buffering=None, *, encoding=None, errors=None, newline=None):
            """makefile(...) -> an I/O stream connected to the socket

        The arguments are as for io.open() after the filename, except the only
        supported mode values are 'r' (default), 'w' and 'b'.
        """
            if not set(mode) <= {'r', 'w', 'b'}:
                raise ValueError('invalid mode %r (only r, w, b allowed)' % (mode,))
            writing = 'w' in mode
            reading = 'r' in mode or not writing
            if not reading:
                assert writing
                binary = 'b' in mode
                rawmode = ''
                if reading:
                    rawmode += 'r'
                if writing:
                    rawmode += 'w'
                raw = SocketIO(self, rawmode)
                self._io_refs += 1
                if buffering is None:
                    buffering = -1
                if buffering < 0:
                    buffering = io.DEFAULT_BUFFER_SIZE
                if buffering == 0:
                    if not binary:
                        raise ValueError('unbuffered streams must be binary')
                    return raw
                if reading and writing:
                    buffer = io.BufferedRWPair(raw, raw, buffering)
                elif reading:
                    buffer = io.BufferedReader(raw, buffering)
                else:
                    assert writing
                    buffer = io.BufferedWriter(raw, buffering)
                if binary:
                    return buffer
                text = io.TextIOWrapper(buffer, encoding, errors, newline)
                text.mode = mode
                return text

        if hasattr(os, 'sendfile'):

            def _sendfile_use_sendfile--- This code section failed: ---

 L. 346         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_sendfile_params
                4  LOAD_FAST                'file'
                6  LOAD_FAST                'offset'
                8  LOAD_FAST                'count'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 347        14  LOAD_FAST                'self'
               16  LOAD_METHOD              fileno
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'sockno'

 L. 348        22  SETUP_FINALLY        36  'to 36'

 L. 349        24  LOAD_FAST                'file'
               26  LOAD_METHOD              fileno
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'fileno'
               32  POP_BLOCK        
               34  JUMP_FORWARD         84  'to 84'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 350        36  DUP_TOP          
               38  LOAD_GLOBAL              AttributeError
               40  LOAD_GLOBAL              io
               42  LOAD_ATTR                UnsupportedOperation
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    82  'to 82'
               50  POP_TOP          
               52  STORE_FAST               'err'
               54  POP_TOP          
               56  SETUP_FINALLY        70  'to 70'

 L. 351        58  LOAD_GLOBAL              _GiveupOnSendfile
               60  LOAD_FAST                'err'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_BLOCK        
               68  BEGIN_FINALLY    
             70_0  COME_FROM_FINALLY    56  '56'
               70  LOAD_CONST               None
               72  STORE_FAST               'err'
               74  DELETE_FAST              'err'
               76  END_FINALLY      
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            48  '48'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            34  '34'

 L. 352        84  SETUP_FINALLY       102  'to 102'

 L. 353        86  LOAD_GLOBAL              os
               88  LOAD_METHOD              fstat
               90  LOAD_FAST                'fileno'
               92  CALL_METHOD_1         1  ''
               94  LOAD_ATTR                st_size
               96  STORE_FAST               'fsize'
               98  POP_BLOCK        
              100  JUMP_FORWARD        144  'to 144'
            102_0  COME_FROM_FINALLY    84  '84'

 L. 354       102  DUP_TOP          
              104  LOAD_GLOBAL              OSError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   142  'to 142'
              110  POP_TOP          
              112  STORE_FAST               'err'
              114  POP_TOP          
              116  SETUP_FINALLY       130  'to 130'

 L. 355       118  LOAD_GLOBAL              _GiveupOnSendfile
              120  LOAD_FAST                'err'
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_FINALLY   116  '116'
              130  LOAD_CONST               None
              132  STORE_FAST               'err'
              134  DELETE_FAST              'err'
              136  END_FINALLY      
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           108  '108'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           100  '100'

 L. 356       144  LOAD_FAST                'fsize'
              146  POP_JUMP_IF_TRUE    152  'to 152'

 L. 357       148  LOAD_CONST               0
              150  RETURN_VALUE     
            152_0  COME_FROM           146  '146'

 L. 359       152  LOAD_GLOBAL              min
              154  LOAD_FAST                'count'
              156  JUMP_IF_TRUE_OR_POP   160  'to 160'
              158  LOAD_FAST                'fsize'
            160_0  COME_FROM           156  '156'
              160  LOAD_CONST               1073741824
              162  CALL_FUNCTION_2       2  ''
              164  STORE_FAST               'blocksize'

 L. 360       166  LOAD_FAST                'self'
              168  LOAD_METHOD              gettimeout
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'timeout'

 L. 361       174  LOAD_FAST                'timeout'
              176  LOAD_CONST               0
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 362       182  LOAD_GLOBAL              ValueError
              184  LOAD_STR                 'non-blocking sockets are not supported'
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'
            190_0  COME_FROM           180  '180'

 L. 366       190  LOAD_GLOBAL              hasattr
              192  LOAD_GLOBAL              selectors
              194  LOAD_STR                 'PollSelector'
              196  CALL_FUNCTION_2       2  ''
              198  POP_JUMP_IF_FALSE   210  'to 210'

 L. 367       200  LOAD_GLOBAL              selectors
              202  LOAD_METHOD              PollSelector
              204  CALL_METHOD_0         0  ''
              206  STORE_FAST               'selector'
              208  JUMP_FORWARD        218  'to 218'
            210_0  COME_FROM           198  '198'

 L. 369       210  LOAD_GLOBAL              selectors
              212  LOAD_METHOD              SelectSelector
              214  CALL_METHOD_0         0  ''
              216  STORE_FAST               'selector'
            218_0  COME_FROM           208  '208'

 L. 370       218  LOAD_FAST                'selector'
              220  LOAD_METHOD              register
              222  LOAD_FAST                'sockno'
              224  LOAD_GLOBAL              selectors
              226  LOAD_ATTR                EVENT_WRITE
              228  CALL_METHOD_2         2  ''
              230  POP_TOP          

 L. 372       232  LOAD_CONST               0
              234  STORE_FAST               'total_sent'

 L. 374       236  LOAD_FAST                'selector'
              238  LOAD_ATTR                select
              240  STORE_FAST               'selector_select'

 L. 375       242  LOAD_GLOBAL              os
              244  LOAD_ATTR                sendfile
              246  STORE_FAST               'os_sendfile'

 L. 376       248  SETUP_FINALLY       460  'to 460'
            250_0  COME_FROM           450  '450'
            250_1  COME_FROM           416  '416'
            250_2  COME_FROM           358  '358'
            250_3  COME_FROM           354  '354'

 L. 378       250  LOAD_FAST                'timeout'
          252_254  POP_JUMP_IF_FALSE   276  'to 276'
              256  LOAD_FAST                'selector_select'
              258  LOAD_FAST                'timeout'
              260  CALL_FUNCTION_1       1  ''
          262_264  POP_JUMP_IF_TRUE    276  'to 276'

 L. 379       266  LOAD_GLOBAL              _socket
              268  LOAD_METHOD              timeout
              270  LOAD_STR                 'timed out'
              272  CALL_METHOD_1         1  ''
              274  RAISE_VARARGS_1       1  'exception instance'
            276_0  COME_FROM           262  '262'
            276_1  COME_FROM           252  '252'

 L. 380       276  LOAD_FAST                'count'
          278_280  POP_JUMP_IF_FALSE   304  'to 304'

 L. 381       282  LOAD_FAST                'count'
              284  LOAD_FAST                'total_sent'
              286  BINARY_SUBTRACT  
              288  STORE_FAST               'blocksize'

 L. 382       290  LOAD_FAST                'blocksize'
              292  LOAD_CONST               0
              294  COMPARE_OP               <=
          296_298  POP_JUMP_IF_FALSE   304  'to 304'

 L. 383   300_302  JUMP_FORWARD        452  'to 452'
            304_0  COME_FROM           296  '296'
            304_1  COME_FROM           278  '278'

 L. 384       304  SETUP_FINALLY       324  'to 324'

 L. 385       306  LOAD_FAST                'os_sendfile'
              308  LOAD_FAST                'sockno'
              310  LOAD_FAST                'fileno'
              312  LOAD_FAST                'offset'
              314  LOAD_FAST                'blocksize'
              316  CALL_FUNCTION_4       4  ''
              318  STORE_FAST               'sent'
              320  POP_BLOCK        
              322  JUMP_FORWARD        420  'to 420'
            324_0  COME_FROM_FINALLY   304  '304'

 L. 386       324  DUP_TOP          
              326  LOAD_GLOBAL              BlockingIOError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   360  'to 360'
              334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L. 387       340  LOAD_FAST                'timeout'
          342_344  POP_JUMP_IF_TRUE    352  'to 352'

 L. 390       346  LOAD_FAST                'selector_select'
              348  CALL_FUNCTION_0       0  ''
              350  POP_TOP          
            352_0  COME_FROM           342  '342'

 L. 391       352  POP_EXCEPT       
              354  JUMP_BACK           250  'to 250'
              356  POP_EXCEPT       
              358  JUMP_BACK           250  'to 250'
            360_0  COME_FROM           330  '330'

 L. 392       360  DUP_TOP          
              362  LOAD_GLOBAL              OSError
              364  COMPARE_OP               exception-match
          366_368  POP_JUMP_IF_FALSE   418  'to 418'
              370  POP_TOP          
              372  STORE_FAST               'err'
              374  POP_TOP          
              376  SETUP_FINALLY       406  'to 406'

 L. 393       378  LOAD_FAST                'total_sent'
              380  LOAD_CONST               0
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   396  'to 396'

 L. 398       388  LOAD_GLOBAL              _GiveupOnSendfile
              390  LOAD_FAST                'err'
              392  CALL_FUNCTION_1       1  ''
              394  RAISE_VARARGS_1       1  'exception instance'
            396_0  COME_FROM           384  '384'

 L. 399       396  LOAD_FAST                'err'
              398  LOAD_CONST               None
              400  RAISE_VARARGS_2       2  'exception instance with __cause__'
              402  POP_BLOCK        
              404  BEGIN_FINALLY    
            406_0  COME_FROM_FINALLY   376  '376'
              406  LOAD_CONST               None
              408  STORE_FAST               'err'
              410  DELETE_FAST              'err'
              412  END_FINALLY      
              414  POP_EXCEPT       
              416  JUMP_BACK           250  'to 250'
            418_0  COME_FROM           366  '366'
              418  END_FINALLY      
            420_0  COME_FROM           322  '322'

 L. 401       420  LOAD_FAST                'sent'
              422  LOAD_CONST               0
              424  COMPARE_OP               ==
          426_428  POP_JUMP_IF_FALSE   434  'to 434'

 L. 402   430_432  JUMP_FORWARD        452  'to 452'
            434_0  COME_FROM           426  '426'

 L. 403       434  LOAD_FAST                'offset'
              436  LOAD_FAST                'sent'
              438  INPLACE_ADD      
              440  STORE_FAST               'offset'

 L. 404       442  LOAD_FAST                'total_sent'
              444  LOAD_FAST                'sent'
              446  INPLACE_ADD      
              448  STORE_FAST               'total_sent'
              450  JUMP_BACK           250  'to 250'
            452_0  COME_FROM           430  '430'
            452_1  COME_FROM           300  '300'

 L. 405       452  LOAD_FAST                'total_sent'
              454  POP_BLOCK        
              456  CALL_FINALLY        460  'to 460'
              458  RETURN_VALUE     
            460_0  COME_FROM           456  '456'
            460_1  COME_FROM_FINALLY   248  '248'

 L. 407       460  LOAD_FAST                'total_sent'
              462  LOAD_CONST               0
              464  COMPARE_OP               >
          466_468  POP_JUMP_IF_FALSE   492  'to 492'
              470  LOAD_GLOBAL              hasattr
              472  LOAD_FAST                'file'
              474  LOAD_STR                 'seek'
              476  CALL_FUNCTION_2       2  ''
          478_480  POP_JUMP_IF_FALSE   492  'to 492'

 L. 408       482  LOAD_FAST                'file'
              484  LOAD_METHOD              seek
              486  LOAD_FAST                'offset'
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          
            492_0  COME_FROM           478  '478'
            492_1  COME_FROM           466  '466'
              492  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 358

        else:

            def _sendfile_use_sendfile(self, file, offset=0, count=None):
                raise _GiveupOnSendfile('os.sendfile() not available on this platform')

        def _sendfile_use_send--- This code section failed: ---

 L. 415         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_sendfile_params
                4  LOAD_FAST                'file'
                6  LOAD_FAST                'offset'
                8  LOAD_FAST                'count'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 416        14  LOAD_FAST                'self'
               16  LOAD_METHOD              gettimeout
               18  CALL_METHOD_0         0  ''
               20  LOAD_CONST               0
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 417        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'non-blocking sockets are not supported'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 418        34  LOAD_FAST                'offset'
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 419        38  LOAD_FAST                'file'
               40  LOAD_METHOD              seek
               42  LOAD_FAST                'offset'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'

 L. 420        48  LOAD_FAST                'count'
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  LOAD_GLOBAL              min
               54  LOAD_FAST                'count'
               56  LOAD_CONST               8192
               58  CALL_FUNCTION_2       2  ''
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            50  '50'
               62  LOAD_CONST               8192
             64_0  COME_FROM            60  '60'
               64  STORE_FAST               'blocksize'

 L. 421        66  LOAD_CONST               0
               68  STORE_FAST               'total_sent'

 L. 423        70  LOAD_FAST                'file'
               72  LOAD_ATTR                read
               74  STORE_FAST               'file_read'

 L. 424        76  LOAD_FAST                'self'
               78  LOAD_ATTR                send
               80  STORE_FAST               'sock_send'

 L. 425        82  SETUP_FINALLY       216  'to 216'
             84_0  COME_FROM           206  '206'
             84_1  COME_FROM           202  '202'

 L. 427        84  LOAD_FAST                'count'
               86  POP_JUMP_IF_FALSE   112  'to 112'

 L. 428        88  LOAD_GLOBAL              min
               90  LOAD_FAST                'count'
               92  LOAD_FAST                'total_sent'
               94  BINARY_SUBTRACT  
               96  LOAD_FAST                'blocksize'
               98  CALL_FUNCTION_2       2  ''
              100  STORE_FAST               'blocksize'

 L. 429       102  LOAD_FAST                'blocksize'
              104  LOAD_CONST               0
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L. 430       110  JUMP_FORWARD        208  'to 208'
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            86  '86'

 L. 431       112  LOAD_GLOBAL              memoryview
              114  LOAD_FAST                'file_read'
              116  LOAD_FAST                'blocksize'
              118  CALL_FUNCTION_1       1  ''
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'data'

 L. 432       124  LOAD_FAST                'data'
              126  POP_JUMP_IF_TRUE    130  'to 130'

 L. 433       128  JUMP_FORWARD        208  'to 208'
            130_0  COME_FROM           204  '204'
            130_1  COME_FROM           200  '200'
            130_2  COME_FROM           164  '164'
            130_3  COME_FROM           160  '160'
            130_4  COME_FROM           126  '126'

 L. 435       130  SETUP_FINALLY       144  'to 144'

 L. 436       132  LOAD_FAST                'sock_send'
              134  LOAD_FAST                'data'
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'sent'
              140  POP_BLOCK        
              142  JUMP_FORWARD        168  'to 168'
            144_0  COME_FROM_FINALLY   130  '130'

 L. 437       144  DUP_TOP          
              146  LOAD_GLOBAL              BlockingIOError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   166  'to 166'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 438       158  POP_EXCEPT       
              160  JUMP_BACK           130  'to 130'
              162  POP_EXCEPT       
              164  JUMP_BACK           130  'to 130'
            166_0  COME_FROM           150  '150'
              166  END_FINALLY      
            168_0  COME_FROM           142  '142'

 L. 440       168  LOAD_FAST                'total_sent'
              170  LOAD_FAST                'sent'
              172  INPLACE_ADD      
              174  STORE_FAST               'total_sent'

 L. 441       176  LOAD_FAST                'sent'
              178  LOAD_GLOBAL              len
              180  LOAD_FAST                'data'
              182  CALL_FUNCTION_1       1  ''
              184  COMPARE_OP               <
              186  POP_JUMP_IF_FALSE   206  'to 206'

 L. 442       188  LOAD_FAST                'data'
              190  LOAD_FAST                'sent'
              192  LOAD_CONST               None
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  STORE_FAST               'data'
              200  JUMP_BACK           130  'to 130'

 L. 444       202  CONTINUE             84  'to 84'
              204  JUMP_BACK           130  'to 130'
            206_0  COME_FROM           186  '186'
              206  JUMP_BACK            84  'to 84'
            208_0  COME_FROM           128  '128'
            208_1  COME_FROM           110  '110'

 L. 445       208  LOAD_FAST                'total_sent'
              210  POP_BLOCK        
              212  CALL_FINALLY        216  'to 216'
              214  RETURN_VALUE     
            216_0  COME_FROM           212  '212'
            216_1  COME_FROM_FINALLY    82  '82'

 L. 447       216  LOAD_FAST                'total_sent'
              218  LOAD_CONST               0
              220  COMPARE_OP               >
              222  POP_JUMP_IF_FALSE   248  'to 248'
              224  LOAD_GLOBAL              hasattr
              226  LOAD_FAST                'file'
              228  LOAD_STR                 'seek'
              230  CALL_FUNCTION_2       2  ''
              232  POP_JUMP_IF_FALSE   248  'to 248'

 L. 448       234  LOAD_FAST                'file'
              236  LOAD_METHOD              seek
              238  LOAD_FAST                'offset'
              240  LOAD_FAST                'total_sent'
              242  BINARY_ADD       
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          
            248_0  COME_FROM           232  '232'
            248_1  COME_FROM           222  '222'
              248  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 164

        def _check_sendfile_params(self, file, offset, count):
            if 'b' not in getattr(file, 'mode', 'b'):
                raise ValueError('file should be opened in binary mode')
            if not self.type & SOCK_STREAM:
                raise ValueError('only SOCK_STREAM type sockets are supported')
            if count is not None:
                if not isinstance(count, int):
                    raise TypeError('count must be a positive integer (got {!r})'.format(count))
                if count <= 0:
                    raise ValueError('count must be a positive integer (got {!r})'.format(count))

        def sendfile(self, file, offset=0, count=None):
            """sendfile(file[, offset[, count]]) -> sent

        Send a file until EOF is reached by using high-performance
        os.sendfile() and return the total number of bytes which
        were sent.
        *file* must be a regular file object opened in binary mode.
        If os.sendfile() is not available (e.g. Windows) or file is
        not a regular file socket.send() will be used instead.
        *offset* tells from where to start reading the file.
        If specified, *count* is the total number of bytes to transmit
        as opposed to sending the file until EOF is reached.
        File position is updated on return or also in case of error in
        which case file.tell() can be used to figure out the number of
        bytes which were sent.
        The socket must be of SOCK_STREAM type.
        Non-blocking sockets are not supported.
        """
            try:
                return self._sendfile_use_sendfile(file, offset, count)
            except _GiveupOnSendfile:
                return self._sendfile_use_send(file, offset, count)

        def _decref_socketios(self):
            if self._io_refs > 0:
                self._io_refs -= 1
            if self._closed:
                self.close()

        def _real_close(self, _ss=_socket.socket):
            _ss.close(self)

        def close(self):
            self._closed = True
            if self._io_refs <= 0:
                self._real_close()

        def detach(self):
            self._closed = True
            return super().detach()

        @property
        def family(self):
            return _intenum_converter(super().family, AddressFamily)

        @property
        def type(self):
            return _intenum_converter(super().type, SocketKind)

        if os.name == 'nt':

            def get_inheritable(self):
                return os.get_handle_inheritable(self.fileno())

            def set_inheritable(self, inheritable):
                os.set_handle_inheritable(self.fileno(), inheritable)

        else:

            def get_inheritable(self):
                return os.get_inheritable(self.fileno())

            def set_inheritable(self, inheritable):
                os.set_inheritable(self.fileno(), inheritable)

        get_inheritable.__doc__ = 'Get the inheritable flag of the socket'
        set_inheritable.__doc__ = 'Set the inheritable flag of the socket'


    def fromfd(fd, family, type, proto=0):
        """ fromfd(fd, family, type[, proto]) -> socket object

    Create a socket object from a duplicate of the given file
    descriptor.  The remaining arguments are the same as for socket().
    """
        nfd = dup(fd)
        return socketfamilytypeprotonfd


    if hasattr(_socket.socket, 'share'):

        def fromshare(info):
            """ fromshare(info) -> socket object

        Create a socket object from the bytes object returned by
        socket.share(pid).
        """
            return socket000info


        __all__.append('fromshare')
    if hasattr(_socket, 'socketpair'):

        def socketpair(family=None, type=SOCK_STREAM, proto=0):
            """socketpair([family[, type[, proto]]]) -> (socket object, socket object)

        Create a pair of socket objects from the sockets returned by the platform
        socketpair() function.
        The arguments are the same as for socket() except the default family is
        AF_UNIX if defined on the platform; otherwise, the default is AF_INET.
        """
            if family is None:
                try:
                    family = AF_UNIX
                except NameError:
                    family = AF_INET
                else:
                    a, b = _socket.socketpair(family, type, proto)
                    a = socketfamilytypeprotoa.detach()
                    b = socketfamilytypeprotob.detach()
                return (a, b)


    else:

        def socketpair(family=AF_INET, type=SOCK_STREAM, proto=0):
            if family == AF_INET:
                host = _LOCALHOST
            elif family == AF_INET6:
                host = _LOCALHOST_V6
            else:
                raise ValueError('Only AF_INET and AF_INET6 socket address families are supported')
            if type != SOCK_STREAM:
                raise ValueError('Only SOCK_STREAM socket type is supported')
            if proto != 0:
                raise ValueError('Only protocol zero is supported')
            lsock = socket(family, type, proto)
            try:
                lsock.bind((host, 0))
                lsock.listen()
                addr, port = lsock.getsockname()[:2]
                csock = socket(family, type, proto)
                try:
                    csock.setblocking(False)
                    try:
                        csock.connect((addr, port))
                    except (BlockingIOError, InterruptedError):
                        pass
                    else:
                        csock.setblocking(True)
                        ssock, _ = lsock.accept()
                except:
                    csock.close()
                    raise

            finally:
                lsock.close()

            return (ssock, csock)


        __all__.append('socketpair')
    socketpair.__doc__ = 'socketpair([family[, type[, proto]]]) -> (socket object, socket object)\nCreate a pair of socket objects from the sockets returned by the platform\nsocketpair() function.\nThe arguments are the same as for socket() except the default family is AF_UNIX\nif defined on the platform; otherwise, the default is AF_INET.\n'
    _blocking_errnos = {
     EAGAIN, EWOULDBLOCK}

    class SocketIO(io.RawIOBase):
        __doc__ = 'Raw I/O implementation for stream sockets.\n\n    This class supports the makefile() method on sockets.  It provides\n    the raw I/O interface on top of a socket object.\n    '

        def __init__(self, sock, mode):
            if mode not in ('r', 'w', 'rw', 'rb', 'wb', 'rwb'):
                raise ValueError('invalid mode: %r' % mode)
            io.RawIOBase.__init__(self)
            self._sock = sock
            if 'b' not in mode:
                mode += 'b'
            self._mode = mode
            self._reading = 'r' in mode
            self._writing = 'w' in mode
            self._timeout_occurred = False

        def readinto--- This code section failed: ---

 L. 663         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkClosed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 664         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _checkReadable
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 665        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _timeout_occurred
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 666        22  LOAD_GLOBAL              OSError
               24  LOAD_STR                 'cannot read from timed out object'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM           132  '132'
             30_1  COME_FROM           128  '128'
             30_2  COME_FROM            70  '70'
             30_3  COME_FROM            20  '20'

 L. 668        30  SETUP_FINALLY        46  'to 46'

 L. 669        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _sock
               36  LOAD_METHOD              recv_into
               38  LOAD_FAST                'b'
               40  CALL_METHOD_1         1  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    30  '30'

 L. 670        46  DUP_TOP          
               48  LOAD_GLOBAL              timeout
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    72  'to 72'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 671        60  LOAD_CONST               True
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _timeout_occurred

 L. 672        66  RAISE_VARARGS_0       0  'reraise'
               68  POP_EXCEPT       
               70  JUMP_BACK            30  'to 30'
             72_0  COME_FROM            52  '52'

 L. 673        72  DUP_TOP          
               74  LOAD_GLOBAL              error
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   130  'to 130'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       118  'to 118'

 L. 674        88  LOAD_FAST                'e'
               90  LOAD_ATTR                args
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  LOAD_GLOBAL              _blocking_errnos
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 675       102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        118  'to 118'
              108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM           100  '100'

 L. 676       112  RAISE_VARARGS_0       0  'reraise'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM           106  '106'
            118_1  COME_FROM_FINALLY    86  '86'
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_BACK            30  'to 30'
            130_0  COME_FROM            78  '78'
              130  END_FINALLY      
              132  JUMP_BACK            30  'to 30'

Parse error at or near `JUMP_BACK' instruction at offset 70

        def write--- This code section failed: ---

 L. 684         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkClosed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 685         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _checkWritable
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 686        16  SETUP_FINALLY        32  'to 32'

 L. 687        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _sock
               22  LOAD_METHOD              send
               24  LOAD_FAST                'b'
               26  CALL_METHOD_1         1  ''
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    16  '16'

 L. 688        32  DUP_TOP          
               34  LOAD_GLOBAL              error
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    90  'to 90'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY        78  'to 78'

 L. 690        48  LOAD_FAST                'e'
               50  LOAD_ATTR                args
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  LOAD_GLOBAL              _blocking_errnos
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 691        62  POP_BLOCK        
               64  POP_EXCEPT       
               66  CALL_FINALLY         78  'to 78'
               68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            60  '60'

 L. 692        72  RAISE_VARARGS_0       0  'reraise'
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM            66  '66'
             78_1  COME_FROM_FINALLY    46  '46'
               78  LOAD_CONST               None
               80  STORE_FAST               'e'
               82  DELETE_FAST              'e'
               84  END_FINALLY      
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            38  '38'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'

Parse error at or near `POP_EXCEPT' instruction at offset 64

        def readable(self):
            """True if the SocketIO is open for reading.
        """
            if self.closed:
                raise ValueError('I/O operation on closed socket.')
            return self._reading

        def writable(self):
            """True if the SocketIO is open for writing.
        """
            if self.closed:
                raise ValueError('I/O operation on closed socket.')
            return self._writing

        def seekable(self):
            if self.closed:
                raise ValueError('I/O operation on closed socket.')
            return super().seekable()

        def fileno(self):
            """Return the file descriptor of the underlying socket.
        """
            self._checkClosed()
            return self._sock.fileno()

        @property
        def name(self):
            if not self.closed:
                return self.fileno()
            return -1

        @property
        def mode(self):
            return self._mode

        def close(self):
            """Close the SocketIO object.  This doesn't close the underlying
        socket, except if all references to it have disappeared.
        """
            if self.closed:
                return
            io.RawIOBase.close(self)
            self._sock._decref_socketios()
            self._sock = None


    def getfqdn(name=''):
        """Get fully qualified domain name from name.

    An empty argument is interpreted as meaning the local host.

    First the hostname returned by gethostbyaddr() is checked, then
    possibly existing aliases. In case no FQDN is available, hostname
    from gethostname() is returned.
    """
        name = name.strip()
        if not name or name == '0.0.0.0':
            name = gethostname()
        try:
            hostname, aliases, ipaddrs = gethostbyaddr(name)
        except error:
            pass
        else:
            aliases.insert(0, hostname)
            for name in aliases:
                if '.' in name:
                    break
            else:
                name = hostname

        return name


    _GLOBAL_DEFAULT_TIMEOUT = object()

    def create_connection--- This code section failed: ---

 L. 785         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L. 786         8  LOAD_CONST               None
               10  STORE_FAST               'err'

 L. 787        12  LOAD_GLOBAL              getaddrinfo
               14  LOAD_FAST                'host'
               16  LOAD_FAST                'port'
               18  LOAD_CONST               0
               20  LOAD_GLOBAL              SOCK_STREAM
               22  CALL_FUNCTION_4       4  ''
               24  GET_ITER         
             26_0  COME_FROM           172  '172'
             26_1  COME_FROM           168  '168'
               26  FOR_ITER            174  'to 174'
               28  STORE_FAST               'res'

 L. 788        30  LOAD_FAST                'res'
               32  UNPACK_SEQUENCE_5     5 
               34  STORE_FAST               'af'
               36  STORE_FAST               'socktype'
               38  STORE_FAST               'proto'
               40  STORE_FAST               'canonname'
               42  STORE_FAST               'sa'

 L. 789        44  LOAD_CONST               None
               46  STORE_FAST               'sock'

 L. 790        48  SETUP_FINALLY       118  'to 118'

 L. 791        50  LOAD_GLOBAL              socket
               52  LOAD_FAST                'af'
               54  LOAD_FAST                'socktype'
               56  LOAD_FAST                'proto'
               58  CALL_FUNCTION_3       3  ''
               60  STORE_FAST               'sock'

 L. 792        62  LOAD_FAST                'timeout'
               64  LOAD_GLOBAL              _GLOBAL_DEFAULT_TIMEOUT
               66  COMPARE_OP               is-not
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 793        70  LOAD_FAST                'sock'
               72  LOAD_METHOD              settimeout
               74  LOAD_FAST                'timeout'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            68  '68'

 L. 794        80  LOAD_FAST                'source_address'
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 795        84  LOAD_FAST                'sock'
               86  LOAD_METHOD              bind
               88  LOAD_FAST                'source_address'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
             94_0  COME_FROM            82  '82'

 L. 796        94  LOAD_FAST                'sock'
               96  LOAD_METHOD              connect
               98  LOAD_FAST                'sa'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 798       104  LOAD_CONST               None
              106  STORE_FAST               'err'

 L. 799       108  LOAD_FAST                'sock'
              110  POP_BLOCK        
              112  ROT_TWO          
              114  POP_TOP          
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY    48  '48'

 L. 801       118  DUP_TOP          
              120  LOAD_GLOBAL              error
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   170  'to 170'
              126  POP_TOP          
              128  STORE_FAST               '_'
              130  POP_TOP          
              132  SETUP_FINALLY       158  'to 158'

 L. 802       134  LOAD_FAST                '_'
              136  STORE_FAST               'err'

 L. 803       138  LOAD_FAST                'sock'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   154  'to 154'

 L. 804       146  LOAD_FAST                'sock'
              148  LOAD_METHOD              close
              150  CALL_METHOD_0         0  ''
              152  POP_TOP          
            154_0  COME_FROM           144  '144'
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM_FINALLY   132  '132'
              158  LOAD_CONST               None
              160  STORE_FAST               '_'
              162  DELETE_FAST              '_'
              164  END_FINALLY      
              166  POP_EXCEPT       
              168  JUMP_BACK            26  'to 26'
            170_0  COME_FROM           124  '124'
              170  END_FINALLY      
              172  JUMP_BACK            26  'to 26'
            174_0  COME_FROM            26  '26'

 L. 806       174  LOAD_FAST                'err'
              176  LOAD_CONST               None
              178  COMPARE_OP               is-not
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L. 807       182  SETUP_FINALLY       192  'to 192'

 L. 808       184  LOAD_FAST                'err'
              186  RAISE_VARARGS_1       1  'exception instance'
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_FINALLY   182  '182'

 L. 811       192  LOAD_CONST               None
              194  STORE_FAST               'err'
              196  END_FINALLY      
              198  JUMP_FORWARD        208  'to 208'
            200_0  COME_FROM           180  '180'

 L. 813       200  LOAD_GLOBAL              error
              202  LOAD_STR                 'getaddrinfo returns an empty list'
              204  CALL_FUNCTION_1       1  ''
              206  RAISE_VARARGS_1       1  'exception instance'
            208_0  COME_FROM           198  '198'

Parse error at or near `ROT_TWO' instruction at offset 112


    def has_dualstack_ipv6--- This code section failed: ---

 L. 820         0  LOAD_GLOBAL              has_ipv6
                2  POP_JUMP_IF_FALSE    24  'to 24'

 L. 821         4  LOAD_GLOBAL              hasattr
                6  LOAD_GLOBAL              _socket
                8  LOAD_STR                 'IPPROTO_IPV6'
               10  CALL_FUNCTION_2       2  ''

 L. 820        12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 822        14  LOAD_GLOBAL              hasattr
               16  LOAD_GLOBAL              _socket
               18  LOAD_STR                 'IPV6_V6ONLY'
               20  CALL_FUNCTION_2       2  ''

 L. 820        22  POP_JUMP_IF_TRUE     28  'to 28'
             24_0  COME_FROM            12  '12'
             24_1  COME_FROM             2  '2'

 L. 823        24  LOAD_CONST               False
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 824        28  SETUP_FINALLY        82  'to 82'

 L. 825        30  LOAD_GLOBAL              socket
               32  LOAD_GLOBAL              AF_INET6
               34  LOAD_GLOBAL              SOCK_STREAM
               36  CALL_FUNCTION_2       2  ''
               38  SETUP_WITH           72  'to 72'
               40  STORE_FAST               'sock'

 L. 826        42  LOAD_FAST                'sock'
               44  LOAD_METHOD              setsockopt
               46  LOAD_GLOBAL              IPPROTO_IPV6
               48  LOAD_GLOBAL              IPV6_V6ONLY
               50  LOAD_CONST               0
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L. 827        56  POP_BLOCK        
               58  BEGIN_FINALLY    
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  POP_FINALLY           0  ''
               66  POP_BLOCK        
               68  LOAD_CONST               True
               70  RETURN_VALUE     
             72_0  COME_FROM_WITH       38  '38'
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  END_FINALLY      
               78  POP_BLOCK        
               80  JUMP_FORWARD        104  'to 104'
             82_0  COME_FROM_FINALLY    28  '28'

 L. 828        82  DUP_TOP          
               84  LOAD_GLOBAL              error
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   102  'to 102'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 829        96  POP_EXCEPT       
               98  LOAD_CONST               False
              100  RETURN_VALUE     
            102_0  COME_FROM            88  '88'
              102  END_FINALLY      
            104_0  COME_FROM            80  '80'

Parse error at or near `WITH_CLEANUP_START' instruction at offset 60


    def create_server(address, *, family=AF_INET, backlog=None, reuse_port=False, dualstack_ipv6=False):
        """Convenience function which creates a SOCK_STREAM type socket
    bound to *address* (a 2-tuple (host, port)) and return the socket
    object.

    *family* should be either AF_INET or AF_INET6.
    *backlog* is the queue size passed to socket.listen().
    *reuse_port* dictates whether to use the SO_REUSEPORT socket option.
    *dualstack_ipv6*: if true and the platform supports it, it will
    create an AF_INET6 socket able to accept both IPv4 or IPv6
    connections. When false it will explicitly disable this option on
    platforms that enable it by default (e.g. Linux).

    >>> with create_server((None, 8000)) as server:
    ...     while True:
    ...         conn, addr = server.accept()
    ...         # handle new connection
    """
        if reuse_port:
            if not hasattr(_socket, 'SO_REUSEPORT'):
                raise ValueError('SO_REUSEPORT not supported on this platform')
            if dualstack_ipv6:
                if not has_dualstack_ipv6():
                    raise ValueError('dualstack_ipv6 not supported on this platform')
                if family != AF_INET6:
                    raise ValueError('dualstack_ipv6 requires AF_INET6 family')
            sock = socket(family, SOCK_STREAM)
            try:
                if os.name not in ('nt', 'cygwin'):
                    if hasattr(_socket, 'SO_REUSEADDR'):
                        try:
                            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                        except error:
                            pass
                        else:
                            if reuse_port:
                                sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
                            if not has_ipv6 or family == AF_INET6:
                                if dualstack_ipv6:
                                    sock.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)
                                elif hasattr(_socket, 'IPV6_V6ONLY'):
                                    if hasattr(_socket, 'IPPROTO_IPV6'):
                                        sock.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 1)
                try:
                    sock.bind(address)
                except error as err:
                    try:
                        msg = '%s (while attempting to bind on address %r)' % (
                         err.strerror, address)
                        raise error(err.errno, msg) from None
                    finally:
                        err = None
                        del err

                if backlog is None:
                    sock.listen()
                else:
                    sock.listen(backlog)
                return sock
            except error:
                sock.close()
                raise


    def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        """Resolve host and port into list of address info entries.

    Translate the host/port argument into a sequence of 5-tuples that contain
    all the necessary arguments for creating a socket connected to that service.
    host is a domain name, a string representation of an IPv4/v6 address or
    None. port is a string service name such as 'http', a numeric port number or
    None. By passing None as the value of host and port, you can pass NULL to
    the underlying C API.

    The family, type and proto arguments can be optionally specified in order to
    narrow the list of addresses returned. Passing zero as a value for each of
    these arguments selects the full range of results.
    """
        addrlist = []
        for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
            af, socktype, proto, canonname, sa = res
            addrlist.append((_intenum_converter(af, AddressFamily),
             _intenum_converter(socktype, SocketKind),
             proto, canonname, sa))
        else:
            return addrlist