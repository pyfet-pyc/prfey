# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Cipher\__init__.py
import os
from Crypto.Cipher._mode_ecb import _create_ecb_cipher
from Crypto.Cipher._mode_cbc import _create_cbc_cipher
from Crypto.Cipher._mode_cfb import _create_cfb_cipher
from Crypto.Cipher._mode_ofb import _create_ofb_cipher
from Crypto.Cipher._mode_ctr import _create_ctr_cipher
from Crypto.Cipher._mode_openpgp import _create_openpgp_cipher
from Crypto.Cipher._mode_ccm import _create_ccm_cipher
from Crypto.Cipher._mode_eax import _create_eax_cipher
from Crypto.Cipher._mode_siv import _create_siv_cipher
from Crypto.Cipher._mode_gcm import _create_gcm_cipher
from Crypto.Cipher._mode_ocb import _create_ocb_cipher
_modes = {1:_create_ecb_cipher, 
 2:_create_cbc_cipher, 
 3:_create_cfb_cipher, 
 5:_create_ofb_cipher, 
 6:_create_ctr_cipher, 
 7:_create_openpgp_cipher, 
 9:_create_eax_cipher}
_extra_modes = {8:_create_ccm_cipher, 
 10:_create_siv_cipher, 
 11:_create_gcm_cipher, 
 12:_create_ocb_cipher}

def _create_cipher--- This code section failed: ---

 L.  56         0  LOAD_FAST                'key'
                2  LOAD_FAST                'kwargs'
                4  LOAD_STR                 'key'
                6  STORE_SUBSCR     

 L.  58         8  LOAD_GLOBAL              dict
               10  LOAD_GLOBAL              _modes
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'modes'

 L.  59        16  LOAD_FAST                'kwargs'
               18  LOAD_METHOD              pop
               20  LOAD_STR                 'add_aes_modes'
               22  LOAD_CONST               False
               24  CALL_METHOD_2         2  ''
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  60        28  LOAD_FAST                'modes'
               30  LOAD_METHOD              update
               32  LOAD_GLOBAL              _extra_modes
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            26  '26'

 L.  61        38  LOAD_FAST                'mode'
               40  LOAD_FAST                'modes'
               42  <118>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L.  62        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'Mode not supported'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L.  64        54  LOAD_FAST                'args'
               56  POP_JUMP_IF_FALSE   188  'to 188'

 L.  65        58  LOAD_FAST                'mode'
               60  LOAD_CONST               (8, 9, 10, 11, 12)
               62  <118>                 0  ''
               64  POP_JUMP_IF_FALSE   100  'to 100'

 L.  66        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'args'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               1
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.  67        78  LOAD_GLOBAL              TypeError
               80  LOAD_STR                 'Too many arguments for this mode'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L.  68        86  LOAD_FAST                'args'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'kwargs'
               94  LOAD_STR                 'nonce'
               96  STORE_SUBSCR     
               98  JUMP_FORWARD        188  'to 188'
            100_0  COME_FROM            64  '64'

 L.  69       100  LOAD_FAST                'mode'
              102  LOAD_CONST               (2, 3, 5, 7)
              104  <118>                 0  ''
              106  POP_JUMP_IF_FALSE   142  'to 142'

 L.  70       108  LOAD_GLOBAL              len
              110  LOAD_FAST                'args'
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_CONST               1
              116  COMPARE_OP               >
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L.  71       120  LOAD_GLOBAL              TypeError
              122  LOAD_STR                 'Too many arguments for this mode'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L.  72       128  LOAD_FAST                'args'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'kwargs'
              136  LOAD_STR                 'IV'
              138  STORE_SUBSCR     
              140  JUMP_FORWARD        188  'to 188'
            142_0  COME_FROM           106  '106'

 L.  73       142  LOAD_FAST                'mode'
              144  LOAD_CONST               6
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   172  'to 172'

 L.  74       150  LOAD_GLOBAL              len
              152  LOAD_FAST                'args'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               0
              158  COMPARE_OP               >
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L.  75       162  LOAD_GLOBAL              TypeError
              164  LOAD_STR                 'Too many arguments for this mode'
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
              170  JUMP_FORWARD        188  'to 188'
            172_0  COME_FROM           148  '148'

 L.  76       172  LOAD_FAST                'mode'
              174  LOAD_CONST               1
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L.  77       180  LOAD_GLOBAL              TypeError
              182  LOAD_STR                 'IV is not meaningful for the ECB mode'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           170  '170'
            188_2  COME_FROM           160  '160'
            188_3  COME_FROM           140  '140'
            188_4  COME_FROM            98  '98'
            188_5  COME_FROM            56  '56'

 L.  79       188  LOAD_FAST                'modes'
              190  LOAD_FAST                'mode'
              192  BINARY_SUBSCR    
              194  LOAD_FAST                'factory'
              196  BUILD_TUPLE_1         1 
              198  BUILD_MAP_0           0 
              200  LOAD_FAST                'kwargs'
              202  <164>                 1  ''
              204  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 42