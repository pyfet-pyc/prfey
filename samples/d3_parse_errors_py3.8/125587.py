# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib3\contrib\pyopenssl.py
"""
TLS with SNI_-support for Python 2. Follow these instructions if you would
like to verify TLS certificates in Python 2. Note, the default libraries do
*not* do certificate checking; you need to do additional work to validate
certificates yourself.

This needs the following packages installed:

* `pyOpenSSL`_ (tested with 16.0.0)
* `cryptography`_ (minimum 1.3.4, from pyopenssl)
* `idna`_ (minimum 2.0, from cryptography)

However, pyopenssl depends on cryptography, which depends on idna, so while we
use all three directly here we end up having relatively few packages required.

You can install them with the following command:

.. code-block:: bash

    $ python -m pip install pyopenssl cryptography idna

To activate certificate checking, call
:func:`~urllib3.contrib.pyopenssl.inject_into_urllib3` from your Python code
before you begin making HTTP requests. This can be done in a ``sitecustomize``
module, or at any other time before your application begins using ``urllib3``,
like this:

.. code-block:: python

    try:
        import urllib3.contrib.pyopenssl
        urllib3.contrib.pyopenssl.inject_into_urllib3()
    except ImportError:
        pass

Now you can use :mod:`urllib3` as you normally would, and it will support SNI
when the required modules are installed.

Activating this module also has the positive side effect of disabling SSL/TLS
compression in Python 2 (see `CRIME attack`_).

.. _sni: https://en.wikipedia.org/wiki/Server_Name_Indication
.. _crime attack: https://en.wikipedia.org/wiki/CRIME_(security_exploit)
.. _pyopenssl: https://www.pyopenssl.org
.. _cryptography: https://cryptography.io
.. _idna: https://github.com/kjd/idna
"""
from __future__ import absolute_import
import OpenSSL.SSL
from cryptography import x509
import cryptography.hazmat.backends.openssl as openssl_backend
from cryptography.hazmat.backends.openssl.x509 import _Certificate
try:
    from cryptography.x509 import UnsupportedExtension
except ImportError:

    class UnsupportedExtension(Exception):
        pass


else:
    from io import BytesIO
    from socket import error as SocketError
    from socket import timeout
    try:
        from socket import _fileobject
    except ImportError:
        _fileobject = None
        from packages.backports.makefile import backport_makefile
    else:
        import logging, ssl, sys
        from .. import util
        from ..packages import six
        __all__ = [
         'inject_into_urllib3', 'extract_from_urllib3']
        HAS_SNI = True
        _openssl_versions = {util.PROTOCOL_TLS: OpenSSL.SSL.SSLv23_METHOD, 
         ssl.PROTOCOL_TLSv1: OpenSSL.SSL.TLSv1_METHOD}
        if hasattr(ssl, 'PROTOCOL_SSLv3'):
            if hasattr(OpenSSL.SSL, 'SSLv3_METHOD'):
                _openssl_versions[ssl.PROTOCOL_SSLv3] = OpenSSL.SSL.SSLv3_METHOD
        if hasattr(ssl, 'PROTOCOL_TLSv1_1'):
            if hasattr(OpenSSL.SSL, 'TLSv1_1_METHOD'):
                _openssl_versions[ssl.PROTOCOL_TLSv1_1] = OpenSSL.SSL.TLSv1_1_METHOD
        if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
            if hasattr(OpenSSL.SSL, 'TLSv1_2_METHOD'):
                _openssl_versions[ssl.PROTOCOL_TLSv1_2] = OpenSSL.SSL.TLSv1_2_METHOD
        _stdlib_to_openssl_verify = {ssl.CERT_NONE: OpenSSL.SSL.VERIFY_NONE, 
         ssl.CERT_OPTIONAL: OpenSSL.SSL.VERIFY_PEER, 
         ssl.CERT_REQUIRED: OpenSSL.SSL.VERIFY_PEER + OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT}
        _openssl_to_stdlib_verify = dict(((v, k) for k, v in _stdlib_to_openssl_verify.items()))
        SSL_WRITE_BLOCKSIZE = 16384
        orig_util_HAS_SNI = util.HAS_SNI
        orig_util_SSLContext = util.ssl_.SSLContext
        log = logging.getLogger(__name__)

        def inject_into_urllib3():
            """Monkey-patch urllib3 with PyOpenSSL-backed SSL-support."""
            _validate_dependencies_met()
            util.SSLContext = PyOpenSSLContext
            util.ssl_.SSLContext = PyOpenSSLContext
            util.HAS_SNI = HAS_SNI
            util.ssl_.HAS_SNI = HAS_SNI
            util.IS_PYOPENSSL = True
            util.ssl_.IS_PYOPENSSL = True


        def extract_from_urllib3():
            """Undo monkey-patching by :func:`inject_into_urllib3`."""
            util.SSLContext = orig_util_SSLContext
            util.ssl_.SSLContext = orig_util_SSLContext
            util.HAS_SNI = orig_util_HAS_SNI
            util.ssl_.HAS_SNI = orig_util_HAS_SNI
            util.IS_PYOPENSSL = False
            util.ssl_.IS_PYOPENSSL = False


        def _validate_dependencies_met():
            """
    Verifies that PyOpenSSL's package-level dependencies have been met.
    Throws `ImportError` if they are not met.
    """
            from cryptography.x509.extensions import Extensions
            if getattr(Extensions, 'get_extension_for_class', None) is None:
                raise ImportError("'cryptography' module missing required functionality.  Try upgrading to v1.3.4 or newer.")
            from OpenSSL.crypto import X509
            x509 = X509()
            if getattr(x509, '_x509', None) is None:
                raise ImportError("'pyOpenSSL' module missing required functionality. Try upgrading to v0.14 or newer.")


        def _dnsname_to_stdlib(name):
            """
    Converts a dNSName SubjectAlternativeName field to the form used by the
    standard library on the given Python version.

    Cryptography produces a dNSName as a unicode string that was idna-decoded
    from ASCII bytes. We need to idna-encode that string to get it back, and
    then on Python 3 we also need to convert to unicode via UTF-8 (the stdlib
    uses PyUnicode_FromStringAndSize on it, which decodes via UTF-8).

    If the name cannot be idna-encoded then we return None signalling that
    the name given should be skipped.
    """

            def idna_encode--- This code section failed: ---

 L. 189         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              idna
                6  STORE_FAST               'idna'

 L. 191         8  SETUP_FINALLY        84  'to 84'

 L. 192        10  LOAD_CONST               ('*.', '.')
               12  GET_ITER         
             14_0  COME_FROM            70  '70'
             14_1  COME_FROM            26  '26'
               14  FOR_ITER             72  'to 72'
               16  STORE_FAST               'prefix'

 L. 193        18  LOAD_FAST                'name'
               20  LOAD_METHOD              startswith
               22  LOAD_FAST                'prefix'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 194        28  LOAD_FAST                'name'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'prefix'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  STORE_FAST               'name'

 L. 195        44  LOAD_FAST                'prefix'
               46  LOAD_METHOD              encode
               48  LOAD_STR                 'ascii'
               50  CALL_METHOD_1         1  ''
               52  LOAD_FAST                'idna'
               54  LOAD_METHOD              encode
               56  LOAD_FAST                'name'
               58  CALL_METHOD_1         1  ''
               60  BINARY_ADD       
               62  ROT_TWO          
               64  POP_TOP          
               66  POP_BLOCK        
               68  RETURN_VALUE     
               70  JUMP_BACK            14  'to 14'
             72_0  COME_FROM            14  '14'

 L. 196        72  LOAD_FAST                'idna'
               74  LOAD_METHOD              encode
               76  LOAD_FAST                'name'
               78  CALL_METHOD_1         1  ''
               80  POP_BLOCK        
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY     8  '8'

 L. 197        84  DUP_TOP          
               86  LOAD_FAST                'idna'
               88  LOAD_ATTR                core
               90  LOAD_ATTR                IDNAError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   108  'to 108'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 198       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            94  '94'
              108  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 66

            if ':' in name:
                return name
            name = idna_encode(name)
            if name is None:
                return
            if sys.version_info >= (3, 0):
                name = name.decode('utf-8')
            return name


        def get_subj_alt_name--- This code section failed: ---

 L. 217         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'peer_cert'
                4  LOAD_STR                 'to_cryptography'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 218        10  LOAD_FAST                'peer_cert'
               12  LOAD_METHOD              to_cryptography
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'cert'
               18  JUMP_FORWARD         32  'to 32'
             20_0  COME_FROM             8  '8'

 L. 222        20  LOAD_GLOBAL              _Certificate
               22  LOAD_GLOBAL              openssl_backend
               24  LOAD_FAST                'peer_cert'
               26  LOAD_ATTR                _x509
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'cert'
             32_0  COME_FROM            18  '18'

 L. 226        32  SETUP_FINALLY        54  'to 54'

 L. 227        34  LOAD_FAST                'cert'
               36  LOAD_ATTR                extensions
               38  LOAD_METHOD              get_extension_for_class
               40  LOAD_GLOBAL              x509
               42  LOAD_ATTR                SubjectAlternativeName
               44  CALL_METHOD_1         1  ''
               46  LOAD_ATTR                value
               48  STORE_FAST               'ext'
               50  POP_BLOCK        
               52  JUMP_FORWARD        144  'to 144'
             54_0  COME_FROM_FINALLY    32  '32'

 L. 228        54  DUP_TOP          
               56  LOAD_GLOBAL              x509
               58  LOAD_ATTR                ExtensionNotFound
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    78  'to 78'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 230        70  BUILD_LIST_0          0 
               72  ROT_FOUR         
               74  POP_EXCEPT       
               76  RETURN_VALUE     
             78_0  COME_FROM            62  '62'

 L. 231        78  DUP_TOP          

 L. 232        80  LOAD_GLOBAL              x509
               82  LOAD_ATTR                DuplicateExtension

 L. 233        84  LOAD_GLOBAL              UnsupportedExtension

 L. 234        86  LOAD_GLOBAL              x509
               88  LOAD_ATTR                UnsupportedGeneralNameType

 L. 235        90  LOAD_GLOBAL              UnicodeError

 L. 231        92  BUILD_TUPLE_4         4 
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   142  'to 142'
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       130  'to 130'

 L. 239       106  LOAD_GLOBAL              log
              108  LOAD_METHOD              warning

 L. 240       110  LOAD_STR                 'A problem was encountered with the certificate that prevented urllib3 from finding the SubjectAlternativeName field. This can affect certificate validation. The error was %s'

 L. 243       112  LOAD_FAST                'e'

 L. 239       114  CALL_METHOD_2         2  ''
              116  POP_TOP          

 L. 245       118  BUILD_LIST_0          0 
              120  ROT_FOUR         
              122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        130  'to 130'
              128  RETURN_VALUE     
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM_FINALLY   104  '104'
              130  LOAD_CONST               None
              132  STORE_FAST               'e'
              134  DELETE_FAST              'e'
              136  END_FINALLY      
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM            96  '96'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM            52  '52'

 L. 254       144  LOAD_LISTCOMP            '<code_object <listcomp>>'
              146  LOAD_STR                 'get_subj_alt_name.<locals>.<listcomp>'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 256       150  LOAD_GLOBAL              map
              152  LOAD_GLOBAL              _dnsname_to_stdlib
              154  LOAD_FAST                'ext'
              156  LOAD_METHOD              get_values_for_type
              158  LOAD_GLOBAL              x509
              160  LOAD_ATTR                DNSName
              162  CALL_METHOD_1         1  ''
              164  CALL_FUNCTION_2       2  ''

 L. 254       166  GET_ITER         
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'names'

 L. 259       172  LOAD_FAST                'names'
              174  LOAD_METHOD              extend
              176  LOAD_GENEXPR             '<code_object <genexpr>>'
              178  LOAD_STR                 'get_subj_alt_name.<locals>.<genexpr>'
              180  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 260       182  LOAD_FAST                'ext'
              184  LOAD_METHOD              get_values_for_type
              186  LOAD_GLOBAL              x509
              188  LOAD_ATTR                IPAddress
              190  CALL_METHOD_1         1  ''

 L. 259       192  GET_ITER         
              194  CALL_FUNCTION_1       1  ''
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 263       200  LOAD_FAST                'names'
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 122


        class WrappedSocket(object):
            __doc__ = "API-compatibility wrapper for Python OpenSSL's Connection-class.\n\n    Note: _makefile_refs, _drop() and _reuse() are needed for the garbage\n    collector of pypy.\n    "

            def __init__(self, connection, socket, suppress_ragged_eofs=True):
                self.connection = connection
                self.socket = socket
                self.suppress_ragged_eofs = suppress_ragged_eofs
                self._makefile_refs = 0
                self._closed = False

            def fileno(self):
                return self.socket.fileno()

            def _decref_socketios(self):
                if self._makefile_refs > 0:
                    self._makefile_refs -= 1
                if self._closed:
                    self.close()

            def recv--- This code section failed: ---

 L. 291         0  SETUP_FINALLY        20  'to 20'

 L. 292         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_ATTR                recv
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'data'
               16  POP_BLOCK        
               18  JUMP_FORWARD        264  'to 264'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 293        20  DUP_TOP          
               22  LOAD_GLOBAL              OpenSSL
               24  LOAD_ATTR                SSL
               26  LOAD_ATTR                SysCallError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    94  'to 94'
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        82  'to 82'

 L. 294        40  LOAD_FAST                'self'
               42  LOAD_ATTR                suppress_ragged_eofs
               44  POP_JUMP_IF_FALSE    66  'to 66'
               46  LOAD_FAST                'e'
               48  LOAD_ATTR                args
               50  LOAD_CONST               (-1, 'Unexpected EOF')
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 295        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         82  'to 82'
               62  LOAD_CONST               b''
               64  RETURN_VALUE     
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            44  '44'

 L. 297        66  LOAD_GLOBAL              SocketError
               68  LOAD_GLOBAL              str
               70  LOAD_FAST                'e'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  POP_BLOCK        
               80  BEGIN_FINALLY    
             82_0  COME_FROM            60  '60'
             82_1  COME_FROM_FINALLY    38  '38'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  END_FINALLY      
               90  POP_EXCEPT       
               92  JUMP_FORWARD        268  'to 268'
             94_0  COME_FROM            30  '30'

 L. 298        94  DUP_TOP          
               96  LOAD_GLOBAL              OpenSSL
               98  LOAD_ATTR                SSL
              100  LOAD_ATTR                ZeroReturnError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   142  'to 142'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 299       112  LOAD_FAST                'self'
              114  LOAD_ATTR                connection
              116  LOAD_METHOD              get_shutdown
              118  CALL_METHOD_0         0  ''
              120  LOAD_GLOBAL              OpenSSL
              122  LOAD_ATTR                SSL
              124  LOAD_ATTR                RECEIVED_SHUTDOWN
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L. 300       130  POP_EXCEPT       
              132  LOAD_CONST               b''
              134  RETURN_VALUE     
            136_0  COME_FROM           128  '128'

 L. 302       136  RAISE_VARARGS_0       0  'reraise'
              138  POP_EXCEPT       
              140  JUMP_FORWARD        268  'to 268'
            142_0  COME_FROM           104  '104'

 L. 303       142  DUP_TOP          
              144  LOAD_GLOBAL              OpenSSL
              146  LOAD_ATTR                SSL
              148  LOAD_ATTR                WantReadError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   210  'to 210'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 304       160  LOAD_GLOBAL              util
              162  LOAD_METHOD              wait_for_read
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                socket
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                socket
              172  LOAD_METHOD              gettimeout
              174  CALL_METHOD_0         0  ''
              176  CALL_METHOD_2         2  ''
              178  POP_JUMP_IF_TRUE    190  'to 190'

 L. 305       180  LOAD_GLOBAL              timeout
              182  LOAD_STR                 'The read operation timed out'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
              188  JUMP_FORWARD        206  'to 206'
            190_0  COME_FROM           178  '178'

 L. 307       190  LOAD_FAST                'self'
              192  LOAD_ATTR                recv
              194  LOAD_FAST                'args'
              196  LOAD_FAST                'kwargs'
              198  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              200  ROT_FOUR         
              202  POP_EXCEPT       
              204  RETURN_VALUE     
            206_0  COME_FROM           188  '188'
              206  POP_EXCEPT       
              208  JUMP_FORWARD        268  'to 268'
            210_0  COME_FROM           152  '152'

 L. 310       210  DUP_TOP          
              212  LOAD_GLOBAL              OpenSSL
              214  LOAD_ATTR                SSL
              216  LOAD_ATTR                Error
              218  COMPARE_OP               exception-match
          220_222  POP_JUMP_IF_FALSE   262  'to 262'
              224  POP_TOP          
              226  STORE_FAST               'e'
              228  POP_TOP          
              230  SETUP_FINALLY       250  'to 250'

 L. 311       232  LOAD_GLOBAL              ssl
              234  LOAD_METHOD              SSLError
              236  LOAD_STR                 'read error: %r'
              238  LOAD_FAST                'e'
              240  BINARY_MODULO    
              242  CALL_METHOD_1         1  ''
              244  RAISE_VARARGS_1       1  'exception instance'
              246  POP_BLOCK        
              248  BEGIN_FINALLY    
            250_0  COME_FROM_FINALLY   230  '230'
              250  LOAD_CONST               None
              252  STORE_FAST               'e'
              254  DELETE_FAST              'e'
              256  END_FINALLY      
              258  POP_EXCEPT       
              260  JUMP_FORWARD        268  'to 268'
            262_0  COME_FROM           220  '220'
              262  END_FINALLY      
            264_0  COME_FROM            18  '18'

 L. 313       264  LOAD_FAST                'data'
              266  RETURN_VALUE     
            268_0  COME_FROM           260  '260'
            268_1  COME_FROM           208  '208'
            268_2  COME_FROM           140  '140'
            268_3  COME_FROM            92  '92'

Parse error at or near `POP_EXCEPT' instruction at offset 58

            def recv_into--- This code section failed: ---

 L. 316         0  SETUP_FINALLY        18  'to 18'

 L. 317         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_ATTR                recv_into
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 318        18  DUP_TOP          
               20  LOAD_GLOBAL              OpenSSL
               22  LOAD_ATTR                SSL
               24  LOAD_ATTR                SysCallError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    92  'to 92'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        80  'to 80'

 L. 319        38  LOAD_FAST                'self'
               40  LOAD_ATTR                suppress_ragged_eofs
               42  POP_JUMP_IF_FALSE    64  'to 64'
               44  LOAD_FAST                'e'
               46  LOAD_ATTR                args
               48  LOAD_CONST               (-1, 'Unexpected EOF')
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L. 320        54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         80  'to 80'
               60  LOAD_CONST               0
               62  RETURN_VALUE     
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            42  '42'

 L. 322        64  LOAD_GLOBAL              SocketError
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'e'
               70  CALL_FUNCTION_1       1  ''
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM            58  '58'
             80_1  COME_FROM_FINALLY    36  '36'
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD        262  'to 262'
             92_0  COME_FROM            28  '28'

 L. 323        92  DUP_TOP          
               94  LOAD_GLOBAL              OpenSSL
               96  LOAD_ATTR                SSL
               98  LOAD_ATTR                ZeroReturnError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   140  'to 140'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 324       110  LOAD_FAST                'self'
              112  LOAD_ATTR                connection
              114  LOAD_METHOD              get_shutdown
              116  CALL_METHOD_0         0  ''
              118  LOAD_GLOBAL              OpenSSL
              120  LOAD_ATTR                SSL
              122  LOAD_ATTR                RECEIVED_SHUTDOWN
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   134  'to 134'

 L. 325       128  POP_EXCEPT       
              130  LOAD_CONST               0
              132  RETURN_VALUE     
            134_0  COME_FROM           126  '126'

 L. 327       134  RAISE_VARARGS_0       0  'reraise'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        262  'to 262'
            140_0  COME_FROM           102  '102'

 L. 328       140  DUP_TOP          
              142  LOAD_GLOBAL              OpenSSL
              144  LOAD_ATTR                SSL
              146  LOAD_ATTR                WantReadError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   208  'to 208'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 329       158  LOAD_GLOBAL              util
              160  LOAD_METHOD              wait_for_read
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                socket
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                socket
              170  LOAD_METHOD              gettimeout
              172  CALL_METHOD_0         0  ''
              174  CALL_METHOD_2         2  ''
              176  POP_JUMP_IF_TRUE    188  'to 188'

 L. 330       178  LOAD_GLOBAL              timeout
              180  LOAD_STR                 'The read operation timed out'
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
              186  JUMP_FORWARD        204  'to 204'
            188_0  COME_FROM           176  '176'

 L. 332       188  LOAD_FAST                'self'
              190  LOAD_ATTR                recv_into
              192  LOAD_FAST                'args'
              194  LOAD_FAST                'kwargs'
              196  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              198  ROT_FOUR         
              200  POP_EXCEPT       
              202  RETURN_VALUE     
            204_0  COME_FROM           186  '186'
              204  POP_EXCEPT       
              206  JUMP_FORWARD        262  'to 262'
            208_0  COME_FROM           150  '150'

 L. 335       208  DUP_TOP          
              210  LOAD_GLOBAL              OpenSSL
              212  LOAD_ATTR                SSL
              214  LOAD_ATTR                Error
              216  COMPARE_OP               exception-match
          218_220  POP_JUMP_IF_FALSE   260  'to 260'
              222  POP_TOP          
              224  STORE_FAST               'e'
              226  POP_TOP          
              228  SETUP_FINALLY       248  'to 248'

 L. 336       230  LOAD_GLOBAL              ssl
              232  LOAD_METHOD              SSLError
              234  LOAD_STR                 'read error: %r'
              236  LOAD_FAST                'e'
              238  BINARY_MODULO    
              240  CALL_METHOD_1         1  ''
              242  RAISE_VARARGS_1       1  'exception instance'
              244  POP_BLOCK        
              246  BEGIN_FINALLY    
            248_0  COME_FROM_FINALLY   228  '228'
              248  LOAD_CONST               None
              250  STORE_FAST               'e'
              252  DELETE_FAST              'e'
              254  END_FINALLY      
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           218  '218'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM           206  '206'
            262_2  COME_FROM           138  '138'
            262_3  COME_FROM            90  '90'

Parse error at or near `POP_EXCEPT' instruction at offset 56

            def settimeout(self, timeout):
                return self.socket.settimeout(timeout)

            def _send_until_done--- This code section failed: ---
              0_0  COME_FROM           118  '118'
              0_1  COME_FROM           114  '114'
              0_2  COME_FROM            66  '66'
              0_3  COME_FROM            62  '62'

 L. 343         0  SETUP_FINALLY        16  'to 16'

 L. 344         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_METHOD              send
                8  LOAD_FAST                'data'
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 345        16  DUP_TOP          
               18  LOAD_GLOBAL              OpenSSL
               20  LOAD_ATTR                SSL
               22  LOAD_ATTR                WantWriteError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    68  'to 68'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 346        34  LOAD_GLOBAL              util
               36  LOAD_METHOD              wait_for_write
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                socket
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                socket
               46  LOAD_METHOD              gettimeout
               48  CALL_METHOD_0         0  ''
               50  CALL_METHOD_2         2  ''
               52  POP_JUMP_IF_TRUE     60  'to 60'

 L. 347        54  LOAD_GLOBAL              timeout
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            52  '52'

 L. 348        60  POP_EXCEPT       
               62  JUMP_BACK             0  'to 0'
               64  POP_EXCEPT       
               66  JUMP_BACK             0  'to 0'
             68_0  COME_FROM            26  '26'

 L. 349        68  DUP_TOP          
               70  LOAD_GLOBAL              OpenSSL
               72  LOAD_ATTR                SSL
               74  LOAD_ATTR                SysCallError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   116  'to 116'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       104  'to 104'

 L. 350        88  LOAD_GLOBAL              SocketError
               90  LOAD_GLOBAL              str
               92  LOAD_FAST                'e'
               94  CALL_FUNCTION_1       1  ''
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
            104_0  COME_FROM_FINALLY    86  '86'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_BACK             0  'to 0'
            116_0  COME_FROM            78  '78'
              116  END_FINALLY      
              118  JUMP_BACK             0  'to 0'

Parse error at or near `JUMP_BACK' instruction at offset 62

            def sendall(self, data):
                total_sent = 0
                while True:
                    if total_sent < len(data):
                        sent = self._send_until_done(data[total_sent:total_sent + SSL_WRITE_BLOCKSIZE])
                        total_sent += sent

            def shutdown(self):
                self.connection.shutdown()

            def close--- This code section failed: ---

 L. 365         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _makefile_refs
                4  LOAD_CONST               1
                6  COMPARE_OP               <
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 366        10  SETUP_FINALLY        30  'to 30'

 L. 367        12  LOAD_CONST               True
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _closed

 L. 368        18  LOAD_FAST                'self'
               20  LOAD_ATTR                connection
               22  LOAD_METHOD              close
               24  CALL_METHOD_0         0  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    10  '10'

 L. 369        30  DUP_TOP          
               32  LOAD_GLOBAL              OpenSSL
               34  LOAD_ATTR                SSL
               36  LOAD_ATTR                Error
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 370        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      
               56  JUMP_FORWARD         72  'to 72'
             58_0  COME_FROM             8  '8'

 L. 372        58  LOAD_FAST                'self'
               60  DUP_TOP          
               62  LOAD_ATTR                _makefile_refs
               64  LOAD_CONST               1
               66  INPLACE_SUBTRACT 
               68  ROT_TWO          
               70  STORE_ATTR               _makefile_refs
             72_0  COME_FROM            56  '56'

Parse error at or near `LOAD_CONST' instruction at offset 50

            def getpeercert(self, binary_form=False):
                x509 = self.connection.get_peer_certificate()
                if not x509:
                    return x509
                if binary_form:
                    return OpenSSL.crypto.dump_certificateOpenSSL.crypto.FILETYPE_ASN1x509
                return {'subject':(
                  (
                   (
                    'commonName', x509.get_subject().CN),),), 
                 'subjectAltName':get_subj_alt_name(x509)}

            def version(self):
                return self.connection.get_protocol_version_name()

            def _reuse(self):
                self._makefile_refs += 1

            def _drop(self):
                if self._makefile_refs < 1:
                    self.close()
                else:
                    self._makefile_refs -= 1


        if _fileobject:

            def makefile(self, mode, bufsize=-1):
                self._makefile_refs += 1
                return _fileobject(self, mode, bufsize, close=True)


        else:
            makefile = backport_makefile
        WrappedSocket.makefile = makefile

        class PyOpenSSLContext(object):
            __doc__ = '\n    I am a wrapper class for the PyOpenSSL ``Context`` object. I am responsible\n    for translating the interface of the standard library ``SSLContext`` object\n    to calls into PyOpenSSL.\n    '

            def __init__(self, protocol):
                self.protocol = _openssl_versions[protocol]
                self._ctx = OpenSSL.SSL.Context(self.protocol)
                self._options = 0
                self.check_hostname = False

            @property
            def options(self):
                return self._options

            @options.setter
            def options(self, value):
                self._options = value
                self._ctx.set_options(value)

            @property
            def verify_mode(self):
                return _openssl_to_stdlib_verify[self._ctx.get_verify_mode()]

            @verify_mode.setter
            def verify_mode(self, value):
                self._ctx.set_verify_stdlib_to_openssl_verify[value]_verify_callback

            def set_default_verify_paths(self):
                self._ctx.set_default_verify_paths()

            def set_ciphers(self, ciphers):
                if isinstance(ciphers, six.text_type):
                    ciphers = ciphers.encode('utf-8')
                self._ctx.set_cipher_list(ciphers)

            def load_verify_locations(self, cafile=None, capath=None, cadata=None):
                if cafile is not None:
                    cafile = cafile.encode('utf-8')
                if capath is not None:
                    capath = capath.encode('utf-8')
                try:
                    self._ctx.load_verify_locationscafilecapath
                    if cadata is not None:
                        self._ctx.load_verify_locations(BytesIO(cadata))
                except OpenSSL.SSL.Error as e:
                    try:
                        raise ssl.SSLError('unable to load trusted certificates: %r' % e)
                    finally:
                        e = None
                        del e

            def load_cert_chain(self, certfile, keyfile=None, password=None):
                self._ctx.use_certificate_chain_file(certfile)
                if password is not None:
                    if not isinstance(password, six.binary_type):
                        password = password.encode('utf-8')
                    self._ctx.set_passwd_cb(lambda *_: password)
                self._ctx.use_privatekey_file(keyfile or certfile)

            def set_alpn_protocols(self, protocols):
                protocols = [six.ensure_binary(p) for p in protocols]
                return self._ctx.set_alpn_protos(protocols)

            def wrap_socket--- This code section failed: ---

 L. 484         0  LOAD_GLOBAL              OpenSSL
                2  LOAD_ATTR                SSL
                4  LOAD_METHOD              Connection
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _ctx
               10  LOAD_FAST                'sock'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'cnx'

 L. 486        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'server_hostname'
               20  LOAD_GLOBAL              six
               22  LOAD_ATTR                text_type
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 487        28  LOAD_FAST                'server_hostname'
               30  LOAD_METHOD              encode
               32  LOAD_STR                 'utf-8'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'server_hostname'
             38_0  COME_FROM            26  '26'

 L. 489        38  LOAD_FAST                'server_hostname'
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 490        46  LOAD_FAST                'cnx'
               48  LOAD_METHOD              set_tlsext_host_name
               50  LOAD_FAST                'server_hostname'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            44  '44'

 L. 492        56  LOAD_FAST                'cnx'
               58  LOAD_METHOD              set_connect_state
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          
             64_0  COME_FROM           182  '182'
             64_1  COME_FROM           122  '122'

 L. 495        64  SETUP_FINALLY        78  'to 78'

 L. 496        66  LOAD_FAST                'cnx'
               68  LOAD_METHOD              do_handshake
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD        184  'to 184'
             78_0  COME_FROM_FINALLY    64  '64'

 L. 497        78  DUP_TOP          
               80  LOAD_GLOBAL              OpenSSL
               82  LOAD_ATTR                SSL
               84  LOAD_ATTR                WantReadError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   128  'to 128'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 498        96  LOAD_GLOBAL              util
               98  LOAD_METHOD              wait_for_read
              100  LOAD_FAST                'sock'
              102  LOAD_FAST                'sock'
              104  LOAD_METHOD              gettimeout
              106  CALL_METHOD_0         0  ''
              108  CALL_METHOD_2         2  ''
              110  POP_JUMP_IF_TRUE    120  'to 120'

 L. 499       112  LOAD_GLOBAL              timeout
              114  LOAD_STR                 'select timed out'
              116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           110  '110'

 L. 500       120  POP_EXCEPT       
              122  JUMP_BACK            64  'to 64'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        184  'to 184'
            128_0  COME_FROM            88  '88'

 L. 501       128  DUP_TOP          
              130  LOAD_GLOBAL              OpenSSL
              132  LOAD_ATTR                SSL
              134  LOAD_ATTR                Error
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   178  'to 178'
              140  POP_TOP          
              142  STORE_FAST               'e'
              144  POP_TOP          
              146  SETUP_FINALLY       166  'to 166'

 L. 502       148  LOAD_GLOBAL              ssl
              150  LOAD_METHOD              SSLError
              152  LOAD_STR                 'bad handshake: %r'
              154  LOAD_FAST                'e'
              156  BINARY_MODULO    
              158  CALL_METHOD_1         1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
              162  POP_BLOCK        
              164  BEGIN_FINALLY    
            166_0  COME_FROM_FINALLY   146  '146'
              166  LOAD_CONST               None
              168  STORE_FAST               'e'
              170  DELETE_FAST              'e'
              172  END_FINALLY      
              174  POP_EXCEPT       
              176  JUMP_FORWARD        184  'to 184'
            178_0  COME_FROM           138  '138'
              178  END_FINALLY      

 L. 503       180  JUMP_FORWARD        184  'to 184'
              182  JUMP_BACK            64  'to 64'
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           176  '176'
            184_2  COME_FROM           126  '126'
            184_3  COME_FROM            76  '76'

 L. 505       184  LOAD_GLOBAL              WrappedSocket
              186  LOAD_FAST                'cnx'
              188  LOAD_FAST                'sock'
              190  CALL_FUNCTION_2       2  ''
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 128


        def _verify_callback(cnx, x509, err_no, err_depth, return_code):
            return err_no == 0