# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\trsock.py
import socket, warnings

class TransportSocket:
    __doc__ = 'A socket-like wrapper for exposing real transport sockets.\n\n    These objects can be safely returned by APIs like\n    `transport.get_extra_info(\'socket\')`.  All potentially disruptive\n    operations (like "socket.close()") are banned.\n    '
    __slots__ = ('_sock', )

    def __init__(self, sock: socket.socket):
        self._sock = sock

    def _na(self, what):
        warnings.warn(f"Using {what} on sockets returned from get_extra_info('socket') will be prohibited in asyncio 3.9. Please report your use case to bugs.python.org.",
          DeprecationWarning,
          source=self)

    @property
    def family(self):
        return self._sock.family

    @property
    def type(self):
        return self._sock.type

    @property
    def proto(self):
        return self._sock.proto

    def __repr__--- This code section failed: ---

 L.  40         0  LOAD_STR                 '<asyncio.TransportSocket fd='
                2  LOAD_FAST                'self'
                4  LOAD_METHOD              fileno
                6  CALL_METHOD_0         0  ''
                8  FORMAT_VALUE          0  ''
               10  LOAD_STR                 ', family='

 L.  41        12  LOAD_FAST                'self'
               14  LOAD_ATTR                family

 L.  40        16  FORMAT_VALUE          1  '!s'
               18  LOAD_STR                 ', type='

 L.  41        20  LOAD_FAST                'self'
               22  LOAD_ATTR                type

 L.  40        24  FORMAT_VALUE          1  '!s'
               26  LOAD_STR                 ', proto='

 L.  42        28  LOAD_FAST                'self'
               30  LOAD_ATTR                proto

 L.  40        32  FORMAT_VALUE          0  ''
               34  BUILD_STRING_8        8 

 L.  39        36  STORE_FAST               's'

 L.  45        38  LOAD_FAST                'self'
               40  LOAD_METHOD              fileno
               42  CALL_METHOD_0         0  ''
               44  LOAD_CONST               -1
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE   154  'to 154'

 L.  46        50  SETUP_FINALLY        82  'to 82'

 L.  47        52  LOAD_FAST                'self'
               54  LOAD_METHOD              getsockname
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'laddr'

 L.  48        60  LOAD_FAST                'laddr'
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L.  49        64  LOAD_FAST                's'
               66  FORMAT_VALUE          0  ''
               68  LOAD_STR                 ', laddr='
               70  LOAD_FAST                'laddr'
               72  FORMAT_VALUE          0  ''
               74  BUILD_STRING_3        3 
               76  STORE_FAST               's'
             78_0  COME_FROM            62  '62'
               78  POP_BLOCK        
               80  JUMP_FORWARD        102  'to 102'
             82_0  COME_FROM_FINALLY    50  '50'

 L.  50        82  DUP_TOP          
               84  LOAD_GLOBAL              socket
               86  LOAD_ATTR                error
               88  <121>               100  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.  51        96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            80  '80'

 L.  52       102  SETUP_FINALLY       134  'to 134'

 L.  53       104  LOAD_FAST                'self'
              106  LOAD_METHOD              getpeername
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'raddr'

 L.  54       112  LOAD_FAST                'raddr'
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.  55       116  LOAD_FAST                's'
              118  FORMAT_VALUE          0  ''
              120  LOAD_STR                 ', raddr='
              122  LOAD_FAST                'raddr'
              124  FORMAT_VALUE          0  ''
              126  BUILD_STRING_3        3 
              128  STORE_FAST               's'
            130_0  COME_FROM           114  '114'
              130  POP_BLOCK        
              132  JUMP_FORWARD        154  'to 154'
            134_0  COME_FROM_FINALLY   102  '102'

 L.  56       134  DUP_TOP          
              136  LOAD_GLOBAL              socket
              138  LOAD_ATTR                error
              140  <121>               152  ''
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.  57       148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
              152  <48>             
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           132  '132'
            154_2  COME_FROM            48  '48'

 L.  59       154  LOAD_FAST                's'
              156  FORMAT_VALUE          0  ''
              158  LOAD_STR                 '>'
              160  BUILD_STRING_2        2 
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 88

    def __getstate__(self):
        raise TypeError('Cannot serialize asyncio.TransportSocket object')

    def fileno(self):
        return self._sock.fileno

    def dup(self):
        return self._sock.dup

    def get_inheritable(self):
        return self._sock.get_inheritable

    def shutdown(self, how):
        self._sock.shutdown(how)

    def getsockopt--- This code section failed: ---

 L.  79         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  LOAD_ATTR                getsockopt
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kwargs'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def setsockopt--- This code section failed: ---

 L.  82         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sock
                4  LOAD_ATTR                setsockopt
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kwargs'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def getpeername(self):
        return self._sock.getpeername

    def getsockname(self):
        return self._sock.getsockname

    def getsockbyname(self):
        return self._sock.getsockbyname

    def accept(self):
        self._na('accept() method')
        return self._sock.accept

    def connect--- This code section failed: ---

 L.  98         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'connect() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  99        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                connect
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def connect_ex--- This code section failed: ---

 L. 102         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'connect_ex() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 103        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                connect_ex
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def bind--- This code section failed: ---

 L. 106         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'bind() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 107        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                bind
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def ioctl--- This code section failed: ---

 L. 110         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'ioctl() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 111        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                ioctl
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def listen--- This code section failed: ---

 L. 114         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'listen() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 115        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                listen
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def makefile(self):
        self._na('makefile() method')
        return self._sock.makefile

    def sendfile--- This code section failed: ---

 L. 122         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'sendfile() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 123        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                sendfile
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def close(self):
        self._na('close() method')
        return self._sock.close

    def detach(self):
        self._na('detach() method')
        return self._sock.detach

    def sendmsg_afalg--- This code section failed: ---

 L. 134         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'sendmsg_afalg() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 135        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                sendmsg_afalg
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def sendmsg--- This code section failed: ---

 L. 138         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'sendmsg() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 139        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                sendmsg
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def sendto--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'sendto() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 143        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                sendto
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def send--- This code section failed: ---

 L. 146         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'send() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 147        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                send
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def sendall--- This code section failed: ---

 L. 150         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'sendall() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 151        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                sendall
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def set_inheritable--- This code section failed: ---

 L. 154         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'set_inheritable() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 155        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                set_inheritable
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def share(self, process_id):
        self._na('share() method')
        return self._sock.share(process_id)

    def recv_into--- This code section failed: ---

 L. 162         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recv_into() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 163        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recv_into
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def recvfrom_into--- This code section failed: ---

 L. 166         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recvfrom_into() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 167        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recvfrom_into
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def recvmsg_into--- This code section failed: ---

 L. 170         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recvmsg_into() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 171        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recvmsg_into
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def recvmsg--- This code section failed: ---

 L. 174         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recvmsg() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 175        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recvmsg
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def recvfrom--- This code section failed: ---

 L. 178         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recvfrom() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 179        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recvfrom
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def recv--- This code section failed: ---

 L. 182         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _na
                4  LOAD_STR                 'recv() method'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 183        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _sock
               14  LOAD_ATTR                recv
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

    def settimeout(self, value):
        if value == 0:
            return
        raise ValueError('settimeout(): only 0 timeout is allowed on transport sockets')

    def gettimeout(self):
        return 0

    def setblocking(self, flag):
        if not flag:
            return
        raise ValueError('setblocking(): transport sockets cannot be blocking')

    def __enter__(self):
        self._na('context manager protocol')
        return self._sock.__enter__

    def __exit__(self, *err):
        self._na('context manager protocol')
        return (self._sock.__exit__)(*err)