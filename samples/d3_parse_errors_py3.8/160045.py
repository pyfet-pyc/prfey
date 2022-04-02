# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: c:\users\user\appdata\local\programs\python\python38-32\lib\site-packages\PyInstaller\loader\pyimod03_importers.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 35592 bytes
"""
PEP-302 and PEP-451 importers for frozen applications.
"""
import sys, pyimod01_os_path as pyi_os_path
from pyimod02_archive import ArchiveReadError, ZlibArchiveReader
SYS_PREFIX = sys._MEIPASS
SYS_PREFIXLEN = len(SYS_PREFIX)
if sys.version_info[0:2] < (3, 3):
    import imp
    imp_lock = imp.acquire_lock
    imp_unlock = imp.release_lock
    EXTENSION_SUFFIXES = dict(((f[0], f) for f in imp.get_suffixes() if f[2] == imp.C_EXTENSION))
    imp_new_module = imp.new_module
else:

    def imp_lock():
        pass


    def imp_unlock():
        pass


    import _frozen_importlib
    EXTENSION_SUFFIXES = _frozen_importlib._bootstrap_external.EXTENSION_SUFFIXES
    EXTENSION_LOADER = _frozen_importlib._bootstrap_external.ExtensionFileLoader
    imp_new_module = type(sys)
if sys.flags.verbose:

    def trace(msg, *a):
        sys.stderr.write(msg % a)
        sys.stderr.write('\n')


else:

    def trace(msg, *a):
        pass


class BuiltinImporter(object):
    __doc__ = '\n    PEP-302 wrapper of the built-in modules for sys.meta_path.\n\n    This wrapper ensures that import machinery will not look for built-in\n    modules in the bundled ZIP archive.\n    '

    def find_module(self, fullname, path=None):
        imp_lock()
        module_loader = None
        if fullname in sys.builtin_module_names:
            module_loader = self
        imp_unlock()
        return module_loader

    def load_module(self, fullname, path=None):
        imp_lock()
        try:
            try:
                module = sys.modules.get(fullname)
                if module is None:
                    module = imp.init_builtin(fullname)
            except Exception:
                if fullname in sys.modules:
                    sys.modules.pop(fullname)
                else:
                    raise

        finally:
            imp_unlock()

        return module

    def is_package(self, fullname):
        """
        Return always False since built-in modules are never packages.
        """
        if fullname in sys.builtin_module_names:
            return False
        raise ImportError('No module named ' + fullname)

    def get_code(self, fullname):
        """
        Return None for a built-in module.
        """
        if fullname in sys.builtin_module_names:
            return
        raise ImportError('No module named ' + fullname)

    def get_source(self, fullname):
        """
        Return None for a built-in module.
        """
        if fullname in sys.builtin_module_names:
            return
        raise ImportError('No module named ' + fullname)


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

 L. 196         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                path
                4  GET_ITER         
              6_0  COME_FROM           148  '148'
              6_1  COME_FROM           128  '128'
              6_2  COME_FROM           102  '102'
                6  FOR_ITER            150  'to 150'
                8  STORE_FAST               'pyz_filepath'

 L. 200        10  LOAD_GLOBAL              imp_lock
               12  CALL_FUNCTION_0       0  ''
               14  POP_TOP          

 L. 201        16  SETUP_FINALLY       140  'to 140'
               18  SETUP_FINALLY        82  'to 82'

 L. 203        20  LOAD_GLOBAL              ZlibArchiveReader
               22  LOAD_FAST                'pyz_filepath'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _pyz_archive

 L. 211        30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                path
               34  LOAD_METHOD              remove
               36  LOAD_FAST                'pyz_filepath'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 214        42  LOAD_GLOBAL              set
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _pyz_archive
               48  LOAD_ATTR                toc
               50  LOAD_METHOD              keys
               52  CALL_METHOD_0         0  ''
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               toc

 L. 216        60  LOAD_GLOBAL              trace
               62  LOAD_STR                 '# PyInstaller: FrozenImporter(%s)'
               64  LOAD_FAST                'pyz_filepath'
               66  CALL_FUNCTION_2       2  ''
               68  POP_TOP          

 L. 217        70  POP_BLOCK        
               72  POP_BLOCK        
               74  CALL_FINALLY        140  'to 140'
               76  POP_TOP          
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY    18  '18'

 L. 218        82  DUP_TOP          
               84  LOAD_GLOBAL              IOError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   108  'to 108'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 220        96  POP_EXCEPT       
               98  POP_BLOCK        
              100  CALL_FINALLY        140  'to 140'
              102  JUMP_BACK             6  'to 6'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        136  'to 136'
            108_0  COME_FROM            88  '88'

 L. 221       108  DUP_TOP          
              110  LOAD_GLOBAL              ArchiveReadError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   134  'to 134'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 223       122  POP_EXCEPT       
              124  POP_BLOCK        
              126  CALL_FINALLY        140  'to 140'
              128  JUMP_BACK             6  'to 6'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM           114  '114'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           106  '106'
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM           126  '126'
            140_1  COME_FROM           100  '100'
            140_2  COME_FROM            74  '74'
            140_3  COME_FROM_FINALLY    16  '16'

 L. 225       140  LOAD_GLOBAL              imp_unlock
              142  CALL_FUNCTION_0       0  ''
              144  POP_TOP          
              146  END_FINALLY      
              148  JUMP_BACK             6  'to 6'
            150_0  COME_FROM             6  '6'

 L. 228       150  LOAD_GLOBAL              ImportError
              152  LOAD_STR                 "Can't load frozen modules."
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_BLOCK' instruction at offset 72

    def __call__(self, path):
        """
        PEP-302 sys.path_hook processor. is_py2: This is only needed for Python
        2; see comments at `path_hook installation`_.

        sys.path_hook is a list of callables, which will be checked in
        sequence to determine if they can handle a given path item.
        """
        if path.startswith(SYS_PREFIX):
            fullname = path[SYS_PREFIXLEN + 1:].replace(pyi_os_path.os_sep, '.')
            loader = self.find_module(fullname)
            if loader is not None:
                return loader
        raise ImportError(path)

    def find_module(self, fullname, path=None):
        """
        PEP-302 finder.find_module() method for the ``sys.meta_path`` hook.

        fullname     fully qualified name of the module
        path         None for a top-level module, or package.__path__
                     for submodules or subpackages.

        Return a loader object if the module was found, or None if it wasn't.
        If find_module() raises an exception, it will be propagated to the
        caller, aborting the import.
        """
        imp_lock()
        module_loader = None
        if fullname in self.toc:
            module_loader = self
            trace'import %s # PyInstaller PYZ'fullname
        else:
            pass
        if path is not None:
            modname = fullname.split('.')[(-1)]
            for p in path:
                p = p[SYS_PREFIXLEN + 1:]
                parts = p.split(pyi_os_path.os_sep)
                if not parts:
                    pass
                else:
                    if not parts[0]:
                        parts = parts[1:]
                    else:
                        parts.append(modname)
                        entry_name = '.'.join(parts)
                    if entry_name in self.toc:
                        module_loader = FrozenPackageImporterselfentry_name
                        trace('import %s as %s # PyInstaller PYZ (__path__ override: %s)', entry_name, fullname, p)
                        break
            else:
                imp_unlock()
                if module_loader is None:
                    trace'# %s not found in PYZ'fullname

            return module_loader

    def load_module(self, fullname, entry_name=None):
        """
        PEP-302 loader.load_module() method for the ``sys.meta_path`` hook.

        Return the loaded module (instance of imp_new_module()) or raises
        an exception, preferably ImportError if an existing exception
        is not being propagated.

        When called from FrozenPackageImporter, `entry_name` is the name of the
        module as it is stored in the archive. This module will be loaded and installed
        into sys.modules using `fullname` as its name
        """
        imp_lock()
        module = None
        if entry_name is None:
            entry_name = fullname
        try:
            try:
                module = sys.modules.get(fullname)
                if module is None:
                    is_pkg, bytecode = self._pyz_archive.extract(entry_name)
                    module = imp_new_module(fullname)
                    module.__file__ = self.get_filename(entry_name)
                    if is_pkg:
                        module.__path__ = [
                         pyi_os_path.os_path_dirname(module.__file__)]
                    module.__loader__ = self
                    if is_pkg:
                        module.__package__ = fullname
                    else:
                        module.__package__ = fullname.rsplit('.', 1)[0]
                    if sys.version_info[0:2] > (3, 3):
                        module.__spec__ = _frozen_importlib.ModuleSpec(entry_name,
                          self, is_package=is_pkg)
                    sys.modules[fullname] = module
                    execbytecodemodule.__dict__
                    module = sys.modules[fullname]
            except Exception:
                if fullname in sys.modules:
                    sys.modules.pop(fullname)
                else:
                    raise

        finally:
            imp_unlock()

        return module

    def is_package(self, fullname):
        if fullname in self.toc:
            try:
                return self._pyz_archive.is_package(fullname)
            except Exception:
                raise ImportError('Loader FrozenImporter cannot handle module ' + fullname)

        else:
            raise ImportError('Loader FrozenImporter cannot handle module ' + fullname)

    def get_code--- This code section failed: ---

 L. 430         0  SETUP_FINALLY        20  'to 20'

 L. 434         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pyz_archive
                6  LOAD_METHOD              extract
                8  LOAD_FAST                'fullname'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               1
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 435        20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 436        26  LOAD_GLOBAL              ImportError
               28  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               30  LOAD_FAST                'fullname'
               32  BINARY_ADD       
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 36

    def get_source(self, fullname):
        """
        Method should return the source code for the module as a string.
        But frozen modules does not contain source code.

        Return None.
        """
        if fullname in self.toc:
            return
        raise ImportError('No module named ' + fullname)

    def get_data(self, path):
        """
        This returns the data as a string, or raise IOError if the "file"
        wasn't found. The data is always returned as if "binary" mode was used.

        This method is useful getting resources with 'pkg_resources' that are
        bundled with Python modules in the PYZ archive.

        The 'path' argument is a path that can be constructed by munging
        module.__file__ (or pkg.__path__ items)
        """
        assert path.startswith(SYS_PREFIX + pyi_os_path.os_sep)
        fullname = path[SYS_PREFIXLEN + 1:]
        if fullname in self.toc:
            return self._pyz_archive.extract(fullname)[1]
        with openpath'rb' as fp:
            return fp.read()

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

    def find_spec(self, fullname, path=None, target=None):
        """
        PEP-451 finder.find_spec() method for the ``sys.meta_path`` hook.

        fullname     fully qualified name of the module
        path         None for a top-level module, or package.__path__ for
                     submodules or subpackages.
        target       unused by this Finder

        Finders are still responsible for identifying, and typically creating,
        the loader that should be used to load a module. That loader will now
        be stored in the module spec returned by find_spec() rather than
        returned directly. As is currently the case without the PEP-452, if a
        loader would be costly to create, that loader can be designed to defer
        the cost until later.

        Finders must return ModuleSpec objects when find_spec() is called.
        This new method replaces find_module() and find_loader() (in the
        PathEntryFinder case). If a loader does not have find_spec(),
        find_module() and find_loader() are used instead, for
        backward-compatibility.
        """
        entry_name = None
        if fullname in self.toc:
            entry_name = fullname
            trace'import %s # PyInstaller PYZ'fullname
        elif path is not None:
            modname = fullname.rsplit('.')[(-1)]
            for p in path:
                p = p[SYS_PREFIXLEN + 1:]
                parts = p.split(pyi_os_path.os_sep)
                if not parts:
                    pass
                else:
                    if not parts[0]:
                        parts = parts[1:]
                    else:
                        parts.append(modname)
                        entry_name = '.'.join(parts)
                    if entry_name in self.toc:
                        trace('import %s as %s # PyInstaller PYZ (__path__ override: %s)', entry_name, fullname, p)
                        break
            else:
                entry_name = None

        if entry_name is None:
            trace'# %s not found in PYZ'fullname
            return
        origin = self.get_filename(entry_name)
        is_pkg = self.is_package(entry_name)
        spec = _frozen_importlib.ModuleSpec(fullname,
          self, is_package=is_pkg,
          origin=origin,
          loader_state=entry_name)
        spec.has_location = True
        return spec

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

    def exec_module(self, module):
        """
        PEP-451 loader.exec_module() method for the ``sys.meta_path`` hook.

        Loaders will have a new method, exec_module(). Its only job is to
        "exec" the module and consequently populate the module's namespace. It
        is not responsible for creating or preparing the module object, nor
        for any cleanup afterward. It has no return value. exec_module() will
        be used during both loading and reloading.

        exec_module() should properly handle the case where it is called more
        than once. For some kinds of modules this may mean raising ImportError
        every time after the first time the method is called. This is
        particularly relevant for reloading, where some kinds of modules do
        not support in-place reloading.
        """
        spec = module.__spec__
        bytecode = self.get_code(spec.loader_state)
        assert hasattrmodule'__file__'
        if spec.submodule_search_locations is not None:
            module.__path__ = [
             pyi_os_path.os_path_dirname(module.__file__)]
        execbytecodemodule.__dict__


class CExtensionImporter(object):
    __doc__ = '\n    PEP-302 hook for sys.meta_path to load Python C extension modules.\n\n    C extension modules are present on the sys.prefix as filenames:\n\n        full.module.name.pyd\n        full.module.name.so\n        full.module.name.cpython-33m.so\n        full.module.name.abi3.so\n    '

    def __init__(self):
        files = pyi_os_path.os_listdir(SYS_PREFIX)
        self._file_cache = set(files)

    def find_module(self, fullname, path=None):
        imp_lock()
        module_loader = None
        for ext in EXTENSION_SUFFIXES:
            if fullname + ext in self._file_cache:
                module_loader = self
                break
        else:
            imp_unlock()
            return module_loader

    def load_module--- This code section failed: ---

 L. 660         0  LOAD_GLOBAL              imp_lock
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 662         6  LOAD_CONST               None
                8  STORE_FAST               'module'

 L. 664     10_12  SETUP_FINALLY       406  'to 406'
            14_16  SETUP_FINALLY       354  'to 354'

 L. 665        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                version_info
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_CONST               2
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   172  'to 172'

 L. 669        32  LOAD_GLOBAL              sys
               34  LOAD_ATTR                modules
               36  LOAD_METHOD              get
               38  LOAD_FAST                'fullname'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'module'

 L. 671        44  LOAD_FAST                'module'
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE   170  'to 170'

 L. 674        52  LOAD_GLOBAL              EXTENSION_SUFFIXES
               54  LOAD_METHOD              iteritems
               56  CALL_METHOD_0         0  ''
               58  GET_ITER         
             60_0  COME_FROM            90  '90'
             60_1  COME_FROM            84  '84'
               60  FOR_ITER             92  'to 92'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'ext'
               66  STORE_FAST               'ext_tuple'

 L. 675        68  LOAD_FAST                'fullname'
               70  LOAD_FAST                'ext'
               72  BINARY_ADD       
               74  STORE_FAST               'filename'

 L. 676        76  LOAD_FAST                'filename'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _file_cache
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE_BACK    60  'to 60'

 L. 677        86  POP_TOP          
               88  BREAK_LOOP           92  'to 92'
               90  JUMP_BACK            60  'to 60'
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            60  '60'

 L. 678        92  LOAD_GLOBAL              pyi_os_path
               94  LOAD_METHOD              os_path_join
               96  LOAD_GLOBAL              SYS_PREFIX
               98  LOAD_FAST                'filename'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'filename'

 L. 679       104  LOAD_GLOBAL              open
              106  LOAD_FAST                'filename'
              108  LOAD_STR                 'rb'
              110  CALL_FUNCTION_2       2  ''
              112  SETUP_WITH          136  'to 136'
              114  STORE_FAST               'fp'

 L. 680       116  LOAD_GLOBAL              imp
              118  LOAD_METHOD              load_module
              120  LOAD_FAST                'fullname'
              122  LOAD_FAST                'fp'
              124  LOAD_FAST                'filename'
              126  LOAD_FAST                'ext_tuple'
              128  CALL_METHOD_4         4  ''
              130  STORE_FAST               'module'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM_WITH      112  '112'
              136  WITH_CLEANUP_START
              138  WITH_CLEANUP_FINISH
              140  END_FINALLY      

 L. 682       142  LOAD_GLOBAL              hasattr
              144  LOAD_FAST                'module'
              146  LOAD_STR                 '__setattr__'
              148  CALL_FUNCTION_2       2  ''
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 683       152  LOAD_FAST                'filename'
              154  LOAD_FAST                'module'
              156  STORE_ATTR               __file__
              158  JUMP_FORWARD        170  'to 170'
            160_0  COME_FROM           150  '150'

 L. 687       160  LOAD_FAST                'filename'
              162  LOAD_FAST                'module'
              164  LOAD_ATTR                __dict__
              166  LOAD_STR                 '__file__'
              168  STORE_SUBSCR     
            170_0  COME_FROM           158  '158'
            170_1  COME_FROM            50  '50'
              170  JUMP_FORWARD        350  'to 350'
            172_0  COME_FROM            30  '30'

 L. 691       172  LOAD_GLOBAL              sys
              174  LOAD_ATTR                modules
              176  LOAD_METHOD              get
              178  LOAD_FAST                'fullname'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'module'

 L. 692       184  LOAD_FAST                'module'
              186  LOAD_CONST               None
              188  COMPARE_OP               is
          190_192  POP_JUMP_IF_FALSE   350  'to 350'

 L. 694       194  LOAD_GLOBAL              EXTENSION_SUFFIXES
              196  GET_ITER         
            198_0  COME_FROM           348  '348'
            198_1  COME_FROM           344  '344'
            198_2  COME_FROM           294  '294'
            198_3  COME_FROM           262  '262'
              198  FOR_ITER            350  'to 350'
              200  STORE_FAST               'ext'

 L. 695       202  LOAD_GLOBAL              pyi_os_path
              204  LOAD_METHOD              os_path_join
              206  LOAD_GLOBAL              SYS_PREFIX
              208  LOAD_FAST                'fullname'
              210  LOAD_FAST                'ext'
              212  BINARY_ADD       
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'filename'

 L. 699       218  SETUP_FINALLY       244  'to 244'

 L. 700       220  LOAD_GLOBAL              open
              222  LOAD_FAST                'filename'
              224  CALL_FUNCTION_1       1  ''
              226  SETUP_WITH          234  'to 234'
              228  POP_TOP          

 L. 701       230  POP_BLOCK        
              232  BEGIN_FINALLY    
            234_0  COME_FROM_WITH      226  '226'
              234  WITH_CLEANUP_START
              236  WITH_CLEANUP_FINISH
              238  END_FINALLY      
              240  POP_BLOCK        
              242  JUMP_FORWARD        270  'to 270'
            244_0  COME_FROM_FINALLY   218  '218'

 L. 702       244  DUP_TOP          
              246  LOAD_GLOBAL              IOError
              248  COMPARE_OP               exception-match
          250_252  POP_JUMP_IF_FALSE   268  'to 268'
              254  POP_TOP          
              256  POP_TOP          
              258  POP_TOP          

 L. 704       260  POP_EXCEPT       
              262  JUMP_BACK           198  'to 198'
              264  POP_EXCEPT       
              266  JUMP_FORWARD        270  'to 270'
            268_0  COME_FROM           250  '250'
              268  END_FINALLY      
            270_0  COME_FROM           266  '266'
            270_1  COME_FROM           242  '242'

 L. 706       270  LOAD_GLOBAL              EXTENSION_LOADER
              272  LOAD_FAST                'fullname'
              274  LOAD_FAST                'filename'
              276  CALL_FUNCTION_2       2  ''
              278  STORE_FAST               'loader'

 L. 707       280  SETUP_FINALLY       296  'to 296'

 L. 708       282  LOAD_FAST                'loader'
              284  LOAD_METHOD              load_module
              286  LOAD_FAST                'fullname'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'module'
              292  POP_BLOCK        
              294  JUMP_BACK           198  'to 198'
            296_0  COME_FROM_FINALLY   280  '280'

 L. 709       296  DUP_TOP          
              298  LOAD_GLOBAL              ImportError
              300  COMPARE_OP               exception-match
          302_304  POP_JUMP_IF_FALSE   346  'to 346'
              306  POP_TOP          
              308  STORE_FAST               'e'
              310  POP_TOP          
              312  SETUP_FINALLY       334  'to 334'

 L. 710       314  LOAD_GLOBAL              ImportError
              316  LOAD_STR                 '%s: %s'
              318  LOAD_FAST                'e'
              320  LOAD_FAST                'fullname'
              322  BUILD_TUPLE_2         2 
              324  BINARY_MODULO    
              326  CALL_FUNCTION_1       1  ''
              328  RAISE_VARARGS_1       1  'exception instance'
              330  POP_BLOCK        
              332  BEGIN_FINALLY    
            334_0  COME_FROM_FINALLY   312  '312'
              334  LOAD_CONST               None
              336  STORE_FAST               'e'
              338  DELETE_FAST              'e'
              340  END_FINALLY      
              342  POP_EXCEPT       
              344  JUMP_BACK           198  'to 198'
            346_0  COME_FROM           302  '302'
              346  END_FINALLY      
              348  JUMP_BACK           198  'to 198'
            350_0  COME_FROM           198  '198'
            350_1  COME_FROM           190  '190'
            350_2  COME_FROM           170  '170'
              350  POP_BLOCK        
              352  JUMP_FORWARD        402  'to 402'
            354_0  COME_FROM_FINALLY    14  '14'

 L. 712       354  DUP_TOP          
              356  LOAD_GLOBAL              Exception
              358  COMPARE_OP               exception-match
          360_362  POP_JUMP_IF_FALSE   400  'to 400'
              364  POP_TOP          
              366  POP_TOP          
              368  POP_TOP          

 L. 714       370  LOAD_FAST                'fullname'
              372  LOAD_GLOBAL              sys
              374  LOAD_ATTR                modules
              376  COMPARE_OP               in
          378_380  POP_JUMP_IF_FALSE   394  'to 394'

 L. 715       382  LOAD_GLOBAL              sys
              384  LOAD_ATTR                modules
              386  LOAD_METHOD              pop
              388  LOAD_FAST                'fullname'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
            394_0  COME_FROM           378  '378'

 L. 716       394  RAISE_VARARGS_0       0  'reraise'
              396  POP_EXCEPT       
              398  JUMP_FORWARD        402  'to 402'
            400_0  COME_FROM           360  '360'
              400  END_FINALLY      
            402_0  COME_FROM           398  '398'
            402_1  COME_FROM           352  '352'
              402  POP_BLOCK        
              404  BEGIN_FINALLY    
            406_0  COME_FROM_FINALLY    10  '10'

 L. 720       406  LOAD_GLOBAL              imp_unlock
              408  CALL_FUNCTION_0       0  ''
              410  POP_TOP          
              412  END_FINALLY      

 L. 722       414  LOAD_FAST                'module'
              416  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 268_0

    def is_package(self, fullname):
        """
        Return always False since C extension modules are never packages.
        """
        return False

    def get_code(self, fullname):
        """
        Return None for a C extension module.
        """
        for ext in EXTENSION_SUFFIXES:
            if fullname + ext in self._file_cache:
                return None
        else:
            raise ImportError('No module named ' + fullname)

    def get_source(self, fullname):
        """
        Return None for a C extension module.
        """
        return self.get_code(fullname)

    def get_data(self, path):
        """
        This returns the data as a string, or raise IOError if the "file"
        wasn't found. The data is always returned as if "binary" mode was used.

        The 'path' argument is a path that can be constructed by munging
        module.__file__ (or pkg.__path__ items)
        """
        with openpath'rb' as fp:
            return fp.read()

    def get_filename(self, fullname):
        """
        This method should return the value that __file__ would be set to
        if the named module was loaded. If the module is not found, then
        ImportError should be raised.
        """
        for ext in EXTENSION_SUFFIXES:
            if fullname + ext in self._file_cache:
                return pyi_os_path.os_path_join(SYS_PREFIX, fullname + ext)
        else:
            raise ImportError('No module named ' + fullname)


def install():
    """
    Install FrozenImporter class and other classes into the import machinery.

    This class method (static method) installs the FrozenImporter class into
    the import machinery of the running process. The importer is added
    to sys.meta_path. It could be added to sys.path_hooks but sys.meta_path
    is processed by Python before looking at sys.path!

    The order of processing import hooks in sys.meta_path:

    1. built-in modules
    2. modules from the bundled ZIP archive
    3. C extension modules
    4. Modules from sys.path
    """
    if sys.version_info[0] == 2:
        sys.meta_path.append(BuiltinImporter())
    fimp = FrozenImporter()
    sys.meta_path.append(fimp)
    if sys.version_info[0] == 2:
        sys.path_hooks.append(fimp)
        sys.meta_path.append(CExtensionImporter())
    else:
        pass
    for item in sys.meta_path:
        if hasattritem'__name__':
            if item.__name__ == 'WindowsRegistryFinder':
                sys.meta_path.remove(item)
                break
    else:
        pathFinders = []
        for item in reversed(sys.meta_path):
            if getattr(item, '__name__', None) == 'PathFinder':
                sys.meta_path.remove(item)
                if item not in pathFinders:
                    pathFinders.append(item)
                sys.meta_path.extend(reversed(pathFinders))