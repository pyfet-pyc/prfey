# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\GifImagePlugin.py
import itertools, math, os, subprocess
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
from ._binary import i8
from ._binary import i16le as i16
from ._binary import o8
from ._binary import o16le as o16

def _accept(prefix):
    return prefix[:6] in (b'GIF87a', b'GIF89a')


class GifImageFile(ImageFile.ImageFile):
    format = 'GIF'
    format_description = 'Compuserve GIF'
    _close_exclusive_fp_after_loading = False
    global_palette = None

    def data(self):
        s = self.fp.read(1)
        if s:
            if i8(s):
                return self.fp.read(i8(s))

    def _open--- This code section failed: ---

 L.  68         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               13
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  69        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L.  70        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a GIF file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  72        28  LOAD_FAST                's'
               30  LOAD_CONST               None
               32  LOAD_CONST               6
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                info
               42  LOAD_STR                 'version'
               44  STORE_SUBSCR     

 L.  73        46  LOAD_GLOBAL              i16
               48  LOAD_FAST                's'
               50  LOAD_CONST               6
               52  LOAD_CONST               None
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_GLOBAL              i16
               62  LOAD_FAST                's'
               64  LOAD_CONST               8
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  ''
               74  BUILD_TUPLE_2         2 
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _size

 L.  74        80  BUILD_LIST_0          0 
               82  LOAD_FAST                'self'
               84  STORE_ATTR               tile

 L.  75        86  LOAD_GLOBAL              i8
               88  LOAD_FAST                's'
               90  LOAD_CONST               10
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'flags'

 L.  76        98  LOAD_FAST                'flags'
              100  LOAD_CONST               7
              102  BINARY_AND       
              104  LOAD_CONST               1
              106  BINARY_ADD       
              108  STORE_FAST               'bits'

 L.  78       110  LOAD_FAST                'flags'
              112  LOAD_CONST               128
              114  BINARY_AND       
          116_118  POP_JUMP_IF_FALSE   274  'to 274'

 L.  80       120  LOAD_GLOBAL              i8
              122  LOAD_FAST                's'
              124  LOAD_CONST               11
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                info
              134  LOAD_STR                 'background'
              136  STORE_SUBSCR     

 L.  82       138  LOAD_FAST                'self'
              140  LOAD_ATTR                fp
              142  LOAD_METHOD              read
              144  LOAD_CONST               3
              146  LOAD_FAST                'bits'
              148  BINARY_LSHIFT    
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'p'

 L.  83       154  LOAD_GLOBAL              range
              156  LOAD_CONST               0
              158  LOAD_GLOBAL              len
              160  LOAD_FAST                'p'
              162  CALL_FUNCTION_1       1  ''
              164  LOAD_CONST               3
              166  CALL_FUNCTION_3       3  ''
              168  GET_ITER         
            170_0  COME_FROM           272  '272'
            170_1  COME_FROM           236  '236'
              170  FOR_ITER            274  'to 274'
              172  STORE_FAST               'i'

 L.  84       174  LOAD_FAST                'i'
              176  LOAD_CONST               3
              178  BINARY_FLOOR_DIVIDE
              180  LOAD_GLOBAL              i8
              182  LOAD_FAST                'p'
              184  LOAD_FAST                'i'
              186  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  ''
              190  DUP_TOP          
              192  ROT_THREE        
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   240  'to 240'
              198  LOAD_GLOBAL              i8
              200  LOAD_FAST                'p'
              202  LOAD_FAST                'i'
              204  LOAD_CONST               1
              206  BINARY_ADD       
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  ''
              212  DUP_TOP          
              214  ROT_THREE        
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   240  'to 240'
              220  LOAD_GLOBAL              i8
              222  LOAD_FAST                'p'
              224  LOAD_FAST                'i'
              226  LOAD_CONST               2
              228  BINARY_ADD       
              230  BINARY_SUBSCR    
              232  CALL_FUNCTION_1       1  ''
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_TRUE_BACK   170  'to 170'
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           218  '218'
            240_1  COME_FROM           196  '196'
              240  POP_TOP          
            242_0  COME_FROM           238  '238'

 L.  85       242  LOAD_GLOBAL              ImagePalette
              244  LOAD_METHOD              raw
              246  LOAD_STR                 'RGB'
              248  LOAD_FAST                'p'
              250  CALL_METHOD_2         2  ''
              252  STORE_FAST               'p'

 L.  86       254  LOAD_FAST                'p'
              256  DUP_TOP          
              258  LOAD_FAST                'self'
              260  STORE_ATTR               global_palette
              262  LOAD_FAST                'self'
              264  STORE_ATTR               palette

 L.  87       266  POP_TOP          
          268_270  BREAK_LOOP          274  'to 274'
              272  JUMP_BACK           170  'to 170'
            274_0  COME_FROM           268  '268'
            274_1  COME_FROM           170  '170'
            274_2  COME_FROM           116  '116'

 L.  89       274  LOAD_FAST                'self'
              276  LOAD_ATTR                fp
              278  LOAD_FAST                'self'
              280  STORE_ATTR               _GifImageFile__fp

 L.  90       282  LOAD_FAST                'self'
              284  LOAD_ATTR                fp
              286  LOAD_METHOD              tell
              288  CALL_METHOD_0         0  ''
              290  LOAD_FAST                'self'
              292  STORE_ATTR               _GifImageFile__rewind

 L.  91       294  LOAD_CONST               None
              296  LOAD_FAST                'self'
              298  STORE_ATTR               _n_frames

 L.  92       300  LOAD_CONST               None
              302  LOAD_FAST                'self'
              304  STORE_ATTR               _is_animated

 L.  93       306  LOAD_FAST                'self'
              308  LOAD_METHOD              _seek
              310  LOAD_CONST               0
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 240_1

    @property
    def n_frames(self):
        if self._n_frames is None:
            current = self.tell
            try:
                while True:
                    self.seek(self.tell + 1)

            except EOFError:
                self._n_frames = self.tell + 1
            else:
                self.seek(current)
            return self._n_frames

    @property
    def is_animated(self):
        if self._is_animated is None:
            if self._n_frames is not None:
                self._is_animated = self._n_frames != 1
            else:
                current = self.tell
                try:
                    self.seek(1)
                    self._is_animated = True
                except EOFError:
                    self._is_animated = False
                else:
                    self.seek(current)
            return self._is_animated

    def seek(self, frame):
        if not self._seek_check(frame):
            return
        if frame < self._GifImageFile__frame:
            if frame != 0:
                self.im = None
            self._seek(0)
        last_frame = self._GifImageFile__frame
        for f in range(self._GifImageFile__frame + 1, frame + 1):
            try:
                self._seek(f)
            except EOFError as e:
                try:
                    self.seek(last_frame)
                    raise EOFError('no more images in GIF file') from e
                finally:
                    e = None
                    del e

    def _seek--- This code section failed: ---

 L. 142         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    68  'to 68'

 L. 144         8  LOAD_CONST               0
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _GifImageFile__offset

 L. 145        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               dispose

 L. 146        20  LOAD_CONST               0
               22  LOAD_CONST               0
               24  LOAD_CONST               0
               26  LOAD_CONST               0
               28  BUILD_LIST_4          4 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               dispose_extent

 L. 147        34  LOAD_CONST               -1
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _GifImageFile__frame

 L. 148        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _GifImageFile__fp
               44  LOAD_METHOD              seek
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _GifImageFile__rewind
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 149        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _prev_im

 L. 150        60  LOAD_CONST               0
               62  LOAD_FAST                'self'
               64  STORE_ATTR               disposal_method
               66  JUMP_FORWARD         82  'to 82'
             68_0  COME_FROM             6  '6'

 L. 153        68  LOAD_FAST                'self'
               70  LOAD_ATTR                im
               72  POP_JUMP_IF_TRUE     82  'to 82'

 L. 154        74  LOAD_FAST                'self'
               76  LOAD_METHOD              load
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            66  '66'

 L. 156        82  LOAD_FAST                'frame'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _GifImageFile__frame
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   110  'to 110'

 L. 157        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'cannot seek to frame '
              100  LOAD_FAST                'frame'
              102  FORMAT_VALUE          0  ''
              104  BUILD_STRING_2        2 
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            94  '94'

 L. 158       110  LOAD_FAST                'frame'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _GifImageFile__frame

 L. 160       116  BUILD_LIST_0          0 
              118  LOAD_FAST                'self'
              120  STORE_ATTR               tile

 L. 162       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _GifImageFile__fp
              126  LOAD_FAST                'self'
              128  STORE_ATTR               fp

 L. 163       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _GifImageFile__offset
              134  POP_JUMP_IF_FALSE   166  'to 166'

 L. 165       136  LOAD_FAST                'self'
              138  LOAD_ATTR                fp
              140  LOAD_METHOD              seek
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _GifImageFile__offset
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
            150_0  COME_FROM           158  '158'

 L. 166       150  LOAD_FAST                'self'
              152  LOAD_METHOD              data
              154  CALL_METHOD_0         0  ''
              156  POP_JUMP_IF_FALSE   160  'to 160'

 L. 167       158  JUMP_BACK           150  'to 150'
            160_0  COME_FROM           156  '156'

 L. 168       160  LOAD_CONST               0
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _GifImageFile__offset
            166_0  COME_FROM           134  '134'

 L. 170       166  LOAD_FAST                'self'
              168  LOAD_ATTR                dispose
              170  POP_JUMP_IF_FALSE   190  'to 190'

 L. 171       172  LOAD_FAST                'self'
              174  LOAD_ATTR                im
              176  LOAD_METHOD              paste
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                dispose
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                dispose_extent
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          
            190_0  COME_FROM           170  '170'

 L. 173       190  LOAD_CONST               0
              192  LOAD_CONST               ('copy',)
              194  IMPORT_NAME              copy
              196  IMPORT_FROM              copy
              198  STORE_FAST               'copy'
              200  POP_TOP          

 L. 175       202  LOAD_FAST                'copy'
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                global_palette
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_FAST                'self'
              212  STORE_ATTR               palette

 L. 177       214  BUILD_MAP_0           0 
              216  STORE_FAST               'info'
            218_0  COME_FROM           892  '892'
            218_1  COME_FROM           890  '890'
            218_2  COME_FROM           586  '586'
            218_3  COME_FROM           578  '578'
            218_4  COME_FROM           450  '450'
            218_5  COME_FROM           400  '400'
            218_6  COME_FROM           246  '246'

 L. 180       218  LOAD_FAST                'self'
              220  LOAD_ATTR                fp
              222  LOAD_METHOD              read
              224  LOAD_CONST               1
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               's'

 L. 181       230  LOAD_FAST                's'
              232  POP_JUMP_IF_FALSE   242  'to 242'
              234  LOAD_FAST                's'
              236  LOAD_CONST               b';'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   248  'to 248'
            242_0  COME_FROM           232  '232'

 L. 182   242_244  JUMP_FORWARD        894  'to 894'
              246  JUMP_BACK           218  'to 218'
            248_0  COME_FROM           240  '240'

 L. 184       248  LOAD_FAST                's'
              250  LOAD_CONST               b'!'
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   580  'to 580'

 L. 188       258  LOAD_FAST                'self'
              260  LOAD_ATTR                fp
              262  LOAD_METHOD              read
              264  LOAD_CONST               1
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               's'

 L. 189       270  LOAD_FAST                'self'
              272  LOAD_METHOD              data
              274  CALL_METHOD_0         0  ''
              276  STORE_FAST               'block'

 L. 190       278  LOAD_GLOBAL              i8
              280  LOAD_FAST                's'
              282  CALL_FUNCTION_1       1  ''
              284  LOAD_CONST               249
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   384  'to 384'

 L. 194       292  LOAD_GLOBAL              i8
              294  LOAD_FAST                'block'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  CALL_FUNCTION_1       1  ''
              302  STORE_FAST               'flags'

 L. 195       304  LOAD_FAST                'flags'
              306  LOAD_CONST               1
              308  BINARY_AND       
          310_312  POP_JUMP_IF_FALSE   330  'to 330'

 L. 196       314  LOAD_GLOBAL              i8
              316  LOAD_FAST                'block'
              318  LOAD_CONST               3
              320  BINARY_SUBSCR    
              322  CALL_FUNCTION_1       1  ''
              324  LOAD_FAST                'info'
              326  LOAD_STR                 'transparency'
              328  STORE_SUBSCR     
            330_0  COME_FROM           310  '310'

 L. 197       330  LOAD_GLOBAL              i16
              332  LOAD_FAST                'block'
              334  LOAD_CONST               1
              336  LOAD_CONST               3
              338  BUILD_SLICE_2         2 
              340  BINARY_SUBSCR    
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_CONST               10
              346  BINARY_MULTIPLY  
              348  LOAD_FAST                'info'
              350  LOAD_STR                 'duration'
              352  STORE_SUBSCR     

 L. 200       354  LOAD_CONST               28
              356  LOAD_FAST                'flags'
              358  BINARY_AND       
              360  STORE_FAST               'dispose_bits'

 L. 201       362  LOAD_FAST                'dispose_bits'
              364  LOAD_CONST               2
              366  BINARY_RSHIFT    
              368  STORE_FAST               'dispose_bits'

 L. 202       370  LOAD_FAST                'dispose_bits'
          372_374  POP_JUMP_IF_FALSE   564  'to 564'

 L. 207       376  LOAD_FAST                'dispose_bits'
              378  LOAD_FAST                'self'
              380  STORE_ATTR               disposal_method
              382  JUMP_FORWARD        564  'to 564'
            384_0  COME_FROM           288  '288'

 L. 208       384  LOAD_GLOBAL              i8
              386  LOAD_FAST                's'
              388  CALL_FUNCTION_1       1  ''
              390  LOAD_CONST               254
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   454  'to 454'
            398_0  COME_FROM           446  '446'

 L. 212       398  LOAD_FAST                'block'
              400  POP_JUMP_IF_FALSE_BACK   218  'to 218'

 L. 213       402  LOAD_STR                 'comment'
              404  LOAD_FAST                'info'
              406  COMPARE_OP               in
          408_410  POP_JUMP_IF_FALSE   430  'to 430'

 L. 214       412  LOAD_FAST                'info'
              414  LOAD_STR                 'comment'
              416  DUP_TOP_TWO      
              418  BINARY_SUBSCR    
              420  LOAD_FAST                'block'
              422  INPLACE_ADD      
              424  ROT_THREE        
              426  STORE_SUBSCR     
              428  JUMP_FORWARD        438  'to 438'
            430_0  COME_FROM           408  '408'

 L. 216       430  LOAD_FAST                'block'
              432  LOAD_FAST                'info'
              434  LOAD_STR                 'comment'
              436  STORE_SUBSCR     
            438_0  COME_FROM           428  '428'

 L. 217       438  LOAD_FAST                'self'
              440  LOAD_METHOD              data
              442  CALL_METHOD_0         0  ''
              444  STORE_FAST               'block'
          446_448  JUMP_BACK           398  'to 398'

 L. 218       450  JUMP_BACK           218  'to 218'
              452  BREAK_LOOP          564  'to 564'
            454_0  COME_FROM           394  '394'

 L. 219       454  LOAD_GLOBAL              i8
              456  LOAD_FAST                's'
              458  CALL_FUNCTION_1       1  ''
              460  LOAD_CONST               255
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_FALSE   564  'to 564'

 L. 223       468  LOAD_FAST                'block'
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                fp
              474  LOAD_METHOD              tell
              476  CALL_METHOD_0         0  ''
              478  BUILD_TUPLE_2         2 
              480  LOAD_FAST                'info'
              482  LOAD_STR                 'extension'
              484  STORE_SUBSCR     

 L. 224       486  LOAD_FAST                'block'
              488  LOAD_CONST               None
              490  LOAD_CONST               11
              492  BUILD_SLICE_2         2 
              494  BINARY_SUBSCR    
              496  LOAD_CONST               b'NETSCAPE2.0'
              498  COMPARE_OP               ==
          500_502  POP_JUMP_IF_FALSE   564  'to 564'

 L. 225       504  LOAD_FAST                'self'
              506  LOAD_METHOD              data
              508  CALL_METHOD_0         0  ''
              510  STORE_FAST               'block'

 L. 226       512  LOAD_GLOBAL              len
              514  LOAD_FAST                'block'
              516  CALL_FUNCTION_1       1  ''
              518  LOAD_CONST               3
              520  COMPARE_OP               >=
          522_524  POP_JUMP_IF_FALSE   564  'to 564'
              526  LOAD_GLOBAL              i8
              528  LOAD_FAST                'block'
              530  LOAD_CONST               0
              532  BINARY_SUBSCR    
              534  CALL_FUNCTION_1       1  ''
              536  LOAD_CONST               1
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   564  'to 564'

 L. 227       544  LOAD_GLOBAL              i16
              546  LOAD_FAST                'block'
              548  LOAD_CONST               1
              550  LOAD_CONST               3
              552  BUILD_SLICE_2         2 
              554  BINARY_SUBSCR    
              556  CALL_FUNCTION_1       1  ''
              558  LOAD_FAST                'info'
              560  LOAD_STR                 'loop'
              562  STORE_SUBSCR     
            564_0  COME_FROM           574  '574'
            564_1  COME_FROM           540  '540'
            564_2  COME_FROM           522  '522'
            564_3  COME_FROM           500  '500'
            564_4  COME_FROM           464  '464'
            564_5  COME_FROM           452  '452'
            564_6  COME_FROM           382  '382'
            564_7  COME_FROM           372  '372'

 L. 228       564  LOAD_FAST                'self'
              566  LOAD_METHOD              data
              568  CALL_METHOD_0         0  ''
          570_572  POP_JUMP_IF_FALSE   892  'to 892'

 L. 229   574_576  JUMP_BACK           564  'to 564'
              578  JUMP_BACK           218  'to 218'
            580_0  COME_FROM           254  '254'

 L. 231       580  LOAD_FAST                's'
              582  LOAD_CONST               b','
              584  COMPARE_OP               ==
              586  POP_JUMP_IF_FALSE_BACK   218  'to 218'

 L. 235       588  LOAD_FAST                'self'
              590  LOAD_ATTR                fp
              592  LOAD_METHOD              read
              594  LOAD_CONST               9
              596  CALL_METHOD_1         1  ''
              598  STORE_FAST               's'

 L. 238       600  LOAD_GLOBAL              i16
              602  LOAD_FAST                's'
              604  LOAD_CONST               0
              606  LOAD_CONST               None
              608  BUILD_SLICE_2         2 
              610  BINARY_SUBSCR    
              612  CALL_FUNCTION_1       1  ''
              614  LOAD_GLOBAL              i16
              616  LOAD_FAST                's'
              618  LOAD_CONST               2
              620  LOAD_CONST               None
              622  BUILD_SLICE_2         2 
              624  BINARY_SUBSCR    
              626  CALL_FUNCTION_1       1  ''
              628  ROT_TWO          
              630  STORE_FAST               'x0'
              632  STORE_FAST               'y0'

 L. 239       634  LOAD_FAST                'x0'
              636  LOAD_GLOBAL              i16
              638  LOAD_FAST                's'
              640  LOAD_CONST               4
              642  LOAD_CONST               None
              644  BUILD_SLICE_2         2 
              646  BINARY_SUBSCR    
              648  CALL_FUNCTION_1       1  ''
              650  BINARY_ADD       
              652  LOAD_FAST                'y0'
              654  LOAD_GLOBAL              i16
              656  LOAD_FAST                's'
              658  LOAD_CONST               6
              660  LOAD_CONST               None
              662  BUILD_SLICE_2         2 
              664  BINARY_SUBSCR    
              666  CALL_FUNCTION_1       1  ''
              668  BINARY_ADD       
              670  ROT_TWO          
              672  STORE_FAST               'x1'
              674  STORE_FAST               'y1'

 L. 240       676  LOAD_FAST                'x1'
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                size
              682  LOAD_CONST               0
              684  BINARY_SUBSCR    
              686  COMPARE_OP               >
          688_690  POP_JUMP_IF_TRUE    708  'to 708'
              692  LOAD_FAST                'y1'
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                size
              698  LOAD_CONST               1
              700  BINARY_SUBSCR    
              702  COMPARE_OP               >
          704_706  POP_JUMP_IF_FALSE   742  'to 742'
            708_0  COME_FROM           688  '688'

 L. 241       708  LOAD_GLOBAL              max
              710  LOAD_FAST                'x1'
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                size
              716  LOAD_CONST               0
              718  BINARY_SUBSCR    
              720  CALL_FUNCTION_2       2  ''
              722  LOAD_GLOBAL              max
              724  LOAD_FAST                'y1'
              726  LOAD_FAST                'self'
              728  LOAD_ATTR                size
              730  LOAD_CONST               1
              732  BINARY_SUBSCR    
              734  CALL_FUNCTION_2       2  ''
              736  BUILD_TUPLE_2         2 
              738  LOAD_FAST                'self'
              740  STORE_ATTR               _size
            742_0  COME_FROM           704  '704'

 L. 242       742  LOAD_FAST                'x0'
              744  LOAD_FAST                'y0'
              746  LOAD_FAST                'x1'
              748  LOAD_FAST                'y1'
              750  BUILD_TUPLE_4         4 
              752  LOAD_FAST                'self'
              754  STORE_ATTR               dispose_extent

 L. 243       756  LOAD_GLOBAL              i8
              758  LOAD_FAST                's'
              760  LOAD_CONST               8
              762  BINARY_SUBSCR    
              764  CALL_FUNCTION_1       1  ''
              766  STORE_FAST               'flags'

 L. 245       768  LOAD_FAST                'flags'
              770  LOAD_CONST               64
              772  BINARY_AND       
              774  LOAD_CONST               0
              776  COMPARE_OP               !=
              778  STORE_FAST               'interlace'

 L. 247       780  LOAD_FAST                'flags'
              782  LOAD_CONST               128
              784  BINARY_AND       
          786_788  POP_JUMP_IF_FALSE   828  'to 828'

 L. 248       790  LOAD_FAST                'flags'
              792  LOAD_CONST               7
              794  BINARY_AND       
              796  LOAD_CONST               1
              798  BINARY_ADD       
              800  STORE_FAST               'bits'

 L. 249       802  LOAD_GLOBAL              ImagePalette
              804  LOAD_METHOD              raw
              806  LOAD_STR                 'RGB'
              808  LOAD_FAST                'self'
              810  LOAD_ATTR                fp
              812  LOAD_METHOD              read
              814  LOAD_CONST               3
              816  LOAD_FAST                'bits'
              818  BINARY_LSHIFT    
              820  CALL_METHOD_1         1  ''
              822  CALL_METHOD_2         2  ''
              824  LOAD_FAST                'self'
              826  STORE_ATTR               palette
            828_0  COME_FROM           786  '786'

 L. 252       828  LOAD_GLOBAL              i8
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                fp
              834  LOAD_METHOD              read
              836  LOAD_CONST               1
              838  CALL_METHOD_1         1  ''
              840  CALL_FUNCTION_1       1  ''
              842  STORE_FAST               'bits'

 L. 253       844  LOAD_FAST                'self'
              846  LOAD_ATTR                fp
              848  LOAD_METHOD              tell
              850  CALL_METHOD_0         0  ''
              852  LOAD_FAST                'self'
              854  STORE_ATTR               _GifImageFile__offset

 L. 255       856  LOAD_STR                 'gif'
              858  LOAD_FAST                'x0'
              860  LOAD_FAST                'y0'
              862  LOAD_FAST                'x1'
              864  LOAD_FAST                'y1'
              866  BUILD_TUPLE_4         4 
              868  LOAD_FAST                'self'
              870  LOAD_ATTR                _GifImageFile__offset
              872  LOAD_FAST                'bits'
              874  LOAD_FAST                'interlace'
              876  BUILD_TUPLE_2         2 
              878  BUILD_TUPLE_4         4 

 L. 254       880  BUILD_LIST_1          1 
              882  LOAD_FAST                'self'
              884  STORE_ATTR               tile

 L. 257   886_888  JUMP_FORWARD        894  'to 894'
              890  JUMP_BACK           218  'to 218'
            892_0  COME_FROM           570  '570'

 L. 260       892  JUMP_BACK           218  'to 218'
            894_0  COME_FROM           886  '886'
            894_1  COME_FROM           242  '242'

 L. 263       894  SETUP_FINALLY      1018  'to 1018'

 L. 264       896  LOAD_FAST                'self'
              898  LOAD_ATTR                disposal_method
              900  LOAD_CONST               2
              902  COMPARE_OP               <
          904_906  POP_JUMP_IF_FALSE   916  'to 916'

 L. 266       908  LOAD_CONST               None
              910  LOAD_FAST                'self'
              912  STORE_ATTR               dispose
              914  JUMP_FORWARD        988  'to 988'
            916_0  COME_FROM           904  '904'

 L. 267       916  LOAD_FAST                'self'
              918  LOAD_ATTR                disposal_method
              920  LOAD_CONST               2
              922  COMPARE_OP               ==
          924_926  POP_JUMP_IF_FALSE   968  'to 968'

 L. 269       928  LOAD_GLOBAL              Image
              930  LOAD_METHOD              _decompression_bomb_check
              932  LOAD_FAST                'self'
              934  LOAD_ATTR                size
              936  CALL_METHOD_1         1  ''
              938  POP_TOP          

 L. 270       940  LOAD_GLOBAL              Image
              942  LOAD_ATTR                core
              944  LOAD_METHOD              fill
              946  LOAD_STR                 'P'
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                size
              952  LOAD_FAST                'self'
              954  LOAD_ATTR                info
              956  LOAD_STR                 'background'
              958  BINARY_SUBSCR    
              960  CALL_METHOD_3         3  ''
              962  LOAD_FAST                'self'
              964  STORE_ATTR               dispose
              966  JUMP_FORWARD        988  'to 988'
            968_0  COME_FROM           924  '924'

 L. 273       968  LOAD_FAST                'self'
              970  LOAD_ATTR                im
          972_974  POP_JUMP_IF_FALSE   988  'to 988'

 L. 274       976  LOAD_FAST                'self'
              978  LOAD_ATTR                im
              980  LOAD_METHOD              copy
              982  CALL_METHOD_0         0  ''
              984  LOAD_FAST                'self'
              986  STORE_ATTR               dispose
            988_0  COME_FROM           972  '972'
            988_1  COME_FROM           966  '966'
            988_2  COME_FROM           914  '914'

 L. 277       988  LOAD_FAST                'self'
              990  LOAD_ATTR                dispose
          992_994  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 278       996  LOAD_FAST                'self'
              998  LOAD_METHOD              _crop
             1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                dispose
             1004  LOAD_FAST                'self'
             1006  LOAD_ATTR                dispose_extent
             1008  CALL_METHOD_2         2  ''
             1010  LOAD_FAST                'self'
             1012  STORE_ATTR               dispose
           1014_0  COME_FROM           992  '992'
             1014  POP_BLOCK        
             1016  JUMP_FORWARD       1044  'to 1044'
           1018_0  COME_FROM_FINALLY   894  '894'

 L. 279      1018  DUP_TOP          
             1020  LOAD_GLOBAL              AttributeError
             1022  LOAD_GLOBAL              KeyError
             1024  BUILD_TUPLE_2         2 
             1026  COMPARE_OP               exception-match
         1028_1030  POP_JUMP_IF_FALSE  1042  'to 1042'
             1032  POP_TOP          
             1034  POP_TOP          
             1036  POP_TOP          

 L. 280      1038  POP_EXCEPT       
             1040  BREAK_LOOP         1044  'to 1044'
           1042_0  COME_FROM          1028  '1028'
             1042  END_FINALLY      
           1044_0  COME_FROM          1040  '1040'
           1044_1  COME_FROM          1016  '1016'

 L. 282      1044  LOAD_FAST                'self'
             1046  LOAD_ATTR                tile
         1048_1050  POP_JUMP_IF_TRUE   1056  'to 1056'

 L. 284      1052  LOAD_GLOBAL              EOFError
             1054  RAISE_VARARGS_1       1  'exception instance'
           1056_0  COME_FROM          1048  '1048'

 L. 286      1056  LOAD_CONST               ('transparency', 'duration', 'comment', 'extension', 'loop')
             1058  GET_ITER         
           1060_0  COME_FROM          1110  '1110'
           1060_1  COME_FROM          1098  '1098'
           1060_2  COME_FROM          1088  '1088'
             1060  FOR_ITER           1114  'to 1114'
             1062  STORE_FAST               'k'

 L. 287      1064  LOAD_FAST                'k'
             1066  LOAD_FAST                'info'
             1068  COMPARE_OP               in
         1070_1072  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 288      1074  LOAD_FAST                'info'
             1076  LOAD_FAST                'k'
             1078  BINARY_SUBSCR    
             1080  LOAD_FAST                'self'
             1082  LOAD_ATTR                info
             1084  LOAD_FAST                'k'
             1086  STORE_SUBSCR     
             1088  JUMP_BACK          1060  'to 1060'
           1090_0  COME_FROM          1070  '1070'

 L. 289      1090  LOAD_FAST                'k'
             1092  LOAD_FAST                'self'
             1094  LOAD_ATTR                info
             1096  COMPARE_OP               in
         1098_1100  POP_JUMP_IF_FALSE_BACK  1060  'to 1060'

 L. 290      1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                info
             1106  LOAD_FAST                'k'
             1108  DELETE_SUBSCR    
         1110_1112  JUMP_BACK          1060  'to 1060'
           1114_0  COME_FROM          1060  '1060'

 L. 292      1114  LOAD_STR                 'L'
             1116  LOAD_FAST                'self'
             1118  STORE_ATTR               mode

 L. 293      1120  LOAD_FAST                'self'
             1122  LOAD_ATTR                palette
         1124_1126  POP_JUMP_IF_FALSE  1134  'to 1134'

 L. 294      1128  LOAD_STR                 'P'
             1130  LOAD_FAST                'self'
             1132  STORE_ATTR               mode
           1134_0  COME_FROM          1124  '1124'

Parse error at or near `JUMP_BACK' instruction at offset 578

    def tell(self):
        return self._GifImageFile__frame

    def load_end(self):
        ImageFile.ImageFile.load_end(self)
        if self._prev_im:
            if self.disposal_method == 1:
                updated = self._crop(self.im, self.dispose_extent)
                self._prev_im.paste(updated, self.dispose_extent, updated.convert('RGBA'))
                self.im = self._prev_im
        self._prev_im = self.im.copy

    def _close__fp(self):
        try:
            try:
                if self._GifImageFile__fp != self.fp:
                    self._GifImageFile__fp.close
            except AttributeError:
                pass

        finally:
            self._GifImageFile__fp = None


RAWMODE = {'1':'L', 
 'L':'L',  'P':'P'}

def _normalize_mode(im, initial_call=False):
    """
    Takes an image (or frame), returns an image in a mode that is appropriate
    for saving in a Gif.

    It may return the original image, or it may return an image converted to
    palette or 'L' mode.

    UNDONE: What is the point of mucking with the initial call palette, for
    an image that shouldn't have a palette, or it would be a mode 'P' and
    get returned in the RAWMODE clause.

    :param im: Image object
    :param initial_call: Default false, set to true for a single frame.
    :returns: Image object
    """
    if im.mode in RAWMODE:
        im.load
        return im
    if Image.getmodebase(im.mode) == 'RGB':
        if initial_call:
            palette_size = 256
            if im.palette:
                palette_size = len(im.palette.getdata[1]) // 3
            return im.convert('P', palette=(Image.ADAPTIVE), colors=palette_size)
        return im.convert('P')
    return im.convert('L')


def _normalize_palette(im, palette, info):
    """
    Normalizes the palette for image.
      - Sets the palette to the incoming palette, if provided.
      - Ensures that there's a palette for L mode images
      - Optimizes the palette if necessary/desired.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: Image object
    """
    source_palette = None
    if palette:
        if isinstance(palette, (bytes, bytearray, list)):
            source_palette = bytearray(palette[:768])
        if isinstance(palette, ImagePalette.ImagePalette):
            source_palette = bytearray(itertools.chain.from_iterable(zip(palette.palette[:256], palette.palette[256:512], palette.palette[512:768])))
    if im.mode == 'P':
        source_palette = (source_palette or im.im.getpalette('RGB'))[:768]
    else:
        if not source_palette:
            source_palette = bytearray((i // 3 for i in range(768)))
        im.palette = ImagePalette.ImagePalette('RGB', palette=source_palette)
    used_palette_colors = _get_optimize(im, info)
    if used_palette_colors is not None:
        return im.remap_palette(used_palette_colors, source_palette)
    im.palette.palette = source_palette
    return im


def _write_single_frame(im, fp, palette):
    im_out = _normalize_mode(im, True)
    for k, v in im_out.info.items:
        im.encoderinfo.setdefault(k, v)
    else:
        im_out = _normalize_palette(im_out, palette, im.encoderinfo)
        for s in _get_global_header(im_out, im.encoderinfo):
            fp.write(s)
        else:
            flags = 0
            if get_interlace(im):
                flags = flags | 64
            _write_local_header(fp, im, (0, 0), flags)
            im_out.encoderconfig = (
             8, get_interlace(im))
            ImageFile._save(im_out, fp, [('gif', (0, 0) + im.size, 0, RAWMODE[im_out.mode])])
            fp.write(b'\x00')


def _write_multiple_frames(im, fp, palette):
    duration = im.encoderinfo.get('duration', im.info.get('duration'))
    disposal = im.encoderinfo.get('disposal', im.info.get('disposal'))
    im_frames = []
    frame_count = 0
    background_im = None
    for imSequence in itertools.chain([im], im.encoderinfo.get('append_images', [])):
        for im_frame in ImageSequence.Iterator(imSequence):
            im_frame = _normalize_mode(im_frame.copy)
            if frame_count == 0:
                for k, v in im_frame.info.items:
                    im.encoderinfo.setdefault(k, v)
                else:
                    im_frame = _normalize_palette(im_frame, palette, im.encoderinfo)
                    encoderinfo = im.encoderinfo.copy
                    if isinstance(duration, (list, tuple)):
                        encoderinfo['duration'] = duration[frame_count]
                    if isinstance(disposal, (list, tuple)):
                        encoderinfo['disposal'] = disposal[frame_count]
                    frame_count += 1
                    if im_frames:
                        previous = im_frames[(-1)]
                        if encoderinfo.get('disposal') == 2:
                            if background_im is None:
                                background = _get_background(im, im.encoderinfo.get('background', im.info.get('background')))
                                background_im = Image.new('P', im_frame.size, background)
                                background_im.putpalette(im_frames[0]['im'].palette)
                            base_im = background_im
                        else:
                            base_im = previous['im']
                        if _get_palette_bytes(im_frame) == _get_palette_bytes(base_im):
                            delta = ImageChops.subtract_modulo(im_frame, base_im)
                        else:
                            delta = ImageChops.subtract_modulo(im_frame.convert('RGB'), base_im.convert('RGB'))
                        bbox = delta.getbbox
                        if not bbox:
                            if duration:
                                previous['encoderinfo']['duration'] += encoderinfo['duration']
                    else:
                        bbox = None
                    im_frames.append({'im':im_frame,  'bbox':bbox,  'encoderinfo':encoderinfo})

    else:
        if len(im_frames) > 1:
            for frame_data in im_frames:
                im_frame = frame_data['im']
                if not frame_data['bbox']:
                    for s in _get_global_header(im_frame, frame_data['encoderinfo']):
                        fp.write(s)
                    else:
                        offset = (0, 0)

                else:
                    frame_data['encoderinfo']['include_color_table'] = True
                    im_frame = im_frame.crop(frame_data['bbox'])
                    offset = frame_data['bbox'][:2]
                _write_frame_data(fp, im_frame, offset, frame_data['encoderinfo'])
            else:
                return True

        if 'duration' in im.encoderinfo:
            if isinstance(im.encoderinfo['duration'], (list, tuple)):
                im.encoderinfo['duration'] = sum(im.encoderinfo['duration'])


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save(im, fp, filename, save_all=False):
    if 'palette' in im.encoderinfo or 'palette' in im.info:
        palette = im.encoderinfo.get('palette', im.info.get('palette'))
    else:
        palette = None
        im.encoderinfo['optimize'] = im.encoderinfo.get('optimize', True)
    if not (save_all and _write_multiple_frames(im, fp, palette)):
        _write_single_frame(im, fp, palette)
    fp.write(b';')
    if hasattr(fp, 'flush'):
        fp.flush


def get_interlace(im):
    interlace = im.encoderinfo.get('interlace', 1)
    if min(im.size) < 16:
        interlace = 0
    return interlace


def _write_local_header(fp, im, offset, flags):
    transparent_color_exists = False
    try:
        transparency = im.encoderinfo['transparency']
    except KeyError:
        pass
    else:
        transparency = int(transparency)
        transparent_color_exists = True
        used_palette_colors = _get_optimize(im, im.encoderinfo)
        if used_palette_colors is not None:
            try:
                transparency = used_palette_colors.index(transparency)
            except ValueError:
                transparent_color_exists = False
            else:
                if 'duration' in im.encoderinfo:
                    duration = int(im.encoderinfo['duration'] / 10)
                else:
                    duration = 0
                disposal = int(im.encoderinfo.get('disposal', 0))
                if transparent_color_exists or (duration != 0 or disposal):
                    packed_flag = 1 if transparent_color_exists else 0
                    packed_flag |= disposal << 2
                    if not transparent_color_exists:
                        transparency = 0
                    fp.write(b'!' + o8(249) + o8(4) + o8(packed_flag) + o16(duration) + o8(transparency) + o8(0))
                if 'comment' in im.encoderinfo:
                    if 1 <= len(im.encoderinfo['comment']):
                        fp.write(b'!' + o8(254))
                        comment = im.encoderinfo['comment']
                        if isinstance(comment, str):
                            comment = comment.encode
                        for i in range(0, len(comment), 255):
                            subblock = comment[i:i + 255]
                            fp.write(o8(len(subblock)) + subblock)
                        else:
                            fp.write(o8(0))

                if 'loop' in im.encoderinfo:
                    number_of_loops = im.encoderinfo['loop']
                    fp.write(b'!' + o8(255) + o8(11) + b'NETSCAPE2.0' + o8(3) + o8(1) + o16(number_of_loops) + o8(0))
                include_color_table = im.encoderinfo.get('include_color_table')
                if include_color_table:
                    palette_bytes = _get_palette_bytes(im)
                    color_table_size = _get_color_table_size(palette_bytes)
                    if color_table_size:
                        flags = flags | 128
                        flags = flags | color_table_size
                fp.write(b',' + o16(offset[0]) + o16(offset[1]) + o16(im.size[0]) + o16(im.size[1]) + o8(flags))
                if include_color_table:
                    if color_table_size:
                        fp.write(_get_header_palette(palette_bytes))
        fp.write(o8(8))


def _save_netpbm(im, fp, filename):
    tempfile = im._dump
    try:
        with open(filename, 'wb') as f:
            if im.mode != 'RGB':
                subprocess.check_call([
                 'ppmtogif', tempfile],
                  stdout=f, stderr=(subprocess.DEVNULL))
            else:
                quant_cmd = [
                 'ppmquant', '256', tempfile]
                togif_cmd = ['ppmtogif']
                quant_proc = subprocess.Popen(quant_cmd,
                  stdout=(subprocess.PIPE), stderr=(subprocess.DEVNULL))
                togif_proc = subprocess.Popen(togif_cmd,
                  stdin=(quant_proc.stdout),
                  stdout=f,
                  stderr=(subprocess.DEVNULL))
                quant_proc.stdout.close
                retcode = quant_proc.wait
                if retcode:
                    raise subprocess.CalledProcessError(retcode, quant_cmd)
                retcode = togif_proc.wait
                if retcode:
                    raise subprocess.CalledProcessError(retcode, togif_cmd)
    finally:
        try:
            os.unlink(tempfile)
        except OSError:
            pass


_FORCE_OPTIMIZE = False

def _get_optimize(im, info):
    """
    Palette optimization is a potentially expensive operation.

    This function determines if the palette should be optimized using
    some heuristics, then returns the list of palette entries in use.

    :param im: Image object
    :param info: encoderinfo
    :returns: list of indexes of palette entries in use, or None
    """
    if im.mode in ('P', 'L'):
        if not info or info.get('optimize', 0):
            optimise = _FORCE_OPTIMIZE or im.mode == 'L'
            if optimise or (im.width * im.height < 262144):
                used_palette_colors = []
                for i, count in enumerate(im.histogram):
                    if count:
                        used_palette_colors.append(i)

            if optimise or (len(used_palette_colors) <= 128 and max(used_palette_colors) > len(used_palette_colors)):
                return used_palette_colors


def _get_color_table_size(palette_bytes):
    if not palette_bytes:
        return 0
    if len(palette_bytes) < 9:
        return 1
    return math.ceil(math.log(len(palette_bytes) // 3, 2)) - 1


def _get_header_palette(palette_bytes):
    """
    Returns the palette, null padded to the next power of 2 (*3) bytes
    suitable for direct inclusion in the GIF header

    :param palette_bytes: Unpadded palette bytes, in RGBRGB form
    :returns: Null padded palette
    """
    color_table_size = _get_color_table_size(palette_bytes)
    actual_target_size_diff = (2 << color_table_size) - len(palette_bytes) // 3
    if actual_target_size_diff > 0:
        palette_bytes += o8(0) * 3 * actual_target_size_diff
    return palette_bytes


def _get_palette_bytes(im):
    """
    Gets the palette for inclusion in the gif header

    :param im: Image object
    :returns: Bytes, len<=768 suitable for inclusion in gif header
    """
    return im.palette.palette


def _get_background(im, infoBackground):
    background = 0
    if infoBackground:
        background = infoBackground
        if isinstance(background, tuple):
            background = im.palette.getcolor(background)
    return background


def _get_global_header--- This code section failed: ---

 L. 762         0  LOAD_CONST               b'87a'
                2  STORE_FAST               'version'

 L. 763         4  LOAD_CONST               ('transparency', 'duration', 'loop', 'comment')
                6  GET_ITER         
              8_0  COME_FROM            92  '92'
              8_1  COME_FROM            82  '82'
              8_2  COME_FROM            78  '78'
              8_3  COME_FROM            42  '42'
              8_4  COME_FROM            22  '22'
              8_5  COME_FROM            14  '14'
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'extensionKey'

 L. 764        12  LOAD_FAST                'info'
               14  POP_JUMP_IF_FALSE_BACK     8  'to 8'
               16  LOAD_FAST                'extensionKey'
               18  LOAD_FAST                'info'
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 765        24  LOAD_FAST                'extensionKey'
               26  LOAD_STR                 'duration'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  LOAD_FAST                'info'
               34  LOAD_FAST                'extensionKey'
               36  BINARY_SUBSCR    
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE_BACK     8  'to 8'
             44_0  COME_FROM            30  '30'

 L. 766        44  LOAD_FAST                'extensionKey'
               46  LOAD_STR                 'comment'
               48  COMPARE_OP               ==

 L. 765        50  POP_JUMP_IF_FALSE    84  'to 84'

 L. 766        52  LOAD_CONST               1

 L. 766        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'extensionKey'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''

 L. 765        64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 766        72  LOAD_CONST               255

 L. 765        74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE     84  'to 84'
               78  JUMP_BACK             8  'to 8'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          

 L. 768        82  JUMP_BACK             8  'to 8'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            50  '50'

 L. 769        84  LOAD_CONST               b'89a'
               86  STORE_FAST               'version'

 L. 770        88  POP_TOP          
               90  BREAK_LOOP          114  'to 114'
               92  JUMP_BACK             8  'to 8'
             94_0  COME_FROM             8  '8'

 L. 772        94  LOAD_FAST                'im'
               96  LOAD_ATTR                info
               98  LOAD_METHOD              get
              100  LOAD_STR                 'version'
              102  CALL_METHOD_1         1  ''
              104  LOAD_CONST               b'89a'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 773       110  LOAD_CONST               b'89a'
              112  STORE_FAST               'version'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            90  '90'

 L. 775       114  LOAD_GLOBAL              _get_background
              116  LOAD_FAST                'im'
              118  LOAD_FAST                'info'
              120  LOAD_METHOD              get
              122  LOAD_STR                 'background'
              124  CALL_METHOD_1         1  ''
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'background'

 L. 777       130  LOAD_GLOBAL              _get_palette_bytes
              132  LOAD_FAST                'im'
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'palette_bytes'

 L. 778       138  LOAD_GLOBAL              _get_color_table_size
              140  LOAD_FAST                'palette_bytes'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'color_table_size'

 L. 781       146  LOAD_CONST               b'GIF'

 L. 782       148  LOAD_FAST                'version'

 L. 781       150  BINARY_ADD       

 L. 783       152  LOAD_GLOBAL              o16
              154  LOAD_FAST                'im'
              156  LOAD_ATTR                size
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''

 L. 781       164  BINARY_ADD       

 L. 784       166  LOAD_GLOBAL              o16
              168  LOAD_FAST                'im'
              170  LOAD_ATTR                size
              172  LOAD_CONST               1
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  ''

 L. 781       178  BINARY_ADD       

 L. 787       180  LOAD_GLOBAL              o8
              182  LOAD_FAST                'color_table_size'
              184  LOAD_CONST               128
              186  BINARY_ADD       
              188  CALL_FUNCTION_1       1  ''

 L. 789       190  LOAD_GLOBAL              o8
              192  LOAD_FAST                'background'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_GLOBAL              o8
              198  LOAD_CONST               0
              200  CALL_FUNCTION_1       1  ''
              202  BINARY_ADD       

 L. 791       204  LOAD_GLOBAL              _get_header_palette
              206  LOAD_FAST                'palette_bytes'
              208  CALL_FUNCTION_1       1  ''

 L. 780       210  BUILD_LIST_4          4 
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 94


def _write_frame_data(fp, im_frame, offset, params):
    try:
        im_frame.encoderinfo = params
        _write_local_header(fp, im_frame, offset, 0)
        ImageFile._save(im_frame, fp, [('gif', (0, 0) + im_frame.size, 0, RAWMODE[im_frame.mode])])
        fp.write(b'\x00')
    finally:
        del im_frame.encoderinfo


def getheader(im, palette=None, info=None):
    """
    Legacy Method to get Gif data from image.

    Warning:: May modify image data.

    :param im: Image object
    :param palette: bytes object containing the source palette, or ....
    :param info: encoderinfo
    :returns: tuple of(list of header items, optimized palette)

    """
    used_palette_colors = _get_optimize(im, info)
    if info is None:
        info = {}
    if 'background' not in info:
        if 'background' in im.info:
            info['background'] = im.info['background']
    im_mod = _normalize_palette(im, palette, info)
    im.palette = im_mod.palette
    im.im = im_mod.im
    header = _get_global_header(im, info)
    return (
     header, used_palette_colors)


def getdata(im, offset=(0, 0), **params):
    r"""
    Legacy Method

    Return a list of strings representing this image.
    The first string is a local image header, the rest contains
    encoded image data.

    :param im: Image object
    :param offset: Tuple of (x, y) pixels. Defaults to (0,0)
    :param \**params: E.g. duration or other encoder info parameters
    :returns: List of Bytes containing gif encoded frame data

    """

    class Collector:
        data = []

        def write(self, data):
            self.data.append(data)

    im.load
    fp = Collector()
    _write_frame_data(fp, im, offset, params)
    return fp.data


Image.register_open(GifImageFile.format, GifImageFile, _accept)
Image.register_save(GifImageFile.format, _save)
Image.register_save_all(GifImageFile.format, _save_all)
Image.register_extension(GifImageFile.format, '.gif')
Image.register_mime(GifImageFile.format, 'image/gif')