# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: shutil.py
"""Utility functions for copying and archiving files and directory trees.

XXX The functions here don't copy the resource fork or other metadata on Mac.

"""
import os, sys, stat, fnmatch, collections, errno
try:
    import zlib
    del zlib
    _ZLIB_SUPPORTED = True
except ImportError:
    _ZLIB_SUPPORTED = False

try:
    import bz2
    del bz2
    _BZ2_SUPPORTED = True
except ImportError:
    _BZ2_SUPPORTED = False

try:
    import lzma
    del lzma
    _LZMA_SUPPORTED = True
except ImportError:
    _LZMA_SUPPORTED = False

try:
    from pwd import getpwnam
except ImportError:
    getpwnam = None
else:
    try:
        from grp import getgrnam
    except ImportError:
        getgrnam = None
    else:
        _WINDOWS = os.name == 'nt'
        posix = nt = None
if os.name == 'posix':
    import posix
else:
    if _WINDOWS:
        import nt
    else:
        COPY_BUFSIZE = 1048576 if _WINDOWS else 65536
        _USE_CP_SENDFILE = hasattr(os, 'sendfile') and sys.platform.startswith('linux')
        _HAS_FCOPYFILE = posix and hasattr(posix, '_fcopyfile')
        __all__ = [
         'copyfileobj', 'copyfile', 'copymode', 'copystat', 'copy', 'copy2',
         'copytree', 'move', 'rmtree', 'Error', 'SpecialFileError',
         'ExecError', 'make_archive', 'get_archive_formats',
         'register_archive_format', 'unregister_archive_format',
         'get_unpack_formats', 'register_unpack_format',
         'unregister_unpack_format', 'unpack_archive',
         'ignore_patterns', 'chown', 'which', 'get_terminal_size',
         'SameFileError']

        class Error(OSError):
            pass


        class SameFileError(Error):
            __doc__ = 'Raised when source and destination are the same file.'


        class SpecialFileError(OSError):
            __doc__ = 'Raised when trying to do a kind of operation (e.g. copying) which is\n    not supported on a special file (e.g. a named pipe)'


        class ExecError(OSError):
            __doc__ = 'Raised when a command could not be executed'


        class ReadError(OSError):
            __doc__ = 'Raised when an archive cannot be read'


        class RegistryError(Exception):
            __doc__ = 'Raised when a registry operation with the archiving\n    and unpacking registries fails'


        class _GiveupOnFastCopy(Exception):
            __doc__ = 'Raised as a signal to fallback on using raw read()/write()\n    file copy when fast-copy functions fail to do so.\n    '


        def _fastcopy_fcopyfile(fsrc, fdst, flags):
            """Copy a regular file content or metadata by using high-performance
    fcopyfile(3) syscall (macOS).
    """
            try:
                infd = fsrc.fileno()
                outfd = fdst.fileno()
            except Exception as err:
                try:
                    raise _GiveupOnFastCopy(err)
                finally:
                    err = None
                    del err

            try:
                posix._fcopyfile(infd, outfd, flags)
            except OSError as err:
                try:
                    err.filename = fsrc.name
                    err.filename2 = fdst.name
                    if err.errno in {errno.EINVAL, errno.ENOTSUP}:
                        raise _GiveupOnFastCopy(err)
                    else:
                        raise err from None
                finally:
                    err = None
                    del err


        def _fastcopy_sendfile(fsrc, fdst):
            """Copy data from one regular mmap-like fd to another by using
    high-performance sendfile(2) syscall.
    This should work on Linux >= 2.6.33 only.
    """
            global _USE_CP_SENDFILE
            try:
                infd = fsrc.fileno()
                outfd = fdst.fileno()
            except Exception as err:
                try:
                    raise _GiveupOnFastCopy(err)
                finally:
                    err = None
                    del err

            else:
                try:
                    blocksize = max(os.fstat(infd).st_size, 8388608)
                except OSError:
                    blocksize = 134217728
                else:
                    if sys.maxsize < 4294967296:
                        blocksize = min(blocksize, 1073741824)
                    offset = 0
                    while True:
                        try:
                            sent = os.sendfile(outfd, infd, offset, blocksize)
                        except OSError as err:
                            try:
                                err.filename = fsrc.name
                                err.filename2 = fdst.name
                                if err.errno == errno.ENOTSOCK:
                                    _USE_CP_SENDFILE = False
                                    raise _GiveupOnFastCopy(err)
                                if err.errno == errno.ENOSPC:
                                    raise err from None
                                if offset == 0:
                                    if os.lseek(outfd, 0, os.SEEK_CUR) == 0:
                                        raise _GiveupOnFastCopy(err)
                                raise err
                            finally:
                                err = None
                                del err

                        else:
                            if sent == 0:
                                break
                            offset += sent


        def _copyfileobj_readinto(fsrc, fdst, length=COPY_BUFSIZE):
            """readinto()/memoryview() based variant of copyfileobj().
    *fsrc* must support readinto() method and both files must be
    open in binary mode.
    """
            fsrc_readinto = fsrc.readinto
            fdst_write = fdst.write
            with memoryview(bytearray(length)) as (mv):
                while True:
                    n = fsrc_readinto(mv)
                    if not n:
                        break
                    elif n < length:
                        with mv[:n] as (smv):
                            fdst.write(smv)
                    else:
                        fdst_write(mv)


        def copyfileobj(fsrc, fdst, length=0):
            """copy data from file-like object fsrc to file-like object fdst"""
            if not length:
                length = COPY_BUFSIZE
            fsrc_read = fsrc.read
            fdst_write = fdst.write
            while True:
                buf = fsrc_read(length)
                if not buf:
                    break
                fdst_write(buf)


        def _samefile--- This code section failed: ---

 L. 209         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'src'
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                DirEntry
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    74  'to 74'
               12  LOAD_GLOBAL              hasattr
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                path
               18  LOAD_STR                 'samestat'
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    74  'to 74'

 L. 210        24  SETUP_FINALLY        52  'to 52'

 L. 211        26  LOAD_GLOBAL              os
               28  LOAD_ATTR                path
               30  LOAD_METHOD              samestat
               32  LOAD_FAST                'src'
               34  LOAD_METHOD              stat
               36  CALL_METHOD_0         0  ''
               38  LOAD_GLOBAL              os
               40  LOAD_METHOD              stat
               42  LOAD_FAST                'dst'
               44  CALL_METHOD_1         1  ''
               46  CALL_METHOD_2         2  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    24  '24'

 L. 212        52  DUP_TOP          
               54  LOAD_GLOBAL              OSError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 213        66  POP_EXCEPT       
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      
             74_0  COME_FROM            22  '22'
             74_1  COME_FROM            10  '10'

 L. 215        74  LOAD_GLOBAL              hasattr
               76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_STR                 'samefile'
               82  CALL_FUNCTION_2       2  ''
               84  POP_JUMP_IF_FALSE   126  'to 126'

 L. 216        86  SETUP_FINALLY       104  'to 104'

 L. 217        88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_METHOD              samefile
               94  LOAD_FAST                'src'
               96  LOAD_FAST                'dst'
               98  CALL_METHOD_2         2  ''
              100  POP_BLOCK        
              102  RETURN_VALUE     
            104_0  COME_FROM_FINALLY    86  '86'

 L. 218       104  DUP_TOP          
              106  LOAD_GLOBAL              OSError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   124  'to 124'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 219       118  POP_EXCEPT       
              120  LOAD_CONST               False
              122  RETURN_VALUE     
            124_0  COME_FROM           110  '110'
              124  END_FINALLY      
            126_0  COME_FROM            84  '84'

 L. 222       126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              normcase
              132  LOAD_GLOBAL              os
              134  LOAD_ATTR                path
              136  LOAD_METHOD              abspath
              138  LOAD_FAST                'src'
              140  CALL_METHOD_1         1  ''
              142  CALL_METHOD_1         1  ''

 L. 223       144  LOAD_GLOBAL              os
              146  LOAD_ATTR                path
              148  LOAD_METHOD              normcase
              150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              abspath
              156  LOAD_FAST                'dst'
              158  CALL_METHOD_1         1  ''
              160  CALL_METHOD_1         1  ''

 L. 222       162  COMPARE_OP               ==
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 62


        def _stat(fn):
            if isinstance(fn, os.DirEntry):
                return fn.stat()
            return os.stat(fn)


        def _islink(fn):
            if isinstance(fn, os.DirEntry):
                return fn.is_symlink()
            return os.path.islink(fn)


        def copyfile--- This code section failed: ---

 L. 238         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              audit
                4  LOAD_STR                 'shutil.copyfile'
                6  LOAD_FAST                'src'
                8  LOAD_FAST                'dst'
               10  CALL_METHOD_3         3  ''
               12  POP_TOP          

 L. 240        14  LOAD_GLOBAL              _samefile
               16  LOAD_FAST                'src'
               18  LOAD_FAST                'dst'
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    40  'to 40'

 L. 241        24  LOAD_GLOBAL              SameFileError
               26  LOAD_STR                 '{!r} and {!r} are the same file'
               28  LOAD_METHOD              format
               30  LOAD_FAST                'src'
               32  LOAD_FAST                'dst'
               34  CALL_METHOD_2         2  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            22  '22'

 L. 243        40  LOAD_CONST               0
               42  STORE_FAST               'file_size'

 L. 244        44  LOAD_GLOBAL              enumerate
               46  LOAD_FAST                'src'
               48  LOAD_FAST                'dst'
               50  BUILD_LIST_2          2 
               52  CALL_FUNCTION_1       1  ''
               54  GET_ITER         
             56_0  COME_FROM           154  '154'
             56_1  COME_FROM           146  '146'
               56  FOR_ITER            164  'to 164'
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'i'
               62  STORE_FAST               'fn'

 L. 245        64  SETUP_FINALLY        78  'to 78'

 L. 246        66  LOAD_GLOBAL              _stat
               68  LOAD_FAST                'fn'
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'st'
               74  POP_BLOCK        
               76  JUMP_FORWARD         98  'to 98'
             78_0  COME_FROM_FINALLY    64  '64'

 L. 247        78  DUP_TOP          
               80  LOAD_GLOBAL              OSError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE    96  'to 96'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 249        92  POP_EXCEPT       
               94  JUMP_BACK            56  'to 56'
             96_0  COME_FROM            84  '84'
               96  END_FINALLY      
             98_0  COME_FROM            76  '76'

 L. 252        98  LOAD_GLOBAL              stat
              100  LOAD_METHOD              S_ISFIFO
              102  LOAD_FAST                'st'
              104  LOAD_ATTR                st_mode
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   144  'to 144'

 L. 253       110  LOAD_GLOBAL              isinstance
              112  LOAD_FAST                'fn'
              114  LOAD_GLOBAL              os
              116  LOAD_ATTR                DirEntry
              118  CALL_FUNCTION_2       2  ''
              120  POP_JUMP_IF_FALSE   128  'to 128'
              122  LOAD_FAST                'fn'
              124  LOAD_ATTR                path
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           120  '120'
              128  LOAD_FAST                'fn'
            130_0  COME_FROM           126  '126'
              130  STORE_FAST               'fn'

 L. 254       132  LOAD_GLOBAL              SpecialFileError
              134  LOAD_STR                 '`%s` is a named pipe'
              136  LOAD_FAST                'fn'
              138  BINARY_MODULO    
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           108  '108'

 L. 255       144  LOAD_GLOBAL              _WINDOWS
              146  POP_JUMP_IF_FALSE    56  'to 56'
              148  LOAD_FAST                'i'
              150  LOAD_CONST               0
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE    56  'to 56'

 L. 256       156  LOAD_FAST                'st'
              158  LOAD_ATTR                st_size
              160  STORE_FAST               'file_size'
              162  JUMP_BACK            56  'to 56'

 L. 258       164  LOAD_FAST                'follow_symlinks'
              166  POP_JUMP_IF_TRUE    198  'to 198'
              168  LOAD_GLOBAL              _islink
              170  LOAD_FAST                'src'
              172  CALL_FUNCTION_1       1  ''
              174  POP_JUMP_IF_FALSE   198  'to 198'

 L. 259       176  LOAD_GLOBAL              os
              178  LOAD_METHOD              symlink
              180  LOAD_GLOBAL              os
              182  LOAD_METHOD              readlink
              184  LOAD_FAST                'src'
              186  CALL_METHOD_1         1  ''
              188  LOAD_FAST                'dst'
              190  CALL_METHOD_2         2  ''
              192  POP_TOP          
          194_196  JUMP_FORWARD        464  'to 464'
            198_0  COME_FROM           174  '174'
            198_1  COME_FROM           166  '166'

 L. 261       198  LOAD_GLOBAL              open
              200  LOAD_FAST                'src'
              202  LOAD_STR                 'rb'
              204  CALL_FUNCTION_2       2  ''
          206_208  SETUP_WITH          458  'to 458'
              210  STORE_FAST               'fsrc'
              212  LOAD_GLOBAL              open
              214  LOAD_FAST                'dst'
              216  LOAD_STR                 'wb'
              218  CALL_FUNCTION_2       2  ''
              220  SETUP_WITH          448  'to 448'
              222  STORE_FAST               'fdst'

 L. 263       224  LOAD_GLOBAL              _HAS_FCOPYFILE
          226_228  POP_JUMP_IF_FALSE   300  'to 300'

 L. 264       230  SETUP_FINALLY       276  'to 276'

 L. 265       232  LOAD_GLOBAL              _fastcopy_fcopyfile
              234  LOAD_FAST                'fsrc'
              236  LOAD_FAST                'fdst'
              238  LOAD_GLOBAL              posix
              240  LOAD_ATTR                _COPYFILE_DATA
              242  CALL_FUNCTION_3       3  ''
              244  POP_TOP          

 L. 266       246  LOAD_FAST                'dst'
              248  POP_BLOCK        
              250  POP_BLOCK        
              252  ROT_TWO          
              254  BEGIN_FINALLY    
              256  WITH_CLEANUP_START
              258  WITH_CLEANUP_FINISH
              260  POP_FINALLY           0  ''
              262  POP_BLOCK        
              264  ROT_TWO          
              266  BEGIN_FINALLY    
              268  WITH_CLEANUP_START
              270  WITH_CLEANUP_FINISH
              272  POP_FINALLY           0  ''
              274  RETURN_VALUE     
            276_0  COME_FROM_FINALLY   230  '230'

 L. 267       276  DUP_TOP          
              278  LOAD_GLOBAL              _GiveupOnFastCopy
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   296  'to 296'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L. 268       292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           282  '282'
              296  END_FINALLY      
            298_0  COME_FROM           294  '294'
              298  JUMP_FORWARD        434  'to 434'
            300_0  COME_FROM           226  '226'

 L. 270       300  LOAD_GLOBAL              _USE_CP_SENDFILE
          302_304  POP_JUMP_IF_FALSE   372  'to 372'

 L. 271       306  SETUP_FINALLY       348  'to 348'

 L. 272       308  LOAD_GLOBAL              _fastcopy_sendfile
              310  LOAD_FAST                'fsrc'
              312  LOAD_FAST                'fdst'
              314  CALL_FUNCTION_2       2  ''
              316  POP_TOP          

 L. 273       318  LOAD_FAST                'dst'
              320  POP_BLOCK        
              322  POP_BLOCK        
              324  ROT_TWO          
              326  BEGIN_FINALLY    
              328  WITH_CLEANUP_START
              330  WITH_CLEANUP_FINISH
              332  POP_FINALLY           0  ''
              334  POP_BLOCK        
              336  ROT_TWO          
              338  BEGIN_FINALLY    
              340  WITH_CLEANUP_START
              342  WITH_CLEANUP_FINISH
              344  POP_FINALLY           0  ''
              346  RETURN_VALUE     
            348_0  COME_FROM_FINALLY   306  '306'

 L. 274       348  DUP_TOP          
              350  LOAD_GLOBAL              _GiveupOnFastCopy
              352  COMPARE_OP               exception-match
          354_356  POP_JUMP_IF_FALSE   368  'to 368'
              358  POP_TOP          
              360  POP_TOP          
              362  POP_TOP          

 L. 275       364  POP_EXCEPT       
              366  JUMP_FORWARD        370  'to 370'
            368_0  COME_FROM           354  '354'
              368  END_FINALLY      
            370_0  COME_FROM           366  '366'
              370  JUMP_FORWARD        434  'to 434'
            372_0  COME_FROM           302  '302'

 L. 278       372  LOAD_GLOBAL              _WINDOWS
          374_376  POP_JUMP_IF_FALSE   434  'to 434'
              378  LOAD_FAST                'file_size'
              380  LOAD_CONST               0
              382  COMPARE_OP               >
          384_386  POP_JUMP_IF_FALSE   434  'to 434'

 L. 279       388  LOAD_GLOBAL              _copyfileobj_readinto
              390  LOAD_FAST                'fsrc'
              392  LOAD_FAST                'fdst'
              394  LOAD_GLOBAL              min
              396  LOAD_FAST                'file_size'
              398  LOAD_GLOBAL              COPY_BUFSIZE
              400  CALL_FUNCTION_2       2  ''
              402  CALL_FUNCTION_3       3  ''
              404  POP_TOP          

 L. 280       406  LOAD_FAST                'dst'
              408  POP_BLOCK        
              410  ROT_TWO          
              412  BEGIN_FINALLY    
              414  WITH_CLEANUP_START
              416  WITH_CLEANUP_FINISH
              418  POP_FINALLY           0  ''
              420  POP_BLOCK        
              422  ROT_TWO          
              424  BEGIN_FINALLY    
              426  WITH_CLEANUP_START
              428  WITH_CLEANUP_FINISH
              430  POP_FINALLY           0  ''
              432  RETURN_VALUE     
            434_0  COME_FROM           384  '384'
            434_1  COME_FROM           374  '374'
            434_2  COME_FROM           370  '370'
            434_3  COME_FROM           298  '298'

 L. 282       434  LOAD_GLOBAL              copyfileobj
              436  LOAD_FAST                'fsrc'
              438  LOAD_FAST                'fdst'
              440  CALL_FUNCTION_2       2  ''
              442  POP_TOP          
              444  POP_BLOCK        
              446  BEGIN_FINALLY    
            448_0  COME_FROM_WITH      220  '220'
              448  WITH_CLEANUP_START
              450  WITH_CLEANUP_FINISH
              452  END_FINALLY      
              454  POP_BLOCK        
              456  BEGIN_FINALLY    
            458_0  COME_FROM_WITH      206  '206'
              458  WITH_CLEANUP_START
              460  WITH_CLEANUP_FINISH
              462  END_FINALLY      
            464_0  COME_FROM           194  '194'

 L. 284       464  LOAD_FAST                'dst'
              466  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 250


        def copymode(src, dst, *, follow_symlinks=True):
            """Copy mode bits from src to dst.

    If follow_symlinks is not set, symlinks aren't followed if and only
    if both `src` and `dst` are symlinks.  If `lchmod` isn't available
    (e.g. Linux) this method does nothing.

    """
            sys.audit('shutil.copymode', src, dst)
            if not follow_symlinks:
                if _islink(src):
                    if os.path.islink(dst):
                        if hasattr(os, 'lchmod'):
                            stat_func, chmod_func = os.lstat, os.lchmod
                    else:
                        return
            else:
                stat_func, chmod_func = _stat, os.chmod
            st = stat_func(src)
            chmod_func(dst, stat.S_IMODE(st.st_mode))


        if hasattr(os, 'listxattr'):

            def _copyxattr--- This code section failed: ---

 L. 317         0  SETUP_FINALLY        20  'to 20'

 L. 318         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                listxattr
                6  LOAD_FAST                'src'
                8  LOAD_FAST                'follow_symlinks'
               10  LOAD_CONST               ('follow_symlinks',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'names'
               16  POP_BLOCK        
               18  JUMP_FORWARD         84  'to 84'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 319        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    82  'to 82'
               28  POP_TOP          
               30  STORE_FAST               'e'
               32  POP_TOP          
               34  SETUP_FINALLY        70  'to 70'

 L. 320        36  LOAD_FAST                'e'
               38  LOAD_ATTR                errno
               40  LOAD_GLOBAL              errno
               42  LOAD_ATTR                ENOTSUP
               44  LOAD_GLOBAL              errno
               46  LOAD_ATTR                ENODATA
               48  LOAD_GLOBAL              errno
               50  LOAD_ATTR                EINVAL
               52  BUILD_TUPLE_3         3 
               54  COMPARE_OP               not-in
               56  POP_JUMP_IF_FALSE    60  'to 60'

 L. 321        58  RAISE_VARARGS_0       0  'reraise'
             60_0  COME_FROM            56  '56'

 L. 322        60  POP_BLOCK        
               62  POP_EXCEPT       
               64  CALL_FINALLY         70  'to 70'
               66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM            64  '64'
             70_1  COME_FROM_FINALLY    34  '34'
               70  LOAD_CONST               None
               72  STORE_FAST               'e'
               74  DELETE_FAST              'e'
               76  END_FINALLY      
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            26  '26'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            18  '18'

 L. 323        84  LOAD_FAST                'names'
               86  GET_ITER         
               88  FOR_ITER            196  'to 196'
               90  STORE_FAST               'name'

 L. 324        92  SETUP_FINALLY       132  'to 132'

 L. 325        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                getxattr
               98  LOAD_FAST                'src'
              100  LOAD_FAST                'name'
              102  LOAD_FAST                'follow_symlinks'
              104  LOAD_CONST               ('follow_symlinks',)
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  STORE_FAST               'value'

 L. 326       110  LOAD_GLOBAL              os
              112  LOAD_ATTR                setxattr
              114  LOAD_FAST                'dst'
              116  LOAD_FAST                'name'
              118  LOAD_FAST                'value'
              120  LOAD_FAST                'follow_symlinks'
              122  LOAD_CONST               ('follow_symlinks',)
              124  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              126  POP_TOP          
              128  POP_BLOCK        
              130  JUMP_BACK            88  'to 88'
            132_0  COME_FROM_FINALLY    92  '92'

 L. 327       132  DUP_TOP          
              134  LOAD_GLOBAL              OSError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   192  'to 192'
              140  POP_TOP          
              142  STORE_FAST               'e'
              144  POP_TOP          
              146  SETUP_FINALLY       180  'to 180'

 L. 328       148  LOAD_FAST                'e'
              150  LOAD_ATTR                errno
              152  LOAD_GLOBAL              errno
              154  LOAD_ATTR                EPERM
              156  LOAD_GLOBAL              errno
              158  LOAD_ATTR                ENOTSUP
              160  LOAD_GLOBAL              errno
              162  LOAD_ATTR                ENODATA

 L. 329       164  LOAD_GLOBAL              errno
              166  LOAD_ATTR                EINVAL

 L. 328       168  BUILD_TUPLE_4         4 
              170  COMPARE_OP               not-in
              172  POP_JUMP_IF_FALSE   176  'to 176'

 L. 330       174  RAISE_VARARGS_0       0  'reraise'
            176_0  COME_FROM           172  '172'
              176  POP_BLOCK        
              178  BEGIN_FINALLY    
            180_0  COME_FROM_FINALLY   146  '146'
              180  LOAD_CONST               None
              182  STORE_FAST               'e'
              184  DELETE_FAST              'e'
              186  END_FINALLY      
              188  POP_EXCEPT       
              190  JUMP_BACK            88  'to 88'
            192_0  COME_FROM           138  '138'
              192  END_FINALLY      
              194  JUMP_BACK            88  'to 88'

Parse error at or near `CALL_FINALLY' instruction at offset 64


        else:

            def _copyxattr(*args, **kwargs):
                pass


        def copystat(src, dst, *, follow_symlinks=True):
            """Copy file metadata

    Copy the permission bits, last access time, last modification time, and
    flags from `src` to `dst`. On Linux, copystat() also copies the "extended
    attributes" where possible. The file contents, owner, and group are
    unaffected. `src` and `dst` are path-like objects or path names given as
    strings.

    If the optional flag `follow_symlinks` is not set, symlinks aren't
    followed if and only if both `src` and `dst` are symlinks.
    """
            sys.audit('shutil.copystat', src, dst)

            def _nop(*args, ns=None, follow_symlinks=None):
                pass

            follow = follow_symlinks or not (_islink(src) and os.path.islink(dst))
            if follow:

                def lookup(name):
                    return getattr(os, name, _nop)

            else:

                def lookup(name):
                    fn = getattr(os, name, _nop)
                    if fn in os.supports_follow_symlinks:
                        return fn
                    return _nop

            if isinstance(src, os.DirEntry):
                st = src.stat(follow_symlinks=follow)
            else:
                st = lookup('stat')(src, follow_symlinks=follow)
            mode = stat.S_IMODE(st.st_mode)
            lookup('utime')(dst, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=follow)
            _copyxattr(src, dst, follow_symlinks=follow)
            try:
                lookup('chmod')(dst, mode, follow_symlinks=follow)
            except NotImplementedError:
                pass
            else:
                if hasattr(st, 'st_flags'):
                    try:
                        lookup('chflags')(dst, (st.st_flags), follow_symlinks=follow)
                    except OSError as why:
                        try:
                            for err in ('EOPNOTSUPP', 'ENOTSUP'):
                                if hasattr(errno, err) and why.errno == getattr(errno, err):
                                    break
                            else:
                                raise

                        finally:
                            why = None
                            del why


        def copy(src, dst, *, follow_symlinks=True):
            """Copy data and mode bits ("cp src dst"). Return the file's destination.

    The destination may be a directory.

    If follow_symlinks is false, symlinks won't be followed. This
    resembles GNU's "cp -P src dst".

    If source and destination are the same file, a SameFileError will be
    raised.

    """
            if os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))
            copyfile(src, dst, follow_symlinks=follow_symlinks)
            copymode(src, dst, follow_symlinks=follow_symlinks)
            return dst


        def copy2(src, dst, *, follow_symlinks=True):
            """Copy data and metadata. Return the file's destination.

    Metadata is copied with copystat(). Please see the copystat function
    for more information.

    The destination may be a directory.

    If follow_symlinks is false, symlinks won't be followed. This
    resembles GNU's "cp -P src dst".
    """
            if os.path.isdir(dst):
                dst = os.path.join(dst, os.path.basename(src))
            copyfile(src, dst, follow_symlinks=follow_symlinks)
            copystat(src, dst, follow_symlinks=follow_symlinks)
            return dst


        def ignore_patterns(*patterns):
            """Function that can be used as copytree() ignore parameter.

    Patterns is a sequence of glob-style patterns
    that are used to exclude files"""

            def _ignore_patterns(path, names):
                ignored_names = []
                for pattern in patterns:
                    ignored_names.extend(fnmatch.filter(names, pattern))
                else:
                    return set(ignored_names)

            return _ignore_patterns


        def _copytree--- This code section failed: ---

 L. 450         0  LOAD_FAST                'ignore'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    36  'to 36'

 L. 451         8  LOAD_FAST                'ignore'
               10  LOAD_GLOBAL              os
               12  LOAD_METHOD              fspath
               14  LOAD_FAST                'src'
               16  CALL_METHOD_1         1  ''
               18  LOAD_LISTCOMP            '<code_object <listcomp>>'
               20  LOAD_STR                 '_copytree.<locals>.<listcomp>'
               22  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               24  LOAD_FAST                'entries'
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'ignored_names'
               34  JUMP_FORWARD         42  'to 42'
             36_0  COME_FROM             6  '6'

 L. 453        36  LOAD_GLOBAL              set
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'ignored_names'
             42_0  COME_FROM            34  '34'

 L. 455        42  LOAD_GLOBAL              os
               44  LOAD_ATTR                makedirs
               46  LOAD_FAST                'dst'
               48  LOAD_FAST                'dirs_exist_ok'
               50  LOAD_CONST               ('exist_ok',)
               52  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               54  POP_TOP          

 L. 456        56  BUILD_LIST_0          0 
               58  STORE_FAST               'errors'

 L. 457        60  LOAD_FAST                'copy_function'
               62  LOAD_GLOBAL              copy2
               64  COMPARE_OP               is
               66  JUMP_IF_TRUE_OR_POP    74  'to 74'
               68  LOAD_FAST                'copy_function'
               70  LOAD_GLOBAL              copy
               72  COMPARE_OP               is
             74_0  COME_FROM            66  '66'
               74  STORE_FAST               'use_srcentry'

 L. 459        76  LOAD_FAST                'entries'
               78  GET_ITER         
            80_82  FOR_ITER            466  'to 466'
               84  STORE_FAST               'srcentry'

 L. 460        86  LOAD_FAST                'srcentry'
               88  LOAD_ATTR                name
               90  LOAD_FAST                'ignored_names'
               92  COMPARE_OP               in
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 461        96  JUMP_BACK            80  'to 80'
             98_0  COME_FROM            94  '94'

 L. 462        98  LOAD_GLOBAL              os
              100  LOAD_ATTR                path
              102  LOAD_METHOD              join
              104  LOAD_FAST                'src'
              106  LOAD_FAST                'srcentry'
              108  LOAD_ATTR                name
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'srcname'

 L. 463       114  LOAD_GLOBAL              os
              116  LOAD_ATTR                path
              118  LOAD_METHOD              join
              120  LOAD_FAST                'dst'
              122  LOAD_FAST                'srcentry'
              124  LOAD_ATTR                name
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'dstname'

 L. 464       130  LOAD_FAST                'use_srcentry'
              132  POP_JUMP_IF_FALSE   138  'to 138'
              134  LOAD_FAST                'srcentry'
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           132  '132'
              138  LOAD_FAST                'srcname'
            140_0  COME_FROM           136  '136'
              140  STORE_FAST               'srcobj'

 L. 465       142  SETUP_FINALLY       358  'to 358'

 L. 466       144  LOAD_FAST                'srcentry'
              146  LOAD_METHOD              is_symlink
              148  CALL_METHOD_0         0  ''
              150  STORE_FAST               'is_symlink'

 L. 467       152  LOAD_FAST                'is_symlink'
              154  POP_JUMP_IF_FALSE   194  'to 194'
              156  LOAD_GLOBAL              os
              158  LOAD_ATTR                name
              160  LOAD_STR                 'nt'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   194  'to 194'

 L. 470       166  LOAD_FAST                'srcentry'
              168  LOAD_ATTR                stat
              170  LOAD_CONST               False
              172  LOAD_CONST               ('follow_symlinks',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  STORE_FAST               'lstat'

 L. 471       178  LOAD_FAST                'lstat'
              180  LOAD_ATTR                st_reparse_tag
              182  LOAD_GLOBAL              stat
              184  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   194  'to 194'

 L. 472       190  LOAD_CONST               False
              192  STORE_FAST               'is_symlink'
            194_0  COME_FROM           188  '188'
            194_1  COME_FROM           164  '164'
            194_2  COME_FROM           154  '154'

 L. 473       194  LOAD_FAST                'is_symlink'
          196_198  POP_JUMP_IF_FALSE   312  'to 312'

 L. 474       200  LOAD_GLOBAL              os
              202  LOAD_METHOD              readlink
              204  LOAD_FAST                'srcname'
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'linkto'

 L. 475       210  LOAD_FAST                'symlinks'
              212  POP_JUMP_IF_FALSE   244  'to 244'

 L. 479       214  LOAD_GLOBAL              os
              216  LOAD_METHOD              symlink
              218  LOAD_FAST                'linkto'
              220  LOAD_FAST                'dstname'
              222  CALL_METHOD_2         2  ''
              224  POP_TOP          

 L. 480       226  LOAD_GLOBAL              copystat
              228  LOAD_FAST                'srcobj'
              230  LOAD_FAST                'dstname'
              232  LOAD_FAST                'symlinks'
              234  UNARY_NOT        
              236  LOAD_CONST               ('follow_symlinks',)
              238  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              240  POP_TOP          
              242  JUMP_FORWARD        310  'to 310'
            244_0  COME_FROM           212  '212'

 L. 483       244  LOAD_GLOBAL              os
              246  LOAD_ATTR                path
              248  LOAD_METHOD              exists
              250  LOAD_FAST                'linkto'
              252  CALL_METHOD_1         1  ''
          254_256  POP_JUMP_IF_TRUE    268  'to 268'
              258  LOAD_FAST                'ignore_dangling_symlinks'
          260_262  POP_JUMP_IF_FALSE   268  'to 268'

 L. 484       264  POP_BLOCK        
              266  JUMP_BACK            80  'to 80'
            268_0  COME_FROM           260  '260'
            268_1  COME_FROM           254  '254'

 L. 486       268  LOAD_FAST                'srcentry'
              270  LOAD_METHOD              is_dir
              272  CALL_METHOD_0         0  ''
          274_276  POP_JUMP_IF_FALSE   300  'to 300'

 L. 487       278  LOAD_GLOBAL              copytree
              280  LOAD_FAST                'srcobj'
              282  LOAD_FAST                'dstname'
              284  LOAD_FAST                'symlinks'
              286  LOAD_FAST                'ignore'

 L. 488       288  LOAD_FAST                'copy_function'

 L. 488       290  LOAD_FAST                'dirs_exist_ok'

 L. 487       292  LOAD_CONST               ('dirs_exist_ok',)
              294  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              296  POP_TOP          
              298  JUMP_FORWARD        310  'to 310'
            300_0  COME_FROM           274  '274'

 L. 490       300  LOAD_FAST                'copy_function'
              302  LOAD_FAST                'srcobj'
              304  LOAD_FAST                'dstname'
              306  CALL_FUNCTION_2       2  ''
              308  POP_TOP          
            310_0  COME_FROM           298  '298'
            310_1  COME_FROM           242  '242'
              310  JUMP_FORWARD        354  'to 354'
            312_0  COME_FROM           196  '196'

 L. 491       312  LOAD_FAST                'srcentry'
              314  LOAD_METHOD              is_dir
              316  CALL_METHOD_0         0  ''
          318_320  POP_JUMP_IF_FALSE   344  'to 344'

 L. 492       322  LOAD_GLOBAL              copytree
              324  LOAD_FAST                'srcobj'
              326  LOAD_FAST                'dstname'
              328  LOAD_FAST                'symlinks'
              330  LOAD_FAST                'ignore'
              332  LOAD_FAST                'copy_function'

 L. 493       334  LOAD_FAST                'dirs_exist_ok'

 L. 492       336  LOAD_CONST               ('dirs_exist_ok',)
              338  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              340  POP_TOP          
              342  JUMP_FORWARD        354  'to 354'
            344_0  COME_FROM           318  '318'

 L. 496       344  LOAD_FAST                'copy_function'
              346  LOAD_FAST                'srcobj'
              348  LOAD_FAST                'dstname'
              350  CALL_FUNCTION_2       2  ''
              352  POP_TOP          
            354_0  COME_FROM           342  '342'
            354_1  COME_FROM           310  '310'
              354  POP_BLOCK        
              356  JUMP_BACK            80  'to 80'
            358_0  COME_FROM_FINALLY   142  '142'

 L. 499       358  DUP_TOP          
              360  LOAD_GLOBAL              Error
              362  COMPARE_OP               exception-match
          364_366  POP_JUMP_IF_FALSE   408  'to 408'
              368  POP_TOP          
              370  STORE_FAST               'err'
              372  POP_TOP          
              374  SETUP_FINALLY       396  'to 396'

 L. 500       376  LOAD_FAST                'errors'
              378  LOAD_METHOD              extend
              380  LOAD_FAST                'err'
              382  LOAD_ATTR                args
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  CALL_METHOD_1         1  ''
              390  POP_TOP          
              392  POP_BLOCK        
              394  BEGIN_FINALLY    
            396_0  COME_FROM_FINALLY   374  '374'
              396  LOAD_CONST               None
              398  STORE_FAST               'err'
              400  DELETE_FAST              'err'
              402  END_FINALLY      
              404  POP_EXCEPT       
              406  JUMP_BACK            80  'to 80'
            408_0  COME_FROM           364  '364'

 L. 501       408  DUP_TOP          
              410  LOAD_GLOBAL              OSError
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   462  'to 462'
              418  POP_TOP          
              420  STORE_FAST               'why'
              422  POP_TOP          
              424  SETUP_FINALLY       450  'to 450'

 L. 502       426  LOAD_FAST                'errors'
              428  LOAD_METHOD              append
              430  LOAD_FAST                'srcname'
              432  LOAD_FAST                'dstname'
              434  LOAD_GLOBAL              str
              436  LOAD_FAST                'why'
              438  CALL_FUNCTION_1       1  ''
              440  BUILD_TUPLE_3         3 
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          
              446  POP_BLOCK        
              448  BEGIN_FINALLY    
            450_0  COME_FROM_FINALLY   424  '424'
              450  LOAD_CONST               None
              452  STORE_FAST               'why'
              454  DELETE_FAST              'why'
              456  END_FINALLY      
              458  POP_EXCEPT       
              460  JUMP_BACK            80  'to 80'
            462_0  COME_FROM           414  '414'
              462  END_FINALLY      
              464  JUMP_BACK            80  'to 80'

 L. 503       466  SETUP_FINALLY       482  'to 482'

 L. 504       468  LOAD_GLOBAL              copystat
              470  LOAD_FAST                'src'
              472  LOAD_FAST                'dst'
              474  CALL_FUNCTION_2       2  ''
              476  POP_TOP          
              478  POP_BLOCK        
              480  JUMP_FORWARD        556  'to 556'
            482_0  COME_FROM_FINALLY   466  '466'

 L. 505       482  DUP_TOP          
              484  LOAD_GLOBAL              OSError
              486  COMPARE_OP               exception-match
          488_490  POP_JUMP_IF_FALSE   554  'to 554'
              492  POP_TOP          
              494  STORE_FAST               'why'
              496  POP_TOP          
              498  SETUP_FINALLY       542  'to 542'

 L. 507       500  LOAD_GLOBAL              getattr
              502  LOAD_FAST                'why'
              504  LOAD_STR                 'winerror'
              506  LOAD_CONST               None
              508  CALL_FUNCTION_3       3  ''
              510  LOAD_CONST               None
              512  COMPARE_OP               is
          514_516  POP_JUMP_IF_FALSE   538  'to 538'

 L. 508       518  LOAD_FAST                'errors'
              520  LOAD_METHOD              append
              522  LOAD_FAST                'src'
              524  LOAD_FAST                'dst'
              526  LOAD_GLOBAL              str
              528  LOAD_FAST                'why'
              530  CALL_FUNCTION_1       1  ''
              532  BUILD_TUPLE_3         3 
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          
            538_0  COME_FROM           514  '514'
              538  POP_BLOCK        
              540  BEGIN_FINALLY    
            542_0  COME_FROM_FINALLY   498  '498'
              542  LOAD_CONST               None
              544  STORE_FAST               'why'
              546  DELETE_FAST              'why'
              548  END_FINALLY      
              550  POP_EXCEPT       
              552  JUMP_FORWARD        556  'to 556'
            554_0  COME_FROM           488  '488'
              554  END_FINALLY      
            556_0  COME_FROM           552  '552'
            556_1  COME_FROM           480  '480'

 L. 509       556  LOAD_FAST                'errors'
          558_560  POP_JUMP_IF_FALSE   570  'to 570'

 L. 510       562  LOAD_GLOBAL              Error
              564  LOAD_FAST                'errors'
              566  CALL_FUNCTION_1       1  ''
              568  RAISE_VARARGS_1       1  'exception instance'
            570_0  COME_FROM           558  '558'

 L. 511       570  LOAD_FAST                'dst'
              572  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 266


        def copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False):
            """Recursively copy a directory tree and return the destination directory.

    dirs_exist_ok dictates whether to raise an exception in case dst or any
    missing parent directory already exists.

    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.

    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():

        callable(src, names) -> ignored_names

    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.

    """
            sys.audit('shutil.copytree', src, dst)
            with os.scandir(src) as (itr):
                entries = list(itr)
            return _copytree(entries=entries, src=src, dst=dst, symlinks=symlinks, ignore=ignore,
              copy_function=copy_function,
              ignore_dangling_symlinks=ignore_dangling_symlinks,
              dirs_exist_ok=dirs_exist_ok)


        if hasattr(os.stat_result, 'st_file_attributes'):

            def _rmtree_isdir--- This code section failed: ---

 L. 564         0  SETUP_FINALLY        54  'to 54'

 L. 565         2  LOAD_FAST                'entry'
                4  LOAD_ATTR                stat
                6  LOAD_CONST               False
                8  LOAD_CONST               ('follow_symlinks',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'st'

 L. 566        14  LOAD_GLOBAL              stat
               16  LOAD_METHOD              S_ISDIR
               18  LOAD_FAST                'st'
               20  LOAD_ATTR                st_mode
               22  CALL_METHOD_1         1  ''
               24  JUMP_IF_FALSE_OR_POP    50  'to 50'

 L. 567        26  LOAD_FAST                'st'
               28  LOAD_ATTR                st_file_attributes
               30  LOAD_GLOBAL              stat
               32  LOAD_ATTR                FILE_ATTRIBUTE_REPARSE_POINT
               34  BINARY_AND       
               36  JUMP_IF_FALSE_OR_POP    48  'to 48'

 L. 568        38  LOAD_FAST                'st'
               40  LOAD_ATTR                st_reparse_tag
               42  LOAD_GLOBAL              stat
               44  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
               46  COMPARE_OP               ==
             48_0  COME_FROM            36  '36'

 L. 566        48  UNARY_NOT        
             50_0  COME_FROM            24  '24'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L. 569        54  DUP_TOP          
               56  LOAD_GLOBAL              OSError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    74  'to 74'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 570        68  POP_EXCEPT       
               70  LOAD_CONST               False
               72  RETURN_VALUE     
             74_0  COME_FROM            60  '60'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 64


            def _rmtree_islink--- This code section failed: ---

 L. 573         0  SETUP_FINALLY        50  'to 50'

 L. 574         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              lstat
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'st'

 L. 575        12  LOAD_GLOBAL              stat
               14  LOAD_METHOD              S_ISLNK
               16  LOAD_FAST                'st'
               18  LOAD_ATTR                st_mode
               20  CALL_METHOD_1         1  ''
               22  JUMP_IF_TRUE_OR_POP    46  'to 46'

 L. 576        24  LOAD_FAST                'st'
               26  LOAD_ATTR                st_file_attributes
               28  LOAD_GLOBAL              stat
               30  LOAD_ATTR                FILE_ATTRIBUTE_REPARSE_POINT
               32  BINARY_AND       
               34  JUMP_IF_FALSE_OR_POP    46  'to 46'

 L. 577        36  LOAD_FAST                'st'
               38  LOAD_ATTR                st_reparse_tag
               40  LOAD_GLOBAL              stat
               42  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
               44  COMPARE_OP               ==
             46_0  COME_FROM            34  '34'
             46_1  COME_FROM            22  '22'

 L. 575        46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY     0  '0'

 L. 578        50  DUP_TOP          
               52  LOAD_GLOBAL              OSError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    70  'to 70'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 579        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
             70_0  COME_FROM            56  '56'
               70  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 60


        else:

            def _rmtree_isdir--- This code section failed: ---

 L. 582         0  SETUP_FINALLY        16  'to 16'

 L. 583         2  LOAD_FAST                'entry'
                4  LOAD_ATTR                is_dir
                6  LOAD_CONST               False
                8  LOAD_CONST               ('follow_symlinks',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 584        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 585        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


        def _rmtree_islink(path):
            return os.path.islink(path)


    def _rmtree_unsafe--- This code section failed: ---

 L. 592         0  SETUP_FINALLY        36  'to 36'

 L. 593         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              scandir
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           26  'to 26'
               12  STORE_FAST               'scandir_it'

 L. 594        14  LOAD_GLOBAL              list
               16  LOAD_FAST                'scandir_it'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'entries'
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH       10  '10'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      
               32  POP_BLOCK        
               34  JUMP_FORWARD         78  'to 78'
             36_0  COME_FROM_FINALLY     0  '0'

 L. 595        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    76  'to 76'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 596        50  LOAD_FAST                'onerror'
               52  LOAD_GLOBAL              os
               54  LOAD_ATTR                scandir
               56  LOAD_FAST                'path'
               58  LOAD_GLOBAL              sys
               60  LOAD_METHOD              exc_info
               62  CALL_METHOD_0         0  ''
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          

 L. 597        68  BUILD_LIST_0          0 
               70  STORE_FAST               'entries'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            42  '42'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            34  '34'

 L. 598        78  LOAD_FAST                'entries'
               80  GET_ITER         
               82  FOR_ITER            234  'to 234'
               84  STORE_FAST               'entry'

 L. 599        86  LOAD_FAST                'entry'
               88  LOAD_ATTR                path
               90  STORE_FAST               'fullname'

 L. 600        92  LOAD_GLOBAL              _rmtree_isdir
               94  LOAD_FAST                'entry'
               96  CALL_FUNCTION_1       1  ''
               98  POP_JUMP_IF_FALSE   178  'to 178'

 L. 601       100  SETUP_FINALLY       122  'to 122'

 L. 602       102  LOAD_FAST                'entry'
              104  LOAD_METHOD              is_symlink
              106  CALL_METHOD_0         0  ''
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 606       110  LOAD_GLOBAL              OSError
              112  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           108  '108'
              118  POP_BLOCK        
              120  JUMP_FORWARD        166  'to 166'
            122_0  COME_FROM_FINALLY   100  '100'

 L. 607       122  DUP_TOP          
              124  LOAD_GLOBAL              OSError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   164  'to 164'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 608       136  LOAD_FAST                'onerror'
              138  LOAD_GLOBAL              os
              140  LOAD_ATTR                path
              142  LOAD_ATTR                islink
              144  LOAD_FAST                'fullname'
              146  LOAD_GLOBAL              sys
              148  LOAD_METHOD              exc_info
              150  CALL_METHOD_0         0  ''
              152  CALL_FUNCTION_3       3  ''
              154  POP_TOP          

 L. 609       156  POP_EXCEPT       
              158  JUMP_BACK            82  'to 82'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           128  '128'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           120  '120'

 L. 610       166  LOAD_GLOBAL              _rmtree_unsafe
              168  LOAD_FAST                'fullname'
              170  LOAD_FAST                'onerror'
              172  CALL_FUNCTION_2       2  ''
              174  POP_TOP          
              176  JUMP_BACK            82  'to 82'
            178_0  COME_FROM            98  '98'

 L. 612       178  SETUP_FINALLY       194  'to 194'

 L. 613       180  LOAD_GLOBAL              os
              182  LOAD_METHOD              unlink
              184  LOAD_FAST                'fullname'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  JUMP_BACK            82  'to 82'
            194_0  COME_FROM_FINALLY   178  '178'

 L. 614       194  DUP_TOP          
              196  LOAD_GLOBAL              OSError
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   230  'to 230'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 615       208  LOAD_FAST                'onerror'
              210  LOAD_GLOBAL              os
              212  LOAD_ATTR                unlink
              214  LOAD_FAST                'fullname'
              216  LOAD_GLOBAL              sys
              218  LOAD_METHOD              exc_info
              220  CALL_METHOD_0         0  ''
              222  CALL_FUNCTION_3       3  ''
              224  POP_TOP          
              226  POP_EXCEPT       
              228  JUMP_BACK            82  'to 82'
            230_0  COME_FROM           200  '200'
              230  END_FINALLY      
              232  JUMP_BACK            82  'to 82'

 L. 616       234  SETUP_FINALLY       250  'to 250'

 L. 617       236  LOAD_GLOBAL              os
              238  LOAD_METHOD              rmdir
              240  LOAD_FAST                'path'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  POP_BLOCK        
              248  JUMP_FORWARD        290  'to 290'
            250_0  COME_FROM_FINALLY   234  '234'

 L. 618       250  DUP_TOP          
              252  LOAD_GLOBAL              OSError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   288  'to 288'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 619       266  LOAD_FAST                'onerror'
              268  LOAD_GLOBAL              os
              270  LOAD_ATTR                rmdir
              272  LOAD_FAST                'path'
              274  LOAD_GLOBAL              sys
              276  LOAD_METHOD              exc_info
              278  CALL_METHOD_0         0  ''
              280  CALL_FUNCTION_3       3  ''
              282  POP_TOP          
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           256  '256'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           248  '248'

Parse error at or near `POP_EXCEPT' instruction at offset 160


    def _rmtree_safe_fd--- This code section failed: ---

 L. 623         0  SETUP_FINALLY        36  'to 36'

 L. 624         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              scandir
                6  LOAD_FAST                'topfd'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           26  'to 26'
               12  STORE_FAST               'scandir_it'

 L. 625        14  LOAD_GLOBAL              list
               16  LOAD_FAST                'scandir_it'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'entries'
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH       10  '10'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      
               32  POP_BLOCK        
               34  JUMP_FORWARD        100  'to 100'
             36_0  COME_FROM_FINALLY     0  '0'

 L. 626        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    98  'to 98'
               44  POP_TOP          
               46  STORE_FAST               'err'
               48  POP_TOP          
               50  SETUP_FINALLY        86  'to 86'

 L. 627        52  LOAD_FAST                'path'
               54  LOAD_FAST                'err'
               56  STORE_ATTR               filename

 L. 628        58  LOAD_FAST                'onerror'
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                scandir
               64  LOAD_FAST                'path'
               66  LOAD_GLOBAL              sys
               68  LOAD_METHOD              exc_info
               70  CALL_METHOD_0         0  ''
               72  CALL_FUNCTION_3       3  ''
               74  POP_TOP          

 L. 629        76  POP_BLOCK        
               78  POP_EXCEPT       
               80  CALL_FINALLY         86  'to 86'
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM_FINALLY    50  '50'
               86  LOAD_CONST               None
               88  STORE_FAST               'err'
               90  DELETE_FAST              'err'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            42  '42'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            34  '34'

 L. 630       100  LOAD_FAST                'entries'
              102  GET_ITER         
          104_106  FOR_ITER            554  'to 554'
              108  STORE_FAST               'entry'

 L. 631       110  LOAD_GLOBAL              os
              112  LOAD_ATTR                path
              114  LOAD_METHOD              join
              116  LOAD_FAST                'path'
              118  LOAD_FAST                'entry'
              120  LOAD_ATTR                name
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'fullname'

 L. 632       126  SETUP_FINALLY       144  'to 144'

 L. 633       128  LOAD_FAST                'entry'
              130  LOAD_ATTR                is_dir
              132  LOAD_CONST               False
              134  LOAD_CONST               ('follow_symlinks',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              138  STORE_FAST               'is_dir'
              140  POP_BLOCK        
              142  JUMP_FORWARD        168  'to 168'
            144_0  COME_FROM_FINALLY   126  '126'

 L. 634       144  DUP_TOP          
              146  LOAD_GLOBAL              OSError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   166  'to 166'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 635       158  LOAD_CONST               False
              160  STORE_FAST               'is_dir'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        244  'to 244'
            166_0  COME_FROM           150  '150'
              166  END_FINALLY      
            168_0  COME_FROM           142  '142'

 L. 637       168  LOAD_FAST                'is_dir'
              170  POP_JUMP_IF_FALSE   244  'to 244'

 L. 638       172  SETUP_FINALLY       202  'to 202'

 L. 639       174  LOAD_FAST                'entry'
              176  LOAD_ATTR                stat
              178  LOAD_CONST               False
              180  LOAD_CONST               ('follow_symlinks',)
              182  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              184  STORE_FAST               'orig_st'

 L. 640       186  LOAD_GLOBAL              stat
              188  LOAD_METHOD              S_ISDIR
              190  LOAD_FAST                'orig_st'
              192  LOAD_ATTR                st_mode
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'is_dir'
              198  POP_BLOCK        
              200  JUMP_FORWARD        244  'to 244'
            202_0  COME_FROM_FINALLY   172  '172'

 L. 641       202  DUP_TOP          
              204  LOAD_GLOBAL              OSError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   242  'to 242'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 642       216  LOAD_FAST                'onerror'
              218  LOAD_GLOBAL              os
              220  LOAD_ATTR                lstat
              222  LOAD_FAST                'fullname'
              224  LOAD_GLOBAL              sys
              226  LOAD_METHOD              exc_info
              228  CALL_METHOD_0         0  ''
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          

 L. 643       234  POP_EXCEPT       
              236  JUMP_BACK           104  'to 104'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           208  '208'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           200  '200'
            244_2  COME_FROM           170  '170'
            244_3  COME_FROM           164  '164'

 L. 644       244  LOAD_FAST                'is_dir'
          246_248  POP_JUMP_IF_FALSE   490  'to 490'

 L. 645       250  SETUP_FINALLY       276  'to 276'

 L. 646       252  LOAD_GLOBAL              os
              254  LOAD_ATTR                open
              256  LOAD_FAST                'entry'
              258  LOAD_ATTR                name
              260  LOAD_GLOBAL              os
              262  LOAD_ATTR                O_RDONLY
              264  LOAD_FAST                'topfd'
              266  LOAD_CONST               ('dir_fd',)
              268  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              270  STORE_FAST               'dirfd'
              272  POP_BLOCK        
              274  JUMP_FORWARD        316  'to 316'
            276_0  COME_FROM_FINALLY   250  '250'

 L. 647       276  DUP_TOP          
              278  LOAD_GLOBAL              OSError
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   314  'to 314'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L. 648       292  LOAD_FAST                'onerror'
              294  LOAD_GLOBAL              os
              296  LOAD_ATTR                open
              298  LOAD_FAST                'fullname'
              300  LOAD_GLOBAL              sys
              302  LOAD_METHOD              exc_info
              304  CALL_METHOD_0         0  ''
              306  CALL_FUNCTION_3       3  ''
              308  POP_TOP          
              310  POP_EXCEPT       
              312  JUMP_FORWARD        488  'to 488'
            314_0  COME_FROM           282  '282'
              314  END_FINALLY      
            316_0  COME_FROM           274  '274'

 L. 650       316  SETUP_FINALLY       476  'to 476'

 L. 651       318  LOAD_GLOBAL              os
              320  LOAD_ATTR                path
              322  LOAD_METHOD              samestat
              324  LOAD_FAST                'orig_st'
              326  LOAD_GLOBAL              os
              328  LOAD_METHOD              fstat
              330  LOAD_FAST                'dirfd'
              332  CALL_METHOD_1         1  ''
              334  CALL_METHOD_2         2  ''
          336_338  POP_JUMP_IF_FALSE   416  'to 416'

 L. 652       340  LOAD_GLOBAL              _rmtree_safe_fd
              342  LOAD_FAST                'dirfd'
              344  LOAD_FAST                'fullname'
              346  LOAD_FAST                'onerror'
              348  CALL_FUNCTION_3       3  ''
              350  POP_TOP          

 L. 653       352  SETUP_FINALLY       374  'to 374'

 L. 654       354  LOAD_GLOBAL              os
              356  LOAD_ATTR                rmdir
              358  LOAD_FAST                'entry'
              360  LOAD_ATTR                name
              362  LOAD_FAST                'topfd'
              364  LOAD_CONST               ('dir_fd',)
              366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              368  POP_TOP          
              370  POP_BLOCK        
              372  JUMP_FORWARD        414  'to 414'
            374_0  COME_FROM_FINALLY   352  '352'

 L. 655       374  DUP_TOP          
              376  LOAD_GLOBAL              OSError
              378  COMPARE_OP               exception-match
          380_382  POP_JUMP_IF_FALSE   412  'to 412'
              384  POP_TOP          
              386  POP_TOP          
              388  POP_TOP          

 L. 656       390  LOAD_FAST                'onerror'
              392  LOAD_GLOBAL              os
              394  LOAD_ATTR                rmdir
              396  LOAD_FAST                'fullname'
              398  LOAD_GLOBAL              sys
              400  LOAD_METHOD              exc_info
              402  CALL_METHOD_0         0  ''
              404  CALL_FUNCTION_3       3  ''
              406  POP_TOP          
              408  POP_EXCEPT       
              410  JUMP_FORWARD        414  'to 414'
            412_0  COME_FROM           380  '380'
              412  END_FINALLY      
            414_0  COME_FROM           410  '410'
            414_1  COME_FROM           372  '372'
              414  JUMP_FORWARD        472  'to 472'
            416_0  COME_FROM           336  '336'

 L. 658       416  SETUP_FINALLY       430  'to 430'

 L. 662       418  LOAD_GLOBAL              OSError
              420  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              422  CALL_FUNCTION_1       1  ''
              424  RAISE_VARARGS_1       1  'exception instance'
              426  POP_BLOCK        
              428  JUMP_FORWARD        472  'to 472'
            430_0  COME_FROM_FINALLY   416  '416'

 L. 664       430  DUP_TOP          
              432  LOAD_GLOBAL              OSError
              434  COMPARE_OP               exception-match
          436_438  POP_JUMP_IF_FALSE   470  'to 470'
              440  POP_TOP          
              442  POP_TOP          
              444  POP_TOP          

 L. 665       446  LOAD_FAST                'onerror'
              448  LOAD_GLOBAL              os
              450  LOAD_ATTR                path
              452  LOAD_ATTR                islink
              454  LOAD_FAST                'fullname'
              456  LOAD_GLOBAL              sys
              458  LOAD_METHOD              exc_info
              460  CALL_METHOD_0         0  ''
              462  CALL_FUNCTION_3       3  ''
              464  POP_TOP          
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
            470_0  COME_FROM           436  '436'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           428  '428'
            472_2  COME_FROM           414  '414'
              472  POP_BLOCK        
              474  BEGIN_FINALLY    
            476_0  COME_FROM_FINALLY   316  '316'

 L. 667       476  LOAD_GLOBAL              os
              478  LOAD_METHOD              close
              480  LOAD_FAST                'dirfd'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
              486  END_FINALLY      
            488_0  COME_FROM           312  '312'
              488  JUMP_BACK           104  'to 104'
            490_0  COME_FROM           246  '246'

 L. 669       490  SETUP_FINALLY       512  'to 512'

 L. 670       492  LOAD_GLOBAL              os
              494  LOAD_ATTR                unlink
              496  LOAD_FAST                'entry'
              498  LOAD_ATTR                name
              500  LOAD_FAST                'topfd'
              502  LOAD_CONST               ('dir_fd',)
              504  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              506  POP_TOP          
              508  POP_BLOCK        
              510  JUMP_BACK           104  'to 104'
            512_0  COME_FROM_FINALLY   490  '490'

 L. 671       512  DUP_TOP          
              514  LOAD_GLOBAL              OSError
              516  COMPARE_OP               exception-match
          518_520  POP_JUMP_IF_FALSE   550  'to 550'
              522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L. 672       528  LOAD_FAST                'onerror'
              530  LOAD_GLOBAL              os
              532  LOAD_ATTR                unlink
              534  LOAD_FAST                'fullname'
              536  LOAD_GLOBAL              sys
              538  LOAD_METHOD              exc_info
              540  CALL_METHOD_0         0  ''
              542  CALL_FUNCTION_3       3  ''
              544  POP_TOP          
              546  POP_EXCEPT       
              548  JUMP_BACK           104  'to 104'
            550_0  COME_FROM           518  '518'
              550  END_FINALLY      
              552  JUMP_BACK           104  'to 104'

Parse error at or near `CALL_FINALLY' instruction at offset 80


    _use_fd_functions = {os.open, os.stat, os.unlink, os.rmdir} <= os.supports_dir_fd and os.scandir in os.supports_fd and os.stat in os.supports_follow_symlinks

    def rmtree--- This code section failed: ---

 L. 690         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              audit
                4  LOAD_STR                 'shutil.rmtree'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 691        12  LOAD_FAST                'ignore_errors'
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 692        16  LOAD_CODE                <code_object onerror>
               18  LOAD_STR                 'rmtree.<locals>.onerror'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'onerror'
               24  JUMP_FORWARD         42  'to 42'
             26_0  COME_FROM            14  '14'

 L. 694        26  LOAD_FAST                'onerror'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 695        34  LOAD_CODE                <code_object onerror>
               36  LOAD_STR                 'rmtree.<locals>.onerror'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  STORE_FAST               'onerror'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'

 L. 697        42  LOAD_GLOBAL              _use_fd_functions
            44_46  POP_JUMP_IF_FALSE   352  'to 352'

 L. 699        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'path'
               52  LOAD_GLOBAL              bytes
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 700        58  LOAD_GLOBAL              os
               60  LOAD_METHOD              fsdecode
               62  LOAD_FAST                'path'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'path'
             68_0  COME_FROM            56  '56'

 L. 703        68  SETUP_FINALLY        84  'to 84'

 L. 704        70  LOAD_GLOBAL              os
               72  LOAD_METHOD              lstat
               74  LOAD_FAST                'path'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'orig_st'
               80  POP_BLOCK        
               82  JUMP_FORWARD        124  'to 124'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 705        84  DUP_TOP          
               86  LOAD_GLOBAL              Exception
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   122  'to 122'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 706        98  LOAD_FAST                'onerror'
              100  LOAD_GLOBAL              os
              102  LOAD_ATTR                lstat
              104  LOAD_FAST                'path'
              106  LOAD_GLOBAL              sys
              108  LOAD_METHOD              exc_info
              110  CALL_METHOD_0         0  ''
              112  CALL_FUNCTION_3       3  ''
              114  POP_TOP          

 L. 707       116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            90  '90'
              122  END_FINALLY      
            124_0  COME_FROM            82  '82'

 L. 708       124  SETUP_FINALLY       144  'to 144'

 L. 709       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              open
              130  LOAD_FAST                'path'
              132  LOAD_GLOBAL              os
              134  LOAD_ATTR                O_RDONLY
              136  CALL_METHOD_2         2  ''
              138  STORE_FAST               'fd'
              140  POP_BLOCK        
              142  JUMP_FORWARD        184  'to 184'
            144_0  COME_FROM_FINALLY   124  '124'

 L. 710       144  DUP_TOP          
              146  LOAD_GLOBAL              Exception
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   182  'to 182'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 711       158  LOAD_FAST                'onerror'
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                lstat
              164  LOAD_FAST                'path'
              166  LOAD_GLOBAL              sys
              168  LOAD_METHOD              exc_info
              170  CALL_METHOD_0         0  ''
              172  CALL_FUNCTION_3       3  ''
              174  POP_TOP          

 L. 712       176  POP_EXCEPT       
              178  LOAD_CONST               None
              180  RETURN_VALUE     
            182_0  COME_FROM           150  '150'
              182  END_FINALLY      
            184_0  COME_FROM           142  '142'

 L. 713       184  SETUP_FINALLY       338  'to 338'

 L. 714       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              samestat
              192  LOAD_FAST                'orig_st'
              194  LOAD_GLOBAL              os
              196  LOAD_METHOD              fstat
              198  LOAD_FAST                'fd'
              200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_2         2  ''
          204_206  POP_JUMP_IF_FALSE   278  'to 278'

 L. 715       208  LOAD_GLOBAL              _rmtree_safe_fd
              210  LOAD_FAST                'fd'
              212  LOAD_FAST                'path'
              214  LOAD_FAST                'onerror'
              216  CALL_FUNCTION_3       3  ''
              218  POP_TOP          

 L. 716       220  SETUP_FINALLY       236  'to 236'

 L. 717       222  LOAD_GLOBAL              os
              224  LOAD_METHOD              rmdir
              226  LOAD_FAST                'path'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  POP_BLOCK        
              234  JUMP_FORWARD        276  'to 276'
            236_0  COME_FROM_FINALLY   220  '220'

 L. 718       236  DUP_TOP          
              238  LOAD_GLOBAL              OSError
              240  COMPARE_OP               exception-match
          242_244  POP_JUMP_IF_FALSE   274  'to 274'
              246  POP_TOP          
              248  POP_TOP          
              250  POP_TOP          

 L. 719       252  LOAD_FAST                'onerror'
              254  LOAD_GLOBAL              os
              256  LOAD_ATTR                rmdir
              258  LOAD_FAST                'path'
              260  LOAD_GLOBAL              sys
              262  LOAD_METHOD              exc_info
              264  CALL_METHOD_0         0  ''
              266  CALL_FUNCTION_3       3  ''
              268  POP_TOP          
              270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           242  '242'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM           234  '234'
              276  JUMP_FORWARD        334  'to 334'
            278_0  COME_FROM           204  '204'

 L. 721       278  SETUP_FINALLY       292  'to 292'

 L. 723       280  LOAD_GLOBAL              OSError
              282  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              284  CALL_FUNCTION_1       1  ''
              286  RAISE_VARARGS_1       1  'exception instance'
              288  POP_BLOCK        
              290  JUMP_FORWARD        334  'to 334'
            292_0  COME_FROM_FINALLY   278  '278'

 L. 724       292  DUP_TOP          
              294  LOAD_GLOBAL              OSError
              296  COMPARE_OP               exception-match
          298_300  POP_JUMP_IF_FALSE   332  'to 332'
              302  POP_TOP          
              304  POP_TOP          
              306  POP_TOP          

 L. 725       308  LOAD_FAST                'onerror'
              310  LOAD_GLOBAL              os
              312  LOAD_ATTR                path
              314  LOAD_ATTR                islink
              316  LOAD_FAST                'path'
              318  LOAD_GLOBAL              sys
              320  LOAD_METHOD              exc_info
              322  CALL_METHOD_0         0  ''
              324  CALL_FUNCTION_3       3  ''
              326  POP_TOP          
              328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           298  '298'
              332  END_FINALLY      
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           290  '290'
            334_2  COME_FROM           276  '276'
              334  POP_BLOCK        
              336  BEGIN_FINALLY    
            338_0  COME_FROM_FINALLY   184  '184'

 L. 727       338  LOAD_GLOBAL              os
              340  LOAD_METHOD              close
              342  LOAD_FAST                'fd'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  END_FINALLY      
              350  JUMP_FORWARD        430  'to 430'
            352_0  COME_FROM            44  '44'

 L. 729       352  SETUP_FINALLY       376  'to 376'

 L. 730       354  LOAD_GLOBAL              _rmtree_islink
              356  LOAD_FAST                'path'
              358  CALL_FUNCTION_1       1  ''
          360_362  POP_JUMP_IF_FALSE   372  'to 372'

 L. 732       364  LOAD_GLOBAL              OSError
              366  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              368  CALL_FUNCTION_1       1  ''
              370  RAISE_VARARGS_1       1  'exception instance'
            372_0  COME_FROM           360  '360'
              372  POP_BLOCK        
              374  JUMP_FORWARD        420  'to 420'
            376_0  COME_FROM_FINALLY   352  '352'

 L. 733       376  DUP_TOP          
              378  LOAD_GLOBAL              OSError
              380  COMPARE_OP               exception-match
          382_384  POP_JUMP_IF_FALSE   418  'to 418'
              386  POP_TOP          
              388  POP_TOP          
              390  POP_TOP          

 L. 734       392  LOAD_FAST                'onerror'
              394  LOAD_GLOBAL              os
              396  LOAD_ATTR                path
              398  LOAD_ATTR                islink
              400  LOAD_FAST                'path'
              402  LOAD_GLOBAL              sys
              404  LOAD_METHOD              exc_info
              406  CALL_METHOD_0         0  ''
              408  CALL_FUNCTION_3       3  ''
              410  POP_TOP          

 L. 736       412  POP_EXCEPT       
              414  LOAD_CONST               None
              416  RETURN_VALUE     
            418_0  COME_FROM           382  '382'
              418  END_FINALLY      
            420_0  COME_FROM           374  '374'

 L. 737       420  LOAD_GLOBAL              _rmtree_unsafe
              422  LOAD_FAST                'path'
              424  LOAD_FAST                'onerror'
              426  CALL_FUNCTION_2       2  ''
              428  RETURN_VALUE     
            430_0  COME_FROM           350  '350'

Parse error at or near `LOAD_CONST' instruction at offset 118


    rmtree.avoids_symlink_attacks = _use_fd_functions

    def _basename(path):
        sep = os.path.sep + (os.path.altsep or '')
        return os.path.basename(path.rstrip(sep))


    def move(src, dst, copy_function=copy2):
        """Recursively move a file or directory to another location. This is
    similar to the Unix "mv" command. Return the file or directory's
    destination.

    If the destination is a directory or a symlink to a directory, the source
    is moved inside the directory. The destination path must not already
    exist.

    If the destination already exists but is not a directory, it may be
    overwritten depending on os.rename() semantics.

    If the destination is on our current filesystem, then rename() is used.
    Otherwise, src is copied to the destination and then removed. Symlinks are
    recreated under the new name if os.rename() fails because of cross
    filesystem renames.

    The optional `copy_function` argument is a callable that will be used
    to copy the source or it will be delegated to `copytree`.
    By default, copy2() is used, but any function that supports the same
    signature (like copy()) can be used.

    A lot more could be done here...  A look at a mv.c shows a lot of
    the issues this implementation glosses over.

    """
        sys.audit('shutil.move', src, dst)
        real_dst = dst
        if os.path.isdir(dst):
            if _samefile(src, dst):
                os.rename(src, dst)
                return None
            real_dst = os.path.join(dst, _basename(src))
            if os.path.exists(real_dst):
                raise Error("Destination path '%s' already exists" % real_dst)
        try:
            os.rename(src, real_dst)
        except OSError:
            if os.path.islink(src):
                linkto = os.readlink(src)
                os.symlink(linkto, real_dst)
                os.unlink(src)
            else:
                if os.path.isdir(src):
                    if _destinsrc(src, dst):
                        raise Error("Cannot move a directory '%s' into itself '%s'." % (
                         src, dst))
                    copytree(src, real_dst, copy_function=copy_function, symlinks=True)
                    rmtree(src)
                else:
                    copy_function(src, real_dst)
                    os.unlink(src)
        else:
            return real_dst


    def _destinsrc(src, dst):
        src = os.path.abspath(src)
        dst = os.path.abspath(dst)
        if not src.endswith(os.path.sep):
            src += os.path.sep
        if not dst.endswith(os.path.sep):
            dst += os.path.sep
        return dst.startswith(src)


    def _get_gid(name):
        """Returns a gid, given a group name."""
        if getgrnam is None or name is None:
            return
        try:
            result = getgrnam(name)
        except KeyError:
            result = None
        else:
            if result is not None:
                return result[2]


    def _get_uid(name):
        """Returns an uid, given a user name."""
        if getpwnam is None or name is None:
            return
        try:
            result = getpwnam(name)
        except KeyError:
            result = None
        else:
            if result is not None:
                return result[2]


    def _make_tarball(base_name, base_dir, compress='gzip', verbose=0, dry_run=0, owner=None, group=None, logger=None):
        """Create a (possibly compressed) tar file from all the files under
    'base_dir'.

    'compress' must be "gzip" (the default), "bzip2", "xz", or None.

    'owner' and 'group' can be used to define an owner and a group for the
    archive that is being built. If not provided, the current owner and group
    will be used.

    The output tar file will be named 'base_name' +  ".tar", possibly plus
    the appropriate compression extension (".gz", ".bz2", or ".xz").

    Returns the output filename.
    """
        if compress is None:
            tar_compression = ''
        else:
            if _ZLIB_SUPPORTED and compress == 'gzip':
                tar_compression = 'gz'
            else:
                if _BZ2_SUPPORTED and compress == 'bzip2':
                    tar_compression = 'bz2'
                else:
                    if _LZMA_SUPPORTED:
                        if compress == 'xz':
                            tar_compression = 'xz'
                        else:
                            raise ValueError("bad value for 'compress', or compression format not supported : {0}".format(compress))
                    else:
                        import tarfile
                        compress_ext = '.' + tar_compression if compress else ''
                        archive_name = base_name + '.tar' + compress_ext
                        archive_dir = os.path.dirname(archive_name)
                        if archive_dir:
                            if not os.path.exists(archive_dir):
                                if logger is not None:
                                    logger.info('creating %s', archive_dir)
                                if not dry_run:
                                    os.makedirs(archive_dir)
                        if logger is not None:
                            logger.info('Creating tar archive')
                        uid = _get_uid(owner)
                        gid = _get_gid(group)

                        def _set_uid_gid(tarinfo):
                            if gid is not None:
                                tarinfo.gid = gid
                                tarinfo.gname = group
                            if uid is not None:
                                tarinfo.uid = uid
                                tarinfo.uname = owner
                            return tarinfo

                        tar = dry_run or tarfile.open(archive_name, 'w|%s' % tar_compression)
                        try:
                            tar.add(base_dir, filter=_set_uid_gid)
                        finally:
                            tar.close()

                    return archive_name


    def _make_zipfile(base_name, base_dir, verbose=0, dry_run=0, logger=None):
        """Create a zip file from all the files under 'base_dir'.

    The output zip file will be named 'base_name' + ".zip".  Returns the
    name of the output zip file.
    """
        import zipfile
        zip_filename = base_name + '.zip'
        archive_dir = os.path.dirname(base_name)
        if archive_dir:
            if not os.path.exists(archive_dir):
                if logger is not None:
                    logger.info('creating %s', archive_dir)
                if not dry_run:
                    os.makedirs(archive_dir)
        if logger is not None:
            logger.info("creating '%s' and adding '%s' to it", zip_filename, base_dir)
        if not dry_run:
            with zipfile.ZipFile(zip_filename, 'w', compression=(zipfile.ZIP_DEFLATED)) as (zf):
                path = os.path.normpath(base_dir)
                if path != os.curdir:
                    zf.write(path, path)
                    if logger is not None:
                        logger.info("adding '%s'", path)
                for dirpath, dirnames, filenames in os.walk(base_dir):
                    for name in sorted(dirnames):
                        path = os.path.normpath(os.path.join(dirpath, name))
                        zf.write(path, path)
                        if logger is not None:
                            logger.info("adding '%s'", path)

                else:
                    for name in filenames:
                        path = os.path.normpath(os.path.join(dirpath, name))
                        if os.path.isfile(path):
                            zf.write(path, path)
                            if logger is not None:
                                logger.info("adding '%s'", path)

        return zip_filename


    _ARCHIVE_FORMATS = {'tar': (_make_tarball, [('compress', None)], 'uncompressed tar file')}
    if _ZLIB_SUPPORTED:
        _ARCHIVE_FORMATS['gztar'] = (
         _make_tarball, [('compress', 'gzip')],
         "gzip'ed tar-file")
        _ARCHIVE_FORMATS['zip'] = (_make_zipfile, [], 'ZIP file')
    if _BZ2_SUPPORTED:
        _ARCHIVE_FORMATS['bztar'] = (
         _make_tarball, [('compress', 'bzip2')],
         "bzip2'ed tar-file")
    if _LZMA_SUPPORTED:
        _ARCHIVE_FORMATS['xztar'] = (
         _make_tarball, [('compress', 'xz')],
         "xz'ed tar-file")

    def get_archive_formats():
        """Returns a list of supported formats for archiving and unarchiving.

    Each element of the returned sequence is a tuple (name, description)
    """
        formats = [(
         name, registry[2]) for name, registry in _ARCHIVE_FORMATS.items()]
        formats.sort()
        return formats


    def register_archive_format(name, function, extra_args=None, description=''):
        """Registers an archive format.

    name is the name of the format. function is the callable that will be
    used to create archives. If provided, extra_args is a sequence of
    (name, value) tuples that will be passed as arguments to the callable.
    description can be provided to describe the format, and will be returned
    by the get_archive_formats() function.
    """
        if extra_args is None:
            extra_args = []
        else:
            if not callable(function):
                raise TypeError('The %s object is not callable' % function)
            assert isinstance(extra_args, (tuple, list)), 'extra_args needs to be a sequence'
        for element in extra_args:
            if not isinstance(element, (tuple, list)) or len(element) != 2:
                raise TypeError('extra_args elements are : (arg_name, value)')
        else:
            _ARCHIVE_FORMATS[name] = (
             function, extra_args, description)


    def unregister_archive_format(name):
        del _ARCHIVE_FORMATS[name]


    def make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None):
        """Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", or "xztar".  Or any other registered format.

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
        sys.audit('shutil.make_archive', base_name, format, root_dir, base_dir)
        save_cwd = os.getcwd()
        if root_dir is not None:
            if logger is not None:
                logger.debug("changing into '%s'", root_dir)
            base_name = os.path.abspath(base_name)
            if not dry_run:
                os.chdir(root_dir)
        if base_dir is None:
            base_dir = os.curdir
        kwargs = {'dry_run':dry_run,  'logger':logger}
        try:
            format_info = _ARCHIVE_FORMATS[format]
        except KeyError:
            raise ValueError("unknown archive format '%s'" % format) from None
        else:
            func = format_info[0]
            for arg, val in format_info[1]:
                kwargs[arg] = val
            else:
                if format != 'zip':
                    kwargs['owner'] = owner
                    kwargs['group'] = group
                try:
                    filename = func(base_name, base_dir, **kwargs)
                finally:
                    if root_dir is not None:
                        if logger is not None:
                            logger.debug("changing back to '%s'", save_cwd)
                        os.chdir(save_cwd)

                return filename


    def get_unpack_formats():
        """Returns a list of supported formats for unpacking.

    Each element of the returned sequence is a tuple
    (name, extensions, description)
    """
        formats = [(
         name, info[0], info[3]) for name, info in _UNPACK_FORMATS.items()]
        formats.sort()
        return formats


    def _check_unpack_options(extensions, function, extra_args):
        """Checks what gets registered as an unpacker."""
        existing_extensions = {}
        for name, info in _UNPACK_FORMATS.items():
            for ext in info[0]:
                existing_extensions[ext] = name

        else:
            for extension in extensions:
                if extension in existing_extensions:
                    msg = '%s is already registered for "%s"'
                    raise RegistryError(msg % (extension,
                     existing_extensions[extension]))
            else:
                if not callable(function):
                    raise TypeError('The registered function must be a callable')


    def register_unpack_format(name, extensions, function, extra_args=None, description=''):
        """Registers an unpack format.

    `name` is the name of the format. `extensions` is a list of extensions
    corresponding to the format.

    `function` is the callable that will be
    used to unpack archives. The callable will receive archives to unpack.
    If it's unable to handle an archive, it needs to raise a ReadError
    exception.

    If provided, `extra_args` is a sequence of
    (name, value) tuples that will be passed as arguments to the callable.
    description can be provided to describe the format, and will be returned
    by the get_unpack_formats() function.
    """
        if extra_args is None:
            extra_args = []
        _check_unpack_options(extensions, function, extra_args)
        _UNPACK_FORMATS[name] = (extensions, function, extra_args, description)


    def unregister_unpack_format(name):
        """Removes the pack format from the registry."""
        del _UNPACK_FORMATS[name]


    def _ensure_directory(path):
        """Ensure that the parent directory of `path` exists"""
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)


    def _unpack_zipfile(filename, extract_dir):
        """Unpack zip `filename` to `extract_dir`
    """
        import zipfile
        if not zipfile.is_zipfile(filename):
            raise ReadError('%s is not a zip file' % filename)
        zip = zipfile.ZipFile(filename)
        try:
            for info in zip.infolist():
                name = info.filename

            if not name.startswith('/'):
                if '..' in name:
                    pass
                else:
                    target = (os.path.join)(extract_dir, *name.split('/'))
                    if not target:
                        pass
                    else:
                        _ensure_directory(target)
                        if not name.endswith('/'):
                            data = zip.read(info.filename)
                            f = open(target, 'wb')
                            try:
                                f.write(data)
                            finally:
                                f.close()
                                del data

        finally:
            zip.close()


    def _unpack_tarfile(filename, extract_dir):
        """Unpack tar/tar.gz/tar.bz2/tar.xz `filename` to `extract_dir`
    """
        import tarfile
        try:
            tarobj = tarfile.open(filename)
        except tarfile.TarError:
            raise ReadError('%s is not a compressed or uncompressed tar file' % filename)
        else:
            try:
                tarobj.extractall(extract_dir)
            finally:
                tarobj.close()


    _UNPACK_FORMATS = {'tar':(['.tar'], _unpack_tarfile, [], 'uncompressed tar file'),  'zip':(
      [
       '.zip'], _unpack_zipfile, [], 'ZIP file')}
    if _ZLIB_SUPPORTED:
        _UNPACK_FORMATS['gztar'] = (
         [
          '.tar.gz', '.tgz'], _unpack_tarfile, [],
         "gzip'ed tar-file")
    if _BZ2_SUPPORTED:
        _UNPACK_FORMATS['bztar'] = (
         [
          '.tar.bz2', '.tbz2'], _unpack_tarfile, [],
         "bzip2'ed tar-file")
    if _LZMA_SUPPORTED:
        _UNPACK_FORMATS['xztar'] = (
         [
          '.tar.xz', '.txz'], _unpack_tarfile, [],
         "xz'ed tar-file")

    def _find_unpack_format(filename):
        for name, info in _UNPACK_FORMATS.items():
            for extension in info[0]:
                if filename.endswith(extension):
                    return name


    def unpack_archive(filename, extract_dir=None, format=None):
        """Unpack an archive.

    `filename` is the name of the archive.

    `extract_dir` is the name of the target directory, where the archive
    is unpacked. If not provided, the current working directory is used.

    `format` is the archive format: one of "zip", "tar", "gztar", "bztar",
    or "xztar".  Or any other registered format.  If not provided,
    unpack_archive will use the filename extension and see if an unpacker
    was registered for that extension.

    In case none is found, a ValueError is raised.
    """
        sys.audit('shutil.unpack_archive', filename, extract_dir, format)
        if extract_dir is None:
            extract_dir = os.getcwd()
        else:
            extract_dir = os.fspath(extract_dir)
            filename = os.fspath(filename)
            if format is not None:
                try:
                    format_info = _UNPACK_FORMATS[format]
                except KeyError:
                    raise ValueError("Unknown unpack format '{0}'".format(format)) from None
                else:
                    func = format_info[1]
                    func(filename, extract_dir, **dict(format_info[2]))
            else:
                format = _find_unpack_format(filename)
                if format is None:
                    raise ReadError("Unknown archive format '{0}'".format(filename))
            func = _UNPACK_FORMATS[format][1]
            kwargs = dict(_UNPACK_FORMATS[format][2])
            func(filename, extract_dir, **kwargs)


if hasattr(os, 'statvfs'):
    __all__.append('disk_usage')
    _ntuple_diskusage = collections.namedtuple('usage', 'total used free')
    _ntuple_diskusage.total.__doc__ = 'Total space in bytes'
    _ntuple_diskusage.used.__doc__ = 'Used space in bytes'
    _ntuple_diskusage.free.__doc__ = 'Free space in bytes'

    def disk_usage(path):
        """Return disk usage statistics about the given path.

        Returned value is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)


else:
    if _WINDOWS:
        __all__.append('disk_usage')
        _ntuple_diskusage = collections.namedtuple('usage', 'total used free')

        def disk_usage(path):
            """Return disk usage statistics about the given path.

        Returned values is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
            total, free = nt._getdiskusage(path)
            used = total - free
            return _ntuple_diskusage(total, used, free)


    def chown(path, user=None, group=None):
        """Change owner user and group of the given path.

    user and group can be the uid/gid or the user/group names, and in that case,
    they are converted to their respective uid/gid.
    """
        sys.audit('shutil.chown', path, user, group)
        if user is None:
            if group is None:
                raise ValueError('user and/or group must be set')
        _user = user
        _group = group
        if user is None:
            _user = -1
        else:
            if isinstance(user, str):
                _user = _get_uid(user)
                if _user is None:
                    raise LookupError('no such user: {!r}'.format(user))
            elif group is None:
                _group = -1
            else:
                if not isinstance(group, int):
                    _group = _get_gid(group)
                    if _group is None:
                        raise LookupError('no such group: {!r}'.format(group))
            os.chown(path, _user, _group)


    def get_terminal_size(fallback=(80, 24)):
        """Get the size of the terminal window.

    For each of the two dimensions, the environment variable, COLUMNS
    and LINES respectively, is checked. If the variable is defined and
    the value is a positive integer, it is used.

    When COLUMNS or LINES is not defined, which is the common case,
    the terminal connected to sys.__stdout__ is queried
    by invoking os.get_terminal_size.

    If the terminal size cannot be successfully queried, either because
    the system doesn't support querying, or because we are not
    connected to a terminal, the value given in fallback parameter
    is used. Fallback defaults to (80, 24) which is the default
    size used by many terminal emulators.

    The value returned is a named tuple of type os.terminal_size.
    """
        try:
            columns = int(os.environ['COLUMNS'])
        except (KeyError, ValueError):
            columns = 0
        else:
            try:
                lines = int(os.environ['LINES'])
            except (KeyError, ValueError):
                lines = 0
            else:
                if columns <= 0 or lines <= 0:
                    try:
                        size = os.get_terminal_size(sys.__stdout__.fileno())
                    except (AttributeError, ValueError, OSError):
                        size = os.terminal_size(fallback)
                    else:
                        if columns <= 0:
                            columns = size.columns
                        if lines <= 0:
                            lines = size.lines
                return os.terminal_size((columns, lines))


    def _access_check(fn, mode):
        return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)


    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return
            use_bytes = isinstance(cmd, bytes)
            if path is None:
                path = os.environ.get('PATH', None)
                if path is None:
                    try:
                        path = os.confstr('CS_PATH')
                    except (AttributeError, ValueError):
                        path = os.defpath

            if not path:
                return
        else:
            if use_bytes:
                path = os.fsencode(path)
                path = path.split(os.fsencode(os.pathsep))
            else:
                path = os.fsdecode(path)
                path = path.split(os.pathsep)
            if sys.platform == 'win32':
                curdir = os.curdir
                if use_bytes:
                    curdir = os.fsencode(curdir)
                else:
                    if curdir not in path:
                        path.insert(0, curdir)
                    pathext = os.environ.get('PATHEXT', '').split(os.pathsep)
                    if use_bytes:
                        pathext = [os.fsencode(ext) for ext in pathext]
                    if any((cmd.lower().endswith(ext.lower()) for ext in pathext)):
                        files = [
                         cmd]
                    else:
                        files = [cmd + ext for ext in pathext]
            else:
                files = [
                 cmd]
        seen = set
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name