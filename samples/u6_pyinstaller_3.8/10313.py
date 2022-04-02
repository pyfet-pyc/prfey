# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: ssl.py
"""This module provides some more Pythonic support for SSL.

Object types:

  SSLSocket -- subtype of socket.socket which does SSL over the socket

Exceptions:

  SSLError -- exception raised for I/O errors

Functions:

  cert_time_to_seconds -- convert time string used for certificate
                          notBefore and notAfter functions to integer
                          seconds past the Epoch (the time values
                          returned from time.time())

  fetch_server_certificate (HOST, PORT) -- fetch the certificate provided
                          by the server running on HOST at port PORT.  No
                          validation of the certificate is performed.

Integer constants:

SSL_ERROR_ZERO_RETURN
SSL_ERROR_WANT_READ
SSL_ERROR_WANT_WRITE
SSL_ERROR_WANT_X509_LOOKUP
SSL_ERROR_SYSCALL
SSL_ERROR_SSL
SSL_ERROR_WANT_CONNECT

SSL_ERROR_EOF
SSL_ERROR_INVALID_ERROR_CODE

The following group define certificate requirements that one side is
allowing/requiring from the other side:

CERT_NONE - no certificates from the other side are required (or will
            be looked at if provided)
CERT_OPTIONAL - certificates are not required, but if provided will be
                validated, and if validation fails, the connection will
                also fail
CERT_REQUIRED - certificates are required, and will be validated, and
                if validation fails, the connection will also fail

The following constants identify various SSL protocol variants:

PROTOCOL_SSLv2
PROTOCOL_SSLv3
PROTOCOL_SSLv23
PROTOCOL_TLS
PROTOCOL_TLS_CLIENT
PROTOCOL_TLS_SERVER
PROTOCOL_TLSv1
PROTOCOL_TLSv1_1
PROTOCOL_TLSv1_2

The following constants identify various SSL alert message descriptions as per
http://www.iana.org/assignments/tls-parameters/tls-parameters.xml#tls-parameters-6

ALERT_DESCRIPTION_CLOSE_NOTIFY
ALERT_DESCRIPTION_UNEXPECTED_MESSAGE
ALERT_DESCRIPTION_BAD_RECORD_MAC
ALERT_DESCRIPTION_RECORD_OVERFLOW
ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
ALERT_DESCRIPTION_HANDSHAKE_FAILURE
ALERT_DESCRIPTION_BAD_CERTIFICATE
ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE
ALERT_DESCRIPTION_CERTIFICATE_REVOKED
ALERT_DESCRIPTION_CERTIFICATE_EXPIRED
ALERT_DESCRIPTION_CERTIFICATE_UNKNOWN
ALERT_DESCRIPTION_ILLEGAL_PARAMETER
ALERT_DESCRIPTION_UNKNOWN_CA
ALERT_DESCRIPTION_ACCESS_DENIED
ALERT_DESCRIPTION_DECODE_ERROR
ALERT_DESCRIPTION_DECRYPT_ERROR
ALERT_DESCRIPTION_PROTOCOL_VERSION
ALERT_DESCRIPTION_INSUFFICIENT_SECURITY
ALERT_DESCRIPTION_INTERNAL_ERROR
ALERT_DESCRIPTION_USER_CANCELLED
ALERT_DESCRIPTION_NO_RENEGOTIATION
ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION
ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE
ALERT_DESCRIPTION_UNRECOGNIZED_NAME
ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
"""
import sys, os
from collections import namedtuple
from enum import Enum as _Enum, IntEnum as _IntEnum, IntFlag as _IntFlag
import _ssl
from _ssl import OPENSSL_VERSION_NUMBER, OPENSSL_VERSION_INFO, OPENSSL_VERSION
from _ssl import _SSLContext, MemoryBIO, SSLSession
from _ssl import SSLError, SSLZeroReturnError, SSLWantReadError, SSLWantWriteError, SSLSyscallError, SSLEOFError, SSLCertVerificationError
from _ssl import txt2obj as _txt2obj, nid2obj as _nid2obj
from _ssl import RAND_status, RAND_add, RAND_bytes, RAND_pseudo_bytes
try:
    from _ssl import RAND_egd
except ImportError:
    pass
else:
    from _ssl import HAS_SNI, HAS_ECDH, HAS_NPN, HAS_ALPN, HAS_SSLv2, HAS_SSLv3, HAS_TLSv1, HAS_TLSv1_1, HAS_TLSv1_2, HAS_TLSv1_3
    from _ssl import _DEFAULT_CIPHERS, _OPENSSL_API_VERSION
    _IntEnum._convert_('_SSLMethod',
      __name__, (lambda name: name.startswith('PROTOCOL_') and name != 'PROTOCOL_SSLv23'),
      source=_ssl)
    _IntFlag._convert_('Options',
      __name__, (lambda name: name.startswith('OP_')),
      source=_ssl)
    _IntEnum._convert_('AlertDescription',
      __name__, (lambda name: name.startswith('ALERT_DESCRIPTION_')),
      source=_ssl)
    _IntEnum._convert_('SSLErrorNumber',
      __name__, (lambda name: name.startswith('SSL_ERROR_')),
      source=_ssl)
    _IntFlag._convert_('VerifyFlags',
      __name__, (lambda name: name.startswith('VERIFY_')),
      source=_ssl)
    _IntEnum._convert_('VerifyMode',
      __name__, (lambda name: name.startswith('CERT_')),
      source=_ssl)
    PROTOCOL_SSLv23 = _SSLMethod.PROTOCOL_SSLv23 = _SSLMethod.PROTOCOL_TLS
    _PROTOCOL_NAMES = {name:value for name, value in _SSLMethod.__members__.items()}
    _SSLv2_IF_EXISTS = getattr(_SSLMethod, 'PROTOCOL_SSLv2', None)

    class TLSVersion(_IntEnum):
        MINIMUM_SUPPORTED = _ssl.PROTO_MINIMUM_SUPPORTED
        SSLv3 = _ssl.PROTO_SSLv3
        TLSv1 = _ssl.PROTO_TLSv1
        TLSv1_1 = _ssl.PROTO_TLSv1_1
        TLSv1_2 = _ssl.PROTO_TLSv1_2
        TLSv1_3 = _ssl.PROTO_TLSv1_3
        MAXIMUM_SUPPORTED = _ssl.PROTO_MAXIMUM_SUPPORTED


    class _TLSContentType(_IntEnum):
        __doc__ = 'Content types (record layer)\n\n    See RFC 8446, section B.1\n    '
        CHANGE_CIPHER_SPEC = 20
        ALERT = 21
        HANDSHAKE = 22
        APPLICATION_DATA = 23
        HEADER = 256
        INNER_CONTENT_TYPE = 257


    class _TLSAlertType(_IntEnum):
        __doc__ = 'Alert types for TLSContentType.ALERT messages\n\n    See RFC 8466, section B.2\n    '
        CLOSE_NOTIFY = 0
        UNEXPECTED_MESSAGE = 10
        BAD_RECORD_MAC = 20
        DECRYPTION_FAILED = 21
        RECORD_OVERFLOW = 22
        DECOMPRESSION_FAILURE = 30
        HANDSHAKE_FAILURE = 40
        NO_CERTIFICATE = 41
        BAD_CERTIFICATE = 42
        UNSUPPORTED_CERTIFICATE = 43
        CERTIFICATE_REVOKED = 44
        CERTIFICATE_EXPIRED = 45
        CERTIFICATE_UNKNOWN = 46
        ILLEGAL_PARAMETER = 47
        UNKNOWN_CA = 48
        ACCESS_DENIED = 49
        DECODE_ERROR = 50
        DECRYPT_ERROR = 51
        EXPORT_RESTRICTION = 60
        PROTOCOL_VERSION = 70
        INSUFFICIENT_SECURITY = 71
        INTERNAL_ERROR = 80
        INAPPROPRIATE_FALLBACK = 86
        USER_CANCELED = 90
        NO_RENEGOTIATION = 100
        MISSING_EXTENSION = 109
        UNSUPPORTED_EXTENSION = 110
        CERTIFICATE_UNOBTAINABLE = 111
        UNRECOGNIZED_NAME = 112
        BAD_CERTIFICATE_STATUS_RESPONSE = 113
        BAD_CERTIFICATE_HASH_VALUE = 114
        UNKNOWN_PSK_IDENTITY = 115
        CERTIFICATE_REQUIRED = 116
        NO_APPLICATION_PROTOCOL = 120


    class _TLSMessageType(_IntEnum):
        __doc__ = 'Message types (handshake protocol)\n\n    See RFC 8446, section B.3\n    '
        HELLO_REQUEST = 0
        CLIENT_HELLO = 1
        SERVER_HELLO = 2
        HELLO_VERIFY_REQUEST = 3
        NEWSESSION_TICKET = 4
        END_OF_EARLY_DATA = 5
        HELLO_RETRY_REQUEST = 6
        ENCRYPTED_EXTENSIONS = 8
        CERTIFICATE = 11
        SERVER_KEY_EXCHANGE = 12
        CERTIFICATE_REQUEST = 13
        SERVER_DONE = 14
        CERTIFICATE_VERIFY = 15
        CLIENT_KEY_EXCHANGE = 16
        FINISHED = 20
        CERTIFICATE_URL = 21
        CERTIFICATE_STATUS = 22
        SUPPLEMENTAL_DATA = 23
        KEY_UPDATE = 24
        NEXT_PROTO = 67
        MESSAGE_HASH = 254
        CHANGE_CIPHER_SPEC = 257


    if sys.platform == 'win32':
        from _ssl import enum_certificates, enum_crls
    from socket import socket, AF_INET, SOCK_STREAM, create_connection
    from socket import SOL_SOCKET, SO_TYPE
    import socket as _socket, base64, errno, warnings
    socket_error = OSError
    CHANNEL_BINDING_TYPES = [
     'tls-unique']
    HAS_NEVER_CHECK_COMMON_NAME = hasattr(_ssl, 'HOSTFLAG_NEVER_CHECK_SUBJECT')
    _RESTRICTED_SERVER_CIPHERS = _DEFAULT_CIPHERS
    CertificateError = SSLCertVerificationError

    def _dnsname_match(dn, hostname):
        """Matching according to RFC 6125, section 6.4.3

    - Hostnames are compared lower case.
    - For IDNA, both dn and hostname must be encoded as IDN A-label (ACE).
    - Partial wildcards like 'www*.example.org', multiple wildcards, sole
      wildcard or wildcards in labels other then the left-most label are not
      supported and a CertificateError is raised.
    - A wildcard must match at least one character.
    """
        if not dn:
            return False
            wildcards = dn.count('*')
            if not wildcards:
                return dn.lower() == hostname.lower()
            if wildcards > 1:
                raise CertificateError('too many wildcards in certificate DNS name: {!r}.'.format(dn))
            dn_leftmost, sep, dn_remainder = dn.partition('.')
            if '*' in dn_remainder:
                raise CertificateError('wildcard can only be present in the leftmost label: {!r}.'.format(dn))
        else:
            if not sep:
                raise CertificateError('sole wildcard without additional labels are not support: {!r}.'.format(dn))
            if dn_leftmost != '*':
                raise CertificateError('partial wildcards in leftmost label are not supported: {!r}.'.format(dn))
            hostname_leftmost, sep, hostname_remainder = hostname.partition('.')
            return hostname_leftmost and sep or False
        return dn_remainder.lower() == hostname_remainder.lower()


    def _inet_paton--- This code section failed: ---

 L. 332         0  SETUP_FINALLY        16  'to 16'

 L. 333         2  LOAD_GLOBAL              _socket
                4  LOAD_METHOD              inet_aton
                6  LOAD_FAST                'ipname'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'addr'
               12  POP_BLOCK        
               14  JUMP_FORWARD         36  'to 36'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 334        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 336        30  POP_EXCEPT       
               32  JUMP_FORWARD         68  'to 68'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            14  '14'

 L. 338        36  LOAD_GLOBAL              _socket
               38  LOAD_METHOD              inet_ntoa
               40  LOAD_FAST                'addr'
               42  CALL_METHOD_1         1  ''
               44  LOAD_FAST                'ipname'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 340        50  LOAD_FAST                'addr'
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 343        54  LOAD_GLOBAL              ValueError

 L. 344        56  LOAD_STR                 '{!r} is not a quad-dotted IPv4 address.'
               58  LOAD_METHOD              format
               60  LOAD_FAST                'ipname'
               62  CALL_METHOD_1         1  ''

 L. 343        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            32  '32'

 L. 347        68  SETUP_FINALLY        86  'to 86'

 L. 348        70  LOAD_GLOBAL              _socket
               72  LOAD_METHOD              inet_pton
               74  LOAD_GLOBAL              _socket
               76  LOAD_ATTR                AF_INET6
               78  LOAD_FAST                'ipname'
               80  CALL_METHOD_2         2  ''
               82  POP_BLOCK        
               84  RETURN_VALUE     
             86_0  COME_FROM_FINALLY    68  '68'

 L. 349        86  DUP_TOP          
               88  LOAD_GLOBAL              OSError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   118  'to 118'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 350       100  LOAD_GLOBAL              ValueError
              102  LOAD_STR                 '{!r} is neither an IPv4 nor an IP6 address.'
              104  LOAD_METHOD              format

 L. 351       106  LOAD_FAST                'ipname'

 L. 350       108  CALL_METHOD_1         1  ''
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        138  'to 138'
            118_0  COME_FROM            92  '92'

 L. 352       118  DUP_TOP          
              120  LOAD_GLOBAL              AttributeError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   136  'to 136'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 354       132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           124  '124'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           116  '116'

 L. 356       138  LOAD_GLOBAL              ValueError
              140  LOAD_STR                 '{!r} is not an IPv4 address.'
              142  LOAD_METHOD              format
              144  LOAD_FAST                'ipname'
              146  CALL_METHOD_1         1  ''
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 96


    def _ipaddress_match(cert_ipaddress, host_ip):
        """Exact matching of IP addresses.

    RFC 6125 explicitly doesn't define an algorithm for this
    (section 1.7.2 - "Out of Scope").
    """
        ip = _inet_paton(cert_ipaddress.rstrip())
        return ip == host_ip


    def match_hostname--- This code section failed: ---

 L. 384         0  LOAD_FAST                'cert'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 385         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'empty or no certificate, match_hostname needs a SSL socket or SSL context with either CERT_OPTIONAL or CERT_REQUIRED'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 388        12  SETUP_FINALLY        26  'to 26'

 L. 389        14  LOAD_GLOBAL              _inet_paton
               16  LOAD_FAST                'hostname'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'host_ip'
               22  POP_BLOCK        
               24  JUMP_FORWARD         50  'to 50'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 390        26  DUP_TOP          
               28  LOAD_GLOBAL              ValueError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    48  'to 48'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 392        40  LOAD_CONST               None
               42  STORE_FAST               'host_ip'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            32  '32'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            24  '24'

 L. 393        50  BUILD_LIST_0          0 
               52  STORE_FAST               'dnsnames'

 L. 394        54  LOAD_FAST                'cert'
               56  LOAD_METHOD              get
               58  LOAD_STR                 'subjectAltName'
               60  LOAD_CONST               ()
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'san'

 L. 395        66  LOAD_FAST                'san'
               68  GET_ITER         
             70_0  COME_FROM           128  '128'
               70  FOR_ITER            166  'to 166'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'key'
               76  STORE_FAST               'value'

 L. 396        78  LOAD_FAST                'key'
               80  LOAD_STR                 'DNS'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   122  'to 122'

 L. 397        86  LOAD_FAST                'host_ip'
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   110  'to 110'
               94  LOAD_GLOBAL              _dnsname_match
               96  LOAD_FAST                'value'
               98  LOAD_FAST                'hostname'
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_FALSE   110  'to 110'

 L. 398       104  POP_TOP          
              106  LOAD_CONST               None
              108  RETURN_VALUE     
            110_0  COME_FROM           102  '102'
            110_1  COME_FROM            92  '92'

 L. 399       110  LOAD_FAST                'dnsnames'
              112  LOAD_METHOD              append
              114  LOAD_FAST                'value'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
              120  JUMP_BACK            70  'to 70'
            122_0  COME_FROM            84  '84'

 L. 400       122  LOAD_FAST                'key'
              124  LOAD_STR                 'IP Address'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE    70  'to 70'

 L. 401       130  LOAD_FAST                'host_ip'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
              136  POP_JUMP_IF_FALSE   154  'to 154'
              138  LOAD_GLOBAL              _ipaddress_match
              140  LOAD_FAST                'value'
              142  LOAD_FAST                'host_ip'
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   154  'to 154'

 L. 402       148  POP_TOP          
              150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           146  '146'
            154_1  COME_FROM           136  '136'

 L. 403       154  LOAD_FAST                'dnsnames'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'value'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK            70  'to 70'

 L. 404       166  LOAD_FAST                'dnsnames'
              168  POP_JUMP_IF_TRUE    238  'to 238'

 L. 407       170  LOAD_FAST                'cert'
              172  LOAD_METHOD              get
              174  LOAD_STR                 'subject'
              176  LOAD_CONST               ()
              178  CALL_METHOD_2         2  ''
              180  GET_ITER         
              182  FOR_ITER            238  'to 238'
              184  STORE_FAST               'sub'

 L. 408       186  LOAD_FAST                'sub'
              188  GET_ITER         
            190_0  COME_FROM           204  '204'
              190  FOR_ITER            236  'to 236'
              192  UNPACK_SEQUENCE_2     2 
              194  STORE_FAST               'key'
              196  STORE_FAST               'value'

 L. 411       198  LOAD_FAST                'key'
              200  LOAD_STR                 'commonName'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   190  'to 190'

 L. 412       206  LOAD_GLOBAL              _dnsname_match
              208  LOAD_FAST                'value'
              210  LOAD_FAST                'hostname'
              212  CALL_FUNCTION_2       2  ''
              214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 413       216  POP_TOP          
              218  POP_TOP          
              220  LOAD_CONST               None
              222  RETURN_VALUE     
            224_0  COME_FROM           214  '214'

 L. 414       224  LOAD_FAST                'dnsnames'
              226  LOAD_METHOD              append
              228  LOAD_FAST                'value'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  JUMP_BACK           190  'to 190'
              236  JUMP_BACK           182  'to 182'
            238_0  COME_FROM           168  '168'

 L. 415       238  LOAD_GLOBAL              len
              240  LOAD_FAST                'dnsnames'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               1
              246  COMPARE_OP               >
          248_250  POP_JUMP_IF_FALSE   282  'to 282'

 L. 416       252  LOAD_GLOBAL              CertificateError
              254  LOAD_STR                 "hostname %r doesn't match either of %s"

 L. 418       256  LOAD_FAST                'hostname'
              258  LOAD_STR                 ', '
              260  LOAD_METHOD              join
              262  LOAD_GLOBAL              map
              264  LOAD_GLOBAL              repr
              266  LOAD_FAST                'dnsnames'
              268  CALL_FUNCTION_2       2  ''
              270  CALL_METHOD_1         1  ''
              272  BUILD_TUPLE_2         2 

 L. 416       274  BINARY_MODULO    
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
              280  JUMP_FORWARD        326  'to 326'
            282_0  COME_FROM           248  '248'

 L. 419       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'dnsnames'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_CONST               1
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   318  'to 318'

 L. 420       296  LOAD_GLOBAL              CertificateError
              298  LOAD_STR                 "hostname %r doesn't match %r"

 L. 422       300  LOAD_FAST                'hostname'
              302  LOAD_FAST                'dnsnames'
              304  LOAD_CONST               0
              306  BINARY_SUBSCR    
              308  BUILD_TUPLE_2         2 

 L. 420       310  BINARY_MODULO    
              312  CALL_FUNCTION_1       1  ''
              314  RAISE_VARARGS_1       1  'exception instance'
              316  JUMP_FORWARD        326  'to 326'
            318_0  COME_FROM           292  '292'

 L. 424       318  LOAD_GLOBAL              CertificateError
              320  LOAD_STR                 'no appropriate commonName or subjectAltName fields were found'
              322  CALL_FUNCTION_1       1  ''
              324  RAISE_VARARGS_1       1  'exception instance'
            326_0  COME_FROM           316  '316'
            326_1  COME_FROM           280  '280'

Parse error at or near `JUMP_BACK' instruction at offset 236


    DefaultVerifyPaths = namedtuple('DefaultVerifyPaths', 'cafile capath openssl_cafile_env openssl_cafile openssl_capath_env openssl_capath')

    def get_default_verify_paths():
        """Return paths to default cafile and capath.
    """
        parts = _ssl.get_default_verify_paths()
        cafile = os.environ.getparts[0]parts[1]
        capath = os.environ.getparts[2]parts[3]
        return DefaultVerifyPaths(cafile if os.path.isfile(cafile) else None, capath if os.path.isdir(capath) else None, *parts)


    class _ASN1Object(namedtuple('_ASN1Object', 'nid shortname longname oid')):
        __doc__ = 'ASN.1 object identifier lookup\n    '
        __slots__ = ()

        def __new__(cls, oid):
            return (super().__new__)(cls, *_txt2obj(oid, name=False))

        @classmethod
        def fromnid(cls, nid):
            return (super().__new__)(cls, *_nid2obj(nid))

        @classmethod
        def fromname(cls, name):
            return (super().__new__)(cls, *_txt2obj(name, name=True))


    class Purpose(_ASN1Object, _Enum):
        __doc__ = 'SSLContext purpose flags with X509v3 Extended Key Usage objects\n    '
        SERVER_AUTH = '1.3.6.1.5.5.7.3.1'
        CLIENT_AUTH = '1.3.6.1.5.5.7.3.2'


    class SSLContext(_SSLContext):
        __doc__ = 'An SSLContext holds various SSL-related configuration options and\n    data, such as certificates and possibly a private key.'
        _windows_cert_stores = ('CA', 'ROOT')
        sslsocket_class = None
        sslobject_class = None

        def __new__(cls, protocol=PROTOCOL_TLS, *args, **kwargs):
            self = _SSLContext.__new__clsprotocol
            return self

        def _encode_hostname(self, hostname):
            if hostname is None:
                return
            if isinstance(hostname, str):
                return hostname.encode('idna').decode('ascii')
            return hostname.decode('ascii')

        def wrap_socket(self, sock, server_side=False, do_handshake_on_connect=True, suppress_ragged_eofs=True, server_hostname=None, session=None):
            return self.sslsocket_class._create(sock=sock,
              server_side=server_side,
              do_handshake_on_connect=do_handshake_on_connect,
              suppress_ragged_eofs=suppress_ragged_eofs,
              server_hostname=server_hostname,
              context=self,
              session=session)

        def wrap_bio(self, incoming, outgoing, server_side=False, server_hostname=None, session=None):
            return self.sslobject_class._create(incoming,
              outgoing, server_side=server_side, server_hostname=(self._encode_hostname(server_hostname)),
              session=session,
              context=self)

        def set_npn_protocols(self, npn_protocols):
            protos = bytearray()
            for protocol in npn_protocols:
                b = bytes(protocol, 'ascii')
                if len(b) == 0 or len(b) > 255:
                    raise SSLError('NPN protocols must be 1 to 255 in length')
                protos.append(len(b))
                protos.extend(b)
            else:
                self._set_npn_protocols(protos)

        def set_servername_callback(self, server_name_callback):
            if server_name_callback is None:
                self.sni_callback = None
            else:
                if not callable(server_name_callback):
                    raise TypeError('not a callable object')

                def shim_cb(sslobj, servername, sslctx):
                    servername = self._encode_hostname(servername)
                    return server_name_callback(sslobj, servername, sslctx)

                self.sni_callback = shim_cb

        def set_alpn_protocols(self, alpn_protocols):
            protos = bytearray()
            for protocol in alpn_protocols:
                b = bytes(protocol, 'ascii')
                if len(b) == 0 or len(b) > 255:
                    raise SSLError('ALPN protocols must be 1 to 255 in length')
                protos.append(len(b))
                protos.extend(b)
            else:
                self._set_alpn_protocols(protos)

        def _load_windows_store_certs(self, storename, purpose):
            certs = bytearray()
            try:
                for cert, encoding, trust in enum_certificates(storename):
                    if not encoding == 'x509_asn' or trust is True or purpose.oid in trust:
                        certs.extend(cert)

            except PermissionError:
                warnings.warn('unable to enumerate Windows certificate store')
            else:
                if certs:
                    self.load_verify_locations(cadata=certs)
                return certs

        def load_default_certs(self, purpose=Purpose.SERVER_AUTH):
            if not isinstance(purpose, _ASN1Object):
                raise TypeError(purpose)
            if sys.platform == 'win32':
                for storename in self._windows_cert_stores:
                    self._load_windows_store_certsstorenamepurpose

            self.set_default_verify_paths()

        if hasattr(_SSLContext, 'minimum_version'):

            @property
            def minimum_version(self):
                return TLSVersion(super().minimum_version)

            @minimum_version.setter
            def minimum_version(self, value):
                if value == TLSVersion.SSLv3:
                    self.options &= ~Options.OP_NO_SSLv3
                super(SSLContext, SSLContext).minimum_version.__set__selfvalue

            @property
            def maximum_version(self):
                return TLSVersion(super().maximum_version)

            @maximum_version.setter
            def maximum_version(self, value):
                super(SSLContext, SSLContext).maximum_version.__set__selfvalue

        else:

            @property
            def options(self):
                return Options(super().options)

            @options.setter
            def options(self, value):
                super(SSLContext, SSLContext).options.__set__selfvalue

            if hasattr(_ssl, 'HOSTFLAG_NEVER_CHECK_SUBJECT'):

                @property
                def hostname_checks_common_name(self):
                    ncs = self._host_flags & _ssl.HOSTFLAG_NEVER_CHECK_SUBJECT
                    return ncs != _ssl.HOSTFLAG_NEVER_CHECK_SUBJECT

                @hostname_checks_common_name.setter
                def hostname_checks_common_name(self, value):
                    if value:
                        self._host_flags &= ~_ssl.HOSTFLAG_NEVER_CHECK_SUBJECT
                    else:
                        self._host_flags |= _ssl.HOSTFLAG_NEVER_CHECK_SUBJECT

            else:

                @property
                def hostname_checks_common_name(self):
                    return True

        @property
        def _msg_callback(self):
            inner = super()._msg_callback
            if inner is not None:
                return inner.user_function
            return

        @_msg_callback.setter
        def _msg_callback(self, callback):
            if callback is None:
                super(SSLContext, SSLContext)._msg_callback.__set__selfNone
                return None
            if not hasattr(callback, '__call__'):
                raise TypeError(f"{callback} is not callable.")

            def inner(conn, direction, version, content_type, msg_type, data):
                try:
                    version = TLSVersion(version)
                except ValueError:
                    pass
                else:
                    try:
                        content_type = _TLSContentType(content_type)
                    except ValueError:
                        pass
                    else:
                        if content_type == _TLSContentType.HEADER:
                            msg_enum = _TLSContentType
                        else:
                            if content_type == _TLSContentType.ALERT:
                                msg_enum = _TLSAlertType
                            else:
                                msg_enum = _TLSMessageType
                        try:
                            msg_type = msg_enum(msg_type)
                        except ValueError:
                            pass
                        else:
                            return callback(conn, direction, version, content_type, msg_type, data)

            inner.user_function = callback
            super(SSLContext, SSLContext)._msg_callback.__set__selfinner

        @property
        def protocol(self):
            return _SSLMethod(super().protocol)

        @property
        def verify_flags(self):
            return VerifyFlags(super().verify_flags)

        @verify_flags.setter
        def verify_flags(self, value):
            super(SSLContext, SSLContext).verify_flags.__set__selfvalue

        @property
        def verify_mode--- This code section failed: ---

 L. 712         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                verify_mode
                6  STORE_FAST               'value'

 L. 713         8  SETUP_FINALLY        20  'to 20'

 L. 714        10  LOAD_GLOBAL              VerifyMode
               12  LOAD_FAST                'value'
               14  CALL_FUNCTION_1       1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     8  '8'

 L. 715        20  DUP_TOP          
               22  LOAD_GLOBAL              ValueError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 716        34  LOAD_FAST                'value'
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30

        @verify_mode.setter
        def verify_mode(self, value):
            super(SSLContext, SSLContext).verify_mode.__set__selfvalue


    def create_default_context(purpose=Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
        """Create a SSLContext object with default settings.

    NOTE: The protocol and settings may change anytime without prior
          deprecation. The values represent a fair balance between maximum
          compatibility and security.
    """
        if not isinstance(purpose, _ASN1Object):
            raise TypeError(purpose)
        else:
            context = SSLContext(PROTOCOL_TLS)
            if purpose == Purpose.SERVER_AUTH:
                context.verify_mode = CERT_REQUIRED
                context.check_hostname = True
            if not cafile:
                if capath or cadata:
                    context.load_verify_locations(cafile, capath, cadata)
            elif context.verify_mode != CERT_NONE:
                context.load_default_certs(purpose)
            if hasattr(context, 'keylog_filename'):
                keylogfile = os.environ.get('SSLKEYLOGFILE')
                if keylogfile:
                    if not sys.flags.ignore_environment:
                        context.keylog_filename = keylogfile
        return context


    def _create_unverified_context(protocol=PROTOCOL_TLS, *, cert_reqs=CERT_NONE, check_hostname=False, purpose=Purpose.SERVER_AUTH, certfile=None, keyfile=None, cafile=None, capath=None, cadata=None):
        """Create a SSLContext object for Python stdlib modules

    All Python stdlib modules shall use this function to create SSLContext
    objects in order to keep common settings in one place. The configuration
    is less restrict than create_default_context()'s to increase backward
    compatibility.
    """
        if not isinstance(purpose, _ASN1Object):
            raise TypeError(purpose)
        else:
            context = SSLContext(protocol)
            if not check_hostname:
                context.check_hostname = False
            if cert_reqs is not None:
                context.verify_mode = cert_reqs
            if check_hostname:
                context.check_hostname = True
            else:
                if keyfile:
                    if not certfile:
                        raise ValueError('certfile must be specified')
                else:
                    if certfile or keyfile:
                        context.load_cert_chaincertfilekeyfile
                    if cafile or capath or cadata:
                        context.load_verify_locations(cafile, capath, cadata)
                if context.verify_mode != CERT_NONE:
                    context.load_default_certs(purpose)
            if hasattr(context, 'keylog_filename'):
                keylogfile = os.environ.get('SSLKEYLOGFILE')
                if keylogfile:
                    if not sys.flags.ignore_environment:
                        context.keylog_filename = keylogfile
        return context


    _create_default_https_context = create_default_context
    _create_stdlib_context = _create_unverified_context

    class SSLObject:
        __doc__ = 'This class implements an interface on top of a low-level SSL object as\n    implemented by OpenSSL. This object captures the state of an SSL connection\n    but does not provide any network IO itself. IO needs to be performed\n    through separate "BIO" objects which are OpenSSL\'s IO abstraction layer.\n\n    This class does not have a public constructor. Instances are returned by\n    ``SSLContext.wrap_bio``. This class is typically used by framework authors\n    that want to implement asynchronous IO for SSL through memory buffers.\n\n    When compared to ``SSLSocket``, this object lacks the following features:\n\n     * Any form of network IO, including methods such as ``recv`` and ``send``.\n     * The ``do_handshake_on_connect`` and ``suppress_ragged_eofs`` machinery.\n    '

        def __init__(self, *args, **kwargs):
            raise TypeError(f"{self.__class__.__name__} does not have a public constructor. Instances are returned by SSLContext.wrap_bio().")

        @classmethod
        def _create(cls, incoming, outgoing, server_side=False, server_hostname=None, session=None, context=None):
            self = cls.__new__(cls)
            sslobj = context._wrap_bio(incoming,
              outgoing, server_side=server_side, server_hostname=server_hostname,
              owner=self,
              session=session)
            self._sslobj = sslobj
            return self

        @property
        def context(self):
            """The SSLContext that is currently in use."""
            return self._sslobj.context

        @context.setter
        def context(self, ctx):
            self._sslobj.context = ctx

        @property
        def session(self):
            """The SSLSession for client socket."""
            return self._sslobj.session

        @session.setter
        def session(self, session):
            self._sslobj.session = session

        @property
        def session_reused(self):
            """Was the client session reused during handshake"""
            return self._sslobj.session_reused

        @property
        def server_side(self):
            """Whether this is a server-side socket."""
            return self._sslobj.server_side

        @property
        def server_hostname(self):
            """The currently set server hostname (for SNI), or ``None`` if no
        server hostname is set."""
            return self._sslobj.server_hostname

        def read(self, len=1024, buffer=None):
            """Read up to 'len' bytes from the SSL object and return them.

        If 'buffer' is provided, read into this buffer and return the number of
        bytes read.
        """
            if buffer is not None:
                v = self._sslobj.readlenbuffer
            else:
                v = self._sslobj.read(len)
            return v

        def write(self, data):
            """Write 'data' to the SSL object and return the number of bytes
        written.

        The 'data' argument must support the buffer interface.
        """
            return self._sslobj.write(data)

        def getpeercert(self, binary_form=False):
            """Returns a formatted version of the data in the certificate provided
        by the other end of the SSL channel.

        Return None if no certificate was provided, {} if a certificate was
        provided, but not validated.
        """
            return self._sslobj.getpeercert(binary_form)

        def selected_npn_protocol(self):
            """Return the currently selected NPN protocol as a string, or ``None``
        if a next protocol was not negotiated or if NPN is not supported by one
        of the peers."""
            if _ssl.HAS_NPN:
                return self._sslobj.selected_npn_protocol()

        def selected_alpn_protocol(self):
            """Return the currently selected ALPN protocol as a string, or ``None``
        if a next protocol was not negotiated or if ALPN is not supported by one
        of the peers."""
            if _ssl.HAS_ALPN:
                return self._sslobj.selected_alpn_protocol()

        def cipher(self):
            """Return the currently selected cipher as a 3-tuple ``(name,
        ssl_version, secret_bits)``."""
            return self._sslobj.cipher()

        def shared_ciphers(self):
            """Return a list of ciphers shared by the client during the handshake or
        None if this is not a valid server connection.
        """
            return self._sslobj.shared_ciphers()

        def compression(self):
            """Return the current compression algorithm in use, or ``None`` if
        compression was not negotiated or not supported by one of the peers."""
            return self._sslobj.compression()

        def pending(self):
            """Return the number of bytes that can be read immediately."""
            return self._sslobj.pending()

        def do_handshake(self):
            """Start the SSL/TLS handshake."""
            self._sslobj.do_handshake()

        def unwrap(self):
            """Start the SSL shutdown handshake."""
            return self._sslobj.shutdown()

        def get_channel_binding(self, cb_type='tls-unique'):
            """Get channel binding data for current connection.  Raise ValueError
        if the requested `cb_type` is not supported.  Return bytes of the data
        or None if the data is not available (e.g. before the handshake)."""
            return self._sslobj.get_channel_binding(cb_type)

        def version(self):
            """Return a string identifying the protocol version used by the
        current SSL channel. """
            return self._sslobj.version()

        def verify_client_post_handshake(self):
            return self._sslobj.verify_client_post_handshake()


    def _sslcopydoc(func):
        """Copy docstring from SSLObject to SSLSocket"""
        func.__doc__ = getattr(SSLObject, func.__name__).__doc__
        return func


    class SSLSocket(socket):
        __doc__ = 'This class implements a subtype of socket.socket that wraps\n    the underlying OS socket in an SSL context when necessary, and\n    provides read and write methods over that channel. '

        def __init__(self, *args, **kwargs):
            raise TypeError(f"{self.__class__.__name__} does not have a public constructor. Instances are returned by SSLContext.wrap_socket().")

        @classmethod
        def _create(cls, sock, server_side=False, do_handshake_on_connect=True, suppress_ragged_eofs=True, server_hostname=None, context=None, session=None):
            if sock.getsockoptSOL_SOCKETSO_TYPE != SOCK_STREAM:
                raise NotImplementedError('only stream sockets are supported')
            elif server_side:
                if server_hostname:
                    raise ValueError('server_hostname can only be specified in client mode')
                if session is not None:
                    raise ValueError('session can only be specified in client mode')
            else:
                if context.check_hostname:
                    if not server_hostname:
                        raise ValueError('check_hostname requires server_hostname')
                kwargs = dict(family=(sock.family),
                  type=(sock.type),
                  proto=(sock.proto),
                  fileno=(sock.fileno()))
                self = (cls.__new__)(cls, **kwargs)
                (super(SSLSocket, self).__init__)(**kwargs)
                self.settimeout(sock.gettimeout())
                sock.detach()
                self._context = context
                self._session = session
                self._closed = False
                self._sslobj = None
                self.server_side = server_side
                self.server_hostname = context._encode_hostname(server_hostname)
                self.do_handshake_on_connect = do_handshake_on_connect
                self.suppress_ragged_eofs = suppress_ragged_eofs
                try:
                    self.getpeername()
                except OSError as e:
                    try:
                        if e.errno != errno.ENOTCONN:
                            raise
                        connected = False
                    finally:
                        e = None
                        del e

                else:
                    connected = True
                self._connected = connected
                if connected:
                    try:
                        self._sslobj = self._context._wrap_socket(self,
                          server_side, (self.server_hostname), owner=self,
                          session=(self._session))
                        if do_handshake_on_connect:
                            timeout = self.gettimeout()
                            if timeout == 0.0:
                                raise ValueError('do_handshake_on_connect should not be specified for non-blocking sockets')
                            self.do_handshake()
                    except (OSError, ValueError):
                        self.close()
                        raise

            return self

        @property
        @_sslcopydoc
        def context(self):
            return self._context

        @context.setter
        def context(self, ctx):
            self._context = ctx
            self._sslobj.context = ctx

        @property
        @_sslcopydoc
        def session(self):
            if self._sslobj is not None:
                return self._sslobj.session

        @session.setter
        def session(self, session):
            self._session = session
            if self._sslobj is not None:
                self._sslobj.session = session

        @property
        @_sslcopydoc
        def session_reused(self):
            if self._sslobj is not None:
                return self._sslobj.session_reused

        def dup(self):
            raise NotImplementedError("Can't dup() %s instances" % self.__class__.__name__)

        def _checkClosed(self, msg=None):
            pass

        def _check_connected(self):
            if not self._connected:
                self.getpeername()

        def read--- This code section failed: ---

 L.1094         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _checkClosed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.1095         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _sslobj
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L.1096        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'Read on closed or unwrapped SSL socket.'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.1097        26  SETUP_FINALLY        70  'to 70'

 L.1098        28  LOAD_FAST                'buffer'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L.1099        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _sslobj
               40  LOAD_METHOD              read
               42  LOAD_FAST                'len'
               44  LOAD_FAST                'buffer'
               46  CALL_METHOD_2         2  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM            34  '34'

 L.1101        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _sslobj
               56  LOAD_METHOD              read
               58  LOAD_FAST                'len'
               60  CALL_METHOD_1         1  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
               66  POP_BLOCK        
               68  JUMP_FORWARD        156  'to 156'
             70_0  COME_FROM_FINALLY    26  '26'

 L.1102        70  DUP_TOP          
               72  LOAD_GLOBAL              SSLError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   154  'to 154'
               78  POP_TOP          
               80  STORE_FAST               'x'
               82  POP_TOP          
               84  SETUP_FINALLY       142  'to 142'

 L.1103        86  LOAD_FAST                'x'
               88  LOAD_ATTR                args
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_GLOBAL              SSL_ERROR_EOF
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   136  'to 136'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                suppress_ragged_eofs
              104  POP_JUMP_IF_FALSE   136  'to 136'

 L.1104       106  LOAD_FAST                'buffer'
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L.1105       114  POP_BLOCK        
              116  POP_EXCEPT       
              118  CALL_FINALLY        142  'to 142'
              120  LOAD_CONST               0
              122  RETURN_VALUE     
            124_0  COME_FROM           112  '112'

 L.1107       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        142  'to 142'
              130  LOAD_CONST               b''
              132  RETURN_VALUE     
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           104  '104'
            136_1  COME_FROM            98  '98'

 L.1109       136  RAISE_VARARGS_0       0  'reraise'
            138_0  COME_FROM           134  '134'
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM           128  '128'
            142_1  COME_FROM           118  '118'
            142_2  COME_FROM_FINALLY    84  '84'
              142  LOAD_CONST               None
              144  STORE_FAST               'x'
              146  DELETE_FAST              'x'
              148  END_FINALLY      
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM            76  '76'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM            68  '68'

Parse error at or near `POP_EXCEPT' instruction at offset 116

        def write(self, data):
            """Write DATA to the underlying SSL channel.  Returns
        number of bytes of DATA actually transmitted."""
            self._checkClosed()
            if self._sslobj is None:
                raise ValueError('Write on closed or unwrapped SSL socket.')
            return self._sslobj.write(data)

        @_sslcopydoc
        def getpeercert(self, binary_form=False):
            self._checkClosed()
            self._check_connected()
            return self._sslobj.getpeercert(binary_form)

        @_sslcopydoc
        def selected_npn_protocol(self):
            self._checkClosed()
            return self._sslobj is None or _ssl.HAS_NPN or None
            return self._sslobj.selected_npn_protocol()

        @_sslcopydoc
        def selected_alpn_protocol(self):
            self._checkClosed()
            return self._sslobj is None or _ssl.HAS_ALPN or None
            return self._sslobj.selected_alpn_protocol()

        @_sslcopydoc
        def cipher(self):
            self._checkClosed()
            if self._sslobj is None:
                return
            return self._sslobj.cipher()

        @_sslcopydoc
        def shared_ciphers(self):
            self._checkClosed()
            if self._sslobj is None:
                return
            return self._sslobj.shared_ciphers()

        @_sslcopydoc
        def compression(self):
            self._checkClosed()
            if self._sslobj is None:
                return
            return self._sslobj.compression()

        def send(self, data, flags=0):
            self._checkClosed()
            if self._sslobj is not None:
                if flags != 0:
                    raise ValueError('non-zero flags not allowed in calls to send() on %s' % self.__class__)
                return self._sslobj.write(data)
            return super().senddataflags

        def sendto(self, data, flags_or_addr, addr=None):
            self._checkClosed()
            if self._sslobj is not None:
                raise ValueError('sendto not allowed on instances of %s' % self.__class__)
            else:
                if addr is None:
                    return super().sendtodataflags_or_addr
                return super().sendto(data, flags_or_addr, addr)

        def sendmsg(self, *args, **kwargs):
            raise NotImplementedError('sendmsg not allowed on instances of %s' % self.__class__)

        def sendall(self, data, flags=0):
            self._checkClosed()
            if self._sslobj is not None:
                if flags != 0:
                    raise ValueError('non-zero flags not allowed in calls to sendall() on %s' % self.__class__)
                count = 0
                with memoryview(data) as (view):
                    with view.cast('B') as (byte_view):
                        amount = len(byte_view)
                        while count < amount:
                            v = self.send(byte_view[count:])
                            count += v

            else:
                return super().sendalldataflags

        def sendfile(self, file, offset=0, count=None):
            """Send a file, possibly by using os.sendfile() if this is a
        clear-text socket.  Return the total number of bytes sent.
        """
            if self._sslobj is not None:
                return self._sendfile_use_send(file, offset, count)
            return super().sendfile(file, offset, count)

        def recv(self, buflen=1024, flags=0):
            self._checkClosed()
            if self._sslobj is not None:
                if flags != 0:
                    raise ValueError('non-zero flags not allowed in calls to recv() on %s' % self.__class__)
                return self.read(buflen)
            return super().recvbuflenflags

        def recv_into(self, buffer, nbytes=None, flags=0):
            self._checkClosed()
            if buffer and nbytes is None:
                nbytes = len(buffer)
            else:
                if nbytes is None:
                    nbytes = 1024
            if self._sslobj is not None:
                if flags != 0:
                    raise ValueError('non-zero flags not allowed in calls to recv_into() on %s' % self.__class__)
                return self.readnbytesbuffer
            return super().recv_into(buffer, nbytes, flags)

        def recvfrom(self, buflen=1024, flags=0):
            self._checkClosed()
            if self._sslobj is not None:
                raise ValueError('recvfrom not allowed on instances of %s' % self.__class__)
            else:
                return super().recvfrombuflenflags

        def recvfrom_into(self, buffer, nbytes=None, flags=0):
            self._checkClosed()
            if self._sslobj is not None:
                raise ValueError('recvfrom_into not allowed on instances of %s' % self.__class__)
            else:
                return super().recvfrom_into(buffer, nbytes, flags)

        def recvmsg(self, *args, **kwargs):
            raise NotImplementedError('recvmsg not allowed on instances of %s' % self.__class__)

        def recvmsg_into(self, *args, **kwargs):
            raise NotImplementedError('recvmsg_into not allowed on instances of %s' % self.__class__)

        @_sslcopydoc
        def pending(self):
            self._checkClosed()
            if self._sslobj is not None:
                return self._sslobj.pending()
            return 0

        def shutdown(self, how):
            self._checkClosed()
            self._sslobj = None
            super().shutdown(how)

        @_sslcopydoc
        def unwrap(self):
            if self._sslobj:
                s = self._sslobj.shutdown()
                self._sslobj = None
                return s
            raise ValueError('No SSL wrapper around ' + str(self))

        @_sslcopydoc
        def verify_client_post_handshake(self):
            if self._sslobj:
                return self._sslobj.verify_client_post_handshake()
            raise ValueError('No SSL wrapper around ' + str(self))

        def _real_close(self):
            self._sslobj = None
            super()._real_close()

        @_sslcopydoc
        def do_handshake(self, block=False):
            self._check_connected()
            timeout = self.gettimeout()
            try:
                if timeout == 0.0:
                    if block:
                        self.settimeout(None)
                self._sslobj.do_handshake()
            finally:
                self.settimeout(timeout)

        def _real_connect--- This code section failed: ---

 L.1314         0  LOAD_FAST                'self'
                2  LOAD_ATTR                server_side
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L.1315         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 "can't connect in server-side mode"
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.1318        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _connected
               18  POP_JUMP_IF_TRUE     30  'to 30'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _sslobj
               24  LOAD_CONST               None
               26  COMPARE_OP               is-not
               28  POP_JUMP_IF_FALSE    38  'to 38'
             30_0  COME_FROM            18  '18'

 L.1319        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'attempt to connect already-connected SSLSocket!'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L.1320        38  LOAD_FAST                'self'
               40  LOAD_ATTR                context
               42  LOAD_ATTR                _wrap_socket

 L.1321        44  LOAD_FAST                'self'

 L.1321        46  LOAD_CONST               False

 L.1321        48  LOAD_FAST                'self'
               50  LOAD_ATTR                server_hostname

 L.1322        52  LOAD_FAST                'self'

 L.1322        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _session

 L.1320        58  LOAD_CONST               ('owner', 'session')
               60  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _sslobj

 L.1324        66  SETUP_FINALLY       132  'to 132'

 L.1325        68  LOAD_FAST                'connect_ex'
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L.1326        72  LOAD_GLOBAL              super
               74  CALL_FUNCTION_0       0  ''
               76  LOAD_METHOD              connect_ex
               78  LOAD_FAST                'addr'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'rc'
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM            70  '70'

 L.1328        86  LOAD_CONST               None
               88  STORE_FAST               'rc'

 L.1329        90  LOAD_GLOBAL              super
               92  CALL_FUNCTION_0       0  ''
               94  LOAD_METHOD              connect
               96  LOAD_FAST                'addr'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L.1330       102  LOAD_FAST                'rc'
              104  POP_JUMP_IF_TRUE    126  'to 126'

 L.1331       106  LOAD_CONST               True
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _connected

 L.1332       112  LOAD_FAST                'self'
              114  LOAD_ATTR                do_handshake_on_connect
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L.1333       118  LOAD_FAST                'self'
              120  LOAD_METHOD              do_handshake
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          
            126_0  COME_FROM           116  '116'
            126_1  COME_FROM           104  '104'

 L.1334       126  LOAD_FAST                'rc'
              128  POP_BLOCK        
              130  RETURN_VALUE     
            132_0  COME_FROM_FINALLY    66  '66'

 L.1335       132  DUP_TOP          
              134  LOAD_GLOBAL              OSError
              136  LOAD_GLOBAL              ValueError
              138  BUILD_TUPLE_2         2 
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   162  'to 162'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L.1336       150  LOAD_CONST               None
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _sslobj

 L.1337       156  RAISE_VARARGS_0       0  'reraise'
              158  POP_EXCEPT       
              160  JUMP_FORWARD        164  'to 164'
            162_0  COME_FROM           142  '142'
              162  END_FINALLY      
            164_0  COME_FROM           160  '160'

Parse error at or near `POP_TOP' instruction at offset 146

        def connect(self, addr):
            """Connects to remote ADDR, and then wraps the connection in
        an SSL channel."""
            self._real_connectaddrFalse

        def connect_ex(self, addr):
            """Connects to remote ADDR, and then wraps the connection in
        an SSL channel."""
            return self._real_connectaddrTrue

        def accept(self):
            newsock, addr = super().accept()
            newsock = self.context.wrap_socket(newsock, do_handshake_on_connect=(self.do_handshake_on_connect),
              suppress_ragged_eofs=(self.suppress_ragged_eofs),
              server_side=True)
            return (newsock, addr)

        @_sslcopydoc
        def get_channel_binding(self, cb_type='tls-unique'):
            if self._sslobj is not None:
                return self._sslobj.get_channel_binding(cb_type)
            if cb_type not in CHANNEL_BINDING_TYPES:
                raise ValueError('{0} channel binding type not implemented'.format(cb_type))
            return

        @_sslcopydoc
        def version(self):
            if self._sslobj is not None:
                return self._sslobj.version()
            return


    SSLContext.sslsocket_class = SSLSocket
    SSLContext.sslobject_class = SSLObject

    def wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=CERT_NONE, ssl_version=PROTOCOL_TLS, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None):
        if server_side:
            if not certfile:
                raise ValueError('certfile must be specified for server-side operations')
        if keyfile:
            if not certfile:
                raise ValueError('certfile must be specified')
        context = SSLContext(ssl_version)
        context.verify_mode = cert_reqs
        if ca_certs:
            context.load_verify_locations(ca_certs)
        if certfile:
            context.load_cert_chaincertfilekeyfile
        if ciphers:
            context.set_ciphers(ciphers)
        return context.wrap_socket(sock=sock,
          server_side=server_side,
          do_handshake_on_connect=do_handshake_on_connect,
          suppress_ragged_eofs=suppress_ragged_eofs)


    def cert_time_to_seconds(cert_time):
        """Return the time in seconds since the Epoch, given the timestring
    representing the "notBefore" or "notAfter" date from a certificate
    in ``"%b %d %H:%M:%S %Y %Z"`` strptime format (C locale).

    "notBefore" or "notAfter" dates must use UTC (RFC 5280).

    Month is one of: Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    UTC should be specified as GMT (see ASN1_TIME_print())
    """
        from time import strptime
        from calendar import timegm
        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                  'Nov', 'Dec')
        time_format = ' %d %H:%M:%S %Y GMT'
        try:
            month_number = months.index(cert_time[:3].title()) + 1
        except ValueError:
            raise ValueError('time data %r does not match format "%%b%s"' % (
             cert_time, time_format))
        else:
            tt = strptime(cert_time[3:], time_format)
            return timegm((tt[0], month_number) + tt[2:6])


    PEM_HEADER = '-----BEGIN CERTIFICATE-----'
    PEM_FOOTER = '-----END CERTIFICATE-----'

    def DER_cert_to_PEM_cert(der_cert_bytes):
        """Takes a certificate in binary DER format and returns the
    PEM version of it as a string."""
        f = str(base64.standard_b64encode(der_cert_bytes), 'ASCII', 'strict')
        ss = [PEM_HEADER]
        ss += [f[i:i + 64] for i in range(0, len(f), 64)]
        ss.append(PEM_FOOTER + '\n')
        return '\n'.join(ss)


    def PEM_cert_to_DER_cert(pem_cert_string):
        """Takes a certificate in ASCII PEM format and returns the
    DER-encoded version of it as a byte sequence"""
        if not pem_cert_string.startswith(PEM_HEADER):
            raise ValueError('Invalid PEM encoding; must start with %s' % PEM_HEADER)
        if not pem_cert_string.strip().endswith(PEM_FOOTER):
            raise ValueError('Invalid PEM encoding; must end with %s' % PEM_FOOTER)
        d = pem_cert_string.strip()[len(PEM_HEADER):-len(PEM_FOOTER)]
        return base64.decodebytes(d.encode'ASCII''strict')


    def get_server_certificate(addr, ssl_version=PROTOCOL_TLS, ca_certs=None):
        """Retrieve the certificate from the server at the specified address,
    and return it as a PEM-encoded string.
    If 'ca_certs' is specified, validate the server cert against it.
    If 'ssl_version' is specified, use it in the connection attempt."""
        host, port = addr
        if ca_certs is not None:
            cert_reqs = CERT_REQUIRED
        else:
            cert_reqs = CERT_NONE
        context = _create_stdlib_context(ssl_version, cert_reqs=cert_reqs,
          cafile=ca_certs)
        with create_connection(addr) as (sock):
            with context.wrap_socket(sock) as (sslsock):
                dercert = sslsock.getpeercert(True)
        return DER_cert_to_PEM_cert(dercert)


    def get_protocol_name(protocol_code):
        return _PROTOCOL_NAMES.getprotocol_code'<unknown>'