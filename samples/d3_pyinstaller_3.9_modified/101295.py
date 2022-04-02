# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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
        if size == 0 and not len(self.mode) * 256 != len(self.palette):
            if not size != 0 or size != len(self.palette):
                raise ValueError('wrong palette size')

    def copy--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              ImagePalette
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'new'

 L.  53         6  LOAD_FAST                'self'
                8  LOAD_ATTR                mode
               10  LOAD_FAST                'new'
               12  STORE_ATTR               mode

 L.  54        14  LOAD_FAST                'self'
               16  LOAD_ATTR                rawmode
               18  LOAD_FAST                'new'
               20  STORE_ATTR               rawmode

 L.  55        22  LOAD_FAST                'self'
               24  LOAD_ATTR                palette
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L.  56        32  LOAD_FAST                'self'
               34  LOAD_ATTR                palette
               36  LOAD_CONST               None
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_FAST                'new'
               46  STORE_ATTR               palette
             48_0  COME_FROM            30  '30'

 L.  57        48  LOAD_FAST                'self'
               50  LOAD_ATTR                colors
               52  LOAD_METHOD              copy
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'new'
               58  STORE_ATTR               colors

 L.  58        60  LOAD_FAST                'self'
               62  LOAD_ATTR                dirty
               64  LOAD_FAST                'new'
               66  STORE_ATTR               dirty

 L.  60        68  LOAD_FAST                'new'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28

    def getdata(self):
        """
        Get palette contents in format suitable for the low-level
        ``im.putpalette`` primitive.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            return (self.rawmode, self.palette)
        return (self.mode + ';L', self.tobytes)

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
            return arr.tobytes
        return arr.tostring

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
               22  POP_JUMP_IF_FALSE   198  'to 198'

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
               42  <121>               194  ''
               44  POP_TOP          
               46  STORE_FAST               'e'
               48  POP_TOP          
               50  SETUP_FINALLY       186  'to 186'

 L. 102        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                palette
               58  LOAD_GLOBAL              bytes
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L. 103        64  LOAD_GLOBAL              bytearray
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                palette
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'self'
               74  STORE_ATTR               palette
             76_0  COME_FROM            62  '62'

 L. 104        76  LOAD_GLOBAL              len
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                colors
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'index'

 L. 105        86  LOAD_FAST                'index'
               88  LOAD_CONST               256
               90  COMPARE_OP               >=
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 106        94  LOAD_GLOBAL              ValueError
               96  LOAD_STR                 'cannot allocate more than 256 colors'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'e'
              102  RAISE_VARARGS_2       2  'exception instance with __cause__'
            104_0  COME_FROM            92  '92'

 L. 107       104  LOAD_FAST                'index'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                colors
              110  LOAD_FAST                'color'
              112  STORE_SUBSCR     

 L. 108       114  LOAD_FAST                'color'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                palette
              124  LOAD_FAST                'index'
              126  STORE_SUBSCR     

 L. 109       128  LOAD_FAST                'color'
              130  LOAD_CONST               1
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                palette
              138  LOAD_FAST                'index'
              140  LOAD_CONST               256
              142  BINARY_ADD       
              144  STORE_SUBSCR     

 L. 110       146  LOAD_FAST                'color'
              148  LOAD_CONST               2
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                palette
              156  LOAD_FAST                'index'
              158  LOAD_CONST               512
              160  BINARY_ADD       
              162  STORE_SUBSCR     

 L. 111       164  LOAD_CONST               1
              166  LOAD_FAST                'self'
              168  STORE_ATTR               dirty

 L. 112       170  LOAD_FAST                'index'
              172  POP_BLOCK        
              174  ROT_FOUR         
              176  POP_EXCEPT       
              178  LOAD_CONST               None
              180  STORE_FAST               'e'
              182  DELETE_FAST              'e'
              184  RETURN_VALUE     
            186_0  COME_FROM_FINALLY    50  '50'
              186  LOAD_CONST               None
              188  STORE_FAST               'e'
              190  DELETE_FAST              'e'
              192  <48>             
              194  <48>             
              196  JUMP_FORWARD        216  'to 216'
            198_0  COME_FROM            22  '22'

 L. 114       198  LOAD_GLOBAL              ValueError
              200  LOAD_STR                 'unknown color specifier: '
              202  LOAD_GLOBAL              repr
              204  LOAD_FAST                'color'
              206  CALL_FUNCTION_1       1  ''
              208  FORMAT_VALUE          0  ''
              210  BUILD_STRING_2        2 
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           196  '196'

Parse error at or near `<121>' instruction at offset 42

    def save--- This code section failed: ---

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawmode
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 122         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 'palette contains raw palette data'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 123        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'fp'
               18  LOAD_GLOBAL              str
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 124        24  LOAD_GLOBAL              open
               26  LOAD_FAST                'fp'
               28  LOAD_STR                 'w'
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'fp'
             34_0  COME_FROM            22  '22'

 L. 125        34  LOAD_FAST                'fp'
               36  LOAD_METHOD              write
               38  LOAD_STR                 '# Palette\n'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 126        44  LOAD_FAST                'fp'
               46  LOAD_METHOD              write
               48  LOAD_STR                 '# Mode: '
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                mode
               54  FORMAT_VALUE          0  ''
               56  LOAD_STR                 '\n'
               58  BUILD_STRING_3        3 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 127        64  LOAD_GLOBAL              range
               66  LOAD_CONST               256
               68  CALL_FUNCTION_1       1  ''
               70  GET_ITER         
             72_0  COME_FROM           194  '194'
               72  FOR_ITER            196  'to 196'
               74  STORE_FAST               'i'

 L. 128        76  LOAD_FAST                'fp'
               78  LOAD_METHOD              write
               80  LOAD_FAST                'i'
               82  FORMAT_VALUE          0  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 129        88  LOAD_GLOBAL              range
               90  LOAD_FAST                'i'
               92  LOAD_GLOBAL              len
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                mode
               98  CALL_FUNCTION_1       1  ''
              100  BINARY_MULTIPLY  
              102  LOAD_FAST                'i'
              104  LOAD_CONST               1
              106  BINARY_ADD       
              108  LOAD_GLOBAL              len
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                mode
              114  CALL_FUNCTION_1       1  ''
              116  BINARY_MULTIPLY  
              118  CALL_FUNCTION_2       2  ''
              120  GET_ITER         
            122_0  COME_FROM           182  '182'
            122_1  COME_FROM           178  '178'
            122_2  COME_FROM           152  '152'
              122  FOR_ITER            184  'to 184'
              124  STORE_FAST               'j'

 L. 130       126  SETUP_FINALLY       154  'to 154'

 L. 131       128  LOAD_FAST                'fp'
              130  LOAD_METHOD              write
              132  LOAD_STR                 ' '
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                palette
              138  LOAD_FAST                'j'
              140  BINARY_SUBSCR    
              142  FORMAT_VALUE          0  ''
              144  BUILD_STRING_2        2 
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  POP_BLOCK        
              152  JUMP_BACK           122  'to 122'
            154_0  COME_FROM_FINALLY   126  '126'

 L. 132       154  DUP_TOP          
              156  LOAD_GLOBAL              IndexError
              158  <121>               180  ''
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 133       166  LOAD_FAST                'fp'
              168  LOAD_METHOD              write
              170  LOAD_STR                 ' 0'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  POP_EXCEPT       
              178  JUMP_BACK           122  'to 122'
              180  <48>             
              182  JUMP_BACK           122  'to 122'
            184_0  COME_FROM           122  '122'

 L. 134       184  LOAD_FAST                'fp'
              186  LOAD_METHOD              write
              188  LOAD_STR                 '\n'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK            72  'to 72'
            196_0  COME_FROM            72  '72'

 L. 135       196  LOAD_FAST                'fp'
              198  LOAD_METHOD              close
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

Parse error at or near `<121>' instruction at offset 158


def raw(rawmode, data):
    palette = ImagePalette
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
        lut.appendint((i / 255.0) ** exp * 255.0 + 0.5)
    else:
        return lut


def negative(mode='RGB'):
    palette = list(range(256))
    palette.reverse
    return ImagePalette(mode, palette * len(mode))


def random(mode='RGB'):
    from random import randint
    palette = []
    for i in range(256 * len(mode)):
        palette.appendrandint(0, 255)
    else:
        return ImagePalette(mode, palette)


def sepia(white='#fff0c0'):
    r, g, b = ImageColor.getrgbwhite
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
                8  SETUP_WITH          116  'to 116'
               10  STORE_FAST               'fp'

 L. 205        12  LOAD_GLOBAL              GimpPaletteFile
               14  LOAD_ATTR                GimpPaletteFile

 L. 206        16  LOAD_GLOBAL              GimpGradientFile
               18  LOAD_ATTR                GimpGradientFile

 L. 207        20  LOAD_GLOBAL              PaletteFile
               22  LOAD_ATTR                PaletteFile

 L. 204        24  BUILD_TUPLE_3         3 
               26  GET_ITER         
             28_0  COME_FROM            92  '92'
             28_1  COME_FROM            88  '88'
             28_2  COME_FROM            68  '68'
               28  FOR_ITER             94  'to 94'
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
               64  JUMP_FORWARD        102  'to 102'
             66_0  COME_FROM            58  '58'
               66  POP_BLOCK        
               68  JUMP_BACK            28  'to 28'
             70_0  COME_FROM_FINALLY    32  '32'

 L. 214        70  DUP_TOP          
               72  LOAD_GLOBAL              SyntaxError
               74  LOAD_GLOBAL              ValueError
               76  BUILD_TUPLE_2         2 
               78  <121>                90  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 217        86  POP_EXCEPT       
               88  JUMP_BACK            28  'to 28'
               90  <48>             
               92  JUMP_BACK            28  'to 28'
             94_0  COME_FROM            28  '28'

 L. 219        94  LOAD_GLOBAL              OSError
               96  LOAD_STR                 'cannot load palette'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            64  '64'
              102  POP_BLOCK        
              104  LOAD_CONST               None
              106  DUP_TOP          
              108  DUP_TOP          
              110  CALL_FUNCTION_3       3  ''
              112  POP_TOP          
              114  JUMP_FORWARD        132  'to 132'
            116_0  COME_FROM_WITH        8  '8'
              116  <49>             
              118  POP_JUMP_IF_TRUE    122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          
              128  POP_EXCEPT       
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L. 221       132  LOAD_FAST                'lut'
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 78