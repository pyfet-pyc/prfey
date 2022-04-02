# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\backends\chainer.py
"""
Keyring Chainer - iterates over other viable backends to
discover passwords in each.
"""
from .. import backend
from ..util import properties
from . import fail

class ChainerBackend(backend.KeyringBackend):
    __doc__ = '\n    >>> ChainerBackend()\n    <keyring.backends.chainer.ChainerBackend object at ...>\n    '
    viable = True

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        """
        If there are backends to chain, high priority
        Otherwise very low priority since our operation when empty
        is the same as null.
        """
        if len(cls.backends) > 1:
            return 10
        return fail.Keyring.priority - 1

    @properties.ClassProperty
    @classmethod
    def backends(cls):
        """
        Discover all keyrings for chaining.
        """

        def allow(keyring):
            limit = backend._limit or bool
            return not isinstance(keyring, ChainerBackend) and limit(keyring) and keyring.priority > 0

        allowed = filter(allow, backend.get_all_keyring())
        return sorted(allowed, key=(backend.by_priority), reverse=True)

    def get_password--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_ATTR                backends
                4  GET_ITER         
              6_0  COME_FROM            38  '38'
              6_1  COME_FROM            28  '28'
                6  FOR_ITER             40  'to 40'
                8  STORE_FAST               'keyring'

 L.  51        10  LOAD_FAST                'keyring'
               12  LOAD_METHOD              get_password
               14  LOAD_FAST                'service'
               16  LOAD_FAST                'username'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'password'

 L.  52        22  LOAD_FAST                'password'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE_BACK     6  'to 6'

 L.  53        30  LOAD_FAST                'password'
               32  ROT_TWO          
               34  POP_TOP          
               36  RETURN_VALUE     
               38  JUMP_BACK             6  'to 6'
             40_0  COME_FROM             6  '6'

Parse error at or near `<117>' instruction at offset 26

    def set_password--- This code section failed: ---

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                backends
                4  GET_ITER         
              6_0  COME_FROM            50  '50'
              6_1  COME_FROM            46  '46'
                6  FOR_ITER             52  'to 52'
                8  STORE_FAST               'keyring'

 L.  57        10  SETUP_FINALLY        32  'to 32'

 L.  58        12  LOAD_FAST                'keyring'
               14  LOAD_METHOD              set_password
               16  LOAD_FAST                'service'
               18  LOAD_FAST                'username'
               20  LOAD_FAST                'password'
               22  CALL_METHOD_3         3  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    10  '10'

 L.  59        32  DUP_TOP          
               34  LOAD_GLOBAL              NotImplementedError
               36  <121>                48  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  60        44  POP_EXCEPT       
               46  JUMP_BACK             6  'to 6'
               48  <48>             
               50  JUMP_BACK             6  'to 6'
             52_0  COME_FROM             6  '6'

Parse error at or near `ROT_TWO' instruction at offset 26

    def delete_password--- This code section failed: ---

 L.  63         0  LOAD_FAST                'self'
                2  LOAD_ATTR                backends
                4  GET_ITER         
              6_0  COME_FROM            48  '48'
              6_1  COME_FROM            44  '44'
                6  FOR_ITER             50  'to 50'
                8  STORE_FAST               'keyring'

 L.  64        10  SETUP_FINALLY        30  'to 30'

 L.  65        12  LOAD_FAST                'keyring'
               14  LOAD_METHOD              delete_password
               16  LOAD_FAST                'service'
               18  LOAD_FAST                'username'
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  POP_TOP          
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    10  '10'

 L.  66        30  DUP_TOP          
               32  LOAD_GLOBAL              NotImplementedError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  67        42  POP_EXCEPT       
               44  JUMP_BACK             6  'to 6'
               46  <48>             
               48  JUMP_BACK             6  'to 6'
             50_0  COME_FROM             6  '6'

Parse error at or near `ROT_TWO' instruction at offset 24

    def get_credential--- This code section failed: ---

 L.  70         0  LOAD_FAST                'self'
                2  LOAD_ATTR                backends
                4  GET_ITER         
              6_0  COME_FROM            38  '38'
              6_1  COME_FROM            28  '28'
                6  FOR_ITER             40  'to 40'
                8  STORE_FAST               'keyring'

 L.  71        10  LOAD_FAST                'keyring'
               12  LOAD_METHOD              get_credential
               14  LOAD_FAST                'service'
               16  LOAD_FAST                'username'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'credential'

 L.  72        22  LOAD_FAST                'credential'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE_BACK     6  'to 6'

 L.  73        30  LOAD_FAST                'credential'
               32  ROT_TWO          
               34  POP_TOP          
               36  RETURN_VALUE     
               38  JUMP_BACK             6  'to 6'
             40_0  COME_FROM             6  '6'

Parse error at or near `<117>' instruction at offset 26