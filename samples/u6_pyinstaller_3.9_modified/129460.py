# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\ocsp.py
import datetime, typing
from cryptography import utils, x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends.openssl.decode_asn1 import _CRL_ENTRY_REASON_CODE_TO_ENUM, _asn1_integer_to_int, _asn1_string_to_bytes, _decode_x509_name, _obj2txt, _parse_asn1_generalized_time
from cryptography.hazmat.backends.openssl.x509 import _Certificate
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.ocsp import OCSPCertStatus, OCSPRequest, OCSPResponse, OCSPResponseStatus, _CERT_STATUS_TO_ENUM, _OIDS_TO_HASH, _RESPONSE_STATUS_TO_ENUM

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

 L.  70         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _ffi
                4  LOAD_METHOD              new
                6  LOAD_STR                 'ASN1_OBJECT **'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'asn1obj'

 L.  71        12  LOAD_FAST                'backend'
               14  LOAD_ATTR                _lib
               16  LOAD_METHOD              OCSP_id_get0_info

 L.  72        18  LOAD_FAST                'backend'
               20  LOAD_ATTR                _ffi
               22  LOAD_ATTR                NULL

 L.  73        24  LOAD_FAST                'asn1obj'

 L.  74        26  LOAD_FAST                'backend'
               28  LOAD_ATTR                _ffi
               30  LOAD_ATTR                NULL

 L.  75        32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _ffi
               36  LOAD_ATTR                NULL

 L.  76        38  LOAD_FAST                'cert_id'

 L.  71        40  CALL_METHOD_5         5  ''
               42  STORE_FAST               'res'

 L.  78        44  LOAD_FAST                'backend'
               46  LOAD_METHOD              openssl_assert
               48  LOAD_FAST                'res'
               50  LOAD_CONST               1
               52  COMPARE_OP               ==
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  79        58  LOAD_FAST                'backend'
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

 L.  80        80  LOAD_GLOBAL              _obj2txt
               82  LOAD_FAST                'backend'
               84  LOAD_FAST                'asn1obj'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'oid'

 L.  81        94  SETUP_FINALLY       106  'to 106'

 L.  82        96  LOAD_GLOBAL              _OIDS_TO_HASH
               98  LOAD_FAST                'oid'
              100  BINARY_SUBSCR    
              102  POP_BLOCK        
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    94  '94'

 L.  83       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  <121>               136  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.  84       118  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  85       120  LOAD_STR                 'Signature algorithm OID: {} not recognized'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'oid'
              126  CALL_METHOD_1         1  ''

 L.  84       128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
              136  <48>             
            138_0  COME_FROM           134  '134'

Parse error at or near `<121>' instruction at offset 110


class _OCSPResponse(OCSPResponse):

    def __init__--- This code section failed: ---

 L.  91         0  LOAD_FAST                'backend'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _backend

 L.  92         6  LOAD_FAST                'ocsp_response'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _ocsp_response

 L.  93        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _backend
               16  LOAD_ATTR                _lib
               18  LOAD_METHOD              OCSP_response_status
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _ocsp_response
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'status'

 L.  94        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _backend
               32  LOAD_METHOD              openssl_assert
               34  LOAD_FAST                'status'
               36  LOAD_GLOBAL              _RESPONSE_STATUS_TO_ENUM
               38  <118>                 0  ''
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  95        44  LOAD_GLOBAL              _RESPONSE_STATUS_TO_ENUM
               46  LOAD_FAST                'status'
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _status

 L.  96        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _status
               58  LOAD_GLOBAL              OCSPResponseStatus
               60  LOAD_ATTR                SUCCESSFUL
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   252  'to 252'

 L.  97        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _lib
               72  LOAD_METHOD              OCSP_response_get1_basic

 L.  98        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _ocsp_response

 L.  97        78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'basic'

 L. 100        82  LOAD_FAST                'self'
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

 L. 101       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _backend
              108  LOAD_ATTR                _ffi
              110  LOAD_METHOD              gc

 L. 102       112  LOAD_FAST                'basic'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _backend
              118  LOAD_ATTR                _lib
              120  LOAD_ATTR                OCSP_BASICRESP_free

 L. 101       122  CALL_METHOD_2         2  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _basic

 L. 104       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _backend
              132  LOAD_ATTR                _lib
              134  LOAD_METHOD              OCSP_resp_count
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _basic
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'num_resp'

 L. 105       144  LOAD_FAST                'num_resp'
              146  LOAD_CONST               1
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L. 106       152  LOAD_GLOBAL              ValueError

 L. 107       154  LOAD_STR                 'OCSP response contains more than one SINGLERESP structure, which this library does not support. {} found'
              156  LOAD_METHOD              format

 L. 109       158  LOAD_FAST                'num_resp'

 L. 107       160  CALL_METHOD_1         1  ''

 L. 106       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           150  '150'

 L. 111       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _backend
              170  LOAD_ATTR                _lib
              172  LOAD_METHOD              OCSP_resp_get0
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                _basic
              178  LOAD_CONST               0
              180  CALL_METHOD_2         2  ''
              182  LOAD_FAST                'self'
              184  STORE_ATTR               _single

 L. 112       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _backend
              190  LOAD_METHOD              openssl_assert

 L. 113       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _single
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                _backend
              200  LOAD_ATTR                _ffi
              202  LOAD_ATTR                NULL
              204  COMPARE_OP               !=

 L. 112       206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L. 115       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _backend
              214  LOAD_ATTR                _lib
              216  LOAD_METHOD              OCSP_SINGLERESP_get0_id

 L. 116       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _single

 L. 115       222  CALL_METHOD_1         1  ''
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _cert_id

 L. 118       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _backend
              232  LOAD_METHOD              openssl_assert

 L. 119       234  LOAD_FAST                'self'
              236  LOAD_ATTR                _cert_id
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                _backend
              242  LOAD_ATTR                _ffi
              244  LOAD_ATTR                NULL
              246  COMPARE_OP               !=

 L. 118       248  CALL_METHOD_1         1  ''
              250  POP_TOP          
            252_0  COME_FROM            64  '64'

Parse error at or near `<118>' instruction at offset 38

    response_status = utils.read_only_property('_status')

    def _requires_successful_response(self) -> None:
        if self.response_status != OCSPResponseStatus.SUCCESSFUL:
            raise ValueError('OCSP response status is not successful so the property has no value')

    @property
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        self._requires_successful_response()
        alg = self._backend._lib.OCSP_resp_get0_tbs_sigalg(self._basic)
        self._backend.openssl_assert(alg != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg.algorithm)
        return x509.ObjectIdentifier(oid)

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 143         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _requires_successful_response
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 144         8  LOAD_FAST                'self'
               10  LOAD_ATTR                signature_algorithm_oid
               12  STORE_FAST               'oid'

 L. 145        14  SETUP_FINALLY        28  'to 28'

 L. 146        16  LOAD_GLOBAL              x509
               18  LOAD_ATTR                _SIG_OIDS_TO_HASH
               20  LOAD_FAST                'oid'
               22  BINARY_SUBSCR    
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    14  '14'

 L. 147        28  DUP_TOP          
               30  LOAD_GLOBAL              KeyError
               32  <121>                58  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 148        40  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 149        42  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               44  LOAD_METHOD              format
               46  LOAD_FAST                'oid'
               48  CALL_METHOD_1         1  ''

 L. 148        50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  <48>             
             60_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 32

    @property
    def signature(self) -> bytes:
        self._requires_successful_response()
        sig = self._backend._lib.OCSP_resp_get0_signature(self._basic)
        self._backend.openssl_assert(sig != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig)

    @property
    def tbs_response_bytes(self) -> bytes:
        self._requires_successful_response()
        respdata = self._backend._lib.OCSP_resp_get0_respdata(self._basic)
        self._backend.openssl_assert(respdata != self._backend._ffi.NULL)
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_OCSP_RESPDATArespdatapp
        self._backend.openssl_assert(pp[0] != self._backend._ffi.NULL)
        pp = self._backend._ffi.gcpp(lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        self._backend.openssl_assert(res > 0)
        return self._backend._ffi.bufferpp[0]res[:]

    @property
    def certificates(self) -> typing.List[x509.Certificate]:
        self._requires_successful_response()
        sk_x509 = self._backend._lib.OCSP_resp_get0_certs(self._basic)
        num = self._backend._lib.sk_X509_num(sk_x509)
        certs = []
        for i in range(num):
            x509_ptr = self._backend._lib.sk_X509_valuesk_x509i
            self._backend.openssl_assert(x509_ptr != self._backend._ffi.NULL)
            cert = _Certificate(self._backend, x509_ptr)
            cert._ocsp_resp_ref = self
            certs.append(cert)
        else:
            return certs

    @property
    def responder_key_hash(self) -> typing.Optional[bytes]:
        self._requires_successful_response()
        _, asn1_string = self._responder_key_name()
        if asn1_string == self._backend._ffi.NULL:
            return
        return _asn1_string_to_bytes(self._backend, asn1_string)

    @property
    def responder_name(self) -> typing.Optional[x509.Name]:
        self._requires_successful_response()
        x509_name, _ = self._responder_key_name()
        if x509_name == self._backend._ffi.NULL:
            return
        return _decode_x509_name(self._backend, x509_name)

    def _responder_key_name(self):
        asn1_string = self._backend._ffi.new('ASN1_OCTET_STRING **')
        x509_name = self._backend._ffi.new('X509_NAME **')
        res = self._backend._lib.OCSP_resp_get0_id(self._basic, asn1_string, x509_name)
        self._backend.openssl_assert(res == 1)
        return (x509_name[0], asn1_string[0])

    @property
    def produced_at(self) -> datetime.datetime:
        self._requires_successful_response()
        produced_at = self._backend._lib.OCSP_resp_get0_produced_at(self._basic)
        return _parse_asn1_generalized_time(self._backend, produced_at)

    @property
    def certificate_status--- This code section failed: ---

 L. 228         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _requires_successful_response
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 229         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _backend
               12  LOAD_ATTR                _lib
               14  LOAD_METHOD              OCSP_single_get0_status

 L. 230        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _single

 L. 231        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _ffi
               26  LOAD_ATTR                NULL

 L. 232        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _backend
               32  LOAD_ATTR                _ffi
               34  LOAD_ATTR                NULL

 L. 233        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _backend
               40  LOAD_ATTR                _ffi
               42  LOAD_ATTR                NULL

 L. 234        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _ffi
               50  LOAD_ATTR                NULL

 L. 229        52  CALL_METHOD_5         5  ''
               54  STORE_FAST               'status'

 L. 236        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _backend
               60  LOAD_METHOD              openssl_assert
               62  LOAD_FAST                'status'
               64  LOAD_GLOBAL              _CERT_STATUS_TO_ENUM
               66  <118>                 0  ''
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 237        72  LOAD_GLOBAL              _CERT_STATUS_TO_ENUM
               74  LOAD_FAST                'status'
               76  BINARY_SUBSCR    
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 66

    @property
    def revocation_time--- This code section failed: ---

 L. 241         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _requires_successful_response
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 242         8  LOAD_FAST                'self'
               10  LOAD_ATTR                certificate_status
               12  LOAD_GLOBAL              OCSPCertStatus
               14  LOAD_ATTR                REVOKED
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 243        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 245        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _backend
               28  LOAD_ATTR                _ffi
               30  LOAD_METHOD              new
               32  LOAD_STR                 'ASN1_GENERALIZEDTIME **'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'asn1_time'

 L. 246        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _backend
               42  LOAD_ATTR                _lib
               44  LOAD_METHOD              OCSP_single_get0_status

 L. 247        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _single

 L. 248        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _backend
               54  LOAD_ATTR                _ffi
               56  LOAD_ATTR                NULL

 L. 249        58  LOAD_FAST                'asn1_time'

 L. 250        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _backend
               64  LOAD_ATTR                _ffi
               66  LOAD_ATTR                NULL

 L. 251        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _backend
               72  LOAD_ATTR                _ffi
               74  LOAD_ATTR                NULL

 L. 246        76  CALL_METHOD_5         5  ''
               78  POP_TOP          

 L. 253        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _backend
               84  LOAD_METHOD              openssl_assert
               86  LOAD_FAST                'asn1_time'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _backend
               96  LOAD_ATTR                _ffi
               98  LOAD_ATTR                NULL
              100  COMPARE_OP               !=
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 254       106  LOAD_GLOBAL              _parse_asn1_generalized_time
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _backend
              112  LOAD_FAST                'asn1_time'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  CALL_FUNCTION_2       2  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    @property
    def revocation_reason--- This code section failed: ---

 L. 258         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _requires_successful_response
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 259         8  LOAD_FAST                'self'
               10  LOAD_ATTR                certificate_status
               12  LOAD_GLOBAL              OCSPCertStatus
               14  LOAD_ATTR                REVOKED
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 260        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 262        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _backend
               28  LOAD_ATTR                _ffi
               30  LOAD_METHOD              new
               32  LOAD_STR                 'int *'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'reason_ptr'

 L. 263        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _backend
               42  LOAD_ATTR                _lib
               44  LOAD_METHOD              OCSP_single_get0_status

 L. 264        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _single

 L. 265        50  LOAD_FAST                'reason_ptr'

 L. 266        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _backend
               56  LOAD_ATTR                _ffi
               58  LOAD_ATTR                NULL

 L. 267        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _backend
               64  LOAD_ATTR                _ffi
               66  LOAD_ATTR                NULL

 L. 268        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _backend
               72  LOAD_ATTR                _ffi
               74  LOAD_ATTR                NULL

 L. 263        76  CALL_METHOD_5         5  ''
               78  POP_TOP          

 L. 271        80  LOAD_FAST                'reason_ptr'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  LOAD_CONST               -1
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE    96  'to 96'

 L. 272        92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'

 L. 274        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _backend
              100  LOAD_METHOD              openssl_assert

 L. 275       102  LOAD_FAST                'reason_ptr'
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
              110  <118>                 0  ''

 L. 274       112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 277       116  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
              118  LOAD_FAST                'reason_ptr'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  BINARY_SUBSCR    
              126  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 16

    @property
    def this_update(self) -> datetime.datetime:
        self._requires_successful_response()
        asn1_time = self._backend._ffi.new('ASN1_GENERALIZEDTIME **')
        self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, self._backend._ffi.NULL, asn1_time, self._backend._ffi.NULL)
        self._backend.openssl_assert(asn1_time[0] != self._backend._ffi.NULL)
        return _parse_asn1_generalized_time(self._backend, asn1_time[0])

    @property
    def next_update(self) -> typing.Optional[datetime.datetime]:
        self._requires_successful_response()
        asn1_time = self._backend._ffi.new('ASN1_GENERALIZEDTIME **')
        self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, asn1_time)
        if asn1_time[0] != self._backend._ffi.NULL:
            return _parse_asn1_generalized_time(self._backend, asn1_time[0])
        return

    @property
    def issuer_key_hash(self) -> bytes:
        self._requires_successful_response()
        return _issuer_key_hash(self._backend, self._cert_id)

    @property
    def issuer_name_hash(self) -> bytes:
        self._requires_successful_response()
        return _issuer_name_hash(self._backend, self._cert_id)

    @property
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        self._requires_successful_response()
        return _hash_algorithm(self._backend, self._cert_id)

    @property
    def serial_number(self) -> int:
        self._requires_successful_response()
        return _serial_number(self._backend, self._cert_id)

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        self._requires_successful_response()
        return self._backend._ocsp_basicresp_ext_parser.parse(self._basic)

    @utils.cached_property
    def single_extensions(self) -> x509.Extensions:
        self._requires_successful_response()
        return self._backend._ocsp_singleresp_ext_parser.parse(self._single)

    def public_bytes--- This code section failed: ---

 L. 340         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                DER
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 341        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'The only allowed encoding value is Encoding.DER'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 343        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_METHOD              _create_mem_bio_gc
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'bio'

 L. 344        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              i2d_OCSP_RESPONSE_bio

 L. 345        38  LOAD_FAST                'bio'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ocsp_response

 L. 344        44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'res'

 L. 347        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _backend
               52  LOAD_METHOD              openssl_assert
               54  LOAD_FAST                'res'
               56  LOAD_CONST               0
               58  COMPARE_OP               >
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 348        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _read_mem_bio
               70  LOAD_FAST                'bio'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class _OCSPRequest(OCSPRequest):

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
    def issuer_key_hash(self) -> bytes:
        return _issuer_key_hash(self._backend, self._cert_id)

    @property
    def issuer_name_hash(self) -> bytes:
        return _issuer_name_hash(self._backend, self._cert_id)

    @property
    def serial_number(self) -> int:
        return _serial_number(self._backend, self._cert_id)

    @property
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        return _hash_algorithm(self._backend, self._cert_id)

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        return self._backend._ocsp_req_ext_parser.parse(self._ocsp_request)

    def public_bytes--- This code section failed: ---

 L. 387         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                DER
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 388        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'The only allowed encoding value is Encoding.DER'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 390        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_METHOD              _create_mem_bio_gc
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'bio'

 L. 391        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              i2d_OCSP_REQUEST_bio
               38  LOAD_FAST                'bio'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ocsp_request
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'res'

 L. 392        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _backend
               52  LOAD_METHOD              openssl_assert
               54  LOAD_FAST                'res'
               56  LOAD_CONST               0
               58  COMPARE_OP               >
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 393        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _read_mem_bio
               70  LOAD_FAST                'bio'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1