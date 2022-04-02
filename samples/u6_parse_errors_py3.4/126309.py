# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\IcoImagePlugin.py
import struct
from io import BytesIO
from . import Image, ImageFile, BmpImagePlugin, PngImagePlugin
from ._binary import i8, i16le as i16, i32le as i32
from math import log, ceil
__version__ = '0.1'
_MAGIC = b'\x00\x00\x01\x00'

def _save(im, fp, filename):
    fp.write(_MAGIC)
    sizes = im.encoderinfo.get('sizes', [
     (16, 16), (24, 24), (32, 32), (48, 48),
     (64, 64), (128, 128), (256, 256)])
    width, height = im.size
    sizes = filter(--- This code section failed: ---

 L.  46         0  LOAD_FAST                'x'
                3  LOAD_CONST               0
                6  BINARY_SUBSCR    
                7  LOAD_DEREF               'width'
               10  COMPARE_OP               >
               13  POP_JUMP_IF_TRUE     64  'to 64'
               16  LOAD_FAST                'x'
               19  LOAD_CONST               1
               22  BINARY_SUBSCR    
               23  LOAD_DEREF               'height'
               26  COMPARE_OP               >
               29  POP_JUMP_IF_TRUE     64  'to 64'

 L.  47        32  LOAD_FAST                'x'
               35  LOAD_CONST               0
               38  BINARY_SUBSCR    
               39  LOAD_CONST               256
               42  COMPARE_OP               >
               45  POP_JUMP_IF_TRUE     64  'to 64'
               48  LOAD_FAST                'x'
               51  LOAD_CONST               1
               54  BINARY_SUBSCR    
               55  LOAD_CONST               256
               58  COMPARE_OP               >
             61_0  COME_FROM            45  '45'
             61_1  COME_FROM            29  '29'
             61_2  COME_FROM            13  '13'
               61  POP_JUMP_IF_FALSE    68  'to 68'
               64  LOAD_CONST               False
               67  RETURN_END_IF_LAMBDA
             68_0  COME_FROM            61  '61'
               68  LOAD_CONST               True
               71  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `COME_FROM' instruction at offset 68_0
, sizes)
    sizes = list(sizes)
    fp.write(struct.pack('<H', len(sizes)))
    offset = fp.tell() + len(sizes) * 16
    for size in sizes:
        width, height = size
        fp.write(struct.pack('B', width if width < 256 else 0))
        fp.write(struct.pack('B', height if height < 256 else 0))
        fp.write(b'\x00')
        fp.write(b'\x00')
        fp.write(b'\x00\x00')
        fp.write(struct.pack('<H', 32))
        image_io = BytesIO()
        tmp = im.copy()
        tmp.thumbnail(size, Image.LANCZOS)
        tmp.save(image_io, 'png')
        image_io.seek(0)
        image_bytes = image_io.read()
        bytes_len = len(image_bytes)
        fp.write(struct.pack('<I', bytes_len))
        fp.write(struct.pack('<I', offset))
        current = fp.tell()
        fp.seek(offset)
        fp.write(image_bytes)
        offset = offset + bytes_len
        fp.seek(current)


def _accept(prefix):
    return prefix[:4] == _MAGIC


class IcoFile(object):

    def __init__(self, buf):
        """
        Parse image from file-like object containing ico file data
        """
        s = buf.read(6)
        if not _accept(s):
            raise SyntaxError('not an ICO file')
        self.buf = buf
        self.entry = []
        self.nb_items = i16(s[4:])
        for i in range(self.nb_items):
            s = buf.read(16)
            icon_header = {'width': i8(s[0]), 
             'height': i8(s[1]), 
             'nb_color': i8(s[2]), 
             'reserved': i8(s[3]), 
             'planes': i16(s[4:]), 
             'bpp': i16(s[6:]), 
             'size': i32(s[8:]), 
             'offset': i32(s[12:])}
            for j in ('width', 'height'):
                if not icon_header[j]:
                    icon_header[j] = 256
                    continue

            icon_header['color_depth'] = icon_header['bpp'] or icon_header['nb_color'] != 0 and ceil(log(icon_header['nb_color'], 2)) or 256
            icon_header['dim'] = (
             icon_header['width'], icon_header['height'])
            icon_header['square'] = icon_header['width'] * icon_header['height']
            self.entry.append(icon_header)

        self.entry = sorted(self.entry, key=lambda x: x['color_depth'])
        self.entry = sorted(self.entry, key=lambda x: x['square'])
        self.entry.reverse()

    def sizes(self):
        """
        Get a list of all available icon sizes and color depths.
        """
        return {(h['width'], h['height']) for h in self.entry}

    def getimage(self, size, bpp=False):
        """
        Get an image from the icon
        """
        for i, h in enumerate(self.entry):
            if size == h['dim'] and (bpp is False or bpp == h['color_depth']):
                return self.frame(i)

        return self.frame(0)

    def frame(self, idx):
        """
        Get an image from frame idx
        """
        header = self.entry[idx]
        self.buf.seek(header['offset'])
        data = self.buf.read(8)
        self.buf.seek(header['offset'])
        if data[:8] == PngImagePlugin._MAGIC:
            im = PngImagePlugin.PngImageFile(self.buf)
        else:
            im = BmpImagePlugin.DibImageFile(self.buf)
            im._size = (
             im.size[0], int(im.size[1] / 2))
            d, e, o, a = im.tile[0]
            im.tile[0] = (d, (0, 0) + im.size, o, a)
            mode = a[0]
            bpp = 8
            for k, v in BmpImagePlugin.BIT2MODE.items():
                if mode == v[1]:
                    bpp = k
                    break

            if 32 == bpp:
                self.buf.seek(o)
                alpha_bytes = self.buf.read(im.size[0] * im.size[1] * 4)[3::4]
                mask = Image.frombuffer('L', im.size, alpha_bytes, 'raw', ('L', 0,
                                                                           -1))
            else:
                w = im.size[0]
                if w % 32 > 0:
                    w += 32 - im.size[0] % 32
                and_mask_offset = o + int(im.size[0] * im.size[1] * (bpp / 8.0))
                total_bytes = int(w * im.size[1] / 8)
                self.buf.seek(and_mask_offset)
                mask_data = self.buf.read(total_bytes)
                mask = Image.frombuffer('1', im.size, mask_data, 'raw', (
                 '1;I', int(w / 8), -1))
            im = im.convert('RGBA')
            im.putalpha(mask)
        return im


class IcoImageFile(ImageFile.ImageFile):
    __doc__ = "\n    PIL read-only image support for Microsoft Windows .ico files.\n\n    By default the largest resolution image in the file will be loaded. This\n    can be changed by altering the 'size' attribute before calling 'load'.\n\n    The info dictionary has a key 'sizes' that is a list of the sizes available\n    in the icon file.\n\n    Handles classic, XP and Vista icon formats.\n\n    This plugin is a refactored version of Win32IconImagePlugin by Bryan Davis\n    <casadebender@gmail.com>.\n    https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki\n    "
    format = 'ICO'
    format_description = 'Windows Icon'

    def _open(self):
        self.ico = IcoFile(self.fp)
        self.info['sizes'] = self.ico.sizes()
        self.size = self.ico.entry[0]['dim']
        self.load()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value not in self.info['sizes']:
            raise ValueError('This is not one of the allowed sizes of this image')
        self._size = value

    def load(self):
        im = self.ico.getimage(self.size)
        im.load()
        self.im = im.im
        self.mode = im.mode
        self.size = im.size

    def load_seek(self):
        pass


Image.register_open(IcoImageFile.format, IcoImageFile, _accept)
Image.register_save(IcoImageFile.format, _save)
Image.register_extension(IcoImageFile.format, '.ico')