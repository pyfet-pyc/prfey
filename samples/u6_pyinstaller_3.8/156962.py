# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\x509.py
import datetime, operator, typing
from cryptography import utils, x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends.openssl import dsa, ec, rsa
from cryptography.hazmat.backends.openssl.decode_asn1 import _asn1_integer_to_int, _asn1_string_to_bytes, _decode_x509_name, _obj2txt, _parse_asn1_time
from cryptography.hazmat.backends.openssl.encode_asn1 import _encode_asn1_int_gc, _txt2obj_gc
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.base import _PUBLIC_KEY_TYPES
from cryptography.x509.name import _ASN1Type

class _Certificate(x509.Certificate):
    _ocsp_resp_ref: typing.Any

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Certificate):
            return NotImplemented
        res = self._backend._lib.X509_cmp(self._x509, other._x509)
        return res == 0

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.public_bytes(serialization.Encoding.DER))

    def __deepcopy__(self, memo):
        return self

    def fingerprint(self, algorithm: hashes.HashAlgorithm) -> bytes:
        h = hashes.Hash(algorithm, self._backend)
        h.update(self.public_bytes(serialization.Encoding.DER))
        return h.finalize()

    version = utils.read_only_property('_version')

    @property
    def serial_number(self) -> int:
        asn1_int = self._backend._lib.X509_get_serialNumber(self._x509)
        self._backend.openssl_assert(asn1_int != self._backend._ffi.NULL)
        return _asn1_integer_to_int(self._backend, asn1_int)

    def public_key(self) -> _PUBLIC_KEY_TYPES:
        pkey = self._backend._lib.X509_get_pubkey(self._x509)
        if pkey == self._backend._ffi.NULL:
            self._backend._consume_errors()
            raise ValueError('Certificate public key is of an unknown type')
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        return self._backend._evp_pkey_to_public_key(pkey)

    @property
    def not_valid_before(self) -> datetime.datetime:
        asn1_time = self._backend._lib.X509_get0_notBefore(self._x509)
        return _parse_asn1_time(self._backend, asn1_time)

    @property
    def not_valid_after(self) -> datetime.datetime:
        asn1_time = self._backend._lib.X509_get0_notAfter(self._x509)
        return _parse_asn1_time(self._backend, asn1_time)

    @property
    def issuer(self) -> x509.Name:
        issuer = self._backend._lib.X509_get_issuer_name(self._x509)
        self._backend.openssl_assert(issuer != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, issuer)

    @property
    def subject(self) -> x509.Name:
        subject = self._backend._lib.X509_get_subject_name(self._x509)
        self._backend.openssl_assert(subject != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, subject)

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 116         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 117         6  SETUP_FINALLY        20  'to 20'

 L. 118         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 119        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 120        34  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 121        36  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               38  LOAD_METHOD              format
               40  LOAD_FAST                'oid'
               42  CALL_METHOD_1         1  ''

 L. 120        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            26  '26'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 30

    @property
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_get0_signature(self._backend._ffi.NULL, alg, self._x509)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        return self._backend._certificate_extension_parser.parse(self._x509)

    @property
    def signature(self) -> bytes:
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_get0_signature(sig, self._backend._ffi.NULL, self._x509)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def tbs_certificate_bytes(self) -> bytes:
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_tbs(self._x509, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        bio = self._backend._create_mem_bio_gc()
        if encoding is serialization.Encoding.PEM:
            res = self._backend._lib.PEM_write_bio_X509(bio, self._x509)
        else:
            if encoding is serialization.Encoding.DER:
                res = self._backend._lib.i2d_X509_bio(bio, self._x509)
            else:
                raise TypeError('encoding must be an item from the Encoding enum')
        self._backend.openssl_assert(res == 1)
        return self._backend._read_mem_bio(bio)


class _RevokedCertificate(x509.RevokedCertificate):

    def __init__(self, backend, crl, x509_revoked):
        self._backend = backend
        self._crl = crl
        self._x509_revoked = x509_revoked

    @property
    def serial_number(self) -> int:
        asn1_int = self._backend._lib.X509_REVOKED_get0_serialNumber(self._x509_revoked)
        self._backend.openssl_assert(asn1_int != self._backend._ffi.NULL)
        return _asn1_integer_to_int(self._backend, asn1_int)

    @property
    def revocation_date(self) -> datetime.datetime:
        return _parse_asn1_time(self._backend, self._backend._lib.X509_REVOKED_get0_revocationDate(self._x509_revoked))

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        return self._backend._revoked_cert_extension_parser.parse(self._x509_revoked)


@utils.register_interface(x509.CertificateRevocationList)
class _CertificateRevocationList(object):

    def __init__(self, backend, x509_crl):
        self._backend = backend
        self._x509_crl = x509_crl

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _CertificateRevocationList):
            return NotImplemented
        res = self._backend._lib.X509_CRL_cmp(self._x509_crl, other._x509_crl)
        return res == 0

    def __ne__(self, other: object) -> bool:
        return not self == other

    def fingerprint(self, algorithm: hashes.HashAlgorithm) -> bytes:
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

    def get_revoked_certificate_by_serial_number(self, serial_number: int) -> typing.Optional[x509.RevokedCertificate]:
        revoked = self._backend._ffi.new('X509_REVOKED **')
        asn1_int = _encode_asn1_int_gc(self._backend, serial_number)
        res = self._backend._lib.X509_CRL_get0_by_serial(self._sorted_crl, revoked, asn1_int)
        if res == 0:
            return
        self._backend.openssl_assert(revoked[0] != self._backend._ffi.NULL)
        return _RevokedCertificate(self._backend, self._sorted_crl, revoked[0])

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 262         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 263         6  SETUP_FINALLY        20  'to 20'

 L. 264         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 265        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 266        34  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 267        36  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               38  LOAD_METHOD              format
               40  LOAD_FAST                'oid'
               42  CALL_METHOD_1         1  ''

 L. 266        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            26  '26'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 30

    @property
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_CRL_get0_signature(self._x509_crl, self._backend._ffi.NULL, alg)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @property
    def issuer(self) -> x509.Name:
        issuer = self._backend._lib.X509_CRL_get_issuer(self._x509_crl)
        self._backend.openssl_assert(issuer != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, issuer)

    @property
    def next_update(self) -> datetime.datetime:
        nu = self._backend._lib.X509_CRL_get0_nextUpdate(self._x509_crl)
        self._backend.openssl_assert(nu != self._backend._ffi.NULL)
        return _parse_asn1_time(self._backend, nu)

    @property
    def last_update(self) -> datetime.datetime:
        lu = self._backend._lib.X509_CRL_get0_lastUpdate(self._x509_crl)
        self._backend.openssl_assert(lu != self._backend._ffi.NULL)
        return _parse_asn1_time(self._backend, lu)

    @property
    def signature(self) -> bytes:
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_CRL_get0_signature(self._x509_crl, sig, self._backend._ffi.NULL)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def tbs_certlist_bytes(self) -> bytes:
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_CRL_tbs(self._x509_crl, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        bio = self._backend._create_mem_bio_gc()
        if encoding is serialization.Encoding.PEM:
            res = self._backend._lib.PEM_write_bio_X509_CRL(bio, self._x509_crl)
        else:
            if encoding is serialization.Encoding.DER:
                res = self._backend._lib.i2d_X509_CRL_bio(bio, self._x509_crl)
            else:
                raise TypeError('encoding must be an item from the Encoding enum')
        self._backend.openssl_assert(res == 1)
        return self._backend._read_mem_bio(bio)

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

    def __len__(self) -> int:
        revoked = self._backend._lib.X509_CRL_get_REVOKED(self._x509_crl)
        if revoked == self._backend._ffi.NULL:
            return 0
        return self._backend._lib.sk_X509_REVOKED_num(revoked)

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        return self._backend._crl_extension_parser.parse(self._x509_crl)

    def is_signature_valid(self, public_key: _PUBLIC_KEY_TYPES) -> bool:
        if not isinstance(public_key, (
         dsa._DSAPublicKey,
         rsa._RSAPublicKey,
         ec._EllipticCurvePublicKey)):
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _CertificateSigningRequest):
            return NotImplemented
        self_bytes = self.public_bytes(serialization.Encoding.DER)
        other_bytes = other.public_bytes(serialization.Encoding.DER)
        return self_bytes == other_bytes

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.public_bytes(serialization.Encoding.DER))

    def public_key(self) -> _PUBLIC_KEY_TYPES:
        pkey = self._backend._lib.X509_REQ_get_pubkey(self._x509_req)
        self._backend.openssl_assert(pkey != self._backend._ffi.NULL)
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        return self._backend._evp_pkey_to_public_key(pkey)

    @property
    def subject(self) -> x509.Name:
        subject = self._backend._lib.X509_REQ_get_subject_name(self._x509_req)
        self._backend.openssl_assert(subject != self._backend._ffi.NULL)
        return _decode_x509_name(self._backend, subject)

    @property
    def signature_hash_algorithm--- This code section failed: ---

 L. 424         0  LOAD_FAST                'self'
                2  LOAD_ATTR                signature_algorithm_oid
                4  STORE_FAST               'oid'

 L. 425         6  SETUP_FINALLY        20  'to 20'

 L. 426         8  LOAD_GLOBAL              x509
               10  LOAD_ATTR                _SIG_OIDS_TO_HASH
               12  LOAD_FAST                'oid'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     6  '6'

 L. 427        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    52  'to 52'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 428        34  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 429        36  LOAD_STR                 'Signature algorithm OID:{} not recognized'
               38  LOAD_METHOD              format
               40  LOAD_FAST                'oid'
               42  CALL_METHOD_1         1  ''

 L. 428        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            26  '26'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 30

    @property
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        alg = self._backend._ffi.new('X509_ALGOR **')
        self._backend._lib.X509_REQ_get0_signature(self._x509_req, self._backend._ffi.NULL, alg)
        self._backend.openssl_assert(alg[0] != self._backend._ffi.NULL)
        oid = _obj2txt(self._backend, alg[0].algorithm)
        return x509.ObjectIdentifier(oid)

    @utils.cached_property
    def extensions(self) -> x509.Extensions:
        x509_exts = self._backend._lib.X509_REQ_get_extensions(self._x509_req)
        x509_exts = self._backend._ffi.gc(x509_exts, lambda x: self._backend._lib.sk_X509_EXTENSION_pop_free(x, self._backend._ffi.addressof(self._backend._lib._original_lib, 'X509_EXTENSION_free')))
        return self._backend._csr_extension_parser.parse(x509_exts)

    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        bio = self._backend._create_mem_bio_gc()
        if encoding is serialization.Encoding.PEM:
            res = self._backend._lib.PEM_write_bio_X509_REQ(bio, self._x509_req)
        else:
            if encoding is serialization.Encoding.DER:
                res = self._backend._lib.i2d_X509_REQ_bio(bio, self._x509_req)
            else:
                raise TypeError('encoding must be an item from the Encoding enum')
        self._backend.openssl_assert(res == 1)
        return self._backend._read_mem_bio(bio)

    @property
    def tbs_certrequest_bytes(self) -> bytes:
        pp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.i2d_re_X509_REQ_tbs(self._x509_req, pp)
        self._backend.openssl_assert(res > 0)
        pp = self._backend._ffi.gc(pp, lambda pointer: self._backend._lib.OPENSSL_free(pointer[0]))
        return self._backend._ffi.buffer(pp[0], res)[:]

    @property
    def signature(self) -> bytes:
        sig = self._backend._ffi.new('ASN1_BIT_STRING **')
        self._backend._lib.X509_REQ_get0_signature(self._x509_req, sig, self._backend._ffi.NULL)
        self._backend.openssl_assert(sig[0] != self._backend._ffi.NULL)
        return _asn1_string_to_bytes(self._backend, sig[0])

    @property
    def is_signature_valid(self) -> bool:
        pkey = self._backend._lib.X509_REQ_get_pubkey(self._x509_req)
        self._backend.openssl_assert(pkey != self._backend._ffi.NULL)
        pkey = self._backend._ffi.gc(pkey, self._backend._lib.EVP_PKEY_free)
        res = self._backend._lib.X509_REQ_verify(self._x509_req, pkey)
        if res != 1:
            self._backend._consume_errors()
            return False
        return True

    def get_attribute_for_oid(self, oid: x509.ObjectIdentifier) -> bytes:
        obj = _txt2obj_gc(self._backend, oid.dotted_string)
        pos = self._backend._lib.X509_REQ_get_attr_by_OBJ(self._x509_req, obj, -1)
        if pos == -1:
            raise x509.AttributeNotFound('No {} attribute was found'.format(oid), oid)
        attr = self._backend._lib.X509_REQ_get_attr(self._x509_req, pos)
        self._backend.openssl_assert(attr != self._backend._ffi.NULL)
        self._backend.openssl_assert(self._backend._lib.X509_ATTRIBUTE_count(attr) == 1)
        asn1_type = self._backend._lib.X509_ATTRIBUTE_get0_type(attr, 0)
        self._backend.openssl_assert(asn1_type != self._backend._ffi.NULL)
        if asn1_type.type not in (
         _ASN1Type.UTF8String.value,
         _ASN1Type.PrintableString.value,
         _ASN1Type.IA5String.value):
            raise ValueError('OID {} has a disallowed ASN.1 type: {}'.format(oid, asn1_type.type))
        data = self._backend._lib.X509_ATTRIBUTE_get0_data(attr, 0, asn1_type.type, self._backend._ffi.NULL)
        self._backend.openssl_assert(data != self._backend._ffi.NULL)
        data = self._backend._ffi.cast('ASN1_STRING *', data)
        return _asn1_string_to_bytes(self._backend, data)


@utils.register_interface(x509.certificate_transparency.SignedCertificateTimestamp)
class _SignedCertificateTimestamp(object):

    def __init__(self, backend, sct_list, sct):
        self._backend = backend
        self._sct_list = sct_list
        self._sct = sct

    @property
    def version(self) -> x509.certificate_transparency.Version:
        version = self._backend._lib.SCT_get_version(self._sct)
        assert version == self._backend._lib.SCT_VERSION_V1
        return x509.certificate_transparency.Version.v1

    @property
    def log_id(self) -> bytes:
        out = self._backend._ffi.new('unsigned char **')
        log_id_length = self._backend._lib.SCT_get0_log_id(self._sct, out)
        assert log_id_length >= 0
        return self._backend._ffi.buffer(out[0], log_id_length)[:]

    @property
    def timestamp(self) -> datetime.datetime:
        timestamp = self._backend._lib.SCT_get_timestamp(self._sct)
        milliseconds = timestamp % 1000
        return datetime.datetime.utcfromtimestamp(timestamp // 1000).replace(microsecond=(milliseconds * 1000))

    @property
    def entry_type(self) -> x509.certificate_transparency.LogEntryType:
        entry_type = self._backend._lib.SCT_get_log_entry_type(self._sct)
        assert entry_type == self._backend._lib.CT_LOG_ENTRY_TYPE_PRECERT
        return x509.certificate_transparency.LogEntryType.PRE_CERTIFICATE

    @property
    def _signature(self):
        ptrptr = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.SCT_get0_signature(self._sct, ptrptr)
        self._backend.openssl_assert(res > 0)
        self._backend.openssl_assert(ptrptr[0] != self._backend._ffi.NULL)
        return self._backend._ffi.buffer(ptrptr[0], res)[:]

    def __hash__(self) -> int:
        return hash(self._signature)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _SignedCertificateTimestamp):
            return NotImplemented
        return self._signature == other._signature

    def __ne__(self, other: object) -> bool:
        return not self == other