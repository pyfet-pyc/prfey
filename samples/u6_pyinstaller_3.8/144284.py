# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\contrib\pyopenssl.py
"""SSL with SNI_-support for Python 2. Follow these instructions if you would
like to verify SSL certificates in Python 2. Note, the default libraries do
*not* do certificate checking; you need to do additional work to validate
certificates yourself.

This needs the following packages installed:

* pyOpenSSL (tested with 0.13)
* ndg-httpsclient (tested with 0.3.2)
* pyasn1 (tested with 0.1.6)

You can install them with the following command:

    pip install pyopenssl ndg-httpsclient pyasn1

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

Module Variables
----------------

:var DEFAULT_SSL_CIPHER_LIST: The list of supported SSL/TLS cipher suites.

.. _sni: https://en.wikipedia.org/wiki/Server_Name_Indication
.. _crime attack: https://en.wikipedia.org/wiki/CRIME_(security_exploit)

"""
try:
    from ndg.httpsclient.ssl_peer_verification import SUBJ_ALT_NAME_SUPPORT
    import ndg.httpsclient.subj_alt_name as BaseSubjectAltName
except SyntaxError as e:
    try:
        raise ImportError(e)
    finally:
        e = None
        del e

else:
    import OpenSSL.SSL
    import pyasn1.codec.der as der_decoder
    from pyasn1.type import univ, constraint
    from socket import _fileobject, timeout
    import ssl, select
    from .. import connection
    from .. import util
    __all__ = [
     'inject_into_urllib3', 'extract_from_urllib3']
    HAS_SNI = SUBJ_ALT_NAME_SUPPORT
    _openssl_versions = {ssl.PROTOCOL_SSLv23: OpenSSL.SSL.SSLv23_METHOD, 
     ssl.PROTOCOL_TLSv1: OpenSSL.SSL.TLSv1_METHOD}
    try:
        _openssl_versions.update({ssl.PROTOCOL_SSLv3: OpenSSL.SSL.SSLv3_METHOD})
    except AttributeError:
        pass
    else:
        _openssl_verify = {ssl.CERT_NONE: OpenSSL.SSL.VERIFY_NONE, 
         ssl.CERT_OPTIONAL: OpenSSL.SSL.VERIFY_PEER, 
         ssl.CERT_REQUIRED: OpenSSL.SSL.VERIFY_PEER + OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT}
        DEFAULT_SSL_CIPHER_LIST = util.ssl_.DEFAULT_CIPHERS
        orig_util_HAS_SNI = util.HAS_SNI
        orig_connection_ssl_wrap_socket = connection.ssl_wrap_socket

        def inject_into_urllib3():
            """Monkey-patch urllib3 with PyOpenSSL-backed SSL-support."""
            connection.ssl_wrap_socket = ssl_wrap_socket
            util.HAS_SNI = HAS_SNI


        def extract_from_urllib3():
            """Undo monkey-patching by :func:`inject_into_urllib3`."""
            connection.ssl_wrap_socket = orig_connection_ssl_wrap_socket
            util.HAS_SNI = orig_util_HAS_SNI


        class SubjectAltName(BaseSubjectAltName):
            __doc__ = 'ASN.1 implementation for subjectAltNames support'
            sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, 1024)


        def get_subj_alt_name(peer_cert):
            dns_name = []
            if not SUBJ_ALT_NAME_SUPPORT:
                return dns_name
            general_names = SubjectAltName()
            for i in range(peer_cert.get_extension_count()):
                ext = peer_cert.get_extension(i)
                ext_name = ext.get_short_name()
                if ext_name != 'subjectAltName':
                    pass
                else:
                    ext_dat = ext.get_data()
                    decoded_dat = der_decoder.decode(ext_dat, asn1Spec=general_names)

            for name in decoded_dat:
                if not isinstance(name, SubjectAltName):
                    pass
                else:
                    for entry in range(len(name)):
                        component = name.getComponentByPosition(entry)
                        if component.getName() != 'dNSName':
                            pass
                        else:
                            dns_name.append(str(component.getComponent()))

            else:
                return dns_name


        class WrappedSocket(object):
            __doc__ = "API-compatibility wrapper for Python OpenSSL's Connection-class.\n\n    Note: _makefile_refs, _drop() and _reuse() are needed for the garbage\n    collector of pypy.\n    "

            def __init__(self, connection, socket, suppress_ragged_eofs=True):
                self.connection = connection
                self.socket = socket
                self.suppress_ragged_eofs = suppress_ragged_eofs
                self._makefile_refs = 0

            def fileno(self):
                return self.socket.fileno()

            def makefile(self, mode, bufsize=-1):
                self._makefile_refs += 1
                return _fileobject(self, mode, bufsize, close=True)

            def recv--- This code section failed: ---

 L. 170         0  SETUP_FINALLY        20  'to 20'

 L. 171         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_ATTR                recv
                8  LOAD_FAST                'args'
               10  LOAD_FAST                'kwargs'
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'data'
               16  POP_BLOCK        
               18  JUMP_FORWARD        236  'to 236'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 172        20  DUP_TOP          
               22  LOAD_GLOBAL              OpenSSL
               24  LOAD_ATTR                SSL
               26  LOAD_ATTR                SysCallError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    84  'to 84'
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        72  'to 72'

 L. 173        40  LOAD_FAST                'self'
               42  LOAD_ATTR                suppress_ragged_eofs
               44  POP_JUMP_IF_FALSE    66  'to 66'
               46  LOAD_FAST                'e'
               48  LOAD_ATTR                args
               50  LOAD_CONST               (-1, 'Unexpected EOF')
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 174        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         72  'to 72'
               62  LOAD_CONST               b''
               64  RETURN_VALUE     
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            44  '44'

 L. 176        66  RAISE_VARARGS_0       0  'reraise'
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM            60  '60'
             72_1  COME_FROM_FINALLY    38  '38'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD        240  'to 240'
             84_0  COME_FROM            30  '30'

 L. 177        84  DUP_TOP          
               86  LOAD_GLOBAL              OpenSSL
               88  LOAD_ATTR                SSL
               90  LOAD_ATTR                ZeroReturnError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   150  'to 150'
               96  POP_TOP          
               98  STORE_FAST               'e'
              100  POP_TOP          
              102  SETUP_FINALLY       138  'to 138'

 L. 178       104  LOAD_FAST                'self'
              106  LOAD_ATTR                connection
              108  LOAD_METHOD              get_shutdown
              110  CALL_METHOD_0         0  ''
              112  LOAD_GLOBAL              OpenSSL
              114  LOAD_ATTR                SSL
              116  LOAD_ATTR                RECEIVED_SHUTDOWN
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 179       122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        138  'to 138'
              128  LOAD_CONST               b''
              130  RETURN_VALUE     
            132_0  COME_FROM           120  '120'

 L. 181       132  RAISE_VARARGS_0       0  'reraise'
              134  POP_BLOCK        
              136  BEGIN_FINALLY    
            138_0  COME_FROM           126  '126'
            138_1  COME_FROM_FINALLY   102  '102'
              138  LOAD_CONST               None
              140  STORE_FAST               'e'
              142  DELETE_FAST              'e'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_FORWARD        240  'to 240'
            150_0  COME_FROM            94  '94'

 L. 182       150  DUP_TOP          
              152  LOAD_GLOBAL              OpenSSL
              154  LOAD_ATTR                SSL
              156  LOAD_ATTR                WantReadError
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   234  'to 234'
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 183       168  LOAD_GLOBAL              select
              170  LOAD_METHOD              select

 L. 184       172  LOAD_FAST                'self'
              174  LOAD_ATTR                socket
              176  BUILD_LIST_1          1 

 L. 184       178  BUILD_LIST_0          0 

 L. 184       180  BUILD_LIST_0          0 

 L. 184       182  LOAD_FAST                'self'
              184  LOAD_ATTR                socket
              186  LOAD_METHOD              gettimeout
              188  CALL_METHOD_0         0  ''

 L. 183       190  CALL_METHOD_4         4  ''
              192  UNPACK_SEQUENCE_3     3 
              194  STORE_FAST               'rd'
              196  STORE_FAST               'wd'
              198  STORE_FAST               'ed'

 L. 185       200  LOAD_FAST                'rd'
              202  POP_JUMP_IF_TRUE    214  'to 214'

 L. 186       204  LOAD_GLOBAL              timeout
              206  LOAD_STR                 'The read operation timed out'
              208  CALL_FUNCTION_1       1  ''
              210  RAISE_VARARGS_1       1  'exception instance'
              212  JUMP_FORWARD        230  'to 230'
            214_0  COME_FROM           202  '202'

 L. 188       214  LOAD_FAST                'self'
              216  LOAD_ATTR                recv
              218  LOAD_FAST                'args'
              220  LOAD_FAST                'kwargs'
              222  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              224  ROT_FOUR         
              226  POP_EXCEPT       
              228  RETURN_VALUE     
            230_0  COME_FROM           212  '212'
              230  POP_EXCEPT       
              232  JUMP_FORWARD        240  'to 240'
            234_0  COME_FROM           160  '160'
              234  END_FINALLY      
            236_0  COME_FROM            18  '18'

 L. 190       236  LOAD_FAST                'data'
              238  RETURN_VALUE     
            240_0  COME_FROM           232  '232'
            240_1  COME_FROM           148  '148'
            240_2  COME_FROM            82  '82'

Parse error at or near `POP_EXCEPT' instruction at offset 58

            def settimeout(self, timeout):
                return self.socket.settimeout(timeout)

            def _send_until_done--- This code section failed: ---

 L. 197         0  SETUP_FINALLY        16  'to 16'

 L. 198         2  LOAD_FAST                'self'
                4  LOAD_ATTR                connection
                6  LOAD_METHOD              send
                8  LOAD_FAST                'data'
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 199        16  DUP_TOP          
               18  LOAD_GLOBAL              OpenSSL
               20  LOAD_ATTR                SSL
               22  LOAD_ATTR                WantWriteError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    84  'to 84'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 200        34  LOAD_GLOBAL              select
               36  LOAD_METHOD              select
               38  BUILD_LIST_0          0 
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                socket
               44  BUILD_LIST_1          1 
               46  BUILD_LIST_0          0 

 L. 201        48  LOAD_FAST                'self'
               50  LOAD_ATTR                socket
               52  LOAD_METHOD              gettimeout
               54  CALL_METHOD_0         0  ''

 L. 200        56  CALL_METHOD_4         4  ''
               58  UNPACK_SEQUENCE_3     3 
               60  STORE_FAST               '_'
               62  STORE_FAST               'wlist'
               64  STORE_FAST               '_'

 L. 202        66  LOAD_FAST                'wlist'
               68  POP_JUMP_IF_TRUE     76  'to 76'

 L. 203        70  LOAD_GLOBAL              timeout
               72  CALL_FUNCTION_0       0  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            68  '68'

 L. 204        76  POP_EXCEPT       
               78  JUMP_BACK             0  'to 0'
               80  POP_EXCEPT       
               82  JUMP_BACK             0  'to 0'
             84_0  COME_FROM            26  '26'
               84  END_FINALLY      
               86  JUMP_BACK             0  'to 0'

Parse error at or near `POP_TOP' instruction at offset 30

            def sendall(self, data):
                while len(data):
                    sent = self._send_until_done(data)
                    data = data[sent:]

            def close(self):
                if self._makefile_refs < 1:
                    return self.connection.shutdown()
                self._makefile_refs -= 1

            def getpeercert(self, binary_form=False):
                x509 = self.connection.get_peer_certificate()
                if not x509:
                    return x509
                if binary_form:
                    return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509)
                return {'subject':(
                  (
                   (
                    'commonName', x509.get_subject().CN),),), 
                 'subjectAltName':[(
                  'DNS', value) for value in get_subj_alt_name(x509)]}

            def _reuse(self):
                self._makefile_refs += 1

            def _drop(self):
                if self._makefile_refs < 1:
                    self.close()
                else:
                    self._makefile_refs -= 1


        def _verify_callback(cnx, x509, err_no, err_depth, return_code):
            return err_no == 0


        def ssl_wrap_socket--- This code section failed: ---

 L. 255         0  LOAD_GLOBAL              OpenSSL
                2  LOAD_ATTR                SSL
                4  LOAD_METHOD              Context
                6  LOAD_GLOBAL              _openssl_versions
                8  LOAD_FAST                'ssl_version'
               10  BINARY_SUBSCR    
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'ctx'

 L. 256        16  LOAD_FAST                'certfile'
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 257        20  LOAD_FAST                'keyfile'
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  LOAD_FAST                'certfile'
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'keyfile'

 L. 258        28  LOAD_FAST                'ctx'
               30  LOAD_METHOD              use_certificate_file
               32  LOAD_FAST                'certfile'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            18  '18'

 L. 259        38  LOAD_FAST                'keyfile'
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 260        42  LOAD_FAST                'ctx'
               44  LOAD_METHOD              use_privatekey_file
               46  LOAD_FAST                'keyfile'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            40  '40'

 L. 261        52  LOAD_FAST                'cert_reqs'
               54  LOAD_GLOBAL              ssl
               56  LOAD_ATTR                CERT_NONE
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    78  'to 78'

 L. 262        62  LOAD_FAST                'ctx'
               64  LOAD_METHOD              set_verify
               66  LOAD_GLOBAL              _openssl_verify
               68  LOAD_FAST                'cert_reqs'
               70  BINARY_SUBSCR    
               72  LOAD_GLOBAL              _verify_callback
               74  CALL_METHOD_2         2  ''
               76  POP_TOP          
             78_0  COME_FROM            60  '60'

 L. 263        78  LOAD_FAST                'ca_certs'
               80  POP_JUMP_IF_FALSE   156  'to 156'

 L. 264        82  SETUP_FINALLY       100  'to 100'

 L. 265        84  LOAD_FAST                'ctx'
               86  LOAD_METHOD              load_verify_locations
               88  LOAD_FAST                'ca_certs'
               90  LOAD_CONST               None
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          
               96  POP_BLOCK        
               98  JUMP_ABSOLUTE       164  'to 164'
            100_0  COME_FROM_FINALLY    82  '82'

 L. 266       100  DUP_TOP          
              102  LOAD_GLOBAL              OpenSSL
              104  LOAD_ATTR                SSL
              106  LOAD_ATTR                Error
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   152  'to 152'
              112  POP_TOP          
              114  STORE_FAST               'e'
              116  POP_TOP          
              118  SETUP_FINALLY       140  'to 140'

 L. 267       120  LOAD_GLOBAL              ssl
              122  LOAD_METHOD              SSLError
              124  LOAD_STR                 'bad ca_certs: %r'
              126  LOAD_FAST                'ca_certs'
              128  BINARY_MODULO    
              130  LOAD_FAST                'e'
              132  CALL_METHOD_2         2  ''
              134  RAISE_VARARGS_1       1  'exception instance'
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM_FINALLY   118  '118'
              140  LOAD_CONST               None
              142  STORE_FAST               'e'
              144  DELETE_FAST              'e'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_ABSOLUTE       164  'to 164'
            152_0  COME_FROM           110  '110'
              152  END_FINALLY      
              154  JUMP_FORWARD        164  'to 164'
            156_0  COME_FROM            80  '80'

 L. 269       156  LOAD_FAST                'ctx'
              158  LOAD_METHOD              set_default_verify_paths
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          
            164_0  COME_FROM           154  '154'

 L. 272       164  LOAD_CONST               131072
              166  STORE_FAST               'OP_NO_COMPRESSION'

 L. 273       168  LOAD_FAST                'ctx'
              170  LOAD_METHOD              set_options
              172  LOAD_FAST                'OP_NO_COMPRESSION'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 276       178  LOAD_FAST                'ctx'
              180  LOAD_METHOD              set_cipher_list
              182  LOAD_GLOBAL              DEFAULT_SSL_CIPHER_LIST
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 278       188  LOAD_GLOBAL              OpenSSL
              190  LOAD_ATTR                SSL
              192  LOAD_METHOD              Connection
              194  LOAD_FAST                'ctx'
              196  LOAD_FAST                'sock'
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'cnx'

 L. 279       202  LOAD_FAST                'cnx'
              204  LOAD_METHOD              set_tlsext_host_name
              206  LOAD_FAST                'server_hostname'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          

 L. 280       212  LOAD_FAST                'cnx'
              214  LOAD_METHOD              set_connect_state
              216  CALL_METHOD_0         0  ''
              218  POP_TOP          

 L. 282       220  SETUP_FINALLY       234  'to 234'

 L. 283       222  LOAD_FAST                'cnx'
              224  LOAD_METHOD              do_handshake
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
              230  POP_BLOCK        
              232  BREAK_LOOP          362  'to 362'
            234_0  COME_FROM_FINALLY   220  '220'

 L. 284       234  DUP_TOP          
              236  LOAD_GLOBAL              OpenSSL
              238  LOAD_ATTR                SSL
              240  LOAD_ATTR                WantReadError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   304  'to 304'
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 285       254  LOAD_GLOBAL              select
              256  LOAD_METHOD              select
              258  LOAD_FAST                'sock'
              260  BUILD_LIST_1          1 
              262  BUILD_LIST_0          0 
              264  BUILD_LIST_0          0 
              266  LOAD_FAST                'sock'
              268  LOAD_METHOD              gettimeout
              270  CALL_METHOD_0         0  ''
              272  CALL_METHOD_4         4  ''
              274  UNPACK_SEQUENCE_3     3 
              276  STORE_FAST               'rd'
              278  STORE_FAST               '_'
              280  STORE_FAST               '_'

 L. 286       282  LOAD_FAST                'rd'
          284_286  POP_JUMP_IF_TRUE    296  'to 296'

 L. 287       288  LOAD_GLOBAL              timeout
              290  LOAD_STR                 'select timed out'
              292  CALL_FUNCTION_1       1  ''
              294  RAISE_VARARGS_1       1  'exception instance'
            296_0  COME_FROM           284  '284'

 L. 288       296  POP_EXCEPT       
              298  JUMP_BACK           220  'to 220'
              300  POP_EXCEPT       
              302  BREAK_LOOP          362  'to 362'
            304_0  COME_FROM           244  '244'

 L. 289       304  DUP_TOP          
              306  LOAD_GLOBAL              OpenSSL
              308  LOAD_ATTR                SSL
              310  LOAD_ATTR                Error
              312  COMPARE_OP               exception-match
          314_316  POP_JUMP_IF_FALSE   354  'to 354'
              318  POP_TOP          
              320  STORE_FAST               'e'
              322  POP_TOP          
              324  SETUP_FINALLY       342  'to 342'

 L. 290       326  LOAD_GLOBAL              ssl
              328  LOAD_METHOD              SSLError
              330  LOAD_STR                 'bad handshake'
              332  LOAD_FAST                'e'
              334  CALL_METHOD_2         2  ''
              336  RAISE_VARARGS_1       1  'exception instance'
              338  POP_BLOCK        
              340  BEGIN_FINALLY    
            342_0  COME_FROM_FINALLY   324  '324'
              342  LOAD_CONST               None
              344  STORE_FAST               'e'
              346  DELETE_FAST              'e'
              348  END_FINALLY      
              350  POP_EXCEPT       
              352  BREAK_LOOP          362  'to 362'
            354_0  COME_FROM           314  '314'
              354  END_FINALLY      

 L. 291   356_358  BREAK_LOOP          362  'to 362'
              360  JUMP_BACK           220  'to 220'

 L. 293       362  LOAD_GLOBAL              WrappedSocket
              364  LOAD_FAST                'cnx'
              366  LOAD_FAST                'sock'
              368  CALL_FUNCTION_2       2  ''
              370  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 250