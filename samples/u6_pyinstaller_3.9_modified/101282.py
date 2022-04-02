# uncompyle6 version 3.7.4
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
            148_0  COME_FROM           202  '202'
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
              202  POP_JUMP_IF_TRUE    148  'to 148'
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
            238_0  COME_FROM           100  '100'

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

Parse error at or near `COME_FROM' instruction at offset 208_0

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

Parse error at or near `<121>' instruction at offset 98

    def _seek--- This code section failed: ---

 L. 141         0  LOAD_FAST                'frame'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    64  'to 64'

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

 L. 148        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _prev_im

 L. 149        56  LOAD_CONST               0
               58  LOAD_FAST                'self'
               60  STORE_ATTR               disposal_method
               62  JUMP_FORWARD         78  'to 78'
             64_0  COME_FROM             6  '6'

 L. 152        64  LOAD_FAST                'self'
               66  LOAD_ATTR                im
               68  POP_JUMP_IF_TRUE     78  'to 78'

 L. 153        70  LOAD_FAST                'self'
               72  LOAD_METHOD              load
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          
             78_0  COME_FROM            68  '68'
             78_1  COME_FROM            62  '62'

 L. 155        78  LOAD_FAST                'frame'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _GifImageFile__frame
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L. 156        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 'cannot seek to frame '
               96  LOAD_FAST                'frame'
               98  FORMAT_VALUE          0  ''
              100  BUILD_STRING_2        2 
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            90  '90'

 L. 157       106  LOAD_FAST                'frame'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _GifImageFile__frame

 L. 159       112  BUILD_LIST_0          0 
              114  LOAD_FAST                'self'
              116  STORE_ATTR               tile

 L. 161       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _GifImageFile__fp
              122  LOAD_FAST                'self'
              124  STORE_ATTR               fp

 L. 162       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _GifImageFile__offset
              130  POP_JUMP_IF_FALSE   162  'to 162'

 L. 164       132  LOAD_FAST                'self'
              134  LOAD_ATTR                fp
              136  LOAD_METHOD              seek
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _GifImageFile__offset
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L. 165       146  LOAD_FAST                'self'
              148  LOAD_METHOD              data
              150  CALL_METHOD_0         0  ''
              152  POP_JUMP_IF_FALSE   156  'to 156'

 L. 166       154  JUMP_BACK           146  'to 146'
            156_0  COME_FROM           152  '152'

 L. 167       156  LOAD_CONST               0
              158  LOAD_FAST                'self'
              160  STORE_ATTR               _GifImageFile__offset
            162_0  COME_FROM           130  '130'

 L. 169       162  LOAD_FAST                'self'
              164  LOAD_ATTR                dispose
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 170       168  LOAD_FAST                'self'
              170  LOAD_ATTR                im
              172  LOAD_METHOD              paste
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                dispose
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                dispose_extent
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          
            186_0  COME_FROM           166  '166'

 L. 172       186  LOAD_CONST               0
              188  LOAD_CONST               ('copy',)
              190  IMPORT_NAME              copy
              192  IMPORT_FROM              copy
              194  STORE_FAST               'copy'
              196  POP_TOP          

 L. 174       198  LOAD_FAST                'copy'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                global_palette
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_FAST                'self'
              208  STORE_ATTR               palette

 L. 176       210  BUILD_MAP_0           0 
              212  STORE_FAST               'info'
            214_0  COME_FROM           558  '558'
            214_1  COME_FROM           382  '382'

 L. 179       214  LOAD_FAST                'self'
              216  LOAD_ATTR                fp
              218  LOAD_METHOD              read
              220  LOAD_CONST               1
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               's'

 L. 180       226  LOAD_FAST                's'
              228  POP_JUMP_IF_FALSE   238  'to 238'
              230  LOAD_FAST                's'
              232  LOAD_CONST               b';'
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   244  'to 244'
            238_0  COME_FROM           228  '228'

 L. 181   238_240  BREAK_LOOP          838  'to 838'
              242  JUMP_BACK           214  'to 214'
            244_0  COME_FROM           236  '236'

 L. 183       244  LOAD_FAST                's'
              246  LOAD_CONST               b'!'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   552  'to 552'

 L. 187       254  LOAD_FAST                'self'
              256  LOAD_ATTR                fp
              258  LOAD_METHOD              read
              260  LOAD_CONST               1
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               's'

 L. 188       266  LOAD_FAST                'self'
              268  LOAD_METHOD              data
              270  CALL_METHOD_0         0  ''
              272  STORE_FAST               'block'

 L. 189       274  LOAD_FAST                's'
              276  LOAD_CONST               0
              278  BINARY_SUBSCR    
              280  LOAD_CONST               249
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   366  'to 366'

 L. 193       288  LOAD_FAST                'block'
              290  LOAD_CONST               0
              292  BINARY_SUBSCR    
              294  STORE_FAST               'flags'

 L. 194       296  LOAD_FAST                'flags'
              298  LOAD_CONST               1
              300  BINARY_AND       
          302_304  POP_JUMP_IF_FALSE   318  'to 318'

 L. 195       306  LOAD_FAST                'block'
              308  LOAD_CONST               3
              310  BINARY_SUBSCR    
              312  LOAD_FAST                'info'
              314  LOAD_STR                 'transparency'
              316  STORE_SUBSCR     
            318_0  COME_FROM           302  '302'

 L. 196       318  LOAD_GLOBAL              i16
              320  LOAD_FAST                'block'
              322  LOAD_CONST               1
              324  CALL_FUNCTION_2       2  ''
              326  LOAD_CONST               10
              328  BINARY_MULTIPLY  
              330  LOAD_FAST                'info'
              332  LOAD_STR                 'duration'
              334  STORE_SUBSCR     

 L. 199       336  LOAD_CONST               28
              338  LOAD_FAST                'flags'
              340  BINARY_AND       
              342  STORE_FAST               'dispose_bits'

 L. 200       344  LOAD_FAST                'dispose_bits'
              346  LOAD_CONST               2
              348  BINARY_RSHIFT    
              350  STORE_FAST               'dispose_bits'

 L. 201       352  LOAD_FAST                'dispose_bits'
          354_356  POP_JUMP_IF_FALSE   536  'to 536'

 L. 206       358  LOAD_FAST                'dispose_bits'
              360  LOAD_FAST                'self'
              362  STORE_ATTR               disposal_method
              364  JUMP_FORWARD        536  'to 536'
            366_0  COME_FROM           284  '284'

 L. 207       366  LOAD_FAST                's'
              368  LOAD_CONST               0
              370  BINARY_SUBSCR    
              372  LOAD_CONST               254
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   436  'to 436'

 L. 211       380  LOAD_FAST                'block'
              382  POP_JUMP_IF_FALSE   214  'to 214'

 L. 212       384  LOAD_STR                 'comment'
              386  LOAD_FAST                'info'
              388  <118>                 0  ''
          390_392  POP_JUMP_IF_FALSE   412  'to 412'

 L. 213       394  LOAD_FAST                'info'
              396  LOAD_STR                 'comment'
              398  DUP_TOP_TWO      
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'block'
              404  INPLACE_ADD      
              406  ROT_THREE        
              408  STORE_SUBSCR     
              410  JUMP_FORWARD        420  'to 420'
            412_0  COME_FROM           390  '390'

 L. 215       412  LOAD_FAST                'block'
              414  LOAD_FAST                'info'
              416  LOAD_STR                 'comment'
              418  STORE_SUBSCR     
            420_0  COME_FROM           410  '410'

 L. 216       420  LOAD_FAST                'self'
              422  LOAD_METHOD              data
              424  CALL_METHOD_0         0  ''
              426  STORE_FAST               'block'
          428_430  JUMP_BACK           380  'to 380'

 L. 217       432  JUMP_BACK           214  'to 214'
              434  JUMP_FORWARD        536  'to 536'
            436_0  COME_FROM           376  '376'

 L. 218       436  LOAD_FAST                's'
              438  LOAD_CONST               0
              440  BINARY_SUBSCR    
              442  LOAD_CONST               255
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   536  'to 536'

 L. 222       450  LOAD_FAST                'block'
              452  LOAD_FAST                'self'
              454  LOAD_ATTR                fp
              456  LOAD_METHOD              tell
              458  CALL_METHOD_0         0  ''
              460  BUILD_TUPLE_2         2 
              462  LOAD_FAST                'info'
              464  LOAD_STR                 'extension'
              466  STORE_SUBSCR     

 L. 223       468  LOAD_FAST                'block'
              470  LOAD_CONST               None
              472  LOAD_CONST               11
              474  BUILD_SLICE_2         2 
              476  BINARY_SUBSCR    
              478  LOAD_CONST               b'NETSCAPE2.0'
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   536  'to 536'

 L. 224       486  LOAD_FAST                'self'
              488  LOAD_METHOD              data
              490  CALL_METHOD_0         0  ''
              492  STORE_FAST               'block'

 L. 225       494  LOAD_GLOBAL              len
              496  LOAD_FAST                'block'
              498  CALL_FUNCTION_1       1  ''
              500  LOAD_CONST               3
              502  COMPARE_OP               >=
          504_506  POP_JUMP_IF_FALSE   536  'to 536'
              508  LOAD_FAST                'block'
              510  LOAD_CONST               0
              512  BINARY_SUBSCR    
              514  LOAD_CONST               1
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   536  'to 536'

 L. 226       522  LOAD_GLOBAL              i16
              524  LOAD_FAST                'block'
              526  LOAD_CONST               1
              528  CALL_FUNCTION_2       2  ''
              530  LOAD_FAST                'info'
              532  LOAD_STR                 'loop'
              534  STORE_SUBSCR     
            536_0  COME_FROM           518  '518'
            536_1  COME_FROM           504  '504'
            536_2  COME_FROM           482  '482'
            536_3  COME_FROM           446  '446'
            536_4  COME_FROM           434  '434'
            536_5  COME_FROM           364  '364'
            536_6  COME_FROM           354  '354'

 L. 227       536  LOAD_FAST                'self'
              538  LOAD_METHOD              data
              540  CALL_METHOD_0         0  ''
          542_544  POP_JUMP_IF_FALSE   836  'to 836'

 L. 228   546_548  JUMP_BACK           536  'to 536'
              550  JUMP_BACK           214  'to 214'
            552_0  COME_FROM           250  '250'

 L. 230       552  LOAD_FAST                's'
              554  LOAD_CONST               b','
              556  COMPARE_OP               ==
              558  POP_JUMP_IF_FALSE   214  'to 214'

 L. 234       560  LOAD_FAST                'self'
              562  LOAD_ATTR                fp
              564  LOAD_METHOD              read
              566  LOAD_CONST               9
              568  CALL_METHOD_1         1  ''
              570  STORE_FAST               's'

 L. 237       572  LOAD_GLOBAL              i16
              574  LOAD_FAST                's'
              576  LOAD_CONST               0
              578  CALL_FUNCTION_2       2  ''
              580  LOAD_GLOBAL              i16
              582  LOAD_FAST                's'
              584  LOAD_CONST               2
              586  CALL_FUNCTION_2       2  ''
              588  ROT_TWO          
              590  STORE_FAST               'x0'
              592  STORE_FAST               'y0'

 L. 238       594  LOAD_FAST                'x0'
              596  LOAD_GLOBAL              i16
              598  LOAD_FAST                's'
              600  LOAD_CONST               4
              602  CALL_FUNCTION_2       2  ''
              604  BINARY_ADD       
              606  LOAD_FAST                'y0'
              608  LOAD_GLOBAL              i16
              610  LOAD_FAST                's'
              612  LOAD_CONST               6
              614  CALL_FUNCTION_2       2  ''
              616  BINARY_ADD       
              618  ROT_TWO          
              620  STORE_FAST               'x1'
              622  STORE_FAST               'y1'

 L. 239       624  LOAD_FAST                'x1'
              626  LOAD_FAST                'self'
              628  LOAD_ATTR                size
              630  LOAD_CONST               0
              632  BINARY_SUBSCR    
              634  COMPARE_OP               >
          636_638  POP_JUMP_IF_TRUE    656  'to 656'
              640  LOAD_FAST                'y1'
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                size
              646  LOAD_CONST               1
              648  BINARY_SUBSCR    
              650  COMPARE_OP               >
          652_654  POP_JUMP_IF_FALSE   690  'to 690'
            656_0  COME_FROM           636  '636'

 L. 240       656  LOAD_GLOBAL              max
              658  LOAD_FAST                'x1'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                size
              664  LOAD_CONST               0
              666  BINARY_SUBSCR    
              668  CALL_FUNCTION_2       2  ''
              670  LOAD_GLOBAL              max
              672  LOAD_FAST                'y1'
              674  LOAD_FAST                'self'
              676  LOAD_ATTR                size
              678  LOAD_CONST               1
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_2       2  ''
              684  BUILD_TUPLE_2         2 
              686  LOAD_FAST                'self'
              688  STORE_ATTR               _size
            690_0  COME_FROM           652  '652'

 L. 241       690  LOAD_FAST                'x0'
              692  LOAD_FAST                'y0'
              694  LOAD_FAST                'x1'
              696  LOAD_FAST                'y1'
              698  BUILD_TUPLE_4         4 
              700  LOAD_FAST                'self'
              702  STORE_ATTR               dispose_extent

 L. 242       704  LOAD_FAST                's'
              706  LOAD_CONST               8
              708  BINARY_SUBSCR    
              710  STORE_FAST               'flags'

 L. 244       712  LOAD_FAST                'flags'
              714  LOAD_CONST               64
              716  BINARY_AND       
              718  LOAD_CONST               0
              720  COMPARE_OP               !=
              722  STORE_FAST               'interlace'

 L. 246       724  LOAD_FAST                'flags'
              726  LOAD_CONST               128
              728  BINARY_AND       
          730_732  POP_JUMP_IF_FALSE   772  'to 772'

 L. 247       734  LOAD_FAST                'flags'
              736  LOAD_CONST               7
              738  BINARY_AND       
              740  LOAD_CONST               1
              742  BINARY_ADD       
              744  STORE_FAST               'bits'

 L. 248       746  LOAD_GLOBAL              ImagePalette
              748  LOAD_METHOD              raw
              750  LOAD_STR                 'RGB'
              752  LOAD_FAST                'self'
              754  LOAD_ATTR                fp
              756  LOAD_METHOD              read
              758  LOAD_CONST               3
              760  LOAD_FAST                'bits'
              762  BINARY_LSHIFT    
              764  CALL_METHOD_1         1  ''
              766  CALL_METHOD_2         2  ''
              768  LOAD_FAST                'self'
              770  STORE_ATTR               palette
            772_0  COME_FROM           730  '730'

 L. 251       772  LOAD_FAST                'self'
              774  LOAD_ATTR                fp
              776  LOAD_METHOD              read
              778  LOAD_CONST               1
              780  CALL_METHOD_1         1  ''
              782  LOAD_CONST               0
              784  BINARY_SUBSCR    
              786  STORE_FAST               'bits'

 L. 252       788  LOAD_FAST                'self'
              790  LOAD_ATTR                fp
              792  LOAD_METHOD              tell
              794  CALL_METHOD_0         0  ''
              796  LOAD_FAST                'self'
              798  STORE_ATTR               _GifImageFile__offset

 L. 254       800  LOAD_STR                 'gif'
              802  LOAD_FAST                'x0'
              804  LOAD_FAST                'y0'
              806  LOAD_FAST                'x1'
              808  LOAD_FAST                'y1'
              810  BUILD_TUPLE_4         4 
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                _GifImageFile__offset
              816  LOAD_FAST                'bits'
              818  LOAD_FAST                'interlace'
              820  BUILD_TUPLE_2         2 
              822  BUILD_TUPLE_4         4 

 L. 253       824  BUILD_LIST_1          1 
              826  LOAD_FAST                'self'
              828  STORE_ATTR               tile

 L. 256   830_832  BREAK_LOOP          838  'to 838'
              834  JUMP_BACK           214  'to 214'
            836_0  COME_FROM           542  '542'

 L. 259       836  JUMP_BACK           214  'to 214'

 L. 262       838  SETUP_FINALLY       962  'to 962'

 L. 263       840  LOAD_FAST                'self'
              842  LOAD_ATTR                disposal_method
              844  LOAD_CONST               2
              846  COMPARE_OP               <
          848_850  POP_JUMP_IF_FALSE   860  'to 860'

 L. 265       852  LOAD_CONST               None
              854  LOAD_FAST                'self'
              856  STORE_ATTR               dispose
              858  JUMP_FORWARD        932  'to 932'
            860_0  COME_FROM           848  '848'

 L. 266       860  LOAD_FAST                'self'
              862  LOAD_ATTR                disposal_method
              864  LOAD_CONST               2
              866  COMPARE_OP               ==
          868_870  POP_JUMP_IF_FALSE   912  'to 912'

 L. 268       872  LOAD_GLOBAL              Image
              874  LOAD_METHOD              _decompression_bomb_check
              876  LOAD_FAST                'self'
              878  LOAD_ATTR                size
              880  CALL_METHOD_1         1  ''
              882  POP_TOP          

 L. 269       884  LOAD_GLOBAL              Image
              886  LOAD_ATTR                core
              888  LOAD_METHOD              fill
              890  LOAD_STR                 'P'
              892  LOAD_FAST                'self'
              894  LOAD_ATTR                size
              896  LOAD_FAST                'self'
              898  LOAD_ATTR                info
              900  LOAD_STR                 'background'
              902  BINARY_SUBSCR    
              904  CALL_METHOD_3         3  ''
              906  LOAD_FAST                'self'
              908  STORE_ATTR               dispose
              910  JUMP_FORWARD        932  'to 932'
            912_0  COME_FROM           868  '868'

 L. 272       912  LOAD_FAST                'self'
              914  LOAD_ATTR                im
          916_918  POP_JUMP_IF_FALSE   932  'to 932'

 L. 273       920  LOAD_FAST                'self'
              922  LOAD_ATTR                im
              924  LOAD_METHOD              copy
              926  CALL_METHOD_0         0  ''
              928  LOAD_FAST                'self'
              930  STORE_ATTR               dispose
            932_0  COME_FROM           916  '916'
            932_1  COME_FROM           910  '910'
            932_2  COME_FROM           858  '858'

 L. 276       932  LOAD_FAST                'self'
              934  LOAD_ATTR                dispose
          936_938  POP_JUMP_IF_FALSE   958  'to 958'

 L. 277       940  LOAD_FAST                'self'
              942  LOAD_METHOD              _crop
              944  LOAD_FAST                'self'
              946  LOAD_ATTR                dispose
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                dispose_extent
              952  CALL_METHOD_2         2  ''
              954  LOAD_FAST                'self'
              956  STORE_ATTR               dispose
            958_0  COME_FROM           936  '936'
              958  POP_BLOCK        
              960  JUMP_FORWARD        986  'to 986'
            962_0  COME_FROM_FINALLY   838  '838'

 L. 278       962  DUP_TOP          
              964  LOAD_GLOBAL              AttributeError
              966  LOAD_GLOBAL              KeyError
              968  BUILD_TUPLE_2         2 
          970_972  <121>               984  ''
              974  POP_TOP          
              976  POP_TOP          
              978  POP_TOP          

 L. 279       980  POP_EXCEPT       
              982  JUMP_FORWARD        986  'to 986'
              984  <48>             
            986_0  COME_FROM           982  '982'
            986_1  COME_FROM           960  '960'

 L. 281       986  LOAD_FAST                'self'
              988  LOAD_ATTR                tile
          990_992  POP_JUMP_IF_TRUE    998  'to 998'

 L. 283       994  LOAD_GLOBAL              EOFError
              996  RAISE_VARARGS_1       1  'exception instance'
            998_0  COME_FROM           990  '990'

 L. 285       998  LOAD_CONST               ('transparency', 'duration', 'comment', 'extension', 'loop')
             1000  GET_ITER         
           1002_0  COME_FROM          1040  '1040'
             1002  FOR_ITER           1056  'to 1056'
             1004  STORE_FAST               'k'

 L. 286      1006  LOAD_FAST                'k'
             1008  LOAD_FAST                'info'
             1010  <118>                 0  ''
         1012_1014  POP_JUMP_IF_FALSE  1032  'to 1032'

 L. 287      1016  LOAD_FAST                'info'
             1018  LOAD_FAST                'k'
             1020  BINARY_SUBSCR    
             1022  LOAD_FAST                'self'
             1024  LOAD_ATTR                info
             1026  LOAD_FAST                'k'
             1028  STORE_SUBSCR     
             1030  JUMP_BACK          1002  'to 1002'
           1032_0  COME_FROM          1012  '1012'

 L. 288      1032  LOAD_FAST                'k'
             1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                info
             1038  <118>                 0  ''
         1040_1042  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 289      1044  LOAD_FAST                'self'
             1046  LOAD_ATTR                info
             1048  LOAD_FAST                'k'
             1050  DELETE_SUBSCR    
         1052_1054  JUMP_BACK          1002  'to 1002'

 L. 291      1056  LOAD_STR                 'L'
             1058  LOAD_FAST                'self'
             1060  STORE_ATTR               mode

 L. 292      1062  LOAD_FAST                'self'
             1064  LOAD_ATTR                palette
         1066_1068  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 293      1070  LOAD_STR                 'P'
             1072  LOAD_FAST                'self'
             1074  STORE_ATTR               mode
           1076_0  COME_FROM          1066  '1066'

Parse error at or near `CALL_FINALLY' instruction at offset 24

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

    def _close__fp--- This code section failed: ---

 L. 313         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 314         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _GifImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 315        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _GifImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 316        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 317        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 319        50  LOAD_CONST               None
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

 L. 345         0  LOAD_FAST                'im'
                2  LOAD_ATTR                mode
                4  LOAD_GLOBAL              RAWMODE
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 346        10  LOAD_FAST                'im'
               12  LOAD_METHOD              load
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          

 L. 347        18  LOAD_FAST                'im'
               20  RETURN_VALUE     
             22_0  COME_FROM             8  '8'

 L. 348        22  LOAD_GLOBAL              Image
               24  LOAD_METHOD              getmodebase
               26  LOAD_FAST                'im'
               28  LOAD_ATTR                mode
               30  CALL_METHOD_1         1  ''
               32  LOAD_STR                 'RGB'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   102  'to 102'

 L. 349        38  LOAD_FAST                'initial_call'
               40  POP_JUMP_IF_FALSE    92  'to 92'

 L. 350        42  LOAD_CONST               256
               44  STORE_FAST               'palette_size'

 L. 351        46  LOAD_FAST                'im'
               48  LOAD_ATTR                palette
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 352        52  LOAD_GLOBAL              len
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

 L. 353        74  LOAD_FAST                'im'
               76  LOAD_ATTR                convert
               78  LOAD_STR                 'P'
               80  LOAD_GLOBAL              Image
               82  LOAD_ATTR                ADAPTIVE
               84  LOAD_FAST                'palette_size'
               86  LOAD_CONST               ('palette', 'colors')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  RETURN_VALUE     
             92_0  COME_FROM            40  '40'

 L. 355        92  LOAD_FAST                'im'
               94  LOAD_METHOD              convert
               96  LOAD_STR                 'P'
               98  CALL_METHOD_1         1  ''
              100  RETURN_VALUE     
            102_0  COME_FROM            36  '36'

 L. 356       102  LOAD_FAST                'im'
              104  LOAD_METHOD              convert
              106  LOAD_STR                 'L'
              108  CALL_METHOD_1         1  ''
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _normalize_palette--- This code section failed: ---

 L. 371         0  LOAD_CONST               None
                2  STORE_FAST               'source_palette'

 L. 372         4  LOAD_FAST                'palette'
                6  POP_JUMP_IF_FALSE   106  'to 106'

 L. 374         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'palette'
               12  LOAD_GLOBAL              bytes
               14  LOAD_GLOBAL              bytearray
               16  LOAD_GLOBAL              list
               18  BUILD_TUPLE_3         3 
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    40  'to 40'

 L. 375        24  LOAD_GLOBAL              bytearray
               26  LOAD_FAST                'palette'
               28  LOAD_CONST               None
               30  LOAD_CONST               768
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'source_palette'
             40_0  COME_FROM            22  '22'

 L. 376        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'palette'
               44  LOAD_GLOBAL              ImagePalette
               46  LOAD_ATTR                ImagePalette
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE   106  'to 106'

 L. 377        52  LOAD_GLOBAL              bytearray

 L. 378        54  LOAD_GLOBAL              itertools
               56  LOAD_ATTR                chain
               58  LOAD_METHOD              from_iterable

 L. 379        60  LOAD_GLOBAL              zip

 L. 380        62  LOAD_FAST                'palette'
               64  LOAD_ATTR                palette
               66  LOAD_CONST               None
               68  LOAD_CONST               256
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    

 L. 381        74  LOAD_FAST                'palette'
               76  LOAD_ATTR                palette
               78  LOAD_CONST               256
               80  LOAD_CONST               512
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    

 L. 382        86  LOAD_FAST                'palette'
               88  LOAD_ATTR                palette
               90  LOAD_CONST               512
               92  LOAD_CONST               768
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    

 L. 379        98  CALL_FUNCTION_3       3  ''

 L. 378       100  CALL_METHOD_1         1  ''

 L. 377       102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'source_palette'
            106_0  COME_FROM            50  '50'
            106_1  COME_FROM             6  '6'

 L. 387       106  LOAD_FAST                'im'
              108  LOAD_ATTR                mode
              110  LOAD_STR                 'P'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   142  'to 142'

 L. 388       116  LOAD_FAST                'source_palette'
              118  POP_JUMP_IF_TRUE    184  'to 184'

 L. 389       120  LOAD_FAST                'im'
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

 L. 391       142  LOAD_FAST                'source_palette'
              144  POP_JUMP_IF_TRUE    168  'to 168'

 L. 392       146  LOAD_GLOBAL              bytearray
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

 L. 393       168  LOAD_GLOBAL              ImagePalette
              170  LOAD_ATTR                ImagePalette
              172  LOAD_STR                 'RGB'
              174  LOAD_FAST                'source_palette'
              176  LOAD_CONST               ('palette',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  LOAD_FAST                'im'
              182  STORE_ATTR               palette
            184_0  COME_FROM           140  '140'
            184_1  COME_FROM           118  '118'

 L. 395       184  LOAD_GLOBAL              _get_optimize
              186  LOAD_FAST                'im'
              188  LOAD_FAST                'info'
              190  CALL_FUNCTION_2       2  ''
              192  STORE_FAST               'used_palette_colors'

 L. 396       194  LOAD_FAST                'used_palette_colors'
              196  LOAD_CONST               None
              198  <117>                 1  ''
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 397       202  LOAD_FAST                'im'
              204  LOAD_METHOD              remap_palette
              206  LOAD_FAST                'used_palette_colors'
              208  LOAD_FAST                'source_palette'
              210  CALL_METHOD_2         2  ''
              212  RETURN_VALUE     
            214_0  COME_FROM           200  '200'

 L. 399       214  LOAD_FAST                'source_palette'
              216  LOAD_FAST                'im'
              218  LOAD_ATTR                palette
              220  STORE_ATTR               palette

 L. 400       222  LOAD_FAST                'im'
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

 L. 426         0  LOAD_FAST                'im'
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

 L. 427        22  LOAD_FAST                'im'
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

 L. 429        44  BUILD_LIST_0          0 
               46  STORE_FAST               'im_frames'

 L. 430        48  LOAD_CONST               0
               50  STORE_FAST               'frame_count'

 L. 431        52  LOAD_CONST               None
               54  STORE_FAST               'background_im'

 L. 432        56  LOAD_GLOBAL              itertools
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
            80_82  FOR_ITER            486  'to 486'
               84  STORE_FAST               'imSequence'

 L. 433        86  LOAD_GLOBAL              ImageSequence
               88  LOAD_METHOD              Iterator
               90  LOAD_FAST                'imSequence'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
             96_0  COME_FROM           430  '430'
            96_98  FOR_ITER            484  'to 484'
              100  STORE_FAST               'im_frame'

 L. 435       102  LOAD_GLOBAL              _normalize_mode
              104  LOAD_FAST                'im_frame'
              106  LOAD_METHOD              copy
              108  CALL_METHOD_0         0  ''
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'im_frame'

 L. 436       114  LOAD_FAST                'frame_count'
              116  LOAD_CONST               0
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   156  'to 156'

 L. 437       122  LOAD_FAST                'im_frame'
              124  LOAD_ATTR                info
              126  LOAD_METHOD              items
              128  CALL_METHOD_0         0  ''
              130  GET_ITER         
              132  FOR_ITER            156  'to 156'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'k'
              138  STORE_FAST               'v'

 L. 438       140  LOAD_FAST                'im'
              142  LOAD_ATTR                encoderinfo
              144  LOAD_METHOD              setdefault
              146  LOAD_FAST                'k'
              148  LOAD_FAST                'v'
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          
              154  JUMP_BACK           132  'to 132'
            156_0  COME_FROM           120  '120'

 L. 439       156  LOAD_GLOBAL              _normalize_palette
              158  LOAD_FAST                'im_frame'
              160  LOAD_FAST                'palette'
              162  LOAD_FAST                'im'
              164  LOAD_ATTR                encoderinfo
              166  CALL_FUNCTION_3       3  ''
              168  STORE_FAST               'im_frame'

 L. 441       170  LOAD_FAST                'im'
              172  LOAD_ATTR                encoderinfo
              174  LOAD_METHOD              copy
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'encoderinfo'

 L. 442       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'duration'
              184  LOAD_GLOBAL              list
              186  LOAD_GLOBAL              tuple
              188  BUILD_TUPLE_2         2 
              190  CALL_FUNCTION_2       2  ''
              192  POP_JUMP_IF_FALSE   206  'to 206'

 L. 443       194  LOAD_FAST                'duration'
              196  LOAD_FAST                'frame_count'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'encoderinfo'
              202  LOAD_STR                 'duration'
              204  STORE_SUBSCR     
            206_0  COME_FROM           192  '192'

 L. 444       206  LOAD_GLOBAL              isinstance
              208  LOAD_FAST                'disposal'
              210  LOAD_GLOBAL              list
              212  LOAD_GLOBAL              tuple
              214  BUILD_TUPLE_2         2 
              216  CALL_FUNCTION_2       2  ''
              218  POP_JUMP_IF_FALSE   232  'to 232'

 L. 445       220  LOAD_FAST                'disposal'
              222  LOAD_FAST                'frame_count'
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'encoderinfo'
              228  LOAD_STR                 'disposal'
              230  STORE_SUBSCR     
            232_0  COME_FROM           218  '218'

 L. 446       232  LOAD_FAST                'frame_count'
              234  LOAD_CONST               1
              236  INPLACE_ADD      
              238  STORE_FAST               'frame_count'

 L. 448       240  LOAD_FAST                'im_frames'
          242_244  POP_JUMP_IF_FALSE   460  'to 460'

 L. 450       246  LOAD_FAST                'im_frames'
              248  LOAD_CONST               -1
              250  BINARY_SUBSCR    
              252  STORE_FAST               'previous'

 L. 451       254  LOAD_FAST                'encoderinfo'
              256  LOAD_METHOD              get
              258  LOAD_STR                 'disposal'
              260  CALL_METHOD_1         1  ''
              262  LOAD_CONST               2
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   350  'to 350'

 L. 452       270  LOAD_FAST                'background_im'
              272  LOAD_CONST               None
              274  <117>                 0  ''
          276_278  POP_JUMP_IF_FALSE   344  'to 344'

 L. 453       280  LOAD_GLOBAL              _get_background

 L. 454       282  LOAD_FAST                'im'

 L. 455       284  LOAD_FAST                'im'
              286  LOAD_ATTR                encoderinfo
              288  LOAD_METHOD              get
              290  LOAD_STR                 'background'
              292  LOAD_FAST                'im'
              294  LOAD_ATTR                info
              296  LOAD_METHOD              get
              298  LOAD_STR                 'background'
              300  CALL_METHOD_1         1  ''
              302  CALL_METHOD_2         2  ''

 L. 453       304  CALL_FUNCTION_2       2  ''
              306  STORE_FAST               'background'

 L. 457       308  LOAD_GLOBAL              Image
              310  LOAD_METHOD              new
              312  LOAD_STR                 'P'
              314  LOAD_FAST                'im_frame'
              316  LOAD_ATTR                size
              318  LOAD_FAST                'background'
              320  CALL_METHOD_3         3  ''
              322  STORE_FAST               'background_im'

 L. 458       324  LOAD_FAST                'background_im'
              326  LOAD_METHOD              putpalette
              328  LOAD_FAST                'im_frames'
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
              334  LOAD_STR                 'im'
              336  BINARY_SUBSCR    
              338  LOAD_ATTR                palette
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
            344_0  COME_FROM           276  '276'

 L. 459       344  LOAD_FAST                'background_im'
              346  STORE_FAST               'base_im'
              348  JUMP_FORWARD        358  'to 358'
            350_0  COME_FROM           266  '266'

 L. 461       350  LOAD_FAST                'previous'
              352  LOAD_STR                 'im'
              354  BINARY_SUBSCR    
              356  STORE_FAST               'base_im'
            358_0  COME_FROM           348  '348'

 L. 462       358  LOAD_GLOBAL              _get_palette_bytes
              360  LOAD_FAST                'im_frame'
              362  CALL_FUNCTION_1       1  ''
              364  LOAD_GLOBAL              _get_palette_bytes
              366  LOAD_FAST                'base_im'
              368  CALL_FUNCTION_1       1  ''
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   390  'to 390'

 L. 463       376  LOAD_GLOBAL              ImageChops
              378  LOAD_METHOD              subtract_modulo
              380  LOAD_FAST                'im_frame'
              382  LOAD_FAST                'base_im'
              384  CALL_METHOD_2         2  ''
              386  STORE_FAST               'delta'
              388  JUMP_FORWARD        414  'to 414'
            390_0  COME_FROM           372  '372'

 L. 465       390  LOAD_GLOBAL              ImageChops
              392  LOAD_METHOD              subtract_modulo

 L. 466       394  LOAD_FAST                'im_frame'
              396  LOAD_METHOD              convert
              398  LOAD_STR                 'RGB'
              400  CALL_METHOD_1         1  ''
              402  LOAD_FAST                'base_im'
              404  LOAD_METHOD              convert
              406  LOAD_STR                 'RGB'
              408  CALL_METHOD_1         1  ''

 L. 465       410  CALL_METHOD_2         2  ''
              412  STORE_FAST               'delta'
            414_0  COME_FROM           388  '388'

 L. 468       414  LOAD_FAST                'delta'
              416  LOAD_METHOD              getbbox
              418  CALL_METHOD_0         0  ''
              420  STORE_FAST               'bbox'

 L. 469       422  LOAD_FAST                'bbox'
          424_426  POP_JUMP_IF_TRUE    464  'to 464'

 L. 471       428  LOAD_FAST                'duration'
              430  POP_JUMP_IF_FALSE    96  'to 96'

 L. 472       432  LOAD_FAST                'previous'
              434  LOAD_STR                 'encoderinfo'
              436  BINARY_SUBSCR    
              438  LOAD_STR                 'duration'
              440  DUP_TOP_TWO      
              442  BINARY_SUBSCR    
              444  LOAD_FAST                'encoderinfo'
              446  LOAD_STR                 'duration'
              448  BINARY_SUBSCR    
              450  INPLACE_ADD      
              452  ROT_THREE        
              454  STORE_SUBSCR     

 L. 473       456  JUMP_BACK            96  'to 96'
              458  JUMP_FORWARD        464  'to 464'
            460_0  COME_FROM           242  '242'

 L. 475       460  LOAD_CONST               None
              462  STORE_FAST               'bbox'
            464_0  COME_FROM           458  '458'
            464_1  COME_FROM           424  '424'

 L. 476       464  LOAD_FAST                'im_frames'
              466  LOAD_METHOD              append
              468  LOAD_FAST                'im_frame'
              470  LOAD_FAST                'bbox'
              472  LOAD_FAST                'encoderinfo'
              474  LOAD_CONST               ('im', 'bbox', 'encoderinfo')
              476  BUILD_CONST_KEY_MAP_3     3 
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          
              482  JUMP_BACK            96  'to 96'
              484  JUMP_BACK            80  'to 80'

 L. 478       486  LOAD_GLOBAL              len
              488  LOAD_FAST                'im_frames'
              490  CALL_FUNCTION_1       1  ''
              492  LOAD_CONST               1
              494  COMPARE_OP               >
          496_498  POP_JUMP_IF_FALSE   632  'to 632'

 L. 479       500  LOAD_FAST                'im_frames'
              502  GET_ITER         
              504  FOR_ITER            628  'to 628'
              506  STORE_FAST               'frame_data'

 L. 480       508  LOAD_FAST                'frame_data'
              510  LOAD_STR                 'im'
              512  BINARY_SUBSCR    
              514  STORE_FAST               'im_frame'

 L. 481       516  LOAD_FAST                'frame_data'
              518  LOAD_STR                 'bbox'
              520  BINARY_SUBSCR    
          522_524  POP_JUMP_IF_TRUE    564  'to 564'

 L. 483       526  LOAD_GLOBAL              _get_global_header
              528  LOAD_FAST                'im_frame'
              530  LOAD_FAST                'frame_data'
              532  LOAD_STR                 'encoderinfo'
              534  BINARY_SUBSCR    
              536  CALL_FUNCTION_2       2  ''
              538  GET_ITER         
              540  FOR_ITER            558  'to 558'
              542  STORE_FAST               's'

 L. 484       544  LOAD_FAST                'fp'
              546  LOAD_METHOD              write
              548  LOAD_FAST                's'
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          
          554_556  JUMP_BACK           540  'to 540'

 L. 485       558  LOAD_CONST               (0, 0)
              560  STORE_FAST               'offset'
              562  JUMP_FORWARD        606  'to 606'
            564_0  COME_FROM           522  '522'

 L. 488       564  LOAD_CONST               True
              566  LOAD_FAST                'frame_data'
              568  LOAD_STR                 'encoderinfo'
              570  BINARY_SUBSCR    
              572  LOAD_STR                 'include_color_table'
              574  STORE_SUBSCR     

 L. 490       576  LOAD_FAST                'im_frame'
              578  LOAD_METHOD              crop
              580  LOAD_FAST                'frame_data'
              582  LOAD_STR                 'bbox'
              584  BINARY_SUBSCR    
              586  CALL_METHOD_1         1  ''
              588  STORE_FAST               'im_frame'

 L. 491       590  LOAD_FAST                'frame_data'
              592  LOAD_STR                 'bbox'
              594  BINARY_SUBSCR    
              596  LOAD_CONST               None
              598  LOAD_CONST               2
              600  BUILD_SLICE_2         2 
              602  BINARY_SUBSCR    
              604  STORE_FAST               'offset'
            606_0  COME_FROM           562  '562'

 L. 492       606  LOAD_GLOBAL              _write_frame_data
              608  LOAD_FAST                'fp'
              610  LOAD_FAST                'im_frame'
              612  LOAD_FAST                'offset'
              614  LOAD_FAST                'frame_data'
              616  LOAD_STR                 'encoderinfo'
              618  BINARY_SUBSCR    
              620  CALL_FUNCTION_4       4  ''
              622  POP_TOP          
          624_626  JUMP_BACK           504  'to 504'

 L. 493       628  LOAD_CONST               True
              630  RETURN_VALUE     
            632_0  COME_FROM           496  '496'

 L. 494       632  LOAD_STR                 'duration'
              634  LOAD_FAST                'im'
              636  LOAD_ATTR                encoderinfo
              638  <118>                 0  ''
          640_642  POP_JUMP_IF_FALSE   686  'to 686'
              644  LOAD_GLOBAL              isinstance

 L. 495       646  LOAD_FAST                'im'
              648  LOAD_ATTR                encoderinfo
              650  LOAD_STR                 'duration'
              652  BINARY_SUBSCR    
              654  LOAD_GLOBAL              list
              656  LOAD_GLOBAL              tuple
              658  BUILD_TUPLE_2         2 

 L. 494       660  CALL_FUNCTION_2       2  ''
          662_664  POP_JUMP_IF_FALSE   686  'to 686'

 L. 498       666  LOAD_GLOBAL              sum
              668  LOAD_FAST                'im'
              670  LOAD_ATTR                encoderinfo
              672  LOAD_STR                 'duration'
              674  BINARY_SUBSCR    
              676  CALL_FUNCTION_1       1  ''
              678  LOAD_FAST                'im'
              680  LOAD_ATTR                encoderinfo
              682  LOAD_STR                 'duration'
              684  STORE_SUBSCR     
            686_0  COME_FROM           662  '662'
            686_1  COME_FROM           640  '640'

Parse error at or near `<117>' instruction at offset 274


def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save--- This code section failed: ---

 L. 507         0  LOAD_STR                 'palette'
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

 L. 508        20  LOAD_FAST                'im'
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

 L. 510        44  LOAD_CONST               None
               46  STORE_FAST               'palette'

 L. 511        48  LOAD_FAST                'im'
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

 L. 513        68  LOAD_FAST                'save_all'
               70  POP_JUMP_IF_FALSE    84  'to 84'
               72  LOAD_GLOBAL              _write_multiple_frames
               74  LOAD_FAST                'im'
               76  LOAD_FAST                'fp'
               78  LOAD_FAST                'palette'
               80  CALL_FUNCTION_3       3  ''
               82  POP_JUMP_IF_TRUE     96  'to 96'
             84_0  COME_FROM            70  '70'

 L. 514        84  LOAD_GLOBAL              _write_single_frame
               86  LOAD_FAST                'im'
               88  LOAD_FAST                'fp'
               90  LOAD_FAST                'palette'
               92  CALL_FUNCTION_3       3  ''
               94  POP_TOP          
             96_0  COME_FROM            82  '82'

 L. 516        96  LOAD_FAST                'fp'
               98  LOAD_METHOD              write
              100  LOAD_CONST               b';'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 518       106  LOAD_GLOBAL              hasattr
              108  LOAD_FAST                'fp'
              110  LOAD_STR                 'flush'
              112  CALL_FUNCTION_2       2  ''
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L. 519       116  LOAD_FAST                'fp'
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

 L. 533         0  LOAD_CONST               False
                2  STORE_FAST               'transparent_color_exists'

 L. 534         4  SETUP_FINALLY        20  'to 20'

 L. 535         6  LOAD_FAST                'im'
                8  LOAD_ATTR                encoderinfo
               10  LOAD_STR                 'transparency'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'transparency'
               16  POP_BLOCK        
               18  JUMP_FORWARD         38  'to 38'
             20_0  COME_FROM_FINALLY     4  '4'

 L. 536        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                36  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 537        32  POP_EXCEPT       
               34  JUMP_FORWARD        108  'to 108'
               36  <48>             
             38_0  COME_FROM            18  '18'

 L. 539        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'transparency'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'transparency'

 L. 541        46  LOAD_CONST               True
               48  STORE_FAST               'transparent_color_exists'

 L. 543        50  LOAD_GLOBAL              _get_optimize
               52  LOAD_FAST                'im'
               54  LOAD_FAST                'im'
               56  LOAD_ATTR                encoderinfo
               58  CALL_FUNCTION_2       2  ''
               60  STORE_FAST               'used_palette_colors'

 L. 544        62  LOAD_FAST                'used_palette_colors'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE   108  'to 108'

 L. 546        70  SETUP_FINALLY        86  'to 86'

 L. 547        72  LOAD_FAST                'used_palette_colors'
               74  LOAD_METHOD              index
               76  LOAD_FAST                'transparency'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'transparency'
               82  POP_BLOCK        
               84  JUMP_FORWARD        108  'to 108'
             86_0  COME_FROM_FINALLY    70  '70'

 L. 548        86  DUP_TOP          
               88  LOAD_GLOBAL              ValueError
               90  <121>               106  ''
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 549        98  LOAD_CONST               False
              100  STORE_FAST               'transparent_color_exists'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            84  '84'
            108_2  COME_FROM            68  '68'
            108_3  COME_FROM            34  '34'

 L. 551       108  LOAD_STR                 'duration'
              110  LOAD_FAST                'im'
              112  LOAD_ATTR                encoderinfo
              114  <118>                 0  ''
              116  POP_JUMP_IF_FALSE   138  'to 138'

 L. 552       118  LOAD_GLOBAL              int
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

 L. 554       138  LOAD_CONST               0
              140  STORE_FAST               'duration'
            142_0  COME_FROM           136  '136'

 L. 556       142  LOAD_GLOBAL              int
              144  LOAD_FAST                'im'
              146  LOAD_ATTR                encoderinfo
              148  LOAD_METHOD              get
              150  LOAD_STR                 'disposal'
              152  LOAD_CONST               0
              154  CALL_METHOD_2         2  ''
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'disposal'

 L. 558       160  LOAD_FAST                'transparent_color_exists'
              162  POP_JUMP_IF_TRUE    178  'to 178'
              164  LOAD_FAST                'duration'
              166  LOAD_CONST               0
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_TRUE    178  'to 178'
              172  LOAD_FAST                'disposal'
          174_176  POP_JUMP_IF_FALSE   268  'to 268'
            178_0  COME_FROM           170  '170'
            178_1  COME_FROM           162  '162'

 L. 559       178  LOAD_FAST                'transparent_color_exists'
              180  POP_JUMP_IF_FALSE   186  'to 186'
              182  LOAD_CONST               1
              184  JUMP_FORWARD        188  'to 188'
            186_0  COME_FROM           180  '180'
              186  LOAD_CONST               0
            188_0  COME_FROM           184  '184'
              188  STORE_FAST               'packed_flag'

 L. 560       190  LOAD_FAST                'packed_flag'
              192  LOAD_FAST                'disposal'
              194  LOAD_CONST               2
              196  BINARY_LSHIFT    
              198  INPLACE_OR       
              200  STORE_FAST               'packed_flag'

 L. 561       202  LOAD_FAST                'transparent_color_exists'
              204  POP_JUMP_IF_TRUE    210  'to 210'

 L. 562       206  LOAD_CONST               0
              208  STORE_FAST               'transparency'
            210_0  COME_FROM           204  '204'

 L. 564       210  LOAD_FAST                'fp'
              212  LOAD_METHOD              write

 L. 565       214  LOAD_CONST               b'!'

 L. 566       216  LOAD_GLOBAL              o8
              218  LOAD_CONST               249
              220  CALL_FUNCTION_1       1  ''

 L. 565       222  BINARY_ADD       

 L. 567       224  LOAD_GLOBAL              o8
              226  LOAD_CONST               4
              228  CALL_FUNCTION_1       1  ''

 L. 565       230  BINARY_ADD       

 L. 568       232  LOAD_GLOBAL              o8
              234  LOAD_FAST                'packed_flag'
              236  CALL_FUNCTION_1       1  ''

 L. 565       238  BINARY_ADD       

 L. 569       240  LOAD_GLOBAL              o16
              242  LOAD_FAST                'duration'
              244  CALL_FUNCTION_1       1  ''

 L. 565       246  BINARY_ADD       

 L. 570       248  LOAD_GLOBAL              o8
              250  LOAD_FAST                'transparency'
              252  CALL_FUNCTION_1       1  ''

 L. 565       254  BINARY_ADD       

 L. 571       256  LOAD_GLOBAL              o8
              258  LOAD_CONST               0
              260  CALL_FUNCTION_1       1  ''

 L. 565       262  BINARY_ADD       

 L. 564       264  CALL_METHOD_1         1  ''
              266  POP_TOP          
            268_0  COME_FROM           174  '174'

 L. 574       268  LOAD_STR                 'comment'
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

 L. 575       300  LOAD_FAST                'fp'
              302  LOAD_METHOD              write
              304  LOAD_CONST               b'!'
              306  LOAD_GLOBAL              o8
              308  LOAD_CONST               254
              310  CALL_FUNCTION_1       1  ''
              312  BINARY_ADD       
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          

 L. 576       318  LOAD_FAST                'im'
              320  LOAD_ATTR                encoderinfo
              322  LOAD_STR                 'comment'
              324  BINARY_SUBSCR    
              326  STORE_FAST               'comment'

 L. 577       328  LOAD_GLOBAL              isinstance
              330  LOAD_FAST                'comment'
              332  LOAD_GLOBAL              str
              334  CALL_FUNCTION_2       2  ''
          336_338  POP_JUMP_IF_FALSE   348  'to 348'

 L. 578       340  LOAD_FAST                'comment'
              342  LOAD_METHOD              encode
              344  CALL_METHOD_0         0  ''
              346  STORE_FAST               'comment'
            348_0  COME_FROM           336  '336'

 L. 579       348  LOAD_GLOBAL              range
              350  LOAD_CONST               0
              352  LOAD_GLOBAL              len
              354  LOAD_FAST                'comment'
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_CONST               255
              360  CALL_FUNCTION_3       3  ''
              362  GET_ITER         
              364  FOR_ITER            410  'to 410'
              366  STORE_FAST               'i'

 L. 580       368  LOAD_FAST                'comment'
              370  LOAD_FAST                'i'
              372  LOAD_FAST                'i'
              374  LOAD_CONST               255
              376  BINARY_ADD       
              378  BUILD_SLICE_2         2 
              380  BINARY_SUBSCR    
              382  STORE_FAST               'subblock'

 L. 581       384  LOAD_FAST                'fp'
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

 L. 582       410  LOAD_FAST                'fp'
              412  LOAD_METHOD              write
              414  LOAD_GLOBAL              o8
              416  LOAD_CONST               0
              418  CALL_FUNCTION_1       1  ''
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           296  '296'
            424_1  COME_FROM           276  '276'

 L. 583       424  LOAD_STR                 'loop'
              426  LOAD_FAST                'im'
              428  LOAD_ATTR                encoderinfo
              430  <118>                 0  ''
          432_434  POP_JUMP_IF_FALSE   508  'to 508'

 L. 584       436  LOAD_FAST                'im'
              438  LOAD_ATTR                encoderinfo
              440  LOAD_STR                 'loop'
              442  BINARY_SUBSCR    
              444  STORE_FAST               'number_of_loops'

 L. 585       446  LOAD_FAST                'fp'
              448  LOAD_METHOD              write

 L. 586       450  LOAD_CONST               b'!'

 L. 587       452  LOAD_GLOBAL              o8
              454  LOAD_CONST               255
              456  CALL_FUNCTION_1       1  ''

 L. 586       458  BINARY_ADD       

 L. 588       460  LOAD_GLOBAL              o8
              462  LOAD_CONST               11
              464  CALL_FUNCTION_1       1  ''

 L. 586       466  BINARY_ADD       

 L. 589       468  LOAD_CONST               b'NETSCAPE2.0'

 L. 586       470  BINARY_ADD       

 L. 590       472  LOAD_GLOBAL              o8
              474  LOAD_CONST               3
              476  CALL_FUNCTION_1       1  ''

 L. 586       478  BINARY_ADD       

 L. 591       480  LOAD_GLOBAL              o8
              482  LOAD_CONST               1
              484  CALL_FUNCTION_1       1  ''

 L. 586       486  BINARY_ADD       

 L. 592       488  LOAD_GLOBAL              o16
              490  LOAD_FAST                'number_of_loops'
              492  CALL_FUNCTION_1       1  ''

 L. 586       494  BINARY_ADD       

 L. 593       496  LOAD_GLOBAL              o8
              498  LOAD_CONST               0
              500  CALL_FUNCTION_1       1  ''

 L. 586       502  BINARY_ADD       

 L. 585       504  CALL_METHOD_1         1  ''
              506  POP_TOP          
            508_0  COME_FROM           432  '432'

 L. 595       508  LOAD_FAST                'im'
              510  LOAD_ATTR                encoderinfo
              512  LOAD_METHOD              get
              514  LOAD_STR                 'include_color_table'
              516  CALL_METHOD_1         1  ''
              518  STORE_FAST               'include_color_table'

 L. 596       520  LOAD_FAST                'include_color_table'
          522_524  POP_JUMP_IF_FALSE   564  'to 564'

 L. 597       526  LOAD_GLOBAL              _get_palette_bytes
              528  LOAD_FAST                'im'
              530  CALL_FUNCTION_1       1  ''
              532  STORE_FAST               'palette_bytes'

 L. 598       534  LOAD_GLOBAL              _get_color_table_size
              536  LOAD_FAST                'palette_bytes'
              538  CALL_FUNCTION_1       1  ''
              540  STORE_FAST               'color_table_size'

 L. 599       542  LOAD_FAST                'color_table_size'
          544_546  POP_JUMP_IF_FALSE   564  'to 564'

 L. 600       548  LOAD_FAST                'flags'
              550  LOAD_CONST               128
              552  BINARY_OR        
              554  STORE_FAST               'flags'

 L. 601       556  LOAD_FAST                'flags'
              558  LOAD_FAST                'color_table_size'
              560  BINARY_OR        
              562  STORE_FAST               'flags'
            564_0  COME_FROM           544  '544'
            564_1  COME_FROM           522  '522'

 L. 603       564  LOAD_FAST                'fp'
              566  LOAD_METHOD              write

 L. 604       568  LOAD_CONST               b','

 L. 605       570  LOAD_GLOBAL              o16
              572  LOAD_FAST                'offset'
              574  LOAD_CONST               0
              576  BINARY_SUBSCR    
              578  CALL_FUNCTION_1       1  ''

 L. 604       580  BINARY_ADD       

 L. 606       582  LOAD_GLOBAL              o16
              584  LOAD_FAST                'offset'
              586  LOAD_CONST               1
              588  BINARY_SUBSCR    
              590  CALL_FUNCTION_1       1  ''

 L. 604       592  BINARY_ADD       

 L. 607       594  LOAD_GLOBAL              o16
              596  LOAD_FAST                'im'
              598  LOAD_ATTR                size
              600  LOAD_CONST               0
              602  BINARY_SUBSCR    
              604  CALL_FUNCTION_1       1  ''

 L. 604       606  BINARY_ADD       

 L. 608       608  LOAD_GLOBAL              o16
              610  LOAD_FAST                'im'
              612  LOAD_ATTR                size
              614  LOAD_CONST               1
              616  BINARY_SUBSCR    
              618  CALL_FUNCTION_1       1  ''

 L. 604       620  BINARY_ADD       

 L. 609       622  LOAD_GLOBAL              o8
              624  LOAD_FAST                'flags'
              626  CALL_FUNCTION_1       1  ''

 L. 604       628  BINARY_ADD       

 L. 603       630  CALL_METHOD_1         1  ''
              632  POP_TOP          

 L. 611       634  LOAD_FAST                'include_color_table'
          636_638  POP_JUMP_IF_FALSE   660  'to 660'
              640  LOAD_FAST                'color_table_size'
          642_644  POP_JUMP_IF_FALSE   660  'to 660'

 L. 612       646  LOAD_FAST                'fp'
              648  LOAD_METHOD              write
              650  LOAD_GLOBAL              _get_header_palette
              652  LOAD_FAST                'palette_bytes'
              654  CALL_FUNCTION_1       1  ''
              656  CALL_METHOD_1         1  ''
              658  POP_TOP          
            660_0  COME_FROM           642  '642'
            660_1  COME_FROM           636  '636'

 L. 613       660  LOAD_FAST                'fp'
              662  LOAD_METHOD              write
              664  LOAD_GLOBAL              o8
              666  LOAD_CONST               8
              668  CALL_FUNCTION_1       1  ''
              670  CALL_METHOD_1         1  ''
              672  POP_TOP          

Parse error at or near `<121>' instruction at offset 24


def _save_netpbm--- This code section failed: ---

 L. 624         0  LOAD_FAST                'im'
                2  LOAD_METHOD              _dump
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tempfile'

 L. 626         8  SETUP_FINALLY       240  'to 240'

 L. 627        10  LOAD_GLOBAL              open
               12  LOAD_FAST                'filename'
               14  LOAD_STR                 'wb'
               16  CALL_FUNCTION_2       2  ''
               18  SETUP_WITH          186  'to 186'
               20  STORE_FAST               'f'

 L. 628        22  LOAD_FAST                'im'
               24  LOAD_ATTR                mode
               26  LOAD_STR                 'RGB'
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 629        32  LOAD_GLOBAL              subprocess
               34  LOAD_ATTR                check_call

 L. 630        36  LOAD_STR                 'ppmtogif'
               38  LOAD_FAST                'tempfile'
               40  BUILD_LIST_2          2 
               42  LOAD_FAST                'f'
               44  LOAD_GLOBAL              subprocess
               46  LOAD_ATTR                DEVNULL

 L. 629        48  LOAD_CONST               ('stdout', 'stderr')
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  POP_TOP          
               54  JUMP_FORWARD        172  'to 172'
             56_0  COME_FROM            30  '30'

 L. 635        56  LOAD_STR                 'ppmquant'
               58  LOAD_STR                 '256'
               60  LOAD_FAST                'tempfile'
               62  BUILD_LIST_3          3 
               64  STORE_FAST               'quant_cmd'

 L. 636        66  LOAD_STR                 'ppmtogif'
               68  BUILD_LIST_1          1 
               70  STORE_FAST               'togif_cmd'

 L. 637        72  LOAD_GLOBAL              subprocess
               74  LOAD_ATTR                Popen

 L. 638        76  LOAD_FAST                'quant_cmd'
               78  LOAD_GLOBAL              subprocess
               80  LOAD_ATTR                PIPE
               82  LOAD_GLOBAL              subprocess
               84  LOAD_ATTR                DEVNULL

 L. 637        86  LOAD_CONST               ('stdout', 'stderr')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  STORE_FAST               'quant_proc'

 L. 640        92  LOAD_GLOBAL              subprocess
               94  LOAD_ATTR                Popen

 L. 641        96  LOAD_FAST                'togif_cmd'

 L. 642        98  LOAD_FAST                'quant_proc'
              100  LOAD_ATTR                stdout

 L. 643       102  LOAD_FAST                'f'

 L. 644       104  LOAD_GLOBAL              subprocess
              106  LOAD_ATTR                DEVNULL

 L. 640       108  LOAD_CONST               ('stdin', 'stdout', 'stderr')
              110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              112  STORE_FAST               'togif_proc'

 L. 648       114  LOAD_FAST                'quant_proc'
              116  LOAD_ATTR                stdout
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 650       124  LOAD_FAST                'quant_proc'
              126  LOAD_METHOD              wait
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'retcode'

 L. 651       132  LOAD_FAST                'retcode'
              134  POP_JUMP_IF_FALSE   148  'to 148'

 L. 652       136  LOAD_GLOBAL              subprocess
              138  LOAD_METHOD              CalledProcessError
              140  LOAD_FAST                'retcode'
              142  LOAD_FAST                'quant_cmd'
              144  CALL_METHOD_2         2  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           134  '134'

 L. 654       148  LOAD_FAST                'togif_proc'
              150  LOAD_METHOD              wait
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'retcode'

 L. 655       156  LOAD_FAST                'retcode'
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L. 656       160  LOAD_GLOBAL              subprocess
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

 L. 658       204  SETUP_FINALLY       220  'to 220'

 L. 659       206  LOAD_GLOBAL              os
              208  LOAD_METHOD              unlink
              210  LOAD_FAST                'tempfile'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  POP_BLOCK        
              218  JUMP_FORWARD        238  'to 238'
            220_0  COME_FROM_FINALLY   204  '204'

 L. 660       220  DUP_TOP          
              222  LOAD_GLOBAL              OSError
              224  <121>               236  ''
              226  POP_TOP          
              228  POP_TOP          
              230  POP_TOP          

 L. 661       232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
              236  <48>             
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           218  '218'
              238  JUMP_FORWARD        278  'to 278'
            240_0  COME_FROM_FINALLY     8  '8'

 L. 658       240  SETUP_FINALLY       256  'to 256'

 L. 659       242  LOAD_GLOBAL              os
              244  LOAD_METHOD              unlink
              246  LOAD_FAST                'tempfile'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
              252  POP_BLOCK        
              254  JUMP_FORWARD        276  'to 276'
            256_0  COME_FROM_FINALLY   240  '240'

 L. 660       256  DUP_TOP          
              258  LOAD_GLOBAL              OSError
          260_262  <121>               274  ''
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L. 661       270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
              274  <48>             
            276_0  COME_FROM           272  '272'
            276_1  COME_FROM           254  '254'
              276  <48>             
            278_0  COME_FROM           238  '238'

Parse error at or near `DUP_TOP' instruction at offset 176


_FORCE_OPTIMIZE = False

def _get_optimize--- This code section failed: ---

 L. 680         0  LOAD_FAST                'im'
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

 L. 691        26  LOAD_GLOBAL              _FORCE_OPTIMIZE
               28  JUMP_IF_TRUE_OR_POP    38  'to 38'
               30  LOAD_FAST                'im'
               32  LOAD_ATTR                mode
               34  LOAD_STR                 'L'
               36  COMPARE_OP               ==
             38_0  COME_FROM            28  '28'
               38  STORE_FAST               'optimise'

 L. 692        40  LOAD_FAST                'optimise'
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

 L. 694        60  BUILD_LIST_0          0 
               62  STORE_FAST               'used_palette_colors'

 L. 695        64  LOAD_GLOBAL              enumerate
               66  LOAD_FAST                'im'
               68  LOAD_METHOD              histogram
               70  CALL_METHOD_0         0  ''
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
             76_0  COME_FROM            86  '86'
               76  FOR_ITER            100  'to 100'
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'i'
               82  STORE_FAST               'count'

 L. 696        84  LOAD_FAST                'count'
               86  POP_JUMP_IF_FALSE    76  'to 76'

 L. 697        88  LOAD_FAST                'used_palette_colors'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'i'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            76  'to 76'

 L. 699       100  LOAD_FAST                'optimise'
              102  POP_JUMP_IF_TRUE    132  'to 132'

 L. 700       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'used_palette_colors'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_CONST               128
              112  COMPARE_OP               <=

 L. 699       114  POP_JUMP_IF_FALSE   136  'to 136'

 L. 701       116  LOAD_GLOBAL              max
              118  LOAD_FAST                'used_palette_colors'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'used_palette_colors'
              126  CALL_FUNCTION_1       1  ''
              128  COMPARE_OP               >

 L. 699       130  POP_JUMP_IF_FALSE   136  'to 136'
            132_0  COME_FROM           102  '102'

 L. 703       132  LOAD_FAST                'used_palette_colors'
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
              8_0  COME_FROM            42  '42'
              8_1  COME_FROM            22  '22'
              8_2  COME_FROM            14  '14'
                8  FOR_ITER             94  'to 94'
               10  STORE_FAST               'extensionKey'

 L. 764        12  LOAD_FAST                'info'
               14  POP_JUMP_IF_FALSE     8  'to 8'
               16  LOAD_FAST                'extensionKey'
               18  LOAD_FAST                'info'
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE     8  'to 8'

 L. 765        24  LOAD_FAST                'extensionKey'
               26  LOAD_STR                 'duration'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  LOAD_FAST                'info'
               34  LOAD_FAST                'extensionKey'
               36  BINARY_SUBSCR    
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE      8  'to 8'
             44_0  COME_FROM            30  '30'

 L. 766        44  LOAD_FAST                'extensionKey'
               46  LOAD_STR                 'comment'
               48  COMPARE_OP               ==

 L. 765        50  POP_JUMP_IF_FALSE    84  'to 84'

 L. 766        52  LOAD_CONST               1
               54  LOAD_GLOBAL              len
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

Parse error at or near `<118>' instruction at offset 20


def _write_frame_data--- This code section failed: ---

 L. 796         0  SETUP_FINALLY        76  'to 76'

 L. 797         2  LOAD_FAST                'params'
                4  LOAD_FAST                'im_frame'
                6  STORE_ATTR               encoderinfo

 L. 800         8  LOAD_GLOBAL              _write_local_header
               10  LOAD_FAST                'fp'
               12  LOAD_FAST                'im_frame'
               14  LOAD_FAST                'offset'
               16  LOAD_CONST               0
               18  CALL_FUNCTION_4       4  ''
               20  POP_TOP          

 L. 802        22  LOAD_GLOBAL              ImageFile
               24  LOAD_METHOD              _save

 L. 803        26  LOAD_FAST                'im_frame'
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

 L. 802        54  CALL_METHOD_3         3  ''
               56  POP_TOP          

 L. 806        58  LOAD_FAST                'fp'
               60  LOAD_METHOD              write
               62  LOAD_CONST               b'\x00'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        

 L. 808        70  LOAD_FAST                'im_frame'
               72  DELETE_ATTR              encoderinfo
               74  JUMP_FORWARD         82  'to 82'
             76_0  COME_FROM_FINALLY     0  '0'
               76  LOAD_FAST                'im_frame'
               78  DELETE_ATTR              encoderinfo
               80  <48>             
             82_0  COME_FROM            74  '74'

Parse error at or near `LOAD_FAST' instruction at offset 70


def getheader--- This code section failed: ---

 L. 827         0  LOAD_GLOBAL              _get_optimize
                2  LOAD_FAST                'im'
                4  LOAD_FAST                'info'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'used_palette_colors'

 L. 829        10  LOAD_FAST                'info'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 830        18  BUILD_MAP_0           0 
               20  STORE_FAST               'info'
             22_0  COME_FROM            16  '16'

 L. 832        22  LOAD_STR                 'background'
               24  LOAD_FAST                'info'
               26  <118>                 1  ''
               28  POP_JUMP_IF_FALSE    54  'to 54'
               30  LOAD_STR                 'background'
               32  LOAD_FAST                'im'
               34  LOAD_ATTR                info
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L. 833        40  LOAD_FAST                'im'
               42  LOAD_ATTR                info
               44  LOAD_STR                 'background'
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'info'
               50  LOAD_STR                 'background'
               52  STORE_SUBSCR     
             54_0  COME_FROM            38  '38'
             54_1  COME_FROM            28  '28'

 L. 835        54  LOAD_GLOBAL              _normalize_palette
               56  LOAD_FAST                'im'
               58  LOAD_FAST                'palette'
               60  LOAD_FAST                'info'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'im_mod'

 L. 836        66  LOAD_FAST                'im_mod'
               68  LOAD_ATTR                palette
               70  LOAD_FAST                'im'
               72  STORE_ATTR               palette

 L. 837        74  LOAD_FAST                'im_mod'
               76  LOAD_ATTR                im
               78  LOAD_FAST                'im'
               80  STORE_ATTR               im

 L. 838        82  LOAD_GLOBAL              _get_global_header
               84  LOAD_FAST                'im'
               86  LOAD_FAST                'info'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'header'

 L. 840        92  LOAD_FAST                'header'
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