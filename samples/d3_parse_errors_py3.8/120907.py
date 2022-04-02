# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\XVThumbImagePlugin.py
from . import Image, ImageFile, ImagePalette
from ._binary import o8
_MAGIC = b'P7 332'
PALETTE = b''
for r in range(8):
    for g in range(8):
        for b in range(4):
            PALETTE = PALETTE + (o8(r * 255 // 7) + o8(g * 255 // 7) + o8(b * 255 // 3))

else:

    def _accept(prefix):
        return prefix[:6] == _MAGIC


    class XVThumbImageFile(ImageFile.ImageFile):
        format = 'XVThumb'
        format_description = 'XV thumbnail image'

        def _open--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              _accept
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               6
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L.  52        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not an XV thumbnail file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L.  55        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              readline
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          
             34_0  COME_FROM            70  '70'
             34_1  COME_FROM            66  '66'

 L.  59        34  LOAD_FAST                'self'
               36  LOAD_ATTR                fp
               38  LOAD_METHOD              readline
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               's'

 L.  60        44  LOAD_FAST                's'
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L.  61        48  LOAD_GLOBAL              SyntaxError
               50  LOAD_STR                 'Unexpected EOF reading XV thumbnail file'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L.  62        56  LOAD_FAST                's'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_CONST               35
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L.  63        68  JUMP_FORWARD         72  'to 72'
               70  JUMP_BACK            34  'to 34'
             72_0  COME_FROM            68  '68'

 L.  66        72  LOAD_FAST                's'
               74  LOAD_METHOD              strip
               76  CALL_METHOD_0         0  ''
               78  LOAD_METHOD              split
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               's'

 L.  68        84  LOAD_STR                 'P'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               mode

 L.  69        90  LOAD_GLOBAL              int
               92  LOAD_FAST                's'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_GLOBAL              int
              102  LOAD_FAST                's'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  CALL_FUNCTION_1       1  ''
              110  BUILD_TUPLE_2         2 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _size

 L.  71       116  LOAD_GLOBAL              ImagePalette
              118  LOAD_METHOD              raw
              120  LOAD_STR                 'RGB'
              122  LOAD_GLOBAL              PALETTE
              124  CALL_METHOD_2         2  ''
              126  LOAD_FAST                'self'
              128  STORE_ATTR               palette

 L.  73       130  LOAD_STR                 'raw'
              132  LOAD_CONST               (0, 0)
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                size
              138  BINARY_ADD       
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                fp
              144  LOAD_METHOD              tell
              146  CALL_METHOD_0         0  ''
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                mode
              152  LOAD_CONST               0
              154  LOAD_CONST               1
              156  BUILD_TUPLE_3         3 
              158  BUILD_TUPLE_4         4 
              160  BUILD_LIST_1          1 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               tile

Parse error at or near `JUMP_BACK' instruction at offset 70


    Image.register_open(XVThumbImageFile.format, XVThumbImageFile, _accept)