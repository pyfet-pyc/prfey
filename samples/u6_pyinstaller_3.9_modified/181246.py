# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PyInstaller\loader\pyimod03_importers.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 25240 bytes
"""
PEP-302 and PEP-451 importers for frozen applications.
"""
import sys, _frozen_importlib, pyimod01_os_path as pyi_os_path
from pyimod02_archive import ArchiveReadError, ZlibArchiveReader
SYS_PREFIX = sys._MEIPASS + pyi_os_path.os_sep
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

 L. 124       114  LOAD_GLOBAL              ImportError
              116  LOAD_STR                 "Can't load frozen modules."
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `LOAD_CONST' instruction at offset 66

    def _is_pep420_namespace_package--- This code section failed: ---

 L. 128         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    78  'to 78'

 L. 129        10  SETUP_FINALLY        26  'to 26'

 L. 130        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _pyz_archive
               16  LOAD_METHOD              is_pep420_namespace_package
               18  LOAD_FAST                'fullname'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L. 131        26  DUP_TOP          
               28  LOAD_GLOBAL              Exception
               30  <121>                74  ''
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        66  'to 66'

 L. 132        40  LOAD_GLOBAL              ImportError

 L. 133        42  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               44  LOAD_FAST                'fullname'
               46  BINARY_ADD       

 L. 132        48  CALL_FUNCTION_1       1  ''

 L. 134        50  LOAD_FAST                'e'

 L. 132        52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  JUMP_ABSOLUTE        90  'to 90'
             66_0  COME_FROM_FINALLY    38  '38'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  <48>             
               74  <48>             
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM             8  '8'

 L. 136        78  LOAD_GLOBAL              ImportError

 L. 137        80  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               82  LOAD_FAST                'fullname'
               84  BINARY_ADD       

 L. 136        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            76  '76'

Parse error at or near `None' instruction at offset -1

    def find_module--- This code section failed: ---

 L. 153         0  LOAD_CONST               None
                2  STORE_FAST               'module_loader'

 L. 155         4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                toc
               10  <118>                 0  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 157        14  LOAD_FAST                'self'
               16  STORE_FAST               'module_loader'

 L. 158        18  LOAD_GLOBAL              trace
               20  LOAD_STR                 'import %s # PyInstaller PYZ'
               22  LOAD_FAST                'fullname'
               24  CALL_FUNCTION_2       2  ''
               26  POP_TOP          
               28  JUMP_FORWARD        182  'to 182'
             30_0  COME_FROM            12  '12'

 L. 159        30  LOAD_FAST                'path'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   182  'to 182'

 L. 164        38  LOAD_FAST                'fullname'
               40  LOAD_METHOD              split
               42  LOAD_STR                 '.'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'modname'

 L. 166        52  LOAD_FAST                'path'
               54  GET_ITER         
             56_0  COME_FROM           150  '150'
               56  FOR_ITER            182  'to 182'
               58  STORE_FAST               'p'

 L. 167        60  LOAD_FAST                'p'
               62  LOAD_METHOD              startswith
               64  LOAD_GLOBAL              SYS_PREFIX
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_TRUE     72  'to 72'

 L. 168        70  JUMP_BACK            56  'to 56'
             72_0  COME_FROM            68  '68'

 L. 169        72  LOAD_FAST                'p'
               74  LOAD_GLOBAL              SYS_PREFIXLEN
               76  LOAD_CONST               None
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'p'

 L. 170        84  LOAD_FAST                'p'
               86  LOAD_METHOD              split
               88  LOAD_GLOBAL              pyi_os_path
               90  LOAD_ATTR                os_sep
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'parts'

 L. 171        96  LOAD_FAST                'parts'
               98  POP_JUMP_IF_TRUE    102  'to 102'
              100  JUMP_BACK            56  'to 56'
            102_0  COME_FROM            98  '98'

 L. 172       102  LOAD_FAST                'parts'
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  POP_JUMP_IF_TRUE    122  'to 122'

 L. 173       110  LOAD_FAST                'parts'
              112  LOAD_CONST               1
              114  LOAD_CONST               None
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'parts'
            122_0  COME_FROM           108  '108'

 L. 174       122  LOAD_FAST                'parts'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'modname'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 175       132  LOAD_STR                 '.'
              134  LOAD_METHOD              join
              136  LOAD_FAST                'parts'
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'entry_name'

 L. 176       142  LOAD_FAST                'entry_name'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                toc
              148  <118>                 0  ''
              150  POP_JUMP_IF_FALSE    56  'to 56'

 L. 177       152  LOAD_GLOBAL              FrozenPackageImporter
              154  LOAD_FAST                'self'
              156  LOAD_FAST                'entry_name'
              158  CALL_FUNCTION_2       2  ''
              160  STORE_FAST               'module_loader'

 L. 178       162  LOAD_GLOBAL              trace
              164  LOAD_STR                 'import %s as %s # PyInstaller PYZ (__path__ override: %s)'

 L. 179       166  LOAD_FAST                'entry_name'
              168  LOAD_FAST                'fullname'
              170  LOAD_FAST                'p'

 L. 178       172  CALL_FUNCTION_4       4  ''
              174  POP_TOP          

 L. 180       176  POP_TOP          
              178  BREAK_LOOP          182  'to 182'
              180  JUMP_BACK            56  'to 56'
            182_0  COME_FROM            36  '36'
            182_1  COME_FROM            28  '28'

 L. 182       182  LOAD_FAST                'module_loader'
              184  LOAD_CONST               None
              186  <117>                 0  ''
              188  POP_JUMP_IF_FALSE   200  'to 200'

 L. 183       190  LOAD_GLOBAL              trace
              192  LOAD_STR                 '# %s not found in PYZ'
              194  LOAD_FAST                'fullname'
              196  CALL_FUNCTION_2       2  ''
              198  POP_TOP          
            200_0  COME_FROM           188  '188'

 L. 184       200  LOAD_FAST                'module_loader'
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 10

    def load_module--- This code section failed: ---

 L. 200         0  LOAD_CONST               None
                2  STORE_FAST               'module'

 L. 201         4  LOAD_FAST                'entry_name'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 202        12  LOAD_FAST                'fullname'
               14  STORE_FAST               'entry_name'
             16_0  COME_FROM            10  '10'

 L. 203        16  SETUP_FINALLY       184  'to 184'

 L. 206        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                modules
               22  LOAD_METHOD              get
               24  LOAD_FAST                'fullname'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'module'

 L. 209        30  LOAD_FAST                'module'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE   180  'to 180'

 L. 211        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _pyz_archive
               42  LOAD_METHOD              extract
               44  LOAD_FAST                'entry_name'
               46  CALL_METHOD_1         1  ''
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'is_pkg'
               52  STORE_FAST               'bytecode'

 L. 213        54  LOAD_GLOBAL              imp_new_module
               56  LOAD_FAST                'fullname'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'module'

 L. 221        62  LOAD_FAST                'self'
               64  LOAD_METHOD              get_filename
               66  LOAD_FAST                'entry_name'
               68  CALL_METHOD_1         1  ''
               70  LOAD_FAST                'module'
               72  STORE_ATTR               __file__

 L. 226        74  LOAD_FAST                'is_pkg'
               76  POP_JUMP_IF_FALSE    94  'to 94'

 L. 241        78  LOAD_GLOBAL              pyi_os_path
               80  LOAD_METHOD              os_path_dirname
               82  LOAD_FAST                'module'
               84  LOAD_ATTR                __file__
               86  CALL_METHOD_1         1  ''
               88  BUILD_LIST_1          1 
               90  LOAD_FAST                'module'
               92  STORE_ATTR               __path__
             94_0  COME_FROM            76  '76'

 L. 247        94  LOAD_FAST                'self'
               96  LOAD_FAST                'module'
               98  STORE_ATTR               __loader__

 L. 256       100  LOAD_FAST                'is_pkg'
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 257       104  LOAD_FAST                'fullname'
              106  LOAD_FAST                'module'
              108  STORE_ATTR               __package__
              110  JUMP_FORWARD        130  'to 130'
            112_0  COME_FROM           102  '102'

 L. 259       112  LOAD_FAST                'fullname'
              114  LOAD_METHOD              rsplit
              116  LOAD_STR                 '.'
              118  LOAD_CONST               1
              120  CALL_METHOD_2         2  ''
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'module'
              128  STORE_ATTR               __package__
            130_0  COME_FROM           110  '110'

 L. 264       130  LOAD_GLOBAL              _frozen_importlib
              132  LOAD_ATTR                ModuleSpec

 L. 265       134  LOAD_FAST                'entry_name'
              136  LOAD_FAST                'self'
              138  LOAD_FAST                'is_pkg'

 L. 264       140  LOAD_CONST               ('is_package',)
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  LOAD_FAST                'module'
              146  STORE_ATTR               __spec__

 L. 273       148  LOAD_FAST                'module'
              150  LOAD_GLOBAL              sys
              152  LOAD_ATTR                modules
              154  LOAD_FAST                'fullname'
              156  STORE_SUBSCR     

 L. 276       158  LOAD_GLOBAL              exec
              160  LOAD_FAST                'bytecode'
              162  LOAD_FAST                'module'
              164  LOAD_ATTR                __dict__
              166  CALL_FUNCTION_2       2  ''
              168  POP_TOP          

 L. 278       170  LOAD_GLOBAL              sys
              172  LOAD_ATTR                modules
              174  LOAD_FAST                'fullname'
              176  BINARY_SUBSCR    
              178  STORE_FAST               'module'
            180_0  COME_FROM            36  '36'
              180  POP_BLOCK        
              182  JUMP_FORWARD        226  'to 226'
            184_0  COME_FROM_FINALLY    16  '16'

 L. 280       184  DUP_TOP          
              186  LOAD_GLOBAL              Exception
              188  <121>               224  ''
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 282       196  LOAD_FAST                'fullname'
              198  LOAD_GLOBAL              sys
              200  LOAD_ATTR                modules
              202  <118>                 0  ''
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L. 283       206  LOAD_GLOBAL              sys
              208  LOAD_ATTR                modules
              210  LOAD_METHOD              pop
              212  LOAD_FAST                'fullname'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L. 288       218  RAISE_VARARGS_0       0  'reraise'
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           182  '182'

 L. 292       226  LOAD_FAST                'module'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8

    def is_package--- This code section failed: ---

 L. 297         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    78  'to 78'

 L. 298        10  SETUP_FINALLY        26  'to 26'

 L. 299        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _pyz_archive
               16  LOAD_METHOD              is_package
               18  LOAD_FAST                'fullname'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L. 300        26  DUP_TOP          
               28  LOAD_GLOBAL              Exception
               30  <121>                74  ''
               32  POP_TOP          
               34  STORE_FAST               'e'
               36  POP_TOP          
               38  SETUP_FINALLY        66  'to 66'

 L. 301        40  LOAD_GLOBAL              ImportError

 L. 302        42  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               44  LOAD_FAST                'fullname'
               46  BINARY_ADD       

 L. 301        48  CALL_FUNCTION_1       1  ''

 L. 303        50  LOAD_FAST                'e'

 L. 301        52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  JUMP_ABSOLUTE        90  'to 90'
             66_0  COME_FROM_FINALLY    38  '38'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  <48>             
               74  <48>             
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM             8  '8'

 L. 305        78  LOAD_GLOBAL              ImportError
               80  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               82  LOAD_FAST                'fullname'
               84  BINARY_ADD       
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            76  '76'

Parse error at or near `None' instruction at offset -1

    def get_code--- This code section failed: ---

 L. 313         0  SETUP_FINALLY        20  'to 20'

 L. 317         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pyz_archive
                6  LOAD_METHOD              extract
                8  LOAD_FAST                'fullname'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               1
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 318        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                68  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        60  'to 60'

 L. 319        34  LOAD_GLOBAL              ImportError

 L. 320        36  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               38  LOAD_FAST                'fullname'
               40  BINARY_ADD       

 L. 319        42  CALL_FUNCTION_1       1  ''

 L. 321        44  LOAD_FAST                'e'

 L. 319        46  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 330         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 331        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 334        14  LOAD_GLOBAL              ImportError
               16  LOAD_STR                 'No module named '
               18  LOAD_FAST                'fullname'
               20  BINARY_ADD       
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    def get_data--- This code section failed: ---

 L. 347         0  LOAD_FAST                'path'
                2  LOAD_METHOD              startswith
                4  LOAD_GLOBAL              SYS_PREFIX
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 348        14  LOAD_FAST                'path'
               16  LOAD_GLOBAL              SYS_PREFIXLEN
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'fullname'

 L. 349        26  LOAD_FAST                'fullname'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                toc
               32  <118>                 0  ''
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L. 351        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _pyz_archive
               40  LOAD_METHOD              extract
               42  LOAD_FAST                'fullname'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               1
               48  BINARY_SUBSCR    
               50  RETURN_VALUE     
             52_0  COME_FROM            34  '34'

 L. 356        52  LOAD_GLOBAL              open
               54  LOAD_FAST                'path'
               56  LOAD_STR                 'rb'
               58  CALL_FUNCTION_2       2  ''
               60  SETUP_WITH           86  'to 86'
               62  STORE_FAST               'fp'

 L. 357        64  LOAD_FAST                'fp'
               66  LOAD_METHOD              read
               68  CALL_METHOD_0         0  ''
               70  POP_BLOCK        
               72  ROT_TWO          
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  RETURN_VALUE     
             86_0  COME_FROM_WITH       60  '60'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          

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

 L. 400         0  LOAD_CONST               None
                2  STORE_FAST               'entry_name'

 L. 402         4  LOAD_FAST                'fullname'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                toc
               10  <118>                 0  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 403        14  LOAD_FAST                'fullname'
               16  STORE_FAST               'entry_name'

 L. 404        18  LOAD_GLOBAL              trace
               20  LOAD_STR                 'import %s # PyInstaller PYZ'
               22  LOAD_FAST                'fullname'
               24  CALL_FUNCTION_2       2  ''
               26  POP_TOP          
               28  JUMP_FORWARD        176  'to 176'
             30_0  COME_FROM            12  '12'

 L. 405        30  LOAD_FAST                'path'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   176  'to 176'

 L. 410        38  LOAD_FAST                'fullname'
               40  LOAD_METHOD              rsplit
               42  LOAD_STR                 '.'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  STORE_FAST               'modname'

 L. 412        52  LOAD_FAST                'path'
               54  GET_ITER         
             56_0  COME_FROM           150  '150'
               56  FOR_ITER            172  'to 172'
               58  STORE_FAST               'p'

 L. 413        60  LOAD_FAST                'p'
               62  LOAD_METHOD              startswith
               64  LOAD_GLOBAL              SYS_PREFIX
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_TRUE     72  'to 72'

 L. 414        70  JUMP_BACK            56  'to 56'
             72_0  COME_FROM            68  '68'

 L. 415        72  LOAD_FAST                'p'
               74  LOAD_GLOBAL              SYS_PREFIXLEN
               76  LOAD_CONST               None
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'p'

 L. 416        84  LOAD_FAST                'p'
               86  LOAD_METHOD              split
               88  LOAD_GLOBAL              pyi_os_path
               90  LOAD_ATTR                os_sep
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'parts'

 L. 417        96  LOAD_FAST                'parts'
               98  POP_JUMP_IF_TRUE    102  'to 102'
              100  JUMP_BACK            56  'to 56'
            102_0  COME_FROM            98  '98'

 L. 418       102  LOAD_FAST                'parts'
              104  LOAD_CONST               0
              106  BINARY_SUBSCR    
              108  POP_JUMP_IF_TRUE    122  'to 122'

 L. 419       110  LOAD_FAST                'parts'
              112  LOAD_CONST               1
              114  LOAD_CONST               None
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'parts'
            122_0  COME_FROM           108  '108'

 L. 420       122  LOAD_FAST                'parts'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'modname'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 421       132  LOAD_STR                 '.'
              134  LOAD_METHOD              join
              136  LOAD_FAST                'parts'
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'entry_name'

 L. 422       142  LOAD_FAST                'entry_name'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                toc
              148  <118>                 0  ''
              150  POP_JUMP_IF_FALSE    56  'to 56'

 L. 423       152  LOAD_GLOBAL              trace
              154  LOAD_STR                 'import %s as %s # PyInstaller PYZ (__path__ override: %s)'

 L. 424       156  LOAD_FAST                'entry_name'
              158  LOAD_FAST                'fullname'
              160  LOAD_FAST                'p'

 L. 423       162  CALL_FUNCTION_4       4  ''
              164  POP_TOP          

 L. 425       166  POP_TOP          
              168  BREAK_LOOP          176  'to 176'
              170  JUMP_BACK            56  'to 56'

 L. 427       172  LOAD_CONST               None
              174  STORE_FAST               'entry_name'
            176_0  COME_FROM            36  '36'
            176_1  COME_FROM            28  '28'

 L. 429       176  LOAD_FAST                'entry_name'
              178  LOAD_CONST               None
              180  <117>                 0  ''
              182  POP_JUMP_IF_FALSE   198  'to 198'

 L. 430       184  LOAD_GLOBAL              trace
              186  LOAD_STR                 '# %s not found in PYZ'
              188  LOAD_FAST                'fullname'
              190  CALL_FUNCTION_2       2  ''
              192  POP_TOP          

 L. 431       194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           182  '182'

 L. 433       198  LOAD_FAST                'self'
              200  LOAD_METHOD              _is_pep420_namespace_package
              202  LOAD_FAST                'entry_name'
              204  CALL_METHOD_1         1  ''
              206  POP_JUMP_IF_FALSE   248  'to 248'

 L. 436       208  LOAD_GLOBAL              _frozen_importlib
              210  LOAD_ATTR                ModuleSpec

 L. 437       212  LOAD_FAST                'fullname'
              214  LOAD_CONST               None

 L. 438       216  LOAD_CONST               True

 L. 436       218  LOAD_CONST               ('is_package',)
              220  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              222  STORE_FAST               'spec'

 L. 442       224  LOAD_GLOBAL              pyi_os_path
              226  LOAD_METHOD              os_path_dirname
              228  LOAD_FAST                'self'
              230  LOAD_METHOD              get_filename
              232  LOAD_FAST                'entry_name'
              234  CALL_METHOD_1         1  ''
              236  CALL_METHOD_1         1  ''

 L. 441       238  BUILD_LIST_1          1 
              240  LOAD_FAST                'spec'
              242  STORE_ATTR               submodule_search_locations

 L. 444       244  LOAD_FAST                'spec'
              246  RETURN_VALUE     
            248_0  COME_FROM           206  '206'

 L. 447       248  LOAD_FAST                'self'
              250  LOAD_METHOD              get_filename
              252  LOAD_FAST                'entry_name'
              254  CALL_METHOD_1         1  ''
              256  STORE_FAST               'origin'

 L. 448       258  LOAD_FAST                'self'
              260  LOAD_METHOD              is_package
              262  LOAD_FAST                'entry_name'
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'is_pkg'

 L. 450       268  LOAD_GLOBAL              _frozen_importlib
              270  LOAD_ATTR                ModuleSpec

 L. 451       272  LOAD_FAST                'fullname'
              274  LOAD_FAST                'self'

 L. 452       276  LOAD_FAST                'is_pkg'
              278  LOAD_FAST                'origin'

 L. 454       280  LOAD_FAST                'entry_name'

 L. 450       282  LOAD_CONST               ('is_package', 'origin', 'loader_state')
              284  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              286  STORE_FAST               'spec'

 L. 462       288  LOAD_CONST               True
              290  LOAD_FAST                'spec'
              292  STORE_ATTR               has_location

 L. 466       294  LOAD_FAST                'is_pkg'
          296_298  POP_JUMP_IF_FALSE   320  'to 320'

 L. 468       300  LOAD_GLOBAL              pyi_os_path
              302  LOAD_METHOD              os_path_dirname
              304  LOAD_FAST                'self'
              306  LOAD_METHOD              get_filename
              308  LOAD_FAST                'entry_name'
              310  CALL_METHOD_1         1  ''
              312  CALL_METHOD_1         1  ''

 L. 467       314  BUILD_LIST_1          1 
              316  LOAD_FAST                'spec'
              318  STORE_ATTR               submodule_search_locations
            320_0  COME_FROM           296  '296'

 L. 471       320  LOAD_FAST                'spec'
              322  RETURN_VALUE     
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

 L. 510         0  LOAD_FAST                'module'
                2  LOAD_ATTR                __spec__
                4  STORE_FAST               'spec'

 L. 511         6  LOAD_FAST                'self'
                8  LOAD_METHOD              get_code
               10  LOAD_FAST                'spec'
               12  LOAD_ATTR                loader_state
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'bytecode'

 L. 514        18  LOAD_GLOBAL              hasattr
               20  LOAD_FAST                'module'
               22  LOAD_STR                 '__file__'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     32  'to 32'
               28  <74>             
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            26  '26'

 L. 518        32  LOAD_FAST                'spec'
               34  LOAD_ATTR                submodule_search_locations
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L. 529        42  LOAD_GLOBAL              pyi_os_path
               44  LOAD_METHOD              os_path_dirname
               46  LOAD_FAST                'module'
               48  LOAD_ATTR                __file__
               50  CALL_METHOD_1         1  ''
               52  BUILD_LIST_1          1 
               54  LOAD_FAST                'module'
               56  STORE_ATTR               __path__
             58_0  COME_FROM            40  '40'

 L. 531        58  LOAD_GLOBAL              exec
               60  LOAD_FAST                'bytecode'
               62  LOAD_FAST                'module'
               64  LOAD_ATTR                __dict__
               66  CALL_FUNCTION_2       2  ''
               68  POP_TOP          

Parse error at or near `<74>' instruction at offset 28


def install--- This code section failed: ---

 L. 552         0  LOAD_GLOBAL              FrozenImporter
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'fimp'

 L. 553         6  LOAD_GLOBAL              sys
                8  LOAD_ATTR                meta_path
               10  LOAD_METHOD              append
               12  LOAD_FAST                'fimp'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 559        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                meta_path
               22  GET_ITER         
             24_0  COME_FROM            46  '46'
             24_1  COME_FROM            36  '36'
               24  FOR_ITER             66  'to 66'
               26  STORE_FAST               'item'

 L. 560        28  LOAD_GLOBAL              hasattr
               30  LOAD_FAST                'item'
               32  LOAD_STR                 '__name__'
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    24  'to 24'
               38  LOAD_FAST                'item'
               40  LOAD_ATTR                __name__
               42  LOAD_STR                 'WindowsRegistryFinder'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    24  'to 24'

 L. 561        48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                meta_path
               52  LOAD_METHOD              remove
               54  LOAD_FAST                'item'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 562        60  POP_TOP          
               62  BREAK_LOOP           66  'to 66'
               64  JUMP_BACK            24  'to 24'

 L. 570        66  BUILD_LIST_0          0 
               68  STORE_FAST               'pathFinders'

 L. 571        70  LOAD_GLOBAL              reversed
               72  LOAD_GLOBAL              sys
               74  LOAD_ATTR                meta_path
               76  CALL_FUNCTION_1       1  ''
               78  GET_ITER         
             80_0  COME_FROM           118  '118'
             80_1  COME_FROM            98  '98'
               80  FOR_ITER            132  'to 132'
               82  STORE_FAST               'item'

 L. 572        84  LOAD_GLOBAL              getattr
               86  LOAD_FAST                'item'
               88  LOAD_STR                 '__name__'
               90  LOAD_CONST               None
               92  CALL_FUNCTION_3       3  ''
               94  LOAD_STR                 'PathFinder'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE    80  'to 80'

 L. 573       100  LOAD_GLOBAL              sys
              102  LOAD_ATTR                meta_path
              104  LOAD_METHOD              remove
              106  LOAD_FAST                'item'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 574       112  LOAD_FAST                'item'
              114  LOAD_FAST                'pathFinders'
              116  <118>                 1  ''
              118  POP_JUMP_IF_FALSE    80  'to 80'

 L. 575       120  LOAD_FAST                'pathFinders'
              122  LOAD_METHOD              append
              124  LOAD_FAST                'item'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  JUMP_BACK            80  'to 80'

 L. 576       132  LOAD_GLOBAL              sys
              134  LOAD_ATTR                meta_path
              136  LOAD_METHOD              extend
              138  LOAD_GLOBAL              reversed
              140  LOAD_FAST                'pathFinders'
              142  CALL_FUNCTION_1       1  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

Parse error at or near `<118>' instruction at offset 116