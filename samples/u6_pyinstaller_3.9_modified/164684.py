# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageTk.py
import tkinter
from io import BytesIO
from . import Image
_pilbitmap_ok = None

def _pilbitmap_check--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              _pilbitmap_ok
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    76  'to 76'

 L.  42         8  SETUP_FINALLY        52  'to 52'

 L.  43        10  LOAD_GLOBAL              Image
               12  LOAD_METHOD              new
               14  LOAD_STR                 '1'
               16  LOAD_CONST               (1, 1)
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'im'

 L.  44        22  LOAD_GLOBAL              tkinter
               24  LOAD_ATTR                BitmapImage
               26  LOAD_STR                 'PIL:'
               28  LOAD_FAST                'im'
               30  LOAD_ATTR                im
               32  LOAD_ATTR                id
               34  FORMAT_VALUE          0  ''
               36  BUILD_STRING_2        2 
               38  LOAD_CONST               ('data',)
               40  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               42  POP_TOP          

 L.  45        44  LOAD_CONST               1
               46  STORE_GLOBAL             _pilbitmap_ok
               48  POP_BLOCK        
               50  JUMP_FORWARD         76  'to 76'
             52_0  COME_FROM_FINALLY     8  '8'

 L.  46        52  DUP_TOP          
               54  LOAD_GLOBAL              tkinter
               56  LOAD_ATTR                TclError
               58  <121>                74  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  47        66  LOAD_CONST               0
               68  STORE_GLOBAL             _pilbitmap_ok
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            50  '50'
             76_2  COME_FROM             6  '6'

 L.  48        76  LOAD_GLOBAL              _pilbitmap_ok
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_image_from_kw--- This code section failed: ---

 L.  52         0  LOAD_CONST               None
                2  STORE_FAST               'source'

 L.  53         4  LOAD_STR                 'file'
                6  LOAD_FAST                'kw'
                8  <118>                 0  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L.  54        12  LOAD_FAST                'kw'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 'file'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'source'
               22  JUMP_FORWARD         46  'to 46'
             24_0  COME_FROM            10  '10'

 L.  55        24  LOAD_STR                 'data'
               26  LOAD_FAST                'kw'
               28  <118>                 0  ''
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L.  56        32  LOAD_GLOBAL              BytesIO
               34  LOAD_FAST                'kw'
               36  LOAD_METHOD              pop
               38  LOAD_STR                 'data'
               40  CALL_METHOD_1         1  ''
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'source'
             46_0  COME_FROM            30  '30'
             46_1  COME_FROM            22  '22'

 L.  57        46  LOAD_FAST                'source'
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L.  58        50  LOAD_GLOBAL              Image
               52  LOAD_METHOD              open
               54  LOAD_FAST                'source'
               56  CALL_METHOD_1         1  ''
               58  RETURN_VALUE     
             60_0  COME_FROM            48  '48'

Parse error at or near `<118>' instruction at offset 8


class PhotoImage:
    __doc__ = '\n    A Tkinter-compatible photo image.  This can be used\n    everywhere Tkinter expects an image object.  If the image is an RGBA\n    image, pixels having alpha 0 are treated as transparent.\n\n    The constructor takes either a PIL image, or a mode and a size.\n    Alternatively, you can use the ``file`` or ``data`` options to initialize\n    the photo image object.\n\n    :param image: Either a PIL image, or a mode string.  If a mode string is\n                  used, a size must also be given.\n    :param size: If the first argument is a mode string, this defines the size\n                 of the image.\n    :keyword file: A filename to load the image from (using\n                   ``Image.open(file)``).\n    :keyword data: An 8-bit string containing image data (as loaded from an\n                   image file).\n    '

    def __init__--- This code section failed: ---

 L.  88         0  LOAD_FAST                'image'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  89         8  LOAD_GLOBAL              _get_image_from_kw
               10  LOAD_FAST                'kw'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'image'
             16_0  COME_FROM             6  '6'

 L.  91        16  LOAD_GLOBAL              hasattr
               18  LOAD_FAST                'image'
               20  LOAD_STR                 'mode'
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE   118  'to 118'
               26  LOAD_GLOBAL              hasattr
               28  LOAD_FAST                'image'
               30  LOAD_STR                 'size'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE   118  'to 118'

 L.  93        36  LOAD_FAST                'image'
               38  LOAD_ATTR                mode
               40  STORE_FAST               'mode'

 L.  94        42  LOAD_FAST                'mode'
               44  LOAD_STR                 'P'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    94  'to 94'

 L.  96        50  LOAD_FAST                'image'
               52  LOAD_METHOD              load
               54  CALL_METHOD_0         0  ''
               56  POP_TOP          

 L.  97        58  SETUP_FINALLY        72  'to 72'

 L.  98        60  LOAD_FAST                'image'
               62  LOAD_ATTR                palette
               64  LOAD_ATTR                mode
               66  STORE_FAST               'mode'
               68  POP_BLOCK        
               70  JUMP_FORWARD         94  'to 94'
             72_0  COME_FROM_FINALLY    58  '58'

 L.  99        72  DUP_TOP          
               74  LOAD_GLOBAL              AttributeError
               76  <121>                92  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 100        84  LOAD_STR                 'RGB'
               86  STORE_FAST               'mode'
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            70  '70'
             94_2  COME_FROM            48  '48'

 L. 101        94  LOAD_FAST                'image'
               96  LOAD_ATTR                size
               98  STORE_FAST               'size'

 L. 102       100  LOAD_FAST                'size'
              102  UNPACK_SEQUENCE_2     2 
              104  LOAD_FAST                'kw'
              106  LOAD_STR                 'width'
              108  STORE_SUBSCR     
              110  LOAD_FAST                'kw'
              112  LOAD_STR                 'height'
              114  STORE_SUBSCR     
              116  JUMP_FORWARD        126  'to 126'
            118_0  COME_FROM            34  '34'
            118_1  COME_FROM            24  '24'

 L. 104       118  LOAD_FAST                'image'
              120  STORE_FAST               'mode'

 L. 105       122  LOAD_CONST               None
              124  STORE_FAST               'image'
            126_0  COME_FROM           116  '116'

 L. 107       126  LOAD_FAST                'mode'
              128  LOAD_CONST               ('1', 'L', 'RGB', 'RGBA')
              130  <118>                 1  ''
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L. 108       134  LOAD_GLOBAL              Image
              136  LOAD_METHOD              getmodebase
              138  LOAD_FAST                'mode'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'mode'
            144_0  COME_FROM           132  '132'

 L. 110       144  LOAD_FAST                'mode'
              146  LOAD_FAST                'self'
              148  STORE_ATTR               _PhotoImage__mode

 L. 111       150  LOAD_FAST                'size'
              152  LOAD_FAST                'self'
              154  STORE_ATTR               _PhotoImage__size

 L. 112       156  LOAD_GLOBAL              tkinter
              158  LOAD_ATTR                PhotoImage
              160  BUILD_TUPLE_0         0 
              162  BUILD_MAP_0           0 
              164  LOAD_FAST                'kw'
              166  <164>                 1  ''
              168  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              170  LOAD_FAST                'self'
              172  STORE_ATTR               _PhotoImage__photo

 L. 113       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _PhotoImage__photo
              178  LOAD_ATTR                tk
              180  LOAD_FAST                'self'
              182  STORE_ATTR               tk

 L. 114       184  LOAD_FAST                'image'
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 115       188  LOAD_FAST                'self'
              190  LOAD_METHOD              paste
              192  LOAD_FAST                'image'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           186  '186'

Parse error at or near `None' instruction at offset -1

    def __del__--- This code section failed: ---

 L. 118         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _PhotoImage__photo
                4  LOAD_ATTR                name
                6  STORE_FAST               'name'

 L. 119         8  LOAD_CONST               None
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _PhotoImage__photo
               14  STORE_ATTR               name

 L. 120        16  SETUP_FINALLY        40  'to 40'

 L. 121        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _PhotoImage__photo
               22  LOAD_ATTR                tk
               24  LOAD_METHOD              call
               26  LOAD_STR                 'image'
               28  LOAD_STR                 'delete'
               30  LOAD_FAST                'name'
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         58  'to 58'
             40_0  COME_FROM_FINALLY    16  '16'

 L. 122        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  <121>                56  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 123        52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            38  '38'

Parse error at or near `<121>' instruction at offset 44

    def __str__(self):
        """
        Get the Tkinter photo image identifier.  This method is automatically
        called by Tkinter whenever a PhotoImage object is passed to a Tkinter
        method.

        :return: A Tkinter photo image identifier (a string).
        """
        return str(self._PhotoImage__photo)

    def width(self):
        """
        Get the width of the image.

        :return: The width, in pixels.
        """
        return self._PhotoImage__size[0]

    def height(self):
        """
        Get the height of the image.

        :return: The height, in pixels.
        """
        return self._PhotoImage__size[1]

    def paste--- This code section failed: ---

 L. 165         0  LOAD_FAST                'im'
                2  LOAD_METHOD              load
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 166         8  LOAD_FAST                'im'
               10  LOAD_ATTR                im
               12  STORE_FAST               'image'

 L. 167        14  LOAD_FAST                'image'
               16  LOAD_METHOD              isblock
               18  CALL_METHOD_0         0  ''
               20  POP_JUMP_IF_FALSE    40  'to 40'
               22  LOAD_FAST                'im'
               24  LOAD_ATTR                mode
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _PhotoImage__mode
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 168        34  LOAD_FAST                'image'
               36  STORE_FAST               'block'
               38  JUMP_FORWARD         68  'to 68'
             40_0  COME_FROM            32  '32'
             40_1  COME_FROM            20  '20'

 L. 170        40  LOAD_FAST                'image'
               42  LOAD_METHOD              new_block
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _PhotoImage__mode
               48  LOAD_FAST                'im'
               50  LOAD_ATTR                size
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'block'

 L. 171        56  LOAD_FAST                'image'
               58  LOAD_METHOD              convert2
               60  LOAD_FAST                'block'
               62  LOAD_FAST                'image'
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
             68_0  COME_FROM            38  '38'

 L. 173        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _PhotoImage__photo
               72  LOAD_ATTR                tk
               74  STORE_FAST               'tk'

 L. 175        76  SETUP_FINALLY       100  'to 100'

 L. 176        78  LOAD_FAST                'tk'
               80  LOAD_METHOD              call
               82  LOAD_STR                 'PyImagingPhoto'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _PhotoImage__photo
               88  LOAD_FAST                'block'
               90  LOAD_ATTR                id
               92  CALL_METHOD_3         3  ''
               94  POP_TOP          
               96  POP_BLOCK        
               98  JUMP_FORWARD        300  'to 300'
            100_0  COME_FROM_FINALLY    76  '76'

 L. 177       100  DUP_TOP          
              102  LOAD_GLOBAL              tkinter
              104  LOAD_ATTR                TclError
          106_108  <121>               298  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 179       116  SETUP_FINALLY       264  'to 264'

 L. 180       118  LOAD_CONST               1
              120  LOAD_CONST               ('_imagingtk',)
              122  IMPORT_NAME              
              124  IMPORT_FROM              _imagingtk
              126  STORE_FAST               '_imagingtk'
              128  POP_TOP          

 L. 182       130  SETUP_FINALLY       208  'to 208'

 L. 183       132  LOAD_GLOBAL              hasattr
              134  LOAD_FAST                'tk'
              136  LOAD_STR                 'interp'
              138  CALL_FUNCTION_2       2  ''
              140  POP_JUMP_IF_FALSE   188  'to 188'

 L. 185       142  LOAD_CONST               0
              144  LOAD_CONST               ('FFI',)
              146  IMPORT_NAME              cffi
              148  IMPORT_FROM              FFI
              150  STORE_FAST               'FFI'
              152  POP_TOP          

 L. 187       154  LOAD_FAST                'FFI'
              156  CALL_FUNCTION_0       0  ''
              158  STORE_FAST               'ffi'

 L. 192       160  LOAD_FAST                '_imagingtk'
              162  LOAD_METHOD              tkinit
              164  LOAD_GLOBAL              int
              166  LOAD_FAST                'ffi'
              168  LOAD_METHOD              cast
              170  LOAD_STR                 'uintptr_t'
              172  LOAD_FAST                'tk'
              174  LOAD_ATTR                interp
              176  CALL_METHOD_2         2  ''
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_CONST               1
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          
              186  JUMP_FORWARD        204  'to 204'
            188_0  COME_FROM           140  '140'

 L. 194       188  LOAD_FAST                '_imagingtk'
              190  LOAD_METHOD              tkinit
              192  LOAD_FAST                'tk'
              194  LOAD_METHOD              interpaddr
              196  CALL_METHOD_0         0  ''
              198  LOAD_CONST               1
              200  CALL_METHOD_2         2  ''
              202  POP_TOP          
            204_0  COME_FROM           186  '186'
              204  POP_BLOCK        
              206  JUMP_FORWARD        242  'to 242'
            208_0  COME_FROM_FINALLY   130  '130'

 L. 195       208  DUP_TOP          
              210  LOAD_GLOBAL              AttributeError
              212  <121>               240  ''
              214  POP_TOP          
              216  POP_TOP          
              218  POP_TOP          

 L. 196       220  LOAD_FAST                '_imagingtk'
              222  LOAD_METHOD              tkinit
              224  LOAD_GLOBAL              id
              226  LOAD_FAST                'tk'
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_CONST               0
              232  CALL_METHOD_2         2  ''
              234  POP_TOP          
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
              240  <48>             
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           206  '206'

 L. 197       242  LOAD_FAST                'tk'
              244  LOAD_METHOD              call
              246  LOAD_STR                 'PyImagingPhoto'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                _PhotoImage__photo
              252  LOAD_FAST                'block'
              254  LOAD_ATTR                id
              256  CALL_METHOD_3         3  ''
              258  POP_TOP          
              260  POP_BLOCK        
              262  JUMP_FORWARD        294  'to 294'
            264_0  COME_FROM_FINALLY   116  '116'

 L. 198       264  DUP_TOP          
              266  LOAD_GLOBAL              ImportError
              268  LOAD_GLOBAL              AttributeError
              270  LOAD_GLOBAL              tkinter
              272  LOAD_ATTR                TclError
              274  BUILD_TUPLE_3         3 
          276_278  <121>               292  ''
              280  POP_TOP          
              282  POP_TOP          
              284  POP_TOP          

 L. 199       286  RAISE_VARARGS_0       0  'reraise'
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
              292  <48>             
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           262  '262'
              294  POP_EXCEPT       
              296  JUMP_FORWARD        300  'to 300'
              298  <48>             
            300_0  COME_FROM           296  '296'
            300_1  COME_FROM            98  '98'

Parse error at or near `<121>' instruction at offset 106_108


class BitmapImage:
    __doc__ = '\n    A Tkinter-compatible bitmap image.  This can be used everywhere Tkinter\n    expects an image object.\n\n    The given image must have mode "1".  Pixels having value 0 are treated as\n    transparent.  Options, if any, are passed on to Tkinter.  The most commonly\n    used option is ``foreground``, which is used to specify the color for the\n    non-transparent parts.  See the Tkinter documentation for information on\n    how to specify colours.\n\n    :param image: A PIL image.\n    '

    def __init__--- This code section failed: ---

 L. 223         0  LOAD_FAST                'image'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 224         8  LOAD_GLOBAL              _get_image_from_kw
               10  LOAD_FAST                'kw'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'image'
             16_0  COME_FROM             6  '6'

 L. 226        16  LOAD_FAST                'image'
               18  LOAD_ATTR                mode
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _BitmapImage__mode

 L. 227        24  LOAD_FAST                'image'
               26  LOAD_ATTR                size
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _BitmapImage__size

 L. 229        32  LOAD_GLOBAL              _pilbitmap_check
               34  CALL_FUNCTION_0       0  ''
               36  POP_JUMP_IF_FALSE    72  'to 72'

 L. 231        38  LOAD_FAST                'image'
               40  LOAD_METHOD              load
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 232        46  LOAD_STR                 'PIL:'
               48  LOAD_FAST                'image'
               50  LOAD_ATTR                im
               52  LOAD_ATTR                id
               54  FORMAT_VALUE          0  ''
               56  BUILD_STRING_2        2 
               58  LOAD_FAST                'kw'
               60  LOAD_STR                 'data'
               62  STORE_SUBSCR     

 L. 233        64  LOAD_FAST                'image'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _BitmapImage__im
               70  JUMP_FORWARD         84  'to 84'
             72_0  COME_FROM            36  '36'

 L. 236        72  LOAD_FAST                'image'
               74  LOAD_METHOD              tobitmap
               76  CALL_METHOD_0         0  ''
               78  LOAD_FAST                'kw'
               80  LOAD_STR                 'data'
               82  STORE_SUBSCR     
             84_0  COME_FROM            70  '70'

 L. 237        84  LOAD_GLOBAL              tkinter
               86  LOAD_ATTR                BitmapImage
               88  BUILD_TUPLE_0         0 
               90  BUILD_MAP_0           0 
               92  LOAD_FAST                'kw'
               94  <164>                 1  ''
               96  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _BitmapImage__photo

Parse error at or near `None' instruction at offset -1

    def __del__--- This code section failed: ---

 L. 240         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _BitmapImage__photo
                4  LOAD_ATTR                name
                6  STORE_FAST               'name'

 L. 241         8  LOAD_CONST               None
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _BitmapImage__photo
               14  STORE_ATTR               name

 L. 242        16  SETUP_FINALLY        40  'to 40'

 L. 243        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _BitmapImage__photo
               22  LOAD_ATTR                tk
               24  LOAD_METHOD              call
               26  LOAD_STR                 'image'
               28  LOAD_STR                 'delete'
               30  LOAD_FAST                'name'
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         58  'to 58'
             40_0  COME_FROM_FINALLY    16  '16'

 L. 244        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  <121>                56  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 245        52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            38  '38'

Parse error at or near `<121>' instruction at offset 44

    def width(self):
        """
        Get the width of the image.

        :return: The width, in pixels.
        """
        return self._BitmapImage__size[0]

    def height(self):
        """
        Get the height of the image.

        :return: The height, in pixels.
        """
        return self._BitmapImage__size[1]

    def __str__(self):
        """
        Get the Tkinter bitmap image identifier.  This method is automatically
        called by Tkinter whenever a BitmapImage object is passed to a Tkinter
        method.

        :return: A Tkinter bitmap image identifier (a string).
        """
        return str(self._BitmapImage__photo)


def getimage(photo):
    """Copies the contents of a PhotoImage to a PIL image memory."""
    im = Image.new'RGBA'(photo.width, photo.height)
    block = im.im
    photo.tk.call'PyImagingPhotoGet'photoblock.id
    return im


def _show(image, title):
    """Helper for the Image.show method."""

    class UI(tkinter.Label):

        def __init__(self, master, im):
            if im.mode == '1':
                self.image = BitmapImage(im, foreground='white', master=master)
            else:
                self.image = PhotoImage(im, master=master)
            super.__init__(master, image=(self.image), bg='black', bd=0)

    if not tkinter._default_root:
        raise OSError('tkinter not initialized')
    top = tkinter.Toplevel
    if title:
        top.titletitle
    UI(top, image).pack


# global _pilbitmap_ok ## Warning: Unused global