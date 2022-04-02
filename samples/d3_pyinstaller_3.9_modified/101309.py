# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\MpoImagePlugin.py
from . import Image, ImageFile, JpegImagePlugin
from ._binary import i16be as i16

def _accept(prefix):
    return JpegImagePlugin._accept(prefix)


def _save(im, fp, filename):
    return JpegImagePlugin._save(im, fp, filename)


class MpoImageFile(JpegImagePlugin.JpegImageFile):
    format = 'MPO'
    format_description = 'MPO (CIPA DC-007)'
    _close_exclusive_fp_after_loading = False

    def _open(self):
        self.fp.seek(0)
        JpegImagePlugin.JpegImageFile._open(self)
        self._after_jpeg_open()

    def _after_jpeg_open--- This code section failed: ---

 L.  50         0  LOAD_FAST                'mpheader'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_FAST                'mpheader'
               10  JUMP_FORWARD         18  'to 18'
             12_0  COME_FROM             6  '6'
               12  LOAD_DEREF               'self'
               14  LOAD_METHOD              _getmp
               16  CALL_METHOD_0         0  ''
             18_0  COME_FROM            10  '10'
               18  LOAD_DEREF               'self'
               20  STORE_ATTR               mpinfo

 L.  51        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                mpinfo
               26  LOAD_CONST               45057
               28  BINARY_SUBSCR    
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               n_frames

 L.  52        34  LOAD_CLOSURE             'self'
               36  BUILD_TUPLE_1         1 
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'MpoImageFile._after_jpeg_open.<locals>.<listcomp>'
               42  MAKE_FUNCTION_8          'closure'

 L.  53        44  LOAD_DEREF               'self'
               46  LOAD_ATTR                mpinfo
               48  LOAD_CONST               45058
               50  BINARY_SUBSCR    

 L.  52        52  GET_ITER         
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_DEREF               'self'
               58  STORE_ATTR               _MpoImageFile__mpoffsets

 L.  55        60  LOAD_CONST               0
               62  LOAD_DEREF               'self'
               64  LOAD_ATTR                _MpoImageFile__mpoffsets
               66  LOAD_CONST               0
               68  STORE_SUBSCR     

 L.  58        70  LOAD_DEREF               'self'
               72  LOAD_ATTR                n_frames
               74  LOAD_GLOBAL              len
               76  LOAD_DEREF               'self'
               78  LOAD_ATTR                _MpoImageFile__mpoffsets
               80  CALL_FUNCTION_1       1  ''
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_TRUE     90  'to 90'
               86  <74>             
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            84  '84'

 L.  59        90  LOAD_DEREF               'self'
               92  LOAD_ATTR                info
               94  LOAD_STR                 'mpoffset'
               96  DELETE_SUBSCR    

 L.  60        98  LOAD_DEREF               'self'
              100  LOAD_ATTR                n_frames
              102  LOAD_CONST               1
              104  COMPARE_OP               >
              106  LOAD_DEREF               'self'
              108  STORE_ATTR               is_animated

 L.  61       110  LOAD_DEREF               'self'
              112  LOAD_ATTR                fp
              114  LOAD_DEREF               'self'
              116  STORE_ATTR               _MpoImageFile__fp

 L.  62       118  LOAD_DEREF               'self'
              120  LOAD_ATTR                _MpoImageFile__fp
              122  LOAD_METHOD              seek
              124  LOAD_DEREF               'self'
              126  LOAD_ATTR                _MpoImageFile__mpoffsets
              128  LOAD_CONST               0
              130  BINARY_SUBSCR    
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L.  63       136  LOAD_CONST               0
              138  LOAD_DEREF               'self'
              140  STORE_ATTR               _MpoImageFile__frame

 L.  64       142  LOAD_CONST               0
              144  LOAD_DEREF               'self'
              146  STORE_ATTR               offset

 L.  66       148  LOAD_CONST               1
              150  LOAD_DEREF               'self'
              152  STORE_ATTR               readonly

Parse error at or near `None' instruction at offset -1

    def load_seek(self, pos):
        self._MpoImageFile__fp.seek(pos)

    def seek--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _seek_check
                4  LOAD_FAST                'frame'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.  73        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  74        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _MpoImageFile__fp
               18  LOAD_FAST                'self'
               20  STORE_ATTR               fp

 L.  75        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _MpoImageFile__mpoffsets
               26  LOAD_FAST                'frame'
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'self'
               32  STORE_ATTR               offset

 L.  77        34  LOAD_FAST                'self'
               36  LOAD_ATTR                fp
               38  LOAD_METHOD              seek
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                offset
               44  LOAD_CONST               2
               46  BINARY_ADD       
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L.  78        52  LOAD_FAST                'self'
               54  LOAD_ATTR                fp
               56  LOAD_METHOD              read
               58  LOAD_CONST               2
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'segment'

 L.  79        64  LOAD_FAST                'segment'
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L.  80        68  LOAD_GLOBAL              ValueError
               70  LOAD_STR                 'No data found for frame'
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L.  81        76  LOAD_GLOBAL              i16
               78  LOAD_FAST                'segment'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_CONST               65505
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   172  'to 172'

 L.  82        88  LOAD_GLOBAL              i16
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                fp
               94  LOAD_METHOD              read
               96  LOAD_CONST               2
               98  CALL_METHOD_1         1  ''
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_CONST               2
              104  BINARY_SUBTRACT  
              106  STORE_FAST               'n'

 L.  83       108  LOAD_GLOBAL              ImageFile
              110  LOAD_METHOD              _safe_read
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                fp
              116  LOAD_FAST                'n'
              118  CALL_METHOD_2         2  ''
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                info
              124  LOAD_STR                 'exif'
              126  STORE_SUBSCR     

 L.  85       128  LOAD_FAST                'self'
              130  LOAD_METHOD              getexif
              132  CALL_METHOD_0         0  ''
              134  STORE_FAST               'exif'

 L.  86       136  LOAD_CONST               40962
              138  LOAD_FAST                'exif'
              140  <118>                 0  ''
              142  POP_JUMP_IF_FALSE   190  'to 190'
              144  LOAD_CONST               40963
              146  LOAD_FAST                'exif'
              148  <118>                 0  ''
              150  POP_JUMP_IF_FALSE   190  'to 190'

 L.  87       152  LOAD_FAST                'exif'
              154  LOAD_CONST               40962
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'exif'
              160  LOAD_CONST               40963
              162  BINARY_SUBSCR    
              164  BUILD_TUPLE_2         2 
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _size
              170  JUMP_FORWARD        190  'to 190'
            172_0  COME_FROM            86  '86'

 L.  88       172  LOAD_STR                 'exif'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                info
              178  <118>                 0  ''
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L.  89       182  LOAD_FAST                'self'
              184  LOAD_ATTR                info
              186  LOAD_STR                 'exif'
              188  DELETE_SUBSCR    
            190_0  COME_FROM           180  '180'
            190_1  COME_FROM           170  '170'
            190_2  COME_FROM           150  '150'
            190_3  COME_FROM           142  '142'

 L.  91       190  LOAD_STR                 'jpeg'
              192  LOAD_CONST               (0, 0)
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                size
              198  BINARY_ADD       
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                offset
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                mode
              208  LOAD_STR                 ''
              210  BUILD_TUPLE_2         2 
              212  BUILD_TUPLE_4         4 
              214  BUILD_LIST_1          1 
              216  LOAD_FAST                'self'
              218  STORE_ATTR               tile

 L.  92       220  LOAD_FAST                'frame'
              222  LOAD_FAST                'self'
              224  STORE_ATTR               _MpoImageFile__frame

Parse error at or near `<118>' instruction at offset 140

    def tell(self):
        return self._MpoImageFile__frame

    def _close__fp--- This code section failed: ---

 L.  98         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L.  99         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _MpoImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 100        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _MpoImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 101        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 102        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 104        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _MpoImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _MpoImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34

    @staticmethod
    def adopt(jpeg_instance, mpheader=None):
        """
        Transform the instance of JpegImageFile into
        an instance of MpoImageFile.
        After the call, the JpegImageFile is extended
        to be an MpoImageFile.

        This is essentially useful when opening a JPEG
        file that reveals itself as an MPO, to avoid
        double call to _open.
        """
        jpeg_instance.__class__ = MpoImageFile
        jpeg_instance._after_jpeg_open(mpheader)
        return jpeg_instance


Image.register_save(MpoImageFile.format, _save)
Image.register_extension(MpoImageFile.format, '.mpo')
Image.register_mime(MpoImageFile.format, 'image/mpo')