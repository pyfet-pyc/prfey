# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\FliImagePlugin.py
from . import Image, ImageFile, ImagePalette
from ._binary import i16le as i16
from ._binary import i32le as i32
from ._binary import o8

def _accept--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'prefix'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               6
                8  COMPARE_OP               >=
               10  JUMP_IF_FALSE_OR_POP    24  'to 24'
               12  LOAD_GLOBAL              i16
               14  LOAD_FAST                'prefix'
               16  LOAD_CONST               4
               18  CALL_FUNCTION_2       2  ''
               20  LOAD_CONST               (44817, 44818)
               22  <118>                 0  ''
             24_0  COME_FROM            10  '10'
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class FliImageFile(ImageFile.ImageFile):
    format = 'FLI'
    format_description = 'Autodesk FLI/FLC Animation'
    _close_exclusive_fp_after_loading = False

    def _open--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               128
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  48        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''

 L.  47        18  POP_JUMP_IF_FALSE    50  'to 50'

 L.  49        20  LOAD_GLOBAL              i16
               22  LOAD_FAST                's'
               24  LOAD_CONST               14
               26  CALL_FUNCTION_2       2  ''
               28  LOAD_CONST               (0, 3)
               30  <118>                 0  ''

 L.  47        32  POP_JUMP_IF_FALSE    50  'to 50'

 L.  50        34  LOAD_FAST                's'
               36  LOAD_CONST               20
               38  LOAD_CONST               22
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_CONST               b'\x00\x00'
               46  COMPARE_OP               ==

 L.  47        48  POP_JUMP_IF_TRUE     58  'to 58'
             50_0  COME_FROM            32  '32'
             50_1  COME_FROM            18  '18'

 L.  52        50  LOAD_GLOBAL              SyntaxError
               52  LOAD_STR                 'not an FLI/FLC file'
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            48  '48'

 L.  55        58  LOAD_GLOBAL              i16
               60  LOAD_FAST                's'
               62  LOAD_CONST               6
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_FAST                'self'
               68  STORE_ATTR               n_frames

 L.  56        70  LOAD_FAST                'self'
               72  LOAD_ATTR                n_frames
               74  LOAD_CONST               1
               76  COMPARE_OP               >
               78  LOAD_FAST                'self'
               80  STORE_ATTR               is_animated

 L.  59        82  LOAD_STR                 'P'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               mode

 L.  60        88  LOAD_GLOBAL              i16
               90  LOAD_FAST                's'
               92  LOAD_CONST               8
               94  CALL_FUNCTION_2       2  ''
               96  LOAD_GLOBAL              i16
               98  LOAD_FAST                's'
              100  LOAD_CONST               10
              102  CALL_FUNCTION_2       2  ''
              104  BUILD_TUPLE_2         2 
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _size

 L.  63       110  LOAD_GLOBAL              i32
              112  LOAD_FAST                's'
              114  LOAD_CONST               16
              116  CALL_FUNCTION_2       2  ''
              118  STORE_FAST               'duration'

 L.  64       120  LOAD_GLOBAL              i16
              122  LOAD_FAST                's'
              124  LOAD_CONST               4
              126  CALL_FUNCTION_2       2  ''
              128  STORE_FAST               'magic'

 L.  65       130  LOAD_FAST                'magic'
              132  LOAD_CONST               44817
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   150  'to 150'

 L.  66       138  LOAD_FAST                'duration'
              140  LOAD_CONST               1000
              142  BINARY_MULTIPLY  
              144  LOAD_CONST               70
              146  BINARY_FLOOR_DIVIDE
              148  STORE_FAST               'duration'
            150_0  COME_FROM           136  '136'

 L.  67       150  LOAD_FAST                'duration'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                info
              156  LOAD_STR                 'duration'
              158  STORE_SUBSCR     

 L.  70       160  LOAD_LISTCOMP            '<code_object <listcomp>>'
              162  LOAD_STR                 'FliImageFile._open.<locals>.<listcomp>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_GLOBAL              range
              168  LOAD_CONST               256
              170  CALL_FUNCTION_1       1  ''
              172  GET_ITER         
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'palette'

 L.  72       178  LOAD_FAST                'self'
              180  LOAD_ATTR                fp
              182  LOAD_METHOD              read
              184  LOAD_CONST               16
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               's'

 L.  74       190  LOAD_CONST               128
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _FliImageFile__offset

 L.  76       196  LOAD_GLOBAL              i16
              198  LOAD_FAST                's'
              200  LOAD_CONST               4
              202  CALL_FUNCTION_2       2  ''
              204  LOAD_CONST               61696
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   238  'to 238'

 L.  78       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _FliImageFile__offset
              214  LOAD_GLOBAL              i32
              216  LOAD_FAST                's'
              218  CALL_FUNCTION_1       1  ''
              220  BINARY_ADD       
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _FliImageFile__offset

 L.  79       226  LOAD_FAST                'self'
              228  LOAD_ATTR                fp
              230  LOAD_METHOD              read
              232  LOAD_CONST               16
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               's'
            238_0  COME_FROM           208  '208'

 L.  81       238  LOAD_GLOBAL              i16
              240  LOAD_FAST                's'
              242  LOAD_CONST               4
              244  CALL_FUNCTION_2       2  ''
              246  LOAD_CONST               61946
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   324  'to 324'

 L.  83       254  LOAD_FAST                'self'
              256  LOAD_ATTR                fp
              258  LOAD_METHOD              read
              260  LOAD_CONST               6
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               's'

 L.  84       266  LOAD_GLOBAL              i16
              268  LOAD_FAST                's'
              270  LOAD_CONST               4
              272  CALL_FUNCTION_2       2  ''
              274  LOAD_CONST               11
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   296  'to 296'

 L.  85       282  LOAD_FAST                'self'
              284  LOAD_METHOD              _palette
              286  LOAD_FAST                'palette'
              288  LOAD_CONST               2
              290  CALL_METHOD_2         2  ''
              292  POP_TOP          
              294  JUMP_FORWARD        324  'to 324'
            296_0  COME_FROM           278  '278'

 L.  86       296  LOAD_GLOBAL              i16
              298  LOAD_FAST                's'
              300  LOAD_CONST               4
              302  CALL_FUNCTION_2       2  ''
              304  LOAD_CONST               4
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   324  'to 324'

 L.  87       312  LOAD_FAST                'self'
              314  LOAD_METHOD              _palette
              316  LOAD_FAST                'palette'
              318  LOAD_CONST               0
              320  CALL_METHOD_2         2  ''
              322  POP_TOP          
            324_0  COME_FROM           308  '308'
            324_1  COME_FROM           294  '294'
            324_2  COME_FROM           250  '250'

 L.  89       324  LOAD_LISTCOMP            '<code_object <listcomp>>'
              326  LOAD_STR                 'FliImageFile._open.<locals>.<listcomp>'
              328  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              330  LOAD_FAST                'palette'
              332  GET_ITER         
              334  CALL_FUNCTION_1       1  ''
              336  STORE_FAST               'palette'

 L.  90       338  LOAD_GLOBAL              ImagePalette
              340  LOAD_METHOD              raw
              342  LOAD_STR                 'RGB'
              344  LOAD_CONST               b''
              346  LOAD_METHOD              join
              348  LOAD_FAST                'palette'
              350  CALL_METHOD_1         1  ''
              352  CALL_METHOD_2         2  ''
              354  LOAD_FAST                'self'
              356  STORE_ATTR               palette

 L.  93       358  LOAD_CONST               -1
              360  LOAD_FAST                'self'
              362  STORE_ATTR               _FliImageFile__frame

 L.  94       364  LOAD_FAST                'self'
              366  LOAD_ATTR                fp
              368  LOAD_FAST                'self'
              370  STORE_ATTR               _FliImageFile__fp

 L.  95       372  LOAD_FAST                'self'
              374  LOAD_ATTR                fp
              376  LOAD_METHOD              tell
              378  CALL_METHOD_0         0  ''
              380  LOAD_FAST                'self'
              382  STORE_ATTR               _FliImageFile__rewind

 L.  96       384  LOAD_FAST                'self'
              386  LOAD_METHOD              seek
              388  LOAD_CONST               0
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

Parse error at or near `<118>' instruction at offset 30

    def _palette(self, palette, shift):
        i = 0
        for e in range(i16(self.fp.read2)):
            s = self.fp.read2
            i = i + s[0]
            n = s[1]
            if n == 0:
                n = 256
            s = self.fp.read(n * 3)
            for n in range(0, len(s), 3):
                r = s[n] << shift
                g = s[(n + 1)] << shift
                b = s[(n + 2)] << shift
                palette[i] = (r, g, b)
                i += 1

    def seek(self, frame):
        if not self._seek_checkframe:
            return
        if frame < self._FliImageFile__frame:
            self._seek0
        for f in range(self._FliImageFile__frame + 1)(frame + 1):
            self._seekf

    def _seek(self, frame):
        if frame == 0:
            self._FliImageFile__frame = -1
            self._FliImageFile__fp.seekself._FliImageFile__rewind
            self._FliImageFile__offset = 128
        else:
            self.load
        if frame != self._FliImageFile__frame + 1:
            raise ValueError(f"cannot seek to frame {frame}")
        self._FliImageFile__frame = frame
        self.fp = self._FliImageFile__fp
        self.fp.seekself._FliImageFile__offset
        s = self.fp.read4
        if not s:
            raise EOFError
        framesize = i32(s)
        self.decodermaxblock = framesize
        self.tile = [('fli', (0, 0) + self.size, self._FliImageFile__offset, None)]
        self._FliImageFile__offset += framesize

    def tell(self):
        return self._FliImageFile__frame

    def _close__fp--- This code section failed: ---

 L. 157         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 158         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _FliImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 159        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _FliImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 160        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 161        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 163        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _FliImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _FliImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


Image.register_open(FliImageFile.format, FliImageFile, _accept)
Image.register_extensions(FliImageFile.format, ['.fli', '.flc'])