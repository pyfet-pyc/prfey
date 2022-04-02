# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\core.py
"""distutils.core

The only module that needs to be imported to use the Distutils; provides
the 'setup' function (which is to be called from the setup script).  Also
indirectly provides the Distribution and Command classes, although they are
really defined in distutils.dist and distutils.cmd.
"""
import os, sys
from distutils.debug import DEBUG
from distutils.errors import *
from distutils.dist import Distribution
from distutils.cmd import Command
from distutils.config import PyPIRCCommand
from distutils.extension import Extension
USAGE = 'usage: %(script)s [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]\n   or: %(script)s --help [cmd1 cmd2 ...]\n   or: %(script)s --help-commands\n   or: %(script)s cmd --help\n'

def gen_usage(script_name):
    script = os.path.basename(script_name)
    return USAGE % vars()


_setup_stop_after = None
_setup_distribution = None
setup_keywords = ('distclass', 'script_name', 'script_args', 'options', 'name', 'version',
                  'author', 'author_email', 'maintainer', 'maintainer_email', 'url',
                  'license', 'description', 'long_description', 'keywords', 'platforms',
                  'classifiers', 'download_url', 'requires', 'provides', 'obsoletes')
extension_keywords = ('name', 'sources', 'include_dirs', 'define_macros', 'undef_macros',
                      'library_dirs', 'libraries', 'runtime_library_dirs', 'extra_objects',
                      'extra_compile_args', 'extra_link_args', 'swig_opts', 'export_symbols',
                      'depends', 'language')

def setup--- This code section failed: ---

 L.  94         0  LOAD_FAST                'attrs'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'distclass'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'klass'

 L.  95        10  LOAD_FAST                'klass'
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L.  96        14  LOAD_FAST                'attrs'
               16  LOAD_STR                 'distclass'
               18  DELETE_SUBSCR    
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM            12  '12'

 L.  98        22  LOAD_GLOBAL              Distribution
               24  STORE_FAST               'klass'
             26_0  COME_FROM            20  '20'

 L. 100        26  LOAD_STR                 'script_name'
               28  LOAD_FAST                'attrs'
               30  <118>                 1  ''
               32  POP_JUMP_IF_FALSE    56  'to 56'

 L. 101        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              basename
               40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                argv
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  CALL_METHOD_1         1  ''
               50  LOAD_FAST                'attrs'
               52  LOAD_STR                 'script_name'
               54  STORE_SUBSCR     
             56_0  COME_FROM            32  '32'

 L. 102        56  LOAD_STR                 'script_args'
               58  LOAD_FAST                'attrs'
               60  <118>                 1  ''
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 103        64  LOAD_GLOBAL              sys
               66  LOAD_ATTR                argv
               68  LOAD_CONST               1
               70  LOAD_CONST               None
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'attrs'
               78  LOAD_STR                 'script_args'
               80  STORE_SUBSCR     
             82_0  COME_FROM            62  '62'

 L. 107        82  SETUP_FINALLY       100  'to 100'

 L. 108        84  LOAD_FAST                'klass'
               86  LOAD_FAST                'attrs'
               88  CALL_FUNCTION_1       1  ''
               90  DUP_TOP          
               92  STORE_GLOBAL             _setup_distribution
               94  STORE_FAST               'dist'
               96  POP_BLOCK        
               98  JUMP_FORWARD        178  'to 178'
            100_0  COME_FROM_FINALLY    82  '82'

 L. 109       100  DUP_TOP          
              102  LOAD_GLOBAL              DistutilsSetupError
              104  <121>               176  ''
              106  POP_TOP          
              108  STORE_FAST               'msg'
              110  POP_TOP          
              112  SETUP_FINALLY       168  'to 168'

 L. 110       114  LOAD_STR                 'name'
              116  LOAD_FAST                'attrs'
              118  <118>                 1  ''
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L. 111       122  LOAD_GLOBAL              SystemExit
              124  LOAD_STR                 'error in setup command: %s'
              126  LOAD_FAST                'msg'
              128  BINARY_MODULO    
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
              134  JUMP_FORWARD        156  'to 156'
            136_0  COME_FROM           120  '120'

 L. 113       136  LOAD_GLOBAL              SystemExit
              138  LOAD_STR                 'error in %s setup command: %s'

 L. 114       140  LOAD_FAST                'attrs'
              142  LOAD_STR                 'name'
              144  BINARY_SUBSCR    
              146  LOAD_FAST                'msg'
              148  BUILD_TUPLE_2         2 

 L. 113       150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           134  '134'
              156  POP_BLOCK        
              158  POP_EXCEPT       
              160  LOAD_CONST               None
              162  STORE_FAST               'msg'
              164  DELETE_FAST              'msg'
              166  JUMP_FORWARD        178  'to 178'
            168_0  COME_FROM_FINALLY   112  '112'
              168  LOAD_CONST               None
              170  STORE_FAST               'msg'
              172  DELETE_FAST              'msg'
              174  <48>             
              176  <48>             
            178_0  COME_FROM           166  '166'
            178_1  COME_FROM            98  '98'

 L. 116       178  LOAD_GLOBAL              _setup_stop_after
              180  LOAD_STR                 'init'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   190  'to 190'

 L. 117       186  LOAD_FAST                'dist'
              188  RETURN_VALUE     
            190_0  COME_FROM           184  '184'

 L. 121       190  LOAD_FAST                'dist'
              192  LOAD_METHOD              parse_config_files
              194  CALL_METHOD_0         0  ''
              196  POP_TOP          

 L. 123       198  LOAD_GLOBAL              DEBUG
              200  POP_JUMP_IF_FALSE   218  'to 218'

 L. 124       202  LOAD_GLOBAL              print
              204  LOAD_STR                 'options (after parsing config files):'
              206  CALL_FUNCTION_1       1  ''
              208  POP_TOP          

 L. 125       210  LOAD_FAST                'dist'
              212  LOAD_METHOD              dump_option_dicts
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          
            218_0  COME_FROM           200  '200'

 L. 127       218  LOAD_GLOBAL              _setup_stop_after
              220  LOAD_STR                 'config'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   230  'to 230'

 L. 128       226  LOAD_FAST                'dist'
              228  RETURN_VALUE     
            230_0  COME_FROM           224  '224'

 L. 133       230  SETUP_FINALLY       244  'to 244'

 L. 134       232  LOAD_FAST                'dist'
              234  LOAD_METHOD              parse_command_line
              236  CALL_METHOD_0         0  ''
              238  STORE_FAST               'ok'
              240  POP_BLOCK        
              242  JUMP_FORWARD        304  'to 304'
            244_0  COME_FROM_FINALLY   230  '230'

 L. 135       244  DUP_TOP          
              246  LOAD_GLOBAL              DistutilsArgError
          248_250  <121>               302  ''
              252  POP_TOP          
              254  STORE_FAST               'msg'
              256  POP_TOP          
              258  SETUP_FINALLY       294  'to 294'

 L. 136       260  LOAD_GLOBAL              SystemExit
              262  LOAD_GLOBAL              gen_usage
              264  LOAD_FAST                'dist'
              266  LOAD_ATTR                script_name
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_STR                 '\nerror: %s'
              272  LOAD_FAST                'msg'
              274  BINARY_MODULO    
              276  BINARY_ADD       
              278  CALL_FUNCTION_1       1  ''
              280  RAISE_VARARGS_1       1  'exception instance'
              282  POP_BLOCK        
              284  POP_EXCEPT       
              286  LOAD_CONST               None
              288  STORE_FAST               'msg'
              290  DELETE_FAST              'msg'
              292  JUMP_FORWARD        304  'to 304'
            294_0  COME_FROM_FINALLY   258  '258'
              294  LOAD_CONST               None
              296  STORE_FAST               'msg'
              298  DELETE_FAST              'msg'
              300  <48>             
              302  <48>             
            304_0  COME_FROM           292  '292'
            304_1  COME_FROM           242  '242'

 L. 138       304  LOAD_GLOBAL              DEBUG
          306_308  POP_JUMP_IF_FALSE   326  'to 326'

 L. 139       310  LOAD_GLOBAL              print
              312  LOAD_STR                 'options (after parsing command line):'
              314  CALL_FUNCTION_1       1  ''
              316  POP_TOP          

 L. 140       318  LOAD_FAST                'dist'
              320  LOAD_METHOD              dump_option_dicts
              322  CALL_METHOD_0         0  ''
              324  POP_TOP          
            326_0  COME_FROM           306  '306'

 L. 142       326  LOAD_GLOBAL              _setup_stop_after
              328  LOAD_STR                 'commandline'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   340  'to 340'

 L. 143       336  LOAD_FAST                'dist'
              338  RETURN_VALUE     
            340_0  COME_FROM           332  '332'

 L. 146       340  LOAD_FAST                'ok'
          342_344  POP_JUMP_IF_FALSE   532  'to 532'

 L. 147       346  SETUP_FINALLY       360  'to 360'

 L. 148       348  LOAD_FAST                'dist'
              350  LOAD_METHOD              run_commands
              352  CALL_METHOD_0         0  ''
              354  POP_TOP          
              356  POP_BLOCK        
              358  JUMP_FORWARD        532  'to 532'
            360_0  COME_FROM_FINALLY   346  '346'

 L. 149       360  DUP_TOP          
              362  LOAD_GLOBAL              KeyboardInterrupt
          364_366  <121>               386  ''
              368  POP_TOP          
              370  POP_TOP          
              372  POP_TOP          

 L. 150       374  LOAD_GLOBAL              SystemExit
              376  LOAD_STR                 'interrupted'
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
              382  POP_EXCEPT       
              384  JUMP_FORWARD        532  'to 532'

 L. 151       386  DUP_TOP          
              388  LOAD_GLOBAL              OSError
          390_392  <121>               464  ''
              394  POP_TOP          
              396  STORE_FAST               'exc'
              398  POP_TOP          
              400  SETUP_FINALLY       456  'to 456'

 L. 152       402  LOAD_GLOBAL              DEBUG
          404_406  POP_JUMP_IF_FALSE   430  'to 430'

 L. 153       408  LOAD_GLOBAL              sys
              410  LOAD_ATTR                stderr
              412  LOAD_METHOD              write
              414  LOAD_STR                 'error: %s\n'
              416  LOAD_FAST                'exc'
              418  BUILD_TUPLE_1         1 
              420  BINARY_MODULO    
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          

 L. 154       426  RAISE_VARARGS_0       0  'reraise'
              428  JUMP_FORWARD        444  'to 444'
            430_0  COME_FROM           404  '404'

 L. 156       430  LOAD_GLOBAL              SystemExit
              432  LOAD_STR                 'error: %s'
              434  LOAD_FAST                'exc'
              436  BUILD_TUPLE_1         1 
              438  BINARY_MODULO    
              440  CALL_FUNCTION_1       1  ''
              442  RAISE_VARARGS_1       1  'exception instance'
            444_0  COME_FROM           428  '428'
              444  POP_BLOCK        
              446  POP_EXCEPT       
              448  LOAD_CONST               None
              450  STORE_FAST               'exc'
              452  DELETE_FAST              'exc'
              454  JUMP_FORWARD        532  'to 532'
            456_0  COME_FROM_FINALLY   400  '400'
              456  LOAD_CONST               None
              458  STORE_FAST               'exc'
              460  DELETE_FAST              'exc'
              462  <48>             

 L. 158       464  DUP_TOP          
              466  LOAD_GLOBAL              DistutilsError

 L. 159       468  LOAD_GLOBAL              CCompilerError

 L. 158       470  BUILD_TUPLE_2         2 
          472_474  <121>               530  ''
              476  POP_TOP          
              478  STORE_FAST               'msg'
              480  POP_TOP          
              482  SETUP_FINALLY       522  'to 522'

 L. 160       484  LOAD_GLOBAL              DEBUG
          486_488  POP_JUMP_IF_FALSE   494  'to 494'

 L. 161       490  RAISE_VARARGS_0       0  'reraise'
              492  JUMP_FORWARD        510  'to 510'
            494_0  COME_FROM           486  '486'

 L. 163       494  LOAD_GLOBAL              SystemExit
              496  LOAD_STR                 'error: '
              498  LOAD_GLOBAL              str
              500  LOAD_FAST                'msg'
              502  CALL_FUNCTION_1       1  ''
              504  BINARY_ADD       
              506  CALL_FUNCTION_1       1  ''
              508  RAISE_VARARGS_1       1  'exception instance'
            510_0  COME_FROM           492  '492'
              510  POP_BLOCK        
              512  POP_EXCEPT       
              514  LOAD_CONST               None
              516  STORE_FAST               'msg'
              518  DELETE_FAST              'msg'
              520  JUMP_FORWARD        532  'to 532'
            522_0  COME_FROM_FINALLY   482  '482'
              522  LOAD_CONST               None
              524  STORE_FAST               'msg'
              526  DELETE_FAST              'msg'
              528  <48>             
              530  <48>             
            532_0  COME_FROM           520  '520'
            532_1  COME_FROM           454  '454'
            532_2  COME_FROM           384  '384'
            532_3  COME_FROM           358  '358'
            532_4  COME_FROM           342  '342'

 L. 165       532  LOAD_FAST                'dist'
              534  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 30


def run_setup--- This code section failed: ---

 L. 201         0  LOAD_FAST                'stop_after'
                2  LOAD_CONST               ('init', 'config', 'commandline', 'run')
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 202         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "invalid value for 'stop_after': %r"
               12  LOAD_FAST                'stop_after'
               14  BUILD_TUPLE_1         1 
               16  BINARY_MODULO    
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 205        22  LOAD_FAST                'stop_after'
               24  STORE_GLOBAL             _setup_stop_after

 L. 207        26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                argv
               30  LOAD_METHOD              copy
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'save_argv'

 L. 208        36  LOAD_STR                 '__file__'
               38  LOAD_FAST                'script_name'
               40  BUILD_MAP_1           1 
               42  STORE_FAST               'g'

 L. 209        44  SETUP_FINALLY       166  'to 166'

 L. 210        46  SETUP_FINALLY       150  'to 150'

 L. 211        48  LOAD_FAST                'script_name'
               50  LOAD_GLOBAL              sys
               52  LOAD_ATTR                argv
               54  LOAD_CONST               0
               56  STORE_SUBSCR     

 L. 212        58  LOAD_FAST                'script_args'
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L. 213        66  LOAD_FAST                'script_args'
               68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                argv
               72  LOAD_CONST               1
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  STORE_SUBSCR     
             80_0  COME_FROM            64  '64'

 L. 214        80  LOAD_GLOBAL              open
               82  LOAD_FAST                'script_name'
               84  LOAD_STR                 'rb'
               86  CALL_FUNCTION_2       2  ''
               88  SETUP_WITH          120  'to 120'
               90  STORE_FAST               'f'

 L. 215        92  LOAD_GLOBAL              exec
               94  LOAD_FAST                'f'
               96  LOAD_METHOD              read
               98  CALL_METHOD_0         0  ''
              100  LOAD_FAST                'g'
              102  CALL_FUNCTION_2       2  ''
              104  POP_TOP          
              106  POP_BLOCK        
              108  LOAD_CONST               None
              110  DUP_TOP          
              112  DUP_TOP          
              114  CALL_FUNCTION_3       3  ''
              116  POP_TOP          
              118  JUMP_FORWARD        136  'to 136'
            120_0  COME_FROM_WITH       88  '88'
              120  <49>             
              122  POP_JUMP_IF_TRUE    126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          
              132  POP_EXCEPT       
              134  POP_TOP          
            136_0  COME_FROM           118  '118'
              136  POP_BLOCK        

 L. 217       138  LOAD_FAST                'save_argv'
              140  LOAD_GLOBAL              sys
              142  STORE_ATTR               argv

 L. 218       144  LOAD_CONST               None
              146  STORE_GLOBAL             _setup_stop_after
              148  JUMP_FORWARD        162  'to 162'
            150_0  COME_FROM_FINALLY    46  '46'

 L. 217       150  LOAD_FAST                'save_argv'
              152  LOAD_GLOBAL              sys
              154  STORE_ATTR               argv

 L. 218       156  LOAD_CONST               None
              158  STORE_GLOBAL             _setup_stop_after
              160  <48>             
            162_0  COME_FROM           148  '148'
              162  POP_BLOCK        
              164  JUMP_FORWARD        184  'to 184'
            166_0  COME_FROM_FINALLY    44  '44'

 L. 219       166  DUP_TOP          
              168  LOAD_GLOBAL              SystemExit
              170  <121>               182  ''
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 222       178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           164  '164'

 L. 224       184  LOAD_GLOBAL              _setup_distribution
              186  LOAD_CONST               None
              188  <117>                 0  ''
              190  POP_JUMP_IF_FALSE   204  'to 204'

 L. 225       192  LOAD_GLOBAL              RuntimeError
              194  LOAD_STR                 "'distutils.core.setup()' was never called -- perhaps '%s' is not a Distutils setup script?"

 L. 227       196  LOAD_FAST                'script_name'

 L. 225       198  BINARY_MODULO    
              200  CALL_FUNCTION_1       1  ''
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           190  '190'

 L. 232       204  LOAD_GLOBAL              _setup_distribution
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


# global _setup_distribution ## Warning: Unused global
# global _setup_stop_after ## Warning: Unused global