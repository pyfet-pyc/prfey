# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\GifImagePlugin.py
import itertools, math, os, subprocess
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
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
            if s[0]:
                return self.fp.read(s[0])

    def _open--- This code section failed: ---

 L.  67         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               13
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  68        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L.  69        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a GIF file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  71        28  LOAD_FAST                's'
               30  LOAD_CONST               None
               32  LOAD_CONST               6
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                info
               42  LOAD_STR                 'version'
               44  STORE_SUBSCR     

 L.  72        46  LOAD_GLOBAL              i16
               48  LOAD_FAST                's'
               50  LOAD_CONST               6
               52  CALL_FUNCTION_2       2  ''
               54  LOAD_GLOBAL              i16
               56  LOAD_FAST                's'
               58  LOAD_CONST               8
               60  CALL_FUNCTION_2       2  ''
               62  BUILD_TUPLE_2         2 
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _size

 L.  73        68  BUILD_LIST_0          0 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               tile

 L.  74        74  LOAD_FAST                's'
               76  LOAD_CONST               10
               78  BINARY_SUBSCR    
               80  STORE_FAST               'flags'

 L.  75        82  LOAD_FAST                'flags'
               84  LOAD_CONST               7
               86  BINARY_AND       
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  STORE_FAST               'bits'

 L.  77        94  LOAD_FAST                'flags'
               96  LOAD_CONST               128
               98  BINARY_AND       
              100  POP_JUMP_IF_FALSE   238  'to 238'

 L.  79       102  LOAD_FAST                's'
              104  LOAD_CONST               11
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                info
              112  LOAD_STR                 'background'
              114  STORE_SUBSCR     

 L.  81       116  LOAD_FAST                'self'
              118  LOAD_ATTR                fp
              120  LOAD_METHOD              read
              122  LOAD_CONST               3
              124  LOAD_FAST                'bits'
              126  BINARY_LSHIFT    
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'p'

 L.  82       132  LOAD_GLOBAL              range
              134  LOAD_CONST               0
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'p'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               3
              144  CALL_FUNCTION_3       3  ''
              146  GET_ITER         
            148_0  COME_FROM           236  '236'
            148_1  COME_FROM           202  '202'
              148  FOR_ITER            238  'to 238'
              150  STORE_FAST               'i'

 L.  83       152  LOAD_FAST                'i'
              154  LOAD_CONST               3
              156  BINARY_FLOOR_DIVIDE
              158  LOAD_FAST                'p'
              160  LOAD_FAST                'i'
              162  BINARY_SUBSCR    
              164  DUP_TOP          
              166  ROT_THREE        
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   206  'to 206'
              172  LOAD_FAST                'p'
              174  LOAD_FAST                'i'
              176  LOAD_CONST               1
              178  BINARY_ADD       
              180  BINARY_SUBSCR    
              182  DUP_TOP          
              184  ROT_THREE        
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   206  'to 206'
              190  LOAD_FAST                'p'
              192  LOAD_FAST                'i'
              194  LOAD_CONST               2
              196  BINARY_ADD       
              198  BINARY_SUBSCR    
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_TRUE_BACK   148  'to 148'
              204  JUMP_FORWARD        208  'to 208'
            206_0  COME_FROM           188  '188'
            206_1  COME_FROM           170  '170'
              206  POP_TOP          
            208_0  COME_FROM           204  '204'

 L.  84       208  LOAD_GLOBAL              ImagePalette
              210  LOAD_METHOD              raw
              212  LOAD_STR                 'RGB'
              214  LOAD_FAST                'p'
              216  CALL_METHOD_2         2  ''
              218  STORE_FAST               'p'

 L.  85       220  LOAD_FAST                'p'
              222  DUP_TOP          
              224  LOAD_FAST                'self'
              226  STORE_ATTR               global_palette
              228  LOAD_FAST                'self'
              230  STORE_ATTR               palette

 L.  86       232  POP_TOP          
              234  BREAK_LOOP          238  'to 238'
              236  JUMP_BACK           148  'to 148'
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           148  '148'
            238_2  COME_FROM           100  '100'

 L.  88       238  LOAD_FAST                'self'
              240  LOAD_ATTR                fp
              242  LOAD_FAST                'self'
              244  STORE_ATTR               _GifImageFile__fp

 L.  89       246  LOAD_FAST                'self'
              248  LOAD_ATTR                fp
              250  LOAD_METHOD              tell
              252  CALL_METHOD_0         0  ''
              254  LOAD_FAST                'self'
              256  STORE_ATTR               _GifImageFile__rewind

 L.  90       258  LOAD_CONST               None
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _n_frames

 L.  91       264  LOAD_CONST               None
              266  LOAD_FAST                'self'
              268  STORE_ATTR               _is_animated

 L.  92       270  LOAD_FAST                'self'
              272  LOAD_METHOD              _seek
              274  LOAD_CONST               0
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 206_1

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
        for f in range(self._GifImageFile__frame + 1)(frame + 1):
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

 L. 141         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    62  'to 62'

 L. 143         8  LOAD_CONST               0
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _GifImageFile__offset

 L. 144        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               dispose

 L. 145        20  LOAD_CONST               0
               22  LOAD_CONST               0
               24  LOAD_CONST               0
               26  LOAD_CONST               0
               28  BUILD_LIST_4          4 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               dispose_extent

 L. 146        34  LOAD_CONST               -1
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _GifImageFile__frame

 L. 147        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _GifImageFile__fp
               44  LOAD_METHOD              seek
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _GifImageFile__rewind
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 148        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               disposal_method
               60  JUMP_FORWARD         76  'to 76'
             62_0  COME_FROM             6  '6'

 L. 151        62  LOAD_FAST                'self'
               64  LOAD_ATTR                im
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L. 152        68  LOAD_FAST                'self'
               70  LOAD_METHOD              load
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            60  '60'

 L. 154        76  LOAD_FAST                'frame'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _GifImageFile__frame
               82  LOAD_CONST               1
               84  BINARY_ADD       
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 155        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'cannot seek to frame '
               94  LOAD_FAST                'frame'
               96  FORMAT_VALUE          0  ''
               98  BUILD_STRING_2        2 
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            88  '88'

 L. 156       104  LOAD_FAST                'frame'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _GifImageFile__frame

 L. 158       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               tile

 L. 160       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _GifImageFile__fp
              120  LOAD_FAST                'self'
              122  STORE_ATTR               fp

 L. 161       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _GifImageFile__offset
              128  POP_JUMP_IF_FALSE   160  'to 160'

 L. 163       130  LOAD_FAST                'self'
              132  LOAD_ATTR                fp
              134  LOAD_METHOD              seek
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _GifImageFile__offset
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           152  '152'

 L. 164       144  LOAD_FAST                'self'
              146  LOAD_METHOD              data
              148  CALL_METHOD_0         0  ''
              150  POP_JUMP_IF_FALSE   154  'to 154'

 L. 165       152  JUMP_BACK           144  'to 144'
            154_0  COME_FROM           150  '150'

 L. 166       154  LOAD_CONST               0
              156  LOAD_FAST                'self'
              158  STORE_ATTR               _GifImageFile__offset
            160_0  COME_FROM           128  '128'

 L. 168       160  LOAD_FAST                'self'
              162  LOAD_ATTR                dispose
              164  POP_JUMP_IF_FALSE   184  'to 184'

 L. 169       166  LOAD_FAST                'self'
              168  LOAD_ATTR                im
              170  LOAD_METHOD              paste
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                dispose
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                dispose_extent
              180  CALL_METHOD_2         2  ''
              182  POP_TOP          
            184_0  COME_FROM           164  '164'

 L. 171       184  LOAD_CONST               0
              186  LOAD_CONST               ('copy',)
              188  IMPORT_NAME              copy
              190  IMPORT_FROM              copy
              192  STORE_FAST               'copy'
              194  POP_TOP          

 L. 173       196  LOAD_FAST                'copy'
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                global_palette
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_FAST                'self'
              206  STORE_ATTR               palette

 L. 175       208  BUILD_MAP_0           0 
              210  STORE_FAST               'info'

 L. 176       212  LOAD_CONST               None
              214  STORE_FAST               'frame_transparency'

 L. 177       216  LOAD_CONST               None
              218  STORE_FAST               'interlace'
            220_0  COME_FROM           808  '808'
            220_1  COME_FROM           806  '806'
            220_2  COME_FROM           560  '560'
            220_3  COME_FROM           552  '552'
            220_4  COME_FROM           434  '434'
            220_5  COME_FROM           384  '384'
            220_6  COME_FROM           248  '248'

 L. 180       220  LOAD_FAST                'self'
              222  LOAD_ATTR                fp
              224  LOAD_METHOD              read
              226  LOAD_CONST               1
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               's'

 L. 181       232  LOAD_FAST                's'
              234  POP_JUMP_IF_FALSE   244  'to 244'
              236  LOAD_FAST                's'
              238  LOAD_CONST               b';'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   250  'to 250'
            244_0  COME_FROM           234  '234'

 L. 182   244_246  JUMP_FORWARD        810  'to 810'
              248  JUMP_BACK           220  'to 220'
            250_0  COME_FROM           242  '242'

 L. 184       250  LOAD_FAST                's'
              252  LOAD_CONST               b'!'
              254  COMPARE_OP               ==
          256_258  POP_JUMP_IF_FALSE   554  'to 554'

 L. 188       260  LOAD_FAST                'self'
              262  LOAD_ATTR                fp
              264  LOAD_METHOD              read
              266  LOAD_CONST               1
              268  CALL_METHOD_1         1  ''
              270  STORE_FAST               's'

 L. 189       272  LOAD_FAST                'self'
              274  LOAD_METHOD              data
              276  CALL_METHOD_0         0  ''
              278  STORE_FAST               'block'

 L. 190       280  LOAD_FAST                's'
              282  LOAD_CONST               0
              284  BINARY_SUBSCR    
              286  LOAD_CONST               249
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   368  'to 368'

 L. 194       294  LOAD_FAST                'block'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  STORE_FAST               'flags'

 L. 195       302  LOAD_FAST                'flags'
              304  LOAD_CONST               1
              306  BINARY_AND       
          308_310  POP_JUMP_IF_FALSE   320  'to 320'

 L. 196       312  LOAD_FAST                'block'
              314  LOAD_CONST               3
              316  BINARY_SUBSCR    
              318  STORE_FAST               'frame_transparency'
            320_0  COME_FROM           308  '308'

 L. 197       320  LOAD_GLOBAL              i16
              322  LOAD_FAST                'block'
              324  LOAD_CONST               1
              326  CALL_FUNCTION_2       2  ''
              328  LOAD_CONST               10
              330  BINARY_MULTIPLY  
              332  LOAD_FAST                'info'
              334  LOAD_STR                 'duration'
              336  STORE_SUBSCR     

 L. 200       338  LOAD_CONST               28
              340  LOAD_FAST                'flags'
              342  BINARY_AND       
              344  STORE_FAST               'dispose_bits'

 L. 201       346  LOAD_FAST                'dispose_bits'
              348  LOAD_CONST               2
              350  BINARY_RSHIFT    
              352  STORE_FAST               'dispose_bits'

 L. 202       354  LOAD_FAST                'dispose_bits'
          356_358  POP_JUMP_IF_FALSE   538  'to 538'

 L. 207       360  LOAD_FAST                'dispose_bits'
              362  LOAD_FAST                'self'
              364  STORE_ATTR               disposal_method
              366  JUMP_FORWARD        538  'to 538'
            368_0  COME_FROM           290  '290'

 L. 208       368  LOAD_FAST                's'
              370  LOAD_CONST               0
              372  BINARY_SUBSCR    
              374  LOAD_CONST               254
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   438  'to 438'
            382_0  COME_FROM           430  '430'

 L. 212       382  LOAD_FAST                'block'
              384  POP_JUMP_IF_FALSE_BACK   220  'to 220'

 L. 213       386  LOAD_STR                 'comment'
              388  LOAD_FAST                'info'
              390  COMPARE_OP               in
          392_394  POP_JUMP_IF_FALSE   414  'to 414'

 L. 214       396  LOAD_FAST                'info'
              398  LOAD_STR                 'comment'
              400  DUP_TOP_TWO      
              402  BINARY_SUBSCR    
              404  LOAD_FAST                'block'
              406  INPLACE_ADD      
              408  ROT_THREE        
              410  STORE_SUBSCR     
              412  JUMP_FORWARD        422  'to 422'
            414_0  COME_FROM           392  '392'

 L. 216       414  LOAD_FAST                'block'
              416  LOAD_FAST                'info'
              418  LOAD_STR                 'comment'
              420  STORE_SUBSCR     
            422_0  COME_FROM           412  '412'

 L. 217       422  LOAD_FAST                'self'
              424  LOAD_METHOD              data
              426  CALL_METHOD_0         0  ''
              428  STORE_FAST               'block'
          430_432  JUMP_BACK           382  'to 382'

 L. 218       434  JUMP_BACK           220  'to 220'
              436  BREAK_LOOP          538  'to 538'
            438_0  COME_FROM           378  '378'

 L. 219       438  LOAD_FAST                's'
              440  LOAD_CONST               0
              442  BINARY_SUBSCR    
              444  LOAD_CONST               255
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   538  'to 538'

 L. 223       452  LOAD_FAST                'block'
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                fp
              458  LOAD_METHOD              tell
              460  CALL_METHOD_0         0  ''
              462  BUILD_TUPLE_2         2 
              464  LOAD_FAST                'info'
              466  LOAD_STR                 'extension'
              468  STORE_SUBSCR     

 L. 224       470  LOAD_FAST                'block'
              472  LOAD_CONST               None
              474  LOAD_CONST               11
              476  BUILD_SLICE_2         2 
              478  BINARY_SUBSCR    
              480  LOAD_CONST               b'NETSCAPE2.0'
              482  COMPARE_OP               ==
          484_486  POP_JUMP_IF_FALSE   538  'to 538'

 L. 225       488  LOAD_FAST                'self'
              490  LOAD_METHOD              data
              492  CALL_METHOD_0         0  ''
              494  STORE_FAST               'block'

 L. 226       496  LOAD_GLOBAL              len
              498  LOAD_FAST                'block'
              500  CALL_FUNCTION_1       1  ''
              502  LOAD_CONST               3
              504  COMPARE_OP               >=
          506_508  POP_JUMP_IF_FALSE   538  'to 538'
              510  LOAD_FAST                'block'
              512  LOAD_CONST               0
              514  BINARY_SUBSCR    
              516  LOAD_CONST               1
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   538  'to 538'

 L. 227       524  LOAD_GLOBAL              i16
              526  LOAD_FAST                'block'
              528  LOAD_CONST               1
              530  CALL_FUNCTION_2       2  ''
              532  LOAD_FAST                'info'
              534  LOAD_STR                 'loop'
              536  STORE_SUBSCR     
            538_0  COME_FROM           548  '548'
            538_1  COME_FROM           520  '520'
            538_2  COME_FROM           506  '506'
            538_3  COME_FROM           484  '484'
            538_4  COME_FROM           448  '448'
            538_5  COME_FROM           436  '436'
            538_6  COME_FROM           366  '366'
            538_7  COME_FROM           356  '356'

 L. 228       538  LOAD_FAST                'self'
              540  LOAD_METHOD              data
              542  CALL_METHOD_0         0  ''
          544_546  POP_JUMP_IF_FALSE   808  'to 808'

 L. 229   548_550  JUMP_BACK           538  'to 538'
              552  JUMP_BACK           220  'to 220'
            554_0  COME_FROM           256  '256'

 L. 231       554  LOAD_FAST                's'
              556  LOAD_CONST               b','
              558  COMPARE_OP               ==
              560  POP_JUMP_IF_FALSE_BACK   220  'to 220'

 L. 235       562  LOAD_FAST                'self'
              564  LOAD_ATTR                fp
              566  LOAD_METHOD              read
              568  LOAD_CONST               9
              570  CALL_METHOD_1         1  ''
              572  STORE_FAST               's'

 L. 238       574  LOAD_GLOBAL              i16
              576  LOAD_FAST                's'
              578  LOAD_CONST               0
              580  CALL_FUNCTION_2       2  ''
              582  LOAD_GLOBAL              i16
              584  LOAD_FAST                's'
              586  LOAD_CONST               2
              588  CALL_FUNCTION_2       2  ''
              590  ROT_TWO          
              592  STORE_FAST               'x0'
              594  STORE_FAST               'y0'

 L. 239       596  LOAD_FAST                'x0'
              598  LOAD_GLOBAL              i16
              600  LOAD_FAST                's'
              602  LOAD_CONST               4
              604  CALL_FUNCTION_2       2  ''
              606  BINARY_ADD       
              608  LOAD_FAST                'y0'
              610  LOAD_GLOBAL              i16
              612  LOAD_FAST                's'
              614  LOAD_CONST               6
              616  CALL_FUNCTION_2       2  ''
              618  BINARY_ADD       
              620  ROT_TWO          
              622  STORE_FAST               'x1'
              624  STORE_FAST               'y1'

 L. 240       626  LOAD_FAST                'x1'
              628  LOAD_FAST                'self'
              630  LOAD_ATTR                size
              632  LOAD_CONST               0
              634  BINARY_SUBSCR    
              636  COMPARE_OP               >
          638_640  POP_JUMP_IF_TRUE    658  'to 658'
              642  LOAD_FAST                'y1'
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                size
              648  LOAD_CONST               1
              650  BINARY_SUBSCR    
              652  COMPARE_OP               >
          654_656  POP_JUMP_IF_FALSE   692  'to 692'
            658_0  COME_FROM           638  '638'

 L. 241       658  LOAD_GLOBAL              max
              660  LOAD_FAST                'x1'
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                size
              666  LOAD_CONST               0
              668  BINARY_SUBSCR    
              670  CALL_FUNCTION_2       2  ''
              672  LOAD_GLOBAL              max
              674  LOAD_FAST                'y1'
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                size
              680  LOAD_CONST               1
              682  BINARY_SUBSCR    
              684  CALL_FUNCTION_2       2  ''
              686  BUILD_TUPLE_2         2 
              688  LOAD_FAST                'self'
              690  STORE_ATTR               _size
            692_0  COME_FROM           654  '654'

 L. 242       692  LOAD_FAST                'x0'
              694  LOAD_FAST                'y0'
              696  LOAD_FAST                'x1'
              698  LOAD_FAST                'y1'
              700  BUILD_TUPLE_4         4 
              702  LOAD_FAST                'self'
              704  STORE_ATTR               dispose_extent

 L. 243       706  LOAD_FAST                's'
              708  LOAD_CONST               8
              710  BINARY_SUBSCR    
              712  STORE_FAST               'flags'

 L. 245       714  LOAD_FAST                'flags'
              716  LOAD_CONST               64
              718  BINARY_AND       
              720  LOAD_CONST               0
              722  COMPARE_OP               !=
              724  STORE_FAST               'interlace'

 L. 247       726  LOAD_FAST                'flags'
              728  LOAD_CONST               128
              730  BINARY_AND       
          732_734  POP_JUMP_IF_FALSE   774  'to 774'

 L. 248       736  LOAD_FAST                'flags'
              738  LOAD_CONST               7
              740  BINARY_AND       
              742  LOAD_CONST               1
              744  BINARY_ADD       
              746  STORE_FAST               'bits'

 L. 249       748  LOAD_GLOBAL              ImagePalette
              750  LOAD_METHOD              raw
              752  LOAD_STR                 'RGB'
              754  LOAD_FAST                'self'
              756  LOAD_ATTR                fp
              758  LOAD_METHOD              read
              760  LOAD_CONST               3
              762  LOAD_FAST                'bits'
              764  BINARY_LSHIFT    
              766  CALL_METHOD_1         1  ''
              768  CALL_METHOD_2         2  ''
              770  LOAD_FAST                'self'
              772  STORE_ATTR               palette
            774_0  COME_FROM           732  '732'

 L. 252       774  LOAD_FAST                'self'
              776  LOAD_ATTR                fp
              778  LOAD_METHOD              read
              780  LOAD_CONST               1
              782  CALL_METHOD_1         1  ''
              784  LOAD_CONST               0
              786  BINARY_SUBSCR    
              788  STORE_FAST               'bits'

 L. 253       790  LOAD_FAST                'self'
              792  LOAD_ATTR                fp
              794  LOAD_METHOD              tell
              796  CALL_METHOD_0         0  ''
              798  LOAD_FAST                'self'
              800  STORE_ATTR               _GifImageFile__offset

 L. 254   802_804  JUMP_FORWARD        810  'to 810'
              806  JUMP_BACK           220  'to 220'
            808_0  COME_FROM           544  '544'

 L. 257       808  JUMP_BACK           220  'to 220'
            810_0  COME_FROM           802  '802'
            810_1  COME_FROM           244  '244'

 L. 260       810  SETUP_FINALLY       940  'to 940'

 L. 261       812  LOAD_FAST                'self'
              814  LOAD_ATTR                disposal_method
              816  LOAD_CONST               2
              818  COMPARE_OP               <
          820_822  POP_JUMP_IF_FALSE   832  'to 832'

 L. 263       824  LOAD_CONST               None
              826  LOAD_FAST                'self'
              828  STORE_ATTR               dispose
              830  JUMP_FORWARD        936  'to 936'
            832_0  COME_FROM           820  '820'

 L. 264       832  LOAD_FAST                'self'
              834  LOAD_ATTR                disposal_method
              836  LOAD_CONST               2
              838  COMPARE_OP               ==
          840_842  POP_JUMP_IF_FALSE   910  'to 910'

 L. 268       844  LOAD_FAST                'self'
              846  LOAD_ATTR                dispose_extent
              848  UNPACK_SEQUENCE_4     4 
              850  STORE_FAST               'x0'
              852  STORE_FAST               'y0'
              854  STORE_FAST               'x1'
              856  STORE_FAST               'y1'

 L. 269       858  LOAD_FAST                'x1'
              860  LOAD_FAST                'x0'
              862  BINARY_SUBTRACT  
              864  LOAD_FAST                'y1'
              866  LOAD_FAST                'y0'
              868  BINARY_SUBTRACT  
              870  BUILD_TUPLE_2         2 
              872  STORE_FAST               'dispose_size'

 L. 271       874  LOAD_GLOBAL              Image
              876  LOAD_METHOD              _decompression_bomb_check
              878  LOAD_FAST                'dispose_size'
              880  CALL_METHOD_1         1  ''
              882  POP_TOP          

 L. 272       884  LOAD_GLOBAL              Image
              886  LOAD_ATTR                core
              888  LOAD_METHOD              fill

 L. 273       890  LOAD_STR                 'P'

 L. 273       892  LOAD_FAST                'dispose_size'

 L. 273       894  LOAD_FAST                'self'
              896  LOAD_ATTR                info
              898  LOAD_STR                 'background'
              900  BINARY_SUBSCR    

 L. 272       902  CALL_METHOD_3         3  ''
              904  LOAD_FAST                'self'
              906  STORE_ATTR               dispose
              908  JUMP_FORWARD        936  'to 936'
            910_0  COME_FROM           840  '840'

 L. 277       910  LOAD_FAST                'self'
              912  LOAD_ATTR                im
          914_916  POP_JUMP_IF_FALSE   936  'to 936'

 L. 279       918  LOAD_FAST                'self'
              920  LOAD_METHOD              _crop
              922  LOAD_FAST                'self'
              924  LOAD_ATTR                im
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                dispose_extent
              930  CALL_METHOD_2         2  ''
              932  LOAD_FAST                'self'
              934  STORE_ATTR               dispose
            936_0  COME_FROM           914  '914'
            936_1  COME_FROM           908  '908'
            936_2  COME_FROM           830  '830'
              936  POP_BLOCK        
              938  JUMP_FORWARD        966  'to 966'
            940_0  COME_FROM_FINALLY   810  '810'

 L. 280       940  DUP_TOP          
              942  LOAD_GLOBAL              AttributeError
              944  LOAD_GLOBAL              KeyError
              946  BUILD_TUPLE_2         2 
              948  COMPARE_OP               exception-match
          950_952  POP_JUMP_IF_FALSE   964  'to 964'
              954  POP_TOP          
              956  POP_TOP          
              958  POP_TOP          

 L. 281       960  POP_EXCEPT       
              962  BREAK_LOOP          966  'to 966'
            964_0  COME_FROM           950  '950'
              964  END_FINALLY      
            966_0  COME_FROM           962  '962'
            966_1  COME_FROM           938  '938'

 L. 283       966  LOAD_FAST                'interlace'
              968  LOAD_CONST               None
              970  COMPARE_OP               is-not
          972_974  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 284       976  LOAD_CONST               -1
              978  STORE_FAST               'transparency'

 L. 285       980  LOAD_FAST                'frame_transparency'
              982  LOAD_CONST               None
              984  COMPARE_OP               is-not
          986_988  POP_JUMP_IF_FALSE  1016  'to 1016'

 L. 286       990  LOAD_FAST                'frame'
              992  LOAD_CONST               0
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 287      1000  LOAD_FAST                'frame_transparency'
             1002  LOAD_FAST                'self'
             1004  LOAD_ATTR                info
             1006  LOAD_STR                 'transparency'
             1008  STORE_SUBSCR     
             1010  JUMP_FORWARD       1016  'to 1016'
           1012_0  COME_FROM           996  '996'

 L. 289      1012  LOAD_FAST                'frame_transparency'
             1014  STORE_FAST               'transparency'
           1016_0  COME_FROM          1010  '1010'
           1016_1  COME_FROM           986  '986'

 L. 292      1016  LOAD_STR                 'gif'

 L. 293      1018  LOAD_FAST                'x0'
             1020  LOAD_FAST                'y0'
             1022  LOAD_FAST                'x1'
             1024  LOAD_FAST                'y1'
             1026  BUILD_TUPLE_4         4 

 L. 294      1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                _GifImageFile__offset

 L. 295      1032  LOAD_FAST                'bits'
             1034  LOAD_FAST                'interlace'
             1036  LOAD_FAST                'transparency'
             1038  BUILD_TUPLE_3         3 

 L. 291      1040  BUILD_TUPLE_4         4 

 L. 290      1042  BUILD_LIST_1          1 
             1044  LOAD_FAST                'self'
             1046  STORE_ATTR               tile
             1048  JUMP_FORWARD       1054  'to 1054'
           1050_0  COME_FROM           972  '972'

 L. 300      1050  LOAD_GLOBAL              EOFError
             1052  RAISE_VARARGS_1       1  'exception instance'
           1054_0  COME_FROM          1048  '1048'

 L. 302      1054  LOAD_CONST               ('duration', 'comment', 'extension', 'loop')
             1056  GET_ITER         
           1058_0  COME_FROM          1108  '1108'
           1058_1  COME_FROM          1096  '1096'
           1058_2  COME_FROM          1086  '1086'
             1058  FOR_ITER           1112  'to 1112'
             1060  STORE_FAST               'k'

 L. 303      1062  LOAD_FAST                'k'
             1064  LOAD_FAST                'info'
             1066  COMPARE_OP               in
         1068_1070  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 304      1072  LOAD_FAST                'info'
             1074  LOAD_FAST                'k'
             1076  BINARY_SUBSCR    
             1078  LOAD_FAST                'self'
             1080  LOAD_ATTR                info
             1082  LOAD_FAST                'k'
             1084  STORE_SUBSCR     
             1086  JUMP_BACK          1058  'to 1058'
           1088_0  COME_FROM          1068  '1068'

 L. 305      1088  LOAD_FAST                'k'
             1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                info
             1094  COMPARE_OP               in
         1096_1098  POP_JUMP_IF_FALSE_BACK  1058  'to 1058'

 L. 306      1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                info
             1104  LOAD_FAST                'k'
             1106  DELETE_SUBSCR    
         1108_1110  JUMP_BACK          1058  'to 1058'
           1112_0  COME_FROM          1058  '1058'

 L. 308      1112  LOAD_STR                 'L'
             1114  LOAD_FAST                'self'
             1116  STORE_ATTR               mode

 L. 309      1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                palette
         1122_1124  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 310      1126  LOAD_STR                 'P'
             1128  LOAD_FAST                'self'
             1130  STORE_ATTR               mode
           1132_0  COME_FROM          1122  '1122'

Parse error at or near `JUMP_BACK' instruction at offset 552

    def tell(self):
        return self._GifImageFile__frame

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
        if isinstancepalette(bytes, bytearray, list):
            source_palette = bytearray(palette[:768])
        if isinstancepaletteImagePalette.ImagePalette:
            source_palette = bytearray(itertools.chain.from_iterable(zip(palette.palette[:256], palette.palette[256:512], palette.palette[512:768])))
    if im.mode == 'P':
        source_palette = (source_palette or im.im.getpalette('RGB'))[:768]
    else:
        if not source_palette:
            source_palette = bytearray((i // 3 for i in range(768)))
        im.palette = ImagePalette.ImagePalette('RGB', palette=source_palette)
    used_palette_colors = _get_optimizeiminfo
    if used_palette_colors is not None:
        return im.remap_palette(used_palette_colors, source_palette)
    im.palette.palette = source_palette
    return im


def _write_single_frame(im, fp, palette):
    im_out = _normalize_modeimTrue
    for k, v in im_out.info.items:
        im.encoderinfo.setdefault(k, v)
    else:
        im_out = _normalize_palette(im_out, palette, im.encoderinfo)
        for s in _get_global_headerim_outim.encoderinfo:
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
                    if isinstanceduration(list, tuple):
                        encoderinfo['duration'] = duration[frame_count]
                    if isinstancedisposal(list, tuple):
                        encoderinfo['disposal'] = disposal[frame_count]
                    frame_count += 1
                    if im_frames:
                        previous = im_frames[(-1)]
                        if encoderinfo.get('disposal') == 2:
                            if background_im is None:
                                background = _get_backgroundimim.encoderinfo.get('background', im.info.get('background'))
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
                    for s in _get_global_headerim_frameframe_data['encoderinfo']:
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
            if isinstanceim.encoderinfo['duration'](list, tuple):
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
    if hasattrfp'flush':
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
        used_palette_colors = _get_optimizeimim.encoderinfo
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
                        if isinstancecommentstr:
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
        with openfilename'wb' as f:
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
        if isinstancebackgroundtuple:
            background = im.palette.getcolor(background)
    return background


def _get_global_header--- This code section failed: ---

 L. 765         0  LOAD_CONST               b'87a'
                2  STORE_FAST               'version'

 L. 766         4  LOAD_CONST               ('transparency', 'duration', 'loop', 'comment')
                6  GET_ITER         
              8_0  COME_FROM            92  '92'
              8_1  COME_FROM            82  '82'
              8_2  COME_FROM            78  '78'
              8_3  COME_FROM            42  '42'
              8_4  COME_FROM            22  '22'
              8_5  COME_FROM            14  '14'
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'extensionKey'

 L. 767        12  LOAD_FAST                'info'
               14  POP_JUMP_IF_FALSE_BACK     8  'to 8'
               16  LOAD_FAST                'extensionKey'
               18  LOAD_FAST                'info'
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 768        24  LOAD_FAST                'extensionKey'
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

 L. 769        44  LOAD_FAST                'extensionKey'
               46  LOAD_STR                 'comment'
               48  COMPARE_OP               ==

 L. 768        50  POP_JUMP_IF_FALSE    84  'to 84'

 L. 769        52  LOAD_CONST               1

 L. 769        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'extensionKey'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''

 L. 768        64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 769        72  LOAD_CONST               255

 L. 768        74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE     84  'to 84'
               78  JUMP_BACK             8  'to 8'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          

 L. 771        82  JUMP_BACK             8  'to 8'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            50  '50'

 L. 772        84  LOAD_CONST               b'89a'
               86  STORE_FAST               'version'

 L. 773        88  POP_TOP          
               90  BREAK_LOOP          114  'to 114'
               92  JUMP_BACK             8  'to 8'
             94_0  COME_FROM             8  '8'

 L. 775        94  LOAD_FAST                'im'
               96  LOAD_ATTR                info
               98  LOAD_METHOD              get
              100  LOAD_STR                 'version'
              102  CALL_METHOD_1         1  ''
              104  LOAD_CONST               b'89a'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 776       110  LOAD_CONST               b'89a'
              112  STORE_FAST               'version'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            90  '90'

 L. 778       114  LOAD_GLOBAL              _get_background
              116  LOAD_FAST                'im'
              118  LOAD_FAST                'info'
              120  LOAD_METHOD              get
              122  LOAD_STR                 'background'
              124  CALL_METHOD_1         1  ''
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'background'

 L. 780       130  LOAD_GLOBAL              _get_palette_bytes
              132  LOAD_FAST                'im'
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'palette_bytes'

 L. 781       138  LOAD_GLOBAL              _get_color_table_size
              140  LOAD_FAST                'palette_bytes'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'color_table_size'

 L. 784       146  LOAD_CONST               b'GIF'

 L. 785       148  LOAD_FAST                'version'

 L. 784       150  BINARY_ADD       

 L. 786       152  LOAD_GLOBAL              o16
              154  LOAD_FAST                'im'
              156  LOAD_ATTR                size
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''

 L. 784       164  BINARY_ADD       

 L. 787       166  LOAD_GLOBAL              o16
              168  LOAD_FAST                'im'
              170  LOAD_ATTR                size
              172  LOAD_CONST               1
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  ''

 L. 784       178  BINARY_ADD       

 L. 790       180  LOAD_GLOBAL              o8
              182  LOAD_FAST                'color_table_size'
              184  LOAD_CONST               128
              186  BINARY_ADD       
              188  CALL_FUNCTION_1       1  ''

 L. 792       190  LOAD_GLOBAL              o8
              192  LOAD_FAST                'background'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_GLOBAL              o8
              198  LOAD_CONST               0
              200  CALL_FUNCTION_1       1  ''
              202  BINARY_ADD       

 L. 794       204  LOAD_GLOBAL              _get_header_palette
              206  LOAD_FAST                'palette_bytes'
              208  CALL_FUNCTION_1       1  ''

 L. 783       210  BUILD_LIST_4          4 
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
    used_palette_colors = _get_optimizeiminfo
    if info is None:
        info = {}
    if 'background' not in info:
        if 'background' in im.info:
            info['background'] = im.info['background']
    im_mod = _normalize_palette(im, palette, info)
    im.palette = im_mod.palette
    im.im = im_mod.im
    header = _get_global_headeriminfo
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