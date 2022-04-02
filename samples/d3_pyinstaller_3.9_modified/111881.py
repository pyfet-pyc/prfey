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
               76  POP_JUMP_IF_FALSE   212  'to 212'

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
              138  POP_JUMP_IF_FALSE   212  'to 212'

 L.  65       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                environ
              144  LOAD_METHOD              get
              146  LOAD_STR                 'MACOSX_DEPLOYMENT_TARGET'
              148  LOAD_GLOBAL              _cfg_target
              150  CALL_METHOD_2         2  ''
              152  STORE_FAST               'cur_target'

 L.  66       154  LOAD_GLOBAL              _cfg_target_split
              156  LOAD_LISTCOMP            '<code_object <listcomp>>'
              158  LOAD_STR                 'spawn.<locals>.<listcomp>'
              160  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              162  LOAD_FAST                'cur_target'
              164  LOAD_METHOD              split
              166  LOAD_STR                 '.'
              168  CALL_METHOD_1         1  ''
              170  GET_ITER         
              172  CALL_FUNCTION_1       1  ''
              174  COMPARE_OP               >
              176  POP_JUMP_IF_FALSE   198  'to 198'

 L.  67       178  LOAD_STR                 '$MACOSX_DEPLOYMENT_TARGET mismatch: now "%s" but "%s" during configure'

 L.  69       180  LOAD_FAST                'cur_target'
              182  LOAD_GLOBAL              _cfg_target
              184  BUILD_TUPLE_2         2 

 L.  67       186  BINARY_MODULO    
              188  STORE_FAST               'my_msg'

 L.  70       190  LOAD_GLOBAL              DistutilsPlatformError
              192  LOAD_FAST                'my_msg'
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           176  '176'

 L.  71       198  LOAD_GLOBAL              dict
              200  LOAD_GLOBAL              os
              202  LOAD_ATTR                environ

 L.  72       204  LOAD_FAST                'cur_target'

 L.  71       206  LOAD_CONST               ('MACOSX_DEPLOYMENT_TARGET',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  STORE_FAST               'env'
            212_0  COME_FROM           138  '138'
            212_1  COME_FROM            76  '76'

 L.  74       212  SETUP_FINALLY       246  'to 246'

 L.  75       214  LOAD_GLOBAL              subprocess
              216  LOAD_ATTR                Popen
              218  LOAD_FAST                'cmd'
              220  LOAD_FAST                'env'
              222  LOAD_CONST               ('env',)
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  STORE_FAST               'proc'

 L.  76       228  LOAD_FAST                'proc'
              230  LOAD_METHOD              wait
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          

 L.  77       236  LOAD_FAST                'proc'
              238  LOAD_ATTR                returncode
              240  STORE_FAST               'exitcode'
              242  POP_BLOCK        
              244  JUMP_FORWARD        322  'to 322'
            246_0  COME_FROM_FINALLY   212  '212'

 L.  78       246  DUP_TOP          
              248  LOAD_GLOBAL              OSError
          250_252  <121>               320  ''
              254  POP_TOP          
              256  STORE_FAST               'exc'
              258  POP_TOP          
              260  SETUP_FINALLY       312  'to 312'

 L.  79       262  LOAD_GLOBAL              DEBUG
          264_266  POP_JUMP_IF_TRUE    276  'to 276'

 L.  80       268  LOAD_FAST                'cmd'
              270  LOAD_CONST               0
              272  BINARY_SUBSCR    
              274  STORE_FAST               'cmd'
            276_0  COME_FROM           264  '264'

 L.  81       276  LOAD_GLOBAL              DistutilsExecError

 L.  82       278  LOAD_STR                 'command %r failed: %s'
              280  LOAD_FAST                'cmd'
              282  LOAD_FAST                'exc'
              284  LOAD_ATTR                args
              286  LOAD_CONST               -1
              288  BINARY_SUBSCR    
              290  BUILD_TUPLE_2         2 
              292  BINARY_MODULO    

 L.  81       294  CALL_FUNCTION_1       1  ''

 L.  82       296  LOAD_FAST                'exc'

 L.  81       298  RAISE_VARARGS_2       2  'exception instance with __cause__'
              300  POP_BLOCK        
              302  POP_EXCEPT       
              304  LOAD_CONST               None
              306  STORE_FAST               'exc'
              308  DELETE_FAST              'exc'
              310  JUMP_FORWARD        322  'to 322'
            312_0  COME_FROM_FINALLY   260  '260'
              312  LOAD_CONST               None
              314  STORE_FAST               'exc'
              316  DELETE_FAST              'exc'
              318  <48>             
              320  <48>             
            322_0  COME_FROM           310  '310'
            322_1  COME_FROM           244  '244'

 L.  84       322  LOAD_FAST                'exitcode'
          324_326  POP_JUMP_IF_FALSE   358  'to 358'

 L.  85       328  LOAD_GLOBAL              DEBUG
          330_332  POP_JUMP_IF_TRUE    342  'to 342'

 L.  86       334  LOAD_FAST                'cmd'
              336  LOAD_CONST               0
              338  BINARY_SUBSCR    
              340  STORE_FAST               'cmd'
            342_0  COME_FROM           330  '330'

 L.  87       342  LOAD_GLOBAL              DistutilsExecError

 L.  88       344  LOAD_STR                 'command %r failed with exit code %s'
              346  LOAD_FAST                'cmd'
              348  LOAD_FAST                'exitcode'
              350  BUILD_TUPLE_2         2 
              352  BINARY_MODULO    

 L.  87       354  CALL_FUNCTION_1       1  ''
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           324  '324'

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