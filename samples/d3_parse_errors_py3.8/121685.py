# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pywintypes.py
import importlib.util, importlib.machinery, sys, os

def __import_pywin32_system_module__--- This code section failed: ---

 L.  21         0  LOAD_STR                 '_d.pyd'
                2  LOAD_GLOBAL              importlib
                4  LOAD_ATTR                machinery
                6  LOAD_ATTR                EXTENSION_SUFFIXES
                8  COMPARE_OP               in
               10  POP_JUMP_IF_FALSE    16  'to 16'
               12  LOAD_STR                 '_d'
               14  JUMP_FORWARD         18  'to 18'
             16_0  COME_FROM            10  '10'
               16  LOAD_STR                 ''
             18_0  COME_FROM            14  '14'
               18  STORE_FAST               'suffix'

 L.  22        20  LOAD_STR                 '%s%d%d%s.dll'

 L.  23        22  LOAD_FAST                'modname'
               24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                version_info
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                version_info
               36  LOAD_CONST               1
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'suffix'
               42  BUILD_TUPLE_4         4 

 L.  22        44  BINARY_MODULO    
               46  STORE_FAST               'filename'

 L.  24        48  LOAD_GLOBAL              hasattr
               50  LOAD_GLOBAL              sys
               52  LOAD_STR                 'frozen'
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE   144  'to 144'

 L.  29        58  LOAD_GLOBAL              sys
               60  LOAD_ATTR                path
               62  GET_ITER         
             64_0  COME_FROM           122  '122'
             64_1  COME_FROM           116  '116'
               64  FOR_ITER            124  'to 124'
               66  STORE_FAST               'look'

 L.  32        68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              isfile
               74  LOAD_FAST                'look'
               76  CALL_METHOD_1         1  ''
               78  POP_JUMP_IF_FALSE    92  'to 92'

 L.  33        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              dirname
               86  LOAD_FAST                'look'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'look'
             92_0  COME_FROM            78  '78'

 L.  34        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              join
               98  LOAD_FAST                'look'
              100  LOAD_FAST                'filename'
              102  CALL_METHOD_2         2  ''
              104  STORE_FAST               'found'

 L.  35       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              isfile
              112  LOAD_FAST                'found'
              114  CALL_METHOD_1         1  ''
              116  POP_JUMP_IF_FALSE_BACK    64  'to 64'

 L.  36       118  POP_TOP          
              120  BREAK_LOOP          142  'to 142'
              122  JUMP_BACK            64  'to 64'
            124_0  COME_FROM            64  '64'

 L.  38       124  LOAD_GLOBAL              ImportError
              126  LOAD_STR                 "Module '%s' isn't in frozen sys.path %s"
              128  LOAD_FAST                'modname'
              130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                path
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           120  '120'
              142  JUMP_FORWARD        380  'to 380'
            144_0  COME_FROM            56  '56'

 L.  41       144  LOAD_CONST               0
              146  LOAD_CONST               None
              148  IMPORT_NAME              _win32sysloader
              150  STORE_FAST               '_win32sysloader'

 L.  42       152  LOAD_FAST                '_win32sysloader'
              154  LOAD_METHOD              GetModuleFilename
              156  LOAD_FAST                'filename'
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'found'

 L.  43       162  LOAD_FAST                'found'
              164  LOAD_CONST               None
              166  COMPARE_OP               is
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L.  56       170  LOAD_FAST                '_win32sysloader'
              172  LOAD_METHOD              LoadModule
              174  LOAD_FAST                'filename'
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'found'
            180_0  COME_FROM           168  '168'

 L.  57       180  LOAD_FAST                'found'
              182  LOAD_CONST               None
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   228  'to 228'

 L.  66       188  LOAD_GLOBAL              os
              190  LOAD_ATTR                path
              192  LOAD_METHOD              isfile
              194  LOAD_GLOBAL              os
              196  LOAD_ATTR                path
              198  LOAD_METHOD              join
              200  LOAD_GLOBAL              sys
              202  LOAD_ATTR                prefix
              204  LOAD_FAST                'filename'
              206  CALL_METHOD_2         2  ''
              208  CALL_METHOD_1         1  ''
              210  POP_JUMP_IF_FALSE   228  'to 228'

 L.  67       212  LOAD_GLOBAL              os
              214  LOAD_ATTR                path
              216  LOAD_METHOD              join
              218  LOAD_GLOBAL              sys
              220  LOAD_ATTR                prefix
              222  LOAD_FAST                'filename'
              224  CALL_METHOD_2         2  ''
              226  STORE_FAST               'found'
            228_0  COME_FROM           210  '210'
            228_1  COME_FROM           186  '186'

 L.  68       228  LOAD_FAST                'found'
              230  LOAD_CONST               None
              232  COMPARE_OP               is
          234_236  POP_JUMP_IF_FALSE   292  'to 292'

 L.  71       238  LOAD_GLOBAL              os
              240  LOAD_ATTR                path
              242  LOAD_METHOD              isfile
              244  LOAD_GLOBAL              os
              246  LOAD_ATTR                path
              248  LOAD_METHOD              join
              250  LOAD_GLOBAL              os
              252  LOAD_ATTR                path
              254  LOAD_METHOD              dirname
              256  LOAD_GLOBAL              __file__
              258  CALL_METHOD_1         1  ''
              260  LOAD_FAST                'filename'
              262  CALL_METHOD_2         2  ''
              264  CALL_METHOD_1         1  ''
          266_268  POP_JUMP_IF_FALSE   292  'to 292'

 L.  72       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_METHOD              join
              276  LOAD_GLOBAL              os
              278  LOAD_ATTR                path
              280  LOAD_METHOD              dirname
              282  LOAD_GLOBAL              __file__
              284  CALL_METHOD_1         1  ''
              286  LOAD_FAST                'filename'
              288  CALL_METHOD_2         2  ''
              290  STORE_FAST               'found'
            292_0  COME_FROM           266  '266'
            292_1  COME_FROM           234  '234'

 L.  73       292  LOAD_FAST                'found'
              294  LOAD_CONST               None
              296  COMPARE_OP               is
          298_300  POP_JUMP_IF_FALSE   354  'to 354'

 L.  80       302  LOAD_CONST               0
              304  LOAD_CONST               None
              306  IMPORT_NAME_ATTR         distutils.sysconfig
              308  STORE_FAST               'distutils'

 L.  81       310  LOAD_GLOBAL              os
              312  LOAD_ATTR                path
              314  LOAD_METHOD              join
              316  LOAD_FAST                'distutils'
              318  LOAD_ATTR                sysconfig
              320  LOAD_ATTR                get_python_lib
              322  LOAD_CONST               1
              324  LOAD_CONST               ('plat_specific',)
              326  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  82       328  LOAD_STR                 'pywin32_system32'

 L.  82       330  LOAD_FAST                'filename'

 L.  81       332  CALL_METHOD_3         3  ''
              334  STORE_FAST               'maybe'

 L.  83       336  LOAD_GLOBAL              os
              338  LOAD_ATTR                path
              340  LOAD_METHOD              isfile
              342  LOAD_FAST                'maybe'
              344  CALL_METHOD_1         1  ''
          346_348  POP_JUMP_IF_FALSE   354  'to 354'

 L.  84       350  LOAD_FAST                'maybe'
              352  STORE_FAST               'found'
            354_0  COME_FROM           346  '346'
            354_1  COME_FROM           298  '298'

 L.  85       354  LOAD_FAST                'found'
              356  LOAD_CONST               None
              358  COMPARE_OP               is
          360_362  POP_JUMP_IF_FALSE   380  'to 380'

 L.  87       364  LOAD_GLOBAL              ImportError
              366  LOAD_STR                 "No system module '%s' (%s)"
              368  LOAD_FAST                'modname'
              370  LOAD_FAST                'filename'
              372  BUILD_TUPLE_2         2 
              374  BINARY_MODULO    
              376  CALL_FUNCTION_1       1  ''
              378  RAISE_VARARGS_1       1  'exception instance'
            380_0  COME_FROM           360  '360'
            380_1  COME_FROM           142  '142'

 L.  91       380  LOAD_GLOBAL              sys
              382  LOAD_ATTR                modules
              384  LOAD_FAST                'modname'
              386  BINARY_SUBSCR    
              388  STORE_FAST               'old_mod'

 L.  93       390  LOAD_GLOBAL              importlib
              392  LOAD_ATTR                machinery
              394  LOAD_METHOD              ExtensionFileLoader
              396  LOAD_FAST                'modname'
              398  LOAD_FAST                'found'
              400  CALL_METHOD_2         2  ''
              402  STORE_FAST               'loader'

 L.  94       404  LOAD_GLOBAL              importlib
              406  LOAD_ATTR                machinery
              408  LOAD_ATTR                ModuleSpec
              410  LOAD_FAST                'modname'
              412  LOAD_FAST                'loader'
              414  LOAD_FAST                'found'
              416  LOAD_CONST               ('name', 'loader', 'origin')
              418  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              420  STORE_FAST               'spec'

 L.  95       422  LOAD_GLOBAL              importlib
              424  LOAD_ATTR                util
              426  LOAD_METHOD              module_from_spec
              428  LOAD_FAST                'spec'
              430  CALL_METHOD_1         1  ''
              432  STORE_FAST               'mod'

 L.  96       434  LOAD_FAST                'spec'
              436  LOAD_ATTR                loader
              438  LOAD_METHOD              exec_module
              440  LOAD_FAST                'mod'
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          

 L.  99       446  LOAD_GLOBAL              sys
              448  LOAD_ATTR                modules
              450  LOAD_FAST                'modname'
              452  BINARY_SUBSCR    
              454  LOAD_FAST                'old_mod'
              456  COMPARE_OP               is-not
          458_460  POP_JUMP_IF_TRUE    466  'to 466'
              462  LOAD_ASSERT              AssertionError
              464  RAISE_VARARGS_1       1  'exception instance'
            466_0  COME_FROM           458  '458'

 L. 100       466  LOAD_GLOBAL              sys
              468  LOAD_ATTR                modules
              470  LOAD_FAST                'modname'
              472  BINARY_SUBSCR    
              474  LOAD_FAST                'mod'
              476  COMPARE_OP               is
          478_480  POP_JUMP_IF_TRUE    486  'to 486'
              482  LOAD_ASSERT              AssertionError
              484  RAISE_VARARGS_1       1  'exception instance'
            486_0  COME_FROM           478  '478'

 L. 102       486  LOAD_FAST                'old_mod'
              488  LOAD_GLOBAL              sys
              490  LOAD_ATTR                modules
              492  LOAD_FAST                'modname'
              494  STORE_SUBSCR     

 L. 103       496  LOAD_FAST                'globs'
              498  LOAD_METHOD              update
              500  LOAD_FAST                'mod'
              502  LOAD_ATTR                __dict__
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          

Parse error at or near `CALL_METHOD_1' instruction at offset 504


__import_pywin32_system_module__('pywintypes', globals())