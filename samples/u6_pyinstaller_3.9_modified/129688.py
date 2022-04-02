# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PsdImagePlugin.py
import io
from . import Image, ImageFile, ImagePalette
from ._binary import i8
from ._binary import i16be as i16
from ._binary import i32be as i32
MODES = {(0, 1):('1', 1), 
 (0, 8):('L', 1), 
 (1, 8):('L', 1), 
 (2, 8):('P', 1), 
 (3, 8):('RGB', 3), 
 (4, 8):('CMYK', 4), 
 (7, 8):('L', 1), 
 (8, 8):('L', 1), 
 (9, 8):('LAB', 3)}

def _accept(prefix):
    return prefix[:4] == b'8BPS'


class PsdImageFile(ImageFile.ImageFile):
    format = 'PSD'
    format_description = 'Adobe Photoshop'
    _close_exclusive_fp_after_loading = False

    def _open(self):
        read = self.fp.read
        s = read(26)
        if not _accept(s) or i16(s, 4) != 1:
            raise SyntaxError('not a PSD file')
        psd_bits = i16(s, 22)
        psd_channels = i16(s, 12)
        psd_mode = i16(s, 24)
        mode, channels = MODES[(psd_mode, psd_bits)]
        if channels > psd_channels:
            raise OSError('not enough channels')
        self.mode = mode
        self._size = (i32(s, 18), i32(s, 14))
        size = i32(read(4))
        if size:
            data = read(size)
            if mode == 'P':
                if size == 768:
                    self.palette = ImagePalette.raw('RGB;L', data)
        self.resources = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            while self.fp.tell() < end:
                read(4)
                id = i16(read(2))
                name = read(i8(read(1)))
                if not len(name) & 1:
                    read(1)
                data = read(i32(read(4)))
                if len(data) & 1:
                    read(1)
                self.resources.append((id, name, data))
                if id == 1039:
                    self.info['icc_profile'] = data

        self.layers = []
        size = i32(read(4))
        if size:
            end = self.fp.tell() + size
            size = i32(read(4))
            if size:
                self.layers = _layerinfo(self.fp)
            self.fp.seek(end)
        self.n_frames = len(self.layers)
        self.is_animated = self.n_frames > 1
        self.tile = _maketile(self.fp, mode, (0, 0) + self.size, channels)
        self._PsdImageFile__fp = self.fp
        self.frame = 1
        self._min_frame = 1

    def seek--- This code section failed: ---

 L. 138         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'layer'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 139        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 142        14  SETUP_FINALLY        74  'to 74'

 L. 143        16  LOAD_FAST                'self'
               18  LOAD_ATTR                layers
               20  LOAD_FAST                'layer'
               22  LOAD_CONST               1
               24  BINARY_SUBTRACT  
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_4     4 
               30  STORE_FAST               'name'
               32  STORE_FAST               'mode'
               34  STORE_FAST               'bbox'
               36  STORE_FAST               'tile'

 L. 144        38  LOAD_FAST                'mode'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               mode

 L. 145        44  LOAD_FAST                'tile'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               tile

 L. 146        50  LOAD_FAST                'layer'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               frame

 L. 147        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _PsdImageFile__fp
               60  LOAD_FAST                'self'
               62  STORE_ATTR               fp

 L. 148        64  LOAD_FAST                'name'
               66  LOAD_FAST                'bbox'
               68  BUILD_TUPLE_2         2 
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY    14  '14'

 L. 149        74  DUP_TOP          
               76  LOAD_GLOBAL              IndexError
               78  <121>               118  ''
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       110  'to 110'

 L. 150        88  LOAD_GLOBAL              EOFError
               90  LOAD_STR                 'no such layer'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'e'
               96  RAISE_VARARGS_2       2  'exception instance with __cause__'
               98  POP_BLOCK        
              100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  STORE_FAST               'e'
              106  DELETE_FAST              'e'
              108  JUMP_FORWARD        120  'to 120'
            110_0  COME_FROM_FINALLY    86  '86'
              110  LOAD_CONST               None
              112  STORE_FAST               'e'
              114  DELETE_FAST              'e'
              116  <48>             
              118  <48>             
            120_0  COME_FROM           108  '108'

Parse error at or near `<121>' instruction at offset 78

    def tell(self):
        return self.frame

    def load_prepare(self):
        if not self.im or self.im.mode != self.mode or self.im.size != self.size:
            self.im = Image.core.fill(self.mode, self.size, 0)
        if self.mode == 'P':
            Image.Image.load(self)

    def _close__fp--- This code section failed: ---

 L. 165         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 166         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _PsdImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 167        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PsdImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 168        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 169        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 171        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _PsdImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _PsdImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


def _layerinfo--- This code section failed: ---

 L. 176         0  BUILD_LIST_0          0 
                2  STORE_FAST               'layers'

 L. 177         4  LOAD_FAST                'file'
                6  LOAD_ATTR                read
                8  STORE_FAST               'read'

 L. 178        10  LOAD_GLOBAL              range
               12  LOAD_GLOBAL              abs
               14  LOAD_GLOBAL              i16
               16  LOAD_FAST                'read'
               18  LOAD_CONST               2
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  GET_ITER         
            30_32  FOR_ITER            492  'to 492'
               34  STORE_FAST               'i'

 L. 181        36  LOAD_GLOBAL              i32
               38  LOAD_FAST                'read'
               40  LOAD_CONST               4
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'y0'

 L. 182        48  LOAD_GLOBAL              i32
               50  LOAD_FAST                'read'
               52  LOAD_CONST               4
               54  CALL_FUNCTION_1       1  ''
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'x0'

 L. 183        60  LOAD_GLOBAL              i32
               62  LOAD_FAST                'read'
               64  LOAD_CONST               4
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'y1'

 L. 184        72  LOAD_GLOBAL              i32
               74  LOAD_FAST                'read'
               76  LOAD_CONST               4
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'x1'

 L. 187        84  BUILD_LIST_0          0 
               86  STORE_FAST               'info'

 L. 188        88  BUILD_LIST_0          0 
               90  STORE_FAST               'mode'

 L. 189        92  LOAD_GLOBAL              list
               94  LOAD_GLOBAL              range
               96  LOAD_GLOBAL              i16
               98  LOAD_FAST                'read'
              100  LOAD_CONST               2
              102  CALL_FUNCTION_1       1  ''
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'types'

 L. 190       112  LOAD_GLOBAL              len
              114  LOAD_FAST                'types'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_CONST               4
              120  COMPARE_OP               >
              122  POP_JUMP_IF_FALSE   126  'to 126'

 L. 191       124  JUMP_BACK            30  'to 30'
            126_0  COME_FROM           122  '122'

 L. 193       126  LOAD_FAST                'types'
              128  GET_ITER         
              130  FOR_ITER            206  'to 206'
              132  STORE_FAST               'i'

 L. 194       134  LOAD_GLOBAL              i16
              136  LOAD_FAST                'read'
              138  LOAD_CONST               2
              140  CALL_FUNCTION_1       1  ''
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'type'

 L. 196       146  LOAD_FAST                'type'
              148  LOAD_CONST               65535
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   160  'to 160'

 L. 197       154  LOAD_STR                 'A'
              156  STORE_FAST               'm'
              158  JUMP_FORWARD        168  'to 168'
            160_0  COME_FROM           152  '152'

 L. 199       160  LOAD_STR                 'RGBA'
              162  LOAD_FAST                'type'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'm'
            168_0  COME_FROM           158  '158'

 L. 201       168  LOAD_FAST                'mode'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'm'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 202       178  LOAD_GLOBAL              i32
              180  LOAD_FAST                'read'
              182  LOAD_CONST               4
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               'size'

 L. 203       190  LOAD_FAST                'info'
              192  LOAD_METHOD              append
              194  LOAD_FAST                'm'
              196  LOAD_FAST                'size'
              198  BUILD_TUPLE_2         2 
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  JUMP_BACK           130  'to 130'

 L. 206       206  LOAD_FAST                'mode'
              208  LOAD_METHOD              sort
              210  CALL_METHOD_0         0  ''
              212  POP_TOP          

 L. 207       214  LOAD_FAST                'mode'
              216  LOAD_STR                 'R'
              218  BUILD_LIST_1          1 
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   230  'to 230'

 L. 208       224  LOAD_STR                 'L'
              226  STORE_FAST               'mode'
              228  JUMP_FORWARD        272  'to 272'
            230_0  COME_FROM           222  '222'

 L. 209       230  LOAD_FAST                'mode'
              232  BUILD_LIST_0          0 
              234  LOAD_CONST               ('B', 'G', 'R')
              236  CALL_FINALLY        239  'to 239'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   248  'to 248'

 L. 210       242  LOAD_STR                 'RGB'
              244  STORE_FAST               'mode'
              246  JUMP_FORWARD        272  'to 272'
            248_0  COME_FROM           240  '240'

 L. 211       248  LOAD_FAST                'mode'
              250  BUILD_LIST_0          0 
              252  LOAD_CONST               ('A', 'B', 'G', 'R')
              254  CALL_FINALLY        257  'to 257'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   268  'to 268'

 L. 212       262  LOAD_STR                 'RGBA'
              264  STORE_FAST               'mode'
              266  JUMP_FORWARD        272  'to 272'
            268_0  COME_FROM           258  '258'

 L. 214       268  LOAD_CONST               None
              270  STORE_FAST               'mode'
            272_0  COME_FROM           266  '266'
            272_1  COME_FROM           246  '246'
            272_2  COME_FROM           228  '228'

 L. 217       272  LOAD_FAST                'read'
              274  LOAD_CONST               12
              276  CALL_FUNCTION_1       1  ''
              278  POP_TOP          

 L. 218       280  LOAD_STR                 ''
              282  STORE_FAST               'name'

 L. 219       284  LOAD_GLOBAL              i32
              286  LOAD_FAST                'read'
              288  LOAD_CONST               4
              290  CALL_FUNCTION_1       1  ''
              292  CALL_FUNCTION_1       1  ''
              294  STORE_FAST               'size'

 L. 220       296  LOAD_CONST               0
              298  STORE_FAST               'combined'

 L. 221       300  LOAD_FAST                'size'
          302_304  POP_JUMP_IF_FALSE   466  'to 466'

 L. 222       306  LOAD_FAST                'file'
              308  LOAD_METHOD              tell
              310  CALL_METHOD_0         0  ''
              312  LOAD_FAST                'size'
              314  BINARY_ADD       
              316  STORE_FAST               'data_end'

 L. 224       318  LOAD_GLOBAL              i32
              320  LOAD_FAST                'read'
              322  LOAD_CONST               4
              324  CALL_FUNCTION_1       1  ''
              326  CALL_FUNCTION_1       1  ''
              328  STORE_FAST               'length'

 L. 225       330  LOAD_FAST                'length'
          332_334  POP_JUMP_IF_FALSE   354  'to 354'

 L. 226       336  LOAD_FAST                'file'
              338  LOAD_METHOD              seek
              340  LOAD_FAST                'length'
              342  LOAD_CONST               16
              344  BINARY_SUBTRACT  
              346  LOAD_GLOBAL              io
              348  LOAD_ATTR                SEEK_CUR
              350  CALL_METHOD_2         2  ''
              352  POP_TOP          
            354_0  COME_FROM           332  '332'

 L. 227       354  LOAD_FAST                'combined'
              356  LOAD_FAST                'length'
              358  LOAD_CONST               4
              360  BINARY_ADD       
              362  INPLACE_ADD      
              364  STORE_FAST               'combined'

 L. 229       366  LOAD_GLOBAL              i32
              368  LOAD_FAST                'read'
              370  LOAD_CONST               4
              372  CALL_FUNCTION_1       1  ''
              374  CALL_FUNCTION_1       1  ''
              376  STORE_FAST               'length'

 L. 230       378  LOAD_FAST                'length'
          380_382  POP_JUMP_IF_FALSE   398  'to 398'

 L. 231       384  LOAD_FAST                'file'
              386  LOAD_METHOD              seek
              388  LOAD_FAST                'length'
              390  LOAD_GLOBAL              io
              392  LOAD_ATTR                SEEK_CUR
              394  CALL_METHOD_2         2  ''
              396  POP_TOP          
            398_0  COME_FROM           380  '380'

 L. 232       398  LOAD_FAST                'combined'
              400  LOAD_FAST                'length'
              402  LOAD_CONST               4
              404  BINARY_ADD       
              406  INPLACE_ADD      
              408  STORE_FAST               'combined'

 L. 234       410  LOAD_GLOBAL              i8
              412  LOAD_FAST                'read'
              414  LOAD_CONST               1
              416  CALL_FUNCTION_1       1  ''
              418  CALL_FUNCTION_1       1  ''
              420  STORE_FAST               'length'

 L. 235       422  LOAD_FAST                'length'
          424_426  POP_JUMP_IF_FALSE   444  'to 444'

 L. 238       428  LOAD_FAST                'read'
              430  LOAD_FAST                'length'
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_METHOD              decode
              436  LOAD_STR                 'latin-1'
              438  LOAD_STR                 'replace'
              440  CALL_METHOD_2         2  ''
              442  STORE_FAST               'name'
            444_0  COME_FROM           424  '424'

 L. 239       444  LOAD_FAST                'combined'
              446  LOAD_FAST                'length'
              448  LOAD_CONST               1
              450  BINARY_ADD       
              452  INPLACE_ADD      
              454  STORE_FAST               'combined'

 L. 241       456  LOAD_FAST                'file'
              458  LOAD_METHOD              seek
              460  LOAD_FAST                'data_end'
              462  CALL_METHOD_1         1  ''
              464  POP_TOP          
            466_0  COME_FROM           302  '302'

 L. 242       466  LOAD_FAST                'layers'
              468  LOAD_METHOD              append
              470  LOAD_FAST                'name'
              472  LOAD_FAST                'mode'
              474  LOAD_FAST                'x0'
              476  LOAD_FAST                'y0'
              478  LOAD_FAST                'x1'
              480  LOAD_FAST                'y1'
              482  BUILD_TUPLE_4         4 
              484  BUILD_TUPLE_3         3 
              486  CALL_METHOD_1         1  ''
              488  POP_TOP          
              490  JUMP_BACK            30  'to 30'

 L. 245       492  LOAD_CONST               0
              494  STORE_FAST               'i'

 L. 246       496  LOAD_FAST                'layers'
              498  GET_ITER         
              500  FOR_ITER            584  'to 584'
              502  UNPACK_SEQUENCE_3     3 
              504  STORE_FAST               'name'
              506  STORE_FAST               'mode'
              508  STORE_FAST               'bbox'

 L. 247       510  BUILD_LIST_0          0 
              512  STORE_FAST               'tile'

 L. 248       514  LOAD_FAST                'mode'
              516  GET_ITER         
            518_0  COME_FROM           538  '538'
              518  FOR_ITER            556  'to 556'
              520  STORE_FAST               'm'

 L. 249       522  LOAD_GLOBAL              _maketile
              524  LOAD_FAST                'file'
              526  LOAD_FAST                'm'
              528  LOAD_FAST                'bbox'
              530  LOAD_CONST               1
              532  CALL_FUNCTION_4       4  ''
              534  STORE_FAST               't'

 L. 250       536  LOAD_FAST                't'
          538_540  POP_JUMP_IF_FALSE   518  'to 518'

 L. 251       542  LOAD_FAST                'tile'
              544  LOAD_METHOD              extend
              546  LOAD_FAST                't'
              548  CALL_METHOD_1         1  ''
              550  POP_TOP          
          552_554  JUMP_BACK           518  'to 518'

 L. 252       556  LOAD_FAST                'name'
              558  LOAD_FAST                'mode'
              560  LOAD_FAST                'bbox'
              562  LOAD_FAST                'tile'
              564  BUILD_TUPLE_4         4 
              566  LOAD_FAST                'layers'
              568  LOAD_FAST                'i'
              570  STORE_SUBSCR     

 L. 253       572  LOAD_FAST                'i'
              574  LOAD_CONST               1
              576  INPLACE_ADD      
              578  STORE_FAST               'i'
          580_582  JUMP_BACK           500  'to 500'

 L. 255       584  LOAD_FAST                'layers'
              586  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 236


def _maketile(file, mode, bbox, channels):
    tile = None
    read = file.read
    compression = i16(read(2))
    xsize = bbox[2] - bbox[0]
    ysize = bbox[3] - bbox[1]
    offset = file.tell()
    if compression == 0:
        tile = []
        for channel in range(channels):
            layer = mode[channel]
            if mode == 'CMYK':
                layer += ';I'
            tile.append(('raw', bbox, offset, layer))
            offset = offset + xsize * ysize

    else:
        if compression == 1:
            i = 0
            tile = []
            bytecount = read(channels * ysize * 2)
            offset = file.tell()
            for channel in range(channels):
                layer = mode[channel]
                if mode == 'CMYK':
                    layer += ';I'
                tile.append(('packbits', bbox, offset, layer))
                for y in range(ysize):
                    offset = offset + i16(bytecount, i)
                    i += 2

        file.seek(offset)
        if offset & 1:
            read(1)
        return tile


Image.register_open(PsdImageFile.format, PsdImageFile, _accept)
Image.register_extension(PsdImageFile.format, '.psd')
Image.register_mime(PsdImageFile.format, 'image/vnd.adobe.photoshop')