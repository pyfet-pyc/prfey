# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: ntpath.py
"""Common pathname manipulations, WindowsNT/95 version.

Instead of importing this module directly, import os and refer to this
module as os.path.
"""
curdir = '.'
pardir = '..'
extsep = '.'
sep = '\\'
pathsep = ';'
altsep = '/'
defpath = '.;C:\\bin'
devnull = 'nul'
import os, sys, stat, genericpath
from genericpath import *
__all__ = [
 'normcase', 'isabs', 'join', 'splitdrive', 'split', 'splitext',
 'basename', 'dirname', 'commonprefix', 'getsize', 'getmtime',
 'getatime', 'getctime', 'islink', 'exists', 'lexists', 'isdir', 'isfile',
 'ismount', 'expanduser', 'expandvars', 'normpath', 'abspath',
 'curdir', 'pardir', 'sep', 'pathsep', 'defpath', 'altsep',
 'extsep', 'devnull', 'realpath', 'supports_unicode_filenames', 'relpath',
 'samefile', 'sameopenfile', 'samestat', 'commonpath']

def _get_bothseps(path):
    if isinstance(path, bytes):
        return '\\/'
    return '\\/'


def normcase(s):
    """Normalize case of pathname.

    Makes all characters lowercase and all slashes into backslashes."""
    s = os.fspath(s)
    try:
        if isinstance(s, bytes):
            return s.replace('/', '\\').lower()
        return s.replace('/', '\\').lower()
    except (TypeError, AttributeError):
        if not isinstance(s, (bytes, str)):
            raise TypeError('normcase() argument must be str or bytes, not %r' % s.__class__.__name__) from None
        else:
            raise


def isabs(s):
    """Test whether a path is absolute"""
    s = os.fspath(s)
    s = splitdrive(s)[1]
    return len(s) > 0 and s[0] in _get_bothseps(s)


def join--- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'path'

 L.  77        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.  78        20  LOAD_STR                 '\\'
               22  STORE_FAST               'sep'

 L.  79        24  LOAD_STR                 '\\/'
               26  STORE_FAST               'seps'

 L.  80        28  LOAD_STR                 ':'
               30  STORE_FAST               'colon'
               32  JUMP_FORWARD         46  'to 46'
             34_0  COME_FROM            18  '18'

 L.  82        34  LOAD_STR                 '\\'
               36  STORE_FAST               'sep'

 L.  83        38  LOAD_STR                 '\\/'
               40  STORE_FAST               'seps'

 L.  84        42  LOAD_STR                 ':'
               44  STORE_FAST               'colon'
             46_0  COME_FROM            32  '32'

 L.  85        46  SETUP_EXCEPT        288  'to 288'

 L.  86        48  LOAD_FAST                'paths'
               50  POP_JUMP_IF_TRUE     68  'to 68'

 L.  87        52  LOAD_FAST                'path'
               54  LOAD_CONST               None
               56  LOAD_CONST               0
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'sep'
               64  BINARY_ADD       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'

 L.  88        68  LOAD_GLOBAL              splitdrive
               70  LOAD_FAST                'path'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'result_drive'
               78  STORE_FAST               'result_path'

 L.  89        80  SETUP_LOOP          224  'to 224'
               82  LOAD_GLOBAL              map
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                fspath
               88  LOAD_FAST                'paths'
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  GET_ITER         
             94_0  COME_FROM           220  '220'
             94_1  COME_FROM           182  '182'
             94_2  COME_FROM           142  '142'
               94  FOR_ITER            222  'to 222'
               96  STORE_FAST               'p'

 L.  90        98  LOAD_GLOBAL              splitdrive
              100  LOAD_FAST                'p'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'p_drive'
              108  STORE_FAST               'p_path'

 L.  91       110  LOAD_FAST                'p_path'
              112  POP_JUMP_IF_FALSE   146  'to 146'
              114  LOAD_FAST                'p_path'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'seps'
              122  COMPARE_OP               in
              124  POP_JUMP_IF_FALSE   146  'to 146'

 L.  93       126  LOAD_FAST                'p_drive'
              128  POP_JUMP_IF_TRUE    134  'to 134'
              130  LOAD_FAST                'result_drive'
              132  POP_JUMP_IF_TRUE    138  'to 138'
            134_0  COME_FROM           128  '128'

 L.  94       134  LOAD_FAST                'p_drive'
              136  STORE_FAST               'result_drive'
            138_0  COME_FROM           132  '132'

 L.  95       138  LOAD_FAST                'p_path'
              140  STORE_FAST               'result_path'

 L.  96       142  CONTINUE             94  'to 94'
              144  JUMP_FORWARD        188  'to 188'
            146_0  COME_FROM           124  '124'
            146_1  COME_FROM           112  '112'

 L.  97       146  LOAD_FAST                'p_drive'
              148  POP_JUMP_IF_FALSE   188  'to 188'
              150  LOAD_FAST                'p_drive'
              152  LOAD_FAST                'result_drive'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   188  'to 188'

 L.  98       158  LOAD_FAST                'p_drive'
              160  LOAD_METHOD              lower
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  LOAD_FAST                'result_drive'
              166  LOAD_METHOD              lower
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  COMPARE_OP               !=
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 100       174  LOAD_FAST                'p_drive'
              176  STORE_FAST               'result_drive'

 L. 101       178  LOAD_FAST                'p_path'
              180  STORE_FAST               'result_path'

 L. 102       182  CONTINUE             94  'to 94'
            184_0  COME_FROM           172  '172'

 L. 104       184  LOAD_FAST                'p_drive'
              186  STORE_FAST               'result_drive'
            188_0  COME_FROM           156  '156'
            188_1  COME_FROM           148  '148'
            188_2  COME_FROM           144  '144'

 L. 106       188  LOAD_FAST                'result_path'
              190  POP_JUMP_IF_FALSE   212  'to 212'
              192  LOAD_FAST                'result_path'
              194  LOAD_CONST               -1
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'seps'
              200  COMPARE_OP               not-in
              202  POP_JUMP_IF_FALSE   212  'to 212'

 L. 107       204  LOAD_FAST                'result_path'
              206  LOAD_FAST                'sep'
              208  BINARY_ADD       
              210  STORE_FAST               'result_path'
            212_0  COME_FROM           202  '202'
            212_1  COME_FROM           190  '190'

 L. 108       212  LOAD_FAST                'result_path'
              214  LOAD_FAST                'p_path'
              216  BINARY_ADD       
              218  STORE_FAST               'result_path'
              220  JUMP_BACK            94  'to 94'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP       80  '80'

 L. 110       224  LOAD_FAST                'result_path'
          226_228  POP_JUMP_IF_FALSE   280  'to 280'
              230  LOAD_FAST                'result_path'
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  LOAD_FAST                'seps'
              238  COMPARE_OP               not-in
          240_242  POP_JUMP_IF_FALSE   280  'to 280'

 L. 111       244  LOAD_FAST                'result_drive'
          246_248  POP_JUMP_IF_FALSE   280  'to 280'
              250  LOAD_FAST                'result_drive'
              252  LOAD_CONST               -1
              254  LOAD_CONST               None
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  LOAD_FAST                'colon'
              262  COMPARE_OP               !=
          264_266  POP_JUMP_IF_FALSE   280  'to 280'

 L. 112       268  LOAD_FAST                'result_drive'
              270  LOAD_FAST                'sep'
              272  BINARY_ADD       
              274  LOAD_FAST                'result_path'
              276  BINARY_ADD       
              278  RETURN_VALUE     
            280_0  COME_FROM           264  '264'
            280_1  COME_FROM           246  '246'
            280_2  COME_FROM           240  '240'
            280_3  COME_FROM           226  '226'

 L. 113       280  LOAD_FAST                'result_drive'
              282  LOAD_FAST                'result_path'
              284  BINARY_ADD       
              286  RETURN_VALUE     
            288_0  COME_FROM_EXCEPT     46  '46'

 L. 114       288  DUP_TOP          
              290  LOAD_GLOBAL              TypeError
              292  LOAD_GLOBAL              AttributeError
              294  LOAD_GLOBAL              BytesWarning
              296  BUILD_TUPLE_3         3 
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   334  'to 334'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 115       310  LOAD_GLOBAL              genericpath
              312  LOAD_ATTR                _check_arg_types
              314  LOAD_STR                 'join'
              316  LOAD_FAST                'path'
              318  BUILD_TUPLE_2         2 
              320  LOAD_FAST                'paths'
              322  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              324  CALL_FUNCTION_EX      0  'positional arguments only'
              326  POP_TOP          

 L. 116       328  RAISE_VARARGS_0       0  'reraise'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           300  '300'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'

Parse error at or near `JUMP_BACK' instruction at offset 220


def splitdrive(p):
    """Split a pathname into drive/UNC sharepoint and relative path specifiers.
    Returns a 2-tuple (drive_or_unc, path); either part may be empty.

    If you assign
        result = splitdrive(p)
    It is always true that:
        result[0] + result[1] == p

    If the path contained a drive letter, drive_or_unc will contain everything
    up to and including the colon.  e.g. splitdrive("c:/dir") returns ("c:", "/dir")

    If the path contained a UNC path, the drive_or_unc will contain the host name
    and share up to but not including the fourth directory separator character.
    e.g. splitdrive("//host/computer/dir") returns ("//host/computer", "/dir")

    Paths cannot contain both a drive letter and a UNC path.

    """
    p = os.fspath(p)
    if len(p) >= 2:
        if isinstance(p, bytes):
            sep = '\\'
            altsep = '/'
            colon = ':'
        else:
            sep = '\\'
            altsep = '/'
            colon = ':'
        normp = p.replace(altsep, sep)
        if normp[0:2] == sep * 2:
            if normp[2:3] != sep:
                index = normp.find(sep, 2)
                if index == -1:
                    return (p[:0], p)
                index2 = normp.find(sep, index + 1)
                if index2 == index + 1:
                    return (p[:0], p)
                if index2 == -1:
                    index2 = len(p)
                return (p[:index2], p[index2:])
        if normp[1:2] == colon:
            return (p[:2], p[2:])
    return (
     p[:0], p)


def split(p):
    """Split a pathname.

    Return tuple (head, tail) where tail is everything after the final slash.
    Either part may be empty."""
    p = os.fspath(p)
    seps = _get_bothseps(p)
    d, p = splitdrive(p)
    i = len(p)
    while i:
        if p[(i - 1)] not in seps:
            i -= 1

    head, tail = p[:i], p[i:]
    head = head.rstrip(seps) or head
    return (
     d + head, tail)


def splitext(p):
    p = os.fspath(p)
    if isinstance(p, bytes):
        return genericpath._splitext(p, '\\', '/', '.')
    return genericpath._splitext(p, '\\', '/', '.')


splitext.__doc__ = genericpath._splitext.__doc__

def basename(p):
    """Returns the final component of a pathname"""
    return split(p)[1]


def dirname(p):
    """Returns the directory component of a pathname"""
    return split(p)[0]


def islink(path):
    """Test whether a path is a symbolic link.
    This will always return false for Windows prior to 6.0.
    """
    try:
        st = os.lstat(path)
    except (OSError, AttributeError):
        return False
    else:
        return stat.S_ISLNK(st.st_mode)


def lexists(path):
    """Test whether a path exists.  Returns True for broken symbolic links"""
    try:
        st = os.lstat(path)
    except OSError:
        return False
    else:
        return True


try:
    from nt import _getvolumepathname
except ImportError:
    _getvolumepathname = None

def ismount(path):
    """Test whether a path is a mount point (a drive root, the root of a
    share, or a mounted volume)"""
    path = os.fspath(path)
    seps = _get_bothseps(path)
    path = abspath(path)
    root, rest = splitdrive(path)
    if root:
        if root[0] in seps:
            return not rest or rest in seps
    if rest in seps:
        return True
    if _getvolumepathname:
        return path.rstrip(seps) == _getvolumepathname(path).rstrip(seps)
    return False


def expanduser(path):
    """Expand ~ and ~user constructs.

    If user or $HOME is unknown, do nothing."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        tilde = '~'
    else:
        tilde = '~'
    if not path.startswith(tilde):
        return path
    i, n = 1, len(path)
    while i < n:
        if path[i] not in _get_bothseps(path):
            i += 1

    if 'HOME' in os.environ:
        userhome = os.environ['HOME']
    elif 'USERPROFILE' in os.environ:
        userhome = os.environ['USERPROFILE']
    else:
        if 'HOMEPATH' not in os.environ:
            return path
        try:
            drive = os.environ['HOMEDRIVE']
        except KeyError:
            drive = ''

        userhome = join(drive, os.environ['HOMEPATH'])
    if isinstance(path, bytes):
        userhome = os.fsencode(userhome)
    if i != 1:
        userhome = join(dirname(userhome), path[1:i])
    return userhome + path[i:]


def expandvars(path):
    """Expand shell variables of the forms $var, ${var} and %var%.

    Unknown variables are left unchanged."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        if '$' not in path:
            if '%' not in path:
                return path
        import string
        varchars = bytes(string.ascii_letters + string.digits + '_-', 'ascii')
        quote = "'"
        percent = '%'
        brace = '{'
        rbrace = '}'
        dollar = '$'
        environ = getattr(os, 'environb', None)
    else:
        if '$' not in path:
            if '%' not in path:
                return path
        import string
        varchars = string.ascii_letters + string.digits + '_-'
        quote = "'"
        percent = '%'
        brace = '{'
        rbrace = '}'
        dollar = '$'
        environ = os.environ
    res = path[:0]
    index = 0
    pathlen = len(path)
    while index < pathlen:
        c = path[index:index + 1]
        if c == quote:
            path = path[index + 1:]
            pathlen = len(path)
            try:
                index = path.index(c)
                res += c + path[:index + 1]
            except ValueError:
                res += c + path
                index = pathlen - 1

        elif c == percent:
            if path[index + 1:index + 2] == percent:
                res += c
                index += 1
            else:
                path = path[index + 1:]
                pathlen = len(path)
                try:
                    index = path.index(percent)
                except ValueError:
                    res += percent + path
                    index = pathlen - 1
                else:
                    var = path[:index]
                    try:
                        if environ is None:
                            value = os.fsencode(os.environ[os.fsdecode(var)])
                        else:
                            value = environ[var]
                    except KeyError:
                        value = percent + var + percent

                    res += value

        elif c == dollar:
            if path[index + 1:index + 2] == dollar:
                res += c
                index += 1
            elif path[index + 1:index + 2] == brace:
                path = path[index + 2:]
                pathlen = len(path)
                try:
                    index = path.index(rbrace)
                except ValueError:
                    res += dollar + brace + path
                    index = pathlen - 1
                else:
                    var = path[:index]
                    try:
                        if environ is None:
                            value = os.fsencode(os.environ[os.fsdecode(var)])
                        else:
                            value = environ[var]
                    except KeyError:
                        value = dollar + brace + var + rbrace

                    res += value

            else:
                var = path[:0]
                index += 1
                c = path[index:index + 1]
                while c:
                    if c in varchars:
                        var += c
                        index += 1
                        c = path[index:index + 1]

                try:
                    if environ is None:
                        value = os.fsencode(os.environ[os.fsdecode(var)])
                    else:
                        value = environ[var]
                except KeyError:
                    value = dollar + var

                res += value
                if c:
                    index -= 1
        else:
            res += c
        index += 1

    return res


def normpath(path):
    """Normalize path, eliminating double slashes, etc."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        sep = '\\'
        altsep = '/'
        curdir = '.'
        pardir = '..'
        special_prefixes = ('\\\\.\\', '\\\\?\\')
    else:
        sep = '\\'
        altsep = '/'
        curdir = '.'
        pardir = '..'
        special_prefixes = ('\\\\.\\', '\\\\?\\')
    if path.startswith(special_prefixes):
        return path
    path = path.replace(altsep, sep)
    prefix, path = splitdrive(path)
    if path.startswith(sep):
        prefix += sep
        path = path.lstrip(sep)
    comps = path.split(sep)
    i = 0
    while i < len(comps):
        if comps[i]:
            if comps[i] == curdir:
                del comps[i]
            else:
                if comps[i] == pardir:
                    if i > 0 and comps[(i - 1)] != pardir:
                        del comps[i - 1:i + 1]
                        i -= 1
                    elif i == 0 and prefix.endswith(sep):
                        del comps[i]
                    else:
                        i += 1
                else:
                    i += 1

    if not prefix:
        if not comps:
            comps.append(curdir)
        return prefix + sep.join(comps)


try:
    from nt import _getfullpathname
except ImportError:

    def abspath(path):
        """Return the absolute version of a path."""
        path = os.fspath(path)
        if not isabs(path):
            if isinstance(path, bytes):
                cwd = os.getcwdb()
            else:
                cwd = os.getcwd()
            path = join(cwd, path)
        return normpath(path)


else:

    def abspath(path):
        """Return the absolute version of a path."""
        if path:
            path = os.fspath(path)
            try:
                path = _getfullpathname(path)
            except OSError:
                pass

        elif isinstance(path, bytes):
            path = os.getcwdb()
        else:
            path = os.getcwd()
        return normpath(path)


realpath = abspath
supports_unicode_filenames = hasattr(sys, 'getwindowsversion') and sys.getwindowsversion()[3] >= 2

def relpath(path, start=None):
    """Return a relative version of a path"""
    path = os.fspath(path)
    if isinstance(path, bytes):
        sep = '\\'
        curdir = '.'
        pardir = '..'
    else:
        sep = '\\'
        curdir = '.'
        pardir = '..'
    if start is None:
        start = curdir
    if not path:
        raise ValueError('no path specified')
    start = os.fspath(start)
    try:
        start_abs = abspath(normpath(start))
        path_abs = abspath(normpath(path))
        start_drive, start_rest = splitdrive(start_abs)
        path_drive, path_rest = splitdrive(path_abs)
        if normcase(start_drive) != normcase(path_drive):
            raise ValueError('path is on mount %r, start on mount %r' % (
             path_drive, start_drive))
        start_list = [x for x in start_rest.split(sep) if x]
        path_list = [x for x in path_rest.split(sep) if x]
        i = 0
        for e1, e2 in zip(start_list, path_list):
            if normcase(e1) != normcase(e2):
                break
            else:
                i += 1

        rel_list = [
         pardir] * (len(start_list) - i) + path_list[i:]
        if not rel_list:
            return curdir
        return join(*rel_list)
    except (TypeError, ValueError, AttributeError, BytesWarning, DeprecationWarning):
        genericpath._check_arg_types('relpath', path, start)
        raise


def commonpath(paths):
    """Given a sequence of path names, returns the longest common sub-path."""
    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')
    paths = tuple(map(os.fspath, paths))
    if isinstance(paths[0], bytes):
        sep = '\\'
        altsep = '/'
        curdir = '.'
    else:
        sep = '\\'
        altsep = '/'
        curdir = '.'
    try:
        drivesplits = [splitdrive(p.replace(altsep, sep).lower()) for p in paths]
        split_paths = [p.split(sep) for d, p in drivesplits]
        try:
            isabs, = set((p[:1] == sep for d, p in drivesplits))
        except ValueError:
            raise ValueError("Can't mix absolute and relative paths") from None

        if len(set((d for d, p in drivesplits))) != 1:
            raise ValueError("Paths don't have the same drive")
        drive, path = splitdrive(paths[0].replace(altsep, sep))
        common = path.split(sep)
        common = [c for c in common if c if c != curdir]
        split_paths = [[c for c in s if c if c != curdir] for s in split_paths]
        s1 = min(split_paths)
        s2 = max(split_paths)
        for i, c in enumerate(s1):
            if c != s2[i]:
                common = common[:i]
                break
        else:
            common = common[:len(s1)]
        prefix = drive + sep if isabs else drive
        return prefix + sep.join(common)
    except (TypeError, AttributeError):
        (genericpath._check_arg_types)(*('commonpath', ), *paths)
        raise


try:
    if sys.getwindowsversion()[:2] >= (6, 0):
        from nt import _getfinalpathname
    else:
        raise ImportError
except (AttributeError, ImportError):

    def _getfinalpathname(f):
        return normcase(abspath(f))


try:
    from nt import _isdir as isdir
except ImportError:
    pass