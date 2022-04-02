# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
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
        return b'\\/'
    return '\\/'


def normcase(s):
    """Normalize case of pathname.

    Makes all characters lowercase and all slashes into backslashes."""
    s = os.fspath(s)
    if isinstance(s, bytes):
        return s.replace(b'/', b'\\').lower()
    return s.replace('/', '\\').lower()


def isabs(s):
    """Test whether a path is absolute"""
    s = os.fspath(s)
    if isinstance(s, bytes):
        if s.replace(b'/', b'\\').startswith(b'\\\\?\\'):
            return True
    elif s.replace('/', '\\').startswith('\\\\?\\'):
        return True
    s = splitdrive(s)[1]
    return len(s) > 0 and s[0] in _get_bothseps(s)


def join--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L.  79        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.  80        20  LOAD_CONST               b'\\'
               22  STORE_FAST               'sep'

 L.  81        24  LOAD_CONST               b'\\/'
               26  STORE_FAST               'seps'

 L.  82        28  LOAD_CONST               b':'
               30  STORE_FAST               'colon'
               32  JUMP_FORWARD         46  'to 46'
             34_0  COME_FROM            18  '18'

 L.  84        34  LOAD_STR                 '\\'
               36  STORE_FAST               'sep'

 L.  85        38  LOAD_STR                 '\\/'
               40  STORE_FAST               'seps'

 L.  86        42  LOAD_STR                 ':'
               44  STORE_FAST               'colon'
             46_0  COME_FROM            32  '32'

 L.  87        46  SETUP_FINALLY       288  'to 288'

 L.  88        48  LOAD_FAST                'paths'
               50  POP_JUMP_IF_TRUE     68  'to 68'

 L.  89        52  LOAD_FAST                'path'
               54  LOAD_CONST               None
               56  LOAD_CONST               0
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'sep'
               64  BINARY_ADD       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'

 L.  90        68  LOAD_GLOBAL              splitdrive
               70  LOAD_FAST                'path'
               72  CALL_FUNCTION_1       1  ''
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'result_drive'
               78  STORE_FAST               'result_path'

 L.  91        80  LOAD_GLOBAL              map
               82  LOAD_GLOBAL              os
               84  LOAD_ATTR                fspath
               86  LOAD_FAST                'paths'
               88  CALL_FUNCTION_2       2  ''
               90  GET_ITER         
             92_0  COME_FROM           218  '218'
             92_1  COME_FROM           180  '180'
             92_2  COME_FROM           140  '140'
               92  FOR_ITER            220  'to 220'
               94  STORE_FAST               'p'

 L.  92        96  LOAD_GLOBAL              splitdrive
               98  LOAD_FAST                'p'
              100  CALL_FUNCTION_1       1  ''
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'p_drive'
              106  STORE_FAST               'p_path'

 L.  93       108  LOAD_FAST                'p_path'
              110  POP_JUMP_IF_FALSE   144  'to 144'
              112  LOAD_FAST                'p_path'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'seps'
              120  COMPARE_OP               in
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L.  95       124  LOAD_FAST                'p_drive'
              126  POP_JUMP_IF_TRUE    132  'to 132'
              128  LOAD_FAST                'result_drive'
              130  POP_JUMP_IF_TRUE    136  'to 136'
            132_0  COME_FROM           126  '126'

 L.  96       132  LOAD_FAST                'p_drive'
              134  STORE_FAST               'result_drive'
            136_0  COME_FROM           130  '130'

 L.  97       136  LOAD_FAST                'p_path'
              138  STORE_FAST               'result_path'

 L.  98       140  JUMP_BACK            92  'to 92'
              142  BREAK_LOOP          186  'to 186'
            144_0  COME_FROM           122  '122'
            144_1  COME_FROM           110  '110'

 L.  99       144  LOAD_FAST                'p_drive'
              146  POP_JUMP_IF_FALSE   186  'to 186'
              148  LOAD_FAST                'p_drive'
              150  LOAD_FAST                'result_drive'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_FALSE   186  'to 186'

 L. 100       156  LOAD_FAST                'p_drive'
              158  LOAD_METHOD              lower
              160  CALL_METHOD_0         0  ''
              162  LOAD_FAST                'result_drive'
              164  LOAD_METHOD              lower
              166  CALL_METHOD_0         0  ''
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L. 102       172  LOAD_FAST                'p_drive'
              174  STORE_FAST               'result_drive'

 L. 103       176  LOAD_FAST                'p_path'
              178  STORE_FAST               'result_path'

 L. 104       180  JUMP_BACK            92  'to 92'
            182_0  COME_FROM           170  '170'

 L. 106       182  LOAD_FAST                'p_drive'
              184  STORE_FAST               'result_drive'
            186_0  COME_FROM           154  '154'
            186_1  COME_FROM           146  '146'
            186_2  COME_FROM           142  '142'

 L. 108       186  LOAD_FAST                'result_path'
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  LOAD_FAST                'result_path'
              192  LOAD_CONST               -1
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'seps'
              198  COMPARE_OP               not-in
              200  POP_JUMP_IF_FALSE   210  'to 210'

 L. 109       202  LOAD_FAST                'result_path'
              204  LOAD_FAST                'sep'
              206  BINARY_ADD       
              208  STORE_FAST               'result_path'
            210_0  COME_FROM           200  '200'
            210_1  COME_FROM           188  '188'

 L. 110       210  LOAD_FAST                'result_path'
              212  LOAD_FAST                'p_path'
              214  BINARY_ADD       
              216  STORE_FAST               'result_path'
              218  JUMP_BACK            92  'to 92'
            220_0  COME_FROM            92  '92'

 L. 112       220  LOAD_FAST                'result_path'
          222_224  POP_JUMP_IF_FALSE   278  'to 278'
              226  LOAD_FAST                'result_path'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'seps'
              234  COMPARE_OP               not-in
          236_238  POP_JUMP_IF_FALSE   278  'to 278'

 L. 113       240  LOAD_FAST                'result_drive'

 L. 112   242_244  POP_JUMP_IF_FALSE   278  'to 278'

 L. 113       246  LOAD_FAST                'result_drive'
              248  LOAD_CONST               -1
              250  LOAD_CONST               None
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  LOAD_FAST                'colon'
              258  COMPARE_OP               !=

 L. 112   260_262  POP_JUMP_IF_FALSE   278  'to 278'

 L. 114       264  LOAD_FAST                'result_drive'
              266  LOAD_FAST                'sep'
              268  BINARY_ADD       
              270  LOAD_FAST                'result_path'
              272  BINARY_ADD       
              274  POP_BLOCK        
              276  RETURN_VALUE     
            278_0  COME_FROM           260  '260'
            278_1  COME_FROM           242  '242'
            278_2  COME_FROM           236  '236'
            278_3  COME_FROM           222  '222'

 L. 115       278  LOAD_FAST                'result_drive'
              280  LOAD_FAST                'result_path'
              282  BINARY_ADD       
              284  POP_BLOCK        
              286  RETURN_VALUE     
            288_0  COME_FROM_FINALLY    46  '46'

 L. 116       288  DUP_TOP          
              290  LOAD_GLOBAL              TypeError
              292  LOAD_GLOBAL              AttributeError
              294  LOAD_GLOBAL              BytesWarning
              296  BUILD_TUPLE_3         3 
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   334  'to 334'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 117       310  LOAD_GLOBAL              genericpath
              312  LOAD_ATTR                _check_arg_types
              314  LOAD_STR                 'join'
              316  LOAD_FAST                'path'
              318  BUILD_TUPLE_2         2 
              320  LOAD_FAST                'paths'
              322  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              324  CALL_FUNCTION_EX      0  'positional arguments only'
              326  POP_TOP          

 L. 118       328  RAISE_VARARGS_0       0  'reraise'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           300  '300'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'

Parse error at or near `LOAD_FAST' instruction at offset 220


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
            sep = b'\\'
            altsep = b'/'
            colon = b':'
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
        return genericpath._splitext(p, b'\\', b'/', b'.')
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
    except (OSError, ValueError, AttributeError):
        return False
    else:
        return stat.S_ISLNK(st.st_mode)


def lexists(path):
    """Test whether a path exists.  Returns True for broken symbolic links"""
    try:
        st = os.lstat(path)
    except (OSError, ValueError):
        return False
    else:
        return True


try:
    from nt import _getvolumepathname
except ImportError:
    _getvolumepathname = None
else:

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
            tilde = b'~'
        else:
            tilde = '~'
        if not path.startswith(tilde):
            return path
        i, n = 1, len(path)
        while i < n:
            if path[i] not in _get_bothseps(path):
                i += 1

        if 'USERPROFILE' in os.environ:
            userhome = os.environ['USERPROFILE']
        else:
            if 'HOMEPATH' not in os.environ:
                return path
            try:
                drive = os.environ['HOMEDRIVE']
            except KeyError:
                drive = ''
            else:
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
            if b'$' not in path:
                if b'%' not in path:
                    return path
            import string
            varchars = bytes(string.ascii_letters + string.digits + '_-', 'ascii')
            quote = b"'"
            percent = b'%'
            brace = b'{'
            rbrace = b'}'
            dollar = b'$'
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
        while True:
            if index < pathlen:
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
                            else:
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
                            else:
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
                        else:
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
            sep = b'\\'
            altsep = b'/'
            curdir = b'.'
            pardir = b'..'
            special_prefixes = (b'\\\\.\\', b'\\\\?\\')
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
        while True:
            if i < len(comps):
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


    def _abspath_fallback(path):
        """Return the absolute version of a path as a fallback function in case
    `nt._getfullpathname` is not available or raises OSError. See bpo-31047 for
    more.

    """
        path = os.fspath(path)
        if not isabs(path):
            if isinstance(path, bytes):
                cwd = os.getcwdb()
            else:
                cwd = os.getcwd()
            path = join(cwd, path)
        return normpath(path)


    try:
        from nt import _getfullpathname
    except ImportError:
        abspath = _abspath_fallback
    else:

        def abspath(path):
            """Return the absolute version of a path."""
            try:
                return normpath(_getfullpathname(path))
            except (OSError, ValueError):
                return _abspath_fallback(path)


    try:
        from nt import _getfinalpathname, readlink as _nt_readlink
    except ImportError:
        realpath = abspath
    else:

        def _readlink_deep--- This code section failed: ---

 L. 552         0  LOAD_CONST               (1, 2, 3, 5, 21, 32, 50, 67, 87, 4390, 4392, 4393)
                2  STORE_FAST               'allowed_winerror'

 L. 554         4  LOAD_GLOBAL              set
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'seen'
             10_0  COME_FROM           172  '172'
             10_1  COME_FROM           168  '168'
             10_2  COME_FROM           146  '146'
             10_3  COME_FROM            94  '94'

 L. 555        10  LOAD_GLOBAL              normcase
               12  LOAD_FAST                'path'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_FAST                'seen'
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_FALSE   174  'to 174'

 L. 556        22  LOAD_FAST                'seen'
               24  LOAD_METHOD              add
               26  LOAD_GLOBAL              normcase
               28  LOAD_FAST                'path'
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 557        36  SETUP_FINALLY        96  'to 96'

 L. 558        38  LOAD_FAST                'path'
               40  STORE_FAST               'old_path'

 L. 559        42  LOAD_GLOBAL              _nt_readlink
               44  LOAD_FAST                'path'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'path'

 L. 562        50  LOAD_GLOBAL              isabs
               52  LOAD_FAST                'path'
               54  CALL_FUNCTION_1       1  ''
               56  POP_JUMP_IF_TRUE     92  'to 92'

 L. 566        58  LOAD_GLOBAL              islink
               60  LOAD_FAST                'old_path'
               62  CALL_FUNCTION_1       1  ''
               64  POP_JUMP_IF_TRUE     74  'to 74'

 L. 567        66  LOAD_FAST                'old_path'
               68  STORE_FAST               'path'

 L. 568        70  POP_BLOCK        
               72  BREAK_LOOP          174  'to 174'
             74_0  COME_FROM            64  '64'

 L. 569        74  LOAD_GLOBAL              normpath
               76  LOAD_GLOBAL              join
               78  LOAD_GLOBAL              dirname
               80  LOAD_FAST                'old_path'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_FAST                'path'
               86  CALL_FUNCTION_2       2  ''
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'path'
             92_0  COME_FROM            56  '56'
               92  POP_BLOCK        
               94  JUMP_BACK            10  'to 10'
             96_0  COME_FROM_FINALLY    36  '36'

 L. 570        96  DUP_TOP          
               98  LOAD_GLOBAL              OSError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   148  'to 148'
              104  POP_TOP          
              106  STORE_FAST               'ex'
              108  POP_TOP          
              110  SETUP_FINALLY       136  'to 136'

 L. 571       112  LOAD_FAST                'ex'
              114  LOAD_ATTR                winerror
              116  LOAD_FAST                'allowed_winerror'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 572       122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        136  'to 136'
              128  JUMP_FORWARD        174  'to 174'
            130_0  COME_FROM           120  '120'

 L. 573       130  RAISE_VARARGS_0       0  'reraise'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM           126  '126'
            136_1  COME_FROM_FINALLY   110  '110'
              136  LOAD_CONST               None
              138  STORE_FAST               'ex'
              140  DELETE_FAST              'ex'
              142  END_FINALLY      
              144  POP_EXCEPT       
              146  JUMP_BACK            10  'to 10'
            148_0  COME_FROM           102  '102'

 L. 574       148  DUP_TOP          
              150  LOAD_GLOBAL              ValueError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   170  'to 170'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 576       162  POP_EXCEPT       
              164  BREAK_LOOP          174  'to 174'
              166  POP_EXCEPT       
              168  JUMP_BACK            10  'to 10'
            170_0  COME_FROM           154  '154'
              170  END_FINALLY      
              172  JUMP_BACK            10  'to 10'
            174_0  COME_FROM           164  '164'
            174_1  COME_FROM           128  '128'
            174_2  COME_FROM            72  '72'
            174_3  COME_FROM            20  '20'

 L. 577       174  LOAD_FAST                'path'
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 124


        def _getfinalpathname_nonstrict--- This code section failed: ---

 L. 594         0  LOAD_CONST               (1, 2, 3, 5, 21, 32, 50, 67, 87, 123, 1920, 1921)
                2  STORE_FAST               'allowed_winerror'

 L. 598         4  LOAD_STR                 ''
                6  STORE_FAST               'tail'
              8_0  COME_FROM           212  '212'
              8_1  COME_FROM           208  '208'

 L. 599         8  LOAD_FAST                'path'
               10  POP_JUMP_IF_FALSE   214  'to 214'

 L. 600        12  SETUP_FINALLY        42  'to 42'

 L. 601        14  LOAD_GLOBAL              _getfinalpathname
               16  LOAD_FAST                'path'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'path'

 L. 602        22  LOAD_FAST                'tail'
               24  POP_JUMP_IF_FALSE    36  'to 36'
               26  LOAD_GLOBAL              join
               28  LOAD_FAST                'path'
               30  LOAD_FAST                'tail'
               32  CALL_FUNCTION_2       2  ''
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            24  '24'
               36  LOAD_FAST                'path'
             38_0  COME_FROM            34  '34'
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    12  '12'

 L. 603        42  DUP_TOP          
               44  LOAD_GLOBAL              OSError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE   210  'to 210'
               50  POP_TOP          
               52  STORE_FAST               'ex'
               54  POP_TOP          
               56  SETUP_FINALLY       198  'to 198'

 L. 604        58  LOAD_FAST                'ex'
               60  LOAD_ATTR                winerror
               62  LOAD_FAST                'allowed_winerror'
               64  COMPARE_OP               not-in
               66  POP_JUMP_IF_FALSE    70  'to 70'

 L. 605        68  RAISE_VARARGS_0       0  'reraise'
             70_0  COME_FROM            66  '66'

 L. 606        70  SETUP_FINALLY       120  'to 120'

 L. 610        72  LOAD_GLOBAL              _readlink_deep
               74  LOAD_FAST                'path'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'new_path'

 L. 611        80  LOAD_FAST                'new_path'
               82  LOAD_FAST                'path'
               84  COMPARE_OP               !=
               86  POP_JUMP_IF_FALSE   116  'to 116'

 L. 612        88  LOAD_FAST                'tail'
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  LOAD_GLOBAL              join
               94  LOAD_FAST                'new_path'
               96  LOAD_FAST                'tail'
               98  CALL_FUNCTION_2       2  ''
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            90  '90'
              102  LOAD_FAST                'new_path'
            104_0  COME_FROM           100  '100'
              104  POP_BLOCK        
              106  ROT_FOUR         
              108  POP_BLOCK        
              110  POP_EXCEPT       
              112  CALL_FINALLY        198  'to 198'
              114  RETURN_VALUE     
            116_0  COME_FROM            86  '86'
              116  POP_BLOCK        
              118  JUMP_FORWARD        140  'to 140'
            120_0  COME_FROM_FINALLY    70  '70'

 L. 613       120  DUP_TOP          
              122  LOAD_GLOBAL              OSError
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   138  'to 138'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 615       134  POP_EXCEPT       
              136  BREAK_LOOP          140  'to 140'
            138_0  COME_FROM           126  '126'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           118  '118'

 L. 616       140  LOAD_GLOBAL              split
              142  LOAD_FAST                'path'
              144  CALL_FUNCTION_1       1  ''
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'path'
              150  STORE_FAST               'name'

 L. 620       152  LOAD_FAST                'path'
              154  POP_JUMP_IF_FALSE   176  'to 176'
              156  LOAD_FAST                'name'
              158  POP_JUMP_IF_TRUE    176  'to 176'

 L. 621       160  LOAD_FAST                'path'
              162  LOAD_FAST                'tail'
              164  BINARY_ADD       
              166  ROT_FOUR         
              168  POP_BLOCK        
              170  POP_EXCEPT       
              172  CALL_FINALLY        198  'to 198'
              174  RETURN_VALUE     
            176_0  COME_FROM           158  '158'
            176_1  COME_FROM           154  '154'

 L. 622       176  LOAD_FAST                'tail'
              178  POP_JUMP_IF_FALSE   190  'to 190'
              180  LOAD_GLOBAL              join
              182  LOAD_FAST                'name'
              184  LOAD_FAST                'tail'
              186  CALL_FUNCTION_2       2  ''
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           178  '178'
              190  LOAD_FAST                'name'
            192_0  COME_FROM           188  '188'
              192  STORE_FAST               'tail'
              194  POP_BLOCK        
              196  BEGIN_FINALLY    
            198_0  COME_FROM           172  '172'
            198_1  COME_FROM           112  '112'
            198_2  COME_FROM_FINALLY    56  '56'
              198  LOAD_CONST               None
              200  STORE_FAST               'ex'
              202  DELETE_FAST              'ex'
              204  END_FINALLY      
              206  POP_EXCEPT       
              208  JUMP_BACK             8  'to 8'
            210_0  COME_FROM            48  '48'
              210  END_FINALLY      
              212  JUMP_BACK             8  'to 8'
            214_0  COME_FROM            10  '10'

 L. 623       214  LOAD_FAST                'tail'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 106


        def realpath(path):
            path = normpath(path)
            if isinstance(path, bytes):
                prefix = b'\\\\?\\'
                unc_prefix = b'\\\\?\\UNC\\'
                new_unc_prefix = b'\\\\'
                cwd = os.getcwdb()
                if normcase(path) == normcase(os.fsencode(devnull)):
                    return b'\\\\.\\NUL'
            else:
                prefix = '\\\\?\\'
                unc_prefix = '\\\\?\\UNC\\'
                new_unc_prefix = '\\\\'
                cwd = os.getcwd()
                if normcase(path) == normcase(devnull):
                    return '\\\\.\\NUL'
            had_prefix = path.startswith(prefix)
            if not had_prefix:
                if not isabs(path):
                    path = join(cwd, path)
            try:
                path = _getfinalpathname(path)
                initial_winerror = 0
            except OSError as ex:
                try:
                    initial_winerror = ex.winerror
                    path = _getfinalpathname_nonstrict(path)
                finally:
                    ex = None
                    del ex

            else:
                if not had_prefix:
                    if path.startswith(prefix):
                        if path.startswith(unc_prefix):
                            spath = new_unc_prefix + path[len(unc_prefix):]
                        else:
                            spath = path[len(prefix):]
                        try:
                            if _getfinalpathname(spath) == path:
                                path = spath
                        except OSError as ex:
                            try:
                                if ex.winerror == initial_winerror:
                                    path = spath
                            finally:
                                ex = None
                                del ex

                        else:
                            return path


    supports_unicode_filenames = hasattr(sys, 'getwindowsversion') and sys.getwindowsversion()[3] >= 2

    def relpath(path, start=None):
        """Return a relative version of a path"""
        path = os.fspath(path)
        if isinstance(path, bytes):
            sep = b'\\'
            curdir = b'.'
            pardir = b'..'
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
            else:
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
            sep = b'\\'
            altsep = b'/'
            curdir = b'.'
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
            else:
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
    from nt import _isdir as isdir
except ImportError:
    pass