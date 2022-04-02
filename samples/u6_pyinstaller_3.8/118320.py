# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymysql\_socketio.py
"""
SocketIO imported from socket module in Python 3.

Copyright (c) 2001-2013 Python Software Foundation; All Rights Reserved.
"""
from socket import *
import io, errno
__all__ = [
 'SocketIO']
EINTR = errno.EINTR
_blocking_errnos = (errno.EAGAIN, errno.EWOULDBLOCK)

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

 L.  53         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkClosed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  54         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _checkReadable
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L.  55        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _timeout_occurred
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.  56        22  LOAD_GLOBAL              IOError
               24  LOAD_STR                 'cannot read from timed out object'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.  58        30  SETUP_FINALLY        46  'to 46'

 L.  59        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _sock
               36  LOAD_METHOD              recv_into
               38  LOAD_FAST                'b'
               40  CALL_METHOD_1         1  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    30  '30'

 L.  60        46  DUP_TOP          
               48  LOAD_GLOBAL              timeout
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    72  'to 72'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  61        60  LOAD_CONST               True
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _timeout_occurred

 L.  62        66  RAISE_VARARGS_0       0  'reraise'
               68  POP_EXCEPT       
               70  JUMP_BACK            30  'to 30'
             72_0  COME_FROM            52  '52'

 L.  63        72  DUP_TOP          
               74  LOAD_GLOBAL              error
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   150  'to 150'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       138  'to 138'

 L.  64        88  LOAD_FAST                'e'
               90  LOAD_ATTR                args
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  STORE_FAST               'n'

 L.  65        98  LOAD_FAST                'n'
              100  LOAD_GLOBAL              EINTR
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L.  66       106  POP_BLOCK        
              108  POP_EXCEPT       
              110  CALL_FINALLY        138  'to 138'
              112  JUMP_BACK            30  'to 30'
            114_0  COME_FROM           104  '104'

 L.  67       114  LOAD_FAST                'n'
              116  LOAD_GLOBAL              _blocking_errnos
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L.  68       122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        138  'to 138'
              128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM           120  '120'

 L.  69       132  RAISE_VARARGS_0       0  'reraise'
              134  POP_BLOCK        
              136  BEGIN_FINALLY    
            138_0  COME_FROM           126  '126'
            138_1  COME_FROM           110  '110'
            138_2  COME_FROM_FINALLY    86  '86'
              138  LOAD_CONST               None
              140  STORE_FAST               'e'
              142  DELETE_FAST              'e'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_BACK            30  'to 30'
            150_0  COME_FROM            78  '78'
              150  END_FINALLY      
              152  JUMP_BACK            30  'to 30'

Parse error at or near `POP_TOP' instruction at offset 56

    def write--- This code section failed: ---

 L.  77         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkClosed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  78         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _checkWritable
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L.  79        16  SETUP_FINALLY        32  'to 32'

 L.  80        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _sock
               22  LOAD_METHOD              send
               24  LOAD_FAST                'b'
               26  CALL_METHOD_1         1  ''
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    16  '16'

 L.  81        32  DUP_TOP          
               34  LOAD_GLOBAL              error
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    90  'to 90'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY        78  'to 78'

 L.  83        48  LOAD_FAST                'e'
               50  LOAD_ATTR                args
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  LOAD_GLOBAL              _blocking_errnos
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L.  84        62  POP_BLOCK        
               64  POP_EXCEPT       
               66  CALL_FINALLY         78  'to 78'
               68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            60  '60'

 L.  85        72  RAISE_VARARGS_0       0  'reraise'
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
        return super().seekable

    def fileno(self):
        """Return the file descriptor of the underlying socket.
        """
        self._checkClosed
        return self._sock.fileno

    @property
    def name(self):
        if not self.closed:
            return self.fileno
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
        self._sock._decref_socketios
        self._sock = None