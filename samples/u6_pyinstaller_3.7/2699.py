# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: cryptography\hazmat\backends\openssl\x25519.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.hazmat.backends.openssl.utils import _evp_pkey_derive
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
_X25519_KEY_SIZE = 32

@utils.register_interface(X25519PublicKey)
class _X25519PublicKey(object):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_bytes(self, encoding, format):
        if encoding is serialization.Encoding.Raw or format is serialization.PublicFormat.Raw:
            if encoding is not serialization.Encoding.Raw or format is not serialization.PublicFormat.Raw:
                raise ValueError('When using Raw both encoding and format must be Raw')
            return self._raw_public_bytes()
        return self._backend._public_key_bytes(encoding, format, self, self._evp_pkey, None)

    def _raw_public_bytes(self):
        ucharpp = self._backend._ffi.new('unsigned char **')
        res = self._backend._lib.EVP_PKEY_get1_tls_encodedpoint(self._evp_pkey, ucharpp)
        self._backend.openssl_assert(res == 32)
        self._backend.openssl_assert(ucharpp[0] != self._backend._ffi.NULL)
        data = self._backend._ffi.gc(ucharpp[0], self._backend._lib.OPENSSL_free)
        return self._backend._ffi.buffer(data, res)[:]


@utils.register_interface(X25519PrivateKey)
class _X25519PrivateKey(object):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self):
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_PUBKEY_bio(bio, self._evp_pkey)
        self._backend.openssl_assert(res == 1)
        evp_pkey = self._backend._lib.d2i_PUBKEY_bio(bio, self._backend._ffi.NULL)
        self._backend.openssl_assert(evp_pkey != self._backend._ffi.NULL)
        evp_pkey = self._backend._ffi.gc(evp_pkey, self._backend._lib.EVP_PKEY_free)
        return _X25519PublicKey(self._backend, evp_pkey)

    def exchange(self, peer_public_key):
        if not isinstance(peer_public_key, X25519PublicKey):
            raise TypeError('peer_public_key must be X25519PublicKey.')
        return _evp_pkey_derive(self._backend, self._evp_pkey, peer_public_key)

    def private_bytes--- This code section failed: ---

 L.  84         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  COMPARE_OP               is
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  85        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L.  88        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_TRUE     60  'to 60'

 L.  89        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L.  90        48  LOAD_GLOBAL              isinstance

 L.  91        50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L.  94        60  LOAD_GLOBAL              ValueError

 L.  95        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L.  99        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 101        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _private_key_bytes

 L. 102        82  LOAD_FAST                'encoding'
               84  LOAD_FAST                'format'
               86  LOAD_FAST                'encryption_algorithm'
               88  LOAD_FAST                'self'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _evp_pkey
               94  LOAD_CONST               None
               96  CALL_METHOD_6         6  '6 positional arguments'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 68_0

    def _raw_private_bytes(self):
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_PKCS8PrivateKey_bio(bio, self._evp_pkey, self._backend._ffi.NULL, self._backend._ffi.NULL, 0, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(res == 1)
        pkcs8 = self._backend._read_mem_bio(bio)
        self._backend.openssl_assert(len(pkcs8) == 48)
        return pkcs8[-_X25519_KEY_SIZE:]