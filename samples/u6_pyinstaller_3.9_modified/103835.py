# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\aead.py
from __future__ import absolute_import, division, print_function
from cryptography.exceptions import InvalidTag
_ENCRYPT = 1
_DECRYPT = 0

def _aead_cipher_name--- This code section failed: ---

 L.  15         0  LOAD_CONST               0
                2  LOAD_CONST               ('AESCCM', 'AESGCM', 'ChaCha20Poly1305')
                4  IMPORT_NAME_ATTR         cryptography.hazmat.primitives.ciphers.aead
                6  IMPORT_FROM              AESCCM
                8  STORE_FAST               'AESCCM'
               10  IMPORT_FROM              AESGCM
               12  STORE_FAST               'AESGCM'
               14  IMPORT_FROM              ChaCha20Poly1305
               16  STORE_FAST               'ChaCha20Poly1305'
               18  POP_TOP          

 L.  21        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'cipher'
               24  LOAD_FAST                'ChaCha20Poly1305'
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L.  22        30  LOAD_CONST               b'chacha20-poly1305'
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L.  23        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'cipher'
               38  LOAD_FAST                'AESCCM'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    70  'to 70'

 L.  24        44  LOAD_STR                 'aes-{}-ccm'
               46  LOAD_METHOD              format
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'cipher'
               52  LOAD_ATTR                _key
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               8
               58  BINARY_MULTIPLY  
               60  CALL_METHOD_1         1  ''
               62  LOAD_METHOD              encode
               64  LOAD_STR                 'ascii'
               66  CALL_METHOD_1         1  ''
               68  RETURN_VALUE     
             70_0  COME_FROM            42  '42'

 L.  26        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'cipher'
               74  LOAD_FAST                'AESGCM'
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  <74>             
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L.  27        84  LOAD_STR                 'aes-{}-gcm'
               86  LOAD_METHOD              format
               88  LOAD_GLOBAL              len
               90  LOAD_FAST                'cipher'
               92  LOAD_ATTR                _key
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               8
               98  BINARY_MULTIPLY  
              100  CALL_METHOD_1         1  ''
              102  LOAD_METHOD              encode
              104  LOAD_STR                 'ascii'
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     

Parse error at or near `<74>' instruction at offset 80


def _aead_setup(backend, cipher_name, key, nonce, tag, tag_len, operation):
    evp_cipher = backend._lib.EVP_get_cipherbynamecipher_name
    backend.openssl_assert(evp_cipher != backend._ffi.NULL)
    ctx = backend._lib.EVP_CIPHER_CTX_new()
    ctx = backend._ffi.gc(ctx, backend._lib.EVP_CIPHER_CTX_free)
    res = backend._lib.EVP_CipherInit_ex(ctx, evp_cipher, backend._ffi.NULL, backend._ffi.NULL, backend._ffi.NULL, int(operation == _ENCRYPT))
    backend.openssl_assert(res != 0)
    res = backend._lib.EVP_CIPHER_CTX_set_key_length(ctx, len(key))
    backend.openssl_assert(res != 0)
    res = backend._lib.EVP_CIPHER_CTX_ctrl(ctx, backend._lib.EVP_CTRL_AEAD_SET_IVLEN, len(nonce), backend._ffi.NULL)
    backend.openssl_assert(res != 0)
    if operation == _DECRYPT:
        res = backend._lib.EVP_CIPHER_CTX_ctrl(ctx, backend._lib.EVP_CTRL_AEAD_SET_TAG, len(tag), tag)
        backend.openssl_assert(res != 0)
    else:
        if cipher_name.endswithb'-ccm':
            res = backend._lib.EVP_CIPHER_CTX_ctrl(ctx, backend._lib.EVP_CTRL_AEAD_SET_TAG, tag_len, backend._ffi.NULL)
            backend.openssl_assert(res != 0)
        nonce_ptr = backend._ffi.from_buffernonce
        key_ptr = backend._ffi.from_bufferkey
        res = backend._lib.EVP_CipherInit_ex(ctx, backend._ffi.NULL, backend._ffi.NULL, key_ptr, nonce_ptr, int(operation == _ENCRYPT))
        backend.openssl_assertres != 0
        return ctx


def _set_length(backend, ctx, data_len):
    intptr = backend._ffi.new'int *'
    res = backend._lib.EVP_CipherUpdate(ctx, backend._ffi.NULL, intptr, backend._ffi.NULL, data_len)
    backend.openssl_assert(res != 0)


def _process_aad(backend, ctx, associated_data):
    outlen = backend._ffi.new'int *'
    res = backend._lib.EVP_CipherUpdate(ctx, backend._ffi.NULL, outlen, associated_data, len(associated_data))
    backend.openssl_assert(res != 0)


def _process_data(backend, ctx, data):
    outlen = backend._ffi.new'int *'
    buf = backend._ffi.new('unsigned char[]', len(data))
    res = backend._lib.EVP_CipherUpdate(ctx, buf, outlen, data, len(data))
    backend.openssl_assertres != 0
    return backend._ffi.buffer(buf, outlen[0])[:]


def _encrypt(backend, cipher, nonce, data, associated_data, tag_length):
    from cryptography.hazmat.primitives.ciphers.aead import AESCCM
    cipher_name = _aead_cipher_name(cipher)
    ctx = _aead_setup(backend, cipher_name, cipher._key, nonce, None, tag_length, _ENCRYPT)
    if isinstancecipherAESCCM:
        _set_length(backend, ctx, len(data))
    _process_aad(backend, ctx, associated_data)
    processed_data = _process_data(backend, ctx, data)
    outlen = backend._ffi.new'int *'
    res = backend._lib.EVP_CipherFinal_ex(ctx, backend._ffi.NULL, outlen)
    backend.openssl_assert(res != 0)
    backend.openssl_assert(outlen[0] == 0)
    tag_buf = backend._ffi.new('unsigned char[]', tag_length)
    res = backend._lib.EVP_CIPHER_CTX_ctrl(ctx, backend._lib.EVP_CTRL_AEAD_GET_TAG, tag_length, tag_buf)
    backend.openssl_assert(res != 0)
    tag = backend._ffi.buffertag_buf[:]
    return processed_data + tag


def _decrypt(backend, cipher, nonce, data, associated_data, tag_length):
    from cryptography.hazmat.primitives.ciphers.aead import AESCCM
    if len(data) < tag_length:
        raise InvalidTag
    tag = data[-tag_length:]
    data = data[:-tag_length]
    cipher_name = _aead_cipher_name(cipher)
    ctx = _aead_setup(backend, cipher_name, cipher._key, nonce, tag, tag_length, _DECRYPT)
    if isinstancecipherAESCCM:
        _set_length(backend, ctx, len(data))
    _process_aad(backend, ctx, associated_data)
    if isinstancecipherAESCCM:
        outlen = backend._ffi.new'int *'
        buf = backend._ffi.new('unsigned char[]', len(data))
        res = backend._lib.EVP_CipherUpdate(ctx, buf, outlen, data, len(data))
        if res != 1:
            backend._consume_errors()
            raise InvalidTag
        processed_data = backend._ffi.buffer(buf, outlen[0])[:]
    else:
        processed_data = _process_data(backend, ctx, data)
        outlen = backend._ffi.new'int *'
        res = backend._lib.EVP_CipherFinal_ex(ctx, backend._ffi.NULL, outlen)
        if res == 0:
            backend._consume_errors()
            raise InvalidTag
        return processed_data