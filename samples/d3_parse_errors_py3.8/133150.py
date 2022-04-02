# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\urllib3\contrib\pyopenssl.py
"""
SSL with SNI_-support for Python 2. Follow these instructions if you would
like to verify SSL certificates in Python 2. Note, the default libraries do
*not* do certificate checking; you need to do additional work to validate
certificates yourself.

This needs the following packages installed:

* pyOpenSSL (tested with 16.0.0)
* cryptography (minimum 1.3.4, from pyopenssl)
* idna (minimum 2.0, from cryptography)

However, pyopenssl depends on cryptography, which depends on idna, so while we
use all three directly here we end up having relatively few packages required.

You can install them with the following command:

    pip install pyopenssl cryptography idna

To activate certificate checking, call
:func:`~urllib3.contrib.pyopenssl.inject_into_urllib3` from your Python code
before you begin making HTTP requests. This can be done in a ``sitecustomize``
module, or at any other time before your application begins using ``urllib3``,
like this::

    try:
        import urllib3.contrib.pyopenssl
        urllib3.contrib.pyopenssl.inject_into_urllib3()
    except ImportError:
        pass

Now you can use :mod:`urllib3` as you normally would, and it will support SNI
when the required modules are installed.

Activating this module also has the positive side effect of disabling SSL/TLS
compression in Python 2 (see `CRIME attack`_).

If you want to configure the default list of supported cipher suites, you can
set the ``urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST`` variable.

.. _sni: https://en.wikipedia.org/wiki/Server_Name_Indication
.. _crime attack: https://en.wikipedia.org/wiki/CRIME_(security_exploit)
"""
from __future__ import absolute_import
import idna, OpenSSL.SSL
from cryptography import x509
import cryptography.hazmat.backends.openssl as openssl_backend
from cryptography.hazmat.backends.openssl.x509 import _Certificate
from socket import timeout, error as SocketError
from io import BytesIO
try:
    from socket import _fileobject
except ImportError:
    _fileobject = None
    from packages.backports.makefile import backport_makefile
else:
    import logging, ssl, select, six, sys
    from .. import util
    __all__ = [
     'inject_into_urllib3', 'extract_from_urllib3']
    HAS_SNI = True
    _openssl_versions = {ssl.PROTOCOL_SSLv23: OpenSSL.SSL.SSLv23_METHOD, 
     ssl.PROTOCOL_TLSv1: OpenSSL.SSL.TLSv1_METHOD}
    if hasattr(ssl, 'PROTOCOL_TLSv1_1'):
        if hasattr(OpenSSL.SSL, 'TLSv1_1_METHOD'):
            _openssl_versions[ssl.PROTOCOL_TLSv1_1] = OpenSSL.SSL.TLSv1_1_METHOD
    if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
        if hasattr(OpenSSL.SSL, 'TLSv1_2_METHOD'):
            _openssl_versions[ssl.PROTOCOL_TLSv1_2] = OpenSSL.SSL.TLSv1_2_METHOD
    try:
        _openssl_versions.update({ssl.PROTOCOL_SSLv3: OpenSSL.SSL.SSLv3_METHOD})
    except AttributeError:
        pass
    else:
        _stdlib_to_openssl_verify = {ssl.CERT_NONE: OpenSSL.SSL.VERIFY_NONE, 
         ssl.CERT_OPTIONAL: OpenSSL.SSL.VERIFY_PEER, 
         ssl.CERT_REQUIRED: OpenSSL.SSL.VERIFY_PEER + OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT}
        _openssl_to_stdlib_verify = dict(((
         v, k) for k, v in _stdlib_to_openssl_verify.items()))
        SSL_WRITE_BLOCKSIZE = 16384
        orig_util_HAS_SNI = util.HAS_SNI
        orig_util_SSLContext = util.ssl_.SSLContext
        log = logging.getLogger(__name__)

        def inject_into_urllib3():
            """Monkey-patch urllib3 with PyOpenSSL-backed SSL-support."""
            util.ssl_.SSLContext = PyOpenSSLContext
            util.HAS_SNI = HAS_SNI
            util.ssl_.HAS_SNI = HAS_SNI
            util.IS_PYOPENSSL = True
            util.ssl_.IS_PYOPENSSL = True


        def extract_from_urllib3():
            """Undo monkey-patching by :func:`inject_into_urllib3`."""
            util.ssl_.SSLContext = orig_util_SSLContext
            util.HAS_SNI = orig_util_HAS_SNI
            util.ssl_.HAS_SNI = orig_util_HAS_SNI
            util.IS_PYOPENSSL = False
            util.ssl_.IS_PYOPENSSL = False


        def _dnsname_to_stdlib(name):
            """
    Converts a dNSName SubjectAlternativeName field to the form used by the
    standard library on the given Python version.

    Cryptography produces a dNSName as a unicode string that was idna-decoded
    from ASCII bytes. We need to idna-encode that string to get it back, and
    then on Python 3 we also need to convert to unicode via UTF-8 (the stdlib
    uses PyUnicode_FromStringAndSize on it, which decodes via UTF-8).
    """

            def idna_encode(name):
                """
        Borrowed wholesale from the Python Cryptography Project. It turns out
        that we can't just safely call `idna.encode`: it can explode for
        wildcard names. This avoids that problem.
        """
                for prefix in ('*.', '.'):
                    if name.startswith(prefix):
                        name = name[len(prefix):]
                        return prefix.encode('ascii') + idna.encode(name)
                else:
                    return idna.encode(name)

            name = idna_encode(name)
            if sys.version_info >= (3, 0):
                name = name.decode('utf-8')
            return name


        def get_subj_alt_name--- This code section failed: ---

 L. 166         0  LOAD_GLOBAL              _Certificate
                2  LOAD_GLOBAL              openssl_backend
                4  LOAD_FAST                'peer_cert'
                6  LOAD_ATTR                _x509
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'cert'

 L. 170        12  SETUP_FINALLY        34  'to 34'

 L. 171        14  LOAD_FAST                'cert'
               16  LOAD_ATTR                extensions
               18  LOAD_METHOD              get_extension_for_class

 L. 172        20  LOAD_GLOBAL              x509
               22  LOAD_ATTR                SubjectAlternativeName

 L. 171        24  CALL_METHOD_1         1  ''
               26  LOAD_ATTR                value
               28  STORE_FAST               'ext'
               30  POP_BLOCK        
               32  JUMP_FORWARD        126  'to 126'
             34_0  COME_FROM_FINALLY    12  '12'

 L. 174        34  DUP_TOP          
               36  LOAD_GLOBAL              x509
               38  LOAD_ATTR                ExtensionNotFound
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 176        50  BUILD_LIST_0          0 
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM            42  '42'

 L. 177        58  DUP_TOP          
               60  LOAD_GLOBAL              x509
               62  LOAD_ATTR                DuplicateExtension
               64  LOAD_GLOBAL              x509
               66  LOAD_ATTR                UnsupportedExtension

 L. 178        68  LOAD_GLOBAL              x509
               70  LOAD_ATTR                UnsupportedGeneralNameType

 L. 178        72  LOAD_GLOBAL              UnicodeError

 L. 177        74  BUILD_TUPLE_4         4 
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   124  'to 124'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       112  'to 112'

 L. 181        88  LOAD_GLOBAL              log
               90  LOAD_METHOD              warning

 L. 182        92  LOAD_STR                 'A problem was encountered with the certificate that prevented urllib3 from finding the SubjectAlternativeName field. This can affect certificate validation. The error was %s'

 L. 185        94  LOAD_FAST                'e'

 L. 181        96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 187       100  BUILD_LIST_0          0 
              102  ROT_FOUR         
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  CALL_FINALLY        112  'to 112'
              110  RETURN_VALUE     
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM_FINALLY    86  '86'
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  END_FINALLY      
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM            78  '78'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM            32  '32'

 L. 195       126  LOAD_LISTCOMP            '<code_object <listcomp>>'
              128  LOAD_STR                 'get_subj_alt_name.<locals>.<listcomp>'
              130  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 197       132  LOAD_FAST                'ext'
              134  LOAD_METHOD              get_values_for_type
              136  LOAD_GLOBAL              x509
              138  LOAD_ATTR                DNSName
              140  CALL_METHOD_1         1  ''

 L. 195       142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'names'

 L. 199       148  LOAD_FAST                'names'
              150  LOAD_METHOD              extend
              152  LOAD_GENEXPR             '<code_object <genexpr>>'
              154  LOAD_STR                 'get_subj_alt_name.<locals>.<genexpr>'
              156  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 201       158  LOAD_FAST                'ext'
              160  LOAD_METHOD              get_values_for_type
              162  LOAD_GLOBAL              x509
              164  LOAD_ATTR                IPAddress
              166  CALL_METHOD_1         1  ''

 L. 199       168  GET_ITER         
              170  CALL_FUNCTION_1       1  ''
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L. 204       176  LOAD_FAST                'names'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 104


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

 L. 232         0  SETUP_FINALLY        20  'to 20'

 L. 233         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_ATTR                recv
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'data'
               16  POP_BLOCK        
               18  JUMP_FORWARD        246  'to 246'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 234        20  DUP_TOP          
               22  LOAD_GLOBAL              OpenSSL
               24  LOAD_ATTR                SSL
               26  LOAD_ATTR                SysCallError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    94  'to 94'
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        82  'to 82'

 L. 235        40  LOAD_FAST                'self'
               42  LOAD_ATTR                suppress_ragged_eofs
               44  POP_JUMP_IF_FALSE    66  'to 66'
               46  LOAD_FAST                'e'
               48  LOAD_ATTR                args
               50  LOAD_CONST               (-1, 'Unexpected EOF')
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 236        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         82  'to 82'
               62  LOAD_CONST               b''
               64  RETURN_VALUE     
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            44  '44'

 L. 238        66  LOAD_GLOBAL              SocketError
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
               92  JUMP_FORWARD        250  'to 250'
             94_0  COME_FROM            30  '30'

 L. 239        94  DUP_TOP          
               96  LOAD_GLOBAL              OpenSSL
               98  LOAD_ATTR                SSL
              100  LOAD_ATTR                ZeroReturnError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   160  'to 160'
              106  POP_TOP          
              108  STORE_FAST               'e'
              110  POP_TOP          
              112  SETUP_FINALLY       148  'to 148'

 L. 240       114  LOAD_FAST                'self'
              116  LOAD_ATTR                connection
              118  LOAD_METHOD              get_shutdown
              120  CALL_METHOD_0         0  ''
              122  LOAD_GLOBAL              OpenSSL
              124  LOAD_ATTR                SSL
              126  LOAD_ATTR                RECEIVED_SHUTDOWN
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L. 241       132  POP_BLOCK        
              134  POP_EXCEPT       
              136  CALL_FINALLY        148  'to 148'
              138  LOAD_CONST               b''
              140  RETURN_VALUE     
            142_0  COME_FROM           130  '130'

 L. 243       142  RAISE_VARARGS_0       0  'reraise'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM           136  '136'
            148_1  COME_FROM_FINALLY   112  '112'
              148  LOAD_CONST               None
              150  STORE_FAST               'e'
              152  DELETE_FAST              'e'
              154  END_FINALLY      
              156  POP_EXCEPT       
              158  JUMP_FORWARD        250  'to 250'
            160_0  COME_FROM           104  '104'

 L. 244       160  DUP_TOP          
              162  LOAD_GLOBAL              OpenSSL
              164  LOAD_ATTR                SSL
              166  LOAD_ATTR                WantReadError
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   244  'to 244'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 245       178  LOAD_GLOBAL              select
              180  LOAD_METHOD              select

 L. 246       182  LOAD_FAST                'self'
              184  LOAD_ATTR                socket
              186  BUILD_LIST_1          1 

 L. 246       188  BUILD_LIST_0          0 

 L. 246       190  BUILD_LIST_0          0 

 L. 246       192  LOAD_FAST                'self'
              194  LOAD_ATTR                socket
              196  LOAD_METHOD              gettimeout
              198  CALL_METHOD_0         0  ''

 L. 245       200  CALL_METHOD_4         4  ''
              202  UNPACK_SEQUENCE_3     3 
              204  STORE_FAST               'rd'
              206  STORE_FAST               'wd'
              208  STORE_FAST               'ed'

 L. 247       210  LOAD_FAST                'rd'
              212  POP_JUMP_IF_TRUE    224  'to 224'

 L. 248       214  LOAD_GLOBAL              timeout
              216  LOAD_STR                 'The read operation timed out'
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
              222  JUMP_FORWARD        240  'to 240'
            224_0  COME_FROM           212  '212'

 L. 250       224  LOAD_FAST                'self'
              226  LOAD_ATTR                recv
              228  LOAD_FAST                'args'
              230  LOAD_FAST                'kwargs'
              232  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              234  ROT_FOUR         
              236  POP_EXCEPT       
              238  RETURN_VALUE     
            240_0  COME_FROM           222  '222'
              240  POP_EXCEPT       
              242  JUMP_FORWARD        250  'to 250'
            244_0  COME_FROM           170  '170'
              244  END_FINALLY      
            246_0  COME_FROM            18  '18'

 L. 252       246  LOAD_FAST                'data'
              248  RETURN_VALUE     
            250_0  COME_FROM           242  '242'
            250_1  COME_FROM           158  '158'
            250_2  COME_FROM            92  '92'

Parse error at or near `POP_EXCEPT' instruction at offset 58

            def recv_into--- This code section failed: ---

 L. 255         0  SETUP_FINALLY        18  'to 18'

 L. 256         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_ATTR                recv_into
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 257        18  DUP_TOP          
               20  LOAD_GLOBAL              OpenSSL
               22  LOAD_ATTR                SSL
               24  LOAD_ATTR                SysCallError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    92  'to 92'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        80  'to 80'

 L. 258        38  LOAD_FAST                'self'
               40  LOAD_ATTR                suppress_ragged_eofs
               42  POP_JUMP_IF_FALSE    64  'to 64'
               44  LOAD_FAST                'e'
               46  LOAD_ATTR                args
               48  LOAD_CONST               (-1, 'Unexpected EOF')
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L. 259        54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         80  'to 80'
               60  LOAD_CONST               0
               62  RETURN_VALUE     
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            42  '42'

 L. 261        64  LOAD_GLOBAL              SocketError
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
               90  JUMP_FORWARD        244  'to 244'
             92_0  COME_FROM            28  '28'

 L. 262        92  DUP_TOP          
               94  LOAD_GLOBAL              OpenSSL
               96  LOAD_ATTR                SSL
               98  LOAD_ATTR                ZeroReturnError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   158  'to 158'
              104  POP_TOP          
              106  STORE_FAST               'e'
              108  POP_TOP          
              110  SETUP_FINALLY       146  'to 146'

 L. 263       112  LOAD_FAST                'self'
              114  LOAD_ATTR                connection
              116  LOAD_METHOD              get_shutdown
              118  CALL_METHOD_0         0  ''
              120  LOAD_GLOBAL              OpenSSL
              122  LOAD_ATTR                SSL
              124  LOAD_ATTR                RECEIVED_SHUTDOWN
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   140  'to 140'

 L. 264       130  POP_BLOCK        
              132  POP_EXCEPT       
              134  CALL_FINALLY        146  'to 146'
              136  LOAD_CONST               0
              138  RETURN_VALUE     
            140_0  COME_FROM           128  '128'

 L. 266       140  RAISE_VARARGS_0       0  'reraise'
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM           134  '134'
            146_1  COME_FROM_FINALLY   110  '110'
              146  LOAD_CONST               None
              148  STORE_FAST               'e'
              150  DELETE_FAST              'e'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_FORWARD        244  'to 244'
            158_0  COME_FROM           102  '102'

 L. 267       158  DUP_TOP          
              160  LOAD_GLOBAL              OpenSSL
              162  LOAD_ATTR                SSL
              164  LOAD_ATTR                WantReadError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   242  'to 242'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 268       176  LOAD_GLOBAL              select
              178  LOAD_METHOD              select

 L. 269       180  LOAD_FAST                'self'
              182  LOAD_ATTR                socket
              184  BUILD_LIST_1          1 

 L. 269       186  BUILD_LIST_0          0 

 L. 269       188  BUILD_LIST_0          0 

 L. 269       190  LOAD_FAST                'self'
              192  LOAD_ATTR                socket
              194  LOAD_METHOD              gettimeout
              196  CALL_METHOD_0         0  ''

 L. 268       198  CALL_METHOD_4         4  ''
              200  UNPACK_SEQUENCE_3     3 
              202  STORE_FAST               'rd'
              204  STORE_FAST               'wd'
              206  STORE_FAST               'ed'

 L. 270       208  LOAD_FAST                'rd'
              210  POP_JUMP_IF_TRUE    222  'to 222'

 L. 271       212  LOAD_GLOBAL              timeout
              214  LOAD_STR                 'The read operation timed out'
              216  CALL_FUNCTION_1       1  ''
              218  RAISE_VARARGS_1       1  'exception instance'
              220  JUMP_FORWARD        238  'to 238'
            222_0  COME_FROM           210  '210'

 L. 273       222  LOAD_FAST                'self'
              224  LOAD_ATTR                recv_into
              226  LOAD_FAST                'args'
              228  LOAD_FAST                'kwargs'
              230  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              232  ROT_FOUR         
              234  POP_EXCEPT       
              236  RETURN_VALUE     
            238_0  COME_FROM           220  '220'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           168  '168'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           156  '156'
            244_2  COME_FROM            90  '90'

Parse error at or near `POP_EXCEPT' instruction at offset 56

            def settimeout(self, timeout):
                return self.socket.settimeout(timeout)

            def _send_until_done--- This code section failed: ---
              0_0  COME_FROM            86  '86'
              0_1  COME_FROM            82  '82'
              0_2  COME_FROM            78  '78'

 L. 280         0  SETUP_FINALLY        16  'to 16'

 L. 281         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_METHOD              send
                8  LOAD_FAST                'data'
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 282        16  DUP_TOP          
               18  LOAD_GLOBAL              OpenSSL
               20  LOAD_ATTR                SSL
               22  LOAD_ATTR                WantWriteError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    84  'to 84'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 283        34  LOAD_GLOBAL              select
               36  LOAD_METHOD              select
               38  BUILD_LIST_0          0 
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                socket
               44  BUILD_LIST_1          1 
               46  BUILD_LIST_0          0 

 L. 284        48  LOAD_FAST                'self'
               50  LOAD_ATTR                socket
               52  LOAD_METHOD              gettimeout
               54  CALL_METHOD_0         0  ''

 L. 283        56  CALL_METHOD_4         4  ''
               58  UNPACK_SEQUENCE_3     3 
               60  STORE_FAST               '_'
               62  STORE_FAST               'wlist'
               64  STORE_FAST               '_'

 L. 285        66  LOAD_FAST                'wlist'
               68  POP_JUMP_IF_TRUE     76  'to 76'

 L. 286        70  LOAD_GLOBAL              timeout
               72  CALL_FUNCTION_0       0  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            68  '68'

 L. 287        76  POP_EXCEPT       
               78  JUMP_BACK             0  'to 0'
               80  POP_EXCEPT       
               82  JUMP_BACK             0  'to 0'
             84_0  COME_FROM            26  '26'
               84  END_FINALLY      
               86  JUMP_BACK             0  'to 0'

Parse error at or near `JUMP_BACK' instruction at offset 78

            def sendall(self, data):
                total_sent = 0
                while True:
                    if total_sent < len(data):
                        sent = self._send_until_done(data[total_sent:total_sent + SSL_WRITE_BLOCKSIZE])
                        total_sent += sent

            def shutdown(self):
                self.connection.shutdown()

            def close--- This code section failed: ---

 L. 300         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _makefile_refs
                4  LOAD_CONST               1
                6  COMPARE_OP               <
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L. 301        10  SETUP_FINALLY        30  'to 30'

 L. 302        12  LOAD_CONST               True
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _closed

 L. 303        18  LOAD_FAST                'self'
               20  LOAD_ATTR                connection
               22  LOAD_METHOD              close
               24  CALL_METHOD_0         0  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    10  '10'

 L. 304        30  DUP_TOP          
               32  LOAD_GLOBAL              OpenSSL
               34  LOAD_ATTR                SSL
               36  LOAD_ATTR                Error
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 305        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      
               56  JUMP_FORWARD         72  'to 72'
             58_0  COME_FROM             8  '8'

 L. 307        58  LOAD_FAST                'self'
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
                self._ctx.load_verify_locationscafilecapath
                if cadata is not None:
                    self._ctx.load_verify_locations(BytesIO(cadata))

            def load_cert_chain(self, certfile, keyfile=None, password=None):
                self._ctx.use_certificate_file(certfile)
                if password is not None:
                    self._ctx.set_passwd_cb(lambda max_length, prompt_twice, userdata: password)
                self._ctx.use_privatekey_file(keyfile or certfile)

            def wrap_socket--- This code section failed: ---

 L. 405         0  LOAD_GLOBAL              OpenSSL
                2  LOAD_ATTR                SSL
                4  LOAD_METHOD              Connection
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _ctx
               10  LOAD_FAST                'sock'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'cnx'

 L. 407        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'server_hostname'
               20  LOAD_GLOBAL              six
               22  LOAD_ATTR                text_type
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 408        28  LOAD_FAST                'server_hostname'
               30  LOAD_METHOD              encode
               32  LOAD_STR                 'utf-8'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'server_hostname'
             38_0  COME_FROM            26  '26'

 L. 410        38  LOAD_FAST                'server_hostname'
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 411        46  LOAD_FAST                'cnx'
               48  LOAD_METHOD              set_tlsext_host_name
               50  LOAD_FAST                'server_hostname'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            44  '44'

 L. 413        56  LOAD_FAST                'cnx'
               58  LOAD_METHOD              set_connect_state
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          
             64_0  COME_FROM           198  '198'
             64_1  COME_FROM           138  '138'

 L. 416        64  SETUP_FINALLY        78  'to 78'

 L. 417        66  LOAD_FAST                'cnx'
               68  LOAD_METHOD              do_handshake
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD        200  'to 200'
             78_0  COME_FROM_FINALLY    64  '64'

 L. 418        78  DUP_TOP          
               80  LOAD_GLOBAL              OpenSSL
               82  LOAD_ATTR                SSL
               84  LOAD_ATTR                WantReadError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   144  'to 144'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 419        96  LOAD_GLOBAL              select
               98  LOAD_METHOD              select
              100  LOAD_FAST                'sock'
              102  BUILD_LIST_1          1 
              104  BUILD_LIST_0          0 
              106  BUILD_LIST_0          0 
              108  LOAD_FAST                'sock'
              110  LOAD_METHOD              gettimeout
              112  CALL_METHOD_0         0  ''
              114  CALL_METHOD_4         4  ''
              116  UNPACK_SEQUENCE_3     3 
              118  STORE_FAST               'rd'
              120  STORE_FAST               '_'
              122  STORE_FAST               '_'

 L. 420       124  LOAD_FAST                'rd'
              126  POP_JUMP_IF_TRUE    136  'to 136'

 L. 421       128  LOAD_GLOBAL              timeout
              130  LOAD_STR                 'select timed out'
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 422       136  POP_EXCEPT       
              138  JUMP_BACK            64  'to 64'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        200  'to 200'
            144_0  COME_FROM            88  '88'

 L. 423       144  DUP_TOP          
              146  LOAD_GLOBAL              OpenSSL
              148  LOAD_ATTR                SSL
              150  LOAD_ATTR                Error
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   194  'to 194'
              156  POP_TOP          
              158  STORE_FAST               'e'
              160  POP_TOP          
              162  SETUP_FINALLY       182  'to 182'

 L. 424       164  LOAD_GLOBAL              ssl
              166  LOAD_METHOD              SSLError
              168  LOAD_STR                 'bad handshake: %r'
              170  LOAD_FAST                'e'
              172  BINARY_MODULO    
              174  CALL_METHOD_1         1  ''
              176  RAISE_VARARGS_1       1  'exception instance'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_FINALLY   162  '162'
              182  LOAD_CONST               None
              184  STORE_FAST               'e'
              186  DELETE_FAST              'e'
              188  END_FINALLY      
              190  POP_EXCEPT       
              192  JUMP_FORWARD        200  'to 200'
            194_0  COME_FROM           154  '154'
              194  END_FINALLY      

 L. 425       196  JUMP_FORWARD        200  'to 200'
              198  JUMP_BACK            64  'to 64'
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           192  '192'
            200_2  COME_FROM           142  '142'
            200_3  COME_FROM            76  '76'

 L. 427       200  LOAD_GLOBAL              WrappedSocket
              202  LOAD_FAST                'cnx'
              204  LOAD_FAST                'sock'
              206  CALL_FUNCTION_2       2  ''
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 144


        def _verify_callback(cnx, x509, err_no, err_depth, return_code):
            return err_no == 0