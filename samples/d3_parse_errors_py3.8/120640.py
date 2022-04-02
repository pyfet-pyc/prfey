# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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


    def cache_from_source(path, debug_override=None):
        """**DEPRECATED**

    Given the path to a .py file, return the path to its .pyc file.

    The .py file does not need to exist; this simply returns the path to the
    .pyc file calculated as if the .py file were imported.

    If debug_override is not None, then it must be a boolean and is used in
    place of sys.flags.optimize.

    If sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return util.cache_from_source(path, debug_override)


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
            elif os.path.isdir(path):
                raise ImportError('existing directory', path=path)

        def find_module(self, fullname):
            """Always returns None."""
            pass


    class _HackedGetData:
        __doc__ = "Compatibility support for 'file' arguments of various load_*()\n    functions."

        def __init__(self, fullname, path, file=None):
            super().__init__(fullname, path)
            self.file = file

        def get_data(self, path):
            if self.file and path == self.path:
                if not self.file.closed:
                    file = self.file
                    if 'b' not in file.mode:
                        file.close()
                if self.file.closed:
                    self.file = file = open(self.path, 'rb')
                with file:
                    return file.read()
            else:
                return super().get_data(path)


    class _LoadSourceCompatibility(_HackedGetData, machinery.SourceFileLoader):
        __doc__ = 'Compatibility support for implementing load_source().'


    def load_source(name, pathname, file=None):
        loader = _LoadSourceCompatibility(name, pathname, file)
        spec = util.spec_from_file_location(name, pathname, loader=loader)
        if name in sys.modules:
            module = _exec(spec, sys.modules[name])
        else:
            module = _load(spec)
        module.__loader__ = machinery.SourceFileLoader(name, pathname)
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
                init_path = os.path.join(path, '__init__' + extension)
                if os.path.exists(init_path):
                    path = init_path
                    break
            else:
                raise ValueError('{!r} is not a package'.format(path))

        spec = util.spec_from_file_location(name, path, submodule_search_locations=[])
        if name in sys.modules:
            return _exec(spec, sys.modules[name])
        return _load(spec)


    def load_module(name, file, filename, details):
        """**DEPRECATED**

    Load a module, given information returned by find_module().

    The module name must include the full package name, if any.

    """
        suffix, mode, type_ = details
        if not mode and mode.startswith(('r', 'U')) or '+' in mode:
            raise ValueError('invalid file open mode {!r}'.format(mode))
        elif file is None and type_ in {PY_SOURCE, PY_COMPILED}:
            msg = 'file object required for import (type code {})'.format(type_)
            raise ValueError(msg)
        else:
            if type_ == PY_SOURCE:
                return load_source(name, filename, file)
            if type_ == PY_COMPILED:
                return load_compiled(name, filename, file)
            if type_ == C_EXTENSION and load_dynamic is not None:
                if file is None:
                    with open(filename, 'rb') as opened_file:
                        return load_dynamic(name, filename, opened_file)
                else:
                    return load_dynamic(name, filename, file)
            else:
                if type_ == PKG_DIRECTORY:
                    return load_package(name, filename)
                if type_ == C_BUILTIN:
                    return init_builtin(name)
                if type_ == PY_FROZEN:
                    return init_frozen(name)
                msg = "Don't know how to import {} (type code {})".format(name, type_)
                raise ImportError(msg, name=name)


    def find_module--- This code section failed: ---

 L. 265         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     30  'to 30'

 L. 266        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 "'name' must be a str, not {}"
               14  LOAD_METHOD              format
               16  LOAD_GLOBAL              type
               18  LOAD_FAST                'name'
               20  CALL_FUNCTION_1       1  ''
               22  CALL_METHOD_1         1  ''
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
               28  JUMP_FORWARD         66  'to 66'
             30_0  COME_FROM             8  '8'

 L. 267        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'path'
               34  LOAD_GLOBAL              type
               36  LOAD_CONST               None
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_GLOBAL              list
               42  BUILD_TUPLE_2         2 
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     66  'to 66'

 L. 269        48  LOAD_GLOBAL              RuntimeError
               50  LOAD_STR                 "'path' must be None or a list, not {}"
               52  LOAD_METHOD              format

 L. 270        54  LOAD_GLOBAL              type
               56  LOAD_FAST                'path'
               58  CALL_FUNCTION_1       1  ''

 L. 269        60  CALL_METHOD_1         1  ''
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            46  '46'
             66_1  COME_FROM            28  '28'

 L. 272        66  LOAD_FAST                'path'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE   128  'to 128'

 L. 273        74  LOAD_GLOBAL              is_builtin
               76  LOAD_FAST                'name'
               78  CALL_FUNCTION_1       1  ''
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L. 274        82  LOAD_CONST               None
               84  LOAD_CONST               None
               86  LOAD_STR                 ''
               88  LOAD_STR                 ''
               90  LOAD_GLOBAL              C_BUILTIN
               92  BUILD_TUPLE_3         3 
               94  BUILD_TUPLE_3         3 
               96  RETURN_VALUE     
             98_0  COME_FROM            80  '80'

 L. 275        98  LOAD_GLOBAL              is_frozen
              100  LOAD_FAST                'name'
              102  CALL_FUNCTION_1       1  ''
              104  POP_JUMP_IF_FALSE   122  'to 122'

 L. 276       106  LOAD_CONST               None
              108  LOAD_CONST               None
              110  LOAD_STR                 ''
              112  LOAD_STR                 ''
              114  LOAD_GLOBAL              PY_FROZEN
              116  BUILD_TUPLE_3         3 
              118  BUILD_TUPLE_3         3 
              120  RETURN_VALUE     
            122_0  COME_FROM           104  '104'

 L. 278       122  LOAD_GLOBAL              sys
              124  LOAD_ATTR                path
              126  STORE_FAST               'path'
            128_0  COME_FROM            72  '72'

 L. 280       128  LOAD_FAST                'path'
              130  GET_ITER         
            132_0  COME_FROM           294  '294'
            132_1  COME_FROM           286  '286'
              132  FOR_ITER            296  'to 296'
              134  STORE_FAST               'entry'

 L. 281       136  LOAD_GLOBAL              os
              138  LOAD_ATTR                path
              140  LOAD_METHOD              join
              142  LOAD_FAST                'entry'
              144  LOAD_FAST                'name'
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'package_directory'

 L. 282       150  LOAD_STR                 '.py'
              152  LOAD_GLOBAL              machinery
              154  LOAD_ATTR                BYTECODE_SUFFIXES
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  BUILD_TUPLE_2         2 
              162  GET_ITER         
            164_0  COME_FROM           226  '226'
            164_1  COME_FROM           200  '200'
              164  FOR_ITER            228  'to 228'
              166  STORE_FAST               'suffix'

 L. 283       168  LOAD_STR                 '__init__'
              170  LOAD_FAST                'suffix'
              172  BINARY_ADD       
              174  STORE_FAST               'package_file_name'

 L. 284       176  LOAD_GLOBAL              os
              178  LOAD_ATTR                path
              180  LOAD_METHOD              join
              182  LOAD_FAST                'package_directory'
              184  LOAD_FAST                'package_file_name'
              186  CALL_METHOD_2         2  ''
              188  STORE_FAST               'file_path'

 L. 285       190  LOAD_GLOBAL              os
              192  LOAD_ATTR                path
              194  LOAD_METHOD              isfile
              196  LOAD_FAST                'file_path'
              198  CALL_METHOD_1         1  ''
              200  POP_JUMP_IF_FALSE_BACK   164  'to 164'

 L. 286       202  LOAD_CONST               None
              204  LOAD_FAST                'package_directory'
              206  LOAD_STR                 ''
              208  LOAD_STR                 ''
              210  LOAD_GLOBAL              PKG_DIRECTORY
              212  BUILD_TUPLE_3         3 
              214  BUILD_TUPLE_3         3 
              216  ROT_TWO          
              218  POP_TOP          
              220  ROT_TWO          
              222  POP_TOP          
              224  RETURN_VALUE     
              226  JUMP_BACK           164  'to 164'
            228_0  COME_FROM           164  '164'

 L. 287       228  LOAD_GLOBAL              get_suffixes
              230  CALL_FUNCTION_0       0  ''
              232  GET_ITER         
            234_0  COME_FROM           284  '284'
            234_1  COME_FROM           276  '276'
              234  FOR_ITER            286  'to 286'
              236  UNPACK_SEQUENCE_3     3 
              238  STORE_FAST               'suffix'
              240  STORE_FAST               'mode'
              242  STORE_FAST               'type_'

 L. 288       244  LOAD_FAST                'name'
              246  LOAD_FAST                'suffix'
              248  BINARY_ADD       
              250  STORE_FAST               'file_name'

 L. 289       252  LOAD_GLOBAL              os
              254  LOAD_ATTR                path
              256  LOAD_METHOD              join
              258  LOAD_FAST                'entry'
              260  LOAD_FAST                'file_name'
              262  CALL_METHOD_2         2  ''
              264  STORE_FAST               'file_path'

 L. 290       266  LOAD_GLOBAL              os
              268  LOAD_ATTR                path
              270  LOAD_METHOD              isfile
              272  LOAD_FAST                'file_path'
              274  CALL_METHOD_1         1  ''
              276  POP_JUMP_IF_FALSE_BACK   234  'to 234'

 L. 291       278  POP_TOP          
          280_282  BREAK_LOOP          288  'to 288'
              284  JUMP_BACK           234  'to 234'
            286_0  COME_FROM           234  '234'

 L. 293       286  JUMP_BACK           132  'to 132'
            288_0  COME_FROM           280  '280'

 L. 294       288  POP_TOP          
          290_292  BREAK_LOOP          314  'to 314'
              294  JUMP_BACK           132  'to 132'
            296_0  COME_FROM           132  '132'

 L. 296       296  LOAD_GLOBAL              ImportError
              298  LOAD_GLOBAL              _ERR_MSG
              300  LOAD_METHOD              format
              302  LOAD_FAST                'name'
              304  CALL_METHOD_1         1  ''
              306  LOAD_FAST                'name'
              308  LOAD_CONST               ('name',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  RAISE_VARARGS_1       1  'exception instance'
            314_0  COME_FROM           290  '290'

 L. 298       314  LOAD_CONST               None
              316  STORE_FAST               'encoding'

 L. 299       318  LOAD_STR                 'b'
              320  LOAD_FAST                'mode'
              322  COMPARE_OP               not-in
          324_326  POP_JUMP_IF_FALSE   366  'to 366'

 L. 300       328  LOAD_GLOBAL              open
              330  LOAD_FAST                'file_path'
              332  LOAD_STR                 'rb'
              334  CALL_FUNCTION_2       2  ''
              336  SETUP_WITH          360  'to 360'
              338  STORE_FAST               'file'

 L. 301       340  LOAD_GLOBAL              tokenize
              342  LOAD_METHOD              detect_encoding
              344  LOAD_FAST                'file'
              346  LOAD_ATTR                readline
              348  CALL_METHOD_1         1  ''
              350  LOAD_CONST               0
              352  BINARY_SUBSCR    
              354  STORE_FAST               'encoding'
              356  POP_BLOCK        
              358  BEGIN_FINALLY    
            360_0  COME_FROM_WITH      336  '336'
              360  WITH_CLEANUP_START
              362  WITH_CLEANUP_FINISH
              364  END_FINALLY      
            366_0  COME_FROM           324  '324'

 L. 302       366  LOAD_GLOBAL              open
              368  LOAD_FAST                'file_path'
              370  LOAD_FAST                'mode'
              372  LOAD_FAST                'encoding'
              374  LOAD_CONST               ('encoding',)
              376  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              378  STORE_FAST               'file'

 L. 303       380  LOAD_FAST                'file'
              382  LOAD_FAST                'file_path'
              384  LOAD_FAST                'suffix'
              386  LOAD_FAST                'mode'
              388  LOAD_FAST                'type_'
              390  BUILD_TUPLE_3         3 
              392  BUILD_TUPLE_3         3 
              394  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 394


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

Parse error at or near `LOAD_CONST' instruction at offset 28


if create_dynamic:

    def load_dynamic(name, path, file=None):
        """**DEPRECATED**

        Load an extension module.
        """
        import importlib.machinery
        loader = importlib.machinery.ExtensionFileLoader(name, path)
        spec = importlib.machinery.ModuleSpec(name=name,
          loader=loader,
          origin=path)
        return _load(spec)


else:
    load_dynamic = None