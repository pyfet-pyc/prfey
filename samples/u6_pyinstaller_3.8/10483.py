# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\util.py
"""Utility code for constructing importers, etc."""
from . import abc
from ._bootstrap import module_from_spec
from ._bootstrap import _resolve_name
from ._bootstrap import spec_from_loader
from ._bootstrap import _find_spec
from ._bootstrap_external import MAGIC_NUMBER
from ._bootstrap_external import _RAW_MAGIC_NUMBER
from ._bootstrap_external import cache_from_source
from ._bootstrap_external import decode_source
from ._bootstrap_external import source_from_cache
from ._bootstrap_external import spec_from_file_location
from contextlib import contextmanager
import _imp, functools, sys, types, warnings

def source_hash(source_bytes):
    """Return the hash of *source_bytes* as used in hash-based pyc files."""
    return _imp.source_hash(_RAW_MAGIC_NUMBER, source_bytes)


def resolve_name(name, package):
    """Resolve a relative module name to an absolute one."""
    if not name.startswith('.'):
        return name
    if not package:
        raise ValueError(f"no package specified for {repr(name)} (required for relative module names)")
    level = 0
    for character in name:
        if character != '.':
            break
        level += 1
    else:
        return _resolve_name(name[level:], package, level)


def _find_spec_from_path(name, path=None):
    """Return the spec for the specified module.

    First, sys.modules is checked to see if the module was already imported. If
    so, then sys.modules[name].__spec__ is returned. If that happens to be
    set to None, then ValueError is raised. If the module is not in
    sys.modules, then sys.meta_path is searched for a suitable spec with the
    value of 'path' given to the finders. None is returned if no spec could
    be found.

    Dotted names do not have their parent packages implicitly imported. You will
    most likely need to explicitly import all parent packages in the proper
    order for a submodule to get the correct spec.

    """
    if name not in sys.modules:
        return _find_spec(name, path)
        module = sys.modules[name]
        if module is None:
            return
    else:
        try:
            spec = module.__spec__
        except AttributeError:
            raise ValueError('{}.__spec__ is not set'.format(name)) from None
        else:
            if spec is None:
                raise ValueError('{}.__spec__ is None'.format(name))
            return spec


def find_spec(name, package=None):
    """Return the spec for the specified module.

    First, sys.modules is checked to see if the module was already imported. If
    so, then sys.modules[name].__spec__ is returned. If that happens to be
    set to None, then ValueError is raised. If the module is not in
    sys.modules, then sys.meta_path is searched for a suitable spec with the
    value of 'path' given to the finders. None is returned if no spec could
    be found.

    If the name is for submodule (contains a dot), the parent module is
    automatically imported.

    The name and package arguments work the same as importlib.import_module().
    In other words, relative module names (with leading dots) work.

    """
    fullname = resolve_name(name, package) if name.startswith('.') else name
    if fullname not in sys.modules:
        parent_name = fullname.rpartition('.')[0]
        if parent_name:
            parent = __import__(parent_name, fromlist=['__path__'])
            try:
                parent_path = parent.__path__
            except AttributeError as e:
                try:
                    raise ModuleNotFoundError(f"__path__ attribute not found on {parent_name!r} while trying to find {fullname!r}",
                      name=fullname) from e
                finally:
                    e = None
                    del e

        else:
            parent_path = None
        return _find_spec(fullname, parent_path)
    module = sys.modules[fullname]
    if module is None:
        return
    try:
        spec = module.__spec__
    except AttributeError:
        raise ValueError('{}.__spec__ is not set'.format(name)) from None
    else:
        if spec is None:
            raise ValueError('{}.__spec__ is None'.format(name))
        return spec


@contextmanager
def _module_to_load(name):
    is_reload = name in sys.modules
    module = sys.modules.get(name)
    if not is_reload:
        module = type(sys)(name)
        module.__initializing__ = True
        sys.modules[name] = module
    try:
        try:
            (yield module)
        except Exception:
            if not is_reload:
                try:
                    del sys.modules[name]
                except KeyError:
                    pass

    finally:
        module.__initializing__ = False


def set_package(fxn):
    """Set __package__ on the returned module.

    This function is deprecated.

    """

    @functools.wraps(fxn)
    def set_package_wrapper(*args, **kwargs):
        warnings.warn('The import system now takes care of this automatically.', DeprecationWarning,
          stacklevel=2)
        module = fxn(*args, **kwargs)
        if getattr(module, '__package__', None) is None:
            module.__package__ = module.__name__
            if not hasattr(module, '__path__'):
                module.__package__ = module.__package__.rpartition('.')[0]
        return module

    return set_package_wrapper


def set_loader(fxn):
    """Set __loader__ on the returned module.

    This function is deprecated.

    """

    @functools.wraps(fxn)
    def set_loader_wrapper(self, *args, **kwargs):
        warnings.warn('The import system now takes care of this automatically.', DeprecationWarning,
          stacklevel=2)
        module = fxn(self, *args, **kwargs)
        if getattr(module, '__loader__', None) is None:
            module.__loader__ = self
        return module

    return set_loader_wrapper


def module_for_loader(fxn):
    """Decorator to handle selecting the proper module for loaders.

    The decorated function is passed the module to use instead of the module
    name. The module passed in to the function is either from sys.modules if
    it already exists or is a new module. If the module is new, then __name__
    is set the first argument to the method, __loader__ is set to self, and
    __package__ is set accordingly (if self.is_package() is defined) will be set
    before it is passed to the decorated function (if self.is_package() does
    not work for the module it will be set post-load).

    If an exception is raised and the decorator created the module it is
    subsequently removed from sys.modules.

    The decorator assumes that the decorated function takes the module name as
    the second argument.

    """
    warnings.warn('The import system now takes care of this automatically.', DeprecationWarning,
      stacklevel=2)

    @functools.wraps(fxn)
    def module_for_loader_wrapper--- This code section failed: ---

 L. 202         0  LOAD_GLOBAL              _module_to_load
                2  LOAD_FAST                'fullname'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH          114  'to 114'
                8  STORE_FAST               'module'

 L. 203        10  LOAD_FAST                'self'
               12  LOAD_FAST                'module'
               14  STORE_ATTR               __loader__

 L. 204        16  SETUP_FINALLY        32  'to 32'

 L. 205        18  LOAD_FAST                'self'
               20  LOAD_METHOD              is_package
               22  LOAD_FAST                'fullname'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'is_package'
               28  POP_BLOCK        
               30  JUMP_FORWARD         56  'to 56'
             32_0  COME_FROM_FINALLY    16  '16'

 L. 206        32  DUP_TOP          
               34  LOAD_GLOBAL              ImportError
               36  LOAD_GLOBAL              AttributeError
               38  BUILD_TUPLE_2         2 
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    54  'to 54'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 207        50  POP_EXCEPT       
               52  JUMP_FORWARD         84  'to 84'
             54_0  COME_FROM            42  '42'
               54  END_FINALLY      
             56_0  COME_FROM            30  '30'

 L. 209        56  LOAD_FAST                'is_package'
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 210        60  LOAD_FAST                'fullname'
               62  LOAD_FAST                'module'
               64  STORE_ATTR               __package__
               66  JUMP_FORWARD         84  'to 84'
             68_0  COME_FROM            58  '58'

 L. 212        68  LOAD_FAST                'fullname'
               70  LOAD_METHOD              rpartition
               72  LOAD_STR                 '.'
               74  CALL_METHOD_1         1  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'module'
               82  STORE_ATTR               __package__
             84_0  COME_FROM            66  '66'
             84_1  COME_FROM            52  '52'

 L. 214        84  LOAD_DEREF               'fxn'
               86  LOAD_FAST                'self'
               88  LOAD_FAST                'module'
               90  BUILD_TUPLE_2         2 
               92  LOAD_FAST                'args'
               94  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               96  LOAD_FAST                'kwargs'
               98  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              100  POP_BLOCK        
              102  ROT_TWO          
              104  BEGIN_FINALLY    
              106  WITH_CLEANUP_START
              108  WITH_CLEANUP_FINISH
              110  POP_FINALLY           0  ''
              112  RETURN_VALUE     
            114_0  COME_FROM_WITH        6  '6'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 102

    return module_for_loader_wrapper


class _LazyModule(types.ModuleType):
    __doc__ = 'A subclass of the module type which triggers loading upon attribute access.'

    def __getattribute__(self, attr):
        """Trigger the load of the module and return the attribute."""
        self.__class__ = types.ModuleType
        original_name = self.__spec__.name
        attrs_then = self.__spec__.loader_state['__dict__']
        original_type = self.__spec__.loader_state['__class__']
        attrs_now = self.__dict__
        attrs_updated = {}
        for key, value in attrs_now.items():
            if key not in attrs_then:
                attrs_updated[key] = value
            else:
                if id(attrs_now[key]) != id(attrs_then[key]):
                    attrs_updated[key] = value
                self.__spec__.loader.exec_module(self)
                if original_name in sys.modules:
                    if id(self) != id(sys.modules[original_name]):
                        raise ValueError(f"module object for {original_name!r} substituted in sys.modules during a lazy load")
                self.__dict__.update(attrs_updated)
                return getattr(self, attr)

    def __delattr__(self, attr):
        """Trigger the load and then perform the deletion."""
        self.__getattribute__(attr)
        delattr(self, attr)


class LazyLoader(abc.Loader):
    __doc__ = 'A loader that creates a module which defers loading until attribute access.'

    @staticmethod
    def __check_eager_loader(loader):
        if not hasattr(loader, 'exec_module'):
            raise TypeError('loader must define exec_module()')

    @classmethod
    def factory(cls, loader):
        """Construct a callable which returns the eager loader made lazy."""
        cls._LazyLoader__check_eager_loader(loader)
        return lambda *args, **kwargs: cls(loader(*args, **kwargs))

    def __init__(self, loader):
        self._LazyLoader__check_eager_loader(loader)
        self.loader = loader

    def create_module(self, spec):
        return self.loader.create_module(spec)

    def exec_module(self, module):
        """Make the module load lazily."""
        module.__spec__.loader = self.loader
        module.__loader__ = self.loader
        loader_state = {}
        loader_state['__dict__'] = module.__dict__.copy()
        loader_state['__class__'] = module.__class__
        module.__spec__.loader_state = loader_state
        module.__class__ = _LazyModule