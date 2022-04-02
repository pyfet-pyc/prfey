# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\FpxImagePlugin.py
import olefile
from . import Image, ImageFile
from ._binary import i32le as i32
MODES = {32766:('A', 'L'), 
 (65536,):('L', 'L'), 
 (98304, 98302):('RGBA', 'LA'), 
 (131072, 131073, 131074):('RGB', 'YCC;P'), 
 (163840, 163841, 163842, 163838):('RGBA', 'YCCA;P'), 
 (196608, 196609, 196610):('RGB', 'RGB'), 
 (229376, 229377, 229378, 229374):('RGBA', 'RGBA')}

def _accept(prefix):
    return prefix[:8] == olefile.MAGIC


class FpxImageFile(ImageFile.ImageFile):
    format = 'FPX'
    format_description = 'FlashPix'

    def _open--- This code section failed: ---

 L.  60         0  SETUP_FINALLY        20  'to 20'

 L.  61         2  LOAD_GLOBAL              olefile
                4  LOAD_METHOD              OleFileIO
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fp
               10  CALL_METHOD_1         1  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               ole
               16  POP_BLOCK        
               18  JUMP_FORWARD         66  'to 66'
             20_0  COME_FROM_FINALLY     0  '0'

 L.  62        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  <121>                64  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        56  'to 56'

 L.  63        34  LOAD_GLOBAL              SyntaxError
               36  LOAD_STR                 'not an FPX file; invalid OLE file'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_FAST                'e'
               42  RAISE_VARARGS_2       2  'exception instance with __cause__'
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'e'
               52  DELETE_FAST              'e'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM_FINALLY    32  '32'
               56  LOAD_CONST               None
               58  STORE_FAST               'e'
               60  DELETE_FAST              'e'
               62  <48>             
               64  <48>             
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            18  '18'

 L.  65        66  LOAD_FAST                'self'
               68  LOAD_ATTR                ole
               70  LOAD_ATTR                root
               72  LOAD_ATTR                clsid
               74  LOAD_STR                 '56616700-C154-11CE-8553-00AA00A1F95B'
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.  66        80  LOAD_GLOBAL              SyntaxError
               82  LOAD_STR                 'not an FPX file; bad root CLSID'
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'

 L.  68        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _open_index
               92  LOAD_CONST               1
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

Parse error at or near `<121>' instruction at offset 24

    def _open_index--- This code section failed: ---

 L.  74         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ole
                4  LOAD_METHOD              getproperties

 L.  75         6  LOAD_STR                 'Data Object Store '
                8  LOAD_FAST                'index'
               10  LOAD_STR                 '06d'
               12  FORMAT_VALUE_ATTR     4  ''
               14  BUILD_STRING_2        2 
               16  LOAD_STR                 '\x05Image Contents'
               18  BUILD_LIST_2          2 

 L.  74        20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'prop'

 L.  80        24  LOAD_FAST                'prop'
               26  LOAD_CONST               16777218
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'prop'
               32  LOAD_CONST               16777219
               34  BINARY_SUBSCR    
               36  BUILD_TUPLE_2         2 
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _size

 L.  82        42  LOAD_GLOBAL              max
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                size
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'size'

 L.  83        52  LOAD_CONST               1
               54  STORE_FAST               'i'
             56_0  COME_FROM            80  '80'

 L.  84        56  LOAD_FAST                'size'
               58  LOAD_CONST               64
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L.  85        64  LOAD_FAST                'size'
               66  LOAD_CONST               2
               68  BINARY_TRUE_DIVIDE
               70  STORE_FAST               'size'

 L.  86        72  LOAD_FAST                'i'
               74  LOAD_CONST               1
               76  INPLACE_ADD      
               78  STORE_FAST               'i'
               80  JUMP_BACK            56  'to 56'
             82_0  COME_FROM            62  '62'

 L.  87        82  LOAD_FAST                'i'
               84  LOAD_CONST               1
               86  BINARY_SUBTRACT  
               88  LOAD_FAST                'self'
               90  STORE_ATTR               maxid

 L.  95        92  LOAD_FAST                'self'
               94  LOAD_ATTR                maxid
               96  LOAD_CONST               16
               98  BINARY_LSHIFT    
              100  STORE_FAST               'id'

 L.  97       102  LOAD_FAST                'prop'
              104  LOAD_CONST               33554434
              106  LOAD_FAST                'id'
              108  BINARY_OR        
              110  BINARY_SUBSCR    
              112  STORE_FAST               's'

 L.  99       114  BUILD_LIST_0          0 
              116  STORE_FAST               'colors'

 L. 100       118  LOAD_GLOBAL              i32
              120  LOAD_FAST                's'
              122  LOAD_CONST               4
              124  CALL_FUNCTION_2       2  ''
              126  STORE_FAST               'bands'

 L. 101       128  LOAD_FAST                'bands'
              130  LOAD_CONST               4
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L. 102       136  LOAD_GLOBAL              OSError
              138  LOAD_STR                 'Invalid number of bands'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           134  '134'

 L. 103       144  LOAD_GLOBAL              range
              146  LOAD_FAST                'bands'
              148  CALL_FUNCTION_1       1  ''
              150  GET_ITER         
            152_0  COME_FROM           184  '184'
              152  FOR_ITER            186  'to 186'
              154  STORE_FAST               'i'

 L. 105       156  LOAD_FAST                'colors'
              158  LOAD_METHOD              append
              160  LOAD_GLOBAL              i32
              162  LOAD_FAST                's'
              164  LOAD_CONST               8
              166  LOAD_FAST                'i'
              168  LOAD_CONST               4
              170  BINARY_MULTIPLY  
              172  BINARY_ADD       
              174  CALL_FUNCTION_2       2  ''
              176  LOAD_CONST               2147483647
              178  BINARY_AND       
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK           152  'to 152'
            186_0  COME_FROM           152  '152'

 L. 107       186  LOAD_GLOBAL              MODES
              188  LOAD_GLOBAL              tuple
              190  LOAD_FAST                'colors'
              192  CALL_FUNCTION_1       1  ''
              194  BINARY_SUBSCR    
              196  UNPACK_SEQUENCE_2     2 
              198  LOAD_FAST                'self'
              200  STORE_ATTR               mode
              202  LOAD_FAST                'self'
              204  STORE_ATTR               rawmode

 L. 110       206  BUILD_MAP_0           0 
              208  LOAD_FAST                'self'
              210  STORE_ATTR               jpeg

 L. 111       212  LOAD_GLOBAL              range
              214  LOAD_CONST               256
              216  CALL_FUNCTION_1       1  ''
              218  GET_ITER         
            220_0  COME_FROM           258  '258'
            220_1  COME_FROM           242  '242'
              220  FOR_ITER            260  'to 260'
              222  STORE_FAST               'i'

 L. 112       224  LOAD_CONST               50331649
              226  LOAD_FAST                'i'
              228  LOAD_CONST               16
              230  BINARY_LSHIFT    
              232  BINARY_OR        
              234  STORE_FAST               'id'

 L. 113       236  LOAD_FAST                'id'
              238  LOAD_FAST                'prop'
              240  <118>                 0  ''
              242  POP_JUMP_IF_FALSE_BACK   220  'to 220'

 L. 114       244  LOAD_FAST                'prop'
              246  LOAD_FAST                'id'
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                jpeg
              254  LOAD_FAST                'i'
              256  STORE_SUBSCR     
              258  JUMP_BACK           220  'to 220'
            260_0  COME_FROM           220  '220'

 L. 116       260  LOAD_FAST                'self'
              262  LOAD_METHOD              _open_subimage
              264  LOAD_CONST               1
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                maxid
              270  CALL_METHOD_2         2  ''
              272  POP_TOP          

Parse error at or near `<118>' instruction at offset 240

    def _open_subimage--- This code section failed: ---

 L. 123         0  LOAD_STR                 'Data Object Store '
                2  LOAD_FAST                'index'
                4  LOAD_STR                 '06d'
                6  FORMAT_VALUE_ATTR     4  ''
                8  BUILD_STRING_2        2 

 L. 124        10  LOAD_STR                 'Resolution '
               12  LOAD_FAST                'subimage'
               14  LOAD_STR                 '04d'
               16  FORMAT_VALUE_ATTR     4  ''
               18  BUILD_STRING_2        2 

 L. 125        20  LOAD_STR                 'Subimage 0000 Header'

 L. 122        22  BUILD_LIST_3          3 
               24  STORE_FAST               'stream'

 L. 128        26  LOAD_FAST                'self'
               28  LOAD_ATTR                ole
               30  LOAD_METHOD              openstream
               32  LOAD_FAST                'stream'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'fp'

 L. 131        38  LOAD_FAST                'fp'
               40  LOAD_METHOD              read
               42  LOAD_CONST               28
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 134        48  LOAD_FAST                'fp'
               50  LOAD_METHOD              read
               52  LOAD_CONST               36
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               's'

 L. 136        58  LOAD_GLOBAL              i32
               60  LOAD_FAST                's'
               62  LOAD_CONST               4
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_GLOBAL              i32
               68  LOAD_FAST                's'
               70  LOAD_CONST               8
               72  CALL_FUNCTION_2       2  ''
               74  BUILD_TUPLE_2         2 
               76  STORE_FAST               'size'

 L. 138        78  LOAD_GLOBAL              i32
               80  LOAD_FAST                's'
               82  LOAD_CONST               16
               84  CALL_FUNCTION_2       2  ''
               86  LOAD_GLOBAL              i32
               88  LOAD_FAST                's'
               90  LOAD_CONST               20
               92  CALL_FUNCTION_2       2  ''
               94  BUILD_TUPLE_2         2 
               96  STORE_FAST               'tilesize'

 L. 140        98  LOAD_GLOBAL              i32
              100  LOAD_FAST                's'
              102  LOAD_CONST               28
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'offset'

 L. 141       108  LOAD_GLOBAL              i32
              110  LOAD_FAST                's'
              112  LOAD_CONST               32
              114  CALL_FUNCTION_2       2  ''
              116  STORE_FAST               'length'

 L. 143       118  LOAD_FAST                'size'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                size
              124  COMPARE_OP               !=
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 144       128  LOAD_GLOBAL              OSError
              130  LOAD_STR                 'subimage mismatch'
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 147       136  LOAD_FAST                'fp'
              138  LOAD_METHOD              seek
              140  LOAD_CONST               28
              142  LOAD_FAST                'offset'
              144  BINARY_ADD       
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 148       150  LOAD_FAST                'fp'
              152  LOAD_METHOD              read
              154  LOAD_GLOBAL              i32
              156  LOAD_FAST                's'
              158  LOAD_CONST               12
              160  CALL_FUNCTION_2       2  ''
              162  LOAD_FAST                'length'
              164  BINARY_MULTIPLY  
              166  CALL_METHOD_1         1  ''
              168  STORE_FAST               's'

 L. 150       170  LOAD_CONST               0
              172  DUP_TOP          
              174  STORE_FAST               'x'
              176  STORE_FAST               'y'

 L. 151       178  LOAD_FAST                'size'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'xsize'
              184  STORE_FAST               'ysize'

 L. 152       186  LOAD_FAST                'tilesize'
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'xtile'
              192  STORE_FAST               'ytile'

 L. 153       194  BUILD_LIST_0          0 
              196  LOAD_FAST                'self'
              198  STORE_ATTR               tile

 L. 155       200  LOAD_GLOBAL              range
              202  LOAD_CONST               0
              204  LOAD_GLOBAL              len
              206  LOAD_FAST                's'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_FAST                'length'
              212  CALL_FUNCTION_3       3  ''
              214  GET_ITER         
            216_0  COME_FROM           558  '558'
            216_1  COME_FROM           550  '550'
            216_2  COME_FROM           528  '528'
          216_218  FOR_ITER            560  'to 560'
              220  STORE_FAST               'i'

 L. 157       222  LOAD_GLOBAL              i32
              224  LOAD_FAST                's'
              226  LOAD_FAST                'i'
              228  LOAD_CONST               8
              230  BINARY_ADD       
              232  CALL_FUNCTION_2       2  ''
              234  STORE_FAST               'compression'

 L. 159       236  LOAD_FAST                'compression'
              238  LOAD_CONST               0
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   296  'to 296'

 L. 160       246  LOAD_FAST                'self'
              248  LOAD_ATTR                tile
              250  LOAD_METHOD              append

 L. 162       252  LOAD_STR                 'raw'

 L. 163       254  LOAD_FAST                'x'
              256  LOAD_FAST                'y'
              258  LOAD_FAST                'x'
              260  LOAD_FAST                'xtile'
              262  BINARY_ADD       
              264  LOAD_FAST                'y'
              266  LOAD_FAST                'ytile'
              268  BINARY_ADD       
              270  BUILD_TUPLE_4         4 

 L. 164       272  LOAD_GLOBAL              i32
              274  LOAD_FAST                's'
              276  LOAD_FAST                'i'
              278  CALL_FUNCTION_2       2  ''
              280  LOAD_CONST               28
              282  BINARY_ADD       

 L. 165       284  LOAD_FAST                'self'
              286  LOAD_ATTR                rawmode

 L. 161       288  BUILD_TUPLE_4         4 

 L. 160       290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  JUMP_FORWARD        514  'to 514'
            296_0  COME_FROM           242  '242'

 L. 169       296  LOAD_FAST                'compression'
              298  LOAD_CONST               1
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   368  'to 368'

 L. 172       306  LOAD_FAST                'self'
              308  LOAD_ATTR                tile
              310  LOAD_METHOD              append

 L. 174       312  LOAD_STR                 'fill'

 L. 175       314  LOAD_FAST                'x'
              316  LOAD_FAST                'y'
              318  LOAD_FAST                'x'
              320  LOAD_FAST                'xtile'
              322  BINARY_ADD       
              324  LOAD_FAST                'y'
              326  LOAD_FAST                'ytile'
              328  BINARY_ADD       
              330  BUILD_TUPLE_4         4 

 L. 176       332  LOAD_GLOBAL              i32
              334  LOAD_FAST                's'
              336  LOAD_FAST                'i'
              338  CALL_FUNCTION_2       2  ''
              340  LOAD_CONST               28
              342  BINARY_ADD       

 L. 177       344  LOAD_FAST                'self'
              346  LOAD_ATTR                rawmode
              348  LOAD_FAST                's'
              350  LOAD_CONST               12
              352  LOAD_CONST               16
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  BUILD_TUPLE_2         2 

 L. 173       360  BUILD_TUPLE_4         4 

 L. 172       362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  JUMP_FORWARD        514  'to 514'
            368_0  COME_FROM           302  '302'

 L. 181       368  LOAD_FAST                'compression'
              370  LOAD_CONST               2
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   506  'to 506'

 L. 183       378  LOAD_FAST                's'
              380  LOAD_CONST               14
              382  BINARY_SUBSCR    
              384  STORE_FAST               'internal_color_conversion'

 L. 184       386  LOAD_FAST                's'
              388  LOAD_CONST               15
              390  BINARY_SUBSCR    
              392  STORE_FAST               'jpeg_tables'

 L. 185       394  LOAD_FAST                'self'
              396  LOAD_ATTR                rawmode
              398  STORE_FAST               'rawmode'

 L. 187       400  LOAD_FAST                'internal_color_conversion'
          402_404  POP_JUMP_IF_FALSE   432  'to 432'

 L. 189       406  LOAD_FAST                'rawmode'
              408  LOAD_STR                 'RGBA'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   426  'to 426'

 L. 193       416  LOAD_CONST               ('YCbCrK', 'CMYK')
              418  UNPACK_SEQUENCE_2     2 
              420  STORE_FAST               'jpegmode'
              422  STORE_FAST               'rawmode'
              424  JUMP_FORWARD        430  'to 430'
            426_0  COME_FROM           412  '412'

 L. 195       426  LOAD_CONST               None
              428  STORE_FAST               'jpegmode'
            430_0  COME_FROM           424  '424'
              430  JUMP_FORWARD        436  'to 436'
            432_0  COME_FROM           402  '402'

 L. 199       432  LOAD_FAST                'rawmode'
              434  STORE_FAST               'jpegmode'
            436_0  COME_FROM           430  '430'

 L. 201       436  LOAD_FAST                'self'
              438  LOAD_ATTR                tile
              440  LOAD_METHOD              append

 L. 203       442  LOAD_STR                 'jpeg'

 L. 204       444  LOAD_FAST                'x'
              446  LOAD_FAST                'y'
              448  LOAD_FAST                'x'
              450  LOAD_FAST                'xtile'
              452  BINARY_ADD       
              454  LOAD_FAST                'y'
              456  LOAD_FAST                'ytile'
              458  BINARY_ADD       
              460  BUILD_TUPLE_4         4 

 L. 205       462  LOAD_GLOBAL              i32
              464  LOAD_FAST                's'
              466  LOAD_FAST                'i'
              468  CALL_FUNCTION_2       2  ''
              470  LOAD_CONST               28
              472  BINARY_ADD       

 L. 206       474  LOAD_FAST                'rawmode'
              476  LOAD_FAST                'jpegmode'
              478  BUILD_TUPLE_2         2 

 L. 202       480  BUILD_TUPLE_4         4 

 L. 201       482  CALL_METHOD_1         1  ''
              484  POP_TOP          

 L. 213       486  LOAD_FAST                'jpeg_tables'
          488_490  POP_JUMP_IF_FALSE   514  'to 514'

 L. 214       492  LOAD_FAST                'self'
              494  LOAD_ATTR                jpeg
              496  LOAD_FAST                'jpeg_tables'
              498  BINARY_SUBSCR    
              500  LOAD_FAST                'self'
              502  STORE_ATTR               tile_prefix
              504  JUMP_FORWARD        514  'to 514'
            506_0  COME_FROM           374  '374'

 L. 217       506  LOAD_GLOBAL              OSError
              508  LOAD_STR                 'unknown/invalid compression'
              510  CALL_FUNCTION_1       1  ''
              512  RAISE_VARARGS_1       1  'exception instance'
            514_0  COME_FROM           504  '504'
            514_1  COME_FROM           488  '488'
            514_2  COME_FROM           366  '366'
            514_3  COME_FROM           294  '294'

 L. 219       514  LOAD_FAST                'x'
              516  LOAD_FAST                'xtile'
              518  BINARY_ADD       
              520  STORE_FAST               'x'

 L. 220       522  LOAD_FAST                'x'
              524  LOAD_FAST                'xsize'
              526  COMPARE_OP               >=
              528  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 221       530  LOAD_CONST               0
              532  LOAD_FAST                'y'
              534  LOAD_FAST                'ytile'
              536  BINARY_ADD       
              538  ROT_TWO          
              540  STORE_FAST               'x'
              542  STORE_FAST               'y'

 L. 222       544  LOAD_FAST                'y'
              546  LOAD_FAST                'ysize'
              548  COMPARE_OP               >=
              550  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 223       552  POP_TOP          
          554_556  JUMP_FORWARD        560  'to 560'
              558  JUMP_BACK           216  'to 216'
            560_0  COME_FROM           554  '554'
            560_1  COME_FROM           216  '216'

 L. 225       560  LOAD_FAST                'stream'
              562  LOAD_FAST                'self'
              564  STORE_ATTR               stream

 L. 226       566  LOAD_CONST               None
              568  LOAD_FAST                'self'
              570  STORE_ATTR               fp

Parse error at or near `JUMP_FORWARD' instruction at offset 554_556

    def load(self):
        if not self.fp:
            self.fp = self.ole.openstream(self.stream[:2] + ['Subimage 0000 Data'])
        return ImageFile.ImageFile.loadself


Image.register_open(FpxImageFile.format, FpxImageFile, _accept)
Image.register_extension(FpxImageFile.format, '.fpx')