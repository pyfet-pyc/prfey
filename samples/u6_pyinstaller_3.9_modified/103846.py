# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\hashes.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import hashes

@utils.register_interface(hashes.HashContext)
class _HashContext(object):

    def __init__--- This code section failed: ---

 L.  16         0  LOAD_FAST                'algorithm'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _algorithm

 L.  18         6  LOAD_FAST                'backend'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _backend

 L.  20        12  LOAD_FAST                'ctx'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE   140  'to 140'

 L.  21        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _lib
               26  LOAD_METHOD              EVP_MD_CTX_new
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'ctx'

 L.  22        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _backend
               36  LOAD_ATTR                _ffi
               38  LOAD_METHOD              gc

 L.  23        40  LOAD_FAST                'ctx'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _backend
               46  LOAD_ATTR                _lib
               48  LOAD_ATTR                EVP_MD_CTX_free

 L.  22        50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'ctx'

 L.  25        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _backend
               58  LOAD_METHOD              _evp_md_from_algorithm
               60  LOAD_FAST                'algorithm'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'evp_md'

 L.  26        66  LOAD_FAST                'evp_md'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _backend
               72  LOAD_ATTR                _ffi
               74  LOAD_ATTR                NULL
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   100  'to 100'

 L.  27        80  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  28        82  LOAD_STR                 '{} is not a supported hash on this backend.'
               84  LOAD_METHOD              format

 L.  29        86  LOAD_FAST                'algorithm'
               88  LOAD_ATTR                name

 L.  28        90  CALL_METHOD_1         1  ''

 L.  31        92  LOAD_GLOBAL              _Reasons
               94  LOAD_ATTR                UNSUPPORTED_HASH

 L.  27        96  CALL_FUNCTION_2       2  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            78  '78'

 L.  33       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _backend
              104  LOAD_ATTR                _lib
              106  LOAD_METHOD              EVP_DigestInit_ex

 L.  34       108  LOAD_FAST                'ctx'
              110  LOAD_FAST                'evp_md'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _backend
              116  LOAD_ATTR                _ffi
              118  LOAD_ATTR                NULL

 L.  33       120  CALL_METHOD_3         3  ''
              122  STORE_FAST               'res'

 L.  36       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _backend
              128  LOAD_METHOD              openssl_assert
              130  LOAD_FAST                'res'
              132  LOAD_CONST               0
              134  COMPARE_OP               !=
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
            140_0  COME_FROM            18  '18'

 L.  38       140  LOAD_FAST                'ctx'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _ctx

Parse error at or near `<117>' instruction at offset 16

    algorithm = utils.read_only_property('_algorithm')

    def copy(self):
        copied_ctx = self._backend._lib.EVP_MD_CTX_new
        copied_ctx = self._backend._ffi.gccopied_ctxself._backend._lib.EVP_MD_CTX_free
        res = self._backend._lib.EVP_MD_CTX_copy_excopied_ctxself._ctx
        self._backend.openssl_assert(res != 0)
        return _HashContext((self._backend), (self.algorithm), ctx=copied_ctx)

    def update(self, data):
        data_ptr = self._backend._ffi.from_buffer(data)
        res = self._backend._lib.EVP_DigestUpdateself._ctxdata_ptrlen(data)
        self._backend.openssl_assert(res != 0)

    def finalize(self):
        if isinstanceself.algorithmhashes.ExtendableOutputFunction:
            return self._finalize_xof
        buf = self._backend._ffi.new'unsigned char[]'self._backend._lib.EVP_MAX_MD_SIZE
        outlen = self._backend._ffi.new('unsigned int *')
        res = self._backend._lib.EVP_DigestFinal_exself._ctxbufoutlen
        self._backend.openssl_assert(res != 0)
        self._backend.openssl_assert(outlen[0] == self.algorithm.digest_size)
        return self._backend._ffi.buffer(buf)[:outlen[0]]

    def _finalize_xof(self):
        buf = self._backend._ffi.new'unsigned char[]'self.algorithm.digest_size
        res = self._backend._lib.EVP_DigestFinalXOFself._ctxbufself.algorithm.digest_size
        self._backend.openssl_assert(res != 0)
        return self._backend._ffi.buffer(buf)[:self.algorithm.digest_size]