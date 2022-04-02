# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\TgaImagePlugin.py
import warnings
from . import Image, ImageFile, ImagePalette
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

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               18
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               's'

 L.  58        12  LOAD_FAST                's'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'id_len'

 L.  60        20  LOAD_FAST                's'
               22  LOAD_CONST               1
               24  BINARY_SUBSCR    
               26  STORE_FAST               'colormaptype'

 L.  61        28  LOAD_FAST                's'
               30  LOAD_CONST               2
               32  BINARY_SUBSCR    
               34  STORE_FAST               'imagetype'

 L.  63        36  LOAD_FAST                's'
               38  LOAD_CONST               16
               40  BINARY_SUBSCR    
               42  STORE_FAST               'depth'

 L.  65        44  LOAD_FAST                's'
               46  LOAD_CONST               17
               48  BINARY_SUBSCR    
               50  STORE_FAST               'flags'

 L.  67        52  LOAD_GLOBAL              i16
               54  LOAD_FAST                's'
               56  LOAD_CONST               12
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  LOAD_GLOBAL              i16
               62  LOAD_FAST                's'
               64  LOAD_CONST               14
               66  CALL_FUNCTION_2       2  '2 positional arguments'
               68  BUILD_TUPLE_2         2 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _size

 L.  71        74  LOAD_FAST                'colormaptype'
               76  LOAD_CONST               (0, 1)
               78  COMPARE_OP               not-in
               80  POP_JUMP_IF_TRUE    118  'to 118'

 L.  72        82  LOAD_FAST                'self'
               84  LOAD_ATTR                size
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  LOAD_CONST               0
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_TRUE    118  'to 118'

 L.  73        96  LOAD_FAST                'self'
               98  LOAD_ATTR                size
              100  LOAD_CONST               1
              102  BINARY_SUBSCR    
              104  LOAD_CONST               0
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_TRUE    118  'to 118'

 L.  74       110  LOAD_FAST                'depth'
              112  LOAD_CONST               (1, 8, 16, 24, 32)
              114  COMPARE_OP               not-in
              116  POP_JUMP_IF_FALSE   126  'to 126'
            118_0  COME_FROM           108  '108'
            118_1  COME_FROM            94  '94'
            118_2  COME_FROM            80  '80'

 L.  76       118  LOAD_GLOBAL              SyntaxError
              120  LOAD_STR                 'not a TGA file'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           116  '116'

 L.  79       126  LOAD_FAST                'imagetype'
              128  LOAD_CONST               (3, 11)
              130  COMPARE_OP               in
              132  POP_JUMP_IF_FALSE   172  'to 172'

 L.  80       134  LOAD_STR                 'L'
              136  LOAD_FAST                'self'
              138  STORE_ATTR               mode

 L.  81       140  LOAD_FAST                'depth'
              142  LOAD_CONST               1
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L.  82       148  LOAD_STR                 '1'
              150  LOAD_FAST                'self'
              152  STORE_ATTR               mode
              154  JUMP_ABSOLUTE       226  'to 226'
            156_0  COME_FROM           146  '146'

 L.  83       156  LOAD_FAST                'depth'
              158  LOAD_CONST               16
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   226  'to 226'

 L.  84       164  LOAD_STR                 'LA'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               mode
              170  JUMP_FORWARD        226  'to 226'
            172_0  COME_FROM           132  '132'

 L.  85       172  LOAD_FAST                'imagetype'
              174  LOAD_CONST               (1, 9)
              176  COMPARE_OP               in
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L.  86       180  LOAD_STR                 'P'
              182  LOAD_FAST                'self'
              184  STORE_ATTR               mode
              186  JUMP_FORWARD        226  'to 226'
            188_0  COME_FROM           178  '178'

 L.  87       188  LOAD_FAST                'imagetype'
              190  LOAD_CONST               (2, 10)
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   218  'to 218'

 L.  88       196  LOAD_STR                 'RGB'
              198  LOAD_FAST                'self'
              200  STORE_ATTR               mode

 L.  89       202  LOAD_FAST                'depth'
              204  LOAD_CONST               32
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L.  90       210  LOAD_STR                 'RGBA'
              212  LOAD_FAST                'self'
              214  STORE_ATTR               mode
              216  JUMP_FORWARD        226  'to 226'
            218_0  COME_FROM           194  '194'

 L.  92       218  LOAD_GLOBAL              SyntaxError
              220  LOAD_STR                 'unknown TGA mode'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           216  '216'
            226_1  COME_FROM           208  '208'
            226_2  COME_FROM           186  '186'
            226_3  COME_FROM           170  '170'
            226_4  COME_FROM           162  '162'

 L.  95       226  LOAD_FAST                'flags'
              228  LOAD_CONST               48
              230  BINARY_AND       
              232  STORE_FAST               'orientation'

 L.  96       234  LOAD_FAST                'orientation'
              236  LOAD_CONST               32
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   248  'to 248'

 L.  97       242  LOAD_CONST               1
              244  STORE_FAST               'orientation'
              246  JUMP_FORWARD        268  'to 268'
            248_0  COME_FROM           240  '240'

 L.  98       248  LOAD_FAST                'orientation'
          250_252  POP_JUMP_IF_TRUE    260  'to 260'

 L.  99       254  LOAD_CONST               -1
              256  STORE_FAST               'orientation'
              258  JUMP_FORWARD        268  'to 268'
            260_0  COME_FROM           250  '250'

 L. 101       260  LOAD_GLOBAL              SyntaxError
              262  LOAD_STR                 'unknown TGA orientation'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  RAISE_VARARGS_1       1  'exception instance'
            268_0  COME_FROM           258  '258'
            268_1  COME_FROM           246  '246'

 L. 103       268  LOAD_FAST                'orientation'
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                info
              274  LOAD_STR                 'orientation'
              276  STORE_SUBSCR     

 L. 105       278  LOAD_FAST                'imagetype'
              280  LOAD_CONST               8
              282  BINARY_AND       
          284_286  POP_JUMP_IF_FALSE   298  'to 298'

 L. 106       288  LOAD_STR                 'tga_rle'
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                info
              294  LOAD_STR                 'compression'
              296  STORE_SUBSCR     
            298_0  COME_FROM           284  '284'

 L. 108       298  LOAD_FAST                'id_len'
          300_302  POP_JUMP_IF_FALSE   322  'to 322'

 L. 109       304  LOAD_FAST                'self'
              306  LOAD_ATTR                fp
              308  LOAD_METHOD              read
              310  LOAD_FAST                'id_len'
              312  CALL_METHOD_1         1  '1 positional argument'
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                info
              318  LOAD_STR                 'id_section'
              320  STORE_SUBSCR     
            322_0  COME_FROM           300  '300'

 L. 111       322  LOAD_FAST                'colormaptype'
          324_326  POP_JUMP_IF_FALSE   498  'to 498'

 L. 113       328  LOAD_GLOBAL              i16
              330  LOAD_FAST                's'
              332  LOAD_CONST               3
              334  CALL_FUNCTION_2       2  '2 positional arguments'
              336  LOAD_GLOBAL              i16
              338  LOAD_FAST                's'
              340  LOAD_CONST               5
              342  CALL_FUNCTION_2       2  '2 positional arguments'
              344  LOAD_GLOBAL              i16
              346  LOAD_FAST                's'
              348  LOAD_CONST               7
              350  CALL_FUNCTION_2       2  '2 positional arguments'
              352  ROT_THREE        
              354  ROT_TWO          
              356  STORE_FAST               'start'
              358  STORE_FAST               'size'
              360  STORE_FAST               'mapdepth'

 L. 114       362  LOAD_FAST                'mapdepth'
              364  LOAD_CONST               16
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   408  'to 408'

 L. 115       372  LOAD_GLOBAL              ImagePalette
              374  LOAD_METHOD              raw

 L. 116       376  LOAD_STR                 'BGR;16'
              378  LOAD_CONST               b'\x00\x00'
              380  LOAD_FAST                'start'
              382  BINARY_MULTIPLY  
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                fp
              388  LOAD_METHOD              read
              390  LOAD_CONST               2
              392  LOAD_FAST                'size'
              394  BINARY_MULTIPLY  
              396  CALL_METHOD_1         1  '1 positional argument'
              398  BINARY_ADD       
              400  CALL_METHOD_2         2  '2 positional arguments'
              402  LOAD_FAST                'self'
              404  STORE_ATTR               palette
              406  JUMP_FORWARD        498  'to 498'
            408_0  COME_FROM           368  '368'

 L. 118       408  LOAD_FAST                'mapdepth'
              410  LOAD_CONST               24
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   454  'to 454'

 L. 119       418  LOAD_GLOBAL              ImagePalette
              420  LOAD_METHOD              raw

 L. 120       422  LOAD_STR                 'BGR'
              424  LOAD_CONST               b'\x00\x00\x00'
              426  LOAD_FAST                'start'
              428  BINARY_MULTIPLY  
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                fp
              434  LOAD_METHOD              read
              436  LOAD_CONST               3
              438  LOAD_FAST                'size'
              440  BINARY_MULTIPLY  
              442  CALL_METHOD_1         1  '1 positional argument'
              444  BINARY_ADD       
              446  CALL_METHOD_2         2  '2 positional arguments'
              448  LOAD_FAST                'self'
              450  STORE_ATTR               palette
              452  JUMP_FORWARD        498  'to 498'
            454_0  COME_FROM           414  '414'

 L. 122       454  LOAD_FAST                'mapdepth'
              456  LOAD_CONST               32
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_FALSE   498  'to 498'

 L. 123       464  LOAD_GLOBAL              ImagePalette
              466  LOAD_METHOD              raw

 L. 124       468  LOAD_STR                 'BGRA'
              470  LOAD_CONST               b'\x00\x00\x00\x00'
              472  LOAD_FAST                'start'
              474  BINARY_MULTIPLY  
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                fp
              480  LOAD_METHOD              read
              482  LOAD_CONST               4
              484  LOAD_FAST                'size'
              486  BINARY_MULTIPLY  
              488  CALL_METHOD_1         1  '1 positional argument'
              490  BINARY_ADD       
              492  CALL_METHOD_2         2  '2 positional arguments'
              494  LOAD_FAST                'self'
              496  STORE_ATTR               palette
            498_0  COME_FROM           460  '460'
            498_1  COME_FROM           452  '452'
            498_2  COME_FROM           406  '406'
            498_3  COME_FROM           324  '324'

 L. 128       498  SETUP_EXCEPT        600  'to 600'

 L. 129       500  LOAD_GLOBAL              MODES
              502  LOAD_FAST                'imagetype'
              504  LOAD_CONST               7
              506  BINARY_AND       
              508  LOAD_FAST                'depth'
              510  BUILD_TUPLE_2         2 
              512  BINARY_SUBSCR    
              514  STORE_FAST               'rawmode'

 L. 130       516  LOAD_FAST                'imagetype'
              518  LOAD_CONST               8
              520  BINARY_AND       
          522_524  POP_JUMP_IF_FALSE   562  'to 562'

 L. 134       526  LOAD_STR                 'tga_rle'

 L. 135       528  LOAD_CONST               (0, 0)
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                size
              534  BINARY_ADD       

 L. 136       536  LOAD_FAST                'self'
              538  LOAD_ATTR                fp
              540  LOAD_METHOD              tell
              542  CALL_METHOD_0         0  '0 positional arguments'

 L. 137       544  LOAD_FAST                'rawmode'
              546  LOAD_FAST                'orientation'
              548  LOAD_FAST                'depth'
              550  BUILD_TUPLE_3         3 
              552  BUILD_TUPLE_4         4 
              554  BUILD_LIST_1          1 
              556  LOAD_FAST                'self'
              558  STORE_ATTR               tile
              560  JUMP_FORWARD        596  'to 596'
            562_0  COME_FROM           522  '522'

 L. 143       562  LOAD_STR                 'raw'

 L. 144       564  LOAD_CONST               (0, 0)
              566  LOAD_FAST                'self'
              568  LOAD_ATTR                size
              570  BINARY_ADD       

 L. 145       572  LOAD_FAST                'self'
              574  LOAD_ATTR                fp
              576  LOAD_METHOD              tell
              578  CALL_METHOD_0         0  '0 positional arguments'

 L. 146       580  LOAD_FAST                'rawmode'
              582  LOAD_CONST               0
              584  LOAD_FAST                'orientation'
              586  BUILD_TUPLE_3         3 
              588  BUILD_TUPLE_4         4 
              590  BUILD_LIST_1          1 
              592  LOAD_FAST                'self'
              594  STORE_ATTR               tile
            596_0  COME_FROM           560  '560'
              596  POP_BLOCK        
              598  JUMP_FORWARD        622  'to 622'
            600_0  COME_FROM_EXCEPT    498  '498'

 L. 149       600  DUP_TOP          
              602  LOAD_GLOBAL              KeyError
              604  COMPARE_OP               exception-match
          606_608  POP_JUMP_IF_FALSE   620  'to 620'
              610  POP_TOP          
              612  POP_TOP          
              614  POP_TOP          

 L. 150       616  POP_EXCEPT       
              618  JUMP_FORWARD        622  'to 622'
            620_0  COME_FROM           606  '606'
              620  END_FINALLY      
            622_0  COME_FROM           618  '618'
            622_1  COME_FROM           598  '598'

Parse error at or near `COME_FROM' instruction at offset 126_0


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