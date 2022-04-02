# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\x448.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.hazmat.backends.openssl.utils import _evp_pkey_derive
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey, X448PublicKey
_X448_KEY_SIZE = 56

@utils.register_interface(X448PublicKey)
class _X448PublicKey(object):

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
        buf = self._backend._ffi.new('unsigned char []', _X448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _X448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _X448_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _X448_KEY_SIZE)[:]


@utils.register_interface(X448PrivateKey)
class _X448PrivateKey(object):

    def __init__(self, backend, evp_pkey):
        self._backend = backend
        self._evp_pkey = evp_pkey

    def public_key(self):
        buf = self._backend._ffi.new('unsigned char []', _X448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _X448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_public_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _X448_KEY_SIZE)
        return self._backend.x448_load_public_bytes(buf)

    def exchange(self, peer_public_key):
        if not isinstance(peer_public_key, X448PublicKey):
            raise TypeError('peer_public_key must be X448PublicKey.')
        return _evp_pkey_derive(self._backend, self._evp_pkey, peer_public_key)

    def private_bytes--- This code section failed: ---

 L.  88         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  COMPARE_OP               is
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  89        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L.  92        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_TRUE     60  'to 60'

 L.  93        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L.  94        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L.  96        60  LOAD_GLOBAL              ValueError

 L.  97        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 101        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 104        76  LOAD_FAST                'encoding'
               78  LOAD_GLOBAL              serialization
               80  LOAD_ATTR                _PEM_DER
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   106  'to 106'

 L. 105        86  LOAD_FAST                'format'
               88  LOAD_GLOBAL              serialization
               90  LOAD_ATTR                PrivateFormat
               92  LOAD_ATTR                PKCS8
               94  COMPARE_OP               is-not
               96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 107        98  LOAD_GLOBAL              ValueError

 L. 108       100  LOAD_STR                 'format must be PKCS8 when encoding is PEM or DER'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            84  '84'

 L. 111       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _backend
              110  LOAD_METHOD              _private_key_bytes

 L. 112       112  LOAD_FAST                'encoding'
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
        buf = self._backend._ffi.new('unsigned char []', _X448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _X448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_private_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _X448_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _X448_KEY_SIZE)[:]