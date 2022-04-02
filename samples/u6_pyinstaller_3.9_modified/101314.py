# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PcxImagePlugin.py
import io, logging
from . import Image, ImageFile, ImagePalette
from ._binary import i16le as i16
from ._binary import o8
from ._binary import o16le as o16
logger = logging.getLogger(__name__)

def _accept--- This code section failed: ---

 L.  40         0  LOAD_FAST                'prefix'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_CONST               10
                8  COMPARE_OP               ==
               10  JUMP_IF_FALSE_OR_POP    22  'to 22'
               12  LOAD_FAST                'prefix'
               14  LOAD_CONST               1
               16  BINARY_SUBSCR    
               18  LOAD_CONST               (0, 2, 3, 5)
               20  <118>                 0  ''
             22_0  COME_FROM            10  '10'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class PcxImageFile(ImageFile.ImageFile):
    format = 'PCX'
    format_description = 'Paintbrush'

    def _open--- This code section failed: ---

 L.  55         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               128
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L.  56        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L.  57        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a PCX file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  60        28  LOAD_GLOBAL              i16
               30  LOAD_FAST                's'
               32  LOAD_CONST               4
               34  CALL_FUNCTION_2       2  ''
               36  LOAD_GLOBAL              i16
               38  LOAD_FAST                's'
               40  LOAD_CONST               6
               42  CALL_FUNCTION_2       2  ''
               44  LOAD_GLOBAL              i16
               46  LOAD_FAST                's'
               48  LOAD_CONST               8
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_CONST               1
               54  BINARY_ADD       
               56  LOAD_GLOBAL              i16
               58  LOAD_FAST                's'
               60  LOAD_CONST               10
               62  CALL_FUNCTION_2       2  ''
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  BUILD_TUPLE_4         4 
               70  STORE_FAST               'bbox'

 L.  61        72  LOAD_FAST                'bbox'
               74  LOAD_CONST               2
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'bbox'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  COMPARE_OP               <=
               86  POP_JUMP_IF_TRUE    104  'to 104'
               88  LOAD_FAST                'bbox'
               90  LOAD_CONST               3
               92  BINARY_SUBSCR    
               94  LOAD_FAST                'bbox'
               96  LOAD_CONST               1
               98  BINARY_SUBSCR    
              100  COMPARE_OP               <=
              102  POP_JUMP_IF_FALSE   112  'to 112'
            104_0  COME_FROM            86  '86'

 L.  62       104  LOAD_GLOBAL              SyntaxError
              106  LOAD_STR                 'bad PCX image size'
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           102  '102'

 L.  63       112  LOAD_GLOBAL              logger
              114  LOAD_ATTR                debug
              116  LOAD_STR                 'BBox: %s %s %s %s'
              118  BUILD_LIST_1          1 
              120  LOAD_FAST                'bbox'
              122  CALL_FINALLY        125  'to 125'
              124  WITH_CLEANUP_FINISH
              126  CALL_FUNCTION_EX      0  'positional arguments only'
              128  POP_TOP          

 L.  66       130  LOAD_FAST                's'
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  STORE_FAST               'version'

 L.  67       138  LOAD_FAST                's'
              140  LOAD_CONST               3
              142  BINARY_SUBSCR    
              144  STORE_FAST               'bits'

 L.  68       146  LOAD_FAST                's'
              148  LOAD_CONST               65
              150  BINARY_SUBSCR    
              152  STORE_FAST               'planes'

 L.  69       154  LOAD_GLOBAL              i16
              156  LOAD_FAST                's'
              158  LOAD_CONST               66
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'ignored_stride'

 L.  70       164  LOAD_GLOBAL              logger
              166  LOAD_METHOD              debug

 L.  71       168  LOAD_STR                 'PCX version %s, bits %s, planes %s, stride %s'

 L.  72       170  LOAD_FAST                'version'

 L.  73       172  LOAD_FAST                'bits'

 L.  74       174  LOAD_FAST                'planes'

 L.  75       176  LOAD_FAST                'ignored_stride'

 L.  70       178  CALL_METHOD_5         5  ''
              180  POP_TOP          

 L.  78       182  LOAD_GLOBAL              i16
              184  LOAD_FAST                's'
              186  LOAD_CONST               12
              188  CALL_FUNCTION_2       2  ''
              190  LOAD_GLOBAL              i16
              192  LOAD_FAST                's'
              194  LOAD_CONST               14
              196  CALL_FUNCTION_2       2  ''
              198  BUILD_TUPLE_2         2 
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                info
              204  LOAD_STR                 'dpi'
              206  STORE_SUBSCR     

 L.  80       208  LOAD_FAST                'bits'
              210  LOAD_CONST               1
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   236  'to 236'
              216  LOAD_FAST                'planes'
              218  LOAD_CONST               1
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   236  'to 236'

 L.  81       224  LOAD_STR                 '1'
              226  DUP_TOP          
              228  STORE_FAST               'mode'
              230  STORE_FAST               'rawmode'
          232_234  JUMP_FORWARD        554  'to 554'
            236_0  COME_FROM           222  '222'
            236_1  COME_FROM           214  '214'

 L.  83       236  LOAD_FAST                'bits'
              238  LOAD_CONST               1
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   294  'to 294'
              246  LOAD_FAST                'planes'
              248  LOAD_CONST               (2, 4)
              250  <118>                 0  ''
          252_254  POP_JUMP_IF_FALSE   294  'to 294'

 L.  84       256  LOAD_STR                 'P'
              258  STORE_FAST               'mode'

 L.  85       260  LOAD_STR                 'P;%dL'
              262  LOAD_FAST                'planes'
              264  BINARY_MODULO    
              266  STORE_FAST               'rawmode'

 L.  86       268  LOAD_GLOBAL              ImagePalette
              270  LOAD_METHOD              raw
              272  LOAD_STR                 'RGB'
              274  LOAD_FAST                's'
              276  LOAD_CONST               16
              278  LOAD_CONST               64
              280  BUILD_SLICE_2         2 
              282  BINARY_SUBSCR    
              284  CALL_METHOD_2         2  ''
              286  LOAD_FAST                'self'
              288  STORE_ATTR               palette
          290_292  JUMP_FORWARD        554  'to 554'
            294_0  COME_FROM           252  '252'
            294_1  COME_FROM           242  '242'

 L.  88       294  LOAD_FAST                'version'
              296  LOAD_CONST               5
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   506  'to 506'
              304  LOAD_FAST                'bits'
              306  LOAD_CONST               8
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   506  'to 506'
              314  LOAD_FAST                'planes'
              316  LOAD_CONST               1
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   506  'to 506'

 L.  89       324  LOAD_STR                 'L'
              326  DUP_TOP          
              328  STORE_FAST               'mode'
              330  STORE_FAST               'rawmode'

 L.  91       332  LOAD_FAST                'self'
              334  LOAD_ATTR                fp
              336  LOAD_METHOD              seek
              338  LOAD_CONST               -769
              340  LOAD_GLOBAL              io
              342  LOAD_ATTR                SEEK_END
              344  CALL_METHOD_2         2  ''
              346  POP_TOP          

 L.  92       348  LOAD_FAST                'self'
              350  LOAD_ATTR                fp
              352  LOAD_METHOD              read
              354  LOAD_CONST               769
              356  CALL_METHOD_1         1  ''
              358  STORE_FAST               's'

 L.  93       360  LOAD_GLOBAL              len
              362  LOAD_FAST                's'
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_CONST               769
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   492  'to 492'
              374  LOAD_FAST                's'
              376  LOAD_CONST               0
              378  BINARY_SUBSCR    
              380  LOAD_CONST               12
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   492  'to 492'

 L.  95       388  LOAD_GLOBAL              range
              390  LOAD_CONST               256
              392  CALL_FUNCTION_1       1  ''
              394  GET_ITER         
            396_0  COME_FROM           438  '438'
              396  FOR_ITER            460  'to 460'
              398  STORE_FAST               'i'

 L.  96       400  LOAD_FAST                's'
              402  LOAD_FAST                'i'
              404  LOAD_CONST               3
              406  BINARY_MULTIPLY  
              408  LOAD_CONST               1
              410  BINARY_ADD       
              412  LOAD_FAST                'i'
              414  LOAD_CONST               3
              416  BINARY_MULTIPLY  
              418  LOAD_CONST               4
              420  BINARY_ADD       
              422  BUILD_SLICE_2         2 
              424  BINARY_SUBSCR    
              426  LOAD_GLOBAL              o8
              428  LOAD_FAST                'i'
              430  CALL_FUNCTION_1       1  ''
              432  LOAD_CONST               3
              434  BINARY_MULTIPLY  
              436  COMPARE_OP               !=
          438_440  POP_JUMP_IF_FALSE   396  'to 396'

 L.  97       442  LOAD_STR                 'P'
              444  DUP_TOP          
              446  STORE_FAST               'mode'
              448  STORE_FAST               'rawmode'

 L.  98       450  POP_TOP          
          452_454  BREAK_LOOP          460  'to 460'
          456_458  JUMP_BACK           396  'to 396'

 L.  99       460  LOAD_FAST                'mode'
              462  LOAD_STR                 'P'
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   492  'to 492'

 L. 100       470  LOAD_GLOBAL              ImagePalette
              472  LOAD_METHOD              raw
              474  LOAD_STR                 'RGB'
              476  LOAD_FAST                's'
              478  LOAD_CONST               1
              480  LOAD_CONST               None
              482  BUILD_SLICE_2         2 
              484  BINARY_SUBSCR    
              486  CALL_METHOD_2         2  ''
              488  LOAD_FAST                'self'
              490  STORE_ATTR               palette
            492_0  COME_FROM           466  '466'
            492_1  COME_FROM           384  '384'
            492_2  COME_FROM           370  '370'

 L. 101       492  LOAD_FAST                'self'
              494  LOAD_ATTR                fp
              496  LOAD_METHOD              seek
              498  LOAD_CONST               128
              500  CALL_METHOD_1         1  ''
              502  POP_TOP          
              504  JUMP_FORWARD        554  'to 554'
            506_0  COME_FROM           320  '320'
            506_1  COME_FROM           310  '310'
            506_2  COME_FROM           300  '300'

 L. 103       506  LOAD_FAST                'version'
              508  LOAD_CONST               5
              510  COMPARE_OP               ==
          512_514  POP_JUMP_IF_FALSE   546  'to 546'
              516  LOAD_FAST                'bits'
              518  LOAD_CONST               8
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   546  'to 546'
              526  LOAD_FAST                'planes'
              528  LOAD_CONST               3
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   546  'to 546'

 L. 104       536  LOAD_STR                 'RGB'
              538  STORE_FAST               'mode'

 L. 105       540  LOAD_STR                 'RGB;L'
              542  STORE_FAST               'rawmode'
              544  JUMP_FORWARD        554  'to 554'
            546_0  COME_FROM           532  '532'
            546_1  COME_FROM           522  '522'
            546_2  COME_FROM           512  '512'

 L. 108       546  LOAD_GLOBAL              OSError
              548  LOAD_STR                 'unknown PCX mode'
              550  CALL_FUNCTION_1       1  ''
              552  RAISE_VARARGS_1       1  'exception instance'
            554_0  COME_FROM           544  '544'
            554_1  COME_FROM           504  '504'
            554_2  COME_FROM           290  '290'
            554_3  COME_FROM           232  '232'

 L. 110       554  LOAD_FAST                'mode'
              556  LOAD_FAST                'self'
              558  STORE_ATTR               mode

 L. 111       560  LOAD_FAST                'bbox'
              562  LOAD_CONST               2
              564  BINARY_SUBSCR    
              566  LOAD_FAST                'bbox'
              568  LOAD_CONST               0
              570  BINARY_SUBSCR    
              572  BINARY_SUBTRACT  
              574  LOAD_FAST                'bbox'
              576  LOAD_CONST               3
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'bbox'
              582  LOAD_CONST               1
              584  BINARY_SUBSCR    
              586  BINARY_SUBTRACT  
              588  BUILD_TUPLE_2         2 
              590  LOAD_FAST                'self'
              592  STORE_ATTR               _size

 L. 115       594  LOAD_FAST                'self'
              596  LOAD_ATTR                _size
              598  LOAD_CONST               0
              600  BINARY_SUBSCR    
              602  LOAD_FAST                'bits'
              604  BINARY_MULTIPLY  
              606  LOAD_CONST               7
              608  BINARY_ADD       
              610  LOAD_CONST               8
              612  BINARY_FLOOR_DIVIDE
              614  STORE_FAST               'stride'

 L. 116       616  LOAD_FAST                'stride'
              618  LOAD_FAST                'stride'
              620  LOAD_CONST               2
              622  BINARY_MODULO    
              624  INPLACE_ADD      
              626  STORE_FAST               'stride'

 L. 118       628  LOAD_CONST               (0, 0)
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                size
              634  BINARY_ADD       
              636  STORE_FAST               'bbox'

 L. 119       638  LOAD_GLOBAL              logger
              640  LOAD_ATTR                debug
              642  LOAD_STR                 'size: %sx%s'
              644  BUILD_LIST_1          1 
              646  LOAD_FAST                'self'
              648  LOAD_ATTR                size
              650  CALL_FINALLY        653  'to 653'
              652  WITH_CLEANUP_FINISH
              654  CALL_FUNCTION_EX      0  'positional arguments only'
              656  POP_TOP          

 L. 121       658  LOAD_STR                 'pcx'
              660  LOAD_FAST                'bbox'
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                fp
              666  LOAD_METHOD              tell
              668  CALL_METHOD_0         0  ''
              670  LOAD_FAST                'rawmode'
              672  LOAD_FAST                'planes'
              674  LOAD_FAST                'stride'
              676  BINARY_MULTIPLY  
              678  BUILD_TUPLE_2         2 
              680  BUILD_TUPLE_4         4 
              682  BUILD_LIST_1          1 
              684  LOAD_FAST                'self'
              686  STORE_ATTR               tile

Parse error at or near `CALL_FINALLY' instruction at offset 122


SAVE = {'1':(2, 1, 1, '1'), 
 'L':(5, 8, 1, 'L'), 
 'P':(5, 8, 1, 'P'), 
 'RGB':(5, 8, 3, 'RGB;L')}

def _save--- This code section failed: ---

 L. 139         0  SETUP_FINALLY        24  'to 24'

 L. 140         2  LOAD_GLOBAL              SAVE
                4  LOAD_FAST                'im'
                6  LOAD_ATTR                mode
                8  BINARY_SUBSCR    
               10  UNPACK_SEQUENCE_4     4 
               12  STORE_FAST               'version'
               14  STORE_FAST               'bits'
               16  STORE_FAST               'planes'
               18  STORE_FAST               'rawmode'
               20  POP_BLOCK        
               22  JUMP_FORWARD         80  'to 80'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 141        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  <121>                78  ''
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        70  'to 70'

 L. 142        38  LOAD_GLOBAL              ValueError
               40  LOAD_STR                 'Cannot save '
               42  LOAD_FAST                'im'
               44  LOAD_ATTR                mode
               46  FORMAT_VALUE          0  ''
               48  LOAD_STR                 ' images as PCX'
               50  BUILD_STRING_3        3 
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_FAST                'e'
               56  RAISE_VARARGS_2       2  'exception instance with __cause__'
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  STORE_FAST               'e'
               66  DELETE_FAST              'e'
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_FINALLY    36  '36'
               70  LOAD_CONST               None
               72  STORE_FAST               'e'
               74  DELETE_FAST              'e'
               76  <48>             
               78  <48>             
             80_0  COME_FROM            68  '68'
             80_1  COME_FROM            22  '22'

 L. 145        80  LOAD_FAST                'im'
               82  LOAD_ATTR                size
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'bits'
               90  BINARY_MULTIPLY  
               92  LOAD_CONST               7
               94  BINARY_ADD       
               96  LOAD_CONST               8
               98  BINARY_FLOOR_DIVIDE
              100  STORE_FAST               'stride'

 L. 147       102  LOAD_FAST                'stride'
              104  LOAD_FAST                'stride'
              106  LOAD_CONST               2
              108  BINARY_MODULO    
              110  INPLACE_ADD      
              112  STORE_FAST               'stride'

 L. 152       114  LOAD_GLOBAL              logger
              116  LOAD_METHOD              debug

 L. 153       118  LOAD_STR                 'PcxImagePlugin._save: xwidth: %d, bits: %d, stride: %d'

 L. 154       120  LOAD_FAST                'im'
              122  LOAD_ATTR                size
              124  LOAD_CONST               0
              126  BINARY_SUBSCR    

 L. 155       128  LOAD_FAST                'bits'

 L. 156       130  LOAD_FAST                'stride'

 L. 152       132  CALL_METHOD_4         4  ''
              134  POP_TOP          

 L. 162       136  LOAD_FAST                'im'
              138  LOAD_ATTR                size
              140  STORE_FAST               'screen'

 L. 164       142  LOAD_CONST               (100, 100)
              144  STORE_FAST               'dpi'

 L. 167       146  LOAD_FAST                'fp'
              148  LOAD_METHOD              write

 L. 168       150  LOAD_GLOBAL              o8
              152  LOAD_CONST               10
              154  CALL_FUNCTION_1       1  ''

 L. 169       156  LOAD_GLOBAL              o8
              158  LOAD_FAST                'version'
              160  CALL_FUNCTION_1       1  ''

 L. 168       162  BINARY_ADD       

 L. 170       164  LOAD_GLOBAL              o8
              166  LOAD_CONST               1
              168  CALL_FUNCTION_1       1  ''

 L. 168       170  BINARY_ADD       

 L. 171       172  LOAD_GLOBAL              o8
              174  LOAD_FAST                'bits'
              176  CALL_FUNCTION_1       1  ''

 L. 168       178  BINARY_ADD       

 L. 172       180  LOAD_GLOBAL              o16
              182  LOAD_CONST               0
              184  CALL_FUNCTION_1       1  ''

 L. 168       186  BINARY_ADD       

 L. 173       188  LOAD_GLOBAL              o16
              190  LOAD_CONST               0
              192  CALL_FUNCTION_1       1  ''

 L. 168       194  BINARY_ADD       

 L. 174       196  LOAD_GLOBAL              o16
              198  LOAD_FAST                'im'
              200  LOAD_ATTR                size
              202  LOAD_CONST               0
              204  BINARY_SUBSCR    
              206  LOAD_CONST               1
              208  BINARY_SUBTRACT  
              210  CALL_FUNCTION_1       1  ''

 L. 168       212  BINARY_ADD       

 L. 175       214  LOAD_GLOBAL              o16
              216  LOAD_FAST                'im'
              218  LOAD_ATTR                size
              220  LOAD_CONST               1
              222  BINARY_SUBSCR    
              224  LOAD_CONST               1
              226  BINARY_SUBTRACT  
              228  CALL_FUNCTION_1       1  ''

 L. 168       230  BINARY_ADD       

 L. 176       232  LOAD_GLOBAL              o16
              234  LOAD_FAST                'dpi'
              236  LOAD_CONST               0
              238  BINARY_SUBSCR    
              240  CALL_FUNCTION_1       1  ''

 L. 168       242  BINARY_ADD       

 L. 177       244  LOAD_GLOBAL              o16
              246  LOAD_FAST                'dpi'
              248  LOAD_CONST               1
              250  BINARY_SUBSCR    
              252  CALL_FUNCTION_1       1  ''

 L. 168       254  BINARY_ADD       

 L. 178       256  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

 L. 168       258  BINARY_ADD       

 L. 179       260  LOAD_CONST               b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

 L. 168       262  BINARY_ADD       

 L. 180       264  LOAD_CONST               b'\x00'

 L. 168       266  BINARY_ADD       

 L. 181       268  LOAD_GLOBAL              o8
              270  LOAD_FAST                'planes'
              272  CALL_FUNCTION_1       1  ''

 L. 168       274  BINARY_ADD       

 L. 182       276  LOAD_GLOBAL              o16
              278  LOAD_FAST                'stride'
              280  CALL_FUNCTION_1       1  ''

 L. 168       282  BINARY_ADD       

 L. 183       284  LOAD_GLOBAL              o16
              286  LOAD_CONST               1
              288  CALL_FUNCTION_1       1  ''

 L. 168       290  BINARY_ADD       

 L. 184       292  LOAD_GLOBAL              o16
              294  LOAD_FAST                'screen'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  CALL_FUNCTION_1       1  ''

 L. 168       302  BINARY_ADD       

 L. 185       304  LOAD_GLOBAL              o16
              306  LOAD_FAST                'screen'
              308  LOAD_CONST               1
              310  BINARY_SUBSCR    
              312  CALL_FUNCTION_1       1  ''

 L. 168       314  BINARY_ADD       

 L. 186       316  LOAD_CONST               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

 L. 168       318  BINARY_ADD       

 L. 167       320  CALL_METHOD_1         1  ''
              322  POP_TOP          

 L. 189       324  LOAD_FAST                'fp'
              326  LOAD_METHOD              tell
              328  CALL_METHOD_0         0  ''
              330  LOAD_CONST               128
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_TRUE    342  'to 342'
              338  <74>             
              340  RAISE_VARARGS_1       1  'exception instance'
            342_0  COME_FROM           334  '334'

 L. 191       342  LOAD_GLOBAL              ImageFile
              344  LOAD_METHOD              _save
              346  LOAD_FAST                'im'
              348  LOAD_FAST                'fp'
              350  LOAD_STR                 'pcx'
              352  LOAD_CONST               (0, 0)
              354  LOAD_FAST                'im'
              356  LOAD_ATTR                size
              358  BINARY_ADD       
              360  LOAD_CONST               0
              362  LOAD_FAST                'rawmode'
              364  LOAD_FAST                'bits'
              366  LOAD_FAST                'planes'
              368  BINARY_MULTIPLY  
              370  BUILD_TUPLE_2         2 
              372  BUILD_TUPLE_4         4 
              374  BUILD_LIST_1          1 
              376  CALL_METHOD_3         3  ''
              378  POP_TOP          

 L. 193       380  LOAD_FAST                'im'
              382  LOAD_ATTR                mode
              384  LOAD_STR                 'P'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   428  'to 428'

 L. 195       392  LOAD_FAST                'fp'
              394  LOAD_METHOD              write
              396  LOAD_GLOBAL              o8
              398  LOAD_CONST               12
              400  CALL_FUNCTION_1       1  ''
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          

 L. 196       406  LOAD_FAST                'fp'
              408  LOAD_METHOD              write
              410  LOAD_FAST                'im'
              412  LOAD_ATTR                im
              414  LOAD_METHOD              getpalette
              416  LOAD_STR                 'RGB'
              418  LOAD_STR                 'RGB'
              420  CALL_METHOD_2         2  ''
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          
              426  JUMP_FORWARD        488  'to 488'
            428_0  COME_FROM           388  '388'

 L. 197       428  LOAD_FAST                'im'
              430  LOAD_ATTR                mode
              432  LOAD_STR                 'L'
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   488  'to 488'

 L. 199       440  LOAD_FAST                'fp'
              442  LOAD_METHOD              write
              444  LOAD_GLOBAL              o8
              446  LOAD_CONST               12
              448  CALL_FUNCTION_1       1  ''
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          

 L. 200       454  LOAD_GLOBAL              range
              456  LOAD_CONST               256
              458  CALL_FUNCTION_1       1  ''
              460  GET_ITER         
              462  FOR_ITER            488  'to 488'
              464  STORE_FAST               'i'

 L. 201       466  LOAD_FAST                'fp'
              468  LOAD_METHOD              write
              470  LOAD_GLOBAL              o8
              472  LOAD_FAST                'i'
              474  CALL_FUNCTION_1       1  ''
              476  LOAD_CONST               3
              478  BINARY_MULTIPLY  
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
          484_486  JUMP_BACK           462  'to 462'
            488_0  COME_FROM           436  '436'
            488_1  COME_FROM           426  '426'

Parse error at or near `<121>' instruction at offset 28


Image.register_open(PcxImageFile.format, PcxImageFile, _accept)
Image.register_save(PcxImageFile.format, _save)
Image.register_extension(PcxImageFile.format, '.pcx')
Image.register_mime(PcxImageFile.format, 'image/x-pcx')