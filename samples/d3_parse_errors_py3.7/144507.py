# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\_bootstrap.py
"""Core implementation of import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
_bootstrap_external = None

def _wrap(new, old):
    """Simple substitute for functools.update_wrapper."""
    for replace in ('__module__', '__name__', '__qualname__', '__doc__'):
        if hasattr(old, replace):
            setattr(new, replace, getattr(old, replace))

    new.__dict__.update(old.__dict__)


def _new_module(name):
    return type(sys)(name)


_module_locks = {}
_blocking_on = {}

class _DeadlockError(RuntimeError):
    pass


class _ModuleLock:
    __doc__ = 'A recursive lock implementation which is able to detect deadlocks\n    (e.g. thread 1 trying to take locks A then B, and thread 2 trying to\n    take locks B then A).\n    '

    def __init__(self, name):
        self.lock = _thread.allocate_lock()
        self.wakeup = _thread.allocate_lock()
        self.name = name
        self.owner = None
        self.count = 0
        self.waiters = 0

    def has_deadlock(self):
        me = _thread.get_ident()
        tid = self.owner
        while 1:
            lock = _blocking_on.get(tid)
            if lock is None:
                return False
            tid = lock.owner
            if tid == me:
                return True

    def acquire(self):
        """
        Acquire the module lock.  If a potential deadlock is detected,
        a _DeadlockError is raised.
        Otherwise, the lock is always acquired and True is returned.
        """
        tid = _thread.get_ident()
        _blocking_on[tid] = self
        try:
            while True:
                with self.lock:
                    if self.count == 0 or (self.owner == tid):
                        self.owner = tid
                        self.count += 1
                        return True
                    if self.has_deadlock():
                        raise _DeadlockError('deadlock detected by %r' % self)
                    if self.wakeup.acquire(False):
                        self.waiters += 1
                self.wakeup.acquire()
                self.wakeup.release()

        finally:
            del _blocking_on[tid]

    def release(self):
        tid = _thread.get_ident()
        with self.lock:
            if self.owner != tid:
                raise RuntimeError('cannot release un-acquired lock')
            assert self.count > 0
            self.count -= 1
            if self.count == 0:
                self.owner = None
                if self.waiters:
                    self.waiters -= 1
                    self.wakeup.release()

    def __repr__(self):
        return '_ModuleLock({!r}) at {}'.format(self.name, id(self))


class _DummyModuleLock:
    __doc__ = 'A simple _ModuleLock equivalent for Python builds without\n    multi-threading support.'

    def __init__(self, name):
        self.name = name
        self.count = 0

    def acquire(self):
        self.count += 1
        return True

    def release(self):
        if self.count == 0:
            raise RuntimeError('cannot release un-acquired lock')
        self.count -= 1

    def __repr__(self):
        return '_DummyModuleLock({!r}) at {}'.format(self.name, id(self))


class _ModuleLockManager:

    def __init__(self, name):
        self._name = name
        self._lock = None

    def __enter__(self):
        self._lock = _get_module_lock(self._name)
        self._lock.acquire()

    def __exit__(self, *args, **kwargs):
        self._lock.release()


def _get_module_lock(name):
    """Get or create the module lock for a given module name.

    Acquire/release internally the global import lock to protect
    _module_locks."""
    _imp.acquire_lock()
    try:
        try:
            lock = _module_locks[name]()
        except KeyError:
            lock = None

        if lock is None:
            if _thread is None:
                lock = _DummyModuleLock(name)
            else:
                lock = _ModuleLock(name)

            def cb(ref, name=name):
                _imp.acquire_lock()
                try:
                    if _module_locks.get(name) is ref:
                        del _module_locks[name]
                finally:
                    _imp.release_lock()

            _module_locks[name] = _weakref.ref(lock, cb)
    finally:
        _imp.release_lock()

    return lock


def _lock_unlock_module(name):
    """Acquires then releases the module lock for a given module name.

    This is used to ensure a module is completely initialized, in the
    event it is being imported by another thread.
    """
    lock = _get_module_lock(name)
    try:
        lock.acquire()
    except _DeadlockError:
        pass
    else:
        lock.release()


def _call_with_frames_removed(f, *args, **kwds):
    """remove_importlib_frames in import.c will always remove sequences
    of importlib frames that end with a call to this function

    Use it instead of a normal call in places where including the importlib
    frames introduces unwanted noise into the traceback (e.g. when executing
    module code)
    """
    return f(*args, **kwds)


def _verbose_message(message, *args, verbosity=1):
    """Print the message to stderr if -v/PYTHONVERBOSE is turned on."""
    if sys.flags.verbose >= verbosity:
        if not message.startswith(('#', 'import ')):
            message = '# ' + message
        print((message.format)(*args), file=(sys.stderr))


def _requires_builtin(fxn):
    """Decorator to verify the named module is built-in."""

    def _requires_builtin_wrapper(self, fullname):
        if fullname not in sys.builtin_module_names:
            raise ImportError(('{!r} is not a built-in module'.format(fullname)), name=fullname)
        return fxn(self, fullname)

    _wrap(_requires_builtin_wrapper, fxn)
    return _requires_builtin_wrapper


def _requires_frozen(fxn):
    """Decorator to verify the named module is frozen."""

    def _requires_frozen_wrapper(self, fullname):
        if not _imp.is_frozen(fullname):
            raise ImportError(('{!r} is not a frozen module'.format(fullname)), name=fullname)
        return fxn(self, fullname)

    _wrap(_requires_frozen_wrapper, fxn)
    return _requires_frozen_wrapper


def _load_module_shim(self, fullname):
    """Load the specified module into sys.modules and return it.

    This method is deprecated.  Use loader.exec_module instead.

    """
    spec = spec_from_loader(fullname, self)
    if fullname in sys.modules:
        module = sys.modules[fullname]
        _exec(spec, module)
        return sys.modules[fullname]
    return _load(spec)


def _module_repr(module):
    loader = getattr(module, '__loader__', None)
    if hasattr(loader, 'module_repr'):
        try:
            return loader.module_repr(module)
        except Exception:
            pass

    try:
        spec = module.__spec__
    except AttributeError:
        pass
    else:
        if spec is not None:
            return _module_repr_from_spec(spec)

    try:
        name = module.__name__
    except AttributeError:
        name = '?'

    try:
        filename = module.__file__
    except AttributeError:
        if loader is None:
            return '<module {!r}>'.format(name)
        else:
            return '<module {!r} ({!r})>'.format(name, loader)
    else:
        return '<module {!r} from {!r}>'.format(name, filename)


class _installed_safely:

    def __init__(self, module):
        self._module = module
        self._spec = module.__spec__

    def __enter__(self):
        self._spec._initializing = True
        sys.modules[self._spec.name] = self._module

    def __exit__(self, *args):
        try:
            spec = self._spec
            if any((arg is not None for arg in args)):
                try:
                    del sys.modules[spec.name]
                except KeyError:
                    pass

            else:
                _verbose_message('import {!r} # {!r}', spec.name, spec.loader)
        finally:
            self._spec._initializing = False


class ModuleSpec:
    __doc__ = 'The specification for a module, used for loading.\n\n    A module\'s spec is the source for information about the module.  For\n    data associated with the module, including source, use the spec\'s\n    loader.\n\n    `name` is the absolute name of the module.  `loader` is the loader\n    to use when loading the module.  `parent` is the name of the\n    package the module is in.  The parent is derived from the name.\n\n    `is_package` determines if the module is considered a package or\n    not.  On modules this is reflected by the `__path__` attribute.\n\n    `origin` is the specific location used by the loader from which to\n    load the module, if that information is available.  When filename is\n    set, origin will match.\n\n    `has_location` indicates that a spec\'s "origin" reflects a location.\n    When this is True, `__file__` attribute of the module is set.\n\n    `cached` is the location of the cached bytecode file, if any.  It\n    corresponds to the `__cached__` attribute.\n\n    `submodule_search_locations` is the sequence of path entries to\n    search when importing submodules.  If set, is_package should be\n    True--and False otherwise.\n\n    Packages are simply modules that (may) have submodules.  If a spec\n    has a non-None value in `submodule_search_locations`, the import\n    system will consider modules loaded from the spec as packages.\n\n    Only finders (see importlib.abc.MetaPathFinder and\n    importlib.abc.PathEntryFinder) should modify ModuleSpec instances.\n\n    '

    def __init__(self, name, loader, *, origin=None, loader_state=None, is_package=None):
        self.name = name
        self.loader = loader
        self.origin = origin
        self.loader_state = loader_state
        self.submodule_search_locations = [] if is_package else None
        self._set_fileattr = False
        self._cached = None

    def __repr__(self):
        args = [
         'name={!r}'.format(self.name),
         'loader={!r}'.format(self.loader)]
        if self.origin is not None:
            args.append('origin={!r}'.format(self.origin))
        if self.submodule_search_locations is not None:
            args.append('submodule_search_locations={}'.format(self.submodule_search_locations))
        return '{}({})'.format(self.__class__.__name__, ', '.join(args))

    def __eq__(self, other):
        smsl = self.submodule_search_locations
        try:
            return self.name == other.name and self.loader == other.loader and self.origin == other.origin and smsl == other.submodule_search_locations and self.cached == other.cached and self.has_location == other.has_location
        except AttributeError:
            return False

    @property
    def cached(self):
        global _bootstrap_external
        if self._cached is None:
            if self.origin is not None:
                if self._set_fileattr:
                    if _bootstrap_external is None:
                        raise NotImplementedError
                    self._cached = _bootstrap_external._get_cached(self.origin)
        return self._cached

    @cached.setter
    def cached(self, cached):
        self._cached = cached

    @property
    def parent(self):
        """The name of the module's parent."""
        if self.submodule_search_locations is None:
            return self.name.rpartition('.')[0]
        return self.name

    @property
    def has_location(self):
        return self._set_fileattr

    @has_location.setter
    def has_location(self, value):
        self._set_fileattr = bool(value)


def spec_from_loader(name, loader, *, origin=None, is_package=None):
    """Return a module spec based on various loader methods."""
    if hasattr(loader, 'get_filename'):
        if _bootstrap_external is None:
            raise NotImplementedError
        spec_from_file_location = _bootstrap_external.spec_from_file_location
        if is_package is None:
            return spec_from_file_location(name, loader=loader)
        search = [] if is_package else None
        return spec_from_file_location(name, loader=loader, submodule_search_locations=search)
    if is_package is None:
        if hasattr(loader, 'is_package'):
            try:
                is_package = loader.is_package(name)
            except ImportError:
                is_package = None

        else:
            is_package = False
    return ModuleSpec(name, loader, origin=origin, is_package=is_package)


def _spec_from_module(module, loader=None, origin=None):
    try:
        spec = module.__spec__
    except AttributeError:
        pass
    else:
        if spec is not None:
            return spec

    name = module.__name__
    if loader is None:
        try:
            loader = module.__loader__
        except AttributeError:
            pass

        try:
            location = module.__file__
        except AttributeError:
            location = None

        if origin is None:
            if location is None:
                try:
                    origin = loader._ORIGIN
                except AttributeError:
                    origin = None

            else:
                origin = location
        try:
            cached = module.__cached__
        except AttributeError:
            cached = None

        try:
            submodule_search_locations = list(module.__path__)
        except AttributeError:
            submodule_search_locations = None

        spec = ModuleSpec(name, loader, origin=origin)
        spec._set_fileattr = False if location is None else True
        spec.cached = cached
        spec.submodule_search_locations = submodule_search_locations
        return spec


def _init_module_attrs(spec, module, *, override=False):
    if override or getattr(module, '__name__', None) is None:
        try:
            module.__name__ = spec.name
        except AttributeError:
            pass

        if override or (getattr(module, '__loader__', None) is None):
            loader = spec.loader
            if loader is None:
                if spec.submodule_search_locations is not None:
                    if _bootstrap_external is None:
                        raise NotImplementedError
                    _NamespaceLoader = _bootstrap_external._NamespaceLoader
                    loader = _NamespaceLoader.__new__(_NamespaceLoader)
                    loader._path = spec.submodule_search_locations
                    spec.loader = loader
                    module.__file__ = None
        try:
            module.__loader__ = loader
        except AttributeError:
            pass

        if override or (getattr(module, '__package__', None) is None):
            try:
                module.__package__ = spec.parent
            except AttributeError:
                pass

        try:
            module.__spec__ = spec
        except AttributeError:
            pass

        if override or (getattr(module, '__path__', None) is None):
            if spec.submodule_search_locations is not None:
                try:
                    module.__path__ = spec.submodule_search_locations
                except AttributeError:
                    pass

        if not spec.has_location or override or getattr(module, '__file__', None) is None:
            try:
                module.__file__ = spec.origin
            except AttributeError:
                pass

            if override or (getattr(module, '__cached__', None) is None):
                if spec.cached is not None:
                    try:
                        module.__cached__ = spec.cached
                    except AttributeError:
                        pass

        return module


def module_from_spec(spec):
    """Create a module based on the provided spec."""
    module = None
    if hasattr(spec.loader, 'create_module'):
        module = spec.loader.create_module(spec)
    elif hasattr(spec.loader, 'exec_module'):
        raise ImportError('loaders that define exec_module() must also define create_module()')
    if module is None:
        module = _new_module(spec.name)
    _init_module_attrs(spec, module)
    return module


def _module_repr_from_spec(spec):
    """Return the repr to use for the module."""
    name = '?' if spec.name is None else spec.name
    if spec.origin is None:
        if spec.loader is None:
            return '<module {!r}>'.format(name)
        return '<module {!r} ({!r})>'.format(name, spec.loader)
    else:
        if spec.has_location:
            return '<module {!r} from {!r}>'.format(name, spec.origin)
        return '<module {!r} ({})>'.format(spec.name, spec.origin)


def _exec(spec, module):
    """Execute the spec's specified module in an existing module's namespace."""
    name = spec.name
    with _ModuleLockManager(name):
        if sys.modules.get(name) is not module:
            msg = 'module {!r} not in sys.modules'.format(name)
            raise ImportError(msg, name=name)
        if spec.loader is None:
            if spec.submodule_search_locations is None:
                raise ImportError('missing loader', name=(spec.name))
            _init_module_attrs(spec, module, override=True)
            return module
        _init_module_attrs(spec, module, override=True)
        if not hasattr(spec.loader, 'exec_module'):
            spec.loader.load_module(name)
        else:
            spec.loader.exec_module(module)
    return sys.modules[name]


def _load_backward_compatible(spec):
    spec.loader.load_module(spec.name)
    module = sys.modules[spec.name]
    if getattr(module, '__loader__', None) is None:
        try:
            module.__loader__ = spec.loader
        except AttributeError:
            pass

        if getattr(module, '__package__', None) is None:
            try:
                module.__package__ = module.__name__
                if not hasattr(module, '__path__'):
                    module.__package__ = spec.name.rpartition('.')[0]
            except AttributeError:
                pass

    if getattr(module, '__spec__', None) is None:
        try:
            module.__spec__ = spec
        except AttributeError:
            pass

        return module


def _load_unlocked(spec):
    if spec.loader is not None:
        if not hasattr(spec.loader, 'exec_module'):
            return _load_backward_compatible(spec)
        module = module_from_spec(spec)
        with _installed_safely(module):
            if spec.loader is None:
                if spec.submodule_search_locations is None:
                    raise ImportError('missing loader', name=(spec.name))
            else:
                spec.loader.exec_module(module)
        return sys.modules[spec.name]


def _load(spec):
    """Return a new module object, loaded by the spec's loader.

    The module is not added to its parent.

    If a module is already in sys.modules, that existing module gets
    clobbered.

    """
    with _ModuleLockManager(spec.name):
        return _load_unlocked(spec)


class BuiltinImporter:
    __doc__ = 'Meta path import for built-in modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    '

    @staticmethod
    def module_repr(module):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} (built-in)>'.format(module.__name__)

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if path is not None:
            return
        if _imp.is_builtin(fullname):
            return spec_from_loader(fullname, cls, origin='built-in')
        return

    @classmethod
    def find_module(cls, fullname, path=None):
        """Find the built-in module.

        If 'path' is ever specified then the search is considered a failure.

        This method is deprecated.  Use find_spec() instead.

        """
        spec = cls.find_spec(fullname, path)
        if spec is not None:
            return spec.loader

    @classmethod
    def create_module(self, spec):
        """Create a built-in module"""
        if spec.name not in sys.builtin_module_names:
            raise ImportError(('{!r} is not a built-in module'.format(spec.name)), name=(spec.name))
        return _call_with_frames_removed(_imp.create_builtin, spec)

    @classmethod
    def exec_module(self, module):
        """Exec a built-in module"""
        _call_with_frames_removed(_imp.exec_builtin, module)

    @classmethod
    @_requires_builtin
    def get_code(cls, fullname):
        """Return None as built-in modules do not have code objects."""
        pass

    @classmethod
    @_requires_builtin
    def get_source(cls, fullname):
        """Return None as built-in modules do not have source code."""
        pass

    @classmethod
    @_requires_builtin
    def is_package(cls, fullname):
        """Return False as built-in modules are never packages."""
        return False

    load_module = classmethod(_load_module_shim)


class FrozenImporter:
    __doc__ = 'Meta path import for frozen modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    '

    @staticmethod
    def module_repr(m):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} (frozen)>'.format(m.__name__)

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if _imp.is_frozen(fullname):
            return spec_from_loader(fullname, cls, origin='frozen')
        return

    @classmethod
    def find_module(cls, fullname, path=None):
        """Find a frozen module.

        This method is deprecated.  Use find_spec() instead.

        """
        if _imp.is_frozen(fullname):
            return cls

    @classmethod
    def create_module(cls, spec):
        """Use default semantics for module creation."""
        pass

    @staticmethod
    def exec_module(module):
        name = module.__spec__.name
        if not _imp.is_frozen(name):
            raise ImportError(('{!r} is not a frozen module'.format(name)), name=name)
        code = _call_with_frames_removed(_imp.get_frozen_object, name)
        exec(code, module.__dict__)

    @classmethod
    def load_module(cls, fullname):
        """Load a frozen module.

        This method is deprecated.  Use exec_module() instead.

        """
        return _load_module_shim(cls, fullname)

    @classmethod
    @_requires_frozen
    def get_code(cls, fullname):
        """Return the code object for the frozen module."""
        return _imp.get_frozen_object(fullname)

    @classmethod
    @_requires_frozen
    def get_source(cls, fullname):
        """Return None as frozen modules do not have source code."""
        pass

    @classmethod
    @_requires_frozen
    def is_package(cls, fullname):
        """Return True if the frozen module is a package."""
        return _imp.is_frozen_package(fullname)


class _ImportLockContext:
    __doc__ = 'Context manager for the import lock.'

    def __enter__(self):
        """Acquire the import lock."""
        _imp.acquire_lock()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Release the import lock regardless of any raised exceptions."""
        _imp.release_lock()


def _resolve_name(name, package, level):
    """Resolve a relative module name to an absolute one."""
    bits = package.rsplit('.', level - 1)
    if len(bits) < level:
        raise ValueError('attempted relative import beyond top-level package')
    base = bits[0]
    if name:
        return '{}.{}'.format(base, name)
    return base


def _find_spec_legacy(finder, name, path):
    loader = finder.find_module(name, path)
    if loader is None:
        return
    return spec_from_loader(name, loader)


def _find_spec(name, path, target=None):
    """Find a module's spec."""
    meta_path = sys.meta_path
    if meta_path is None:
        raise ImportError('sys.meta_path is None, Python is likely shutting down')
    if not meta_path:
        _warnings.warn('sys.meta_path is empty', ImportWarning)
    is_reload = name in sys.modules
    for finder in meta_path:
        with _ImportLockContext():
            try:
                find_spec = finder.find_spec
            except AttributeError:
                spec = _find_spec_legacy(finder, name, path)
                if spec is None:
                    continue
            else:
                spec = find_spec(name, path, target)

        if spec is not None:
            if not is_reload:
                if name in sys.modules:
                    module = sys.modules[name]
                    try:
                        __spec__ = module.__spec__
                    except AttributeError:
                        return spec

                    if __spec__ is None:
                        return spec
                    else:
                        return __spec__
            return spec
    else:
        return


def _sanity_check(name, package, level):
    """Verify arguments are "sane"."""
    if not isinstance(name, str):
        raise TypeError('module name must be str, not {}'.format(type(name)))
    if level < 0:
        raise ValueError('level must be >= 0')
    if level > 0:
        if not isinstance(package, str):
            raise TypeError('__package__ not set to a string')
        elif not package:
            raise ImportError('attempted relative import with no known parent package')
        if not name:
            if level == 0:
                raise ValueError('Empty module name')


_ERR_MSG_PREFIX = 'No module named '
_ERR_MSG = _ERR_MSG_PREFIX + '{!r}'

def _find_and_load_unlocked(name, import_):
    path = None
    parent = name.rpartition('.')[0]
    if parent:
        if parent not in sys.modules:
            _call_with_frames_removed(import_, parent)
        if name in sys.modules:
            return sys.modules[name]
        parent_module = sys.modules[parent]
        try:
            path = parent_module.__path__
        except AttributeError:
            msg = (_ERR_MSG + '; {!r} is not a package').format(name, parent)
            raise ModuleNotFoundError(msg, name=name) from None

        spec = _find_spec(name, path)
        if spec is None:
            raise ModuleNotFoundError((_ERR_MSG.format(name)), name=name)
        else:
            module = _load_unlocked(spec)
        if parent:
            parent_module = sys.modules[parent]
            setattr(parent_module, name.rpartition('.')[2], module)
        return module


_NEEDS_LOADING = object()

def _find_and_load(name, import_):
    """Find and load the module."""
    with _ModuleLockManager(name):
        module = sys.modules.get(name, _NEEDS_LOADING)
        if module is _NEEDS_LOADING:
            return _find_and_load_unlocked(name, import_)
    if module is None:
        message = 'import of {} halted; None in sys.modules'.format(name)
        raise ModuleNotFoundError(message, name=name)
    _lock_unlock_module(name)
    return module


def _gcd_import(name, package=None, level=0):
    """Import and return the module based on its name, the package the call is
    being made from, and the level adjustment.

    This function represents the greatest common denominator of functionality
    between import_module and __import__. This includes setting __package__ if
    the loader did not.

    """
    _sanity_check(name, package, level)
    if level > 0:
        name = _resolve_name(name, package, level)
    return _find_and_load(name, _gcd_import)


def _handle_fromlist--- This code section failed: ---

 L.1019         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'module'
                4  LOAD_STR                 '__path__'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE   230  'to 230'

 L.1020        10  SETUP_LOOP          230  'to 230'
               12  LOAD_FAST                'fromlist'
               14  GET_ITER         
             16_0  COME_FROM           226  '226'
             16_1  COME_FROM           222  '222'
             16_2  COME_FROM           204  '204'
             16_3  COME_FROM           158  '158'
             16_4  COME_FROM           128  '128'
             16_5  COME_FROM           118  '118'
             16_6  COME_FROM            76  '76'
               16  FOR_ITER            228  'to 228'
               18  STORE_FAST               'x'

 L.1021        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'x'
               24  LOAD_GLOBAL              str
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_TRUE     78  'to 78'

 L.1022        30  LOAD_FAST                'recursive'
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L.1023        34  LOAD_FAST                'module'
               36  LOAD_ATTR                __name__
               38  LOAD_STR                 '.__all__'
               40  BINARY_ADD       
               42  STORE_FAST               'where'
               44  JUMP_FORWARD         50  'to 50'
             46_0  COME_FROM            32  '32'

 L.1025        46  LOAD_STR                 "``from list''"
               48  STORE_FAST               'where'
             50_0  COME_FROM            44  '44'

 L.1026        50  LOAD_GLOBAL              TypeError
               52  LOAD_STR                 'Item in '
               54  LOAD_FAST                'where'
               56  FORMAT_VALUE          0  ''
               58  LOAD_STR                 ' must be str, not '
               60  LOAD_GLOBAL              type
               62  LOAD_FAST                'x'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  LOAD_ATTR                __name__
               68  FORMAT_VALUE          0  ''
               70  BUILD_STRING_4        4 
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  RAISE_VARARGS_1       1  'exception instance'
               76  JUMP_BACK            16  'to 16'
             78_0  COME_FROM            28  '28'

 L.1028        78  LOAD_FAST                'x'
               80  LOAD_STR                 '*'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   120  'to 120'

 L.1029        86  LOAD_FAST                'recursive'
               88  POP_JUMP_IF_TRUE    226  'to 226'
               90  LOAD_GLOBAL              hasattr
               92  LOAD_FAST                'module'
               94  LOAD_STR                 '__all__'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   226  'to 226'

 L.1030       100  LOAD_GLOBAL              _handle_fromlist
              102  LOAD_FAST                'module'
              104  LOAD_FAST                'module'
              106  LOAD_ATTR                __all__
              108  LOAD_FAST                'import_'

 L.1031       110  LOAD_CONST               True
              112  LOAD_CONST               ('recursive',)
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  POP_TOP          
              118  JUMP_BACK            16  'to 16'
            120_0  COME_FROM            84  '84'

 L.1032       120  LOAD_GLOBAL              hasattr
              122  LOAD_FAST                'module'
              124  LOAD_FAST                'x'
              126  CALL_FUNCTION_2       2  '2 positional arguments'
              128  POP_JUMP_IF_TRUE_BACK    16  'to 16'

 L.1033       130  LOAD_STR                 '{}.{}'
              132  LOAD_METHOD              format
              134  LOAD_FAST                'module'
              136  LOAD_ATTR                __name__
              138  LOAD_FAST                'x'
              140  CALL_METHOD_2         2  '2 positional arguments'
              142  STORE_FAST               'from_name'

 L.1034       144  SETUP_EXCEPT        160  'to 160'

 L.1035       146  LOAD_GLOBAL              _call_with_frames_removed
              148  LOAD_FAST                'import_'
              150  LOAD_FAST                'from_name'
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  POP_TOP          
              156  POP_BLOCK        
              158  JUMP_BACK            16  'to 16'
            160_0  COME_FROM_EXCEPT    144  '144'

 L.1036       160  DUP_TOP          
              162  LOAD_GLOBAL              ModuleNotFoundError
              164  COMPARE_OP               exception-match
              166  POP_JUMP_IF_FALSE   224  'to 224'
              168  POP_TOP          
              170  STORE_FAST               'exc'
              172  POP_TOP          
              174  SETUP_FINALLY       212  'to 212'

 L.1040       176  LOAD_FAST                'exc'
              178  LOAD_ATTR                name
              180  LOAD_FAST                'from_name'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   206  'to 206'

 L.1041       186  LOAD_GLOBAL              sys
              188  LOAD_ATTR                modules
              190  LOAD_METHOD              get
              192  LOAD_FAST                'from_name'
              194  LOAD_GLOBAL              _NEEDS_LOADING
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  LOAD_CONST               None
              200  COMPARE_OP               is-not
              202  POP_JUMP_IF_FALSE   206  'to 206'

 L.1042       204  CONTINUE_LOOP        16  'to 16'
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           184  '184'

 L.1043       206  RAISE_VARARGS_0       0  'reraise'
              208  POP_BLOCK        
              210  LOAD_CONST               None
            212_0  COME_FROM_FINALLY   174  '174'
              212  LOAD_CONST               None
              214  STORE_FAST               'exc'
              216  DELETE_FAST              'exc'
              218  END_FINALLY      
              220  POP_EXCEPT       
              222  JUMP_BACK            16  'to 16'
            224_0  COME_FROM           166  '166'
              224  END_FINALLY      
            226_0  COME_FROM            98  '98'
            226_1  COME_FROM            88  '88'
              226  JUMP_BACK            16  'to 16'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP       10  '10'
            230_1  COME_FROM             8  '8'

 L.1044       230  LOAD_FAST                'module'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 230_0


def _calc___package__(globals):
    """Calculate what __package__ should be.

    __package__ is not guaranteed to be defined or could be set to None
    to represent that its proper value is unknown.

    """
    package = globals.get('__package__')
    spec = globals.get('__spec__')
    if package is not None:
        if spec is not None:
            if package != spec.parent:
                _warnings.warn(f"__package__ != __spec__.parent ({package!r} != {spec.parent!r})", ImportWarning,
                  stacklevel=3)
        return package
    if spec is not None:
        return spec.parent
    _warnings.warn("can't resolve package from __spec__ or __package__, falling back on __name__ and __path__", ImportWarning,
      stacklevel=3)
    package = globals['__name__']
    if '__path__' not in globals:
        package = package.rpartition('.')[0]
    return package


def __import__(name, globals=None, locals=None, fromlist=(), level=0):
    """Import a module.

    The 'globals' argument is used to infer where the import is occurring from
    to handle relative imports. The 'locals' argument is ignored. The
    'fromlist' argument specifies what should exist as attributes on the module
    being imported (e.g. ``from module import <fromlist>``).  The 'level'
    argument represents the package location to import from in a relative
    import (e.g. ``from ..pkg import mod`` would have a 'level' of 2).

    """
    if level == 0:
        module = _gcd_import(name)
    else:
        globals_ = globals if globals is not None else {}
        package = _calc___package__(globals_)
        module = _gcd_import(name, package, level)
    if not fromlist:
        if level == 0:
            return _gcd_import(name.partition('.')[0])
        if not name:
            return module
        cut_off = len(name) - len(name.partition('.')[0])
        return sys.modules[module.__name__[:len(module.__name__) - cut_off]]
    else:
        return _handle_fromlist(module, fromlist, _gcd_import)


def _builtin_from_name(name):
    spec = BuiltinImporter.find_spec(name)
    if spec is None:
        raise ImportError('no built-in module named ' + name)
    return _load_unlocked(spec)


def _setup--- This code section failed: ---

 L.1125         0  LOAD_FAST                '_imp_module'
                2  STORE_GLOBAL             _imp

 L.1126         4  LOAD_FAST                'sys_module'
                6  STORE_GLOBAL             sys

 L.1129         8  LOAD_GLOBAL              type
               10  LOAD_GLOBAL              sys
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'module_type'

 L.1130        16  SETUP_LOOP          104  'to 104'
               18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                modules
               22  LOAD_METHOD              items
               24  CALL_METHOD_0         0  '0 positional arguments'
               26  GET_ITER         
             28_0  COME_FROM           100  '100'
             28_1  COME_FROM            78  '78'
             28_2  COME_FROM            70  '70'
             28_3  COME_FROM            44  '44'
               28  FOR_ITER            102  'to 102'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'name'
               34  STORE_FAST               'module'

 L.1131        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'module'
               40  LOAD_FAST                'module_type'
               42  CALL_FUNCTION_2       2  '2 positional arguments'
               44  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L.1132        46  LOAD_FAST                'name'
               48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                builtin_module_names
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    62  'to 62'

 L.1133        56  LOAD_GLOBAL              BuiltinImporter
               58  STORE_FAST               'loader'
               60  JUMP_FORWARD         80  'to 80'
             62_0  COME_FROM            54  '54'

 L.1134        62  LOAD_GLOBAL              _imp
               64  LOAD_METHOD              is_frozen
               66  LOAD_FAST                'name'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L.1135        72  LOAD_GLOBAL              FrozenImporter
               74  STORE_FAST               'loader'
               76  JUMP_FORWARD         80  'to 80'

 L.1137        78  CONTINUE             28  'to 28'
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            60  '60'

 L.1138        80  LOAD_GLOBAL              _spec_from_module
               82  LOAD_FAST                'module'
               84  LOAD_FAST                'loader'
               86  CALL_FUNCTION_2       2  '2 positional arguments'
               88  STORE_FAST               'spec'

 L.1139        90  LOAD_GLOBAL              _init_module_attrs
               92  LOAD_FAST                'spec'
               94  LOAD_FAST                'module'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_TOP          
              100  JUMP_BACK            28  'to 28'
              102  POP_BLOCK        
            104_0  COME_FROM_LOOP       16  '16'

 L.1142       104  LOAD_GLOBAL              sys
              106  LOAD_ATTR                modules
              108  LOAD_GLOBAL              __name__
              110  BINARY_SUBSCR    
              112  STORE_FAST               'self_module'

 L.1143       114  SETUP_LOOP          170  'to 170'
              116  LOAD_CONST               ('_thread', '_warnings', '_weakref')
              118  GET_ITER         
            120_0  COME_FROM           166  '166'
              120  FOR_ITER            168  'to 168'
              122  STORE_FAST               'builtin_name'

 L.1144       124  LOAD_FAST                'builtin_name'
              126  LOAD_GLOBAL              sys
              128  LOAD_ATTR                modules
              130  COMPARE_OP               not-in
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L.1145       134  LOAD_GLOBAL              _builtin_from_name
              136  LOAD_FAST                'builtin_name'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  STORE_FAST               'builtin_module'
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM           132  '132'

 L.1147       144  LOAD_GLOBAL              sys
              146  LOAD_ATTR                modules
              148  LOAD_FAST                'builtin_name'
              150  BINARY_SUBSCR    
              152  STORE_FAST               'builtin_module'
            154_0  COME_FROM           142  '142'

 L.1148       154  LOAD_GLOBAL              setattr
              156  LOAD_FAST                'self_module'
              158  LOAD_FAST                'builtin_name'
              160  LOAD_FAST                'builtin_module'
              162  CALL_FUNCTION_3       3  '3 positional arguments'
              164  POP_TOP          
              166  JUMP_BACK           120  'to 120'
              168  POP_BLOCK        
            170_0  COME_FROM_LOOP      114  '114'

Parse error at or near `CONTINUE' instruction at offset 78


def _install(sys_module, _imp_module):
    """Install importers for builtin and frozen modules"""
    _setup(sys_module, _imp_module)
    sys.meta_path.append(BuiltinImporter)
    sys.meta_path.append(FrozenImporter)


def _install_external_importers():
    """Install importers that require external filesystem access"""
    global _bootstrap_external
    import _frozen_importlib_external
    _bootstrap_external = _frozen_importlib_external
    _frozen_importlib_external._install(sys.modules[__name__])