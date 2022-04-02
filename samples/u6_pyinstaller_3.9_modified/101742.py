# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: mss\tools.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import os, struct, zlib
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Tuple

def to_png--- This code section failed: ---

 L.  28         0  LOAD_GLOBAL              struct
                2  LOAD_ATTR                pack
                4  STORE_FAST               'pack'

 L.  29         6  LOAD_GLOBAL              zlib
                8  LOAD_ATTR                crc32
               10  STORE_FAST               'crc32'

 L.  31        12  LOAD_FAST                'size'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'width'
               18  STORE_FAST               'height'

 L.  32        20  LOAD_FAST                'width'
               22  LOAD_CONST               3
               24  BINARY_MULTIPLY  
               26  STORE_DEREF              'line'

 L.  33        28  LOAD_FAST                'pack'
               30  LOAD_STR                 '>B'
               32  LOAD_CONST               0
               34  CALL_FUNCTION_2       2  ''
               36  STORE_DEREF              'png_filter'

 L.  34        38  LOAD_CONST               b''
               40  LOAD_METHOD              join

 L.  35        42  LOAD_CLOSURE             'data'
               44  LOAD_CLOSURE             'line'
               46  LOAD_CLOSURE             'png_filter'
               48  BUILD_TUPLE_3         3 
               50  LOAD_LISTCOMP            '<code_object <listcomp>>'
               52  LOAD_STR                 'to_png.<locals>.<listcomp>'
               54  MAKE_FUNCTION_8          'closure'
               56  LOAD_GLOBAL              range
               58  LOAD_FAST                'height'
               60  CALL_FUNCTION_1       1  ''
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''

 L.  34        66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'scanlines'

 L.  38        70  LOAD_FAST                'pack'
               72  LOAD_STR                 '>8B'
               74  LOAD_CONST               137
               76  LOAD_CONST               80
               78  LOAD_CONST               78
               80  LOAD_CONST               71
               82  LOAD_CONST               13
               84  LOAD_CONST               10
               86  LOAD_CONST               26
               88  LOAD_CONST               10
               90  CALL_FUNCTION_9       9  ''
               92  STORE_FAST               'magic'

 L.  41        94  BUILD_LIST_0          0 
               96  LOAD_CONST               (b'', b'IHDR', b'', b'')
               98  CALL_FINALLY        101  'to 101'
              100  STORE_FAST               'ihdr'

 L.  42       102  LOAD_FAST                'pack'
              104  LOAD_STR                 '>2I5B'
              106  LOAD_FAST                'width'
              108  LOAD_FAST                'height'
              110  LOAD_CONST               8
              112  LOAD_CONST               2
              114  LOAD_CONST               0
              116  LOAD_CONST               0
              118  LOAD_CONST               0
              120  CALL_FUNCTION_8       8  ''
              122  LOAD_FAST                'ihdr'
              124  LOAD_CONST               2
              126  STORE_SUBSCR     

 L.  43       128  LOAD_FAST                'pack'
              130  LOAD_STR                 '>I'
              132  LOAD_FAST                'crc32'
              134  LOAD_CONST               b''
              136  LOAD_METHOD              join
              138  LOAD_FAST                'ihdr'
              140  LOAD_CONST               1
              142  LOAD_CONST               3
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  CALL_METHOD_1         1  ''
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               4294967295
              154  BINARY_AND       
              156  CALL_FUNCTION_2       2  ''
              158  LOAD_FAST                'ihdr'
              160  LOAD_CONST               3
              162  STORE_SUBSCR     

 L.  44       164  LOAD_FAST                'pack'
              166  LOAD_STR                 '>I'
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'ihdr'
              172  LOAD_CONST               2
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  ''
              178  CALL_FUNCTION_2       2  ''
              180  LOAD_FAST                'ihdr'
              182  LOAD_CONST               0
              184  STORE_SUBSCR     

 L.  47       186  LOAD_CONST               b''
              188  LOAD_CONST               b'IDAT'
              190  LOAD_GLOBAL              zlib
              192  LOAD_METHOD              compress
              194  LOAD_FAST                'scanlines'
              196  LOAD_FAST                'level'
              198  CALL_METHOD_2         2  ''
              200  LOAD_CONST               b''
              202  BUILD_LIST_4          4 
              204  STORE_FAST               'idat'

 L.  48       206  LOAD_FAST                'pack'
              208  LOAD_STR                 '>I'
              210  LOAD_FAST                'crc32'
              212  LOAD_CONST               b''
              214  LOAD_METHOD              join
              216  LOAD_FAST                'idat'
              218  LOAD_CONST               1
              220  LOAD_CONST               3
              222  BUILD_SLICE_2         2 
              224  BINARY_SUBSCR    
              226  CALL_METHOD_1         1  ''
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_CONST               4294967295
              232  BINARY_AND       
              234  CALL_FUNCTION_2       2  ''
              236  LOAD_FAST                'idat'
              238  LOAD_CONST               3
              240  STORE_SUBSCR     

 L.  49       242  LOAD_FAST                'pack'
              244  LOAD_STR                 '>I'
              246  LOAD_GLOBAL              len
              248  LOAD_FAST                'idat'
              250  LOAD_CONST               2
              252  BINARY_SUBSCR    
              254  CALL_FUNCTION_1       1  ''
              256  CALL_FUNCTION_2       2  ''
              258  LOAD_FAST                'idat'
              260  LOAD_CONST               0
              262  STORE_SUBSCR     

 L.  52       264  BUILD_LIST_0          0 
              266  LOAD_CONST               (b'', b'IEND', b'', b'')
              268  CALL_FINALLY        271  'to 271'
              270  STORE_FAST               'iend'

 L.  53       272  LOAD_FAST                'pack'
              274  LOAD_STR                 '>I'
              276  LOAD_FAST                'crc32'
              278  LOAD_FAST                'iend'
              280  LOAD_CONST               1
              282  BINARY_SUBSCR    
              284  CALL_FUNCTION_1       1  ''
              286  LOAD_CONST               4294967295
              288  BINARY_AND       
              290  CALL_FUNCTION_2       2  ''
              292  LOAD_FAST                'iend'
              294  LOAD_CONST               3
              296  STORE_SUBSCR     

 L.  54       298  LOAD_FAST                'pack'
              300  LOAD_STR                 '>I'
              302  LOAD_GLOBAL              len
              304  LOAD_FAST                'iend'
              306  LOAD_CONST               2
              308  BINARY_SUBSCR    
              310  CALL_FUNCTION_1       1  ''
              312  CALL_FUNCTION_2       2  ''
              314  LOAD_FAST                'iend'
              316  LOAD_CONST               0
              318  STORE_SUBSCR     

 L.  56       320  LOAD_FAST                'output'
          322_324  POP_JUMP_IF_TRUE    348  'to 348'

 L.  58       326  LOAD_FAST                'magic'
              328  LOAD_CONST               b''
              330  LOAD_METHOD              join
              332  LOAD_FAST                'ihdr'
              334  LOAD_FAST                'idat'
              336  BINARY_ADD       
              338  LOAD_FAST                'iend'
              340  BINARY_ADD       
              342  CALL_METHOD_1         1  ''
              344  BINARY_ADD       
              346  RETURN_VALUE     
            348_0  COME_FROM           322  '322'

 L.  60       348  LOAD_GLOBAL              open
              350  LOAD_FAST                'output'
              352  LOAD_STR                 'wb'
              354  CALL_FUNCTION_2       2  ''
              356  SETUP_WITH          454  'to 454'
              358  STORE_FAST               'fileh'

 L.  61       360  LOAD_FAST                'fileh'
              362  LOAD_METHOD              write
              364  LOAD_FAST                'magic'
              366  CALL_METHOD_1         1  ''
              368  POP_TOP          

 L.  62       370  LOAD_FAST                'fileh'
              372  LOAD_METHOD              write
              374  LOAD_CONST               b''
              376  LOAD_METHOD              join
              378  LOAD_FAST                'ihdr'
              380  CALL_METHOD_1         1  ''
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          

 L.  63       386  LOAD_FAST                'fileh'
              388  LOAD_METHOD              write
              390  LOAD_CONST               b''
              392  LOAD_METHOD              join
              394  LOAD_FAST                'idat'
              396  CALL_METHOD_1         1  ''
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          

 L.  64       402  LOAD_FAST                'fileh'
              404  LOAD_METHOD              write
              406  LOAD_CONST               b''
              408  LOAD_METHOD              join
              410  LOAD_FAST                'iend'
              412  CALL_METHOD_1         1  ''
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          

 L.  67       418  LOAD_FAST                'fileh'
              420  LOAD_METHOD              flush
              422  CALL_METHOD_0         0  ''
              424  POP_TOP          

 L.  68       426  LOAD_GLOBAL              os
              428  LOAD_METHOD              fsync
              430  LOAD_FAST                'fileh'
              432  LOAD_METHOD              fileno
              434  CALL_METHOD_0         0  ''
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          
              440  POP_BLOCK        
              442  LOAD_CONST               None
              444  DUP_TOP          
              446  DUP_TOP          
              448  CALL_FUNCTION_3       3  ''
              450  POP_TOP          
              452  JUMP_FORWARD        472  'to 472'
            454_0  COME_FROM_WITH      356  '356'
              454  <49>             
          456_458  POP_JUMP_IF_TRUE    462  'to 462'
              460  <48>             
            462_0  COME_FROM           456  '456'
              462  POP_TOP          
              464  POP_TOP          
              466  POP_TOP          
              468  POP_EXCEPT       
              470  POP_TOP          
            472_0  COME_FROM           452  '452'

Parse error at or near `CALL_FINALLY' instruction at offset 98