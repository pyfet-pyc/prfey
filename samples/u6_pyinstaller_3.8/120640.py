# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: imp.py
"""This module provides the components needed to build your own __import__
function.  Undocumented functions are obsolete.

In most cases it is preferred you consider using the importlib module's
functionality over this module.

"""
from _imp import lock_held, acquire_lock, release_lock, get_frozen_object, is_frozen_package, init_frozen, is_builtin, is_frozen, _fix_co_filename
try:
    from _imp import create_dynamic
except ImportError:
    create_dynamic = None
else:
    from importlib._bootstrap import _ERR_MSG, _exec, _load, _builtin_from_name
    from importlib._bootstrap_external import SourcelessFileLoader
    from importlib import machinery
    from importlib import util
    import importlib, os, sys, tokenize, types, warnings
    warnings.warn("the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses", DeprecationWarning,
      stacklevel=2)
    SEARCH_ERROR = 0
    PY_SOURCE = 1
    PY_COMPILED = 2
    C_EXTENSION = 3
    PY_RESOURCE = 4
    PKG_DIRECTORY = 5
    C_BUILTIN = 6
    PY_FROZEN = 7
    PY_CODERESOURCE = 8
    IMP_HOOK = 9

    def new_module(name):
        """**DEPRECATED**

    Create a new module.

    The module is not entered into sys.modules.

    """
        return types.ModuleType(name)


    def get_magic():
        """**DEPRECATED**

    Return the magic number for .pyc files.
    """
        return util.MAGIC_NUMBER


    def get_tag():
        """Return the magic tag for .pyc files."""
        return sys.implementation.cache_tag


    def cache_from_source--- This code section failed: ---

 L.  86         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              catch_warnings
                4  CALL_METHOD_0         0  ''
                6  SETUP_WITH           44  'to 44'
                8  POP_TOP          

 L.  87        10  LOAD_GLOBAL              warnings
               12  LOAD_METHOD              simplefilter
               14  LOAD_STR                 'ignore'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  88        20  LOAD_GLOBAL              util
               22  LOAD_METHOD              cache_from_source
               24  LOAD_FAST                'path'
               26  LOAD_FAST                'debug_override'
               28  CALL_METHOD_2         2  ''
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  POP_FINALLY           0  ''
               42  RETURN_VALUE     
             44_0  COME_FROM_WITH        6  '6'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 32


    def source_from_cache(path):
        """**DEPRECATED**

    Given the path to a .pyc. file, return the path to its .py file.

    The .pyc file does not need to exist; this simply returns the path to
    the .py file calculated to correspond to the .pyc file.  If path does
    not conform to PEP 3147 format, ValueError will be raised. If
    sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
        return util.source_from_cache(path)


    def get_suffixes():
        """**DEPRECATED**"""
        extensions = [(
         s, 'rb', C_EXTENSION) for s in machinery.EXTENSION_SUFFIXES]
        source = [(s, 'r', PY_SOURCE) for s in machinery.SOURCE_SUFFIXES]
        bytecode = [(s, 'rb', PY_COMPILED) for s in machinery.BYTECODE_SUFFIXES]
        return extensions + source + bytecode


    class NullImporter:
        __doc__ = '**DEPRECATED**\n\n    Null import object.\n\n    '

        def __init__(self, path):
            if path == '':
                raise ImportError('empty pathname', path='')
            else:
                if os.path.isdir(path):
                    raise ImportError('existing directory', path=path)

        def find_module(self, fullname):
            """Always returns None."""
            pass


    class _HackedGetData:
        __doc__ = "Compatibility support for 'file' arguments of various load_*()\n    functions."

        def __init__(self, fullname, path, file=None):
            super().__init__fullnamepath
            self.file = file

        def get_data--- This code section failed: ---

 L. 144         0  LOAD_FAST                'self'
                2  LOAD_ATTR                file
                4  POP_JUMP_IF_FALSE   108  'to 108'
                6  LOAD_FAST                'path'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                path
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE   108  'to 108'

 L. 147        16  LOAD_FAST                'self'
               18  LOAD_ATTR                file
               20  LOAD_ATTR                closed
               22  POP_JUMP_IF_TRUE     48  'to 48'

 L. 148        24  LOAD_FAST                'self'
               26  LOAD_ATTR                file
               28  STORE_FAST               'file'

 L. 149        30  LOAD_STR                 'b'
               32  LOAD_FAST                'file'
               34  LOAD_ATTR                mode
               36  COMPARE_OP               not-in
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 150        40  LOAD_FAST                'file'
               42  LOAD_METHOD              close
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            22  '22'

 L. 151        48  LOAD_FAST                'self'
               50  LOAD_ATTR                file
               52  LOAD_ATTR                closed
               54  POP_JUMP_IF_FALSE    74  'to 74'

 L. 152        56  LOAD_GLOBAL              open
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                path
               62  LOAD_STR                 'rb'
               64  CALL_FUNCTION_2       2  ''
               66  DUP_TOP          
               68  LOAD_FAST                'self'
               70  STORE_ATTR               file
               72  STORE_FAST               'file'
             74_0  COME_FROM            54  '54'

 L. 154        74  LOAD_FAST                'file'
               76  SETUP_WITH          100  'to 100'
               78  POP_TOP          

 L. 155        80  LOAD_FAST                'file'
               82  LOAD_METHOD              read
               84  CALL_METHOD_0         0  ''
               86  POP_BLOCK        
               88  ROT_TWO          
               90  BEGIN_FINALLY    
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  POP_FINALLY           0  ''
               98  RETURN_VALUE     
            100_0  COME_FROM_WITH       76  '76'
              100  WITH_CLEANUP_START
              102  WITH_CLEANUP_FINISH
              104  END_FINALLY      
              106  JUMP_FORWARD        120  'to 120'
            108_0  COME_FROM            14  '14'
            108_1  COME_FROM             4  '4'

 L. 157       108  LOAD_GLOBAL              super
              110  CALL_FUNCTION_0       0  ''
              112  LOAD_METHOD              get_data
              114  LOAD_FAST                'path'
              116  CALL_METHOD_1         1  ''
              118  RETURN_VALUE     
            120_0  COME_FROM           106  '106'

Parse error at or near `ROT_TWO' instruction at offset 88


    class _LoadSourceCompatibility(_HackedGetData, machinery.SourceFileLoader):
        __doc__ = 'Compatibility support for implementing load_source().'


    def load_source(name, pathname, file=None):
        loader = _LoadSourceCompatibility(name, pathname, file)
        spec = util.spec_from_file_location(name, pathname, loader=loader)
        if name in sys.modules:
            module = _exec(spec, sys.modules[name])
        else:
            module = _load(spec)
        module.__loader__ = machinery.SourceFileLoadernamepathname
        module.__spec__.loader = module.__loader__
        return module


    class _LoadCompiledCompatibility(_HackedGetData, SourcelessFileLoader):
        __doc__ = 'Compatibility support for implementing load_compiled().'


    def load_compiled(name, pathname, file=None):
        """**DEPRECATED**"""
        loader = _LoadCompiledCompatibility(name, pathname, file)
        spec = util.spec_from_file_location(name, pathname, loader=loader)
        if name in sys.modules:
            module = _exec(spec, sys.modules[name])
        else:
            module = _load(spec)
        module.__loader__ = SourcelessFileLoader(name, pathname)
        module.__spec__.loader = module.__loader__
        return module


    def load_package(name, path):
        """**DEPRECATED**"""
        if os.path.isdir(path):
            extensions = machinery.SOURCE_SUFFIXES[:] + machinery.BYTECODE_SUFFIXES[:]
            for extension in extensions:
                init_path = os.path.joinpath('__init__' + extension)
                if os.path.exists(init_path):
                    path = init_path
                    break
            else:
                raise ValueError('{!r} is not a package'.format(path))

        spec = util.spec_from_file_location(name, path, submodule_search_locations=[])
        if name in sys.modules:
            return _exec(spec, sys.modules[name])
        return _load(spec)


    def load_module--- This code section failed: ---

 L. 227         0  LOAD_FAST                'details'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'suffix'
                6  STORE_FAST               'mode'
                8  STORE_FAST               'type_'

 L. 228        10  LOAD_FAST                'mode'
               12  POP_JUMP_IF_FALSE    48  'to 48'
               14  LOAD_FAST                'mode'
               16  LOAD_METHOD              startswith
               18  LOAD_CONST               ('r', 'U')
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'
               24  LOAD_STR                 '+'
               26  LOAD_FAST                'mode'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    48  'to 48'
             32_0  COME_FROM            22  '22'

 L. 229        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'invalid file open mode {!r}'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'mode'
               40  CALL_METHOD_1         1  ''
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  JUMP_FORWARD        288  'to 288'
             48_0  COME_FROM            30  '30'
             48_1  COME_FROM            12  '12'

 L. 230        48  LOAD_FAST                'file'
               50  LOAD_CONST               None
               52  COMPARE_OP               is
               54  POP_JUMP_IF_FALSE    88  'to 88'
               56  LOAD_FAST                'type_'
               58  LOAD_GLOBAL              PY_SOURCE
               60  LOAD_GLOBAL              PY_COMPILED
               62  BUILD_SET_2           2 
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE    88  'to 88'

 L. 231        68  LOAD_STR                 'file object required for import (type code {})'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'type_'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'msg'

 L. 232        78  LOAD_GLOBAL              ValueError
               80  LOAD_FAST                'msg'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
               86  JUMP_FORWARD        288  'to 288'
             88_0  COME_FROM            66  '66'
             88_1  COME_FROM            54  '54'

 L. 233        88  LOAD_FAST                'type_'
               90  LOAD_GLOBAL              PY_SOURCE
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 234        96  LOAD_GLOBAL              load_source
               98  LOAD_FAST                'name'
              100  LOAD_FAST                'filename'
              102  LOAD_FAST                'file'
              104  CALL_FUNCTION_3       3  ''
              106  RETURN_VALUE     
            108_0  COME_FROM            94  '94'

 L. 235       108  LOAD_FAST                'type_'
              110  LOAD_GLOBAL              PY_COMPILED
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L. 236       116  LOAD_GLOBAL              load_compiled
              118  LOAD_FAST                'name'
              120  LOAD_FAST                'filename'
              122  LOAD_FAST                'file'
              124  CALL_FUNCTION_3       3  ''
              126  RETURN_VALUE     
            128_0  COME_FROM           114  '114'

 L. 237       128  LOAD_FAST                'type_'
              130  LOAD_GLOBAL              C_EXTENSION
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   210  'to 210'
              136  LOAD_GLOBAL              load_dynamic
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE   210  'to 210'

 L. 238       144  LOAD_FAST                'file'
              146  LOAD_CONST               None
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   196  'to 196'

 L. 239       152  LOAD_GLOBAL              open
              154  LOAD_FAST                'filename'
              156  LOAD_STR                 'rb'
              158  CALL_FUNCTION_2       2  ''
              160  SETUP_WITH          188  'to 188'
              162  STORE_FAST               'opened_file'

 L. 240       164  LOAD_GLOBAL              load_dynamic
              166  LOAD_FAST                'name'
              168  LOAD_FAST                'filename'
              170  LOAD_FAST                'opened_file'
              172  CALL_FUNCTION_3       3  ''
              174  POP_BLOCK        
              176  ROT_TWO          
              178  BEGIN_FINALLY    
              180  WITH_CLEANUP_START
              182  WITH_CLEANUP_FINISH
              184  POP_FINALLY           0  ''
              186  RETURN_VALUE     
            188_0  COME_FROM_WITH      160  '160'
              188  WITH_CLEANUP_START
              190  WITH_CLEANUP_FINISH
              192  END_FINALLY      
              194  JUMP_FORWARD        208  'to 208'
            196_0  COME_FROM           150  '150'

 L. 242       196  LOAD_GLOBAL              load_dynamic
              198  LOAD_FAST                'name'
              200  LOAD_FAST                'filename'
              202  LOAD_FAST                'file'
              204  CALL_FUNCTION_3       3  ''
              206  RETURN_VALUE     
            208_0  COME_FROM           194  '194'
              208  JUMP_FORWARD        288  'to 288'
            210_0  COME_FROM           142  '142'
            210_1  COME_FROM           134  '134'

 L. 243       210  LOAD_FAST                'type_'
              212  LOAD_GLOBAL              PKG_DIRECTORY
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 244       218  LOAD_GLOBAL              load_package
              220  LOAD_FAST                'name'
              222  LOAD_FAST                'filename'
              224  CALL_FUNCTION_2       2  ''
              226  RETURN_VALUE     
            228_0  COME_FROM           216  '216'

 L. 245       228  LOAD_FAST                'type_'
              230  LOAD_GLOBAL              C_BUILTIN
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   246  'to 246'

 L. 246       238  LOAD_GLOBAL              init_builtin
              240  LOAD_FAST                'name'
              242  CALL_FUNCTION_1       1  ''
              244  RETURN_VALUE     
            246_0  COME_FROM           234  '234'

 L. 247       246  LOAD_FAST                'type_'
              248  LOAD_GLOBAL              PY_FROZEN
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   264  'to 264'

 L. 248       256  LOAD_GLOBAL              init_frozen
              258  LOAD_FAST                'name'
              260  CALL_FUNCTION_1       1  ''
              262  RETURN_VALUE     
            264_0  COME_FROM           252  '252'

 L. 250       264  LOAD_STR                 "Don't know how to import {} (type code {})"
              266  LOAD_METHOD              format
              268  LOAD_FAST                'name'
              270  LOAD_FAST                'type_'
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'msg'

 L. 251       276  LOAD_GLOBAL              ImportError
              278  LOAD_FAST                'msg'
              280  LOAD_FAST                'name'
              282  LOAD_CONST               ('name',)
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  RAISE_VARARGS_1       1  'exception instance'
            288_0  COME_FROM           208  '208'
            288_1  COME_FROM            86  '86'
            288_2  COME_FROM            46  '46'

Parse error at or near `ROT_TWO' instruction at offset 176


    def find_module(name, path=None):
        """**DEPRECATED**

    Search for a module.

    If path is omitted or None, search for a built-in, frozen or special
    module and continue search in sys.path. The module name cannot
    contain '.'; to search for a submodule of a package, pass the
    submodule name and the package's __path__.

    """
        if not isinstance(name, str):
            raise TypeError("'name' must be a str, not {}".format(type(name)))
        else:
            if not isinstance(path, (type(None), list)):
                raise RuntimeError("'path' must be None or a list, not {}".format(type(path)))
            else:
                if path is None:
                    if is_builtin(name):
                        return (
                         None, None, ('', '', C_BUILTIN))
                    if is_frozen(name):
                        return (
                         None, None, ('', '', PY_FROZEN))
                    path = sys.path
                for entry in path:
                    package_directory = os.path.joinentryname
                    for suffix in ('.py', machinery.BYTECODE_SUFFIXES[0]):
                        package_file_name = '__init__' + suffix
                        file_path = os.path.joinpackage_directorypackage_file_name
                        if os.path.isfile(file_path):
                            return (
                             None, package_directory, ('', '', PKG_DIRECTORY))
                        for suffix, mode, type_ in get_suffixes():
                            file_name = name + suffix
                            file_path = os.path.joinentryfile_name
                            if os.path.isfile(file_path):
                                break
                        else:
                            break

                    else:
                        raise ImportError((_ERR_MSG.format(name)), name=name)
                        encoding = None

                    if 'b' not in mode:
                        with open(file_path, 'rb') as (file):
                            encoding = tokenize.detect_encoding(file.readline)[0]

            file = open(file_path, mode, encoding=encoding)
            return (file, file_path, (suffix, mode, type_))


    def reload(module):
        """**DEPRECATED**

    Reload the module and return it.

    The module must have been successfully imported before.

    """
        return importlib.reload(module)


    def init_builtin--- This code section failed: ---

 L. 323         0  SETUP_FINALLY        12  'to 12'

 L. 324         2  LOAD_GLOBAL              _builtin_from_name
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 325        12  DUP_TOP          
               14  LOAD_GLOBAL              ImportError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    32  'to 32'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 326        26  POP_EXCEPT       
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            18  '18'
               32  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


    if create_dynamic:

        def load_dynamic(name, path, file=None):
            """**DEPRECATED**

        Load an extension module.
        """
            import importlib.machinery
            loader = importlib.machinery.ExtensionFileLoadernamepath
            spec = importlib.machinery.ModuleSpec(name=name,
              loader=loader,
              origin=path)
            return _load(spec)


    else:
        load_dynamic = None