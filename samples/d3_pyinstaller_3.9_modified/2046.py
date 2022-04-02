# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

    def decode--- This code section failed: ---

 L. 280         0  SETUP_FINALLY        48  'to 48'

 L. 281         2  LOAD_FAST                'self'
                4  LOAD_ATTR                fd
                6  LOAD_METHOD              seek
                8  LOAD_CONST               0
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L. 282        14  LOAD_FAST                'self'
               16  LOAD_ATTR                fd
               18  LOAD_METHOD              read
               20  LOAD_CONST               4
               22  CALL_METHOD_1         1  ''
               24  LOAD_FAST                'self'
               26  STORE_ATTR               magic

 L. 283        28  LOAD_FAST                'self'
               30  LOAD_METHOD              _read_blp_header
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L. 284        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _load
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_FORWARD         96  'to 96'
             48_0  COME_FROM_FINALLY     0  '0'

 L. 285        48  DUP_TOP          
               50  LOAD_GLOBAL              struct
               52  LOAD_ATTR                error
               54  <121>                94  ''
               56  POP_TOP          
               58  STORE_FAST               'e'
               60  POP_TOP          
               62  SETUP_FINALLY        86  'to 86'

 L. 286        64  LOAD_GLOBAL              OSError
               66  LOAD_STR                 'Truncated Blp file'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'e'
               72  RAISE_VARARGS_2       2  'exception instance with __cause__'
               74  POP_BLOCK        
               76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  STORE_FAST               'e'
               82  DELETE_FAST              'e'
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM_FINALLY    62  '62'
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  <48>             
               94  <48>             
             96_0  COME_FROM            84  '84'
             96_1  COME_FROM            46  '46'

 L. 287        96  LOAD_CONST               (0, 0)
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 54

    def _safe_read(self, length):
        return ImageFile._safe_read(self.fd, length)

    def _read_palette--- This code section failed: ---

 L. 293         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L. 294         4  LOAD_GLOBAL              range
                6  LOAD_CONST               256
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM            92  '92'
               12  FOR_ITER             94  'to 94'
               14  STORE_FAST               'i'

 L. 295        16  SETUP_FINALLY        48  'to 48'

 L. 296        18  LOAD_GLOBAL              struct
               20  LOAD_METHOD              unpack
               22  LOAD_STR                 '<4B'
               24  LOAD_FAST                'self'
               26  LOAD_METHOD              _safe_read
               28  LOAD_CONST               4
               30  CALL_METHOD_1         1  ''
               32  CALL_METHOD_2         2  ''
               34  UNPACK_SEQUENCE_4     4 
               36  STORE_FAST               'b'
               38  STORE_FAST               'g'
               40  STORE_FAST               'r'
               42  STORE_FAST               'a'
               44  POP_BLOCK        
               46  JUMP_FORWARD         74  'to 74'
             48_0  COME_FROM_FINALLY    16  '16'

 L. 297        48  DUP_TOP          
               50  LOAD_GLOBAL              struct
               52  LOAD_ATTR                error
               54  <121>                72  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 298        62  POP_EXCEPT       
               64  POP_TOP          
               66  JUMP_FORWARD         94  'to 94'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            46  '46'

 L. 299        74  LOAD_FAST                'ret'
               76  LOAD_METHOD              append
               78  LOAD_FAST                'b'
               80  LOAD_FAST                'g'
               82  LOAD_FAST                'r'
               84  LOAD_FAST                'a'
               86  BUILD_TUPLE_4         4 
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_BACK            12  'to 12'
             94_0  COME_FROM            66  '66'
             94_1  COME_FROM            12  '12'

 L. 300        94  LOAD_FAST                'ret'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 54

    def _read_blp_header(self):
        self._blp_compression, = struct.unpack('<i', self._safe_read(4))
        self._blp_encoding, = struct.unpack('<b', self._safe_read(1))
        self._blp_alpha_depth, = struct.unpack('<b', self._safe_read(1))
        self._blp_alpha_encoding, = struct.unpack('<b', self._safe_read(1))
        self._blp_mips, = struct.unpack('<b', self._safe_read(1))
        self.size = struct.unpack('<II', self._safe_read(8))
        if self.magic == b'BLP1':
            self._blp_encoding, = struct.unpack('<i', self._safe_read(4))
            self._blp_subtype, = struct.unpack('<i', self._safe_read(4))
        self._blp_offsets = struct.unpack('<16I', self._safe_read(64))
        self._blp_lengths = struct.unpack('<16I', self._safe_read(64))


class BLP1Decoder(_BLPBaseDecoder):

    def _load--- This code section failed: ---

 L. 323         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _blp_compression
                4  LOAD_GLOBAL              BLP_FORMAT_JPEG
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 324        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _decode_jpeg_stream
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
               18  JUMP_FORWARD        216  'to 216'
             20_0  COME_FROM             8  '8'

 L. 326        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _blp_compression
               24  LOAD_CONST               1
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE   196  'to 196'

 L. 327        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _blp_encoding
               34  LOAD_CONST               (4, 5)
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE   174  'to 174'

 L. 328        40  LOAD_GLOBAL              bytearray
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'data'

 L. 329        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _read_palette
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'palette'

 L. 330        54  LOAD_GLOBAL              BytesIO
               56  LOAD_FAST                'self'
               58  LOAD_METHOD              _safe_read
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _blp_lengths
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               '_data'
             74_0  COME_FROM           156  '156'

 L. 332        74  SETUP_FINALLY       100  'to 100'

 L. 333        76  LOAD_GLOBAL              struct
               78  LOAD_METHOD              unpack
               80  LOAD_STR                 '<B'
               82  LOAD_FAST                '_data'
               84  LOAD_METHOD              read
               86  LOAD_CONST               1
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_2         2  ''
               92  UNPACK_SEQUENCE_1     1 
               94  STORE_FAST               'offset'
               96  POP_BLOCK        
               98  JUMP_FORWARD        124  'to 124'
            100_0  COME_FROM_FINALLY    74  '74'

 L. 334       100  DUP_TOP          
              102  LOAD_GLOBAL              struct
              104  LOAD_ATTR                error
              106  <121>               122  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 335       114  POP_EXCEPT       
              116  BREAK_LOOP          158  'to 158'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            98  '98'

 L. 336       124  LOAD_FAST                'palette'
              126  LOAD_FAST                'offset'
              128  BINARY_SUBSCR    
              130  UNPACK_SEQUENCE_4     4 
              132  STORE_FAST               'b'
              134  STORE_FAST               'g'
              136  STORE_FAST               'r'
              138  STORE_FAST               'a'

 L. 337       140  LOAD_FAST                'data'
              142  LOAD_METHOD              extend
              144  LOAD_FAST                'r'
              146  LOAD_FAST                'g'
              148  LOAD_FAST                'b'
              150  BUILD_LIST_3          3 
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
              156  JUMP_BACK            74  'to 74'
            158_0  COME_FROM           116  '116'

 L. 339       158  LOAD_FAST                'self'
              160  LOAD_METHOD              set_as_raw
              162  LOAD_GLOBAL              bytes
              164  LOAD_FAST                'data'
              166  CALL_FUNCTION_1       1  ''
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_FORWARD        216  'to 216'
            174_0  COME_FROM            38  '38'

 L. 341       174  LOAD_GLOBAL              BLPFormatError

 L. 342       176  LOAD_STR                 'Unsupported BLP encoding '
              178  LOAD_GLOBAL              repr
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                _blp_encoding
              184  CALL_FUNCTION_1       1  ''
              186  FORMAT_VALUE          0  ''
              188  BUILD_STRING_2        2 

 L. 341       190  CALL_FUNCTION_1       1  ''
              192  RAISE_VARARGS_1       1  'exception instance'
              194  JUMP_FORWARD        216  'to 216'
            196_0  COME_FROM            28  '28'

 L. 345       196  LOAD_GLOBAL              BLPFormatError

 L. 346       198  LOAD_STR                 'Unsupported BLP compression '
              200  LOAD_GLOBAL              repr
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                _blp_encoding
              206  CALL_FUNCTION_1       1  ''
              208  FORMAT_VALUE          0  ''
              210  BUILD_STRING_2        2 

 L. 345       212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           194  '194'
            216_1  COME_FROM           172  '172'
            216_2  COME_FROM            18  '18'

Parse error at or near `<118>' instruction at offset 36

    def _decode_jpeg_stream(self):
        from PIL.JpegImagePlugin import JpegImageFile
        jpeg_header_size, = struct.unpack('<I', self._safe_read(4))
        jpeg_header = self._safe_read(jpeg_header_size)
        self._safe_read(self._blp_offsets[0] - self.fd.tell())
        data = self._safe_read(self._blp_lengths[0])
        data = jpeg_header + data
        data = BytesIO(data)
        image = JpegImageFile(data)
        Image._decompression_bomb_check(image.size)
        self.tile = image.tile
        self.fd = image.fp
        self.mode = image.mode


class BLP2Decoder(_BLPBaseDecoder):

    def _load--- This code section failed: ---

 L. 367         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _read_palette
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'palette'

 L. 369         8  LOAD_GLOBAL              bytearray
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'data'

 L. 370        14  LOAD_FAST                'self'
               16  LOAD_ATTR                fd
               18  LOAD_METHOD              seek
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _blp_offsets
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 372        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _blp_compression
               36  LOAD_CONST               1
               38  COMPARE_OP               ==
            40_42  POP_JUMP_IF_FALSE   514  'to 514'

 L. 375        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _blp_encoding
               48  LOAD_GLOBAL              BLP_ENCODING_UNCOMPRESSED
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   162  'to 162'

 L. 376        54  LOAD_GLOBAL              BytesIO
               56  LOAD_FAST                'self'
               58  LOAD_METHOD              _safe_read
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _blp_lengths
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               '_data'
             74_0  COME_FROM           156  '156'

 L. 378        74  SETUP_FINALLY       100  'to 100'

 L. 379        76  LOAD_GLOBAL              struct
               78  LOAD_METHOD              unpack
               80  LOAD_STR                 '<B'
               82  LOAD_FAST                '_data'
               84  LOAD_METHOD              read
               86  LOAD_CONST               1
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_2         2  ''
               92  UNPACK_SEQUENCE_1     1 
               94  STORE_FAST               'offset'
               96  POP_BLOCK        
               98  JUMP_FORWARD        124  'to 124'
            100_0  COME_FROM_FINALLY    74  '74'

 L. 380       100  DUP_TOP          
              102  LOAD_GLOBAL              struct
              104  LOAD_ATTR                error
              106  <121>               122  ''
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 381       114  POP_EXCEPT       
              116  BREAK_LOOP          158  'to 158'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            98  '98'

 L. 382       124  LOAD_FAST                'palette'
              126  LOAD_FAST                'offset'
              128  BINARY_SUBSCR    
              130  UNPACK_SEQUENCE_4     4 
              132  STORE_FAST               'b'
              134  STORE_FAST               'g'
              136  STORE_FAST               'r'
              138  STORE_FAST               'a'

 L. 383       140  LOAD_FAST                'data'
              142  LOAD_METHOD              extend
              144  LOAD_FAST                'r'
              146  LOAD_FAST                'g'
              148  LOAD_FAST                'b'
              150  BUILD_TUPLE_3         3 
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
              156  JUMP_BACK            74  'to 74'
            158_0  COME_FROM           116  '116'
          158_160  JUMP_FORWARD        534  'to 534'
            162_0  COME_FROM            52  '52'

 L. 385       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _blp_encoding
              166  LOAD_GLOBAL              BLP_ENCODING_DXT
              168  COMPARE_OP               ==
          170_172  POP_JUMP_IF_FALSE   492  'to 492'

 L. 386       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _blp_alpha_encoding
              178  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT1
              180  COMPARE_OP               ==
          182_184  POP_JUMP_IF_FALSE   278  'to 278'

 L. 387       186  LOAD_FAST                'self'
              188  LOAD_ATTR                size
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  LOAD_CONST               3
              196  BINARY_ADD       
              198  LOAD_CONST               4
              200  BINARY_FLOOR_DIVIDE
              202  LOAD_CONST               8
              204  BINARY_MULTIPLY  
              206  STORE_FAST               'linesize'

 L. 388       208  LOAD_GLOBAL              range
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                size
              214  LOAD_CONST               1
              216  BINARY_SUBSCR    
              218  LOAD_CONST               3
              220  BINARY_ADD       
              222  LOAD_CONST               4
              224  BINARY_FLOOR_DIVIDE
              226  CALL_FUNCTION_1       1  ''
              228  GET_ITER         
            230_0  COME_FROM           274  '274'
              230  FOR_ITER            276  'to 276'
              232  STORE_FAST               'yb'

 L. 389       234  LOAD_GLOBAL              decode_dxt1

 L. 390       236  LOAD_FAST                'self'
              238  LOAD_METHOD              _safe_read
              240  LOAD_FAST                'linesize'
              242  CALL_METHOD_1         1  ''
              244  LOAD_GLOBAL              bool
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                _blp_alpha_depth
              250  CALL_FUNCTION_1       1  ''

 L. 389       252  LOAD_CONST               ('alpha',)
              254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              256  GET_ITER         
            258_0  COME_FROM           270  '270'
              258  FOR_ITER            274  'to 274'
              260  STORE_FAST               'd'

 L. 392       262  LOAD_FAST                'data'
              264  LOAD_FAST                'd'
              266  INPLACE_ADD      
              268  STORE_FAST               'data'
          270_272  JUMP_BACK           258  'to 258'
            274_0  COME_FROM           258  '258'
              274  JUMP_BACK           230  'to 230'
            276_0  COME_FROM           230  '230'
              276  JUMP_FORWARD        490  'to 490'
            278_0  COME_FROM           182  '182'

 L. 394       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _blp_alpha_encoding
              282  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT3
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   374  'to 374'

 L. 395       290  LOAD_FAST                'self'
              292  LOAD_ATTR                size
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  LOAD_CONST               3
              300  BINARY_ADD       
              302  LOAD_CONST               4
              304  BINARY_FLOOR_DIVIDE
              306  LOAD_CONST               16
              308  BINARY_MULTIPLY  
              310  STORE_FAST               'linesize'

 L. 396       312  LOAD_GLOBAL              range
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                size
              318  LOAD_CONST               1
              320  BINARY_SUBSCR    
              322  LOAD_CONST               3
              324  BINARY_ADD       
              326  LOAD_CONST               4
              328  BINARY_FLOOR_DIVIDE
              330  CALL_FUNCTION_1       1  ''
              332  GET_ITER         
            334_0  COME_FROM           368  '368'
              334  FOR_ITER            372  'to 372'
              336  STORE_FAST               'yb'

 L. 397       338  LOAD_GLOBAL              decode_dxt3
              340  LOAD_FAST                'self'
              342  LOAD_METHOD              _safe_read
              344  LOAD_FAST                'linesize'
              346  CALL_METHOD_1         1  ''
              348  CALL_FUNCTION_1       1  ''
              350  GET_ITER         
            352_0  COME_FROM           364  '364'
              352  FOR_ITER            368  'to 368'
              354  STORE_FAST               'd'

 L. 398       356  LOAD_FAST                'data'
              358  LOAD_FAST                'd'
              360  INPLACE_ADD      
              362  STORE_FAST               'data'
          364_366  JUMP_BACK           352  'to 352'
            368_0  COME_FROM           352  '352'
          368_370  JUMP_BACK           334  'to 334'
            372_0  COME_FROM           334  '334'
              372  JUMP_FORWARD        490  'to 490'
            374_0  COME_FROM           286  '286'

 L. 400       374  LOAD_FAST                'self'
              376  LOAD_ATTR                _blp_alpha_encoding
              378  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT5
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   470  'to 470'

 L. 401       386  LOAD_FAST                'self'
              388  LOAD_ATTR                size
              390  LOAD_CONST               0
              392  BINARY_SUBSCR    
              394  LOAD_CONST               3
              396  BINARY_ADD       
              398  LOAD_CONST               4
              400  BINARY_FLOOR_DIVIDE
              402  LOAD_CONST               16
              404  BINARY_MULTIPLY  
              406  STORE_FAST               'linesize'

 L. 402       408  LOAD_GLOBAL              range
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                size
              414  LOAD_CONST               1
              416  BINARY_SUBSCR    
              418  LOAD_CONST               3
              420  BINARY_ADD       
              422  LOAD_CONST               4
              424  BINARY_FLOOR_DIVIDE
              426  CALL_FUNCTION_1       1  ''
              428  GET_ITER         
            430_0  COME_FROM           464  '464'
              430  FOR_ITER            468  'to 468'
              432  STORE_FAST               'yb'

 L. 403       434  LOAD_GLOBAL              decode_dxt5
              436  LOAD_FAST                'self'
              438  LOAD_METHOD              _safe_read
              440  LOAD_FAST                'linesize'
              442  CALL_METHOD_1         1  ''
              444  CALL_FUNCTION_1       1  ''
              446  GET_ITER         
            448_0  COME_FROM           460  '460'
              448  FOR_ITER            464  'to 464'
              450  STORE_FAST               'd'

 L. 404       452  LOAD_FAST                'data'
              454  LOAD_FAST                'd'
              456  INPLACE_ADD      
              458  STORE_FAST               'data'
          460_462  JUMP_BACK           448  'to 448'
            464_0  COME_FROM           448  '448'
          464_466  JUMP_BACK           430  'to 430'
            468_0  COME_FROM           430  '430'
              468  JUMP_FORWARD        490  'to 490'
            470_0  COME_FROM           382  '382'

 L. 406       470  LOAD_GLOBAL              BLPFormatError

 L. 407       472  LOAD_STR                 'Unsupported alpha encoding '
              474  LOAD_GLOBAL              repr
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                _blp_alpha_encoding
              480  CALL_FUNCTION_1       1  ''
              482  FORMAT_VALUE          0  ''
              484  BUILD_STRING_2        2 

 L. 406       486  CALL_FUNCTION_1       1  ''
              488  RAISE_VARARGS_1       1  'exception instance'
            490_0  COME_FROM           468  '468'
            490_1  COME_FROM           372  '372'
            490_2  COME_FROM           276  '276'
              490  JUMP_FORWARD        512  'to 512'
            492_0  COME_FROM           170  '170'

 L. 410       492  LOAD_GLOBAL              BLPFormatError
              494  LOAD_STR                 'Unknown BLP encoding '
              496  LOAD_GLOBAL              repr
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                _blp_encoding
              502  CALL_FUNCTION_1       1  ''
              504  FORMAT_VALUE          0  ''
              506  BUILD_STRING_2        2 
              508  CALL_FUNCTION_1       1  ''
              510  RAISE_VARARGS_1       1  'exception instance'
            512_0  COME_FROM           490  '490'
              512  JUMP_FORWARD        534  'to 534'
            514_0  COME_FROM            40  '40'

 L. 413       514  LOAD_GLOBAL              BLPFormatError

 L. 414       516  LOAD_STR                 'Unknown BLP compression '
              518  LOAD_GLOBAL              repr
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                _blp_compression
              524  CALL_FUNCTION_1       1  ''
              526  FORMAT_VALUE          0  ''
              528  BUILD_STRING_2        2 

 L. 413       530  CALL_FUNCTION_1       1  ''
              532  RAISE_VARARGS_1       1  'exception instance'
            534_0  COME_FROM           512  '512'
            534_1  COME_FROM           158  '158'

 L. 417       534  LOAD_FAST                'self'
              536  LOAD_METHOD              set_as_raw
              538  LOAD_GLOBAL              bytes
              540  LOAD_FAST                'data'
              542  CALL_FUNCTION_1       1  ''
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          

Parse error at or near `<121>' instruction at offset 106


def _accept--- This code section failed: ---

 L. 421         0  LOAD_FAST                'prefix'
                2  LOAD_CONST               None
                4  LOAD_CONST               4
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_CONST               (b'BLP1', b'BLP2')
               12  <118>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


Image.register_open(BlpImageFile.format, BlpImageFile, _accept)
Image.register_extension(BlpImageFile.format, '.blp')
Image.register_decoder('BLP1', BLP1Decoder)
Image.register_decoder('BLP2', BLP2Decoder)