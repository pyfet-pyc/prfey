# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\ocsp.py
from __future__ import absolute_import, division, print_function
import functools
from cryptography import utils, x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends.openssl.decode_asn1 import _CRL_ENTRY_REASON_CODE_TO_ENUM, _asn1_integer_to_int, _asn1_string_to_bytes, _decode_x509_name, _obj2txt, _parse_asn1_generalized_time
from cryptography.hazmat.backends.openssl.x509 import _Certificate
from cryptography.hazmat.primitives import serialization
from cryptography.x509.ocsp import OCSPCertStatus, OCSPRequest, OCSPResponse, OCSPResponseStatus, _CERT_STATUS_TO_ENUM, _OIDS_TO_HASH, _RESPONSE_STATUS_TO_ENUM

def _requires_successful_response(func):

    @functools.wraps(func)
    def wrapper--- This code section failed: ---

 L.  35         0  LOAD_FAST                'self'
                2  LOAD_ATTR                response_status
                4  LOAD_GLOBAL              OCSPResponseStatus
                6  LOAD_ATTR                SUCCESSFUL
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L.  36        12  LOAD_GLOBAL              ValueError

 L.  37        14  LOAD_STR                 'OCSP response status is not successful so the property has no value'

 L.  36        16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
               20  JUMP_FORWARD         38  'to 38'
             22_0  COME_FROM            10  '10'

 L.  41        22  LOAD_DEREF               'func'
               24  LOAD_FAST                'self'
               26  BUILD_LIST_1          1 
               28  LOAD_FAST                'args'
               30  CALL_FINALLY         33  'to 33'
               32  WITH_CLEANUP_FINISH
               34  CALL_FUNCTION_EX      0  'positional arguments only'
               36  RETURN_VALUE     
             38_0  COME_FROM            20  '20'

Parse error at or near `CALL_FINALLY' instruction at offset 30

    return wrapper


def _issuer_key_hash(backend, cert_id):
    key_hash = backend._ffi.new('ASN1_OCTET_STRING **')
    res = backend._lib.OCSP_id_get0_info(backend._ffi.NULL, backend._ffi.NULL, key_hash, backend._ffi.NULL, cert_id)
    backend.openssl_assert(res == 1)
    backend.openssl_assert(key_hash[0] != backend._ffi.NULL)
    return _asn1_string_to_bytes(backend, key_hash[0])


def _issuer_name_hash(backend, cert_id):
    name_hash = backend._ffi.new('ASN1_OCTET_STRING **')
    res = backend._lib.OCSP_id_get0_info(name_hash, backend._ffi.NULL, backend._ffi.NULL, backend._ffi.NULL, cert_id)
    backend.openssl_assert(res == 1)
    backend.openssl_assert(name_hash[0] != backend._ffi.NULL)
    return _asn1_string_to_bytes(backend, name_hash[0])


def _serial_number(backend, cert_id):
    num = backend._ffi.new('ASN1_INTEGER **')
    res = backend._lib.OCSP_id_get0_info(backend._ffi.NULL, backend._ffi.NULL, backend._ffi.NULL, num, cert_id)
    backend.openssl_assert(res == 1)
    backend.openssl_assert(num[0] != backend._ffi.NULL)
    return _asn1_integer_to_int(backend, num[0])


def _hash_algorithm--- This code section failed: ---

 L.  85         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _ffi
                4  LOAD_METHOD              new
                6  LOAD_STR                 'ASN1_OBJECT **'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'asn1obj'

 L.  86        12  LOAD_FAST                'backend'
               14  LOAD_ATTR                _lib
               16  LOAD_METHOD              OCSP_id_get0_info

 L.  87        18  LOAD_FAST                'backend'
               20  LOAD_ATTR                _ffi
               22  LOAD_ATTR                NULL

 L.  88        24  LOAD_FAST                'asn1obj'

 L.  89        26  LOAD_FAST                'backend'
               28  LOAD_ATTR                _ffi
               30  LOAD_ATTR                NULL

 L.  90        32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _ffi
               36  LOAD_ATTR                NULL

 L.  91        38  LOAD_FAST                'cert_id'

 L.  86        40  CALL_METHOD_5         5  ''
               42  STORE_FAST               'res'

 L.  93        44  LOAD_FAST                'backend'
               46  LOAD_METHOD              openssl_assert
               48  LOAD_FAST                'res'
               50  LOAD_CONST               1
               52  COMPARE_OP               ==
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  94        58  LOAD_FAST                'backend'
               60  LOAD_METHOD              openssl_assert
               62  LOAD_FAST                'asn1obj'
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'backend'
               70  LOAD_ATTR                _ffi
               72  LOAD_ATTR                NULL
               74  COMPARE_OP               !=
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  95        80  LOAD_GLOBAL              _obj2txt
               82  LOAD_FAST                'backend'
               84  LOAD_FAST                'asn1obj'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'oid'

 L.  96        94  SETUP_FINALLY       106  'to 106'

 L.  97        96  LOAD_GLOBAL              _OIDS_TO_HASH
               98  LOAD_FAST                'oid'
              100  BINARY_SUBSCR    
              102  POP_BLOCK        
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    94  '94'

 L.  98       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  <121>               136  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.  99       118  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 100       120  LOAD_STR                 'Signature algorithm OID: {} not recognized'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'oid'
              126  CALL_METHOD_1         1  ''

 L.  99       128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
              136  <48>             
            138_0  COME_FROM           134  '134'

Parse error at or near `<121>' instruction at offset 110


@utils.register_interface(OCSPResponse)
class _OCSPResponse(object):

    def __init__--- This code section failed: ---

 L. 107         0  LOAD_FAST                'backend'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _backend

 L. 108         6  LOAD_FAST                'ocsp_response'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _ocsp_response

 L. 109        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _backend
               16  LOAD_ATTR                _lib
               18  LOAD_METHOD              OCSP_response_status
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _ocsp_response
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'status'

 L. 110        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _backend
               32  LOAD_METHOD              openssl_assert
               34  LOAD_FAST                'status'
               36  LOAD_GLOBAL              _RESPONSE_STATUS_TO_ENUM
               38  <118>                 0  ''
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 111        44  LOAD_GLOBAL              _RESPONSE_STATUS_TO_ENUM
               46  LOAD_FAST                'status'
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _status

 L. 112        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _status
               58  LOAD_GLOBAL              OCSPResponseStatus
               60  LOAD_ATTR                SUCCESSFUL
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   252  'to 252'

 L. 113        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _lib
               72  LOAD_METHOD              OCSP_response_get1_basic

 L. 114        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _ocsp_response

 L. 113        78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'basic'

 L. 116        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _backend
               86  LOAD_METHOD              openssl_assert
               88  LOAD_FAST                'basic'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _backend
               94  LOAD_ATTR                _ffi
               96  LOAD_ATTR                NULL
               98  COMPARE_OP               !=
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 117       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _backend
              108  LOAD_ATTR                _ffi
              110  LOAD_METHOD              gc

 L. 118       112  LOAD_FAST                'basic'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _backend
              118  LOAD_ATTR                _lib
              120  LOAD_ATTR                OCSP_BASICRESP_free

 L. 117       122  CALL_METHOD_2         2  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _basic

 L. 120       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _backend
              132  LOAD_ATTR                _lib
              134  LOAD_METHOD              OCSP_resp_count
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _basic
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'num_resp'

 L. 121       144  LOAD_FAST                'num_resp'
              146  LOAD_CONST               1
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L. 122       152  LOAD_GLOBAL              ValueError

 L. 123       154  LOAD_STR                 'OCSP response contains more than one SINGLERESP structure, which this library does not support. {} found'
              156  LOAD_METHOD              format

 L. 125       158  LOAD_FAST                'num_resp'

 L. 123       160  CALL_METHOD_1         1  ''

 L. 122       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           150  '150'

 L. 127       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _backend
              170  LOAD_ATTR                _lib
              172  LOAD_METHOD              OCSP_resp_get0
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                _basic
              178  LOAD_CONST               0
              180  CALL_METHOD_2         2  ''
              182  LOAD_FAST                'self'
              184  STORE_ATTR               _single

 L. 128       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _backend
              190  LOAD_METHOD              openssl_assert

 L. 129       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _single
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                _backend
              200  LOAD_ATTR                _ffi
              202  LOAD_ATTR                NULL
              204  COMPARE_OP               !=

 L. 128       206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 131       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _backend
              214  LOAD_ATTR                _lib
              216  LOAD_METHOD              OCSP_SINGLERESP_get0_id

 L. 132       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _single

 L. 131       222  CALL_METHOD_1         1  ''
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _cert_id

 L. 134       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _backend
              232  LOAD_METHOD              openssl_assert

 L. 135       234  LOAD_FAST                'self'
              236  LOAD_ATTR                _cert_id
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                _backend
              242  LOAD_ATTR                _ffi
              244  LOAD_ATTR                NULL
              246  COMPARE_OP               !=

 L. 134       248  CALL_METHOD_1         1  ''
              250  POP_TOP          
            252_0  COME_FROM            64  '64'

Parse error at or near `<118>' instruction at offset 38

    response_status = utils.read_only_property('_status')

    @property
    @_requires_successful_response
    def signature_algorithm_oid(self):
        alg = self._backend._lib.OCSP_resp_get0_tbs_sigalg(self._basic)
        self._backend.openssl_assert(alg != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg.algorithm)
        return x509.ObjectIdentifier(oid)

    @property
    @_requires_successful_response
    def signature_hash_algorithm--- This code section failed: ---

 L. 151         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 152         6  SETUP_FINALLY        20  'to 20'

 L. 153         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 154        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                50  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 155        32  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 156        34  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'oid'
               40  CALL_METHOD_1         1  ''

 L. 155        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 24

    @property
    @_requires_successful_response
    def signature(self):
        sig = self._backend._lib.OCSP_resp_get0_signature(self._basic)
        self._backend.openssl_assert(sig != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig)

    @property
    @_requires_successful_response
    def tbs_response_bytes(self):
        respdata = self._backend._lib.OCSP_resp_get0_respdata(self._basic)
        self._backend.openssl_assert(respdata != self._backend._ffi.NULL)
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_OCSP_RESPDATArespdatapp
        self._backend.openssl_assert(pp[0] != self._backend._ffi.NULL)
        pp = self._backend._ffi.gcpp(lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        self._backend.openssl_assert(res > 0)
        return self._backend._ffi.bufferpp[0]res[:]

    @property
    @_requires_successful_response
    def certificates(self):
        sk_x509 = self._backend._lib.OCSP_resp_get0_certs(self._basic)
        num = self._backend._lib.sk_X509_num(sk_x509)
        certs = []
        for i in range(num):
            x509 = self._backend._lib.sk_X509_valuesk_x509i
            self._backend.openssl_assert(x509 != self._backend._ffi.NULL)
            cert = _Certificate(self._backend, x509)
            cert._ocsp_resp = self
            certs.append(cert)
        else:
            return certs

    @property
    @_requires_successful_response
    def responder_key_hash(self):
        _, asn1_string = self._responder_key_name()
        if asn1_string == self._backend._ffi.NULL:
            return
        return _asn1_string_to_bytes(self._backend, asn1_string)

    @property
    @_requires_successful_response
    def responder_name(self):
        x509_name, _ = self._responder_key_name()
        if x509_name == self._backend._ffi.NULL:
            return
        return _decode_x509_name(self._backend, x509_name)

    def _responder_key_name(self):
        asn1_string = self._backend._ffi.new('ASN1_OCTET_STRING **')
        x509_name = self._backend._ffi.new('X509_NAME **')
        res = self._backend._lib.OCSP_resp_get0_id(self._basic, asn1_string, x509_name)
        self._backend.openssl_assert(res == 1)
        return (
         x509_name[0], asn1_string[0])

    @property
    @_requires_successful_response
    def produced_at(self):
        produced_at = self._backend._lib.OCSP_resp_get0_produced_at(self._basic)
        return _parse_asn1_generalized_time(self._backend, produced_at)

    @property
    @_requires_successful_response
    def certificate_status--- This code section failed: ---

 L. 236         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_ATTR                _lib
                6  LOAD_METHOD              OCSP_single_get0_status

 L. 237         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _single

 L. 238        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _backend
               16  LOAD_ATTR                _ffi
               18  LOAD_ATTR                NULL

 L. 239        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _ffi
               26  LOAD_ATTR                NULL

 L. 240        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _backend
               32  LOAD_ATTR                _ffi
               34  LOAD_ATTR                NULL

 L. 241        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _backend
               40  LOAD_ATTR                _ffi
               42  LOAD_ATTR                NULL

 L. 236        44  CALL_METHOD_5         5  ''
               46  STORE_FAST               'status'

 L. 243        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _backend
               52  LOAD_METHOD              openssl_assert
               54  LOAD_FAST                'status'
               56  LOAD_GLOBAL              _CERT_STATUS_TO_ENUM
               58  <118>                 0  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 244        64  LOAD_GLOBAL              _CERT_STATUS_TO_ENUM
               66  LOAD_FAST                'status'
               68  BINARY_SUBSCR    
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 58

    @property
    @_requires_successful_response
    def revocation_time--- This code section failed: ---

 L. 249         0  LOAD_FAST                'self'
                2  LOAD_ATTR                certificate_status
                4  LOAD_GLOBAL              OCSPCertStatus
                6  LOAD_ATTR                REVOKED
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 250        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 252        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _backend
               20  LOAD_ATTR                _ffi
               22  LOAD_METHOD              new
               24  LOAD_STR                 'ASN1_GENERALIZEDTIME **'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'asn1_time'

 L. 253        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              OCSP_single_get0_status

 L. 254        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _single

 L. 255        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _backend
               46  LOAD_ATTR                _ffi
               48  LOAD_ATTR                NULL

 L. 256        50  LOAD_FAST                'asn1_time'

 L. 257        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _backend
               56  LOAD_ATTR                _ffi
               58  LOAD_ATTR                NULL

 L. 258        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _backend
               64  LOAD_ATTR                _ffi
               66  LOAD_ATTR                NULL

 L. 253        68  CALL_METHOD_5         5  ''
               70  POP_TOP          

 L. 260        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _backend
               76  LOAD_METHOD              openssl_assert
               78  LOAD_FAST                'asn1_time'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _backend
               88  LOAD_ATTR                _ffi
               90  LOAD_ATTR                NULL
               92  COMPARE_OP               !=
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 261        98  LOAD_GLOBAL              _parse_asn1_generalized_time
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _backend
              104  LOAD_FAST                'asn1_time'
              106  LOAD_CONST               0
              108  BINARY_SUBSCR    
              110  CALL_FUNCTION_2       2  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    @_requires_successful_response
    def revocation_reason--- This code section failed: ---

 L. 266         0  LOAD_FAST                'self'
                2  LOAD_ATTR                certificate_status
                4  LOAD_GLOBAL              OCSPCertStatus
                6  LOAD_ATTR                REVOKED
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 267        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 269        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _backend
               20  LOAD_ATTR                _ffi
               22  LOAD_METHOD              new
               24  LOAD_STR                 'int *'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'reason_ptr'

 L. 270        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              OCSP_single_get0_status

 L. 271        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _single

 L. 272        42  LOAD_FAST                'reason_ptr'

 L. 273        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _ffi
               50  LOAD_ATTR                NULL

 L. 274        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _backend
               56  LOAD_ATTR                _ffi
               58  LOAD_ATTR                NULL

 L. 275        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _backend
               64  LOAD_ATTR                _ffi
               66  LOAD_ATTR                NULL

 L. 270        68  CALL_METHOD_5         5  ''
               70  POP_TOP          

 L. 278        72  LOAD_FAST                'reason_ptr'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_CONST               -1
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L. 279        84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            82  '82'

 L. 281        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _backend
               92  LOAD_METHOD              openssl_assert

 L. 282        94  LOAD_FAST                'reason_ptr'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
              102  <118>                 0  ''

 L. 281       104  CALL_METHOD_1         1  ''
              106  POP_TOP          

 L. 284       108  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
              110  LOAD_FAST                'reason_ptr'
              112  LOAD_CONST               0
              114  BINARY_SUBSCR    
              116  BINARY_SUBSCR    
              118  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    @property
    @_requires_successful_response
    def this_update(self):
        asn1_time = self._backend._ffi.new('ASN1_GENERALIZEDTIME **')
        self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, self._backend._ffi.NULL, asn1_time, self._backend._ffi.NULL)
        self._backend.openssl_assert(asn1_time[0] != self._backend._ffi.NULL)
        return _parse_asn1_generalized_time(self._backend, asn1_time[0])

    @property
    @_requires_successful_response
    def next_update(self):
        asn1_time = self._backend._ffi.new('ASN1_GENERALIZEDTIME **')
        self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, asn1_time)
        if asn1_time[0] != self._backend._ffi.NULL:
            return _parse_asn1_generalized_time(self._backend, asn1_time[0])
        return

    @property
    @_requires_successful_response
    def issuer_key_hash(self):
        return _issuer_key_hash(self._backend, self._cert_id)

    @property
    @_requires_successful_response
    def issuer_name_hash(self):
        return _issuer_name_hash(self._backend, self._cert_id)

    @property
    @_requires_successful_response
    def hash_algorithm(self):
        return _hash_algorithm(self._backend, self._cert_id)

    @property
    @_requires_successful_response
    def serial_number(self):
        return _serial_number(self._backend, self._cert_id)

    @utils.cached_property
    @_requires_successful_response
    def extensions(self):
        return self._backend._ocsp_basicresp_ext_parser.parse(self._basic)

    @utils.cached_property
    @_requires_successful_response
    def single_extensions(self):
        return self._backend._ocsp_singleresp_ext_parser.parse(self._single)

    def public_bytes--- This code section failed: ---

 L. 347         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                DER
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 348        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'The only allowed encoding value is Encoding.DER'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 350        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_METHOD              _create_mem_bio_gc
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'bio'

 L. 351        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              i2d_OCSP_RESPONSE_bio

 L. 352        38  LOAD_FAST                'bio'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ocsp_response

 L. 351        44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'res'

 L. 354        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _backend
               52  LOAD_METHOD              openssl_assert
               54  LOAD_FAST                'res'
               56  LOAD_CONST               0
               58  COMPARE_OP               >
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 355        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _read_mem_bio
               70  LOAD_FAST                'bio'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


@utils.register_interface(OCSPRequest)
class _OCSPRequest(object):

    def __init__(self, backend, ocsp_request):
        if backend._lib.OCSP_request_onereq_count(ocsp_request) > 1:
            raise NotImplementedError('OCSP request contains more than one request')
        self._backend = backend
        self._ocsp_request = ocsp_request
        self._request = self._backend._lib.OCSP_request_onereq_get0self._ocsp_request0
        self._backend.openssl_assert(self._request != self._backend._ffi.NULL)
        self._cert_id = self._backend._lib.OCSP_onereq_get0_id(self._request)
        self._backend.openssl_assert(self._cert_id != self._backend._ffi.NULL)

    @property
    def issuer_key_hash(self):
        return _issuer_key_hash(self._backend, self._cert_id)

    @property
    def issuer_name_hash(self):
        return _issuer_name_hash(self._backend, self._cert_id)

    @property
    def serial_number(self):
        return _serial_number(self._backend, self._cert_id)

    @property
    def hash_algorithm(self):
        return _hash_algorithm(self._backend, self._cert_id)

    @utils.cached_property
    def extensions(self):
        return self._backend._ocsp_req_ext_parser.parse(self._ocsp_request)

    def public_bytes--- This code section failed: ---

 L. 395         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                DER
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 396        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'The only allowed encoding value is Encoding.DER'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 398        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_METHOD              _create_mem_bio_gc
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'bio'

 L. 399        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              i2d_OCSP_REQUEST_bio
               38  LOAD_FAST                'bio'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ocsp_request
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'res'

 L. 400        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _backend
               52  LOAD_METHOD              openssl_assert
               54  LOAD_FAST                'res'
               56  LOAD_CONST               0
               58  COMPARE_OP               >
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 401        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _read_mem_bio
               70  LOAD_FAST                'bio'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1