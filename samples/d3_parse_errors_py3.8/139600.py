# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\unicode_utils.py
import unicodedata, sys

def decompose(path):
    if isinstance(path, str):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass
    else:
        return path


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
             38_0  COME_FROM            84  '84'
             38_1  COME_FROM            80  '80'
             38_2  COME_FROM            76  '76'
               38  FOR_ITER             86  'to 86'
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
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    82  'to 82'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  34        74  POP_EXCEPT       
               76  JUMP_BACK            38  'to 38'
               78  POP_EXCEPT       
               80  JUMP_BACK            38  'to 38'
             82_0  COME_FROM            66  '66'
               82  END_FINALLY      
               84  JUMP_BACK            38  'to 38'
             86_0  COME_FROM            38  '38'

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
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  42        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30