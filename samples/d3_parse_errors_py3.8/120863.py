# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\IcoImagePlugin.py
import struct, warnings
from io import BytesIO
from math import ceil, log
from . import BmpImagePlugin, Image, ImageFile, PngImagePlugin
from ._binary import i16le as i16
from ._binary import i32le as i32
_MAGIC = b'\x00\x00\x01\x00'

def _save(im, fp, filename):
    fp.write(_MAGIC)
    sizes = im.encoderinfo.get('sizes', [
     (16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    width, height = im.size
    sizes = filter(--- This code section failed: ---

 L.  49         0  LOAD_FAST                'x'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_DEREF               'width'
                8  COMPARE_OP               >

 L.  48        10  POP_JUMP_IF_TRUE     48  'to 48'

 L.  49        12  LOAD_FAST                'x'
               14  LOAD_CONST               1
               16  BINARY_SUBSCR    
               18  LOAD_DEREF               'height'
               20  COMPARE_OP               >

 L.  48        22  POP_JUMP_IF_TRUE     48  'to 48'

 L.  49        24  LOAD_FAST                'x'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_CONST               256
               32  COMPARE_OP               >

 L.  48        34  POP_JUMP_IF_TRUE     48  'to 48'

 L.  49        36  LOAD_FAST                'x'
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  LOAD_CONST               256
               44  COMPARE_OP               >

 L.  48        46  POP_JUMP_IF_FALSE    52  'to 52'
             48_0  COME_FROM            34  '34'
             48_1  COME_FROM            22  '22'
             48_2  COME_FROM            10  '10'
               48  LOAD_CONST               False
               50  RETURN_VALUE_LAMBDA
             52_0  COME_FROM            46  '46'

 L.  50        52  LOAD_CONST               True
               54  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `RETURN_VALUE_LAMBDA' instruction at offset 50
, sizes)
    sizes = list(sizes)
    fp.write(struct.pack('<H', len(sizes)))
    offset = fp.tell() + len(sizes) * 16
    provided_images = {im:im.size for im in im.encoderinfo.get('append_images', [])}
    for size in sizes:
        width, height = size
        fp.write(struct.pack('B', width if width < 256 else 0))
        fp.write(struct.pack('B', height if height < 256 else 0))
        fp.write(b'\x00')
        fp.write(b'\x00')
        fp.write(b'\x00\x00')
        fp.write(struct.pack('<H', 32))
        image_io = BytesIO()
        tmp = provided_images.get(size)
        if not tmp:
            tmp = im.copy()
            tmp.thumbnail(size, (Image.LANCZOS), reducing_gap=None)
        else:
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


class IcoFile:

    def __init__(self, buf):
        """
        Parse image from file-like object containing ico file data
        """
        s = buf.read(6)
        if not _accept(s):
            raise SyntaxError('not an ICO file')
        self.buf = buf
        self.entry = []
        self.nb_items = i16(s, 4)
        for i in range(self.nb_items):
            s = buf.read(16)
            icon_header = {'width':s[0], 
             'height':s[1], 
             'nb_color':s[2], 
             'reserved':s[3], 
             'planes':i16(s, 4), 
             'bpp':i16(s, 6), 
             'size':i32(s, 8), 
             'offset':i32(s, 12)}
            for j in ('width', 'height'):
                if not icon_header[j]:
                    icon_header[j] = 256
            else:
                icon_header['color_depth'] = icon_header['bpp'] or (icon_header['nb_color'] != 0) and (ceil(log(icon_header['nb_color'], 2))) or 256
                icon_header['dim'] = (
                 icon_header['width'], icon_header['height'])
                icon_header['square'] = icon_header['width'] * icon_header['height']
                self.entry.append(icon_header)

        else:
            self.entry = sorted((self.entry), key=(lambda x: x['color_depth']))
            self.entry = sorted((self.entry), key=(lambda x: x['square']))
            self.entry.reverse()

    def sizes(self):
        """
        Get a list of all available icon sizes and color depths.
        """
        return {(
         h['width'], h['height']) for h in self.entry}

    def getentryindex(self, size, bpp=False):
        for i, h in enumerate(self.entry):
            if size == h['dim']:
                if not bpp is False:
                    if bpp == h['color_depth']:
                        pass
                return i
        else:
            return 0

    def getimage(self, size, bpp=False):
        """
        Get an image from the icon
        """
        return self.frame(self.getentryindex(size, bpp))

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
            Image._decompression_bomb_check(im.size)
        else:
            im = BmpImagePlugin.DibImageFile(self.buf)
            Image._decompression_bomb_check(im.size)
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
            else:
                if 32 == bpp:
                    self.buf.seek(o)
                    alpha_bytes = self.buf.read(im.size[0] * im.size[1] * 4)[3::4]
                    mask = Image.frombuffer('L', im.size, alpha_bytes, 'raw', ('L',
                                                                               0,
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
    __doc__ = "\n    PIL read-only image support for Microsoft Windows .ico files.\n\n    By default the largest resolution image in the file will be loaded. This\n    can be changed by altering the 'size' attribute before calling 'load'.\n\n    The info dictionary has a key 'sizes' that is a list of the sizes available\n    in the icon file.\n\n    Handles classic, XP and Vista icon formats.\n\n    When saving, PNG compression is used. Support for this was only added in\n    Windows Vista.\n\n    This plugin is a refactored version of Win32IconImagePlugin by Bryan Davis\n    <casadebender@gmail.com>.\n    https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki\n    "
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
        if self.im:
            if self.im.size == self.size:
                return
        im = self.ico.getimage(self.size)
        im.load()
        self.im = im.im
        self.mode = im.mode
        if im.size != self.size:
            warnings.warn('Image was not the expected size')
            index = self.ico.getentryindex(self.size)
            sizes = list(self.info['sizes'])
            sizes[index] = im.size
            self.info['sizes'] = set(sizes)
            self.size = im.size

    def load_seek(self):
        pass


Image.register_open(IcoImageFile.format, IcoImageFile, _accept)
Image.register_save(IcoImageFile.format, _save)
Image.register_extension(IcoImageFile.format, '.ico')
Image.register_mime(IcoImageFile.format, 'image/x-icon')