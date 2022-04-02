# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: socks.py
from base64 import b64encode
try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable
else:
    from errno import EOPNOTSUPP, EINVAL, EAGAIN
    import functools
    from io import BytesIO
    import logging, os
    from os import SEEK_CUR
    import socket, struct, sys
    __version__ = '1.7.1'
    if os.name == 'nt':
        if sys.version_info < (3, 0):
            try:
                import win_inet_pton
            except ImportError:
                raise ImportError('To run PySocks on Windows you must install win_inet_pton')

    log = logging.getLogger(__name__)
    PROXY_TYPE_SOCKS4 = SOCKS4 = 1
    PROXY_TYPE_SOCKS5 = SOCKS5 = 2
    PROXY_TYPE_HTTP = HTTP = 3
    PROXY_TYPES = {'SOCKS4':SOCKS4, 
     'SOCKS5':SOCKS5,  'HTTP':HTTP}
    PRINTABLE_PROXY_TYPES = dict(zip(PROXY_TYPES.values(), PROXY_TYPES.keys()))
    _orgsocket = _orig_socket = socket.socket

    def set_self_blocking(function):

        @functools.wraps(function)
        def wrapper--- This code section failed: ---

 L.  42         0  LOAD_FAST                'args'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'self'

 L.  43         8  SETUP_FINALLY        94  'to 94'
               10  SETUP_FINALLY        54  'to 54'

 L.  44        12  LOAD_FAST                'self'
               14  LOAD_METHOD              gettimeout
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               '_is_blocking'

 L.  45        20  LOAD_FAST                '_is_blocking'
               22  LOAD_CONST               0
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  46        28  LOAD_FAST                'self'
               30  LOAD_METHOD              setblocking
               32  LOAD_CONST               True
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            26  '26'

 L.  47        38  LOAD_DEREF               'function'
               40  LOAD_FAST                'args'
               42  LOAD_FAST                'kwargs'
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  POP_BLOCK        
               48  POP_BLOCK        
               50  CALL_FINALLY         94  'to 94'
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    10  '10'

 L.  48        54  DUP_TOP          
               56  LOAD_GLOBAL              Exception
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    88  'to 88'
               62  POP_TOP          
               64  STORE_FAST               'e'
               66  POP_TOP          
               68  SETUP_FINALLY        76  'to 76'

 L.  49        70  RAISE_VARARGS_0       0  'reraise'
               72  POP_BLOCK        
               74  BEGIN_FINALLY    
             76_0  COME_FROM_FINALLY    68  '68'
               76  LOAD_CONST               None
               78  STORE_FAST               'e'
               80  DELETE_FAST              'e'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            60  '60'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM            50  '50'
             94_1  COME_FROM_FINALLY     8  '8'

 L.  52        94  LOAD_FAST                '_is_blocking'
               96  LOAD_CONST               0
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L.  53       102  LOAD_FAST                'self'
              104  LOAD_METHOD              setblocking
              106  LOAD_CONST               False
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'
              112  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 48

        return wrapper


    class ProxyError(IOError):
        __doc__ = 'Socket_err contains original socket.error exception.'

        def __init__(self, msg, socket_err=None):
            self.msg = msg
            self.socket_err = socket_err
            if socket_err:
                self.msg += ': {}'.format(socket_err)

        def __str__(self):
            return self.msg


    class GeneralProxyError(ProxyError):
        pass


    class ProxyConnectionError(ProxyError):
        pass


    class SOCKS5AuthError(ProxyError):
        pass


    class SOCKS5Error(ProxyError):
        pass


    class SOCKS4Error(ProxyError):
        pass


    class HTTPError(ProxyError):
        pass


    SOCKS4_ERRORS = {91:'Request rejected or failed', 
     92:'Request rejected because SOCKS server cannot connect to identd on the client', 
     93:'Request rejected because the client program and identd report different user-ids'}
    SOCKS5_ERRORS = {1:'General SOCKS server failure', 
     2:'Connection not allowed by ruleset', 
     3:'Network unreachable', 
     4:'Host unreachable', 
     5:'Connection refused', 
     6:'TTL expired', 
     7:'Command not supported, or protocol error', 
     8:'Address type not supported'}
    DEFAULT_PORTS = {SOCKS4: 1080, SOCKS5: 1080, HTTP: 8080}

    def set_default_proxy(proxy_type=None, addr=None, port=None, rdns=True, username=None, password=None):
        """Sets a default proxy.

    All further socksocket objects will use the default unless explicitly
    changed. All parameters are as for socket.set_proxy()."""
        socksocket.default_proxy = (
         proxy_type, addr, port, rdns,
         username.encode() if username else None,
         password.encode() if password else None)


    def setdefaultproxy(*args, **kwargs):
        if 'proxytype' in kwargs:
            kwargs['proxy_type'] = kwargs.pop('proxytype')
        return set_default_proxy(*args, **kwargs)


    def get_default_proxy():
        """Returns the default proxy, set by set_default_proxy."""
        return socksocket.default_proxy


    getdefaultproxy = get_default_proxy

    def wrap_module(module):
        """Attempts to replace a module's socket library with a SOCKS socket.

    Must set a default proxy using set_default_proxy(...) first. This will
    only work on modules that import socket directly into the namespace;
    most of the Python Standard Library falls into this category."""
        if socksocket.default_proxy:
            module.socket.socket = socksocket
        else:
            raise GeneralProxyError('No default proxy specified')


    wrapmodule = wrap_module

    def create_connection--- This code section failed: ---

 L. 171         0  LOAD_FAST                'dest_pair'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'remote_host'
                6  STORE_FAST               'remote_port'

 L. 172         8  LOAD_FAST                'remote_host'
               10  LOAD_METHOD              startswith
               12  LOAD_STR                 '['
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 173        18  LOAD_FAST                'remote_host'
               20  LOAD_METHOD              strip
               22  LOAD_STR                 '[]'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'remote_host'
             28_0  COME_FROM            16  '16'

 L. 174        28  LOAD_FAST                'proxy_addr'
               30  POP_JUMP_IF_FALSE    52  'to 52'
               32  LOAD_FAST                'proxy_addr'
               34  LOAD_METHOD              startswith
               36  LOAD_STR                 '['
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 175        42  LOAD_FAST                'proxy_addr'
               44  LOAD_METHOD              strip
               46  LOAD_STR                 '[]'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'proxy_addr'
             52_0  COME_FROM            40  '40'
             52_1  COME_FROM            30  '30'

 L. 177        52  LOAD_CONST               None
               54  STORE_FAST               'err'

 L. 180        56  LOAD_GLOBAL              socket
               58  LOAD_METHOD              getaddrinfo
               60  LOAD_FAST                'proxy_addr'
               62  LOAD_FAST                'proxy_port'
               64  LOAD_CONST               0
               66  LOAD_GLOBAL              socket
               68  LOAD_ATTR                SOCK_STREAM
               70  CALL_METHOD_4         4  ''
               72  GET_ITER         
               74  FOR_ITER            286  'to 286'
               76  STORE_FAST               'r'

 L. 181        78  LOAD_FAST                'r'
               80  UNPACK_SEQUENCE_5     5 
               82  STORE_FAST               'family'
               84  STORE_FAST               'socket_type'
               86  STORE_FAST               'proto'
               88  STORE_FAST               'canonname'
               90  STORE_FAST               'sa'

 L. 182        92  LOAD_CONST               None
               94  STORE_FAST               'sock'

 L. 183        96  SETUP_FINALLY       220  'to 220'

 L. 184        98  LOAD_GLOBAL              socksocket
              100  LOAD_FAST                'family'
              102  LOAD_FAST                'socket_type'
              104  LOAD_FAST                'proto'
              106  CALL_FUNCTION_3       3  ''
              108  STORE_FAST               'sock'

 L. 186       110  LOAD_FAST                'socket_options'
              112  POP_JUMP_IF_FALSE   134  'to 134'

 L. 187       114  LOAD_FAST                'socket_options'
              116  GET_ITER         
              118  FOR_ITER            134  'to 134'
              120  STORE_FAST               'opt'

 L. 188       122  LOAD_FAST                'sock'
              124  LOAD_ATTR                setsockopt
              126  LOAD_FAST                'opt'
              128  CALL_FUNCTION_EX      0  'positional arguments only'
              130  POP_TOP          
              132  JUMP_BACK           118  'to 118'
            134_0  COME_FROM           112  '112'

 L. 190       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'timeout'
              138  LOAD_GLOBAL              int
              140  LOAD_GLOBAL              float
              142  BUILD_TUPLE_2         2 
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L. 191       148  LOAD_FAST                'sock'
              150  LOAD_METHOD              settimeout
              152  LOAD_FAST                'timeout'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
            158_0  COME_FROM           146  '146'

 L. 193       158  LOAD_FAST                'proxy_type'
              160  POP_JUMP_IF_FALSE   182  'to 182'

 L. 194       162  LOAD_FAST                'sock'
              164  LOAD_METHOD              set_proxy
              166  LOAD_FAST                'proxy_type'
              168  LOAD_FAST                'proxy_addr'
              170  LOAD_FAST                'proxy_port'
              172  LOAD_FAST                'proxy_rdns'

 L. 195       174  LOAD_FAST                'proxy_username'

 L. 195       176  LOAD_FAST                'proxy_password'

 L. 194       178  CALL_METHOD_6         6  ''
              180  POP_TOP          
            182_0  COME_FROM           160  '160'

 L. 196       182  LOAD_FAST                'source_address'
              184  POP_JUMP_IF_FALSE   196  'to 196'

 L. 197       186  LOAD_FAST                'sock'
              188  LOAD_METHOD              bind
              190  LOAD_FAST                'source_address'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           184  '184'

 L. 199       196  LOAD_FAST                'sock'
              198  LOAD_METHOD              connect
              200  LOAD_FAST                'remote_host'
              202  LOAD_FAST                'remote_port'
              204  BUILD_TUPLE_2         2 
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 200       210  LOAD_FAST                'sock'
              212  POP_BLOCK        
              214  ROT_TWO          
              216  POP_TOP          
              218  RETURN_VALUE     
            220_0  COME_FROM_FINALLY    96  '96'

 L. 202       220  DUP_TOP          
              222  LOAD_GLOBAL              socket
              224  LOAD_ATTR                error
              226  LOAD_GLOBAL              ProxyError
              228  BUILD_TUPLE_2         2 
              230  COMPARE_OP               exception-match
          232_234  POP_JUMP_IF_FALSE   282  'to 282'
              236  POP_TOP          
              238  STORE_FAST               'e'
              240  POP_TOP          
              242  SETUP_FINALLY       270  'to 270'

 L. 203       244  LOAD_FAST                'e'
              246  STORE_FAST               'err'

 L. 204       248  LOAD_FAST                'sock'
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L. 205       254  LOAD_FAST                'sock'
              256  LOAD_METHOD              close
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          

 L. 206       262  LOAD_CONST               None
              264  STORE_FAST               'sock'
            266_0  COME_FROM           250  '250'
              266  POP_BLOCK        
              268  BEGIN_FINALLY    
            270_0  COME_FROM_FINALLY   242  '242'
              270  LOAD_CONST               None
              272  STORE_FAST               'e'
              274  DELETE_FAST              'e'
              276  END_FINALLY      
              278  POP_EXCEPT       
              280  JUMP_BACK            74  'to 74'
            282_0  COME_FROM           232  '232'
              282  END_FINALLY      
              284  JUMP_BACK            74  'to 74'

 L. 208       286  LOAD_FAST                'err'
          288_290  POP_JUMP_IF_FALSE   296  'to 296'

 L. 209       292  LOAD_FAST                'err'
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           288  '288'

 L. 211       296  LOAD_GLOBAL              socket
              298  LOAD_METHOD              error
              300  LOAD_STR                 'gai returned empty list.'
              302  CALL_METHOD_1         1  ''
              304  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 214


    class _BaseSocket(socket.socket):
        __doc__ = 'Allows Python 2 delegated methods such as send() to be overridden.'

        def __init__(self, *pos, **kw):
            (_orig_socket.__init__)(self, *pos, **kw)
            self._savedmethods = dict()
            for name in self._savenames:
                self._savedmethods[name] = getattr(self, name)
                delattr(self, name)

        _savenames = list()


    def _makemethod(name):
        return lambda self, *pos, **kw: (self._savedmethods[name])(*pos, **kw)


    for name in ('sendto', 'send', 'recvfrom', 'recv'):
        method = getattr(_BaseSocket, name, None)
        if not isinstance(method, Callable):
            _BaseSocket._savenames.append(name)
            setattr(_BaseSocket, name, _makemethod(name))

        class socksocket(_BaseSocket):
            __doc__ = 'socksocket([family[, type[, proto]]]) -> socket object\n\n    Open a SOCKS enabled socket. The parameters are the same as\n    those of the standard socket init. In order for SOCKS to work,\n    you must specify family=AF_INET and proto=0.\n    The "type" argument must be either SOCK_STREAM or SOCK_DGRAM.\n    '
            default_proxy = None

            def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, *args, **kwargs):
                if type not in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
                    msg = 'Socket type must be stream or datagram, not {!r}'
                    raise ValueError(msg.format(type))
                else:
                    (super(socksocket, self).__init__)(family, type, proto, *args, **kwargs)
                    self._proxyconn = None
                    if self.default_proxy:
                        self.proxy = self.default_proxy
                    else:
                        self.proxy = (None, None, None, None, None, None)
                self.proxy_sockname = None
                self.proxy_peername = None
                self._timeout = None

            def _readall(self, file, count):
                """Receive EXACTLY the number of bytes requested from the file object.

        Blocks until the required number of bytes have been received."""
                data = b''
                while len(data) < count:
                    d = file.read(count - len(data))
                    if not d:
                        raise GeneralProxyError('Connection closed unexpectedly')
                    data += d

                return data

            def settimeout(self, timeout):
                self._timeout = timeout
                try:
                    peer = self.get_proxy_peername()
                    super(socksocket, self).settimeout(self._timeout)
                except socket.error:
                    pass

            def gettimeout(self):
                return self._timeout

            def setblocking(self, v):
                if v:
                    self.settimeout(None)
                else:
                    self.settimeout(0.0)

            def set_proxy(self, proxy_type=None, addr=None, port=None, rdns=True, username=None, password=None):
                """ Sets the proxy to be used.

        proxy_type -  The type of the proxy to be used. Three types
                        are supported: PROXY_TYPE_SOCKS4 (including socks4a),
                        PROXY_TYPE_SOCKS5 and PROXY_TYPE_HTTP
        addr -        The address of the server (IP or DNS).
        port -        The port of the server. Defaults to 1080 for SOCKS
                        servers and 8080 for HTTP proxy servers.
        rdns -        Should DNS queries be performed on the remote side
                       (rather than the local side). The default is True.
                       Note: This has no effect with SOCKS4 servers.
        username -    Username to authenticate with to the server.
                       The default is no authentication.
        password -    Password to authenticate with to the server.
                       Only relevant when username is also provided."""
                self.proxy = (
                 proxy_type, addr, port, rdns,
                 username.encode() if username else None,
                 password.encode() if password else None)

            def setproxy(self, *args, **kwargs):
                if 'proxytype' in kwargs:
                    kwargs['proxy_type'] = kwargs.pop('proxytype')
                return (self.set_proxy)(*args, **kwargs)

            def bind(self, *pos, **kw):
                proxy_type, proxy_addr, proxy_port, rdns, username, password = self.proxy
                if not proxy_type or self.type != socket.SOCK_DGRAM:
                    return (_orig_socket.bind)(self, *pos, **kw)
                if self._proxyconn:
                    raise socket.error(EINVAL, 'Socket already bound to an address')
                if proxy_type != SOCKS5:
                    msg = 'UDP only supported by SOCKS5 proxy type'
                    raise socket.error(EOPNOTSUPP, msg)
                (super(socksocket, self).bind)(*pos, **kw)
                _, port = self.getsockname()
                dst = ('0', port)
                self._proxyconn = _orig_socket()
                proxy = self._proxy_addr()
                self._proxyconn.connect(proxy)
                UDP_ASSOCIATE = b'\x03'
                _, relay = self._SOCKS5_request(self._proxyconn, UDP_ASSOCIATE, dst)
                host, _ = proxy
                _, port = relay
                super(socksocket, self).connect((host, port))
                super(socksocket, self).settimeout(self._timeout)
                self.proxy_sockname = ('0.0.0.0', 0)

            def sendto(self, bytes, *args, **kwargs):
                if self.type != socket.SOCK_DGRAM:
                    return (super(socksocket, self).sendto)(bytes, *args, **kwargs)
                if not self._proxyconn:
                    self.bind(('', 0))
                address = args[(-1)]
                flags = args[:-1]
                header = BytesIO()
                RSV = b'\x00\x00'
                header.write(RSV)
                STANDALONE = b'\x00'
                header.write(STANDALONE)
                self._write_SOCKS5_address(address, header)
                sent = (super(socksocket, self).send)(header.getvalue() + bytes, *flags, **kwargs)
                return sent - header.tell()

            def send(self, bytes, flags=0, **kwargs):
                if self.type == socket.SOCK_DGRAM:
                    return (self.sendto)(bytes, flags, (self.proxy_peername), **kwargs)
                return (super(socksocket, self).send)(bytes, flags, **kwargs)

            def recvfrom(self, bufsize, flags=0):
                if self.type != socket.SOCK_DGRAM:
                    return super(socksocket, self).recvfrom(bufsize, flags)
                else:
                    if not self._proxyconn:
                        self.bind(('', 0))
                    buf = BytesIO(super(socksocket, self).recv(bufsize + 1024, flags))
                    buf.seek(2, SEEK_CUR)
                    frag = buf.read(1)
                    if ord(frag):
                        raise NotImplementedError('Received UDP packet fragment')
                    fromhost, fromport = self._read_SOCKS5_address(buf)
                    if self.proxy_peername:
                        peerhost, peerport = self.proxy_peername
                        if fromhost != peerhost or peerport not in (0, fromport):
                            raise socket.error(EAGAIN, 'Packet filtered')
                return (
                 buf.read(bufsize), (fromhost, fromport))

            def recv(self, *pos, **kw):
                bytes, _ = (self.recvfrom)(*pos, **kw)
                return bytes

            def close(self):
                if self._proxyconn:
                    self._proxyconn.close()
                return super(socksocket, self).close()

            def get_proxy_sockname(self):
                """Returns the bound IP address and port number at the proxy."""
                return self.proxy_sockname

            getproxysockname = get_proxy_sockname

            def get_proxy_peername(self):
                """
        Returns the IP and port number of the proxy.
        """
                return self.getpeername()

            getproxypeername = get_proxy_peername

            def get_peername(self):
                """Returns the IP address and port number of the destination machine.

        Note: get_proxy_peername returns the proxy."""
                return self.proxy_peername

            getpeername = get_peername

            def _negotiate_SOCKS5(self, *dest_addr):
                """Negotiates a stream connection through a SOCKS5 server."""
                CONNECT = b'\x01'
                self.proxy_peername, self.proxy_sockname = self._SOCKS5_request(self, CONNECT, dest_addr)

            def _SOCKS5_request--- This code section failed: ---

 L. 451         0  LOAD_FAST                'self'
                2  LOAD_ATTR                proxy
                4  UNPACK_SEQUENCE_6     6 
                6  STORE_FAST               'proxy_type'
                8  STORE_FAST               'addr'
               10  STORE_FAST               'port'
               12  STORE_FAST               'rdns'
               14  STORE_FAST               'username'
               16  STORE_FAST               'password'

 L. 453        18  LOAD_FAST                'conn'
               20  LOAD_METHOD              makefile
               22  LOAD_STR                 'wb'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'writer'

 L. 454        28  LOAD_FAST                'conn'
               30  LOAD_METHOD              makefile
               32  LOAD_STR                 'rb'
               34  LOAD_CONST               0
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'reader'

 L. 455     40_42  SETUP_FINALLY       498  'to 498'

 L. 457        44  LOAD_FAST                'username'
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_FAST                'password'
               50  POP_JUMP_IF_FALSE    64  'to 64'

 L. 461        52  LOAD_FAST                'writer'
               54  LOAD_METHOD              write
               56  LOAD_CONST               b'\x05\x02\x00\x02'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_FORWARD         74  'to 74'
             64_0  COME_FROM            50  '50'
             64_1  COME_FROM            46  '46'

 L. 465        64  LOAD_FAST                'writer'
               66  LOAD_METHOD              write
               68  LOAD_CONST               b'\x05\x01\x00'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            62  '62'

 L. 469        74  LOAD_FAST                'writer'
               76  LOAD_METHOD              flush
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          

 L. 470        82  LOAD_FAST                'self'
               84  LOAD_METHOD              _readall
               86  LOAD_FAST                'reader'
               88  LOAD_CONST               2
               90  CALL_METHOD_2         2  ''
               92  STORE_FAST               'chosen_auth'

 L. 472        94  LOAD_FAST                'chosen_auth'
               96  LOAD_CONST               0
               98  LOAD_CONST               1
              100  BUILD_SLICE_2         2 
              102  BINARY_SUBSCR    
              104  LOAD_CONST               b'\x05'
              106  COMPARE_OP               !=
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 475       110  LOAD_GLOBAL              GeneralProxyError

 L. 476       112  LOAD_STR                 'SOCKS5 proxy server sent invalid data'

 L. 475       114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           108  '108'

 L. 480       118  LOAD_FAST                'chosen_auth'
              120  LOAD_CONST               1
              122  LOAD_CONST               2
              124  BUILD_SLICE_2         2 
              126  BINARY_SUBSCR    
              128  LOAD_CONST               b'\x02'
              130  COMPARE_OP               ==
          132_134  POP_JUMP_IF_FALSE   274  'to 274'

 L. 483       136  LOAD_FAST                'username'
              138  POP_JUMP_IF_FALSE   144  'to 144'
              140  LOAD_FAST                'password'
              142  POP_JUMP_IF_TRUE    152  'to 152'
            144_0  COME_FROM           138  '138'

 L. 487       144  LOAD_GLOBAL              SOCKS5AuthError
              146  LOAD_STR                 'No username/password supplied. Server requested username/password authentication'
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           142  '142'

 L. 491       152  LOAD_FAST                'writer'
              154  LOAD_METHOD              write
              156  LOAD_CONST               b'\x01'
              158  LOAD_GLOBAL              chr
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'username'
              164  CALL_FUNCTION_1       1  ''
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_METHOD              encode
              170  CALL_METHOD_0         0  ''
              172  BINARY_ADD       

 L. 492       174  LOAD_FAST                'username'

 L. 491       176  BINARY_ADD       

 L. 493       178  LOAD_GLOBAL              chr
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'password'
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_METHOD              encode
              190  CALL_METHOD_0         0  ''

 L. 491       192  BINARY_ADD       

 L. 494       194  LOAD_FAST                'password'

 L. 491       196  BINARY_ADD       
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 495       202  LOAD_FAST                'writer'
              204  LOAD_METHOD              flush
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          

 L. 496       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _readall
              214  LOAD_FAST                'reader'
              216  LOAD_CONST               2
              218  CALL_METHOD_2         2  ''
              220  STORE_FAST               'auth_status'

 L. 497       222  LOAD_FAST                'auth_status'
              224  LOAD_CONST               0
              226  LOAD_CONST               1
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  LOAD_CONST               b'\x01'
              234  COMPARE_OP               !=
              236  POP_JUMP_IF_FALSE   246  'to 246'

 L. 499       238  LOAD_GLOBAL              GeneralProxyError

 L. 500       240  LOAD_STR                 'SOCKS5 proxy server sent invalid data'

 L. 499       242  CALL_FUNCTION_1       1  ''
              244  RAISE_VARARGS_1       1  'exception instance'
            246_0  COME_FROM           236  '236'

 L. 501       246  LOAD_FAST                'auth_status'
              248  LOAD_CONST               1
              250  LOAD_CONST               2
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  LOAD_CONST               b'\x00'
              258  COMPARE_OP               !=
          260_262  POP_JUMP_IF_FALSE   328  'to 328'

 L. 503       264  LOAD_GLOBAL              SOCKS5AuthError
              266  LOAD_STR                 'SOCKS5 authentication failed'
              268  CALL_FUNCTION_1       1  ''
              270  RAISE_VARARGS_1       1  'exception instance'
              272  JUMP_FORWARD        328  'to 328'
            274_0  COME_FROM           132  '132'

 L. 508       274  LOAD_FAST                'chosen_auth'
              276  LOAD_CONST               1
              278  LOAD_CONST               2
              280  BUILD_SLICE_2         2 
              282  BINARY_SUBSCR    
              284  LOAD_CONST               b'\x00'
              286  COMPARE_OP               !=
          288_290  POP_JUMP_IF_FALSE   328  'to 328'

 L. 510       292  LOAD_FAST                'chosen_auth'
              294  LOAD_CONST               1
              296  LOAD_CONST               2
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  LOAD_CONST               b'\xff'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   320  'to 320'

 L. 511       310  LOAD_GLOBAL              SOCKS5AuthError

 L. 512       312  LOAD_STR                 'All offered SOCKS5 authentication methods were rejected'

 L. 511       314  CALL_FUNCTION_1       1  ''
              316  RAISE_VARARGS_1       1  'exception instance'
              318  JUMP_FORWARD        328  'to 328'
            320_0  COME_FROM           306  '306'

 L. 515       320  LOAD_GLOBAL              GeneralProxyError

 L. 516       322  LOAD_STR                 'SOCKS5 proxy server sent invalid data'

 L. 515       324  CALL_FUNCTION_1       1  ''
              326  RAISE_VARARGS_1       1  'exception instance'
            328_0  COME_FROM           318  '318'
            328_1  COME_FROM           288  '288'
            328_2  COME_FROM           272  '272'
            328_3  COME_FROM           260  '260'

 L. 519       328  LOAD_FAST                'writer'
              330  LOAD_METHOD              write
              332  LOAD_CONST               b'\x05'
              334  LOAD_FAST                'cmd'
              336  BINARY_ADD       
              338  LOAD_CONST               b'\x00'
              340  BINARY_ADD       
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L. 520       346  LOAD_FAST                'self'
              348  LOAD_METHOD              _write_SOCKS5_address
              350  LOAD_FAST                'dst'
              352  LOAD_FAST                'writer'
              354  CALL_METHOD_2         2  ''
              356  STORE_FAST               'resolved'

 L. 521       358  LOAD_FAST                'writer'
              360  LOAD_METHOD              flush
              362  CALL_METHOD_0         0  ''
              364  POP_TOP          

 L. 524       366  LOAD_FAST                'self'
              368  LOAD_METHOD              _readall
              370  LOAD_FAST                'reader'
              372  LOAD_CONST               3
              374  CALL_METHOD_2         2  ''
              376  STORE_FAST               'resp'

 L. 525       378  LOAD_FAST                'resp'
              380  LOAD_CONST               0
              382  LOAD_CONST               1
              384  BUILD_SLICE_2         2 
              386  BINARY_SUBSCR    
              388  LOAD_CONST               b'\x05'
              390  COMPARE_OP               !=
          392_394  POP_JUMP_IF_FALSE   404  'to 404'

 L. 526       396  LOAD_GLOBAL              GeneralProxyError

 L. 527       398  LOAD_STR                 'SOCKS5 proxy server sent invalid data'

 L. 526       400  CALL_FUNCTION_1       1  ''
              402  RAISE_VARARGS_1       1  'exception instance'
            404_0  COME_FROM           392  '392'

 L. 529       404  LOAD_GLOBAL              ord
              406  LOAD_FAST                'resp'
              408  LOAD_CONST               1
              410  LOAD_CONST               2
              412  BUILD_SLICE_2         2 
              414  BINARY_SUBSCR    
              416  CALL_FUNCTION_1       1  ''
              418  STORE_FAST               'status'

 L. 530       420  LOAD_FAST                'status'
              422  LOAD_CONST               0
              424  COMPARE_OP               !=
          426_428  POP_JUMP_IF_FALSE   458  'to 458'

 L. 532       430  LOAD_GLOBAL              SOCKS5_ERRORS
              432  LOAD_METHOD              get
              434  LOAD_FAST                'status'
              436  LOAD_STR                 'Unknown error'
              438  CALL_METHOD_2         2  ''
              440  STORE_FAST               'error'

 L. 533       442  LOAD_GLOBAL              SOCKS5Error
              444  LOAD_STR                 '{:#04x}: {}'
              446  LOAD_METHOD              format
              448  LOAD_FAST                'status'
              450  LOAD_FAST                'error'
              452  CALL_METHOD_2         2  ''
              454  CALL_FUNCTION_1       1  ''
              456  RAISE_VARARGS_1       1  'exception instance'
            458_0  COME_FROM           426  '426'

 L. 536       458  LOAD_FAST                'self'
              460  LOAD_METHOD              _read_SOCKS5_address
              462  LOAD_FAST                'reader'
              464  CALL_METHOD_1         1  ''
              466  STORE_FAST               'bnd'

 L. 538       468  LOAD_GLOBAL              super
              470  LOAD_GLOBAL              socksocket
              472  LOAD_FAST                'self'
              474  CALL_FUNCTION_2       2  ''
              476  LOAD_METHOD              settimeout
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                _timeout
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          

 L. 539       486  LOAD_FAST                'resolved'
              488  LOAD_FAST                'bnd'
              490  BUILD_TUPLE_2         2 
              492  POP_BLOCK        
              494  CALL_FINALLY        498  'to 498'
              496  RETURN_VALUE     
            498_0  COME_FROM           494  '494'
            498_1  COME_FROM_FINALLY    40  '40'

 L. 541       498  LOAD_FAST                'reader'
              500  LOAD_METHOD              close
              502  CALL_METHOD_0         0  ''
              504  POP_TOP          

 L. 542       506  LOAD_FAST                'writer'
              508  LOAD_METHOD              close
              510  CALL_METHOD_0         0  ''
              512  POP_TOP          
              514  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 494

            def _write_SOCKS5_address--- This code section failed: ---

 L. 549         0  LOAD_FAST                'addr'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L. 550         8  LOAD_FAST                'self'
               10  LOAD_ATTR                proxy
               12  UNPACK_SEQUENCE_6     6 
               14  STORE_FAST               'proxy_type'
               16  STORE_FAST               '_'
               18  STORE_FAST               '_'
               20  STORE_FAST               'rdns'
               22  STORE_FAST               'username'
               24  STORE_FAST               'password'

 L. 551        26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                AF_INET
               30  LOAD_CONST               b'\x01'
               32  LOAD_GLOBAL              socket
               34  LOAD_ATTR                AF_INET6
               36  LOAD_CONST               b'\x04'
               38  BUILD_MAP_2           2 
               40  STORE_FAST               'family_to_byte'

 L. 556        42  LOAD_GLOBAL              socket
               44  LOAD_ATTR                AF_INET
               46  LOAD_GLOBAL              socket
               48  LOAD_ATTR                AF_INET6
               50  BUILD_TUPLE_2         2 
               52  GET_ITER         
               54  FOR_ITER            162  'to 162'
               56  STORE_FAST               'family'

 L. 557        58  SETUP_FINALLY       134  'to 134'

 L. 558        60  LOAD_GLOBAL              socket
               62  LOAD_METHOD              inet_pton
               64  LOAD_FAST                'family'
               66  LOAD_FAST                'host'
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'addr_bytes'

 L. 559        72  LOAD_FAST                'file'
               74  LOAD_METHOD              write
               76  LOAD_FAST                'family_to_byte'
               78  LOAD_FAST                'family'
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'addr_bytes'
               84  BINARY_ADD       
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 560        90  LOAD_GLOBAL              socket
               92  LOAD_METHOD              inet_ntop
               94  LOAD_FAST                'family'
               96  LOAD_FAST                'addr_bytes'
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'host'

 L. 561       102  LOAD_FAST                'file'
              104  LOAD_METHOD              write
              106  LOAD_GLOBAL              struct
              108  LOAD_METHOD              pack
              110  LOAD_STR                 '>H'
              112  LOAD_FAST                'port'
              114  CALL_METHOD_2         2  ''
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 562       120  LOAD_FAST                'host'
              122  LOAD_FAST                'port'
              124  BUILD_TUPLE_2         2 
              126  POP_BLOCK        
              128  ROT_TWO          
              130  POP_TOP          
              132  RETURN_VALUE     
            134_0  COME_FROM_FINALLY    58  '58'

 L. 563       134  DUP_TOP          
              136  LOAD_GLOBAL              socket
              138  LOAD_ATTR                error
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   158  'to 158'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 564       150  POP_EXCEPT       
              152  JUMP_BACK            54  'to 54'
              154  POP_EXCEPT       
              156  JUMP_BACK            54  'to 54'
            158_0  COME_FROM           142  '142'
              158  END_FINALLY      
              160  JUMP_BACK            54  'to 54'

 L. 567       162  LOAD_FAST                'rdns'
              164  POP_JUMP_IF_FALSE   208  'to 208'

 L. 569       166  LOAD_FAST                'host'
              168  LOAD_METHOD              encode
              170  LOAD_STR                 'idna'
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'host_bytes'

 L. 570       176  LOAD_FAST                'file'
              178  LOAD_METHOD              write
              180  LOAD_CONST               b'\x03'
              182  LOAD_GLOBAL              chr
              184  LOAD_GLOBAL              len
              186  LOAD_FAST                'host_bytes'
              188  CALL_FUNCTION_1       1  ''
              190  CALL_FUNCTION_1       1  ''
              192  LOAD_METHOD              encode
              194  CALL_METHOD_0         0  ''
              196  BINARY_ADD       
              198  LOAD_FAST                'host_bytes'
              200  BINARY_ADD       
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
              206  JUMP_FORWARD        306  'to 306'
            208_0  COME_FROM           164  '164'

 L. 573       208  LOAD_GLOBAL              socket
              210  LOAD_METHOD              getaddrinfo
              212  LOAD_FAST                'host'
              214  LOAD_FAST                'port'
              216  LOAD_GLOBAL              socket
              218  LOAD_ATTR                AF_UNSPEC

 L. 574       220  LOAD_GLOBAL              socket
              222  LOAD_ATTR                SOCK_STREAM

 L. 575       224  LOAD_GLOBAL              socket
              226  LOAD_ATTR                IPPROTO_TCP

 L. 576       228  LOAD_GLOBAL              socket
              230  LOAD_ATTR                AI_ADDRCONFIG

 L. 573       232  CALL_METHOD_6         6  ''
              234  STORE_FAST               'addresses'

 L. 579       236  LOAD_FAST                'addresses'
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  STORE_FAST               'target_addr'

 L. 580       244  LOAD_FAST                'target_addr'
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  STORE_FAST               'family'

 L. 581       252  LOAD_FAST                'target_addr'
              254  LOAD_CONST               4
              256  BINARY_SUBSCR    
              258  LOAD_CONST               0
              260  BINARY_SUBSCR    
              262  STORE_FAST               'host'

 L. 583       264  LOAD_GLOBAL              socket
              266  LOAD_METHOD              inet_pton
              268  LOAD_FAST                'family'
              270  LOAD_FAST                'host'
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'addr_bytes'

 L. 584       276  LOAD_FAST                'file'
              278  LOAD_METHOD              write
              280  LOAD_FAST                'family_to_byte'
              282  LOAD_FAST                'family'
              284  BINARY_SUBSCR    
              286  LOAD_FAST                'addr_bytes'
              288  BINARY_ADD       
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          

 L. 585       294  LOAD_GLOBAL              socket
              296  LOAD_METHOD              inet_ntop
              298  LOAD_FAST                'family'
              300  LOAD_FAST                'addr_bytes'
              302  CALL_METHOD_2         2  ''
              304  STORE_FAST               'host'
            306_0  COME_FROM           206  '206'

 L. 586       306  LOAD_FAST                'file'
              308  LOAD_METHOD              write
              310  LOAD_GLOBAL              struct
              312  LOAD_METHOD              pack
              314  LOAD_STR                 '>H'
              316  LOAD_FAST                'port'
              318  CALL_METHOD_2         2  ''
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L. 587       324  LOAD_FAST                'host'
              326  LOAD_FAST                'port'
              328  BUILD_TUPLE_2         2 
              330  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 128

            def _read_SOCKS5_address(self, file):
                atyp = self._readall(file, 1)
                if atyp == b'\x01':
                    addr = socket.inet_ntoa(self._readall(file, 4))
                else:
                    if atyp == b'\x03':
                        length = self._readall(file, 1)
                        addr = self._readall(file, ord(length))
                    else:
                        if atyp == b'\x04':
                            addr = socket.inet_ntop(socket.AF_INET6, self._readall(file, 16))
                        else:
                            raise GeneralProxyError('SOCKS5 proxy server sent invalid data')
                port = struct.unpack('>H', self._readall(file, 2))[0]
                return (addr, port)

            def _negotiate_SOCKS4(self, dest_addr, dest_port):
                """Negotiates a connection through a SOCKS4 server."""
                proxy_type, addr, port, rdns, username, password = self.proxy
                writer = self.makefile('wb')
                reader = self.makefile('rb', 0)
                try:
                    remote_resolve = False
                    try:
                        addr_bytes = socket.inet_aton(dest_addr)
                    except socket.error:
                        if rdns:
                            addr_bytes = b'\x00\x00\x00\x01'
                            remote_resolve = True
                        else:
                            addr_bytes = socket.inet_aton(socket.gethostbyname(dest_addr))
                    else:
                        writer.write(struct.pack'>BBH'41dest_port)
                        writer.write(addr_bytes)
                        if username:
                            writer.write(username)
                        else:
                            writer.write(b'\x00')
                            if remote_resolve:
                                writer.write(dest_addr.encode('idna') + b'\x00')
                            writer.flush()
                            resp = self._readall(reader, 8)
                            if resp[0:1] != b'\x00':
                                raise GeneralProxyError('SOCKS4 proxy server sent invalid data')
                            status = ord(resp[1:2])
                            if status != 90:
                                error = SOCKS4_ERRORS.get(status, 'Unknown error')
                                raise SOCKS4Error('{:#04x}: {}'.format(status, error))
                            self.proxy_sockname = (
                             socket.inet_ntoa(resp[4:]),
                             struct.unpack('>H', resp[2:4])[0])
                            if remote_resolve:
                                self.proxy_peername = (
                                 socket.inet_ntoa(addr_bytes), dest_port)
                            else:
                                self.proxy_peername = (
                                 dest_addr, dest_port)
                finally:
                    reader.close()
                    writer.close()

            def _negotiate_HTTP(self, dest_addr, dest_port):
                """Negotiates a connection through an HTTP server.

        NOTE: This currently only supports HTTP CONNECT-style proxies."""
                proxy_type, addr, port, rdns, username, password = self.proxy
                addr = dest_addr if rdns else socket.gethostbyname(dest_addr)
                http_headers = [
                 b'CONNECT ' + addr.encode('idna') + b':' + str(dest_port).encode() + b' HTTP/1.1',
                 b'Host: ' + dest_addr.encode('idna')]
                if username:
                    if password:
                        http_headers.append(b'Proxy-Authorization: basic ' + b64encode(username + b':' + password))
                http_headers.append(b'\r\n')
                self.sendall((b'\r\n').join(http_headers))
                fobj = self.makefile()
                status_line = fobj.readline()
                fobj.close()
                if not status_line:
                    raise GeneralProxyError('Connection closed unexpectedly')
                try:
                    proto, status_code, status_msg = status_line.split(' ', 2)
                except ValueError:
                    raise GeneralProxyError('HTTP proxy server sent invalid response')
                else:
                    if not proto.startswith('HTTP/'):
                        raise GeneralProxyError('Proxy server does not appear to be an HTTP proxy')
                try:
                    status_code = int(status_code)
                except ValueError:
                    raise HTTPError('HTTP proxy server did not return a valid HTTP status')
                else:
                    if status_code != 200:
                        error = '{}: {}'.format(status_code, status_msg)
                        if status_code in (400, 403, 405):
                            error += '\n[*] Note: The HTTP proxy server may not be supported by PySocks (must be a CONNECT tunnel proxy)'
                        raise HTTPError(error)
                    self.proxy_sockname = (b'0.0.0.0', 0)
                    self.proxy_peername = (addr, dest_port)

            _proxy_negotiators = {SOCKS4: _negotiate_SOCKS4, 
             SOCKS5: _negotiate_SOCKS5, 
             HTTP: _negotiate_HTTP}

            @set_self_blocking
            def connect(self, dest_pair, catch_errors=None):
                """
        Connects to the specified destination through a proxy.
        Uses the same API as socket's connect().
        To select the proxy server, use set_proxy().

        dest_pair - 2-tuple of (IP/hostname, port).
        """
                if not len(dest_pair) != 2:
                    if dest_pair[0].startswith('['):
                        raise socket.error("PySocks doesn't support IPv6: %s" % str(dest_pair))
                    dest_addr, dest_port = dest_pair
                    if self.type == socket.SOCK_DGRAM:
                        if not self._proxyconn:
                            self.bind(('', 0))
                        dest_addr = socket.gethostbyname(dest_addr)
                        if dest_addr == '0.0.0.0':
                            self.proxy_peername = dest_port or None
                        else:
                            self.proxy_peername = (
                             dest_addr, dest_port)
                        return
                    proxy_type, proxy_addr, proxy_port, rdns, username, password = self.proxy
                    if isinstance(dest_pair, (list, tuple)) and not len(dest_pair) != 2:
                        if not (dest_addr and isinstance(dest_port, int)):
                            raise GeneralProxyError('Invalid destination-connection (host, port) pair')
                        super(socksocket, self).settimeout(self._timeout)
                        if proxy_type is None:
                            self.proxy_peername = dest_pair
                            super(socksocket, self).settimeout(self._timeout)
                            super(socksocket, self).connect((dest_addr, dest_port))
                            return None
                        proxy_addr = self._proxy_addr()
                        try:
                            super(socksocket, self).connect(proxy_addr)
                        except socket.error as error:
                            try:
                                self.close()
                                if not catch_errors:
                                    proxy_addr, proxy_port = proxy_addr
                                    proxy_server = '{}:{}'.format(proxy_addr, proxy_port)
                                    printable_type = PRINTABLE_PROXY_TYPES[proxy_type]
                                    msg = 'Error connecting to {} proxy {}'.format(printable_type, proxy_server)
                                    log.debug('%s due to: %s', msg, error)
                                    raise ProxyConnectionError(msg, error)
                                else:
                                    raise error
                            finally:
                                error = None
                                del error

                else:
                    try:
                        negotiate = self._proxy_negotiators[proxy_type]
                        negotiate(self, dest_addr, dest_port)
                    except socket.error as error:
                        try:
                            if not catch_errors:
                                self.close()
                                raise GeneralProxyError('Socket error', error)
                            else:
                                raise error
                        finally:
                            error = None
                            del error

                    except ProxyError:
                        self.close()
                        raise

            @set_self_blocking
            def connect_ex--- This code section failed: ---

 L. 827         0  SETUP_FINALLY        22  'to 22'

 L. 828         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connect
                6  LOAD_FAST                'dest_pair'
                8  LOAD_CONST               True
               10  LOAD_CONST               ('catch_errors',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  POP_TOP          

 L. 829        16  POP_BLOCK        
               18  LOAD_CONST               0
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 830        22  DUP_TOP          
               24  LOAD_GLOBAL              OSError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    76  'to 76'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        64  'to 64'

 L. 833        38  LOAD_FAST                'e'
               40  LOAD_ATTR                errno
               42  POP_JUMP_IF_FALSE    58  'to 58'

 L. 834        44  LOAD_FAST                'e'
               46  LOAD_ATTR                errno
               48  ROT_FOUR         
               50  POP_BLOCK        
               52  POP_EXCEPT       
               54  CALL_FINALLY         64  'to 64'
               56  RETURN_VALUE     
             58_0  COME_FROM            42  '42'

 L. 836        58  RAISE_VARARGS_0       0  'reraise'
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM_FINALLY    36  '36'
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  END_FINALLY      
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            28  '28'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'

Parse error at or near `RETURN_VALUE' instruction at offset 20

            def _proxy_addr(self):
                """
        Return proxy address to connect to as tuple object
        """
                proxy_type, proxy_addr, proxy_port, rdns, username, password = self.proxy
                proxy_port = proxy_port or DEFAULT_PORTS.get(proxy_type)
                if not proxy_port:
                    raise GeneralProxyError('Invalid proxy type')
                return (
                 proxy_addr, proxy_port)