# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\JpegImagePlugin.py
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
              186  JUMP_FORWARD        852  'to 852'
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
          228_230  JUMP_FORWARD        852  'to 852'
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
          268_270  POP_JUMP_IF_FALSE   852  'to 852'

 L.  86       272  LOAD_FAST                's'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                info
              278  LOAD_STR                 'exif'
              280  STORE_SUBSCR     
          282_284  JUMP_FORWARD        852  'to 852'
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
          324_326  JUMP_FORWARD        852  'to 852'
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
          368_370  JUMP_FORWARD        852  'to 852'
            372_0  COME_FROM           352  '352'
            372_1  COME_FROM           334  '334'

 L. 103       372  LOAD_FAST                'marker'
              374  LOAD_CONST               65517
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   686  'to 686'
              382  LOAD_FAST                's'
              384  LOAD_CONST               None
              386  LOAD_CONST               14
              388  BUILD_SLICE_2         2 
              390  BINARY_SUBSCR    
              392  LOAD_CONST               b'Photoshop 3.0\x00'
              394  COMPARE_OP               ==
          396_398  POP_JUMP_IF_FALSE   686  'to 686'

 L. 105       400  LOAD_CONST               14
              402  STORE_FAST               'offset'

 L. 106       404  LOAD_FAST                'self'
              406  LOAD_ATTR                info
              408  LOAD_METHOD              setdefault
              410  LOAD_STR                 'photoshop'
              412  BUILD_MAP_0           0 
              414  CALL_METHOD_2         2  ''
              416  STORE_FAST               'photoshop'

 L. 107       418  LOAD_FAST                's'
              420  LOAD_FAST                'offset'
              422  LOAD_FAST                'offset'
              424  LOAD_CONST               4
              426  BINARY_ADD       
              428  BUILD_SLICE_2         2 
              430  BINARY_SUBSCR    
              432  LOAD_CONST               b'8BIM'
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_FALSE   852  'to 852'

 L. 108       440  SETUP_FINALLY       650  'to 650'

 L. 109       442  LOAD_FAST                'offset'
              444  LOAD_CONST               4
              446  INPLACE_ADD      
              448  STORE_FAST               'offset'

 L. 111       450  LOAD_GLOBAL              i16
              452  LOAD_FAST                's'
              454  LOAD_FAST                'offset'
              456  CALL_FUNCTION_2       2  ''
              458  STORE_FAST               'code'

 L. 112       460  LOAD_FAST                'offset'
              462  LOAD_CONST               2
              464  INPLACE_ADD      
              466  STORE_FAST               'offset'

 L. 114       468  LOAD_GLOBAL              i8
              470  LOAD_FAST                's'
              472  LOAD_FAST                'offset'
              474  BINARY_SUBSCR    
              476  CALL_FUNCTION_1       1  ''
              478  STORE_FAST               'name_len'

 L. 116       480  LOAD_FAST                'offset'
              482  LOAD_CONST               1
              484  LOAD_FAST                'name_len'
              486  BINARY_ADD       
              488  INPLACE_ADD      
              490  STORE_FAST               'offset'

 L. 117       492  LOAD_FAST                'offset'
              494  LOAD_FAST                'offset'
              496  LOAD_CONST               1
              498  BINARY_AND       
              500  INPLACE_ADD      
              502  STORE_FAST               'offset'

 L. 119       504  LOAD_GLOBAL              i32
              506  LOAD_FAST                's'
              508  LOAD_FAST                'offset'
              510  CALL_FUNCTION_2       2  ''
              512  STORE_FAST               'size'

 L. 120       514  LOAD_FAST                'offset'
              516  LOAD_CONST               4
              518  INPLACE_ADD      
              520  STORE_FAST               'offset'

 L. 121       522  LOAD_FAST                's'
              524  LOAD_FAST                'offset'
              526  LOAD_FAST                'offset'
              528  LOAD_FAST                'size'
              530  BINARY_ADD       
              532  BUILD_SLICE_2         2 
              534  BINARY_SUBSCR    
              536  STORE_FAST               'data'

 L. 122       538  LOAD_FAST                'code'
              540  LOAD_CONST               1005
              542  COMPARE_OP               ==
          544_546  POP_JUMP_IF_FALSE   618  'to 618'

 L. 124       548  LOAD_GLOBAL              i32
              550  LOAD_FAST                'data'
              552  LOAD_CONST               None
              554  LOAD_CONST               4
              556  BUILD_SLICE_2         2 
              558  BINARY_SUBSCR    
              560  CALL_FUNCTION_1       1  ''
              562  LOAD_CONST               65536
              564  BINARY_TRUE_DIVIDE

 L. 125       566  LOAD_GLOBAL              i16
              568  LOAD_FAST                'data'
              570  LOAD_CONST               4
              572  LOAD_CONST               8
              574  BUILD_SLICE_2         2 
              576  BINARY_SUBSCR    
              578  CALL_FUNCTION_1       1  ''

 L. 126       580  LOAD_GLOBAL              i32
              582  LOAD_FAST                'data'
              584  LOAD_CONST               8
              586  LOAD_CONST               12
              588  BUILD_SLICE_2         2 
              590  BINARY_SUBSCR    
              592  CALL_FUNCTION_1       1  ''
              594  LOAD_CONST               65536
              596  BINARY_TRUE_DIVIDE

 L. 127       598  LOAD_GLOBAL              i16
              600  LOAD_FAST                'data'
              602  LOAD_CONST               12
              604  LOAD_CONST               None
              606  BUILD_SLICE_2         2 
              608  BINARY_SUBSCR    
              610  CALL_FUNCTION_1       1  ''

 L. 123       612  LOAD_CONST               ('XResolution', 'DisplayedUnitsX', 'YResolution', 'DisplayedUnitsY')
              614  BUILD_CONST_KEY_MAP_4     4 
              616  STORE_FAST               'data'
            618_0  COME_FROM           544  '544'

 L. 129       618  LOAD_FAST                'data'
              620  LOAD_FAST                'photoshop'
              622  LOAD_FAST                'code'
              624  STORE_SUBSCR     

 L. 130       626  LOAD_FAST                'offset'
              628  LOAD_FAST                'size'
              630  INPLACE_ADD      
              632  STORE_FAST               'offset'

 L. 131       634  LOAD_FAST                'offset'
              636  LOAD_FAST                'offset'
              638  LOAD_CONST               1
              640  BINARY_AND       
              642  INPLACE_ADD      
              644  STORE_FAST               'offset'
              646  POP_BLOCK        
              648  JUMP_BACK           418  'to 418'
            650_0  COME_FROM_FINALLY   440  '440'

 L. 132       650  DUP_TOP          
              652  LOAD_GLOBAL              struct
              654  LOAD_ATTR                error
              656  COMPARE_OP               exception-match
          658_660  POP_JUMP_IF_FALSE   678  'to 678'
              662  POP_TOP          
              664  POP_TOP          
              666  POP_TOP          

 L. 133       668  POP_EXCEPT       
          670_672  JUMP_ABSOLUTE       852  'to 852'
              674  POP_EXCEPT       
              676  JUMP_BACK           418  'to 418'
            678_0  COME_FROM           658  '658'
              678  END_FINALLY      
          680_682  JUMP_BACK           418  'to 418'
              684  JUMP_FORWARD        852  'to 852'
            686_0  COME_FROM           396  '396'
            686_1  COME_FROM           378  '378'

 L. 135       686  LOAD_FAST                'marker'
              688  LOAD_CONST               65518
              690  COMPARE_OP               ==
          692_694  POP_JUMP_IF_FALSE   782  'to 782'
              696  LOAD_FAST                's'
              698  LOAD_CONST               None
              700  LOAD_CONST               5
              702  BUILD_SLICE_2         2 
              704  BINARY_SUBSCR    
              706  LOAD_CONST               b'Adobe'
              708  COMPARE_OP               ==
          710_712  POP_JUMP_IF_FALSE   782  'to 782'

 L. 136       714  LOAD_GLOBAL              i16
              716  LOAD_FAST                's'
              718  LOAD_CONST               5
              720  CALL_FUNCTION_2       2  ''
              722  LOAD_FAST                'self'
              724  LOAD_ATTR                info
              726  LOAD_STR                 'adobe'
              728  STORE_SUBSCR     

 L. 138       730  SETUP_FINALLY       748  'to 748'

 L. 139       732  LOAD_GLOBAL              i8
              734  LOAD_FAST                's'
              736  LOAD_CONST               1
              738  BINARY_SUBSCR    
              740  CALL_FUNCTION_1       1  ''
              742  STORE_FAST               'adobe_transform'
              744  POP_BLOCK        
              746  JUMP_FORWARD        770  'to 770'
            748_0  COME_FROM_FINALLY   730  '730'

 L. 140       748  DUP_TOP          
              750  LOAD_GLOBAL              Exception
              752  COMPARE_OP               exception-match
          754_756  POP_JUMP_IF_FALSE   768  'to 768'
              758  POP_TOP          
              760  POP_TOP          
              762  POP_TOP          

 L. 141       764  POP_EXCEPT       
              766  JUMP_FORWARD        780  'to 780'
            768_0  COME_FROM           754  '754'
              768  END_FINALLY      
            770_0  COME_FROM           746  '746'

 L. 143       770  LOAD_FAST                'adobe_transform'
              772  LOAD_FAST                'self'
              774  LOAD_ATTR                info
              776  LOAD_STR                 'adobe_transform'
              778  STORE_SUBSCR     
            780_0  COME_FROM           766  '766'
              780  JUMP_FORWARD        852  'to 852'
            782_0  COME_FROM           710  '710'
            782_1  COME_FROM           692  '692'

 L. 144       782  LOAD_FAST                'marker'
              784  LOAD_CONST               65506
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   852  'to 852'
              792  LOAD_FAST                's'
              794  LOAD_CONST               None
              796  LOAD_CONST               4
              798  BUILD_SLICE_2         2 
              800  BINARY_SUBSCR    
              802  LOAD_CONST               b'MPF\x00'
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   852  'to 852'

 L. 146       810  LOAD_FAST                's'
              812  LOAD_CONST               4
              814  LOAD_CONST               None
              816  BUILD_SLICE_2         2 
              818  BINARY_SUBSCR    
              820  LOAD_FAST                'self'
              822  LOAD_ATTR                info
              824  LOAD_STR                 'mp'
              826  STORE_SUBSCR     

 L. 149       828  LOAD_FAST                'self'
              830  LOAD_ATTR                fp
              832  LOAD_METHOD              tell
              834  CALL_METHOD_0         0  ''
              836  LOAD_FAST                'n'
              838  BINARY_SUBTRACT  
              840  LOAD_CONST               4
              842  BINARY_ADD       
              844  LOAD_FAST                'self'
              846  LOAD_ATTR                info
              848  LOAD_STR                 'mpoffset'
              850  STORE_SUBSCR     
            852_0  COME_FROM           806  '806'
            852_1  COME_FROM           788  '788'
            852_2  COME_FROM           780  '780'
            852_3  COME_FROM           684  '684'
            852_4  COME_FROM           436  '436'
            852_5  COME_FROM           368  '368'
            852_6  COME_FROM           324  '324'
            852_7  COME_FROM           282  '282'
            852_8  COME_FROM           268  '268'
            852_9  COME_FROM           228  '228'

 L. 152       852  LOAD_STR                 'dpi'
              854  LOAD_FAST                'self'
              856  LOAD_ATTR                info
              858  COMPARE_OP               not-in
          860_862  POP_JUMP_IF_FALSE  1046  'to 1046'
              864  LOAD_STR                 'exif'
              866  LOAD_FAST                'self'
              868  LOAD_ATTR                info
              870  COMPARE_OP               in
          872_874  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 153       876  SETUP_FINALLY      1006  'to 1006'

 L. 154       878  LOAD_FAST                'self'
              880  LOAD_METHOD              getexif
              882  CALL_METHOD_0         0  ''
              884  STORE_FAST               'exif'

 L. 155       886  LOAD_FAST                'exif'
              888  LOAD_CONST               296
              890  BINARY_SUBSCR    
              892  STORE_FAST               'resolution_unit'

 L. 156       894  LOAD_FAST                'exif'
              896  LOAD_CONST               282
              898  BINARY_SUBSCR    
              900  STORE_FAST               'x_resolution'

 L. 157       902  SETUP_FINALLY       928  'to 928'

 L. 158       904  LOAD_GLOBAL              float
              906  LOAD_FAST                'x_resolution'
              908  LOAD_CONST               0
              910  BINARY_SUBSCR    
              912  CALL_FUNCTION_1       1  ''
              914  LOAD_FAST                'x_resolution'
              916  LOAD_CONST               1
              918  BINARY_SUBSCR    
              920  BINARY_TRUE_DIVIDE
              922  STORE_FAST               'dpi'
              924  POP_BLOCK        
              926  JUMP_FORWARD        954  'to 954'
            928_0  COME_FROM_FINALLY   902  '902'

 L. 159       928  DUP_TOP          
              930  LOAD_GLOBAL              TypeError
              932  COMPARE_OP               exception-match
          934_936  POP_JUMP_IF_FALSE   952  'to 952'
              938  POP_TOP          
              940  POP_TOP          
              942  POP_TOP          

 L. 160       944  LOAD_FAST                'x_resolution'
              946  STORE_FAST               'dpi'
              948  POP_EXCEPT       
              950  JUMP_FORWARD        954  'to 954'
            952_0  COME_FROM           934  '934'
              952  END_FINALLY      
            954_0  COME_FROM           950  '950'
            954_1  COME_FROM           926  '926'

 L. 161       954  LOAD_FAST                'resolution_unit'
              956  LOAD_CONST               3
              958  COMPARE_OP               ==
          960_962  POP_JUMP_IF_FALSE   972  'to 972'

 L. 163       964  LOAD_FAST                'dpi'
              966  LOAD_CONST               2.54
              968  INPLACE_MULTIPLY 
              970  STORE_FAST               'dpi'
            972_0  COME_FROM           960  '960'

 L. 164       972  LOAD_GLOBAL              int
              974  LOAD_FAST                'dpi'
              976  LOAD_CONST               0.5
              978  BINARY_ADD       
              980  CALL_FUNCTION_1       1  ''
              982  LOAD_GLOBAL              int
              984  LOAD_FAST                'dpi'
              986  LOAD_CONST               0.5
              988  BINARY_ADD       
              990  CALL_FUNCTION_1       1  ''
              992  BUILD_TUPLE_2         2 
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                info
              998  LOAD_STR                 'dpi'
             1000  STORE_SUBSCR     
             1002  POP_BLOCK        
             1004  JUMP_FORWARD       1046  'to 1046'
           1006_0  COME_FROM_FINALLY   876  '876'

 L. 165      1006  DUP_TOP          
             1008  LOAD_GLOBAL              KeyError
             1010  LOAD_GLOBAL              SyntaxError
             1012  LOAD_GLOBAL              ValueError
             1014  LOAD_GLOBAL              ZeroDivisionError
             1016  BUILD_TUPLE_4         4 
             1018  COMPARE_OP               exception-match
         1020_1022  POP_JUMP_IF_FALSE  1044  'to 1044'
             1024  POP_TOP          
             1026  POP_TOP          
             1028  POP_TOP          

 L. 170      1030  LOAD_CONST               (72, 72)
             1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                info
             1036  LOAD_STR                 'dpi'
             1038  STORE_SUBSCR     
             1040  POP_EXCEPT       
             1042  JUMP_FORWARD       1046  'to 1046'
           1044_0  COME_FROM          1020  '1020'
             1044  END_FINALLY      
           1046_0  COME_FROM          1042  '1042'
           1046_1  COME_FROM          1004  '1004'
           1046_2  COME_FROM           872  '872'
           1046_3  COME_FROM           860  '860'

Parse error at or near `POP_EXCEPT' instruction at offset 674


def COM(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self.info['comment'] = s
    self.app['COM'] = s
    self.applist.append(('COM', s))


def SOF(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self._size = (i16(s[3:]), i16(s[1:]))
    self.bits = i8(s[0])
    if self.bits != 8:
        raise SyntaxError('cannot handle %d-bit layers' % self.bits)
    else:
        self.layers = i8(s[5])
        if self.layers == 1:
            self.mode = 'L'
        else:
            if self.layers == 3:
                self.mode = 'RGB'
            else:
                if self.layers == 4:
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
        self.icclist = []
    for i in range(6, len(s), 3):
        t = s[i:i + 3]
        self.layer.append((t[0], i8(t[1]) // 16, i8(t[1]) & 15, i8(t[2])))


def DQT(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    while len(s):
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
    return prefix[0:3] == b'\xff\xd8\xff'


class JpegImageFile(ImageFile.ImageFile):
    format = 'JPEG'
    format_description = 'JPEG (ISO 10918)'

    def _open--- This code section failed: ---

 L. 341         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               3
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L. 343        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 344        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a JPEG file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 345        28  LOAD_CONST               b'\xff'
               30  STORE_FAST               's'

 L. 348        32  LOAD_CONST               0
               34  DUP_TOP          
               36  LOAD_FAST                'self'
               38  STORE_ATTR               bits
               40  LOAD_FAST                'self'
               42  STORE_ATTR               layers

 L. 351        44  BUILD_LIST_0          0 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               layer

 L. 352        50  BUILD_MAP_0           0 
               52  LOAD_FAST                'self'
               54  STORE_ATTR               huffman_dc

 L. 353        56  BUILD_MAP_0           0 
               58  LOAD_FAST                'self'
               60  STORE_ATTR               huffman_ac

 L. 354        62  BUILD_MAP_0           0 
               64  LOAD_FAST                'self'
               66  STORE_ATTR               quantization

 L. 355        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               app

 L. 356        74  BUILD_LIST_0          0 
               76  LOAD_FAST                'self'
               78  STORE_ATTR               applist

 L. 357        80  BUILD_LIST_0          0 
               82  LOAD_FAST                'self'
               84  STORE_ATTR               icclist

 L. 361        86  LOAD_GLOBAL              i8
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'i'

 L. 362        94  LOAD_FAST                'i'
               96  LOAD_CONST               255
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   128  'to 128'

 L. 363       102  LOAD_FAST                's'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                fp
              108  LOAD_METHOD              read
              110  LOAD_CONST               1
              112  CALL_METHOD_1         1  ''
              114  BINARY_ADD       
              116  STORE_FAST               's'

 L. 364       118  LOAD_GLOBAL              i16
              120  LOAD_FAST                's'
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'i'
              126  JUMP_FORWARD        142  'to 142'
            128_0  COME_FROM           100  '100'

 L. 367       128  LOAD_FAST                'self'
              130  LOAD_ATTR                fp
              132  LOAD_METHOD              read
              134  LOAD_CONST               1
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               's'

 L. 368       140  JUMP_BACK            86  'to 86'
            142_0  COME_FROM           126  '126'

 L. 370       142  LOAD_FAST                'i'
              144  LOAD_GLOBAL              MARKER
              146  COMPARE_OP               in
              148  POP_JUMP_IF_FALSE   254  'to 254'

 L. 371       150  LOAD_GLOBAL              MARKER
              152  LOAD_FAST                'i'
              154  BINARY_SUBSCR    
              156  UNPACK_SEQUENCE_3     3 
              158  STORE_FAST               'name'
              160  STORE_FAST               'description'
              162  STORE_FAST               'handler'

 L. 372       164  LOAD_FAST                'handler'
              166  LOAD_CONST               None
              168  COMPARE_OP               is-not
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L. 373       172  LOAD_FAST                'handler'
              174  LOAD_FAST                'self'
              176  LOAD_FAST                'i'
              178  CALL_FUNCTION_2       2  ''
              180  POP_TOP          
            182_0  COME_FROM           170  '170'

 L. 374       182  LOAD_FAST                'i'
              184  LOAD_CONST               65498
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   240  'to 240'

 L. 375       190  LOAD_FAST                'self'
              192  LOAD_ATTR                mode
              194  STORE_FAST               'rawmode'

 L. 376       196  LOAD_FAST                'self'
              198  LOAD_ATTR                mode
              200  LOAD_STR                 'CMYK'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   210  'to 210'

 L. 377       206  LOAD_STR                 'CMYK;I'
              208  STORE_FAST               'rawmode'
            210_0  COME_FROM           204  '204'

 L. 378       210  LOAD_STR                 'jpeg'
              212  LOAD_CONST               (0, 0)
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                size
              218  BINARY_ADD       
              220  LOAD_CONST               0
              222  LOAD_FAST                'rawmode'
              224  LOAD_STR                 ''
              226  BUILD_TUPLE_2         2 
              228  BUILD_TUPLE_4         4 
              230  BUILD_LIST_1          1 
              232  LOAD_FAST                'self'
              234  STORE_ATTR               tile

 L. 380   236_238  BREAK_LOOP          314  'to 314'
            240_0  COME_FROM           188  '188'

 L. 381       240  LOAD_FAST                'self'
              242  LOAD_ATTR                fp
              244  LOAD_METHOD              read
              246  LOAD_CONST               1
              248  CALL_METHOD_1         1  ''
              250  STORE_FAST               's'
              252  JUMP_BACK            86  'to 86'
            254_0  COME_FROM           148  '148'

 L. 382       254  LOAD_FAST                'i'
              256  LOAD_CONST               0
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_TRUE    274  'to 274'
              264  LOAD_FAST                'i'
              266  LOAD_CONST               65535
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   280  'to 280'
            274_0  COME_FROM           260  '260'

 L. 384       274  LOAD_CONST               b'\xff'
              276  STORE_FAST               's'
              278  JUMP_BACK            86  'to 86'
            280_0  COME_FROM           270  '270'

 L. 385       280  LOAD_FAST                'i'
              282  LOAD_CONST               65280
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   304  'to 304'

 L. 386       290  LOAD_FAST                'self'
              292  LOAD_ATTR                fp
              294  LOAD_METHOD              read
              296  LOAD_CONST               1
              298  CALL_METHOD_1         1  ''
              300  STORE_FAST               's'
              302  JUMP_BACK            86  'to 86'
            304_0  COME_FROM           286  '286'

 L. 388       304  LOAD_GLOBAL              SyntaxError
              306  LOAD_STR                 'no marker found'
              308  CALL_FUNCTION_1       1  ''
              310  RAISE_VARARGS_1       1  'exception instance'
              312  JUMP_BACK            86  'to 86'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 310

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
        else:
            if self.decoderconfig:
                return
            d, e, o, a = self.tile[0]
            scale = 1
            original_size = self.size
            if a[0] == 'RGB' and mode in ('L', 'YCbCr'):
                self.mode = mode
                a = (mode, '')
        if size:
            scale = min(self.size[0] // size[0])(self.size[1] // size[1])
            for s in (8, 4, 2, 1):
                if scale >= s:
                    break
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
         0, 0, original_size[0] / scale, original_size[1] / scale)
        return (self.mode, box)

    def load_djpeg(self):
        f, path = tempfile.mkstemp
        os.close(f)
        if os.path.exists(self.filename):
            subprocess.check_call(['djpeg', '-outfile', path, self.filename])
        else:
            raise ValueError('Invalid Filename')
        try:
            with Image.open(path) as (_im):
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
        except Exception as e:
            try:
                raise SyntaxError('malformed MP Index (unreadable directory)') from e
            finally:
                e = None
                del e

        try:
            quant = mp[45057]
        except KeyError as e:
            try:
                raise SyntaxError('malformed MP Index (no number of images)') from e
            finally:
                e = None
                del e

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

            except KeyError as e:
                try:
                    raise SyntaxError('malformed MP Index (bad MP Entry)') from e
                finally:
                    e = None
                    del e

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
    except KeyError as e:
        try:
            raise OSError('cannot write mode %s as JPEG' % im.mode) from e
        finally:
            e = None
            del e

    else:
        info = im.encoderinfo
        dpi = [round(x) for x in info.get('dpi', (0, 0))]
        quality = info.get('quality', -1)
        subsampling = info.get('subsampling', -1)
        qtables = info.get('qtables')
        if quality == 'keep':
            quality = -1
            subsampling = 'keep'
            qtables = 'keep'
        else:
            if quality in presets:
                preset = presets[quality]
                quality = -1
                subsampling = preset.get('subsampling', -1)
                qtables = preset.get('quantization')
            else:
                if not isinstancequalityint:
                    raise ValueError('Invalid quality setting')
                else:
                    if subsampling in presets:
                        subsampling = presets[subsampling].get('subsampling', -1)
        if isinstanceqtablesstr:
            if qtables in presets:
                qtables = presets[qtables].get('quantization')
            if subsampling == '4:4:4':
                subsampling = 0
            else:
                if subsampling == '4:2:2':
                    subsampling = 1
                else:
                    if subsampling == '4:2:0':
                        subsampling = 2
                    else:
                        if subsampling == '4:1:1':
                            subsampling = 2
                        else:
                            if subsampling == 'keep':
                                if im.format != 'JPEG':
                                    raise ValueError("Cannot use 'keep' when original image is not a JPEG")
                                subsampling = get_sampling(im)

                            def validate_qtables(qtables):
                                if qtables is None:
                                    return qtables
                                else:
                                    if isinstanceqtablesstr:
                                        try:
                                            lines = [int(num) for line in qtables.splitlines for num in line.split('#', 1)[0].split]
                                        except ValueError as e:
                                            try:
                                                raise ValueError('Invalid quantization table') from e
                                            finally:
                                                e = None
                                                del e

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
                                        except TypeError as e:
                                            try:
                                                raise ValueError('Invalid quantization table') from e
                                            finally:
                                                e = None
                                                del e

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
                if icc_profile:
                    markers.append(icc_profile[:MAX_DATA_BYTES_IN_MARKER])
                    icc_profile = icc_profile[MAX_DATA_BYTES_IN_MARKER:]
        else:
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
                else:
                    im.encoderconfig = (quality,
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
                            if quality >= 95 or quality == -1:
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