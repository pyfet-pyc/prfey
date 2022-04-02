# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Util\strxor.py
from Crypto.Util._raw_api import load_pycryptodome_raw_lib, c_size_t, create_string_buffer, get_raw_buffer, c_uint8_ptr, is_writeable_buffer
_raw_strxor = load_pycryptodome_raw_lib('Crypto.Util._strxor', '\n                    void strxor(const uint8_t *in1,\n                                const uint8_t *in2,\n                                uint8_t *out, size_t len);\n                    void strxor_c(const uint8_t *in,\n                                  uint8_t c,\n                                  uint8_t *out,\n                                  size_t len);\n                    ')

def strxor--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'term1'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'term2'
               10  CALL_FUNCTION_1       1  ''
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  64        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'Only byte strings of equal length can be xored'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L.  66        24  LOAD_FAST                'output'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L.  67        32  LOAD_GLOBAL              create_string_buffer
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'term1'
               38  CALL_FUNCTION_1       1  ''
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'result'
               44  JUMP_FORWARD         98  'to 98'
             46_0  COME_FROM            30  '30'

 L.  70        46  LOAD_FAST                'output'
               48  STORE_FAST               'result'

 L.  72        50  LOAD_GLOBAL              is_writeable_buffer
               52  LOAD_FAST                'output'
               54  CALL_FUNCTION_1       1  ''
               56  POP_JUMP_IF_TRUE     66  'to 66'

 L.  73        58  LOAD_GLOBAL              TypeError
               60  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            56  '56'

 L.  75        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'term1'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'output'
               76  CALL_FUNCTION_1       1  ''
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L.  76        82  LOAD_GLOBAL              ValueError
               84  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L.  77        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'term1'
               90  CALL_FUNCTION_1       1  ''

 L.  76        92  BINARY_MODULO    
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            80  '80'
             98_1  COME_FROM            44  '44'

 L.  79        98  LOAD_GLOBAL              _raw_strxor
              100  LOAD_METHOD              strxor
              102  LOAD_GLOBAL              c_uint8_ptr
              104  LOAD_FAST                'term1'
              106  CALL_FUNCTION_1       1  ''

 L.  80       108  LOAD_GLOBAL              c_uint8_ptr
              110  LOAD_FAST                'term2'
              112  CALL_FUNCTION_1       1  ''

 L.  81       114  LOAD_GLOBAL              c_uint8_ptr
              116  LOAD_FAST                'result'
              118  CALL_FUNCTION_1       1  ''

 L.  82       120  LOAD_GLOBAL              c_size_t
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'term1'
              126  CALL_FUNCTION_1       1  ''
              128  CALL_FUNCTION_1       1  ''

 L.  79       130  CALL_METHOD_4         4  ''
              132  POP_TOP          

 L.  84       134  LOAD_FAST                'output'
              136  LOAD_CONST               None
              138  <117>                 0  ''
              140  POP_JUMP_IF_FALSE   150  'to 150'

 L.  85       142  LOAD_GLOBAL              get_raw_buffer
              144  LOAD_FAST                'result'
              146  CALL_FUNCTION_1       1  ''
              148  RETURN_VALUE     
            150_0  COME_FROM           140  '140'

 L.  87       150  LOAD_CONST               None
              152  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 28


def strxor_c--- This code section failed: ---

 L. 106         0  LOAD_CONST               0
                2  LOAD_FAST                'c'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_CONST               256
               14  COMPARE_OP               <
               16  POP_JUMP_IF_TRUE     30  'to 30'
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM            10  '10'
               20  POP_TOP          
             22_0  COME_FROM            18  '18'

 L. 107        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'c must be in range(256)'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L. 109        30  LOAD_FAST                'output'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 110        38  LOAD_GLOBAL              create_string_buffer
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'term'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'result'
               50  JUMP_FORWARD        104  'to 104'
             52_0  COME_FROM            36  '36'

 L. 113        52  LOAD_FAST                'output'
               54  STORE_FAST               'result'

 L. 115        56  LOAD_GLOBAL              is_writeable_buffer
               58  LOAD_FAST                'output'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 116        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'output must be a bytearray or a writeable memoryview'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 118        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'term'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'output'
               82  CALL_FUNCTION_1       1  ''
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 119        88  LOAD_GLOBAL              ValueError
               90  LOAD_STR                 'output must have the same length as the input  (%d bytes)'

 L. 120        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'term'
               96  CALL_FUNCTION_1       1  ''

 L. 119        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            50  '50'

 L. 122       104  LOAD_GLOBAL              _raw_strxor
              106  LOAD_METHOD              strxor_c
              108  LOAD_GLOBAL              c_uint8_ptr
              110  LOAD_FAST                'term'
              112  CALL_FUNCTION_1       1  ''

 L. 123       114  LOAD_FAST                'c'

 L. 124       116  LOAD_GLOBAL              c_uint8_ptr
              118  LOAD_FAST                'result'
              120  CALL_FUNCTION_1       1  ''

 L. 125       122  LOAD_GLOBAL              c_size_t
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'term'
              128  CALL_FUNCTION_1       1  ''
              130  CALL_FUNCTION_1       1  ''

 L. 122       132  CALL_METHOD_4         4  ''
              134  POP_TOP          

 L. 128       136  LOAD_FAST                'output'
              138  LOAD_CONST               None
              140  <117>                 0  ''
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L. 129       144  LOAD_GLOBAL              get_raw_buffer
              146  LOAD_FAST                'result'
              148  CALL_FUNCTION_1       1  ''
              150  RETURN_VALUE     
            152_0  COME_FROM           142  '142'

 L. 131       152  LOAD_CONST               None
              154  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 34


def _strxor_direct(term1, term2, result):
    """Very fast XOR - check conditions!"""
    _raw_strxor.strxorterm1term2resultc_size_t(len(term1))