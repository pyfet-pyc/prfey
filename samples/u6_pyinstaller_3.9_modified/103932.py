# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\mime\text.py
"""Class representing text/* type MIME documents."""
__all__ = [
 'MIMEText']
from email.charset import Charset
from email.mime.nonmultipart import MIMENonMultipart

class MIMEText(MIMENonMultipart):
    __doc__ = 'Class for generating text/* type MIME documents.'

    def __init__--- This code section failed: ---

 L.  32         0  LOAD_FAST                '_charset'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    50  'to 50'

 L.  33         8  SETUP_FINALLY        28  'to 28'

 L.  34        10  LOAD_FAST                '_text'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'us-ascii'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  35        20  LOAD_STR                 'us-ascii'
               22  STORE_FAST               '_charset'
               24  POP_BLOCK        
               26  JUMP_FORWARD         50  'to 50'
             28_0  COME_FROM_FINALLY     8  '8'

 L.  36        28  DUP_TOP          
               30  LOAD_GLOBAL              UnicodeEncodeError
               32  <121>                48  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  37        40  LOAD_STR                 'utf-8'
               42  STORE_FAST               '_charset'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            26  '26'
             50_2  COME_FROM             6  '6'

 L.  39        50  LOAD_GLOBAL              MIMENonMultipart
               52  LOAD_ATTR                __init__
               54  LOAD_FAST                'self'
               56  LOAD_STR                 'text'
               58  LOAD_FAST                '_subtype'
               60  BUILD_TUPLE_3         3 
               62  LOAD_STR                 'policy'
               64  LOAD_FAST                'policy'
               66  BUILD_MAP_1           1 

 L.  40        68  LOAD_STR                 'charset'
               70  LOAD_GLOBAL              str
               72  LOAD_FAST                '_charset'
               74  CALL_FUNCTION_1       1  ''
               76  BUILD_MAP_1           1 

 L.  39        78  <164>                 1  ''
               80  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               82  POP_TOP          

 L.  42        84  LOAD_FAST                'self'
               86  LOAD_METHOD              set_payload
               88  LOAD_FAST                '_text'
               90  LOAD_FAST                '_charset'
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          

Parse error at or near `None' instruction at offset -1