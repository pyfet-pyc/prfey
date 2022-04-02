# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\x25519.py
from cryptography.hazmat.backends.openssl.utils import _evp_pkey_derive
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
_X25519_KEY_SIZE = 32

class _X25519PublicKey(X25519PublicKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_bytes--- This code section failed: ---

 L.  28         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L.  27        10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  29        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L.  27        22  POP_JUMP_IF_FALSE    64  'to 64'
             24_0  COME_FROM            10  '10'

 L.  32        24  LOAD_FAST                'encoding'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                Encoding
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L.  31        34  POP_JUMP_IF_TRUE     48  'to 48'

 L.  33        36  LOAD_FAST                'format'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                PublicFormat
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L.  31        46  POP_JUMP_IF_FALSE    56  'to 56'
             48_0  COME_FROM            34  '34'

 L.  35        48  LOAD_GLOBAL              ValueError

 L.  36        50  LOAD_STR                 'When using Raw both encoding and format must be Raw'

 L.  35        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  39        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _raw_public_bytes
               60  CALL_METHOD_0         0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            22  '22'

 L.  41        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _public_key_bytes

 L.  42        70  LOAD_FAST                'encoding'
               72  LOAD_FAST                'format'
               74  LOAD_FAST                'self'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _evp_pkey
               80  LOAD_CONST               None

 L.  41        82  CALL_METHOD_5         5  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _raw_public_bytes(self) -> bytes:
        ucharpp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.EVP_PKEY_get1_tls_encodedpoint(self._evp_pkey, ucharpp)
        self._backend.openssl_assert(res == 32)
        self._backend.openssl_assert(ucharpp[0] != self._backend._ffi.NULL)
        data = self._backend._ffi.gc(ucharpp[0], self._backend._lib.OPENSSL_free)
        return self._backend._ffi.buffer(data, res)[:]


class _X25519PrivateKey(X25519PrivateKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self) -> X25519PublicKey:
        bio = self._backend._create_mem_bio_gc
        res = self._backend._lib.i2d_PUBKEY_bio(bio, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        evp_pkey = self._backend._lib.d2i_PUBKEY_bio(bio, self._backend._ffi.NULL)
        self._backend.openssl_assert(evp_pkey != self._backend._ffi.NULL)
        evp_pkey = self._backend._ffi.gc(evp_pkey, self._backend._lib.EVP_PKEY_free)
        return _X25519PublicKey(self._backend, evp_pkey)

    def exchange(self, peer_public_key: X25519PublicKey) -> bytes:
        if not isinstance(peer_public_key, X25519PublicKey):
            raise TypeError('peer_public_key must be X25519PublicKey.')
        return _evp_pkey_derive(self._backend, self._evp_pkey, peer_public_key)

    def private_bytes--- This code section failed: ---

 L.  89         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L.  88        10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  90        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L.  88        22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L.  93        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L.  92        34  POP_JUMP_IF_TRUE     60  'to 60'

 L.  94        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L.  92        46  POP_JUMP_IF_TRUE     60  'to 60'

 L.  95        48  LOAD_GLOBAL              isinstance

 L.  96        50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption

 L.  95        56  CALL_FUNCTION_2       2  ''

 L.  92        58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L.  99        60  LOAD_GLOBAL              ValueError

 L. 100        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'

 L.  99        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 104        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 106        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _private_key_bytes

 L. 107        82  LOAD_FAST                'encoding'
               84  LOAD_FAST                'format'
               86  LOAD_FAST                'encryption_algorithm'
               88  LOAD_FAST                'self'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _evp_pkey
               94  LOAD_CONST               None

 L. 106        96  CALL_METHOD_6         6  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _raw_private_bytes(self) -> bytes:
        bio = self._backend._create_mem_bio_gc
        res = self._backend._lib.i2d_PKCS8PrivateKey_bio(bio, self._evp_pkey, self._backend._ffi.NULL, self._backend._ffi.NULL, 0, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(res == 1)
        pkcs8 = self._backend._read_mem_bio(bio)
        self._backend.openssl_assert(len(pkcs8) == 48)
        return pkcs8[-_X25519_KEY_SIZE:]