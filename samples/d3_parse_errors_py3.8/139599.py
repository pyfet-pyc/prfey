# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\ssl_support.py
import os, socket, atexit, re, functools, urllib.request, http.client
from pkg_resources import ResolutionError, ExtractionError
try:
    import ssl
except ImportError:
    ssl = None
else:
    __all__ = [
     'VerifyingHTTPSHandler', 'find_ca_bundle', 'is_available', 'cert_paths',
     'opener_for']
    cert_paths = '\n/etc/pki/tls/certs/ca-bundle.crt\n/etc/ssl/certs/ca-certificates.crt\n/usr/share/ssl/certs/ca-bundle.crt\n/usr/local/share/certs/ca-root.crt\n/etc/ssl/cert.pem\n/System/Library/OpenSSL/certs/cert.pem\n/usr/local/share/certs/ca-root-nss.crt\n/etc/ssl/ca-bundle.pem\n'.strip().split()
    try:
        HTTPSHandler = urllib.request.HTTPSHandler
        HTTPSConnection = http.client.HTTPSConnection
    except AttributeError:
        HTTPSHandler = HTTPSConnection = object
    else:
        is_available = ssl is not None and object not in (
         HTTPSHandler, HTTPSConnection)
        try:
            from ssl import CertificateError, match_hostname
        except ImportError:
            try:
                from backports.ssl_match_hostname import CertificateError
                from backports.ssl_match_hostname import match_hostname
            except ImportError:
                CertificateError = None
                match_hostname = None

        else:
            if not CertificateError:

                class CertificateError(ValueError):
                    pass


            if not match_hostname:

                def _dnsname_match(dn, hostname, max_wildcards=1):
                    """Matching according to RFC 6125, section 6.4.3

        https://tools.ietf.org/html/rfc6125#section-6.4.3
        """
                    pats = []
                    if not dn:
                        return False
                    parts = dn.split('.')
                    leftmost = parts[0]
                    remainder = parts[1:]
                    wildcards = leftmost.count('*')
                    if wildcards > max_wildcards:
                        raise CertificateError('too many wildcards in certificate DNS name: ' + repr(dn))
                    if not wildcards:
                        return dn.lower() == hostname.lower()
                    if leftmost == '*':
                        pats.append('[^.]+')
                    elif leftmost.startswith('xn--') or hostname.startswith('xn--'):
                        pats.append(re.escape(leftmost))
                    else:
                        pats.append(re.escape(leftmost).replace('\\*', '[^.]*'))
                    for frag in remainder:
                        pats.append(re.escape(frag))
                    else:
                        pat = re.compile('\\A' + '\\.'.join(pats) + '\\Z', re.IGNORECASE)
                        return pat.match(hostname)


                def match_hostname(cert, hostname):
                    """Verify that *cert* (in decoded format as returned by
        SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
        rules are followed, but IP addresses are not accepted for *hostname*.

        CertificateError is raised on failure. On success, the function
        returns nothing.
        """
                    if not cert:
                        raise ValueError('empty or no certificate')
                    dnsnames = []
                    san = cert.get('subjectAltName', ())
                    for key, value in san:
                        if key == 'DNS':
                            if _dnsname_match(value, hostname):
                                return None
                            else:
                                dnsnames.append(value)

                    for sub in dnsnames or cert.get('subject', ()):
                        for key, value in sub:
                            if key == 'commonName':
                                if _dnsname_match(value, hostname):
                                    return None
                                else:
                                    dnsnames.append(value)

                    else:
                        if len(dnsnames) > 1:
                            raise CertificateError("hostname %r doesn't match either of %s" % (
                             hostname, ', '.join(map(repr, dnsnames))))
                        elif len(dnsnames) == 1:
                            raise CertificateError("hostname %r doesn't match %r" % (
                             hostname, dnsnames[0]))
                        else:
                            raise CertificateError('no appropriate commonName or subjectAltName fields were found')


            class VerifyingHTTPSHandler(HTTPSHandler):
                __doc__ = 'Simple verifying handler: no auth, subclasses, timeouts, etc.'

                def __init__(self, ca_bundle):
                    self.ca_bundle = ca_bundle
                    HTTPSHandler.__init__(self)

                def https_open(self, req):
                    return self.do_open(lambda host, **kw: VerifyingHTTPSConn(host, (self.ca_bundle), **kw), req)


            class VerifyingHTTPSConn(HTTPSConnection):
                __doc__ = 'Simple verifying connection: no auth, subclasses, timeouts, etc.'

                def __init__(self, host, ca_bundle, **kw):
                    (HTTPSConnection.__init__)(self, host, **kw)
                    self.ca_bundle = ca_bundle

                def connect(self):
                    sock = socket.create_connection((
                     self.host, self.port), getattr(self, 'source_address', None))
                    if hasattr(self, '_tunnel') and getattr(self, '_tunnel_host', None):
                        self.sock = sock
                        self._tunnel()
                        actual_host = self._tunnel_host
                    else:
                        actual_host = self.host
                    if hasattr(ssl, 'create_default_context'):
                        ctx = ssl.create_default_context(cafile=(self.ca_bundle))
                        self.sock = ctx.wrap_socket(sock, server_hostname=actual_host)
                    else:
                        self.sock = ssl.wrap_socket(sock,
                          cert_reqs=(ssl.CERT_REQUIRED), ca_certs=(self.ca_bundle))
                    try:
                        match_hostname(self.sock.getpeercert(), actual_host)
                    except CertificateError:
                        self.sock.shutdown(socket.SHUT_RDWR)
                        self.sock.close()
                        raise


            def opener_for(ca_bundle=None):
                """Get a urlopen() replacement that uses ca_bundle for verification"""
                return urllib.request.build_opener(VerifyingHTTPSHandler(ca_bundle or find_ca_bundle())).open


            def once(func):

                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    if not hasattr(func, 'always_returns'):
                        func.always_returns = func(*args, **kwargs)
                    return func.always_returns

                return wrapper


            @once
            def get_win_certfile():
                try:
                    import wincertstore
                except ImportError:
                    return
                else:

                    class CertFile(wincertstore.CertFile):

                        def __init__(self):
                            super(CertFile, self).__init__()
                            atexit.register(self.close)

                        def close(self):
                            try:
                                super(CertFile, self).close()
                            except OSError:
                                pass

                    _wincerts = CertFile()
                    _wincerts.addstore('CA')
                    _wincerts.addstore('ROOT')
                    return _wincerts.name


            def find_ca_bundle():
                """Return an existing CA bundle path, or None"""
                extant_cert_paths = filter(os.path.isfile, cert_paths)
                return get_win_certfile() or next(extant_cert_paths, None) or _certifi_where()


            def _certifi_where--- This code section failed: ---

 L. 263         0  SETUP_FINALLY        16  'to 16'

 L. 264         2  LOAD_GLOBAL              __import__
                4  LOAD_STR                 'certifi'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_METHOD              where
               10  CALL_METHOD_0         0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 265        16  DUP_TOP          
               18  LOAD_GLOBAL              ImportError
               20  LOAD_GLOBAL              ResolutionError
               22  LOAD_GLOBAL              ExtractionError
               24  BUILD_TUPLE_3         3 
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    40  'to 40'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 266        36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            28  '28'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

Parse error at or near `COME_FROM' instruction at offset 40_0