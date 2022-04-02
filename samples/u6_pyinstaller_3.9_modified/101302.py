# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\IptcImagePlugin.py
import os, tempfile
from . import Image, ImageFile
from ._binary import i8
from ._binary import i16be as i16
from ._binary import i32be as i32
from ._binary import o8
COMPRESSION = {1:'raw', 
 5:'jpeg'}
PAD = o8(0) * 4

def i(c):
    return i32((PAD + c)[-4:])


def dump(c):
    for i in c:
        print(('%02x' % i8(i)), end=' ')
    else:
        print()


class IptcImageFile(ImageFile.ImageFile):
    format = 'IPTC'
    format_description = 'IPTC/NAA'

    def getint(self, key):
        return i(self.info[key])

    def field(self):
        s = self.fp.read(5)
        if not len(s):
            return (None, 0)
            tag = (
             s[1], s[2])
            if s[0] != 28 or tag[0] < 1 or tag[0] > 9:
                raise SyntaxError('invalid IPTC/NAA file')
            size = s[3]
            if size > 132:
                raise OSError('illegal field length in IPTC/NAA file')
        elif size == 128:
            size = 0
        else:
            if size > 128:
                size = i(self.fp.read(size - 128))
            else:
                size = i16(s, 3)
        return (
         tag, size)

    def _open--- This code section failed: ---

 L.  88         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              tell
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'offset'

 L.  89        10  LOAD_FAST                'self'
               12  LOAD_METHOD              field
               14  CALL_METHOD_0         0  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'tag'
               20  STORE_FAST               'size'

 L.  90        22  LOAD_FAST                'tag'
               24  POP_JUMP_IF_FALSE   136  'to 136'
               26  LOAD_FAST                'tag'
               28  LOAD_CONST               (8, 10)
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    36  'to 36'

 L.  91        34  BREAK_LOOP          136  'to 136'
             36_0  COME_FROM            32  '32'

 L.  92        36  LOAD_FAST                'size'
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L.  93        40  LOAD_FAST                'self'
               42  LOAD_ATTR                fp
               44  LOAD_METHOD              read
               46  LOAD_FAST                'size'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'tagdata'
               52  JUMP_FORWARD         58  'to 58'
             54_0  COME_FROM            38  '38'

 L.  95        54  LOAD_CONST               None
               56  STORE_FAST               'tagdata'
             58_0  COME_FROM            52  '52'

 L.  96        58  LOAD_FAST                'tag'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                info
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE   124  'to 124'

 L.  97        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                info
               74  LOAD_FAST                'tag'
               76  BINARY_SUBSCR    
               78  LOAD_GLOBAL              list
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L.  98        84  LOAD_FAST                'self'
               86  LOAD_ATTR                info
               88  LOAD_FAST                'tag'
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              append
               94  LOAD_FAST                'tagdata'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_ABSOLUTE       134  'to 134'
            102_0  COME_FROM            82  '82'

 L. 100       102  LOAD_FAST                'self'
              104  LOAD_ATTR                info
              106  LOAD_FAST                'tag'
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'tagdata'
              112  BUILD_LIST_2          2 
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                info
              118  LOAD_FAST                'tag'
              120  STORE_SUBSCR     
              122  JUMP_BACK             0  'to 0'
            124_0  COME_FROM            66  '66'

 L. 102       124  LOAD_FAST                'tagdata'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                info
              130  LOAD_FAST                'tag'
              132  STORE_SUBSCR     
              134  JUMP_BACK             0  'to 0'
            136_0  COME_FROM            24  '24'

 L. 105       136  LOAD_GLOBAL              i8
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                info
              142  LOAD_CONST               (3, 60)
              144  BINARY_SUBSCR    
              146  LOAD_CONST               0
              148  BINARY_SUBSCR    
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'layers'

 L. 106       154  LOAD_GLOBAL              i8
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                info
              160  LOAD_CONST               (3, 60)
              162  BINARY_SUBSCR    
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'component'

 L. 107       172  LOAD_CONST               (3, 65)
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                info
              178  <118>                 0  ''
              180  POP_JUMP_IF_FALSE   206  'to 206'

 L. 108       182  LOAD_GLOBAL              i8
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                info
              188  LOAD_CONST               (3, 65)
              190  BINARY_SUBSCR    
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_CONST               1
              200  BINARY_SUBTRACT  
              202  STORE_FAST               'id'
              204  JUMP_FORWARD        210  'to 210'
            206_0  COME_FROM           180  '180'

 L. 110       206  LOAD_CONST               0
              208  STORE_FAST               'id'
            210_0  COME_FROM           204  '204'

 L. 111       210  LOAD_FAST                'layers'
              212  LOAD_CONST               1
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   230  'to 230'
              218  LOAD_FAST                'component'
              220  POP_JUMP_IF_TRUE    230  'to 230'

 L. 112       222  LOAD_STR                 'L'
              224  LOAD_FAST                'self'
              226  STORE_ATTR               mode
              228  JUMP_FORWARD        280  'to 280'
            230_0  COME_FROM           220  '220'
            230_1  COME_FROM           216  '216'

 L. 113       230  LOAD_FAST                'layers'
              232  LOAD_CONST               3
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   254  'to 254'
              238  LOAD_FAST                'component'
              240  POP_JUMP_IF_FALSE   254  'to 254'

 L. 114       242  LOAD_STR                 'RGB'
              244  LOAD_FAST                'id'
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'self'
              250  STORE_ATTR               mode
              252  JUMP_FORWARD        280  'to 280'
            254_0  COME_FROM           240  '240'
            254_1  COME_FROM           236  '236'

 L. 115       254  LOAD_FAST                'layers'
              256  LOAD_CONST               4
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   280  'to 280'
              264  LOAD_FAST                'component'
          266_268  POP_JUMP_IF_FALSE   280  'to 280'

 L. 116       270  LOAD_STR                 'CMYK'
              272  LOAD_FAST                'id'
              274  BINARY_SUBSCR    
              276  LOAD_FAST                'self'
              278  STORE_ATTR               mode
            280_0  COME_FROM           266  '266'
            280_1  COME_FROM           260  '260'
            280_2  COME_FROM           252  '252'
            280_3  COME_FROM           228  '228'

 L. 119       280  LOAD_FAST                'self'
              282  LOAD_METHOD              getint
              284  LOAD_CONST               (3, 20)
              286  CALL_METHOD_1         1  ''
              288  LOAD_FAST                'self'
              290  LOAD_METHOD              getint
              292  LOAD_CONST               (3, 30)
              294  CALL_METHOD_1         1  ''
              296  BUILD_TUPLE_2         2 
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _size

 L. 122       302  SETUP_FINALLY       322  'to 322'

 L. 123       304  LOAD_GLOBAL              COMPRESSION
              306  LOAD_FAST                'self'
              308  LOAD_METHOD              getint
              310  LOAD_CONST               (3, 120)
              312  CALL_METHOD_1         1  ''
              314  BINARY_SUBSCR    
              316  STORE_FAST               'compression'
              318  POP_BLOCK        
              320  JUMP_FORWARD        370  'to 370'
            322_0  COME_FROM_FINALLY   302  '302'

 L. 124       322  DUP_TOP          
              324  LOAD_GLOBAL              KeyError
          326_328  <121>               368  ''
              330  POP_TOP          
              332  STORE_FAST               'e'
              334  POP_TOP          
              336  SETUP_FINALLY       360  'to 360'

 L. 125       338  LOAD_GLOBAL              OSError
              340  LOAD_STR                 'Unknown IPTC image compression'
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_FAST                'e'
              346  RAISE_VARARGS_2       2  'exception instance with __cause__'
              348  POP_BLOCK        
              350  POP_EXCEPT       
              352  LOAD_CONST               None
              354  STORE_FAST               'e'
              356  DELETE_FAST              'e'
              358  JUMP_FORWARD        370  'to 370'
            360_0  COME_FROM_FINALLY   336  '336'
              360  LOAD_CONST               None
              362  STORE_FAST               'e'
              364  DELETE_FAST              'e'
              366  <48>             
              368  <48>             
            370_0  COME_FROM           358  '358'
            370_1  COME_FROM           320  '320'

 L. 128       370  LOAD_FAST                'tag'
              372  LOAD_CONST               (8, 10)
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   418  'to 418'

 L. 130       380  LOAD_STR                 'iptc'
              382  LOAD_FAST                'compression'
              384  LOAD_FAST                'offset'
              386  BUILD_TUPLE_2         2 
              388  LOAD_CONST               0
              390  LOAD_CONST               0
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                size
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                size
              404  LOAD_CONST               1
              406  BINARY_SUBSCR    
              408  BUILD_TUPLE_4         4 
              410  BUILD_TUPLE_3         3 

 L. 129       412  BUILD_LIST_1          1 
              414  LOAD_FAST                'self'
              416  STORE_ATTR               tile
            418_0  COME_FROM           376  '376'

Parse error at or near `<118>' instruction at offset 64

    def load--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                tile
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               1
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_TRUE     32  'to 32'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                tile
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_STR                 'iptc'
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    44  'to 44'
             32_0  COME_FROM            12  '12'

 L. 136        32  LOAD_GLOBAL              ImageFile
               34  LOAD_ATTR                ImageFile
               36  LOAD_METHOD              load
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'

 L. 138        44  LOAD_FAST                'self'
               46  LOAD_ATTR                tile
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  UNPACK_SEQUENCE_3     3 
               54  STORE_FAST               'type'
               56  STORE_FAST               'tile'
               58  STORE_FAST               'box'

 L. 140        60  LOAD_FAST                'tile'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'encoding'
               66  STORE_FAST               'offset'

 L. 142        68  LOAD_FAST                'self'
               70  LOAD_ATTR                fp
               72  LOAD_METHOD              seek
               74  LOAD_FAST                'offset'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 145        80  LOAD_GLOBAL              tempfile
               82  LOAD_ATTR                mkstemp
               84  LOAD_CONST               False
               86  LOAD_CONST               ('text',)
               88  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'o_fd'
               94  STORE_FAST               'outfile'

 L. 146        96  LOAD_GLOBAL              os
               98  LOAD_METHOD              fdopen
              100  LOAD_FAST                'o_fd'
              102  CALL_METHOD_1         1  ''
              104  STORE_FAST               'o'

 L. 147       106  LOAD_FAST                'encoding'
              108  LOAD_STR                 'raw'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   130  'to 130'

 L. 150       114  LOAD_FAST                'o'
              116  LOAD_METHOD              write
              118  LOAD_STR                 'P5\n%d %d\n255\n'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                size
              124  BINARY_MODULO    
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM           158  '158'
            130_1  COME_FROM           112  '112'

 L. 152       130  LOAD_FAST                'self'
              132  LOAD_METHOD              field
              134  CALL_METHOD_0         0  ''
              136  UNPACK_SEQUENCE_2     2 
              138  STORE_FAST               'type'
              140  STORE_FAST               'size'

 L. 153       142  LOAD_FAST                'type'
              144  LOAD_CONST               (8, 10)
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_FALSE   152  'to 152'

 L. 154       150  BREAK_LOOP          210  'to 210'
            152_0  COME_FROM           148  '148'

 L. 155       152  LOAD_FAST                'size'
              154  LOAD_CONST               0
              156  COMPARE_OP               >
              158  POP_JUMP_IF_FALSE   130  'to 130'

 L. 156       160  LOAD_FAST                'self'
              162  LOAD_ATTR                fp
              164  LOAD_METHOD              read
              166  LOAD_GLOBAL              min
              168  LOAD_FAST                'size'
              170  LOAD_CONST               8192
              172  CALL_FUNCTION_2       2  ''
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               's'

 L. 157       178  LOAD_FAST                's'
              180  POP_JUMP_IF_TRUE    184  'to 184'

 L. 158       182  JUMP_BACK           130  'to 130'
            184_0  COME_FROM           180  '180'

 L. 159       184  LOAD_FAST                'o'
              186  LOAD_METHOD              write
              188  LOAD_FAST                's'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 160       194  LOAD_FAST                'size'
              196  LOAD_GLOBAL              len
              198  LOAD_FAST                's'
              200  CALL_FUNCTION_1       1  ''
              202  INPLACE_SUBTRACT 
              204  STORE_FAST               'size'
              206  JUMP_BACK           152  'to 152'
              208  JUMP_BACK           130  'to 130'

 L. 161       210  LOAD_FAST                'o'
              212  LOAD_METHOD              close
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          

 L. 163       218  SETUP_FINALLY       320  'to 320'

 L. 164       220  LOAD_GLOBAL              Image
              222  LOAD_METHOD              open
              224  LOAD_FAST                'outfile'
              226  CALL_METHOD_1         1  ''
              228  SETUP_WITH          262  'to 262'
              230  STORE_FAST               '_im'

 L. 165       232  LOAD_FAST                '_im'
              234  LOAD_METHOD              load
              236  CALL_METHOD_0         0  ''
              238  POP_TOP          

 L. 166       240  LOAD_FAST                '_im'
              242  LOAD_ATTR                im
              244  LOAD_FAST                'self'
              246  STORE_ATTR               im
              248  POP_BLOCK        
              250  LOAD_CONST               None
              252  DUP_TOP          
              254  DUP_TOP          
              256  CALL_FUNCTION_3       3  ''
              258  POP_TOP          
              260  JUMP_FORWARD        280  'to 280'
            262_0  COME_FROM_WITH      228  '228'
              262  <49>             
          264_266  POP_JUMP_IF_TRUE    270  'to 270'
              268  <48>             
            270_0  COME_FROM           264  '264'
              270  POP_TOP          
              272  POP_TOP          
              274  POP_TOP          
              276  POP_EXCEPT       
              278  POP_TOP          
            280_0  COME_FROM           260  '260'
              280  POP_BLOCK        

 L. 168       282  SETUP_FINALLY       298  'to 298'

 L. 169       284  LOAD_GLOBAL              os
              286  LOAD_METHOD              unlink
              288  LOAD_FAST                'outfile'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          
              294  POP_BLOCK        
              296  JUMP_FORWARD        318  'to 318'
            298_0  COME_FROM_FINALLY   282  '282'

 L. 170       298  DUP_TOP          
              300  LOAD_GLOBAL              OSError
          302_304  <121>               316  ''
              306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 171       312  POP_EXCEPT       
              314  JUMP_FORWARD        318  'to 318'
              316  <48>             
            318_0  COME_FROM           314  '314'
            318_1  COME_FROM           296  '296'
              318  JUMP_FORWARD        358  'to 358'
            320_0  COME_FROM_FINALLY   218  '218'

 L. 168       320  SETUP_FINALLY       336  'to 336'

 L. 169       322  LOAD_GLOBAL              os
              324  LOAD_METHOD              unlink
              326  LOAD_FAST                'outfile'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  POP_BLOCK        
              334  JUMP_FORWARD        356  'to 356'
            336_0  COME_FROM_FINALLY   320  '320'

 L. 170       336  DUP_TOP          
              338  LOAD_GLOBAL              OSError
          340_342  <121>               354  ''
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 171       350  POP_EXCEPT       
              352  JUMP_FORWARD        356  'to 356'
              354  <48>             
            356_0  COME_FROM           352  '352'
            356_1  COME_FROM           334  '334'
              356  <48>             
            358_0  COME_FROM           318  '318'

Parse error at or near `DUP_TOP' instruction at offset 252


Image.register_open(IptcImageFile.format, IptcImageFile)
Image.register_extension(IptcImageFile.format, '.iim')

def getiptcinfo--- This code section failed: ---

 L. 187         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              io
                6  STORE_FAST               'io'

 L. 189         8  LOAD_CONST               1
               10  LOAD_CONST               ('JpegImagePlugin', 'TiffImagePlugin')
               12  IMPORT_NAME              
               14  IMPORT_FROM              JpegImagePlugin
               16  STORE_FAST               'JpegImagePlugin'
               18  IMPORT_FROM              TiffImagePlugin
               20  STORE_FAST               'TiffImagePlugin'
               22  POP_TOP          

 L. 191        24  LOAD_CONST               None
               26  STORE_FAST               'data'

 L. 193        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'im'
               32  LOAD_GLOBAL              IptcImageFile
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 195        38  LOAD_FAST                'im'
               40  LOAD_ATTR                info
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 197        44  LOAD_GLOBAL              isinstance
               46  LOAD_FAST                'im'
               48  LOAD_FAST                'JpegImagePlugin'
               50  LOAD_ATTR                JpegImageFile
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    84  'to 84'

 L. 199        56  LOAD_FAST                'im'
               58  LOAD_ATTR                info
               60  LOAD_METHOD              get
               62  LOAD_STR                 'photoshop'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'photoshop'

 L. 200        68  LOAD_FAST                'photoshop'
               70  POP_JUMP_IF_FALSE   138  'to 138'

 L. 201        72  LOAD_FAST                'photoshop'
               74  LOAD_METHOD              get
               76  LOAD_CONST               1028
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'data'
               82  JUMP_FORWARD        138  'to 138'
             84_0  COME_FROM            54  '54'

 L. 203        84  LOAD_GLOBAL              isinstance
               86  LOAD_FAST                'im'
               88  LOAD_FAST                'TiffImagePlugin'
               90  LOAD_ATTR                TiffImageFile
               92  CALL_FUNCTION_2       2  ''
               94  POP_JUMP_IF_FALSE   138  'to 138'

 L. 206        96  SETUP_FINALLY       116  'to 116'

 L. 207        98  LOAD_FAST                'im'
              100  LOAD_ATTR                tag
              102  LOAD_ATTR                tagdata
              104  LOAD_FAST                'TiffImagePlugin'
              106  LOAD_ATTR                IPTC_NAA_CHUNK
              108  BINARY_SUBSCR    
              110  STORE_FAST               'data'
              112  POP_BLOCK        
              114  JUMP_FORWARD        138  'to 138'
            116_0  COME_FROM_FINALLY    96  '96'

 L. 208       116  DUP_TOP          
              118  LOAD_GLOBAL              AttributeError
              120  LOAD_GLOBAL              KeyError
              122  BUILD_TUPLE_2         2 
              124  <121>               136  ''
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 209       132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
              136  <48>             
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           114  '114'
            138_2  COME_FROM            94  '94'
            138_3  COME_FROM            82  '82'
            138_4  COME_FROM            70  '70'

 L. 211       138  LOAD_FAST                'data'
              140  LOAD_CONST               None
              142  <117>                 0  ''
              144  POP_JUMP_IF_FALSE   150  'to 150'

 L. 212       146  LOAD_CONST               None
              148  RETURN_VALUE     
            150_0  COME_FROM           144  '144'

 L. 215       150  LOAD_BUILD_CLASS 
              152  LOAD_CODE                <code_object FakeImage>
              154  LOAD_STR                 'FakeImage'
              156  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              158  LOAD_STR                 'FakeImage'
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'FakeImage'

 L. 218       164  LOAD_FAST                'FakeImage'
              166  CALL_FUNCTION_0       0  ''
              168  STORE_FAST               'im'

 L. 219       170  LOAD_GLOBAL              IptcImageFile
              172  LOAD_FAST                'im'
              174  STORE_ATTR               __class__

 L. 222       176  BUILD_MAP_0           0 
              178  LOAD_FAST                'im'
              180  STORE_ATTR               info

 L. 223       182  LOAD_FAST                'io'
              184  LOAD_METHOD              BytesIO
              186  LOAD_FAST                'data'
              188  CALL_METHOD_1         1  ''
              190  LOAD_FAST                'im'
              192  STORE_ATTR               fp

 L. 225       194  SETUP_FINALLY       208  'to 208'

 L. 226       196  LOAD_FAST                'im'
              198  LOAD_METHOD              _open
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          
              204  POP_BLOCK        
              206  JUMP_FORWARD        230  'to 230'
            208_0  COME_FROM_FINALLY   194  '194'

 L. 227       208  DUP_TOP          
              210  LOAD_GLOBAL              IndexError
              212  LOAD_GLOBAL              KeyError
              214  BUILD_TUPLE_2         2 
              216  <121>               228  ''
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 228       224  POP_EXCEPT       
              226  JUMP_FORWARD        230  'to 230'
              228  <48>             
            230_0  COME_FROM           226  '226'
            230_1  COME_FROM           206  '206'

 L. 230       230  LOAD_FAST                'im'
              232  LOAD_ATTR                info
              234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 124