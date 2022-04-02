# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\ImImagePlugin.py
import os, re
from . import Image, ImageFile, ImagePalette
from ._binary import i8
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

 L. 108         0  SETUP_FINALLY        12  'to 12'

 L. 109         2  LOAD_GLOBAL              int
                4  LOAD_FAST                's'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 110        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 111        26  LOAD_GLOBAL              float
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  ''
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            18  '18'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


                class ImImageFile(ImageFile.ImageFile):
                    format = 'IM'
                    format_description = 'IFUNC Image Memory'
                    _close_exclusive_fp_after_loading = False

                    def _open--- This code section failed: ---

 L. 129         0  LOAD_CONST               b'\n'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               100
               10  CALL_METHOD_1         1  ''
               12  COMPARE_OP               not-in
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 130        16  LOAD_GLOBAL              SyntaxError
               18  LOAD_STR                 'not an IM file'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 131        24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_METHOD              seek
               30  LOAD_CONST               0
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 133        36  LOAD_CONST               0
               38  STORE_FAST               'n'

 L. 136        40  LOAD_STR                 'L'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                info
               46  LOAD_GLOBAL              MODE
               48  STORE_SUBSCR     

 L. 137        50  LOAD_CONST               (512, 512)
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                info
               56  LOAD_GLOBAL              SIZE
               58  STORE_SUBSCR     

 L. 138        60  LOAD_CONST               1
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                info
               66  LOAD_GLOBAL              FRAMES
               68  STORE_SUBSCR     

 L. 140        70  LOAD_STR                 'L'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               rawmode

 L. 144        76  LOAD_FAST                'self'
               78  LOAD_ATTR                fp
               80  LOAD_METHOD              read
               82  LOAD_CONST               1
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               's'

 L. 147        88  LOAD_FAST                's'
               90  LOAD_CONST               b'\r'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 148        96  JUMP_BACK            76  'to 76'
             98_0  COME_FROM            94  '94'

 L. 150        98  LOAD_FAST                's'
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

 L. 151   118_120  BREAK_LOOP          536  'to 536'
            122_0  COME_FROM           116  '116'

 L. 154       122  LOAD_FAST                's'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                fp
              128  LOAD_METHOD              readline
              130  CALL_METHOD_0         0  ''
              132  BINARY_ADD       
              134  STORE_FAST               's'

 L. 156       136  LOAD_GLOBAL              len
              138  LOAD_FAST                's'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               100
              144  COMPARE_OP               >
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L. 157       148  LOAD_GLOBAL              SyntaxError
              150  LOAD_STR                 'not an IM file'
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           146  '146'

 L. 159       156  LOAD_FAST                's'
              158  LOAD_CONST               -2
              160  LOAD_CONST               None
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  LOAD_CONST               b'\r\n'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   186  'to 186'

 L. 160       172  LOAD_FAST                's'
              174  LOAD_CONST               None
              176  LOAD_CONST               -2
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  STORE_FAST               's'
              184  JUMP_FORWARD        214  'to 214'
            186_0  COME_FROM           170  '170'

 L. 161       186  LOAD_FAST                's'
              188  LOAD_CONST               -1
              190  LOAD_CONST               None
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  LOAD_CONST               b'\n'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 162       202  LOAD_FAST                's'
              204  LOAD_CONST               None
              206  LOAD_CONST               -1
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_FAST               's'
            214_0  COME_FROM           200  '200'
            214_1  COME_FROM           184  '184'

 L. 164       214  SETUP_FINALLY       230  'to 230'

 L. 165       216  LOAD_GLOBAL              split
              218  LOAD_METHOD              match
              220  LOAD_FAST                's'
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'm'
              226  POP_BLOCK        
              228  JUMP_FORWARD        278  'to 278'
            230_0  COME_FROM_FINALLY   214  '214'

 L. 166       230  DUP_TOP          
              232  LOAD_GLOBAL              re
              234  LOAD_ATTR                error
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   276  'to 276'
              242  POP_TOP          
              244  STORE_FAST               'e'
              246  POP_TOP          
              248  SETUP_FINALLY       264  'to 264'

 L. 167       250  LOAD_GLOBAL              SyntaxError
              252  LOAD_STR                 'not an IM file'
              254  CALL_FUNCTION_1       1  ''
              256  LOAD_FAST                'e'
              258  RAISE_VARARGS_2       2  'exception instance with __cause__'
              260  POP_BLOCK        
              262  BEGIN_FINALLY    
            264_0  COME_FROM_FINALLY   248  '248'
              264  LOAD_CONST               None
              266  STORE_FAST               'e'
              268  DELETE_FAST              'e'
              270  END_FINALLY      
              272  POP_EXCEPT       
              274  JUMP_FORWARD        278  'to 278'
            276_0  COME_FROM           238  '238'
              276  END_FINALLY      
            278_0  COME_FROM           274  '274'
            278_1  COME_FROM           228  '228'

 L. 169       278  LOAD_FAST                'm'
          280_282  POP_JUMP_IF_FALSE   514  'to 514'

 L. 171       284  LOAD_FAST                'm'
              286  LOAD_METHOD              group
              288  LOAD_CONST               1
              290  LOAD_CONST               2
              292  CALL_METHOD_2         2  ''
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'k'
              298  STORE_FAST               'v'

 L. 175       300  LOAD_FAST                'k'
              302  LOAD_METHOD              decode
              304  LOAD_STR                 'latin-1'
              306  LOAD_STR                 'replace'
              308  CALL_METHOD_2         2  ''
              310  STORE_FAST               'k'

 L. 176       312  LOAD_FAST                'v'
              314  LOAD_METHOD              decode
              316  LOAD_STR                 'latin-1'
              318  LOAD_STR                 'replace'
              320  CALL_METHOD_2         2  ''
              322  STORE_FAST               'v'

 L. 179       324  LOAD_FAST                'k'
              326  LOAD_GLOBAL              FRAMES
              328  LOAD_GLOBAL              SCALE
              330  LOAD_GLOBAL              SIZE
              332  BUILD_TUPLE_3         3 
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   396  'to 396'

 L. 180       340  LOAD_FAST                'v'
              342  LOAD_METHOD              replace
              344  LOAD_STR                 '*'
              346  LOAD_STR                 ','
              348  CALL_METHOD_2         2  ''
              350  STORE_FAST               'v'

 L. 181       352  LOAD_GLOBAL              tuple
              354  LOAD_GLOBAL              map
              356  LOAD_GLOBAL              number
              358  LOAD_FAST                'v'
              360  LOAD_METHOD              split
              362  LOAD_STR                 ','
              364  CALL_METHOD_1         1  ''
              366  CALL_FUNCTION_2       2  ''
              368  CALL_FUNCTION_1       1  ''
              370  STORE_FAST               'v'

 L. 182       372  LOAD_GLOBAL              len
              374  LOAD_FAST                'v'
              376  CALL_FUNCTION_1       1  ''
              378  LOAD_CONST               1
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   430  'to 430'

 L. 183       386  LOAD_FAST                'v'
              388  LOAD_CONST               0
              390  BINARY_SUBSCR    
              392  STORE_FAST               'v'
              394  JUMP_FORWARD        430  'to 430'
            396_0  COME_FROM           336  '336'

 L. 184       396  LOAD_FAST                'k'
              398  LOAD_GLOBAL              MODE
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   430  'to 430'
              406  LOAD_FAST                'v'
              408  LOAD_GLOBAL              OPEN
              410  COMPARE_OP               in
          412_414  POP_JUMP_IF_FALSE   430  'to 430'

 L. 185       416  LOAD_GLOBAL              OPEN
              418  LOAD_FAST                'v'
              420  BINARY_SUBSCR    
              422  UNPACK_SEQUENCE_2     2 
              424  STORE_FAST               'v'
              426  LOAD_FAST                'self'
              428  STORE_ATTR               rawmode
            430_0  COME_FROM           412  '412'
            430_1  COME_FROM           402  '402'
            430_2  COME_FROM           394  '394'
            430_3  COME_FROM           382  '382'

 L. 189       430  LOAD_FAST                'k'
              432  LOAD_GLOBAL              COMMENT
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   484  'to 484'

 L. 190       440  LOAD_FAST                'k'
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                info
              446  COMPARE_OP               in
          448_450  POP_JUMP_IF_FALSE   470  'to 470'

 L. 191       452  LOAD_FAST                'self'
              454  LOAD_ATTR                info
              456  LOAD_FAST                'k'
              458  BINARY_SUBSCR    
              460  LOAD_METHOD              append
              462  LOAD_FAST                'v'
              464  CALL_METHOD_1         1  ''
              466  POP_TOP          
              468  JUMP_FORWARD        482  'to 482'
            470_0  COME_FROM           448  '448'

 L. 193       470  LOAD_FAST                'v'
              472  BUILD_LIST_1          1 
              474  LOAD_FAST                'self'
              476  LOAD_ATTR                info
              478  LOAD_FAST                'k'
              480  STORE_SUBSCR     
            482_0  COME_FROM           468  '468'
              482  JUMP_FORWARD        494  'to 494'
            484_0  COME_FROM           436  '436'

 L. 195       484  LOAD_FAST                'v'
              486  LOAD_FAST                'self'
              488  LOAD_ATTR                info
              490  LOAD_FAST                'k'
              492  STORE_SUBSCR     
            494_0  COME_FROM           482  '482'

 L. 197       494  LOAD_FAST                'k'
              496  LOAD_GLOBAL              TAGS
              498  COMPARE_OP               in
          500_502  POP_JUMP_IF_FALSE   534  'to 534'

 L. 198       504  LOAD_FAST                'n'
              506  LOAD_CONST               1
              508  INPLACE_ADD      
              510  STORE_FAST               'n'
              512  JUMP_BACK            76  'to 76'
            514_0  COME_FROM           280  '280'

 L. 202       514  LOAD_GLOBAL              SyntaxError

 L. 203       516  LOAD_STR                 'Syntax error in IM header: '
              518  LOAD_FAST                's'
              520  LOAD_METHOD              decode
              522  LOAD_STR                 'ascii'
              524  LOAD_STR                 'replace'
              526  CALL_METHOD_2         2  ''
              528  BINARY_ADD       

 L. 202       530  CALL_FUNCTION_1       1  ''
              532  RAISE_VARARGS_1       1  'exception instance'
            534_0  COME_FROM           500  '500'
              534  JUMP_BACK            76  'to 76'

 L. 206       536  LOAD_FAST                'n'
          538_540  POP_JUMP_IF_TRUE    550  'to 550'

 L. 207       542  LOAD_GLOBAL              SyntaxError
              544  LOAD_STR                 'Not an IM file'
              546  CALL_FUNCTION_1       1  ''
              548  RAISE_VARARGS_1       1  'exception instance'
            550_0  COME_FROM           538  '538'

 L. 210       550  LOAD_FAST                'self'
              552  LOAD_ATTR                info
              554  LOAD_GLOBAL              SIZE
              556  BINARY_SUBSCR    
              558  LOAD_FAST                'self'
              560  STORE_ATTR               _size

 L. 211       562  LOAD_FAST                'self'
              564  LOAD_ATTR                info
              566  LOAD_GLOBAL              MODE
              568  BINARY_SUBSCR    
              570  LOAD_FAST                'self'
              572  STORE_ATTR               mode

 L. 214       574  LOAD_FAST                's'
          576_578  POP_JUMP_IF_FALSE   614  'to 614'
              580  LOAD_FAST                's'
              582  LOAD_CONST               0
              584  LOAD_CONST               1
              586  BUILD_SLICE_2         2 
              588  BINARY_SUBSCR    
              590  LOAD_CONST               b'\x1a'
              592  COMPARE_OP               !=
          594_596  POP_JUMP_IF_FALSE   614  'to 614'

 L. 215       598  LOAD_FAST                'self'
              600  LOAD_ATTR                fp
              602  LOAD_METHOD              read
              604  LOAD_CONST               1
              606  CALL_METHOD_1         1  ''
              608  STORE_FAST               's'
          610_612  JUMP_BACK           574  'to 574'
            614_0  COME_FROM           594  '594'
            614_1  COME_FROM           576  '576'

 L. 216       614  LOAD_FAST                's'
          616_618  POP_JUMP_IF_TRUE    628  'to 628'

 L. 217       620  LOAD_GLOBAL              SyntaxError
              622  LOAD_STR                 'File truncated'
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           616  '616'

 L. 219       628  LOAD_GLOBAL              LUT
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                info
              634  COMPARE_OP               in
          636_638  POP_JUMP_IF_FALSE   908  'to 908'

 L. 221       640  LOAD_FAST                'self'
              642  LOAD_ATTR                fp
              644  LOAD_METHOD              read
              646  LOAD_CONST               768
              648  CALL_METHOD_1         1  ''
              650  STORE_FAST               'palette'

 L. 222       652  LOAD_CONST               1
              654  STORE_FAST               'greyscale'

 L. 223       656  LOAD_CONST               1
              658  STORE_FAST               'linear'

 L. 224       660  LOAD_GLOBAL              range
              662  LOAD_CONST               256
              664  CALL_FUNCTION_1       1  ''
              666  GET_ITER         
              668  FOR_ITER            752  'to 752'
              670  STORE_FAST               'i'

 L. 225       672  LOAD_FAST                'palette'
              674  LOAD_FAST                'i'
              676  BINARY_SUBSCR    
              678  LOAD_FAST                'palette'
              680  LOAD_FAST                'i'
              682  LOAD_CONST               256
              684  BINARY_ADD       
              686  BINARY_SUBSCR    
              688  DUP_TOP          
              690  ROT_THREE        
              692  COMPARE_OP               ==
          694_696  POP_JUMP_IF_FALSE   716  'to 716'
              698  LOAD_FAST                'palette'
              700  LOAD_FAST                'i'
              702  LOAD_CONST               512
              704  BINARY_ADD       
              706  BINARY_SUBSCR    
              708  COMPARE_OP               ==
          710_712  POP_JUMP_IF_FALSE   744  'to 744'
              714  JUMP_FORWARD        720  'to 720'
            716_0  COME_FROM           694  '694'
              716  POP_TOP          
              718  JUMP_FORWARD        744  'to 744'
            720_0  COME_FROM           714  '714'

 L. 226       720  LOAD_GLOBAL              i8
              722  LOAD_FAST                'palette'
              724  LOAD_FAST                'i'
              726  BINARY_SUBSCR    
              728  CALL_FUNCTION_1       1  ''
              730  LOAD_FAST                'i'
              732  COMPARE_OP               !=
          734_736  POP_JUMP_IF_FALSE   748  'to 748'

 L. 227       738  LOAD_CONST               0
              740  STORE_FAST               'linear'
              742  JUMP_BACK           668  'to 668'
            744_0  COME_FROM           718  '718'
            744_1  COME_FROM           710  '710'

 L. 229       744  LOAD_CONST               0
              746  STORE_FAST               'greyscale'
            748_0  COME_FROM           734  '734'
          748_750  JUMP_BACK           668  'to 668'

 L. 230       752  LOAD_FAST                'self'
              754  LOAD_ATTR                mode
              756  LOAD_CONST               ('L', 'LA', 'P', 'PA')
              758  COMPARE_OP               in
          760_762  POP_JUMP_IF_FALSE   868  'to 868'

 L. 231       764  LOAD_FAST                'greyscale'
          766_768  POP_JUMP_IF_FALSE   802  'to 802'

 L. 232       770  LOAD_FAST                'linear'
          772_774  POP_JUMP_IF_TRUE    866  'to 866'

 L. 233       776  LOAD_LISTCOMP            '<code_object <listcomp>>'
              778  LOAD_STR                 'ImImageFile._open.<locals>.<listcomp>'
              780  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              782  LOAD_FAST                'palette'
              784  LOAD_CONST               None
              786  LOAD_CONST               256
              788  BUILD_SLICE_2         2 
              790  BINARY_SUBSCR    
              792  GET_ITER         
              794  CALL_FUNCTION_1       1  ''
              796  LOAD_FAST                'self'
              798  STORE_ATTR               lut
              800  JUMP_FORWARD        866  'to 866'
            802_0  COME_FROM           766  '766'

 L. 235       802  LOAD_FAST                'self'
              804  LOAD_ATTR                mode
              806  LOAD_CONST               ('L', 'P')
              808  COMPARE_OP               in
          810_812  POP_JUMP_IF_FALSE   828  'to 828'

 L. 236       814  LOAD_STR                 'P'
              816  DUP_TOP          
              818  LOAD_FAST                'self'
              820  STORE_ATTR               mode
              822  LOAD_FAST                'self'
              824  STORE_ATTR               rawmode
              826  JUMP_FORWARD        852  'to 852'
            828_0  COME_FROM           810  '810'

 L. 237       828  LOAD_FAST                'self'
              830  LOAD_ATTR                mode
              832  LOAD_CONST               ('LA', 'PA')
              834  COMPARE_OP               in
          836_838  POP_JUMP_IF_FALSE   852  'to 852'

 L. 238       840  LOAD_STR                 'PA'
              842  LOAD_FAST                'self'
              844  STORE_ATTR               mode

 L. 239       846  LOAD_STR                 'PA;L'
              848  LOAD_FAST                'self'
              850  STORE_ATTR               rawmode
            852_0  COME_FROM           836  '836'
            852_1  COME_FROM           826  '826'

 L. 240       852  LOAD_GLOBAL              ImagePalette
              854  LOAD_METHOD              raw
              856  LOAD_STR                 'RGB;L'
              858  LOAD_FAST                'palette'
              860  CALL_METHOD_2         2  ''
              862  LOAD_FAST                'self'
              864  STORE_ATTR               palette
            866_0  COME_FROM           800  '800'
            866_1  COME_FROM           772  '772'
              866  JUMP_FORWARD        908  'to 908'
            868_0  COME_FROM           760  '760'

 L. 241       868  LOAD_FAST                'self'
              870  LOAD_ATTR                mode
              872  LOAD_STR                 'RGB'
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_FALSE   908  'to 908'

 L. 242       880  LOAD_FAST                'greyscale'
          882_884  POP_JUMP_IF_FALSE   892  'to 892'
              886  LOAD_FAST                'linear'
          888_890  POP_JUMP_IF_TRUE    908  'to 908'
            892_0  COME_FROM           882  '882'

 L. 243       892  LOAD_LISTCOMP            '<code_object <listcomp>>'
              894  LOAD_STR                 'ImImageFile._open.<locals>.<listcomp>'
              896  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              898  LOAD_FAST                'palette'
              900  GET_ITER         
              902  CALL_FUNCTION_1       1  ''
              904  LOAD_FAST                'self'
              906  STORE_ATTR               lut
            908_0  COME_FROM           888  '888'
            908_1  COME_FROM           876  '876'
            908_2  COME_FROM           866  '866'
            908_3  COME_FROM           636  '636'

 L. 245       908  LOAD_CONST               0
              910  LOAD_FAST                'self'
              912  STORE_ATTR               frame

 L. 247       914  LOAD_FAST                'self'
              916  LOAD_ATTR                fp
              918  LOAD_METHOD              tell
              920  CALL_METHOD_0         0  ''
              922  DUP_TOP          
              924  LOAD_FAST                'self'
              926  STORE_ATTR               _ImImageFile__offset
              928  STORE_FAST               'offs'

 L. 249       930  LOAD_FAST                'self'
              932  LOAD_ATTR                fp
              934  LOAD_FAST                'self'
              936  STORE_ATTR               _ImImageFile__fp

 L. 251       938  LOAD_FAST                'self'
              940  LOAD_ATTR                rawmode
              942  LOAD_CONST               None
              944  LOAD_CONST               2
              946  BUILD_SLICE_2         2 
              948  BINARY_SUBSCR    
              950  LOAD_STR                 'F;'
              952  COMPARE_OP               ==
          954_956  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 254       958  SETUP_FINALLY      1030  'to 1030'

 L. 256       960  LOAD_GLOBAL              int
              962  LOAD_FAST                'self'
              964  LOAD_ATTR                rawmode
              966  LOAD_CONST               2
              968  LOAD_CONST               None
              970  BUILD_SLICE_2         2 
              972  BINARY_SUBSCR    
              974  CALL_FUNCTION_1       1  ''
              976  STORE_FAST               'bits'

 L. 257       978  LOAD_FAST                'bits'
              980  LOAD_CONST               (8, 16, 32)
              982  COMPARE_OP               not-in
          984_986  POP_JUMP_IF_FALSE  1026  'to 1026'

 L. 258       988  LOAD_STR                 'bit'
              990  LOAD_CONST               (0, 0)
              992  LOAD_FAST                'self'
              994  LOAD_ATTR                size
              996  BINARY_ADD       
              998  LOAD_FAST                'offs'
             1000  LOAD_FAST                'bits'
             1002  LOAD_CONST               8
             1004  LOAD_CONST               3
             1006  LOAD_CONST               0
             1008  LOAD_CONST               -1
             1010  BUILD_TUPLE_5         5 
             1012  BUILD_TUPLE_4         4 
             1014  BUILD_LIST_1          1 
             1016  LOAD_FAST                'self'
             1018  STORE_ATTR               tile

 L. 259      1020  POP_BLOCK        
             1022  LOAD_CONST               None
             1024  RETURN_VALUE     
           1026_0  COME_FROM           984  '984'
             1026  POP_BLOCK        
             1028  JUMP_FORWARD       1052  'to 1052'
           1030_0  COME_FROM_FINALLY   958  '958'

 L. 260      1030  DUP_TOP          
             1032  LOAD_GLOBAL              ValueError
             1034  COMPARE_OP               exception-match
         1036_1038  POP_JUMP_IF_FALSE  1050  'to 1050'
             1040  POP_TOP          
             1042  POP_TOP          
             1044  POP_TOP          

 L. 261      1046  POP_EXCEPT       
             1048  JUMP_FORWARD       1052  'to 1052'
           1050_0  COME_FROM          1036  '1036'
             1050  END_FINALLY      
           1052_0  COME_FROM          1048  '1048'
           1052_1  COME_FROM          1028  '1028'
           1052_2  COME_FROM           954  '954'

 L. 263      1052  LOAD_FAST                'self'
             1054  LOAD_ATTR                rawmode
             1056  LOAD_CONST               ('RGB;T', 'RYB;T')
             1058  COMPARE_OP               in
         1060_1062  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 266      1064  LOAD_FAST                'self'
             1066  LOAD_ATTR                size
             1068  LOAD_CONST               0
             1070  BINARY_SUBSCR    
             1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                size
             1076  LOAD_CONST               1
             1078  BINARY_SUBSCR    
             1080  BINARY_MULTIPLY  
             1082  STORE_FAST               'size'

 L. 268      1084  LOAD_STR                 'raw'
             1086  LOAD_CONST               (0, 0)
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                size
             1092  BINARY_ADD       
             1094  LOAD_FAST                'offs'
             1096  LOAD_CONST               ('G', 0, -1)
             1098  BUILD_TUPLE_4         4 

 L. 269      1100  LOAD_STR                 'raw'
             1102  LOAD_CONST               (0, 0)
             1104  LOAD_FAST                'self'
             1106  LOAD_ATTR                size
             1108  BINARY_ADD       
             1110  LOAD_FAST                'offs'
             1112  LOAD_FAST                'size'
             1114  BINARY_ADD       
             1116  LOAD_CONST               ('R', 0, -1)
             1118  BUILD_TUPLE_4         4 

 L. 270      1120  LOAD_STR                 'raw'
             1122  LOAD_CONST               (0, 0)
             1124  LOAD_FAST                'self'
             1126  LOAD_ATTR                size
             1128  BINARY_ADD       
             1130  LOAD_FAST                'offs'
             1132  LOAD_CONST               2
             1134  LOAD_FAST                'size'
             1136  BINARY_MULTIPLY  
             1138  BINARY_ADD       
             1140  LOAD_CONST               ('B', 0, -1)
             1142  BUILD_TUPLE_4         4 

 L. 267      1144  BUILD_LIST_3          3 
             1146  LOAD_FAST                'self'
             1148  STORE_ATTR               tile
             1150  JUMP_FORWARD       1182  'to 1182'
           1152_0  COME_FROM          1060  '1060'

 L. 274      1152  LOAD_STR                 'raw'
             1154  LOAD_CONST               (0, 0)
             1156  LOAD_FAST                'self'
             1158  LOAD_ATTR                size
             1160  BINARY_ADD       
             1162  LOAD_FAST                'offs'
             1164  LOAD_FAST                'self'
             1166  LOAD_ATTR                rawmode
             1168  LOAD_CONST               0
             1170  LOAD_CONST               -1
             1172  BUILD_TUPLE_3         3 
             1174  BUILD_TUPLE_4         4 
             1176  BUILD_LIST_1          1 
             1178  LOAD_FAST                'self'
             1180  STORE_ATTR               tile
           1182_0  COME_FROM          1150  '1150'

Parse error at or near `LOAD_CONST' instruction at offset 1022

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

                    def _close__fp(self):
                        try:
                            try:
                                if self._ImImageFile__fp != self.fp:
                                    self._ImImageFile__fp.close
                            except AttributeError:
                                pass

                        finally:
                            self._ImImageFile__fp = None


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

                def _save(im, fp, filename):
                    try:
                        image_type, rawmode = SAVE[im.mode]
                    except KeyError as e:
                        try:
                            raise ValueError(f"Cannot save {im.mode} images as IM") from e
                        finally:
                            e = None
                            del e

                    else:
                        frames = im.encoderinfo.get('frames', 1)
                        fp.write(f"Image type: {image_type} image\r\n".encode('ascii'))
                        if filename:
                            name, ext = os.path.splitext(os.path.basename(filename))
                            name = ''.join([name[:92 - len(ext)], ext])
                            fp.write(f"Name: {name}\r\n".encode('ascii'))
                        fp.write(('Image size (x*y): %d*%d\r\n' % im.size).encode('ascii'))
                        fp.write(f"File size (no of images): {frames}\r\n".encode('ascii'))
                        if im.mode in ('P', 'PA'):
                            fp.write(b'Lut: 1\r\n')
                        fp.write(b'\x00' * (511 - fp.tell) + b'\x1a')
                        if im.mode in ('P', 'PA'):
                            fp.write(im.im.getpalette('RGB', 'RGB;L'))
                        ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, -1))])


                Image.register_open(ImImageFile.format, ImImageFile)
                Image.register_save(ImImageFile.format, _save)
                Image.register_extension(ImImageFile.format, '.im')