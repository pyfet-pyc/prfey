# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: C:\Users\Admin\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_pkgres.py
import os, sys, pathlib, pkg_resources
from pyimod03_importers import FrozenImporter
SYS_PREFIX = pathlib.PurePath(sys._MEIPASS)

class _TocFilesystem:
    __doc__ = 'A prefix tree implementation for embedded filesystem reconstruction.'

    def __init__(self, toc_files, toc_dirs=[]):
        self._tree = dict()
        for path in toc_files:
            path = pathlib.PurePath(path)
            current = self._tree
            for component in path.parts[:-1]:
                current = current.setdefault(component, {})
            else:
                current[path.parts[(-1)]] = ''

        else:
            for path in toc_dirs:
                path = pathlib.PurePath(path)
                current = self._tree
                for component in path.parts:
                    current = current.setdefault(component, {})

    def _get_tree_node--- This code section failed: ---

 L.  73         0  LOAD_GLOBAL              pathlib
                2  LOAD_METHOD              PurePath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L.  74        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _tree
               14  STORE_FAST               'current'

 L.  75        16  LOAD_FAST                'path'
               18  LOAD_ATTR                parts
               20  GET_ITER         
               22  FOR_ITER             50  'to 50'
               24  STORE_FAST               'component'

 L.  76        26  LOAD_FAST                'component'
               28  LOAD_FAST                'current'
               30  <118>                 1  ''
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L.  77        34  POP_TOP          
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'

 L.  78        40  LOAD_FAST                'current'
               42  LOAD_FAST                'component'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'current'
               48  JUMP_BACK            22  'to 22'

 L.  79        50  LOAD_FAST                'current'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 30

    def path_exists--- This code section failed: ---

 L.  82         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_tree_node
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'node'

 L.  83        10  LOAD_FAST                'node'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def path_isdir--- This code section failed: ---

 L.  86         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_tree_node
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'node'

 L.  87        10  LOAD_FAST                'node'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  88        18  LOAD_CONST               False
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  89        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'node'
               26  LOAD_GLOBAL              str
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  90        32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  91        36  LOAD_CONST               True
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def path_listdir(self, path):
        node = self._get_tree_node(path)
        if not isinstance(node, dict):
            return []
        return list(node.keys())


_toc_tree_cache = {}

class PyiFrozenProvider(pkg_resources.NullProvider):
    __doc__ = 'Custom pkg_resourvces provider for FrozenImporter.'

    def __init__(self, module):
        super().__init__(module)
        self._pkg_path = pathlib.PurePath(module.__file__).parent
        self._embedded_tree = None

    def _init_embedded_tree--- This code section failed: ---

 L. 125         0  BUILD_LIST_0          0 
                2  STORE_FAST               'data_files'

 L. 126         4  BUILD_LIST_0          0 
                6  STORE_FAST               'package_dirs'

 L. 127         8  LOAD_FAST                'self'
               10  LOAD_ATTR                loader
               12  LOAD_ATTR                toc
               14  GET_ITER         
             16_0  COME_FROM            72  '72'
             16_1  COME_FROM            60  '60'
               16  FOR_ITER            102  'to 102'
               18  STORE_FAST               'entry'

 L. 128        20  LOAD_GLOBAL              pathlib
               22  LOAD_METHOD              PurePath
               24  LOAD_FAST                'entry'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'entry_path'

 L. 129        30  LOAD_FAST                'rel_pkg_path'
               32  LOAD_FAST                'entry_path'
               34  LOAD_ATTR                parents
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 131        40  LOAD_FAST                'data_files'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'entry_path'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            16  'to 16'
             52_0  COME_FROM            38  '38'

 L. 132        52  LOAD_FAST                'entry'
               54  LOAD_METHOD              startswith
               56  LOAD_FAST                'pkg_name'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    16  'to 16'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                loader
               66  LOAD_METHOD              is_package
               68  LOAD_FAST                'entry'
               70  CALL_METHOD_1         1  ''
               72  POP_JUMP_IF_FALSE    16  'to 16'

 L. 134        74  LOAD_GLOBAL              pathlib
               76  LOAD_ATTR                PurePath
               78  LOAD_FAST                'entry'
               80  LOAD_METHOD              split
               82  LOAD_STR                 '.'
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_EX      0  'positional arguments only'
               88  STORE_FAST               'package_dir'

 L. 135        90  LOAD_FAST                'package_dirs'
               92  LOAD_METHOD              append
               94  LOAD_FAST                'package_dir'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_BACK            16  'to 16'

 L. 138       102  LOAD_GLOBAL              _TocFilesystem
              104  LOAD_FAST                'data_files'
              106  LOAD_FAST                'package_dirs'
              108  CALL_FUNCTION_2       2  ''
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 36

    @property
    def embedded_tree--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _embedded_tree
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    68  'to 68'

 L. 145        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pkg_path
               14  LOAD_METHOD              relative_to
               16  LOAD_GLOBAL              SYS_PREFIX
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'rel_pkg_path'

 L. 149        22  LOAD_STR                 '.'
               24  LOAD_METHOD              join
               26  LOAD_FAST                'rel_pkg_path'
               28  LOAD_ATTR                parts
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'pkg_name'

 L. 152        34  LOAD_FAST                'pkg_name'
               36  LOAD_GLOBAL              _toc_tree_cache
               38  <118>                 1  ''
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L. 154        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _init_embedded_tree
               46  LOAD_FAST                'rel_pkg_path'
               48  LOAD_FAST                'pkg_name'
               50  CALL_METHOD_2         2  ''

 L. 153        52  LOAD_GLOBAL              _toc_tree_cache
               54  LOAD_FAST                'pkg_name'
               56  STORE_SUBSCR     
             58_0  COME_FROM            40  '40'

 L. 155        58  LOAD_GLOBAL              _toc_tree_cache
               60  LOAD_FAST                'pkg_name'
               62  BINARY_SUBSCR    
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _embedded_tree
             68_0  COME_FROM             8  '8'

 L. 156        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _embedded_tree
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _normalize_path(self, path):
        return pathlib.Path(os.path.abspath(path))

    def _is_relative_to_package--- This code section failed: ---

 L. 167         0  LOAD_FAST                'path'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pkg_path
                6  COMPARE_OP               ==
                8  JUMP_IF_TRUE_OR_POP    20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pkg_path
               14  LOAD_FAST                'path'
               16  LOAD_ATTR                parents
               18  <118>                 0  ''
             20_0  COME_FROM             8  '8'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _has(self, path):
        path = self._normalize_path(path)
        if not self._is_relative_to_package(path):
            return False
        if path.exists():
            return True
        rel_path = path.relative_to(SYS_PREFIX)
        return self.embedded_tree.path_exists(rel_path)

    def _isdir--- This code section failed: ---

 L. 184         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _normalize_path
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L. 185        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _is_relative_to_package
               14  LOAD_FAST                'path'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'

 L. 186        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 189        24  LOAD_FAST                'path'
               26  LOAD_METHOD              relative_to
               28  LOAD_GLOBAL              SYS_PREFIX
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'rel_path'

 L. 190        34  LOAD_FAST                'self'
               36  LOAD_ATTR                embedded_tree
               38  LOAD_METHOD              _get_tree_node
               40  LOAD_FAST                'rel_path'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'node'

 L. 191        46  LOAD_FAST                'node'
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 192        54  LOAD_FAST                'path'
               56  LOAD_METHOD              is_dir
               58  CALL_METHOD_0         0  ''
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 195        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'node'
               66  LOAD_GLOBAL              str
               68  CALL_FUNCTION_2       2  ''
               70  UNARY_NOT        
               72  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 50

    def _listdir(self, path):
        path = self._normalize_path(path)
        if not self._is_relative_to_package(path):
            return []
        rel_path = path.relative_to(SYS_PREFIX)
        content = self.embedded_tree.path_listdir(rel_path)
        if path.is_dir():
            path = str(path)
            content = list(set(content + os.listdir(path)))
        return content


pkg_resources.register_loader_type(FrozenImporter, PyiFrozenProvider)