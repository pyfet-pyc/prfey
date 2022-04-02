# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\FitsStubImagePlugin.py
from . import Image, ImageFile
_handler = None

def register_handler(handler):
    """
    Install application-specific FITS image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def _accept(prefix):
    return prefix[:6] == b'SIMPLE'


class FITSStubImageFile(ImageFile.StubImageFile):
    format = 'FITS'
    format_description = 'FITS'

    def _open--- This code section failed: ---

 L.  41         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              tell
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'offset'

 L.  43        10  BUILD_MAP_0           0 
               12  STORE_FAST               'headers'
             14_0  COME_FROM           142  '142'

 L.  45        14  LOAD_FAST                'self'
               16  LOAD_ATTR                fp
               18  LOAD_METHOD              read
               20  LOAD_CONST               80
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'header'

 L.  46        26  LOAD_FAST                'header'
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L.  47        30  LOAD_GLOBAL              OSError
               32  LOAD_STR                 'Truncated FITS file'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L.  48        38  LOAD_FAST                'header'
               40  LOAD_CONST               None
               42  LOAD_CONST               8
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  LOAD_METHOD              strip
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'keyword'

 L.  49        54  LOAD_FAST                'keyword'
               56  LOAD_CONST               b'END'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    64  'to 64'

 L.  50        62  JUMP_FORWARD        144  'to 144'
             64_0  COME_FROM            60  '60'

 L.  51        64  LOAD_FAST                'header'
               66  LOAD_CONST               8
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              strip
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'value'

 L.  52        80  LOAD_FAST                'value'
               82  LOAD_METHOD              startswith
               84  LOAD_CONST               b'='
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L.  53        90  LOAD_FAST                'value'
               92  LOAD_CONST               1
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_METHOD              strip
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'value'
            106_0  COME_FROM            88  '88'

 L.  54       106  LOAD_FAST                'headers'
              108  POP_JUMP_IF_TRUE    134  'to 134'
              110  LOAD_GLOBAL              _accept
              112  LOAD_FAST                'keyword'
              114  CALL_FUNCTION_1       1  ''
              116  POP_JUMP_IF_FALSE   126  'to 126'
              118  LOAD_FAST                'value'
              120  LOAD_CONST               b'T'
              122  COMPARE_OP               !=
              124  POP_JUMP_IF_FALSE   134  'to 134'
            126_0  COME_FROM           116  '116'

 L.  55       126  LOAD_GLOBAL              SyntaxError
              128  LOAD_STR                 'Not a FITS file'
              130  CALL_FUNCTION_1       1  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           124  '124'
            134_1  COME_FROM           108  '108'

 L.  56       134  LOAD_FAST                'value'
              136  LOAD_FAST                'headers'
              138  LOAD_FAST                'keyword'
              140  STORE_SUBSCR     
              142  JUMP_BACK            14  'to 14'
            144_0  COME_FROM            62  '62'

 L.  58       144  LOAD_GLOBAL              int
              146  LOAD_FAST                'headers'
              148  LOAD_CONST               b'NAXIS'
              150  BINARY_SUBSCR    
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'naxis'

 L.  59       156  LOAD_FAST                'naxis'
              158  LOAD_CONST               0
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   174  'to 174'

 L.  60       164  LOAD_GLOBAL              ValueError
              166  LOAD_STR                 'No image data'
              168  CALL_FUNCTION_1       1  ''
              170  RAISE_VARARGS_1       1  'exception instance'
              172  JUMP_FORWARD        228  'to 228'
            174_0  COME_FROM           162  '162'

 L.  61       174  LOAD_FAST                'naxis'
              176  LOAD_CONST               1
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   202  'to 202'

 L.  62       182  LOAD_CONST               1
              184  LOAD_GLOBAL              int
              186  LOAD_FAST                'headers'
              188  LOAD_CONST               b'NAXIS1'
              190  BINARY_SUBSCR    
              192  CALL_FUNCTION_1       1  ''
              194  BUILD_TUPLE_2         2 
              196  LOAD_FAST                'self'
              198  STORE_ATTR               _size
              200  JUMP_FORWARD        228  'to 228'
            202_0  COME_FROM           180  '180'

 L.  64       202  LOAD_GLOBAL              int
              204  LOAD_FAST                'headers'
              206  LOAD_CONST               b'NAXIS1'
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_GLOBAL              int
              214  LOAD_FAST                'headers'
              216  LOAD_CONST               b'NAXIS2'
              218  BINARY_SUBSCR    
              220  CALL_FUNCTION_1       1  ''
              222  BUILD_TUPLE_2         2 
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _size
            228_0  COME_FROM           200  '200'
            228_1  COME_FROM           172  '172'

 L.  66       228  LOAD_GLOBAL              int
              230  LOAD_FAST                'headers'
              232  LOAD_CONST               b'BITPIX'
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'number_of_bits'

 L.  67       240  LOAD_FAST                'number_of_bits'
              242  LOAD_CONST               8
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   258  'to 258'

 L.  68       250  LOAD_STR                 'L'
              252  LOAD_FAST                'self'
              254  STORE_ATTR               mode
              256  JUMP_FORWARD        310  'to 310'
            258_0  COME_FROM           246  '246'

 L.  69       258  LOAD_FAST                'number_of_bits'
              260  LOAD_CONST               16
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   276  'to 276'

 L.  70       268  LOAD_STR                 'I'
              270  LOAD_FAST                'self'
              272  STORE_ATTR               mode
              274  JUMP_FORWARD        310  'to 310'
            276_0  COME_FROM           264  '264'

 L.  72       276  LOAD_FAST                'number_of_bits'
              278  LOAD_CONST               32
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_FALSE   294  'to 294'

 L.  73       286  LOAD_STR                 'I'
              288  LOAD_FAST                'self'
              290  STORE_ATTR               mode
              292  JUMP_FORWARD        310  'to 310'
            294_0  COME_FROM           282  '282'

 L.  74       294  LOAD_FAST                'number_of_bits'
              296  LOAD_CONST               (-32, -64)
              298  <118>                 0  ''
          300_302  POP_JUMP_IF_FALSE   310  'to 310'

 L.  75       304  LOAD_STR                 'F'
              306  LOAD_FAST                'self'
              308  STORE_ATTR               mode
            310_0  COME_FROM           300  '300'
            310_1  COME_FROM           292  '292'
            310_2  COME_FROM           274  '274'
            310_3  COME_FROM           256  '256'

 L.  78       310  LOAD_FAST                'self'
              312  LOAD_ATTR                fp
              314  LOAD_METHOD              seek
              316  LOAD_FAST                'offset'
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L.  80       322  LOAD_FAST                'self'
              324  LOAD_METHOD              _load
              326  CALL_METHOD_0         0  ''
              328  STORE_FAST               'loader'

 L.  81       330  LOAD_FAST                'loader'
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L.  82       336  LOAD_FAST                'loader'
              338  LOAD_METHOD              open
              340  LOAD_FAST                'self'
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          
            346_0  COME_FROM           332  '332'

Parse error at or near `<118>' instruction at offset 298

    def _load(self):
        return _handler


def _save--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              _handler
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     18  'to 18'
                8  LOAD_GLOBAL              hasattr
               10  LOAD_STR                 '_handler'
               12  LOAD_STR                 'save'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'
             18_0  COME_FROM             6  '6'

 L.  90        18  LOAD_GLOBAL              OSError
               20  LOAD_STR                 'FITS save handler not installed'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.  91        26  LOAD_GLOBAL              _handler
               28  LOAD_METHOD              save
               30  LOAD_FAST                'im'
               32  LOAD_FAST                'fp'
               34  LOAD_FAST                'filename'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          

Parse error at or near `None' instruction at offset -1


Image.register_open(FITSStubImageFile.format, FITSStubImageFile, _accept)
Image.register_save(FITSStubImageFile.format, _save)
Image.register_extensions(FITSStubImageFile.format, ['.fit', '.fits'])