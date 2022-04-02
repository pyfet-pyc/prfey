# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\GbrImagePlugin.py
from . import Image, ImageFile
from ._binary import i32be as i32

def _accept--- This code section failed: ---

 L.  32         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'prefix'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               8
                8  COMPARE_OP               >=
               10  JUMP_IF_FALSE_OR_POP    38  'to 38'
               12  LOAD_GLOBAL              i32
               14  LOAD_FAST                'prefix'
               16  LOAD_CONST               0
               18  CALL_FUNCTION_2       2  ''
               20  LOAD_CONST               20
               22  COMPARE_OP               >=
               24  JUMP_IF_FALSE_OR_POP    38  'to 38'
               26  LOAD_GLOBAL              i32
               28  LOAD_FAST                'prefix'
               30  LOAD_CONST               4
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_CONST               (1, 2)
               36  <118>                 0  ''
             38_0  COME_FROM            24  '24'
             38_1  COME_FROM            10  '10'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class GbrImageFile(ImageFile.ImageFile):
    format = 'GBR'
    format_description = 'GIMP brush file'

    def _open--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              i32
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               4
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'header_size'

 L.  46        16  LOAD_GLOBAL              i32
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  LOAD_METHOD              read
               24  LOAD_CONST               4
               26  CALL_METHOD_1         1  ''
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'version'

 L.  47        32  LOAD_FAST                'header_size'
               34  LOAD_CONST               20
               36  COMPARE_OP               <
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  48        40  LOAD_GLOBAL              SyntaxError
               42  LOAD_STR                 'not a GIMP brush'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  49        48  LOAD_FAST                'version'
               50  LOAD_CONST               (1, 2)
               52  <118>                 1  ''
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L.  50        56  LOAD_GLOBAL              SyntaxError
               58  LOAD_STR                 'Unsupported GIMP brush version: '
               60  LOAD_FAST                'version'
               62  FORMAT_VALUE          0  ''
               64  BUILD_STRING_2        2 
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            54  '54'

 L.  52        70  LOAD_GLOBAL              i32
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                fp
               76  LOAD_METHOD              read
               78  LOAD_CONST               4
               80  CALL_METHOD_1         1  ''
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'width'

 L.  53        86  LOAD_GLOBAL              i32
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                fp
               92  LOAD_METHOD              read
               94  LOAD_CONST               4
               96  CALL_METHOD_1         1  ''
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'height'

 L.  54       102  LOAD_GLOBAL              i32
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                fp
              108  LOAD_METHOD              read
              110  LOAD_CONST               4
              112  CALL_METHOD_1         1  ''
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'color_depth'

 L.  55       118  LOAD_FAST                'width'
              120  LOAD_CONST               0
              122  COMPARE_OP               <=
              124  POP_JUMP_IF_TRUE    134  'to 134'
              126  LOAD_FAST                'height'
              128  LOAD_CONST               0
              130  COMPARE_OP               <=
              132  POP_JUMP_IF_FALSE   142  'to 142'
            134_0  COME_FROM           124  '124'

 L.  56       134  LOAD_GLOBAL              SyntaxError
              136  LOAD_STR                 'not a GIMP brush'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           132  '132'

 L.  57       142  LOAD_FAST                'color_depth'
              144  LOAD_CONST               (1, 4)
              146  <118>                 1  ''
              148  POP_JUMP_IF_FALSE   164  'to 164'

 L.  58       150  LOAD_GLOBAL              SyntaxError
              152  LOAD_STR                 'Unsupported GIMP brush color depth: '
              154  LOAD_FAST                'color_depth'
              156  FORMAT_VALUE          0  ''
              158  BUILD_STRING_2        2 
              160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           148  '148'

 L.  60       164  LOAD_FAST                'version'
              166  LOAD_CONST               1
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L.  61       172  LOAD_FAST                'header_size'
              174  LOAD_CONST               20
              176  BINARY_SUBTRACT  
              178  STORE_FAST               'comment_length'
              180  JUMP_FORWARD        240  'to 240'
            182_0  COME_FROM           170  '170'

 L.  63       182  LOAD_FAST                'header_size'
              184  LOAD_CONST               28
              186  BINARY_SUBTRACT  
              188  STORE_FAST               'comment_length'

 L.  64       190  LOAD_FAST                'self'
              192  LOAD_ATTR                fp
              194  LOAD_METHOD              read
              196  LOAD_CONST               4
              198  CALL_METHOD_1         1  ''
              200  STORE_FAST               'magic_number'

 L.  65       202  LOAD_FAST                'magic_number'
              204  LOAD_CONST               b'GIMP'
              206  COMPARE_OP               !=
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L.  66       210  LOAD_GLOBAL              SyntaxError
              212  LOAD_STR                 'not a GIMP brush, bad magic number'
              214  CALL_FUNCTION_1       1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           208  '208'

 L.  67       218  LOAD_GLOBAL              i32
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                fp
              224  LOAD_METHOD              read
              226  LOAD_CONST               4
              228  CALL_METHOD_1         1  ''
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                info
              236  LOAD_STR                 'spacing'
              238  STORE_SUBSCR     
            240_0  COME_FROM           180  '180'

 L.  69       240  LOAD_FAST                'self'
              242  LOAD_ATTR                fp
              244  LOAD_METHOD              read
              246  LOAD_FAST                'comment_length'
              248  CALL_METHOD_1         1  ''
              250  LOAD_CONST               None
              252  LOAD_CONST               -1
              254  BUILD_SLICE_2         2 
              256  BINARY_SUBSCR    
              258  STORE_FAST               'comment'

 L.  71       260  LOAD_FAST                'color_depth'
              262  LOAD_CONST               1
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   278  'to 278'

 L.  72       270  LOAD_STR                 'L'
              272  LOAD_FAST                'self'
              274  STORE_ATTR               mode
              276  JUMP_FORWARD        284  'to 284'
            278_0  COME_FROM           266  '266'

 L.  74       278  LOAD_STR                 'RGBA'
              280  LOAD_FAST                'self'
              282  STORE_ATTR               mode
            284_0  COME_FROM           276  '276'

 L.  76       284  LOAD_FAST                'width'
              286  LOAD_FAST                'height'
              288  BUILD_TUPLE_2         2 
              290  LOAD_FAST                'self'
              292  STORE_ATTR               _size

 L.  78       294  LOAD_FAST                'comment'
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                info
              300  LOAD_STR                 'comment'
              302  STORE_SUBSCR     

 L.  81       304  LOAD_GLOBAL              Image
              306  LOAD_METHOD              _decompression_bomb_check
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                size
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          

 L.  84       316  LOAD_FAST                'width'
              318  LOAD_FAST                'height'
              320  BINARY_MULTIPLY  
              322  LOAD_FAST                'color_depth'
              324  BINARY_MULTIPLY  
              326  LOAD_FAST                'self'
              328  STORE_ATTR               _data_size

Parse error at or near `<118>' instruction at offset 52

    def load(self):
        if self.im:
            return
        self.im = Image.core.new(self.mode, self.size)
        self.frombytesself.fp.readself._data_size


Image.register_open(GbrImageFile.format, GbrImageFile, _accept)
Image.register_extension(GbrImageFile.format, '.gbr')