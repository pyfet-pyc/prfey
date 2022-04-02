# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\XVThumbImagePlugin.py
from . import Image, ImageFile, ImagePalette
from ._binary import i8, o8
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
             34_0  COME_FROM            74  '74'
             34_1  COME_FROM            70  '70'

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

 L.  62        56  LOAD_GLOBAL              i8
               58  LOAD_FAST                's'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               35
               68  COMPARE_OP               !=
               70  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L.  63        72  JUMP_FORWARD         76  'to 76'
               74  JUMP_BACK            34  'to 34'
             76_0  COME_FROM            72  '72'

 L.  66        76  LOAD_FAST                's'
               78  LOAD_METHOD              strip
               80  CALL_METHOD_0         0  ''
               82  LOAD_METHOD              split
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               's'

 L.  68        88  LOAD_STR                 'P'
               90  LOAD_FAST                'self'
               92  STORE_ATTR               mode

 L.  69        94  LOAD_GLOBAL              int
               96  LOAD_FAST                's'
               98  LOAD_CONST               0
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_GLOBAL              int
              106  LOAD_FAST                's'
              108  LOAD_CONST               1
              110  BINARY_SUBSCR    
              112  CALL_FUNCTION_1       1  ''
              114  BUILD_TUPLE_2         2 
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _size

 L.  71       120  LOAD_GLOBAL              ImagePalette
              122  LOAD_METHOD              raw
              124  LOAD_STR                 'RGB'
              126  LOAD_GLOBAL              PALETTE
              128  CALL_METHOD_2         2  ''
              130  LOAD_FAST                'self'
              132  STORE_ATTR               palette

 L.  73       134  LOAD_STR                 'raw'
              136  LOAD_CONST               (0, 0)
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                size
              142  BINARY_ADD       
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                fp
              148  LOAD_METHOD              tell
              150  CALL_METHOD_0         0  ''
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                mode
              156  LOAD_CONST               0
              158  LOAD_CONST               1
              160  BUILD_TUPLE_3         3 
              162  BUILD_TUPLE_4         4 
              164  BUILD_LIST_1          1 
              166  LOAD_FAST                'self'
              168  STORE_ATTR               tile

Parse error at or near `JUMP_BACK' instruction at offset 74


    Image.register_open(XVThumbImageFile.format, XVThumbImageFile, _accept)