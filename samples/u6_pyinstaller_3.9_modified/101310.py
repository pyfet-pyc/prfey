# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\MspImagePlugin.py
import io, struct
from . import Image, ImageFile
from ._binary import i16le as i16
from ._binary import o16le as o16

def _accept--- This code section failed: ---

 L.  38         0  LOAD_FAST                'prefix'
                2  LOAD_CONST               None
                4  LOAD_CONST               4
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_CONST               (b'DanM', b'LinS')
               12  <118>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class MspImageFile(ImageFile.ImageFile):
    format = 'MSP'
    format_description = 'Windows Paint'

    def _open(self):
        s = self.fp.read(32)
        if not _accept(s):
            raise SyntaxError('not an MSP file')
        checksum = 0
        for i in range(0, 32, 2):
            checksum = checksum ^ i16(s, i)
        else:
            if checksum != 0:
                raise SyntaxError('bad MSP checksum')
            else:
                self.mode = '1'
                self._size = (i16(s, 4), i16(s, 6))
                if s[:4] == b'DanM':
                    self.tile = [
                     (
                      'raw', (0, 0) + self.size, 32, ('1', 0, 1))]
                else:
                    self.tile = [
                     (
                      'MSP', (0, 0) + self.size, 32, None)]


class MspDecoder(ImageFile.PyDecoder):
    _pulls_fd = True

    def decode--- This code section failed: ---

 L. 113         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              BytesIO
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'img'

 L. 114         8  LOAD_GLOBAL              bytearray
               10  LOAD_CONST               (255,)
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                state
               16  LOAD_ATTR                xsize
               18  LOAD_CONST               7
               20  BINARY_ADD       
               22  LOAD_CONST               8
               24  BINARY_FLOOR_DIVIDE
               26  BINARY_MULTIPLY  
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'blank_line'

 L. 115        32  SETUP_FINALLY        90  'to 90'

 L. 116        34  LOAD_FAST                'self'
               36  LOAD_ATTR                fd
               38  LOAD_METHOD              seek
               40  LOAD_CONST               32
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 117        46  LOAD_GLOBAL              struct
               48  LOAD_METHOD              unpack_from

 L. 118        50  LOAD_STR                 '<'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                state
               56  LOAD_ATTR                ysize
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 'H'
               62  BUILD_STRING_3        3 
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                fd
               68  LOAD_METHOD              read
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                state
               74  LOAD_ATTR                ysize
               76  LOAD_CONST               2
               78  BINARY_MULTIPLY  
               80  CALL_METHOD_1         1  ''

 L. 117        82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'rowmap'
               86  POP_BLOCK        
               88  JUMP_FORWARD        138  'to 138'
             90_0  COME_FROM_FINALLY    32  '32'

 L. 120        90  DUP_TOP          
               92  LOAD_GLOBAL              struct
               94  LOAD_ATTR                error
               96  <121>               136  ''
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       128  'to 128'

 L. 121       106  LOAD_GLOBAL              OSError
              108  LOAD_STR                 'Truncated MSP file in row map'
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_FAST                'e'
              114  RAISE_VARARGS_2       2  'exception instance with __cause__'
              116  POP_BLOCK        
              118  POP_EXCEPT       
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  JUMP_FORWARD        138  'to 138'
            128_0  COME_FROM_FINALLY   104  '104'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  <48>             
              136  <48>             
            138_0  COME_FROM           126  '126'
            138_1  COME_FROM            88  '88'

 L. 123       138  LOAD_GLOBAL              enumerate
              140  LOAD_FAST                'rowmap'
              142  CALL_FUNCTION_1       1  ''
              144  GET_ITER         
              146  FOR_ITER            396  'to 396'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'x'
              152  STORE_FAST               'rowlen'

 L. 124       154  SETUP_FINALLY       338  'to 338'

 L. 125       156  LOAD_FAST                'rowlen'
              158  LOAD_CONST               0
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   178  'to 178'

 L. 126       164  LOAD_FAST                'img'
              166  LOAD_METHOD              write
              168  LOAD_FAST                'blank_line'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 127       174  POP_BLOCK        
              176  JUMP_BACK           146  'to 146'
            178_0  COME_FROM           162  '162'

 L. 128       178  LOAD_FAST                'self'
              180  LOAD_ATTR                fd
              182  LOAD_METHOD              read
              184  LOAD_FAST                'rowlen'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'row'

 L. 129       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'row'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_FAST                'rowlen'
              198  COMPARE_OP               !=
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L. 130       202  LOAD_GLOBAL              OSError

 L. 131       204  LOAD_STR                 'Truncated MSP file, expected %d bytes on row %s'
              206  LOAD_FAST                'rowlen'
              208  LOAD_FAST                'x'
              210  BUILD_TUPLE_2         2 

 L. 130       212  CALL_FUNCTION_2       2  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           200  '200'

 L. 133       216  LOAD_CONST               0
              218  STORE_FAST               'idx'

 L. 134       220  LOAD_FAST                'idx'
              222  LOAD_FAST                'rowlen'
              224  COMPARE_OP               <
          226_228  POP_JUMP_IF_FALSE   334  'to 334'

 L. 135       230  LOAD_FAST                'row'
              232  LOAD_FAST                'idx'
              234  BINARY_SUBSCR    
              236  STORE_FAST               'runtype'

 L. 136       238  LOAD_FAST                'idx'
              240  LOAD_CONST               1
              242  INPLACE_ADD      
              244  STORE_FAST               'idx'

 L. 137       246  LOAD_FAST                'runtype'
              248  LOAD_CONST               0
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   298  'to 298'

 L. 138       256  LOAD_GLOBAL              struct
              258  LOAD_METHOD              unpack_from
              260  LOAD_STR                 'Bc'
              262  LOAD_FAST                'row'
              264  LOAD_FAST                'idx'
              266  CALL_METHOD_3         3  ''
              268  UNPACK_SEQUENCE_2     2 
              270  STORE_FAST               'runcount'
              272  STORE_FAST               'runval'

 L. 139       274  LOAD_FAST                'img'
              276  LOAD_METHOD              write
              278  LOAD_FAST                'runval'
              280  LOAD_FAST                'runcount'
              282  BINARY_MULTIPLY  
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 140       288  LOAD_FAST                'idx'
              290  LOAD_CONST               2
              292  INPLACE_ADD      
              294  STORE_FAST               'idx'
              296  JUMP_BACK           220  'to 220'
            298_0  COME_FROM           252  '252'

 L. 142       298  LOAD_FAST                'runtype'
              300  STORE_FAST               'runcount'

 L. 143       302  LOAD_FAST                'img'
              304  LOAD_METHOD              write
              306  LOAD_FAST                'row'
              308  LOAD_FAST                'idx'
              310  LOAD_FAST                'idx'
              312  LOAD_FAST                'runcount'
              314  BINARY_ADD       
              316  BUILD_SLICE_2         2 
              318  BINARY_SUBSCR    
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L. 144       324  LOAD_FAST                'idx'
              326  LOAD_FAST                'runcount'
              328  INPLACE_ADD      
              330  STORE_FAST               'idx'
              332  JUMP_BACK           220  'to 220'
            334_0  COME_FROM           226  '226'
              334  POP_BLOCK        
              336  JUMP_BACK           146  'to 146'
            338_0  COME_FROM_FINALLY   154  '154'

 L. 146       338  DUP_TOP          
              340  LOAD_GLOBAL              struct
              342  LOAD_ATTR                error
          344_346  <121>               392  ''
              348  POP_TOP          
              350  STORE_FAST               'e'
              352  POP_TOP          
              354  SETUP_FINALLY       384  'to 384'

 L. 147       356  LOAD_GLOBAL              OSError
              358  LOAD_STR                 'Corrupted MSP file in row '
              360  LOAD_FAST                'x'
              362  FORMAT_VALUE          0  ''
              364  BUILD_STRING_2        2 
              366  CALL_FUNCTION_1       1  ''
              368  LOAD_FAST                'e'
              370  RAISE_VARARGS_2       2  'exception instance with __cause__'
              372  POP_BLOCK        
              374  POP_EXCEPT       
              376  LOAD_CONST               None
              378  STORE_FAST               'e'
              380  DELETE_FAST              'e'
              382  JUMP_BACK           146  'to 146'
            384_0  COME_FROM_FINALLY   354  '354'
              384  LOAD_CONST               None
              386  STORE_FAST               'e'
              388  DELETE_FAST              'e'
              390  <48>             
              392  <48>             
              394  JUMP_BACK           146  'to 146'

 L. 149       396  LOAD_FAST                'self'
              398  LOAD_METHOD              set_as_raw
              400  LOAD_FAST                'img'
              402  LOAD_METHOD              getvalue
              404  CALL_METHOD_0         0  ''
              406  LOAD_CONST               ('1', 0, 1)
              408  CALL_METHOD_2         2  ''
              410  POP_TOP          

 L. 151       412  LOAD_CONST               (0, 0)
              414  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 96


Image.register_decoder('MSP', MspDecoder)

def _save(im, fp, filename):
    if im.mode != '1':
        raise OSError(f"cannot write mode {im.mode} as MSP")
    header = [
     0] * 16
    header[0], header[1] = i16(b'Da'), i16(b'nM')
    header[2], header[3] = im.size
    header[4], header[5] = (1, 1)
    header[6], header[7] = (1, 1)
    header[8], header[9] = im.size
    checksum = 0
    for h in header:
        checksum = checksum ^ h
    else:
        header[12] = checksum
        for h in header:
            fp.write(o16(h))
        else:
            ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 32, ('1', 0, 1))])


Image.register_open(MspImageFile.format, MspImageFile, _accept)
Image.register_save(MspImageFile.format, _save)
Image.register_extension(MspImageFile.format, '.msp')