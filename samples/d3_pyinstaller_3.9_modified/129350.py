# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\client\_code_cache.py
"""comtypes.client._code_cache helper module.

The main function is _find_gen_dir(), which on-demand creates the
comtypes.gen package and returns a directory where generated code can
be written to.
"""
import ctypes, logging, os, sys, tempfile, types
logger = logging.getLogger(__name__)

def _ensure_list(path):
    """
    On Python 3.4 and later, when a package is imported from
    an empty directory, its `__path__` will be a _NamespacePath
    object and not a list, and _NamespacePath objects cannot
    be indexed, leading to the error reported in #102.
    This wrapper ensures that the path is a list for that reason.
    """
    return list(path)


def _find_gen_dir():
    r"""Create, if needed, and return a directory where automatically
    generated modules will be created.

    Usually, this is the directory 'Lib/site-packages/comtypes/gen'.

    If the above directory cannot be created, or if it is not a
    directory in the file system (when comtypes is imported from a
    zip-archive or a zipped egg), or if the current user cannot create
    files in this directory, an additional directory is created and
    appended to comtypes.gen.__path__ .

    For a Python script using comtypes, the additional directory is
    '%APPDATA%\<username>\Python\Python25\comtypes_cache'.

    For an executable frozen with py2exe, the additional directory is
    '%TEMP%\comtypes_cache\<imagebasename>-25'.
    """
    _create_comtypes_gen_package()
    from comtypes import gen
    gen_path = _ensure_list(gen.__path__)
    if not _is_writeable(gen_path):
        ftype = getattr(sys, 'frozen', None)
        version_str = '%d%d' % sys.version_info[:2]
        if ftype == None:
            subdir = 'Python\\Python%s\\comtypes_cache' % version_str
            basedir = _get_appdata_dir()
        elif ftype == 'dll':
            path = _get_module_filename(sys.frozendllhandle)
            base = os.path.splitext(os.path.basename(path))[0]
            subdir = 'comtypes_cache\\%s-%s' % (base, version_str)
            basedir = tempfile.gettempdir()
        else:
            base = os.path.splitext(os.path.basename(sys.executable))[0]
            subdir = 'comtypes_cache\\%s-%s' % (base, version_str)
            basedir = tempfile.gettempdir()
        gen_dir = os.path.join(basedir, subdir)
        if not os.path.exists(gen_dir):
            logger.info("Creating writeable comtypes cache directory: '%s'", gen_dir)
            os.makedirs(gen_dir)
        gen_path.append(gen_dir)
    result = os.path.abspath(gen_path[(-1)])
    logger.info("Using writeable comtypes cache directory: '%s'", result)
    return result


SHGetSpecialFolderPath = ctypes.OleDLL('shell32.dll').SHGetSpecialFolderPathW
GetModuleFileName = ctypes.WinDLL('kernel32.dll').GetModuleFileNameW
SHGetSpecialFolderPath.argtypes = [ctypes.c_ulong, ctypes.c_wchar_p,
 ctypes.c_int, ctypes.c_int]
GetModuleFileName.restype = ctypes.c_ulong
GetModuleFileName.argtypes = [ctypes.c_ulong, ctypes.c_wchar_p, ctypes.c_ulong]
CSIDL_APPDATA = 26
MAX_PATH = 260

def _create_comtypes_gen_package--- This code section failed: ---

 L.  89         0  SETUP_FINALLY        30  'to 30'

 L.  90         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME_ATTR         comtypes.gen
                8  STORE_FAST               'comtypes'

 L.  91        10  LOAD_GLOBAL              logger
               12  LOAD_METHOD              info
               14  LOAD_STR                 'Imported existing %s'
               16  LOAD_FAST                'comtypes'
               18  LOAD_ATTR                gen
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
               24  POP_BLOCK        
            26_28  JUMP_FORWARD        300  'to 300'
             30_0  COME_FROM_FINALLY     0  '0'

 L.  92        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
            34_36  <121>               298  ''
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  93        44  LOAD_CONST               0
               46  LOAD_CONST               None
               48  IMPORT_NAME              comtypes
               50  STORE_FAST               'comtypes'

 L.  94        52  LOAD_GLOBAL              logger
               54  LOAD_METHOD              info
               56  LOAD_STR                 'Could not import comtypes.gen, trying to create it.'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L.  95        62  SETUP_FINALLY       196  'to 196'

 L.  96        64  LOAD_GLOBAL              os
               66  LOAD_ATTR                path
               68  LOAD_METHOD              abspath
               70  LOAD_GLOBAL              os
               72  LOAD_ATTR                path
               74  LOAD_METHOD              join
               76  LOAD_FAST                'comtypes'
               78  LOAD_ATTR                __path__
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_STR                 'gen'
               86  CALL_METHOD_2         2  ''
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'comtypes_path'

 L.  97        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              isdir
               98  LOAD_FAST                'comtypes_path'
              100  CALL_METHOD_1         1  ''
              102  POP_JUMP_IF_TRUE    126  'to 126'

 L.  98       104  LOAD_GLOBAL              os
              106  LOAD_METHOD              mkdir
              108  LOAD_FAST                'comtypes_path'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L.  99       114  LOAD_GLOBAL              logger
              116  LOAD_METHOD              info
              118  LOAD_STR                 "Created comtypes.gen directory: '%s'"
              120  LOAD_FAST                'comtypes_path'
              122  CALL_METHOD_2         2  ''
              124  POP_TOP          
            126_0  COME_FROM           102  '102'

 L. 100       126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              join
              132  LOAD_FAST                'comtypes_path'
              134  LOAD_STR                 '__init__.py'
              136  CALL_METHOD_2         2  ''
              138  STORE_FAST               'comtypes_init'

 L. 101       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              exists
              146  LOAD_FAST                'comtypes_init'
              148  CALL_METHOD_1         1  ''
              150  POP_JUMP_IF_TRUE    192  'to 192'

 L. 102       152  LOAD_GLOBAL              logger
              154  LOAD_METHOD              info
              156  LOAD_STR                 "Writing __init__.py file: '%s'"
              158  LOAD_FAST                'comtypes_init'
              160  CALL_METHOD_2         2  ''
              162  POP_TOP          

 L. 103       164  LOAD_GLOBAL              open
              166  LOAD_FAST                'comtypes_init'
              168  LOAD_STR                 'w'
              170  CALL_FUNCTION_2       2  ''
              172  STORE_FAST               'ofi'

 L. 104       174  LOAD_FAST                'ofi'
              176  LOAD_METHOD              write
              178  LOAD_STR                 '# comtypes.gen package, directory for generated files.\n'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 105       184  LOAD_FAST                'ofi'
              186  LOAD_METHOD              close
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          
            192_0  COME_FROM           150  '150'
              192  POP_BLOCK        
              194  JUMP_FORWARD        294  'to 294'
            196_0  COME_FROM_FINALLY    62  '62'

 L. 106       196  DUP_TOP          
              198  LOAD_GLOBAL              OSError
              200  LOAD_GLOBAL              IOError
              202  BUILD_TUPLE_2         2 
          204_206  <121>               292  ''
              208  POP_TOP          
              210  STORE_FAST               'details'
              212  POP_TOP          
              214  SETUP_FINALLY       284  'to 284'

 L. 107       216  LOAD_GLOBAL              logger
              218  LOAD_METHOD              info
              220  LOAD_STR                 'Creating comtypes.gen package failed: %s'
              222  LOAD_FAST                'details'
              224  CALL_METHOD_2         2  ''
              226  POP_TOP          

 L. 108       228  LOAD_GLOBAL              types
              230  LOAD_METHOD              ModuleType
              232  LOAD_STR                 'comtypes.gen'
              234  CALL_METHOD_1         1  ''
              236  DUP_TOP          
              238  STORE_FAST               'module'
              240  LOAD_GLOBAL              sys
              242  LOAD_ATTR                modules
              244  LOAD_STR                 'comtypes.gen'
              246  STORE_SUBSCR     

 L. 109       248  LOAD_FAST                'module'
              250  LOAD_FAST                'comtypes'
              252  STORE_ATTR               gen

 L. 110       254  BUILD_LIST_0          0 
              256  LOAD_FAST                'comtypes'
              258  LOAD_ATTR                gen
              260  STORE_ATTR               __path__

 L. 111       262  LOAD_GLOBAL              logger
              264  LOAD_METHOD              info
              266  LOAD_STR                 'Created a memory-only package.'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
              272  POP_BLOCK        
              274  POP_EXCEPT       
              276  LOAD_CONST               None
              278  STORE_FAST               'details'
              280  DELETE_FAST              'details'
              282  JUMP_FORWARD        294  'to 294'
            284_0  COME_FROM_FINALLY   214  '214'
              284  LOAD_CONST               None
              286  STORE_FAST               'details'
              288  DELETE_FAST              'details'
              290  <48>             
              292  <48>             
            294_0  COME_FROM           282  '282'
            294_1  COME_FROM           194  '194'
              294  POP_EXCEPT       
              296  JUMP_FORWARD        300  'to 300'
              298  <48>             
            300_0  COME_FROM           296  '296'
            300_1  COME_FROM            26  '26'

Parse error at or near `<121>' instruction at offset 34_36


def _is_writeable(path):
    """Check if the first part, if any, on path is a directory in
    which we can create files."""
    if not path:
        return False
    return os.access(path[0], os.W_OK)


def _get_module_filename(hmodule):
    """Call the Windows GetModuleFileName function which determines
    the path from a module handle."""
    path = ctypes.create_unicode_buffer(MAX_PATH)
    if GetModuleFileName(hmodule, path, MAX_PATH):
        return path.value
    raise ctypes.WinError()


def _get_appdata_dir():
    """Return the 'file system directory that serves as a common
    repository for application-specific data' - CSIDL_APPDATA"""
    path = ctypes.create_unicode_buffer(MAX_PATH)
    SHGetSpecialFolderPath(0, path, CSIDL_APPDATA, True)
    return path.value