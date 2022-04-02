# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\FpxImagePlugin.py
import olefile
from . import Image, ImageFile
from ._binary import i8
from ._binary import i32le as i32
MODES = {32766:('A', 'L'), 
 (65536,):('L', 'L'), 
 (98304, 98302):('RGBA', 'LA'), 
 (131072, 131073, 131074):('RGB', 'YCC;P'), 
 (163840, 163841, 163842, 163838):('RGBA', 'YCCA;P'), 
 (196608, 196609, 196610):('RGB', 'RGB'), 
 (229376, 229377, 229378, 229374):('RGBA', 'RGBA')}

def _accept(prefix):
    return prefix[:8] == olefile.MAGIC


class FpxImageFile(ImageFile.ImageFile):
    format = 'FPX'
    format_description = 'FlashPix'

    def _open(self):
        try:
            self.ole = olefile.OleFileIO(self.fp)
        except OSError as e:
            try:
                raise SyntaxError('not an FPX file; invalid OLE file') from e
            finally:
                e = None
                del e

        else:
            if self.ole.root.clsid != '56616700-C154-11CE-8553-00AA00A1F95B':
                raise SyntaxError('not an FPX file; bad root CLSID')
            self._open_index(1)

    def _open_index(self, index=1):
        prop = self.ole.getproperties([
         f"Data Object Store {index:06d}", '\x05Image Contents'])
        self._size = (
         prop[16777218], prop[16777219])
        size = max(self.size)
        i = 1
        while size > 64:
            size = size / 2
            i += 1

        self.maxid = i - 1
        id = self.maxid << 16
        s = prop[(33554434 | id)]
        colors = []
        bands = i32(s, 4)
        if bands > 4:
            raise OSError('Invalid number of bands')
        for i in range(bands):
            colors.append(i32(s, 8 + i * 4) & 2147483647)
        else:
            self.mode, self.rawmode = MODES[tuple(colors)]
            self.jpeg = {}
            for i in range(256):
                id = 50331649 | i << 16
                if id in prop:
                    self.jpeg[i] = prop[id]
            else:
                self._open_subimage(1, self.maxid)

    def _open_subimage--- This code section failed: ---

 L. 124         0  LOAD_STR                 'Data Object Store '
                2  LOAD_FAST                'index'
                4  LOAD_STR                 '06d'
                6  FORMAT_VALUE_ATTR     4  ''
                8  BUILD_STRING_2        2 

 L. 125        10  LOAD_STR                 'Resolution '
               12  LOAD_FAST                'subimage'
               14  LOAD_STR                 '04d'
               16  FORMAT_VALUE_ATTR     4  ''
               18  BUILD_STRING_2        2 

 L. 126        20  LOAD_STR                 'Subimage 0000 Header'

 L. 123        22  BUILD_LIST_3          3 
               24  STORE_FAST               'stream'

 L. 129        26  LOAD_FAST                'self'
               28  LOAD_ATTR                ole
               30  LOAD_METHOD              openstream
               32  LOAD_FAST                'stream'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'fp'

 L. 132        38  LOAD_FAST                'fp'
               40  LOAD_METHOD              read
               42  LOAD_CONST               28
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 135        48  LOAD_FAST                'fp'
               50  LOAD_METHOD              read
               52  LOAD_CONST               36
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               's'

 L. 137        58  LOAD_GLOBAL              i32
               60  LOAD_FAST                's'
               62  LOAD_CONST               4
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_GLOBAL              i32
               68  LOAD_FAST                's'
               70  LOAD_CONST               8
               72  CALL_FUNCTION_2       2  ''
               74  BUILD_TUPLE_2         2 
               76  STORE_FAST               'size'

 L. 139        78  LOAD_GLOBAL              i32
               80  LOAD_FAST                's'
               82  LOAD_CONST               16
               84  CALL_FUNCTION_2       2  ''
               86  LOAD_GLOBAL              i32
               88  LOAD_FAST                's'
               90  LOAD_CONST               20
               92  CALL_FUNCTION_2       2  ''
               94  BUILD_TUPLE_2         2 
               96  STORE_FAST               'tilesize'

 L. 141        98  LOAD_GLOBAL              i32
              100  LOAD_FAST                's'
              102  LOAD_CONST               28
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'offset'

 L. 142       108  LOAD_GLOBAL              i32
              110  LOAD_FAST                's'
              112  LOAD_CONST               32
              114  CALL_FUNCTION_2       2  ''
              116  STORE_FAST               'length'

 L. 144       118  LOAD_FAST                'size'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                size
              124  COMPARE_OP               !=
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 145       128  LOAD_GLOBAL              OSError
              130  LOAD_STR                 'subimage mismatch'
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L. 148       136  LOAD_FAST                'fp'
              138  LOAD_METHOD              seek
              140  LOAD_CONST               28
              142  LOAD_FAST                'offset'
              144  BINARY_ADD       
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 149       150  LOAD_FAST                'fp'
              152  LOAD_METHOD              read
              154  LOAD_GLOBAL              i32
              156  LOAD_FAST                's'
              158  LOAD_CONST               12
              160  CALL_FUNCTION_2       2  ''
              162  LOAD_FAST                'length'
              164  BINARY_MULTIPLY  
              166  CALL_METHOD_1         1  ''
              168  STORE_FAST               's'

 L. 151       170  LOAD_CONST               0
              172  DUP_TOP          
              174  STORE_FAST               'x'
              176  STORE_FAST               'y'

 L. 152       178  LOAD_FAST                'size'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'xsize'
              184  STORE_FAST               'ysize'

 L. 153       186  LOAD_FAST                'tilesize'
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'xtile'
              192  STORE_FAST               'ytile'

 L. 154       194  BUILD_LIST_0          0 
              196  LOAD_FAST                'self'
              198  STORE_ATTR               tile

 L. 156       200  LOAD_GLOBAL              range
              202  LOAD_CONST               0
              204  LOAD_GLOBAL              len
              206  LOAD_FAST                's'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_FAST                'length'
              212  CALL_FUNCTION_3       3  ''
              214  GET_ITER         
            216_0  COME_FROM           558  '558'
            216_1  COME_FROM           536  '536'
          216_218  FOR_ITER            568  'to 568'
              220  STORE_FAST               'i'

 L. 158       222  LOAD_GLOBAL              i32
              224  LOAD_FAST                's'
              226  LOAD_FAST                'i'
              228  LOAD_CONST               8
              230  BINARY_ADD       
              232  CALL_FUNCTION_2       2  ''
              234  STORE_FAST               'compression'

 L. 160       236  LOAD_FAST                'compression'
              238  LOAD_CONST               0
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   296  'to 296'

 L. 161       246  LOAD_FAST                'self'
              248  LOAD_ATTR                tile
              250  LOAD_METHOD              append

 L. 163       252  LOAD_STR                 'raw'

 L. 164       254  LOAD_FAST                'x'
              256  LOAD_FAST                'y'
              258  LOAD_FAST                'x'
              260  LOAD_FAST                'xtile'
              262  BINARY_ADD       
              264  LOAD_FAST                'y'
              266  LOAD_FAST                'ytile'
              268  BINARY_ADD       
              270  BUILD_TUPLE_4         4 

 L. 165       272  LOAD_GLOBAL              i32
              274  LOAD_FAST                's'
              276  LOAD_FAST                'i'
              278  CALL_FUNCTION_2       2  ''
              280  LOAD_CONST               28
              282  BINARY_ADD       

 L. 166       284  LOAD_FAST                'self'
              286  LOAD_ATTR                rawmode

 L. 162       288  BUILD_TUPLE_4         4 

 L. 161       290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  JUMP_FORWARD        522  'to 522'
            296_0  COME_FROM           242  '242'

 L. 170       296  LOAD_FAST                'compression'
              298  LOAD_CONST               1
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   368  'to 368'

 L. 173       306  LOAD_FAST                'self'
              308  LOAD_ATTR                tile
              310  LOAD_METHOD              append

 L. 175       312  LOAD_STR                 'fill'

 L. 176       314  LOAD_FAST                'x'
              316  LOAD_FAST                'y'
              318  LOAD_FAST                'x'
              320  LOAD_FAST                'xtile'
              322  BINARY_ADD       
              324  LOAD_FAST                'y'
              326  LOAD_FAST                'ytile'
              328  BINARY_ADD       
              330  BUILD_TUPLE_4         4 

 L. 177       332  LOAD_GLOBAL              i32
              334  LOAD_FAST                's'
              336  LOAD_FAST                'i'
              338  CALL_FUNCTION_2       2  ''
              340  LOAD_CONST               28
              342  BINARY_ADD       

 L. 178       344  LOAD_FAST                'self'
              346  LOAD_ATTR                rawmode
              348  LOAD_FAST                's'
              350  LOAD_CONST               12
              352  LOAD_CONST               16
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  BUILD_TUPLE_2         2 

 L. 174       360  BUILD_TUPLE_4         4 

 L. 173       362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  JUMP_FORWARD        522  'to 522'
            368_0  COME_FROM           302  '302'

 L. 182       368  LOAD_FAST                'compression'
              370  LOAD_CONST               2
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   514  'to 514'

 L. 184       378  LOAD_GLOBAL              i8
              380  LOAD_FAST                's'
              382  LOAD_CONST               14
              384  BINARY_SUBSCR    
              386  CALL_FUNCTION_1       1  ''
              388  STORE_FAST               'internal_color_conversion'

 L. 185       390  LOAD_GLOBAL              i8
              392  LOAD_FAST                's'
              394  LOAD_CONST               15
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  ''
              400  STORE_FAST               'jpeg_tables'

 L. 186       402  LOAD_FAST                'self'
              404  LOAD_ATTR                rawmode
              406  STORE_FAST               'rawmode'

 L. 188       408  LOAD_FAST                'internal_color_conversion'
          410_412  POP_JUMP_IF_FALSE   440  'to 440'

 L. 190       414  LOAD_FAST                'rawmode'
              416  LOAD_STR                 'RGBA'
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   434  'to 434'

 L. 194       424  LOAD_CONST               ('YCbCrK', 'CMYK')
              426  UNPACK_SEQUENCE_2     2 
              428  STORE_FAST               'jpegmode'
              430  STORE_FAST               'rawmode'
              432  JUMP_FORWARD        438  'to 438'
            434_0  COME_FROM           420  '420'

 L. 196       434  LOAD_CONST               None
              436  STORE_FAST               'jpegmode'
            438_0  COME_FROM           432  '432'
              438  JUMP_FORWARD        444  'to 444'
            440_0  COME_FROM           410  '410'

 L. 200       440  LOAD_FAST                'rawmode'
              442  STORE_FAST               'jpegmode'
            444_0  COME_FROM           438  '438'

 L. 202       444  LOAD_FAST                'self'
              446  LOAD_ATTR                tile
              448  LOAD_METHOD              append

 L. 204       450  LOAD_STR                 'jpeg'

 L. 205       452  LOAD_FAST                'x'
              454  LOAD_FAST                'y'
              456  LOAD_FAST                'x'
              458  LOAD_FAST                'xtile'
              460  BINARY_ADD       
              462  LOAD_FAST                'y'
              464  LOAD_FAST                'ytile'
              466  BINARY_ADD       
              468  BUILD_TUPLE_4         4 

 L. 206       470  LOAD_GLOBAL              i32
              472  LOAD_FAST                's'
              474  LOAD_FAST                'i'
              476  CALL_FUNCTION_2       2  ''
              478  LOAD_CONST               28
              480  BINARY_ADD       

 L. 207       482  LOAD_FAST                'rawmode'
              484  LOAD_FAST                'jpegmode'
              486  BUILD_TUPLE_2         2 

 L. 203       488  BUILD_TUPLE_4         4 

 L. 202       490  CALL_METHOD_1         1  ''
              492  POP_TOP          

 L. 214       494  LOAD_FAST                'jpeg_tables'
          496_498  POP_JUMP_IF_FALSE   522  'to 522'

 L. 215       500  LOAD_FAST                'self'
              502  LOAD_ATTR                jpeg
              504  LOAD_FAST                'jpeg_tables'
              506  BINARY_SUBSCR    
              508  LOAD_FAST                'self'
              510  STORE_ATTR               tile_prefix
              512  JUMP_FORWARD        522  'to 522'
            514_0  COME_FROM           374  '374'

 L. 218       514  LOAD_GLOBAL              OSError
              516  LOAD_STR                 'unknown/invalid compression'
              518  CALL_FUNCTION_1       1  ''
              520  RAISE_VARARGS_1       1  'exception instance'
            522_0  COME_FROM           512  '512'
            522_1  COME_FROM           496  '496'
            522_2  COME_FROM           366  '366'
            522_3  COME_FROM           294  '294'

 L. 220       522  LOAD_FAST                'x'
              524  LOAD_FAST                'xtile'
              526  BINARY_ADD       
              528  STORE_FAST               'x'

 L. 221       530  LOAD_FAST                'x'
              532  LOAD_FAST                'xsize'
              534  COMPARE_OP               >=
              536  POP_JUMP_IF_FALSE   216  'to 216'

 L. 222       538  LOAD_CONST               0
              540  LOAD_FAST                'y'
              542  LOAD_FAST                'ytile'
              544  BINARY_ADD       
              546  ROT_TWO          
              548  STORE_FAST               'x'
              550  STORE_FAST               'y'

 L. 223       552  LOAD_FAST                'y'
              554  LOAD_FAST                'ysize'
              556  COMPARE_OP               >=
              558  POP_JUMP_IF_FALSE   216  'to 216'

 L. 224       560  POP_TOP          
          562_564  JUMP_ABSOLUTE       568  'to 568'
              566  JUMP_BACK           216  'to 216'

 L. 226       568  LOAD_FAST                'stream'
              570  LOAD_FAST                'self'
              572  STORE_ATTR               stream

 L. 227       574  LOAD_CONST               None
              576  LOAD_FAST                'self'
              578  STORE_ATTR               fp

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 562_564

    def load(self):
        if not self.fp:
            self.fp = self.ole.openstream(self.stream[:2] + ['Subimage 0000 Data'])
        return ImageFile.ImageFile.load(self)


Image.register_open(FpxImageFile.format, FpxImageFile, _accept)
Image.register_extension(FpxImageFile.format, '.fpx')