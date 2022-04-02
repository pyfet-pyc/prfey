# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\mime\multipart.py
"""Base class for MIME multipart/* type messages."""
__all__ = [
 'MIMEMultipart']
from email.mime.base import MIMEBase

class MIMEMultipart(MIMEBase):
    __doc__ = 'Base class for MIME multipart/* type messages.'

    def __init__--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              MIMEBase
                2  LOAD_ATTR                __init__
                4  LOAD_FAST                'self'
                6  LOAD_STR                 'multipart'
                8  LOAD_FAST                '_subtype'
               10  BUILD_TUPLE_3         3 
               12  LOAD_STR                 'policy'
               14  LOAD_FAST                'policy'
               16  BUILD_MAP_1           1 
               18  LOAD_FAST                '_params'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  POP_TOP          

 L.  42        26  BUILD_LIST_0          0 
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _payload

 L.  44        32  LOAD_FAST                '_subparts'
               34  POP_JUMP_IF_FALSE    56  'to 56'

 L.  45        36  LOAD_FAST                '_subparts'
               38  GET_ITER         
             40_0  COME_FROM            54  '54'
               40  FOR_ITER             56  'to 56'
               42  STORE_FAST               'p'

 L.  46        44  LOAD_FAST                'self'
               46  LOAD_METHOD              attach
               48  LOAD_FAST                'p'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
               54  JUMP_BACK            40  'to 40'
             56_0  COME_FROM            40  '40'
             56_1  COME_FROM            34  '34'

 L.  47        56  LOAD_FAST                'boundary'
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L.  48        60  LOAD_FAST                'self'
               62  LOAD_METHOD              set_boundary
               64  LOAD_FAST                'boundary'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
             70_0  COME_FROM            58  '58'

Parse error at or near `None' instruction at offset -1