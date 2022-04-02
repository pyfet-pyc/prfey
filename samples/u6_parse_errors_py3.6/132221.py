# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PngImagePlugin.py
import logging, re, zlib, struct
from . import Image, ImageFile, ImagePalette
from ._binary import i8, i16be as i16, i32be as i32, o16be as o16, o32be as o32
from ._util import py3
__version__ = '0.9'
logger = logging.getLogger(__name__)
is_cid = re.compile(b'\\w\\w\\w\\w').match
_MAGIC = b'\x89PNG\r\n\x1a\n'
_MODES = {(1, 0): ('1', '1'), 
 (2, 0): ('L', 'L;2'), 
 (4, 0): ('L', 'L;4'), 
 (8, 0): ('L', 'L'), 
 (16, 0): ('I', 'I;16B'), 
 (8, 2): ('RGB', 'RGB'), 
 (16, 2): ('RGB', 'RGB;16B'), 
 (1, 3): ('P', 'P;1'), 
 (2, 3): ('P', 'P;2'), 
 (4, 3): ('P', 'P;4'), 
 (8, 3): ('P', 'P'), 
 (8, 4): ('LA', 'LA'), 
 (16, 4): ('RGBA', 'LA;16B'), 
 (8, 6): ('RGBA', 'RGBA'), 
 (16, 6): ('RGBA', 'RGBA;16B')}
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


class ChunkStream(object):

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
                return
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
                raise IOError('truncated PNG file')

            if cid == endchunk:
                break
            self.crc(cid, ImageFile._safe_read(self.fp, length))
            cids.append(cid)

        return cids


class iTXt(str):
    __doc__ = '\n    Subclass of string to allow iTXt chunks to look like strings while\n    keeping their extra information\n\n    '

    @staticmethod
    def __new__(cls, text, lang, tkey):
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


class PngInfo(object):
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
        else:
            if not isinstance(value, bytes):
                try:
                    value = value.encode('latin-1', 'strict')
                except UnicodeError:
                    return self.add_itxt(key, value, zip=zip)

            if not isinstance(key, bytes):
                key = key.encode('latin-1', 'strict')
            if zip:
                self.add(b'zTXt', key + b'\x00\x00' + zlib.compress(value))
            else:
                self.add(b'tEXt', key + b'\x00' + value)


class PngStream(ChunkStream):

    def __init__(self, fp):
        ChunkStream.__init__(self, fp)
        self.im_info = {}
        self.im_text = {}
        self.im_size = (0, 0)
        self.im_mode = None
        self.im_tile = None
        self.im_palette = None
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

        self.im_info['icc_profile'] = icc_profile
        return s

    def chunk_IHDR(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_size = (i32(s), i32(s[4:]))
        try:
            self.im_mode, self.im_rawmode = _MODES[(i8(s[8]), i8(s[9]))]
        except:
            pass

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

    def chunk_tRNS--- This code section failed: ---

 L. 374         0  LOAD_GLOBAL              ImageFile
                2  LOAD_ATTR                _safe_read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  LOAD_FAST                'length'
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  STORE_FAST               's'

 L. 375        14  LOAD_FAST                'self'
               16  LOAD_ATTR                im_mode
               18  LOAD_STR                 'P'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    76  'to 76'

 L. 376        24  LOAD_GLOBAL              _simple_palette
               26  LOAD_ATTR                match
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  POP_JUMP_IF_FALSE    64  'to 64'

 L. 379        34  LOAD_FAST                's'
               36  LOAD_ATTR                find
               38  LOAD_CONST               b'\x00'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'i'

 L. 380        44  LOAD_FAST                'i'
               46  LOAD_CONST               0
               48  COMPARE_OP               >=
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 381        52  LOAD_FAST                'i'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                im_info
               58  LOAD_STR                 'transparency'
               60  STORE_SUBSCR     
               62  JUMP_ABSOLUTE       156  'to 156'
               64  ELSE                     '74'

 L. 385        64  LOAD_FAST                's'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                im_info
               70  LOAD_STR                 'transparency'
               72  STORE_SUBSCR     
             74_0  COME_FROM            50  '50'
               74  JUMP_FORWARD        156  'to 156'
               76  ELSE                     '156'

 L. 386        76  LOAD_FAST                'self'
               78  LOAD_ATTR                im_mode
               80  LOAD_STR                 'L'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 387        86  LOAD_GLOBAL              i16
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                im_info
               96  LOAD_STR                 'transparency'
               98  STORE_SUBSCR     
              100  JUMP_FORWARD        156  'to 156'
              102  ELSE                     '156'

 L. 388       102  LOAD_FAST                'self'
              104  LOAD_ATTR                im_mode
              106  LOAD_STR                 'RGB'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   156  'to 156'

 L. 389       112  LOAD_GLOBAL              i16
              114  LOAD_FAST                's'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  LOAD_GLOBAL              i16
              120  LOAD_FAST                's'
              122  LOAD_CONST               2
              124  LOAD_CONST               None
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  LOAD_GLOBAL              i16
              134  LOAD_FAST                's'
              136  LOAD_CONST               4
              138  LOAD_CONST               None
              140  BUILD_SLICE_2         2 
              142  BINARY_SUBSCR    
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  BUILD_TUPLE_3         3 
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                im_info
              152  LOAD_STR                 'transparency'
              154  STORE_SUBSCR     
            156_0  COME_FROM           110  '110'
            156_1  COME_FROM           100  '100'
            156_2  COME_FROM            74  '74'

 L. 390       156  LOAD_FAST                's'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 158

    def chunk_gAMA(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_info['gamma'] = i32(s) / 100000.0
        return s

    def chunk_cHRM(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        raw_vals = struct.unpack('>%dI' % (len(s) // 4), s)
        self.im_info['chromaticity'] = tuple(elt / 100000.0 for elt in raw_vals)
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

        if k:
            if py3:
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

        if k:
            if py3:
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
                if py3:
                    try:
                        k = k.decode('latin-1', 'strict')
                        lang = lang.decode('utf-8', 'strict')
                        tk = tk.decode('utf-8', 'strict')
                        v = v.decode('utf-8', 'strict')
                    except UnicodeError:
                        return s

                self.im_info[k] = self.im_text[k] = iTXt(v, lang, tk)
                self.check_text_memory(len(v))
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

            self.png.crc(cid, s)

        self.mode = self.png.im_mode
        self._size = self.png.im_size
        self.info = self.png.im_info
        self.text = self.png.im_text
        self.tile = self.png.im_tile
        if self.png.im_palette:
            rawmode, data = self.png.im_palette
            self.palette = ImagePalette.raw(rawmode, data)
        self._PngImageFile__idat = length

    def verify(self):
        """Verify PNG file"""
        if self.fp is None:
            raise RuntimeError('verify must be called directly after open')
        self.fp.seek(self.tile[0][2] - 8)
        self.png.verify()
        self.png.close()
        self.fp = None

    def load_prepare(self):
        """internal: prepare to read PNG file"""
        if self.info.get('interlace'):
            self.decoderconfig = self.decoderconfig + (1, )
        ImageFile.ImageFile.load_prepare(self)

    def load_read(self, read_bytes):
        """internal: read more image data"""
        while self._PngImageFile__idat == 0:
            self.fp.read(4)
            cid, pos, length = self.png.read()
            if cid not in (b'IDAT', b'DDAT'):
                self.png.push(cid, pos, length)
                return b''
            self._PngImageFile__idat = length

        if read_bytes <= 0:
            read_bytes = self._PngImageFile__idat
        else:
            read_bytes = min(read_bytes, self._PngImageFile__idat)
        self._PngImageFile__idat = self._PngImageFile__idat - read_bytes
        return self.fp.read(read_bytes)

    def load_end(self):
        """internal: finished reading image data"""
        self.png.close()
        self.png = None


_OUTMODES = {'1':('1', b'\x01\x00'), 
 'L;1':('L;1', b'\x01\x00'), 
 'L;2':('L;2', b'\x02\x00'), 
 'L;4':('L;4', b'\x04\x00'), 
 'L':('L', b'\x08\x00'), 
 'LA':('LA', b'\x08\x04'), 
 'I':('I;16B', b'\x10\x00'), 
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


class _idat(object):

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
        raise IOError('cannot write mode %s as PNG' % mode)

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

    if im.mode == 'P':
        palette_byte_number = 2 ** bits * 3
        palette_bytes = im.im.getpalette('RGB')[:palette_byte_number]
        while len(palette_bytes) < palette_byte_number:
            palette_bytes += b'\x00'

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
            if im.mode == 'L':
                transparency = max(0, min(65535, transparency))
                chunk(fp, b'tRNS', o16(transparency))
            else:
                if im.mode == 'RGB':
                    red, green, blue = transparency
                    chunk(fp, b'tRNS', o16(red) + o16(green) + o16(blue))
                else:
                    if 'transparency' in im.encoderinfo:
                        raise IOError('cannot use transparency for this mode')
    else:
        if im.mode == 'P':
            if im.im.getpalettemode() == 'RGBA':
                alpha = im.im.getpalette('RGBA', 'A')
                alpha_bytes = 2 ** bits
                chunk(fp, b'tRNS', alpha[:alpha_bytes])
    dpi = im.encoderinfo.get('dpi')
    if dpi:
        chunk(fp, b'pHYs', o32(int(dpi[0] / 0.0254 + 0.5)), o32(int(dpi[1] / 0.0254 + 0.5)), b'\x01')
    info = im.encoderinfo.get('pnginfo')
    if info:
        chunks = [
         b'bKGD', b'hIST']
        for cid, data in info.chunks:
            if cid in chunks:
                chunks.remove(cid)
                chunk(fp, cid, data)

    ImageFile._save(im, _idat(fp, chunk), [
     (
      'zip', (0, 0) + im.size, 0, rawmode)])
    chunk(fp, b'IEND', b'')
    if hasattr(fp, 'flush'):
        fp.flush()


def getchunks(im, **params):
    """Return a list of PNG chunks representing this image."""

    class collector(object):
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
Image.register_extension(PngImageFile.format, '.png')
Image.register_mime(PngImageFile.format, 'image/png')