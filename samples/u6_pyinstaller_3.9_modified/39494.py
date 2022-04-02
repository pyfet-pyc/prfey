# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\signals.py
from aiohttp.frozenlist import FrozenList
__all__ = ('Signal', )

class Signal(FrozenList):
    __doc__ = 'Coroutine-based signal implementation.\n\n    To connect a callback to a signal, use any list method.\n\n    Signals are fired using the send() coroutine, which takes named\n    arguments.\n    '
    __slots__ = ('_owner', )

    def __init__(self, owner):
        super().__init__()
        self._owner = owner

    def __repr__(self):
        return '<Signal owner={}, frozen={}, {!r}>'.format(self._owner, self.frozen, list(self))

    async def send--- This code section failed: ---

 L.  30         0  LOAD_FAST                'self'
                2  LOAD_ATTR                frozen
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L.  31         6  LOAD_GLOBAL              RuntimeError
                8  LOAD_STR                 'Cannot send non-frozen signal.'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.  33        14  LOAD_FAST                'self'
               16  GET_ITER         
               18  FOR_ITER             44  'to 44'
               20  STORE_FAST               'receiver'

 L.  34        22  LOAD_FAST                'receiver'
               24  LOAD_FAST                'args'
               26  BUILD_MAP_0           0 
               28  LOAD_FAST                'kwargs'
               30  <164>                 1  ''
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  JUMP_BACK            18  'to 18'

Parse error at or near `<164>' instruction at offset 30