# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: zipimport.py
"""zipimport provides support for importing Python modules from Zip archives.

This module exports three objects:
- zipimporter: a class; its constructor takes a path to a Zip archive.
- ZipImportError: exception raised by zipimporter objects. It's a
  subclass of ImportError, so it can be caught as ImportError, too.
- _zip_directory_cache: a dict, mapping archive paths to zip directory
  info dicts, as used in zipimporter._files.

It is usually not needed to use the zipimport module explicitly; it is
used by the builtin import mechanism for sys.path items that are paths
to Zip archives.
"""
import _frozen_importlib_external as _bootstrap_external
from _frozen_importlib_external import _unpack_uint16, _unpack_uint32
import _frozen_importlib as _bootstrap, _imp, _io, marshal, sys, time
__all__ = [
 'ZipImportError', 'zipimporter']
path_sep = _bootstrap_external.path_sep
alt_path_sep = _bootstrap_external.path_separators[1:]

class ZipImportError(ImportError):
    pass


_zip_directory_cache = {}
_module_type = type(sys)
END_CENTRAL_DIR_SIZE = 22
STRING_END_ARCHIVE = b'PK\x05\x06'
MAX_COMMENT_LEN = 65535

class zipimporter:
    __doc__ = "zipimporter(archivepath) -> zipimporter object\n\n    Create a new zipimporter instance. 'archivepath' must be a path to\n    a zipfile, or to a specific path inside a zipfile. For example, it can be\n    '/tmp/myimport.zip', or '/tmp/myimport.zip/mydirectory', if mydirectory is a\n    valid directory inside the archive.\n\n    'ZipImportError is raised if 'archivepath' doesn't point to a valid Zip\n    archive.\n\n    The 'archive' attribute of zipimporter objects contains the name of the\n    zipfile targeted.\n    "

    def __init__--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     28  'to 28'

 L.  65        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              os
               16  STORE_FAST               'os'

 L.  66        18  LOAD_FAST                'os'
               20  LOAD_METHOD              fsdecode
               22  LOAD_FAST                'path'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'path'
             28_0  COME_FROM             8  '8'

 L.  67        28  LOAD_FAST                'path'
               30  POP_JUMP_IF_TRUE     44  'to 44'

 L.  68        32  LOAD_GLOBAL              ZipImportError
               34  LOAD_STR                 'archive path is empty'
               36  LOAD_FAST                'path'
               38  LOAD_CONST               ('path',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            30  '30'

 L.  69        44  LOAD_GLOBAL              alt_path_sep
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.  70        48  LOAD_FAST                'path'
               50  LOAD_METHOD              replace
               52  LOAD_GLOBAL              alt_path_sep
               54  LOAD_GLOBAL              path_sep
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'path'
             60_0  COME_FROM            46  '46'

 L.  72        60  BUILD_LIST_0          0 
               62  STORE_FAST               'prefix'
             64_0  COME_FROM           178  '178'
             64_1  COME_FROM           146  '146'

 L.  74        64  SETUP_FINALLY        80  'to 80'

 L.  75        66  LOAD_GLOBAL              _bootstrap_external
               68  LOAD_METHOD              _path_stat
               70  LOAD_FAST                'path'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'st'
               76  POP_BLOCK        
               78  JUMP_FORWARD        150  'to 150'
             80_0  COME_FROM_FINALLY    64  '64'

 L.  76        80  DUP_TOP          
               82  LOAD_GLOBAL              OSError
               84  LOAD_GLOBAL              ValueError
               86  BUILD_TUPLE_2         2 
               88  <121>               148  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.  79        96  LOAD_GLOBAL              _bootstrap_external
               98  LOAD_METHOD              _path_split
              100  LOAD_FAST                'path'
              102  CALL_METHOD_1         1  ''
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'dirname'
              108  STORE_FAST               'basename'

 L.  80       110  LOAD_FAST                'dirname'
              112  LOAD_FAST                'path'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   130  'to 130'

 L.  81       118  LOAD_GLOBAL              ZipImportError
              120  LOAD_STR                 'not a Zip file'
              122  LOAD_FAST                'path'
              124  LOAD_CONST               ('path',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           116  '116'

 L.  82       130  LOAD_FAST                'dirname'
              132  STORE_FAST               'path'

 L.  83       134  LOAD_FAST                'prefix'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'basename'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  POP_EXCEPT       
              146  JUMP_BACK            64  'to 64'
              148  <48>             
            150_0  COME_FROM            78  '78'

 L.  86       150  LOAD_FAST                'st'
              152  LOAD_ATTR                st_mode
              154  LOAD_CONST               61440
              156  BINARY_AND       
              158  LOAD_CONST               32768
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   180  'to 180'

 L.  88       164  LOAD_GLOBAL              ZipImportError
              166  LOAD_STR                 'not a Zip file'
              168  LOAD_FAST                'path'
              170  LOAD_CONST               ('path',)
              172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              174  RAISE_VARARGS_1       1  'exception instance'

 L.  89       176  JUMP_FORWARD        180  'to 180'
              178  JUMP_BACK            64  'to 64'
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           162  '162'

 L.  91       180  SETUP_FINALLY       194  'to 194'

 L.  92       182  LOAD_GLOBAL              _zip_directory_cache
              184  LOAD_FAST                'path'
              186  BINARY_SUBSCR    
              188  STORE_FAST               'files'
              190  POP_BLOCK        
              192  JUMP_FORWARD        228  'to 228'
            194_0  COME_FROM_FINALLY   180  '180'

 L.  93       194  DUP_TOP          
              196  LOAD_GLOBAL              KeyError
              198  <121>               226  ''
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L.  94       206  LOAD_GLOBAL              _read_directory
              208  LOAD_FAST                'path'
              210  CALL_FUNCTION_1       1  ''
              212  STORE_FAST               'files'

 L.  95       214  LOAD_FAST                'files'
              216  LOAD_GLOBAL              _zip_directory_cache
              218  LOAD_FAST                'path'
              220  STORE_SUBSCR     
              222  POP_EXCEPT       
              224  JUMP_FORWARD        228  'to 228'
              226  <48>             
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           192  '192'

 L.  96       228  LOAD_FAST                'files'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               _files

 L.  97       234  LOAD_FAST                'path'
              236  LOAD_FAST                'self'
              238  STORE_ATTR               archive

 L.  99       240  LOAD_GLOBAL              _bootstrap_external
              242  LOAD_ATTR                _path_join
              244  LOAD_FAST                'prefix'
              246  LOAD_CONST               None
              248  LOAD_CONST               None
              250  LOAD_CONST               -1
              252  BUILD_SLICE_3         3 
              254  BINARY_SUBSCR    
              256  CALL_FUNCTION_EX      0  'positional arguments only'
              258  LOAD_FAST                'self'
              260  STORE_ATTR               prefix

 L. 100       262  LOAD_FAST                'self'
              264  LOAD_ATTR                prefix
          266_268  POP_JUMP_IF_FALSE   284  'to 284'

 L. 101       270  LOAD_FAST                'self'
              272  DUP_TOP          
              274  LOAD_ATTR                prefix
              276  LOAD_GLOBAL              path_sep
              278  INPLACE_ADD      
              280  ROT_TWO          
              282  STORE_ATTR               prefix
            284_0  COME_FROM           266  '266'

Parse error at or near `<121>' instruction at offset 88

    def find_loader--- This code section failed: ---

 L. 119         0  LOAD_GLOBAL              _get_module_info
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'mi'

 L. 120        10  LOAD_FAST                'mi'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 122        18  LOAD_FAST                'self'
               20  BUILD_LIST_0          0 
               22  BUILD_TUPLE_2         2 
               24  RETURN_VALUE     
             26_0  COME_FROM            16  '16'

 L. 129        26  LOAD_GLOBAL              _get_module_path
               28  LOAD_FAST                'self'
               30  LOAD_FAST                'fullname'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'modpath'

 L. 130        36  LOAD_GLOBAL              _is_dir
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'modpath'
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    70  'to 70'

 L. 134        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                archive
               52  FORMAT_VALUE          0  ''
               54  LOAD_GLOBAL              path_sep
               56  FORMAT_VALUE          0  ''
               58  LOAD_FAST                'modpath'
               60  FORMAT_VALUE          0  ''
               62  BUILD_STRING_3        3 
               64  BUILD_LIST_1          1 
               66  BUILD_TUPLE_2         2 
               68  RETURN_VALUE     
             70_0  COME_FROM            44  '44'

 L. 136        70  LOAD_CONST               None
               72  BUILD_LIST_0          0 
               74  BUILD_TUPLE_2         2 
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def find_module(self, fullname, path=None):
        """find_module(fullname, path=None) -> self or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, or None if it wasn't.
        The optional 'path' argument is ignored -- it's there for compatibility
        with the importer protocol.
        """
        return self.find_loaderfullnamepath[0]

    def get_code(self, fullname):
        """get_code(fullname) -> code object.

        Return the code object for the specified module. Raise ZipImportError
        if the module couldn't be found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return code

    def get_data--- This code section failed: ---

 L. 169         0  LOAD_GLOBAL              alt_path_sep
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 170         4  LOAD_FAST                'pathname'
                6  LOAD_METHOD              replace
                8  LOAD_GLOBAL              alt_path_sep
               10  LOAD_GLOBAL              path_sep
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'pathname'
             16_0  COME_FROM             2  '2'

 L. 172        16  LOAD_FAST                'pathname'
               18  STORE_FAST               'key'

 L. 173        20  LOAD_FAST                'pathname'
               22  LOAD_METHOD              startswith
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                archive
               28  LOAD_GLOBAL              path_sep
               30  BINARY_ADD       
               32  CALL_METHOD_1         1  ''
               34  POP_JUMP_IF_FALSE    58  'to 58'

 L. 174        36  LOAD_FAST                'pathname'
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                archive
               44  LOAD_GLOBAL              path_sep
               46  BINARY_ADD       
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               None
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  STORE_FAST               'key'
             58_0  COME_FROM            34  '34'

 L. 176        58  SETUP_FINALLY        74  'to 74'

 L. 177        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _files
               64  LOAD_FAST                'key'
               66  BINARY_SUBSCR    
               68  STORE_FAST               'toc_entry'
               70  POP_BLOCK        
               72  JUMP_FORWARD        104  'to 104'
             74_0  COME_FROM_FINALLY    58  '58'

 L. 178        74  DUP_TOP          
               76  LOAD_GLOBAL              KeyError
               78  <121>               102  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 179        86  LOAD_GLOBAL              OSError
               88  LOAD_CONST               0
               90  LOAD_STR                 ''
               92  LOAD_FAST                'key'
               94  CALL_FUNCTION_3       3  ''
               96  RAISE_VARARGS_1       1  'exception instance'
               98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
              102  <48>             
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            72  '72'

 L. 180       104  LOAD_GLOBAL              _get_data
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                archive
              110  LOAD_FAST                'toc_entry'
              112  CALL_FUNCTION_2       2  ''
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 78

    def get_filename(self, fullname):
        """get_filename(fullname) -> filename string.

        Return the filename for the specified module.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return modpath

    def get_source--- This code section failed: ---

 L. 202         0  LOAD_GLOBAL              _get_module_info
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'mi'

 L. 203        10  LOAD_FAST                'mi'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L. 204        18  LOAD_GLOBAL              ZipImportError
               20  LOAD_STR                 "can't find module "
               22  LOAD_FAST                'fullname'
               24  FORMAT_VALUE          2  '!r'
               26  BUILD_STRING_2        2 
               28  LOAD_FAST                'fullname'
               30  LOAD_CONST               ('name',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            16  '16'

 L. 206        36  LOAD_GLOBAL              _get_module_path
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'fullname'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'path'

 L. 207        46  LOAD_FAST                'mi'
               48  POP_JUMP_IF_FALSE    64  'to 64'

 L. 208        50  LOAD_GLOBAL              _bootstrap_external
               52  LOAD_METHOD              _path_join
               54  LOAD_FAST                'path'
               56  LOAD_STR                 '__init__.py'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'fullpath'
               62  JUMP_FORWARD         74  'to 74'
             64_0  COME_FROM            48  '48'

 L. 210        64  LOAD_FAST                'path'
               66  FORMAT_VALUE          0  ''
               68  LOAD_STR                 '.py'
               70  BUILD_STRING_2        2 
               72  STORE_FAST               'fullpath'
             74_0  COME_FROM            62  '62'

 L. 212        74  SETUP_FINALLY        90  'to 90'

 L. 213        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _files
               80  LOAD_FAST                'fullpath'
               82  BINARY_SUBSCR    
               84  STORE_FAST               'toc_entry'
               86  POP_BLOCK        
               88  JUMP_FORWARD        110  'to 110'
             90_0  COME_FROM_FINALLY    74  '74'

 L. 214        90  DUP_TOP          
               92  LOAD_GLOBAL              KeyError
               94  <121>               108  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 216       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
              108  <48>             
            110_0  COME_FROM            88  '88'

 L. 217       110  LOAD_GLOBAL              _get_data
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                archive
              116  LOAD_FAST                'toc_entry'
              118  CALL_FUNCTION_2       2  ''
              120  LOAD_METHOD              decode
              122  CALL_METHOD_0         0  ''
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def is_package--- This code section failed: ---

 L. 227         0  LOAD_GLOBAL              _get_module_info
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'mi'

 L. 228        10  LOAD_FAST                'mi'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L. 229        18  LOAD_GLOBAL              ZipImportError
               20  LOAD_STR                 "can't find module "
               22  LOAD_FAST                'fullname'
               24  FORMAT_VALUE          2  '!r'
               26  BUILD_STRING_2        2 
               28  LOAD_FAST                'fullname'
               30  LOAD_CONST               ('name',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            16  '16'

 L. 230        36  LOAD_FAST                'mi'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def load_module--- This code section failed: ---

 L. 241         0  LOAD_GLOBAL              _get_module_code
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'code'
               12  STORE_FAST               'ispackage'
               14  STORE_FAST               'modpath'

 L. 242        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_METHOD              get
               22  LOAD_FAST                'fullname'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'mod'

 L. 243        28  LOAD_FAST                'mod'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_TRUE     46  'to 46'
               36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'mod'
               40  LOAD_GLOBAL              _module_type
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_TRUE     64  'to 64'
             46_0  COME_FROM            34  '34'

 L. 244        46  LOAD_GLOBAL              _module_type
               48  LOAD_FAST                'fullname'
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'mod'

 L. 245        54  LOAD_FAST                'mod'
               56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                modules
               60  LOAD_FAST                'fullname'
               62  STORE_SUBSCR     
             64_0  COME_FROM            44  '44'

 L. 246        64  LOAD_FAST                'self'
               66  LOAD_FAST                'mod'
               68  STORE_ATTR               __loader__

 L. 248        70  SETUP_FINALLY       156  'to 156'

 L. 249        72  LOAD_FAST                'ispackage'
               74  POP_JUMP_IF_FALSE   108  'to 108'

 L. 252        76  LOAD_GLOBAL              _get_module_path
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'fullname'
               82  CALL_FUNCTION_2       2  ''
               84  STORE_FAST               'path'

 L. 253        86  LOAD_GLOBAL              _bootstrap_external
               88  LOAD_METHOD              _path_join
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                archive
               94  LOAD_FAST                'path'
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'fullpath'

 L. 254       100  LOAD_FAST                'fullpath'
              102  BUILD_LIST_1          1 
              104  LOAD_FAST                'mod'
              106  STORE_ATTR               __path__
            108_0  COME_FROM            74  '74'

 L. 256       108  LOAD_GLOBAL              hasattr
              110  LOAD_FAST                'mod'
              112  LOAD_STR                 '__builtins__'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_TRUE    124  'to 124'

 L. 257       118  LOAD_GLOBAL              __builtins__
              120  LOAD_FAST                'mod'
              122  STORE_ATTR               __builtins__
            124_0  COME_FROM           116  '116'

 L. 258       124  LOAD_GLOBAL              _bootstrap_external
              126  LOAD_METHOD              _fix_up_module
              128  LOAD_FAST                'mod'
              130  LOAD_ATTR                __dict__
              132  LOAD_FAST                'fullname'
              134  LOAD_FAST                'modpath'
              136  CALL_METHOD_3         3  ''
              138  POP_TOP          

 L. 259       140  LOAD_GLOBAL              exec
              142  LOAD_FAST                'code'
              144  LOAD_FAST                'mod'
              146  LOAD_ATTR                __dict__
              148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          
              152  POP_BLOCK        
              154  JUMP_FORWARD        178  'to 178'
            156_0  COME_FROM_FINALLY    70  '70'

 L. 260       156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 261       162  LOAD_GLOBAL              sys
              164  LOAD_ATTR                modules
              166  LOAD_FAST                'fullname'
              168  DELETE_SUBSCR    

 L. 262       170  RAISE_VARARGS_0       0  'reraise'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
              176  <48>             
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           154  '154'

 L. 264       178  SETUP_FINALLY       194  'to 194'

 L. 265       180  LOAD_GLOBAL              sys
              182  LOAD_ATTR                modules
              184  LOAD_FAST                'fullname'
              186  BINARY_SUBSCR    
              188  STORE_FAST               'mod'
              190  POP_BLOCK        
              192  JUMP_FORWARD        228  'to 228'
            194_0  COME_FROM_FINALLY   178  '178'

 L. 266       194  DUP_TOP          
              196  LOAD_GLOBAL              KeyError
              198  <121>               226  ''
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 267       206  LOAD_GLOBAL              ImportError
              208  LOAD_STR                 'Loaded module '
              210  LOAD_FAST                'fullname'
              212  FORMAT_VALUE          2  '!r'
              214  LOAD_STR                 ' not found in sys.modules'
              216  BUILD_STRING_3        3 
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
              222  POP_EXCEPT       
              224  JUMP_FORWARD        228  'to 228'
              226  <48>             
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           192  '192'

 L. 268       228  LOAD_GLOBAL              _bootstrap
              230  LOAD_METHOD              _verbose_message
              232  LOAD_STR                 'import {} # loaded from Zip {}'
              234  LOAD_FAST                'fullname'
              236  LOAD_FAST                'modpath'
              238  CALL_METHOD_3         3  ''
              240  POP_TOP          

 L. 269       242  LOAD_FAST                'mod'
              244  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    def get_resource_reader--- This code section failed: ---

 L. 278         0  SETUP_FINALLY        22  'to 22'

 L. 279         2  LOAD_FAST                'self'
                4  LOAD_METHOD              is_package
                6  LOAD_FAST                'fullname'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     18  'to 18'

 L. 280        12  POP_BLOCK        
               14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            10  '10'
               18  POP_BLOCK        
               20  JUMP_FORWARD         42  'to 42'
             22_0  COME_FROM_FINALLY     0  '0'

 L. 281        22  DUP_TOP          
               24  LOAD_GLOBAL              ZipImportError
               26  <121>                40  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 282        34  POP_EXCEPT       
               36  LOAD_CONST               None
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            20  '20'

 L. 283        42  LOAD_GLOBAL              _ZipImportResourceReader
               44  LOAD_ATTR                _registered
               46  POP_JUMP_IF_TRUE     76  'to 76'

 L. 284        48  LOAD_CONST               0
               50  LOAD_CONST               ('ResourceReader',)
               52  IMPORT_NAME_ATTR         importlib.abc
               54  IMPORT_FROM              ResourceReader
               56  STORE_FAST               'ResourceReader'
               58  POP_TOP          

 L. 285        60  LOAD_FAST                'ResourceReader'
               62  LOAD_METHOD              register
               64  LOAD_GLOBAL              _ZipImportResourceReader
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 286        70  LOAD_CONST               True
               72  LOAD_GLOBAL              _ZipImportResourceReader
               74  STORE_ATTR               _registered
             76_0  COME_FROM            46  '46'

 L. 287        76  LOAD_GLOBAL              _ZipImportResourceReader
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'fullname'
               82  CALL_FUNCTION_2       2  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 14

    def __repr__(self):
        return f'<zipimporter object "{self.archive}{path_sep}{self.prefix}">'


_zip_searchorder = (
 (
  path_sep + '__init__.pyc', True, True),
 (
  path_sep + '__init__.py', False, True),
 ('.pyc', True, False),
 ('.py', False, False))

def _get_module_path(self, fullname):
    return self.prefix + fullname.rpartition'.'[2]


def _is_dir--- This code section failed: ---

 L. 316         0  LOAD_FAST                'path'
                2  LOAD_GLOBAL              path_sep
                4  BINARY_ADD       
                6  STORE_FAST               'dirpath'

 L. 318         8  LOAD_FAST                'dirpath'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _files
               14  <118>                 0  ''
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 14


def _get_module_info--- This code section failed: ---

 L. 322         0  LOAD_GLOBAL              _get_module_path
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'path'

 L. 323        10  LOAD_GLOBAL              _zip_searchorder
               12  GET_ITER         
             14_0  COME_FROM            50  '50'
             14_1  COME_FROM            40  '40'
               14  FOR_ITER             52  'to 52'
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'suffix'
               20  STORE_FAST               'isbytecode'
               22  STORE_FAST               'ispackage'

 L. 324        24  LOAD_FAST                'path'
               26  LOAD_FAST                'suffix'
               28  BINARY_ADD       
               30  STORE_FAST               'fullpath'

 L. 325        32  LOAD_FAST                'fullpath'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _files
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 326        42  LOAD_FAST                'ispackage'
               44  ROT_TWO          
               46  POP_TOP          
               48  RETURN_VALUE     
               50  JUMP_BACK            14  'to 14'
             52_0  COME_FROM            14  '14'

Parse error at or near `<118>' instruction at offset 38


def _read_directory--- This code section failed: ---

 L. 353         0  SETUP_FINALLY        16  'to 16'

 L. 354         2  LOAD_GLOBAL              _io
                4  LOAD_METHOD              open_code
                6  LOAD_FAST                'archive'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'fp'
               12  POP_BLOCK        
               14  JUMP_FORWARD         52  'to 52'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 355        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  <121>                50  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 356        28  LOAD_GLOBAL              ZipImportError
               30  LOAD_STR                 "can't open Zip file: "
               32  LOAD_FAST                'archive'
               34  FORMAT_VALUE          2  '!r'
               36  BUILD_STRING_2        2 
               38  LOAD_FAST                'archive'
               40  LOAD_CONST               ('path',)
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            14  '14'

 L. 358        52  LOAD_FAST                'fp'
            54_56  SETUP_WITH         1246  'to 1246'
               58  POP_TOP          

 L. 359        60  SETUP_FINALLY        98  'to 98'

 L. 360        62  LOAD_FAST                'fp'
               64  LOAD_METHOD              seek
               66  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE
               68  UNARY_NEGATIVE   
               70  LOAD_CONST               2
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

 L. 361        76  LOAD_FAST                'fp'
               78  LOAD_METHOD              tell
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'header_position'

 L. 362        84  LOAD_FAST                'fp'
               86  LOAD_METHOD              read
               88  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'buffer'
               94  POP_BLOCK        
               96  JUMP_FORWARD        134  'to 134'
             98_0  COME_FROM_FINALLY    60  '60'

 L. 363        98  DUP_TOP          
              100  LOAD_GLOBAL              OSError
              102  <121>               132  ''
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 364       110  LOAD_GLOBAL              ZipImportError
              112  LOAD_STR                 "can't read Zip file: "
              114  LOAD_FAST                'archive'
              116  FORMAT_VALUE          2  '!r'
              118  BUILD_STRING_2        2 
              120  LOAD_FAST                'archive'
              122  LOAD_CONST               ('path',)
              124  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              126  RAISE_VARARGS_1       1  'exception instance'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
              132  <48>             
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM            96  '96'

 L. 365       134  LOAD_GLOBAL              len
              136  LOAD_FAST                'buffer'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE
              142  COMPARE_OP               !=
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 366       146  LOAD_GLOBAL              ZipImportError
              148  LOAD_STR                 "can't read Zip file: "
              150  LOAD_FAST                'archive'
              152  FORMAT_VALUE          2  '!r'
              154  BUILD_STRING_2        2 
              156  LOAD_FAST                'archive'
              158  LOAD_CONST               ('path',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           144  '144'

 L. 367       164  LOAD_FAST                'buffer'
              166  LOAD_CONST               None
              168  LOAD_CONST               4
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  LOAD_GLOBAL              STRING_END_ARCHIVE
              176  COMPARE_OP               !=
          178_180  POP_JUMP_IF_FALSE   426  'to 426'

 L. 370       182  SETUP_FINALLY       208  'to 208'

 L. 371       184  LOAD_FAST                'fp'
              186  LOAD_METHOD              seek
              188  LOAD_CONST               0
              190  LOAD_CONST               2
              192  CALL_METHOD_2         2  ''
              194  POP_TOP          

 L. 372       196  LOAD_FAST                'fp'
              198  LOAD_METHOD              tell
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'file_size'
              204  POP_BLOCK        
              206  JUMP_FORWARD        244  'to 244'
            208_0  COME_FROM_FINALLY   182  '182'

 L. 373       208  DUP_TOP          
              210  LOAD_GLOBAL              OSError
              212  <121>               242  ''
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 374       220  LOAD_GLOBAL              ZipImportError
              222  LOAD_STR                 "can't read Zip file: "
              224  LOAD_FAST                'archive'
              226  FORMAT_VALUE          2  '!r'
              228  BUILD_STRING_2        2 

 L. 375       230  LOAD_FAST                'archive'

 L. 374       232  LOAD_CONST               ('path',)
              234  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              236  RAISE_VARARGS_1       1  'exception instance'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
              242  <48>             
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           206  '206'

 L. 376       244  LOAD_GLOBAL              max
              246  LOAD_FAST                'file_size'
              248  LOAD_GLOBAL              MAX_COMMENT_LEN
              250  BINARY_SUBTRACT  

 L. 377       252  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE

 L. 376       254  BINARY_SUBTRACT  

 L. 377       256  LOAD_CONST               0

 L. 376       258  CALL_FUNCTION_2       2  ''
              260  STORE_FAST               'max_comment_start'

 L. 378       262  SETUP_FINALLY       286  'to 286'

 L. 379       264  LOAD_FAST                'fp'
              266  LOAD_METHOD              seek
              268  LOAD_FAST                'max_comment_start'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          

 L. 380       274  LOAD_FAST                'fp'
              276  LOAD_METHOD              read
              278  CALL_METHOD_0         0  ''
              280  STORE_FAST               'data'
              282  POP_BLOCK        
              284  JUMP_FORWARD        324  'to 324'
            286_0  COME_FROM_FINALLY   262  '262'

 L. 381       286  DUP_TOP          
              288  LOAD_GLOBAL              OSError
          290_292  <121>               322  ''
              294  POP_TOP          
              296  POP_TOP          
              298  POP_TOP          

 L. 382       300  LOAD_GLOBAL              ZipImportError
              302  LOAD_STR                 "can't read Zip file: "
              304  LOAD_FAST                'archive'
              306  FORMAT_VALUE          2  '!r'
              308  BUILD_STRING_2        2 

 L. 383       310  LOAD_FAST                'archive'

 L. 382       312  LOAD_CONST               ('path',)
              314  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              316  RAISE_VARARGS_1       1  'exception instance'
              318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
              322  <48>             
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           284  '284'

 L. 384       324  LOAD_FAST                'data'
              326  LOAD_METHOD              rfind
              328  LOAD_GLOBAL              STRING_END_ARCHIVE
              330  CALL_METHOD_1         1  ''
              332  STORE_FAST               'pos'

 L. 385       334  LOAD_FAST                'pos'
              336  LOAD_CONST               0
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_FALSE   362  'to 362'

 L. 386       344  LOAD_GLOBAL              ZipImportError
              346  LOAD_STR                 'not a Zip file: '
              348  LOAD_FAST                'archive'
              350  FORMAT_VALUE          2  '!r'
              352  BUILD_STRING_2        2 

 L. 387       354  LOAD_FAST                'archive'

 L. 386       356  LOAD_CONST               ('path',)
              358  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              360  RAISE_VARARGS_1       1  'exception instance'
            362_0  COME_FROM           340  '340'

 L. 388       362  LOAD_FAST                'data'
              364  LOAD_FAST                'pos'
              366  LOAD_FAST                'pos'
              368  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE
              370  BINARY_ADD       
              372  BUILD_SLICE_2         2 
              374  BINARY_SUBSCR    
              376  STORE_FAST               'buffer'

 L. 389       378  LOAD_GLOBAL              len
              380  LOAD_FAST                'buffer'
              382  CALL_FUNCTION_1       1  ''
              384  LOAD_GLOBAL              END_CENTRAL_DIR_SIZE
              386  COMPARE_OP               !=
          388_390  POP_JUMP_IF_FALSE   410  'to 410'

 L. 390       392  LOAD_GLOBAL              ZipImportError
              394  LOAD_STR                 'corrupt Zip file: '
              396  LOAD_FAST                'archive'
              398  FORMAT_VALUE          2  '!r'
              400  BUILD_STRING_2        2 

 L. 391       402  LOAD_FAST                'archive'

 L. 390       404  LOAD_CONST               ('path',)
              406  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              408  RAISE_VARARGS_1       1  'exception instance'
            410_0  COME_FROM           388  '388'

 L. 392       410  LOAD_FAST                'file_size'
              412  LOAD_GLOBAL              len
              414  LOAD_FAST                'data'
              416  CALL_FUNCTION_1       1  ''
              418  BINARY_SUBTRACT  
              420  LOAD_FAST                'pos'
              422  BINARY_ADD       
              424  STORE_FAST               'header_position'
            426_0  COME_FROM           178  '178'

 L. 394       426  LOAD_GLOBAL              _unpack_uint32
              428  LOAD_FAST                'buffer'
              430  LOAD_CONST               12
              432  LOAD_CONST               16
              434  BUILD_SLICE_2         2 
              436  BINARY_SUBSCR    
              438  CALL_FUNCTION_1       1  ''
              440  STORE_FAST               'header_size'

 L. 395       442  LOAD_GLOBAL              _unpack_uint32
              444  LOAD_FAST                'buffer'
              446  LOAD_CONST               16
              448  LOAD_CONST               20
              450  BUILD_SLICE_2         2 
              452  BINARY_SUBSCR    
              454  CALL_FUNCTION_1       1  ''
              456  STORE_FAST               'header_offset'

 L. 396       458  LOAD_FAST                'header_position'
              460  LOAD_FAST                'header_size'
              462  COMPARE_OP               <
          464_466  POP_JUMP_IF_FALSE   486  'to 486'

 L. 397       468  LOAD_GLOBAL              ZipImportError
              470  LOAD_STR                 'bad central directory size: '
              472  LOAD_FAST                'archive'
              474  FORMAT_VALUE          2  '!r'
              476  BUILD_STRING_2        2 
              478  LOAD_FAST                'archive'
              480  LOAD_CONST               ('path',)
              482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              484  RAISE_VARARGS_1       1  'exception instance'
            486_0  COME_FROM           464  '464'

 L. 398       486  LOAD_FAST                'header_position'
              488  LOAD_FAST                'header_offset'
              490  COMPARE_OP               <
          492_494  POP_JUMP_IF_FALSE   514  'to 514'

 L. 399       496  LOAD_GLOBAL              ZipImportError
              498  LOAD_STR                 'bad central directory offset: '
              500  LOAD_FAST                'archive'
              502  FORMAT_VALUE          2  '!r'
              504  BUILD_STRING_2        2 
              506  LOAD_FAST                'archive'
              508  LOAD_CONST               ('path',)
              510  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              512  RAISE_VARARGS_1       1  'exception instance'
            514_0  COME_FROM           492  '492'

 L. 400       514  LOAD_FAST                'header_position'
              516  LOAD_FAST                'header_size'
              518  INPLACE_SUBTRACT 
              520  STORE_FAST               'header_position'

 L. 401       522  LOAD_FAST                'header_position'
              524  LOAD_FAST                'header_offset'
              526  BINARY_SUBTRACT  
              528  STORE_FAST               'arc_offset'

 L. 402       530  LOAD_FAST                'arc_offset'
              532  LOAD_CONST               0
              534  COMPARE_OP               <
          536_538  POP_JUMP_IF_FALSE   558  'to 558'

 L. 403       540  LOAD_GLOBAL              ZipImportError
              542  LOAD_STR                 'bad central directory size or offset: '
              544  LOAD_FAST                'archive'
              546  FORMAT_VALUE          2  '!r'
              548  BUILD_STRING_2        2 
              550  LOAD_FAST                'archive'
              552  LOAD_CONST               ('path',)
              554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              556  RAISE_VARARGS_1       1  'exception instance'
            558_0  COME_FROM           536  '536'

 L. 405       558  BUILD_MAP_0           0 
              560  STORE_FAST               'files'

 L. 407       562  LOAD_CONST               0
              564  STORE_FAST               'count'

 L. 408       566  SETUP_FINALLY       582  'to 582'

 L. 409       568  LOAD_FAST                'fp'
              570  LOAD_METHOD              seek
              572  LOAD_FAST                'header_position'
              574  CALL_METHOD_1         1  ''
              576  POP_TOP          
              578  POP_BLOCK        
              580  JUMP_FORWARD        620  'to 620'
            582_0  COME_FROM_FINALLY   566  '566'

 L. 410       582  DUP_TOP          
              584  LOAD_GLOBAL              OSError
          586_588  <121>               618  ''
              590  POP_TOP          
              592  POP_TOP          
              594  POP_TOP          

 L. 411       596  LOAD_GLOBAL              ZipImportError
              598  LOAD_STR                 "can't read Zip file: "
              600  LOAD_FAST                'archive'
              602  FORMAT_VALUE          2  '!r'
              604  BUILD_STRING_2        2 
              606  LOAD_FAST                'archive'
              608  LOAD_CONST               ('path',)
              610  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              612  RAISE_VARARGS_1       1  'exception instance'
              614  POP_EXCEPT       
              616  JUMP_FORWARD        620  'to 620'
              618  <48>             
            620_0  COME_FROM          1228  '1228'
            620_1  COME_FROM           616  '616'
            620_2  COME_FROM           580  '580'

 L. 413       620  LOAD_FAST                'fp'
              622  LOAD_METHOD              read
              624  LOAD_CONST               46
              626  CALL_METHOD_1         1  ''
              628  STORE_FAST               'buffer'

 L. 414       630  LOAD_GLOBAL              len
              632  LOAD_FAST                'buffer'
              634  CALL_FUNCTION_1       1  ''
              636  LOAD_CONST               4
              638  COMPARE_OP               <
          640_642  POP_JUMP_IF_FALSE   652  'to 652'

 L. 415       644  LOAD_GLOBAL              EOFError
              646  LOAD_STR                 'EOF read where not expected'
              648  CALL_FUNCTION_1       1  ''
              650  RAISE_VARARGS_1       1  'exception instance'
            652_0  COME_FROM           640  '640'

 L. 417       652  LOAD_FAST                'buffer'
              654  LOAD_CONST               None
              656  LOAD_CONST               4
              658  BUILD_SLICE_2         2 
              660  BINARY_SUBSCR    
              662  LOAD_CONST               b'PK\x01\x02'
              664  COMPARE_OP               !=
          666_668  POP_JUMP_IF_FALSE   674  'to 674'

 L. 418   670_672  JUMP_FORWARD       1232  'to 1232'
            674_0  COME_FROM           666  '666'

 L. 419       674  LOAD_GLOBAL              len
              676  LOAD_FAST                'buffer'
              678  CALL_FUNCTION_1       1  ''
              680  LOAD_CONST               46
              682  COMPARE_OP               !=
          684_686  POP_JUMP_IF_FALSE   696  'to 696'

 L. 420       688  LOAD_GLOBAL              EOFError
              690  LOAD_STR                 'EOF read where not expected'
              692  CALL_FUNCTION_1       1  ''
              694  RAISE_VARARGS_1       1  'exception instance'
            696_0  COME_FROM           684  '684'

 L. 421       696  LOAD_GLOBAL              _unpack_uint16
              698  LOAD_FAST                'buffer'
              700  LOAD_CONST               8
              702  LOAD_CONST               10
              704  BUILD_SLICE_2         2 
              706  BINARY_SUBSCR    
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'flags'

 L. 422       712  LOAD_GLOBAL              _unpack_uint16
              714  LOAD_FAST                'buffer'
              716  LOAD_CONST               10
              718  LOAD_CONST               12
              720  BUILD_SLICE_2         2 
              722  BINARY_SUBSCR    
              724  CALL_FUNCTION_1       1  ''
              726  STORE_FAST               'compress'

 L. 423       728  LOAD_GLOBAL              _unpack_uint16
              730  LOAD_FAST                'buffer'
              732  LOAD_CONST               12
              734  LOAD_CONST               14
              736  BUILD_SLICE_2         2 
              738  BINARY_SUBSCR    
              740  CALL_FUNCTION_1       1  ''
              742  STORE_FAST               'time'

 L. 424       744  LOAD_GLOBAL              _unpack_uint16
              746  LOAD_FAST                'buffer'
              748  LOAD_CONST               14
              750  LOAD_CONST               16
              752  BUILD_SLICE_2         2 
              754  BINARY_SUBSCR    
              756  CALL_FUNCTION_1       1  ''
              758  STORE_FAST               'date'

 L. 425       760  LOAD_GLOBAL              _unpack_uint32
              762  LOAD_FAST                'buffer'
              764  LOAD_CONST               16
              766  LOAD_CONST               20
              768  BUILD_SLICE_2         2 
              770  BINARY_SUBSCR    
              772  CALL_FUNCTION_1       1  ''
              774  STORE_FAST               'crc'

 L. 426       776  LOAD_GLOBAL              _unpack_uint32
              778  LOAD_FAST                'buffer'
              780  LOAD_CONST               20
              782  LOAD_CONST               24
              784  BUILD_SLICE_2         2 
              786  BINARY_SUBSCR    
              788  CALL_FUNCTION_1       1  ''
              790  STORE_FAST               'data_size'

 L. 427       792  LOAD_GLOBAL              _unpack_uint32
              794  LOAD_FAST                'buffer'
              796  LOAD_CONST               24
              798  LOAD_CONST               28
              800  BUILD_SLICE_2         2 
              802  BINARY_SUBSCR    
              804  CALL_FUNCTION_1       1  ''
              806  STORE_FAST               'file_size'

 L. 428       808  LOAD_GLOBAL              _unpack_uint16
              810  LOAD_FAST                'buffer'
              812  LOAD_CONST               28
              814  LOAD_CONST               30
              816  BUILD_SLICE_2         2 
              818  BINARY_SUBSCR    
              820  CALL_FUNCTION_1       1  ''
              822  STORE_FAST               'name_size'

 L. 429       824  LOAD_GLOBAL              _unpack_uint16
              826  LOAD_FAST                'buffer'
              828  LOAD_CONST               30
              830  LOAD_CONST               32
              832  BUILD_SLICE_2         2 
              834  BINARY_SUBSCR    
              836  CALL_FUNCTION_1       1  ''
              838  STORE_FAST               'extra_size'

 L. 430       840  LOAD_GLOBAL              _unpack_uint16
              842  LOAD_FAST                'buffer'
              844  LOAD_CONST               32
              846  LOAD_CONST               34
              848  BUILD_SLICE_2         2 
              850  BINARY_SUBSCR    
              852  CALL_FUNCTION_1       1  ''
              854  STORE_FAST               'comment_size'

 L. 431       856  LOAD_GLOBAL              _unpack_uint32
              858  LOAD_FAST                'buffer'
              860  LOAD_CONST               42
              862  LOAD_CONST               46
              864  BUILD_SLICE_2         2 
              866  BINARY_SUBSCR    
              868  CALL_FUNCTION_1       1  ''
              870  STORE_FAST               'file_offset'

 L. 432       872  LOAD_FAST                'name_size'
              874  LOAD_FAST                'extra_size'
              876  BINARY_ADD       
              878  LOAD_FAST                'comment_size'
              880  BINARY_ADD       
              882  STORE_FAST               'header_size'

 L. 433       884  LOAD_FAST                'file_offset'
              886  LOAD_FAST                'header_offset'
              888  COMPARE_OP               >
          890_892  POP_JUMP_IF_FALSE   912  'to 912'

 L. 434       894  LOAD_GLOBAL              ZipImportError
              896  LOAD_STR                 'bad local header offset: '
              898  LOAD_FAST                'archive'
              900  FORMAT_VALUE          2  '!r'
              902  BUILD_STRING_2        2 
              904  LOAD_FAST                'archive'
              906  LOAD_CONST               ('path',)
              908  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              910  RAISE_VARARGS_1       1  'exception instance'
            912_0  COME_FROM           890  '890'

 L. 435       912  LOAD_FAST                'file_offset'
              914  LOAD_FAST                'arc_offset'
              916  INPLACE_ADD      
              918  STORE_FAST               'file_offset'

 L. 437       920  SETUP_FINALLY       936  'to 936'

 L. 438       922  LOAD_FAST                'fp'
              924  LOAD_METHOD              read
              926  LOAD_FAST                'name_size'
              928  CALL_METHOD_1         1  ''
              930  STORE_FAST               'name'
              932  POP_BLOCK        
              934  JUMP_FORWARD        974  'to 974'
            936_0  COME_FROM_FINALLY   920  '920'

 L. 439       936  DUP_TOP          
              938  LOAD_GLOBAL              OSError
          940_942  <121>               972  ''
              944  POP_TOP          
              946  POP_TOP          
              948  POP_TOP          

 L. 440       950  LOAD_GLOBAL              ZipImportError
              952  LOAD_STR                 "can't read Zip file: "
              954  LOAD_FAST                'archive'
              956  FORMAT_VALUE          2  '!r'
              958  BUILD_STRING_2        2 
              960  LOAD_FAST                'archive'
              962  LOAD_CONST               ('path',)
              964  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              966  RAISE_VARARGS_1       1  'exception instance'
              968  POP_EXCEPT       
              970  JUMP_FORWARD        974  'to 974'
              972  <48>             
            974_0  COME_FROM           970  '970'
            974_1  COME_FROM           934  '934'

 L. 441       974  LOAD_GLOBAL              len
              976  LOAD_FAST                'name'
              978  CALL_FUNCTION_1       1  ''
              980  LOAD_FAST                'name_size'
              982  COMPARE_OP               !=
          984_986  POP_JUMP_IF_FALSE  1006  'to 1006'

 L. 442       988  LOAD_GLOBAL              ZipImportError
              990  LOAD_STR                 "can't read Zip file: "
              992  LOAD_FAST                'archive'
              994  FORMAT_VALUE          2  '!r'
              996  BUILD_STRING_2        2 
              998  LOAD_FAST                'archive'
             1000  LOAD_CONST               ('path',)
             1002  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1004  RAISE_VARARGS_1       1  'exception instance'
           1006_0  COME_FROM           984  '984'

 L. 446      1006  SETUP_FINALLY      1058  'to 1058'

 L. 447      1008  LOAD_GLOBAL              len
             1010  LOAD_FAST                'fp'
             1012  LOAD_METHOD              read
             1014  LOAD_FAST                'header_size'
             1016  LOAD_FAST                'name_size'
             1018  BINARY_SUBTRACT  
             1020  CALL_METHOD_1         1  ''
             1022  CALL_FUNCTION_1       1  ''
             1024  LOAD_FAST                'header_size'
             1026  LOAD_FAST                'name_size'
             1028  BINARY_SUBTRACT  
             1030  COMPARE_OP               !=
         1032_1034  POP_JUMP_IF_FALSE  1054  'to 1054'

 L. 448      1036  LOAD_GLOBAL              ZipImportError
             1038  LOAD_STR                 "can't read Zip file: "
             1040  LOAD_FAST                'archive'
             1042  FORMAT_VALUE          2  '!r'
             1044  BUILD_STRING_2        2 
             1046  LOAD_FAST                'archive'
             1048  LOAD_CONST               ('path',)
             1050  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1052  RAISE_VARARGS_1       1  'exception instance'
           1054_0  COME_FROM          1032  '1032'
             1054  POP_BLOCK        
             1056  JUMP_FORWARD       1096  'to 1096'
           1058_0  COME_FROM_FINALLY  1006  '1006'

 L. 449      1058  DUP_TOP          
             1060  LOAD_GLOBAL              OSError
         1062_1064  <121>              1094  ''
             1066  POP_TOP          
             1068  POP_TOP          
             1070  POP_TOP          

 L. 450      1072  LOAD_GLOBAL              ZipImportError
             1074  LOAD_STR                 "can't read Zip file: "
             1076  LOAD_FAST                'archive'
             1078  FORMAT_VALUE          2  '!r'
             1080  BUILD_STRING_2        2 
             1082  LOAD_FAST                'archive'
             1084  LOAD_CONST               ('path',)
             1086  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1088  RAISE_VARARGS_1       1  'exception instance'
             1090  POP_EXCEPT       
             1092  JUMP_FORWARD       1096  'to 1096'
             1094  <48>             
           1096_0  COME_FROM          1092  '1092'
           1096_1  COME_FROM          1056  '1056'

 L. 452      1096  LOAD_FAST                'flags'
             1098  LOAD_CONST               2048
             1100  BINARY_AND       
         1102_1104  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 454      1106  LOAD_FAST                'name'
             1108  LOAD_METHOD              decode
             1110  CALL_METHOD_0         0  ''
             1112  STORE_FAST               'name'
             1114  JUMP_FORWARD       1168  'to 1168'
           1116_0  COME_FROM          1102  '1102'

 L. 457      1116  SETUP_FINALLY      1132  'to 1132'

 L. 458      1118  LOAD_FAST                'name'
             1120  LOAD_METHOD              decode
             1122  LOAD_STR                 'ascii'
             1124  CALL_METHOD_1         1  ''
             1126  STORE_FAST               'name'
             1128  POP_BLOCK        
             1130  JUMP_FORWARD       1168  'to 1168'
           1132_0  COME_FROM_FINALLY  1116  '1116'

 L. 459      1132  DUP_TOP          
             1134  LOAD_GLOBAL              UnicodeDecodeError
         1136_1138  <121>              1166  ''
             1140  POP_TOP          
             1142  POP_TOP          
             1144  POP_TOP          

 L. 460      1146  LOAD_FAST                'name'
             1148  LOAD_METHOD              decode
             1150  LOAD_STR                 'latin1'
             1152  CALL_METHOD_1         1  ''
             1154  LOAD_METHOD              translate
             1156  LOAD_GLOBAL              cp437_table
             1158  CALL_METHOD_1         1  ''
             1160  STORE_FAST               'name'
             1162  POP_EXCEPT       
             1164  JUMP_FORWARD       1168  'to 1168'
             1166  <48>             
           1168_0  COME_FROM          1164  '1164'
           1168_1  COME_FROM          1130  '1130'
           1168_2  COME_FROM          1114  '1114'

 L. 462      1168  LOAD_FAST                'name'
             1170  LOAD_METHOD              replace
             1172  LOAD_STR                 '/'
             1174  LOAD_GLOBAL              path_sep
             1176  CALL_METHOD_2         2  ''
             1178  STORE_FAST               'name'

 L. 463      1180  LOAD_GLOBAL              _bootstrap_external
             1182  LOAD_METHOD              _path_join
             1184  LOAD_FAST                'archive'
             1186  LOAD_FAST                'name'
             1188  CALL_METHOD_2         2  ''
             1190  STORE_FAST               'path'

 L. 464      1192  LOAD_FAST                'path'
             1194  LOAD_FAST                'compress'
             1196  LOAD_FAST                'data_size'
             1198  LOAD_FAST                'file_size'
             1200  LOAD_FAST                'file_offset'
             1202  LOAD_FAST                'time'
             1204  LOAD_FAST                'date'
             1206  LOAD_FAST                'crc'
             1208  BUILD_TUPLE_8         8 
             1210  STORE_FAST               't'

 L. 465      1212  LOAD_FAST                't'
             1214  LOAD_FAST                'files'
             1216  LOAD_FAST                'name'
             1218  STORE_SUBSCR     

 L. 466      1220  LOAD_FAST                'count'
             1222  LOAD_CONST               1
             1224  INPLACE_ADD      
             1226  STORE_FAST               'count'
         1228_1230  JUMP_BACK           620  'to 620'
           1232_0  COME_FROM           670  '670'
             1232  POP_BLOCK        
             1234  LOAD_CONST               None
             1236  DUP_TOP          
             1238  DUP_TOP          
             1240  CALL_FUNCTION_3       3  ''
             1242  POP_TOP          
             1244  JUMP_FORWARD       1264  'to 1264'
           1246_0  COME_FROM_WITH       54  '54'
             1246  <49>             
         1248_1250  POP_JUMP_IF_TRUE   1254  'to 1254'
             1252  <48>             
           1254_0  COME_FROM          1248  '1248'
             1254  POP_TOP          
             1256  POP_TOP          
             1258  POP_TOP          
             1260  POP_EXCEPT       
             1262  POP_TOP          
           1264_0  COME_FROM          1244  '1244'

 L. 467      1264  LOAD_GLOBAL              _bootstrap
             1266  LOAD_METHOD              _verbose_message
             1268  LOAD_STR                 'zipimport: found {} names in {!r}'
             1270  LOAD_FAST                'count'
             1272  LOAD_FAST                'archive'
             1274  CALL_METHOD_3         3  ''
             1276  POP_TOP          

 L. 468      1278  LOAD_FAST                'files'
             1280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20


cp437_table = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7fÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■\xa0'
_importing_zlib = False

def _get_decompress_func--- This code section failed: ---

 L. 512         0  LOAD_GLOBAL              _importing_zlib
                2  POP_JUMP_IF_FALSE    22  'to 22'

 L. 515         4  LOAD_GLOBAL              _bootstrap
                6  LOAD_METHOD              _verbose_message
                8  LOAD_STR                 'zipimport: zlib UNAVAILABLE'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L. 516        14  LOAD_GLOBAL              ZipImportError
               16  LOAD_STR                 "can't decompress data; zlib not available"
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             2  '2'

 L. 518        22  LOAD_CONST               True
               24  STORE_GLOBAL             _importing_zlib

 L. 519        26  SETUP_FINALLY        90  'to 90'
               28  SETUP_FINALLY        46  'to 46'

 L. 520        30  LOAD_CONST               0
               32  LOAD_CONST               ('decompress',)
               34  IMPORT_NAME              zlib
               36  IMPORT_FROM              decompress
               38  STORE_FAST               'decompress'
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_FORWARD         82  'to 82'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 521        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  <121>                80  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 522        58  LOAD_GLOBAL              _bootstrap
               60  LOAD_METHOD              _verbose_message
               62  LOAD_STR                 'zipimport: zlib UNAVAILABLE'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 523        68  LOAD_GLOBAL              ZipImportError
               70  LOAD_STR                 "can't decompress data; zlib not available"
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            44  '44'
               82  POP_BLOCK        

 L. 525        84  LOAD_CONST               False
               86  STORE_GLOBAL             _importing_zlib
               88  JUMP_FORWARD         96  'to 96'
             90_0  COME_FROM_FINALLY    26  '26'
               90  LOAD_CONST               False
               92  STORE_GLOBAL             _importing_zlib
               94  <48>             
             96_0  COME_FROM            88  '88'

 L. 527        96  LOAD_GLOBAL              _bootstrap
               98  LOAD_METHOD              _verbose_message
              100  LOAD_STR                 'zipimport: zlib available'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 528       106  LOAD_FAST                'decompress'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 50


def _get_data--- This code section failed: ---

 L. 532         0  LOAD_FAST                'toc_entry'
                2  UNPACK_SEQUENCE_8     8 
                4  STORE_FAST               'datapath'
                6  STORE_FAST               'compress'
                8  STORE_FAST               'data_size'
               10  STORE_FAST               'file_size'
               12  STORE_FAST               'file_offset'
               14  STORE_FAST               'time'
               16  STORE_FAST               'date'
               18  STORE_FAST               'crc'

 L. 533        20  LOAD_FAST                'data_size'
               22  LOAD_CONST               0
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 534        28  LOAD_GLOBAL              ZipImportError
               30  LOAD_STR                 'negative data size'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 536        36  LOAD_GLOBAL              _io
               38  LOAD_METHOD              open_code
               40  LOAD_FAST                'archive'
               42  CALL_METHOD_1         1  ''
            44_46  SETUP_WITH          318  'to 318'
               48  STORE_FAST               'fp'

 L. 538        50  SETUP_FINALLY        66  'to 66'

 L. 539        52  LOAD_FAST                'fp'
               54  LOAD_METHOD              seek
               56  LOAD_FAST                'file_offset'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  POP_BLOCK        
               64  JUMP_FORWARD        102  'to 102'
             66_0  COME_FROM_FINALLY    50  '50'

 L. 540        66  DUP_TOP          
               68  LOAD_GLOBAL              OSError
               70  <121>               100  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 541        78  LOAD_GLOBAL              ZipImportError
               80  LOAD_STR                 "can't read Zip file: "
               82  LOAD_FAST                'archive'
               84  FORMAT_VALUE          2  '!r'
               86  BUILD_STRING_2        2 
               88  LOAD_FAST                'archive'
               90  LOAD_CONST               ('path',)
               92  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               94  RAISE_VARARGS_1       1  'exception instance'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            64  '64'

 L. 542       102  LOAD_FAST                'fp'
              104  LOAD_METHOD              read
              106  LOAD_CONST               30
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'buffer'

 L. 543       112  LOAD_GLOBAL              len
              114  LOAD_FAST                'buffer'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_CONST               30
              120  COMPARE_OP               !=
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 544       124  LOAD_GLOBAL              EOFError
              126  LOAD_STR                 'EOF read where not expected'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'

 L. 546       132  LOAD_FAST                'buffer'
              134  LOAD_CONST               None
              136  LOAD_CONST               4
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  LOAD_CONST               b'PK\x03\x04'
              144  COMPARE_OP               !=
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 548       148  LOAD_GLOBAL              ZipImportError
              150  LOAD_STR                 'bad local file header: '
              152  LOAD_FAST                'archive'
              154  FORMAT_VALUE          2  '!r'
              156  BUILD_STRING_2        2 
              158  LOAD_FAST                'archive'
              160  LOAD_CONST               ('path',)
              162  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           146  '146'

 L. 550       166  LOAD_GLOBAL              _unpack_uint16
              168  LOAD_FAST                'buffer'
              170  LOAD_CONST               26
              172  LOAD_CONST               28
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'name_size'

 L. 551       182  LOAD_GLOBAL              _unpack_uint16
              184  LOAD_FAST                'buffer'
              186  LOAD_CONST               28
              188  LOAD_CONST               30
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'extra_size'

 L. 552       198  LOAD_CONST               30
              200  LOAD_FAST                'name_size'
              202  BINARY_ADD       
              204  LOAD_FAST                'extra_size'
              206  BINARY_ADD       
              208  STORE_FAST               'header_size'

 L. 553       210  LOAD_FAST                'file_offset'
              212  LOAD_FAST                'header_size'
              214  INPLACE_ADD      
              216  STORE_FAST               'file_offset'

 L. 554       218  SETUP_FINALLY       234  'to 234'

 L. 555       220  LOAD_FAST                'fp'
              222  LOAD_METHOD              seek
              224  LOAD_FAST                'file_offset'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          
              230  POP_BLOCK        
              232  JUMP_FORWARD        272  'to 272'
            234_0  COME_FROM_FINALLY   218  '218'

 L. 556       234  DUP_TOP          
              236  LOAD_GLOBAL              OSError
          238_240  <121>               270  ''
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 557       248  LOAD_GLOBAL              ZipImportError
              250  LOAD_STR                 "can't read Zip file: "
              252  LOAD_FAST                'archive'
              254  FORMAT_VALUE          2  '!r'
              256  BUILD_STRING_2        2 
              258  LOAD_FAST                'archive'
              260  LOAD_CONST               ('path',)
              262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              264  RAISE_VARARGS_1       1  'exception instance'
              266  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
              270  <48>             
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           232  '232'

 L. 558       272  LOAD_FAST                'fp'
              274  LOAD_METHOD              read
              276  LOAD_FAST                'data_size'
              278  CALL_METHOD_1         1  ''
              280  STORE_FAST               'raw_data'

 L. 559       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'raw_data'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_FAST                'data_size'
              290  COMPARE_OP               !=
          292_294  POP_JUMP_IF_FALSE   304  'to 304'

 L. 560       296  LOAD_GLOBAL              OSError
              298  LOAD_STR                 "zipimport: can't read data"
              300  CALL_FUNCTION_1       1  ''
              302  RAISE_VARARGS_1       1  'exception instance'
            304_0  COME_FROM           292  '292'
              304  POP_BLOCK        
              306  LOAD_CONST               None
              308  DUP_TOP          
              310  DUP_TOP          
              312  CALL_FUNCTION_3       3  ''
              314  POP_TOP          
              316  JUMP_FORWARD        336  'to 336'
            318_0  COME_FROM_WITH       44  '44'
              318  <49>             
          320_322  POP_JUMP_IF_TRUE    326  'to 326'
              324  <48>             
            326_0  COME_FROM           320  '320'
              326  POP_TOP          
              328  POP_TOP          
              330  POP_TOP          
              332  POP_EXCEPT       
              334  POP_TOP          
            336_0  COME_FROM           316  '316'

 L. 562       336  LOAD_FAST                'compress'
              338  LOAD_CONST               0
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   350  'to 350'

 L. 564       346  LOAD_FAST                'raw_data'
              348  RETURN_VALUE     
            350_0  COME_FROM           342  '342'

 L. 567       350  SETUP_FINALLY       362  'to 362'

 L. 568       352  LOAD_GLOBAL              _get_decompress_func
              354  CALL_FUNCTION_0       0  ''
              356  STORE_FAST               'decompress'
              358  POP_BLOCK        
              360  JUMP_FORWARD        390  'to 390'
            362_0  COME_FROM_FINALLY   350  '350'

 L. 569       362  DUP_TOP          
              364  LOAD_GLOBAL              Exception
          366_368  <121>               388  ''
              370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L. 570       376  LOAD_GLOBAL              ZipImportError
              378  LOAD_STR                 "can't decompress data; zlib not available"
              380  CALL_FUNCTION_1       1  ''
              382  RAISE_VARARGS_1       1  'exception instance'
              384  POP_EXCEPT       
              386  JUMP_FORWARD        390  'to 390'
              388  <48>             
            390_0  COME_FROM           386  '386'
            390_1  COME_FROM           360  '360'

 L. 571       390  LOAD_FAST                'decompress'
              392  LOAD_FAST                'raw_data'
              394  LOAD_CONST               -15
              396  CALL_FUNCTION_2       2  ''
              398  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 70


def _eq_mtime(t1, t2):
    return abs(t1 - t2) <= 1


def _unmarshal_code--- This code section failed: ---

 L. 589         0  LOAD_FAST                'fullname'

 L. 590         2  LOAD_FAST                'fullpath'

 L. 588         4  LOAD_CONST               ('name', 'path')
                6  BUILD_CONST_KEY_MAP_2     2 
                8  STORE_FAST               'exc_details'

 L. 593        10  SETUP_FINALLY        30  'to 30'

 L. 594        12  LOAD_GLOBAL              _bootstrap_external
               14  LOAD_METHOD              _classify_pyc
               16  LOAD_FAST                'data'
               18  LOAD_FAST                'fullname'
               20  LOAD_FAST                'exc_details'
               22  CALL_METHOD_3         3  ''
               24  STORE_FAST               'flags'
               26  POP_BLOCK        
               28  JUMP_FORWARD         50  'to 50'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 595        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  <121>                48  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 596        42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  RETURN_VALUE     
               48  <48>             
             50_0  COME_FROM            28  '28'

 L. 598        50  LOAD_FAST                'flags'
               52  LOAD_CONST               1
               54  BINARY_AND       
               56  LOAD_CONST               0
               58  COMPARE_OP               !=
               60  STORE_FAST               'hash_based'

 L. 599        62  LOAD_FAST                'hash_based'
               64  POP_JUMP_IF_FALSE   178  'to 178'

 L. 600        66  LOAD_FAST                'flags'
               68  LOAD_CONST               2
               70  BINARY_AND       
               72  LOAD_CONST               0
               74  COMPARE_OP               !=
               76  STORE_FAST               'check_source'

 L. 601        78  LOAD_GLOBAL              _imp
               80  LOAD_ATTR                check_hash_based_pycs
               82  LOAD_STR                 'never'
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   176  'to 176'

 L. 602        88  LOAD_FAST                'check_source'

 L. 601        90  POP_JUMP_IF_TRUE    102  'to 102'

 L. 602        92  LOAD_GLOBAL              _imp
               94  LOAD_ATTR                check_hash_based_pycs
               96  LOAD_STR                 'always'
               98  COMPARE_OP               ==

 L. 601       100  POP_JUMP_IF_FALSE   176  'to 176'
            102_0  COME_FROM            90  '90'

 L. 603       102  LOAD_GLOBAL              _get_pyc_source
              104  LOAD_FAST                'self'
              106  LOAD_FAST                'fullpath'
              108  CALL_FUNCTION_2       2  ''
              110  STORE_FAST               'source_bytes'

 L. 604       112  LOAD_FAST                'source_bytes'
              114  LOAD_CONST               None
              116  <117>                 1  ''
              118  POP_JUMP_IF_FALSE   176  'to 176'

 L. 605       120  LOAD_GLOBAL              _imp
              122  LOAD_METHOD              source_hash

 L. 606       124  LOAD_GLOBAL              _bootstrap_external
              126  LOAD_ATTR                _RAW_MAGIC_NUMBER

 L. 607       128  LOAD_FAST                'source_bytes'

 L. 605       130  CALL_METHOD_2         2  ''
              132  STORE_FAST               'source_hash'

 L. 610       134  SETUP_FINALLY       156  'to 156'

 L. 611       136  LOAD_GLOBAL              _bootstrap_external
              138  LOAD_METHOD              _validate_hash_pyc

 L. 612       140  LOAD_FAST                'data'
              142  LOAD_FAST                'source_hash'
              144  LOAD_FAST                'fullname'
              146  LOAD_FAST                'exc_details'

 L. 611       148  CALL_METHOD_4         4  ''
              150  POP_TOP          
              152  POP_BLOCK        
              154  JUMP_FORWARD        176  'to 176'
            156_0  COME_FROM_FINALLY   134  '134'

 L. 613       156  DUP_TOP          
              158  LOAD_GLOBAL              ImportError
              160  <121>               174  ''
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 614       168  POP_EXCEPT       
              170  LOAD_CONST               None
              172  RETURN_VALUE     
              174  <48>             
            176_0  COME_FROM           154  '154'
            176_1  COME_FROM           118  '118'
            176_2  COME_FROM           100  '100'
            176_3  COME_FROM            86  '86'
              176  JUMP_FORWARD        262  'to 262'
            178_0  COME_FROM            64  '64'

 L. 617       178  LOAD_GLOBAL              _get_mtime_and_size_of_source
              180  LOAD_FAST                'self'
              182  LOAD_FAST                'fullpath'
              184  CALL_FUNCTION_2       2  ''

 L. 616       186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'source_mtime'
              190  STORE_FAST               'source_size'

 L. 619       192  LOAD_FAST                'source_mtime'
          194_196  POP_JUMP_IF_FALSE   262  'to 262'

 L. 622       198  LOAD_GLOBAL              _eq_mtime
              200  LOAD_GLOBAL              _unpack_uint32
              202  LOAD_FAST                'data'
              204  LOAD_CONST               8
              206  LOAD_CONST               12
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_FAST                'source_mtime'
              216  CALL_FUNCTION_2       2  ''
              218  POP_JUMP_IF_FALSE   242  'to 242'

 L. 623       220  LOAD_GLOBAL              _unpack_uint32
              222  LOAD_FAST                'data'
              224  LOAD_CONST               12
              226  LOAD_CONST               16
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  CALL_FUNCTION_1       1  ''
              234  LOAD_FAST                'source_size'
              236  COMPARE_OP               !=

 L. 622   238_240  POP_JUMP_IF_FALSE   262  'to 262'
            242_0  COME_FROM           218  '218'

 L. 624       242  LOAD_GLOBAL              _bootstrap
              244  LOAD_METHOD              _verbose_message

 L. 625       246  LOAD_STR                 'bytecode is stale for '
              248  LOAD_FAST                'fullname'
              250  FORMAT_VALUE          2  '!r'
              252  BUILD_STRING_2        2 

 L. 624       254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L. 626       258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           238  '238'
            262_1  COME_FROM           194  '194'
            262_2  COME_FROM           176  '176'

 L. 628       262  LOAD_GLOBAL              marshal
              264  LOAD_METHOD              loads
              266  LOAD_FAST                'data'
              268  LOAD_CONST               16
              270  LOAD_CONST               None
              272  BUILD_SLICE_2         2 
              274  BINARY_SUBSCR    
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'code'

 L. 629       280  LOAD_GLOBAL              isinstance
              282  LOAD_FAST                'code'
              284  LOAD_GLOBAL              _code_type
              286  CALL_FUNCTION_2       2  ''
          288_290  POP_JUMP_IF_TRUE    308  'to 308'

 L. 630       292  LOAD_GLOBAL              TypeError
              294  LOAD_STR                 'compiled module '
              296  LOAD_FAST                'pathname'
              298  FORMAT_VALUE          2  '!r'
              300  LOAD_STR                 ' is not a code object'
              302  BUILD_STRING_3        3 
              304  CALL_FUNCTION_1       1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           288  '288'

 L. 631       308  LOAD_FAST                'code'
              310  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34


_code_type = type(_unmarshal_code.__code__)

def _normalize_line_endings(source):
    source = source.replaceb'\r\n'b'\n'
    source = source.replaceb'\r'b'\n'
    return source


def _compile_source(pathname, source):
    source = _normalize_line_endings(source)
    return compile(source, pathname, 'exec', dont_inherit=True)


def _parse_dostime(d, t):
    return time.mktime(
     (d >> 9) + 1980,
     d >> 5 & 15,
     d & 31,
     t >> 11,
     t >> 5 & 63,
     (t & 31) * 2,
     -1, -1, -1)


def _get_mtime_and_size_of_source--- This code section failed: ---

 L. 665         0  SETUP_FINALLY        84  'to 84'

 L. 667         2  LOAD_FAST                'path'
                4  LOAD_CONST               -1
                6  LOAD_CONST               None
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  LOAD_CONST               ('c', 'o')
               14  <118>                 0  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'

 L. 668        22  LOAD_FAST                'path'
               24  LOAD_CONST               None
               26  LOAD_CONST               -1
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  STORE_FAST               'path'

 L. 669        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _files
               38  LOAD_FAST                'path'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'toc_entry'

 L. 672        44  LOAD_FAST                'toc_entry'
               46  LOAD_CONST               5
               48  BINARY_SUBSCR    
               50  STORE_FAST               'time'

 L. 673        52  LOAD_FAST                'toc_entry'
               54  LOAD_CONST               6
               56  BINARY_SUBSCR    
               58  STORE_FAST               'date'

 L. 674        60  LOAD_FAST                'toc_entry'
               62  LOAD_CONST               3
               64  BINARY_SUBSCR    
               66  STORE_FAST               'uncompressed_size'

 L. 675        68  LOAD_GLOBAL              _parse_dostime
               70  LOAD_FAST                'date'
               72  LOAD_FAST                'time'
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_FAST                'uncompressed_size'
               78  BUILD_TUPLE_2         2 
               80  POP_BLOCK        
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY     0  '0'

 L. 676        84  DUP_TOP          
               86  LOAD_GLOBAL              KeyError
               88  LOAD_GLOBAL              IndexError
               90  LOAD_GLOBAL              TypeError
               92  BUILD_TUPLE_3         3 
               94  <121>               108  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 677       102  POP_EXCEPT       
              104  LOAD_CONST               (0, 0)
              106  RETURN_VALUE     
              108  <48>             

Parse error at or near `<118>' instruction at offset 14


def _get_pyc_source--- This code section failed: ---

 L. 685         0  LOAD_FAST                'path'
                2  LOAD_CONST               -1
                4  LOAD_CONST               None
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_CONST               ('c', 'o')
               12  <118>                 0  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 686        20  LOAD_FAST                'path'
               22  LOAD_CONST               None
               24  LOAD_CONST               -1
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  STORE_FAST               'path'

 L. 688        32  SETUP_FINALLY        48  'to 48'

 L. 689        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _files
               38  LOAD_FAST                'path'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'toc_entry'
               44  POP_BLOCK        
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM_FINALLY    32  '32'

 L. 690        48  DUP_TOP          
               50  LOAD_GLOBAL              KeyError
               52  <121>                66  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 691        60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  RETURN_VALUE     
               66  <48>             
             68_0  COME_FROM            46  '46'

 L. 693        68  LOAD_GLOBAL              _get_data
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                archive
               74  LOAD_FAST                'toc_entry'
               76  CALL_FUNCTION_2       2  ''
               78  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _get_module_code--- This code section failed: ---

 L. 699         0  LOAD_GLOBAL              _get_module_path
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'fullname'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'path'

 L. 700        10  LOAD_GLOBAL              _zip_searchorder
               12  GET_ITER         
             14_0  COME_FROM           172  '172'
             14_1  COME_FROM           148  '148'
             14_2  COME_FROM            84  '84'
               14  FOR_ITER            174  'to 174'
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'suffix'
               20  STORE_FAST               'isbytecode'
               22  STORE_FAST               'ispackage'

 L. 701        24  LOAD_FAST                'path'
               26  LOAD_FAST                'suffix'
               28  BINARY_ADD       
               30  STORE_FAST               'fullpath'

 L. 702        32  LOAD_GLOBAL              _bootstrap
               34  LOAD_ATTR                _verbose_message
               36  LOAD_STR                 'trying {}{}{}'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                archive
               42  LOAD_GLOBAL              path_sep
               44  LOAD_FAST                'fullpath'
               46  LOAD_CONST               2
               48  LOAD_CONST               ('verbosity',)
               50  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               52  POP_TOP          

 L. 703        54  SETUP_FINALLY        70  'to 70'

 L. 704        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _files
               60  LOAD_FAST                'fullpath'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'toc_entry'
               66  POP_BLOCK        
               68  JUMP_FORWARD         88  'to 88'
             70_0  COME_FROM_FINALLY    54  '54'

 L. 705        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  <121>                86  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 706        82  POP_EXCEPT       
               84  JUMP_BACK            14  'to 14'
               86  <48>             
             88_0  COME_FROM            68  '68'

 L. 708        88  LOAD_FAST                'toc_entry'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  STORE_FAST               'modpath'

 L. 709        96  LOAD_GLOBAL              _get_data
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                archive
              102  LOAD_FAST                'toc_entry'
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'data'

 L. 710       108  LOAD_FAST                'isbytecode'
              110  POP_JUMP_IF_FALSE   130  'to 130'

 L. 711       112  LOAD_GLOBAL              _unmarshal_code
              114  LOAD_FAST                'self'
              116  LOAD_FAST                'modpath'
              118  LOAD_FAST                'fullpath'
              120  LOAD_FAST                'fullname'
              122  LOAD_FAST                'data'
              124  CALL_FUNCTION_5       5  ''
              126  STORE_FAST               'code'
              128  JUMP_FORWARD        140  'to 140'
            130_0  COME_FROM           110  '110'

 L. 713       130  LOAD_GLOBAL              _compile_source
              132  LOAD_FAST                'modpath'
              134  LOAD_FAST                'data'
              136  CALL_FUNCTION_2       2  ''
              138  STORE_FAST               'code'
            140_0  COME_FROM           128  '128'

 L. 714       140  LOAD_FAST                'code'
              142  LOAD_CONST               None
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   150  'to 150'

 L. 717       148  JUMP_BACK            14  'to 14'
            150_0  COME_FROM           146  '146'

 L. 718       150  LOAD_FAST                'toc_entry'
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  STORE_FAST               'modpath'

 L. 719       158  LOAD_FAST                'code'
              160  LOAD_FAST                'ispackage'
              162  LOAD_FAST                'modpath'
              164  BUILD_TUPLE_3         3 
              166  ROT_TWO          
              168  POP_TOP          
              170  RETURN_VALUE     
              172  JUMP_BACK            14  'to 14'
            174_0  COME_FROM            14  '14'

 L. 721       174  LOAD_GLOBAL              ZipImportError
              176  LOAD_STR                 "can't find module "
              178  LOAD_FAST                'fullname'
              180  FORMAT_VALUE          2  '!r'
              182  BUILD_STRING_2        2 
              184  LOAD_FAST                'fullname'
              186  LOAD_CONST               ('name',)
              188  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              190  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 74


class _ZipImportResourceReader:
    __doc__ = 'Private class used to support ZipImport.get_resource_reader().\n\n    This class is allowed to reference all the innards and private parts of\n    the zipimporter.\n    '
    _registered = False

    def __init__(self, zipimporter, fullname):
        self.zipimporter = zipimporter
        self.fullname = fullname

    def open_resource--- This code section failed: ---

 L. 737         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fullname
                4  LOAD_METHOD              replace
                6  LOAD_STR                 '.'
                8  LOAD_STR                 '/'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'fullname_as_path'

 L. 738        14  LOAD_FAST                'fullname_as_path'
               16  FORMAT_VALUE          0  ''
               18  LOAD_STR                 '/'
               20  LOAD_FAST                'resource'
               22  FORMAT_VALUE          0  ''
               24  BUILD_STRING_3        3 
               26  STORE_FAST               'path'

 L. 739        28  LOAD_CONST               0
               30  LOAD_CONST               ('BytesIO',)
               32  IMPORT_NAME              io
               34  IMPORT_FROM              BytesIO
               36  STORE_FAST               'BytesIO'
               38  POP_TOP          

 L. 740        40  SETUP_FINALLY        60  'to 60'

 L. 741        42  LOAD_FAST                'BytesIO'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                zipimporter
               48  LOAD_METHOD              get_data
               50  LOAD_FAST                'path'
               52  CALL_METHOD_1         1  ''
               54  CALL_FUNCTION_1       1  ''
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    40  '40'

 L. 742        60  DUP_TOP          
               62  LOAD_GLOBAL              OSError
               64  <121>                84  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 743        72  LOAD_GLOBAL              FileNotFoundError
               74  LOAD_FAST                'path'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'

Parse error at or near `<121>' instruction at offset 64

    def resource_path(self, resource):
        raise FileNotFoundError

    def is_resource--- This code section failed: ---

 L. 754         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fullname
                4  LOAD_METHOD              replace
                6  LOAD_STR                 '.'
                8  LOAD_STR                 '/'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'fullname_as_path'

 L. 755        14  LOAD_FAST                'fullname_as_path'
               16  FORMAT_VALUE          0  ''
               18  LOAD_STR                 '/'
               20  LOAD_FAST                'name'
               22  FORMAT_VALUE          0  ''
               24  BUILD_STRING_3        3 
               26  STORE_FAST               'path'

 L. 756        28  SETUP_FINALLY        46  'to 46'

 L. 757        30  LOAD_FAST                'self'
               32  LOAD_ATTR                zipimporter
               34  LOAD_METHOD              get_data
               36  LOAD_FAST                'path'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_FORWARD         66  'to 66'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 758        46  DUP_TOP          
               48  LOAD_GLOBAL              OSError
               50  <121>                64  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 759        58  POP_EXCEPT       
               60  LOAD_CONST               False
               62  RETURN_VALUE     
               64  <48>             
             66_0  COME_FROM            44  '44'

 L. 760        66  LOAD_CONST               True
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 50

    def contents--- This code section failed: ---

 L. 770         0  LOAD_CONST               0
                2  LOAD_CONST               ('Path',)
                4  IMPORT_NAME              pathlib
                6  IMPORT_FROM              Path
                8  STORE_FAST               'Path'
               10  POP_TOP          

 L. 771        12  LOAD_FAST                'Path'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                zipimporter
               18  LOAD_METHOD              get_filename
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                fullname
               24  CALL_METHOD_1         1  ''
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'fullname_path'

 L. 772        30  LOAD_FAST                'fullname_path'
               32  LOAD_METHOD              relative_to
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                zipimporter
               38  LOAD_ATTR                archive
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'relative_path'

 L. 775        44  LOAD_FAST                'relative_path'
               46  LOAD_ATTR                name
               48  LOAD_STR                 '__init__.py'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     58  'to 58'
               54  <74>             
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'

 L. 776        58  LOAD_FAST                'relative_path'
               60  LOAD_ATTR                parent
               62  STORE_FAST               'package_path'

 L. 777        64  LOAD_GLOBAL              set
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'subdirs_seen'

 L. 778        70  LOAD_FAST                'self'
               72  LOAD_ATTR                zipimporter
               74  LOAD_ATTR                _files
               76  GET_ITER         
             78_0  COME_FROM           178  '178'
             78_1  COME_FROM           160  '160'
             78_2  COME_FROM           152  '152'
             78_3  COME_FROM           116  '116'
               78  FOR_ITER            180  'to 180'
               80  STORE_FAST               'filename'

 L. 779        82  SETUP_FINALLY       102  'to 102'

 L. 780        84  LOAD_FAST                'Path'
               86  LOAD_FAST                'filename'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_METHOD              relative_to
               92  LOAD_FAST                'package_path'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'relative'
               98  POP_BLOCK        
              100  JUMP_FORWARD        124  'to 124'
            102_0  COME_FROM_FINALLY    82  '82'

 L. 781       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  <121>               122  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 782       114  POP_EXCEPT       
              116  JUMP_BACK            78  'to 78'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           100  '100'

 L. 787       124  LOAD_FAST                'relative'
              126  LOAD_ATTR                parent
              128  LOAD_ATTR                name
              130  STORE_FAST               'parent_name'

 L. 788       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'parent_name'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_CONST               0
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   154  'to 154'

 L. 789       144  LOAD_FAST                'relative'
              146  LOAD_ATTR                name
              148  YIELD_VALUE      
              150  POP_TOP          
              152  JUMP_BACK            78  'to 78'
            154_0  COME_FROM           142  '142'

 L. 790       154  LOAD_FAST                'parent_name'
              156  LOAD_FAST                'subdirs_seen'
              158  <118>                 1  ''
              160  POP_JUMP_IF_FALSE_BACK    78  'to 78'

 L. 791       162  LOAD_FAST                'subdirs_seen'
              164  LOAD_METHOD              add
              166  LOAD_FAST                'parent_name'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 792       172  LOAD_FAST                'parent_name'
              174  YIELD_VALUE      
              176  POP_TOP          
              178  JUMP_BACK            78  'to 78'
            180_0  COME_FROM            78  '78'

Parse error at or near `<74>' instruction at offset 54


# global _importing_zlib ## Warning: Unused global