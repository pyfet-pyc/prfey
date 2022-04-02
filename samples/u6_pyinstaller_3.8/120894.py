# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\PpmImagePlugin.py
from . import Image, ImageFile
b_whitespace = b' \t\n\x0b\x0c\r'
MODES = {b'P4':'1', 
 b'P5':'L', 
 b'P6':'RGB', 
 b'P0CMYK':'CMYK', 
 b'PyP':'P', 
 b'PyRGBA':'RGBA', 
 b'PyCMYK':'CMYK'}

def _accept(prefix):
    return prefix[0:1] == b'P' and prefix[1] in b'0456y'


class PpmImageFile(ImageFile.ImageFile):
    format = 'PPM'
    format_description = 'Pbmplus image'

    def _token--- This code section failed: ---
              0_0  COME_FROM            60  '60'

 L.  54         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               1
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'c'

 L.  55        12  LOAD_FAST                'c'
               14  POP_JUMP_IF_FALSE    72  'to 72'
               16  LOAD_FAST                'c'
               18  LOAD_GLOBAL              b_whitespace
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE    26  'to 26'

 L.  56        24  BREAK_LOOP           72  'to 72'
             26_0  COME_FROM            22  '22'

 L.  57        26  LOAD_FAST                'c'
               28  LOAD_CONST               b'y'
               30  COMPARE_OP               >
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  58        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 'Expected ASCII value, found binary'
               38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'

 L.  59        42  LOAD_FAST                's'
               44  LOAD_FAST                'c'
               46  BINARY_ADD       
               48  STORE_FAST               's'

 L.  60        50  LOAD_GLOBAL              len
               52  LOAD_FAST                's'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               9
               58  COMPARE_OP               >
               60  POP_JUMP_IF_FALSE     0  'to 0'

 L.  61        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'Expected int, got > 9 digits'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  JUMP_BACK             0  'to 0'
             72_0  COME_FROM            14  '14'

 L.  62        72  LOAD_FAST                's'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 74

    def _open--- This code section failed: ---

 L.  67         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               1
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  68        12  LOAD_FAST                's'
               14  LOAD_CONST               b'P'
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.  69        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a PPM file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  70        28  LOAD_FAST                'self'
               30  LOAD_METHOD              _token
               32  LOAD_FAST                's'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'magic_number'

 L.  71        38  LOAD_GLOBAL              MODES
               40  LOAD_FAST                'magic_number'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'mode'

 L.  74        46  LOAD_STR                 'image/x-portable-bitmap'

 L.  75        48  LOAD_STR                 'image/x-portable-graymap'

 L.  76        50  LOAD_STR                 'image/x-portable-pixmap'

 L.  73        52  LOAD_CONST               (b'P4', b'P5', b'P6')
               54  BUILD_CONST_KEY_MAP_3     3 
               56  LOAD_METHOD              get

 L.  77        58  LOAD_FAST                'magic_number'

 L.  73        60  CALL_METHOD_1         1  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               custom_mimetype

 L.  79        66  LOAD_FAST                'mode'
               68  LOAD_STR                 '1'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.  80        74  LOAD_STR                 '1'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               mode

 L.  81        80  LOAD_STR                 '1;I'
               82  STORE_FAST               'rawmode'
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM            72  '72'

 L.  83        86  LOAD_FAST                'mode'
               88  DUP_TOP          
               90  LOAD_FAST                'self'
               92  STORE_ATTR               mode
               94  STORE_FAST               'rawmode'
             96_0  COME_FROM            84  '84'

 L.  85        96  LOAD_GLOBAL              range
               98  LOAD_CONST               3
              100  CALL_FUNCTION_1       1  ''
              102  GET_ITER         
            104_0  COME_FROM           240  '240'
            104_1  COME_FROM           232  '232'
              104  FOR_ITER            300  'to 300'
              106  STORE_FAST               'ix'
            108_0  COME_FROM           136  '136'

 L.  88       108  LOAD_FAST                'self'
              110  LOAD_ATTR                fp
              112  LOAD_METHOD              read
              114  LOAD_CONST               1
              116  CALL_METHOD_1         1  ''
              118  STORE_FAST               's'

 L.  89       120  LOAD_FAST                's'
              122  LOAD_GLOBAL              b_whitespace
              124  COMPARE_OP               not-in
              126  POP_JUMP_IF_FALSE   130  'to 130'

 L.  90       128  JUMP_ABSOLUTE       148  'to 148'
            130_0  COME_FROM           126  '126'

 L.  91       130  LOAD_FAST                's'
              132  LOAD_CONST               b''
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   108  'to 108'

 L.  92       138  LOAD_GLOBAL              ValueError
              140  LOAD_STR                 'File does not extend beyond magic number'
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
              146  JUMP_BACK           108  'to 108'

 L.  93       148  LOAD_FAST                's'
              150  LOAD_CONST               b'#'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_FALSE   158  'to 158'

 L.  94       156  BREAK_LOOP          170  'to 170'
            158_0  COME_FROM           154  '154'

 L.  95       158  LOAD_FAST                'self'
              160  LOAD_ATTR                fp
              162  LOAD_METHOD              readline
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               's'
              168  JUMP_BACK           108  'to 108'

 L.  96       170  LOAD_GLOBAL              int
              172  LOAD_FAST                'self'
              174  LOAD_METHOD              _token
              176  LOAD_FAST                's'
              178  CALL_METHOD_1         1  ''
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               's'

 L.  97       184  LOAD_FAST                'ix'
              186  LOAD_CONST               0
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L.  98       192  LOAD_FAST                's'
              194  STORE_FAST               'xsize'
              196  JUMP_BACK           104  'to 104'
            198_0  COME_FROM           190  '190'

 L.  99       198  LOAD_FAST                'ix'
              200  LOAD_CONST               1
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   226  'to 226'

 L. 100       206  LOAD_FAST                's'
              208  STORE_FAST               'ysize'

 L. 101       210  LOAD_FAST                'mode'
              212  LOAD_STR                 '1'
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   224  'to 224'

 L. 102       218  POP_TOP          
          220_222  BREAK_LOOP          300  'to 300'
            224_0  COME_FROM           216  '216'
              224  JUMP_BACK           104  'to 104'
            226_0  COME_FROM           204  '204'

 L. 103       226  LOAD_FAST                'ix'
              228  LOAD_CONST               2
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   104  'to 104'

 L. 105       234  LOAD_FAST                's'
              236  LOAD_CONST               255
              238  COMPARE_OP               >
              240  POP_JUMP_IF_FALSE   104  'to 104'

 L. 106       242  LOAD_FAST                'mode'
              244  LOAD_STR                 'L'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_TRUE    266  'to 266'

 L. 107       252  LOAD_GLOBAL              ValueError
              254  LOAD_STR                 'Too many colors for band: '
              256  LOAD_FAST                's'
              258  FORMAT_VALUE          0  ''
              260  BUILD_STRING_2        2 
              262  CALL_FUNCTION_1       1  ''
              264  RAISE_VARARGS_1       1  'exception instance'
            266_0  COME_FROM           248  '248'

 L. 108       266  LOAD_FAST                's'
              268  LOAD_CONST               65536
              270  COMPARE_OP               <
          272_274  POP_JUMP_IF_FALSE   288  'to 288'

 L. 109       276  LOAD_STR                 'I'
              278  LOAD_FAST                'self'
              280  STORE_ATTR               mode

 L. 110       282  LOAD_STR                 'I;16B'
              284  STORE_FAST               'rawmode'
              286  JUMP_BACK           104  'to 104'
            288_0  COME_FROM           272  '272'

 L. 112       288  LOAD_STR                 'I'
              290  LOAD_FAST                'self'
              292  STORE_ATTR               mode

 L. 113       294  LOAD_STR                 'I;32B'
              296  STORE_FAST               'rawmode'
              298  JUMP_BACK           104  'to 104'

 L. 115       300  LOAD_FAST                'xsize'
              302  LOAD_FAST                'ysize'
              304  BUILD_TUPLE_2         2 
              306  LOAD_FAST                'self'
              308  STORE_ATTR               _size

 L. 116       310  LOAD_STR                 'raw'
              312  LOAD_CONST               0
              314  LOAD_CONST               0
              316  LOAD_FAST                'xsize'
              318  LOAD_FAST                'ysize'
              320  BUILD_TUPLE_4         4 
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                fp
              326  LOAD_METHOD              tell
              328  CALL_METHOD_0         0  ''
              330  LOAD_FAST                'rawmode'
              332  LOAD_CONST               0
              334  LOAD_CONST               1
              336  BUILD_TUPLE_3         3 
              338  BUILD_TUPLE_4         4 
              340  BUILD_LIST_1          1 
              342  LOAD_FAST                'self'
              344  STORE_ATTR               tile

Parse error at or near `COME_FROM' instruction at offset 130_0


def _save(im, fp, filename):
    if im.mode == '1':
        rawmode, head = ('1;I', b'P4')
    else:
        if im.mode == 'L':
            rawmode, head = ('L', b'P5')
        else:
            if im.mode == 'I':
                if im.getextrema[1] < 65536:
                    rawmode, head = ('I;16B', b'P5')
                else:
                    rawmode, head = ('I;32B', b'P5')
            elif im.mode == 'RGB':
                rawmode, head = ('RGB', b'P6')
            else:
                if im.mode == 'RGBA':
                    rawmode, head = ('RGB', b'P6')
                else:
                    raise OSError(f"cannot write mode {im.mode} as PPM")
    fp.write(head + ('\n%d %d\n' % im.size).encode'ascii')
    if head == b'P6':
        fp.writeb'255\n'
    elif head == b'P5':
        if rawmode == 'L':
            fp.writeb'255\n'
        else:
            if rawmode == 'I;16B':
                fp.writeb'65535\n'
            else:
                if rawmode == 'I;32B':
                    fp.writeb'2147483648\n'
    ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, 1))])


Image.register_open(PpmImageFile.format, PpmImageFile, _accept)
Image.register_save(PpmImageFile.format, _save)
Image.register_extensions(PpmImageFile.format, ['.pbm', '.pgm', '.ppm', '.pnm'])
Image.register_mime(PpmImageFile.format, 'image/x-portable-anymap')