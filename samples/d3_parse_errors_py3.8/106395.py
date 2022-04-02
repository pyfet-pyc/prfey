# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\MspImagePlugin.py
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
        if s[:4] not in (b'DanM', b'LinS'):
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
               84  JUMP_FORWARD        116  'to 116'
             86_0  COME_FROM_FINALLY    32  '32'

 L. 119        86  DUP_TOP          
               88  LOAD_GLOBAL              struct
               90  LOAD_ATTR                error
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   114  'to 114'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 120       102  LOAD_GLOBAL              OSError
              104  LOAD_STR                 'Truncated MSP file in row map'
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM            94  '94'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            84  '84'

 L. 122       116  LOAD_GLOBAL              enumerate
              118  LOAD_FAST                'rowmap'
              120  CALL_FUNCTION_1       1  ''
              122  GET_ITER         
            124_0  COME_FROM           356  '356'
            124_1  COME_FROM           352  '352'
            124_2  COME_FROM           318  '318'
            124_3  COME_FROM           154  '154'
              124  FOR_ITER            358  'to 358'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'x'
              130  STORE_FAST               'rowlen'

 L. 123       132  SETUP_FINALLY       320  'to 320'

 L. 124       134  LOAD_FAST                'rowlen'
              136  LOAD_CONST               0
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   156  'to 156'

 L. 125       142  LOAD_FAST                'img'
              144  LOAD_METHOD              write
              146  LOAD_FAST                'blank_line'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L. 126       152  POP_BLOCK        
              154  JUMP_BACK           124  'to 124'
            156_0  COME_FROM           140  '140'

 L. 127       156  LOAD_FAST                'self'
              158  LOAD_ATTR                fd
              160  LOAD_METHOD              read
              162  LOAD_FAST                'rowlen'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'row'

 L. 128       168  LOAD_GLOBAL              len
              170  LOAD_FAST                'row'
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_FAST                'rowlen'
              176  COMPARE_OP               !=
              178  POP_JUMP_IF_FALSE   194  'to 194'

 L. 129       180  LOAD_GLOBAL              OSError

 L. 130       182  LOAD_STR                 'Truncated MSP file, expected %d bytes on row %s'

 L. 130       184  LOAD_FAST                'rowlen'
              186  LOAD_FAST                'x'
              188  BUILD_TUPLE_2         2 

 L. 129       190  CALL_FUNCTION_2       2  ''
              192  RAISE_VARARGS_1       1  'exception instance'
            194_0  COME_FROM           178  '178'

 L. 132       194  LOAD_CONST               0
              196  STORE_FAST               'idx'
            198_0  COME_FROM           314  '314'
            198_1  COME_FROM           278  '278'

 L. 133       198  LOAD_FAST                'idx'
              200  LOAD_FAST                'rowlen'
              202  COMPARE_OP               <
          204_206  POP_JUMP_IF_FALSE   316  'to 316'

 L. 134       208  LOAD_GLOBAL              i8
              210  LOAD_FAST                'row'
              212  LOAD_FAST                'idx'
              214  BINARY_SUBSCR    
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'runtype'

 L. 135       220  LOAD_FAST                'idx'
              222  LOAD_CONST               1
              224  INPLACE_ADD      
              226  STORE_FAST               'idx'

 L. 136       228  LOAD_FAST                'runtype'
              230  LOAD_CONST               0
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   280  'to 280'

 L. 137       238  LOAD_GLOBAL              struct
              240  LOAD_METHOD              unpack_from
              242  LOAD_STR                 'Bc'
              244  LOAD_FAST                'row'
              246  LOAD_FAST                'idx'
              248  CALL_METHOD_3         3  ''
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'runcount'
              254  STORE_FAST               'runval'

 L. 138       256  LOAD_FAST                'img'
              258  LOAD_METHOD              write
              260  LOAD_FAST                'runval'
              262  LOAD_FAST                'runcount'
              264  BINARY_MULTIPLY  
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          

 L. 139       270  LOAD_FAST                'idx'
              272  LOAD_CONST               2
              274  INPLACE_ADD      
              276  STORE_FAST               'idx'
              278  JUMP_BACK           198  'to 198'
            280_0  COME_FROM           234  '234'

 L. 141       280  LOAD_FAST                'runtype'
              282  STORE_FAST               'runcount'

 L. 142       284  LOAD_FAST                'img'
              286  LOAD_METHOD              write
              288  LOAD_FAST                'row'
              290  LOAD_FAST                'idx'
              292  LOAD_FAST                'idx'
              294  LOAD_FAST                'runcount'
              296  BINARY_ADD       
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          

 L. 143       306  LOAD_FAST                'idx'
              308  LOAD_FAST                'runcount'
              310  INPLACE_ADD      
              312  STORE_FAST               'idx'
              314  JUMP_BACK           198  'to 198'
            316_0  COME_FROM           204  '204'
              316  POP_BLOCK        
              318  JUMP_BACK           124  'to 124'
            320_0  COME_FROM_FINALLY   132  '132'

 L. 145       320  DUP_TOP          
              322  LOAD_GLOBAL              struct
              324  LOAD_ATTR                error
              326  COMPARE_OP               exception-match
          328_330  POP_JUMP_IF_FALSE   354  'to 354'
              332  POP_TOP          
              334  POP_TOP          
              336  POP_TOP          

 L. 146       338  LOAD_GLOBAL              OSError
              340  LOAD_STR                 'Corrupted MSP file in row %d'
              342  LOAD_FAST                'x'
              344  BINARY_MODULO    
              346  CALL_FUNCTION_1       1  ''
              348  RAISE_VARARGS_1       1  'exception instance'
              350  POP_EXCEPT       
              352  JUMP_BACK           124  'to 124'
            354_0  COME_FROM           328  '328'
              354  END_FINALLY      
              356  JUMP_BACK           124  'to 124'
            358_0  COME_FROM           124  '124'

 L. 148       358  LOAD_FAST                'self'
              360  LOAD_METHOD              set_as_raw
              362  LOAD_FAST                'img'
              364  LOAD_METHOD              getvalue
              366  CALL_METHOD_0         0  ''
              368  LOAD_CONST               ('1', 0, 1)
              370  CALL_METHOD_2         2  ''
              372  POP_TOP          

 L. 150       374  LOAD_CONST               (0, 0)
              376  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 154


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