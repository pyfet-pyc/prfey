# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\SunImagePlugin.py
from . import Image, ImageFile, ImagePalette
from ._binary import i32be as i32

def _accept(prefix):
    return len(prefix) >= 4 and i32(prefix) == 1504078485


class SunImageFile(ImageFile.ImageFile):
    format = 'SUN'
    format_description = 'Sun Raster File'

    def _open--- This code section failed: ---

 L.  55         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               32
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  56        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L.  57        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not an SUN raster file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  59        28  LOAD_CONST               32
               30  STORE_FAST               'offset'

 L.  61        32  LOAD_GLOBAL              i32
               34  LOAD_FAST                's'
               36  LOAD_CONST               4
               38  CALL_FUNCTION_2       2  ''
               40  LOAD_GLOBAL              i32
               42  LOAD_FAST                's'
               44  LOAD_CONST               8
               46  CALL_FUNCTION_2       2  ''
               48  BUILD_TUPLE_2         2 
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _size

 L.  63        54  LOAD_GLOBAL              i32
               56  LOAD_FAST                's'
               58  LOAD_CONST               12
               60  CALL_FUNCTION_2       2  ''
               62  STORE_FAST               'depth'

 L.  65        64  LOAD_GLOBAL              i32
               66  LOAD_FAST                's'
               68  LOAD_CONST               20
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'file_type'

 L.  66        74  LOAD_GLOBAL              i32
               76  LOAD_FAST                's'
               78  LOAD_CONST               24
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               'palette_type'

 L.  67        84  LOAD_GLOBAL              i32
               86  LOAD_FAST                's'
               88  LOAD_CONST               28
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'palette_length'

 L.  69        94  LOAD_FAST                'depth'
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   114  'to 114'

 L.  70       102  LOAD_CONST               ('1', '1;I')
              104  UNPACK_SEQUENCE_2     2 
              106  LOAD_FAST                'self'
              108  STORE_ATTR               mode
              110  STORE_FAST               'rawmode'
              112  JUMP_FORWARD        242  'to 242'
            114_0  COME_FROM           100  '100'

 L.  71       114  LOAD_FAST                'depth'
              116  LOAD_CONST               4
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L.  72       122  LOAD_CONST               ('L', 'L;4')
              124  UNPACK_SEQUENCE_2     2 
              126  LOAD_FAST                'self'
              128  STORE_ATTR               mode
              130  STORE_FAST               'rawmode'
              132  JUMP_FORWARD        242  'to 242'
            134_0  COME_FROM           120  '120'

 L.  73       134  LOAD_FAST                'depth'
              136  LOAD_CONST               8
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L.  74       142  LOAD_STR                 'L'
              144  DUP_TOP          
              146  LOAD_FAST                'self'
              148  STORE_ATTR               mode
              150  STORE_FAST               'rawmode'
              152  JUMP_FORWARD        242  'to 242'
            154_0  COME_FROM           140  '140'

 L.  75       154  LOAD_FAST                'depth'
              156  LOAD_CONST               24
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   194  'to 194'

 L.  76       162  LOAD_FAST                'file_type'
              164  LOAD_CONST               3
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   182  'to 182'

 L.  77       170  LOAD_CONST               ('RGB', 'RGB')
              172  UNPACK_SEQUENCE_2     2 
              174  LOAD_FAST                'self'
              176  STORE_ATTR               mode
              178  STORE_FAST               'rawmode'
              180  JUMP_FORWARD        242  'to 242'
            182_0  COME_FROM           168  '168'

 L.  79       182  LOAD_CONST               ('RGB', 'BGR')
              184  UNPACK_SEQUENCE_2     2 
              186  LOAD_FAST                'self'
              188  STORE_ATTR               mode
              190  STORE_FAST               'rawmode'
              192  JUMP_FORWARD        242  'to 242'
            194_0  COME_FROM           160  '160'

 L.  80       194  LOAD_FAST                'depth'
              196  LOAD_CONST               32
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   234  'to 234'

 L.  81       202  LOAD_FAST                'file_type'
              204  LOAD_CONST               3
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   222  'to 222'

 L.  82       210  LOAD_CONST               ('RGB', 'RGBX')
              212  UNPACK_SEQUENCE_2     2 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               mode
              218  STORE_FAST               'rawmode'
              220  JUMP_FORWARD        242  'to 242'
            222_0  COME_FROM           208  '208'

 L.  84       222  LOAD_CONST               ('RGB', 'BGRX')
              224  UNPACK_SEQUENCE_2     2 
              226  LOAD_FAST                'self'
              228  STORE_ATTR               mode
              230  STORE_FAST               'rawmode'
              232  JUMP_FORWARD        242  'to 242'
            234_0  COME_FROM           200  '200'

 L.  86       234  LOAD_GLOBAL              SyntaxError
              236  LOAD_STR                 'Unsupported Mode/Bit Depth'
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           232  '232'
            242_1  COME_FROM           220  '220'
            242_2  COME_FROM           192  '192'
            242_3  COME_FROM           180  '180'
            242_4  COME_FROM           152  '152'
            242_5  COME_FROM           132  '132'
            242_6  COME_FROM           112  '112'

 L.  88       242  LOAD_FAST                'palette_length'
          244_246  POP_JUMP_IF_FALSE   344  'to 344'

 L.  89       248  LOAD_FAST                'palette_length'
              250  LOAD_CONST               1024
              252  COMPARE_OP               >
          254_256  POP_JUMP_IF_FALSE   266  'to 266'

 L.  90       258  LOAD_GLOBAL              SyntaxError
              260  LOAD_STR                 'Unsupported Color Palette Length'
              262  CALL_FUNCTION_1       1  ''
              264  RAISE_VARARGS_1       1  'exception instance'
            266_0  COME_FROM           254  '254'

 L.  92       266  LOAD_FAST                'palette_type'
              268  LOAD_CONST               1
              270  COMPARE_OP               !=
          272_274  POP_JUMP_IF_FALSE   284  'to 284'

 L.  93       276  LOAD_GLOBAL              SyntaxError
              278  LOAD_STR                 'Unsupported Palette Type'
              280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
            284_0  COME_FROM           272  '272'

 L.  95       284  LOAD_FAST                'offset'
              286  LOAD_FAST                'palette_length'
              288  BINARY_ADD       
              290  STORE_FAST               'offset'

 L.  96       292  LOAD_GLOBAL              ImagePalette
              294  LOAD_METHOD              raw
              296  LOAD_STR                 'RGB;L'
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                fp
              302  LOAD_METHOD              read
              304  LOAD_FAST                'palette_length'
              306  CALL_METHOD_1         1  ''
              308  CALL_METHOD_2         2  ''
              310  LOAD_FAST                'self'
              312  STORE_ATTR               palette

 L.  97       314  LOAD_FAST                'self'
              316  LOAD_ATTR                mode
              318  LOAD_STR                 'L'
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   344  'to 344'

 L.  98       326  LOAD_STR                 'P'
              328  LOAD_FAST                'self'
              330  STORE_ATTR               mode

 L.  99       332  LOAD_FAST                'rawmode'
              334  LOAD_METHOD              replace
              336  LOAD_STR                 'L'
              338  LOAD_STR                 'P'
              340  CALL_METHOD_2         2  ''
              342  STORE_FAST               'rawmode'
            344_0  COME_FROM           322  '322'
            344_1  COME_FROM           244  '244'

 L. 102       344  LOAD_FAST                'self'
              346  LOAD_ATTR                size
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  LOAD_FAST                'depth'
              354  BINARY_MULTIPLY  
              356  LOAD_CONST               15
              358  BINARY_ADD       
              360  LOAD_CONST               16
              362  BINARY_FLOOR_DIVIDE
              364  LOAD_CONST               2
              366  BINARY_MULTIPLY  
              368  STORE_FAST               'stride'

 L. 122       370  LOAD_FAST                'file_type'
              372  LOAD_CONST               (0, 1, 3, 4, 5)
              374  <118>                 0  ''
          376_378  POP_JUMP_IF_FALSE   408  'to 408'

 L. 123       380  LOAD_STR                 'raw'
              382  LOAD_CONST               (0, 0)
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                size
              388  BINARY_ADD       
              390  LOAD_FAST                'offset'
              392  LOAD_FAST                'rawmode'
              394  LOAD_FAST                'stride'
              396  BUILD_TUPLE_2         2 
              398  BUILD_TUPLE_4         4 
              400  BUILD_LIST_1          1 
              402  LOAD_FAST                'self'
              404  STORE_ATTR               tile
              406  JUMP_FORWARD        450  'to 450'
            408_0  COME_FROM           376  '376'

 L. 124       408  LOAD_FAST                'file_type'
              410  LOAD_CONST               2
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   442  'to 442'

 L. 125       418  LOAD_STR                 'sun_rle'
              420  LOAD_CONST               (0, 0)
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                size
              426  BINARY_ADD       
              428  LOAD_FAST                'offset'
              430  LOAD_FAST                'rawmode'
              432  BUILD_TUPLE_4         4 
              434  BUILD_LIST_1          1 
              436  LOAD_FAST                'self'
              438  STORE_ATTR               tile
              440  JUMP_FORWARD        450  'to 450'
            442_0  COME_FROM           414  '414'

 L. 127       442  LOAD_GLOBAL              SyntaxError
              444  LOAD_STR                 'Unsupported Sun Raster file type'
              446  CALL_FUNCTION_1       1  ''
              448  RAISE_VARARGS_1       1  'exception instance'
            450_0  COME_FROM           440  '440'
            450_1  COME_FROM           406  '406'

Parse error at or near `<118>' instruction at offset 374


Image.register_open(SunImageFile.format, SunImageFile, _accept)
Image.register_extension(SunImageFile.format, '.ras')