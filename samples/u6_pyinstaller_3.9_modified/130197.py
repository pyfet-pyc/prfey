# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\MicImagePlugin.py
import olefile
from . import Image, TiffImagePlugin

def _accept(prefix):
    return prefix[:8] == olefile.MAGIC


class MicImageFile(TiffImagePlugin.TiffImageFile):
    format = 'MIC'
    format_description = 'Microsoft Image Composer'
    _close_exclusive_fp_after_loading = False

    def _open--- This code section failed: ---

 L.  47         0  SETUP_FINALLY        20  'to 20'

 L.  48         2  LOAD_GLOBAL              olefile
                4  LOAD_METHOD              OleFileIO
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fp
               10  CALL_METHOD_1         1  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               ole
               16  POP_BLOCK        
               18  JUMP_FORWARD         66  'to 66'
             20_0  COME_FROM_FINALLY     0  '0'

 L.  49        20  DUP_TOP          
               22  LOAD_GLOBAL              OSError
               24  <121>                64  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        56  'to 56'

 L.  50        34  LOAD_GLOBAL              SyntaxError
               36  LOAD_STR                 'not an MIC file; invalid OLE file'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_FAST                'e'
               42  RAISE_VARARGS_2       2  'exception instance with __cause__'
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'e'
               52  DELETE_FAST              'e'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM_FINALLY    32  '32'
               56  LOAD_CONST               None
               58  STORE_FAST               'e'
               60  DELETE_FAST              'e'
               62  <48>             
               64  <48>             
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            18  '18'

 L.  55        66  BUILD_LIST_0          0 
               68  LOAD_FAST                'self'
               70  STORE_ATTR               images

 L.  56        72  LOAD_FAST                'self'
               74  LOAD_ATTR                ole
               76  LOAD_METHOD              listdir
               78  CALL_METHOD_0         0  ''
               80  GET_ITER         
             82_0  COME_FROM           128  '128'
             82_1  COME_FROM           116  '116'
             82_2  COME_FROM            96  '96'
               82  FOR_ITER            144  'to 144'
               84  STORE_FAST               'path'

 L.  57        86  LOAD_FAST                'path'
               88  LOAD_CONST               1
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  POP_JUMP_IF_FALSE    82  'to 82'
               98  LOAD_FAST                'path'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  LOAD_CONST               -4
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  LOAD_STR                 '.ACI'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE    82  'to 82'
              118  LOAD_FAST                'path'
              120  LOAD_CONST               1
              122  BINARY_SUBSCR    
              124  LOAD_STR                 'Image'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE    82  'to 82'

 L.  58       130  LOAD_FAST                'self'
              132  LOAD_ATTR                images
              134  LOAD_METHOD              append
              136  LOAD_FAST                'path'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK            82  'to 82'

 L.  62       144  LOAD_FAST                'self'
              146  LOAD_ATTR                images
              148  POP_JUMP_IF_TRUE    158  'to 158'

 L.  63       150  LOAD_GLOBAL              SyntaxError
              152  LOAD_STR                 'not an MIC file; no image entries'
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           148  '148'

 L.  65       158  LOAD_FAST                'self'
              160  LOAD_ATTR                fp
              162  LOAD_FAST                'self'
              164  STORE_ATTR               _MicImageFile__fp

 L.  66       166  LOAD_CONST               None
              168  LOAD_FAST                'self'
              170  STORE_ATTR               frame

 L.  67       172  LOAD_GLOBAL              len
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                images
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_FAST                'self'
              182  STORE_ATTR               _n_frames

 L.  68       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _n_frames
              188  LOAD_CONST               1
              190  COMPARE_OP               >
              192  LOAD_FAST                'self'
              194  STORE_ATTR               is_animated

 L.  70       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                images
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_CONST               1
              206  COMPARE_OP               >
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L.  71       210  LOAD_GLOBAL              Image
              212  LOAD_ATTR                CONTAINER
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _category
            218_0  COME_FROM           208  '208'

 L.  73       218  LOAD_FAST                'self'
              220  LOAD_METHOD              seek
              222  LOAD_CONST               0
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          

Parse error at or near `<121>' instruction at offset 24

    def seek--- This code section failed: ---

 L.  76         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'frame'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.  77        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  78        14  SETUP_FINALLY        30  'to 30'

 L.  79        16  LOAD_FAST                'self'
               18  LOAD_ATTR                images
               20  LOAD_FAST                'frame'
               22  BINARY_SUBSCR    
               24  STORE_FAST               'filename'
               26  POP_BLOCK        
               28  JUMP_FORWARD         76  'to 76'
             30_0  COME_FROM_FINALLY    14  '14'

 L.  80        30  DUP_TOP          
               32  LOAD_GLOBAL              IndexError
               34  <121>                74  ''
               36  POP_TOP          
               38  STORE_FAST               'e'
               40  POP_TOP          
               42  SETUP_FINALLY        66  'to 66'

 L.  81        44  LOAD_GLOBAL              EOFError
               46  LOAD_STR                 'no such frame'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_FAST                'e'
               52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM_FINALLY    42  '42'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  <48>             
               74  <48>             
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            28  '28'

 L.  83        76  LOAD_FAST                'self'
               78  LOAD_ATTR                ole
               80  LOAD_METHOD              openstream
               82  LOAD_FAST                'filename'
               84  CALL_METHOD_1         1  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               fp

 L.  85        90  LOAD_GLOBAL              TiffImagePlugin
               92  LOAD_ATTR                TiffImageFile
               94  LOAD_METHOD              _open
               96  LOAD_FAST                'self'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L.  87       102  LOAD_FAST                'frame'
              104  LOAD_FAST                'self'
              106  STORE_ATTR               frame

Parse error at or near `<121>' instruction at offset 34

    def tell(self):
        return self.frame

    def _close__fp--- This code section failed: ---

 L.  93         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L.  94         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _MicImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  95        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _MicImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L.  96        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  97        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L.  99        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _MicImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _MicImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


Image.register_open(MicImageFile.format, MicImageFile, _accept)
Image.register_extension(MicImageFile.format, '.mic')