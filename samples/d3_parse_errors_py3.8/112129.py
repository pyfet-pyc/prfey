# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: gzip.py
"""Functions that read and write gzipped files.

The user of the file doesn't have to worry about the compression,
but random access is not allowed."""
import struct, sys, time, os, zlib, builtins, io, _compression
__all__ = [
 'BadGzipFile', 'GzipFile', 'open', 'compress', 'decompress']
FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = (1, 2, 4, 8, 16)
READ, WRITE = (1, 2)
_COMPRESS_LEVEL_FAST = 1
_COMPRESS_LEVEL_TRADEOFF = 6
_COMPRESS_LEVEL_BEST = 9

def open(filename, mode='rb', compresslevel=_COMPRESS_LEVEL_BEST, encoding=None, errors=None, newline=None):
    """Open a gzip-compressed file in binary or text mode.

    The filename argument can be an actual filename (a str or bytes object), or
    an existing file object to read from or write to.

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab" for
    binary mode, or "rt", "wt", "xt" or "at" for text mode. The default mode is
    "rb", and the default compresslevel is 9.

    For binary mode, this function is equivalent to the GzipFile constructor:
    GzipFile(filename, mode, compresslevel). In this case, the encoding, errors
    and newline arguments must not be provided.

    For text mode, a GzipFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).

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
    gz_mode = mode.replace('t', '')
    if isinstance(filename, (str, bytes, os.PathLike)):
        binary_file = GzipFile(filename, gz_mode, compresslevel)
    elif hasattr(filename, 'read') or hasattr(filename, 'write'):
        binary_file = GzipFile(None, gz_mode, compresslevel, filename)
    else:
        raise TypeError('filename must be a str or bytes object, or a file')
    if 't' in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    return binary_file


def write32u(output, value):
    output.write(struct.pack('<L', value))


class _PaddedFile:
    __doc__ = "Minimal read-only file object that prepends a string to the contents\n    of an actual file. Shouldn't be used outside of gzip.py, as it lacks\n    essential functionality."

    def __init__(self, f, prepend=b''):
        self._buffer = prepend
        self._length = len(prepend)
        self.file = f
        self._read = 0

    def read(self, size):
        if self._read is None:
            return self.file.read(size)
        if self._read + size <= self._length:
            read = self._read
            self._read += size
            return self._buffer[read:self._read]
        read = self._read
        self._read = None
        return self._buffer[read:] + self.file.read(size - self._length + read)

    def prepend(self, prepend=b''):
        if self._read is None:
            self._buffer = prepend
        else:
            self._read -= len(prepend)
            return
        self._length = len(self._buffer)
        self._read = 0

    def seek(self, off):
        self._read = None
        self._buffer = None
        return self.file.seek(off)

    def seekable(self):
        return True


class BadGzipFile(OSError):
    __doc__ = 'Exception raised in some cases for invalid gzip files.'


class GzipFile(_compression.BaseStream):
    __doc__ = 'The GzipFile class simulates most of the methods of a file object with\n    the exception of the truncate() method.\n\n    This class only supports opening files in binary mode. If you need to open a\n    compressed file in text mode, use the gzip.open() function.\n\n    '
    myfileobj = None

    def __init__(self, filename=None, mode=None, compresslevel=_COMPRESS_LEVEL_BEST, fileobj=None, mtime=None):
        """Constructor for the GzipFile class.

        At least one of fileobj and filename must be given a
        non-trivial value.

        The new class instance is based on fileobj, which can be a regular
        file, an io.BytesIO object, or any other object which simulates a file.
        It defaults to None, in which case filename is opened to provide
        a file object.

        When fileobj is not None, the filename argument is only used to be
        included in the gzip file header, which may include the original
        filename of the uncompressed file.  It defaults to the filename of
        fileobj, if discernible; otherwise, it defaults to the empty string,
        and in this case the original filename is not included in the header.

        The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x', or
        'xb' depending on whether the file will be read or written.  The default
        is the mode of fileobj if discernible; otherwise, the default is 'rb'.
        A mode of 'r' is equivalent to one of 'rb', and similarly for 'w' and
        'wb', 'a' and 'ab', and 'x' and 'xb'.

        The compresslevel argument is an integer from 0 to 9 controlling the
        level of compression; 1 is fastest and produces the least compression,
        and 9 is slowest and produces the most compression. 0 is no compression
        at all. The default is 9.

        The mtime argument is an optional numeric timestamp to be written
        to the last modification time field in the stream when compressing.
        If omitted or None, the current time is used.

        """
        if mode:
            if 't' in mode or ('U' in mode):
                raise ValueError('Invalid mode: {!r}'.format(mode))
            if mode:
                if 'b' not in mode:
                    mode += 'b'
            if fileobj is None:
                fileobj = self.myfileobj = builtins.open(filename, mode or 'rb')
            if filename is None:
                filename = getattr(fileobj, 'name', '')
                if not isinstance(filename, (str, bytes)):
                    filename = ''
            else:
                filename = os.fspath(filename)
            if mode is None:
                mode = getattr(fileobj, 'mode', 'rb')
            if mode.startswith('r'):
                self.mode = READ
                raw = _GzipReader(fileobj)
                self._buffer = io.BufferedReader(raw)
                self.name = filename
            elif mode.startswith(('w', 'a', 'x')):
                self.mode = WRITE
                self._init_write(filename)
                self.compress = zlib.compressobj(compresslevel, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
                self._write_mtime = mtime
            else:
                raise ValueError('Invalid mode: {!r}'.format(mode))
            self.fileobj = fileobj
            if self.mode == WRITE:
                self._write_gzip_header()

    @property
    def filename(self):
        import warnings
        warnings.warn('use the name attribute', DeprecationWarning, 2)
        if self.mode == WRITE:
            if self.name[-3:] != '.gz':
                return self.name + '.gz'
        return self.name

    @property
    def mtime(self):
        """Last modification time read from stream, or None"""
        return self._buffer.raw._last_mtime

    def __repr__(self):
        s = repr(self.fileobj)
        return '<gzip ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    def _init_write(self, filename):
        self.name = filename
        self.crc = zlib.crc32(b'')
        self.size = 0
        self.writebuf = []
        self.bufsize = 0
        self.offset = 0

    def _write_gzip_header(self):
        self.fileobj.write(b'\x1f\x8b')
        self.fileobj.write(b'\x08')
        try:
            fname = os.path.basename(self.name)
            if not isinstance(fname, bytes):
                fname = fname.encode('latin-1')
            if fname.endswith(b'.gz'):
                fname = fname[:-3]
        except UnicodeEncodeError:
            fname = b''
        else:
            flags = 0
            if fname:
                flags = FNAME
            self.fileobj.write(chr(flags).encode('latin-1'))
            mtime = self._write_mtime
            if mtime is None:
                mtime = time.time()
            write32u(self.fileobj, int(mtime))
            self.fileobj.write(b'\x02')
            self.fileobj.write(b'\xff')
            if fname:
                self.fileobj.write(fname + b'\x00')

    def write(self, data):
        self._check_not_closed()
        if self.mode != WRITE:
            import errno
            raise OSError(errno.EBADF, 'write() on read-only GzipFile object')
        if self.fileobj is None:
            raise ValueError('write() on closed GzipFile object')
        if isinstance(data, bytes):
            length = len(data)
        else:
            data = memoryview(data)
            length = data.nbytes
        if length > 0:
            self.fileobj.write(self.compress.compress(data))
            self.size += length
            self.crc = zlib.crc32(data, self.crc)
            self.offset += length
        return length

    def read(self, size=-1):
        self._check_not_closed()
        if self.mode != READ:
            import errno
            raise OSError(errno.EBADF, 'read() on write-only GzipFile object')
        return self._buffer.read(size)

    def read1(self, size=-1):
        """Implements BufferedIOBase.read1()

        Reads up to a buffer's worth of data if size is negative."""
        self._check_not_closed()
        if self.mode != READ:
            import errno
            raise OSError(errno.EBADF, 'read1() on write-only GzipFile object')
        if size < 0:
            size = io.DEFAULT_BUFFER_SIZE
        return self._buffer.read1(size)

    def peek(self, n):
        self._check_not_closed()
        if self.mode != READ:
            import errno
            raise OSError(errno.EBADF, 'peek() on write-only GzipFile object')
        return self._buffer.peek(n)

    @property
    def closed(self):
        return self.fileobj is None

    def close(self):
        fileobj = self.fileobj
        if fileobj is None:
            return
        self.fileobj = None
        try:
            if self.mode == WRITE:
                fileobj.write(self.compress.flush())
                write32u(fileobj, self.crc)
                write32u(fileobj, self.size & 4294967295)
            elif self.mode == READ:
                self._buffer.close()
        finally:
            myfileobj = self.myfileobj
            if myfileobj:
                self.myfileobj = None
                myfileobj.close()

    def flush(self, zlib_mode=zlib.Z_SYNC_FLUSH):
        self._check_not_closed()
        if self.mode == WRITE:
            self.fileobj.write(self.compress.flush(zlib_mode))
            self.fileobj.flush()

    def fileno(self):
        """Invoke the underlying file object's fileno() method.

        This will raise AttributeError if the underlying file object
        doesn't support fileno().
        """
        return self.fileobj.fileno()

    def rewind(self):
        """Return the uncompressed stream file position indicator to the
        beginning of the file"""
        if self.mode != READ:
            raise OSError("Can't rewind in write mode")
        self._buffer.seek(0)

    def readable(self):
        return self.mode == READ

    def writable(self):
        return self.mode == WRITE

    def seekable(self):
        return True

    def seek(self, offset, whence=io.SEEK_SET):
        if self.mode == WRITE:
            if whence != io.SEEK_SET:
                if whence == io.SEEK_CUR:
                    offset = self.offset + offset
                else:
                    raise ValueError('Seek from end not supported')
            if offset < self.offset:
                raise OSError('Negative seek in write mode')
            count = offset - self.offset
            chunk = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            for i in range(count // 1024):
                self.write(chunk)
            else:
                self.write(b'\x00' * (count % 1024))

        elif self.mode == READ:
            self._check_not_closed()
            return self._buffer.seek(offset, whence)
        return self.offset

    def readline(self, size=-1):
        self._check_not_closed()
        return self._buffer.readline(size)


class _GzipReader(_compression.DecompressReader):

    def __init__(self, fp):
        super().__init__((_PaddedFile(fp)), (zlib.decompressobj), wbits=(-zlib.MAX_WBITS))
        self._new_member = True
        self._last_mtime = None

    def _init_read(self):
        self._crc = zlib.crc32(b'')
        self._stream_size = 0

    def _read_exact(self, n):
        """Read exactly *n* bytes from `self._fp`

        This method is required because self._fp may be unbuffered,
        i.e. return short reads.
        """
        data = self._fp.read(n)
        while True:
            if len(data) < n:
                b = self._fp.read(n - len(data))
                if not b:
                    raise EOFError('Compressed file ended before the end-of-stream marker was reached')
                data += b

        return data

    def _read_gzip_header--- This code section failed: ---

 L. 416         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               2
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'magic'

 L. 417        12  LOAD_FAST                'magic'
               14  LOAD_CONST               b''
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 418        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 420        24  LOAD_FAST                'magic'
               26  LOAD_CONST               b'\x1f\x8b'
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L. 421        32  LOAD_GLOBAL              BadGzipFile
               34  LOAD_STR                 'Not a gzipped file (%r)'
               36  LOAD_FAST                'magic'
               38  BINARY_MODULO    
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            30  '30'

 L. 424        44  LOAD_GLOBAL              struct
               46  LOAD_METHOD              unpack
               48  LOAD_STR                 '<BBIxx'
               50  LOAD_FAST                'self'
               52  LOAD_METHOD              _read_exact
               54  LOAD_CONST               8
               56  CALL_METHOD_1         1  ''
               58  CALL_METHOD_2         2  ''

 L. 423        60  UNPACK_SEQUENCE_3     3 
               62  STORE_FAST               'method'
               64  STORE_FAST               'flag'

 L. 424        66  LOAD_FAST                'self'
               68  STORE_ATTR               _last_mtime

 L. 425        70  LOAD_FAST                'method'
               72  LOAD_CONST               8
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 426        78  LOAD_GLOBAL              BadGzipFile
               80  LOAD_STR                 'Unknown compression method'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L. 428        86  LOAD_FAST                'flag'
               88  LOAD_GLOBAL              FEXTRA
               90  BINARY_AND       
               92  POP_JUMP_IF_FALSE   124  'to 124'

 L. 430        94  LOAD_GLOBAL              struct
               96  LOAD_METHOD              unpack
               98  LOAD_STR                 '<H'
              100  LOAD_FAST                'self'
              102  LOAD_METHOD              _read_exact
              104  LOAD_CONST               2
              106  CALL_METHOD_1         1  ''
              108  CALL_METHOD_2         2  ''
              110  UNPACK_SEQUENCE_1     1 
              112  STORE_FAST               'extra_len'

 L. 431       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _read_exact
              118  LOAD_FAST                'extra_len'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM            92  '92'

 L. 432       124  LOAD_FAST                'flag'
              126  LOAD_GLOBAL              FNAME
              128  BINARY_AND       
              130  POP_JUMP_IF_FALSE   160  'to 160'
            132_0  COME_FROM           158  '158'
            132_1  COME_FROM           154  '154'

 L. 435       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _fp
              136  LOAD_METHOD              read
              138  LOAD_CONST               1
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               's'

 L. 436       144  LOAD_FAST                's'
              146  POP_JUMP_IF_FALSE   160  'to 160'
              148  LOAD_FAST                's'
              150  LOAD_CONST               b'\x00'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE_BACK   132  'to 132'

 L. 437       156  JUMP_FORWARD        160  'to 160'
              158  JUMP_BACK           132  'to 132'
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           146  '146'
            160_2  COME_FROM           130  '130'

 L. 438       160  LOAD_FAST                'flag'
              162  LOAD_GLOBAL              FCOMMENT
              164  BINARY_AND       
              166  POP_JUMP_IF_FALSE   196  'to 196'
            168_0  COME_FROM           194  '194'
            168_1  COME_FROM           190  '190'

 L. 441       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _fp
              172  LOAD_METHOD              read
              174  LOAD_CONST               1
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               's'

 L. 442       180  LOAD_FAST                's'
              182  POP_JUMP_IF_FALSE   196  'to 196'
              184  LOAD_FAST                's'
              186  LOAD_CONST               b'\x00'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE_BACK   168  'to 168'

 L. 443       192  JUMP_FORWARD        196  'to 196'
              194  JUMP_BACK           168  'to 168'
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           182  '182'
            196_2  COME_FROM           166  '166'

 L. 444       196  LOAD_FAST                'flag'
              198  LOAD_GLOBAL              FHCRC
              200  BINARY_AND       
              202  POP_JUMP_IF_FALSE   214  'to 214'

 L. 445       204  LOAD_FAST                'self'
              206  LOAD_METHOD              _read_exact
              208  LOAD_CONST               2
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
            214_0  COME_FROM           202  '202'

 L. 446       214  LOAD_CONST               True
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 158

    def read(self, size=-1):
        if size < 0:
            return self.readall()
        if not size:
            return b''
            while True:
                if self._decompressor.eof:
                    self._read_eof()
                    self._new_member = True
                    self._decompressor = (self._decomp_factory)(**self._decomp_args)
                if self._new_member:
                    self._init_read()
                    if not self._read_gzip_header():
                        self._size = self._pos
                        return b''
                    self._new_member = False
                buf = self._fp.read(io.DEFAULT_BUFFER_SIZE)
                uncompress = self._decompressor.decompress(buf, size)
                if self._decompressor.unconsumed_tail != b'':
                    self._fp.prepend(self._decompressor.unconsumed_tail)
                elif self._decompressor.unused_data != b'':
                    self._fp.prepend(self._decompressor.unused_data)
                if uncompress != b'':
                    pass
                else:
                    if buf == b'':
                        raise EOFError('Compressed file ended before the end-of-stream marker was reached')

            self._add_read_data(uncompress)
            self._pos += len(uncompress)
            return uncompress

    def _add_read_data(self, data):
        self._crc = zlib.crc32(data, self._crc)
        self._stream_size = self._stream_size + len(data)

    def _read_eof(self):
        crc32, isize = struct.unpack('<II', self._read_exact(8))
        if crc32 != self._crc:
            raise BadGzipFile('CRC check failed %s != %s' % (hex(crc32),
             hex(self._crc)))
        elif isize != self._stream_size & 4294967295:
            raise BadGzipFile('Incorrect length of data produced')
        c = b'\x00'
        while True:
            if c == b'\x00':
                c = self._fp.read(1)

        if c:
            self._fp.prepend(c)

    def _rewind(self):
        super()._rewind()
        self._new_member = True


def compress(data, compresslevel=_COMPRESS_LEVEL_BEST, *, mtime=None):
    """Compress data in one shot and return the compressed string.
    Optional argument is the compression level, in range of 0-9.
    """
    buf = io.BytesIO()
    with GzipFile(fileobj=buf, mode='wb', compresslevel=compresslevel, mtime=mtime) as f:
        f.write(data)
    return buf.getvalue()


def decompress(data):
    """Decompress a gzip compressed string in one shot.
    Return the decompressed string.
    """
    with GzipFile(fileobj=(io.BytesIO(data))) as f:
        return f.read()


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='A simple command line interface for the gzip module: act like gzip, but do not delete the input file.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fast', action='store_true', help='compress faster')
    group.add_argument('--best', action='store_true', help='compress better')
    group.add_argument('-d', '--decompress', action='store_true', help='act like gunzip instead of gzip')
    parser.add_argument('args', nargs='*', default=['-'], metavar='file')
    args = parser.parse_args()
    compresslevel = _COMPRESS_LEVEL_TRADEOFF
    if args.fast:
        compresslevel = _COMPRESS_LEVEL_FAST
    elif args.best:
        compresslevel = _COMPRESS_LEVEL_BEST
    for arg in args.args:
        if args.decompress:
            if arg == '-':
                f = GzipFile(filename='', mode='rb', fileobj=(sys.stdin.buffer))
                g = sys.stdout.buffer
            else:
                if arg[-3:] != '.gz':
                    print("filename doesn't end in .gz:", repr(arg))
                else:
                    f = open(arg, 'rb')
                    g = builtins.open(arg[:-3], 'wb')
        else:
            if arg == '-':
                f = sys.stdin.buffer
                g = GzipFile(filename='', mode='wb', fileobj=(sys.stdout.buffer), compresslevel=compresslevel)
            else:
                f = builtins.open(arg, 'rb')
                g = open(arg + '.gz', 'wb')
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        pass
                    else:
                        g.write(chunk)

                if g is not sys.stdout.buffer:
                    g.close()
                if f is not sys.stdin.buffer:
                    f.close()


if __name__ == '__main__':
    main()