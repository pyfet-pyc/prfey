# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\unicode_utils.py
import unicodedata, sys

def decompose--- This code section failed: ---

 L.   7         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L.   8        10  LOAD_GLOBAL              unicodedata
               12  LOAD_METHOD              normalize
               14  LOAD_STR                 'NFD'
               16  LOAD_FAST                'path'
               18  CALL_METHOD_2         2  ''
               20  RETURN_VALUE     
             22_0  COME_FROM             8  '8'

 L.   9        22  SETUP_FINALLY        60  'to 60'

 L.  10        24  LOAD_FAST                'path'
               26  LOAD_METHOD              decode
               28  LOAD_STR                 'utf-8'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'path'

 L.  11        34  LOAD_GLOBAL              unicodedata
               36  LOAD_METHOD              normalize
               38  LOAD_STR                 'NFD'
               40  LOAD_FAST                'path'
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'path'

 L.  12        46  LOAD_FAST                'path'
               48  LOAD_METHOD              encode
               50  LOAD_STR                 'utf-8'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'path'
               56  POP_BLOCK        
               58  JUMP_FORWARD         78  'to 78'
             60_0  COME_FROM_FINALLY    22  '22'

 L.  13        60  DUP_TOP          
               62  LOAD_GLOBAL              UnicodeError
               64  <121>                76  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  14        72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            58  '58'

 L.  15        78  LOAD_FAST                'path'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 64


def filesys_decode--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  25        10  LOAD_FAST                'path'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  27        14  LOAD_GLOBAL              sys
               16  LOAD_METHOD              getfilesystemencoding
               18  CALL_METHOD_0         0  ''
               20  JUMP_IF_TRUE_OR_POP    24  'to 24'
               22  LOAD_STR                 'utf-8'
             24_0  COME_FROM            20  '20'
               24  STORE_FAST               'fs_enc'

 L.  28        26  LOAD_FAST                'fs_enc'
               28  LOAD_STR                 'utf-8'
               30  BUILD_TUPLE_2         2 
               32  STORE_FAST               'candidates'

 L.  30        34  LOAD_FAST                'candidates'
               36  GET_ITER         
             38_0  COME_FROM            82  '82'
             38_1  COME_FROM            78  '78'
             38_2  COME_FROM            74  '74'
               38  FOR_ITER             84  'to 84'
               40  STORE_FAST               'enc'

 L.  31        42  SETUP_FINALLY        60  'to 60'

 L.  32        44  LOAD_FAST                'path'
               46  LOAD_METHOD              decode
               48  LOAD_FAST                'enc'
               50  CALL_METHOD_1         1  ''
               52  POP_BLOCK        
               54  ROT_TWO          
               56  POP_TOP          
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    42  '42'

 L.  33        60  DUP_TOP          
               62  LOAD_GLOBAL              UnicodeDecodeError
               64  <121>                80  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  34        72  POP_EXCEPT       
               74  JUMP_BACK            38  'to 38'
               76  POP_EXCEPT       
               78  JUMP_BACK            38  'to 38'
               80  <48>             
               82  JUMP_BACK            38  'to 38'
             84_0  COME_FROM            38  '38'

Parse error at or near `ROT_TWO' instruction at offset 54


def try_encode--- This code section failed: ---

 L.  39         0  SETUP_FINALLY        14  'to 14'

 L.  40         2  LOAD_FAST                'string'
                4  LOAD_METHOD              encode
                6  LOAD_FAST                'enc'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  41        14  DUP_TOP          
               16  LOAD_GLOBAL              UnicodeEncodeError
               18  <121>                32  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  42        26  POP_EXCEPT       
               28  LOAD_CONST               None
               30  RETURN_VALUE     
               32  <48>             

Parse error at or near `<121>' instruction at offset 18