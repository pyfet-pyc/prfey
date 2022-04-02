# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PngImagePlugin.py
import logging, re, struct, zlib
from . import Image, ImageFile, ImagePalette
from ._binary import i8, i16be as i16, i32be as i32, o16be as o16, o32be as o32
logger = logging.getLogger(__name__)
is_cid = re.compile(b'\\w\\w\\w\\w').match
_MAGIC = b'\x89PNG\r\n\x1a\n'
_MODES = {(1, 0):('1', '1'), 
 (2, 0):('L', 'L;2'), 
 (4, 0):('L', 'L;4'), 
 (8, 0):('L', 'L'), 
 (16, 0):('I', 'I;16B'), 
 (8, 2):('RGB', 'RGB'), 
 (16, 2):('RGB', 'RGB;16B'), 
 (1, 3):('P', 'P;1'), 
 (2, 3):('P', 'P;2'), 
 (4, 3):('P', 'P;4'), 
 (8, 3):('P', 'P'), 
 (8, 4):('LA', 'LA'), 
 (16, 4):('RGBA', 'LA;16B'), 
 (8, 6):('RGBA', 'RGBA'), 
 (16, 6):('RGBA', 'RGBA;16B')}
_simple_palette = re.compile(b'^\xff*\x00\xff*$')
MAX_TEXT_CHUNK = ImageFile.SAFEBLOCK
MAX_TEXT_MEMORY = 64 * MAX_TEXT_CHUNK

def _safe_zlib_decompress(s):
    dobj = zlib.decompressobj()
    plaintext = dobj.decompress(s, MAX_TEXT_CHUNK)
    if dobj.unconsumed_tail:
        raise ValueError('Decompressed Data Too Large')
    return plaintext


def _crc32(data, seed=0):
    return zlib.crc32(data, seed) & 4294967295


class ChunkStream:

    def __init__(self, fp):
        self.fp = fp
        self.queue = []

    def read(self):
        """Fetch a new chunk. Returns header information."""
        cid = None
        if self.queue:
            cid, pos, length = self.queue.pop()
            self.fp.seek(pos)
        else:
            s = self.fp.read(8)
            cid = s[4:]
            pos = self.fp.tell()
            length = i32(s)
        if not is_cid(cid):
            if not ImageFile.LOAD_TRUNCATED_IMAGES:
                raise SyntaxError('broken PNG file (chunk %s)' % repr(cid))
        return (
         cid, pos, length)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.queue = self.crc = self.fp = None

    def push(self, cid, pos, length):
        self.queue.append((cid, pos, length))

    def call(self, cid, pos, length):
        """Call the appropriate chunk handler"""
        logger.debug('STREAM %r %s %s', cid, pos, length)
        return getattr(self, 'chunk_' + cid.decode('ascii'))(pos, length)

    def crc(self, cid, data):
        """Read and verify checksum"""
        if ImageFile.LOAD_TRUNCATED_IMAGES:
            if i8(cid[0]) >> 5 & 1:
                self.crc_skip(cid, data)
                return None
        try:
            crc1 = _crc32(data, _crc32(cid))
            crc2 = i32(self.fp.read(4))
            if crc1 != crc2:
                raise SyntaxError('broken PNG file (bad header checksum in %r)' % cid)
        except struct.error:
            raise SyntaxError('broken PNG file (incomplete checksum in %r)' % cid)

    def crc_skip(self, cid, data):
        """Read checksum.  Used if the C module is not present"""
        self.fp.read(4)

    def verify(self, endchunk=b'IEND'):
        cids = []
        while True:
            try:
                cid, pos, length = self.read()
            except struct.error:
                raise OSError('truncated PNG file')
            else:
                if cid == endchunk:
                    break
                self.crc(cid, ImageFile._safe_read(self.fp, length))
                cids.append(cid)

        return cids


class iTXt(str):
    __doc__ = '\n    Subclass of string to allow iTXt chunks to look like strings while\n    keeping their extra information\n\n    '

    @staticmethod
    def __new__(cls, text, lang=None, tkey=None):
        """
        :param cls: the class to use when creating the instance
        :param text: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        """
        self = str.__new__(cls, text)
        self.lang = lang
        self.tkey = tkey
        return self


class PngInfo:
    __doc__ = '\n    PNG chunk container (for use with save(pnginfo=))\n\n    '

    def __init__(self):
        self.chunks = []

    def add(self, cid, data):
        """Appends an arbitrary chunk. Use with caution.

        :param cid: a byte string, 4 bytes long.
        :param data: a byte string of the encoded data

        """
        self.chunks.append((cid, data))

    def add_itxt(self, key, value, lang='', tkey='', zip=False):
        """Appends an iTXt chunk.

        :param key: latin-1 encodable text key name
        :param value: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        :param zip: compression flag

        """
        if not isinstance(key, bytes):
            key = key.encode('latin-1', 'strict')
        else:
            if not isinstance(value, bytes):
                value = value.encode('utf-8', 'strict')
            else:
                if not isinstance(lang, bytes):
                    lang = lang.encode('utf-8', 'strict')
                tkey = isinstance(tkey, bytes) or tkey.encode('utf-8', 'strict')
            if zip:
                self.add(b'iTXt', key + b'\x00\x01\x00' + lang + b'\x00' + tkey + b'\x00' + zlib.compress(value))
            else:
                self.add(b'iTXt', key + b'\x00\x00\x00' + lang + b'\x00' + tkey + b'\x00' + value)

    def add_text(self, key, value, zip=False):
        """Appends a text chunk.

        :param key: latin-1 encodable text key name
        :param value: value for this key, text or an
           :py:class:`PIL.PngImagePlugin.iTXt` instance
        :param zip: compression flag

        """
        if isinstance(value, iTXt):
            return self.add_itxt(key, value, (value.lang), (value.tkey), zip=zip)
            if not isinstance(value, bytes):
                try:
                    value = value.encode('latin-1', 'strict')
                except UnicodeError:
                    return self.add_itxt(key, value, zip=zip)

        else:
            if not isinstance(key, bytes):
                key = key.encode('latin-1', 'strict')
            if zip:
                self.add(b'zTXt', key + b'\x00\x00' + zlib.compress(value))
            else:
                self.add(b'tEXt', key + b'\x00' + value)


class PngStream(ChunkStream):

    def __init__(self, fp):
        super().__init__(fp)
        self.im_info = {}
        self.im_text = {}
        self.im_size = (0, 0)
        self.im_mode = None
        self.im_tile = None
        self.im_palette = None
        self.im_custom_mimetype = None
        self.text_memory = 0

    def check_text_memory(self, chunklen):
        self.text_memory += chunklen
        if self.text_memory > MAX_TEXT_MEMORY:
            raise ValueError('Too much memory used in text chunks: %s>MAX_TEXT_MEMORY' % self.text_memory)

    def chunk_iCCP(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        i = s.find(b'\x00')
        logger.debug('iCCP profile name %r', s[:i])
        logger.debug('Compression method %s', i8(s[i]))
        comp_method = i8(s[i])
        if comp_method != 0:
            raise SyntaxError('Unknown compression method %s in iCCP chunk' % comp_method)
        try:
            icc_profile = _safe_zlib_decompress(s[i + 2:])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                icc_profile = None
            else:
                raise
        except zlib.error:
            icc_profile = None
        else:
            self.im_info['icc_profile'] = icc_profile
            return s

    def chunk_IHDR(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_size = (i32(s), i32(s[4:]))
        try:
            self.im_mode, self.im_rawmode = _MODES[(i8(s[8]), i8(s[9]))]
        except Exception:
            pass
        else:
            if i8(s[12]):
                self.im_info['interlace'] = 1
            if i8(s[11]):
                raise SyntaxError('unknown filter category')
            return s

    def chunk_IDAT(self, pos, length):
        self.im_tile = [
         (
          'zip', (0, 0) + self.im_size, pos, self.im_rawmode)]
        self.im_idat = length
        raise EOFError

    def chunk_IEND(self, pos, length):
        raise EOFError

    def chunk_PLTE(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == 'P':
            self.im_palette = (
             'RGB', s)
        return s

    def chunk_tRNS(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == 'P':
            if _simple_palette.match(s):
                i = s.find(b'\x00')
                if i >= 0:
                    self.im_info['transparency'] = i
                else:
                    self.im_info['transparency'] = s
            elif self.im_mode in ('1', 'L', 'I'):
                self.im_info['transparency'] = i16(s)
        elif self.im_mode == 'RGB':
            self.im_info['transparency'] = (
             i16(s), i16(s[2:]), i16(s[4:]))
        return s

    def chunk_gAMA(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['gamma'] = i32(s) / 100000.0
        return s

    def chunk_cHRM(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        raw_vals = struct.unpack('>%dI' % (len(s) // 4), s)
        self.im_info['chromaticity'] = tuple((elt / 100000.0 for elt in raw_vals))
        return s

    def chunk_sRGB(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['srgb'] = i8(s)
        return s

    def chunk_pHYs(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        px, py = i32(s), i32(s[4:])
        unit = i8(s[8])
        if unit == 1:
            dpi = (
             int(px * 0.0254 + 0.5), int(py * 0.0254 + 0.5))
            self.im_info['dpi'] = dpi
        else:
            if unit == 0:
                self.im_info['aspect'] = (
                 px, py)
        return s

    def chunk_tEXt(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b'\x00', 1)
        except ValueError:
            k = s
            v = b''
        else:
            if k:
                k = k.decode('latin-1', 'strict')
                v = v.decode('latin-1', 'replace')
                self.im_info[k] = self.im_text[k] = v
                self.check_text_memory(len(v))
            return s

    def chunk_zTXt(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b'\x00', 1)
        except ValueError:
            k = s
            v = b''
        else:
            if v:
                comp_method = i8(v[0])
            else:
                comp_method = 0
            if comp_method != 0:
                raise SyntaxError('Unknown compression method %s in zTXt chunk' % comp_method)
        try:
            v = _safe_zlib_decompress(v[1:])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                v = b''
            else:
                raise
        except zlib.error:
            v = b''
        else:
            if k:
                k = k.decode('latin-1', 'strict')
                v = v.decode('latin-1', 'replace')
                self.im_info[k] = self.im_text[k] = v
                self.check_text_memory(len(v))
            return s

    def chunk_iTXt(self, pos, length):
        r = s = ImageFile._safe_read(self.fp, length)
        try:
            k, r = r.split(b'\x00', 1)
        except ValueError:
            return s
        else:
            if len(r) < 2:
                return s
            cf, cm, r = i8(r[0]), i8(r[1]), r[2:]
        try:
            lang, tk, v = r.split(b'\x00', 2)
        except ValueError:
            return s
        else:
            if cf != 0:
                if cm == 0:
                    try:
                        v = _safe_zlib_decompress(v)
                    except ValueError:
                        if ImageFile.LOAD_TRUNCATED_IMAGES:
                            return s
                        raise
                    except zlib.error:
                        return s

                else:
                    return s
            try:
                k = k.decode('latin-1', 'strict')
                lang = lang.decode('utf-8', 'strict')
                tk = tk.decode('utf-8', 'strict')
                v = v.decode('utf-8', 'strict')
            except UnicodeError:
                return s
            else:
                self.im_info[k] = self.im_text[k] = iTXt(v, lang, tk)
                self.check_text_memory(len(v))
                return s

    def chunk_eXIf(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['exif'] = b'Exif\x00\x00' + s
        return s

    def chunk_acTL(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_custom_mimetype = 'image/apng'
        return s


def _accept(prefix):
    return prefix[:8] == _MAGIC


class PngImageFile(ImageFile.ImageFile):
    format = 'PNG'
    format_description = 'Portable network graphics'

    def _open(self):
        if self.fp.read(8) != _MAGIC:
            raise SyntaxError('not a PNG file')
        self.png = PngStream(self.fp)
        while True:
            cid, pos, length = self.png.read()
            try:
                s = self.png.call(cid, pos, length)
            except EOFError:
                break
            except AttributeError:
                logger.debug('%r %s %s (unknown)', cid, pos, length)
                s = ImageFile._safe_read(self.fp, length)
            else:
                self.png.crc(cid, s)

        self.mode = self.png.im_mode
        self._size = self.png.im_size
        self.info = self.png.im_info
        self._text = None
        self.tile = self.png.im_tile
        self.custom_mimetype = self.png.im_custom_mimetype
        if self.png.im_palette:
            rawmode, data = self.png.im_palette
            self.palette = ImagePalette.raw(rawmode, data)
        self._PngImageFile__prepare_idat = length

    @property
    def text(self):
        if self._text is None:
            self.load()
        return self._text

    def verify(self):
        """Verify PNG file"""
        if self.fp is None:
            raise RuntimeError('verify must be called directly after open')
        self.fp.seek(self.tile[0][2] - 8)
        self.png.verify()
        self.png.close()
        if self._exclusive_fp:
            self.fp.close()
        self.fp = None

    def load_prepare(self):
        """internal: prepare to read PNG file"""
        if self.info.get('interlace'):
            self.decoderconfig = self.decoderconfig + (1, )
        self._PngImageFile__idat = self._PngImageFile__prepare_idat
        ImageFile.ImageFile.load_prepare(self)

    def load_read(self, read_bytes):
        """internal: read more image data"""
        if self._PngImageFile__idat == 0:
            self.fp.read(4)
            cid, pos, length = self.png.read()
            if cid not in (b'IDAT', b'DDAT'):
                self.png.push(cid, pos, length)
                return b''
                self._PngImageFile__idat = length
            elif read_bytes <= 0:
                read_bytes = self._PngImageFile__idat
        else:
            read_bytes = min(read_bytes, self._PngImageFile__idat)
        self._PngImageFile__idat = self._PngImageFile__idat - read_bytes
        return self.fp.read(read_bytes)

    def load_end--- This code section failed: ---

 L. 671         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               4
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 673        12  SETUP_FINALLY        34  'to 34'

 L. 674        14  LOAD_FAST                'self'
               16  LOAD_ATTR                png
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'cid'
               26  STORE_FAST               'pos'
               28  STORE_FAST               'length'
               30  POP_BLOCK        
               32  JUMP_FORWARD         64  'to 64'
             34_0  COME_FROM_FINALLY    12  '12'

 L. 675        34  DUP_TOP          
               36  LOAD_GLOBAL              struct
               38  LOAD_ATTR                error
               40  LOAD_GLOBAL              SyntaxError
               42  BUILD_TUPLE_2         2 
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    62  'to 62'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 676        54  POP_EXCEPT       
               56  BREAK_LOOP          202  'to 202'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            46  '46'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            32  '32'

 L. 678        64  LOAD_FAST                'cid'
               66  LOAD_CONST               b'IEND'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    74  'to 74'

 L. 679        72  BREAK_LOOP          202  'to 202'
             74_0  COME_FROM            70  '70'

 L. 681        74  SETUP_FINALLY        96  'to 96'

 L. 682        76  LOAD_FAST                'self'
               78  LOAD_ATTR                png
               80  LOAD_METHOD              call
               82  LOAD_FAST                'cid'
               84  LOAD_FAST                'pos'
               86  LOAD_FAST                'length'
               88  CALL_METHOD_3         3  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_BACK             0  'to 0'
             96_0  COME_FROM_FINALLY    74  '74'

 L. 683        96  DUP_TOP          
               98  LOAD_GLOBAL              UnicodeDecodeError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   118  'to 118'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 684       110  POP_EXCEPT       
              112  BREAK_LOOP          202  'to 202'
              114  POP_EXCEPT       
              116  JUMP_BACK             0  'to 0'
            118_0  COME_FROM           102  '102'

 L. 685       118  DUP_TOP          
              120  LOAD_GLOBAL              EOFError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   150  'to 150'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 686       132  LOAD_GLOBAL              ImageFile
              134  LOAD_METHOD              _safe_read
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                fp
              140  LOAD_FAST                'length'
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          
              146  POP_EXCEPT       
              148  JUMP_BACK             0  'to 0'
            150_0  COME_FROM           124  '124'

 L. 687       150  DUP_TOP          
              152  LOAD_GLOBAL              AttributeError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   198  'to 198'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 688       164  LOAD_GLOBAL              logger
              166  LOAD_METHOD              debug
              168  LOAD_STR                 '%r %s %s (unknown)'
              170  LOAD_FAST                'cid'
              172  LOAD_FAST                'pos'
              174  LOAD_FAST                'length'
              176  CALL_METHOD_4         4  ''
              178  POP_TOP          

 L. 689       180  LOAD_GLOBAL              ImageFile
              182  LOAD_METHOD              _safe_read
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                fp
              188  LOAD_FAST                'length'
              190  CALL_METHOD_2         2  ''
              192  POP_TOP          
              194  POP_EXCEPT       
              196  JUMP_BACK             0  'to 0'
            198_0  COME_FROM           156  '156'
              198  END_FINALLY      
              200  JUMP_BACK             0  'to 0'
            202_0  COME_FROM_EXCEPT_CLAUSE   112  '112'
            202_1  COME_FROM_EXCEPT_CLAUSE    56  '56'

 L. 690       202  LOAD_FAST                'self'
              204  LOAD_ATTR                png
              206  LOAD_ATTR                im_text
              208  LOAD_FAST                'self'
              210  STORE_ATTR               _text

 L. 691       212  LOAD_FAST                'self'
              214  LOAD_ATTR                png
              216  LOAD_METHOD              close
              218  CALL_METHOD_0         0  ''
              220  POP_TOP          

 L. 692       222  LOAD_CONST               None
              224  LOAD_FAST                'self'
              226  STORE_ATTR               png

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 202_1

    def _getexif(self):
        if 'exif' not in self.info:
            self.load()
        if 'exif' not in self.info:
            return
        return dict(self.getexif())

    def getexif(self):
        if 'exif' not in self.info:
            self.load()
        return ImageFile.ImageFile.getexif(self)


_OUTMODES = {'1':('1', b'\x01\x00'), 
 'L;1':('L;1', b'\x01\x00'), 
 'L;2':('L;2', b'\x02\x00'), 
 'L;4':('L;4', b'\x04\x00'), 
 'L':('L', b'\x08\x00'), 
 'LA':('LA', b'\x08\x04'), 
 'I':('I;16B', b'\x10\x00'), 
 'I;16':('I;16B', b'\x10\x00'), 
 'P;1':('P;1', b'\x01\x03'), 
 'P;2':('P;2', b'\x02\x03'), 
 'P;4':('P;4', b'\x04\x03'), 
 'P':('P', b'\x08\x03'), 
 'RGB':('RGB', b'\x08\x02'), 
 'RGBA':('RGBA', b'\x08\x06')}

def putchunk(fp, cid, *data):
    """Write a PNG chunk (including CRC field)"""
    data = (b'').join(data)
    fp.write(o32(len(data)) + cid)
    fp.write(data)
    crc = _crc32(data, _crc32(cid))
    fp.write(o32(crc))


class _idat:

    def __init__(self, fp, chunk):
        self.fp = fp
        self.chunk = chunk

    def write(self, data):
        self.chunk(self.fp, b'IDAT', data)


def _save(im, fp, filename, chunk=putchunk):
    mode = im.mode
    if mode == 'P':
        if 'bits' in im.encoderinfo:
            colors = 1 << im.encoderinfo['bits']
        else:
            if im.palette:
                colors = max(min(len(im.palette.getdata()[1]) // 3, 256), 2)
            else:
                colors = 256
        if colors <= 2:
            bits = 1
        else:
            if colors <= 4:
                bits = 2
            else:
                if colors <= 16:
                    bits = 4
                else:
                    bits = 8
        if bits != 8:
            mode = '%s;%d' % (mode, bits)
    im.encoderconfig = (
     im.encoderinfo.get('optimize', False),
     im.encoderinfo.get('compress_level', -1),
     im.encoderinfo.get('compress_type', -1),
     im.encoderinfo.get('dictionary', b''))
    try:
        rawmode, mode = _OUTMODES[mode]
    except KeyError:
        raise OSError('cannot write mode %s as PNG' % mode)
    else:
        fp.write(_MAGIC)
        chunk(fp, b'IHDR', o32(im.size[0]), o32(im.size[1]), mode, b'\x00', b'\x00', b'\x00')
        chunks = [
         b'cHRM', b'gAMA', b'sBIT', b'sRGB', b'tIME']
        icc = im.encoderinfo.get('icc_profile', im.info.get('icc_profile'))
        if icc:
            name = b'ICC Profile'
            data = name + b'\x00\x00' + zlib.compress(icc)
            chunk(fp, b'iCCP', data)
            chunks.remove(b'sRGB')
        info = im.encoderinfo.get('pnginfo')
        if info:
            chunks_multiple_allowed = [
             b'sPLT', b'iTXt', b'tEXt', b'zTXt']
            for cid, data in info.chunks:
                if cid in chunks:
                    chunks.remove(cid)
                    chunk(fp, cid, data)

        elif cid in chunks_multiple_allowed:
            chunk(fp, cid, data)
        else:
            if im.mode == 'P':
                palette_byte_number = 2 ** bits * 3
                palette_bytes = im.im.getpalette('RGB')[:palette_byte_number]
                if len(palette_bytes) < palette_byte_number:
                    palette_bytes += b'\x00'
                else:
                    chunk(fp, b'PLTE', palette_bytes)
            transparency = im.encoderinfo.get('transparency', im.info.get('transparency', None))
    if transparency or transparency == 0:
        if im.mode == 'P':
            alpha_bytes = 2 ** bits
            if isinstance(transparency, bytes):
                chunk(fp, b'tRNS', transparency[:alpha_bytes])
            else:
                transparency = max(0, min(255, transparency))
                alpha = b'\xff' * transparency + b'\x00'
                chunk(fp, b'tRNS', alpha[:alpha_bytes])
        else:
            if im.mode in ('1', 'L', 'I'):
                transparency = max(0, min(65535, transparency))
                chunk(fp, b'tRNS', o16(transparency))
            else:
                if im.mode == 'RGB':
                    red, green, blue = transparency
                    chunk(fp, b'tRNS', o16(red) + o16(green) + o16(blue))
                else:
                    if 'transparency' in im.encoderinfo:
                        raise OSError('cannot use transparency for this mode')
    else:
        if im.mode == 'P':
            if im.im.getpalettemode() == 'RGBA':
                alpha = im.im.getpalette('RGBA', 'A')
                alpha_bytes = 2 ** bits
                chunk(fp, b'tRNS', alpha[:alpha_bytes])
        else:
            dpi = im.encoderinfo.get('dpi')
            if dpi:
                chunk(fp, b'pHYs', o32(int(dpi[0] / 0.0254 + 0.5)), o32(int(dpi[1] / 0.0254 + 0.5)), b'\x01')
            if info:
                chunks = [
                 b'bKGD', b'hIST']
                for cid, data in info.chunks:
                    if cid in chunks:
                        chunks.remove(cid)
                        chunk(fp, cid, data)

        exif = im.encoderinfo.get('exif', im.info.get('exif'))
        if exif:
            if isinstance(exif, Image.Exif):
                exif = exif.tobytes(8)
            if exif.startswith(b'Exif\x00\x00'):
                exif = exif[6:]
            chunk(fp, b'eXIf', exif)
        ImageFile._save(im, _idat(fp, chunk), [('zip', (0, 0) + im.size, 0, rawmode)])
        chunk(fp, b'IEND', b'')
        if hasattr(fp, 'flush'):
            fp.flush()


def getchunks(im, **params):
    """Return a list of PNG chunks representing this image."""

    class collector:
        data = []

        def write(self, data):
            pass

        def append(self, chunk):
            self.data.append(chunk)

    def append(fp, cid, *data):
        data = (b'').join(data)
        crc = o32(_crc32(data, _crc32(cid)))
        fp.append((cid, data, crc))

    fp = collector()
    try:
        im.encoderinfo = params
        _save(im, fp, None, append)
    finally:
        del im.encoderinfo

    return fp.data


Image.register_open(PngImageFile.format, PngImageFile, _accept)
Image.register_save(PngImageFile.format, _save)
Image.register_extensions(PngImageFile.format, ['.png', '.apng'])
Image.register_mime(PngImageFile.format, 'image/png')