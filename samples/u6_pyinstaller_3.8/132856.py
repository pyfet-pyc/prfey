# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: cryptography\hazmat\backends\openssl\ed448.py
from cryptography import exceptions
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey, Ed448PublicKey
_ED448_KEY_SIZE = 57
_ED448_SIG_SIZE = 114

class _Ed448PublicKey(Ed448PublicKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_bytes(self, encoding: serialization.Encoding, format: serialization.PublicFormat) -> bytes:
        if encoding is serialization.Encoding.Raw or format is serialization.PublicFormat.Raw:
            if encoding is not serialization.Encoding.Raw or format is not serialization.PublicFormat.Raw:
                raise ValueError('When using Raw both encoding and format must be Raw')
            return self._raw_public_bytes()
        return self._backend._public_key_bytes(encoding, format, self, self._evp_pkey, None)

    def _raw_public_bytes(self) -> bytes:
        buf = self._backend._ffi.new('unsigned char []', _ED448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED448_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED448_KEY_SIZE)[:]

    def verify(self, signature: bytes, data: bytes) -> None:
        evp_md_ctx = self._backend._lib.EVP_MD_CTX_new()
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestVerifyInit(evp_md_ctx, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        res = self._backend._lib.EVP_DigestVerify(evp_md_ctx, signature, len(signature), data, len(data))
        if res != 1:
            self._backend._consume_errors()
            raise exceptions.InvalidSignature


class _Ed448PrivateKey(Ed448PrivateKey):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self) -> Ed448PublicKey:
        buf = self._backend._ffi.new('unsigned char []', _ED448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED448_KEY_SIZE)
        public_bytes = self._backend._ffi.buffer(buf)[:]
        return self._backend.ed448_load_public_bytes(public_bytes)

    def sign(self, data: bytes) -> bytes:
        evp_md_ctx = self._backend._lib.EVP_MD_CTX_new()
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestSignInit(evp_md_ctx, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        buf = self._backend._ffi.new('unsigned char[]', _ED448_SIG_SIZE)
        buflen = self._backend._ffi.new('size_t *', len(buf))
        res = self._backend._lib.EVP_DigestSign(evp_md_ctx, buf, buflen, data, len(data))
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED448_SIG_SIZE)
        return self._backend._ffi.buffer(buf, buflen[0])[:]

    def private_bytes--- This code section failed: ---

 L. 123         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  COMPARE_OP               is

 L. 122        10  POP_JUMP_IF_TRUE     24  'to 24'

 L. 124        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  COMPARE_OP               is

 L. 122        22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L. 127        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  COMPARE_OP               is-not

 L. 126        34  POP_JUMP_IF_TRUE     60  'to 60'

 L. 128        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  COMPARE_OP               is-not

 L. 126        46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 129        48  LOAD_GLOBAL              isinstance

 L. 130        50  LOAD_FAST                'encryption_algorithm'

 L. 130        52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption

 L. 129        56  CALL_FUNCTION_2       2  ''

 L. 126        58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L. 133        60  LOAD_GLOBAL              ValueError

 L. 134        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'

 L. 133        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 138        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 140        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _private_key_bytes

 L. 141        82  LOAD_FAST                'encoding'

 L. 141        84  LOAD_FAST                'format'

 L. 141        86  LOAD_FAST                'encryption_algorithm'

 L. 141        88  LOAD_FAST                'self'

 L. 141        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _evp_pkey

 L. 141        94  LOAD_CONST               None

 L. 140        96  CALL_METHOD_6         6  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 98

    def _raw_private_bytes(self) -> bytes:
        buf = self._backend._ffi.new('unsigned char []', _ED448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_private_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED448_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED448_KEY_SIZE)[:]