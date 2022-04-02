# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\GifImagePlugin.py
import itertools, os, subprocess
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
from ._binary import i8, i16le as i16, o8, o16le as o16

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

 L.  64         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               13
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  65        12  LOAD_FAST                's'
               14  LOAD_CONST               None
               16  LOAD_CONST               6
               18  BUILD_SLICE_2         2 
               20  BINARY_SUBSCR    
               22  LOAD_CONST               (b'GIF87a', b'GIF89a')
               24  COMPARE_OP               not-in
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.  66        28  LOAD_GLOBAL              SyntaxError
               30  LOAD_STR                 'not a GIF file'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.  68        36  LOAD_FAST                's'
               38  LOAD_CONST               None
               40  LOAD_CONST               6
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                info
               50  LOAD_STR                 'version'
               52  STORE_SUBSCR     

 L.  69        54  LOAD_GLOBAL              i16
               56  LOAD_FAST                's'
               58  LOAD_CONST               6
               60  LOAD_CONST               None
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_GLOBAL              i16
               70  LOAD_FAST                's'
               72  LOAD_CONST               8
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  ''
               82  BUILD_TUPLE_2         2 
               84  LOAD_FAST                'self'
               86  STORE_ATTR               _size

 L.  70        88  BUILD_LIST_0          0 
               90  LOAD_FAST                'self'
               92  STORE_ATTR               tile

 L.  71        94  LOAD_GLOBAL              i8
               96  LOAD_FAST                's'
               98  LOAD_CONST               10
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'flags'

 L.  72       106  LOAD_FAST                'flags'
              108  LOAD_CONST               7
              110  BINARY_AND       
              112  LOAD_CONST               1
              114  BINARY_ADD       
              116  STORE_FAST               'bits'

 L.  74       118  LOAD_FAST                'flags'
              120  LOAD_CONST               128
              122  BINARY_AND       
          124_126  POP_JUMP_IF_FALSE   282  'to 282'

 L.  76       128  LOAD_GLOBAL              i8
              130  LOAD_FAST                's'
              132  LOAD_CONST               11
              134  BINARY_SUBSCR    
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                info
              142  LOAD_STR                 'background'
              144  STORE_SUBSCR     

 L.  78       146  LOAD_FAST                'self'
              148  LOAD_ATTR                fp
              150  LOAD_METHOD              read
              152  LOAD_CONST               3
              154  LOAD_FAST                'bits'
              156  BINARY_LSHIFT    
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'p'

 L.  79       162  LOAD_GLOBAL              range
              164  LOAD_CONST               0
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'p'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_CONST               3
              174  CALL_FUNCTION_3       3  ''
              176  GET_ITER         
            178_0  COME_FROM           280  '280'
            178_1  COME_FROM           244  '244'
              178  FOR_ITER            282  'to 282'
              180  STORE_FAST               'i'

 L.  80       182  LOAD_FAST                'i'
              184  LOAD_CONST               3
              186  BINARY_FLOOR_DIVIDE
              188  LOAD_GLOBAL              i8
              190  LOAD_FAST                'p'
              192  LOAD_FAST                'i'
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  DUP_TOP          
              200  ROT_THREE        
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   248  'to 248'
              206  LOAD_GLOBAL              i8
              208  LOAD_FAST                'p'
              210  LOAD_FAST                'i'
              212  LOAD_CONST               1
              214  BINARY_ADD       
              216  BINARY_SUBSCR    
              218  CALL_FUNCTION_1       1  ''
              220  DUP_TOP          
              222  ROT_THREE        
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   248  'to 248'
              228  LOAD_GLOBAL              i8
              230  LOAD_FAST                'p'
              232  LOAD_FAST                'i'
              234  LOAD_CONST               2
              236  BINARY_ADD       
              238  BINARY_SUBSCR    
              240  CALL_FUNCTION_1       1  ''
              242  COMPARE_OP               ==
              244  POP_JUMP_IF_TRUE_BACK   178  'to 178'
              246  JUMP_FORWARD        250  'to 250'
            248_0  COME_FROM           226  '226'
            248_1  COME_FROM           204  '204'
              248  POP_TOP          
            250_0  COME_FROM           246  '246'

 L.  81       250  LOAD_GLOBAL              ImagePalette
              252  LOAD_METHOD              raw
              254  LOAD_STR                 'RGB'
              256  LOAD_FAST                'p'
              258  CALL_METHOD_2         2  ''
              260  STORE_FAST               'p'

 L.  82       262  LOAD_FAST                'p'
              264  DUP_TOP          
              266  LOAD_FAST                'self'
              268  STORE_ATTR               global_palette
              270  LOAD_FAST                'self'
              272  STORE_ATTR               palette

 L.  83       274  POP_TOP          
          276_278  BREAK_LOOP          282  'to 282'
              280  JUMP_BACK           178  'to 178'
            282_0  COME_FROM           276  '276'
            282_1  COME_FROM           178  '178'
            282_2  COME_FROM           124  '124'

 L.  85       282  LOAD_FAST                'self'
              284  LOAD_ATTR                fp
              286  LOAD_FAST                'self'
              288  STORE_ATTR               _GifImageFile__fp

 L.  86       290  LOAD_FAST                'self'
              292  LOAD_ATTR                fp
              294  LOAD_METHOD              tell
              296  CALL_METHOD_0         0  ''
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _GifImageFile__rewind

 L.  87       302  LOAD_CONST               None
              304  LOAD_FAST                'self'
              306  STORE_ATTR               _n_frames

 L.  88       308  LOAD_CONST               None
              310  LOAD_FAST                'self'
              312  STORE_ATTR               _is_animated

 L.  89       314  LOAD_FAST                'self'
              316  LOAD_METHOD              _seek
              318  LOAD_CONST               0
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 248_1

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
            except EOFError:
                self.seek(last_frame)
                raise EOFError('no more images in GIF file')

    def _seek--- This code section failed: ---

 L. 138         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    68  'to 68'

 L. 140         8  LOAD_CONST               0
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _GifImageFile__offset

 L. 141        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               dispose

 L. 142        20  LOAD_CONST               0
               22  LOAD_CONST               0
               24  LOAD_CONST               0
               26  LOAD_CONST               0
               28  BUILD_LIST_4          4 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               dispose_extent

 L. 143        34  LOAD_CONST               -1
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _GifImageFile__frame

 L. 144        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _GifImageFile__fp
               44  LOAD_METHOD              seek
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _GifImageFile__rewind
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 145        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _prev_im

 L. 146        60  LOAD_CONST               0
               62  LOAD_FAST                'self'
               64  STORE_ATTR               disposal_method
               66  JUMP_FORWARD         82  'to 82'
             68_0  COME_FROM             6  '6'

 L. 149        68  LOAD_FAST                'self'
               70  LOAD_ATTR                im
               72  POP_JUMP_IF_TRUE     82  'to 82'

 L. 150        74  LOAD_FAST                'self'
               76  LOAD_METHOD              load
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            66  '66'

 L. 152        82  LOAD_FAST                'frame'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _GifImageFile__frame
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  COMPARE_OP               !=
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 153        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'cannot seek to frame %d'
              100  LOAD_FAST                'frame'
              102  BINARY_MODULO    
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'

 L. 154       108  LOAD_FAST                'frame'
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _GifImageFile__frame

 L. 156       114  BUILD_LIST_0          0 
              116  LOAD_FAST                'self'
              118  STORE_ATTR               tile

 L. 158       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _GifImageFile__fp
              124  LOAD_FAST                'self'
              126  STORE_ATTR               fp

 L. 159       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _GifImageFile__offset
              132  POP_JUMP_IF_FALSE   164  'to 164'

 L. 161       134  LOAD_FAST                'self'
              136  LOAD_ATTR                fp
              138  LOAD_METHOD              seek
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _GifImageFile__offset
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
            148_0  COME_FROM           156  '156'

 L. 162       148  LOAD_FAST                'self'
              150  LOAD_METHOD              data
              152  CALL_METHOD_0         0  ''
              154  POP_JUMP_IF_FALSE   158  'to 158'

 L. 163       156  JUMP_BACK           148  'to 148'
            158_0  COME_FROM           154  '154'

 L. 164       158  LOAD_CONST               0
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _GifImageFile__offset
            164_0  COME_FROM           132  '132'

 L. 166       164  LOAD_FAST                'self'
              166  LOAD_ATTR                dispose
              168  POP_JUMP_IF_FALSE   188  'to 188'

 L. 167       170  LOAD_FAST                'self'
              172  LOAD_ATTR                im
              174  LOAD_METHOD              paste
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                dispose
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                dispose_extent
              184  CALL_METHOD_2         2  ''
              186  POP_TOP          
            188_0  COME_FROM           168  '168'

 L. 169       188  LOAD_CONST               0
              190  LOAD_CONST               ('copy',)
              192  IMPORT_NAME              copy
              194  IMPORT_FROM              copy
              196  STORE_FAST               'copy'
              198  POP_TOP          

 L. 171       200  LOAD_FAST                'copy'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                global_palette
              206  CALL_FUNCTION_1       1  ''
              208  LOAD_FAST                'self'
              210  STORE_ATTR               palette

 L. 173       212  BUILD_MAP_0           0 
              214  STORE_FAST               'info'
            216_0  COME_FROM           890  '890'
            216_1  COME_FROM           888  '888'
            216_2  COME_FROM           584  '584'
            216_3  COME_FROM           576  '576'
            216_4  COME_FROM           448  '448'
            216_5  COME_FROM           398  '398'
            216_6  COME_FROM           244  '244'

 L. 176       216  LOAD_FAST                'self'
              218  LOAD_ATTR                fp
              220  LOAD_METHOD              read
              222  LOAD_CONST               1
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               's'

 L. 177       228  LOAD_FAST                's'
              230  POP_JUMP_IF_FALSE   240  'to 240'
              232  LOAD_FAST                's'
              234  LOAD_CONST               b';'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_FALSE   246  'to 246'
            240_0  COME_FROM           230  '230'

 L. 178   240_242  JUMP_FORWARD        892  'to 892'
              244  JUMP_BACK           216  'to 216'
            246_0  COME_FROM           238  '238'

 L. 180       246  LOAD_FAST                's'
              248  LOAD_CONST               b'!'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   578  'to 578'

 L. 184       256  LOAD_FAST                'self'
              258  LOAD_ATTR                fp
              260  LOAD_METHOD              read
              262  LOAD_CONST               1
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               's'

 L. 185       268  LOAD_FAST                'self'
              270  LOAD_METHOD              data
              272  CALL_METHOD_0         0  ''
              274  STORE_FAST               'block'

 L. 186       276  LOAD_GLOBAL              i8
              278  LOAD_FAST                's'
              280  CALL_FUNCTION_1       1  ''
              282  LOAD_CONST               249
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   382  'to 382'

 L. 190       290  LOAD_GLOBAL              i8
              292  LOAD_FAST                'block'
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               'flags'

 L. 191       302  LOAD_FAST                'flags'
              304  LOAD_CONST               1
              306  BINARY_AND       
          308_310  POP_JUMP_IF_FALSE   328  'to 328'

 L. 192       312  LOAD_GLOBAL              i8
              314  LOAD_FAST                'block'
              316  LOAD_CONST               3
              318  BINARY_SUBSCR    
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_FAST                'info'
              324  LOAD_STR                 'transparency'
              326  STORE_SUBSCR     
            328_0  COME_FROM           308  '308'

 L. 193       328  LOAD_GLOBAL              i16
              330  LOAD_FAST                'block'
              332  LOAD_CONST               1
              334  LOAD_CONST               3
              336  BUILD_SLICE_2         2 
              338  BINARY_SUBSCR    
              340  CALL_FUNCTION_1       1  ''
              342  LOAD_CONST               10
              344  BINARY_MULTIPLY  
              346  LOAD_FAST                'info'
              348  LOAD_STR                 'duration'
              350  STORE_SUBSCR     

 L. 196       352  LOAD_CONST               28
              354  LOAD_FAST                'flags'
              356  BINARY_AND       
              358  STORE_FAST               'dispose_bits'

 L. 197       360  LOAD_FAST                'dispose_bits'
              362  LOAD_CONST               2
              364  BINARY_RSHIFT    
              366  STORE_FAST               'dispose_bits'

 L. 198       368  LOAD_FAST                'dispose_bits'
          370_372  POP_JUMP_IF_FALSE   562  'to 562'

 L. 203       374  LOAD_FAST                'dispose_bits'
              376  LOAD_FAST                'self'
              378  STORE_ATTR               disposal_method
              380  JUMP_FORWARD        562  'to 562'
            382_0  COME_FROM           286  '286'

 L. 204       382  LOAD_GLOBAL              i8
              384  LOAD_FAST                's'
              386  CALL_FUNCTION_1       1  ''
              388  LOAD_CONST               254
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   452  'to 452'
            396_0  COME_FROM           444  '444'

 L. 208       396  LOAD_FAST                'block'
              398  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 209       400  LOAD_STR                 'comment'
              402  LOAD_FAST                'info'
              404  COMPARE_OP               in
          406_408  POP_JUMP_IF_FALSE   428  'to 428'

 L. 210       410  LOAD_FAST                'info'
              412  LOAD_STR                 'comment'
              414  DUP_TOP_TWO      
              416  BINARY_SUBSCR    
              418  LOAD_FAST                'block'
              420  INPLACE_ADD      
              422  ROT_THREE        
              424  STORE_SUBSCR     
              426  JUMP_FORWARD        436  'to 436'
            428_0  COME_FROM           406  '406'

 L. 212       428  LOAD_FAST                'block'
              430  LOAD_FAST                'info'
              432  LOAD_STR                 'comment'
              434  STORE_SUBSCR     
            436_0  COME_FROM           426  '426'

 L. 213       436  LOAD_FAST                'self'
              438  LOAD_METHOD              data
              440  CALL_METHOD_0         0  ''
              442  STORE_FAST               'block'
          444_446  JUMP_BACK           396  'to 396'

 L. 214       448  JUMP_BACK           216  'to 216'
              450  BREAK_LOOP          562  'to 562'
            452_0  COME_FROM           392  '392'

 L. 215       452  LOAD_GLOBAL              i8
              454  LOAD_FAST                's'
              456  CALL_FUNCTION_1       1  ''
              458  LOAD_CONST               255
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   562  'to 562'

 L. 219       466  LOAD_FAST                'block'
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                fp
              472  LOAD_METHOD              tell
              474  CALL_METHOD_0         0  ''
              476  BUILD_TUPLE_2         2 
              478  LOAD_FAST                'info'
              480  LOAD_STR                 'extension'
              482  STORE_SUBSCR     

 L. 220       484  LOAD_FAST                'block'
              486  LOAD_CONST               None
              488  LOAD_CONST               11
              490  BUILD_SLICE_2         2 
              492  BINARY_SUBSCR    
              494  LOAD_CONST               b'NETSCAPE2.0'
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   562  'to 562'

 L. 221       502  LOAD_FAST                'self'
              504  LOAD_METHOD              data
              506  CALL_METHOD_0         0  ''
              508  STORE_FAST               'block'

 L. 222       510  LOAD_GLOBAL              len
              512  LOAD_FAST                'block'
              514  CALL_FUNCTION_1       1  ''
              516  LOAD_CONST               3
              518  COMPARE_OP               >=
          520_522  POP_JUMP_IF_FALSE   562  'to 562'
              524  LOAD_GLOBAL              i8
              526  LOAD_FAST                'block'
              528  LOAD_CONST               0
              530  BINARY_SUBSCR    
              532  CALL_FUNCTION_1       1  ''
              534  LOAD_CONST               1
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   562  'to 562'

 L. 223       542  LOAD_GLOBAL              i16
              544  LOAD_FAST                'block'
              546  LOAD_CONST               1
              548  LOAD_CONST               3
              550  BUILD_SLICE_2         2 
              552  BINARY_SUBSCR    
              554  CALL_FUNCTION_1       1  ''
              556  LOAD_FAST                'info'
              558  LOAD_STR                 'loop'
              560  STORE_SUBSCR     
            562_0  COME_FROM           572  '572'
            562_1  COME_FROM           538  '538'
            562_2  COME_FROM           520  '520'
            562_3  COME_FROM           498  '498'
            562_4  COME_FROM           462  '462'
            562_5  COME_FROM           450  '450'
            562_6  COME_FROM           380  '380'
            562_7  COME_FROM           370  '370'

 L. 224       562  LOAD_FAST                'self'
              564  LOAD_METHOD              data
              566  CALL_METHOD_0         0  ''
          568_570  POP_JUMP_IF_FALSE   890  'to 890'

 L. 225   572_574  JUMP_BACK           562  'to 562'
              576  JUMP_BACK           216  'to 216'
            578_0  COME_FROM           252  '252'

 L. 227       578  LOAD_FAST                's'
              580  LOAD_CONST               b','
              582  COMPARE_OP               ==
              584  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 231       586  LOAD_FAST                'self'
              588  LOAD_ATTR                fp
              590  LOAD_METHOD              read
              592  LOAD_CONST               9
              594  CALL_METHOD_1         1  ''
              596  STORE_FAST               's'

 L. 234       598  LOAD_GLOBAL              i16
              600  LOAD_FAST                's'
              602  LOAD_CONST               0
              604  LOAD_CONST               None
              606  BUILD_SLICE_2         2 
              608  BINARY_SUBSCR    
              610  CALL_FUNCTION_1       1  ''
              612  LOAD_GLOBAL              i16
              614  LOAD_FAST                's'
              616  LOAD_CONST               2
              618  LOAD_CONST               None
              620  BUILD_SLICE_2         2 
              622  BINARY_SUBSCR    
              624  CALL_FUNCTION_1       1  ''
              626  ROT_TWO          
              628  STORE_FAST               'x0'
              630  STORE_FAST               'y0'

 L. 235       632  LOAD_FAST                'x0'
              634  LOAD_GLOBAL              i16
              636  LOAD_FAST                's'
              638  LOAD_CONST               4
              640  LOAD_CONST               None
              642  BUILD_SLICE_2         2 
              644  BINARY_SUBSCR    
              646  CALL_FUNCTION_1       1  ''
              648  BINARY_ADD       
              650  LOAD_FAST                'y0'
              652  LOAD_GLOBAL              i16
              654  LOAD_FAST                's'
              656  LOAD_CONST               6
              658  LOAD_CONST               None
              660  BUILD_SLICE_2         2 
              662  BINARY_SUBSCR    
              664  CALL_FUNCTION_1       1  ''
              666  BINARY_ADD       
              668  ROT_TWO          
              670  STORE_FAST               'x1'
              672  STORE_FAST               'y1'

 L. 236       674  LOAD_FAST                'x1'
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                size
              680  LOAD_CONST               0
              682  BINARY_SUBSCR    
              684  COMPARE_OP               >
          686_688  POP_JUMP_IF_TRUE    706  'to 706'
              690  LOAD_FAST                'y1'
              692  LOAD_FAST                'self'
              694  LOAD_ATTR                size
              696  LOAD_CONST               1
              698  BINARY_SUBSCR    
              700  COMPARE_OP               >
          702_704  POP_JUMP_IF_FALSE   740  'to 740'
            706_0  COME_FROM           686  '686'

 L. 237       706  LOAD_GLOBAL              max
              708  LOAD_FAST                'x1'
              710  LOAD_FAST                'self'
              712  LOAD_ATTR                size
              714  LOAD_CONST               0
              716  BINARY_SUBSCR    
              718  CALL_FUNCTION_2       2  ''
              720  LOAD_GLOBAL              max
              722  LOAD_FAST                'y1'
              724  LOAD_FAST                'self'
              726  LOAD_ATTR                size
              728  LOAD_CONST               1
              730  BINARY_SUBSCR    
              732  CALL_FUNCTION_2       2  ''
              734  BUILD_TUPLE_2         2 
              736  LOAD_FAST                'self'
              738  STORE_ATTR               _size
            740_0  COME_FROM           702  '702'

 L. 238       740  LOAD_FAST                'x0'
              742  LOAD_FAST                'y0'
              744  LOAD_FAST                'x1'
              746  LOAD_FAST                'y1'
              748  BUILD_TUPLE_4         4 
              750  LOAD_FAST                'self'
              752  STORE_ATTR               dispose_extent

 L. 239       754  LOAD_GLOBAL              i8
              756  LOAD_FAST                's'
              758  LOAD_CONST               8
              760  BINARY_SUBSCR    
              762  CALL_FUNCTION_1       1  ''
              764  STORE_FAST               'flags'

 L. 241       766  LOAD_FAST                'flags'
              768  LOAD_CONST               64
              770  BINARY_AND       
              772  LOAD_CONST               0
              774  COMPARE_OP               !=
              776  STORE_FAST               'interlace'

 L. 243       778  LOAD_FAST                'flags'
              780  LOAD_CONST               128
              782  BINARY_AND       
          784_786  POP_JUMP_IF_FALSE   826  'to 826'

 L. 244       788  LOAD_FAST                'flags'
              790  LOAD_CONST               7
              792  BINARY_AND       
              794  LOAD_CONST               1
              796  BINARY_ADD       
              798  STORE_FAST               'bits'

 L. 245       800  LOAD_GLOBAL              ImagePalette
              802  LOAD_METHOD              raw
              804  LOAD_STR                 'RGB'
              806  LOAD_FAST                'self'
              808  LOAD_ATTR                fp
              810  LOAD_METHOD              read
              812  LOAD_CONST               3
              814  LOAD_FAST                'bits'
              816  BINARY_LSHIFT    
              818  CALL_METHOD_1         1  ''
              820  CALL_METHOD_2         2  ''
              822  LOAD_FAST                'self'
              824  STORE_ATTR               palette
            826_0  COME_FROM           784  '784'

 L. 248       826  LOAD_GLOBAL              i8
              828  LOAD_FAST                'self'
              830  LOAD_ATTR                fp
              832  LOAD_METHOD              read
              834  LOAD_CONST               1
              836  CALL_METHOD_1         1  ''
              838  CALL_FUNCTION_1       1  ''
              840  STORE_FAST               'bits'

 L. 249       842  LOAD_FAST                'self'
              844  LOAD_ATTR                fp
              846  LOAD_METHOD              tell
              848  CALL_METHOD_0         0  ''
              850  LOAD_FAST                'self'
              852  STORE_ATTR               _GifImageFile__offset

 L. 251       854  LOAD_STR                 'gif'
              856  LOAD_FAST                'x0'
              858  LOAD_FAST                'y0'
              860  LOAD_FAST                'x1'
              862  LOAD_FAST                'y1'
              864  BUILD_TUPLE_4         4 
              866  LOAD_FAST                'self'
              868  LOAD_ATTR                _GifImageFile__offset
              870  LOAD_FAST                'bits'
              872  LOAD_FAST                'interlace'
              874  BUILD_TUPLE_2         2 
              876  BUILD_TUPLE_4         4 

 L. 250       878  BUILD_LIST_1          1 
              880  LOAD_FAST                'self'
              882  STORE_ATTR               tile

 L. 253   884_886  JUMP_FORWARD        892  'to 892'
              888  JUMP_BACK           216  'to 216'
            890_0  COME_FROM           568  '568'

 L. 256       890  JUMP_BACK           216  'to 216'
            892_0  COME_FROM           884  '884'
            892_1  COME_FROM           240  '240'

 L. 259       892  SETUP_FINALLY      1016  'to 1016'

 L. 260       894  LOAD_FAST                'self'
              896  LOAD_ATTR                disposal_method
              898  LOAD_CONST               2
              900  COMPARE_OP               <
          902_904  POP_JUMP_IF_FALSE   914  'to 914'

 L. 262       906  LOAD_CONST               None
              908  LOAD_FAST                'self'
              910  STORE_ATTR               dispose
              912  JUMP_FORWARD        986  'to 986'
            914_0  COME_FROM           902  '902'

 L. 263       914  LOAD_FAST                'self'
              916  LOAD_ATTR                disposal_method
              918  LOAD_CONST               2
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   966  'to 966'

 L. 265       926  LOAD_GLOBAL              Image
              928  LOAD_METHOD              _decompression_bomb_check
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                size
              934  CALL_METHOD_1         1  ''
              936  POP_TOP          

 L. 266       938  LOAD_GLOBAL              Image
              940  LOAD_ATTR                core
              942  LOAD_METHOD              fill
              944  LOAD_STR                 'P'
              946  LOAD_FAST                'self'
              948  LOAD_ATTR                size
              950  LOAD_FAST                'self'
              952  LOAD_ATTR                info
              954  LOAD_STR                 'background'
              956  BINARY_SUBSCR    
              958  CALL_METHOD_3         3  ''
              960  LOAD_FAST                'self'
              962  STORE_ATTR               dispose
              964  JUMP_FORWARD        986  'to 986'
            966_0  COME_FROM           922  '922'

 L. 269       966  LOAD_FAST                'self'
              968  LOAD_ATTR                im
          970_972  POP_JUMP_IF_FALSE   986  'to 986'

 L. 270       974  LOAD_FAST                'self'
              976  LOAD_ATTR                im
              978  LOAD_METHOD              copy
              980  CALL_METHOD_0         0  ''
              982  LOAD_FAST                'self'
              984  STORE_ATTR               dispose
            986_0  COME_FROM           970  '970'
            986_1  COME_FROM           964  '964'
            986_2  COME_FROM           912  '912'

 L. 273       986  LOAD_FAST                'self'
              988  LOAD_ATTR                dispose
          990_992  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 274       994  LOAD_FAST                'self'
              996  LOAD_METHOD              _crop
              998  LOAD_FAST                'self'
             1000  LOAD_ATTR                dispose
             1002  LOAD_FAST                'self'
             1004  LOAD_ATTR                dispose_extent
             1006  CALL_METHOD_2         2  ''
             1008  LOAD_FAST                'self'
             1010  STORE_ATTR               dispose
           1012_0  COME_FROM           990  '990'
             1012  POP_BLOCK        
             1014  JUMP_FORWARD       1042  'to 1042'
           1016_0  COME_FROM_FINALLY   892  '892'

 L. 275      1016  DUP_TOP          
             1018  LOAD_GLOBAL              AttributeError
             1020  LOAD_GLOBAL              KeyError
             1022  BUILD_TUPLE_2         2 
             1024  COMPARE_OP               exception-match
         1026_1028  POP_JUMP_IF_FALSE  1040  'to 1040'
             1030  POP_TOP          
             1032  POP_TOP          
             1034  POP_TOP          

 L. 276      1036  POP_EXCEPT       
             1038  BREAK_LOOP         1042  'to 1042'
           1040_0  COME_FROM          1026  '1026'
             1040  END_FINALLY      
           1042_0  COME_FROM          1038  '1038'
           1042_1  COME_FROM          1014  '1014'

 L. 278      1042  LOAD_FAST                'self'
             1044  LOAD_ATTR                tile
         1046_1048  POP_JUMP_IF_TRUE   1054  'to 1054'

 L. 280      1050  LOAD_GLOBAL              EOFError
             1052  RAISE_VARARGS_1       1  'exception instance'
           1054_0  COME_FROM          1046  '1046'

 L. 282      1054  LOAD_CONST               ('transparency', 'duration', 'comment', 'extension', 'loop')
             1056  GET_ITER         
           1058_0  COME_FROM          1108  '1108'
           1058_1  COME_FROM          1096  '1096'
           1058_2  COME_FROM          1086  '1086'
             1058  FOR_ITER           1112  'to 1112'
             1060  STORE_FAST               'k'

 L. 283      1062  LOAD_FAST                'k'
             1064  LOAD_FAST                'info'
             1066  COMPARE_OP               in
         1068_1070  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 284      1072  LOAD_FAST                'info'
             1074  LOAD_FAST                'k'
             1076  BINARY_SUBSCR    
             1078  LOAD_FAST                'self'
             1080  LOAD_ATTR                info
             1082  LOAD_FAST                'k'
             1084  STORE_SUBSCR     
             1086  JUMP_BACK          1058  'to 1058'
           1088_0  COME_FROM          1068  '1068'

 L. 285      1088  LOAD_FAST                'k'
             1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                info
             1094  COMPARE_OP               in
         1096_1098  POP_JUMP_IF_FALSE_BACK  1058  'to 1058'

 L. 286      1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                info
             1104  LOAD_FAST                'k'
             1106  DELETE_SUBSCR    
         1108_1110  JUMP_BACK          1058  'to 1058'
           1112_0  COME_FROM          1058  '1058'

 L. 288      1112  LOAD_STR                 'L'
             1114  LOAD_FAST                'self'
             1116  STORE_ATTR               mode

 L. 289      1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                palette
         1122_1124  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 290      1126  LOAD_STR                 'P'
             1128  LOAD_FAST                'self'
             1130  STORE_ATTR               mode
           1132_0  COME_FROM          1122  '1122'

Parse error at or near `JUMP_BACK' instruction at offset 576

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
    import math
    if not palette_bytes:
        return 0
    if len(palette_bytes) < 9:
        return 1
    return int(math.ceil(math.log(len(palette_bytes) // 3, 2))) - 1


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

 L. 760         0  LOAD_CONST               b'87a'
                2  STORE_FAST               'version'

 L. 761         4  LOAD_CONST               ('transparency', 'duration', 'loop', 'comment')
                6  GET_ITER         
              8_0  COME_FROM            92  '92'
              8_1  COME_FROM            82  '82'
              8_2  COME_FROM            78  '78'
              8_3  COME_FROM            42  '42'
              8_4  COME_FROM            22  '22'
              8_5  COME_FROM            14  '14'
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'extensionKey'

 L. 762        12  LOAD_FAST                'info'
               14  POP_JUMP_IF_FALSE_BACK     8  'to 8'
               16  LOAD_FAST                'extensionKey'
               18  LOAD_FAST                'info'
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 763        24  LOAD_FAST                'extensionKey'
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

 L. 764        44  LOAD_FAST                'extensionKey'
               46  LOAD_STR                 'comment'
               48  COMPARE_OP               ==

 L. 763        50  POP_JUMP_IF_FALSE    84  'to 84'

 L. 764        52  LOAD_CONST               1

 L. 764        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'extensionKey'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''

 L. 763        64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 764        72  LOAD_CONST               255

 L. 763        74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE     84  'to 84'
               78  JUMP_BACK             8  'to 8'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          

 L. 766        82  JUMP_BACK             8  'to 8'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            50  '50'

 L. 767        84  LOAD_CONST               b'89a'
               86  STORE_FAST               'version'

 L. 768        88  POP_TOP          
               90  BREAK_LOOP          114  'to 114'
               92  JUMP_BACK             8  'to 8'
             94_0  COME_FROM             8  '8'

 L. 770        94  LOAD_FAST                'im'
               96  LOAD_ATTR                info
               98  LOAD_METHOD              get
              100  LOAD_STR                 'version'
              102  CALL_METHOD_1         1  ''
              104  LOAD_CONST               b'89a'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 771       110  LOAD_CONST               b'89a'
              112  STORE_FAST               'version'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            90  '90'

 L. 773       114  LOAD_GLOBAL              _get_background
              116  LOAD_FAST                'im'
              118  LOAD_FAST                'info'
              120  LOAD_METHOD              get
              122  LOAD_STR                 'background'
              124  CALL_METHOD_1         1  ''
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'background'

 L. 775       130  LOAD_GLOBAL              _get_palette_bytes
              132  LOAD_FAST                'im'
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'palette_bytes'

 L. 776       138  LOAD_GLOBAL              _get_color_table_size
              140  LOAD_FAST                'palette_bytes'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'color_table_size'

 L. 779       146  LOAD_CONST               b'GIF'

 L. 780       148  LOAD_FAST                'version'

 L. 779       150  BINARY_ADD       

 L. 781       152  LOAD_GLOBAL              o16
              154  LOAD_FAST                'im'
              156  LOAD_ATTR                size
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''

 L. 779       164  BINARY_ADD       

 L. 782       166  LOAD_GLOBAL              o16
              168  LOAD_FAST                'im'
              170  LOAD_ATTR                size
              172  LOAD_CONST               1
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  ''

 L. 779       178  BINARY_ADD       

 L. 785       180  LOAD_GLOBAL              o8
              182  LOAD_FAST                'color_table_size'
              184  LOAD_CONST               128
              186  BINARY_ADD       
              188  CALL_FUNCTION_1       1  ''

 L. 787       190  LOAD_GLOBAL              o8
              192  LOAD_FAST                'background'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_GLOBAL              o8
              198  LOAD_CONST               0
              200  CALL_FUNCTION_1       1  ''
              202  BINARY_ADD       

 L. 789       204  LOAD_GLOBAL              _get_header_palette
              206  LOAD_FAST                'palette_bytes'
              208  CALL_FUNCTION_1       1  ''

 L. 778       210  BUILD_LIST_4          4 
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