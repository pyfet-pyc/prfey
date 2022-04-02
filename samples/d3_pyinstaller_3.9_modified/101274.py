# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\DdsImagePlugin.py
"""
A Pillow loader for .dds files (S3TC-compressed aka DXTC)
Jerome Leclanche <jerome@leclan.ch>

Documentation:
  https://web.archive.org/web/20170802060935/http://oss.sgi.com/projects/ogl-sample/registry/EXT/texture_compression_s3tc.txt

The contents of this file are hereby released in the public domain (CC0)
Full text of the CC0 license:
  https://creativecommons.org/publicdomain/zero/1.0/
"""
import struct
from io import BytesIO
from . import Image, ImageFile
DDS_MAGIC = 542327876
DDSD_CAPS = 1
DDSD_HEIGHT = 2
DDSD_WIDTH = 4
DDSD_PITCH = 8
DDSD_PIXELFORMAT = 4096
DDSD_MIPMAPCOUNT = 131072
DDSD_LINEARSIZE = 524288
DDSD_DEPTH = 8388608
DDSCAPS_COMPLEX = 8
DDSCAPS_TEXTURE = 4096
DDSCAPS_MIPMAP = 4194304
DDSCAPS2_CUBEMAP = 512
DDSCAPS2_CUBEMAP_POSITIVEX = 1024
DDSCAPS2_CUBEMAP_NEGATIVEX = 2048
DDSCAPS2_CUBEMAP_POSITIVEY = 4096
DDSCAPS2_CUBEMAP_NEGATIVEY = 8192
DDSCAPS2_CUBEMAP_POSITIVEZ = 16384
DDSCAPS2_CUBEMAP_NEGATIVEZ = 32768
DDSCAPS2_VOLUME = 2097152
DDPF_ALPHAPIXELS = 1
DDPF_ALPHA = 2
DDPF_FOURCC = 4
DDPF_PALETTEINDEXED8 = 32
DDPF_RGB = 64
DDPF_LUMINANCE = 131072
DDS_FOURCC = DDPF_FOURCC
DDS_RGB = DDPF_RGB
DDS_RGBA = DDPF_RGB | DDPF_ALPHAPIXELS
DDS_LUMINANCE = DDPF_LUMINANCE
DDS_LUMINANCEA = DDPF_LUMINANCE | DDPF_ALPHAPIXELS
DDS_ALPHA = DDPF_ALPHA
DDS_PAL8 = DDPF_PALETTEINDEXED8
DDS_HEADER_FLAGS_TEXTURE = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT
DDS_HEADER_FLAGS_MIPMAP = DDSD_MIPMAPCOUNT
DDS_HEADER_FLAGS_VOLUME = DDSD_DEPTH
DDS_HEADER_FLAGS_PITCH = DDSD_PITCH
DDS_HEADER_FLAGS_LINEARSIZE = DDSD_LINEARSIZE
DDS_HEIGHT = DDSD_HEIGHT
DDS_WIDTH = DDSD_WIDTH
DDS_SURFACE_FLAGS_TEXTURE = DDSCAPS_TEXTURE
DDS_SURFACE_FLAGS_MIPMAP = DDSCAPS_COMPLEX | DDSCAPS_MIPMAP
DDS_SURFACE_FLAGS_CUBEMAP = DDSCAPS_COMPLEX
DDS_CUBEMAP_POSITIVEX = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEX
DDS_CUBEMAP_NEGATIVEX = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEX
DDS_CUBEMAP_POSITIVEY = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEY
DDS_CUBEMAP_NEGATIVEY = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEY
DDS_CUBEMAP_POSITIVEZ = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEZ
DDS_CUBEMAP_NEGATIVEZ = DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEZ
DXT1_FOURCC = 827611204
DXT3_FOURCC = 861165636
DXT5_FOURCC = 894720068
DXGI_FORMAT_R8G8B8A8_TYPELESS = 27
DXGI_FORMAT_R8G8B8A8_UNORM = 28
DXGI_FORMAT_R8G8B8A8_UNORM_SRGB = 29
DXGI_FORMAT_BC7_TYPELESS = 97
DXGI_FORMAT_BC7_UNORM = 98
DXGI_FORMAT_BC7_UNORM_SRGB = 99

class DdsImageFile(ImageFile.ImageFile):
    format = 'DDS'
    format_description = 'DirectDraw Surface'

    def _open--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL              struct
                2  LOAD_METHOD              unpack
                4  LOAD_STR                 '<II'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fp
               10  LOAD_METHOD              read
               12  LOAD_CONST               8
               14  CALL_METHOD_1         1  ''
               16  CALL_METHOD_2         2  ''
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'magic'
               22  STORE_FAST               'header_size'

 L. 111        24  LOAD_FAST                'header_size'
               26  LOAD_CONST               124
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    50  'to 50'

 L. 112        32  LOAD_GLOBAL              OSError
               34  LOAD_STR                 'Unsupported header size '
               36  LOAD_GLOBAL              repr
               38  LOAD_FAST                'header_size'
               40  CALL_FUNCTION_1       1  ''
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_2        2 
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            30  '30'

 L. 113        50  LOAD_FAST                'self'
               52  LOAD_ATTR                fp
               54  LOAD_METHOD              read
               56  LOAD_FAST                'header_size'
               58  LOAD_CONST               4
               60  BINARY_SUBTRACT  
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'header_bytes'

 L. 114        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'header_bytes'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               120
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    98  'to 98'

 L. 115        78  LOAD_GLOBAL              OSError
               80  LOAD_STR                 'Incomplete header: '
               82  LOAD_GLOBAL              len
               84  LOAD_FAST                'header_bytes'
               86  CALL_FUNCTION_1       1  ''
               88  FORMAT_VALUE          0  ''
               90  LOAD_STR                 ' bytes'
               92  BUILD_STRING_3        3 
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            76  '76'

 L. 116        98  LOAD_GLOBAL              BytesIO
              100  LOAD_FAST                'header_bytes'
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'header'

 L. 118       106  LOAD_GLOBAL              struct
              108  LOAD_METHOD              unpack
              110  LOAD_STR                 '<3I'
              112  LOAD_FAST                'header'
              114  LOAD_METHOD              read
              116  LOAD_CONST               12
              118  CALL_METHOD_1         1  ''
              120  CALL_METHOD_2         2  ''
              122  UNPACK_SEQUENCE_3     3 
              124  STORE_FAST               'flags'
              126  STORE_FAST               'height'
              128  STORE_FAST               'width'

 L. 119       130  LOAD_FAST                'width'
              132  LOAD_FAST                'height'
              134  BUILD_TUPLE_2         2 
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _size

 L. 120       140  LOAD_STR                 'RGBA'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               mode

 L. 122       146  LOAD_GLOBAL              struct
              148  LOAD_METHOD              unpack
              150  LOAD_STR                 '<3I'
              152  LOAD_FAST                'header'
              154  LOAD_METHOD              read
              156  LOAD_CONST               12
              158  CALL_METHOD_1         1  ''
              160  CALL_METHOD_2         2  ''
              162  UNPACK_SEQUENCE_3     3 
              164  STORE_FAST               'pitch'
              166  STORE_FAST               'depth'
              168  STORE_FAST               'mipmaps'

 L. 123       170  LOAD_GLOBAL              struct
              172  LOAD_METHOD              unpack
              174  LOAD_STR                 '<11I'
              176  LOAD_FAST                'header'
              178  LOAD_METHOD              read
              180  LOAD_CONST               44
              182  CALL_METHOD_1         1  ''
              184  CALL_METHOD_2         2  ''
              186  POP_TOP          

 L. 126       188  LOAD_GLOBAL              struct
              190  LOAD_METHOD              unpack
              192  LOAD_STR                 '<2I'
              194  LOAD_FAST                'header'
              196  LOAD_METHOD              read
              198  LOAD_CONST               8
              200  CALL_METHOD_1         1  ''
              202  CALL_METHOD_2         2  ''
              204  UNPACK_SEQUENCE_2     2 
              206  STORE_FAST               'pfsize'
              208  STORE_FAST               'pfflags'

 L. 127       210  LOAD_FAST                'header'
              212  LOAD_METHOD              read
              214  LOAD_CONST               4
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'fourcc'

 L. 128       220  LOAD_GLOBAL              struct
              222  LOAD_METHOD              unpack
              224  LOAD_STR                 '<I'
              226  LOAD_FAST                'header'
              228  LOAD_METHOD              read
              230  LOAD_CONST               4
              232  CALL_METHOD_1         1  ''
              234  CALL_METHOD_2         2  ''
              236  UNPACK_SEQUENCE_1     1 
              238  STORE_FAST               'bitcount'

 L. 129       240  LOAD_GLOBAL              struct
              242  LOAD_METHOD              unpack
              244  LOAD_STR                 '<4I'
              246  LOAD_FAST                'header'
              248  LOAD_METHOD              read
              250  LOAD_CONST               16
              252  CALL_METHOD_1         1  ''
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'masks'

 L. 130       258  LOAD_FAST                'pfflags'
              260  LOAD_CONST               64
              262  BINARY_AND       
          264_266  POP_JUMP_IF_FALSE   372  'to 372'

 L. 132       268  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              270  LOAD_STR                 'DdsImageFile._open.<locals>.<dictcomp>'
              272  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              274  LOAD_GLOBAL              enumerate
              276  LOAD_FAST                'masks'
              278  CALL_FUNCTION_1       1  ''
              280  GET_ITER         
              282  CALL_FUNCTION_1       1  ''
              284  STORE_FAST               'masks'

 L. 133       286  LOAD_STR                 ''
              288  STORE_FAST               'rawmode'

 L. 134       290  LOAD_FAST                'bitcount'
              292  LOAD_CONST               32
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   312  'to 312'

 L. 135       300  LOAD_FAST                'rawmode'
              302  LOAD_FAST                'masks'
              304  LOAD_CONST               4278190080
              306  BINARY_SUBSCR    
              308  INPLACE_ADD      
              310  STORE_FAST               'rawmode'
            312_0  COME_FROM           296  '296'

 L. 136       312  LOAD_FAST                'rawmode'
              314  LOAD_FAST                'masks'
              316  LOAD_CONST               16711680
              318  BINARY_SUBSCR    
              320  LOAD_FAST                'masks'
              322  LOAD_CONST               65280
              324  BINARY_SUBSCR    
              326  BINARY_ADD       
              328  LOAD_FAST                'masks'
              330  LOAD_CONST               255
              332  BINARY_SUBSCR    
              334  BINARY_ADD       
              336  INPLACE_ADD      
              338  STORE_FAST               'rawmode'

 L. 138       340  LOAD_STR                 'raw'
              342  LOAD_CONST               (0, 0)
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                size
              348  BINARY_ADD       
              350  LOAD_CONST               0
              352  LOAD_FAST                'rawmode'
              354  LOAD_CONST               0
              356  LOAD_CONST               1
              358  BUILD_TUPLE_3         3 
              360  BUILD_TUPLE_4         4 
              362  BUILD_LIST_1          1 
              364  LOAD_FAST                'self'
              366  STORE_ATTR               tile
          368_370  JUMP_FORWARD        684  'to 684'
            372_0  COME_FROM           264  '264'

 L. 140       372  LOAD_FAST                'header_size'
              374  LOAD_CONST               4
              376  BINARY_ADD       
              378  STORE_FAST               'data_start'

 L. 141       380  LOAD_CONST               0
              382  STORE_FAST               'n'

 L. 142       384  LOAD_FAST                'fourcc'
              386  LOAD_CONST               b'DXT1'
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   408  'to 408'

 L. 143       394  LOAD_STR                 'DXT1'
              396  LOAD_FAST                'self'
              398  STORE_ATTR               pixel_format

 L. 144       400  LOAD_CONST               1
              402  STORE_FAST               'n'
          404_406  JUMP_FORWARD        662  'to 662'
            408_0  COME_FROM           390  '390'

 L. 145       408  LOAD_FAST                'fourcc'
              410  LOAD_CONST               b'DXT3'
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   430  'to 430'

 L. 146       418  LOAD_STR                 'DXT3'
              420  LOAD_FAST                'self'
              422  STORE_ATTR               pixel_format

 L. 147       424  LOAD_CONST               2
              426  STORE_FAST               'n'
              428  JUMP_FORWARD        662  'to 662'
            430_0  COME_FROM           414  '414'

 L. 148       430  LOAD_FAST                'fourcc'
              432  LOAD_CONST               b'DXT5'
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   452  'to 452'

 L. 149       440  LOAD_STR                 'DXT5'
              442  LOAD_FAST                'self'
              444  STORE_ATTR               pixel_format

 L. 150       446  LOAD_CONST               3
              448  STORE_FAST               'n'
              450  JUMP_FORWARD        662  'to 662'
            452_0  COME_FROM           436  '436'

 L. 151       452  LOAD_FAST                'fourcc'
              454  LOAD_CONST               b'DX10'
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   644  'to 644'

 L. 152       462  LOAD_FAST                'data_start'
              464  LOAD_CONST               20
              466  INPLACE_ADD      
              468  STORE_FAST               'data_start'

 L. 154       470  LOAD_GLOBAL              BytesIO
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                fp
              476  LOAD_METHOD              read
              478  LOAD_CONST               20
              480  CALL_METHOD_1         1  ''
              482  CALL_FUNCTION_1       1  ''
              484  STORE_FAST               'dxt10'

 L. 155       486  LOAD_GLOBAL              struct
              488  LOAD_METHOD              unpack
              490  LOAD_STR                 '<II'
              492  LOAD_FAST                'dxt10'
              494  LOAD_METHOD              read
              496  LOAD_CONST               8
              498  CALL_METHOD_1         1  ''
              500  CALL_METHOD_2         2  ''
              502  UNPACK_SEQUENCE_2     2 
              504  STORE_FAST               'dxgi_format'
              506  STORE_FAST               'dimension'

 L. 156       508  LOAD_FAST                'dxgi_format'
              510  LOAD_GLOBAL              DXGI_FORMAT_BC7_TYPELESS
              512  LOAD_GLOBAL              DXGI_FORMAT_BC7_UNORM
              514  BUILD_TUPLE_2         2 
              516  <118>                 0  ''
          518_520  POP_JUMP_IF_FALSE   534  'to 534'

 L. 157       522  LOAD_STR                 'BC7'
              524  LOAD_FAST                'self'
              526  STORE_ATTR               pixel_format

 L. 158       528  LOAD_CONST               7
              530  STORE_FAST               'n'
              532  JUMP_FORWARD        642  'to 642'
            534_0  COME_FROM           518  '518'

 L. 159       534  LOAD_FAST                'dxgi_format'
              536  LOAD_GLOBAL              DXGI_FORMAT_BC7_UNORM_SRGB
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   566  'to 566'

 L. 160       544  LOAD_STR                 'BC7'
              546  LOAD_FAST                'self'
              548  STORE_ATTR               pixel_format

 L. 161       550  LOAD_CONST               0.45454545454545453
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                info
              556  LOAD_STR                 'gamma'
              558  STORE_SUBSCR     

 L. 162       560  LOAD_CONST               7
              562  STORE_FAST               'n'
              564  JUMP_FORWARD        642  'to 642'
            566_0  COME_FROM           540  '540'

 L. 163       566  LOAD_FAST                'dxgi_format'

 L. 164       568  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_TYPELESS

 L. 165       570  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM

 L. 166       572  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM_SRGB

 L. 163       574  BUILD_TUPLE_3         3 
              576  <118>                 0  ''
          578_580  POP_JUMP_IF_FALSE   628  'to 628'

 L. 168       582  LOAD_STR                 'raw'
              584  LOAD_CONST               (0, 0)
              586  LOAD_FAST                'self'
              588  LOAD_ATTR                size
              590  BINARY_ADD       
              592  LOAD_CONST               0
              594  LOAD_CONST               ('RGBA', 0, 1)
              596  BUILD_TUPLE_4         4 
              598  BUILD_LIST_1          1 
              600  LOAD_FAST                'self'
              602  STORE_ATTR               tile

 L. 169       604  LOAD_FAST                'dxgi_format'
              606  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM_SRGB
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   624  'to 624'

 L. 170       614  LOAD_CONST               0.45454545454545453
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                info
              620  LOAD_STR                 'gamma'
              622  STORE_SUBSCR     
            624_0  COME_FROM           610  '610'

 L. 171       624  LOAD_CONST               None
              626  RETURN_VALUE     
            628_0  COME_FROM           578  '578'

 L. 173       628  LOAD_GLOBAL              NotImplementedError

 L. 174       630  LOAD_STR                 'Unimplemented DXGI format '
              632  LOAD_FAST                'dxgi_format'
              634  FORMAT_VALUE          0  ''
              636  BUILD_STRING_2        2 

 L. 173       638  CALL_FUNCTION_1       1  ''
              640  RAISE_VARARGS_1       1  'exception instance'
            642_0  COME_FROM           564  '564'
            642_1  COME_FROM           532  '532'
              642  JUMP_FORWARD        662  'to 662'
            644_0  COME_FROM           458  '458'

 L. 177       644  LOAD_GLOBAL              NotImplementedError
              646  LOAD_STR                 'Unimplemented pixel format '
              648  LOAD_GLOBAL              repr
              650  LOAD_FAST                'fourcc'
              652  CALL_FUNCTION_1       1  ''
              654  FORMAT_VALUE          0  ''
              656  BUILD_STRING_2        2 
              658  CALL_FUNCTION_1       1  ''
              660  RAISE_VARARGS_1       1  'exception instance'
            662_0  COME_FROM           642  '642'
            662_1  COME_FROM           450  '450'
            662_2  COME_FROM           428  '428'
            662_3  COME_FROM           404  '404'

 L. 179       662  LOAD_STR                 'bcn'
              664  LOAD_CONST               (0, 0)
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                size
              670  BINARY_ADD       
              672  LOAD_FAST                'data_start'
              674  LOAD_FAST                'n'
              676  BUILD_TUPLE_4         4 
              678  BUILD_LIST_1          1 
              680  LOAD_FAST                'self'
              682  STORE_ATTR               tile
            684_0  COME_FROM           368  '368'

Parse error at or near `<118>' instruction at offset 516

    def load_seek(self, pos):
        pass


def _validate(prefix):
    return prefix[:4] == b'DDS '


Image.register_open(DdsImageFile.format, DdsImageFile, _validate)
Image.register_extension(DdsImageFile.format, '.dds')