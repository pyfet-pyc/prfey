# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
    else:
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
        while True:
            lock = _blocking_on.get(tid)
            if lock is None:
                return False
            tid = lock.owner
            if tid == me:
                return True

    def acquire--- This code section failed: ---

 L.  84         0  LOAD_GLOBAL              _thread
                2  LOAD_METHOD              get_ident
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tid'

 L.  85         8  LOAD_FAST                'self'
               10  LOAD_GLOBAL              _blocking_on
               12  LOAD_FAST                'tid'
               14  STORE_SUBSCR     

 L.  86        16  SETUP_FINALLY       166  'to 166'

 L.  88        18  LOAD_FAST                'self'
               20  LOAD_ATTR                lock
               22  SETUP_WITH          134  'to 134'
               24  POP_TOP          

 L.  89        26  LOAD_FAST                'self'
               28  LOAD_ATTR                count
               30  LOAD_CONST               0
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     46  'to 46'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                owner
               40  LOAD_FAST                'tid'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    84  'to 84'
             46_0  COME_FROM            34  '34'

 L.  90        46  LOAD_FAST                'tid'
               48  LOAD_FAST                'self'
               50  STORE_ATTR               owner

 L.  91        52  LOAD_FAST                'self'
               54  DUP_TOP          
               56  LOAD_ATTR                count
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  ROT_TWO          
               64  STORE_ATTR               count

 L.  92        66  POP_BLOCK        
               68  BEGIN_FINALLY    
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  POP_FINALLY           0  ''
               76  POP_BLOCK        
               78  CALL_FINALLY        166  'to 166'
               80  LOAD_CONST               True
               82  RETURN_VALUE     
             84_0  COME_FROM            44  '44'

 L.  93        84  LOAD_FAST                'self'
               86  LOAD_METHOD              has_deadlock
               88  CALL_METHOD_0         0  ''
               90  POP_JUMP_IF_FALSE   104  'to 104'

 L.  94        92  LOAD_GLOBAL              _DeadlockError
               94  LOAD_STR                 'deadlock detected by %r'
               96  LOAD_FAST                'self'
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            90  '90'

 L.  95       104  LOAD_FAST                'self'
              106  LOAD_ATTR                wakeup
              108  LOAD_METHOD              acquire
              110  LOAD_CONST               False
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.  96       116  LOAD_FAST                'self'
              118  DUP_TOP          
              120  LOAD_ATTR                waiters
              122  LOAD_CONST               1
              124  INPLACE_ADD      
              126  ROT_TWO          
              128  STORE_ATTR               waiters
            130_0  COME_FROM           114  '114'
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_WITH       22  '22'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      

 L.  98       140  LOAD_FAST                'self'
              142  LOAD_ATTR                wakeup
              144  LOAD_METHOD              acquire
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          

 L.  99       150  LOAD_FAST                'self'
              152  LOAD_ATTR                wakeup
              154  LOAD_METHOD              release
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          
              160  JUMP_BACK            18  'to 18'
              162  POP_BLOCK        
              164  BEGIN_FINALLY    
            166_0  COME_FROM            78  '78'
            166_1  COME_FROM_FINALLY    16  '16'

 L. 101       166  LOAD_GLOBAL              _blocking_on
              168  LOAD_FAST                'tid'
              170  DELETE_SUBSCR    
              172  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 68

    def release(self):
        tid = _thread.get_ident()
        with self.lock:
            if self.owner != tid:
                raise RuntimeError('cannot release un-acquired lock')
            else:
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
        else:
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


def _module_repr--- This code section failed: ---

 L. 271         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'module'
                4  LOAD_STR                 '__loader__'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'loader'

 L. 272        12  LOAD_GLOBAL              hasattr
               14  LOAD_FAST                'loader'
               16  LOAD_STR                 'module_repr'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    56  'to 56'

 L. 276        22  SETUP_FINALLY        36  'to 36'

 L. 277        24  LOAD_FAST                'loader'
               26  LOAD_METHOD              module_repr
               28  LOAD_FAST                'module'
               30  CALL_METHOD_1         1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    22  '22'

 L. 278        36  DUP_TOP          
               38  LOAD_GLOBAL              Exception
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    54  'to 54'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 279        50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            42  '42'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            20  '20'

 L. 280        56  SETUP_FINALLY        68  'to 68'

 L. 281        58  LOAD_FAST                'module'
               60  LOAD_ATTR                __spec__
               62  STORE_FAST               'spec'
               64  POP_BLOCK        
               66  JUMP_FORWARD         88  'to 88'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 282        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    86  'to 86'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 283        82  POP_EXCEPT       
               84  JUMP_FORWARD        104  'to 104'
             86_0  COME_FROM            74  '74'
               86  END_FINALLY      
             88_0  COME_FROM            66  '66'

 L. 285        88  LOAD_FAST                'spec'
               90  LOAD_CONST               None
               92  COMPARE_OP               is-not
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 286        96  LOAD_GLOBAL              _module_repr_from_spec
               98  LOAD_FAST                'spec'
              100  CALL_FUNCTION_1       1  ''
              102  RETURN_VALUE     
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            84  '84'

 L. 290       104  SETUP_FINALLY       116  'to 116'

 L. 291       106  LOAD_FAST                'module'
              108  LOAD_ATTR                __name__
              110  STORE_FAST               'name'
              112  POP_BLOCK        
              114  JUMP_FORWARD        140  'to 140'
            116_0  COME_FROM_FINALLY   104  '104'

 L. 292       116  DUP_TOP          
              118  LOAD_GLOBAL              AttributeError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   138  'to 138'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 293       130  LOAD_STR                 '?'
              132  STORE_FAST               'name'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           122  '122'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           114  '114'

 L. 294       140  SETUP_FINALLY       152  'to 152'

 L. 295       142  LOAD_FAST                'module'
              144  LOAD_ATTR                __file__
              146  STORE_FAST               'filename'
              148  POP_BLOCK        
              150  JUMP_FORWARD        210  'to 210'
            152_0  COME_FROM_FINALLY   140  '140'

 L. 296       152  DUP_TOP          
              154  LOAD_GLOBAL              AttributeError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   208  'to 208'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 297       166  LOAD_FAST                'loader'
              168  LOAD_CONST               None
              170  COMPARE_OP               is
              172  POP_JUMP_IF_FALSE   188  'to 188'

 L. 298       174  LOAD_STR                 '<module {!r}>'
              176  LOAD_METHOD              format
              178  LOAD_FAST                'name'
              180  CALL_METHOD_1         1  ''
              182  ROT_FOUR         
              184  POP_EXCEPT       
              186  RETURN_VALUE     
            188_0  COME_FROM           172  '172'

 L. 300       188  LOAD_STR                 '<module {!r} ({!r})>'
              190  LOAD_METHOD              format
              192  LOAD_FAST                'name'
              194  LOAD_FAST                'loader'
              196  CALL_METHOD_2         2  ''
              198  ROT_FOUR         
              200  POP_EXCEPT       
              202  RETURN_VALUE     
              204  POP_EXCEPT       
              206  JUMP_FORWARD        222  'to 222'
            208_0  COME_FROM           158  '158'
              208  END_FINALLY      
            210_0  COME_FROM           150  '150'

 L. 302       210  LOAD_STR                 '<module {!r} from {!r}>'
              212  LOAD_METHOD              format
              214  LOAD_FAST                'name'
              216  LOAD_FAST                'filename'
              218  CALL_METHOD_2         2  ''
              220  RETURN_VALUE     
            222_0  COME_FROM           206  '206'

Parse error at or near `POP_TOP' instruction at offset 46


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

    def __eq__--- This code section failed: ---

 L. 365         0  LOAD_FAST                'self'
                2  LOAD_ATTR                submodule_search_locations
                4  STORE_FAST               'smsl'

 L. 366         6  SETUP_FINALLY        80  'to 80'

 L. 367         8  LOAD_FAST                'self'
               10  LOAD_ATTR                name
               12  LOAD_FAST                'other'
               14  LOAD_ATTR                name
               16  COMPARE_OP               ==
               18  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 368        20  LOAD_FAST                'self'
               22  LOAD_ATTR                loader
               24  LOAD_FAST                'other'
               26  LOAD_ATTR                loader
               28  COMPARE_OP               ==

 L. 367        30  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 369        32  LOAD_FAST                'self'
               34  LOAD_ATTR                origin
               36  LOAD_FAST                'other'
               38  LOAD_ATTR                origin
               40  COMPARE_OP               ==

 L. 367        42  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 370        44  LOAD_FAST                'smsl'
               46  LOAD_FAST                'other'
               48  LOAD_ATTR                submodule_search_locations
               50  COMPARE_OP               ==

 L. 367        52  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 371        54  LOAD_FAST                'self'
               56  LOAD_ATTR                cached
               58  LOAD_FAST                'other'
               60  LOAD_ATTR                cached
               62  COMPARE_OP               ==

 L. 367        64  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L. 372        66  LOAD_FAST                'self'
               68  LOAD_ATTR                has_location
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                has_location
               74  COMPARE_OP               ==
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            52  '52'
             76_2  COME_FROM            42  '42'
             76_3  COME_FROM            30  '30'
             76_4  COME_FROM            18  '18'

 L. 367        76  POP_BLOCK        
               78  RETURN_VALUE     
             80_0  COME_FROM_FINALLY     6  '6'

 L. 373        80  DUP_TOP          
               82  LOAD_GLOBAL              AttributeError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   100  'to 100'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L. 374        94  POP_EXCEPT       
               96  LOAD_CONST               False
               98  RETURN_VALUE     
            100_0  COME_FROM            86  '86'
              100  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 90

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
        else:
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
            else:
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
        else:
            try:
                submodule_search_locations = list(module.__path__)
            except AttributeError:
                submodule_search_locations = None
            else:
                spec = ModuleSpec(name, loader, origin=origin)
                spec._set_fileattr = False if location is None else True
                spec.cached = cached
                spec.submodule_search_locations = submodule_search_locations
                return spec


def _init_module_attrs(spec, module, *, override=False):
    if not override:
        if getattr(module, '__name__', None) is None:
            try:
                module.__name__ = spec.name
            except AttributeError:
                pass

        if override or getattr(module, '__loader__', None) is None:
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

    else:
        if override or getattr(module, '__package__', None) is None:
            try:
                module.__package__ = spec.parent
            except AttributeError:
                pass

    try:
        module.__spec__ = spec
    except AttributeError:
        pass
    else:
        if override or getattr(module, '__path__', None) is None:
            if spec.submodule_search_locations is not None:
                try:
                    module.__path__ = spec.submodule_search_locations
                except AttributeError:
                    pass

        elif not spec.has_location or override or getattr(module, '__file__', None) is None:
            try:
                module.__file__ = spec.origin
            except AttributeError:
                pass

            if override or getattr(module, '__cached__', None) is None:
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
    else:
        if hasattr(spec.loader, 'exec_module'):
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
        try:
            if spec.loader is None:
                if spec.submodule_search_locations is None:
                    raise ImportError('missing loader', name=(spec.name))
                _init_module_attrs(spec, module, override=True)
            else:
                _init_module_attrs(spec, module, override=True)
                if not hasattr(spec.loader, 'exec_module'):
                    spec.loader.load_module(name)
                else:
                    spec.loader.exec_module(module)
        finally:
            module = sys.modules.pop(spec.name)
            sys.modules[spec.name] = module

    return module


def _load_backward_compatible(spec):
    try:
        spec.loader.load_module(spec.name)
    except:
        if spec.name in sys.modules:
            module = sys.modules.pop(spec.name)
            sys.modules[spec.name] = module
        raise
    else:
        module = sys.modules.pop(spec.name)
        sys.modules[spec.name] = module
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
    spec._initializing = True
    try:
        sys.modules[spec.name] = module
        try:
            if spec.loader is None:
                if spec.submodule_search_locations is None:
                    raise ImportError('missing loader', name=(spec.name))
            else:
                spec.loader.exec_module(module)
        except:
            try:
                del sys.modules[spec.name]
            except KeyError:
                pass
            else:
                raise
        else:
            module = sys.modules.pop(spec.name)
            sys.modules[spec.name] = module
            _verbose_message('import {!r} # {!r}', spec.name, spec.loader)
    finally:
        spec._initializing = False

    return module


def _load--- This code section failed: ---

 L. 701         0  LOAD_GLOBAL              _ModuleLockManager
                2  LOAD_FAST                'spec'
                4  LOAD_ATTR                name
                6  CALL_FUNCTION_1       1  ''
                8  SETUP_WITH           32  'to 32'
               10  POP_TOP          

 L. 702        12  LOAD_GLOBAL              _load_unlocked
               14  LOAD_FAST                'spec'
               16  CALL_FUNCTION_1       1  ''
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
    _ORIGIN = 'frozen'

    @staticmethod
    def module_repr(m):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} ({})>'.format(m.__name__, FrozenImporter._ORIGIN)

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if _imp.is_frozen(fullname):
            return spec_from_loader(fullname, cls, origin=(cls._ORIGIN))
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


def _find_spec--- This code section failed: ---

 L. 892         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                meta_path
                4  STORE_FAST               'meta_path'

 L. 893         6  LOAD_FAST                'meta_path'
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 895        14  LOAD_GLOBAL              ImportError
               16  LOAD_STR                 'sys.meta_path is None, Python is likely shutting down'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 898        22  LOAD_FAST                'meta_path'
               24  POP_JUMP_IF_TRUE     38  'to 38'

 L. 899        26  LOAD_GLOBAL              _warnings
               28  LOAD_METHOD              warn
               30  LOAD_STR                 'sys.meta_path is empty'
               32  LOAD_GLOBAL              ImportWarning
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          
             38_0  COME_FROM            24  '24'

 L. 904        38  LOAD_FAST                'name'
               40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                modules
               44  COMPARE_OP               in
               46  STORE_FAST               'is_reload'

 L. 905        48  LOAD_FAST                'meta_path'
               50  GET_ITER         
             52_0  COME_FROM           158  '158'
               52  FOR_ITER            264  'to 264'
               54  STORE_FAST               'finder'

 L. 906        56  LOAD_GLOBAL              _ImportLockContext
               58  CALL_FUNCTION_0       0  ''
               60  SETUP_WITH          146  'to 146'
               62  POP_TOP          

 L. 907        64  SETUP_FINALLY        76  'to 76'

 L. 908        66  LOAD_FAST                'finder'
               68  LOAD_ATTR                find_spec
               70  STORE_FAST               'find_spec'
               72  POP_BLOCK        
               74  JUMP_FORWARD        130  'to 130'
             76_0  COME_FROM_FINALLY    64  '64'

 L. 909        76  DUP_TOP          
               78  LOAD_GLOBAL              AttributeError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   128  'to 128'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 910        90  LOAD_GLOBAL              _find_spec_legacy
               92  LOAD_FAST                'finder'
               94  LOAD_FAST                'name'
               96  LOAD_FAST                'path'
               98  CALL_FUNCTION_3       3  ''
              100  STORE_FAST               'spec'

 L. 911       102  LOAD_FAST                'spec'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 912       110  POP_EXCEPT       
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  POP_FINALLY           0  ''
              122  JUMP_BACK            52  'to 52'
            124_0  COME_FROM           108  '108'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        142  'to 142'
            128_0  COME_FROM            82  '82'
              128  END_FINALLY      
            130_0  COME_FROM            74  '74'

 L. 914       130  LOAD_FAST                'find_spec'
              132  LOAD_FAST                'name'
              134  LOAD_FAST                'path'
              136  LOAD_FAST                'target'
              138  CALL_FUNCTION_3       3  ''
              140  STORE_FAST               'spec'
            142_0  COME_FROM           126  '126'
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM_WITH       60  '60'
              146  WITH_CLEANUP_START
              148  WITH_CLEANUP_FINISH
              150  END_FINALLY      

 L. 915       152  LOAD_FAST                'spec'
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
              158  POP_JUMP_IF_FALSE    52  'to 52'

 L. 917       160  LOAD_FAST                'is_reload'
          162_164  POP_JUMP_IF_TRUE    254  'to 254'
              166  LOAD_FAST                'name'
              168  LOAD_GLOBAL              sys
              170  LOAD_ATTR                modules
              172  COMPARE_OP               in
          174_176  POP_JUMP_IF_FALSE   254  'to 254'

 L. 918       178  LOAD_GLOBAL              sys
              180  LOAD_ATTR                modules
              182  LOAD_FAST                'name'
              184  BINARY_SUBSCR    
              186  STORE_FAST               'module'

 L. 919       188  SETUP_FINALLY       200  'to 200'

 L. 920       190  LOAD_FAST                'module'
              192  LOAD_ATTR                __spec__
              194  STORE_FAST               '__spec__'
              196  POP_BLOCK        
              198  JUMP_FORWARD        228  'to 228'
            200_0  COME_FROM_FINALLY   188  '188'

 L. 921       200  DUP_TOP          
              202  LOAD_GLOBAL              AttributeError
              204  COMPARE_OP               exception-match
              206  POP_JUMP_IF_FALSE   226  'to 226'
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L. 925       214  LOAD_FAST                'spec'
              216  ROT_FOUR         
              218  POP_EXCEPT       
              220  ROT_TWO          
              222  POP_TOP          
              224  RETURN_VALUE     
            226_0  COME_FROM           206  '206'
              226  END_FINALLY      
            228_0  COME_FROM           198  '198'

 L. 927       228  LOAD_FAST                '__spec__'
              230  LOAD_CONST               None
              232  COMPARE_OP               is
              234  POP_JUMP_IF_FALSE   244  'to 244'

 L. 928       236  LOAD_FAST                'spec'
              238  ROT_TWO          
              240  POP_TOP          
              242  RETURN_VALUE     
            244_0  COME_FROM           234  '234'

 L. 930       244  LOAD_FAST                '__spec__'
              246  ROT_TWO          
              248  POP_TOP          
              250  RETURN_VALUE     
              252  JUMP_BACK            52  'to 52'
            254_0  COME_FROM           174  '174'
            254_1  COME_FROM           162  '162'

 L. 932       254  LOAD_FAST                'spec'
              256  ROT_TWO          
              258  POP_TOP          
              260  RETURN_VALUE     
              262  JUMP_BACK            52  'to 52'

Parse error at or near `POP_BLOCK' instruction at offset 112


def _sanity_check(name, package, level):
    """Verify arguments are "sane"."""
    if not isinstance(name, str):
        raise TypeError('module name must be str, not {}'.format(type(name)))
    else:
        if level < 0:
            raise ValueError('level must be >= 0')
        elif level > 0:
            if not isinstance(package, str):
                raise TypeError('__package__ not set to a string')
            else:
                if not package:
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
    else:
        parent_module = sys.modules[parent]
        try:
            path = parent_module.__path__
        except AttributeError:
            msg = (_ERR_MSG + '; {!r} is not a package').format(name, parent)
            raise ModuleNotFoundError(msg, name=name) from None
        else:
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

def _find_and_load--- This code section failed: ---

 L. 988         0  LOAD_GLOBAL              _ModuleLockManager
                2  LOAD_FAST                'name'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           58  'to 58'
                8  POP_TOP          

 L. 989        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                modules
               14  LOAD_METHOD              get
               16  LOAD_FAST                'name'
               18  LOAD_GLOBAL              _NEEDS_LOADING
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'module'

 L. 990        24  LOAD_FAST                'module'
               26  LOAD_GLOBAL              _NEEDS_LOADING
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    54  'to 54'

 L. 991        32  LOAD_GLOBAL              _find_and_load_unlocked
               34  LOAD_FAST                'name'
               36  LOAD_FAST                'import_'
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  ROT_TWO          
               44  BEGIN_FINALLY    
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  POP_FINALLY           0  ''
               52  RETURN_VALUE     
             54_0  COME_FROM            30  '30'
               54  POP_BLOCK        
               56  BEGIN_FINALLY    
             58_0  COME_FROM_WITH        6  '6'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

 L. 993        64  LOAD_FAST                'module'
               66  LOAD_CONST               None
               68  COMPARE_OP               is
               70  POP_JUMP_IF_FALSE    94  'to 94'

 L. 994        72  LOAD_STR                 'import of {} halted; None in sys.modules'
               74  LOAD_METHOD              format

 L. 995        76  LOAD_FAST                'name'

 L. 994        78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'message'

 L. 996        82  LOAD_GLOBAL              ModuleNotFoundError
               84  LOAD_FAST                'message'
               86  LOAD_FAST                'name'
               88  LOAD_CONST               ('name',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            70  '70'

 L. 998        94  LOAD_GLOBAL              _lock_unlock_module
               96  LOAD_FAST                'name'
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          

 L. 999       102  LOAD_FAST                'module'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 42


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

 L.1027         0  LOAD_FAST                'fromlist'
                2  GET_ITER         
              4_0  COME_FROM           116  '116'
                4  FOR_ITER            222  'to 222'
                6  STORE_FAST               'x'

 L.1028         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'x'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     66  'to 66'

 L.1029        18  LOAD_FAST                'recursive'
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L.1030        22  LOAD_FAST                'module'
               24  LOAD_ATTR                __name__
               26  LOAD_STR                 '.__all__'
               28  BINARY_ADD       
               30  STORE_FAST               'where'
               32  JUMP_FORWARD         38  'to 38'
             34_0  COME_FROM            20  '20'

 L.1032        34  LOAD_STR                 "``from list''"
               36  STORE_FAST               'where'
             38_0  COME_FROM            32  '32'

 L.1033        38  LOAD_GLOBAL              TypeError
               40  LOAD_STR                 'Item in '
               42  LOAD_FAST                'where'
               44  FORMAT_VALUE          0  ''
               46  LOAD_STR                 ' must be str, not '
               48  LOAD_GLOBAL              type
               50  LOAD_FAST                'x'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_ATTR                __name__
               56  FORMAT_VALUE          0  ''
               58  BUILD_STRING_4        4 
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  JUMP_BACK             4  'to 4'
             66_0  COME_FROM            16  '16'

 L.1035        66  LOAD_FAST                'x'
               68  LOAD_STR                 '*'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE   108  'to 108'

 L.1036        74  LOAD_FAST                'recursive'
               76  POP_JUMP_IF_TRUE    220  'to 220'
               78  LOAD_GLOBAL              hasattr
               80  LOAD_FAST                'module'
               82  LOAD_STR                 '__all__'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   220  'to 220'

 L.1037        88  LOAD_GLOBAL              _handle_fromlist
               90  LOAD_FAST                'module'
               92  LOAD_FAST                'module'
               94  LOAD_ATTR                __all__
               96  LOAD_FAST                'import_'

 L.1038        98  LOAD_CONST               True

 L.1037       100  LOAD_CONST               ('recursive',)
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  POP_TOP          
              106  JUMP_BACK             4  'to 4'
            108_0  COME_FROM            72  '72'

 L.1039       108  LOAD_GLOBAL              hasattr
              110  LOAD_FAST                'module'
              112  LOAD_FAST                'x'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_TRUE      4  'to 4'

 L.1040       118  LOAD_STR                 '{}.{}'
              120  LOAD_METHOD              format
              122  LOAD_FAST                'module'
              124  LOAD_ATTR                __name__
              126  LOAD_FAST                'x'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'from_name'

 L.1041       132  SETUP_FINALLY       148  'to 148'

 L.1042       134  LOAD_GLOBAL              _call_with_frames_removed
              136  LOAD_FAST                'import_'
              138  LOAD_FAST                'from_name'
              140  CALL_FUNCTION_2       2  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_BACK             4  'to 4'
            148_0  COME_FROM_FINALLY   132  '132'

 L.1043       148  DUP_TOP          
              150  LOAD_GLOBAL              ModuleNotFoundError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   218  'to 218'
              156  POP_TOP          
              158  STORE_FAST               'exc'
              160  POP_TOP          
              162  SETUP_FINALLY       206  'to 206'

 L.1047       164  LOAD_FAST                'exc'
              166  LOAD_ATTR                name
              168  LOAD_FAST                'from_name'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   200  'to 200'

 L.1048       174  LOAD_GLOBAL              sys
              176  LOAD_ATTR                modules
              178  LOAD_METHOD              get
              180  LOAD_FAST                'from_name'
              182  LOAD_GLOBAL              _NEEDS_LOADING
              184  CALL_METHOD_2         2  ''
              186  LOAD_CONST               None
              188  COMPARE_OP               is-not

 L.1047       190  POP_JUMP_IF_FALSE   200  'to 200'

 L.1049       192  POP_BLOCK        
              194  POP_EXCEPT       
              196  CALL_FINALLY        206  'to 206'
              198  JUMP_BACK             4  'to 4'
            200_0  COME_FROM           190  '190'
            200_1  COME_FROM           172  '172'

 L.1050       200  RAISE_VARARGS_0       0  'reraise'
              202  POP_BLOCK        
              204  BEGIN_FINALLY    
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM_FINALLY   162  '162'
              206  LOAD_CONST               None
              208  STORE_FAST               'exc'
              210  DELETE_FAST              'exc'
              212  END_FINALLY      
              214  POP_EXCEPT       
              216  JUMP_BACK             4  'to 4'
            218_0  COME_FROM           154  '154'
              218  END_FINALLY      
            220_0  COME_FROM            86  '86'
            220_1  COME_FROM            76  '76'
              220  JUMP_BACK             4  'to 4'

 L.1051       222  LOAD_FAST                'module'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 194


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
        else:
            return name or module
        cut_off = len(name) - len(name.partition('.')[0])
        return sys.modules[module.__name__[:len(module.__name__) - cut_off]]
    else:
        if hasattr(module, '__path__'):
            return _handle_fromlist(module, fromlist, _gcd_import)
        return module


def _builtin_from_name(name):
    spec = BuiltinImporter.find_spec(name)
    if spec is None:
        raise ImportError('no built-in module named ' + name)
    return _load_unlocked(spec)


def _setup(sys_module, _imp_module):
    """Setup importlib by importing needed built-in modules and injecting them
    into the global namespace.

    As sys is needed for sys.modules access and _imp is needed to load built-in
    modules, those two modules must be explicitly passed in.

    """
    global _imp
    global sys
    _imp = _imp_module
    sys = sys_module
    module_type = type(sys)
    for name, module in sys.modules.items():
        if isinstance(module, module_type):
            if name in sys.builtin_module_names:
                loader = BuiltinImporter
        if _imp.is_frozen(name):
            loader = FrozenImporter
            break
        else:
            spec = _spec_from_module(module, loader)
            _init_module_attrs(spec, module)
    else:
        self_module = sys.modules[__name__]
        for builtin_name in ('_thread', '_warnings', '_weakref'):
            if builtin_name not in sys.modules:
                builtin_module = _builtin_from_name(builtin_name)
            else:
                builtin_module = sys.modules[builtin_name]
            setattr(self_module, builtin_name, builtin_module)


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