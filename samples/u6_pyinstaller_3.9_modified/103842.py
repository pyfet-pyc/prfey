# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\ec.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.openssl.utils import _calculate_digest_and_algorithm, _check_not_prehashed, _warn_sign_verify_deprecated
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, ec

def _check_signature_algorithm(signature_algorithm):
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

 L.  77         0  SETUP_FINALLY        16  'to 16'

 L.  78         2  LOAD_GLOBAL              ec
                4  LOAD_ATTR                _CURVE_TYPES
                6  LOAD_FAST                'sn'
                8  BINARY_SUBSCR    
               10  CALL_FUNCTION_0       0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  79        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                50  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  80        28  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  81        30  LOAD_STR                 '{} is not a supported elliptic curve'
               32  LOAD_METHOD              format
               34  LOAD_FAST                'sn'
               36  CALL_METHOD_1         1  ''

 L.  82        38  LOAD_GLOBAL              _Reasons
               40  LOAD_ATTR                UNSUPPORTED_ELLIPTIC_CURVE

 L.  80        42  CALL_FUNCTION_2       2  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 20


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


@utils.register_interface(AsymmetricSignatureContext)
class _ECDSASignatureContext(object):

    def __init__(self, backend, private_key, algorithm):
        self._backend = backend
        self._private_key = private_key
        self._digest = hashes.Hash(algorithm, backend)

    def update(self, data):
        self._digest.update(data)

    def finalize(self):
        digest = self._digest.finalize()
        return _ecdsa_sig_sign(self._backend, self._private_key, digest)


@utils.register_interface(AsymmetricVerificationContext)
class _ECDSAVerificationContext(object):

    def __init__(self, backend, public_key, signature, algorithm):
        self._backend = backend
        self._public_key = public_key
        self._signature = signature
        self._digest = hashes.Hash(algorithm, backend)

    def update(self, data):
        self._digest.update(data)

    def verify(self):
        digest = self._digest.finalize()
        _ecdsa_sig_verify(self._backend, self._public_key, self._signature, digest)


@utils.register_interface(ec.EllipticCurvePrivateKeyWithSerialization)
class _EllipticCurvePrivateKey(object):

    def __init__(self, backend, ec_key_cdata, evp_pkey):
        self._backend = backend
        self._ec_key = ec_key_cdata
        self._evp_pkey = evp_pkey
        sn = _ec_key_curve_sn(backend, ec_key_cdata)
        self._curve = _sn_to_elliptic_curve(backend, sn)
        _mark_asn1_named_ec_curve(backend, ec_key_cdata)

    curve = utils.read_only_property('_curve')

    @property
    def key_size(self):
        return self.curve.key_size

    def signer(self, signature_algorithm):
        _warn_sign_verify_deprecated
        _check_signature_algorithm(signature_algorithm)
        _check_not_prehashed(signature_algorithm.algorithm)
        return _ECDSASignatureContext(self._backend, self, signature_algorithm.algorithm)

    def exchange(self, algorithm, peer_public_key):
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

    def public_key(self):
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

    def private_numbers(self):
        bn = self._backend._lib.EC_KEY_get0_private_key(self._ec_key)
        private_value = self._backend._bn_to_int(bn)
        return ec.EllipticCurvePrivateNumbers(private_value=private_value,
          public_numbers=(self.public_key().public_numbers()))

    def private_bytes(self, encoding, format, encryption_algorithm):
        return self._backend._private_key_bytes(encoding, format, encryption_algorithm, self, self._evp_pkey, self._ec_key)

    def sign(self, data, signature_algorithm):
        _check_signature_algorithm(signature_algorithm)
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, signature_algorithm._algorithm)
        return _ecdsa_sig_sign(self._backend, self, data)


@utils.register_interface(ec.EllipticCurvePublicKeyWithSerialization)
class _EllipticCurvePublicKey(object):

    def __init__(self, backend, ec_key_cdata, evp_pkey):
        self._backend = backend
        self._ec_key = ec_key_cdata
        self._evp_pkey = evp_pkey
        sn = _ec_key_curve_sn(backend, ec_key_cdata)
        self._curve = _sn_to_elliptic_curve(backend, sn)
        _mark_asn1_named_ec_curve(backend, ec_key_cdata)

    curve = utils.read_only_property('_curve')

    @property
    def key_size(self):
        return self.curve.key_size

    def verifier(self, signature, signature_algorithm):
        _warn_sign_verify_deprecated
        utils._check_bytes('signature', signature)
        _check_signature_algorithm(signature_algorithm)
        _check_not_prehashed(signature_algorithm.algorithm)
        return _ECDSAVerificationContext(self._backend, self, signature, signature_algorithm.algorithm)

    def public_numbers--- This code section failed: ---

 L. 268         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _backend
                4  LOAD_METHOD              _ec_key_determine_group_get_func

 L. 269         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _ec_key

 L. 268        10  CALL_METHOD_1         1  ''
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'get_func'
               16  STORE_FAST               'group'

 L. 271        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _backend
               22  LOAD_ATTR                _lib
               24  LOAD_METHOD              EC_KEY_get0_public_key
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _ec_key
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'point'

 L. 272        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _backend
               38  LOAD_METHOD              openssl_assert
               40  LOAD_FAST                'point'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _backend
               46  LOAD_ATTR                _ffi
               48  LOAD_ATTR                NULL
               50  COMPARE_OP               !=
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 274        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _backend
               60  LOAD_METHOD              _tmp_bn_ctx
               62  CALL_METHOD_0         0  ''
               64  SETUP_WITH          166  'to 166'
               66  STORE_FAST               'bn_ctx'

 L. 275        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _backend
               72  LOAD_ATTR                _lib
               74  LOAD_METHOD              BN_CTX_get
               76  LOAD_FAST                'bn_ctx'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'bn_x'

 L. 276        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _backend
               86  LOAD_ATTR                _lib
               88  LOAD_METHOD              BN_CTX_get
               90  LOAD_FAST                'bn_ctx'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'bn_y'

 L. 278        96  LOAD_FAST                'get_func'
               98  LOAD_FAST                'group'
              100  LOAD_FAST                'point'
              102  LOAD_FAST                'bn_x'
              104  LOAD_FAST                'bn_y'
              106  LOAD_FAST                'bn_ctx'
              108  CALL_FUNCTION_5       5  ''
              110  STORE_FAST               'res'

 L. 279       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _backend
              116  LOAD_METHOD              openssl_assert
              118  LOAD_FAST                'res'
              120  LOAD_CONST               1
              122  COMPARE_OP               ==
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 281       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _backend
              132  LOAD_METHOD              _bn_to_int
              134  LOAD_FAST                'bn_x'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'x'

 L. 282       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _backend
              144  LOAD_METHOD              _bn_to_int
              146  LOAD_FAST                'bn_y'
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'y'
              152  POP_BLOCK        
              154  LOAD_CONST               None
              156  DUP_TOP          
              158  DUP_TOP          
              160  CALL_FUNCTION_3       3  ''
              162  POP_TOP          
              164  JUMP_FORWARD        182  'to 182'
            166_0  COME_FROM_WITH       64  '64'
              166  <49>             
              168  POP_JUMP_IF_TRUE    172  'to 172'
              170  <48>             
            172_0  COME_FROM           168  '168'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          
              178  POP_EXCEPT       
              180  POP_TOP          
            182_0  COME_FROM           164  '164'

 L. 284       182  LOAD_GLOBAL              ec
              184  LOAD_ATTR                EllipticCurvePublicNumbers
              186  LOAD_FAST                'x'
              188  LOAD_FAST                'y'
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                _curve
              194  LOAD_CONST               ('x', 'y', 'curve')
              196  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 156

    def _encode_point--- This code section failed: ---

 L. 287         0  LOAD_FAST                'format'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                PublicFormat
                6  LOAD_ATTR                CompressedPoint
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L. 288        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _backend
               16  LOAD_ATTR                _lib
               18  LOAD_ATTR                POINT_CONVERSION_COMPRESSED
               20  STORE_FAST               'conversion'
               22  JUMP_FORWARD         50  'to 50'
             24_0  COME_FROM            10  '10'

 L. 290        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PublicFormat
               30  LOAD_ATTR                UncompressedPoint
               32  <117>                 0  ''
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  <74>             
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 291        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _backend
               44  LOAD_ATTR                _lib
               46  LOAD_ATTR                POINT_CONVERSION_UNCOMPRESSED
               48  STORE_FAST               'conversion'
             50_0  COME_FROM            22  '22'

 L. 293        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _backend
               54  LOAD_ATTR                _lib
               56  LOAD_METHOD              EC_KEY_get0_group
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _ec_key
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'group'

 L. 294        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_METHOD              openssl_assert
               72  LOAD_FAST                'group'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _backend
               78  LOAD_ATTR                _ffi
               80  LOAD_ATTR                NULL
               82  COMPARE_OP               !=
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 295        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _backend
               92  LOAD_ATTR                _lib
               94  LOAD_METHOD              EC_KEY_get0_public_key
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _ec_key
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'point'

 L. 296       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _backend
              108  LOAD_METHOD              openssl_assert
              110  LOAD_FAST                'point'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _backend
              116  LOAD_ATTR                _ffi
              118  LOAD_ATTR                NULL
              120  COMPARE_OP               !=
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 297       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _backend
              130  LOAD_METHOD              _tmp_bn_ctx
              132  CALL_METHOD_0         0  ''
              134  SETUP_WITH          254  'to 254'
              136  STORE_FAST               'bn_ctx'

 L. 298       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _backend
              142  LOAD_ATTR                _lib
              144  LOAD_METHOD              EC_POINT_point2oct

 L. 299       146  LOAD_FAST                'group'
              148  LOAD_FAST                'point'
              150  LOAD_FAST                'conversion'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _backend
              156  LOAD_ATTR                _ffi
              158  LOAD_ATTR                NULL
              160  LOAD_CONST               0
              162  LOAD_FAST                'bn_ctx'

 L. 298       164  CALL_METHOD_6         6  ''
              166  STORE_FAST               'buflen'

 L. 301       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _backend
              172  LOAD_METHOD              openssl_assert
              174  LOAD_FAST                'buflen'
              176  LOAD_CONST               0
              178  COMPARE_OP               >
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 302       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _backend
              188  LOAD_ATTR                _ffi
              190  LOAD_METHOD              new
              192  LOAD_STR                 'char[]'
              194  LOAD_FAST                'buflen'
              196  CALL_METHOD_2         2  ''
              198  STORE_FAST               'buf'

 L. 303       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _backend
              204  LOAD_ATTR                _lib
              206  LOAD_METHOD              EC_POINT_point2oct

 L. 304       208  LOAD_FAST                'group'
              210  LOAD_FAST                'point'
              212  LOAD_FAST                'conversion'
              214  LOAD_FAST                'buf'
              216  LOAD_FAST                'buflen'
              218  LOAD_FAST                'bn_ctx'

 L. 303       220  CALL_METHOD_6         6  ''
              222  STORE_FAST               'res'

 L. 306       224  LOAD_FAST                'self'
              226  LOAD_ATTR                _backend
              228  LOAD_METHOD              openssl_assert
              230  LOAD_FAST                'buflen'
              232  LOAD_FAST                'res'
              234  COMPARE_OP               ==
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
              240  POP_BLOCK        
              242  LOAD_CONST               None
              244  DUP_TOP          
              246  DUP_TOP          
              248  CALL_FUNCTION_3       3  ''
              250  POP_TOP          
              252  JUMP_FORWARD        272  'to 272'
            254_0  COME_FROM_WITH      134  '134'
              254  <49>             
          256_258  POP_JUMP_IF_TRUE    262  'to 262'
              260  <48>             
            262_0  COME_FROM           256  '256'
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          
              268  POP_EXCEPT       
              270  POP_TOP          
            272_0  COME_FROM           252  '252'

 L. 308       272  LOAD_FAST                'self'
              274  LOAD_ATTR                _backend
              276  LOAD_ATTR                _ffi
              278  LOAD_METHOD              buffer
              280  LOAD_FAST                'buf'
              282  CALL_METHOD_1         1  ''
              284  LOAD_CONST               None
              286  LOAD_CONST               None
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    
              292  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def public_bytes--- This code section failed: ---

 L. 313         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                X962
                8  <117>                 0  ''

 L. 312        10  POP_JUMP_IF_TRUE     36  'to 36'

 L. 314        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                CompressedPoint
               20  <117>                 0  ''

 L. 312        22  POP_JUMP_IF_TRUE     36  'to 36'

 L. 315        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PublicFormat
               30  LOAD_ATTR                UncompressedPoint
               32  <117>                 0  ''

 L. 312        34  POP_JUMP_IF_FALSE    86  'to 86'
             36_0  COME_FROM            22  '22'
             36_1  COME_FROM            10  '10'

 L. 317        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                X962
               44  <117>                 1  ''
               46  POP_JUMP_IF_TRUE     68  'to 68'
               48  LOAD_FAST                'format'

 L. 318        50  LOAD_GLOBAL              serialization
               52  LOAD_ATTR                PublicFormat
               54  LOAD_ATTR                CompressedPoint

 L. 319        56  LOAD_GLOBAL              serialization
               58  LOAD_ATTR                PublicFormat
               60  LOAD_ATTR                UncompressedPoint

 L. 317        62  BUILD_TUPLE_2         2 
               64  <118>                 1  ''
               66  POP_JUMP_IF_FALSE    76  'to 76'
             68_0  COME_FROM            46  '46'

 L. 321        68  LOAD_GLOBAL              ValueError

 L. 322        70  LOAD_STR                 'X962 encoding must be used with CompressedPoint or UncompressedPoint format'

 L. 321        72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L. 326        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _encode_point
               80  LOAD_FAST                'format'
               82  CALL_METHOD_1         1  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            34  '34'

 L. 328        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _backend
               90  LOAD_METHOD              _public_key_bytes

 L. 329        92  LOAD_FAST                'encoding'
               94  LOAD_FAST                'format'
               96  LOAD_FAST                'self'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                _evp_pkey
              102  LOAD_CONST               None

 L. 328       104  CALL_METHOD_5         5  ''
              106  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def verify(self, signature, data, signature_algorithm):
        _check_signature_algorithm(signature_algorithm)
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, signature_algorithm._algorithm)
        _ecdsa_sig_verify(self._backend, self, signature, data)