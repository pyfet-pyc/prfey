# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\Jpeg2KImagePlugin.py
import io, os, struct
from . import Image, ImageFile

def _parse_codestream(fp):
    """Parse the JPEG 2000 codestream to extract the size and component
    count from the SIZ marker segment, returning a PIL (size, mode) tuple."""
    hdr = fp.read(2)
    lsiz = struct.unpack('>H', hdr)[0]
    siz = hdr + fp.read(lsiz - 2)
    lsiz, rsiz, xsiz, ysiz, xosiz, yosiz, _, _, _, _, csiz = struct.unpack_from('>HHIIIIIIIIH', siz)
    ssiz = [
     None] * csiz
    xrsiz = [None] * csiz
    yrsiz = [None] * csiz
    for i in range(csiz):
        ssiz[i], xrsiz[i], yrsiz[i] = struct.unpack_from('>BBB', siz, 36 + 3 * i)
    else:
        size = (
         xsiz - xosiz, ysiz - yosiz)
        if csiz == 1:
            if yrsiz[0] & 127 > 8:
                mode = 'I;16'
            else:
                mode = 'L'
        else:
            if csiz == 2:
                mode = 'LA'
            else:
                if csiz == 3:
                    mode = 'RGB'
                else:
                    if csiz == 4:
                        mode = 'RGBA'
                    else:
                        mode = None
        return (
         size, mode)


def _parse_jp2_header--- This code section failed: ---

 L.  61         0  LOAD_CONST               None
                2  STORE_FAST               'header'

 L.  62         4  LOAD_CONST               None
                6  STORE_FAST               'mimetype'

 L.  64         8  LOAD_GLOBAL              struct
               10  LOAD_METHOD              unpack
               12  LOAD_STR                 '>I4s'
               14  LOAD_FAST                'fp'
               16  LOAD_METHOD              read
               18  LOAD_CONST               8
               20  CALL_METHOD_1         1  ''
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'lbox'
               28  STORE_FAST               'tbox'

 L.  65        30  LOAD_FAST                'lbox'
               32  LOAD_CONST               1
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    66  'to 66'

 L.  66        38  LOAD_GLOBAL              struct
               40  LOAD_METHOD              unpack
               42  LOAD_STR                 '>Q'
               44  LOAD_FAST                'fp'
               46  LOAD_METHOD              read
               48  LOAD_CONST               8
               50  CALL_METHOD_1         1  ''
               52  CALL_METHOD_2         2  ''
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  STORE_FAST               'lbox'

 L.  67        60  LOAD_CONST               16
               62  STORE_FAST               'hlen'
               64  JUMP_FORWARD         70  'to 70'
             66_0  COME_FROM            36  '36'

 L.  69        66  LOAD_CONST               8
               68  STORE_FAST               'hlen'
             70_0  COME_FROM            64  '64'

 L.  71        70  LOAD_FAST                'lbox'
               72  LOAD_FAST                'hlen'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.  72        78  LOAD_GLOBAL              SyntaxError
               80  LOAD_STR                 'Invalid JP2 header length'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L.  74        86  LOAD_FAST                'tbox'
               88  LOAD_CONST               b'jp2h'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L.  75        94  LOAD_FAST                'fp'
               96  LOAD_METHOD              read
               98  LOAD_FAST                'lbox'
              100  LOAD_FAST                'hlen'
              102  BINARY_SUBTRACT  
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'header'

 L.  76       108  BREAK_LOOP          182  'to 182'
              110  JUMP_BACK             8  'to 8'
            112_0  COME_FROM            92  '92'

 L.  77       112  LOAD_FAST                'tbox'
              114  LOAD_CONST               b'ftyp'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   162  'to 162'

 L.  78       120  LOAD_FAST                'fp'
              122  LOAD_METHOD              read
              124  LOAD_CONST               4
              126  CALL_METHOD_1         1  ''
              128  LOAD_CONST               b'jpx '
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   138  'to 138'

 L.  79       134  LOAD_STR                 'image/jpx'
              136  STORE_FAST               'mimetype'
            138_0  COME_FROM           132  '132'

 L.  80       138  LOAD_FAST                'fp'
              140  LOAD_METHOD              seek
              142  LOAD_FAST                'lbox'
              144  LOAD_FAST                'hlen'
              146  BINARY_SUBTRACT  
              148  LOAD_CONST               4
              150  BINARY_SUBTRACT  
              152  LOAD_GLOBAL              os
              154  LOAD_ATTR                SEEK_CUR
              156  CALL_METHOD_2         2  ''
              158  POP_TOP          
              160  JUMP_BACK             8  'to 8'
            162_0  COME_FROM           118  '118'

 L.  82       162  LOAD_FAST                'fp'
              164  LOAD_METHOD              seek
              166  LOAD_FAST                'lbox'
              168  LOAD_FAST                'hlen'
              170  BINARY_SUBTRACT  
              172  LOAD_GLOBAL              os
              174  LOAD_ATTR                SEEK_CUR
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          
              180  JUMP_BACK             8  'to 8'

 L.  84       182  LOAD_FAST                'header'
              184  LOAD_CONST               None
              186  COMPARE_OP               is
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L.  85       190  LOAD_GLOBAL              SyntaxError
              192  LOAD_STR                 'could not find JP2 header'
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           188  '188'

 L.  87       198  LOAD_CONST               None
              200  STORE_FAST               'size'

 L.  88       202  LOAD_CONST               None
              204  STORE_FAST               'mode'

 L.  89       206  LOAD_CONST               None
              208  STORE_FAST               'bpc'

 L.  90       210  LOAD_CONST               None
              212  STORE_FAST               'nc'

 L.  92       214  LOAD_GLOBAL              io
              216  LOAD_METHOD              BytesIO
              218  LOAD_FAST                'header'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'hio'
            224_0  COME_FROM           676  '676'
            224_1  COME_FROM           482  '482'
            224_2  COME_FROM           456  '456'

 L.  94       224  LOAD_GLOBAL              struct
              226  LOAD_METHOD              unpack
              228  LOAD_STR                 '>I4s'
              230  LOAD_FAST                'hio'
              232  LOAD_METHOD              read
              234  LOAD_CONST               8
              236  CALL_METHOD_1         1  ''
              238  CALL_METHOD_2         2  ''
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               'lbox'
              244  STORE_FAST               'tbox'

 L.  95       246  LOAD_FAST                'lbox'
              248  LOAD_CONST               1
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   284  'to 284'

 L.  96       256  LOAD_GLOBAL              struct
              258  LOAD_METHOD              unpack
              260  LOAD_STR                 '>Q'
              262  LOAD_FAST                'hio'
              264  LOAD_METHOD              read
              266  LOAD_CONST               8
              268  CALL_METHOD_1         1  ''
              270  CALL_METHOD_2         2  ''
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  STORE_FAST               'lbox'

 L.  97       278  LOAD_CONST               16
              280  STORE_FAST               'hlen'
              282  JUMP_FORWARD        288  'to 288'
            284_0  COME_FROM           252  '252'

 L.  99       284  LOAD_CONST               8
              286  STORE_FAST               'hlen'
            288_0  COME_FROM           282  '282'

 L. 101       288  LOAD_FAST                'hio'
              290  LOAD_METHOD              read
              292  LOAD_FAST                'lbox'
              294  LOAD_FAST                'hlen'
              296  BINARY_SUBTRACT  
              298  CALL_METHOD_1         1  ''
              300  STORE_FAST               'content'

 L. 103       302  LOAD_FAST                'tbox'
              304  LOAD_CONST               b'ihdr'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   450  'to 450'

 L. 104       312  LOAD_GLOBAL              struct
              314  LOAD_METHOD              unpack
              316  LOAD_STR                 '>IIHBBBB'
              318  LOAD_FAST                'content'
              320  CALL_METHOD_2         2  ''
              322  UNPACK_SEQUENCE_7     7 
              324  STORE_FAST               'height'
              326  STORE_FAST               'width'
              328  STORE_FAST               'nc'
              330  STORE_FAST               'bpc'
              332  STORE_FAST               'c'
              334  STORE_FAST               'unkc'
              336  STORE_FAST               'ipr'

 L. 105       338  LOAD_FAST                'width'
              340  LOAD_FAST                'height'
              342  BUILD_TUPLE_2         2 
              344  STORE_FAST               'size'

 L. 106       346  LOAD_FAST                'unkc'
          348_350  POP_JUMP_IF_FALSE   712  'to 712'

 L. 107       352  LOAD_FAST                'nc'
              354  LOAD_CONST               1
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   382  'to 382'
              362  LOAD_FAST                'bpc'
              364  LOAD_CONST               127
              366  BINARY_AND       
              368  LOAD_CONST               8
              370  COMPARE_OP               >
          372_374  POP_JUMP_IF_FALSE   382  'to 382'

 L. 108       376  LOAD_STR                 'I;16'
              378  STORE_FAST               'mode'
              380  JUMP_ABSOLUTE       714  'to 714'
            382_0  COME_FROM           372  '372'
            382_1  COME_FROM           358  '358'

 L. 109       382  LOAD_FAST                'nc'
              384  LOAD_CONST               1
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   398  'to 398'

 L. 110       392  LOAD_STR                 'L'
              394  STORE_FAST               'mode'
              396  JUMP_ABSOLUTE       714  'to 714'
            398_0  COME_FROM           388  '388'

 L. 111       398  LOAD_FAST                'nc'
              400  LOAD_CONST               2
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   414  'to 414'

 L. 112       408  LOAD_STR                 'LA'
              410  STORE_FAST               'mode'
              412  JUMP_ABSOLUTE       714  'to 714'
            414_0  COME_FROM           404  '404'

 L. 113       414  LOAD_FAST                'nc'
              416  LOAD_CONST               3
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   430  'to 430'

 L. 114       424  LOAD_STR                 'RGB'
              426  STORE_FAST               'mode'
              428  JUMP_ABSOLUTE       714  'to 714'
            430_0  COME_FROM           420  '420'

 L. 115       430  LOAD_FAST                'nc'
              432  LOAD_CONST               4
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   714  'to 714'

 L. 116       440  LOAD_STR                 'RGBA'
              442  STORE_FAST               'mode'

 L. 117   444_446  BREAK_LOOP          714  'to 714'
              448  JUMP_BACK           224  'to 224'
            450_0  COME_FROM           308  '308'

 L. 118       450  LOAD_FAST                'tbox'
              452  LOAD_CONST               b'colr'
              454  COMPARE_OP               ==
              456  POP_JUMP_IF_FALSE   224  'to 224'

 L. 119       458  LOAD_GLOBAL              struct
              460  LOAD_METHOD              unpack_from
              462  LOAD_STR                 '>BBB'
              464  LOAD_FAST                'content'
              466  CALL_METHOD_2         2  ''
              468  UNPACK_SEQUENCE_3     3 
              470  STORE_FAST               'meth'
              472  STORE_FAST               'prec'
              474  STORE_FAST               'approx'

 L. 120       476  LOAD_FAST                'meth'
              478  LOAD_CONST               1
              480  COMPARE_OP               ==
              482  POP_JUMP_IF_FALSE   224  'to 224'

 L. 121       484  LOAD_GLOBAL              struct
              486  LOAD_METHOD              unpack_from
              488  LOAD_STR                 '>I'
              490  LOAD_FAST                'content'
              492  LOAD_CONST               3
              494  CALL_METHOD_3         3  ''
              496  LOAD_CONST               0
              498  BINARY_SUBSCR    
              500  STORE_FAST               'cs'

 L. 122       502  LOAD_FAST                'cs'
              504  LOAD_CONST               16
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   594  'to 594'

 L. 123       512  LOAD_FAST                'nc'
              514  LOAD_CONST               1
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   542  'to 542'
              522  LOAD_FAST                'bpc'
              524  LOAD_CONST               127
              526  BINARY_AND       
              528  LOAD_CONST               8
              530  COMPARE_OP               >
          532_534  POP_JUMP_IF_FALSE   542  'to 542'

 L. 124       536  LOAD_STR                 'I;16'
              538  STORE_FAST               'mode'
              540  JUMP_ABSOLUTE       714  'to 714'
            542_0  COME_FROM           532  '532'
            542_1  COME_FROM           518  '518'

 L. 125       542  LOAD_FAST                'nc'
              544  LOAD_CONST               1
              546  COMPARE_OP               ==
          548_550  POP_JUMP_IF_FALSE   558  'to 558'

 L. 126       552  LOAD_STR                 'L'
              554  STORE_FAST               'mode'
              556  JUMP_ABSOLUTE       714  'to 714'
            558_0  COME_FROM           548  '548'

 L. 127       558  LOAD_FAST                'nc'
              560  LOAD_CONST               3
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   574  'to 574'

 L. 128       568  LOAD_STR                 'RGB'
              570  STORE_FAST               'mode'
              572  JUMP_ABSOLUTE       714  'to 714'
            574_0  COME_FROM           564  '564'

 L. 129       574  LOAD_FAST                'nc'
              576  LOAD_CONST               4
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   714  'to 714'

 L. 130       584  LOAD_STR                 'RGBA'
              586  STORE_FAST               'mode'

 L. 131   588_590  BREAK_LOOP          714  'to 714'
              592  JUMP_BACK           224  'to 224'
            594_0  COME_FROM           508  '508'

 L. 132       594  LOAD_FAST                'cs'
              596  LOAD_CONST               17
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   670  'to 670'

 L. 133       604  LOAD_FAST                'nc'
              606  LOAD_CONST               1
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   634  'to 634'
              614  LOAD_FAST                'bpc'
              616  LOAD_CONST               127
              618  BINARY_AND       
              620  LOAD_CONST               8
              622  COMPARE_OP               >
          624_626  POP_JUMP_IF_FALSE   634  'to 634'

 L. 134       628  LOAD_STR                 'I;16'
              630  STORE_FAST               'mode'
              632  JUMP_ABSOLUTE       714  'to 714'
            634_0  COME_FROM           624  '624'
            634_1  COME_FROM           610  '610'

 L. 135       634  LOAD_FAST                'nc'
              636  LOAD_CONST               1
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   650  'to 650'

 L. 136       644  LOAD_STR                 'L'
              646  STORE_FAST               'mode'
              648  JUMP_ABSOLUTE       714  'to 714'
            650_0  COME_FROM           640  '640'

 L. 137       650  LOAD_FAST                'nc'
              652  LOAD_CONST               2
              654  COMPARE_OP               ==
          656_658  POP_JUMP_IF_FALSE   714  'to 714'

 L. 138       660  LOAD_STR                 'LA'
              662  STORE_FAST               'mode'

 L. 139   664_666  BREAK_LOOP          714  'to 714'
              668  JUMP_BACK           224  'to 224'
            670_0  COME_FROM           600  '600'

 L. 140       670  LOAD_FAST                'cs'
              672  LOAD_CONST               18
              674  COMPARE_OP               ==
              676  POP_JUMP_IF_FALSE   224  'to 224'

 L. 141       678  LOAD_FAST                'nc'
              680  LOAD_CONST               3
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   694  'to 694'

 L. 142       688  LOAD_STR                 'RGB'
              690  STORE_FAST               'mode'
              692  JUMP_ABSOLUTE       714  'to 714'
            694_0  COME_FROM           684  '684'

 L. 143       694  LOAD_FAST                'nc'
              696  LOAD_CONST               4
              698  COMPARE_OP               ==
          700_702  POP_JUMP_IF_FALSE   714  'to 714'

 L. 144       704  LOAD_STR                 'RGBA'
              706  STORE_FAST               'mode'

 L. 145   708_710  BREAK_LOOP          714  'to 714'
            712_0  COME_FROM           348  '348'
              712  JUMP_BACK           224  'to 224'
            714_0  COME_FROM           700  '700'
            714_1  COME_FROM           656  '656'
            714_2  COME_FROM           580  '580'
            714_3  COME_FROM           436  '436'

 L. 147       714  LOAD_FAST                'size'
              716  LOAD_CONST               None
              718  COMPARE_OP               is
          720_722  POP_JUMP_IF_TRUE    734  'to 734'
              724  LOAD_FAST                'mode'
              726  LOAD_CONST               None
              728  COMPARE_OP               is
          730_732  POP_JUMP_IF_FALSE   742  'to 742'
            734_0  COME_FROM           720  '720'

 L. 148       734  LOAD_GLOBAL              SyntaxError
              736  LOAD_STR                 'Malformed jp2 header'
              738  CALL_FUNCTION_1       1  ''
              740  RAISE_VARARGS_1       1  'exception instance'
            742_0  COME_FROM           730  '730'

 L. 150       742  LOAD_FAST                'size'
              744  LOAD_FAST                'mode'
              746  LOAD_FAST                'mimetype'
              748  BUILD_TUPLE_3         3 
              750  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 750


class Jpeg2KImageFile(ImageFile.ImageFile):
    format = 'JPEG2000'
    format_description = 'JPEG 2000 (ISO 15444)'

    def _open(self):
        sig = self.fp.read(4)
        if sig == b'\xffO\xffQ':
            self.codec = 'j2k'
            self._size, self.mode = _parse_codestream(self.fp)
        else:
            sig = sig + self.fp.read(8)
            if sig == b'\x00\x00\x00\x0cjP  \r\n\x87\n':
                self.codec = 'jp2'
                header = _parse_jp2_header(self.fp)
                self._size, self.mode, self.custom_mimetype = header
            else:
                raise SyntaxError('not a JPEG 2000 file')
        if self.size is None or self.mode is None:
            raise SyntaxError('unable to determine size/mode')
        self._reduce = 0
        self.layers = 0
        fd = -1
        length = -1
        try:
            fd = self.fp.fileno()
            length = os.fstat(fd).st_size
        except Exception:
            fd = -1
            try:
                pos = self.fp.tell()
                self.fp.seek(0, io.SEEK_END)
                length = self.fp.tell()
                self.fp.seek(pos)
            except Exception:
                length = -1

        else:
            self.tile = [
             (
              'jpeg2k',
              (0, 0) + self.size,
              0,
              (
               self.codec, self._reduce, self.layers, fd, length))]

    @property
    def reduce(self):
        return self._reduce or super().reduce

    @reduce.setter
    def reduce(self, value):
        self._reduce = value

    def load(self):
        if self.tile:
            if self._reduce:
                power = 1 << self._reduce
                adjust = power >> 1
                self._size = (
                 int((self.size[0] + adjust) / power),
                 int((self.size[1] + adjust) / power))
                t = self.tile[0]
                t3 = (t[3][0], self._reduce, self.layers, t[3][3], t[3][4])
                self.tile = [(t[0], (0, 0) + self.size, t[2], t3)]
        return ImageFile.ImageFile.load(self)


def _accept(prefix):
    return prefix[:4] == b'\xffO\xffQ' or prefix[:12] == b'\x00\x00\x00\x0cjP  \r\n\x87\n'


def _save(im, fp, filename):
    if filename.endswith('.j2k'):
        kind = 'j2k'
    else:
        kind = 'jp2'
    info = im.encoderinfo
    offset = info.get('offset', None)
    tile_offset = info.get('tile_offset', None)
    tile_size = info.get('tile_size', None)
    quality_mode = info.get('quality_mode', 'rates')
    quality_layers = info.get('quality_layers', None)
    if quality_layers is not None:
        raise isinstance(quality_layers, (list, tuple)) and all([isinstance(quality_layer, (int, float)) for quality_layer in quality_layers]) or ValueError('quality_layers must be a sequence of numbers')
    num_resolutions = info.get('num_resolutions', 0)
    cblk_size = info.get('codeblock_size', None)
    precinct_size = info.get('precinct_size', None)
    irreversible = info.get('irreversible', False)
    progression = info.get('progression', 'LRCP')
    cinema_mode = info.get('cinema_mode', 'no')
    fd = -1
    if hasattr(fp, 'fileno'):
        try:
            fd = fp.fileno()
        except Exception:
            fd = -1

    im.encoderconfig = (offset,
     tile_offset,
     tile_size,
     quality_mode,
     quality_layers,
     num_resolutions,
     cblk_size,
     precinct_size,
     irreversible,
     progression,
     cinema_mode,
     fd)
    ImageFile._save(im, fp, [('jpeg2k', (0, 0) + im.size, 0, kind)])


Image.register_open(Jpeg2KImageFile.format, Jpeg2KImageFile, _accept)
Image.register_save(Jpeg2KImageFile.format, _save)
Image.register_extensions(Jpeg2KImageFile.format, ['.jp2', '.j2k', '.jpc', '.jpf', '.jpx', '.j2c'])
Image.register_mime(Jpeg2KImageFile.format, 'image/jp2')