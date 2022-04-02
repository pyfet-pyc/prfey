# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_cbc.py
"""
Ciphertext Block Chaining (CBC) mode.
"""
__all__ = [
 'CbcMode']
from Crypto.Util.py3compat import _copy_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
from Crypto.Random import get_random_bytes
raw_cbc_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_cbc', '\n                int CBC_start_operation(void *cipher,\n                                        const uint8_t iv[],\n                                        size_t iv_len,\n                                        void **pResult);\n                int CBC_encrypt(void *cbcState,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n                int CBC_decrypt(void *cbcState,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n                int CBC_stop_operation(void *state);\n                ')

class CbcMode(object):
    __doc__ = '*Cipher-Block Chaining (CBC)*.\n\n    Each of the ciphertext blocks depends on the current\n    and all previous plaintext blocks.\n\n    An Initialization Vector (*IV*) is required.\n\n    See `NIST SP800-38A`_ , Section 6.2 .\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher, iv):
        """Create a new block cipher, configured in CBC mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.

          iv : bytes/bytearray/memoryview
            The initialization vector to use for encryption or decryption.
            It is as long as the cipher block.

            **The IV must be unpredictable**. Ideally it is picked randomly.

            Reusing the *IV* for encryptions performed with the same key
            compromises confidentiality.
        """
        self._state = VoidPointer()
        result = raw_cbc_lib.CBC_start_operation(block_cipher.get(), c_uint8_ptr(iv), c_size_t(len(iv)), self._state.address_of())
        if result:
            raise ValueError('Error %d while instantiating the CBC mode' % result)
        self._state = SmartPointer(self._state.get(), raw_cbc_lib.CBC_stop_operation)
        block_cipher.release()
        self.block_size = len(iv)
        self.iv = _copy_bytes(None, None, iv)
        self.IV = self.iv
        self._next = [
         self.encrypt, self.decrypt]

    def encrypt--- This code section failed: ---

 L. 161         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 162        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() cannot be called after decrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 163        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 165        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 166        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'plaintext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'ciphertext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 168        52  LOAD_FAST                'output'
               54  STORE_FAST               'ciphertext'

 L. 170        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 171        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 173        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'plaintext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 174        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 175        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 174        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 177       104  LOAD_GLOBAL              raw_cbc_lib
              106  LOAD_METHOD              CBC_encrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 178       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'plaintext'
              120  CALL_FUNCTION_1       1  ''

 L. 179       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'ciphertext'
              126  CALL_FUNCTION_1       1  ''

 L. 180       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'plaintext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 177       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 181       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   180  'to 180'

 L. 182       146  LOAD_FAST                'result'
              148  LOAD_CONST               3
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   168  'to 168'

 L. 183       154  LOAD_GLOBAL              ValueError
              156  LOAD_STR                 'Data must be padded to %d byte boundary in CBC mode'
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                block_size
              162  BINARY_MODULO    
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           152  '152'

 L. 184       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'Error %d while encrypting in CBC mode'
              172  LOAD_FAST                'result'
              174  BINARY_MODULO    
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           144  '144'

 L. 186       180  LOAD_FAST                'output'
              182  LOAD_CONST               None
              184  <117>                 0  ''
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L. 187       188  LOAD_GLOBAL              get_raw_buffer
              190  LOAD_FAST                'ciphertext'
              192  CALL_FUNCTION_1       1  ''
              194  RETURN_VALUE     
            196_0  COME_FROM           186  '186'

 L. 189       196  LOAD_CONST               None
              198  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 224         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 225        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() cannot be called after encrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 226        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 228        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 229        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'ciphertext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'plaintext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 231        52  LOAD_FAST                'output'
               54  STORE_FAST               'plaintext'

 L. 233        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 234        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 236        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'ciphertext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 237        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 238        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 237        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 240       104  LOAD_GLOBAL              raw_cbc_lib
              106  LOAD_METHOD              CBC_decrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 241       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'ciphertext'
              120  CALL_FUNCTION_1       1  ''

 L. 242       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'plaintext'
              126  CALL_FUNCTION_1       1  ''

 L. 243       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'ciphertext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 240       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 244       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   180  'to 180'

 L. 245       146  LOAD_FAST                'result'
              148  LOAD_CONST               3
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   168  'to 168'

 L. 246       154  LOAD_GLOBAL              ValueError
              156  LOAD_STR                 'Data must be padded to %d byte boundary in CBC mode'
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                block_size
              162  BINARY_MODULO    
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           152  '152'

 L. 247       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'Error %d while decrypting in CBC mode'
              172  LOAD_FAST                'result'
              174  BINARY_MODULO    
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           144  '144'

 L. 249       180  LOAD_FAST                'output'
              182  LOAD_CONST               None
              184  <117>                 0  ''
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L. 250       188  LOAD_GLOBAL              get_raw_buffer
              190  LOAD_FAST                'plaintext'
              192  CALL_FUNCTION_1       1  ''
              194  RETURN_VALUE     
            196_0  COME_FROM           186  '186'

 L. 252       196  LOAD_CONST               None
              198  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _create_cbc_cipher--- This code section failed: ---

 L. 274         0  LOAD_FAST                'factory'
                2  LOAD_METHOD              _create_base_cipher
                4  LOAD_FAST                'kwargs'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'cipher_state'

 L. 275        10  LOAD_FAST                'kwargs'
               12  LOAD_METHOD              pop
               14  LOAD_STR                 'IV'
               16  LOAD_CONST               None
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'iv'

 L. 276        22  LOAD_FAST                'kwargs'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'iv'
               28  LOAD_CONST               None
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'IV'

 L. 278        34  LOAD_CONST               (None, None)
               36  LOAD_FAST                'iv'
               38  LOAD_FAST                'IV'
               40  BUILD_TUPLE_2         2 
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 279        46  LOAD_GLOBAL              get_random_bytes
               48  LOAD_FAST                'factory'
               50  LOAD_ATTR                block_size
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'iv'
             56_0  COME_FROM            44  '44'

 L. 280        56  LOAD_FAST                'iv'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 281        64  LOAD_FAST                'IV'
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L. 282        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 "You must either use 'iv' or 'IV', not both"
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            62  '62'

 L. 284        82  LOAD_FAST                'IV'
               84  STORE_FAST               'iv'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            70  '70'

 L. 286        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'iv'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_FAST                'factory'
               94  LOAD_ATTR                block_size
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 287       100  LOAD_GLOBAL              ValueError
              102  LOAD_STR                 'Incorrect IV length (it must be %d bytes long)'

 L. 288       104  LOAD_FAST                'factory'
              106  LOAD_ATTR                block_size

 L. 287       108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            98  '98'

 L. 290       114  LOAD_FAST                'kwargs'
              116  POP_JUMP_IF_FALSE   134  'to 134'

 L. 291       118  LOAD_GLOBAL              TypeError
              120  LOAD_STR                 'Unknown parameters for CBC: %s'
              122  LOAD_GLOBAL              str
              124  LOAD_FAST                'kwargs'
              126  CALL_FUNCTION_1       1  ''
              128  BINARY_MODULO    
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           116  '116'

 L. 293       134  LOAD_GLOBAL              CbcMode
              136  LOAD_FAST                'cipher_state'
              138  LOAD_FAST                'iv'
              140  CALL_FUNCTION_2       2  ''
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 60