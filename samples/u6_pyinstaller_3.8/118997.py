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

 L. 238         0  LOAD_GLOBAL              _samefile
                2  LOAD_FAST                'src'
                4  LOAD_FAST                'dst'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 239        10  LOAD_GLOBAL              SameFileError
               12  LOAD_STR                 '{!r} and {!r} are the same file'
               14  LOAD_METHOD              format
               16  LOAD_FAST                'src'
               18  LOAD_FAST                'dst'
               20  CALL_METHOD_2         2  ''
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 241        26  LOAD_CONST               0
               28  STORE_FAST               'file_size'

 L. 242        30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'src'
               34  LOAD_FAST                'dst'
               36  BUILD_LIST_2          2 
               38  CALL_FUNCTION_1       1  ''
               40  GET_ITER         
             42_0  COME_FROM           140  '140'
             42_1  COME_FROM           132  '132'
               42  FOR_ITER            150  'to 150'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'i'
               48  STORE_FAST               'fn'

 L. 243        50  SETUP_FINALLY        64  'to 64'

 L. 244        52  LOAD_GLOBAL              _stat
               54  LOAD_FAST                'fn'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'st'
               60  POP_BLOCK        
               62  JUMP_FORWARD         84  'to 84'
             64_0  COME_FROM_FINALLY    50  '50'

 L. 245        64  DUP_TOP          
               66  LOAD_GLOBAL              OSError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    82  'to 82'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 247        78  POP_EXCEPT       
               80  JUMP_BACK            42  'to 42'
             82_0  COME_FROM            70  '70'
               82  END_FINALLY      
             84_0  COME_FROM            62  '62'

 L. 250        84  LOAD_GLOBAL              stat
               86  LOAD_METHOD              S_ISFIFO
               88  LOAD_FAST                'st'
               90  LOAD_ATTR                st_mode
               92  CALL_METHOD_1         1  ''
               94  POP_JUMP_IF_FALSE   130  'to 130'

 L. 251        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'fn'
              100  LOAD_GLOBAL              os
              102  LOAD_ATTR                DirEntry
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   114  'to 114'
              108  LOAD_FAST                'fn'
              110  LOAD_ATTR                path
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM           106  '106'
              114  LOAD_FAST                'fn'
            116_0  COME_FROM           112  '112'
              116  STORE_FAST               'fn'

 L. 252       118  LOAD_GLOBAL              SpecialFileError
              120  LOAD_STR                 '`%s` is a named pipe'
              122  LOAD_FAST                'fn'
              124  BINARY_MODULO    
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM            94  '94'

 L. 253       130  LOAD_GLOBAL              _WINDOWS
              132  POP_JUMP_IF_FALSE    42  'to 42'
              134  LOAD_FAST                'i'
              136  LOAD_CONST               0
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE    42  'to 42'

 L. 254       142  LOAD_FAST                'st'
              144  LOAD_ATTR                st_size
              146  STORE_FAST               'file_size'
              148  JUMP_BACK            42  'to 42'

 L. 256       150  LOAD_FAST                'follow_symlinks'
              152  POP_JUMP_IF_TRUE    184  'to 184'
              154  LOAD_GLOBAL              _islink
              156  LOAD_FAST                'src'
              158  CALL_FUNCTION_1       1  ''
              160  POP_JUMP_IF_FALSE   184  'to 184'

 L. 257       162  LOAD_GLOBAL              os
              164  LOAD_METHOD              symlink
              166  LOAD_GLOBAL              os
              168  LOAD_METHOD              readlink
              170  LOAD_FAST                'src'
              172  CALL_METHOD_1         1  ''
              174  LOAD_FAST                'dst'
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          
          180_182  JUMP_FORWARD        450  'to 450'
            184_0  COME_FROM           160  '160'
            184_1  COME_FROM           152  '152'

 L. 259       184  LOAD_GLOBAL              open
              186  LOAD_FAST                'src'
              188  LOAD_STR                 'rb'
              190  CALL_FUNCTION_2       2  ''
          192_194  SETUP_WITH          444  'to 444'
              196  STORE_FAST               'fsrc'
              198  LOAD_GLOBAL              open
              200  LOAD_FAST                'dst'
              202  LOAD_STR                 'wb'
              204  CALL_FUNCTION_2       2  ''
              206  SETUP_WITH          434  'to 434'
              208  STORE_FAST               'fdst'

 L. 261       210  LOAD_GLOBAL              _HAS_FCOPYFILE
          212_214  POP_JUMP_IF_FALSE   286  'to 286'

 L. 262       216  SETUP_FINALLY       262  'to 262'

 L. 263       218  LOAD_GLOBAL              _fastcopy_fcopyfile
              220  LOAD_FAST                'fsrc'
              222  LOAD_FAST                'fdst'
              224  LOAD_GLOBAL              posix
              226  LOAD_ATTR                _COPYFILE_DATA
              228  CALL_FUNCTION_3       3  ''
              230  POP_TOP          

 L. 264       232  LOAD_FAST                'dst'
              234  POP_BLOCK        
              236  POP_BLOCK        
              238  ROT_TWO          
              240  BEGIN_FINALLY    
              242  WITH_CLEANUP_START
              244  WITH_CLEANUP_FINISH
              246  POP_FINALLY           0  ''
              248  POP_BLOCK        
              250  ROT_TWO          
              252  BEGIN_FINALLY    
              254  WITH_CLEANUP_START
              256  WITH_CLEANUP_FINISH
              258  POP_FINALLY           0  ''
              260  RETURN_VALUE     
            262_0  COME_FROM_FINALLY   216  '216'

 L. 265       262  DUP_TOP          
              264  LOAD_GLOBAL              _GiveupOnFastCopy
              266  COMPARE_OP               exception-match
          268_270  POP_JUMP_IF_FALSE   282  'to 282'
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 266       278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           268  '268'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
              284  JUMP_FORWARD        420  'to 420'
            286_0  COME_FROM           212  '212'

 L. 268       286  LOAD_GLOBAL              _USE_CP_SENDFILE
          288_290  POP_JUMP_IF_FALSE   358  'to 358'

 L. 269       292  SETUP_FINALLY       334  'to 334'

 L. 270       294  LOAD_GLOBAL              _fastcopy_sendfile
              296  LOAD_FAST                'fsrc'
              298  LOAD_FAST                'fdst'
              300  CALL_FUNCTION_2       2  ''
              302  POP_TOP          

 L. 271       304  LOAD_FAST                'dst'
              306  POP_BLOCK        
              308  POP_BLOCK        
              310  ROT_TWO          
              312  BEGIN_FINALLY    
              314  WITH_CLEANUP_START
              316  WITH_CLEANUP_FINISH
              318  POP_FINALLY           0  ''
              320  POP_BLOCK        
              322  ROT_TWO          
              324  BEGIN_FINALLY    
              326  WITH_CLEANUP_START
              328  WITH_CLEANUP_FINISH
              330  POP_FINALLY           0  ''
              332  RETURN_VALUE     
            334_0  COME_FROM_FINALLY   292  '292'

 L. 272       334  DUP_TOP          
              336  LOAD_GLOBAL              _GiveupOnFastCopy
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   354  'to 354'
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 273       350  POP_EXCEPT       
              352  JUMP_FORWARD        356  'to 356'
            354_0  COME_FROM           340  '340'
              354  END_FINALLY      
            356_0  COME_FROM           352  '352'
              356  JUMP_FORWARD        420  'to 420'
            358_0  COME_FROM           288  '288'

 L. 276       358  LOAD_GLOBAL              _WINDOWS
          360_362  POP_JUMP_IF_FALSE   420  'to 420'
              364  LOAD_FAST                'file_size'
              366  LOAD_CONST               0
              368  COMPARE_OP               >
          370_372  POP_JUMP_IF_FALSE   420  'to 420'

 L. 277       374  LOAD_GLOBAL              _copyfileobj_readinto
              376  LOAD_FAST                'fsrc'
              378  LOAD_FAST                'fdst'
              380  LOAD_GLOBAL              min
              382  LOAD_FAST                'file_size'
              384  LOAD_GLOBAL              COPY_BUFSIZE
              386  CALL_FUNCTION_2       2  ''
              388  CALL_FUNCTION_3       3  ''
              390  POP_TOP          

 L. 278       392  LOAD_FAST                'dst'
              394  POP_BLOCK        
              396  ROT_TWO          
              398  BEGIN_FINALLY    
              400  WITH_CLEANUP_START
              402  WITH_CLEANUP_FINISH
              404  POP_FINALLY           0  ''
              406  POP_BLOCK        
              408  ROT_TWO          
              410  BEGIN_FINALLY    
              412  WITH_CLEANUP_START
              414  WITH_CLEANUP_FINISH
              416  POP_FINALLY           0  ''
              418  RETURN_VALUE     
            420_0  COME_FROM           370  '370'
            420_1  COME_FROM           360  '360'
            420_2  COME_FROM           356  '356'
            420_3  COME_FROM           284  '284'

 L. 280       420  LOAD_GLOBAL              copyfileobj
              422  LOAD_FAST                'fsrc'
              424  LOAD_FAST                'fdst'
              426  CALL_FUNCTION_2       2  ''
              428  POP_TOP          
              430  POP_BLOCK        
              432  BEGIN_FINALLY    
            434_0  COME_FROM_WITH      206  '206'
              434  WITH_CLEANUP_START
              436  WITH_CLEANUP_FINISH
              438  END_FINALLY      
              440  POP_BLOCK        
              442  BEGIN_FINALLY    
            444_0  COME_FROM_WITH      192  '192'
              444  WITH_CLEANUP_START
              446  WITH_CLEANUP_FINISH
              448  END_FINALLY      
            450_0  COME_FROM           180  '180'

 L. 282       450  LOAD_FAST                'dst'
              452  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 236


        def copymode(src, dst, *, follow_symlinks=True):
            """Copy mode bits from src to dst.

    If follow_symlinks is not set, symlinks aren't followed if and only
    if both `src` and `dst` are symlinks.  If `lchmod` isn't available
    (e.g. Linux) this method does nothing.

    """
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

 L. 313         0  SETUP_FINALLY        20  'to 20'

 L. 314         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                listxattr
                6  LOAD_FAST                'src'
                8  LOAD_FAST                'follow_symlinks'
               10  LOAD_CONST               ('follow_symlinks',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'names'
               16  POP_BLOCK        
               18  JUMP_FORWARD         84  'to 84'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 315        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    82  'to 82'
               28  POP_TOP          
               30  STORE_FAST               'e'
               32  POP_TOP          
               34  SETUP_FINALLY        70  'to 70'

 L. 316        36  LOAD_FAST                'e'
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

 L. 317        58  RAISE_VARARGS_0       0  'reraise'
             60_0  COME_FROM            56  '56'

 L. 318        60  POP_BLOCK        
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

 L. 319        84  LOAD_FAST                'names'
               86  GET_ITER         
               88  FOR_ITER            196  'to 196'
               90  STORE_FAST               'name'

 L. 320        92  SETUP_FINALLY       132  'to 132'

 L. 321        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                getxattr
               98  LOAD_FAST                'src'
              100  LOAD_FAST                'name'
              102  LOAD_FAST                'follow_symlinks'
              104  LOAD_CONST               ('follow_symlinks',)
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  STORE_FAST               'value'

 L. 322       110  LOAD_GLOBAL              os
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

 L. 323       132  DUP_TOP          
              134  LOAD_GLOBAL              OSError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   192  'to 192'
              140  POP_TOP          
              142  STORE_FAST               'e'
              144  POP_TOP          
              146  SETUP_FINALLY       180  'to 180'

 L. 324       148  LOAD_FAST                'e'
              150  LOAD_ATTR                errno
              152  LOAD_GLOBAL              errno
              154  LOAD_ATTR                EPERM
              156  LOAD_GLOBAL              errno
              158  LOAD_ATTR                ENOTSUP
              160  LOAD_GLOBAL              errno
              162  LOAD_ATTR                ENODATA

 L. 325       164  LOAD_GLOBAL              errno
              166  LOAD_ATTR                EINVAL

 L. 324       168  BUILD_TUPLE_4         4 
              170  COMPARE_OP               not-in
              172  POP_JUMP_IF_FALSE   176  'to 176'

 L. 326       174  RAISE_VARARGS_0       0  'reraise'
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

 L. 444         0  LOAD_FAST                'ignore'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L. 445         8  LOAD_FAST                'ignore'
               10  LOAD_FAST                'src'
               12  LOAD_SETCOMP             '<code_object <setcomp>>'
               14  LOAD_STR                 '_copytree.<locals>.<setcomp>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_FAST                'entries'
               20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'ignored_names'
               28  JUMP_FORWARD         36  'to 36'
             30_0  COME_FROM             6  '6'

 L. 447        30  LOAD_GLOBAL              set
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'ignored_names'
             36_0  COME_FROM            28  '28'

 L. 449        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                makedirs
               40  LOAD_FAST                'dst'
               42  LOAD_FAST                'dirs_exist_ok'
               44  LOAD_CONST               ('exist_ok',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  POP_TOP          

 L. 450        50  BUILD_LIST_0          0 
               52  STORE_FAST               'errors'

 L. 451        54  LOAD_FAST                'copy_function'
               56  LOAD_GLOBAL              copy2
               58  COMPARE_OP               is
               60  JUMP_IF_TRUE_OR_POP    68  'to 68'
               62  LOAD_FAST                'copy_function'
               64  LOAD_GLOBAL              copy
               66  COMPARE_OP               is
             68_0  COME_FROM            60  '60'
               68  STORE_FAST               'use_srcentry'

 L. 453        70  LOAD_FAST                'entries'
               72  GET_ITER         
            74_76  FOR_ITER            460  'to 460'
               78  STORE_FAST               'srcentry'

 L. 454        80  LOAD_FAST                'srcentry'
               82  LOAD_ATTR                name
               84  LOAD_FAST                'ignored_names'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE    92  'to 92'

 L. 455        90  JUMP_BACK            74  'to 74'
             92_0  COME_FROM            88  '88'

 L. 456        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              join
               98  LOAD_FAST                'src'
              100  LOAD_FAST                'srcentry'
              102  LOAD_ATTR                name
              104  CALL_METHOD_2         2  ''
              106  STORE_FAST               'srcname'

 L. 457       108  LOAD_GLOBAL              os
              110  LOAD_ATTR                path
              112  LOAD_METHOD              join
              114  LOAD_FAST                'dst'
              116  LOAD_FAST                'srcentry'
              118  LOAD_ATTR                name
              120  CALL_METHOD_2         2  ''
              122  STORE_FAST               'dstname'

 L. 458       124  LOAD_FAST                'use_srcentry'
              126  POP_JUMP_IF_FALSE   132  'to 132'
              128  LOAD_FAST                'srcentry'
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM           126  '126'
              132  LOAD_FAST                'srcname'
            134_0  COME_FROM           130  '130'
              134  STORE_FAST               'srcobj'

 L. 459       136  SETUP_FINALLY       352  'to 352'

 L. 460       138  LOAD_FAST                'srcentry'
              140  LOAD_METHOD              is_symlink
              142  CALL_METHOD_0         0  ''
              144  STORE_FAST               'is_symlink'

 L. 461       146  LOAD_FAST                'is_symlink'
              148  POP_JUMP_IF_FALSE   188  'to 188'
              150  LOAD_GLOBAL              os
              152  LOAD_ATTR                name
              154  LOAD_STR                 'nt'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   188  'to 188'

 L. 464       160  LOAD_FAST                'srcentry'
              162  LOAD_ATTR                stat
              164  LOAD_CONST               False
              166  LOAD_CONST               ('follow_symlinks',)
              168  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              170  STORE_FAST               'lstat'

 L. 465       172  LOAD_FAST                'lstat'
              174  LOAD_ATTR                st_reparse_tag
              176  LOAD_GLOBAL              stat
              178  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 466       184  LOAD_CONST               False
              186  STORE_FAST               'is_symlink'
            188_0  COME_FROM           182  '182'
            188_1  COME_FROM           158  '158'
            188_2  COME_FROM           148  '148'

 L. 467       188  LOAD_FAST                'is_symlink'
          190_192  POP_JUMP_IF_FALSE   306  'to 306'

 L. 468       194  LOAD_GLOBAL              os
              196  LOAD_METHOD              readlink
              198  LOAD_FAST                'srcname'
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'linkto'

 L. 469       204  LOAD_FAST                'symlinks'
              206  POP_JUMP_IF_FALSE   238  'to 238'

 L. 473       208  LOAD_GLOBAL              os
              210  LOAD_METHOD              symlink
              212  LOAD_FAST                'linkto'
              214  LOAD_FAST                'dstname'
              216  CALL_METHOD_2         2  ''
              218  POP_TOP          

 L. 474       220  LOAD_GLOBAL              copystat
              222  LOAD_FAST                'srcobj'
              224  LOAD_FAST                'dstname'
              226  LOAD_FAST                'symlinks'
              228  UNARY_NOT        
              230  LOAD_CONST               ('follow_symlinks',)
              232  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              234  POP_TOP          
              236  JUMP_FORWARD        304  'to 304'
            238_0  COME_FROM           206  '206'

 L. 477       238  LOAD_GLOBAL              os
              240  LOAD_ATTR                path
              242  LOAD_METHOD              exists
              244  LOAD_FAST                'linkto'
              246  CALL_METHOD_1         1  ''
          248_250  POP_JUMP_IF_TRUE    262  'to 262'
              252  LOAD_FAST                'ignore_dangling_symlinks'
          254_256  POP_JUMP_IF_FALSE   262  'to 262'

 L. 478       258  POP_BLOCK        
              260  JUMP_BACK            74  'to 74'
            262_0  COME_FROM           254  '254'
            262_1  COME_FROM           248  '248'

 L. 480       262  LOAD_FAST                'srcentry'
              264  LOAD_METHOD              is_dir
              266  CALL_METHOD_0         0  ''
          268_270  POP_JUMP_IF_FALSE   294  'to 294'

 L. 481       272  LOAD_GLOBAL              copytree
              274  LOAD_FAST                'srcobj'
              276  LOAD_FAST                'dstname'
              278  LOAD_FAST                'symlinks'
              280  LOAD_FAST                'ignore'

 L. 482       282  LOAD_FAST                'copy_function'

 L. 482       284  LOAD_FAST                'dirs_exist_ok'

 L. 481       286  LOAD_CONST               ('dirs_exist_ok',)
              288  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              290  POP_TOP          
              292  JUMP_FORWARD        304  'to 304'
            294_0  COME_FROM           268  '268'

 L. 484       294  LOAD_FAST                'copy_function'
              296  LOAD_FAST                'srcobj'
              298  LOAD_FAST                'dstname'
              300  CALL_FUNCTION_2       2  ''
              302  POP_TOP          
            304_0  COME_FROM           292  '292'
            304_1  COME_FROM           236  '236'
              304  JUMP_FORWARD        348  'to 348'
            306_0  COME_FROM           190  '190'

 L. 485       306  LOAD_FAST                'srcentry'
              308  LOAD_METHOD              is_dir
              310  CALL_METHOD_0         0  ''
          312_314  POP_JUMP_IF_FALSE   338  'to 338'

 L. 486       316  LOAD_GLOBAL              copytree
              318  LOAD_FAST                'srcobj'
              320  LOAD_FAST                'dstname'
              322  LOAD_FAST                'symlinks'
              324  LOAD_FAST                'ignore'
              326  LOAD_FAST                'copy_function'

 L. 487       328  LOAD_FAST                'dirs_exist_ok'

 L. 486       330  LOAD_CONST               ('dirs_exist_ok',)
              332  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              334  POP_TOP          
              336  JUMP_FORWARD        348  'to 348'
            338_0  COME_FROM           312  '312'

 L. 490       338  LOAD_FAST                'copy_function'
              340  LOAD_FAST                'srcobj'
              342  LOAD_FAST                'dstname'
              344  CALL_FUNCTION_2       2  ''
              346  POP_TOP          
            348_0  COME_FROM           336  '336'
            348_1  COME_FROM           304  '304'
              348  POP_BLOCK        
              350  JUMP_BACK            74  'to 74'
            352_0  COME_FROM_FINALLY   136  '136'

 L. 493       352  DUP_TOP          
              354  LOAD_GLOBAL              Error
              356  COMPARE_OP               exception-match
          358_360  POP_JUMP_IF_FALSE   402  'to 402'
              362  POP_TOP          
              364  STORE_FAST               'err'
              366  POP_TOP          
              368  SETUP_FINALLY       390  'to 390'

 L. 494       370  LOAD_FAST                'errors'
              372  LOAD_METHOD              extend
              374  LOAD_FAST                'err'
              376  LOAD_ATTR                args
              378  LOAD_CONST               0
              380  BINARY_SUBSCR    
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          
              386  POP_BLOCK        
              388  BEGIN_FINALLY    
            390_0  COME_FROM_FINALLY   368  '368'
              390  LOAD_CONST               None
              392  STORE_FAST               'err'
              394  DELETE_FAST              'err'
              396  END_FINALLY      
              398  POP_EXCEPT       
              400  JUMP_BACK            74  'to 74'
            402_0  COME_FROM           358  '358'

 L. 495       402  DUP_TOP          
              404  LOAD_GLOBAL              OSError
              406  COMPARE_OP               exception-match
          408_410  POP_JUMP_IF_FALSE   456  'to 456'
              412  POP_TOP          
              414  STORE_FAST               'why'
              416  POP_TOP          
              418  SETUP_FINALLY       444  'to 444'

 L. 496       420  LOAD_FAST                'errors'
              422  LOAD_METHOD              append
              424  LOAD_FAST                'srcname'
              426  LOAD_FAST                'dstname'
              428  LOAD_GLOBAL              str
              430  LOAD_FAST                'why'
              432  CALL_FUNCTION_1       1  ''
              434  BUILD_TUPLE_3         3 
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          
              440  POP_BLOCK        
              442  BEGIN_FINALLY    
            444_0  COME_FROM_FINALLY   418  '418'
              444  LOAD_CONST               None
              446  STORE_FAST               'why'
              448  DELETE_FAST              'why'
              450  END_FINALLY      
              452  POP_EXCEPT       
              454  JUMP_BACK            74  'to 74'
            456_0  COME_FROM           408  '408'
              456  END_FINALLY      
              458  JUMP_BACK            74  'to 74'

 L. 497       460  SETUP_FINALLY       476  'to 476'

 L. 498       462  LOAD_GLOBAL              copystat
              464  LOAD_FAST                'src'
              466  LOAD_FAST                'dst'
              468  CALL_FUNCTION_2       2  ''
              470  POP_TOP          
              472  POP_BLOCK        
              474  JUMP_FORWARD        550  'to 550'
            476_0  COME_FROM_FINALLY   460  '460'

 L. 499       476  DUP_TOP          
              478  LOAD_GLOBAL              OSError
              480  COMPARE_OP               exception-match
          482_484  POP_JUMP_IF_FALSE   548  'to 548'
              486  POP_TOP          
              488  STORE_FAST               'why'
              490  POP_TOP          
              492  SETUP_FINALLY       536  'to 536'

 L. 501       494  LOAD_GLOBAL              getattr
              496  LOAD_FAST                'why'
              498  LOAD_STR                 'winerror'
              500  LOAD_CONST               None
              502  CALL_FUNCTION_3       3  ''
              504  LOAD_CONST               None
              506  COMPARE_OP               is
          508_510  POP_JUMP_IF_FALSE   532  'to 532'

 L. 502       512  LOAD_FAST                'errors'
              514  LOAD_METHOD              append
              516  LOAD_FAST                'src'
              518  LOAD_FAST                'dst'
              520  LOAD_GLOBAL              str
              522  LOAD_FAST                'why'
              524  CALL_FUNCTION_1       1  ''
              526  BUILD_TUPLE_3         3 
              528  CALL_METHOD_1         1  ''
              530  POP_TOP          
            532_0  COME_FROM           508  '508'
              532  POP_BLOCK        
              534  BEGIN_FINALLY    
            536_0  COME_FROM_FINALLY   492  '492'
              536  LOAD_CONST               None
              538  STORE_FAST               'why'
              540  DELETE_FAST              'why'
              542  END_FINALLY      
              544  POP_EXCEPT       
              546  JUMP_FORWARD        550  'to 550'
            548_0  COME_FROM           482  '482'
              548  END_FINALLY      
            550_0  COME_FROM           546  '546'
            550_1  COME_FROM           474  '474'

 L. 503       550  LOAD_FAST                'errors'
          552_554  POP_JUMP_IF_FALSE   564  'to 564'

 L. 504       556  LOAD_GLOBAL              Error
              558  LOAD_FAST                'errors'
              560  CALL_FUNCTION_1       1  ''
              562  RAISE_VARARGS_1       1  'exception instance'
            564_0  COME_FROM           552  '552'

 L. 505       564  LOAD_FAST                'dst'
              566  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 260


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

 L. 558         0  SETUP_FINALLY        54  'to 54'

 L. 559         2  LOAD_FAST                'entry'
                4  LOAD_ATTR                stat
                6  LOAD_CONST               False
                8  LOAD_CONST               ('follow_symlinks',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'st'

 L. 560        14  LOAD_GLOBAL              stat
               16  LOAD_METHOD              S_ISDIR
               18  LOAD_FAST                'st'
               20  LOAD_ATTR                st_mode
               22  CALL_METHOD_1         1  ''
               24  JUMP_IF_FALSE_OR_POP    50  'to 50'

 L. 561        26  LOAD_FAST                'st'
               28  LOAD_ATTR                st_file_attributes
               30  LOAD_GLOBAL              stat
               32  LOAD_ATTR                FILE_ATTRIBUTE_REPARSE_POINT
               34  BINARY_AND       
               36  JUMP_IF_FALSE_OR_POP    48  'to 48'

 L. 562        38  LOAD_FAST                'st'
               40  LOAD_ATTR                st_reparse_tag
               42  LOAD_GLOBAL              stat
               44  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
               46  COMPARE_OP               ==
             48_0  COME_FROM            36  '36'

 L. 560        48  UNARY_NOT        
             50_0  COME_FROM            24  '24'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L. 563        54  DUP_TOP          
               56  LOAD_GLOBAL              OSError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    74  'to 74'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 564        68  POP_EXCEPT       
               70  LOAD_CONST               False
               72  RETURN_VALUE     
             74_0  COME_FROM            60  '60'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 64


            def _rmtree_islink--- This code section failed: ---

 L. 567         0  SETUP_FINALLY        50  'to 50'

 L. 568         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              lstat
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'st'

 L. 569        12  LOAD_GLOBAL              stat
               14  LOAD_METHOD              S_ISLNK
               16  LOAD_FAST                'st'
               18  LOAD_ATTR                st_mode
               20  CALL_METHOD_1         1  ''
               22  JUMP_IF_TRUE_OR_POP    46  'to 46'

 L. 570        24  LOAD_FAST                'st'
               26  LOAD_ATTR                st_file_attributes
               28  LOAD_GLOBAL              stat
               30  LOAD_ATTR                FILE_ATTRIBUTE_REPARSE_POINT
               32  BINARY_AND       
               34  JUMP_IF_FALSE_OR_POP    46  'to 46'

 L. 571        36  LOAD_FAST                'st'
               38  LOAD_ATTR                st_reparse_tag
               40  LOAD_GLOBAL              stat
               42  LOAD_ATTR                IO_REPARSE_TAG_MOUNT_POINT
               44  COMPARE_OP               ==
             46_0  COME_FROM            34  '34'
             46_1  COME_FROM            22  '22'

 L. 569        46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY     0  '0'

 L. 572        50  DUP_TOP          
               52  LOAD_GLOBAL              OSError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    70  'to 70'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 573        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
             70_0  COME_FROM            56  '56'
               70  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 60


        else:

            def _rmtree_isdir--- This code section failed: ---

 L. 576         0  SETUP_FINALLY        16  'to 16'

 L. 577         2  LOAD_FAST                'entry'
                4  LOAD_ATTR                is_dir
                6  LOAD_CONST               False
                8  LOAD_CONST               ('follow_symlinks',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 578        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 579        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


        def _rmtree_islink(path):
            return os.path.islink(path)


    def _rmtree_unsafe--- This code section failed: ---

 L. 586         0  SETUP_FINALLY        36  'to 36'

 L. 587         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              scandir
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           26  'to 26'
               12  STORE_FAST               'scandir_it'

 L. 588        14  LOAD_GLOBAL              list
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

 L. 589        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    76  'to 76'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 590        50  LOAD_FAST                'onerror'
               52  LOAD_GLOBAL              os
               54  LOAD_ATTR                scandir
               56  LOAD_FAST                'path'
               58  LOAD_GLOBAL              sys
               60  LOAD_METHOD              exc_info
               62  CALL_METHOD_0         0  ''
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          

 L. 591        68  BUILD_LIST_0          0 
               70  STORE_FAST               'entries'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            42  '42'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            34  '34'

 L. 592        78  LOAD_FAST                'entries'
               80  GET_ITER         
               82  FOR_ITER            234  'to 234'
               84  STORE_FAST               'entry'

 L. 593        86  LOAD_FAST                'entry'
               88  LOAD_ATTR                path
               90  STORE_FAST               'fullname'

 L. 594        92  LOAD_GLOBAL              _rmtree_isdir
               94  LOAD_FAST                'entry'
               96  CALL_FUNCTION_1       1  ''
               98  POP_JUMP_IF_FALSE   178  'to 178'

 L. 595       100  SETUP_FINALLY       122  'to 122'

 L. 596       102  LOAD_FAST                'entry'
              104  LOAD_METHOD              is_symlink
              106  CALL_METHOD_0         0  ''
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 600       110  LOAD_GLOBAL              OSError
              112  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           108  '108'
              118  POP_BLOCK        
              120  JUMP_FORWARD        166  'to 166'
            122_0  COME_FROM_FINALLY   100  '100'

 L. 601       122  DUP_TOP          
              124  LOAD_GLOBAL              OSError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   164  'to 164'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 602       136  LOAD_FAST                'onerror'
              138  LOAD_GLOBAL              os
              140  LOAD_ATTR                path
              142  LOAD_ATTR                islink
              144  LOAD_FAST                'fullname'
              146  LOAD_GLOBAL              sys
              148  LOAD_METHOD              exc_info
              150  CALL_METHOD_0         0  ''
              152  CALL_FUNCTION_3       3  ''
              154  POP_TOP          

 L. 603       156  POP_EXCEPT       
              158  JUMP_BACK            82  'to 82'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           128  '128'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           120  '120'

 L. 604       166  LOAD_GLOBAL              _rmtree_unsafe
              168  LOAD_FAST                'fullname'
              170  LOAD_FAST                'onerror'
              172  CALL_FUNCTION_2       2  ''
              174  POP_TOP          
              176  JUMP_BACK            82  'to 82'
            178_0  COME_FROM            98  '98'

 L. 606       178  SETUP_FINALLY       194  'to 194'

 L. 607       180  LOAD_GLOBAL              os
              182  LOAD_METHOD              unlink
              184  LOAD_FAST                'fullname'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  JUMP_BACK            82  'to 82'
            194_0  COME_FROM_FINALLY   178  '178'

 L. 608       194  DUP_TOP          
              196  LOAD_GLOBAL              OSError
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   230  'to 230'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 609       208  LOAD_FAST                'onerror'
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

 L. 610       234  SETUP_FINALLY       250  'to 250'

 L. 611       236  LOAD_GLOBAL              os
              238  LOAD_METHOD              rmdir
              240  LOAD_FAST                'path'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  POP_BLOCK        
              248  JUMP_FORWARD        290  'to 290'
            250_0  COME_FROM_FINALLY   234  '234'

 L. 612       250  DUP_TOP          
              252  LOAD_GLOBAL              OSError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   288  'to 288'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 613       266  LOAD_FAST                'onerror'
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

 L. 617         0  SETUP_FINALLY        36  'to 36'

 L. 618         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              scandir
                6  LOAD_FAST                'topfd'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           26  'to 26'
               12  STORE_FAST               'scandir_it'

 L. 619        14  LOAD_GLOBAL              list
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

 L. 620        36  DUP_TOP          
               38  LOAD_GLOBAL              OSError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    98  'to 98'
               44  POP_TOP          
               46  STORE_FAST               'err'
               48  POP_TOP          
               50  SETUP_FINALLY        86  'to 86'

 L. 621        52  LOAD_FAST                'path'
               54  LOAD_FAST                'err'
               56  STORE_ATTR               filename

 L. 622        58  LOAD_FAST                'onerror'
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                scandir
               64  LOAD_FAST                'path'
               66  LOAD_GLOBAL              sys
               68  LOAD_METHOD              exc_info
               70  CALL_METHOD_0         0  ''
               72  CALL_FUNCTION_3       3  ''
               74  POP_TOP          

 L. 623        76  POP_BLOCK        
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

 L. 624       100  LOAD_FAST                'entries'
              102  GET_ITER         
          104_106  FOR_ITER            554  'to 554'
              108  STORE_FAST               'entry'

 L. 625       110  LOAD_GLOBAL              os
              112  LOAD_ATTR                path
              114  LOAD_METHOD              join
              116  LOAD_FAST                'path'
              118  LOAD_FAST                'entry'
              120  LOAD_ATTR                name
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'fullname'

 L. 626       126  SETUP_FINALLY       144  'to 144'

 L. 627       128  LOAD_FAST                'entry'
              130  LOAD_ATTR                is_dir
              132  LOAD_CONST               False
              134  LOAD_CONST               ('follow_symlinks',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              138  STORE_FAST               'is_dir'
              140  POP_BLOCK        
              142  JUMP_FORWARD        168  'to 168'
            144_0  COME_FROM_FINALLY   126  '126'

 L. 628       144  DUP_TOP          
              146  LOAD_GLOBAL              OSError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   166  'to 166'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 629       158  LOAD_CONST               False
              160  STORE_FAST               'is_dir'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        244  'to 244'
            166_0  COME_FROM           150  '150'
              166  END_FINALLY      
            168_0  COME_FROM           142  '142'

 L. 631       168  LOAD_FAST                'is_dir'
              170  POP_JUMP_IF_FALSE   244  'to 244'

 L. 632       172  SETUP_FINALLY       202  'to 202'

 L. 633       174  LOAD_FAST                'entry'
              176  LOAD_ATTR                stat
              178  LOAD_CONST               False
              180  LOAD_CONST               ('follow_symlinks',)
              182  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              184  STORE_FAST               'orig_st'

 L. 634       186  LOAD_GLOBAL              stat
              188  LOAD_METHOD              S_ISDIR
              190  LOAD_FAST                'orig_st'
              192  LOAD_ATTR                st_mode
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'is_dir'
              198  POP_BLOCK        
              200  JUMP_FORWARD        244  'to 244'
            202_0  COME_FROM_FINALLY   172  '172'

 L. 635       202  DUP_TOP          
              204  LOAD_GLOBAL              OSError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   242  'to 242'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 636       216  LOAD_FAST                'onerror'
              218  LOAD_GLOBAL              os
              220  LOAD_ATTR                lstat
              222  LOAD_FAST                'fullname'
              224  LOAD_GLOBAL              sys
              226  LOAD_METHOD              exc_info
              228  CALL_METHOD_0         0  ''
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          

 L. 637       234  POP_EXCEPT       
              236  JUMP_BACK           104  'to 104'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           208  '208'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           200  '200'
            244_2  COME_FROM           170  '170'
            244_3  COME_FROM           164  '164'

 L. 638       244  LOAD_FAST                'is_dir'
          246_248  POP_JUMP_IF_FALSE   490  'to 490'

 L. 639       250  SETUP_FINALLY       276  'to 276'

 L. 640       252  LOAD_GLOBAL              os
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

 L. 641       276  DUP_TOP          
              278  LOAD_GLOBAL              OSError
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   314  'to 314'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L. 642       292  LOAD_FAST                'onerror'
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

 L. 644       316  SETUP_FINALLY       476  'to 476'

 L. 645       318  LOAD_GLOBAL              os
              320  LOAD_ATTR                path
              322  LOAD_METHOD              samestat
              324  LOAD_FAST                'orig_st'
              326  LOAD_GLOBAL              os
              328  LOAD_METHOD              fstat
              330  LOAD_FAST                'dirfd'
              332  CALL_METHOD_1         1  ''
              334  CALL_METHOD_2         2  ''
          336_338  POP_JUMP_IF_FALSE   416  'to 416'

 L. 646       340  LOAD_GLOBAL              _rmtree_safe_fd
              342  LOAD_FAST                'dirfd'
              344  LOAD_FAST                'fullname'
              346  LOAD_FAST                'onerror'
              348  CALL_FUNCTION_3       3  ''
              350  POP_TOP          

 L. 647       352  SETUP_FINALLY       374  'to 374'

 L. 648       354  LOAD_GLOBAL              os
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

 L. 649       374  DUP_TOP          
              376  LOAD_GLOBAL              OSError
              378  COMPARE_OP               exception-match
          380_382  POP_JUMP_IF_FALSE   412  'to 412'
              384  POP_TOP          
              386  POP_TOP          
              388  POP_TOP          

 L. 650       390  LOAD_FAST                'onerror'
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

 L. 652       416  SETUP_FINALLY       430  'to 430'

 L. 656       418  LOAD_GLOBAL              OSError
              420  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              422  CALL_FUNCTION_1       1  ''
              424  RAISE_VARARGS_1       1  'exception instance'
              426  POP_BLOCK        
              428  JUMP_FORWARD        472  'to 472'
            430_0  COME_FROM_FINALLY   416  '416'

 L. 658       430  DUP_TOP          
              432  LOAD_GLOBAL              OSError
              434  COMPARE_OP               exception-match
          436_438  POP_JUMP_IF_FALSE   470  'to 470'
              440  POP_TOP          
              442  POP_TOP          
              444  POP_TOP          

 L. 659       446  LOAD_FAST                'onerror'
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

 L. 661       476  LOAD_GLOBAL              os
              478  LOAD_METHOD              close
              480  LOAD_FAST                'dirfd'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
              486  END_FINALLY      
            488_0  COME_FROM           312  '312'
              488  JUMP_BACK           104  'to 104'
            490_0  COME_FROM           246  '246'

 L. 663       490  SETUP_FINALLY       512  'to 512'

 L. 664       492  LOAD_GLOBAL              os
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

 L. 665       512  DUP_TOP          
              514  LOAD_GLOBAL              OSError
              516  COMPARE_OP               exception-match
          518_520  POP_JUMP_IF_FALSE   550  'to 550'
              522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L. 666       528  LOAD_FAST                'onerror'
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

 L. 684         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              audit
                4  LOAD_STR                 'shutil.rmtree'
                6  LOAD_FAST                'path'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 685        12  LOAD_FAST                'ignore_errors'
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 686        16  LOAD_CODE                <code_object onerror>
               18  LOAD_STR                 'rmtree.<locals>.onerror'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'onerror'
               24  JUMP_FORWARD         42  'to 42'
             26_0  COME_FROM            14  '14'

 L. 688        26  LOAD_FAST                'onerror'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 689        34  LOAD_CODE                <code_object onerror>
               36  LOAD_STR                 'rmtree.<locals>.onerror'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  STORE_FAST               'onerror'
             42_0  COME_FROM            32  '32'
             42_1  COME_FROM            24  '24'

 L. 691        42  LOAD_GLOBAL              _use_fd_functions
            44_46  POP_JUMP_IF_FALSE   352  'to 352'

 L. 693        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'path'
               52  LOAD_GLOBAL              bytes
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 694        58  LOAD_GLOBAL              os
               60  LOAD_METHOD              fsdecode
               62  LOAD_FAST                'path'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'path'
             68_0  COME_FROM            56  '56'

 L. 697        68  SETUP_FINALLY        84  'to 84'

 L. 698        70  LOAD_GLOBAL              os
               72  LOAD_METHOD              lstat
               74  LOAD_FAST                'path'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'orig_st'
               80  POP_BLOCK        
               82  JUMP_FORWARD        124  'to 124'
             84_0  COME_FROM_FINALLY    68  '68'

 L. 699        84  DUP_TOP          
               86  LOAD_GLOBAL              Exception
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   122  'to 122'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 700        98  LOAD_FAST                'onerror'
              100  LOAD_GLOBAL              os
              102  LOAD_ATTR                lstat
              104  LOAD_FAST                'path'
              106  LOAD_GLOBAL              sys
              108  LOAD_METHOD              exc_info
              110  CALL_METHOD_0         0  ''
              112  CALL_FUNCTION_3       3  ''
              114  POP_TOP          

 L. 701       116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            90  '90'
              122  END_FINALLY      
            124_0  COME_FROM            82  '82'

 L. 702       124  SETUP_FINALLY       144  'to 144'

 L. 703       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              open
              130  LOAD_FAST                'path'
              132  LOAD_GLOBAL              os
              134  LOAD_ATTR                O_RDONLY
              136  CALL_METHOD_2         2  ''
              138  STORE_FAST               'fd'
              140  POP_BLOCK        
              142  JUMP_FORWARD        184  'to 184'
            144_0  COME_FROM_FINALLY   124  '124'

 L. 704       144  DUP_TOP          
              146  LOAD_GLOBAL              Exception
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   182  'to 182'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 705       158  LOAD_FAST                'onerror'
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                lstat
              164  LOAD_FAST                'path'
              166  LOAD_GLOBAL              sys
              168  LOAD_METHOD              exc_info
              170  CALL_METHOD_0         0  ''
              172  CALL_FUNCTION_3       3  ''
              174  POP_TOP          

 L. 706       176  POP_EXCEPT       
              178  LOAD_CONST               None
              180  RETURN_VALUE     
            182_0  COME_FROM           150  '150'
              182  END_FINALLY      
            184_0  COME_FROM           142  '142'

 L. 707       184  SETUP_FINALLY       338  'to 338'

 L. 708       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              samestat
              192  LOAD_FAST                'orig_st'
              194  LOAD_GLOBAL              os
              196  LOAD_METHOD              fstat
              198  LOAD_FAST                'fd'
              200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_2         2  ''
          204_206  POP_JUMP_IF_FALSE   278  'to 278'

 L. 709       208  LOAD_GLOBAL              _rmtree_safe_fd
              210  LOAD_FAST                'fd'
              212  LOAD_FAST                'path'
              214  LOAD_FAST                'onerror'
              216  CALL_FUNCTION_3       3  ''
              218  POP_TOP          

 L. 710       220  SETUP_FINALLY       236  'to 236'

 L. 711       222  LOAD_GLOBAL              os
              224  LOAD_METHOD              rmdir
              226  LOAD_FAST                'path'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  POP_BLOCK        
              234  JUMP_FORWARD        276  'to 276'
            236_0  COME_FROM_FINALLY   220  '220'

 L. 712       236  DUP_TOP          
              238  LOAD_GLOBAL              OSError
              240  COMPARE_OP               exception-match
          242_244  POP_JUMP_IF_FALSE   274  'to 274'
              246  POP_TOP          
              248  POP_TOP          
              250  POP_TOP          

 L. 713       252  LOAD_FAST                'onerror'
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

 L. 715       278  SETUP_FINALLY       292  'to 292'

 L. 717       280  LOAD_GLOBAL              OSError
              282  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              284  CALL_FUNCTION_1       1  ''
              286  RAISE_VARARGS_1       1  'exception instance'
              288  POP_BLOCK        
              290  JUMP_FORWARD        334  'to 334'
            292_0  COME_FROM_FINALLY   278  '278'

 L. 718       292  DUP_TOP          
              294  LOAD_GLOBAL              OSError
              296  COMPARE_OP               exception-match
          298_300  POP_JUMP_IF_FALSE   332  'to 332'
              302  POP_TOP          
              304  POP_TOP          
              306  POP_TOP          

 L. 719       308  LOAD_FAST                'onerror'
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

 L. 721       338  LOAD_GLOBAL              os
              340  LOAD_METHOD              close
              342  LOAD_FAST                'fd'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  END_FINALLY      
              350  JUMP_FORWARD        430  'to 430'
            352_0  COME_FROM            44  '44'

 L. 723       352  SETUP_FINALLY       376  'to 376'

 L. 724       354  LOAD_GLOBAL              _rmtree_islink
              356  LOAD_FAST                'path'
              358  CALL_FUNCTION_1       1  ''
          360_362  POP_JUMP_IF_FALSE   372  'to 372'

 L. 726       364  LOAD_GLOBAL              OSError
              366  LOAD_STR                 'Cannot call rmtree on a symbolic link'
              368  CALL_FUNCTION_1       1  ''
              370  RAISE_VARARGS_1       1  'exception instance'
            372_0  COME_FROM           360  '360'
              372  POP_BLOCK        
              374  JUMP_FORWARD        420  'to 420'
            376_0  COME_FROM_FINALLY   352  '352'

 L. 727       376  DUP_TOP          
              378  LOAD_GLOBAL              OSError
              380  COMPARE_OP               exception-match
          382_384  POP_JUMP_IF_FALSE   418  'to 418'
              386  POP_TOP          
              388  POP_TOP          
              390  POP_TOP          

 L. 728       392  LOAD_FAST                'onerror'
              394  LOAD_GLOBAL              os
              396  LOAD_ATTR                path
              398  LOAD_ATTR                islink
              400  LOAD_FAST                'path'
              402  LOAD_GLOBAL              sys
              404  LOAD_METHOD              exc_info
              406  CALL_METHOD_0         0  ''
              408  CALL_FUNCTION_3       3  ''
              410  POP_TOP          

 L. 730       412  POP_EXCEPT       
              414  LOAD_CONST               None
              416  RETURN_VALUE     
            418_0  COME_FROM           382  '382'
              418  END_FINALLY      
            420_0  COME_FROM           374  '374'

 L. 731       420  LOAD_GLOBAL              _rmtree_unsafe
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