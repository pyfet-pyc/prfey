# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\DES3.py
"""
Module's constants for the modes of operation supported with Triple DES:

:var MODE_ECB: :ref:`Electronic Code Book (ECB) <ecb_mode>`
:var MODE_CBC: :ref:`Cipher-Block Chaining (CBC) <cbc_mode>`
:var MODE_CFB: :ref:`Cipher FeedBack (CFB) <cfb_mode>`
:var MODE_OFB: :ref:`Output FeedBack (OFB) <ofb_mode>`
:var MODE_CTR: :ref:`CounTer Mode (CTR) <ctr_mode>`
:var MODE_OPENPGP:  :ref:`OpenPGP Mode <openpgp_mode>`
:var MODE_EAX: :ref:`EAX Mode <eax_mode>`
"""
import sys
from Crypto.Cipher import _create_cipher
from Crypto.Util.py3compat import byte_string, bchr, bord, bstr
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, c_size_t
_raw_des3_lib = load_pycryptodome_raw_lib('Crypto.Cipher._raw_des3', '\n                    int DES3_start_operation(const uint8_t key[],\n                                             size_t key_len,\n                                             void **pResult);\n                    int DES3_encrypt(const void *state,\n                                     const uint8_t *in,\n                                     uint8_t *out,\n                                     size_t data_len);\n                    int DES3_decrypt(const void *state,\n                                     const uint8_t *in,\n                                     uint8_t *out,\n                                     size_t data_len);\n                    int DES3_stop_operation(void *state);\n                    ')

def adjust_key_parity--- This code section failed: ---

 L.  73         0  LOAD_CODE                <code_object parity_byte>
                2  LOAD_STR                 'adjust_key_parity.<locals>.parity_byte'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_DEREF              'parity_byte'

 L.  79         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'key_in'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              key_size
               16  <118>                 1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.  80        20  LOAD_GLOBAL              ValueError
               22  LOAD_STR                 'Not a valid TDES key'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  82        28  LOAD_CONST               b''
               30  LOAD_METHOD              join
               32  LOAD_CLOSURE             'parity_byte'
               34  BUILD_TUPLE_1         1 
               36  LOAD_LISTCOMP            '<code_object <listcomp>>'
               38  LOAD_STR                 'adjust_key_parity.<locals>.<listcomp>'
               40  MAKE_FUNCTION_8          'closure'
               42  LOAD_FAST                'key_in'
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'key_out'

 L.  84        52  LOAD_FAST                'key_out'
               54  LOAD_CONST               None
               56  LOAD_CONST               8
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'key_out'
               64  LOAD_CONST               8
               66  LOAD_CONST               16
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_TRUE    100  'to 100'
               76  LOAD_FAST                'key_out'
               78  LOAD_CONST               -16
               80  LOAD_CONST               -8
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'key_out'
               88  LOAD_CONST               -8
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   108  'to 108'
            100_0  COME_FROM            74  '74'

 L.  85       100  LOAD_GLOBAL              ValueError
              102  LOAD_STR                 'Triple DES key degenerates to single DES'
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            98  '98'

 L.  87       108  LOAD_FAST                'key_out'
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 16


def _create_base_cipher--- This code section failed: ---

 L.  94         0  SETUP_FINALLY        16  'to 16'

 L.  95         2  LOAD_FAST                'dict_parameters'
                4  LOAD_METHOD              pop
                6  LOAD_STR                 'key'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'key_in'
               12  POP_BLOCK        
               14  JUMP_FORWARD         42  'to 42'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  96        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                40  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  97        28  LOAD_GLOBAL              TypeError
               30  LOAD_STR                 "Missing 'key' parameter"
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
               36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
               40  <48>             
             42_0  COME_FROM            38  '38'
             42_1  COME_FROM            14  '14'

 L.  99        42  LOAD_GLOBAL              adjust_key_parity
               44  LOAD_GLOBAL              bstr
               46  LOAD_FAST                'key_in'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'key'

 L. 101        54  LOAD_GLOBAL              _raw_des3_lib
               56  LOAD_ATTR                DES3_start_operation
               58  STORE_FAST               'start_operation'

 L. 102        60  LOAD_GLOBAL              _raw_des3_lib
               62  LOAD_ATTR                DES3_stop_operation
               64  STORE_FAST               'stop_operation'

 L. 104        66  LOAD_GLOBAL              VoidPointer
               68  CALL_FUNCTION_0       0  ''
               70  STORE_FAST               'cipher'

 L. 105        72  LOAD_FAST                'start_operation'
               74  LOAD_FAST                'key'

 L. 106        76  LOAD_GLOBAL              c_size_t
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'key'
               82  CALL_FUNCTION_1       1  ''
               84  CALL_FUNCTION_1       1  ''

 L. 107        86  LOAD_FAST                'cipher'
               88  LOAD_METHOD              address_of
               90  CALL_METHOD_0         0  ''

 L. 105        92  CALL_FUNCTION_3       3  ''
               94  STORE_FAST               'result'

 L. 108        96  LOAD_FAST                'result'
               98  POP_JUMP_IF_FALSE   112  'to 112'

 L. 109       100  LOAD_GLOBAL              ValueError
              102  LOAD_STR                 'Error %X while instantiating the TDES cipher'

 L. 110       104  LOAD_FAST                'result'

 L. 109       106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            98  '98'

 L. 111       112  LOAD_GLOBAL              SmartPointer
              114  LOAD_FAST                'cipher'
              116  LOAD_METHOD              get
              118  CALL_METHOD_0         0  ''
              120  LOAD_FAST                'stop_operation'
              122  CALL_FUNCTION_2       2  ''
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20


def new--- This code section failed: ---

 L. 174         0  LOAD_GLOBAL              _create_cipher
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                modules
                6  LOAD_GLOBAL              __name__
                8  BINARY_SUBSCR    
               10  LOAD_FAST                'key'
               12  LOAD_FAST                'mode'
               14  BUILD_LIST_3          3 
               16  LOAD_FAST                'args'
               18  CALL_FINALLY         21  'to 21'
               20  WITH_CLEANUP_FINISH
               22  BUILD_MAP_0           0 
               24  LOAD_FAST                'kwargs'
               26  <164>                 1  ''
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
MODE_EAX = 9
block_size = 8
key_size = (16, 24)