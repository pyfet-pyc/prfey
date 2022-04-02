# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyasn1\compat\string.py
from sys import version_info
if version_info[:2] <= (2, 5):

    def partition--- This code section failed: ---

 L.  12         0  SETUP_FINALLY        22  'to 22'

 L.  13         2  LOAD_FAST                'string'
                4  LOAD_METHOD              split
                6  LOAD_FAST                'sep'
                8  LOAD_CONST               1
               10  CALL_METHOD_2         2  ''
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'a'
               16  STORE_FAST               'c'
               18  POP_BLOCK        
               20  JUMP_FORWARD         56  'to 56'
             22_0  COME_FROM_FINALLY     0  '0'

 L.  15        22  DUP_TOP          
               24  LOAD_GLOBAL              ValueError
               26  <121>                54  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  16        34  LOAD_FAST                'string'
               36  LOAD_STR                 ''
               38  LOAD_STR                 ''
               40  ROT_THREE        
               42  ROT_TWO          
               44  STORE_FAST               'a'
               46  STORE_FAST               'b'
               48  STORE_FAST               'c'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         60  'to 60'
               54  <48>             
             56_0  COME_FROM            20  '20'

 L.  19        56  LOAD_FAST                'sep'
               58  STORE_FAST               'b'
             60_0  COME_FROM            52  '52'

 L.  21        60  LOAD_FAST                'a'
               62  LOAD_FAST                'b'
               64  LOAD_FAST                'c'
               66  BUILD_TUPLE_3         3 
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 26


else:

    def partition(string, sep):
        return string.partition(sep)