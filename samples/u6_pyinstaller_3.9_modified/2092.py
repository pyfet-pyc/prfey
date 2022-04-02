# uncompyle6 version 3.7.4
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
            148_0  COME_FROM           184  '184'
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
              184  POP_JUMP_IF_FALSE   148  'to 148'

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
            320_0  COME_FROM           268  '268'

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
              382  JUMP_FORWARD        386  'to 386'
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
          474_476  JUMP_BACK           340  'to 340'

 L. 112       478  LOAD_FAST                'existing_pdf'
              480  LOAD_METHOD              write_catalog
              482  CALL_METHOD_0         0  ''
              484  POP_TOP          

 L. 114       486  LOAD_CONST               0
              488  STORE_FAST               'pageNumber'

 L. 115       490  LOAD_FAST                'ims'
              492  GET_ITER         
          494_496  FOR_ITER           1168  'to 1168'
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
          526_528  FOR_ITER           1164  'to 1164'
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

 L. 127       556  LOAD_STR                 'DCTDecode'
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
          778_780  POP_JUMP_IF_FALSE   816  'to 816'

 L. 164       782  LOAD_GLOBAL              ImageFile
              784  LOAD_METHOD              _save
              786  LOAD_FAST                'im'
              788  LOAD_FAST                'op'
              790  LOAD_STR                 'hex'
              792  LOAD_CONST               (0, 0)
              794  LOAD_FAST                'im'
              796  LOAD_ATTR                size
              798  BINARY_ADD       
              800  LOAD_CONST               0
              802  LOAD_FAST                'im'
              804  LOAD_ATTR                mode
              806  BUILD_TUPLE_4         4 
              808  BUILD_LIST_1          1 
              810  CALL_METHOD_3         3  ''
              812  POP_TOP          
              814  JUMP_FORWARD        950  'to 950'
            816_0  COME_FROM           778  '778'

 L. 165       816  LOAD_FAST                'filter'
              818  LOAD_STR                 'DCTDecode'
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   846  'to 846'

 L. 166       826  LOAD_GLOBAL              Image
              828  LOAD_ATTR                SAVE
              830  LOAD_STR                 'JPEG'
              832  BINARY_SUBSCR    
              834  LOAD_FAST                'im'
              836  LOAD_FAST                'op'
              838  LOAD_FAST                'filename'
              840  CALL_FUNCTION_3       3  ''
              842  POP_TOP          
              844  JUMP_FORWARD        950  'to 950'
            846_0  COME_FROM           822  '822'

 L. 167       846  LOAD_FAST                'filter'
              848  LOAD_STR                 'FlateDecode'
              850  COMPARE_OP               ==
          852_854  POP_JUMP_IF_FALSE   890  'to 890'

 L. 168       856  LOAD_GLOBAL              ImageFile
              858  LOAD_METHOD              _save
              860  LOAD_FAST                'im'
              862  LOAD_FAST                'op'
              864  LOAD_STR                 'zip'
              866  LOAD_CONST               (0, 0)
              868  LOAD_FAST                'im'
              870  LOAD_ATTR                size
              872  BINARY_ADD       
              874  LOAD_CONST               0
              876  LOAD_FAST                'im'
              878  LOAD_ATTR                mode
              880  BUILD_TUPLE_4         4 
              882  BUILD_LIST_1          1 
              884  CALL_METHOD_3         3  ''
              886  POP_TOP          
              888  JUMP_FORWARD        950  'to 950'
            890_0  COME_FROM           852  '852'

 L. 169       890  LOAD_FAST                'filter'
              892  LOAD_STR                 'RunLengthDecode'
              894  COMPARE_OP               ==
          896_898  POP_JUMP_IF_FALSE   934  'to 934'

 L. 170       900  LOAD_GLOBAL              ImageFile
              902  LOAD_METHOD              _save
              904  LOAD_FAST                'im'
              906  LOAD_FAST                'op'
              908  LOAD_STR                 'packbits'
              910  LOAD_CONST               (0, 0)
              912  LOAD_FAST                'im'
              914  LOAD_ATTR                size
              916  BINARY_ADD       
              918  LOAD_CONST               0
              920  LOAD_FAST                'im'
              922  LOAD_ATTR                mode
              924  BUILD_TUPLE_4         4 
              926  BUILD_LIST_1          1 
              928  CALL_METHOD_3         3  ''
              930  POP_TOP          
              932  JUMP_FORWARD        950  'to 950'
            934_0  COME_FROM           896  '896'

 L. 172       934  LOAD_GLOBAL              ValueError
              936  LOAD_STR                 'unsupported PDF filter ('
              938  LOAD_FAST                'filter'
              940  FORMAT_VALUE          0  ''
              942  LOAD_STR                 ')'
              944  BUILD_STRING_3        3 
              946  CALL_FUNCTION_1       1  ''
              948  RAISE_VARARGS_1       1  'exception instance'
            950_0  COME_FROM           932  '932'
            950_1  COME_FROM           888  '888'
            950_2  COME_FROM           844  '844'
            950_3  COME_FROM           814  '814'

 L. 177       950  LOAD_FAST                'im'
              952  LOAD_ATTR                size
              954  UNPACK_SEQUENCE_2     2 
              956  STORE_FAST               'width'
              958  STORE_FAST               'height'

 L. 179       960  LOAD_FAST                'existing_pdf'
              962  LOAD_ATTR                write_obj

 L. 180       964  LOAD_FAST                'image_refs'
              966  LOAD_FAST                'pageNumber'
              968  BINARY_SUBSCR    

 L. 181       970  LOAD_FAST                'op'
              972  LOAD_METHOD              getvalue
              974  CALL_METHOD_0         0  ''

 L. 182       976  LOAD_GLOBAL              PdfParser
              978  LOAD_METHOD              PdfName
              980  LOAD_STR                 'XObject'
              982  CALL_METHOD_1         1  ''

 L. 183       984  LOAD_GLOBAL              PdfParser
              986  LOAD_METHOD              PdfName
              988  LOAD_STR                 'Image'
              990  CALL_METHOD_1         1  ''

 L. 184       992  LOAD_FAST                'width'

 L. 185       994  LOAD_FAST                'height'

 L. 186       996  LOAD_GLOBAL              PdfParser
              998  LOAD_METHOD              PdfName
             1000  LOAD_FAST                'filter'
             1002  CALL_METHOD_1         1  ''

 L. 187      1004  LOAD_FAST                'bits'

 L. 188      1006  LOAD_FAST                'decode'

 L. 189      1008  LOAD_FAST                'params'

 L. 190      1010  LOAD_FAST                'colorspace'

 L. 179      1012  LOAD_CONST               ('stream', 'Type', 'Subtype', 'Width', 'Height', 'Filter', 'BitsPerComponent', 'Decode', 'DecodeParams', 'ColorSpace')
             1014  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1016  POP_TOP          

 L. 196      1018  LOAD_FAST                'existing_pdf'
             1020  LOAD_ATTR                write_page

 L. 197      1022  LOAD_FAST                'page_refs'
             1024  LOAD_FAST                'pageNumber'
             1026  BINARY_SUBSCR    

 L. 198      1028  LOAD_GLOBAL              PdfParser
             1030  LOAD_ATTR                PdfDict

 L. 199      1032  LOAD_GLOBAL              PdfParser
             1034  LOAD_METHOD              PdfName
             1036  LOAD_STR                 'PDF'
             1038  CALL_METHOD_1         1  ''
             1040  LOAD_GLOBAL              PdfParser
             1042  LOAD_METHOD              PdfName
             1044  LOAD_FAST                'procset'
             1046  CALL_METHOD_1         1  ''
             1048  BUILD_LIST_2          2 

 L. 200      1050  LOAD_GLOBAL              PdfParser
             1052  LOAD_ATTR                PdfDict
             1054  LOAD_FAST                'image_refs'
             1056  LOAD_FAST                'pageNumber'
             1058  BINARY_SUBSCR    
             1060  LOAD_CONST               ('image',)
             1062  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 198      1064  LOAD_CONST               ('ProcSet', 'XObject')
             1066  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 203      1068  LOAD_CONST               0

 L. 204      1070  LOAD_CONST               0

 L. 205      1072  LOAD_FAST                'width'
             1074  LOAD_CONST               72.0
             1076  BINARY_MULTIPLY  
             1078  LOAD_FAST                'resolution'
             1080  BINARY_TRUE_DIVIDE

 L. 206      1082  LOAD_FAST                'height'
             1084  LOAD_CONST               72.0
             1086  BINARY_MULTIPLY  
             1088  LOAD_FAST                'resolution'
             1090  BINARY_TRUE_DIVIDE

 L. 202      1092  BUILD_LIST_4          4 

 L. 208      1094  LOAD_FAST                'contents_refs'
             1096  LOAD_FAST                'pageNumber'
             1098  BINARY_SUBSCR    

 L. 196      1100  LOAD_CONST               ('Resources', 'MediaBox', 'Contents')
             1102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1104  POP_TOP          

 L. 214      1106  LOAD_CONST               b'q %f 0 0 %f 0 0 cm /image Do Q\n'

 L. 215      1108  LOAD_FAST                'width'
             1110  LOAD_CONST               72.0
             1112  BINARY_MULTIPLY  
             1114  LOAD_FAST                'resolution'
             1116  BINARY_TRUE_DIVIDE

 L. 216      1118  LOAD_FAST                'height'
             1120  LOAD_CONST               72.0
             1122  BINARY_MULTIPLY  
             1124  LOAD_FAST                'resolution'
             1126  BINARY_TRUE_DIVIDE

 L. 214      1128  BUILD_TUPLE_2         2 
             1130  BINARY_MODULO    
             1132  STORE_FAST               'page_contents'

 L. 219      1134  LOAD_FAST                'existing_pdf'
             1136  LOAD_ATTR                write_obj
             1138  LOAD_FAST                'contents_refs'
             1140  LOAD_FAST                'pageNumber'
             1142  BINARY_SUBSCR    
             1144  LOAD_FAST                'page_contents'
             1146  LOAD_CONST               ('stream',)
             1148  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1150  POP_TOP          

 L. 221      1152  LOAD_FAST                'pageNumber'
             1154  LOAD_CONST               1
             1156  INPLACE_ADD      
             1158  STORE_FAST               'pageNumber'
         1160_1162  JUMP_BACK           526  'to 526'
         1164_1166  JUMP_BACK           494  'to 494'

 L. 225      1168  LOAD_FAST                'existing_pdf'
             1170  LOAD_METHOD              write_xref_and_trailer
             1172  CALL_METHOD_0         0  ''
             1174  POP_TOP          

 L. 226      1176  LOAD_GLOBAL              hasattr
             1178  LOAD_FAST                'fp'
             1180  LOAD_STR                 'flush'
             1182  CALL_FUNCTION_2       2  ''
         1184_1186  POP_JUMP_IF_FALSE  1196  'to 1196'

 L. 227      1188  LOAD_FAST                'fp'
             1190  LOAD_METHOD              flush
             1192  CALL_METHOD_0         0  ''
             1194  POP_TOP          
           1196_0  COME_FROM          1184  '1184'

 L. 228      1196  LOAD_FAST                'existing_pdf'
             1198  LOAD_METHOD              close
             1200  CALL_METHOD_0         0  ''
             1202  POP_TOP          

Parse error at or near `<118>' instruction at offset 162


Image.register_save('PDF', _save)
Image.register_save_all('PDF', _save_all)
Image.register_extension('PDF', '.pdf')
Image.register_mime('PDF', 'application/pdf')