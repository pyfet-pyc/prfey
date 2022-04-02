# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\x25519.py
from __future__ import absolute_import, division, print_function
import warnings
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

    def public_bytes(self, encoding=None, format=None):
        if not encoding is None:
            if format is None:
                if encoding is not None or format is not None:
                    raise ValueError('Both encoding and format are required')
                else:
                    warnings.warn('public_bytes now requires encoding and format arguments. Support for calling without arguments will be removed in cryptography 2.7', utils.DeprecatedIn25)
                    encoding = serialization.Encoding.Raw
                    format = serialization.PublicFormat.Raw
        else:
            if encoding is serialization.Encoding.Raw or format is serialization.PublicFormat.Raw:
                if encoding is not serialization.Encoding.Raw or format is not serialization.PublicFormat.Raw:
                    raise ValueError('When using Raw both encoding and format must be Raw')
                return self._raw_public_bytes()
            if encoding in serialization._PEM_DER and format is not serialization.PublicFormat.SubjectPublicKeyInfo:
                raise ValueError('format must be SubjectPublicKeyInfo when encoding is PEM or DER')
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

 L. 108         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  COMPARE_OP               is
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L. 109        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L. 112        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_TRUE     60  'to 60'

 L. 113        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 114        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L. 116        60  LOAD_GLOBAL              ValueError

 L. 117        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 121        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 124        76  LOAD_FAST                'encoding'
               78  LOAD_GLOBAL              serialization
               80  LOAD_ATTR                _PEM_DER
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   106  'to 106'

 L. 125        86  LOAD_FAST                'format'
               88  LOAD_GLOBAL              serialization
               90  LOAD_ATTR                PrivateFormat
               92  LOAD_ATTR                PKCS8
               94  COMPARE_OP               is-not
               96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 127        98  LOAD_GLOBAL              ValueError

 L. 128       100  LOAD_STR                 'format must be PKCS8 when encoding is PEM or DER'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            84  '84'

 L. 131       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _backend
              110  LOAD_METHOD              _private_key_bytes

 L. 132       112  LOAD_FAST                'encoding'
              114  LOAD_FAST                'format'
              116  LOAD_FAST                'encryption_algorithm'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _evp_pkey
              122  LOAD_CONST               None
              124  CALL_METHOD_5         5  '5 positional arguments'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 68_0

    def _raw_private_bytes(self):
        bio = self._backend._create_mem_bio_gc()
        res = self._backend._lib.i2d_PKCS8PrivateKey_bio(bio, self._evp_pkey, self._backend._ffi.NULL, self._backend._ffi.NULL, 0, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(res == 1)
        pkcs8 = self._backend._read_mem_bio(bio)
        self._backend.openssl_assert(len(pkcs8) == 48)
        return pkcs8[-_X25519_KEY_SIZE:]