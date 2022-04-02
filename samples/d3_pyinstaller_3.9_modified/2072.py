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
        self.palette = palette or bytearray()
        self.dirty = None
        if size != 0:
            if size != len(self.palette):
                raise ValueError('wrong palette size')

    @property
    def palette(self):
        return self._palette

    @palette.setter
    def palette--- This code section failed: ---

 L.  53         0  LOAD_FAST                'palette'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _palette

 L.  55         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                mode
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'mode_len'

 L.  56        16  BUILD_MAP_0           0 
               18  LOAD_FAST                'self'
               20  STORE_ATTR               colors

 L.  57        22  LOAD_GLOBAL              range
               24  LOAD_CONST               0
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                palette
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'mode_len'
               36  CALL_FUNCTION_3       3  ''
               38  GET_ITER         
             40_0  COME_FROM            92  '92'
             40_1  COME_FROM            76  '76'
               40  FOR_ITER             94  'to 94'
               42  STORE_FAST               'i'

 L.  58        44  LOAD_GLOBAL              tuple
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                palette
               50  LOAD_FAST                'i'
               52  LOAD_FAST                'i'
               54  LOAD_FAST                'mode_len'
               56  BINARY_ADD       
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'color'

 L.  59        66  LOAD_FAST                'color'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                colors
               72  <118>                 0  ''
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L.  60        76  JUMP_BACK            40  'to 40'
             78_0  COME_FROM            74  '74'

 L.  61        78  LOAD_FAST                'i'
               80  LOAD_FAST                'mode_len'
               82  BINARY_FLOOR_DIVIDE
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                colors
               88  LOAD_FAST                'color'
               90  STORE_SUBSCR     
               92  JUMP_BACK            40  'to 40'
             94_0  COME_FROM            40  '40'

Parse error at or near `<118>' instruction at offset 72

    def copy--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              ImagePalette
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'new'

 L.  66         6  LOAD_FAST                'self'
                8  LOAD_ATTR                mode
               10  LOAD_FAST                'new'
               12  STORE_ATTR               mode

 L.  67        14  LOAD_FAST                'self'
               16  LOAD_ATTR                rawmode
               18  LOAD_FAST                'new'
               20  STORE_ATTR               rawmode

 L.  68        22  LOAD_FAST                'self'
               24  LOAD_ATTR                palette
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L.  69        32  LOAD_FAST                'self'
               34  LOAD_ATTR                palette
               36  LOAD_CONST               None
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_FAST                'new'
               46  STORE_ATTR               palette
             48_0  COME_FROM            30  '30'

 L.  70        48  LOAD_FAST                'self'
               50  LOAD_ATTR                dirty
               52  LOAD_FAST                'new'
               54  STORE_ATTR               dirty

 L.  72        56  LOAD_FAST                'new'
               58  RETURN_VALUE     
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
        return (self.mode, self.tobytes())

    def tobytes(self):
        """Convert palette to bytes.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            raise ValueError('palette contains raw palette data')
        if isinstance(self.palette, bytes):
            return self.palette
        arr = array.array('B', self.palette)
        return arr.tobytes()

    tostring = tobytes

    def getcolor--- This code section failed: ---

 L. 105         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawmode
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 106         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 'palette contains raw palette data'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 107        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'color'
               18  LOAD_GLOBAL              tuple
               20  CALL_FUNCTION_2       2  ''
            22_24  POP_JUMP_IF_FALSE   456  'to 456'

 L. 108        26  LOAD_FAST                'self'
               28  LOAD_ATTR                mode
               30  LOAD_STR                 'RGB'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    74  'to 74'

 L. 109        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'color'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               4
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE   104  'to 104'
               48  LOAD_FAST                'color'
               50  LOAD_CONST               3
               52  BINARY_SUBSCR    
               54  LOAD_CONST               255
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE   104  'to 104'

 L. 110        60  LOAD_FAST                'color'
               62  LOAD_CONST               None
               64  LOAD_CONST               3
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  STORE_FAST               'color'
               72  JUMP_FORWARD        104  'to 104'
             74_0  COME_FROM            34  '34'

 L. 111        74  LOAD_FAST                'self'
               76  LOAD_ATTR                mode
               78  LOAD_STR                 'RGBA'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   104  'to 104'

 L. 112        84  LOAD_GLOBAL              len
               86  LOAD_FAST                'color'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_CONST               3
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 113        96  LOAD_FAST                'color'
               98  LOAD_CONST               (255,)
              100  INPLACE_ADD      
              102  STORE_FAST               'color'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            82  '82'
            104_2  COME_FROM            72  '72'
            104_3  COME_FROM            58  '58'
            104_4  COME_FROM            46  '46'

 L. 114       104  SETUP_FINALLY       118  'to 118'

 L. 115       106  LOAD_FAST                'self'
              108  LOAD_ATTR                colors
              110  LOAD_FAST                'color'
              112  BINARY_SUBSCR    
              114  POP_BLOCK        
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY   104  '104'

 L. 116       118  DUP_TOP          
              120  LOAD_GLOBAL              KeyError
          122_124  <121>               452  ''
              126  POP_TOP          
              128  STORE_FAST               'e'
              130  POP_TOP          
          132_134  SETUP_FINALLY       444  'to 444'

 L. 118       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                palette
              142  LOAD_GLOBAL              bytearray
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_TRUE    160  'to 160'

 L. 119       148  LOAD_GLOBAL              bytearray
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                palette
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _palette
            160_0  COME_FROM           146  '146'

 L. 120       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                palette
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_CONST               3
              170  BINARY_FLOOR_DIVIDE
              172  STORE_FAST               'index'

 L. 121       174  LOAD_CONST               ()
              176  STORE_FAST               'special_colors'

 L. 122       178  LOAD_FAST                'image'
              180  POP_JUMP_IF_FALSE   206  'to 206'

 L. 124       182  LOAD_FAST                'image'
              184  LOAD_ATTR                info
              186  LOAD_METHOD              get
              188  LOAD_STR                 'background'
              190  CALL_METHOD_1         1  ''

 L. 125       192  LOAD_FAST                'image'
              194  LOAD_ATTR                info
              196  LOAD_METHOD              get
              198  LOAD_STR                 'transparency'
              200  CALL_METHOD_1         1  ''

 L. 123       202  BUILD_TUPLE_2         2 
              204  STORE_FAST               'special_colors'
            206_0  COME_FROM           222  '222'
            206_1  COME_FROM           180  '180'

 L. 127       206  LOAD_FAST                'index'
              208  LOAD_FAST                'special_colors'
              210  <118>                 0  ''
              212  POP_JUMP_IF_FALSE   224  'to 224'

 L. 128       214  LOAD_FAST                'index'
              216  LOAD_CONST               1
              218  INPLACE_ADD      
              220  STORE_FAST               'index'
              222  JUMP_BACK           206  'to 206'
            224_0  COME_FROM           212  '212'

 L. 129       224  LOAD_FAST                'index'
              226  LOAD_CONST               256
              228  COMPARE_OP               >=
          230_232  POP_JUMP_IF_FALSE   322  'to 322'

 L. 130       234  LOAD_FAST                'image'
          236_238  POP_JUMP_IF_FALSE   302  'to 302'

 L. 132       240  LOAD_GLOBAL              reversed
              242  LOAD_GLOBAL              list
              244  LOAD_GLOBAL              enumerate
              246  LOAD_FAST                'image'
              248  LOAD_METHOD              histogram
              250  CALL_METHOD_0         0  ''
              252  CALL_FUNCTION_1       1  ''
              254  CALL_FUNCTION_1       1  ''
              256  CALL_FUNCTION_1       1  ''
              258  GET_ITER         
            260_0  COME_FROM           298  '298'
            260_1  COME_FROM           284  '284'
            260_2  COME_FROM           274  '274'
              260  FOR_ITER            302  'to 302'
              262  UNPACK_SEQUENCE_2     2 
              264  STORE_FAST               'i'
              266  STORE_FAST               'count'

 L. 133       268  LOAD_FAST                'count'
              270  LOAD_CONST               0
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE_BACK   260  'to 260'
              278  LOAD_FAST                'i'
              280  LOAD_FAST                'special_colors'
              282  <118>                 1  ''
          284_286  POP_JUMP_IF_FALSE_BACK   260  'to 260'

 L. 134       288  LOAD_FAST                'i'
              290  STORE_FAST               'index'

 L. 135       292  POP_TOP          
          294_296  BREAK_LOOP          302  'to 302'
          298_300  JUMP_BACK           260  'to 260'
            302_0  COME_FROM           294  '294'
            302_1  COME_FROM           260  '260'
            302_2  COME_FROM           236  '236'

 L. 136       302  LOAD_FAST                'index'
              304  LOAD_CONST               256
              306  COMPARE_OP               >=
          308_310  POP_JUMP_IF_FALSE   322  'to 322'

 L. 137       312  LOAD_GLOBAL              ValueError
              314  LOAD_STR                 'cannot allocate more than 256 colors'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_FAST                'e'
              320  RAISE_VARARGS_2       2  'exception instance with __cause__'
            322_0  COME_FROM           308  '308'
            322_1  COME_FROM           230  '230'

 L. 138       322  LOAD_FAST                'index'
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                colors
              328  LOAD_FAST                'color'
              330  STORE_SUBSCR     

 L. 139       332  LOAD_FAST                'index'
              334  LOAD_CONST               3
              336  BINARY_MULTIPLY  
              338  LOAD_GLOBAL              len
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                palette
              344  CALL_FUNCTION_1       1  ''
              346  COMPARE_OP               <
          348_350  POP_JUMP_IF_FALSE   404  'to 404'

 L. 141       352  LOAD_FAST                'self'
              354  LOAD_ATTR                palette
              356  LOAD_CONST               None
              358  LOAD_FAST                'index'
              360  LOAD_CONST               3
              362  BINARY_MULTIPLY  
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    

 L. 142       368  LOAD_GLOBAL              bytes
              370  LOAD_FAST                'color'
              372  CALL_FUNCTION_1       1  ''

 L. 141       374  BINARY_ADD       

 L. 143       376  LOAD_FAST                'self'
              378  LOAD_ATTR                palette
              380  LOAD_FAST                'index'
              382  LOAD_CONST               3
              384  BINARY_MULTIPLY  
              386  LOAD_CONST               3
              388  BINARY_ADD       
              390  LOAD_CONST               None
              392  BUILD_SLICE_2         2 
              394  BINARY_SUBSCR    

 L. 141       396  BINARY_ADD       

 L. 140       398  LOAD_FAST                'self'
              400  STORE_ATTR               _palette
              402  JUMP_FORWARD        422  'to 422'
            404_0  COME_FROM           348  '348'

 L. 146       404  LOAD_FAST                'self'
              406  DUP_TOP          
              408  LOAD_ATTR                _palette
              410  LOAD_GLOBAL              bytes
              412  LOAD_FAST                'color'
              414  CALL_FUNCTION_1       1  ''
              416  INPLACE_ADD      
              418  ROT_TWO          
              420  STORE_ATTR               _palette
            422_0  COME_FROM           402  '402'

 L. 147       422  LOAD_CONST               1
              424  LOAD_FAST                'self'
              426  STORE_ATTR               dirty

 L. 148       428  LOAD_FAST                'index'
              430  POP_BLOCK        
              432  ROT_FOUR         
              434  POP_EXCEPT       
              436  LOAD_CONST               None
              438  STORE_FAST               'e'
              440  DELETE_FAST              'e'
              442  RETURN_VALUE     
            444_0  COME_FROM_FINALLY   132  '132'
              444  LOAD_CONST               None
              446  STORE_FAST               'e'
              448  DELETE_FAST              'e'
              450  <48>             
              452  <48>             
              454  JUMP_FORWARD        474  'to 474'
            456_0  COME_FROM            22  '22'

 L. 150       456  LOAD_GLOBAL              ValueError
              458  LOAD_STR                 'unknown color specifier: '
              460  LOAD_GLOBAL              repr
              462  LOAD_FAST                'color'
              464  CALL_FUNCTION_1       1  ''
              466  FORMAT_VALUE          0  ''
              468  BUILD_STRING_2        2 
              470  CALL_FUNCTION_1       1  ''
              472  RAISE_VARARGS_1       1  'exception instance'
            474_0  COME_FROM           454  '454'

Parse error at or near `<121>' instruction at offset 122_124

    def save--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawmode
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 158         6  LOAD_GLOBAL              ValueError
                8  LOAD_STR                 'palette contains raw palette data'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 159        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'fp'
               18  LOAD_GLOBAL              str
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 160        24  LOAD_GLOBAL              open
               26  LOAD_FAST                'fp'
               28  LOAD_STR                 'w'
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'fp'
             34_0  COME_FROM            22  '22'

 L. 161        34  LOAD_FAST                'fp'
               36  LOAD_METHOD              write
               38  LOAD_STR                 '# Palette\n'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 162        44  LOAD_FAST                'fp'
               46  LOAD_METHOD              write
               48  LOAD_STR                 '# Mode: '
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                mode
               54  FORMAT_VALUE          0  ''
               56  LOAD_STR                 '\n'
               58  BUILD_STRING_3        3 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 163        64  LOAD_GLOBAL              range
               66  LOAD_CONST               256
               68  CALL_FUNCTION_1       1  ''
               70  GET_ITER         
             72_0  COME_FROM           194  '194'
               72  FOR_ITER            196  'to 196'
               74  STORE_FAST               'i'

 L. 164        76  LOAD_FAST                'fp'
               78  LOAD_METHOD              write
               80  LOAD_FAST                'i'
               82  FORMAT_VALUE          0  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 165        88  LOAD_GLOBAL              range
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

 L. 166       126  SETUP_FINALLY       154  'to 154'

 L. 167       128  LOAD_FAST                'fp'
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

 L. 168       154  DUP_TOP          
              156  LOAD_GLOBAL              IndexError
              158  <121>               180  ''
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 169       166  LOAD_FAST                'fp'
              168  LOAD_METHOD              write
              170  LOAD_STR                 ' 0'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  POP_EXCEPT       
              178  JUMP_BACK           122  'to 122'
              180  <48>             
              182  JUMP_BACK           122  'to 122'
            184_0  COME_FROM           122  '122'

 L. 170       184  LOAD_FAST                'fp'
              186  LOAD_METHOD              write
              188  LOAD_STR                 '\n'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK            72  'to 72'
            196_0  COME_FROM            72  '72'

 L. 171       196  LOAD_FAST                'fp'
              198  LOAD_METHOD              close
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

Parse error at or near `<121>' instruction at offset 158


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
        lut.appendint((i / 255.0) ** exp * 255.0 + 0.5)
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

 L. 238         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filename'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH          116  'to 116'
               10  STORE_FAST               'fp'

 L. 241        12  LOAD_GLOBAL              GimpPaletteFile
               14  LOAD_ATTR                GimpPaletteFile

 L. 242        16  LOAD_GLOBAL              GimpGradientFile
               18  LOAD_ATTR                GimpGradientFile

 L. 243        20  LOAD_GLOBAL              PaletteFile
               22  LOAD_ATTR                PaletteFile

 L. 240        24  BUILD_TUPLE_3         3 
               26  GET_ITER         
             28_0  COME_FROM            92  '92'
             28_1  COME_FROM            88  '88'
             28_2  COME_FROM            68  '68'
               28  FOR_ITER             94  'to 94'
               30  STORE_FAST               'paletteHandler'

 L. 245        32  SETUP_FINALLY        70  'to 70'

 L. 246        34  LOAD_FAST                'fp'
               36  LOAD_METHOD              seek
               38  LOAD_CONST               0
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 247        44  LOAD_FAST                'paletteHandler'
               46  LOAD_FAST                'fp'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_METHOD              getpalette
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'lut'

 L. 248        56  LOAD_FAST                'lut'
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 249        60  POP_BLOCK        
               62  POP_TOP          
               64  JUMP_FORWARD        102  'to 102'
             66_0  COME_FROM            58  '58'
               66  POP_BLOCK        
               68  JUMP_BACK            28  'to 28'
             70_0  COME_FROM_FINALLY    32  '32'

 L. 250        70  DUP_TOP          
               72  LOAD_GLOBAL              SyntaxError
               74  LOAD_GLOBAL              ValueError
               76  BUILD_TUPLE_2         2 
               78  <121>                90  ''
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 253        86  POP_EXCEPT       
               88  JUMP_BACK            28  'to 28'
               90  <48>             
               92  JUMP_BACK            28  'to 28'
             94_0  COME_FROM            28  '28'

 L. 255        94  LOAD_GLOBAL              OSError
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

 L. 257       132  LOAD_FAST                'lut'
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 78