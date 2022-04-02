# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: c:\users\win10\appdata\local\programs\python\python39\lib\site-packages\PyInstaller\loader\pyimod03_importers.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 23707 bytes
"""
PEP-302 and PEP-451 importers for frozen applications.
"""
import sys, _frozen_importlib, pyimod01_os_path as pyi_os_path
from pyimod02_archive import ArchiveReadError, ZlibArchiveReader
SYS_PREFIX = sys._MEIPASS
SYS_PREFIXLEN = len(SYS_PREFIX)
imp_new_module = type(sys)
if sys.flags.verbose:

    def trace(msg, *a):
        sys.stderr.write(msg % a)
        sys.stderr.write('\n')


else:

    def trace(msg, *a):
        pass


class FrozenPackageImporter(object):
    __doc__ = '\n    Wrapper class for FrozenImporter that imports one specific fullname from\n    a module named by an alternate fullname. The alternate fullname is derived from the\n    __path__ of the package module containing that module.\n\n    This is called by FrozenImporter.find_module whenever a module is found as a result\n    of searching module.__path__\n    '

    def __init__(self, importer, entry_name):
        self._entry_name = entry_name
        self._importer = importer

    def load_module(self, fullname):
        return self._importer.load_module(fullname, self._entry_name)


class FrozenImporter(object):
    __doc__ = "\n    Load bytecode of Python modules from the executable created by PyInstaller.\n\n    Python bytecode is zipped and appended to the executable.\n\n    NOTE: PYZ format cannot be replaced by zipimport module.\n\n    The problem is that we have no control over zipimport; for instance,\n    it doesn't work if the zip file is embedded into a PKG appended\n    to an executable, like we create in one-file.\n\n    This is PEP-302 finder and loader class for the ``sys.meta_path`` hook.\n    A PEP-302 finder requires method find_module() to return loader\n    class with method load_module(). Both these methods are implemented\n    in one class.\n\n    This is also a PEP-451 finder and loader class for the ModuleSpec type\n    import system. A PEP-451 finder requires method find_spec(), a PEP-451\n    loader requires methods exec_module(), load_module(9 and (optionally)\n    create_module(). All these methods are implemented in this one class.\n\n    To use this class just call\n\n        FrozenImporter.install()\n    "

    def __init__--- This code section failed: ---

 L.  98         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                path
                4  GET_ITER         
              6_0  COME_FROM           112  '112'
              6_1  COME_FROM           108  '108'
              6_2  COME_FROM           104  '104'
              6_3  COME_FROM            88  '88'
              6_4  COME_FROM            84  '84'
                6  FOR_ITER            114  'to 114'
                8  STORE_FAST               'pyz_filepath'

 L.  99        10  SETUP_FINALLY        70  'to 70'

 L. 101        12  LOAD_GLOBAL              ZlibArchiveReader
               14  LOAD_FAST                'pyz_filepath'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _pyz_archive

 L. 109        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                path
               26  LOAD_METHOD              remove
               28  LOAD_FAST                'pyz_filepath'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 112        34  LOAD_GLOBAL              set
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _pyz_archive
               40  LOAD_ATTR                toc
               42  LOAD_METHOD              keys
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               toc

 L. 114        52  LOAD_GLOBAL              trace
               54  LOAD_STR                 '# PyInstaller: FrozenImporter(%s)'
               56  LOAD_FAST                'pyz_filepath'
               58  CALL_FUNCTION_2       2  ''
               60  POP_TOP          

 L. 115        62  POP_BLOCK        
               64  POP_TOP          
               66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    10  '10'

 L. 116        70  DUP_TOP          
               72  LOAD_GLOBAL              IOError
               74  <121>                90  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 118        82  POP_EXCEPT       
               84  JUMP_BACK             6  'to 6'
               86  POP_EXCEPT       
               88  JUMP_BACK             6  'to 6'

 L. 119        90  DUP_TOP          
               92  LOAD_GLOBAL              ArchiveReadError
               94  <121>               110  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 121       102  POP_EXCEPT       
              104  JUMP_BACK             6  'to 6'
              106  POP_EXCEPT       
              108  JUMP_BACK             6  'to 6'
              110  <48>             
              112  JUMP_BACK             6  'to 6'
            114_0  COME_FROM             6  '6'

 L. 124       114  LOAD_GLOBAL              ImportError
              116  LOAD_STR                 "Can't load frozen modules."
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `DUP_TOP' instruction at offset 70

    def find_module--- This code section failed: ---

 L. 140         0  LOAD_CONST               None
                2  STORE_FAST               'module_loader'

 L. 142         4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                toc
               10  <118>                 0  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 144        14  LOAD_FAST                'self'
               16  STORE_FAST               'module_loader'

 L. 145        18  LOAD_GLOBAL              trace
               20  LOAD_STR                 'import %s # PyInstaller PYZ'
               22  LOAD_FAST                'fullname'
               24  CALL_FUNCTION_2       2  ''
               26  POP_TOP          
               28  JUMP_FORWARD        174  'to 174'
             30_0  COME_FROM            12  '12'

 L. 146        30  LOAD_FAST                'path'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   174  'to 174'

 L. 151        38  LOAD_FAST                'fullname'
               40  LOAD_METHOD              split
               42  LOAD_STR                 '.'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'modname'

 L. 153        52  LOAD_FAST                'path'
               54  GET_ITER         
             56_0  COME_FROM           172  '172'
             56_1  COME_FROM           142  '142'
             56_2  COME_FROM            92  '92'
               56  FOR_ITER            174  'to 174'
               58  STORE_FAST               'p'

 L. 154        60  LOAD_FAST                'p'
               62  LOAD_GLOBAL              SYS_PREFIXLEN
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  STORE_FAST               'p'

 L. 155        76  LOAD_FAST                'p'
               78  LOAD_METHOD              split
               80  LOAD_GLOBAL              pyi_os_path
               82  LOAD_ATTR                os_sep
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'parts'

 L. 156        88  LOAD_FAST                'parts'
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  JUMP_BACK            56  'to 56'
             94_0  COME_FROM            90  '90'

 L. 157        94  LOAD_FAST                'parts'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  POP_JUMP_IF_TRUE    114  'to 114'

 L. 158       102  LOAD_FAST                'parts'
              104  LOAD_CONST               1
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  STORE_FAST               'parts'
            114_0  COME_FROM           100  '100'

 L. 159       114  LOAD_FAST                'parts'
              116  LOAD_METHOD              append
              118  LOAD_FAST                'modname'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 160       124  LOAD_STR                 '.'
              126  LOAD_METHOD              join
              128  LOAD_FAST                'parts'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'entry_name'

 L. 161       134  LOAD_FAST                'entry_name'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                toc
              140  <118>                 0  ''
              142  POP_JUMP_IF_FALSE_BACK    56  'to 56'

 L. 162       144  LOAD_GLOBAL              FrozenPackageImporter
              146  LOAD_FAST                'self'
              148  LOAD_FAST                'entry_name'
              150  CALL_FUNCTION_2       2  ''
              152  STORE_FAST               'module_loader'

 L. 163       154  LOAD_GLOBAL              trace
              156  LOAD_STR                 'import %s as %s # PyInstaller PYZ (__path__ override: %s)'

 L. 164       158  LOAD_FAST                'entry_name'
              160  LOAD_FAST                'fullname'
              162  LOAD_FAST                'p'

 L. 163       164  CALL_FUNCTION_4       4  ''
              166  POP_TOP          

 L. 165       168  POP_TOP          
              170  BREAK_LOOP          174  'to 174'
              172  JUMP_BACK            56  'to 56'
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM            56  '56'
            174_2  COME_FROM            36  '36'
            174_3  COME_FROM            28  '28'

 L. 167       174  LOAD_FAST                'module_loader'
              176  LOAD_CONST               None
              178  <117>                 0  ''
              180  POP_JUMP_IF_FALSE   192  'to 192'

 L. 168       182  LOAD_GLOBAL              trace
              184  LOAD_STR                 '# %s not found in PYZ'
              186  LOAD_FAST                'fullname'
              188  CALL_FUNCTION_2       2  ''
              190  POP_TOP          
            192_0  COME_FROM           180  '180'

 L. 169       192  LOAD_FAST                'module_loader'
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 10

    def load_module--- This code section failed: ---

 L. 185         0  LOAD_CONST               None
                2  STORE_FAST               'module'

 L. 186         4  LOAD_FAST                'entry_name'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 187        12  LOAD_FAST                'fullname'
               14  STORE_FAST               'entry_name'
             16_0  COME_FROM            10  '10'

 L. 188        16  SETUP_FINALLY       184  'to 184'

 L. 191        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                modules
               22  LOAD_METHOD              get
               24  LOAD_FAST                'fullname'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'module'

 L. 194        30  LOAD_FAST                'module'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE   180  'to 180'

 L. 196        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _pyz_archive
               42  LOAD_METHOD              extract
               44  LOAD_FAST                'entry_name'
               46  CALL_METHOD_1         1  ''
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'is_pkg'
               52  STORE_FAST               'bytecode'

 L. 198        54  LOAD_GLOBAL              imp_new_module
               56  LOAD_FAST                'fullname'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'module'

 L. 206        62  LOAD_FAST                'self'
               64  LOAD_METHOD              get_filename
               66  LOAD_FAST                'entry_name'
               68  CALL_METHOD_1         1  ''
               70  LOAD_FAST                'module'
               72  STORE_ATTR               __file__

 L. 211        74  LOAD_FAST                'is_pkg'
               76  POP_JUMP_IF_FALSE    94  'to 94'

 L. 226        78  LOAD_GLOBAL              pyi_os_path
               80  LOAD_METHOD              os_path_dirname
               82  LOAD_FAST                'module'
               84  LOAD_ATTR                __file__
               86  CALL_METHOD_1         1  ''
               88  BUILD_LIST_1          1 
               90  LOAD_FAST                'module'
               92  STORE_ATTR               __path__
             94_0  COME_FROM            76  '76'

 L. 232        94  LOAD_FAST                'self'
               96  LOAD_FAST                'module'
               98  STORE_ATTR               __loader__

 L. 241       100  LOAD_FAST                'is_pkg'
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 242       104  LOAD_FAST                'fullname'
              106  LOAD_FAST                'module'
              108  STORE_ATTR               __package__
              110  JUMP_FORWARD        130  'to 130'
            112_0  COME_FROM           102  '102'

 L. 244       112  LOAD_FAST                'fullname'
              114  LOAD_METHOD              rsplit
              116  LOAD_STR                 '.'
              118  LOAD_CONST               1
              120  CALL_METHOD_2         2  ''
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'module'
              128  STORE_ATTR               __package__
            130_0  COME_FROM           110  '110'

 L. 249       130  LOAD_GLOBAL              _frozen_importlib
              132  LOAD_ATTR                ModuleSpec

 L. 250       134  LOAD_FAST                'entry_name'
              136  LOAD_FAST                'self'
              138  LOAD_FAST                'is_pkg'

 L. 249       140  LOAD_CONST               ('is_package',)
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  LOAD_FAST                'module'
              146  STORE_ATTR               __spec__

 L. 258       148  LOAD_FAST                'module'
              150  LOAD_GLOBAL              sys
              152  LOAD_ATTR                modules
              154  LOAD_FAST                'fullname'
              156  STORE_SUBSCR     

 L. 261       158  LOAD_GLOBAL              exec
              160  LOAD_FAST                'bytecode'
              162  LOAD_FAST                'module'
              164  LOAD_ATTR                __dict__
              166  CALL_FUNCTION_2       2  ''
              168  POP_TOP          

 L. 263       170  LOAD_GLOBAL              sys
              172  LOAD_ATTR                modules
              174  LOAD_FAST                'fullname'
              176  BINARY_SUBSCR    
              178  STORE_FAST               'module'
            180_0  COME_FROM            36  '36'
              180  POP_BLOCK        
              182  JUMP_FORWARD        226  'to 226'
            184_0  COME_FROM_FINALLY    16  '16'

 L. 265       184  DUP_TOP          
              186  LOAD_GLOBAL              Exception
              188  <121>               224  ''
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 267       196  LOAD_FAST                'fullname'
              198  LOAD_GLOBAL              sys
              200  LOAD_ATTR                modules
              202  <118>                 0  ''
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L. 268       206  LOAD_GLOBAL              sys
              208  LOAD_ATTR                modules
              210  LOAD_METHOD              pop
              212  LOAD_FAST                'fullname'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L. 273       218  RAISE_VARARGS_0       0  'reraise'
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           182  '182'

 L. 277       226  LOAD_FAST                'module'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8

    def is_package--- This code section failed: ---

 L. 282         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    78  'to 78'

 L. 283        10  SETUP_FINALLY        26  'to 26'

 L. 284        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _pyz_archive
               16  LOAD_METHOD              is_package
               18  LOAD_FAST                'fullname'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L. 285        26  DUP_TOP          
               28  LOAD_GLOBAL              Exception
               30  <121>                74  ''
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        66  'to 66'

 L. 286        40  LOAD_GLOBAL              ImportError

 L. 287        42  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               44  LOAD_FAST                'fullname'
               46  BINARY_ADD       

 L. 286        48  CALL_FUNCTION_1       1  ''

 L. 288        50  LOAD_FAST                'e'

 L. 286        52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  JUMP_FORWARD         90  'to 90'
             66_0  COME_FROM_FINALLY    38  '38'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  <48>             
               74  <48>             
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM             8  '8'

 L. 290        78  LOAD_GLOBAL              ImportError
               80  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               82  LOAD_FAST                'fullname'
               84  BINARY_ADD       
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            76  '76'
             90_1  COME_FROM            64  '64'

Parse error at or near `None' instruction at offset -1

    def get_code--- This code section failed: ---

 L. 298         0  SETUP_FINALLY        20  'to 20'

 L. 302         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pyz_archive
                6  LOAD_METHOD              extract
                8  LOAD_FAST                'fullname'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               1
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 303        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                68  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        60  'to 60'

 L. 304        34  LOAD_GLOBAL              ImportError

 L. 305        36  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               38  LOAD_FAST                'fullname'
               40  BINARY_ADD       

 L. 304        42  CALL_FUNCTION_1       1  ''

 L. 306        44  LOAD_FAST                'e'

 L. 304        46  RAISE_VARARGS_2       2  'exception instance with __cause__'
               48  POP_BLOCK        
               50  POP_EXCEPT       
               52  LOAD_CONST               None
               54  STORE_FAST               'e'
               56  DELETE_FAST              'e'
               58  JUMP_FORWARD         70  'to 70'
             60_0  COME_FROM_FINALLY    32  '32'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  <48>             
               68  <48>             
             70_0  COME_FROM            58  '58'

Parse error at or near `<121>' instruction at offset 24

    def get_source--- This code section failed: ---

 L. 315         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 316        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 319        14  LOAD_GLOBAL              ImportError
               16  LOAD_STR                 'No module named '
               18  LOAD_FAST                'fullname'
               20  BINARY_ADD       
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    def get_data--- This code section failed: ---

 L. 332         0  LOAD_FAST                'path'
                2  LOAD_METHOD              startswith
                4  LOAD_GLOBAL              SYS_PREFIX
                6  LOAD_GLOBAL              pyi_os_path
                8  LOAD_ATTR                os_sep
               10  BINARY_ADD       
               12  CALL_METHOD_1         1  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 333        20  LOAD_FAST                'path'
               22  LOAD_GLOBAL              SYS_PREFIXLEN
               24  LOAD_CONST               1
               26  BINARY_ADD       
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  STORE_FAST               'fullname'

 L. 334        36  LOAD_FAST                'fullname'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                toc
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 336        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _pyz_archive
               50  LOAD_METHOD              extract
               52  LOAD_FAST                'fullname'
               54  CALL_METHOD_1         1  ''
               56  LOAD_CONST               1
               58  BINARY_SUBSCR    
               60  RETURN_VALUE     
             62_0  COME_FROM            44  '44'

 L. 341        62  LOAD_GLOBAL              open
               64  LOAD_FAST                'path'
               66  LOAD_STR                 'rb'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH           96  'to 96'
               72  STORE_FAST               'fp'

 L. 342        74  LOAD_FAST                'fp'
               76  LOAD_METHOD              read
               78  CALL_METHOD_0         0  ''
               80  POP_BLOCK        
               82  ROT_TWO          
               84  LOAD_CONST               None
               86  DUP_TOP          
               88  DUP_TOP          
               90  CALL_FUNCTION_3       3  ''
               92  POP_TOP          
               94  RETURN_VALUE     
             96_0  COME_FROM_WITH       70  '70'
               96  <49>             
               98  POP_JUMP_IF_TRUE    102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          
              108  POP_EXCEPT       
              110  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def get_filename(self, fullname):
        """
        This method should return the value that __file__ would be set to
        if the named module was loaded. If the module is not found, then
        ImportError should be raised.
        """
        if self.is_package(fullname):
            filename = pyi_os_path.os_path_join(pyi_os_path.os_path_join(SYS_PREFIX, fullname.replace('.', pyi_os_path.os_sep)), '__init__.pyc')
        else:
            filename = pyi_os_path.os_path_join(SYS_PREFIX, fullname.replace('.', pyi_os_path.os_sep) + '.pyc')
        return filename

    def find_spec--- This code section failed: ---

 L. 385         0  LOAD_CONST               None
                2  STORE_FAST               'entry_name'

 L. 387         4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                toc
               10  <118>                 0  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 388        14  LOAD_FAST                'fullname'
               16  STORE_FAST               'entry_name'

 L. 389        18  LOAD_GLOBAL              trace
               20  LOAD_STR                 'import %s # PyInstaller PYZ'
               22  LOAD_FAST                'fullname'
               24  CALL_FUNCTION_2       2  ''
               26  POP_TOP          
               28  JUMP_FORWARD        168  'to 168'
             30_0  COME_FROM            12  '12'

 L. 390        30  LOAD_FAST                'path'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   168  'to 168'

 L. 395        38  LOAD_FAST                'fullname'
               40  LOAD_METHOD              rsplit
               42  LOAD_STR                 '.'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'modname'

 L. 397        52  LOAD_FAST                'path'
               54  GET_ITER         
             56_0  COME_FROM           162  '162'
             56_1  COME_FROM           142  '142'
             56_2  COME_FROM            92  '92'
               56  FOR_ITER            164  'to 164'
               58  STORE_FAST               'p'

 L. 398        60  LOAD_FAST                'p'
               62  LOAD_GLOBAL              SYS_PREFIXLEN
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  STORE_FAST               'p'

 L. 399        76  LOAD_FAST                'p'
               78  LOAD_METHOD              split
               80  LOAD_GLOBAL              pyi_os_path
               82  LOAD_ATTR                os_sep
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'parts'

 L. 400        88  LOAD_FAST                'parts'
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  JUMP_BACK            56  'to 56'
             94_0  COME_FROM            90  '90'

 L. 401        94  LOAD_FAST                'parts'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  POP_JUMP_IF_TRUE    114  'to 114'

 L. 402       102  LOAD_FAST                'parts'
              104  LOAD_CONST               1
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  STORE_FAST               'parts'
            114_0  COME_FROM           100  '100'

 L. 403       114  LOAD_FAST                'parts'
              116  LOAD_METHOD              append
              118  LOAD_FAST                'modname'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 404       124  LOAD_STR                 '.'
              126  LOAD_METHOD              join
              128  LOAD_FAST                'parts'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'entry_name'

 L. 405       134  LOAD_FAST                'entry_name'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                toc
              140  <118>                 0  ''
              142  POP_JUMP_IF_FALSE_BACK    56  'to 56'

 L. 406       144  LOAD_GLOBAL              trace
              146  LOAD_STR                 'import %s as %s # PyInstaller PYZ (__path__ override: %s)'

 L. 407       148  LOAD_FAST                'entry_name'
              150  LOAD_FAST                'fullname'
              152  LOAD_FAST                'p'

 L. 406       154  CALL_FUNCTION_4       4  ''
              156  POP_TOP          

 L. 408       158  POP_TOP          
              160  BREAK_LOOP          168  'to 168'
              162  JUMP_BACK            56  'to 56'
            164_0  COME_FROM            56  '56'

 L. 410       164  LOAD_CONST               None
              166  STORE_FAST               'entry_name'
            168_0  COME_FROM           160  '160'
            168_1  COME_FROM            36  '36'
            168_2  COME_FROM            28  '28'

 L. 412       168  LOAD_FAST                'entry_name'
              170  LOAD_CONST               None
              172  <117>                 0  ''
              174  POP_JUMP_IF_FALSE   190  'to 190'

 L. 413       176  LOAD_GLOBAL              trace
              178  LOAD_STR                 '# %s not found in PYZ'
              180  LOAD_FAST                'fullname'
              182  CALL_FUNCTION_2       2  ''
              184  POP_TOP          

 L. 414       186  LOAD_CONST               None
              188  RETURN_VALUE     
            190_0  COME_FROM           174  '174'

 L. 417       190  LOAD_FAST                'self'
              192  LOAD_METHOD              get_filename
              194  LOAD_FAST                'entry_name'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'origin'

 L. 418       200  LOAD_FAST                'self'
              202  LOAD_METHOD              is_package
              204  LOAD_FAST                'entry_name'
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'is_pkg'

 L. 420       210  LOAD_GLOBAL              _frozen_importlib
              212  LOAD_ATTR                ModuleSpec

 L. 421       214  LOAD_FAST                'fullname'
              216  LOAD_FAST                'self'

 L. 422       218  LOAD_FAST                'is_pkg'
              220  LOAD_FAST                'origin'

 L. 424       222  LOAD_FAST                'entry_name'

 L. 420       224  LOAD_CONST               ('is_package', 'origin', 'loader_state')
              226  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              228  STORE_FAST               'spec'

 L. 432       230  LOAD_CONST               True
              232  LOAD_FAST                'spec'
              234  STORE_ATTR               has_location

 L. 433       236  LOAD_FAST                'spec'
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 10

    def create_module(self, spec):
        """
        PEP-451 loader.create_module() method for the ``sys.meta_path`` hook.

        Loaders may also implement create_module() that will return a new
        module to exec. It may return None to indicate that the default module
        creation code should be used. One use case, though atypical, for
        create_module() is to provide a module that is a subclass of the
        builtin module type. Most loaders will not need to implement
        create_module(),

        create_module() should properly handle the case where it is called
        more than once for the same spec/module. This may include returning
        None or raising ImportError.
        """
        pass

    def exec_module--- This code section failed: ---

 L. 472         0  LOAD_FAST                'module'
                2  LOAD_ATTR                __spec__
                4  STORE_FAST               'spec'

 L. 473         6  LOAD_FAST                'self'
                8  LOAD_METHOD              get_code
               10  LOAD_FAST                'spec'
               12  LOAD_ATTR                loader_state
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'bytecode'

 L. 476        18  LOAD_GLOBAL              hasattr
               20  LOAD_FAST                'module'
               22  LOAD_STR                 '__file__'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     32  'to 32'
               28  <74>             
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'

 L. 480        32  LOAD_FAST                'spec'
               34  LOAD_ATTR                submodule_search_locations
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L. 491        42  LOAD_GLOBAL              pyi_os_path
               44  LOAD_METHOD              os_path_dirname
               46  LOAD_FAST                'module'
               48  LOAD_ATTR                __file__
               50  CALL_METHOD_1         1  ''
               52  BUILD_LIST_1          1 
               54  LOAD_FAST                'module'
               56  STORE_ATTR               __path__
             58_0  COME_FROM            40  '40'

 L. 493        58  LOAD_GLOBAL              exec
               60  LOAD_FAST                'bytecode'
               62  LOAD_FAST                'module'
               64  LOAD_ATTR                __dict__
               66  CALL_FUNCTION_2       2  ''
               68  POP_TOP          

Parse error at or near `<74>' instruction at offset 28


def install--- This code section failed: ---

 L. 514         0  LOAD_GLOBAL              FrozenImporter
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'fimp'

 L. 515         6  LOAD_GLOBAL              sys
                8  LOAD_ATTR                meta_path
               10  LOAD_METHOD              append
               12  LOAD_FAST                'fimp'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 521        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                meta_path
               22  GET_ITER         
             24_0  COME_FROM            64  '64'
             24_1  COME_FROM            46  '46'
             24_2  COME_FROM            36  '36'
               24  FOR_ITER             66  'to 66'
               26  STORE_FAST               'item'

 L. 522        28  LOAD_GLOBAL              hasattr
               30  LOAD_FAST                'item'
               32  LOAD_STR                 '__name__'
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE_BACK    24  'to 24'
               38  LOAD_FAST                'item'
               40  LOAD_ATTR                __name__
               42  LOAD_STR                 'WindowsRegistryFinder'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 523        48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                meta_path
               52  LOAD_METHOD              remove
               54  LOAD_FAST                'item'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 524        60  POP_TOP          
               62  BREAK_LOOP           66  'to 66'
               64  JUMP_BACK            24  'to 24'
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            24  '24'

 L. 532        66  BUILD_LIST_0          0 
               68  STORE_FAST               'pathFinders'

 L. 533        70  LOAD_GLOBAL              reversed
               72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                meta_path
               76  CALL_FUNCTION_1       1  ''
               78  GET_ITER         
             80_0  COME_FROM           130  '130'
             80_1  COME_FROM           118  '118'
             80_2  COME_FROM            98  '98'
               80  FOR_ITER            132  'to 132'
               82  STORE_FAST               'item'

 L. 534        84  LOAD_GLOBAL              getattr
               86  LOAD_FAST                'item'
               88  LOAD_STR                 '__name__'
               90  LOAD_CONST               None
               92  CALL_FUNCTION_3       3  ''
               94  LOAD_STR                 'PathFinder'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE_BACK    80  'to 80'

 L. 535       100  LOAD_GLOBAL              sys
              102  LOAD_ATTR                meta_path
              104  LOAD_METHOD              remove
              106  LOAD_FAST                'item'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 536       112  LOAD_FAST                'item'
              114  LOAD_FAST                'pathFinders'
              116  <118>                 1  ''
              118  POP_JUMP_IF_FALSE_BACK    80  'to 80'

 L. 537       120  LOAD_FAST                'pathFinders'
              122  LOAD_METHOD              append
              124  LOAD_FAST                'item'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  JUMP_BACK            80  'to 80'
            132_0  COME_FROM            80  '80'

 L. 538       132  LOAD_GLOBAL              sys
              134  LOAD_ATTR                meta_path
              136  LOAD_METHOD              extend
              138  LOAD_GLOBAL              reversed
              140  LOAD_FAST                'pathFinders'
              142  CALL_FUNCTION_1       1  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

Parse error at or near `<118>' instruction at offset 116