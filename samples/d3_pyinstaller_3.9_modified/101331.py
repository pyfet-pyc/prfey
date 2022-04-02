# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\XpmImagePlugin.py
import re
from . import Image, ImageFile, ImagePalette
from ._binary import o8
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
            164_0  COME_FROM           440  '440'
            164_1  COME_FROM           426  '426'
          164_166  FOR_ITER            442  'to 442'
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
              222  <118>                 0  ''
              224  POP_JUMP_IF_FALSE   238  'to 238'

 L.  73       226  LOAD_FAST                's'
              228  LOAD_CONST               None
              230  LOAD_CONST               -1
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  STORE_FAST               's'
            238_0  COME_FROM           224  '224'
            238_1  COME_FROM           208  '208'

 L.  75       238  LOAD_FAST                's'
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  STORE_FAST               'c'

 L.  76       246  LOAD_FAST                's'
              248  LOAD_CONST               2
              250  LOAD_CONST               -2
              252  BUILD_SLICE_2         2 
              254  BINARY_SUBSCR    
              256  LOAD_METHOD              split
              258  CALL_METHOD_0         0  ''
              260  STORE_FAST               's'

 L.  78       262  LOAD_GLOBAL              range
              264  LOAD_CONST               0
              266  LOAD_GLOBAL              len
              268  LOAD_FAST                's'
              270  CALL_FUNCTION_1       1  ''
              272  LOAD_CONST               2
              274  CALL_FUNCTION_3       3  ''
              276  GET_ITER         
            278_0  COME_FROM           428  '428'
            278_1  COME_FROM           292  '292'
              278  FOR_ITER            432  'to 432'
              280  STORE_FAST               'i'

 L.  80       282  LOAD_FAST                's'
              284  LOAD_FAST                'i'
              286  BINARY_SUBSCR    
              288  LOAD_CONST               b'c'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE_BACK   278  'to 278'

 L.  83       296  LOAD_FAST                's'
              298  LOAD_FAST                'i'
              300  LOAD_CONST               1
              302  BINARY_ADD       
              304  BINARY_SUBSCR    
              306  STORE_FAST               'rgb'

 L.  84       308  LOAD_FAST                'rgb'
              310  LOAD_CONST               b'None'
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   330  'to 330'

 L.  85       318  LOAD_FAST                'c'
              320  LOAD_FAST                'self'
              322  LOAD_ATTR                info
              324  LOAD_STR                 'transparency'
              326  STORE_SUBSCR     
              328  JUMP_FORWARD        424  'to 424'
            330_0  COME_FROM           314  '314'

 L.  86       330  LOAD_FAST                'rgb'
              332  LOAD_CONST               0
              334  LOAD_CONST               1
              336  BUILD_SLICE_2         2 
              338  BINARY_SUBSCR    
              340  LOAD_CONST               b'#'
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_FALSE   416  'to 416'

 L.  88       348  LOAD_GLOBAL              int
              350  LOAD_FAST                'rgb'
              352  LOAD_CONST               1
              354  LOAD_CONST               None
              356  BUILD_SLICE_2         2 
              358  BINARY_SUBSCR    
              360  LOAD_CONST               16
              362  CALL_FUNCTION_2       2  ''
              364  STORE_FAST               'rgb'

 L.  90       366  LOAD_GLOBAL              o8
              368  LOAD_FAST                'rgb'
              370  LOAD_CONST               16
              372  BINARY_RSHIFT    
              374  LOAD_CONST               255
              376  BINARY_AND       
              378  CALL_FUNCTION_1       1  ''
              380  LOAD_GLOBAL              o8
              382  LOAD_FAST                'rgb'
              384  LOAD_CONST               8
              386  BINARY_RSHIFT    
              388  LOAD_CONST               255
              390  BINARY_AND       
              392  CALL_FUNCTION_1       1  ''
              394  BINARY_ADD       
              396  LOAD_GLOBAL              o8
              398  LOAD_FAST                'rgb'
              400  LOAD_CONST               255
              402  BINARY_AND       
              404  CALL_FUNCTION_1       1  ''
              406  BINARY_ADD       

 L.  89       408  LOAD_FAST                'palette'
              410  LOAD_FAST                'c'
              412  STORE_SUBSCR     
              414  JUMP_FORWARD        424  'to 424'
            416_0  COME_FROM           344  '344'

 L.  94       416  LOAD_GLOBAL              ValueError
              418  LOAD_STR                 'cannot read this XPM file'
              420  CALL_FUNCTION_1       1  ''
              422  RAISE_VARARGS_1       1  'exception instance'
            424_0  COME_FROM           414  '414'
            424_1  COME_FROM           328  '328'

 L.  95       424  POP_TOP          
              426  BREAK_LOOP          164  'to 164'
          428_430  JUMP_BACK           278  'to 278'
            432_0  COME_FROM           278  '278'

 L. 100       432  LOAD_GLOBAL              ValueError
              434  LOAD_STR                 'cannot read this XPM file'
              436  CALL_FUNCTION_1       1  ''
              438  RAISE_VARARGS_1       1  'exception instance'
              440  JUMP_BACK           164  'to 164'
            442_0  COME_FROM           164  '164'

 L. 102       442  LOAD_STR                 'P'
              444  LOAD_FAST                'self'
              446  STORE_ATTR               mode

 L. 103       448  LOAD_GLOBAL              ImagePalette
              450  LOAD_METHOD              raw
              452  LOAD_STR                 'RGB'
              454  LOAD_CONST               b''
              456  LOAD_METHOD              join
              458  LOAD_FAST                'palette'
              460  CALL_METHOD_1         1  ''
              462  CALL_METHOD_2         2  ''
              464  LOAD_FAST                'self'
              466  STORE_ATTR               palette

 L. 105       468  LOAD_STR                 'raw'
              470  LOAD_CONST               (0, 0)
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                size
              476  BINARY_ADD       
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                fp
              482  LOAD_METHOD              tell
              484  CALL_METHOD_0         0  ''
              486  LOAD_CONST               ('P', 0, 1)
              488  BUILD_TUPLE_4         4 
              490  BUILD_LIST_1          1 
              492  LOAD_FAST                'self'
              494  STORE_ATTR               tile

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