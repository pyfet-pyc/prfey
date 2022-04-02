# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\_bootstrap_external.py
"""Core implementation of path-based import.

This module is NOT meant to be directly imported! It has been designed such
that it can be bootstrapped into Python as the implementation of import. As
such it requires the injection of specific modules and attributes in order to
work. One should use importlib as the public-facing version of this module.

"""
_CASE_INSENSITIVE_PLATFORMS_STR_KEY = ('win', )
_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY = ('cygwin', 'darwin')
_CASE_INSENSITIVE_PLATFORMS = _CASE_INSENSITIVE_PLATFORMS_BYTES_KEY + _CASE_INSENSITIVE_PLATFORMS_STR_KEY

def _make_relax_case():
    if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
        if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS_STR_KEY):
            key = 'PYTHONCASEOK'
        else:
            key = b'PYTHONCASEOK'

        def _relax_case():
            return key in _os.environ

    else:

        def _relax_case():
            """True if filenames must be checked case-insensitively."""
            return False

    return _relax_case


def _pack_uint32(x):
    """Convert a 32-bit integer to little-endian."""
    return (int(x) & 4294967295).to_bytes(4, 'little')


def _unpack_uint32(data):
    """Convert 4 bytes in little-endian to an integer."""
    assert len(data) == 4
    return int.from_bytes(data, 'little')


def _unpack_uint16(data):
    """Convert 2 bytes in little-endian to an integer."""
    assert len(data) == 2
    return int.from_bytes(data, 'little')


def _path_join(*path_parts):
    """Replacement for os.path.join()."""
    return path_sep.join([part.rstrip(path_separators) for part in path_parts if part])


def _path_split(path):
    """Replacement for os.path.split()."""
    if len(path_separators) == 1:
        front, _, tail = path.rpartition(path_sep)
        return (
         front, tail)
    for x in reversed(path):
        if x in path_separators:
            front, tail = path.rsplit(x, maxsplit=1)
            return (
             front, tail)
    else:
        return (
         '', path)


def _path_stat(path):
    """Stat the path.

    Made a separate function to make it easier to override in experiments
    (e.g. cache stat results).

    """
    return _os.stat(path)


def _path_is_mode_type(path, mode):
    """Test whether the path is the specified mode type."""
    try:
        stat_info = _path_stat(path)
    except OSError:
        return False
    else:
        return stat_info.st_mode & 61440 == mode


def _path_isfile(path):
    """Replacement for os.path.isfile."""
    return _path_is_mode_type(path, 32768)


def _path_isdir(path):
    """Replacement for os.path.isdir."""
    if not path:
        path = _os.getcwd()
    return _path_is_mode_type(path, 16384)


def _path_isabs(path):
    """Replacement for os.path.isabs.

    Considers a Windows drive-relative path (no drive, but starts with slash) to
    still be "absolute".
    """
    return path.startswith(path_separators) or path[1:3] in _pathseps_with_colon


def _write_atomic(path, data, mode=438):
    """Best-effort function to write data to a path atomically.
    Be prepared to handle a FileExistsError if concurrent writing of the
    temporary file is attempted."""
    path_tmp = '{}.{}'.format(path, id(path))
    fd = _os.open(path_tmp, _os.O_EXCL | _os.O_CREAT | _os.O_WRONLY, mode & 438)
    try:
        with _io.FileIO(fd, 'wb') as file:
            file.write(data)
        _os.replace(path_tmp, path)
    except OSError:
        try:
            _os.unlink(path_tmp)
        except OSError:
            pass
        else:
            raise


_code_type = type(_write_atomic.__code__)
MAGIC_NUMBER = (3413).to_bytes(2, 'little') + b'\r\n'
_RAW_MAGIC_NUMBER = int.from_bytes(MAGIC_NUMBER, 'little')
_PYCACHE = '__pycache__'
_OPT = 'opt-'
SOURCE_SUFFIXES = [
 '.py']
BYTECODE_SUFFIXES = [
 '.pyc']
DEBUG_BYTECODE_SUFFIXES = OPTIMIZED_BYTECODE_SUFFIXES = BYTECODE_SUFFIXES

def cache_from_source(path, debug_override=None, *, optimization=None):
    """Given the path to a .py file, return the path to its .pyc file.

    The .py file does not need to exist; this simply returns the path to the
    .pyc file calculated as if the .py file were imported.

    The 'optimization' parameter controls the presumed optimization level of
    the bytecode file. If 'optimization' is not None, the string representation
    of the argument is taken and verified to be alphanumeric (else ValueError
    is raised).

    The debug_override parameter is deprecated. If debug_override is not None,
    a True value is the same as setting 'optimization' to the empty string
    while a False value is equivalent to setting 'optimization' to '1'.

    If sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    if debug_override is not None:
        _warnings.warn("the debug_override parameter is deprecated; use 'optimization' instead", DeprecationWarning)
        if optimization is not None:
            message = 'debug_override or optimization must be set to None'
            raise TypeError(message)
        optimization = '' if debug_override else 1
    path = _os.fspath(path)
    head, tail = _path_split(path)
    base, sep, rest = tail.rpartition('.')
    tag = sys.implementation.cache_tag
    if tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    almost_filename = ''.join([base if base else rest, sep, tag])
    if optimization is None:
        if sys.flags.optimize == 0:
            optimization = ''
        else:
            optimization = sys.flags.optimize
    optimization = str(optimization)
    if optimization != '':
        if not optimization.isalnum():
            raise ValueError('{!r} is not alphanumeric'.format(optimization))
        almost_filename = '{}.{}{}'.format(almost_filename, _OPT, optimization)
    filename = almost_filename + BYTECODE_SUFFIXES[0]
    if sys.pycache_prefix is not None:
        if not _path_isabs(head):
            head = _path_join(_os.getcwd(), head)
        if head[1] == ':':
            if head[0] not in path_separators:
                head = head[2:]
        return _path_join(sys.pycache_prefix, head.lstrip(path_separators), filename)
    return _path_join(head, _PYCACHE, filename)


def source_from_cache(path):
    """Given the path to a .pyc. file, return the path to its .py file.

    The .pyc file does not need to exist; this simply returns the path to
    the .py file calculated to correspond to the .pyc file.  If path does
    not conform to PEP 3147/488 format, ValueError will be raised. If
    sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    if sys.implementation.cache_tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    path = _os.fspath(path)
    head, pycache_filename = _path_split(path)
    found_in_pycache_prefix = False
    if sys.pycache_prefix is not None:
        stripped_path = sys.pycache_prefix.rstrip(path_separators)
        if head.startswith(stripped_path + path_sep):
            head = head[len(stripped_path):]
            found_in_pycache_prefix = True
    if not found_in_pycache_prefix:
        head, pycache = _path_split(head)
        if pycache != _PYCACHE:
            raise ValueError(f"{_PYCACHE} not bottom-level directory in {path!r}")
    dot_count = pycache_filename.count('.')
    if dot_count not in frozenset({2, 3}):
        raise ValueError(f"expected only 2 or 3 dots in {pycache_filename!r}")
    else:
        pass
    if dot_count == 3:
        optimization = pycache_filename.rsplit('.', 2)[(-2)]
        if not optimization.startswith(_OPT):
            raise ValueError(f"optimization portion of filename does not start with {_OPT!r}")
        opt_level = optimization[len(_OPT):]
        if not opt_level.isalnum():
            raise ValueError(f"optimization level {optimization!r} is not an alphanumeric value")
        base_filename = pycache_filename.partition('.')[0]
        return _path_join(head, base_filename + SOURCE_SUFFIXES[0])


def _get_sourcefile(bytecode_path):
    """Convert a bytecode file path to a source path (if possible).

    This function exists purely for backwards-compatibility for
    PyImport_ExecCodeModuleWithFilenames() in the C API.

    """
    if len(bytecode_path) == 0:
        return
    rest, _, extension = bytecode_path.rpartition('.')
    if not rest or extension.lower()[-3:-1] != 'py':
        return bytecode_path
    try:
        source_path = source_from_cache(bytecode_path)
    except (NotImplementedError, ValueError):
        source_path = bytecode_path[:-1]
    else:
        if _path_isfile(source_path):
            return source_path
        else:
            return bytecode_path


def _get_cached--- This code section failed: ---

 L. 425         0  LOAD_FAST                'filename'
                2  LOAD_METHOD              endswith
                4  LOAD_GLOBAL              tuple
                6  LOAD_GLOBAL              SOURCE_SUFFIXES
                8  CALL_FUNCTION_1       1  ''
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_FALSE    48  'to 48'

 L. 426        14  SETUP_FINALLY        26  'to 26'

 L. 427        16  LOAD_GLOBAL              cache_from_source
               18  LOAD_FAST                'filename'
               20  CALL_FUNCTION_1       1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    14  '14'

 L. 428        26  DUP_TOP          
               28  LOAD_GLOBAL              NotImplementedError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 429        40  POP_EXCEPT       
               42  JUMP_FORWARD         70  'to 70'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
               46  JUMP_FORWARD         70  'to 70'
             48_0  COME_FROM            12  '12'

 L. 430        48  LOAD_FAST                'filename'
               50  LOAD_METHOD              endswith
               52  LOAD_GLOBAL              tuple
               54  LOAD_GLOBAL              BYTECODE_SUFFIXES
               56  CALL_FUNCTION_1       1  ''
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 431        62  LOAD_FAST                'filename'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 433        66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM            46  '46'
             70_1  COME_FROM            42  '42'

Parse error at or near `COME_FROM' instruction at offset 44_0


def _calc_mode(path):
    """Calculate the mode permissions for a bytecode file."""
    try:
        mode = _path_stat(path).st_mode
    except OSError:
        mode = 438
    else:
        mode |= 128
        return mode


def _check_name(method):
    """Decorator to verify that the module being requested matches the one the
    loader can handle.

    The first argument (self) must define _name which the second argument is
    compared against. If the comparison fails then ImportError is raised.

    """

    def _check_name_wrapper(self, name=None, *args, **kwargs):
        if name is None:
            name = self.name
        elif self.name != name:
            raise ImportError(('loader for %s cannot handle %s' % (
             self.name, name)),
              name=name)
        return method(self, name, *args, **kwargs)

    try:
        _wrap = _bootstrap._wrap
    except NameError:

        def _wrap(new, old):
            for replace in ('__module__', '__name__', '__qualname__', '__doc__'):
                if hasattr(old, replace):
                    setattr(new, replace, getattr(old, replace))
            else:
                new.__dict__.update(old.__dict__)

    else:
        _wrap(_check_name_wrapper, method)
        return _check_name_wrapper


def _find_module_shim(self, fullname):
    """Try to find a loader for the specified module by delegating to
    self.find_loader().

    This method is deprecated in favor of finder.find_spec().

    """
    loader, portions = self.find_loader(fullname)
    if loader is None:
        if len(portions):
            msg = 'Not importing directory {}: missing __init__'
            _warnings.warn(msg.format(portions[0]), ImportWarning)
    return loader


def _classify_pyc(data, name, exc_details):
    """Perform basic validity checking of a pyc header and return the flags field,
    which determines how the pyc should be further validated against the source.

    *data* is the contents of the pyc file. (Only the first 16 bytes are
    required, though.)

    *name* is the name of the module being imported. It is used for logging.

    *exc_details* is a dictionary passed to ImportError if it raised for
    improved debugging.

    ImportError is raised when the magic number is incorrect or when the flags
    field is invalid. EOFError is raised when the data is found to be truncated.

    """
    magic = data[:4]
    if magic != MAGIC_NUMBER:
        message = f"bad magic number in {name!r}: {magic!r}"
        _bootstrap._verbose_message('{}', message)
        raise ImportError(message, **exc_details)
    if len(data) < 16:
        message = f"reached EOF while reading pyc header of {name!r}"
        _bootstrap._verbose_message('{}', message)
        raise EOFError(message)
    flags = _unpack_uint32(data[4:8])
    if flags & -4:
        message = f"invalid flags {flags!r} in {name!r}"
        raise ImportError(message, **exc_details)
    return flags


def _validate_timestamp_pyc(data, source_mtime, source_size, name, exc_details):
    """Validate a pyc against the source last-modified time.

    *data* is the contents of the pyc file. (Only the first 16 bytes are
    required.)

    *source_mtime* is the last modified timestamp of the source file.

    *source_size* is None or the size of the source file in bytes.

    *name* is the name of the module being imported. It is used for logging.

    *exc_details* is a dictionary passed to ImportError if it raised for
    improved debugging.

    An ImportError is raised if the bytecode is stale.

    """
    if _unpack_uint32(data[8:12]) != source_mtime & 4294967295:
        message = f"bytecode is stale for {name!r}"
        _bootstrap._verbose_message('{}', message)
        raise ImportError(message, **exc_details)
    if source_size is not None:
        if _unpack_uint32(data[12:16]) != source_size & 4294967295:
            raise ImportError(f"bytecode is stale for {name!r}", **exc_details)


def _validate_hash_pyc(data, source_hash, name, exc_details):
    """Validate a hash-based pyc by checking the real source hash against the one in
    the pyc header.

    *data* is the contents of the pyc file. (Only the first 16 bytes are
    required.)

    *source_hash* is the importlib.util.source_hash() of the source file.

    *name* is the name of the module being imported. It is used for logging.

    *exc_details* is a dictionary passed to ImportError if it raised for
    improved debugging.

    An ImportError is raised if the bytecode is stale.

    """
    if data[8:16] != source_hash:
        raise ImportError(
         f"hash in bytecode doesn't match hash of source {name!r}", **exc_details)


def _compile_bytecode(data, name=None, bytecode_path=None, source_path=None):
    """Compile bytecode as found in a pyc."""
    code = marshal.loads(data)
    if isinstance(code, _code_type):
        _bootstrap._verbose_message('code object from {!r}', bytecode_path)
        if source_path is not None:
            _imp._fix_co_filename(code, source_path)
        return code
    raise ImportError(('Non-code object in {!r}'.format(bytecode_path)), name=name,
      path=bytecode_path)


def _code_to_timestamp_pyc(code, mtime=0, source_size=0):
    """Produce the data for a timestamp-based pyc."""
    data = bytearray(MAGIC_NUMBER)
    data.extend(_pack_uint32(0))
    data.extend(_pack_uint32(mtime))
    data.extend(_pack_uint32(source_size))
    data.extend(marshal.dumps(code))
    return data


def _code_to_hash_pyc(code, source_hash, checked=True):
    """Produce the data for a hash-based pyc."""
    data = bytearray(MAGIC_NUMBER)
    flags = 1 | checked << 1
    data.extend(_pack_uint32(flags))
    assert len(source_hash) == 8
    data.extend(source_hash)
    data.extend(marshal.dumps(code))
    return data


def decode_source(source_bytes):
    """Decode bytes representing source code and return the string.

    Universal newline support is used in the decoding.
    """
    import tokenize
    source_bytes_readline = _io.BytesIO(source_bytes).readline
    encoding = tokenize.detect_encoding(source_bytes_readline)
    newline_decoder = _io.IncrementalNewlineDecoder(None, True)
    return newline_decoder.decode(source_bytes.decode(encoding[0]))


_POPULATE = object()

def spec_from_file_location(name, location=None, *, loader=None, submodule_search_locations=_POPULATE):
    """Return a module spec based on a file location.

    To indicate that the module is a package, set
    submodule_search_locations to a list of directory paths.  An
    empty list is sufficient, though its not otherwise useful to the
    import system.

    The loader must take a spec as its only __init__() arg.

    """
    if location is None:
        location = '<unknown>'
        if hasattr(loader, 'get_filename'):
            try:
                location = loader.get_filename(name)
            except ImportError:
                pass

    else:
        location = _os.fspath(location)
    spec = _bootstrap.ModuleSpec(name, loader, origin=location)
    spec._set_fileattr = True
    if loader is None:
        for loader_class, suffixes in _get_supported_file_loaders():
            if location.endswith(tuple(suffixes)):
                loader = loader_class(name, location)
                spec.loader = loader
                break
        else:
            return

    if submodule_search_locations is _POPULATE:
        if hasattr(loader, 'is_package'):
            try:
                is_package = loader.is_package(name)
            except ImportError:
                pass
            else:
                if is_package:
                    spec.submodule_search_locations = []
            spec.submodule_search_locations = submodule_search_locations
        if spec.submodule_search_locations == []:
            if location:
                dirname = _path_split(location)[0]
                spec.submodule_search_locations.append(dirname)
        return spec


class WindowsRegistryFinder:
    __doc__ = 'Meta path finder for modules declared in the Windows registry.'
    REGISTRY_KEY = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}'
    REGISTRY_KEY_DEBUG = 'Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}\\Debug'
    DEBUG_BUILD = False

    @classmethod
    def _open_registry(cls, key):
        try:
            return _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, key)
        except OSError:
            return _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)

    @classmethod
    def _search_registry(cls, fullname):
        if cls.DEBUG_BUILD:
            registry_key = cls.REGISTRY_KEY_DEBUG
        else:
            registry_key = cls.REGISTRY_KEY
        key = registry_key.format(fullname=fullname, sys_version=('%d.%d' % sys.version_info[:2]))
        try:
            with cls._open_registry(key) as hkey:
                filepath = _winreg.QueryValue(hkey, '')
        except OSError:
            return
        else:
            return filepath

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        filepath = cls._search_registry(fullname)
        if filepath is None:
            return
        try:
            _path_stat(filepath)
        except OSError:
            return
        else:
            for loader, suffixes in _get_supported_file_loaders():
                if filepath.endswith(tuple(suffixes)):
                    spec = _bootstrap.spec_from_loader(fullname, (loader(fullname, filepath)),
                      origin=filepath)
                    return spec

    @classmethod
    def find_module(cls, fullname, path=None):
        """Find module named in the registry.

        This method is deprecated.  Use exec_module() instead.

        """
        spec = cls.find_spec(fullname, path)
        if spec is not None:
            return spec.loader
        return


class _LoaderBasics:
    __doc__ = 'Base class of common code needed by both SourceLoader and\n    SourcelessFileLoader.'

    def is_package(self, fullname):
        """Concrete implementation of InspectLoader.is_package by checking if
        the path returned by get_filename has a filename of '__init__.py'."""
        filename = _path_split(self.get_filename(fullname))[1]
        filename_base = filename.rsplit('.', 1)[0]
        tail_name = fullname.rpartition('.')[2]
        return filename_base == '__init__' and tail_name != '__init__'

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module(self, module):
        """Execute the module."""
        code = self.get_code(module.__name__)
        if code is None:
            raise ImportError('cannot load module {!r} when get_code() returns None'.format(module.__name__))
        _bootstrap._call_with_frames_removed(exec, code, module.__dict__)

    def load_module(self, fullname):
        """This module is deprecated."""
        return _bootstrap._load_module_shim(self, fullname)


class SourceLoader(_LoaderBasics):

    def path_mtime(self, path):
        """Optional method that returns the modification time (an int) for the
        specified path (a str).

        Raises OSError when the path cannot be handled.
        """
        raise OSError

    def path_stats(self, path):
        """Optional method returning a metadata dict for the specified
        path (a str).

        Possible keys:
        - 'mtime' (mandatory) is the numeric timestamp of last source
          code modification;
        - 'size' (optional) is the size in bytes of the source code.

        Implementing this method allows the loader to read bytecode files.
        Raises OSError when the path cannot be handled.
        """
        return {'mtime': self.path_mtime(path)}

    def _cache_bytecode(self, source_path, cache_path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.

        The source path is needed in order to correctly transfer permissions
        """
        return self.set_data(cache_path, data)

    def set_data(self, path, data):
        """Optional method which writes data (bytes) to a file path (a str).

        Implementing this method allows for the writing of bytecode files.
        """
        pass

    def get_source(self, fullname):
        """Concrete implementation of InspectLoader.get_source."""
        path = self.get_filename(fullname)
        try:
            source_bytes = self.get_data(path)
        except OSError as exc:
            try:
                raise ImportError('source not available through get_data()', name=fullname) from exc
            finally:
                exc = None
                del exc

        else:
            return decode_source(source_bytes)

    def source_to_code(self, data, path, *, _optimize=-1):
        """Return the code object compiled from source.

        The 'data' argument can be any object type that compile() supports.
        """
        return _bootstrap._call_with_frames_removed(compile, data, path, 'exec', dont_inherit=True,
          optimize=_optimize)

    def get_code(self, fullname):
        """Concrete implementation of InspectLoader.get_code.

        Reading of bytecode requires path_stats to be implemented. To write
        bytecode, set_data must also be implemented.

        """
        source_path = self.get_filename(fullname)
        source_mtime = None
        source_bytes = None
        source_hash = None
        hash_based = False
        check_source = True
        try:
            bytecode_path = cache_from_source(source_path)
        except NotImplementedError:
            bytecode_path = None

        try:
            st = self.path_stats(source_path)
        except OSError:
            pass
        else:
            source_mtime = int(st['mtime'])
            try:
                data = self.get_data(bytecode_path)
            except OSError:
                pass
            else:
                exc_details = {'name':fullname,  'path':bytecode_path}
                try:
                    flags = _classify_pyc(data, fullname, exc_details)
                    bytes_data = memoryview(data)[16:]
                    hash_based = flags & 1 != 0
                    if hash_based:
                        check_source = flags & 2 != 0
                        if _imp.check_hash_based_pycs != 'never':
                            if check_source or _imp.check_hash_based_pycs == 'always':
                                source_bytes = self.get_data(source_path)
                                source_hash = _imp.source_hash(_RAW_MAGIC_NUMBER, source_bytes)
                                _validate_hash_pyc(data, source_hash, fullname, exc_details)
                    else:
                        _validate_timestamp_pyc(data, source_mtime, st['size'], fullname, exc_details)
                except (ImportError, EOFError):
                    pass
                else:
                    _bootstrap._verbose_message('{} matches {}', bytecode_path, source_path)
                    return _compile_bytecode(bytes_data, name=fullname, bytecode_path=bytecode_path,
                      source_path=source_path)
                if source_bytes is None:
                    source_bytes = self.get_data(source_path)
                code_object = self.source_to_code(source_bytes, source_path)
                _bootstrap._verbose_message('code object from {}', source_path)
                if not sys.dont_write_bytecode:
                    if bytecode_path is not None:
                        if source_mtime is not None:
                            if hash_based:
                                if source_hash is None:
                                    source_hash = _imp.source_hash(source_bytes)
                                data = _code_to_hash_pyc(code_object, source_hash, check_source)
                            else:
                                data = _code_to_timestamp_pyc(code_object, source_mtime, len(source_bytes))
                            try:
                                self._cache_bytecode(source_path, bytecode_path, data)
                            except NotImplementedError:
                                pass
                            else:
                                return code_object


class FileLoader:
    __doc__ = 'Base file loader class which implements the loader protocol methods that\n    require file system usage.'

    def __init__(self, fullname, path):
        """Cache the module name and the path to the file found by the
        finder."""
        self.name = fullname
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    @_check_name
    def load_module(self, fullname):
        return super(FileLoader, self).load_module(fullname)

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path

    def get_data(self, path):
        """Return the data from path as raw bytes."""
        if isinstance(self, (SourceLoader, ExtensionFileLoader)):
            with _io.open_code(str(path)) as file:
                return file.read()
        else:
            with _io.FileIO(path, 'r') as file:
                return file.read()

    @_check_name
    def get_resource_reader(self, module):
        if self.is_package(module):
            return self

    def open_resource(self, resource):
        path = _path_join(_path_split(self.path)[0], resource)
        return _io.FileIO(path, 'r')

    def resource_path(self, resource):
        if not self.is_resource(resource):
            raise FileNotFoundError
        path = _path_join(_path_split(self.path)[0], resource)
        return path

    def is_resource(self, name):
        if path_sep in name:
            return False
        path = _path_join(_path_split(self.path)[0], name)
        return _path_isfile(path)

    def contents(self):
        return iter(_os.listdir(_path_split(self.path)[0]))


class SourceFileLoader(FileLoader, SourceLoader):
    __doc__ = 'Concrete implementation of SourceLoader using the file system.'

    def path_stats(self, path):
        """Return the metadata for the path."""
        st = _path_stat(path)
        return {'mtime':st.st_mtime, 
         'size':st.st_size}

    def _cache_bytecode(self, source_path, bytecode_path, data):
        mode = _calc_mode(source_path)
        return self.set_data(bytecode_path, data, _mode=mode)

    def set_data--- This code section failed: ---

 L.1022         0  LOAD_GLOBAL              _path_split
                2  LOAD_FAST                'path'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'parent'
               10  STORE_FAST               'filename'

 L.1023        12  BUILD_LIST_0          0 
               14  STORE_FAST               'path_parts'
             16_0  COME_FROM            50  '50'

 L.1025        16  LOAD_FAST                'parent'
               18  POP_JUMP_IF_FALSE    52  'to 52'
               20  LOAD_GLOBAL              _path_isdir
               22  LOAD_FAST                'parent'
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_TRUE     52  'to 52'

 L.1026        28  LOAD_GLOBAL              _path_split
               30  LOAD_FAST                'parent'
               32  CALL_FUNCTION_1       1  ''
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'parent'
               38  STORE_FAST               'part'

 L.1027        40  LOAD_FAST                'path_parts'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'part'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_BACK            16  'to 16'
             52_0  COME_FROM            26  '26'
             52_1  COME_FROM            18  '18'

 L.1029        52  LOAD_GLOBAL              reversed
               54  LOAD_FAST                'path_parts'
               56  CALL_FUNCTION_1       1  ''
               58  GET_ITER         
             60_0  COME_FROM           168  '168'
             60_1  COME_FROM           164  '164'
             60_2  COME_FROM           110  '110'
             60_3  COME_FROM           106  '106'
             60_4  COME_FROM            88  '88'
               60  FOR_ITER            170  'to 170'
               62  STORE_FAST               'part'

 L.1030        64  LOAD_GLOBAL              _path_join
               66  LOAD_FAST                'parent'
               68  LOAD_FAST                'part'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'parent'

 L.1031        74  SETUP_FINALLY        90  'to 90'

 L.1032        76  LOAD_GLOBAL              _os
               78  LOAD_METHOD              mkdir
               80  LOAD_FAST                'parent'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_BACK            60  'to 60'
             90_0  COME_FROM_FINALLY    74  '74'

 L.1033        90  DUP_TOP          
               92  LOAD_GLOBAL              FileExistsError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   112  'to 112'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L.1035       104  POP_EXCEPT       
              106  JUMP_BACK            60  'to 60'
              108  POP_EXCEPT       
              110  JUMP_BACK            60  'to 60'
            112_0  COME_FROM            96  '96'

 L.1036       112  DUP_TOP          
              114  LOAD_GLOBAL              OSError
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   166  'to 166'
              120  POP_TOP          
              122  STORE_FAST               'exc'
              124  POP_TOP          
              126  SETUP_FINALLY       154  'to 154'

 L.1039       128  LOAD_GLOBAL              _bootstrap
              130  LOAD_METHOD              _verbose_message
              132  LOAD_STR                 'could not create {!r}: {!r}'

 L.1040       134  LOAD_FAST                'parent'

 L.1040       136  LOAD_FAST                'exc'

 L.1039       138  CALL_METHOD_3         3  ''
              140  POP_TOP          

 L.1041       142  POP_BLOCK        
              144  POP_EXCEPT       
              146  CALL_FINALLY        154  'to 154'
              148  POP_TOP          
              150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           146  '146'
            154_1  COME_FROM_FINALLY   126  '126'
              154  LOAD_CONST               None
              156  STORE_FAST               'exc'
              158  DELETE_FAST              'exc'
              160  END_FINALLY      
              162  POP_EXCEPT       
              164  JUMP_BACK            60  'to 60'
            166_0  COME_FROM           118  '118'
              166  END_FINALLY      
              168  JUMP_BACK            60  'to 60'
            170_0  COME_FROM            60  '60'

 L.1042       170  SETUP_FINALLY       200  'to 200'

 L.1043       172  LOAD_GLOBAL              _write_atomic
              174  LOAD_FAST                'path'
              176  LOAD_FAST                'data'
              178  LOAD_FAST                '_mode'
              180  CALL_FUNCTION_3       3  ''
              182  POP_TOP          

 L.1044       184  LOAD_GLOBAL              _bootstrap
              186  LOAD_METHOD              _verbose_message
              188  LOAD_STR                 'created {!r}'
              190  LOAD_FAST                'path'
              192  CALL_METHOD_2         2  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_FORWARD        248  'to 248'
            200_0  COME_FROM_FINALLY   170  '170'

 L.1045       200  DUP_TOP          
              202  LOAD_GLOBAL              OSError
              204  COMPARE_OP               exception-match
              206  POP_JUMP_IF_FALSE   246  'to 246'
              208  POP_TOP          
              210  STORE_FAST               'exc'
              212  POP_TOP          
              214  SETUP_FINALLY       234  'to 234'

 L.1047       216  LOAD_GLOBAL              _bootstrap
              218  LOAD_METHOD              _verbose_message
              220  LOAD_STR                 'could not create {!r}: {!r}'
              222  LOAD_FAST                'path'

 L.1048       224  LOAD_FAST                'exc'

 L.1047       226  CALL_METHOD_3         3  ''
              228  POP_TOP          
              230  POP_BLOCK        
              232  BEGIN_FINALLY    
            234_0  COME_FROM_FINALLY   214  '214'
              234  LOAD_CONST               None
              236  STORE_FAST               'exc'
              238  DELETE_FAST              'exc'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           206  '206'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           198  '198'

Parse error at or near `JUMP_BACK' instruction at offset 110


class SourcelessFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader which handles sourceless file imports.'

    def get_code(self, fullname):
        path = self.get_filename(fullname)
        data = self.get_data(path)
        exc_details = {'name':fullname, 
         'path':path}
        _classify_pyc(data, fullname, exc_details)
        return _compile_bytecode((memoryview(data)[16:]),
          name=fullname,
          bytecode_path=path)

    def get_source(self, fullname):
        """Return None as there is no source code."""
        pass


EXTENSION_SUFFIXES = []

class ExtensionFileLoader(FileLoader, _LoaderBasics):
    __doc__ = 'Loader for extension modules.\n\n    The constructor is designed to work with FileFinder.\n\n    '

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name) ^ hash(self.path)

    def create_module(self, spec):
        """Create an unitialized extension module"""
        module = _bootstrap._call_with_frames_removed(_imp.create_dynamic, spec)
        _bootstrap._verbose_message('extension module {!r} loaded from {!r}', spec.name, self.path)
        return module

    def exec_module(self, module):
        """Initialize an extension module"""
        _bootstrap._call_with_frames_removed(_imp.exec_dynamic, module)
        _bootstrap._verbose_message('extension module {!r} executed from {!r}', self.name, self.path)

    def is_package(self, fullname):
        """Return True if the extension module is a package."""
        file_name = _path_split(self.path)[1]
        return any((file_name == '__init__' + suffix for suffix in EXTENSION_SUFFIXES))

    def get_code(self, fullname):
        """Return None as an extension module cannot create a code object."""
        pass

    def get_source(self, fullname):
        """Return None as extension modules have no source code."""
        pass

    @_check_name
    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        return self.path


class _NamespacePath:
    __doc__ = "Represents a namespace package's path.  It uses the module name\n    to find its parent module, and from there it looks up the parent's\n    __path__.  When this changes, the module's own path is recomputed,\n    using path_finder.  For top-level modules, the parent module's path\n    is sys.path."

    def __init__(self, name, path, path_finder):
        self._name = name
        self._path = path
        self._last_parent_path = tuple(self._get_parent_path())
        self._path_finder = path_finder

    def _find_parent_path_names(self):
        """Returns a tuple of (parent-module-name, parent-path-attr-name)"""
        parent, dot, me = self._name.rpartition('.')
        if dot == '':
            return ('sys', 'path')
        return (
         parent, '__path__')

    def _get_parent_path(self):
        parent_module_name, path_attr_name = self._find_parent_path_names()
        return getattr(sys.modules[parent_module_name], path_attr_name)

    def _recalculate(self):
        parent_path = tuple(self._get_parent_path())
        if parent_path != self._last_parent_path:
            spec = self._path_finder(self._name, parent_path)
            if spec is not None:
                if spec.loader is None:
                    if spec.submodule_search_locations:
                        self._path = spec.submodule_search_locations
            self._last_parent_path = parent_path
        return self._path

    def __iter__(self):
        return iter(self._recalculate())

    def __getitem__(self, index):
        return self._recalculate()[index]

    def __setitem__(self, index, path):
        self._path[index] = path

    def __len__(self):
        return len(self._recalculate())

    def __repr__(self):
        return '_NamespacePath({!r})'.format(self._path)

    def __contains__(self, item):
        return item in self._recalculate()

    def append(self, item):
        self._path.append(item)


class _NamespaceLoader:

    def __init__(self, name, path, path_finder):
        self._path = _NamespacePath(name, path, path_finder)

    @classmethod
    def module_repr(cls, module):
        """Return repr for the module.

        The method is deprecated.  The import machinery does the job itself.

        """
        return '<module {!r} (namespace)>'.format(module.__name__)

    def is_package(self, fullname):
        return True

    def get_source(self, fullname):
        return ''

    def get_code(self, fullname):
        return compile('', '<string>', 'exec', dont_inherit=True)

    def create_module(self, spec):
        """Use default semantics for module creation."""
        pass

    def exec_module(self, module):
        pass

    def load_module(self, fullname):
        """Load a namespace module.

        This method is deprecated.  Use exec_module() instead.

        """
        _bootstrap._verbose_message('namespace module loaded with path {!r}', self._path)
        return _bootstrap._load_module_shim(self, fullname)


class PathFinder:
    __doc__ = 'Meta path finder for sys.path and package __path__ attributes.'

    @classmethod
    def invalidate_caches(cls):
        """Call the invalidate_caches() method on all path entry finders
        stored in sys.path_importer_caches (where implemented)."""
        for name, finder in list(sys.path_importer_cache.items()):
            if finder is None:
                del sys.path_importer_cache[name]
            else:
                if hasattr(finder, 'invalidate_caches'):
                    finder.invalidate_caches()

    @classmethod
    def _path_hooks--- This code section failed: ---

 L.1255         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                path_hooks
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    28  'to 28'
               10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                path_hooks
               14  POP_JUMP_IF_TRUE     28  'to 28'

 L.1256        16  LOAD_GLOBAL              _warnings
               18  LOAD_METHOD              warn
               20  LOAD_STR                 'sys.path_hooks is empty'
               22  LOAD_GLOBAL              ImportWarning
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          
             28_0  COME_FROM            14  '14'
             28_1  COME_FROM             8  '8'

 L.1257        28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                path_hooks
               32  GET_ITER         
             34_0  COME_FROM            78  '78'
             34_1  COME_FROM            74  '74'
             34_2  COME_FROM            70  '70'
               34  FOR_ITER             80  'to 80'
               36  STORE_FAST               'hook'

 L.1258        38  SETUP_FINALLY        54  'to 54'

 L.1259        40  LOAD_FAST                'hook'
               42  LOAD_FAST                'path'
               44  CALL_FUNCTION_1       1  ''
               46  POP_BLOCK        
               48  ROT_TWO          
               50  POP_TOP          
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    38  '38'

 L.1260        54  DUP_TOP          
               56  LOAD_GLOBAL              ImportError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    76  'to 76'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.1261        68  POP_EXCEPT       
               70  JUMP_BACK            34  'to 34'
               72  POP_EXCEPT       
               74  JUMP_BACK            34  'to 34'
             76_0  COME_FROM            60  '60'
               76  END_FINALLY      
               78  JUMP_BACK            34  'to 34'
             80_0  COME_FROM            34  '34'

Parse error at or near `POP_TOP' instruction at offset 50

    @classmethod
    def _path_importer_cache(cls, path):
        """Get the finder for the path entry from sys.path_importer_cache.

        If the path entry is not in the cache, find the appropriate finder
        and cache it. If no finder is available, store None.

        """
        if path == '':
            try:
                path = _os.getcwd()
            except FileNotFoundError:
                return

            try:
                finder = sys.path_importer_cache[path]
            except KeyError:
                finder = cls._path_hooks(path)
                sys.path_importer_cache[path] = finder

            return finder

    @classmethod
    def _legacy_get_spec(cls, fullname, finder):
        if hasattr(finder, 'find_loader'):
            loader, portions = finder.find_loader(fullname)
        else:
            loader = finder.find_module(fullname)
            portions = []
        if loader is not None:
            return _bootstrap.spec_from_loader(fullname, loader)
        spec = _bootstrap.ModuleSpec(fullname, None)
        spec.submodule_search_locations = portions
        return spec

    @classmethod
    def _get_spec(cls, fullname, path, target=None):
        """Find the loader or namespace_path for this module/package name."""
        namespace_path = []
        for entry in path:
            if not isinstance(entry, (str, bytes)):
                pass
            else:
                finder = cls._path_importer_cache(entry)
                if finder is not None:
                    if hasattr(finder, 'find_spec'):
                        spec = finder.find_spec(fullname, target)
                    else:
                        spec = cls._legacy_get_spec(fullname, finder)
                    if spec is None:
                        pass
                    else:
                        if spec.loader is not None:
                            return spec
                        portions = spec.submodule_search_locations
                if portions is None:
                    raise ImportError('spec missing loader')
                else:
                    namespace_path.extend(portions)
        else:
            spec = _bootstrap.ModuleSpec(fullname, None)
            spec.submodule_search_locations = namespace_path
            return spec

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        """Try to find a spec for 'fullname' on sys.path or 'path'.

        The search is based on sys.path_hooks and sys.path_importer_cache.
        """
        if path is None:
            path = sys.path
        spec = cls._get_spec(fullname, path, target)
        if spec is None:
            return
        if spec.loader is None:
            namespace_path = spec.submodule_search_locations
            if namespace_path:
                spec.origin = None
                spec.submodule_search_locations = _NamespacePath(fullname, namespace_path, cls._get_spec)
                return spec
            return
        else:
            return spec

    @classmethod
    def find_module(cls, fullname, path=None):
        """find the module on sys.path or 'path' based on sys.path_hooks and
        sys.path_importer_cache.

        This method is deprecated.  Use find_spec() instead.

        """
        spec = cls.find_spec(fullname, path)
        if spec is None:
            return
        return spec.loader

    @classmethod
    def find_distributions(cls, *args, **kwargs):
        """
        Find distributions.

        Return an iterable of all Distribution instances capable of
        loading the metadata for packages matching ``context.name``
        (or all names if ``None`` indicated) along the paths in the list
        of directories ``context.path``.
        """
        from importlib.metadata import MetadataPathFinder
        return (MetadataPathFinder.find_distributions)(*args, **kwargs)


class FileFinder:
    __doc__ = 'File-based finder.\n\n    Interactions with the file system are cached for performance, being\n    refreshed when the directory the finder is handling has been modified.\n\n    '

    def __init__(self, path, *loader_details):
        """Initialize with the path to search on and a variable number of
        2-tuples containing the loader and the file suffixes the loader
        recognizes."""
        loaders = []
        for loader, suffixes in loader_details:
            loaders.extend(((suffix, loader) for suffix in suffixes))
        else:
            self._loaders = loaders
            self.path = path or '.'
            self._path_mtime = -1
            self._path_cache = set()
            self._relaxed_path_cache = set()

    def invalidate_caches(self):
        """Invalidate the directory mtime."""
        self._path_mtime = -1

    find_module = _find_module_shim

    def find_loader(self, fullname):
        """Try to find a loader for the specified module, or the namespace
        package portions. Returns (loader, list-of-portions).

        This method is deprecated.  Use find_spec() instead.

        """
        spec = self.find_spec(fullname)
        if spec is None:
            return (None, [])
        return (spec.loader, spec.submodule_search_locations or [])

    def _get_spec(self, loader_class, fullname, path, smsl, target):
        loader = loader_class(fullname, path)
        return spec_from_file_location(fullname, path, loader=loader, submodule_search_locations=smsl)

    def find_spec(self, fullname, target=None):
        """Try to find a spec for the specified module.

        Returns the matching spec, or None if not found.
        """
        is_namespace = False
        tail_module = fullname.rpartition('.')[2]
        try:
            mtime = _path_stat(self.path or _os.getcwd()).st_mtime
        except OSError:
            mtime = -1
        else:
            if mtime != self._path_mtime:
                self._fill_cache()
                self._path_mtime = mtime
            if _relax_case():
                cache = self._relaxed_path_cache
                cache_module = tail_module.lower()
            else:
                cache = self._path_cache
                cache_module = tail_module
            if cache_module in cache:
                base_path = _path_join(self.path, tail_module)
                for suffix, loader_class in self._loaders:
                    init_filename = '__init__' + suffix
                    full_path = _path_join(base_path, init_filename)
                    if _path_isfile(full_path):
                        return self._get_spec(loader_class, fullname, full_path, [base_path], target)
                    is_namespace = _path_isdir(base_path)

        for suffix, loader_class in self._loaders:
            full_path = _path_join(self.path, tail_module + suffix)
            _bootstrap._verbose_message('trying {}', full_path, verbosity=2)
            if cache_module + suffix in cache:
                if _path_isfile(full_path):
                    return self._get_spec(loader_class, fullname, full_path, None, target)
        else:
            if is_namespace:
                _bootstrap._verbose_message('possible namespace for {}', base_path)
                spec = _bootstrap.ModuleSpec(fullname, None)
                spec.submodule_search_locations = [base_path]
                return spec

    def _fill_cache(self):
        """Fill the cache of potential modules and packages for this directory."""
        path = self.path
        try:
            contents = _os.listdir(path or _os.getcwd())
        except (FileNotFoundError, PermissionError, NotADirectoryError):
            contents = []
        else:
            if not sys.platform.startswith('win'):
                self._path_cache = set(contents)
            else:
                lower_suffix_contents = set()
                for item in contents:
                    name, dot, suffix = item.partition('.')
                    if dot:
                        new_name = '{}.{}'.format(name, suffix.lower())
                    else:
                        new_name = name
                    lower_suffix_contents.add(new_name)
                else:
                    self._path_cache = lower_suffix_contents

            if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
                self._relaxed_path_cache = {fn.lower() for fn in contents}

    @classmethod
    def path_hook(cls, *loader_details):
        """A class method which returns a closure to use on sys.path_hook
        which will return an instance using the specified loaders and the path
        called on the closure.

        If the path called on the closure is not a directory, ImportError is
        raised.

        """

        def path_hook_for_FileFinder(path):
            if not _path_isdir(path):
                raise ImportError('only directories are supported', path=path)
            return cls(path, *loader_details)

        return path_hook_for_FileFinder

    def __repr__(self):
        return 'FileFinder({!r})'.format(self.path)


def _fix_up_module(ns, name, pathname, cpathname=None):
    loader = ns.get('__loader__')
    spec = ns.get('__spec__')
    if not loader:
        if spec:
            loader = spec.loader
        elif pathname == cpathname:
            loader = SourcelessFileLoader(name, pathname)
        else:
            loader = SourceFileLoader(name, pathname)
    if not spec:
        spec = spec_from_file_location(name, pathname, loader=loader)
    try:
        ns['__spec__'] = spec
        ns['__loader__'] = loader
        ns['__file__'] = pathname
        ns['__cached__'] = cpathname
    except Exception:
        pass


def _get_supported_file_loaders():
    """Returns a list of file-based module loaders.

    Each item is a tuple (loader, suffixes).
    """
    extensions = (
     ExtensionFileLoader, _imp.extension_suffixes())
    source = (SourceFileLoader, SOURCE_SUFFIXES)
    bytecode = (SourcelessFileLoader, BYTECODE_SUFFIXES)
    return [
     extensions, source, bytecode]


def _setup--- This code section failed: ---

 L.1576         0  LOAD_FAST                '_bootstrap_module'
                2  STORE_GLOBAL             _bootstrap

 L.1577         4  LOAD_GLOBAL              _bootstrap
                6  LOAD_ATTR                sys
                8  STORE_GLOBAL             sys

 L.1578        10  LOAD_GLOBAL              _bootstrap
               12  LOAD_ATTR                _imp
               14  STORE_GLOBAL             _imp

 L.1581        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                modules
               20  LOAD_GLOBAL              __name__
               22  BINARY_SUBSCR    
               24  STORE_FAST               'self_module'

 L.1582        26  LOAD_CONST               ('_io', '_warnings', 'builtins', 'marshal')
               28  GET_ITER         
             30_0  COME_FROM            78  '78'
               30  FOR_ITER             80  'to 80'
               32  STORE_FAST               'builtin_name'

 L.1583        34  LOAD_FAST                'builtin_name'
               36  LOAD_GLOBAL              sys
               38  LOAD_ATTR                modules
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.1584        44  LOAD_GLOBAL              _bootstrap
               46  LOAD_METHOD              _builtin_from_name
               48  LOAD_FAST                'builtin_name'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'builtin_module'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM            42  '42'

 L.1586        56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                modules
               60  LOAD_FAST                'builtin_name'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'builtin_module'
             66_0  COME_FROM            54  '54'

 L.1587        66  LOAD_GLOBAL              setattr
               68  LOAD_FAST                'self_module'
               70  LOAD_FAST                'builtin_name'
               72  LOAD_FAST                'builtin_module'
               74  CALL_FUNCTION_3       3  ''
               76  POP_TOP          
               78  JUMP_BACK            30  'to 30'
             80_0  COME_FROM            30  '30'

 L.1590        80  LOAD_STR                 'posix'
               82  LOAD_STR                 '/'
               84  BUILD_LIST_1          1 
               86  BUILD_TUPLE_2         2 
               88  LOAD_STR                 'nt'
               90  LOAD_STR                 '\\'
               92  LOAD_STR                 '/'
               94  BUILD_LIST_2          2 
               96  BUILD_TUPLE_2         2 
               98  BUILD_TUPLE_2         2 
              100  STORE_FAST               'os_details'

 L.1591       102  LOAD_FAST                'os_details'
              104  GET_ITER         
            106_0  COME_FROM           216  '216'
            106_1  COME_FROM           212  '212'
            106_2  COME_FROM           208  '208'
            106_3  COME_FROM           190  '190'
            106_4  COME_FROM           168  '168'
              106  FOR_ITER            218  'to 218'
              108  UNPACK_SEQUENCE_2     2 
              110  STORE_FAST               'builtin_os'
              112  STORE_FAST               'path_separators'

 L.1593       114  LOAD_GLOBAL              all
              116  LOAD_GENEXPR             '<code_object <genexpr>>'
              118  LOAD_STR                 '_setup.<locals>.<genexpr>'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              122  LOAD_FAST                'path_separators'
              124  GET_ITER         
              126  CALL_FUNCTION_1       1  ''
              128  CALL_FUNCTION_1       1  ''
              130  POP_JUMP_IF_TRUE    136  'to 136'
              132  LOAD_ASSERT              AssertionError
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           130  '130'

 L.1594       136  LOAD_FAST                'path_separators'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  STORE_FAST               'path_sep'

 L.1595       144  LOAD_FAST                'builtin_os'
              146  LOAD_GLOBAL              sys
              148  LOAD_ATTR                modules
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   170  'to 170'

 L.1596       154  LOAD_GLOBAL              sys
              156  LOAD_ATTR                modules
              158  LOAD_FAST                'builtin_os'
              160  BINARY_SUBSCR    
              162  STORE_FAST               'os_module'

 L.1597       164  POP_TOP          
              166  BREAK_LOOP          226  'to 226'
              168  JUMP_BACK           106  'to 106'
            170_0  COME_FROM           152  '152'

 L.1599       170  SETUP_FINALLY       192  'to 192'

 L.1600       172  LOAD_GLOBAL              _bootstrap
              174  LOAD_METHOD              _builtin_from_name
              176  LOAD_FAST                'builtin_os'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'os_module'

 L.1601       182  POP_BLOCK        
              184  POP_TOP          
              186  JUMP_FORWARD        226  'to 226'
              188  POP_BLOCK        
              190  JUMP_BACK           106  'to 106'
            192_0  COME_FROM_FINALLY   170  '170'

 L.1602       192  DUP_TOP          
              194  LOAD_GLOBAL              ImportError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   214  'to 214'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L.1603       206  POP_EXCEPT       
              208  JUMP_BACK           106  'to 106'
              210  POP_EXCEPT       
              212  JUMP_BACK           106  'to 106'
            214_0  COME_FROM           198  '198'
              214  END_FINALLY      
              216  JUMP_BACK           106  'to 106'
            218_0  COME_FROM           106  '106'

 L.1605       218  LOAD_GLOBAL              ImportError
              220  LOAD_STR                 'importlib requires posix or nt'
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           186  '186'
            226_1  COME_FROM           166  '166'

 L.1606       226  LOAD_GLOBAL              setattr
              228  LOAD_FAST                'self_module'
              230  LOAD_STR                 '_os'
              232  LOAD_FAST                'os_module'
              234  CALL_FUNCTION_3       3  ''
              236  POP_TOP          

 L.1607       238  LOAD_GLOBAL              setattr
              240  LOAD_FAST                'self_module'
              242  LOAD_STR                 'path_sep'
              244  LOAD_FAST                'path_sep'
              246  CALL_FUNCTION_3       3  ''
              248  POP_TOP          

 L.1608       250  LOAD_GLOBAL              setattr
              252  LOAD_FAST                'self_module'
              254  LOAD_STR                 'path_separators'
              256  LOAD_STR                 ''
              258  LOAD_METHOD              join
              260  LOAD_FAST                'path_separators'
              262  CALL_METHOD_1         1  ''
              264  CALL_FUNCTION_3       3  ''
              266  POP_TOP          

 L.1609       268  LOAD_GLOBAL              setattr
              270  LOAD_FAST                'self_module'
              272  LOAD_STR                 '_pathseps_with_colon'
              274  LOAD_SETCOMP             '<code_object <setcomp>>'
              276  LOAD_STR                 '_setup.<locals>.<setcomp>'
              278  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              280  LOAD_FAST                'path_separators'
              282  GET_ITER         
              284  CALL_FUNCTION_1       1  ''
              286  CALL_FUNCTION_3       3  ''
              288  POP_TOP          

 L.1612       290  LOAD_GLOBAL              _bootstrap
              292  LOAD_METHOD              _builtin_from_name
              294  LOAD_STR                 '_thread'
              296  CALL_METHOD_1         1  ''
              298  STORE_FAST               'thread_module'

 L.1613       300  LOAD_GLOBAL              setattr
              302  LOAD_FAST                'self_module'
              304  LOAD_STR                 '_thread'
              306  LOAD_FAST                'thread_module'
              308  CALL_FUNCTION_3       3  ''
              310  POP_TOP          

 L.1616       312  LOAD_GLOBAL              _bootstrap
              314  LOAD_METHOD              _builtin_from_name
              316  LOAD_STR                 '_weakref'
              318  CALL_METHOD_1         1  ''
              320  STORE_FAST               'weakref_module'

 L.1617       322  LOAD_GLOBAL              setattr
              324  LOAD_FAST                'self_module'
              326  LOAD_STR                 '_weakref'
              328  LOAD_FAST                'weakref_module'
              330  CALL_FUNCTION_3       3  ''
              332  POP_TOP          

 L.1620       334  LOAD_FAST                'builtin_os'
              336  LOAD_STR                 'nt'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   366  'to 366'

 L.1621       344  LOAD_GLOBAL              _bootstrap
              346  LOAD_METHOD              _builtin_from_name
              348  LOAD_STR                 'winreg'
              350  CALL_METHOD_1         1  ''
              352  STORE_FAST               'winreg_module'

 L.1622       354  LOAD_GLOBAL              setattr
              356  LOAD_FAST                'self_module'
              358  LOAD_STR                 '_winreg'
              360  LOAD_FAST                'winreg_module'
              362  CALL_FUNCTION_3       3  ''
              364  POP_TOP          
            366_0  COME_FROM           340  '340'

 L.1625       366  LOAD_GLOBAL              setattr
              368  LOAD_FAST                'self_module'
              370  LOAD_STR                 '_relax_case'
              372  LOAD_GLOBAL              _make_relax_case
              374  CALL_FUNCTION_0       0  ''
              376  CALL_FUNCTION_3       3  ''
              378  POP_TOP          

 L.1626       380  LOAD_GLOBAL              EXTENSION_SUFFIXES
              382  LOAD_METHOD              extend
              384  LOAD_GLOBAL              _imp
              386  LOAD_METHOD              extension_suffixes
              388  CALL_METHOD_0         0  ''
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

 L.1627       394  LOAD_FAST                'builtin_os'
              396  LOAD_STR                 'nt'
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   430  'to 430'

 L.1628       404  LOAD_GLOBAL              SOURCE_SUFFIXES
              406  LOAD_METHOD              append
              408  LOAD_STR                 '.pyw'
              410  CALL_METHOD_1         1  ''
              412  POP_TOP          

 L.1629       414  LOAD_STR                 '_d.pyd'
              416  LOAD_GLOBAL              EXTENSION_SUFFIXES
              418  COMPARE_OP               in
          420_422  POP_JUMP_IF_FALSE   430  'to 430'

 L.1630       424  LOAD_CONST               True
              426  LOAD_GLOBAL              WindowsRegistryFinder
              428  STORE_ATTR               DEBUG_BUILD
            430_0  COME_FROM           420  '420'
            430_1  COME_FROM           400  '400'

Parse error at or near `JUMP_BACK' instruction at offset 212


def _install(_bootstrap_module):
    """Install the path-based import components."""
    _setup(_bootstrap_module)
    supported_loaders = _get_supported_file_loaders()
    sys.path_hooks.extend([(FileFinder.path_hook)(*supported_loaders)])
    sys.meta_path.append(PathFinder)