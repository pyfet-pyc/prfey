# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: importlib_metadata\_itertools.py
from itertools import filterfalse

def unique_everseen--- This code section failed: ---

 L.   8         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'seen'

 L.   9         6  LOAD_FAST                'seen'
                8  LOAD_ATTR                add
               10  STORE_FAST               'seen_add'

 L.  10        12  LOAD_FAST                'key'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    54  'to 54'

 L.  11        20  LOAD_GLOBAL              filterfalse
               22  LOAD_FAST                'seen'
               24  LOAD_ATTR                __contains__
               26  LOAD_FAST                'iterable'
               28  CALL_FUNCTION_2       2  ''
               30  GET_ITER         
             32_0  COME_FROM            50  '50'
               32  FOR_ITER             52  'to 52'
               34  STORE_FAST               'element'

 L.  12        36  LOAD_FAST                'seen_add'
               38  LOAD_FAST                'element'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          

 L.  13        44  LOAD_FAST                'element'
               46  YIELD_VALUE      
               48  POP_TOP          
               50  JUMP_BACK            32  'to 32'
             52_0  COME_FROM            32  '32'
               52  JUMP_FORWARD         94  'to 94'
             54_0  COME_FROM            18  '18'

 L.  15        54  LOAD_FAST                'iterable'
               56  GET_ITER         
             58_0  COME_FROM            92  '92'
             58_1  COME_FROM            76  '76'
               58  FOR_ITER             94  'to 94'
               60  STORE_FAST               'element'

 L.  16        62  LOAD_FAST                'key'
               64  LOAD_FAST                'element'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'k'

 L.  17        70  LOAD_FAST                'k'
               72  LOAD_FAST                'seen'
               74  <118>                 1  ''
               76  POP_JUMP_IF_FALSE_BACK    58  'to 58'

 L.  18        78  LOAD_FAST                'seen_add'
               80  LOAD_FAST                'k'
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          

 L.  19        86  LOAD_FAST                'element'
               88  YIELD_VALUE      
               90  POP_TOP          
               92  JUMP_BACK            58  'to 58'
             94_0  COME_FROM            58  '58'
             94_1  COME_FROM            52  '52'

Parse error at or near `<117>' instruction at offset 16