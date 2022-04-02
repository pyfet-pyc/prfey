# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\ImagePalette.py
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
        if size == 0 and len(self.mode) * 256 != len(self.palette) or size != 0:
            if size != len(self.palette):
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
            return (
             self.rawmode, self.palette)
        return (
         self.mode + ';L', self.tobytes())

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

    def getcolor--- This code section failed: ---

 L.  95         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawmode
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L.  96         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 'palette contains raw palette data'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.  97        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'color'
               18  LOAD_GLOBAL              tuple
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE   200  'to 200'

 L.  98        24  SETUP_FINALLY        38  'to 38'

 L.  99        26  LOAD_FAST                'self'
               28  LOAD_ATTR                colors
               30  LOAD_FAST                'color'
               32  BINARY_SUBSCR    
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 100        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   196  'to 196'
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY       184  'to 184'

 L. 102        54  LOAD_GLOBAL              isinstance
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                palette
               60  LOAD_GLOBAL              bytes
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE    78  'to 78'

 L. 103        66  LOAD_GLOBAL              bytearray
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                palette
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_FAST                'self'
               76  STORE_ATTR               palette
             78_0  COME_FROM            64  '64'

 L. 104        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                colors
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'index'

 L. 105        88  LOAD_FAST                'index'
               90  LOAD_CONST               256
               92  COMPARE_OP               >=
               94  POP_JUMP_IF_FALSE   106  'to 106'

 L. 106        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'cannot allocate more than 256 colors'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_FAST                'e'
              104  RAISE_VARARGS_2       2  'exception instance with __cause__'
            106_0  COME_FROM            94  '94'

 L. 107       106  LOAD_FAST                'index'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                colors
              112  LOAD_FAST                'color'
              114  STORE_SUBSCR     

 L. 108       116  LOAD_FAST                'color'
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                palette
              126  LOAD_FAST                'index'
              128  STORE_SUBSCR     

 L. 109       130  LOAD_FAST                'color'
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                palette
              140  LOAD_FAST                'index'
              142  LOAD_CONST               256
              144  BINARY_ADD       
              146  STORE_SUBSCR     

 L. 110       148  LOAD_FAST                'color'
              150  LOAD_CONST               2
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                palette
              158  LOAD_FAST                'index'
              160  LOAD_CONST               512
              162  BINARY_ADD       
              164  STORE_SUBSCR     

 L. 111       166  LOAD_CONST               1
              168  LOAD_FAST                'self'
              170  STORE_ATTR               dirty

 L. 112       172  LOAD_FAST                'index'
              174  ROT_FOUR         
              176  POP_BLOCK        
              178  POP_EXCEPT       
              180  CALL_FINALLY        184  'to 184'
              182  RETURN_VALUE     
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM_FINALLY    52  '52'
              184  LOAD_CONST               None
              186  STORE_FAST               'e'
              188  DELETE_FAST              'e'
              190  END_FINALLY      
              192  POP_EXCEPT       
              194  JUMP_ABSOLUTE       212  'to 212'
            196_0  COME_FROM            44  '44'
              196  END_FINALLY      
              198  JUMP_FORWARD        212  'to 212'
            200_0  COME_FROM            22  '22'

 L. 114       200  LOAD_GLOBAL              ValueError
              202  LOAD_STR                 'unknown color specifier: %r'
              204  LOAD_FAST                'color'
              206  BINARY_MODULO    
              208  CALL_FUNCTION_1       1  ''
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           198  '198'

Parse error at or near `POP_BLOCK' instruction at offset 176

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
               64  JUMP_ABSOLUTE       104  'to 104'
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

 L. 219        96  LOAD_GLOBAL              OSError
               98  LOAD_STR                 'cannot load palette'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_WITH        8  '8'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

 L. 221       114  LOAD_FAST                'lut'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 64