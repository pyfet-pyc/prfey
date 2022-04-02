# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: tarfile.py
"""Read from and write to tar format archives.
"""
version = '0.9.0'
__author__ = 'Lars Gustäbel (lars@gustaebel.de)'
__credits__ = 'Gustavo Niemeyer, Niels Gustäbel, Richard Townsend.'
from builtins import open as bltn_open
import sys, os, io, shutil, stat, time, struct, copy, re
try:
    import pwd
except ImportError:
    pwd = None
else:
    try:
        import grp
    except ImportError:
        grp = None
    else:
        symlink_exception = (
         AttributeError, NotImplementedError)
        try:
            symlink_exception += (OSError,)
        except NameError:
            pass
        else:
            __all__ = ['TarFile', 'TarInfo', 'is_tarfile', 'TarError', 'ReadError',
             'CompressionError', 'StreamError', 'ExtractError', 'HeaderError',
             'ENCODING', 'USTAR_FORMAT', 'GNU_FORMAT', 'PAX_FORMAT',
             'DEFAULT_FORMAT', 'open']
            NUL = b'\x00'
            BLOCKSIZE = 512
            RECORDSIZE = BLOCKSIZE * 20
            GNU_MAGIC = b'ustar  \x00'
            POSIX_MAGIC = b'ustar\x0000'
            LENGTH_NAME = 100
            LENGTH_LINK = 100
            LENGTH_PREFIX = 155
            REGTYPE = b'0'
            AREGTYPE = b'\x00'
            LNKTYPE = b'1'
            SYMTYPE = b'2'
            CHRTYPE = b'3'
            BLKTYPE = b'4'
            DIRTYPE = b'5'
            FIFOTYPE = b'6'
            CONTTYPE = b'7'
            GNUTYPE_LONGNAME = b'L'
            GNUTYPE_LONGLINK = b'K'
            GNUTYPE_SPARSE = b'S'
            XHDTYPE = b'x'
            XGLTYPE = b'g'
            SOLARIS_XHDTYPE = b'X'
            USTAR_FORMAT = 0
            GNU_FORMAT = 1
            PAX_FORMAT = 2
            DEFAULT_FORMAT = PAX_FORMAT
            SUPPORTED_TYPES = (
             REGTYPE, AREGTYPE, LNKTYPE,
             SYMTYPE, DIRTYPE, FIFOTYPE,
             CONTTYPE, CHRTYPE, BLKTYPE,
             GNUTYPE_LONGNAME, GNUTYPE_LONGLINK,
             GNUTYPE_SPARSE)
            REGULAR_TYPES = (
             REGTYPE, AREGTYPE,
             CONTTYPE, GNUTYPE_SPARSE)
            GNU_TYPES = (
             GNUTYPE_LONGNAME, GNUTYPE_LONGLINK,
             GNUTYPE_SPARSE)
            PAX_FIELDS = ('path', 'linkpath', 'size', 'mtime', 'uid', 'gid', 'uname',
                          'gname')
            PAX_NAME_FIELDS = {
             'path', 'linkpath', 'uname', 'gname'}
            PAX_NUMBER_FIELDS = {'atime':float, 
             'ctime':float, 
             'mtime':float, 
             'uid':int, 
             'gid':int, 
             'size':int}
            if os.name == 'nt':
                ENCODING = 'utf-8'
            else:
                ENCODING = sys.getfilesystemencoding()

            def stn(s, length, encoding, errors):
                """Convert a string to a null-terminated bytes object.
    """
                s = s.encode(encoding, errors)
                return s[:length] + (length - len(s)) * NUL


            def nts(s, encoding, errors):
                """Convert a null-terminated bytes object to a string.
    """
                p = s.find(b'\x00')
                if p != -1:
                    s = s[:p]
                return s.decode(encoding, errors)


            def nti(s):
                """Convert a number field to a python number.
    """
                if s[0] in (128, 255):
                    n = 0
                    for i in range(len(s) - 1):
                        n <<= 8
                        n += s[(i + 1)]
                    else:
                        if s[0] == 255:
                            n = -(256 ** (len(s) - 1) - n)

                else:
                    pass
                try:
                    s = nts(s, 'ascii', 'strict')
                    n = int(s.strip() or '0', 8)
                except ValueError:
                    raise InvalidHeaderError('invalid header')
                else:
                    return n


            def itn(n, digits=8, format=DEFAULT_FORMAT):
                """Convert a python number to a number field.
    """
                n = int(n)
                if 0 <= n < 8 ** (digits - 1):
                    s = bytes('%0*o' % (digits - 1, n), 'ascii') + NUL
                else:
                    if format == GNU_FORMAT:
                        if -256 ** (digits - 1) <= n < 256 ** (digits - 1) and n >= 0:
                            s = bytearray([128])
                        else:
                            s = bytearray([255])
                            n = 256 ** digits + n
                        for i in range(digits - 1):
                            s.insert(1, n & 255)
                            n >>= 8

                    else:
                        pass
                    raise ValueError('overflow in number field')
                return s


            def calc_chksums(buf):
                """Calculate the checksum for a member's header by summing up all
       characters except for the chksum field which is treated as if
       it was filled with spaces. According to the GNU tar sources,
       some tars (Sun and NeXT) calculate chksum with signed char,
       which will be different if there are chars in the buffer with
       the high bit set. So we calculate two checksums, unsigned and
       signed.
    """
                unsigned_chksum = 256 + sum(struct.unpack_from('148B8x356B', buf))
                signed_chksum = 256 + sum(struct.unpack_from('148b8x356b', buf))
                return (
                 unsigned_chksum, signed_chksum)


            def copyfileobj(src, dst, length=None, exception=OSError, bufsize=None):
                """Copy length bytes from fileobj src to fileobj dst.
       If length is None, copy the entire content.
    """
                bufsize = bufsize or 16384
                if length == 0:
                    return
                if length is None:
                    shutil.copyfileobj(src, dst, bufsize)
                    return
                blocks, remainder = divmod(length, bufsize)
                for b in range(blocks):
                    buf = src.read(bufsize)
                    if len(buf) < bufsize:
                        raise exception('unexpected end of data')
                    else:
                        dst.write(buf)
                else:
                    if remainder != 0:
                        buf = src.read(remainder)
                        if len(buf) < remainder:
                            raise exception('unexpected end of data')
                        dst.write(buf)


            def _safe_print(s):
                encoding = getattr(sys.stdout, 'encoding', None)
                if encoding is not None:
                    s = s.encode(encoding, 'backslashreplace').decode(encoding)
                print(s, end=' ')


            class TarError(Exception):
                __doc__ = 'Base exception.'


            class ExtractError(TarError):
                __doc__ = 'General exception for extract errors.'


            class ReadError(TarError):
                __doc__ = 'Exception for unreadable tar archives.'


            class CompressionError(TarError):
                __doc__ = 'Exception for unavailable compression methods.'


            class StreamError(TarError):
                __doc__ = 'Exception for unsupported operations on stream-like TarFiles.'


            class HeaderError(TarError):
                __doc__ = 'Base exception for header errors.'


            class EmptyHeaderError(HeaderError):
                __doc__ = 'Exception for empty headers.'


            class TruncatedHeaderError(HeaderError):
                __doc__ = 'Exception for truncated headers.'


            class EOFHeaderError(HeaderError):
                __doc__ = 'Exception for end of file headers.'


            class InvalidHeaderError(HeaderError):
                __doc__ = 'Exception for invalid headers.'


            class SubsequentHeaderError(HeaderError):
                __doc__ = 'Exception for missing and invalid extended headers.'


            class _LowLevelFile:
                __doc__ = 'Low-level file object. Supports reading and writing.\n       It is used instead of a regular file object for streaming\n       access.\n    '

                def __init__(self, name, mode):
                    mode = {'r':os.O_RDONLY, 
                     'w':os.O_WRONLY | os.O_CREAT | os.O_TRUNC}[mode]
                    if hasattr(os, 'O_BINARY'):
                        mode |= os.O_BINARY
                    self.fd = os.open(name, mode, 438)

                def close(self):
                    os.close(self.fd)

                def read(self, size):
                    return os.read(self.fd, size)

                def write(self, s):
                    os.write(self.fd, s)


            class _Stream:
                __doc__ = 'Class that serves as an adapter between TarFile and\n       a stream-like object.  The stream-like object only\n       needs to have a read() or write() method and is accessed\n       blockwise.  Use of gzip or bzip2 compression is possible.\n       A stream-like object could be for example: sys.stdin,\n       sys.stdout, a socket, a tape device etc.\n\n       _Stream is intended to be used only internally.\n    '

                def __init__(self, name, mode, comptype, fileobj, bufsize):
                    """Construct a _Stream object.
        """
                    self._extfileobj = True
                    if fileobj is None:
                        fileobj = _LowLevelFile(name, mode)
                        self._extfileobj = False
                    if comptype == '*':
                        fileobj = _StreamProxy(fileobj)
                        comptype = fileobj.getcomptype()
                    self.name = name or ''
                    self.mode = mode
                    self.comptype = comptype
                    self.fileobj = fileobj
                    self.bufsize = bufsize
                    self.buf = b''
                    self.pos = 0
                    self.closed = False
                    try:
                        if comptype == 'gz':
                            try:
                                import zlib
                            except ImportError:
                                raise CompressionError('zlib module is not available')
                            else:
                                self.zlib = zlib
                                self.crc = zlib.crc32(b'')
                            if mode == 'r':
                                self._init_read_gz()
                                self.exception = zlib.error
                            else:
                                self._init_write_gz()
                        elif comptype == 'bz2':
                            try:
                                import bz2
                            except ImportError:
                                raise CompressionError('bz2 module is not available')

                            if mode == 'r':
                                self.dbuf = b''
                                self.cmp = bz2.BZ2Decompressor()
                                self.exception = OSError
                            else:
                                self.cmp = bz2.BZ2Compressor()
                        elif comptype == 'xz':
                            try:
                                import lzma
                            except ImportError:
                                raise CompressionError('lzma module is not available')

                            if mode == 'r':
                                self.dbuf = b''
                                self.cmp = lzma.LZMADecompressor()
                                self.exception = lzma.LZMAError
                            else:
                                self.cmp = lzma.LZMACompressor()
                        elif comptype != 'tar':
                            raise CompressionError('unknown compression type %r' % comptype)
                    except:
                        if not self._extfileobj:
                            self.fileobj.close()
                        else:
                            self.closed = True
                            raise

                def __del__(self):
                    if hasattr(self, 'closed'):
                        if not self.closed:
                            self.close()

                def _init_write_gz(self):
                    """Initialize for writing with gzip compression.
        """
                    self.cmp = self.zlib.compressobj(9, self.zlib.DEFLATED, -self.zlib.MAX_WBITS, self.zlib.DEF_MEM_LEVEL, 0)
                    timestamp = struct.pack('<L', int(time.time()))
                    self._Stream__write(b'\x1f\x8b\x08\x08' + timestamp + b'\x02\xff')
                    if self.name.endswith('.gz'):
                        self.name = self.name[:-3]
                    self._Stream__write(self.name.encode('iso-8859-1', 'replace') + NUL)

                def write(self, s):
                    """Write string s to the stream.
        """
                    if self.comptype == 'gz':
                        self.crc = self.zlib.crc32(s, self.crc)
                    self.pos += len(s)
                    if self.comptype != 'tar':
                        s = self.cmp.compress(s)
                    self._Stream__write(s)

                def __write(self, s):
                    """Write string s to the stream if a whole new block
           is ready to be written.
        """
                    self.buf += s
                    while True:
                        if len(self.buf) > self.bufsize:
                            self.fileobj.write(self.buf[:self.bufsize])
                            self.buf = self.buf[self.bufsize:]

                def close(self):
                    """Close the _Stream object. No operation should be
           done on it afterwards.
        """
                    if self.closed:
                        return
                    self.closed = True
                    try:
                        if self.mode == 'w':
                            if self.comptype != 'tar':
                                self.buf += self.cmp.flush()
                        if self.mode == 'w':
                            if self.buf:
                                self.fileobj.write(self.buf)
                                self.buf = b''
                                if self.comptype == 'gz':
                                    self.fileobj.write(struct.pack('<L', self.crc))
                                    self.fileobj.write(struct.pack('<L', self.pos & 4294967295))
                    finally:
                        if not self._extfileobj:
                            self.fileobj.close()

                def _init_read_gz--- This code section failed: ---

 L. 470         0  LOAD_FAST                'self'
                2  LOAD_ATTR                zlib
                4  LOAD_METHOD              decompressobj
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                zlib
               10  LOAD_ATTR                MAX_WBITS
               12  UNARY_NEGATIVE   
               14  CALL_METHOD_1         1  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               cmp

 L. 471        20  LOAD_CONST               b''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               dbuf

 L. 474        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _Stream__read
               30  LOAD_CONST               2
               32  CALL_METHOD_1         1  ''
               34  LOAD_CONST               b'\x1f\x8b'
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 475        40  LOAD_GLOBAL              ReadError
               42  LOAD_STR                 'not a gzip file'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 476        48  LOAD_FAST                'self'
               50  LOAD_METHOD              _Stream__read
               52  LOAD_CONST               1
               54  CALL_METHOD_1         1  ''
               56  LOAD_CONST               b'\x08'
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 477        62  LOAD_GLOBAL              CompressionError
               64  LOAD_STR                 'unsupported compression method'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 479        70  LOAD_GLOBAL              ord
               72  LOAD_FAST                'self'
               74  LOAD_METHOD              _Stream__read
               76  LOAD_CONST               1
               78  CALL_METHOD_1         1  ''
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'flag'

 L. 480        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _Stream__read
               88  LOAD_CONST               6
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 482        94  LOAD_FAST                'flag'
               96  LOAD_CONST               4
               98  BINARY_AND       
              100  POP_JUMP_IF_FALSE   144  'to 144'

 L. 483       102  LOAD_GLOBAL              ord
              104  LOAD_FAST                'self'
              106  LOAD_METHOD              _Stream__read
              108  LOAD_CONST               1
              110  CALL_METHOD_1         1  ''
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_CONST               256
              116  LOAD_GLOBAL              ord
              118  LOAD_FAST                'self'
              120  LOAD_METHOD              _Stream__read
              122  LOAD_CONST               1
              124  CALL_METHOD_1         1  ''
              126  CALL_FUNCTION_1       1  ''
              128  BINARY_MULTIPLY  
              130  BINARY_ADD       
              132  STORE_FAST               'xlen'

 L. 484       134  LOAD_FAST                'self'
              136  LOAD_METHOD              read
              138  LOAD_FAST                'xlen'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           100  '100'

 L. 485       144  LOAD_FAST                'flag'
              146  LOAD_CONST               8
              148  BINARY_AND       
              150  POP_JUMP_IF_FALSE   178  'to 178'
            152_0  COME_FROM           176  '176'
            152_1  COME_FROM           172  '172'

 L. 487       152  LOAD_FAST                'self'
              154  LOAD_METHOD              _Stream__read
              156  LOAD_CONST               1
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               's'

 L. 488       162  LOAD_FAST                's'
              164  POP_JUMP_IF_FALSE   178  'to 178'
              166  LOAD_FAST                's'
              168  LOAD_GLOBAL              NUL
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE_BACK   152  'to 152'

 L. 489       174  JUMP_FORWARD        178  'to 178'
              176  JUMP_BACK           152  'to 152'
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           164  '164'
            178_2  COME_FROM           150  '150'

 L. 490       178  LOAD_FAST                'flag'
              180  LOAD_CONST               16
              182  BINARY_AND       
              184  POP_JUMP_IF_FALSE   212  'to 212'
            186_0  COME_FROM           210  '210'
            186_1  COME_FROM           206  '206'

 L. 492       186  LOAD_FAST                'self'
              188  LOAD_METHOD              _Stream__read
              190  LOAD_CONST               1
              192  CALL_METHOD_1         1  ''
              194  STORE_FAST               's'

 L. 493       196  LOAD_FAST                's'
              198  POP_JUMP_IF_FALSE   212  'to 212'
              200  LOAD_FAST                's'
              202  LOAD_GLOBAL              NUL
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE_BACK   186  'to 186'

 L. 494       208  JUMP_FORWARD        212  'to 212'
              210  JUMP_BACK           186  'to 186'
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           198  '198'
            212_2  COME_FROM           184  '184'

 L. 495       212  LOAD_FAST                'flag'
              214  LOAD_CONST               2
              216  BINARY_AND       
              218  POP_JUMP_IF_FALSE   230  'to 230'

 L. 496       220  LOAD_FAST                'self'
              222  LOAD_METHOD              _Stream__read
              224  LOAD_CONST               2
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          
            230_0  COME_FROM           218  '218'

Parse error at or near `JUMP_BACK' instruction at offset 176

                def tell(self):
                    """Return the stream's file pointer position.
        """
                    return self.pos

                def seek(self, pos=0):
                    """Set the stream's file pointer to pos. Negative seeking
           is forbidden.
        """
                    if pos - self.pos >= 0:
                        blocks, remainder = divmod(pos - self.pos, self.bufsize)
                        for i in range(blocks):
                            self.read(self.bufsize)
                        else:
                            self.read(remainder)

                    else:
                        raise StreamError('seeking backwards is not allowed')
                    return self.pos

                def read(self, size):
                    """Return the next size number of bytes from the stream."""
                    assert size is not None
                    buf = self._read(size)
                    self.pos += len(buf)
                    return buf

                def _read(self, size):
                    """Return size bytes from the stream.
        """
                    if self.comptype == 'tar':
                        return self._Stream__read(size)
                    c = len(self.dbuf)
                    t = [self.dbuf]
                    while True:
                        if c < size:
                            if self.buf:
                                buf = self.buf
                                self.buf = b''
                            else:
                                buf = self.fileobj.read(self.bufsize)
                                if not buf:
                                    pass
                                else:
                                    pass
                            try:
                                buf = self.cmp.decompress(buf)
                            except self.exception:
                                raise ReadError('invalid compressed data')
                            else:
                                t.append(buf)
                                c += len(buf)

                    t = (b'').join(t)
                    self.dbuf = t[size:]
                    return t[:size]

                def __read(self, size):
                    """Return size bytes from stream. If internal buffer is empty,
           read another block from the stream.
        """
                    c = len(self.buf)
                    t = [self.buf]
                    while True:
                        if c < size:
                            buf = self.fileobj.read(self.bufsize)
                            if not buf:
                                pass
                            else:
                                t.append(buf)
                                c += len(buf)

                    t = (b'').join(t)
                    self.buf = t[size:]
                    return t[:size]


            class _StreamProxy(object):
                __doc__ = "Small proxy class that enables transparent compression\n       detection for the Stream interface (mode 'r|*').\n    "

                def __init__(self, fileobj):
                    self.fileobj = fileobj
                    self.buf = self.fileobj.read(BLOCKSIZE)

                def read(self, size):
                    self.read = self.fileobj.read
                    return self.buf

                def getcomptype(self):
                    if self.buf.startswith(b'\x1f\x8b\x08'):
                        return 'gz'
                    if self.buf[0:3] == b'BZh':
                        if self.buf[4:10] == b'1AY&SY':
                            return 'bz2'
                    if self.buf.startswith((b']\x00\x00\x80', b'\xfd7zXZ')):
                        return 'xz'
                    return 'tar'

                def close(self):
                    self.fileobj.close()


            class _FileInFile(object):
                __doc__ = 'A thin wrapper around an existing file object that\n       provides a part of its data as an individual file\n       object.\n    '

                def __init__(self, fileobj, offset, size, blockinfo=None):
                    self.fileobj = fileobj
                    self.offset = offset
                    self.size = size
                    self.position = 0
                    self.name = getattr(fileobj, 'name', None)
                    self.closed = False
                    if blockinfo is None:
                        blockinfo = [
                         (
                          0, size)]
                    self.map_index = 0
                    self.map = []
                    lastpos = 0
                    realpos = self.offset
                    for offset, size in blockinfo:
                        if offset > lastpos:
                            self.map.append((False, lastpos, offset, None))
                        else:
                            self.map.append((True, offset, offset + size, realpos))
                            realpos += size
                            lastpos = offset + size
                    else:
                        if lastpos < self.size:
                            self.map.append((False, lastpos, self.size, None))

                def flush(self):
                    pass

                def readable(self):
                    return True

                def writable(self):
                    return False

                def seekable(self):
                    return self.fileobj.seekable()

                def tell(self):
                    """Return the current file position.
        """
                    return self.position

                def seek(self, position, whence=io.SEEK_SET):
                    """Seek to a position in the file.
        """
                    if whence == io.SEEK_SET:
                        self.position = min(max(position, 0), self.size)
                    elif whence == io.SEEK_CUR:
                        if position < 0:
                            self.position = max(self.position + position, 0)
                        else:
                            self.position = min(self.position + position, self.size)
                    elif whence == io.SEEK_END:
                        self.position = max(min(self.size + position, self.size), 0)
                    else:
                        raise ValueError('Invalid argument')
                    return self.position

                def read(self, size=None):
                    """Read data from the file.
        """
                    if size is None:
                        size = self.size - self.position
                    else:
                        size = min(size, self.size - self.position)
                    buf = b''
                    while True:
                        if size > 0:
                            while True:
                                while True:
                                    data, start, stop, offset = self.map[self.map_index]
                                    if start <= self.position < stop:
                                        pass

                                self.map_index += 1
                                if self.map_index == len(self.map):
                                    self.map_index = 0

                            length = min(size, stop - self.position)
                            if data:
                                self.fileobj.seek(offset + (self.position - start))
                                b = self.fileobj.read(length)
                                if len(b) != length:
                                    raise ReadError('unexpected end of data')
                                buf += b
                            else:
                                buf += NUL * length
                            size -= length
                            self.position += length

                    return buf

                def readinto(self, b):
                    buf = self.read(len(b))
                    b[:len(buf)] = buf
                    return len(buf)

                def close(self):
                    self.closed = True


            class ExFileObject(io.BufferedReader):

                def __init__(self, tarfile, tarinfo):
                    fileobj = _FileInFile(tarfile.fileobj, tarinfo.offset_data, tarinfo.size, tarinfo.sparse)
                    super().__init__(fileobj)


            class TarInfo(object):
                __doc__ = 'Informational class which holds the details about an\n       archive member given by a tar header block.\n       TarInfo objects are returned by TarFile.getmember(),\n       TarFile.getmembers() and TarFile.gettarinfo() and are\n       usually created internally.\n    '
                __slots__ = dict(name='Name of the archive member.',
                  mode='Permission bits.',
                  uid='User ID of the user who originally stored this member.',
                  gid='Group ID of the user who originally stored this member.',
                  size='Size in bytes.',
                  mtime='Time of last modification.',
                  chksum='Header checksum.',
                  type='File type. type is usually one of these constants: REGTYPE, AREGTYPE, LNKTYPE, SYMTYPE, DIRTYPE, FIFOTYPE, CONTTYPE, CHRTYPE, BLKTYPE, GNUTYPE_SPARSE.',
                  linkname='Name of the target file name, which is only present in TarInfo objects of type LNKTYPE and SYMTYPE.',
                  uname='User name.',
                  gname='Group name.',
                  devmajor='Device major number.',
                  devminor='Device minor number.',
                  offset='The tar header starts here.',
                  offset_data="The file's data starts here.",
                  pax_headers='A dictionary containing key-value pairs of an associated pax extended header.',
                  sparse='Sparse member information.',
                  tarfile=None,
                  _sparse_structs=None,
                  _link_target=None)

                def __init__(self, name=''):
                    """Construct a TarInfo object. name is the optional name
           of the member.
        """
                    self.name = name
                    self.mode = 420
                    self.uid = 0
                    self.gid = 0
                    self.size = 0
                    self.mtime = 0
                    self.chksum = 0
                    self.type = REGTYPE
                    self.linkname = ''
                    self.uname = ''
                    self.gname = ''
                    self.devmajor = 0
                    self.devminor = 0
                    self.offset = 0
                    self.offset_data = 0
                    self.sparse = None
                    self.pax_headers = {}

                @property
                def path(self):
                    """In pax headers, "name" is called "path"."""
                    return self.name

                @path.setter
                def path(self, name):
                    self.name = name

                @property
                def linkpath(self):
                    """In pax headers, "linkname" is called "linkpath"."""
                    return self.linkname

                @linkpath.setter
                def linkpath(self, linkname):
                    self.linkname = linkname

                def __repr__(self):
                    return '<%s %r at %#x>' % (self.__class__.__name__, self.name, id(self))

                def get_info(self):
                    """Return the TarInfo's attributes as a dictionary.
        """
                    info = {'name':self.name, 
                     'mode':self.mode & 4095, 
                     'uid':self.uid, 
                     'gid':self.gid, 
                     'size':self.size, 
                     'mtime':self.mtime, 
                     'chksum':self.chksum, 
                     'type':self.type, 
                     'linkname':self.linkname, 
                     'uname':self.uname, 
                     'gname':self.gname, 
                     'devmajor':self.devmajor, 
                     'devminor':self.devminor}
                    if info['type'] == DIRTYPE:
                        if not info['name'].endswith('/'):
                            info['name'] += '/'
                        return info

                def tobuf(self, format=DEFAULT_FORMAT, encoding=ENCODING, errors='surrogateescape'):
                    """Return a tar header as a string of 512 byte blocks.
        """
                    info = self.get_info()
                    if format == USTAR_FORMAT:
                        return self.create_ustar_header(info, encoding, errors)
                    if format == GNU_FORMAT:
                        return self.create_gnu_header(info, encoding, errors)
                    if format == PAX_FORMAT:
                        return self.create_pax_header(info, encoding)
                    raise ValueError('invalid format')

                def create_ustar_header(self, info, encoding, errors):
                    """Return the object as a ustar header block.
        """
                    info['magic'] = POSIX_MAGIC
                    if len(info['linkname'].encode(encoding, errors)) > LENGTH_LINK:
                        raise ValueError('linkname is too long')
                    if len(info['name'].encode(encoding, errors)) > LENGTH_NAME:
                        info['prefix'], info['name'] = self._posix_split_name(info['name'], encoding, errors)
                    return self._create_header(info, USTAR_FORMAT, encoding, errors)

                def create_gnu_header(self, info, encoding, errors):
                    """Return the object as a GNU header block sequence.
        """
                    info['magic'] = GNU_MAGIC
                    buf = b''
                    if len(info['linkname'].encode(encoding, errors)) > LENGTH_LINK:
                        buf += self._create_gnu_long_header(info['linkname'], GNUTYPE_LONGLINK, encoding, errors)
                    if len(info['name'].encode(encoding, errors)) > LENGTH_NAME:
                        buf += self._create_gnu_long_header(info['name'], GNUTYPE_LONGNAME, encoding, errors)
                    return buf + self._create_header(info, GNU_FORMAT, encoding, errors)

                def create_pax_header--- This code section failed: ---

 L. 862         0  LOAD_GLOBAL              POSIX_MAGIC
                2  LOAD_FAST                'info'
                4  LOAD_STR                 'magic'
                6  STORE_SUBSCR     

 L. 863         8  LOAD_FAST                'self'
               10  LOAD_ATTR                pax_headers
               12  LOAD_METHOD              copy
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'pax_headers'

 L. 868        18  LOAD_STR                 'name'
               20  LOAD_STR                 'path'
               22  LOAD_GLOBAL              LENGTH_NAME
               24  BUILD_TUPLE_3         3 

 L. 868        26  LOAD_STR                 'linkname'
               28  LOAD_STR                 'linkpath'
               30  LOAD_GLOBAL              LENGTH_LINK
               32  BUILD_TUPLE_3         3 

 L. 869        34  LOAD_CONST               ('uname', 'uname', 32)

 L. 869        36  LOAD_CONST               ('gname', 'gname', 32)

 L. 867        38  BUILD_TUPLE_4         4 
               40  GET_ITER         
             42_0  COME_FROM           148  '148'
             42_1  COME_FROM           134  '134'
             42_2  COME_FROM           112  '112'
             42_3  COME_FROM            60  '60'
               42  FOR_ITER            150  'to 150'
               44  UNPACK_SEQUENCE_3     3 
               46  STORE_FAST               'name'
               48  STORE_FAST               'hname'
               50  STORE_FAST               'length'

 L. 871        52  LOAD_FAST                'hname'
               54  LOAD_FAST                'pax_headers'
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE    62  'to 62'

 L. 873        60  JUMP_BACK            42  'to 42'
             62_0  COME_FROM            58  '58'

 L. 876        62  SETUP_FINALLY        84  'to 84'

 L. 877        64  LOAD_FAST                'info'
               66  LOAD_FAST                'name'
               68  BINARY_SUBSCR    
               70  LOAD_METHOD              encode
               72  LOAD_STR                 'ascii'
               74  LOAD_STR                 'strict'
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  JUMP_FORWARD        120  'to 120'
             84_0  COME_FROM_FINALLY    62  '62'

 L. 878        84  DUP_TOP          
               86  LOAD_GLOBAL              UnicodeEncodeError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   118  'to 118'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 879        98  LOAD_FAST                'info'
              100  LOAD_FAST                'name'
              102  BINARY_SUBSCR    
              104  LOAD_FAST                'pax_headers'
              106  LOAD_FAST                'hname'
              108  STORE_SUBSCR     

 L. 880       110  POP_EXCEPT       
              112  JUMP_BACK            42  'to 42'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            90  '90'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            82  '82'

 L. 882       120  LOAD_GLOBAL              len
              122  LOAD_FAST                'info'
              124  LOAD_FAST                'name'
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_FAST                'length'
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE_BACK    42  'to 42'

 L. 883       136  LOAD_FAST                'info'
              138  LOAD_FAST                'name'
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'pax_headers'
              144  LOAD_FAST                'hname'
              146  STORE_SUBSCR     
              148  JUMP_BACK            42  'to 42'
            150_0  COME_FROM            42  '42'

 L. 887       150  LOAD_CONST               (('uid', 8), ('gid', 8), ('size', 12), ('mtime', 12))
              152  GET_ITER         
            154_0  COME_FROM           250  '250'
            154_1  COME_FROM           228  '228'
            154_2  COME_FROM           178  '178'
              154  FOR_ITER            252  'to 252'
              156  UNPACK_SEQUENCE_2     2 
              158  STORE_FAST               'name'
              160  STORE_FAST               'digits'

 L. 888       162  LOAD_FAST                'name'
              164  LOAD_FAST                'pax_headers'
              166  COMPARE_OP               in
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L. 890       170  LOAD_CONST               0
              172  LOAD_FAST                'info'
              174  LOAD_FAST                'name'
              176  STORE_SUBSCR     

 L. 891       178  JUMP_BACK           154  'to 154'
            180_0  COME_FROM           168  '168'

 L. 893       180  LOAD_FAST                'info'
              182  LOAD_FAST                'name'
              184  BINARY_SUBSCR    
              186  STORE_FAST               'val'

 L. 894       188  LOAD_CONST               0
              190  LOAD_FAST                'val'
              192  DUP_TOP          
              194  ROT_THREE        
              196  COMPARE_OP               <=
              198  POP_JUMP_IF_FALSE   216  'to 216'
              200  LOAD_CONST               8
              202  LOAD_FAST                'digits'
              204  LOAD_CONST               1
              206  BINARY_SUBTRACT  
              208  BINARY_POWER     
              210  COMPARE_OP               <
              212  POP_JUMP_IF_FALSE   230  'to 230'
              214  JUMP_FORWARD        220  'to 220'
            216_0  COME_FROM           198  '198'
              216  POP_TOP          
              218  JUMP_FORWARD        230  'to 230'
            220_0  COME_FROM           214  '214'
              220  LOAD_GLOBAL              isinstance
              222  LOAD_FAST                'val'
              224  LOAD_GLOBAL              float
              226  CALL_FUNCTION_2       2  ''
              228  POP_JUMP_IF_FALSE_BACK   154  'to 154'
            230_0  COME_FROM           218  '218'
            230_1  COME_FROM           212  '212'

 L. 895       230  LOAD_GLOBAL              str
              232  LOAD_FAST                'val'
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_FAST                'pax_headers'
              238  LOAD_FAST                'name'
              240  STORE_SUBSCR     

 L. 896       242  LOAD_CONST               0
              244  LOAD_FAST                'info'
              246  LOAD_FAST                'name'
              248  STORE_SUBSCR     
              250  JUMP_BACK           154  'to 154'
            252_0  COME_FROM           154  '154'

 L. 899       252  LOAD_FAST                'pax_headers'
          254_256  POP_JUMP_IF_FALSE   274  'to 274'

 L. 900       258  LOAD_FAST                'self'
              260  LOAD_METHOD              _create_pax_generic_header
              262  LOAD_FAST                'pax_headers'
              264  LOAD_GLOBAL              XHDTYPE
              266  LOAD_FAST                'encoding'
              268  CALL_METHOD_3         3  ''
              270  STORE_FAST               'buf'
              272  JUMP_FORWARD        278  'to 278'
            274_0  COME_FROM           254  '254'

 L. 902       274  LOAD_CONST               b''
              276  STORE_FAST               'buf'
            278_0  COME_FROM           272  '272'

 L. 904       278  LOAD_FAST                'buf'
              280  LOAD_FAST                'self'
              282  LOAD_METHOD              _create_header
              284  LOAD_FAST                'info'
              286  LOAD_GLOBAL              USTAR_FORMAT
              288  LOAD_STR                 'ascii'
              290  LOAD_STR                 'replace'
              292  CALL_METHOD_4         4  ''
              294  BINARY_ADD       
              296  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 118_0

                @classmethod
                def create_pax_global_header(cls, pax_headers):
                    """Return the object as a pax global header block sequence.
        """
                    return cls._create_pax_generic_header(pax_headers, XGLTYPE, 'utf-8')

                def _posix_split_name--- This code section failed: ---

 L. 916         0  LOAD_FAST                'name'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'components'

 L. 917        10  LOAD_GLOBAL              range
               12  LOAD_CONST               1
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'components'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_2       2  ''
               22  GET_ITER         
             24_0  COME_FROM           108  '108'
             24_1  COME_FROM           102  '102'
             24_2  COME_FROM            82  '82'
               24  FOR_ITER            110  'to 110'
               26  STORE_FAST               'i'

 L. 918        28  LOAD_STR                 '/'
               30  LOAD_METHOD              join
               32  LOAD_FAST                'components'
               34  LOAD_CONST               None
               36  LOAD_FAST                'i'
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'prefix'

 L. 919        46  LOAD_STR                 '/'
               48  LOAD_METHOD              join
               50  LOAD_FAST                'components'
               52  LOAD_FAST                'i'
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'name'

 L. 920        64  LOAD_GLOBAL              len
               66  LOAD_FAST                'prefix'
               68  LOAD_METHOD              encode
               70  LOAD_FAST                'encoding'
               72  LOAD_FAST                'errors'
               74  CALL_METHOD_2         2  ''
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              LENGTH_PREFIX
               80  COMPARE_OP               <=
               82  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 921        84  LOAD_GLOBAL              len
               86  LOAD_FAST                'name'
               88  LOAD_METHOD              encode
               90  LOAD_FAST                'encoding'
               92  LOAD_FAST                'errors'
               94  CALL_METHOD_2         2  ''
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_GLOBAL              LENGTH_NAME
              100  COMPARE_OP               <=

 L. 920       102  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 922       104  POP_TOP          
              106  BREAK_LOOP          118  'to 118'
              108  JUMP_BACK            24  'to 24'
            110_0  COME_FROM            24  '24'

 L. 924       110  LOAD_GLOBAL              ValueError
              112  LOAD_STR                 'name is too long'
              114  CALL_FUNCTION_1       1  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           106  '106'

 L. 926       118  LOAD_FAST                'prefix'
              120  LOAD_FAST                'name'
              122  BUILD_TUPLE_2         2 
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 124

                @staticmethod
                def _create_header(info, format, encoding, errors):
                    """Return a header block. info is a dictionary with file
           information, format must be one of the *_FORMAT constants.
        """
                    parts = [
                     stn(info.get('name', ''), 100, encoding, errors),
                     itn(info.get('mode', 0) & 4095, 8, format),
                     itn(info.get('uid', 0), 8, format),
                     itn(info.get('gid', 0), 8, format),
                     itn(info.get('size', 0), 12, format),
                     itn(info.get('mtime', 0), 12, format),
                     b'        ',
                     info.get('type', REGTYPE),
                     stn(info.get('linkname', ''), 100, encoding, errors),
                     info.get('magic', POSIX_MAGIC),
                     stn(info.get('uname', ''), 32, encoding, errors),
                     stn(info.get('gname', ''), 32, encoding, errors),
                     itn(info.get('devmajor', 0), 8, format),
                     itn(info.get('devminor', 0), 8, format),
                     stn(info.get('prefix', ''), 155, encoding, errors)]
                    buf = struct.pack('%ds' % BLOCKSIZE, (b'').join(parts))
                    chksum = calc_chksums(buf[-BLOCKSIZE:])[0]
                    buf = buf[:-364] + bytes('%06o\x00' % chksum, 'ascii') + buf[-357:]
                    return buf

                @staticmethod
                def _create_payload(payload):
                    """Return the string payload filled with zero bytes
           up to the next 512 byte border.
        """
                    blocks, remainder = divmod(len(payload), BLOCKSIZE)
                    if remainder > 0:
                        payload += (BLOCKSIZE - remainder) * NUL
                    return payload

                @classmethod
                def _create_gnu_long_header(cls, name, type, encoding, errors):
                    """Return a GNUTYPE_LONGNAME or GNUTYPE_LONGLINK sequence
           for name.
        """
                    name = name.encode(encoding, errors) + NUL
                    info = {}
                    info['name'] = '././@LongLink'
                    info['type'] = type
                    info['size'] = len(name)
                    info['magic'] = GNU_MAGIC
                    return cls._create_header(info, USTAR_FORMAT, encoding, errors) + cls._create_payload(name)

                @classmethod
                def _create_pax_generic_header--- This code section failed: ---

 L. 991         0  LOAD_CONST               False
                2  STORE_FAST               'binary'

 L. 992         4  LOAD_FAST                'pax_headers'
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM            68  '68'
             12_1  COME_FROM            64  '64'
             12_2  COME_FROM            36  '36'
               12  FOR_ITER             70  'to 70'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'keyword'
               18  STORE_FAST               'value'

 L. 993        20  SETUP_FINALLY        38  'to 38'

 L. 994        22  LOAD_FAST                'value'
               24  LOAD_METHOD              encode
               26  LOAD_STR                 'utf-8'
               28  LOAD_STR                 'strict'
               30  CALL_METHOD_2         2  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_BACK            12  'to 12'
             38_0  COME_FROM_FINALLY    20  '20'

 L. 995        38  DUP_TOP          
               40  LOAD_GLOBAL              UnicodeEncodeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    66  'to 66'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 996        52  LOAD_CONST               True
               54  STORE_FAST               'binary'

 L. 997        56  POP_EXCEPT       
               58  POP_TOP          
               60  JUMP_FORWARD         70  'to 70'
               62  POP_EXCEPT       
               64  JUMP_BACK            12  'to 12'
             66_0  COME_FROM            44  '44'
               66  END_FINALLY      
               68  JUMP_BACK            12  'to 12'
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            12  '12'

 L. 999        70  LOAD_CONST               b''
               72  STORE_FAST               'records'

 L.1000        74  LOAD_FAST                'binary'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.1002        78  LOAD_FAST                'records'
               80  LOAD_CONST               b'21 hdrcharset=BINARY\n'
               82  INPLACE_ADD      
               84  STORE_FAST               'records'
             86_0  COME_FROM            76  '76'

 L.1004        86  LOAD_FAST                'pax_headers'
               88  LOAD_METHOD              items
               90  CALL_METHOD_0         0  ''
               92  GET_ITER         
             94_0  COME_FROM           238  '238'
               94  FOR_ITER            240  'to 240'
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'keyword'
              100  STORE_FAST               'value'

 L.1005       102  LOAD_FAST                'keyword'
              104  LOAD_METHOD              encode
              106  LOAD_STR                 'utf-8'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'keyword'

 L.1006       112  LOAD_FAST                'binary'
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.1009       116  LOAD_FAST                'value'
              118  LOAD_METHOD              encode
              120  LOAD_FAST                'encoding'
              122  LOAD_STR                 'surrogateescape'
              124  CALL_METHOD_2         2  ''
              126  STORE_FAST               'value'
              128  JUMP_FORWARD        140  'to 140'
            130_0  COME_FROM           114  '114'

 L.1011       130  LOAD_FAST                'value'
              132  LOAD_METHOD              encode
              134  LOAD_STR                 'utf-8'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'value'
            140_0  COME_FROM           128  '128'

 L.1013       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'keyword'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_GLOBAL              len
              148  LOAD_FAST                'value'
              150  CALL_FUNCTION_1       1  ''
              152  BINARY_ADD       
              154  LOAD_CONST               3
              156  BINARY_ADD       
              158  STORE_FAST               'l'

 L.1014       160  LOAD_CONST               0
              162  DUP_TOP          
              164  STORE_FAST               'n'
              166  STORE_FAST               'p'
            168_0  COME_FROM           198  '198'

 L.1016       168  LOAD_FAST                'l'
              170  LOAD_GLOBAL              len
              172  LOAD_GLOBAL              str
              174  LOAD_FAST                'p'
              176  CALL_FUNCTION_1       1  ''
              178  CALL_FUNCTION_1       1  ''
              180  BINARY_ADD       
              182  STORE_FAST               'n'

 L.1017       184  LOAD_FAST                'n'
              186  LOAD_FAST                'p'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   194  'to 194'

 L.1018       192  JUMP_FORWARD        200  'to 200'
            194_0  COME_FROM           190  '190'

 L.1019       194  LOAD_FAST                'n'
              196  STORE_FAST               'p'
              198  JUMP_BACK           168  'to 168'
            200_0  COME_FROM           192  '192'

 L.1020       200  LOAD_FAST                'records'
              202  LOAD_GLOBAL              bytes
              204  LOAD_GLOBAL              str
              206  LOAD_FAST                'p'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_STR                 'ascii'
              212  CALL_FUNCTION_2       2  ''
              214  LOAD_CONST               b' '
              216  BINARY_ADD       
              218  LOAD_FAST                'keyword'
              220  BINARY_ADD       
              222  LOAD_CONST               b'='
              224  BINARY_ADD       
              226  LOAD_FAST                'value'
              228  BINARY_ADD       
              230  LOAD_CONST               b'\n'
              232  BINARY_ADD       
              234  INPLACE_ADD      
              236  STORE_FAST               'records'
              238  JUMP_BACK            94  'to 94'
            240_0  COME_FROM            94  '94'

 L.1024       240  BUILD_MAP_0           0 
              242  STORE_FAST               'info'

 L.1025       244  LOAD_STR                 '././@PaxHeader'
              246  LOAD_FAST                'info'
              248  LOAD_STR                 'name'
              250  STORE_SUBSCR     

 L.1026       252  LOAD_FAST                'type'
              254  LOAD_FAST                'info'
              256  LOAD_STR                 'type'
              258  STORE_SUBSCR     

 L.1027       260  LOAD_GLOBAL              len
              262  LOAD_FAST                'records'
              264  CALL_FUNCTION_1       1  ''
              266  LOAD_FAST                'info'
              268  LOAD_STR                 'size'
              270  STORE_SUBSCR     

 L.1028       272  LOAD_GLOBAL              POSIX_MAGIC
              274  LOAD_FAST                'info'
              276  LOAD_STR                 'magic'
              278  STORE_SUBSCR     

 L.1031       280  LOAD_FAST                'cls'
              282  LOAD_METHOD              _create_header
              284  LOAD_FAST                'info'
              286  LOAD_GLOBAL              USTAR_FORMAT
              288  LOAD_STR                 'ascii'
              290  LOAD_STR                 'replace'
              292  CALL_METHOD_4         4  ''

 L.1032       294  LOAD_FAST                'cls'
              296  LOAD_METHOD              _create_payload
              298  LOAD_FAST                'records'
              300  CALL_METHOD_1         1  ''

 L.1031       302  BINARY_ADD       
              304  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 58

                @classmethod
                def frombuf--- This code section failed: ---

 L.1038         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'buf'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.1039        12  LOAD_GLOBAL              EmptyHeaderError
               14  LOAD_STR                 'empty header'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.1040        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'buf'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_GLOBAL              BLOCKSIZE
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.1041        32  LOAD_GLOBAL              TruncatedHeaderError
               34  LOAD_STR                 'truncated header'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L.1042        40  LOAD_FAST                'buf'
               42  LOAD_METHOD              count
               44  LOAD_GLOBAL              NUL
               46  CALL_METHOD_1         1  ''
               48  LOAD_GLOBAL              BLOCKSIZE
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L.1043        54  LOAD_GLOBAL              EOFHeaderError
               56  LOAD_STR                 'end of file header'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'

 L.1045        62  LOAD_GLOBAL              nti
               64  LOAD_FAST                'buf'
               66  LOAD_CONST               148
               68  LOAD_CONST               156
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'chksum'

 L.1046        78  LOAD_FAST                'chksum'
               80  LOAD_GLOBAL              calc_chksums
               82  LOAD_FAST                'buf'
               84  CALL_FUNCTION_1       1  ''
               86  COMPARE_OP               not-in
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L.1047        90  LOAD_GLOBAL              InvalidHeaderError
               92  LOAD_STR                 'bad checksum'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            88  '88'

 L.1049        98  LOAD_FAST                'cls'
              100  CALL_FUNCTION_0       0  ''
              102  STORE_FAST               'obj'

 L.1050       104  LOAD_GLOBAL              nts
              106  LOAD_FAST                'buf'
              108  LOAD_CONST               0
              110  LOAD_CONST               100
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'encoding'
              118  LOAD_FAST                'errors'
              120  CALL_FUNCTION_3       3  ''
              122  LOAD_FAST                'obj'
              124  STORE_ATTR               name

 L.1051       126  LOAD_GLOBAL              nti
              128  LOAD_FAST                'buf'
              130  LOAD_CONST               100
              132  LOAD_CONST               108
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_FAST                'obj'
              142  STORE_ATTR               mode

 L.1052       144  LOAD_GLOBAL              nti
              146  LOAD_FAST                'buf'
              148  LOAD_CONST               108
              150  LOAD_CONST               116
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_FAST                'obj'
              160  STORE_ATTR               uid

 L.1053       162  LOAD_GLOBAL              nti
              164  LOAD_FAST                'buf'
              166  LOAD_CONST               116
              168  LOAD_CONST               124
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_FAST                'obj'
              178  STORE_ATTR               gid

 L.1054       180  LOAD_GLOBAL              nti
              182  LOAD_FAST                'buf'
              184  LOAD_CONST               124
              186  LOAD_CONST               136
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  CALL_FUNCTION_1       1  ''
              194  LOAD_FAST                'obj'
              196  STORE_ATTR               size

 L.1055       198  LOAD_GLOBAL              nti
              200  LOAD_FAST                'buf'
              202  LOAD_CONST               136
              204  LOAD_CONST               148
              206  BUILD_SLICE_2         2 
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_FAST                'obj'
              214  STORE_ATTR               mtime

 L.1056       216  LOAD_FAST                'chksum'
              218  LOAD_FAST                'obj'
              220  STORE_ATTR               chksum

 L.1057       222  LOAD_FAST                'buf'
              224  LOAD_CONST               156
              226  LOAD_CONST               157
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'obj'
              234  STORE_ATTR               type

 L.1058       236  LOAD_GLOBAL              nts
              238  LOAD_FAST                'buf'
              240  LOAD_CONST               157
              242  LOAD_CONST               257
              244  BUILD_SLICE_2         2 
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'encoding'
              250  LOAD_FAST                'errors'
              252  CALL_FUNCTION_3       3  ''
              254  LOAD_FAST                'obj'
              256  STORE_ATTR               linkname

 L.1059       258  LOAD_GLOBAL              nts
              260  LOAD_FAST                'buf'
              262  LOAD_CONST               265
              264  LOAD_CONST               297
              266  BUILD_SLICE_2         2 
              268  BINARY_SUBSCR    
              270  LOAD_FAST                'encoding'
              272  LOAD_FAST                'errors'
              274  CALL_FUNCTION_3       3  ''
              276  LOAD_FAST                'obj'
              278  STORE_ATTR               uname

 L.1060       280  LOAD_GLOBAL              nts
              282  LOAD_FAST                'buf'
              284  LOAD_CONST               297
              286  LOAD_CONST               329
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    
              292  LOAD_FAST                'encoding'
              294  LOAD_FAST                'errors'
              296  CALL_FUNCTION_3       3  ''
              298  LOAD_FAST                'obj'
              300  STORE_ATTR               gname

 L.1061       302  LOAD_GLOBAL              nti
              304  LOAD_FAST                'buf'
              306  LOAD_CONST               329
              308  LOAD_CONST               337
              310  BUILD_SLICE_2         2 
              312  BINARY_SUBSCR    
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_FAST                'obj'
              318  STORE_ATTR               devmajor

 L.1062       320  LOAD_GLOBAL              nti
              322  LOAD_FAST                'buf'
              324  LOAD_CONST               337
              326  LOAD_CONST               345
              328  BUILD_SLICE_2         2 
              330  BINARY_SUBSCR    
              332  CALL_FUNCTION_1       1  ''
              334  LOAD_FAST                'obj'
              336  STORE_ATTR               devminor

 L.1063       338  LOAD_GLOBAL              nts
              340  LOAD_FAST                'buf'
              342  LOAD_CONST               345
              344  LOAD_CONST               500
              346  BUILD_SLICE_2         2 
              348  BINARY_SUBSCR    
              350  LOAD_FAST                'encoding'
              352  LOAD_FAST                'errors'
              354  CALL_FUNCTION_3       3  ''
              356  STORE_FAST               'prefix'

 L.1067       358  LOAD_FAST                'obj'
              360  LOAD_ATTR                type
              362  LOAD_GLOBAL              AREGTYPE
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   390  'to 390'
              370  LOAD_FAST                'obj'
              372  LOAD_ATTR                name
              374  LOAD_METHOD              endswith
              376  LOAD_STR                 '/'
              378  CALL_METHOD_1         1  ''
          380_382  POP_JUMP_IF_FALSE   390  'to 390'

 L.1068       384  LOAD_GLOBAL              DIRTYPE
              386  LOAD_FAST                'obj'
              388  STORE_ATTR               type
            390_0  COME_FROM           380  '380'
            390_1  COME_FROM           366  '366'

 L.1073       390  LOAD_FAST                'obj'
              392  LOAD_ATTR                type
              394  LOAD_GLOBAL              GNUTYPE_SPARSE
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   568  'to 568'

 L.1074       402  LOAD_CONST               386
              404  STORE_FAST               'pos'

 L.1075       406  BUILD_LIST_0          0 
              408  STORE_FAST               'structs'

 L.1076       410  LOAD_GLOBAL              range
              412  LOAD_CONST               4
              414  CALL_FUNCTION_1       1  ''
              416  GET_ITER         
            418_0  COME_FROM           524  '524'
              418  FOR_ITER            528  'to 528'
              420  STORE_FAST               'i'

 L.1077       422  SETUP_FINALLY       472  'to 472'

 L.1078       424  LOAD_GLOBAL              nti
              426  LOAD_FAST                'buf'
              428  LOAD_FAST                'pos'
              430  LOAD_FAST                'pos'
              432  LOAD_CONST               12
              434  BINARY_ADD       
              436  BUILD_SLICE_2         2 
              438  BINARY_SUBSCR    
              440  CALL_FUNCTION_1       1  ''
              442  STORE_FAST               'offset'

 L.1079       444  LOAD_GLOBAL              nti
              446  LOAD_FAST                'buf'
              448  LOAD_FAST                'pos'
              450  LOAD_CONST               12
              452  BINARY_ADD       
              454  LOAD_FAST                'pos'
              456  LOAD_CONST               24
              458  BINARY_ADD       
              460  BUILD_SLICE_2         2 
              462  BINARY_SUBSCR    
              464  CALL_FUNCTION_1       1  ''
              466  STORE_FAST               'numbytes'
              468  POP_BLOCK        
              470  JUMP_FORWARD        502  'to 502'
            472_0  COME_FROM_FINALLY   422  '422'

 L.1080       472  DUP_TOP          
              474  LOAD_GLOBAL              ValueError
              476  COMPARE_OP               exception-match
          478_480  POP_JUMP_IF_FALSE   500  'to 500'
              482  POP_TOP          
              484  POP_TOP          
              486  POP_TOP          

 L.1081       488  POP_EXCEPT       
              490  POP_TOP          
          492_494  JUMP_FORWARD        528  'to 528'
              496  POP_EXCEPT       
              498  JUMP_FORWARD        502  'to 502'
            500_0  COME_FROM           478  '478'
              500  END_FINALLY      
            502_0  COME_FROM           498  '498'
            502_1  COME_FROM           470  '470'

 L.1082       502  LOAD_FAST                'structs'
              504  LOAD_METHOD              append
              506  LOAD_FAST                'offset'
              508  LOAD_FAST                'numbytes'
              510  BUILD_TUPLE_2         2 
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          

 L.1083       516  LOAD_FAST                'pos'
              518  LOAD_CONST               24
              520  INPLACE_ADD      
              522  STORE_FAST               'pos'
          524_526  JUMP_BACK           418  'to 418'
            528_0  COME_FROM           492  '492'
            528_1  COME_FROM           418  '418'

 L.1084       528  LOAD_GLOBAL              bool
              530  LOAD_FAST                'buf'
              532  LOAD_CONST               482
              534  BINARY_SUBSCR    
              536  CALL_FUNCTION_1       1  ''
              538  STORE_FAST               'isextended'

 L.1085       540  LOAD_GLOBAL              nti
              542  LOAD_FAST                'buf'
              544  LOAD_CONST               483
              546  LOAD_CONST               495
              548  BUILD_SLICE_2         2 
              550  BINARY_SUBSCR    
              552  CALL_FUNCTION_1       1  ''
              554  STORE_FAST               'origsize'

 L.1086       556  LOAD_FAST                'structs'
              558  LOAD_FAST                'isextended'
              560  LOAD_FAST                'origsize'
              562  BUILD_TUPLE_3         3 
              564  LOAD_FAST                'obj'
              566  STORE_ATTR               _sparse_structs
            568_0  COME_FROM           398  '398'

 L.1089       568  LOAD_FAST                'obj'
              570  LOAD_METHOD              isdir
              572  CALL_METHOD_0         0  ''
          574_576  POP_JUMP_IF_FALSE   592  'to 592'

 L.1090       578  LOAD_FAST                'obj'
              580  LOAD_ATTR                name
              582  LOAD_METHOD              rstrip
              584  LOAD_STR                 '/'
              586  CALL_METHOD_1         1  ''
              588  LOAD_FAST                'obj'
              590  STORE_ATTR               name
            592_0  COME_FROM           574  '574'

 L.1093       592  LOAD_FAST                'prefix'
          594_596  POP_JUMP_IF_FALSE   626  'to 626'
              598  LOAD_FAST                'obj'
              600  LOAD_ATTR                type
              602  LOAD_GLOBAL              GNU_TYPES
              604  COMPARE_OP               not-in
          606_608  POP_JUMP_IF_FALSE   626  'to 626'

 L.1094       610  LOAD_FAST                'prefix'
              612  LOAD_STR                 '/'
              614  BINARY_ADD       
              616  LOAD_FAST                'obj'
              618  LOAD_ATTR                name
              620  BINARY_ADD       
              622  LOAD_FAST                'obj'
              624  STORE_ATTR               name
            626_0  COME_FROM           606  '606'
            626_1  COME_FROM           594  '594'

 L.1095       626  LOAD_FAST                'obj'
              628  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 492_494

                @classmethod
                def fromtarfile(cls, tarfile):
                    """Return the next TarInfo object from TarFile object
           tarfile.
        """
                    buf = tarfile.fileobj.read(BLOCKSIZE)
                    obj = cls.frombuf(buf, tarfile.encoding, tarfile.errors)
                    obj.offset = tarfile.fileobj.tell() - BLOCKSIZE
                    return obj._proc_member(tarfile)

                def _proc_member(self, tarfile):
                    """Choose the right processing method depending on
           the type and call it.
        """
                    if self.type in (GNUTYPE_LONGNAME, GNUTYPE_LONGLINK):
                        return self._proc_gnulong(tarfile)
                    if self.type == GNUTYPE_SPARSE:
                        return self._proc_sparse(tarfile)
                    if self.type in (XHDTYPE, XGLTYPE, SOLARIS_XHDTYPE):
                        return self._proc_pax(tarfile)
                    return self._proc_builtin(tarfile)

                def _proc_builtin(self, tarfile):
                    """Process a builtin type or an unknown type which
           will be treated as a regular file.
        """
                    self.offset_data = tarfile.fileobj.tell()
                    offset = self.offset_data
                    if self.isreg() or (self.type not in SUPPORTED_TYPES):
                        offset += self._block(self.size)
                    tarfile.offset = offset
                    self._apply_pax_info(tarfile.pax_headers, tarfile.encoding, tarfile.errors)
                    return self

                def _proc_gnulong(self, tarfile):
                    """Process the blocks that hold a GNU longname
           or longlink member.
        """
                    buf = tarfile.fileobj.read(self._block(self.size))
                    try:
                        next = self.fromtarfile(tarfile)
                    except HeaderError:
                        raise SubsequentHeaderError('missing or bad subsequent header')
                    else:
                        next.offset = self.offset
                        if self.type == GNUTYPE_LONGNAME:
                            next.name = nts(buf, tarfile.encoding, tarfile.errors)
                        elif self.type == GNUTYPE_LONGLINK:
                            next.linkname = nts(buf, tarfile.encoding, tarfile.errors)
                        return next

                def _proc_sparse--- This code section failed: ---

 L.1174         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _sparse_structs
                4  UNPACK_SEQUENCE_3     3 
                6  STORE_FAST               'structs'
                8  STORE_FAST               'isextended'
               10  STORE_FAST               'origsize'

 L.1175        12  LOAD_FAST                'self'
               14  DELETE_ATTR              _sparse_structs
             16_0  COME_FROM           168  '168'

 L.1178        16  LOAD_FAST                'isextended'
               18  POP_JUMP_IF_FALSE   170  'to 170'

 L.1179        20  LOAD_FAST                'tarfile'
               22  LOAD_ATTR                fileobj
               24  LOAD_METHOD              read
               26  LOAD_GLOBAL              BLOCKSIZE
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'buf'

 L.1180        32  LOAD_CONST               0
               34  STORE_FAST               'pos'

 L.1181        36  LOAD_GLOBAL              range
               38  LOAD_CONST               21
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
             44_0  COME_FROM           154  '154'
               44  FOR_ITER            156  'to 156'
               46  STORE_FAST               'i'

 L.1182        48  SETUP_FINALLY        98  'to 98'

 L.1183        50  LOAD_GLOBAL              nti
               52  LOAD_FAST                'buf'
               54  LOAD_FAST                'pos'
               56  LOAD_FAST                'pos'
               58  LOAD_CONST               12
               60  BINARY_ADD       
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'offset'

 L.1184        70  LOAD_GLOBAL              nti
               72  LOAD_FAST                'buf'
               74  LOAD_FAST                'pos'
               76  LOAD_CONST               12
               78  BINARY_ADD       
               80  LOAD_FAST                'pos'
               82  LOAD_CONST               24
               84  BINARY_ADD       
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'numbytes'
               94  POP_BLOCK        
               96  JUMP_FORWARD        124  'to 124'
             98_0  COME_FROM_FINALLY    48  '48'

 L.1185        98  DUP_TOP          
              100  LOAD_GLOBAL              ValueError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   122  'to 122'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L.1186       112  POP_EXCEPT       
              114  POP_TOP          
              116  JUMP_FORWARD        156  'to 156'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           104  '104'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            96  '96'

 L.1187       124  LOAD_FAST                'offset'
              126  POP_JUMP_IF_FALSE   146  'to 146'
              128  LOAD_FAST                'numbytes'
              130  POP_JUMP_IF_FALSE   146  'to 146'

 L.1188       132  LOAD_FAST                'structs'
              134  LOAD_METHOD              append
              136  LOAD_FAST                'offset'
              138  LOAD_FAST                'numbytes'
              140  BUILD_TUPLE_2         2 
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           130  '130'
            146_1  COME_FROM           126  '126'

 L.1189       146  LOAD_FAST                'pos'
              148  LOAD_CONST               24
              150  INPLACE_ADD      
              152  STORE_FAST               'pos'
              154  JUMP_BACK            44  'to 44'
            156_0  COME_FROM           116  '116'
            156_1  COME_FROM            44  '44'

 L.1190       156  LOAD_GLOBAL              bool
              158  LOAD_FAST                'buf'
              160  LOAD_CONST               504
              162  BINARY_SUBSCR    
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'isextended'
              168  JUMP_BACK            16  'to 16'
            170_0  COME_FROM            18  '18'

 L.1191       170  LOAD_FAST                'structs'
              172  LOAD_FAST                'self'
              174  STORE_ATTR               sparse

 L.1193       176  LOAD_FAST                'tarfile'
              178  LOAD_ATTR                fileobj
              180  LOAD_METHOD              tell
              182  CALL_METHOD_0         0  ''
              184  LOAD_FAST                'self'
              186  STORE_ATTR               offset_data

 L.1194       188  LOAD_FAST                'self'
              190  LOAD_ATTR                offset_data
              192  LOAD_FAST                'self'
              194  LOAD_METHOD              _block
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                size
              200  CALL_METHOD_1         1  ''
              202  BINARY_ADD       
              204  LOAD_FAST                'tarfile'
              206  STORE_ATTR               offset

 L.1195       208  LOAD_FAST                'origsize'
              210  LOAD_FAST                'self'
              212  STORE_ATTR               size

 L.1196       214  LOAD_FAST                'self'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 116

                def _proc_pax(self, tarfile):
                    """Process an extended or global header as described in
           POSIX.1-2008.
        """
                    buf = tarfile.fileobj.read(self._block(self.size))
                    if self.type == XGLTYPE:
                        pax_headers = tarfile.pax_headers
                    else:
                        pax_headers = tarfile.pax_headers.copy()
                    match = re.search(b'\\d+ hdrcharset=([^\\n]+)\\n', buf)
                    if match is not None:
                        pax_headers['hdrcharset'] = match.group(1).decode('utf-8')
                    hdrcharset = pax_headers.get('hdrcharset')
                    if hdrcharset == 'BINARY':
                        encoding = tarfile.encoding
                    else:
                        encoding = 'utf-8'
                    regex = re.compile(b'(\\d+) ([^=]+)=')
                    pos = 0
                    while True:
                        match = regex.match(buf, pos)
                        if not match:
                            pass
                        else:
                            length, keyword = match.groups()
                            length = int(length)
                        if length == 0:
                            raise InvalidHeaderError('invalid header')
                        else:
                            value = buf[match.end(2) + 1:match.start(1) + length - 1]
                            keyword = self._decode_pax_field(keyword, 'utf-8', 'utf-8', tarfile.errors)
                            if keyword in PAX_NAME_FIELDS:
                                value = self._decode_pax_field(value, encoding, tarfile.encoding, tarfile.errors)
                            else:
                                value = self._decode_pax_field(value, 'utf-8', 'utf-8', tarfile.errors)
                            pax_headers[keyword] = value
                            pos += length

                    try:
                        next = self.fromtarfile(tarfile)
                    except HeaderError:
                        raise SubsequentHeaderError('missing or bad subsequent header')
                    else:
                        if 'GNU.sparse.map' in pax_headers:
                            self._proc_gnusparse_01(next, pax_headers)
                        elif 'GNU.sparse.size' in pax_headers:
                            self._proc_gnusparse_00(next, pax_headers, buf)
                        elif pax_headers.get('GNU.sparse.major') == '1':
                            if pax_headers.get('GNU.sparse.minor') == '0':
                                self._proc_gnusparse_10(next, pax_headers, tarfile)
                        if self.type in (XHDTYPE, SOLARIS_XHDTYPE):
                            next._apply_pax_info(pax_headers, tarfile.encoding, tarfile.errors)
                            next.offset = self.offset
                            if 'size' in pax_headers:
                                offset = next.offset_data
                                if next.isreg() or (next.type not in SUPPORTED_TYPES):
                                    offset += next._block(next.size)
                                tarfile.offset = offset
                        return next

                def _proc_gnusparse_00(self, next, pax_headers, buf):
                    """Process a GNU tar extended sparse header, version 0.0.
        """
                    offsets = []
                    for match in re.finditer(b'\\d+ GNU.sparse.offset=(\\d+)\\n', buf):
                        offsets.append(int(match.group(1)))
                    else:
                        numbytes = []
                        for match in re.finditer(b'\\d+ GNU.sparse.numbytes=(\\d+)\\n', buf):
                            numbytes.append(int(match.group(1)))
                        else:
                            next.sparse = list(zip(offsets, numbytes))

                def _proc_gnusparse_01(self, next, pax_headers):
                    """Process a GNU tar extended sparse header, version 0.1.
        """
                    sparse = [int(x) for x in pax_headers['GNU.sparse.map'].split(',')]
                    next.sparse = list(zip(sparse[::2], sparse[1::2]))

                def _proc_gnusparse_10(self, next, pax_headers, tarfile):
                    """Process a GNU tar extended sparse header, version 1.0.
        """
                    fields = None
                    sparse = []
                    buf = tarfile.fileobj.read(BLOCKSIZE)
                    fields, buf = buf.split(b'\n', 1)
                    fields = int(fields)
                    while True:
                        if len(sparse) < fields * 2:
                            if b'\n' not in buf:
                                buf += tarfile.fileobj.read(BLOCKSIZE)
                            number, buf = buf.split(b'\n', 1)
                            sparse.append(int(number))

                    next.offset_data = tarfile.fileobj.tell()
                    next.sparse = list(zip(sparse[::2], sparse[1::2]))

                def _apply_pax_info(self, pax_headers, encoding, errors):
                    """Replace fields with supplemental information from a previous
           pax extended or global header.
        """
                    for keyword, value in pax_headers.items():
                        if keyword == 'GNU.sparse.name':
                            setattr(self, 'path', value)
                        else:
                            if keyword == 'GNU.sparse.size':
                                setattr(self, 'size', int(value))
                            else:
                                if keyword == 'GNU.sparse.realsize':
                                    setattr(self, 'size', int(value))
                                else:
                                    if keyword in PAX_FIELDS:
                                        if keyword in PAX_NUMBER_FIELDS:
                                            try:
                                                value = PAX_NUMBER_FIELDS[keyword](value)
                                            except ValueError:
                                                value = 0

                                        if keyword == 'path':
                                            value = value.rstrip('/')
                                        else:
                                            setattr(self, keyword, value)
                    else:
                        self.pax_headers = pax_headers.copy()

                def _decode_pax_field(self, value, encoding, fallback_encoding, fallback_errors):
                    """Decode a single field from a pax record.
        """
                    try:
                        return value.decode(encoding, 'strict')
                    except UnicodeDecodeError:
                        return value.decode(fallback_encoding, fallback_errors)

                def _block(self, count):
                    """Round up a byte count by BLOCKSIZE and return it,
           e.g. _block(834) => 1024.
        """
                    blocks, remainder = divmod(count, BLOCKSIZE)
                    if remainder:
                        blocks += 1
                    return blocks * BLOCKSIZE

                def isreg(self):
                    """Return True if the Tarinfo object is a regular file."""
                    return self.type in REGULAR_TYPES

                def isfile(self):
                    """Return True if the Tarinfo object is a regular file."""
                    return self.isreg()

                def isdir(self):
                    """Return True if it is a directory."""
                    return self.type == DIRTYPE

                def issym(self):
                    """Return True if it is a symbolic link."""
                    return self.type == SYMTYPE

                def islnk(self):
                    """Return True if it is a hard link."""
                    return self.type == LNKTYPE

                def ischr(self):
                    """Return True if it is a character device."""
                    return self.type == CHRTYPE

                def isblk(self):
                    """Return True if it is a block device."""
                    return self.type == BLKTYPE

                def isfifo(self):
                    """Return True if it is a FIFO."""
                    return self.type == FIFOTYPE

                def issparse(self):
                    return self.sparse is not None

                def isdev(self):
                    """Return True if it is one of character device, block device or FIFO."""
                    return self.type in (CHRTYPE, BLKTYPE, FIFOTYPE)


            class TarFile(object):
                __doc__ = 'The TarFile Class provides an interface to tar archives.\n    '
                debug = 0
                dereference = False
                ignore_zeros = False
                errorlevel = 1
                format = DEFAULT_FORMAT
                encoding = ENCODING
                errors = None
                tarinfo = TarInfo
                fileobject = ExFileObject

                def __init__(self, name=None, mode='r', fileobj=None, format=None, tarinfo=None, dereference=None, ignore_zeros=None, encoding=None, errors='surrogateescape', pax_headers=None, debug=None, errorlevel=None, copybufsize=None):
                    """Open an (uncompressed) tar archive `name'. `mode' is either 'r' to
           read from an existing archive, 'a' to append data to an existing
           file or 'w' to create a new file overwriting an existing one. `mode'
           defaults to 'r'.
           If `fileobj' is given, it is used for reading or writing data. If it
           can be determined, `mode' is overridden by `fileobj's mode.
           `fileobj' is not closed, when TarFile is closed.
        """
                    modes = {'r':'rb', 
                     'a':'r+b',  'w':'wb',  'x':'xb'}
                    if mode not in modes:
                        raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
                    self.mode = mode
                    self._mode = modes[mode]
                    if not fileobj:
                        if self.mode == 'a':
                            if not os.path.exists(name):
                                self.mode = 'w'
                                self._mode = 'wb'
                        fileobj = bltn_open(name, self._mode)
                        self._extfileobj = False
                    else:
                        if name is None:
                            if hasattr(fileobj, 'name'):
                                if isinstance(fileobj.name, (str, bytes)):
                                    name = fileobj.name
                        if hasattr(fileobj, 'mode'):
                            self._mode = fileobj.mode
                        self._extfileobj = True
                    self.name = os.path.abspath(name) if name else None
                    self.fileobj = fileobj
                    if format is not None:
                        self.format = format
                    if tarinfo is not None:
                        self.tarinfo = tarinfo
                    if dereference is not None:
                        self.dereference = dereference
                    if ignore_zeros is not None:
                        self.ignore_zeros = ignore_zeros
                    if encoding is not None:
                        self.encoding = encoding
                    self.errors = errors
                    if pax_headers is not None and self.format == PAX_FORMAT:
                        self.pax_headers = pax_headers
                    else:
                        self.pax_headers = {}
                    if debug is not None:
                        self.debug = debug
                    if errorlevel is not None:
                        self.errorlevel = errorlevel
                    self.copybufsize = copybufsize
                    self.closed = False
                    self.members = []
                    self._loaded = False
                    self.offset = self.fileobj.tell()
                    self.inodes = {}
                    try:
                        if self.mode == 'r':
                            self.firstmember = None
                            self.firstmember = self.next()
                        if self.mode == 'a':
                            while True:
                                self.fileobj.seek(self.offset)
                                try:
                                    tarinfo = self.tarinfo.fromtarfile(self)
                                    self.members.append(tarinfo)
                                except EOFHeaderError:
                                    self.fileobj.seek(self.offset)
                                    break
                                except HeaderError as e:
                                    try:
                                        raise ReadError(str(e))
                                    finally:
                                        e = None
                                        del e

                            if self.mode in ('a', 'w', 'x'):
                                self._loaded = True
                                if self.pax_headers:
                                    buf = self.tarinfo.create_pax_global_header(self.pax_headers.copy())
                                    self.fileobj.write(buf)
                                    self.offset += len(buf)
                    except:
                        if not self._extfileobj:
                            self.fileobj.close()
                        else:
                            self.closed = True
                            raise

                @classmethod
                def open--- This code section failed: ---

 L.1589         0  LOAD_FAST                'name'
                2  POP_JUMP_IF_TRUE     16  'to 16'
                4  LOAD_FAST                'fileobj'
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.1590         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'nothing to open'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'
             16_1  COME_FROM             2  '2'

 L.1592        16  LOAD_FAST                'mode'
               18  LOAD_CONST               ('r', 'r:*')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE   170  'to 170'

 L.1594        24  LOAD_CLOSURE             'cls'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object not_compressed>
               30  LOAD_STR                 'TarFile.open.<locals>.not_compressed'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'not_compressed'

 L.1596        36  LOAD_GLOBAL              sorted
               38  LOAD_DEREF               'cls'
               40  LOAD_ATTR                OPEN_METH
               42  LOAD_FAST                'not_compressed'
               44  LOAD_CONST               ('key',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  GET_ITER         
             50_0  COME_FROM           156  '156'
             50_1  COME_FROM           152  '152'
             50_2  COME_FROM           148  '148'
               50  FOR_ITER            158  'to 158'
               52  STORE_FAST               'comptype'

 L.1597        54  LOAD_GLOBAL              getattr
               56  LOAD_DEREF               'cls'
               58  LOAD_DEREF               'cls'
               60  LOAD_ATTR                OPEN_METH
               62  LOAD_FAST                'comptype'
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'func'

 L.1598        70  LOAD_FAST                'fileobj'
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.1599        78  LOAD_FAST                'fileobj'
               80  LOAD_METHOD              tell
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'saved_pos'
             86_0  COME_FROM            76  '76'

 L.1600        86  SETUP_FINALLY       110  'to 110'

 L.1601        88  LOAD_FAST                'func'
               90  LOAD_FAST                'name'
               92  LOAD_STR                 'r'
               94  LOAD_FAST                'fileobj'
               96  BUILD_TUPLE_3         3 
               98  LOAD_FAST                'kwargs'
              100  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              102  POP_BLOCK        
              104  ROT_TWO          
              106  POP_TOP          
              108  RETURN_VALUE     
            110_0  COME_FROM_FINALLY    86  '86'

 L.1602       110  DUP_TOP          
              112  LOAD_GLOBAL              ReadError
              114  LOAD_GLOBAL              CompressionError
              116  BUILD_TUPLE_2         2 
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   154  'to 154'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.1603       128  LOAD_FAST                'fileobj'
              130  LOAD_CONST               None
              132  COMPARE_OP               is-not
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L.1604       136  LOAD_FAST                'fileobj'
              138  LOAD_METHOD              seek
              140  LOAD_FAST                'saved_pos'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           134  '134'

 L.1605       146  POP_EXCEPT       
              148  JUMP_BACK            50  'to 50'
              150  POP_EXCEPT       
              152  JUMP_BACK            50  'to 50'
            154_0  COME_FROM           120  '120'
              154  END_FINALLY      
              156  JUMP_BACK            50  'to 50'
            158_0  COME_FROM            50  '50'

 L.1606       158  LOAD_GLOBAL              ReadError
              160  LOAD_STR                 'file could not be opened successfully'
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
          166_168  JUMP_FORWARD        430  'to 430'
            170_0  COME_FROM            22  '22'

 L.1608       170  LOAD_STR                 ':'
              172  LOAD_FAST                'mode'
              174  COMPARE_OP               in
          176_178  POP_JUMP_IF_FALSE   268  'to 268'

 L.1609       180  LOAD_FAST                'mode'
              182  LOAD_METHOD              split
              184  LOAD_STR                 ':'
              186  LOAD_CONST               1
              188  CALL_METHOD_2         2  ''
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'filemode'
              194  STORE_FAST               'comptype'

 L.1610       196  LOAD_FAST                'filemode'
              198  JUMP_IF_TRUE_OR_POP   202  'to 202'
              200  LOAD_STR                 'r'
            202_0  COME_FROM           198  '198'
              202  STORE_FAST               'filemode'

 L.1611       204  LOAD_FAST                'comptype'
              206  JUMP_IF_TRUE_OR_POP   210  'to 210'
              208  LOAD_STR                 'tar'
            210_0  COME_FROM           206  '206'
              210  STORE_FAST               'comptype'

 L.1615       212  LOAD_FAST                'comptype'
              214  LOAD_DEREF               'cls'
              216  LOAD_ATTR                OPEN_METH
              218  COMPARE_OP               in
              220  POP_JUMP_IF_FALSE   240  'to 240'

 L.1616       222  LOAD_GLOBAL              getattr
              224  LOAD_DEREF               'cls'
              226  LOAD_DEREF               'cls'
              228  LOAD_ATTR                OPEN_METH
              230  LOAD_FAST                'comptype'
              232  BINARY_SUBSCR    
              234  CALL_FUNCTION_2       2  ''
              236  STORE_FAST               'func'
              238  JUMP_FORWARD        252  'to 252'
            240_0  COME_FROM           220  '220'

 L.1618       240  LOAD_GLOBAL              CompressionError
              242  LOAD_STR                 'unknown compression type %r'
              244  LOAD_FAST                'comptype'
              246  BINARY_MODULO    
              248  CALL_FUNCTION_1       1  ''
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           238  '238'

 L.1619       252  LOAD_FAST                'func'
              254  LOAD_FAST                'name'
              256  LOAD_FAST                'filemode'
              258  LOAD_FAST                'fileobj'
              260  BUILD_TUPLE_3         3 
              262  LOAD_FAST                'kwargs'
              264  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              266  RETURN_VALUE     
            268_0  COME_FROM           176  '176'

 L.1621       268  LOAD_STR                 '|'
              270  LOAD_FAST                'mode'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   402  'to 402'

 L.1622       278  LOAD_FAST                'mode'
              280  LOAD_METHOD              split
              282  LOAD_STR                 '|'
              284  LOAD_CONST               1
              286  CALL_METHOD_2         2  ''
              288  UNPACK_SEQUENCE_2     2 
              290  STORE_FAST               'filemode'
              292  STORE_FAST               'comptype'

 L.1623       294  LOAD_FAST                'filemode'
          296_298  JUMP_IF_TRUE_OR_POP   302  'to 302'
              300  LOAD_STR                 'r'
            302_0  COME_FROM           296  '296'
              302  STORE_FAST               'filemode'

 L.1624       304  LOAD_FAST                'comptype'
          306_308  JUMP_IF_TRUE_OR_POP   312  'to 312'
              310  LOAD_STR                 'tar'
            312_0  COME_FROM           306  '306'
              312  STORE_FAST               'comptype'

 L.1626       314  LOAD_FAST                'filemode'
              316  LOAD_CONST               ('r', 'w')
              318  COMPARE_OP               not-in
          320_322  POP_JUMP_IF_FALSE   332  'to 332'

 L.1627       324  LOAD_GLOBAL              ValueError
              326  LOAD_STR                 "mode must be 'r' or 'w'"
              328  CALL_FUNCTION_1       1  ''
              330  RAISE_VARARGS_1       1  'exception instance'
            332_0  COME_FROM           320  '320'

 L.1629       332  LOAD_GLOBAL              _Stream
              334  LOAD_FAST                'name'
              336  LOAD_FAST                'filemode'
              338  LOAD_FAST                'comptype'
              340  LOAD_FAST                'fileobj'
              342  LOAD_FAST                'bufsize'
              344  CALL_FUNCTION_5       5  ''
              346  STORE_FAST               'stream'

 L.1630       348  SETUP_FINALLY       370  'to 370'

 L.1631       350  LOAD_DEREF               'cls'
              352  LOAD_FAST                'name'
              354  LOAD_FAST                'filemode'
              356  LOAD_FAST                'stream'
              358  BUILD_TUPLE_3         3 
              360  LOAD_FAST                'kwargs'
              362  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              364  STORE_FAST               't'
              366  POP_BLOCK        
              368  JUMP_FORWARD        392  'to 392'
            370_0  COME_FROM_FINALLY   348  '348'

 L.1632       370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L.1633       376  LOAD_FAST                'stream'
              378  LOAD_METHOD              close
              380  CALL_METHOD_0         0  ''
              382  POP_TOP          

 L.1634       384  RAISE_VARARGS_0       0  'reraise'
              386  POP_EXCEPT       
              388  JUMP_FORWARD        392  'to 392'
              390  END_FINALLY      
            392_0  COME_FROM           388  '388'
            392_1  COME_FROM           368  '368'

 L.1635       392  LOAD_CONST               False
              394  LOAD_FAST                't'
              396  STORE_ATTR               _extfileobj

 L.1636       398  LOAD_FAST                't'
              400  RETURN_VALUE     
            402_0  COME_FROM           274  '274'

 L.1638       402  LOAD_FAST                'mode'
              404  LOAD_CONST               ('a', 'w', 'x')
              406  COMPARE_OP               in
          408_410  POP_JUMP_IF_FALSE   430  'to 430'

 L.1639       412  LOAD_DEREF               'cls'
              414  LOAD_ATTR                taropen
              416  LOAD_FAST                'name'
              418  LOAD_FAST                'mode'
              420  LOAD_FAST                'fileobj'
              422  BUILD_TUPLE_3         3 
              424  LOAD_FAST                'kwargs'
              426  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              428  RETURN_VALUE     
            430_0  COME_FROM           408  '408'
            430_1  COME_FROM           166  '166'

 L.1641       430  LOAD_GLOBAL              ValueError
              432  LOAD_STR                 'undiscernible mode'
              434  CALL_FUNCTION_1       1  ''
              436  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 104

                @classmethod
                def taropen(cls, name, mode='r', fileobj=None, **kwargs):
                    """Open uncompressed tar archive name for reading or writing.
        """
                    if mode not in ('r', 'a', 'w', 'x'):
                        raise ValueError("mode must be 'r', 'a', 'w' or 'x'")
                    return cls(name, mode, fileobj, **kwargs)

                @classmethod
                def gzopen(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
                    """Open gzip compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
                    if mode not in ('r', 'w', 'x'):
                        raise ValueError("mode must be 'r', 'w' or 'x'")
                    try:
                        from gzip import GzipFile
                    except ImportError:
                        raise CompressionError('gzip module is not available')

                    try:
                        fileobj = GzipFile(name, mode + 'b', compresslevel, fileobj)
                    except OSError:
                        if fileobj is not None:
                            if mode == 'r':
                                raise ReadError('not a gzip file')
                        raise
                    else:
                        try:
                            t = (cls.taropen)(name, mode, fileobj, **kwargs)
                        except OSError:
                            fileobj.close()
                            if mode == 'r':
                                raise ReadError('not a gzip file')
                            raise
                        except:
                            fileobj.close()
                            raise
                        else:
                            t._extfileobj = False
                            return t

                @classmethod
                def bz2open(cls, name, mode='r', fileobj=None, compresslevel=9, **kwargs):
                    """Open bzip2 compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
                    if mode not in ('r', 'w', 'x'):
                        raise ValueError("mode must be 'r', 'w' or 'x'")
                    try:
                        from bz2 import BZ2File
                    except ImportError:
                        raise CompressionError('bz2 module is not available')
                    else:
                        fileobj = BZ2File((fileobj or name), mode, compresslevel=compresslevel)
                        try:
                            t = (cls.taropen)(name, mode, fileobj, **kwargs)
                        except (OSError, EOFError):
                            fileobj.close()
                            if mode == 'r':
                                raise ReadError('not a bzip2 file')
                            raise
                        except:
                            fileobj.close()
                            raise
                        else:
                            t._extfileobj = False
                            return t

                @classmethod
                def xzopen(cls, name, mode='r', fileobj=None, preset=None, **kwargs):
                    """Open lzma compressed tar archive name for reading or writing.
           Appending is not allowed.
        """
                    if mode not in ('r', 'w', 'x'):
                        raise ValueError("mode must be 'r', 'w' or 'x'")
                    try:
                        from lzma import LZMAFile, LZMAError
                    except ImportError:
                        raise CompressionError('lzma module is not available')
                    else:
                        fileobj = LZMAFile((fileobj or name), mode, preset=preset)
                        try:
                            t = (cls.taropen)(name, mode, fileobj, **kwargs)
                        except (LZMAError, EOFError):
                            fileobj.close()
                            if mode == 'r':
                                raise ReadError('not an lzma file')
                            raise
                        except:
                            fileobj.close()
                            raise
                        else:
                            t._extfileobj = False
                            return t

                OPEN_METH = {'tar':'taropen', 
                 'gz':'gzopen', 
                 'bz2':'bz2open', 
                 'xz':'xzopen'}

                def close(self):
                    """Close the TarFile. In write-mode, two finishing zero blocks are
           appended to the archive.
        """
                    if self.closed:
                        return
                    self.closed = True
                    try:
                        if self.mode in ('a', 'w', 'x'):
                            self.fileobj.write(NUL * (BLOCKSIZE * 2))
                            self.offset += BLOCKSIZE * 2
                            blocks, remainder = divmod(self.offset, RECORDSIZE)
                            if remainder > 0:
                                self.fileobj.write(NUL * (RECORDSIZE - remainder))
                    finally:
                        if not self._extfileobj:
                            self.fileobj.close()

                def getmember(self, name):
                    """Return a TarInfo object for member `name'. If `name' can not be
           found in the archive, KeyError is raised. If a member occurs more
           than once in the archive, its last occurrence is assumed to be the
           most up-to-date version.
        """
                    tarinfo = self._getmember(name)
                    if tarinfo is None:
                        raise KeyError('filename %r not found' % name)
                    return tarinfo

                def getmembers(self):
                    """Return the members of the archive as a list of TarInfo objects. The
           list has the same order as the members in the archive.
        """
                    self._check()
                    if not self._loaded:
                        self._load()
                    return self.members

                def getnames(self):
                    """Return the members of the archive as a list of their names. It has
           the same order as the list returned by getmembers().
        """
                    return [tarinfo.name for tarinfo in self.getmembers()]

                def gettarinfo(self, name=None, arcname=None, fileobj=None):
                    """Create a TarInfo object from the result of os.stat or equivalent
           on an existing file. The file is either named by `name', or
           specified as a file object `fileobj' with a file descriptor. If
           given, `arcname' specifies an alternative name for the file in the
           archive, otherwise, the name is taken from the 'name' attribute of
           'fileobj', or the 'name' argument. The name should be a text
           string.
        """
                    self._check('awx')
                    if fileobj is not None:
                        name = fileobj.name
                    if arcname is None:
                        arcname = name
                    drv, arcname = os.path.splitdrive(arcname)
                    arcname = arcname.replace(os.sep, '/')
                    arcname = arcname.lstrip('/')
                    tarinfo = self.tarinfo()
                    tarinfo.tarfile = self
                    if fileobj is None:
                        if not self.dereference:
                            statres = os.lstat(name)
                        else:
                            statres = os.stat(name)
                    else:
                        statres = os.fstat(fileobj.fileno())
                    linkname = ''
                    stmd = statres.st_mode
                    if stat.S_ISREG(stmd):
                        inode = (
                         statres.st_ino, statres.st_dev)
                        if (self.dereference or statres.st_nlink) > 1 and inode in self.inodes and arcname != self.inodes[inode]:
                            type = LNKTYPE
                            linkname = self.inodes[inode]
                        else:
                            type = REGTYPE
                            if inode[0]:
                                self.inodes[inode] = arcname
                    elif stat.S_ISDIR(stmd):
                        type = DIRTYPE
                    elif stat.S_ISFIFO(stmd):
                        type = FIFOTYPE
                    elif stat.S_ISLNK(stmd):
                        type = SYMTYPE
                        linkname = os.readlink(name)
                    elif stat.S_ISCHR(stmd):
                        type = CHRTYPE
                    elif stat.S_ISBLK(stmd):
                        type = BLKTYPE
                    else:
                        return
                    tarinfo.name = arcname
                    tarinfo.mode = stmd
                    tarinfo.uid = statres.st_uid
                    tarinfo.gid = statres.st_gid
                    if type == REGTYPE:
                        tarinfo.size = statres.st_size
                    else:
                        tarinfo.size = 0
                    tarinfo.mtime = statres.st_mtime
                    tarinfo.type = type
                    tarinfo.linkname = linkname
                    if pwd:
                        try:
                            tarinfo.uname = pwd.getpwuid(tarinfo.uid)[0]
                        except KeyError:
                            pass

                    if grp:
                        try:
                            tarinfo.gname = grp.getgrgid(tarinfo.gid)[0]
                        except KeyError:
                            pass
                        else:
                            if type in (CHRTYPE, BLKTYPE):
                                if hasattr(os, 'major'):
                                    if hasattr(os, 'minor'):
                                        tarinfo.devmajor = os.major(statres.st_rdev)
                                        tarinfo.devminor = os.minor(statres.st_rdev)
                        return tarinfo

                def list(self, verbose=True, *, members=None):
                    """Print a table of contents to sys.stdout. If `verbose' is False, only
           the names of the members are printed. If it is True, an `ls -l'-like
           output is produced. `members' is optional and must be a subset of the
           list returned by getmembers().
        """
                    self._check()
                    if members is None:
                        members = self
                    for tarinfo in members:
                        if verbose:
                            _safe_print(stat.filemode(tarinfo.mode))
                            _safe_print('%s/%s' % (tarinfo.uname or tarinfo.uid,
                             tarinfo.gname or tarinfo.gid))
                            if tarinfo.ischr() or tarinfo.isblk():
                                _safe_print('%10s' % ('%d,%d' % (tarinfo.devmajor, tarinfo.devminor)))
                            else:
                                _safe_print('%10d' % tarinfo.size)
                            _safe_print('%d-%02d-%02d %02d:%02d:%02d' % time.localtime(tarinfo.mtime)[:6])
                        else:
                            _safe_print(tarinfo.name + ('/' if tarinfo.isdir() else ''))
                            if verbose:
                                if tarinfo.issym():
                                    _safe_print('-> ' + tarinfo.linkname)
                                if tarinfo.islnk():
                                    _safe_print('link to ' + tarinfo.linkname)
                            print()

                def add(self, name, arcname=None, recursive=True, *, filter=None):
                    """Add the file `name' to the archive. `name' may be any type of file
           (directory, fifo, symbolic link, etc.). If given, `arcname'
           specifies an alternative name for the file in the archive.
           Directories are added recursively by default. This can be avoided by
           setting `recursive' to False. `filter' is a function
           that expects a TarInfo object argument and returns the changed
           TarInfo object, if it returns None the TarInfo object will be
           excluded from the archive.
        """
                    self._check('awx')
                    if arcname is None:
                        arcname = name
                    if self.name is not None:
                        if os.path.abspath(name) == self.name:
                            self._dbg(2, 'tarfile: Skipped %r' % name)
                            return
                    self._dbg(1, name)
                    tarinfo = self.gettarinfo(name, arcname)
                    if tarinfo is None:
                        self._dbg(1, 'tarfile: Unsupported type %r' % name)
                        return
                    if filter is not None:
                        tarinfo = filter(tarinfo)
                        if tarinfo is None:
                            self._dbg(2, 'tarfile: Excluded %r' % name)
                            return
                    if tarinfo.isreg():
                        with bltn_open(name, 'rb') as f:
                            self.addfile(tarinfo, f)
                    elif tarinfo.isdir():
                        self.addfile(tarinfo)
                        if recursive:
                            for f in sorted(os.listdir(name)):
                                self.add((os.path.join(name, f)), (os.path.join(arcname, f)), recursive,
                                  filter=filter)

                    else:
                        self.addfile(tarinfo)

                def addfile(self, tarinfo, fileobj=None):
                    """Add the TarInfo object `tarinfo' to the archive. If `fileobj' is
           given, it should be a binary file, and tarinfo.size bytes are read
           from it and added to the archive. You can create TarInfo objects
           directly, or by using gettarinfo().
        """
                    self._check('awx')
                    tarinfo = copy.copy(tarinfo)
                    buf = tarinfo.tobuf(self.format, self.encoding, self.errors)
                    self.fileobj.write(buf)
                    self.offset += len(buf)
                    bufsize = self.copybufsize
                    if fileobj is not None:
                        copyfileobj(fileobj, (self.fileobj), (tarinfo.size), bufsize=bufsize)
                        blocks, remainder = divmod(tarinfo.size, BLOCKSIZE)
                        if remainder > 0:
                            self.fileobj.write(NUL * (BLOCKSIZE - remainder))
                            blocks += 1
                        self.offset += blocks * BLOCKSIZE
                    self.members.append(tarinfo)

                def extractall--- This code section failed: ---

 L.2014         0  BUILD_LIST_0          0 
                2  STORE_FAST               'directories'

 L.2016         4  LOAD_FAST                'members'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L.2017        12  LOAD_FAST                'self'
               14  STORE_FAST               'members'
             16_0  COME_FROM            10  '10'

 L.2019        16  LOAD_FAST                'members'
               18  GET_ITER         
             20_0  COME_FROM            82  '82'
               20  FOR_ITER             84  'to 84'
               22  STORE_FAST               'tarinfo'

 L.2020        24  LOAD_FAST                'tarinfo'
               26  LOAD_METHOD              isdir
               28  CALL_METHOD_0         0  ''
               30  POP_JUMP_IF_FALSE    58  'to 58'

 L.2022        32  LOAD_FAST                'directories'
               34  LOAD_METHOD              append
               36  LOAD_FAST                'tarinfo'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L.2023        42  LOAD_GLOBAL              copy
               44  LOAD_METHOD              copy
               46  LOAD_FAST                'tarinfo'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'tarinfo'

 L.2024        52  LOAD_CONST               448
               54  LOAD_FAST                'tarinfo'
               56  STORE_ATTR               mode
             58_0  COME_FROM            30  '30'

 L.2026        58  LOAD_FAST                'self'
               60  LOAD_ATTR                extract
               62  LOAD_FAST                'tarinfo'
               64  LOAD_FAST                'path'
               66  LOAD_FAST                'tarinfo'
               68  LOAD_METHOD              isdir
               70  CALL_METHOD_0         0  ''
               72  UNARY_NOT        

 L.2027        74  LOAD_FAST                'numeric_owner'

 L.2026        76  LOAD_CONST               ('set_attrs', 'numeric_owner')
               78  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               80  POP_TOP          
               82  JUMP_BACK            20  'to 20'
             84_0  COME_FROM            20  '20'

 L.2030        84  LOAD_FAST                'directories'
               86  LOAD_ATTR                sort
               88  LOAD_LAMBDA              '<code_object <lambda>>'
               90  LOAD_STR                 'TarFile.extractall.<locals>.<lambda>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               94  LOAD_CONST               ('key',)
               96  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               98  POP_TOP          

 L.2031       100  LOAD_FAST                'directories'
              102  LOAD_METHOD              reverse
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          

 L.2034       108  LOAD_FAST                'directories'
              110  GET_ITER         
            112_0  COME_FROM           242  '242'
            112_1  COME_FROM           238  '238'
            112_2  COME_FROM           176  '176'
              112  FOR_ITER            244  'to 244'
              114  STORE_FAST               'tarinfo'

 L.2035       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              join
              122  LOAD_FAST                'path'
              124  LOAD_FAST                'tarinfo'
              126  LOAD_ATTR                name
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'dirpath'

 L.2036       132  SETUP_FINALLY       178  'to 178'

 L.2037       134  LOAD_FAST                'self'
              136  LOAD_ATTR                chown
              138  LOAD_FAST                'tarinfo'
              140  LOAD_FAST                'dirpath'
              142  LOAD_FAST                'numeric_owner'
              144  LOAD_CONST               ('numeric_owner',)
              146  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              148  POP_TOP          

 L.2038       150  LOAD_FAST                'self'
              152  LOAD_METHOD              utime
              154  LOAD_FAST                'tarinfo'
              156  LOAD_FAST                'dirpath'
              158  CALL_METHOD_2         2  ''
              160  POP_TOP          

 L.2039       162  LOAD_FAST                'self'
              164  LOAD_METHOD              chmod
              166  LOAD_FAST                'tarinfo'
              168  LOAD_FAST                'dirpath'
              170  CALL_METHOD_2         2  ''
              172  POP_TOP          
              174  POP_BLOCK        
              176  JUMP_BACK           112  'to 112'
            178_0  COME_FROM_FINALLY   132  '132'

 L.2040       178  DUP_TOP          
              180  LOAD_GLOBAL              ExtractError
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   240  'to 240'
              186  POP_TOP          
              188  STORE_FAST               'e'
              190  POP_TOP          
              192  SETUP_FINALLY       228  'to 228'

 L.2041       194  LOAD_FAST                'self'
              196  LOAD_ATTR                errorlevel
              198  LOAD_CONST               1
              200  COMPARE_OP               >
              202  POP_JUMP_IF_FALSE   208  'to 208'

 L.2042       204  RAISE_VARARGS_0       0  'reraise'
              206  BREAK_LOOP          224  'to 224'
            208_0  COME_FROM           202  '202'

 L.2044       208  LOAD_FAST                'self'
              210  LOAD_METHOD              _dbg
              212  LOAD_CONST               1
              214  LOAD_STR                 'tarfile: %s'
              216  LOAD_FAST                'e'
              218  BINARY_MODULO    
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          
            224_0  COME_FROM           206  '206'
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   192  '192'
              228  LOAD_CONST               None
              230  STORE_FAST               'e'
              232  DELETE_FAST              'e'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_BACK           112  'to 112'
            240_0  COME_FROM           184  '184'
              240  END_FINALLY      
              242  JUMP_BACK           112  'to 112'
            244_0  COME_FROM           112  '112'

Parse error at or near `BEGIN_FINALLY' instruction at offset 226

                def extract(self, member, path='', set_attrs=True, *, numeric_owner=False):
                    """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. `member' may be a filename or a TarInfo object. You can
           specify a different directory using `path'. File attributes (owner,
           mtime, mode) are set unless `set_attrs' is False. If `numeric_owner`
           is True, only the numbers for user/group names are used and not
           the names.
        """
                    self._check('r')
                    if isinstance(member, str):
                        tarinfo = self.getmember(member)
                    else:
                        tarinfo = member
                    if tarinfo.islnk():
                        tarinfo._link_target = os.path.join(path, tarinfo.linkname)
                    try:
                        self._extract_member(tarinfo, (os.path.join(path, tarinfo.name)), set_attrs=set_attrs,
                          numeric_owner=numeric_owner)
                    except OSError as e:
                        try:
                            if self.errorlevel > 0:
                                raise
                            elif e.filename is None:
                                self._dbg(1, 'tarfile: %s' % e.strerror)
                            else:
                                self._dbg(1, 'tarfile: %s %r' % (e.strerror, e.filename))
                        finally:
                            e = None
                            del e

                    except ExtractError as e:
                        try:
                            if self.errorlevel > 1:
                                raise
                            else:
                                self._dbg(1, 'tarfile: %s' % e)
                        finally:
                            e = None
                            del e

                def extractfile(self, member):
                    """Extract a member from the archive as a file object. `member' may be
           a filename or a TarInfo object. If `member' is a regular file or a
           link, an io.BufferedReader object is returned. Otherwise, None is
           returned.
        """
                    self._check('r')
                    if isinstance(member, str):
                        tarinfo = self.getmember(member)
                    else:
                        tarinfo = member
                    if tarinfo.isreg() or (tarinfo.type not in SUPPORTED_TYPES):
                        return self.fileobject(self, tarinfo)
                    if tarinfo.islnk() or tarinfo.issym():
                        if isinstance(self.fileobj, _Stream):
                            raise StreamError('cannot extract (sym)link as file object')
                        else:
                            return self.extractfile(self._find_link_target(tarinfo))
                    else:
                        return

                def _extract_member(self, tarinfo, targetpath, set_attrs=True, numeric_owner=False):
                    """Extract the TarInfo object tarinfo to a physical
           file called targetpath.
        """
                    targetpath = targetpath.rstrip('/')
                    targetpath = targetpath.replace('/', os.sep)
                    upperdirs = os.path.dirname(targetpath)
                    if upperdirs:
                        if not os.path.exists(upperdirs):
                            os.makedirs(upperdirs)
                        if tarinfo.islnk() or tarinfo.issym():
                            self._dbg(1, '%s -> %s' % (tarinfo.name, tarinfo.linkname))
                        else:
                            self._dbg(1, tarinfo.name)
                        if tarinfo.isreg():
                            self.makefile(tarinfo, targetpath)
                        elif tarinfo.isdir():
                            self.makedir(tarinfo, targetpath)
                        elif tarinfo.isfifo():
                            self.makefifo(tarinfo, targetpath)
                        elif tarinfo.ischr() or tarinfo.isblk():
                            self.makedev(tarinfo, targetpath)
                        elif tarinfo.islnk() or tarinfo.issym():
                            self.makelink(tarinfo, targetpath)
                        elif tarinfo.type not in SUPPORTED_TYPES:
                            self.makeunknown(tarinfo, targetpath)
                        else:
                            self.makefile(tarinfo, targetpath)
                        if set_attrs:
                            self.chown(tarinfo, targetpath, numeric_owner)
                            if not tarinfo.issym():
                                self.chmod(tarinfo, targetpath)
                                self.utime(tarinfo, targetpath)

                def makedir(self, tarinfo, targetpath):
                    """Make a directory called targetpath.
        """
                    try:
                        os.mkdir(targetpath, 448)
                    except FileExistsError:
                        pass

                def makefile(self, tarinfo, targetpath):
                    """Make a file called targetpath.
        """
                    source = self.fileobj
                    source.seek(tarinfo.offset_data)
                    bufsize = self.copybufsize
                    with bltn_open(targetpath, 'wb') as target:
                        if tarinfo.sparse is not None:
                            for offset, size in tarinfo.sparse:
                                target.seek(offset)
                                copyfileobjsourcetargetsizeReadErrorbufsize
                            else:
                                target.seek(tarinfo.size)
                                target.truncate()

                        else:
                            copyfileobjsourcetargettarinfo.sizeReadErrorbufsize

                def makeunknown(self, tarinfo, targetpath):
                    """Make a file from a TarInfo object with an unknown type
           at targetpath.
        """
                    self.makefile(tarinfo, targetpath)
                    self._dbg(1, 'tarfile: Unknown file type %r, extracted as regular file.' % tarinfo.type)

                def makefifo(self, tarinfo, targetpath):
                    """Make a fifo called targetpath.
        """
                    if hasattr(os, 'mkfifo'):
                        os.mkfifo(targetpath)
                    else:
                        raise ExtractError('fifo not supported by system')

                def makedev(self, tarinfo, targetpath):
                    """Make a character or block device called targetpath.
        """
                    if not (hasattr(os, 'mknod') and hasattr(os, 'makedev')):
                        raise ExtractError('special devices not supported by system')
                    mode = tarinfo.mode
                    if tarinfo.isblk():
                        mode |= stat.S_IFBLK
                    else:
                        mode |= stat.S_IFCHR
                    os.mknod(targetpath, mode, os.makedev(tarinfo.devmajor, tarinfo.devminor))

                def makelink(self, tarinfo, targetpath):
                    """Make a (symbolic) link called targetpath. If it cannot be created
          (platform limitation), we try to make a copy of the referenced file
          instead of a link.
        """
                    try:
                        if tarinfo.issym():
                            os.symlink(tarinfo.linkname, targetpath)
                        elif os.path.exists(tarinfo._link_target):
                            os.link(tarinfo._link_target, targetpath)
                        else:
                            self._extract_member(self._find_link_target(tarinfo), targetpath)
                    except symlink_exception:
                        try:
                            self._extract_member(self._find_link_target(tarinfo), targetpath)
                        except KeyError:
                            raise ExtractError('unable to resolve link inside archive')

                def chown(self, tarinfo, targetpath, numeric_owner):
                    """Set owner of targetpath according to tarinfo. If numeric_owner
           is True, use .gid/.uid instead of .gname/.uname. If numeric_owner
           is False, fall back to .gid/.uid when the search based on name
           fails.
        """
                    if not hasattr(os, 'geteuid') or os.geteuid() == 0:
                        g = tarinfo.gid
                        u = tarinfo.uid
                        if not numeric_owner:
                            try:
                                if grp:
                                    g = grp.getgrnam(tarinfo.gname)[2]
                            except KeyError:
                                pass

                            try:
                                if pwd:
                                    u = pwd.getpwnam(tarinfo.uname)[2]
                            except KeyError:
                                pass

                        try:
                            if tarinfo.issym() and hasattr(os, 'lchown'):
                                os.lchown(targetpath, u, g)
                            else:
                                os.chown(targetpath, u, g)
                        except OSError:
                            raise ExtractError('could not change owner')

                def chmod(self, tarinfo, targetpath):
                    """Set file permissions of targetpath according to tarinfo.
        """
                    try:
                        os.chmod(targetpath, tarinfo.mode)
                    except OSError:
                        raise ExtractError('could not change mode')

                def utime(self, tarinfo, targetpath):
                    """Set modification time of targetpath according to tarinfo.
        """
                    if not hasattr(os, 'utime'):
                        return
                    try:
                        os.utime(targetpath, (tarinfo.mtime, tarinfo.mtime))
                    except OSError:
                        raise ExtractError('could not change modification time')

                def next--- This code section failed: ---

 L.2297         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check
                4  LOAD_STR                 'ra'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.2298        10  LOAD_FAST                'self'
               12  LOAD_ATTR                firstmember
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L.2299        20  LOAD_FAST                'self'
               22  LOAD_ATTR                firstmember
               24  STORE_FAST               'm'

 L.2300        26  LOAD_CONST               None
               28  LOAD_FAST                'self'
               30  STORE_ATTR               firstmember

 L.2301        32  LOAD_FAST                'm'
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'

 L.2304        36  LOAD_FAST                'self'
               38  LOAD_ATTR                offset
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                fileobj
               44  LOAD_METHOD              tell
               46  CALL_METHOD_0         0  ''
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    90  'to 90'

 L.2305        52  LOAD_FAST                'self'
               54  LOAD_ATTR                fileobj
               56  LOAD_METHOD              seek
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                offset
               62  LOAD_CONST               1
               64  BINARY_SUBTRACT  
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.2306        70  LOAD_FAST                'self'
               72  LOAD_ATTR                fileobj
               74  LOAD_METHOD              read
               76  LOAD_CONST               1
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_TRUE     90  'to 90'

 L.2307        82  LOAD_GLOBAL              ReadError
               84  LOAD_STR                 'unexpected end of data'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            50  '50'

 L.2310        90  LOAD_CONST               None
               92  STORE_FAST               'tarinfo'
             94_0  COME_FROM           460  '460'
             94_1  COME_FROM           266  '266'
             94_2  COME_FROM           178  '178'

 L.2312        94  SETUP_FINALLY       114  'to 114'

 L.2313        96  LOAD_FAST                'self'
               98  LOAD_ATTR                tarinfo
              100  LOAD_METHOD              fromtarfile
              102  LOAD_FAST                'self'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'tarinfo'
              108  POP_BLOCK        
          110_112  JUMP_FORWARD        462  'to 462'
            114_0  COME_FROM_FINALLY    94  '94'

 L.2314       114  DUP_TOP          
              116  LOAD_GLOBAL              EOFHeaderError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   198  'to 198'
              122  POP_TOP          
              124  STORE_FAST               'e'
              126  POP_TOP          
              128  SETUP_FINALLY       184  'to 184'

 L.2315       130  LOAD_FAST                'self'
              132  LOAD_ATTR                ignore_zeros
              134  POP_JUMP_IF_FALSE   180  'to 180'

 L.2316       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _dbg
              140  LOAD_CONST               2
              142  LOAD_STR                 '0x%X: %s'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                offset
              148  LOAD_FAST                'e'
              150  BUILD_TUPLE_2         2 
              152  BINARY_MODULO    
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          

 L.2317       158  LOAD_FAST                'self'
              160  DUP_TOP          
              162  LOAD_ATTR                offset
              164  LOAD_GLOBAL              BLOCKSIZE
              166  INPLACE_ADD      
              168  ROT_TWO          
              170  STORE_ATTR               offset

 L.2318       172  POP_BLOCK        
              174  POP_EXCEPT       
              176  CALL_FINALLY        184  'to 184'
              178  JUMP_BACK            94  'to 94'
            180_0  COME_FROM           134  '134'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM           176  '176'
            184_1  COME_FROM_FINALLY   128  '128'
              184  LOAD_CONST               None
              186  STORE_FAST               'e'
              188  DELETE_FAST              'e'
              190  END_FINALLY      
              192  POP_EXCEPT       
          194_196  JUMP_FORWARD        462  'to 462'
            198_0  COME_FROM           120  '120'

 L.2319       198  DUP_TOP          
              200  LOAD_GLOBAL              InvalidHeaderError
              202  COMPARE_OP               exception-match
          204_206  POP_JUMP_IF_FALSE   310  'to 310'
              208  POP_TOP          
              210  STORE_FAST               'e'
              212  POP_TOP          
              214  SETUP_FINALLY       298  'to 298'

 L.2320       216  LOAD_FAST                'self'
              218  LOAD_ATTR                ignore_zeros
          220_222  POP_JUMP_IF_FALSE   270  'to 270'

 L.2321       224  LOAD_FAST                'self'
              226  LOAD_METHOD              _dbg
              228  LOAD_CONST               2
              230  LOAD_STR                 '0x%X: %s'
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                offset
              236  LOAD_FAST                'e'
              238  BUILD_TUPLE_2         2 
              240  BINARY_MODULO    
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          

 L.2322       246  LOAD_FAST                'self'
              248  DUP_TOP          
              250  LOAD_ATTR                offset
              252  LOAD_GLOBAL              BLOCKSIZE
              254  INPLACE_ADD      
              256  ROT_TWO          
              258  STORE_ATTR               offset

 L.2323       260  POP_BLOCK        
              262  POP_EXCEPT       
              264  CALL_FINALLY        298  'to 298'
              266  JUMP_BACK            94  'to 94'
              268  JUMP_FORWARD        294  'to 294'
            270_0  COME_FROM           220  '220'

 L.2324       270  LOAD_FAST                'self'
              272  LOAD_ATTR                offset
              274  LOAD_CONST               0
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   294  'to 294'

 L.2325       282  LOAD_GLOBAL              ReadError
              284  LOAD_GLOBAL              str
              286  LOAD_FAST                'e'
              288  CALL_FUNCTION_1       1  ''
              290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           278  '278'
            294_1  COME_FROM           268  '268'
              294  POP_BLOCK        
              296  BEGIN_FINALLY    
            298_0  COME_FROM           264  '264'
            298_1  COME_FROM_FINALLY   214  '214'
              298  LOAD_CONST               None
              300  STORE_FAST               'e'
              302  DELETE_FAST              'e'
              304  END_FINALLY      
              306  POP_EXCEPT       
              308  JUMP_FORWARD        462  'to 462'
            310_0  COME_FROM           204  '204'

 L.2326       310  DUP_TOP          
              312  LOAD_GLOBAL              EmptyHeaderError
              314  COMPARE_OP               exception-match
          316_318  POP_JUMP_IF_FALSE   350  'to 350'
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L.2327       326  LOAD_FAST                'self'
              328  LOAD_ATTR                offset
              330  LOAD_CONST               0
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   346  'to 346'

 L.2328       338  LOAD_GLOBAL              ReadError
              340  LOAD_STR                 'empty file'
              342  CALL_FUNCTION_1       1  ''
              344  RAISE_VARARGS_1       1  'exception instance'
            346_0  COME_FROM           334  '334'
              346  POP_EXCEPT       
              348  JUMP_FORWARD        462  'to 462'
            350_0  COME_FROM           316  '316'

 L.2329       350  DUP_TOP          
              352  LOAD_GLOBAL              TruncatedHeaderError
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   408  'to 408'
              360  POP_TOP          
              362  STORE_FAST               'e'
              364  POP_TOP          
              366  SETUP_FINALLY       396  'to 396'

 L.2330       368  LOAD_FAST                'self'
              370  LOAD_ATTR                offset
              372  LOAD_CONST               0
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   392  'to 392'

 L.2331       380  LOAD_GLOBAL              ReadError
              382  LOAD_GLOBAL              str
              384  LOAD_FAST                'e'
              386  CALL_FUNCTION_1       1  ''
              388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           376  '376'
              392  POP_BLOCK        
              394  BEGIN_FINALLY    
            396_0  COME_FROM_FINALLY   366  '366'
              396  LOAD_CONST               None
              398  STORE_FAST               'e'
              400  DELETE_FAST              'e'
              402  END_FINALLY      
              404  POP_EXCEPT       
              406  JUMP_FORWARD        462  'to 462'
            408_0  COME_FROM           356  '356'

 L.2332       408  DUP_TOP          
              410  LOAD_GLOBAL              SubsequentHeaderError
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   454  'to 454'
              418  POP_TOP          
              420  STORE_FAST               'e'
              422  POP_TOP          
              424  SETUP_FINALLY       442  'to 442'

 L.2333       426  LOAD_GLOBAL              ReadError
              428  LOAD_GLOBAL              str
              430  LOAD_FAST                'e'
              432  CALL_FUNCTION_1       1  ''
              434  CALL_FUNCTION_1       1  ''
              436  RAISE_VARARGS_1       1  'exception instance'
              438  POP_BLOCK        
              440  BEGIN_FINALLY    
            442_0  COME_FROM_FINALLY   424  '424'
              442  LOAD_CONST               None
              444  STORE_FAST               'e'
              446  DELETE_FAST              'e'
              448  END_FINALLY      
              450  POP_EXCEPT       
              452  JUMP_FORWARD        462  'to 462'
            454_0  COME_FROM           414  '414'
              454  END_FINALLY      

 L.2334   456_458  JUMP_FORWARD        462  'to 462'
              460  JUMP_BACK            94  'to 94'
            462_0  COME_FROM           456  '456'
            462_1  COME_FROM           452  '452'
            462_2  COME_FROM           406  '406'
            462_3  COME_FROM           348  '348'
            462_4  COME_FROM           308  '308'
            462_5  COME_FROM           194  '194'
            462_6  COME_FROM           110  '110'

 L.2336       462  LOAD_FAST                'tarinfo'
              464  LOAD_CONST               None
              466  COMPARE_OP               is-not
          468_470  POP_JUMP_IF_FALSE   486  'to 486'

 L.2337       472  LOAD_FAST                'self'
              474  LOAD_ATTR                members
              476  LOAD_METHOD              append
              478  LOAD_FAST                'tarinfo'
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
              484  JUMP_FORWARD        492  'to 492'
            486_0  COME_FROM           468  '468'

 L.2339       486  LOAD_CONST               True
              488  LOAD_FAST                'self'
              490  STORE_ATTR               _loaded
            492_0  COME_FROM           484  '484'

 L.2341       492  LOAD_FAST                'tarinfo'
              494  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 174

                def _getmember(self, name, tarinfo=None, normalize=False):
                    """Find an archive member by name from bottom to top.
           If tarinfo is given, it is used as the starting point.
        """
                    members = self.getmembers()
                    if tarinfo is not None:
                        members = members[:members.index(tarinfo)]
                    if normalize:
                        name = os.path.normpath(name)
                    for member in reversed(members):
                        if normalize:
                            member_name = os.path.normpath(member.name)
                        else:
                            member_name = member.name
                        if name == member_name:
                            return member

                def _load--- This code section failed: ---
              0_0  COME_FROM            18  '18'
              0_1  COME_FROM            14  '14'

 L.2374         0  LOAD_FAST                'self'
                2  LOAD_METHOD              next
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tarinfo'

 L.2375         8  LOAD_FAST                'tarinfo'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L.2376        16  JUMP_FORWARD         20  'to 20'
               18  JUMP_BACK             0  'to 0'
             20_0  COME_FROM            16  '16'

 L.2377        20  LOAD_CONST               True
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _loaded

Parse error at or near `JUMP_BACK' instruction at offset 18

                def _check(self, mode=None):
                    """Check if TarFile is still open, and if the operation's mode
           corresponds to TarFile's mode.
        """
                    if self.closed:
                        raise OSError('%s is closed' % self.__class__.__name__)
                    if mode is not None:
                        if self.mode not in mode:
                            raise OSError('bad operation for mode %r' % self.mode)

                def _find_link_target(self, tarinfo):
                    """Find the target member of a symlink or hardlink member in the
           archive.
        """
                    if tarinfo.issym():
                        linkname = '/'.join(filter(None, (os.path.dirname(tarinfo.name), tarinfo.linkname)))
                        limit = None
                    else:
                        linkname = tarinfo.linkname
                        limit = tarinfo
                    member = self._getmember(linkname, tarinfo=limit, normalize=True)
                    if member is None:
                        raise KeyError('linkname %r not found' % linkname)
                    return member

                def __iter__(self):
                    """Provide an iterator object.
        """
                    if self._loaded:
                        yield from self.members
                        return
                    index = 0
                    if self.firstmember is not None:
                        tarinfo = self.next()
                        index += 1
                        yield tarinfo
                    while True:
                        if index < len(self.members):
                            tarinfo = self.members[index]
                        elif not self._loaded:
                            tarinfo = self.next()
                            if not tarinfo:
                                self._loaded = True
                                return
                        else:
                            return
                        index += 1
                        yield tarinfo

                def _dbg(self, level, msg):
                    """Write debugging output to sys.stderr.
        """
                    if level <= self.debug:
                        print(msg, file=(sys.stderr))

                def __enter__(self):
                    self._check()
                    return self

                def __exit__(self, type, value, traceback):
                    if type is None:
                        self.close()
                    else:
                        if not self._extfileobj:
                            self.fileobj.close()
                        self.closed = True


            def is_tarfile--- This code section failed: ---

 L.2465         0  SETUP_FINALLY        24  'to 24'

 L.2466         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               't'

 L.2467        10  LOAD_FAST                't'
               12  LOAD_METHOD              close
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L.2468        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.2469        24  DUP_TOP          
               26  LOAD_GLOBAL              TarError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.2470        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 24


            open = TarFile.open

            def main():
                import argparse
                description = 'A simple command-line interface for tarfile module.'
                parser = argparse.ArgumentParser(description=description)
                parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')
                group = parser.add_mutually_exclusive_group(required=True)
                group.add_argument('-l', '--list', metavar='<tarfile>', help='Show listing of a tarfile')
                group.add_argument('-e', '--extract', nargs='+', metavar=('<tarfile>',
                                                                          '<output_dir>'),
                  help='Extract tarfile into target dir')
                group.add_argument('-c', '--create', nargs='+', metavar=('<name>',
                                                                         '<file>'),
                  help='Create tarfile from sources')
                group.add_argument('-t', '--test', metavar='<tarfile>', help='Test if a tarfile is valid')
                args = parser.parse_args()
                if args.test is not None:
                    src = args.test
                    if is_tarfile(src):
                        with open(src, 'r') as tar:
                            tar.getmembers()
                            print((tar.getmembers()), file=(sys.stderr))
                        if args.verbose:
                            print('{!r} is a tar archive.'.format(src))
                    else:
                        parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
                elif args.list is not None:
                    src = args.list
                    if is_tarfile(src):
                        with TarFile.open(src, 'r:*') as tf:
                            tf.list(verbose=(args.verbose))
                    else:
                        parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
                elif args.extract is not None:
                    if len(args.extract) == 1:
                        src = args.extract[0]
                        curdir = os.curdir
                    elif len(args.extract) == 2:
                        src, curdir = args.extract
                    else:
                        parser.exit(1, parser.format_help())
                    if is_tarfile(src):
                        with TarFile.open(src, 'r:*') as tf:
                            tf.extractall(path=curdir)
                        if args.verbose:
                            if curdir == '.':
                                msg = '{!r} file is extracted.'.format(src)
                            else:
                                msg = '{!r} file is extracted into {!r} directory.'.format(src, curdir)
                            print(msg)
                    else:
                        parser.exit(1, '{!r} is not a tar archive.\n'.format(src))
                elif args.create is not None:
                    tar_name = args.create.pop(0)
                    _, ext = os.path.splitext(tar_name)
                    compressions = {'.gz':'gz', 
                     '.tgz':'gz', 
                     '.xz':'xz', 
                     '.txz':'xz', 
                     '.bz2':'bz2', 
                     '.tbz':'bz2', 
                     '.tbz2':'bz2', 
                     '.tb2':'bz2'}
                    tar_mode = 'w:' + compressions[ext] if ext in compressions else 'w'
                    tar_files = args.create
                    with TarFile.open(tar_name, tar_mode) as tf:
                        for file_name in tar_files:
                            tf.add(file_name)

                    if args.verbose:
                        print('{!r} file created.'.format(tar_name))


            if __name__ == '__main__':
                main()