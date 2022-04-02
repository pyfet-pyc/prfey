# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\_EKSBlowfish.py
import sys
from Crypto.Cipher import _create_cipher
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, c_size_t, c_uint8_ptr, c_uint
_raw_blowfish_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_eksblowfish', '\n        int EKSBlowfish_start_operation(const uint8_t key[],\n                                        size_t key_len,\n                                        const uint8_t salt[16],\n                                        size_t salt_len,\n                                        unsigned cost,\n                                        unsigned invert,\n                                        void **pResult);\n        int EKSBlowfish_encrypt(const void *state,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n        int EKSBlowfish_decrypt(const void *state,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n        int EKSBlowfish_stop_operation(void *state);\n        ')

def _create_base_cipher--- This code section failed: ---

 L.  66         0  SETUP_FINALLY        36  'to 36'

 L.  67         2  LOAD_FAST                'dict_parameters'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'key'

 L.  68        12  LOAD_FAST                'dict_parameters'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'salt'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'salt'

 L.  69        22  LOAD_FAST                'dict_parameters'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'cost'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'cost'
               32  POP_BLOCK        
               34  JUMP_FORWARD         88  'to 88'
             36_0  COME_FROM_FINALLY     0  '0'

 L.  70        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  <121>                86  ''
               42  POP_TOP          
               44  STORE_FAST               'e'
               46  POP_TOP          
               48  SETUP_FINALLY        78  'to 78'

 L.  71        50  LOAD_GLOBAL              TypeError
               52  LOAD_STR                 'Missing EKSBlowfish parameter: '
               54  LOAD_GLOBAL              str
               56  LOAD_FAST                'e'
               58  CALL_FUNCTION_1       1  ''
               60  BINARY_ADD       
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_BLOCK        
               68  POP_EXCEPT       
               70  LOAD_CONST               None
               72  STORE_FAST               'e'
               74  DELETE_FAST              'e'
               76  JUMP_FORWARD         88  'to 88'
             78_0  COME_FROM_FINALLY    48  '48'
               78  LOAD_CONST               None
               80  STORE_FAST               'e'
               82  DELETE_FAST              'e'
               84  <48>             
               86  <48>             
             88_0  COME_FROM            76  '76'
             88_1  COME_FROM            34  '34'

 L.  72        88  LOAD_FAST                'dict_parameters'
               90  LOAD_METHOD              pop
               92  LOAD_STR                 'invert'
               94  LOAD_CONST               True
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'invert'

 L.  74       100  LOAD_GLOBAL              len
              102  LOAD_FAST                'key'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_GLOBAL              key_size
              108  <118>                 1  ''
              110  POP_JUMP_IF_FALSE   128  'to 128'

 L.  75       112  LOAD_GLOBAL              ValueError
              114  LOAD_STR                 'Incorrect EKSBlowfish key length (%d bytes)'
              116  LOAD_GLOBAL              len
              118  LOAD_FAST                'key'
              120  CALL_FUNCTION_1       1  ''
              122  BINARY_MODULO    
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           110  '110'

 L.  77       128  LOAD_GLOBAL              _raw_blowfish_lib
              130  LOAD_ATTR                EKSBlowfish_start_operation
              132  STORE_FAST               'start_operation'

 L.  78       134  LOAD_GLOBAL              _raw_blowfish_lib
              136  LOAD_ATTR                EKSBlowfish_stop_operation
              138  STORE_FAST               'stop_operation'

 L.  80       140  LOAD_GLOBAL              VoidPointer
              142  CALL_FUNCTION_0       0  ''
              144  STORE_FAST               'void_p'

 L.  81       146  LOAD_FAST                'start_operation'
              148  LOAD_GLOBAL              c_uint8_ptr
              150  LOAD_FAST                'key'
              152  CALL_FUNCTION_1       1  ''

 L.  82       154  LOAD_GLOBAL              c_size_t
              156  LOAD_GLOBAL              len
              158  LOAD_FAST                'key'
              160  CALL_FUNCTION_1       1  ''
              162  CALL_FUNCTION_1       1  ''

 L.  83       164  LOAD_GLOBAL              c_uint8_ptr
              166  LOAD_FAST                'salt'
              168  CALL_FUNCTION_1       1  ''

 L.  84       170  LOAD_GLOBAL              c_size_t
              172  LOAD_GLOBAL              len
              174  LOAD_FAST                'salt'
              176  CALL_FUNCTION_1       1  ''
              178  CALL_FUNCTION_1       1  ''

 L.  85       180  LOAD_GLOBAL              c_uint
              182  LOAD_FAST                'cost'
              184  CALL_FUNCTION_1       1  ''

 L.  86       186  LOAD_GLOBAL              c_uint
              188  LOAD_GLOBAL              int
              190  LOAD_FAST                'invert'
              192  CALL_FUNCTION_1       1  ''
              194  CALL_FUNCTION_1       1  ''

 L.  87       196  LOAD_FAST                'void_p'
              198  LOAD_METHOD              address_of
              200  CALL_METHOD_0         0  ''

 L.  81       202  CALL_FUNCTION_7       7  ''
              204  STORE_FAST               'result'

 L.  88       206  LOAD_FAST                'result'
              208  POP_JUMP_IF_FALSE   222  'to 222'

 L.  89       210  LOAD_GLOBAL              ValueError
              212  LOAD_STR                 'Error %X while instantiating the EKSBlowfish cipher'

 L.  90       214  LOAD_FAST                'result'

 L.  89       216  BINARY_MODULO    
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
            222_0  COME_FROM           208  '208'

 L.  91       222  LOAD_GLOBAL              SmartPointer
              224  LOAD_FAST                'void_p'
              226  LOAD_METHOD              get
              228  CALL_METHOD_0         0  ''
              230  LOAD_FAST                'stop_operation'
              232  CALL_FUNCTION_2       2  ''
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 40


def new--- This code section failed: ---

 L. 122         0  LOAD_FAST                'salt'
                2  LOAD_FAST                'cost'
                4  LOAD_FAST                'invert'
                6  LOAD_CONST               ('salt', 'cost', 'invert')
                8  BUILD_CONST_KEY_MAP_3     3 
               10  STORE_FAST               'kwargs'

 L. 123        12  LOAD_GLOBAL              _create_cipher
               14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                modules
               18  LOAD_GLOBAL              __name__
               20  BINARY_SUBSCR    
               22  LOAD_FAST                'key'
               24  LOAD_FAST                'mode'
               26  BUILD_TUPLE_3         3 
               28  BUILD_MAP_0           0 
               30  LOAD_FAST                'kwargs'
               32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 32


MODE_ECB = 1
block_size = 8
key_size = range(0, 73)