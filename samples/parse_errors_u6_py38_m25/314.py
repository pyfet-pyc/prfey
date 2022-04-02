# uncompyle6 version 3.7.4
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
        PAX_FIELDS = ('path', 'linkpath', 'size', 'mtime', 'uid', 'gid', 'uname', 'gname')
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

                if s[0] == 255:
                    n = -(256 ** (len(s) - 1) - n)
            else:
                try:
                    s = nts(s, 'ascii', 'strict')
                    n = int(s.strip() or '0', 8)
                except ValueError:
                    raise InvalidHeaderError('invalid header')

            return n


        def itn(n, digits=8, format=DEFAULT_FORMAT):
            """Convert a python number to a number field.
    """
            n = int(n)
            if 0 <= n < 8 ** (digits - 1):
                s = bytes('%0*o' % (digits - 1, n), 'ascii') + NUL
            else:
                if format == GNU_FORMAT:
                    if -256 ** (digits - 1) <= n < 256 ** (digits - 1):
                        if n >= 0:
                            s = bytearray([128])
                    else:
                        s = bytearray([255])
                        n = 256 ** digits + n
                    for i in range(digits - 1):
                        s.insert(1, n & 255)
                        n >>= 8

                else:
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
            return (unsigned_chksum, signed_chksum)


        def copyfileobj(src, dst, length=None, exception=OSError, bufsize=None):
            """Copy length bytes from fileobj src to fileobj dst.
       If length is None, copy the entire content.
    """
            bufsize = bufsize or 16384
            if length == 0:
                return
            if length is None:
                shutil.copyfileobj(src, dst, bufsize)
                return None
            blocks, remainder = divmod(length, bufsize)
            for b in range(blocks):
                buf = src.read(bufsize)
                if len(buf) < bufsize:
                    raise exception('unexpected end of data')
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
                    else:
                        if comptype == 'bz2':
                            try:
                                import bz2
                            except ImportError:
                                raise CompressionError('bz2 module is not available')
                            else:
                                if mode == 'r':
                                    self.dbuf = b''
                                    self.cmp = bz2.BZ2Decompressor()
                                    self.exception = OSError
                                else:
                                    self.cmp = bz2.BZ2Compressor()
                        else:
                            if comptype == 'xz':
                                try:
                                    import lzma
                                except ImportError:
                                    raise CompressionError('lzma module is not available')
                                else:
                                    if mode == 'r':
                                        self.dbuf = b''
                                        self.cmp = lzma.LZMADecompressor()
                                        self.exception = lzma.LZMAError
                                    else:
                                        self.cmp = lzma.LZMACompressor()
                            else:
                                if comptype != 'tar':
                                    raise CompressionError('unknown compression type %r' % comptype)
                except:
                    if not self._extfileobj:
                        self.fileobj.close()
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
                while len(self.buf) > self.bufsize:
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

            def _init_read_gz(self):
                """Initialize for reading a gzip compressed fileobj.
        """
                self.cmp = self.zlib.decompressobj(-self.zlib.MAX_WBITS)
                self.dbuf = b''
                if self._Stream__read(2) != b'\x1f\x8b':
                    raise ReadError('not a gzip file')
                if self._Stream__read(1) != b'\x08':
                    raise CompressionError('unsupported compression method')
                flag = ord(self._Stream__read(1))
                self._Stream__read(6)
                if flag & 4:
                    xlen = ord(self._Stream__read(1)) + 256 * ord(self._Stream__read(1))
                    self.read(xlen)
                if flag & 8:
                    while True:
                        s = self._Stream__read(1)
                        if s:
                            if s == NUL:
                                break

                if flag & 16:
                    while True:
                        s = self._Stream__read(1)
                        if s:
                            if s == NUL:
                                break

                if flag & 2:
                    self._Stream__read(2)

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
                else:
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
                                    break
                                else:
                                    try:
                                        buf = self.cmp.decompress(buf)
                                    except self.exception:
                                        raise ReadError('invalid compressed data')

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
                while c < size:
                    buf = self.fileobj.read(self.bufsize)
                    if not buf:
                        break
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
                else:
                    if whence == io.SEEK_CUR:
                        if position < 0:
                            self.position = max(self.position + position, 0)
                        else:
                            self.position = min(self.position + position, self.size)
                    elif whence == io.SEEK_END:
                        self.position = max(min(self.size + position, self.size), 0)
                    else:
                        raise ValueError('Invalid argument')
                return self.position

            def read--- This code section failed: ---

 L. 664         0  LOAD_FAST                'size'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 665         8  LOAD_FAST                'self'
               10  LOAD_ATTR                size
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                position
               16  BINARY_SUBTRACT  
               18  STORE_FAST               'size'
               20  JUMP_FORWARD         40  'to 40'
             22_0  COME_FROM             6  '6'

 L. 667        22  LOAD_GLOBAL              min
               24  LOAD_FAST                'size'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                size
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                position
               34  BINARY_SUBTRACT  
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'size'
             40_0  COME_FROM            20  '20'

 L. 669        40  LOAD_CONST               b''
               42  STORE_FAST               'buf'

 L. 670        44  LOAD_FAST                'size'
               46  LOAD_CONST               0
               48  COMPARE_OP               >
            50_52  POP_JUMP_IF_FALSE   262  'to 262'
             54_0  COME_FROM           132  '132'

 L. 672        54  LOAD_FAST                'self'
               56  LOAD_ATTR                map
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                map_index
               62  BINARY_SUBSCR    
               64  UNPACK_SEQUENCE_4     4 
               66  STORE_FAST               'data'
               68  STORE_FAST               'start'
               70  STORE_FAST               'stop'
               72  STORE_FAST               'offset'

 L. 673        74  LOAD_FAST                'start'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                position
               80  DUP_TOP          
               82  ROT_THREE        
               84  COMPARE_OP               <=
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_FAST                'stop'
               90  COMPARE_OP               <
               92  POP_JUMP_IF_FALSE   104  'to 104'
               94  BREAK_LOOP          142  'to 142'
             96_0  COME_FROM            86  '86'
               96  POP_TOP          
               98  JUMP_FORWARD        104  'to 104'

 L. 674       100  BREAK_LOOP          142  'to 142'
              102  JUMP_BACK            54  'to 54'
            104_0  COME_FROM            98  '98'
            104_1  COME_FROM            92  '92'

 L. 676       104  LOAD_FAST                'self'
              106  DUP_TOP          
              108  LOAD_ATTR                map_index
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  ROT_TWO          
              116  STORE_ATTR               map_index

 L. 677       118  LOAD_FAST                'self'
              120  LOAD_ATTR                map_index
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                map
              128  CALL_FUNCTION_1       1  ''
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE    54  'to 54'

 L. 678       134  LOAD_CONST               0
              136  LOAD_FAST                'self'
              138  STORE_ATTR               map_index
              140  JUMP_BACK            54  'to 54'

 L. 679       142  LOAD_GLOBAL              min
              144  LOAD_FAST                'size'
              146  LOAD_FAST                'stop'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                position
              152  BINARY_SUBTRACT  
              154  CALL_FUNCTION_2       2  ''
              156  STORE_FAST               'length'

 L. 680       158  LOAD_FAST                'data'
              160  POP_JUMP_IF_FALSE   226  'to 226'

 L. 681       162  LOAD_FAST                'self'
              164  LOAD_ATTR                fileobj
              166  LOAD_METHOD              seek
              168  LOAD_FAST                'offset'
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                position
              174  LOAD_FAST                'start'
              176  BINARY_SUBTRACT  
              178  BINARY_ADD       
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 682       184  LOAD_FAST                'self'
              186  LOAD_ATTR                fileobj
              188  LOAD_METHOD              read
              190  LOAD_FAST                'length'
              192  CALL_METHOD_1         1  ''
              194  STORE_FAST               'b'

 L. 683       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'b'
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_FAST                'length'
              204  COMPARE_OP               !=
              206  POP_JUMP_IF_FALSE   216  'to 216'

 L. 684       208  LOAD_GLOBAL              ReadError
              210  LOAD_STR                 'unexpected end of data'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           206  '206'

 L. 685       216  LOAD_FAST                'buf'
              218  LOAD_FAST                'b'
              220  INPLACE_ADD      
              222  STORE_FAST               'buf'
              224  JUMP_FORWARD        238  'to 238'
            226_0  COME_FROM           160  '160'

 L. 687       226  LOAD_FAST                'buf'
              228  LOAD_GLOBAL              NUL
              230  LOAD_FAST                'length'
              232  BINARY_MULTIPLY  
              234  INPLACE_ADD      
              236  STORE_FAST               'buf'
            238_0  COME_FROM           224  '224'

 L. 688       238  LOAD_FAST                'size'
              240  LOAD_FAST                'length'
              242  INPLACE_SUBTRACT 
              244  STORE_FAST               'size'

 L. 689       246  LOAD_FAST                'self'
              248  DUP_TOP          
              250  LOAD_ATTR                position
              252  LOAD_FAST                'length'
              254  INPLACE_ADD      
              256  ROT_TWO          
              258  STORE_ATTR               position
              260  JUMP_BACK            44  'to 44'
            262_0  COME_FROM            50  '50'

 L. 690       262  LOAD_FAST                'buf'
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 98

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
             42_0  COME_FROM           134  '134'
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
              134  POP_JUMP_IF_FALSE    42  'to 42'

 L. 883       136  LOAD_FAST                'info'
              138  LOAD_FAST                'name'
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'pax_headers'
              144  LOAD_FAST                'hname'
              146  STORE_SUBSCR     
              148  JUMP_BACK            42  'to 42'

 L. 887       150  LOAD_CONST               (('uid', 8), ('gid', 8), ('size', 12), ('mtime', 12))
              152  GET_ITER         
            154_0  COME_FROM           228  '228'
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
              228  POP_JUMP_IF_FALSE   154  'to 154'
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

Parse error at or near `POP_EXCEPT' instruction at offset 114

            @classmethod
            def create_pax_global_header(cls, pax_headers):
                """Return the object as a pax global header block sequence.
        """
                return cls._create_pax_generic_header(pax_headers, XGLTYPE, 'utf-8')

            def _posix_split_name(self, name, encoding, errors):
                """Split a name longer than 100 chars into a prefix
           and a name part.
        """
                components = name.split('/')
                for i in range(1, len(components)):
                    prefix = '/'.join(components[:i])
                    name = '/'.join(components[i:])
                    if len(prefix.encode(encoding, errors)) <= LENGTH_PREFIX and len(name.encode(encoding, errors)) <= LENGTH_NAME:
                        break
                    raise ValueError('name is too long')
                    return (
                     prefix, name)

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
               60  BREAK_LOOP           70  'to 70'
               62  POP_EXCEPT       
               64  JUMP_BACK            12  'to 12'
             66_0  COME_FROM            44  '44'
               66  END_FINALLY      
               68  JUMP_BACK            12  'to 12'

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

 L.1018       192  BREAK_LOOP          200  'to 200'
            194_0  COME_FROM           190  '190'

 L.1019       194  LOAD_FAST                'n'
              196  STORE_FAST               'p'
              198  JUMP_BACK           168  'to 168'

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
            def frombuf(cls, buf, encoding, errors):
                """Construct a TarInfo object from a 512 byte bytes object.
        """
                if len(buf) == 0:
                    raise EmptyHeaderError('empty header')
                else:
                    if len(buf) != BLOCKSIZE:
                        raise TruncatedHeaderError('truncated header')
                    else:
                        if buf.count(NUL) == BLOCKSIZE:
                            raise EOFHeaderError('end of file header')
                        chksum = nti(buf[148:156])
                        if chksum not in calc_chksums(buf):
                            raise InvalidHeaderError('bad checksum')
                        obj = cls()
                        obj.name = nts(buf[0:100], encoding, errors)
                        obj.mode = nti(buf[100:108])
                        obj.uid = nti(buf[108:116])
                        obj.gid = nti(buf[116:124])
                        obj.size = nti(buf[124:136])
                        obj.mtime = nti(buf[136:148])
                        obj.chksum = chksum
                        obj.type = buf[156:157]
                        obj.linkname = nts(buf[157:257], encoding, errors)
                        obj.uname = nts(buf[265:297], encoding, errors)
                        obj.gname = nts(buf[297:329], encoding, errors)
                        obj.devmajor = nti(buf[329:337])
                        obj.devminor = nti(buf[337:345])
                        prefix = nts(buf[345:500], encoding, errors)
                        if obj.type == AREGTYPE and obj.name.endswith('/'):
                            obj.type = DIRTYPE
                    if obj.type == GNUTYPE_SPARSE:
                        pos = 386
                        structs = []
                        for i in range(4):
                            try:
                                offset = nti(buf[pos:pos + 12])
                                numbytes = nti(buf[pos + 12:pos + 24])
                            except ValueError:
                                break
                            else:
                                structs.append((offset, numbytes))
                                pos += 24
                        else:
                            isextended = bool(buf[482])
                            origsize = nti(buf[483:495])
                            obj._sparse_structs = (structs, isextended, origsize)

                    if obj.isdir():
                        obj.name = obj.name.rstrip('/')
                    if prefix and obj.type not in GNU_TYPES:
                        obj.name = prefix + '/' + obj.name
                return obj

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
                if self.isreg() or self.type not in SUPPORTED_TYPES:
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
                    else:
                        if self.type == GNUTYPE_LONGLINK:
                            next.linkname = nts(buf, tarfile.encoding, tarfile.errors)
                    return next

            def _proc_sparse(self, tarfile):
                """Process a GNU sparse header plus extra headers.
        """
                structs, isextended, origsize = self._sparse_structs
                del self._sparse_structs
                while isextended:
                    buf = tarfile.fileobj.read(BLOCKSIZE)
                    pos = 0
                    for i in range(21):
                        try:
                            offset = nti(buf[pos:pos + 12])
                            numbytes = nti(buf[pos + 12:pos + 24])
                        except ValueError:
                            break
                        else:
                            if offset:
                                if numbytes:
                                    structs.append((offset, numbytes))
                            pos += 24
                    else:
                        isextended = bool(buf[504])

                self.sparse = structs
                self.offset_data = tarfile.fileobj.tell()
                tarfile.offset = self.offset_data + self._block(self.size)
                self.size = origsize
                return self

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
                else:
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
                        break
                    else:
                        length, keyword = match.groups()
                        length = int(length)
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

                if 'GNU.sparse.map' in pax_headers:
                    self._proc_gnusparse_01(next, pax_headers)
                else:
                    if 'GNU.sparse.size' in pax_headers:
                        self._proc_gnusparse_00(next, pax_headers, buf)
                    else:
                        if pax_headers.get('GNU.sparse.major') == '1':
                            if pax_headers.get('GNU.sparse.minor') == '0':
                                self._proc_gnusparse_10(next, pax_headers, tarfile)
                        if self.type in (XHDTYPE, SOLARIS_XHDTYPE):
                            next._apply_pax_info(pax_headers, tarfile.encoding, tarfile.errors)
                            next.offset = self.offset
                            if 'size' in pax_headers:
                                offset = next.offset_data
                                if next.isreg() or next.type not in SUPPORTED_TYPES:
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
                while len(sparse) < fields * 2:
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
                    elif keyword == 'GNU.sparse.size':
                        setattr(self, 'size', int(value))
                    elif keyword == 'GNU.sparse.realsize':
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
                        setattr(self, keyword, value)
                    self.pax_headers = pax_headers.copy()

            def _decode_pax_field--- This code section failed: ---

 L.1359         0  SETUP_FINALLY        16  'to 16'

 L.1360         2  LOAD_FAST                'value'
                4  LOAD_METHOD              decode
                6  LOAD_FAST                'encoding'
                8  LOAD_STR                 'strict'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1361        16  DUP_TOP          
               18  LOAD_GLOBAL              UnicodeDecodeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    46  'to 46'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1362        30  LOAD_FAST                'value'
               32  LOAD_METHOD              decode
               34  LOAD_FAST                'fallback_encoding'
               36  LOAD_FAST                'fallback_errors'
               38  CALL_METHOD_2         2  ''
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
             46_0  COME_FROM            22  '22'
               46  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26

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

            def __init__--- This code section failed: ---

 L.1451         0  LOAD_STR                 'rb'
                2  LOAD_STR                 'r+b'
                4  LOAD_STR                 'wb'
                6  LOAD_STR                 'xb'
                8  LOAD_CONST               ('r', 'a', 'w', 'x')
               10  BUILD_CONST_KEY_MAP_4     4 
               12  STORE_FAST               'modes'

 L.1452        14  LOAD_FAST                'mode'
               16  LOAD_FAST                'modes'
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.1453        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 "mode must be 'r', 'a', 'w' or 'x'"
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.1454        30  LOAD_FAST                'mode'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               mode

 L.1455        36  LOAD_FAST                'modes'
               38  LOAD_FAST                'mode'
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _mode

 L.1457        46  LOAD_FAST                'fileobj'
               48  POP_JUMP_IF_TRUE    104  'to 104'

 L.1458        50  LOAD_FAST                'self'
               52  LOAD_ATTR                mode
               54  LOAD_STR                 'a'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    84  'to 84'
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              exists
               66  LOAD_FAST                'name'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_TRUE     84  'to 84'

 L.1460        72  LOAD_STR                 'w'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               mode

 L.1461        78  LOAD_STR                 'wb'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _mode
             84_0  COME_FROM            70  '70'
             84_1  COME_FROM            58  '58'

 L.1462        84  LOAD_GLOBAL              bltn_open
               86  LOAD_FAST                'name'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _mode
               92  CALL_FUNCTION_2       2  ''
               94  STORE_FAST               'fileobj'

 L.1463        96  LOAD_CONST               False
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _extfileobj
              102  JUMP_FORWARD        168  'to 168'
            104_0  COME_FROM            48  '48'

 L.1465       104  LOAD_FAST                'name'
              106  LOAD_CONST               None
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   144  'to 144'
              112  LOAD_GLOBAL              hasattr
              114  LOAD_FAST                'fileobj'
              116  LOAD_STR                 'name'
              118  CALL_FUNCTION_2       2  ''
              120  POP_JUMP_IF_FALSE   144  'to 144'

 L.1466       122  LOAD_GLOBAL              isinstance
              124  LOAD_FAST                'fileobj'
              126  LOAD_ATTR                name
              128  LOAD_GLOBAL              str
              130  LOAD_GLOBAL              bytes
              132  BUILD_TUPLE_2         2 
              134  CALL_FUNCTION_2       2  ''

 L.1465       136  POP_JUMP_IF_FALSE   144  'to 144'

 L.1467       138  LOAD_FAST                'fileobj'
              140  LOAD_ATTR                name
              142  STORE_FAST               'name'
            144_0  COME_FROM           136  '136'
            144_1  COME_FROM           120  '120'
            144_2  COME_FROM           110  '110'

 L.1468       144  LOAD_GLOBAL              hasattr
              146  LOAD_FAST                'fileobj'
              148  LOAD_STR                 'mode'
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L.1469       154  LOAD_FAST                'fileobj'
              156  LOAD_ATTR                mode
              158  LOAD_FAST                'self'
              160  STORE_ATTR               _mode
            162_0  COME_FROM           152  '152'

 L.1470       162  LOAD_CONST               True
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _extfileobj
            168_0  COME_FROM           102  '102'

 L.1471       168  LOAD_FAST                'name'
              170  POP_JUMP_IF_FALSE   184  'to 184'
              172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              abspath
              178  LOAD_FAST                'name'
              180  CALL_METHOD_1         1  ''
              182  JUMP_FORWARD        186  'to 186'
            184_0  COME_FROM           170  '170'
              184  LOAD_CONST               None
            186_0  COME_FROM           182  '182'
              186  LOAD_FAST                'self'
              188  STORE_ATTR               name

 L.1472       190  LOAD_FAST                'fileobj'
              192  LOAD_FAST                'self'
              194  STORE_ATTR               fileobj

 L.1475       196  LOAD_FAST                'format'
              198  LOAD_CONST               None
              200  COMPARE_OP               is-not
              202  POP_JUMP_IF_FALSE   210  'to 210'

 L.1476       204  LOAD_FAST                'format'
              206  LOAD_FAST                'self'
              208  STORE_ATTR               format
            210_0  COME_FROM           202  '202'

 L.1477       210  LOAD_FAST                'tarinfo'
              212  LOAD_CONST               None
              214  COMPARE_OP               is-not
              216  POP_JUMP_IF_FALSE   224  'to 224'

 L.1478       218  LOAD_FAST                'tarinfo'
              220  LOAD_FAST                'self'
              222  STORE_ATTR               tarinfo
            224_0  COME_FROM           216  '216'

 L.1479       224  LOAD_FAST                'dereference'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE   238  'to 238'

 L.1480       232  LOAD_FAST                'dereference'
              234  LOAD_FAST                'self'
              236  STORE_ATTR               dereference
            238_0  COME_FROM           230  '230'

 L.1481       238  LOAD_FAST                'ignore_zeros'
              240  LOAD_CONST               None
              242  COMPARE_OP               is-not
              244  POP_JUMP_IF_FALSE   252  'to 252'

 L.1482       246  LOAD_FAST                'ignore_zeros'
              248  LOAD_FAST                'self'
              250  STORE_ATTR               ignore_zeros
            252_0  COME_FROM           244  '244'

 L.1483       252  LOAD_FAST                'encoding'
              254  LOAD_CONST               None
              256  COMPARE_OP               is-not
          258_260  POP_JUMP_IF_FALSE   268  'to 268'

 L.1484       262  LOAD_FAST                'encoding'
              264  LOAD_FAST                'self'
              266  STORE_ATTR               encoding
            268_0  COME_FROM           258  '258'

 L.1485       268  LOAD_FAST                'errors'
              270  LOAD_FAST                'self'
              272  STORE_ATTR               errors

 L.1487       274  LOAD_FAST                'pax_headers'
              276  LOAD_CONST               None
              278  COMPARE_OP               is-not
          280_282  POP_JUMP_IF_FALSE   304  'to 304'
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                format
              288  LOAD_GLOBAL              PAX_FORMAT
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   304  'to 304'

 L.1488       296  LOAD_FAST                'pax_headers'
              298  LOAD_FAST                'self'
              300  STORE_ATTR               pax_headers
              302  JUMP_FORWARD        310  'to 310'
            304_0  COME_FROM           292  '292'
            304_1  COME_FROM           280  '280'

 L.1490       304  BUILD_MAP_0           0 
              306  LOAD_FAST                'self'
              308  STORE_ATTR               pax_headers
            310_0  COME_FROM           302  '302'

 L.1492       310  LOAD_FAST                'debug'
              312  LOAD_CONST               None
              314  COMPARE_OP               is-not
          316_318  POP_JUMP_IF_FALSE   326  'to 326'

 L.1493       320  LOAD_FAST                'debug'
              322  LOAD_FAST                'self'
              324  STORE_ATTR               debug
            326_0  COME_FROM           316  '316'

 L.1494       326  LOAD_FAST                'errorlevel'
              328  LOAD_CONST               None
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_FALSE   342  'to 342'

 L.1495       336  LOAD_FAST                'errorlevel'
              338  LOAD_FAST                'self'
              340  STORE_ATTR               errorlevel
            342_0  COME_FROM           332  '332'

 L.1498       342  LOAD_FAST                'copybufsize'
              344  LOAD_FAST                'self'
              346  STORE_ATTR               copybufsize

 L.1499       348  LOAD_CONST               False
              350  LOAD_FAST                'self'
              352  STORE_ATTR               closed

 L.1500       354  BUILD_LIST_0          0 
              356  LOAD_FAST                'self'
              358  STORE_ATTR               members

 L.1501       360  LOAD_CONST               False
              362  LOAD_FAST                'self'
              364  STORE_ATTR               _loaded

 L.1502       366  LOAD_FAST                'self'
              368  LOAD_ATTR                fileobj
              370  LOAD_METHOD              tell
              372  CALL_METHOD_0         0  ''
              374  LOAD_FAST                'self'
              376  STORE_ATTR               offset

 L.1504       378  BUILD_MAP_0           0 
              380  LOAD_FAST                'self'
              382  STORE_ATTR               inodes

 L.1507       384  SETUP_FINALLY       640  'to 640'

 L.1508       386  LOAD_FAST                'self'
              388  LOAD_ATTR                mode
              390  LOAD_STR                 'r'
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   414  'to 414'

 L.1509       398  LOAD_CONST               None
              400  LOAD_FAST                'self'
              402  STORE_ATTR               firstmember

 L.1510       404  LOAD_FAST                'self'
              406  LOAD_METHOD              next
              408  CALL_METHOD_0         0  ''
              410  LOAD_FAST                'self'
              412  STORE_ATTR               firstmember
            414_0  COME_FROM           394  '394'

 L.1512       414  LOAD_FAST                'self'
              416  LOAD_ATTR                mode
              418  LOAD_STR                 'a'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   562  'to 562'

 L.1516       426  LOAD_FAST                'self'
              428  LOAD_ATTR                fileobj
              430  LOAD_METHOD              seek
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                offset
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          

 L.1517       440  SETUP_FINALLY       470  'to 470'

 L.1518       442  LOAD_FAST                'self'
              444  LOAD_ATTR                tarinfo
              446  LOAD_METHOD              fromtarfile
              448  LOAD_FAST                'self'
              450  CALL_METHOD_1         1  ''
              452  STORE_FAST               'tarinfo'

 L.1519       454  LOAD_FAST                'self'
              456  LOAD_ATTR                members
              458  LOAD_METHOD              append
              460  LOAD_FAST                'tarinfo'
              462  CALL_METHOD_1         1  ''
              464  POP_TOP          
              466  POP_BLOCK        
              468  JUMP_BACK           426  'to 426'
            470_0  COME_FROM_FINALLY   440  '440'

 L.1520       470  DUP_TOP          
              472  LOAD_GLOBAL              EOFHeaderError
              474  COMPARE_OP               exception-match
          476_478  POP_JUMP_IF_FALSE   510  'to 510'
              480  POP_TOP          
              482  POP_TOP          
              484  POP_TOP          

 L.1521       486  LOAD_FAST                'self'
              488  LOAD_ATTR                fileobj
              490  LOAD_METHOD              seek
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                offset
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          

 L.1522       500  POP_EXCEPT       
          502_504  JUMP_ABSOLUTE       562  'to 562'
              506  POP_EXCEPT       
              508  JUMP_BACK           426  'to 426'
            510_0  COME_FROM           476  '476'

 L.1523       510  DUP_TOP          
              512  LOAD_GLOBAL              HeaderError
              514  COMPARE_OP               exception-match
          516_518  POP_JUMP_IF_FALSE   556  'to 556'
              520  POP_TOP          
              522  STORE_FAST               'e'
              524  POP_TOP          
              526  SETUP_FINALLY       544  'to 544'

 L.1524       528  LOAD_GLOBAL              ReadError
              530  LOAD_GLOBAL              str
              532  LOAD_FAST                'e'
              534  CALL_FUNCTION_1       1  ''
              536  CALL_FUNCTION_1       1  ''
              538  RAISE_VARARGS_1       1  'exception instance'
              540  POP_BLOCK        
              542  BEGIN_FINALLY    
            544_0  COME_FROM_FINALLY   526  '526'
              544  LOAD_CONST               None
              546  STORE_FAST               'e'
              548  DELETE_FAST              'e'
              550  END_FINALLY      
              552  POP_EXCEPT       
              554  JUMP_BACK           426  'to 426'
            556_0  COME_FROM           516  '516'
              556  END_FINALLY      
          558_560  JUMP_BACK           426  'to 426'
            562_0  COME_FROM           422  '422'

 L.1526       562  LOAD_FAST                'self'
              564  LOAD_ATTR                mode
              566  LOAD_CONST               ('a', 'w', 'x')
              568  COMPARE_OP               in
          570_572  POP_JUMP_IF_FALSE   636  'to 636'

 L.1527       574  LOAD_CONST               True
              576  LOAD_FAST                'self'
              578  STORE_ATTR               _loaded

 L.1529       580  LOAD_FAST                'self'
              582  LOAD_ATTR                pax_headers
          584_586  POP_JUMP_IF_FALSE   636  'to 636'

 L.1530       588  LOAD_FAST                'self'
              590  LOAD_ATTR                tarinfo
              592  LOAD_METHOD              create_pax_global_header
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                pax_headers
              598  LOAD_METHOD              copy
              600  CALL_METHOD_0         0  ''
              602  CALL_METHOD_1         1  ''
              604  STORE_FAST               'buf'

 L.1531       606  LOAD_FAST                'self'
              608  LOAD_ATTR                fileobj
              610  LOAD_METHOD              write
              612  LOAD_FAST                'buf'
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          

 L.1532       618  LOAD_FAST                'self'
              620  DUP_TOP          
              622  LOAD_ATTR                offset
              624  LOAD_GLOBAL              len
              626  LOAD_FAST                'buf'
              628  CALL_FUNCTION_1       1  ''
              630  INPLACE_ADD      
              632  ROT_TWO          
              634  STORE_ATTR               offset
            636_0  COME_FROM           584  '584'
            636_1  COME_FROM           570  '570'
              636  POP_BLOCK        
              638  JUMP_FORWARD        678  'to 678'
            640_0  COME_FROM_FINALLY   384  '384'

 L.1533       640  POP_TOP          
              642  POP_TOP          
              644  POP_TOP          

 L.1534       646  LOAD_FAST                'self'
              648  LOAD_ATTR                _extfileobj
          650_652  POP_JUMP_IF_TRUE    664  'to 664'

 L.1535       654  LOAD_FAST                'self'
              656  LOAD_ATTR                fileobj
              658  LOAD_METHOD              close
              660  CALL_METHOD_0         0  ''
              662  POP_TOP          
            664_0  COME_FROM           650  '650'

 L.1536       664  LOAD_CONST               True
              666  LOAD_FAST                'self'
              668  STORE_ATTR               closed

 L.1537       670  RAISE_VARARGS_0       0  'reraise'
              672  POP_EXCEPT       
              674  JUMP_FORWARD        678  'to 678'
              676  END_FINALLY      
            678_0  COME_FROM           674  '674'
            678_1  COME_FROM           638  '638'

Parse error at or near `POP_EXCEPT' instruction at offset 506

            @classmethod
            def open--- This code section failed: ---

 L.1587         0  LOAD_FAST                'name'
                2  POP_JUMP_IF_TRUE     16  'to 16'
                4  LOAD_FAST                'fileobj'
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.1588         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'nothing to open'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'
             16_1  COME_FROM             2  '2'

 L.1590        16  LOAD_FAST                'mode'
               18  LOAD_CONST               ('r', 'r:*')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE   170  'to 170'

 L.1592        24  LOAD_CLOSURE             'cls'
               26  BUILD_TUPLE_1         1 
               28  LOAD_CODE                <code_object not_compressed>
               30  LOAD_STR                 'TarFile.open.<locals>.not_compressed'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'not_compressed'

 L.1594        36  LOAD_GLOBAL              sorted
               38  LOAD_DEREF               'cls'
               40  LOAD_ATTR                OPEN_METH
               42  LOAD_FAST                'not_compressed'
               44  LOAD_CONST               ('key',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  GET_ITER         
               50  FOR_ITER            158  'to 158'
               52  STORE_FAST               'comptype'

 L.1595        54  LOAD_GLOBAL              getattr
               56  LOAD_DEREF               'cls'
               58  LOAD_DEREF               'cls'
               60  LOAD_ATTR                OPEN_METH
               62  LOAD_FAST                'comptype'
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'func'

 L.1596        70  LOAD_FAST                'fileobj'
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.1597        78  LOAD_FAST                'fileobj'
               80  LOAD_METHOD              tell
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'saved_pos'
             86_0  COME_FROM            76  '76'

 L.1598        86  SETUP_FINALLY       110  'to 110'

 L.1599        88  LOAD_FAST                'func'
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

 L.1600       110  DUP_TOP          
              112  LOAD_GLOBAL              ReadError
              114  LOAD_GLOBAL              CompressionError
              116  BUILD_TUPLE_2         2 
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   154  'to 154'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.1601       128  LOAD_FAST                'fileobj'
              130  LOAD_CONST               None
              132  COMPARE_OP               is-not
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L.1602       136  LOAD_FAST                'fileobj'
              138  LOAD_METHOD              seek
              140  LOAD_FAST                'saved_pos'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           134  '134'

 L.1603       146  POP_EXCEPT       
              148  JUMP_BACK            50  'to 50'
              150  POP_EXCEPT       
              152  JUMP_BACK            50  'to 50'
            154_0  COME_FROM           120  '120'
              154  END_FINALLY      
              156  JUMP_BACK            50  'to 50'

 L.1604       158  LOAD_GLOBAL              ReadError
              160  LOAD_STR                 'file could not be opened successfully'
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
          166_168  JUMP_FORWARD        430  'to 430'
            170_0  COME_FROM            22  '22'

 L.1606       170  LOAD_STR                 ':'
              172  LOAD_FAST                'mode'
              174  COMPARE_OP               in
          176_178  POP_JUMP_IF_FALSE   268  'to 268'

 L.1607       180  LOAD_FAST                'mode'
              182  LOAD_METHOD              split
              184  LOAD_STR                 ':'
              186  LOAD_CONST               1
              188  CALL_METHOD_2         2  ''
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'filemode'
              194  STORE_FAST               'comptype'

 L.1608       196  LOAD_FAST                'filemode'
              198  JUMP_IF_TRUE_OR_POP   202  'to 202'
              200  LOAD_STR                 'r'
            202_0  COME_FROM           198  '198'
              202  STORE_FAST               'filemode'

 L.1609       204  LOAD_FAST                'comptype'
              206  JUMP_IF_TRUE_OR_POP   210  'to 210'
              208  LOAD_STR                 'tar'
            210_0  COME_FROM           206  '206'
              210  STORE_FAST               'comptype'

 L.1613       212  LOAD_FAST                'comptype'
              214  LOAD_DEREF               'cls'
              216  LOAD_ATTR                OPEN_METH
              218  COMPARE_OP               in
              220  POP_JUMP_IF_FALSE   240  'to 240'

 L.1614       222  LOAD_GLOBAL              getattr
              224  LOAD_DEREF               'cls'
              226  LOAD_DEREF               'cls'
              228  LOAD_ATTR                OPEN_METH
              230  LOAD_FAST                'comptype'
              232  BINARY_SUBSCR    
              234  CALL_FUNCTION_2       2  ''
              236  STORE_FAST               'func'
              238  JUMP_FORWARD        252  'to 252'
            240_0  COME_FROM           220  '220'

 L.1616       240  LOAD_GLOBAL              CompressionError
              242  LOAD_STR                 'unknown compression type %r'
              244  LOAD_FAST                'comptype'
              246  BINARY_MODULO    
              248  CALL_FUNCTION_1       1  ''
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           238  '238'

 L.1617       252  LOAD_FAST                'func'
              254  LOAD_FAST                'name'
              256  LOAD_FAST                'filemode'
              258  LOAD_FAST                'fileobj'
              260  BUILD_TUPLE_3         3 
              262  LOAD_FAST                'kwargs'
              264  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              266  RETURN_VALUE     
            268_0  COME_FROM           176  '176'

 L.1619       268  LOAD_STR                 '|'
              270  LOAD_FAST                'mode'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   402  'to 402'

 L.1620       278  LOAD_FAST                'mode'
              280  LOAD_METHOD              split
              282  LOAD_STR                 '|'
              284  LOAD_CONST               1
              286  CALL_METHOD_2         2  ''
              288  UNPACK_SEQUENCE_2     2 
              290  STORE_FAST               'filemode'
              292  STORE_FAST               'comptype'

 L.1621       294  LOAD_FAST                'filemode'
          296_298  JUMP_IF_TRUE_OR_POP   302  'to 302'
              300  LOAD_STR                 'r'
            302_0  COME_FROM           296  '296'
              302  STORE_FAST               'filemode'

 L.1622       304  LOAD_FAST                'comptype'
          306_308  JUMP_IF_TRUE_OR_POP   312  'to 312'
              310  LOAD_STR                 'tar'
            312_0  COME_FROM           306  '306'
              312  STORE_FAST               'comptype'

 L.1624       314  LOAD_FAST                'filemode'
              316  LOAD_CONST               ('r', 'w')
              318  COMPARE_OP               not-in
          320_322  POP_JUMP_IF_FALSE   332  'to 332'

 L.1625       324  LOAD_GLOBAL              ValueError
              326  LOAD_STR                 "mode must be 'r' or 'w'"
              328  CALL_FUNCTION_1       1  ''
              330  RAISE_VARARGS_1       1  'exception instance'
            332_0  COME_FROM           320  '320'

 L.1627       332  LOAD_GLOBAL              _Stream
              334  LOAD_FAST                'name'
              336  LOAD_FAST                'filemode'
              338  LOAD_FAST                'comptype'
              340  LOAD_FAST                'fileobj'
              342  LOAD_FAST                'bufsize'
              344  CALL_FUNCTION_5       5  ''
              346  STORE_FAST               'stream'

 L.1628       348  SETUP_FINALLY       370  'to 370'

 L.1629       350  LOAD_DEREF               'cls'
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

 L.1630       370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L.1631       376  LOAD_FAST                'stream'
              378  LOAD_METHOD              close
              380  CALL_METHOD_0         0  ''
              382  POP_TOP          

 L.1632       384  RAISE_VARARGS_0       0  'reraise'
              386  POP_EXCEPT       
              388  JUMP_FORWARD        392  'to 392'
              390  END_FINALLY      
            392_0  COME_FROM           388  '388'
            392_1  COME_FROM           368  '368'

 L.1633       392  LOAD_CONST               False
              394  LOAD_FAST                't'
              396  STORE_ATTR               _extfileobj

 L.1634       398  LOAD_FAST                't'
              400  RETURN_VALUE     
            402_0  COME_FROM           274  '274'

 L.1636       402  LOAD_FAST                'mode'
              404  LOAD_CONST               ('a', 'w', 'x')
              406  COMPARE_OP               in
          408_410  POP_JUMP_IF_FALSE   430  'to 430'

 L.1637       412  LOAD_DEREF               'cls'
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

 L.1639       430  LOAD_GLOBAL              ValueError
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
                else:
                    if arcname is None:
                        arcname = name
                    else:
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
                        if not self.dereference:
                            if statres.st_nlink > 1 and inode in self.inodes and arcname != self.inodes[inode]:
                                type = LNKTYPE
                                linkname = self.inodes[inode]
                            else:
                                type = REGTYPE
                                if inode[0]:
                                    self.inodes[inode] = arcname
                        else:
                            if stat.S_ISDIR(stmd):
                                type = DIRTYPE
                            else:
                                if stat.S_ISFIFO(stmd):
                                    type = FIFOTYPE
                                else:
                                    if stat.S_ISLNK(stmd):
                                        type = SYMTYPE
                                        linkname = os.readlink(name)
                                    else:
                                        if stat.S_ISCHR(stmd):
                                            type = CHRTYPE
                                        else:
                                            if stat.S_ISBLK(stmd):
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
                elif self.name is not None:
                    if os.path.abspath(name) == self.name:
                        self._dbg(2, 'tarfile: Skipped %r' % name)
                        return
                    else:
                        self._dbg(1, name)
                        tarinfo = self.gettarinfo(name, arcname)
                        if tarinfo is None:
                            self._dbg(1, 'tarfile: Unsupported type %r' % name)
                            return None
                        if filter is not None:
                            tarinfo = filter(tarinfo)
                            if tarinfo is None:
                                self._dbg(2, 'tarfile: Excluded %r' % name)
                                return None
                    if tarinfo.isreg():
                        with bltn_open(name, 'rb') as (f):
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

            def extractall(self, path='.', members=None, *, numeric_owner=False):
                """Extract all members from the archive to the current working
           directory and set owner, modification time and permissions on
           directories afterwards. `path' specifies a different directory
           to extract to. `members' is optional and must be a subset of the
           list returned by getmembers(). If `numeric_owner` is True, only
           the numbers for user/group names are used and not the names.
        """
                directories = []
                if members is None:
                    members = self
                for tarinfo in members:
                    if tarinfo.isdir():
                        directories.append(tarinfo)
                        tarinfo = copy.copy(tarinfo)
                        tarinfo.mode = 448
                    self.extract(tarinfo, path, set_attrs=(not tarinfo.isdir()), numeric_owner=numeric_owner)
                else:
                    directories.sort(key=(lambda a: a.name))
                    directories.reverse()
                    for tarinfo in directories:
                        dirpath = os.path.join(path, tarinfo.name)
                        try:
                            self.chown(tarinfo, dirpath, numeric_owner=numeric_owner)
                            self.utime(tarinfo, dirpath)
                            self.chmod(tarinfo, dirpath)
                        except ExtractError as e:
                            try:
                                if self.errorlevel > 1:
                                    raise
                                else:
                                    self._dbg(1, 'tarfile: %s' % e)
                            finally:
                                e = None
                                del e

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
                        else:
                            if e.filename is None:
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
                if not tarinfo.isreg():
                    if tarinfo.type not in SUPPORTED_TYPES:
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
                elif tarinfo.islnk() or tarinfo.issym():
                    self._dbg(1, '%s -> %s' % (tarinfo.name, tarinfo.linkname))
                else:
                    self._dbg(1, tarinfo.name)
                if tarinfo.isreg():
                    self.makefile(tarinfo, targetpath)
                else:
                    if tarinfo.isdir():
                        self.makedir(tarinfo, targetpath)
                    else:
                        if tarinfo.isfifo():
                            self.makefifo(tarinfo, targetpath)
                        else:
                            if tarinfo.ischr() or tarinfo.isblk():
                                self.makedev(tarinfo, targetpath)
                            else:
                                if tarinfo.islnk() or tarinfo.issym():
                                    self.makelink(tarinfo, targetpath)
                                else:
                                    if tarinfo.type not in SUPPORTED_TYPES:
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
                with bltn_open(targetpath, 'wb') as (target):
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
                if hasattr(os, 'mknod'):
                    raise hasattr(os, 'makedev') or ExtractError('special devices not supported by system')
                else:
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
                    else:
                        if os.path.exists(tarinfo._link_target):
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
                if hasattr(os, 'geteuid'):
                    if os.geteuid() == 0:
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

 L.2295         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check
                4  LOAD_STR                 'ra'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.2296        10  LOAD_FAST                'self'
               12  LOAD_ATTR                firstmember
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L.2297        20  LOAD_FAST                'self'
               22  LOAD_ATTR                firstmember
               24  STORE_FAST               'm'

 L.2298        26  LOAD_CONST               None
               28  LOAD_FAST                'self'
               30  STORE_ATTR               firstmember

 L.2299        32  LOAD_FAST                'm'
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'

 L.2302        36  LOAD_FAST                'self'
               38  LOAD_ATTR                offset
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                fileobj
               44  LOAD_METHOD              tell
               46  CALL_METHOD_0         0  ''
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    90  'to 90'

 L.2303        52  LOAD_FAST                'self'
               54  LOAD_ATTR                fileobj
               56  LOAD_METHOD              seek
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                offset
               62  LOAD_CONST               1
               64  BINARY_SUBTRACT  
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.2304        70  LOAD_FAST                'self'
               72  LOAD_ATTR                fileobj
               74  LOAD_METHOD              read
               76  LOAD_CONST               1
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_TRUE     90  'to 90'

 L.2305        82  LOAD_GLOBAL              ReadError
               84  LOAD_STR                 'unexpected end of data'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            50  '50'

 L.2308        90  LOAD_CONST               None
               92  STORE_FAST               'tarinfo'

 L.2310        94  SETUP_FINALLY       114  'to 114'

 L.2311        96  LOAD_FAST                'self'
               98  LOAD_ATTR                tarinfo
              100  LOAD_METHOD              fromtarfile
              102  LOAD_FAST                'self'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'tarinfo'
              108  POP_BLOCK        
          110_112  BREAK_LOOP          462  'to 462'
            114_0  COME_FROM_FINALLY    94  '94'

 L.2312       114  DUP_TOP          
              116  LOAD_GLOBAL              EOFHeaderError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   198  'to 198'
              122  POP_TOP          
              124  STORE_FAST               'e'
              126  POP_TOP          
              128  SETUP_FINALLY       184  'to 184'

 L.2313       130  LOAD_FAST                'self'
              132  LOAD_ATTR                ignore_zeros
              134  POP_JUMP_IF_FALSE   180  'to 180'

 L.2314       136  LOAD_FAST                'self'
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

 L.2315       158  LOAD_FAST                'self'
              160  DUP_TOP          
              162  LOAD_ATTR                offset
              164  LOAD_GLOBAL              BLOCKSIZE
              166  INPLACE_ADD      
              168  ROT_TWO          
              170  STORE_ATTR               offset

 L.2316       172  POP_BLOCK        
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
          194_196  BREAK_LOOP          462  'to 462'
            198_0  COME_FROM           120  '120'

 L.2317       198  DUP_TOP          
              200  LOAD_GLOBAL              InvalidHeaderError
              202  COMPARE_OP               exception-match
          204_206  POP_JUMP_IF_FALSE   310  'to 310'
              208  POP_TOP          
              210  STORE_FAST               'e'
              212  POP_TOP          
              214  SETUP_FINALLY       298  'to 298'

 L.2318       216  LOAD_FAST                'self'
              218  LOAD_ATTR                ignore_zeros
          220_222  POP_JUMP_IF_FALSE   270  'to 270'

 L.2319       224  LOAD_FAST                'self'
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

 L.2320       246  LOAD_FAST                'self'
              248  DUP_TOP          
              250  LOAD_ATTR                offset
              252  LOAD_GLOBAL              BLOCKSIZE
              254  INPLACE_ADD      
              256  ROT_TWO          
              258  STORE_ATTR               offset

 L.2321       260  POP_BLOCK        
              262  POP_EXCEPT       
              264  CALL_FINALLY        298  'to 298'
              266  JUMP_BACK            94  'to 94'
              268  JUMP_FORWARD        294  'to 294'
            270_0  COME_FROM           220  '220'

 L.2322       270  LOAD_FAST                'self'
              272  LOAD_ATTR                offset
              274  LOAD_CONST               0
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   294  'to 294'

 L.2323       282  LOAD_GLOBAL              ReadError
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
              308  BREAK_LOOP          462  'to 462'
            310_0  COME_FROM           204  '204'

 L.2324       310  DUP_TOP          
              312  LOAD_GLOBAL              EmptyHeaderError
              314  COMPARE_OP               exception-match
          316_318  POP_JUMP_IF_FALSE   350  'to 350'
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L.2325       326  LOAD_FAST                'self'
              328  LOAD_ATTR                offset
              330  LOAD_CONST               0
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   346  'to 346'

 L.2326       338  LOAD_GLOBAL              ReadError
              340  LOAD_STR                 'empty file'
              342  CALL_FUNCTION_1       1  ''
              344  RAISE_VARARGS_1       1  'exception instance'
            346_0  COME_FROM           334  '334'
              346  POP_EXCEPT       
              348  BREAK_LOOP          462  'to 462'
            350_0  COME_FROM           316  '316'

 L.2327       350  DUP_TOP          
              352  LOAD_GLOBAL              TruncatedHeaderError
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   408  'to 408'
              360  POP_TOP          
              362  STORE_FAST               'e'
              364  POP_TOP          
              366  SETUP_FINALLY       396  'to 396'

 L.2328       368  LOAD_FAST                'self'
              370  LOAD_ATTR                offset
              372  LOAD_CONST               0
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   392  'to 392'

 L.2329       380  LOAD_GLOBAL              ReadError
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
              406  BREAK_LOOP          462  'to 462'
            408_0  COME_FROM           356  '356'

 L.2330       408  DUP_TOP          
              410  LOAD_GLOBAL              SubsequentHeaderError
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   454  'to 454'
              418  POP_TOP          
              420  STORE_FAST               'e'
              422  POP_TOP          
              424  SETUP_FINALLY       442  'to 442'

 L.2331       426  LOAD_GLOBAL              ReadError
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
              452  BREAK_LOOP          462  'to 462'
            454_0  COME_FROM           414  '414'
              454  END_FINALLY      

 L.2332   456_458  BREAK_LOOP          462  'to 462'
              460  JUMP_BACK            94  'to 94'

 L.2334       462  LOAD_FAST                'tarinfo'
              464  LOAD_CONST               None
              466  COMPARE_OP               is-not
          468_470  POP_JUMP_IF_FALSE   486  'to 486'

 L.2335       472  LOAD_FAST                'self'
              474  LOAD_ATTR                members
              476  LOAD_METHOD              append
              478  LOAD_FAST                'tarinfo'
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
              484  JUMP_FORWARD        492  'to 492'
            486_0  COME_FROM           468  '468'

 L.2337       486  LOAD_CONST               True
              488  LOAD_FAST                'self'
              490  STORE_ATTR               _loaded
            492_0  COME_FROM           484  '484'

 L.2339       492  LOAD_FAST                'tarinfo'
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

            def _load(self):
                """Read through the entire archive file and look for readable
           members.
        """
                while True:
                    tarinfo = self.next()
                    if tarinfo is None:
                        break

                self._loaded = True

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
                    (yield from self.members)
                    return
                index = 0
                if self.firstmember is not None:
                    tarinfo = self.next()
                    index += 1
                    (yield tarinfo)
                while True:
                    if index < len(self.members):
                        tarinfo = self.members[index]
                    else:
                        tarinfo = self._loaded or self.next()
                        if not tarinfo:
                            self._loaded = True
                            return
                        else:
                            return
                    index += 1
                    (yield tarinfo)

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

 L.2463         0  SETUP_FINALLY        24  'to 24'

 L.2464         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'name'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               't'

 L.2465        10  LOAD_FAST                't'
               12  LOAD_METHOD              close
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L.2466        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.2467        24  DUP_TOP          
               26  LOAD_GLOBAL              TarError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.2468        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 22


        open = TarFile.open

        def main--- This code section failed: ---

 L.2474         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              argparse
                6  STORE_FAST               'argparse'

 L.2476         8  LOAD_STR                 'A simple command-line interface for tarfile module.'
               10  STORE_FAST               'description'

 L.2477        12  LOAD_FAST                'argparse'
               14  LOAD_ATTR                ArgumentParser
               16  LOAD_FAST                'description'
               18  LOAD_CONST               ('description',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  STORE_FAST               'parser'

 L.2478        24  LOAD_FAST                'parser'
               26  LOAD_ATTR                add_argument
               28  LOAD_STR                 '-v'
               30  LOAD_STR                 '--verbose'
               32  LOAD_STR                 'store_true'
               34  LOAD_CONST               False

 L.2479        36  LOAD_STR                 'Verbose output'

 L.2478        38  LOAD_CONST               ('action', 'default', 'help')
               40  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               42  POP_TOP          

 L.2480        44  LOAD_FAST                'parser'
               46  LOAD_ATTR                add_mutually_exclusive_group
               48  LOAD_CONST               True
               50  LOAD_CONST               ('required',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  STORE_FAST               'group'

 L.2481        56  LOAD_FAST                'group'
               58  LOAD_ATTR                add_argument
               60  LOAD_STR                 '-l'
               62  LOAD_STR                 '--list'
               64  LOAD_STR                 '<tarfile>'

 L.2482        66  LOAD_STR                 'Show listing of a tarfile'

 L.2481        68  LOAD_CONST               ('metavar', 'help')
               70  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               72  POP_TOP          

 L.2483        74  LOAD_FAST                'group'
               76  LOAD_ATTR                add_argument
               78  LOAD_STR                 '-e'
               80  LOAD_STR                 '--extract'
               82  LOAD_STR                 '+'

 L.2484        84  LOAD_CONST               ('<tarfile>', '<output_dir>')

 L.2485        86  LOAD_STR                 'Extract tarfile into target dir'

 L.2483        88  LOAD_CONST               ('nargs', 'metavar', 'help')
               90  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               92  POP_TOP          

 L.2486        94  LOAD_FAST                'group'
               96  LOAD_ATTR                add_argument
               98  LOAD_STR                 '-c'
              100  LOAD_STR                 '--create'
              102  LOAD_STR                 '+'

 L.2487       104  LOAD_CONST               ('<name>', '<file>')

 L.2488       106  LOAD_STR                 'Create tarfile from sources'

 L.2486       108  LOAD_CONST               ('nargs', 'metavar', 'help')
              110  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              112  POP_TOP          

 L.2489       114  LOAD_FAST                'group'
              116  LOAD_ATTR                add_argument
              118  LOAD_STR                 '-t'
              120  LOAD_STR                 '--test'
              122  LOAD_STR                 '<tarfile>'

 L.2490       124  LOAD_STR                 'Test if a tarfile is valid'

 L.2489       126  LOAD_CONST               ('metavar', 'help')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  POP_TOP          

 L.2491       132  LOAD_FAST                'parser'
              134  LOAD_METHOD              parse_args
              136  CALL_METHOD_0         0  ''
              138  STORE_FAST               'args'

 L.2493       140  LOAD_FAST                'args'
              142  LOAD_ATTR                test
              144  LOAD_CONST               None
              146  COMPARE_OP               is-not
          148_150  POP_JUMP_IF_FALSE   258  'to 258'

 L.2494       152  LOAD_FAST                'args'
              154  LOAD_ATTR                test
              156  STORE_FAST               'src'

 L.2495       158  LOAD_GLOBAL              is_tarfile
              160  LOAD_FAST                'src'
              162  CALL_FUNCTION_1       1  ''
              164  POP_JUMP_IF_FALSE   236  'to 236'

 L.2496       166  LOAD_GLOBAL              open
              168  LOAD_FAST                'src'
              170  LOAD_STR                 'r'
              172  CALL_FUNCTION_2       2  ''
              174  SETUP_WITH          208  'to 208'
              176  STORE_FAST               'tar'

 L.2497       178  LOAD_FAST                'tar'
              180  LOAD_METHOD              getmembers
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          

 L.2498       186  LOAD_GLOBAL              print
              188  LOAD_FAST                'tar'
              190  LOAD_METHOD              getmembers
              192  CALL_METHOD_0         0  ''
              194  LOAD_GLOBAL              sys
              196  LOAD_ATTR                stderr
              198  LOAD_CONST               ('file',)
              200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              202  POP_TOP          
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM_WITH      174  '174'
              208  WITH_CLEANUP_START
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      

 L.2499       214  LOAD_FAST                'args'
              216  LOAD_ATTR                verbose
              218  POP_JUMP_IF_FALSE   254  'to 254'

 L.2500       220  LOAD_GLOBAL              print
              222  LOAD_STR                 '{!r} is a tar archive.'
              224  LOAD_METHOD              format
              226  LOAD_FAST                'src'
              228  CALL_METHOD_1         1  ''
              230  CALL_FUNCTION_1       1  ''
              232  POP_TOP          
              234  JUMP_FORWARD        718  'to 718'
            236_0  COME_FROM           164  '164'

 L.2502       236  LOAD_FAST                'parser'
              238  LOAD_METHOD              exit
              240  LOAD_CONST               1
              242  LOAD_STR                 '{!r} is not a tar archive.\n'
              244  LOAD_METHOD              format
              246  LOAD_FAST                'src'
              248  CALL_METHOD_1         1  ''
              250  CALL_METHOD_2         2  ''
              252  POP_TOP          
            254_0  COME_FROM           218  '218'
          254_256  JUMP_FORWARD        718  'to 718'
            258_0  COME_FROM           148  '148'

 L.2504       258  LOAD_FAST                'args'
              260  LOAD_ATTR                list
              262  LOAD_CONST               None
              264  COMPARE_OP               is-not
          266_268  POP_JUMP_IF_FALSE   348  'to 348'

 L.2505       270  LOAD_FAST                'args'
              272  LOAD_ATTR                list
              274  STORE_FAST               'src'

 L.2506       276  LOAD_GLOBAL              is_tarfile
              278  LOAD_FAST                'src'
              280  CALL_FUNCTION_1       1  ''
          282_284  POP_JUMP_IF_FALSE   326  'to 326'

 L.2507       286  LOAD_GLOBAL              TarFile
              288  LOAD_METHOD              open
              290  LOAD_FAST                'src'
              292  LOAD_STR                 'r:*'
              294  CALL_METHOD_2         2  ''
              296  SETUP_WITH          318  'to 318'
              298  STORE_FAST               'tf'

 L.2508       300  LOAD_FAST                'tf'
              302  LOAD_ATTR                list
              304  LOAD_FAST                'args'
              306  LOAD_ATTR                verbose
              308  LOAD_CONST               ('verbose',)
              310  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              312  POP_TOP          
              314  POP_BLOCK        
              316  BEGIN_FINALLY    
            318_0  COME_FROM_WITH      296  '296'
              318  WITH_CLEANUP_START
              320  WITH_CLEANUP_FINISH
              322  END_FINALLY      
              324  JUMP_FORWARD        718  'to 718'
            326_0  COME_FROM           282  '282'

 L.2510       326  LOAD_FAST                'parser'
              328  LOAD_METHOD              exit
              330  LOAD_CONST               1
              332  LOAD_STR                 '{!r} is not a tar archive.\n'
              334  LOAD_METHOD              format
              336  LOAD_FAST                'src'
              338  CALL_METHOD_1         1  ''
              340  CALL_METHOD_2         2  ''
              342  POP_TOP          
          344_346  JUMP_FORWARD        718  'to 718'
            348_0  COME_FROM           266  '266'

 L.2512       348  LOAD_FAST                'args'
              350  LOAD_ATTR                extract
              352  LOAD_CONST               None
              354  COMPARE_OP               is-not
          356_358  POP_JUMP_IF_FALSE   556  'to 556'

 L.2513       360  LOAD_GLOBAL              len
              362  LOAD_FAST                'args'
              364  LOAD_ATTR                extract
              366  CALL_FUNCTION_1       1  ''
              368  LOAD_CONST               1
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   394  'to 394'

 L.2514       376  LOAD_FAST                'args'
              378  LOAD_ATTR                extract
              380  LOAD_CONST               0
              382  BINARY_SUBSCR    
              384  STORE_FAST               'src'

 L.2515       386  LOAD_GLOBAL              os
              388  LOAD_ATTR                curdir
              390  STORE_FAST               'curdir'
              392  JUMP_FORWARD        438  'to 438'
            394_0  COME_FROM           372  '372'

 L.2516       394  LOAD_GLOBAL              len
              396  LOAD_FAST                'args'
              398  LOAD_ATTR                extract
              400  CALL_FUNCTION_1       1  ''
              402  LOAD_CONST               2
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   422  'to 422'

 L.2517       410  LOAD_FAST                'args'
              412  LOAD_ATTR                extract
              414  UNPACK_SEQUENCE_2     2 
              416  STORE_FAST               'src'
              418  STORE_FAST               'curdir'
              420  JUMP_FORWARD        438  'to 438'
            422_0  COME_FROM           406  '406'

 L.2519       422  LOAD_FAST                'parser'
              424  LOAD_METHOD              exit
              426  LOAD_CONST               1
              428  LOAD_FAST                'parser'
              430  LOAD_METHOD              format_help
              432  CALL_METHOD_0         0  ''
              434  CALL_METHOD_2         2  ''
              436  POP_TOP          
            438_0  COME_FROM           420  '420'
            438_1  COME_FROM           392  '392'

 L.2521       438  LOAD_GLOBAL              is_tarfile
              440  LOAD_FAST                'src'
              442  CALL_FUNCTION_1       1  ''
          444_446  POP_JUMP_IF_FALSE   536  'to 536'

 L.2522       448  LOAD_GLOBAL              TarFile
              450  LOAD_METHOD              open
              452  LOAD_FAST                'src'
              454  LOAD_STR                 'r:*'
              456  CALL_METHOD_2         2  ''
              458  SETUP_WITH          478  'to 478'
              460  STORE_FAST               'tf'

 L.2523       462  LOAD_FAST                'tf'
              464  LOAD_ATTR                extractall
              466  LOAD_FAST                'curdir'
              468  LOAD_CONST               ('path',)
              470  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              472  POP_TOP          
              474  POP_BLOCK        
              476  BEGIN_FINALLY    
            478_0  COME_FROM_WITH      458  '458'
              478  WITH_CLEANUP_START
              480  WITH_CLEANUP_FINISH
              482  END_FINALLY      

 L.2524       484  LOAD_FAST                'args'
              486  LOAD_ATTR                verbose
          488_490  POP_JUMP_IF_FALSE   554  'to 554'

 L.2525       492  LOAD_FAST                'curdir'
              494  LOAD_STR                 '.'
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   514  'to 514'

 L.2526       502  LOAD_STR                 '{!r} file is extracted.'
              504  LOAD_METHOD              format
              506  LOAD_FAST                'src'
              508  CALL_METHOD_1         1  ''
              510  STORE_FAST               'msg'
              512  JUMP_FORWARD        526  'to 526'
            514_0  COME_FROM           498  '498'

 L.2528       514  LOAD_STR                 '{!r} file is extracted into {!r} directory.'
              516  LOAD_METHOD              format

 L.2529       518  LOAD_FAST                'src'

 L.2529       520  LOAD_FAST                'curdir'

 L.2528       522  CALL_METHOD_2         2  ''
              524  STORE_FAST               'msg'
            526_0  COME_FROM           512  '512'

 L.2530       526  LOAD_GLOBAL              print
              528  LOAD_FAST                'msg'
              530  CALL_FUNCTION_1       1  ''
              532  POP_TOP          
              534  JUMP_FORWARD        554  'to 554'
            536_0  COME_FROM           444  '444'

 L.2532       536  LOAD_FAST                'parser'
              538  LOAD_METHOD              exit
              540  LOAD_CONST               1
              542  LOAD_STR                 '{!r} is not a tar archive.\n'
              544  LOAD_METHOD              format
              546  LOAD_FAST                'src'
              548  CALL_METHOD_1         1  ''
              550  CALL_METHOD_2         2  ''
              552  POP_TOP          
            554_0  COME_FROM           534  '534'
            554_1  COME_FROM           488  '488'
              554  JUMP_FORWARD        718  'to 718'
            556_0  COME_FROM           356  '356'

 L.2534       556  LOAD_FAST                'args'
              558  LOAD_ATTR                create
              560  LOAD_CONST               None
              562  COMPARE_OP               is-not
          564_566  POP_JUMP_IF_FALSE   718  'to 718'

 L.2535       568  LOAD_FAST                'args'
              570  LOAD_ATTR                create
              572  LOAD_METHOD              pop
              574  LOAD_CONST               0
              576  CALL_METHOD_1         1  ''
              578  STORE_FAST               'tar_name'

 L.2536       580  LOAD_GLOBAL              os
              582  LOAD_ATTR                path
              584  LOAD_METHOD              splitext
              586  LOAD_FAST                'tar_name'
              588  CALL_METHOD_1         1  ''
              590  UNPACK_SEQUENCE_2     2 
              592  STORE_FAST               '_'
              594  STORE_FAST               'ext'

 L.2539       596  LOAD_STR                 'gz'

 L.2540       598  LOAD_STR                 'gz'

 L.2542       600  LOAD_STR                 'xz'

 L.2543       602  LOAD_STR                 'xz'

 L.2545       604  LOAD_STR                 'bz2'

 L.2546       606  LOAD_STR                 'bz2'

 L.2547       608  LOAD_STR                 'bz2'

 L.2548       610  LOAD_STR                 'bz2'

 L.2537       612  LOAD_CONST               ('.gz', '.tgz', '.xz', '.txz', '.bz2', '.tbz', '.tbz2', '.tb2')
              614  BUILD_CONST_KEY_MAP_8     8 
              616  STORE_FAST               'compressions'

 L.2550       618  LOAD_FAST                'ext'
              620  LOAD_FAST                'compressions'
              622  COMPARE_OP               in
          624_626  POP_JUMP_IF_FALSE   640  'to 640'
              628  LOAD_STR                 'w:'
              630  LOAD_FAST                'compressions'
              632  LOAD_FAST                'ext'
              634  BINARY_SUBSCR    
              636  BINARY_ADD       
              638  JUMP_FORWARD        642  'to 642'
            640_0  COME_FROM           624  '624'
              640  LOAD_STR                 'w'
            642_0  COME_FROM           638  '638'
              642  STORE_FAST               'tar_mode'

 L.2551       644  LOAD_FAST                'args'
              646  LOAD_ATTR                create
              648  STORE_FAST               'tar_files'

 L.2553       650  LOAD_GLOBAL              TarFile
              652  LOAD_METHOD              open
              654  LOAD_FAST                'tar_name'
              656  LOAD_FAST                'tar_mode'
              658  CALL_METHOD_2         2  ''
              660  SETUP_WITH          690  'to 690'
              662  STORE_FAST               'tf'

 L.2554       664  LOAD_FAST                'tar_files'
              666  GET_ITER         
              668  FOR_ITER            686  'to 686'
              670  STORE_FAST               'file_name'

 L.2555       672  LOAD_FAST                'tf'
              674  LOAD_METHOD              add
              676  LOAD_FAST                'file_name'
              678  CALL_METHOD_1         1  ''
              680  POP_TOP          
          682_684  JUMP_BACK           668  'to 668'
              686  POP_BLOCK        
              688  BEGIN_FINALLY    
            690_0  COME_FROM_WITH      660  '660'
              690  WITH_CLEANUP_START
              692  WITH_CLEANUP_FINISH
              694  END_FINALLY      
            696_0  COME_FROM           324  '324'
            696_1  COME_FROM           234  '234'

 L.2557       696  LOAD_FAST                'args'
              698  LOAD_ATTR                verbose
          700_702  POP_JUMP_IF_FALSE   718  'to 718'

 L.2558       704  LOAD_GLOBAL              print
              706  LOAD_STR                 '{!r} file created.'
              708  LOAD_METHOD              format
              710  LOAD_FAST                'tar_name'
              712  CALL_METHOD_1         1  ''
              714  CALL_FUNCTION_1       1  ''
              716  POP_TOP          
            718_0  COME_FROM           700  '700'
            718_1  COME_FROM           564  '564'
            718_2  COME_FROM           554  '554'
            718_3  COME_FROM           344  '344'
            718_4  COME_FROM           254  '254'

Parse error at or near `COME_FROM' instruction at offset 718_3


        if __name__ == '__main__':
            main()