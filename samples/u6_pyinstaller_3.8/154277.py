# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\FpxImagePlugin.py
import olefile
from . import Image, ImageFile
from ._binary import i8, i32le as i32
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
         'Data Object Store %06d' % index, '\x05Image Contents'])
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

 L. 123         0  LOAD_STR                 'Data Object Store %06d'
                2  LOAD_FAST                'index'
                4  BINARY_MODULO    

 L. 124         6  LOAD_STR                 'Resolution %04d'
                8  LOAD_FAST                'subimage'
               10  BINARY_MODULO    

 L. 125        12  LOAD_STR                 'Subimage 0000 Header'

 L. 122        14  BUILD_LIST_3          3 
               16  STORE_FAST               'stream'

 L. 128        18  LOAD_FAST                'self'
               20  LOAD_ATTR                ole
               22  LOAD_METHOD              openstream
               24  LOAD_FAST                'stream'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'fp'

 L. 131        30  LOAD_FAST                'fp'
               32  LOAD_METHOD              read
               34  LOAD_CONST               28
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 134        40  LOAD_FAST                'fp'
               42  LOAD_METHOD              read
               44  LOAD_CONST               36
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               's'

 L. 136        50  LOAD_GLOBAL              i32
               52  LOAD_FAST                's'
               54  LOAD_CONST               4
               56  CALL_FUNCTION_2       2  ''
               58  LOAD_GLOBAL              i32
               60  LOAD_FAST                's'
               62  LOAD_CONST               8
               64  CALL_FUNCTION_2       2  ''
               66  BUILD_TUPLE_2         2 
               68  STORE_FAST               'size'

 L. 138        70  LOAD_GLOBAL              i32
               72  LOAD_FAST                's'
               74  LOAD_CONST               16
               76  CALL_FUNCTION_2       2  ''
               78  LOAD_GLOBAL              i32
               80  LOAD_FAST                's'
               82  LOAD_CONST               20
               84  CALL_FUNCTION_2       2  ''
               86  BUILD_TUPLE_2         2 
               88  STORE_FAST               'tilesize'

 L. 140        90  LOAD_GLOBAL              i32
               92  LOAD_FAST                's'
               94  LOAD_CONST               28
               96  CALL_FUNCTION_2       2  ''
               98  STORE_FAST               'offset'

 L. 141       100  LOAD_GLOBAL              i32
              102  LOAD_FAST                's'
              104  LOAD_CONST               32
              106  CALL_FUNCTION_2       2  ''
              108  STORE_FAST               'length'

 L. 143       110  LOAD_FAST                'size'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                size
              116  COMPARE_OP               !=
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 144       120  LOAD_GLOBAL              OSError
              122  LOAD_STR                 'subimage mismatch'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 147       128  LOAD_FAST                'fp'
              130  LOAD_METHOD              seek
              132  LOAD_CONST               28
              134  LOAD_FAST                'offset'
              136  BINARY_ADD       
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 148       142  LOAD_FAST                'fp'
              144  LOAD_METHOD              read
              146  LOAD_GLOBAL              i32
              148  LOAD_FAST                's'
              150  LOAD_CONST               12
              152  CALL_FUNCTION_2       2  ''
              154  LOAD_FAST                'length'
              156  BINARY_MULTIPLY  
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               's'

 L. 150       162  LOAD_CONST               0
              164  DUP_TOP          
              166  STORE_FAST               'x'
              168  STORE_FAST               'y'

 L. 151       170  LOAD_FAST                'size'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               'xsize'
              176  STORE_FAST               'ysize'

 L. 152       178  LOAD_FAST                'tilesize'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'xtile'
              184  STORE_FAST               'ytile'

 L. 153       186  BUILD_LIST_0          0 
              188  LOAD_FAST                'self'
              190  STORE_ATTR               tile

 L. 155       192  LOAD_GLOBAL              range
              194  LOAD_CONST               0
              196  LOAD_GLOBAL              len
              198  LOAD_FAST                's'
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_FAST                'length'
              204  CALL_FUNCTION_3       3  ''
              206  GET_ITER         
            208_0  COME_FROM           550  '550'
            208_1  COME_FROM           528  '528'
          208_210  FOR_ITER            560  'to 560'
              212  STORE_FAST               'i'

 L. 157       214  LOAD_GLOBAL              i32
              216  LOAD_FAST                's'
              218  LOAD_FAST                'i'
              220  LOAD_CONST               8
              222  BINARY_ADD       
              224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'compression'

 L. 159       228  LOAD_FAST                'compression'
              230  LOAD_CONST               0
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   288  'to 288'

 L. 160       238  LOAD_FAST                'self'
              240  LOAD_ATTR                tile
              242  LOAD_METHOD              append

 L. 162       244  LOAD_STR                 'raw'

 L. 163       246  LOAD_FAST                'x'
              248  LOAD_FAST                'y'
              250  LOAD_FAST                'x'
              252  LOAD_FAST                'xtile'
              254  BINARY_ADD       
              256  LOAD_FAST                'y'
              258  LOAD_FAST                'ytile'
              260  BINARY_ADD       
              262  BUILD_TUPLE_4         4 

 L. 164       264  LOAD_GLOBAL              i32
              266  LOAD_FAST                's'
              268  LOAD_FAST                'i'
              270  CALL_FUNCTION_2       2  ''
              272  LOAD_CONST               28
              274  BINARY_ADD       

 L. 165       276  LOAD_FAST                'self'
              278  LOAD_ATTR                rawmode

 L. 161       280  BUILD_TUPLE_4         4 

 L. 160       282  CALL_METHOD_1         1  ''
              284  POP_TOP          
              286  JUMP_FORWARD        514  'to 514'
            288_0  COME_FROM           234  '234'

 L. 169       288  LOAD_FAST                'compression'
              290  LOAD_CONST               1
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   360  'to 360'

 L. 172       298  LOAD_FAST                'self'
              300  LOAD_ATTR                tile
              302  LOAD_METHOD              append

 L. 174       304  LOAD_STR                 'fill'

 L. 175       306  LOAD_FAST                'x'
              308  LOAD_FAST                'y'
              310  LOAD_FAST                'x'
              312  LOAD_FAST                'xtile'
              314  BINARY_ADD       
              316  LOAD_FAST                'y'
              318  LOAD_FAST                'ytile'
              320  BINARY_ADD       
              322  BUILD_TUPLE_4         4 

 L. 176       324  LOAD_GLOBAL              i32
              326  LOAD_FAST                's'
              328  LOAD_FAST                'i'
              330  CALL_FUNCTION_2       2  ''
              332  LOAD_CONST               28
              334  BINARY_ADD       

 L. 177       336  LOAD_FAST                'self'
              338  LOAD_ATTR                rawmode
              340  LOAD_FAST                's'
              342  LOAD_CONST               12
              344  LOAD_CONST               16
              346  BUILD_SLICE_2         2 
              348  BINARY_SUBSCR    
              350  BUILD_TUPLE_2         2 

 L. 173       352  BUILD_TUPLE_4         4 

 L. 172       354  CALL_METHOD_1         1  ''
              356  POP_TOP          
              358  JUMP_FORWARD        514  'to 514'
            360_0  COME_FROM           294  '294'

 L. 181       360  LOAD_FAST                'compression'
              362  LOAD_CONST               2
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   506  'to 506'

 L. 183       370  LOAD_GLOBAL              i8
              372  LOAD_FAST                's'
              374  LOAD_CONST               14
              376  BINARY_SUBSCR    
              378  CALL_FUNCTION_1       1  ''
              380  STORE_FAST               'internal_color_conversion'

 L. 184       382  LOAD_GLOBAL              i8
              384  LOAD_FAST                's'
              386  LOAD_CONST               15
              388  BINARY_SUBSCR    
              390  CALL_FUNCTION_1       1  ''
              392  STORE_FAST               'jpeg_tables'

 L. 185       394  LOAD_FAST                'self'
              396  LOAD_ATTR                rawmode
              398  STORE_FAST               'rawmode'

 L. 187       400  LOAD_FAST                'internal_color_conversion'
          402_404  POP_JUMP_IF_FALSE   432  'to 432'

 L. 189       406  LOAD_FAST                'rawmode'
              408  LOAD_STR                 'RGBA'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   426  'to 426'

 L. 193       416  LOAD_CONST               ('YCbCrK', 'CMYK')
              418  UNPACK_SEQUENCE_2     2 
              420  STORE_FAST               'jpegmode'
              422  STORE_FAST               'rawmode'
              424  JUMP_FORWARD        430  'to 430'
            426_0  COME_FROM           412  '412'

 L. 195       426  LOAD_CONST               None
              428  STORE_FAST               'jpegmode'
            430_0  COME_FROM           424  '424'
              430  JUMP_FORWARD        436  'to 436'
            432_0  COME_FROM           402  '402'

 L. 199       432  LOAD_FAST                'rawmode'
              434  STORE_FAST               'jpegmode'
            436_0  COME_FROM           430  '430'

 L. 201       436  LOAD_FAST                'self'
              438  LOAD_ATTR                tile
              440  LOAD_METHOD              append

 L. 203       442  LOAD_STR                 'jpeg'

 L. 204       444  LOAD_FAST                'x'
              446  LOAD_FAST                'y'
              448  LOAD_FAST                'x'
              450  LOAD_FAST                'xtile'
              452  BINARY_ADD       
              454  LOAD_FAST                'y'
              456  LOAD_FAST                'ytile'
              458  BINARY_ADD       
              460  BUILD_TUPLE_4         4 

 L. 205       462  LOAD_GLOBAL              i32
              464  LOAD_FAST                's'
              466  LOAD_FAST                'i'
              468  CALL_FUNCTION_2       2  ''
              470  LOAD_CONST               28
              472  BINARY_ADD       

 L. 206       474  LOAD_FAST                'rawmode'
              476  LOAD_FAST                'jpegmode'
              478  BUILD_TUPLE_2         2 

 L. 202       480  BUILD_TUPLE_4         4 

 L. 201       482  CALL_METHOD_1         1  ''
              484  POP_TOP          

 L. 213       486  LOAD_FAST                'jpeg_tables'
          488_490  POP_JUMP_IF_FALSE   514  'to 514'

 L. 214       492  LOAD_FAST                'self'
              494  LOAD_ATTR                jpeg
              496  LOAD_FAST                'jpeg_tables'
              498  BINARY_SUBSCR    
              500  LOAD_FAST                'self'
              502  STORE_ATTR               tile_prefix
              504  JUMP_FORWARD        514  'to 514'
            506_0  COME_FROM           366  '366'

 L. 217       506  LOAD_GLOBAL              OSError
              508  LOAD_STR                 'unknown/invalid compression'
              510  CALL_FUNCTION_1       1  ''
              512  RAISE_VARARGS_1       1  'exception instance'
            514_0  COME_FROM           504  '504'
            514_1  COME_FROM           488  '488'
            514_2  COME_FROM           358  '358'
            514_3  COME_FROM           286  '286'

 L. 219       514  LOAD_FAST                'x'
              516  LOAD_FAST                'xtile'
              518  BINARY_ADD       
              520  STORE_FAST               'x'

 L. 220       522  LOAD_FAST                'x'
              524  LOAD_FAST                'xsize'
              526  COMPARE_OP               >=
              528  POP_JUMP_IF_FALSE   208  'to 208'

 L. 221       530  LOAD_CONST               0
              532  LOAD_FAST                'y'
              534  LOAD_FAST                'ytile'
              536  BINARY_ADD       
              538  ROT_TWO          
              540  STORE_FAST               'x'
              542  STORE_FAST               'y'

 L. 222       544  LOAD_FAST                'y'
              546  LOAD_FAST                'ysize'
              548  COMPARE_OP               >=
              550  POP_JUMP_IF_FALSE   208  'to 208'

 L. 223       552  POP_TOP          
          554_556  JUMP_ABSOLUTE       560  'to 560'
              558  JUMP_BACK           208  'to 208'

 L. 225       560  LOAD_FAST                'stream'
              562  LOAD_FAST                'self'
              564  STORE_ATTR               stream

 L. 226       566  LOAD_CONST               None
              568  LOAD_FAST                'self'
              570  STORE_ATTR               fp

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 554_556

    def load(self):
        if not self.fp:
            self.fp = self.ole.openstream(self.stream[:2] + ['Subimage 0000 Data'])
        return ImageFile.ImageFile.load(self)


Image.register_open(FpxImageFile.format, FpxImageFile, _accept)
Image.register_extension(FpxImageFile.format, '.fpx')