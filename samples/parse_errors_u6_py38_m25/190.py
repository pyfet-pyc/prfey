# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: posixpath.py
"""Common operations on Posix pathnames.

Instead of importing this module directly, import os and refer to
this module as os.path.  The "os.path" name is an alias for this
module on Posix systems; on other systems (e.g. Windows),
os.path provides the same operations in a manner specific to that
platform, and is an alias to another module (e.g. ntpath).

Some of this can actually be useful on non-Posix systems too, e.g.
for manipulation of the pathname component of URLs.
"""
curdir = '.'
pardir = '..'
extsep = '.'
sep = '/'
pathsep = ':'
defpath = '/bin:/usr/bin'
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
        return b'/'
    return '/'


def normcase(s):
    """Normalize case of pathname.  Has no effect under Posix"""
    return os.fspath(s)


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
            elif not path or path.endswith(sep):
                path += b
            else:
                path += sep + b

    except (TypeError, AttributeError, BytesWarning):
        (genericpath._check_arg_types)('join', a, *p)
        raise
    else:
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
        sep = b'/'
        extsep = b'.'
    else:
        sep = '/'
        extsep = '.'
    return genericpath._splitext(p, sep, None, extsep)


splitext.__doc__ = genericpath._splitext.__doc__

def splitdrive(p):
    """Split a pathname into drive and path. On Posix, drive is always
    empty."""
    p = os.fspath(p)
    return (p[:0], p)


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
    except (OSError, ValueError, AttributeError):
        return False
    else:
        return stat.S_ISLNK(st.st_mode)


def lexists(path):
    """Test whether a path exists.  Returns True for broken symbolic links"""
    try:
        os.lstat(path)
    except (OSError, ValueError):
        return False
    else:
        return True


def ismount(path):
    """Test whether a path is a mount point"""
    try:
        s1 = os.lstat(path)
    except (OSError, ValueError):
        return False
    else:
        if stat.S_ISLNK(s1.st_mode):
            return False
        elif isinstance(path, bytes):
            parent = join(path, b'..')
        else:
            parent = join(path, '..')
        parent = realpath(parent)
        try:
            s2 = os.lstat(parent)
        except (OSError, ValueError):
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
        tilde = b'~'
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
        else:
            try:
                pwent = pwd.getpwnam(name)
            except KeyError:
                return path
            else:
                userhome = pwent.pw_dir
            if isinstance(path, bytes):
                userhome = os.fsencode(userhome)
                root = b'/'
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
        if b'$' not in path:
            return path
        if not _varprogb:
            import re
            _varprogb = re.compile(b'\\$(\\w+|\\{[^}]*\\})', re.ASCII)
        search = _varprogb.search
        start = b'{'
        end = b'}'
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

 L. 336         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L. 337        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 338        20  LOAD_CONST               b'/'
               22  STORE_FAST               'sep'

 L. 339        24  LOAD_CONST               b''
               26  STORE_FAST               'empty'

 L. 340        28  LOAD_CONST               b'.'
               30  STORE_FAST               'dot'

 L. 341        32  LOAD_CONST               b'..'
               34  STORE_FAST               'dotdot'
               36  JUMP_FORWARD         54  'to 54'
             38_0  COME_FROM            18  '18'

 L. 343        38  LOAD_STR                 '/'
               40  STORE_FAST               'sep'

 L. 344        42  LOAD_STR                 ''
               44  STORE_FAST               'empty'

 L. 345        46  LOAD_STR                 '.'
               48  STORE_FAST               'dot'

 L. 346        50  LOAD_STR                 '..'
               52  STORE_FAST               'dotdot'
             54_0  COME_FROM            36  '36'

 L. 347        54  LOAD_FAST                'path'
               56  LOAD_FAST                'empty'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 348        62  LOAD_FAST                'dot'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 349        66  LOAD_FAST                'path'
               68  LOAD_METHOD              startswith
               70  LOAD_FAST                'sep'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'initial_slashes'

 L. 352        76  LOAD_FAST                'initial_slashes'
               78  POP_JUMP_IF_FALSE   112  'to 112'

 L. 353        80  LOAD_FAST                'path'
               82  LOAD_METHOD              startswith
               84  LOAD_FAST                'sep'
               86  LOAD_CONST               2
               88  BINARY_MULTIPLY  
               90  CALL_METHOD_1         1  ''

 L. 352        92  POP_JUMP_IF_FALSE   112  'to 112'

 L. 353        94  LOAD_FAST                'path'
               96  LOAD_METHOD              startswith
               98  LOAD_FAST                'sep'
              100  LOAD_CONST               3
              102  BINARY_MULTIPLY  
              104  CALL_METHOD_1         1  ''

 L. 352       106  POP_JUMP_IF_TRUE    112  'to 112'

 L. 354       108  LOAD_CONST               2
              110  STORE_FAST               'initial_slashes'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            92  '92'
            112_2  COME_FROM            78  '78'

 L. 355       112  LOAD_FAST                'path'
              114  LOAD_METHOD              split
              116  LOAD_FAST                'sep'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'comps'

 L. 356       122  BUILD_LIST_0          0 
              124  STORE_FAST               'new_comps'

 L. 357       126  LOAD_FAST                'comps'
              128  GET_ITER         
            130_0  COME_FROM           194  '194'
              130  FOR_ITER            206  'to 206'
              132  STORE_FAST               'comp'

 L. 358       134  LOAD_FAST                'comp'
              136  LOAD_FAST                'empty'
              138  LOAD_FAST                'dot'
              140  BUILD_TUPLE_2         2 
              142  COMPARE_OP               in
              144  POP_JUMP_IF_FALSE   148  'to 148'

 L. 359       146  JUMP_BACK           130  'to 130'
            148_0  COME_FROM           144  '144'

 L. 360       148  LOAD_FAST                'comp'
              150  LOAD_FAST                'dotdot'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_TRUE    180  'to 180'
              156  LOAD_FAST                'initial_slashes'
              158  POP_JUMP_IF_TRUE    164  'to 164'
              160  LOAD_FAST                'new_comps'
              162  POP_JUMP_IF_FALSE   180  'to 180'
            164_0  COME_FROM           158  '158'

 L. 361       164  LOAD_FAST                'new_comps'

 L. 360       166  POP_JUMP_IF_FALSE   192  'to 192'

 L. 361       168  LOAD_FAST                'new_comps'
              170  LOAD_CONST               -1
              172  BINARY_SUBSCR    
              174  LOAD_FAST                'dotdot'
              176  COMPARE_OP               ==

 L. 360       178  POP_JUMP_IF_FALSE   192  'to 192'
            180_0  COME_FROM           162  '162'
            180_1  COME_FROM           154  '154'

 L. 362       180  LOAD_FAST                'new_comps'
              182  LOAD_METHOD              append
              184  LOAD_FAST                'comp'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  JUMP_BACK           130  'to 130'
            192_0  COME_FROM           178  '178'
            192_1  COME_FROM           166  '166'

 L. 363       192  LOAD_FAST                'new_comps'
              194  POP_JUMP_IF_FALSE   130  'to 130'

 L. 364       196  LOAD_FAST                'new_comps'
              198  LOAD_METHOD              pop
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          
              204  JUMP_BACK           130  'to 130'

 L. 365       206  LOAD_FAST                'new_comps'
              208  STORE_FAST               'comps'

 L. 366       210  LOAD_FAST                'sep'
              212  LOAD_METHOD              join
              214  LOAD_FAST                'comps'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'path'

 L. 367       220  LOAD_FAST                'initial_slashes'
              222  POP_JUMP_IF_FALSE   236  'to 236'

 L. 368       224  LOAD_FAST                'sep'
              226  LOAD_FAST                'initial_slashes'
              228  BINARY_MULTIPLY  
              230  LOAD_FAST                'path'
              232  BINARY_ADD       
              234  STORE_FAST               'path'
            236_0  COME_FROM           222  '222'

 L. 369       236  LOAD_FAST                'path'
              238  JUMP_IF_TRUE_OR_POP   242  'to 242'
              240  LOAD_FAST                'dot'
            242_0  COME_FROM           238  '238'
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 242


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


def _joinrealpath(path, rest, seen):
    if isinstance(path, bytes):
        sep = b'/'
        curdir = b'.'
        pardir = b'..'
    else:
        sep = '/'
        curdir = '.'
        pardir = '..'
    if isabs(rest):
        rest = rest[1:]
        path = sep
    else:
        while rest:
            name, _, rest = rest.partition(sep)
            if name:
                if name == curdir:
                    pass
                elif name == pardir:
                    if path:
                        path, name = split(path)
                        if name == pardir:
                            path = join(path, pardir, pardir)
                    else:
                        path = pardir
                else:
                    newpath = join(path, name)
                    if not islink(newpath):
                        path = newpath
                    else:
                        if newpath in seen:
                            path = seen[newpath]
                            if path is not None:
                                pass
                            else:
                                return (
                                 join(newpath, rest), False)
                        else:
                            seen[newpath] = None
                            path, ok = _joinrealpath(path, os.readlink(newpath), seen)
                            return ok or (
                             join(path, rest), False)
                        seen[newpath] = path

    return (
     path, True)


supports_unicode_filenames = sys.platform == 'darwin'

def relpath--- This code section failed: ---

 L. 452         0  LOAD_FAST                'path'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 453         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'no path specified'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 455        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              fspath
               16  LOAD_FAST                'path'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'path'

 L. 456        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'path'
               26  LOAD_GLOBAL              bytes
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 457        32  LOAD_CONST               b'.'
               34  STORE_FAST               'curdir'

 L. 458        36  LOAD_CONST               b'/'
               38  STORE_FAST               'sep'

 L. 459        40  LOAD_CONST               b'..'
               42  STORE_FAST               'pardir'
               44  JUMP_FORWARD         58  'to 58'
             46_0  COME_FROM            30  '30'

 L. 461        46  LOAD_STR                 '.'
               48  STORE_FAST               'curdir'

 L. 462        50  LOAD_STR                 '/'
               52  STORE_FAST               'sep'

 L. 463        54  LOAD_STR                 '..'
               56  STORE_FAST               'pardir'
             58_0  COME_FROM            44  '44'

 L. 465        58  LOAD_FAST                'start'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L. 466        66  LOAD_FAST                'curdir'
               68  STORE_FAST               'start'
               70  JUMP_FORWARD         82  'to 82'
             72_0  COME_FROM            64  '64'

 L. 468        72  LOAD_GLOBAL              os
               74  LOAD_METHOD              fspath
               76  LOAD_FAST                'start'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'start'
             82_0  COME_FROM            70  '70'

 L. 470        82  SETUP_FINALLY       198  'to 198'

 L. 471        84  LOAD_LISTCOMP            '<code_object <listcomp>>'
               86  LOAD_STR                 'relpath.<locals>.<listcomp>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_GLOBAL              abspath
               92  LOAD_FAST                'start'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_METHOD              split
               98  LOAD_FAST                'sep'
              100  CALL_METHOD_1         1  ''
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'start_list'

 L. 472       108  LOAD_LISTCOMP            '<code_object <listcomp>>'
              110  LOAD_STR                 'relpath.<locals>.<listcomp>'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  LOAD_GLOBAL              abspath
              116  LOAD_FAST                'path'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_METHOD              split
              122  LOAD_FAST                'sep'
              124  CALL_METHOD_1         1  ''
              126  GET_ITER         
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'path_list'

 L. 474       132  LOAD_GLOBAL              len
              134  LOAD_GLOBAL              commonprefix
              136  LOAD_FAST                'start_list'
              138  LOAD_FAST                'path_list'
              140  BUILD_LIST_2          2 
              142  CALL_FUNCTION_1       1  ''
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'i'

 L. 476       148  LOAD_FAST                'pardir'
              150  BUILD_LIST_1          1 
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'start_list'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_FAST                'i'
              160  BINARY_SUBTRACT  
              162  BINARY_MULTIPLY  
              164  LOAD_FAST                'path_list'
              166  LOAD_FAST                'i'
              168  LOAD_CONST               None
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  BINARY_ADD       
              176  STORE_FAST               'rel_list'

 L. 477       178  LOAD_FAST                'rel_list'
              180  POP_JUMP_IF_TRUE    188  'to 188'

 L. 478       182  LOAD_FAST                'curdir'
              184  POP_BLOCK        
              186  RETURN_VALUE     
            188_0  COME_FROM           180  '180'

 L. 479       188  LOAD_GLOBAL              join
              190  LOAD_FAST                'rel_list'
              192  CALL_FUNCTION_EX      0  'positional arguments only'
              194  POP_BLOCK        
              196  RETURN_VALUE     
            198_0  COME_FROM_FINALLY    82  '82'

 L. 480       198  DUP_TOP          
              200  LOAD_GLOBAL              TypeError
              202  LOAD_GLOBAL              AttributeError
              204  LOAD_GLOBAL              BytesWarning
              206  LOAD_GLOBAL              DeprecationWarning
              208  BUILD_TUPLE_4         4 
              210  COMPARE_OP               exception-match
              212  POP_JUMP_IF_FALSE   240  'to 240'
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 481       220  LOAD_GLOBAL              genericpath
              222  LOAD_METHOD              _check_arg_types
              224  LOAD_STR                 'relpath'
              226  LOAD_FAST                'path'
              228  LOAD_FAST                'start'
              230  CALL_METHOD_3         3  ''
              232  POP_TOP          

 L. 482       234  RAISE_VARARGS_0       0  'reraise'
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           212  '212'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'

Parse error at or near `POP_TOP' instruction at offset 216


def commonpath--- This code section failed: ---

 L. 493         0  LOAD_FAST                'paths'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 494         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'commonpath() arg is an empty sequence'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 496        12  LOAD_GLOBAL              tuple
               14  LOAD_GLOBAL              map
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                fspath
               20  LOAD_FAST                'paths'
               22  CALL_FUNCTION_2       2  ''
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'paths'

 L. 497        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'paths'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_GLOBAL              bytes
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 498        42  LOAD_CONST               b'/'
               44  STORE_DEREF              'sep'

 L. 499        46  LOAD_CONST               b'.'
               48  STORE_DEREF              'curdir'
               50  JUMP_FORWARD         60  'to 60'
             52_0  COME_FROM            40  '40'

 L. 501        52  LOAD_STR                 '/'
               54  STORE_DEREF              'sep'

 L. 502        56  LOAD_STR                 '.'
               58  STORE_DEREF              'curdir'
             60_0  COME_FROM            50  '50'

 L. 504        60  SETUP_FINALLY       260  'to 260'

 L. 505        62  LOAD_CLOSURE             'sep'
               64  BUILD_TUPLE_1         1 
               66  LOAD_LISTCOMP            '<code_object <listcomp>>'
               68  LOAD_STR                 'commonpath.<locals>.<listcomp>'
               70  MAKE_FUNCTION_8          'closure'
               72  LOAD_FAST                'paths'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'split_paths'

 L. 507        80  SETUP_FINALLY       110  'to 110'

 L. 508        82  LOAD_GLOBAL              set
               84  LOAD_CLOSURE             'sep'
               86  BUILD_TUPLE_1         1 
               88  LOAD_GENEXPR             '<code_object <genexpr>>'
               90  LOAD_STR                 'commonpath.<locals>.<genexpr>'
               92  MAKE_FUNCTION_8          'closure'
               94  LOAD_FAST                'paths'
               96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  CALL_FUNCTION_1       1  ''
              102  UNPACK_SEQUENCE_1     1 
              104  STORE_FAST               'isabs'
              106  POP_BLOCK        
              108  JUMP_FORWARD        140  'to 140'
            110_0  COME_FROM_FINALLY    80  '80'

 L. 509       110  DUP_TOP          
              112  LOAD_GLOBAL              ValueError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   138  'to 138'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 510       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 "Can't mix absolute and relative paths"
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_CONST               None
              132  RAISE_VARARGS_2       2  'exception instance with __cause__'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           116  '116'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           108  '108'

 L. 512       140  LOAD_CLOSURE             'curdir'
              142  BUILD_TUPLE_1         1 
              144  LOAD_LISTCOMP            '<code_object <listcomp>>'
              146  LOAD_STR                 'commonpath.<locals>.<listcomp>'
              148  MAKE_FUNCTION_8          'closure'
              150  LOAD_FAST                'split_paths'
              152  GET_ITER         
              154  CALL_FUNCTION_1       1  ''
              156  STORE_FAST               'split_paths'

 L. 513       158  LOAD_GLOBAL              min
              160  LOAD_FAST                'split_paths'
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               's1'

 L. 514       166  LOAD_GLOBAL              max
              168  LOAD_FAST                'split_paths'
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               's2'

 L. 515       174  LOAD_FAST                's1'
              176  STORE_FAST               'common'

 L. 516       178  LOAD_GLOBAL              enumerate
              180  LOAD_FAST                's1'
              182  CALL_FUNCTION_1       1  ''
              184  GET_ITER         
            186_0  COME_FROM           204  '204'
              186  FOR_ITER            224  'to 224'
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'i'
              192  STORE_FAST               'c'

 L. 517       194  LOAD_FAST                'c'
              196  LOAD_FAST                's2'
              198  LOAD_FAST                'i'
              200  BINARY_SUBSCR    
              202  COMPARE_OP               !=
              204  POP_JUMP_IF_FALSE   186  'to 186'

 L. 518       206  LOAD_FAST                's1'
              208  LOAD_CONST               None
              210  LOAD_FAST                'i'
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  STORE_FAST               'common'

 L. 519       218  POP_TOP          
              220  BREAK_LOOP          224  'to 224'
              222  JUMP_BACK           186  'to 186'

 L. 521       224  LOAD_FAST                'isabs'
              226  POP_JUMP_IF_FALSE   232  'to 232'
              228  LOAD_DEREF               'sep'
              230  JUMP_FORWARD        242  'to 242'
            232_0  COME_FROM           226  '226'
              232  LOAD_DEREF               'sep'
              234  LOAD_CONST               None
              236  LOAD_CONST               0
              238  BUILD_SLICE_2         2 
              240  BINARY_SUBSCR    
            242_0  COME_FROM           230  '230'
              242  STORE_FAST               'prefix'

 L. 522       244  LOAD_FAST                'prefix'
              246  LOAD_DEREF               'sep'
              248  LOAD_METHOD              join
              250  LOAD_FAST                'common'
              252  CALL_METHOD_1         1  ''
              254  BINARY_ADD       
              256  POP_BLOCK        
              258  RETURN_VALUE     
            260_0  COME_FROM_FINALLY    60  '60'

 L. 523       260  DUP_TOP          
              262  LOAD_GLOBAL              TypeError
              264  LOAD_GLOBAL              AttributeError
              266  BUILD_TUPLE_2         2 
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   300  'to 300'
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          

 L. 524       280  LOAD_GLOBAL              genericpath
              282  LOAD_ATTR                _check_arg_types
              284  LOAD_CONST               ('commonpath',)
              286  LOAD_FAST                'paths'
              288  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              290  CALL_FUNCTION_EX      0  'positional arguments only'
              292  POP_TOP          

 L. 525       294  RAISE_VARARGS_0       0  'reraise'
              296  POP_EXCEPT       
              298  JUMP_FORWARD        302  'to 302'
            300_0  COME_FROM           270  '270'
              300  END_FINALLY      
            302_0  COME_FROM           298  '298'

Parse error at or near `POP_TOP' instruction at offset 276