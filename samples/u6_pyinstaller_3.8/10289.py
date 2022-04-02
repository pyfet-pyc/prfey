# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: os.py
r"""OS routines for NT or Posix depending on what system we're on.

This exports:
  - all functions from posix or nt, e.g. unlink, stat, etc.
  - os.path is either posixpath or ntpath
  - os.name is either 'posix' or 'nt'
  - os.curdir is a string representing the current directory (always '.')
  - os.pardir is a string representing the parent directory (always '..')
  - os.sep is the (or a most common) pathname separator ('/' or '\\')
  - os.extsep is the extension separator (always '.')
  - os.altsep is the alternate pathname separator (None or '/')
  - os.pathsep is the component separator used in $PATH etc
  - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
  - os.defpath is the default search path for executables
  - os.devnull is the file path of the null device ('/dev/null', etc.)

Programs that import and use 'os' stand a better chance of being
portable between different platforms.  Of course, they must then
only use functions that are defined by all platforms (e.g., unlink
and opendir), and leave all pathname manipulation to os.path
(e.g., split and join).
"""
import abc, sys, stat as st
from _collections_abc import _check_methods
_names = sys.builtin_module_names
__all__ = [
 'altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep',
 'defpath', 'name', 'path', 'devnull', 'SEEK_SET', 'SEEK_CUR',
 'SEEK_END', 'fsencode', 'fsdecode', 'get_exec_path', 'fdopen',
 'popen', 'extsep']

def _exists(name):
    return name in globals()


def _get_exports_list--- This code section failed: ---

 L.  43         0  SETUP_FINALLY        14  'to 14'

 L.  44         2  LOAD_GLOBAL              list
                4  LOAD_FAST                'module'
                6  LOAD_ATTR                __all__
                8  CALL_FUNCTION_1       1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  45        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    50  'to 50'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  46        28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 '_get_exports_list.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_GLOBAL              dir
               36  LOAD_FAST                'module'
               38  CALL_FUNCTION_1       1  ''
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
             50_0  COME_FROM            20  '20'
               50  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    from posix import *
    try:
        from posix import _exit
        __all__.append('_exit')
    except ImportError:
        pass
    else:
        import posixpath as path
        try:
            from posix import _have_functions
        except ImportError:
            pass
        else:
            import posix
            __all__.extend(_get_exports_list(posix))
            del posix
else:
    if 'nt' in _names:
        name = 'nt'
        linesep = '\r\n'
        from nt import *
        try:
            from nt import _exit
            __all__.append('_exit')
        except ImportError:
            pass
        else:
            import ntpath as path, nt
            __all__.extend(_get_exports_list(nt))
            del nt
        try:
            from nt import _have_functions
        except ImportError:
            pass

    else:
        raise ImportError('no os specific module found')
sys.modules['os.path'] = path
from os.path import curdir, pardir, sep, pathsep, defpath, extsep, altsep, devnull
del _names
if _exists('_have_functions'):
    _globals = globals()

    def _add(str, fn):
        if fn in _globals:
            if str in _have_functions:
                _set.add(_globals[fn])


    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHMODAT', 'chmod')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_FUTIMESAT', 'utime')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_MKDIRAT', 'mkdir')
    _add('HAVE_MKFIFOAT', 'mkfifo')
    _add('HAVE_MKNODAT', 'mknod')
    _add('HAVE_OPENAT', 'open')
    _add('HAVE_READLINKAT', 'readlink')
    _add('HAVE_RENAMEAT', 'rename')
    _add('HAVE_SYMLINKAT', 'symlink')
    _add('HAVE_UNLINKAT', 'unlink')
    _add('HAVE_UNLINKAT', 'rmdir')
    _add('HAVE_UTIMENSAT', 'utime')
    supports_dir_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    supports_effective_ids = _set
    _set = set()
    _add('HAVE_FCHDIR', 'chdir')
    _add('HAVE_FCHMOD', 'chmod')
    _add('HAVE_FCHOWN', 'chown')
    _add('HAVE_FDOPENDIR', 'listdir')
    _add('HAVE_FDOPENDIR', 'scandir')
    _add('HAVE_FEXECVE', 'execve')
    _set.add(stat)
    _add('HAVE_FTRUNCATE', 'truncate')
    _add('HAVE_FUTIMENS', 'utime')
    _add('HAVE_FUTIMES', 'utime')
    _add('HAVE_FPATHCONF', 'pathconf')
    if _exists('statvfs'):
        if _exists('fstatvfs'):
            _add('HAVE_FSTATVFS', 'statvfs')
    supports_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_LCHFLAGS', 'chflags')
    _add('HAVE_LCHMOD', 'chmod')
    if _exists('lchown'):
        _add('HAVE_LCHOWN', 'chown')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_LUTIMES', 'utime')
    _add('HAVE_LSTAT', 'stat')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_UTIMENSAT', 'utime')
    _add('MS_WINDOWS', 'stat')
    supports_follow_symlinks = _set
    del _set
    del _have_functions
    del _globals
    del _add
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def makedirs(name, mode=511, exist_ok=False):
    """makedirs(name [, mode=0o777][, exist_ok=False])

    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.

    """
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    elif head and tail:
        if not path.exists(head):
            try:
                makedirs(head, exist_ok=exist_ok)
            except FileExistsError:
                pass
            else:
                cdir = curdir
                if isinstance(tail, bytes):
                    cdir = bytes(curdir, 'ASCII')
            if tail == cdir:
                return
    try:
        mkdir(name, mode)
    except OSError:
        if not (exist_ok and path.isdir(name)):
            raise


def removedirs--- This code section failed: ---

 L. 241         0  LOAD_GLOBAL              rmdir
                2  LOAD_FAST                'name'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 242         8  LOAD_GLOBAL              path
               10  LOAD_METHOD              split
               12  LOAD_FAST                'name'
               14  CALL_METHOD_1         1  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'head'
               20  STORE_FAST               'tail'

 L. 243        22  LOAD_FAST                'tail'
               24  POP_JUMP_IF_TRUE     40  'to 40'

 L. 244        26  LOAD_GLOBAL              path
               28  LOAD_METHOD              split
               30  LOAD_FAST                'head'
               32  CALL_METHOD_1         1  ''
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'head'
               38  STORE_FAST               'tail'
             40_0  COME_FROM            24  '24'

 L. 245        40  LOAD_FAST                'head'
               42  POP_JUMP_IF_FALSE   102  'to 102'
               44  LOAD_FAST                'tail'
               46  POP_JUMP_IF_FALSE   102  'to 102'

 L. 246        48  SETUP_FINALLY        62  'to 62'

 L. 247        50  LOAD_GLOBAL              rmdir
               52  LOAD_FAST                'head'
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          
               58  POP_BLOCK        
               60  JUMP_FORWARD         86  'to 86'
             62_0  COME_FROM_FINALLY    48  '48'

 L. 248        62  DUP_TOP          
               64  LOAD_GLOBAL              OSError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    84  'to 84'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 249        76  POP_EXCEPT       
               78  BREAK_LOOP          102  'to 102'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            68  '68'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            60  '60'

 L. 250        86  LOAD_GLOBAL              path
               88  LOAD_METHOD              split
               90  LOAD_FAST                'head'
               92  CALL_METHOD_1         1  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'head'
               98  STORE_FAST               'tail'
              100  JUMP_BACK            40  'to 40'
            102_0  COME_FROM_EXCEPT_CLAUSE    78  '78'
            102_1  COME_FROM_EXCEPT_CLAUSE    46  '46'
            102_2  COME_FROM_EXCEPT_CLAUSE    42  '42'

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 102_1


def renames(old, new):
    """renames(old, new)

    Super-rename; create directories as necessary and delete any left
    empty.  Works like rename, except creation of any intermediate
    directories needed to make the new pathname good is attempted
    first.  After the rename, directories corresponding to rightmost
    path segments of the old name will be pruned until either the
    whole path is consumed or a nonempty directory is found.

    Note: this function can fail with the new directory structure made
    if you lack permissions needed to unlink the leaf directory or
    file.

    """
    head, tail = path.split(new)
    if head:
        if tail:
            if not path.exists(head):
                makedirs(head)
    rename(old, new)
    head, tail = path.split(old)
    if head:
        if tail:
            try:
                removedirs(head)
            except OSError:
                pass


__all__.extend(['makedirs', 'removedirs', 'renames'])

def walk--- This code section failed: ---

 L. 339         0  LOAD_GLOBAL              fspath
                2  LOAD_FAST                'top'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'top'

 L. 340         8  BUILD_LIST_0          0 
               10  STORE_FAST               'dirs'

 L. 341        12  BUILD_LIST_0          0 
               14  STORE_FAST               'nondirs'

 L. 342        16  BUILD_LIST_0          0 
               18  STORE_FAST               'walk_dirs'

 L. 349        20  SETUP_FINALLY        34  'to 34'

 L. 352        22  LOAD_GLOBAL              scandir
               24  LOAD_FAST                'top'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'scandir_it'
               30  POP_BLOCK        
               32  JUMP_FORWARD         90  'to 90'
             34_0  COME_FROM_FINALLY    20  '20'

 L. 353        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    88  'to 88'
               42  POP_TOP          
               44  STORE_FAST               'error'
               46  POP_TOP          
               48  SETUP_FINALLY        76  'to 76'

 L. 354        50  LOAD_FAST                'onerror'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 355        58  LOAD_FAST                'onerror'
               60  LOAD_FAST                'error'
               62  CALL_FUNCTION_1       1  ''
               64  POP_TOP          
             66_0  COME_FROM            56  '56'

 L. 356        66  POP_BLOCK        
               68  POP_EXCEPT       
               70  CALL_FINALLY         76  'to 76'
               72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM_FINALLY    48  '48'
               76  LOAD_CONST               None
               78  STORE_FAST               'error'
               80  DELETE_FAST              'error'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            40  '40'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            32  '32'

 L. 358        90  LOAD_FAST                'scandir_it'
            92_94  SETUP_WITH          372  'to 372'
               96  POP_TOP          
             98_0  COME_FROM           352  '352'
             98_1  COME_FROM           290  '290'
             98_2  COME_FROM           286  '286'

 L. 360        98  SETUP_FINALLY       146  'to 146'

 L. 361       100  SETUP_FINALLY       114  'to 114'

 L. 362       102  LOAD_GLOBAL              next
              104  LOAD_FAST                'scandir_it'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'entry'
              110  POP_BLOCK        
              112  JUMP_FORWARD        142  'to 142'
            114_0  COME_FROM_FINALLY   100  '100'

 L. 363       114  DUP_TOP          
              116  LOAD_GLOBAL              StopIteration
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   140  'to 140'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 364       128  POP_EXCEPT       
              130  POP_BLOCK        
          132_134  BREAK_LOOP          368  'to 368'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           120  '120'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           112  '112'
              142  POP_BLOCK        
              144  JUMP_FORWARD        212  'to 212'
            146_0  COME_FROM_FINALLY    98  '98'

 L. 365       146  DUP_TOP          
              148  LOAD_GLOBAL              OSError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   210  'to 210'
              154  POP_TOP          
              156  STORE_FAST               'error'
              158  POP_TOP          
              160  SETUP_FINALLY       198  'to 198'

 L. 366       162  LOAD_FAST                'onerror'
              164  LOAD_CONST               None
              166  COMPARE_OP               is-not
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L. 367       170  LOAD_FAST                'onerror'
              172  LOAD_FAST                'error'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
            178_0  COME_FROM           168  '168'

 L. 368       178  POP_BLOCK        
              180  POP_EXCEPT       
              182  CALL_FINALLY        198  'to 198'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
              188  WITH_CLEANUP_START
              190  WITH_CLEANUP_FINISH
              192  POP_FINALLY           0  ''
              194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           182  '182'
            198_1  COME_FROM_FINALLY   160  '160'
              198  LOAD_CONST               None
              200  STORE_FAST               'error'
              202  DELETE_FAST              'error'
              204  END_FINALLY      
              206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
            210_0  COME_FROM           152  '152'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           144  '144'

 L. 370       212  SETUP_FINALLY       226  'to 226'

 L. 371       214  LOAD_FAST                'entry'
              216  LOAD_METHOD              is_dir
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'is_dir'
              222  POP_BLOCK        
              224  JUMP_FORWARD        252  'to 252'
            226_0  COME_FROM_FINALLY   212  '212'

 L. 372       226  DUP_TOP          
              228  LOAD_GLOBAL              OSError
              230  COMPARE_OP               exception-match
          232_234  POP_JUMP_IF_FALSE   250  'to 250'
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          

 L. 375       242  LOAD_CONST               False
              244  STORE_FAST               'is_dir'
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           232  '232'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           224  '224'

 L. 377       252  LOAD_FAST                'is_dir'
          254_256  POP_JUMP_IF_FALSE   272  'to 272'

 L. 378       258  LOAD_FAST                'dirs'
              260  LOAD_METHOD              append
              262  LOAD_FAST                'entry'
              264  LOAD_ATTR                name
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  JUMP_FORWARD        284  'to 284'
            272_0  COME_FROM           254  '254'

 L. 380       272  LOAD_FAST                'nondirs'
              274  LOAD_METHOD              append
              276  LOAD_FAST                'entry'
              278  LOAD_ATTR                name
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          
            284_0  COME_FROM           270  '270'

 L. 382       284  LOAD_FAST                'topdown'
              286  POP_JUMP_IF_TRUE     98  'to 98'
              288  LOAD_FAST                'is_dir'
              290  POP_JUMP_IF_FALSE    98  'to 98'

 L. 385       292  LOAD_FAST                'followlinks'
          294_296  POP_JUMP_IF_FALSE   304  'to 304'

 L. 386       298  LOAD_CONST               True
              300  STORE_FAST               'walk_into'
              302  JUMP_FORWARD        350  'to 350'
            304_0  COME_FROM           294  '294'

 L. 388       304  SETUP_FINALLY       318  'to 318'

 L. 389       306  LOAD_FAST                'entry'
              308  LOAD_METHOD              is_symlink
              310  CALL_METHOD_0         0  ''
              312  STORE_FAST               'is_symlink'
              314  POP_BLOCK        
              316  JUMP_FORWARD        344  'to 344'
            318_0  COME_FROM_FINALLY   304  '304'

 L. 390       318  DUP_TOP          
              320  LOAD_GLOBAL              OSError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   342  'to 342'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 394       334  LOAD_CONST               False
              336  STORE_FAST               'is_symlink'
              338  POP_EXCEPT       
              340  JUMP_FORWARD        344  'to 344'
            342_0  COME_FROM           324  '324'
              342  END_FINALLY      
            344_0  COME_FROM           340  '340'
            344_1  COME_FROM           316  '316'

 L. 395       344  LOAD_FAST                'is_symlink'
              346  UNARY_NOT        
              348  STORE_FAST               'walk_into'
            350_0  COME_FROM           302  '302'

 L. 397       350  LOAD_FAST                'walk_into'
              352  POP_JUMP_IF_FALSE    98  'to 98'

 L. 398       354  LOAD_FAST                'walk_dirs'
              356  LOAD_METHOD              append
              358  LOAD_FAST                'entry'
              360  LOAD_ATTR                path
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  JUMP_BACK            98  'to 98'
              368  POP_BLOCK        
              370  BEGIN_FINALLY    
            372_0  COME_FROM_WITH       92  '92'
              372  WITH_CLEANUP_START
              374  WITH_CLEANUP_FINISH
              376  END_FINALLY      

 L. 401       378  LOAD_FAST                'topdown'
          380_382  POP_JUMP_IF_FALSE   470  'to 470'

 L. 402       384  LOAD_FAST                'top'
              386  LOAD_FAST                'dirs'
              388  LOAD_FAST                'nondirs'
              390  BUILD_TUPLE_3         3 
              392  YIELD_VALUE      
              394  POP_TOP          

 L. 405       396  LOAD_GLOBAL              path
              398  LOAD_ATTR                islink
              400  LOAD_GLOBAL              path
              402  LOAD_ATTR                join
              404  ROT_TWO          
              406  STORE_FAST               'islink'
              408  STORE_FAST               'join'

 L. 406       410  LOAD_FAST                'dirs'
              412  GET_ITER         
            414_0  COME_FROM           440  '440'
              414  FOR_ITER            468  'to 468'
              416  STORE_FAST               'dirname'

 L. 407       418  LOAD_FAST                'join'
              420  LOAD_FAST                'top'
              422  LOAD_FAST                'dirname'
              424  CALL_FUNCTION_2       2  ''
              426  STORE_FAST               'new_path'

 L. 412       428  LOAD_FAST                'followlinks'
          430_432  POP_JUMP_IF_TRUE    444  'to 444'
              434  LOAD_FAST                'islink'
              436  LOAD_FAST                'new_path'
              438  CALL_FUNCTION_1       1  ''
          440_442  POP_JUMP_IF_TRUE    414  'to 414'
            444_0  COME_FROM           430  '430'

 L. 413       444  LOAD_GLOBAL              walk
              446  LOAD_FAST                'new_path'
              448  LOAD_FAST                'topdown'
              450  LOAD_FAST                'onerror'
              452  LOAD_FAST                'followlinks'
              454  CALL_FUNCTION_4       4  ''
              456  GET_YIELD_FROM_ITER
              458  LOAD_CONST               None
              460  YIELD_FROM       
              462  POP_TOP          
          464_466  JUMP_BACK           414  'to 414'
              468  JUMP_FORWARD        514  'to 514'
            470_0  COME_FROM           380  '380'

 L. 416       470  LOAD_FAST                'walk_dirs'
              472  GET_ITER         
              474  FOR_ITER            502  'to 502'
              476  STORE_FAST               'new_path'

 L. 417       478  LOAD_GLOBAL              walk
              480  LOAD_FAST                'new_path'
              482  LOAD_FAST                'topdown'
              484  LOAD_FAST                'onerror'
              486  LOAD_FAST                'followlinks'
              488  CALL_FUNCTION_4       4  ''
              490  GET_YIELD_FROM_ITER
              492  LOAD_CONST               None
              494  YIELD_FROM       
              496  POP_TOP          
          498_500  JUMP_BACK           474  'to 474'

 L. 419       502  LOAD_FAST                'top'
              504  LOAD_FAST                'dirs'
              506  LOAD_FAST                'nondirs'
              508  BUILD_TUPLE_3         3 
              510  YIELD_VALUE      
              512  POP_TOP          
            514_0  COME_FROM           468  '468'

Parse error at or near `CALL_FINALLY' instruction at offset 70


__all__.append('walk')
if {
 open, stat} <= supports_dir_fd:
    if {scandir, stat} <= supports_fd:

        def fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None):
            """Directory tree generator.

        This behaves exactly like walk(), except that it yields a 4-tuple

            dirpath, dirnames, filenames, dirfd

        `dirpath`, `dirnames` and `filenames` are identical to walk() output,
        and `dirfd` is a file descriptor referring to the directory `dirpath`.

        The advantage of fwalk() over walk() is that it's safe against symlink
        races (when follow_symlinks is False).

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and top should be relative; top will then be relative to that directory.
          (dir_fd is always supported for fwalk.)

        Caution:
        Since fwalk() yields file descriptors, those are only valid until the
        next iteration step, so you should dup() them if you want to keep them
        for a longer period.

        Example:

        import os
        for root, dirs, files, rootfd in os.fwalk('python/Lib/email'):
            print(root, "consumes", end="")
            print(sum(os.stat(name, dir_fd=rootfd).st_size for name in files),
                  end="")
            print("bytes in", len(files), "non-directory files")
            if 'CVS' in dirs:
                dirs.remove('CVS')  # don't visit CVS directories
        """
            if not (isinstance(top, int) and hasattr(top, '__index__')):
                top = fspath(top)
            if not follow_symlinks:
                orig_st = stat(top, follow_symlinks=False, dir_fd=dir_fd)
            topfd = open(top, O_RDONLY, dir_fd=dir_fd)
            try:
                if (follow_symlinks or st.S_ISDIR)(orig_st.st_mode):
                    if path.samestat(orig_st, stat(topfd)):
                        (yield from _fwalk(topfd, top, isinstance(top, bytes), topdown, onerror, follow_symlinks))
            finally:
                close(topfd)

            if False:
                yield None


        def _fwalk--- This code section failed: ---

 L. 478         0  LOAD_GLOBAL              scandir
                2  LOAD_FAST                'topfd'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'scandir_it'

 L. 479         8  BUILD_LIST_0          0 
               10  STORE_FAST               'dirs'

 L. 480        12  BUILD_LIST_0          0 
               14  STORE_FAST               'nondirs'

 L. 481        16  LOAD_FAST                'topdown'
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  LOAD_FAST                'follow_symlinks'
               22  POP_JUMP_IF_FALSE    28  'to 28'
             24_0  COME_FROM            18  '18'
               24  LOAD_CONST               None
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            22  '22'
               28  BUILD_LIST_0          0 
             30_0  COME_FROM            26  '26'
               30  STORE_FAST               'entries'

 L. 482        32  LOAD_FAST                'scandir_it'
               34  GET_ITER         
               36  FOR_ITER            178  'to 178'
               38  STORE_FAST               'entry'

 L. 483        40  LOAD_FAST                'entry'
               42  LOAD_ATTR                name
               44  STORE_FAST               'name'

 L. 484        46  LOAD_FAST                'isbytes'
               48  POP_JUMP_IF_FALSE    58  'to 58'

 L. 485        50  LOAD_GLOBAL              fsencode
               52  LOAD_FAST                'name'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'name'
             58_0  COME_FROM            48  '48'

 L. 486        58  SETUP_FINALLY       112  'to 112'

 L. 487        60  LOAD_FAST                'entry'
               62  LOAD_METHOD              is_dir
               64  CALL_METHOD_0         0  ''
               66  POP_JUMP_IF_FALSE    98  'to 98'

 L. 488        68  LOAD_FAST                'dirs'
               70  LOAD_METHOD              append
               72  LOAD_FAST                'name'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 489        78  LOAD_FAST                'entries'
               80  LOAD_CONST               None
               82  COMPARE_OP               is-not
               84  POP_JUMP_IF_FALSE   108  'to 108'

 L. 490        86  LOAD_FAST                'entries'
               88  LOAD_METHOD              append
               90  LOAD_FAST                'entry'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  JUMP_FORWARD        108  'to 108'
             98_0  COME_FROM            66  '66'

 L. 492        98  LOAD_FAST                'nondirs'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'name'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            96  '96'
            108_1  COME_FROM            84  '84'
              108  POP_BLOCK        
              110  JUMP_BACK            36  'to 36'
            112_0  COME_FROM_FINALLY    58  '58'

 L. 493       112  DUP_TOP          
              114  LOAD_GLOBAL              OSError
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   174  'to 174'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L. 494       126  SETUP_FINALLY       150  'to 150'

 L. 496       128  LOAD_FAST                'entry'
              130  LOAD_METHOD              is_symlink
              132  CALL_METHOD_0         0  ''
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 497       136  LOAD_FAST                'nondirs'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'name'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           134  '134'
              146  POP_BLOCK        
              148  JUMP_FORWARD        170  'to 170'
            150_0  COME_FROM_FINALLY   126  '126'

 L. 498       150  DUP_TOP          
              152  LOAD_GLOBAL              OSError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   168  'to 168'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 499       164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           156  '156'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           148  '148'
              170  POP_EXCEPT       
              172  JUMP_BACK            36  'to 36'
            174_0  COME_FROM           118  '118'
              174  END_FINALLY      
              176  JUMP_BACK            36  'to 36'

 L. 501       178  LOAD_FAST                'topdown'
              180  POP_JUMP_IF_FALSE   196  'to 196'

 L. 502       182  LOAD_FAST                'toppath'
              184  LOAD_FAST                'dirs'
              186  LOAD_FAST                'nondirs'
              188  LOAD_FAST                'topfd'
              190  BUILD_TUPLE_4         4 
              192  YIELD_VALUE      
              194  POP_TOP          
            196_0  COME_FROM           180  '180'

 L. 504       196  LOAD_FAST                'entries'
              198  LOAD_CONST               None
              200  COMPARE_OP               is
              202  POP_JUMP_IF_FALSE   208  'to 208'
              204  LOAD_FAST                'dirs'
              206  JUMP_FORWARD        216  'to 216'
            208_0  COME_FROM           202  '202'
              208  LOAD_GLOBAL              zip
              210  LOAD_FAST                'dirs'
              212  LOAD_FAST                'entries'
              214  CALL_FUNCTION_2       2  ''
            216_0  COME_FROM           206  '206'
              216  GET_ITER         
              218  FOR_ITER            442  'to 442'
              220  STORE_FAST               'name'

 L. 505       222  SETUP_FINALLY       302  'to 302'

 L. 506       224  LOAD_FAST                'follow_symlinks'
          226_228  POP_JUMP_IF_TRUE    284  'to 284'

 L. 507       230  LOAD_FAST                'topdown'
              232  POP_JUMP_IF_FALSE   250  'to 250'

 L. 508       234  LOAD_GLOBAL              stat
              236  LOAD_FAST                'name'
              238  LOAD_FAST                'topfd'
              240  LOAD_CONST               False
              242  LOAD_CONST               ('dir_fd', 'follow_symlinks')
              244  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              246  STORE_FAST               'orig_st'
              248  JUMP_FORWARD        284  'to 284'
            250_0  COME_FROM           232  '232'

 L. 510       250  LOAD_FAST                'entries'
              252  LOAD_CONST               None
              254  COMPARE_OP               is-not
          256_258  POP_JUMP_IF_TRUE    264  'to 264'
              260  LOAD_ASSERT              AssertionError
              262  RAISE_VARARGS_1       1  'exception instance'
            264_0  COME_FROM           256  '256'

 L. 511       264  LOAD_FAST                'name'
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'name'
              270  STORE_FAST               'entry'

 L. 512       272  LOAD_FAST                'entry'
              274  LOAD_ATTR                stat
              276  LOAD_CONST               False
              278  LOAD_CONST               ('follow_symlinks',)
              280  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              282  STORE_FAST               'orig_st'
            284_0  COME_FROM           248  '248'
            284_1  COME_FROM           226  '226'

 L. 513       284  LOAD_GLOBAL              open
              286  LOAD_FAST                'name'
              288  LOAD_GLOBAL              O_RDONLY
              290  LOAD_FAST                'topfd'
              292  LOAD_CONST               ('dir_fd',)
              294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              296  STORE_FAST               'dirfd'
              298  POP_BLOCK        
              300  JUMP_FORWARD        364  'to 364'
            302_0  COME_FROM_FINALLY   222  '222'

 L. 514       302  DUP_TOP          
              304  LOAD_GLOBAL              OSError
              306  COMPARE_OP               exception-match
          308_310  POP_JUMP_IF_FALSE   362  'to 362'
              312  POP_TOP          
              314  STORE_FAST               'err'
              316  POP_TOP          
              318  SETUP_FINALLY       350  'to 350'

 L. 515       320  LOAD_FAST                'onerror'
              322  LOAD_CONST               None
              324  COMPARE_OP               is-not
          326_328  POP_JUMP_IF_FALSE   338  'to 338'

 L. 516       330  LOAD_FAST                'onerror'
              332  LOAD_FAST                'err'
              334  CALL_FUNCTION_1       1  ''
              336  POP_TOP          
            338_0  COME_FROM           326  '326'

 L. 517       338  POP_BLOCK        
              340  POP_EXCEPT       
              342  CALL_FINALLY        350  'to 350'
              344  JUMP_BACK           218  'to 218'
              346  POP_BLOCK        
              348  BEGIN_FINALLY    
            350_0  COME_FROM           342  '342'
            350_1  COME_FROM_FINALLY   318  '318'
              350  LOAD_CONST               None
              352  STORE_FAST               'err'
              354  DELETE_FAST              'err'
              356  END_FINALLY      
              358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
            362_0  COME_FROM           308  '308'
              362  END_FINALLY      
            364_0  COME_FROM           360  '360'
            364_1  COME_FROM           300  '300'

 L. 518       364  SETUP_FINALLY       430  'to 430'

 L. 519       366  LOAD_FAST                'follow_symlinks'
          368_370  POP_JUMP_IF_TRUE    390  'to 390'
              372  LOAD_GLOBAL              path
              374  LOAD_METHOD              samestat
              376  LOAD_FAST                'orig_st'
              378  LOAD_GLOBAL              stat
              380  LOAD_FAST                'dirfd'
              382  CALL_FUNCTION_1       1  ''
              384  CALL_METHOD_2         2  ''
          386_388  POP_JUMP_IF_FALSE   426  'to 426'
            390_0  COME_FROM           368  '368'

 L. 520       390  LOAD_GLOBAL              path
              392  LOAD_METHOD              join
              394  LOAD_FAST                'toppath'
              396  LOAD_FAST                'name'
              398  CALL_METHOD_2         2  ''
              400  STORE_FAST               'dirpath'

 L. 521       402  LOAD_GLOBAL              _fwalk
              404  LOAD_FAST                'dirfd'
              406  LOAD_FAST                'dirpath'
              408  LOAD_FAST                'isbytes'

 L. 522       410  LOAD_FAST                'topdown'

 L. 522       412  LOAD_FAST                'onerror'

 L. 522       414  LOAD_FAST                'follow_symlinks'

 L. 521       416  CALL_FUNCTION_6       6  ''
              418  GET_YIELD_FROM_ITER
              420  LOAD_CONST               None
              422  YIELD_FROM       
              424  POP_TOP          
            426_0  COME_FROM           386  '386'
              426  POP_BLOCK        
              428  BEGIN_FINALLY    
            430_0  COME_FROM_FINALLY   364  '364'

 L. 524       430  LOAD_GLOBAL              close
              432  LOAD_FAST                'dirfd'
              434  CALL_FUNCTION_1       1  ''
              436  POP_TOP          
              438  END_FINALLY      
              440  JUMP_BACK           218  'to 218'

 L. 526       442  LOAD_FAST                'topdown'
          444_446  POP_JUMP_IF_TRUE    462  'to 462'

 L. 527       448  LOAD_FAST                'toppath'
              450  LOAD_FAST                'dirs'
              452  LOAD_FAST                'nondirs'
              454  LOAD_FAST                'topfd'
              456  BUILD_TUPLE_4         4 
              458  YIELD_VALUE      
              460  POP_TOP          
            462_0  COME_FROM           444  '444'

Parse error at or near `CALL_FINALLY' instruction at offset 342


        __all__.append('fwalk')

def execl(file, *args):
    """execl(file, *args)

    Execute the executable file with argument list args, replacing the
    current process. """
    execv(file, args)


def execle(file, *args):
    """execle(file, *args, env)

    Execute the executable file with argument list args and
    environment env, replacing the current process. """
    env = args[(-1)]
    execve(file, args[:-1], env)


def execlp(file, *args):
    """execlp(file, *args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process. """
    execvp(file, args)


def execlpe(file, *args):
    """execlpe(file, *args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env, replacing the current
    process. """
    env = args[(-1)]
    execvpe(file, args[:-1], env)


def execvp(file, args):
    """execvp(file, args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args)


def execvpe(file, args, env):
    """execvpe(file, args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env, replacing the
    current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args, env)


__all__.extend(['execl', 'execle', 'execlp', 'execlpe', 'execvp', 'execvpe'])

def _execvpe(file, args, env=None):
    if env is not None:
        exec_func = execve
        argrest = (args, env)
    else:
        exec_func = execv
        argrest = (args,)
        env = environ
    if path.dirname(file):
        exec_func(file, *argrest)
        return
    saved_exc = None
    path_list = get_exec_path(env)
    if name != 'nt':
        file = fsencode(file)
        path_list = map(fsencode, path_list)
    for dir in path_list:
        fullname = path.join(dir, file)
        try:
            exec_func(fullname, *argrest)
        except (FileNotFoundError, NotADirectoryError) as e:
            try:
                last_exc = e
            finally:
                e = None
                del e

        except OSError as e:
            try:
                last_exc = e
                if saved_exc is None:
                    saved_exc = e
            finally:
                e = None
                del e

    else:
        if saved_exc is not None:
            raise saved_exc
        raise last_exc


def get_exec_path(env=None):
    """Returns the sequence of directories that will be searched for the
    named executable (similar to a shell) when launching a process.

    *env* must be an environment variable dict or None.  If *env* is None,
    os.environ will be used.
    """
    import warnings
    if env is None:
        env = environ
    with warnings.catch_warnings:
        warnings.simplefilter('ignore', BytesWarning)
        try:
            path_list = env.get('PATH')
        except TypeError:
            path_list = None
        else:
            if supports_bytes_environ:
                try:
                    path_listb = env[b'PATH']
                except (KeyError, TypeError):
                    pass
                else:
                    if path_list is not None:
                        raise ValueError("env cannot contain 'PATH' and b'PATH' keys")
                    path_list = path_listb
                if path_list is not None:
                    if isinstance(path_list, bytes):
                        path_list = fsdecode(path_list)
    if path_list is None:
        path_list = defpath
    return path_list.split(pathsep)


from _collections_abc import MutableMapping

class _Environ(MutableMapping):

    def __init__(self, data, encodekey, decodekey, encodevalue, decodevalue, putenv, unsetenv):
        self.encodekey = encodekey
        self.decodekey = decodekey
        self.encodevalue = encodevalue
        self.decodevalue = decodevalue
        self.putenv = putenv
        self.unsetenv = unsetenv
        self._data = data

    def __getitem__(self, key):
        try:
            value = self._data[self.encodekey(key)]
        except KeyError:
            raise KeyError(key) from None
        else:
            return self.decodevalue(value)

    def __setitem__(self, key, value):
        key = self.encodekey(key)
        value = self.encodevalue(value)
        self.putenv(key, value)
        self._data[key] = value

    def __delitem__(self, key):
        encodedkey = self.encodekey(key)
        self.unsetenv(encodedkey)
        try:
            del self._data[encodedkey]
        except KeyError:
            raise KeyError(key) from None

    def __iter__(self):
        keys = list(self._data)
        for key in keys:
            (yield self.decodekey(key))

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return 'environ({{{}}})'.format(', '.join(('{!r}: {!r}'.format(self.decodekey(key), self.decodevalue(value)) for key, value in self._data.items)))

    def copy(self):
        return dict(self)

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
        return self[key]


try:
    _putenv = putenv
except NameError:
    _putenv = lambda key, value: None

if 'putenv' not in __all__:
    __all__.append('putenv')
try:
    _unsetenv = unsetenv
except NameError:
    _unsetenv = lambda key: _putenv(key, '')
else:
    if 'unsetenv' not in __all__:
        __all__.append('unsetenv')

    def _createenviron():
        if name == 'nt':

            def check_str(value):
                if not isinstance(value, str):
                    raise TypeError('str expected, not %s' % type(value).__name__)
                return value

            encode = check_str
            decode = str

            def encodekey(key):
                return encode(key).upper

            data = {}
            for key, value in environ.items:
                data[encodekey(key)] = value

        else:
            encoding = sys.getfilesystemencoding

            def encode(value):
                if not isinstance(value, str):
                    raise TypeError('str expected, not %s' % type(value).__name__)
                return value.encode(encoding, 'surrogateescape')

            def decode(value):
                return value.decode(encoding, 'surrogateescape')

            encodekey = encode
            data = environ
        return _Environ(data, encodekey, decode, encode, decode, _putenv, _unsetenv)


    environ = _createenviron()
    del _createenviron

    def getenv(key, default=None):
        """Get an environment variable, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    key, default and the result are str."""
        return environ.get(key, default)


    supports_bytes_environ = name != 'nt'
    __all__.extend(('getenv', 'supports_bytes_environ'))
    if supports_bytes_environ:

        def _check_bytes(value):
            if not isinstance(value, bytes):
                raise TypeError('bytes expected, not %s' % type(value).__name__)
            return value


        environb = _Environ(environ._data, _check_bytes, bytes, _check_bytes, bytes, _putenv, _unsetenv)
        del _check_bytes

        def getenvb(key, default=None):
            """Get an environment variable, return None if it doesn't exist.
        The optional second argument can specify an alternate default.
        key, default and the result are bytes."""
            return environb.get(key, default)


        __all__.extend(('environb', 'getenvb'))

    def _fscodec():
        encoding = sys.getfilesystemencoding
        errors = sys.getfilesystemencodeerrors

        def fsencode(filename):
            filename = fspath(filename)
            if isinstance(filename, str):
                return filename.encode(encoding, errors)
            return filename

        def fsdecode(filename):
            filename = fspath(filename)
            if isinstance(filename, bytes):
                return filename.decode(encoding, errors)
            return filename

        return (
         fsencode, fsdecode)


    fsencode, fsdecode = _fscodec()
    del _fscodec
    if _exists('fork') and not _exists('spawnv'):
        if _exists('execv'):
            P_WAIT = 0
            P_NOWAIT = P_NOWAITO = 1
            __all__.extend(['P_WAIT', 'P_NOWAIT', 'P_NOWAITO'])

            def _spawnvef(mode, file, args, env, func):
                if not isinstance(args, (tuple, list)):
                    raise TypeError('argv must be a tuple or a list')
                elif args:
                    if not args[0]:
                        raise ValueError('argv first element cannot be empty')
                    pid = fork()
                    if not pid:
                        try:
                            if env is None:
                                func(file, args)
                            else:
                                func(file, args, env)
                        except:
                            _exit(127)

                else:
                    if mode == P_NOWAIT:
                        return pid
                    while True:
                        wpid, sts = waitpid(pid, 0)
                        if WIFSTOPPED(sts):
                            continue
                        else:
                            if WIFSIGNALED(sts):
                                return -WTERMSIG(sts)
                            if WIFEXITED(sts):
                                return WEXITSTATUS(sts)
                            raise OSError('Not stopped, signaled or exited???')


            def spawnv(mode, file, args):
                """spawnv(mode, file, args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                return _spawnvef(mode, file, args, None, execv)


            def spawnve(mode, file, args, env):
                """spawnve(mode, file, args, env) -> integer

Execute file with arguments from args in a subprocess with the
specified environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                return _spawnvef(mode, file, args, env, execve)


            def spawnvp(mode, file, args):
                """spawnvp(mode, file, args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                return _spawnvef(mode, file, args, None, execvp)


            def spawnvpe(mode, file, args, env):
                """spawnvpe(mode, file, args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                return _spawnvef(mode, file, args, env, execvpe)


            __all__.extend(['spawnv', 'spawnve', 'spawnvp', 'spawnvpe'])
        else:
            if _exists('spawnv'):

                def spawnl(mode, file, *args):
                    """spawnl(mode, file, *args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    return spawnv(mode, file, args)


                def spawnle(mode, file, *args):
                    """spawnle(mode, file, *args, env) -> integer

Execute file with arguments from args in a subprocess with the
supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    env = args[(-1)]
                    return spawnvemodefileargs[:-1]env


                __all__.extend(['spawnl', 'spawnle'])
            if _exists('spawnvp'):

                def spawnlp(mode, file, *args):
                    """spawnlp(mode, file, *args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    return spawnvp(mode, file, args)


                def spawnlpe(mode, file, *args):
                    """spawnlpe(mode, file, *args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    env = args[(-1)]
                    return spawnvpemodefileargs[:-1]env


                __all__.extend(['spawnlp', 'spawnlpe'])

            def popen(cmd, mode='r', buffering=-1):
                if not isinstance(cmd, str):
                    raise TypeError('invalid cmd type (%s, expected string)' % type(cmd))
                if mode not in ('r', 'w'):
                    raise ValueError('invalid mode %r' % mode)
                if buffering == 0 or buffering is None:
                    raise ValueError('popen() does not support unbuffered streams')
                import subprocess, io
                if mode == 'r':
                    proc = subprocess.Popen(cmd, shell=True,
                      stdout=(subprocess.PIPE),
                      bufsize=buffering)
                    return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
                proc = subprocess.Popen(cmd, shell=True,
                  stdin=(subprocess.PIPE),
                  bufsize=buffering)
                return _wrap_close(io.TextIOWrapper(proc.stdin), proc)


            class _wrap_close:

                def __init__(self, stream, proc):
                    self._stream = stream
                    self._proc = proc

                def close(self):
                    self._stream.close
                    returncode = self._proc.wait
                    if returncode == 0:
                        return
                    if name == 'nt':
                        return returncode
                    return returncode << 8

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    self.close

                def __getattr__(self, name):
                    return getattr(self._stream, name)

                def __iter__(self):
                    return iter(self._stream)


            def fdopen(fd, *args, **kwargs):
                if not isinstance(fd, int):
                    raise TypeError('invalid fd type (%s, expected integer)' % type(fd))
                import io
                return (io.open)(fd, *args, **kwargs)


            def _fspath(path):
                """Return the path representation of a path-like object.

    If str or bytes is passed in, it is returned unchanged. Otherwise the
    os.PathLike interface is used to get the path representation. If the
    path representation is not str or bytes, TypeError is raised. If the
    provided path is not str, bytes, or os.PathLike, TypeError is raised.
    """
                if isinstance(path, (str, bytes)):
                    return path
                path_type = type(path)
                try:
                    path_repr = path_type.__fspath__(path)
                except AttributeError:
                    if hasattr(path_type, '__fspath__'):
                        raise
                    else:
                        raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__)
                else:
                    if isinstance(path_repr, (str, bytes)):
                        return path_repr
                    raise TypeError('expected {}.__fspath__() to return str or bytes, not {}'.format(path_type.__name__, type(path_repr).__name__))


            fspath = _exists('fspath') or _fspath
            fspath.__name__ = 'fspath'

        class PathLike(abc.ABC):
            __doc__ = 'Abstract base class for implementing the file system path protocol.'

            @abc.abstractmethod
            def __fspath__(self):
                """Return the file system path representation of the object."""
                raise NotImplementedError

            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is PathLike:
                    return _check_methods(subclass, '__fspath__')
                return NotImplemented


        if name == 'nt':

            class _AddedDllDirectory:

                def __init__(self, path, cookie, remove_dll_directory):
                    self.path = path
                    self._cookie = cookie
                    self._remove_dll_directory = remove_dll_directory

                def close(self):
                    self._remove_dll_directory(self._cookie)
                    self.path = None

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    self.close

                def __repr__(self):
                    if self.path:
                        return '<AddedDllDirectory({!r})>'.format(self.path)
                    return '<AddedDllDirectory()>'


            def add_dll_directory(path):
                """Add a path to the DLL search path.

        This search path is used when resolving dependencies for imported
        extension modules (the module itself is resolved through sys.path),
        and also by ctypes.

        Remove the directory by calling close() on the returned object or
        using it in a with statement.
        """
                import nt
                cookie = nt._add_dll_directory(path)
                return _AddedDllDirectory(path, cookie, nt._remove_dll_directory)