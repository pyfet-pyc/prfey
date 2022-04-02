# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: charset_normalizer\legacy.py
from charset_normalizer.api import from_bytes
from charset_normalizer.constant import CHARDET_CORRESPONDENCE
from typing import Dict, Optional, Union

def detect--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'byte_str'
                4  LOAD_GLOBAL              bytearray
                6  LOAD_GLOBAL              bytes
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     32  'to 32'

 L.  17        14  LOAD_GLOBAL              TypeError
               16  LOAD_STR                 'Expected object of type bytes or bytearray, got: {0}'
               18  LOAD_METHOD              format

 L.  18        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'byte_str'
               24  CALL_FUNCTION_1       1  ''

 L.  17        26  CALL_METHOD_1         1  ''
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            12  '12'

 L.  20        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'byte_str'
               36  LOAD_GLOBAL              bytearray
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L.  21        42  LOAD_GLOBAL              bytes
               44  LOAD_FAST                'byte_str'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'byte_str'
             50_0  COME_FROM            40  '40'

 L.  23        50  LOAD_GLOBAL              from_bytes
               52  LOAD_FAST                'byte_str'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_METHOD              best
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'r'

 L.  25        62  LOAD_FAST                'r'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    76  'to 76'
               70  LOAD_FAST                'r'
               72  LOAD_ATTR                encoding
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            68  '68'
               76  LOAD_CONST               None
             78_0  COME_FROM            74  '74'
               78  STORE_FAST               'encoding'

 L.  26        80  LOAD_FAST                'r'
               82  LOAD_CONST               None
               84  <117>                 1  ''
               86  POP_JUMP_IF_FALSE   104  'to 104'
               88  LOAD_FAST                'r'
               90  LOAD_ATTR                language
               92  LOAD_STR                 'Unknown'
               94  COMPARE_OP               !=
               96  POP_JUMP_IF_FALSE   104  'to 104'
               98  LOAD_FAST                'r'
              100  LOAD_ATTR                language
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            96  '96'
            104_1  COME_FROM            86  '86'
              104  LOAD_STR                 ''
            106_0  COME_FROM           102  '102'
              106  STORE_FAST               'language'

 L.  27       108  LOAD_FAST                'r'
              110  LOAD_CONST               None
              112  <117>                 1  ''
              114  POP_JUMP_IF_FALSE   126  'to 126'
              116  LOAD_CONST               1.0
              118  LOAD_FAST                'r'
              120  LOAD_ATTR                chaos
              122  BINARY_SUBTRACT  
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           114  '114'
              126  LOAD_CONST               None
            128_0  COME_FROM           124  '124'
              128  STORE_FAST               'confidence'

 L.  31       130  LOAD_FAST                'r'
              132  LOAD_CONST               None
              134  <117>                 1  ''
              136  POP_JUMP_IF_FALSE   160  'to 160'
              138  LOAD_FAST                'encoding'
              140  LOAD_STR                 'utf_8'
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   160  'to 160'
              146  LOAD_FAST                'r'
              148  LOAD_ATTR                bom
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L.  32       152  LOAD_FAST                'encoding'
              154  LOAD_STR                 '_sig'
              156  INPLACE_ADD      
              158  STORE_FAST               'encoding'
            160_0  COME_FROM           150  '150'
            160_1  COME_FROM           144  '144'
            160_2  COME_FROM           136  '136'

 L.  35       160  LOAD_FAST                'encoding'
              162  LOAD_GLOBAL              CHARDET_CORRESPONDENCE
              164  <118>                 1  ''
              166  POP_JUMP_IF_FALSE   172  'to 172'
              168  LOAD_FAST                'encoding'
              170  JUMP_FORWARD        178  'to 178'
            172_0  COME_FROM           166  '166'
              172  LOAD_GLOBAL              CHARDET_CORRESPONDENCE
              174  LOAD_FAST                'encoding'
              176  BINARY_SUBSCR    
            178_0  COME_FROM           170  '170'

 L.  36       178  LOAD_FAST                'language'

 L.  37       180  LOAD_FAST                'confidence'

 L.  34       182  LOAD_CONST               ('encoding', 'language', 'confidence')
              184  BUILD_CONST_KEY_MAP_3     3 
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 66