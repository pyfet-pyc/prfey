# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pathlib.py
import fnmatch, functools, io, ntpath, os, posixpath, re, sys
from _collections_abc import Sequence
from errno import EINVAL, ENOENT, ENOTDIR, EBADF, ELOOP
from operator import attrgetter
from stat import S_ISDIR, S_ISLNK, S_ISREG, S_ISSOCK, S_ISBLK, S_ISCHR, S_ISFIFO
import urllib.parse as urlquote_from_bytes
supports_symlinks = True
if os.name == 'nt':
    import nt
    if sys.getwindowsversion()[:2] >= (6, 0):
        from nt import _getfinalpathname
    else:
        supports_symlinks = False
        _getfinalpathname = None
else:
    nt = None
__all__ = [
 'PurePath', 'PurePosixPath', 'PureWindowsPath',
 'Path', 'PosixPath', 'WindowsPath']
_IGNORED_ERROS = (
 ENOENT, ENOTDIR, EBADF, ELOOP)
_IGNORED_WINERRORS = (21, 1921)

def _ignore_error(exception):
    return getattr(exception, 'errno', None) in _IGNORED_ERROS or getattr(exception, 'winerror', None) in _IGNORED_WINERRORS


def _is_wildcard_pattern(pat):
    return '*' in pat or '?' in pat or '[' in pat


class _Flavour(object):
    __doc__ = 'A flavour implements a particular (platform-specific) set of path\n    semantics.'

    def __init__(self):
        self.join = self.sep.join

    def parse_parts(self, parts):
        parsed = []
        sep = self.sep
        altsep = self.altsep
        drv = root = ''
        it = reversed(parts)
        for part in it:
            if not part:
                pass
            else:
                if altsep:
                    part = part.replace(altsep, sep)
                else:
                    drv, root, rel = self.splitroot(part)
                    if sep in rel:
                        for x in reversed(rel.split(sep)):
                            if x:
                                if x != '.':
                                    parsed.append(sys.intern(x))

                    elif rel:
                        if rel != '.':
                            parsed.append(sys.intern(rel))
                if not drv:
                    if root:
                        pass
                for part in drv or it:
                    if not part:
                        pass
                    else:
                        if altsep:
                            part = part.replace(altsep, sep)
                        else:
                            drv = self.splitroot(part)[0]
                        if drv:
                            break
                else:
                    break

        else:
            if drv or (root):
                parsed.append(drv + root)
            parsed.reverse()
            return (
             drv, root, parsed)

    def join_parsed_parts(self, drv, root, parts, drv2, root2, parts2):
        """
        Join the two paths represented by the respective
        (drive, root, parts) tuples.  Return a new (drive, root, parts) tuple.
        """
        if root2:
            if not drv2:
                if drv:
                    return (
                     drv, root2, [drv + root2] + parts2[1:])
        elif drv2:
            if drv2 == drv or self.casefold(drv2) == self.casefold(drv):
                return (
                 drv, root, parts + parts2[1:])
        else:
            return (
             drv, root, parts + parts2)
        return (drv2, root2, parts2)


class _WindowsFlavour(_Flavour):
    sep = '\\'
    altsep = '/'
    has_drv = True
    pathmod = ntpath
    is_supported = os.name == 'nt'
    drive_letters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ext_namespace_prefix = '\\\\?\\'
    reserved_names = {
     'CON', 'PRN', 'AUX', 'NUL'} | {'COM%d' % i for i in range(1, 10)} | {'LPT%d' % i for i in range(1, 10)}

    def splitroot(self, part, sep=sep):
        first = part[0:1]
        second = part[1:2]
        if second == sep and first == sep:
            prefix, part = self._split_extended_path(part)
            first = part[0:1]
            second = part[1:2]
        else:
            prefix = ''
        third = part[2:3]
        if second == sep:
            if first == sep:
                if third != sep:
                    index = part.find(sep, 2)
                    if index != -1:
                        index2 = part.find(sep, index + 1)
                        if index2 != index + 1:
                            if index2 == -1:
                                index2 = len(part)
                            if prefix:
                                return (prefix + part[1:index2], sep, part[index2 + 1:])
                            return (
                             part[:index2], sep, part[index2 + 1:])
        drv = root = ''
        if second == ':':
            if first in self.drive_letters:
                drv = part[:2]
                part = part[2:]
                first = third
        if first == sep:
            root = first
            part = part.lstrip(sep)
        return (prefix + drv, root, part)

    def casefold(self, s):
        return s.lower()

    def casefold_parts(self, parts):
        return [p.lower() for p in parts]

    def resolve(self, path, strict=False):
        s = str(path)
        if not s:
            return os.getcwd()
        previous_s = None
        if _getfinalpathname is not None:
            if strict:
                return self._ext_to_normal(_getfinalpathname(s))
            tail_parts = []
            while True:
                try:
                    s = self._ext_to_normal(_getfinalpathname(s))
                except FileNotFoundError:
                    previous_s = s
                    s, tail = os.path.split(s)
                    tail_parts.append(tail)
                    if previous_s == s:
                        return path
                else:
                    return (os.path.join)(s, *reversed(tail_parts))

    def _split_extended_path(self, s, ext_prefix=ext_namespace_prefix):
        prefix = ''
        if s.startswith(ext_prefix):
            prefix = s[:4]
            s = s[4:]
            if s.startswith('UNC\\'):
                prefix += s[:3]
                s = '\\' + s[3:]
        return (
         prefix, s)

    def _ext_to_normal(self, s):
        return self._split_extended_path(s)[1]

    def is_reserved(self, parts):
        if not parts:
            return False
        if parts[0].startswith('\\\\'):
            return False
        return parts[(-1)].partition('.')[0].upper() in self.reserved_names

    def make_uri(self, path):
        drive = path.drive
        if len(drive) == 2:
            if drive[1] == ':':
                rest = path.as_posix()[2:].lstrip('/')
                return 'file:///%s/%s' % (
                 drive, urlquote_from_bytes(rest.encode('utf-8')))
        return 'file:' + urlquote_from_bytes(path.as_posix().encode('utf-8'))

    def gethomedir(self, username):
        if 'HOME' in os.environ:
            userhome = os.environ['HOME']
        elif 'USERPROFILE' in os.environ:
            userhome = os.environ['USERPROFILE']
        elif 'HOMEPATH' in os.environ:
            try:
                drv = os.environ['HOMEDRIVE']
            except KeyError:
                drv = ''
            else:
                userhome = drv + os.environ['HOMEPATH']
        else:
            raise RuntimeError("Can't determine home directory")
        if username:
            if os.environ['USERNAME'] != username:
                drv, root, parts = self.parse_parts((userhome,))
                if parts[(-1)] != os.environ['USERNAME']:
                    raise RuntimeError("Can't determine home directory for %r" % username)
                parts[-1] = username
                if drv or root:
                    userhome = drv + root + self.join(parts[1:])
                else:
                    userhome = self.join(parts)
        return userhome


class _PosixFlavour(_Flavour):
    sep = '/'
    altsep = ''
    has_drv = False
    pathmod = posixpath
    is_supported = os.name != 'nt'

    def splitroot(self, part, sep=sep):
        if part and part[0] == sep:
            stripped_part = part.lstrip(sep)
            if len(part) - len(stripped_part) == 2:
                return ('', sep * 2, stripped_part)
            return (
             '', sep, stripped_part)
        else:
            return (
             '', '', part)

    def casefold(self, s):
        return s

    def casefold_parts(self, parts):
        return parts

    def resolve(self, path, strict=False):
        sep = self.sep
        accessor = path._accessor
        seen = {}

        def _resolve(path, rest):
            if rest.startswith(sep):
                path = ''
            for name in rest.split(sep):
                if name:
                    if name == '.':
                        pass
                    else:
                        if name == '..':
                            path, _, _ = path.rpartition(sep)
                        else:
                            newpath = path + sep + name
                            if newpath in seen:
                                path = seen[newpath]
                                if path is not None:
                                    pass
                                else:
                                    raise RuntimeError('Symlink loop from %r' % newpath)
                            else:
                                try:
                                    target = accessor.readlink(newpath)
                                except OSError as e:
                                    try:
                                        if e.errno != EINVAL:
                                            if strict:
                                                raise
                                        path = newpath
                                    finally:
                                        e = None
                                        del e

                                else:
                                    seen[newpath] = None
                                    path = _resolve(path, target)
                                    seen[newpath] = path
            else:
                return path

        base = '' if path.is_absolute() else os.getcwd()
        return _resolve(base, str(path)) or sep

    def is_reserved(self, parts):
        return False

    def make_uri(self, path):
        bpath = bytes(path)
        return 'file://' + urlquote_from_bytes(bpath)

    def gethomedir(self, username):
        if not username:
            try:
                return os.environ['HOME']
            except KeyError:
                import pwd
                return pwd.getpwuid(os.getuid()).pw_dir

        else:
            import pwd
            try:
                return pwd.getpwnam(username).pw_dir
            except KeyError:
                raise RuntimeError("Can't determine home directory for %r" % username)


_windows_flavour = _WindowsFlavour()
_posix_flavour = _PosixFlavour()

class _Accessor:
    __doc__ = 'An accessor implements a particular (system-specific or not) way of\n    accessing paths on the filesystem.'


class _NormalAccessor(_Accessor):
    stat = os.stat
    lstat = os.lstat
    open = os.open
    listdir = os.listdir
    scandir = os.scandir
    chmod = os.chmod
    if hasattr(os, 'lchmod'):
        lchmod = os.lchmod
    else:

        def lchmod(self, pathobj, mode):
            raise NotImplementedError('lchmod() not available on this system')

    mkdir = os.mkdir
    unlink = os.unlink
    link_to = os.link
    rmdir = os.rmdir
    rename = os.rename
    replace = os.replace
    if nt:
        if supports_symlinks:
            symlink = os.symlink
        else:

            def symlink(a, b, target_is_directory):
                raise NotImplementedError('symlink() not available on this system')

    else:

        @staticmethod
        def symlink(a, b, target_is_directory):
            return os.symlink(a, b)

    utime = os.utime

    def readlink(self, path):
        return os.readlink(path)


_normal_accessor = _NormalAccessor()

def _make_selector(pattern_parts):
    pat = pattern_parts[0]
    child_parts = pattern_parts[1:]
    if pat == '**':
        cls = _RecursiveWildcardSelector
    elif '**' in pat:
        raise ValueError("Invalid pattern: '**' can only be an entire path component")
    elif _is_wildcard_pattern(pat):
        cls = _WildcardSelector
    else:
        cls = _PreciseSelector
    return cls(pat, child_parts)


if hasattr(functools, 'lru_cache'):
    _make_selector = functools.lru_cache()(_make_selector)

class _Selector:
    __doc__ = 'A selector matches a specific glob pattern part against the children\n    of a given path.'

    def __init__(self, child_parts):
        self.child_parts = child_parts
        if child_parts:
            self.successor = _make_selector(child_parts)
            self.dironly = True
        else:
            self.successor = _TerminatingSelector()
            self.dironly = False

    def select_from(self, parent_path):
        """Iterate over all child paths of `parent_path` matched by this
        selector.  This can contain parent_path itself."""
        path_cls = type(parent_path)
        is_dir = path_cls.is_dir
        exists = path_cls.exists
        scandir = parent_path._accessor.scandir
        if not is_dir(parent_path):
            return iter([])
        return self._select_from(parent_path, is_dir, exists, scandir)


class _TerminatingSelector:

    def _select_from(self, parent_path, is_dir, exists, scandir):
        yield parent_path


class _PreciseSelector(_Selector):

    def __init__(self, name, child_parts):
        self.name = name
        _Selector.__init__(self, child_parts)

    def _select_from(self, parent_path, is_dir, exists, scandir):
        try:
            path = parent_path._make_child_relpath(self.name)
            if is_dir if self.dironly else exists(path):
                for p in self.successor._select_from(path, is_dir, exists, scandir):
                    yield p

        except PermissionError:
            return


class _WildcardSelector(_Selector):

    def __init__(self, pat, child_parts):
        self.pat = re.compile(fnmatch.translate(pat))
        _Selector.__init__(self, child_parts)

    def _select_from(self, parent_path, is_dir, exists, scandir):
        try:
            cf = parent_path._flavour.casefold
            entries = list(scandir(parent_path))
            for entry in entries:
                entry_is_dir = False
                try:
                    entry_is_dir = entry.is_dir()
                except OSError as e:
                    try:
                        if not _ignore_error(e):
                            raise
                    finally:
                        e = None
                        del e

                else:
                    if self.dironly:
                        if entry_is_dir:
                            pass
                        name = entry.name
                        casefolded = cf(name)
                    if self.pat.match(casefolded):
                        path = parent_path._make_child_relpath(name)
                        for p in self.successor._select_from(path, is_dir, exists, scandir):
                            yield p

        except PermissionError:
            return


class _RecursiveWildcardSelector(_Selector):

    def __init__(self, pat, child_parts):
        _Selector.__init__(self, child_parts)

    def _iterate_directories(self, parent_path, is_dir, scandir):
        yield parent_path
        try:
            entries = list(scandir(parent_path))
            for entry in entries:
                entry_is_dir = False
                try:
                    entry_is_dir = entry.is_dir()
                except OSError as e:
                    try:
                        if not _ignore_error(e):
                            raise
                    finally:
                        e = None
                        del e

                else:
                    if entry_is_dir:
                        if not entry.is_symlink():
                            path = parent_path._make_child_relpath(entry.name)
                            for p in self._iterate_directories(path, is_dir, scandir):
                                yield p

        except PermissionError:
            return

    def _select_from(self, parent_path, is_dir, exists, scandir):
        try:
            yielded = set()
            try:
                successor_select = self.successor._select_from
                for starting_point in self._iterate_directories(parent_path, is_dir, scandir):
                    for p in successor_select(starting_point, is_dir, exists, scandir):
                        if p not in yielded:
                            yield p
                            yielded.add(p)

            finally:
                yielded.clear()

        except PermissionError:
            return


class _PathParents(Sequence):
    __doc__ = "This object provides sequence-like access to the logical ancestors\n    of a path.  Don't try to construct it yourself."
    __slots__ = ('_pathcls', '_drv', '_root', '_parts')

    def __init__(self, path):
        self._pathcls = type(path)
        self._drv = path._drv
        self._root = path._root
        self._parts = path._parts

    def __len__(self):
        if self._drv or (self._root):
            return len(self._parts) - 1
        return len(self._parts)

    def __getitem__(self, idx):
        if idx < 0 or (idx >= len(self)):
            raise IndexError(idx)
        return self._pathcls._from_parsed_parts(self._drv, self._root, self._parts[:-idx - 1])

    def __repr__(self):
        return '<{}.parents>'.format(self._pathcls.__name__)


class PurePath(object):
    __doc__ = "Base class for manipulating paths without I/O.\n\n    PurePath represents a filesystem path and offers operations which\n    don't imply any actual filesystem I/O.  Depending on your system,\n    instantiating a PurePath will return either a PurePosixPath or a\n    PureWindowsPath object.  You can also instantiate either of these classes\n    directly, regardless of your system.\n    "
    __slots__ = ('_drv', '_root', '_parts', '_str', '_hash', '_pparts', '_cached_cparts')

    def __new__(cls, *args):
        """Construct a PurePath from one or several strings and or existing
        PurePath objects.  The strings and path objects are combined so as
        to yield a canonicalized path, which is incorporated into the
        new PurePath object.
        """
        if cls is PurePath:
            cls = PureWindowsPath if os.name == 'nt' else PurePosixPath
        return cls._from_parts(args)

    def __reduce__(self):
        return (
         self.__class__, tuple(self._parts))

    @classmethod
    def _parse_args(cls, args):
        parts = []
        for a in args:
            if isinstance(a, PurePath):
                parts += a._parts
            else:
                a = os.fspath(a)
                if isinstance(a, str):
                    parts.append(str(a))
                else:
                    raise TypeError('argument should be a str object or an os.PathLike object returning str, not %r' % type(a))
        else:
            return cls._flavour.parse_parts(parts)

    @classmethod
    def _from_parts(cls, args, init=True):
        self = object.__new__(cls)
        drv, root, parts = self._parse_args(args)
        self._drv = drv
        self._root = root
        self._parts = parts
        if init:
            self._init()
        return self

    @classmethod
    def _from_parsed_parts(cls, drv, root, parts, init=True):
        self = object.__new__(cls)
        self._drv = drv
        self._root = root
        self._parts = parts
        if init:
            self._init()
        return self

    @classmethod
    def _format_parsed_parts(cls, drv, root, parts):
        if drv or (root):
            return drv + root + cls._flavour.join(parts[1:])
        return cls._flavour.join(parts)

    def _init(self):
        pass

    def _make_child(self, args):
        drv, root, parts = self._parse_args(args)
        drv, root, parts = self._flavour.join_parsed_parts(self._drv, self._root, self._parts, drv, root, parts)
        return self._from_parsed_parts(drv, root, parts)

    def __str__(self):
        """Return the string representation of the path, suitable for
        passing to system calls."""
        try:
            return self._str
        except AttributeError:
            self._str = self._format_parsed_parts(self._drv, self._root, self._parts) or '.'
            return self._str

    def __fspath__(self):
        return str(self)

    def as_posix(self):
        """Return the string representation of the path with forward (/)
        slashes."""
        f = self._flavour
        return str(self).replace(f.sep, '/')

    def __bytes__(self):
        """Return the bytes representation of the path.  This is only
        recommended to use under Unix."""
        return os.fsencode(self)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.as_posix())

    def as_uri(self):
        """Return the path as a 'file' URI."""
        if not self.is_absolute():
            raise ValueError("relative path can't be expressed as a file URI")
        return self._flavour.make_uri(self)

    @property
    def _cparts(self):
        try:
            return self._cached_cparts
        except AttributeError:
            self._cached_cparts = self._flavour.casefold_parts(self._parts)
            return self._cached_cparts

    def __eq__(self, other):
        if not isinstance(other, PurePath):
            return NotImplemented
        return self._cparts == other._cparts and self._flavour is other._flavour

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(tuple(self._cparts))
            return self._hash

    def __lt__(self, other):
        if not isinstance(other, PurePath) or self._flavour is not other._flavour:
            return NotImplemented
        return self._cparts < other._cparts

    def __le__(self, other):
        if not isinstance(other, PurePath) or self._flavour is not other._flavour:
            return NotImplemented
        return self._cparts <= other._cparts

    def __gt__(self, other):
        if not isinstance(other, PurePath) or self._flavour is not other._flavour:
            return NotImplemented
        return self._cparts > other._cparts

    def __ge__(self, other):
        if not isinstance(other, PurePath) or self._flavour is not other._flavour:
            return NotImplemented
        return self._cparts >= other._cparts

    drive = property((attrgetter('_drv')), doc='The drive prefix (letter or UNC path), if any.')
    root = property((attrgetter('_root')), doc='The root of the path, if any.')

    @property
    def anchor(self):
        """The concatenation of the drive and root, or ''."""
        anchor = self._drv + self._root
        return anchor

    @property
    def name(self):
        """The final path component, if any."""
        parts = self._parts
        if len(parts) == 1 if (self._drv or self._root) else 0:
            return ''
        return parts[(-1)]

    @property
    def suffix(self):
        """The final component's last suffix, if any."""
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[i:]
        return ''

    @property
    def suffixes(self):
        """A list of the final component's suffixes, if any."""
        name = self.name
        if name.endswith('.'):
            return []
        name = name.lstrip('.')
        return ['.' + suffix for suffix in name.split('.')[1:]]

    @property
    def stem(self):
        """The final path component, minus its last suffix."""
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[:i]
        return name

    def with_name(self, name):
        """Return a new path with the file name changed."""
        if not self.name:
            raise ValueError('%r has an empty name' % (self,))
        drv, root, parts = self._flavour.parse_parts((name,))
        if name:
            if name[(-1)] in (self._flavour.sep, self._flavour.altsep) or (drv or root or len(parts) != 1):
                raise ValueError('Invalid name %r' % name)
            return self._from_parsed_parts(self._drv, self._root, self._parts[:-1] + [name])

    def with_suffix--- This code section failed: ---

 L. 841         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _flavour
                4  STORE_FAST               'f'

 L. 842         6  LOAD_FAST                'f'
                8  LOAD_ATTR                sep
               10  LOAD_FAST                'suffix'
               12  COMPARE_OP               in
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  LOAD_FAST                'f'
               18  LOAD_ATTR                altsep
               20  POP_JUMP_IF_FALSE    46  'to 46'
               22  LOAD_FAST                'f'
               24  LOAD_ATTR                altsep
               26  LOAD_FAST                'suffix'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    46  'to 46'
             32_0  COME_FROM            14  '14'

 L. 843        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'Invalid suffix %r'
               36  LOAD_FAST                'suffix'
               38  BUILD_TUPLE_1         1 
               40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            30  '30'
             46_1  COME_FROM            20  '20'

 L. 844        46  LOAD_FAST                'suffix'
               48  POP_JUMP_IF_FALSE    60  'to 60'
               50  LOAD_FAST                'suffix'
               52  LOAD_METHOD              startswith
               54  LOAD_STR                 '.'
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_FALSE    68  'to 68'
             60_0  COME_FROM            48  '48'
               60  LOAD_FAST                'suffix'
               62  LOAD_STR                 '.'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'
             68_0  COME_FROM            58  '58'

 L. 845        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 'Invalid suffix %r'
               72  LOAD_FAST                'suffix'
               74  BINARY_MODULO    
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            66  '66'

 L. 846        80  LOAD_FAST                'self'
               82  LOAD_ATTR                name
               84  STORE_FAST               'name'

 L. 847        86  LOAD_FAST                'name'
               88  POP_JUMP_IF_TRUE    104  'to 104'

 L. 848        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 '%r has an empty name'
               94  LOAD_FAST                'self'
               96  BUILD_TUPLE_1         1 
               98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            88  '88'

 L. 849       104  LOAD_FAST                'self'
              106  LOAD_ATTR                suffix
              108  STORE_FAST               'old_suffix'

 L. 850       110  LOAD_FAST                'old_suffix'
              112  POP_JUMP_IF_TRUE    124  'to 124'

 L. 851       114  LOAD_FAST                'name'
              116  LOAD_FAST                'suffix'
              118  BINARY_ADD       
              120  STORE_FAST               'name'
              122  JUMP_FORWARD        146  'to 146'
            124_0  COME_FROM           112  '112'

 L. 853       124  LOAD_FAST                'name'
              126  LOAD_CONST               None
              128  LOAD_GLOBAL              len
              130  LOAD_FAST                'old_suffix'
              132  CALL_FUNCTION_1       1  ''
              134  UNARY_NEGATIVE   
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  LOAD_FAST                'suffix'
              142  BINARY_ADD       
              144  STORE_FAST               'name'
            146_0  COME_FROM           122  '122'

 L. 854       146  LOAD_FAST                'self'
              148  LOAD_METHOD              _from_parsed_parts
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _drv
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _root

 L. 855       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _parts
              162  LOAD_CONST               None
              164  LOAD_CONST               -1
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'name'
              172  BUILD_LIST_1          1 
              174  BINARY_ADD       

 L. 854       176  CALL_METHOD_3         3  ''
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 178

    def relative_to--- This code section failed: ---

 L. 866         0  LOAD_FAST                'other'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 867         4  LOAD_GLOBAL              TypeError
                6  LOAD_STR                 'need at least one argument'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 868        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _parts
               16  STORE_FAST               'parts'

 L. 869        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _drv
               22  STORE_FAST               'drv'

 L. 870        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _root
               28  STORE_FAST               'root'

 L. 871        30  LOAD_FAST                'root'
               32  POP_JUMP_IF_FALSE    56  'to 56'

 L. 872        34  LOAD_FAST                'drv'
               36  LOAD_FAST                'root'
               38  BUILD_LIST_2          2 
               40  LOAD_FAST                'parts'
               42  LOAD_CONST               1
               44  LOAD_CONST               None
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  BINARY_ADD       
               52  STORE_FAST               'abs_parts'
               54  JUMP_FORWARD         60  'to 60'
             56_0  COME_FROM            32  '32'

 L. 874        56  LOAD_FAST                'parts'
               58  STORE_FAST               'abs_parts'
             60_0  COME_FROM            54  '54'

 L. 875        60  LOAD_FAST                'self'
               62  LOAD_METHOD              _parse_args
               64  LOAD_FAST                'other'
               66  CALL_METHOD_1         1  ''
               68  UNPACK_SEQUENCE_3     3 
               70  STORE_FAST               'to_drv'
               72  STORE_FAST               'to_root'
               74  STORE_FAST               'to_parts'

 L. 876        76  LOAD_FAST                'to_root'
               78  POP_JUMP_IF_FALSE   102  'to 102'

 L. 877        80  LOAD_FAST                'to_drv'
               82  LOAD_FAST                'to_root'
               84  BUILD_LIST_2          2 
               86  LOAD_FAST                'to_parts'
               88  LOAD_CONST               1
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  BINARY_ADD       
               98  STORE_FAST               'to_abs_parts'
              100  JUMP_FORWARD        106  'to 106'
            102_0  COME_FROM            78  '78'

 L. 879       102  LOAD_FAST                'to_parts'
              104  STORE_FAST               'to_abs_parts'
            106_0  COME_FROM           100  '100'

 L. 880       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'to_abs_parts'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'n'

 L. 881       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _flavour
              118  LOAD_ATTR                casefold_parts
              120  STORE_FAST               'cf'

 L. 882       122  LOAD_FAST                'n'
              124  LOAD_CONST               0
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   140  'to 140'
              130  LOAD_FAST                'root'
              132  POP_JUMP_IF_TRUE    164  'to 164'
              134  LOAD_FAST                'drv'
              136  POP_JUMP_IF_FALSE   202  'to 202'
              138  JUMP_FORWARD        164  'to 164'
            140_0  COME_FROM           128  '128'
              140  LOAD_FAST                'cf'
              142  LOAD_FAST                'abs_parts'
              144  LOAD_CONST               None
              146  LOAD_FAST                'n'
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_FAST                'cf'
              156  LOAD_FAST                'to_abs_parts'
              158  CALL_FUNCTION_1       1  ''
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   202  'to 202'
            164_0  COME_FROM           138  '138'
            164_1  COME_FROM           132  '132'

 L. 883       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _format_parsed_parts
              168  LOAD_FAST                'to_drv'
              170  LOAD_FAST                'to_root'
              172  LOAD_FAST                'to_parts'
              174  CALL_METHOD_3         3  ''
              176  STORE_FAST               'formatted'

 L. 884       178  LOAD_GLOBAL              ValueError
              180  LOAD_STR                 '{!r} does not start with {!r}'
              182  LOAD_METHOD              format

 L. 885       184  LOAD_GLOBAL              str
              186  LOAD_FAST                'self'
              188  CALL_FUNCTION_1       1  ''

 L. 885       190  LOAD_GLOBAL              str
              192  LOAD_FAST                'formatted'
              194  CALL_FUNCTION_1       1  ''

 L. 884       196  CALL_METHOD_2         2  ''
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           162  '162'
            202_1  COME_FROM           136  '136'

 L. 886       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _from_parsed_parts
              206  LOAD_STR                 ''
              208  LOAD_FAST                'n'
              210  LOAD_CONST               1
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   220  'to 220'
              216  LOAD_FAST                'root'
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           214  '214'
              220  LOAD_STR                 ''
            222_0  COME_FROM           218  '218'

 L. 887       222  LOAD_FAST                'abs_parts'
              224  LOAD_FAST                'n'
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    

 L. 886       232  CALL_METHOD_3         3  ''
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 234

    @property
    def parts(self):
        """An object providing sequence-like access to the
        components in the filesystem path."""
        try:
            return self._pparts
        except AttributeError:
            self._pparts = tuple(self._parts)
            return self._pparts

    def joinpath(self, *args):
        """Combine this path with one or several arguments, and return a
        new path representing either a subpath (if all arguments are relative
        paths) or a totally different path (if one of the arguments is
        anchored).
        """
        return self._make_child(args)

    def __truediv__(self, key):
        try:
            return self._make_child((key,))
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, key):
        try:
            return self._from_parts([key] + self._parts)
        except TypeError:
            return NotImplemented

    @property
    def parent(self):
        """The logical parent of the path."""
        drv = self._drv
        root = self._root
        parts = self._parts
        if len(parts) == 1:
            if drv or (root):
                return self
            return self._from_parsed_parts(drv, root, parts[:-1])

    @property
    def parents(self):
        """A sequence of this path's logical parents."""
        return _PathParents(self)

    def is_absolute(self):
        """True if the path is absolute (has both a root and, if applicable,
        a drive)."""
        if not self._root:
            return False
        return not self._flavour.has_drv or bool(self._drv)

    def is_reserved(self):
        """Return True if the path contains one of the special names reserved
        by the system, if any."""
        return self._flavour.is_reserved(self._parts)

    def match(self, path_pattern):
        """
        Return True if this path matches the given pattern.
        """
        cf = self._flavour.casefold
        path_pattern = cf(path_pattern)
        drv, root, pat_parts = self._flavour.parse_parts((path_pattern,))
        if not pat_parts:
            raise ValueError('empty pattern')
        if drv:
            if drv != cf(self._drv):
                return False
        if root:
            if root != cf(self._root):
                return False
        parts = self._cparts
        if drv or root:
            if len(pat_parts) != len(parts):
                return False
            pat_parts = pat_parts[1:]
        elif len(pat_parts) > len(parts):
            return False
        for part, pat in zip(reversed(parts), reversed(pat_parts)):
            if not fnmatch.fnmatchcase(part, pat):
                return False
        else:
            return True


os.PathLike.register(PurePath)

class PurePosixPath(PurePath):
    __doc__ = 'PurePath subclass for non-Windows systems.\n\n    On a POSIX system, instantiating a PurePath should return this object.\n    However, you can also instantiate it directly on any system.\n    '
    _flavour = _posix_flavour
    __slots__ = ()


class PureWindowsPath(PurePath):
    __doc__ = 'PurePath subclass for Windows systems.\n\n    On a Windows system, instantiating a PurePath should return this object.\n    However, you can also instantiate it directly on any system.\n    '
    _flavour = _windows_flavour
    __slots__ = ()


class Path(PurePath):
    __doc__ = 'PurePath subclass that can make system calls.\n\n    Path represents a filesystem path but unlike PurePath, also offers\n    methods to do system calls on path objects. Depending on your system,\n    instantiating a Path will return either a PosixPath or a WindowsPath\n    object. You can also instantiate a PosixPath or WindowsPath directly,\n    but cannot instantiate a WindowsPath on a POSIX system or vice versa.\n    '
    __slots__ = ('_accessor', '_closed')

    def __new__(cls, *args, **kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError('cannot instantiate %r on your system' % (
             cls.__name__,))
        self._init()
        return self

    def _init(self, template=None):
        self._closed = False
        if template is not None:
            self._accessor = template._accessor
        else:
            self._accessor = _normal_accessor

    def _make_child_relpath(self, part):
        parts = self._parts + [part]
        return self._from_parsed_parts(self._drv, self._root, parts)

    def __enter__(self):
        if self._closed:
            self._raise_closed()
        return self

    def __exit__(self, t, v, tb):
        self._closed = True

    def _raise_closed(self):
        raise ValueError('I/O operation on closed path')

    def _opener(self, name, flags, mode=438):
        return self._accessor.open(self, flags, mode)

    def _raw_open(self, flags, mode=511):
        """
        Open the file pointed by this path and return a file descriptor,
        as os.open() does.
        """
        if self._closed:
            self._raise_closed()
        return self._accessor.open(self, flags, mode)

    @classmethod
    def cwd(cls):
        """Return a new path pointing to the current working directory
        (as returned by os.getcwd()).
        """
        return cls(os.getcwd())

    @classmethod
    def home(cls):
        """Return a new path pointing to the user's home directory (as
        returned by os.path.expanduser('~')).
        """
        return cls(cls()._flavour.gethomedir(None))

    def samefile(self, other_path):
        """Return whether other_path is the same or not as this file
        (as returned by os.path.samefile()).
        """
        st = self.stat()
        try:
            other_st = other_path.stat()
        except AttributeError:
            other_st = os.stat(other_path)
        else:
            return os.path.samestat(st, other_st)

    def iterdir(self):
        """Iterate over the files in this directory.  Does not yield any
        result for the special paths '.' and '..'.
        """
        if self._closed:
            self._raise_closed()
        for name in self._accessor.listdir(self):
            if name in frozenset({'..', '.'}):
                pass
            else:
                yield self._make_child_relpath(name)
                if self._closed:
                    self._raise_closed()

    def glob(self, pattern):
        """Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.
        """
        if not pattern:
            raise ValueError('Unacceptable pattern: {!r}'.format(pattern))
        pattern = self._flavour.casefold(pattern)
        drv, root, pattern_parts = self._flavour.parse_parts((pattern,))
        if drv or (root):
            raise NotImplementedError('Non-relative patterns are unsupported')
        selector = _make_selector(tuple(pattern_parts))
        for p in selector.select_from(self):
            yield p

    def rglob(self, pattern):
        """Recursively yield all existing files (of any kind, including
        directories) matching the given relative pattern, anywhere in
        this subtree.
        """
        pattern = self._flavour.casefold(pattern)
        drv, root, pattern_parts = self._flavour.parse_parts((pattern,))
        if drv or (root):
            raise NotImplementedError('Non-relative patterns are unsupported')
        selector = _make_selector(('**', ) + tuple(pattern_parts))
        for p in selector.select_from(self):
            yield p

    def absolute(self):
        """Return an absolute version of this path.  This function works
        even if the path doesn't point to anything.

        No normalization is done, i.e. all '.' and '..' will be kept along.
        Use resolve() to get the canonical path to a file.
        """
        if self._closed:
            self._raise_closed()
        if self.is_absolute():
            return self
        obj = self._from_parts(([os.getcwd()] + self._parts), init=False)
        obj._init(template=self)
        return obj

    def resolve(self, strict=False):
        """
        Make the path absolute, resolving all symlinks on the way and also
        normalizing it (for example turning slashes into backslashes under
        Windows).
        """
        if self._closed:
            self._raise_closed()
        s = self._flavour.resolve(self, strict=strict)
        if s is None:
            self.stat()
            s = str(self.absolute())
        normed = self._flavour.pathmod.normpath(s)
        obj = self._from_parts((normed,), init=False)
        obj._init(template=self)
        return obj

    def stat(self):
        """
        Return the result of the stat() system call on this path, like
        os.stat() does.
        """
        return self._accessor.stat(self)

    def owner(self):
        """
        Return the login name of the file owner.
        """
        import pwd
        return pwd.getpwuid(self.stat().st_uid).pw_name

    def group(self):
        """
        Return the group name of the file gid.
        """
        import grp
        return grp.getgrgid(self.stat().st_gid).gr_name

    def open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None):
        """
        Open the file pointed by this path and return a file object, as
        the built-in open() function does.
        """
        if self._closed:
            self._raise_closed()
        return io.open(self, mode, buffering, encoding, errors, newline, opener=(self._opener))

    def read_bytes(self):
        """
        Open the file in bytes mode, read it, and close the file.
        """
        with self.open(mode='rb') as f:
            return f.read()

    def read_text(self, encoding=None, errors=None):
        """
        Open the file in text mode, read it, and close the file.
        """
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
            return f.read()

    def write_bytes(self, data):
        """
        Open the file in bytes mode, write to it, and close the file.
        """
        view = memoryview(data)
        with self.open(mode='wb') as f:
            return f.write(view)

    def write_text(self, data, encoding=None, errors=None):
        """
        Open the file in text mode, write to it, and close the file.
        """
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' % data.__class__.__name__)
        with self.open(mode='w', encoding=encoding, errors=errors) as f:
            return f.write(data)

    def touch(self, mode=438, exist_ok=True):
        """
        Create this file with the given access mode, if it doesn't exist.
        """
        if self._closed:
            self._raise_closed()
        if exist_ok:
            try:
                self._accessor.utime(self, None)
            except OSError:
                pass
            else:
                return
            flags = os.O_CREAT | os.O_WRONLY
            exist_ok or flags |= os.O_EXCL
        fd = self._raw_open(flags, mode)
        os.close(fd)

    def mkdir(self, mode=511, parents=False, exist_ok=False):
        """
        Create a new directory at this given path.
        """
        if self._closed:
            self._raise_closed()
        try:
            self._accessor.mkdir(self, mode)
        except FileNotFoundError:
            if not parents or self.parent == self:
                raise
            else:
                self.parent.mkdir(parents=True, exist_ok=True)
                self.mkdir(mode, parents=False, exist_ok=exist_ok)
        except OSError:
            if not (exist_ok and self.is_dir()):
                raise

    def chmod(self, mode):
        """
        Change the permissions of the path, like os.chmod().
        """
        if self._closed:
            self._raise_closed()
        self._accessor.chmod(self, mode)

    def lchmod(self, mode):
        """
        Like chmod(), except if the path points to a symlink, the symlink's
        permissions are changed, rather than its target's.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.lchmod(self, mode)

    def unlink(self, missing_ok=False):
        """
        Remove this file or link.
        If the path is a directory, use rmdir() instead.
        """
        if self._closed:
            self._raise_closed()
        try:
            self._accessor.unlink(self)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def rmdir(self):
        """
        Remove this directory.  The directory must be empty.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.rmdir(self)

    def lstat(self):
        """
        Like stat(), except if the path points to a symlink, the symlink's
        status information is returned, rather than its target's.
        """
        if self._closed:
            self._raise_closed()
        return self._accessor.lstat(self)

    def link_to(self, target):
        """
        Create a hard link pointing to a path named target.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.link_to(self, target)

    def rename(self, target):
        """
        Rename this path to the given path,
        and return a new Path instance pointing to the given path.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.rename(self, target)
        return self.__class__(target)

    def replace(self, target):
        """
        Rename this path to the given path, clobbering the existing
        destination if it exists, and return a new Path instance
        pointing to the given path.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.replace(self, target)
        return self.__class__(target)

    def symlink_to(self, target, target_is_directory=False):
        """
        Make this path a symlink pointing to the given path.
        Note the order of arguments (self, target) is the reverse of os.symlink's.
        """
        if self._closed:
            self._raise_closed()
        self._accessor.symlink(target, self, target_is_directory)

    def exists--- This code section failed: ---

 L.1369         0  SETUP_FINALLY        14  'to 14'

 L.1370         2  LOAD_FAST                'self'
                4  LOAD_METHOD              stat
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         84  'to 84'
             14_0  COME_FROM_FINALLY     0  '0'

 L.1371        14  DUP_TOP          
               16  LOAD_GLOBAL              OSError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    62  'to 62'
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        50  'to 50'

 L.1372        30  LOAD_GLOBAL              _ignore_error
               32  LOAD_FAST                'e'
               34  CALL_FUNCTION_1       1  ''
               36  POP_JUMP_IF_TRUE     40  'to 40'

 L.1373        38  RAISE_VARARGS_0       0  'reraise'
             40_0  COME_FROM            36  '36'

 L.1374        40  POP_BLOCK        
               42  POP_EXCEPT       
               44  CALL_FINALLY         50  'to 50'
               46  LOAD_CONST               False
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM_FINALLY    28  '28'
               50  LOAD_CONST               None
               52  STORE_FAST               'e'
               54  DELETE_FAST              'e'
               56  END_FINALLY      
               58  POP_EXCEPT       
               60  JUMP_FORWARD         84  'to 84'
             62_0  COME_FROM            20  '20'

 L.1375        62  DUP_TOP          
               64  LOAD_GLOBAL              ValueError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    82  'to 82'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L.1377        76  POP_EXCEPT       
               78  LOAD_CONST               False
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'
               82  END_FINALLY      
             84_0  COME_FROM            60  '60'
             84_1  COME_FROM            12  '12'

 L.1378        84  LOAD_CONST               True
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 44

    def is_dir--- This code section failed: ---

 L.1384         0  SETUP_FINALLY        18  'to 18'

 L.1385         2  LOAD_GLOBAL              S_ISDIR
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1386        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1387        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1388        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1391        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1392        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1394        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_file--- This code section failed: ---

 L.1401         0  SETUP_FINALLY        18  'to 18'

 L.1402         2  LOAD_GLOBAL              S_ISREG
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1403        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1404        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1405        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1408        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1409        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1411        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_mount(self):
        """
        Check if this path is a POSIX mount point
        """
        if not (self.exists() and self.is_dir()):
            return False
        parent = Path(self.parent)
        try:
            parent_dev = parent.stat().st_dev
        except OSError:
            return False
        else:
            dev = self.stat().st_dev
            if dev != parent_dev:
                return True
            else:
                ino = self.stat().st_ino
                parent_ino = parent.stat().st_ino
                return ino == parent_ino

    def is_symlink--- This code section failed: ---

 L.1438         0  SETUP_FINALLY        18  'to 18'

 L.1439         2  LOAD_GLOBAL              S_ISLNK
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              lstat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1440        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1441        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1442        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1444        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1445        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1447        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_block_device--- This code section failed: ---

 L.1453         0  SETUP_FINALLY        18  'to 18'

 L.1454         2  LOAD_GLOBAL              S_ISBLK
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1455        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1456        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1457        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1460        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1461        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1463        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_char_device--- This code section failed: ---

 L.1469         0  SETUP_FINALLY        18  'to 18'

 L.1470         2  LOAD_GLOBAL              S_ISCHR
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1471        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1472        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1473        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1476        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1477        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1479        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_fifo--- This code section failed: ---

 L.1485         0  SETUP_FINALLY        18  'to 18'

 L.1486         2  LOAD_GLOBAL              S_ISFIFO
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1487        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1488        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1489        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1492        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1493        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1495        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def is_socket--- This code section failed: ---

 L.1501         0  SETUP_FINALLY        18  'to 18'

 L.1502         2  LOAD_GLOBAL              S_ISSOCK
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              stat
                8  CALL_METHOD_0         0  ''
               10  LOAD_ATTR                st_mode
               12  CALL_FUNCTION_1       1  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.1503        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.1504        34  LOAD_GLOBAL              _ignore_error
               36  LOAD_FAST                'e'
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.1505        42  RAISE_VARARGS_0       0  'reraise'
             44_0  COME_FROM            40  '40'

 L.1508        44  POP_BLOCK        
               46  POP_EXCEPT       
               48  CALL_FINALLY         54  'to 54'
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            24  '24'

 L.1509        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1511        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'
               86  END_FINALLY      
             88_0  COME_FROM            64  '64'

Parse error at or near `POP_EXCEPT' instruction at offset 46

    def expanduser(self):
        """ Return a new path with expanded ~ and ~user constructs
        (as returned by os.path.expanduser)
        """
        if not self._drv:
            if not self._root:
                if self._parts:
                    if self._parts[0][:1] == '~':
                        homedir = self._flavour.gethomedir(self._parts[0][1:])
                        return self._from_parts([homedir] + self._parts[1:])
            return self


class PosixPath(Path, PurePosixPath):
    __doc__ = 'Path subclass for non-Windows systems.\n\n    On a POSIX system, instantiating a Path should return this object.\n    '
    __slots__ = ()


class WindowsPath(Path, PureWindowsPath):
    __doc__ = 'Path subclass for Windows systems.\n\n    On a Windows system, instantiating a Path should return this object.\n    '
    __slots__ = ()

    def owner(self):
        raise NotImplementedError('Path.owner() is unsupported on this system')

    def group(self):
        raise NotImplementedError('Path.group() is unsupported on this system')

    def is_mount(self):
        raise NotImplementedError('Path.is_mount() is unsupported on this system')