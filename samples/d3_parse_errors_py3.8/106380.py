# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\ImagePalette.py
import array
from . import GimpGradientFile, GimpPaletteFile, ImageColor, PaletteFile

class ImagePalette:
    __doc__ = '\n    Color palette for palette mapped images\n\n    :param mode: The mode to use for the Palette. See:\n        :ref:`concept-modes`. Defaults to "RGB"\n    :param palette: An optional palette. If given, it must be a bytearray,\n        an array or a list of ints between 0-255 and of length ``size``\n        times the number of colors in ``mode``. The list must be aligned\n        by channel (All R values must be contiguous in the list before G\n        and B values.) Defaults to 0 through 255 per channel.\n    :param size: An optional palette size. If given, it cannot be equal to\n        or greater than 256. Defaults to 0.\n    '

    def __init__(self, mode='RGB', palette=None, size=0):
        self.mode = mode
        self.rawmode = None
        self.palette = palette or bytearray(range(256)) * len(self.mode)
        self.colors = {}
        self.dirty = None
        if size == 0 and not len(self.mode) * 256 != len(self.palette):
            if not size != 0 or size != len(self.palette):
                raise ValueError('wrong palette size')

    def copy(self):
        new = ImagePalette()
        new.mode = self.mode
        new.rawmode = self.rawmode
        if self.palette is not None:
            new.palette = self.palette[:]
        new.colors = self.colors.copy()
        new.dirty = self.dirty
        return new

    def getdata(self):
        """
        Get palette contents in format suitable for the low-level
        ``im.putpalette`` primitive.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            return (self.rawmode, self.palette)
        return (self.mode + ';L', self.tobytes())

    def tobytes(self):
        """Convert palette to bytes.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if isinstance(self.palette, bytes):
            return self.palette
        arr = array.array('B', self.palette)
        if hasattr(arr, 'tobytes'):
            return arr.tobytes()
        return arr.tostring()

    tostring = tobytes

    def getcolor(self, color):
        """Given an rgb tuple, allocate palette entry.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if isinstance(color, tuple):
            try:
                return self.colors[color]
            except KeyError:
                if isinstance(self.palette, bytes):
                    self.palette = bytearray(self.palette)
                index = len(self.colors)
                if index >= 256:
                    raise ValueError('cannot allocate more than 256 colors')
                self.colors[color] = index
                self.palette[index] = color[0]
                self.palette[index + 256] = color[1]
                self.palette[index + 512] = color[2]
                self.dirty = 1
                return index

        else:
            raise ValueError('unknown color specifier: %r' % color)

    def save(self, fp):
        """Save palette to text file.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if isinstance(fp, str):
            fp = open(fp, 'w')
        fp.write('# Palette\n')
        fp.write('# Mode: %s\n' % self.mode)
        for i in range(256):
            fp.write('%d' % i)
            for j in range(i * len(self.mode), (i + 1) * len(self.mode)):
                try:
                    fp.write(' %d' % self.palette[j])
                except IndexError:
                    fp.write(' 0')

            else:
                fp.write('\n')

        else:
            fp.close()


def raw(rawmode, data):
    palette = ImagePalette()
    palette.rawmode = rawmode
    palette.palette = data
    palette.dirty = 1
    return palette


def make_linear_lut(black, white):
    lut = []
    if black == 0:
        for i in range(256):
            lut.append(white * i // 255)

    else:
        raise NotImplementedError
    return lut


def make_gamma_lut(exp):
    lut = []
    for i in range(256):
        lut.append(int((i / 255.0) ** exp * 255.0 + 0.5))
    else:
        return lut


def negative(mode='RGB'):
    palette = list(range(256))
    palette.reverse()
    return ImagePalette(mode, palette * len(mode))


def random(mode='RGB'):
    from random import randint
    palette = []
    for i in range(256 * len(mode)):
        palette.append(randint(0, 255))
    else:
        return ImagePalette(mode, palette)


def sepia(white='#fff0c0'):
    r, g, b = ImageColor.getrgb(white)
    r = make_linear_lut(0, r)
    g = make_linear_lut(0, g)
    b = make_linear_lut(0, b)
    return ImagePalette('RGB', r + g + b)


def wedge(mode='RGB'):
    return ImagePalette(mode, list(range(256)) * len(mode))


def load--- This code section failed: ---

 L. 202         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH          108  'to 108'
               10  STORE_FAST               'fp'

 L. 205        12  LOAD_GLOBAL              GimpPaletteFile
               14  LOAD_ATTR                GimpPaletteFile

 L. 206        16  LOAD_GLOBAL              GimpGradientFile
               18  LOAD_ATTR                GimpGradientFile

 L. 207        20  LOAD_GLOBAL              PaletteFile
               22  LOAD_ATTR                PaletteFile

 L. 204        24  BUILD_TUPLE_3         3 
               26  GET_ITER         
             28_0  COME_FROM            94  '94'
             28_1  COME_FROM            90  '90'
             28_2  COME_FROM            68  '68'
               28  FOR_ITER             96  'to 96'
               30  STORE_FAST               'paletteHandler'

 L. 209        32  SETUP_FINALLY        70  'to 70'

 L. 210        34  LOAD_FAST                'fp'
               36  LOAD_METHOD              seek
               38  LOAD_CONST               0
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 211        44  LOAD_FAST                'paletteHandler'
               46  LOAD_FAST                'fp'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_METHOD              getpalette
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'lut'

 L. 212        56  LOAD_FAST                'lut'
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 213        60  POP_BLOCK        
               62  POP_TOP          
               64  JUMP_FORWARD        104  'to 104'
             66_0  COME_FROM            58  '58'
               66  POP_BLOCK        
               68  JUMP_BACK            28  'to 28'
             70_0  COME_FROM_FINALLY    32  '32'

 L. 214        70  DUP_TOP          
               72  LOAD_GLOBAL              SyntaxError
               74  LOAD_GLOBAL              ValueError
               76  BUILD_TUPLE_2         2 
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    92  'to 92'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 217        88  POP_EXCEPT       
               90  JUMP_BACK            28  'to 28'
             92_0  COME_FROM            80  '80'
               92  END_FINALLY      
               94  JUMP_BACK            28  'to 28'
             96_0  COME_FROM            28  '28'

 L. 219        96  LOAD_GLOBAL              OSError
               98  LOAD_STR                 'cannot load palette'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            64  '64'
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_WITH        8  '8'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

 L. 221       114  LOAD_FAST                'lut'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 106