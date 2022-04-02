# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\unicode_utils.py
import unicodedata, sys
from setuptools.extern import six

def decompose(path):
    if isinstance(path, six.text_type):
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
             40_0  COME_FROM            86  '86'
             40_1  COME_FROM            82  '82'
             40_2  COME_FROM            78  '78'
               40  FOR_ITER             88  'to 88'
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
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    84  'to 84'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L.  36        76  POP_EXCEPT       
               78  JUMP_BACK            40  'to 40'
               80  POP_EXCEPT       
               82  JUMP_BACK            40  'to 40'
             84_0  COME_FROM            68  '68'
               84  END_FINALLY      
               86  JUMP_BACK            40  'to 40'
             88_0  COME_FROM            40  '40'

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
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  44        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30