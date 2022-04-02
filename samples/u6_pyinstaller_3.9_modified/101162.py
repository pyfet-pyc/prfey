# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_cfb.py
"""
Counter Feedback (CFB) mode.
"""
__all__ = [
 'CfbMode']
from Crypto.Util.py3compat import _copy_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
from Crypto.Random import get_random_bytes
raw_cfb_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_cfb', '\n                    int CFB_start_operation(void *cipher,\n                                            const uint8_t iv[],\n                                            size_t iv_len,\n                                            size_t segment_len, /* In bytes */\n                                            void **pResult);\n                    int CFB_encrypt(void *cfbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CFB_decrypt(void *cfbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CFB_stop_operation(void *state);')

class CfbMode(object):
    __doc__ = '*Cipher FeedBack (CFB)*.\n\n    This mode is similar to CFB, but it transforms\n    the underlying block cipher into a stream cipher.\n\n    Plaintext and ciphertext are processed in *segments*\n    of **s** bits. The mode is therefore sometimes\n    labelled **s**-bit CFB.\n\n    An Initialization Vector (*IV*) is required.\n\n    See `NIST SP800-38A`_ , Section 6.3.\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher, iv, segment_size):
        """Create a new block cipher, configured in CFB mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.

          iv : bytes/bytearray/memoryview
            The initialization vector to use for encryption or decryption.
            It is as long as the cipher block.

            **The IV must be unpredictable**. Ideally it is picked randomly.

            Reusing the *IV* for encryptions performed with the same key
            compromises confidentiality.

          segment_size : integer
            The number of bytes the plaintext and ciphertext are segmented in.
        """
        self._state = VoidPointer()
        result = raw_cfb_lib.CFB_start_operation(block_cipher.get(), c_uint8_ptr(iv), c_size_t(len(iv)), c_size_t(segment_size), self._state.address_of())
        if result:
            raise ValueError('Error %d while instantiating the CFB mode' % result)
        self._state = SmartPointer(self._state.get(), raw_cfb_lib.CFB_stop_operation)
        block_cipher.release()
        self.block_size = len(iv)
        self.iv = _copy_bytes(None, None, iv)
        self.IV = self.iv
        self._next = [
         self.encrypt, self.decrypt]

    def encrypt--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 158        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() cannot be called after decrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 159        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 161        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 162        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'plaintext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'ciphertext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 164        52  LOAD_FAST                'output'
               54  STORE_FAST               'ciphertext'

 L. 166        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 167        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 169        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'plaintext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 170        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 171        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 170        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 173       104  LOAD_GLOBAL              raw_cfb_lib
              106  LOAD_METHOD              CFB_encrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 174       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'plaintext'
              120  CALL_FUNCTION_1       1  ''

 L. 175       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'ciphertext'
              126  CALL_FUNCTION_1       1  ''

 L. 176       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'plaintext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 173       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 177       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   158  'to 158'

 L. 178       146  LOAD_GLOBAL              ValueError
              148  LOAD_STR                 'Error %d while encrypting in CFB mode'
              150  LOAD_FAST                'result'
              152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           144  '144'

 L. 180       158  LOAD_FAST                'output'
              160  LOAD_CONST               None
              162  <117>                 0  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 181       166  LOAD_GLOBAL              get_raw_buffer
              168  LOAD_FAST                'ciphertext'
              170  CALL_FUNCTION_1       1  ''
              172  RETURN_VALUE     
            174_0  COME_FROM           164  '164'

 L. 183       174  LOAD_CONST               None
              176  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 218         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 219        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() cannot be called after encrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 220        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 222        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 223        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'ciphertext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'plaintext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 225        52  LOAD_FAST                'output'
               54  STORE_FAST               'plaintext'

 L. 227        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 228        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 230        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'ciphertext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 231        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 232        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 231        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 234       104  LOAD_GLOBAL              raw_cfb_lib
              106  LOAD_METHOD              CFB_decrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 235       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'ciphertext'
              120  CALL_FUNCTION_1       1  ''

 L. 236       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'plaintext'
              126  CALL_FUNCTION_1       1  ''

 L. 237       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'ciphertext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 234       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 238       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   158  'to 158'

 L. 239       146  LOAD_GLOBAL              ValueError
              148  LOAD_STR                 'Error %d while decrypting in CFB mode'
              150  LOAD_FAST                'result'
              152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           144  '144'

 L. 241       158  LOAD_FAST                'output'
              160  LOAD_CONST               None
              162  <117>                 0  ''
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L. 242       166  LOAD_GLOBAL              get_raw_buffer
              168  LOAD_FAST                'plaintext'
              170  CALL_FUNCTION_1       1  ''
              172  RETURN_VALUE     
            174_0  COME_FROM           164  '164'

 L. 244       174  LOAD_CONST               None
              176  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _create_cfb_cipher--- This code section failed: ---

 L. 270         0  LOAD_FAST                'factory'
                2  LOAD_METHOD              _create_base_cipher
                4  LOAD_FAST                'kwargs'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'cipher_state'

 L. 272        10  LOAD_FAST                'kwargs'
               12  LOAD_METHOD              pop
               14  LOAD_STR                 'IV'
               16  LOAD_CONST               None
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'iv'

 L. 273        22  LOAD_FAST                'kwargs'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'iv'
               28  LOAD_CONST               None
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'IV'

 L. 275        34  LOAD_CONST               (None, None)
               36  LOAD_FAST                'iv'
               38  LOAD_FAST                'IV'
               40  BUILD_TUPLE_2         2 
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 276        46  LOAD_GLOBAL              get_random_bytes
               48  LOAD_FAST                'factory'
               50  LOAD_ATTR                block_size
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'iv'
             56_0  COME_FROM            44  '44'

 L. 277        56  LOAD_FAST                'iv'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 278        64  LOAD_FAST                'IV'
               66  LOAD_CONST               None
               68  <117>                 1  ''
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L. 279        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 "You must either use 'iv' or 'IV', not both"
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            62  '62'

 L. 281        82  LOAD_FAST                'IV'
               84  STORE_FAST               'iv'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            70  '70'

 L. 283        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'iv'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_FAST                'factory'
               94  LOAD_ATTR                block_size
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 284       100  LOAD_GLOBAL              ValueError
              102  LOAD_STR                 'Incorrect IV length (it must be %d bytes long)'

 L. 285       104  LOAD_FAST                'factory'
              106  LOAD_ATTR                block_size

 L. 284       108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            98  '98'

 L. 287       114  LOAD_GLOBAL              divmod
              116  LOAD_FAST                'kwargs'
              118  LOAD_METHOD              pop
              120  LOAD_STR                 'segment_size'
              122  LOAD_CONST               8
              124  CALL_METHOD_2         2  ''
              126  LOAD_CONST               8
              128  CALL_FUNCTION_2       2  ''
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'segment_size_bytes'
              134  STORE_FAST               'rem'

 L. 288       136  LOAD_FAST                'segment_size_bytes'
              138  LOAD_CONST               0
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_TRUE    152  'to 152'
              144  LOAD_FAST                'rem'
              146  LOAD_CONST               0
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   160  'to 160'
            152_0  COME_FROM           142  '142'

 L. 289       152  LOAD_GLOBAL              ValueError
              154  LOAD_STR                 "'segment_size' must be positive and multiple of 8 bits"
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'

 L. 291       160  LOAD_FAST                'kwargs'
              162  POP_JUMP_IF_FALSE   180  'to 180'

 L. 292       164  LOAD_GLOBAL              TypeError
              166  LOAD_STR                 'Unknown parameters for CFB: %s'
              168  LOAD_GLOBAL              str
              170  LOAD_FAST                'kwargs'
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_MODULO    
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           162  '162'

 L. 293       180  LOAD_GLOBAL              CfbMode
              182  LOAD_FAST                'cipher_state'
              184  LOAD_FAST                'iv'
              186  LOAD_FAST                'segment_size_bytes'
              188  CALL_FUNCTION_3       3  ''
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 60