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

    def _read_palette--- This code section failed: ---

 L. 290         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L. 291         4  LOAD_GLOBAL              range
                6  LOAD_CONST               256
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM            94  '94'
               12  FOR_ITER             96  'to 96'
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
               48  JUMP_FORWARD         76  'to 76'
             50_0  COME_FROM_FINALLY    16  '16'

 L. 294        50  DUP_TOP          
               52  LOAD_GLOBAL              struct
               54  LOAD_ATTR                error
               56  <121>                74  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 295        64  POP_EXCEPT       
               66  POP_TOP          
               68  JUMP_FORWARD         96  'to 96'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            48  '48'

 L. 296        76  LOAD_FAST                'ret'
               78  LOAD_METHOD              append
               80  LOAD_FAST                'b'
               82  LOAD_FAST                'g'
               84  LOAD_FAST                'r'
               86  LOAD_FAST                'a'
               88  BUILD_TUPLE_4         4 
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  JUMP_BACK            12  'to 12'
             96_0  COME_FROM            68  '68'
             96_1  COME_FROM            12  '12'

 L. 297        96  LOAD_FAST                'ret'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56

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

    def _load--- This code section failed: ---

 L. 320         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _blp_compression
                4  LOAD_GLOBAL              BLP_FORMAT_JPEG
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 321        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _decode_jpeg_stream
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
               18  JUMP_FORWARD        218  'to 218'
             20_0  COME_FROM             8  '8'

 L. 323        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _blp_compression
               24  LOAD_CONST               1
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE   198  'to 198'

 L. 324        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _blp_encoding
               34  LOAD_CONST               (4, 5)
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE   176  'to 176'

 L. 325        40  LOAD_GLOBAL              bytearray
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'data'

 L. 326        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _read_palette
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'palette'

 L. 327        54  LOAD_GLOBAL              BytesIO
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                fd
               60  LOAD_METHOD              read
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _blp_lengths
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  CALL_METHOD_1         1  ''
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               '_data'
             76_0  COME_FROM           158  '158'

 L. 329        76  SETUP_FINALLY       102  'to 102'

 L. 330        78  LOAD_GLOBAL              struct
               80  LOAD_METHOD              unpack
               82  LOAD_STR                 '<B'
               84  LOAD_FAST                '_data'
               86  LOAD_METHOD              read
               88  LOAD_CONST               1
               90  CALL_METHOD_1         1  ''
               92  CALL_METHOD_2         2  ''
               94  UNPACK_SEQUENCE_1     1 
               96  STORE_FAST               'offset'
               98  POP_BLOCK        
              100  JUMP_FORWARD        126  'to 126'
            102_0  COME_FROM_FINALLY    76  '76'

 L. 331       102  DUP_TOP          
              104  LOAD_GLOBAL              struct
              106  LOAD_ATTR                error
              108  <121>               124  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 332       116  POP_EXCEPT       
              118  BREAK_LOOP          160  'to 160'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           100  '100'

 L. 333       126  LOAD_FAST                'palette'
              128  LOAD_FAST                'offset'
              130  BINARY_SUBSCR    
              132  UNPACK_SEQUENCE_4     4 
              134  STORE_FAST               'b'
              136  STORE_FAST               'g'
              138  STORE_FAST               'r'
              140  STORE_FAST               'a'

 L. 334       142  LOAD_FAST                'data'
              144  LOAD_METHOD              extend
              146  LOAD_FAST                'r'
              148  LOAD_FAST                'g'
              150  LOAD_FAST                'b'
              152  BUILD_LIST_3          3 
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  JUMP_BACK            76  'to 76'
            160_0  COME_FROM           118  '118'

 L. 336       160  LOAD_FAST                'self'
              162  LOAD_METHOD              set_as_raw
              164  LOAD_GLOBAL              bytes
              166  LOAD_FAST                'data'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_FORWARD        218  'to 218'
            176_0  COME_FROM            38  '38'

 L. 338       176  LOAD_GLOBAL              BLPFormatError

 L. 339       178  LOAD_STR                 'Unsupported BLP encoding '
              180  LOAD_GLOBAL              repr
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                _blp_encoding
              186  CALL_FUNCTION_1       1  ''
              188  FORMAT_VALUE          0  ''
              190  BUILD_STRING_2        2 

 L. 338       192  CALL_FUNCTION_1       1  ''
              194  RAISE_VARARGS_1       1  'exception instance'
              196  JUMP_FORWARD        218  'to 218'
            198_0  COME_FROM            28  '28'

 L. 342       198  LOAD_GLOBAL              BLPFormatError

 L. 343       200  LOAD_STR                 'Unsupported BLP compression '
              202  LOAD_GLOBAL              repr
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                _blp_encoding
              208  CALL_FUNCTION_1       1  ''
              210  FORMAT_VALUE          0  ''
              212  BUILD_STRING_2        2 

 L. 342       214  CALL_FUNCTION_1       1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           196  '196'
            218_1  COME_FROM           174  '174'
            218_2  COME_FROM            18  '18'

Parse error at or near `<118>' instruction at offset 36

    def _decode_jpeg_stream(self):
        from PIL.JpegImagePlugin import JpegImageFile
        jpeg_header_size, = struct.unpack('<I', self.fd.read(4))
        jpeg_header = self.fd.read(jpeg_header_size)
        self.fd.read(self._blp_offsets[0] - self.fd.tell())
        data = self.fd.read(self._blp_lengths[0])
        data = jpeg_header + data
        data = BytesIO(data)
        image = JpegImageFile(data)
        Image._decompression_bomb_check(image.size)
        self.tile = image.tile
        self.fd = image.fp
        self.mode = image.mode


class BLP2Decoder(_BLPBaseDecoder):

    def _load--- This code section failed: ---

 L. 364         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _read_palette
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'palette'

 L. 366         8  LOAD_GLOBAL              bytearray
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'data'

 L. 367        14  LOAD_FAST                'self'
               16  LOAD_ATTR                fd
               18  LOAD_METHOD              seek
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _blp_offsets
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 369        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _blp_compression
               36  LOAD_CONST               1
               38  COMPARE_OP               ==
            40_42  POP_JUMP_IF_FALSE   522  'to 522'

 L. 372        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _blp_encoding
               48  LOAD_GLOBAL              BLP_ENCODING_UNCOMPRESSED
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   164  'to 164'

 L. 373        54  LOAD_GLOBAL              BytesIO
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                fd
               60  LOAD_METHOD              read
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _blp_lengths
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  CALL_METHOD_1         1  ''
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               '_data'
             76_0  COME_FROM           158  '158'

 L. 375        76  SETUP_FINALLY       102  'to 102'

 L. 376        78  LOAD_GLOBAL              struct
               80  LOAD_METHOD              unpack
               82  LOAD_STR                 '<B'
               84  LOAD_FAST                '_data'
               86  LOAD_METHOD              read
               88  LOAD_CONST               1
               90  CALL_METHOD_1         1  ''
               92  CALL_METHOD_2         2  ''
               94  UNPACK_SEQUENCE_1     1 
               96  STORE_FAST               'offset'
               98  POP_BLOCK        
              100  JUMP_FORWARD        126  'to 126'
            102_0  COME_FROM_FINALLY    76  '76'

 L. 377       102  DUP_TOP          
              104  LOAD_GLOBAL              struct
              106  LOAD_ATTR                error
              108  <121>               124  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 378       116  POP_EXCEPT       
              118  BREAK_LOOP          160  'to 160'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           100  '100'

 L. 379       126  LOAD_FAST                'palette'
              128  LOAD_FAST                'offset'
              130  BINARY_SUBSCR    
              132  UNPACK_SEQUENCE_4     4 
              134  STORE_FAST               'b'
              136  STORE_FAST               'g'
              138  STORE_FAST               'r'
              140  STORE_FAST               'a'

 L. 380       142  LOAD_FAST                'data'
              144  LOAD_METHOD              extend
              146  LOAD_FAST                'r'
              148  LOAD_FAST                'g'
              150  LOAD_FAST                'b'
              152  BUILD_TUPLE_3         3 
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  JUMP_BACK            76  'to 76'
            160_0  COME_FROM           118  '118'
          160_162  JUMP_FORWARD        542  'to 542'
            164_0  COME_FROM            52  '52'

 L. 382       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _blp_encoding
              168  LOAD_GLOBAL              BLP_ENCODING_DXT
              170  COMPARE_OP               ==
          172_174  POP_JUMP_IF_FALSE   500  'to 500'

 L. 383       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _blp_alpha_encoding
              180  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT1
              182  COMPARE_OP               ==
          184_186  POP_JUMP_IF_FALSE   282  'to 282'

 L. 384       188  LOAD_FAST                'self'
              190  LOAD_ATTR                size
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  LOAD_CONST               3
              198  BINARY_ADD       
              200  LOAD_CONST               4
              202  BINARY_FLOOR_DIVIDE
              204  LOAD_CONST               8
              206  BINARY_MULTIPLY  
              208  STORE_FAST               'linesize'

 L. 385       210  LOAD_GLOBAL              range
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                size
              216  LOAD_CONST               1
              218  BINARY_SUBSCR    
              220  LOAD_CONST               3
              222  BINARY_ADD       
              224  LOAD_CONST               4
              226  BINARY_FLOOR_DIVIDE
              228  CALL_FUNCTION_1       1  ''
              230  GET_ITER         
            232_0  COME_FROM           278  '278'
              232  FOR_ITER            280  'to 280'
              234  STORE_FAST               'yb'

 L. 386       236  LOAD_GLOBAL              decode_dxt1

 L. 387       238  LOAD_FAST                'self'
              240  LOAD_ATTR                fd
              242  LOAD_METHOD              read
              244  LOAD_FAST                'linesize'
              246  CALL_METHOD_1         1  ''
              248  LOAD_GLOBAL              bool
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                _blp_alpha_depth
              254  CALL_FUNCTION_1       1  ''

 L. 386       256  LOAD_CONST               ('alpha',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  GET_ITER         
            262_0  COME_FROM           274  '274'
              262  FOR_ITER            278  'to 278'
              264  STORE_FAST               'd'

 L. 389       266  LOAD_FAST                'data'
              268  LOAD_FAST                'd'
              270  INPLACE_ADD      
              272  STORE_FAST               'data'
          274_276  JUMP_BACK           262  'to 262'
            278_0  COME_FROM           262  '262'
              278  JUMP_BACK           232  'to 232'
            280_0  COME_FROM           232  '232'
              280  JUMP_FORWARD        498  'to 498'
            282_0  COME_FROM           184  '184'

 L. 391       282  LOAD_FAST                'self'
              284  LOAD_ATTR                _blp_alpha_encoding
              286  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT3
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   380  'to 380'

 L. 392       294  LOAD_FAST                'self'
              296  LOAD_ATTR                size
              298  LOAD_CONST               0
              300  BINARY_SUBSCR    
              302  LOAD_CONST               3
              304  BINARY_ADD       
              306  LOAD_CONST               4
              308  BINARY_FLOOR_DIVIDE
              310  LOAD_CONST               16
              312  BINARY_MULTIPLY  
              314  STORE_FAST               'linesize'

 L. 393       316  LOAD_GLOBAL              range
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                size
              322  LOAD_CONST               1
              324  BINARY_SUBSCR    
              326  LOAD_CONST               3
              328  BINARY_ADD       
              330  LOAD_CONST               4
              332  BINARY_FLOOR_DIVIDE
              334  CALL_FUNCTION_1       1  ''
              336  GET_ITER         
            338_0  COME_FROM           374  '374'
              338  FOR_ITER            378  'to 378'
              340  STORE_FAST               'yb'

 L. 394       342  LOAD_GLOBAL              decode_dxt3
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                fd
              348  LOAD_METHOD              read
              350  LOAD_FAST                'linesize'
              352  CALL_METHOD_1         1  ''
              354  CALL_FUNCTION_1       1  ''
              356  GET_ITER         
            358_0  COME_FROM           370  '370'
              358  FOR_ITER            374  'to 374'
              360  STORE_FAST               'd'

 L. 395       362  LOAD_FAST                'data'
              364  LOAD_FAST                'd'
              366  INPLACE_ADD      
              368  STORE_FAST               'data'
          370_372  JUMP_BACK           358  'to 358'
            374_0  COME_FROM           358  '358'
          374_376  JUMP_BACK           338  'to 338'
            378_0  COME_FROM           338  '338'
              378  JUMP_FORWARD        498  'to 498'
            380_0  COME_FROM           290  '290'

 L. 397       380  LOAD_FAST                'self'
              382  LOAD_ATTR                _blp_alpha_encoding
              384  LOAD_GLOBAL              BLP_ALPHA_ENCODING_DXT5
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   478  'to 478'

 L. 398       392  LOAD_FAST                'self'
              394  LOAD_ATTR                size
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  LOAD_CONST               3
              402  BINARY_ADD       
              404  LOAD_CONST               4
              406  BINARY_FLOOR_DIVIDE
              408  LOAD_CONST               16
              410  BINARY_MULTIPLY  
              412  STORE_FAST               'linesize'

 L. 399       414  LOAD_GLOBAL              range
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                size
              420  LOAD_CONST               1
              422  BINARY_SUBSCR    
              424  LOAD_CONST               3
              426  BINARY_ADD       
              428  LOAD_CONST               4
              430  BINARY_FLOOR_DIVIDE
              432  CALL_FUNCTION_1       1  ''
              434  GET_ITER         
            436_0  COME_FROM           472  '472'
              436  FOR_ITER            476  'to 476'
              438  STORE_FAST               'yb'

 L. 400       440  LOAD_GLOBAL              decode_dxt5
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                fd
              446  LOAD_METHOD              read
              448  LOAD_FAST                'linesize'
              450  CALL_METHOD_1         1  ''
              452  CALL_FUNCTION_1       1  ''
              454  GET_ITER         
            456_0  COME_FROM           468  '468'
              456  FOR_ITER            472  'to 472'
              458  STORE_FAST               'd'

 L. 401       460  LOAD_FAST                'data'
              462  LOAD_FAST                'd'
              464  INPLACE_ADD      
              466  STORE_FAST               'data'
          468_470  JUMP_BACK           456  'to 456'
            472_0  COME_FROM           456  '456'
          472_474  JUMP_BACK           436  'to 436'
            476_0  COME_FROM           436  '436'
              476  JUMP_FORWARD        498  'to 498'
            478_0  COME_FROM           388  '388'

 L. 403       478  LOAD_GLOBAL              BLPFormatError

 L. 404       480  LOAD_STR                 'Unsupported alpha encoding '
              482  LOAD_GLOBAL              repr
              484  LOAD_FAST                'self'
              486  LOAD_ATTR                _blp_alpha_encoding
              488  CALL_FUNCTION_1       1  ''
              490  FORMAT_VALUE          0  ''
              492  BUILD_STRING_2        2 

 L. 403       494  CALL_FUNCTION_1       1  ''
              496  RAISE_VARARGS_1       1  'exception instance'
            498_0  COME_FROM           476  '476'
            498_1  COME_FROM           378  '378'
            498_2  COME_FROM           280  '280'
              498  JUMP_FORWARD        520  'to 520'
            500_0  COME_FROM           172  '172'

 L. 407       500  LOAD_GLOBAL              BLPFormatError
              502  LOAD_STR                 'Unknown BLP encoding '
              504  LOAD_GLOBAL              repr
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                _blp_encoding
              510  CALL_FUNCTION_1       1  ''
              512  FORMAT_VALUE          0  ''
              514  BUILD_STRING_2        2 
              516  CALL_FUNCTION_1       1  ''
              518  RAISE_VARARGS_1       1  'exception instance'
            520_0  COME_FROM           498  '498'
              520  JUMP_FORWARD        542  'to 542'
            522_0  COME_FROM            40  '40'

 L. 410       522  LOAD_GLOBAL              BLPFormatError

 L. 411       524  LOAD_STR                 'Unknown BLP compression '
              526  LOAD_GLOBAL              repr
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                _blp_compression
              532  CALL_FUNCTION_1       1  ''
              534  FORMAT_VALUE          0  ''
              536  BUILD_STRING_2        2 

 L. 410       538  CALL_FUNCTION_1       1  ''
              540  RAISE_VARARGS_1       1  'exception instance'
            542_0  COME_FROM           520  '520'
            542_1  COME_FROM           160  '160'

 L. 414       542  LOAD_FAST                'self'
              544  LOAD_METHOD              set_as_raw
              546  LOAD_GLOBAL              bytes
              548  LOAD_FAST                'data'
              550  CALL_FUNCTION_1       1  ''
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          

Parse error at or near `<121>' instruction at offset 108


Image.register_open(BlpImageFile.format, BlpImageFile, --- This code section failed: ---

 L. 418         0  LOAD_FAST                'p'
                2  LOAD_CONST               None
                4  LOAD_CONST               4
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_CONST               (b'BLP1', b'BLP2')
               12  <118>                 0  ''
               14  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
)
Image.register_extension(BlpImageFile.format, '.blp')
Image.register_decoder('BLP1', BLP1Decoder)
Image.register_decoder('BLP2', BLP2Decoder)