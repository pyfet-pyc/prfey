# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\IcoImagePlugin.py
import struct, warnings
from io import BytesIO
from math import ceil, log
from . import BmpImagePlugin, Image, ImageFile, PngImagePlugin
from ._binary import i16le as i16
from ._binary import i32le as i32
from ._binary import o32le as o32
_MAGIC = b'\x00\x00\x01\x00'

def _save--- This code section failed: ---

 L.  42         0  LOAD_FAST                'fp'
                2  LOAD_METHOD              write
                4  LOAD_GLOBAL              _MAGIC
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  43        10  LOAD_FAST                'im'
               12  LOAD_ATTR                encoderinfo
               14  LOAD_METHOD              get

 L.  44        16  LOAD_STR                 'sizes'

 L.  45        18  BUILD_LIST_0          0 
               20  LOAD_CONST               ((16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256))
               22  CALL_FINALLY         25  'to 25'

 L.  43        24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'sizes'

 L.  47        28  LOAD_FAST                'im'
               30  LOAD_ATTR                size
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_DEREF              'width'
               36  STORE_DEREF              'height'

 L.  48        38  LOAD_GLOBAL              filter

 L.  49        40  LOAD_CLOSURE             'height'
               42  LOAD_CLOSURE             'width'
               44  BUILD_TUPLE_2         2 
               46  LOAD_LAMBDA              '<code_object <lambda>>'
               48  LOAD_STR                 '_save.<locals>.<lambda>'
               50  MAKE_FUNCTION_8          'closure'

 L.  52        52  LOAD_FAST                'sizes'

 L.  48        54  CALL_FUNCTION_2       2  ''
               56  STORE_FAST               'sizes'

 L.  54        58  LOAD_GLOBAL              list
               60  LOAD_FAST                'sizes'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'sizes'

 L.  55        66  LOAD_FAST                'fp'
               68  LOAD_METHOD              write
               70  LOAD_GLOBAL              struct
               72  LOAD_METHOD              pack
               74  LOAD_STR                 '<H'
               76  LOAD_GLOBAL              len
               78  LOAD_FAST                'sizes'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_METHOD_2         2  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.  56        88  LOAD_FAST                'fp'
               90  LOAD_METHOD              tell
               92  CALL_METHOD_0         0  ''
               94  LOAD_GLOBAL              len
               96  LOAD_FAST                'sizes'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               16
              102  BINARY_MULTIPLY  
              104  BINARY_ADD       
              106  STORE_FAST               'offset'

 L.  57       108  LOAD_FAST                'im'
              110  LOAD_ATTR                encoderinfo
              112  LOAD_METHOD              get
              114  LOAD_STR                 'bitmap_format'
              116  CALL_METHOD_1         1  ''
              118  LOAD_STR                 'bmp'
              120  COMPARE_OP               ==
              122  STORE_FAST               'bmp'

 L.  58       124  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              126  LOAD_STR                 '_save.<locals>.<dictcomp>'
              128  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              130  LOAD_FAST                'im'
              132  LOAD_ATTR                encoderinfo
              134  LOAD_METHOD              get
              136  LOAD_STR                 'append_images'
              138  BUILD_LIST_0          0 
              140  CALL_METHOD_2         2  ''
              142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'provided_images'

 L.  59       148  LOAD_FAST                'sizes'
              150  GET_ITER         
          152_154  FOR_ITER            586  'to 586'
              156  STORE_FAST               'size'

 L.  60       158  LOAD_FAST                'size'
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_DEREF              'width'
              164  STORE_DEREF              'height'

 L.  62       166  LOAD_FAST                'fp'
              168  LOAD_METHOD              write
              170  LOAD_GLOBAL              struct
              172  LOAD_METHOD              pack
              174  LOAD_STR                 'B'
              176  LOAD_DEREF               'width'
              178  LOAD_CONST               256
              180  COMPARE_OP               <
              182  POP_JUMP_IF_FALSE   188  'to 188'
              184  LOAD_DEREF               'width'
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           182  '182'
              188  LOAD_CONST               0
            190_0  COME_FROM           186  '186'
              190  CALL_METHOD_2         2  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L.  63       196  LOAD_FAST                'fp'
              198  LOAD_METHOD              write
              200  LOAD_GLOBAL              struct
              202  LOAD_METHOD              pack
              204  LOAD_STR                 'B'
              206  LOAD_DEREF               'height'
              208  LOAD_CONST               256
              210  COMPARE_OP               <
              212  POP_JUMP_IF_FALSE   218  'to 218'
              214  LOAD_DEREF               'height'
              216  JUMP_FORWARD        220  'to 220'
            218_0  COME_FROM           212  '212'
              218  LOAD_CONST               0
            220_0  COME_FROM           216  '216'
              220  CALL_METHOD_2         2  ''
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L.  64       226  LOAD_FAST                'fp'
              228  LOAD_METHOD              write
              230  LOAD_CONST               b'\x00'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L.  65       236  LOAD_FAST                'fp'
              238  LOAD_METHOD              write
              240  LOAD_CONST               b'\x00'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L.  66       246  LOAD_FAST                'fp'
              248  LOAD_METHOD              write
              250  LOAD_CONST               b'\x00\x00'
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          

 L.  68       256  LOAD_FAST                'provided_images'
              258  LOAD_METHOD              get
              260  LOAD_FAST                'size'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'tmp'

 L.  69       266  LOAD_FAST                'tmp'
          268_270  POP_JUMP_IF_TRUE    298  'to 298'

 L.  71       272  LOAD_FAST                'im'
              274  LOAD_METHOD              copy
              276  CALL_METHOD_0         0  ''
              278  STORE_FAST               'tmp'

 L.  72       280  LOAD_FAST                'tmp'
              282  LOAD_ATTR                thumbnail
              284  LOAD_FAST                'size'
              286  LOAD_GLOBAL              Image
              288  LOAD_ATTR                LANCZOS
              290  LOAD_CONST               None
              292  LOAD_CONST               ('reducing_gap',)
              294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              296  POP_TOP          
            298_0  COME_FROM           268  '268'

 L.  73       298  LOAD_FAST                'bmp'
          300_302  POP_JUMP_IF_FALSE   320  'to 320'
              304  LOAD_GLOBAL              BmpImagePlugin
              306  LOAD_ATTR                SAVE
              308  LOAD_FAST                'tmp'
              310  LOAD_ATTR                mode
              312  BINARY_SUBSCR    
              314  LOAD_CONST               1
              316  BINARY_SUBSCR    
              318  JUMP_FORWARD        322  'to 322'
            320_0  COME_FROM           300  '300'
              320  LOAD_CONST               32
            322_0  COME_FROM           318  '318'
              322  STORE_FAST               'bits'

 L.  74       324  LOAD_FAST                'fp'
              326  LOAD_METHOD              write
              328  LOAD_GLOBAL              struct
              330  LOAD_METHOD              pack
              332  LOAD_STR                 '<H'
              334  LOAD_FAST                'bits'
              336  CALL_METHOD_2         2  ''
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          

 L.  76       342  LOAD_GLOBAL              BytesIO
              344  CALL_FUNCTION_0       0  ''
              346  STORE_FAST               'image_io'

 L.  77       348  LOAD_FAST                'bmp'
          350_352  POP_JUMP_IF_FALSE   422  'to 422'

 L.  78       354  LOAD_FAST                'tmp'
              356  LOAD_METHOD              save
              358  LOAD_FAST                'image_io'
              360  LOAD_STR                 'dib'
              362  CALL_METHOD_2         2  ''
              364  POP_TOP          

 L.  80       366  LOAD_FAST                'bits'
              368  LOAD_CONST               32
              370  COMPARE_OP               !=
          372_374  POP_JUMP_IF_FALSE   434  'to 434'

 L.  81       376  LOAD_GLOBAL              Image
              378  LOAD_METHOD              new
              380  LOAD_STR                 '1'
              382  LOAD_FAST                'tmp'
              384  LOAD_ATTR                size
              386  CALL_METHOD_2         2  ''
              388  STORE_FAST               'and_mask'

 L.  82       390  LOAD_GLOBAL              ImageFile
              392  LOAD_METHOD              _save

 L.  83       394  LOAD_FAST                'and_mask'
              396  LOAD_FAST                'image_io'
              398  LOAD_STR                 'raw'
              400  LOAD_CONST               (0, 0)
              402  LOAD_FAST                'tmp'
              404  LOAD_ATTR                size
              406  BINARY_ADD       
              408  LOAD_CONST               0
              410  LOAD_CONST               ('1', 0, -1)
              412  BUILD_TUPLE_4         4 
              414  BUILD_LIST_1          1 

 L.  82       416  CALL_METHOD_3         3  ''
              418  POP_TOP          
              420  JUMP_FORWARD        434  'to 434'
            422_0  COME_FROM           350  '350'

 L.  86       422  LOAD_FAST                'tmp'
              424  LOAD_METHOD              save
              426  LOAD_FAST                'image_io'
              428  LOAD_STR                 'png'
              430  CALL_METHOD_2         2  ''
              432  POP_TOP          
            434_0  COME_FROM           420  '420'
            434_1  COME_FROM           372  '372'

 L.  87       434  LOAD_FAST                'image_io'
              436  LOAD_METHOD              seek
              438  LOAD_CONST               0
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          

 L.  88       444  LOAD_FAST                'image_io'
              446  LOAD_METHOD              read
              448  CALL_METHOD_0         0  ''
              450  STORE_FAST               'image_bytes'

 L.  89       452  LOAD_FAST                'bmp'
          454_456  POP_JUMP_IF_FALSE   494  'to 494'

 L.  90       458  LOAD_FAST                'image_bytes'
              460  LOAD_CONST               None
              462  LOAD_CONST               8
              464  BUILD_SLICE_2         2 
              466  BINARY_SUBSCR    
              468  LOAD_GLOBAL              o32
              470  LOAD_DEREF               'height'
              472  LOAD_CONST               2
              474  BINARY_MULTIPLY  
              476  CALL_FUNCTION_1       1  ''
              478  BINARY_ADD       
              480  LOAD_FAST                'image_bytes'
              482  LOAD_CONST               12
              484  LOAD_CONST               None
              486  BUILD_SLICE_2         2 
              488  BINARY_SUBSCR    
              490  BINARY_ADD       
              492  STORE_FAST               'image_bytes'
            494_0  COME_FROM           454  '454'

 L.  91       494  LOAD_GLOBAL              len
              496  LOAD_FAST                'image_bytes'
              498  CALL_FUNCTION_1       1  ''
              500  STORE_FAST               'bytes_len'

 L.  92       502  LOAD_FAST                'fp'
              504  LOAD_METHOD              write
              506  LOAD_GLOBAL              struct
              508  LOAD_METHOD              pack
              510  LOAD_STR                 '<I'
              512  LOAD_FAST                'bytes_len'
              514  CALL_METHOD_2         2  ''
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

 L.  93       520  LOAD_FAST                'fp'
              522  LOAD_METHOD              write
              524  LOAD_GLOBAL              struct
              526  LOAD_METHOD              pack
              528  LOAD_STR                 '<I'
              530  LOAD_FAST                'offset'
              532  CALL_METHOD_2         2  ''
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          

 L.  94       538  LOAD_FAST                'fp'
              540  LOAD_METHOD              tell
              542  CALL_METHOD_0         0  ''
              544  STORE_FAST               'current'

 L.  95       546  LOAD_FAST                'fp'
              548  LOAD_METHOD              seek
              550  LOAD_FAST                'offset'
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          

 L.  96       556  LOAD_FAST                'fp'
              558  LOAD_METHOD              write
              560  LOAD_FAST                'image_bytes'
              562  CALL_METHOD_1         1  ''
              564  POP_TOP          

 L.  97       566  LOAD_FAST                'offset'
              568  LOAD_FAST                'bytes_len'
              570  BINARY_ADD       
              572  STORE_FAST               'offset'

 L.  98       574  LOAD_FAST                'fp'
              576  LOAD_METHOD              seek
              578  LOAD_FAST                'current'
              580  CALL_METHOD_1         1  ''
              582  POP_TOP          
              584  JUMP_BACK           152  'to 152'

Parse error at or near `CALL_FINALLY' instruction at offset 22


def _accept(prefix):
    return prefix[:4] == _MAGIC


class IcoFile:

    def __init__(self, buf):
        """
        Parse image from file-like object containing ico file data
        """
        s = buf.read6
        if not _accept(s):
            raise SyntaxError('not an ICO file')
        self.buf = buf
        self.entry = []
        self.nb_items = i16(s, 4)
        for i in range(self.nb_items):
            s = buf.read16
            icon_header = {'width':s[0], 
             'height':s[1], 
             'nb_color':s[2], 
             'reserved':s[3], 
             'planes':i16(s, 4), 
             'bpp':i16(s, 6), 
             'size':i32(s, 8), 
             'offset':i32(s, 12)}
            for j in ('width', 'height'):
                if not icon_header[j]:
                    icon_header[j] = 256
                icon_header['color_depth'] = icon_header['bpp'] or icon_header['nb_color'] != 0 and ceil(log(icon_header['nb_color'], 2)) or 256
                icon_header['dim'] = (
                 icon_header['width'], icon_header['height'])
                icon_header['square'] = icon_header['width'] * icon_header['height']
                self.entry.appendicon_header
            else:
                self.entry = sorted((self.entry), key=(lambda x: x['color_depth']))
                self.entry = sorted((self.entry), key=(lambda x: x['square']))
                self.entry.reverse

    def sizes(self):
        """
        Get a list of all available icon sizes and color depths.
        """
        return {(h['width'], h['height']) for h in self.entry}

    def getentryindex--- This code section failed: ---

 L. 171         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                entry
                6  CALL_FUNCTION_1       1  ''
                8  GET_ITER         
             10_0  COME_FROM            48  '48'
             10_1  COME_FROM            28  '28'
               10  FOR_ITER             60  'to 60'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'i'
               16  STORE_FAST               'h'

 L. 172        18  LOAD_FAST                'size'
               20  LOAD_FAST                'h'
               22  LOAD_STR                 'dim'
               24  BINARY_SUBSCR    
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    10  'to 10'
               30  LOAD_FAST                'bpp'
               32  LOAD_CONST               False
               34  <117>                 0  ''
               36  POP_JUMP_IF_TRUE     50  'to 50'
               38  LOAD_FAST                'bpp'
               40  LOAD_FAST                'h'
               42  LOAD_STR                 'color_depth'
               44  BINARY_SUBSCR    
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    10  'to 10'
             50_0  COME_FROM            36  '36'

 L. 173        50  LOAD_FAST                'i'
               52  ROT_TWO          
               54  POP_TOP          
               56  RETURN_VALUE     
               58  JUMP_BACK            10  'to 10'

 L. 174        60  LOAD_CONST               0
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34

    def getimage(self, size, bpp=False):
        """
        Get an image from the icon
        """
        return self.frameself.getentryindex(size, bpp)

    def frame(self, idx):
        """
        Get an image from frame idx
        """
        header = self.entry[idx]
        self.buf.seekheader['offset']
        data = self.buf.read8
        self.buf.seekheader['offset']
        if data[:8] == PngImagePlugin._MAGIC:
            im = PngImagePlugin.PngImageFileself.buf
            Image._decompression_bomb_checkim.size
        else:
            im = BmpImagePlugin.DibImageFileself.buf
            Image._decompression_bomb_checkim.size
            im._size = (
             im.size[0], int(im.size[1] / 2))
            d, e, o, a = im.tile[0]
            im.tile[0] = (d, (0, 0) + im.size, o, a)
            bpp = header['bpp']
            if 32 == bpp:
                self.buf.seeko
                alpha_bytes = self.buf.read(im.size[0] * im.size[1] * 4)[3::4]
                mask = Image.frombuffer('L', im.size, alpha_bytes, 'raw', ('L', 0,
                                                                           -1))
            else:
                w = im.size[0]
                if w % 32 > 0:
                    w += 32 - im.size[0] % 32
                and_mask_offset = o + int(im.size[0] * im.size[1] * (bpp / 8.0))
                total_bytes = int(w * im.size[1] / 8)
                self.buf.seekand_mask_offset
                mask_data = self.buf.readtotal_bytes
                mask = Image.frombuffer('1', im.size, mask_data, 'raw', (
                 '1;I', int(w / 8), -1))
            im = im.convert'RGBA'
            im.putalphamask
        return im


class IcoImageFile(ImageFile.ImageFile):
    __doc__ = '\n    PIL read-only image support for Microsoft Windows .ico files.\n\n    By default the largest resolution image in the file will be loaded. This\n    can be changed by altering the \'size\' attribute before calling \'load\'.\n\n    The info dictionary has a key \'sizes\' that is a list of the sizes available\n    in the icon file.\n\n    Handles classic, XP and Vista icon formats.\n\n    When saving, PNG compression is used. Support for this was only added in\n    Windows Vista. If you are unable to view the icon in Windows, convert the\n    image to "RGBA" mode before saving.\n\n    This plugin is a refactored version of Win32IconImagePlugin by Bryan Davis\n    <casadebender@gmail.com>.\n    https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki\n    '
    format = 'ICO'
    format_description = 'Windows Icon'

    def _open(self):
        self.ico = IcoFile(self.fp)
        self.info['sizes'] = self.ico.sizes
        self.size = self.ico.entry[0]['dim']
        self.load

    @property
    def size(self):
        return self._size

    @size.setter
    def size--- This code section failed: ---

 L. 302         0  LOAD_FAST                'value'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  LOAD_STR                 'sizes'
                8  BINARY_SUBSCR    
               10  <118>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 303        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'This is not one of the allowed sizes of this image'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 304        22  LOAD_FAST                'value'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _size

Parse error at or near `None' instruction at offset -1

    def load(self):
        if self.im:
            if self.im.size == self.size:
                return
        im = self.ico.getimageself.size
        im.load
        self.im = im.im
        self.mode = im.mode
        if im.size != self.size:
            warnings.warn'Image was not the expected size'
            index = self.ico.getentryindexself.size
            sizes = list(self.info['sizes'])
            sizes[index] = im.size
            self.info['sizes'] = set(sizes)
            self.size = im.size

    def load_seek(self):
        pass


Image.register_open(IcoImageFile.format, IcoImageFile, _accept)
Image.register_save(IcoImageFile.format, _save)
Image.register_extension(IcoImageFile.format, '.ico')
Image.register_mime(IcoImageFile.format, 'image/x-icon')