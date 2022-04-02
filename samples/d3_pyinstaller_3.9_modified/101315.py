# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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
              162  <118>                 0  ''
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
            340_0  COME_FROM           474  '474'
              340  FOR_ITER            478  'to 478'
              342  STORE_FAST               'im'

 L.  95       344  LOAD_CONST               1
              346  STORE_FAST               'im_numberOfPages'

 L.  96       348  LOAD_FAST                'save_all'
          350_352  POP_JUMP_IF_FALSE   386  'to 386'

 L.  97       354  SETUP_FINALLY       366  'to 366'

 L.  98       356  LOAD_FAST                'im'
              358  LOAD_ATTR                n_frames
              360  STORE_FAST               'im_numberOfPages'
              362  POP_BLOCK        
              364  JUMP_FORWARD        386  'to 386'
            366_0  COME_FROM_FINALLY   354  '354'

 L.  99       366  DUP_TOP          
              368  LOAD_GLOBAL              AttributeError
          370_372  <121>               384  ''
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 102       380  POP_EXCEPT       
              382  BREAK_LOOP          386  'to 386'
              384  <48>             
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           364  '364'
            386_2  COME_FROM           350  '350'

 L. 103       386  LOAD_FAST                'numberOfPages'
              388  LOAD_FAST                'im_numberOfPages'
              390  INPLACE_ADD      
              392  STORE_FAST               'numberOfPages'

 L. 104       394  LOAD_GLOBAL              range
              396  LOAD_FAST                'im_numberOfPages'
              398  CALL_FUNCTION_1       1  ''
              400  GET_ITER         
            402_0  COME_FROM           470  '470'
              402  FOR_ITER            474  'to 474'
              404  STORE_FAST               'i'

 L. 105       406  LOAD_FAST                'image_refs'
              408  LOAD_METHOD              append
              410  LOAD_FAST                'existing_pdf'
              412  LOAD_METHOD              next_object_id
              414  LOAD_CONST               0
              416  CALL_METHOD_1         1  ''
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          

 L. 106       422  LOAD_FAST                'page_refs'
              424  LOAD_METHOD              append
              426  LOAD_FAST                'existing_pdf'
              428  LOAD_METHOD              next_object_id
              430  LOAD_CONST               0
              432  CALL_METHOD_1         1  ''
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          

 L. 107       438  LOAD_FAST                'contents_refs'
              440  LOAD_METHOD              append
              442  LOAD_FAST                'existing_pdf'
              444  LOAD_METHOD              next_object_id
              446  LOAD_CONST               0
              448  CALL_METHOD_1         1  ''
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          

 L. 108       454  LOAD_FAST                'existing_pdf'
              456  LOAD_ATTR                pages
              458  LOAD_METHOD              append
              460  LOAD_FAST                'page_refs'
              462  LOAD_CONST               -1
              464  BINARY_SUBSCR    
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
          470_472  JUMP_BACK           402  'to 402'
            474_0  COME_FROM           402  '402'
          474_476  JUMP_BACK           340  'to 340'
            478_0  COME_FROM           340  '340'

 L. 112       478  LOAD_FAST                'existing_pdf'
              480  LOAD_METHOD              write_catalog
              482  CALL_METHOD_0         0  ''
              484  POP_TOP          

 L. 114       486  LOAD_CONST               0
              488  STORE_FAST               'pageNumber'

 L. 115       490  LOAD_FAST                'ims'
              492  GET_ITER         
            494_0  COME_FROM          1226  '1226'
          494_496  FOR_ITER           1230  'to 1230'
              498  STORE_FAST               'imSequence'

 L. 116       500  LOAD_FAST                'save_all'
          502_504  POP_JUMP_IF_FALSE   516  'to 516'
              506  LOAD_GLOBAL              ImageSequence
              508  LOAD_METHOD              Iterator
              510  LOAD_FAST                'imSequence'
              512  CALL_METHOD_1         1  ''
              514  JUMP_FORWARD        520  'to 520'
            516_0  COME_FROM           502  '502'
              516  LOAD_FAST                'imSequence'
              518  BUILD_LIST_1          1 
            520_0  COME_FROM           514  '514'
              520  STORE_FAST               'im_pages'

 L. 117       522  LOAD_FAST                'im_pages'
              524  GET_ITER         
            526_0  COME_FROM          1222  '1222'
          526_528  FOR_ITER           1226  'to 1226'
              530  STORE_FAST               'im'

 L. 122       532  LOAD_CONST               8
              534  STORE_FAST               'bits'

 L. 123       536  LOAD_CONST               None
              538  STORE_FAST               'params'

 L. 124       540  LOAD_CONST               None
              542  STORE_FAST               'decode'

 L. 126       544  LOAD_FAST                'im'
              546  LOAD_ATTR                mode
              548  LOAD_STR                 '1'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   580  'to 580'

 L. 127       556  LOAD_STR                 'ASCIIHexDecode'
              558  STORE_FAST               'filter'

 L. 128       560  LOAD_GLOBAL              PdfParser
              562  LOAD_METHOD              PdfName
              564  LOAD_STR                 'DeviceGray'
              566  CALL_METHOD_1         1  ''
              568  STORE_FAST               'colorspace'

 L. 129       570  LOAD_STR                 'ImageB'
              572  STORE_FAST               'procset'

 L. 130       574  LOAD_CONST               1
              576  STORE_FAST               'bits'
              578  JUMP_FORWARD        764  'to 764'
            580_0  COME_FROM           552  '552'

 L. 131       580  LOAD_FAST                'im'
              582  LOAD_ATTR                mode
              584  LOAD_STR                 'L'
              586  COMPARE_OP               ==
          588_590  POP_JUMP_IF_FALSE   612  'to 612'

 L. 132       592  LOAD_STR                 'DCTDecode'
              594  STORE_FAST               'filter'

 L. 134       596  LOAD_GLOBAL              PdfParser
              598  LOAD_METHOD              PdfName
              600  LOAD_STR                 'DeviceGray'
              602  CALL_METHOD_1         1  ''
              604  STORE_FAST               'colorspace'

 L. 135       606  LOAD_STR                 'ImageB'
              608  STORE_FAST               'procset'
              610  JUMP_FORWARD        764  'to 764'
            612_0  COME_FROM           588  '588'

 L. 136       612  LOAD_FAST                'im'
              614  LOAD_ATTR                mode
              616  LOAD_STR                 'P'
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_FALSE   676  'to 676'

 L. 137       624  LOAD_STR                 'ASCIIHexDecode'
              626  STORE_FAST               'filter'

 L. 138       628  LOAD_FAST                'im'
              630  LOAD_ATTR                im
              632  LOAD_METHOD              getpalette
              634  LOAD_STR                 'RGB'
              636  CALL_METHOD_1         1  ''
              638  STORE_FAST               'palette'

 L. 140       640  LOAD_GLOBAL              PdfParser
              642  LOAD_METHOD              PdfName
              644  LOAD_STR                 'Indexed'
              646  CALL_METHOD_1         1  ''

 L. 141       648  LOAD_GLOBAL              PdfParser
              650  LOAD_METHOD              PdfName
              652  LOAD_STR                 'DeviceRGB'
              654  CALL_METHOD_1         1  ''

 L. 142       656  LOAD_CONST               255

 L. 143       658  LOAD_GLOBAL              PdfParser
              660  LOAD_METHOD              PdfBinary
              662  LOAD_FAST                'palette'
              664  CALL_METHOD_1         1  ''

 L. 139       666  BUILD_LIST_4          4 
              668  STORE_FAST               'colorspace'

 L. 145       670  LOAD_STR                 'ImageI'
              672  STORE_FAST               'procset'
              674  JUMP_FORWARD        764  'to 764'
            676_0  COME_FROM           620  '620'

 L. 146       676  LOAD_FAST                'im'
              678  LOAD_ATTR                mode
              680  LOAD_STR                 'RGB'
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   708  'to 708'

 L. 147       688  LOAD_STR                 'DCTDecode'
              690  STORE_FAST               'filter'

 L. 148       692  LOAD_GLOBAL              PdfParser
              694  LOAD_METHOD              PdfName
              696  LOAD_STR                 'DeviceRGB'
              698  CALL_METHOD_1         1  ''
              700  STORE_FAST               'colorspace'

 L. 149       702  LOAD_STR                 'ImageC'
              704  STORE_FAST               'procset'
              706  JUMP_FORWARD        764  'to 764'
            708_0  COME_FROM           684  '684'

 L. 150       708  LOAD_FAST                'im'
              710  LOAD_ATTR                mode
              712  LOAD_STR                 'CMYK'
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   748  'to 748'

 L. 151       720  LOAD_STR                 'DCTDecode'
              722  STORE_FAST               'filter'

 L. 152       724  LOAD_GLOBAL              PdfParser
              726  LOAD_METHOD              PdfName
              728  LOAD_STR                 'DeviceCMYK'
              730  CALL_METHOD_1         1  ''
              732  STORE_FAST               'colorspace'

 L. 153       734  LOAD_STR                 'ImageC'
              736  STORE_FAST               'procset'

 L. 154       738  BUILD_LIST_0          0 
              740  LOAD_CONST               (1, 0, 1, 0, 1, 0, 1, 0)
              742  CALL_FINALLY        745  'to 745'
              744  STORE_FAST               'decode'
              746  JUMP_FORWARD        764  'to 764'
            748_0  COME_FROM           716  '716'

 L. 156       748  LOAD_GLOBAL              ValueError
              750  LOAD_STR                 'cannot save mode '
              752  LOAD_FAST                'im'
              754  LOAD_ATTR                mode
              756  FORMAT_VALUE          0  ''
              758  BUILD_STRING_2        2 
              760  CALL_FUNCTION_1       1  ''
              762  RAISE_VARARGS_1       1  'exception instance'
            764_0  COME_FROM           746  '746'
            764_1  COME_FROM           706  '706'
            764_2  COME_FROM           674  '674'
            764_3  COME_FROM           610  '610'
            764_4  COME_FROM           578  '578'

 L. 161       764  LOAD_GLOBAL              io
              766  LOAD_METHOD              BytesIO
              768  CALL_METHOD_0         0  ''
              770  STORE_FAST               'op'

 L. 163       772  LOAD_FAST                'filter'
              774  LOAD_STR                 'ASCIIHexDecode'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   862  'to 862'

 L. 164       782  LOAD_FAST                'bits'
              784  LOAD_CONST               1
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   828  'to 828'

 L. 167       792  LOAD_FAST                'im'
              794  LOAD_METHOD              tobytes
              796  LOAD_STR                 'raw'
              798  LOAD_STR                 '1'
              800  CALL_METHOD_2         2  ''
              802  STORE_FAST               'data'

 L. 168       804  LOAD_GLOBAL              Image
              806  LOAD_METHOD              new
              808  LOAD_STR                 'L'
              810  LOAD_FAST                'im'
              812  LOAD_ATTR                size
              814  CALL_METHOD_2         2  ''
              816  STORE_FAST               'im'

 L. 169       818  LOAD_FAST                'im'
              820  LOAD_METHOD              putdata
              822  LOAD_FAST                'data'
              824  CALL_METHOD_1         1  ''
              826  POP_TOP          
            828_0  COME_FROM           788  '788'

 L. 170       828  LOAD_GLOBAL              ImageFile
              830  LOAD_METHOD              _save
              832  LOAD_FAST                'im'
              834  LOAD_FAST                'op'
              836  LOAD_STR                 'hex'
              838  LOAD_CONST               (0, 0)
              840  LOAD_FAST                'im'
              842  LOAD_ATTR                size
              844  BINARY_ADD       
              846  LOAD_CONST               0
              848  LOAD_FAST                'im'
              850  LOAD_ATTR                mode
              852  BUILD_TUPLE_4         4 
              854  BUILD_LIST_1          1 
              856  CALL_METHOD_3         3  ''
              858  POP_TOP          
              860  JUMP_FORWARD        996  'to 996'
            862_0  COME_FROM           778  '778'

 L. 171       862  LOAD_FAST                'filter'
              864  LOAD_STR                 'DCTDecode'
              866  COMPARE_OP               ==
          868_870  POP_JUMP_IF_FALSE   892  'to 892'

 L. 172       872  LOAD_GLOBAL              Image
              874  LOAD_ATTR                SAVE
              876  LOAD_STR                 'JPEG'
              878  BINARY_SUBSCR    
              880  LOAD_FAST                'im'
              882  LOAD_FAST                'op'
              884  LOAD_FAST                'filename'
              886  CALL_FUNCTION_3       3  ''
              888  POP_TOP          
              890  JUMP_FORWARD        996  'to 996'
            892_0  COME_FROM           868  '868'

 L. 173       892  LOAD_FAST                'filter'
              894  LOAD_STR                 'FlateDecode'
              896  COMPARE_OP               ==
          898_900  POP_JUMP_IF_FALSE   936  'to 936'

 L. 174       902  LOAD_GLOBAL              ImageFile
              904  LOAD_METHOD              _save
              906  LOAD_FAST                'im'
              908  LOAD_FAST                'op'
              910  LOAD_STR                 'zip'
              912  LOAD_CONST               (0, 0)
              914  LOAD_FAST                'im'
              916  LOAD_ATTR                size
              918  BINARY_ADD       
              920  LOAD_CONST               0
              922  LOAD_FAST                'im'
              924  LOAD_ATTR                mode
              926  BUILD_TUPLE_4         4 
              928  BUILD_LIST_1          1 
              930  CALL_METHOD_3         3  ''
              932  POP_TOP          
              934  JUMP_FORWARD        996  'to 996'
            936_0  COME_FROM           898  '898'

 L. 175       936  LOAD_FAST                'filter'
              938  LOAD_STR                 'RunLengthDecode'
              940  COMPARE_OP               ==
          942_944  POP_JUMP_IF_FALSE   980  'to 980'

 L. 176       946  LOAD_GLOBAL              ImageFile
              948  LOAD_METHOD              _save
              950  LOAD_FAST                'im'
              952  LOAD_FAST                'op'
              954  LOAD_STR                 'packbits'
              956  LOAD_CONST               (0, 0)
              958  LOAD_FAST                'im'
              960  LOAD_ATTR                size
              962  BINARY_ADD       
              964  LOAD_CONST               0
              966  LOAD_FAST                'im'
              968  LOAD_ATTR                mode
              970  BUILD_TUPLE_4         4 
              972  BUILD_LIST_1          1 
              974  CALL_METHOD_3         3  ''
              976  POP_TOP          
              978  JUMP_FORWARD        996  'to 996'
            980_0  COME_FROM           942  '942'

 L. 178       980  LOAD_GLOBAL              ValueError
              982  LOAD_STR                 'unsupported PDF filter ('
              984  LOAD_FAST                'filter'
              986  FORMAT_VALUE          0  ''
              988  LOAD_STR                 ')'
              990  BUILD_STRING_3        3 
              992  CALL_FUNCTION_1       1  ''
              994  RAISE_VARARGS_1       1  'exception instance'
            996_0  COME_FROM           978  '978'
            996_1  COME_FROM           934  '934'
            996_2  COME_FROM           890  '890'
            996_3  COME_FROM           860  '860'

 L. 183       996  LOAD_FAST                'im'
              998  LOAD_ATTR                size
             1000  UNPACK_SEQUENCE_2     2 
             1002  STORE_FAST               'width'
             1004  STORE_FAST               'height'

 L. 185      1006  LOAD_FAST                'existing_pdf'
             1008  LOAD_ATTR                write_obj

 L. 186      1010  LOAD_FAST                'image_refs'
             1012  LOAD_FAST                'pageNumber'
             1014  BINARY_SUBSCR    

 L. 187      1016  LOAD_FAST                'op'
             1018  LOAD_METHOD              getvalue
             1020  CALL_METHOD_0         0  ''

 L. 188      1022  LOAD_GLOBAL              PdfParser
             1024  LOAD_METHOD              PdfName
             1026  LOAD_STR                 'XObject'
             1028  CALL_METHOD_1         1  ''

 L. 189      1030  LOAD_GLOBAL              PdfParser
             1032  LOAD_METHOD              PdfName
             1034  LOAD_STR                 'Image'
             1036  CALL_METHOD_1         1  ''

 L. 190      1038  LOAD_FAST                'width'

 L. 191      1040  LOAD_FAST                'height'

 L. 192      1042  LOAD_GLOBAL              PdfParser
             1044  LOAD_METHOD              PdfName
             1046  LOAD_FAST                'filter'
             1048  CALL_METHOD_1         1  ''

 L. 193      1050  LOAD_FAST                'bits'

 L. 194      1052  LOAD_FAST                'decode'

 L. 195      1054  LOAD_FAST                'params'

 L. 196      1056  LOAD_FAST                'colorspace'

 L. 185      1058  LOAD_CONST               ('stream', 'Type', 'Subtype', 'Width', 'Height', 'Filter', 'BitsPerComponent', 'Decode', 'DecodeParams', 'ColorSpace')
             1060  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1062  POP_TOP          

 L. 202      1064  LOAD_FAST                'existing_pdf'
             1066  LOAD_ATTR                write_page

 L. 203      1068  LOAD_FAST                'page_refs'
             1070  LOAD_FAST                'pageNumber'
             1072  BINARY_SUBSCR    

 L. 204      1074  LOAD_GLOBAL              PdfParser
             1076  LOAD_ATTR                PdfDict

 L. 205      1078  LOAD_GLOBAL              PdfParser
             1080  LOAD_METHOD              PdfName
             1082  LOAD_STR                 'PDF'
             1084  CALL_METHOD_1         1  ''
             1086  LOAD_GLOBAL              PdfParser
             1088  LOAD_METHOD              PdfName
             1090  LOAD_FAST                'procset'
             1092  CALL_METHOD_1         1  ''
             1094  BUILD_LIST_2          2 

 L. 206      1096  LOAD_GLOBAL              PdfParser
             1098  LOAD_ATTR                PdfDict
             1100  LOAD_FAST                'image_refs'
             1102  LOAD_FAST                'pageNumber'
             1104  BINARY_SUBSCR    
             1106  LOAD_CONST               ('image',)
             1108  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 204      1110  LOAD_CONST               ('ProcSet', 'XObject')
             1112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 209      1114  LOAD_CONST               0

 L. 210      1116  LOAD_CONST               0

 L. 211      1118  LOAD_GLOBAL              int
             1120  LOAD_FAST                'width'
             1122  LOAD_CONST               72.0
             1124  BINARY_MULTIPLY  
             1126  LOAD_FAST                'resolution'
             1128  BINARY_TRUE_DIVIDE
             1130  CALL_FUNCTION_1       1  ''

 L. 212      1132  LOAD_GLOBAL              int
             1134  LOAD_FAST                'height'
             1136  LOAD_CONST               72.0
             1138  BINARY_MULTIPLY  
             1140  LOAD_FAST                'resolution'
             1142  BINARY_TRUE_DIVIDE
             1144  CALL_FUNCTION_1       1  ''

 L. 208      1146  BUILD_LIST_4          4 

 L. 214      1148  LOAD_FAST                'contents_refs'
             1150  LOAD_FAST                'pageNumber'
             1152  BINARY_SUBSCR    

 L. 202      1154  LOAD_CONST               ('Resources', 'MediaBox', 'Contents')
             1156  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1158  POP_TOP          

 L. 220      1160  LOAD_CONST               b'q %d 0 0 %d 0 0 cm /image Do Q\n'

 L. 221      1162  LOAD_GLOBAL              int
             1164  LOAD_FAST                'width'
             1166  LOAD_CONST               72.0
             1168  BINARY_MULTIPLY  
             1170  LOAD_FAST                'resolution'
             1172  BINARY_TRUE_DIVIDE
             1174  CALL_FUNCTION_1       1  ''

 L. 222      1176  LOAD_GLOBAL              int
             1178  LOAD_FAST                'height'
             1180  LOAD_CONST               72.0
             1182  BINARY_MULTIPLY  
             1184  LOAD_FAST                'resolution'
             1186  BINARY_TRUE_DIVIDE
             1188  CALL_FUNCTION_1       1  ''

 L. 220      1190  BUILD_TUPLE_2         2 
             1192  BINARY_MODULO    
             1194  STORE_FAST               'page_contents'

 L. 225      1196  LOAD_FAST                'existing_pdf'
             1198  LOAD_ATTR                write_obj
             1200  LOAD_FAST                'contents_refs'
             1202  LOAD_FAST                'pageNumber'
             1204  BINARY_SUBSCR    
             1206  LOAD_FAST                'page_contents'
             1208  LOAD_CONST               ('stream',)
             1210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1212  POP_TOP          

 L. 227      1214  LOAD_FAST                'pageNumber'
             1216  LOAD_CONST               1
             1218  INPLACE_ADD      
             1220  STORE_FAST               'pageNumber'
         1222_1224  JUMP_BACK           526  'to 526'
           1226_0  COME_FROM           526  '526'
         1226_1228  JUMP_BACK           494  'to 494'
           1230_0  COME_FROM           494  '494'

 L. 231      1230  LOAD_FAST                'existing_pdf'
             1232  LOAD_METHOD              write_xref_and_trailer
             1234  CALL_METHOD_0         0  ''
             1236  POP_TOP          

 L. 232      1238  LOAD_GLOBAL              hasattr
             1240  LOAD_FAST                'fp'
             1242  LOAD_STR                 'flush'
             1244  CALL_FUNCTION_2       2  ''
         1246_1248  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 233      1250  LOAD_FAST                'fp'
             1252  LOAD_METHOD              flush
             1254  CALL_METHOD_0         0  ''
             1256  POP_TOP          
           1258_0  COME_FROM          1246  '1246'

 L. 234      1258  LOAD_FAST                'existing_pdf'
             1260  LOAD_METHOD              close
             1262  CALL_METHOD_0         0  ''
             1264  POP_TOP          

Parse error at or near `<118>' instruction at offset 162


Image.register_save('PDF', _save)
Image.register_save_all('PDF', _save_all)
Image.register_extension('PDF', '.pdf')
Image.register_mime('PDF', 'application/pdf')