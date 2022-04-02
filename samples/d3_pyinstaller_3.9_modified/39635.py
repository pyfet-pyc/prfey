# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\spawn.py
"""distutils.spawn

Provides the 'spawn()' function, a front-end to various platform-
specific functions for launching another program in a sub-process.
Also provides the 'find_executable()' to search the path for a given
executable name.
"""
import sys, os, subprocess
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils.debug import DEBUG
from distutils import log
if sys.platform == 'darwin':
    _cfg_target = None
    _cfg_target_split = None

def spawn--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'cmd'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'cmd'

 L.  43         8  LOAD_GLOBAL              log
               10  LOAD_METHOD              info
               12  LOAD_STR                 ' '
               14  LOAD_METHOD              join
               16  LOAD_FAST                'cmd'
               18  CALL_METHOD_1         1  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  44        24  LOAD_FAST                'dry_run'
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L.  45        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L.  47        32  LOAD_FAST                'search_path'
               34  POP_JUMP_IF_FALSE    64  'to 64'

 L.  48        36  LOAD_GLOBAL              find_executable
               38  LOAD_FAST                'cmd'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'executable'

 L.  49        48  LOAD_FAST                'executable'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L.  50        56  LOAD_FAST                'executable'
               58  LOAD_FAST                'cmd'
               60  LOAD_CONST               0
               62  STORE_SUBSCR     
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            34  '34'

 L.  52        64  LOAD_CONST               None
               66  STORE_FAST               'env'

 L.  53        68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                platform
               72  LOAD_STR                 'darwin'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   248  'to 248'

 L.  55        78  LOAD_GLOBAL              _cfg_target
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE   136  'to 136'

 L.  56        86  LOAD_CONST               0
               88  LOAD_CONST               ('sysconfig',)
               90  IMPORT_NAME              distutils
               92  IMPORT_FROM              sysconfig
               94  STORE_FAST               'sysconfig'
               96  POP_TOP          

 L.  57        98  LOAD_FAST                'sysconfig'
              100  LOAD_METHOD              get_config_var

 L.  58       102  LOAD_STR                 'MACOSX_DEPLOYMENT_TARGET'

 L.  57       104  CALL_METHOD_1         1  ''
              106  JUMP_IF_TRUE_OR_POP   110  'to 110'

 L.  58       108  LOAD_STR                 ''
            110_0  COME_FROM           106  '106'

 L.  57       110  STORE_GLOBAL             _cfg_target

 L.  59       112  LOAD_GLOBAL              _cfg_target
              114  POP_JUMP_IF_FALSE   136  'to 136'

 L.  60       116  LOAD_LISTCOMP            '<code_object <listcomp>>'
              118  LOAD_STR                 'spawn.<locals>.<listcomp>'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              122  LOAD_GLOBAL              _cfg_target
              124  LOAD_METHOD              split
              126  LOAD_STR                 '.'
              128  CALL_METHOD_1         1  ''
              130  GET_ITER         
              132  CALL_FUNCTION_1       1  ''
              134  STORE_GLOBAL             _cfg_target_split
            136_0  COME_FROM           114  '114'
            136_1  COME_FROM            84  '84'

 L.  61       136  LOAD_GLOBAL              _cfg_target
              138  POP_JUMP_IF_FALSE   248  'to 248'

 L.  67       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                environ
              144  LOAD_METHOD              get
              146  LOAD_STR                 'MACOSX_DEPLOYMENT_TARGET'
              148  LOAD_GLOBAL              _cfg_target
              150  CALL_METHOD_2         2  ''
              152  STORE_FAST               'cur_target'

 L.  68       154  LOAD_LISTCOMP            '<code_object <listcomp>>'
              156  LOAD_STR                 'spawn.<locals>.<listcomp>'
              158  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              160  LOAD_FAST                'cur_target'
              162  LOAD_METHOD              split
              164  LOAD_STR                 '.'
              166  CALL_METHOD_1         1  ''
              168  GET_ITER         
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'cur_target_split'

 L.  69       174  LOAD_GLOBAL              _cfg_target_split
              176  LOAD_CONST               None
              178  LOAD_CONST               2
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  LOAD_CONST               10
              186  LOAD_CONST               3
              188  BUILD_LIST_2          2 
              190  COMPARE_OP               >=
              192  POP_JUMP_IF_FALSE   234  'to 234'
              194  LOAD_FAST                'cur_target_split'
              196  LOAD_CONST               None
              198  LOAD_CONST               2
              200  BUILD_SLICE_2         2 
              202  BINARY_SUBSCR    
              204  LOAD_CONST               10
              206  LOAD_CONST               3
              208  BUILD_LIST_2          2 
              210  COMPARE_OP               <
              212  POP_JUMP_IF_FALSE   234  'to 234'

 L.  70       214  LOAD_STR                 '$MACOSX_DEPLOYMENT_TARGET mismatch: now "%s" but "%s" during configure;must use 10.3 or later'

 L.  73       216  LOAD_FAST                'cur_target'
              218  LOAD_GLOBAL              _cfg_target
              220  BUILD_TUPLE_2         2 

 L.  70       222  BINARY_MODULO    
              224  STORE_FAST               'my_msg'

 L.  74       226  LOAD_GLOBAL              DistutilsPlatformError
              228  LOAD_FAST                'my_msg'
              230  CALL_FUNCTION_1       1  ''
              232  RAISE_VARARGS_1       1  'exception instance'
            234_0  COME_FROM           212  '212'
            234_1  COME_FROM           192  '192'

 L.  75       234  LOAD_GLOBAL              dict
              236  LOAD_GLOBAL              os
              238  LOAD_ATTR                environ

 L.  76       240  LOAD_FAST                'cur_target'

 L.  75       242  LOAD_CONST               ('MACOSX_DEPLOYMENT_TARGET',)
              244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              246  STORE_FAST               'env'
            248_0  COME_FROM           138  '138'
            248_1  COME_FROM            76  '76'

 L.  78       248  SETUP_FINALLY       282  'to 282'

 L.  79       250  LOAD_GLOBAL              subprocess
              252  LOAD_ATTR                Popen
              254  LOAD_FAST                'cmd'
              256  LOAD_FAST                'env'
              258  LOAD_CONST               ('env',)
              260  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              262  STORE_FAST               'proc'

 L.  80       264  LOAD_FAST                'proc'
              266  LOAD_METHOD              wait
              268  CALL_METHOD_0         0  ''
              270  POP_TOP          

 L.  81       272  LOAD_FAST                'proc'
              274  LOAD_ATTR                returncode
              276  STORE_FAST               'exitcode'
              278  POP_BLOCK        
              280  JUMP_FORWARD        358  'to 358'
            282_0  COME_FROM_FINALLY   248  '248'

 L.  82       282  DUP_TOP          
              284  LOAD_GLOBAL              OSError
          286_288  <121>               356  ''
              290  POP_TOP          
              292  STORE_FAST               'exc'
              294  POP_TOP          
              296  SETUP_FINALLY       348  'to 348'

 L.  83       298  LOAD_GLOBAL              DEBUG
          300_302  POP_JUMP_IF_TRUE    312  'to 312'

 L.  84       304  LOAD_FAST                'cmd'
              306  LOAD_CONST               0
              308  BINARY_SUBSCR    
              310  STORE_FAST               'cmd'
            312_0  COME_FROM           300  '300'

 L.  85       312  LOAD_GLOBAL              DistutilsExecError

 L.  86       314  LOAD_STR                 'command %r failed: %s'
              316  LOAD_FAST                'cmd'
              318  LOAD_FAST                'exc'
              320  LOAD_ATTR                args
              322  LOAD_CONST               -1
              324  BINARY_SUBSCR    
              326  BUILD_TUPLE_2         2 
              328  BINARY_MODULO    

 L.  85       330  CALL_FUNCTION_1       1  ''

 L.  86       332  LOAD_FAST                'exc'

 L.  85       334  RAISE_VARARGS_2       2  'exception instance with __cause__'
              336  POP_BLOCK        
              338  POP_EXCEPT       
              340  LOAD_CONST               None
              342  STORE_FAST               'exc'
              344  DELETE_FAST              'exc'
              346  JUMP_FORWARD        358  'to 358'
            348_0  COME_FROM_FINALLY   296  '296'
              348  LOAD_CONST               None
              350  STORE_FAST               'exc'
              352  DELETE_FAST              'exc'
              354  <48>             
              356  <48>             
            358_0  COME_FROM           346  '346'
            358_1  COME_FROM           280  '280'

 L.  88       358  LOAD_FAST                'exitcode'
          360_362  POP_JUMP_IF_FALSE   394  'to 394'

 L.  89       364  LOAD_GLOBAL              DEBUG
          366_368  POP_JUMP_IF_TRUE    378  'to 378'

 L.  90       370  LOAD_FAST                'cmd'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  STORE_FAST               'cmd'
            378_0  COME_FROM           366  '366'

 L.  91       378  LOAD_GLOBAL              DistutilsExecError

 L.  92       380  LOAD_STR                 'command %r failed with exit code %s'
              382  LOAD_FAST                'cmd'
              384  LOAD_FAST                'exitcode'
              386  BUILD_TUPLE_2         2 
              388  BINARY_MODULO    

 L.  91       390  CALL_FUNCTION_1       1  ''
              392  RAISE_VARARGS_1       1  'exception instance'
            394_0  COME_FROM           360  '360'

Parse error at or near `<117>' instruction at offset 52


def find_executable--- This code section failed: ---

 L. 101         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              splitext
                6  LOAD_FAST                'executable'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               '_'
               14  STORE_FAST               'ext'

 L. 102        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                platform
               20  LOAD_STR                 'win32'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    42  'to 42'
               26  LOAD_FAST                'ext'
               28  LOAD_STR                 '.exe'
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 103        34  LOAD_FAST                'executable'
               36  LOAD_STR                 '.exe'
               38  BINARY_ADD       
               40  STORE_FAST               'executable'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'

 L. 105        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              isfile
               48  LOAD_FAST                'executable'
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 106        54  LOAD_FAST                'executable'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 108        58  LOAD_FAST                'path'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   132  'to 132'

 L. 109        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                environ
               70  LOAD_METHOD              get
               72  LOAD_STR                 'PATH'
               74  LOAD_CONST               None
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'path'

 L. 110        80  LOAD_FAST                'path'
               82  LOAD_CONST               None
               84  <117>                 0  ''
               86  POP_JUMP_IF_FALSE   132  'to 132'

 L. 111        88  SETUP_FINALLY       104  'to 104'

 L. 112        90  LOAD_GLOBAL              os
               92  LOAD_METHOD              confstr
               94  LOAD_STR                 'CS_PATH'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'path'
              100  POP_BLOCK        
              102  JUMP_FORWARD        132  'to 132'
            104_0  COME_FROM_FINALLY    88  '88'

 L. 113       104  DUP_TOP          
              106  LOAD_GLOBAL              AttributeError
              108  LOAD_GLOBAL              ValueError
              110  BUILD_TUPLE_2         2 
              112  <121>               130  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 115       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                defpath
              124  STORE_FAST               'path'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
              130  <48>             
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           102  '102'
            132_2  COME_FROM            86  '86'
            132_3  COME_FROM            64  '64'

 L. 120       132  LOAD_FAST                'path'
              134  POP_JUMP_IF_TRUE    140  'to 140'

 L. 121       136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM           134  '134'

 L. 123       140  LOAD_FAST                'path'
              142  LOAD_METHOD              split
              144  LOAD_GLOBAL              os
              146  LOAD_ATTR                pathsep
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'paths'

 L. 124       152  LOAD_FAST                'paths'
              154  GET_ITER         
            156_0  COME_FROM           194  '194'
            156_1  COME_FROM           184  '184'
              156  FOR_ITER            196  'to 196'
              158  STORE_FAST               'p'

 L. 125       160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_FAST                'p'
              168  LOAD_FAST                'executable'
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'f'

 L. 126       174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              isfile
              180  LOAD_FAST                'f'
              182  CALL_METHOD_1         1  ''
              184  POP_JUMP_IF_FALSE_BACK   156  'to 156'

 L. 128       186  LOAD_FAST                'f'
              188  ROT_TWO          
              190  POP_TOP          
              192  RETURN_VALUE     
              194  JUMP_BACK           156  'to 156'
            196_0  COME_FROM           156  '156'

Parse error at or near `<117>' instruction at offset 62


# global _cfg_target ## Warning: Unused global
# global _cfg_target_split ## Warning: Unused global