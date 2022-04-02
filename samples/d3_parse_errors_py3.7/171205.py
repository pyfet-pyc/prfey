# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\urllib3\util\ssl_.py
from __future__ import absolute_import
import errno, warnings, hmac, socket
from binascii import hexlify, unhexlify
from hashlib import md5, sha1, sha256
from ..exceptions import SSLError, InsecurePlatformWarning, SNIMissingWarning
from ..packages import six
SSLContext = None
HAS_SNI = False
IS_PYOPENSSL = False
IS_SECURETRANSPORT = False
HASHFUNC_MAP = {32:md5, 
 40:sha1, 
 64:sha256}

def _const_compare_digest_backport(a, b):
    """
    Compare two digests of equal length in constant time.

    The digests must be of type str/bytes.
    Returns True if the digests match, and False otherwise.
    """
    result = abs(len(a) - len(b))
    for l, r in zip(bytearray(a), bytearray(b)):
        result |= l ^ r

    return result == 0


_const_compare_digest = getattr(hmac, 'compare_digest', _const_compare_digest_backport)
try:
    import ssl
    from ssl import wrap_socket, CERT_NONE, PROTOCOL_SSLv23
    from ssl import HAS_SNI
except ImportError:
    pass

try:
    from ssl import OP_NO_SSLv2, OP_NO_SSLv3, OP_NO_COMPRESSION
except ImportError:
    OP_NO_SSLv2, OP_NO_SSLv3 = (16777216, 33554432)
    OP_NO_COMPRESSION = 131072

if hasattr(socket, 'inet_pton'):
    inet_pton = socket.inet_pton
else:
    try:
        import ipaddress

        def inet_pton(_, host):
            if isinstance(host, bytes):
                host = host.decode('ascii')
            return ipaddress.ip_address(host)


    except ImportError:

        def inet_pton(_, host):
            return socket.inet_aton(host)


DEFAULT_CIPHERS = ':'.join([
 'TLS13-AES-256-GCM-SHA384',
 'TLS13-CHACHA20-POLY1305-SHA256',
 'TLS13-AES-128-GCM-SHA256',
 'ECDH+AESGCM',
 'ECDH+CHACHA20',
 'DH+AESGCM',
 'DH+CHACHA20',
 'ECDH+AES256',
 'DH+AES256',
 'ECDH+AES128',
 'DH+AES',
 'RSA+AESGCM',
 'RSA+AES',
 '!aNULL',
 '!eNULL',
 '!MD5'])
try:
    from ssl import SSLContext
except ImportError:
    import sys

    class SSLContext(object):

        def __init__(self, protocol_version):
            self.protocol = protocol_version
            self.check_hostname = False
            self.verify_mode = ssl.CERT_NONE
            self.ca_certs = None
            self.options = 0
            self.certfile = None
            self.keyfile = None
            self.ciphers = None

        def load_cert_chain(self, certfile, keyfile):
            self.certfile = certfile
            self.keyfile = keyfile

        def load_verify_locations(self, cafile=None, capath=None):
            self.ca_certs = cafile
            if capath is not None:
                raise SSLError('CA directories not supported in older Pythons')

        def set_ciphers(self, cipher_suite):
            self.ciphers = cipher_suite

        def wrap_socket(self, socket, server_hostname=None, server_side=False):
            warnings.warn('A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings', InsecurePlatformWarning)
            kwargs = {'keyfile':self.keyfile, 
             'certfile':self.certfile, 
             'ca_certs':self.ca_certs, 
             'cert_reqs':self.verify_mode, 
             'ssl_version':self.protocol, 
             'server_side':server_side}
            return wrap_socket(socket, ciphers=self.ciphers, **kwargs)


def assert_fingerprint(cert, fingerprint):
    """
    Checks if given fingerprint matches the supplied certificate.

    :param cert:
        Certificate as bytes object.
    :param fingerprint:
        Fingerprint as string of hexdigits, can be interspersed by colons.
    """
    fingerprint = fingerprint.replace(':', '').lower()
    digest_length = len(fingerprint)
    hashfunc = HASHFUNC_MAP.get(digest_length)
    if not hashfunc:
        raise SSLError('Fingerprint of invalid length: {0}'.format(fingerprint))
    fingerprint_bytes = unhexlify(fingerprint.encode())
    cert_digest = hashfunc(cert).digest()
    if not _const_compare_digest(cert_digest, fingerprint_bytes):
        raise SSLError('Fingerprints did not match. Expected "{0}", got "{1}".'.format(fingerprint, hexlify(cert_digest)))


def resolve_cert_reqs(candidate):
    """
    Resolves the argument to a numeric constant, which can be passed to
    the wrap_socket function/method from the ssl module.
    Defaults to :data:`ssl.CERT_NONE`.
    If given a string it is assumed to be the name of the constant in the
    :mod:`ssl` module or its abbreviation.
    (So you can specify `REQUIRED` instead of `CERT_REQUIRED`.
    If it's neither `None` nor a string we assume it is already the numeric
    constant which can directly be passed to wrap_socket.
    """
    if candidate is None:
        return CERT_NONE
    if isinstance(candidate, str):
        res = getattr(ssl, candidate, None)
        if res is None:
            res = getattr(ssl, 'CERT_' + candidate)
        return res
    return candidate


def resolve_ssl_version(candidate):
    """
    like resolve_cert_reqs
    """
    if candidate is None:
        return PROTOCOL_SSLv23
    if isinstance(candidate, str):
        res = getattr(ssl, candidate, None)
        if res is None:
            res = getattr(ssl, 'PROTOCOL_' + candidate)
        return res
    return candidate


def create_urllib3_context(ssl_version=None, cert_reqs=None, options=None, ciphers=None):
    """All arguments have the same meaning as ``ssl_wrap_socket``.

    By default, this function does a lot of the same work that
    ``ssl.create_default_context`` does on Python 3.4+. It:

    - Disables SSLv2, SSLv3, and compression
    - Sets a restricted set of server ciphers

    If you wish to enable SSLv3, you can do::

        from urllib3.util import ssl_
        context = ssl_.create_urllib3_context()
        context.options &= ~ssl_.OP_NO_SSLv3

    You can do the same to enable compression (substituting ``COMPRESSION``
    for ``SSLv3`` in the last line above).

    :param ssl_version:
        The desired protocol version to use. This will default to
        PROTOCOL_SSLv23 which will negotiate the highest protocol that both
        the server and your installation of OpenSSL support.
    :param cert_reqs:
        Whether to require the certificate verification. This defaults to
        ``ssl.CERT_REQUIRED``.
    :param options:
        Specific OpenSSL options. These default to ``ssl.OP_NO_SSLv2``,
        ``ssl.OP_NO_SSLv3``, ``ssl.OP_NO_COMPRESSION``.
    :param ciphers:
        Which cipher suites to allow the server to select.
    :returns:
        Constructed SSLContext object with specified options
    :rtype: SSLContext
    """
    context = SSLContext(ssl_version or ssl.PROTOCOL_SSLv23)
    context.set_ciphers(ciphers or DEFAULT_CIPHERS)
    cert_reqs = ssl.CERT_REQUIRED if cert_reqs is None else cert_reqs
    if options is None:
        options = 0
        options |= OP_NO_SSLv2
        options |= OP_NO_SSLv3
        options |= OP_NO_COMPRESSION
    context.options |= options
    context.verify_mode = cert_reqs
    if getattr(context, 'check_hostname', None) is not None:
        context.check_hostname = False
    return context


def ssl_wrap_socket--- This code section failed: ---

 L. 311         0  LOAD_FAST                'ssl_context'
                2  STORE_FAST               'context'

 L. 312         4  LOAD_FAST                'context'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 316        12  LOAD_GLOBAL              create_urllib3_context
               14  LOAD_FAST                'ssl_version'
               16  LOAD_FAST                'cert_reqs'

 L. 317        18  LOAD_FAST                'ciphers'
               20  LOAD_CONST               ('ciphers',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'context'
             26_0  COME_FROM            10  '10'

 L. 319        26  LOAD_FAST                'ca_certs'
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  LOAD_FAST                'ca_cert_dir'
               32  POP_JUMP_IF_FALSE   150  'to 150'
             34_0  COME_FROM            28  '28'

 L. 320        34  SETUP_EXCEPT         52  'to 52'

 L. 321        36  LOAD_FAST                'context'
               38  LOAD_METHOD              load_verify_locations
               40  LOAD_FAST                'ca_certs'
               42  LOAD_FAST                'ca_cert_dir'
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  POP_TOP          
               48  POP_BLOCK        
               50  JUMP_FORWARD        174  'to 174'
             52_0  COME_FROM_EXCEPT     34  '34'

 L. 322        52  DUP_TOP          
               54  LOAD_GLOBAL              IOError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    92  'to 92'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY        80  'to 80'

 L. 323        68  LOAD_GLOBAL              SSLError
               70  LOAD_FAST                'e'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_BLOCK        
               78  LOAD_CONST               None
             80_0  COME_FROM_FINALLY    66  '66'
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD        174  'to 174'
             92_0  COME_FROM            58  '58'

 L. 326        92  DUP_TOP          
               94  LOAD_GLOBAL              OSError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   146  'to 146'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       134  'to 134'

 L. 327       108  LOAD_FAST                'e'
              110  LOAD_ATTR                errno
              112  LOAD_GLOBAL              errno
              114  LOAD_ATTR                ENOENT
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 328       120  LOAD_GLOBAL              SSLError
              122  LOAD_FAST                'e'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 329       128  RAISE_VARARGS_0       0  'reraise'
              130  POP_BLOCK        
              132  LOAD_CONST               None
            134_0  COME_FROM_FINALLY   106  '106'
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        174  'to 174'
            146_0  COME_FROM            98  '98'
              146  END_FINALLY      
              148  JUMP_FORWARD        174  'to 174'
            150_0  COME_FROM            32  '32'

 L. 330       150  LOAD_GLOBAL              getattr
              152  LOAD_FAST                'context'
              154  LOAD_STR                 'load_default_certs'
              156  LOAD_CONST               None
              158  CALL_FUNCTION_3       3  '3 positional arguments'
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 332       166  LOAD_FAST                'context'
              168  LOAD_METHOD              load_default_certs
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  POP_TOP          
            174_0  COME_FROM_EXCEPT_CLAUSE   164  '164'
            174_1  COME_FROM_EXCEPT_CLAUSE   148  '148'
            174_2  COME_FROM_EXCEPT_CLAUSE   144  '144'
            174_3  COME_FROM_EXCEPT_CLAUSE    90  '90'
            174_4  COME_FROM_EXCEPT_CLAUSE    50  '50'

 L. 334       174  LOAD_FAST                'certfile'
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L. 335       178  LOAD_FAST                'context'
              180  LOAD_METHOD              load_cert_chain
              182  LOAD_FAST                'certfile'
              184  LOAD_FAST                'keyfile'
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  POP_TOP          
            190_0  COME_FROM           176  '176'

 L. 341       190  LOAD_FAST                'server_hostname'
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   206  'to 206'
              198  LOAD_GLOBAL              is_ipaddress
              200  LOAD_FAST                'server_hostname'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  POP_JUMP_IF_FALSE   210  'to 210'
            206_0  COME_FROM           196  '196'

 L. 342       206  LOAD_GLOBAL              IS_SECURETRANSPORT
              208  POP_JUMP_IF_FALSE   248  'to 248'
            210_0  COME_FROM           204  '204'

 L. 343       210  LOAD_GLOBAL              HAS_SNI
              212  POP_JUMP_IF_FALSE   236  'to 236'
              214  LOAD_FAST                'server_hostname'
              216  LOAD_CONST               None
              218  COMPARE_OP               is-not
              220  POP_JUMP_IF_FALSE   236  'to 236'

 L. 344       222  LOAD_FAST                'context'
              224  LOAD_ATTR                wrap_socket
              226  LOAD_FAST                'sock'
              228  LOAD_FAST                'server_hostname'
              230  LOAD_CONST               ('server_hostname',)
              232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              234  RETURN_VALUE     
            236_0  COME_FROM           220  '220'
            236_1  COME_FROM           212  '212'

 L. 346       236  LOAD_GLOBAL              warnings
              238  LOAD_METHOD              warn

 L. 347       240  LOAD_STR                 'An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings'

 L. 354       242  LOAD_GLOBAL              SNIMissingWarning
              244  CALL_METHOD_2         2  '2 positional arguments'
              246  POP_TOP          
            248_0  COME_FROM           208  '208'

 L. 357       248  LOAD_FAST                'context'
              250  LOAD_METHOD              wrap_socket
              252  LOAD_FAST                'sock'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 174_0


def is_ipaddress(hostname):
    """Detects whether the hostname given is an IP address.

    :param str hostname: Hostname to examine.
    :return: True if the hostname is an IP address, False otherwise.
    """
    if six.PY3:
        if isinstance(hostname, bytes):
            hostname = hostname.decode('ascii')
    families = [
     socket.AF_INET]
    if hasattr(socket, 'AF_INET6'):
        families.append(socket.AF_INET6)
    for af in families:
        try:
            inet_pton(af, hostname)
        except (socket.error, ValueError, OSError):
            pass
        else:
            return True

    return False