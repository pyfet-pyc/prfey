# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
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
import weakref as _weakref, _thread
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
if hasattr(_os, 'lstat'):
    _stat = _os.lstat
elif hasattr(_os, 'stat'):
    _stat = _os.stat
else:

    def _stat(fn):
        fd = _os.open(fn, _os.O_RDONLY)
        _os.close(fd)


def _exists(fn):
    try:
        _stat(fn)
    except OSError:
        return False
    else:
        return True


def _infer_return_type(*args):
    """Look at the type of all args and divine their implied return type."""
    return_type = None
    for arg in args:
        if arg is None:
            continue
        if isinstance(arg, bytes):
            if return_type is str:
                raise TypeError("Can't mix bytes and non-bytes in path components.")
            else:
                return_type = bytes
        if return_type is bytes:
            raise TypeError("Can't mix bytes and non-bytes in path components.")
        else:
            return_type = str

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

    return dirlist


def _get_default_tempdir():
    """Calculate the default directory to use for temporary files.
    This routine should be called exactly once.

    We determine whether or not a candidate temp dir is usable by
    trying to create and write to a file in that directory.  If this
    is successful, the test file is deleted.  To prevent denial of
    service, the name of the test file must be randomized."""
    namer = _RandomNameSequence()
    dirlist = _candidate_tempdir_list()
    for dir in dirlist:
        if dir != _os.curdir:
            dir = _os.path.abspath(dir)
        else:
            for seq in range(100):
                name = next(namer)
                filename = _os.path.join(dir, name)
                try:
                    fd = _os.open(filename, _bin_openflags, 384)
                    try:
                        try:
                            with _io.open(fd, 'wb', closefd=False) as fp:
                                fp.write(b'blat')
                        finally:
                            _os.close(fd)

                    finally:
                        _os.unlink(filename)

                    return dir
                except FileExistsError:
                    pass
                except PermissionError:
                    if _os.name == 'nt':
                        if _os.path.isdir(dir):
                            if _os.access(dir, _os.W_OK):
                                continue
                    break
                except OSError:
                    break

    raise FileNotFoundError(_errno.ENOENT, 'No usable temporary directory found in %s' % dirlist)


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

 L. 250         0  LOAD_GLOBAL              _get_candidate_names
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'names'

 L. 251         6  LOAD_FAST                'output_type'
                8  LOAD_GLOBAL              bytes
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L. 252        14  LOAD_GLOBAL              map
               16  LOAD_GLOBAL              _os
               18  LOAD_ATTR                fsencode
               20  LOAD_FAST                'names'
               22  CALL_FUNCTION_2       2  '2 positional arguments'
               24  STORE_FAST               'names'
             26_0  COME_FROM            12  '12'

 L. 254        26  SETUP_LOOP          190  'to 190'
               28  LOAD_GLOBAL              range
               30  LOAD_GLOBAL              TMP_MAX
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  GET_ITER         
             36_0  COME_FROM           160  '160'
             36_1  COME_FROM           104  '104'
               36  FOR_ITER            188  'to 188'
               38  STORE_FAST               'seq'

 L. 255        40  LOAD_GLOBAL              next
               42  LOAD_FAST                'names'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'name'

 L. 256        48  LOAD_GLOBAL              _os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              join
               54  LOAD_FAST                'dir'
               56  LOAD_FAST                'pre'
               58  LOAD_FAST                'name'
               60  BINARY_ADD       
               62  LOAD_FAST                'suf'
               64  BINARY_ADD       
               66  CALL_METHOD_2         2  '2 positional arguments'
               68  STORE_FAST               'file'

 L. 257        70  SETUP_EXCEPT         90  'to 90'

 L. 258        72  LOAD_GLOBAL              _os
               74  LOAD_METHOD              open
               76  LOAD_FAST                'file'
               78  LOAD_FAST                'flags'
               80  LOAD_CONST               384
               82  CALL_METHOD_3         3  '3 positional arguments'
               84  STORE_FAST               'fd'
               86  POP_BLOCK        
               88  JUMP_FORWARD        172  'to 172'
             90_0  COME_FROM_EXCEPT     70  '70'

 L. 259        90  DUP_TOP          
               92  LOAD_GLOBAL              FileExistsError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   110  'to 110'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 260       104  CONTINUE_LOOP        36  'to 36'
              106  POP_EXCEPT       
              108  JUMP_FORWARD        172  'to 172'
            110_0  COME_FROM            96  '96'

 L. 261       110  DUP_TOP          
              112  LOAD_GLOBAL              PermissionError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   170  'to 170'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 264       124  LOAD_GLOBAL              _os
              126  LOAD_ATTR                name
              128  LOAD_STR                 'nt'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   164  'to 164'
              134  LOAD_GLOBAL              _os
              136  LOAD_ATTR                path
              138  LOAD_METHOD              isdir
              140  LOAD_FAST                'dir'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 265       146  LOAD_GLOBAL              _os
              148  LOAD_METHOD              access
              150  LOAD_FAST                'dir'
              152  LOAD_GLOBAL              _os
              154  LOAD_ATTR                W_OK
              156  CALL_METHOD_2         2  '2 positional arguments'
              158  POP_JUMP_IF_FALSE   164  'to 164'

 L. 266       160  CONTINUE_LOOP        36  'to 36'
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           158  '158'
            164_1  COME_FROM           144  '144'
            164_2  COME_FROM           132  '132'

 L. 268       164  RAISE_VARARGS_0       0  'reraise'
            166_0  COME_FROM           162  '162'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           116  '116'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           108  '108'
            172_2  COME_FROM            88  '88'

 L. 269       172  LOAD_FAST                'fd'
              174  LOAD_GLOBAL              _os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              abspath
              180  LOAD_FAST                'file'
              182  CALL_METHOD_1         1  '1 positional argument'
              184  BUILD_TUPLE_2         2 
              186  RETURN_VALUE     
              188  POP_BLOCK        
            190_0  COME_FROM_LOOP       26  '26'

 L. 271       190  LOAD_GLOBAL              FileExistsError
              192  LOAD_GLOBAL              _errno
              194  LOAD_ATTR                EEXIST

 L. 272       196  LOAD_STR                 'No usable temporary file name found'
              198  CALL_FUNCTION_2       2  '2 positional arguments'
              200  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_EXCEPT' instruction at offset 166


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

 L. 356         0  LOAD_GLOBAL              _sanitize_params
                2  LOAD_FAST                'prefix'
                4  LOAD_FAST                'suffix'
                6  LOAD_FAST                'dir'
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  UNPACK_SEQUENCE_4     4 
               12  STORE_FAST               'prefix'
               14  STORE_FAST               'suffix'
               16  STORE_FAST               'dir'
               18  STORE_FAST               'output_type'

 L. 358        20  LOAD_GLOBAL              _get_candidate_names
               22  CALL_FUNCTION_0       0  '0 positional arguments'
               24  STORE_FAST               'names'

 L. 359        26  LOAD_FAST                'output_type'
               28  LOAD_GLOBAL              bytes
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 360        34  LOAD_GLOBAL              map
               36  LOAD_GLOBAL              _os
               38  LOAD_ATTR                fsencode
               40  LOAD_FAST                'names'
               42  CALL_FUNCTION_2       2  '2 positional arguments'
               44  STORE_FAST               'names'
             46_0  COME_FROM            32  '32'

 L. 362        46  SETUP_LOOP          196  'to 196'
               48  LOAD_GLOBAL              range
               50  LOAD_GLOBAL              TMP_MAX
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  GET_ITER         
             56_0  COME_FROM           178  '178'
             56_1  COME_FROM           122  '122'
               56  FOR_ITER            194  'to 194'
               58  STORE_FAST               'seq'

 L. 363        60  LOAD_GLOBAL              next
               62  LOAD_FAST                'names'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  STORE_FAST               'name'

 L. 364        68  LOAD_GLOBAL              _os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              join
               74  LOAD_FAST                'dir'
               76  LOAD_FAST                'prefix'
               78  LOAD_FAST                'name'
               80  BINARY_ADD       
               82  LOAD_FAST                'suffix'
               84  BINARY_ADD       
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  STORE_FAST               'file'

 L. 365        90  SETUP_EXCEPT        108  'to 108'

 L. 366        92  LOAD_GLOBAL              _os
               94  LOAD_METHOD              mkdir
               96  LOAD_FAST                'file'
               98  LOAD_CONST               448
              100  CALL_METHOD_2         2  '2 positional arguments'
              102  POP_TOP          
              104  POP_BLOCK        
              106  JUMP_FORWARD        190  'to 190'
            108_0  COME_FROM_EXCEPT     90  '90'

 L. 367       108  DUP_TOP          
              110  LOAD_GLOBAL              FileExistsError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   128  'to 128'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 368       122  CONTINUE_LOOP        56  'to 56'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        190  'to 190'
            128_0  COME_FROM           114  '114'

 L. 369       128  DUP_TOP          
              130  LOAD_GLOBAL              PermissionError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   188  'to 188'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 372       142  LOAD_GLOBAL              _os
              144  LOAD_ATTR                name
              146  LOAD_STR                 'nt'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   182  'to 182'
              152  LOAD_GLOBAL              _os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              isdir
              158  LOAD_FAST                'dir'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_JUMP_IF_FALSE   182  'to 182'

 L. 373       164  LOAD_GLOBAL              _os
              166  LOAD_METHOD              access
              168  LOAD_FAST                'dir'
              170  LOAD_GLOBAL              _os
              172  LOAD_ATTR                W_OK
              174  CALL_METHOD_2         2  '2 positional arguments'
              176  POP_JUMP_IF_FALSE   182  'to 182'

 L. 374       178  CONTINUE_LOOP        56  'to 56'
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           176  '176'
            182_1  COME_FROM           162  '162'
            182_2  COME_FROM           150  '150'

 L. 376       182  RAISE_VARARGS_0       0  'reraise'
            184_0  COME_FROM           180  '180'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           134  '134'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           126  '126'
            190_2  COME_FROM           106  '106'

 L. 377       190  LOAD_FAST                'file'
              192  RETURN_VALUE     
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP       46  '46'

 L. 379       196  LOAD_GLOBAL              FileExistsError
              198  LOAD_GLOBAL              _errno
              200  LOAD_ATTR                EEXIST

 L. 380       202  LOAD_STR                 'No usable temporary directory name found'
              204  CALL_FUNCTION_2       2  '2 positional arguments'
              206  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_EXCEPT' instruction at offset 184


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
        file = _os.path.join(dir, prefix + name + suffix)
        if not _exists(file):
            return file

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
        result = self.file.__exit__(exc, value, tb)
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


def NamedTemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, delete=True):
    """Create and return a temporary file.
    Arguments:
    'prefix', 'suffix', 'dir' -- as for mkstemp.
    'mode' -- the mode argument to io.open (default "w+b").
    'buffering' -- the buffer size argument to io.open (default -1).
    'encoding' -- the encoding argument to io.open (default None)
    'newline' -- the newline argument to io.open (default None)
    'delete' -- whether the file is deleted on close (default True).
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
          encoding=encoding)
        return _TemporaryFileWrapper(file, name, delete)
    except BaseException:
        _os.unlink(name)
        _os.close(fd)
        raise


if _os.name != 'posix' or _os.sys.platform == 'cygwin':
    TemporaryFile = NamedTemporaryFile
else:
    _O_TMPFILE_WORKS = hasattr(_os, 'O_TMPFILE')

    def TemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None):
        """Create and return a temporary file.
        Arguments:
        'prefix', 'suffix', 'dir' -- as for mkstemp.
        'mode' -- the mode argument to io.open (default "w+b").
        'buffering' -- the buffer size argument to io.open (default -1).
        'encoding' -- the encoding argument to io.open (default None)
        'newline' -- the newline argument to io.open (default None)
        The file is created as mkstemp() would do it.

        Returns an object with a file-like interface.  The file has no
        name, and will cease to exist when it is closed.
        """
        global _O_TMPFILE_WORKS
        prefix, suffix, dir, output_type = _sanitize_params(prefix, suffix, dir)
        flags = _bin_openflags
        if _O_TMPFILE_WORKS:
            try:
                flags2 = (flags | _os.O_TMPFILE) & ~_os.O_CREAT
                fd = _os.open(dir, flags2, 384)
            except IsADirectoryError:
                _O_TMPFILE_WORKS = False
            except OSError:
                pass
            else:
                try:
                    return _io.open(fd, mode, buffering=buffering, newline=newline,
                      encoding=encoding)
                except:
                    _os.close(fd)
                    raise

        fd, name = _mkstemp_inner(dir, prefix, suffix, flags, output_type)
        try:
            _os.unlink(name)
            return _io.open(fd, mode, buffering=buffering, newline=newline,
              encoding=encoding)
        except:
            _os.close(fd)
            raise


class SpooledTemporaryFile:
    __doc__ = 'Temporary file wrapper, specialized to switch from BytesIO\n    or StringIO to a real file when it exceeds a certain size or\n    when a fileno is needed.\n    '
    _rolled = False

    def __init__(self, max_size=0, mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None):
        if 'b' in mode:
            self._file = _io.BytesIO()
        else:
            self._file = _io.StringIO(newline='\n')
        self._max_size = max_size
        self._rolled = False
        self._TemporaryFileArgs = {'mode':mode,  'buffering':buffering,  'suffix':suffix, 
         'prefix':prefix,  'encoding':encoding, 
         'newline':newline,  'dir':dir}

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
        newfile.seek(file.tell(), 0)
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
        try:
            return self._file.encoding
        except AttributeError:
            if 'b' in self._TemporaryFileArgs['mode']:
                raise
            return self._TemporaryFileArgs['encoding']

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
    def name(self):
        try:
            return self._file.name
        except AttributeError:
            return

    @property
    def newlines(self):
        try:
            return self._file.newlines
        except AttributeError:
            if 'b' in self._TemporaryFileArgs['mode']:
                raise
            return self._TemporaryFileArgs['newline']

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
    def _cleanup(cls, name, warn_message):
        _shutil.rmtree(name)
        _warnings.warn(warn_message, ResourceWarning)

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self._finalizer.detach():
            _shutil.rmtree(self.name)