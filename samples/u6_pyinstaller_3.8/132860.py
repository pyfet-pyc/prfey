# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   138  'to 138'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  84       120  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  85       122  LOAD_STR                 'Signature algorithm OID: {} not recognized'
              124  LOAD_METHOD              format
              126  LOAD_FAST                'oid'
              128  CALL_METHOD_1         1  ''

 L.  84       130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           112  '112'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'

Parse error at or near `POP_TOP' instruction at offset 116


class _OCSPResponse(OCSPResponse):

    def __init__(self, backend, ocsp_response):
        self._backend = backend
        self._ocsp_response = ocsp_response
        status = self._backend._lib.OCSP_response_status(self._ocsp_response)
        self._backend.openssl_assert(status in _RESPONSE_STATUS_TO_ENUM)
        self._status = _RESPONSE_STATUS_TO_ENUM[status]
        if self._status is OCSPResponseStatus.SUCCESSFUL:
            basic = self._backend._lib.OCSP_response_get1_basic(self._ocsp_response)
            self._backend.openssl_assert(basic != self._backend._ffi.NULL)
            self._basic = self._backend._ffi.gc(basic, self._backend._lib.OCSP_BASICRESP_free)
            num_resp = self._backend._lib.OCSP_resp_count(self._basic)
            if num_resp != 1:
                raise ValueError('OCSP response contains more than one SINGLERESP structure, which this library does not support. {} found'.format(num_resp))
            self._single = self._backend._lib.OCSP_resp_get0(self._basic, 0)
            self._backend.openssl_assert(self._single != self._backend._ffi.NULL)
            self._cert_id = self._backend._lib.OCSP_SINGLERESP_get0_id(self._single)
            self._backend.openssl_assert(self._cert_id != self._backend._ffi.NULL)

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
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    60  'to 60'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 148        42  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 149        44  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               46  LOAD_METHOD              format
               48  LOAD_FAST                'oid'
               50  CALL_METHOD_1         1  ''

 L. 148        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            34  '34'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

Parse error at or near `POP_TOP' instruction at offset 38

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
        res = self._backend._lib.i2d_OCSP_RESPDATA(respdata, pp)
        self._backend.openssl_assert(pp[0] != self._backend._ffi.NULL)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        self._backend.openssl_assert(res > 0)
        return self._backend._ffi.buffer(pp[0], res)[:]

    @property
    def certificates(self) -> typing.List[x509.Certificate]:
        self._requires_successful_response()
        sk_x509 = self._backend._lib.OCSP_resp_get0_certs(self._basic)
        num = self._backend._lib.sk_X509_num(sk_x509)
        certs = []
        for i in range(num):
            x509_ptr = self._backend._lib.sk_X509_value(sk_x509, i)
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
    def certificate_status(self) -> OCSPCertStatus:
        self._requires_successful_response()
        status = self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(status in _CERT_STATUS_TO_ENUM)
        return _CERT_STATUS_TO_ENUM[status]

    @property
    def revocation_time(self) -> typing.Optional[datetime.datetime]:
        self._requires_successful_response()
        if self.certificate_status is not OCSPCertStatus.REVOKED:
            return
        asn1_time = self._backend._ffi.new('ASN1_GENERALIZEDTIME **')
        self._backend._lib.OCSP_single_get0_status(self._single, self._backend._ffi.NULL, asn1_time, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(asn1_time[0] != self._backend._ffi.NULL)
        return _parse_asn1_generalized_time(self._backend, asn1_time[0])

    @property
    def revocation_reason(self) -> typing.Optional[x509.ReasonFlags]:
        self._requires_successful_response()
        if self.certificate_status is not OCSPCertStatus.REVOKED:
            return
        reason_ptr = self._backend._ffi.new('int *')
        self._backend._lib.OCSP_single_get0_status(self._single, reason_ptr, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL)
        if reason_ptr[0] == -1:
            return
        self._backend.openssl_assert(reason_ptr[0] in _CRL_ENTRY_REASON_CODE_TO_ENUM)
        return _CRL_ENTRY_REASON_CODE_TO_ENUM[reason_ptr[0]]

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

    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        if encoding is not serialization.Encoding.DER:
            raise ValueError('The only allowed encoding value is Encoding.DER')
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_OCSP_RESPONSE_bio(bio, self._ocsp_response)
        self._backend.openssl_assert(res > 0)
        return self._backend._read_mem_bio(bio)


class _OCSPRequest(OCSPRequest):

    def __init__(self, backend, ocsp_request):
        if backend._lib.OCSP_request_onereq_count(ocsp_request) > 1:
            raise NotImplementedError('OCSP request contains more than one request')
        self._backend = backend
        self._ocsp_request = ocsp_request
        self._request = self._backend._lib.OCSP_request_onereq_get0(self._ocsp_request, 0)
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

    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        if encoding is not serialization.Encoding.DER:
            raise ValueError('The only allowed encoding value is Encoding.DER')
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_OCSP_REQUEST_bio(bio, self._ocsp_request)
        self._backend.openssl_assert(res > 0)
        return self._backend._read_mem_bio(bio)