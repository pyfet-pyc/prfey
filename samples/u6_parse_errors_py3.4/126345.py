# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
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
_MODES = {(1, 0): (
          '1', '1'), 
 (2, 0): (
          'L', 'L;2'), 
 (4, 0): (
          'L', 'L;4'), 
 (8, 0): (
          'L', 'L'), 
 (16, 0): (
           'I', 'I;16B'), 
 (8, 2): (
          'RGB', 'RGB'), 
 (16, 2): (
           'RGB', 'RGB;16B'), 
 (1, 3): (
          'P', 'P;1'), 
 (2, 3): (
          'P', 'P;2'), 
 (4, 3): (
          'P', 'P;4'), 
 (8, 3): (
          'P', 'P'), 
 (8, 4): (
          'LA', 'LA'), 
 (16, 4): (
           'RGBA', 'LA;16B'), 
 (8, 6): (
          'RGBA', 'RGBA'), 
 (16, 6): (
           'RGBA', 'RGBA;16B')}
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
        if ImageFile.LOAD_TRUNCATED_IMAGES and i8(cid[0]) >> 5 & 1:
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
            return self.add_itxt(key, value, value.lang, value.tkey, zip=zip)
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

        self.im_info['icc_profile'] = icc_profile
        return s

    def chunk_IHDR(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_size = (i32(s), i32(s[4:]))
        try:
            self.im_mode, self.im_rawmode = _MODES[(i8(s[8]), i8(s[9]))]
        except Exception:
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

    def chunk_tRNS(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == 'P':
            if _simple_palette.match(s):
                i = s.find(b'\x00')
                if i >= 0:
                    self.im_info['transparency'] = i
            else:
                self.im_info['transparency'] = s
        else:
            if self.im_mode == 'L':
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

    def chunk_iTXt--- This code section failed: ---

 L. 491         0  LOAD_GLOBAL              ImageFile
                3  LOAD_ATTR                _safe_read
                6  LOAD_FAST                'self'
                9  LOAD_ATTR                fp
               12  LOAD_FAST                'length'
               15  CALL_FUNCTION_2       2  '2 positional, 0 named'
               18  DUP_TOP          
               19  STORE_FAST               'r'
               22  STORE_FAST               's'

 L. 492        25  SETUP_EXCEPT         56  'to 56'

 L. 493        28  LOAD_FAST                'r'
               31  LOAD_ATTR                split
               34  LOAD_CONST               b'\x00'
               37  LOAD_CONST               1
               40  CALL_FUNCTION_2       2  '2 positional, 0 named'
               43  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'k'
               49  STORE_FAST               'r'
               52  POP_BLOCK        
               53  JUMP_FORWARD         78  'to 78'
             56_0  COME_FROM_EXCEPT     25  '25'

 L. 494        56  DUP_TOP          
               57  LOAD_GLOBAL              ValueError
               60  COMPARE_OP               exception-match
               63  POP_JUMP_IF_FALSE    77  'to 77'
               66  POP_TOP          
               67  POP_TOP          
               68  POP_TOP          

 L. 495        69  LOAD_FAST                's'
               72  RETURN_VALUE     
               73  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
               77  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            53  '53'

 L. 496        78  LOAD_GLOBAL              len
               81  LOAD_FAST                'r'
               84  CALL_FUNCTION_1       1  '1 positional, 0 named'
               87  LOAD_CONST               2
               90  COMPARE_OP               <
               93  POP_JUMP_IF_FALSE   100  'to 100'

 L. 497        96  LOAD_FAST                's'
               99  RETURN_END_IF    
            100_0  COME_FROM            93  '93'

 L. 498       100  LOAD_GLOBAL              i8
              103  LOAD_FAST                'r'
              106  LOAD_CONST               0
              109  BINARY_SUBSCR    
              110  CALL_FUNCTION_1       1  '1 positional, 0 named'
              113  LOAD_GLOBAL              i8
              116  LOAD_FAST                'r'
              119  LOAD_CONST               1
              122  BINARY_SUBSCR    
              123  CALL_FUNCTION_1       1  '1 positional, 0 named'
              126  LOAD_FAST                'r'
              129  LOAD_CONST               2
              132  LOAD_CONST               None
              135  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              139  ROT_THREE        
              140  ROT_TWO          
              141  STORE_FAST               'cf'
              144  STORE_FAST               'cm'
              147  STORE_FAST               'r'

 L. 499       150  SETUP_EXCEPT        184  'to 184'

 L. 500       153  LOAD_FAST                'r'
              156  LOAD_ATTR                split
              159  LOAD_CONST               b'\x00'
              162  LOAD_CONST               2
              165  CALL_FUNCTION_2       2  '2 positional, 0 named'
              168  UNPACK_SEQUENCE_3     3 
              171  STORE_FAST               'lang'
              174  STORE_FAST               'tk'
              177  STORE_FAST               'v'
              180  POP_BLOCK        
              181  JUMP_FORWARD        206  'to 206'
            184_0  COME_FROM_EXCEPT    150  '150'

 L. 501       184  DUP_TOP          
              185  LOAD_GLOBAL              ValueError
              188  COMPARE_OP               exception-match
              191  POP_JUMP_IF_FALSE   205  'to 205'
              194  POP_TOP          
              195  POP_TOP          
              196  POP_TOP          

 L. 502       197  LOAD_FAST                's'
              200  RETURN_VALUE     
              201  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
              205  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           181  '181'

 L. 503       206  LOAD_FAST                'cf'
              209  LOAD_CONST               0
              212  COMPARE_OP               !=
              215  POP_JUMP_IF_FALSE   317  'to 317'

 L. 504       218  LOAD_FAST                'cm'
              221  LOAD_CONST               0
              224  COMPARE_OP               ==
              227  POP_JUMP_IF_FALSE   310  'to 310'

 L. 505       230  SETUP_EXCEPT        249  'to 249'

 L. 506       233  LOAD_GLOBAL              _safe_zlib_decompress
              236  LOAD_FAST                'v'
              239  CALL_FUNCTION_1       1  '1 positional, 0 named'
              242  STORE_FAST               'v'
              245  POP_BLOCK        
              246  JUMP_ABSOLUTE       314  'to 314'
            249_0  COME_FROM_EXCEPT    230  '230'

 L. 507       249  DUP_TOP          
              250  LOAD_GLOBAL              ValueError
              253  COMPARE_OP               exception-match
              256  POP_JUMP_IF_FALSE   282  'to 282'
              259  POP_TOP          
              260  POP_TOP          
              261  POP_TOP          

 L. 508       262  LOAD_GLOBAL              ImageFile
              265  LOAD_ATTR                LOAD_TRUNCATED_IMAGES
              268  POP_JUMP_IF_FALSE   275  'to 275'

 L. 509       271  LOAD_FAST                's'
              274  RETURN_END_IF    
            275_0  COME_FROM           268  '268'

 L. 511       275  RAISE_VARARGS_0       0  'reraise'
              278  POP_EXCEPT       
              279  JUMP_ABSOLUTE       314  'to 314'

 L. 512       282  DUP_TOP          
              283  LOAD_GLOBAL              zlib
              286  LOAD_ATTR                error
              289  COMPARE_OP               exception-match
              292  POP_JUMP_IF_FALSE   306  'to 306'
              295  POP_TOP          
              296  POP_TOP          
              297  POP_TOP          

 L. 513       298  LOAD_FAST                's'
              301  RETURN_VALUE     
              302  POP_EXCEPT       
              303  JUMP_ABSOLUTE       314  'to 314'
              306  END_FINALLY      
              307  JUMP_ABSOLUTE       317  'to 317'

 L. 515       310  LOAD_FAST                's'
              313  RETURN_VALUE     
            314_0  COME_FROM_EXCEPT_CLAUSE   279  '279'
              314  JUMP_FORWARD        317  'to 317'
            317_0  COME_FROM           314  '314'

 L. 516       317  LOAD_GLOBAL              py3
              320  POP_JUMP_IF_FALSE   427  'to 427'

 L. 517       323  SETUP_EXCEPT        402  'to 402'

 L. 518       326  LOAD_FAST                'k'
              329  LOAD_ATTR                decode
              332  LOAD_STR                 'latin-1'
              335  LOAD_STR                 'strict'
              338  CALL_FUNCTION_2       2  '2 positional, 0 named'
              341  STORE_FAST               'k'

 L. 519       344  LOAD_FAST                'lang'
              347  LOAD_ATTR                decode
              350  LOAD_STR                 'utf-8'
              353  LOAD_STR                 'strict'
              356  CALL_FUNCTION_2       2  '2 positional, 0 named'
              359  STORE_FAST               'lang'

 L. 520       362  LOAD_FAST                'tk'
              365  LOAD_ATTR                decode
              368  LOAD_STR                 'utf-8'
              371  LOAD_STR                 'strict'
              374  CALL_FUNCTION_2       2  '2 positional, 0 named'
              377  STORE_FAST               'tk'

 L. 521       380  LOAD_FAST                'v'
              383  LOAD_ATTR                decode
              386  LOAD_STR                 'utf-8'
              389  LOAD_STR                 'strict'
              392  CALL_FUNCTION_2       2  '2 positional, 0 named'
              395  STORE_FAST               'v'
              398  POP_BLOCK        
              399  JUMP_ABSOLUTE       427  'to 427'
            402_0  COME_FROM_EXCEPT    323  '323'

 L. 522       402  DUP_TOP          
              403  LOAD_GLOBAL              UnicodeError
              406  COMPARE_OP               exception-match
              409  POP_JUMP_IF_FALSE   423  'to 423'
              412  POP_TOP          
              413  POP_TOP          
              414  POP_TOP          

 L. 523       415  LOAD_FAST                's'
              418  RETURN_VALUE     
              419  POP_EXCEPT       
              420  JUMP_ABSOLUTE       427  'to 427'
              423  END_FINALLY      
              424  JUMP_FORWARD        427  'to 427'
            427_0  COME_FROM           424  '424'

 L. 525       427  LOAD_GLOBAL              iTXt
              430  LOAD_FAST                'v'
              433  LOAD_FAST                'lang'
              436  LOAD_FAST                'tk'
              439  CALL_FUNCTION_3       3  '3 positional, 0 named'
              442  DUP_TOP          
              443  LOAD_FAST                'self'
              446  LOAD_ATTR                im_info
              449  LOAD_FAST                'k'
              452  STORE_SUBSCR     
              453  LOAD_FAST                'self'
              456  LOAD_ATTR                im_text
              459  LOAD_FAST                'k'
              462  STORE_SUBSCR     

 L. 526       463  LOAD_FAST                'self'
              466  LOAD_ATTR                check_text_memory
              469  LOAD_GLOBAL              len
              472  LOAD_FAST                'v'
              475  CALL_FUNCTION_1       1  '1 positional, 0 named'
              478  CALL_FUNCTION_1       1  '1 positional, 0 named'
              481  POP_TOP          

 L. 528       482  LOAD_FAST                's'
              485  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 314

    def chunk_acTL(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        self.im_custom_mimetype = 'image/apng'
        return s

    def chunk_fcTL(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
        return s

    def chunk_fdAT(self, pos, length):
        s = ImageFile._safe_read(self.fp, length)
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
        self._text = None
        self.tile = self.png.im_tile
        self.custom_mimetype = self.png.im_custom_mimetype
        if self.png.im_palette:
            rawmode, data = self.png.im_palette
            self.palette = ImagePalette.raw(rawmode, data)
        self._PngImageFile__idat = length

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
        while True:
            self.fp.read(4)
            try:
                cid, pos, length = self.png.read()
            except (struct.error, SyntaxError):
                break

            if cid == b'IEND':
                break
            try:
                self.png.call(cid, pos, length)
            except UnicodeDecodeError:
                break
            except EOFError:
                ImageFile._safe_read(self.fp, length)

        self._text = self.png.im_text
        self.png.close()
        self.png = None


_OUTMODES = {'1': (
       '1', b'\x01\x00'), 
 'L;1': (
         'L;1', b'\x01\x00'), 
 'L;2': (
         'L;2', b'\x02\x00'), 
 'L;4': (
         'L;4', b'\x04\x00'), 
 'L': (
       'L', b'\x08\x00'), 
 'LA': (
        'LA', b'\x08\x04'), 
 'I': (
       'I;16B', b'\x10\x00'), 
 'P;1': (
         'P;1', b'\x01\x03'), 
 'P;2': (
         'P;2', b'\x02\x03'), 
 'P;4': (
         'P;4', b'\x04\x03'), 
 'P': (
       'P', b'\x08\x03'), 
 'RGB': (
         'RGB', b'\x08\x02'), 
 'RGBA': (
          'RGBA', b'\x08\x06')}

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
                        continue

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
                        elif 'transparency' in im.encoderinfo:
                            raise IOError('cannot use transparency for this mode')
            elif im.mode == 'P':
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
                continue

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
Image.register_extensions(PngImageFile.format, ['.png', '.apng'])
Image.register_mime(PngImageFile.format, 'image/png')