# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\MspImagePlugin.py
import io, struct
from . import Image, ImageFile
from ._binary import i8, i16le as i16, o16le as o16

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

 L. 112         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              BytesIO
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'img'

 L. 113         8  LOAD_GLOBAL              bytearray
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

 L. 114        32  SETUP_FINALLY        86  'to 86'

 L. 115        34  LOAD_FAST                'self'
               36  LOAD_ATTR                fd
               38  LOAD_METHOD              seek
               40  LOAD_CONST               32
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 116        46  LOAD_GLOBAL              struct
               48  LOAD_METHOD              unpack_from

 L. 117        50  LOAD_STR                 '<%dH'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                state
               56  LOAD_ATTR                ysize
               58  BINARY_MODULO    

 L. 117        60  LOAD_FAST                'self'
               62  LOAD_ATTR                fd
               64  LOAD_METHOD              read
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                state
               70  LOAD_ATTR                ysize
               72  LOAD_CONST               2
               74  BINARY_MULTIPLY  
               76  CALL_METHOD_1         1  ''

 L. 116        78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'rowmap'
               82  POP_BLOCK        
               84  JUMP_FORWARD        132  'to 132'
             86_0  COME_FROM_FINALLY    32  '32'

 L. 119        86  DUP_TOP          
               88  LOAD_GLOBAL              struct
               90  LOAD_ATTR                error
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   130  'to 130'
               96  POP_TOP          
               98  STORE_FAST               'e'
              100  POP_TOP          
              102  SETUP_FINALLY       118  'to 118'

 L. 120       104  LOAD_GLOBAL              OSError
              106  LOAD_STR                 'Truncated MSP file in row map'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'e'
              112  RAISE_VARARGS_2       2  'exception instance with __cause__'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY   102  '102'
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM            94  '94'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            84  '84'

 L. 122       132  LOAD_GLOBAL              enumerate
              134  LOAD_FAST                'rowmap'
              136  CALL_FUNCTION_1       1  ''
              138  GET_ITER         
            140_0  COME_FROM           388  '388'
            140_1  COME_FROM           384  '384'
            140_2  COME_FROM           334  '334'
            140_3  COME_FROM           170  '170'
              140  FOR_ITER            390  'to 390'
              142  UNPACK_SEQUENCE_2     2 
              144  STORE_FAST               'x'
              146  STORE_FAST               'rowlen'

 L. 123       148  SETUP_FINALLY       336  'to 336'

 L. 124       150  LOAD_FAST                'rowlen'
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 125       158  LOAD_FAST                'img'
              160  LOAD_METHOD              write
              162  LOAD_FAST                'blank_line'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 126       168  POP_BLOCK        
              170  JUMP_BACK           140  'to 140'
            172_0  COME_FROM           156  '156'

 L. 127       172  LOAD_FAST                'self'
              174  LOAD_ATTR                fd
              176  LOAD_METHOD              read
              178  LOAD_FAST                'rowlen'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'row'

 L. 128       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'row'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'rowlen'
              192  COMPARE_OP               !=
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 129       196  LOAD_GLOBAL              OSError

 L. 130       198  LOAD_STR                 'Truncated MSP file, expected %d bytes on row %s'

 L. 130       200  LOAD_FAST                'rowlen'
              202  LOAD_FAST                'x'
              204  BUILD_TUPLE_2         2 

 L. 129       206  CALL_FUNCTION_2       2  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           194  '194'

 L. 132       210  LOAD_CONST               0
              212  STORE_FAST               'idx'
            214_0  COME_FROM           330  '330'
            214_1  COME_FROM           294  '294'

 L. 133       214  LOAD_FAST                'idx'
              216  LOAD_FAST                'rowlen'
              218  COMPARE_OP               <
          220_222  POP_JUMP_IF_FALSE   332  'to 332'

 L. 134       224  LOAD_GLOBAL              i8
              226  LOAD_FAST                'row'
              228  LOAD_FAST                'idx'
              230  BINARY_SUBSCR    
              232  CALL_FUNCTION_1       1  ''
              234  STORE_FAST               'runtype'

 L. 135       236  LOAD_FAST                'idx'
              238  LOAD_CONST               1
              240  INPLACE_ADD      
              242  STORE_FAST               'idx'

 L. 136       244  LOAD_FAST                'runtype'
              246  LOAD_CONST               0
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   296  'to 296'

 L. 137       254  LOAD_GLOBAL              struct
              256  LOAD_METHOD              unpack_from
              258  LOAD_STR                 'Bc'
              260  LOAD_FAST                'row'
              262  LOAD_FAST                'idx'
              264  CALL_METHOD_3         3  ''
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'runcount'
              270  STORE_FAST               'runval'

 L. 138       272  LOAD_FAST                'img'
              274  LOAD_METHOD              write
              276  LOAD_FAST                'runval'
              278  LOAD_FAST                'runcount'
              280  BINARY_MULTIPLY  
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          

 L. 139       286  LOAD_FAST                'idx'
              288  LOAD_CONST               2
              290  INPLACE_ADD      
              292  STORE_FAST               'idx'
              294  JUMP_BACK           214  'to 214'
            296_0  COME_FROM           250  '250'

 L. 141       296  LOAD_FAST                'runtype'
              298  STORE_FAST               'runcount'

 L. 142       300  LOAD_FAST                'img'
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

 L. 143       322  LOAD_FAST                'idx'
              324  LOAD_FAST                'runcount'
              326  INPLACE_ADD      
              328  STORE_FAST               'idx'
              330  JUMP_BACK           214  'to 214'
            332_0  COME_FROM           220  '220'
              332  POP_BLOCK        
              334  JUMP_BACK           140  'to 140'
            336_0  COME_FROM_FINALLY   148  '148'

 L. 145       336  DUP_TOP          
              338  LOAD_GLOBAL              struct
              340  LOAD_ATTR                error
              342  COMPARE_OP               exception-match
          344_346  POP_JUMP_IF_FALSE   386  'to 386'
              348  POP_TOP          
              350  STORE_FAST               'e'
              352  POP_TOP          
              354  SETUP_FINALLY       374  'to 374'

 L. 146       356  LOAD_GLOBAL              OSError
              358  LOAD_STR                 'Corrupted MSP file in row %d'
              360  LOAD_FAST                'x'
              362  BINARY_MODULO    
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_FAST                'e'
              368  RAISE_VARARGS_2       2  'exception instance with __cause__'
              370  POP_BLOCK        
              372  BEGIN_FINALLY    
            374_0  COME_FROM_FINALLY   354  '354'
              374  LOAD_CONST               None
              376  STORE_FAST               'e'
              378  DELETE_FAST              'e'
              380  END_FINALLY      
              382  POP_EXCEPT       
              384  JUMP_BACK           140  'to 140'
            386_0  COME_FROM           344  '344'
              386  END_FINALLY      
              388  JUMP_BACK           140  'to 140'
            390_0  COME_FROM           140  '140'

 L. 148       390  LOAD_FAST                'self'
              392  LOAD_METHOD              set_as_raw
              394  LOAD_FAST                'img'
              396  LOAD_METHOD              getvalue
              398  CALL_METHOD_0         0  ''
              400  LOAD_CONST               ('1', 0, 1)
              402  CALL_METHOD_2         2  ''
              404  POP_TOP          

 L. 150       406  LOAD_CONST               (0, 0)
              408  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 170


Image.register_decoder('MSP', MspDecoder)

def _save(im, fp, filename):
    if im.mode != '1':
        raise OSError('cannot write mode %s as MSP' % im.mode)
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