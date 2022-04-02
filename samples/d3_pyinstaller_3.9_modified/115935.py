# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\unicode_utils.py
import unicodedata, sys
from setuptools.extern import six

def decompose--- This code section failed: ---

 L.   9         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                text_type
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L.  10        12  LOAD_GLOBAL              unicodedata
               14  LOAD_METHOD              normalize
               16  LOAD_STR                 'NFD'
               18  LOAD_FAST                'path'
               20  CALL_METHOD_2         2  ''
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'

 L.  11        24  SETUP_FINALLY        62  'to 62'

 L.  12        26  LOAD_FAST                'path'
               28  LOAD_METHOD              decode
               30  LOAD_STR                 'utf-8'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'path'

 L.  13        36  LOAD_GLOBAL              unicodedata
               38  LOAD_METHOD              normalize
               40  LOAD_STR                 'NFD'
               42  LOAD_FAST                'path'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'path'

 L.  14        48  LOAD_FAST                'path'
               50  LOAD_METHOD              encode
               52  LOAD_STR                 'utf-8'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'path'
               58  POP_BLOCK        
               60  JUMP_FORWARD         80  'to 80'
             62_0  COME_FROM_FINALLY    24  '24'

 L.  15        62  DUP_TOP          
               64  LOAD_GLOBAL              UnicodeError
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  16        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            60  '60'

 L.  17        80  LOAD_FAST                'path'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 66


def filesys_decode--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                text_type
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L.  27        12  LOAD_FAST                'path'
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  29        16  LOAD_GLOBAL              sys
               18  LOAD_METHOD              getfilesystemencoding
               20  CALL_METHOD_0         0  ''
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  LOAD_STR                 'utf-8'
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'fs_enc'

 L.  30        28  LOAD_FAST                'fs_enc'
               30  LOAD_STR                 'utf-8'
               32  BUILD_TUPLE_2         2 
               34  STORE_FAST               'candidates'

 L.  32        36  LOAD_FAST                'candidates'
               38  GET_ITER         
             40_0  COME_FROM            84  '84'
             40_1  COME_FROM            80  '80'
             40_2  COME_FROM            76  '76'
               40  FOR_ITER             86  'to 86'
               42  STORE_FAST               'enc'

 L.  33        44  SETUP_FINALLY        62  'to 62'

 L.  34        46  LOAD_FAST                'path'
               48  LOAD_METHOD              decode
               50  LOAD_FAST                'enc'
               52  CALL_METHOD_1         1  ''
               54  POP_BLOCK        
               56  ROT_TWO          
               58  POP_TOP          
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    44  '44'

 L.  35        62  DUP_TOP          
               64  LOAD_GLOBAL              UnicodeDecodeError
               66  <121>                82  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  36        74  POP_EXCEPT       
               76  JUMP_BACK            40  'to 40'
               78  POP_EXCEPT       
               80  JUMP_BACK            40  'to 40'
               82  <48>             
               84  JUMP_BACK            40  'to 40'
             86_0  COME_FROM            40  '40'

Parse error at or near `ROT_TWO' instruction at offset 56


def try_encode--- This code section failed: ---

 L.  41         0  SETUP_FINALLY        14  'to 14'

 L.  42         2  LOAD_FAST                'string'
                4  LOAD_METHOD              encode
                6  LOAD_FAST                'enc'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  43        14  DUP_TOP          
               16  LOAD_GLOBAL              UnicodeEncodeError
               18  <121>                32  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  44        26  POP_EXCEPT       
               28  LOAD_CONST               None
               30  RETURN_VALUE     
               32  <48>             

Parse error at or near `<121>' instruction at offset 18