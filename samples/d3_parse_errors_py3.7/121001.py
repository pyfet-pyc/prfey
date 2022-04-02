# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: posixpath.py
"""Common operations on Posix pathnames.

Instead of importing this module directly, import os and refer to
this module as os.path.  The "os.path" name is an alias for this
module on Posix systems; on other systems (e.g. Mac, Windows),
os.path provides the same operations in a manner specific to that
platform, and is an alias to another module (e.g. macpath, ntpath).

Some of this can actually be useful on non-Posix systems too, e.g.
for manipulation of the pathname component of URLs.
"""
curdir = '.'
pardir = '..'
extsep = '.'
sep = '/'
pathsep = ':'
defpath = ':/bin:/usr/bin'
altsep = None
devnull = '/dev/null'
import os, sys, stat, genericpath
from genericpath import *
__all__ = [
 'normcase', 'isabs', 'join', 'splitdrive', 'split', 'splitext',
 'basename', 'dirname', 'commonprefix', 'getsize', 'getmtime',
 'getatime', 'getctime', 'islink', 'exists', 'lexists', 'isdir', 'isfile',
 'ismount', 'expanduser', 'expandvars', 'normpath', 'abspath',
 'samefile', 'sameopenfile', 'samestat',
 'curdir', 'pardir', 'sep', 'pathsep', 'defpath', 'altsep', 'extsep',
 'devnull', 'realpath', 'supports_unicode_filenames', 'relpath',
 'commonpath']

def _get_sep(path):
    if isinstance(path, bytes):
        return '/'
    return '/'


def normcase(s):
    """Normalize case of pathname.  Has no effect under Posix"""
    s = os.fspath(s)
    if not isinstance(s, (bytes, str)):
        raise TypeError("normcase() argument must be str or bytes, not '{}'".format(s.__class__.__name__))
    return s


def isabs(s):
    """Test whether a path is absolute"""
    s = os.fspath(s)
    sep = _get_sep(s)
    return s.startswith(sep)


def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    a = os.fspath(a)
    sep = _get_sep(a)
    path = a
    try:
        if not p:
            path[:0] + sep
        for b in map(os.fspath, p):
            if b.startswith(sep):
                path = b
            if path:
                if path.endswith(sep):
                    path += b
                else:
                    path += sep + b

    except (TypeError, AttributeError, BytesWarning):
        (genericpath._check_arg_types)('join', a, *p)
        raise

    return path


def split(p):
    """Split a pathname.  Returns tuple "(head, tail)" where "tail" is
    everything after the final slash.  Either part may be empty."""
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    head, tail = p[:i], p[i:]
    if head:
        if head != sep * len(head):
            head = head.rstrip(sep)
    return (
     head, tail)


def splitext(p):
    p = os.fspath(p)
    if isinstance(p, bytes):
        sep = '/'
        extsep = '.'
    else:
        sep = '/'
        extsep = '.'
    return genericpath._splitext(p, sep, None, extsep)


splitext.__doc__ = genericpath._splitext.__doc__

def splitdrive(p):
    """Split a pathname into drive and path. On Posix, drive is always
    empty."""
    p = os.fspath(p)
    return (
     p[:0], p)


def basename(p):
    """Returns the final component of a pathname"""
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    return p[i:]


def dirname(p):
    """Returns the directory component of a pathname"""
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    head = p[:i]
    if head:
        if head != sep * len(head):
            head = head.rstrip(sep)
    return head


def islink(path):
    """Test whether a path is a symbolic link"""
    try:
        st = os.lstat(path)
    except (OSError, AttributeError):
        return False
    else:
        return stat.S_ISLNK(st.st_mode)


def lexists(path):
    """Test whether a path exists.  Returns True for broken symbolic links"""
    try:
        os.lstat(path)
    except OSError:
        return False
    else:
        return True


def ismount(path):
    """Test whether a path is a mount point"""
    try:
        s1 = os.lstat(path)
    except OSError:
        return False
    else:
        if stat.S_ISLNK(s1.st_mode):
            return False
        if isinstance(path, bytes):
            parent = join(path, '..')
        else:
            parent = join(path, '..')
        parent = realpath(parent)
        try:
            s2 = os.lstat(parent)
        except OSError:
            return False
        else:
            dev1 = s1.st_dev
            dev2 = s2.st_dev
            if dev1 != dev2:
                return True
            ino1 = s1.st_ino
            ino2 = s2.st_ino
            if ino1 == ino2:
                return True
            return False


def expanduser(path):
    """Expand ~ and ~user constructions.  If user or $HOME is unknown,
    do nothing."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        tilde = '~'
    else:
        tilde = '~'
    if not path.startswith(tilde):
        return path
    sep = _get_sep(path)
    i = path.find(sep, 1)
    if i < 0:
        i = len(path)
    if i == 1:
        if 'HOME' not in os.environ:
            import pwd
            try:
                userhome = pwd.getpwuid(os.getuid()).pw_dir
            except KeyError:
                return path

        else:
            userhome = os.environ['HOME']
    else:
        import pwd
        name = path[1:i]
        if isinstance(name, bytes):
            name = str(name, 'ASCII')
        try:
            pwent = pwd.getpwnam(name)
        except KeyError:
            return path
        else:
            userhome = pwent.pw_dir

    if isinstance(path, bytes):
        userhome = os.fsencode(userhome)
        root = '/'
    else:
        root = '/'
    userhome = userhome.rstrip(root)
    return userhome + path[i:] or root


_varprog = None
_varprogb = None

def expandvars(path):
    """Expand shell variables of form $var and ${var}.  Unknown variables
    are left unchanged."""
    global _varprog
    global _varprogb
    path = os.fspath(path)
    if isinstance(path, bytes):
        if '$' not in path:
            return path
        if not _varprogb:
            import re
            _varprogb = re.compile('\\$(\\w+|\\{[^}]*\\})', re.ASCII)
        search = _varprogb.search
        start = '{'
        end = '}'
        environ = getattr(os, 'environb', None)
    else:
        if '$' not in path:
            return path
        if not _varprog:
            import re
            _varprog = re.compile('\\$(\\w+|\\{[^}]*\\})', re.ASCII)
        search = _varprog.search
        start = '{'
        end = '}'
        environ = os.environ
    i = 0
    while True:
        m = search(path, i)
        if not m:
            break
        else:
            i, j = m.span(0)
            name = m.group(1)
            if name.startswith(start):
                if name.endswith(end):
                    name = name[1:-1]
            try:
                if environ is None:
                    value = os.fsencode(os.environ[os.fsdecode(name)])
                else:
                    value = environ[name]
            except KeyError:
                i = j
            else:
                tail = path[j:]
                path = path[:i] + value
                i = len(path)
                path += tail

    return path


def normpath--- This code section failed: ---

 L. 340         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'path'

 L. 341        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 342        20  LOAD_STR                 '/'
               22  STORE_FAST               'sep'

 L. 343        24  LOAD_STR                 ''
               26  STORE_FAST               'empty'

 L. 344        28  LOAD_STR                 '.'
               30  STORE_FAST               'dot'

 L. 345        32  LOAD_STR                 '..'
               34  STORE_FAST               'dotdot'
               36  JUMP_FORWARD         54  'to 54'
             38_0  COME_FROM            18  '18'

 L. 347        38  LOAD_STR                 '/'
               40  STORE_FAST               'sep'

 L. 348        42  LOAD_STR                 ''
               44  STORE_FAST               'empty'

 L. 349        46  LOAD_STR                 '.'
               48  STORE_FAST               'dot'

 L. 350        50  LOAD_STR                 '..'
               52  STORE_FAST               'dotdot'
             54_0  COME_FROM            36  '36'

 L. 351        54  LOAD_FAST                'path'
               56  LOAD_FAST                'empty'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 352        62  LOAD_FAST                'dot'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 353        66  LOAD_FAST                'path'
               68  LOAD_METHOD              startswith
               70  LOAD_FAST                'sep'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  STORE_FAST               'initial_slashes'

 L. 356        76  LOAD_FAST                'initial_slashes'
               78  POP_JUMP_IF_FALSE   112  'to 112'

 L. 357        80  LOAD_FAST                'path'
               82  LOAD_METHOD              startswith
               84  LOAD_FAST                'sep'
               86  LOAD_CONST               2
               88  BINARY_MULTIPLY  
               90  CALL_METHOD_1         1  '1 positional argument'
               92  POP_JUMP_IF_FALSE   112  'to 112'
               94  LOAD_FAST                'path'
               96  LOAD_METHOD              startswith
               98  LOAD_FAST                'sep'
              100  LOAD_CONST               3
              102  BINARY_MULTIPLY  
              104  CALL_METHOD_1         1  '1 positional argument'
              106  POP_JUMP_IF_TRUE    112  'to 112'

 L. 358       108  LOAD_CONST               2
              110  STORE_FAST               'initial_slashes'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            92  '92'
            112_2  COME_FROM            78  '78'

 L. 359       112  LOAD_FAST                'path'
              114  LOAD_METHOD              split
              116  LOAD_FAST                'sep'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  STORE_FAST               'comps'

 L. 360       122  BUILD_LIST_0          0 
              124  STORE_FAST               'new_comps'

 L. 361       126  SETUP_LOOP          210  'to 210'
              128  LOAD_FAST                'comps'
              130  GET_ITER         
            132_0  COME_FROM           206  '206'
            132_1  COME_FROM           196  '196'
            132_2  COME_FROM           192  '192'
            132_3  COME_FROM           148  '148'
              132  FOR_ITER            208  'to 208'
              134  STORE_FAST               'comp'

 L. 362       136  LOAD_FAST                'comp'
              138  LOAD_FAST                'empty'
              140  LOAD_FAST                'dot'
              142  BUILD_TUPLE_2         2 
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   150  'to 150'

 L. 363       148  CONTINUE            132  'to 132'
            150_0  COME_FROM           146  '146'

 L. 364       150  LOAD_FAST                'comp'
              152  LOAD_FAST                'dotdot'
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_TRUE    182  'to 182'
              158  LOAD_FAST                'initial_slashes'
              160  POP_JUMP_IF_TRUE    166  'to 166'
              162  LOAD_FAST                'new_comps'
              164  POP_JUMP_IF_FALSE   182  'to 182'
            166_0  COME_FROM           160  '160'

 L. 365       166  LOAD_FAST                'new_comps'
              168  POP_JUMP_IF_FALSE   194  'to 194'
              170  LOAD_FAST                'new_comps'
              172  LOAD_CONST               -1
              174  BINARY_SUBSCR    
              176  LOAD_FAST                'dotdot'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   194  'to 194'
            182_0  COME_FROM           164  '164'
            182_1  COME_FROM           156  '156'

 L. 366       182  LOAD_FAST                'new_comps'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'comp'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_TOP          
              192  JUMP_BACK           132  'to 132'
            194_0  COME_FROM           180  '180'
            194_1  COME_FROM           168  '168'

 L. 367       194  LOAD_FAST                'new_comps'
              196  POP_JUMP_IF_FALSE_BACK   132  'to 132'

 L. 368       198  LOAD_FAST                'new_comps'
              200  LOAD_METHOD              pop
              202  CALL_METHOD_0         0  '0 positional arguments'
              204  POP_TOP          
              206  JUMP_BACK           132  'to 132'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      126  '126'

 L. 369       210  LOAD_FAST                'new_comps'
              212  STORE_FAST               'comps'

 L. 370       214  LOAD_FAST                'sep'
              216  LOAD_METHOD              join
              218  LOAD_FAST                'comps'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  STORE_FAST               'path'

 L. 371       224  LOAD_FAST                'initial_slashes'
              226  POP_JUMP_IF_FALSE   240  'to 240'

 L. 372       228  LOAD_FAST                'sep'
              230  LOAD_FAST                'initial_slashes'
              232  BINARY_MULTIPLY  
              234  LOAD_FAST                'path'
              236  BINARY_ADD       
              238  STORE_FAST               'path'
            240_0  COME_FROM           226  '226'

 L. 373       240  LOAD_FAST                'path'
              242  JUMP_IF_TRUE_OR_POP   246  'to 246'
              244  LOAD_FAST                'dot'
            246_0  COME_FROM           242  '242'
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 210_0


def abspath(path):
    """Return an absolute path."""
    path = os.fspath(path)
    if not isabs(path):
        if isinstance(path, bytes):
            cwd = os.getcwdb()
        else:
            cwd = os.getcwd()
        path = join(cwd, path)
    return normpath(path)


def realpath(filename):
    """Return the canonical path of the specified filename, eliminating any
symbolic links encountered in the path."""
    filename = os.fspath(filename)
    path, ok = _joinrealpath(filename[:0], filename, {})
    return abspath(path)


def _joinrealpath--- This code section failed: ---

 L. 401         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              bytes
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 402        10  LOAD_STR                 '/'
               12  STORE_FAST               'sep'

 L. 403        14  LOAD_STR                 '.'
               16  STORE_FAST               'curdir'

 L. 404        18  LOAD_STR                 '..'
               20  STORE_FAST               'pardir'
               22  JUMP_FORWARD         36  'to 36'
             24_0  COME_FROM             8  '8'

 L. 406        24  LOAD_STR                 '/'
               26  STORE_FAST               'sep'

 L. 407        28  LOAD_STR                 '.'
               30  STORE_FAST               'curdir'

 L. 408        32  LOAD_STR                 '..'
               34  STORE_FAST               'pardir'
             36_0  COME_FROM            22  '22'

 L. 410        36  LOAD_GLOBAL              isabs
               38  LOAD_FAST                'rest'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 411        44  LOAD_FAST                'rest'
               46  LOAD_CONST               1
               48  LOAD_CONST               None
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  STORE_FAST               'rest'

 L. 412        56  LOAD_FAST                'sep'
               58  STORE_FAST               'path'
             60_0  COME_FROM            42  '42'

 L. 414        60  SETUP_LOOP          276  'to 276'
             62_0  COME_FROM           272  '272'
             62_1  COME_FROM           198  '198'
             62_2  COME_FROM           172  '172'
             62_3  COME_FROM           148  '148'
             62_4  COME_FROM           142  '142'
             62_5  COME_FROM            96  '96'
             62_6  COME_FROM            86  '86'
               62  LOAD_FAST                'rest'
            64_66  POP_JUMP_IF_FALSE   274  'to 274'

 L. 415        68  LOAD_FAST                'rest'
               70  LOAD_METHOD              partition
               72  LOAD_FAST                'sep'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  UNPACK_SEQUENCE_3     3 
               78  STORE_FAST               'name'
               80  STORE_FAST               '_'
               82  STORE_FAST               'rest'

 L. 416        84  LOAD_FAST                'name'
               86  POP_JUMP_IF_FALSE_BACK    62  'to 62'
               88  LOAD_FAST                'name'
               90  LOAD_FAST                'curdir'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 418        96  CONTINUE             62  'to 62'
             98_0  COME_FROM            94  '94'

 L. 419        98  LOAD_FAST                'name'
              100  LOAD_FAST                'pardir'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   150  'to 150'

 L. 421       106  LOAD_FAST                'path'
              108  POP_JUMP_IF_FALSE   144  'to 144'

 L. 422       110  LOAD_GLOBAL              split
              112  LOAD_FAST                'path'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  UNPACK_SEQUENCE_2     2 
              118  STORE_FAST               'path'
              120  STORE_FAST               'name'

 L. 423       122  LOAD_FAST                'name'
              124  LOAD_FAST                'pardir'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   148  'to 148'

 L. 424       130  LOAD_GLOBAL              join
              132  LOAD_FAST                'path'
              134  LOAD_FAST                'pardir'
              136  LOAD_FAST                'pardir'
              138  CALL_FUNCTION_3       3  '3 positional arguments'
              140  STORE_FAST               'path'
              142  JUMP_BACK            62  'to 62'
            144_0  COME_FROM           108  '108'

 L. 426       144  LOAD_FAST                'pardir'
              146  STORE_FAST               'path'
            148_0  COME_FROM           128  '128'

 L. 427       148  CONTINUE             62  'to 62'
            150_0  COME_FROM           104  '104'

 L. 428       150  LOAD_GLOBAL              join
              152  LOAD_FAST                'path'
              154  LOAD_FAST                'name'
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  STORE_FAST               'newpath'

 L. 429       160  LOAD_GLOBAL              islink
              162  LOAD_FAST                'newpath'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  POP_JUMP_IF_TRUE    174  'to 174'

 L. 430       168  LOAD_FAST                'newpath'
              170  STORE_FAST               'path'

 L. 431       172  CONTINUE             62  'to 62'
            174_0  COME_FROM           166  '166'

 L. 433       174  LOAD_FAST                'newpath'
              176  LOAD_FAST                'seen'
              178  COMPARE_OP               in
              180  POP_JUMP_IF_FALSE   214  'to 214'

 L. 435       182  LOAD_FAST                'seen'
              184  LOAD_FAST                'newpath'
              186  BINARY_SUBSCR    
              188  STORE_FAST               'path'

 L. 436       190  LOAD_FAST                'path'
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   200  'to 200'

 L. 438       198  CONTINUE             62  'to 62'
            200_0  COME_FROM           196  '196'

 L. 441       200  LOAD_GLOBAL              join
              202  LOAD_FAST                'newpath'
              204  LOAD_FAST                'rest'
              206  CALL_FUNCTION_2       2  '2 positional arguments'
              208  LOAD_CONST               False
              210  BUILD_TUPLE_2         2 
              212  RETURN_VALUE     
            214_0  COME_FROM           180  '180'

 L. 442       214  LOAD_CONST               None
              216  LOAD_FAST                'seen'
              218  LOAD_FAST                'newpath'
              220  STORE_SUBSCR     

 L. 443       222  LOAD_GLOBAL              _joinrealpath
              224  LOAD_FAST                'path'
              226  LOAD_GLOBAL              os
              228  LOAD_METHOD              readlink
              230  LOAD_FAST                'newpath'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  LOAD_FAST                'seen'
              236  CALL_FUNCTION_3       3  '3 positional arguments'
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'path'
              242  STORE_FAST               'ok'

 L. 444       244  LOAD_FAST                'ok'
          246_248  POP_JUMP_IF_TRUE    264  'to 264'

 L. 445       250  LOAD_GLOBAL              join
              252  LOAD_FAST                'path'
              254  LOAD_FAST                'rest'
              256  CALL_FUNCTION_2       2  '2 positional arguments'
              258  LOAD_CONST               False
              260  BUILD_TUPLE_2         2 
              262  RETURN_VALUE     
            264_0  COME_FROM           246  '246'

 L. 446       264  LOAD_FAST                'path'
              266  LOAD_FAST                'seen'
              268  LOAD_FAST                'newpath'
              270  STORE_SUBSCR     
              272  JUMP_BACK            62  'to 62'
            274_0  COME_FROM            64  '64'
              274  POP_BLOCK        
            276_0  COME_FROM_LOOP       60  '60'

 L. 448       276  LOAD_FAST                'path'
              278  LOAD_CONST               True
              280  BUILD_TUPLE_2         2 
              282  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 148


supports_unicode_filenames = sys.platform == 'darwin'

def relpath(path, start=None):
    """Return a relative version of a path"""
    if not path:
        raise ValueError('no path specified')
    path = os.fspath(path)
    if isinstance(path, bytes):
        curdir = '.'
        sep = '/'
        pardir = '..'
    else:
        curdir = '.'
        sep = '/'
        pardir = '..'
    if start is None:
        start = curdir
    else:
        start = os.fspath(start)
    try:
        start_list = [x for x in abspath(start).split(sep) if x]
        path_list = [x for x in abspath(path).split(sep) if x]
        i = len(commonprefix([start_list, path_list]))
        rel_list = [
         pardir] * (len(start_list) - i) + path_list[i:]
        if not rel_list:
            return curdir
        return join(*rel_list)
    except (TypeError, AttributeError, BytesWarning, DeprecationWarning):
        genericpath._check_arg_types('relpath', path, start)
        raise


def commonpath(paths):
    """Given a sequence of path names, returns the longest common sub-path."""
    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')
    paths = tuple(map(os.fspath, paths))
    if isinstance(paths[0], bytes):
        sep = '/'
        curdir = '.'
    else:
        sep = '/'
        curdir = '.'
    try:
        split_paths = [path.split(sep) for path in paths]
        try:
            isabs, = set((p[:1] == sep for p in paths))
        except ValueError:
            raise ValueError("Can't mix absolute and relative paths") from None

        split_paths = [[c for c in s if c if c != curdir] for s in split_paths]
        s1 = min(split_paths)
        s2 = max(split_paths)
        common = s1
        for i, c in enumerate(s1):
            if c != s2[i]:
                common = s1[:i]
                break

        prefix = sep if isabs else sep[:0]
        return prefix + sep.join(common)
    except (TypeError, AttributeError):
        (genericpath._check_arg_types)(*('commonpath', ), *paths)
        raise