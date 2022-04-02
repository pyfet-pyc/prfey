# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\WmfImagePlugin.py
from . import Image, ImageFile
from ._binary import i16le as word
from ._binary import i32le as dword
from ._binary import si16le as short
from ._binary import si32le as _long
_handler = None

def register_handler(handler):
    """
    Install application-specific WMF image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


if hasattr(Image.core, 'drawwmf'):

    class WmfHandler:

        def open(self, im):
            im.mode = 'RGB'
            self.bbox = im.info['wmf_bbox']

        def load(self, im):
            im.fp.seek(0)
            return Image.frombytes('RGB', im.size, Image.core.drawwmf(im.fp.read(), im.size, self.bbox), 'raw', 'BGR', im.size[0] * 3 + 3 & -4, -1)


    register_handler(WmfHandler())

def _accept(prefix):
    return prefix[:6] == b'\xd7\xcd\xc6\x9a\x00\x00' or prefix[:4] == b'\x01\x00\x00\x00'


class WmfStubImageFile(ImageFile.StubImageFile):
    format = 'WMF'
    format_description = 'Windows Metafile'

    def _open(self):
        self._inch = None
        s = self.fp.read(80)
        if s[:6] == b'\xd7\xcd\xc6\x9a\x00\x00':
            self._inch = word(s, 14)
            x0 = short(s, 6)
            y0 = short(s, 8)
            x1 = short(s, 10)
            y1 = short(s, 12)
            self.info['dpi'] = 72
            size = (
             (x1 - x0) * self.info['dpi'] // self._inch,
             (y1 - y0) * self.info['dpi'] // self._inch)
            self.info['wmf_bbox'] = (
             x0, y0, x1, y1)
            if s[22:26] != b'\x01\x00\t\x00':
                raise SyntaxError('Unsupported WMF file format')
        else:
            if dword(s) == 1:
                if s[40:44] == b' EMF':
                    x0 = _long(s, 8)
                    y0 = _long(s, 12)
                    x1 = _long(s, 16)
                    y1 = _long(s, 20)
                    frame = (
                     _long(s, 24), _long(s, 28), _long(s, 32), _long(s, 36))
                    size = (
                     x1 - x0, y1 - y0)
                    xdpi = 2540.0 * (x1 - y0) / (frame[2] - frame[0])
                    ydpi = 2540.0 * (y1 - y0) / (frame[3] - frame[1])
                    self.info['wmf_bbox'] = (
                     x0, y0, x1, y1)
                    if xdpi == ydpi:
                        self.info['dpi'] = xdpi
                else:
                    self.info['dpi'] = (
                     xdpi, ydpi)
            else:
                raise SyntaxError('Unsupported file format')
        self.mode = 'RGB'
        self._size = size
        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler

    def load--- This code section failed: ---

 L. 154         0  LOAD_FAST                'dpi'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    96  'to 96'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _inch
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    96  'to 96'

 L. 155        18  LOAD_FAST                'dpi'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                info
               24  LOAD_STR                 'dpi'
               26  STORE_SUBSCR     

 L. 156        28  LOAD_FAST                'self'
               30  LOAD_ATTR                info
               32  LOAD_STR                 'wmf_bbox'
               34  BINARY_SUBSCR    
               36  UNPACK_SEQUENCE_4     4 
               38  STORE_FAST               'x0'
               40  STORE_FAST               'y0'
               42  STORE_FAST               'x1'
               44  STORE_FAST               'y1'

 L. 158        46  LOAD_FAST                'x1'
               48  LOAD_FAST                'x0'
               50  BINARY_SUBTRACT  
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                info
               56  LOAD_STR                 'dpi'
               58  BINARY_SUBSCR    
               60  BINARY_MULTIPLY  
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _inch
               66  BINARY_FLOOR_DIVIDE

 L. 159        68  LOAD_FAST                'y1'
               70  LOAD_FAST                'y0'
               72  BINARY_SUBTRACT  
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                info
               78  LOAD_STR                 'dpi'
               80  BINARY_SUBSCR    
               82  BINARY_MULTIPLY  
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _inch
               88  BINARY_FLOOR_DIVIDE

 L. 157        90  BUILD_TUPLE_2         2 
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _size
             96_0  COME_FROM            16  '16'
             96_1  COME_FROM             6  '6'

 L. 161        96  LOAD_GLOBAL              super
               98  CALL_FUNCTION_0       0  ''
              100  LOAD_METHOD              load
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          

Parse error at or near `None' instruction at offset -1


def _save--- This code section failed: ---

 L. 165         0  LOAD_GLOBAL              _handler
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     18  'to 18'
                8  LOAD_GLOBAL              hasattr
               10  LOAD_GLOBAL              _handler
               12  LOAD_STR                 'save'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'
             18_0  COME_FROM             6  '6'

 L. 166        18  LOAD_GLOBAL              OSError
               20  LOAD_STR                 'WMF save handler not installed'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 167        26  LOAD_GLOBAL              _handler
               28  LOAD_METHOD              save
               30  LOAD_FAST                'im'
               32  LOAD_FAST                'fp'
               34  LOAD_FAST                'filename'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          

Parse error at or near `None' instruction at offset -1


Image.register_open(WmfStubImageFile.format, WmfStubImageFile, _accept)
Image.register_save(WmfStubImageFile.format, _save)
Image.register_extensions(WmfStubImageFile.format, ['.wmf', '.emf'])