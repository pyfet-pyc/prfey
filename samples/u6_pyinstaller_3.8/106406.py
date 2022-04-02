# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PyAccess.py
import logging, sys
from cffi import FFI
logger = logging.getLogger(__name__)
defs = '\nstruct Pixel_RGBA {\n    unsigned char r,g,b,a;\n};\nstruct Pixel_I16 {\n    unsigned char l,r;\n};\n'
ffi = FFI()
ffi.cdef(defs)

class PyAccess:

    def __init__(self, img, readonly=False):
        vals = dict(img.im.unsafe_ptrs)
        self.readonly = readonly
        self.image8 = ffi.cast('unsigned char **', vals['image8'])
        self.image32 = ffi.cast('int **', vals['image32'])
        self.image = ffi.cast('unsigned char **', vals['image'])
        self.xsize, self.ysize = img.im.size
        self._im = img.im
        if self._im.mode == 'P':
            self._palette = img.palette
        self._post_init()

    def _post_init(self):
        pass

    def __setitem__(self, xy, color):
        """
        Modifies the pixel at x,y. The color is given as a single
        numerical value for single band images, and a tuple for
        multi-band images

        :param xy: The pixel coordinate, given as (x, y). See
           :ref:`coordinate-system`.
        :param color: The pixel value.
        """
        if self.readonly:
            raise ValueError('Attempt to putpixel a read only image')
        else:
            x, y = xy
            if x < 0:
                x = self.xsize + x
            if y < 0:
                y = self.ysize + y
            x, y = self.check_xy((x, y))
            if self._im.mode == 'P':
                if isinstance(color, (list, tuple)) and len(color) in (3, 4):
                    color = self._palette.getcolor(color)
        return self.set_pixel(x, y, color)

    def __getitem__(self, xy):
        """
        Returns the pixel at x,y. The pixel is returned as a single
        value for single band images or a tuple for multiple band
        images

        :param xy: The pixel coordinate, given as (x, y). See
          :ref:`coordinate-system`.
        :returns: a pixel value for single band images, a tuple of
          pixel values for multiband images.
        """
        x, y = xy
        if x < 0:
            x = self.xsize + x
        if y < 0:
            y = self.ysize + y
        x, y = self.check_xy((x, y))
        return self.get_pixel(x, y)

    putpixel = __setitem__
    getpixel = __getitem__

    def check_xy--- This code section failed: ---

 L. 117         0  LOAD_FAST                'xy'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'x'
                6  STORE_FAST               'y'

 L. 118         8  LOAD_CONST               0
               10  LOAD_FAST                'x'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               <=
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                xsize
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    58  'to 58'
               28  JUMP_FORWARD         34  'to 34'
             30_0  COME_FROM            18  '18'
               30  POP_TOP          
               32  JUMP_FORWARD         58  'to 58'
             34_0  COME_FROM            28  '28'
               34  LOAD_CONST               0
               36  LOAD_FAST                'y'
               38  DUP_TOP          
               40  ROT_THREE        
               42  COMPARE_OP               <=
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ysize
               50  COMPARE_OP               <
               52  POP_JUMP_IF_TRUE     66  'to 66'
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            44  '44'
               56  POP_TOP          
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            32  '32'
             58_2  COME_FROM            26  '26'

 L. 119        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'pixel location out of range'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            52  '52'

 L. 120        66  LOAD_FAST                'xy'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 68


class _PyAccess32_2(PyAccess):
    __doc__ = ' PA, LA, stored in first and last bytes of a 32 bit word '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('struct Pixel_RGBA **', self.image32)

    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return (pixel.r, pixel.a)

    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        pixel.r = min(color[0], 255)
        pixel.a = min(color[1], 255)


class _PyAccess32_3(PyAccess):
    __doc__ = ' RGB and friends, stored in the first three bytes of a 32 bit word '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('struct Pixel_RGBA **', self.image32)

    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return (pixel.r, pixel.g, pixel.b)

    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        pixel.r = min(color[0], 255)
        pixel.g = min(color[1], 255)
        pixel.b = min(color[2], 255)
        pixel.a = 255


class _PyAccess32_4(PyAccess):
    __doc__ = ' RGBA etc, all 4 bytes of a 32 bit word '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('struct Pixel_RGBA **', self.image32)

    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return (pixel.r, pixel.g, pixel.b, pixel.a)

    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        pixel.r = min(color[0], 255)
        pixel.g = min(color[1], 255)
        pixel.b = min(color[2], 255)
        pixel.a = min(color[3], 255)


class _PyAccess8(PyAccess):
    __doc__ = ' 1, L, P, 8 bit images stored as uint8 '

    def _post_init(self, *args, **kwargs):
        self.pixels = self.image8

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def set_pixel(self, x, y, color):
        try:
            self.pixels[y][x] = min(color, 255)
        except TypeError:
            self.pixels[y][x] = min(color[0], 255)


class _PyAccessI16_N(PyAccess):
    __doc__ = ' I;16 access, native bitendian without conversion '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('unsigned short **', self.image)

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def set_pixel(self, x, y, color):
        try:
            self.pixels[y][x] = min(color, 65535)
        except TypeError:
            self.pixels[y][x] = min(color[0], 65535)


class _PyAccessI16_L(PyAccess):
    __doc__ = ' I;16L access, with conversion '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('struct Pixel_I16 **', self.image)

    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return pixel.l + pixel.r * 256

    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        try:
            color = min(color, 65535)
        except TypeError:
            color = min(color[0], 65535)
        else:
            pixel.l = color & 255
            pixel.r = color >> 8


class _PyAccessI16_B(PyAccess):
    __doc__ = ' I;16B access, with conversion '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('struct Pixel_I16 **', self.image)

    def get_pixel(self, x, y):
        pixel = self.pixels[y][x]
        return pixel.l * 256 + pixel.r

    def set_pixel(self, x, y, color):
        pixel = self.pixels[y][x]
        try:
            color = min(color, 65535)
        except Exception:
            color = min(color[0], 65535)
        else:
            pixel.l = color >> 8
            pixel.r = color & 255


class _PyAccessI32_N(PyAccess):
    __doc__ = ' Signed Int32 access, native endian '

    def _post_init(self, *args, **kwargs):
        self.pixels = self.image32

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color


class _PyAccessI32_Swap(PyAccess):
    __doc__ = ' I;32L/B access, with byteswapping conversion '

    def _post_init(self, *args, **kwargs):
        self.pixels = self.image32

    def reverse(self, i):
        orig = ffi.new('int *', i)
        chars = ffi.cast('unsigned char *', orig)
        chars[0], chars[1], chars[2], chars[3] = (chars[3], chars[2], chars[1], chars[0])
        return ffi.cast('int *', chars)[0]

    def get_pixel(self, x, y):
        return self.reverse(self.pixels[y][x])

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = self.reverse(color)


class _PyAccessF(PyAccess):
    __doc__ = ' 32 bit float access '

    def _post_init(self, *args, **kwargs):
        self.pixels = ffi.cast('float **', self.image32)

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def set_pixel(self, x, y, color):
        try:
            self.pixels[y][x] = color
        except TypeError:
            self.pixels[y][x] = color[0]


mode_map = {'1':_PyAccess8, 
 'L':_PyAccess8, 
 'P':_PyAccess8, 
 'LA':_PyAccess32_2, 
 'La':_PyAccess32_2, 
 'PA':_PyAccess32_2, 
 'RGB':_PyAccess32_3, 
 'LAB':_PyAccess32_3, 
 'HSV':_PyAccess32_3, 
 'YCbCr':_PyAccess32_3, 
 'RGBA':_PyAccess32_4, 
 'RGBa':_PyAccess32_4, 
 'RGBX':_PyAccess32_4, 
 'CMYK':_PyAccess32_4, 
 'F':_PyAccessF, 
 'I':_PyAccessI32_N}
if sys.byteorder == 'little':
    mode_map['I;16'] = _PyAccessI16_N
    mode_map['I;16L'] = _PyAccessI16_N
    mode_map['I;16B'] = _PyAccessI16_B
    mode_map['I;32L'] = _PyAccessI32_N
    mode_map['I;32B'] = _PyAccessI32_Swap
else:
    mode_map['I;16'] = _PyAccessI16_L
    mode_map['I;16L'] = _PyAccessI16_L
    mode_map['I;16B'] = _PyAccessI16_N
    mode_map['I;32L'] = _PyAccessI32_Swap
    mode_map['I;32B'] = _PyAccessI32_N

def new(img, readonly=False):
    access_type = mode_map.get(img.mode, None)
    if not access_type:
        logger.debug('PyAccess Not Implemented: %s', img.mode)
        return None
    return access_type(img, readonly)