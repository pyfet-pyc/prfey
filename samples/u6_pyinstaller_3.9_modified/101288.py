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
_MAGIC = b'\x00\x00\x01\x00'

def _save--- This code section failed: ---

 L.  41         0  LOAD_FAST                'fp'
                2  LOAD_METHOD              write
                4  LOAD_GLOBAL              _MAGIC
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  42        10  LOAD_FAST                'im'
               12  LOAD_ATTR                encoderinfo
               14  LOAD_METHOD              get

 L.  43        16  LOAD_STR                 'sizes'

 L.  44        18  BUILD_LIST_0          0 
               20  LOAD_CONST               ((16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256))
               22  CALL_FINALLY         25  'to 25'

 L.  42        24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'sizes'

 L.  46        28  LOAD_FAST                'im'
               30  LOAD_ATTR                size
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_DEREF              'width'
               36  STORE_DEREF              'height'

 L.  47        38  LOAD_GLOBAL              filter

 L.  48        40  LOAD_CLOSURE             'height'
               42  LOAD_CLOSURE             'width'
               44  BUILD_TUPLE_2         2 
               46  LOAD_LAMBDA              '<code_object <lambda>>'
               48  LOAD_STR                 '_save.<locals>.<lambda>'
               50  MAKE_FUNCTION_8          'closure'

 L.  51        52  LOAD_FAST                'sizes'

 L.  47        54  CALL_FUNCTION_2       2  ''
               56  STORE_FAST               'sizes'

 L.  53        58  LOAD_GLOBAL              list
               60  LOAD_FAST                'sizes'
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'sizes'

 L.  54        66  LOAD_FAST                'fp'
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

 L.  55        88  LOAD_FAST                'fp'
               90  LOAD_METHOD              tell
               92  CALL_METHOD_0         0  ''
               94  LOAD_GLOBAL              len
               96  LOAD_FAST                'sizes'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               16
              102  BINARY_MULTIPLY  
              104  BINARY_ADD       
              106  STORE_FAST               'offset'

 L.  56       108  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              110  LOAD_STR                 '_save.<locals>.<dictcomp>'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  LOAD_FAST                'im'
              116  LOAD_ATTR                encoderinfo
              118  LOAD_METHOD              get
              120  LOAD_STR                 'append_images'
              122  BUILD_LIST_0          0 
              124  CALL_METHOD_2         2  ''
              126  GET_ITER         
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'provided_images'

 L.  57       132  LOAD_FAST                'sizes'
              134  GET_ITER         
          136_138  FOR_ITER            428  'to 428'
              140  STORE_FAST               'size'

 L.  58       142  LOAD_FAST                'size'
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_DEREF              'width'
              148  STORE_DEREF              'height'

 L.  60       150  LOAD_FAST                'fp'
              152  LOAD_METHOD              write
              154  LOAD_GLOBAL              struct
              156  LOAD_METHOD              pack
              158  LOAD_STR                 'B'
              160  LOAD_DEREF               'width'
              162  LOAD_CONST               256
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   172  'to 172'
              168  LOAD_DEREF               'width'
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           166  '166'
              172  LOAD_CONST               0
            174_0  COME_FROM           170  '170'
              174  CALL_METHOD_2         2  ''
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.  61       180  LOAD_FAST                'fp'
              182  LOAD_METHOD              write
              184  LOAD_GLOBAL              struct
              186  LOAD_METHOD              pack
              188  LOAD_STR                 'B'
              190  LOAD_DEREF               'height'
              192  LOAD_CONST               256
              194  COMPARE_OP               <
              196  POP_JUMP_IF_FALSE   202  'to 202'
              198  LOAD_DEREF               'height'
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM           196  '196'
              202  LOAD_CONST               0
            204_0  COME_FROM           200  '200'
              204  CALL_METHOD_2         2  ''
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L.  62       210  LOAD_FAST                'fp'
              212  LOAD_METHOD              write
              214  LOAD_CONST               b'\x00'
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L.  63       220  LOAD_FAST                'fp'
              222  LOAD_METHOD              write
              224  LOAD_CONST               b'\x00'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L.  64       230  LOAD_FAST                'fp'
              232  LOAD_METHOD              write
              234  LOAD_CONST               b'\x00\x00'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L.  65       240  LOAD_FAST                'fp'
              242  LOAD_METHOD              write
              244  LOAD_GLOBAL              struct
              246  LOAD_METHOD              pack
              248  LOAD_STR                 '<H'
              250  LOAD_CONST               32
              252  CALL_METHOD_2         2  ''
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L.  67       258  LOAD_GLOBAL              BytesIO
              260  CALL_FUNCTION_0       0  ''
              262  STORE_FAST               'image_io'

 L.  68       264  LOAD_FAST                'provided_images'
              266  LOAD_METHOD              get
              268  LOAD_FAST                'size'
              270  CALL_METHOD_1         1  ''
              272  STORE_FAST               'tmp'

 L.  69       274  LOAD_FAST                'tmp'
          276_278  POP_JUMP_IF_TRUE    306  'to 306'

 L.  71       280  LOAD_FAST                'im'
              282  LOAD_METHOD              copy
              284  CALL_METHOD_0         0  ''
              286  STORE_FAST               'tmp'

 L.  72       288  LOAD_FAST                'tmp'
              290  LOAD_ATTR                thumbnail
              292  LOAD_FAST                'size'
              294  LOAD_GLOBAL              Image
              296  LOAD_ATTR                LANCZOS
              298  LOAD_CONST               None
              300  LOAD_CONST               ('reducing_gap',)
              302  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              304  POP_TOP          
            306_0  COME_FROM           276  '276'

 L.  73       306  LOAD_FAST                'tmp'
              308  LOAD_METHOD              save
              310  LOAD_FAST                'image_io'
              312  LOAD_STR                 'png'
              314  CALL_METHOD_2         2  ''
              316  POP_TOP          

 L.  74       318  LOAD_FAST                'image_io'
              320  LOAD_METHOD              seek
              322  LOAD_CONST               0
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          

 L.  75       328  LOAD_FAST                'image_io'
              330  LOAD_METHOD              read
              332  CALL_METHOD_0         0  ''
              334  STORE_FAST               'image_bytes'

 L.  76       336  LOAD_GLOBAL              len
              338  LOAD_FAST                'image_bytes'
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'bytes_len'

 L.  77       344  LOAD_FAST                'fp'
              346  LOAD_METHOD              write
              348  LOAD_GLOBAL              struct
              350  LOAD_METHOD              pack
              352  LOAD_STR                 '<I'
              354  LOAD_FAST                'bytes_len'
              356  CALL_METHOD_2         2  ''
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          

 L.  78       362  LOAD_FAST                'fp'
              364  LOAD_METHOD              write
              366  LOAD_GLOBAL              struct
              368  LOAD_METHOD              pack
              370  LOAD_STR                 '<I'
              372  LOAD_FAST                'offset'
              374  CALL_METHOD_2         2  ''
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          

 L.  79       380  LOAD_FAST                'fp'
              382  LOAD_METHOD              tell
              384  CALL_METHOD_0         0  ''
              386  STORE_FAST               'current'

 L.  80       388  LOAD_FAST                'fp'
              390  LOAD_METHOD              seek
              392  LOAD_FAST                'offset'
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          

 L.  81       398  LOAD_FAST                'fp'
              400  LOAD_METHOD              write
              402  LOAD_FAST                'image_bytes'
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          

 L.  82       408  LOAD_FAST                'offset'
              410  LOAD_FAST                'bytes_len'
              412  BINARY_ADD       
              414  STORE_FAST               'offset'

 L.  83       416  LOAD_FAST                'fp'
              418  LOAD_METHOD              seek
              420  LOAD_FAST                'current'
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          
              426  JUMP_BACK           136  'to 136'

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

 L. 156         0  LOAD_GLOBAL              enumerate
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

 L. 157        18  LOAD_FAST                'size'
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

 L. 158        50  LOAD_FAST                'i'
               52  ROT_TWO          
               54  POP_TOP          
               56  RETURN_VALUE     
               58  JUMP_BACK            10  'to 10'

 L. 159        60  LOAD_CONST               0
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
        else:
            im = BmpImagePlugin.DibImageFileself.buf
            Image._decompression_bomb_checkim.size
            im._size = (
             im.size[0], int(im.size[1] / 2))
            d, e, o, a = im.tile[0]
            im.tile[0] = (d, (0, 0) + im.size, o, a)
            mode = a[0]
            bpp = 8
            for k, v in BmpImagePlugin.BIT2MODE.items:
                if mode == v[1]:
                    bpp = k
                    break
            else:
                if 32 == bpp:
                    self.buf.seeko
                    alpha_bytes = self.buf.read(im.size[0] * im.size[1] * 4)[3::4]
                    mask = Image.frombuffer('L', im.size, alpha_bytes, 'raw', ('L',
                                                                               0,
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
    __doc__ = "\n    PIL read-only image support for Microsoft Windows .ico files.\n\n    By default the largest resolution image in the file will be loaded. This\n    can be changed by altering the 'size' attribute before calling 'load'.\n\n    The info dictionary has a key 'sizes' that is a list of the sizes available\n    in the icon file.\n\n    Handles classic, XP and Vista icon formats.\n\n    When saving, PNG compression is used. Support for this was only added in\n    Windows Vista.\n\n    This plugin is a refactored version of Win32IconImagePlugin by Bryan Davis\n    <casadebender@gmail.com>.\n    https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki\n    "
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

 L. 291         0  LOAD_FAST                'value'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  LOAD_STR                 'sizes'
                8  BINARY_SUBSCR    
               10  <118>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 292        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'This is not one of the allowed sizes of this image'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 293        22  LOAD_FAST                'value'
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