# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\hmac.py
from cryptography import utils
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import constant_time, hashes

class _HMACContext(hashes.HashContext):

    def __init__--- This code section failed: ---

 L.  19         0  LOAD_FAST                'algorithm'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _algorithm

 L.  20         6  LOAD_FAST                'backend'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _backend

 L.  22        12  LOAD_FAST                'ctx'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE   184  'to 184'

 L.  23        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _backend
               24  LOAD_ATTR                _lib
               26  LOAD_METHOD              HMAC_CTX_new
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'ctx'

 L.  24        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _backend
               36  LOAD_METHOD              openssl_assert
               38  LOAD_FAST                'ctx'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _backend
               44  LOAD_ATTR                _ffi
               46  LOAD_ATTR                NULL
               48  COMPARE_OP               !=
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  25        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _backend
               58  LOAD_ATTR                _ffi
               60  LOAD_METHOD              gc
               62  LOAD_FAST                'ctx'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_ATTR                _lib
               70  LOAD_ATTR                HMAC_CTX_free
               72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'ctx'

 L.  26        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              _evp_md_from_algorithm
               82  LOAD_FAST                'algorithm'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'evp_md'

 L.  27        88  LOAD_FAST                'evp_md'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _backend
               94  LOAD_ATTR                _ffi
               96  LOAD_ATTR                NULL
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   122  'to 122'

 L.  28       102  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  29       104  LOAD_STR                 '{} is not a supported hash on this backend'
              106  LOAD_METHOD              format

 L.  30       108  LOAD_FAST                'algorithm'
              110  LOAD_ATTR                name

 L.  29       112  CALL_METHOD_1         1  ''

 L.  32       114  LOAD_GLOBAL              _Reasons
              116  LOAD_ATTR                UNSUPPORTED_HASH

 L.  28       118  CALL_FUNCTION_2       2  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           100  '100'

 L.  34       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _backend
              126  LOAD_ATTR                _ffi
              128  LOAD_METHOD              from_buffer
              130  LOAD_FAST                'key'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'key_ptr'

 L.  35       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _backend
              140  LOAD_ATTR                _lib
              142  LOAD_METHOD              HMAC_Init_ex

 L.  36       144  LOAD_FAST                'ctx'
              146  LOAD_FAST                'key_ptr'
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'key'
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_FAST                'evp_md'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _backend
              160  LOAD_ATTR                _ffi
              162  LOAD_ATTR                NULL

 L.  35       164  CALL_METHOD_5         5  ''
              166  STORE_FAST               'res'

 L.  38       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _backend
              172  LOAD_METHOD              openssl_assert
              174  LOAD_FAST                'res'
              176  LOAD_CONST               0
              178  COMPARE_OP               !=
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
            184_0  COME_FROM            18  '18'

 L.  40       184  LOAD_FAST                'ctx'
              186  LOAD_FAST                'self'
              188  STORE_ATTR               _ctx

 L.  41       190  LOAD_FAST                'key'
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _key

Parse error at or near `<117>' instruction at offset 16

    algorithm = utils.read_only_property('_algorithm')

    def copy(self) -> '_HMACContext':
        copied_ctx = self._backend._lib.HMAC_CTX_new
        self._backend.openssl_assert(copied_ctx != self._backend._ffi.NULL)
        copied_ctx = self._backend._ffi.gccopied_ctxself._backend._lib.HMAC_CTX_free
        res = self._backend._lib.HMAC_CTX_copycopied_ctxself._ctx
        self._backend.openssl_assert(res != 0)
        return _HMACContext((self._backend),
          (self._key), (self.algorithm), ctx=copied_ctx)

    def update(self, data: bytes) -> None:
        data_ptr = self._backend._ffi.from_buffer(data)
        res = self._backend._lib.HMAC_Update(self._ctx, data_ptr, len(data))
        self._backend.openssl_assert(res != 0)

    def finalize(self) -> bytes:
        buf = self._backend._ffi.new'unsigned char[]'self._backend._lib.EVP_MAX_MD_SIZE
        outlen = self._backend._ffi.new('unsigned int *')
        res = self._backend._lib.HMAC_Final(self._ctx, buf, outlen)
        self._backend.openssl_assert(res != 0)
        self._backend.openssl_assert(outlen[0] == self.algorithm.digest_size)
        return self._backend._ffi.buffer(buf)[:outlen[0]]

    def verify(self, signature: bytes) -> None:
        digest = self.finalize
        if not constant_time.bytes_eqdigestsignature:
            raise InvalidSignature('Signature did not match digest.')