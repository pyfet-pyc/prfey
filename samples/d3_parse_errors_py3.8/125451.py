# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\XpmImagePlugin.py
import re
from . import Image, ImageFile, ImagePalette
from ._binary import i8, o8
xpm_head = re.compile(b'"([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*)')

def _accept(prefix):
    return prefix[:9] == b'/* XPM */'


class XpmImageFile(ImageFile.ImageFile):
    format = 'XPM'
    format_description = 'X11 Pixel Map'

    def _open--- This code section failed: ---

 L.  42         0  LOAD_GLOBAL              _accept
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               9
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L.  43        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not an XPM file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            62  '62'
             24_1  COME_FROM            58  '58'
             24_2  COME_FROM            14  '14'

 L.  47        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              readline
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               's'

 L.  48        34  LOAD_FAST                's'
               36  POP_JUMP_IF_TRUE     46  'to 46'

 L.  49        38  LOAD_GLOBAL              SyntaxError
               40  LOAD_STR                 'broken XPM file'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L.  50        46  LOAD_GLOBAL              xpm_head
               48  LOAD_METHOD              match
               50  LOAD_FAST                's'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'm'

 L.  51        56  LOAD_FAST                'm'
               58  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L.  52        60  JUMP_FORWARD         64  'to 64'
               62  JUMP_BACK            24  'to 24'
             64_0  COME_FROM            60  '60'

 L.  54        64  LOAD_GLOBAL              int
               66  LOAD_FAST                'm'
               68  LOAD_METHOD              group
               70  LOAD_CONST               1
               72  CALL_METHOD_1         1  ''
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_GLOBAL              int
               78  LOAD_FAST                'm'
               80  LOAD_METHOD              group
               82  LOAD_CONST               2
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  BUILD_TUPLE_2         2 
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _size

 L.  56        94  LOAD_GLOBAL              int
               96  LOAD_FAST                'm'
               98  LOAD_METHOD              group
              100  LOAD_CONST               3
              102  CALL_METHOD_1         1  ''
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'pal'

 L.  57       108  LOAD_GLOBAL              int
              110  LOAD_FAST                'm'
              112  LOAD_METHOD              group
              114  LOAD_CONST               4
              116  CALL_METHOD_1         1  ''
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'bpp'

 L.  59       122  LOAD_FAST                'pal'
              124  LOAD_CONST               256
              126  COMPARE_OP               >
              128  POP_JUMP_IF_TRUE    138  'to 138'
              130  LOAD_FAST                'bpp'
              132  LOAD_CONST               1
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_FALSE   146  'to 146'
            138_0  COME_FROM           128  '128'

 L.  60       138  LOAD_GLOBAL              ValueError
              140  LOAD_STR                 'cannot read this XPM file'
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           136  '136'

 L.  65       146  LOAD_CONST               b'\x00\x00\x00'
              148  BUILD_LIST_1          1 
              150  LOAD_CONST               256
              152  BINARY_MULTIPLY  
              154  STORE_FAST               'palette'

 L.  67       156  LOAD_GLOBAL              range
              158  LOAD_FAST                'pal'
              160  CALL_FUNCTION_1       1  ''
              162  GET_ITER         
            164_0  COME_FROM           444  '444'
            164_1  COME_FROM           430  '430'
          164_166  FOR_ITER            446  'to 446'
              168  STORE_FAST               'i'

 L.  69       170  LOAD_FAST                'self'
              172  LOAD_ATTR                fp
              174  LOAD_METHOD              readline
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               's'

 L.  70       180  LOAD_FAST                's'
              182  LOAD_CONST               -2
              184  LOAD_CONST               None
              186  BUILD_SLICE_2         2 
              188  BINARY_SUBSCR    
              190  LOAD_CONST               b'\r\n'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L.  71       196  LOAD_FAST                's'
              198  LOAD_CONST               None
              200  LOAD_CONST               -2
              202  BUILD_SLICE_2         2 
              204  BINARY_SUBSCR    
              206  STORE_FAST               's'
              208  JUMP_FORWARD        238  'to 238'
            210_0  COME_FROM           194  '194'

 L.  72       210  LOAD_FAST                's'
              212  LOAD_CONST               -1
              214  LOAD_CONST               None
              216  BUILD_SLICE_2         2 
              218  BINARY_SUBSCR    
              220  LOAD_CONST               b'\r\n'
              222  COMPARE_OP               in
              224  POP_JUMP_IF_FALSE   238  'to 238'

 L.  73       226  LOAD_FAST                's'
              228  LOAD_CONST               None
              230  LOAD_CONST               -1
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  STORE_FAST               's'
            238_0  COME_FROM           224  '224'
            238_1  COME_FROM           208  '208'

 L.  75       238  LOAD_GLOBAL              i8
              240  LOAD_FAST                's'
              242  LOAD_CONST               1
              244  BINARY_SUBSCR    
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'c'

 L.  76       250  LOAD_FAST                's'
              252  LOAD_CONST               2
              254  LOAD_CONST               -2
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  LOAD_METHOD              split
              262  CALL_METHOD_0         0  ''
              264  STORE_FAST               's'

 L.  78       266  LOAD_GLOBAL              range
              268  LOAD_CONST               0
              270  LOAD_GLOBAL              len
              272  LOAD_FAST                's'
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_CONST               2
              278  CALL_FUNCTION_3       3  ''
              280  GET_ITER         
            282_0  COME_FROM           432  '432'
            282_1  COME_FROM           296  '296'
              282  FOR_ITER            436  'to 436'
              284  STORE_FAST               'i'

 L.  80       286  LOAD_FAST                's'
              288  LOAD_FAST                'i'
              290  BINARY_SUBSCR    
              292  LOAD_CONST               b'c'
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE_BACK   282  'to 282'

 L.  83       300  LOAD_FAST                's'
              302  LOAD_FAST                'i'
              304  LOAD_CONST               1
              306  BINARY_ADD       
              308  BINARY_SUBSCR    
              310  STORE_FAST               'rgb'

 L.  84       312  LOAD_FAST                'rgb'
              314  LOAD_CONST               b'None'
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   334  'to 334'

 L.  85       322  LOAD_FAST                'c'
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                info
              328  LOAD_STR                 'transparency'
              330  STORE_SUBSCR     
              332  JUMP_FORWARD        428  'to 428'
            334_0  COME_FROM           318  '318'

 L.  86       334  LOAD_FAST                'rgb'
              336  LOAD_CONST               0
              338  LOAD_CONST               1
              340  BUILD_SLICE_2         2 
              342  BINARY_SUBSCR    
              344  LOAD_CONST               b'#'
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   420  'to 420'

 L.  88       352  LOAD_GLOBAL              int
              354  LOAD_FAST                'rgb'
              356  LOAD_CONST               1
              358  LOAD_CONST               None
              360  BUILD_SLICE_2         2 
              362  BINARY_SUBSCR    
              364  LOAD_CONST               16
              366  CALL_FUNCTION_2       2  ''
              368  STORE_FAST               'rgb'

 L.  90       370  LOAD_GLOBAL              o8
              372  LOAD_FAST                'rgb'
              374  LOAD_CONST               16
              376  BINARY_RSHIFT    
              378  LOAD_CONST               255
              380  BINARY_AND       
              382  CALL_FUNCTION_1       1  ''
              384  LOAD_GLOBAL              o8
              386  LOAD_FAST                'rgb'
              388  LOAD_CONST               8
              390  BINARY_RSHIFT    
              392  LOAD_CONST               255
              394  BINARY_AND       
              396  CALL_FUNCTION_1       1  ''
              398  BINARY_ADD       
              400  LOAD_GLOBAL              o8
              402  LOAD_FAST                'rgb'
              404  LOAD_CONST               255
              406  BINARY_AND       
              408  CALL_FUNCTION_1       1  ''
              410  BINARY_ADD       

 L.  89       412  LOAD_FAST                'palette'
              414  LOAD_FAST                'c'
              416  STORE_SUBSCR     
              418  JUMP_FORWARD        428  'to 428'
            420_0  COME_FROM           348  '348'

 L.  94       420  LOAD_GLOBAL              ValueError
              422  LOAD_STR                 'cannot read this XPM file'
              424  CALL_FUNCTION_1       1  ''
              426  RAISE_VARARGS_1       1  'exception instance'
            428_0  COME_FROM           418  '418'
            428_1  COME_FROM           332  '332'

 L.  95       428  POP_TOP          
              430  BREAK_LOOP          164  'to 164'
          432_434  JUMP_BACK           282  'to 282'
            436_0  COME_FROM           282  '282'

 L. 100       436  LOAD_GLOBAL              ValueError
              438  LOAD_STR                 'cannot read this XPM file'
              440  CALL_FUNCTION_1       1  ''
              442  RAISE_VARARGS_1       1  'exception instance'
              444  JUMP_BACK           164  'to 164'
            446_0  COME_FROM           164  '164'

 L. 102       446  LOAD_STR                 'P'
              448  LOAD_FAST                'self'
              450  STORE_ATTR               mode

 L. 103       452  LOAD_GLOBAL              ImagePalette
              454  LOAD_METHOD              raw
              456  LOAD_STR                 'RGB'
              458  LOAD_CONST               b''
              460  LOAD_METHOD              join
              462  LOAD_FAST                'palette'
              464  CALL_METHOD_1         1  ''
              466  CALL_METHOD_2         2  ''
              468  LOAD_FAST                'self'
              470  STORE_ATTR               palette

 L. 105       472  LOAD_STR                 'raw'
              474  LOAD_CONST               (0, 0)
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                size
              480  BINARY_ADD       
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                fp
              486  LOAD_METHOD              tell
              488  CALL_METHOD_0         0  ''
              490  LOAD_CONST               ('P', 0, 1)
              492  BUILD_TUPLE_4         4 
              494  BUILD_LIST_1          1 
              496  LOAD_FAST                'self'
              498  STORE_ATTR               tile

Parse error at or near `JUMP_BACK' instruction at offset 62

    def load_read(self, bytes):
        xsize, ysize = self.size
        s = [
         None] * ysize
        for i in range(ysize):
            s[i] = self.fp.readline[1:xsize + 1].ljust(xsize)
        else:
            return (b'').join(s)


Image.register_open(XpmImageFile.format, XpmImageFile, _accept)
Image.register_extension(XpmImageFile.format, '.xpm')
Image.register_mime(XpmImageFile.format, 'image/xpm')