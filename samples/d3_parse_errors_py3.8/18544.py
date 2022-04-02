# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\JpegImagePlugin.py
import array, io, os, struct, subprocess, tempfile, warnings
from . import Image, ImageFile, TiffImagePlugin
from ._binary import i8, i16be as i16, i32be as i32, o8
from .JpegPresets import presets

def Skip(self, marker):
    n = i16(self.fp.read(2)) - 2
    ImageFile._safe_read(self.fp, n)


def APP--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              i16
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               2
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               2
               16  BINARY_SUBTRACT  
               18  STORE_FAST               'n'

 L.  61        20  LOAD_GLOBAL              ImageFile
               22  LOAD_METHOD              _safe_read
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_FAST                'n'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               's'

 L.  63        34  LOAD_STR                 'APP%d'
               36  LOAD_FAST                'marker'
               38  LOAD_CONST               15
               40  BINARY_AND       
               42  BINARY_MODULO    
               44  STORE_FAST               'app'

 L.  65        46  LOAD_FAST                's'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                app
               52  LOAD_FAST                'app'
               54  STORE_SUBSCR     

 L.  66        56  LOAD_FAST                'self'
               58  LOAD_ATTR                applist
               60  LOAD_METHOD              append
               62  LOAD_FAST                'app'
               64  LOAD_FAST                's'
               66  BUILD_TUPLE_2         2 
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  68        72  LOAD_FAST                'marker'
               74  LOAD_CONST               65504
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   232  'to 232'
               80  LOAD_FAST                's'
               82  LOAD_CONST               None
               84  LOAD_CONST               4
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  LOAD_CONST               b'JFIF'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   232  'to 232'

 L.  70        96  LOAD_GLOBAL              i16
               98  LOAD_FAST                's'
              100  LOAD_CONST               5
              102  CALL_FUNCTION_2       2  ''
              104  DUP_TOP          
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                info
              110  LOAD_STR                 'jfif'
              112  STORE_SUBSCR     
              114  STORE_FAST               'version'

 L.  71       116  LOAD_GLOBAL              divmod
              118  LOAD_FAST                'version'
              120  LOAD_CONST               256
              122  CALL_FUNCTION_2       2  ''
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                info
              128  LOAD_STR                 'jfif_version'
              130  STORE_SUBSCR     

 L.  73       132  SETUP_FINALLY       170  'to 170'

 L.  74       134  LOAD_GLOBAL              i8
              136  LOAD_FAST                's'
              138  LOAD_CONST               7
              140  BINARY_SUBSCR    
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'jfif_unit'

 L.  75       146  LOAD_GLOBAL              i16
              148  LOAD_FAST                's'
              150  LOAD_CONST               8
              152  CALL_FUNCTION_2       2  ''
              154  LOAD_GLOBAL              i16
              156  LOAD_FAST                's'
              158  LOAD_CONST               10
              160  CALL_FUNCTION_2       2  ''
              162  BUILD_TUPLE_2         2 
              164  STORE_FAST               'jfif_density'
              166  POP_BLOCK        
              168  JUMP_FORWARD        190  'to 190'
            170_0  COME_FROM_FINALLY   132  '132'

 L.  76       170  DUP_TOP          
              172  LOAD_GLOBAL              Exception
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   188  'to 188'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L.  77       184  POP_EXCEPT       
              186  JUMP_FORWARD        876  'to 876'
            188_0  COME_FROM           176  '176'
              188  END_FINALLY      
            190_0  COME_FROM           168  '168'

 L.  79       190  LOAD_FAST                'jfif_unit'
              192  LOAD_CONST               1
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   208  'to 208'

 L.  80       198  LOAD_FAST                'jfif_density'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                info
              204  LOAD_STR                 'dpi'
              206  STORE_SUBSCR     
            208_0  COME_FROM           196  '196'

 L.  81       208  LOAD_FAST                'jfif_unit'
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                info
              214  LOAD_STR                 'jfif_unit'
              216  STORE_SUBSCR     

 L.  82       218  LOAD_FAST                'jfif_density'
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                info
              224  LOAD_STR                 'jfif_density'
              226  STORE_SUBSCR     
          228_230  JUMP_FORWARD        876  'to 876'
            232_0  COME_FROM            94  '94'
            232_1  COME_FROM            78  '78'

 L.  83       232  LOAD_FAST                'marker'
              234  LOAD_CONST               65505
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   286  'to 286'
              242  LOAD_FAST                's'
              244  LOAD_CONST               None
              246  LOAD_CONST               5
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  LOAD_CONST               b'Exif\x00'
              254  COMPARE_OP               ==
          256_258  POP_JUMP_IF_FALSE   286  'to 286'

 L.  84       260  LOAD_STR                 'exif'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                info
              266  COMPARE_OP               not-in
          268_270  POP_JUMP_IF_FALSE   876  'to 876'

 L.  86       272  LOAD_FAST                's'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                info
              278  LOAD_STR                 'exif'
              280  STORE_SUBSCR     
          282_284  JUMP_FORWARD        876  'to 876'
            286_0  COME_FROM           256  '256'
            286_1  COME_FROM           238  '238'

 L.  87       286  LOAD_FAST                'marker'
              288  LOAD_CONST               65506
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   328  'to 328'
              296  LOAD_FAST                's'
              298  LOAD_CONST               None
              300  LOAD_CONST               5
              302  BUILD_SLICE_2         2 
              304  BINARY_SUBSCR    
              306  LOAD_CONST               b'FPXR\x00'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   328  'to 328'

 L.  89       314  LOAD_FAST                's'
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                info
              320  LOAD_STR                 'flashpix'
              322  STORE_SUBSCR     
          324_326  JUMP_FORWARD        876  'to 876'
            328_0  COME_FROM           310  '310'
            328_1  COME_FROM           292  '292'

 L.  90       328  LOAD_FAST                'marker'
              330  LOAD_CONST               65506
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   372  'to 372'
              338  LOAD_FAST                's'
              340  LOAD_CONST               None
              342  LOAD_CONST               12
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  LOAD_CONST               b'ICC_PROFILE\x00'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   372  'to 372'

 L. 102       356  LOAD_FAST                'self'
              358  LOAD_ATTR                icclist
              360  LOAD_METHOD              append
              362  LOAD_FAST                's'
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
          368_370  JUMP_FORWARD        876  'to 876'
            372_0  COME_FROM           352  '352'
            372_1  COME_FROM           334  '334'

 L. 103       372  LOAD_FAST                'marker'
              374  LOAD_CONST               65517
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   710  'to 710'

 L. 104       382  LOAD_FAST                's'
              384  LOAD_CONST               None
              386  LOAD_CONST               14
              388  BUILD_SLICE_2         2 
              390  BINARY_SUBSCR    
              392  LOAD_CONST               b'Photoshop 3.0\x00'
              394  COMPARE_OP               ==
          396_398  POP_JUMP_IF_FALSE   876  'to 876'

 L. 105       400  LOAD_FAST                's'
              402  LOAD_CONST               14
              404  LOAD_CONST               None
              406  BUILD_SLICE_2         2 
              408  BINARY_SUBSCR    
              410  STORE_FAST               'blocks'

 L. 107       412  LOAD_CONST               0
              414  STORE_FAST               'offset'

 L. 108       416  BUILD_MAP_0           0 
              418  STORE_FAST               'photoshop'
            420_0  COME_FROM           694  '694'
            420_1  COME_FROM           682  '682'

 L. 109       420  LOAD_FAST                'blocks'
              422  LOAD_FAST                'offset'
              424  LOAD_FAST                'offset'
              426  LOAD_CONST               4
              428  BINARY_ADD       
              430  BUILD_SLICE_2         2 
              432  BINARY_SUBSCR    
              434  LOAD_CONST               b'8BIM'
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   698  'to 698'

 L. 110       442  LOAD_FAST                'offset'
              444  LOAD_CONST               4
              446  INPLACE_ADD      
              448  STORE_FAST               'offset'

 L. 112       450  SETUP_FINALLY       466  'to 466'

 L. 113       452  LOAD_GLOBAL              i16
              454  LOAD_FAST                'blocks'
              456  LOAD_FAST                'offset'
              458  CALL_FUNCTION_2       2  ''
              460  STORE_FAST               'code'
              462  POP_BLOCK        
              464  JUMP_FORWARD        496  'to 496'
            466_0  COME_FROM_FINALLY   450  '450'

 L. 114       466  DUP_TOP          
              468  LOAD_GLOBAL              struct
              470  LOAD_ATTR                error
              472  COMPARE_OP               exception-match
          474_476  POP_JUMP_IF_FALSE   494  'to 494'
              478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L. 115       484  POP_EXCEPT       
          486_488  BREAK_LOOP          698  'to 698'
              490  POP_EXCEPT       
              492  JUMP_FORWARD        496  'to 496'
            494_0  COME_FROM           474  '474'
              494  END_FINALLY      
            496_0  COME_FROM           492  '492'
            496_1  COME_FROM           464  '464'

 L. 116       496  LOAD_FAST                'offset'
              498  LOAD_CONST               2
              500  INPLACE_ADD      
              502  STORE_FAST               'offset'

 L. 118       504  LOAD_GLOBAL              i8
              506  LOAD_FAST                'blocks'
              508  LOAD_FAST                'offset'
              510  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  ''
              514  STORE_FAST               'name_len'

 L. 120       516  LOAD_CONST               1
              518  LOAD_FAST                'offset'
              520  BINARY_ADD       
              522  LOAD_FAST                'name_len'
              524  BINARY_ADD       
              526  STORE_FAST               'offset'

 L. 121       528  LOAD_FAST                'offset'
              530  LOAD_CONST               1
              532  BINARY_AND       
          534_536  POP_JUMP_IF_FALSE   546  'to 546'

 L. 122       538  LOAD_FAST                'offset'
              540  LOAD_CONST               1
              542  INPLACE_ADD      
              544  STORE_FAST               'offset'
            546_0  COME_FROM           534  '534'

 L. 124       546  LOAD_GLOBAL              i32
              548  LOAD_FAST                'blocks'
              550  LOAD_FAST                'offset'
              552  CALL_FUNCTION_2       2  ''
              554  STORE_FAST               'size'

 L. 125       556  LOAD_FAST                'offset'
              558  LOAD_CONST               4
              560  INPLACE_ADD      
              562  STORE_FAST               'offset'

 L. 126       564  LOAD_FAST                'blocks'
              566  LOAD_FAST                'offset'
              568  LOAD_FAST                'offset'
              570  LOAD_FAST                'size'
              572  BINARY_ADD       
              574  BUILD_SLICE_2         2 
              576  BINARY_SUBSCR    
              578  STORE_FAST               'data'

 L. 127       580  LOAD_FAST                'code'
              582  LOAD_CONST               1005
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   660  'to 660'

 L. 129       590  LOAD_GLOBAL              i32
              592  LOAD_FAST                'data'
              594  LOAD_CONST               None
              596  LOAD_CONST               4
              598  BUILD_SLICE_2         2 
              600  BINARY_SUBSCR    
              602  CALL_FUNCTION_1       1  ''
              604  LOAD_CONST               65536
              606  BINARY_TRUE_DIVIDE

 L. 130       608  LOAD_GLOBAL              i16
              610  LOAD_FAST                'data'
              612  LOAD_CONST               4
              614  LOAD_CONST               8
              616  BUILD_SLICE_2         2 
              618  BINARY_SUBSCR    
              620  CALL_FUNCTION_1       1  ''

 L. 131       622  LOAD_GLOBAL              i32
              624  LOAD_FAST                'data'
              626  LOAD_CONST               8
              628  LOAD_CONST               12
              630  BUILD_SLICE_2         2 
              632  BINARY_SUBSCR    
              634  CALL_FUNCTION_1       1  ''
              636  LOAD_CONST               65536
              638  BINARY_TRUE_DIVIDE

 L. 132       640  LOAD_GLOBAL              i16
              642  LOAD_FAST                'data'
              644  LOAD_CONST               12
              646  LOAD_CONST               None
              648  BUILD_SLICE_2         2 
              650  BINARY_SUBSCR    
              652  CALL_FUNCTION_1       1  ''

 L. 128       654  LOAD_CONST               ('XResolution', 'DisplayedUnitsX', 'YResolution', 'DisplayedUnitsY')
              656  BUILD_CONST_KEY_MAP_4     4 
              658  STORE_FAST               'data'
            660_0  COME_FROM           586  '586'

 L. 134       660  LOAD_FAST                'data'
              662  LOAD_FAST                'photoshop'
              664  LOAD_FAST                'code'
              666  STORE_SUBSCR     

 L. 135       668  LOAD_FAST                'offset'
              670  LOAD_FAST                'size'
              672  BINARY_ADD       
              674  STORE_FAST               'offset'

 L. 136       676  LOAD_FAST                'offset'
              678  LOAD_CONST               1
              680  BINARY_AND       
          682_684  POP_JUMP_IF_FALSE_BACK   420  'to 420'

 L. 137       686  LOAD_FAST                'offset'
              688  LOAD_CONST               1
              690  INPLACE_ADD      
              692  STORE_FAST               'offset'
          694_696  JUMP_BACK           420  'to 420'
            698_0  COME_FROM           486  '486'
            698_1  COME_FROM           438  '438'

 L. 138       698  LOAD_FAST                'photoshop'
              700  LOAD_FAST                'self'
              702  LOAD_ATTR                info
              704  LOAD_STR                 'photoshop'
              706  STORE_SUBSCR     
              708  JUMP_FORWARD        876  'to 876'
            710_0  COME_FROM           378  '378'

 L. 139       710  LOAD_FAST                'marker'
              712  LOAD_CONST               65518
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   806  'to 806'
              720  LOAD_FAST                's'
              722  LOAD_CONST               None
              724  LOAD_CONST               5
              726  BUILD_SLICE_2         2 
              728  BINARY_SUBSCR    
              730  LOAD_CONST               b'Adobe'
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   806  'to 806'

 L. 140       738  LOAD_GLOBAL              i16
              740  LOAD_FAST                's'
              742  LOAD_CONST               5
              744  CALL_FUNCTION_2       2  ''
              746  LOAD_FAST                'self'
              748  LOAD_ATTR                info
              750  LOAD_STR                 'adobe'
              752  STORE_SUBSCR     

 L. 142       754  SETUP_FINALLY       772  'to 772'

 L. 143       756  LOAD_GLOBAL              i8
              758  LOAD_FAST                's'
              760  LOAD_CONST               1
              762  BINARY_SUBSCR    
              764  CALL_FUNCTION_1       1  ''
              766  STORE_FAST               'adobe_transform'
              768  POP_BLOCK        
              770  JUMP_FORWARD        794  'to 794'
            772_0  COME_FROM_FINALLY   754  '754'

 L. 144       772  DUP_TOP          
              774  LOAD_GLOBAL              Exception
              776  COMPARE_OP               exception-match
          778_780  POP_JUMP_IF_FALSE   792  'to 792'
              782  POP_TOP          
              784  POP_TOP          
              786  POP_TOP          

 L. 145       788  POP_EXCEPT       
              790  BREAK_LOOP          804  'to 804'
            792_0  COME_FROM           778  '778'
              792  END_FINALLY      
            794_0  COME_FROM           770  '770'

 L. 147       794  LOAD_FAST                'adobe_transform'
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                info
              800  LOAD_STR                 'adobe_transform'
              802  STORE_SUBSCR     
            804_0  COME_FROM           790  '790'
              804  JUMP_FORWARD        876  'to 876'
            806_0  COME_FROM           734  '734'
            806_1  COME_FROM           716  '716'

 L. 148       806  LOAD_FAST                'marker'
              808  LOAD_CONST               65506
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_FALSE   876  'to 876'
              816  LOAD_FAST                's'
              818  LOAD_CONST               None
              820  LOAD_CONST               4
              822  BUILD_SLICE_2         2 
              824  BINARY_SUBSCR    
              826  LOAD_CONST               b'MPF\x00'
              828  COMPARE_OP               ==
          830_832  POP_JUMP_IF_FALSE   876  'to 876'

 L. 150       834  LOAD_FAST                's'
              836  LOAD_CONST               4
              838  LOAD_CONST               None
              840  BUILD_SLICE_2         2 
              842  BINARY_SUBSCR    
              844  LOAD_FAST                'self'
              846  LOAD_ATTR                info
              848  LOAD_STR                 'mp'
              850  STORE_SUBSCR     

 L. 153       852  LOAD_FAST                'self'
              854  LOAD_ATTR                fp
              856  LOAD_METHOD              tell
              858  CALL_METHOD_0         0  ''
              860  LOAD_FAST                'n'
              862  BINARY_SUBTRACT  
              864  LOAD_CONST               4
              866  BINARY_ADD       
              868  LOAD_FAST                'self'
              870  LOAD_ATTR                info
              872  LOAD_STR                 'mpoffset'
              874  STORE_SUBSCR     
            876_0  COME_FROM           830  '830'
            876_1  COME_FROM           812  '812'
            876_2  COME_FROM           804  '804'
            876_3  COME_FROM           708  '708'
            876_4  COME_FROM           396  '396'
            876_5  COME_FROM           368  '368'
            876_6  COME_FROM           324  '324'
            876_7  COME_FROM           282  '282'
            876_8  COME_FROM           268  '268'
            876_9  COME_FROM           228  '228'
           876_10  COME_FROM           186  '186'

 L. 156       876  LOAD_STR                 'dpi'
              878  LOAD_FAST                'self'
              880  LOAD_ATTR                info
              882  COMPARE_OP               not-in
          884_886  POP_JUMP_IF_FALSE  1070  'to 1070'
              888  LOAD_STR                 'exif'
              890  LOAD_FAST                'self'
              892  LOAD_ATTR                info
              894  COMPARE_OP               in
          896_898  POP_JUMP_IF_FALSE  1070  'to 1070'

 L. 157       900  SETUP_FINALLY      1030  'to 1030'

 L. 158       902  LOAD_FAST                'self'
              904  LOAD_METHOD              getexif
              906  CALL_METHOD_0         0  ''
              908  STORE_FAST               'exif'

 L. 159       910  LOAD_FAST                'exif'
              912  LOAD_CONST               296
              914  BINARY_SUBSCR    
              916  STORE_FAST               'resolution_unit'

 L. 160       918  LOAD_FAST                'exif'
              920  LOAD_CONST               282
              922  BINARY_SUBSCR    
              924  STORE_FAST               'x_resolution'

 L. 161       926  SETUP_FINALLY       952  'to 952'

 L. 162       928  LOAD_GLOBAL              float
              930  LOAD_FAST                'x_resolution'
              932  LOAD_CONST               0
              934  BINARY_SUBSCR    
              936  CALL_FUNCTION_1       1  ''
              938  LOAD_FAST                'x_resolution'
              940  LOAD_CONST               1
              942  BINARY_SUBSCR    
              944  BINARY_TRUE_DIVIDE
              946  STORE_FAST               'dpi'
              948  POP_BLOCK        
              950  JUMP_FORWARD        978  'to 978'
            952_0  COME_FROM_FINALLY   926  '926'

 L. 163       952  DUP_TOP          
              954  LOAD_GLOBAL              TypeError
              956  COMPARE_OP               exception-match
          958_960  POP_JUMP_IF_FALSE   976  'to 976'
              962  POP_TOP          
              964  POP_TOP          
              966  POP_TOP          

 L. 164       968  LOAD_FAST                'x_resolution'
              970  STORE_FAST               'dpi'
              972  POP_EXCEPT       
              974  JUMP_FORWARD        978  'to 978'
            976_0  COME_FROM           958  '958'
              976  END_FINALLY      
            978_0  COME_FROM           974  '974'
            978_1  COME_FROM           950  '950'

 L. 165       978  LOAD_FAST                'resolution_unit'
              980  LOAD_CONST               3
              982  COMPARE_OP               ==
          984_986  POP_JUMP_IF_FALSE   996  'to 996'

 L. 167       988  LOAD_FAST                'dpi'
              990  LOAD_CONST               2.54
              992  INPLACE_MULTIPLY 
              994  STORE_FAST               'dpi'
            996_0  COME_FROM           984  '984'

 L. 168       996  LOAD_GLOBAL              int
              998  LOAD_FAST                'dpi'
             1000  LOAD_CONST               0.5
             1002  BINARY_ADD       
             1004  CALL_FUNCTION_1       1  ''
             1006  LOAD_GLOBAL              int
             1008  LOAD_FAST                'dpi'
             1010  LOAD_CONST               0.5
             1012  BINARY_ADD       
             1014  CALL_FUNCTION_1       1  ''
             1016  BUILD_TUPLE_2         2 
             1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                info
             1022  LOAD_STR                 'dpi'
             1024  STORE_SUBSCR     
             1026  POP_BLOCK        
             1028  JUMP_FORWARD       1070  'to 1070'
           1030_0  COME_FROM_FINALLY   900  '900'

 L. 169      1030  DUP_TOP          
             1032  LOAD_GLOBAL              KeyError
             1034  LOAD_GLOBAL              SyntaxError
             1036  LOAD_GLOBAL              ValueError
             1038  LOAD_GLOBAL              ZeroDivisionError
             1040  BUILD_TUPLE_4         4 
             1042  COMPARE_OP               exception-match
         1044_1046  POP_JUMP_IF_FALSE  1068  'to 1068'
             1048  POP_TOP          
             1050  POP_TOP          
             1052  POP_TOP          

 L. 174      1054  LOAD_CONST               (72, 72)
             1056  LOAD_FAST                'self'
             1058  LOAD_ATTR                info
             1060  LOAD_STR                 'dpi'
             1062  STORE_SUBSCR     
             1064  POP_EXCEPT       
             1066  JUMP_FORWARD       1070  'to 1070'
           1068_0  COME_FROM          1044  '1044'
             1068  END_FINALLY      
           1070_0  COME_FROM          1066  '1066'
           1070_1  COME_FROM          1028  '1028'
           1070_2  COME_FROM           896  '896'
           1070_3  COME_FROM           884  '884'

Parse error at or near `END_FINALLY' instruction at offset 792


def COM(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self.app['COM'] = s
    self.applist.append(('COM', s))


def SOF(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self._size = (i16(s[3:]), i16(s[1:]))
    self.bits = i8(s[0])
    if self.bits != 8:
        raise SyntaxError('cannot handle %d-bit layers' % self.bits)
    self.layers = i8(s[5])
    if self.layers == 1:
        self.mode = 'L'
    elif self.layers == 3:
        self.mode = 'RGB'
    elif self.layers == 4:
        self.mode = 'CMYK'
    else:
        raise SyntaxError('cannot handle %d-layer images' % self.layers)
    if marker in (65474, 65478, 65482, 65486):
        self.info['progressive'] = self.info['progression'] = 1
    if self.icclist:
        self.icclist.sort
        if i8(self.icclist[0][13]) == len(self.icclist):
            profile = []
            for p in self.icclist:
                profile.append(p[14:])
            else:
                icc_profile = (b'').join(profile)

        else:
            icc_profile = None
        self.info['icc_profile'] = icc_profile
        self.icclist = None
    for i in range(6, len(s), 3):
        t = s[i:i + 3]
        self.layer.append((t[0], i8(t[1]) // 16, i8(t[1]) & 15, i8(t[2])))


def DQT(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    while True:
        if len(s):
            if len(s) < 65:
                raise SyntaxError('bad quantization table marker')
            v = i8(s[0])
            if v // 16 == 0:
                self.quantization[v & 15] = array.array('B', s[1:65])
                s = s[65:]
            else:
                return


MARKER = {65472:(
  'SOF0', 'Baseline DCT', SOF), 
 65473:(
  'SOF1', 'Extended Sequential DCT', SOF), 
 65474:(
  'SOF2', 'Progressive DCT', SOF), 
 65475:(
  'SOF3', 'Spatial lossless', SOF), 
 65476:(
  'DHT', 'Define Huffman table', Skip), 
 65477:(
  'SOF5', 'Differential sequential DCT', SOF), 
 65478:(
  'SOF6', 'Differential progressive DCT', SOF), 
 65479:(
  'SOF7', 'Differential spatial', SOF), 
 65480:('JPG', 'Extension', None), 
 65481:(
  'SOF9', 'Extended sequential DCT (AC)', SOF), 
 65482:(
  'SOF10', 'Progressive DCT (AC)', SOF), 
 65483:(
  'SOF11', 'Spatial lossless DCT (AC)', SOF), 
 65484:(
  'DAC', 'Define arithmetic coding conditioning', Skip), 
 65485:(
  'SOF13', 'Differential sequential DCT (AC)', SOF), 
 65486:(
  'SOF14', 'Differential progressive DCT (AC)', SOF), 
 65487:(
  'SOF15', 'Differential spatial (AC)', SOF), 
 65488:('RST0', 'Restart 0', None), 
 65489:('RST1', 'Restart 1', None), 
 65490:('RST2', 'Restart 2', None), 
 65491:('RST3', 'Restart 3', None), 
 65492:('RST4', 'Restart 4', None), 
 65493:('RST5', 'Restart 5', None), 
 65494:('RST6', 'Restart 6', None), 
 65495:('RST7', 'Restart 7', None), 
 65496:('SOI', 'Start of image', None), 
 65497:('EOI', 'End of image', None), 
 65498:(
  'SOS', 'Start of scan', Skip), 
 65499:(
  'DQT', 'Define quantization table', DQT), 
 65500:(
  'DNL', 'Define number of lines', Skip), 
 65501:(
  'DRI', 'Define restart interval', Skip), 
 65502:(
  'DHP', 'Define hierarchical progression', SOF), 
 65503:(
  'EXP', 'Expand reference component', Skip), 
 65504:(
  'APP0', 'Application segment 0', APP), 
 65505:(
  'APP1', 'Application segment 1', APP), 
 65506:(
  'APP2', 'Application segment 2', APP), 
 65507:(
  'APP3', 'Application segment 3', APP), 
 65508:(
  'APP4', 'Application segment 4', APP), 
 65509:(
  'APP5', 'Application segment 5', APP), 
 65510:(
  'APP6', 'Application segment 6', APP), 
 65511:(
  'APP7', 'Application segment 7', APP), 
 65512:(
  'APP8', 'Application segment 8', APP), 
 65513:(
  'APP9', 'Application segment 9', APP), 
 65514:(
  'APP10', 'Application segment 10', APP), 
 65515:(
  'APP11', 'Application segment 11', APP), 
 65516:(
  'APP12', 'Application segment 12', APP), 
 65517:(
  'APP13', 'Application segment 13', APP), 
 65518:(
  'APP14', 'Application segment 14', APP), 
 65519:(
  'APP15', 'Application segment 15', APP), 
 65520:('JPG0', 'Extension 0', None), 
 65521:('JPG1', 'Extension 1', None), 
 65522:('JPG2', 'Extension 2', None), 
 65523:('JPG3', 'Extension 3', None), 
 65524:('JPG4', 'Extension 4', None), 
 65525:('JPG5', 'Extension 5', None), 
 65526:('JPG6', 'Extension 6', None), 
 65527:('JPG7', 'Extension 7', None), 
 65528:('JPG8', 'Extension 8', None), 
 65529:('JPG9', 'Extension 9', None), 
 65530:('JPG10', 'Extension 10', None), 
 65531:('JPG11', 'Extension 11', None), 
 65532:('JPG12', 'Extension 12', None), 
 65533:('JPG13', 'Extension 13', None), 
 65534:(
  'COM', 'Comment', COM)}

def _accept(prefix):
    return prefix[0:1] == b'\xff'


class JpegImageFile(ImageFile.ImageFile):
    format = 'JPEG'
    format_description = 'JPEG (ISO 10918)'

    def _open(self):
        s = self.fp.read(1)
        if i8(s) != 255:
            raise SyntaxError('not a JPEG file')
        self.bits = self.layers = 0
        self.layer = []
        self.huffman_dc = {}
        self.huffman_ac = {}
        self.quantization = {}
        self.app = {}
        self.applist = []
        self.icclist = []
        while True:
            while True:
                i = i8(s)
                if i == 255:
                    s = s + self.fp.read(1)
                    i = i16(s)
                else:
                    s = self.fp.read(1)

            if i in MARKER:
                name, description, handler = MARKER[i]
                if handler is not None:
                    handlerselfi
                elif i == 65498:
                    rawmode = self.mode
                    if self.mode == 'CMYK':
                        rawmode = 'CMYK;I'
                    self.tile = [
                     (
                      'jpeg', (0, 0) + self.size, 0, (rawmode, ''))]
                else:
                    s = self.fp.read(1)
            else:
                if not i == 0 or i == 65535:
                    s = b'\xff'
                else:
                    if i == 65280:
                        s = self.fp.read(1)
                    else:
                        raise SyntaxError('no marker found')

    def load_read(self, read_bytes):
        """
        internal: read more image data
        For premature EOF and LOAD_TRUNCATED_IMAGES adds EOI marker
        so libjpeg can finish decoding
        """
        s = self.fp.read(read_bytes)
        if not s:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                return b'\xff\xd9'
        return s

    def draft(self, mode, size):
        if len(self.tile) != 1:
            return
        if self.decoderconfig:
            return
        d, e, o, a = self.tile[0]
        scale = 1
        original_size = self.size
        if a[0] == 'RGB':
            if mode in ('L', 'YCbCr'):
                self.mode = mode
                a = (mode, '')
        if size:
            scale = min(self.size[0] // size[0])(self.size[1] // size[1])
            for s in (8, 4, 2, 1):
                if scale >= s:
                    break
            else:
                e = (
                 e[0],
                 e[1],
                 (e[2] - e[0] + s - 1) // s + e[0],
                 (e[3] - e[1] + s - 1) // s + e[1])
                self._size = (
                 (self.size[0] + s - 1) // s, (self.size[1] + s - 1) // s)
                scale = s

        self.tile = [
         (
          d, e, o, a)]
        self.decoderconfig = (scale, 0)
        box = (
         0, 0, original_size[0] / float(scale), original_size[1] / float(scale))
        return (
         self.mode, box)

    def load_djpeg(self):
        f, path = tempfile.mkstemp
        os.close(f)
        if os.path.exists(self.filename):
            subprocess.check_call(['djpeg', '-outfile', path, self.filename])
        else:
            raise ValueError('Invalid Filename')
        try:
            _im = Image.open(path)
            _im.load
            self.im = _im.im
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

        self.mode = self.im.mode
        self._size = self.im.size
        self.tile = []

    def _getexif(self):
        return _getexif(self)

    def _getmp(self):
        return _getmp(self)


def _fixup_dict(src_dict):
    exif = Image.Exif
    return exif._fixup_dict(src_dict)


def _getexif(self):
    if 'exif' not in self.info:
        return
    return dict(self.getexif)


def _getmp(self):
    try:
        data = self.info['mp']
    except KeyError:
        return
    else:
        file_contents = io.BytesIO(data)
        head = file_contents.read(8)
        endianness = '>' if head[:4] == b'MM\x00*' else '<'
        try:
            info = TiffImagePlugin.ImageFileDirectory_v2(head)
            file_contents.seek(info.next)
            info.load(file_contents)
            mp = dict(info)
        except Exception:
            raise SyntaxError('malformed MP Index (unreadable directory)')

        try:
            quant = mp[45057]
        except KeyError:
            raise SyntaxError('malformed MP Index (no number of images)')
        else:
            mpentries = []
            try:
                rawmpentries = mp[45058]
                for entrynum in range0quant:
                    unpackedentry = struct.unpack_from('{}LLLHH'.format(endianness), rawmpentries, entrynum * 16)
                    labels = ('Attribute', 'Size', 'DataOffset', 'EntryNo1', 'EntryNo2')
                    mpentry = dict(ziplabelsunpackedentry)
                    mpentryattr = {'DependentParentImageFlag':bool(mpentry['Attribute'] & 2147483648), 
                     'DependentChildImageFlag':bool(mpentry['Attribute'] & 1073741824), 
                     'RepresentativeImageFlag':bool(mpentry['Attribute'] & 536870912), 
                     'Reserved':mpentry['Attribute'] & 402653184 >> 27, 
                     'ImageDataFormat':mpentry['Attribute'] & 117440512 >> 24, 
                     'MPType':mpentry['Attribute'] & 16777215}
                    if mpentryattr['ImageDataFormat'] == 0:
                        mpentryattr['ImageDataFormat'] = 'JPEG'
                    else:
                        raise SyntaxError('unsupported picture format in MPO')
                    mptypemap = {0:'Undefined',  65537:'Large Thumbnail (VGA Equivalent)', 
                     65538:'Large Thumbnail (Full HD Equivalent)', 
                     131073:'Multi-Frame Image (Panorama)', 
                     131074:'Multi-Frame Image: (Disparity)', 
                     131075:'Multi-Frame Image: (Multi-Angle)', 
                     196608:'Baseline MP Primary Image'}
                    mpentryattr['MPType'] = mptypemap.get(mpentryattr['MPType'], 'Unknown')
                    mpentry['Attribute'] = mpentryattr
                    mpentries.append(mpentry)
                else:
                    mp[45058] = mpentries

            except KeyError:
                raise SyntaxError('malformed MP Index (bad MP Entry)')
            else:
                return mp


RAWMODE = {'1':'L', 
 'L':'L', 
 'RGB':'RGB', 
 'RGBX':'RGB', 
 'CMYK':'CMYK;I', 
 'YCbCr':'YCbCr'}
zigzag_index = (0, 1, 5, 6, 14, 15, 27, 28, 2, 4, 7, 13, 16, 26, 29, 42, 3, 8, 12,
                17, 25, 30, 41, 43, 9, 11, 18, 24, 31, 40, 44, 53, 10, 19, 23, 32,
                39, 45, 52, 54, 20, 22, 33, 38, 46, 51, 55, 60, 21, 34, 37, 47, 50,
                56, 59, 61, 35, 36, 48, 49, 57, 58, 62, 63)
samplings = {(1, 1, 1, 1, 1, 1):0, 
 (2, 1, 1, 1, 1, 1):1, 
 (2, 2, 1, 1, 1, 1):2}

def convert_dict_qtables(qtables):
    qtables = [qtables[key] for key in range(len(qtables)) if key in qtables]
    for idx, table in enumerate(qtables):
        qtables[idx] = [table[i] for i in zigzag_index]
    else:
        return qtables


def get_sampling(im):
    if not hasattrim'layers' or im.layers in (1, 4):
        return -1
    sampling = im.layer[0][1:3] + im.layer[1][1:3] + im.layer[2][1:3]
    return samplings.get(sampling, -1)


def _save(im, fp, filename):
    try:
        rawmode = RAWMODE[im.mode]
    except KeyError:
        raise OSError('cannot write mode %s as JPEG' % im.mode)
    else:
        info = im.encoderinfo
        dpi = [int(round(x)) for x in info.get('dpi', (0, 0))]
        quality = info.get('quality', 0)
        subsampling = info.get('subsampling', -1)
        qtables = info.get('qtables')
        if quality == 'keep':
            quality = 0
            subsampling = 'keep'
            qtables = 'keep'
        elif quality in presets:
            preset = presets[quality]
            quality = 0
            subsampling = preset.get('subsampling', -1)
            qtables = preset.get('quantization')
        elif not isinstancequalityint:
            raise ValueError('Invalid quality setting')
        else:
            if subsampling in presets:
                subsampling = presets[subsampling].get('subsampling', -1)
            if isinstanceqtablesstr:
                if qtables in presets:
                    qtables = presets[qtables].get('quantization')
        if subsampling == '4:4:4':
            subsampling = 0
        elif subsampling == '4:2:2':
            subsampling = 1
        elif subsampling == '4:2:0':
            subsampling = 2
        elif subsampling == '4:1:1':
            subsampling = 2
        elif subsampling == 'keep':
            if im.format != 'JPEG':
                raise ValueError("Cannot use 'keep' when original image is not a JPEG")
            subsampling = get_sampling(im)

        def validate_qtables(qtables):
            if qtables is None:
                return qtables
            if isinstanceqtablesstr:
                try:
                    lines = [int(num) for line in qtables.splitlines for num in line.split('#', 1)[0].split]
                except ValueError:
                    raise ValueError('Invalid quantization table')
                else:
                    qtables = [lines[s:s + 64] for s in range(0, len(lines), 64)]
                if isinstanceqtables(tuple, list, dict):
                    if isinstanceqtablesdict:
                        qtables = convert_dict_qtables(qtables)
                    elif isinstanceqtablestuple:
                        qtables = list(qtables)
                    if not 0 < len(qtables) < 5:
                        raise ValueError('None or too many quantization tables')
                    for idx, table in enumerate(qtables):
                        try:
                            if len(table) != 64:
                                raise TypeError
                            table = array.array('B', table)
                        except TypeError:
                            raise ValueError('Invalid quantization table')
                        else:
                            qtables[idx] = list(table)
                    else:
                        return qtables

        if qtables == 'keep':
            if im.format != 'JPEG':
                raise ValueError("Cannot use 'keep' when original image is not a JPEG")
            qtables = getattr(im, 'quantization', None)
        qtables = validate_qtables(qtables)
        extra = b''
        icc_profile = info.get('icc_profile')
        if icc_profile:
            ICC_OVERHEAD_LEN = 14
            MAX_BYTES_IN_MARKER = 65533
            MAX_DATA_BYTES_IN_MARKER = MAX_BYTES_IN_MARKER - ICC_OVERHEAD_LEN
            markers = []
            while True:
                if icc_profile:
                    markers.append(icc_profile[:MAX_DATA_BYTES_IN_MARKER])
                    icc_profile = icc_profile[MAX_DATA_BYTES_IN_MARKER:]

            i = 1
            for marker in markers:
                size = struct.pack('>H', 2 + ICC_OVERHEAD_LEN + len(marker))
                extra += b'\xff\xe2' + size + b'ICC_PROFILE\x00' + o8(i) + o8(len(markers)) + marker
                i += 1
            else:
                progressive = info.get('progressive', False) or info.get('progression', False)
                optimize = info.get('optimize', False)
                exif = info.get('exif', b'')
                if isinstanceexifImage.Exif:
                    exif = exif.tobytes
                im.encoderconfig = (
                 quality,
                 progressive,
                 info.get('smooth', 0),
                 optimize,
                 info.get('streamtype', 0),
                 dpi[0],
                 dpi[1],
                 subsampling,
                 qtables,
                 extra,
                 exif)
                bufsize = 0
                if optimize or progressive:
                    if im.mode == 'CMYK':
                        bufsize = 4 * im.size[0] * im.size[1]
                else:
                    pass
                if quality >= 95 or quality == 0:
                    bufsize = 2 * im.size[0] * im.size[1]
                else:
                    bufsize = im.size[0] * im.size[1]

        bufsize = max(ImageFile.MAXBLOCK, bufsize, len(exif) + 5, len(extra) + 1)
        ImageFile._save(im, fp, [('jpeg', (0, 0) + im.size, 0, rawmode)], bufsize)


def _save_cjpeg(im, fp, filename):
    tempfile = im._dump
    subprocess.check_call(['cjpeg', '-outfile', filename, tempfile])
    try:
        os.unlink(tempfile)
    except OSError:
        pass


def jpeg_factory(fp=None, filename=None):
    im = JpegImageFilefpfilename
    try:
        mpheader = im._getmp
        if mpheader[45057] > 1:
            from .MpoImagePlugin import MpoImageFile
            im = MpoImageFile.adopt(im, mpheader)
    except (TypeError, IndexError):
        pass
    except SyntaxError:
        warnings.warn('Image appears to be a malformed MPO file, it will be interpreted as a base JPEG file')
    else:
        return im


Image.register_open(JpegImageFile.format, jpeg_factory, _accept)
Image.register_save(JpegImageFile.format, _save)
Image.register_extensions(JpegImageFile.format, ['.jfif', '.jpe', '.jpg', '.jpeg'])
Image.register_mime(JpegImageFile.format, 'image/jpeg')