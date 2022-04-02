# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_ocb.py
"""
Offset Codebook (OCB) mode.

OCB is Authenticated Encryption with Associated Data (AEAD) cipher mode
designed by Prof. Phillip Rogaway and specified in `RFC7253`_.

The algorithm provides both authenticity and privacy, it is very efficient,
it uses only one key and it can be used in online mode (so that encryption
or decryption can start before the end of the message is available).

This module implements the third and last variant of OCB (OCB3) and it only
works in combination with a 128-bit block symmetric cipher, like AES.

OCB is patented in US but `free licenses`_ exist for software implementations
meant for non-military purposes.

Example:
    >>> from Crypto.Cipher import AES
    >>> from Crypto.Random import get_random_bytes
    >>>
    >>> key = get_random_bytes(32)
    >>> cipher = AES.new(key, AES.MODE_OCB)
    >>> plaintext = b"Attack at dawn"
    >>> ciphertext, mac = cipher.encrypt_and_digest(plaintext)
    >>> # Deliver cipher.nonce, ciphertext and mac
    ...
    >>> cipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
    >>> try:
    >>>     plaintext = cipher.decrypt_and_verify(ciphertext, mac)
    >>> except ValueError:
    >>>     print "Invalid message"
    >>> else:
    >>>     print plaintext

:undocumented: __package__

.. _RFC7253: http://www.rfc-editor.org/info/rfc7253
.. _free licenses: http://web.cs.ucdavis.edu/~rogaway/ocb/license.htm
"""
import struct
from binascii import unhexlify
from Crypto.Util.py3compat import bord, _copy_bytes
from Crypto.Util.number import long_to_bytes, bytes_to_long
import Crypto.Util.strxor as strxor
from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_buffer
_raw_ocb_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_ocb', '\n                                    int OCB_start_operation(void *cipher,\n                                        const uint8_t *offset_0,\n                                        size_t offset_0_len,\n                                        void **pState);\n                                    int OCB_encrypt(void *state,\n                                        const uint8_t *in,\n                                        uint8_t *out,\n                                        size_t data_len);\n                                    int OCB_decrypt(void *state,\n                                        const uint8_t *in,\n                                        uint8_t *out,\n                                        size_t data_len);\n                                    int OCB_update(void *state,\n                                        const uint8_t *in,\n                                        size_t data_len);\n                                    int OCB_digest(void *state,\n                                        uint8_t *tag,\n                                        size_t tag_len);\n                                    int OCB_stop_operation(void *state);\n                                    ')

class OcbMode(object):
    __doc__ = 'Offset Codebook (OCB) mode.\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L. 117         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_CONST               16
                6  COMPARE_OP               !=
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 118        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'OCB mode is only available for ciphers that operate on 128 bits blocks'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 121        18  LOAD_CONST               16
               20  LOAD_FAST                'self'
               22  STORE_ATTR               block_size

 L. 124        24  LOAD_GLOBAL              _copy_bytes
               26  LOAD_CONST               None
               28  LOAD_CONST               None
               30  LOAD_FAST                'nonce'
               32  CALL_FUNCTION_3       3  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               nonce

 L. 126        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'nonce'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_GLOBAL              range
               46  LOAD_CONST               1
               48  LOAD_CONST               16
               50  CALL_FUNCTION_2       2  ''
               52  <118>                 1  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L. 127        56  LOAD_GLOBAL              ValueError
               58  LOAD_STR                 'Nonce must be at most 15 bytes long'
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 128        64  LOAD_GLOBAL              is_buffer
               66  LOAD_FAST                'nonce'
               68  CALL_FUNCTION_1       1  ''
               70  POP_JUMP_IF_TRUE     80  'to 80'

 L. 129        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 'Nonce must be bytes, bytearray or memoryview'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 131        80  LOAD_FAST                'mac_len'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _mac_len

 L. 132        86  LOAD_CONST               8
               88  LOAD_FAST                'mac_len'
               90  DUP_TOP          
               92  ROT_THREE        
               94  COMPARE_OP               <=
               96  POP_JUMP_IF_FALSE   106  'to 106'
               98  LOAD_CONST               16
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_TRUE    116  'to 116'
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            96  '96'
              106  POP_TOP          
            108_0  COME_FROM           104  '104'

 L. 133       108  LOAD_GLOBAL              ValueError
              110  LOAD_STR                 'MAC tag must be between 8 and 16 bytes long'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           102  '102'

 L. 136       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _mac_tag

 L. 139       122  LOAD_CONST               b''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _cache_A

 L. 142       128  LOAD_CONST               b''
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _cache_P

 L. 145       134  LOAD_FAST                'self'
              136  LOAD_ATTR                update
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                encrypt
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                decrypt

 L. 146       146  LOAD_FAST                'self'
              148  LOAD_ATTR                digest
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                verify

 L. 145       154  BUILD_LIST_5          5 
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _next

 L. 149       160  LOAD_GLOBAL              dict
              162  LOAD_FAST                'cipher_params'
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'params_without_key'

 L. 150       168  LOAD_FAST                'params_without_key'
              170  LOAD_METHOD              pop
              172  LOAD_STR                 'key'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'key'

 L. 151       178  LOAD_GLOBAL              struct
              180  LOAD_METHOD              pack
              182  LOAD_STR                 'B'
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                _mac_len
              188  LOAD_CONST               4
              190  BINARY_LSHIFT    
              192  LOAD_CONST               255
              194  BINARY_AND       
              196  CALL_METHOD_2         2  ''

 L. 152       198  LOAD_CONST               b'\x00'
              200  LOAD_CONST               14
              202  LOAD_GLOBAL              len
              204  LOAD_FAST                'nonce'
              206  CALL_FUNCTION_1       1  ''
              208  BINARY_SUBTRACT  
              210  BINARY_MULTIPLY  

 L. 151       212  BINARY_ADD       

 L. 153       214  LOAD_CONST               b'\x01'

 L. 151       216  BINARY_ADD       

 L. 153       218  LOAD_FAST                'self'
              220  LOAD_ATTR                nonce

 L. 151       222  BINARY_ADD       
              224  STORE_FAST               'nonce'

 L. 155       226  LOAD_GLOBAL              bord
              228  LOAD_FAST                'nonce'
              230  LOAD_CONST               15
              232  BINARY_SUBSCR    
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_CONST               63
              238  BINARY_AND       
              240  STORE_FAST               'bottom_bits'

 L. 156       242  LOAD_GLOBAL              bord
              244  LOAD_FAST                'nonce'
              246  LOAD_CONST               15
              248  BINARY_SUBSCR    
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_CONST               192
              254  BINARY_AND       
              256  STORE_FAST               'top_bits'

 L. 158       258  LOAD_FAST                'factory'
              260  LOAD_ATTR                new
              262  LOAD_FAST                'key'

 L. 159       264  LOAD_FAST                'factory'
              266  LOAD_ATTR                MODE_ECB

 L. 158       268  BUILD_TUPLE_2         2 
              270  BUILD_MAP_0           0 

 L. 160       272  LOAD_FAST                'params_without_key'

 L. 158       274  <164>                 1  ''
              276  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              278  STORE_FAST               'ktop_cipher'

 L. 161       280  LOAD_FAST                'ktop_cipher'
              282  LOAD_METHOD              encrypt
              284  LOAD_GLOBAL              struct
              286  LOAD_METHOD              pack
              288  LOAD_STR                 '15sB'

 L. 162       290  LOAD_FAST                'nonce'
              292  LOAD_CONST               None
              294  LOAD_CONST               15
              296  BUILD_SLICE_2         2 
              298  BINARY_SUBSCR    

 L. 163       300  LOAD_FAST                'top_bits'

 L. 161       302  CALL_METHOD_3         3  ''
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'ktop'

 L. 165       308  LOAD_FAST                'ktop'
              310  LOAD_GLOBAL              strxor
              312  LOAD_FAST                'ktop'
              314  LOAD_CONST               None
              316  LOAD_CONST               8
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'ktop'
              324  LOAD_CONST               1
              326  LOAD_CONST               9
              328  BUILD_SLICE_2         2 
              330  BINARY_SUBSCR    
              332  CALL_FUNCTION_2       2  ''
              334  BINARY_ADD       
              336  STORE_FAST               'stretch'

 L. 166       338  LOAD_GLOBAL              long_to_bytes
              340  LOAD_GLOBAL              bytes_to_long
              342  LOAD_FAST                'stretch'
              344  CALL_FUNCTION_1       1  ''

 L. 167       346  LOAD_CONST               64
              348  LOAD_FAST                'bottom_bits'
              350  BINARY_SUBTRACT  

 L. 166       352  BINARY_RSHIFT    

 L. 167       354  LOAD_CONST               24

 L. 166       356  CALL_FUNCTION_2       2  ''

 L. 167       358  LOAD_CONST               8
              360  LOAD_CONST               None
              362  BUILD_SLICE_2         2 

 L. 166       364  BINARY_SUBSCR    
              366  STORE_FAST               'offset_0'

 L. 170       368  LOAD_FAST                'factory'
              370  LOAD_METHOD              _create_base_cipher
              372  LOAD_FAST                'cipher_params'
              374  CALL_METHOD_1         1  ''
              376  STORE_FAST               'raw_cipher'

 L. 171       378  LOAD_FAST                'cipher_params'
          380_382  POP_JUMP_IF_FALSE   400  'to 400'

 L. 172       384  LOAD_GLOBAL              TypeError
              386  LOAD_STR                 'Unknown keywords: '
              388  LOAD_GLOBAL              str
              390  LOAD_FAST                'cipher_params'
              392  CALL_FUNCTION_1       1  ''
              394  BINARY_ADD       
              396  CALL_FUNCTION_1       1  ''
              398  RAISE_VARARGS_1       1  'exception instance'
            400_0  COME_FROM           380  '380'

 L. 174       400  LOAD_GLOBAL              VoidPointer
              402  CALL_FUNCTION_0       0  ''
              404  LOAD_FAST                'self'
              406  STORE_ATTR               _state

 L. 175       408  LOAD_GLOBAL              _raw_ocb_lib
              410  LOAD_METHOD              OCB_start_operation
              412  LOAD_FAST                'raw_cipher'
              414  LOAD_METHOD              get
              416  CALL_METHOD_0         0  ''

 L. 176       418  LOAD_FAST                'offset_0'

 L. 177       420  LOAD_GLOBAL              c_size_t
              422  LOAD_GLOBAL              len
              424  LOAD_FAST                'offset_0'
              426  CALL_FUNCTION_1       1  ''
              428  CALL_FUNCTION_1       1  ''

 L. 178       430  LOAD_FAST                'self'
              432  LOAD_ATTR                _state
              434  LOAD_METHOD              address_of
              436  CALL_METHOD_0         0  ''

 L. 175       438  CALL_METHOD_4         4  ''
              440  STORE_FAST               'result'

 L. 179       442  LOAD_FAST                'result'
          444_446  POP_JUMP_IF_FALSE   460  'to 460'

 L. 180       448  LOAD_GLOBAL              ValueError
              450  LOAD_STR                 'Error %d while instantiating the OCB mode'

 L. 181       452  LOAD_FAST                'result'

 L. 180       454  BINARY_MODULO    
              456  CALL_FUNCTION_1       1  ''
              458  RAISE_VARARGS_1       1  'exception instance'
            460_0  COME_FROM           444  '444'

 L. 185       460  LOAD_GLOBAL              SmartPointer
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                _state
              466  LOAD_METHOD              get
              468  CALL_METHOD_0         0  ''

 L. 186       470  LOAD_GLOBAL              _raw_ocb_lib
              472  LOAD_ATTR                OCB_stop_operation

 L. 185       474  CALL_FUNCTION_2       2  ''
              476  LOAD_FAST                'self'
              478  STORE_ATTR               _state

 L. 190       480  LOAD_FAST                'raw_cipher'
              482  LOAD_METHOD              release
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          

Parse error at or near `<118>' instruction at offset 52

    def _update(self, assoc_data, assoc_data_len):
        result = _raw_ocb_lib.OCB_updateself._state.getc_uint8_ptr(assoc_data)c_size_t(assoc_data_len)
        if result:
            raise ValueError('Error %d while computing MAC in OCB mode' % result)

    def update--- This code section failed: ---

 L. 220         0  LOAD_FAST                'self'
                2  LOAD_ATTR                update
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 221        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'update() can only be called immediately after initialization'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 224        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                decrypt
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                digest

 L. 225        32  LOAD_FAST                'self'
               34  LOAD_ATTR                verify
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                update

 L. 224        40  BUILD_LIST_5          5 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _next

 L. 227        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _cache_A
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               0
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE   160  'to 160'

 L. 228        60  LOAD_GLOBAL              min
               62  LOAD_CONST               16
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _cache_A
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_SUBTRACT  
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'assoc_data'
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               'filler'

 L. 229        84  LOAD_FAST                'self'
               86  DUP_TOP          
               88  LOAD_ATTR                _cache_A
               90  LOAD_GLOBAL              _copy_bytes
               92  LOAD_CONST               None
               94  LOAD_FAST                'filler'
               96  LOAD_FAST                'assoc_data'
               98  CALL_FUNCTION_3       3  ''
              100  INPLACE_ADD      
              102  ROT_TWO          
              104  STORE_ATTR               _cache_A

 L. 230       106  LOAD_FAST                'assoc_data'
              108  LOAD_FAST                'filler'
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  STORE_FAST               'assoc_data'

 L. 232       118  LOAD_GLOBAL              len
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _cache_A
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_CONST               16
              128  COMPARE_OP               <
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 233       132  LOAD_FAST                'self'
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'

 L. 236       136  LOAD_CONST               b''
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _cache_A
              142  ROT_TWO          
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _cache_A
              148  STORE_FAST               'seg'

 L. 237       150  LOAD_FAST                'self'
              152  LOAD_METHOD              update
              154  LOAD_FAST                'seg'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
            160_0  COME_FROM            58  '58'

 L. 239       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'assoc_data'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_CONST               16
              168  BINARY_FLOOR_DIVIDE
              170  LOAD_CONST               16
              172  BINARY_MULTIPLY  
              174  STORE_FAST               'update_len'

 L. 240       176  LOAD_GLOBAL              _copy_bytes
              178  LOAD_FAST                'update_len'
              180  LOAD_CONST               None
              182  LOAD_FAST                'assoc_data'
              184  CALL_FUNCTION_3       3  ''
              186  LOAD_FAST                'self'
              188  STORE_ATTR               _cache_A

 L. 241       190  LOAD_FAST                'self'
              192  LOAD_METHOD              _update
              194  LOAD_FAST                'assoc_data'
              196  LOAD_FAST                'update_len'
              198  CALL_METHOD_2         2  ''
              200  POP_TOP          

 L. 242       202  LOAD_FAST                'self'
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _transcrypt_aligned(self, in_data, in_data_len, trans_func, trans_desc):
        out_data = create_string_buffer(in_data_len)
        result = trans_func(self._state.get, in_data, out_data, c_size_t(in_data_len))
        if result:
            raise ValueError('Error %d while %sing in OCB mode' % (
             result, trans_desc))
        return get_raw_buffer(out_data)

    def _transcrypt--- This code section failed: ---

 L. 259         0  LOAD_FAST                'in_data'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    42  'to 42'

 L. 260         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _transcrypt_aligned
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _cache_P

 L. 261        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _cache_P
               22  CALL_FUNCTION_1       1  ''

 L. 262        24  LOAD_FAST                'trans_func'

 L. 263        26  LOAD_FAST                'trans_desc'

 L. 260        28  CALL_METHOD_4         4  ''
               30  STORE_FAST               'out_data'

 L. 264        32  LOAD_CONST               b''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _cache_P

 L. 265        38  LOAD_FAST                'out_data'
               40  RETURN_VALUE     
             42_0  COME_FROM             6  '6'

 L. 268        42  LOAD_CONST               b''
               44  STORE_FAST               'prefix'

 L. 269        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _cache_P
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               0
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE   166  'to 166'

 L. 270        60  LOAD_GLOBAL              min
               62  LOAD_CONST               16
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _cache_P
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_SUBTRACT  
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'in_data'
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               'filler'

 L. 271        84  LOAD_FAST                'self'
               86  DUP_TOP          
               88  LOAD_ATTR                _cache_P
               90  LOAD_GLOBAL              _copy_bytes
               92  LOAD_CONST               None
               94  LOAD_FAST                'filler'
               96  LOAD_FAST                'in_data'
               98  CALL_FUNCTION_3       3  ''
              100  INPLACE_ADD      
              102  ROT_TWO          
              104  STORE_ATTR               _cache_P

 L. 272       106  LOAD_FAST                'in_data'
              108  LOAD_FAST                'filler'
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  STORE_FAST               'in_data'

 L. 274       118  LOAD_GLOBAL              len
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _cache_P
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_CONST               16
              128  COMPARE_OP               <
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 277       132  LOAD_CONST               b''
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'

 L. 280       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _transcrypt_aligned
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _cache_P

 L. 281       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _cache_P
              150  CALL_FUNCTION_1       1  ''

 L. 282       152  LOAD_FAST                'trans_func'

 L. 283       154  LOAD_FAST                'trans_desc'

 L. 280       156  CALL_METHOD_4         4  ''
              158  STORE_FAST               'prefix'

 L. 284       160  LOAD_CONST               b''
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _cache_P
            166_0  COME_FROM            58  '58'

 L. 287       166  LOAD_GLOBAL              len
              168  LOAD_FAST                'in_data'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_CONST               16
              174  BINARY_FLOOR_DIVIDE
              176  LOAD_CONST               16
              178  BINARY_MULTIPLY  
              180  STORE_FAST               'trans_len'

 L. 288       182  LOAD_FAST                'self'
              184  LOAD_METHOD              _transcrypt_aligned
              186  LOAD_GLOBAL              c_uint8_ptr
              188  LOAD_FAST                'in_data'
              190  CALL_FUNCTION_1       1  ''

 L. 289       192  LOAD_FAST                'trans_len'

 L. 290       194  LOAD_FAST                'trans_func'

 L. 291       196  LOAD_FAST                'trans_desc'

 L. 288       198  CALL_METHOD_4         4  ''
              200  STORE_FAST               'result'

 L. 292       202  LOAD_FAST                'prefix'
              204  POP_JUMP_IF_FALSE   214  'to 214'

 L. 293       206  LOAD_FAST                'prefix'
              208  LOAD_FAST                'result'
              210  BINARY_ADD       
              212  STORE_FAST               'result'
            214_0  COME_FROM           204  '204'

 L. 296       214  LOAD_GLOBAL              _copy_bytes
              216  LOAD_FAST                'trans_len'
              218  LOAD_CONST               None
              220  LOAD_FAST                'in_data'
              222  CALL_FUNCTION_3       3  ''
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _cache_P

 L. 298       228  LOAD_FAST                'result'
              230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def encrypt--- This code section failed: ---

 L. 319         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 320        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 323        20  LOAD_FAST                'plaintext'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 324        28  LOAD_FAST                'self'
               30  LOAD_ATTR                digest
               32  BUILD_LIST_1          1 
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _next
               38  JUMP_FORWARD         50  'to 50'
             40_0  COME_FROM            26  '26'

 L. 326        40  LOAD_FAST                'self'
               42  LOAD_ATTR                encrypt
               44  BUILD_LIST_1          1 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _next
             50_0  COME_FROM            38  '38'

 L. 327        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _transcrypt
               54  LOAD_FAST                'plaintext'
               56  LOAD_GLOBAL              _raw_ocb_lib
               58  LOAD_ATTR                OCB_encrypt
               60  LOAD_STR                 'encrypt'
               62  CALL_METHOD_3         3  ''
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 348         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 349        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 352        20  LOAD_FAST                'ciphertext'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 353        28  LOAD_FAST                'self'
               30  LOAD_ATTR                verify
               32  BUILD_LIST_1          1 
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _next
               38  JUMP_FORWARD         50  'to 50'
             40_0  COME_FROM            26  '26'

 L. 355        40  LOAD_FAST                'self'
               42  LOAD_ATTR                decrypt
               44  BUILD_LIST_1          1 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _next
             50_0  COME_FROM            38  '38'

 L. 356        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _transcrypt
               54  LOAD_FAST                'ciphertext'

 L. 357        56  LOAD_GLOBAL              _raw_ocb_lib
               58  LOAD_ATTR                OCB_decrypt

 L. 358        60  LOAD_STR                 'decrypt'

 L. 356        62  CALL_METHOD_3         3  ''
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _compute_mac_tag--- This code section failed: ---

 L. 362         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _mac_tag
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 363        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 365        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _cache_A
               18  POP_JUMP_IF_FALSE    46  'to 46'

 L. 366        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _update
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _cache_A
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _cache_A
               34  CALL_FUNCTION_1       1  ''
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L. 367        40  LOAD_CONST               b''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _cache_A
             46_0  COME_FROM            18  '18'

 L. 369        46  LOAD_GLOBAL              create_string_buffer
               48  LOAD_CONST               16
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'mac_tag'

 L. 370        54  LOAD_GLOBAL              _raw_ocb_lib
               56  LOAD_METHOD              OCB_digest
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _state
               62  LOAD_METHOD              get
               64  CALL_METHOD_0         0  ''

 L. 371        66  LOAD_FAST                'mac_tag'

 L. 372        68  LOAD_GLOBAL              c_size_t
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'mac_tag'
               74  CALL_FUNCTION_1       1  ''
               76  CALL_FUNCTION_1       1  ''

 L. 370        78  CALL_METHOD_3         3  ''
               80  STORE_FAST               'result'

 L. 374        82  LOAD_FAST                'result'
               84  POP_JUMP_IF_FALSE    98  'to 98'

 L. 375        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 'Error %d while computing digest in OCB mode'

 L. 376        90  LOAD_FAST                'result'

 L. 375        92  BINARY_MODULO    
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            84  '84'

 L. 377        98  LOAD_GLOBAL              get_raw_buffer
              100  LOAD_FAST                'mac_tag'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _mac_len
              110  BUILD_SLICE_2         2 
              112  BINARY_SUBSCR    
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _mac_tag

Parse error at or near `None' instruction at offset -1

    def digest--- This code section failed: ---

 L. 391         0  LOAD_FAST                'self'
                2  LOAD_ATTR                digest
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 392        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'digest() cannot be called now for this cipher'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 394        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _cache_P
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               0
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 396        38  LOAD_FAST                'self'
               40  LOAD_ATTR                digest
               42  BUILD_LIST_1          1 
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _next

 L. 398        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _mac_tag
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 399        58  LOAD_FAST                'self'
               60  LOAD_METHOD              _compute_mac_tag
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          
             66_0  COME_FROM            56  '56'

 L. 401        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _mac_tag
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify--- This code section failed: ---

 L. 426         0  LOAD_FAST                'self'
                2  LOAD_ATTR                verify
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 427        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'verify() cannot be called now for this cipher'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 429        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _cache_P
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               0
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 431        38  LOAD_FAST                'self'
               40  LOAD_ATTR                verify
               42  BUILD_LIST_1          1 
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _next

 L. 433        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _mac_tag
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 434        58  LOAD_FAST                'self'
               60  LOAD_METHOD              _compute_mac_tag
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          
             66_0  COME_FROM            56  '56'

 L. 436        66  LOAD_GLOBAL              get_random_bytes
               68  LOAD_CONST               16
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'secret'

 L. 437        74  LOAD_GLOBAL              BLAKE2s
               76  LOAD_ATTR                new
               78  LOAD_CONST               160
               80  LOAD_FAST                'secret'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                _mac_tag
               86  LOAD_CONST               ('digest_bits', 'key', 'data')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  STORE_FAST               'mac1'

 L. 438        92  LOAD_GLOBAL              BLAKE2s
               94  LOAD_ATTR                new
               96  LOAD_CONST               160
               98  LOAD_FAST                'secret'
              100  LOAD_FAST                'received_mac_tag'
              102  LOAD_CONST               ('digest_bits', 'key', 'data')
              104  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              106  STORE_FAST               'mac2'

 L. 440       108  LOAD_FAST                'mac1'
              110  LOAD_METHOD              digest
              112  CALL_METHOD_0         0  ''
              114  LOAD_FAST                'mac2'
              116  LOAD_METHOD              digest
              118  CALL_METHOD_0         0  ''
              120  COMPARE_OP               !=
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 441       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'MAC check failed'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

Parse error at or near `None' instruction at offset -1

    def hexverify(self, hex_mac_tag):
        """Validate the *printable* MAC tag.

        This method is like `verify`.

        :Parameters:
          hex_mac_tag : string
            This is the *printable* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        self.verifyunhexlify(hex_mac_tag)

    def encrypt_and_digest(self, plaintext):
        """Encrypt the message and create the MAC tag in one step.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The entire message to encrypt.
        :Return:
            a tuple with two byte strings:

            - the encrypted data
            - the MAC
        """
        return (
         self.encryptplaintext + self.encrypt, self.digest)

    def decrypt_and_verify(self, ciphertext, received_mac_tag):
        """Decrypted the message and verify its authenticity in one step.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The entire message to decrypt.
          received_mac_tag : byte string
            This is the *binary* MAC, as received from the sender.

        :Return: the decrypted data (byte string).
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        plaintext = self.decryptciphertext + self.decrypt
        self.verifyreceived_mac_tag
        return plaintext


def _create_ocb_cipher--- This code section failed: ---

 L. 517         0  SETUP_FINALLY        46  'to 46'

 L. 518         2  LOAD_FAST                'kwargs'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'nonce'
                8  LOAD_CONST               None
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'nonce'

 L. 519        14  LOAD_FAST                'nonce'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 520        22  LOAD_GLOBAL              get_random_bytes
               24  LOAD_CONST               15
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'nonce'
             30_0  COME_FROM            20  '20'

 L. 521        30  LOAD_FAST                'kwargs'
               32  LOAD_METHOD              pop
               34  LOAD_STR                 'mac_len'
               36  LOAD_CONST               16
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'mac_len'
               42  POP_BLOCK        
               44  JUMP_FORWARD         98  'to 98'
             46_0  COME_FROM_FINALLY     0  '0'

 L. 522        46  DUP_TOP          
               48  LOAD_GLOBAL              KeyError
               50  <121>                96  ''
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        88  'to 88'

 L. 523        60  LOAD_GLOBAL              TypeError
               62  LOAD_STR                 'Keyword missing: '
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'e'
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_ADD       
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_BLOCK        
               78  POP_EXCEPT       
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  JUMP_FORWARD         98  'to 98'
             88_0  COME_FROM_FINALLY    58  '58'
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  <48>             
               96  <48>             
             98_0  COME_FROM            86  '86'
             98_1  COME_FROM            44  '44'

 L. 525        98  LOAD_GLOBAL              OcbMode
              100  LOAD_FAST                'factory'
              102  LOAD_FAST                'nonce'
              104  LOAD_FAST                'mac_len'
              106  LOAD_FAST                'kwargs'
              108  CALL_FUNCTION_4       4  ''
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18