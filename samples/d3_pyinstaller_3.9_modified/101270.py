# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\BmpImagePlugin.py
from . import Image, ImageFile, ImagePalette
from ._binary import i16le as i16
from ._binary import i32le as i32
from ._binary import o8
from ._binary import o16le as o16
from ._binary import o32le as o32
BIT2MODE = {1:('P', 'P;1'), 
 4:('P', 'P;4'), 
 8:('P', 'P'), 
 16:('RGB', 'BGR;15'), 
 24:('RGB', 'BGR'), 
 32:('RGB', 'BGRX')}

def _accept(prefix):
    return prefix[:2] == b'BM'


def _dib_accept--- This code section failed: ---

 L.  54         0  LOAD_GLOBAL              i32
                2  LOAD_FAST                'prefix'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               (12, 40, 64, 108, 124)
                8  <118>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class BmpImageFile(ImageFile.ImageFile):
    __doc__ = ' Image plugin for the Windows Bitmap format (BMP) '
    format_description = 'Windows Bitmap'
    format = 'BMP'
    COMPRESSIONS = {'RAW':0, 
     'RLE8':1,  'RLE4':2,  'BITFIELDS':3,  'JPEG':4,  'PNG':5}
    for k, v in COMPRESSIONS.items():
        vars()[k] = v
    else:

        def _bitmap--- This code section failed: ---

 L.  74         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_ATTR                read
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fp
               10  LOAD_ATTR                seek
               12  ROT_TWO          
               14  STORE_FAST               'read'
               16  STORE_FAST               'seek'

 L.  75        18  LOAD_FAST                'header'
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.  76        22  LOAD_FAST                'seek'
               24  LOAD_FAST                'header'
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          
             30_0  COME_FROM            20  '20'

 L.  77        30  BUILD_MAP_0           0 
               32  STORE_FAST               'file_info'

 L.  79        34  LOAD_GLOBAL              i32
               36  LOAD_FAST                'read'
               38  LOAD_CONST               4
               40  CALL_FUNCTION_1       1  ''
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'file_info'
               46  LOAD_STR                 'header_size'
               48  STORE_SUBSCR     

 L.  80        50  LOAD_CONST               -1
               52  LOAD_FAST                'file_info'
               54  LOAD_STR                 'direction'
               56  STORE_SUBSCR     

 L.  84        58  LOAD_GLOBAL              ImageFile
               60  LOAD_METHOD              _safe_read
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                fp
               66  LOAD_FAST                'file_info'
               68  LOAD_STR                 'header_size'
               70  BINARY_SUBSCR    
               72  LOAD_CONST               4
               74  BINARY_SUBTRACT  
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'header_data'

 L.  88        80  LOAD_FAST                'file_info'
               82  LOAD_STR                 'header_size'
               84  BINARY_SUBSCR    
               86  LOAD_CONST               12
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   170  'to 170'

 L.  89        92  LOAD_GLOBAL              i16
               94  LOAD_FAST                'header_data'
               96  LOAD_CONST               0
               98  CALL_FUNCTION_2       2  ''
              100  LOAD_FAST                'file_info'
              102  LOAD_STR                 'width'
              104  STORE_SUBSCR     

 L.  90       106  LOAD_GLOBAL              i16
              108  LOAD_FAST                'header_data'
              110  LOAD_CONST               2
              112  CALL_FUNCTION_2       2  ''
              114  LOAD_FAST                'file_info'
              116  LOAD_STR                 'height'
              118  STORE_SUBSCR     

 L.  91       120  LOAD_GLOBAL              i16
              122  LOAD_FAST                'header_data'
              124  LOAD_CONST               4
              126  CALL_FUNCTION_2       2  ''
              128  LOAD_FAST                'file_info'
              130  LOAD_STR                 'planes'
              132  STORE_SUBSCR     

 L.  92       134  LOAD_GLOBAL              i16
              136  LOAD_FAST                'header_data'
              138  LOAD_CONST               6
              140  CALL_FUNCTION_2       2  ''
              142  LOAD_FAST                'file_info'
              144  LOAD_STR                 'bits'
              146  STORE_SUBSCR     

 L.  93       148  LOAD_FAST                'self'
              150  LOAD_ATTR                RAW
              152  LOAD_FAST                'file_info'
              154  LOAD_STR                 'compression'
              156  STORE_SUBSCR     

 L.  94       158  LOAD_CONST               3
              160  LOAD_FAST                'file_info'
              162  LOAD_STR                 'palette_padding'
              164  STORE_SUBSCR     
          166_168  JUMP_FORWARD        594  'to 594'
            170_0  COME_FROM            90  '90'

 L.  98       170  LOAD_FAST                'file_info'
              172  LOAD_STR                 'header_size'
              174  BINARY_SUBSCR    
              176  LOAD_CONST               (40, 64, 108, 124)
              178  <118>                 0  ''
          180_182  POP_JUMP_IF_FALSE   574  'to 574'

 L.  99       184  LOAD_FAST                'header_data'
              186  LOAD_CONST               7
              188  BINARY_SUBSCR    
              190  LOAD_CONST               255
              192  COMPARE_OP               ==
              194  LOAD_FAST                'file_info'
              196  LOAD_STR                 'y_flip'
              198  STORE_SUBSCR     

 L. 100       200  LOAD_FAST                'file_info'
              202  LOAD_STR                 'y_flip'
              204  BINARY_SUBSCR    
              206  POP_JUMP_IF_FALSE   212  'to 212'
              208  LOAD_CONST               1
              210  JUMP_FORWARD        214  'to 214'
            212_0  COME_FROM           206  '206'
              212  LOAD_CONST               -1
            214_0  COME_FROM           210  '210'
              214  LOAD_FAST                'file_info'
              216  LOAD_STR                 'direction'
              218  STORE_SUBSCR     

 L. 101       220  LOAD_GLOBAL              i32
              222  LOAD_FAST                'header_data'
              224  LOAD_CONST               0
              226  CALL_FUNCTION_2       2  ''
              228  LOAD_FAST                'file_info'
              230  LOAD_STR                 'width'
              232  STORE_SUBSCR     

 L. 104       234  LOAD_FAST                'file_info'
              236  LOAD_STR                 'y_flip'
              238  BINARY_SUBSCR    

 L. 103       240  POP_JUMP_IF_TRUE    252  'to 252'
              242  LOAD_GLOBAL              i32
              244  LOAD_FAST                'header_data'
              246  LOAD_CONST               4
              248  CALL_FUNCTION_2       2  ''
              250  JUMP_FORWARD        264  'to 264'
            252_0  COME_FROM           240  '240'

 L. 105       252  LOAD_CONST               4294967296
              254  LOAD_GLOBAL              i32
              256  LOAD_FAST                'header_data'
              258  LOAD_CONST               4
              260  CALL_FUNCTION_2       2  ''
              262  BINARY_SUBTRACT  
            264_0  COME_FROM           250  '250'

 L. 102       264  LOAD_FAST                'file_info'
              266  LOAD_STR                 'height'
              268  STORE_SUBSCR     

 L. 107       270  LOAD_GLOBAL              i16
              272  LOAD_FAST                'header_data'
              274  LOAD_CONST               8
              276  CALL_FUNCTION_2       2  ''
              278  LOAD_FAST                'file_info'
              280  LOAD_STR                 'planes'
              282  STORE_SUBSCR     

 L. 108       284  LOAD_GLOBAL              i16
              286  LOAD_FAST                'header_data'
              288  LOAD_CONST               10
              290  CALL_FUNCTION_2       2  ''
              292  LOAD_FAST                'file_info'
              294  LOAD_STR                 'bits'
              296  STORE_SUBSCR     

 L. 109       298  LOAD_GLOBAL              i32
              300  LOAD_FAST                'header_data'
              302  LOAD_CONST               12
              304  CALL_FUNCTION_2       2  ''
              306  LOAD_FAST                'file_info'
              308  LOAD_STR                 'compression'
              310  STORE_SUBSCR     

 L. 111       312  LOAD_GLOBAL              i32
              314  LOAD_FAST                'header_data'
              316  LOAD_CONST               16
              318  CALL_FUNCTION_2       2  ''
              320  LOAD_FAST                'file_info'
              322  LOAD_STR                 'data_size'
              324  STORE_SUBSCR     

 L. 113       326  LOAD_GLOBAL              i32
              328  LOAD_FAST                'header_data'
              330  LOAD_CONST               20
              332  CALL_FUNCTION_2       2  ''

 L. 114       334  LOAD_GLOBAL              i32
              336  LOAD_FAST                'header_data'
              338  LOAD_CONST               24
              340  CALL_FUNCTION_2       2  ''

 L. 112       342  BUILD_TUPLE_2         2 
              344  LOAD_FAST                'file_info'
              346  LOAD_STR                 'pixels_per_meter'
              348  STORE_SUBSCR     

 L. 116       350  LOAD_GLOBAL              i32
              352  LOAD_FAST                'header_data'
              354  LOAD_CONST               28
              356  CALL_FUNCTION_2       2  ''
              358  LOAD_FAST                'file_info'
              360  LOAD_STR                 'colors'
              362  STORE_SUBSCR     

 L. 117       364  LOAD_CONST               4
              366  LOAD_FAST                'file_info'
              368  LOAD_STR                 'palette_padding'
              370  STORE_SUBSCR     

 L. 118       372  LOAD_GLOBAL              tuple
              374  LOAD_GENEXPR             '<code_object <genexpr>>'
              376  LOAD_STR                 'BmpImageFile._bitmap.<locals>.<genexpr>'
              378  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 119       380  LOAD_FAST                'file_info'
              382  LOAD_STR                 'pixels_per_meter'
              384  BINARY_SUBSCR    

 L. 118       386  GET_ITER         
              388  CALL_FUNCTION_1       1  ''
              390  CALL_FUNCTION_1       1  ''
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                info
              396  LOAD_STR                 'dpi'
              398  STORE_SUBSCR     

 L. 121       400  LOAD_FAST                'file_info'
              402  LOAD_STR                 'compression'
              404  BINARY_SUBSCR    
              406  LOAD_FAST                'self'
              408  LOAD_ATTR                BITFIELDS
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   594  'to 594'

 L. 122       416  LOAD_GLOBAL              len
              418  LOAD_FAST                'header_data'
              420  CALL_FUNCTION_1       1  ''
              422  LOAD_CONST               52
              424  COMPARE_OP               >=
          426_428  POP_JUMP_IF_FALSE   478  'to 478'

 L. 123       430  LOAD_GLOBAL              enumerate

 L. 124       432  BUILD_LIST_0          0 
              434  LOAD_CONST               ('r_mask', 'g_mask', 'b_mask', 'a_mask')
              436  CALL_FINALLY        439  'to 439'

 L. 123       438  CALL_FUNCTION_1       1  ''
              440  GET_ITER         
            442_0  COME_FROM           472  '472'
              442  FOR_ITER            476  'to 476'
              444  UNPACK_SEQUENCE_2     2 
              446  STORE_FAST               'idx'
              448  STORE_FAST               'mask'

 L. 126       450  LOAD_GLOBAL              i32
              452  LOAD_FAST                'header_data'
              454  LOAD_CONST               36
              456  LOAD_FAST                'idx'
              458  LOAD_CONST               4
              460  BINARY_MULTIPLY  
              462  BINARY_ADD       
              464  CALL_FUNCTION_2       2  ''
              466  LOAD_FAST                'file_info'
              468  LOAD_FAST                'mask'
              470  STORE_SUBSCR     
          472_474  JUMP_BACK           442  'to 442'
            476_0  COME_FROM           442  '442'
              476  JUMP_FORWARD        514  'to 514'
            478_0  COME_FROM           426  '426'

 L. 136       478  LOAD_CONST               0
              480  LOAD_FAST                'file_info'
              482  LOAD_STR                 'a_mask'
              484  STORE_SUBSCR     

 L. 137       486  LOAD_CONST               ('r_mask', 'g_mask', 'b_mask')
              488  GET_ITER         
            490_0  COME_FROM           510  '510'
              490  FOR_ITER            514  'to 514'
              492  STORE_FAST               'mask'

 L. 138       494  LOAD_GLOBAL              i32
              496  LOAD_FAST                'read'
              498  LOAD_CONST               4
              500  CALL_FUNCTION_1       1  ''
              502  CALL_FUNCTION_1       1  ''
              504  LOAD_FAST                'file_info'
              506  LOAD_FAST                'mask'
              508  STORE_SUBSCR     
          510_512  JUMP_BACK           490  'to 490'
            514_0  COME_FROM           490  '490'
            514_1  COME_FROM           476  '476'

 L. 140       514  LOAD_FAST                'file_info'
              516  LOAD_STR                 'r_mask'
              518  BINARY_SUBSCR    

 L. 141       520  LOAD_FAST                'file_info'
              522  LOAD_STR                 'g_mask'
              524  BINARY_SUBSCR    

 L. 142       526  LOAD_FAST                'file_info'
              528  LOAD_STR                 'b_mask'
              530  BINARY_SUBSCR    

 L. 139       532  BUILD_TUPLE_3         3 
              534  LOAD_FAST                'file_info'
              536  LOAD_STR                 'rgb_mask'
              538  STORE_SUBSCR     

 L. 145       540  LOAD_FAST                'file_info'
              542  LOAD_STR                 'r_mask'
              544  BINARY_SUBSCR    

 L. 146       546  LOAD_FAST                'file_info'
              548  LOAD_STR                 'g_mask'
              550  BINARY_SUBSCR    

 L. 147       552  LOAD_FAST                'file_info'
              554  LOAD_STR                 'b_mask'
              556  BINARY_SUBSCR    

 L. 148       558  LOAD_FAST                'file_info'
              560  LOAD_STR                 'a_mask'
              562  BINARY_SUBSCR    

 L. 144       564  BUILD_TUPLE_4         4 
              566  LOAD_FAST                'file_info'
              568  LOAD_STR                 'rgba_mask'
              570  STORE_SUBSCR     
              572  JUMP_FORWARD        594  'to 594'
            574_0  COME_FROM           180  '180'

 L. 151       574  LOAD_GLOBAL              OSError
              576  LOAD_STR                 'Unsupported BMP header type ('
              578  LOAD_FAST                'file_info'
              580  LOAD_STR                 'header_size'
              582  BINARY_SUBSCR    
              584  FORMAT_VALUE          0  ''
              586  LOAD_STR                 ')'
              588  BUILD_STRING_3        3 
              590  CALL_FUNCTION_1       1  ''
              592  RAISE_VARARGS_1       1  'exception instance'
            594_0  COME_FROM           572  '572'
            594_1  COME_FROM           412  '412'
            594_2  COME_FROM           166  '166'

 L. 155       594  LOAD_FAST                'file_info'
              596  LOAD_STR                 'width'
              598  BINARY_SUBSCR    
              600  LOAD_FAST                'file_info'
              602  LOAD_STR                 'height'
              604  BINARY_SUBSCR    
              606  BUILD_TUPLE_2         2 
              608  LOAD_FAST                'self'
              610  STORE_ATTR               _size

 L. 160       612  LOAD_FAST                'file_info'
              614  LOAD_METHOD              get
              616  LOAD_STR                 'colors'
              618  LOAD_CONST               0
              620  CALL_METHOD_2         2  ''

 L. 159   622_624  POP_JUMP_IF_FALSE   634  'to 634'
              626  LOAD_FAST                'file_info'
              628  LOAD_STR                 'colors'
              630  BINARY_SUBSCR    
              632  JUMP_FORWARD        644  'to 644'
            634_0  COME_FROM           622  '622'

 L. 161       634  LOAD_CONST               1
              636  LOAD_FAST                'file_info'
              638  LOAD_STR                 'bits'
              640  BINARY_SUBSCR    
              642  BINARY_LSHIFT    
            644_0  COME_FROM           632  '632'

 L. 158       644  LOAD_FAST                'file_info'
              646  LOAD_STR                 'colors'
              648  STORE_SUBSCR     

 L. 165       650  LOAD_GLOBAL              BIT2MODE
              652  LOAD_METHOD              get
              654  LOAD_FAST                'file_info'
              656  LOAD_STR                 'bits'
              658  BINARY_SUBSCR    
              660  LOAD_CONST               (None, None)
              662  CALL_METHOD_2         2  ''
              664  UNPACK_SEQUENCE_2     2 
              666  LOAD_FAST                'self'
              668  STORE_ATTR               mode
              670  STORE_FAST               'raw_mode'

 L. 166       672  LOAD_FAST                'self'
              674  LOAD_ATTR                mode
              676  LOAD_CONST               None
              678  <117>                 0  ''
          680_682  POP_JUMP_IF_FALSE   704  'to 704'

 L. 167       684  LOAD_GLOBAL              OSError
              686  LOAD_STR                 'Unsupported BMP pixel depth ('
              688  LOAD_FAST                'file_info'
              690  LOAD_STR                 'bits'
              692  BINARY_SUBSCR    
              694  FORMAT_VALUE          0  ''
              696  LOAD_STR                 ')'
              698  BUILD_STRING_3        3 
              700  CALL_FUNCTION_1       1  ''
              702  RAISE_VARARGS_1       1  'exception instance'
            704_0  COME_FROM           680  '680'

 L. 170       704  LOAD_FAST                'file_info'
              706  LOAD_STR                 'compression'
              708  BINARY_SUBSCR    
              710  LOAD_FAST                'self'
              712  LOAD_ATTR                BITFIELDS
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   936  'to 936'

 L. 172       720  BUILD_LIST_0          0 
              722  LOAD_CONST               ((16711680, 65280, 255, 0), (16711680, 65280, 255, 4278190080), (255, 65280, 16711680, 4278190080), (0, 0, 0, 0), (4278190080, 16711680, 65280, 0))
              724  CALL_FINALLY        727  'to 727'

 L. 179       726  LOAD_CONST               (16711680, 65280, 255)
              728  BUILD_LIST_1          1 

 L. 180       730  LOAD_CONST               (63488, 2016, 31)
              732  LOAD_CONST               (31744, 992, 31)
              734  BUILD_LIST_2          2 

 L. 171       736  LOAD_CONST               (32, 24, 16)
              738  BUILD_CONST_KEY_MAP_3     3 
              740  STORE_FAST               'SUPPORTED'

 L. 183       742  LOAD_STR                 'BGRX'

 L. 184       744  LOAD_STR                 'XBGR'

 L. 185       746  LOAD_STR                 'RGBA'

 L. 186       748  LOAD_STR                 'BGRA'

 L. 187       750  LOAD_STR                 'BGRA'

 L. 188       752  LOAD_STR                 'BGR'

 L. 189       754  LOAD_STR                 'BGR;16'

 L. 190       756  LOAD_STR                 'BGR;15'

 L. 182       758  LOAD_CONST               ((32, (16711680, 65280, 255, 0)), (32, (4278190080, 16711680, 65280, 0)), (32, (255, 65280, 16711680, 4278190080)), (32, (16711680, 65280, 255, 4278190080)), (32, (0, 0, 0, 0)), (24, (16711680, 65280, 255)), (16, (63488, 2016, 31)), (16, (31744, 992, 31)))
              760  BUILD_CONST_KEY_MAP_8     8 
              762  STORE_FAST               'MASK_MODES'

 L. 192       764  LOAD_FAST                'file_info'
              766  LOAD_STR                 'bits'
              768  BINARY_SUBSCR    
              770  LOAD_FAST                'SUPPORTED'
              772  <118>                 0  ''
          774_776  POP_JUMP_IF_FALSE   926  'to 926'

 L. 194       778  LOAD_FAST                'file_info'
              780  LOAD_STR                 'bits'
              782  BINARY_SUBSCR    
              784  LOAD_CONST               32
              786  COMPARE_OP               ==

 L. 193   788_790  POP_JUMP_IF_FALSE   858  'to 858'

 L. 195       792  LOAD_FAST                'file_info'
              794  LOAD_STR                 'rgba_mask'
              796  BINARY_SUBSCR    
              798  LOAD_FAST                'SUPPORTED'
              800  LOAD_FAST                'file_info'
              802  LOAD_STR                 'bits'
              804  BINARY_SUBSCR    
              806  BINARY_SUBSCR    
              808  <118>                 0  ''

 L. 193   810_812  POP_JUMP_IF_FALSE   858  'to 858'

 L. 197       814  LOAD_FAST                'MASK_MODES'
              816  LOAD_FAST                'file_info'
              818  LOAD_STR                 'bits'
              820  BINARY_SUBSCR    
              822  LOAD_FAST                'file_info'
              824  LOAD_STR                 'rgba_mask'
              826  BINARY_SUBSCR    
              828  BUILD_TUPLE_2         2 
              830  BINARY_SUBSCR    
              832  STORE_FAST               'raw_mode'

 L. 198       834  LOAD_STR                 'A'
              836  LOAD_FAST                'raw_mode'
              838  <118>                 0  ''
          840_842  POP_JUMP_IF_FALSE   848  'to 848'
              844  LOAD_STR                 'RGBA'
              846  JUMP_FORWARD        852  'to 852'
            848_0  COME_FROM           840  '840'
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                mode
            852_0  COME_FROM           846  '846'
              852  LOAD_FAST                'self'
              854  STORE_ATTR               mode
              856  JUMP_FORWARD        924  'to 924'
            858_0  COME_FROM           810  '810'
            858_1  COME_FROM           788  '788'

 L. 200       858  LOAD_FAST                'file_info'
              860  LOAD_STR                 'bits'
              862  BINARY_SUBSCR    
              864  LOAD_CONST               (24, 16)
              866  <118>                 0  ''

 L. 199   868_870  POP_JUMP_IF_FALSE   916  'to 916'

 L. 201       872  LOAD_FAST                'file_info'
              874  LOAD_STR                 'rgb_mask'
              876  BINARY_SUBSCR    
              878  LOAD_FAST                'SUPPORTED'
              880  LOAD_FAST                'file_info'
              882  LOAD_STR                 'bits'
              884  BINARY_SUBSCR    
              886  BINARY_SUBSCR    
              888  <118>                 0  ''

 L. 199   890_892  POP_JUMP_IF_FALSE   916  'to 916'

 L. 203       894  LOAD_FAST                'MASK_MODES'
              896  LOAD_FAST                'file_info'
              898  LOAD_STR                 'bits'
              900  BINARY_SUBSCR    
              902  LOAD_FAST                'file_info'
              904  LOAD_STR                 'rgb_mask'
              906  BINARY_SUBSCR    
              908  BUILD_TUPLE_2         2 
              910  BINARY_SUBSCR    
              912  STORE_FAST               'raw_mode'
              914  JUMP_FORWARD        924  'to 924'
            916_0  COME_FROM           890  '890'
            916_1  COME_FROM           868  '868'

 L. 205       916  LOAD_GLOBAL              OSError
              918  LOAD_STR                 'Unsupported BMP bitfields layout'
              920  CALL_FUNCTION_1       1  ''
              922  RAISE_VARARGS_1       1  'exception instance'
            924_0  COME_FROM           914  '914'
            924_1  COME_FROM           856  '856'
              924  JUMP_FORWARD        934  'to 934'
            926_0  COME_FROM           774  '774'

 L. 207       926  LOAD_GLOBAL              OSError
              928  LOAD_STR                 'Unsupported BMP bitfields layout'
              930  CALL_FUNCTION_1       1  ''
              932  RAISE_VARARGS_1       1  'exception instance'
            934_0  COME_FROM           924  '924'
              934  JUMP_FORWARD       1008  'to 1008'
            936_0  COME_FROM           716  '716'

 L. 208       936  LOAD_FAST                'file_info'
              938  LOAD_STR                 'compression'
              940  BINARY_SUBSCR    
              942  LOAD_FAST                'self'
              944  LOAD_ATTR                RAW
              946  COMPARE_OP               ==
          948_950  POP_JUMP_IF_FALSE   988  'to 988'

 L. 209       952  LOAD_FAST                'file_info'
              954  LOAD_STR                 'bits'
              956  BINARY_SUBSCR    
              958  LOAD_CONST               32
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE  1008  'to 1008'
              966  LOAD_FAST                'header'
              968  LOAD_CONST               22
              970  COMPARE_OP               ==
          972_974  POP_JUMP_IF_FALSE  1008  'to 1008'

 L. 210       976  LOAD_CONST               ('BGRA', 'RGBA')
              978  UNPACK_SEQUENCE_2     2 
              980  STORE_FAST               'raw_mode'
              982  LOAD_FAST                'self'
              984  STORE_ATTR               mode
              986  JUMP_FORWARD       1008  'to 1008'
            988_0  COME_FROM           948  '948'

 L. 212       988  LOAD_GLOBAL              OSError
              990  LOAD_STR                 'Unsupported BMP compression ('
              992  LOAD_FAST                'file_info'
              994  LOAD_STR                 'compression'
              996  BINARY_SUBSCR    
              998  FORMAT_VALUE          0  ''
             1000  LOAD_STR                 ')'
             1002  BUILD_STRING_3        3 
             1004  CALL_FUNCTION_1       1  ''
             1006  RAISE_VARARGS_1       1  'exception instance'
           1008_0  COME_FROM           986  '986'
           1008_1  COME_FROM           972  '972'
           1008_2  COME_FROM           962  '962'
           1008_3  COME_FROM           934  '934'

 L. 215      1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                mode
             1012  LOAD_STR                 'P'
             1014  COMPARE_OP               ==
         1016_1018  POP_JUMP_IF_FALSE  1272  'to 1272'

 L. 218      1020  LOAD_CONST               0
             1022  LOAD_FAST                'file_info'
             1024  LOAD_STR                 'colors'
             1026  BINARY_SUBSCR    
             1028  DUP_TOP          
             1030  ROT_THREE        
             1032  COMPARE_OP               <
         1034_1036  POP_JUMP_IF_FALSE  1048  'to 1048'
             1038  LOAD_CONST               65536
             1040  COMPARE_OP               <=
         1042_1044  POP_JUMP_IF_TRUE   1072  'to 1072'
             1046  JUMP_FORWARD       1050  'to 1050'
           1048_0  COME_FROM          1034  '1034'
             1048  POP_TOP          
           1050_0  COME_FROM          1046  '1046'

 L. 219      1050  LOAD_GLOBAL              OSError
             1052  LOAD_STR                 'Unsupported BMP Palette size ('
             1054  LOAD_FAST                'file_info'
             1056  LOAD_STR                 'colors'
             1058  BINARY_SUBSCR    
             1060  FORMAT_VALUE          0  ''
             1062  LOAD_STR                 ')'
             1064  BUILD_STRING_3        3 
             1066  CALL_FUNCTION_1       1  ''
             1068  RAISE_VARARGS_1       1  'exception instance'
             1070  JUMP_FORWARD       1272  'to 1272'
           1072_0  COME_FROM          1042  '1042'

 L. 221      1072  LOAD_FAST                'file_info'
             1074  LOAD_STR                 'palette_padding'
             1076  BINARY_SUBSCR    
             1078  STORE_FAST               'padding'

 L. 222      1080  LOAD_FAST                'read'
             1082  LOAD_FAST                'padding'
             1084  LOAD_FAST                'file_info'
             1086  LOAD_STR                 'colors'
             1088  BINARY_SUBSCR    
             1090  BINARY_MULTIPLY  
             1092  CALL_FUNCTION_1       1  ''
             1094  STORE_FAST               'palette'

 L. 223      1096  LOAD_CONST               True
             1098  STORE_FAST               'greyscale'

 L. 226      1100  LOAD_FAST                'file_info'
             1102  LOAD_STR                 'colors'
             1104  BINARY_SUBSCR    
             1106  LOAD_CONST               2
             1108  COMPARE_OP               ==

 L. 225  1110_1112  POP_JUMP_IF_FALSE  1118  'to 1118'
             1114  LOAD_CONST               (0, 255)
             1116  JUMP_FORWARD       1132  'to 1132'
           1118_0  COME_FROM          1110  '1110'

 L. 227      1118  LOAD_GLOBAL              list
             1120  LOAD_GLOBAL              range
             1122  LOAD_FAST                'file_info'
             1124  LOAD_STR                 'colors'
             1126  BINARY_SUBSCR    
             1128  CALL_FUNCTION_1       1  ''
             1130  CALL_FUNCTION_1       1  ''
           1132_0  COME_FROM          1116  '1116'

 L. 224      1132  STORE_FAST               'indices'

 L. 231      1134  LOAD_GLOBAL              enumerate
             1136  LOAD_FAST                'indices'
             1138  CALL_FUNCTION_1       1  ''
             1140  GET_ITER         
           1142_0  COME_FROM          1196  '1196'
           1142_1  COME_FROM          1188  '1188'
             1142  FOR_ITER           1200  'to 1200'
             1144  UNPACK_SEQUENCE_2     2 
             1146  STORE_FAST               'ind'
             1148  STORE_FAST               'val'

 L. 232      1150  LOAD_FAST                'palette'
             1152  LOAD_FAST                'ind'
             1154  LOAD_FAST                'padding'
             1156  BINARY_MULTIPLY  
             1158  LOAD_FAST                'ind'
             1160  LOAD_FAST                'padding'
             1162  BINARY_MULTIPLY  
             1164  LOAD_CONST               3
             1166  BINARY_ADD       
             1168  BUILD_SLICE_2         2 
             1170  BINARY_SUBSCR    
             1172  STORE_FAST               'rgb'

 L. 233      1174  LOAD_FAST                'rgb'
             1176  LOAD_GLOBAL              o8
             1178  LOAD_FAST                'val'
             1180  CALL_FUNCTION_1       1  ''
             1182  LOAD_CONST               3
             1184  BINARY_MULTIPLY  
             1186  COMPARE_OP               !=
         1188_1190  POP_JUMP_IF_FALSE_BACK  1142  'to 1142'

 L. 234      1192  LOAD_CONST               False
             1194  STORE_FAST               'greyscale'
         1196_1198  JUMP_BACK          1142  'to 1142'
           1200_0  COME_FROM          1142  '1142'

 L. 237      1200  LOAD_FAST                'greyscale'
         1202_1204  POP_JUMP_IF_FALSE  1238  'to 1238'

 L. 238      1206  LOAD_FAST                'file_info'
             1208  LOAD_STR                 'colors'
             1210  BINARY_SUBSCR    
             1212  LOAD_CONST               2
             1214  COMPARE_OP               ==
         1216_1218  POP_JUMP_IF_FALSE  1224  'to 1224'
             1220  LOAD_STR                 '1'
             1222  JUMP_FORWARD       1226  'to 1226'
           1224_0  COME_FROM          1216  '1216'
             1224  LOAD_STR                 'L'
           1226_0  COME_FROM          1222  '1222'
             1226  LOAD_FAST                'self'
             1228  STORE_ATTR               mode

 L. 239      1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                mode
             1234  STORE_FAST               'raw_mode'
             1236  JUMP_FORWARD       1272  'to 1272'
           1238_0  COME_FROM          1202  '1202'

 L. 241      1238  LOAD_STR                 'P'
             1240  LOAD_FAST                'self'
             1242  STORE_ATTR               mode

 L. 242      1244  LOAD_GLOBAL              ImagePalette
             1246  LOAD_METHOD              raw

 L. 243      1248  LOAD_FAST                'padding'
             1250  LOAD_CONST               4
             1252  COMPARE_OP               ==
         1254_1256  POP_JUMP_IF_FALSE  1262  'to 1262'
             1258  LOAD_STR                 'BGRX'
             1260  JUMP_FORWARD       1264  'to 1264'
           1262_0  COME_FROM          1254  '1254'
             1262  LOAD_STR                 'BGR'
           1264_0  COME_FROM          1260  '1260'
             1264  LOAD_FAST                'palette'

 L. 242      1266  CALL_METHOD_2         2  ''
             1268  LOAD_FAST                'self'
             1270  STORE_ATTR               palette
           1272_0  COME_FROM          1236  '1236'
           1272_1  COME_FROM          1070  '1070'
           1272_2  COME_FROM          1016  '1016'

 L. 247      1272  LOAD_FAST                'file_info'
             1274  LOAD_STR                 'compression'
             1276  BINARY_SUBSCR    
             1278  LOAD_FAST                'self'
             1280  LOAD_ATTR                info
             1282  LOAD_STR                 'compression'
             1284  STORE_SUBSCR     

 L. 250      1286  LOAD_STR                 'raw'

 L. 251      1288  LOAD_CONST               0
             1290  LOAD_CONST               0
             1292  LOAD_FAST                'file_info'
             1294  LOAD_STR                 'width'
             1296  BINARY_SUBSCR    
             1298  LOAD_FAST                'file_info'
             1300  LOAD_STR                 'height'
             1302  BINARY_SUBSCR    
             1304  BUILD_TUPLE_4         4 

 L. 252      1306  LOAD_FAST                'offset'
         1308_1310  JUMP_IF_TRUE_OR_POP  1320  'to 1320'
             1312  LOAD_FAST                'self'
             1314  LOAD_ATTR                fp
             1316  LOAD_METHOD              tell
             1318  CALL_METHOD_0         0  ''
           1320_0  COME_FROM          1308  '1308'

 L. 254      1320  LOAD_FAST                'raw_mode'

 L. 255      1322  LOAD_FAST                'file_info'
             1324  LOAD_STR                 'width'
             1326  BINARY_SUBSCR    
             1328  LOAD_FAST                'file_info'
             1330  LOAD_STR                 'bits'
             1332  BINARY_SUBSCR    
             1334  BINARY_MULTIPLY  
             1336  LOAD_CONST               31
             1338  BINARY_ADD       
             1340  LOAD_CONST               3
             1342  BINARY_RSHIFT    
             1344  LOAD_CONST               -4
             1346  BINARY_AND       

 L. 256      1348  LOAD_FAST                'file_info'
             1350  LOAD_STR                 'direction'
             1352  BINARY_SUBSCR    

 L. 253      1354  BUILD_TUPLE_3         3 

 L. 249      1356  BUILD_TUPLE_4         4 

 L. 248      1358  BUILD_LIST_1          1 
             1360  LOAD_FAST                'self'
             1362  STORE_ATTR               tile

Parse error at or near `<118>' instruction at offset 178

        def _open(self):
            """ Open file, check magic number and read header """
            head_data = self.fp.read(14)
            if not _accept(head_data):
                raise SyntaxError('Not a BMP file')
            offset = i32head_data10
            self._bitmap(offset=offset)


class DibImageFile(BmpImageFile):
    format = 'DIB'
    format_description = 'Windows Bitmap'

    def _open(self):
        self._bitmap()


SAVE = {'1':('1', 1, 2), 
 'L':('L', 8, 256), 
 'P':('P', 8, 256), 
 'RGB':('BGR', 24, 0), 
 'RGBA':('BGRA', 32, 0)}

def _dib_save(im, fp, filename):
    _save(im, fp, filename, False)


def _save--- This code section failed: ---

 L. 305         0  SETUP_FINALLY        22  'to 22'

 L. 306         2  LOAD_GLOBAL              SAVE
                4  LOAD_FAST                'im'
                6  LOAD_ATTR                mode
                8  BINARY_SUBSCR    
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'rawmode'
               14  STORE_FAST               'bits'
               16  STORE_FAST               'colors'
               18  POP_BLOCK        
               20  JUMP_FORWARD         78  'to 78'
             22_0  COME_FROM_FINALLY     0  '0'

 L. 307        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  <121>                76  ''
               28  POP_TOP          
               30  STORE_FAST               'e'
               32  POP_TOP          
               34  SETUP_FINALLY        68  'to 68'

 L. 308        36  LOAD_GLOBAL              OSError
               38  LOAD_STR                 'cannot write mode '
               40  LOAD_FAST                'im'
               42  LOAD_ATTR                mode
               44  FORMAT_VALUE          0  ''
               46  LOAD_STR                 ' as BMP'
               48  BUILD_STRING_3        3 
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'e'
               54  RAISE_VARARGS_2       2  'exception instance with __cause__'
               56  POP_BLOCK        
               58  POP_EXCEPT       
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  JUMP_FORWARD         78  'to 78'
             68_0  COME_FROM_FINALLY    34  '34'
               68  LOAD_CONST               None
               70  STORE_FAST               'e'
               72  DELETE_FAST              'e'
               74  <48>             
               76  <48>             
             78_0  COME_FROM            66  '66'
             78_1  COME_FROM            20  '20'

 L. 310        78  LOAD_FAST                'im'
               80  LOAD_ATTR                encoderinfo
               82  STORE_FAST               'info'

 L. 312        84  LOAD_FAST                'info'
               86  LOAD_METHOD              get
               88  LOAD_STR                 'dpi'
               90  LOAD_CONST               (96, 96)
               92  CALL_METHOD_2         2  ''
               94  STORE_FAST               'dpi'

 L. 315        96  LOAD_GLOBAL              tuple
               98  LOAD_GLOBAL              map
              100  LOAD_LAMBDA              '<code_object <lambda>>'
              102  LOAD_STR                 '_save.<locals>.<lambda>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              106  LOAD_FAST                'dpi'
              108  CALL_FUNCTION_2       2  ''
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'ppm'

 L. 317       114  LOAD_FAST                'im'
              116  LOAD_ATTR                size
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  LOAD_FAST                'bits'
              124  BINARY_MULTIPLY  
              126  LOAD_CONST               7
              128  BINARY_ADD       
              130  LOAD_CONST               8
              132  BINARY_FLOOR_DIVIDE
              134  LOAD_CONST               3
              136  BINARY_ADD       
              138  LOAD_CONST               -4
              140  BINARY_AND       
              142  STORE_FAST               'stride'

 L. 318       144  LOAD_CONST               40
              146  STORE_FAST               'header'

 L. 319       148  LOAD_FAST                'stride'
              150  LOAD_FAST                'im'
              152  LOAD_ATTR                size
              154  LOAD_CONST               1
              156  BINARY_SUBSCR    
              158  BINARY_MULTIPLY  
              160  STORE_FAST               'image'

 L. 322       162  LOAD_FAST                'bitmap_header'
              164  POP_JUMP_IF_FALSE   240  'to 240'

 L. 323       166  LOAD_CONST               14
              168  LOAD_FAST                'header'
              170  BINARY_ADD       
              172  LOAD_FAST                'colors'
              174  LOAD_CONST               4
              176  BINARY_MULTIPLY  
              178  BINARY_ADD       
              180  STORE_FAST               'offset'

 L. 324       182  LOAD_FAST                'offset'
              184  LOAD_FAST                'image'
              186  BINARY_ADD       
              188  STORE_FAST               'file_size'

 L. 325       190  LOAD_FAST                'file_size'
              192  LOAD_CONST               4294967295
              194  COMPARE_OP               >
              196  POP_JUMP_IF_FALSE   206  'to 206'

 L. 326       198  LOAD_GLOBAL              ValueError
              200  LOAD_STR                 'File size is too large for the BMP format'
              202  CALL_FUNCTION_1       1  ''
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           196  '196'

 L. 327       206  LOAD_FAST                'fp'
              208  LOAD_METHOD              write

 L. 328       210  LOAD_CONST               b'BM'

 L. 329       212  LOAD_GLOBAL              o32
              214  LOAD_FAST                'file_size'
              216  CALL_FUNCTION_1       1  ''

 L. 328       218  BINARY_ADD       

 L. 330       220  LOAD_GLOBAL              o32
              222  LOAD_CONST               0
              224  CALL_FUNCTION_1       1  ''

 L. 328       226  BINARY_ADD       

 L. 331       228  LOAD_GLOBAL              o32
              230  LOAD_FAST                'offset'
              232  CALL_FUNCTION_1       1  ''

 L. 328       234  BINARY_ADD       

 L. 327       236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           164  '164'

 L. 335       240  LOAD_FAST                'fp'
              242  LOAD_METHOD              write

 L. 336       244  LOAD_GLOBAL              o32
              246  LOAD_FAST                'header'
              248  CALL_FUNCTION_1       1  ''

 L. 337       250  LOAD_GLOBAL              o32
              252  LOAD_FAST                'im'
              254  LOAD_ATTR                size
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  CALL_FUNCTION_1       1  ''

 L. 336       262  BINARY_ADD       

 L. 338       264  LOAD_GLOBAL              o32
              266  LOAD_FAST                'im'
              268  LOAD_ATTR                size
              270  LOAD_CONST               1
              272  BINARY_SUBSCR    
              274  CALL_FUNCTION_1       1  ''

 L. 336       276  BINARY_ADD       

 L. 339       278  LOAD_GLOBAL              o16
              280  LOAD_CONST               1
              282  CALL_FUNCTION_1       1  ''

 L. 336       284  BINARY_ADD       

 L. 340       286  LOAD_GLOBAL              o16
              288  LOAD_FAST                'bits'
              290  CALL_FUNCTION_1       1  ''

 L. 336       292  BINARY_ADD       

 L. 341       294  LOAD_GLOBAL              o32
              296  LOAD_CONST               0
              298  CALL_FUNCTION_1       1  ''

 L. 336       300  BINARY_ADD       

 L. 342       302  LOAD_GLOBAL              o32
              304  LOAD_FAST                'image'
              306  CALL_FUNCTION_1       1  ''

 L. 336       308  BINARY_ADD       

 L. 343       310  LOAD_GLOBAL              o32
              312  LOAD_FAST                'ppm'
              314  LOAD_CONST               0
              316  BINARY_SUBSCR    
              318  CALL_FUNCTION_1       1  ''

 L. 336       320  BINARY_ADD       

 L. 344       322  LOAD_GLOBAL              o32
              324  LOAD_FAST                'ppm'
              326  LOAD_CONST               1
              328  BINARY_SUBSCR    
              330  CALL_FUNCTION_1       1  ''

 L. 336       332  BINARY_ADD       

 L. 345       334  LOAD_GLOBAL              o32
              336  LOAD_FAST                'colors'
              338  CALL_FUNCTION_1       1  ''

 L. 336       340  BINARY_ADD       

 L. 346       342  LOAD_GLOBAL              o32
              344  LOAD_FAST                'colors'
              346  CALL_FUNCTION_1       1  ''

 L. 336       348  BINARY_ADD       

 L. 335       350  CALL_METHOD_1         1  ''
              352  POP_TOP          

 L. 349       354  LOAD_FAST                'fp'
              356  LOAD_METHOD              write
              358  LOAD_CONST               b'\x00'
              360  LOAD_FAST                'header'
              362  LOAD_CONST               40
              364  BINARY_SUBTRACT  
              366  BINARY_MULTIPLY  
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 351       372  LOAD_FAST                'im'
              374  LOAD_ATTR                mode
              376  LOAD_STR                 '1'
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   416  'to 416'

 L. 352       384  LOAD_CONST               (0, 255)
              386  GET_ITER         
            388_0  COME_FROM           410  '410'
              388  FOR_ITER            414  'to 414'
              390  STORE_FAST               'i'

 L. 353       392  LOAD_FAST                'fp'
              394  LOAD_METHOD              write
              396  LOAD_GLOBAL              o8
              398  LOAD_FAST                'i'
              400  CALL_FUNCTION_1       1  ''
              402  LOAD_CONST               4
              404  BINARY_MULTIPLY  
              406  CALL_METHOD_1         1  ''
              408  POP_TOP          
          410_412  JUMP_BACK           388  'to 388'
            414_0  COME_FROM           388  '388'
              414  JUMP_FORWARD        496  'to 496'
            416_0  COME_FROM           380  '380'

 L. 354       416  LOAD_FAST                'im'
              418  LOAD_ATTR                mode
              420  LOAD_STR                 'L'
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   464  'to 464'

 L. 355       428  LOAD_GLOBAL              range
              430  LOAD_CONST               256
              432  CALL_FUNCTION_1       1  ''
              434  GET_ITER         
            436_0  COME_FROM           458  '458'
              436  FOR_ITER            462  'to 462'
              438  STORE_FAST               'i'

 L. 356       440  LOAD_FAST                'fp'
              442  LOAD_METHOD              write
              444  LOAD_GLOBAL              o8
              446  LOAD_FAST                'i'
              448  CALL_FUNCTION_1       1  ''
              450  LOAD_CONST               4
              452  BINARY_MULTIPLY  
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
          458_460  JUMP_BACK           436  'to 436'
            462_0  COME_FROM           436  '436'
              462  JUMP_FORWARD        496  'to 496'
            464_0  COME_FROM           424  '424'

 L. 357       464  LOAD_FAST                'im'
              466  LOAD_ATTR                mode
              468  LOAD_STR                 'P'
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   496  'to 496'

 L. 358       476  LOAD_FAST                'fp'
              478  LOAD_METHOD              write
              480  LOAD_FAST                'im'
              482  LOAD_ATTR                im
              484  LOAD_METHOD              getpalette
              486  LOAD_STR                 'RGB'
              488  LOAD_STR                 'BGRX'
              490  CALL_METHOD_2         2  ''
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
            496_0  COME_FROM           472  '472'
            496_1  COME_FROM           462  '462'
            496_2  COME_FROM           414  '414'

 L. 360       496  LOAD_GLOBAL              ImageFile
              498  LOAD_METHOD              _save
              500  LOAD_FAST                'im'
              502  LOAD_FAST                'fp'
              504  LOAD_STR                 'raw'
              506  LOAD_CONST               (0, 0)
              508  LOAD_FAST                'im'
              510  LOAD_ATTR                size
              512  BINARY_ADD       
              514  LOAD_CONST               0
              516  LOAD_FAST                'rawmode'
              518  LOAD_FAST                'stride'
              520  LOAD_CONST               -1
              522  BUILD_TUPLE_3         3 
              524  BUILD_TUPLE_4         4 
              526  BUILD_LIST_1          1 
              528  CALL_METHOD_3         3  ''
              530  POP_TOP          

Parse error at or near `<121>' instruction at offset 26


Image.register_open(BmpImageFile.format, BmpImageFile, _accept)
Image.register_save(BmpImageFile.format, _save)
Image.register_extension(BmpImageFile.format, '.bmp')
Image.register_mime(BmpImageFile.format, 'image/bmp')
Image.register_open(DibImageFile.format, DibImageFile, _dib_accept)
Image.register_save(DibImageFile.format, _dib_save)
Image.register_extension(DibImageFile.format, '.dib')
Image.register_mime(DibImageFile.format, 'image/bmp')