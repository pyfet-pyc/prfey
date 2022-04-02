# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: pkgutil.py
"""Utilities to support packages."""
from collections import namedtuple
from functools import singledispatch as simplegeneric
import importlib, importlib.util, importlib.machinery, os, os.path, sys
from types import ModuleType
import warnings
__all__ = [
 'get_importer', 'iter_importers', 'get_loader', 'find_loader',
 'walk_packages', 'iter_modules', 'get_data',
 'ImpImporter', 'ImpLoader', 'read_code', 'extend_path',
 'ModuleInfo']
ModuleInfo = namedtuple('ModuleInfo', 'module_finder name ispkg')
ModuleInfo.__doc__ = 'A namedtuple with minimal info about a module.'

def _get_spec--- This code section failed: ---

 L.  29         0  SETUP_FINALLY        12  'to 12'

 L.  30         2  LOAD_FAST                'finder'
                4  LOAD_ATTR                find_spec
                6  STORE_FAST               'find_spec'
                8  POP_BLOCK        
               10  JUMP_FORWARD         70  'to 70'
             12_0  COME_FROM_FINALLY     0  '0'

 L.  31        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    68  'to 68'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  32        26  LOAD_FAST                'finder'
               28  LOAD_METHOD              find_module
               30  LOAD_FAST                'name'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'loader'

 L.  33        36  LOAD_FAST                'loader'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L.  34        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            42  '42'

 L.  35        50  LOAD_GLOBAL              importlib
               52  LOAD_ATTR                util
               54  LOAD_METHOD              spec_from_loader
               56  LOAD_FAST                'name'
               58  LOAD_FAST                'loader'
               60  CALL_METHOD_2         2  ''
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM            18  '18'
               68  END_FINALLY      
             70_0  COME_FROM            10  '10'

 L.  37        70  LOAD_FAST                'find_spec'
               72  LOAD_FAST                'name'
               74  CALL_FUNCTION_1       1  ''
               76  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 46


def read_code(stream):
    import marshal
    magic = stream.read4
    if magic != importlib.util.MAGIC_NUMBER:
        return
    stream.read12
    return marshal.loadstream


def walk_packages(path=None, prefix='', onerror=None):
    """Yields ModuleInfo for all modules recursively
    on path, or, if path is None, all accessible modules.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.

    Note that this function must import all *packages* (NOT all
    modules!) on the given path, in order to access the __path__
    attribute to find submodules.

    'onerror' is a function which gets called with one argument (the
    name of the package which was being imported) if any exception
    occurs while trying to import a package.  If no onerror function is
    supplied, ImportErrors are caught and ignored, while all other
    exceptions are propagated, terminating the search.

    Examples:

    # list all modules python can access
    walk_packages()

    # list all submodules of ctypes
    walk_packages(ctypes.__path__, ctypes.__name__+'.')
    """

    def seen(p, m={}):
        if p in m:
            return True
        m[p] = True

    for info in iter_modules(path, prefix):
        (yield info)
        if info.ispkg:
            try:
                __import__(info.name)
            except ImportError:
                if onerror is not None:
                    onerror(info.name)
            except Exception:
                if onerror is not None:
                    onerror(info.name)
                else:
                    raise
            else:
                path = getattr(sys.modules[info.name], '__path__', None) or []
                path = [p for p in path if not seen(p)]
                (yield from walk_packages(path, info.name + '.', onerror))


def iter_modules(path=None, prefix=''):
    """Yields ModuleInfo for all submodules on path,
    or, if path is None, all top-level modules on sys.path.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.
    """
    if path is None:
        importers = iter_importers()
    else:
        if isinstance(path, str):
            raise ValueError('path must be None or list of paths to look for modules in')
        else:
            importers = map(get_importer, path)
    yielded = {}
    for i in importers:
        for name, ispkg in iter_importer_modules(i, prefix):
            if name not in yielded:
                yielded[name] = 1
                (yield ModuleInfo(i, name, ispkg))


@simplegeneric
def iter_importer_modules(importer, prefix=''):
    if not hasattr(importer, 'iter_modules'):
        return []
    return importer.iter_modulesprefix


def _iter_file_finder_modules(importer, prefix=''):
    return importer.path is None or os.path.isdirimporter.path or None
    yielded = {}
    import inspect
    try:
        filenames = os.listdirimporter.path
    except OSError:
        filenames = []
    else:
        filenames.sort()
        for fn in filenames:
            modname = inspect.getmodulenamefn
            if modname == '__init__' or modname in yielded:
                pass
            else:
                path = os.path.join(importer.path, fn)
                ispkg = False
                if not modname:
                    if os.path.isdirpath and '.' not in fn:
                        modname = fn
                        try:
                            dircontents = os.listdirpath
                        except OSError:
                            dircontents = []
                        else:
                            for fn in dircontents:
                                subname = inspect.getmodulenamefn
                                if subname == '__init__':
                                    ispkg = True
                                    break

                elif modname and '.' not in modname:
                    yielded[modname] = 1
                    (yield (prefix + modname, ispkg))


iter_importer_modules.register(importlib.machinery.FileFinder, _iter_file_finder_modules)

def _import_imp():
    global imp
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        imp = importlib.import_module'imp'


class ImpImporter:
    __doc__ = 'PEP 302 Finder that wraps Python\'s "classic" import algorithm\n\n    ImpImporter(dirname) produces a PEP 302 finder that searches that\n    directory.  ImpImporter(None) produces a PEP 302 finder that searches\n    the current sys.path, plus any modules that are frozen or built-in.\n\n    Note that ImpImporter does not currently support being used by placement\n    on sys.meta_path.\n    '

    def __init__(self, path=None):
        warnings.warn("This emulation is deprecated, use 'importlib' instead", DeprecationWarning)
        _import_imp()
        self.path = path

    def find_module(self, fullname, path=None):
        subname = fullname.split'.'[(-1)]
        if subname != fullname:
            if self.path is None:
                return
        elif self.path is None:
            path = None
        else:
            path = [
             os.path.realpathself.path]
        try:
            file, filename, etc = imp.find_module(subname, path)
        except ImportError:
            return
        else:
            return ImpLoader(fullname, file, filename, etc)

    def iter_modules(self, prefix=''):
        return self.path is None or os.path.isdirself.path or None
        yielded = {}
        import inspect
        try:
            filenames = os.listdirself.path
        except OSError:
            filenames = []
        else:
            filenames.sort()
            for fn in filenames:
                modname = inspect.getmodulenamefn
                if modname == '__init__' or modname in yielded:
                    pass
                else:
                    path = os.path.join(self.path, fn)
                    ispkg = False
                    if not modname:
                        if os.path.isdirpath and '.' not in fn:
                            modname = fn
                            try:
                                dircontents = os.listdirpath
                            except OSError:
                                dircontents = []
                            else:
                                for fn in dircontents:
                                    subname = inspect.getmodulenamefn
                                    if subname == '__init__':
                                        ispkg = True
                                        break

                    elif modname and '.' not in modname:
                        yielded[modname] = 1
                        (yield (prefix + modname, ispkg))


class ImpLoader:
    __doc__ = 'PEP 302 Loader that wraps Python\'s "classic" import algorithm\n    '
    code = source = None

    def __init__(self, fullname, file, filename, etc):
        warnings.warn("This emulation is deprecated, use 'importlib' instead", DeprecationWarning)
        _import_imp()
        self.file = file
        self.filename = filename
        self.fullname = fullname
        self.etc = etc

    def load_module(self, fullname):
        self._reopen()
        try:
            mod = imp.load_module(fullname, self.file, self.filename, self.etc)
        finally:
            if self.file:
                self.file.close()

        return mod

    def get_data--- This code section failed: ---

 L. 294         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'pathname'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           32  'to 32'
               10  STORE_FAST               'file'

 L. 295        12  LOAD_FAST                'file'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        8  '8'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    def _reopen(self):
        if self.file:
            if self.file.closed:
                mod_type = self.etc[2]
                if mod_type == imp.PY_SOURCE:
                    self.file = open(self.filename, 'r')
                else:
                    if mod_type in (imp.PY_COMPILED, imp.C_EXTENSION):
                        self.file = open(self.filename, 'rb')

    def _fix_name(self, fullname):
        if fullname is None:
            fullname = self.fullname
        else:
            if fullname != self.fullname:
                raise ImportError('Loader for module %s cannot handle module %s' % (
                 self.fullname, fullname))
        return fullname

    def is_package(self, fullname):
        fullname = self._fix_namefullname
        return self.etc[2] == imp.PKG_DIRECTORY

    def get_code(self, fullname=None):
        fullname = self._fix_namefullname
        if self.code is None:
            mod_type = self.etc[2]
            if mod_type == imp.PY_SOURCE:
                source = self.get_sourcefullname
                self.code = compile(source, self.filename, 'exec')
            else:
                if mod_type == imp.PY_COMPILED:
                    self._reopen()
                    try:
                        self.code = read_code(self.file)
                    finally:
                        self.file.close()

                else:
                    if mod_type == imp.PKG_DIRECTORY:
                        self.code = self._get_delegate().get_code()
        return self.code

    def get_source(self, fullname=None):
        fullname = self._fix_namefullname
        if self.source is None:
            mod_type = self.etc[2]
            if mod_type == imp.PY_SOURCE:
                self._reopen()
                try:
                    self.source = self.file.read()
                finally:
                    self.file.close()

            else:
                if mod_type == imp.PY_COMPILED:
                    if os.path.existsself.filename[:-1]:
                        with open(self.filename[:-1], 'r') as (f):
                            self.source = f.read()
                elif mod_type == imp.PKG_DIRECTORY:
                    self.source = self._get_delegate().get_source()
        return self.source

    def _get_delegate(self):
        finder = ImpImporter(self.filename)
        spec = _get_spec(finder, '__init__')
        return spec.loader

    def get_filename(self, fullname=None):
        fullname = self._fix_namefullname
        mod_type = self.etc[2]
        if mod_type == imp.PKG_DIRECTORY:
            return self._get_delegate().get_filename()
        if mod_type in (imp.PY_SOURCE, imp.PY_COMPILED, imp.C_EXTENSION):
            return self.filename


try:
    import zipimport
    from zipimport import zipimporter

    def iter_zipimport_modules(importer, prefix=''):
        dirlist = sorted(zipimport._zip_directory_cache[importer.archive])
        _prefix = importer.prefix
        plen = len(_prefix)
        yielded = {}
        import inspect
        for fn in dirlist:
            if not fn.startswith_prefix:
                pass
            else:
                fn = fn[plen:].splitos.sep
                if len(fn) == 2:
                    if fn[1].startswith'__init__.py':
                        if fn[0] not in yielded:
                            yielded[fn[0]] = 1
                            (yield (prefix + fn[0], True))
                if len(fn) != 1:
                    pass
                else:
                    modname = inspect.getmodulenamefn[0]
                    if modname == '__init__':
                        pass
                    elif modname and '.' not in modname and modname not in yielded:
                        yielded[modname] = 1
                        (yield (prefix + modname, False))


    iter_importer_modules.register(zipimporter, iter_zipimport_modules)
except ImportError:
    pass
else:

    def get_importer--- This code section failed: ---

 L. 414         0  SETUP_FINALLY        16  'to 16'

 L. 415         2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                path_importer_cache
                6  LOAD_FAST                'path_item'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'importer'
               12  POP_BLOCK        
               14  JUMP_FORWARD        106  'to 106'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 416        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE   104  'to 104'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 417        30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                path_hooks
               34  GET_ITER         
               36  FOR_ITER             96  'to 96'
               38  STORE_FAST               'path_hook'

 L. 418        40  SETUP_FINALLY        74  'to 74'

 L. 419        42  LOAD_FAST                'path_hook'
               44  LOAD_FAST                'path_item'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'importer'

 L. 420        50  LOAD_GLOBAL              sys
               52  LOAD_ATTR                path_importer_cache
               54  LOAD_METHOD              setdefault
               56  LOAD_FAST                'path_item'
               58  LOAD_FAST                'importer'
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          

 L. 421        64  POP_BLOCK        
               66  POP_TOP          
               68  JUMP_ABSOLUTE       100  'to 100'
               70  POP_BLOCK        
               72  JUMP_BACK            36  'to 36'
             74_0  COME_FROM_FINALLY    40  '40'

 L. 422        74  DUP_TOP          
               76  LOAD_GLOBAL              ImportError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    92  'to 92'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 423        88  POP_EXCEPT       
               90  JUMP_BACK            36  'to 36'
             92_0  COME_FROM            80  '80'
               92  END_FINALLY      
               94  JUMP_BACK            36  'to 36'

 L. 425        96  LOAD_CONST               None
               98  STORE_FAST               'importer'
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            22  '22'
              104  END_FINALLY      
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            14  '14'

 L. 426       106  LOAD_FAST                'importer'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 68


    def iter_importers(fullname=''):
        """Yield finders for the given module name

    If fullname contains a '.', the finders will be for the package
    containing fullname, otherwise they will be all registered top level
    finders (i.e. those on both sys.meta_path and sys.path_hooks).

    If the named module is in a package, that package is imported as a side
    effect of invoking this function.

    If no module name is specified, all top level finders are produced.
    """
        if fullname.startswith'.':
            msg = 'Relative module name {!r} not supported'.formatfullname
            raise ImportError(msg)
        elif '.' in fullname:
            pkg_name = fullname.rpartition'.'[0]
            pkg = importlib.import_modulepkg_name
            path = getattr(pkg, '__path__', None)
            if path is None:
                return
        else:
            (yield from sys.meta_path)
            path = sys.path
        for item in path:
            (yield get_importer(item))


    def get_loader(module_or_name):
        """Get a "loader" object for module_or_name

    Returns None if the module cannot be found or imported.
    If the named module is not already imported, its containing package
    (if any) is imported, in order to establish the package __path__.
    """
        if module_or_name in sys.modules:
            module_or_name = sys.modules[module_or_name]
            if module_or_name is None:
                return
        elif isinstance(module_or_name, ModuleType):
            module = module_or_name
            loader = getattr(module, '__loader__', None)
            if loader is not None:
                return loader
            if getattr(module, '__spec__', None) is None:
                return
            fullname = module.__name__
        else:
            fullname = module_or_name
        return find_loader(fullname)


    def find_loader(fullname):
        """Find a "loader" object for fullname

    This is a backwards compatibility wrapper around
    importlib.util.find_spec that converts most failures to ImportError
    and only returns the loader rather than the full spec
    """
        if fullname.startswith'.':
            msg = 'Relative module name {!r} not supported'.formatfullname
            raise ImportError(msg)
        try:
            spec = importlib.util.find_specfullname
        except (ImportError, AttributeError, TypeError, ValueError) as ex:
            try:
                msg = 'Error while finding loader for {!r} ({}: {})'
                raise ImportError(msg.format(fullname, type(ex), ex)) from ex
            finally:
                ex = None
                del ex

        else:
            if spec is not None:
                return spec.loader


    def extend_path(path, name):
        """Extend a package's path.

    Intended use is to place the following code in a package's __init__.py:

        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)

    This will add to the package's __path__ all subdirectories of
    directories on sys.path named after the package.  This is useful
    if one wants to distribute different parts of a single logical
    package as multiple directories.

    It also looks for *.pkg files beginning where * matches the name
    argument.  This feature is similar to *.pth files (see site.py),
    except that it doesn't special-case lines starting with 'import'.
    A *.pkg file is trusted at face value: apart from checking for
    duplicates, all entries found in a *.pkg file are added to the
    path, regardless of whether they are exist the filesystem.  (This
    is a feature.)

    If the input path is not a list (as is the case for frozen
    packages) it is returned unchanged.  The input path is not
    modified; an extended copy is returned.  Items are only appended
    to the copy at the end.

    It is assumed that sys.path is a sequence.  Items of sys.path that
    are not (unicode or 8-bit) strings referring to existing
    directories are ignored.  Unicode items of sys.path that cause
    errors when used as filenames may cause this function to raise an
    exception (in line with os.path.isdir() behavior).
    """
        if not isinstance(path, list):
            return path
            sname_pkg = name + '.pkg'
            path = path[:]
            parent_package, _, final_name = name.rpartition'.'
            if parent_package:
                try:
                    search_path = sys.modules[parent_package].__path__
                except (KeyError, AttributeError):
                    return path

            else:
                search_path = sys.path
            for dir in search_path:
                if not isinstance(dir, str):
                    pass
                else:
                    finder = get_importer(dir)
                    if finder is not None:
                        portions = []
                        if hasattr(finder, 'find_spec'):
                            spec = finder.find_specfinal_name
                            if spec is not None:
                                portions = spec.submodule_search_locations or []

        else:
            if hasattr(finder, 'find_loader'):
                _, portions = finder.find_loaderfinal_name
        for portion in portions:
            if portion not in path:
                path.appendportion
            else:
                pkgfile = os.path.join(dir, sname_pkg)
                if os.path.isfilepkgfile:
                    try:
                        f = open(pkgfile)
                    except OSError as msg:
                        try:
                            sys.stderr.write("Can't open %s: %s\n" % (
                             pkgfile, msg))
                        finally:
                            msg = None
                            del msg

                    else:
                        with f:
                            for line in f:
                                line = line.rstrip'\n'

                            if line:
                                if line.startswith'#':
                                    pass
                                else:
                                    path.appendline
                return path


    def get_data(package, resource):
        """Get a resource from a package.

    This is a wrapper round the PEP 302 loader get_data API. The package
    argument should be the name of a package, in standard module format
    (foo.bar). The resource argument should be in the form of a relative
    filename, using '/' as the path separator. The parent directory name '..'
    is not allowed, and nor is a rooted name (starting with a '/').

    The function returns a binary string, which is the contents of the
    specified resource.

    For packages located in the filesystem, which have already been imported,
    this is the rough equivalent of

        d = os.path.dirname(sys.modules[package].__file__)
        data = open(os.path.join(d, resource), 'rb').read()

    If the package cannot be located or loaded, or it uses a PEP 302 loader
    which does not support get_data(), then None is returned.
    """
        spec = importlib.util.find_specpackage
        if spec is None:
            return
        else:
            loader = spec.loader
            return loader is None or hasattr(loader, 'get_data') or None
            mod = sys.modules.getpackage or importlib._bootstrap._loadspec
            return mod is None or hasattr(mod, '__file__') or None
        parts = resource.split'/'
        parts.insert(0, os.path.dirnamemod.__file__)
        resource_name = (os.path.join)(*parts)
        return loader.get_dataresource_name