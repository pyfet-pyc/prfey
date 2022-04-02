# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageFilter.py
import functools

class Filter:
    pass


class MultibandFilter(Filter):
    pass


class BuiltinFilter(MultibandFilter):

    def filter(self, image):
        if image.mode == 'P':
            raise ValueError('cannot filter palette images')
        return (image.filter)(*self.filterargs)


class Kernel(BuiltinFilter):
    __doc__ = '\n    Create a convolution kernel.  The current version only\n    supports 3x3 and 5x5 integer and floating point kernels.\n\n    In the current version, kernels can only be applied to\n    "L" and "RGB" images.\n\n    :param size: Kernel size, given as (width, height). In the current\n                    version, this must be (3,3) or (5,5).\n    :param kernel: A sequence containing kernel weights.\n    :param scale: Scale factor. If given, the result for each pixel is\n                    divided by this value.  The default is the sum of the\n                    kernel weights.\n    :param offset: Offset. If given, this value is added to the result,\n                    after it has been divided by the scale factor.\n    '
    name = 'Kernel'

    def __init__--- This code section failed: ---

 L.  56         0  LOAD_FAST                'scale'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  58         8  LOAD_GLOBAL              functools
               10  LOAD_METHOD              reduce
               12  LOAD_LAMBDA              '<code_object <lambda>>'
               14  LOAD_STR                 'Kernel.__init__.<locals>.<lambda>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_FAST                'kernel'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'scale'
             24_0  COME_FROM             6  '6'

 L.  59        24  LOAD_FAST                'size'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'size'
               32  LOAD_CONST               1
               34  BINARY_SUBSCR    
               36  BINARY_MULTIPLY  
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'kernel'
               42  CALL_FUNCTION_1       1  ''
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  60        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'not enough coefficients in kernel'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  61        56  LOAD_FAST                'size'
               58  LOAD_FAST                'scale'
               60  LOAD_FAST                'offset'
               62  LOAD_FAST                'kernel'
               64  BUILD_TUPLE_4         4 
               66  LOAD_FAST                'self'
               68  STORE_ATTR               filterargs

Parse error at or near `None' instruction at offset -1


class RankFilter(Filter):
    __doc__ = "\n    Create a rank filter.  The rank filter sorts all pixels in\n    a window of the given size, and returns the ``rank``'th value.\n\n    :param size: The kernel size, in pixels.\n    :param rank: What pixel value to pick.  Use 0 for a min filter,\n                 ``size * size / 2`` for a median filter, ``size * size - 1``\n                 for a max filter, etc.\n    "
    name = 'Rank'

    def __init__(self, size, rank):
        self.size = size
        self.rank = rank

    def filter(self, image):
        if image.mode == 'P':
            raise ValueError('cannot filter palette images')
        image = image.expand(self.size // 2)(self.size // 2)
        return image.rankfilterself.sizeself.rank


class MedianFilter(RankFilter):
    __doc__ = '\n    Create a median filter. Picks the median pixel value in a window with the\n    given size.\n\n    :param size: The kernel size, in pixels.\n    '
    name = 'Median'

    def __init__(self, size=3):
        self.size = size
        self.rank = size * size // 2


class MinFilter(RankFilter):
    __doc__ = '\n    Create a min filter.  Picks the lowest pixel value in a window with the\n    given size.\n\n    :param size: The kernel size, in pixels.\n    '
    name = 'Min'

    def __init__(self, size=3):
        self.size = size
        self.rank = 0


class MaxFilter(RankFilter):
    __doc__ = '\n    Create a max filter.  Picks the largest pixel value in a window with the\n    given size.\n\n    :param size: The kernel size, in pixels.\n    '
    name = 'Max'

    def __init__(self, size=3):
        self.size = size
        self.rank = size * size - 1


class ModeFilter(Filter):
    __doc__ = '\n    Create a mode filter. Picks the most frequent pixel value in a box with the\n    given size.  Pixel values that occur only once or twice are ignored; if no\n    pixel value occurs more than twice, the original pixel value is preserved.\n\n    :param size: The kernel size, in pixels.\n    '
    name = 'Mode'

    def __init__(self, size=3):
        self.size = size

    def filter(self, image):
        return image.modefilter(self.size)


class GaussianBlur(MultibandFilter):
    __doc__ = 'Gaussian blur filter.\n\n    :param radius: Blur radius.\n    '
    name = 'GaussianBlur'

    def __init__(self, radius=2):
        self.radius = radius

    def filter(self, image):
        return image.gaussian_blur(self.radius)


class BoxBlur(MultibandFilter):
    __doc__ = 'Blurs the image by setting each pixel to the average value of the pixels\n    in a square box extending radius pixels in each direction.\n    Supports float radius of arbitrary size. Uses an optimized implementation\n    which runs in linear time relative to the size of the image\n    for any radius value.\n\n    :param radius: Size of the box in one direction. Radius 0 does not blur,\n                   returns an identical image. Radius 1 takes 1 pixel\n                   in each direction, i.e. 9 pixels in total.\n    '
    name = 'BoxBlur'

    def __init__(self, radius):
        self.radius = radius

    def filter(self, image):
        return image.box_blur(self.radius)


class UnsharpMask(MultibandFilter):
    __doc__ = "Unsharp mask filter.\n\n    See Wikipedia's entry on `digital unsharp masking`_ for an explanation of\n    the parameters.\n\n    :param radius: Blur Radius\n    :param percent: Unsharp strength, in percent\n    :param threshold: Threshold controls the minimum brightness change that\n      will be sharpened\n\n    .. _digital unsharp masking: https://en.wikipedia.org/wiki/Unsharp_masking#Digital_unsharp_masking\n\n    "
    name = 'UnsharpMask'

    def __init__(self, radius=2, percent=150, threshold=3):
        self.radius = radius
        self.percent = percent
        self.threshold = threshold

    def filter(self, image):
        return image.unsharp_mask(self.radius, self.percent, self.threshold)


class BLUR(BuiltinFilter):
    name = 'Blur'
    filterargs = ((5, 5), 16, 0, (1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1))


class CONTOUR(BuiltinFilter):
    name = 'Contour'
    filterargs = ((3, 3), 1, 255, (-1, -1, -1, -1, 8, -1, -1, -1, -1))


class DETAIL(BuiltinFilter):
    name = 'Detail'
    filterargs = ((3, 3), 6, 0, (0, -1, 0, -1, 10, -1, 0, -1, 0))


class EDGE_ENHANCE(BuiltinFilter):
    name = 'Edge-enhance'
    filterargs = ((3, 3), 2, 0, (-1, -1, -1, -1, 10, -1, -1, -1, -1))


class EDGE_ENHANCE_MORE(BuiltinFilter):
    name = 'Edge-enhance More'
    filterargs = ((3, 3), 1, 0, (-1, -1, -1, -1, 9, -1, -1, -1, -1))


class EMBOSS(BuiltinFilter):
    name = 'Emboss'
    filterargs = ((3, 3), 1, 128, (-1, 0, 0, 0, 1, 0, 0, 0, 0))


class FIND_EDGES(BuiltinFilter):
    name = 'Find Edges'
    filterargs = ((3, 3), 1, 0, (-1, -1, -1, -1, 8, -1, -1, -1, -1))


class SHARPEN(BuiltinFilter):
    name = 'Sharpen'
    filterargs = ((3, 3), 16, 0, (-2, -2, -2, -2, 32, -2, -2, -2, -2))


class SMOOTH(BuiltinFilter):
    name = 'Smooth'
    filterargs = ((3, 3), 13, 0, (1, 1, 1, 1, 5, 1, 1, 1, 1))


class SMOOTH_MORE(BuiltinFilter):
    name = 'Smooth More'
    filterargs = ((5, 5), 100, 0, (1, 1, 1, 1, 1, 1, 5, 5, 5, 1, 1, 5, 44, 5, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1))


class Color3DLUT(MultibandFilter):
    __doc__ = "Three-dimensional color lookup table.\n\n    Transforms 3-channel pixels using the values of the channels as coordinates\n    in the 3D lookup table and interpolating the nearest elements.\n\n    This method allows you to apply almost any color transformation\n    in constant time by using pre-calculated decimated tables.\n\n    .. versionadded:: 5.2.0\n\n    :param size: Size of the table. One int or tuple of (int, int, int).\n                 Minimal size in any dimension is 2, maximum is 65.\n    :param table: Flat lookup table. A list of ``channels * size**3``\n                  float elements or a list of ``size**3`` channels-sized\n                  tuples with floats. Channels are changed first,\n                  then first dimension, then second, then third.\n                  Value 0.0 corresponds lowest value of output, 1.0 highest.\n    :param channels: Number of channels in the table. Could be 3 or 4.\n                     Default is 3.\n    :param target_mode: A mode for the result image. Should have not less\n                        than ``channels`` channels. Default is ``None``,\n                        which means that mode wouldn't be changed.\n    "
    name = 'Color 3D LUT'

    def __init__--- This code section failed: ---

 L. 355         0  LOAD_FAST                'channels'
                2  LOAD_CONST               (3, 4)
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 356         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Only 3 or 4 output channels are supported'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 357        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _check_size
               20  LOAD_FAST                'size'
               22  CALL_METHOD_1         1  ''
               24  DUP_TOP          
               26  LOAD_FAST                'self'
               28  STORE_ATTR               size
               30  STORE_FAST               'size'

 L. 358        32  LOAD_FAST                'channels'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               channels

 L. 359        38  LOAD_FAST                'target_mode'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               mode

 L. 363        44  LOAD_FAST                'kwargs'
               46  LOAD_METHOD              get
               48  LOAD_STR                 '_copy_table'
               50  LOAD_CONST               True
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'copy_table'

 L. 364        56  LOAD_FAST                'size'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'size'
               64  LOAD_CONST               1
               66  BINARY_SUBSCR    
               68  BINARY_MULTIPLY  
               70  LOAD_FAST                'size'
               72  LOAD_CONST               2
               74  BINARY_SUBSCR    
               76  BINARY_MULTIPLY  
               78  STORE_FAST               'items'

 L. 365        80  LOAD_CONST               False
               82  STORE_FAST               'wrong_size'

 L. 367        84  LOAD_CONST               None
               86  STORE_FAST               'numpy'

 L. 368        88  LOAD_GLOBAL              hasattr
               90  LOAD_FAST                'table'
               92  LOAD_STR                 'shape'
               94  CALL_FUNCTION_2       2  ''
               96  POP_JUMP_IF_FALSE   130  'to 130'

 L. 369        98  SETUP_FINALLY       112  'to 112'

 L. 370       100  LOAD_CONST               0
              102  LOAD_CONST               None
              104  IMPORT_NAME              numpy
              106  STORE_FAST               'numpy'
              108  POP_BLOCK        
              110  JUMP_FORWARD        130  'to 130'
            112_0  COME_FROM_FINALLY    98  '98'

 L. 371       112  DUP_TOP          
              114  LOAD_GLOBAL              ImportError
              116  <121>               128  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 372       124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
              128  <48>             
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           110  '110'
            130_2  COME_FROM            96  '96'

 L. 374       130  LOAD_FAST                'numpy'
              132  POP_JUMP_IF_FALSE   226  'to 226'
              134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'table'
              138  LOAD_FAST                'numpy'
              140  LOAD_ATTR                ndarray
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   226  'to 226'

 L. 375       146  LOAD_FAST                'copy_table'
              148  POP_JUMP_IF_FALSE   158  'to 158'

 L. 376       150  LOAD_FAST                'table'
              152  LOAD_METHOD              copy
              154  CALL_METHOD_0         0  ''
              156  STORE_FAST               'table'
            158_0  COME_FROM           148  '148'

 L. 378       158  LOAD_FAST                'table'
              160  LOAD_ATTR                shape

 L. 379       162  LOAD_FAST                'items'
              164  LOAD_FAST                'channels'
              166  BINARY_MULTIPLY  
              168  BUILD_TUPLE_1         1 

 L. 380       170  LOAD_FAST                'items'
              172  LOAD_FAST                'channels'
              174  BUILD_TUPLE_2         2 

 L. 381       176  LOAD_FAST                'size'
              178  LOAD_CONST               2
              180  BINARY_SUBSCR    
              182  LOAD_FAST                'size'
              184  LOAD_CONST               1
              186  BINARY_SUBSCR    
              188  LOAD_FAST                'size'
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  LOAD_FAST                'channels'
              196  BUILD_TUPLE_4         4 

 L. 378       198  BUILD_TUPLE_3         3 
              200  <118>                 0  ''
              202  POP_JUMP_IF_FALSE   220  'to 220'

 L. 383       204  LOAD_FAST                'table'
              206  LOAD_METHOD              reshape
              208  LOAD_FAST                'items'
              210  LOAD_FAST                'channels'
              212  BINARY_MULTIPLY  
              214  CALL_METHOD_1         1  ''
              216  STORE_FAST               'table'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           202  '202'

 L. 385       220  LOAD_CONST               True
              222  STORE_FAST               'wrong_size'
            224_0  COME_FROM           218  '218'
              224  JUMP_FORWARD        324  'to 324'
            226_0  COME_FROM           144  '144'
            226_1  COME_FROM           132  '132'

 L. 388       226  LOAD_FAST                'copy_table'
              228  POP_JUMP_IF_FALSE   238  'to 238'

 L. 389       230  LOAD_GLOBAL              list
              232  LOAD_FAST                'table'
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'table'
            238_0  COME_FROM           228  '228'

 L. 392       238  LOAD_FAST                'table'
          240_242  POP_JUMP_IF_FALSE   324  'to 324'
              244  LOAD_GLOBAL              isinstance
              246  LOAD_FAST                'table'
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_GLOBAL              list
              254  LOAD_GLOBAL              tuple
              256  BUILD_TUPLE_2         2 
              258  CALL_FUNCTION_2       2  ''
          260_262  POP_JUMP_IF_FALSE   324  'to 324'

 L. 393       264  BUILD_LIST_0          0 
              266  LOAD_FAST                'table'
              268  ROT_TWO          
              270  STORE_FAST               'table'
              272  STORE_FAST               'raw_table'

 L. 394       274  LOAD_FAST                'raw_table'
              276  GET_ITER         
            278_0  COME_FROM           320  '320'
              278  FOR_ITER            324  'to 324'
              280  STORE_FAST               'pixel'

 L. 395       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'pixel'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_FAST                'channels'
              290  COMPARE_OP               !=
          292_294  POP_JUMP_IF_FALSE   310  'to 310'

 L. 396       296  LOAD_GLOBAL              ValueError

 L. 397       298  LOAD_STR                 'The elements of the table should have a length of {}.'
              300  LOAD_METHOD              format

 L. 398       302  LOAD_FAST                'channels'

 L. 397       304  CALL_METHOD_1         1  ''

 L. 396       306  CALL_FUNCTION_1       1  ''
              308  RAISE_VARARGS_1       1  'exception instance'
            310_0  COME_FROM           292  '292'

 L. 400       310  LOAD_FAST                'table'
              312  LOAD_METHOD              extend
              314  LOAD_FAST                'pixel'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
          320_322  JUMP_BACK           278  'to 278'
            324_0  COME_FROM           278  '278'
            324_1  COME_FROM           260  '260'
            324_2  COME_FROM           240  '240'
            324_3  COME_FROM           224  '224'

 L. 402       324  LOAD_FAST                'wrong_size'
          326_328  POP_JUMP_IF_TRUE    348  'to 348'
              330  LOAD_GLOBAL              len
              332  LOAD_FAST                'table'
              334  CALL_FUNCTION_1       1  ''
              336  LOAD_FAST                'items'
              338  LOAD_FAST                'channels'
              340  BINARY_MULTIPLY  
              342  COMPARE_OP               !=
          344_346  POP_JUMP_IF_FALSE   402  'to 402'
            348_0  COME_FROM           326  '326'

 L. 403       348  LOAD_GLOBAL              ValueError

 L. 404       350  LOAD_STR                 'The table should have either channels * size**3 float items or size**3 items of channels-sized tuples with floats. Table should be: '

 L. 406       352  LOAD_FAST                'channels'

 L. 404       354  FORMAT_VALUE          0  ''
              356  LOAD_STR                 'x'

 L. 406       358  LOAD_FAST                'size'
              360  LOAD_CONST               0
              362  BINARY_SUBSCR    

 L. 404       364  FORMAT_VALUE          0  ''
              366  LOAD_STR                 'x'

 L. 406       368  LOAD_FAST                'size'
              370  LOAD_CONST               1
              372  BINARY_SUBSCR    

 L. 404       374  FORMAT_VALUE          0  ''
              376  LOAD_STR                 'x'

 L. 406       378  LOAD_FAST                'size'
              380  LOAD_CONST               2
              382  BINARY_SUBSCR    

 L. 404       384  FORMAT_VALUE          0  ''
              386  LOAD_STR                 '. Actual length: '

 L. 407       388  LOAD_GLOBAL              len
              390  LOAD_FAST                'table'
              392  CALL_FUNCTION_1       1  ''

 L. 404       394  FORMAT_VALUE          0  ''
              396  BUILD_STRING_10      10 

 L. 403       398  CALL_FUNCTION_1       1  ''
              400  RAISE_VARARGS_1       1  'exception instance'
            402_0  COME_FROM           344  '344'

 L. 409       402  LOAD_FAST                'table'
              404  LOAD_FAST                'self'
              406  STORE_ATTR               table

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _check_size--- This code section failed: ---

 L. 413         0  SETUP_FINALLY        16  'to 16'

 L. 414         2  LOAD_FAST                'size'
                4  UNPACK_SEQUENCE_3     3 
                6  STORE_FAST               '_'
                8  STORE_FAST               '_'
               10  STORE_FAST               '_'
               12  POP_BLOCK        
               14  JUMP_FORWARD         88  'to 88'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 415        16  DUP_TOP          
               18  LOAD_GLOBAL              ValueError
               20  <121>                60  ''
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        52  'to 52'

 L. 416        30  LOAD_GLOBAL              ValueError

 L. 417        32  LOAD_STR                 'Size should be either an integer or a tuple of three integers.'

 L. 416        34  CALL_FUNCTION_1       1  ''

 L. 418        36  LOAD_FAST                'e'

 L. 416        38  RAISE_VARARGS_2       2  'exception instance with __cause__'
               40  POP_BLOCK        
               42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  STORE_FAST               'e'
               48  DELETE_FAST              'e'
               50  JUMP_FORWARD         88  'to 88'
             52_0  COME_FROM_FINALLY    28  '28'
               52  LOAD_CONST               None
               54  STORE_FAST               'e'
               56  DELETE_FAST              'e'
               58  <48>             

 L. 419        60  DUP_TOP          
               62  LOAD_GLOBAL              TypeError
               64  <121>                86  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 420        72  LOAD_FAST                'size'
               74  LOAD_FAST                'size'
               76  LOAD_FAST                'size'
               78  BUILD_TUPLE_3         3 
               80  STORE_FAST               'size'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            50  '50'
             88_2  COME_FROM            14  '14'

 L. 421        88  LOAD_LISTCOMP            '<code_object <listcomp>>'
               90  LOAD_STR                 'Color3DLUT._check_size.<locals>.<listcomp>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               94  LOAD_FAST                'size'
               96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'size'

 L. 422       102  LOAD_FAST                'size'
              104  GET_ITER         
            106_0  COME_FROM           140  '140'
            106_1  COME_FROM           126  '126'
              106  FOR_ITER            142  'to 142'
              108  STORE_FAST               'size1D'

 L. 423       110  LOAD_CONST               2
              112  LOAD_FAST                'size1D'
              114  DUP_TOP          
              116  ROT_THREE        
              118  COMPARE_OP               <=
              120  POP_JUMP_IF_FALSE   130  'to 130'
              122  LOAD_CONST               65
              124  COMPARE_OP               <=
              126  POP_JUMP_IF_TRUE_BACK   106  'to 106'
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           120  '120'
              130  POP_TOP          
            132_0  COME_FROM           128  '128'

 L. 424       132  LOAD_GLOBAL              ValueError
              134  LOAD_STR                 'Size should be in [2, 65] range.'
              136  CALL_FUNCTION_1       1  ''
              138  RAISE_VARARGS_1       1  'exception instance'
              140  JUMP_BACK           106  'to 106'
            142_0  COME_FROM           106  '106'

 L. 425       142  LOAD_FAST                'size'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 20

    @classmethod
    def generate--- This code section failed: ---

 L. 440         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              _check_size
                4  LOAD_FAST                'size'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'size1D'
               12  STORE_FAST               'size2D'
               14  STORE_FAST               'size3D'

 L. 441        16  LOAD_FAST                'channels'
               18  LOAD_CONST               (3, 4)
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 442        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'Only 3 or 4 output channels are supported'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 444        32  LOAD_CONST               0
               34  BUILD_LIST_1          1 
               36  LOAD_FAST                'size1D'
               38  LOAD_FAST                'size2D'
               40  BINARY_MULTIPLY  
               42  LOAD_FAST                'size3D'
               44  BINARY_MULTIPLY  
               46  LOAD_FAST                'channels'
               48  BINARY_MULTIPLY  
               50  BINARY_MULTIPLY  
               52  STORE_FAST               'table'

 L. 445        54  LOAD_CONST               0
               56  STORE_FAST               'idx_out'

 L. 446        58  LOAD_GLOBAL              range
               60  LOAD_FAST                'size3D'
               62  CALL_FUNCTION_1       1  ''
               64  GET_ITER         
             66_0  COME_FROM           154  '154'
               66  FOR_ITER            156  'to 156'
               68  STORE_FAST               'b'

 L. 447        70  LOAD_GLOBAL              range
               72  LOAD_FAST                'size2D'
               74  CALL_FUNCTION_1       1  ''
               76  GET_ITER         
             78_0  COME_FROM           152  '152'
               78  FOR_ITER            154  'to 154'
               80  STORE_FAST               'g'

 L. 448        82  LOAD_GLOBAL              range
               84  LOAD_FAST                'size1D'
               86  CALL_FUNCTION_1       1  ''
               88  GET_ITER         
             90_0  COME_FROM           150  '150'
               90  FOR_ITER            152  'to 152'
               92  STORE_FAST               'r'

 L. 449        94  LOAD_FAST                'callback'

 L. 450        96  LOAD_FAST                'r'
               98  LOAD_FAST                'size1D'
              100  LOAD_CONST               1
              102  BINARY_SUBTRACT  
              104  BINARY_TRUE_DIVIDE
              106  LOAD_FAST                'g'
              108  LOAD_FAST                'size2D'
              110  LOAD_CONST               1
              112  BINARY_SUBTRACT  
              114  BINARY_TRUE_DIVIDE
              116  LOAD_FAST                'b'
              118  LOAD_FAST                'size3D'
              120  LOAD_CONST               1
              122  BINARY_SUBTRACT  
              124  BINARY_TRUE_DIVIDE

 L. 449       126  CALL_FUNCTION_3       3  ''
              128  LOAD_FAST                'table'
              130  LOAD_FAST                'idx_out'
              132  LOAD_FAST                'idx_out'
              134  LOAD_FAST                'channels'
              136  BINARY_ADD       
              138  BUILD_SLICE_2         2 
              140  STORE_SUBSCR     

 L. 452       142  LOAD_FAST                'idx_out'
              144  LOAD_FAST                'channels'
              146  INPLACE_ADD      
              148  STORE_FAST               'idx_out'
              150  JUMP_BACK            90  'to 90'
            152_0  COME_FROM            90  '90'
              152  JUMP_BACK            78  'to 78'
            154_0  COME_FROM            78  '78'
              154  JUMP_BACK            66  'to 66'
            156_0  COME_FROM            66  '66'

 L. 454       156  LOAD_FAST                'cls'

 L. 455       158  LOAD_FAST                'size1D'
              160  LOAD_FAST                'size2D'
              162  LOAD_FAST                'size3D'
              164  BUILD_TUPLE_3         3 

 L. 456       166  LOAD_FAST                'table'

 L. 457       168  LOAD_FAST                'channels'

 L. 458       170  LOAD_FAST                'target_mode'

 L. 459       172  LOAD_CONST               False

 L. 454       174  LOAD_CONST               ('channels', 'target_mode', '_copy_table')
              176  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20

    def transform--- This code section failed: ---

 L. 481         0  LOAD_FAST                'channels'
                2  LOAD_CONST               (None, 3, 4)
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 482         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Only 3 or 4 output channels are supported'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 483        16  LOAD_FAST                'self'
               18  LOAD_ATTR                channels
               20  STORE_FAST               'ch_in'

 L. 484        22  LOAD_FAST                'channels'
               24  JUMP_IF_TRUE_OR_POP    28  'to 28'
               26  LOAD_FAST                'ch_in'
             28_0  COME_FROM            24  '24'
               28  STORE_FAST               'ch_out'

 L. 485        30  LOAD_FAST                'self'
               32  LOAD_ATTR                size
               34  UNPACK_SEQUENCE_3     3 
               36  STORE_FAST               'size1D'
               38  STORE_FAST               'size2D'
               40  STORE_FAST               'size3D'

 L. 487        42  LOAD_CONST               0
               44  BUILD_LIST_1          1 
               46  LOAD_FAST                'size1D'
               48  LOAD_FAST                'size2D'
               50  BINARY_MULTIPLY  
               52  LOAD_FAST                'size3D'
               54  BINARY_MULTIPLY  
               56  LOAD_FAST                'ch_out'
               58  BINARY_MULTIPLY  
               60  BINARY_MULTIPLY  
               62  STORE_FAST               'table'

 L. 488        64  LOAD_CONST               0
               66  STORE_FAST               'idx_in'

 L. 489        68  LOAD_CONST               0
               70  STORE_FAST               'idx_out'

 L. 490        72  LOAD_GLOBAL              range
               74  LOAD_FAST                'size3D'
               76  CALL_FUNCTION_1       1  ''
               78  GET_ITER         
             80_0  COME_FROM           220  '220'
               80  FOR_ITER            222  'to 222'
               82  STORE_FAST               'b'

 L. 491        84  LOAD_GLOBAL              range
               86  LOAD_FAST                'size2D'
               88  CALL_FUNCTION_1       1  ''
               90  GET_ITER         
             92_0  COME_FROM           218  '218'
               92  FOR_ITER            220  'to 220'
               94  STORE_FAST               'g'

 L. 492        96  LOAD_GLOBAL              range
               98  LOAD_FAST                'size1D'
              100  CALL_FUNCTION_1       1  ''
              102  GET_ITER         
            104_0  COME_FROM           216  '216'
              104  FOR_ITER            218  'to 218'
              106  STORE_FAST               'r'

 L. 493       108  LOAD_FAST                'self'
              110  LOAD_ATTR                table
              112  LOAD_FAST                'idx_in'
              114  LOAD_FAST                'idx_in'
              116  LOAD_FAST                'ch_in'
              118  BINARY_ADD       
              120  BUILD_SLICE_2         2 
              122  BINARY_SUBSCR    
              124  STORE_FAST               'values'

 L. 494       126  LOAD_FAST                'with_normals'
              128  POP_JUMP_IF_FALSE   176  'to 176'

 L. 495       130  LOAD_FAST                'callback'

 L. 496       132  LOAD_FAST                'r'
              134  LOAD_FAST                'size1D'
              136  LOAD_CONST               1
              138  BINARY_SUBTRACT  
              140  BINARY_TRUE_DIVIDE

 L. 497       142  LOAD_FAST                'g'
              144  LOAD_FAST                'size2D'
              146  LOAD_CONST               1
              148  BINARY_SUBTRACT  
              150  BINARY_TRUE_DIVIDE

 L. 498       152  LOAD_FAST                'b'
              154  LOAD_FAST                'size3D'
              156  LOAD_CONST               1
              158  BINARY_SUBTRACT  
              160  BINARY_TRUE_DIVIDE

 L. 495       162  BUILD_LIST_3          3 

 L. 499       164  LOAD_FAST                'values'

 L. 495       166  CALL_FINALLY        169  'to 169'
              168  WITH_CLEANUP_FINISH
              170  CALL_FUNCTION_EX      0  'positional arguments only'
              172  STORE_FAST               'values'
              174  JUMP_FORWARD        184  'to 184'
            176_0  COME_FROM           128  '128'

 L. 502       176  LOAD_FAST                'callback'
              178  LOAD_FAST                'values'
              180  CALL_FUNCTION_EX      0  'positional arguments only'
              182  STORE_FAST               'values'
            184_0  COME_FROM           174  '174'

 L. 503       184  LOAD_FAST                'values'
              186  LOAD_FAST                'table'
              188  LOAD_FAST                'idx_out'
              190  LOAD_FAST                'idx_out'
              192  LOAD_FAST                'ch_out'
              194  BINARY_ADD       
              196  BUILD_SLICE_2         2 
              198  STORE_SUBSCR     

 L. 504       200  LOAD_FAST                'idx_in'
              202  LOAD_FAST                'ch_in'
              204  INPLACE_ADD      
              206  STORE_FAST               'idx_in'

 L. 505       208  LOAD_FAST                'idx_out'
              210  LOAD_FAST                'ch_out'
              212  INPLACE_ADD      
              214  STORE_FAST               'idx_out'
              216  JUMP_BACK           104  'to 104'
            218_0  COME_FROM           104  '104'
              218  JUMP_BACK            92  'to 92'
            220_0  COME_FROM            92  '92'
              220  JUMP_BACK            80  'to 80'
            222_0  COME_FROM            80  '80'

 L. 507       222  LOAD_GLOBAL              type
              224  LOAD_FAST                'self'
              226  CALL_FUNCTION_1       1  ''

 L. 508       228  LOAD_FAST                'self'
              230  LOAD_ATTR                size

 L. 509       232  LOAD_FAST                'table'

 L. 510       234  LOAD_FAST                'ch_out'

 L. 511       236  LOAD_FAST                'target_mode'
              238  JUMP_IF_TRUE_OR_POP   244  'to 244'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                mode
            244_0  COME_FROM           238  '238'

 L. 512       244  LOAD_CONST               False

 L. 507       246  LOAD_CONST               ('channels', 'target_mode', '_copy_table')
              248  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        r = [
         f"{self.__class__.__name__} from {self.table.__class__.__name__}",
         ('size={:d}x{:d}x{:d}'.format)(*self.size),
         f"channels={self.channels:d}"]
        if self.mode:
            r.append(f"target_mode={self.mode}")
        return '<{}>'.format(' '.join(r))

    def filter(self, image):
        from . import Image
        return image.color_lut_3d(self.mode or image.mode, Image.LINEAR, self.channels, self.size[0], self.size[1], self.size[2], self.table)