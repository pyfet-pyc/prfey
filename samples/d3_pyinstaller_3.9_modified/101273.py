# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\DcxImagePlugin.py
from . import Image
from ._binary import i32le as i32
from .PcxImagePlugin import PcxImageFile
MAGIC = 987654321

def _accept(prefix):
    return len(prefix) >= 4 and i32(prefix) == MAGIC


class DcxImageFile(PcxImageFile):
    format = 'DCX'
    format_description = 'Intel DCX'
    _close_exclusive_fp_after_loading = False

    def _open(self):
        s = self.fp.read(4)
        if not _accept(s):
            raise SyntaxError('not a DCX file')
        self._offset = []
        for i in range(1024):
            offset = i32(self.fp.read(4))
            if not offset:
                break
            else:
                self._offset.append(offset)
        else:
            self._DcxImageFile__fp = self.fp
            self.frame = None
            self.n_frames = len(self._offset)
            self.is_animated = self.n_frames > 1
            self.seek(0)

    def seek(self, frame):
        if not self._seek_check(frame):
            return
        self.frame = frame
        self.fp = self._DcxImageFile__fp
        self.fp.seek(self._offset[frame])
        PcxImageFile._open(self)

    def tell(self):
        return self.frame

    def _close__fp--- This code section failed: ---

 L.  78         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L.  79         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _DcxImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  80        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _DcxImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L.  81        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  82        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L.  84        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _DcxImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _DcxImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


Image.register_open(DcxImageFile.format, DcxImageFile, _accept)
Image.register_extension(DcxImageFile.format, '.dcx')