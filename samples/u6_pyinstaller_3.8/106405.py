# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PsdImagePlugin.py
import io
from . import Image, ImageFile, ImagePalette
from ._binary import i8, i16be as i16, i32be as i32
MODES = {(0, 1):('1', 1), 
 (0, 8):('L', 1), 
 (1, 8):('L', 1), 
 (2, 8):('P', 1), 
 (3, 8):('RGB', 3), 
 (4, 8):('CMYK', 4), 
 (7, 8):('L', 1), 
 (8, 8):('L', 1), 
 (9, 8):('LAB', 3)}

def _accept(prefix):
    return prefix[:4] == b'8BPS'


class PsdImageFile(ImageFile.ImageFile):
    format = 'PSD'
    format_description = 'Adobe Photoshop'
    _close_exclusive_fp_after_loading = False

    def _open(self):
        read = self.fp.read
        s = read(26)
        if s[:4] != b'8BPS' or i16(s[4:]) != 1:
            raise SyntaxError('not a PSD file')
        psd_bits = i16(s[22:])
        psd_channels = i16(s[12:])
        psd_mode = i16(s[24:])
        mode, channels = MODES[(psd_mode, psd_bits)]
        if channels > psd_channels:
            raise OSError('not enough channels')
        self.mode = mode
        self._size = (i32(s[18:]), i32(s[14:]))
        size = i32(read(4))
        if size:
            data = read(size)
            if mode == 'P':
                if size == 768:
                    self.palette = ImagePalette.raw('RGB;L', data)
        self.resources = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            while self.fp.tell() < end:
                read(4)
                id = i16(read(2))
                name = read(i8(read(1)))
                if not len(name) & 1:
                    read(1)
                data = read(i32(read(4)))
                if len(data) & 1:
                    read(1)
                self.resources.append((id, name, data))
                if id == 1039:
                    self.info['icc_profile'] = data

        self.layers = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            size = i32(read(4))
            if size:
                self.layers = _layerinfo(self.fp)
            self.fp.seek(end)
        self.tile = _maketile(self.fp, mode, (0, 0) + self.size, channels)
        self._PsdImageFile__fp = self.fp
        self.frame = 1
        self._min_frame = 1

    @property
    def n_frames(self):
        return len(self.layers)

    @property
    def is_animated(self):
        return len(self.layers) > 1

    def seek--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'layer'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 143        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 146        14  SETUP_FINALLY        74  'to 74'

 L. 147        16  LOAD_FAST                'self'
               18  LOAD_ATTR                layers
               20  LOAD_FAST                'layer'
               22  LOAD_CONST               1
               24  BINARY_SUBTRACT  
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_4     4 
               30  STORE_FAST               'name'
               32  STORE_FAST               'mode'
               34  STORE_FAST               'bbox'
               36  STORE_FAST               'tile'

 L. 148        38  LOAD_FAST                'mode'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               mode

 L. 149        44  LOAD_FAST                'tile'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               tile

 L. 150        50  LOAD_FAST                'layer'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               frame

 L. 151        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _PsdImageFile__fp
               60  LOAD_FAST                'self'
               62  STORE_ATTR               fp

 L. 152        64  LOAD_FAST                'name'
               66  LOAD_FAST                'bbox'
               68  BUILD_TUPLE_2         2 
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY    14  '14'

 L. 153        74  DUP_TOP          
               76  LOAD_GLOBAL              IndexError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   100  'to 100'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 154        88  LOAD_GLOBAL              EOFError
               90  LOAD_STR                 'no such layer'
               92  CALL_FUNCTION_1       1  ''
               94  RAISE_VARARGS_1       1  'exception instance'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            80  '80'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'

Parse error at or near `POP_TOP' instruction at offset 84

    def tell(self):
        return self.frame

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.fill(self.mode, self.size, 0)
        if self.mode == 'P':
            Image.Image.load(self)

    def _close__fp(self):
        try:
            try:
                if self._PsdImageFile__fp != self.fp:
                    self._PsdImageFile__fp.close()
            except AttributeError:
                pass

        finally:
            self._PsdImageFile__fp = None


def _layerinfo(file):
    layers = []
    read = file.read
    for i in range(abs(i16(read(2)))):
        y0 = i32(read(4))
        x0 = i32(read(4))
        y1 = i32(read(4))
        x1 = i32(read(4))
        info = []
        mode = []
        types = list(range(i16(read(2))))
        if len(types) > 4:
            pass
        else:
            for i in types:
                type = i16(read(2))
                if type == 65535:
                    m = 'A'
                else:
                    m = 'RGBA'[type]
                mode.append(m)
                size = i32(read(4))
                info.append((m, size))
            else:
                mode.sort()
                if mode == ['R']:
                    mode = 'L'
                else:
                    if mode == ['B', 'G', 'R']:
                        mode = 'RGB'
                    else:
                        if mode == ['A', 'B', 'G', 'R']:
                            mode = 'RGBA'
                        else:
                            mode = None
                read(12)
                name = ''
                size = i32(read(4))
                combined = 0
                if size:
                    data_end = file.tell() + size
                    length = i32(read(4))
                    if length:
                        file.seek(length - 16, io.SEEK_CUR)
                    combined += length + 4
                    length = i32(read(4))
                    if length:
                        file.seek(length, io.SEEK_CUR)
                    combined += length + 4
                    length = i8(read(1))
                    if length:
                        name = read(length).decode('latin-1', 'replace')
                    combined += length + 1
                    file.seek(data_end)
                layers.append((name, mode, (x0, y0, x1, y1)))

    else:
        i = 0
        for name, mode, bbox in layers:
            tile = []
            for m in mode:
                t = _maketile(file, m, bbox, 1)
                if t:
                    tile.extend(t)
                layers[i] = (
                 name, mode, bbox, tile)
                i += 1
            else:
                return layers


def _maketile(file, mode, bbox, channels):
    tile = None
    read = file.read
    compression = i16(read(2))
    xsize = bbox[2] - bbox[0]
    ysize = bbox[3] - bbox[1]
    offset = file.tell()
    if compression == 0:
        tile = []
        for channel in range(channels):
            layer = mode[channel]
            if mode == 'CMYK':
                layer += ';I'
            tile.append(('raw', bbox, offset, layer))
            offset = offset + xsize * ysize

    else:
        if compression == 1:
            i = 0
            tile = []
            bytecount = read(channels * ysize * 2)
            offset = file.tell()
            for channel in range(channels):
                layer = mode[channel]
                if mode == 'CMYK':
                    layer += ';I'
                tile.append(('packbits', bbox, offset, layer))
                for y in range(ysize):
                    offset = offset + i16(bytecount[i:i + 2])
                    i += 2

        file.seek(offset)
        if offset & 1:
            read(1)
        return tile


Image.register_open(PsdImageFile.format, PsdImageFile, _accept)
Image.register_extension(PsdImageFile.format, '.psd')