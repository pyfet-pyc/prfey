# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_ecb.py
"""
Electronic Code Book (ECB) mode.
"""
__all__ = [
 'EcbMode']
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
raw_ecb_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_ecb', '\n                    int ECB_start_operation(void *cipher,\n                                            void **pResult);\n                    int ECB_encrypt(void *ecbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int ECB_decrypt(void *ecbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int ECB_stop_operation(void *state);\n                    ')

class EcbMode(object):
    __doc__ = '*Electronic Code Book (ECB)*.\n\n    This is the simplest encryption mode. Each of the plaintext blocks\n    is directly encrypted into a ciphertext block, independently of\n    any other block.\n\n    This mode is dangerous because it exposes frequency of symbols\n    in your plaintext. Other modes (e.g. *CBC*) should be used instead.\n\n    See `NIST SP800-38A`_ , Section 6.1.\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher):
        """Create a new block cipher, configured in ECB mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.
        """
        self._state = VoidPointer()
        result = raw_ecb_lib.ECB_start_operation(block_cipher.get(), self._state.address_of())
        if result:
            raise ValueError('Error %d while instantiating the ECB mode' % result)
        self._state = SmartPointer(self._state.get(), raw_ecb_lib.ECB_stop_operation)
        block_cipher.release()

    def encrypt--- This code section failed: ---

 L. 122         0  LOAD_FAST                'output'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 123         8  LOAD_GLOBAL              create_string_buffer
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'plaintext'
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'ciphertext'
               20  JUMP_FORWARD         74  'to 74'
             22_0  COME_FROM             6  '6'

 L. 125        22  LOAD_FAST                'output'
               24  STORE_FAST               'ciphertext'

 L. 127        26  LOAD_GLOBAL              is_writeable_buffer
               28  LOAD_FAST                'output'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_TRUE     42  'to 42'

 L. 128        34  LOAD_GLOBAL              TypeError
               36  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'

 L. 130        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'plaintext'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'output'
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               !=
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 131        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 132        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'plaintext'
               66  CALL_FUNCTION_1       1  ''

 L. 131        68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            56  '56'
             74_1  COME_FROM            20  '20'

 L. 134        74  LOAD_GLOBAL              raw_ecb_lib
               76  LOAD_METHOD              ECB_encrypt
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _state
               82  LOAD_METHOD              get
               84  CALL_METHOD_0         0  ''

 L. 135        86  LOAD_GLOBAL              c_uint8_ptr
               88  LOAD_FAST                'plaintext'
               90  CALL_FUNCTION_1       1  ''

 L. 136        92  LOAD_GLOBAL              c_uint8_ptr
               94  LOAD_FAST                'ciphertext'
               96  CALL_FUNCTION_1       1  ''

 L. 137        98  LOAD_GLOBAL              c_size_t
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'plaintext'
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''

 L. 134       108  CALL_METHOD_4         4  ''
              110  STORE_FAST               'result'

 L. 138       112  LOAD_FAST                'result'
              114  POP_JUMP_IF_FALSE   144  'to 144'

 L. 139       116  LOAD_FAST                'result'
              118  LOAD_CONST               3
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 140       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'Data must be aligned to block boundary in ECB mode'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

 L. 141       132  LOAD_GLOBAL              ValueError
              134  LOAD_STR                 'Error %d while encrypting in ECB mode'
              136  LOAD_FAST                'result'
              138  BINARY_MODULO    
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           114  '114'

 L. 143       144  LOAD_FAST                'output'
              146  LOAD_CONST               None
              148  <117>                 0  ''
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 144       152  LOAD_GLOBAL              get_raw_buffer
              154  LOAD_FAST                'ciphertext'
              156  CALL_FUNCTION_1       1  ''
              158  RETURN_VALUE     
            160_0  COME_FROM           150  '150'

 L. 146       160  LOAD_CONST               None
              162  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 177         0  LOAD_FAST                'output'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 178         8  LOAD_GLOBAL              create_string_buffer
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'ciphertext'
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'plaintext'
               20  JUMP_FORWARD         74  'to 74'
             22_0  COME_FROM             6  '6'

 L. 180        22  LOAD_FAST                'output'
               24  STORE_FAST               'plaintext'

 L. 182        26  LOAD_GLOBAL              is_writeable_buffer
               28  LOAD_FAST                'output'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_TRUE     42  'to 42'

 L. 183        34  LOAD_GLOBAL              TypeError
               36  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'

 L. 185        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'ciphertext'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'output'
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               !=
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 186        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 187        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'plaintext'
               66  CALL_FUNCTION_1       1  ''

 L. 186        68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            56  '56'
             74_1  COME_FROM            20  '20'

 L. 189        74  LOAD_GLOBAL              raw_ecb_lib
               76  LOAD_METHOD              ECB_decrypt
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _state
               82  LOAD_METHOD              get
               84  CALL_METHOD_0         0  ''

 L. 190        86  LOAD_GLOBAL              c_uint8_ptr
               88  LOAD_FAST                'ciphertext'
               90  CALL_FUNCTION_1       1  ''

 L. 191        92  LOAD_GLOBAL              c_uint8_ptr
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 192        98  LOAD_GLOBAL              c_size_t
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'ciphertext'
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''

 L. 189       108  CALL_METHOD_4         4  ''
              110  STORE_FAST               'result'

 L. 193       112  LOAD_FAST                'result'
              114  POP_JUMP_IF_FALSE   144  'to 144'

 L. 194       116  LOAD_FAST                'result'
              118  LOAD_CONST               3
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 195       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'Data must be aligned to block boundary in ECB mode'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

 L. 196       132  LOAD_GLOBAL              ValueError
              134  LOAD_STR                 'Error %d while decrypting in ECB mode'
              136  LOAD_FAST                'result'
              138  BINARY_MODULO    
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           114  '114'

 L. 198       144  LOAD_FAST                'output'
              146  LOAD_CONST               None
              148  <117>                 0  ''
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 199       152  LOAD_GLOBAL              get_raw_buffer
              154  LOAD_FAST                'plaintext'
              156  CALL_FUNCTION_1       1  ''
              158  RETURN_VALUE     
            160_0  COME_FROM           150  '150'

 L. 201       160  LOAD_CONST               None
              162  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _create_ecb_cipher(factory, **kwargs):
    """Instantiate a cipher object that performs ECB encryption/decryption.

    :Parameters:
      factory : module
        The underlying block cipher, a module from ``Crypto.Cipher``.

    All keywords are passed to the underlying block cipher.
    See the relevant documentation for details (at least ``key`` will need
    to be present"""
    cipher_state = factory._create_base_cipher(kwargs)
    if kwargs:
        raise TypeError('Unknown parameters for ECB: %s' % str(kwargs))
    return EcbMode(cipher_state)