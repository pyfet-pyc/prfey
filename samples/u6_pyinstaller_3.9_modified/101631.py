# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_ctr.py
"""
Counter (CTR) mode.
"""
__all__ = [
 'CtrMode']
import struct
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
from Crypto.Random import get_random_bytes
from Crypto.Util.py3compat import _copy_bytes, is_native_int
from Crypto.Util.number import long_to_bytes
raw_ctr_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_ctr', '\n                    int CTR_start_operation(void *cipher,\n                                            uint8_t   initialCounterBlock[],\n                                            size_t    initialCounterBlock_len,\n                                            size_t    prefix_len,\n                                            unsigned  counter_len,\n                                            unsigned  littleEndian,\n                                            void **pResult);\n                    int CTR_encrypt(void *ctrState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CTR_decrypt(void *ctrState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CTR_stop_operation(void *ctrState);')

class CtrMode(object):
    __doc__ = '*CounTeR (CTR)* mode.\n\n    This mode is very similar to ECB, in that\n    encryption of one block is done independently of all other blocks.\n\n    Unlike ECB, the block *position* contributes to the encryption\n    and no information leaks about symbol frequency.\n\n    Each message block is associated to a *counter* which\n    must be unique across all messages that get encrypted\n    with the same key (not just within the same message).\n    The counter is as big as the block size.\n\n    Counters can be generated in several ways. The most\n    straightword one is to choose an *initial counter block*\n    (which can be made public, similarly to the *IV* for the\n    other modes) and increment its lowest **m** bits by one\n    (modulo *2^m*) for each block. In most cases, **m** is\n    chosen to be half the block size.\n\n    See `NIST SP800-38A`_, Section 6.5 (for the mode) and\n    Appendix B (for how to manage the *initial counter block*).\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher, initial_counter_block, prefix_len, counter_len, little_endian):
        """Create a new block cipher, configured in CTR mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.

          initial_counter_block : bytes/bytearray/memoryview
            The initial plaintext to use to generate the key stream.

            It is as large as the cipher block, and it embeds
            the initial value of the counter.

            This value must not be reused.
            It shall contain a nonce or a random component.
            Reusing the *initial counter block* for encryptions
            performed with the same key compromises confidentiality.

          prefix_len : integer
            The amount of bytes at the beginning of the counter block
            that never change.

          counter_len : integer
            The length in bytes of the counter embedded in the counter
            block.

          little_endian : boolean
            True if the counter in the counter block is an integer encoded
            in little endian mode. If False, it is big endian.
        """
        if len(initial_counter_block) == prefix_len + counter_len:
            self.nonce = _copy_bytes(None, prefix_len, initial_counter_block)
        self._state = VoidPointer()
        result = raw_ctr_lib.CTR_start_operation(block_cipher.get(), c_uint8_ptr(initial_counter_block), c_size_t(len(initial_counter_block)), c_size_t(prefix_len), counter_len, little_endian, self._state.address_of())
        if result:
            raise ValueError('Error %X while instantiating the CTR mode' % result)
        self._state = SmartPointer(self._state.get(), raw_ctr_lib.CTR_stop_operation)
        block_cipher.release()
        self.block_size = len(initial_counter_block)
        self._next = [
         self.encrypt, self.decrypt]

    def encrypt--- This code section failed: ---

 L. 184         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 185        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() cannot be called after decrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 186        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 188        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 189        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'plaintext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'ciphertext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 191        52  LOAD_FAST                'output'
               54  STORE_FAST               'ciphertext'

 L. 193        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 194        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 196        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'plaintext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 197        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 198        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 197        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 200       104  LOAD_GLOBAL              raw_ctr_lib
              106  LOAD_METHOD              CTR_encrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 201       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'plaintext'
              120  CALL_FUNCTION_1       1  ''

 L. 202       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'ciphertext'
              126  CALL_FUNCTION_1       1  ''

 L. 203       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'plaintext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 200       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 204       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   174  'to 174'

 L. 205       146  LOAD_FAST                'result'
              148  LOAD_CONST               393218
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 206       154  LOAD_GLOBAL              OverflowError
              156  LOAD_STR                 'The counter has wrapped around in CTR mode'
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'

 L. 208       162  LOAD_GLOBAL              ValueError
              164  LOAD_STR                 'Error %X while encrypting in CTR mode'
              166  LOAD_FAST                'result'
              168  BINARY_MODULO    
              170  CALL_FUNCTION_1       1  ''
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           144  '144'

 L. 210       174  LOAD_FAST                'output'
              176  LOAD_CONST               None
              178  <117>                 0  ''
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 211       182  LOAD_GLOBAL              get_raw_buffer
              184  LOAD_FAST                'ciphertext'
              186  CALL_FUNCTION_1       1  ''
              188  RETURN_VALUE     
            190_0  COME_FROM           180  '180'

 L. 213       190  LOAD_CONST               None
              192  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 248         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 249        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() cannot be called after encrypt()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 250        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 252        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 253        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'ciphertext'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'plaintext'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 255        52  LOAD_FAST                'output'
               54  STORE_FAST               'plaintext'

 L. 257        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 258        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 260        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'ciphertext'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 261        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 262        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'plaintext'
               96  CALL_FUNCTION_1       1  ''

 L. 261        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 264       104  LOAD_GLOBAL              raw_ctr_lib
              106  LOAD_METHOD              CTR_decrypt
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _state
              112  LOAD_METHOD              get
              114  CALL_METHOD_0         0  ''

 L. 265       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'ciphertext'
              120  CALL_FUNCTION_1       1  ''

 L. 266       122  LOAD_GLOBAL              c_uint8_ptr
              124  LOAD_FAST                'plaintext'
              126  CALL_FUNCTION_1       1  ''

 L. 267       128  LOAD_GLOBAL              c_size_t
              130  LOAD_GLOBAL              len
              132  LOAD_FAST                'ciphertext'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_FUNCTION_1       1  ''

 L. 264       138  CALL_METHOD_4         4  ''
              140  STORE_FAST               'result'

 L. 268       142  LOAD_FAST                'result'
              144  POP_JUMP_IF_FALSE   174  'to 174'

 L. 269       146  LOAD_FAST                'result'
              148  LOAD_CONST               393218
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 270       154  LOAD_GLOBAL              OverflowError
              156  LOAD_STR                 'The counter has wrapped around in CTR mode'
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'

 L. 272       162  LOAD_GLOBAL              ValueError
              164  LOAD_STR                 'Error %X while decrypting in CTR mode'
              166  LOAD_FAST                'result'
              168  BINARY_MODULO    
              170  CALL_FUNCTION_1       1  ''
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           144  '144'

 L. 274       174  LOAD_FAST                'output'
              176  LOAD_CONST               None
              178  <117>                 0  ''
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 275       182  LOAD_GLOBAL              get_raw_buffer
              184  LOAD_FAST                'plaintext'
              186  CALL_FUNCTION_1       1  ''
              188  RETURN_VALUE     
            190_0  COME_FROM           180  '180'

 L. 277       190  LOAD_CONST               None
              192  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _create_ctr_cipher--- This code section failed: ---

 L. 317         0  LOAD_FAST                'factory'
                2  LOAD_METHOD              _create_base_cipher
                4  LOAD_FAST                'kwargs'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'cipher_state'

 L. 319        10  LOAD_FAST                'kwargs'
               12  LOAD_METHOD              pop
               14  LOAD_STR                 'counter'
               16  LOAD_CONST               None
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'counter'

 L. 320        22  LOAD_FAST                'kwargs'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'nonce'
               28  LOAD_CONST               None
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'nonce'

 L. 321        34  LOAD_FAST                'kwargs'
               36  LOAD_METHOD              pop
               38  LOAD_STR                 'initial_value'
               40  LOAD_CONST               None
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'initial_value'

 L. 322        46  LOAD_FAST                'kwargs'
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L. 323        50  LOAD_GLOBAL              TypeError
               52  LOAD_STR                 'Invalid parameters for CTR mode: %s'
               54  LOAD_GLOBAL              str
               56  LOAD_FAST                'kwargs'
               58  CALL_FUNCTION_1       1  ''
               60  BINARY_MODULO    
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            48  '48'

 L. 325        66  LOAD_FAST                'counter'
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    94  'to 94'
               74  LOAD_FAST                'nonce'
               76  LOAD_FAST                'initial_value'
               78  BUILD_TUPLE_2         2 
               80  LOAD_CONST               (None, None)
               82  COMPARE_OP               !=
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 326        86  LOAD_GLOBAL              TypeError
               88  LOAD_STR                 "'counter' and 'nonce'/'initial_value' are mutually exclusive"
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            84  '84'
             94_1  COME_FROM            72  '72'

 L. 329        94  LOAD_FAST                'counter'
               96  LOAD_CONST               None
               98  <117>                 0  ''
          100_102  POP_JUMP_IF_FALSE   308  'to 308'

 L. 331       104  LOAD_FAST                'nonce'
              106  LOAD_CONST               None
              108  <117>                 0  ''
              110  POP_JUMP_IF_FALSE   146  'to 146'

 L. 332       112  LOAD_FAST                'factory'
              114  LOAD_ATTR                block_size
              116  LOAD_CONST               16
              118  COMPARE_OP               <
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 333       122  LOAD_GLOBAL              TypeError
              124  LOAD_STR                 'Impossible to create a safe nonce for short block sizes'
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           120  '120'

 L. 335       130  LOAD_GLOBAL              get_random_bytes
              132  LOAD_FAST                'factory'
              134  LOAD_ATTR                block_size
              136  LOAD_CONST               2
              138  BINARY_FLOOR_DIVIDE
              140  CALL_FUNCTION_1       1  ''
              142  STORE_FAST               'nonce'
              144  JUMP_FORWARD        168  'to 168'
            146_0  COME_FROM           110  '110'

 L. 337       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'nonce'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_FAST                'factory'
              154  LOAD_ATTR                block_size
              156  COMPARE_OP               >=
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 338       160  LOAD_GLOBAL              ValueError
              162  LOAD_STR                 'Nonce is too long'
              164  CALL_FUNCTION_1       1  ''
              166  RAISE_VARARGS_1       1  'exception instance'
            168_0  COME_FROM           158  '158'
            168_1  COME_FROM           144  '144'

 L. 341       168  LOAD_FAST                'factory'
              170  LOAD_ATTR                block_size
              172  LOAD_GLOBAL              len
              174  LOAD_FAST                'nonce'
              176  CALL_FUNCTION_1       1  ''
              178  BINARY_SUBTRACT  
              180  STORE_FAST               'counter_len'

 L. 343       182  LOAD_FAST                'initial_value'
              184  LOAD_CONST               None
              186  <117>                 0  ''
              188  POP_JUMP_IF_FALSE   194  'to 194'

 L. 344       190  LOAD_CONST               0
              192  STORE_FAST               'initial_value'
            194_0  COME_FROM           188  '188'

 L. 346       194  LOAD_GLOBAL              is_native_int
              196  LOAD_FAST                'initial_value'
              198  CALL_FUNCTION_1       1  ''
              200  POP_JUMP_IF_FALSE   246  'to 246'

 L. 347       202  LOAD_CONST               1
              204  LOAD_FAST                'counter_len'
              206  LOAD_CONST               8
              208  BINARY_MULTIPLY  
              210  BINARY_LSHIFT    
              212  LOAD_CONST               1
              214  BINARY_SUBTRACT  
              216  LOAD_FAST                'initial_value'
              218  COMPARE_OP               <
              220  POP_JUMP_IF_FALSE   230  'to 230'

 L. 348       222  LOAD_GLOBAL              ValueError
              224  LOAD_STR                 'Initial counter value is too large'
              226  CALL_FUNCTION_1       1  ''
              228  RAISE_VARARGS_1       1  'exception instance'
            230_0  COME_FROM           220  '220'

 L. 349       230  LOAD_FAST                'nonce'
              232  LOAD_GLOBAL              long_to_bytes
              234  LOAD_FAST                'initial_value'
              236  LOAD_FAST                'counter_len'
              238  CALL_FUNCTION_2       2  ''
              240  BINARY_ADD       
              242  STORE_FAST               'initial_counter_block'
              244  JUMP_FORWARD        288  'to 288'
            246_0  COME_FROM           200  '200'

 L. 351       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'initial_value'
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_FAST                'counter_len'
              254  COMPARE_OP               !=
          256_258  POP_JUMP_IF_FALSE   280  'to 280'

 L. 352       260  LOAD_GLOBAL              ValueError
              262  LOAD_STR                 'Incorrect length for counter byte string (%d bytes, expected %d)'

 L. 353       264  LOAD_GLOBAL              len
              266  LOAD_FAST                'initial_value'
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_FAST                'counter_len'
              272  BUILD_TUPLE_2         2 

 L. 352       274  BINARY_MODULO    
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
            280_0  COME_FROM           256  '256'

 L. 354       280  LOAD_FAST                'nonce'
              282  LOAD_FAST                'initial_value'
              284  BINARY_ADD       
              286  STORE_FAST               'initial_counter_block'
            288_0  COME_FROM           244  '244'

 L. 356       288  LOAD_GLOBAL              CtrMode
              290  LOAD_FAST                'cipher_state'

 L. 357       292  LOAD_FAST                'initial_counter_block'

 L. 358       294  LOAD_GLOBAL              len
              296  LOAD_FAST                'nonce'
              298  CALL_FUNCTION_1       1  ''

 L. 359       300  LOAD_FAST                'counter_len'

 L. 360       302  LOAD_CONST               False

 L. 356       304  CALL_FUNCTION_5       5  ''
              306  RETURN_VALUE     
            308_0  COME_FROM           100  '100'

 L. 366       308  LOAD_GLOBAL              dict
              310  LOAD_FAST                'counter'
              312  CALL_FUNCTION_1       1  ''
              314  STORE_FAST               '_counter'

 L. 367       316  SETUP_FINALLY       372  'to 372'

 L. 368       318  LOAD_FAST                '_counter'
              320  LOAD_METHOD              pop
              322  LOAD_STR                 'counter_len'
              324  CALL_METHOD_1         1  ''
              326  STORE_FAST               'counter_len'

 L. 369       328  LOAD_FAST                '_counter'
              330  LOAD_METHOD              pop
              332  LOAD_STR                 'prefix'
              334  CALL_METHOD_1         1  ''
              336  STORE_FAST               'prefix'

 L. 370       338  LOAD_FAST                '_counter'
              340  LOAD_METHOD              pop
              342  LOAD_STR                 'suffix'
              344  CALL_METHOD_1         1  ''
              346  STORE_FAST               'suffix'

 L. 371       348  LOAD_FAST                '_counter'
              350  LOAD_METHOD              pop
              352  LOAD_STR                 'initial_value'
              354  CALL_METHOD_1         1  ''
              356  STORE_FAST               'initial_value'

 L. 372       358  LOAD_FAST                '_counter'
              360  LOAD_METHOD              pop
              362  LOAD_STR                 'little_endian'
              364  CALL_METHOD_1         1  ''
              366  STORE_FAST               'little_endian'
              368  POP_BLOCK        
              370  JUMP_FORWARD        400  'to 400'
            372_0  COME_FROM_FINALLY   316  '316'

 L. 373       372  DUP_TOP          
              374  LOAD_GLOBAL              KeyError
          376_378  <121>               398  ''
              380  POP_TOP          
              382  POP_TOP          
              384  POP_TOP          

 L. 374       386  LOAD_GLOBAL              TypeError
              388  LOAD_STR                 'Incorrect counter object (use Crypto.Util.Counter.new)'
              390  CALL_FUNCTION_1       1  ''
              392  RAISE_VARARGS_1       1  'exception instance'
              394  POP_EXCEPT       
              396  JUMP_FORWARD        400  'to 400'
              398  <48>             
            400_0  COME_FROM           396  '396'
            400_1  COME_FROM           370  '370'

 L. 378       400  BUILD_LIST_0          0 
              402  STORE_FAST               'words'

 L. 379       404  LOAD_FAST                'initial_value'
              406  LOAD_CONST               0
              408  COMPARE_OP               >
          410_412  POP_JUMP_IF_FALSE   448  'to 448'

 L. 380       414  LOAD_FAST                'words'
              416  LOAD_METHOD              append
              418  LOAD_GLOBAL              struct
              420  LOAD_METHOD              pack
              422  LOAD_STR                 'B'
              424  LOAD_FAST                'initial_value'
              426  LOAD_CONST               255
              428  BINARY_AND       
              430  CALL_METHOD_2         2  ''
              432  CALL_METHOD_1         1  ''
              434  POP_TOP          

 L. 381       436  LOAD_FAST                'initial_value'
              438  LOAD_CONST               8
              440  INPLACE_RSHIFT   
              442  STORE_FAST               'initial_value'
          444_446  JUMP_BACK           404  'to 404'
            448_0  COME_FROM           410  '410'

 L. 382       448  LOAD_FAST                'words'
              450  LOAD_CONST               b'\x00'
              452  BUILD_LIST_1          1 
              454  LOAD_GLOBAL              max
              456  LOAD_CONST               0
              458  LOAD_FAST                'counter_len'
              460  LOAD_GLOBAL              len
              462  LOAD_FAST                'words'
              464  CALL_FUNCTION_1       1  ''
              466  BINARY_SUBTRACT  
              468  CALL_FUNCTION_2       2  ''
              470  BINARY_MULTIPLY  
              472  INPLACE_ADD      
              474  STORE_FAST               'words'

 L. 383       476  LOAD_FAST                'little_endian'
          478_480  POP_JUMP_IF_TRUE    490  'to 490'

 L. 384       482  LOAD_FAST                'words'
              484  LOAD_METHOD              reverse
              486  CALL_METHOD_0         0  ''
              488  POP_TOP          
            490_0  COME_FROM           478  '478'

 L. 385       490  LOAD_FAST                'prefix'
              492  LOAD_CONST               b''
              494  LOAD_METHOD              join
              496  LOAD_FAST                'words'
              498  CALL_METHOD_1         1  ''
              500  BINARY_ADD       
              502  LOAD_FAST                'suffix'
              504  BINARY_ADD       
              506  STORE_FAST               'initial_counter_block'

 L. 387       508  LOAD_GLOBAL              len
              510  LOAD_FAST                'initial_counter_block'
              512  CALL_FUNCTION_1       1  ''
              514  LOAD_FAST                'factory'
              516  LOAD_ATTR                block_size
              518  COMPARE_OP               !=
          520_522  POP_JUMP_IF_FALSE   546  'to 546'

 L. 388       524  LOAD_GLOBAL              ValueError
              526  LOAD_STR                 'Size of the counter block (%d bytes) must match block size (%d)'

 L. 389       528  LOAD_GLOBAL              len
              530  LOAD_FAST                'initial_counter_block'
              532  CALL_FUNCTION_1       1  ''

 L. 390       534  LOAD_FAST                'factory'
              536  LOAD_ATTR                block_size

 L. 389       538  BUILD_TUPLE_2         2 

 L. 388       540  BINARY_MODULO    
              542  CALL_FUNCTION_1       1  ''
              544  RAISE_VARARGS_1       1  'exception instance'
            546_0  COME_FROM           520  '520'

 L. 392       546  LOAD_GLOBAL              CtrMode
              548  LOAD_FAST                'cipher_state'
              550  LOAD_FAST                'initial_counter_block'

 L. 393       552  LOAD_GLOBAL              len
              554  LOAD_FAST                'prefix'
              556  CALL_FUNCTION_1       1  ''
              558  LOAD_FAST                'counter_len'
              560  LOAD_FAST                'little_endian'

 L. 392       562  CALL_FUNCTION_5       5  ''
              564  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 70