# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\GifImagePlugin.py
import itertools, math, os, subprocess
from . import Image, ImageChops, ImageFile, ImagePalette, ImageSequence
from ._binary import i16le as i16
from ._binary import o8
from ._binary import o16le as o16

def _accept--- This code section failed: ---

 L.  42         0  LOAD_FAST                'prefix'
                2  LOAD_CONST               None
                4  LOAD_CONST               6
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_CONST               (b'GIF87a', b'GIF89a')
               12  <118>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


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
    def n_frames--- This code section failed: ---

 L.  96         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _n_frames
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    86  'to 86'

 L.  97        10  LOAD_FAST                'self'
               12  LOAD_METHOD              tell
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'current'

 L.  98        18  SETUP_FINALLY        44  'to 44'
             20_0  COME_FROM            38  '38'

 L. 100        20  LOAD_FAST                'self'
               22  LOAD_METHOD              seek
               24  LOAD_FAST                'self'
               26  LOAD_METHOD              tell
               28  CALL_METHOD_0         0  ''
               30  LOAD_CONST               1
               32  BINARY_ADD       
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK            20  'to 20'
               40  POP_BLOCK        
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM_FINALLY    18  '18'

 L. 101        44  DUP_TOP          
               46  LOAD_GLOBAL              EOFError
               48  <121>                74  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 102        56  LOAD_FAST                'self'
               58  LOAD_METHOD              tell
               60  CALL_METHOD_0         0  ''
               62  LOAD_CONST               1
               64  BINARY_ADD       
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _n_frames
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            42  '42'

 L. 103        76  LOAD_FAST                'self'
               78  LOAD_METHOD              seek
               80  LOAD_FAST                'current'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM             8  '8'

 L. 104        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _n_frames
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def is_animated--- This code section failed: ---

 L. 108         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _is_animated
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    98  'to 98'

 L. 109        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _n_frames
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 110        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _n_frames
               24  LOAD_CONST               1
               26  COMPARE_OP               !=
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _is_animated
               32  JUMP_FORWARD         98  'to 98'
             34_0  COME_FROM            18  '18'

 L. 112        34  LOAD_FAST                'self'
               36  LOAD_METHOD              tell
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'current'

 L. 114        42  SETUP_FINALLY        64  'to 64'

 L. 115        44  LOAD_FAST                'self'
               46  LOAD_METHOD              seek
               48  LOAD_CONST               1
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 116        54  LOAD_CONST               True
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _is_animated
               60  POP_BLOCK        
               62  JUMP_FORWARD         88  'to 88'
             64_0  COME_FROM_FINALLY    42  '42'

 L. 117        64  DUP_TOP          
               66  LOAD_GLOBAL              EOFError
               68  <121>                86  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 118        76  LOAD_CONST               False
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _is_animated
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            62  '62'

 L. 120        88  LOAD_FAST                'self'
               90  LOAD_METHOD              seek
               92  LOAD_FAST                'current'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
             98_0  COME_FROM            32  '32'
             98_1  COME_FROM             8  '8'

 L. 121        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _is_animated
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def seek--- This code section failed: ---

 L. 124         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'frame'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 125        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 126        14  LOAD_FAST                'frame'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _GifImageFile__frame
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    48  'to 48'

 L. 127        24  LOAD_FAST                'frame'
               26  LOAD_CONST               0
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L. 128        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               im
             38_0  COME_FROM            30  '30'

 L. 129        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _seek
               42  LOAD_CONST               0
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            22  '22'

 L. 131        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _GifImageFile__frame
               52  STORE_FAST               'last_frame'

 L. 132        54  LOAD_GLOBAL              range
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _GifImageFile__frame
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  LOAD_FAST                'frame'
               66  LOAD_CONST               1
               68  BINARY_ADD       
               70  CALL_FUNCTION_2       2  ''
               72  GET_ITER         
             74_0  COME_FROM           150  '150'
             74_1  COME_FROM           138  '138'
             74_2  COME_FROM            92  '92'
               74  FOR_ITER            152  'to 152'
               76  STORE_FAST               'f'

 L. 133        78  SETUP_FINALLY        94  'to 94'

 L. 134        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _seek
               84  LOAD_FAST                'f'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  JUMP_BACK            74  'to 74'
             94_0  COME_FROM_FINALLY    78  '78'

 L. 135        94  DUP_TOP          
               96  LOAD_GLOBAL              EOFError
               98  <121>               148  ''
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       140  'to 140'

 L. 136       108  LOAD_FAST                'self'
              110  LOAD_METHOD              seek
              112  LOAD_FAST                'last_frame'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 137       118  LOAD_GLOBAL              EOFError
              120  LOAD_STR                 'no more images in GIF file'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'e'
              126  RAISE_VARARGS_2       2  'exception instance with __cause__'
              128  POP_BLOCK        
              130  POP_EXCEPT       
              132  LOAD_CONST               None
              134  STORE_FAST               'e'
              136  DELETE_FAST              'e'
              138  JUMP_BACK            74  'to 74'
            140_0  COME_FROM_FINALLY   106  '106'
              140  LOAD_CONST               None
              142  STORE_FAST               'e'
              144  DELETE_FAST              'e'
              146  <48>             
              148  <48>             
              150  JUMP_BACK            74  'to 74'
            152_0  COME_FROM            74  '74'

Parse error at or near `<121>' instruction at offset 98

    def _seek--- This code section failed: ---

 L. 141         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    58  'to 58'

 L. 143         8  LOAD_CONST               0
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _GifImageFile__offset

 L. 144        14  LOAD_CONST               None
               16  LOAD_FAST                'self'
               18  STORE_ATTR               dispose

 L. 145        20  BUILD_LIST_0          0 
               22  LOAD_CONST               (0, 0, 0, 0)
               24  CALL_FINALLY         27  'to 27'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               dispose_extent

 L. 146        30  LOAD_CONST               -1
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _GifImageFile__frame

 L. 147        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _GifImageFile__fp
               40  LOAD_METHOD              seek
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _GifImageFile__rewind
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 148        50  LOAD_CONST               0
               52  LOAD_FAST                'self'
               54  STORE_ATTR               disposal_method
               56  JUMP_FORWARD         72  'to 72'
             58_0  COME_FROM             6  '6'

 L. 151        58  LOAD_FAST                'self'
               60  LOAD_ATTR                tile
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 152        64  LOAD_FAST                'self'
               66  LOAD_METHOD              load
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM            56  '56'

 L. 154        72  LOAD_FAST                'frame'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _GifImageFile__frame
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  COMPARE_OP               !=
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 155        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 'cannot seek to frame '
               90  LOAD_FAST                'frame'
               92  FORMAT_VALUE          0  ''
               94  BUILD_STRING_2        2 
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            84  '84'

 L. 156       100  LOAD_FAST                'frame'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _GifImageFile__frame

 L. 158       106  BUILD_LIST_0          0 
              108  LOAD_FAST                'self'
              110  STORE_ATTR               tile

 L. 160       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _GifImageFile__fp
              116  LOAD_FAST                'self'
              118  STORE_ATTR               fp

 L. 161       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _GifImageFile__offset
              124  POP_JUMP_IF_FALSE   156  'to 156'

 L. 163       126  LOAD_FAST                'self'
              128  LOAD_ATTR                fp
              130  LOAD_METHOD              seek
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _GifImageFile__offset
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
            140_0  COME_FROM           148  '148'

 L. 164       140  LOAD_FAST                'self'
              142  LOAD_METHOD              data
              144  CALL_METHOD_0         0  ''
              146  POP_JUMP_IF_FALSE   150  'to 150'

 L. 165       148  JUMP_BACK           140  'to 140'
            150_0  COME_FROM           146  '146'

 L. 166       150  LOAD_CONST               0
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _GifImageFile__offset
            156_0  COME_FROM           124  '124'

 L. 168       156  LOAD_FAST                'self'
              158  LOAD_ATTR                dispose
              160  POP_JUMP_IF_FALSE   180  'to 180'

 L. 169       162  LOAD_FAST                'self'
              164  LOAD_ATTR                im
              166  LOAD_METHOD              paste
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                dispose
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                dispose_extent
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          
            180_0  COME_FROM           160  '160'

 L. 171       180  LOAD_CONST               0
              182  LOAD_CONST               ('copy',)
              184  IMPORT_NAME              copy
              186  IMPORT_FROM              copy
              188  STORE_FAST               'copy'
              190  POP_TOP          

 L. 173       192  LOAD_FAST                'copy'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                global_palette
              198  CALL_FUNCTION_1       1  ''
              200  LOAD_FAST                'self'
              202  STORE_ATTR               palette

 L. 175       204  BUILD_MAP_0           0 
              206  STORE_FAST               'info'

 L. 176       208  LOAD_CONST               None
              210  STORE_FAST               'frame_transparency'

 L. 177       212  LOAD_CONST               None
              214  STORE_FAST               'interlace'
            216_0  COME_FROM           804  '804'
            216_1  COME_FROM           802  '802'
            216_2  COME_FROM           556  '556'
            216_3  COME_FROM           548  '548'
            216_4  COME_FROM           430  '430'
            216_5  COME_FROM           380  '380'
            216_6  COME_FROM           244  '244'

 L. 180       216  LOAD_FAST                'self'
              218  LOAD_ATTR                fp
              220  LOAD_METHOD              read
              222  LOAD_CONST               1
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               's'

 L. 181       228  LOAD_FAST                's'
              230  POP_JUMP_IF_FALSE   240  'to 240'
              232  LOAD_FAST                's'
              234  LOAD_CONST               b';'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_FALSE   246  'to 246'
            240_0  COME_FROM           230  '230'

 L. 182   240_242  JUMP_FORWARD        806  'to 806'
              244  JUMP_BACK           216  'to 216'
            246_0  COME_FROM           238  '238'

 L. 184       246  LOAD_FAST                's'
              248  LOAD_CONST               b'!'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   550  'to 550'

 L. 188       256  LOAD_FAST                'self'
              258  LOAD_ATTR                fp
              260  LOAD_METHOD              read
              262  LOAD_CONST               1
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               's'

 L. 189       268  LOAD_FAST                'self'
              270  LOAD_METHOD              data
              272  CALL_METHOD_0         0  ''
              274  STORE_FAST               'block'

 L. 190       276  LOAD_FAST                's'
              278  LOAD_CONST               0
              280  BINARY_SUBSCR    
              282  LOAD_CONST               249
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   364  'to 364'

 L. 194       290  LOAD_FAST                'block'
              292  LOAD_CONST               0
              294  BINARY_SUBSCR    
              296  STORE_FAST               'flags'

 L. 195       298  LOAD_FAST                'flags'
              300  LOAD_CONST               1
              302  BINARY_AND       
          304_306  POP_JUMP_IF_FALSE   316  'to 316'

 L. 196       308  LOAD_FAST                'block'
              310  LOAD_CONST               3
              312  BINARY_SUBSCR    
              314  STORE_FAST               'frame_transparency'
            316_0  COME_FROM           304  '304'

 L. 197       316  LOAD_GLOBAL              i16
              318  LOAD_FAST                'block'
              320  LOAD_CONST               1
              322  CALL_FUNCTION_2       2  ''
              324  LOAD_CONST               10
              326  BINARY_MULTIPLY  
              328  LOAD_FAST                'info'
              330  LOAD_STR                 'duration'
              332  STORE_SUBSCR     

 L. 200       334  LOAD_CONST               28
              336  LOAD_FAST                'flags'
              338  BINARY_AND       
              340  STORE_FAST               'dispose_bits'

 L. 201       342  LOAD_FAST                'dispose_bits'
              344  LOAD_CONST               2
              346  BINARY_RSHIFT    
              348  STORE_FAST               'dispose_bits'

 L. 202       350  LOAD_FAST                'dispose_bits'
          352_354  POP_JUMP_IF_FALSE   534  'to 534'

 L. 207       356  LOAD_FAST                'dispose_bits'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               disposal_method
              362  JUMP_FORWARD        534  'to 534'
            364_0  COME_FROM           286  '286'

 L. 208       364  LOAD_FAST                's'
              366  LOAD_CONST               0
              368  BINARY_SUBSCR    
              370  LOAD_CONST               254
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   434  'to 434'
            378_0  COME_FROM           426  '426'

 L. 212       378  LOAD_FAST                'block'
              380  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 213       382  LOAD_STR                 'comment'
              384  LOAD_FAST                'info'
              386  <118>                 0  ''
          388_390  POP_JUMP_IF_FALSE   410  'to 410'

 L. 214       392  LOAD_FAST                'info'
              394  LOAD_STR                 'comment'
              396  DUP_TOP_TWO      
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'block'
              402  INPLACE_ADD      
              404  ROT_THREE        
              406  STORE_SUBSCR     
              408  JUMP_FORWARD        418  'to 418'
            410_0  COME_FROM           388  '388'

 L. 216       410  LOAD_FAST                'block'
              412  LOAD_FAST                'info'
              414  LOAD_STR                 'comment'
              416  STORE_SUBSCR     
            418_0  COME_FROM           408  '408'

 L. 217       418  LOAD_FAST                'self'
              420  LOAD_METHOD              data
              422  CALL_METHOD_0         0  ''
              424  STORE_FAST               'block'
          426_428  JUMP_BACK           378  'to 378'

 L. 218       430  JUMP_BACK           216  'to 216'
              432  BREAK_LOOP          534  'to 534'
            434_0  COME_FROM           374  '374'

 L. 219       434  LOAD_FAST                's'
              436  LOAD_CONST               0
              438  BINARY_SUBSCR    
              440  LOAD_CONST               255
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_FALSE   534  'to 534'

 L. 223       448  LOAD_FAST                'block'
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                fp
              454  LOAD_METHOD              tell
              456  CALL_METHOD_0         0  ''
              458  BUILD_TUPLE_2         2 
              460  LOAD_FAST                'info'
              462  LOAD_STR                 'extension'
              464  STORE_SUBSCR     

 L. 224       466  LOAD_FAST                'block'
              468  LOAD_CONST               None
              470  LOAD_CONST               11
              472  BUILD_SLICE_2         2 
              474  BINARY_SUBSCR    
              476  LOAD_CONST               b'NETSCAPE2.0'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   534  'to 534'

 L. 225       484  LOAD_FAST                'self'
              486  LOAD_METHOD              data
              488  CALL_METHOD_0         0  ''
              490  STORE_FAST               'block'

 L. 226       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'block'
              496  CALL_FUNCTION_1       1  ''
              498  LOAD_CONST               3
              500  COMPARE_OP               >=
          502_504  POP_JUMP_IF_FALSE   534  'to 534'
              506  LOAD_FAST                'block'
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  LOAD_CONST               1
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   534  'to 534'

 L. 227       520  LOAD_GLOBAL              i16
              522  LOAD_FAST                'block'
              524  LOAD_CONST               1
              526  CALL_FUNCTION_2       2  ''
              528  LOAD_FAST                'info'
              530  LOAD_STR                 'loop'
              532  STORE_SUBSCR     
            534_0  COME_FROM           544  '544'
            534_1  COME_FROM           516  '516'
            534_2  COME_FROM           502  '502'
            534_3  COME_FROM           480  '480'
            534_4  COME_FROM           444  '444'
            534_5  COME_FROM           432  '432'
            534_6  COME_FROM           362  '362'
            534_7  COME_FROM           352  '352'

 L. 228       534  LOAD_FAST                'self'
              536  LOAD_METHOD              data
              538  CALL_METHOD_0         0  ''
          540_542  POP_JUMP_IF_FALSE   804  'to 804'

 L. 229   544_546  JUMP_BACK           534  'to 534'
              548  JUMP_BACK           216  'to 216'
            550_0  COME_FROM           252  '252'

 L. 231       550  LOAD_FAST                's'
              552  LOAD_CONST               b','
              554  COMPARE_OP               ==
              556  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 235       558  LOAD_FAST                'self'
              560  LOAD_ATTR                fp
              562  LOAD_METHOD              read
              564  LOAD_CONST               9
              566  CALL_METHOD_1         1  ''
              568  STORE_FAST               's'

 L. 238       570  LOAD_GLOBAL              i16
              572  LOAD_FAST                's'
              574  LOAD_CONST               0
              576  CALL_FUNCTION_2       2  ''
              578  LOAD_GLOBAL              i16
              580  LOAD_FAST                's'
              582  LOAD_CONST               2
              584  CALL_FUNCTION_2       2  ''
              586  ROT_TWO          
              588  STORE_FAST               'x0'
              590  STORE_FAST               'y0'

 L. 239       592  LOAD_FAST                'x0'
              594  LOAD_GLOBAL              i16
              596  LOAD_FAST                's'
              598  LOAD_CONST               4
              600  CALL_FUNCTION_2       2  ''
              602  BINARY_ADD       
              604  LOAD_FAST                'y0'
              606  LOAD_GLOBAL              i16
              608  LOAD_FAST                's'
              610  LOAD_CONST               6
              612  CALL_FUNCTION_2       2  ''
              614  BINARY_ADD       
              616  ROT_TWO          
              618  STORE_FAST               'x1'
              620  STORE_FAST               'y1'

 L. 240       622  LOAD_FAST                'x1'
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                size
              628  LOAD_CONST               0
              630  BINARY_SUBSCR    
              632  COMPARE_OP               >
          634_636  POP_JUMP_IF_TRUE    654  'to 654'
              638  LOAD_FAST                'y1'
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                size
              644  LOAD_CONST               1
              646  BINARY_SUBSCR    
              648  COMPARE_OP               >
          650_652  POP_JUMP_IF_FALSE   688  'to 688'
            654_0  COME_FROM           634  '634'

 L. 241       654  LOAD_GLOBAL              max
              656  LOAD_FAST                'x1'
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                size
              662  LOAD_CONST               0
              664  BINARY_SUBSCR    
              666  CALL_FUNCTION_2       2  ''
              668  LOAD_GLOBAL              max
              670  LOAD_FAST                'y1'
              672  LOAD_FAST                'self'
              674  LOAD_ATTR                size
              676  LOAD_CONST               1
              678  BINARY_SUBSCR    
              680  CALL_FUNCTION_2       2  ''
              682  BUILD_TUPLE_2         2 
              684  LOAD_FAST                'self'
              686  STORE_ATTR               _size
            688_0  COME_FROM           650  '650'

 L. 242       688  LOAD_FAST                'x0'
              690  LOAD_FAST                'y0'
              692  LOAD_FAST                'x1'
              694  LOAD_FAST                'y1'
              696  BUILD_TUPLE_4         4 
              698  LOAD_FAST                'self'
              700  STORE_ATTR               dispose_extent

 L. 243       702  LOAD_FAST                's'
              704  LOAD_CONST               8
              706  BINARY_SUBSCR    
              708  STORE_FAST               'flags'

 L. 245       710  LOAD_FAST                'flags'
              712  LOAD_CONST               64
              714  BINARY_AND       
              716  LOAD_CONST               0
              718  COMPARE_OP               !=
              720  STORE_FAST               'interlace'

 L. 247       722  LOAD_FAST                'flags'
              724  LOAD_CONST               128
              726  BINARY_AND       
          728_730  POP_JUMP_IF_FALSE   770  'to 770'

 L. 248       732  LOAD_FAST                'flags'
              734  LOAD_CONST               7
              736  BINARY_AND       
              738  LOAD_CONST               1
              740  BINARY_ADD       
              742  STORE_FAST               'bits'

 L. 249       744  LOAD_GLOBAL              ImagePalette
              746  LOAD_METHOD              raw
              748  LOAD_STR                 'RGB'
              750  LOAD_FAST                'self'
              752  LOAD_ATTR                fp
              754  LOAD_METHOD              read
              756  LOAD_CONST               3
              758  LOAD_FAST                'bits'
              760  BINARY_LSHIFT    
              762  CALL_METHOD_1         1  ''
              764  CALL_METHOD_2         2  ''
              766  LOAD_FAST                'self'
              768  STORE_ATTR               palette
            770_0  COME_FROM           728  '728'

 L. 252       770  LOAD_FAST                'self'
              772  LOAD_ATTR                fp
              774  LOAD_METHOD              read
              776  LOAD_CONST               1
              778  CALL_METHOD_1         1  ''
              780  LOAD_CONST               0
              782  BINARY_SUBSCR    
              784  STORE_FAST               'bits'

 L. 253       786  LOAD_FAST                'self'
              788  LOAD_ATTR                fp
              790  LOAD_METHOD              tell
              792  CALL_METHOD_0         0  ''
              794  LOAD_FAST                'self'
              796  STORE_ATTR               _GifImageFile__offset

 L. 254   798_800  JUMP_FORWARD        806  'to 806'
              802  JUMP_BACK           216  'to 216'
            804_0  COME_FROM           540  '540'

 L. 257       804  JUMP_BACK           216  'to 216'
            806_0  COME_FROM           798  '798'
            806_1  COME_FROM           240  '240'

 L. 260       806  SETUP_FINALLY      1028  'to 1028'

 L. 261       808  LOAD_FAST                'self'
              810  LOAD_ATTR                disposal_method
              812  LOAD_CONST               2
              814  COMPARE_OP               <
          816_818  POP_JUMP_IF_FALSE   828  'to 828'

 L. 263       820  LOAD_CONST               None
              822  LOAD_FAST                'self'
              824  STORE_ATTR               dispose
              826  JUMP_FORWARD       1024  'to 1024'
            828_0  COME_FROM           816  '816'

 L. 264       828  LOAD_FAST                'self'
              830  LOAD_ATTR                disposal_method
              832  LOAD_CONST               2
              834  COMPARE_OP               ==
          836_838  POP_JUMP_IF_FALSE   928  'to 928'

 L. 268       840  LOAD_FAST                'self'
              842  LOAD_ATTR                dispose_extent
              844  UNPACK_SEQUENCE_4     4 
              846  STORE_FAST               'x0'
              848  STORE_FAST               'y0'
              850  STORE_FAST               'x1'
              852  STORE_FAST               'y1'

 L. 269       854  LOAD_FAST                'x1'
              856  LOAD_FAST                'x0'
              858  BINARY_SUBTRACT  
              860  LOAD_FAST                'y1'
              862  LOAD_FAST                'y0'
              864  BINARY_SUBTRACT  
              866  BUILD_TUPLE_2         2 
              868  STORE_FAST               'dispose_size'

 L. 271       870  LOAD_GLOBAL              Image
              872  LOAD_METHOD              _decompression_bomb_check
              874  LOAD_FAST                'dispose_size'
              876  CALL_METHOD_1         1  ''
              878  POP_TOP          

 L. 276       880  LOAD_FAST                'frame_transparency'
              882  LOAD_CONST               None
              884  <117>                 1  ''

 L. 275   886_888  POP_JUMP_IF_FALSE   894  'to 894'
              890  LOAD_FAST                'frame_transparency'
              892  JUMP_FORWARD        906  'to 906'
            894_0  COME_FROM           886  '886'

 L. 277       894  LOAD_FAST                'self'
              896  LOAD_ATTR                info
              898  LOAD_METHOD              get
              900  LOAD_STR                 'background'
              902  LOAD_CONST               0
              904  CALL_METHOD_2         2  ''
            906_0  COME_FROM           892  '892'

 L. 274       906  STORE_FAST               'color'

 L. 279       908  LOAD_GLOBAL              Image
              910  LOAD_ATTR                core
              912  LOAD_METHOD              fill
              914  LOAD_STR                 'P'
              916  LOAD_FAST                'dispose_size'
              918  LOAD_FAST                'color'
              920  CALL_METHOD_3         3  ''
              922  LOAD_FAST                'self'
              924  STORE_ATTR               dispose
              926  JUMP_FORWARD       1024  'to 1024'
            928_0  COME_FROM           836  '836'

 L. 282       928  LOAD_FAST                'self'
              930  LOAD_ATTR                im
          932_934  POP_JUMP_IF_FALSE   956  'to 956'

 L. 284       936  LOAD_FAST                'self'
              938  LOAD_METHOD              _crop
              940  LOAD_FAST                'self'
              942  LOAD_ATTR                im
              944  LOAD_FAST                'self'
              946  LOAD_ATTR                dispose_extent
              948  CALL_METHOD_2         2  ''
              950  LOAD_FAST                'self'
              952  STORE_ATTR               dispose
              954  JUMP_FORWARD       1024  'to 1024'
            956_0  COME_FROM           932  '932'

 L. 285       956  LOAD_FAST                'frame_transparency'
              958  LOAD_CONST               None
              960  <117>                 1  ''
          962_964  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 286       966  LOAD_FAST                'self'
              968  LOAD_ATTR                dispose_extent
              970  UNPACK_SEQUENCE_4     4 
              972  STORE_FAST               'x0'
              974  STORE_FAST               'y0'
              976  STORE_FAST               'x1'
              978  STORE_FAST               'y1'

 L. 287       980  LOAD_FAST                'x1'
              982  LOAD_FAST                'x0'
              984  BINARY_SUBTRACT  
              986  LOAD_FAST                'y1'
              988  LOAD_FAST                'y0'
              990  BINARY_SUBTRACT  
              992  BUILD_TUPLE_2         2 
              994  STORE_FAST               'dispose_size'

 L. 289       996  LOAD_GLOBAL              Image
              998  LOAD_METHOD              _decompression_bomb_check
             1000  LOAD_FAST                'dispose_size'
             1002  CALL_METHOD_1         1  ''
             1004  POP_TOP          

 L. 290      1006  LOAD_GLOBAL              Image
             1008  LOAD_ATTR                core
             1010  LOAD_METHOD              fill

 L. 291      1012  LOAD_STR                 'P'
             1014  LOAD_FAST                'dispose_size'
             1016  LOAD_FAST                'frame_transparency'

 L. 290      1018  CALL_METHOD_3         3  ''
             1020  LOAD_FAST                'self'
             1022  STORE_ATTR               dispose
           1024_0  COME_FROM           962  '962'
           1024_1  COME_FROM           954  '954'
           1024_2  COME_FROM           926  '926'
           1024_3  COME_FROM           826  '826'
             1024  POP_BLOCK        
             1026  JUMP_FORWARD       1048  'to 1048'
           1028_0  COME_FROM_FINALLY   806  '806'

 L. 293      1028  DUP_TOP          
             1030  LOAD_GLOBAL              AttributeError
         1032_1034  <121>              1046  ''
             1036  POP_TOP          
             1038  POP_TOP          
             1040  POP_TOP          

 L. 294      1042  POP_EXCEPT       
             1044  BREAK_LOOP         1048  'to 1048'
             1046  <48>             
           1048_0  COME_FROM          1044  '1044'
           1048_1  COME_FROM          1026  '1026'

 L. 296      1048  LOAD_FAST                'interlace'
             1050  LOAD_CONST               None
             1052  <117>                 1  ''
         1054_1056  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 297      1058  LOAD_CONST               -1
             1060  STORE_FAST               'transparency'

 L. 298      1062  LOAD_FAST                'frame_transparency'
             1064  LOAD_CONST               None
             1066  <117>                 1  ''
         1068_1070  POP_JUMP_IF_FALSE  1098  'to 1098'

 L. 299      1072  LOAD_FAST                'frame'
             1074  LOAD_CONST               0
             1076  COMPARE_OP               ==
         1078_1080  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 300      1082  LOAD_FAST                'frame_transparency'
             1084  LOAD_FAST                'self'
             1086  LOAD_ATTR                info
             1088  LOAD_STR                 'transparency'
             1090  STORE_SUBSCR     
             1092  JUMP_FORWARD       1098  'to 1098'
           1094_0  COME_FROM          1078  '1078'

 L. 302      1094  LOAD_FAST                'frame_transparency'
             1096  STORE_FAST               'transparency'
           1098_0  COME_FROM          1092  '1092'
           1098_1  COME_FROM          1068  '1068'

 L. 305      1098  LOAD_STR                 'gif'

 L. 306      1100  LOAD_FAST                'x0'
             1102  LOAD_FAST                'y0'
             1104  LOAD_FAST                'x1'
             1106  LOAD_FAST                'y1'
             1108  BUILD_TUPLE_4         4 

 L. 307      1110  LOAD_FAST                'self'
             1112  LOAD_ATTR                _GifImageFile__offset

 L. 308      1114  LOAD_FAST                'bits'
             1116  LOAD_FAST                'interlace'
             1118  LOAD_FAST                'transparency'
             1120  BUILD_TUPLE_3         3 

 L. 304      1122  BUILD_TUPLE_4         4 

 L. 303      1124  BUILD_LIST_1          1 
             1126  LOAD_FAST                'self'
             1128  STORE_ATTR               tile
             1130  JUMP_FORWARD       1136  'to 1136'
           1132_0  COME_FROM          1054  '1054'

 L. 313      1132  LOAD_GLOBAL              EOFError
             1134  RAISE_VARARGS_1       1  'exception instance'
           1136_0  COME_FROM          1130  '1130'

 L. 315      1136  LOAD_CONST               ('duration', 'comment', 'extension', 'loop')
             1138  GET_ITER         
           1140_0  COME_FROM          1190  '1190'
           1140_1  COME_FROM          1178  '1178'
           1140_2  COME_FROM          1168  '1168'
             1140  FOR_ITER           1194  'to 1194'
             1142  STORE_FAST               'k'

 L. 316      1144  LOAD_FAST                'k'
             1146  LOAD_FAST                'info'
             1148  <118>                 0  ''
         1150_1152  POP_JUMP_IF_FALSE  1170  'to 1170'

 L. 317      1154  LOAD_FAST                'info'
             1156  LOAD_FAST                'k'
             1158  BINARY_SUBSCR    
             1160  LOAD_FAST                'self'
             1162  LOAD_ATTR                info
             1164  LOAD_FAST                'k'
             1166  STORE_SUBSCR     
             1168  JUMP_BACK          1140  'to 1140'
           1170_0  COME_FROM          1150  '1150'

 L. 318      1170  LOAD_FAST                'k'
             1172  LOAD_FAST                'self'
             1174  LOAD_ATTR                info
             1176  <118>                 0  ''
         1178_1180  POP_JUMP_IF_FALSE_BACK  1140  'to 1140'

 L. 319      1182  LOAD_FAST                'self'
             1184  LOAD_ATTR                info
             1186  LOAD_FAST                'k'
             1188  DELETE_SUBSCR    
         1190_1192  JUMP_BACK          1140  'to 1140'
           1194_0  COME_FROM          1140  '1140'

 L. 321      1194  LOAD_STR                 'L'
             1196  LOAD_FAST                'self'
             1198  STORE_ATTR               mode

 L. 322      1200  LOAD_FAST                'self'
             1202  LOAD_ATTR                palette
         1204_1206  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 323      1208  LOAD_STR                 'P'
             1210  LOAD_FAST                'self'
             1212  STORE_ATTR               mode
           1214_0  COME_FROM          1204  '1204'

Parse error at or near `CALL_FINALLY' instruction at offset 24

    def load_prepare--- This code section failed: ---

 L. 326         0  LOAD_FAST                'self'
                2  LOAD_ATTR                im
                4  POP_JUMP_IF_TRUE     44  'to 44'
                6  LOAD_STR                 'transparency'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                info
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    44  'to 44'

 L. 327        16  LOAD_GLOBAL              Image
               18  LOAD_ATTR                core
               20  LOAD_METHOD              fill
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                mode
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                size
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                info
               34  LOAD_STR                 'transparency'
               36  BINARY_SUBSCR    
               38  CALL_METHOD_3         3  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               im
             44_0  COME_FROM            14  '14'
             44_1  COME_FROM             4  '4'

 L. 329        44  LOAD_GLOBAL              super
               46  LOAD_GLOBAL              GifImageFile
               48  LOAD_FAST                'self'
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_METHOD              load_prepare
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def tell(self):
        return self._GifImageFile__frame

    def _close__fp--- This code section failed: ---

 L. 335         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 336         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _GifImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 337        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _GifImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 338        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 339        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 341        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _GifImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _GifImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


RAWMODE = {'1':'L', 
 'L':'L',  'P':'P'}

def _normalize_mode--- This code section failed: ---

 L. 367         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  LOAD_GLOBAL              RAWMODE
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 368        10  LOAD_FAST                'im'
               12  LOAD_METHOD              load
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 369        18  LOAD_FAST                'im'
               20  RETURN_VALUE     
             22_0  COME_FROM             8  '8'

 L. 370        22  LOAD_GLOBAL              Image
               24  LOAD_METHOD              getmodebase
               26  LOAD_FAST                'im'
               28  LOAD_ATTR                mode
               30  CALL_METHOD_1         1  ''
               32  LOAD_STR                 'RGB'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   102  'to 102'

 L. 371        38  LOAD_FAST                'initial_call'
               40  POP_JUMP_IF_FALSE    92  'to 92'

 L. 372        42  LOAD_CONST               256
               44  STORE_FAST               'palette_size'

 L. 373        46  LOAD_FAST                'im'
               48  LOAD_ATTR                palette
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 374        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'im'
               56  LOAD_ATTR                palette
               58  LOAD_METHOD              getdata
               60  CALL_METHOD_0         0  ''
               62  LOAD_CONST               1
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               3
               70  BINARY_FLOOR_DIVIDE
               72  STORE_FAST               'palette_size'
             74_0  COME_FROM            50  '50'

 L. 375        74  LOAD_FAST                'im'
               76  LOAD_ATTR                convert
               78  LOAD_STR                 'P'
               80  LOAD_GLOBAL              Image
               82  LOAD_ATTR                ADAPTIVE
               84  LOAD_FAST                'palette_size'
               86  LOAD_CONST               ('palette', 'colors')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  RETURN_VALUE     
             92_0  COME_FROM            40  '40'

 L. 377        92  LOAD_FAST                'im'
               94  LOAD_METHOD              convert
               96  LOAD_STR                 'P'
               98  CALL_METHOD_1         1  ''
              100  RETURN_VALUE     
            102_0  COME_FROM            36  '36'

 L. 378       102  LOAD_FAST                'im'
              104  LOAD_METHOD              convert
              106  LOAD_STR                 'L'
              108  CALL_METHOD_1         1  ''
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _normalize_palette--- This code section failed: ---

 L. 393         0  LOAD_CONST               None
                2  STORE_FAST               'source_palette'

 L. 394         4  LOAD_FAST                'palette'
                6  POP_JUMP_IF_FALSE   106  'to 106'

 L. 396         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'palette'
               12  LOAD_GLOBAL              bytes
               14  LOAD_GLOBAL              bytearray
               16  LOAD_GLOBAL              list
               18  BUILD_TUPLE_3         3 
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    40  'to 40'

 L. 397        24  LOAD_GLOBAL              bytearray
               26  LOAD_FAST                'palette'
               28  LOAD_CONST               None
               30  LOAD_CONST               768
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'source_palette'
             40_0  COME_FROM            22  '22'

 L. 398        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'palette'
               44  LOAD_GLOBAL              ImagePalette
               46  LOAD_ATTR                ImagePalette
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE   106  'to 106'

 L. 399        52  LOAD_GLOBAL              bytearray

 L. 400        54  LOAD_GLOBAL              itertools
               56  LOAD_ATTR                chain
               58  LOAD_METHOD              from_iterable

 L. 401        60  LOAD_GLOBAL              zip

 L. 402        62  LOAD_FAST                'palette'
               64  LOAD_ATTR                palette
               66  LOAD_CONST               None
               68  LOAD_CONST               256
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    

 L. 403        74  LOAD_FAST                'palette'
               76  LOAD_ATTR                palette
               78  LOAD_CONST               256
               80  LOAD_CONST               512
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    

 L. 404        86  LOAD_FAST                'palette'
               88  LOAD_ATTR                palette
               90  LOAD_CONST               512
               92  LOAD_CONST               768
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    

 L. 401        98  CALL_FUNCTION_3       3  ''

 L. 400       100  CALL_METHOD_1         1  ''

 L. 399       102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'source_palette'
            106_0  COME_FROM            50  '50'
            106_1  COME_FROM             6  '6'

 L. 409       106  LOAD_FAST                'im'
              108  LOAD_ATTR                mode
              110  LOAD_STR                 'P'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   142  'to 142'

 L. 410       116  LOAD_FAST                'source_palette'
              118  POP_JUMP_IF_TRUE    184  'to 184'

 L. 411       120  LOAD_FAST                'im'
              122  LOAD_ATTR                im
              124  LOAD_METHOD              getpalette
              126  LOAD_STR                 'RGB'
              128  CALL_METHOD_1         1  ''
              130  LOAD_CONST               None
              132  LOAD_CONST               768
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  STORE_FAST               'source_palette'
              140  JUMP_FORWARD        184  'to 184'
            142_0  COME_FROM           114  '114'

 L. 413       142  LOAD_FAST                'source_palette'
              144  POP_JUMP_IF_TRUE    168  'to 168'

 L. 414       146  LOAD_GLOBAL              bytearray
              148  LOAD_GENEXPR             '<code_object <genexpr>>'
              150  LOAD_STR                 '_normalize_palette.<locals>.<genexpr>'
              152  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              154  LOAD_GLOBAL              range
              156  LOAD_CONST               768
              158  CALL_FUNCTION_1       1  ''
              160  GET_ITER         
              162  CALL_FUNCTION_1       1  ''
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'source_palette'
            168_0  COME_FROM           144  '144'

 L. 415       168  LOAD_GLOBAL              ImagePalette
              170  LOAD_ATTR                ImagePalette
              172  LOAD_STR                 'RGB'
              174  LOAD_FAST                'source_palette'
              176  LOAD_CONST               ('palette',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  LOAD_FAST                'im'
              182  STORE_ATTR               palette
            184_0  COME_FROM           140  '140'
            184_1  COME_FROM           118  '118'

 L. 417       184  LOAD_GLOBAL              _get_optimize
              186  LOAD_FAST                'im'
              188  LOAD_FAST                'info'
              190  CALL_FUNCTION_2       2  ''
              192  STORE_FAST               'used_palette_colors'

 L. 418       194  LOAD_FAST                'used_palette_colors'
              196  LOAD_CONST               None
              198  <117>                 1  ''
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 419       202  LOAD_FAST                'im'
              204  LOAD_METHOD              remap_palette
              206  LOAD_FAST                'used_palette_colors'
              208  LOAD_FAST                'source_palette'
              210  CALL_METHOD_2         2  ''
              212  RETURN_VALUE     
            214_0  COME_FROM           200  '200'

 L. 421       214  LOAD_FAST                'source_palette'
              216  LOAD_FAST                'im'
              218  LOAD_ATTR                palette
              220  STORE_ATTR               palette

 L. 422       222  LOAD_FAST                'im'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 198


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


def _write_multiple_frames--- This code section failed: ---

 L. 448         0  LOAD_FAST                'im'
                2  LOAD_ATTR                encoderinfo
                4  LOAD_METHOD              get
                6  LOAD_STR                 'duration'
                8  LOAD_FAST                'im'
               10  LOAD_ATTR                info
               12  LOAD_METHOD              get
               14  LOAD_STR                 'duration'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'duration'

 L. 449        22  LOAD_FAST                'im'
               24  LOAD_ATTR                encoderinfo
               26  LOAD_METHOD              get
               28  LOAD_STR                 'disposal'
               30  LOAD_FAST                'im'
               32  LOAD_ATTR                info
               34  LOAD_METHOD              get
               36  LOAD_STR                 'disposal'
               38  CALL_METHOD_1         1  ''
               40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'disposal'

 L. 451        44  BUILD_LIST_0          0 
               46  STORE_FAST               'im_frames'

 L. 452        48  LOAD_CONST               0
               50  STORE_FAST               'frame_count'

 L. 453        52  LOAD_CONST               None
               54  STORE_FAST               'background_im'

 L. 454        56  LOAD_GLOBAL              itertools
               58  LOAD_METHOD              chain
               60  LOAD_FAST                'im'
               62  BUILD_LIST_1          1 
               64  LOAD_FAST                'im'
               66  LOAD_ATTR                encoderinfo
               68  LOAD_METHOD              get
               70  LOAD_STR                 'append_images'
               72  BUILD_LIST_0          0 
               74  CALL_METHOD_2         2  ''
               76  CALL_METHOD_2         2  ''
               78  GET_ITER         
             80_0  COME_FROM           490  '490'
            80_82  FOR_ITER            492  'to 492'
               84  STORE_FAST               'imSequence'

 L. 455        86  LOAD_GLOBAL              ImageSequence
               88  LOAD_METHOD              Iterator
               90  LOAD_FAST                'imSequence'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
             96_0  COME_FROM           488  '488'
             96_1  COME_FROM           462  '462'
             96_2  COME_FROM           436  '436'
            96_98  FOR_ITER            490  'to 490'
              100  STORE_FAST               'im_frame'

 L. 457       102  LOAD_GLOBAL              _normalize_mode
              104  LOAD_FAST                'im_frame'
              106  LOAD_METHOD              copy
              108  CALL_METHOD_0         0  ''
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'im_frame'

 L. 458       114  LOAD_FAST                'frame_count'
              116  LOAD_CONST               0
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   156  'to 156'

 L. 459       122  LOAD_FAST                'im_frame'
              124  LOAD_ATTR                info
              126  LOAD_METHOD              items
              128  CALL_METHOD_0         0  ''
              130  GET_ITER         
            132_0  COME_FROM           154  '154'
              132  FOR_ITER            156  'to 156'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'k'
              138  STORE_FAST               'v'

 L. 460       140  LOAD_FAST                'im'
              142  LOAD_ATTR                encoderinfo
              144  LOAD_METHOD              setdefault
              146  LOAD_FAST                'k'
              148  LOAD_FAST                'v'
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          
              154  JUMP_BACK           132  'to 132'
            156_0  COME_FROM           132  '132'
            156_1  COME_FROM           120  '120'

 L. 461       156  LOAD_GLOBAL              _normalize_palette
              158  LOAD_FAST                'im_frame'
              160  LOAD_FAST                'palette'
              162  LOAD_FAST                'im'
              164  LOAD_ATTR                encoderinfo
              166  CALL_FUNCTION_3       3  ''
              168  STORE_FAST               'im_frame'

 L. 463       170  LOAD_FAST                'im'
              172  LOAD_ATTR                encoderinfo
              174  LOAD_METHOD              copy
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'encoderinfo'

 L. 464       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'duration'
              184  LOAD_GLOBAL              list
              186  LOAD_GLOBAL              tuple
              188  BUILD_TUPLE_2         2 
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_FALSE   206  'to 206'

 L. 465       194  LOAD_FAST                'duration'
              196  LOAD_FAST                'frame_count'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'encoderinfo'
              202  LOAD_STR                 'duration'
              204  STORE_SUBSCR     
            206_0  COME_FROM           192  '192'

 L. 466       206  LOAD_GLOBAL              isinstance
              208  LOAD_FAST                'disposal'
              210  LOAD_GLOBAL              list
              212  LOAD_GLOBAL              tuple
              214  BUILD_TUPLE_2         2 
              216  CALL_FUNCTION_2       2  ''
              218  POP_JUMP_IF_FALSE   232  'to 232'

 L. 467       220  LOAD_FAST                'disposal'
              222  LOAD_FAST                'frame_count'
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'encoderinfo'
              228  LOAD_STR                 'disposal'
              230  STORE_SUBSCR     
            232_0  COME_FROM           218  '218'

 L. 468       232  LOAD_FAST                'frame_count'
              234  LOAD_CONST               1
              236  INPLACE_ADD      
              238  STORE_FAST               'frame_count'

 L. 470       240  LOAD_FAST                'im_frames'
          242_244  POP_JUMP_IF_FALSE   466  'to 466'

 L. 472       246  LOAD_FAST                'im_frames'
              248  LOAD_CONST               -1
              250  BINARY_SUBSCR    
              252  STORE_FAST               'previous'

 L. 473       254  LOAD_FAST                'encoderinfo'
              256  LOAD_METHOD              get
              258  LOAD_STR                 'disposal'
              260  CALL_METHOD_1         1  ''
              262  LOAD_CONST               2
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   356  'to 356'

 L. 474       270  LOAD_FAST                'background_im'
              272  LOAD_CONST               None
              274  <117>                 0  ''
          276_278  POP_JUMP_IF_FALSE   350  'to 350'

 L. 475       280  LOAD_FAST                'im'
              282  LOAD_ATTR                encoderinfo
              284  LOAD_METHOD              get

 L. 476       286  LOAD_STR                 'transparency'
              288  LOAD_FAST                'im'
              290  LOAD_ATTR                info
              292  LOAD_METHOD              get
              294  LOAD_STR                 'transparency'
              296  LOAD_CONST               (0, 0, 0)
              298  CALL_METHOD_2         2  ''

 L. 475       300  CALL_METHOD_2         2  ''
              302  STORE_FAST               'color'

 L. 478       304  LOAD_GLOBAL              _get_background
              306  LOAD_FAST                'im_frame'
              308  LOAD_FAST                'color'
              310  CALL_FUNCTION_2       2  ''
              312  STORE_FAST               'background'

 L. 479       314  LOAD_GLOBAL              Image
              316  LOAD_METHOD              new
              318  LOAD_STR                 'P'
              320  LOAD_FAST                'im_frame'
              322  LOAD_ATTR                size
              324  LOAD_FAST                'background'
              326  CALL_METHOD_3         3  ''
              328  STORE_FAST               'background_im'

 L. 480       330  LOAD_FAST                'background_im'
              332  LOAD_METHOD              putpalette
              334  LOAD_FAST                'im_frames'
              336  LOAD_CONST               0
              338  BINARY_SUBSCR    
              340  LOAD_STR                 'im'
              342  BINARY_SUBSCR    
              344  LOAD_ATTR                palette
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
            350_0  COME_FROM           276  '276'

 L. 481       350  LOAD_FAST                'background_im'
              352  STORE_FAST               'base_im'
              354  JUMP_FORWARD        364  'to 364'
            356_0  COME_FROM           266  '266'

 L. 483       356  LOAD_FAST                'previous'
              358  LOAD_STR                 'im'
              360  BINARY_SUBSCR    
              362  STORE_FAST               'base_im'
            364_0  COME_FROM           354  '354'

 L. 484       364  LOAD_GLOBAL              _get_palette_bytes
              366  LOAD_FAST                'im_frame'
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_GLOBAL              _get_palette_bytes
              372  LOAD_FAST                'base_im'
              374  CALL_FUNCTION_1       1  ''
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   396  'to 396'

 L. 485       382  LOAD_GLOBAL              ImageChops
              384  LOAD_METHOD              subtract_modulo
              386  LOAD_FAST                'im_frame'
              388  LOAD_FAST                'base_im'
              390  CALL_METHOD_2         2  ''
              392  STORE_FAST               'delta'
              394  JUMP_FORWARD        420  'to 420'
            396_0  COME_FROM           378  '378'

 L. 487       396  LOAD_GLOBAL              ImageChops
              398  LOAD_METHOD              subtract_modulo

 L. 488       400  LOAD_FAST                'im_frame'
              402  LOAD_METHOD              convert
              404  LOAD_STR                 'RGB'
              406  CALL_METHOD_1         1  ''
              408  LOAD_FAST                'base_im'
              410  LOAD_METHOD              convert
              412  LOAD_STR                 'RGB'
              414  CALL_METHOD_1         1  ''

 L. 487       416  CALL_METHOD_2         2  ''
              418  STORE_FAST               'delta'
            420_0  COME_FROM           394  '394'

 L. 490       420  LOAD_FAST                'delta'
              422  LOAD_METHOD              getbbox
              424  CALL_METHOD_0         0  ''
              426  STORE_FAST               'bbox'

 L. 491       428  LOAD_FAST                'bbox'
          430_432  POP_JUMP_IF_TRUE    470  'to 470'

 L. 493       434  LOAD_FAST                'duration'
              436  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 494       438  LOAD_FAST                'previous'
              440  LOAD_STR                 'encoderinfo'
              442  BINARY_SUBSCR    
              444  LOAD_STR                 'duration'
              446  DUP_TOP_TWO      
              448  BINARY_SUBSCR    
              450  LOAD_FAST                'encoderinfo'
              452  LOAD_STR                 'duration'
              454  BINARY_SUBSCR    
              456  INPLACE_ADD      
              458  ROT_THREE        
              460  STORE_SUBSCR     

 L. 495       462  JUMP_BACK            96  'to 96'
              464  JUMP_FORWARD        470  'to 470'
            466_0  COME_FROM           242  '242'

 L. 497       466  LOAD_CONST               None
              468  STORE_FAST               'bbox'
            470_0  COME_FROM           464  '464'
            470_1  COME_FROM           430  '430'

 L. 498       470  LOAD_FAST                'im_frames'
              472  LOAD_METHOD              append
              474  LOAD_FAST                'im_frame'
              476  LOAD_FAST                'bbox'
              478  LOAD_FAST                'encoderinfo'
              480  LOAD_CONST               ('im', 'bbox', 'encoderinfo')
              482  BUILD_CONST_KEY_MAP_3     3 
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          
              488  JUMP_BACK            96  'to 96'
            490_0  COME_FROM            96  '96'
              490  JUMP_BACK            80  'to 80'
            492_0  COME_FROM            80  '80'

 L. 500       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'im_frames'
              496  CALL_FUNCTION_1       1  ''
              498  LOAD_CONST               1
              500  COMPARE_OP               >
          502_504  POP_JUMP_IF_FALSE   638  'to 638'

 L. 501       506  LOAD_FAST                'im_frames'
              508  GET_ITER         
            510_0  COME_FROM           630  '630'
              510  FOR_ITER            634  'to 634'
              512  STORE_FAST               'frame_data'

 L. 502       514  LOAD_FAST                'frame_data'
              516  LOAD_STR                 'im'
              518  BINARY_SUBSCR    
              520  STORE_FAST               'im_frame'

 L. 503       522  LOAD_FAST                'frame_data'
              524  LOAD_STR                 'bbox'
              526  BINARY_SUBSCR    
          528_530  POP_JUMP_IF_TRUE    570  'to 570'

 L. 505       532  LOAD_GLOBAL              _get_global_header
              534  LOAD_FAST                'im_frame'
              536  LOAD_FAST                'frame_data'
              538  LOAD_STR                 'encoderinfo'
              540  BINARY_SUBSCR    
              542  CALL_FUNCTION_2       2  ''
              544  GET_ITER         
            546_0  COME_FROM           560  '560'
              546  FOR_ITER            564  'to 564'
              548  STORE_FAST               's'

 L. 506       550  LOAD_FAST                'fp'
              552  LOAD_METHOD              write
              554  LOAD_FAST                's'
              556  CALL_METHOD_1         1  ''
              558  POP_TOP          
          560_562  JUMP_BACK           546  'to 546'
            564_0  COME_FROM           546  '546'

 L. 507       564  LOAD_CONST               (0, 0)
              566  STORE_FAST               'offset'
              568  JUMP_FORWARD        612  'to 612'
            570_0  COME_FROM           528  '528'

 L. 510       570  LOAD_CONST               True
              572  LOAD_FAST                'frame_data'
              574  LOAD_STR                 'encoderinfo'
              576  BINARY_SUBSCR    
              578  LOAD_STR                 'include_color_table'
              580  STORE_SUBSCR     

 L. 512       582  LOAD_FAST                'im_frame'
              584  LOAD_METHOD              crop
              586  LOAD_FAST                'frame_data'
              588  LOAD_STR                 'bbox'
              590  BINARY_SUBSCR    
              592  CALL_METHOD_1         1  ''
              594  STORE_FAST               'im_frame'

 L. 513       596  LOAD_FAST                'frame_data'
              598  LOAD_STR                 'bbox'
              600  BINARY_SUBSCR    
              602  LOAD_CONST               None
              604  LOAD_CONST               2
              606  BUILD_SLICE_2         2 
              608  BINARY_SUBSCR    
              610  STORE_FAST               'offset'
            612_0  COME_FROM           568  '568'

 L. 514       612  LOAD_GLOBAL              _write_frame_data
              614  LOAD_FAST                'fp'
              616  LOAD_FAST                'im_frame'
              618  LOAD_FAST                'offset'
              620  LOAD_FAST                'frame_data'
              622  LOAD_STR                 'encoderinfo'
              624  BINARY_SUBSCR    
              626  CALL_FUNCTION_4       4  ''
              628  POP_TOP          
          630_632  JUMP_BACK           510  'to 510'
            634_0  COME_FROM           510  '510'

 L. 515       634  LOAD_CONST               True
              636  RETURN_VALUE     
            638_0  COME_FROM           502  '502'

 L. 516       638  LOAD_STR                 'duration'
              640  LOAD_FAST                'im'
              642  LOAD_ATTR                encoderinfo
              644  <118>                 0  ''
          646_648  POP_JUMP_IF_FALSE   692  'to 692'
              650  LOAD_GLOBAL              isinstance

 L. 517       652  LOAD_FAST                'im'
              654  LOAD_ATTR                encoderinfo
              656  LOAD_STR                 'duration'
              658  BINARY_SUBSCR    
              660  LOAD_GLOBAL              list
              662  LOAD_GLOBAL              tuple
              664  BUILD_TUPLE_2         2 

 L. 516       666  CALL_FUNCTION_2       2  ''
          668_670  POP_JUMP_IF_FALSE   692  'to 692'

 L. 520       672  LOAD_GLOBAL              sum
              674  LOAD_FAST                'im'
              676  LOAD_ATTR                encoderinfo
              678  LOAD_STR                 'duration'
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_1       1  ''
              684  LOAD_FAST                'im'
              686  LOAD_ATTR                encoderinfo
              688  LOAD_STR                 'duration'
              690  STORE_SUBSCR     
            692_0  COME_FROM           668  '668'
            692_1  COME_FROM           646  '646'

Parse error at or near `<117>' instruction at offset 274


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save--- This code section failed: ---

 L. 529         0  LOAD_STR                 'palette'
                2  LOAD_FAST                'im'
                4  LOAD_ATTR                encoderinfo
                6  <118>                 0  ''
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_STR                 'palette'
               12  LOAD_FAST                'im'
               14  LOAD_ATTR                info
               16  <118>                 0  ''
               18  POP_JUMP_IF_FALSE    44  'to 44'
             20_0  COME_FROM             8  '8'

 L. 530        20  LOAD_FAST                'im'
               22  LOAD_ATTR                encoderinfo
               24  LOAD_METHOD              get
               26  LOAD_STR                 'palette'
               28  LOAD_FAST                'im'
               30  LOAD_ATTR                info
               32  LOAD_METHOD              get
               34  LOAD_STR                 'palette'
               36  CALL_METHOD_1         1  ''
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'palette'
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM            18  '18'

 L. 532        44  LOAD_CONST               None
               46  STORE_FAST               'palette'

 L. 533        48  LOAD_FAST                'im'
               50  LOAD_ATTR                encoderinfo
               52  LOAD_METHOD              get
               54  LOAD_STR                 'optimize'
               56  LOAD_CONST               True
               58  CALL_METHOD_2         2  ''
               60  LOAD_FAST                'im'
               62  LOAD_ATTR                encoderinfo
               64  LOAD_STR                 'optimize'
               66  STORE_SUBSCR     
             68_0  COME_FROM            42  '42'

 L. 535        68  LOAD_FAST                'save_all'
               70  POP_JUMP_IF_FALSE    84  'to 84'
               72  LOAD_GLOBAL              _write_multiple_frames
               74  LOAD_FAST                'im'
               76  LOAD_FAST                'fp'
               78  LOAD_FAST                'palette'
               80  CALL_FUNCTION_3       3  ''
               82  POP_JUMP_IF_TRUE     96  'to 96'
             84_0  COME_FROM            70  '70'

 L. 536        84  LOAD_GLOBAL              _write_single_frame
               86  LOAD_FAST                'im'
               88  LOAD_FAST                'fp'
               90  LOAD_FAST                'palette'
               92  CALL_FUNCTION_3       3  ''
               94  POP_TOP          
             96_0  COME_FROM            82  '82'

 L. 538        96  LOAD_FAST                'fp'
               98  LOAD_METHOD              write
              100  LOAD_CONST               b';'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 540       106  LOAD_GLOBAL              hasattr
              108  LOAD_FAST                'fp'
              110  LOAD_STR                 'flush'
              112  CALL_FUNCTION_2       2  ''
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L. 541       116  LOAD_FAST                'fp'
              118  LOAD_METHOD              flush
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          
            124_0  COME_FROM           114  '114'

Parse error at or near `None' instruction at offset -1


def get_interlace(im):
    interlace = im.encoderinfo.get('interlace', 1)
    if min(im.size) < 16:
        interlace = 0
    return interlace


def _write_local_header--- This code section failed: ---

 L. 555         0  LOAD_CONST               False
                2  STORE_FAST               'transparent_color_exists'

 L. 556         4  SETUP_FINALLY        20  'to 20'

 L. 557         6  LOAD_FAST                'im'
                8  LOAD_ATTR                encoderinfo
               10  LOAD_STR                 'transparency'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'transparency'
               16  POP_BLOCK        
               18  JUMP_FORWARD         38  'to 38'
             20_0  COME_FROM_FINALLY     4  '4'

 L. 558        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                36  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 559        32  POP_EXCEPT       
               34  JUMP_FORWARD        108  'to 108'
               36  <48>             
             38_0  COME_FROM            18  '18'

 L. 561        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'transparency'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'transparency'

 L. 563        46  LOAD_CONST               True
               48  STORE_FAST               'transparent_color_exists'

 L. 565        50  LOAD_GLOBAL              _get_optimize
               52  LOAD_FAST                'im'
               54  LOAD_FAST                'im'
               56  LOAD_ATTR                encoderinfo
               58  CALL_FUNCTION_2       2  ''
               60  STORE_FAST               'used_palette_colors'

 L. 566        62  LOAD_FAST                'used_palette_colors'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE   108  'to 108'

 L. 568        70  SETUP_FINALLY        86  'to 86'

 L. 569        72  LOAD_FAST                'used_palette_colors'
               74  LOAD_METHOD              index
               76  LOAD_FAST                'transparency'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'transparency'
               82  POP_BLOCK        
               84  JUMP_FORWARD        108  'to 108'
             86_0  COME_FROM_FINALLY    70  '70'

 L. 570        86  DUP_TOP          
               88  LOAD_GLOBAL              ValueError
               90  <121>               106  ''
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 571        98  LOAD_CONST               False
              100  STORE_FAST               'transparent_color_exists'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            84  '84'
            108_2  COME_FROM            68  '68'
            108_3  COME_FROM            34  '34'

 L. 573       108  LOAD_STR                 'duration'
              110  LOAD_FAST                'im'
              112  LOAD_ATTR                encoderinfo
              114  <118>                 0  ''
              116  POP_JUMP_IF_FALSE   138  'to 138'

 L. 574       118  LOAD_GLOBAL              int
              120  LOAD_FAST                'im'
              122  LOAD_ATTR                encoderinfo
              124  LOAD_STR                 'duration'
              126  BINARY_SUBSCR    
              128  LOAD_CONST               10
              130  BINARY_TRUE_DIVIDE
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'duration'
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM           116  '116'

 L. 576       138  LOAD_CONST               0
              140  STORE_FAST               'duration'
            142_0  COME_FROM           136  '136'

 L. 578       142  LOAD_GLOBAL              int
              144  LOAD_FAST                'im'
              146  LOAD_ATTR                encoderinfo
              148  LOAD_METHOD              get
              150  LOAD_STR                 'disposal'
              152  LOAD_CONST               0
              154  CALL_METHOD_2         2  ''
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'disposal'

 L. 580       160  LOAD_FAST                'transparent_color_exists'
              162  POP_JUMP_IF_TRUE    178  'to 178'
              164  LOAD_FAST                'duration'
              166  LOAD_CONST               0
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_TRUE    178  'to 178'
              172  LOAD_FAST                'disposal'
          174_176  POP_JUMP_IF_FALSE   268  'to 268'
            178_0  COME_FROM           170  '170'
            178_1  COME_FROM           162  '162'

 L. 581       178  LOAD_FAST                'transparent_color_exists'
              180  POP_JUMP_IF_FALSE   186  'to 186'
              182  LOAD_CONST               1
              184  JUMP_FORWARD        188  'to 188'
            186_0  COME_FROM           180  '180'
              186  LOAD_CONST               0
            188_0  COME_FROM           184  '184'
              188  STORE_FAST               'packed_flag'

 L. 582       190  LOAD_FAST                'packed_flag'
              192  LOAD_FAST                'disposal'
              194  LOAD_CONST               2
              196  BINARY_LSHIFT    
              198  INPLACE_OR       
              200  STORE_FAST               'packed_flag'

 L. 583       202  LOAD_FAST                'transparent_color_exists'
              204  POP_JUMP_IF_TRUE    210  'to 210'

 L. 584       206  LOAD_CONST               0
              208  STORE_FAST               'transparency'
            210_0  COME_FROM           204  '204'

 L. 586       210  LOAD_FAST                'fp'
              212  LOAD_METHOD              write

 L. 587       214  LOAD_CONST               b'!'

 L. 588       216  LOAD_GLOBAL              o8
              218  LOAD_CONST               249
              220  CALL_FUNCTION_1       1  ''

 L. 587       222  BINARY_ADD       

 L. 589       224  LOAD_GLOBAL              o8
              226  LOAD_CONST               4
              228  CALL_FUNCTION_1       1  ''

 L. 587       230  BINARY_ADD       

 L. 590       232  LOAD_GLOBAL              o8
              234  LOAD_FAST                'packed_flag'
              236  CALL_FUNCTION_1       1  ''

 L. 587       238  BINARY_ADD       

 L. 591       240  LOAD_GLOBAL              o16
              242  LOAD_FAST                'duration'
              244  CALL_FUNCTION_1       1  ''

 L. 587       246  BINARY_ADD       

 L. 592       248  LOAD_GLOBAL              o8
              250  LOAD_FAST                'transparency'
              252  CALL_FUNCTION_1       1  ''

 L. 587       254  BINARY_ADD       

 L. 593       256  LOAD_GLOBAL              o8
              258  LOAD_CONST               0
              260  CALL_FUNCTION_1       1  ''

 L. 587       262  BINARY_ADD       

 L. 586       264  CALL_METHOD_1         1  ''
              266  POP_TOP          
            268_0  COME_FROM           174  '174'

 L. 596       268  LOAD_STR                 'comment'
              270  LOAD_FAST                'im'
              272  LOAD_ATTR                encoderinfo
              274  <118>                 0  ''
          276_278  POP_JUMP_IF_FALSE   424  'to 424'
              280  LOAD_CONST               1
              282  LOAD_GLOBAL              len
              284  LOAD_FAST                'im'
              286  LOAD_ATTR                encoderinfo
              288  LOAD_STR                 'comment'
              290  BINARY_SUBSCR    
              292  CALL_FUNCTION_1       1  ''
              294  COMPARE_OP               <=
          296_298  POP_JUMP_IF_FALSE   424  'to 424'

 L. 597       300  LOAD_FAST                'fp'
              302  LOAD_METHOD              write
              304  LOAD_CONST               b'!'
              306  LOAD_GLOBAL              o8
              308  LOAD_CONST               254
              310  CALL_FUNCTION_1       1  ''
              312  BINARY_ADD       
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          

 L. 598       318  LOAD_FAST                'im'
              320  LOAD_ATTR                encoderinfo
              322  LOAD_STR                 'comment'
              324  BINARY_SUBSCR    
              326  STORE_FAST               'comment'

 L. 599       328  LOAD_GLOBAL              isinstance
              330  LOAD_FAST                'comment'
              332  LOAD_GLOBAL              str
              334  CALL_FUNCTION_2       2  ''
          336_338  POP_JUMP_IF_FALSE   348  'to 348'

 L. 600       340  LOAD_FAST                'comment'
              342  LOAD_METHOD              encode
              344  CALL_METHOD_0         0  ''
              346  STORE_FAST               'comment'
            348_0  COME_FROM           336  '336'

 L. 601       348  LOAD_GLOBAL              range
              350  LOAD_CONST               0
              352  LOAD_GLOBAL              len
              354  LOAD_FAST                'comment'
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_CONST               255
              360  CALL_FUNCTION_3       3  ''
              362  GET_ITER         
            364_0  COME_FROM           406  '406'
              364  FOR_ITER            410  'to 410'
              366  STORE_FAST               'i'

 L. 602       368  LOAD_FAST                'comment'
              370  LOAD_FAST                'i'
              372  LOAD_FAST                'i'
              374  LOAD_CONST               255
              376  BINARY_ADD       
              378  BUILD_SLICE_2         2 
              380  BINARY_SUBSCR    
              382  STORE_FAST               'subblock'

 L. 603       384  LOAD_FAST                'fp'
              386  LOAD_METHOD              write
              388  LOAD_GLOBAL              o8
              390  LOAD_GLOBAL              len
              392  LOAD_FAST                'subblock'
              394  CALL_FUNCTION_1       1  ''
              396  CALL_FUNCTION_1       1  ''
              398  LOAD_FAST                'subblock'
              400  BINARY_ADD       
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
          406_408  JUMP_BACK           364  'to 364'
            410_0  COME_FROM           364  '364'

 L. 604       410  LOAD_FAST                'fp'
              412  LOAD_METHOD              write
              414  LOAD_GLOBAL              o8
              416  LOAD_CONST               0
              418  CALL_FUNCTION_1       1  ''
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           296  '296'
            424_1  COME_FROM           276  '276'

 L. 605       424  LOAD_STR                 'loop'
              426  LOAD_FAST                'im'
              428  LOAD_ATTR                encoderinfo
              430  <118>                 0  ''
          432_434  POP_JUMP_IF_FALSE   508  'to 508'

 L. 606       436  LOAD_FAST                'im'
              438  LOAD_ATTR                encoderinfo
              440  LOAD_STR                 'loop'
              442  BINARY_SUBSCR    
              444  STORE_FAST               'number_of_loops'

 L. 607       446  LOAD_FAST                'fp'
              448  LOAD_METHOD              write

 L. 608       450  LOAD_CONST               b'!'

 L. 609       452  LOAD_GLOBAL              o8
              454  LOAD_CONST               255
              456  CALL_FUNCTION_1       1  ''

 L. 608       458  BINARY_ADD       

 L. 610       460  LOAD_GLOBAL              o8
              462  LOAD_CONST               11
              464  CALL_FUNCTION_1       1  ''

 L. 608       466  BINARY_ADD       

 L. 611       468  LOAD_CONST               b'NETSCAPE2.0'

 L. 608       470  BINARY_ADD       

 L. 612       472  LOAD_GLOBAL              o8
              474  LOAD_CONST               3
              476  CALL_FUNCTION_1       1  ''

 L. 608       478  BINARY_ADD       

 L. 613       480  LOAD_GLOBAL              o8
              482  LOAD_CONST               1
              484  CALL_FUNCTION_1       1  ''

 L. 608       486  BINARY_ADD       

 L. 614       488  LOAD_GLOBAL              o16
              490  LOAD_FAST                'number_of_loops'
              492  CALL_FUNCTION_1       1  ''

 L. 608       494  BINARY_ADD       

 L. 615       496  LOAD_GLOBAL              o8
              498  LOAD_CONST               0
              500  CALL_FUNCTION_1       1  ''

 L. 608       502  BINARY_ADD       

 L. 607       504  CALL_METHOD_1         1  ''
              506  POP_TOP          
            508_0  COME_FROM           432  '432'

 L. 617       508  LOAD_FAST                'im'
              510  LOAD_ATTR                encoderinfo
              512  LOAD_METHOD              get
              514  LOAD_STR                 'include_color_table'
              516  CALL_METHOD_1         1  ''
              518  STORE_FAST               'include_color_table'

 L. 618       520  LOAD_FAST                'include_color_table'
          522_524  POP_JUMP_IF_FALSE   564  'to 564'

 L. 619       526  LOAD_GLOBAL              _get_palette_bytes
              528  LOAD_FAST                'im'
              530  CALL_FUNCTION_1       1  ''
              532  STORE_FAST               'palette_bytes'

 L. 620       534  LOAD_GLOBAL              _get_color_table_size
              536  LOAD_FAST                'palette_bytes'
              538  CALL_FUNCTION_1       1  ''
              540  STORE_FAST               'color_table_size'

 L. 621       542  LOAD_FAST                'color_table_size'
          544_546  POP_JUMP_IF_FALSE   564  'to 564'

 L. 622       548  LOAD_FAST                'flags'
              550  LOAD_CONST               128
              552  BINARY_OR        
              554  STORE_FAST               'flags'

 L. 623       556  LOAD_FAST                'flags'
              558  LOAD_FAST                'color_table_size'
              560  BINARY_OR        
              562  STORE_FAST               'flags'
            564_0  COME_FROM           544  '544'
            564_1  COME_FROM           522  '522'

 L. 625       564  LOAD_FAST                'fp'
              566  LOAD_METHOD              write

 L. 626       568  LOAD_CONST               b','

 L. 627       570  LOAD_GLOBAL              o16
              572  LOAD_FAST                'offset'
              574  LOAD_CONST               0
              576  BINARY_SUBSCR    
              578  CALL_FUNCTION_1       1  ''

 L. 626       580  BINARY_ADD       

 L. 628       582  LOAD_GLOBAL              o16
              584  LOAD_FAST                'offset'
              586  LOAD_CONST               1
              588  BINARY_SUBSCR    
              590  CALL_FUNCTION_1       1  ''

 L. 626       592  BINARY_ADD       

 L. 629       594  LOAD_GLOBAL              o16
              596  LOAD_FAST                'im'
              598  LOAD_ATTR                size
              600  LOAD_CONST               0
              602  BINARY_SUBSCR    
              604  CALL_FUNCTION_1       1  ''

 L. 626       606  BINARY_ADD       

 L. 630       608  LOAD_GLOBAL              o16
              610  LOAD_FAST                'im'
              612  LOAD_ATTR                size
              614  LOAD_CONST               1
              616  BINARY_SUBSCR    
              618  CALL_FUNCTION_1       1  ''

 L. 626       620  BINARY_ADD       

 L. 631       622  LOAD_GLOBAL              o8
              624  LOAD_FAST                'flags'
              626  CALL_FUNCTION_1       1  ''

 L. 626       628  BINARY_ADD       

 L. 625       630  CALL_METHOD_1         1  ''
              632  POP_TOP          

 L. 633       634  LOAD_FAST                'include_color_table'
          636_638  POP_JUMP_IF_FALSE   660  'to 660'
              640  LOAD_FAST                'color_table_size'
          642_644  POP_JUMP_IF_FALSE   660  'to 660'

 L. 634       646  LOAD_FAST                'fp'
              648  LOAD_METHOD              write
              650  LOAD_GLOBAL              _get_header_palette
              652  LOAD_FAST                'palette_bytes'
              654  CALL_FUNCTION_1       1  ''
              656  CALL_METHOD_1         1  ''
              658  POP_TOP          
            660_0  COME_FROM           642  '642'
            660_1  COME_FROM           636  '636'

 L. 635       660  LOAD_FAST                'fp'
              662  LOAD_METHOD              write
              664  LOAD_GLOBAL              o8
              666  LOAD_CONST               8
              668  CALL_FUNCTION_1       1  ''
              670  CALL_METHOD_1         1  ''
              672  POP_TOP          

Parse error at or near `<121>' instruction at offset 24


def _save_netpbm--- This code section failed: ---

 L. 646         0  LOAD_FAST                'im'
                2  LOAD_METHOD              _dump
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tempfile'

 L. 648         8  SETUP_FINALLY       240  'to 240'

 L. 649        10  LOAD_GLOBAL              open
               12  LOAD_FAST                'filename'
               14  LOAD_STR                 'wb'
               16  CALL_FUNCTION_2       2  ''
               18  SETUP_WITH          186  'to 186'
               20  STORE_FAST               'f'

 L. 650        22  LOAD_FAST                'im'
               24  LOAD_ATTR                mode
               26  LOAD_STR                 'RGB'
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 651        32  LOAD_GLOBAL              subprocess
               34  LOAD_ATTR                check_call

 L. 652        36  LOAD_STR                 'ppmtogif'
               38  LOAD_FAST                'tempfile'
               40  BUILD_LIST_2          2 
               42  LOAD_FAST                'f'
               44  LOAD_GLOBAL              subprocess
               46  LOAD_ATTR                DEVNULL

 L. 651        48  LOAD_CONST               ('stdout', 'stderr')
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  POP_TOP          
               54  JUMP_FORWARD        172  'to 172'
             56_0  COME_FROM            30  '30'

 L. 657        56  LOAD_STR                 'ppmquant'
               58  LOAD_STR                 '256'
               60  LOAD_FAST                'tempfile'
               62  BUILD_LIST_3          3 
               64  STORE_FAST               'quant_cmd'

 L. 658        66  LOAD_STR                 'ppmtogif'
               68  BUILD_LIST_1          1 
               70  STORE_FAST               'togif_cmd'

 L. 659        72  LOAD_GLOBAL              subprocess
               74  LOAD_ATTR                Popen

 L. 660        76  LOAD_FAST                'quant_cmd'
               78  LOAD_GLOBAL              subprocess
               80  LOAD_ATTR                PIPE
               82  LOAD_GLOBAL              subprocess
               84  LOAD_ATTR                DEVNULL

 L. 659        86  LOAD_CONST               ('stdout', 'stderr')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  STORE_FAST               'quant_proc'

 L. 662        92  LOAD_GLOBAL              subprocess
               94  LOAD_ATTR                Popen

 L. 663        96  LOAD_FAST                'togif_cmd'

 L. 664        98  LOAD_FAST                'quant_proc'
              100  LOAD_ATTR                stdout

 L. 665       102  LOAD_FAST                'f'

 L. 666       104  LOAD_GLOBAL              subprocess
              106  LOAD_ATTR                DEVNULL

 L. 662       108  LOAD_CONST               ('stdin', 'stdout', 'stderr')
              110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              112  STORE_FAST               'togif_proc'

 L. 670       114  LOAD_FAST                'quant_proc'
              116  LOAD_ATTR                stdout
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 672       124  LOAD_FAST                'quant_proc'
              126  LOAD_METHOD              wait
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'retcode'

 L. 673       132  LOAD_FAST                'retcode'
              134  POP_JUMP_IF_FALSE   148  'to 148'

 L. 674       136  LOAD_GLOBAL              subprocess
              138  LOAD_METHOD              CalledProcessError
              140  LOAD_FAST                'retcode'
              142  LOAD_FAST                'quant_cmd'
              144  CALL_METHOD_2         2  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           134  '134'

 L. 676       148  LOAD_FAST                'togif_proc'
              150  LOAD_METHOD              wait
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'retcode'

 L. 677       156  LOAD_FAST                'retcode'
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L. 678       160  LOAD_GLOBAL              subprocess
              162  LOAD_METHOD              CalledProcessError
              164  LOAD_FAST                'retcode'
              166  LOAD_FAST                'togif_cmd'
              168  CALL_METHOD_2         2  ''
              170  RAISE_VARARGS_1       1  'exception instance'
            172_0  COME_FROM           158  '158'
            172_1  COME_FROM            54  '54'
              172  POP_BLOCK        
              174  LOAD_CONST               None
              176  DUP_TOP          
              178  DUP_TOP          
              180  CALL_FUNCTION_3       3  ''
              182  POP_TOP          
              184  JUMP_FORWARD        202  'to 202'
            186_0  COME_FROM_WITH       18  '18'
              186  <49>             
              188  POP_JUMP_IF_TRUE    192  'to 192'
              190  <48>             
            192_0  COME_FROM           188  '188'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          
              198  POP_EXCEPT       
              200  POP_TOP          
            202_0  COME_FROM           184  '184'
              202  POP_BLOCK        

 L. 680       204  SETUP_FINALLY       220  'to 220'

 L. 681       206  LOAD_GLOBAL              os
              208  LOAD_METHOD              unlink
              210  LOAD_FAST                'tempfile'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  POP_BLOCK        
              218  JUMP_FORWARD        238  'to 238'
            220_0  COME_FROM_FINALLY   204  '204'

 L. 682       220  DUP_TOP          
              222  LOAD_GLOBAL              OSError
              224  <121>               236  ''
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          

 L. 683       232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
              236  <48>             
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           218  '218'
              238  JUMP_FORWARD        278  'to 278'
            240_0  COME_FROM_FINALLY     8  '8'

 L. 680       240  SETUP_FINALLY       256  'to 256'

 L. 681       242  LOAD_GLOBAL              os
              244  LOAD_METHOD              unlink
              246  LOAD_FAST                'tempfile'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
              252  POP_BLOCK        
              254  JUMP_FORWARD        276  'to 276'
            256_0  COME_FROM_FINALLY   240  '240'

 L. 682       256  DUP_TOP          
              258  LOAD_GLOBAL              OSError
          260_262  <121>               274  ''
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L. 683       270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
              274  <48>             
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM           254  '254'
              276  <48>             
            278_0  COME_FROM           238  '238'

Parse error at or near `DUP_TOP' instruction at offset 176


_FORCE_OPTIMIZE = False

def _get_optimize--- This code section failed: ---

 L. 702         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  LOAD_CONST               ('P', 'L')
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE   136  'to 136'
               10  LOAD_FAST                'info'
               12  POP_JUMP_IF_FALSE   136  'to 136'
               14  LOAD_FAST                'info'
               16  LOAD_METHOD              get
               18  LOAD_STR                 'optimize'
               20  LOAD_CONST               0
               22  CALL_METHOD_2         2  ''
               24  POP_JUMP_IF_FALSE   136  'to 136'

 L. 713        26  LOAD_GLOBAL              _FORCE_OPTIMIZE
               28  JUMP_IF_TRUE_OR_POP    38  'to 38'
               30  LOAD_FAST                'im'
               32  LOAD_ATTR                mode
               34  LOAD_STR                 'L'
               36  COMPARE_OP               ==
             38_0  COME_FROM            28  '28'
               38  STORE_FAST               'optimise'

 L. 714        40  LOAD_FAST                'optimise'
               42  POP_JUMP_IF_TRUE     60  'to 60'
               44  LOAD_FAST                'im'
               46  LOAD_ATTR                width
               48  LOAD_FAST                'im'
               50  LOAD_ATTR                height
               52  BINARY_MULTIPLY  
               54  LOAD_CONST               262144
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE   136  'to 136'
             60_0  COME_FROM            42  '42'

 L. 716        60  BUILD_LIST_0          0 
               62  STORE_FAST               'used_palette_colors'

 L. 717        64  LOAD_GLOBAL              enumerate
               66  LOAD_FAST                'im'
               68  LOAD_METHOD              histogram
               70  CALL_METHOD_0         0  ''
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
             76_0  COME_FROM            98  '98'
             76_1  COME_FROM            86  '86'
               76  FOR_ITER            100  'to 100'
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'i'
               82  STORE_FAST               'count'

 L. 718        84  LOAD_FAST                'count'
               86  POP_JUMP_IF_FALSE_BACK    76  'to 76'

 L. 719        88  LOAD_FAST                'used_palette_colors'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'i'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            76  'to 76'
            100_0  COME_FROM            76  '76'

 L. 721       100  LOAD_FAST                'optimise'
              102  POP_JUMP_IF_TRUE    132  'to 132'

 L. 722       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'used_palette_colors'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_CONST               128
              112  COMPARE_OP               <=

 L. 721       114  POP_JUMP_IF_FALSE   136  'to 136'

 L. 723       116  LOAD_GLOBAL              max
              118  LOAD_FAST                'used_palette_colors'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'used_palette_colors'
              126  CALL_FUNCTION_1       1  ''
              128  COMPARE_OP               >

 L. 721       130  POP_JUMP_IF_FALSE   136  'to 136'
            132_0  COME_FROM           102  '102'

 L. 725       132  LOAD_FAST                'used_palette_colors'
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'
            136_1  COME_FROM           114  '114'
            136_2  COME_FROM            58  '58'
            136_3  COME_FROM            24  '24'
            136_4  COME_FROM            12  '12'
            136_5  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


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


def _get_background--- This code section failed: ---

 L. 767         0  LOAD_CONST               0
                2  STORE_FAST               'background'

 L. 768         4  LOAD_FAST                'infoBackground'
                6  POP_JUMP_IF_FALSE   106  'to 106'

 L. 769         8  LOAD_FAST                'infoBackground'
               10  STORE_FAST               'background'

 L. 770        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'background'
               16  LOAD_GLOBAL              tuple
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE   106  'to 106'

 L. 774        22  SETUP_FINALLY        42  'to 42'

 L. 775        24  LOAD_FAST                'im'
               26  LOAD_ATTR                palette
               28  LOAD_METHOD              getcolor
               30  LOAD_FAST                'background'
               32  LOAD_FAST                'im'
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'background'
               38  POP_BLOCK        
               40  JUMP_FORWARD        106  'to 106'
             42_0  COME_FROM_FINALLY    22  '22'

 L. 776        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  <121>               104  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        96  'to 96'

 L. 777        56  LOAD_GLOBAL              str
               58  LOAD_FAST                'e'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_STR                 'cannot allocate more than 256 colors'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 780        68  POP_BLOCK        
               70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  LOAD_CONST               0
               80  RETURN_VALUE     
             82_0  COME_FROM            66  '66'

 L. 782        82  RAISE_VARARGS_0       0  'reraise'
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM_FINALLY    54  '54'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  <48>             
              104  <48>             
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            40  '40'
            106_2  COME_FROM            20  '20'
            106_3  COME_FROM             6  '6'

 L. 783       106  LOAD_FAST                'background'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 46


def _get_global_header--- This code section failed: ---

 L. 792         0  LOAD_CONST               b'87a'
                2  STORE_FAST               'version'

 L. 793         4  LOAD_CONST               ('transparency', 'duration', 'loop', 'comment')
                6  GET_ITER         
              8_0  COME_FROM            92  '92'
              8_1  COME_FROM            82  '82'
              8_2  COME_FROM            78  '78'
              8_3  COME_FROM            42  '42'
              8_4  COME_FROM            22  '22'
              8_5  COME_FROM            14  '14'
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'extensionKey'

 L. 794        12  LOAD_FAST                'info'
               14  POP_JUMP_IF_FALSE_BACK     8  'to 8'
               16  LOAD_FAST                'extensionKey'
               18  LOAD_FAST                'info'
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 795        24  LOAD_FAST                'extensionKey'
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

 L. 796        44  LOAD_FAST                'extensionKey'
               46  LOAD_STR                 'comment'
               48  COMPARE_OP               ==

 L. 795        50  POP_JUMP_IF_FALSE    84  'to 84'

 L. 796        52  LOAD_CONST               1
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'info'
               58  LOAD_FAST                'extensionKey'
               60  BINARY_SUBSCR    
               62  CALL_FUNCTION_1       1  ''

 L. 795        64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 796        72  LOAD_CONST               255

 L. 795        74  COMPARE_OP               <=
               76  POP_JUMP_IF_TRUE     84  'to 84'
               78  JUMP_BACK             8  'to 8'
             80_0  COME_FROM            70  '70'
               80  POP_TOP          

 L. 798        82  JUMP_BACK             8  'to 8'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            50  '50'

 L. 799        84  LOAD_CONST               b'89a'
               86  STORE_FAST               'version'

 L. 800        88  POP_TOP          
               90  BREAK_LOOP          114  'to 114'
               92  JUMP_BACK             8  'to 8'
             94_0  COME_FROM             8  '8'

 L. 802        94  LOAD_FAST                'im'
               96  LOAD_ATTR                info
               98  LOAD_METHOD              get
              100  LOAD_STR                 'version'
              102  CALL_METHOD_1         1  ''
              104  LOAD_CONST               b'89a'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 803       110  LOAD_CONST               b'89a'
              112  STORE_FAST               'version'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            90  '90'

 L. 805       114  LOAD_GLOBAL              _get_background
              116  LOAD_FAST                'im'
              118  LOAD_FAST                'info'
              120  LOAD_METHOD              get
              122  LOAD_STR                 'background'
              124  CALL_METHOD_1         1  ''
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'background'

 L. 807       130  LOAD_GLOBAL              _get_palette_bytes
              132  LOAD_FAST                'im'
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'palette_bytes'

 L. 808       138  LOAD_GLOBAL              _get_color_table_size
              140  LOAD_FAST                'palette_bytes'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'color_table_size'

 L. 811       146  LOAD_CONST               b'GIF'

 L. 812       148  LOAD_FAST                'version'

 L. 811       150  BINARY_ADD       

 L. 813       152  LOAD_GLOBAL              o16
              154  LOAD_FAST                'im'
              156  LOAD_ATTR                size
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''

 L. 811       164  BINARY_ADD       

 L. 814       166  LOAD_GLOBAL              o16
              168  LOAD_FAST                'im'
              170  LOAD_ATTR                size
              172  LOAD_CONST               1
              174  BINARY_SUBSCR    
              176  CALL_FUNCTION_1       1  ''

 L. 811       178  BINARY_ADD       

 L. 817       180  LOAD_GLOBAL              o8
              182  LOAD_FAST                'color_table_size'
              184  LOAD_CONST               128
              186  BINARY_ADD       
              188  CALL_FUNCTION_1       1  ''

 L. 819       190  LOAD_GLOBAL              o8
              192  LOAD_FAST                'background'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_GLOBAL              o8
              198  LOAD_CONST               0
              200  CALL_FUNCTION_1       1  ''
              202  BINARY_ADD       

 L. 821       204  LOAD_GLOBAL              _get_header_palette
              206  LOAD_FAST                'palette_bytes'
              208  CALL_FUNCTION_1       1  ''

 L. 810       210  BUILD_LIST_4          4 
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def _write_frame_data--- This code section failed: ---

 L. 826         0  SETUP_FINALLY        76  'to 76'

 L. 827         2  LOAD_FAST                'params'
                4  LOAD_FAST                'im_frame'
                6  STORE_ATTR               encoderinfo

 L. 830         8  LOAD_GLOBAL              _write_local_header
               10  LOAD_FAST                'fp'
               12  LOAD_FAST                'im_frame'
               14  LOAD_FAST                'offset'
               16  LOAD_CONST               0
               18  CALL_FUNCTION_4       4  ''
               20  POP_TOP          

 L. 832        22  LOAD_GLOBAL              ImageFile
               24  LOAD_METHOD              _save

 L. 833        26  LOAD_FAST                'im_frame'
               28  LOAD_FAST                'fp'
               30  LOAD_STR                 'gif'
               32  LOAD_CONST               (0, 0)
               34  LOAD_FAST                'im_frame'
               36  LOAD_ATTR                size
               38  BINARY_ADD       
               40  LOAD_CONST               0
               42  LOAD_GLOBAL              RAWMODE
               44  LOAD_FAST                'im_frame'
               46  LOAD_ATTR                mode
               48  BINARY_SUBSCR    
               50  BUILD_TUPLE_4         4 
               52  BUILD_LIST_1          1 

 L. 832        54  CALL_METHOD_3         3  ''
               56  POP_TOP          

 L. 836        58  LOAD_FAST                'fp'
               60  LOAD_METHOD              write
               62  LOAD_CONST               b'\x00'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        

 L. 838        70  LOAD_FAST                'im_frame'
               72  DELETE_ATTR              encoderinfo
               74  JUMP_FORWARD         82  'to 82'
             76_0  COME_FROM_FINALLY     0  '0'
               76  LOAD_FAST                'im_frame'
               78  DELETE_ATTR              encoderinfo
               80  <48>             
             82_0  COME_FROM            74  '74'

Parse error at or near `DELETE_ATTR' instruction at offset 72


def getheader--- This code section failed: ---

 L. 857         0  LOAD_GLOBAL              _get_optimize
                2  LOAD_FAST                'im'
                4  LOAD_FAST                'info'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'used_palette_colors'

 L. 859        10  LOAD_FAST                'info'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 860        18  BUILD_MAP_0           0 
               20  STORE_FAST               'info'
             22_0  COME_FROM            16  '16'

 L. 862        22  LOAD_STR                 'background'
               24  LOAD_FAST                'info'
               26  <118>                 1  ''
               28  POP_JUMP_IF_FALSE    54  'to 54'
               30  LOAD_STR                 'background'
               32  LOAD_FAST                'im'
               34  LOAD_ATTR                info
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L. 863        40  LOAD_FAST                'im'
               42  LOAD_ATTR                info
               44  LOAD_STR                 'background'
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'info'
               50  LOAD_STR                 'background'
               52  STORE_SUBSCR     
             54_0  COME_FROM            38  '38'
             54_1  COME_FROM            28  '28'

 L. 865        54  LOAD_GLOBAL              _normalize_palette
               56  LOAD_FAST                'im'
               58  LOAD_FAST                'palette'
               60  LOAD_FAST                'info'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'im_mod'

 L. 866        66  LOAD_FAST                'im_mod'
               68  LOAD_ATTR                palette
               70  LOAD_FAST                'im'
               72  STORE_ATTR               palette

 L. 867        74  LOAD_FAST                'im_mod'
               76  LOAD_ATTR                im
               78  LOAD_FAST                'im'
               80  STORE_ATTR               im

 L. 868        82  LOAD_GLOBAL              _get_global_header
               84  LOAD_FAST                'im'
               86  LOAD_FAST                'info'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'header'

 L. 870        92  LOAD_FAST                'header'
               94  LOAD_FAST                'used_palette_colors'
               96  BUILD_TUPLE_2         2 
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


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