# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\x509.py
from __future__ import absolute_import, division, print_function
import datetime, operator
from cryptography import utils, x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends.openssl.decode_asn1 import _asn1_integer_to_int, _asn1_string_to_bytes, _decode_x509_name, _obj2txt, _parse_asn1_time
from cryptography.hazmat.backends.openssl.encode_asn1 import _encode_asn1_int_gc, _txt2obj_gc
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa, ec, rsa
from cryptography.x509.name import _ASN1Type

@utils.register_interface(x509.Certificate)
class _Certificate(object):

    def __init__(self, backend, x509_cert):
        self._backend = backend
        self._x509 = x509_cert
        version = self._backend._lib.X509_get_version(self._x509)
        if version == 0:
            self._version = x509.Version.v1
        else:
            if version == 2:
                self._version = x509.Version.v3
            else:
                raise x509.InvalidVersion('{} is not a valid X509 version'.format(version), version)

    def __repr__(self):
        return '<Certificate(subject={}, ...)>'.format(self.subject)

    def __eq__(self, other):
        if not isinstance(other, x509.Certificate):
            return NotImplemented
        res = self._backend._lib.X509_cmp(self._x509, other._x509)
        return res == 0

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.public_bytes(serialization.Encoding.DER))

    def __deepcopy__(self, memo):
        return self

    def fingerprint(self, algorithm):
        h = hashes.Hash(algorithm, self._backend)
        h.update(self.public_bytes(serialization.Encoding.DER))
        return h.finalize()

    version = utils.read_only_property('_version')

    @property
    def serial_number(self):
        asn1_int = self._backend._lib.X509_get_serialNumber(self._x509)
        self._backend.openssl_assert(asn1_int != self._backend._ffi.NULL)
        return _asn1_integer_to_int(self._backend, asn1_int)

    def public_key(self):
        pkey = self._backend._lib.X509_get_pubkey(self._x509)
        if pkey == self._backend._ffi.NULL:
            self._backend._consume_errors()
            raise ValueError('Certificate public key is of an unknown type')
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        return self._backend._evp_pkey_to_public_key(pkey)

    @property
    def not_valid_before(self):
        asn1_time = self._backend._lib.X509_getm_notBefore(self._x509)
        return _parse_asn1_time(self._backend, asn1_time)

    @property
    def not_valid_after(self):
        asn1_time = self._backend._lib.X509_getm_notAfter(self._x509)
        return _parse_asn1_time(self._backend, asn1_time)

    @property
    def issuer(self):
        issuer = self._backend._lib.X509_get_issuer_name(self._x509)
        self._backend.openssl_assert(issuer != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, issuer)

    @property
    def subject(self):
        subject = self._backend._lib.X509_get_subject_name(self._x509)
        self._backend.openssl_assert(subject != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, subject)

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 111         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 112         6  SETUP_FINALLY        20  'to 20'

 L. 113         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 114        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                50  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 115        32  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 116        34  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'oid'
               40  CALL_METHOD_1         1  ''

 L. 115        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 24

    @property
    def signature_algorithm_oid(self):
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_get0_signature(self._backend._ffi.NULL, alg, self._x509)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @utils.cached_property
    def extensions(self):
        return self._backend._certificate_extension_parser.parse(self._x509)

    @property
    def signature(self):
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_get0_signature(sig, self._backend._ffi.NULL, self._x509)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def tbs_certificate_bytes(self):
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_tbs(self._x509, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    def public_bytes--- This code section failed: ---

 L. 153         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_METHOD              _create_mem_bio_gc
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'bio'

 L. 154        10  LOAD_FAST                'encoding'
               12  LOAD_GLOBAL              serialization
               14  LOAD_ATTR                Encoding
               16  LOAD_ATTR                PEM
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L. 155        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _backend
               26  LOAD_ATTR                _lib
               28  LOAD_METHOD              PEM_write_bio_X509
               30  LOAD_FAST                'bio'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _x509
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'res'
               40  JUMP_FORWARD         82  'to 82'
             42_0  COME_FROM            20  '20'

 L. 156        42  LOAD_FAST                'encoding'
               44  LOAD_GLOBAL              serialization
               46  LOAD_ATTR                Encoding
               48  LOAD_ATTR                DER
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L. 157        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _backend
               58  LOAD_ATTR                _lib
               60  LOAD_METHOD              i2d_X509_bio
               62  LOAD_FAST                'bio'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _x509
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'res'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            52  '52'

 L. 159        74  LOAD_GLOBAL              TypeError
               76  LOAD_STR                 'encoding must be an item from the Encoding enum'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            40  '40'

 L. 161        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _backend
               86  LOAD_METHOD              openssl_assert
               88  LOAD_FAST                'res'
               90  LOAD_CONST               1
               92  COMPARE_OP               ==
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 162        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _backend
              102  LOAD_METHOD              _read_mem_bio
              104  LOAD_FAST                'bio'
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18


@utils.register_interface(x509.RevokedCertificate)
class _RevokedCertificate(object):

    def __init__(self, backend, crl, x509_revoked):
        self._backend = backend
        self._crl = crl
        self._x509_revoked = x509_revoked

    @property
    def serial_number(self):
        asn1_int = self._backend._lib.X509_REVOKED_get0_serialNumber(self._x509_revoked)
        self._backend.openssl_assert(asn1_int != self._backend._ffi.NULL)
        return _asn1_integer_to_int(self._backend, asn1_int)

    @property
    def revocation_date(self):
        return _parse_asn1_time(self._backend, self._backend._lib.X509_REVOKED_get0_revocationDate(self._x509_revoked))

    @utils.cached_property
    def extensions(self):
        return self._backend._revoked_cert_extension_parser.parse(self._x509_revoked)


@utils.register_interface(x509.CertificateRevocationList)
class _CertificateRevocationList(object):

    def __init__(self, backend, x509_crl):
        self._backend = backend
        self._x509_crl = x509_crl

    def __eq__(self, other):
        if not isinstance(other, x509.CertificateRevocationList):
            return NotImplemented
        res = self._backend._lib.X509_CRL_cmp(self._x509_crl, other._x509_crl)
        return res == 0

    def __ne__(self, other):
        return not self == other

    def fingerprint(self, algorithm):
        h = hashes.Hash(algorithm, self._backend)
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_X509_CRL_bio(bio, self._x509_crl)
        self._backend.openssl_assert(res == 1)
        der = self._backend._read_mem_bio(bio)
        h.update(der)
        return h.finalize()

    @utils.cached_property
    def _sorted_crl(self):
        dup = self._backend._lib.X509_CRL_dup(self._x509_crl)
        self._backend.openssl_assert(dup != self._backend._ffi.NULL)
        dup = self._backend._ffi.gc(dup, self._backend._lib.X509_CRL_free)
        return dup

    def get_revoked_certificate_by_serial_number(self, serial_number):
        revoked = self._backend._ffi.new('X509_REVOKED **')
        asn1_int = _encode_asn1_int_gc(self._backend, serial_number)
        res = self._backend._lib.X509_CRL_get0_by_serial(self._sorted_crl, revoked, asn1_int)
        if res == 0:
            return
        self._backend.openssl_assert(revoked[0] != self._backend._ffi.NULL)
        return _RevokedCertificate(self._backend, self._sorted_crl, revoked[0])

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 254         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 255         6  SETUP_FINALLY        20  'to 20'

 L. 256         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 257        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                50  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 258        32  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 259        34  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'oid'
               40  CALL_METHOD_1         1  ''

 L. 258        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 24

    @property
    def signature_algorithm_oid(self):
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_CRL_get0_signature(self._x509_crl, self._backend._ffi.NULL, alg)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @property
    def issuer(self):
        issuer = self._backend._lib.X509_CRL_get_issuer(self._x509_crl)
        self._backend.openssl_assert(issuer != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, issuer)

    @property
    def next_update(self):
        nu = self._backend._lib.X509_CRL_get_nextUpdate(self._x509_crl)
        self._backend.openssl_assert(nu != self._backend._ffi.NULL)
        return _parse_asn1_time(self._backend, nu)

    @property
    def last_update(self):
        lu = self._backend._lib.X509_CRL_get_lastUpdate(self._x509_crl)
        self._backend.openssl_assert(lu != self._backend._ffi.NULL)
        return _parse_asn1_time(self._backend, lu)

    @property
    def signature(self):
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_CRL_get0_signature(self._x509_crl, sig, self._backend._ffi.NULL)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def tbs_certlist_bytes(self):
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_CRL_tbs(self._x509_crl, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    def public_bytes--- This code section failed: ---

 L. 310         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_METHOD              _create_mem_bio_gc
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'bio'

 L. 311        10  LOAD_FAST                'encoding'
               12  LOAD_GLOBAL              serialization
               14  LOAD_ATTR                Encoding
               16  LOAD_ATTR                PEM
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L. 312        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _backend
               26  LOAD_ATTR                _lib
               28  LOAD_METHOD              PEM_write_bio_X509_CRL

 L. 313        30  LOAD_FAST                'bio'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _x509_crl

 L. 312        36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'res'
               40  JUMP_FORWARD         82  'to 82'
             42_0  COME_FROM            20  '20'

 L. 315        42  LOAD_FAST                'encoding'
               44  LOAD_GLOBAL              serialization
               46  LOAD_ATTR                Encoding
               48  LOAD_ATTR                DER
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L. 316        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _backend
               58  LOAD_ATTR                _lib
               60  LOAD_METHOD              i2d_X509_CRL_bio
               62  LOAD_FAST                'bio'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _x509_crl
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'res'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            52  '52'

 L. 318        74  LOAD_GLOBAL              TypeError
               76  LOAD_STR                 'encoding must be an item from the Encoding enum'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            40  '40'

 L. 320        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _backend
               86  LOAD_METHOD              openssl_assert
               88  LOAD_FAST                'res'
               90  LOAD_CONST               1
               92  COMPARE_OP               ==
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 321        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _backend
              102  LOAD_METHOD              _read_mem_bio
              104  LOAD_FAST                'bio'
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

    def _revoked_cert(self, idx):
        revoked = self._backend._lib.X509_CRL_get_REVOKED(self._x509_crl)
        r = self._backend._lib.sk_X509_REVOKED_value(revoked, idx)
        self._backend.openssl_assert(r != self._backend._ffi.NULL)
        return _RevokedCertificate(self._backend, self, r)

    def __iter__(self):
        for i in range(len(self)):
            (yield self._revoked_cert(i))

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))
            return [self._revoked_cert(i) for i in range(start, stop, step)]
        else:
            idx = operator.index(idx)
            if idx < 0:
                idx += len(self)
            assert 0 <= idx < len(self)
        return self._revoked_cert(idx)

    def __len__(self):
        revoked = self._backend._lib.X509_CRL_get_REVOKED(self._x509_crl)
        if revoked == self._backend._ffi.NULL:
            return 0
        return self._backend._lib.sk_X509_REVOKED_num(revoked)

    @utils.cached_property
    def extensions(self):
        return self._backend._crl_extension_parser.parse(self._x509_crl)

    def is_signature_valid(self, public_key):
        if not isinstance(public_key, (
         dsa.DSAPublicKey, rsa.RSAPublicKey, ec.EllipticCurvePublicKey)):
            raise TypeError('Expecting one of DSAPublicKey, RSAPublicKey, or EllipticCurvePublicKey.')
        res = self._backend._lib.X509_CRL_verify(self._x509_crl, public_key._evp_pkey)
        if res != 1:
            self._backend._consume_errors()
            return False
        return True


@utils.register_interface(x509.CertificateSigningRequest)
class _CertificateSigningRequest(object):

    def __init__(self, backend, x509_req):
        self._backend = backend
        self._x509_req = x509_req

    def __eq__(self, other):
        if not isinstance(other, _CertificateSigningRequest):
            return NotImplemented
        self_bytes = self.public_bytes(serialization.Encoding.DER)
        other_bytes = other.public_bytes(serialization.Encoding.DER)
        return self_bytes == other_bytes

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.public_bytes(serialization.Encoding.DER))

    def public_key(self):
        pkey = self._backend._lib.X509_REQ_get_pubkey(self._x509_req)
        self._backend.openssl_assert(pkey != self._backend._ffi.NULL)
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        return self._backend._evp_pkey_to_public_key(pkey)

    @property
    def subject(self):
        subject = self._backend._lib.X509_REQ_get_subject_name(self._x509_req)
        self._backend.openssl_assert(subject != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, subject)

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 410         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 411         6  SETUP_FINALLY        20  'to 20'

 L. 412         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 413        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                50  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 414        32  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 415        34  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'oid'
               40  CALL_METHOD_1         1  ''

 L. 414        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 24

    @property
    def signature_algorithm_oid(self):
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_REQ_get0_signature(self._x509_req, self._backend._ffi.NULL, alg)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @utils.cached_property
    def extensions(self):
        x509_exts = self._backend._lib.X509_REQ_get_extensions(self._x509_req)
        x509_exts = self._backend._ffi.gc(x509_exts, lambda x: self._backend._lib.sk_X509_EXTENSION_pop_free(x, self._backend._ffi.addressof(self._backend._lib._original_lib, 'X509_EXTENSION_free')))
        return self._backend._csr_extension_parser.parse(x509_exts)

    def public_bytes--- This code section failed: ---

 L. 443         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_METHOD              _create_mem_bio_gc
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'bio'

 L. 444        10  LOAD_FAST                'encoding'
               12  LOAD_GLOBAL              serialization
               14  LOAD_ATTR                Encoding
               16  LOAD_ATTR                PEM
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L. 445        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _backend
               26  LOAD_ATTR                _lib
               28  LOAD_METHOD              PEM_write_bio_X509_REQ

 L. 446        30  LOAD_FAST                'bio'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _x509_req

 L. 445        36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'res'
               40  JUMP_FORWARD         82  'to 82'
             42_0  COME_FROM            20  '20'

 L. 448        42  LOAD_FAST                'encoding'
               44  LOAD_GLOBAL              serialization
               46  LOAD_ATTR                Encoding
               48  LOAD_ATTR                DER
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L. 449        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _backend
               58  LOAD_ATTR                _lib
               60  LOAD_METHOD              i2d_X509_REQ_bio
               62  LOAD_FAST                'bio'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _x509_req
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'res'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            52  '52'

 L. 451        74  LOAD_GLOBAL              TypeError
               76  LOAD_STR                 'encoding must be an item from the Encoding enum'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            40  '40'

 L. 453        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _backend
               86  LOAD_METHOD              openssl_assert
               88  LOAD_FAST                'res'
               90  LOAD_CONST               1
               92  COMPARE_OP               ==
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 454        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _backend
              102  LOAD_METHOD              _read_mem_bio
              104  LOAD_FAST                'bio'
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

    @property
    def tbs_certrequest_bytes(self):
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_REQ_tbs(self._x509_req, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    @property
    def signature(self):
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_REQ_get0_signature(self._x509_req, sig, self._backend._ffi.NULL)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def is_signature_valid(self):
        pkey = self._backend._lib.X509_REQ_get_pubkey(self._x509_req)
        self._backend.openssl_assert(pkey != self._backend._ffi.NULL)
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        res = self._backend._lib.X509_REQ_verify(self._x509_req, pkey)
        if res != 1:
            self._backend._consume_errors()
            return False
        return True

    def get_attribute_for_oid--- This code section failed: ---

 L. 489         0  LOAD_GLOBAL              _txt2obj_gc
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _backend
                6  LOAD_FAST                'oid'
                8  LOAD_ATTR                dotted_string
               10  CALL_FUNCTION_2       2  ''
               12  STORE_FAST               'obj'

 L. 490        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _backend
               18  LOAD_ATTR                _lib
               20  LOAD_METHOD              X509_REQ_get_attr_by_OBJ

 L. 491        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _x509_req
               26  LOAD_FAST                'obj'
               28  LOAD_CONST               -1

 L. 490        30  CALL_METHOD_3         3  ''
               32  STORE_FAST               'pos'

 L. 493        34  LOAD_FAST                'pos'
               36  LOAD_CONST               -1
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    60  'to 60'

 L. 494        42  LOAD_GLOBAL              x509
               44  LOAD_METHOD              AttributeNotFound

 L. 495        46  LOAD_STR                 'No {} attribute was found'
               48  LOAD_METHOD              format
               50  LOAD_FAST                'oid'
               52  CALL_METHOD_1         1  ''
               54  LOAD_FAST                'oid'

 L. 494        56  CALL_METHOD_2         2  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            40  '40'

 L. 498        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _backend
               64  LOAD_ATTR                _lib
               66  LOAD_METHOD              X509_REQ_get_attr
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _x509_req
               72  LOAD_FAST                'pos'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'attr'

 L. 499        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _backend
               82  LOAD_METHOD              openssl_assert
               84  LOAD_FAST                'attr'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _backend
               90  LOAD_ATTR                _ffi
               92  LOAD_ATTR                NULL
               94  COMPARE_OP               !=
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 501       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _backend
              104  LOAD_METHOD              openssl_assert

 L. 502       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _backend
              110  LOAD_ATTR                _lib
              112  LOAD_METHOD              X509_ATTRIBUTE_count
              114  LOAD_FAST                'attr'
              116  CALL_METHOD_1         1  ''
              118  LOAD_CONST               1
              120  COMPARE_OP               ==

 L. 501       122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 504       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _backend
              130  LOAD_ATTR                _lib
              132  LOAD_METHOD              X509_ATTRIBUTE_get0_type
              134  LOAD_FAST                'attr'
              136  LOAD_CONST               0
              138  CALL_METHOD_2         2  ''
              140  STORE_FAST               'asn1_type'

 L. 505       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _backend
              146  LOAD_METHOD              openssl_assert
              148  LOAD_FAST                'asn1_type'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _backend
              154  LOAD_ATTR                _ffi
              156  LOAD_ATTR                NULL
              158  COMPARE_OP               !=
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 509       164  LOAD_FAST                'asn1_type'
              166  LOAD_ATTR                type

 L. 510       168  LOAD_GLOBAL              _ASN1Type
              170  LOAD_ATTR                UTF8String
              172  LOAD_ATTR                value

 L. 511       174  LOAD_GLOBAL              _ASN1Type
              176  LOAD_ATTR                PrintableString
              178  LOAD_ATTR                value

 L. 512       180  LOAD_GLOBAL              _ASN1Type
              182  LOAD_ATTR                IA5String
              184  LOAD_ATTR                value

 L. 509       186  BUILD_TUPLE_3         3 
              188  <118>                 1  ''
              190  POP_JUMP_IF_FALSE   210  'to 210'

 L. 514       192  LOAD_GLOBAL              ValueError

 L. 515       194  LOAD_STR                 'OID {} has a disallowed ASN.1 type: {}'
              196  LOAD_METHOD              format

 L. 516       198  LOAD_FAST                'oid'
              200  LOAD_FAST                'asn1_type'
              202  LOAD_ATTR                type

 L. 515       204  CALL_METHOD_2         2  ''

 L. 514       206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           190  '190'

 L. 520       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _backend
              214  LOAD_ATTR                _lib
              216  LOAD_METHOD              X509_ATTRIBUTE_get0_data

 L. 521       218  LOAD_FAST                'attr'
              220  LOAD_CONST               0
              222  LOAD_FAST                'asn1_type'
              224  LOAD_ATTR                type
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                _backend
              230  LOAD_ATTR                _ffi
              232  LOAD_ATTR                NULL

 L. 520       234  CALL_METHOD_4         4  ''
              236  STORE_FAST               'data'

 L. 523       238  LOAD_FAST                'self'
              240  LOAD_ATTR                _backend
              242  LOAD_METHOD              openssl_assert
              244  LOAD_FAST                'data'
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                _backend
              250  LOAD_ATTR                _ffi
              252  LOAD_ATTR                NULL
              254  COMPARE_OP               !=
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 526       260  LOAD_FAST                'self'
              262  LOAD_ATTR                _backend
              264  LOAD_ATTR                _ffi
              266  LOAD_METHOD              cast
              268  LOAD_STR                 'ASN1_STRING *'
              270  LOAD_FAST                'data'
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'data'

 L. 527       276  LOAD_GLOBAL              _asn1_string_to_bytes
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                _backend
              282  LOAD_FAST                'data'
              284  CALL_FUNCTION_2       2  ''
              286  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 188


@utils.register_interface(x509.certificate_transparency.SignedCertificateTimestamp)
class _SignedCertificateTimestamp(object):

    def __init__(self, backend, sct_list, sct):
        self._backend = backend
        self._sct_list = sct_list
        self._sct = sct

    @property
    def version--- This code section failed: ---

 L. 542         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_ATTR                _lib
                6  LOAD_METHOD              SCT_get_version
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _sct
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'version'

 L. 543        16  LOAD_FAST                'version'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _backend
               22  LOAD_ATTR                _lib
               24  LOAD_ATTR                SCT_VERSION_V1
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  <74>             
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L. 544        34  LOAD_GLOBAL              x509
               36  LOAD_ATTR                certificate_transparency
               38  LOAD_ATTR                Version
               40  LOAD_ATTR                v1
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 30

    @property
    def log_id--- This code section failed: ---

 L. 548         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_ATTR                _ffi
                6  LOAD_METHOD              new
                8  LOAD_STR                 'unsigned char **'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'out'

 L. 549        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _backend
               18  LOAD_ATTR                _lib
               20  LOAD_METHOD              SCT_get0_log_id
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _sct
               26  LOAD_FAST                'out'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'log_id_length'

 L. 550        32  LOAD_FAST                'log_id_length'
               34  LOAD_CONST               0
               36  COMPARE_OP               >=
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  <74>             
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 551        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _ffi
               50  LOAD_METHOD              buffer
               52  LOAD_FAST                'out'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'log_id_length'
               60  CALL_METHOD_2         2  ''
               62  LOAD_CONST               None
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 40

    @property
    def timestamp(self):
        timestamp = self._backend._lib.SCT_get_timestamp(self._sct)
        milliseconds = timestamp % 1000
        return datetime.datetime.utcfromtimestamp(timestamp // 1000).replace(microsecond=(milliseconds * 1000))

    @property
    def entry_type--- This code section failed: ---

 L. 563         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_ATTR                _lib
                6  LOAD_METHOD              SCT_get_log_entry_type
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _sct
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'entry_type'

 L. 566        16  LOAD_FAST                'entry_type'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _backend
               22  LOAD_ATTR                _lib
               24  LOAD_ATTR                CT_LOG_ENTRY_TYPE_PRECERT
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  <74>             
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L. 567        34  LOAD_GLOBAL              x509
               36  LOAD_ATTR                certificate_transparency
               38  LOAD_ATTR                LogEntryType
               40  LOAD_ATTR                PRE_CERTIFICATE
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 30

    @property
    def _signature(self):
        ptrptr = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.SCT_get0_signature(self._sct, ptrptr)
        self._backend.openssl_assert(res > 0)
        self._backend.openssl_assert(ptrptr[0] != self._backend._ffi.NULL)
        return self._backend._ffi.buffer(ptrptr[0], res)[:]

    def __hash__(self):
        return hash(self._signature)

    def __eq__(self, other):
        if not isinstance(other, _SignedCertificateTimestamp):
            return NotImplemented
        return self._signature == other._signature

    def __ne__(self, other):
        return not self == other