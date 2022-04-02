# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\PdfImagePlugin.py
import io, os, time
from . import Image, ImageFile, ImageSequence, PdfParser, __version__

def _save_all(im, fp, filename):
    _save(im, fp, filename, save_all=True)


def _save--- This code section failed: ---

 L.  49         0  LOAD_FAST                'im'
                2  LOAD_ATTR                encoderinfo
                4  LOAD_METHOD              get
                6  LOAD_STR                 'append'
                8  LOAD_CONST               False
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'is_appending'

 L.  50        14  LOAD_FAST                'is_appending'
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  51        18  LOAD_GLOBAL              PdfParser
               20  LOAD_ATTR                PdfParser
               22  LOAD_FAST                'fp'
               24  LOAD_FAST                'filename'
               26  LOAD_STR                 'r+b'
               28  LOAD_CONST               ('f', 'filename', 'mode')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  STORE_FAST               'existing_pdf'
               34  JUMP_FORWARD         52  'to 52'
             36_0  COME_FROM            16  '16'

 L.  53        36  LOAD_GLOBAL              PdfParser
               38  LOAD_ATTR                PdfParser
               40  LOAD_FAST                'fp'
               42  LOAD_FAST                'filename'
               44  LOAD_STR                 'w+b'
               46  LOAD_CONST               ('f', 'filename', 'mode')
               48  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               50  STORE_FAST               'existing_pdf'
             52_0  COME_FROM            34  '34'

 L.  55        52  LOAD_FAST                'im'
               54  LOAD_ATTR                encoderinfo
               56  LOAD_METHOD              get
               58  LOAD_STR                 'resolution'
               60  LOAD_CONST               72.0
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'resolution'

 L.  59        66  LOAD_FAST                'is_appending'

 L.  58        68  POP_JUMP_IF_FALSE    74  'to 74'
               70  LOAD_CONST               None
               72  JUMP_FORWARD         96  'to 96'
             74_0  COME_FROM            68  '68'

 L.  60        74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              splitext
               80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              basename
               86  LOAD_FAST                'filename'
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
             96_0  COME_FROM            72  '72'

 L.  61        96  LOAD_CONST               None

 L.  62        98  LOAD_CONST               None

 L.  63       100  LOAD_CONST               None

 L.  64       102  LOAD_CONST               None

 L.  65       104  LOAD_CONST               None

 L.  66       106  LOAD_FAST                'is_appending'
              108  POP_JUMP_IF_FALSE   114  'to 114'
              110  LOAD_CONST               None
              112  JUMP_FORWARD        120  'to 120'
            114_0  COME_FROM           108  '108'
              114  LOAD_GLOBAL              time
              116  LOAD_METHOD              gmtime
              118  CALL_METHOD_0         0  ''
            120_0  COME_FROM           112  '112'

 L.  67       120  LOAD_FAST                'is_appending'
              122  POP_JUMP_IF_FALSE   128  'to 128'
              124  LOAD_CONST               None
              126  JUMP_FORWARD        134  'to 134'
            128_0  COME_FROM           122  '122'
              128  LOAD_GLOBAL              time
              130  LOAD_METHOD              gmtime
              132  CALL_METHOD_0         0  ''
            134_0  COME_FROM           126  '126'

 L.  57       134  LOAD_CONST               ('title', 'author', 'subject', 'keywords', 'creator', 'producer', 'creationDate', 'modDate')
              136  BUILD_CONST_KEY_MAP_8     8 
              138  STORE_FAST               'info'

 L.  69       140  LOAD_FAST                'info'
              142  LOAD_METHOD              items
              144  CALL_METHOD_0         0  ''
              146  GET_ITER         
            148_0  COME_FROM           216  '216'
            148_1  COME_FROM           184  '184'
              148  FOR_ITER            218  'to 218'
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'k'
              154  STORE_FAST               'default'

 L.  70       156  LOAD_FAST                'k'
              158  LOAD_FAST                'im'
              160  LOAD_ATTR                encoderinfo
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   178  'to 178'
              166  LOAD_FAST                'im'
              168  LOAD_ATTR                encoderinfo
              170  LOAD_METHOD              get
              172  LOAD_FAST                'k'
              174  CALL_METHOD_1         1  ''
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           164  '164'
              178  LOAD_FAST                'default'
            180_0  COME_FROM           176  '176'
              180  STORE_FAST               'v'

 L.  71       182  LOAD_FAST                'v'
              184  POP_JUMP_IF_FALSE_BACK   148  'to 148'

 L.  72       186  LOAD_FAST                'v'
              188  LOAD_FAST                'existing_pdf'
              190  LOAD_ATTR                info
              192  LOAD_FAST                'k'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_METHOD              upper
              200  CALL_METHOD_0         0  ''
              202  LOAD_FAST                'k'
              204  LOAD_CONST               1
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  BINARY_ADD       
              214  STORE_SUBSCR     
              216  JUMP_BACK           148  'to 148'
            218_0  COME_FROM           148  '148'

 L.  76       218  LOAD_FAST                'im'
              220  LOAD_METHOD              load
              222  CALL_METHOD_0         0  ''
              224  POP_TOP          

 L.  78       226  LOAD_FAST                'existing_pdf'
              228  LOAD_METHOD              start_writing
              230  CALL_METHOD_0         0  ''
              232  POP_TOP          

 L.  79       234  LOAD_FAST                'existing_pdf'
              236  LOAD_METHOD              write_header
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          

 L.  80       242  LOAD_FAST                'existing_pdf'
              244  LOAD_METHOD              write_comment
              246  LOAD_STR                 'created by Pillow '
              248  LOAD_GLOBAL              __version__
              250  FORMAT_VALUE          0  ''
              252  LOAD_STR                 ' PDF driver'
              254  BUILD_STRING_3        3 
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L.  84       260  LOAD_FAST                'im'
              262  BUILD_LIST_1          1 
              264  STORE_FAST               'ims'

 L.  85       266  LOAD_FAST                'save_all'
          268_270  POP_JUMP_IF_FALSE   320  'to 320'

 L.  86       272  LOAD_FAST                'im'
              274  LOAD_ATTR                encoderinfo
              276  LOAD_METHOD              get
              278  LOAD_STR                 'append_images'
              280  BUILD_LIST_0          0 
              282  CALL_METHOD_2         2  ''
              284  STORE_FAST               'append_images'

 L.  87       286  LOAD_FAST                'append_images'
              288  GET_ITER         
            290_0  COME_FROM           316  '316'
              290  FOR_ITER            320  'to 320'
              292  STORE_FAST               'append_im'

 L.  88       294  LOAD_FAST                'im'
              296  LOAD_ATTR                encoderinfo
              298  LOAD_METHOD              copy
              300  CALL_METHOD_0         0  ''
              302  LOAD_FAST                'append_im'
              304  STORE_ATTR               encoderinfo

 L.  89       306  LOAD_FAST                'ims'
              308  LOAD_METHOD              append
              310  LOAD_FAST                'append_im'
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          
          316_318  JUMP_BACK           290  'to 290'
            320_0  COME_FROM           290  '290'
            320_1  COME_FROM           268  '268'

 L.  90       320  LOAD_CONST               0
              322  STORE_FAST               'numberOfPages'

 L.  91       324  BUILD_LIST_0          0 
              326  STORE_FAST               'image_refs'

 L.  92       328  BUILD_LIST_0          0 
              330  STORE_FAST               'page_refs'

 L.  93       332  BUILD_LIST_0          0 
              334  STORE_FAST               'contents_refs'

 L.  94       336  LOAD_FAST                'ims'
              338  GET_ITER         
            340_0  COME_FROM           476  '476'
              340  FOR_ITER            480  'to 480'
              342  STORE_FAST               'im'

 L.  95       344  LOAD_CONST               1
              346  STORE_FAST               'im_numberOfPages'

 L.  96       348  LOAD_FAST                'save_all'
          350_352  POP_JUMP_IF_FALSE   388  'to 388'

 L.  97       354  SETUP_FINALLY       366  'to 366'

 L.  98       356  LOAD_FAST                'im'
              358  LOAD_ATTR                n_frames
              360  STORE_FAST               'im_numberOfPages'
              362  POP_BLOCK        
              364  JUMP_FORWARD        388  'to 388'
            366_0  COME_FROM_FINALLY   354  '354'

 L.  99       366  DUP_TOP          
              368  LOAD_GLOBAL              AttributeError
              370  COMPARE_OP               exception-match
          372_374  POP_JUMP_IF_FALSE   386  'to 386'
              376  POP_TOP          
              378  POP_TOP          
              380  POP_TOP          

 L. 102       382  POP_EXCEPT       
              384  BREAK_LOOP          388  'to 388'
            386_0  COME_FROM           372  '372'
              386  END_FINALLY      
            388_0  COME_FROM           384  '384'
            388_1  COME_FROM           364  '364'
            388_2  COME_FROM           350  '350'

 L. 103       388  LOAD_FAST                'numberOfPages'
              390  LOAD_FAST                'im_numberOfPages'
              392  INPLACE_ADD      
              394  STORE_FAST               'numberOfPages'

 L. 104       396  LOAD_GLOBAL              range
              398  LOAD_FAST                'im_numberOfPages'
              400  CALL_FUNCTION_1       1  ''
              402  GET_ITER         
            404_0  COME_FROM           472  '472'
              404  FOR_ITER            476  'to 476'
              406  STORE_FAST               'i'

 L. 105       408  LOAD_FAST                'image_refs'
              410  LOAD_METHOD              append
              412  LOAD_FAST                'existing_pdf'
              414  LOAD_METHOD              next_object_id
              416  LOAD_CONST               0
              418  CALL_METHOD_1         1  ''
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          

 L. 106       424  LOAD_FAST                'page_refs'
              426  LOAD_METHOD              append
              428  LOAD_FAST                'existing_pdf'
              430  LOAD_METHOD              next_object_id
              432  LOAD_CONST               0
              434  CALL_METHOD_1         1  ''
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          

 L. 107       440  LOAD_FAST                'contents_refs'
              442  LOAD_METHOD              append
              444  LOAD_FAST                'existing_pdf'
              446  LOAD_METHOD              next_object_id
              448  LOAD_CONST               0
              450  CALL_METHOD_1         1  ''
              452  CALL_METHOD_1         1  ''
              454  POP_TOP          

 L. 108       456  LOAD_FAST                'existing_pdf'
              458  LOAD_ATTR                pages
              460  LOAD_METHOD              append
              462  LOAD_FAST                'page_refs'
              464  LOAD_CONST               -1
              466  BINARY_SUBSCR    
              468  CALL_METHOD_1         1  ''
              470  POP_TOP          
          472_474  JUMP_BACK           404  'to 404'
            476_0  COME_FROM           404  '404'
          476_478  JUMP_BACK           340  'to 340'
            480_0  COME_FROM           340  '340'

 L. 112       480  LOAD_FAST                'existing_pdf'
              482  LOAD_METHOD              write_catalog
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          

 L. 114       488  LOAD_CONST               0
              490  STORE_FAST               'pageNumber'

 L. 115       492  LOAD_FAST                'ims'
              494  GET_ITER         
            496_0  COME_FROM          1240  '1240'
          496_498  FOR_ITER           1244  'to 1244'
              500  STORE_FAST               'imSequence'

 L. 116       502  LOAD_FAST                'save_all'
          504_506  POP_JUMP_IF_FALSE   518  'to 518'
              508  LOAD_GLOBAL              ImageSequence
              510  LOAD_METHOD              Iterator
              512  LOAD_FAST                'imSequence'
              514  CALL_METHOD_1         1  ''
              516  JUMP_FORWARD        522  'to 522'
            518_0  COME_FROM           504  '504'
              518  LOAD_FAST                'imSequence'
              520  BUILD_LIST_1          1 
            522_0  COME_FROM           516  '516'
              522  STORE_FAST               'im_pages'

 L. 117       524  LOAD_FAST                'im_pages'
              526  GET_ITER         
            528_0  COME_FROM          1236  '1236'
          528_530  FOR_ITER           1240  'to 1240'
              532  STORE_FAST               'im'

 L. 122       534  LOAD_CONST               8
              536  STORE_FAST               'bits'

 L. 123       538  LOAD_CONST               None
              540  STORE_FAST               'params'

 L. 124       542  LOAD_CONST               None
              544  STORE_FAST               'decode'

 L. 126       546  LOAD_FAST                'im'
              548  LOAD_ATTR                mode
              550  LOAD_STR                 '1'
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   582  'to 582'

 L. 127       558  LOAD_STR                 'ASCIIHexDecode'
              560  STORE_FAST               'filter'

 L. 128       562  LOAD_GLOBAL              PdfParser
              564  LOAD_METHOD              PdfName
              566  LOAD_STR                 'DeviceGray'
              568  CALL_METHOD_1         1  ''
              570  STORE_FAST               'colorspace'

 L. 129       572  LOAD_STR                 'ImageB'
              574  STORE_FAST               'procset'

 L. 130       576  LOAD_CONST               1
              578  STORE_FAST               'bits'
              580  JUMP_FORWARD        778  'to 778'
            582_0  COME_FROM           554  '554'

 L. 131       582  LOAD_FAST                'im'
              584  LOAD_ATTR                mode
              586  LOAD_STR                 'L'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   614  'to 614'

 L. 132       594  LOAD_STR                 'DCTDecode'
              596  STORE_FAST               'filter'

 L. 134       598  LOAD_GLOBAL              PdfParser
              600  LOAD_METHOD              PdfName
              602  LOAD_STR                 'DeviceGray'
              604  CALL_METHOD_1         1  ''
              606  STORE_FAST               'colorspace'

 L. 135       608  LOAD_STR                 'ImageB'
              610  STORE_FAST               'procset'
              612  JUMP_FORWARD        778  'to 778'
            614_0  COME_FROM           590  '590'

 L. 136       614  LOAD_FAST                'im'
              616  LOAD_ATTR                mode
              618  LOAD_STR                 'P'
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   678  'to 678'

 L. 137       626  LOAD_STR                 'ASCIIHexDecode'
              628  STORE_FAST               'filter'

 L. 138       630  LOAD_FAST                'im'
              632  LOAD_ATTR                im
              634  LOAD_METHOD              getpalette
              636  LOAD_STR                 'RGB'
              638  CALL_METHOD_1         1  ''
              640  STORE_FAST               'palette'

 L. 140       642  LOAD_GLOBAL              PdfParser
              644  LOAD_METHOD              PdfName
              646  LOAD_STR                 'Indexed'
              648  CALL_METHOD_1         1  ''

 L. 141       650  LOAD_GLOBAL              PdfParser
              652  LOAD_METHOD              PdfName
              654  LOAD_STR                 'DeviceRGB'
              656  CALL_METHOD_1         1  ''

 L. 142       658  LOAD_CONST               255

 L. 143       660  LOAD_GLOBAL              PdfParser
              662  LOAD_METHOD              PdfBinary
              664  LOAD_FAST                'palette'
              666  CALL_METHOD_1         1  ''

 L. 139       668  BUILD_LIST_4          4 
              670  STORE_FAST               'colorspace'

 L. 145       672  LOAD_STR                 'ImageI'
              674  STORE_FAST               'procset'
              676  JUMP_FORWARD        778  'to 778'
            678_0  COME_FROM           622  '622'

 L. 146       678  LOAD_FAST                'im'
              680  LOAD_ATTR                mode
              682  LOAD_STR                 'RGB'
              684  COMPARE_OP               ==
          686_688  POP_JUMP_IF_FALSE   710  'to 710'

 L. 147       690  LOAD_STR                 'DCTDecode'
              692  STORE_FAST               'filter'

 L. 148       694  LOAD_GLOBAL              PdfParser
              696  LOAD_METHOD              PdfName
              698  LOAD_STR                 'DeviceRGB'
              700  CALL_METHOD_1         1  ''
              702  STORE_FAST               'colorspace'

 L. 149       704  LOAD_STR                 'ImageC'
              706  STORE_FAST               'procset'
              708  JUMP_FORWARD        778  'to 778'
            710_0  COME_FROM           686  '686'

 L. 150       710  LOAD_FAST                'im'
              712  LOAD_ATTR                mode
              714  LOAD_STR                 'CMYK'
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   762  'to 762'

 L. 151       722  LOAD_STR                 'DCTDecode'
              724  STORE_FAST               'filter'

 L. 152       726  LOAD_GLOBAL              PdfParser
              728  LOAD_METHOD              PdfName
              730  LOAD_STR                 'DeviceCMYK'
              732  CALL_METHOD_1         1  ''
              734  STORE_FAST               'colorspace'

 L. 153       736  LOAD_STR                 'ImageC'
              738  STORE_FAST               'procset'

 L. 154       740  LOAD_CONST               1
              742  LOAD_CONST               0
              744  LOAD_CONST               1
              746  LOAD_CONST               0
              748  LOAD_CONST               1
              750  LOAD_CONST               0
              752  LOAD_CONST               1
              754  LOAD_CONST               0
              756  BUILD_LIST_8          8 
              758  STORE_FAST               'decode'
              760  JUMP_FORWARD        778  'to 778'
            762_0  COME_FROM           718  '718'

 L. 156       762  LOAD_GLOBAL              ValueError
              764  LOAD_STR                 'cannot save mode '
              766  LOAD_FAST                'im'
              768  LOAD_ATTR                mode
              770  FORMAT_VALUE          0  ''
              772  BUILD_STRING_2        2 
              774  CALL_FUNCTION_1       1  ''
              776  RAISE_VARARGS_1       1  'exception instance'
            778_0  COME_FROM           760  '760'
            778_1  COME_FROM           708  '708'
            778_2  COME_FROM           676  '676'
            778_3  COME_FROM           612  '612'
            778_4  COME_FROM           580  '580'

 L. 161       778  LOAD_GLOBAL              io
              780  LOAD_METHOD              BytesIO
              782  CALL_METHOD_0         0  ''
              784  STORE_FAST               'op'

 L. 163       786  LOAD_FAST                'filter'
              788  LOAD_STR                 'ASCIIHexDecode'
              790  COMPARE_OP               ==
          792_794  POP_JUMP_IF_FALSE   876  'to 876'

 L. 164       796  LOAD_FAST                'bits'
              798  LOAD_CONST               1
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_FALSE   842  'to 842'

 L. 167       806  LOAD_FAST                'im'
              808  LOAD_METHOD              tobytes
              810  LOAD_STR                 'raw'
              812  LOAD_STR                 '1'
              814  CALL_METHOD_2         2  ''
              816  STORE_FAST               'data'

 L. 168       818  LOAD_GLOBAL              Image
              820  LOAD_METHOD              new
              822  LOAD_STR                 'L'
              824  LOAD_FAST                'im'
              826  LOAD_ATTR                size
              828  CALL_METHOD_2         2  ''
              830  STORE_FAST               'im'

 L. 169       832  LOAD_FAST                'im'
              834  LOAD_METHOD              putdata
              836  LOAD_FAST                'data'
              838  CALL_METHOD_1         1  ''
              840  POP_TOP          
            842_0  COME_FROM           802  '802'

 L. 170       842  LOAD_GLOBAL              ImageFile
              844  LOAD_METHOD              _save
              846  LOAD_FAST                'im'
              848  LOAD_FAST                'op'
              850  LOAD_STR                 'hex'
              852  LOAD_CONST               (0, 0)
              854  LOAD_FAST                'im'
              856  LOAD_ATTR                size
              858  BINARY_ADD       
              860  LOAD_CONST               0
              862  LOAD_FAST                'im'
              864  LOAD_ATTR                mode
              866  BUILD_TUPLE_4         4 
              868  BUILD_LIST_1          1 
              870  CALL_METHOD_3         3  ''
              872  POP_TOP          
              874  JUMP_FORWARD       1010  'to 1010'
            876_0  COME_FROM           792  '792'

 L. 171       876  LOAD_FAST                'filter'
              878  LOAD_STR                 'DCTDecode'
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   906  'to 906'

 L. 172       886  LOAD_GLOBAL              Image
              888  LOAD_ATTR                SAVE
              890  LOAD_STR                 'JPEG'
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'im'
              896  LOAD_FAST                'op'
              898  LOAD_FAST                'filename'
              900  CALL_FUNCTION_3       3  ''
              902  POP_TOP          
              904  JUMP_FORWARD       1010  'to 1010'
            906_0  COME_FROM           882  '882'

 L. 173       906  LOAD_FAST                'filter'
              908  LOAD_STR                 'FlateDecode'
              910  COMPARE_OP               ==
          912_914  POP_JUMP_IF_FALSE   950  'to 950'

 L. 174       916  LOAD_GLOBAL              ImageFile
              918  LOAD_METHOD              _save
              920  LOAD_FAST                'im'
              922  LOAD_FAST                'op'
              924  LOAD_STR                 'zip'
              926  LOAD_CONST               (0, 0)
              928  LOAD_FAST                'im'
              930  LOAD_ATTR                size
              932  BINARY_ADD       
              934  LOAD_CONST               0
              936  LOAD_FAST                'im'
              938  LOAD_ATTR                mode
              940  BUILD_TUPLE_4         4 
              942  BUILD_LIST_1          1 
              944  CALL_METHOD_3         3  ''
              946  POP_TOP          
              948  JUMP_FORWARD       1010  'to 1010'
            950_0  COME_FROM           912  '912'

 L. 175       950  LOAD_FAST                'filter'
              952  LOAD_STR                 'RunLengthDecode'
              954  COMPARE_OP               ==
          956_958  POP_JUMP_IF_FALSE   994  'to 994'

 L. 176       960  LOAD_GLOBAL              ImageFile
              962  LOAD_METHOD              _save
              964  LOAD_FAST                'im'
              966  LOAD_FAST                'op'
              968  LOAD_STR                 'packbits'
              970  LOAD_CONST               (0, 0)
              972  LOAD_FAST                'im'
              974  LOAD_ATTR                size
              976  BINARY_ADD       
              978  LOAD_CONST               0
              980  LOAD_FAST                'im'
              982  LOAD_ATTR                mode
              984  BUILD_TUPLE_4         4 
              986  BUILD_LIST_1          1 
              988  CALL_METHOD_3         3  ''
              990  POP_TOP          
              992  JUMP_FORWARD       1010  'to 1010'
            994_0  COME_FROM           956  '956'

 L. 178       994  LOAD_GLOBAL              ValueError
              996  LOAD_STR                 'unsupported PDF filter ('
              998  LOAD_FAST                'filter'
             1000  FORMAT_VALUE          0  ''
             1002  LOAD_STR                 ')'
             1004  BUILD_STRING_3        3 
             1006  CALL_FUNCTION_1       1  ''
             1008  RAISE_VARARGS_1       1  'exception instance'
           1010_0  COME_FROM           992  '992'
           1010_1  COME_FROM           948  '948'
           1010_2  COME_FROM           904  '904'
           1010_3  COME_FROM           874  '874'

 L. 183      1010  LOAD_FAST                'im'
             1012  LOAD_ATTR                size
             1014  UNPACK_SEQUENCE_2     2 
             1016  STORE_FAST               'width'
             1018  STORE_FAST               'height'

 L. 185      1020  LOAD_FAST                'existing_pdf'
             1022  LOAD_ATTR                write_obj

 L. 186      1024  LOAD_FAST                'image_refs'
             1026  LOAD_FAST                'pageNumber'
             1028  BINARY_SUBSCR    

 L. 187      1030  LOAD_FAST                'op'
             1032  LOAD_METHOD              getvalue
             1034  CALL_METHOD_0         0  ''

 L. 188      1036  LOAD_GLOBAL              PdfParser
             1038  LOAD_METHOD              PdfName
             1040  LOAD_STR                 'XObject'
             1042  CALL_METHOD_1         1  ''

 L. 189      1044  LOAD_GLOBAL              PdfParser
             1046  LOAD_METHOD              PdfName
             1048  LOAD_STR                 'Image'
             1050  CALL_METHOD_1         1  ''

 L. 190      1052  LOAD_FAST                'width'

 L. 191      1054  LOAD_FAST                'height'

 L. 192      1056  LOAD_GLOBAL              PdfParser
             1058  LOAD_METHOD              PdfName
             1060  LOAD_FAST                'filter'
             1062  CALL_METHOD_1         1  ''

 L. 193      1064  LOAD_FAST                'bits'

 L. 194      1066  LOAD_FAST                'decode'

 L. 195      1068  LOAD_FAST                'params'

 L. 196      1070  LOAD_FAST                'colorspace'

 L. 185      1072  LOAD_CONST               ('stream', 'Type', 'Subtype', 'Width', 'Height', 'Filter', 'BitsPerComponent', 'Decode', 'DecodeParams', 'ColorSpace')
             1074  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1076  POP_TOP          

 L. 202      1078  LOAD_FAST                'existing_pdf'
             1080  LOAD_ATTR                write_page

 L. 203      1082  LOAD_FAST                'page_refs'
             1084  LOAD_FAST                'pageNumber'
             1086  BINARY_SUBSCR    

 L. 204      1088  LOAD_GLOBAL              PdfParser
             1090  LOAD_ATTR                PdfDict

 L. 205      1092  LOAD_GLOBAL              PdfParser
             1094  LOAD_METHOD              PdfName
             1096  LOAD_STR                 'PDF'
             1098  CALL_METHOD_1         1  ''
             1100  LOAD_GLOBAL              PdfParser
             1102  LOAD_METHOD              PdfName
             1104  LOAD_FAST                'procset'
             1106  CALL_METHOD_1         1  ''
             1108  BUILD_LIST_2          2 

 L. 206      1110  LOAD_GLOBAL              PdfParser
             1112  LOAD_ATTR                PdfDict
             1114  LOAD_FAST                'image_refs'
             1116  LOAD_FAST                'pageNumber'
             1118  BINARY_SUBSCR    
             1120  LOAD_CONST               ('image',)
             1122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 204      1124  LOAD_CONST               ('ProcSet', 'XObject')
             1126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 209      1128  LOAD_CONST               0

 L. 210      1130  LOAD_CONST               0

 L. 211      1132  LOAD_GLOBAL              int
             1134  LOAD_FAST                'width'
             1136  LOAD_CONST               72.0
             1138  BINARY_MULTIPLY  
             1140  LOAD_FAST                'resolution'
             1142  BINARY_TRUE_DIVIDE
             1144  CALL_FUNCTION_1       1  ''

 L. 212      1146  LOAD_GLOBAL              int
             1148  LOAD_FAST                'height'
             1150  LOAD_CONST               72.0
             1152  BINARY_MULTIPLY  
             1154  LOAD_FAST                'resolution'
             1156  BINARY_TRUE_DIVIDE
             1158  CALL_FUNCTION_1       1  ''

 L. 208      1160  BUILD_LIST_4          4 

 L. 214      1162  LOAD_FAST                'contents_refs'
             1164  LOAD_FAST                'pageNumber'
             1166  BINARY_SUBSCR    

 L. 202      1168  LOAD_CONST               ('Resources', 'MediaBox', 'Contents')
             1170  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1172  POP_TOP          

 L. 220      1174  LOAD_CONST               b'q %d 0 0 %d 0 0 cm /image Do Q\n'

 L. 221      1176  LOAD_GLOBAL              int
             1178  LOAD_FAST                'width'
             1180  LOAD_CONST               72.0
             1182  BINARY_MULTIPLY  
             1184  LOAD_FAST                'resolution'
             1186  BINARY_TRUE_DIVIDE
             1188  CALL_FUNCTION_1       1  ''

 L. 222      1190  LOAD_GLOBAL              int
             1192  LOAD_FAST                'height'
             1194  LOAD_CONST               72.0
             1196  BINARY_MULTIPLY  
             1198  LOAD_FAST                'resolution'
             1200  BINARY_TRUE_DIVIDE
             1202  CALL_FUNCTION_1       1  ''

 L. 220      1204  BUILD_TUPLE_2         2 
             1206  BINARY_MODULO    
             1208  STORE_FAST               'page_contents'

 L. 225      1210  LOAD_FAST                'existing_pdf'
             1212  LOAD_ATTR                write_obj
             1214  LOAD_FAST                'contents_refs'
             1216  LOAD_FAST                'pageNumber'
             1218  BINARY_SUBSCR    
             1220  LOAD_FAST                'page_contents'
             1222  LOAD_CONST               ('stream',)
             1224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1226  POP_TOP          

 L. 227      1228  LOAD_FAST                'pageNumber'
             1230  LOAD_CONST               1
             1232  INPLACE_ADD      
             1234  STORE_FAST               'pageNumber'
         1236_1238  JUMP_BACK           528  'to 528'
           1240_0  COME_FROM           528  '528'
         1240_1242  JUMP_BACK           496  'to 496'
           1244_0  COME_FROM           496  '496'

 L. 231      1244  LOAD_FAST                'existing_pdf'
             1246  LOAD_METHOD              write_xref_and_trailer
             1248  CALL_METHOD_0         0  ''
             1250  POP_TOP          

 L. 232      1252  LOAD_GLOBAL              hasattr
             1254  LOAD_FAST                'fp'
             1256  LOAD_STR                 'flush'
             1258  CALL_FUNCTION_2       2  ''
         1260_1262  POP_JUMP_IF_FALSE  1272  'to 1272'

 L. 233      1264  LOAD_FAST                'fp'
             1266  LOAD_METHOD              flush
             1268  CALL_METHOD_0         0  ''
             1270  POP_TOP          
           1272_0  COME_FROM          1260  '1260'

 L. 234      1272  LOAD_FAST                'existing_pdf'
             1274  LOAD_METHOD              close
             1276  CALL_METHOD_0         0  ''
             1278  POP_TOP          

Parse error at or near `END_FINALLY' instruction at offset 386


Image.register_save('PDF', _save)
Image.register_save_all('PDF', _save_all)
Image.register_extension('PDF', '.pdf')
Image.register_mime('PDF', 'application/pdf')