# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\ciphers\aead.py
from __future__ import absolute_import, division, print_function
import os
from cryptography import exceptions, utils
from cryptography.hazmat.backends.openssl import aead
import cryptography.hazmat.backends.openssl.backend as backend

class ChaCha20Poly1305(object):
    _MAX_SIZE = 4294967296

    def __init__(self, key):
        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm('ChaCha20Poly1305 is not supported by this version of OpenSSL', exceptions._Reasons.UNSUPPORTED_CIPHER)
        utils._check_byteslike('key', key)
        if len(key) != 32:
            raise ValueError('ChaCha20Poly1305 key must be 32 bytes.')
        self._key = key

    @classmethod
    def generate_key(cls):
        return os.urandom(32)

    def encrypt--- This code section failed: ---

 L.  35         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  36         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L.  38        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'data'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _MAX_SIZE
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     40  'to 40'
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'associated_data'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _MAX_SIZE
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    48  'to 48'
             40_0  COME_FROM            24  '24'

 L.  40        40  LOAD_GLOBAL              OverflowError

 L.  41        42  LOAD_STR                 'Data or associated data too long. Max 2**32 bytes'

 L.  40        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  44        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _check_params
               52  LOAD_FAST                'nonce'
               54  LOAD_FAST                'data'
               56  LOAD_FAST                'associated_data'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L.  45        62  LOAD_GLOBAL              aead
               64  LOAD_METHOD              _encrypt
               66  LOAD_GLOBAL              backend
               68  LOAD_FAST                'self'
               70  LOAD_FAST                'nonce'
               72  LOAD_FAST                'data'
               74  LOAD_FAST                'associated_data'
               76  LOAD_CONST               16
               78  CALL_METHOD_6         6  ''
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L.  48         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  49         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L.  51        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _check_params
               16  LOAD_FAST                'nonce'
               18  LOAD_FAST                'data'
               20  LOAD_FAST                'associated_data'
               22  CALL_METHOD_3         3  ''
               24  POP_TOP          

 L.  52        26  LOAD_GLOBAL              aead
               28  LOAD_METHOD              _decrypt
               30  LOAD_GLOBAL              backend
               32  LOAD_FAST                'self'
               34  LOAD_FAST                'nonce'
               36  LOAD_FAST                'data'
               38  LOAD_FAST                'associated_data'
               40  LOAD_CONST               16
               42  CALL_METHOD_6         6  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _check_params(self, nonce, data, associated_data):
        utils._check_byteslike('nonce', nonce)
        utils._check_bytes('data', data)
        utils._check_bytes('associated_data', associated_data)
        if len(nonce) != 12:
            raise ValueError('Nonce must be 12 bytes')


class AESCCM(object):
    _MAX_SIZE = 4294967296

    def __init__--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_byteslike
                4  LOAD_STR                 'key'
                6  LOAD_FAST                'key'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L.  67        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'key'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               (16, 24, 32)
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.  68        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'AESCCM key must be 128, 192, or 256 bits.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  70        32  LOAD_FAST                'key'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _key

 L.  71        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'tag_length'
               42  LOAD_GLOBAL              int
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L.  72        48  LOAD_GLOBAL              TypeError
               50  LOAD_STR                 'tag_length must be an integer'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  74        56  LOAD_FAST                'tag_length'
               58  LOAD_CONST               (4, 6, 8, 10, 12, 14, 16)
               60  <118>                 1  ''
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L.  75        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'Invalid tag_length'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L.  77        72  LOAD_FAST                'tag_length'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _tag_length

Parse error at or near `<118>' instruction at offset 20

    @classmethod
    def generate_key--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'bit_length'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.  82        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'bit_length must be an integer'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  84        18  LOAD_FAST                'bit_length'
               20  LOAD_CONST               (128, 192, 256)
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L.  85        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'bit_length must be 128, 192, or 256'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L.  87        34  LOAD_GLOBAL              os
               36  LOAD_METHOD              urandom
               38  LOAD_FAST                'bit_length'
               40  LOAD_CONST               8
               42  BINARY_FLOOR_DIVIDE
               44  CALL_METHOD_1         1  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def encrypt--- This code section failed: ---

 L.  90         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  91         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L.  93        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'data'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _MAX_SIZE
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     40  'to 40'
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'associated_data'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _MAX_SIZE
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    48  'to 48'
             40_0  COME_FROM            24  '24'

 L.  95        40  LOAD_GLOBAL              OverflowError

 L.  96        42  LOAD_STR                 'Data or associated data too long. Max 2**32 bytes'

 L.  95        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  99        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _check_params
               52  LOAD_FAST                'nonce'
               54  LOAD_FAST                'data'
               56  LOAD_FAST                'associated_data'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 100        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _validate_lengths
               66  LOAD_FAST                'nonce'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'data'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_METHOD_2         2  ''
               76  POP_TOP          

 L. 101        78  LOAD_GLOBAL              aead
               80  LOAD_METHOD              _encrypt

 L. 102        82  LOAD_GLOBAL              backend
               84  LOAD_FAST                'self'
               86  LOAD_FAST                'nonce'
               88  LOAD_FAST                'data'
               90  LOAD_FAST                'associated_data'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _tag_length

 L. 101        96  CALL_METHOD_6         6  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 106         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 107         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L. 109        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _check_params
               16  LOAD_FAST                'nonce'
               18  LOAD_FAST                'data'
               20  LOAD_FAST                'associated_data'
               22  CALL_METHOD_3         3  ''
               24  POP_TOP          

 L. 110        26  LOAD_GLOBAL              aead
               28  LOAD_METHOD              _decrypt

 L. 111        30  LOAD_GLOBAL              backend
               32  LOAD_FAST                'self'
               34  LOAD_FAST                'nonce'
               36  LOAD_FAST                'data'
               38  LOAD_FAST                'associated_data'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _tag_length

 L. 110        44  CALL_METHOD_6         6  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _validate_lengths(self, nonce, data_len):
        l_val = 15 - len(nonce)
        if 2 ** (8 * l_val) < data_len:
            raise ValueError('Data too long for nonce')

    def _check_params(self, nonce, data, associated_data):
        utils._check_byteslike('nonce', nonce)
        utils._check_bytes('data', data)
        utils._check_bytes('associated_data', associated_data)
        if not 7 <= len(nonce) <= 13:
            raise ValueError('Nonce must be between 7 and 13 bytes')


class AESGCM(object):
    _MAX_SIZE = 4294967296

    def __init__--- This code section failed: ---

 L. 133         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_byteslike
                4  LOAD_STR                 'key'
                6  LOAD_FAST                'key'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 134        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'key'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               (16, 24, 32)
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 135        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'AESGCM key must be 128, 192, or 256 bits.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 137        32  LOAD_FAST                'key'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _key

Parse error at or near `<118>' instruction at offset 20

    @classmethod
    def generate_key--- This code section failed: ---

 L. 141         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'bit_length'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 142        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'bit_length must be an integer'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 144        18  LOAD_FAST                'bit_length'
               20  LOAD_CONST               (128, 192, 256)
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 145        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'bit_length must be 128, 192, or 256'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 147        34  LOAD_GLOBAL              os
               36  LOAD_METHOD              urandom
               38  LOAD_FAST                'bit_length'
               40  LOAD_CONST               8
               42  BINARY_FLOOR_DIVIDE
               44  CALL_METHOD_1         1  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def encrypt--- This code section failed: ---

 L. 150         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 151         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L. 153        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'data'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _MAX_SIZE
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     40  'to 40'
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'associated_data'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _MAX_SIZE
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    48  'to 48'
             40_0  COME_FROM            24  '24'

 L. 155        40  LOAD_GLOBAL              OverflowError

 L. 156        42  LOAD_STR                 'Data or associated data too long. Max 2**32 bytes'

 L. 155        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 159        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _check_params
               52  LOAD_FAST                'nonce'
               54  LOAD_FAST                'data'
               56  LOAD_FAST                'associated_data'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 160        62  LOAD_GLOBAL              aead
               64  LOAD_METHOD              _encrypt
               66  LOAD_GLOBAL              backend
               68  LOAD_FAST                'self'
               70  LOAD_FAST                'nonce'
               72  LOAD_FAST                'data'
               74  LOAD_FAST                'associated_data'
               76  LOAD_CONST               16
               78  CALL_METHOD_6         6  ''
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 163         0  LOAD_FAST                'associated_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 164         8  LOAD_CONST               b''
               10  STORE_FAST               'associated_data'
             12_0  COME_FROM             6  '6'

 L. 166        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _check_params
               16  LOAD_FAST                'nonce'
               18  LOAD_FAST                'data'
               20  LOAD_FAST                'associated_data'
               22  CALL_METHOD_3         3  ''
               24  POP_TOP          

 L. 167        26  LOAD_GLOBAL              aead
               28  LOAD_METHOD              _decrypt
               30  LOAD_GLOBAL              backend
               32  LOAD_FAST                'self'
               34  LOAD_FAST                'nonce'
               36  LOAD_FAST                'data'
               38  LOAD_FAST                'associated_data'
               40  LOAD_CONST               16
               42  CALL_METHOD_6         6  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _check_params(self, nonce, data, associated_data):
        utils._check_byteslike('nonce', nonce)
        utils._check_bytes('data', data)
        utils._check_bytes('associated_data', associated_data)
        if len(nonce) < 8 or (len(nonce) > 128):
            raise ValueError('Nonce must be between 8 and 128 bytes')