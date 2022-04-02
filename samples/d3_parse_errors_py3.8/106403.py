# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PngImagePlugin.py
import itertools, logging, re, struct, warnings, zlib
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
from ._binary import i8, i16be as i16, i32be as i32, o8, o16be as o16, o32be as o32
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
APNG_DISPOSE_OP_NONE = 0
APNG_DISPOSE_OP_BACKGROUND = 1
APNG_DISPOSE_OP_PREVIOUS = 2
APNG_BLEND_OP_SOURCE = 0
APNG_BLEND_OP_OVER = 1

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
                raise OSError('truncated PNG file')
            else:
                if cid == endchunk:
                    pass
                else:
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
        if not isinstance(value, bytes):
            value = value.encode('utf-8', 'strict')
        if not isinstance(lang, bytes):
            lang = lang.encode('utf-8', 'strict')
        if not isinstance(tkey, bytes):
            tkey = tkey.encode('utf-8', 'strict')
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
        self.im_n_frames = None
        self._seq_num = None
        self.rewind_state = None
        self.text_memory = 0

    def check_text_memory(self, chunklen):
        self.text_memory += chunklen
        if self.text_memory > MAX_TEXT_MEMORY:
            raise ValueError('Too much memory used in text chunks: %s>MAX_TEXT_MEMORY' % self.text_memory)

    def save_rewind(self):
        self.rewind_state = {'info':self.im_info.copy(), 
         'tile':self.im_tile, 
         'seq_num':self._seq_num}

    def rewind(self):
        self.im_info = self.rewind_state['info']
        self.im_tile = self.rewind_state['tile']
        self._seq_num = self.rewind_state['seq_num']

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
            else:
                if i8(s[11]):
                    raise SyntaxError('unknown filter category')
                return s

    def chunk_IDAT(self, pos, length):
        if 'bbox' in self.im_info:
            tile = [
             (
              'zip', self.im_info['bbox'], pos, self.im_rawmode)]
        else:
            if self.im_n_frames is not None:
                self.im_info['default_image'] = True
            tile = [
             (
              'zip', (0, 0) + self.im_size, pos, self.im_rawmode)]
        self.im_tile = tile
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
        elif unit == 0:
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
            else:
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
                else:
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
                        else:
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
        if self.im_n_frames is not None:
            self.im_n_frames = None
            warnings.warn('Invalid APNG, will use default PNG image if possible')
            return s
        n_frames = i32(s)
        if n_frames == 0 or (n_frames > 2147483648):
            warnings.warn('Invalid APNG, will use default PNG image if possible')
            return s
        self.im_n_frames = n_frames
        self.im_info['loop'] = i32(s[4:])
        self.im_custom_mimetype = 'image/apng'
        return s

    def chunk_fcTL(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        seq = i32(s)
        if not (self._seq_num is None and seq != 0):
            if not self._seq_num is not None or self._seq_num != seq - 1:
                raise SyntaxError('APNG contains frame sequence errors')
            self._seq_num = seq
            width, height = i32(s[4:]), i32(s[8:])
            px, py = i32(s[12:]), i32(s[16:])
            im_w, im_h = self.im_size
            if px + width > im_w or (py + height > im_h):
                raise SyntaxError('APNG contains invalid frames')
            self.im_info['bbox'] = (
             px, py, px + width, py + height)
            delay_num, delay_den = i16(s[20:]), i16(s[22:])
            if delay_den == 0:
                delay_den = 100
            self.im_info['duration'] = float(delay_num) / float(delay_den) * 1000
            self.im_info['disposal'] = i8(s[24])
            self.im_info['blend'] = i8(s[25])
            return s

    def chunk_fdAT(self, pos, length):
        s = ImageFile._safe_read(self.fp, 4)
        seq = i32(s)
        if self._seq_num != seq - 1:
            raise SyntaxError('APNG contains frame sequence errors')
        self._seq_num = seq
        return self.chunk_IDAT(pos + 4, length - 4)


def _accept(prefix):
    return prefix[:8] == _MAGIC


class PngImageFile(ImageFile.ImageFile):
    format = 'PNG'
    format_description = 'Portable network graphics'

    def _open(self):
        if self.fp.read(8) != _MAGIC:
            raise SyntaxError('not a PNG file')
        self._PngImageFile__fp = self.fp
        self._PngImageFile__frame = 0
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
        self.n_frames = self.png.im_n_frames or 1
        self.default_image = self.info.get('default_image', False)
        if self.png.im_palette:
            rawmode, data = self.png.im_palette
            self.palette = ImagePalette.raw(rawmode, data)
        if cid == b'fdAT':
            self._PngImageFile__prepare_idat = length - 4
        else:
            self._PngImageFile__prepare_idat = length
        if self.png.im_n_frames is not None:
            self._close_exclusive_fp_after_loading = False
            self.png.save_rewind()
            self._PngImageFile__rewind_idat = self._PngImageFile__prepare_idat
            self._PngImageFile__rewind = self._PngImageFile__fp.tell()
            if self.default_image:
                self.n_frames += 1
            self._seek(0)
        self.is_animated = self.n_frames > 1

    @property
    def text(self):
        if self._text is None:
            if self.is_animated:
                frame = self._PngImageFile__frame
                self.seek(self.n_frames - 1)
            self.load()
            if self.is_animated:
                self.seek(frame)
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

    def seek(self, frame):
        if not self._seek_check(frame):
            return
        if frame < self._PngImageFile__frame:
            self._seek(0, True)
        last_frame = self._PngImageFile__frame
        for f in range(self._PngImageFile__frame + 1, frame + 1):
            try:
                self._seek(f)
            except EOFError:
                self.seek(last_frame)
                raise EOFError('no more images in APNG file')

    def _seek(self, frame, rewind=False):
        if frame == 0:
            if rewind:
                self._PngImageFile__fp.seek(self._PngImageFile__rewind)
                self.png.rewind()
                self._PngImageFile__prepare_idat = self._PngImageFile__rewind_idat
                self.im = None
                if self.pyaccess:
                    self.pyaccess = None
                self.info = self.png.im_info
                self.tile = self.png.im_tile
                self.fp = self._PngImageFile__fp
            self._prev_im = None
            self.dispose = None
            self.default_image = self.info.get('default_image', False)
            self.dispose_op = self.info.get('disposal')
            self.blend_op = self.info.get('blend')
            self.dispose_extent = self.info.get('bbox')
            self._PngImageFile__frame = 0
            return
        if frame != self._PngImageFile__frame + 1:
            raise ValueError('cannot seek to frame %d' % frame)
        self.load()
        self.fp = self._PngImageFile__fp
        if self._PngImageFile__prepare_idat:
            ImageFile._safe_read(self.fp, self._PngImageFile__prepare_idat)
            self._PngImageFile__prepare_idat = 0
        frame_start = False
        while True:
            self.fp.read(4)
            try:
                cid, pos, length = self.png.read()
            except (struct.error, SyntaxError):
                break

            if cid == b'IEND':
                raise EOFError('No more images in APNG file')
            else:
                if cid == b'fcTL':
                    if frame_start:
                        raise SyntaxError('APNG missing frame data')
                    frame_start = True
                try:
                    self.png.call(cid, pos, length)
                except UnicodeDecodeError:
                    break
                except EOFError:
                    if cid == b'fdAT':
                        length -= 4
                        if frame_start:
                            self._PngImageFile__prepare_idat = length
                            break
                    ImageFile._safe_read(self.fp, length)
                except AttributeError:
                    logger.debug('%r %s %s (unknown)', cid, pos, length)
                    ImageFile._safe_read(self.fp, length)

        self._PngImageFile__frame = frame
        self.tile = self.png.im_tile
        self.dispose_op = self.info.get('disposal')
        self.blend_op = self.info.get('blend')
        self.dispose_extent = self.info.get('bbox')
        if not self.tile:
            raise EOFError

    def tell(self):
        return self._PngImageFile__frame

    def load_prepare(self):
        """internal: prepare to read PNG file"""
        if self.info.get('interlace'):
            self.decoderconfig = self.decoderconfig + (1, )
        self._PngImageFile__idat = self._PngImageFile__prepare_idat
        ImageFile.ImageFile.load_prepare(self)

    def load_read--- This code section failed: ---
              0_0  COME_FROM           134  '134'
              0_1  COME_FROM           126  '126'

 L. 833         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _PngImageFile__idat
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   136  'to 136'

 L. 836        10  LOAD_FAST                'self'
               12  LOAD_ATTR                fp
               14  LOAD_METHOD              read
               16  LOAD_CONST               4
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 838        22  LOAD_FAST                'self'
               24  LOAD_ATTR                png
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  UNPACK_SEQUENCE_3     3 
               32  STORE_FAST               'cid'
               34  STORE_FAST               'pos'
               36  STORE_FAST               'length'

 L. 840        38  LOAD_FAST                'cid'
               40  LOAD_CONST               (b'IDAT', b'DDAT', b'fdAT')
               42  COMPARE_OP               not-in
               44  POP_JUMP_IF_FALSE    66  'to 66'

 L. 841        46  LOAD_FAST                'self'
               48  LOAD_ATTR                png
               50  LOAD_METHOD              push
               52  LOAD_FAST                'cid'
               54  LOAD_FAST                'pos'
               56  LOAD_FAST                'length'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 842        62  LOAD_CONST               b''
               64  RETURN_VALUE     
             66_0  COME_FROM            44  '44'

 L. 844        66  LOAD_FAST                'cid'
               68  LOAD_CONST               b'fdAT'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE   128  'to 128'

 L. 845        74  SETUP_FINALLY        96  'to 96'

 L. 846        76  LOAD_FAST                'self'
               78  LOAD_ATTR                png
               80  LOAD_METHOD              call
               82  LOAD_FAST                'cid'
               84  LOAD_FAST                'pos'
               86  LOAD_FAST                'length'
               88  CALL_METHOD_3         3  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_FORWARD        116  'to 116'
             96_0  COME_FROM_FINALLY    74  '74'

 L. 847        96  DUP_TOP          
               98  LOAD_GLOBAL              EOFError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   114  'to 114'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 848       110  POP_EXCEPT       
              112  BREAK_LOOP          116  'to 116'
            114_0  COME_FROM           102  '102'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            94  '94'

 L. 849       116  LOAD_FAST                'length'
              118  LOAD_CONST               4
              120  BINARY_SUBTRACT  
              122  LOAD_FAST                'self'
              124  STORE_ATTR               _PngImageFile__idat
              126  JUMP_BACK             0  'to 0'
            128_0  COME_FROM            72  '72'

 L. 851       128  LOAD_FAST                'length'
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _PngImageFile__idat
              134  JUMP_BACK             0  'to 0'
            136_0  COME_FROM             8  '8'

 L. 854       136  LOAD_FAST                'read_bytes'
              138  LOAD_CONST               0
              140  COMPARE_OP               <=
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L. 855       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _PngImageFile__idat
              148  STORE_FAST               'read_bytes'
              150  JUMP_FORWARD        164  'to 164'
            152_0  COME_FROM           142  '142'

 L. 857       152  LOAD_GLOBAL              min
              154  LOAD_FAST                'read_bytes'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _PngImageFile__idat
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'read_bytes'
            164_0  COME_FROM           150  '150'

 L. 859       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _PngImageFile__idat
              168  LOAD_FAST                'read_bytes'
              170  BINARY_SUBTRACT  
              172  LOAD_FAST                'self'
              174  STORE_ATTR               _PngImageFile__idat

 L. 861       176  LOAD_FAST                'self'
              178  LOAD_ATTR                fp
              180  LOAD_METHOD              read
              182  LOAD_FAST                'read_bytes'
              184  CALL_METHOD_1         1  ''
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 114

    def load_end(self):
        """internal: finished reading image data"""
        while True:
            self.fp.read(4)
            try:
                cid, pos, length = self.png.read()
            except (struct.error, SyntaxError):
                break
            else:
                if cid == b'IEND':
                    pass
                else:
                    break
                if cid == b'fcTL':
                    if self.is_animated:
                        self._PngImageFile__prepare_idat = 0
                        self.png.push(cid, pos, length)
                    else:
                        pass
            try:
                self.png.call(cid, pos, length)
            except UnicodeDecodeError:
                break
            except EOFError:
                if cid == b'fdAT':
                    length -= 4
                else:
                    ImageFile._safe_read(self.fp, length)
            except AttributeError:
                logger.debug('%r %s %s (unknown)', cid, pos, length)
                ImageFile._safe_read(self.fp, length)

        self._text = self.png.im_text
        if not self.is_animated:
            self.png.close()
            self.png = None
        else:
            if self._prev_im is None:
                if self.dispose_op == APNG_DISPOSE_OP_PREVIOUS:
                    self.dispose_op = APNG_DISPOSE_OP_BACKGROUND
            if self.dispose_op == APNG_DISPOSE_OP_PREVIOUS:
                dispose = self._prev_im.copy()
                dispose = self._crop(dispose, self.dispose_extent)
            elif self.dispose_op == APNG_DISPOSE_OP_BACKGROUND:
                dispose = Image.core.fill('RGBA', self.size, (0, 0, 0, 0))
                dispose = self._crop(dispose, self.dispose_extent)
            else:
                dispose = None
            if self._prev_im:
                if self.blend_op == APNG_BLEND_OP_OVER:
                    updated = self._crop(self.im, self.dispose_extent)
                    self._prev_im.paste(updated, self.dispose_extent, updated.convert('RGBA'))
                    self.im = self._prev_im
                    if self.pyaccess:
                        self.pyaccess = None
            self._prev_im = self.im.copy()
            if dispose:
                self._prev_im.paste(dispose, self.dispose_extent)

    def _getexif(self):
        if 'exif' not in self.info:
            self.load()
        if 'exif' not in self.info:
            if 'Raw profile type exif' not in self.info:
                return
        return dict(self.getexif())

    def getexif(self):
        if 'exif' not in self.info:
            self.load()
        if self._exif is None:
            self._exif = Image.Exif()
        exif_info = self.info.get('exif')
        if exif_info is None:
            if 'Raw profile type exif' in self.info:
                exif_info = bytes.fromhex(''.join(self.info['Raw profile type exif'].split('\n')[3:]))
        self._exif.load(exif_info)
        return self._exif

    def _close__fp(self):
        try:
            try:
                if self._PngImageFile__fp != self.fp:
                    self._PngImageFile__fp.close()
            except AttributeError:
                pass

        finally:
            self._PngImageFile__fp = None


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


class _fdat:

    def __init__(self, fp, chunk, seq_num):
        self.fp = fp
        self.chunk = chunk
        self.seq_num = seq_num

    def write(self, data):
        self.chunk(self.fp, b'fdAT', o32(self.seq_num), data)
        self.seq_num += 1


def _write_multiple_frames(im, fp, chunk, rawmode):
    default_image = im.encoderinfo.get('default_image', im.info.get('default_image'))
    duration = im.encoderinfo.get('duration', im.info.get('duration', 0))
    loop = im.encoderinfo.get('loop', im.info.get('loop', 0))
    disposal = im.encoderinfo.get('disposal', im.info.get('disposal'))
    blend = im.encoderinfo.get('blend', im.info.get('blend'))
    if default_image:
        chain = itertools.chain(im.encoderinfo.get('append_images', []))
    else:
        chain = itertools.chain([im], im.encoderinfo.get('append_images', []))
    im_frames = []
    frame_count = 0
    for im_seq in chain:
        for im_frame in ImageSequence.Iterator(im_seq):
            im_frame = im_frame.copy()
            if im_frame.mode != im.mode:
                if im.mode == 'P':
                    im_frame = im_frame.convert((im.mode), palette=(im.palette))
                else:
                    im_frame = im_frame.convert(im.mode)
            encoderinfo = im.encoderinfo.copy()
            if isinstance(duration, (list, tuple)):
                encoderinfo['duration'] = duration[frame_count]
            if isinstance(disposal, (list, tuple)):
                encoderinfo['disposal'] = disposal[frame_count]
            if isinstance(blend, (list, tuple)):
                encoderinfo['blend'] = blend[frame_count]
            frame_count += 1
            if im_frames:
                previous = im_frames[(-1)]
                prev_disposal = previous['encoderinfo'].get('disposal')
                prev_blend = previous['encoderinfo'].get('blend')
                if prev_disposal == APNG_DISPOSE_OP_PREVIOUS:
                    if len(im_frames) < 2:
                        prev_disposal == APNG_DISPOSE_OP_BACKGROUND
                if prev_disposal == APNG_DISPOSE_OP_BACKGROUND:
                    base_im = previous['im']
                    dispose = Image.core.fill('RGBA', im.size, (0, 0, 0, 0))
                    bbox = previous['bbox']
                    if bbox:
                        dispose = dispose.crop(bbox)
                    else:
                        bbox = (0, 0) + im.size
                    base_im.paste(dispose, bbox)
                elif prev_disposal == APNG_DISPOSE_OP_PREVIOUS:
                    base_im = im_frames[(-2)]['im']
                else:
                    base_im = previous['im']
                delta = ImageChops.subtract_modulo(im_frame.convert('RGB'), base_im.convert('RGB'))
                bbox = delta.getbbox()
                if not bbox:
                    if not prev_disposal == encoderinfo.get('disposal') or prev_blend == encoderinfo.get('blend'):
                        duration = encoderinfo.get('duration', 0)
                        if duration:
                            if 'duration' in previous['encoderinfo']:
                                previous['encoderinfo']['duration'] += duration
                            else:
                                previous['encoderinfo']['duration'] = duration
            else:
                bbox = None
            im_frames.append({'im':im_frame,  'bbox':bbox,  'encoderinfo':encoderinfo})

    else:
        chunk(fp, b'acTL', o32(len(im_frames)), o32(loop))
        if default_image:
            ImageFile._save(im, _idat(fp, chunk), [('zip', (0, 0) + im.size, 0, rawmode)])
        seq_num = 0
        for frame, frame_data in enumerate(im_frames):
            im_frame = frame_data['im']
            if not frame_data['bbox']:
                bbox = (0, 0) + im_frame.size
            else:
                bbox = frame_data['bbox']
                im_frame = im_frame.crop(bbox)
            size = im_frame.size
            duration = int(round(frame_data['encoderinfo'].get('duration', 0)))
            disposal = frame_data['encoderinfo'].get('disposal', APNG_DISPOSE_OP_NONE)
            blend = frame_data['encoderinfo'].get('blend', APNG_BLEND_OP_SOURCE)
            chunk(fp, b'fcTL', o32(seq_num), o32(size[0]), o32(size[1]), o32(bbox[0]), o32(bbox[1]), o16(duration), o16(1000), o8(disposal), o8(blend))
            seq_num += 1
            if frame == 0:
                if not default_image:
                    ImageFile._save(im_frame, _idat(fp, chunk), [
                     (
                      'zip', (0, 0) + im_frame.size, 0, rawmode)])
                fdat_chunks = _fdat(fp, chunk, seq_num)
                ImageFile._save(im_frame, fdat_chunks, [('zip', (0, 0) + im_frame.size, 0, rawmode)])
                seq_num = fdat_chunks.seq_num


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save(im, fp, filename, chunk=putchunk, save_all=False):
    mode = im.mode
    if mode == 'P':
        if 'bits' in im.encoderinfo:
            colors = 1 << im.encoderinfo['bits']
        elif im.palette:
            colors = max(min(len(im.palette.getdata()[1]) // 3, 256), 2)
        else:
            colors = 256
        if colors <= 2:
            bits = 1
        elif colors <= 4:
            bits = 2
        elif colors <= 16:
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
                else:
                    if cid in chunks_multiple_allowed:
                        chunk(fp, cid, data)
            else:
                if im.mode == 'P':
                    palette_byte_number = 2 ** bits * 3
                    palette_bytes = im.im.getpalette('RGB')[:palette_byte_number]
                    while True:
                        if len(palette_bytes) < palette_byte_number:
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
                    elif im.mode in ('1', 'L', 'I'):
                        transparency = max(0, min(65535, transparency))
                        chunk(fp, b'tRNS', o16(transparency))
                    elif im.mode == 'RGB':
                        red, green, blue = transparency
                        chunk(fp, b'tRNS', o16(red) + o16(green) + o16(blue))
                    elif 'transparency' in im.encoderinfo:
                        raise OSError('cannot use transparency for this mode')
                elif im.mode == 'P':
                    if im.im.getpalettemode() == 'RGBA':
                        alpha = im.im.getpalette('RGBA', 'A')
                        alpha_bytes = 2 ** bits
                        chunk(fp, b'tRNS', alpha[:alpha_bytes])
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
            else:
                exif = im.encoderinfo.get('exif', im.info.get('exif'))
                if exif:
                    if isinstance(exif, Image.Exif):
                        exif = exif.tobytes(8)
                    if exif.startswith(b'Exif\x00\x00'):
                        exif = exif[6:]
                    chunk(fp, b'eXIf', exif)
                if save_all:
                    _write_multiple_frames(im, fp, chunk, rawmode)
                else:
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
Image.register_save_all(PngImageFile.format, _save_all)
Image.register_extensions(PngImageFile.format, ['.png', '.apng'])
Image.register_mime(PngImageFile.format, 'image/png')