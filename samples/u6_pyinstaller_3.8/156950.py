# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\ec.py
from cryptography import utils
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.openssl.utils import _calculate_digest_and_algorithm, _check_not_prehashed, _warn_sign_verify_deprecated
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, ec

def _check_signature_algorithm(signature_algorithm: ec.EllipticCurveSignatureAlgorithm):
    if not isinstance(signature_algorithm, ec.ECDSA):
        raise UnsupportedAlgorithm('Unsupported elliptic curve signature algorithm.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)


def _ec_key_curve_sn(backend, ec_key):
    group = backend._lib.EC_KEY_get0_group(ec_key)
    backend.openssl_assert(group != backend._ffi.NULL)
    nid = backend._lib.EC_GROUP_get_curve_name(group)
    if nid == backend._lib.NID_undef:
        raise NotImplementedError('ECDSA keys with unnamed curves are unsupported at this time')
    if not backend._lib.CRYPTOGRAPHY_IS_LIBRESSL:
        if backend._lib.EC_GROUP_get_asn1_flag(group) == 0:
            raise NotImplementedError('ECDSA keys with unnamed curves are unsupported at this time')
    curve_name = backend._lib.OBJ_nid2sn(nid)
    backend.openssl_assert(curve_name != backend._ffi.NULL)
    sn = backend._ffi.string(curve_name).decode('ascii')
    return sn


def _mark_asn1_named_ec_curve(backend, ec_cdata):
    """
    Set the named curve flag on the EC_KEY. This causes OpenSSL to
    serialize EC keys along with their curve OID which makes
    deserialization easier.
    """
    backend._lib.EC_KEY_set_asn1_flag(ec_cdata, backend._lib.OPENSSL_EC_NAMED_CURVE)


def _sn_to_elliptic_curve--- This code section failed: ---

 L.  78         0  SETUP_FINALLY        16  'to 16'

 L.  79         2  LOAD_GLOBAL              ec
                4  LOAD_ATTR                _CURVE_TYPES
                6  LOAD_FAST                'sn'
                8  BINARY_SUBSCR    
               10  CALL_FUNCTION_0       0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  80        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    52  'to 52'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  81        30  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  82        32  LOAD_STR                 '{} is not a supported elliptic curve'
               34  LOAD_METHOD              format
               36  LOAD_FAST                'sn'
               38  CALL_METHOD_1         1  ''

 L.  83        40  LOAD_GLOBAL              _Reasons
               42  LOAD_ATTR                UNSUPPORTED_ELLIPTIC_CURVE

 L.  81        44  CALL_FUNCTION_2       2  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            22  '22'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 26


def _ecdsa_sig_sign(backend, private_key, data):
    max_size = backend._lib.ECDSA_size(private_key._ec_key)
    backend.openssl_assert(max_size > 0)
    sigbuf = backend._ffi.new('unsigned char[]', max_size)
    siglen_ptr = backend._ffi.new('unsigned int[]', 1)
    res = backend._lib.ECDSA_sign(0, data, len(data), sigbuf, siglen_ptr, private_key._ec_key)
    backend.openssl_assert(res == 1)
    return backend._ffi.buffer(sigbuf)[:siglen_ptr[0]]


def _ecdsa_sig_verify(backend, public_key, signature, data):
    res = backend._lib.ECDSA_verify(0, data, len(data), signature, len(signature), public_key._ec_key)
    if res != 1:
        backend._consume_errors()
        raise InvalidSignature


class _ECDSASignatureContext(AsymmetricSignatureContext):

    def __init__(self, backend, private_key: ec.EllipticCurvePrivateKey, algorithm: hashes.HashAlgorithm):
        self._backend = backend
        self._private_key = private_key
        self._digest = hashes.Hash(algorithm, backend)

    def update(self, data: bytes) -> None:
        self._digest.update(data)

    def finalize(self) -> bytes:
        digest = self._digest.finalize()
        return _ecdsa_sig_sign(self._backend, self._private_key, digest)


class _ECDSAVerificationContext(AsymmetricVerificationContext):

    def __init__(self, backend, public_key: ec.EllipticCurvePublicKey, signature: bytes, algorithm: hashes.HashAlgorithm):
        self._backend = backend
        self._public_key = public_key
        self._signature = signature
        self._digest = hashes.Hash(algorithm, backend)

    def update(self, data: bytes) -> None:
        self._digest.update(data)

    def verify(self) -> None:
        digest = self._digest.finalize()
        _ecdsa_sig_verify(self._backend, self._public_key, self._signature, digest)


class _EllipticCurvePrivateKey(ec.EllipticCurvePrivateKey):

    def __init__(self, backend, ec_key_cdata, evp_pkey):
        self._backend = backend
        self._ec_key = ec_key_cdata
        self._evp_pkey = evp_pkey
        sn = _ec_key_curve_sn(backend, ec_key_cdata)
        self._curve = _sn_to_elliptic_curve(backend, sn)
        _mark_asn1_named_ec_curve(backend, ec_key_cdata)

    curve = utils.read_only_property('_curve')

    @property
    def key_size(self) -> int:
        return self.curve.key_size

    def signer(self, signature_algorithm: ec.EllipticCurveSignatureAlgorithm) -> AsymmetricSignatureContext:
        _warn_sign_verify_deprecated
        _check_signature_algorithm(signature_algorithm)
        _check_not_prehashed(signature_algorithm.algorithm)
        assert isinstance(signature_algorithm.algorithm, hashes.HashAlgorithm)
        return _ECDSASignatureContext(self._backend, self, signature_algorithm.algorithm)

    def exchange(self, algorithm: ec.ECDH, peer_public_key: ec.EllipticCurvePublicKey) -> bytes:
        if not self._backend.elliptic_curve_exchange_algorithm_supported(algorithm, self.curve):
            raise UnsupportedAlgorithm('This backend does not support the ECDH algorithm.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        if peer_public_key.curve.name != self.curve.name:
            raise ValueError('peer_public_key and self are not on the same curve')
        group = self._backend._lib.EC_KEY_get0_group(self._ec_key)
        z_len = (self._backend._lib.EC_GROUP_get_degree(group) + 7) // 8
        self._backend.openssl_assert(z_len > 0)
        z_buf = self._backend._ffi.new('uint8_t[]', z_len)
        peer_key = self._backend._lib.EC_KEY_get0_public_key(peer_public_key._ec_key)
        r = self._backend._lib.ECDH_compute_key(z_buf, z_len, peer_key, self._ec_key, self._backend._ffi.NULL)
        self._backend.openssl_assert(r > 0)
        return self._backend._ffi.buffer(z_buf)[:z_len]

    def public_key(self) -> ec.EllipticCurvePublicKey:
        group = self._backend._lib.EC_KEY_get0_group(self._ec_key)
        self._backend.openssl_assert(group != self._backend._ffi.NULL)
        curve_nid = self._backend._lib.EC_GROUP_get_curve_name(group)
        public_ec_key = self._backend._ec_key_new_by_curve_nid(curve_nid)
        point = self._backend._lib.EC_KEY_get0_public_key(self._ec_key)
        self._backend.openssl_assert(point != self._backend._ffi.NULL)
        res = self._backend._lib.EC_KEY_set_public_key(public_ec_key, point)
        self._backend.openssl_assert(res == 1)
        evp_pkey = self._backend._ec_cdata_to_evp_pkey(public_ec_key)
        return _EllipticCurvePublicKey(self._backend, public_ec_key, evp_pkey)

    def private_numbers(self) -> ec.EllipticCurvePrivateNumbers:
        bn = self._backend._lib.EC_KEY_get0_private_key(self._ec_key)
        private_value = self._backend._bn_to_int(bn)
        return ec.EllipticCurvePrivateNumbers(private_value=private_value,
          public_numbers=(self.public_key().public_numbers()))

    def private_bytes(self, encoding: serialization.Encoding, format: serialization.PrivateFormat, encryption_algorithm: serialization.KeySerializationEncryption) -> bytes:
        return self._backend._private_key_bytes(encoding, format, encryption_algorithm, self, self._evp_pkey, self._ec_key)

    def sign(self, data: bytes, signature_algorithm: ec.EllipticCurveSignatureAlgorithm) -> bytes:
        _check_signature_algorithm(signature_algorithm)
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, signature_algorithm._algorithm)
        return _ecdsa_sig_sign(self._backend, self, data)


class _EllipticCurvePublicKey(ec.EllipticCurvePublicKey):

    def __init__(self, backend, ec_key_cdata, evp_pkey):
        self._backend = backend
        self._ec_key = ec_key_cdata
        self._evp_pkey = evp_pkey
        sn = _ec_key_curve_sn(backend, ec_key_cdata)
        self._curve = _sn_to_elliptic_curve(backend, sn)
        _mark_asn1_named_ec_curve(backend, ec_key_cdata)

    curve = utils.read_only_property('_curve')

    @property
    def key_size(self) -> int:
        return self.curve.key_size

    def verifier(self, signature: bytes, signature_algorithm: ec.EllipticCurveSignatureAlgorithm) -> AsymmetricVerificationContext:
        _warn_sign_verify_deprecated
        utils._check_bytes('signature', signature)
        _check_signature_algorithm(signature_algorithm)
        _check_not_prehashed(signature_algorithm.algorithm)
        assert isinstance(signature_algorithm.algorithm, hashes.HashAlgorithm)
        return _ECDSAVerificationContext(self._backend, self, signature, signature_algorithm.algorithm)

    def public_numbers(self) -> ec.EllipticCurvePublicNumbers:
        get_func, group = self._backend._ec_key_determine_group_get_func(self._ec_key)
        point = self._backend._lib.EC_KEY_get0_public_key(self._ec_key)
        self._backend.openssl_assert(point != self._backend._ffi.NULL)
        with self._backend._tmp_bn_ctx() as (bn_ctx):
            bn_x = self._backend._lib.BN_CTX_get(bn_ctx)
            bn_y = self._backend._lib.BN_CTX_get(bn_ctx)
            res = get_func(group, point, bn_x, bn_y, bn_ctx)
            self._backend.openssl_assert(res == 1)
            x = self._backend._bn_to_int(bn_x)
            y = self._backend._bn_to_int(bn_y)
        return ec.EllipticCurvePublicNumbers(x=x, y=y, curve=(self._curve))

    def _encode_point(self, format: serialization.PublicFormat) -> bytes:
        if format is serialization.PublicFormat.CompressedPoint:
            conversion = self._backend._lib.POINT_CONVERSION_COMPRESSED
        else:
            assert format is serialization.PublicFormat.UncompressedPoint
            conversion = self._backend._lib.POINT_CONVERSION_UNCOMPRESSED
        group = self._backend._lib.EC_KEY_get0_group(self._ec_key)
        self._backend.openssl_assert(group != self._backend._ffi.NULL)
        point = self._backend._lib.EC_KEY_get0_public_key(self._ec_key)
        self._backend.openssl_assert(point != self._backend._ffi.NULL)
        with self._backend._tmp_bn_ctx() as (bn_ctx):
            buflen = self._backend._lib.EC_POINT_point2oct(group, point, conversion, self._backend._ffi.NULL, 0, bn_ctx)
            self._backend.openssl_assert(buflen > 0)
            buf = self._backend._ffi.new('char[]', buflen)
            res = self._backend._lib.EC_POINT_point2oct(group, point, conversion, buf, buflen, bn_ctx)
            self._backend.openssl_assert(buflen == res)
        return self._backend._ffi.buffer(buf)[:]

    def public_bytes(self, encoding: serialization.Encoding, format: serialization.PublicFormat) -> bytes:
        if encoding is serialization.Encoding.X962 or format is serialization.PublicFormat.CompressedPoint or format is serialization.PublicFormat.UncompressedPoint:
            if encoding is not serialization.Encoding.X962 or format not in (
             serialization.PublicFormat.CompressedPoint,
             serialization.PublicFormat.UncompressedPoint):
                raise ValueError('X962 encoding must be used with CompressedPoint or UncompressedPoint format')
            return self._encode_point(format)
        return self._backend._public_key_bytes(encoding, format, self, self._evp_pkey, None)

    def verify(self, signature: bytes, data: bytes, signature_algorithm: ec.EllipticCurveSignatureAlgorithm) -> None:
        _check_signature_algorithm(signature_algorithm)
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, signature_algorithm._algorithm)
        _ecdsa_sig_verify(self._backend, self, signature, data)