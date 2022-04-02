# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\util\__init__.py
import functools

def once(func):
    """
    Decorate func so it's only ever called the first time.

    This decorator can ensure that an expensive or non-idempotent function
    will not be expensive on subsequent calls and is idempotent.

    >>> func = once(lambda a: a+3)
    >>> func(3)
    6
    >>> func(9)
    6
    >>> func('12')
    6
    """

    def wrapper--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'func'
                4  LOAD_STR                 'always_returns'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L.  22        10  LOAD_DEREF               'func'
               12  LOAD_FAST                'args'
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  LOAD_DEREF               'func'
               24  STORE_ATTR               always_returns
             26_0  COME_FROM             8  '8'

 L.  23        26  LOAD_DEREF               'func'
               28  LOAD_ATTR                always_returns
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 18

    return functools.wraps(func)(wrapper)


def suppress_exceptions--- This code section failed: ---

 L.  33         0  LOAD_FAST                'callables'
                2  GET_ITER         
                4  FOR_ITER             42  'to 42'
                6  STORE_FAST               'callable'

 L.  34         8  SETUP_FINALLY        22  'to 22'

 L.  35        10  LOAD_FAST                'callable'
               12  CALL_FUNCTION_0       0  ''
               14  YIELD_VALUE      
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_BACK             4  'to 4'
             22_0  COME_FROM_FINALLY     8  '8'

 L.  36        22  DUP_TOP          
               24  LOAD_FAST                'exceptions'
               26  <121>                38  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  37        34  POP_EXCEPT       
               36  JUMP_BACK             4  'to 4'
               38  <48>             
               40  JUMP_BACK             4  'to 4'

Parse error at or near `<121>' instruction at offset 26