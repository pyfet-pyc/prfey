# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\MspImagePlugin.py
import io, struct
from . import Image, ImageFile
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
            checksum = checksum ^ i16(s, i)
        else:
            if checksum != 0:
                raise SyntaxError('bad MSP checksum')
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

 L. 118        64  LOAD_FAST                'self'
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
               88  JUMP_FORWARD        136  'to 136'
             90_0  COME_FROM_FINALLY    32  '32'

 L. 120        90  DUP_TOP          
               92  LOAD_GLOBAL              struct
               94  LOAD_ATTR                error
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   134  'to 134'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       122  'to 122'

 L. 121       108  LOAD_GLOBAL              OSError
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

 L. 123       136  LOAD_GLOBAL              enumerate
              138  LOAD_FAST                'rowmap'
              140  CALL_FUNCTION_1       1  ''
              142  GET_ITER         
            144_0  COME_FROM           390  '390'
            144_1  COME_FROM           386  '386'
            144_2  COME_FROM           334  '334'
            144_3  COME_FROM           174  '174'
              144  FOR_ITER            392  'to 392'
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'x'
              150  STORE_FAST               'rowlen'

 L. 124       152  SETUP_FINALLY       336  'to 336'

 L. 125       154  LOAD_FAST                'rowlen'
              156  LOAD_CONST               0
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L. 126       162  LOAD_FAST                'img'
              164  LOAD_METHOD              write
              166  LOAD_FAST                'blank_line'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 127       172  POP_BLOCK        
              174  JUMP_BACK           144  'to 144'
            176_0  COME_FROM           160  '160'

 L. 128       176  LOAD_FAST                'self'
              178  LOAD_ATTR                fd
              180  LOAD_METHOD              read
              182  LOAD_FAST                'rowlen'
              184  CALL_METHOD_1         1  ''
              186  STORE_FAST               'row'

 L. 129       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'row'
              192  CALL_FUNCTION_1       1  ''
              194  LOAD_FAST                'rowlen'
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L. 130       200  LOAD_GLOBAL              OSError

 L. 131       202  LOAD_STR                 'Truncated MSP file, expected %d bytes on row %s'

 L. 131       204  LOAD_FAST                'rowlen'
              206  LOAD_FAST                'x'
              208  BUILD_TUPLE_2         2 

 L. 130       210  CALL_FUNCTION_2       2  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           198  '198'

 L. 133       214  LOAD_CONST               0
              216  STORE_FAST               'idx'
            218_0  COME_FROM           330  '330'
            218_1  COME_FROM           294  '294'

 L. 134       218  LOAD_FAST                'idx'
              220  LOAD_FAST                'rowlen'
              222  COMPARE_OP               <
          224_226  POP_JUMP_IF_FALSE   332  'to 332'

 L. 135       228  LOAD_FAST                'row'
              230  LOAD_FAST                'idx'
              232  BINARY_SUBSCR    
              234  STORE_FAST               'runtype'

 L. 136       236  LOAD_FAST                'idx'
              238  LOAD_CONST               1
              240  INPLACE_ADD      
              242  STORE_FAST               'idx'

 L. 137       244  LOAD_FAST                'runtype'
              246  LOAD_CONST               0
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   296  'to 296'

 L. 138       254  LOAD_GLOBAL              struct
              256  LOAD_METHOD              unpack_from
              258  LOAD_STR                 'Bc'
              260  LOAD_FAST                'row'
              262  LOAD_FAST                'idx'
              264  CALL_METHOD_3         3  ''
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'runcount'
              270  STORE_FAST               'runval'

 L. 139       272  LOAD_FAST                'img'
              274  LOAD_METHOD              write
              276  LOAD_FAST                'runval'
              278  LOAD_FAST                'runcount'
              280  BINARY_MULTIPLY  
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L. 140       286  LOAD_FAST                'idx'
              288  LOAD_CONST               2
              290  INPLACE_ADD      
              292  STORE_FAST               'idx'
              294  JUMP_BACK           218  'to 218'
            296_0  COME_FROM           250  '250'

 L. 142       296  LOAD_FAST                'runtype'
              298  STORE_FAST               'runcount'

 L. 143       300  LOAD_FAST                'img'
              302  LOAD_METHOD              write
              304  LOAD_FAST                'row'
              306  LOAD_FAST                'idx'
              308  LOAD_FAST                'idx'
              310  LOAD_FAST                'runcount'
              312  BINARY_ADD       
              314  BUILD_SLICE_2         2 
              316  BINARY_SUBSCR    
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 144       322  LOAD_FAST                'idx'
              324  LOAD_FAST                'runcount'
              326  INPLACE_ADD      
              328  STORE_FAST               'idx'
              330  JUMP_BACK           218  'to 218'
            332_0  COME_FROM           224  '224'
              332  POP_BLOCK        
              334  JUMP_BACK           144  'to 144'
            336_0  COME_FROM_FINALLY   152  '152'

 L. 146       336  DUP_TOP          
              338  LOAD_GLOBAL              struct
              340  LOAD_ATTR                error
              342  COMPARE_OP               exception-match
          344_346  POP_JUMP_IF_FALSE   388  'to 388'
              348  POP_TOP          
              350  STORE_FAST               'e'
              352  POP_TOP          
              354  SETUP_FINALLY       376  'to 376'

 L. 147       356  LOAD_GLOBAL              OSError
              358  LOAD_STR                 'Corrupted MSP file in row '
              360  LOAD_FAST                'x'
              362  FORMAT_VALUE          0  ''
              364  BUILD_STRING_2        2 
              366  CALL_FUNCTION_1       1  ''
              368  LOAD_FAST                'e'
              370  RAISE_VARARGS_2       2  'exception instance with __cause__'
              372  POP_BLOCK        
              374  BEGIN_FINALLY    
            376_0  COME_FROM_FINALLY   354  '354'
              376  LOAD_CONST               None
              378  STORE_FAST               'e'
              380  DELETE_FAST              'e'
              382  END_FINALLY      
              384  POP_EXCEPT       
              386  JUMP_BACK           144  'to 144'
            388_0  COME_FROM           344  '344'
              388  END_FINALLY      
              390  JUMP_BACK           144  'to 144'
            392_0  COME_FROM           144  '144'

 L. 149       392  LOAD_FAST                'self'
              394  LOAD_METHOD              set_as_raw
              396  LOAD_FAST                'img'
              398  LOAD_METHOD              getvalue
              400  CALL_METHOD_0         0  ''
              402  LOAD_CONST               ('1', 0, 1)
              404  CALL_METHOD_2         2  ''
              406  POP_TOP          

 L. 151       408  LOAD_CONST               (0, 0)
              410  RETURN_VALUE     
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