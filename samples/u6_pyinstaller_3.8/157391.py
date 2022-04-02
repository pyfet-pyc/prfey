# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\ssl_support.py
import os, socket, atexit, re, functools
from setuptools.extern.six.moves import urllib, http_client, map, filter
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
    HTTPSConnection = http_client.HTTPSConnection
except AttributeError:
    HTTPSHandler = HTTPSConnection = object
else:
    is_available = ssl is not None and object not in (HTTPSHandler, HTTPSConnection)
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
                elif not wildcards:
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


            def match_hostname--- This code section failed: ---

 L. 119         0  LOAD_FAST                'cert'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 120         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'empty or no certificate'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 121        12  BUILD_LIST_0          0 
               14  STORE_FAST               'dnsnames'

 L. 122        16  LOAD_FAST                'cert'
               18  LOAD_METHOD              get
               20  LOAD_STR                 'subjectAltName'
               22  LOAD_CONST               ()
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'san'

 L. 123        28  LOAD_FAST                'san'
               30  GET_ITER         
             32_0  COME_FROM            46  '46'
               32  FOR_ITER             76  'to 76'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'key'
               38  STORE_FAST               'value'

 L. 124        40  LOAD_FAST                'key'
               42  LOAD_STR                 'DNS'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    32  'to 32'

 L. 125        48  LOAD_GLOBAL              _dnsname_match
               50  LOAD_FAST                'value'
               52  LOAD_FAST                'hostname'
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 126        58  POP_TOP          
               60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            56  '56'

 L. 127        64  LOAD_FAST                'dnsnames'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'value'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_BACK            32  'to 32'

 L. 128        76  LOAD_FAST                'dnsnames'
               78  POP_JUMP_IF_TRUE    148  'to 148'

 L. 131        80  LOAD_FAST                'cert'
               82  LOAD_METHOD              get
               84  LOAD_STR                 'subject'
               86  LOAD_CONST               ()
               88  CALL_METHOD_2         2  ''
               90  GET_ITER         
               92  FOR_ITER            148  'to 148'
               94  STORE_FAST               'sub'

 L. 132        96  LOAD_FAST                'sub'
               98  GET_ITER         
            100_0  COME_FROM           114  '114'
              100  FOR_ITER            146  'to 146'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'key'
              106  STORE_FAST               'value'

 L. 135       108  LOAD_FAST                'key'
              110  LOAD_STR                 'commonName'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   100  'to 100'

 L. 136       116  LOAD_GLOBAL              _dnsname_match
              118  LOAD_FAST                'value'
              120  LOAD_FAST                'hostname'
              122  CALL_FUNCTION_2       2  ''
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L. 137       126  POP_TOP          
              128  POP_TOP          
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           124  '124'

 L. 138       134  LOAD_FAST                'dnsnames'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'value'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK           100  'to 100'
              146  JUMP_BACK            92  'to 92'
            148_0  COME_FROM            78  '78'

 L. 139       148  LOAD_GLOBAL              len
              150  LOAD_FAST                'dnsnames'
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_CONST               1
              156  COMPARE_OP               >
              158  POP_JUMP_IF_FALSE   190  'to 190'

 L. 140       160  LOAD_GLOBAL              CertificateError
              162  LOAD_STR                 "hostname %r doesn't match either of %s"

 L. 142       164  LOAD_FAST                'hostname'
              166  LOAD_STR                 ', '
              168  LOAD_METHOD              join
              170  LOAD_GLOBAL              map
              172  LOAD_GLOBAL              repr
              174  LOAD_FAST                'dnsnames'
              176  CALL_FUNCTION_2       2  ''
              178  CALL_METHOD_1         1  ''
              180  BUILD_TUPLE_2         2 

 L. 140       182  BINARY_MODULO    
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
              188  JUMP_FORWARD        232  'to 232'
            190_0  COME_FROM           158  '158'

 L. 143       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'dnsnames'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               1
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   224  'to 224'

 L. 144       202  LOAD_GLOBAL              CertificateError
              204  LOAD_STR                 "hostname %r doesn't match %r"

 L. 146       206  LOAD_FAST                'hostname'
              208  LOAD_FAST                'dnsnames'
              210  LOAD_CONST               0
              212  BINARY_SUBSCR    
              214  BUILD_TUPLE_2         2 

 L. 144       216  BINARY_MODULO    
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
              222  JUMP_FORWARD        232  'to 232'
            224_0  COME_FROM           200  '200'

 L. 148       224  LOAD_GLOBAL              CertificateError
              226  LOAD_STR                 'no appropriate commonName or subjectAltName fields were found'
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           188  '188'

Parse error at or near `JUMP_BACK' instruction at offset 146


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
                if hasattrself'_tunnel':
                    if getattr(self, '_tunnel_host', None):
                        self.sock = sock
                        self._tunnel()
                        actual_host = self._tunnel_host
                    else:
                        actual_host = self.host
                elif hasattrssl'create_default_context':
                    ctx = ssl.create_default_context(cafile=(self.ca_bundle))
                    self.sock = ctx.wrap_socket(sock, server_hostname=actual_host)
                else:
                    self.sock = ssl.wrap_socket(sock,
                      cert_reqs=(ssl.CERT_REQUIRED), ca_certs=(self.ca_bundle))
                try:
                    match_hostnameself.sock.getpeercert()actual_host
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
                if not hasattrfunc'always_returns':
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
                        superCertFileself.__init__()
                        atexit.register(self.close)

                    def close(self):
                        try:
                            superCertFileself.close()
                        except OSError:
                            pass

                _wincerts = CertFile()
                _wincerts.addstore('CA')
                _wincerts.addstore('ROOT')
                return _wincerts.name


        def find_ca_bundle():
            """Return an existing CA bundle path, or None"""
            extant_cert_paths = filteros.path.isfilecert_paths
            return get_win_certfile() or nextextant_cert_pathsNone or _certifi_where()


        def _certifi_where--- This code section failed: ---

 L. 257         0  SETUP_FINALLY        16  'to 16'

 L. 258         2  LOAD_GLOBAL              __import__
                4  LOAD_STR                 'certifi'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_METHOD              where
               10  CALL_METHOD_0         0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 259        16  DUP_TOP          
               18  LOAD_GLOBAL              ImportError
               20  LOAD_GLOBAL              ResolutionError
               22  LOAD_GLOBAL              ExtractionError
               24  BUILD_TUPLE_3         3 
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    40  'to 40'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 260        36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            28  '28'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

Parse error at or near `POP_TOP' instruction at offset 32