# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE   116  'to 116'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  23        28  SETUP_FINALLY        84  'to 84'

 L.  24        30  SETUP_FINALLY        58  'to 58'

 L.  25        32  LOAD_GLOBAL              win32api
               34  LOAD_METHOD              RegQueryValue
               36  LOAD_GLOBAL              win32con
               38  LOAD_ATTR                HKEY_CLASSES_ROOT
               40  LOAD_STR                 'Interface\\%s'
               42  LOAD_FAST                'iid'
               44  BINARY_MODULO    
               46  CALL_METHOD_2         2  ''
               48  POP_BLOCK        
               50  POP_BLOCK        
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    30  '30'

 L.  26        58  DUP_TOP          
               60  LOAD_GLOBAL              win32api
               62  LOAD_ATTR                error
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    78  'to 78'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  27        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            66  '66'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
               80  POP_BLOCK        
               82  JUMP_FORWARD        104  'to 104'
             84_0  COME_FROM_FINALLY    28  '28'

 L.  28        84  DUP_TOP          
               86  LOAD_GLOBAL              ImportError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  29        98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            90  '90'
              102  END_FINALLY      
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            82  '82'

 L.  30       104  LOAD_GLOBAL              str
              106  LOAD_FAST                'iid'
              108  CALL_FUNCTION_1       1  ''
              110  ROT_FOUR         
              112  POP_EXCEPT       
              114  RETURN_VALUE     
            116_0  COME_FROM            20  '20'
              116  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 50