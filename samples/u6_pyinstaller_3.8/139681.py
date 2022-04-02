# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib3\util\ssl_.py
from __future__ import absolute_import
import hmac, os, sys, warnings
from binascii import hexlify, unhexlify
from hashlib import md5, sha1, sha256
from ..exceptions import InsecurePlatformWarning, ProxySchemeUnsupported, SNIMissingWarning, SSLError
from ..packages import six
from .url import BRACELESS_IPV6_ADDRZ_RE, IPV4_RE
SSLContext = None
SSLTransport = None
HAS_SNI = False
IS_PYOPENSSL = False
IS_SECURETRANSPORT = False
ALPN_PROTOCOLS = ['http/1.1']
HASHFUNC_MAP = {32:md5, 
 40:sha1,  64:sha256}

def _const_compare_digest_backport(a, b):
    """
    Compare two digests of equal length in constant time.

    The digests must be of type str/bytes.
    Returns True if the digests match, and False otherwise.
    """
    result = abs(len(a) - len(b))
    for left, right in zip(bytearray(a), bytearray(b)):
        result |= left ^ right
    else:
        return result == 0


_const_compare_digest = getattr(hmac, 'compare_digest', _const_compare_digest_backport)
try:
    import ssl
    from ssl import CERT_REQUIRED, wrap_socket
except ImportError:
    pass

try:
    from ssl import HAS_SNI
except ImportError:
    pass

try:
    from .ssltransport import SSLTransport
except ImportError:
    pass

try:
    from ssl import PROTOCOL_TLS
    PROTOCOL_SSLv23 = PROTOCOL_TLS
except ImportError:
    try:
        from ssl import PROTOCOL_SSLv23 as PROTOCOL_TLS
        PROTOCOL_SSLv23 = PROTOCOL_TLS
    except ImportError:
        PROTOCOL_SSLv23 = PROTOCOL_TLS = 2

try:
    from ssl import OP_NO_COMPRESSION, OP_NO_SSLv2, OP_NO_SSLv3
except ImportError:
    OP_NO_SSLv2, OP_NO_SSLv3 = (16777216, 33554432)
    OP_NO_COMPRESSION = 131072

try:
    from ssl import OP_NO_TICKET
except ImportError:
    OP_NO_TICKET = 16384
else:
    DEFAULT_CIPHERS = ':'.join([
     'ECDHE+AESGCM',
     'ECDHE+CHACHA20',
     'DHE+AESGCM',
     'DHE+CHACHA20',
     'ECDH+AESGCM',
     'DH+AESGCM',
     'ECDH+AES',
     'DH+AES',
     'RSA+AESGCM',
     'RSA+AES',
     '!aNULL',
     '!eNULL',
     '!MD5',
     '!DSS'])
    try:
        from ssl import SSLContext
    except ImportError:

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

            def load_verify_locations(self, cafile=None, capath=None, cadata=None):
                self.ca_certs = cafile
                if capath is not None:
                    raise SSLError('CA directories not supported in older Pythons')
                if cadata is not None:
                    raise SSLError('CA data not supported in older Pythons')

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


    else:

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
    Defaults to :data:`ssl.CERT_REQUIRED`.
    If given a string it is assumed to be the name of the constant in the
    :mod:`ssl` module or its abbreviation.
    (So you can specify `REQUIRED` instead of `CERT_REQUIRED`.
    If it's neither `None` nor a string we assume it is already the numeric
    constant which can directly be passed to wrap_socket.
    """
            if candidate is None:
                return CERT_REQUIRED
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
                return PROTOCOL_TLS
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
        ``ssl.OP_NO_SSLv3``, ``ssl.OP_NO_COMPRESSION``, and ``ssl.OP_NO_TICKET``.
    :param ciphers:
        Which cipher suites to allow the server to select.
    :returns:
        Constructed SSLContext object with specified options
    :rtype: SSLContext
    """
            context = SSLContext(ssl_version or PROTOCOL_TLS)
            context.set_ciphers(ciphers or DEFAULT_CIPHERS)
            cert_reqs = ssl.CERT_REQUIRED if cert_reqs is None else cert_reqs
            if options is None:
                options = 0
                options |= OP_NO_SSLv2
                options |= OP_NO_SSLv3
                options |= OP_NO_COMPRESSION
                options |= OP_NO_TICKET
            context.options |= options
            if cert_reqs == ssl.CERT_REQUIRED or sys.version_info >= (3, 7, 4):
                if getattr(context, 'post_handshake_auth', None) is not None:
                    context.post_handshake_auth = True
            context.verify_mode = cert_reqs
            if getattr(context, 'check_hostname', None) is not None:
                context.check_hostname = False
            if hasattr(context, 'keylog_filename'):
                sslkeylogfile = os.environ.get('SSLKEYLOGFILE')
                if sslkeylogfile:
                    context.keylog_filename = sslkeylogfile
            return context


        def ssl_wrap_socket(sock, keyfile=None, certfile=None, cert_reqs=None, ca_certs=None, server_hostname=None, ssl_version=None, ciphers=None, ssl_context=None, ca_cert_dir=None, key_password=None, ca_cert_data=None, tls_in_tls=False):
            """
    All arguments except for server_hostname, ssl_context, and ca_cert_dir have
    the same meaning as they do when using :func:`ssl.wrap_socket`.

    :param server_hostname:
        When SNI is supported, the expected hostname of the certificate
    :param ssl_context:
        A pre-made :class:`SSLContext` object. If none is provided, one will
        be created using :func:`create_urllib3_context`.
    :param ciphers:
        A string of ciphers we wish the client to support.
    :param ca_cert_dir:
        A directory containing CA certificates in multiple separate files, as
        supported by OpenSSL's -CApath flag or the capath argument to
        SSLContext.load_verify_locations().
    :param key_password:
        Optional password if the keyfile is encrypted.
    :param ca_cert_data:
        Optional string containing CA certificates in PEM format suitable for
        passing as the cadata parameter to SSLContext.load_verify_locations()
    :param tls_in_tls:
        Use SSLTransport to wrap the existing socket.
    """
            context = ssl_context
            if context is None:
                context = create_urllib3_context(ssl_version, cert_reqs, ciphers=ciphers)
            elif not ca_certs:
                if ca_cert_dir or ca_cert_data:
                    try:
                        context.load_verify_locations(ca_certs, ca_cert_dir, ca_cert_data)
                    except (IOError, OSError) as e:
                        try:
                            raise SSLError(e)
                        finally:
                            e = None
                            del e

            elif ssl_context is None and hasattr(context, 'load_default_certs'):
                context.load_default_certs()
            if keyfile:
                if key_password is None:
                    if _is_key_file_encrypted(keyfile):
                        raise SSLError('Client private key is encrypted, password is required')
            elif certfile:
                if key_password is None:
                    context.load_cert_chain(certfile, keyfile)
                else:
                    context.load_cert_chain(certfile, keyfile, key_password)
            try:
                if hasattr(context, 'set_alpn_protocols'):
                    context.set_alpn_protocols(ALPN_PROTOCOLS)
            except NotImplementedError:
                pass
            else:
                use_sni_hostname = server_hostname and not is_ipaddress(server_hostname)
                send_sni = use_sni_hostname and HAS_SNI or IS_SECURETRANSPORT and server_hostname
                if not HAS_SNI:
                    if use_sni_hostname:
                        warnings.warn('An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings', SNIMissingWarning)
                elif send_sni:
                    ssl_sock = _ssl_wrap_socket_impl(sock,
                      context, tls_in_tls, server_hostname=server_hostname)
                else:
                    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls)
                return ssl_sock


        def is_ipaddress(hostname):
            """Detects whether the hostname given is an IPv4 or IPv6 address.
    Also detects IPv6 addresses with Zone IDs.

    :param str hostname: Hostname to examine.
    :return: True if the hostname is an IP address, False otherwise.
    """
            if not six.PY2:
                if isinstance(hostname, bytes):
                    hostname = hostname.decode('ascii')
            return bool(IPV4_RE.match(hostname) or BRACELESS_IPV6_ADDRZ_RE.match(hostname))


        def _is_key_file_encrypted--- This code section failed: ---

 L. 451         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'key_file'
                4  LOAD_STR                 'r'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           50  'to 50'
               10  STORE_FAST               'f'

 L. 452        12  LOAD_FAST                'f'
               14  GET_ITER         
             16_0  COME_FROM            26  '26'
               16  FOR_ITER             46  'to 46'
               18  STORE_FAST               'line'

 L. 454        20  LOAD_STR                 'ENCRYPTED'
               22  LOAD_FAST                'line'
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    16  'to 16'

 L. 455        28  POP_TOP          
               30  POP_BLOCK        
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  LOAD_CONST               True
               42  RETURN_VALUE     
               44  JUMP_BACK            16  'to 16'
               46  POP_BLOCK        
               48  BEGIN_FINALLY    
             50_0  COME_FROM_WITH        8  '8'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

 L. 457        56  LOAD_CONST               False
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `WITH_CLEANUP_START' instruction at offset 34


        def _ssl_wrap_socket_impl(sock, ssl_context, tls_in_tls, server_hostname=None):
            if tls_in_tls:
                if not SSLTransport:
                    raise ProxySchemeUnsupported("TLS in TLS requires support for the 'ssl' module")
                SSLTransport._validate_ssl_context_for_tls_in_tls(ssl_context)
                return SSLTransport(sock, ssl_context, server_hostname)
            if server_hostname:
                return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
            return ssl_context.wrap_socket(sock)