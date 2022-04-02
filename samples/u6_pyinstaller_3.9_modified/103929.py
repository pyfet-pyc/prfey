# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\mime\base.py
"""Base class for MIME specializations."""
__all__ = [
 'MIMEBase']
import email.policy
from email import message

class MIMEBase(message.Message):
    __doc__ = 'Base class for MIME specializations.'

    def __init__--- This code section failed: ---

 L.  25         0  LOAD_FAST                'policy'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  26         8  LOAD_GLOBAL              email
               10  LOAD_ATTR                policy
               12  LOAD_ATTR                compat32
               14  STORE_FAST               'policy'
             16_0  COME_FROM             6  '6'

 L.  27        16  LOAD_GLOBAL              message
               18  LOAD_ATTR                Message
               20  LOAD_ATTR                __init__
               22  LOAD_FAST                'self'
               24  LOAD_FAST                'policy'
               26  LOAD_CONST               ('policy',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  POP_TOP          

 L.  28        32  LOAD_STR                 '%s/%s'
               34  LOAD_FAST                '_maintype'
               36  LOAD_FAST                '_subtype'
               38  BUILD_TUPLE_2         2 
               40  BINARY_MODULO    
               42  STORE_FAST               'ctype'

 L.  29        44  LOAD_FAST                'self'
               46  LOAD_ATTR                add_header
               48  LOAD_STR                 'Content-Type'
               50  LOAD_FAST                'ctype'
               52  BUILD_TUPLE_2         2 
               54  BUILD_MAP_0           0 
               56  LOAD_FAST                '_params'
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  POP_TOP          

 L.  30        64  LOAD_STR                 '1.0'
               66  LOAD_FAST                'self'
               68  LOAD_STR                 'MIME-Version'
               70  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1