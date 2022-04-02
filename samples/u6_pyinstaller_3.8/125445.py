# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\TgaImagePlugin.py
import warnings
from . import Image, ImageFile, ImagePalette
from ._binary import i8
from ._binary import i16le as i16
from ._binary import o8
from ._binary import o16le as o16
MODES = {(1, 8):'P', 
 (3, 1):'1', 
 (3, 8):'L', 
 (3, 16):'LA', 
 (2, 16):'BGR;5', 
 (2, 24):'BGR', 
 (2, 32):'BGRA'}

class TgaImageFile(ImageFile.ImageFile):
    format = 'TGA'
    format_description = 'Targa'

    def _open--- This code section failed: ---

 L.  57         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               18
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  59        12  LOAD_GLOBAL              i8
               14  LOAD_FAST                's'
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'id_len'

 L.  61        24  LOAD_GLOBAL              i8
               26  LOAD_FAST                's'
               28  LOAD_CONST               1
               30  BINARY_SUBSCR    
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'colormaptype'

 L.  62        36  LOAD_GLOBAL              i8
               38  LOAD_FAST                's'
               40  LOAD_CONST               2
               42  BINARY_SUBSCR    
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'imagetype'

 L.  64        48  LOAD_GLOBAL              i8
               50  LOAD_FAST                's'
               52  LOAD_CONST               16
               54  BINARY_SUBSCR    
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'depth'

 L.  66        60  LOAD_GLOBAL              i8
               62  LOAD_FAST                's'
               64  LOAD_CONST               17
               66  BINARY_SUBSCR    
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'flags'

 L.  68        72  LOAD_GLOBAL              i16
               74  LOAD_FAST                's'
               76  LOAD_CONST               12
               78  LOAD_CONST               None
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  ''
               86  LOAD_GLOBAL              i16
               88  LOAD_FAST                's'
               90  LOAD_CONST               14
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  ''
              100  BUILD_TUPLE_2         2 
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _size

 L.  72       106  LOAD_FAST                'colormaptype'
              108  LOAD_CONST               (0, 1)
              110  COMPARE_OP               not-in

 L.  71       112  POP_JUMP_IF_TRUE    150  'to 150'

 L.  73       114  LOAD_FAST                'self'
              116  LOAD_ATTR                size
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  LOAD_CONST               0
              124  COMPARE_OP               <=

 L.  71       126  POP_JUMP_IF_TRUE    150  'to 150'

 L.  74       128  LOAD_FAST                'self'
              130  LOAD_ATTR                size
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  LOAD_CONST               0
              138  COMPARE_OP               <=

 L.  71       140  POP_JUMP_IF_TRUE    150  'to 150'

 L.  75       142  LOAD_FAST                'depth'
              144  LOAD_CONST               (1, 8, 16, 24, 32)
              146  COMPARE_OP               not-in

 L.  71       148  POP_JUMP_IF_FALSE   158  'to 158'
            150_0  COME_FROM           140  '140'
            150_1  COME_FROM           126  '126'
            150_2  COME_FROM           112  '112'

 L.  77       150  LOAD_GLOBAL              SyntaxError
              152  LOAD_STR                 'not a TGA file'
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           148  '148'

 L.  80       158  LOAD_FAST                'imagetype'
              160  LOAD_CONST               (3, 11)
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   204  'to 204'

 L.  81       166  LOAD_STR                 'L'
              168  LOAD_FAST                'self'
              170  STORE_ATTR               mode

 L.  82       172  LOAD_FAST                'depth'
              174  LOAD_CONST               1
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L.  83       180  LOAD_STR                 '1'
              182  LOAD_FAST                'self'
              184  STORE_ATTR               mode
              186  JUMP_FORWARD        202  'to 202'
            188_0  COME_FROM           178  '178'

 L.  84       188  LOAD_FAST                'depth'
              190  LOAD_CONST               16
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   202  'to 202'

 L.  85       196  LOAD_STR                 'LA'
              198  LOAD_FAST                'self'
              200  STORE_ATTR               mode
            202_0  COME_FROM           194  '194'
            202_1  COME_FROM           186  '186'
              202  JUMP_FORWARD        258  'to 258'
            204_0  COME_FROM           164  '164'

 L.  86       204  LOAD_FAST                'imagetype'
              206  LOAD_CONST               (1, 9)
              208  COMPARE_OP               in
              210  POP_JUMP_IF_FALSE   220  'to 220'

 L.  87       212  LOAD_STR                 'P'
              214  LOAD_FAST                'self'
              216  STORE_ATTR               mode
              218  JUMP_FORWARD        258  'to 258'
            220_0  COME_FROM           210  '210'

 L.  88       220  LOAD_FAST                'imagetype'
              222  LOAD_CONST               (2, 10)
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE   250  'to 250'

 L.  89       228  LOAD_STR                 'RGB'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               mode

 L.  90       234  LOAD_FAST                'depth'
              236  LOAD_CONST               32
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   248  'to 248'

 L.  91       242  LOAD_STR                 'RGBA'
              244  LOAD_FAST                'self'
              246  STORE_ATTR               mode
            248_0  COME_FROM           240  '240'
              248  JUMP_FORWARD        258  'to 258'
            250_0  COME_FROM           226  '226'

 L.  93       250  LOAD_GLOBAL              SyntaxError
              252  LOAD_STR                 'unknown TGA mode'
              254  CALL_FUNCTION_1       1  ''
              256  RAISE_VARARGS_1       1  'exception instance'
            258_0  COME_FROM           248  '248'
            258_1  COME_FROM           218  '218'
            258_2  COME_FROM           202  '202'

 L.  96       258  LOAD_FAST                'flags'
              260  LOAD_CONST               48
              262  BINARY_AND       
              264  STORE_FAST               'orientation'

 L.  97       266  LOAD_FAST                'orientation'
              268  LOAD_CONST               32
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   282  'to 282'

 L.  98       276  LOAD_CONST               1
              278  STORE_FAST               'orientation'
              280  JUMP_FORWARD        302  'to 302'
            282_0  COME_FROM           272  '272'

 L.  99       282  LOAD_FAST                'orientation'
          284_286  POP_JUMP_IF_TRUE    294  'to 294'

 L. 100       288  LOAD_CONST               -1
              290  STORE_FAST               'orientation'
              292  JUMP_FORWARD        302  'to 302'
            294_0  COME_FROM           284  '284'

 L. 102       294  LOAD_GLOBAL              SyntaxError
              296  LOAD_STR                 'unknown TGA orientation'
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  'exception instance'
            302_0  COME_FROM           292  '292'
            302_1  COME_FROM           280  '280'

 L. 104       302  LOAD_FAST                'orientation'
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                info
              308  LOAD_STR                 'orientation'
              310  STORE_SUBSCR     

 L. 106       312  LOAD_FAST                'imagetype'
              314  LOAD_CONST               8
              316  BINARY_AND       
          318_320  POP_JUMP_IF_FALSE   332  'to 332'

 L. 107       322  LOAD_STR                 'tga_rle'
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                info
              328  LOAD_STR                 'compression'
              330  STORE_SUBSCR     
            332_0  COME_FROM           318  '318'

 L. 109       332  LOAD_FAST                'id_len'
          334_336  POP_JUMP_IF_FALSE   356  'to 356'

 L. 110       338  LOAD_FAST                'self'
              340  LOAD_ATTR                fp
              342  LOAD_METHOD              read
              344  LOAD_FAST                'id_len'
              346  CALL_METHOD_1         1  ''
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                info
              352  LOAD_STR                 'id_section'
              354  STORE_SUBSCR     
            356_0  COME_FROM           334  '334'

 L. 112       356  LOAD_FAST                'colormaptype'
          358_360  POP_JUMP_IF_FALSE   550  'to 550'

 L. 114       362  LOAD_GLOBAL              i16
              364  LOAD_FAST                's'
              366  LOAD_CONST               3
              368  LOAD_CONST               None
              370  BUILD_SLICE_2         2 
              372  BINARY_SUBSCR    
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_GLOBAL              i16
              378  LOAD_FAST                's'
              380  LOAD_CONST               5
              382  LOAD_CONST               None
              384  BUILD_SLICE_2         2 
              386  BINARY_SUBSCR    
              388  CALL_FUNCTION_1       1  ''
              390  LOAD_GLOBAL              i16
              392  LOAD_FAST                's'
              394  LOAD_CONST               7
              396  LOAD_CONST               None
              398  BUILD_SLICE_2         2 
              400  BINARY_SUBSCR    
              402  CALL_FUNCTION_1       1  ''
              404  ROT_THREE        
              406  ROT_TWO          
              408  STORE_FAST               'start'
              410  STORE_FAST               'size'
              412  STORE_FAST               'mapdepth'

 L. 115       414  LOAD_FAST                'mapdepth'
              416  LOAD_CONST               16
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   460  'to 460'

 L. 116       424  LOAD_GLOBAL              ImagePalette
              426  LOAD_METHOD              raw

 L. 117       428  LOAD_STR                 'BGR;16'

 L. 117       430  LOAD_CONST               b'\x00\x00'
              432  LOAD_FAST                'start'
              434  BINARY_MULTIPLY  
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                fp
              440  LOAD_METHOD              read
              442  LOAD_CONST               2
              444  LOAD_FAST                'size'
              446  BINARY_MULTIPLY  
              448  CALL_METHOD_1         1  ''
              450  BINARY_ADD       

 L. 116       452  CALL_METHOD_2         2  ''
              454  LOAD_FAST                'self'
              456  STORE_ATTR               palette
              458  JUMP_FORWARD        550  'to 550'
            460_0  COME_FROM           420  '420'

 L. 119       460  LOAD_FAST                'mapdepth'
              462  LOAD_CONST               24
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   506  'to 506'

 L. 120       470  LOAD_GLOBAL              ImagePalette
              472  LOAD_METHOD              raw

 L. 121       474  LOAD_STR                 'BGR'

 L. 121       476  LOAD_CONST               b'\x00\x00\x00'
              478  LOAD_FAST                'start'
              480  BINARY_MULTIPLY  
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                fp
              486  LOAD_METHOD              read
              488  LOAD_CONST               3
              490  LOAD_FAST                'size'
              492  BINARY_MULTIPLY  
              494  CALL_METHOD_1         1  ''
              496  BINARY_ADD       

 L. 120       498  CALL_METHOD_2         2  ''
              500  LOAD_FAST                'self'
              502  STORE_ATTR               palette
              504  JUMP_FORWARD        550  'to 550'
            506_0  COME_FROM           466  '466'

 L. 123       506  LOAD_FAST                'mapdepth'
              508  LOAD_CONST               32
              510  COMPARE_OP               ==
          512_514  POP_JUMP_IF_FALSE   550  'to 550'

 L. 124       516  LOAD_GLOBAL              ImagePalette
              518  LOAD_METHOD              raw

 L. 125       520  LOAD_STR                 'BGRA'

 L. 125       522  LOAD_CONST               b'\x00\x00\x00\x00'
              524  LOAD_FAST                'start'
              526  BINARY_MULTIPLY  
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                fp
              532  LOAD_METHOD              read
              534  LOAD_CONST               4
              536  LOAD_FAST                'size'
              538  BINARY_MULTIPLY  
              540  CALL_METHOD_1         1  ''
              542  BINARY_ADD       

 L. 124       544  CALL_METHOD_2         2  ''
              546  LOAD_FAST                'self'
              548  STORE_ATTR               palette
            550_0  COME_FROM           512  '512'
            550_1  COME_FROM           504  '504'
            550_2  COME_FROM           458  '458'
            550_3  COME_FROM           358  '358'

 L. 129       550  SETUP_FINALLY       652  'to 652'

 L. 130       552  LOAD_GLOBAL              MODES
              554  LOAD_FAST                'imagetype'
              556  LOAD_CONST               7
              558  BINARY_AND       
              560  LOAD_FAST                'depth'
              562  BUILD_TUPLE_2         2 
              564  BINARY_SUBSCR    
              566  STORE_FAST               'rawmode'

 L. 131       568  LOAD_FAST                'imagetype'
              570  LOAD_CONST               8
              572  BINARY_AND       
          574_576  POP_JUMP_IF_FALSE   614  'to 614'

 L. 135       578  LOAD_STR                 'tga_rle'

 L. 136       580  LOAD_CONST               (0, 0)
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                size
              586  BINARY_ADD       

 L. 137       588  LOAD_FAST                'self'
              590  LOAD_ATTR                fp
              592  LOAD_METHOD              tell
              594  CALL_METHOD_0         0  ''

 L. 138       596  LOAD_FAST                'rawmode'
              598  LOAD_FAST                'orientation'
              600  LOAD_FAST                'depth'
              602  BUILD_TUPLE_3         3 

 L. 134       604  BUILD_TUPLE_4         4 

 L. 133       606  BUILD_LIST_1          1 
              608  LOAD_FAST                'self'
              610  STORE_ATTR               tile
              612  JUMP_FORWARD        648  'to 648'
            614_0  COME_FROM           574  '574'

 L. 144       614  LOAD_STR                 'raw'

 L. 145       616  LOAD_CONST               (0, 0)
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                size
              622  BINARY_ADD       

 L. 146       624  LOAD_FAST                'self'
              626  LOAD_ATTR                fp
              628  LOAD_METHOD              tell
              630  CALL_METHOD_0         0  ''

 L. 147       632  LOAD_FAST                'rawmode'
              634  LOAD_CONST               0
              636  LOAD_FAST                'orientation'
              638  BUILD_TUPLE_3         3 

 L. 143       640  BUILD_TUPLE_4         4 

 L. 142       642  BUILD_LIST_1          1 
              644  LOAD_FAST                'self'
              646  STORE_ATTR               tile
            648_0  COME_FROM           612  '612'
              648  POP_BLOCK        
              650  JUMP_FORWARD        674  'to 674'
            652_0  COME_FROM_FINALLY   550  '550'

 L. 150       652  DUP_TOP          
              654  LOAD_GLOBAL              KeyError
              656  COMPARE_OP               exception-match
          658_660  POP_JUMP_IF_FALSE   672  'to 672'
              662  POP_TOP          
              664  POP_TOP          
              666  POP_TOP          

 L. 151       668  POP_EXCEPT       
              670  JUMP_FORWARD        674  'to 674'
            672_0  COME_FROM           658  '658'
              672  END_FINALLY      
            674_0  COME_FROM           670  '670'
            674_1  COME_FROM           650  '650'

Parse error at or near `COME_FROM' instruction at offset 674_0


SAVE = {'1':('1', 1, 0, 3), 
 'L':('L', 8, 0, 3), 
 'LA':('LA', 16, 0, 3), 
 'P':('P', 8, 1, 1), 
 'RGB':('BGR', 24, 0, 2), 
 'RGBA':('BGRA', 32, 0, 2)}

def _save(im, fp, filename):
    try:
        rawmode, bits, colormaptype, imagetype = SAVE[im.mode]
    except KeyError as e:
        try:
            raise OSError(f"cannot write mode {im.mode} as TGA") from e
        finally:
            e = None
            del e

    else:
        if 'rle' in im.encoderinfo:
            rle = im.encoderinfo['rle']
        else:
            compression = im.encoderinfo.get('compression', im.info.get'compression')
            rle = compression == 'tga_rle'
        if rle:
            imagetype += 8
        else:
            id_section = im.encoderinfo.get('id_section', im.info.get('id_section', ''))
            id_len = len(id_section)
            if id_len > 255:
                id_len = 255
                id_section = id_section[:255]
                warnings.warn'id_section has been trimmed to 255 characters'
            else:
                if colormaptype:
                    colormapfirst, colormaplength, colormapentry = (0, 256, 24)
                else:
                    colormapfirst, colormaplength, colormapentry = (0, 0, 0)
                if im.mode in ('LA', 'RGBA'):
                    flags = 8
                else:
                    flags = 0
            orientation = im.encoderinfo.get('orientation', im.info.get('orientation', -1))
            if orientation > 0:
                flags = flags | 32
            fp.write(o8(id_len) + o8(colormaptype) + o8(imagetype) + o16(colormapfirst) + o16(colormaplength) + o8(colormapentry) + o16(0) + o16(0) + o16(im.size[0]) + o16(im.size[1]) + o8(bits) + o8(flags))
            if id_section:
                fp.writeid_section
            if colormaptype:
                fp.writeim.im.getpalette('RGB', 'BGR')
            if rle:
                ImageFile._save(im, fp, [('tga_rle', (0, 0) + im.size, 0, (rawmode, orientation))])
            else:
                ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, orientation))])
        fp.writeb'\x00\x00\x00\x00\x00\x00\x00\x00TRUEVISION-XFILE.\x00'


Image.register_open(TgaImageFile.format, TgaImageFile)
Image.register_save(TgaImageFile.format, _save)
Image.register_extensions(TgaImageFile.format, ['.tga', '.icb', '.vda', '.vst'])
Image.register_mime(TgaImageFile.format, 'image/x-tga')