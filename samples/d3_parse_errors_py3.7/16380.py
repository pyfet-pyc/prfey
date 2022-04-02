# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\picarto.py
from __future__ import unicode_literals
import re, time
from .common import InfoExtractor
from ..compat import compat_str
from ..utils import ExtractorError, js_to_json, try_get, update_url_query, urlencode_postdata

class PicartoIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/(?P<id>[a-zA-Z0-9]+)(?:/(?P<token>[a-zA-Z0-9]+))?'
    _TEST = {'url':'https://picarto.tv/Setz', 
     'info_dict':{'id':'Setz', 
      'ext':'mp4', 
      'title':'re:^Setz [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}$', 
      'timestamp':int, 
      'is_live':True}, 
     'skip':'Stream is offline'}

    @classmethod
    def suitable(cls, url):
        if PicartoVodIE.suitable(url):
            return False
        return super(PicartoIE, cls).suitable(url)

    def _real_extract--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              match
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _VALID_URL
                8  LOAD_FAST                'url'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  STORE_FAST               'mobj'

 L.  38        14  LOAD_FAST                'mobj'
               16  LOAD_METHOD              group
               18  LOAD_STR                 'id'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  STORE_FAST               'channel_id'

 L.  40        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _download_json

 L.  41        28  LOAD_STR                 'https://api.picarto.tv/v1/channel/name/'
               30  LOAD_FAST                'channel_id'
               32  BINARY_ADD       

 L.  42        34  LOAD_FAST                'channel_id'
               36  CALL_METHOD_2         2  '2 positional arguments'
               38  STORE_FAST               'metadata'

 L.  44        40  LOAD_FAST                'metadata'
               42  LOAD_METHOD              get
               44  LOAD_STR                 'online'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  LOAD_CONST               False
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    66  'to 66'

 L.  45        54  LOAD_GLOBAL              ExtractorError
               56  LOAD_STR                 'Stream is offline'
               58  LOAD_CONST               True
               60  LOAD_CONST               ('expected',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            52  '52'

 L.  47        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _download_json

 L.  48        70  LOAD_STR                 'https://picarto.tv/process/channel'
               72  LOAD_FAST                'channel_id'

 L.  49        74  LOAD_GLOBAL              urlencode_postdata
               76  LOAD_STR                 'loadbalancinginfo'
               78  LOAD_FAST                'channel_id'
               80  BUILD_MAP_1           1 
               82  CALL_FUNCTION_1       1  '1 positional argument'

 L.  50        84  LOAD_STR                 'Downloading load balancing info'
               86  LOAD_CONST               ('data', 'note')
               88  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               90  STORE_FAST               'cdn_data'

 L.  52        92  LOAD_FAST                'mobj'
               94  LOAD_METHOD              group
               96  LOAD_STR                 'token'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  JUMP_IF_TRUE_OR_POP   104  'to 104'
              102  LOAD_STR                 'public'
            104_0  COME_FROM           100  '100'
              104  STORE_FAST               'token'

 L.  54       106  LOAD_GLOBAL              int
              108  LOAD_GLOBAL              time
              110  LOAD_METHOD              time
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  LOAD_CONST               1000
              116  BINARY_MULTIPLY  
              118  CALL_FUNCTION_1       1  '1 positional argument'

 L.  55       120  LOAD_FAST                'token'
              122  LOAD_CONST               ('con', 'token')
              124  BUILD_CONST_KEY_MAP_2     2 
              126  STORE_FAST               'params'

 L.  58       128  LOAD_FAST                'cdn_data'
              130  LOAD_METHOD              get
              132  LOAD_STR                 'preferedEdge'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  STORE_FAST               'prefered_edge'

 L.  59       138  BUILD_LIST_0          0 
              140  STORE_FAST               'formats'

 L.  61   142_144  SETUP_LOOP          430  'to 430'
              146  LOAD_FAST                'cdn_data'
              148  LOAD_STR                 'edges'
              150  BINARY_SUBSCR    
              152  GET_ITER         
            154_0  COME_FROM           426  '426'
            154_1  COME_FROM           184  '184'
            154_2  COME_FROM           172  '172'
          154_156  FOR_ITER            428  'to 428'
              158  STORE_FAST               'edge'

 L.  62       160  LOAD_FAST                'edge'
              162  LOAD_METHOD              get
              164  LOAD_STR                 'ep'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  STORE_FAST               'edge_ep'

 L.  63       170  LOAD_FAST                'edge_ep'
              172  POP_JUMP_IF_FALSE_BACK   154  'to 154'
              174  LOAD_GLOBAL              isinstance
              176  LOAD_FAST                'edge_ep'
              178  LOAD_GLOBAL              compat_str
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  POP_JUMP_IF_TRUE    186  'to 186'

 L.  64       184  CONTINUE            154  'to 154'
            186_0  COME_FROM           182  '182'

 L.  65       186  LOAD_FAST                'edge'
              188  LOAD_METHOD              get
              190  LOAD_STR                 'id'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  STORE_FAST               'edge_id'

 L.  66       196  SETUP_LOOP          426  'to 426'
              198  LOAD_FAST                'cdn_data'
              200  LOAD_STR                 'techs'
              202  BINARY_SUBSCR    
              204  GET_ITER         
            206_0  COME_FROM           422  '422'
            206_1  COME_FROM           420  '420'
            206_2  COME_FROM           418  '418'
            206_3  COME_FROM           368  '368'
            206_4  COME_FROM           350  '350'
            206_5  COME_FROM           348  '348'
              206  FOR_ITER            424  'to 424'
              208  STORE_FAST               'tech'

 L.  67       210  LOAD_FAST                'tech'
              212  LOAD_METHOD              get
              214  LOAD_STR                 'label'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'tech_label'

 L.  68       220  LOAD_FAST                'tech'
              222  LOAD_METHOD              get
              224  LOAD_STR                 'type'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               'tech_type'

 L.  69       230  LOAD_CONST               0
              232  STORE_FAST               'preference'

 L.  70       234  LOAD_FAST                'edge_id'
              236  LOAD_FAST                'prefered_edge'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   250  'to 250'

 L.  71       242  LOAD_FAST                'preference'
              244  LOAD_CONST               1
              246  INPLACE_ADD      
              248  STORE_FAST               'preference'
            250_0  COME_FROM           240  '240'

 L.  72       250  BUILD_LIST_0          0 
              252  STORE_FAST               'format_id'

 L.  73       254  LOAD_FAST                'edge_id'
          256_258  POP_JUMP_IF_FALSE   270  'to 270'

 L.  74       260  LOAD_FAST                'format_id'
              262  LOAD_METHOD              append
              264  LOAD_FAST                'edge_id'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  POP_TOP          
            270_0  COME_FROM           256  '256'

 L.  75       270  LOAD_FAST                'tech_type'
              272  LOAD_STR                 'application/x-mpegurl'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_TRUE    290  'to 290'
              280  LOAD_FAST                'tech_label'
              282  LOAD_STR                 'HLS'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   352  'to 352'
            290_0  COME_FROM           276  '276'

 L.  76       290  LOAD_FAST                'format_id'
              292  LOAD_METHOD              append
              294  LOAD_STR                 'hls'
              296  CALL_METHOD_1         1  '1 positional argument'
              298  POP_TOP          

 L.  77       300  LOAD_FAST                'formats'
              302  LOAD_METHOD              extend
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _extract_m3u8_formats

 L.  78       308  LOAD_GLOBAL              update_url_query

 L.  79       310  LOAD_STR                 'https://%s/hls/%s/index.m3u8'

 L.  80       312  LOAD_FAST                'edge_ep'
              314  LOAD_FAST                'channel_id'
              316  BUILD_TUPLE_2         2 
              318  BINARY_MODULO    
              320  LOAD_FAST                'params'
              322  CALL_FUNCTION_2       2  '2 positional arguments'

 L.  81       324  LOAD_FAST                'channel_id'
              326  LOAD_STR                 'mp4'
              328  LOAD_FAST                'preference'

 L.  82       330  LOAD_STR                 '-'
              332  LOAD_METHOD              join
              334  LOAD_FAST                'format_id'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  LOAD_CONST               False
              340  LOAD_CONST               ('preference', 'm3u8_id', 'fatal')
              342  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  POP_TOP          

 L.  83       348  CONTINUE            206  'to 206'
              350  JUMP_BACK           206  'to 206'
            352_0  COME_FROM           286  '286'

 L.  84       352  LOAD_FAST                'tech_type'
              354  LOAD_STR                 'video/mp4'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_TRUE    370  'to 370'
              362  LOAD_FAST                'tech_label'
              364  LOAD_STR                 'MP4'
              366  COMPARE_OP               ==
              368  POP_JUMP_IF_FALSE_BACK   206  'to 206'
            370_0  COME_FROM           358  '358'

 L.  85       370  LOAD_FAST                'format_id'
              372  LOAD_METHOD              append
              374  LOAD_STR                 'mp4'
              376  CALL_METHOD_1         1  '1 positional argument'
              378  POP_TOP          

 L.  86       380  LOAD_FAST                'formats'
              382  LOAD_METHOD              append

 L.  87       384  LOAD_GLOBAL              update_url_query

 L.  88       386  LOAD_STR                 'https://%s/mp4/%s.mp4'
              388  LOAD_FAST                'edge_ep'
              390  LOAD_FAST                'channel_id'
              392  BUILD_TUPLE_2         2 
              394  BINARY_MODULO    

 L.  89       396  LOAD_FAST                'params'
              398  CALL_FUNCTION_2       2  '2 positional arguments'

 L.  90       400  LOAD_STR                 '-'
              402  LOAD_METHOD              join
              404  LOAD_FAST                'format_id'
              406  CALL_METHOD_1         1  '1 positional argument'

 L.  91       408  LOAD_FAST                'preference'
              410  LOAD_CONST               ('url', 'format_id', 'preference')
              412  BUILD_CONST_KEY_MAP_3     3 
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          
              418  JUMP_BACK           206  'to 206'

 L.  95       420  CONTINUE            206  'to 206'
              422  JUMP_BACK           206  'to 206'
              424  POP_BLOCK        
            426_0  COME_FROM_LOOP      196  '196'
              426  JUMP_BACK           154  'to 154'
              428  POP_BLOCK        
            430_0  COME_FROM_LOOP      142  '142'

 L.  96       430  LOAD_FAST                'self'
              432  LOAD_METHOD              _sort_formats
              434  LOAD_FAST                'formats'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  POP_TOP          

 L.  98       440  LOAD_FAST                'metadata'
              442  LOAD_METHOD              get
              444  LOAD_STR                 'adult'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  STORE_FAST               'mature'

 L.  99       450  LOAD_FAST                'mature'
              452  LOAD_CONST               None
              454  COMPARE_OP               is
          456_458  POP_JUMP_IF_FALSE   466  'to 466'

 L. 100       460  LOAD_CONST               None
              462  STORE_FAST               'age_limit'
              464  JUMP_FORWARD        484  'to 484'
            466_0  COME_FROM           456  '456'

 L. 102       466  LOAD_FAST                'mature'
              468  LOAD_CONST               True
              470  COMPARE_OP               is
          472_474  POP_JUMP_IF_FALSE   480  'to 480'
              476  LOAD_CONST               18
              478  JUMP_FORWARD        482  'to 482'
            480_0  COME_FROM           472  '472'
              480  LOAD_CONST               0
            482_0  COME_FROM           478  '478'
              482  STORE_FAST               'age_limit'
            484_0  COME_FROM           464  '464'

 L. 105       484  LOAD_FAST                'channel_id'

 L. 106       486  LOAD_FAST                'self'
              488  LOAD_METHOD              _live_title
              490  LOAD_FAST                'metadata'
              492  LOAD_METHOD              get
              494  LOAD_STR                 'title'
              496  CALL_METHOD_1         1  '1 positional argument'
          498_500  JUMP_IF_TRUE_OR_POP   504  'to 504'
              502  LOAD_FAST                'channel_id'
            504_0  COME_FROM           498  '498'
              504  CALL_METHOD_1         1  '1 positional argument'

 L. 107       506  LOAD_CONST               True

 L. 108       508  LOAD_GLOBAL              try_get
              510  LOAD_FAST                'metadata'
              512  LOAD_LAMBDA              '<code_object <lambda>>'
              514  LOAD_STR                 'PicartoIE._real_extract.<locals>.<lambda>'
              516  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              518  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 109       520  LOAD_FAST                'channel_id'

 L. 110       522  LOAD_STR                 'https://picarto.tv/%s'
              524  LOAD_FAST                'channel_id'
              526  BINARY_MODULO    

 L. 111       528  LOAD_FAST                'age_limit'

 L. 112       530  LOAD_FAST                'formats'
              532  LOAD_CONST               ('id', 'title', 'is_live', 'thumbnail', 'channel', 'channel_url', 'age_limit', 'formats')
              534  BUILD_CONST_KEY_MAP_8     8 
              536  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 420


class PicartoVodIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www.)?picarto\\.tv/videopopout/(?P<id>[^/?#&]+)'
    _TESTS = [
     {'url':'https://picarto.tv/videopopout/ArtofZod_2017.12.12.00.13.23.flv', 
      'md5':'3ab45ba4352c52ee841a28fb73f2d9ca', 
      'info_dict':{'id':'ArtofZod_2017.12.12.00.13.23.flv', 
       'ext':'mp4', 
       'title':'ArtofZod_2017.12.12.00.13.23.flv', 
       'thumbnail':'re:^https?://.*\\.jpg'}},
     {'url':'https://picarto.tv/videopopout/Plague', 
      'only_matching':True}]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpageurlvideo_id
        vod_info = self._parse_json((self._search_regex('(?s)#vod-player["\\\']\\s*,\\s*(\\{.+?\\})\\s*\\)', webpage, video_id)),
          video_id,
          transform_source=js_to_json)
        formats = self._extract_m3u8_formats((vod_info['vod']),
          video_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls')
        self._sort_formats(formats)
        return {'id':video_id, 
         'title':video_id, 
         'thumbnail':vod_info.get('vodThumb'), 
         'formats':formats}