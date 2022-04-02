# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\JpegImagePlugin.py
import array, io, os, struct, subprocess, sys, tempfile, warnings, xml.etree.ElementTree
from . import Image, ImageFile, TiffImagePlugin
from ._binary import i16be as i16
from ._binary import i32be as i32
from ._binary import o8
from .JpegPresets import presets

def Skip(self, marker):
    n = i16(self.fp.read(2)) - 2
    ImageFile._safe_read(self.fp, n)


def APP--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              i16
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                fp
                6  LOAD_METHOD              read
                8  LOAD_CONST               2
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_CONST               2
               16  BINARY_SUBTRACT  
               18  STORE_FAST               'n'

 L.  65        20  LOAD_GLOBAL              ImageFile
               22  LOAD_METHOD              _safe_read
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                fp
               28  LOAD_FAST                'n'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               's'

 L.  67        34  LOAD_STR                 'APP%d'
               36  LOAD_FAST                'marker'
               38  LOAD_CONST               15
               40  BINARY_AND       
               42  BINARY_MODULO    
               44  STORE_FAST               'app'

 L.  69        46  LOAD_FAST                's'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                app
               52  LOAD_FAST                'app'
               54  STORE_SUBSCR     

 L.  70        56  LOAD_FAST                'self'
               58  LOAD_ATTR                applist
               60  LOAD_METHOD              append
               62  LOAD_FAST                'app'
               64  LOAD_FAST                's'
               66  BUILD_TUPLE_2         2 
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  72        72  LOAD_FAST                'marker'
               74  LOAD_CONST               65504
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   228  'to 228'
               80  LOAD_FAST                's'
               82  LOAD_CONST               None
               84  LOAD_CONST               4
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  LOAD_CONST               b'JFIF'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   228  'to 228'

 L.  74        96  LOAD_GLOBAL              i16
               98  LOAD_FAST                's'
              100  LOAD_CONST               5
              102  CALL_FUNCTION_2       2  ''
              104  DUP_TOP          
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                info
              110  LOAD_STR                 'jfif'
              112  STORE_SUBSCR     
              114  STORE_FAST               'version'

 L.  75       116  LOAD_GLOBAL              divmod
              118  LOAD_FAST                'version'
              120  LOAD_CONST               256
              122  CALL_FUNCTION_2       2  ''
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                info
              128  LOAD_STR                 'jfif_version'
              130  STORE_SUBSCR     

 L.  77       132  SETUP_FINALLY       166  'to 166'

 L.  78       134  LOAD_FAST                's'
              136  LOAD_CONST               7
              138  BINARY_SUBSCR    
              140  STORE_FAST               'jfif_unit'

 L.  79       142  LOAD_GLOBAL              i16
              144  LOAD_FAST                's'
              146  LOAD_CONST               8
              148  CALL_FUNCTION_2       2  ''
              150  LOAD_GLOBAL              i16
              152  LOAD_FAST                's'
              154  LOAD_CONST               10
              156  CALL_FUNCTION_2       2  ''
              158  BUILD_TUPLE_2         2 
              160  STORE_FAST               'jfif_density'
              162  POP_BLOCK        
              164  JUMP_FORWARD        186  'to 186'
            166_0  COME_FROM_FINALLY   132  '132'

 L.  80       166  DUP_TOP          
              168  LOAD_GLOBAL              Exception
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   184  'to 184'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L.  81       180  POP_EXCEPT       
              182  JUMP_FORWARD        816  'to 816'
            184_0  COME_FROM           172  '172'
              184  END_FINALLY      
            186_0  COME_FROM           164  '164'

 L.  83       186  LOAD_FAST                'jfif_unit'
              188  LOAD_CONST               1
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L.  84       194  LOAD_FAST                'jfif_density'
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                info
              200  LOAD_STR                 'dpi'
              202  STORE_SUBSCR     
            204_0  COME_FROM           192  '192'

 L.  85       204  LOAD_FAST                'jfif_unit'
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                info
              210  LOAD_STR                 'jfif_unit'
              212  STORE_SUBSCR     

 L.  86       214  LOAD_FAST                'jfif_density'
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                info
              220  LOAD_STR                 'jfif_density'
              222  STORE_SUBSCR     
          224_226  JUMP_FORWARD        816  'to 816'
            228_0  COME_FROM            94  '94'
            228_1  COME_FROM            78  '78'

 L.  87       228  LOAD_FAST                'marker'
              230  LOAD_CONST               65505
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   282  'to 282'
              238  LOAD_FAST                's'
              240  LOAD_CONST               None
              242  LOAD_CONST               5
              244  BUILD_SLICE_2         2 
              246  BINARY_SUBSCR    
              248  LOAD_CONST               b'Exif\x00'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   282  'to 282'

 L.  88       256  LOAD_STR                 'exif'
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                info
              262  COMPARE_OP               not-in
          264_266  POP_JUMP_IF_FALSE   816  'to 816'

 L.  90       268  LOAD_FAST                's'
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                info
              274  LOAD_STR                 'exif'
              276  STORE_SUBSCR     
          278_280  JUMP_FORWARD        816  'to 816'
            282_0  COME_FROM           252  '252'
            282_1  COME_FROM           234  '234'

 L.  91       282  LOAD_FAST                'marker'
              284  LOAD_CONST               65506
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   324  'to 324'
              292  LOAD_FAST                's'
              294  LOAD_CONST               None
              296  LOAD_CONST               5
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  LOAD_CONST               b'FPXR\x00'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   324  'to 324'

 L.  93       310  LOAD_FAST                's'
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                info
              316  LOAD_STR                 'flashpix'
              318  STORE_SUBSCR     
          320_322  JUMP_FORWARD        816  'to 816'
            324_0  COME_FROM           306  '306'
            324_1  COME_FROM           288  '288'

 L.  94       324  LOAD_FAST                'marker'
              326  LOAD_CONST               65506
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   368  'to 368'
              334  LOAD_FAST                's'
              336  LOAD_CONST               None
              338  LOAD_CONST               12
              340  BUILD_SLICE_2         2 
              342  BINARY_SUBSCR    
              344  LOAD_CONST               b'ICC_PROFILE\x00'
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   368  'to 368'

 L. 106       352  LOAD_FAST                'self'
              354  LOAD_ATTR                icclist
              356  LOAD_METHOD              append
              358  LOAD_FAST                's'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
          364_366  JUMP_FORWARD        816  'to 816'
            368_0  COME_FROM           348  '348'
            368_1  COME_FROM           330  '330'

 L. 107       368  LOAD_FAST                'marker'
              370  LOAD_CONST               65517
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   654  'to 654'
              378  LOAD_FAST                's'
              380  LOAD_CONST               None
              382  LOAD_CONST               14
              384  BUILD_SLICE_2         2 
              386  BINARY_SUBSCR    
              388  LOAD_CONST               b'Photoshop 3.0\x00'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   654  'to 654'

 L. 109       396  LOAD_CONST               14
              398  STORE_FAST               'offset'

 L. 110       400  LOAD_FAST                'self'
              402  LOAD_ATTR                info
              404  LOAD_METHOD              setdefault
              406  LOAD_STR                 'photoshop'
              408  BUILD_MAP_0           0 
              410  CALL_METHOD_2         2  ''
              412  STORE_FAST               'photoshop'

 L. 111       414  LOAD_FAST                's'
              416  LOAD_FAST                'offset'
              418  LOAD_FAST                'offset'
              420  LOAD_CONST               4
              422  BINARY_ADD       
              424  BUILD_SLICE_2         2 
              426  BINARY_SUBSCR    
              428  LOAD_CONST               b'8BIM'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   816  'to 816'

 L. 112       436  SETUP_FINALLY       618  'to 618'

 L. 113       438  LOAD_FAST                'offset'
              440  LOAD_CONST               4
              442  INPLACE_ADD      
              444  STORE_FAST               'offset'

 L. 115       446  LOAD_GLOBAL              i16
              448  LOAD_FAST                's'
              450  LOAD_FAST                'offset'
              452  CALL_FUNCTION_2       2  ''
              454  STORE_FAST               'code'

 L. 116       456  LOAD_FAST                'offset'
              458  LOAD_CONST               2
              460  INPLACE_ADD      
              462  STORE_FAST               'offset'

 L. 118       464  LOAD_FAST                's'
              466  LOAD_FAST                'offset'
              468  BINARY_SUBSCR    
              470  STORE_FAST               'name_len'

 L. 120       472  LOAD_FAST                'offset'
              474  LOAD_CONST               1
              476  LOAD_FAST                'name_len'
              478  BINARY_ADD       
              480  INPLACE_ADD      
              482  STORE_FAST               'offset'

 L. 121       484  LOAD_FAST                'offset'
              486  LOAD_FAST                'offset'
              488  LOAD_CONST               1
              490  BINARY_AND       
              492  INPLACE_ADD      
              494  STORE_FAST               'offset'

 L. 123       496  LOAD_GLOBAL              i32
              498  LOAD_FAST                's'
              500  LOAD_FAST                'offset'
              502  CALL_FUNCTION_2       2  ''
              504  STORE_FAST               'size'

 L. 124       506  LOAD_FAST                'offset'
              508  LOAD_CONST               4
              510  INPLACE_ADD      
              512  STORE_FAST               'offset'

 L. 125       514  LOAD_FAST                's'
              516  LOAD_FAST                'offset'
              518  LOAD_FAST                'offset'
              520  LOAD_FAST                'size'
              522  BINARY_ADD       
              524  BUILD_SLICE_2         2 
              526  BINARY_SUBSCR    
              528  STORE_FAST               'data'

 L. 126       530  LOAD_FAST                'code'
              532  LOAD_CONST               1005
              534  COMPARE_OP               ==
          536_538  POP_JUMP_IF_FALSE   586  'to 586'

 L. 128       540  LOAD_GLOBAL              i32
              542  LOAD_FAST                'data'
              544  LOAD_CONST               0
              546  CALL_FUNCTION_2       2  ''
              548  LOAD_CONST               65536
              550  BINARY_TRUE_DIVIDE

 L. 129       552  LOAD_GLOBAL              i16
              554  LOAD_FAST                'data'
              556  LOAD_CONST               4
              558  CALL_FUNCTION_2       2  ''

 L. 130       560  LOAD_GLOBAL              i32
              562  LOAD_FAST                'data'
              564  LOAD_CONST               8
              566  CALL_FUNCTION_2       2  ''
              568  LOAD_CONST               65536
              570  BINARY_TRUE_DIVIDE

 L. 131       572  LOAD_GLOBAL              i16
              574  LOAD_FAST                'data'
              576  LOAD_CONST               12
              578  CALL_FUNCTION_2       2  ''

 L. 127       580  LOAD_CONST               ('XResolution', 'DisplayedUnitsX', 'YResolution', 'DisplayedUnitsY')
              582  BUILD_CONST_KEY_MAP_4     4 
              584  STORE_FAST               'data'
            586_0  COME_FROM           536  '536'

 L. 133       586  LOAD_FAST                'data'
              588  LOAD_FAST                'photoshop'
              590  LOAD_FAST                'code'
              592  STORE_SUBSCR     

 L. 134       594  LOAD_FAST                'offset'
              596  LOAD_FAST                'size'
              598  INPLACE_ADD      
              600  STORE_FAST               'offset'

 L. 135       602  LOAD_FAST                'offset'
              604  LOAD_FAST                'offset'
              606  LOAD_CONST               1
              608  BINARY_AND       
              610  INPLACE_ADD      
              612  STORE_FAST               'offset'
              614  POP_BLOCK        
              616  JUMP_BACK           414  'to 414'
            618_0  COME_FROM_FINALLY   436  '436'

 L. 136       618  DUP_TOP          
              620  LOAD_GLOBAL              struct
              622  LOAD_ATTR                error
              624  COMPARE_OP               exception-match
          626_628  POP_JUMP_IF_FALSE   646  'to 646'
              630  POP_TOP          
              632  POP_TOP          
              634  POP_TOP          

 L. 137       636  POP_EXCEPT       
          638_640  JUMP_ABSOLUTE       816  'to 816'
              642  POP_EXCEPT       
              644  JUMP_BACK           414  'to 414'
            646_0  COME_FROM           626  '626'
              646  END_FINALLY      
          648_650  JUMP_BACK           414  'to 414'
              652  JUMP_FORWARD        816  'to 816'
            654_0  COME_FROM           392  '392'
            654_1  COME_FROM           374  '374'

 L. 139       654  LOAD_FAST                'marker'
              656  LOAD_CONST               65518
              658  COMPARE_OP               ==
          660_662  POP_JUMP_IF_FALSE   746  'to 746'
              664  LOAD_FAST                's'
              666  LOAD_CONST               None
              668  LOAD_CONST               5
              670  BUILD_SLICE_2         2 
              672  BINARY_SUBSCR    
              674  LOAD_CONST               b'Adobe'
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   746  'to 746'

 L. 140       682  LOAD_GLOBAL              i16
              684  LOAD_FAST                's'
              686  LOAD_CONST               5
              688  CALL_FUNCTION_2       2  ''
              690  LOAD_FAST                'self'
              692  LOAD_ATTR                info
              694  LOAD_STR                 'adobe'
              696  STORE_SUBSCR     

 L. 142       698  SETUP_FINALLY       712  'to 712'

 L. 143       700  LOAD_FAST                's'
              702  LOAD_CONST               1
              704  BINARY_SUBSCR    
              706  STORE_FAST               'adobe_transform'
              708  POP_BLOCK        
              710  JUMP_FORWARD        734  'to 734'
            712_0  COME_FROM_FINALLY   698  '698'

 L. 144       712  DUP_TOP          
              714  LOAD_GLOBAL              Exception
              716  COMPARE_OP               exception-match
          718_720  POP_JUMP_IF_FALSE   732  'to 732'
              722  POP_TOP          
              724  POP_TOP          
              726  POP_TOP          

 L. 145       728  POP_EXCEPT       
              730  JUMP_FORWARD        744  'to 744'
            732_0  COME_FROM           718  '718'
              732  END_FINALLY      
            734_0  COME_FROM           710  '710'

 L. 147       734  LOAD_FAST                'adobe_transform'
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                info
              740  LOAD_STR                 'adobe_transform'
              742  STORE_SUBSCR     
            744_0  COME_FROM           730  '730'
              744  JUMP_FORWARD        816  'to 816'
            746_0  COME_FROM           678  '678'
            746_1  COME_FROM           660  '660'

 L. 148       746  LOAD_FAST                'marker'
              748  LOAD_CONST               65506
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE   816  'to 816'
              756  LOAD_FAST                's'
              758  LOAD_CONST               None
              760  LOAD_CONST               4
              762  BUILD_SLICE_2         2 
              764  BINARY_SUBSCR    
              766  LOAD_CONST               b'MPF\x00'
              768  COMPARE_OP               ==
          770_772  POP_JUMP_IF_FALSE   816  'to 816'

 L. 150       774  LOAD_FAST                's'
              776  LOAD_CONST               4
              778  LOAD_CONST               None
              780  BUILD_SLICE_2         2 
              782  BINARY_SUBSCR    
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                info
              788  LOAD_STR                 'mp'
              790  STORE_SUBSCR     

 L. 153       792  LOAD_FAST                'self'
              794  LOAD_ATTR                fp
              796  LOAD_METHOD              tell
              798  CALL_METHOD_0         0  ''
              800  LOAD_FAST                'n'
              802  BINARY_SUBTRACT  
              804  LOAD_CONST               4
              806  BINARY_ADD       
              808  LOAD_FAST                'self'
              810  LOAD_ATTR                info
              812  LOAD_STR                 'mpoffset'
              814  STORE_SUBSCR     
            816_0  COME_FROM           770  '770'
            816_1  COME_FROM           752  '752'
            816_2  COME_FROM           744  '744'
            816_3  COME_FROM           652  '652'
            816_4  COME_FROM           432  '432'
            816_5  COME_FROM           364  '364'
            816_6  COME_FROM           320  '320'
            816_7  COME_FROM           278  '278'
            816_8  COME_FROM           264  '264'
            816_9  COME_FROM           224  '224'

 L. 156       816  LOAD_STR                 'dpi'
              818  LOAD_FAST                'self'
              820  LOAD_ATTR                info
              822  COMPARE_OP               not-in
          824_826  POP_JUMP_IF_FALSE  1010  'to 1010'
              828  LOAD_STR                 'exif'
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                info
              834  COMPARE_OP               in
          836_838  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 157       840  SETUP_FINALLY       970  'to 970'

 L. 158       842  LOAD_FAST                'self'
              844  LOAD_METHOD              getexif
              846  CALL_METHOD_0         0  ''
              848  STORE_FAST               'exif'

 L. 159       850  LOAD_FAST                'exif'
              852  LOAD_CONST               296
              854  BINARY_SUBSCR    
              856  STORE_FAST               'resolution_unit'

 L. 160       858  LOAD_FAST                'exif'
              860  LOAD_CONST               282
              862  BINARY_SUBSCR    
              864  STORE_FAST               'x_resolution'

 L. 161       866  SETUP_FINALLY       892  'to 892'

 L. 162       868  LOAD_GLOBAL              float
              870  LOAD_FAST                'x_resolution'
              872  LOAD_CONST               0
              874  BINARY_SUBSCR    
              876  CALL_FUNCTION_1       1  ''
              878  LOAD_FAST                'x_resolution'
              880  LOAD_CONST               1
              882  BINARY_SUBSCR    
              884  BINARY_TRUE_DIVIDE
              886  STORE_FAST               'dpi'
              888  POP_BLOCK        
              890  JUMP_FORWARD        918  'to 918'
            892_0  COME_FROM_FINALLY   866  '866'

 L. 163       892  DUP_TOP          
              894  LOAD_GLOBAL              TypeError
              896  COMPARE_OP               exception-match
          898_900  POP_JUMP_IF_FALSE   916  'to 916'
              902  POP_TOP          
              904  POP_TOP          
              906  POP_TOP          

 L. 164       908  LOAD_FAST                'x_resolution'
              910  STORE_FAST               'dpi'
              912  POP_EXCEPT       
              914  JUMP_FORWARD        918  'to 918'
            916_0  COME_FROM           898  '898'
              916  END_FINALLY      
            918_0  COME_FROM           914  '914'
            918_1  COME_FROM           890  '890'

 L. 165       918  LOAD_FAST                'resolution_unit'
              920  LOAD_CONST               3
              922  COMPARE_OP               ==
          924_926  POP_JUMP_IF_FALSE   936  'to 936'

 L. 167       928  LOAD_FAST                'dpi'
              930  LOAD_CONST               2.54
              932  INPLACE_MULTIPLY 
              934  STORE_FAST               'dpi'
            936_0  COME_FROM           924  '924'

 L. 168       936  LOAD_GLOBAL              int
              938  LOAD_FAST                'dpi'
              940  LOAD_CONST               0.5
              942  BINARY_ADD       
              944  CALL_FUNCTION_1       1  ''
              946  LOAD_GLOBAL              int
              948  LOAD_FAST                'dpi'
              950  LOAD_CONST               0.5
              952  BINARY_ADD       
              954  CALL_FUNCTION_1       1  ''
              956  BUILD_TUPLE_2         2 
              958  LOAD_FAST                'self'
              960  LOAD_ATTR                info
              962  LOAD_STR                 'dpi'
              964  STORE_SUBSCR     
              966  POP_BLOCK        
              968  JUMP_FORWARD       1010  'to 1010'
            970_0  COME_FROM_FINALLY   840  '840'

 L. 169       970  DUP_TOP          
              972  LOAD_GLOBAL              KeyError
              974  LOAD_GLOBAL              SyntaxError
              976  LOAD_GLOBAL              ValueError
              978  LOAD_GLOBAL              ZeroDivisionError
              980  BUILD_TUPLE_4         4 
              982  COMPARE_OP               exception-match
          984_986  POP_JUMP_IF_FALSE  1008  'to 1008'
              988  POP_TOP          
              990  POP_TOP          
              992  POP_TOP          

 L. 174       994  LOAD_CONST               (72, 72)
              996  LOAD_FAST                'self'
              998  LOAD_ATTR                info
             1000  LOAD_STR                 'dpi'
             1002  STORE_SUBSCR     
             1004  POP_EXCEPT       
             1006  JUMP_FORWARD       1010  'to 1010'
           1008_0  COME_FROM           984  '984'
             1008  END_FINALLY      
           1010_0  COME_FROM          1006  '1006'
           1010_1  COME_FROM           968  '968'
           1010_2  COME_FROM           836  '836'
           1010_3  COME_FROM           824  '824'

Parse error at or near `POP_EXCEPT' instruction at offset 642


def COM(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self.info['comment'] = s
    self.app['COM'] = s
    self.applist.append(('COM', s))


def SOF(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self._size = (i16s3, i16s1)
    self.bits = s[0]
    if self.bits != 8:
        raise SyntaxError(f"cannot handle {self.bits}-bit layers")
    else:
        self.layers = s[5]
        if self.layers == 1:
            self.mode = 'L'
        else:
            if self.layers == 3:
                self.mode = 'RGB'
            else:
                if self.layers == 4:
                    self.mode = 'CMYK'
                else:
                    raise SyntaxError(f"cannot handle {self.layers}-layer images")
    if marker in (65474, 65478, 65482, 65486):
        self.info['progressive'] = self.info['progression'] = 1
    if self.icclist:
        self.icclist.sort
        if self.icclist[0][13] == len(self.icclist):
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
        self.layer.append((t[0], t[1] // 16, t[1] & 15, t[2]))


def DQT(self, marker):
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    while len(s):
        v = s[0]
        precision = 1 if v // 16 == 0 else 2
        qt_length = 1 + precision * 64
        if len(s) < qt_length:
            raise SyntaxError('bad quantization table marker')
        data = array.array('B' if precision == 1 else 'H', s[1:qt_length])
        if sys.byteorder == 'little':
            if precision > 1:
                data.byteswap
        self.quantization[v & 15] = data
        s = s[qt_length:]


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

 L. 345         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_METHOD              read
                6  LOAD_CONST               3
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               's'

 L. 347        12  LOAD_GLOBAL              _accept
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 348        20  LOAD_GLOBAL              SyntaxError
               22  LOAD_STR                 'not a JPEG file'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 349        28  LOAD_CONST               b'\xff'
               30  STORE_FAST               's'

 L. 352        32  LOAD_CONST               0
               34  DUP_TOP          
               36  LOAD_FAST                'self'
               38  STORE_ATTR               bits
               40  LOAD_FAST                'self'
               42  STORE_ATTR               layers

 L. 355        44  BUILD_LIST_0          0 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               layer

 L. 356        50  BUILD_MAP_0           0 
               52  LOAD_FAST                'self'
               54  STORE_ATTR               huffman_dc

 L. 357        56  BUILD_MAP_0           0 
               58  LOAD_FAST                'self'
               60  STORE_ATTR               huffman_ac

 L. 358        62  BUILD_MAP_0           0 
               64  LOAD_FAST                'self'
               66  STORE_ATTR               quantization

 L. 359        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               app

 L. 360        74  BUILD_LIST_0          0 
               76  LOAD_FAST                'self'
               78  STORE_ATTR               applist

 L. 361        80  BUILD_LIST_0          0 
               82  LOAD_FAST                'self'
               84  STORE_ATTR               icclist

 L. 362        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _xmp

 L. 366        92  LOAD_FAST                's'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  STORE_FAST               'i'

 L. 367       100  LOAD_FAST                'i'
              102  LOAD_CONST               255
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   134  'to 134'

 L. 368       108  LOAD_FAST                's'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                fp
              114  LOAD_METHOD              read
              116  LOAD_CONST               1
              118  CALL_METHOD_1         1  ''
              120  BINARY_ADD       
              122  STORE_FAST               's'

 L. 369       124  LOAD_GLOBAL              i16
              126  LOAD_FAST                's'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'i'
              132  JUMP_FORWARD        148  'to 148'
            134_0  COME_FROM           106  '106'

 L. 372       134  LOAD_FAST                'self'
              136  LOAD_ATTR                fp
              138  LOAD_METHOD              read
              140  LOAD_CONST               1
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               's'

 L. 373       146  JUMP_BACK            92  'to 92'
            148_0  COME_FROM           132  '132'

 L. 375       148  LOAD_FAST                'i'
              150  LOAD_GLOBAL              MARKER
              152  COMPARE_OP               in
          154_156  POP_JUMP_IF_FALSE   262  'to 262'

 L. 376       158  LOAD_GLOBAL              MARKER
              160  LOAD_FAST                'i'
              162  BINARY_SUBSCR    
              164  UNPACK_SEQUENCE_3     3 
              166  STORE_FAST               'name'
              168  STORE_FAST               'description'
              170  STORE_FAST               'handler'

 L. 377       172  LOAD_FAST                'handler'
              174  LOAD_CONST               None
              176  COMPARE_OP               is-not
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L. 378       180  LOAD_FAST                'handler'
              182  LOAD_FAST                'self'
              184  LOAD_FAST                'i'
              186  CALL_FUNCTION_2       2  ''
              188  POP_TOP          
            190_0  COME_FROM           178  '178'

 L. 379       190  LOAD_FAST                'i'
              192  LOAD_CONST               65498
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   248  'to 248'

 L. 380       198  LOAD_FAST                'self'
              200  LOAD_ATTR                mode
              202  STORE_FAST               'rawmode'

 L. 381       204  LOAD_FAST                'self'
              206  LOAD_ATTR                mode
              208  LOAD_STR                 'CMYK'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   218  'to 218'

 L. 382       214  LOAD_STR                 'CMYK;I'
              216  STORE_FAST               'rawmode'
            218_0  COME_FROM           212  '212'

 L. 383       218  LOAD_STR                 'jpeg'
              220  LOAD_CONST               (0, 0)
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                size
              226  BINARY_ADD       
              228  LOAD_CONST               0
              230  LOAD_FAST                'rawmode'
              232  LOAD_STR                 ''
              234  BUILD_TUPLE_2         2 
              236  BUILD_TUPLE_4         4 
              238  BUILD_LIST_1          1 
              240  LOAD_FAST                'self'
              242  STORE_ATTR               tile

 L. 385   244_246  BREAK_LOOP          322  'to 322'
            248_0  COME_FROM           196  '196'

 L. 386       248  LOAD_FAST                'self'
              250  LOAD_ATTR                fp
              252  LOAD_METHOD              read
              254  LOAD_CONST               1
              256  CALL_METHOD_1         1  ''
              258  STORE_FAST               's'
              260  JUMP_BACK            92  'to 92'
            262_0  COME_FROM           154  '154'

 L. 387       262  LOAD_FAST                'i'
              264  LOAD_CONST               0
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_TRUE    282  'to 282'
              272  LOAD_FAST                'i'
              274  LOAD_CONST               65535
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   288  'to 288'
            282_0  COME_FROM           268  '268'

 L. 389       282  LOAD_CONST               b'\xff'
              284  STORE_FAST               's'
              286  JUMP_BACK            92  'to 92'
            288_0  COME_FROM           278  '278'

 L. 390       288  LOAD_FAST                'i'
              290  LOAD_CONST               65280
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   312  'to 312'

 L. 391       298  LOAD_FAST                'self'
              300  LOAD_ATTR                fp
              302  LOAD_METHOD              read
              304  LOAD_CONST               1
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               's'
              310  JUMP_BACK            92  'to 92'
            312_0  COME_FROM           294  '294'

 L. 393       312  LOAD_GLOBAL              SyntaxError
              314  LOAD_STR                 'no marker found'
              316  CALL_FUNCTION_1       1  ''
              318  RAISE_VARARGS_1       1  'exception instance'
              320  JUMP_BACK            92  'to 92'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 318

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

    def getxmp(self):
        """
        Returns a dictionary containing the XMP tags.
        :returns: XMP tags in a dictionary.
        """
        if self._xmp is None:
            self._xmp = {}
        for segment, content in self.applist:
            if segment == 'APP1':
                marker, xmp_tags = content.rsplit(b'\x00', 1)
                if marker == b'http://ns.adobe.com/xap/1.0/':
                    root = xml.etree.ElementTree.fromstring(xmp_tags)
                    for element in root.findall('.//'):
                        self._xmp[element.tag.split('}')[1]] = {value:child.split('}')[1] for child, value in element.attrib.items}

            return self._xmp


def _getexif(self):
    if 'exif' not in self.info:
        return
    return self.getexif._get_merged_dict


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
                    unpackedentry = struct.unpack_from(f"{endianness}LLLHH", rawmpentries, entrynum * 16)
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
            raise OSError(f"cannot write mode {im.mode} as JPEG") from e
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
                                            table = array.array('H', table)
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