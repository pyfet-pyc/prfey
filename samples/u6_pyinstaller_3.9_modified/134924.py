# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32ctypes\pywin32\pywintypes.py
""" A module which supports common Windows types. """
from __future__ import absolute_import
import contextlib

class error(Exception):

    def __init__--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'args'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'nargs'

 L.  17         8  LOAD_FAST                'nargs'
               10  LOAD_CONST               0
               12  COMPARE_OP               >
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L.  18        16  LOAD_FAST                'args'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_FAST                'self'
               24  STORE_ATTR               winerror
               26  JUMP_FORWARD         34  'to 34'
             28_0  COME_FROM            14  '14'

 L.  20        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               winerror
             34_0  COME_FROM            26  '26'

 L.  21        34  LOAD_FAST                'nargs'
               36  LOAD_CONST               1
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L.  22        42  LOAD_FAST                'args'
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'self'
               50  STORE_ATTR               funcname
               52  JUMP_FORWARD         60  'to 60'
             54_0  COME_FROM            40  '40'

 L.  24        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               funcname
             60_0  COME_FROM            52  '52'

 L.  25        60  LOAD_FAST                'nargs'
               62  LOAD_CONST               2
               64  COMPARE_OP               >
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L.  26        68  LOAD_FAST                'args'
               70  LOAD_CONST               2
               72  BINARY_SUBSCR    
               74  LOAD_FAST                'self'
               76  STORE_ATTR               strerror
               78  JUMP_FORWARD         86  'to 86'
             80_0  COME_FROM            66  '66'

 L.  28        80  LOAD_CONST               None
               82  LOAD_FAST                'self'
               84  STORE_ATTR               strerror
             86_0  COME_FROM            78  '78'

 L.  29        86  LOAD_GLOBAL              Exception
               88  LOAD_ATTR                __init__
               90  LOAD_FAST                'self'
               92  BUILD_LIST_1          1 
               94  LOAD_FAST                'args'
               96  CALL_FINALLY         99  'to 99'
               98  WITH_CLEANUP_FINISH
              100  BUILD_MAP_0           0 
              102  LOAD_FAST                'kw'
              104  <164>                 1  ''
              106  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              108  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 96


@contextlib.contextmanager
def pywin32error--- This code section failed: ---

 L.  34         0  SETUP_FINALLY        12  'to 12'

 L.  35         2  LOAD_CONST               None
                4  YIELD_VALUE      
                6  POP_TOP          
                8  POP_BLOCK        
               10  JUMP_FORWARD         66  'to 66'
             12_0  COME_FROM_FINALLY     0  '0'

 L.  36        12  DUP_TOP          
               14  LOAD_GLOBAL              WindowsError
               16  <121>                64  ''
               18  POP_TOP          
               20  STORE_FAST               'exception'
               22  POP_TOP          
               24  SETUP_FINALLY        56  'to 56'

 L.  37        26  LOAD_GLOBAL              error
               28  LOAD_FAST                'exception'
               30  LOAD_ATTR                winerror
               32  LOAD_FAST                'exception'
               34  LOAD_ATTR                function
               36  LOAD_FAST                'exception'
               38  LOAD_ATTR                strerror
               40  CALL_FUNCTION_3       3  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'exception'
               52  DELETE_FAST              'exception'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM_FINALLY    24  '24'
               56  LOAD_CONST               None
               58  STORE_FAST               'exception'
               60  DELETE_FAST              'exception'
               62  <48>             
               64  <48>             
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            10  '10'

Parse error at or near `<121>' instruction at offset 16