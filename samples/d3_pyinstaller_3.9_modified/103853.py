# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\x448.py
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

    def public_bytes--- This code section failed: ---

 L.  26         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L.  25        10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  27        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L.  25        22  POP_JUMP_IF_FALSE    64  'to 64'
             24_0  COME_FROM            10  '10'

 L.  30        24  LOAD_FAST                'encoding'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                Encoding
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L.  29        34  POP_JUMP_IF_TRUE     48  'to 48'

 L.  31        36  LOAD_FAST                'format'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                PublicFormat
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L.  29        46  POP_JUMP_IF_FALSE    56  'to 56'
             48_0  COME_FROM            34  '34'

 L.  33        48  LOAD_GLOBAL              ValueError

 L.  34        50  LOAD_STR                 'When using Raw both encoding and format must be Raw'

 L.  33        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  37        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _raw_public_bytes
               60  CALL_METHOD_0         0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            22  '22'

 L.  39        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_METHOD              _public_key_bytes

 L.  40        70  LOAD_FAST                'encoding'
               72  LOAD_FAST                'format'
               74  LOAD_FAST                'self'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _evp_pkey
               80  LOAD_CONST               None

 L.  39        82  CALL_METHOD_5         5  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

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

 L.  78         0  LOAD_FAST                'encoding'
                2  LOAD_GLOBAL              serialization
                4  LOAD_ATTR                Encoding
                6  LOAD_ATTR                Raw
                8  <117>                 0  ''

 L.  77        10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  79        12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                PublicFormat
               18  LOAD_ATTR                Raw
               20  <117>                 0  ''

 L.  77        22  POP_JUMP_IF_FALSE    76  'to 76'
             24_0  COME_FROM            10  '10'

 L.  82        24  LOAD_FAST                'format'
               26  LOAD_GLOBAL              serialization
               28  LOAD_ATTR                PrivateFormat
               30  LOAD_ATTR                Raw
               32  <117>                 1  ''

 L.  81        34  POP_JUMP_IF_TRUE     60  'to 60'

 L.  83        36  LOAD_FAST                'encoding'
               38  LOAD_GLOBAL              serialization
               40  LOAD_ATTR                Encoding
               42  LOAD_ATTR                Raw
               44  <117>                 1  ''

 L.  81        46  POP_JUMP_IF_TRUE     60  'to 60'

 L.  84        48  LOAD_GLOBAL              isinstance

 L.  85        50  LOAD_FAST                'encryption_algorithm'
               52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                NoEncryption

 L.  84        56  CALL_FUNCTION_2       2  ''

 L.  81        58  POP_JUMP_IF_TRUE     68  'to 68'
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            34  '34'

 L.  88        60  LOAD_GLOBAL              ValueError

 L.  89        62  LOAD_STR                 'When using Raw both encoding and format must be Raw and encryption_algorithm must be NoEncryption()'

 L.  88        64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L.  93        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _raw_private_bytes
               72  CALL_METHOD_0         0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L.  95        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _private_key_bytes

 L.  96        82  LOAD_FAST                'encoding'
               84  LOAD_FAST                'format'
               86  LOAD_FAST                'encryption_algorithm'
               88  LOAD_FAST                'self'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _evp_pkey
               94  LOAD_CONST               None

 L.  95        96  CALL_METHOD_6         6  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _raw_private_bytes(self):
        buf = self._backend._ffi.new('unsigned char []', _X448_KEY_SIZE)
        buflen = self._backend._ffi.new('size_t *', _X448_KEY_SIZE)
        res = self._backend._lib.EVP_PKEY_get_raw_private_key(self._evp_pkey, buf, buflen)
        self._backend.openssl_assert(res == 1)
        self._backend.openssl_assert(buflen[0] == _X448_KEY_SIZE)
        return self._backend._ffi.buffer(buf, _X448_KEY_SIZE)[:]