# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: c:\users\farhad\appdata\local\programs\python\python38-32\lib\site-packages\PyInstaller\loader\pyimod03_importers.py
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
              6_0  COME_FROM           116  '116'
              6_1  COME_FROM           112  '112'
              6_2  COME_FROM           108  '108'
              6_3  COME_FROM            90  '90'
              6_4  COME_FROM            86  '86'
                6  FOR_ITER            118  'to 118'
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
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    92  'to 92'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 118        84  POP_EXCEPT       
               86  JUMP_BACK             6  'to 6'
               88  POP_EXCEPT       
               90  JUMP_BACK             6  'to 6'
             92_0  COME_FROM            76  '76'

 L. 119        92  DUP_TOP          
               94  LOAD_GLOBAL              ArchiveReadError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   114  'to 114'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 121       106  POP_EXCEPT       
              108  JUMP_BACK             6  'to 6'
              110  POP_EXCEPT       
              112  JUMP_BACK             6  'to 6'
            114_0  COME_FROM            98  '98'
              114  END_FINALLY      
              116  JUMP_BACK             6  'to 6'
            118_0  COME_FROM             6  '6'

 L. 124       118  LOAD_GLOBAL              ImportError
              120  LOAD_STR                 "Can't load frozen modules."
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `DUP_TOP' instruction at offset 70

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
        module = None
        if entry_name is None:
            entry_name = fullname
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
        else:
            return module

    def is_package--- This code section failed: ---

 L. 282         0  LOAD_FAST                'fullname'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                toc
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    76  'to 76'

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
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    72  'to 72'
               34  POP_TOP          
               36  STORE_FAST               'e'
               38  POP_TOP          
               40  SETUP_FINALLY        60  'to 60'

 L. 286        42  LOAD_GLOBAL              ImportError

 L. 287        44  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               46  LOAD_FAST                'fullname'
               48  BINARY_ADD       

 L. 286        50  CALL_FUNCTION_1       1  ''

 L. 288        52  LOAD_FAST                'e'

 L. 286        54  RAISE_VARARGS_2       2  'exception instance with __cause__'
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_FINALLY    40  '40'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_FORWARD         88  'to 88'
             72_0  COME_FROM            32  '32'
               72  END_FINALLY      
               74  JUMP_FORWARD         88  'to 88'
             76_0  COME_FROM             8  '8'

 L. 290        76  LOAD_GLOBAL              ImportError
               78  LOAD_STR                 'Loader FrozenImporter cannot handle module '
               80  LOAD_FAST                'fullname'
               82  BINARY_ADD       
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            74  '74'
             88_1  COME_FROM            70  '70'

Parse error at or near `JUMP_FORWARD' instruction at offset 74

    def get_code(self, fullname):
        """
        Get the code object associated with the module.

        ImportError should be raised if module not found.
        """
        try:
            return self._pyz_archive.extract(fullname)[1]
            except Exception as e:
            try:
                raise ImportError('Loader FrozenImporter cannot handle module ' + fullname) from e
            finally:
                e = None
                del e

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
            return fp.read

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
    fimp = FrozenImporter()
    sys.meta_path.append(fimp)
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
        else:
            sys.meta_path.extend(reversed(pathFinders))