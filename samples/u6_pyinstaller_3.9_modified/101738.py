# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: mss\factory.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import platform
from typing import TYPE_CHECKING
from .exception import ScreenShotError
if TYPE_CHECKING:
    from typing import Any
    from .base import MSSBase

def mss--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              platform
                2  LOAD_METHOD              system
                4  CALL_METHOD_0         0  ''
                6  LOAD_METHOD              lower
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'os_'

 L.  33        12  LOAD_FAST                'os_'
               14  LOAD_STR                 'darwin'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    48  'to 48'

 L.  34        20  LOAD_CONST               1
               22  LOAD_CONST               ('darwin',)
               24  IMPORT_NAME              
               26  IMPORT_FROM              darwin
               28  STORE_FAST               'darwin'
               30  POP_TOP          

 L.  36        32  LOAD_FAST                'darwin'
               34  LOAD_ATTR                MSS
               36  BUILD_TUPLE_0         0 
               38  BUILD_MAP_0           0 
               40  LOAD_FAST                'kwargs'
               42  <164>                 1  ''
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  RETURN_VALUE     
             48_0  COME_FROM            18  '18'

 L.  38        48  LOAD_FAST                'os_'
               50  LOAD_STR                 'linux'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    84  'to 84'

 L.  39        56  LOAD_CONST               1
               58  LOAD_CONST               ('linux',)
               60  IMPORT_NAME              
               62  IMPORT_FROM              linux
               64  STORE_FAST               'linux'
               66  POP_TOP          

 L.  41        68  LOAD_FAST                'linux'
               70  LOAD_ATTR                MSS
               72  BUILD_TUPLE_0         0 
               74  BUILD_MAP_0           0 
               76  LOAD_FAST                'kwargs'
               78  <164>                 1  ''
               80  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               82  RETURN_VALUE     
             84_0  COME_FROM            54  '54'

 L.  43        84  LOAD_FAST                'os_'
               86  LOAD_STR                 'windows'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   120  'to 120'

 L.  44        92  LOAD_CONST               1
               94  LOAD_CONST               ('windows',)
               96  IMPORT_NAME              
               98  IMPORT_FROM              windows
              100  STORE_FAST               'windows'
              102  POP_TOP          

 L.  46       104  LOAD_FAST                'windows'
              106  LOAD_ATTR                MSS
              108  BUILD_TUPLE_0         0 
              110  BUILD_MAP_0           0 
              112  LOAD_FAST                'kwargs'
              114  <164>                 1  ''
              116  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              118  RETURN_VALUE     
            120_0  COME_FROM            90  '90'

 L.  48       120  LOAD_GLOBAL              ScreenShotError
              122  LOAD_STR                 'System {!r} not (yet?) implemented.'
              124  LOAD_METHOD              format
              126  LOAD_FAST                'os_'
              128  CALL_METHOD_1         1  ''
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<164>' instruction at offset 42