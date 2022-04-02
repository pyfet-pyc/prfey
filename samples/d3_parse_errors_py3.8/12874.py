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
                6  POP_JUMP_IF_FALSE    68  'to 68'

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

 L. 148        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _prev_im

 L. 149        60  LOAD_CONST               0
               62  LOAD_FAST                'self'
               64  STORE_ATTR               disposal_method
               66  JUMP_FORWARD         82  'to 82'
             68_0  COME_FROM             6  '6'

 L. 152        68  LOAD_FAST                'self'
               70  LOAD_ATTR                im
               72  POP_JUMP_IF_TRUE     82  'to 82'

 L. 153        74  LOAD_FAST                'self'
               76  LOAD_METHOD              load
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            66  '66'

 L. 155        82  LOAD_FAST                'frame'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _GifImageFile__frame
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   110  'to 110'

 L. 156        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'cannot seek to frame '
              100  LOAD_FAST                'frame'
              102  FORMAT_VALUE          0  ''
              104  BUILD_STRING_2        2 
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM            94  '94'

 L. 157       110  LOAD_FAST                'frame'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _GifImageFile__frame

 L. 159       116  BUILD_LIST_0          0 
              118  LOAD_FAST                'self'
              120  STORE_ATTR               tile

 L. 161       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _GifImageFile__fp
              126  LOAD_FAST                'self'
              128  STORE_ATTR               fp

 L. 162       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _GifImageFile__offset
              134  POP_JUMP_IF_FALSE   166  'to 166'

 L. 164       136  LOAD_FAST                'self'
              138  LOAD_ATTR                fp
              140  LOAD_METHOD              seek
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _GifImageFile__offset
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
            150_0  COME_FROM           158  '158'

 L. 165       150  LOAD_FAST                'self'
              152  LOAD_METHOD              data
              154  CALL_METHOD_0         0  ''
              156  POP_JUMP_IF_FALSE   160  'to 160'

 L. 166       158  JUMP_BACK           150  'to 150'
            160_0  COME_FROM           156  '156'

 L. 167       160  LOAD_CONST               0
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _GifImageFile__offset
            166_0  COME_FROM           134  '134'

 L. 169       166  LOAD_FAST                'self'
              168  LOAD_ATTR                dispose
              170  POP_JUMP_IF_FALSE   190  'to 190'

 L. 170       172  LOAD_FAST                'self'
              174  LOAD_ATTR                im
              176  LOAD_METHOD              paste
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                dispose
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                dispose_extent
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          
            190_0  COME_FROM           170  '170'

 L. 172       190  LOAD_CONST               0
              192  LOAD_CONST               ('copy',)
              194  IMPORT_NAME              copy
              196  IMPORT_FROM              copy
              198  STORE_FAST               'copy'
              200  POP_TOP          

 L. 174       202  LOAD_FAST                'copy'
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                global_palette
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_FAST                'self'
              212  STORE_ATTR               palette

 L. 176       214  BUILD_MAP_0           0 
              216  STORE_FAST               'info'
            218_0  COME_FROM           840  '840'
            218_1  COME_FROM           838  '838'
            218_2  COME_FROM           562  '562'
            218_3  COME_FROM           554  '554'
            218_4  COME_FROM           436  '436'
            218_5  COME_FROM           386  '386'
            218_6  COME_FROM           246  '246'

 L. 179       218  LOAD_FAST                'self'
              220  LOAD_ATTR                fp
              222  LOAD_METHOD              read
              224  LOAD_CONST               1
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               's'

 L. 180       230  LOAD_FAST                's'
              232  POP_JUMP_IF_FALSE   242  'to 242'
              234  LOAD_FAST                's'
              236  LOAD_CONST               b';'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   248  'to 248'
            242_0  COME_FROM           232  '232'

 L. 181   242_244  JUMP_FORWARD        842  'to 842'
              246  JUMP_BACK           218  'to 218'
            248_0  COME_FROM           240  '240'

 L. 183       248  LOAD_FAST                's'
              250  LOAD_CONST               b'!'
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   556  'to 556'

 L. 187       258  LOAD_FAST                'self'
              260  LOAD_ATTR                fp
              262  LOAD_METHOD              read
              264  LOAD_CONST               1
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               's'

 L. 188       270  LOAD_FAST                'self'
              272  LOAD_METHOD              data
              274  CALL_METHOD_0         0  ''
              276  STORE_FAST               'block'

 L. 189       278  LOAD_FAST                's'
              280  LOAD_CONST               0
              282  BINARY_SUBSCR    
              284  LOAD_CONST               249
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   370  'to 370'

 L. 193       292  LOAD_FAST                'block'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  STORE_FAST               'flags'

 L. 194       300  LOAD_FAST                'flags'
              302  LOAD_CONST               1
              304  BINARY_AND       
          306_308  POP_JUMP_IF_FALSE   322  'to 322'

 L. 195       310  LOAD_FAST                'block'
              312  LOAD_CONST               3
              314  BINARY_SUBSCR    
              316  LOAD_FAST                'info'
              318  LOAD_STR                 'transparency'
              320  STORE_SUBSCR     
            322_0  COME_FROM           306  '306'

 L. 196       322  LOAD_GLOBAL              i16
              324  LOAD_FAST                'block'
              326  LOAD_CONST               1
              328  CALL_FUNCTION_2       2  ''
              330  LOAD_CONST               10
              332  BINARY_MULTIPLY  
              334  LOAD_FAST                'info'
              336  LOAD_STR                 'duration'
              338  STORE_SUBSCR     

 L. 199       340  LOAD_CONST               28
              342  LOAD_FAST                'flags'
              344  BINARY_AND       
              346  STORE_FAST               'dispose_bits'

 L. 200       348  LOAD_FAST                'dispose_bits'
              350  LOAD_CONST               2
              352  BINARY_RSHIFT    
              354  STORE_FAST               'dispose_bits'

 L. 201       356  LOAD_FAST                'dispose_bits'
          358_360  POP_JUMP_IF_FALSE   540  'to 540'

 L. 206       362  LOAD_FAST                'dispose_bits'
              364  LOAD_FAST                'self'
              366  STORE_ATTR               disposal_method
              368  JUMP_FORWARD        540  'to 540'
            370_0  COME_FROM           288  '288'

 L. 207       370  LOAD_FAST                's'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  LOAD_CONST               254
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   440  'to 440'
            384_0  COME_FROM           432  '432'

 L. 211       384  LOAD_FAST                'block'
              386  POP_JUMP_IF_FALSE_BACK   218  'to 218'

 L. 212       388  LOAD_STR                 'comment'
              390  LOAD_FAST                'info'
              392  COMPARE_OP               in
          394_396  POP_JUMP_IF_FALSE   416  'to 416'

 L. 213       398  LOAD_FAST                'info'
              400  LOAD_STR                 'comment'
              402  DUP_TOP_TWO      
              404  BINARY_SUBSCR    
              406  LOAD_FAST                'block'
              408  INPLACE_ADD      
              410  ROT_THREE        
              412  STORE_SUBSCR     
              414  JUMP_FORWARD        424  'to 424'
            416_0  COME_FROM           394  '394'

 L. 215       416  LOAD_FAST                'block'
              418  LOAD_FAST                'info'
              420  LOAD_STR                 'comment'
              422  STORE_SUBSCR     
            424_0  COME_FROM           414  '414'

 L. 216       424  LOAD_FAST                'self'
              426  LOAD_METHOD              data
              428  CALL_METHOD_0         0  ''
              430  STORE_FAST               'block'
          432_434  JUMP_BACK           384  'to 384'

 L. 217       436  JUMP_BACK           218  'to 218'
              438  BREAK_LOOP          540  'to 540'
            440_0  COME_FROM           380  '380'

 L. 218       440  LOAD_FAST                's'
              442  LOAD_CONST               0
              444  BINARY_SUBSCR    
              446  LOAD_CONST               255
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_FALSE   540  'to 540'

 L. 222       454  LOAD_FAST                'block'
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                fp
              460  LOAD_METHOD              tell
              462  CALL_METHOD_0         0  ''
              464  BUILD_TUPLE_2         2 
              466  LOAD_FAST                'info'
              468  LOAD_STR                 'extension'
              470  STORE_SUBSCR     

 L. 223       472  LOAD_FAST                'block'
              474  LOAD_CONST               None
              476  LOAD_CONST               11
              478  BUILD_SLICE_2         2 
              480  BINARY_SUBSCR    
              482  LOAD_CONST               b'NETSCAPE2.0'
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   540  'to 540'

 L. 224       490  LOAD_FAST                'self'
              492  LOAD_METHOD              data
              494  CALL_METHOD_0         0  ''
              496  STORE_FAST               'block'

 L. 225       498  LOAD_GLOBAL              len
              500  LOAD_FAST                'block'
              502  CALL_FUNCTION_1       1  ''
              504  LOAD_CONST               3
              506  COMPARE_OP               >=
          508_510  POP_JUMP_IF_FALSE   540  'to 540'
              512  LOAD_FAST                'block'
              514  LOAD_CONST               0
              516  BINARY_SUBSCR    
              518  LOAD_CONST               1
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   540  'to 540'

 L. 226       526  LOAD_GLOBAL              i16
              528  LOAD_FAST                'block'
              530  LOAD_CONST               1
              532  CALL_FUNCTION_2       2  ''
              534  LOAD_FAST                'info'
              536  LOAD_STR                 'loop'
              538  STORE_SUBSCR     
            540_0  COME_FROM           550  '550'
            540_1  COME_FROM           522  '522'
            540_2  COME_FROM           508  '508'
            540_3  COME_FROM           486  '486'
            540_4  COME_FROM           450  '450'
            540_5  COME_FROM           438  '438'
            540_6  COME_FROM           368  '368'
            540_7  COME_FROM           358  '358'

 L. 227       540  LOAD_FAST                'self'
              542  LOAD_METHOD              data
              544  CALL_METHOD_0         0  ''
          546_548  POP_JUMP_IF_FALSE   840  'to 840'

 L. 228   550_552  JUMP_BACK           540  'to 540'
              554  JUMP_BACK           218  'to 218'
            556_0  COME_FROM           254  '254'

 L. 230       556  LOAD_FAST                's'
              558  LOAD_CONST               b','
              560  COMPARE_OP               ==
              562  POP_JUMP_IF_FALSE_BACK   218  'to 218'

 L. 234       564  LOAD_FAST                'self'
              566  LOAD_ATTR                fp
              568  LOAD_METHOD              read
              570  LOAD_CONST               9
              572  CALL_METHOD_1         1  ''
              574  STORE_FAST               's'

 L. 237       576  LOAD_GLOBAL              i16
              578  LOAD_FAST                's'
              580  LOAD_CONST               0
              582  CALL_FUNCTION_2       2  ''
              584  LOAD_GLOBAL              i16
              586  LOAD_FAST                's'
              588  LOAD_CONST               2
              590  CALL_FUNCTION_2       2  ''
              592  ROT_TWO          
              594  STORE_FAST               'x0'
              596  STORE_FAST               'y0'

 L. 238       598  LOAD_FAST                'x0'
              600  LOAD_GLOBAL              i16
              602  LOAD_FAST                's'
              604  LOAD_CONST               4
              606  CALL_FUNCTION_2       2  ''
              608  BINARY_ADD       
              610  LOAD_FAST                'y0'
              612  LOAD_GLOBAL              i16
              614  LOAD_FAST                's'
              616  LOAD_CONST               6
              618  CALL_FUNCTION_2       2  ''
              620  BINARY_ADD       
              622  ROT_TWO          
              624  STORE_FAST               'x1'
              626  STORE_FAST               'y1'

 L. 239       628  LOAD_FAST                'x1'
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                size
              634  LOAD_CONST               0
              636  BINARY_SUBSCR    
              638  COMPARE_OP               >
          640_642  POP_JUMP_IF_TRUE    660  'to 660'
              644  LOAD_FAST                'y1'
              646  LOAD_FAST                'self'
              648  LOAD_ATTR                size
              650  LOAD_CONST               1
              652  BINARY_SUBSCR    
              654  COMPARE_OP               >
          656_658  POP_JUMP_IF_FALSE   694  'to 694'
            660_0  COME_FROM           640  '640'

 L. 240       660  LOAD_GLOBAL              max
              662  LOAD_FAST                'x1'
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                size
              668  LOAD_CONST               0
              670  BINARY_SUBSCR    
              672  CALL_FUNCTION_2       2  ''
              674  LOAD_GLOBAL              max
              676  LOAD_FAST                'y1'
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                size
              682  LOAD_CONST               1
              684  BINARY_SUBSCR    
              686  CALL_FUNCTION_2       2  ''
              688  BUILD_TUPLE_2         2 
              690  LOAD_FAST                'self'
              692  STORE_ATTR               _size
            694_0  COME_FROM           656  '656'

 L. 241       694  LOAD_FAST                'x0'
              696  LOAD_FAST                'y0'
              698  LOAD_FAST                'x1'
              700  LOAD_FAST                'y1'
              702  BUILD_TUPLE_4         4 
              704  LOAD_FAST                'self'
              706  STORE_ATTR               dispose_extent

 L. 242       708  LOAD_FAST                's'
              710  LOAD_CONST               8
              712  BINARY_SUBSCR    
              714  STORE_FAST               'flags'

 L. 244       716  LOAD_FAST                'flags'
              718  LOAD_CONST               64
              720  BINARY_AND       
              722  LOAD_CONST               0
              724  COMPARE_OP               !=
              726  STORE_FAST               'interlace'

 L. 246       728  LOAD_FAST                'flags'
              730  LOAD_CONST               128
              732  BINARY_AND       
          734_736  POP_JUMP_IF_FALSE   776  'to 776'

 L. 247       738  LOAD_FAST                'flags'
              740  LOAD_CONST               7
              742  BINARY_AND       
              744  LOAD_CONST               1
              746  BINARY_ADD       
              748  STORE_FAST               'bits'

 L. 248       750  LOAD_GLOBAL              ImagePalette
              752  LOAD_METHOD              raw
              754  LOAD_STR                 'RGB'
              756  LOAD_FAST                'self'
              758  LOAD_ATTR                fp
              760  LOAD_METHOD              read
              762  LOAD_CONST               3
              764  LOAD_FAST                'bits'
              766  BINARY_LSHIFT    
              768  CALL_METHOD_1         1  ''
              770  CALL_METHOD_2         2  ''
              772  LOAD_FAST                'self'
              774  STORE_ATTR               palette
            776_0  COME_FROM           734  '734'

 L. 251       776  LOAD_FAST                'self'
              778  LOAD_ATTR                fp
              780  LOAD_METHOD              read
              782  LOAD_CONST               1
              784  CALL_METHOD_1         1  ''
              786  LOAD_CONST               0
              788  BINARY_SUBSCR    
              790  STORE_FAST               'bits'

 L. 252       792  LOAD_FAST                'self'
              794  LOAD_ATTR                fp
              796  LOAD_METHOD              tell
              798  CALL_METHOD_0         0  ''
              800  LOAD_FAST                'self'
              802  STORE_ATTR               _GifImageFile__offset

 L. 254       804  LOAD_STR                 'gif'
              806  LOAD_FAST                'x0'
              808  LOAD_FAST                'y0'
              810  LOAD_FAST                'x1'
              812  LOAD_FAST                'y1'
              814  BUILD_TUPLE_4         4 
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                _GifImageFile__offset
              820  LOAD_FAST                'bits'
              822  LOAD_FAST                'interlace'
              824  BUILD_TUPLE_2         2 
              826  BUILD_TUPLE_4         4 

 L. 253       828  BUILD_LIST_1          1 
              830  LOAD_FAST                'self'
              832  STORE_ATTR               tile

 L. 256   834_836  JUMP_FORWARD        842  'to 842'
              838  JUMP_BACK           218  'to 218'
            840_0  COME_FROM           546  '546'

 L. 259       840  JUMP_BACK           218  'to 218'
            842_0  COME_FROM           834  '834'
            842_1  COME_FROM           242  '242'

 L. 262       842  SETUP_FINALLY       966  'to 966'

 L. 263       844  LOAD_FAST                'self'
              846  LOAD_ATTR                disposal_method
              848  LOAD_CONST               2
              850  COMPARE_OP               <
          852_854  POP_JUMP_IF_FALSE   864  'to 864'

 L. 265       856  LOAD_CONST               None
              858  LOAD_FAST                'self'
              860  STORE_ATTR               dispose
              862  JUMP_FORWARD        936  'to 936'
            864_0  COME_FROM           852  '852'

 L. 266       864  LOAD_FAST                'self'
              866  LOAD_ATTR                disposal_method
              868  LOAD_CONST               2
              870  COMPARE_OP               ==
          872_874  POP_JUMP_IF_FALSE   916  'to 916'

 L. 268       876  LOAD_GLOBAL              Image
              878  LOAD_METHOD              _decompression_bomb_check
              880  LOAD_FAST                'self'
              882  LOAD_ATTR                size
              884  CALL_METHOD_1         1  ''
              886  POP_TOP          

 L. 269       888  LOAD_GLOBAL              Image
              890  LOAD_ATTR                core
              892  LOAD_METHOD              fill
              894  LOAD_STR                 'P'
              896  LOAD_FAST                'self'
              898  LOAD_ATTR                size
              900  LOAD_FAST                'self'
              902  LOAD_ATTR                info
              904  LOAD_STR                 'background'
              906  BINARY_SUBSCR    
              908  CALL_METHOD_3         3  ''
              910  LOAD_FAST                'self'
              912  STORE_ATTR               dispose
              914  JUMP_FORWARD        936  'to 936'
            916_0  COME_FROM           872  '872'

 L. 272       916  LOAD_FAST                'self'
              918  LOAD_ATTR                im
          920_922  POP_JUMP_IF_FALSE   936  'to 936'

 L. 273       924  LOAD_FAST                'self'
              926  LOAD_ATTR                im
              928  LOAD_METHOD              copy
              930  CALL_METHOD_0         0  ''
              932  LOAD_FAST                'self'
              934  STORE_ATTR               dispose
            936_0  COME_FROM           920  '920'
            936_1  COME_FROM           914  '914'
            936_2  COME_FROM           862  '862'

 L. 276       936  LOAD_FAST                'self'
              938  LOAD_ATTR                dispose
          940_942  POP_JUMP_IF_FALSE   962  'to 962'

 L. 277       944  LOAD_FAST                'self'
              946  LOAD_METHOD              _crop
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                dispose
              952  LOAD_FAST                'self'
              954  LOAD_ATTR                dispose_extent
              956  CALL_METHOD_2         2  ''
              958  LOAD_FAST                'self'
              960  STORE_ATTR               dispose
            962_0  COME_FROM           940  '940'
              962  POP_BLOCK        
              964  JUMP_FORWARD        992  'to 992'
            966_0  COME_FROM_FINALLY   842  '842'

 L. 278       966  DUP_TOP          
              968  LOAD_GLOBAL              AttributeError
              970  LOAD_GLOBAL              KeyError
              972  BUILD_TUPLE_2         2 
              974  COMPARE_OP               exception-match
          976_978  POP_JUMP_IF_FALSE   990  'to 990'
              980  POP_TOP          
              982  POP_TOP          
              984  POP_TOP          

 L. 279       986  POP_EXCEPT       
              988  BREAK_LOOP          992  'to 992'
            990_0  COME_FROM           976  '976'
              990  END_FINALLY      
            992_0  COME_FROM           988  '988'
            992_1  COME_FROM           964  '964'

 L. 281       992  LOAD_FAST                'self'
              994  LOAD_ATTR                tile
          996_998  POP_JUMP_IF_TRUE   1004  'to 1004'

 L. 283      1000  LOAD_GLOBAL              EOFError
             1002  RAISE_VARARGS_1       1  'exception instance'
           1004_0  COME_FROM           996  '996'

 L. 285      1004  LOAD_CONST               ('transparency', 'duration', 'comment', 'extension', 'loop')
             1006  GET_ITER         
           1008_0  COME_FROM          1058  '1058'
           1008_1  COME_FROM          1046  '1046'
           1008_2  COME_FROM          1036  '1036'
             1008  FOR_ITER           1062  'to 1062'
             1010  STORE_FAST               'k'

 L. 286      1012  LOAD_FAST                'k'
             1014  LOAD_FAST                'info'
             1016  COMPARE_OP               in
         1018_1020  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 287      1022  LOAD_FAST                'info'
             1024  LOAD_FAST                'k'
             1026  BINARY_SUBSCR    
             1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                info
             1032  LOAD_FAST                'k'
             1034  STORE_SUBSCR     
             1036  JUMP_BACK          1008  'to 1008'
           1038_0  COME_FROM          1018  '1018'

 L. 288      1038  LOAD_FAST                'k'
             1040  LOAD_FAST                'self'
             1042  LOAD_ATTR                info
             1044  COMPARE_OP               in
         1046_1048  POP_JUMP_IF_FALSE_BACK  1008  'to 1008'

 L. 289      1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                info
             1054  LOAD_FAST                'k'
             1056  DELETE_SUBSCR    
         1058_1060  JUMP_BACK          1008  'to 1008'
           1062_0  COME_FROM          1008  '1008'

 L. 291      1062  LOAD_STR                 'L'
             1064  LOAD_FAST                'self'
             1066  STORE_ATTR               mode

 L. 292      1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                palette
         1072_1074  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 293      1076  LOAD_STR                 'P'
             1078  LOAD_FAST                'self'
             1080  STORE_ATTR               mode
           1082_0  COME_FROM          1072  '1072'

Parse error at or near `JUMP_BACK' instruction at offset 554

    def tell(self):
        return self._GifImageFile__frame

    def load_end(self):
        ImageFile.ImageFile.load_end(self)
        if self._prev_im:
            if self._prev_disposal_method == 1:
                updated = self._crop(self.im, self.dispose_extent)
                self._prev_im.paste(updated, self.dispose_extent, updated.convert('RGBA'))
                self.im = self._prev_im
        self._prev_im = self.im.copy
        self._prev_disposal_method = self.disposal_method

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