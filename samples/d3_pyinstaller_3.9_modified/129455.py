# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\ed25519.py
from cryptography import exceptions
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey, _ED25519_KEY_SIZE, _ED25519_SIG_SIZE

class _Ed25519PublicKey(Ed25519PublicKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_bytes--- This code section failed: ---

 L.  27         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L.  26        10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  28        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L.  26        22  POP_JUMP_IF_FALSE    64  'to 64'
             24_0  COME_FROM            10  '10'

 L.  31        24  LOAD_FAST                'encoding'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                Encoding
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L.  30        34  POP_JUMP_IF_TRUE     48  'to 48'

 L.  32        36  LOAD_FAST                'format'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                PublicFormat
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L.  30        46  POP_JUMP_IF_FALSE    56  'to 56'
             48_0  COME_FROM            34  '34'

 L.  34        48  LOAD_GLOBAL              ValueError

 L.  35        50  LOAD_STR                 'When using Raw both encoding and format must be Raw'

 L.  34        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  38        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _raw_public_bytes
               60  CALL_METHOD_0         0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            22  '22'

 L.  40        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _public_key_bytes

 L.  41        70  LOAD_FAST                'encoding'
               72  LOAD_FAST                'format'
               74  LOAD_FAST                'self'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _evp_pkey
               80  LOAD_CONST               None

 L.  40        82  CALL_METHOD_5         5  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _raw_public_bytes(self) -> bytes:
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED25519_KEY_SIZE)[:]

    def verify(self, signature: bytes, data: bytes) -> None:
        evp_md_ctx = self._backend._lib.EVP_MD_CTX_new
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestVerifyInitevp_md_ctxself._backend._ffi.NULLself._backend._ffi.NULLself._backend._ffi.NULLself._evp_pkey
        self._backend.openssl_assert(res == 1)
        res = self._backend._lib.EVP_DigestVerifyevp_md_ctxsignaturelen(signature)datalen(data)
        if res != 1:
            self._backend._consume_errors
            raise exceptions.InvalidSignature


class _Ed25519PrivateKey(Ed25519PrivateKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self) -> Ed25519PublicKey:
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        public_bytes = self._backend._ffi.buffer(buf)[:]
        return self._backend.ed25519_load_public_bytes(public_bytes)

    def sign(self, data: bytes) -> bytes:
        evp_md_ctx = self._backend._lib.EVP_MD_CTX_new
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestSignInitevp_md_ctxself._backend._ffi.NULLself._backend._ffi.NULLself._backend._ffi.NULLself._evp_pkey
        self._backend.openssl_assert(res == 1)
        buf = self._backend._ffi.new('unsigned char[]', _ED25519_SIG_SIZE)
        buflen = self._backend._ffi.new('size_t *', len(buf))
        res = self._backend._lib.EVP_DigestSignevp_md_ctxbufbuflendatalen(data)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_SIG_SIZE)
        return self._backend._ffi.buffer(buf, buflen[0])[:]

    def private_bytes--- This code section failed: ---

 L. 122         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L. 121        10  POP_JUMP_IF_TRUE     24  'to 24'

 L. 123        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L. 121        22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L. 126        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L. 125        34  POP_JUMP_IF_TRUE     60  'to 60'

 L. 127        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L. 125        46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 128        48  LOAD_GLOBAL              isinstance

 L. 129        50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption

 L. 128        56  CALL_FUNCTION_2       2  ''

 L. 125        58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L. 132        60  LOAD_GLOBAL              ValueError

 L. 133        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'

 L. 132        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 137        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 139        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _private_key_bytes

 L. 140        82  LOAD_FAST                'encoding'
               84  LOAD_FAST                'format'
               86  LOAD_FAST                'encryption_algorithm'
               88  LOAD_FAST                'self'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _evp_pkey
               94  LOAD_CONST               None

 L. 139        96  CALL_METHOD_6         6  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _raw_private_bytes(self) -> bytes:
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_private_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED25519_KEY_SIZE)[:]