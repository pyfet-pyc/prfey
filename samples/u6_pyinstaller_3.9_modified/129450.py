# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\cmac.py
from cryptography import utils
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.ciphers.modes import CBC

class _CMACContext(object):

    def __init__--- This code section failed: ---

 L.  18         0  LOAD_FAST                'backend'
                2  LOAD_METHOD              cmac_algorithm_supported
                4  LOAD_FAST                'algorithm'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     22  'to 22'

 L.  19        10  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  20        12  LOAD_STR                 'This backend does not support CMAC.'

 L.  21        14  LOAD_GLOBAL              _Reasons
               16  LOAD_ATTR                UNSUPPORTED_CIPHER

 L.  19        18  CALL_FUNCTION_2       2  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             8  '8'

 L.  24        22  LOAD_FAST                'backend'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _backend

 L.  25        28  LOAD_FAST                'algorithm'
               30  LOAD_ATTR                key
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _key

 L.  26        36  LOAD_FAST                'algorithm'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _algorithm

 L.  27        42  LOAD_FAST                'algorithm'
               44  LOAD_ATTR                block_size
               46  LOAD_CONST               8
               48  BINARY_FLOOR_DIVIDE
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _output_length

 L.  29        54  LOAD_FAST                'ctx'
               56  LOAD_CONST               None
               58  <117>                 0  ''
               60  POP_JUMP_IF_FALSE   222  'to 222'

 L.  30        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _backend
               66  LOAD_ATTR                _cipher_registry
               68  STORE_FAST               'registry'

 L.  31        70  LOAD_FAST                'registry'
               72  LOAD_GLOBAL              type
               74  LOAD_FAST                'algorithm'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              CBC
               80  BUILD_TUPLE_2         2 
               82  BINARY_SUBSCR    
               84  STORE_FAST               'adapter'

 L.  33        86  LOAD_FAST                'adapter'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _backend
               92  LOAD_FAST                'algorithm'
               94  LOAD_GLOBAL              CBC
               96  CALL_FUNCTION_3       3  ''
               98  STORE_FAST               'evp_cipher'

 L.  35       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _backend
              104  LOAD_ATTR                _lib
              106  LOAD_METHOD              CMAC_CTX_new
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'ctx'

 L.  37       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _backend
              116  LOAD_METHOD              openssl_assert
              118  LOAD_FAST                'ctx'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _backend
              124  LOAD_ATTR                _ffi
              126  LOAD_ATTR                NULL
              128  COMPARE_OP               !=
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.  38       134  LOAD_FAST                'self'
              136  LOAD_ATTR                _backend
              138  LOAD_ATTR                _ffi
              140  LOAD_METHOD              gc
              142  LOAD_FAST                'ctx'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                _backend
              148  LOAD_ATTR                _lib
              150  LOAD_ATTR                CMAC_CTX_free
              152  CALL_METHOD_2         2  ''
              154  STORE_FAST               'ctx'

 L.  40       156  LOAD_FAST                'self'
              158  LOAD_ATTR                _backend
              160  LOAD_ATTR                _ffi
              162  LOAD_METHOD              from_buffer
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _key
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'key_ptr'

 L.  41       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _backend
              176  LOAD_ATTR                _lib
              178  LOAD_METHOD              CMAC_Init

 L.  42       180  LOAD_FAST                'ctx'

 L.  43       182  LOAD_FAST                'key_ptr'

 L.  44       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _key
              190  CALL_FUNCTION_1       1  ''

 L.  45       192  LOAD_FAST                'evp_cipher'

 L.  46       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _backend
              198  LOAD_ATTR                _ffi
              200  LOAD_ATTR                NULL

 L.  41       202  CALL_METHOD_5         5  ''
              204  STORE_FAST               'res'

 L.  48       206  LOAD_FAST                'self'
              208  LOAD_ATTR                _backend
              210  LOAD_METHOD              openssl_assert
              212  LOAD_FAST                'res'
              214  LOAD_CONST               1
              216  COMPARE_OP               ==
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
            222_0  COME_FROM            60  '60'

 L.  50       222  LOAD_FAST                'ctx'
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _ctx

Parse error at or near `<117>' instruction at offset 58

    algorithm = utils.read_only_property('_algorithm')

    def update(self, data: bytes) -> None:
        res = self._backend._lib.CMAC_Update(self._ctx, data, len(data))
        self._backend.openssl_assert(res == 1)

    def finalize(self) -> bytes:
        buf = self._backend._ffi.new'unsigned char[]'self._output_length
        length = self._backend._ffi.new'size_t *'self._output_length
        res = self._backend._lib.CMAC_Final(self._ctx, buf, length)
        self._backend.openssl_assert(res == 1)
        self._ctx = None
        return self._backend._ffi.buffer(buf)[:]

    def copy(self) -> '_CMACContext':
        copied_ctx = self._backend._lib.CMAC_CTX_new
        copied_ctx = self._backend._ffi.gccopied_ctxself._backend._lib.CMAC_CTX_free
        res = self._backend._lib.CMAC_CTX_copycopied_ctxself._ctx
        self._backend.openssl_assert(res == 1)
        return _CMACContext((self._backend), (self._algorithm), ctx=copied_ctx)

    def verify(self, signature: bytes) -> None:
        digest = self.finalize
        if not constant_time.bytes_eqdigestsignature:
            raise InvalidSignature('Signature did not match digest.')