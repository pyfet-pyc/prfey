# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\sandbox.py
import os, sys, tempfile, operator, functools, itertools, re, contextlib, pickle, textwrap, builtins, pkg_resources
from distutils.errors import DistutilsError
from pkg_resources import working_set
if sys.platform.startswith('java'):
    import org.python.modules.posix.PosixModule as _os
else:
    _os = sys.modules[os.name]
try:
    _file = file
except NameError:
    _file = None
else:
    _open = open
    __all__ = [
     'AbstractSandbox', 'DirectorySandbox', 'SandboxViolation', 'run_setup']

    def _execfile(filename, globals, locals=None):
        """
    Python 3 implementation of execfile.
    """
        mode = 'rb'
        with open(filename, mode) as stream:
            script = stream.read()
        if locals is None:
            locals = globals
        code = compile(script, filename, 'exec')
        exec(code, globals, locals)


    @contextlib.contextmanager
    def save_argv(repl=None):
        saved = sys.argv[:]
        if repl is not None:
            sys.argv[:] = repl
        try:
            yield saved
        finally:
            sys.argv[:] = saved


    @contextlib.contextmanager
    def save_path():
        saved = sys.path[:]
        try:
            yield saved
        finally:
            sys.path[:] = saved


    @contextlib.contextmanager
    def override_temp(replacement):
        """
    Monkey-patch tempfile.tempdir with replacement, ensuring it exists
    """
        os.makedirs(replacement, exist_ok=True)
        saved = tempfile.tempdir
        tempfile.tempdir = replacement
        try:
            yield
        finally:
            tempfile.tempdir = saved


    @contextlib.contextmanager
    def pushd(target):
        saved = os.getcwd()
        os.chdir(target)
        try:
            yield saved
        finally:
            os.chdir(saved)


    class UnpickleableException(Exception):
        __doc__ = '\n    An exception representing another Exception that could not be pickled.\n    '

        @staticmethod
        def dump(type, exc):
            """
        Always return a dumped (pickled) type and exc. If exc can't be pickled,
        wrap it in UnpickleableException first.
        """
            try:
                return (
                 pickle.dumps(type), pickle.dumps(exc))
            except Exception:
                import setuptools.sandbox as cls
                return cls.dump(cls, cls(repr(exc)))


    class ExceptionSaver:
        __doc__ = '\n    A Context Manager that will save an exception, serialized, and restore it\n    later.\n    '

        def __enter__(self):
            return self

        def __exit__(self, type, exc, tb):
            if not exc:
                return
            self._saved = UnpickleableException.dump(type, exc)
            self._tb = tb
            return True

        def resume(self):
            """restore and re-raise any exception"""
            if '_saved' not in vars(self):
                return
            type, exc = map(pickle.loads, self._saved)
            raise exc.with_traceback(self._tb)


    @contextlib.contextmanager
    def save_modules():
        """
    Context in which imported modules are saved.

    Translates exceptions internal to the context into the equivalent exception
    outside the context.
    """
        saved = sys.modules.copy()
        with ExceptionSaver() as saved_exc:
            yield saved
        sys.modules.update(saved)
        del_modules = (mod_name for mod_name in sys.modules if mod_name not in saved if not mod_name.startswith('encodings.'))
        _clear_modules(del_modules)
        saved_exc.resume()


    def _clear_modules(module_names):
        for mod_name in list(module_names):
            del sys.modules[mod_name]


    @contextlib.contextmanager
    def save_pkg_resources_state():
        saved = pkg_resources.__getstate__()
        try:
            yield saved
        finally:
            pkg_resources.__setstate__(saved)


    @contextlib.contextmanager
    def setup_context(setup_dir):
        temp_dir = os.path.join(setup_dir, 'temp')
        with save_pkg_resources_state():
            with save_modules():
                with save_path():
                    hide_setuptools()
                    with save_argv():
                        with override_temp(temp_dir):
                            with pushd(setup_dir):
                                __import__('setuptools')
                                yield


    _MODULES_TO_HIDE = {
     'setuptools',
     'distutils',
     'pkg_resources',
     'Cython',
     '_distutils_hack'}

    def _needs_hiding(mod_name):
        """
    >>> _needs_hiding('setuptools')
    True
    >>> _needs_hiding('pkg_resources')
    True
    >>> _needs_hiding('setuptools_plugin')
    False
    >>> _needs_hiding('setuptools.__init__')
    True
    >>> _needs_hiding('distutils')
    True
    >>> _needs_hiding('os')
    False
    >>> _needs_hiding('Cython')
    True
    """
        base_module = mod_name.split('.', 1)[0]
        return base_module in _MODULES_TO_HIDE


    def hide_setuptools():
        """
    Remove references to setuptools' modules from sys.modules to allow the
    invocation to import the most appropriate setuptools. This technique is
    necessary to avoid issues such as #315 where setuptools upgrading itself
    would fail to find a function declared in the metadata.
    """
        _distutils_hack = sys.modules.get('_distutils_hack', None)
        if _distutils_hack is not None:
            _distutils_hack.remove_shim()
        modules = filter(_needs_hiding, sys.modules)
        _clear_modules(modules)


    def run_setup(setup_script, args):
        """Run a distutils setup script, sandboxed in its directory"""
        setup_dir = os.path.abspath(os.path.dirname(setup_script))
        with setup_context(setup_dir):
            try:
                sys.argv[:] = [
                 setup_script] + list(args)
                sys.path.insert(0, setup_dir)
                working_set.__init__()
                working_set.callbacks.append(lambda dist: dist.activate())
                with DirectorySandbox(setup_dir):
                    ns = dict(__file__=setup_script, __name__='__main__')
                    _execfile(setup_script, ns)
            except SystemExit as v:
                try:
                    if v.args:
                        if v.args[0]:
                            raise
                finally:
                    v = None
                    del v


    class AbstractSandbox:
        __doc__ = "Wrap 'os' module and 'open()' builtin for virtualizing setup scripts"
        _active = False

        def __init__(self):
            self._attrs = [name for name in dir(_os) if not name.startswith('_') if hasattr(self, name)]

        def _copy(self, source):
            for name in self._attrs:
                setattr(os, name, getattr(source, name))

        def __enter__(self):
            self._copy(self)
            if _file:
                builtins.file = self._file
            builtins.open = self._open
            self._active = True

        def __exit__(self, exc_type, exc_value, traceback):
            self._active = False
            if _file:
                builtins.file = _file
            builtins.open = _open
            self._copy(_os)

        def run(self, func):
            """Run 'func' under os sandboxing"""
            with self:
                return func()

        def _mk_dual_path_wrapper(name):
            original = getattr(_os, name)

            def wrap(self, src, dst, *args, **kw):
                if self._active:
                    src, dst = (self._remap_pair)(name, src, dst, *args, **kw)
                return original(src, dst, *args, **kw)

            return wrap

        for name in ('rename', 'link', 'symlink'):
            if hasattr(_os, name):
                locals()[name] = _mk_dual_path_wrapper(name)
        else:

            def _mk_single_path_wrapper(name, original=None):
                original = original or getattr(_os, name)

                def wrap(self, path, *args, **kw):
                    if self._active:
                        path = (self._remap_input)(name, path, *args, **kw)
                    return original(path, *args, **kw)

                return wrap

            if _file:
                _file = _mk_single_path_wrapper('file', _file)
            _open = _mk_single_path_wrapper('open', _open)
            for name in ('stat', 'listdir', 'chdir', 'open', 'chmod', 'chown', 'mkdir',
                         'remove', 'unlink', 'rmdir', 'utime', 'lchown', 'chroot',
                         'lstat', 'startfile', 'mkfifo', 'mknod', 'pathconf', 'access'):
                if hasattr(_os, name):
                    locals()[name] = _mk_single_path_wrapper(name)
            else:

                def _mk_single_with_return(name):
                    original = getattr(_os, name)

                    def wrap(self, path, *args, **kw):
                        if self._active:
                            path = (self._remap_input)(name, path, *args, **kw)
                            return self._remap_output(name, original(path, *args, **kw))
                        return original(path, *args, **kw)

                    return wrap

                for name in ('readlink', 'tempnam'):
                    if hasattr(_os, name):
                        locals()[name] = _mk_single_with_return(name)
                else:

                    def _mk_query(name):
                        original = getattr(_os, name)

                        def wrap(self, *args, **kw):
                            retval = original(*args, **kw)
                            if self._active:
                                return self._remap_output(name, retval)
                            return retval

                        return wrap

                    for name in ('getcwd', 'tmpnam'):
                        if hasattr(_os, name):
                            locals()[name] = _mk_query(name)
                    else:

                        def _validate_path(self, path):
                            """Called to remap or validate any path, whether input or output"""
                            return path

                        def _remap_input(self, operation, path, *args, **kw):
                            """Called for path inputs"""
                            return self._validate_path(path)

                        def _remap_output(self, operation, path):
                            """Called for path outputs"""
                            return self._validate_path(path)

                        def _remap_pair(self, operation, src, dst, *args, **kw):
                            """Called for path pairs like rename, link, and symlink operations"""
                            return (
                             (self._remap_input)(operation + '-from', src, *args, **kw),
                             (self._remap_input)(operation + '-to', dst, *args, **kw))


    if hasattr(os, 'devnull'):
        _EXCEPTIONS = [
         os.devnull]
    else:
        _EXCEPTIONS = []

    class DirectorySandbox(AbstractSandbox):
        __doc__ = 'Restrict operations to a single subdirectory - pseudo-chroot'
        write_ops = dict.fromkeys([
         'open', 'chmod', 'chown', 'mkdir', 'remove', 'unlink', 'rmdir',
         'utime', 'lchown', 'chroot', 'mkfifo', 'mknod', 'tempnam'])
        _exception_patterns = [
         '.*lib2to3.*\\.pickle$']

        def __init__(self, sandbox, exceptions=_EXCEPTIONS):
            self._sandbox = os.path.normcase(os.path.realpath(sandbox))
            self._prefix = os.path.join(self._sandbox, '')
            self._exceptions = [os.path.normcase(os.path.realpath(path)) for path in exceptions]
            AbstractSandbox.__init__(self)

        def _violation(self, operation, *args, **kw):
            from setuptools.sandbox import SandboxViolation
            raise SandboxViolation(operation, args, kw)

        if _file:

            def _file(self, path, mode='r', *args, **kw):
                if mode not in ('r', 'rt', 'rb', 'rU', 'U'):
                    if not self._ok(path):
                        (self._violation)('file', path, mode, *args, **kw)
                    return _file(path, mode, *args, **kw)

        def _open(self, path, mode='r', *args, **kw):
            if mode not in ('r', 'rt', 'rb', 'rU', 'U'):
                if not self._ok(path):
                    (self._violation)('open', path, mode, *args, **kw)
                return _open(path, mode, *args, **kw)

        def tmpnam(self):
            self._violation('tmpnam')

        def _ok--- This code section failed: ---

 L. 429         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _active
                4  STORE_FAST               'active'

 L. 430         6  SETUP_FINALLY        70  'to 70'

 L. 431         8  LOAD_CONST               False
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _active

 L. 432        14  LOAD_GLOBAL              os
               16  LOAD_ATTR                path
               18  LOAD_METHOD              normcase
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              realpath
               26  LOAD_FAST                'path'
               28  CALL_METHOD_1         1  ''
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'realpath'

 L. 434        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _exempted
               38  LOAD_FAST                'realpath'
               40  CALL_METHOD_1         1  ''
               42  JUMP_IF_TRUE_OR_POP    64  'to 64'

 L. 435        44  LOAD_FAST                'realpath'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _sandbox
               50  COMPARE_OP               ==

 L. 434        52  JUMP_IF_TRUE_OR_POP    64  'to 64'

 L. 436        54  LOAD_FAST                'realpath'
               56  LOAD_METHOD              startswith
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _prefix
               62  CALL_METHOD_1         1  ''
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            42  '42'

 L. 433        64  POP_BLOCK        
               66  CALL_FINALLY         70  'to 70'
               68  RETURN_VALUE     
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM_FINALLY     6  '6'

 L. 439        70  LOAD_FAST                'active'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _active
               76  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 66

        def _exempted(self, filepath):
            start_matches = (filepath.startswith(exception) for exception in self._exceptions)
            pattern_matches = (re.match(pattern, filepath) for pattern in self._exception_patterns)
            candidates = itertools.chain(start_matches, pattern_matches)
            return any(candidates)

        def _remap_input(self, operation, path, *args, **kw):
            """Called for path inputs"""
            if operation in self.write_ops:
                if not self._ok(path):
                    (self._violation)(operation, os.path.realpath(path), *args, **kw)
                return path

        def _remap_pair(self, operation, src, dst, *args, **kw):
            """Called for path pairs like rename, link, and symlink operations"""
            if not (self._ok(src) and self._ok(dst)):
                (self._violation)(operation, src, dst, *args, **kw)
            return (src, dst)

        def open(self, file, flags, mode=511, *args, **kw):
            """Called for low-level os.open()"""
            if flags & WRITE_FLAGS:
                if not self._ok(file):
                    (self._violation)('os.open', file, flags, mode, *args, **kw)
                return (_os.open)(file, flags, mode, *args, **kw)


    WRITE_FLAGS = functools.reduce(operator.or_, [getattr(_os, a, 0) for a in 'O_WRONLY O_RDWR O_APPEND O_CREAT O_TRUNC O_TEMPORARY'.split()])

    class SandboxViolation(DistutilsError):
        __doc__ = 'A setup script attempted to modify the filesystem outside the sandbox'
        tmpl = textwrap.dedent("\n        SandboxViolation: {cmd}{args!r} {kwargs}\n\n        The package setup script has attempted to modify files on your system\n        that are not within the EasyInstall build area, and has been aborted.\n\n        This package cannot be safely installed by EasyInstall, and may not\n        support alternate installation locations even if you run its setup\n        script by hand.  Please inform the package's author and the EasyInstall\n        maintainers to find out if a fix or workaround is available.\n        ").lstrip()

        def __str__(self):
            cmd, args, kwargs = self.args
            return (self.tmpl.format)(**locals())