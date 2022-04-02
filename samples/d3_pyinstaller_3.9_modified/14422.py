# decompyle3 version 3.7.5
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
            while True:
                if self.fp.tell() < end:
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
                    _layer_data = io.BytesIO(ImageFile._safe_read(self.fp, size))
                    self.layers = _layerinfo(_layer_data, size)
                self.fp.seek(end)
        self.n_frames = len(self.layers)
        self.is_animated = self.n_frames > 1
        self.tile = _maketile(self.fp, mode, (0, 0) + self.size, channels)
        self._PsdImageFile__fp = self.fp
        self.frame = 1
        self._min_frame = 1

    def seek--- This code section failed: ---

 L. 139         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'layer'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 140        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 143        14  SETUP_FINALLY        74  'to 74'

 L. 144        16  LOAD_FAST                'self'
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

 L. 145        38  LOAD_FAST                'mode'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               mode

 L. 146        44  LOAD_FAST                'tile'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               tile

 L. 147        50  LOAD_FAST                'layer'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               frame

 L. 148        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _PsdImageFile__fp
               60  LOAD_FAST                'self'
               62  STORE_ATTR               fp

 L. 149        64  LOAD_FAST                'name'
               66  LOAD_FAST                'bbox'
               68  BUILD_TUPLE_2         2 
               70  POP_BLOCK        
               72  RETURN_VALUE     
             74_0  COME_FROM_FINALLY    14  '14'

 L. 150        74  DUP_TOP          
               76  LOAD_GLOBAL              IndexError
               78  <121>               118  ''
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       110  'to 110'

 L. 151        88  LOAD_GLOBAL              EOFError
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
        if self.im:
            if self.im.mode != self.mode or (self.im.size != self.size):
                self.im = Image.core.fill(self.mode, self.size, 0)
            if self.mode == 'P':
                Image.Image.load(self)

    def _close__fp--- This code section failed: ---

 L. 166         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 167         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _PsdImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 168        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _PsdImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 169        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 170        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 172        50  LOAD_CONST               None
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

 L. 177         0  BUILD_LIST_0          0 
                2  STORE_FAST               'layers'

 L. 179         4  LOAD_CLOSURE             'fp'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object read>
               10  LOAD_STR                 '_layerinfo.<locals>.read'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_FAST               'read'

 L. 182        16  LOAD_GLOBAL              i16
               18  LOAD_FAST                'read'
               20  LOAD_CONST               2
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'ct'

 L. 185        28  LOAD_FAST                'ct_bytes'
               30  LOAD_GLOBAL              abs
               32  LOAD_FAST                'ct'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               20
               38  BINARY_MULTIPLY  
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 186        44  LOAD_GLOBAL              SyntaxError
               46  LOAD_STR                 'Layer block too short for number of layers requested'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'

 L. 188        52  LOAD_GLOBAL              range
               54  LOAD_GLOBAL              abs
               56  LOAD_FAST                'ct'
               58  CALL_FUNCTION_1       1  ''
               60  CALL_FUNCTION_1       1  ''
               62  GET_ITER         
             64_0  COME_FROM           532  '532'
             64_1  COME_FROM           162  '162'
            64_66  FOR_ITER            534  'to 534'
               68  STORE_FAST               'i'

 L. 191        70  LOAD_GLOBAL              i32
               72  LOAD_FAST                'read'
               74  LOAD_CONST               4
               76  CALL_FUNCTION_1       1  ''
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'y0'

 L. 192        82  LOAD_GLOBAL              i32
               84  LOAD_FAST                'read'
               86  LOAD_CONST               4
               88  CALL_FUNCTION_1       1  ''
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'x0'

 L. 193        94  LOAD_GLOBAL              i32
               96  LOAD_FAST                'read'
               98  LOAD_CONST               4
              100  CALL_FUNCTION_1       1  ''
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'y1'

 L. 194       106  LOAD_GLOBAL              i32
              108  LOAD_FAST                'read'
              110  LOAD_CONST               4
              112  CALL_FUNCTION_1       1  ''
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'x1'

 L. 197       118  BUILD_LIST_0          0 
              120  STORE_FAST               'info'

 L. 198       122  BUILD_LIST_0          0 
              124  STORE_FAST               'mode'

 L. 199       126  LOAD_GLOBAL              i16
              128  LOAD_FAST                'read'
              130  LOAD_CONST               2
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'ct_types'

 L. 200       138  LOAD_GLOBAL              list
              140  LOAD_GLOBAL              range
              142  LOAD_FAST                'ct_types'
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'types'

 L. 201       150  LOAD_GLOBAL              len
              152  LOAD_FAST                'types'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               4
              158  COMPARE_OP               >
              160  POP_JUMP_IF_FALSE   164  'to 164'

 L. 202       162  JUMP_BACK            64  'to 64'
            164_0  COME_FROM           160  '160'

 L. 204       164  LOAD_FAST                'types'
              166  GET_ITER         
            168_0  COME_FROM           242  '242'
              168  FOR_ITER            244  'to 244'
              170  STORE_FAST               'i'

 L. 205       172  LOAD_GLOBAL              i16
              174  LOAD_FAST                'read'
              176  LOAD_CONST               2
              178  CALL_FUNCTION_1       1  ''
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'type'

 L. 207       184  LOAD_FAST                'type'
              186  LOAD_CONST               65535
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L. 208       192  LOAD_STR                 'A'
              194  STORE_FAST               'm'
              196  JUMP_FORWARD        206  'to 206'
            198_0  COME_FROM           190  '190'

 L. 210       198  LOAD_STR                 'RGBA'
              200  LOAD_FAST                'type'
              202  BINARY_SUBSCR    
              204  STORE_FAST               'm'
            206_0  COME_FROM           196  '196'

 L. 212       206  LOAD_FAST                'mode'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'm'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 213       216  LOAD_GLOBAL              i32
              218  LOAD_FAST                'read'
              220  LOAD_CONST               4
              222  CALL_FUNCTION_1       1  ''
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'size'

 L. 214       228  LOAD_FAST                'info'
              230  LOAD_METHOD              append
              232  LOAD_FAST                'm'
              234  LOAD_FAST                'size'
              236  BUILD_TUPLE_2         2 
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  JUMP_BACK           168  'to 168'
            244_0  COME_FROM           168  '168'

 L. 217       244  LOAD_FAST                'mode'
              246  LOAD_METHOD              sort
              248  CALL_METHOD_0         0  ''
              250  POP_TOP          

 L. 218       252  LOAD_FAST                'mode'
              254  LOAD_STR                 'R'
              256  BUILD_LIST_1          1 
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   270  'to 270'

 L. 219       264  LOAD_STR                 'L'
              266  STORE_FAST               'mode'
              268  JUMP_FORWARD        314  'to 314'
            270_0  COME_FROM           260  '260'

 L. 220       270  LOAD_FAST                'mode'
              272  BUILD_LIST_0          0 
              274  LOAD_CONST               ('B', 'G', 'R')
              276  CALL_FINALLY        279  'to 279'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   290  'to 290'

 L. 221       284  LOAD_STR                 'RGB'
              286  STORE_FAST               'mode'
              288  JUMP_FORWARD        314  'to 314'
            290_0  COME_FROM           280  '280'

 L. 222       290  LOAD_FAST                'mode'
              292  BUILD_LIST_0          0 
              294  LOAD_CONST               ('A', 'B', 'G', 'R')
              296  CALL_FINALLY        299  'to 299'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   310  'to 310'

 L. 223       304  LOAD_STR                 'RGBA'
              306  STORE_FAST               'mode'
              308  JUMP_FORWARD        314  'to 314'
            310_0  COME_FROM           300  '300'

 L. 225       310  LOAD_CONST               None
              312  STORE_FAST               'mode'
            314_0  COME_FROM           308  '308'
            314_1  COME_FROM           288  '288'
            314_2  COME_FROM           268  '268'

 L. 228       314  LOAD_FAST                'read'
              316  LOAD_CONST               12
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          

 L. 229       322  LOAD_STR                 ''
              324  STORE_FAST               'name'

 L. 230       326  LOAD_GLOBAL              i32
              328  LOAD_FAST                'read'
              330  LOAD_CONST               4
              332  CALL_FUNCTION_1       1  ''
              334  CALL_FUNCTION_1       1  ''
              336  STORE_FAST               'size'

 L. 231       338  LOAD_CONST               0
              340  STORE_FAST               'combined'

 L. 232       342  LOAD_FAST                'size'
          344_346  POP_JUMP_IF_FALSE   508  'to 508'

 L. 233       348  LOAD_DEREF               'fp'
              350  LOAD_METHOD              tell
              352  CALL_METHOD_0         0  ''
              354  LOAD_FAST                'size'
              356  BINARY_ADD       
              358  STORE_FAST               'data_end'

 L. 235       360  LOAD_GLOBAL              i32
              362  LOAD_FAST                'read'
              364  LOAD_CONST               4
              366  CALL_FUNCTION_1       1  ''
              368  CALL_FUNCTION_1       1  ''
              370  STORE_FAST               'length'

 L. 236       372  LOAD_FAST                'length'
          374_376  POP_JUMP_IF_FALSE   396  'to 396'

 L. 237       378  LOAD_DEREF               'fp'
              380  LOAD_METHOD              seek
              382  LOAD_FAST                'length'
              384  LOAD_CONST               16
              386  BINARY_SUBTRACT  
              388  LOAD_GLOBAL              io
              390  LOAD_ATTR                SEEK_CUR
              392  CALL_METHOD_2         2  ''
              394  POP_TOP          
            396_0  COME_FROM           374  '374'

 L. 238       396  LOAD_FAST                'combined'
              398  LOAD_FAST                'length'
              400  LOAD_CONST               4
              402  BINARY_ADD       
              404  INPLACE_ADD      
              406  STORE_FAST               'combined'

 L. 240       408  LOAD_GLOBAL              i32
              410  LOAD_FAST                'read'
              412  LOAD_CONST               4
              414  CALL_FUNCTION_1       1  ''
              416  CALL_FUNCTION_1       1  ''
              418  STORE_FAST               'length'

 L. 241       420  LOAD_FAST                'length'
          422_424  POP_JUMP_IF_FALSE   440  'to 440'

 L. 242       426  LOAD_DEREF               'fp'
              428  LOAD_METHOD              seek
              430  LOAD_FAST                'length'
              432  LOAD_GLOBAL              io
              434  LOAD_ATTR                SEEK_CUR
              436  CALL_METHOD_2         2  ''
              438  POP_TOP          
            440_0  COME_FROM           422  '422'

 L. 243       440  LOAD_FAST                'combined'
              442  LOAD_FAST                'length'
              444  LOAD_CONST               4
              446  BINARY_ADD       
              448  INPLACE_ADD      
              450  STORE_FAST               'combined'

 L. 245       452  LOAD_GLOBAL              i8
              454  LOAD_FAST                'read'
              456  LOAD_CONST               1
              458  CALL_FUNCTION_1       1  ''
              460  CALL_FUNCTION_1       1  ''
              462  STORE_FAST               'length'

 L. 246       464  LOAD_FAST                'length'
          466_468  POP_JUMP_IF_FALSE   486  'to 486'

 L. 249       470  LOAD_FAST                'read'
              472  LOAD_FAST                'length'
              474  CALL_FUNCTION_1       1  ''
              476  LOAD_METHOD              decode
              478  LOAD_STR                 'latin-1'
              480  LOAD_STR                 'replace'
              482  CALL_METHOD_2         2  ''
              484  STORE_FAST               'name'
            486_0  COME_FROM           466  '466'

 L. 250       486  LOAD_FAST                'combined'
              488  LOAD_FAST                'length'
              490  LOAD_CONST               1
              492  BINARY_ADD       
              494  INPLACE_ADD      
              496  STORE_FAST               'combined'

 L. 252       498  LOAD_DEREF               'fp'
              500  LOAD_METHOD              seek
              502  LOAD_FAST                'data_end'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
            508_0  COME_FROM           344  '344'

 L. 253       508  LOAD_FAST                'layers'
              510  LOAD_METHOD              append
              512  LOAD_FAST                'name'
              514  LOAD_FAST                'mode'
              516  LOAD_FAST                'x0'
              518  LOAD_FAST                'y0'
              520  LOAD_FAST                'x1'
              522  LOAD_FAST                'y1'
              524  BUILD_TUPLE_4         4 
              526  BUILD_TUPLE_3         3 
              528  CALL_METHOD_1         1  ''
              530  POP_TOP          
              532  JUMP_BACK            64  'to 64'
            534_0  COME_FROM            64  '64'

 L. 256       534  LOAD_CONST               0
              536  STORE_FAST               'i'

 L. 257       538  LOAD_FAST                'layers'
              540  GET_ITER         
            542_0  COME_FROM           622  '622'
              542  FOR_ITER            626  'to 626'
              544  UNPACK_SEQUENCE_3     3 
              546  STORE_FAST               'name'
              548  STORE_FAST               'mode'
              550  STORE_FAST               'bbox'

 L. 258       552  BUILD_LIST_0          0 
              554  STORE_FAST               'tile'

 L. 259       556  LOAD_FAST                'mode'
              558  GET_ITER         
            560_0  COME_FROM           594  '594'
            560_1  COME_FROM           580  '580'
              560  FOR_ITER            598  'to 598'
              562  STORE_FAST               'm'

 L. 260       564  LOAD_GLOBAL              _maketile
              566  LOAD_DEREF               'fp'
              568  LOAD_FAST                'm'
              570  LOAD_FAST                'bbox'
              572  LOAD_CONST               1
              574  CALL_FUNCTION_4       4  ''
              576  STORE_FAST               't'

 L. 261       578  LOAD_FAST                't'
          580_582  POP_JUMP_IF_FALSE_BACK   560  'to 560'

 L. 262       584  LOAD_FAST                'tile'
              586  LOAD_METHOD              extend
              588  LOAD_FAST                't'
              590  CALL_METHOD_1         1  ''
              592  POP_TOP          
          594_596  JUMP_BACK           560  'to 560'
            598_0  COME_FROM           560  '560'

 L. 263       598  LOAD_FAST                'name'
              600  LOAD_FAST                'mode'
              602  LOAD_FAST                'bbox'
              604  LOAD_FAST                'tile'
              606  BUILD_TUPLE_4         4 
              608  LOAD_FAST                'layers'
              610  LOAD_FAST                'i'
              612  STORE_SUBSCR     

 L. 264       614  LOAD_FAST                'i'
              616  LOAD_CONST               1
              618  INPLACE_ADD      
              620  STORE_FAST               'i'
          622_624  JUMP_BACK           542  'to 542'
            626_0  COME_FROM           542  '542'

 L. 266       626  LOAD_FAST                'layers'
              628  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 276


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
            else:
                tile.append(('raw', bbox, offset, layer))
                offset = offset + xsize * ysize

    else:
        pass
    if compression == 1:
        i = 0
        tile = []
        bytecount = read(channels * ysize * 2)
        offset = file.tell()
        for channel in range(channels):
            layer = mode[channel]
            if mode == 'CMYK':
                layer += ';I'
            else:
                tile.append(('packbits', bbox, offset, layer))
                for y in range(ysize):
                    offset = offset + i16(bytecount, i)
                    i += 2

        else:
            file.seek(offset)
            if offset & 1:
                read(1)

        return tile


Image.register_open(PsdImageFile.format, PsdImageFile, _accept)
Image.register_extension(PsdImageFile.format, '.psd')
Image.register_mime(PsdImageFile.format, 'image/vnd.adobe.photoshop')