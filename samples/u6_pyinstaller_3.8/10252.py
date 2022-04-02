# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
        else:
            if not 1 <= compresslevel <= 9:
                raise ValueError('compresslevel must be between 1 and 9')
            else:
                if mode in ('', 'r', 'rb'):
                    mode = 'rb'
                    mode_code = _MODE_READ
                else:
                    if mode in ('w', 'wb'):
                        mode = 'wb'
                        mode_code = _MODE_WRITE
                        self._compressor = BZ2Compressor(compresslevel)
                    else:
                        if mode in ('x', 'xb'):
                            mode = 'xb'
                            mode_code = _MODE_WRITE
                            self._compressor = BZ2Compressor(compresslevel)
                        else:
                            if mode in ('a', 'ab'):
                                mode = 'ab'
                                mode_code = _MODE_WRITE
                                self._compressor = BZ2Compressor(compresslevel)
                            else:
                                raise ValueError('Invalid mode: %r' % (mode,))
                if isinstance(filename, (str, bytes, os.PathLike)):
                    self._fp = _builtin_open(filename, mode)
                    self._closefp = True
                    self._mode = mode_code
                else:
                    if hasattr(filename, 'read') or hasattr(filename, 'write'):
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

    def peek--- This code section failed: ---

 L. 167         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           40  'to 40'
                6  POP_TOP          

 L. 168         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_read
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 172        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _buffer
               20  LOAD_METHOD              peek
               22  LOAD_FAST                'n'
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH        4  '4'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 28

    def read--- This code section failed: ---

 L. 180         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           40  'to 40'
                6  POP_TOP          

 L. 181         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_read
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 182        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _buffer
               20  LOAD_METHOD              read
               22  LOAD_FAST                'size'
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH        4  '4'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 28

    def read1--- This code section failed: ---

 L. 191         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           54  'to 54'
                6  POP_TOP          

 L. 192         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_read
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 193        16  LOAD_FAST                'size'
               18  LOAD_CONST               0
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 194        24  LOAD_GLOBAL              io
               26  LOAD_ATTR                DEFAULT_BUFFER_SIZE
               28  STORE_FAST               'size'
             30_0  COME_FROM            22  '22'

 L. 195        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _buffer
               34  LOAD_METHOD              read1
               36  LOAD_FAST                'size'
               38  CALL_METHOD_1         1  ''
               40  POP_BLOCK        
               42  ROT_TWO          
               44  BEGIN_FINALLY    
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  POP_FINALLY           0  ''
               52  RETURN_VALUE     
             54_0  COME_FROM_WITH        4  '4'
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 42

    def readinto--- This code section failed: ---

 L. 202         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           40  'to 40'
                6  POP_TOP          

 L. 203         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_read
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 204        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _buffer
               20  LOAD_METHOD              readinto
               22  LOAD_FAST                'b'
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH        4  '4'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 28

    def readline--- This code section failed: ---

 L. 213         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'size'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     36  'to 36'

 L. 214        10  LOAD_GLOBAL              hasattr
               12  LOAD_FAST                'size'
               14  LOAD_STR                 '__index__'
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 215        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'Integer argument expected'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 216        28  LOAD_FAST                'size'
               30  LOAD_METHOD              __index__
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'size'
             36_0  COME_FROM             8  '8'

 L. 217        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _lock
               40  SETUP_WITH           76  'to 76'
               42  POP_TOP          

 L. 218        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _check_can_read
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L. 219        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _buffer
               56  LOAD_METHOD              readline
               58  LOAD_FAST                'size'
               60  CALL_METHOD_1         1  ''
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM_WITH       40  '40'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 64

    def readlines--- This code section failed: ---

 L. 228         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'size'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     36  'to 36'

 L. 229        10  LOAD_GLOBAL              hasattr
               12  LOAD_FAST                'size'
               14  LOAD_STR                 '__index__'
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 230        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'Integer argument expected'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 231        28  LOAD_FAST                'size'
               30  LOAD_METHOD              __index__
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'size'
             36_0  COME_FROM             8  '8'

 L. 232        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _lock
               40  SETUP_WITH           76  'to 76'
               42  POP_TOP          

 L. 233        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _check_can_read
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L. 234        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _buffer
               56  LOAD_METHOD              readlines
               58  LOAD_FAST                'size'
               60  CALL_METHOD_1         1  ''
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM_WITH       40  '40'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 64

    def write--- This code section failed: ---

 L. 243         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           78  'to 78'
                6  POP_TOP          

 L. 244         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_write
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 245        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _compressor
               20  LOAD_METHOD              compress
               22  LOAD_FAST                'data'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'compressed'

 L. 246        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _fp
               32  LOAD_METHOD              write
               34  LOAD_FAST                'compressed'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 247        40  LOAD_FAST                'self'
               42  DUP_TOP          
               44  LOAD_ATTR                _pos
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'data'
               50  CALL_FUNCTION_1       1  ''
               52  INPLACE_ADD      
               54  ROT_TWO          
               56  STORE_ATTR               _pos

 L. 248        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'data'
               62  CALL_FUNCTION_1       1  ''
               64  POP_BLOCK        
               66  ROT_TWO          
               68  BEGIN_FINALLY    
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  POP_FINALLY           0  ''
               76  RETURN_VALUE     
             78_0  COME_FROM_WITH        4  '4'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 66

    def writelines--- This code section failed: ---

 L. 258         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 259         8  LOAD_GLOBAL              _compression
               10  LOAD_ATTR                BaseStream
               12  LOAD_METHOD              writelines
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'seq'
               18  CALL_METHOD_2         2  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22

    def seek--- This code section failed: ---

 L. 276         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           42  'to 42'
                6  POP_TOP          

 L. 277         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_can_seek
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 278        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _buffer
               20  LOAD_METHOD              seek
               22  LOAD_FAST                'offset'
               24  LOAD_FAST                'whence'
               26  CALL_METHOD_2         2  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH        4  '4'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30

    def tell--- This code section failed: ---

 L. 282         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           66  'to 66'
                6  POP_TOP          

 L. 283         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _check_not_closed
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 284        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _mode
               20  LOAD_GLOBAL              _MODE_READ
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    48  'to 48'

 L. 285        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _buffer
               30  LOAD_METHOD              tell
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  ROT_TWO          
               38  BEGIN_FINALLY    
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  POP_FINALLY           0  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            24  '24'

 L. 286        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _pos
               52  POP_BLOCK        
               54  ROT_TWO          
               56  BEGIN_FINALLY    
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  POP_FINALLY           0  ''
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH        4  '4'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 36


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
    bz_mode = mode.replace't'''
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


def decompress--- This code section failed: ---

 L. 346         0  BUILD_LIST_0          0 
                2  STORE_FAST               'results'

 L. 347         4  LOAD_FAST                'data'
                6  POP_JUMP_IF_FALSE    94  'to 94'

 L. 348         8  LOAD_GLOBAL              BZ2Decompressor
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'decomp'

 L. 349        14  SETUP_FINALLY        30  'to 30'

 L. 350        16  LOAD_FAST                'decomp'
               18  LOAD_METHOD              decompress
               20  LOAD_FAST                'data'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'res'
               26  POP_BLOCK        
               28  JUMP_FORWARD         62  'to 62'
             30_0  COME_FROM_FINALLY    14  '14'

 L. 351        30  DUP_TOP          
               32  LOAD_GLOBAL              OSError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    60  'to 60'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 352        44  LOAD_FAST                'results'
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 353        48  POP_EXCEPT       
               50  BREAK_LOOP           94  'to 94'
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            46  '46'

 L. 355        54  RAISE_VARARGS_0       0  'reraise'
             56_0  COME_FROM            52  '52'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            36  '36'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            28  '28'

 L. 356        62  LOAD_FAST                'results'
               64  LOAD_METHOD              append
               66  LOAD_FAST                'res'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 357        72  LOAD_FAST                'decomp'
               74  LOAD_ATTR                eof
               76  POP_JUMP_IF_TRUE     86  'to 86'

 L. 358        78  LOAD_GLOBAL              ValueError
               80  LOAD_STR                 'Compressed data ended before the end-of-stream marker was reached'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L. 360        86  LOAD_FAST                'decomp'
               88  LOAD_ATTR                unused_data
               90  STORE_FAST               'data'
               92  JUMP_BACK             4  'to 4'
             94_0  COME_FROM_EXCEPT_CLAUSE    50  '50'
             94_1  COME_FROM_EXCEPT_CLAUSE     6  '6'

 L. 361        94  LOAD_CONST               b''
               96  LOAD_METHOD              join
               98  LOAD_FAST                'results'
              100  CALL_METHOD_1         1  ''
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 94_1