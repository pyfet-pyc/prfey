# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\dh.py
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh

def _dh_params_dup(dh_cdata, backend):
    lib = backend._lib
    ffi = backend._ffi
    param_cdata = lib.DHparams_dup(dh_cdata)
    backend.openssl_assert(param_cdata != ffi.NULL)
    param_cdata = ffi.gc(param_cdata, lib.DH_free)
    if lib.CRYPTOGRAPHY_IS_LIBRESSL:
        q = ffi.new('BIGNUM **')
        lib.DH_get0_pqg(dh_cdata, ffi.NULL, q, ffi.NULL)
        q_dup = lib.BN_dup(q[0])
        res = lib.DH_set0_pqg(param_cdata, ffi.NULL, q_dup, ffi.NULL)
        backend.openssl_assert(res == 1)
    return param_cdata


def _dh_cdata_to_parameters(dh_cdata, backend):
    param_cdata = _dh_params_dup(dh_cdata, backend)
    return _DHParameters(backend, param_cdata)


class _DHParameters(dh.DHParameters):

    def __init__(self, backend, dh_cdata):
        self._backend = backend
        self._dh_cdata = dh_cdata

    def parameter_numbers(self) -> dh.DHParameterNumbers:
        p = self._backend._ffi.new('BIGNUM **')
        g = self._backend._ffi.new('BIGNUM **')
        q = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_pqg(self._dh_cdata, p, q, g)
        self._backend.openssl_assert(p[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(g[0] != self._backend._ffi.NULL)
        if q[0] == self._backend._ffi.NULL:
            q_val = None
        else:
            q_val = self._backend._bn_to_int(q[0])
        return dh.DHParameterNumbers(p=(self._backend._bn_to_int(p[0])),
          g=(self._backend._bn_to_int(g[0])),
          q=q_val)

    def generate_private_key(self) -> dh.DHPrivateKey:
        return self._backend.generate_dh_private_key(self)

    def parameter_bytes--- This code section failed: ---

 L.  64         0  LOAD_FAST                'format'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                ParameterFormat
                6  LOAD_ATTR                PKCS3
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  65        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'Only PKCS3 serialization is supported'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  66        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                Cryptography_HAS_EVP_PKEY_DHX
               28  POP_JUMP_IF_TRUE    108  'to 108'

 L.  67        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _ffi
               36  LOAD_METHOD              new
               38  LOAD_STR                 'BIGNUM **'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'q'

 L.  68        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _lib
               50  LOAD_METHOD              DH_get0_pqg

 L.  69        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _dh_cdata

 L.  70        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _backend
               60  LOAD_ATTR                _ffi
               62  LOAD_ATTR                NULL

 L.  71        64  LOAD_FAST                'q'

 L.  72        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _ffi
               72  LOAD_ATTR                NULL

 L.  68        74  CALL_METHOD_4         4  ''
               76  POP_TOP          

 L.  74        78  LOAD_FAST                'q'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _backend
               88  LOAD_ATTR                _ffi
               90  LOAD_ATTR                NULL
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L.  75        96  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  76        98  LOAD_STR                 'DH X9.42 serialization is not supported'

 L.  77       100  LOAD_GLOBAL              _Reasons
              102  LOAD_ATTR                UNSUPPORTED_SERIALIZATION

 L.  75       104  CALL_FUNCTION_2       2  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            28  '28'

 L.  80       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _backend
              112  LOAD_METHOD              _parameter_bytes
              114  LOAD_FAST                'encoding'
              116  LOAD_FAST                'format'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _dh_cdata
              122  CALL_METHOD_3         3  ''
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_dh_num_bits(backend, dh_cdata) -> int:
    p = backend._ffi.new('BIGNUM **')
    backend._lib.DH_get0_pqg(dh_cdata, p, backend._ffi.NULL, backend._ffi.NULL)
    backend.openssl_assert(p[0] != backend._ffi.NULL)
    return backend._lib.BN_num_bits(p[0])


class _DHPrivateKey(dh.DHPrivateKey):

    def __init__(self, backend, dh_cdata, evp_pkey):
        self._backend = backend
        self._dh_cdata = dh_cdata
        self._evp_pkey = evp_pkey
        self._key_size_bytes = self._backend._lib.DH_size(dh_cdata)

    @property
    def key_size(self) -> int:
        return _get_dh_num_bits(self._backend, self._dh_cdata)

    def private_numbers(self) -> dh.DHPrivateNumbers:
        p = self._backend._ffi.new('BIGNUM **')
        g = self._backend._ffi.new('BIGNUM **')
        q = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_pqg(self._dh_cdata, p, q, g)
        self._backend.openssl_assert(p[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(g[0] != self._backend._ffi.NULL)
        if q[0] == self._backend._ffi.NULL:
            q_val = None
        else:
            q_val = self._backend._bn_to_int(q[0])
        pub_key = self._backend._ffi.new('BIGNUM **')
        priv_key = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_keyself._dh_cdatapub_keypriv_key
        self._backend.openssl_assert(pub_key[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(priv_key[0] != self._backend._ffi.NULL)
        return dh.DHPrivateNumbers(public_numbers=dh.DHPublicNumbers(parameter_numbers=dh.DHParameterNumbers(p=(self._backend._bn_to_int(p[0])),
          g=(self._backend._bn_to_int(g[0])),
          q=q_val),
          y=(self._backend._bn_to_int(pub_key[0]))),
          x=(self._backend._bn_to_int(priv_key[0])))

    def exchange(self, peer_public_key: dh.DHPublicKey) -> bytes:
        buf = self._backend._ffi.new('unsigned char[]', self._key_size_bytes)
        pub_key = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_keypeer_public_key._dh_cdatapub_keyself._backend._ffi.NULL
        self._backend.openssl_assert(pub_key[0] != self._backend._ffi.NULL)
        res = self._backend._lib.DH_compute_keybufpub_key[0]self._dh_cdata
        if res == -1:
            errors_with_text = self._backend._consume_errors_with_text()
            raise ValueError('Error computing shared key. Public key is likely invalid for this exchange.', errors_with_text)
        else:
            self._backend.openssl_assert(res >= 1)
            key = self._backend._ffi.buffer(buf)[:res]
            pad = self._key_size_bytes - len(key)
            if pad > 0:
                key = b'\x00' * pad + key
            return key

    def public_key(self) -> dh.DHPublicKey:
        dh_cdata = _dh_params_dup(self._dh_cdata, self._backend)
        pub_key = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_keyself._dh_cdatapub_keyself._backend._ffi.NULL
        self._backend.openssl_assert(pub_key[0] != self._backend._ffi.NULL)
        pub_key_dup = self._backend._lib.BN_dup(pub_key[0])
        self._backend.openssl_assert(pub_key_dup != self._backend._ffi.NULL)
        res = self._backend._lib.DH_set0_keydh_cdatapub_key_dupself._backend._ffi.NULL
        self._backend.openssl_assert(res == 1)
        evp_pkey = self._backend._dh_cdata_to_evp_pkey(dh_cdata)
        return _DHPublicKey(self._backend, dh_cdata, evp_pkey)

    def parameters(self) -> dh.DHParameters:
        return _dh_cdata_to_parameters(self._dh_cdata, self._backend)

    def private_bytes--- This code section failed: ---

 L. 186         0  LOAD_FAST                'format'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                PrivateFormat
                6  LOAD_ATTR                PKCS8
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 187        12  LOAD_GLOBAL              ValueError

 L. 188        14  LOAD_STR                 'DH private keys support only PKCS8 serialization'

 L. 187        16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 190        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                Cryptography_HAS_EVP_PKEY_DHX
               28  POP_JUMP_IF_TRUE    108  'to 108'

 L. 191        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _ffi
               36  LOAD_METHOD              new
               38  LOAD_STR                 'BIGNUM **'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'q'

 L. 192        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _lib
               50  LOAD_METHOD              DH_get0_pqg

 L. 193        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _dh_cdata

 L. 194        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _backend
               60  LOAD_ATTR                _ffi
               62  LOAD_ATTR                NULL

 L. 195        64  LOAD_FAST                'q'

 L. 196        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _ffi
               72  LOAD_ATTR                NULL

 L. 192        74  CALL_METHOD_4         4  ''
               76  POP_TOP          

 L. 198        78  LOAD_FAST                'q'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _backend
               88  LOAD_ATTR                _ffi
               90  LOAD_ATTR                NULL
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 199        96  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 200        98  LOAD_STR                 'DH X9.42 serialization is not supported'

 L. 201       100  LOAD_GLOBAL              _Reasons
              102  LOAD_ATTR                UNSUPPORTED_SERIALIZATION

 L. 199       104  CALL_FUNCTION_2       2  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            28  '28'

 L. 204       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _backend
              112  LOAD_METHOD              _private_key_bytes

 L. 205       114  LOAD_FAST                'encoding'

 L. 206       116  LOAD_FAST                'format'

 L. 207       118  LOAD_FAST                'encryption_algorithm'

 L. 208       120  LOAD_FAST                'self'

 L. 209       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _evp_pkey

 L. 210       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _dh_cdata

 L. 204       130  CALL_METHOD_6         6  ''
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class _DHPublicKey(dh.DHPublicKey):

    def __init__(self, backend, dh_cdata, evp_pkey):
        self._backend = backend
        self._dh_cdata = dh_cdata
        self._evp_pkey = evp_pkey
        self._key_size_bits = _get_dh_num_bits(self._backend, self._dh_cdata)

    @property
    def key_size(self) -> int:
        return self._key_size_bits

    def public_numbers(self) -> dh.DHPublicNumbers:
        p = self._backend._ffi.new('BIGNUM **')
        g = self._backend._ffi.new('BIGNUM **')
        q = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_pqg(self._dh_cdata, p, q, g)
        self._backend.openssl_assert(p[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(g[0] != self._backend._ffi.NULL)
        if q[0] == self._backend._ffi.NULL:
            q_val = None
        else:
            q_val = self._backend._bn_to_int(q[0])
        pub_key = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.DH_get0_keyself._dh_cdatapub_keyself._backend._ffi.NULL
        self._backend.openssl_assert(pub_key[0] != self._backend._ffi.NULL)
        return dh.DHPublicNumbers(parameter_numbers=dh.DHParameterNumbers(p=(self._backend._bn_to_int(p[0])),
          g=(self._backend._bn_to_int(g[0])),
          q=q_val),
          y=(self._backend._bn_to_int(pub_key[0])))

    def parameters(self) -> dh.DHParameters:
        return _dh_cdata_to_parameters(self._dh_cdata, self._backend)

    def public_bytes--- This code section failed: ---

 L. 258         0  LOAD_FAST                'format'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                PublicFormat
                6  LOAD_ATTR                SubjectPublicKeyInfo
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 259        12  LOAD_GLOBAL              ValueError

 L. 260        14  LOAD_STR                 'DH public keys support only SubjectPublicKeyInfo serialization'

 L. 259        16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 264        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                Cryptography_HAS_EVP_PKEY_DHX
               28  POP_JUMP_IF_TRUE    108  'to 108'

 L. 265        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _backend
               34  LOAD_ATTR                _ffi
               36  LOAD_METHOD              new
               38  LOAD_STR                 'BIGNUM **'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'q'

 L. 266        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _lib
               50  LOAD_METHOD              DH_get0_pqg

 L. 267        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _dh_cdata

 L. 268        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _backend
               60  LOAD_ATTR                _ffi
               62  LOAD_ATTR                NULL

 L. 269        64  LOAD_FAST                'q'

 L. 270        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _ffi
               72  LOAD_ATTR                NULL

 L. 266        74  CALL_METHOD_4         4  ''
               76  POP_TOP          

 L. 272        78  LOAD_FAST                'q'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _backend
               88  LOAD_ATTR                _ffi
               90  LOAD_ATTR                NULL
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 273        96  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 274        98  LOAD_STR                 'DH X9.42 serialization is not supported'

 L. 275       100  LOAD_GLOBAL              _Reasons
              102  LOAD_ATTR                UNSUPPORTED_SERIALIZATION

 L. 273       104  CALL_FUNCTION_2       2  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            28  '28'

 L. 278       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _backend
              112  LOAD_METHOD              _public_key_bytes

 L. 279       114  LOAD_FAST                'encoding'
              116  LOAD_FAST                'format'
              118  LOAD_FAST                'self'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _evp_pkey
              124  LOAD_CONST               None

 L. 278       126  CALL_METHOD_5         5  ''
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1