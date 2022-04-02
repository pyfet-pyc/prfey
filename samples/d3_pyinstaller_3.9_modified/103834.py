# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\__init__.py
from __future__ import absolute_import, division, print_function
_default_backend = None

def default_backend--- This code section failed: ---

 L.  14         0  LOAD_GLOBAL              _default_backend
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  15         8  LOAD_CONST               0
               10  LOAD_CONST               ('backend',)
               12  IMPORT_NAME_ATTR         cryptography.hazmat.backends.openssl.backend
               14  IMPORT_FROM              backend
               16  STORE_FAST               'backend'
               18  POP_TOP          

 L.  17        20  LOAD_FAST                'backend'
               22  STORE_GLOBAL             _default_backend
             24_0  COME_FROM             6  '6'

 L.  19        24  LOAD_GLOBAL              _default_backend
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_backend--- This code section failed: ---

 L.  23         0  LOAD_FAST                'backend'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  24         8  LOAD_GLOBAL              default_backend
               10  CALL_FUNCTION_0       0  ''
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L.  26        14  LOAD_FAST                'backend'
               16  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


# global _default_backend ## Warning: Unused global