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
    s = splitdrive(s)[1]
    return len(s) > 0 and s[0] in _get_bothseps(s)


def join--- This code section failed: ---

 L.  70         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L.  71        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.  72        20  LOAD_CONST               b'\\'
               22  STORE_FAST               'sep'

 L.  73        24  LOAD_CONST               b'\\/'
               26  STORE_FAST               'seps'

 L.  74        28  LOAD_CONST               b':'
               30  STORE_FAST               'colon'
               32  JUMP_FORWARD         46  'to 46'
             34_0  COME_FROM            18  '18'

 L.  76        34  LOAD_STR                 '\\'
               36  STORE_FAST               'sep'

 L.  77        38  LOAD_STR                 '\\/'
               40  STORE_FAST               'seps'

 L.  78        42  LOAD_STR                 ':'
               44  STORE_FAST               'colon'
             46_0  COME_FROM            32  '32'

 L.  79        46  SETUP_FINALLY       288  'to 288'

 L.  80        48  LOAD_FAST                'paths'
               50  POP_JUMP_IF_TRUE     68  'to 68'

 L.  81        52  LOAD_FAST                'path'
               54  LOAD_CONST               None
               56  LOAD_CONST               0
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'sep'
               64  BINARY_ADD       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'

 L.  82        68  LOAD_GLOBAL              splitdrive
               70  LOAD_FAST                'path'
               72  CALL_FUNCTION_1       1  ''
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'result_drive'
               78  STORE_FAST               'result_path'

 L.  83        80  LOAD_GLOBAL              map
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

 L.  84        96  LOAD_GLOBAL              splitdrive
               98  LOAD_FAST                'p'
              100  CALL_FUNCTION_1       1  ''
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'p_drive'
              106  STORE_FAST               'p_path'

 L.  85       108  LOAD_FAST                'p_path'
              110  POP_JUMP_IF_FALSE   144  'to 144'
              112  LOAD_FAST                'p_path'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'seps'
              120  COMPARE_OP               in
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L.  87       124  LOAD_FAST                'p_drive'
              126  POP_JUMP_IF_TRUE    132  'to 132'
              128  LOAD_FAST                'result_drive'
              130  POP_JUMP_IF_TRUE    136  'to 136'
            132_0  COME_FROM           126  '126'

 L.  88       132  LOAD_FAST                'p_drive'
              134  STORE_FAST               'result_drive'
            136_0  COME_FROM           130  '130'

 L.  89       136  LOAD_FAST                'p_path'
              138  STORE_FAST               'result_path'

 L.  90       140  JUMP_BACK            92  'to 92'
              142  BREAK_LOOP          186  'to 186'
            144_0  COME_FROM           122  '122'
            144_1  COME_FROM           110  '110'

 L.  91       144  LOAD_FAST                'p_drive'
              146  POP_JUMP_IF_FALSE   186  'to 186'
              148  LOAD_FAST                'p_drive'
              150  LOAD_FAST                'result_drive'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_FALSE   186  'to 186'

 L.  92       156  LOAD_FAST                'p_drive'
              158  LOAD_METHOD              lower
              160  CALL_METHOD_0         0  ''
              162  LOAD_FAST                'result_drive'
              164  LOAD_METHOD              lower
              166  CALL_METHOD_0         0  ''
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L.  94       172  LOAD_FAST                'p_drive'
              174  STORE_FAST               'result_drive'

 L.  95       176  LOAD_FAST                'p_path'
              178  STORE_FAST               'result_path'

 L.  96       180  JUMP_BACK            92  'to 92'
            182_0  COME_FROM           170  '170'

 L.  98       182  LOAD_FAST                'p_drive'
              184  STORE_FAST               'result_drive'
            186_0  COME_FROM           154  '154'
            186_1  COME_FROM           146  '146'
            186_2  COME_FROM           142  '142'

 L. 100       186  LOAD_FAST                'result_path'
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  LOAD_FAST                'result_path'
              192  LOAD_CONST               -1
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'seps'
              198  COMPARE_OP               not-in
              200  POP_JUMP_IF_FALSE   210  'to 210'

 L. 101       202  LOAD_FAST                'result_path'
              204  LOAD_FAST                'sep'
              206  BINARY_ADD       
              208  STORE_FAST               'result_path'
            210_0  COME_FROM           200  '200'
            210_1  COME_FROM           188  '188'

 L. 102       210  LOAD_FAST                'result_path'
              212  LOAD_FAST                'p_path'
              214  BINARY_ADD       
              216  STORE_FAST               'result_path'
              218  JUMP_BACK            92  'to 92'
            220_0  COME_FROM            92  '92'

 L. 104       220  LOAD_FAST                'result_path'
          222_224  POP_JUMP_IF_FALSE   278  'to 278'
              226  LOAD_FAST                'result_path'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'seps'
              234  COMPARE_OP               not-in
          236_238  POP_JUMP_IF_FALSE   278  'to 278'

 L. 105       240  LOAD_FAST                'result_drive'

 L. 104   242_244  POP_JUMP_IF_FALSE   278  'to 278'

 L. 105       246  LOAD_FAST                'result_drive'
              248  LOAD_CONST               -1
              250  LOAD_CONST               None
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  LOAD_FAST                'colon'
              258  COMPARE_OP               !=

 L. 104   260_262  POP_JUMP_IF_FALSE   278  'to 278'

 L. 106       264  LOAD_FAST                'result_drive'
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

 L. 107       278  LOAD_FAST                'result_drive'
              280  LOAD_FAST                'result_path'
              282  BINARY_ADD       
              284  POP_BLOCK        
              286  RETURN_VALUE     
            288_0  COME_FROM_FINALLY    46  '46'

 L. 108       288  DUP_TOP          
              290  LOAD_GLOBAL              TypeError
              292  LOAD_GLOBAL              AttributeError
              294  LOAD_GLOBAL              BytesWarning
              296  BUILD_TUPLE_3         3 
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   334  'to 334'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 109       310  LOAD_GLOBAL              genericpath
              312  LOAD_ATTR                _check_arg_types
              314  LOAD_STR                 'join'
              316  LOAD_FAST                'path'
              318  BUILD_TUPLE_2         2 
              320  LOAD_FAST                'paths'
              322  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              324  CALL_FUNCTION_EX      0  'positional arguments only'
              326  POP_TOP          

 L. 110       328  RAISE_VARARGS_0       0  'reraise'
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

 L. 530         0  LOAD_FAST                'seen'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 531         8  LOAD_GLOBAL              set
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'seen'
             14_0  COME_FROM             6  '6'

 L. 547        14  LOAD_CONST               (1, 2, 3, 5, 21, 32, 50, 67, 87, 4390, 4392, 4393)
               16  STORE_FAST               'allowed_winerror'
             18_0  COME_FROM           134  '134'
             18_1  COME_FROM           130  '130'
             18_2  COME_FROM           108  '108'
             18_3  COME_FROM            56  '56'

 L. 549        18  LOAD_GLOBAL              normcase
               20  LOAD_FAST                'path'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'seen'
               26  COMPARE_OP               not-in
               28  POP_JUMP_IF_FALSE   136  'to 136'

 L. 550        30  LOAD_FAST                'seen'
               32  LOAD_METHOD              add
               34  LOAD_GLOBAL              normcase
               36  LOAD_FAST                'path'
               38  CALL_FUNCTION_1       1  ''
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 551        44  SETUP_FINALLY        58  'to 58'

 L. 552        46  LOAD_GLOBAL              _nt_readlink
               48  LOAD_FAST                'path'
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'path'
               54  POP_BLOCK        
               56  JUMP_BACK            18  'to 18'
             58_0  COME_FROM_FINALLY    44  '44'

 L. 553        58  DUP_TOP          
               60  LOAD_GLOBAL              OSError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   110  'to 110'
               66  POP_TOP          
               68  STORE_FAST               'ex'
               70  POP_TOP          
               72  SETUP_FINALLY        98  'to 98'

 L. 554        74  LOAD_FAST                'ex'
               76  LOAD_ATTR                winerror
               78  LOAD_FAST                'allowed_winerror'
               80  COMPARE_OP               in
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L. 555        84  POP_BLOCK        
               86  POP_EXCEPT       
               88  CALL_FINALLY         98  'to 98'
               90  JUMP_FORWARD        136  'to 136'
             92_0  COME_FROM            82  '82'

 L. 556        92  RAISE_VARARGS_0       0  'reraise'
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM_FINALLY    72  '72'
               98  LOAD_CONST               None
              100  STORE_FAST               'ex'
              102  DELETE_FAST              'ex'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_BACK            18  'to 18'
            110_0  COME_FROM            64  '64'

 L. 557       110  DUP_TOP          
              112  LOAD_GLOBAL              ValueError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   132  'to 132'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 559       124  POP_EXCEPT       
              126  BREAK_LOOP          136  'to 136'
              128  POP_EXCEPT       
              130  JUMP_BACK            18  'to 18'
            132_0  COME_FROM           116  '116'
              132  END_FINALLY      
              134  JUMP_BACK            18  'to 18'
            136_0  COME_FROM           126  '126'
            136_1  COME_FROM            90  '90'
            136_2  COME_FROM            28  '28'

 L. 560       136  LOAD_FAST                'path'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 86


        def _getfinalpathname_nonstrict--- This code section failed: ---

 L. 577         0  LOAD_CONST               (1, 2, 3, 5, 21, 32, 50, 67, 87, 123, 1920, 1921)
                2  STORE_FAST               'allowed_winerror'

 L. 581         4  LOAD_STR                 ''
                6  STORE_FAST               'tail'

 L. 582         8  LOAD_GLOBAL              set
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'seen'
             14_0  COME_FROM           162  '162'
             14_1  COME_FROM           158  '158'

 L. 583        14  LOAD_FAST                'path'
               16  POP_JUMP_IF_FALSE   164  'to 164'

 L. 584        18  SETUP_FINALLY        58  'to 58'

 L. 585        20  LOAD_GLOBAL              _readlink_deep
               22  LOAD_FAST                'path'
               24  LOAD_FAST                'seen'
               26  CALL_FUNCTION_2       2  ''
               28  STORE_FAST               'path'

 L. 586        30  LOAD_GLOBAL              _getfinalpathname
               32  LOAD_FAST                'path'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'path'

 L. 587        38  LOAD_FAST                'tail'
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  LOAD_GLOBAL              join
               44  LOAD_FAST                'path'
               46  LOAD_FAST                'tail'
               48  CALL_FUNCTION_2       2  ''
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            40  '40'
               52  LOAD_FAST                'path'
             54_0  COME_FROM            50  '50'
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    18  '18'

 L. 588        58  DUP_TOP          
               60  LOAD_GLOBAL              OSError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   160  'to 160'
               66  POP_TOP          
               68  STORE_FAST               'ex'
               70  POP_TOP          
               72  SETUP_FINALLY       148  'to 148'

 L. 589        74  LOAD_FAST                'ex'
               76  LOAD_ATTR                winerror
               78  LOAD_FAST                'allowed_winerror'
               80  COMPARE_OP               not-in
               82  POP_JUMP_IF_FALSE    86  'to 86'

 L. 590        84  RAISE_VARARGS_0       0  'reraise'
             86_0  COME_FROM            82  '82'

 L. 591        86  LOAD_GLOBAL              split
               88  LOAD_FAST                'path'
               90  CALL_FUNCTION_1       1  ''
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'path'
               96  STORE_FAST               'name'

 L. 595        98  LOAD_FAST                'path'
              100  POP_JUMP_IF_FALSE   126  'to 126'
              102  LOAD_FAST                'name'
              104  POP_JUMP_IF_TRUE    126  'to 126'

 L. 596       106  LOAD_GLOBAL              abspath
              108  LOAD_FAST                'path'
              110  LOAD_FAST                'tail'
              112  BINARY_ADD       
              114  CALL_FUNCTION_1       1  ''
              116  ROT_FOUR         
              118  POP_BLOCK        
              120  POP_EXCEPT       
              122  CALL_FINALLY        148  'to 148'
              124  RETURN_VALUE     
            126_0  COME_FROM           104  '104'
            126_1  COME_FROM           100  '100'

 L. 597       126  LOAD_FAST                'tail'
              128  POP_JUMP_IF_FALSE   140  'to 140'
              130  LOAD_GLOBAL              join
              132  LOAD_FAST                'name'
              134  LOAD_FAST                'tail'
              136  CALL_FUNCTION_2       2  ''
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           128  '128'
              140  LOAD_FAST                'name'
            142_0  COME_FROM           138  '138'
              142  STORE_FAST               'tail'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM           122  '122'
            148_1  COME_FROM_FINALLY    72  '72'
              148  LOAD_CONST               None
              150  STORE_FAST               'ex'
              152  DELETE_FAST              'ex'
              154  END_FINALLY      
              156  POP_EXCEPT       
              158  JUMP_BACK            14  'to 14'
            160_0  COME_FROM            64  '64'
              160  END_FINALLY      
              162  JUMP_BACK            14  'to 14'
            164_0  COME_FROM            16  '16'

 L. 598       164  LOAD_GLOBAL              abspath
              166  LOAD_FAST                'tail'
              168  CALL_FUNCTION_1       1  ''
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 118


        def realpath(path):
            path = normpath(path)
            if isinstance(path, bytes):
                prefix = b'\\\\?\\'
                unc_prefix = b'\\\\?\\UNC\\'
                new_unc_prefix = b'\\\\'
                cwd = os.getcwdb()
            else:
                prefix = '\\\\?\\'
                unc_prefix = '\\\\?\\UNC\\'
                new_unc_prefix = '\\\\'
                cwd = os.getcwd()
            had_prefix = path.startswith(prefix)
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