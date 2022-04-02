# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\ed25519.py
from __future__ import absolute_import, division, print_function
from cryptography import exceptions, utils
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey, _ED25519_KEY_SIZE, _ED25519_SIG_SIZE

@utils.register_interface(Ed25519PublicKey)
class _Ed25519PublicKey(object):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_bytes(self, encoding, format):
        if encoding is serialization.Encoding.Raw or format is serialization.PublicFormat.Raw:
            if encoding is not serialization.Encoding.Raw or format is not serialization.PublicFormat.Raw:
                raise ValueError('When using Raw both encoding and format must be Raw')
            return self._raw_public_bytes()
        if encoding in serialization._PEM_DER:
            if format is not serialization.PublicFormat.SubjectPublicKeyInfo:
                raise ValueError('format must be SubjectPublicKeyInfo when encoding is PEM or DER')
        return self._backend._public_key_bytes(encoding, format, self, self._evp_pkey, None)

    def _raw_public_bytes(self):
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED25519_KEY_SIZE)[:]

    def verify(self, signature, data):
        evp_md_ctx = self._backend._lib.Cryptography_EVP_MD_CTX_new()
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.Cryptography_EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestVerifyInit(evp_md_ctx, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        res = self._backend._lib.EVP_DigestVerify(evp_md_ctx, signature, len(signature), data, len(data))
        if res != 1:
            self._backend._consume_errors()
            raise exceptions.InvalidSignature


@utils.register_interface(Ed25519PrivateKey)
class _Ed25519PrivateKey(object):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self):
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        public_bytes = self._backend._ffi.buffer(buf)[:]
        return self._backend.ed25519_load_public_bytes(public_bytes)

    def sign(self, data):
        evp_md_ctx = self._backend._lib.Cryptography_EVP_MD_CTX_new()
        self._backend.openssl_assert(evp_md_ctx != self._backend._ffi.NULL)
        evp_md_ctx = self._backend._ffi.gc(evp_md_ctx, self._backend._lib.Cryptography_EVP_MD_CTX_free)
        res = self._backend._lib.EVP_DigestSignInit(evp_md_ctx, self._backend._ffi.NULL, self._backend._ffi.NULL, self._backend._ffi.NULL, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        buf = self._backend._ffi.new('unsigned char[]', _ED25519_SIG_SIZE)
        buflen = self._backend._ffi.new('size_t *', len(buf))
        res = self._backend._lib.EVP_DigestSign(evp_md_ctx, buf, buflen, data, len(data))
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_SIG_SIZE)
        return self._backend._ffi.buffer(buf, buflen[0])[:]

    def private_bytes--- This code section failed: ---

 L. 116         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  COMPARE_OP               is

 L. 115        10  POP_JUMP_IF_TRUE     24  'to 24'

 L. 117        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  COMPARE_OP               is

 L. 115        22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L. 120        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  COMPARE_OP               is-not

 L. 119        34  POP_JUMP_IF_TRUE     60  'to 60'

 L. 121        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  COMPARE_OP               is-not

 L. 119        46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 122        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption
               56  CALL_FUNCTION_2       2  ''

 L. 119        58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L. 124        60  LOAD_GLOBAL              ValueError

 L. 125        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'

 L. 124        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 129        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 132        76  LOAD_FAST                'encoding'
               78  LOAD_GLOBAL              serialization
               80  LOAD_ATTR                _PEM_DER
               82  COMPARE_OP               in

 L. 131        84  POP_JUMP_IF_FALSE   106  'to 106'

 L. 133        86  LOAD_FAST                'format'
               88  LOAD_GLOBAL              serialization
               90  LOAD_ATTR                PrivateFormat
               92  LOAD_ATTR                PKCS8
               94  COMPARE_OP               is-not

 L. 131        96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 135        98  LOAD_GLOBAL              ValueError

 L. 136       100  LOAD_STR                 'format must be PKCS8 when encoding is PEM or DER'

 L. 135       102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            84  '84'

 L. 139       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _backend
              110  LOAD_METHOD              _private_key_bytes

 L. 140       112  LOAD_FAST                'encoding'

 L. 140       114  LOAD_FAST                'format'

 L. 140       116  LOAD_FAST                'encryption_algorithm'

 L. 140       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _evp_pkey

 L. 140       122  LOAD_CONST               None

 L. 139       124  CALL_METHOD_5         5  ''
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 126

    def _raw_private_bytes(self):
        buf = self._backend._ffi.new('unsigned char []', _ED25519_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _ED25519_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_private_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _ED25519_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _ED25519_KEY_SIZE)[:]