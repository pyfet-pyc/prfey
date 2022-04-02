# uncompyle6 version 3.7.4
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
from ._binary import o32le as o32
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
DXGI_FORMAT_BC5_TYPELESS = 82
DXGI_FORMAT_BC5_UNORM = 83
DXGI_FORMAT_BC5_SNORM = 84
DXGI_FORMAT_BC7_TYPELESS = 97
DXGI_FORMAT_BC7_UNORM = 98
DXGI_FORMAT_BC7_UNORM_SRGB = 99

class DdsImageFile(ImageFile.ImageFile):
    format = 'DDS'
    format_description = 'DirectDraw Surface'

    def _open--- This code section failed: ---

 L. 114         0  LOAD_GLOBAL              struct
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

 L. 115        24  LOAD_FAST                'header_size'
               26  LOAD_CONST               124
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    50  'to 50'

 L. 116        32  LOAD_GLOBAL              OSError
               34  LOAD_STR                 'Unsupported header size '
               36  LOAD_GLOBAL              repr
               38  LOAD_FAST                'header_size'
               40  CALL_FUNCTION_1       1  ''
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_2        2 
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            30  '30'

 L. 117        50  LOAD_FAST                'self'
               52  LOAD_ATTR                fp
               54  LOAD_METHOD              read
               56  LOAD_FAST                'header_size'
               58  LOAD_CONST               4
               60  BINARY_SUBTRACT  
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'header_bytes'

 L. 118        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'header_bytes'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               120
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    98  'to 98'

 L. 119        78  LOAD_GLOBAL              OSError
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

 L. 120        98  LOAD_GLOBAL              BytesIO
              100  LOAD_FAST                'header_bytes'
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'header'

 L. 122       106  LOAD_GLOBAL              struct
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

 L. 123       130  LOAD_FAST                'width'
              132  LOAD_FAST                'height'
              134  BUILD_TUPLE_2         2 
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _size

 L. 124       140  LOAD_STR                 'RGBA'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               mode

 L. 126       146  LOAD_GLOBAL              struct
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

 L. 127       170  LOAD_GLOBAL              struct
              172  LOAD_METHOD              unpack
              174  LOAD_STR                 '<11I'
              176  LOAD_FAST                'header'
              178  LOAD_METHOD              read
              180  LOAD_CONST               44
              182  CALL_METHOD_1         1  ''
              184  CALL_METHOD_2         2  ''
              186  POP_TOP          

 L. 130       188  LOAD_GLOBAL              struct
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

 L. 131       210  LOAD_FAST                'header'
              212  LOAD_METHOD              read
              214  LOAD_CONST               4
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'fourcc'

 L. 132       220  LOAD_GLOBAL              struct
              222  LOAD_METHOD              unpack
              224  LOAD_STR                 '<I'
              226  LOAD_FAST                'header'
              228  LOAD_METHOD              read
              230  LOAD_CONST               4
              232  CALL_METHOD_1         1  ''
              234  CALL_METHOD_2         2  ''
              236  UNPACK_SEQUENCE_1     1 
              238  STORE_FAST               'bitcount'

 L. 133       240  LOAD_GLOBAL              struct
              242  LOAD_METHOD              unpack
              244  LOAD_STR                 '<4I'
              246  LOAD_FAST                'header'
              248  LOAD_METHOD              read
              250  LOAD_CONST               16
              252  CALL_METHOD_1         1  ''
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'masks'

 L. 134       258  LOAD_FAST                'pfflags'
              260  LOAD_GLOBAL              DDPF_RGB
              262  BINARY_AND       
          264_266  POP_JUMP_IF_FALSE   390  'to 390'

 L. 136       268  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              270  LOAD_STR                 'DdsImageFile._open.<locals>.<dictcomp>'
              272  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              274  LOAD_GLOBAL              enumerate
              276  LOAD_FAST                'masks'
              278  CALL_FUNCTION_1       1  ''
              280  GET_ITER         
              282  CALL_FUNCTION_1       1  ''
              284  STORE_FAST               'masks'

 L. 137       286  LOAD_STR                 ''
              288  STORE_FAST               'rawmode'

 L. 138       290  LOAD_FAST                'bitcount'
              292  LOAD_CONST               32
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   314  'to 314'

 L. 139       300  LOAD_FAST                'rawmode'
              302  LOAD_FAST                'masks'
              304  LOAD_CONST               4278190080
              306  BINARY_SUBSCR    
              308  INPLACE_ADD      
              310  STORE_FAST               'rawmode'
              312  JUMP_FORWARD        320  'to 320'
            314_0  COME_FROM           296  '296'

 L. 141       314  LOAD_STR                 'RGB'
              316  LOAD_FAST                'self'
              318  STORE_ATTR               mode
            320_0  COME_FROM           312  '312'

 L. 142       320  LOAD_FAST                'rawmode'
              322  LOAD_FAST                'masks'
              324  LOAD_CONST               16711680
              326  BINARY_SUBSCR    
              328  LOAD_FAST                'masks'
              330  LOAD_CONST               65280
              332  BINARY_SUBSCR    
              334  BINARY_ADD       
              336  LOAD_FAST                'masks'
              338  LOAD_CONST               255
              340  BINARY_SUBSCR    
              342  BINARY_ADD       
              344  INPLACE_ADD      
              346  STORE_FAST               'rawmode'

 L. 144       348  LOAD_STR                 'raw'
              350  LOAD_CONST               (0, 0)
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                size
              356  BINARY_ADD       
              358  LOAD_CONST               0
              360  LOAD_FAST                'rawmode'
              362  LOAD_CONST               None
              364  LOAD_CONST               None
              366  LOAD_CONST               -1
              368  BUILD_SLICE_3         3 
              370  BINARY_SUBSCR    
              372  LOAD_CONST               0
              374  LOAD_CONST               1
              376  BUILD_TUPLE_3         3 
              378  BUILD_TUPLE_4         4 
              380  BUILD_LIST_1          1 
              382  LOAD_FAST                'self'
              384  STORE_ATTR               tile
          386_388  JUMP_FORWARD        798  'to 798'
            390_0  COME_FROM           264  '264'

 L. 146       390  LOAD_FAST                'header_size'
              392  LOAD_CONST               4
              394  BINARY_ADD       
              396  STORE_FAST               'data_start'

 L. 147       398  LOAD_CONST               0
              400  STORE_FAST               'n'

 L. 148       402  LOAD_FAST                'fourcc'
              404  LOAD_CONST               b'DXT1'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   426  'to 426'

 L. 149       412  LOAD_STR                 'DXT1'
              414  LOAD_FAST                'self'
              416  STORE_ATTR               pixel_format

 L. 150       418  LOAD_CONST               1
              420  STORE_FAST               'n'
          422_424  JUMP_FORWARD        770  'to 770'
            426_0  COME_FROM           408  '408'

 L. 151       426  LOAD_FAST                'fourcc'
              428  LOAD_CONST               b'DXT3'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   450  'to 450'

 L. 152       436  LOAD_STR                 'DXT3'
              438  LOAD_FAST                'self'
              440  STORE_ATTR               pixel_format

 L. 153       442  LOAD_CONST               2
              444  STORE_FAST               'n'
          446_448  JUMP_FORWARD        770  'to 770'
            450_0  COME_FROM           432  '432'

 L. 154       450  LOAD_FAST                'fourcc'
              452  LOAD_CONST               b'DXT5'
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   474  'to 474'

 L. 155       460  LOAD_STR                 'DXT5'
              462  LOAD_FAST                'self'
              464  STORE_ATTR               pixel_format

 L. 156       466  LOAD_CONST               3
              468  STORE_FAST               'n'
          470_472  JUMP_FORWARD        770  'to 770'
            474_0  COME_FROM           456  '456'

 L. 157       474  LOAD_FAST                'fourcc'
              476  LOAD_CONST               b'BC5S'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   504  'to 504'

 L. 158       484  LOAD_STR                 'BC5S'
              486  LOAD_FAST                'self'
              488  STORE_ATTR               pixel_format

 L. 159       490  LOAD_CONST               5
              492  STORE_FAST               'n'

 L. 160       494  LOAD_STR                 'RGB'
              496  LOAD_FAST                'self'
              498  STORE_ATTR               mode
          500_502  JUMP_FORWARD        770  'to 770'
            504_0  COME_FROM           480  '480'

 L. 161       504  LOAD_FAST                'fourcc'
              506  LOAD_CONST               b'DX10'
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   752  'to 752'

 L. 162       514  LOAD_FAST                'data_start'
              516  LOAD_CONST               20
              518  INPLACE_ADD      
              520  STORE_FAST               'data_start'

 L. 164       522  LOAD_GLOBAL              struct
              524  LOAD_METHOD              unpack
              526  LOAD_STR                 '<I'
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                fp
              532  LOAD_METHOD              read
              534  LOAD_CONST               4
              536  CALL_METHOD_1         1  ''
              538  CALL_METHOD_2         2  ''
              540  UNPACK_SEQUENCE_1     1 
              542  STORE_FAST               'dxgi_format'

 L. 165       544  LOAD_FAST                'self'
              546  LOAD_ATTR                fp
              548  LOAD_METHOD              read
              550  LOAD_CONST               16
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          

 L. 166       556  LOAD_FAST                'dxgi_format'
              558  LOAD_GLOBAL              DXGI_FORMAT_BC5_TYPELESS
              560  LOAD_GLOBAL              DXGI_FORMAT_BC5_UNORM
              562  BUILD_TUPLE_2         2 
              564  <118>                 0  ''
          566_568  POP_JUMP_IF_FALSE   588  'to 588'

 L. 167       570  LOAD_STR                 'BC5'
              572  LOAD_FAST                'self'
              574  STORE_ATTR               pixel_format

 L. 168       576  LOAD_CONST               5
              578  STORE_FAST               'n'

 L. 169       580  LOAD_STR                 'RGB'
              582  LOAD_FAST                'self'
              584  STORE_ATTR               mode
              586  JUMP_FORWARD        750  'to 750'
            588_0  COME_FROM           566  '566'

 L. 170       588  LOAD_FAST                'dxgi_format'
              590  LOAD_GLOBAL              DXGI_FORMAT_BC5_SNORM
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   616  'to 616'

 L. 171       598  LOAD_STR                 'BC5S'
              600  LOAD_FAST                'self'
              602  STORE_ATTR               pixel_format

 L. 172       604  LOAD_CONST               5
              606  STORE_FAST               'n'

 L. 173       608  LOAD_STR                 'RGB'
              610  LOAD_FAST                'self'
              612  STORE_ATTR               mode
              614  JUMP_FORWARD        750  'to 750'
            616_0  COME_FROM           594  '594'

 L. 174       616  LOAD_FAST                'dxgi_format'
              618  LOAD_GLOBAL              DXGI_FORMAT_BC7_TYPELESS
              620  LOAD_GLOBAL              DXGI_FORMAT_BC7_UNORM
              622  BUILD_TUPLE_2         2 
              624  <118>                 0  ''
          626_628  POP_JUMP_IF_FALSE   642  'to 642'

 L. 175       630  LOAD_STR                 'BC7'
              632  LOAD_FAST                'self'
              634  STORE_ATTR               pixel_format

 L. 176       636  LOAD_CONST               7
              638  STORE_FAST               'n'
              640  JUMP_FORWARD        750  'to 750'
            642_0  COME_FROM           626  '626'

 L. 177       642  LOAD_FAST                'dxgi_format'
              644  LOAD_GLOBAL              DXGI_FORMAT_BC7_UNORM_SRGB
              646  COMPARE_OP               ==
          648_650  POP_JUMP_IF_FALSE   674  'to 674'

 L. 178       652  LOAD_STR                 'BC7'
              654  LOAD_FAST                'self'
              656  STORE_ATTR               pixel_format

 L. 179       658  LOAD_CONST               0.45454545454545453
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                info
              664  LOAD_STR                 'gamma'
              666  STORE_SUBSCR     

 L. 180       668  LOAD_CONST               7
              670  STORE_FAST               'n'
              672  JUMP_FORWARD        750  'to 750'
            674_0  COME_FROM           648  '648'

 L. 181       674  LOAD_FAST                'dxgi_format'

 L. 182       676  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_TYPELESS

 L. 183       678  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM

 L. 184       680  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM_SRGB

 L. 181       682  BUILD_TUPLE_3         3 
              684  <118>                 0  ''
          686_688  POP_JUMP_IF_FALSE   736  'to 736'

 L. 186       690  LOAD_STR                 'raw'
              692  LOAD_CONST               (0, 0)
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                size
              698  BINARY_ADD       
              700  LOAD_CONST               0
              702  LOAD_CONST               ('RGBA', 0, 1)
              704  BUILD_TUPLE_4         4 
              706  BUILD_LIST_1          1 
              708  LOAD_FAST                'self'
              710  STORE_ATTR               tile

 L. 187       712  LOAD_FAST                'dxgi_format'
              714  LOAD_GLOBAL              DXGI_FORMAT_R8G8B8A8_UNORM_SRGB
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   732  'to 732'

 L. 188       722  LOAD_CONST               0.45454545454545453
              724  LOAD_FAST                'self'
              726  LOAD_ATTR                info
              728  LOAD_STR                 'gamma'
              730  STORE_SUBSCR     
            732_0  COME_FROM           718  '718'

 L. 189       732  LOAD_CONST               None
              734  RETURN_VALUE     
            736_0  COME_FROM           686  '686'

 L. 191       736  LOAD_GLOBAL              NotImplementedError

 L. 192       738  LOAD_STR                 'Unimplemented DXGI format '
              740  LOAD_FAST                'dxgi_format'
              742  FORMAT_VALUE          0  ''
              744  BUILD_STRING_2        2 

 L. 191       746  CALL_FUNCTION_1       1  ''
              748  RAISE_VARARGS_1       1  'exception instance'
            750_0  COME_FROM           672  '672'
            750_1  COME_FROM           640  '640'
            750_2  COME_FROM           614  '614'
            750_3  COME_FROM           586  '586'
              750  JUMP_FORWARD        770  'to 770'
            752_0  COME_FROM           510  '510'

 L. 195       752  LOAD_GLOBAL              NotImplementedError
              754  LOAD_STR                 'Unimplemented pixel format '
              756  LOAD_GLOBAL              repr
              758  LOAD_FAST                'fourcc'
              760  CALL_FUNCTION_1       1  ''
              762  FORMAT_VALUE          0  ''
              764  BUILD_STRING_2        2 
              766  CALL_FUNCTION_1       1  ''
              768  RAISE_VARARGS_1       1  'exception instance'
            770_0  COME_FROM           750  '750'
            770_1  COME_FROM           500  '500'
            770_2  COME_FROM           470  '470'
            770_3  COME_FROM           446  '446'
            770_4  COME_FROM           422  '422'

 L. 198       770  LOAD_STR                 'bcn'
              772  LOAD_CONST               (0, 0)
              774  LOAD_FAST                'self'
              776  LOAD_ATTR                size
              778  BINARY_ADD       
              780  LOAD_FAST                'data_start'
              782  LOAD_FAST                'n'
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                pixel_format
              788  BUILD_TUPLE_2         2 
              790  BUILD_TUPLE_4         4 

 L. 197       792  BUILD_LIST_1          1 
              794  LOAD_FAST                'self'
              796  STORE_ATTR               tile
            798_0  COME_FROM           386  '386'

Parse error at or near `<118>' instruction at offset 564

    def load_seek(self, pos):
        pass


def _save--- This code section failed: ---

 L. 206         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  LOAD_CONST               ('RGB', 'RGBA')
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 207        10  LOAD_GLOBAL              OSError
               12  LOAD_STR                 'cannot write mode '
               14  LOAD_FAST                'im'
               16  LOAD_ATTR                mode
               18  FORMAT_VALUE          0  ''
               20  LOAD_STR                 ' as DDS'
               22  BUILD_STRING_3        3 
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM             8  '8'

 L. 209        28  LOAD_FAST                'fp'
               30  LOAD_METHOD              write

 L. 210        32  LOAD_GLOBAL              o32
               34  LOAD_GLOBAL              DDS_MAGIC
               36  CALL_FUNCTION_1       1  ''

 L. 211        38  LOAD_GLOBAL              o32
               40  LOAD_CONST               124
               42  CALL_FUNCTION_1       1  ''

 L. 210        44  BINARY_ADD       

 L. 212        46  LOAD_GLOBAL              o32

 L. 213        48  LOAD_GLOBAL              DDSD_CAPS
               50  LOAD_GLOBAL              DDSD_HEIGHT
               52  BINARY_OR        
               54  LOAD_GLOBAL              DDSD_WIDTH
               56  BINARY_OR        
               58  LOAD_GLOBAL              DDSD_PITCH
               60  BINARY_OR        
               62  LOAD_GLOBAL              DDSD_PIXELFORMAT
               64  BINARY_OR        

 L. 212        66  CALL_FUNCTION_1       1  ''

 L. 210        68  BINARY_ADD       

 L. 215        70  LOAD_GLOBAL              o32
               72  LOAD_FAST                'im'
               74  LOAD_ATTR                height
               76  CALL_FUNCTION_1       1  ''

 L. 210        78  BINARY_ADD       

 L. 216        80  LOAD_GLOBAL              o32
               82  LOAD_FAST                'im'
               84  LOAD_ATTR                width
               86  CALL_FUNCTION_1       1  ''

 L. 210        88  BINARY_ADD       

 L. 217        90  LOAD_GLOBAL              o32
               92  LOAD_FAST                'im'
               94  LOAD_ATTR                width
               96  LOAD_FAST                'im'
               98  LOAD_ATTR                mode
              100  LOAD_STR                 'RGBA'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   110  'to 110'
              106  LOAD_CONST               32
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM           104  '104'
              110  LOAD_CONST               24
            112_0  COME_FROM           108  '108'
              112  BINARY_MULTIPLY  
              114  LOAD_CONST               7
              116  BINARY_ADD       
              118  LOAD_CONST               8
              120  BINARY_FLOOR_DIVIDE
              122  CALL_FUNCTION_1       1  ''

 L. 210       124  BINARY_ADD       

 L. 218       126  LOAD_GLOBAL              o32
              128  LOAD_CONST               0
              130  CALL_FUNCTION_1       1  ''

 L. 210       132  BINARY_ADD       

 L. 219       134  LOAD_GLOBAL              o32
              136  LOAD_CONST               0
              138  CALL_FUNCTION_1       1  ''

 L. 210       140  BINARY_ADD       

 L. 220       142  LOAD_GLOBAL              o32
              144  LOAD_CONST               0
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               11
              150  BINARY_MULTIPLY  

 L. 210       152  BINARY_ADD       

 L. 221       154  LOAD_GLOBAL              o32
              156  LOAD_CONST               32
              158  CALL_FUNCTION_1       1  ''

 L. 210       160  BINARY_ADD       

 L. 222       162  LOAD_GLOBAL              o32
              164  LOAD_FAST                'im'
              166  LOAD_ATTR                mode
              168  LOAD_STR                 'RGBA'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   178  'to 178'
              174  LOAD_GLOBAL              DDS_RGBA
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           172  '172'
              178  LOAD_GLOBAL              DDPF_RGB
            180_0  COME_FROM           176  '176'
              180  CALL_FUNCTION_1       1  ''

 L. 210       182  BINARY_ADD       

 L. 223       184  LOAD_GLOBAL              o32
              186  LOAD_CONST               0
              188  CALL_FUNCTION_1       1  ''

 L. 210       190  BINARY_ADD       

 L. 224       192  LOAD_GLOBAL              o32
              194  LOAD_FAST                'im'
              196  LOAD_ATTR                mode
              198  LOAD_STR                 'RGBA'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   208  'to 208'
              204  LOAD_CONST               32
              206  JUMP_FORWARD        210  'to 210'
            208_0  COME_FROM           202  '202'
              208  LOAD_CONST               24
            210_0  COME_FROM           206  '206'
              210  CALL_FUNCTION_1       1  ''

 L. 210       212  BINARY_ADD       

 L. 225       214  LOAD_GLOBAL              o32
              216  LOAD_CONST               16711680
              218  CALL_FUNCTION_1       1  ''

 L. 210       220  BINARY_ADD       

 L. 226       222  LOAD_GLOBAL              o32
              224  LOAD_CONST               65280
              226  CALL_FUNCTION_1       1  ''

 L. 210       228  BINARY_ADD       

 L. 227       230  LOAD_GLOBAL              o32
              232  LOAD_CONST               255
              234  CALL_FUNCTION_1       1  ''

 L. 210       236  BINARY_ADD       

 L. 228       238  LOAD_GLOBAL              o32
              240  LOAD_FAST                'im'
              242  LOAD_ATTR                mode
              244  LOAD_STR                 'RGBA'
              246  COMPARE_OP               ==
              248  POP_JUMP_IF_FALSE   254  'to 254'
              250  LOAD_CONST               4278190080
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           248  '248'
              254  LOAD_CONST               0
            256_0  COME_FROM           252  '252'
              256  CALL_FUNCTION_1       1  ''

 L. 210       258  BINARY_ADD       

 L. 229       260  LOAD_GLOBAL              o32
              262  LOAD_GLOBAL              DDSCAPS_TEXTURE
              264  CALL_FUNCTION_1       1  ''

 L. 210       266  BINARY_ADD       

 L. 230       268  LOAD_GLOBAL              o32
              270  LOAD_CONST               0
              272  CALL_FUNCTION_1       1  ''

 L. 210       274  BINARY_ADD       

 L. 231       276  LOAD_GLOBAL              o32
              278  LOAD_CONST               0
              280  CALL_FUNCTION_1       1  ''

 L. 210       282  BINARY_ADD       

 L. 232       284  LOAD_GLOBAL              o32
              286  LOAD_CONST               0
              288  CALL_FUNCTION_1       1  ''

 L. 210       290  BINARY_ADD       

 L. 233       292  LOAD_GLOBAL              o32
              294  LOAD_CONST               0
              296  CALL_FUNCTION_1       1  ''

 L. 210       298  BINARY_ADD       

 L. 209       300  CALL_METHOD_1         1  ''
              302  POP_TOP          

 L. 235       304  LOAD_FAST                'im'
              306  LOAD_ATTR                mode
              308  LOAD_STR                 'RGBA'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   352  'to 352'

 L. 236       316  LOAD_FAST                'im'
              318  LOAD_METHOD              split
              320  CALL_METHOD_0         0  ''
              322  UNPACK_SEQUENCE_4     4 
              324  STORE_FAST               'r'
              326  STORE_FAST               'g'
              328  STORE_FAST               'b'
              330  STORE_FAST               'a'

 L. 237       332  LOAD_GLOBAL              Image
              334  LOAD_METHOD              merge
              336  LOAD_STR                 'RGBA'
              338  LOAD_FAST                'a'
              340  LOAD_FAST                'r'
              342  LOAD_FAST                'g'
              344  LOAD_FAST                'b'
              346  BUILD_TUPLE_4         4 
              348  CALL_METHOD_2         2  ''
              350  STORE_FAST               'im'
            352_0  COME_FROM           312  '312'

 L. 238       352  LOAD_GLOBAL              ImageFile
              354  LOAD_METHOD              _save
              356  LOAD_FAST                'im'
              358  LOAD_FAST                'fp'
              360  LOAD_STR                 'raw'
              362  LOAD_CONST               (0, 0)
              364  LOAD_FAST                'im'
              366  LOAD_ATTR                size
              368  BINARY_ADD       
              370  LOAD_CONST               0
              372  LOAD_FAST                'im'
              374  LOAD_ATTR                mode
              376  LOAD_CONST               None
              378  LOAD_CONST               None
              380  LOAD_CONST               -1
              382  BUILD_SLICE_3         3 
              384  BINARY_SUBSCR    
              386  LOAD_CONST               0
              388  LOAD_CONST               1
              390  BUILD_TUPLE_3         3 
              392  BUILD_TUPLE_4         4 
              394  BUILD_LIST_1          1 
              396  CALL_METHOD_3         3  ''
              398  POP_TOP          

Parse error at or near `None' instruction at offset -1


def _accept(prefix):
    return prefix[:4] == b'DDS '


Image.register_open(DdsImageFile.format, DdsImageFile, _accept)
Image.register_save(DdsImageFile.format, _save)
Image.register_extension(DdsImageFile.format, '.dds')