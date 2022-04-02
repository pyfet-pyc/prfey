# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\srgssr.py
from __future__ import unicode_literals
import re
from .common import InfoExtractor
from ..compat import compat_urllib_parse_urlparse
from ..utils import ExtractorError, parse_iso8601, qualities

class SRGSSRIE(InfoExtractor):
    _VALID_URL = '(?:https?://tp\\.srgssr\\.ch/p(?:/[^/]+)+\\?urn=urn|srgssr):(?P<bu>srf|rts|rsi|rtr|swi):(?:[^:]+:)?(?P<type>video|audio):(?P<id>[0-9a-f\\-]{36}|\\d+)'
    _GEO_BYPASS = False
    _GEO_COUNTRIES = ['CH']
    _ERRORS = {'AGERATING12':'To protect children under the age of 12, this video is only available between 8 p.m. and 6 a.m.', 
     'AGERATING18':'To protect children under the age of 18, this video is only available between 11 p.m. and 5 a.m.', 
     'GEOBLOCK':'For legal reasons, this video is only available in Switzerland.', 
     'LEGAL':'The video cannot be transmitted for legal reasons.', 
     'STARTDATE':'This video is not yet available. Please try again later.'}

    def _get_tokenized_src(self, url, video_id, format_id):
        sp = compat_urllib_parse_urlparse(url).path.split('/')
        token = self._download_json(('http://tp.srgssr.ch/akahd/token?acl=/%s/%s/*' % (sp[1], sp[2])),
          video_id,
          ('Downloading %s token' % format_id), fatal=False) or {}
        auth_params = token.get('token', {}).get('authparams')
        if auth_params:
            url += '?' + auth_params
        return url

    def get_media_data(self, bu, media_type, media_id):
        media_data = self._download_json('http://il.srgssr.ch/integrationlayer/1.0/ue/%s/%s/play/%s.json' % (bu, media_type, media_id), media_id)[media_type.capitalize()]
        if media_data.get('block'):
            if media_data['block'] in self._ERRORS:
                message = self._ERRORS[media_data['block']]
                if media_data['block'] == 'GEOBLOCK':
                    self.raise_geo_restricted(msg=message,
                      countries=(self._GEO_COUNTRIES))
                raise ExtractorError(('%s said: %s' % (self.IE_NAME, message)),
                  expected=True)
        return media_data

    def _real_extract--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              match
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _VALID_URL
                8  LOAD_FAST                'url'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  LOAD_METHOD              groups
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'bu'
               20  STORE_FAST               'media_type'
               22  STORE_FAST               'media_id'

 L.  57        24  LOAD_FAST                'self'
               26  LOAD_METHOD              get_media_data
               28  LOAD_FAST                'bu'
               30  LOAD_FAST                'media_type'
               32  LOAD_FAST                'media_id'
               34  CALL_METHOD_3         3  '3 positional arguments'
               36  STORE_FAST               'media_data'

 L.  59        38  LOAD_FAST                'media_data'
               40  LOAD_STR                 'AssetMetadatas'
               42  BINARY_SUBSCR    
               44  LOAD_STR                 'AssetMetadata'
               46  BINARY_SUBSCR    
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  STORE_FAST               'metadata'

 L.  60        54  LOAD_FAST                'metadata'
               56  LOAD_STR                 'title'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'title'

 L.  61        62  LOAD_FAST                'metadata'
               64  LOAD_METHOD              get
               66  LOAD_STR                 'description'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  STORE_FAST               'description'

 L.  62        72  LOAD_FAST                'media_data'
               74  LOAD_METHOD              get
               76  LOAD_STR                 'createdDate'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  JUMP_IF_TRUE_OR_POP    90  'to 90'
               82  LOAD_FAST                'metadata'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'createdDate'
               88  CALL_METHOD_1         1  '1 positional argument'
             90_0  COME_FROM            80  '80'
               90  STORE_FAST               'created_date'

 L.  63        92  LOAD_GLOBAL              parse_iso8601
               94  LOAD_FAST                'created_date'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'timestamp'

 L.  65       100  LOAD_LISTCOMP            '<code_object <listcomp>>'
              102  LOAD_STR                 'SRGSSRIE._real_extract.<locals>.<listcomp>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  68       106  LOAD_FAST                'media_data'
              108  LOAD_METHOD              get
              110  LOAD_STR                 'Image'
              112  BUILD_MAP_0           0 
              114  CALL_METHOD_2         2  '2 positional arguments'
              116  LOAD_METHOD              get
              118  LOAD_STR                 'ImageRepresentations'
              120  BUILD_MAP_0           0 
              122  CALL_METHOD_2         2  '2 positional arguments'
              124  LOAD_METHOD              get
              126  LOAD_STR                 'ImageRepresentation'
              128  BUILD_LIST_0          0 
              130  CALL_METHOD_2         2  '2 positional arguments'
              132  GET_ITER         
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  STORE_FAST               'thumbnails'

 L.  70       138  LOAD_GLOBAL              qualities
              140  LOAD_STR                 'LQ'
              142  LOAD_STR                 'MQ'
              144  LOAD_STR                 'SD'
              146  LOAD_STR                 'HQ'
              148  LOAD_STR                 'HD'
              150  BUILD_LIST_5          5 
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  STORE_FAST               'preference'

 L.  71       156  BUILD_LIST_0          0 
              158  STORE_FAST               'formats'

 L.  72   160_162  SETUP_LOOP          446  'to 446'
              164  LOAD_FAST                'media_data'
              166  LOAD_METHOD              get
              168  LOAD_STR                 'Playlists'
              170  BUILD_MAP_0           0 
              172  CALL_METHOD_2         2  '2 positional arguments'
              174  LOAD_METHOD              get
              176  LOAD_STR                 'Playlist'
              178  BUILD_LIST_0          0 
              180  CALL_METHOD_2         2  '2 positional arguments'
              182  LOAD_FAST                'media_data'
              184  LOAD_METHOD              get
              186  LOAD_STR                 'Downloads'
              188  BUILD_MAP_0           0 
              190  CALL_METHOD_2         2  '2 positional arguments'
              192  LOAD_METHOD              get
              194  LOAD_STR                 'Download'
              196  BUILD_LIST_0          0 
              198  CALL_METHOD_2         2  '2 positional arguments'
              200  BINARY_ADD       
              202  GET_ITER         
              204  FOR_ITER            444  'to 444'
              206  STORE_FAST               'source'

 L.  73       208  LOAD_FAST                'source'
              210  LOAD_METHOD              get
              212  LOAD_STR                 '@protocol'
              214  CALL_METHOD_1         1  '1 positional argument'
              216  STORE_FAST               'protocol'

 L.  74       218  SETUP_LOOP          442  'to 442'
              220  LOAD_FAST                'source'
              222  LOAD_STR                 'url'
              224  BINARY_SUBSCR    
              226  GET_ITER         
              228  FOR_ITER            440  'to 440'
              230  STORE_FAST               'asset'

 L.  75       232  LOAD_FAST                'asset'
              234  LOAD_STR                 'text'
              236  BINARY_SUBSCR    
              238  STORE_FAST               'asset_url'

 L.  76       240  LOAD_FAST                'asset'
              242  LOAD_STR                 '@quality'
              244  BINARY_SUBSCR    
              246  STORE_FAST               'quality'

 L.  77       248  LOAD_STR                 '%s-%s'
              250  LOAD_FAST                'protocol'
              252  LOAD_FAST                'quality'
              254  BUILD_TUPLE_2         2 
              256  BINARY_MODULO    
              258  STORE_FAST               'format_id'

 L.  78       260  LOAD_FAST                'protocol'
              262  LOAD_METHOD              startswith
              264  LOAD_STR                 'HTTP-HDS'
              266  CALL_METHOD_1         1  '1 positional argument'
          268_270  POP_JUMP_IF_TRUE    284  'to 284'
              272  LOAD_FAST                'protocol'
              274  LOAD_METHOD              startswith
              276  LOAD_STR                 'HTTP-HLS'
              278  CALL_METHOD_1         1  '1 positional argument'
          280_282  POP_JUMP_IF_FALSE   400  'to 400'
            284_0  COME_FROM           268  '268'

 L.  79       284  LOAD_FAST                'self'
              286  LOAD_METHOD              _get_tokenized_src
              288  LOAD_FAST                'asset_url'
              290  LOAD_FAST                'media_id'
              292  LOAD_FAST                'format_id'
              294  CALL_METHOD_3         3  '3 positional arguments'
              296  STORE_FAST               'asset_url'

 L.  80       298  LOAD_FAST                'protocol'
              300  LOAD_METHOD              startswith
              302  LOAD_STR                 'HTTP-HDS'
              304  CALL_METHOD_1         1  '1 positional argument'
          306_308  POP_JUMP_IF_FALSE   358  'to 358'

 L.  81       310  LOAD_FAST                'formats'
              312  LOAD_METHOD              extend
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                _extract_f4m_formats

 L.  82       318  LOAD_FAST                'asset_url'
              320  LOAD_STR                 '?'
              322  LOAD_FAST                'asset_url'
              324  COMPARE_OP               not-in
          326_328  POP_JUMP_IF_FALSE   334  'to 334'
              330  LOAD_STR                 '?'
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           326  '326'
              334  LOAD_STR                 '&'
            336_0  COME_FROM           332  '332'
              336  BINARY_ADD       
              338  LOAD_STR                 'hdcore=3.4.0'
              340  BINARY_ADD       

 L.  83       342  LOAD_FAST                'media_id'
              344  LOAD_FAST                'format_id'
              346  LOAD_CONST               False
              348  LOAD_CONST               ('f4m_id', 'fatal')
              350  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          
              356  JUMP_FORWARD        398  'to 398'
            358_0  COME_FROM           306  '306'

 L.  84       358  LOAD_FAST                'protocol'
              360  LOAD_METHOD              startswith
              362  LOAD_STR                 'HTTP-HLS'
              364  CALL_METHOD_1         1  '1 positional argument'
          366_368  POP_JUMP_IF_FALSE   438  'to 438'

 L.  85       370  LOAD_FAST                'formats'
              372  LOAD_METHOD              extend
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                _extract_m3u8_formats

 L.  86       378  LOAD_FAST                'asset_url'
              380  LOAD_FAST                'media_id'
              382  LOAD_STR                 'mp4'
              384  LOAD_STR                 'm3u8_native'

 L.  87       386  LOAD_FAST                'format_id'
              388  LOAD_CONST               False
              390  LOAD_CONST               ('m3u8_id', 'fatal')
              392  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              394  CALL_METHOD_1         1  '1 positional argument'
              396  POP_TOP          
            398_0  COME_FROM           356  '356'
              398  JUMP_BACK           228  'to 228'
            400_0  COME_FROM           280  '280'

 L.  89       400  LOAD_FAST                'formats'
              402  LOAD_METHOD              append

 L.  90       404  LOAD_FAST                'format_id'

 L.  91       406  LOAD_FAST                'asset_url'

 L.  92       408  LOAD_FAST                'preference'
              410  LOAD_FAST                'quality'
              412  CALL_FUNCTION_1       1  '1 positional argument'

 L.  93       414  LOAD_FAST                'protocol'
              416  LOAD_STR                 'RTMP'
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   428  'to 428'
              424  LOAD_STR                 'flv'
              426  JUMP_FORWARD        430  'to 430'
            428_0  COME_FROM           420  '420'
              428  LOAD_CONST               None
            430_0  COME_FROM           426  '426'
              430  LOAD_CONST               ('format_id', 'url', 'preference', 'ext')
              432  BUILD_CONST_KEY_MAP_4     4 
              434  CALL_METHOD_1         1  '1 positional argument'
              436  POP_TOP          
            438_0  COME_FROM           366  '366'
              438  JUMP_BACK           228  'to 228'
              440  POP_BLOCK        
            442_0  COME_FROM_LOOP      218  '218'
              442  JUMP_BACK           204  'to 204'
              444  POP_BLOCK        
            446_0  COME_FROM_LOOP      160  '160'

 L.  95       446  LOAD_FAST                'self'
              448  LOAD_METHOD              _sort_formats
              450  LOAD_FAST                'formats'
              452  CALL_METHOD_1         1  '1 positional argument'
              454  POP_TOP          

 L.  98       456  LOAD_FAST                'media_id'

 L.  99       458  LOAD_FAST                'title'

 L. 100       460  LOAD_FAST                'description'

 L. 101       462  LOAD_FAST                'timestamp'

 L. 102       464  LOAD_FAST                'thumbnails'

 L. 103       466  LOAD_FAST                'formats'
              468  LOAD_CONST               ('id', 'title', 'description', 'timestamp', 'thumbnails', 'formats')
              470  BUILD_CONST_KEY_MAP_6     6 
              472  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 438_0


class SRGSSRPlayIE(InfoExtractor):
    IE_DESC = 'srf.ch, rts.ch, rsi.ch, rtr.ch and swissinfo.ch play sites'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:(?:www|play)\\.)?\n                        (?P<bu>srf|rts|rsi|rtr|swissinfo)\\.ch/play/(?:tv|radio)/\n                        (?:\n                            [^/]+/(?P<type>video|audio)/[^?]+|\n                            popup(?P<type_2>video|audio)player\n                        )\n                        \\?.*?\\b(?:id=|urn=urn:[^:]+:video:)(?P<id>[0-9a-f\\-]{36}|\\d+)\n                    '
    _TESTS = [
     {'url':'http://www.srf.ch/play/tv/10vor10/video/snowden-beantragt-asyl-in-russland?id=28e1a57d-5b76-4399-8ab3-9097f071e6c5', 
      'md5':'da6b5b3ac9fa4761a942331cef20fcb3', 
      'info_dict':{'id':'28e1a57d-5b76-4399-8ab3-9097f071e6c5', 
       'ext':'mp4', 
       'upload_date':'20130701', 
       'title':'Snowden beantragt Asyl in Russland', 
       'timestamp':1372713995}},
     {'url':'http://www.srf.ch/play/tv/top-gear/video/jaguar-xk120-shadow-und-tornado-dampflokomotive?id=677f5829-e473-4823-ac83-a1087fe97faa', 
      'md5':'0a274ce38fda48c53c01890651985bc6', 
      'info_dict':{'id':'677f5829-e473-4823-ac83-a1087fe97faa', 
       'ext':'flv', 
       'upload_date':'20130710', 
       'title':'Jaguar XK120, Shadow und Tornado-Dampflokomotive', 
       'description':'md5:88604432b60d5a38787f152dec89cd56', 
       'timestamp':1373493600}},
     {'url':'http://www.rtr.ch/play/radio/actualitad/audio/saira-tujetsch-tuttina-cuntinuar-cun-sedrun-muster-turissem?id=63cb0778-27f8-49af-9284-8c7a8c6d15fc', 
      'info_dict':{'id':'63cb0778-27f8-49af-9284-8c7a8c6d15fc', 
       'ext':'mp3', 
       'upload_date':'20151013', 
       'title':'Saira: Tujetsch - tuttina cuntinuar cun Sedrun Mustér Turissem', 
       'timestamp':1444750398}, 
      'params':{'skip_download': True}},
     {'url':'http://www.rts.ch/play/tv/-/video/le-19h30?id=6348260', 
      'md5':'67a2a9ae4e8e62a68d0e9820cc9782df', 
      'info_dict':{'id':'6348260', 
       'display_id':'6348260', 
       'ext':'mp4', 
       'duration':1796, 
       'title':'Le 19h30', 
       'description':'', 
       'uploader':'19h30', 
       'upload_date':'20141201', 
       'timestamp':1417458600, 
       'thumbnail':'re:^https?://.*\\.image', 
       'view_count':int}, 
      'params':{'skip_download': True}},
     {'url':'https://www.srf.ch/play/tv/popupvideoplayer?id=c4dba0ca-e75b-43b2-a34f-f708a4932e01', 
      'only_matching':True},
     {'url':'https://www.srf.ch/play/tv/10vor10/video/snowden-beantragt-asyl-in-russland?urn=urn:srf:video:28e1a57d-5b76-4399-8ab3-9097f071e6c5', 
      'only_matching':True},
     {'url':'https://www.rts.ch/play/tv/19h30/video/le-19h30?urn=urn:rts:video:6348260', 
      'only_matching':True}]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        bu = mobj.group('bu')
        media_type = mobj.group('type') or mobj.group('type_2')
        media_id = mobj.group('id')
        return self.url_result('srgssr:%s:%s:%s' % (bu[:3], media_type, media_id), 'SRGSSR')