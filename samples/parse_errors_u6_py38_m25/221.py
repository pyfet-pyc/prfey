# uncompyle6 version 3.7.4
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
              142  JUMP_FORWARD        186  'to 186'
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

Parse error at or near `JUMP_FORWARD' instruction at offset 142


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
                    return (
                     p[:0], p)
                index2 = normp.find(sep, index + 1)
                if index2 == index + 1:
                    return (
                     p[:0], p)
                if index2 == -1:
                    index2 = len(p)
                return (
                 p[:index2], p[index2:])
        if normp[1:2] == colon:
            return (
             p[:2], p[2:])
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
    return (d + head, tail)


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
        else:
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


    def expandvars--- This code section failed: ---

 L. 341         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L. 342        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE   104  'to 104'

 L. 343        20  LOAD_CONST               b'$'
               22  LOAD_FAST                'path'
               24  COMPARE_OP               not-in
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  LOAD_CONST               b'%'
               30  LOAD_FAST                'path'
               32  COMPARE_OP               not-in
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 344        36  LOAD_FAST                'path'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM            26  '26'

 L. 345        40  LOAD_CONST               0
               42  LOAD_CONST               None
               44  IMPORT_NAME              string
               46  STORE_FAST               'string'

 L. 346        48  LOAD_GLOBAL              bytes
               50  LOAD_FAST                'string'
               52  LOAD_ATTR                ascii_letters
               54  LOAD_FAST                'string'
               56  LOAD_ATTR                digits
               58  BINARY_ADD       
               60  LOAD_STR                 '_-'
               62  BINARY_ADD       
               64  LOAD_STR                 'ascii'
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'varchars'

 L. 347        70  LOAD_CONST               b"'"
               72  STORE_FAST               'quote'

 L. 348        74  LOAD_CONST               b'%'
               76  STORE_FAST               'percent'

 L. 349        78  LOAD_CONST               b'{'
               80  STORE_FAST               'brace'

 L. 350        82  LOAD_CONST               b'}'
               84  STORE_FAST               'rbrace'

 L. 351        86  LOAD_CONST               b'$'
               88  STORE_FAST               'dollar'

 L. 352        90  LOAD_GLOBAL              getattr
               92  LOAD_GLOBAL              os
               94  LOAD_STR                 'environb'
               96  LOAD_CONST               None
               98  CALL_FUNCTION_3       3  ''
              100  STORE_FAST               'environ'
              102  JUMP_FORWARD        174  'to 174'
            104_0  COME_FROM            18  '18'

 L. 354       104  LOAD_STR                 '$'
              106  LOAD_FAST                'path'
              108  COMPARE_OP               not-in
              110  POP_JUMP_IF_FALSE   124  'to 124'
              112  LOAD_STR                 '%'
              114  LOAD_FAST                'path'
              116  COMPARE_OP               not-in
              118  POP_JUMP_IF_FALSE   124  'to 124'

 L. 355       120  LOAD_FAST                'path'
              122  RETURN_VALUE     
            124_0  COME_FROM           118  '118'
            124_1  COME_FROM           110  '110'

 L. 356       124  LOAD_CONST               0
              126  LOAD_CONST               None
              128  IMPORT_NAME              string
              130  STORE_FAST               'string'

 L. 357       132  LOAD_FAST                'string'
              134  LOAD_ATTR                ascii_letters
              136  LOAD_FAST                'string'
              138  LOAD_ATTR                digits
              140  BINARY_ADD       
              142  LOAD_STR                 '_-'
              144  BINARY_ADD       
              146  STORE_FAST               'varchars'

 L. 358       148  LOAD_STR                 "'"
              150  STORE_FAST               'quote'

 L. 359       152  LOAD_STR                 '%'
              154  STORE_FAST               'percent'

 L. 360       156  LOAD_STR                 '{'
              158  STORE_FAST               'brace'

 L. 361       160  LOAD_STR                 '}'
              162  STORE_FAST               'rbrace'

 L. 362       164  LOAD_STR                 '$'
              166  STORE_FAST               'dollar'

 L. 363       168  LOAD_GLOBAL              os
              170  LOAD_ATTR                environ
              172  STORE_FAST               'environ'
            174_0  COME_FROM           102  '102'

 L. 364       174  LOAD_FAST                'path'
              176  LOAD_CONST               None
              178  LOAD_CONST               0
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  STORE_FAST               'res'

 L. 365       186  LOAD_CONST               0
              188  STORE_FAST               'index'

 L. 366       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'path'
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'pathlen'

 L. 367       198  LOAD_FAST                'index'
              200  LOAD_FAST                'pathlen'
              202  COMPARE_OP               <
          204_206  POP_JUMP_IF_FALSE  1070  'to 1070'

 L. 368       208  LOAD_FAST                'path'
              210  LOAD_FAST                'index'
              212  LOAD_FAST                'index'
              214  LOAD_CONST               1
              216  BINARY_ADD       
              218  BUILD_SLICE_2         2 
              220  BINARY_SUBSCR    
              222  STORE_FAST               'c'

 L. 369       224  LOAD_FAST                'c'
              226  LOAD_FAST                'quote'
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   344  'to 344'

 L. 370       234  LOAD_FAST                'path'
              236  LOAD_FAST                'index'
              238  LOAD_CONST               1
              240  BINARY_ADD       
              242  LOAD_CONST               None
              244  BUILD_SLICE_2         2 
              246  BINARY_SUBSCR    
              248  STORE_FAST               'path'

 L. 371       250  LOAD_GLOBAL              len
              252  LOAD_FAST                'path'
              254  CALL_FUNCTION_1       1  ''
              256  STORE_FAST               'pathlen'

 L. 372       258  SETUP_FINALLY       298  'to 298'

 L. 373       260  LOAD_FAST                'path'
              262  LOAD_METHOD              index
              264  LOAD_FAST                'c'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'index'

 L. 374       270  LOAD_FAST                'res'
              272  LOAD_FAST                'c'
              274  LOAD_FAST                'path'
              276  LOAD_CONST               None
              278  LOAD_FAST                'index'
              280  LOAD_CONST               1
              282  BINARY_ADD       
              284  BUILD_SLICE_2         2 
              286  BINARY_SUBSCR    
              288  BINARY_ADD       
              290  INPLACE_ADD      
              292  STORE_FAST               'res'
              294  POP_BLOCK        
              296  JUMP_FORWARD       1060  'to 1060'
            298_0  COME_FROM_FINALLY   258  '258'

 L. 375       298  DUP_TOP          
              300  LOAD_GLOBAL              ValueError
              302  COMPARE_OP               exception-match
          304_306  POP_JUMP_IF_FALSE   338  'to 338'
              308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 376       314  LOAD_FAST                'res'
              316  LOAD_FAST                'c'
              318  LOAD_FAST                'path'
              320  BINARY_ADD       
              322  INPLACE_ADD      
              324  STORE_FAST               'res'

 L. 377       326  LOAD_FAST                'pathlen'
              328  LOAD_CONST               1
              330  BINARY_SUBTRACT  
              332  STORE_FAST               'index'
              334  POP_EXCEPT       
              336  JUMP_FORWARD       1060  'to 1060'
            338_0  COME_FROM           304  '304'
              338  END_FINALLY      
          340_342  JUMP_FORWARD       1060  'to 1060'
            344_0  COME_FROM           230  '230'

 L. 378       344  LOAD_FAST                'c'
              346  LOAD_FAST                'percent'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   586  'to 586'

 L. 379       354  LOAD_FAST                'path'
              356  LOAD_FAST                'index'
              358  LOAD_CONST               1
              360  BINARY_ADD       
              362  LOAD_FAST                'index'
              364  LOAD_CONST               2
              366  BINARY_ADD       
              368  BUILD_SLICE_2         2 
              370  BINARY_SUBSCR    
              372  LOAD_FAST                'percent'
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   398  'to 398'

 L. 380       380  LOAD_FAST                'res'
              382  LOAD_FAST                'c'
              384  INPLACE_ADD      
              386  STORE_FAST               'res'

 L. 381       388  LOAD_FAST                'index'
              390  LOAD_CONST               1
              392  INPLACE_ADD      
              394  STORE_FAST               'index'
              396  JUMP_FORWARD       1060  'to 1060'
            398_0  COME_FROM           376  '376'

 L. 383       398  LOAD_FAST                'path'
              400  LOAD_FAST                'index'
              402  LOAD_CONST               1
              404  BINARY_ADD       
              406  LOAD_CONST               None
              408  BUILD_SLICE_2         2 
              410  BINARY_SUBSCR    
              412  STORE_FAST               'path'

 L. 384       414  LOAD_GLOBAL              len
              416  LOAD_FAST                'path'
              418  CALL_FUNCTION_1       1  ''
              420  STORE_FAST               'pathlen'

 L. 385       422  SETUP_FINALLY       438  'to 438'

 L. 386       424  LOAD_FAST                'path'
              426  LOAD_METHOD              index
              428  LOAD_FAST                'percent'
              430  CALL_METHOD_1         1  ''
              432  STORE_FAST               'index'
              434  POP_BLOCK        
              436  JUMP_FORWARD        480  'to 480'
            438_0  COME_FROM_FINALLY   422  '422'

 L. 387       438  DUP_TOP          
              440  LOAD_GLOBAL              ValueError
              442  COMPARE_OP               exception-match
          444_446  POP_JUMP_IF_FALSE   478  'to 478'
              448  POP_TOP          
              450  POP_TOP          
              452  POP_TOP          

 L. 388       454  LOAD_FAST                'res'
              456  LOAD_FAST                'percent'
              458  LOAD_FAST                'path'
              460  BINARY_ADD       
              462  INPLACE_ADD      
              464  STORE_FAST               'res'

 L. 389       466  LOAD_FAST                'pathlen'
              468  LOAD_CONST               1
              470  BINARY_SUBTRACT  
              472  STORE_FAST               'index'
              474  POP_EXCEPT       
              476  JUMP_FORWARD       1060  'to 1060'
            478_0  COME_FROM           444  '444'
              478  END_FINALLY      
            480_0  COME_FROM           436  '436'

 L. 391       480  LOAD_FAST                'path'
              482  LOAD_CONST               None
              484  LOAD_FAST                'index'
              486  BUILD_SLICE_2         2 
              488  BINARY_SUBSCR    
              490  STORE_FAST               'var'

 L. 392       492  SETUP_FINALLY       540  'to 540'

 L. 393       494  LOAD_FAST                'environ'
              496  LOAD_CONST               None
              498  COMPARE_OP               is
          500_502  POP_JUMP_IF_FALSE   528  'to 528'

 L. 394       504  LOAD_GLOBAL              os
              506  LOAD_METHOD              fsencode
              508  LOAD_GLOBAL              os
              510  LOAD_ATTR                environ
              512  LOAD_GLOBAL              os
              514  LOAD_METHOD              fsdecode
              516  LOAD_FAST                'var'
              518  CALL_METHOD_1         1  ''
              520  BINARY_SUBSCR    
              522  CALL_METHOD_1         1  ''
              524  STORE_FAST               'value'
              526  JUMP_FORWARD        536  'to 536'
            528_0  COME_FROM           500  '500'

 L. 396       528  LOAD_FAST                'environ'
              530  LOAD_FAST                'var'
              532  BINARY_SUBSCR    
              534  STORE_FAST               'value'
            536_0  COME_FROM           526  '526'
              536  POP_BLOCK        
              538  JUMP_FORWARD        574  'to 574'
            540_0  COME_FROM_FINALLY   492  '492'

 L. 397       540  DUP_TOP          
              542  LOAD_GLOBAL              KeyError
              544  COMPARE_OP               exception-match
          546_548  POP_JUMP_IF_FALSE   572  'to 572'
              550  POP_TOP          
              552  POP_TOP          
              554  POP_TOP          

 L. 398       556  LOAD_FAST                'percent'
              558  LOAD_FAST                'var'
              560  BINARY_ADD       
              562  LOAD_FAST                'percent'
              564  BINARY_ADD       
              566  STORE_FAST               'value'
              568  POP_EXCEPT       
              570  JUMP_FORWARD        574  'to 574'
            572_0  COME_FROM           546  '546'
              572  END_FINALLY      
            574_0  COME_FROM           570  '570'
            574_1  COME_FROM           538  '538'

 L. 399       574  LOAD_FAST                'res'
              576  LOAD_FAST                'value'
              578  INPLACE_ADD      
              580  STORE_FAST               'res'
          582_584  JUMP_FORWARD       1060  'to 1060'
            586_0  COME_FROM           350  '350'

 L. 400       586  LOAD_FAST                'c'
              588  LOAD_FAST                'dollar'
              590  COMPARE_OP               ==
          592_594  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 401       596  LOAD_FAST                'path'
              598  LOAD_FAST                'index'
              600  LOAD_CONST               1
              602  BINARY_ADD       
              604  LOAD_FAST                'index'
              606  LOAD_CONST               2
              608  BINARY_ADD       
              610  BUILD_SLICE_2         2 
              612  BINARY_SUBSCR    
              614  LOAD_FAST                'dollar'
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   642  'to 642'

 L. 402       622  LOAD_FAST                'res'
              624  LOAD_FAST                'c'
              626  INPLACE_ADD      
              628  STORE_FAST               'res'

 L. 403       630  LOAD_FAST                'index'
              632  LOAD_CONST               1
              634  INPLACE_ADD      
              636  STORE_FAST               'index'
          638_640  JUMP_ABSOLUTE      1060  'to 1060'
            642_0  COME_FROM           618  '618'

 L. 404       642  LOAD_FAST                'path'
              644  LOAD_FAST                'index'
              646  LOAD_CONST               1
              648  BINARY_ADD       
              650  LOAD_FAST                'index'
              652  LOAD_CONST               2
              654  BINARY_ADD       
              656  BUILD_SLICE_2         2 
              658  BINARY_SUBSCR    
              660  LOAD_FAST                'brace'
              662  COMPARE_OP               ==
          664_666  POP_JUMP_IF_FALSE   862  'to 862'

 L. 405       668  LOAD_FAST                'path'
              670  LOAD_FAST                'index'
              672  LOAD_CONST               2
              674  BINARY_ADD       
              676  LOAD_CONST               None
              678  BUILD_SLICE_2         2 
              680  BINARY_SUBSCR    
              682  STORE_FAST               'path'

 L. 406       684  LOAD_GLOBAL              len
              686  LOAD_FAST                'path'
              688  CALL_FUNCTION_1       1  ''
              690  STORE_FAST               'pathlen'

 L. 407       692  SETUP_FINALLY       708  'to 708'

 L. 408       694  LOAD_FAST                'path'
              696  LOAD_METHOD              index
              698  LOAD_FAST                'rbrace'
              700  CALL_METHOD_1         1  ''
              702  STORE_FAST               'index'
              704  POP_BLOCK        
              706  JUMP_FORWARD        754  'to 754'
            708_0  COME_FROM_FINALLY   692  '692'

 L. 409       708  DUP_TOP          
              710  LOAD_GLOBAL              ValueError
              712  COMPARE_OP               exception-match
          714_716  POP_JUMP_IF_FALSE   752  'to 752'
              718  POP_TOP          
              720  POP_TOP          
              722  POP_TOP          

 L. 410       724  LOAD_FAST                'res'
              726  LOAD_FAST                'dollar'
              728  LOAD_FAST                'brace'
              730  BINARY_ADD       
              732  LOAD_FAST                'path'
              734  BINARY_ADD       
              736  INPLACE_ADD      
              738  STORE_FAST               'res'

 L. 411       740  LOAD_FAST                'pathlen'
              742  LOAD_CONST               1
              744  BINARY_SUBTRACT  
              746  STORE_FAST               'index'
              748  POP_EXCEPT       
              750  JUMP_FORWARD        860  'to 860'
            752_0  COME_FROM           714  '714'
              752  END_FINALLY      
            754_0  COME_FROM           706  '706'

 L. 413       754  LOAD_FAST                'path'
              756  LOAD_CONST               None
              758  LOAD_FAST                'index'
              760  BUILD_SLICE_2         2 
              762  BINARY_SUBSCR    
              764  STORE_FAST               'var'

 L. 414       766  SETUP_FINALLY       814  'to 814'

 L. 415       768  LOAD_FAST                'environ'
              770  LOAD_CONST               None
              772  COMPARE_OP               is
          774_776  POP_JUMP_IF_FALSE   802  'to 802'

 L. 416       778  LOAD_GLOBAL              os
              780  LOAD_METHOD              fsencode
              782  LOAD_GLOBAL              os
              784  LOAD_ATTR                environ
              786  LOAD_GLOBAL              os
              788  LOAD_METHOD              fsdecode
              790  LOAD_FAST                'var'
              792  CALL_METHOD_1         1  ''
              794  BINARY_SUBSCR    
              796  CALL_METHOD_1         1  ''
              798  STORE_FAST               'value'
              800  JUMP_FORWARD        810  'to 810'
            802_0  COME_FROM           774  '774'

 L. 418       802  LOAD_FAST                'environ'
              804  LOAD_FAST                'var'
              806  BINARY_SUBSCR    
              808  STORE_FAST               'value'
            810_0  COME_FROM           800  '800'
              810  POP_BLOCK        
              812  JUMP_FORWARD        852  'to 852'
            814_0  COME_FROM_FINALLY   766  '766'

 L. 419       814  DUP_TOP          
              816  LOAD_GLOBAL              KeyError
              818  COMPARE_OP               exception-match
          820_822  POP_JUMP_IF_FALSE   850  'to 850'
              824  POP_TOP          
              826  POP_TOP          
              828  POP_TOP          

 L. 420       830  LOAD_FAST                'dollar'
              832  LOAD_FAST                'brace'
              834  BINARY_ADD       
              836  LOAD_FAST                'var'
              838  BINARY_ADD       
              840  LOAD_FAST                'rbrace'
              842  BINARY_ADD       
              844  STORE_FAST               'value'
              846  POP_EXCEPT       
              848  JUMP_FORWARD        852  'to 852'
            850_0  COME_FROM           820  '820'
              850  END_FINALLY      
            852_0  COME_FROM           848  '848'
            852_1  COME_FROM           812  '812'

 L. 421       852  LOAD_FAST                'res'
              854  LOAD_FAST                'value'
              856  INPLACE_ADD      
              858  STORE_FAST               'res'
            860_0  COME_FROM           750  '750'
              860  JUMP_FORWARD       1050  'to 1050'
            862_0  COME_FROM           664  '664'

 L. 423       862  LOAD_FAST                'path'
              864  LOAD_CONST               None
              866  LOAD_CONST               0
              868  BUILD_SLICE_2         2 
              870  BINARY_SUBSCR    
            872_0  COME_FROM           396  '396'
              872  STORE_FAST               'var'

 L. 424       874  LOAD_FAST                'index'
              876  LOAD_CONST               1
              878  INPLACE_ADD      
              880  STORE_FAST               'index'

 L. 425       882  LOAD_FAST                'path'
              884  LOAD_FAST                'index'
              886  LOAD_FAST                'index'
              888  LOAD_CONST               1
              890  BINARY_ADD       
              892  BUILD_SLICE_2         2 
              894  BINARY_SUBSCR    
              896  STORE_FAST               'c'

 L. 426       898  LOAD_FAST                'c'
          900_902  POP_JUMP_IF_FALSE   950  'to 950'
              904  LOAD_FAST                'c'
              906  LOAD_FAST                'varchars'
              908  COMPARE_OP               in
          910_912  POP_JUMP_IF_FALSE   950  'to 950'

 L. 427       914  LOAD_FAST                'var'
              916  LOAD_FAST                'c'
              918  INPLACE_ADD      
              920  STORE_FAST               'var'

 L. 428       922  LOAD_FAST                'index'
              924  LOAD_CONST               1
              926  INPLACE_ADD      
              928  STORE_FAST               'index'

 L. 429       930  LOAD_FAST                'path'
              932  LOAD_FAST                'index'
              934  LOAD_FAST                'index'
              936  LOAD_CONST               1
              938  BINARY_ADD       
              940  BUILD_SLICE_2         2 
              942  BINARY_SUBSCR    
              944  STORE_FAST               'c'
          946_948  JUMP_BACK           898  'to 898'
            950_0  COME_FROM           910  '910'
            950_1  COME_FROM           900  '900'

 L. 430       950  SETUP_FINALLY       998  'to 998'
            952_0  COME_FROM           476  '476'

 L. 431       952  LOAD_FAST                'environ'
              954  LOAD_CONST               None
              956  COMPARE_OP               is
          958_960  POP_JUMP_IF_FALSE   986  'to 986'

 L. 432       962  LOAD_GLOBAL              os
              964  LOAD_METHOD              fsencode
              966  LOAD_GLOBAL              os
              968  LOAD_ATTR                environ
              970  LOAD_GLOBAL              os
              972  LOAD_METHOD              fsdecode
              974  LOAD_FAST                'var'
              976  CALL_METHOD_1         1  ''
              978  BINARY_SUBSCR    
              980  CALL_METHOD_1         1  ''
              982  STORE_FAST               'value'
              984  JUMP_FORWARD        994  'to 994'
            986_0  COME_FROM           958  '958'

 L. 434       986  LOAD_FAST                'environ'
              988  LOAD_FAST                'var'
              990  BINARY_SUBSCR    
              992  STORE_FAST               'value'
            994_0  COME_FROM           984  '984'
              994  POP_BLOCK        
              996  JUMP_FORWARD       1028  'to 1028'
            998_0  COME_FROM_FINALLY   950  '950'

 L. 435       998  DUP_TOP          
             1000  LOAD_GLOBAL              KeyError
             1002  COMPARE_OP               exception-match
         1004_1006  POP_JUMP_IF_FALSE  1026  'to 1026'
             1008  POP_TOP          
             1010  POP_TOP          
             1012  POP_TOP          
           1014_0  COME_FROM           296  '296'

 L. 436      1014  LOAD_FAST                'dollar'
             1016  LOAD_FAST                'var'
             1018  BINARY_ADD       
             1020  STORE_FAST               'value'
             1022  POP_EXCEPT       
             1024  JUMP_FORWARD       1028  'to 1028'
           1026_0  COME_FROM          1004  '1004'
             1026  END_FINALLY      
           1028_0  COME_FROM          1024  '1024'
           1028_1  COME_FROM           996  '996'

 L. 437      1028  LOAD_FAST                'res'
             1030  LOAD_FAST                'value'
             1032  INPLACE_ADD      
             1034  STORE_FAST               'res'

 L. 438      1036  LOAD_FAST                'c'
         1038_1040  POP_JUMP_IF_FALSE  1060  'to 1060'

 L. 439      1042  LOAD_FAST                'index'
             1044  LOAD_CONST               1
             1046  INPLACE_SUBTRACT 
             1048  STORE_FAST               'index'
           1050_0  COME_FROM           860  '860'
             1050  JUMP_FORWARD       1060  'to 1060'
           1052_0  COME_FROM           592  '592'

 L. 441      1052  LOAD_FAST                'res'
           1054_0  COME_FROM           336  '336'
             1054  LOAD_FAST                'c'
             1056  INPLACE_ADD      
             1058  STORE_FAST               'res'
           1060_0  COME_FROM          1050  '1050'
           1060_1  COME_FROM          1038  '1038'
           1060_2  COME_FROM           582  '582'
           1060_3  COME_FROM           340  '340'

 L. 442      1060  LOAD_FAST                'index'
             1062  LOAD_CONST               1
             1064  INPLACE_ADD      
             1066  STORE_FAST               'index'
             1068  JUMP_BACK           198  'to 198'
           1070_0  COME_FROM           204  '204'

 L. 443      1070  LOAD_FAST                'res'
             1072  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 872_0


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
        else:
            path = path.replace(altsep, sep)
            prefix, path = splitdrive(path)
            if path.startswith(sep):
                prefix += sep
                path = path.lstrip(sep)
            comps = path.split(sep)
            i = 0
            while True:
                while i < len(comps):
                    if not comps[i] or comps[i] == curdir:
                        del comps[i]

                if comps[i] == pardir:
                    if i > 0 and comps[(i - 1)] != pardir:
                        del comps[i - 1:i + 1]
                        i -= 1
                    else:
                        if i == 0 and prefix.endswith(sep):
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

        def abspath--- This code section failed: ---

 L. 526         0  SETUP_FINALLY        16  'to 16'

 L. 527         2  LOAD_GLOBAL              normpath
                4  LOAD_GLOBAL              _getfullpathname
                6  LOAD_FAST                'path'
                8  CALL_FUNCTION_1       1  ''
               10  CALL_FUNCTION_1       1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 528        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  LOAD_GLOBAL              ValueError
               22  BUILD_TUPLE_2         2 
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    46  'to 46'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 529        34  LOAD_GLOBAL              _abspath_fallback
               36  LOAD_FAST                'path'
               38  CALL_FUNCTION_1       1  ''
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
             46_0  COME_FROM            26  '26'
               46  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30


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
              128  BREAK_LOOP          174  'to 174'
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
            174_0  COME_FROM_EXCEPT_CLAUSE   164  '164'
            174_1  COME_FROM_EXCEPT_CLAUSE    20  '20'

 L. 577       174  LOAD_FAST                'path'
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 124


        def _getfinalpathname_nonstrict--- This code section failed: ---

 L. 594         0  LOAD_CONST               (1, 2, 3, 5, 21, 32, 50, 67, 87, 123, 1920, 1921)
                2  STORE_FAST               'allowed_winerror'

 L. 598         4  LOAD_STR                 ''
                6  STORE_FAST               'tail'

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
              136  JUMP_FORWARD        140  'to 140'
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

                return path


    supports_unicode_filenames = hasattr(sys, 'getwindowsversion') and sys.getwindowsversion()[3] >= 2

    def relpath--- This code section failed: ---

 L. 680         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              fspath
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'path'

 L. 681        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'path'
               14  LOAD_GLOBAL              bytes
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 682        20  LOAD_CONST               b'\\'
               22  STORE_FAST               'sep'

 L. 683        24  LOAD_CONST               b'.'
               26  STORE_FAST               'curdir'

 L. 684        28  LOAD_CONST               b'..'
               30  STORE_FAST               'pardir'
               32  JUMP_FORWARD         46  'to 46'
             34_0  COME_FROM            18  '18'

 L. 686        34  LOAD_STR                 '\\'
               36  STORE_FAST               'sep'

 L. 687        38  LOAD_STR                 '.'
               40  STORE_FAST               'curdir'

 L. 688        42  LOAD_STR                 '..'
               44  STORE_FAST               'pardir'
             46_0  COME_FROM            32  '32'

 L. 690        46  LOAD_FAST                'start'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 691        54  LOAD_FAST                'curdir'
               56  STORE_FAST               'start'
             58_0  COME_FROM            52  '52'

 L. 693        58  LOAD_FAST                'path'
               60  POP_JUMP_IF_TRUE     70  'to 70'

 L. 694        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'no path specified'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 696        70  LOAD_GLOBAL              os
               72  LOAD_METHOD              fspath
               74  LOAD_FAST                'start'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'start'

 L. 697        80  SETUP_FINALLY       306  'to 306'

 L. 698        82  LOAD_GLOBAL              abspath
               84  LOAD_GLOBAL              normpath
               86  LOAD_FAST                'start'
               88  CALL_FUNCTION_1       1  ''
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'start_abs'

 L. 699        94  LOAD_GLOBAL              abspath
               96  LOAD_GLOBAL              normpath
               98  LOAD_FAST                'path'
              100  CALL_FUNCTION_1       1  ''
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'path_abs'

 L. 700       106  LOAD_GLOBAL              splitdrive
              108  LOAD_FAST                'start_abs'
              110  CALL_FUNCTION_1       1  ''
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'start_drive'
              116  STORE_FAST               'start_rest'

 L. 701       118  LOAD_GLOBAL              splitdrive
              120  LOAD_FAST                'path_abs'
              122  CALL_FUNCTION_1       1  ''
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'path_drive'
              128  STORE_FAST               'path_rest'

 L. 702       130  LOAD_GLOBAL              normcase
              132  LOAD_FAST                'start_drive'
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_GLOBAL              normcase
              138  LOAD_FAST                'path_drive'
              140  CALL_FUNCTION_1       1  ''
              142  COMPARE_OP               !=
              144  POP_JUMP_IF_FALSE   162  'to 162'

 L. 703       146  LOAD_GLOBAL              ValueError
              148  LOAD_STR                 'path is on mount %r, start on mount %r'

 L. 704       150  LOAD_FAST                'path_drive'

 L. 704       152  LOAD_FAST                'start_drive'

 L. 703       154  BUILD_TUPLE_2         2 
              156  BINARY_MODULO    
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           144  '144'

 L. 706       162  LOAD_LISTCOMP            '<code_object <listcomp>>'
              164  LOAD_STR                 'relpath.<locals>.<listcomp>'
              166  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              168  LOAD_FAST                'start_rest'
              170  LOAD_METHOD              split
              172  LOAD_FAST                'sep'
              174  CALL_METHOD_1         1  ''
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'start_list'

 L. 707       182  LOAD_LISTCOMP            '<code_object <listcomp>>'
              184  LOAD_STR                 'relpath.<locals>.<listcomp>'
              186  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              188  LOAD_FAST                'path_rest'
              190  LOAD_METHOD              split
              192  LOAD_FAST                'sep'
              194  CALL_METHOD_1         1  ''
              196  GET_ITER         
              198  CALL_FUNCTION_1       1  ''
              200  STORE_FAST               'path_list'

 L. 709       202  LOAD_CONST               0
              204  STORE_FAST               'i'

 L. 710       206  LOAD_GLOBAL              zip
              208  LOAD_FAST                'start_list'
              210  LOAD_FAST                'path_list'
              212  CALL_FUNCTION_2       2  ''
              214  GET_ITER         
              216  FOR_ITER            254  'to 254'
              218  UNPACK_SEQUENCE_2     2 
              220  STORE_FAST               'e1'
              222  STORE_FAST               'e2'

 L. 711       224  LOAD_GLOBAL              normcase
              226  LOAD_FAST                'e1'
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_GLOBAL              normcase
              232  LOAD_FAST                'e2'
              234  CALL_FUNCTION_1       1  ''
              236  COMPARE_OP               !=
              238  POP_JUMP_IF_FALSE   244  'to 244'

 L. 712       240  POP_TOP          
              242  BREAK_LOOP          254  'to 254'
            244_0  COME_FROM           238  '238'

 L. 713       244  LOAD_FAST                'i'
              246  LOAD_CONST               1
              248  INPLACE_ADD      
              250  STORE_FAST               'i'
              252  JUMP_BACK           216  'to 216'

 L. 715       254  LOAD_FAST                'pardir'
              256  BUILD_LIST_1          1 
              258  LOAD_GLOBAL              len
              260  LOAD_FAST                'start_list'
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_FAST                'i'
              266  BINARY_SUBTRACT  
              268  BINARY_MULTIPLY  
              270  LOAD_FAST                'path_list'
              272  LOAD_FAST                'i'
              274  LOAD_CONST               None
              276  BUILD_SLICE_2         2 
              278  BINARY_SUBSCR    
              280  BINARY_ADD       
              282  STORE_FAST               'rel_list'

 L. 716       284  LOAD_FAST                'rel_list'
          286_288  POP_JUMP_IF_TRUE    296  'to 296'

 L. 717       290  LOAD_FAST                'curdir'
              292  POP_BLOCK        
              294  RETURN_VALUE     
            296_0  COME_FROM           286  '286'

 L. 718       296  LOAD_GLOBAL              join
              298  LOAD_FAST                'rel_list'
              300  CALL_FUNCTION_EX      0  'positional arguments only'
              302  POP_BLOCK        
              304  RETURN_VALUE     
            306_0  COME_FROM_FINALLY    80  '80'

 L. 719       306  DUP_TOP          
              308  LOAD_GLOBAL              TypeError
              310  LOAD_GLOBAL              ValueError
              312  LOAD_GLOBAL              AttributeError
              314  LOAD_GLOBAL              BytesWarning
              316  LOAD_GLOBAL              DeprecationWarning
              318  BUILD_TUPLE_5         5 
              320  COMPARE_OP               exception-match
          322_324  POP_JUMP_IF_FALSE   352  'to 352'
              326  POP_TOP          
              328  POP_TOP          
              330  POP_TOP          

 L. 720       332  LOAD_GLOBAL              genericpath
              334  LOAD_METHOD              _check_arg_types
              336  LOAD_STR                 'relpath'
              338  LOAD_FAST                'path'
              340  LOAD_FAST                'start'
              342  CALL_METHOD_3         3  ''
              344  POP_TOP          

 L. 721       346  RAISE_VARARGS_0       0  'reraise'
              348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           322  '322'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'

Parse error at or near `POP_TOP' instruction at offset 328


    def commonpath--- This code section failed: ---

 L. 737         0  LOAD_FAST                'paths'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 738         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'commonpath() arg is an empty sequence'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 740        12  LOAD_GLOBAL              tuple
               14  LOAD_GLOBAL              map
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                fspath
               20  LOAD_FAST                'paths'
               22  CALL_FUNCTION_2       2  ''
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'paths'

 L. 741        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'paths'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_GLOBAL              bytes
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    56  'to 56'

 L. 742        42  LOAD_CONST               b'\\'
               44  STORE_DEREF              'sep'

 L. 743        46  LOAD_CONST               b'/'
               48  STORE_DEREF              'altsep'

 L. 744        50  LOAD_CONST               b'.'
               52  STORE_DEREF              'curdir'
               54  JUMP_FORWARD         68  'to 68'
             56_0  COME_FROM            40  '40'

 L. 746        56  LOAD_STR                 '\\'
               58  STORE_DEREF              'sep'

 L. 747        60  LOAD_STR                 '/'
               62  STORE_DEREF              'altsep'

 L. 748        64  LOAD_STR                 '.'
               66  STORE_DEREF              'curdir'
             68_0  COME_FROM            54  '54'

 L. 750     68_70  SETUP_FINALLY       392  'to 392'

 L. 751        72  LOAD_CLOSURE             'altsep'
               74  LOAD_CLOSURE             'sep'
               76  BUILD_TUPLE_2         2 
               78  LOAD_LISTCOMP            '<code_object <listcomp>>'
               80  LOAD_STR                 'commonpath.<locals>.<listcomp>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_FAST                'paths'
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'drivesplits'

 L. 752        92  LOAD_CLOSURE             'sep'
               94  BUILD_TUPLE_1         1 
               96  LOAD_LISTCOMP            '<code_object <listcomp>>'
               98  LOAD_STR                 'commonpath.<locals>.<listcomp>'
              100  MAKE_FUNCTION_8          'closure'
              102  LOAD_FAST                'drivesplits'
              104  GET_ITER         
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'split_paths'

 L. 754       110  SETUP_FINALLY       140  'to 140'

 L. 755       112  LOAD_GLOBAL              set
              114  LOAD_CLOSURE             'sep'
              116  BUILD_TUPLE_1         1 
              118  LOAD_GENEXPR             '<code_object <genexpr>>'
              120  LOAD_STR                 'commonpath.<locals>.<genexpr>'
              122  MAKE_FUNCTION_8          'closure'
              124  LOAD_FAST                'drivesplits'
              126  GET_ITER         
              128  CALL_FUNCTION_1       1  ''
              130  CALL_FUNCTION_1       1  ''
              132  UNPACK_SEQUENCE_1     1 
              134  STORE_FAST               'isabs'
              136  POP_BLOCK        
              138  JUMP_FORWARD        170  'to 170'
            140_0  COME_FROM_FINALLY   110  '110'

 L. 756       140  DUP_TOP          
              142  LOAD_GLOBAL              ValueError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   168  'to 168'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 757       154  LOAD_GLOBAL              ValueError
              156  LOAD_STR                 "Can't mix absolute and relative paths"
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_CONST               None
              162  RAISE_VARARGS_2       2  'exception instance with __cause__'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           146  '146'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           138  '138'

 L. 762       170  LOAD_GLOBAL              len
              172  LOAD_GLOBAL              set
              174  LOAD_GENEXPR             '<code_object <genexpr>>'
              176  LOAD_STR                 'commonpath.<locals>.<genexpr>'
              178  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              180  LOAD_FAST                'drivesplits'
              182  GET_ITER         
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_CONST               1
              192  COMPARE_OP               !=
              194  POP_JUMP_IF_FALSE   204  'to 204'

 L. 763       196  LOAD_GLOBAL              ValueError
              198  LOAD_STR                 "Paths don't have the same drive"
              200  CALL_FUNCTION_1       1  ''
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           194  '194'

 L. 765       204  LOAD_GLOBAL              splitdrive
              206  LOAD_FAST                'paths'
              208  LOAD_CONST               0
              210  BINARY_SUBSCR    
              212  LOAD_METHOD              replace
              214  LOAD_DEREF               'altsep'
              216  LOAD_DEREF               'sep'
              218  CALL_METHOD_2         2  ''
              220  CALL_FUNCTION_1       1  ''
              222  UNPACK_SEQUENCE_2     2 
              224  STORE_FAST               'drive'
              226  STORE_FAST               'path'

 L. 766       228  LOAD_FAST                'path'
              230  LOAD_METHOD              split
              232  LOAD_DEREF               'sep'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'common'

 L. 767       238  LOAD_CLOSURE             'curdir'
              240  BUILD_TUPLE_1         1 
              242  LOAD_LISTCOMP            '<code_object <listcomp>>'
              244  LOAD_STR                 'commonpath.<locals>.<listcomp>'
              246  MAKE_FUNCTION_8          'closure'
              248  LOAD_FAST                'common'
              250  GET_ITER         
              252  CALL_FUNCTION_1       1  ''
              254  STORE_FAST               'common'

 L. 769       256  LOAD_CLOSURE             'curdir'
              258  BUILD_TUPLE_1         1 
              260  LOAD_LISTCOMP            '<code_object <listcomp>>'
              262  LOAD_STR                 'commonpath.<locals>.<listcomp>'
              264  MAKE_FUNCTION_8          'closure'
              266  LOAD_FAST                'split_paths'
              268  GET_ITER         
              270  CALL_FUNCTION_1       1  ''
              272  STORE_FAST               'split_paths'

 L. 770       274  LOAD_GLOBAL              min
              276  LOAD_FAST                'split_paths'
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               's1'

 L. 771       282  LOAD_GLOBAL              max
              284  LOAD_FAST                'split_paths'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               's2'

 L. 772       290  LOAD_GLOBAL              enumerate
              292  LOAD_FAST                's1'
              294  CALL_FUNCTION_1       1  ''
              296  GET_ITER         
            298_0  COME_FROM           316  '316'
              298  FOR_ITER            342  'to 342'
              300  UNPACK_SEQUENCE_2     2 
              302  STORE_FAST               'i'
              304  STORE_FAST               'c'

 L. 773       306  LOAD_FAST                'c'
              308  LOAD_FAST                's2'
              310  LOAD_FAST                'i'
              312  BINARY_SUBSCR    
              314  COMPARE_OP               !=
          316_318  POP_JUMP_IF_FALSE   298  'to 298'

 L. 774       320  LOAD_FAST                'common'
              322  LOAD_CONST               None
              324  LOAD_FAST                'i'
              326  BUILD_SLICE_2         2 
              328  BINARY_SUBSCR    
              330  STORE_FAST               'common'

 L. 775       332  POP_TOP          
          334_336  BREAK_LOOP          358  'to 358'
          338_340  JUMP_BACK           298  'to 298'

 L. 777       342  LOAD_FAST                'common'
              344  LOAD_CONST               None
              346  LOAD_GLOBAL              len
              348  LOAD_FAST                's1'
              350  CALL_FUNCTION_1       1  ''
              352  BUILD_SLICE_2         2 
              354  BINARY_SUBSCR    
              356  STORE_FAST               'common'

 L. 779       358  LOAD_FAST                'isabs'
          360_362  POP_JUMP_IF_FALSE   372  'to 372'
              364  LOAD_FAST                'drive'
              366  LOAD_DEREF               'sep'
              368  BINARY_ADD       
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           360  '360'
              372  LOAD_FAST                'drive'
            374_0  COME_FROM           370  '370'
              374  STORE_FAST               'prefix'

 L. 780       376  LOAD_FAST                'prefix'
              378  LOAD_DEREF               'sep'
              380  LOAD_METHOD              join
              382  LOAD_FAST                'common'
              384  CALL_METHOD_1         1  ''
              386  BINARY_ADD       
              388  POP_BLOCK        
              390  RETURN_VALUE     
            392_0  COME_FROM_FINALLY    68  '68'

 L. 781       392  DUP_TOP          
              394  LOAD_GLOBAL              TypeError
              396  LOAD_GLOBAL              AttributeError
              398  BUILD_TUPLE_2         2 
              400  COMPARE_OP               exception-match
          402_404  POP_JUMP_IF_FALSE   432  'to 432'
              406  POP_TOP          
              408  POP_TOP          
              410  POP_TOP          

 L. 782       412  LOAD_GLOBAL              genericpath
              414  LOAD_ATTR                _check_arg_types
              416  LOAD_CONST               ('commonpath',)
              418  LOAD_FAST                'paths'
              420  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              422  CALL_FUNCTION_EX      0  'positional arguments only'
              424  POP_TOP          

 L. 783       426  RAISE_VARARGS_0       0  'reraise'
              428  POP_EXCEPT       
              430  JUMP_FORWARD        434  'to 434'
            432_0  COME_FROM           402  '402'
              432  END_FINALLY      
            434_0  COME_FROM           430  '430'

Parse error at or near `POP_TOP' instruction at offset 408


try:
    from nt import _isdir as isdir
except ImportError:
    pass