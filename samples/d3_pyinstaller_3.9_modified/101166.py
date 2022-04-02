# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_mode_gcm.py
"""
Galois/Counter Mode (GCM).
"""
__all__ = [
 'GcmMode']
from binascii import unhexlify
from Crypto.Util.py3compat import bord, _copy_bytes
from Crypto.Util._raw_api import is_buffer
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Hash import BLAKE2s
from Crypto.Random import get_random_bytes
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr
from Crypto.Util import _cpu_features
_ghash_api_template = '\n    int ghash_%imp%(uint8_t y_out[16],\n                    const uint8_t block_data[],\n                    size_t len,\n                    const uint8_t y_in[16],\n                    const void *exp_key);\n    int ghash_expand_%imp%(const uint8_t h[16],\n                           void **ghash_tables);\n    int ghash_destroy_%imp%(void *ghash_tables);\n'

def _build_impl--- This code section failed: ---

 L.  67         0  LOAD_CONST               0
                2  LOAD_CONST               ('namedtuple',)
                4  IMPORT_NAME              collections
                6  IMPORT_FROM              namedtuple
                8  STORE_FAST               'namedtuple'
               10  POP_TOP          

 L.  69        12  LOAD_CONST               ('ghash', 'ghash_expand', 'ghash_destroy')
               14  STORE_FAST               'funcs'

 L.  70        16  LOAD_FAST                'namedtuple'
               18  LOAD_STR                 '_GHash_Imp'
               20  LOAD_FAST                'funcs'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'GHASH_Imp'

 L.  71        26  SETUP_FINALLY        52  'to 52'

 L.  72        28  LOAD_CLOSURE             'lib'
               30  LOAD_CLOSURE             'postfix'
               32  BUILD_TUPLE_2         2 
               34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 '_build_impl.<locals>.<listcomp>'
               38  MAKE_FUNCTION_8          'closure'
               40  LOAD_FAST                'funcs'
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'imp_funcs'
               48  POP_BLOCK        
               50  JUMP_FORWARD         80  'to 80'
             52_0  COME_FROM_FINALLY    26  '26'

 L.  73        52  DUP_TOP          
               54  LOAD_GLOBAL              AttributeError
               56  <121>                78  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  74        64  LOAD_CONST               None
               66  BUILD_LIST_1          1 
               68  LOAD_CONST               3
               70  BINARY_MULTIPLY  
               72  STORE_FAST               'imp_funcs'
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            50  '50'

 L.  75        80  LOAD_GLOBAL              dict
               82  LOAD_GLOBAL              zip
               84  LOAD_FAST                'funcs'
               86  LOAD_FAST                'imp_funcs'
               88  CALL_FUNCTION_2       2  ''
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'params'

 L.  76        94  LOAD_FAST                'GHASH_Imp'
               96  BUILD_TUPLE_0         0 
               98  BUILD_MAP_0           0 
              100  LOAD_FAST                'params'
              102  <164>                 1  ''
              104  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56


def _get_ghash_portable():
    api = _ghash_api_template.replace('%imp%', 'portable')
    lib = load_pycryptodome_raw_lib'Crypto.Hash._ghash_portable'api
    result = _build_impllib'portable'
    return result


_ghash_portable = _get_ghash_portable()

def _get_ghash_clmul--- This code section failed: ---

 L.  90         0  LOAD_GLOBAL              _cpu_features
                2  LOAD_METHOD              have_clmul
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'

 L.  91         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  92        12  SETUP_FINALLY        50  'to 50'

 L.  93        14  LOAD_GLOBAL              _ghash_api_template
               16  LOAD_METHOD              replace
               18  LOAD_STR                 '%imp%'
               20  LOAD_STR                 'clmul'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'api'

 L.  94        26  LOAD_GLOBAL              load_pycryptodome_raw_lib
               28  LOAD_STR                 'Crypto.Hash._ghash_clmul'
               30  LOAD_FAST                'api'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'lib'

 L.  95        36  LOAD_GLOBAL              _build_impl
               38  LOAD_FAST                'lib'
               40  LOAD_STR                 'clmul'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'result'
               46  POP_BLOCK        
               48  JUMP_FORWARD         72  'to 72'
             50_0  COME_FROM_FINALLY    12  '12'

 L.  96        50  DUP_TOP          
               52  LOAD_GLOBAL              OSError
               54  <121>                70  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  97        62  LOAD_CONST               None
               64  STORE_FAST               'result'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            48  '48'

 L.  98        72  LOAD_FAST                'result'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 54


_ghash_clmul = _get_ghash_clmul()

class _GHASH(object):
    __doc__ = 'GHASH function defined in NIST SP 800-38D, Algorithm 2.\n\n    If X_1, X_2, .. X_m are the blocks of input data, the function\n    computes:\n\n       X_1*H^{m} + X_2*H^{m-1} + ... + X_m*H\n\n    in the Galois field GF(2^256) using the reducing polynomial\n    (x^128 + x^7 + x^2 + x + 1).\n    '

    def __init__--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'subkey'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               16
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L. 117        16  LOAD_FAST                'ghash_c'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               ghash_c

 L. 119        22  LOAD_GLOBAL              VoidPointer
               24  CALL_FUNCTION_0       0  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _exp_key

 L. 120        30  LOAD_FAST                'ghash_c'
               32  LOAD_METHOD              ghash_expand
               34  LOAD_GLOBAL              c_uint8_ptr
               36  LOAD_FAST                'subkey'
               38  CALL_FUNCTION_1       1  ''

 L. 121        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _exp_key
               44  LOAD_METHOD              address_of
               46  CALL_METHOD_0         0  ''

 L. 120        48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'result'

 L. 122        52  LOAD_FAST                'result'
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L. 123        56  LOAD_GLOBAL              ValueError
               58  LOAD_STR                 'Error %d while expanding the GHASH key'
               60  LOAD_FAST                'result'
               62  BINARY_MODULO    
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            54  '54'

 L. 125        68  LOAD_GLOBAL              SmartPointer
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _exp_key
               74  LOAD_METHOD              get
               76  CALL_METHOD_0         0  ''

 L. 126        78  LOAD_FAST                'ghash_c'
               80  LOAD_ATTR                ghash_destroy

 L. 125        82  CALL_FUNCTION_2       2  ''
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _exp_key

 L. 129        88  LOAD_GLOBAL              create_string_buffer
               90  LOAD_CONST               16
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _last_y

Parse error at or near `None' instruction at offset -1

    def update--- This code section failed: ---

 L. 132         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'block_data'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               16
                8  BINARY_MODULO    
               10  LOAD_CONST               0
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 134        20  LOAD_FAST                'self'
               22  LOAD_ATTR                ghash_c
               24  LOAD_METHOD              ghash
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _last_y

 L. 135        30  LOAD_GLOBAL              c_uint8_ptr
               32  LOAD_FAST                'block_data'
               34  CALL_FUNCTION_1       1  ''

 L. 136        36  LOAD_GLOBAL              c_size_t
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'block_data'
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''

 L. 137        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _last_y

 L. 138        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _exp_key
               54  LOAD_METHOD              get
               56  CALL_METHOD_0         0  ''

 L. 134        58  CALL_METHOD_5         5  ''
               60  STORE_FAST               'result'

 L. 139        62  LOAD_FAST                'result'
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L. 140        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'Error %d while updating GHASH'
               70  LOAD_FAST                'result'
               72  BINARY_MODULO    
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            64  '64'

 L. 142        78  LOAD_FAST                'self'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def digest(self):
        return get_raw_buffer(self._last_y)


def enum(**enums):
    return type('Enum', (), enums)


MacStatus = enum(PROCESSING_AUTH_DATA=1, PROCESSING_CIPHERTEXT=2)

class GcmMode(object):
    __doc__ = 'Galois Counter Mode (GCM).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    This mode requires a *nonce*.\n\n    This mode is only available for ciphers that operate on 128 bits blocks\n    (e.g. AES but not TDES).\n\n    See `NIST SP800-38D`_.\n\n    .. _`NIST SP800-38D`: http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n\n    :undocumented: __init__\n    '

    def __init__--- This code section failed: ---

 L. 182         0  LOAD_FAST                'factory'
                2  LOAD_ATTR                block_size
                4  LOAD_FAST                'self'
                6  STORE_ATTR               block_size

 L. 183         8  LOAD_FAST                'self'
               10  LOAD_ATTR                block_size
               12  LOAD_CONST               16
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 184        18  LOAD_GLOBAL              ValueError
               20  LOAD_STR                 'GCM mode is only available for ciphers that operate on 128 bits blocks'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 187        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'nonce'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               0
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 188        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'Nonce cannot be empty'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 190        46  LOAD_GLOBAL              is_buffer
               48  LOAD_FAST                'nonce'
               50  CALL_FUNCTION_1       1  ''
               52  POP_JUMP_IF_TRUE     62  'to 62'

 L. 191        54  LOAD_GLOBAL              TypeError
               56  LOAD_STR                 'Nonce must be bytes, bytearray or memoryview'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L. 194        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'nonce'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               18446744073709551615
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE    82  'to 82'

 L. 195        74  LOAD_GLOBAL              ValueError
               76  LOAD_STR                 'Nonce exceeds maximum length'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'

 L. 198        82  LOAD_GLOBAL              _copy_bytes
               84  LOAD_CONST               None
               86  LOAD_CONST               None
               88  LOAD_FAST                'nonce'
               90  CALL_FUNCTION_3       3  ''
               92  LOAD_FAST                'self'
               94  STORE_ATTR               nonce

 L. 201        96  LOAD_FAST                'factory'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _factory

 L. 202       102  LOAD_GLOBAL              _copy_bytes
              104  LOAD_CONST               None
              106  LOAD_CONST               None
              108  LOAD_FAST                'key'
              110  CALL_FUNCTION_3       3  ''
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _key

 L. 203       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _tag

 L. 205       122  LOAD_FAST                'mac_len'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _mac_len

 L. 206       128  LOAD_CONST               4
              130  LOAD_FAST                'mac_len'
              132  DUP_TOP          
              134  ROT_THREE        
              136  COMPARE_OP               <=
              138  POP_JUMP_IF_FALSE   148  'to 148'
              140  LOAD_CONST               16
              142  COMPARE_OP               <=
              144  POP_JUMP_IF_TRUE    158  'to 158'
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           138  '138'
              148  POP_TOP          
            150_0  COME_FROM           146  '146'

 L. 207       150  LOAD_GLOBAL              ValueError
              152  LOAD_STR                 "Parameter 'mac_len' must be in the range 4..16"
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           144  '144'

 L. 210       158  LOAD_FAST                'self'
              160  LOAD_ATTR                update
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                encrypt
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                decrypt

 L. 211       170  LOAD_FAST                'self'
              172  LOAD_ATTR                digest
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                verify

 L. 210       178  BUILD_LIST_5          5 
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _next

 L. 213       184  LOAD_CONST               False
              186  LOAD_FAST                'self'
              188  STORE_ATTR               _no_more_assoc_data

 L. 216       190  LOAD_CONST               0
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _auth_len

 L. 219       196  LOAD_CONST               0
              198  LOAD_FAST                'self'
              200  STORE_ATTR               _msg_len

 L. 223       202  LOAD_FAST                'factory'
              204  LOAD_ATTR                new
              206  LOAD_FAST                'key'

 L. 224       208  LOAD_FAST                'self'
              210  LOAD_ATTR                _factory
              212  LOAD_ATTR                MODE_ECB

 L. 223       214  BUILD_TUPLE_2         2 
              216  BUILD_MAP_0           0 

 L. 225       218  LOAD_FAST                'cipher_params'

 L. 223       220  <164>                 1  ''
              222  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              224  LOAD_METHOD              encrypt

 L. 226       226  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

 L. 223       228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'hash_subkey'

 L. 229       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                nonce
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_CONST               12
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L. 230       248  LOAD_FAST                'self'
              250  LOAD_ATTR                nonce
              252  LOAD_CONST               b'\x00\x00\x00\x01'
              254  BINARY_ADD       
              256  STORE_FAST               'j0'
              258  JUMP_FORWARD        336  'to 336'
            260_0  COME_FROM           244  '244'

 L. 232       260  LOAD_CONST               16
              262  LOAD_GLOBAL              len
              264  LOAD_FAST                'nonce'
              266  CALL_FUNCTION_1       1  ''
              268  LOAD_CONST               16
              270  BINARY_MODULO    
              272  BINARY_SUBTRACT  
              274  LOAD_CONST               16
              276  BINARY_MODULO    
              278  LOAD_CONST               8
              280  BINARY_ADD       
              282  STORE_FAST               'fill'

 L. 233       284  LOAD_FAST                'self'
              286  LOAD_ATTR                nonce

 L. 234       288  LOAD_CONST               b'\x00'
              290  LOAD_FAST                'fill'
              292  BINARY_MULTIPLY  

 L. 233       294  BINARY_ADD       

 L. 235       296  LOAD_GLOBAL              long_to_bytes
              298  LOAD_CONST               8
              300  LOAD_GLOBAL              len
              302  LOAD_FAST                'nonce'
              304  CALL_FUNCTION_1       1  ''
              306  BINARY_MULTIPLY  
              308  LOAD_CONST               8
              310  CALL_FUNCTION_2       2  ''

 L. 233       312  BINARY_ADD       
              314  STORE_FAST               'ghash_in'

 L. 236       316  LOAD_GLOBAL              _GHASH
              318  LOAD_FAST                'hash_subkey'
              320  LOAD_FAST                'ghash_c'
              322  CALL_FUNCTION_2       2  ''
              324  LOAD_METHOD              update
              326  LOAD_FAST                'ghash_in'
              328  CALL_METHOD_1         1  ''
              330  LOAD_METHOD              digest
              332  CALL_METHOD_0         0  ''
              334  STORE_FAST               'j0'
            336_0  COME_FROM           258  '258'

 L. 239       336  LOAD_FAST                'j0'
              338  LOAD_CONST               None
              340  LOAD_CONST               12
              342  BUILD_SLICE_2         2 
              344  BINARY_SUBSCR    
              346  STORE_FAST               'nonce_ctr'

 L. 240       348  LOAD_GLOBAL              bytes_to_long
              350  LOAD_FAST                'j0'
              352  CALL_FUNCTION_1       1  ''
              354  LOAD_CONST               1
              356  BINARY_ADD       
              358  LOAD_CONST               4294967295
              360  BINARY_AND       
              362  STORE_FAST               'iv_ctr'

 L. 241       364  LOAD_FAST                'factory'
              366  LOAD_ATTR                new
              368  LOAD_FAST                'key'

 L. 242       370  LOAD_FAST                'self'
              372  LOAD_ATTR                _factory
              374  LOAD_ATTR                MODE_CTR

 L. 241       376  BUILD_TUPLE_2         2 

 L. 243       378  LOAD_FAST                'iv_ctr'

 L. 244       380  LOAD_FAST                'nonce_ctr'

 L. 241       382  LOAD_CONST               ('initial_value', 'nonce')
              384  BUILD_CONST_KEY_MAP_2     2 

 L. 245       386  LOAD_FAST                'cipher_params'

 L. 241       388  <164>                 1  ''
              390  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              392  LOAD_FAST                'self'
              394  STORE_ATTR               _cipher

 L. 248       396  LOAD_GLOBAL              _GHASH
              398  LOAD_FAST                'hash_subkey'
              400  LOAD_FAST                'ghash_c'
              402  CALL_FUNCTION_2       2  ''
              404  LOAD_FAST                'self'
              406  STORE_ATTR               _signer

 L. 251       408  LOAD_FAST                'factory'
              410  LOAD_ATTR                new
              412  LOAD_FAST                'key'

 L. 252       414  LOAD_FAST                'self'
              416  LOAD_ATTR                _factory
              418  LOAD_ATTR                MODE_CTR

 L. 251       420  BUILD_TUPLE_2         2 

 L. 253       422  LOAD_FAST                'j0'

 L. 254       424  LOAD_CONST               b''

 L. 251       426  LOAD_CONST               ('initial_value', 'nonce')
              428  BUILD_CONST_KEY_MAP_2     2 

 L. 255       430  LOAD_FAST                'cipher_params'

 L. 251       432  <164>                 1  ''
              434  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              436  LOAD_FAST                'self'
              438  STORE_ATTR               _tag_cipher

 L. 258       440  LOAD_CONST               b''
              442  LOAD_FAST                'self'
              444  STORE_ATTR               _cache

 L. 260       446  LOAD_GLOBAL              MacStatus
              448  LOAD_ATTR                PROCESSING_AUTH_DATA
              450  LOAD_FAST                'self'
              452  STORE_ATTR               _status

Parse error at or near `<164>' instruction at offset 220

    def update--- This code section failed: ---

 L. 285         0  LOAD_FAST                'self'
                2  LOAD_ATTR                update
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 286        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'update() can only be called immediately after initialization'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 289        20  LOAD_FAST                'self'
               22  LOAD_ATTR                update
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                encrypt
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                decrypt

 L. 290        32  LOAD_FAST                'self'
               34  LOAD_ATTR                digest
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                verify

 L. 289        40  BUILD_LIST_5          5 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _next

 L. 292        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _update
               50  LOAD_FAST                'assoc_data'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 293        56  LOAD_FAST                'self'
               58  DUP_TOP          
               60  LOAD_ATTR                _auth_len
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'assoc_data'
               66  CALL_FUNCTION_1       1  ''
               68  INPLACE_ADD      
               70  ROT_TWO          
               72  STORE_ATTR               _auth_len

 L. 296        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _auth_len
               78  LOAD_CONST               18446744073709551615
               80  COMPARE_OP               >
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 297        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Additional Authenticated Data exceeds maximum length'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 299        92  LOAD_FAST                'self'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _update--- This code section failed: ---

 L. 302         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _cache
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               16
               10  COMPARE_OP               <
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 304        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _cache
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE   128  'to 128'

 L. 305        32  LOAD_GLOBAL              min
               34  LOAD_CONST               16
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _cache
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_SUBTRACT  
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'data'
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_2       2  ''
               54  STORE_FAST               'filler'

 L. 306        56  LOAD_FAST                'self'
               58  DUP_TOP          
               60  LOAD_ATTR                _cache
               62  LOAD_GLOBAL              _copy_bytes
               64  LOAD_CONST               None
               66  LOAD_FAST                'filler'
               68  LOAD_FAST                'data'
               70  CALL_FUNCTION_3       3  ''
               72  INPLACE_ADD      
               74  ROT_TWO          
               76  STORE_ATTR               _cache

 L. 307        78  LOAD_FAST                'data'
               80  LOAD_FAST                'filler'
               82  LOAD_CONST               None
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  STORE_FAST               'data'

 L. 309        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _cache
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_CONST               16
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   108  'to 108'

 L. 310       104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM           102  '102'

 L. 313       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _signer
              112  LOAD_METHOD              update
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _cache
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 314       122  LOAD_CONST               b''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _cache
            128_0  COME_FROM            30  '30'

 L. 316       128  LOAD_GLOBAL              len
              130  LOAD_FAST                'data'
              132  CALL_FUNCTION_1       1  ''
              134  LOAD_CONST               16
              136  BINARY_FLOOR_DIVIDE
              138  LOAD_CONST               16
              140  BINARY_MULTIPLY  
              142  STORE_FAST               'update_len'

 L. 317       144  LOAD_GLOBAL              _copy_bytes
              146  LOAD_FAST                'update_len'
              148  LOAD_CONST               None
              150  LOAD_FAST                'data'
              152  CALL_FUNCTION_3       3  ''
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _cache

 L. 318       158  LOAD_FAST                'update_len'
              160  LOAD_CONST               0
              162  COMPARE_OP               >
              164  POP_JUMP_IF_FALSE   186  'to 186'

 L. 319       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _signer
              170  LOAD_METHOD              update
              172  LOAD_FAST                'data'
              174  LOAD_CONST               None
              176  LOAD_FAST                'update_len'
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
            186_0  COME_FROM           164  '164'

Parse error at or near `None' instruction at offset -1

    def _pad_cache_and_update--- This code section failed: ---

 L. 322         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _cache
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               16
               10  COMPARE_OP               <
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  <74>             
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L. 330        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _cache
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'len_cache'

 L. 331        28  LOAD_FAST                'len_cache'
               30  LOAD_CONST               0
               32  COMPARE_OP               >
               34  POP_JUMP_IF_FALSE    54  'to 54'

 L. 332        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _update
               40  LOAD_CONST               b'\x00'
               42  LOAD_CONST               16
               44  LOAD_FAST                'len_cache'
               46  BINARY_SUBTRACT  
               48  BINARY_MULTIPLY  
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            34  '34'

Parse error at or near `None' instruction at offset -1

    def encrypt--- This code section failed: ---

 L. 367         0  LOAD_FAST                'self'
                2  LOAD_ATTR                encrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 368        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'encrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 370        20  LOAD_FAST                'self'
               22  LOAD_ATTR                encrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                digest
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 372        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _cipher
               38  LOAD_ATTR                encrypt
               40  LOAD_FAST                'plaintext'
               42  LOAD_FAST                'output'
               44  LOAD_CONST               ('output',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  STORE_FAST               'ciphertext'

 L. 374        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _status
               54  LOAD_GLOBAL              MacStatus
               56  LOAD_ATTR                PROCESSING_AUTH_DATA
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    78  'to 78'

 L. 375        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _pad_cache_and_update
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L. 376        70  LOAD_GLOBAL              MacStatus
               72  LOAD_ATTR                PROCESSING_CIPHERTEXT
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _status
             78_0  COME_FROM            60  '60'

 L. 378        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _update
               82  LOAD_FAST                'output'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    94  'to 94'
               90  LOAD_FAST                'ciphertext'
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            88  '88'
               94  LOAD_FAST                'output'
             96_0  COME_FROM            92  '92'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 379       100  LOAD_FAST                'self'
              102  DUP_TOP          
              104  LOAD_ATTR                _msg_len
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'plaintext'
              110  CALL_FUNCTION_1       1  ''
              112  INPLACE_ADD      
              114  ROT_TWO          
              116  STORE_ATTR               _msg_len

 L. 382       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _msg_len
              122  LOAD_CONST               549755813632
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 383       128  LOAD_GLOBAL              ValueError
              130  LOAD_STR                 'Plaintext exceeds maximum length'
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 385       136  LOAD_FAST                'ciphertext'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def decrypt--- This code section failed: ---

 L. 420         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decrypt
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 421        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'decrypt() can only be called after initialization or an update()'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 423        20  LOAD_FAST                'self'
               22  LOAD_ATTR                decrypt
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                verify
               28  BUILD_LIST_2          2 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _next

 L. 425        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _status
               38  LOAD_GLOBAL              MacStatus
               40  LOAD_ATTR                PROCESSING_AUTH_DATA
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 426        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _pad_cache_and_update
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 427        54  LOAD_GLOBAL              MacStatus
               56  LOAD_ATTR                PROCESSING_CIPHERTEXT
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _status
             62_0  COME_FROM            44  '44'

 L. 429        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _update
               66  LOAD_FAST                'ciphertext'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 430        72  LOAD_FAST                'self'
               74  DUP_TOP          
               76  LOAD_ATTR                _msg_len
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'ciphertext'
               82  CALL_FUNCTION_1       1  ''
               84  INPLACE_ADD      
               86  ROT_TWO          
               88  STORE_ATTR               _msg_len

 L. 432        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _cipher
               94  LOAD_ATTR                decrypt
               96  LOAD_FAST                'ciphertext'
               98  LOAD_FAST                'output'
              100  LOAD_CONST               ('output',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def digest--- This code section failed: ---

 L. 445         0  LOAD_FAST                'self'
                2  LOAD_ATTR                digest
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 446        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'digest() cannot be called when decrypting or validating a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 448        20  LOAD_FAST                'self'
               22  LOAD_ATTR                digest
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 450        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _compute_mac
               34  CALL_METHOD_0         0  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _compute_mac(self):
        """Compute MAC without any FSM checks."""
        if self._tag:
            return self._tag
        self._pad_cache_and_update
        self._updatelong_to_bytes(8 * self._auth_len)8
        self._updatelong_to_bytes(8 * self._msg_len)8
        s_tag = self._signer.digest
        self._tag = self._tag_cipher.encrypts_tag[:self._mac_len]
        return self._tag

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join['%02x' % bord(x) for x in self.digest]

    def verify--- This code section failed: ---

 L. 495         0  LOAD_FAST                'self'
                2  LOAD_ATTR                verify
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _next
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 496        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'verify() cannot be called when encrypting a message'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 498        20  LOAD_FAST                'self'
               22  LOAD_ATTR                verify
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _next

 L. 500        30  LOAD_GLOBAL              get_random_bytes
               32  LOAD_CONST               16
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'secret'

 L. 502        38  LOAD_GLOBAL              BLAKE2s
               40  LOAD_ATTR                new
               42  LOAD_CONST               160
               44  LOAD_FAST                'secret'

 L. 503        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _compute_mac
               50  CALL_METHOD_0         0  ''

 L. 502        52  LOAD_CONST               ('digest_bits', 'key', 'data')
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  STORE_FAST               'mac1'

 L. 504        58  LOAD_GLOBAL              BLAKE2s
               60  LOAD_ATTR                new
               62  LOAD_CONST               160
               64  LOAD_FAST                'secret'

 L. 505        66  LOAD_FAST                'received_mac_tag'

 L. 504        68  LOAD_CONST               ('digest_bits', 'key', 'data')
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  STORE_FAST               'mac2'

 L. 507        74  LOAD_FAST                'mac1'
               76  LOAD_METHOD              digest
               78  CALL_METHOD_0         0  ''
               80  LOAD_FAST                'mac2'
               82  LOAD_METHOD              digest
               84  CALL_METHOD_0         0  ''
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 508        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'MAC check failed'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'

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

    def encrypt_and_digest(self, plaintext, output=None):
        """Perform encrypt() and digest() in one step.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
            a tuple with two items:

            - the ciphertext, as ``bytes``
            - the MAC tag, as ``bytes``

            The first item becomes ``None`` when the ``output`` parameter
            specified a location for the result.
        """
        return (
         self.encrypt(plaintext, output=output), self.digest)

    def decrypt_and_verify(self, ciphertext, received_mac_tag, output=None):
        """Perform decrypt() and verify() in one step.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
          received_mac_tag : byte string
            This is the *binary* MAC, as received from the sender.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return: the plaintext as ``bytes`` or ``None`` when the ``output``
            parameter specified a location for the result.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        plaintext = self.decrypt(ciphertext, output=output)
        self.verifyreceived_mac_tag
        return plaintext


def _create_gcm_cipher--- This code section failed: ---

 L. 603         0  SETUP_FINALLY        16  'to 16'

 L. 604         2  LOAD_FAST                'kwargs'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'key'
               12  POP_BLOCK        
               14  JUMP_FORWARD         68  'to 68'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 605        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                66  ''
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        58  'to 58'

 L. 606        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'Missing parameter:'
               34  LOAD_GLOBAL              str
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  BINARY_ADD       
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_BLOCK        
               48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  STORE_FAST               'e'
               54  DELETE_FAST              'e'
               56  JUMP_FORWARD         68  'to 68'
             58_0  COME_FROM_FINALLY    28  '28'
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  <48>             
               66  <48>             
             68_0  COME_FROM            56  '56'
             68_1  COME_FROM            14  '14'

 L. 608        68  LOAD_FAST                'kwargs'
               70  LOAD_METHOD              pop
               72  LOAD_STR                 'nonce'
               74  LOAD_CONST               None
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'nonce'

 L. 609        80  LOAD_FAST                'nonce'
               82  LOAD_CONST               None
               84  <117>                 0  ''
               86  POP_JUMP_IF_FALSE    96  'to 96'

 L. 610        88  LOAD_GLOBAL              get_random_bytes
               90  LOAD_CONST               16
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'nonce'
             96_0  COME_FROM            86  '86'

 L. 611        96  LOAD_FAST                'kwargs'
               98  LOAD_METHOD              pop
              100  LOAD_STR                 'mac_len'
              102  LOAD_CONST               16
              104  CALL_METHOD_2         2  ''
              106  STORE_FAST               'mac_len'

 L. 614       108  LOAD_FAST                'kwargs'
              110  LOAD_METHOD              pop
              112  LOAD_STR                 'use_clmul'
              114  LOAD_CONST               True
              116  CALL_METHOD_2         2  ''
              118  STORE_FAST               'use_clmul'

 L. 615       120  LOAD_FAST                'use_clmul'
              122  POP_JUMP_IF_FALSE   134  'to 134'
              124  LOAD_GLOBAL              _ghash_clmul
              126  POP_JUMP_IF_FALSE   134  'to 134'

 L. 616       128  LOAD_GLOBAL              _ghash_clmul
              130  STORE_FAST               'ghash_c'
              132  JUMP_FORWARD        138  'to 138'
            134_0  COME_FROM           126  '126'
            134_1  COME_FROM           122  '122'

 L. 618       134  LOAD_GLOBAL              _ghash_portable
              136  STORE_FAST               'ghash_c'
            138_0  COME_FROM           132  '132'

 L. 620       138  LOAD_GLOBAL              GcmMode
              140  LOAD_FAST                'factory'
              142  LOAD_FAST                'key'
              144  LOAD_FAST                'nonce'
              146  LOAD_FAST                'mac_len'
              148  LOAD_FAST                'kwargs'
              150  LOAD_FAST                'ghash_c'
              152  CALL_FUNCTION_6       6  ''
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20