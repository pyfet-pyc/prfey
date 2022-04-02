# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\BufrStubImagePlugin.py
from . import Image, ImageFile
_handler = None

def register_handler(handler):
    """
    Install application-specific BUFR image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler


def _accept(prefix):
    return prefix[:4] == b'BUFR' or prefix[:4] == b'ZCZC'


class BufrStubImageFile(ImageFile.StubImageFile):
    format = 'BUFR'
    format_description = 'BUFR'

    def _open(self):
        offset = self.fp.tell()
        if not _accept(self.fp.read(4)):
            raise SyntaxError('Not a BUFR file')
        self.fp.seek(offset)
        self.mode = 'F'
        self._size = (1, 1)
        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler


def _save--- This code section failed: ---

 L.  62         0  LOAD_GLOBAL              _handler
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     18  'to 18'
                8  LOAD_GLOBAL              hasattr
               10  LOAD_STR                 '_handler'
               12  LOAD_STR                 'save'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'
             18_0  COME_FROM             6  '6'

 L.  63        18  LOAD_GLOBAL              OSError
               20  LOAD_STR                 'BUFR save handler not installed'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.  64        26  LOAD_GLOBAL              _handler
               28  LOAD_METHOD              save
               30  LOAD_FAST                'im'
               32  LOAD_FAST                'fp'
               34  LOAD_FAST                'filename'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          

Parse error at or near `None' instruction at offset -1


Image.register_open(BufrStubImageFile.format, BufrStubImageFile, _accept)
Image.register_save(BufrStubImageFile.format, _save)
Image.register_extension(BufrStubImageFile.format, '.bufr')