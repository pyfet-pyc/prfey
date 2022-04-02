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
               76  POP_JUMP_IF_FALSE   216  'to 216'

 L.  55        78  LOAD_GLOBAL              _cfg_target
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE   140  'to 140'

 L.  56        86  LOAD_CONST               0
               88  LOAD_CONST               ('sysconfig',)
               90  IMPORT_NAME              distutils
               92  IMPORT_FROM              sysconfig
               94  STORE_FAST               'sysconfig'
               96  POP_TOP          

 L.  57        98  LOAD_GLOBAL              str
              100  LOAD_FAST                'sysconfig'
              102  LOAD_METHOD              get_config_var

 L.  58       104  LOAD_STR                 'MACOSX_DEPLOYMENT_TARGET'

 L.  57       106  CALL_METHOD_1         1  ''
              108  JUMP_IF_TRUE_OR_POP   112  'to 112'

 L.  58       110  LOAD_STR                 ''
            112_0  COME_FROM           108  '108'

 L.  57       112  CALL_FUNCTION_1       1  ''
              114  STORE_GLOBAL             _cfg_target

 L.  59       116  LOAD_GLOBAL              _cfg_target
              118  POP_JUMP_IF_FALSE   140  'to 140'

 L.  60       120  LOAD_LISTCOMP            '<code_object <listcomp>>'
              122  LOAD_STR                 'spawn.<locals>.<listcomp>'
              124  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              126  LOAD_GLOBAL              _cfg_target
              128  LOAD_METHOD              split
              130  LOAD_STR                 '.'
              132  CALL_METHOD_1         1  ''
              134  GET_ITER         
              136  CALL_FUNCTION_1       1  ''
              138  STORE_GLOBAL             _cfg_target_split
            140_0  COME_FROM           118  '118'
            140_1  COME_FROM            84  '84'

 L.  61       140  LOAD_GLOBAL              _cfg_target
              142  POP_JUMP_IF_FALSE   216  'to 216'

 L.  65       144  LOAD_GLOBAL              os
              146  LOAD_ATTR                environ
              148  LOAD_METHOD              get
              150  LOAD_STR                 'MACOSX_DEPLOYMENT_TARGET'
              152  LOAD_GLOBAL              _cfg_target
              154  CALL_METHOD_2         2  ''
              156  STORE_FAST               'cur_target'

 L.  66       158  LOAD_GLOBAL              _cfg_target_split
              160  LOAD_LISTCOMP            '<code_object <listcomp>>'
              162  LOAD_STR                 'spawn.<locals>.<listcomp>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_FAST                'cur_target'
              168  LOAD_METHOD              split
              170  LOAD_STR                 '.'
              172  CALL_METHOD_1         1  ''
              174  GET_ITER         
              176  CALL_FUNCTION_1       1  ''
              178  COMPARE_OP               >
              180  POP_JUMP_IF_FALSE   202  'to 202'

 L.  67       182  LOAD_STR                 '$MACOSX_DEPLOYMENT_TARGET mismatch: now "%s" but "%s" during configure'

 L.  69       184  LOAD_FAST                'cur_target'
              186  LOAD_GLOBAL              _cfg_target
              188  BUILD_TUPLE_2         2 

 L.  67       190  BINARY_MODULO    
              192  STORE_FAST               'my_msg'

 L.  70       194  LOAD_GLOBAL              DistutilsPlatformError
              196  LOAD_FAST                'my_msg'
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           180  '180'

 L.  71       202  LOAD_GLOBAL              dict
              204  LOAD_GLOBAL              os
              206  LOAD_ATTR                environ

 L.  72       208  LOAD_FAST                'cur_target'

 L.  71       210  LOAD_CONST               ('MACOSX_DEPLOYMENT_TARGET',)
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  STORE_FAST               'env'
            216_0  COME_FROM           142  '142'
            216_1  COME_FROM            76  '76'

 L.  74       216  SETUP_FINALLY       250  'to 250'

 L.  75       218  LOAD_GLOBAL              subprocess
              220  LOAD_ATTR                Popen
              222  LOAD_FAST                'cmd'
              224  LOAD_FAST                'env'
              226  LOAD_CONST               ('env',)
              228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              230  STORE_FAST               'proc'

 L.  76       232  LOAD_FAST                'proc'
              234  LOAD_METHOD              wait
              236  CALL_METHOD_0         0  ''
              238  POP_TOP          

 L.  77       240  LOAD_FAST                'proc'
              242  LOAD_ATTR                returncode
              244  STORE_FAST               'exitcode'
              246  POP_BLOCK        
              248  JUMP_FORWARD        326  'to 326'
            250_0  COME_FROM_FINALLY   216  '216'

 L.  78       250  DUP_TOP          
              252  LOAD_GLOBAL              OSError
          254_256  <121>               324  ''
              258  POP_TOP          
              260  STORE_FAST               'exc'
              262  POP_TOP          
              264  SETUP_FINALLY       316  'to 316'

 L.  79       266  LOAD_GLOBAL              DEBUG
          268_270  POP_JUMP_IF_TRUE    280  'to 280'

 L.  80       272  LOAD_FAST                'cmd'
              274  LOAD_CONST               0
              276  BINARY_SUBSCR    
              278  STORE_FAST               'cmd'
            280_0  COME_FROM           268  '268'

 L.  81       280  LOAD_GLOBAL              DistutilsExecError

 L.  82       282  LOAD_STR                 'command %r failed: %s'
              284  LOAD_FAST                'cmd'
              286  LOAD_FAST                'exc'
              288  LOAD_ATTR                args
              290  LOAD_CONST               -1
              292  BINARY_SUBSCR    
              294  BUILD_TUPLE_2         2 
              296  BINARY_MODULO    

 L.  81       298  CALL_FUNCTION_1       1  ''

 L.  82       300  LOAD_FAST                'exc'

 L.  81       302  RAISE_VARARGS_2       2  'exception instance with __cause__'
              304  POP_BLOCK        
              306  POP_EXCEPT       
              308  LOAD_CONST               None
              310  STORE_FAST               'exc'
              312  DELETE_FAST              'exc'
              314  JUMP_FORWARD        326  'to 326'
            316_0  COME_FROM_FINALLY   264  '264'
              316  LOAD_CONST               None
              318  STORE_FAST               'exc'
              320  DELETE_FAST              'exc'
              322  <48>             
              324  <48>             
            326_0  COME_FROM           314  '314'
            326_1  COME_FROM           248  '248'

 L.  84       326  LOAD_FAST                'exitcode'
          328_330  POP_JUMP_IF_FALSE   362  'to 362'

 L.  85       332  LOAD_GLOBAL              DEBUG
          334_336  POP_JUMP_IF_TRUE    346  'to 346'

 L.  86       338  LOAD_FAST                'cmd'
              340  LOAD_CONST               0
              342  BINARY_SUBSCR    
              344  STORE_FAST               'cmd'
            346_0  COME_FROM           334  '334'

 L.  87       346  LOAD_GLOBAL              DistutilsExecError

 L.  88       348  LOAD_STR                 'command %r failed with exit code %s'
              350  LOAD_FAST                'cmd'
              352  LOAD_FAST                'exitcode'
              354  BUILD_TUPLE_2         2 
              356  BINARY_MODULO    

 L.  87       358  CALL_FUNCTION_1       1  ''
              360  RAISE_VARARGS_1       1  'exception instance'
            362_0  COME_FROM           328  '328'

Parse error at or near `<117>' instruction at offset 52


def find_executable--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              splitext
                6  LOAD_FAST                'executable'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               '_'
               14  STORE_FAST               'ext'

 L.  98        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                platform
               20  LOAD_STR                 'win32'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    42  'to 42'
               26  LOAD_FAST                'ext'
               28  LOAD_STR                 '.exe'
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  99        34  LOAD_FAST                'executable'
               36  LOAD_STR                 '.exe'
               38  BINARY_ADD       
               40  STORE_FAST               'executable'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'

 L. 101        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                path
               46  LOAD_METHOD              isfile
               48  LOAD_FAST                'executable'
               50  CALL_METHOD_1         1  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 102        54  LOAD_FAST                'executable'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 104        58  LOAD_FAST                'path'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE   132  'to 132'

 L. 105        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                environ
               70  LOAD_METHOD              get
               72  LOAD_STR                 'PATH'
               74  LOAD_CONST               None
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'path'

 L. 106        80  LOAD_FAST                'path'
               82  LOAD_CONST               None
               84  <117>                 0  ''
               86  POP_JUMP_IF_FALSE   132  'to 132'

 L. 107        88  SETUP_FINALLY       104  'to 104'

 L. 108        90  LOAD_GLOBAL              os
               92  LOAD_METHOD              confstr
               94  LOAD_STR                 'CS_PATH'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'path'
              100  POP_BLOCK        
              102  JUMP_FORWARD        132  'to 132'
            104_0  COME_FROM_FINALLY    88  '88'

 L. 109       104  DUP_TOP          
              106  LOAD_GLOBAL              AttributeError
              108  LOAD_GLOBAL              ValueError
              110  BUILD_TUPLE_2         2 
              112  <121>               130  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 111       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                defpath
              124  STORE_FAST               'path'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
              130  <48>             
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           102  '102'
            132_2  COME_FROM            86  '86'
            132_3  COME_FROM            64  '64'

 L. 116       132  LOAD_FAST                'path'
              134  POP_JUMP_IF_TRUE    140  'to 140'

 L. 117       136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM           134  '134'

 L. 119       140  LOAD_FAST                'path'
              142  LOAD_METHOD              split
              144  LOAD_GLOBAL              os
              146  LOAD_ATTR                pathsep
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'paths'

 L. 120       152  LOAD_FAST                'paths'
              154  GET_ITER         
            156_0  COME_FROM           194  '194'
            156_1  COME_FROM           184  '184'
              156  FOR_ITER            196  'to 196'
              158  STORE_FAST               'p'

 L. 121       160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_FAST                'p'
              168  LOAD_FAST                'executable'
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'f'

 L. 122       174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              isfile
              180  LOAD_FAST                'f'
              182  CALL_METHOD_1         1  ''
              184  POP_JUMP_IF_FALSE_BACK   156  'to 156'

 L. 124       186  LOAD_FAST                'f'
              188  ROT_TWO          
              190  POP_TOP          
              192  RETURN_VALUE     
              194  JUMP_BACK           156  'to 156'
            196_0  COME_FROM           156  '156'

Parse error at or near `<117>' instruction at offset 62


# global _cfg_target ## Warning: Unused global
# global _cfg_target_split ## Warning: Unused global