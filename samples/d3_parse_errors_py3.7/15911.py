# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\socks.py
from __future__ import unicode_literals
import collections, socket
from .compat import compat_ord, compat_struct_pack, compat_struct_unpack
__author__ = 'Timo Schmid <coding@timoschmid.de>'
SOCKS4_VERSION = 4
SOCKS4_REPLY_VERSION = 0
SOCKS4_DEFAULT_DSTIP = compat_struct_pack('!BBBB', 0, 0, 0, 255)
SOCKS5_VERSION = 5
SOCKS5_USER_AUTH_VERSION = 1
SOCKS5_USER_AUTH_SUCCESS = 0

class Socks4Command(object):
    CMD_CONNECT = 1
    CMD_BIND = 2


class Socks5Command(Socks4Command):
    CMD_UDP_ASSOCIATE = 3


class Socks5Auth(object):
    AUTH_NONE = 0
    AUTH_GSSAPI = 1
    AUTH_USER_PASS = 2
    AUTH_NO_ACCEPTABLE = 255


class Socks5AddressType(object):
    ATYP_IPV4 = 1
    ATYP_DOMAINNAME = 3
    ATYP_IPV6 = 4


class ProxyError(socket.error):
    ERR_SUCCESS = 0

    def __init__(self, code=None, msg=None):
        if code is not None:
            if msg is None:
                msg = self.CODES.get(code) or 'unknown error'
        super(ProxyError, self).__init__(code, msg)


class InvalidVersionError(ProxyError):

    def __init__(self, expected_version, got_version):
        msg = 'Invalid response version from server. Expected {0:02x} got {1:02x}'.format(expected_version, got_version)
        super(InvalidVersionError, self).__init__(0, msg)


class Socks4Error(ProxyError):
    ERR_SUCCESS = 90
    CODES = {91:'request rejected or failed', 
     92:'request rejected because SOCKS server cannot connect to identd on the client', 
     93:'request rejected because the client program and identd report different user-ids'}


class Socks5Error(ProxyError):
    ERR_GENERAL_FAILURE = 1
    CODES = {1:'general SOCKS server failure', 
     2:'connection not allowed by ruleset', 
     3:'Network unreachable', 
     4:'Host unreachable', 
     5:'Connection refused', 
     6:'TTL expired', 
     7:'Command not supported', 
     8:'Address type not supported', 
     254:'unknown username or invalid password', 
     255:'all offered authentication methods were rejected'}


class ProxyType(object):
    SOCKS4 = 0
    SOCKS4A = 1
    SOCKS5 = 2


Proxy = collections.namedtuple('Proxy', ('type', 'host', 'port', 'username', 'password',
                                         'remote_dns'))

class sockssocket(socket.socket):

    def __init__(self, *args, **kwargs):
        self._proxy = None
        (super(sockssocket, self).__init__)(*args, **kwargs)

    def setproxy(self, proxytype, addr, port, rdns=True, username=None, password=None):
        assert proxytype in (ProxyType.SOCKS4, ProxyType.SOCKS4A, ProxyType.SOCKS5)
        self._proxy = Proxy(proxytype, addr, port, username, password, rdns)

    def recvall(self, cnt):
        data = ''
        while len(data) < cnt:
            cur = self.recv(cnt - len(data))
            if not cur:
                raise EOFError('{0} bytes missing'.format(cnt - len(data)))
            else:
                data += cur

        return data

    def _recv_bytes(self, cnt):
        data = self.recvall(cnt)
        return compat_struct_unpack('!{0}B'.format(cnt), data)

    @staticmethod
    def _len_and_data(data):
        return compat_struct_pack('!B', len(data)) + data

    def _check_response_version(self, expected_version, got_version):
        if got_version != expected_version:
            self.close()
            raise InvalidVersionError(expected_version, got_version)

    def _resolve_address(self, destaddr, default, use_remote_dns):
        try:
            return socket.inet_aton(destaddr)
        except socket.error:
            if use_remote_dns:
                if self._proxy.remote_dns:
                    return default
            return socket.inet_aton(socket.gethostbyname(destaddr))

    def _setup_socks4(self, address, is_4a=False):
        destaddr, port = address
        ipaddr = self._resolve_address(destaddr, SOCKS4_DEFAULT_DSTIP, use_remote_dns=is_4a)
        packet = compat_struct_pack('!BBH', SOCKS4_VERSION, Socks4Command.CMD_CONNECT, port) + ipaddr
        username = (self._proxy.username or '').encode('utf-8')
        packet += username + '\x00'
        if is_4a:
            if self._proxy.remote_dns:
                packet += destaddr.encode('utf-8') + '\x00'
        self.sendall(packet)
        version, resp_code, dstport, dsthost = compat_struct_unpack('!BBHI', self.recvall(8))
        self._check_response_version(SOCKS4_REPLY_VERSION, version)
        if resp_code != Socks4Error.ERR_SUCCESS:
            self.close()
            raise Socks4Error(resp_code)
        return (
         dsthost, dstport)

    def _setup_socks4a(self, address):
        self._setup_socks4(address, is_4a=True)

    def _socks5_auth--- This code section failed: ---

 L. 181         0  LOAD_GLOBAL              compat_struct_pack
                2  LOAD_STR                 '!B'
                4  LOAD_GLOBAL              SOCKS5_VERSION
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'packet'

 L. 183        10  LOAD_GLOBAL              Socks5Auth
               12  LOAD_ATTR                AUTH_NONE
               14  BUILD_LIST_1          1 
               16  STORE_FAST               'auth_methods'

 L. 184        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _proxy
               22  LOAD_ATTR                username
               24  POP_JUMP_IF_FALSE    46  'to 46'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _proxy
               30  LOAD_ATTR                password
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 185        34  LOAD_FAST                'auth_methods'
               36  LOAD_METHOD              append
               38  LOAD_GLOBAL              Socks5Auth
               40  LOAD_ATTR                AUTH_USER_PASS
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_TOP          
             46_0  COME_FROM            32  '32'
             46_1  COME_FROM            24  '24'

 L. 187        46  LOAD_FAST                'packet'
               48  LOAD_GLOBAL              compat_struct_pack
               50  LOAD_STR                 '!B'
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'auth_methods'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  INPLACE_ADD      
               62  STORE_FAST               'packet'

 L. 188        64  LOAD_FAST                'packet'
               66  LOAD_GLOBAL              compat_struct_pack
               68  LOAD_STR                 '!{0}B'
               70  LOAD_METHOD              format
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'auth_methods'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  BUILD_TUPLE_1         1 
               82  LOAD_FAST                'auth_methods'
               84  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               86  CALL_FUNCTION_EX      0  'positional arguments only'
               88  INPLACE_ADD      
               90  STORE_FAST               'packet'

 L. 190        92  LOAD_FAST                'self'
               94  LOAD_METHOD              sendall
               96  LOAD_FAST                'packet'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_TOP          

 L. 192       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _recv_bytes
              106  LOAD_CONST               2
              108  CALL_METHOD_1         1  '1 positional argument'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'version'
              114  STORE_FAST               'method'

 L. 194       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _check_response_version
              120  LOAD_GLOBAL              SOCKS5_VERSION
              122  LOAD_FAST                'version'
              124  CALL_METHOD_2         2  '2 positional arguments'
              126  POP_TOP          

 L. 196       128  LOAD_FAST                'method'
              130  LOAD_GLOBAL              Socks5Auth
              132  LOAD_ATTR                AUTH_NO_ACCEPTABLE
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_TRUE    164  'to 164'

 L. 197       138  LOAD_FAST                'method'
              140  LOAD_GLOBAL              Socks5Auth
              142  LOAD_ATTR                AUTH_USER_PASS
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   182  'to 182'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                _proxy
              152  LOAD_ATTR                username
              154  POP_JUMP_IF_FALSE   164  'to 164'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _proxy
              160  LOAD_ATTR                password
              162  POP_JUMP_IF_TRUE    182  'to 182'
            164_0  COME_FROM           154  '154'
            164_1  COME_FROM           136  '136'

 L. 198       164  LOAD_FAST                'self'
              166  LOAD_METHOD              close
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  POP_TOP          

 L. 199       172  LOAD_GLOBAL              Socks5Error
              174  LOAD_GLOBAL              Socks5Auth
              176  LOAD_ATTR                AUTH_NO_ACCEPTABLE
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  RAISE_VARARGS_1       1  'exception instance'
            182_0  COME_FROM           162  '162'
            182_1  COME_FROM           146  '146'

 L. 201       182  LOAD_FAST                'method'
              184  LOAD_GLOBAL              Socks5Auth
              186  LOAD_ATTR                AUTH_USER_PASS
              188  COMPARE_OP               ==
          190_192  POP_JUMP_IF_FALSE   320  'to 320'

 L. 202       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _proxy
              198  LOAD_ATTR                username
              200  LOAD_METHOD              encode
              202  LOAD_STR                 'utf-8'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  STORE_FAST               'username'

 L. 203       208  LOAD_FAST                'self'
              210  LOAD_ATTR                _proxy
              212  LOAD_ATTR                password
              214  LOAD_METHOD              encode
              216  LOAD_STR                 'utf-8'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  STORE_FAST               'password'

 L. 204       222  LOAD_GLOBAL              compat_struct_pack
              224  LOAD_STR                 '!B'
              226  LOAD_GLOBAL              SOCKS5_USER_AUTH_VERSION
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  STORE_FAST               'packet'

 L. 205       232  LOAD_FAST                'packet'
              234  LOAD_FAST                'self'
              236  LOAD_METHOD              _len_and_data
              238  LOAD_FAST                'username'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  LOAD_FAST                'self'
              244  LOAD_METHOD              _len_and_data
              246  LOAD_FAST                'password'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  BINARY_ADD       
              252  INPLACE_ADD      
              254  STORE_FAST               'packet'

 L. 206       256  LOAD_FAST                'self'
              258  LOAD_METHOD              sendall
              260  LOAD_FAST                'packet'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          

 L. 208       266  LOAD_FAST                'self'
              268  LOAD_METHOD              _recv_bytes
              270  LOAD_CONST               2
              272  CALL_METHOD_1         1  '1 positional argument'
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'version'
              278  STORE_FAST               'status'

 L. 210       280  LOAD_FAST                'self'
              282  LOAD_METHOD              _check_response_version
              284  LOAD_GLOBAL              SOCKS5_USER_AUTH_VERSION
              286  LOAD_FAST                'version'
              288  CALL_METHOD_2         2  '2 positional arguments'
              290  POP_TOP          

 L. 212       292  LOAD_FAST                'status'
              294  LOAD_GLOBAL              SOCKS5_USER_AUTH_SUCCESS
              296  COMPARE_OP               !=
          298_300  POP_JUMP_IF_FALSE   320  'to 320'

 L. 213       302  LOAD_FAST                'self'
              304  LOAD_METHOD              close
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  POP_TOP          

 L. 214       310  LOAD_GLOBAL              Socks5Error
              312  LOAD_GLOBAL              Socks5Error
              314  LOAD_ATTR                ERR_GENERAL_FAILURE
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  RAISE_VARARGS_1       1  'exception instance'
            320_0  COME_FROM           298  '298'
            320_1  COME_FROM           190  '190'

Parse error at or near `COME_FROM' instruction at offset 320_0

    def _setup_socks5(self, address):
        destaddr, port = address
        ipaddr = self._resolve_address(destaddr, None, use_remote_dns=True)
        self._socks5_auth()
        reserved = 0
        packet = compat_struct_pack('!BBB', SOCKS5_VERSION, Socks5Command.CMD_CONNECT, reserved)
        if ipaddr is None:
            destaddr = destaddr.encode('utf-8')
            packet += compat_struct_pack('!B', Socks5AddressType.ATYP_DOMAINNAME)
            packet += self._len_and_data(destaddr)
        else:
            packet += compat_struct_pack('!B', Socks5AddressType.ATYP_IPV4) + ipaddr
        packet += compat_struct_pack('!H', port)
        self.sendall(packet)
        version, status, reserved, atype = self._recv_bytes(4)
        self._check_response_version(SOCKS5_VERSION, version)
        if status != Socks5Error.ERR_SUCCESS:
            self.close()
            raise Socks5Error(status)
        if atype == Socks5AddressType.ATYP_IPV4:
            destaddr = self.recvall(4)
        elif atype == Socks5AddressType.ATYP_DOMAINNAME:
            alen = compat_ord(self.recv(1))
            destaddr = self.recvall(alen)
        elif atype == Socks5AddressType.ATYP_IPV6:
            destaddr = self.recvall(16)
        destport = compat_struct_unpack('!H', self.recvall(2))[0]
        return (
         destaddr, destport)

    def _make_proxy(self, connect_func, address):
        if not self._proxy:
            return connect_func(self, address)
        result = connect_func(self, (self._proxy.host, self._proxy.port))
        if result != 0:
            if result is not None:
                return result
        setup_funcs = {ProxyType.SOCKS4: self._setup_socks4, 
         ProxyType.SOCKS4A: self._setup_socks4a, 
         ProxyType.SOCKS5: self._setup_socks5}
        setup_funcs[self._proxy.type](address)
        return result

    def connect(self, address):
        self._make_proxy(socket.socket.connect, address)

    def connect_ex(self, address):
        return self._make_proxy(socket.socket.connect_ex, address)