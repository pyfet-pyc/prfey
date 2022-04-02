# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\random\_pickle.py
from .mtrand import RandomState
from ._philox import Philox
from ._pcg64 import PCG64
from ._sfc64 import SFC64
from ._generator import Generator
from ._mt19937 import MT19937
BitGenerators = {'MT19937':MT19937, 
 'PCG64':PCG64, 
 'Philox':Philox, 
 'SFC64':SFC64}

def __generator_ctor--- This code section failed: ---

 L.  30         0  LOAD_FAST                'bit_generator_name'
                2  LOAD_GLOBAL              BitGenerators
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  31         8  LOAD_GLOBAL              BitGenerators
               10  LOAD_FAST                'bit_generator_name'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'bit_generator'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L.  33        18  LOAD_GLOBAL              ValueError
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'bit_generator_name'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_STR                 ' is not a known BitGenerator module.'
               28  BINARY_ADD       
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            16  '16'

 L.  36        34  LOAD_GLOBAL              Generator
               36  LOAD_FAST                'bit_generator'
               38  CALL_FUNCTION_0       0  ''
               40  CALL_FUNCTION_1       1  ''
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def __bit_generator_ctor--- This code section failed: ---

 L.  53         0  LOAD_FAST                'bit_generator_name'
                2  LOAD_GLOBAL              BitGenerators
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  54         8  LOAD_GLOBAL              BitGenerators
               10  LOAD_FAST                'bit_generator_name'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'bit_generator'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L.  56        18  LOAD_GLOBAL              ValueError
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'bit_generator_name'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_STR                 ' is not a known BitGenerator module.'
               28  BINARY_ADD       
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            16  '16'

 L.  59        34  LOAD_FAST                'bit_generator'
               36  CALL_FUNCTION_0       0  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def __randomstate_ctor--- This code section failed: ---

 L.  76         0  LOAD_FAST                'bit_generator_name'
                2  LOAD_GLOBAL              BitGenerators
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  77         8  LOAD_GLOBAL              BitGenerators
               10  LOAD_FAST                'bit_generator_name'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'bit_generator'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L.  79        18  LOAD_GLOBAL              ValueError
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'bit_generator_name'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_STR                 ' is not a known BitGenerator module.'
               28  BINARY_ADD       
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            16  '16'

 L.  82        34  LOAD_GLOBAL              RandomState
               36  LOAD_FAST                'bit_generator'
               38  CALL_FUNCTION_0       0  ''
               40  CALL_FUNCTION_1       1  ''
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1