# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PalmImagePlugin.py
from . import Image, ImageFile
from ._binary import o8
from ._binary import o16be as o16b
_Palm8BitColormapValues = ((255, 255, 255), (255, 204, 255), (255, 153, 255), (255, 102, 255),
                           (255, 51, 255), (255, 0, 255), (255, 255, 204), (255, 204, 204),
                           (255, 153, 204), (255, 102, 204), (255, 51, 204), (255, 0, 204),
                           (255, 255, 153), (255, 204, 153), (255, 153, 153), (255, 102, 153),
                           (255, 51, 153), (255, 0, 153), (204, 255, 255), (204, 204, 255),
                           (204, 153, 255), (204, 102, 255), (204, 51, 255), (204, 0, 255),
                           (204, 255, 204), (204, 204, 204), (204, 153, 204), (204, 102, 204),
                           (204, 51, 204), (204, 0, 204), (204, 255, 153), (204, 204, 153),
                           (204, 153, 153), (204, 102, 153), (204, 51, 153), (204, 0, 153),
                           (153, 255, 255), (153, 204, 255), (153, 153, 255), (153, 102, 255),
                           (153, 51, 255), (153, 0, 255), (153, 255, 204), (153, 204, 204),
                           (153, 153, 204), (153, 102, 204), (153, 51, 204), (153, 0, 204),
                           (153, 255, 153), (153, 204, 153), (153, 153, 153), (153, 102, 153),
                           (153, 51, 153), (153, 0, 153), (102, 255, 255), (102, 204, 255),
                           (102, 153, 255), (102, 102, 255), (102, 51, 255), (102, 0, 255),
                           (102, 255, 204), (102, 204, 204), (102, 153, 204), (102, 102, 204),
                           (102, 51, 204), (102, 0, 204), (102, 255, 153), (102, 204, 153),
                           (102, 153, 153), (102, 102, 153), (102, 51, 153), (102, 0, 153),
                           (51, 255, 255), (51, 204, 255), (51, 153, 255), (51, 102, 255),
                           (51, 51, 255), (51, 0, 255), (51, 255, 204), (51, 204, 204),
                           (51, 153, 204), (51, 102, 204), (51, 51, 204), (51, 0, 204),
                           (51, 255, 153), (51, 204, 153), (51, 153, 153), (51, 102, 153),
                           (51, 51, 153), (51, 0, 153), (0, 255, 255), (0, 204, 255),
                           (0, 153, 255), (0, 102, 255), (0, 51, 255), (0, 0, 255),
                           (0, 255, 204), (0, 204, 204), (0, 153, 204), (0, 102, 204),
                           (0, 51, 204), (0, 0, 204), (0, 255, 153), (0, 204, 153),
                           (0, 153, 153), (0, 102, 153), (0, 51, 153), (0, 0, 153),
                           (255, 255, 102), (255, 204, 102), (255, 153, 102), (255, 102, 102),
                           (255, 51, 102), (255, 0, 102), (255, 255, 51), (255, 204, 51),
                           (255, 153, 51), (255, 102, 51), (255, 51, 51), (255, 0, 51),
                           (255, 255, 0), (255, 204, 0), (255, 153, 0), (255, 102, 0),
                           (255, 51, 0), (255, 0, 0), (204, 255, 102), (204, 204, 102),
                           (204, 153, 102), (204, 102, 102), (204, 51, 102), (204, 0, 102),
                           (204, 255, 51), (204, 204, 51), (204, 153, 51), (204, 102, 51),
                           (204, 51, 51), (204, 0, 51), (204, 255, 0), (204, 204, 0),
                           (204, 153, 0), (204, 102, 0), (204, 51, 0), (204, 0, 0),
                           (153, 255, 102), (153, 204, 102), (153, 153, 102), (153, 102, 102),
                           (153, 51, 102), (153, 0, 102), (153, 255, 51), (153, 204, 51),
                           (153, 153, 51), (153, 102, 51), (153, 51, 51), (153, 0, 51),
                           (153, 255, 0), (153, 204, 0), (153, 153, 0), (153, 102, 0),
                           (153, 51, 0), (153, 0, 0), (102, 255, 102), (102, 204, 102),
                           (102, 153, 102), (102, 102, 102), (102, 51, 102), (102, 0, 102),
                           (102, 255, 51), (102, 204, 51), (102, 153, 51), (102, 102, 51),
                           (102, 51, 51), (102, 0, 51), (102, 255, 0), (102, 204, 0),
                           (102, 153, 0), (102, 102, 0), (102, 51, 0), (102, 0, 0),
                           (51, 255, 102), (51, 204, 102), (51, 153, 102), (51, 102, 102),
                           (51, 51, 102), (51, 0, 102), (51, 255, 51), (51, 204, 51),
                           (51, 153, 51), (51, 102, 51), (51, 51, 51), (51, 0, 51),
                           (51, 255, 0), (51, 204, 0), (51, 153, 0), (51, 102, 0),
                           (51, 51, 0), (51, 0, 0), (0, 255, 102), (0, 204, 102),
                           (0, 153, 102), (0, 102, 102), (0, 51, 102), (0, 0, 102),
                           (0, 255, 51), (0, 204, 51), (0, 153, 51), (0, 102, 51),
                           (0, 51, 51), (0, 0, 51), (0, 255, 0), (0, 204, 0), (0, 153, 0),
                           (0, 102, 0), (0, 51, 0), (17, 17, 17), (34, 34, 34), (68, 68, 68),
                           (85, 85, 85), (119, 119, 119), (136, 136, 136), (170, 170, 170),
                           (187, 187, 187), (221, 221, 221), (238, 238, 238), (192, 192, 192),
                           (128, 0, 0), (128, 0, 128), (0, 128, 0), (0, 128, 128),
                           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                           (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                           (0, 0, 0))

def build_prototype_image():
    image = Image.new('L', (1, len(_Palm8BitColormapValues)))
    image.putdata(list(range(len(_Palm8BitColormapValues))))
    palettedata = ()
    for colormapValue in _Palm8BitColormapValues:
        palettedata += colormapValue
    else:
        palettedata += (0, 0, 0) * (256 - len(_Palm8BitColormapValues))
        image.putpalette(palettedata)
        return image


Palm8BitColormapImage = build_prototype_image()
_FLAGS = {'custom-colormap':16384, 
 'is-compressed':32768,  'has-transparent':8192}
_COMPRESSION_TYPES = {'none':255, 
 'rle':1,  'scanline':0}

def _save--- This code section failed: ---

 L. 116         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  LOAD_STR                 'P'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 121        10  LOAD_STR                 'P'
               12  STORE_FAST               'rawmode'

 L. 122        14  LOAD_CONST               8
               16  STORE_FAST               'bpp'

 L. 123        18  LOAD_CONST               1
               20  STORE_FAST               'version'
               22  JUMP_FORWARD        232  'to 232'
             24_0  COME_FROM             8  '8'

 L. 125        24  LOAD_FAST                'im'
               26  LOAD_ATTR                mode
               28  LOAD_STR                 'L'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE   190  'to 190'

 L. 126        34  LOAD_FAST                'im'
               36  LOAD_ATTR                encoderinfo
               38  LOAD_METHOD              get
               40  LOAD_STR                 'bpp'
               42  CALL_METHOD_1         1  ''
               44  LOAD_CONST               (1, 2, 4)
               46  <118>                 0  ''
               48  POP_JUMP_IF_FALSE    94  'to 94'

 L. 130        50  LOAD_FAST                'im'
               52  LOAD_ATTR                encoderinfo
               54  LOAD_STR                 'bpp'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'bpp'

 L. 131        60  LOAD_FAST                'im'
               62  LOAD_METHOD              point

 L. 132        64  LOAD_CONST               8
               66  LOAD_FAST                'bpp'
               68  BINARY_SUBTRACT  
               70  LOAD_CONST               1
               72  LOAD_FAST                'bpp'
               74  BINARY_LSHIFT    
               76  LOAD_CONST               1
               78  BINARY_SUBTRACT  
               80  BUILD_TUPLE_2         2 
               82  LOAD_LAMBDA              '<code_object <lambda>>'
               84  LOAD_STR                 '_save.<locals>.<lambda>'
               86  MAKE_FUNCTION_1          'default'

 L. 131        88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'im'
               92  JUMP_FORWARD        166  'to 166'
             94_0  COME_FROM            48  '48'

 L. 134        94  LOAD_FAST                'im'
               96  LOAD_ATTR                info
               98  LOAD_METHOD              get
              100  LOAD_STR                 'bpp'
              102  CALL_METHOD_1         1  ''
              104  LOAD_CONST               (1, 2, 4)
              106  <118>                 0  ''
              108  POP_JUMP_IF_FALSE   148  'to 148'

 L. 138       110  LOAD_FAST                'im'
              112  LOAD_ATTR                info
              114  LOAD_STR                 'bpp'
              116  BINARY_SUBSCR    
              118  STORE_FAST               'bpp'

 L. 139       120  LOAD_FAST                'im'
              122  LOAD_METHOD              point
              124  LOAD_CONST               1
              126  LOAD_FAST                'bpp'
              128  BINARY_LSHIFT    
              130  LOAD_CONST               1
              132  BINARY_SUBTRACT  
              134  BUILD_TUPLE_1         1 
              136  LOAD_LAMBDA              '<code_object <lambda>>'
              138  LOAD_STR                 '_save.<locals>.<lambda>'
              140  MAKE_FUNCTION_1          'default'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'im'
              146  JUMP_FORWARD        166  'to 166'
            148_0  COME_FROM           108  '108'

 L. 141       148  LOAD_GLOBAL              OSError
              150  LOAD_STR                 'cannot write mode '
              152  LOAD_FAST                'im'
              154  LOAD_ATTR                mode
              156  FORMAT_VALUE          0  ''
              158  LOAD_STR                 ' as Palm'
              160  BUILD_STRING_3        3 
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           146  '146'
            166_1  COME_FROM            92  '92'

 L. 144       166  LOAD_STR                 'P'
              168  LOAD_FAST                'im'
              170  STORE_ATTR               mode

 L. 145       172  LOAD_STR                 'P;'
              174  LOAD_GLOBAL              str
              176  LOAD_FAST                'bpp'
              178  CALL_FUNCTION_1       1  ''
              180  BINARY_ADD       
              182  STORE_FAST               'rawmode'

 L. 146       184  LOAD_CONST               1
              186  STORE_FAST               'version'
              188  JUMP_FORWARD        232  'to 232'
            190_0  COME_FROM            32  '32'

 L. 148       190  LOAD_FAST                'im'
              192  LOAD_ATTR                mode
              194  LOAD_STR                 '1'
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L. 151       200  LOAD_STR                 '1;I'
              202  STORE_FAST               'rawmode'

 L. 152       204  LOAD_CONST               1
              206  STORE_FAST               'bpp'

 L. 153       208  LOAD_CONST               0
              210  STORE_FAST               'version'
              212  JUMP_FORWARD        232  'to 232'
            214_0  COME_FROM           198  '198'

 L. 157       214  LOAD_GLOBAL              OSError
              216  LOAD_STR                 'cannot write mode '
              218  LOAD_FAST                'im'
              220  LOAD_ATTR                mode
              222  FORMAT_VALUE          0  ''
              224  LOAD_STR                 ' as Palm'
              226  BUILD_STRING_3        3 
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           212  '212'
            232_1  COME_FROM           188  '188'
            232_2  COME_FROM            22  '22'

 L. 161       232  LOAD_FAST                'im'
              234  LOAD_METHOD              load
              236  CALL_METHOD_0         0  ''
              238  POP_TOP          

 L. 165       240  LOAD_FAST                'im'
              242  LOAD_ATTR                size
              244  LOAD_CONST               0
              246  BINARY_SUBSCR    
              248  STORE_FAST               'cols'

 L. 166       250  LOAD_FAST                'im'
              252  LOAD_ATTR                size
              254  LOAD_CONST               1
              256  BINARY_SUBSCR    
              258  STORE_FAST               'rows'

 L. 168       260  LOAD_GLOBAL              int
              262  LOAD_FAST                'cols'
              264  LOAD_CONST               16
              266  LOAD_FAST                'bpp'
              268  BINARY_FLOOR_DIVIDE
              270  LOAD_CONST               1
              272  BINARY_SUBTRACT  
              274  BINARY_ADD       
              276  LOAD_CONST               16
              278  LOAD_FAST                'bpp'
              280  BINARY_FLOOR_DIVIDE
              282  BINARY_TRUE_DIVIDE
              284  CALL_FUNCTION_1       1  ''
              286  LOAD_CONST               2
              288  BINARY_MULTIPLY  
              290  STORE_FAST               'rowbytes'

 L. 169       292  LOAD_CONST               0
              294  STORE_FAST               'transparent_index'

 L. 170       296  LOAD_GLOBAL              _COMPRESSION_TYPES
              298  LOAD_STR                 'none'
              300  BINARY_SUBSCR    
              302  STORE_FAST               'compression_type'

 L. 172       304  LOAD_CONST               0
              306  STORE_FAST               'flags'

 L. 173       308  LOAD_FAST                'im'
              310  LOAD_ATTR                mode
              312  LOAD_STR                 'P'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   370  'to 370'
              320  LOAD_STR                 'custom-colormap'
              322  LOAD_FAST                'im'
              324  LOAD_ATTR                info
              326  <118>                 0  ''
          328_330  POP_JUMP_IF_FALSE   370  'to 370'

 L. 174       332  LOAD_FAST                'flags'
              334  LOAD_GLOBAL              _FLAGS
              336  LOAD_STR                 'custom-colormap'
              338  BINARY_SUBSCR    
              340  BINARY_AND       
              342  STORE_FAST               'flags'

 L. 175       344  LOAD_CONST               1026
              346  STORE_FAST               'colormapsize'

 L. 176       348  LOAD_FAST                'im'
              350  LOAD_ATTR                palette
              352  LOAD_ATTR                mode
              354  STORE_FAST               'colormapmode'

 L. 177       356  LOAD_FAST                'im'
              358  LOAD_METHOD              getdata
              360  CALL_METHOD_0         0  ''
              362  LOAD_METHOD              getpalette
              364  CALL_METHOD_0         0  ''
              366  STORE_FAST               'colormap'
              368  JUMP_FORWARD        374  'to 374'
            370_0  COME_FROM           328  '328'
            370_1  COME_FROM           316  '316'

 L. 179       370  LOAD_CONST               0
              372  STORE_FAST               'colormapsize'
            374_0  COME_FROM           368  '368'

 L. 181       374  LOAD_STR                 'offset'
              376  LOAD_FAST                'im'
              378  LOAD_ATTR                info
              380  <118>                 0  ''
          382_384  POP_JUMP_IF_FALSE   412  'to 412'

 L. 182       386  LOAD_FAST                'rowbytes'
              388  LOAD_FAST                'rows'
              390  BINARY_MULTIPLY  
              392  LOAD_CONST               16
              394  BINARY_ADD       
              396  LOAD_CONST               3
              398  BINARY_ADD       
              400  LOAD_FAST                'colormapsize'
              402  BINARY_ADD       
              404  LOAD_CONST               4
              406  BINARY_FLOOR_DIVIDE
              408  STORE_FAST               'offset'
              410  JUMP_FORWARD        416  'to 416'
            412_0  COME_FROM           382  '382'

 L. 184       412  LOAD_CONST               0
              414  STORE_FAST               'offset'
            416_0  COME_FROM           410  '410'

 L. 186       416  LOAD_FAST                'fp'
              418  LOAD_METHOD              write
              420  LOAD_GLOBAL              o16b
              422  LOAD_FAST                'cols'
              424  CALL_FUNCTION_1       1  ''
              426  LOAD_GLOBAL              o16b
              428  LOAD_FAST                'rows'
              430  CALL_FUNCTION_1       1  ''
              432  BINARY_ADD       
              434  LOAD_GLOBAL              o16b
              436  LOAD_FAST                'rowbytes'
              438  CALL_FUNCTION_1       1  ''
              440  BINARY_ADD       
              442  LOAD_GLOBAL              o16b
              444  LOAD_FAST                'flags'
              446  CALL_FUNCTION_1       1  ''
              448  BINARY_ADD       
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          

 L. 187       454  LOAD_FAST                'fp'
              456  LOAD_METHOD              write
              458  LOAD_GLOBAL              o8
              460  LOAD_FAST                'bpp'
              462  CALL_FUNCTION_1       1  ''
              464  CALL_METHOD_1         1  ''
              466  POP_TOP          

 L. 188       468  LOAD_FAST                'fp'
              470  LOAD_METHOD              write
              472  LOAD_GLOBAL              o8
              474  LOAD_FAST                'version'
              476  CALL_FUNCTION_1       1  ''
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          

 L. 189       482  LOAD_FAST                'fp'
              484  LOAD_METHOD              write
              486  LOAD_GLOBAL              o16b
              488  LOAD_FAST                'offset'
              490  CALL_FUNCTION_1       1  ''
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          

 L. 190       496  LOAD_FAST                'fp'
              498  LOAD_METHOD              write
              500  LOAD_GLOBAL              o8
              502  LOAD_FAST                'transparent_index'
              504  CALL_FUNCTION_1       1  ''
              506  CALL_METHOD_1         1  ''
              508  POP_TOP          

 L. 191       510  LOAD_FAST                'fp'
              512  LOAD_METHOD              write
              514  LOAD_GLOBAL              o8
              516  LOAD_FAST                'compression_type'
              518  CALL_FUNCTION_1       1  ''
              520  CALL_METHOD_1         1  ''
              522  POP_TOP          

 L. 192       524  LOAD_FAST                'fp'
              526  LOAD_METHOD              write
              528  LOAD_GLOBAL              o16b
              530  LOAD_CONST               0
              532  CALL_FUNCTION_1       1  ''
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          

 L. 196       538  LOAD_FAST                'colormapsize'
              540  LOAD_CONST               0
              542  COMPARE_OP               >
          544_546  POP_JUMP_IF_FALSE   738  'to 738'

 L. 197       548  LOAD_FAST                'fp'
              550  LOAD_METHOD              write
              552  LOAD_GLOBAL              o16b
              554  LOAD_CONST               256
              556  CALL_FUNCTION_1       1  ''
              558  CALL_METHOD_1         1  ''
              560  POP_TOP          

 L. 198       562  LOAD_GLOBAL              range
              564  LOAD_CONST               256
              566  CALL_FUNCTION_1       1  ''
              568  GET_ITER         
            570_0  COME_FROM           668  '668'
              570  FOR_ITER            738  'to 738'
              572  STORE_FAST               'i'

 L. 199       574  LOAD_FAST                'fp'
              576  LOAD_METHOD              write
              578  LOAD_GLOBAL              o8
              580  LOAD_FAST                'i'
              582  CALL_FUNCTION_1       1  ''
              584  CALL_METHOD_1         1  ''
              586  POP_TOP          

 L. 200       588  LOAD_FAST                'colormapmode'
              590  LOAD_STR                 'RGB'
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   662  'to 662'

 L. 201       598  LOAD_FAST                'fp'
              600  LOAD_METHOD              write

 L. 202       602  LOAD_GLOBAL              o8
              604  LOAD_FAST                'colormap'
              606  LOAD_CONST               3
              608  LOAD_FAST                'i'
              610  BINARY_MULTIPLY  
              612  BINARY_SUBSCR    
              614  CALL_FUNCTION_1       1  ''

 L. 203       616  LOAD_GLOBAL              o8
              618  LOAD_FAST                'colormap'
              620  LOAD_CONST               3
              622  LOAD_FAST                'i'
              624  BINARY_MULTIPLY  
              626  LOAD_CONST               1
              628  BINARY_ADD       
              630  BINARY_SUBSCR    
              632  CALL_FUNCTION_1       1  ''

 L. 202       634  BINARY_ADD       

 L. 204       636  LOAD_GLOBAL              o8
              638  LOAD_FAST                'colormap'
              640  LOAD_CONST               3
              642  LOAD_FAST                'i'
              644  BINARY_MULTIPLY  
              646  LOAD_CONST               2
              648  BINARY_ADD       
              650  BINARY_SUBSCR    
              652  CALL_FUNCTION_1       1  ''

 L. 202       654  BINARY_ADD       

 L. 201       656  CALL_METHOD_1         1  ''
              658  POP_TOP          
              660  JUMP_BACK           570  'to 570'
            662_0  COME_FROM           594  '594'

 L. 206       662  LOAD_FAST                'colormapmode'
              664  LOAD_STR                 'RGBA'
              666  COMPARE_OP               ==
          668_670  POP_JUMP_IF_FALSE   570  'to 570'

 L. 207       672  LOAD_FAST                'fp'
              674  LOAD_METHOD              write

 L. 208       676  LOAD_GLOBAL              o8
              678  LOAD_FAST                'colormap'
              680  LOAD_CONST               4
              682  LOAD_FAST                'i'
              684  BINARY_MULTIPLY  
              686  BINARY_SUBSCR    
              688  CALL_FUNCTION_1       1  ''

 L. 209       690  LOAD_GLOBAL              o8
              692  LOAD_FAST                'colormap'
              694  LOAD_CONST               4
              696  LOAD_FAST                'i'
              698  BINARY_MULTIPLY  
              700  LOAD_CONST               1
              702  BINARY_ADD       
              704  BINARY_SUBSCR    
              706  CALL_FUNCTION_1       1  ''

 L. 208       708  BINARY_ADD       

 L. 210       710  LOAD_GLOBAL              o8
              712  LOAD_FAST                'colormap'
              714  LOAD_CONST               4
              716  LOAD_FAST                'i'
              718  BINARY_MULTIPLY  
              720  LOAD_CONST               2
              722  BINARY_ADD       
              724  BINARY_SUBSCR    
              726  CALL_FUNCTION_1       1  ''

 L. 208       728  BINARY_ADD       

 L. 207       730  CALL_METHOD_1         1  ''
              732  POP_TOP          
          734_736  JUMP_BACK           570  'to 570'
            738_0  COME_FROM           544  '544'

 L. 214       738  LOAD_GLOBAL              ImageFile
              740  LOAD_METHOD              _save
              742  LOAD_FAST                'im'
              744  LOAD_FAST                'fp'
              746  LOAD_STR                 'raw'
              748  LOAD_CONST               (0, 0)
              750  LOAD_FAST                'im'
              752  LOAD_ATTR                size
              754  BINARY_ADD       
              756  LOAD_CONST               0
              758  LOAD_FAST                'rawmode'
              760  LOAD_FAST                'rowbytes'
              762  LOAD_CONST               1
              764  BUILD_TUPLE_3         3 
              766  BUILD_TUPLE_4         4 
              768  BUILD_LIST_1          1 
              770  CALL_METHOD_3         3  ''
              772  POP_TOP          

 L. 216       774  LOAD_GLOBAL              hasattr
              776  LOAD_FAST                'fp'
              778  LOAD_STR                 'flush'
              780  CALL_FUNCTION_2       2  ''
          782_784  POP_JUMP_IF_FALSE   794  'to 794'

 L. 217       786  LOAD_FAST                'fp'
              788  LOAD_METHOD              flush
              790  CALL_METHOD_0         0  ''
              792  POP_TOP          
            794_0  COME_FROM           782  '782'

Parse error at or near `<118>' instruction at offset 46


Image.register_save('Palm', _save)
Image.register_extension('Palm', '.palm')
Image.register_mime('Palm', 'image/palm')