# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PdfImagePlugin.py
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
              246  LOAD_STR                 'created by Pillow {} PDF driver'
              248  LOAD_METHOD              format
              250  LOAD_GLOBAL              __version__
              252  CALL_METHOD_1         1  ''
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L.  84       258  LOAD_FAST                'im'
              260  BUILD_LIST_1          1 
              262  STORE_FAST               'ims'

 L.  85       264  LOAD_FAST                'save_all'
          266_268  POP_JUMP_IF_FALSE   318  'to 318'

 L.  86       270  LOAD_FAST                'im'
              272  LOAD_ATTR                encoderinfo
              274  LOAD_METHOD              get
              276  LOAD_STR                 'append_images'
              278  BUILD_LIST_0          0 
              280  CALL_METHOD_2         2  ''
              282  STORE_FAST               'append_images'

 L.  87       284  LOAD_FAST                'append_images'
              286  GET_ITER         
            288_0  COME_FROM           314  '314'
              288  FOR_ITER            318  'to 318'
              290  STORE_FAST               'append_im'

 L.  88       292  LOAD_FAST                'im'
              294  LOAD_ATTR                encoderinfo
              296  LOAD_METHOD              copy
              298  CALL_METHOD_0         0  ''
              300  LOAD_FAST                'append_im'
              302  STORE_ATTR               encoderinfo

 L.  89       304  LOAD_FAST                'ims'
              306  LOAD_METHOD              append
              308  LOAD_FAST                'append_im'
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
          314_316  JUMP_BACK           288  'to 288'
            318_0  COME_FROM           288  '288'
            318_1  COME_FROM           266  '266'

 L.  90       318  LOAD_CONST               0
              320  STORE_FAST               'numberOfPages'

 L.  91       322  BUILD_LIST_0          0 
              324  STORE_FAST               'image_refs'

 L.  92       326  BUILD_LIST_0          0 
              328  STORE_FAST               'page_refs'

 L.  93       330  BUILD_LIST_0          0 
              332  STORE_FAST               'contents_refs'

 L.  94       334  LOAD_FAST                'ims'
              336  GET_ITER         
            338_0  COME_FROM           474  '474'
              338  FOR_ITER            478  'to 478'
              340  STORE_FAST               'im'

 L.  95       342  LOAD_CONST               1
              344  STORE_FAST               'im_numberOfPages'

 L.  96       346  LOAD_FAST                'save_all'
          348_350  POP_JUMP_IF_FALSE   386  'to 386'

 L.  97       352  SETUP_FINALLY       364  'to 364'

 L.  98       354  LOAD_FAST                'im'
              356  LOAD_ATTR                n_frames
              358  STORE_FAST               'im_numberOfPages'
              360  POP_BLOCK        
              362  JUMP_FORWARD        386  'to 386'
            364_0  COME_FROM_FINALLY   352  '352'

 L.  99       364  DUP_TOP          
              366  LOAD_GLOBAL              AttributeError
              368  COMPARE_OP               exception-match
          370_372  POP_JUMP_IF_FALSE   384  'to 384'
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 102       380  POP_EXCEPT       
              382  BREAK_LOOP          386  'to 386'
            384_0  COME_FROM           370  '370'
              384  END_FINALLY      
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           362  '362'
            386_2  COME_FROM           348  '348'

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
          474_476  JUMP_BACK           338  'to 338'
            478_0  COME_FROM           338  '338'

 L. 112       478  LOAD_FAST                'existing_pdf'
              480  LOAD_METHOD              write_catalog
              482  CALL_METHOD_0         0  ''
              484  POP_TOP          

 L. 114       486  LOAD_CONST               0
              488  STORE_FAST               'pageNumber'

 L. 115       490  LOAD_FAST                'ims'
              492  GET_ITER         
            494_0  COME_FROM          1212  '1212'
          494_496  FOR_ITER           1216  'to 1216'
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
            526_0  COME_FROM          1208  '1208'
          526_528  FOR_ITER           1212  'to 1212'
              530  STORE_FAST               'im'

 L. 122       532  LOAD_CONST               8
              534  STORE_FAST               'bits'

 L. 123       536  LOAD_CONST               None
              538  STORE_FAST               'params'

 L. 125       540  LOAD_FAST                'im'
              542  LOAD_ATTR                mode
              544  LOAD_STR                 '1'
              546  COMPARE_OP               ==
          548_550  POP_JUMP_IF_FALSE   576  'to 576'

 L. 126       552  LOAD_STR                 'ASCIIHexDecode'
              554  STORE_FAST               'filter'

 L. 127       556  LOAD_GLOBAL              PdfParser
              558  LOAD_METHOD              PdfName
              560  LOAD_STR                 'DeviceGray'
              562  CALL_METHOD_1         1  ''
              564  STORE_FAST               'colorspace'

 L. 128       566  LOAD_STR                 'ImageB'
              568  STORE_FAST               'procset'

 L. 129       570  LOAD_CONST               1
              572  STORE_FAST               'bits'
              574  JUMP_FORWARD        750  'to 750'
            576_0  COME_FROM           548  '548'

 L. 130       576  LOAD_FAST                'im'
              578  LOAD_ATTR                mode
              580  LOAD_STR                 'L'
              582  COMPARE_OP               ==
          584_586  POP_JUMP_IF_FALSE   608  'to 608'

 L. 131       588  LOAD_STR                 'DCTDecode'
              590  STORE_FAST               'filter'

 L. 133       592  LOAD_GLOBAL              PdfParser
              594  LOAD_METHOD              PdfName
              596  LOAD_STR                 'DeviceGray'
              598  CALL_METHOD_1         1  ''
              600  STORE_FAST               'colorspace'

 L. 134       602  LOAD_STR                 'ImageB'
              604  STORE_FAST               'procset'
              606  JUMP_FORWARD        750  'to 750'
            608_0  COME_FROM           584  '584'

 L. 135       608  LOAD_FAST                'im'
              610  LOAD_ATTR                mode
              612  LOAD_STR                 'P'
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   672  'to 672'

 L. 136       620  LOAD_STR                 'ASCIIHexDecode'
              622  STORE_FAST               'filter'

 L. 137       624  LOAD_FAST                'im'
              626  LOAD_ATTR                im
              628  LOAD_METHOD              getpalette
              630  LOAD_STR                 'RGB'
              632  CALL_METHOD_1         1  ''
              634  STORE_FAST               'palette'

 L. 139       636  LOAD_GLOBAL              PdfParser
              638  LOAD_METHOD              PdfName
              640  LOAD_STR                 'Indexed'
              642  CALL_METHOD_1         1  ''

 L. 140       644  LOAD_GLOBAL              PdfParser
              646  LOAD_METHOD              PdfName
              648  LOAD_STR                 'DeviceRGB'
              650  CALL_METHOD_1         1  ''

 L. 141       652  LOAD_CONST               255

 L. 142       654  LOAD_GLOBAL              PdfParser
              656  LOAD_METHOD              PdfBinary
              658  LOAD_FAST                'palette'
              660  CALL_METHOD_1         1  ''

 L. 138       662  BUILD_LIST_4          4 
              664  STORE_FAST               'colorspace'

 L. 144       666  LOAD_STR                 'ImageI'
              668  STORE_FAST               'procset'
              670  JUMP_FORWARD        750  'to 750'
            672_0  COME_FROM           616  '616'

 L. 145       672  LOAD_FAST                'im'
              674  LOAD_ATTR                mode
              676  LOAD_STR                 'RGB'
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   704  'to 704'

 L. 146       684  LOAD_STR                 'DCTDecode'
              686  STORE_FAST               'filter'

 L. 147       688  LOAD_GLOBAL              PdfParser
              690  LOAD_METHOD              PdfName
              692  LOAD_STR                 'DeviceRGB'
              694  CALL_METHOD_1         1  ''
              696  STORE_FAST               'colorspace'

 L. 148       698  LOAD_STR                 'ImageC'
              700  STORE_FAST               'procset'
              702  JUMP_FORWARD        750  'to 750'
            704_0  COME_FROM           680  '680'

 L. 149       704  LOAD_FAST                'im'
              706  LOAD_ATTR                mode
              708  LOAD_STR                 'CMYK'
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   736  'to 736'

 L. 150       716  LOAD_STR                 'DCTDecode'
              718  STORE_FAST               'filter'

 L. 151       720  LOAD_GLOBAL              PdfParser
              722  LOAD_METHOD              PdfName
              724  LOAD_STR                 'DeviceCMYK'
              726  CALL_METHOD_1         1  ''
              728  STORE_FAST               'colorspace'

 L. 152       730  LOAD_STR                 'ImageC'
              732  STORE_FAST               'procset'
              734  JUMP_FORWARD        750  'to 750'
            736_0  COME_FROM           712  '712'

 L. 154       736  LOAD_GLOBAL              ValueError
              738  LOAD_STR                 'cannot save mode %s'
              740  LOAD_FAST                'im'
              742  LOAD_ATTR                mode
              744  BINARY_MODULO    
              746  CALL_FUNCTION_1       1  ''
              748  RAISE_VARARGS_1       1  'exception instance'
            750_0  COME_FROM           734  '734'
            750_1  COME_FROM           702  '702'
            750_2  COME_FROM           670  '670'
            750_3  COME_FROM           606  '606'
            750_4  COME_FROM           574  '574'

 L. 159       750  LOAD_GLOBAL              io
              752  LOAD_METHOD              BytesIO
              754  CALL_METHOD_0         0  ''
              756  STORE_FAST               'op'

 L. 161       758  LOAD_FAST                'filter'
              760  LOAD_STR                 'ASCIIHexDecode'
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   848  'to 848'

 L. 162       768  LOAD_FAST                'bits'
              770  LOAD_CONST               1
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_FALSE   814  'to 814'

 L. 165       778  LOAD_FAST                'im'
              780  LOAD_METHOD              tobytes
              782  LOAD_STR                 'raw'
              784  LOAD_STR                 '1'
              786  CALL_METHOD_2         2  ''
              788  STORE_FAST               'data'

 L. 166       790  LOAD_GLOBAL              Image
              792  LOAD_METHOD              new
              794  LOAD_STR                 'L'
              796  LOAD_FAST                'im'
              798  LOAD_ATTR                size
              800  CALL_METHOD_2         2  ''
              802  STORE_FAST               'im'

 L. 167       804  LOAD_FAST                'im'
              806  LOAD_METHOD              putdata
              808  LOAD_FAST                'data'
              810  CALL_METHOD_1         1  ''
              812  POP_TOP          
            814_0  COME_FROM           774  '774'

 L. 168       814  LOAD_GLOBAL              ImageFile
              816  LOAD_METHOD              _save
              818  LOAD_FAST                'im'
              820  LOAD_FAST                'op'
              822  LOAD_STR                 'hex'
              824  LOAD_CONST               (0, 0)
              826  LOAD_FAST                'im'
              828  LOAD_ATTR                size
              830  BINARY_ADD       
              832  LOAD_CONST               0
              834  LOAD_FAST                'im'
              836  LOAD_ATTR                mode
              838  BUILD_TUPLE_4         4 
              840  BUILD_LIST_1          1 
              842  CALL_METHOD_3         3  ''
              844  POP_TOP          
              846  JUMP_FORWARD        978  'to 978'
            848_0  COME_FROM           764  '764'

 L. 169       848  LOAD_FAST                'filter'
              850  LOAD_STR                 'DCTDecode'
              852  COMPARE_OP               ==
          854_856  POP_JUMP_IF_FALSE   878  'to 878'

 L. 170       858  LOAD_GLOBAL              Image
              860  LOAD_ATTR                SAVE
              862  LOAD_STR                 'JPEG'
              864  BINARY_SUBSCR    
              866  LOAD_FAST                'im'
              868  LOAD_FAST                'op'
              870  LOAD_FAST                'filename'
              872  CALL_FUNCTION_3       3  ''
              874  POP_TOP          
              876  JUMP_FORWARD        978  'to 978'
            878_0  COME_FROM           854  '854'

 L. 171       878  LOAD_FAST                'filter'
              880  LOAD_STR                 'FlateDecode'
              882  COMPARE_OP               ==
          884_886  POP_JUMP_IF_FALSE   922  'to 922'

 L. 172       888  LOAD_GLOBAL              ImageFile
              890  LOAD_METHOD              _save
              892  LOAD_FAST                'im'
              894  LOAD_FAST                'op'
              896  LOAD_STR                 'zip'
              898  LOAD_CONST               (0, 0)
              900  LOAD_FAST                'im'
              902  LOAD_ATTR                size
              904  BINARY_ADD       
              906  LOAD_CONST               0
              908  LOAD_FAST                'im'
              910  LOAD_ATTR                mode
              912  BUILD_TUPLE_4         4 
              914  BUILD_LIST_1          1 
              916  CALL_METHOD_3         3  ''
              918  POP_TOP          
              920  JUMP_FORWARD        978  'to 978'
            922_0  COME_FROM           884  '884'

 L. 173       922  LOAD_FAST                'filter'
              924  LOAD_STR                 'RunLengthDecode'
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_FALSE   966  'to 966'

 L. 174       932  LOAD_GLOBAL              ImageFile
              934  LOAD_METHOD              _save
              936  LOAD_FAST                'im'
              938  LOAD_FAST                'op'
              940  LOAD_STR                 'packbits'
              942  LOAD_CONST               (0, 0)
              944  LOAD_FAST                'im'
              946  LOAD_ATTR                size
              948  BINARY_ADD       
              950  LOAD_CONST               0
              952  LOAD_FAST                'im'
              954  LOAD_ATTR                mode
              956  BUILD_TUPLE_4         4 
              958  BUILD_LIST_1          1 
              960  CALL_METHOD_3         3  ''
              962  POP_TOP          
              964  JUMP_FORWARD        978  'to 978'
            966_0  COME_FROM           928  '928'

 L. 176       966  LOAD_GLOBAL              ValueError
              968  LOAD_STR                 'unsupported PDF filter (%s)'
              970  LOAD_FAST                'filter'
              972  BINARY_MODULO    
              974  CALL_FUNCTION_1       1  ''
              976  RAISE_VARARGS_1       1  'exception instance'
            978_0  COME_FROM           964  '964'
            978_1  COME_FROM           920  '920'
            978_2  COME_FROM           876  '876'
            978_3  COME_FROM           846  '846'

 L. 181       978  LOAD_FAST                'im'
              980  LOAD_ATTR                size
              982  UNPACK_SEQUENCE_2     2 
              984  STORE_FAST               'width'
              986  STORE_FAST               'height'

 L. 183       988  LOAD_FAST                'existing_pdf'
              990  LOAD_ATTR                write_obj

 L. 184       992  LOAD_FAST                'image_refs'
              994  LOAD_FAST                'pageNumber'
              996  BINARY_SUBSCR    

 L. 185       998  LOAD_FAST                'op'
             1000  LOAD_METHOD              getvalue
             1002  CALL_METHOD_0         0  ''

 L. 186      1004  LOAD_GLOBAL              PdfParser
             1006  LOAD_METHOD              PdfName
             1008  LOAD_STR                 'XObject'
             1010  CALL_METHOD_1         1  ''

 L. 187      1012  LOAD_GLOBAL              PdfParser
             1014  LOAD_METHOD              PdfName
             1016  LOAD_STR                 'Image'
             1018  CALL_METHOD_1         1  ''

 L. 188      1020  LOAD_FAST                'width'

 L. 189      1022  LOAD_FAST                'height'

 L. 190      1024  LOAD_GLOBAL              PdfParser
             1026  LOAD_METHOD              PdfName
             1028  LOAD_FAST                'filter'
             1030  CALL_METHOD_1         1  ''

 L. 191      1032  LOAD_FAST                'bits'

 L. 192      1034  LOAD_FAST                'params'

 L. 193      1036  LOAD_FAST                'colorspace'

 L. 183      1038  LOAD_CONST               ('stream', 'Type', 'Subtype', 'Width', 'Height', 'Filter', 'BitsPerComponent', 'DecodeParams', 'ColorSpace')
             1040  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
             1042  POP_TOP          

 L. 199      1044  LOAD_FAST                'existing_pdf'
             1046  LOAD_ATTR                write_page

 L. 200      1048  LOAD_FAST                'page_refs'
             1050  LOAD_FAST                'pageNumber'
             1052  BINARY_SUBSCR    

 L. 201      1054  LOAD_GLOBAL              PdfParser
             1056  LOAD_ATTR                PdfDict

 L. 202      1058  LOAD_GLOBAL              PdfParser
             1060  LOAD_METHOD              PdfName
             1062  LOAD_STR                 'PDF'
             1064  CALL_METHOD_1         1  ''
             1066  LOAD_GLOBAL              PdfParser
             1068  LOAD_METHOD              PdfName
             1070  LOAD_FAST                'procset'
             1072  CALL_METHOD_1         1  ''
             1074  BUILD_LIST_2          2 

 L. 203      1076  LOAD_GLOBAL              PdfParser
             1078  LOAD_ATTR                PdfDict
             1080  LOAD_FAST                'image_refs'
             1082  LOAD_FAST                'pageNumber'
             1084  BINARY_SUBSCR    
             1086  LOAD_CONST               ('image',)
             1088  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 201      1090  LOAD_CONST               ('ProcSet', 'XObject')
             1092  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 206      1094  LOAD_CONST               0

 L. 207      1096  LOAD_CONST               0

 L. 208      1098  LOAD_GLOBAL              int
             1100  LOAD_FAST                'width'
             1102  LOAD_CONST               72.0
             1104  BINARY_MULTIPLY  
             1106  LOAD_FAST                'resolution'
             1108  BINARY_TRUE_DIVIDE
             1110  CALL_FUNCTION_1       1  ''

 L. 209      1112  LOAD_GLOBAL              int
             1114  LOAD_FAST                'height'
             1116  LOAD_CONST               72.0
             1118  BINARY_MULTIPLY  
             1120  LOAD_FAST                'resolution'
             1122  BINARY_TRUE_DIVIDE
             1124  CALL_FUNCTION_1       1  ''

 L. 205      1126  BUILD_LIST_4          4 

 L. 211      1128  LOAD_FAST                'contents_refs'
             1130  LOAD_FAST                'pageNumber'
             1132  BINARY_SUBSCR    

 L. 199      1134  LOAD_CONST               ('Resources', 'MediaBox', 'Contents')
             1136  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1138  POP_TOP          

 L. 217      1140  LOAD_GLOBAL              PdfParser
             1142  LOAD_METHOD              make_bytes

 L. 218      1144  LOAD_STR                 'q %d 0 0 %d 0 0 cm /image Do Q\n'

 L. 219      1146  LOAD_GLOBAL              int
             1148  LOAD_FAST                'width'
             1150  LOAD_CONST               72.0
             1152  BINARY_MULTIPLY  
             1154  LOAD_FAST                'resolution'
             1156  BINARY_TRUE_DIVIDE
             1158  CALL_FUNCTION_1       1  ''
             1160  LOAD_GLOBAL              int
             1162  LOAD_FAST                'height'
             1164  LOAD_CONST               72.0
             1166  BINARY_MULTIPLY  
             1168  LOAD_FAST                'resolution'
             1170  BINARY_TRUE_DIVIDE
             1172  CALL_FUNCTION_1       1  ''
             1174  BUILD_TUPLE_2         2 

 L. 218      1176  BINARY_MODULO    

 L. 217      1178  CALL_METHOD_1         1  ''
             1180  STORE_FAST               'page_contents'

 L. 222      1182  LOAD_FAST                'existing_pdf'
             1184  LOAD_ATTR                write_obj
             1186  LOAD_FAST                'contents_refs'
             1188  LOAD_FAST                'pageNumber'
             1190  BINARY_SUBSCR    
             1192  LOAD_FAST                'page_contents'
             1194  LOAD_CONST               ('stream',)
             1196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1198  POP_TOP          

 L. 224      1200  LOAD_FAST                'pageNumber'
             1202  LOAD_CONST               1
             1204  INPLACE_ADD      
             1206  STORE_FAST               'pageNumber'
         1208_1210  JUMP_BACK           526  'to 526'
           1212_0  COME_FROM           526  '526'
         1212_1214  JUMP_BACK           494  'to 494'
           1216_0  COME_FROM           494  '494'

 L. 228      1216  LOAD_FAST                'existing_pdf'
             1218  LOAD_METHOD              write_xref_and_trailer
             1220  CALL_METHOD_0         0  ''
             1222  POP_TOP          

 L. 229      1224  LOAD_GLOBAL              hasattr
             1226  LOAD_FAST                'fp'
             1228  LOAD_STR                 'flush'
             1230  CALL_FUNCTION_2       2  ''
         1232_1234  POP_JUMP_IF_FALSE  1244  'to 1244'

 L. 230      1236  LOAD_FAST                'fp'
             1238  LOAD_METHOD              flush
             1240  CALL_METHOD_0         0  ''
             1242  POP_TOP          
           1244_0  COME_FROM          1232  '1232'

 L. 231      1244  LOAD_FAST                'existing_pdf'
             1246  LOAD_METHOD              close
             1248  CALL_METHOD_0         0  ''
             1250  POP_TOP          

Parse error at or near `END_FINALLY' instruction at offset 384


Image.register_save('PDF', _save)
Image.register_save_all('PDF', _save_all)
Image.register_extension('PDF', '.pdf')
Image.register_mime('PDF', 'application/pdf')