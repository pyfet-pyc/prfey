# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: C:\python3\Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_pkgutil.py
import os, sys, pkgutil
from pyimod03_importers import FrozenImporter
SYS_PREFIX = sys._MEIPASS + os.path.sep
SYS_PREFIXLEN = len(SYS_PREFIX)
_orig_pkgutil_iter_modules = pkgutil.iter_modules

def _pyi_pkgutil_iter_modules--- This code section failed: ---

 L.  50         0  LOAD_GLOBAL              _orig_pkgutil_iter_modules
                2  LOAD_FAST                'path'
                4  LOAD_FAST                'prefix'
                6  CALL_FUNCTION_2       2  ''
                8  GET_YIELD_FROM_ITER
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  POP_TOP          

 L.  53        16  LOAD_GLOBAL              pkgutil
               18  LOAD_METHOD              iter_importers
               20  CALL_METHOD_0         0  ''
               22  GET_ITER         
             24_0  COME_FROM            36  '36'
               24  FOR_ITER             44  'to 44'
               26  STORE_FAST               'importer'

 L.  54        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'importer'
               32  LOAD_GLOBAL              FrozenImporter
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    24  'to 24'

 L.  55        38  POP_TOP          
               40  BREAK_LOOP           48  'to 48'
               42  JUMP_BACK            24  'to 24'

 L.  57        44  LOAD_CONST               None
               46  RETURN_VALUE     

 L.  59        48  LOAD_FAST                'path'
               50  POP_JUMP_IF_TRUE    112  'to 112'

 L.  62        52  LOAD_FAST                'importer'
               54  LOAD_ATTR                toc
               56  GET_ITER         
               58  FOR_ITER            110  'to 110'
               60  STORE_FAST               'entry'

 L.  63        62  LOAD_FAST                'entry'
               64  LOAD_METHOD              count
               66  LOAD_STR                 '.'
               68  CALL_METHOD_1         1  ''
               70  LOAD_CONST               0
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L.  64        76  JUMP_BACK            58  'to 58'
             78_0  COME_FROM            74  '74'

 L.  65        78  LOAD_FAST                'importer'
               80  LOAD_METHOD              is_package
               82  LOAD_FAST                'entry'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'is_pkg'

 L.  66        88  LOAD_GLOBAL              pkgutil
               90  LOAD_METHOD              ModuleInfo
               92  LOAD_FAST                'importer'
               94  LOAD_FAST                'prefix'
               96  LOAD_FAST                'entry'
               98  BINARY_ADD       
              100  LOAD_FAST                'is_pkg'
              102  CALL_METHOD_3         3  ''
              104  YIELD_VALUE      
              106  POP_TOP          
              108  JUMP_BACK            58  'to 58'
              110  JUMP_FORWARD        278  'to 278'
            112_0  COME_FROM            50  '50'

 L.  70       112  LOAD_GLOBAL              os
              114  LOAD_ATTR                path
              116  LOAD_METHOD              normpath
              118  LOAD_FAST                'path'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'pkg_path'

 L.  71       128  LOAD_FAST                'pkg_path'
              130  LOAD_METHOD              startswith
              132  LOAD_GLOBAL              SYS_PREFIX
              134  CALL_METHOD_1         1  ''
              136  POP_JUMP_IF_TRUE    142  'to 142'
              138  <74>             
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           136  '136'

 L.  73       142  LOAD_FAST                'pkg_path'
              144  LOAD_GLOBAL              SYS_PREFIXLEN
              146  LOAD_CONST               None
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  STORE_FAST               'pkg_prefix'

 L.  74       154  LOAD_FAST                'pkg_prefix'
              156  LOAD_METHOD              replace
              158  LOAD_GLOBAL              os
              160  LOAD_ATTR                path
              162  LOAD_ATTR                sep
              164  LOAD_STR                 '.'
              166  CALL_METHOD_2         2  ''
              168  STORE_FAST               'pkg_prefix'

 L.  77       170  LOAD_FAST                'pkg_prefix'
              172  LOAD_METHOD              endswith
              174  LOAD_STR                 '.'
              176  CALL_METHOD_1         1  ''
              178  POP_JUMP_IF_TRUE    188  'to 188'

 L.  78       180  LOAD_FAST                'pkg_prefix'
              182  LOAD_STR                 '.'
              184  INPLACE_ADD      
              186  STORE_FAST               'pkg_prefix'
            188_0  COME_FROM           178  '178'

 L.  79       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'pkg_prefix'
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'pkg_prefix_len'

 L.  81       196  LOAD_FAST                'importer'
              198  LOAD_ATTR                toc
              200  GET_ITER         
              202  FOR_ITER            278  'to 278'
              204  STORE_FAST               'entry'

 L.  82       206  LOAD_FAST                'entry'
              208  LOAD_METHOD              startswith
              210  LOAD_FAST                'pkg_prefix'
              212  CALL_METHOD_1         1  ''
              214  POP_JUMP_IF_TRUE    218  'to 218'

 L.  83       216  JUMP_BACK           202  'to 202'
            218_0  COME_FROM           214  '214'

 L.  84       218  LOAD_FAST                'entry'
              220  LOAD_FAST                'pkg_prefix_len'
              222  LOAD_CONST               None
              224  BUILD_SLICE_2         2 
              226  BINARY_SUBSCR    
              228  STORE_FAST               'name'

 L.  85       230  LOAD_FAST                'name'
              232  LOAD_METHOD              count
              234  LOAD_STR                 '.'
              236  CALL_METHOD_1         1  ''
              238  LOAD_CONST               0
              240  COMPARE_OP               !=
              242  POP_JUMP_IF_FALSE   246  'to 246'

 L.  86       244  JUMP_BACK           202  'to 202'
            246_0  COME_FROM           242  '242'

 L.  87       246  LOAD_FAST                'importer'
              248  LOAD_METHOD              is_package
              250  LOAD_FAST                'entry'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'is_pkg'

 L.  88       256  LOAD_GLOBAL              pkgutil
              258  LOAD_METHOD              ModuleInfo
              260  LOAD_FAST                'importer'
              262  LOAD_FAST                'prefix'
              264  LOAD_FAST                'name'
              266  BINARY_ADD       
              268  LOAD_FAST                'is_pkg'
              270  CALL_METHOD_3         3  ''
              272  YIELD_VALUE      
              274  POP_TOP          
              276  JUMP_BACK           202  'to 202'
            278_0  COME_FROM           110  '110'

Parse error at or near `<74>' instruction at offset 138


pkgutil.iter_modules = _pyi_pkgutil_iter_modules