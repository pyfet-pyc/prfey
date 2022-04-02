# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\puhutv.py
from __future__ import unicode_literals
from .common import InfoExtractor
from ..compat import compat_HTTPError, compat_str
from ..utils import ExtractorError, int_or_none, float_or_none, parse_resolution, str_or_none, try_get, unified_timestamp, url_or_none, urljoin

class PuhuTVIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-izle'
    IE_NAME = 'puhutv'
    _TESTS = [
     {'url':'https://puhutv.com/sut-kardesler-izle', 
      'md5':'a347470371d56e1585d1b2c8dab01c96', 
      'info_dict':{'id':'5085', 
       'display_id':'sut-kardesler', 
       'ext':'mp4', 
       'title':'Süt Kardeşler', 
       'description':'md5:ca09da25b7e57cbb5a9280d6e48d17aa', 
       'thumbnail':'re:^https?://.*\\.jpg$', 
       'duration':4832.44, 
       'creator':'Arzu Film', 
       'timestamp':1561062602, 
       'upload_date':'20190620', 
       'release_year':1976, 
       'view_count':int, 
       'tags':list}},
     {'url':'https://puhutv.com/jet-sosyete-1-bolum-izle', 
      'only_matching':True},
     {'url':'https://puhutv.com/dip-1-bolum-izle', 
      'only_matching':True}]
    _SUBTITLE_LANGS = {'English':'en', 
     'Deutsch':'de', 
     'عربى':'ar'}

    def _real_extract--- This code section failed: ---

 L.  60         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _match_id
                4  LOAD_FAST                'url'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'display_id'

 L.  62        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _download_json

 L.  63        14  LOAD_GLOBAL              urljoin
               16  LOAD_FAST                'url'
               18  LOAD_STR                 '/api/slug/%s-izle'
               20  LOAD_FAST                'display_id'
               22  BINARY_MODULO    
               24  CALL_FUNCTION_2       2  '2 positional arguments'

 L.  64        26  LOAD_FAST                'display_id'
               28  CALL_METHOD_2         2  '2 positional arguments'
               30  LOAD_STR                 'data'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'info'

 L.  66        36  LOAD_GLOBAL              compat_str
               38  LOAD_FAST                'info'
               40  LOAD_STR                 'id'
               42  BINARY_SUBSCR    
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'video_id'

 L.  67        48  LOAD_FAST                'info'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'title'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  JUMP_IF_TRUE_OR_POP    60  'to 60'
               58  BUILD_MAP_0           0 
             60_0  COME_FROM            56  '56'
               60  STORE_FAST               'show'

 L.  68        62  LOAD_FAST                'info'
               64  LOAD_METHOD              get
               66  LOAD_STR                 'name'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  JUMP_IF_TRUE_OR_POP    78  'to 78'
               72  LOAD_FAST                'show'
               74  LOAD_STR                 'name'
               76  BINARY_SUBSCR    
             78_0  COME_FROM            70  '70'
               78  STORE_FAST               'title'

 L.  69        80  LOAD_FAST                'info'
               82  LOAD_METHOD              get
               84  LOAD_STR                 'display_name'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L.  70        90  LOAD_STR                 '%s %s'
               92  LOAD_FAST                'title'
               94  LOAD_FAST                'info'
               96  LOAD_STR                 'display_name'
               98  BINARY_SUBSCR    
              100  BUILD_TUPLE_2         2 
              102  BINARY_MODULO    
              104  STORE_FAST               'title'
            106_0  COME_FROM            88  '88'

 L.  72       106  SETUP_EXCEPT        138  'to 138'

 L.  73       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _download_json

 L.  74       112  LOAD_STR                 'https://puhutv.com/api/assets/%s/videos'
              114  LOAD_FAST                'video_id'
              116  BINARY_MODULO    

 L.  75       118  LOAD_FAST                'display_id'
              120  LOAD_STR                 'Downloading video JSON'

 L.  76       122  LOAD_FAST                'self'
              124  LOAD_METHOD              geo_verification_headers
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  LOAD_CONST               ('headers',)
              130  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              132  STORE_FAST               'videos'
              134  POP_BLOCK        
              136  JUMP_FORWARD        206  'to 206'
            138_0  COME_FROM_EXCEPT    106  '106'

 L.  77       138  DUP_TOP          
              140  LOAD_GLOBAL              ExtractorError
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   204  'to 204'
              146  POP_TOP          
              148  STORE_FAST               'e'
              150  POP_TOP          
              152  SETUP_FINALLY       192  'to 192'

 L.  78       154  LOAD_GLOBAL              isinstance
              156  LOAD_FAST                'e'
              158  LOAD_ATTR                cause
              160  LOAD_GLOBAL              compat_HTTPError
              162  CALL_FUNCTION_2       2  '2 positional arguments'
              164  POP_JUMP_IF_FALSE   186  'to 186'
              166  LOAD_FAST                'e'
              168  LOAD_ATTR                cause
              170  LOAD_ATTR                code
              172  LOAD_CONST               403
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L.  79       178  LOAD_FAST                'self'
              180  LOAD_METHOD              raise_geo_restricted
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  POP_TOP          
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           164  '164'

 L.  80       186  RAISE_VARARGS_0       0  'reraise'
              188  POP_BLOCK        
              190  LOAD_CONST               None
            192_0  COME_FROM_FINALLY   152  '152'
              192  LOAD_CONST               None
              194  STORE_FAST               'e'
              196  DELETE_FAST              'e'
              198  END_FINALLY      
              200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           144  '144'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'
            206_1  COME_FROM           136  '136'

 L.  82       206  BUILD_LIST_0          0 
              208  STORE_FAST               'urls'

 L.  83       210  BUILD_LIST_0          0 
              212  STORE_FAST               'formats'

 L.  85   214_216  SETUP_LOOP          502  'to 502'
              218  LOAD_FAST                'videos'
              220  LOAD_STR                 'data'
              222  BINARY_SUBSCR    
              224  LOAD_STR                 'videos'
              226  BINARY_SUBSCR    
              228  GET_ITER         
            230_0  COME_FROM           452  '452'
            230_1  COME_FROM           252  '252'
          230_232  FOR_ITER            500  'to 500'
              234  STORE_FAST               'video'

 L.  86       236  LOAD_GLOBAL              url_or_none
              238  LOAD_FAST                'video'
              240  LOAD_METHOD              get
              242  LOAD_STR                 'url'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  STORE_FAST               'media_url'

 L.  87       250  LOAD_FAST                'media_url'
              252  POP_JUMP_IF_FALSE   230  'to 230'
              254  LOAD_FAST                'media_url'
              256  LOAD_FAST                'urls'
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_FALSE   266  'to 266'

 L.  88       264  CONTINUE            230  'to 230'
            266_0  COME_FROM           260  '260'

 L.  89       266  LOAD_FAST                'urls'
              268  LOAD_METHOD              append
              270  LOAD_FAST                'media_url'
              272  CALL_METHOD_1         1  '1 positional argument'
              274  POP_TOP          

 L.  91       276  LOAD_FAST                'video'
              278  LOAD_METHOD              get
              280  LOAD_STR                 'is_playlist'
              282  CALL_METHOD_1         1  '1 positional argument'
              284  STORE_FAST               'playlist'

 L.  92       286  LOAD_FAST                'video'
              288  LOAD_METHOD              get
              290  LOAD_STR                 'stream_type'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  LOAD_STR                 'hls'
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   312  'to 312'
              302  LOAD_FAST                'playlist'
              304  LOAD_CONST               True
              306  COMPARE_OP               is
          308_310  POP_JUMP_IF_TRUE    322  'to 322'
            312_0  COME_FROM           298  '298'
              312  LOAD_STR                 'playlist.m3u8'
              314  LOAD_FAST                'media_url'
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   352  'to 352'
            322_0  COME_FROM           308  '308'

 L.  93       322  LOAD_FAST                'formats'
              324  LOAD_METHOD              extend
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                _extract_m3u8_formats

 L.  94       330  LOAD_FAST                'media_url'
              332  LOAD_FAST                'video_id'
              334  LOAD_STR                 'mp4'
              336  LOAD_STR                 'm3u8_native'

 L.  95       338  LOAD_STR                 'hls'
              340  LOAD_CONST               False
              342  LOAD_CONST               ('entry_protocol', 'm3u8_id', 'fatal')
              344  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          

 L.  96       350  CONTINUE            230  'to 230'
            352_0  COME_FROM           318  '318'

 L.  98       352  LOAD_GLOBAL              int_or_none
              354  LOAD_FAST                'video'
              356  LOAD_METHOD              get
              358  LOAD_STR                 'quality'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  STORE_FAST               'quality'

 L. 100       366  LOAD_FAST                'media_url'

 L. 101       368  LOAD_STR                 'mp4'

 L. 102       370  LOAD_FAST                'quality'
              372  LOAD_CONST               ('url', 'ext', 'height')
              374  BUILD_CONST_KEY_MAP_3     3 
              376  STORE_FAST               'f'

 L. 104       378  LOAD_FAST                'video'
              380  LOAD_METHOD              get
              382  LOAD_STR                 'video_format'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  STORE_FAST               'video_format'

 L. 105       388  LOAD_FAST                'video_format'
              390  LOAD_STR                 'hls'
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_TRUE    418  'to 418'
              398  LOAD_STR                 '/hls/'
              400  LOAD_FAST                'media_url'
              402  COMPARE_OP               in
          404_406  POP_JUMP_IF_TRUE    418  'to 418'
              408  LOAD_STR                 '/chunklist.m3u8'
              410  LOAD_FAST                'media_url'
              412  COMPARE_OP               in
          414_416  JUMP_IF_FALSE_OR_POP   424  'to 424'
            418_0  COME_FROM           404  '404'
            418_1  COME_FROM           394  '394'
              418  LOAD_FAST                'playlist'
              420  LOAD_CONST               False
              422  COMPARE_OP               is
            424_0  COME_FROM           414  '414'
              424  STORE_FAST               'is_hls'

 L. 106       426  LOAD_FAST                'is_hls'
          428_430  POP_JUMP_IF_FALSE   446  'to 446'

 L. 107       432  LOAD_STR                 'hls'
              434  STORE_FAST               'format_id'

 L. 108       436  LOAD_STR                 'm3u8_native'
              438  LOAD_FAST                'f'
              440  LOAD_STR                 'protocol'
              442  STORE_SUBSCR     
              444  JUMP_FORWARD        462  'to 462'
            446_0  COME_FROM           428  '428'

 L. 109       446  LOAD_FAST                'video_format'
              448  LOAD_STR                 'mp4'
              450  COMPARE_OP               ==
              452  POP_JUMP_IF_FALSE   230  'to 230'

 L. 110       454  LOAD_STR                 'http'
              456  STORE_FAST               'format_id'
              458  JUMP_FORWARD        462  'to 462'

 L. 112       460  CONTINUE            230  'to 230'
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           444  '444'

 L. 113       462  LOAD_FAST                'quality'
          464_466  POP_JUMP_IF_FALSE   480  'to 480'

 L. 114       468  LOAD_FAST                'format_id'
              470  LOAD_STR                 '-%sp'
              472  LOAD_FAST                'quality'
              474  BINARY_MODULO    
              476  INPLACE_ADD      
              478  STORE_FAST               'format_id'
            480_0  COME_FROM           464  '464'

 L. 115       480  LOAD_FAST                'format_id'
              482  LOAD_FAST                'f'
              484  LOAD_STR                 'format_id'
              486  STORE_SUBSCR     

 L. 116       488  LOAD_FAST                'formats'
              490  LOAD_METHOD              append
              492  LOAD_FAST                'f'
              494  CALL_METHOD_1         1  '1 positional argument'
              496  POP_TOP          
              498  JUMP_BACK           230  'to 230'
              500  POP_BLOCK        
            502_0  COME_FROM_LOOP      214  '214'

 L. 117       502  LOAD_FAST                'self'
              504  LOAD_METHOD              _sort_formats
              506  LOAD_FAST                'formats'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          

 L. 119       512  LOAD_GLOBAL              try_get

 L. 120       514  LOAD_FAST                'show'
              516  LOAD_LAMBDA              '<code_object <lambda>>'
              518  LOAD_STR                 'PuhuTVIE._real_extract.<locals>.<lambda>'
              520  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              522  LOAD_GLOBAL              compat_str
              524  CALL_FUNCTION_3       3  '3 positional arguments'
              526  STORE_FAST               'creator'

 L. 122       528  LOAD_FAST                'info'
              530  LOAD_METHOD              get
              532  LOAD_STR                 'content'
              534  CALL_METHOD_1         1  '1 positional argument'
          536_538  JUMP_IF_TRUE_OR_POP   542  'to 542'
              540  BUILD_MAP_0           0 
            542_0  COME_FROM           536  '536'
              542  STORE_FAST               'content'

 L. 124       544  LOAD_GLOBAL              try_get

 L. 125       546  LOAD_FAST                'content'
              548  LOAD_LAMBDA              '<code_object <lambda>>'
              550  LOAD_STR                 'PuhuTVIE._real_extract.<locals>.<lambda>'
              552  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              554  LOAD_GLOBAL              dict
              556  CALL_FUNCTION_3       3  '3 positional arguments'
          558_560  JUMP_IF_TRUE_OR_POP   564  'to 564'
              562  BUILD_MAP_0           0 
            564_0  COME_FROM           558  '558'
              564  STORE_FAST               'images'

 L. 126       566  BUILD_LIST_0          0 
              568  STORE_FAST               'thumbnails'

 L. 127       570  SETUP_LOOP          664  'to 664'
              572  LOAD_FAST                'images'
              574  LOAD_METHOD              items
              576  CALL_METHOD_0         0  '0 positional arguments'
              578  GET_ITER         
              580  FOR_ITER            662  'to 662'
              582  UNPACK_SEQUENCE_2     2 
              584  STORE_FAST               'image_id'
              586  STORE_FAST               'image_url'

 L. 128       588  LOAD_GLOBAL              isinstance
              590  LOAD_FAST                'image_url'
              592  LOAD_GLOBAL              compat_str
              594  CALL_FUNCTION_2       2  '2 positional arguments'
          596_598  POP_JUMP_IF_TRUE    604  'to 604'

 L. 129   600_602  CONTINUE            580  'to 580'
            604_0  COME_FROM           596  '596'

 L. 130       604  LOAD_FAST                'image_url'
              606  LOAD_METHOD              startswith
              608  LOAD_CONST               ('http', '//')
              610  CALL_METHOD_1         1  '1 positional argument'
          612_614  POP_JUMP_IF_TRUE    624  'to 624'

 L. 131       616  LOAD_STR                 'https://%s'
              618  LOAD_FAST                'image_url'
              620  BINARY_MODULO    
              622  STORE_FAST               'image_url'
            624_0  COME_FROM           612  '612'

 L. 132       624  LOAD_GLOBAL              parse_resolution
              626  LOAD_FAST                'image_id'
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  STORE_FAST               't'

 L. 133       632  LOAD_FAST                't'
              634  LOAD_METHOD              update

 L. 134       636  LOAD_FAST                'image_id'

 L. 135       638  LOAD_FAST                'image_url'
              640  LOAD_CONST               ('id', 'url')
              642  BUILD_CONST_KEY_MAP_2     2 
              644  CALL_METHOD_1         1  '1 positional argument'
              646  POP_TOP          

 L. 137       648  LOAD_FAST                'thumbnails'
              650  LOAD_METHOD              append
              652  LOAD_FAST                't'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          
          658_660  JUMP_BACK           580  'to 580'
              662  POP_BLOCK        
            664_0  COME_FROM_LOOP      570  '570'

 L. 139       664  BUILD_LIST_0          0 
              666  STORE_FAST               'tags'

 L. 140       668  SETUP_LOOP          750  'to 750'
              670  LOAD_FAST                'show'
              672  LOAD_METHOD              get
              674  LOAD_STR                 'genres'
              676  CALL_METHOD_1         1  '1 positional argument'
          678_680  JUMP_IF_TRUE_OR_POP   684  'to 684'
              682  BUILD_LIST_0          0 
            684_0  COME_FROM           678  '678'
              684  GET_ITER         
            686_0  COME_FROM           730  '730'
            686_1  COME_FROM           718  '718'
              686  FOR_ITER            748  'to 748'
              688  STORE_FAST               'genre'

 L. 141       690  LOAD_GLOBAL              isinstance
              692  LOAD_FAST                'genre'
              694  LOAD_GLOBAL              dict
              696  CALL_FUNCTION_2       2  '2 positional arguments'
          698_700  POP_JUMP_IF_TRUE    706  'to 706'

 L. 142   702_704  CONTINUE            686  'to 686'
            706_0  COME_FROM           698  '698'

 L. 143       706  LOAD_FAST                'genre'
              708  LOAD_METHOD              get
              710  LOAD_STR                 'name'
              712  CALL_METHOD_1         1  '1 positional argument'
              714  STORE_FAST               'genre_name'

 L. 144       716  LOAD_FAST                'genre_name'
          718_720  POP_JUMP_IF_FALSE   686  'to 686'
              722  LOAD_GLOBAL              isinstance
              724  LOAD_FAST                'genre_name'
              726  LOAD_GLOBAL              compat_str
              728  CALL_FUNCTION_2       2  '2 positional arguments'
          730_732  POP_JUMP_IF_FALSE   686  'to 686'

 L. 145       734  LOAD_FAST                'tags'
              736  LOAD_METHOD              append
              738  LOAD_FAST                'genre_name'
              740  CALL_METHOD_1         1  '1 positional argument'
              742  POP_TOP          
          744_746  JUMP_BACK           686  'to 686'
              748  POP_BLOCK        
            750_0  COME_FROM_LOOP      668  '668'

 L. 147       750  BUILD_MAP_0           0 
              752  STORE_FAST               'subtitles'

 L. 148       754  SETUP_LOOP          886  'to 886'
              756  LOAD_FAST                'content'
              758  LOAD_METHOD              get
              760  LOAD_STR                 'subtitles'
              762  CALL_METHOD_1         1  '1 positional argument'
          764_766  JUMP_IF_TRUE_OR_POP   770  'to 770'
              768  BUILD_LIST_0          0 
            770_0  COME_FROM           764  '764'
              770  GET_ITER         
            772_0  COME_FROM           842  '842'
            772_1  COME_FROM           830  '830'
              772  FOR_ITER            884  'to 884'
              774  STORE_FAST               'subtitle'

 L. 149       776  LOAD_GLOBAL              isinstance
              778  LOAD_FAST                'subtitle'
              780  LOAD_GLOBAL              dict
              782  CALL_FUNCTION_2       2  '2 positional arguments'
          784_786  POP_JUMP_IF_TRUE    792  'to 792'

 L. 150   788_790  CONTINUE            772  'to 772'
            792_0  COME_FROM           784  '784'

 L. 151       792  LOAD_FAST                'subtitle'
              794  LOAD_METHOD              get
              796  LOAD_STR                 'language'
              798  CALL_METHOD_1         1  '1 positional argument'
              800  STORE_FAST               'lang'

 L. 152       802  LOAD_GLOBAL              url_or_none
              804  LOAD_FAST                'subtitle'
              806  LOAD_METHOD              get
              808  LOAD_STR                 'url'
              810  CALL_METHOD_1         1  '1 positional argument'
          812_814  JUMP_IF_TRUE_OR_POP   824  'to 824'
              816  LOAD_FAST                'subtitle'
              818  LOAD_METHOD              get
              820  LOAD_STR                 'file'
              822  CALL_METHOD_1         1  '1 positional argument'
            824_0  COME_FROM           812  '812'
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  STORE_FAST               'sub_url'

 L. 153       828  LOAD_FAST                'lang'
          830_832  POP_JUMP_IF_FALSE   772  'to 772'
              834  LOAD_GLOBAL              isinstance
              836  LOAD_FAST                'lang'
              838  LOAD_GLOBAL              compat_str
              840  CALL_FUNCTION_2       2  '2 positional arguments'
          842_844  POP_JUMP_IF_FALSE   772  'to 772'
              846  LOAD_FAST                'sub_url'
          848_850  POP_JUMP_IF_TRUE    856  'to 856'

 L. 154   852_854  CONTINUE            772  'to 772'
            856_0  COME_FROM           848  '848'

 L. 156       856  LOAD_STR                 'url'
              858  LOAD_FAST                'sub_url'
              860  BUILD_MAP_1           1 
              862  BUILD_LIST_1          1 
              864  LOAD_FAST                'subtitles'
              866  LOAD_FAST                'self'
              868  LOAD_ATTR                _SUBTITLE_LANGS
              870  LOAD_METHOD              get
              872  LOAD_FAST                'lang'
              874  LOAD_FAST                'lang'
              876  CALL_METHOD_2         2  '2 positional arguments'
              878  STORE_SUBSCR     
          880_882  JUMP_BACK           772  'to 772'
              884  POP_BLOCK        
            886_0  COME_FROM_LOOP      754  '754'

 L. 160       886  LOAD_FAST                'video_id'

 L. 161       888  LOAD_FAST                'display_id'

 L. 162       890  LOAD_FAST                'title'

 L. 163       892  LOAD_FAST                'info'
              894  LOAD_METHOD              get
              896  LOAD_STR                 'description'
              898  CALL_METHOD_1         1  '1 positional argument'
          900_902  JUMP_IF_TRUE_OR_POP   912  'to 912'
              904  LOAD_FAST                'show'
              906  LOAD_METHOD              get
              908  LOAD_STR                 'description'
              910  CALL_METHOD_1         1  '1 positional argument'
            912_0  COME_FROM           900  '900'

 L. 164       912  LOAD_GLOBAL              str_or_none
              914  LOAD_FAST                'info'
              916  LOAD_METHOD              get
              918  LOAD_STR                 'season_id'
              920  CALL_METHOD_1         1  '1 positional argument'
              922  CALL_FUNCTION_1       1  '1 positional argument'

 L. 165       924  LOAD_GLOBAL              int_or_none
              926  LOAD_FAST                'info'
              928  LOAD_METHOD              get
              930  LOAD_STR                 'season_number'
              932  CALL_METHOD_1         1  '1 positional argument'
              934  CALL_FUNCTION_1       1  '1 positional argument'

 L. 166       936  LOAD_GLOBAL              int_or_none
              938  LOAD_FAST                'info'
              940  LOAD_METHOD              get
              942  LOAD_STR                 'episode_number'
              944  CALL_METHOD_1         1  '1 positional argument'
              946  CALL_FUNCTION_1       1  '1 positional argument'

 L. 167       948  LOAD_GLOBAL              int_or_none
              950  LOAD_FAST                'show'
              952  LOAD_METHOD              get
              954  LOAD_STR                 'released_at'
              956  CALL_METHOD_1         1  '1 positional argument'
              958  CALL_FUNCTION_1       1  '1 positional argument'

 L. 168       960  LOAD_GLOBAL              unified_timestamp
              962  LOAD_FAST                'info'
              964  LOAD_METHOD              get
              966  LOAD_STR                 'created_at'
              968  CALL_METHOD_1         1  '1 positional argument'
              970  CALL_FUNCTION_1       1  '1 positional argument'

 L. 169       972  LOAD_FAST                'creator'

 L. 170       974  LOAD_GLOBAL              int_or_none
              976  LOAD_FAST                'content'
              978  LOAD_METHOD              get
              980  LOAD_STR                 'watch_count'
              982  CALL_METHOD_1         1  '1 positional argument'
              984  CALL_FUNCTION_1       1  '1 positional argument'

 L. 171       986  LOAD_GLOBAL              float_or_none
              988  LOAD_FAST                'content'
              990  LOAD_METHOD              get
              992  LOAD_STR                 'duration_in_ms'
              994  CALL_METHOD_1         1  '1 positional argument'
              996  LOAD_CONST               1000
              998  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 172      1000  LOAD_FAST                'tags'

 L. 173      1002  LOAD_FAST                'subtitles'

 L. 174      1004  LOAD_FAST                'thumbnails'

 L. 175      1006  LOAD_FAST                'formats'
             1008  LOAD_CONST               ('id', 'display_id', 'title', 'description', 'season_id', 'season_number', 'episode_number', 'release_year', 'timestamp', 'creator', 'view_count', 'duration', 'tags', 'subtitles', 'thumbnails', 'formats')
             1010  BUILD_CONST_KEY_MAP_16    16 
             1012  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 424


class PuhuTVSerieIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?puhutv\\.com/(?P<id>[^/?#&]+)-detay'
    IE_NAME = 'puhutv:serie'
    _TESTS = [
     {'url':'https://puhutv.com/deniz-yildizi-detay', 
      'info_dict':{'title':'Deniz Yıldızı', 
       'id':'deniz-yildizi'}, 
      'playlist_mincount':205},
     {'url':'https://puhutv.com/kaybedenler-kulubu-detay', 
      'only_matching':True}]

    def _extract_entries(self, seasons):
        for season in seasons:
            season_id = season.get'id'
            if not season_id:
                continue
            page = 1
            has_more = True
            while has_more is True:
                season = self._download_json(('https://galadriel.puhutv.com/seasons/%s' % season_id),
                  season_id,
                  ('Downloading page %s' % page), query={'page':page, 
                 'per':40})
                episodes = season.get'episodes'
                if isinstanceepisodeslist:
                    for ep in episodes:
                        slug_path = str_or_none(ep.get'slugPath')
                        if not slug_path:
                            continue
                        video_id = str_or_none(int_or_none(ep.get'id'))
                        yield self.url_result(('https://puhutv.com/%s' % slug_path),
                          ie=(PuhuTVIE.ie_key),
                          video_id=video_id,
                          video_title=(ep.get'name' or ep.get'eventLabel'))

                page += 1
                has_more = season.get'hasMore'

    def _real_extract(self, url):
        playlist_id = self._match_idurl
        info = self._download_jsonurljoinurl('/api/slug/%s-detay' % playlist_id)playlist_id['data']
        seasons = info.get'seasons'
        if seasons:
            return self.playlist_result(self._extract_entriesseasons, playlist_id, info.get'name')
        video_id = info.get'slug' or info['assets'][0]['slug']
        return self.url_result('https://puhutv.com/%s-izle' % video_id, PuhuTVIE.ie_key, video_id)