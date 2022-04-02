# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\ImImagePlugin.py
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
    OPEN['L %s image' % i] = (
     'F', 'F;%s' % i)
    OPEN['L*%s image' % i] = ('F', 'F;%s' % i)
else:
    for i in ('16', '16L', '16B'):
        OPEN['L %s image' % i] = (
         'I;%s' % i, 'I;%s' % i)
        OPEN['L*%s image' % i] = ('I;%s' % i, 'I;%s' % i)
    else:
        for i in ('32S', ):
            OPEN['L %s image' % i] = (
             'I', 'I;%s' % i)
            OPEN['L*%s image' % i] = ('I', 'I;%s' % i)
        else:
            for i in range(2, 33):
                OPEN['L*%s image' % i] = (
                 'F', 'F;%s' % i)
            else:
                split = re.compile(b'^([A-Za-z][^:]*):[ \\t]*(.*)[ \\t]*$')

                def number(s):
                    try:
                        return int(s)
                    except ValueError:
                        return float(s)


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
             76_0  COME_FROM           518  '518'
             76_1  COME_FROM           496  '496'
             76_2  COME_FROM            96  '96'

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

 L. 151   118_120  JUMP_FORWARD        520  'to 520'
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
              228  JUMP_FORWARD        262  'to 262'
            230_0  COME_FROM_FINALLY   214  '214'

 L. 166       230  DUP_TOP          
              232  LOAD_GLOBAL              re
              234  LOAD_ATTR                error
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   260  'to 260'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 167       248  LOAD_GLOBAL              SyntaxError
              250  LOAD_STR                 'not an IM file'
              252  CALL_FUNCTION_1       1  ''
              254  RAISE_VARARGS_1       1  'exception instance'
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           238  '238'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM           228  '228'

 L. 169       262  LOAD_FAST                'm'
          264_266  POP_JUMP_IF_FALSE   498  'to 498'

 L. 171       268  LOAD_FAST                'm'
              270  LOAD_METHOD              group
              272  LOAD_CONST               1
              274  LOAD_CONST               2
              276  CALL_METHOD_2         2  ''
              278  UNPACK_SEQUENCE_2     2 
              280  STORE_FAST               'k'
              282  STORE_FAST               'v'

 L. 175       284  LOAD_FAST                'k'
              286  LOAD_METHOD              decode
              288  LOAD_STR                 'latin-1'
              290  LOAD_STR                 'replace'
              292  CALL_METHOD_2         2  ''
              294  STORE_FAST               'k'

 L. 176       296  LOAD_FAST                'v'
              298  LOAD_METHOD              decode
              300  LOAD_STR                 'latin-1'
              302  LOAD_STR                 'replace'
              304  CALL_METHOD_2         2  ''
              306  STORE_FAST               'v'

 L. 179       308  LOAD_FAST                'k'
              310  LOAD_GLOBAL              FRAMES
              312  LOAD_GLOBAL              SCALE
              314  LOAD_GLOBAL              SIZE
              316  BUILD_TUPLE_3         3 
              318  COMPARE_OP               in
          320_322  POP_JUMP_IF_FALSE   380  'to 380'

 L. 180       324  LOAD_FAST                'v'
              326  LOAD_METHOD              replace
              328  LOAD_STR                 '*'
              330  LOAD_STR                 ','
              332  CALL_METHOD_2         2  ''
              334  STORE_FAST               'v'

 L. 181       336  LOAD_GLOBAL              tuple
              338  LOAD_GLOBAL              map
              340  LOAD_GLOBAL              number
              342  LOAD_FAST                'v'
              344  LOAD_METHOD              split
              346  LOAD_STR                 ','
              348  CALL_METHOD_1         1  ''
              350  CALL_FUNCTION_2       2  ''
              352  CALL_FUNCTION_1       1  ''
              354  STORE_FAST               'v'

 L. 182       356  LOAD_GLOBAL              len
              358  LOAD_FAST                'v'
              360  CALL_FUNCTION_1       1  ''
              362  LOAD_CONST               1
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   414  'to 414'

 L. 183       370  LOAD_FAST                'v'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  STORE_FAST               'v'
              378  JUMP_FORWARD        414  'to 414'
            380_0  COME_FROM           320  '320'

 L. 184       380  LOAD_FAST                'k'
              382  LOAD_GLOBAL              MODE
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   414  'to 414'
              390  LOAD_FAST                'v'
              392  LOAD_GLOBAL              OPEN
              394  COMPARE_OP               in
          396_398  POP_JUMP_IF_FALSE   414  'to 414'

 L. 185       400  LOAD_GLOBAL              OPEN
              402  LOAD_FAST                'v'
              404  BINARY_SUBSCR    
              406  UNPACK_SEQUENCE_2     2 
              408  STORE_FAST               'v'
              410  LOAD_FAST                'self'
              412  STORE_ATTR               rawmode
            414_0  COME_FROM           396  '396'
            414_1  COME_FROM           386  '386'
            414_2  COME_FROM           378  '378'
            414_3  COME_FROM           366  '366'

 L. 189       414  LOAD_FAST                'k'
              416  LOAD_GLOBAL              COMMENT
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   468  'to 468'

 L. 190       424  LOAD_FAST                'k'
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                info
              430  COMPARE_OP               in
          432_434  POP_JUMP_IF_FALSE   454  'to 454'

 L. 191       436  LOAD_FAST                'self'
              438  LOAD_ATTR                info
              440  LOAD_FAST                'k'
              442  BINARY_SUBSCR    
              444  LOAD_METHOD              append
              446  LOAD_FAST                'v'
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          
              452  JUMP_FORWARD        466  'to 466'
            454_0  COME_FROM           432  '432'

 L. 193       454  LOAD_FAST                'v'
              456  BUILD_LIST_1          1 
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                info
              462  LOAD_FAST                'k'
              464  STORE_SUBSCR     
            466_0  COME_FROM           452  '452'
              466  JUMP_FORWARD        478  'to 478'
            468_0  COME_FROM           420  '420'

 L. 195       468  LOAD_FAST                'v'
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                info
              474  LOAD_FAST                'k'
              476  STORE_SUBSCR     
            478_0  COME_FROM           466  '466'

 L. 197       478  LOAD_FAST                'k'
              480  LOAD_GLOBAL              TAGS
              482  COMPARE_OP               in
          484_486  POP_JUMP_IF_FALSE   518  'to 518'

 L. 198       488  LOAD_FAST                'n'
              490  LOAD_CONST               1
              492  INPLACE_ADD      
              494  STORE_FAST               'n'
              496  JUMP_BACK            76  'to 76'
            498_0  COME_FROM           264  '264'

 L. 202       498  LOAD_GLOBAL              SyntaxError

 L. 203       500  LOAD_STR                 'Syntax error in IM header: '
              502  LOAD_FAST                's'
              504  LOAD_METHOD              decode
              506  LOAD_STR                 'ascii'
              508  LOAD_STR                 'replace'
              510  CALL_METHOD_2         2  ''
              512  BINARY_ADD       

 L. 202       514  CALL_FUNCTION_1       1  ''
              516  RAISE_VARARGS_1       1  'exception instance'
            518_0  COME_FROM           484  '484'
              518  JUMP_BACK            76  'to 76'
            520_0  COME_FROM           118  '118'

 L. 206       520  LOAD_FAST                'n'
          522_524  POP_JUMP_IF_TRUE    534  'to 534'

 L. 207       526  LOAD_GLOBAL              SyntaxError
              528  LOAD_STR                 'Not an IM file'
              530  CALL_FUNCTION_1       1  ''
              532  RAISE_VARARGS_1       1  'exception instance'
            534_0  COME_FROM           522  '522'

 L. 210       534  LOAD_FAST                'self'
              536  LOAD_ATTR                info
              538  LOAD_GLOBAL              SIZE
              540  BINARY_SUBSCR    
              542  LOAD_FAST                'self'
              544  STORE_ATTR               _size

 L. 211       546  LOAD_FAST                'self'
              548  LOAD_ATTR                info
              550  LOAD_GLOBAL              MODE
              552  BINARY_SUBSCR    
              554  LOAD_FAST                'self'
              556  STORE_ATTR               mode
            558_0  COME_FROM           594  '594'

 L. 214       558  LOAD_FAST                's'
          560_562  POP_JUMP_IF_FALSE   598  'to 598'
              564  LOAD_FAST                's'
              566  LOAD_CONST               0
              568  LOAD_CONST               1
              570  BUILD_SLICE_2         2 
              572  BINARY_SUBSCR    
              574  LOAD_CONST               b'\x1a'
              576  COMPARE_OP               !=
          578_580  POP_JUMP_IF_FALSE   598  'to 598'

 L. 215       582  LOAD_FAST                'self'
              584  LOAD_ATTR                fp
              586  LOAD_METHOD              read
              588  LOAD_CONST               1
              590  CALL_METHOD_1         1  ''
              592  STORE_FAST               's'
          594_596  JUMP_BACK           558  'to 558'
            598_0  COME_FROM           578  '578'
            598_1  COME_FROM           560  '560'

 L. 216       598  LOAD_FAST                's'
          600_602  POP_JUMP_IF_TRUE    612  'to 612'

 L. 217       604  LOAD_GLOBAL              SyntaxError
              606  LOAD_STR                 'File truncated'
              608  CALL_FUNCTION_1       1  ''
              610  RAISE_VARARGS_1       1  'exception instance'
            612_0  COME_FROM           600  '600'

 L. 219       612  LOAD_GLOBAL              LUT
              614  LOAD_FAST                'self'
              616  LOAD_ATTR                info
              618  COMPARE_OP               in
          620_622  POP_JUMP_IF_FALSE   892  'to 892'

 L. 221       624  LOAD_FAST                'self'
              626  LOAD_ATTR                fp
              628  LOAD_METHOD              read
              630  LOAD_CONST               768
              632  CALL_METHOD_1         1  ''
              634  STORE_FAST               'palette'

 L. 222       636  LOAD_CONST               1
              638  STORE_FAST               'greyscale'

 L. 223       640  LOAD_CONST               1
              642  STORE_FAST               'linear'

 L. 224       644  LOAD_GLOBAL              range
              646  LOAD_CONST               256
              648  CALL_FUNCTION_1       1  ''
              650  GET_ITER         
            652_0  COME_FROM           732  '732'
            652_1  COME_FROM           726  '726'
              652  FOR_ITER            736  'to 736'
              654  STORE_FAST               'i'

 L. 225       656  LOAD_FAST                'palette'
              658  LOAD_FAST                'i'
              660  BINARY_SUBSCR    
              662  LOAD_FAST                'palette'
              664  LOAD_FAST                'i'
              666  LOAD_CONST               256
              668  BINARY_ADD       
              670  BINARY_SUBSCR    
              672  DUP_TOP          
              674  ROT_THREE        
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   700  'to 700'
              682  LOAD_FAST                'palette'
              684  LOAD_FAST                'i'
              686  LOAD_CONST               512
              688  BINARY_ADD       
              690  BINARY_SUBSCR    
              692  COMPARE_OP               ==
          694_696  POP_JUMP_IF_FALSE   728  'to 728'
              698  JUMP_FORWARD        704  'to 704'
            700_0  COME_FROM           678  '678'
              700  POP_TOP          
              702  JUMP_FORWARD        728  'to 728'
            704_0  COME_FROM           698  '698'

 L. 226       704  LOAD_GLOBAL              i8
              706  LOAD_FAST                'palette'
              708  LOAD_FAST                'i'
              710  BINARY_SUBSCR    
              712  CALL_FUNCTION_1       1  ''
              714  LOAD_FAST                'i'
              716  COMPARE_OP               !=
          718_720  POP_JUMP_IF_FALSE   732  'to 732'

 L. 227       722  LOAD_CONST               0
              724  STORE_FAST               'linear'
              726  JUMP_BACK           652  'to 652'
            728_0  COME_FROM           702  '702'
            728_1  COME_FROM           694  '694'

 L. 229       728  LOAD_CONST               0
              730  STORE_FAST               'greyscale'
            732_0  COME_FROM           718  '718'
          732_734  JUMP_BACK           652  'to 652'
            736_0  COME_FROM           652  '652'

 L. 230       736  LOAD_FAST                'self'
              738  LOAD_ATTR                mode
              740  LOAD_CONST               ('L', 'LA', 'P', 'PA')
              742  COMPARE_OP               in
          744_746  POP_JUMP_IF_FALSE   852  'to 852'

 L. 231       748  LOAD_FAST                'greyscale'
          750_752  POP_JUMP_IF_FALSE   786  'to 786'

 L. 232       754  LOAD_FAST                'linear'
          756_758  POP_JUMP_IF_TRUE    850  'to 850'

 L. 233       760  LOAD_LISTCOMP            '<code_object <listcomp>>'
              762  LOAD_STR                 'ImImageFile._open.<locals>.<listcomp>'
              764  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              766  LOAD_FAST                'palette'
              768  LOAD_CONST               None
              770  LOAD_CONST               256
              772  BUILD_SLICE_2         2 
              774  BINARY_SUBSCR    
              776  GET_ITER         
              778  CALL_FUNCTION_1       1  ''
              780  LOAD_FAST                'self'
              782  STORE_ATTR               lut
              784  JUMP_FORWARD        850  'to 850'
            786_0  COME_FROM           750  '750'

 L. 235       786  LOAD_FAST                'self'
              788  LOAD_ATTR                mode
              790  LOAD_CONST               ('L', 'P')
              792  COMPARE_OP               in
          794_796  POP_JUMP_IF_FALSE   812  'to 812'

 L. 236       798  LOAD_STR                 'P'
              800  DUP_TOP          
              802  LOAD_FAST                'self'
              804  STORE_ATTR               mode
              806  LOAD_FAST                'self'
              808  STORE_ATTR               rawmode
              810  JUMP_FORWARD        836  'to 836'
            812_0  COME_FROM           794  '794'

 L. 237       812  LOAD_FAST                'self'
              814  LOAD_ATTR                mode
              816  LOAD_CONST               ('LA', 'PA')
              818  COMPARE_OP               in
          820_822  POP_JUMP_IF_FALSE   836  'to 836'

 L. 238       824  LOAD_STR                 'PA'
              826  LOAD_FAST                'self'
              828  STORE_ATTR               mode

 L. 239       830  LOAD_STR                 'PA;L'
              832  LOAD_FAST                'self'
              834  STORE_ATTR               rawmode
            836_0  COME_FROM           820  '820'
            836_1  COME_FROM           810  '810'

 L. 240       836  LOAD_GLOBAL              ImagePalette
              838  LOAD_METHOD              raw
              840  LOAD_STR                 'RGB;L'
              842  LOAD_FAST                'palette'
              844  CALL_METHOD_2         2  ''
              846  LOAD_FAST                'self'
              848  STORE_ATTR               palette
            850_0  COME_FROM           784  '784'
            850_1  COME_FROM           756  '756'
              850  JUMP_FORWARD        892  'to 892'
            852_0  COME_FROM           744  '744'

 L. 241       852  LOAD_FAST                'self'
              854  LOAD_ATTR                mode
              856  LOAD_STR                 'RGB'
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_FALSE   892  'to 892'

 L. 242       864  LOAD_FAST                'greyscale'
          866_868  POP_JUMP_IF_FALSE   876  'to 876'
              870  LOAD_FAST                'linear'
          872_874  POP_JUMP_IF_TRUE    892  'to 892'
            876_0  COME_FROM           866  '866'

 L. 243       876  LOAD_LISTCOMP            '<code_object <listcomp>>'
              878  LOAD_STR                 'ImImageFile._open.<locals>.<listcomp>'
              880  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              882  LOAD_FAST                'palette'
              884  GET_ITER         
              886  CALL_FUNCTION_1       1  ''
              888  LOAD_FAST                'self'
              890  STORE_ATTR               lut
            892_0  COME_FROM           872  '872'
            892_1  COME_FROM           860  '860'
            892_2  COME_FROM           850  '850'
            892_3  COME_FROM           620  '620'

 L. 245       892  LOAD_CONST               0
              894  LOAD_FAST                'self'
              896  STORE_ATTR               frame

 L. 247       898  LOAD_FAST                'self'
              900  LOAD_ATTR                fp
              902  LOAD_METHOD              tell
              904  CALL_METHOD_0         0  ''
              906  DUP_TOP          
              908  LOAD_FAST                'self'
              910  STORE_ATTR               _ImImageFile__offset
              912  STORE_FAST               'offs'

 L. 249       914  LOAD_FAST                'self'
              916  LOAD_ATTR                fp
              918  LOAD_FAST                'self'
              920  STORE_ATTR               _ImImageFile__fp

 L. 251       922  LOAD_FAST                'self'
              924  LOAD_ATTR                rawmode
              926  LOAD_CONST               None
              928  LOAD_CONST               2
              930  BUILD_SLICE_2         2 
              932  BINARY_SUBSCR    
              934  LOAD_STR                 'F;'
              936  COMPARE_OP               ==
          938_940  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 254       942  SETUP_FINALLY      1014  'to 1014'

 L. 256       944  LOAD_GLOBAL              int
              946  LOAD_FAST                'self'
              948  LOAD_ATTR                rawmode
              950  LOAD_CONST               2
              952  LOAD_CONST               None
              954  BUILD_SLICE_2         2 
              956  BINARY_SUBSCR    
              958  CALL_FUNCTION_1       1  ''
              960  STORE_FAST               'bits'

 L. 257       962  LOAD_FAST                'bits'
              964  LOAD_CONST               (8, 16, 32)
              966  COMPARE_OP               not-in
          968_970  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 258       972  LOAD_STR                 'bit'
              974  LOAD_CONST               (0, 0)
              976  LOAD_FAST                'self'
              978  LOAD_ATTR                size
              980  BINARY_ADD       
              982  LOAD_FAST                'offs'
              984  LOAD_FAST                'bits'
              986  LOAD_CONST               8
              988  LOAD_CONST               3
              990  LOAD_CONST               0
              992  LOAD_CONST               -1
              994  BUILD_TUPLE_5         5 
              996  BUILD_TUPLE_4         4 
              998  BUILD_LIST_1          1 
             1000  LOAD_FAST                'self'
             1002  STORE_ATTR               tile

 L. 259      1004  POP_BLOCK        
             1006  LOAD_CONST               None
             1008  RETURN_VALUE     
           1010_0  COME_FROM           968  '968'
             1010  POP_BLOCK        
             1012  JUMP_FORWARD       1036  'to 1036'
           1014_0  COME_FROM_FINALLY   942  '942'

 L. 260      1014  DUP_TOP          
             1016  LOAD_GLOBAL              ValueError
             1018  COMPARE_OP               exception-match
         1020_1022  POP_JUMP_IF_FALSE  1034  'to 1034'
             1024  POP_TOP          
             1026  POP_TOP          
             1028  POP_TOP          

 L. 261      1030  POP_EXCEPT       
             1032  BREAK_LOOP         1036  'to 1036'
           1034_0  COME_FROM          1020  '1020'
             1034  END_FINALLY      
           1036_0  COME_FROM          1032  '1032'
           1036_1  COME_FROM          1012  '1012'
           1036_2  COME_FROM           938  '938'

 L. 263      1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                rawmode
             1040  LOAD_CONST               ('RGB;T', 'RYB;T')
             1042  COMPARE_OP               in
         1044_1046  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 266      1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                size
             1052  LOAD_CONST               0
             1054  BINARY_SUBSCR    
             1056  LOAD_FAST                'self'
             1058  LOAD_ATTR                size
             1060  LOAD_CONST               1
             1062  BINARY_SUBSCR    
             1064  BINARY_MULTIPLY  
             1066  STORE_FAST               'size'

 L. 268      1068  LOAD_STR                 'raw'
             1070  LOAD_CONST               (0, 0)
             1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                size
             1076  BINARY_ADD       
             1078  LOAD_FAST                'offs'
             1080  LOAD_CONST               ('G', 0, -1)
             1082  BUILD_TUPLE_4         4 

 L. 269      1084  LOAD_STR                 'raw'
             1086  LOAD_CONST               (0, 0)
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                size
             1092  BINARY_ADD       
             1094  LOAD_FAST                'offs'
             1096  LOAD_FAST                'size'
             1098  BINARY_ADD       
             1100  LOAD_CONST               ('R', 0, -1)
             1102  BUILD_TUPLE_4         4 

 L. 270      1104  LOAD_STR                 'raw'
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

 L. 267      1128  BUILD_LIST_3          3 
             1130  LOAD_FAST                'self'
             1132  STORE_ATTR               tile
             1134  JUMP_FORWARD       1166  'to 1166'
           1136_0  COME_FROM          1044  '1044'

 L. 274      1136  LOAD_STR                 'raw'
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

Parse error at or near `LOAD_CONST' instruction at offset 1006

                    @property
                    def n_frames(self):
                        return self.info[FRAMES]

                    @property
                    def is_animated(self):
                        return self.info[FRAMES] > 1

                    def seek(self, frame):
                        if not self._seek_check(frame):
                            return
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
                    except KeyError:
                        raise ValueError('Cannot save %s images as IM' % im.mode)
                    else:
                        frames = im.encoderinfo.get('frames', 1)
                        fp.write(('Image type: %s image\r\n' % image_type).encode('ascii'))
                        if filename:
                            name, ext = os.path.splitext(os.path.basename(filename))
                            name = ''.join([name[:92 - len(ext)], ext])
                            fp.write(('Name: %s\r\n' % name).encode('ascii'))
                        fp.write(('Image size (x*y): %d*%d\r\n' % im.size).encode('ascii'))
                        fp.write(('File size (no of images): %d\r\n' % frames).encode('ascii'))
                        if im.mode in ('P', 'PA'):
                            fp.write(b'Lut: 1\r\n')
                        fp.write(b'\x00' * (511 - fp.tell) + b'\x1a')
                        if im.mode in ('P', 'PA'):
                            fp.write(im.im.getpalette('RGB', 'RGB;L'))
                        ImageFile._save(im, fp, [('raw', (0, 0) + im.size, 0, (rawmode, 0, -1))])


                Image.register_open(ImImageFile.format, ImImageFile)
                Image.register_save(ImImageFile.format, _save)
                Image.register_extension(ImImageFile.format, '.im')