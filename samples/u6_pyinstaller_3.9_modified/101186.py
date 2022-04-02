# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Util\_file_system.py
import os

def pycryptodome_filename--- This code section failed: ---

 L.  45         0  LOAD_FAST                'dir_comps'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_STR                 'Crypto'
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  46        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 "Only available for modules under 'Crypto'"
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  48        20  LOAD_GLOBAL              list
               22  LOAD_FAST                'dir_comps'
               24  LOAD_CONST               1
               26  LOAD_CONST               None
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'filename'
               36  BUILD_LIST_1          1 
               38  BINARY_ADD       
               40  STORE_FAST               'dir_comps'

 L.  50        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              split
               48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              abspath
               54  LOAD_GLOBAL              __file__
               56  CALL_METHOD_1         1  ''
               58  CALL_METHOD_1         1  ''
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'util_lib'
               64  STORE_FAST               '_'

 L.  51        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              join
               72  LOAD_FAST                'util_lib'
               74  LOAD_STR                 '..'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'root_lib'

 L.  53        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_ATTR                join
               86  LOAD_FAST                'root_lib'
               88  BUILD_LIST_1          1 
               90  LOAD_FAST                'dir_comps'
               92  CALL_FINALLY         95  'to 95'
               94  WITH_CLEANUP_FINISH
               96  CALL_FUNCTION_EX      0  'positional arguments only'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 92