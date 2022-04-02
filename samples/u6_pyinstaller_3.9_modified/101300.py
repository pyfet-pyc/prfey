# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImImagePlugin.py
import os, re
from . import Image, ImageFile, ImagePalette
COMMENT = 'Comment'
DATE = 'Date'
EQUIPMENT = 'Digitalization equipment'
FRAMES = 'File size (no of images)'
LUT = 'Lut'
NAME = 'Name'
SCALE = 'Scale (x,y)'
SIZE = 'Image size (x*y)'
MODE = 'Image type'
TAGS = {COMMENT: 0, 
 DATE: 0, 
 EQUIPMENT: 0, 
 FRAMES: 0, 
 LUT: 0, 
 NAME: 0, 
 SCALE: 0, 
 SIZE: 0, 
 MODE: 0}
OPEN = {'0 1 image':('1', '1'), 
 'L 1 image':('1', '1'), 
 'Greyscale image':('L', 'L'), 
 'Grayscale image':('L', 'L'), 
 'RGB image':('RGB', 'RGB;L'), 
 'RLB image':('RGB', 'RLB'), 
 'RYB image':('RGB', 'RLB'), 
 'B1 image':('1', '1'), 
 'B2 image':('P', 'P;2'), 
 'B4 image':('P', 'P;4'), 
 'X 24 image':('RGB', 'RGB'), 
 'L 32 S image':('I', 'I;32'), 
 'L 32 F image':('F', 'F;32'), 
 'RGB3 image':('RGB', 'RGB;T'), 
 'RYB3 image':('RGB', 'RYB;T'), 
 'LA image':('LA', 'LA;L'), 
 'PA image':('LA', 'PA;L'), 
 'RGBA image':('RGBA', 'RGBA;L'), 
 'RGBX image':('RGBX', 'RGBX;L'), 
 'CMYK image':('CMYK', 'CMYK;L'), 
 'YCC image':('YCbCr', 'YCbCr;L')}
for i in ('8', '8S', '16', '16S', '32', '32F'):
    OPEN[f"L {i} image"] = (
     'F', f"F;{i}")
    OPEN[f"L*{i} image"] = ('F', f"F;{i}")
else:
    for i in ('16', '16L', '16B'):
        OPEN[f"L {i} image"] = (
         f"I;{i}", f"I;{i}")
        OPEN[f"L*{i} image"] = (f"I;{i}", f"I;{i}")
    else:
        for i in ('32S', ):
            OPEN[f"L {i} image"] = (
             'I', f"I;{i}")
            OPEN[f"L*{i} image"] = ('I', f"I;{i}")
        else:
            for i in range(2, 33):
                OPEN[f"L*{i} image"] = (
                 'F', f"F;{i}")
            else:
                split = re.compile(b'^([A-Za-z][^:]*):[ \\t]*(.*)[ \\t]*$')

                def number--- This code section failed: ---

 L. 107         0  SETUP_FINALLY        12  'to 12'

 L. 108         2  LOAD_GLOBAL              int
                4  LOAD_FAST                's'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 109        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  <121>                36  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 110        24  LOAD_GLOBAL              float
               26  LOAD_FAST                's'
               28  CALL_FUNCTION_1       1  ''
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
               36  <48>             

Parse error at or near `<121>' instruction at offset 16


                class ImImageFile(ImageFile.ImageFile):
                    format = 'IM'
                    format_description = 'IFUNC Image Memory'
                    _close_exclusive_fp_after_loading = False

                    def _open--- This code section failed: ---

 L. 128         0  LOAD_CONST               b'\n'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               100
               10  CALL_METHOD_1         1  ''
               12  <118>                 1  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 129        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not an IM file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 130        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              seek
               30  LOAD_CONST               0
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 132        36  LOAD_CONST               0
               38  STORE_FAST               'n'

 L. 135        40  LOAD_STR                 'L'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                info
               46  LOAD_GLOBAL              MODE
               48  STORE_SUBSCR     

 L. 136        50  LOAD_CONST               (512, 512)
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                info
               56  LOAD_GLOBAL              SIZE
               58  STORE_SUBSCR     

 L. 137        60  LOAD_CONST               1
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                info
               66  LOAD_GLOBAL              FRAMES
               68  STORE_SUBSCR     

 L. 139        70  LOAD_STR                 'L'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               rawmode

 L. 143        76  LOAD_FAST                'self'
               78  LOAD_ATTR                fp
               80  LOAD_METHOD              read
               82  LOAD_CONST               1
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               's'

 L. 146        88  LOAD_FAST                's'
               90  LOAD_CONST               b'\r'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 147        96  JUMP_BACK            76  'to 76'
             98_0  COME_FROM            94  '94'

 L. 149        98  LOAD_FAST                's'
              100  POP_JUMP_IF_FALSE   118  'to 118'
              102  LOAD_FAST                's'
              104  LOAD_CONST               b'\x00'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_TRUE    118  'to 118'
              110  LOAD_FAST                's'
              112  LOAD_CONST               b'\x1a'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   122  'to 122'
            118_0  COME_FROM           108  '108'
            118_1  COME_FROM           100  '100'

 L. 150   118_120  BREAK_LOOP          538  'to 538'
            122_0  COME_FROM           116  '116'

 L. 153       122  LOAD_FAST                's'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                fp
              128  LOAD_METHOD              readline
              130  CALL_METHOD_0         0  ''
              132  BINARY_ADD       
              134  STORE_FAST               's'

 L. 155       136  LOAD_GLOBAL              len
              138  LOAD_FAST                's'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               100
              144  COMPARE_OP               >
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L. 156       148  LOAD_GLOBAL              SyntaxError
              150  LOAD_STR                 'not an IM file'
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           146  '146'

 L. 158       156  LOAD_FAST                's'
              158  LOAD_CONST               -2
              160  LOAD_CONST               None
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  LOAD_CONST               b'\r\n'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   186  'to 186'

 L. 159       172  LOAD_FAST                's'
              174  LOAD_CONST               None
              176  LOAD_CONST               -2
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  STORE_FAST               's'
              184  JUMP_FORWARD        214  'to 214'
            186_0  COME_FROM           170  '170'

 L. 160       186  LOAD_FAST                's'
              188  LOAD_CONST               -1
              190  LOAD_CONST               None
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  LOAD_CONST               b'\n'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 161       202  LOAD_FAST                's'
              204  LOAD_CONST               None
              206  LOAD_CONST               -1
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_FAST               's'
            214_0  COME_FROM           200  '200'
            214_1  COME_FROM           184  '184'

 L. 163       214  SETUP_FINALLY       230  'to 230'

 L. 164       216  LOAD_GLOBAL              split
              218  LOAD_METHOD              match
              220  LOAD_FAST                's'
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'm'
              226  POP_BLOCK        
              228  JUMP_FORWARD        280  'to 280'
            230_0  COME_FROM_FINALLY   214  '214'

 L. 165       230  DUP_TOP          
              232  LOAD_GLOBAL              re
              234  LOAD_ATTR                error
          236_238  <121>               278  ''
              240  POP_TOP          
              242  STORE_FAST               'e'
              244  POP_TOP          
              246  SETUP_FINALLY       270  'to 270'

 L. 166       248  LOAD_GLOBAL              SyntaxError
              250  LOAD_STR                 'not an IM file'
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_FAST                'e'
              256  RAISE_VARARGS_2       2  'exception instance with __cause__'
              258  POP_BLOCK        
              260  POP_EXCEPT       
              262  LOAD_CONST               None
              264  STORE_FAST               'e'
              266  DELETE_FAST              'e'
              268  JUMP_FORWARD        280  'to 280'
            270_0  COME_FROM_FINALLY   246  '246'
              270  LOAD_CONST               None
              272  STORE_FAST               'e'
              274  DELETE_FAST              'e'
              276  <48>             
              278  <48>             
            280_0  COME_FROM           268  '268'
            280_1  COME_FROM           228  '228'

 L. 168       280  LOAD_FAST                'm'
          282_284  POP_JUMP_IF_FALSE   516  'to 516'

 L. 170       286  LOAD_FAST                'm'
              288  LOAD_METHOD              group
              290  LOAD_CONST               1
              292  LOAD_CONST               2
              294  CALL_METHOD_2         2  ''
              296  UNPACK_SEQUENCE_2     2 
              298  STORE_FAST               'k'
              300  STORE_FAST               'v'

 L. 174       302  LOAD_FAST                'k'
              304  LOAD_METHOD              decode
              306  LOAD_STR                 'latin-1'
              308  LOAD_STR                 'replace'
              310  CALL_METHOD_2         2  ''
              312  STORE_FAST               'k'

 L. 175       314  LOAD_FAST                'v'
              316  LOAD_METHOD              decode
              318  LOAD_STR                 'latin-1'
              320  LOAD_STR                 'replace'
              322  CALL_METHOD_2         2  ''
              324  STORE_FAST               'v'

 L. 178       326  LOAD_FAST                'k'
              328  LOAD_GLOBAL              FRAMES
              330  LOAD_GLOBAL              SCALE
              332  LOAD_GLOBAL              SIZE
              334  BUILD_TUPLE_3         3 
              336  <118>                 0  ''
          338_340  POP_JUMP_IF_FALSE   398  'to 398'

 L. 179       342  LOAD_FAST                'v'
              344  LOAD_METHOD              replace
              346  LOAD_STR                 '*'
              348  LOAD_STR                 ','
              350  CALL_METHOD_2         2  ''
              352  STORE_FAST               'v'

 L. 180       354  LOAD_GLOBAL              tuple
              356  LOAD_GLOBAL              map
              358  LOAD_GLOBAL              number
              360  LOAD_FAST                'v'
              362  LOAD_METHOD              split
              364  LOAD_STR                 ','
              366  CALL_METHOD_1         1  ''
              368  CALL_FUNCTION_2       2  ''
              370  CALL_FUNCTION_1       1  ''
              372  STORE_FAST               'v'

 L. 181       374  LOAD_GLOBAL              len
              376  LOAD_FAST                'v'
              378  CALL_FUNCTION_1       1  ''
              380  LOAD_CONST               1
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   432  'to 432'

 L. 182       388  LOAD_FAST                'v'
              390  LOAD_CONST               0
              392  BINARY_SUBSCR    
              394  STORE_FAST               'v'
              396  JUMP_FORWARD        432  'to 432'
            398_0  COME_FROM           338  '338'

 L. 183       398  LOAD_FAST                'k'
              400  LOAD_GLOBAL              MODE
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   432  'to 432'
              408  LOAD_FAST                'v'
              410  LOAD_GLOBAL              OPEN
              412  <118>                 0  ''
          414_416  POP_JUMP_IF_FALSE   432  'to 432'

 L. 184       418  LOAD_GLOBAL              OPEN
              420  LOAD_FAST                'v'
              422  BINARY_SUBSCR    
              424  UNPACK_SEQUENCE_2     2 
              426  STORE_FAST               'v'
              428  LOAD_FAST                'self'
              430  STORE_ATTR               rawmode
            432_0  COME_FROM           414  '414'
            432_1  COME_FROM           404  '404'
            432_2  COME_FROM           396  '396'
            432_3  COME_FROM           384  '384'

 L. 188       432  LOAD_FAST                'k'
              434  LOAD_GLOBAL              COMMENT
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   486  'to 486'

 L. 189       442  LOAD_FAST                'k'
              444  LOAD_FAST                'self'
              446  LOAD_ATTR                info
              448  <118>                 0  ''
          450_452  POP_JUMP_IF_FALSE   472  'to 472'

 L. 190       454  LOAD_FAST                'self'
              456  LOAD_ATTR                info
              458  LOAD_FAST                'k'
              460  BINARY_SUBSCR    
              462  LOAD_METHOD              append
              464  LOAD_FAST                'v'
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
              470  JUMP_FORWARD        484  'to 484'
            472_0  COME_FROM           450  '450'

 L. 192       472  LOAD_FAST                'v'
              474  BUILD_LIST_1          1 
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                info
              480  LOAD_FAST                'k'
              482  STORE_SUBSCR     
            484_0  COME_FROM           470  '470'
              484  JUMP_FORWARD        496  'to 496'
            486_0  COME_FROM           438  '438'

 L. 194       486  LOAD_FAST                'v'
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                info
              492  LOAD_FAST                'k'
              494  STORE_SUBSCR     
            496_0  COME_FROM           484  '484'

 L. 196       496  LOAD_FAST                'k'
              498  LOAD_GLOBAL              TAGS
              500  <118>                 0  ''
          502_504  POP_JUMP_IF_FALSE   536  'to 536'

 L. 197       506  LOAD_FAST                'n'
              508  LOAD_CONST               1
              510  INPLACE_ADD      
              512  STORE_FAST               'n'
              514  JUMP_BACK            76  'to 76'
            516_0  COME_FROM           282  '282'

 L. 201       516  LOAD_GLOBAL              SyntaxError

 L. 202       518  LOAD_STR                 'Syntax error in IM header: '
              520  LOAD_FAST                's'
              522  LOAD_METHOD              decode
              524  LOAD_STR                 'ascii'
              526  LOAD_STR                 'replace'
              528  CALL_METHOD_2         2  ''
              530  BINARY_ADD       

 L. 201       532  CALL_FUNCTION_1       1  ''
              534  RAISE_VARARGS_1       1  'exception instance'
            536_0  COME_FROM           502  '502'
              536  JUMP_BACK            76  'to 76'

 L. 205       538  LOAD_FAST                'n'
          540_542  POP_JUMP_IF_TRUE    552  'to 552'

 L. 206       544  LOAD_GLOBAL              SyntaxError
              546  LOAD_STR                 'Not an IM file'
              548  CALL_FUNCTION_1       1  ''
              550  RAISE_VARARGS_1       1  'exception instance'
            552_0  COME_FROM           540  '540'

 L. 209       552  LOAD_FAST                'self'
              554  LOAD_ATTR                info
              556  LOAD_GLOBAL              SIZE
              558  BINARY_SUBSCR    
              560  LOAD_FAST                'self'
              562  STORE_ATTR               _size

 L. 210       564  LOAD_FAST                'self'
              566  LOAD_ATTR                info
              568  LOAD_GLOBAL              MODE
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'self'
              574  STORE_ATTR               mode

 L. 213       576  LOAD_FAST                's'
          578_580  POP_JUMP_IF_FALSE   616  'to 616'
              582  LOAD_FAST                's'
              584  LOAD_CONST               0
              586  LOAD_CONST               1
              588  BUILD_SLICE_2         2 
              590  BINARY_SUBSCR    
              592  LOAD_CONST               b'\x1a'
              594  COMPARE_OP               !=
          596_598  POP_JUMP_IF_FALSE   616  'to 616'

 L. 214       600  LOAD_FAST                'self'
              602  LOAD_ATTR                fp
              604  LOAD_METHOD              read
              606  LOAD_CONST               1
              608  CALL_METHOD_1         1  ''
              610  STORE_FAST               's'
          612_614  JUMP_BACK           576  'to 576'
            616_0  COME_FROM           596  '596'
            616_1  COME_FROM           578  '578'

 L. 215       616  LOAD_FAST                's'
          618_620  POP_JUMP_IF_TRUE    630  'to 630'

 L. 216       622  LOAD_GLOBAL              SyntaxError
              624  LOAD_STR                 'File truncated'
              626  CALL_FUNCTION_1       1  ''
              628  RAISE_VARARGS_1       1  'exception instance'
            630_0  COME_FROM           618  '618'

 L. 218       630  LOAD_GLOBAL              LUT
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                info
              636  <118>                 0  ''
          638_640  POP_JUMP_IF_FALSE   894  'to 894'

 L. 220       642  LOAD_FAST                'self'
              644  LOAD_ATTR                fp
              646  LOAD_METHOD              read
              648  LOAD_CONST               768
              650  CALL_METHOD_1         1  ''
              652  STORE_FAST               'palette'

 L. 221       654  LOAD_CONST               1
              656  STORE_FAST               'greyscale'

 L. 222       658  LOAD_CONST               1
              660  STORE_FAST               'linear'

 L. 223       662  LOAD_GLOBAL              range
              664  LOAD_CONST               256
              666  CALL_FUNCTION_1       1  ''
              668  GET_ITER         
              670  FOR_ITER            750  'to 750'
              672  STORE_FAST               'i'

 L. 224       674  LOAD_FAST                'palette'
              676  LOAD_FAST                'i'
              678  BINARY_SUBSCR    
              680  LOAD_FAST                'palette'
              682  LOAD_FAST                'i'
              684  LOAD_CONST               256
              686  BINARY_ADD       
              688  BINARY_SUBSCR    
              690  DUP_TOP          
              692  ROT_THREE        
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   718  'to 718'
              700  LOAD_FAST                'palette'
              702  LOAD_FAST                'i'
              704  LOAD_CONST               512
              706  BINARY_ADD       
              708  BINARY_SUBSCR    
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   742  'to 742'
              716  JUMP_FORWARD        722  'to 722'
            718_0  COME_FROM           696  '696'
              718  POP_TOP          
              720  JUMP_FORWARD        742  'to 742'
            722_0  COME_FROM           716  '716'

 L. 225       722  LOAD_FAST                'palette'
              724  LOAD_FAST                'i'
              726  BINARY_SUBSCR    
              728  LOAD_FAST                'i'
              730  COMPARE_OP               !=
          732_734  POP_JUMP_IF_FALSE   746  'to 746'

 L. 226       736  LOAD_CONST               0
              738  STORE_FAST               'linear'
              740  JUMP_BACK           670  'to 670'
            742_0  COME_FROM           720  '720'
            742_1  COME_FROM           712  '712'

 L. 228       742  LOAD_CONST               0
              744  STORE_FAST               'greyscale'
            746_0  COME_FROM           732  '732'
          746_748  JUMP_BACK           670  'to 670'

 L. 229       750  LOAD_FAST                'self'
              752  LOAD_ATTR                mode
              754  LOAD_CONST               ('L', 'LA', 'P', 'PA')
              756  <118>                 0  ''
          758_760  POP_JUMP_IF_FALSE   860  'to 860'

 L. 230       762  LOAD_FAST                'greyscale'
          764_766  POP_JUMP_IF_FALSE   794  'to 794'

 L. 231       768  LOAD_FAST                'linear'
          770_772  POP_JUMP_IF_TRUE    858  'to 858'

 L. 232       774  LOAD_GLOBAL              list
              776  LOAD_FAST                'palette'
              778  LOAD_CONST               None
              780  LOAD_CONST               256
              782  BUILD_SLICE_2         2 
              784  BINARY_SUBSCR    
              786  CALL_FUNCTION_1       1  ''
              788  LOAD_FAST                'self'
              790  STORE_ATTR               lut
              792  JUMP_FORWARD        858  'to 858'
            794_0  COME_FROM           764  '764'

 L. 234       794  LOAD_FAST                'self'
              796  LOAD_ATTR                mode
              798  LOAD_CONST               ('L', 'P')
              800  <118>                 0  ''
          802_804  POP_JUMP_IF_FALSE   820  'to 820'

 L. 235       806  LOAD_STR                 'P'
              808  DUP_TOP          
              810  LOAD_FAST                'self'
              812  STORE_ATTR               mode
              814  LOAD_FAST                'self'
              816  STORE_ATTR               rawmode
              818  JUMP_FORWARD        844  'to 844'
            820_0  COME_FROM           802  '802'

 L. 236       820  LOAD_FAST                'self'
              822  LOAD_ATTR                mode
              824  LOAD_CONST               ('LA', 'PA')
              826  <118>                 0  ''
          828_830  POP_JUMP_IF_FALSE   844  'to 844'

 L. 237       832  LOAD_STR                 'PA'
              834  LOAD_FAST                'self'
              836  STORE_ATTR               mode

 L. 238       838  LOAD_STR                 'PA;L'
              840  LOAD_FAST                'self'
              842  STORE_ATTR               rawmode
            844_0  COME_FROM           828  '828'
            844_1  COME_FROM           818  '818'

 L. 239       844  LOAD_GLOBAL              ImagePalette
              846  LOAD_METHOD              raw
              848  LOAD_STR                 'RGB;L'
              850  LOAD_FAST                'palette'
              852  CALL_METHOD_2         2  ''
              854  LOAD_FAST                'self'
              856  STORE_ATTR               palette
            858_0  COME_FROM           792  '792'
            858_1  COME_FROM           770  '770'
              858  JUMP_FORWARD        894  'to 894'
            860_0  COME_FROM           758  '758'

 L. 240       860  LOAD_FAST                'self'
              862  LOAD_ATTR                mode
              864  LOAD_STR                 'RGB'
              866  COMPARE_OP               ==
          868_870  POP_JUMP_IF_FALSE   894  'to 894'

 L. 241       872  LOAD_FAST                'greyscale'
          874_876  POP_JUMP_IF_FALSE   884  'to 884'
              878  LOAD_FAST                'linear'
          880_882  POP_JUMP_IF_TRUE    894  'to 894'
            884_0  COME_FROM           874  '874'

 L. 242       884  LOAD_GLOBAL              list
              886  LOAD_FAST                'palette'
              888  CALL_FUNCTION_1       1  ''
              890  LOAD_FAST                'self'
              892  STORE_ATTR               lut
            894_0  COME_FROM           880  '880'
            894_1  COME_FROM           868  '868'
            894_2  COME_FROM           858  '858'
            894_3  COME_FROM           638  '638'

 L. 244       894  LOAD_CONST               0
              896  LOAD_FAST                'self'
              898  STORE_ATTR               frame

 L. 246       900  LOAD_FAST                'self'
              902  LOAD_ATTR                fp
              904  LOAD_METHOD              tell
              906  CALL_METHOD_0         0  ''
              908  DUP_TOP          
              910  LOAD_FAST                'self'
              912  STORE_ATTR               _ImImageFile__offset
              914  STORE_FAST               'offs'

 L. 248       916  LOAD_FAST                'self'
              918  LOAD_ATTR                fp
              920  LOAD_FAST                'self'
              922  STORE_ATTR               _ImImageFile__fp

 L. 250       924  LOAD_FAST                'self'
              926  LOAD_ATTR                rawmode
              928  LOAD_CONST               None
              930  LOAD_CONST               2
              932  BUILD_SLICE_2         2 
              934  BINARY_SUBSCR    
              936  LOAD_STR                 'F;'
              938  COMPARE_OP               ==
          940_942  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 253       944  SETUP_FINALLY      1016  'to 1016'

 L. 255       946  LOAD_GLOBAL              int
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                rawmode
              952  LOAD_CONST               2
              954  LOAD_CONST               None
              956  BUILD_SLICE_2         2 
              958  BINARY_SUBSCR    
              960  CALL_FUNCTION_1       1  ''
              962  STORE_FAST               'bits'

 L. 256       964  LOAD_FAST                'bits'
              966  LOAD_CONST               (8, 16, 32)
              968  <118>                 1  ''
          970_972  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 257       974  LOAD_STR                 'bit'
              976  LOAD_CONST               (0, 0)
              978  LOAD_FAST                'self'
              980  LOAD_ATTR                size
              982  BINARY_ADD       
              984  LOAD_FAST                'offs'
              986  LOAD_FAST                'bits'
              988  LOAD_CONST               8
              990  LOAD_CONST               3
              992  LOAD_CONST               0
              994  LOAD_CONST               -1
              996  BUILD_TUPLE_5         5 
              998  BUILD_TUPLE_4         4 
             1000  BUILD_LIST_1          1 
             1002  LOAD_FAST                'self'
             1004  STORE_ATTR               tile

 L. 258      1006  POP_BLOCK        
             1008  LOAD_CONST               None
             1010  RETURN_VALUE     
           1012_0  COME_FROM           970  '970'
             1012  POP_BLOCK        
             1014  JUMP_FORWARD       1036  'to 1036'
           1016_0  COME_FROM_FINALLY   944  '944'

 L. 259      1016  DUP_TOP          
             1018  LOAD_GLOBAL              ValueError
         1020_1022  <121>              1034  ''
             1024  POP_TOP          
             1026  POP_TOP          
             1028  POP_TOP          

 L. 260      1030  POP_EXCEPT       
             1032  JUMP_FORWARD       1036  'to 1036'
             1034  <48>             
           1036_0  COME_FROM          1032  '1032'
           1036_1  COME_FROM          1014  '1014'
           1036_2  COME_FROM           940  '940'

 L. 262      1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                rawmode
             1040  LOAD_CONST               ('RGB;T', 'RYB;T')
             1042  <118>                 0  ''
         1044_1046  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 265      1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                size
             1052  LOAD_CONST               0
             1054  BINARY_SUBSCR    
             1056  LOAD_FAST                'self'
             1058  LOAD_ATTR                size
             1060  LOAD_CONST               1
             1062  BINARY_SUBSCR    
             1064  BINARY_MULTIPLY  
             1066  STORE_FAST               'size'

 L. 267      1068  LOAD_STR                 'raw'
             1070  LOAD_CONST               (0, 0)
             1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                size
             1076  BINARY_ADD       
             1078  LOAD_FAST                'offs'
             1080  LOAD_CONST               ('G', 0, -1)
             1082  BUILD_TUPLE_4         4 

 L. 268      1084  LOAD_STR                 'raw'
             1086  LOAD_CONST               (0, 0)
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                size
             1092  BINARY_ADD       
             1094  LOAD_FAST                'offs'
             1096  LOAD_FAST                'size'
             1098  BINARY_ADD       
             1100  LOAD_CONST               ('R', 0, -1)
             1102  BUILD_TUPLE_4         4 

 L. 269      1104  LOAD_STR                 'raw'
             1106  LOAD_CONST               (0, 0)
             1108  LOAD_FAST                'self'
             1110  LOAD_ATTR                size
             1112  BINARY_ADD       
             1114  LOAD_FAST                'offs'
             1116  LOAD_CONST               2
             1118  LOAD_FAST                'size'
             1120  BINARY_MULTIPLY  
             1122  BINARY_ADD       
             1124  LOAD_CONST               ('B', 0, -1)
             1126  BUILD_TUPLE_4         4 

 L. 266      1128  BUILD_LIST_3          3 
             1130  LOAD_FAST                'self'
             1132  STORE_ATTR               tile
             1134  JUMP_FORWARD       1166  'to 1166'
           1136_0  COME_FROM          1044  '1044'

 L. 273      1136  LOAD_STR                 'raw'
             1138  LOAD_CONST               (0, 0)
             1140  LOAD_FAST                'self'
             1142  LOAD_ATTR                size
             1144  BINARY_ADD       
             1146  LOAD_FAST                'offs'
             1148  LOAD_FAST                'self'
             1150  LOAD_ATTR                rawmode
             1152  LOAD_CONST               0
             1154  LOAD_CONST               -1
             1156  BUILD_TUPLE_3         3 
             1158  BUILD_TUPLE_4         4 
             1160  BUILD_LIST_1          1 
             1162  LOAD_FAST                'self'
             1164  STORE_ATTR               tile
           1166_0  COME_FROM          1134  '1134'

Parse error at or near `None' instruction at offset -1

                    @property
                    def n_frames(self):
                        return self.info[FRAMES]

                    @property
                    def is_animated(self):
                        return self.info[FRAMES] > 1

                    def seek(self, frame):
                        if not self._seek_check(frame):
                            return
                        else:
                            self.frame = frame
                            if self.mode == '1':
                                bits = 1
                            else:
                                bits = 8 * len(self.mode)
                        size = (self.size[0] * bits + 7) // 8 * self.size[1]
                        offs = self._ImImageFile__offset + frame * size
                        self.fp = self._ImImageFile__fp
                        self.tile = [
                         (
                          'raw', (0, 0) + self.size, offs, (self.rawmode, 0, -1))]

                    def tell(self):
                        return self.frame

                    def _close__fp--- This code section failed: ---

 L. 305         0  SETUP_FINALLY        58  'to 58'
                2  SETUP_FINALLY        30  'to 30'

 L. 306         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _ImImageFile__fp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                fp
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 307        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _ImImageFile__fp
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     2  '2'

 L. 308        30  DUP_TOP          
               32  LOAD_GLOBAL              AttributeError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 309        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'
               48  POP_BLOCK        

 L. 311        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _ImImageFile__fp
               56  JUMP_FORWARD         66  'to 66'
             58_0  COME_FROM_FINALLY     0  '0'
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _ImImageFile__fp
               64  <48>             
             66_0  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 34


                SAVE = {'1':('0 1', '1'), 
                 'L':('Greyscale', 'L'), 
                 'LA':('LA', 'LA;L'), 
                 'P':('Greyscale', 'P'), 
                 'PA':('LA', 'PA;L'), 
                 'I':('L 32S', 'I;32S'), 
                 'I;16':('L 16', 'I;16'), 
                 'I;16L':('L 16L', 'I;16L'), 
                 'I;16B':('L 16B', 'I;16B'), 
                 'F':('L 32F', 'F;32F'), 
                 'RGB':('RGB', 'RGB;L'), 
                 'RGBA':('RGBA', 'RGBA;L'), 
                 'RGBX':('RGBX', 'RGBX;L'), 
                 'CMYK':('CMYK', 'CMYK;L'), 
                 'YCbCr':('YCC', 'YCbCr;L')}

                def _save--- This code section failed: ---

 L. 341         0  SETUP_FINALLY        20  'to 20'

 L. 342         2  LOAD_GLOBAL              SAVE
                4  LOAD_FAST                'im'
                6  LOAD_ATTR                mode
                8  BINARY_SUBSCR    
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'image_type'
               14  STORE_FAST               'rawmode'
               16  POP_BLOCK        
               18  JUMP_FORWARD         76  'to 76'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 343        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                74  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        66  'to 66'

 L. 344        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 'Cannot save '
               38  LOAD_FAST                'im'
               40  LOAD_ATTR                mode
               42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 ' images as IM'
               46  BUILD_STRING_3        3 
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_FAST                'e'
               52  RAISE_VARARGS_2       2  'exception instance with __cause__'
               54  POP_BLOCK        
               56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM_FINALLY    32  '32'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  <48>             
               74  <48>             
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            18  '18'

 L. 346        76  LOAD_FAST                'im'
               78  LOAD_ATTR                encoderinfo
               80  LOAD_METHOD              get
               82  LOAD_STR                 'frames'
               84  LOAD_CONST               1
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'frames'

 L. 348        90  LOAD_FAST                'fp'
               92  LOAD_METHOD              write
               94  LOAD_STR                 'Image type: '
               96  LOAD_FAST                'image_type'
               98  FORMAT_VALUE          0  ''
              100  LOAD_STR                 ' image\r\n'
              102  BUILD_STRING_3        3 
              104  LOAD_METHOD              encode
              106  LOAD_STR                 'ascii'
              108  CALL_METHOD_1         1  ''
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 349       114  LOAD_FAST                'filename'
              116  POP_JUMP_IF_FALSE   196  'to 196'

 L. 354       118  LOAD_GLOBAL              os
              120  LOAD_ATTR                path
              122  LOAD_METHOD              splitext
              124  LOAD_GLOBAL              os
              126  LOAD_ATTR                path
              128  LOAD_METHOD              basename
              130  LOAD_FAST                'filename'
              132  CALL_METHOD_1         1  ''
              134  CALL_METHOD_1         1  ''
              136  UNPACK_SEQUENCE_2     2 
              138  STORE_FAST               'name'
              140  STORE_FAST               'ext'

 L. 355       142  LOAD_STR                 ''
              144  LOAD_METHOD              join
              146  LOAD_FAST                'name'
              148  LOAD_CONST               None
              150  LOAD_CONST               92
              152  LOAD_GLOBAL              len
              154  LOAD_FAST                'ext'
              156  CALL_FUNCTION_1       1  ''
              158  BINARY_SUBTRACT  
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'ext'
              166  BUILD_LIST_2          2 
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'name'

 L. 357       172  LOAD_FAST                'fp'
              174  LOAD_METHOD              write
              176  LOAD_STR                 'Name: '
              178  LOAD_FAST                'name'
              180  FORMAT_VALUE          0  ''
              182  LOAD_STR                 '\r\n'
              184  BUILD_STRING_3        3 
              186  LOAD_METHOD              encode
              188  LOAD_STR                 'ascii'
              190  CALL_METHOD_1         1  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           116  '116'

 L. 358       196  LOAD_FAST                'fp'
              198  LOAD_METHOD              write
              200  LOAD_STR                 'Image size (x*y): %d*%d\r\n'
              202  LOAD_FAST                'im'
              204  LOAD_ATTR                size
              206  BINARY_MODULO    
              208  LOAD_METHOD              encode
              210  LOAD_STR                 'ascii'
              212  CALL_METHOD_1         1  ''
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          

 L. 359       218  LOAD_FAST                'fp'
              220  LOAD_METHOD              write
              222  LOAD_STR                 'File size (no of images): '
              224  LOAD_FAST                'frames'
              226  FORMAT_VALUE          0  ''
              228  LOAD_STR                 '\r\n'
              230  BUILD_STRING_3        3 
              232  LOAD_METHOD              encode
              234  LOAD_STR                 'ascii'
              236  CALL_METHOD_1         1  ''
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          

 L. 360       242  LOAD_FAST                'im'
              244  LOAD_ATTR                mode
              246  LOAD_CONST               ('P', 'PA')
              248  <118>                 0  ''
          250_252  POP_JUMP_IF_FALSE   264  'to 264'

 L. 361       254  LOAD_FAST                'fp'
              256  LOAD_METHOD              write
              258  LOAD_CONST               b'Lut: 1\r\n'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           250  '250'

 L. 362       264  LOAD_FAST                'fp'
              266  LOAD_METHOD              write
              268  LOAD_CONST               b'\x00'
              270  LOAD_CONST               511
              272  LOAD_FAST                'fp'
              274  LOAD_METHOD              tell
              276  CALL_METHOD_0         0  ''
              278  BINARY_SUBTRACT  
              280  BINARY_MULTIPLY  
              282  LOAD_CONST               b'\x1a'
              284  BINARY_ADD       
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 363       290  LOAD_FAST                'im'
              292  LOAD_ATTR                mode
              294  LOAD_CONST               ('P', 'PA')
              296  <118>                 0  ''
          298_300  POP_JUMP_IF_FALSE   322  'to 322'

 L. 364       302  LOAD_FAST                'fp'
              304  LOAD_METHOD              write
              306  LOAD_FAST                'im'
              308  LOAD_ATTR                im
              310  LOAD_METHOD              getpalette
              312  LOAD_STR                 'RGB'
              314  LOAD_STR                 'RGB;L'
              316  CALL_METHOD_2         2  ''
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
            322_0  COME_FROM           298  '298'

 L. 365       322  LOAD_GLOBAL              ImageFile
              324  LOAD_METHOD              _save
              326  LOAD_FAST                'im'
              328  LOAD_FAST                'fp'
              330  LOAD_STR                 'raw'
              332  LOAD_CONST               (0, 0)
              334  LOAD_FAST                'im'
              336  LOAD_ATTR                size
              338  BINARY_ADD       
              340  LOAD_CONST               0
              342  LOAD_FAST                'rawmode'
              344  LOAD_CONST               0
              346  LOAD_CONST               -1
              348  BUILD_TUPLE_3         3 
              350  BUILD_TUPLE_4         4 
              352  BUILD_LIST_1          1 
              354  CALL_METHOD_3         3  ''
              356  POP_TOP          

Parse error at or near `<121>' instruction at offset 24


                Image.register_open(ImImageFile.format, ImImageFile)
                Image.register_save(ImImageFile.format, _save)
                Image.register_extension(ImImageFile.format, '.im')