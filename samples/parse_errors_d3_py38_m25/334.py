# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: zipfile.py
"""
Read and write ZIP files.

XXX references to utf-8 need further investigation.
"""
import binascii, functools, importlib.util, io, itertools, os, posixpath, shutil, stat, struct, sys, threading, time, contextlib
from collections import OrderedDict
try:
    import zlib
    crc32 = zlib.crc32
except ImportError:
    zlib = None
    crc32 = binascii.crc32
else:
    try:
        import bz2
    except ImportError:
        bz2 = None
    else:
        try:
            import lzma
        except ImportError:
            lzma = None
        else:
            __all__ = [
             'BadZipFile', 'BadZipfile', 'error',
             'ZIP_STORED', 'ZIP_DEFLATED', 'ZIP_BZIP2', 'ZIP_LZMA',
             'is_zipfile', 'ZipInfo', 'ZipFile', 'PyZipFile', 'LargeZipFile']

            class BadZipFile(Exception):
                pass


            class LargeZipFile(Exception):
                __doc__ = '\n    Raised when writing a zipfile, the zipfile requires ZIP64 extensions\n    and those extensions are disabled.\n    '


            error = BadZipfile = BadZipFile
            ZIP64_LIMIT = 2147483647
            ZIP_FILECOUNT_LIMIT = 65535
            ZIP_MAX_COMMENT = 65535
            ZIP_STORED = 0
            ZIP_DEFLATED = 8
            ZIP_BZIP2 = 12
            ZIP_LZMA = 14
            DEFAULT_VERSION = 20
            ZIP64_VERSION = 45
            BZIP2_VERSION = 46
            LZMA_VERSION = 63
            MAX_EXTRACT_VERSION = 63
            structEndArchive = b'<4s4H2LH'
            stringEndArchive = b'PK\x05\x06'
            sizeEndCentDir = struct.calcsize(structEndArchive)
            _ECD_SIGNATURE = 0
            _ECD_DISK_NUMBER = 1
            _ECD_DISK_START = 2
            _ECD_ENTRIES_THIS_DISK = 3
            _ECD_ENTRIES_TOTAL = 4
            _ECD_SIZE = 5
            _ECD_OFFSET = 6
            _ECD_COMMENT_SIZE = 7
            _ECD_COMMENT = 8
            _ECD_LOCATION = 9
            structCentralDir = '<4s4B4HL2L5H2L'
            stringCentralDir = b'PK\x01\x02'
            sizeCentralDir = struct.calcsize(structCentralDir)
            _CD_SIGNATURE = 0
            _CD_CREATE_VERSION = 1
            _CD_CREATE_SYSTEM = 2
            _CD_EXTRACT_VERSION = 3
            _CD_EXTRACT_SYSTEM = 4
            _CD_FLAG_BITS = 5
            _CD_COMPRESS_TYPE = 6
            _CD_TIME = 7
            _CD_DATE = 8
            _CD_CRC = 9
            _CD_COMPRESSED_SIZE = 10
            _CD_UNCOMPRESSED_SIZE = 11
            _CD_FILENAME_LENGTH = 12
            _CD_EXTRA_FIELD_LENGTH = 13
            _CD_COMMENT_LENGTH = 14
            _CD_DISK_NUMBER_START = 15
            _CD_INTERNAL_FILE_ATTRIBUTES = 16
            _CD_EXTERNAL_FILE_ATTRIBUTES = 17
            _CD_LOCAL_HEADER_OFFSET = 18
            structFileHeader = '<4s2B4HL2L2H'
            stringFileHeader = b'PK\x03\x04'
            sizeFileHeader = struct.calcsize(structFileHeader)
            _FH_SIGNATURE = 0
            _FH_EXTRACT_VERSION = 1
            _FH_EXTRACT_SYSTEM = 2
            _FH_GENERAL_PURPOSE_FLAG_BITS = 3
            _FH_COMPRESSION_METHOD = 4
            _FH_LAST_MOD_TIME = 5
            _FH_LAST_MOD_DATE = 6
            _FH_CRC = 7
            _FH_COMPRESSED_SIZE = 8
            _FH_UNCOMPRESSED_SIZE = 9
            _FH_FILENAME_LENGTH = 10
            _FH_EXTRA_FIELD_LENGTH = 11
            structEndArchive64Locator = '<4sLQL'
            stringEndArchive64Locator = b'PK\x06\x07'
            sizeEndCentDir64Locator = struct.calcsize(structEndArchive64Locator)
            structEndArchive64 = '<4sQ2H2L4Q'
            stringEndArchive64 = b'PK\x06\x06'
            sizeEndCentDir64 = struct.calcsize(structEndArchive64)
            _CD64_SIGNATURE = 0
            _CD64_DIRECTORY_RECSIZE = 1
            _CD64_CREATE_VERSION = 2
            _CD64_EXTRACT_VERSION = 3
            _CD64_DISK_NUMBER = 4
            _CD64_DISK_NUMBER_START = 5
            _CD64_NUMBER_ENTRIES_THIS_DISK = 6
            _CD64_NUMBER_ENTRIES_TOTAL = 7
            _CD64_DIRECTORY_SIZE = 8
            _CD64_OFFSET_START_CENTDIR = 9
            _DD_SIGNATURE = 134695760
            _EXTRA_FIELD_STRUCT = struct.Struct('<HH')

            def _strip_extra(extra, xids):
                unpack = _EXTRA_FIELD_STRUCT.unpack
                modified = False
                buffer = []
                start = i = 0
                while True:
                    if i + 4 <= len(extra):
                        xid, xlen = unpack(extra[i:i + 4])
                        j = i + 4 + xlen
                        if xid in xids:
                            if i != start:
                                buffer.append(extra[start:i])
                            start = j
                            modified = True
                        i = j

                if not modified:
                    return extra
                return (b'').join(buffer)


            def _check_zipfile--- This code section failed: ---

 L. 191         0  SETUP_FINALLY        20  'to 20'

 L. 192         2  LOAD_GLOBAL              _EndRecData
                4  LOAD_FAST                'fp'
                6  CALL_FUNCTION_1       1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 193        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'
               16  POP_BLOCK        
               18  JUMP_FORWARD         40  'to 40'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 194        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    38  'to 38'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 195        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            26  '26'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM            18  '18'

 L. 196        40  LOAD_CONST               False
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 12


            def is_zipfile(filename):
                """Quickly see if a file is a ZIP file by checking the magic number.

    The filename argument may be a file or file-like object too.
    """
                result = False
                try:
                    if hasattr(filename, 'read'):
                        result = _check_zipfile(fp=filename)
                    else:
                        with open(filename, 'rb') as fp:
                            result = _check_zipfile(fp)
                except OSError:
                    pass
                else:
                    return result


            def _EndRecData64(fpin, offset, endrec):
                """
    Read the ZIP64 end-of-archive records and use that to update endrec
    """
                try:
                    fpin.seek(offset - sizeEndCentDir64Locator, 2)
                except OSError:
                    return endrec
                else:
                    data = fpin.read(sizeEndCentDir64Locator)
                    if len(data) != sizeEndCentDir64Locator:
                        return endrec
                    else:
                        sig, diskno, reloff, disks = struct.unpack(structEndArchive64Locator, data)
                        if sig != stringEndArchive64Locator:
                            return endrec
                        if diskno != 0 or (disks > 1):
                            raise BadZipFile('zipfiles that span multiple disks are not supported')
                        fpin.seek(offset - sizeEndCentDir64Locator - sizeEndCentDir64, 2)
                        data = fpin.read(sizeEndCentDir64)
                        if len(data) != sizeEndCentDir64:
                            return endrec
                        sig, sz, create_version, read_version, disk_num, disk_dir, dircount, dircount2, dirsize, diroffset = struct.unpack(structEndArchive64, data)
                        if sig != stringEndArchive64:
                            return endrec
                        endrec[_ECD_SIGNATURE] = sig
                        endrec[_ECD_DISK_NUMBER] = disk_num
                        endrec[_ECD_DISK_START] = disk_dir
                        endrec[_ECD_ENTRIES_THIS_DISK] = dircount
                        endrec[_ECD_ENTRIES_TOTAL] = dircount2
                        endrec[_ECD_SIZE] = dirsize
                        endrec[_ECD_OFFSET] = diroffset
                        return endrec


            def _EndRecData(fpin):
                """Return data from the "End of Central Directory" record, or None.

    The data is a list of the nine items in the ZIP "End of central dir"
    record followed by a tenth item, the file seek offset of this record."""
                fpin.seek(0, 2)
                filesize = fpin.tell()
                try:
                    fpin.seek(-sizeEndCentDir, 2)
                except OSError:
                    return
                else:
                    data = fpin.read()
                    if len(data) == sizeEndCentDir:
                        if data[0:4] == stringEndArchive:
                            if data[-2:] == b'\x00\x00':
                                endrec = struct.unpack(structEndArchive, data)
                                endrec = list(endrec)
                                endrec.append(b'')
                                endrec.append(filesize - sizeEndCentDir)
                                return _EndRecData64(fpin, -sizeEndCentDir, endrec)
                    maxCommentStart = max(filesize - 65536 - sizeEndCentDir, 0)
                    fpin.seek(maxCommentStart, 0)
                    data = fpin.read()
                    start = data.rfind(stringEndArchive)
                    if start >= 0:
                        recData = data[start:start + sizeEndCentDir]
                        if len(recData) != sizeEndCentDir:
                            return
                        endrec = list(struct.unpack(structEndArchive, recData))
                        commentSize = endrec[_ECD_COMMENT_SIZE]
                        comment = data[start + sizeEndCentDir:start + sizeEndCentDir + commentSize]
                        endrec.append(comment)
                        endrec.append(maxCommentStart + start)
                        return _EndRecData64(fpin, maxCommentStart + start - filesize, endrec)


            class ZipInfo(object):
                __doc__ = 'Class with attributes describing each file in the ZIP archive.'
                __slots__ = ('orig_filename', 'filename', 'date_time', 'compress_type',
                             '_compresslevel', 'comment', 'extra', 'create_system',
                             'create_version', 'extract_version', 'reserved', 'flag_bits',
                             'volume', 'internal_attr', 'external_attr', 'header_offset',
                             'CRC', 'compress_size', 'file_size', '_raw_time')

                def __init__(self, filename='NoName', date_time=(1980, 1, 1, 0, 0, 0)):
                    self.orig_filename = filename
                    null_byte = filename.find(chr(0))
                    if null_byte >= 0:
                        filename = filename[0:null_byte]
                    if os.sep != '/':
                        if os.sep in filename:
                            filename = filename.replace(os.sep, '/')
                    self.filename = filename
                    self.date_time = date_time
                    if date_time[0] < 1980:
                        raise ValueError('ZIP does not support timestamps before 1980')
                    self.compress_type = ZIP_STORED
                    self._compresslevel = None
                    self.comment = b''
                    self.extra = b''
                    if sys.platform == 'win32':
                        self.create_system = 0
                    else:
                        self.create_system = 3
                    self.create_version = DEFAULT_VERSION
                    self.extract_version = DEFAULT_VERSION
                    self.reserved = 0
                    self.flag_bits = 0
                    self.volume = 0
                    self.internal_attr = 0
                    self.external_attr = 0

                def __repr__(self):
                    result = [
                     '<%s filename=%r' % (self.__class__.__name__, self.filename)]
                    if self.compress_type != ZIP_STORED:
                        result.append(' compress_type=%s' % compressor_names.get(self.compress_type, self.compress_type))
                    hi = self.external_attr >> 16
                    lo = self.external_attr & 65535
                    if hi:
                        result.append(' filemode=%r' % stat.filemode(hi))
                    if lo:
                        result.append(' external_attr=%#x' % lo)
                    isdir = self.is_dir()
                    if not isdir or self.file_size:
                        result.append(' file_size=%r' % self.file_size)
                    if not isdir or self.compress_size:
                        if self.compress_type != ZIP_STORED or (self.file_size != self.compress_size):
                            result.append(' compress_size=%r' % self.compress_size)
                        result.append('>')
                        return ''.join(result)

                def FileHeader(self, zip64=None):
                    """Return the per-file header as a bytes object."""
                    dt = self.date_time
                    dosdate = dt[0] - 1980 << 9 | dt[1] << 5 | dt[2]
                    dostime = dt[3] << 11 | dt[4] << 5 | dt[5] // 2
                    if self.flag_bits & 8:
                        CRC = compress_size = file_size = 0
                    else:
                        CRC = self.CRC
                        compress_size = self.compress_size
                        file_size = self.file_size
                    extra = self.extra
                    min_version = 0
                    if zip64 is None:
                        zip64 = file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT
                    if zip64:
                        fmt = '<HHQQ'
                        extra = extra + struct.pack(fmt, 1, struct.calcsize(fmt) - 4, file_size, compress_size)
                    if file_size > ZIP64_LIMIT or (compress_size > ZIP64_LIMIT):
                        if not zip64:
                            raise LargeZipFile('Filesize would require ZIP64 extensions')
                        file_size = 4294967295
                        compress_size = 4294967295
                        min_version = ZIP64_VERSION
                    if self.compress_type == ZIP_BZIP2:
                        min_version = max(BZIP2_VERSION, min_version)
                    elif self.compress_type == ZIP_LZMA:
                        min_version = max(LZMA_VERSION, min_version)
                    self.extract_version = max(min_version, self.extract_version)
                    self.create_version = max(min_version, self.create_version)
                    filename, flag_bits = self._encodeFilenameFlags()
                    header = struct.pack(structFileHeader, stringFileHeader, self.extract_version, self.reserved, flag_bits, self.compress_type, dostime, dosdate, CRC, compress_size, file_size, len(filename), len(extra))
                    return header + filename + extra

                def _encodeFilenameFlags(self):
                    try:
                        return (self.filename.encode('ascii'), self.flag_bits)
                    except UnicodeEncodeError:
                        return (
                         self.filename.encode('utf-8'), self.flag_bits | 2048)

                def _decodeExtra(self):
                    extra = self.extra
                    unpack = struct.unpack
                    while True:
                        if len(extra) >= 4:
                            tp, ln = unpack('<HH', extra[:4])
                            if ln + 4 > len(extra):
                                raise BadZipFile('Corrupt extra field %04x (size=%d)' % (tp, ln))
                            if tp == 1:
                                if ln >= 24:
                                    counts = unpack('<QQQ', extra[4:28])
                                elif ln == 16:
                                    counts = unpack('<QQ', extra[4:20])
                                elif ln == 8:
                                    counts = unpack('<Q', extra[4:12])
                                elif ln == 0:
                                    counts = ()
                                else:
                                    raise BadZipFile('Corrupt extra field %04x (size=%d)' % (tp, ln))
                                idx = 0
                                if self.file_size in (18446744073709551615, 4294967295):
                                    if len(counts) <= idx:
                                        raise BadZipFile('Corrupt zip64 extra field. File size not found.')
                                    self.file_size = counts[idx]
                                    idx += 1
                                if self.compress_size == 4294967295:
                                    if len(counts) <= idx:
                                        raise BadZipFile('Corrupt zip64 extra field. Compress size not found.')
                                    self.compress_size = counts[idx]
                                    idx += 1
                                if self.header_offset == 4294967295:
                                    if len(counts) <= idx:
                                        raise BadZipFile('Corrupt zip64 extra field. Header offset not found.')
                                    old = self.header_offset
                                    self.header_offset = counts[idx]
                                    idx += 1
                            extra = extra[ln + 4:]

                @classmethod
                def from_file(cls, filename, arcname=None, *, strict_timestamps=True):
                    """Construct an appropriate ZipInfo for a file on the filesystem.

        filename should be the path to a file or directory on the filesystem.

        arcname is the name which it will have within the archive (by default,
        this will be the same as filename, but without a drive letter and with
        leading path separators removed).
        """
                    if isinstance(filename, os.PathLike):
                        filename = os.fspath(filename)
                    st = os.stat(filename)
                    isdir = stat.S_ISDIR(st.st_mode)
                    mtime = time.localtime(st.st_mtime)
                    date_time = mtime[0:6]
                    if not strict_timestamps or date_time[0] < 1980:
                        date_time = (1980, 1, 1, 0, 0, 0)
                    elif not strict_timestamps:
                        if date_time[0] > 2107:
                            date_time = (2107, 12, 31, 23, 59, 59)
                    if arcname is None:
                        arcname = filename
                    arcname = os.path.normpath(os.path.splitdrive(arcname)[1])
                    while True:
                        if arcname[0] in (os.sep, os.altsep):
                            arcname = arcname[1:]

                    if isdir:
                        arcname += '/'
                    zinfo = cls(arcname, date_time)
                    zinfo.external_attr = (st.st_mode & 65535) << 16
                    if isdir:
                        zinfo.file_size = 0
                        zinfo.external_attr |= 16
                    else:
                        zinfo.file_size = st.st_size
                    return zinfo

                def is_dir(self):
                    """Return True if this archive member is a directory."""
                    return self.filename[(-1)] == '/'


            _crctable = None

            def _gen_crc(crc):
                for j in range(8):
                    if crc & 1:
                        crc = crc >> 1 ^ 3988292384
                    else:
                        crc >>= 1
                else:
                    return crc


            def _ZipDecrypter(pwd):
                global _crctable
                key0 = 305419896
                key1 = 591751049
                key2 = 878082192
                if _crctable is None:
                    _crctable = list(map(_gen_crc, range(256)))
                crctable = _crctable

                def crc32(ch, crc):
                    return crc >> 8 ^ crctable[((crc ^ ch) & 255)]

                def update_keys(c):
                    nonlocal key0
                    nonlocal key1
                    nonlocal key2
                    key0 = crc32(c, key0)
                    key1 = key1 + (key0 & 255) & 4294967295
                    key1 = key1 * 134775813 + 1 & 4294967295
                    key2 = crc32(key1 >> 24, key2)

                for p in pwd:
                    update_keys(p)
                else:

                    def decrypter(data):
                        result = bytearray()
                        append = result.append
                        for c in data:
                            k = key2 | 2
                            c ^= k * (k ^ 1) >> 8 & 255
                            update_keys(c)
                            append(c)
                        else:
                            return bytes(result)

                    return decrypter


            class LZMACompressor:

                def __init__(self):
                    self._comp = None

                def _init(self):
                    props = lzma._encode_filter_properties({'id': lzma.FILTER_LZMA1})
                    self._comp = lzma.LZMACompressor((lzma.FORMAT_RAW), filters=[
                     lzma._decode_filter_properties(lzma.FILTER_LZMA1, props)])
                    return struct.pack('<BBH', 9, 4, len(props)) + props

                def compress(self, data):
                    if self._comp is None:
                        return self._init() + self._comp.compress(data)
                    return self._comp.compress(data)

                def flush(self):
                    if self._comp is None:
                        return self._init() + self._comp.flush()
                    return self._comp.flush()


            class LZMADecompressor:

                def __init__(self):
                    self._decomp = None
                    self._unconsumed = b''
                    self.eof = False

                def decompress(self, data):
                    if self._decomp is None:
                        self._unconsumed += data
                        if len(self._unconsumed) <= 4:
                            return b''
                        psize, = struct.unpack('<H', self._unconsumed[2:4])
                        if len(self._unconsumed) <= 4 + psize:
                            return b''
                        self._decomp = lzma.LZMADecompressor((lzma.FORMAT_RAW), filters=[
                         lzma._decode_filter_properties(lzma.FILTER_LZMA1, self._unconsumed[4:4 + psize])])
                        data = self._unconsumed[4 + psize:]
                        del self._unconsumed
                    result = self._decomp.decompress(data)
                    self.eof = self._decomp.eof
                    return result


            compressor_names = {0:'store', 
             1:'shrink', 
             2:'reduce', 
             3:'reduce', 
             4:'reduce', 
             5:'reduce', 
             6:'implode', 
             7:'tokenize', 
             8:'deflate', 
             9:'deflate64', 
             10:'implode', 
             12:'bzip2', 
             14:'lzma', 
             18:'terse', 
             19:'lz77', 
             97:'wavpack', 
             98:'ppmd'}

            def _check_compression(compression):
                if compression == ZIP_STORED:
                    pass
                elif compression == ZIP_DEFLATED:
                    assert zlib, 'Compression requires the (missing) zlib module'
                elif compression == ZIP_BZIP2:
                    assert bz2, 'Compression requires the (missing) bz2 module'
                elif compression == ZIP_LZMA:
                    assert lzma, 'Compression requires the (missing) lzma module'
                else:
                    raise NotImplementedError('That compression method is not supported')


            def _get_compressor(compress_type, compresslevel=None):
                if compress_type == ZIP_DEFLATED:
                    if compresslevel is not None:
                        return zlib.compressobj(compresslevel, zlib.DEFLATED, -15)
                    return zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
                if compress_type == ZIP_BZIP2:
                    if compresslevel is not None:
                        return bz2.BZ2Compressor(compresslevel)
                    return bz2.BZ2Compressor()
                if compress_type == ZIP_LZMA:
                    return LZMACompressor()
                return


            def _get_decompressor(compress_type):
                _check_compression(compress_type)
                if compress_type == ZIP_STORED:
                    return
                if compress_type == ZIP_DEFLATED:
                    return zlib.decompressobj(-15)
                if compress_type == ZIP_BZIP2:
                    return bz2.BZ2Decompressor()
                if compress_type == ZIP_LZMA:
                    return LZMADecompressor()
                descr = compressor_names.get(compress_type)
                if descr:
                    raise NotImplementedError('compression type %d (%s)' % (compress_type, descr))
                else:
                    raise NotImplementedError('compression type %d' % (compress_type,))


            class _SharedFile:

                def __init__(self, file, pos, close, lock, writing):
                    self._file = file
                    self._pos = pos
                    self._close = close
                    self._lock = lock
                    self._writing = writing
                    self.seekable = file.seekable
                    self.tell = file.tell

                def seek(self, offset, whence=0):
                    with self._lock:
                        if self._writing():
                            raise ValueError("Can't reposition in the ZIP file while there is an open writing handle on it. Close the writing handle before trying to read.")
                        self._file.seek(offset, whence)
                        self._pos = self._file.tell()
                        return self._pos

                def read(self, n=-1):
                    with self._lock:
                        if self._writing():
                            raise ValueError("Can't read from the ZIP file while there is an open writing handle on it. Close the writing handle before trying to read.")
                        self._file.seek(self._pos)
                        data = self._file.read(n)
                        self._pos = self._file.tell()
                        return data

                def close(self):
                    if self._file is not None:
                        fileobj = self._file
                        self._file = None
                        self._close(fileobj)


            class _Tellable:

                def __init__(self, fp):
                    self.fp = fp
                    self.offset = 0

                def write(self, data):
                    n = self.fp.write(data)
                    self.offset += n
                    return n

                def tell(self):
                    return self.offset

                def flush(self):
                    self.fp.flush()

                def close(self):
                    self.fp.close()


            class ZipExtFile(io.BufferedIOBase):
                __doc__ = 'File-like object for reading an archive member.\n       Is returned by ZipFile.open().\n    '
                MAX_N = 1073741824
                MIN_READ_SIZE = 4096
                MAX_SEEK_READ = 16777216

                def __init__(self, fileobj, mode, zipinfo, pwd=None, close_fileobj=False):
                    self._fileobj = fileobj
                    self._pwd = pwd
                    self._close_fileobj = close_fileobj
                    self._compress_type = zipinfo.compress_type
                    self._compress_left = zipinfo.compress_size
                    self._left = zipinfo.file_size
                    self._decompressor = _get_decompressor(self._compress_type)
                    self._eof = False
                    self._readbuffer = b''
                    self._offset = 0
                    self.newlines = None
                    self.mode = mode
                    self.name = zipinfo.filename
                    if hasattr(zipinfo, 'CRC'):
                        self._expected_crc = zipinfo.CRC
                        self._running_crc = crc32(b'')
                    else:
                        self._expected_crc = None
                    self._seekable = False
                    try:
                        if fileobj.seekable():
                            self._orig_compress_start = fileobj.tell()
                            self._orig_compress_size = zipinfo.compress_size
                            self._orig_file_size = zipinfo.file_size
                            self._orig_start_crc = self._running_crc
                            self._seekable = True
                    except AttributeError:
                        pass
                    else:
                        self._decrypter = None
                        if pwd:
                            if zipinfo.flag_bits & 8:
                                check_byte = zipinfo._raw_time >> 8 & 255
                            else:
                                check_byte = zipinfo.CRC >> 24 & 255
                            h = self._init_decrypter()
                            if h != check_byte:
                                raise RuntimeError('Bad password for file %r' % zipinfo.orig_filename)

                def _init_decrypter(self):
                    self._decrypter = _ZipDecrypter(self._pwd)
                    header = self._fileobj.read(12)
                    self._compress_left -= 12
                    return self._decrypter(header)[11]

                def __repr__(self):
                    result = [
                     '<%s.%s' % (self.__class__.__module__,
                      self.__class__.__qualname__)]
                    if not self.closed:
                        result.append(' name=%r mode=%r' % (self.name, self.mode))
                        if self._compress_type != ZIP_STORED:
                            result.append(' compress_type=%s' % compressor_names.get(self._compress_type, self._compress_type))
                    else:
                        result.append(' [closed]')
                    result.append('>')
                    return ''.join(result)

                def readline(self, limit=-1):
                    """Read and return a line from the stream.

        If limit is specified, at most limit bytes will be read.
        """
                    if limit < 0:
                        i = self._readbuffer.find(b'\n', self._offset) + 1
                        if i > 0:
                            line = self._readbuffer[self._offset:i]
                            self._offset = i
                            return line
                    return io.BufferedIOBase.readline(self, limit)

                def peek(self, n=1):
                    """Returns buffered bytes without advancing the position."""
                    if n > len(self._readbuffer) - self._offset:
                        chunk = self.read(n)
                        if len(chunk) > self._offset:
                            self._readbuffer = chunk + self._readbuffer[self._offset:]
                            self._offset = 0
                        else:
                            self._offset -= len(chunk)
                    return self._readbuffer[self._offset:self._offset + 512]

                def readable(self):
                    return True

                def read(self, n=-1):
                    """Read and return up to n bytes.
        If the argument is omitted, None, or negative, data is read and returned until EOF is reached.
        """
                    if n is None or (n < 0):
                        buf = self._readbuffer[self._offset:]
                        self._readbuffer = b''
                        self._offset = 0
                        while True:
                            self._eof or buf += self._read1(self.MAX_N)

                        return buf
                    end = n + self._offset
                    if end < len(self._readbuffer):
                        buf = self._readbuffer[self._offset:end]
                        self._offset = end
                        return buf
                    n = end - len(self._readbuffer)
                    buf = self._readbuffer[self._offset:]
                    self._readbuffer = b''
                    self._offset = 0
                    while True:
                        if n > 0:
                            data = (self._eof or self._read1)(n)
                            if n < len(data):
                                self._readbuffer = data
                                self._offset = n
                                buf += data[:n]
                            else:
                                buf += data
                                n -= len(data)

                    return buf

                def _update_crc(self, newdata):
                    if self._expected_crc is None:
                        return
                    self._running_crc = crc32(newdata, self._running_crc)
                    if self._eof:
                        if self._running_crc != self._expected_crc:
                            raise BadZipFile('Bad CRC-32 for file %r' % self.name)

                def read1--- This code section failed: ---

 L. 963         0  LOAD_FAST                'n'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'n'
               10  LOAD_CONST               0
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    82  'to 82'
             16_0  COME_FROM             6  '6'

 L. 964        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _readbuffer
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _offset
               24  LOAD_CONST               None
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  STORE_FAST               'buf'

 L. 965        32  LOAD_CONST               b''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _readbuffer

 L. 966        38  LOAD_CONST               0
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _offset
             44_0  COME_FROM            76  '76'
             44_1  COME_FROM            64  '64'

 L. 967        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _eof
               48  POP_JUMP_IF_TRUE     78  'to 78'

 L. 968        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _read1
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                MAX_N
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'data'

 L. 969        62  LOAD_FAST                'data'
               64  POP_JUMP_IF_FALSE_BACK    44  'to 44'

 L. 970        66  LOAD_FAST                'buf'
               68  LOAD_FAST                'data'
               70  INPLACE_ADD      
               72  STORE_FAST               'buf'

 L. 971        74  JUMP_FORWARD         78  'to 78'
               76  JUMP_BACK            44  'to 44'
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            48  '48'

 L. 972        78  LOAD_FAST                'buf'
               80  RETURN_VALUE     
             82_0  COME_FROM            14  '14'

 L. 974        82  LOAD_FAST                'n'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _offset
               88  BINARY_ADD       
               90  STORE_FAST               'end'

 L. 975        92  LOAD_FAST                'end'
               94  LOAD_GLOBAL              len
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _readbuffer
              100  CALL_FUNCTION_1       1  ''
              102  COMPARE_OP               <
              104  POP_JUMP_IF_FALSE   132  'to 132'

 L. 976       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _readbuffer
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _offset
              114  LOAD_FAST                'end'
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'buf'

 L. 977       122  LOAD_FAST                'end'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _offset

 L. 978       128  LOAD_FAST                'buf'
              130  RETURN_VALUE     
            132_0  COME_FROM           104  '104'

 L. 980       132  LOAD_FAST                'end'
              134  LOAD_GLOBAL              len
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _readbuffer
              140  CALL_FUNCTION_1       1  ''
              142  BINARY_SUBTRACT  
              144  STORE_FAST               'n'

 L. 981       146  LOAD_FAST                'self'
              148  LOAD_ATTR                _readbuffer
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _offset
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  STORE_FAST               'buf'

 L. 982       162  LOAD_CONST               b''
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _readbuffer

 L. 983       168  LOAD_CONST               0
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _offset

 L. 984       174  LOAD_FAST                'n'
              176  LOAD_CONST               0
              178  COMPARE_OP               >
          180_182  POP_JUMP_IF_FALSE   264  'to 264'
            184_0  COME_FROM           262  '262'
            184_1  COME_FROM           248  '248'

 L. 985       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _eof
          188_190  POP_JUMP_IF_TRUE    264  'to 264'

 L. 986       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _read1
              196  LOAD_FAST                'n'
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'data'

 L. 987       202  LOAD_FAST                'n'
              204  LOAD_GLOBAL              len
              206  LOAD_FAST                'data'
              208  CALL_FUNCTION_1       1  ''
              210  COMPARE_OP               <
              212  POP_JUMP_IF_FALSE   246  'to 246'

 L. 988       214  LOAD_FAST                'data'
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _readbuffer

 L. 989       220  LOAD_FAST                'n'
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _offset

 L. 990       226  LOAD_FAST                'buf'
              228  LOAD_FAST                'data'
              230  LOAD_CONST               None
              232  LOAD_FAST                'n'
              234  BUILD_SLICE_2         2 
              236  BINARY_SUBSCR    
              238  INPLACE_ADD      
              240  STORE_FAST               'buf'

 L. 991   242_244  JUMP_FORWARD        264  'to 264'
            246_0  COME_FROM           212  '212'

 L. 992       246  LOAD_FAST                'data'
              248  POP_JUMP_IF_FALSE_BACK   184  'to 184'

 L. 993       250  LOAD_FAST                'buf'
              252  LOAD_FAST                'data'
              254  INPLACE_ADD      
              256  STORE_FAST               'buf'

 L. 994   258_260  JUMP_FORWARD        264  'to 264'
              262  JUMP_BACK           184  'to 184'
            264_0  COME_FROM           258  '258'
            264_1  COME_FROM           242  '242'
            264_2  COME_FROM           188  '188'
            264_3  COME_FROM           180  '180'

 L. 995       264  LOAD_FAST                'buf'
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 76

                def _read1(self, n):
                    if self._eof or (n <= 0):
                        return b''
                    if self._compress_type == ZIP_DEFLATED:
                        data = self._decompressor.unconsumed_tail
                        if n > len(data):
                            data += self._read2(n - len(data))
                    else:
                        data = self._read2(n)
                    if self._compress_type == ZIP_STORED:
                        self._eof = self._compress_left <= 0
                    elif self._compress_type == ZIP_DEFLATED:
                        n = max(n, self.MIN_READ_SIZE)
                        data = self._decompressor.decompress(data, n)
                        self._eof = (self._decompressor.eof) or ((self._compress_left <= 0) and (not self._decompressor.unconsumed_tail))
                        if self._eof:
                            data += self._decompressor.flush()
                    else:
                        data = self._decompressor.decompress(data)
                        self._eof = self._decompressor.eof or self._compress_left <= 0
                    data = data[:self._left]
                    self._left -= len(data)
                    if self._left <= 0:
                        self._eof = True
                    self._update_crc(data)
                    return data

                def _read2(self, n):
                    if self._compress_left <= 0:
                        return b''
                    n = max(n, self.MIN_READ_SIZE)
                    n = min(n, self._compress_left)
                    data = self._fileobj.read(n)
                    self._compress_left -= len(data)
                    if not data:
                        raise EOFError
                    if self._decrypter is not None:
                        data = self._decrypter(data)
                    return data

                def close(self):
                    try:
                        if self._close_fileobj:
                            self._fileobj.close()
                    finally:
                        super().close()

                def seekable(self):
                    return self._seekable

                def seek(self, offset, whence=0):
                    if not self._seekable:
                        raise io.UnsupportedOperation('underlying stream is not seekable')
                    curr_pos = self.tell()
                    if whence == 0:
                        new_pos = offset
                    elif whence == 1:
                        new_pos = curr_pos + offset
                    elif whence == 2:
                        new_pos = self._orig_file_size + offset
                    else:
                        raise ValueError('whence must be os.SEEK_SET (0), os.SEEK_CUR (1), or os.SEEK_END (2)')
                    if new_pos > self._orig_file_size:
                        new_pos = self._orig_file_size
                    if new_pos < 0:
                        new_pos = 0
                    read_offset = new_pos - curr_pos
                    buff_offset = read_offset + self._offset
                    if buff_offset >= 0 and buff_offset < len(self._readbuffer):
                        self._offset = buff_offset
                        read_offset = 0
                    else:
                        pass
                    if read_offset < 0:
                        self._fileobj.seek(self._orig_compress_start)
                        self._running_crc = self._orig_start_crc
                        self._compress_left = self._orig_compress_size
                        self._left = self._orig_file_size
                        self._readbuffer = b''
                        self._offset = 0
                        self._decompressor = _get_decompressor(self._compress_type)
                        self._eof = False
                        read_offset = new_pos
                        if self._decrypter is not None:
                            self._init_decrypter()
                            while True:
                                if read_offset > 0:
                                    read_len = min(self.MAX_SEEK_READ, read_offset)
                                    self.read(read_len)
                                    read_offset -= read_len

                        return self.tell()

                def tell(self):
                    if not self._seekable:
                        raise io.UnsupportedOperation('underlying stream is not seekable')
                    filepos = self._orig_file_size - self._left - len(self._readbuffer) + self._offset
                    return filepos


            class _ZipWriteFile(io.BufferedIOBase):

                def __init__(self, zf, zinfo, zip64):
                    self._zinfo = zinfo
                    self._zip64 = zip64
                    self._zipfile = zf
                    self._compressor = _get_compressor(zinfo.compress_type, zinfo._compresslevel)
                    self._file_size = 0
                    self._compress_size = 0
                    self._crc = 0

                @property
                def _fileobj(self):
                    return self._zipfile.fp

                def writable(self):
                    return True

                def write(self, data):
                    if self.closed:
                        raise ValueError('I/O operation on closed file.')
                    nbytes = len(data)
                    self._file_size += nbytes
                    self._crc = crc32(data, self._crc)
                    if self._compressor:
                        data = self._compressor.compress(data)
                        self._compress_size += len(data)
                    self._fileobj.write(data)
                    return nbytes

                def close(self):
                    if self.closed:
                        return
                    try:
                        super().close()
                        if self._compressor:
                            buf = self._compressor.flush()
                            self._compress_size += len(buf)
                            self._fileobj.write(buf)
                            self._zinfo.compress_size = self._compress_size
                        else:
                            self._zinfo.compress_size = self._file_size
                        self._zinfo.CRC = self._crc
                        self._zinfo.file_size = self._file_size
                        if self._zinfo.flag_bits & 8:
                            fmt = '<LLQQ' if self._zip64 else '<LLLL'
                            self._fileobj.write(struct.pack(fmt, _DD_SIGNATURE, self._zinfo.CRC, self._zinfo.compress_size, self._zinfo.file_size))
                            self._zipfile.start_dir = self._fileobj.tell()
                        else:
                            if not self._zip64:
                                if self._file_size > ZIP64_LIMIT:
                                    raise RuntimeError('File size unexpectedly exceeded ZIP64 limit')
                                if self._compress_size > ZIP64_LIMIT:
                                    raise RuntimeError('Compressed size unexpectedly exceeded ZIP64 limit')
                            self._zipfile.start_dir = self._fileobj.tell()
                            self._fileobj.seek(self._zinfo.header_offset)
                            self._fileobj.write(self._zinfo.FileHeader(self._zip64))
                            self._fileobj.seek(self._zipfile.start_dir)
                        self._zipfile.filelist.append(self._zinfo)
                        self._zipfile.NameToInfo[self._zinfo.filename] = self._zinfo
                    finally:
                        self._zipfile._writing = False


            class ZipFile:
                __doc__ = ' Class with methods to open, read, write, close, list zip files.\n\n    z = ZipFile(file, mode="r", compression=ZIP_STORED, allowZip64=True,\n                compresslevel=None)\n\n    file: Either the path to the file, or a file-like object.\n          If it is a path, the file will be opened and closed by ZipFile.\n    mode: The mode can be either read \'r\', write \'w\', exclusive create \'x\',\n          or append \'a\'.\n    compression: ZIP_STORED (no compression), ZIP_DEFLATED (requires zlib),\n                 ZIP_BZIP2 (requires bz2) or ZIP_LZMA (requires lzma).\n    allowZip64: if True ZipFile will create files with ZIP64 extensions when\n                needed, otherwise it will raise an exception when this would\n                be necessary.\n    compresslevel: None (default for the given compression type) or an integer\n                   specifying the level to pass to the compressor.\n                   When using ZIP_STORED or ZIP_LZMA this keyword has no effect.\n                   When using ZIP_DEFLATED integers 0 through 9 are accepted.\n                   When using ZIP_BZIP2 integers 1 through 9 are accepted.\n\n    '
                fp = None
                _windows_illegal_name_trans_table = None

                def __init__--- This code section failed: ---

 L.1222         0  LOAD_FAST                'mode'
                2  LOAD_CONST               ('r', 'w', 'x', 'a')
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.1223         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 "ZipFile requires mode 'r', 'w', 'x', or 'a'"
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.1225        16  LOAD_GLOBAL              _check_compression
               18  LOAD_FAST                'compression'
               20  CALL_FUNCTION_1       1  ''
               22  POP_TOP          

 L.1227        24  LOAD_FAST                'allowZip64'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _allowZip64

 L.1228        30  LOAD_CONST               False
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _didModify

 L.1229        36  LOAD_CONST               0
               38  LOAD_FAST                'self'
               40  STORE_ATTR               debug

 L.1230        42  BUILD_MAP_0           0 
               44  LOAD_FAST                'self'
               46  STORE_ATTR               NameToInfo

 L.1231        48  BUILD_LIST_0          0 
               50  LOAD_FAST                'self'
               52  STORE_ATTR               filelist

 L.1232        54  LOAD_FAST                'compression'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               compression

 L.1233        60  LOAD_FAST                'compresslevel'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               compresslevel

 L.1234        66  LOAD_FAST                'mode'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               mode

 L.1235        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               pwd

 L.1236        78  LOAD_CONST               b''
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _comment

 L.1237        84  LOAD_FAST                'strict_timestamps'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _strict_timestamps

 L.1240        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'file'
               94  LOAD_GLOBAL              os
               96  LOAD_ATTR                PathLike
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L.1241       102  LOAD_GLOBAL              os
              104  LOAD_METHOD              fspath
              106  LOAD_FAST                'file'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'file'
            112_0  COME_FROM           100  '100'

 L.1242       112  LOAD_GLOBAL              isinstance
              114  LOAD_FAST                'file'
              116  LOAD_GLOBAL              str
              118  CALL_FUNCTION_2       2  ''
              120  POP_JUMP_IF_FALSE   230  'to 230'

 L.1244       122  LOAD_CONST               0
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _filePassed

 L.1245       128  LOAD_FAST                'file'
              130  LOAD_FAST                'self'
              132  STORE_ATTR               filename

 L.1246       134  LOAD_STR                 'rb'
              136  LOAD_STR                 'w+b'
              138  LOAD_STR                 'x+b'
              140  LOAD_STR                 'r+b'

 L.1247       142  LOAD_STR                 'w+b'

 L.1247       144  LOAD_STR                 'wb'

 L.1247       146  LOAD_STR                 'xb'

 L.1246       148  LOAD_CONST               ('r', 'w', 'x', 'a', 'r+b', 'w+b', 'x+b')
              150  BUILD_CONST_KEY_MAP_7     7 
              152  STORE_FAST               'modeDict'

 L.1248       154  LOAD_FAST                'modeDict'
              156  LOAD_FAST                'mode'
              158  BINARY_SUBSCR    
              160  STORE_FAST               'filemode'
            162_0  COME_FROM           226  '226'
            162_1  COME_FROM           214  '214'

 L.1250       162  SETUP_FINALLY       182  'to 182'

 L.1251       164  LOAD_GLOBAL              io
              166  LOAD_METHOD              open
              168  LOAD_FAST                'file'
              170  LOAD_FAST                'filemode'
              172  CALL_METHOD_2         2  ''
              174  LOAD_FAST                'self'
              176  STORE_ATTR               fp
              178  POP_BLOCK        
              180  JUMP_FORWARD        228  'to 228'
            182_0  COME_FROM_FINALLY   162  '162'

 L.1252       182  DUP_TOP          
              184  LOAD_GLOBAL              OSError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   222  'to 222'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L.1253       196  LOAD_FAST                'filemode'
              198  LOAD_FAST                'modeDict'
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   216  'to 216'

 L.1254       204  LOAD_FAST                'modeDict'
              206  LOAD_FAST                'filemode'
              208  BINARY_SUBSCR    
              210  STORE_FAST               'filemode'

 L.1255       212  POP_EXCEPT       
              214  JUMP_BACK           162  'to 162'
            216_0  COME_FROM           202  '202'

 L.1256       216  RAISE_VARARGS_0       0  'reraise'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        228  'to 228'
            222_0  COME_FROM           188  '188'
              222  END_FINALLY      

 L.1257       224  JUMP_FORWARD        228  'to 228'
              226  JUMP_BACK           162  'to 162'
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           220  '220'
            228_2  COME_FROM           180  '180'
              228  JUMP_FORWARD        256  'to 256'
            230_0  COME_FROM           120  '120'

 L.1259       230  LOAD_CONST               1
              232  LOAD_FAST                'self'
              234  STORE_ATTR               _filePassed

 L.1260       236  LOAD_FAST                'file'
              238  LOAD_FAST                'self'
              240  STORE_ATTR               fp

 L.1261       242  LOAD_GLOBAL              getattr
              244  LOAD_FAST                'file'
              246  LOAD_STR                 'name'
              248  LOAD_CONST               None
              250  CALL_FUNCTION_3       3  ''
              252  LOAD_FAST                'self'
              254  STORE_ATTR               filename
            256_0  COME_FROM           228  '228'

 L.1262       256  LOAD_CONST               1
              258  LOAD_FAST                'self'
              260  STORE_ATTR               _fileRefCnt

 L.1263       262  LOAD_GLOBAL              threading
              264  LOAD_METHOD              RLock
              266  CALL_METHOD_0         0  ''
              268  LOAD_FAST                'self'
              270  STORE_ATTR               _lock

 L.1264       272  LOAD_CONST               True
              274  LOAD_FAST                'self'
              276  STORE_ATTR               _seekable

 L.1265       278  LOAD_CONST               False
              280  LOAD_FAST                'self'
              282  STORE_ATTR               _writing

 L.1267   284_286  SETUP_FINALLY       552  'to 552'

 L.1268       288  LOAD_FAST                'mode'
              290  LOAD_STR                 'r'
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   308  'to 308'

 L.1269       298  LOAD_FAST                'self'
              300  LOAD_METHOD              _RealGetContents
              302  CALL_METHOD_0         0  ''
              304  POP_TOP          
              306  JUMP_FORWARD        548  'to 548'
            308_0  COME_FROM           294  '294'

 L.1270       308  LOAD_FAST                'mode'
              310  LOAD_CONST               ('w', 'x')
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   446  'to 446'

 L.1273       318  LOAD_CONST               True
              320  LOAD_FAST                'self'
              322  STORE_ATTR               _didModify

 L.1274       324  SETUP_FINALLY       342  'to 342'

 L.1275       326  LOAD_FAST                'self'
              328  LOAD_ATTR                fp
              330  LOAD_METHOD              tell
              332  CALL_METHOD_0         0  ''
              334  LOAD_FAST                'self'
              336  STORE_ATTR               start_dir
              338  POP_BLOCK        
              340  JUMP_FORWARD        392  'to 392'
            342_0  COME_FROM_FINALLY   324  '324'

 L.1276       342  DUP_TOP          
              344  LOAD_GLOBAL              AttributeError
              346  LOAD_GLOBAL              OSError
              348  BUILD_TUPLE_2         2 
              350  COMPARE_OP               exception-match
          352_354  POP_JUMP_IF_FALSE   390  'to 390'
              356  POP_TOP          
              358  POP_TOP          
              360  POP_TOP          

 L.1277       362  LOAD_GLOBAL              _Tellable
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                fp
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_FAST                'self'
              372  STORE_ATTR               fp

 L.1278       374  LOAD_CONST               0
              376  LOAD_FAST                'self'
              378  STORE_ATTR               start_dir

 L.1279       380  LOAD_CONST               False
              382  LOAD_FAST                'self'
              384  STORE_ATTR               _seekable
              386  POP_EXCEPT       
              388  JUMP_FORWARD        444  'to 444'
            390_0  COME_FROM           352  '352'
              390  END_FINALLY      
            392_0  COME_FROM           340  '340'

 L.1282       392  SETUP_FINALLY       412  'to 412'

 L.1283       394  LOAD_FAST                'self'
              396  LOAD_ATTR                fp
              398  LOAD_METHOD              seek
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                start_dir
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          
              408  POP_BLOCK        
              410  JUMP_FORWARD        444  'to 444'
            412_0  COME_FROM_FINALLY   392  '392'

 L.1284       412  DUP_TOP          
              414  LOAD_GLOBAL              AttributeError
              416  LOAD_GLOBAL              OSError
              418  BUILD_TUPLE_2         2 
              420  COMPARE_OP               exception-match
          422_424  POP_JUMP_IF_FALSE   442  'to 442'
              426  POP_TOP          
              428  POP_TOP          
              430  POP_TOP          

 L.1285       432  LOAD_CONST               False
              434  LOAD_FAST                'self'
              436  STORE_ATTR               _seekable
              438  POP_EXCEPT       
              440  JUMP_FORWARD        444  'to 444'
            442_0  COME_FROM           422  '422'
              442  END_FINALLY      
            444_0  COME_FROM           440  '440'
            444_1  COME_FROM           410  '410'
            444_2  COME_FROM           388  '388'
              444  JUMP_FORWARD        548  'to 548'
            446_0  COME_FROM           314  '314'

 L.1286       446  LOAD_FAST                'mode'
              448  LOAD_STR                 'a'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   540  'to 540'

 L.1287       456  SETUP_FINALLY       484  'to 484'

 L.1289       458  LOAD_FAST                'self'
              460  LOAD_METHOD              _RealGetContents
              462  CALL_METHOD_0         0  ''
              464  POP_TOP          

 L.1291       466  LOAD_FAST                'self'
              468  LOAD_ATTR                fp
              470  LOAD_METHOD              seek
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                start_dir
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          
              480  POP_BLOCK        
              482  JUMP_FORWARD        538  'to 538'
            484_0  COME_FROM_FINALLY   456  '456'

 L.1292       484  DUP_TOP          
              486  LOAD_GLOBAL              BadZipFile
              488  COMPARE_OP               exception-match
          490_492  POP_JUMP_IF_FALSE   536  'to 536'
              494  POP_TOP          
              496  POP_TOP          
              498  POP_TOP          

 L.1294       500  LOAD_FAST                'self'
              502  LOAD_ATTR                fp
              504  LOAD_METHOD              seek
              506  LOAD_CONST               0
              508  LOAD_CONST               2
              510  CALL_METHOD_2         2  ''
              512  POP_TOP          

 L.1298       514  LOAD_CONST               True
              516  LOAD_FAST                'self'
              518  STORE_ATTR               _didModify

 L.1299       520  LOAD_FAST                'self'
              522  LOAD_ATTR                fp
              524  LOAD_METHOD              tell
              526  CALL_METHOD_0         0  ''
              528  LOAD_FAST                'self'
              530  STORE_ATTR               start_dir
              532  POP_EXCEPT       
              534  JUMP_FORWARD        538  'to 538'
            536_0  COME_FROM           490  '490'
              536  END_FINALLY      
            538_0  COME_FROM           534  '534'
            538_1  COME_FROM           482  '482'
              538  JUMP_FORWARD        548  'to 548'
            540_0  COME_FROM           452  '452'

 L.1301       540  LOAD_GLOBAL              ValueError
              542  LOAD_STR                 "Mode must be 'r', 'w', 'x', or 'a'"
              544  CALL_FUNCTION_1       1  ''
              546  RAISE_VARARGS_1       1  'exception instance'
            548_0  COME_FROM           538  '538'
            548_1  COME_FROM           444  '444'
            548_2  COME_FROM           306  '306'
              548  POP_BLOCK        
              550  JUMP_FORWARD        588  'to 588'
            552_0  COME_FROM_FINALLY   284  '284'

 L.1302       552  POP_TOP          
              554  POP_TOP          
              556  POP_TOP          

 L.1303       558  LOAD_FAST                'self'
              560  LOAD_ATTR                fp
              562  STORE_FAST               'fp'

 L.1304       564  LOAD_CONST               None
              566  LOAD_FAST                'self'
              568  STORE_ATTR               fp

 L.1305       570  LOAD_FAST                'self'
              572  LOAD_METHOD              _fpclose
              574  LOAD_FAST                'fp'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          

 L.1306       580  RAISE_VARARGS_0       0  'reraise'
              582  POP_EXCEPT       
              584  JUMP_FORWARD        588  'to 588'
              586  END_FINALLY      
            588_0  COME_FROM           584  '584'
            588_1  COME_FROM           550  '550'

Parse error at or near `JUMP_BACK' instruction at offset 214

                def __enter__(self):
                    return self

                def __exit__(self, type, value, traceback):
                    self.close()

                def __repr__(self):
                    result = [
                     '<%s.%s' % (self.__class__.__module__,
                      self.__class__.__qualname__)]
                    if self.fp is not None:
                        if self._filePassed:
                            result.append(' file=%r' % self.fp)
                        elif self.filename is not None:
                            result.append(' filename=%r' % self.filename)
                        result.append(' mode=%r' % self.mode)
                    else:
                        result.append(' [closed]')
                    result.append('>')
                    return ''.join(result)

                def _RealGetContents(self):
                    """Read in the table of contents for the ZIP file."""
                    fp = self.fp
                    try:
                        endrec = _EndRecData(fp)
                    except OSError:
                        raise BadZipFile('File is not a zip file')
                    else:
                        if not endrec:
                            raise BadZipFile('File is not a zip file')
                        if self.debug > 1:
                            print(endrec)
                        size_cd = endrec[_ECD_SIZE]
                        offset_cd = endrec[_ECD_OFFSET]
                        self._comment = endrec[_ECD_COMMENT]
                        concat = endrec[_ECD_LOCATION] - size_cd - offset_cd
                        if endrec[_ECD_SIGNATURE] == stringEndArchive64:
                            concat -= sizeEndCentDir64 + sizeEndCentDir64Locator
                        if self.debug > 2:
                            inferred = concat + offset_cd
                            print('given, inferred, offset', offset_cd, inferred, concat)
                        self.start_dir = offset_cd + concat
                        fp.seek(self.start_dir, 0)
                        data = fp.read(size_cd)
                        fp = io.BytesIO(data)
                        total = 0
                        while True:
                            if total < size_cd:
                                centdir = fp.read(sizeCentralDir)
                                if len(centdir) != sizeCentralDir:
                                    raise BadZipFile('Truncated central directory')
                                centdir = struct.unpack(structCentralDir, centdir)
                                if centdir[_CD_SIGNATURE] != stringCentralDir:
                                    raise BadZipFile('Bad magic number for central directory')
                                if self.debug > 2:
                                    print(centdir)
                                filename = fp.read(centdir[_CD_FILENAME_LENGTH])
                                flags = centdir[5]
                                if flags & 2048:
                                    filename = filename.decode('utf-8')
                                else:
                                    filename = filename.decode('cp437')
                                x = ZipInfo(filename)
                                x.extra = fp.read(centdir[_CD_EXTRA_FIELD_LENGTH])
                                x.comment = fp.read(centdir[_CD_COMMENT_LENGTH])
                                x.header_offset = centdir[_CD_LOCAL_HEADER_OFFSET]
                                x.create_version, x.create_system, x.extract_version, x.reserved, x.flag_bits, x.compress_type, t, d, x.CRC, x.compress_size, x.file_size = centdir[1:12]
                                if x.extract_version > MAX_EXTRACT_VERSION:
                                    raise NotImplementedError('zip file version %.1f' % (x.extract_version / 10))
                                x.volume, x.internal_attr, x.external_attr = centdir[15:18]
                                x._raw_time = t
                                x.date_time = ((d >> 9) + 1980, d >> 5 & 15, d & 31,
                                 t >> 11, t >> 5 & 63, (t & 31) * 2)
                                x._decodeExtra()
                                x.header_offset = x.header_offset + concat
                                self.filelist.append(x)
                                self.NameToInfo[x.filename] = x
                                total = total + sizeCentralDir + centdir[_CD_FILENAME_LENGTH] + centdir[_CD_EXTRA_FIELD_LENGTH] + centdir[_CD_COMMENT_LENGTH]
                                if self.debug > 2:
                                    print('total', total)

                def namelist(self):
                    """Return a list of file names in the archive."""
                    return [data.filename for data in self.filelist]

                def infolist(self):
                    """Return a list of class ZipInfo instances for files in the
        archive."""
                    return self.filelist

                def printdir(self, file=None):
                    """Print a table of contents for the zip file."""
                    print(('%-46s %19s %12s' % ('File Name', 'Modified    ', 'Size')), file=file)
                    for zinfo in self.filelist:
                        date = '%d-%02d-%02d %02d:%02d:%02d' % zinfo.date_time[:6]
                        print(('%-46s %s %12d' % (zinfo.filename, date, zinfo.file_size)), file=file)

                def testzip--- This code section failed: ---

 L.1426         0  LOAD_CONST               1048576
                2  STORE_FAST               'chunk_size'

 L.1427         4  LOAD_FAST                'self'
                6  LOAD_ATTR                filelist
                8  GET_ITER         
             10_0  COME_FROM            88  '88'
             10_1  COME_FROM            56  '56'
               10  FOR_ITER             90  'to 90'
               12  STORE_FAST               'zinfo'

 L.1428        14  SETUP_FINALLY        58  'to 58'

 L.1431        16  LOAD_FAST                'self'
               18  LOAD_METHOD              open
               20  LOAD_FAST                'zinfo'
               22  LOAD_ATTR                filename
               24  LOAD_STR                 'r'
               26  CALL_METHOD_2         2  ''
               28  SETUP_WITH           48  'to 48'
               30  STORE_FAST               'f'
             32_0  COME_FROM            42  '42'

 L.1432        32  LOAD_FAST                'f'
               34  LOAD_METHOD              read
               36  LOAD_FAST                'chunk_size'
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE    44  'to 44'

 L.1433        42  JUMP_BACK            32  'to 32'
             44_0  COME_FROM            40  '40'
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       28  '28'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      
               54  POP_BLOCK        
               56  JUMP_BACK            10  'to 10'
             58_0  COME_FROM_FINALLY    14  '14'

 L.1434        58  DUP_TOP          
               60  LOAD_GLOBAL              BadZipFile
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    86  'to 86'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.1435        72  LOAD_FAST                'zinfo'
               74  LOAD_ATTR                filename
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  ROT_TWO          
               82  POP_TOP          
               84  RETURN_VALUE     
             86_0  COME_FROM            64  '64'
               86  END_FINALLY      
               88  JUMP_BACK            10  'to 10'
             90_0  COME_FROM            10  '10'

Parse error at or near `ROT_TWO' instruction at offset 80

                def getinfo(self, name):
                    """Return the instance of ZipInfo given 'name'."""
                    info = self.NameToInfo.get(name)
                    if info is None:
                        raise KeyError('There is no item named %r in the archive' % name)
                    return info

                def setpassword(self, pwd):
                    """Set default password for encrypted files."""
                    if pwd:
                        if not isinstance(pwd, bytes):
                            raise TypeError('pwd: expected bytes, got %s' % type(pwd).__name__)
                    if pwd:
                        self.pwd = pwd
                    else:
                        self.pwd = None

                @property
                def comment(self):
                    """The comment text associated with the ZIP file."""
                    return self._comment

                @comment.setter
                def comment(self, comment):
                    if not isinstance(comment, bytes):
                        raise TypeError('comment: expected bytes, got %s' % type(comment).__name__)
                    if len(comment) > ZIP_MAX_COMMENT:
                        import warnings
                        warnings.warn(('Archive comment is too long; truncating to %d bytes' % ZIP_MAX_COMMENT),
                          stacklevel=2)
                        comment = comment[:ZIP_MAX_COMMENT]
                    self._comment = comment
                    self._didModify = True

                def read(self, name, pwd=None):
                    """Return file bytes for name."""
                    with self.open(name, 'r', pwd) as fp:
                        return fp.read()

                def open--- This code section failed: ---

 L.1494         0  LOAD_FAST                'mode'
                2  LOAD_CONST               frozenset({'w', 'r'})
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.1495         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'open() requires mode "r" or "w"'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.1496        16  LOAD_FAST                'pwd'
               18  POP_JUMP_IF_FALSE    48  'to 48'
               20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'pwd'
               24  LOAD_GLOBAL              bytes
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     48  'to 48'

 L.1497        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'pwd: expected bytes, got %s'
               34  LOAD_GLOBAL              type
               36  LOAD_FAST                'pwd'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_ATTR                __name__
               42  BINARY_MODULO    
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            28  '28'
             48_1  COME_FROM            18  '18'

 L.1498        48  LOAD_FAST                'pwd'
               50  POP_JUMP_IF_FALSE    68  'to 68'
               52  LOAD_FAST                'mode'
               54  LOAD_STR                 'w'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L.1499        60  LOAD_GLOBAL              ValueError
               62  LOAD_STR                 'pwd is only supported for reading files'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'
             68_1  COME_FROM            50  '50'

 L.1500        68  LOAD_DEREF               'self'
               70  LOAD_ATTR                fp
               72  POP_JUMP_IF_TRUE     82  'to 82'

 L.1501        74  LOAD_GLOBAL              ValueError

 L.1502        76  LOAD_STR                 'Attempt to use ZIP archive that was already closed'

 L.1501        78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            72  '72'

 L.1505        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'name'
               86  LOAD_GLOBAL              ZipInfo
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L.1507        92  LOAD_FAST                'name'
               94  STORE_FAST               'zinfo'
               96  JUMP_FORWARD        142  'to 142'
             98_0  COME_FROM            90  '90'

 L.1508        98  LOAD_FAST                'mode'
              100  LOAD_STR                 'w'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   132  'to 132'

 L.1509       106  LOAD_GLOBAL              ZipInfo
              108  LOAD_FAST                'name'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'zinfo'

 L.1510       114  LOAD_DEREF               'self'
              116  LOAD_ATTR                compression
              118  LOAD_FAST                'zinfo'
              120  STORE_ATTR               compress_type

 L.1511       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                compresslevel
              126  LOAD_FAST                'zinfo'
              128  STORE_ATTR               _compresslevel
              130  JUMP_FORWARD        142  'to 142'
            132_0  COME_FROM           104  '104'

 L.1514       132  LOAD_DEREF               'self'
              134  LOAD_METHOD              getinfo
              136  LOAD_FAST                'name'
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'zinfo'
            142_0  COME_FROM           130  '130'
            142_1  COME_FROM            96  '96'

 L.1516       142  LOAD_FAST                'mode'
              144  LOAD_STR                 'w'
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   164  'to 164'

 L.1517       150  LOAD_DEREF               'self'
              152  LOAD_ATTR                _open_to_write
              154  LOAD_FAST                'zinfo'
              156  LOAD_FAST                'force_zip64'
              158  LOAD_CONST               ('force_zip64',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  RETURN_VALUE     
            164_0  COME_FROM           148  '148'

 L.1519       164  LOAD_DEREF               'self'
              166  LOAD_ATTR                _writing
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L.1520       170  LOAD_GLOBAL              ValueError
              172  LOAD_STR                 "Can't read from the ZIP file while there is an open writing handle on it. Close the writing handle before trying to read."
              174  CALL_FUNCTION_1       1  ''
              176  RAISE_VARARGS_1       1  'exception instance'
            178_0  COME_FROM           168  '168'

 L.1525       178  LOAD_DEREF               'self'
              180  DUP_TOP          
              182  LOAD_ATTR                _fileRefCnt
              184  LOAD_CONST               1
              186  INPLACE_ADD      
              188  ROT_TWO          
              190  STORE_ATTR               _fileRefCnt

 L.1526       192  LOAD_GLOBAL              _SharedFile
              194  LOAD_DEREF               'self'
              196  LOAD_ATTR                fp
              198  LOAD_FAST                'zinfo'
              200  LOAD_ATTR                header_offset

 L.1527       202  LOAD_DEREF               'self'
              204  LOAD_ATTR                _fpclose

 L.1527       206  LOAD_DEREF               'self'
              208  LOAD_ATTR                _lock

 L.1527       210  LOAD_CLOSURE             'self'
              212  BUILD_TUPLE_1         1 
              214  LOAD_LAMBDA              '<code_object <lambda>>'
              216  LOAD_STR                 'ZipFile.open.<locals>.<lambda>'
              218  MAKE_FUNCTION_8          'closure'

 L.1526       220  CALL_FUNCTION_5       5  ''
              222  STORE_FAST               'zef_file'

 L.1528   224_226  SETUP_FINALLY       506  'to 506'

 L.1530       228  LOAD_FAST                'zef_file'
              230  LOAD_METHOD              read
              232  LOAD_GLOBAL              sizeFileHeader
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'fheader'

 L.1531       238  LOAD_GLOBAL              len
              240  LOAD_FAST                'fheader'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_GLOBAL              sizeFileHeader
              246  COMPARE_OP               !=
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L.1532       252  LOAD_GLOBAL              BadZipFile
              254  LOAD_STR                 'Truncated file header'
              256  CALL_FUNCTION_1       1  ''
              258  RAISE_VARARGS_1       1  'exception instance'
            260_0  COME_FROM           248  '248'

 L.1533       260  LOAD_GLOBAL              struct
              262  LOAD_METHOD              unpack
              264  LOAD_GLOBAL              structFileHeader
              266  LOAD_FAST                'fheader'
              268  CALL_METHOD_2         2  ''
              270  STORE_FAST               'fheader'

 L.1534       272  LOAD_FAST                'fheader'
              274  LOAD_GLOBAL              _FH_SIGNATURE
              276  BINARY_SUBSCR    
              278  LOAD_GLOBAL              stringFileHeader
              280  COMPARE_OP               !=
          282_284  POP_JUMP_IF_FALSE   294  'to 294'

 L.1535       286  LOAD_GLOBAL              BadZipFile
              288  LOAD_STR                 'Bad magic number for file header'
              290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           282  '282'

 L.1537       294  LOAD_FAST                'zef_file'
              296  LOAD_METHOD              read
              298  LOAD_FAST                'fheader'
              300  LOAD_GLOBAL              _FH_FILENAME_LENGTH
              302  BINARY_SUBSCR    
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'fname'

 L.1538       308  LOAD_FAST                'fheader'
              310  LOAD_GLOBAL              _FH_EXTRA_FIELD_LENGTH
              312  BINARY_SUBSCR    
          314_316  POP_JUMP_IF_FALSE   332  'to 332'

 L.1539       318  LOAD_FAST                'zef_file'
              320  LOAD_METHOD              read
              322  LOAD_FAST                'fheader'
              324  LOAD_GLOBAL              _FH_EXTRA_FIELD_LENGTH
              326  BINARY_SUBSCR    
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
            332_0  COME_FROM           314  '314'

 L.1541       332  LOAD_FAST                'zinfo'
              334  LOAD_ATTR                flag_bits
              336  LOAD_CONST               32
              338  BINARY_AND       
          340_342  POP_JUMP_IF_FALSE   352  'to 352'

 L.1543       344  LOAD_GLOBAL              NotImplementedError
              346  LOAD_STR                 'compressed patched data (flag bit 5)'
              348  CALL_FUNCTION_1       1  ''
              350  RAISE_VARARGS_1       1  'exception instance'
            352_0  COME_FROM           340  '340'

 L.1545       352  LOAD_FAST                'zinfo'
              354  LOAD_ATTR                flag_bits
              356  LOAD_CONST               64
              358  BINARY_AND       
          360_362  POP_JUMP_IF_FALSE   372  'to 372'

 L.1547       364  LOAD_GLOBAL              NotImplementedError
              366  LOAD_STR                 'strong encryption (flag bit 6)'
              368  CALL_FUNCTION_1       1  ''
              370  RAISE_VARARGS_1       1  'exception instance'
            372_0  COME_FROM           360  '360'

 L.1549       372  LOAD_FAST                'zinfo'
              374  LOAD_ATTR                flag_bits
              376  LOAD_CONST               2048
              378  BINARY_AND       
          380_382  POP_JUMP_IF_FALSE   396  'to 396'

 L.1551       384  LOAD_FAST                'fname'
              386  LOAD_METHOD              decode
              388  LOAD_STR                 'utf-8'
              390  CALL_METHOD_1         1  ''
              392  STORE_FAST               'fname_str'
              394  JUMP_FORWARD        406  'to 406'
            396_0  COME_FROM           380  '380'

 L.1553       396  LOAD_FAST                'fname'
              398  LOAD_METHOD              decode
              400  LOAD_STR                 'cp437'
              402  CALL_METHOD_1         1  ''
              404  STORE_FAST               'fname_str'
            406_0  COME_FROM           394  '394'

 L.1555       406  LOAD_FAST                'fname_str'
              408  LOAD_FAST                'zinfo'
              410  LOAD_ATTR                orig_filename
              412  COMPARE_OP               !=
          414_416  POP_JUMP_IF_FALSE   436  'to 436'

 L.1556       418  LOAD_GLOBAL              BadZipFile

 L.1557       420  LOAD_STR                 'File name in directory %r and header %r differ.'

 L.1558       422  LOAD_FAST                'zinfo'
              424  LOAD_ATTR                orig_filename
              426  LOAD_FAST                'fname'
              428  BUILD_TUPLE_2         2 

 L.1557       430  BINARY_MODULO    

 L.1556       432  CALL_FUNCTION_1       1  ''
              434  RAISE_VARARGS_1       1  'exception instance'
            436_0  COME_FROM           414  '414'

 L.1561       436  LOAD_FAST                'zinfo'
              438  LOAD_ATTR                flag_bits
              440  LOAD_CONST               1
              442  BINARY_AND       
              444  STORE_FAST               'is_encrypted'

 L.1562       446  LOAD_FAST                'is_encrypted'
          448_450  POP_JUMP_IF_FALSE   484  'to 484'

 L.1563       452  LOAD_FAST                'pwd'
          454_456  POP_JUMP_IF_TRUE    464  'to 464'

 L.1564       458  LOAD_DEREF               'self'
              460  LOAD_ATTR                pwd
              462  STORE_FAST               'pwd'
            464_0  COME_FROM           454  '454'

 L.1565       464  LOAD_FAST                'pwd'
          466_468  POP_JUMP_IF_TRUE    488  'to 488'

 L.1566       470  LOAD_GLOBAL              RuntimeError
              472  LOAD_STR                 'File %r is encrypted, password required for extraction'

 L.1567       474  LOAD_FAST                'name'

 L.1566       476  BINARY_MODULO    
              478  CALL_FUNCTION_1       1  ''
              480  RAISE_VARARGS_1       1  'exception instance'
              482  JUMP_FORWARD        488  'to 488'
            484_0  COME_FROM           448  '448'

 L.1569       484  LOAD_CONST               None
              486  STORE_FAST               'pwd'
            488_0  COME_FROM           482  '482'
            488_1  COME_FROM           466  '466'

 L.1571       488  LOAD_GLOBAL              ZipExtFile
              490  LOAD_FAST                'zef_file'
              492  LOAD_FAST                'mode'
              494  LOAD_FAST                'zinfo'
              496  LOAD_FAST                'pwd'
              498  LOAD_CONST               True
              500  CALL_FUNCTION_5       5  ''
              502  POP_BLOCK        
              504  RETURN_VALUE     
            506_0  COME_FROM_FINALLY   224  '224'

 L.1572       506  POP_TOP          
              508  POP_TOP          
              510  POP_TOP          

 L.1573       512  LOAD_FAST                'zef_file'
              514  LOAD_METHOD              close
              516  CALL_METHOD_0         0  ''
              518  POP_TOP          

 L.1574       520  RAISE_VARARGS_0       0  'reraise'
              522  POP_EXCEPT       
              524  JUMP_FORWARD        528  'to 528'
              526  END_FINALLY      
            528_0  COME_FROM           524  '524'

Parse error at or near `POP_TOP' instruction at offset 518

                def _open_to_write(self, zinfo, force_zip64=False):
                    if force_zip64:
                        if not self._allowZip64:
                            raise ValueError('force_zip64 is True, but allowZip64 was False when opening the ZIP file.')
                        if self._writing:
                            raise ValueError("Can't write to the ZIP file while there is another write handle open on it. Close the first handle before opening another.")
                        if not hasattr(zinfo, 'file_size'):
                            zinfo.file_size = 0
                        zinfo.compress_size = 0
                        zinfo.CRC = 0
                        zinfo.flag_bits = 0
                        if zinfo.compress_type == ZIP_LZMA:
                            zinfo.flag_bits |= 2
                        if not self._seekable:
                            zinfo.flag_bits |= 8
                        if not zinfo.external_attr:
                            zinfo.external_attr = 25165824
                        zip64 = (self._allowZip64) and (force_zip64 or (zinfo.file_size * 1.05 > ZIP64_LIMIT))
                        if self._seekable:
                            self.fp.seek(self.start_dir)
                        zinfo.header_offset = self.fp.tell()
                        self._writecheck(zinfo)
                        self._didModify = True
                        self.fp.write(zinfo.FileHeader(zip64))
                        self._writing = True
                        return _ZipWriteFile(self, zinfo, zip64)

                def extract(self, member, path=None, pwd=None):
                    """Extract a member from the archive to the current working directory,
           using its full name. Its file information is extracted as accurately
           as possible. `member' may be a filename or a ZipInfo object. You can
           specify a different directory using `path'.
        """
                    if path is None:
                        path = os.getcwd()
                    else:
                        path = os.fspath(path)
                    return self._extract_member(member, path, pwd)

                def extractall(self, path=None, members=None, pwd=None):
                    """Extract all members from the archive to the current working
           directory. `path' specifies a different directory to extract to.
           `members' is optional and must be a subset of the list returned
           by namelist().
        """
                    if members is None:
                        members = self.namelist()
                    if path is None:
                        path = os.getcwd()
                    else:
                        path = os.fspath(path)
                    for zipinfo in members:
                        self._extract_member(zipinfo, path, pwd)

                @classmethod
                def _sanitize_windows_name(cls, arcname, pathsep):
                    """Replace bad characters and remove trailing dots from parts."""
                    table = cls._windows_illegal_name_trans_table
                    if not table:
                        illegal = ':<>|"?*'
                        table = str.maketrans(illegal, '_' * len(illegal))
                        cls._windows_illegal_name_trans_table = table
                    arcname = arcname.translate(table)
                    arcname = (x.rstrip('.') for x in arcname.split(pathsep))
                    arcname = pathsep.join((x for x in arcname if x))
                    return arcname

                def _extract_member(self, member, targetpath, pwd):
                    """Extract the ZipInfo object 'member' to a physical
           file on the path targetpath.
        """
                    if not isinstance(member, ZipInfo):
                        member = self.getinfo(member)
                    arcname = member.filename.replace('/', os.path.sep)
                    if os.path.altsep:
                        arcname = arcname.replace(os.path.altsep, os.path.sep)
                    arcname = os.path.splitdrive(arcname)[1]
                    invalid_path_parts = ('', os.path.curdir, os.path.pardir)
                    arcname = os.path.sep.join((x for x in arcname.split(os.path.sep) if x not in invalid_path_parts))
                    if os.path.sep == '\\':
                        arcname = self._sanitize_windows_name(arcname, os.path.sep)
                    targetpath = os.path.join(targetpath, arcname)
                    targetpath = os.path.normpath(targetpath)
                    upperdirs = os.path.dirname(targetpath)
                    if upperdirs:
                        if not os.path.exists(upperdirs):
                            os.makedirs(upperdirs)
                        if member.is_dir():
                            if not os.path.isdir(targetpath):
                                os.mkdir(targetpath)
                            return targetpath
                        with self.open(member, pwd=pwd) as source:
                            with open(targetpath, 'wb') as target:
                                shutil.copyfileobj(source, target)
                        return targetpath

                def _writecheck(self, zinfo):
                    """Check for errors before writing a file to the archive."""
                    if zinfo.filename in self.NameToInfo:
                        import warnings
                        warnings.warn(('Duplicate name: %r' % zinfo.filename), stacklevel=3)
                    if self.mode not in ('w', 'x', 'a'):
                        raise ValueError("write() requires mode 'w', 'x', or 'a'")
                    if not self.fp:
                        raise ValueError('Attempt to write ZIP archive that was already closed')
                    _check_compression(zinfo.compress_type)
                    if not self._allowZip64:
                        requires_zip64 = None
                        if len(self.filelist) >= ZIP_FILECOUNT_LIMIT:
                            requires_zip64 = 'Files count'
                        elif zinfo.file_size > ZIP64_LIMIT:
                            requires_zip64 = 'Filesize'
                        elif zinfo.header_offset > ZIP64_LIMIT:
                            requires_zip64 = 'Zipfile size'
                        if requires_zip64:
                            raise LargeZipFile(requires_zip64 + ' would require ZIP64 extensions')

                def write(self, filename, arcname=None, compress_type=None, compresslevel=None):
                    """Put the bytes from filename into the archive under the name
        arcname."""
                    if not self.fp:
                        raise ValueError('Attempt to write to ZIP archive that was already closed')
                    if self._writing:
                        raise ValueError("Can't write to ZIP archive while an open writing handle exists")
                    zinfo = ZipInfo.from_file(filename, arcname, strict_timestamps=(self._strict_timestamps))
                    if zinfo.is_dir():
                        zinfo.compress_size = 0
                        zinfo.CRC = 0
                    else:
                        if compress_type is not None:
                            zinfo.compress_type = compress_type
                        else:
                            zinfo.compress_type = self.compression
                        if compresslevel is not None:
                            zinfo._compresslevel = compresslevel
                        else:
                            zinfo._compresslevel = self.compresslevel
                    if zinfo.is_dir():
                        with self._lock:
                            if self._seekable:
                                self.fp.seek(self.start_dir)
                            zinfo.header_offset = self.fp.tell()
                            if zinfo.compress_type == ZIP_LZMA:
                                zinfo.flag_bits |= 2
                            self._writecheck(zinfo)
                            self._didModify = True
                            self.filelist.append(zinfo)
                            self.NameToInfo[zinfo.filename] = zinfo
                            self.fp.write(zinfo.FileHeader(False))
                            self.start_dir = self.fp.tell()
                    else:
                        with open(filename, 'rb') as src:
                            with self.open(zinfo, 'w') as dest:
                                shutil.copyfileobj(src, dest, 8192)

                def writestr(self, zinfo_or_arcname, data, compress_type=None, compresslevel=None):
                    """Write a file into the archive.  The contents is 'data', which
        may be either a 'str' or a 'bytes' instance; if it is a 'str',
        it is encoded as UTF-8 first.
        'zinfo_or_arcname' is either a ZipInfo instance or
        the name of the file in the archive."""
                    if isinstance(data, str):
                        data = data.encode('utf-8')
                    if not isinstance(zinfo_or_arcname, ZipInfo):
                        zinfo = ZipInfo(filename=zinfo_or_arcname, date_time=(time.localtime(time.time())[:6]))
                        zinfo.compress_type = self.compression
                        zinfo._compresslevel = self.compresslevel
                        if zinfo.filename[(-1)] == '/':
                            zinfo.external_attr = 1107099648
                            zinfo.external_attr |= 16
                        else:
                            zinfo.external_attr = 25165824
                    else:
                        zinfo = zinfo_or_arcname
                    if not self.fp:
                        raise ValueError('Attempt to write to ZIP archive that was already closed')
                    if self._writing:
                        raise ValueError("Can't write to ZIP archive while an open writing handle exists.")
                    if compress_type is not None:
                        zinfo.compress_type = compress_type
                    if compresslevel is not None:
                        zinfo._compresslevel = compresslevel
                    zinfo.file_size = len(data)
                    with self._lock:
                        with self.open(zinfo, mode='w') as dest:
                            dest.write(data)

                def __del__(self):
                    """Call the "close()" method in case the user forgot."""
                    self.close()

                def close(self):
                    """Close the file, and for mode 'w', 'x' and 'a' write the ending
        records."""
                    if self.fp is None:
                        return
                    if self._writing:
                        raise ValueError("Can't close the ZIP file while there is an open writing handle on it. Close the writing handle before closing the zip.")
                    try:
                        if self.mode in ('w', 'x', 'a'):
                            if self._didModify:
                                with self._lock:
                                    if self._seekable:
                                        self.fp.seek(self.start_dir)
                                    self._write_end_record()
                    finally:
                        fp = self.fp
                        self.fp = None
                        self._fpclose(fp)

                def _write_end_record(self):
                    for zinfo in self.filelist:
                        dt = zinfo.date_time
                        dosdate = dt[0] - 1980 << 9 | dt[1] << 5 | dt[2]
                        dostime = dt[3] << 11 | dt[4] << 5 | dt[5] // 2
                        extra = []
                        if zinfo.file_size > ZIP64_LIMIT or zinfo.compress_size > ZIP64_LIMIT:
                            extra.append(zinfo.file_size)
                            extra.append(zinfo.compress_size)
                            file_size = 4294967295
                            compress_size = 4294967295
                        else:
                            file_size = zinfo.file_size
                            compress_size = zinfo.compress_size
                        if zinfo.header_offset > ZIP64_LIMIT:
                            extra.append(zinfo.header_offset)
                            header_offset = 4294967295
                        else:
                            header_offset = zinfo.header_offset
                        extra_data = zinfo.extra
                        min_version = 0
                        if extra:
                            extra_data = _strip_extra(extra_data, (1, ))
                            extra_data = (struct.pack)('<HH' + 'Q' * len(extra), 1, 8 * len(extra), *extra) + extra_data
                            min_version = ZIP64_VERSION
                        else:
                            if zinfo.compress_type == ZIP_BZIP2:
                                min_version = max(BZIP2_VERSION, min_version)
                            elif zinfo.compress_type == ZIP_LZMA:
                                min_version = max(LZMA_VERSION, min_version)
                            extract_version = max(min_version, zinfo.extract_version)
                            create_version = max(min_version, zinfo.create_version)
                            try:
                                filename, flag_bits = zinfo._encodeFilenameFlags()
                                centdir = struct.pack(structCentralDir, stringCentralDir, create_version, zinfo.create_system, extract_version, zinfo.reserved, flag_bits, zinfo.compress_type, dostime, dosdate, zinfo.CRC, compress_size, file_size, len(filename), len(extra_data), len(zinfo.comment), 0, zinfo.internal_attr, zinfo.external_attr, header_offset)
                            except DeprecationWarning:
                                print((structCentralDir, stringCentralDir, create_version,
                                 zinfo.create_system, extract_version, zinfo.reserved,
                                 zinfo.flag_bits, zinfo.compress_type, dostime, dosdate,
                                 zinfo.CRC, compress_size, file_size,
                                 len(zinfo.filename), len(extra_data), len(zinfo.comment),
                                 0, zinfo.internal_attr, zinfo.external_attr,
                                 header_offset),
                                  file=(sys.stderr))
                                raise
                            else:
                                self.fp.write(centdir)
                                self.fp.write(filename)
                                self.fp.write(extra_data)
                                self.fp.write(zinfo.comment)
                    else:
                        pos2 = self.fp.tell()
                        centDirCount = len(self.filelist)
                        centDirSize = pos2 - self.start_dir
                        centDirOffset = self.start_dir
                        requires_zip64 = None
                        if centDirCount > ZIP_FILECOUNT_LIMIT:
                            requires_zip64 = 'Files count'
                        elif centDirOffset > ZIP64_LIMIT:
                            requires_zip64 = 'Central directory offset'
                        elif centDirSize > ZIP64_LIMIT:
                            requires_zip64 = 'Central directory size'
                        if requires_zip64:
                            if not self._allowZip64:
                                raise LargeZipFile(requires_zip64 + ' would require ZIP64 extensions')
                            zip64endrec = struct.pack(structEndArchive64, stringEndArchive64, 44, 45, 45, 0, 0, centDirCount, centDirCount, centDirSize, centDirOffset)
                            self.fp.write(zip64endrec)
                            zip64locrec = struct.pack(structEndArchive64Locator, stringEndArchive64Locator, 0, pos2, 1)
                            self.fp.write(zip64locrec)
                            centDirCount = min(centDirCount, 65535)
                            centDirSize = min(centDirSize, 4294967295)
                            centDirOffset = min(centDirOffset, 4294967295)
                        endrec = struct.pack(structEndArchive, stringEndArchive, 0, 0, centDirCount, centDirCount, centDirSize, centDirOffset, len(self._comment))
                        self.fp.write(endrec)
                        self.fp.write(self._comment)
                        self.fp.flush()

                def _fpclose(self, fp):
                    assert self._fileRefCnt > 0
                    self._fileRefCnt -= 1
                    if not self._fileRefCnt:
                        if not self._filePassed:
                            fp.close()


            class PyZipFile(ZipFile):
                __doc__ = 'Class to create ZIP archives with Python library files and packages.'

                def __init__(self, file, mode='r', compression=ZIP_STORED, allowZip64=True, optimize=-1):
                    ZipFile.__init__(self, file, mode=mode, compression=compression, allowZip64=allowZip64)
                    self._optimize = optimize

                def writepy(self, pathname, basename='', filterfunc=None):
                    """Add all files from "pathname" to the ZIP archive.

        If pathname is a package directory, search the directory and
        all package subdirectories recursively for all *.py and enter
        the modules into the archive.  If pathname is a plain
        directory, listdir *.py and enter all modules.  Else, pathname
        must be a Python *.py file and the module will be put into the
        archive.  Added modules are always module.pyc.
        This method will compile the module.py into module.pyc if
        necessary.
        If filterfunc(pathname) is given, it is called with every argument.
        When it is False, the file or directory is skipped.
        """
                    pathname = os.fspath(pathname)
                    if filterfunc:
                        if not filterfunc(pathname):
                            if self.debug:
                                label = 'path' if os.path.isdir(pathname) else 'file'
                                print('%s %r skipped by filterfunc' % (label, pathname))
                            return
                    dir, name = os.path.split(pathname)
                    if os.path.isdir(pathname):
                        initname = os.path.join(pathname, '__init__.py')
                        if os.path.isfile(initname):
                            if basename:
                                basename = '%s/%s' % (basename, name)
                            else:
                                basename = name
                            if self.debug:
                                print('Adding package in', pathname, 'as', basename)
                            fname, arcname = self._get_codename(initname[0:-3], basename)
                            if self.debug:
                                print('Adding', arcname)
                            self.write(fname, arcname)
                            dirlist = sorted(os.listdir(pathname))
                            dirlist.remove('__init__.py')
                            for filename in dirlist:
                                path = os.path.join(pathname, filename)
                                root, ext = os.path.splitext(filename)
                                if os.path.isdir(path):
                                    if os.path.isfile(os.path.join(path, '__init__.py')):
                                        self.writepy(path, basename, filterfunc=filterfunc)
                                else:
                                    if ext == '.py':
                                        if filterfunc:
                                            if not filterfunc(path):
                                                if self.debug:
                                                    print('file %r skipped by filterfunc' % path)
                                            fname, arcname = self._get_codename(path[0:-3], basename)
                                if self.debug:
                                    print('Adding', arcname)
                                else:
                                    self.write(fname, arcname)

                        else:
                            if self.debug:
                                print('Adding files from directory', pathname)
                            for filename in sorted(os.listdir(pathname)):
                                path = os.path.join(pathname, filename)
                                root, ext = os.path.splitext(filename)
                                if ext == '.py':
                                    if filterfunc and not filterfunc(path):
                                        if self.debug:
                                            print('file %r skipped by filterfunc' % path)
                                    else:
                                        fname, arcname = self._get_codename(path[0:-3], basename)
                                        if self.debug:
                                            print('Adding', arcname)
                                        self.write(fname, arcname)

                    else:
                        if pathname[-3:] != '.py':
                            raise RuntimeError('Files added with writepy() must end with ".py"')
                        fname, arcname = self._get_codename(pathname[0:-3], basename)
                        if self.debug:
                            print('Adding file', arcname)
                        self.write(fname, arcname)

                def _get_codename(self, pathname, basename):
                    """Return (filename, archivename) for the path.

        Given a module name path, return the correct file path and
        archive name, compiling if necessary.  For example, given
        /python/lib/string, return (/python/lib/string.pyc, string).
        """

                    def _compile--- This code section failed: ---

 L.2053         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              py_compile
                6  STORE_FAST               'py_compile'

 L.2054         8  LOAD_DEREF               'self'
               10  LOAD_ATTR                debug
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L.2055        14  LOAD_GLOBAL              print
               16  LOAD_STR                 'Compiling'
               18  LOAD_FAST                'file'
               20  CALL_FUNCTION_2       2  ''
               22  POP_TOP          
             24_0  COME_FROM            12  '12'

 L.2056        24  SETUP_FINALLY        46  'to 46'

 L.2057        26  LOAD_FAST                'py_compile'
               28  LOAD_ATTR                compile
               30  LOAD_FAST                'file'
               32  LOAD_CONST               True
               34  LOAD_FAST                'optimize'
               36  LOAD_CONST               ('doraise', 'optimize')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_FORWARD         98  'to 98'
             46_0  COME_FROM_FINALLY    24  '24'

 L.2058        46  DUP_TOP          
               48  LOAD_FAST                'py_compile'
               50  LOAD_ATTR                PyCompileError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    96  'to 96'
               56  POP_TOP          
               58  STORE_FAST               'err'
               60  POP_TOP          
               62  SETUP_FINALLY        84  'to 84'

 L.2059        64  LOAD_GLOBAL              print
               66  LOAD_FAST                'err'
               68  LOAD_ATTR                msg
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          

 L.2060        74  POP_BLOCK        
               76  POP_EXCEPT       
               78  CALL_FINALLY         84  'to 84'
               80  LOAD_CONST               False
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'
             84_1  COME_FROM_FINALLY    62  '62'
               84  LOAD_CONST               None
               86  STORE_FAST               'err'
               88  DELETE_FAST              'err'
               90  END_FINALLY      
               92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            54  '54'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            44  '44'

 L.2061        98  LOAD_CONST               True
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 78

                    file_py = pathname + '.py'
                    file_pyc = pathname + '.pyc'
                    pycache_opt0 = importlib.util.cache_from_source(file_py, optimization='')
                    pycache_opt1 = importlib.util.cache_from_source(file_py, optimization=1)
                    pycache_opt2 = importlib.util.cache_from_source(file_py, optimization=2)
                    if self._optimize == -1:
                        if os.path.isfile(file_pyc) and os.stat(file_pyc).st_mtime >= os.stat(file_py).st_mtime:
                            arcname = fname = file_pyc
                        elif os.path.isfile(pycache_opt0) and os.stat(pycache_opt0).st_mtime >= os.stat(file_py).st_mtime:
                            fname = pycache_opt0
                            arcname = file_pyc
                        elif os.path.isfile(pycache_opt1) and os.stat(pycache_opt1).st_mtime >= os.stat(file_py).st_mtime:
                            fname = pycache_opt1
                            arcname = file_pyc
                        elif os.path.isfile(pycache_opt2) and os.stat(pycache_opt2).st_mtime >= os.stat(file_py).st_mtime:
                            fname = pycache_opt2
                            arcname = file_pyc
                        elif _compile(file_py):
                            if sys.flags.optimize == 0:
                                fname = pycache_opt0
                            elif sys.flags.optimize == 1:
                                fname = pycache_opt1
                            else:
                                fname = pycache_opt2
                            arcname = file_pyc
                        else:
                            fname = arcname = file_py
                    elif self._optimize == 0:
                        fname = pycache_opt0
                        arcname = file_pyc
                    else:
                        arcname = file_pyc
                        if self._optimize == 1:
                            fname = pycache_opt1
                        elif self._optimize == 2:
                            fname = pycache_opt2
                        else:
                            msg = "invalid value for 'optimize': {!r}".format(self._optimize)
                            raise ValueError(msg)
                    if not (os.path.isfile(fname) and os.stat(fname).st_mtime >= os.stat(file_py).st_mtime):
                        if not _compile(file_py, optimize=(self._optimize)):
                            fname = arcname = file_py
                        archivename = os.path.split(arcname)[1]
                        if basename:
                            archivename = '%s/%s' % (basename, archivename)
                        return (fname, archivename)


            def _unique_everseen(iterable, key=None):
                """List unique elements, preserving order. Remember all elements ever seen."""
                seen = set()
                seen_add = seen.add
                if key is None:
                    for element in itertools.filterfalse(seen.__contains__, iterable):
                        seen_add(element)
                        yield element

                else:
                    for element in iterable:
                        k = key(element)
                        if k not in seen:
                            seen_add(k)
                            yield element


            def _parents(path):
                """
    Given a path with elements separated by
    posixpath.sep, generate all parents of that path.

    >>> list(_parents('b/d'))
    ['b']
    >>> list(_parents('/b/d/'))
    ['/b']
    >>> list(_parents('b/d/f/'))
    ['b/d', 'b']
    >>> list(_parents('b'))
    []
    >>> list(_parents(''))
    []
    """
                return itertools.islice(_ancestry(path), 1, None)


            def _ancestry(path):
                """
    Given a path with elements separated by
    posixpath.sep, generate all elements of that path

    >>> list(_ancestry('b/d'))
    ['b/d', 'b']
    >>> list(_ancestry('/b/d/'))
    ['/b/d', '/b']
    >>> list(_ancestry('b/d/f/'))
    ['b/d/f', 'b/d', 'b']
    >>> list(_ancestry('b'))
    ['b']
    >>> list(_ancestry(''))
    []
    """
                path = path.rstrip(posixpath.sep)
                while path:
                    if path != posixpath.sep:
                        yield path
                        path, tail = posixpath.split(path)


            class CompleteDirs(ZipFile):
                __doc__ = '\n    A ZipFile subclass that ensures that implied directories\n    are always included in the namelist.\n    '

                @staticmethod
                def _implied_dirs(names):
                    parents = itertools.chain.from_iterable(map(_parents, names))
                    implied_dirs = OrderedDict.fromkeys((p + posixpath.sep for p in parents if p + posixpath.sep not in set(names)))
                    return implied_dirs

                def namelist(self):
                    names = super(CompleteDirs, self).namelist()
                    return names + list(self._implied_dirs(names))

                def _name_set(self):
                    return set(self.namelist())

                def resolve_dir(self, name):
                    """
        If the name represents a directory, return that name
        as a directory (with the trailing slash).
        """
                    names = self._name_set()
                    dirname = name + '/'
                    dir_match = name not in names and dirname in names
                    if dir_match:
                        return dirname
                    return name

                @classmethod
                def make(cls, source):
                    """
        Given a source (filename or zipfile), return an
        appropriate CompleteDirs subclass.
        """
                    if isinstance(source, CompleteDirs):
                        return source
                    if not isinstance(source, ZipFile):
                        return cls(source)
                    if 'r' not in source.mode:
                        cls = CompleteDirs
                    res = cls.__new__(cls)
                    vars(res).update(vars(source))
                    return res


            class FastLookup(CompleteDirs):
                __doc__ = '\n    ZipFile subclass to ensure implicit\n    dirs exist and are resolved rapidly.\n    '

                def namelist(self):
                    with contextlib.suppress(AttributeError):
                        return self._FastLookup__names
                    self._FastLookup__names = super(FastLookup, self).namelist()
                    return self._FastLookup__names

                def _name_set(self):
                    with contextlib.suppress(AttributeError):
                        return self._FastLookup__lookup
                    self._FastLookup__lookup = super(FastLookup, self)._name_set()
                    return self._FastLookup__lookup


            class Path:
                __doc__ = "\n    A pathlib-compatible interface for zip files.\n\n    Consider a zip file with this structure::\n\n        .\n        ├── a.txt\n        └── b\n            ├── c.txt\n            └── d\n                └── e.txt\n\n    >>> data = io.BytesIO()\n    >>> zf = ZipFile(data, 'w')\n    >>> zf.writestr('a.txt', 'content of a')\n    >>> zf.writestr('b/c.txt', 'content of c')\n    >>> zf.writestr('b/d/e.txt', 'content of e')\n    >>> zf.filename = 'abcde.zip'\n\n    Path accepts the zipfile object itself or a filename\n\n    >>> root = Path(zf)\n\n    From there, several path operations are available.\n\n    Directory iteration (including the zip file itself):\n\n    >>> a, b = root.iterdir()\n    >>> a\n    Path('abcde.zip', 'a.txt')\n    >>> b\n    Path('abcde.zip', 'b/')\n\n    name property:\n\n    >>> b.name\n    'b'\n\n    join with divide operator:\n\n    >>> c = b / 'c.txt'\n    >>> c\n    Path('abcde.zip', 'b/c.txt')\n    >>> c.name\n    'c.txt'\n\n    Read text:\n\n    >>> c.read_text()\n    'content of c'\n\n    existence:\n\n    >>> c.exists()\n    True\n    >>> (b / 'missing.txt').exists()\n    False\n\n    Coercion to string:\n\n    >>> str(c)\n    'abcde.zip/b/c.txt'\n    "
                _Path__repr = '{self.__class__.__name__}({self.root.filename!r}, {self.at!r})'

                def __init__(self, root, at=''):
                    self.root = FastLookup.make(root)
                    self.at = at

                @property
                def open(self):
                    return functools.partial(self.root.open, self.at)

                @property
                def name(self):
                    return posixpath.basename(self.at.rstrip('/'))

                def read_text(self, *args, **kwargs):
                    with self.open() as strm:
                        return (io.TextIOWrapper)(strm, *args, **kwargs).read()

                def read_bytes(self):
                    with self.open() as strm:
                        return strm.read()

                def _is_child(self, path):
                    return posixpath.dirname(path.at.rstrip('/')) == self.at.rstrip('/')

                def _next(self, at):
                    return Path(self.root, at)

                def is_dir(self):
                    return not self.at or self.at.endswith('/')

                def is_file(self):
                    return not self.is_dir()

                def exists(self):
                    return self.at in self.root._name_set()

                def iterdir(self):
                    if not self.is_dir():
                        raise ValueError("Can't listdir a file")
                    subs = map(self._next, self.root.namelist())
                    return filter(self._is_child, subs)

                def __str__(self):
                    return posixpath.join(self.root.filename, self.at)

                def __repr__(self):
                    return self._Path__repr.format(self=self)

                def joinpath(self, add):
                    next = posixpath.join(self.at, add)
                    return self._next(self.root.resolve_dir(next))

                __truediv__ = joinpath

                @property
                def parent(self):
                    parent_at = posixpath.dirname(self.at.rstrip('/'))
                    if parent_at:
                        parent_at += '/'
                    return self._next(parent_at)


            def main(args=None):
                import argparse
                description = 'A simple command-line interface for zipfile module.'
                parser = argparse.ArgumentParser(description=description)
                group = parser.add_mutually_exclusive_group(required=True)
                group.add_argument('-l', '--list', metavar='<zipfile>', help='Show listing of a zipfile')
                group.add_argument('-e', '--extract', nargs=2, metavar=('<zipfile>',
                                                                        '<output_dir>'),
                  help='Extract zipfile into target dir')
                group.add_argument('-c', '--create', nargs='+', metavar=('<name>',
                                                                         '<file>'),
                  help='Create zipfile from sources')
                group.add_argument('-t', '--test', metavar='<zipfile>', help='Test if a zipfile is valid')
                args = parser.parse_args(args)
                if args.test is not None:
                    src = args.test
                    with ZipFile(src, 'r') as zf:
                        badfile = zf.testzip()
                    if badfile:
                        print('The following enclosed file is corrupted: {!r}'.format(badfile))
                    print('Done testing')
                elif args.list is not None:
                    src = args.list
                    with ZipFile(src, 'r') as zf:
                        zf.printdir()
                elif args.extract is not None:
                    src, curdir = args.extract
                    with ZipFile(src, 'r') as zf:
                        zf.extractall(curdir)
                elif args.create is not None:
                    zip_name = args.create.pop(0)
                    files = args.create

                    def addToZip(zf, path, zippath):
                        if os.path.isfile(path):
                            zf.write(path, zippath, ZIP_DEFLATED)
                        elif os.path.isdir(path):
                            if zippath:
                                zf.write(path, zippath)
                            for nm in sorted(os.listdir(path)):
                                addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))

                    with ZipFile(zip_name, 'w') as zf:
                        for path in files:
                            zippath = os.path.basename(path)
                            if not zippath:
                                zippath = os.path.basename(os.path.dirname(path))
                            else:
                                if zippath in ('', os.curdir, os.pardir):
                                    zippath = ''
                                addToZip(zf, path, zippath)


            if __name__ == '__main__':
                main()