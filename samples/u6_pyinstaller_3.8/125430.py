# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\MspImagePlugin.py
import io, struct
from . import Image, ImageFile
from ._binary import i8
from ._binary import i16le as i16
from ._binary import o16le as o16

def _accept(prefix):
    return prefix[:4] in (b'DanM', b'LinS')


class MspImageFile(ImageFile.ImageFile):
    format = 'MSP'
    format_description = 'Windows Paint'

    def _open(self):
        s = self.fp.read(32)
        if not _accept(s):
            raise SyntaxError('not an MSP file')
        checksum = 0
        for i in range(0, 32, 2):
            checksum = checksum ^ i16(s[i:i + 2])
        else:
            if checksum != 0:
                raise SyntaxError('bad MSP checksum')
            else:
                self.mode = '1'
                self._size = (i16(s[4:]), i16(s[6:]))
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

 L. 114         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              BytesIO
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'img'

 L. 115         8  LOAD_GLOBAL              bytearray
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

 L. 116        32  SETUP_FINALLY        90  'to 90'

 L. 117        34  LOAD_FAST                'self'
               36  LOAD_ATTR                fd
               38  LOAD_METHOD              seek
               40  LOAD_CONST               32
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 118        46  LOAD_GLOBAL              struct
               48  LOAD_METHOD              unpack_from

 L. 119        50  LOAD_STR                 '<'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                state
               56  LOAD_ATTR                ysize
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 'H'
               62  BUILD_STRING_3        3 

 L. 119        64  LOAD_FAST                'self'
               66  LOAD_ATTR                fd
               68  LOAD_METHOD              read
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                state
               74  LOAD_ATTR                ysize
               76  LOAD_CONST               2
               78  BINARY_MULTIPLY  
               80  CALL_METHOD_1         1  ''

 L. 118        82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'rowmap'
               86  POP_BLOCK        
               88  JUMP_FORWARD        136  'to 136'
             90_0  COME_FROM_FINALLY    32  '32'

 L. 121        90  DUP_TOP          
               92  LOAD_GLOBAL              struct
               94  LOAD_ATTR                error
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   134  'to 134'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       122  'to 122'

 L. 122       108  LOAD_GLOBAL              OSError
              110  LOAD_STR                 'Truncated MSP file in row map'
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_FAST                'e'
              116  RAISE_VARARGS_2       2  'exception instance with __cause__'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_FINALLY   106  '106'
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM            98  '98'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            88  '88'

 L. 124       136  LOAD_GLOBAL              enumerate
              138  LOAD_FAST                'rowmap'
              140  CALL_FUNCTION_1       1  ''
              142  GET_ITER         
              144  FOR_ITER            396  'to 396'
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'x'
              150  STORE_FAST               'rowlen'

 L. 125       152  SETUP_FINALLY       340  'to 340'

 L. 126       154  LOAD_FAST                'rowlen'
              156  LOAD_CONST               0
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 127       162  LOAD_FAST                'img'
              164  LOAD_METHOD              write
              166  LOAD_FAST                'blank_line'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 128       172  POP_BLOCK        
              174  JUMP_BACK           144  'to 144'
            176_0  COME_FROM           160  '160'

 L. 129       176  LOAD_FAST                'self'
              178  LOAD_ATTR                fd
              180  LOAD_METHOD              read
              182  LOAD_FAST                'rowlen'
              184  CALL_METHOD_1         1  ''
              186  STORE_FAST               'row'

 L. 130       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'row'
              192  CALL_FUNCTION_1       1  ''
              194  LOAD_FAST                'rowlen'
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L. 131       200  LOAD_GLOBAL              OSError

 L. 132       202  LOAD_STR                 'Truncated MSP file, expected %d bytes on row %s'

 L. 132       204  LOAD_FAST                'rowlen'
              206  LOAD_FAST                'x'
              208  BUILD_TUPLE_2         2 

 L. 131       210  CALL_FUNCTION_2       2  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           198  '198'

 L. 134       214  LOAD_CONST               0
              216  STORE_FAST               'idx'

 L. 135       218  LOAD_FAST                'idx'
              220  LOAD_FAST                'rowlen'
              222  COMPARE_OP               <
          224_226  POP_JUMP_IF_FALSE   336  'to 336'

 L. 136       228  LOAD_GLOBAL              i8
              230  LOAD_FAST                'row'
              232  LOAD_FAST                'idx'
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'runtype'

 L. 137       240  LOAD_FAST                'idx'
              242  LOAD_CONST               1
              244  INPLACE_ADD      
              246  STORE_FAST               'idx'

 L. 138       248  LOAD_FAST                'runtype'
              250  LOAD_CONST               0
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   300  'to 300'

 L. 139       258  LOAD_GLOBAL              struct
              260  LOAD_METHOD              unpack_from
              262  LOAD_STR                 'Bc'
              264  LOAD_FAST                'row'
              266  LOAD_FAST                'idx'
              268  CALL_METHOD_3         3  ''
              270  UNPACK_SEQUENCE_2     2 
              272  STORE_FAST               'runcount'
              274  STORE_FAST               'runval'

 L. 140       276  LOAD_FAST                'img'
              278  LOAD_METHOD              write
              280  LOAD_FAST                'runval'
              282  LOAD_FAST                'runcount'
              284  BINARY_MULTIPLY  
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 141       290  LOAD_FAST                'idx'
              292  LOAD_CONST               2
              294  INPLACE_ADD      
              296  STORE_FAST               'idx'
              298  JUMP_BACK           218  'to 218'
            300_0  COME_FROM           254  '254'

 L. 143       300  LOAD_FAST                'runtype'
              302  STORE_FAST               'runcount'

 L. 144       304  LOAD_FAST                'img'
              306  LOAD_METHOD              write
              308  LOAD_FAST                'row'
              310  LOAD_FAST                'idx'
              312  LOAD_FAST                'idx'
              314  LOAD_FAST                'runcount'
              316  BINARY_ADD       
              318  BUILD_SLICE_2         2 
              320  BINARY_SUBSCR    
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L. 145       326  LOAD_FAST                'idx'
              328  LOAD_FAST                'runcount'
              330  INPLACE_ADD      
              332  STORE_FAST               'idx'
              334  JUMP_BACK           218  'to 218'
            336_0  COME_FROM           224  '224'
              336  POP_BLOCK        
              338  JUMP_BACK           144  'to 144'
            340_0  COME_FROM_FINALLY   152  '152'

 L. 147       340  DUP_TOP          
              342  LOAD_GLOBAL              struct
              344  LOAD_ATTR                error
              346  COMPARE_OP               exception-match
          348_350  POP_JUMP_IF_FALSE   392  'to 392'
              352  POP_TOP          
              354  STORE_FAST               'e'
              356  POP_TOP          
              358  SETUP_FINALLY       380  'to 380'

 L. 148       360  LOAD_GLOBAL              OSError
              362  LOAD_STR                 'Corrupted MSP file in row '
              364  LOAD_FAST                'x'
              366  FORMAT_VALUE          0  ''
              368  BUILD_STRING_2        2 
              370  CALL_FUNCTION_1       1  ''
              372  LOAD_FAST                'e'
              374  RAISE_VARARGS_2       2  'exception instance with __cause__'
              376  POP_BLOCK        
              378  BEGIN_FINALLY    
            380_0  COME_FROM_FINALLY   358  '358'
              380  LOAD_CONST               None
              382  STORE_FAST               'e'
              384  DELETE_FAST              'e'
              386  END_FINALLY      
              388  POP_EXCEPT       
              390  JUMP_BACK           144  'to 144'
            392_0  COME_FROM           348  '348'
              392  END_FINALLY      
              394  JUMP_BACK           144  'to 144'

 L. 150       396  LOAD_FAST                'self'
              398  LOAD_METHOD              set_as_raw
              400  LOAD_FAST                'img'
              402  LOAD_METHOD              getvalue
              404  CALL_METHOD_0         0  ''
              406  LOAD_CONST               ('1', 0, 1)
              408  CALL_METHOD_2         2  ''
              410  POP_TOP          

 L. 152       412  LOAD_CONST               (0, 0)
              414  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 174


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