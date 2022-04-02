# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\BlpImagePlugin.py
"""
Blizzard Mipmap Format (.blp)
Jerome Leclanche <jerome@leclan.ch>

The contents of this file are hereby released in the public domain (CC0)
Full text of the CC0 license:
  https://creativecommons.org/publicdomain/zero/1.0/

BLP1 files, used mostly in Warcraft III, are not fully supported.
All types of BLP2 files used in World of Warcraft are supported.

The BLP file structure consists of a header, up to 16 mipmaps of the
texture

Texture sizes must be powers of two, though the two dimensions do
not have to be equal; 512x256 is valid, but 512x200 is not.
The first mipmap (mipmap #0) is the full size image; each subsequent
mipmap halves both dimensions. The final mipmap should be 1x1.

BLP files come in many different flavours:
* JPEG-compressed (type == 0) - only supported for BLP1.
* RAW images (type == 1, encoding == 1). Each mipmap is stored as an
  array of 8-bit values, one per pixel, left to right, top to bottom.
  Each value is an index to the palette.
* DXT-compressed (type == 1, encoding == 2):
- DXT1 compression is used if alpha_encoding == 0.
  - An additional alpha bit is used if alpha_depth == 1.
  - DXT3 compression is used if alpha_encoding == 1.
  - DXT5 compression is used if alpha_encoding == 7.
"""
import struct
from io import BytesIO
from . import Image, ImageFile
BLP_FORMAT_JPEG = 0
BLP_ENCODING_UNCOMPRESSED = 1
BLP_ENCODING_DXT = 2
BLP_ENCODING_UNCOMPRESSED_RAW_BGRA = 3
BLP_ALPHA_ENCODING_DXT1 = 0
BLP_ALPHA_ENCODING_DXT3 = 1
BLP_ALPHA_ENCODING_DXT5 = 7

def unpack_565(i):
    return (
     (i >> 11 & 31) << 3, (i >> 5 & 63) << 2, (i & 31) << 3)


def decode_dxt1(data, alpha=False):
    """
    input: one "row" of data (i.e. will produce 4*width pixels)
    """
    blocks = len(data) // 8
    ret = (bytearray(), bytearray(), bytearray(), bytearray())
    for block in range(blocks):
        idx = block * 8
        color0, color1, bits = struct.unpack_from('<HHI', data, idx)
        r0, g0, b0 = unpack_565(color0)
        r1, g1, b1 = unpack_565(color1)
        for j in range(4):
            for i in range(4):
                control = bits & 3
                bits = bits >> 2
                a = 255
                if control == 0:
                    r, g, b = r0, g0, b0
                elif control == 1:
                    r, g, b = r1, g1, b1
                elif control == 2:
                    if color0 > color1:
                        r = (2 * r0 + r1) // 3
                        g = (2 * g0 + g1) // 3
                        b = (2 * b0 + b1) // 3
                    else:
                        r = (r0 + r1) // 2
                        g = (g0 + g1) // 2
                        b = (b0 + b1) // 2
                elif control == 3:
                    if color0 > color1:
                        r = (2 * r1 + r0) // 3
                        g = (2 * g1 + g0) // 3
                        b = (2 * b1 + b0) // 3
                    else:
                        r, g, b, a = (0, 0, 0, 0)
                if alpha:
                    ret[j].extend([r, g, b, a])
                else:
                    ret[j].extend([r, g, b])

        else:
            return ret


def decode_dxt3(data):
    """
    input: one "row" of data (i.e. will produce 4*width pixels)
    """
    blocks = len(data) // 16
    ret = (bytearray(), bytearray(), bytearray(), bytearray())
    for block in range(blocks):
        idx = block * 16
        block = data[idx:idx + 16]
        bits = struct.unpack_from('<8B', block)
        color0, color1 = struct.unpack_from('<HH', block, 8)
        code, = struct.unpack_from('<I', block, 12)
        r0, g0, b0 = unpack_565(color0)
        r1, g1, b1 = unpack_565(color1)
        for j in range(4):
            high = False
            for i in range(4):
                alphacode_index = (4 * j + i) // 2
                a = bits[alphacode_index]
                if high:
                    high = False
                    a >>= 4
                else:
                    high = True
                    a &= 15
                a *= 17
                color_code = code >> 2 * (4 * j + i) & 3
                if color_code == 0:
                    r, g, b = r0, g0, b0
                elif color_code == 1:
                    r, g, b = r1, g1, b1
                elif color_code == 2:
                    r = (2 * r0 + r1) // 3
                    g = (2 * g0 + g1) // 3
                    b = (2 * b0 + b1) // 3
                elif color_code == 3:
                    r = (2 * r1 + r0) // 3
                    g = (2 * g1 + g0) // 3
                    b = (2 * b1 + b0) // 3
                ret[j].extend([r, g, b, a])

    else:
        return ret


def decode_dxt5(data):
    """
    input: one "row" of data (i.e. will produce 4 * width pixels)
    """
    blocks = len(data) // 16
    ret = (bytearray(), bytearray(), bytearray(), bytearray())
    for block in range(blocks):
        idx = block * 16
        block = data[idx:idx + 16]
        a0, a1 = struct.unpack_from('<BB', block)
        bits = struct.unpack_from('<6B', block, 2)
        alphacode1 = bits[2] | bits[3] << 8 | bits[4] << 16 | bits[5] << 24
        alphacode2 = bits[0] | bits[1] << 8
        color0, color1 = struct.unpack_from('<HH', block, 8)
        code, = struct.unpack_from('<I', block, 12)
        r0, g0, b0 = unpack_565(color0)
        r1, g1, b1 = unpack_565(color1)
        for j in range(4):
            for i in range(4):
                alphacode_index = 3 * (4 * j + i)
                if alphacode_index <= 12:
                    alphacode = alphacode2 >> alphacode_index & 7
                elif alphacode_index == 15:
                    alphacode = alphacode2 >> 15 | alphacode1 << 1 & 6
                else:
                    alphacode = alphacode1 >> alphacode_index - 16 & 7
                if alphacode == 0:
                    a = a0
                elif alphacode == 1:
                    a = a1
                elif a0 > a1:
                    a = ((8 - alphacode) * a0 + (alphacode - 1) * a1) // 7
                elif alphacode == 6:
                    a = 0
                elif alphacode == 7:
                    a = 255
                else:
                    a = ((6 - alphacode) * a0 + (alphacode - 1) * a1) // 5
                color_code = code >> 2 * (4 * j + i) & 3
                if color_code == 0:
                    r, g, b = r0, g0, b0
                elif color_code == 1:
                    r, g, b = r1, g1, b1
                elif color_code == 2:
                    r = (2 * r0 + r1) // 3
                    g = (2 * g0 + g1) // 3
                    b = (2 * b0 + b1) // 3
                elif color_code == 3:
                    r = (2 * r1 + r0) // 3
                    g = (2 * g1 + g0) // 3
                    b = (2 * b1 + b0) // 3
                ret[j].extend([r, g, b, a])

    else:
        return ret


class BLPFormatError(NotImplementedError):
    pass


class BlpImageFile(ImageFile.ImageFile):
    __doc__ = '\n    Blizzard Mipmap Format\n    '
    format = 'BLP'
    format_description = 'Blizzard Mipmap Format'

    def _open(self):
        self.magic = self.fp.read(4)
        self._read_blp_header()
        if self.magic == b'BLP1':
            decoder = 'BLP1'
            self.mode = 'RGB'
        elif self.magic == b'BLP2':
            decoder = 'BLP2'
            self.mode = 'RGBA' if self._blp_alpha_depth else 'RGB'
        else:
            raise BLPFormatError(f"Bad BLP magic {repr(self.magic)}")
        self.tile = [(decoder, (0, 0) + self.size, 0, (self.mode, 0, 1))]

    def _read_blp_header(self):
        self._blp_compression, = struct.unpack('<i', self.fp.read(4))
        self._blp_encoding, = struct.unpack('<b', self.fp.read(1))
        self._blp_alpha_depth, = struct.unpack('<b', self.fp.read(1))
        self._blp_alpha_encoding, = struct.unpack('<b', self.fp.read(1))
        self._blp_mips, = struct.unpack('<b', self.fp.read(1))
        self._size = struct.unpack('<II', self.fp.read(8))
        if self.magic == b'BLP1':
            self._blp_encoding, = struct.unpack('<i', self.fp.read(4))
            self._blp_subtype, = struct.unpack('<i', self.fp.read(4))
        self._blp_offsets = struct.unpack('<16I', self.fp.read(64))
        self._blp_lengths = struct.unpack('<16I', self.fp.read(64))


class _BLPBaseDecoder(ImageFile.PyDecoder):
    _pulls_fd = True

    def decode(self, buffer):
        try:
            self.fd.seek(0)
            self.magic = self.fd.read(4)
            self._read_blp_header()
            self._load()
        except struct.error as e:
            try:
                raise OSError('Truncated Blp file') from e
            finally:
                e = None
                del e

        else:
            return (0, 0)

    def _read_palette--- This code section failed: ---

 L. 290         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L. 291         4  LOAD_GLOBAL              range
                6  LOAD_CONST               256
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM            96  '96'
               12  FOR_ITER             98  'to 98'
               14  STORE_FAST               'i'

 L. 292        16  SETUP_FINALLY        50  'to 50'

 L. 293        18  LOAD_GLOBAL              struct
               20  LOAD_METHOD              unpack
               22  LOAD_STR                 '<4B'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                fd
               28  LOAD_METHOD              read
               30  LOAD_CONST               4
               32  CALL_METHOD_1         1  ''
               34  CALL_METHOD_2         2  ''
               36  UNPACK_SEQUENCE_4     4 
               38  STORE_FAST               'b'
               40  STORE_FAST               'g'
               42  STORE_FAST               'r'
               44  STORE_FAST               'a'
               46  POP_BLOCK        
               48  JUMP_FORWARD         78  'to 78'
             50_0  COME_FROM_FINALLY    16  '16'

 L. 294        50  DUP_TOP          
               52  LOAD_GLOBAL              struct
               54  LOAD_ATTR                error
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    76  'to 76'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 295        66  POP_EXCEPT       
               68  POP_TOP          
               70  JUMP_FORWARD         98  'to 98'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            58  '58'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            48  '48'

 L. 296        78  LOAD_FAST                'ret'
               80  LOAD_METHOD              append
               82  LOAD_FAST                'b'
               84  LOAD_FAST                'g'
               86  LOAD_FAST                'r'
               88  LOAD_FAST                'a'
               90  BUILD_TUPLE_4         4 
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  JUMP_BACK            12  'to 12'
             98_0  COME_FROM            70  '70'
             98_1  COME_FROM            12  '12'

 L. 297        98  LOAD_FAST                'ret'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 70

    def _read_blp_header(self):
        self._blp_compression, = struct.unpack('<i', self.fd.read(4))
        self._blp_encoding, = struct.unpack('<b', self.fd.read(1))
        self._blp_alpha_depth, = struct.unpack('<b', self.fd.read(1))
        self._blp_alpha_encoding, = struct.unpack('<b', self.fd.read(1))
        self._blp_mips, = struct.unpack('<b', self.fd.read(1))
        self.size = struct.unpack('<II', self.fd.read(8))
        if self.magic == b'BLP1':
            self._blp_encoding, = struct.unpack('<i', self.fd.read(4))
            self._blp_subtype, = struct.unpack('<i', self.fd.read(4))
        self._blp_offsets = struct.unpack('<16I', self.fd.read(64))
        self._blp_lengths = struct.unpack('<16I', self.fd.read(64))


class BLP1Decoder(_BLPBaseDecoder):

    def _load(self):
        if self._blp_compression == BLP_FORMAT_JPEG:
            self._decode_jpeg_stream()
        elif self._blp_compression == 1:
            if self._blp_encoding in (4, 5):
                data = bytearray()
                palette = self._read_palette()
                _data = BytesIO(self.fd.read(self._blp_lengths[0]))
                while True:
                    try:
                        offset, = struct.unpack('<B', _data.read(1))
                    except struct.error:
                        break
                    else:
                        b, g, r, a = palette[offset]
                        data.extend([r, g, b])

                self.set_as_raw(bytes(data))
            else:
                raise BLPFormatError(f"Unsupported BLP encoding {repr(self._blp_encoding)}")
        else:
            raise BLPFormatError(f"Unsupported BLP compression {repr(self._blp_encoding)}")

    def _decode_jpeg_stream(self):
        from PIL.JpegImagePlugin import JpegImageFile
        jpeg_header_size, = struct.unpack('<I', self.fd.read(4))
        jpeg_header = self.fd.read(jpeg_header_size)
        self.fd.read(self._blp_offsets[0] - self.fd.tell())
        data = self.fd.read(self._blp_lengths[0])
        data = jpeg_header + data
        data = BytesIO(data)
        image = JpegImageFile(data)
        self.tile = image.tile
        self.fd = image.fp
        self.mode = image.mode


class BLP2Decoder(_BLPBaseDecoder):

    def _load(self):
        palette = self._read_palette()
        data = bytearray()
        self.fd.seek(self._blp_offsets[0])
        if self._blp_compression == 1:
            if self._blp_encoding == BLP_ENCODING_UNCOMPRESSED:
                _data = BytesIO(self.fd.read(self._blp_lengths[0]))
                while True:
                    try:
                        offset, = struct.unpack('<B', _data.read(1))
                    except struct.error:
                        break
                    else:
                        b, g, r, a = palette[offset]
                        data.extend((r, g, b))

            elif self._blp_encoding == BLP_ENCODING_DXT:
                if self._blp_alpha_encoding == BLP_ALPHA_ENCODING_DXT1:
                    linesize = (self.size[0] + 3) // 4 * 8
                    for yb in range((self.size[1] + 3) // 4):
                        for d in decode_dxt1((self.fd.read(linesize)),
                          alpha=(bool(self._blp_alpha_depth))):
                            data += d

                elif self._blp_alpha_encoding == BLP_ALPHA_ENCODING_DXT3:
                    linesize = (self.size[0] + 3) // 4 * 16
                    for yb in range((self.size[1] + 3) // 4):
                        for d in decode_dxt3(self.fd.read(linesize)):
                            data += d

                elif self._blp_alpha_encoding == BLP_ALPHA_ENCODING_DXT5:
                    linesize = (self.size[0] + 3) // 4 * 16
                    for yb in range((self.size[1] + 3) // 4):
                        for d in decode_dxt5(self.fd.read(linesize)):
                            data += d

                else:
                    raise BLPFormatError(f"Unsupported alpha encoding {repr(self._blp_alpha_encoding)}")
            else:
                raise BLPFormatError(f"Unknown BLP encoding {repr(self._blp_encoding)}")
        else:
            raise BLPFormatError(f"Unknown BLP compression {repr(self._blp_compression)}")
        self.set_as_raw(bytes(data))


Image.register_open(BlpImageFile.format, BlpImageFile, lambda p: p[:4] in (b'BLP1', b'BLP2'))
Image.register_extension(BlpImageFile.format, '.blp')
Image.register_decoder('BLP1', BLP1Decoder)
Image.register_decoder('BLP2', BLP2Decoder)