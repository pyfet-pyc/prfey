# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\util.py
"""General utility functions common to client and server.

  This module contains a collection of general purpose utility functions.
"""
import pythoncom, win32api, win32con

def IIDToInterfaceName--- This code section failed: ---

 L.  20         0  SETUP_FINALLY        14  'to 14'

 L.  21         2  LOAD_GLOBAL              pythoncom
                4  LOAD_ATTR                ServerInterfaces
                6  LOAD_FAST                'iid'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  22        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>               110  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  23        26  SETUP_FINALLY        80  'to 80'

 L.  24        28  SETUP_FINALLY        56  'to 56'

 L.  25        30  LOAD_GLOBAL              win32api
               32  LOAD_METHOD              RegQueryValue
               34  LOAD_GLOBAL              win32con
               36  LOAD_ATTR                HKEY_CLASSES_ROOT
               38  LOAD_STR                 'Interface\\%s'
               40  LOAD_FAST                'iid'
               42  BINARY_MODULO    
               44  CALL_METHOD_2         2  ''
               46  POP_BLOCK        
               48  POP_BLOCK        
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    28  '28'

 L.  26        56  DUP_TOP          
               58  LOAD_GLOBAL              win32api
               60  LOAD_ATTR                error
               62  <121>                74  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  27        70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
               76  POP_BLOCK        
               78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM_FINALLY    26  '26'

 L.  28        80  DUP_TOP          
               82  LOAD_GLOBAL              ImportError
               84  <121>                96  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.  29        92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
               96  <48>             
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            78  '78'

 L.  30        98  LOAD_GLOBAL              str
              100  LOAD_FAST                'iid'
              102  CALL_FUNCTION_1       1  ''
              104  ROT_FOUR         
              106  POP_EXCEPT       
              108  RETURN_VALUE     
              110  <48>             

Parse error at or near `<121>' instruction at offset 18