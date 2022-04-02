# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: bz2.py
"""Interface to the libbzip2 compression library.

This module provides a file interface, classes for incremental
(de)compression, and functions for one-shot (de)compression.
"""
__all__ = [
 'BZ2File', 'BZ2Compressor', 'BZ2Decompressor',
 'open', 'compress', 'decompress']
__author__ = 'Nadeem Vawda <nadeem.vawda@gmail.com>'
from builtins import open as _builtin_open
import io, os, warnings, _compression
from threading import RLock
from _bz2 import BZ2Compressor, BZ2Decompressor
_MODE_CLOSED = 0
_MODE_READ = 1
_MODE_WRITE = 3
_sentinel = object()

class BZ2File(_compression.BaseStream):
    __doc__ = 'A file object providing transparent bzip2 (de)compression.\n\n    A BZ2File can act as a wrapper for an existing file object, or refer\n    directly to a named file on disk.\n\n    Note that BZ2File provides a *binary* file interface - data read is\n    returned as bytes, and data to be written should be given as bytes.\n    '

    def __init__(self, filename, mode='r', buffering=_sentinel, compresslevel=9):
        """Open a bzip2-compressed file.

        If filename is a str, bytes, or PathLike object, it gives the
        name of the file to be opened. Otherwise, it should be a file
        object, which will be used to read or write the compressed data.

        mode can be 'r' for reading (default), 'w' for (over)writing,
        'x' for creating exclusively, or 'a' for appending. These can
        equivalently be given as 'rb', 'wb', 'xb', and 'ab'.

        buffering is ignored since Python 3.0. Its use is deprecated.

        If mode is 'w', 'x' or 'a', compresslevel can be a number between 1
        and 9 specifying the level of compression: 1 produces the least
        compression, and 9 (default) produces the most compression.

        If mode is 'r', the input file may be the concatenation of
        multiple compressed streams.
        """
        self._lock = RLock()
        self._fp = None
        self._closefp = False
        self._mode = _MODE_CLOSED
        if buffering is not _sentinel:
            warnings.warn("Use of 'buffering' argument is deprecated and ignored since Python 3.0.", DeprecationWarning,
              stacklevel=2)
        if not 1 <= compresslevel <= 9:
            raise ValueError('compresslevel must be between 1 and 9')
        if mode in ('', 'r', 'rb'):
            mode = 'rb'
            mode_code = _MODE_READ
        elif mode in ('w', 'wb'):
            mode = 'wb'
            mode_code = _MODE_WRITE
            self._compressor = BZ2Compressor(compresslevel)
        elif mode in ('x', 'xb'):
            mode = 'xb'
            mode_code = _MODE_WRITE
            self._compressor = BZ2Compressor(compresslevel)
        elif mode in ('a', 'ab'):
            mode = 'ab'
            mode_code = _MODE_WRITE
            self._compressor = BZ2Compressor(compresslevel)
        else:
            raise ValueError('Invalid mode: %r' % (mode,))
        if isinstance(filename, (str, bytes, os.PathLike)):
            self._fp = _builtin_open(filename, mode)
            self._closefp = True
            self._mode = mode_code
        elif hasattr(filename, 'read') or hasattr(filename, 'write'):
            self._fp = filename
            self._mode = mode_code
        else:
            raise TypeError('filename must be a str, bytes, file or PathLike object')
        if self._mode == _MODE_READ:
            raw = _compression.DecompressReader((self._fp), BZ2Decompressor,
              trailing_error=OSError)
            self._buffer = io.BufferedReader(raw)
        else:
            self._pos = 0

    def close--- This code section failed: ---

 L. 118         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH          148  'to 148'
                6  POP_TOP          

 L. 119         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _mode
               12  LOAD_GLOBAL              _MODE_CLOSED
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L. 120        18  POP_BLOCK        
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            16  '16'

 L. 121        32  SETUP_FINALLY        94  'to 94'

 L. 122        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _mode
               38  LOAD_GLOBAL              _MODE_READ
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 123        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _buffer
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  JUMP_FORWARD         90  'to 90'
             56_0  COME_FROM            42  '42'

 L. 124        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _mode
               60  LOAD_GLOBAL              _MODE_WRITE
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    90  'to 90'

 L. 125        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _fp
               70  LOAD_METHOD              write
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _compressor
               76  LOAD_METHOD              flush
               78  CALL_METHOD_0         0  ''
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 126        84  LOAD_CONST               None
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _compressor
             90_0  COME_FROM            64  '64'
             90_1  COME_FROM            54  '54'
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_FINALLY    32  '32'

 L. 128        94  SETUP_FINALLY       116  'to 116'

 L. 129        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _closefp
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 130       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _fp
              106  LOAD_METHOD              close
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_FINALLY    94  '94'

 L. 132       116  LOAD_CONST               None
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _fp

 L. 133       122  LOAD_CONST               False
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _closefp

 L. 134       128  LOAD_GLOBAL              _MODE_CLOSED
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _mode

 L. 135       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _buffer
              140  END_FINALLY      
              142  END_FINALLY      
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM_WITH        4  '4'
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 20

    @property
    def closed(self):
        """True if this file is closed."""
        return self._mode == _MODE_CLOSED

    def fileno(self):
        """Return the file descriptor for the underlying file."""
        self._check_not_closed
        return self._fp.fileno

    def seekable(self):
        """Return whether the file supports seeking."""
        return self.readable and self._buffer.seekable

    def readable(self):
        """Return whether the file was opened for reading."""
        self._check_not_closed
        return self._mode == _MODE_READ

    def writable(self):
        """Return whether the file was opened for writing."""
        self._check_not_closed
        return self._mode == _MODE_WRITE

    def peek(self, n=0):
        """Return buffered data without advancing the file position.

        Always returns at least one byte of data, unless at EOF.
        The exact number of bytes returned is unspecified.
        """
        with self._lock:
            self._check_can_read
            return self._buffer.peek(n)

    def read(self, size=-1):
        """Read up to size uncompressed bytes from the file.

        If size is negative or omitted, read until EOF is reached.
        Returns b'' if the file is already at EOF.
        """
        with self._lock:
            self._check_can_read
            return self._buffer.read(size)

    def read1(self, size=-1):
        """Read up to size uncompressed bytes, while trying to avoid
        making multiple reads from the underlying stream. Reads up to a
        buffer's worth of data if size is negative.

        Returns b'' if the file is at EOF.
        """
        with self._lock:
            self._check_can_read
            if size < 0:
                size = io.DEFAULT_BUFFER_SIZE
            return self._buffer.read1(size)

    def readinto(self, b):
        """Read bytes into b.

        Returns the number of bytes read (0 for EOF).
        """
        with self._lock:
            self._check_can_read
            return self._buffer.readinto(b)

    def readline(self, size=-1):
        """Read a line of uncompressed bytes from the file.

        The terminating newline (if present) is retained. If size is
        non-negative, no more than size bytes will be read (in which
        case the line may be incomplete). Returns b'' if already at EOF.
        """
        if not isinstance(size, int):
            if not hasattr(size, '__index__'):
                raise TypeError('Integer argument expected')
            size = size.__index__
        with self._lock:
            self._check_can_read
            return self._buffer.readline(size)

    def readlines(self, size=-1):
        """Read a list of lines of uncompressed bytes from the file.

        size can be specified to control the number of lines read: no
        further lines will be read once the total size of the lines read
        so far equals or exceeds size.
        """
        if not isinstance(size, int):
            if not hasattr(size, '__index__'):
                raise TypeError('Integer argument expected')
            size = size.__index__
        with self._lock:
            self._check_can_read
            return self._buffer.readlines(size)

    def write(self, data):
        """Write a byte string to the file.

        Returns the number of uncompressed bytes written, which is
        always len(data). Note that due to buffering, the file on disk
        may not reflect the data written until close() is called.
        """
        with self._lock:
            self._check_can_write
            compressed = self._compressor.compress(data)
            self._fp.write(compressed)
            self._pos += len(data)
            return len(data)

    def writelines(self, seq):
        """Write a sequence of byte strings to the file.

        Returns the number of uncompressed bytes written.
        seq can be any iterable yielding byte strings.

        Line separators are not added between the written byte strings.
        """
        with self._lock:
            return _compression.BaseStream.writelines(self, seq)

    def seek(self, offset, whence=io.SEEK_SET):
        """Change the file position.

        The new position is specified by offset, relative to the
        position indicated by whence. Values for whence are:

            0: start of stream (default); offset must not be negative
            1: current stream position
            2: end of stream; offset must not be positive

        Returns the new file position.

        Note that seeking is emulated, so depending on the parameters,
        this operation may be extremely slow.
        """
        with self._lock:
            self._check_can_seek
            return self._buffer.seek(offset, whence)

    def tell(self):
        """Return the current file position."""
        with self._lock:
            self._check_not_closed
            if self._mode == _MODE_READ:
                return self._buffer.tell
            return self._pos


def open(filename, mode='rb', compresslevel=9, encoding=None, errors=None, newline=None):
    """Open a bzip2-compressed file in binary or text mode.

    The filename argument can be an actual filename (a str, bytes, or
    PathLike object), or an existing file object to read from or write
    to.

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or
    "ab" for binary mode, or "rt", "wt", "xt" or "at" for text mode.
    The default mode is "rb", and the default compresslevel is 9.

    For binary mode, this function is equivalent to the BZ2File
    constructor: BZ2File(filename, mode, compresslevel). In this case,
    the encoding, errors and newline arguments must not be provided.

    For text mode, a BZ2File object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error
    handling behavior, and line ending(s).

    """
    if 't' in mode:
        if 'b' in mode:
            raise ValueError('Invalid mode: %r' % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")
    bz_mode = mode.replace('t', '')
    binary_file = BZ2File(filename, bz_mode, compresslevel=compresslevel)
    if 't' in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    return binary_file


def compress(data, compresslevel=9):
    """Compress a block of data.

    compresslevel, if given, must be a number between 1 and 9.

    For incremental compression, use a BZ2Compressor object instead.
    """
    comp = BZ2Compressor(compresslevel)
    return comp.compress(data) + comp.flush


def decompress(data):
    """Decompress a block of data.

    For incremental decompression, use a BZ2Decompressor object instead.
    """
    results = []
    while True:
        if data:
            decomp = BZ2Decompressor()
            try:
                res = decomp.decompress(data)
            except OSError:
                if results:
                    break
                else:
                    raise
            else:
                results.append(res)
                if not decomp.eof:
                    raise ValueError('Compressed data ended before the end-of-stream marker was reached')
                data = decomp.unused_data

    return (b'').join(results)