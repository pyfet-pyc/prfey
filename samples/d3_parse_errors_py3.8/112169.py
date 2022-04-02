# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: tempfile.py
"""Temporary files.

This module provides generic, low- and high-level interfaces for
creating temporary files and directories.  All of the interfaces
provided by this module can be used without fear of race conditions
except for 'mktemp'.  'mktemp' is subject to race conditions and
should not be used; it is provided for backward compatibility only.

The default path names are returned as str.  If you supply bytes as
input, all return values will be in bytes.  Ex:

    >>> tempfile.mkstemp()
    (4, '/tmp/tmptpu9nin8')
    >>> tempfile.mkdtemp(suffix=b'')
    b'/tmp/tmppbi8f0hy'

This module also provides some data items to the user:

  TMP_MAX  - maximum number of names that will be tried before
             giving up.
  tempdir  - If this is set to a string before the first use of
             any routine from this module, it will be considered as
             another candidate location to store temporary files.
"""
__all__ = [
 'NamedTemporaryFile', 'TemporaryFile',
 'SpooledTemporaryFile', 'TemporaryDirectory',
 'mkstemp', 'mkdtemp',
 'mktemp',
 'TMP_MAX', 'gettempprefix',
 'tempdir', 'gettempdir',
 'gettempprefixb', 'gettempdirb']
import functools as _functools, warnings as _warnings, io as _io, os as _os, shutil as _shutil, errno as _errno
from random import Random as _Random
import sys as _sys, weakref as _weakref, _thread
_allocate_lock = _thread.allocate_lock
_text_openflags = _os.O_RDWR | _os.O_CREAT | _os.O_EXCL
if hasattr(_os, 'O_NOFOLLOW'):
    _text_openflags |= _os.O_NOFOLLOW
_bin_openflags = _text_openflags
if hasattr(_os, 'O_BINARY'):
    _bin_openflags |= _os.O_BINARY
if hasattr(_os, 'TMP_MAX'):
    TMP_MAX = _os.TMP_MAX
else:
    TMP_MAX = 10000
template = 'tmp'
_once_lock = _allocate_lock()

def _exists(fn):
    try:
        _os.lstat(fn)
    except OSError:
        return False
    else:
        return True


def _infer_return_type(*args):
    """Look at the type of all args and divine their implied return type."""
    return_type = None
    for arg in args:
        if arg is None:
            pass
        else:
            if isinstance(arg, bytes):
                if return_type is str:
                    raise TypeError("Can't mix bytes and non-bytes in path components.")
                else:
                    return_type = bytes
            else:
                if return_type is bytes:
                    raise TypeError("Can't mix bytes and non-bytes in path components.")
                return_type = str
    else:
        if return_type is None:
            return str
        return return_type


def _sanitize_params(prefix, suffix, dir):
    """Common parameter processing for most APIs in this module."""
    output_type = _infer_return_type(prefix, suffix, dir)
    if suffix is None:
        suffix = output_type()
    if prefix is None:
        if output_type is str:
            prefix = template
        else:
            prefix = _os.fsencode(template)
    if dir is None:
        if output_type is str:
            dir = gettempdir()
        else:
            dir = gettempdirb()
    return (
     prefix, suffix, dir, output_type)


class _RandomNameSequence:
    __doc__ = 'An instance of _RandomNameSequence generates an endless\n    sequence of unpredictable strings which can safely be incorporated\n    into file names.  Each string is eight characters long.  Multiple\n    threads can safely use the same instance at the same time.\n\n    _RandomNameSequence is an iterator.'
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789_'

    @property
    def rng(self):
        cur_pid = _os.getpid()
        if cur_pid != getattr(self, '_rng_pid', None):
            self._rng = _Random()
            self._rng_pid = cur_pid
        return self._rng

    def __iter__(self):
        return self

    def __next__(self):
        c = self.characters
        choose = self.rng.choice
        letters = [choose(c) for dummy in range(8)]
        return ''.join(letters)


def _candidate_tempdir_list():
    """Generate a list of candidate temporary directories which
    _get_default_tempdir will try."""
    dirlist = []
    for envname in ('TMPDIR', 'TEMP', 'TMP'):
        dirname = _os.getenv(envname)
        if dirname:
            dirlist.append(dirname)
    else:
        if _os.name == 'nt':
            dirlist.extend([_os.path.expanduser('~\\AppData\\Local\\Temp'),
             _os.path.expandvars('%SYSTEMROOT%\\Temp'),
             'c:\\temp', 'c:\\tmp', '\\temp', '\\tmp'])
        else:
            dirlist.extend(['/tmp', '/var/tmp', '/usr/tmp'])
        try:
            dirlist.append(_os.getcwd())
        except (AttributeError, OSError):
            dirlist.append(_os.curdir)
        else:
            return dirlist


def _get_default_tempdir--- This code section failed: ---

 L. 186         0  LOAD_GLOBAL              _RandomNameSequence
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'namer'

 L. 187         6  LOAD_GLOBAL              _candidate_tempdir_list
                8  CALL_FUNCTION_0       0  ''
               10  STORE_FAST               'dirlist'

 L. 189        12  LOAD_FAST                'dirlist'
               14  GET_ITER         
             16_0  COME_FROM           304  '304'
             16_1  COME_FROM           294  '294'
             16_2  COME_FROM           268  '268'
            16_18  FOR_ITER            306  'to 306'
               20  STORE_FAST               'dir'

 L. 190        22  LOAD_FAST                'dir'
               24  LOAD_GLOBAL              _os
               26  LOAD_ATTR                curdir
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L. 191        32  LOAD_GLOBAL              _os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              abspath
               38  LOAD_FAST                'dir'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'dir'
             44_0  COME_FROM            30  '30'

 L. 193        44  LOAD_GLOBAL              range
               46  LOAD_CONST               100
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
             52_0  COME_FROM           302  '302'
             52_1  COME_FROM           298  '298'
             52_2  COME_FROM           272  '272'
             52_3  COME_FROM           262  '262'
             52_4  COME_FROM           200  '200'
            52_54  FOR_ITER            304  'to 304'
               56  STORE_FAST               'seq'

 L. 194        58  LOAD_GLOBAL              next
               60  LOAD_FAST                'namer'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'name'

 L. 195        66  LOAD_GLOBAL              _os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              join
               72  LOAD_FAST                'dir'
               74  LOAD_FAST                'name'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'filename'

 L. 196        80  SETUP_FINALLY       184  'to 184'

 L. 197        82  LOAD_GLOBAL              _os
               84  LOAD_METHOD              open
               86  LOAD_FAST                'filename'
               88  LOAD_GLOBAL              _bin_openflags
               90  LOAD_CONST               384
               92  CALL_METHOD_3         3  ''
               94  STORE_FAST               'fd'

 L. 198        96  SETUP_FINALLY       158  'to 158'

 L. 199        98  SETUP_FINALLY       142  'to 142'

 L. 200       100  LOAD_GLOBAL              _io
              102  LOAD_ATTR                open
              104  LOAD_FAST                'fd'
              106  LOAD_STR                 'wb'
              108  LOAD_CONST               False
              110  LOAD_CONST               ('closefd',)
              112  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              114  SETUP_WITH          132  'to 132'
              116  STORE_FAST               'fp'

 L. 201       118  LOAD_FAST                'fp'
              120  LOAD_METHOD              write
              122  LOAD_CONST               b'blat'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_WITH      114  '114'
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_FINALLY    98  '98'

 L. 203       142  LOAD_GLOBAL              _os
              144  LOAD_METHOD              close
              146  LOAD_FAST                'fd'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  END_FINALLY      
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM_FINALLY    96  '96'

 L. 205       158  LOAD_GLOBAL              _os
              160  LOAD_METHOD              unlink
              162  LOAD_FAST                'filename'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  END_FINALLY      

 L. 206       170  LOAD_FAST                'dir'
              172  POP_BLOCK        
              174  ROT_TWO          
              176  POP_TOP          
              178  ROT_TWO          
              180  POP_TOP          
              182  RETURN_VALUE     
            184_0  COME_FROM_FINALLY    80  '80'

 L. 207       184  DUP_TOP          
              186  LOAD_GLOBAL              FileExistsError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   202  'to 202'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 208       198  POP_EXCEPT       
              200  JUMP_BACK            52  'to 52'
            202_0  COME_FROM           190  '190'

 L. 209       202  DUP_TOP          
              204  LOAD_GLOBAL              PermissionError
              206  COMPARE_OP               exception-match
          208_210  POP_JUMP_IF_FALSE   274  'to 274'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 212       218  LOAD_GLOBAL              _os
              220  LOAD_ATTR                name
              222  LOAD_STR                 'nt'
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_FALSE   264  'to 264'
              230  LOAD_GLOBAL              _os
              232  LOAD_ATTR                path
              234  LOAD_METHOD              isdir
              236  LOAD_FAST                'dir'
              238  CALL_METHOD_1         1  ''
          240_242  POP_JUMP_IF_FALSE   264  'to 264'

 L. 213       244  LOAD_GLOBAL              _os
              246  LOAD_METHOD              access
              248  LOAD_FAST                'dir'
              250  LOAD_GLOBAL              _os
              252  LOAD_ATTR                W_OK
              254  CALL_METHOD_2         2  ''

 L. 212   256_258  POP_JUMP_IF_FALSE   264  'to 264'

 L. 214       260  POP_EXCEPT       
              262  JUMP_BACK            52  'to 52'
            264_0  COME_FROM           256  '256'
            264_1  COME_FROM           240  '240'
            264_2  COME_FROM           226  '226'

 L. 215       264  POP_EXCEPT       
              266  POP_TOP          
              268  JUMP_BACK            16  'to 16'
              270  POP_EXCEPT       
              272  JUMP_BACK            52  'to 52'
            274_0  COME_FROM           208  '208'

 L. 216       274  DUP_TOP          
              276  LOAD_GLOBAL              OSError
              278  COMPARE_OP               exception-match
          280_282  POP_JUMP_IF_FALSE   300  'to 300'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L. 217       290  POP_EXCEPT       
              292  POP_TOP          
              294  JUMP_BACK            16  'to 16'
              296  POP_EXCEPT       
              298  JUMP_BACK            52  'to 52'
            300_0  COME_FROM           280  '280'
              300  END_FINALLY      
              302  JUMP_BACK            52  'to 52'
            304_0  COME_FROM            52  '52'
              304  JUMP_BACK            16  'to 16'
            306_0  COME_FROM            16  '16'

 L. 218       306  LOAD_GLOBAL              FileNotFoundError
              308  LOAD_GLOBAL              _errno
              310  LOAD_ATTR                ENOENT

 L. 219       312  LOAD_STR                 'No usable temporary directory found in %s'

 L. 220       314  LOAD_FAST                'dirlist'

 L. 219       316  BINARY_MODULO    

 L. 218       318  CALL_FUNCTION_2       2  ''
              320  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 176


_name_sequence = None

def _get_candidate_names():
    """Common setup sequence for all user-callable interfaces."""
    global _name_sequence
    if _name_sequence is None:
        _once_lock.acquire()
        try:
            if _name_sequence is None:
                _name_sequence = _RandomNameSequence()
        finally:
            _once_lock.release()

    return _name_sequence


def _mkstemp_inner--- This code section failed: ---

 L. 241         0  LOAD_GLOBAL              _get_candidate_names
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'names'

 L. 242         6  LOAD_FAST                'output_type'
                8  LOAD_GLOBAL              bytes
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L. 243        14  LOAD_GLOBAL              map
               16  LOAD_GLOBAL              _os
               18  LOAD_ATTR                fsencode
               20  LOAD_FAST                'names'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'names'
             26_0  COME_FROM            12  '12'

 L. 245        26  LOAD_GLOBAL              range
               28  LOAD_GLOBAL              TMP_MAX
               30  CALL_FUNCTION_1       1  ''
               32  GET_ITER         
             34_0  COME_FROM           174  '174'
             34_1  COME_FROM           116  '116'
               34  FOR_ITER            206  'to 206'
               36  STORE_FAST               'seq'

 L. 246        38  LOAD_GLOBAL              next
               40  LOAD_FAST                'names'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'name'

 L. 247        46  LOAD_GLOBAL              _os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              join
               52  LOAD_FAST                'dir'
               54  LOAD_FAST                'pre'
               56  LOAD_FAST                'name'
               58  BINARY_ADD       
               60  LOAD_FAST                'suf'
               62  BINARY_ADD       
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'file'

 L. 248        68  LOAD_GLOBAL              _sys
               70  LOAD_METHOD              audit
               72  LOAD_STR                 'tempfile.mkstemp'
               74  LOAD_FAST                'file'
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          

 L. 249        80  SETUP_FINALLY       100  'to 100'

 L. 250        82  LOAD_GLOBAL              _os
               84  LOAD_METHOD              open
               86  LOAD_FAST                'file'
               88  LOAD_FAST                'flags'
               90  LOAD_CONST               384
               92  CALL_METHOD_3         3  ''
               94  STORE_FAST               'fd'
               96  POP_BLOCK        
               98  JUMP_FORWARD        186  'to 186'
            100_0  COME_FROM_FINALLY    80  '80'

 L. 251       100  DUP_TOP          
              102  LOAD_GLOBAL              FileExistsError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   122  'to 122'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 252       114  POP_EXCEPT       
              116  JUMP_BACK            34  'to 34'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        186  'to 186'
            122_0  COME_FROM           106  '106'

 L. 253       122  DUP_TOP          
              124  LOAD_GLOBAL              PermissionError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   184  'to 184'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 256       136  LOAD_GLOBAL              _os
              138  LOAD_ATTR                name
              140  LOAD_STR                 'nt'
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   178  'to 178'
              146  LOAD_GLOBAL              _os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              isdir
              152  LOAD_FAST                'dir'
              154  CALL_METHOD_1         1  ''
              156  POP_JUMP_IF_FALSE   178  'to 178'

 L. 257       158  LOAD_GLOBAL              _os
              160  LOAD_METHOD              access
              162  LOAD_FAST                'dir'
              164  LOAD_GLOBAL              _os
              166  LOAD_ATTR                W_OK
              168  CALL_METHOD_2         2  ''

 L. 256       170  POP_JUMP_IF_FALSE   178  'to 178'

 L. 258       172  POP_EXCEPT       
              174  JUMP_BACK            34  'to 34'
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           170  '170'
            178_1  COME_FROM           156  '156'
            178_2  COME_FROM           144  '144'

 L. 260       178  RAISE_VARARGS_0       0  'reraise'
            180_0  COME_FROM           176  '176'
              180  POP_EXCEPT       
              182  JUMP_FORWARD        186  'to 186'
            184_0  COME_FROM           128  '128'
              184  END_FINALLY      
            186_0  COME_FROM           182  '182'
            186_1  COME_FROM           120  '120'
            186_2  COME_FROM            98  '98'

 L. 261       186  LOAD_FAST                'fd'
              188  LOAD_GLOBAL              _os
              190  LOAD_ATTR                path
              192  LOAD_METHOD              abspath
              194  LOAD_FAST                'file'
              196  CALL_METHOD_1         1  ''
              198  BUILD_TUPLE_2         2 
              200  ROT_TWO          
              202  POP_TOP          
              204  RETURN_VALUE     
            206_0  COME_FROM            34  '34'

 L. 263       206  LOAD_GLOBAL              FileExistsError
              208  LOAD_GLOBAL              _errno
              210  LOAD_ATTR                EEXIST

 L. 264       212  LOAD_STR                 'No usable temporary file name found'

 L. 263       214  CALL_FUNCTION_2       2  ''
              216  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 122_0


def gettempprefix():
    """The default prefix for temporary directories."""
    return template


def gettempprefixb():
    """The default prefix for temporary directories as bytes."""
    return _os.fsencode(gettempprefix())


tempdir = None

def gettempdir():
    """Accessor for tempfile.tempdir."""
    global tempdir
    if tempdir is None:
        _once_lock.acquire()
        try:
            if tempdir is None:
                tempdir = _get_default_tempdir()
        finally:
            _once_lock.release()

    return tempdir


def gettempdirb():
    """A bytes version of tempfile.gettempdir()."""
    return _os.fsencode(gettempdir())


def mkstemp(suffix=None, prefix=None, dir=None, text=False):
    """User-callable function to create and return a unique temporary
    file.  The return value is a pair (fd, name) where fd is the
    file descriptor returned by os.open, and name is the filename.

    If 'suffix' is not None, the file name will end with that suffix,
    otherwise there will be no suffix.

    If 'prefix' is not None, the file name will begin with that prefix,
    otherwise a default prefix is used.

    If 'dir' is not None, the file will be created in that directory,
    otherwise a default directory is used.

    If 'text' is specified and true, the file is opened in text
    mode.  Else (the default) the file is opened in binary mode.  On
    some operating systems, this makes no difference.

    If any of 'suffix', 'prefix' and 'dir' are not None, they must be the
    same type.  If they are bytes, the returned name will be bytes; str
    otherwise.

    The file is readable and writable only by the creating user ID.
    If the operating system uses permission bits to indicate whether a
    file is executable, the file is executable by no one. The file
    descriptor is not inherited by children of this process.

    Caller is responsible for deleting the file when done with it.
    """
    prefix, suffix, dir, output_type = _sanitize_params(prefix, suffix, dir)
    if text:
        flags = _text_openflags
    else:
        flags = _bin_openflags
    return _mkstemp_inner(dir, prefix, suffix, flags, output_type)


def mkdtemp--- This code section failed: ---

 L. 348         0  LOAD_GLOBAL              _sanitize_params
                2  LOAD_FAST                'prefix'
                4  LOAD_FAST                'suffix'
                6  LOAD_FAST                'dir'
                8  CALL_FUNCTION_3       3  ''
               10  UNPACK_SEQUENCE_4     4 
               12  STORE_FAST               'prefix'
               14  STORE_FAST               'suffix'
               16  STORE_FAST               'dir'
               18  STORE_FAST               'output_type'

 L. 350        20  LOAD_GLOBAL              _get_candidate_names
               22  CALL_FUNCTION_0       0  ''
               24  STORE_FAST               'names'

 L. 351        26  LOAD_FAST                'output_type'
               28  LOAD_GLOBAL              bytes
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 352        34  LOAD_GLOBAL              map
               36  LOAD_GLOBAL              _os
               38  LOAD_ATTR                fsencode
               40  LOAD_FAST                'names'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'names'
             46_0  COME_FROM            32  '32'

 L. 354        46  LOAD_GLOBAL              range
               48  LOAD_GLOBAL              TMP_MAX
               50  CALL_FUNCTION_1       1  ''
               52  GET_ITER         
             54_0  COME_FROM           192  '192'
             54_1  COME_FROM           134  '134'
               54  FOR_ITER            212  'to 212'
               56  STORE_FAST               'seq'

 L. 355        58  LOAD_GLOBAL              next
               60  LOAD_FAST                'names'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'name'

 L. 356        66  LOAD_GLOBAL              _os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              join
               72  LOAD_FAST                'dir'
               74  LOAD_FAST                'prefix'
               76  LOAD_FAST                'name'
               78  BINARY_ADD       
               80  LOAD_FAST                'suffix'
               82  BINARY_ADD       
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'file'

 L. 357        88  LOAD_GLOBAL              _sys
               90  LOAD_METHOD              audit
               92  LOAD_STR                 'tempfile.mkdtemp'
               94  LOAD_FAST                'file'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 358       100  SETUP_FINALLY       118  'to 118'

 L. 359       102  LOAD_GLOBAL              _os
              104  LOAD_METHOD              mkdir
              106  LOAD_FAST                'file'
              108  LOAD_CONST               448
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          
              114  POP_BLOCK        
              116  JUMP_FORWARD        204  'to 204'
            118_0  COME_FROM_FINALLY   100  '100'

 L. 360       118  DUP_TOP          
              120  LOAD_GLOBAL              FileExistsError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   140  'to 140'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 361       132  POP_EXCEPT       
              134  JUMP_BACK            54  'to 54'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        204  'to 204'
            140_0  COME_FROM           124  '124'

 L. 362       140  DUP_TOP          
              142  LOAD_GLOBAL              PermissionError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   202  'to 202'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 365       154  LOAD_GLOBAL              _os
              156  LOAD_ATTR                name
              158  LOAD_STR                 'nt'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   196  'to 196'
              164  LOAD_GLOBAL              _os
              166  LOAD_ATTR                path
              168  LOAD_METHOD              isdir
              170  LOAD_FAST                'dir'
              172  CALL_METHOD_1         1  ''
              174  POP_JUMP_IF_FALSE   196  'to 196'

 L. 366       176  LOAD_GLOBAL              _os
              178  LOAD_METHOD              access
              180  LOAD_FAST                'dir'
              182  LOAD_GLOBAL              _os
              184  LOAD_ATTR                W_OK
              186  CALL_METHOD_2         2  ''

 L. 365       188  POP_JUMP_IF_FALSE   196  'to 196'

 L. 367       190  POP_EXCEPT       
              192  JUMP_BACK            54  'to 54'
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           188  '188'
            196_1  COME_FROM           174  '174'
            196_2  COME_FROM           162  '162'

 L. 369       196  RAISE_VARARGS_0       0  'reraise'
            198_0  COME_FROM           194  '194'
              198  POP_EXCEPT       
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM           146  '146'
              202  END_FINALLY      
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           138  '138'
            204_2  COME_FROM           116  '116'

 L. 370       204  LOAD_FAST                'file'
              206  ROT_TWO          
              208  POP_TOP          
              210  RETURN_VALUE     
            212_0  COME_FROM            54  '54'

 L. 372       212  LOAD_GLOBAL              FileExistsError
              214  LOAD_GLOBAL              _errno
              216  LOAD_ATTR                EEXIST

 L. 373       218  LOAD_STR                 'No usable temporary directory name found'

 L. 372       220  CALL_FUNCTION_2       2  ''
              222  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 140_0


def mktemp(suffix='', prefix=template, dir=None):
    """User-callable function to return a unique temporary file name.  The
    file is not created.

    Arguments are similar to mkstemp, except that the 'text' argument is
    not accepted, and suffix=None, prefix=None and bytes file names are not
    supported.

    THIS FUNCTION IS UNSAFE AND SHOULD NOT BE USED.  The file name may
    refer to a file that did not exist at some point, but by the time
    you get around to creating it, someone else may have beaten you to
    the punch.
    """
    if dir is None:
        dir = gettempdir()
    names = _get_candidate_names()
    for seq in range(TMP_MAX):
        name = next(names)
        file = _os.path.joindir(prefix + name + suffix)
        if not _exists(file):
            return file
    else:
        raise FileExistsError(_errno.EEXIST, 'No usable temporary filename found')


class _TemporaryFileCloser:
    __doc__ = "A separate object allowing proper closing of a temporary file's\n    underlying file object, without adding a __del__ method to the\n    temporary file."
    file = None
    close_called = False

    def __init__(self, file, name, delete=True):
        self.file = file
        self.name = name
        self.delete = delete

    if _os.name != 'nt':

        def close(self, unlink=_os.unlink):
            if not self.close_called:
                if self.file is not None:
                    self.close_called = True
                    try:
                        self.file.close()
                    finally:
                        if self.delete:
                            unlink(self.name)

        def __del__(self):
            self.close()

    else:

        def close(self):
            if not self.close_called:
                self.close_called = True
                self.file.close()


class _TemporaryFileWrapper:
    __doc__ = 'Temporary file wrapper\n\n    This class provides a wrapper around files opened for\n    temporary use.  In particular, it seeks to automatically\n    remove the file when it is no longer needed.\n    '

    def __init__(self, file, name, delete=True):
        self.file = file
        self.name = name
        self.delete = delete
        self._closer = _TemporaryFileCloser(file, name, delete)

    def __getattr__(self, name):
        file = self.__dict__['file']
        a = getattr(file, name)
        if hasattr(a, '__call__'):
            func = a

            @_functools.wraps(func)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            func_wrapper._closer = self._closer
            a = func_wrapper
        if not isinstance(a, int):
            setattr(self, name, a)
        return a

    def __enter__(self):
        self.file.__enter__()
        return self

    def __exit__(self, exc, value, tb):
        result = self.file.__exit__excvaluetb
        self.close()
        return result

    def close(self):
        """
        Close the temporary file, possibly deleting it.
        """
        self._closer.close()

    def __iter__(self):
        for line in self.file:
            yield line


def NamedTemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, delete=True, *, errors=None):
    """Create and return a temporary file.
    Arguments:
    'prefix', 'suffix', 'dir' -- as for mkstemp.
    'mode' -- the mode argument to io.open (default "w+b").
    'buffering' -- the buffer size argument to io.open (default -1).
    'encoding' -- the encoding argument to io.open (default None)
    'newline' -- the newline argument to io.open (default None)
    'delete' -- whether the file is deleted on close (default True).
    'errors' -- the errors argument to io.open (default None)
    The file is created as mkstemp() would do it.

    Returns an object with a file-like interface; the name of the file
    is accessible as its 'name' attribute.  The file will be automatically
    deleted when it is closed unless the 'delete' argument is set to False.
    """
    prefix, suffix, dir, output_type = _sanitize_params(prefix, suffix, dir)
    flags = _bin_openflags
    if _os.name == 'nt':
        if delete:
            flags |= _os.O_TEMPORARY
    fd, name = _mkstemp_inner(dir, prefix, suffix, flags, output_type)
    try:
        file = _io.open(fd, mode, buffering=buffering, newline=newline,
          encoding=encoding,
          errors=errors)
        return _TemporaryFileWrapper(file, name, delete)
    except BaseException:
        _os.unlink(name)
        _os.close(fd)
        raise


if _os.name != 'posix' or _sys.platform == 'cygwin':
    TemporaryFile = NamedTemporaryFile
else:
    _O_TMPFILE_WORKS = hasattr(_os, 'O_TMPFILE')

    def TemporaryFile--- This code section failed: ---

 L. 581         0  LOAD_GLOBAL              _sanitize_params
                2  LOAD_FAST                'prefix'
                4  LOAD_FAST                'suffix'
                6  LOAD_FAST                'dir'
                8  CALL_FUNCTION_3       3  ''
               10  UNPACK_SEQUENCE_4     4 
               12  STORE_FAST               'prefix'
               14  STORE_FAST               'suffix'
               16  STORE_FAST               'dir'
               18  STORE_FAST               'output_type'

 L. 583        20  LOAD_GLOBAL              _bin_openflags
               22  STORE_FAST               'flags'

 L. 584        24  LOAD_GLOBAL              _O_TMPFILE_WORKS
               26  POP_JUMP_IF_FALSE   158  'to 158'

 L. 585        28  SETUP_FINALLY        66  'to 66'

 L. 586        30  LOAD_FAST                'flags'
               32  LOAD_GLOBAL              _os
               34  LOAD_ATTR                O_TMPFILE
               36  BINARY_OR        
               38  LOAD_GLOBAL              _os
               40  LOAD_ATTR                O_CREAT
               42  UNARY_INVERT     
               44  BINARY_AND       
               46  STORE_FAST               'flags2'

 L. 587        48  LOAD_GLOBAL              _os
               50  LOAD_METHOD              open
               52  LOAD_FAST                'dir'
               54  LOAD_FAST                'flags2'
               56  LOAD_CONST               384
               58  CALL_METHOD_3         3  ''
               60  STORE_FAST               'fd'
               62  POP_BLOCK        
               64  JUMP_FORWARD        108  'to 108'
             66_0  COME_FROM_FINALLY    28  '28'

 L. 588        66  DUP_TOP          
               68  LOAD_GLOBAL              IsADirectoryError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    88  'to 88'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 594        80  LOAD_CONST               False
               82  STORE_GLOBAL             _O_TMPFILE_WORKS
               84  POP_EXCEPT       
               86  JUMP_FORWARD        158  'to 158'
             88_0  COME_FROM            72  '72'

 L. 595        88  DUP_TOP          
               90  LOAD_GLOBAL              OSError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   106  'to 106'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 603       102  POP_EXCEPT       
              104  JUMP_FORWARD        158  'to 158'
            106_0  COME_FROM            94  '94'
              106  END_FINALLY      
            108_0  COME_FROM            64  '64'

 L. 605       108  SETUP_FINALLY       134  'to 134'

 L. 606       110  LOAD_GLOBAL              _io
              112  LOAD_ATTR                open
              114  LOAD_FAST                'fd'
              116  LOAD_FAST                'mode'
              118  LOAD_FAST                'buffering'

 L. 607       120  LOAD_FAST                'newline'

 L. 607       122  LOAD_FAST                'encoding'

 L. 608       124  LOAD_FAST                'errors'

 L. 606       126  LOAD_CONST               ('buffering', 'newline', 'encoding', 'errors')
              128  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              130  POP_BLOCK        
              132  RETURN_VALUE     
            134_0  COME_FROM_FINALLY   108  '108'

 L. 609       134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 610       140  LOAD_GLOBAL              _os
              142  LOAD_METHOD              close
              144  LOAD_FAST                'fd'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 611       150  RAISE_VARARGS_0       0  'reraise'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           104  '104'
            158_2  COME_FROM            86  '86'
            158_3  COME_FROM            26  '26'

 L. 614       158  LOAD_GLOBAL              _mkstemp_inner
              160  LOAD_FAST                'dir'
              162  LOAD_FAST                'prefix'
              164  LOAD_FAST                'suffix'
              166  LOAD_FAST                'flags'
              168  LOAD_FAST                'output_type'
              170  CALL_FUNCTION_5       5  ''
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               'fd'
              176  STORE_FAST               'name'

 L. 615       178  SETUP_FINALLY       214  'to 214'

 L. 616       180  LOAD_GLOBAL              _os
              182  LOAD_METHOD              unlink
              184  LOAD_FAST                'name'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 617       190  LOAD_GLOBAL              _io
              192  LOAD_ATTR                open
              194  LOAD_FAST                'fd'
              196  LOAD_FAST                'mode'
              198  LOAD_FAST                'buffering'

 L. 618       200  LOAD_FAST                'newline'

 L. 618       202  LOAD_FAST                'encoding'

 L. 618       204  LOAD_FAST                'errors'

 L. 617       206  LOAD_CONST               ('buffering', 'newline', 'encoding', 'errors')
              208  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              210  POP_BLOCK        
              212  RETURN_VALUE     
            214_0  COME_FROM_FINALLY   178  '178'

 L. 619       214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 620       220  LOAD_GLOBAL              _os
              222  LOAD_METHOD              close
              224  LOAD_FAST                'fd'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 621       230  RAISE_VARARGS_0       0  'reraise'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'

Parse error at or near `POP_TOP' instruction at offset 148


class SpooledTemporaryFile:
    __doc__ = 'Temporary file wrapper, specialized to switch from BytesIO\n    or StringIO to a real file when it exceeds a certain size or\n    when a fileno is needed.\n    '
    _rolled = False

    def __init__(self, max_size=0, mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, *, errors=None):
        if 'b' in mode:
            self._file = _io.BytesIO()
        else:
            self._file = _io.StringIO(newline='\n')
        self._max_size = max_size
        self._rolled = False
        self._TemporaryFileArgs = {'mode':mode,  'buffering':buffering,  'suffix':suffix, 
         'prefix':prefix,  'encoding':encoding, 
         'newline':newline,  'dir':dir, 
         'errors':errors}

    def _check(self, file):
        if self._rolled:
            return
        max_size = self._max_size
        if max_size:
            if file.tell() > max_size:
                self.rollover()

    def rollover(self):
        if self._rolled:
            return
        file = self._file
        newfile = self._file = TemporaryFile(**self._TemporaryFileArgs)
        del self._TemporaryFileArgs
        newfile.write(file.getvalue())
        newfile.seekfile.tell()0
        self._rolled = True

    def __enter__(self):
        if self._file.closed:
            raise ValueError('Cannot enter context with closed file')
        return self

    def __exit__(self, exc, value, tb):
        self._file.close()

    def __iter__(self):
        return self._file.__iter__()

    def close(self):
        self._file.close()

    @property
    def closed(self):
        return self._file.closed

    @property
    def encoding(self):
        return self._file.encoding

    @property
    def errors(self):
        return self._file.errors

    def fileno(self):
        self.rollover()
        return self._file.fileno()

    def flush(self):
        self._file.flush()

    def isatty(self):
        return self._file.isatty()

    @property
    def mode(self):
        try:
            return self._file.mode
        except AttributeError:
            return self._TemporaryFileArgs['mode']

    @property
    def name--- This code section failed: ---

 L. 716         0  SETUP_FINALLY        12  'to 12'

 L. 717         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _file
                6  LOAD_ATTR                name
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 718        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    32  'to 32'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 719        26  POP_EXCEPT       
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            18  '18'
               32  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 28

    @property
    def newlines(self):
        return self._file.newlines

    def read(self, *args):
        return (self._file.read)(*args)

    def readline(self, *args):
        return (self._file.readline)(*args)

    def readlines(self, *args):
        return (self._file.readlines)(*args)

    def seek(self, *args):
        (self._file.seek)(*args)

    @property
    def softspace(self):
        return self._file.softspace

    def tell(self):
        return self._file.tell()

    def truncate(self, size=None):
        if size is None:
            self._file.truncate()
        else:
            if size > self._max_size:
                self.rollover()
            self._file.truncate(size)

    def write(self, s):
        file = self._file
        rv = file.write(s)
        self._check(file)
        return rv

    def writelines(self, iterable):
        file = self._file
        rv = file.writelines(iterable)
        self._check(file)
        return rv


class TemporaryDirectory(object):
    __doc__ = 'Create and return a temporary directory.  This has the same\n    behavior as mkdtemp but can be used as a context manager.  For\n    example:\n\n        with TemporaryDirectory() as tmpdir:\n            ...\n\n    Upon exiting the context, the directory and everything contained\n    in it are removed.\n    '

    def __init__(self, suffix=None, prefix=None, dir=None):
        self.name = mkdtemp(suffix, prefix, dir)
        self._finalizer = _weakref.finalize(self,
          (self._cleanup), (self.name), warn_message=('Implicitly cleaning up {!r}'.format(self)))

    @classmethod
    def _rmtree(cls, name):

        def onerror(func, path, exc_info):
            if issubclass(exc_info[0], PermissionError):

                def resetperms(path):
                    try:
                        _os.chflagspath0
                    except AttributeError:
                        pass
                    else:
                        _os.chmodpath448

                try:
                    if path != name:
                        resetperms(_os.path.dirname(path))
                    resetperms(path)
                    try:
                        _os.unlink(path)
                    except (IsADirectoryError, PermissionError):
                        cls._rmtree(path)

                except FileNotFoundError:
                    pass

            elif issubclass(exc_info[0], FileNotFoundError):
                pass
            else:
                raise

        _shutil.rmtree(name, onerror=onerror)

    @classmethod
    def _cleanup(cls, name, warn_message):
        cls._rmtree(name)
        _warnings.warnwarn_messageResourceWarning

    def __repr__(self):
        return '<{} {!r}>'.formatself.__class__.__name__self.name

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self._finalizer.detach():
            self._rmtree(self.name)


# global _O_TMPFILE_WORKS ## Warning: Unused global