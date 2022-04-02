# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\nowness.py
from __future__ import unicode_literals
from .brightcove import BrightcoveLegacyIE, BrightcoveNewIE
from .common import InfoExtractor
from ..compat import compat_str
from ..utils import ExtractorError, sanitized_Request

class NownessBaseIE(InfoExtractor):

    def _extract_url_result--- This code section failed: ---

 L.  18         0  LOAD_FAST                'post'
                2  LOAD_STR                 'type'
                4  BINARY_SUBSCR    
                6  LOAD_STR                 'video'
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE   212  'to 212'

 L.  19        12  SETUP_LOOP          212  'to 212'
               14  LOAD_FAST                'post'
               16  LOAD_STR                 'media'
               18  BINARY_SUBSCR    
               20  GET_ITER         
             22_0  COME_FROM           206  '206'
             22_1  COME_FROM            36  '36'
               22  FOR_ITER            210  'to 210'
               24  STORE_FAST               'media'

 L.  20        26  LOAD_FAST                'media'
               28  LOAD_STR                 'type'
               30  BINARY_SUBSCR    
               32  LOAD_STR                 'video'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    22  'to 22'

 L.  21        38  LOAD_FAST                'media'
               40  LOAD_STR                 'content'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'video_id'

 L.  22        46  LOAD_FAST                'media'
               48  LOAD_STR                 'source'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'source'

 L.  23        54  LOAD_FAST                'source'
               56  LOAD_STR                 'brightcove'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   156  'to 156'

 L.  24        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _download_webpage

 L.  25        66  LOAD_STR                 'http://www.nowness.com/iframe?id=%s'
               68  LOAD_FAST                'video_id'
               70  BINARY_MODULO    
               72  LOAD_FAST                'video_id'

 L.  26        74  LOAD_STR                 'Downloading player JavaScript'

 L.  27        76  LOAD_STR                 'Unable to download player JavaScript'
               78  LOAD_CONST               ('note', 'errnote')
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  STORE_FAST               'player_code'

 L.  28        84  LOAD_GLOBAL              BrightcoveLegacyIE
               86  LOAD_METHOD              _extract_brightcove_url
               88  LOAD_FAST                'player_code'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               'bc_url'

 L.  29        94  LOAD_FAST                'bc_url'
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L.  30        98  LOAD_FAST                'self'
              100  LOAD_METHOD              url_result
              102  LOAD_FAST                'bc_url'
              104  LOAD_GLOBAL              BrightcoveLegacyIE
              106  LOAD_METHOD              ie_key
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  RETURN_VALUE     
            114_0  COME_FROM            96  '96'

 L.  31       114  LOAD_GLOBAL              BrightcoveNewIE
              116  LOAD_METHOD              _extract_url
              118  LOAD_FAST                'self'
              120  LOAD_FAST                'player_code'
              122  CALL_METHOD_2         2  '2 positional arguments'
              124  STORE_FAST               'bc_url'

 L.  32       126  LOAD_FAST                'bc_url'
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L.  33       130  LOAD_FAST                'self'
              132  LOAD_METHOD              url_result
              134  LOAD_FAST                'bc_url'
              136  LOAD_GLOBAL              BrightcoveNewIE
              138  LOAD_METHOD              ie_key
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  CALL_METHOD_2         2  '2 positional arguments'
              144  RETURN_VALUE     
            146_0  COME_FROM           128  '128'

 L.  34       146  LOAD_GLOBAL              ExtractorError
              148  LOAD_STR                 'Could not find player definition'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception instance'
              154  JUMP_BACK            22  'to 22'
            156_0  COME_FROM            60  '60'

 L.  35       156  LOAD_FAST                'source'
              158  LOAD_STR                 'vimeo'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   180  'to 180'

 L.  36       164  LOAD_FAST                'self'
              166  LOAD_METHOD              url_result
              168  LOAD_STR                 'http://vimeo.com/%s'
              170  LOAD_FAST                'video_id'
              172  BINARY_MODULO    
              174  LOAD_STR                 'Vimeo'
              176  CALL_METHOD_2         2  '2 positional arguments'
              178  RETURN_VALUE     
            180_0  COME_FROM           162  '162'

 L.  37       180  LOAD_FAST                'source'
              182  LOAD_STR                 'youtube'
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L.  38       188  LOAD_FAST                'self'
              190  LOAD_METHOD              url_result
              192  LOAD_FAST                'video_id'
              194  LOAD_STR                 'Youtube'
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  RETURN_VALUE     
            200_0  COME_FROM           186  '186'

 L.  39       200  LOAD_FAST                'source'
              202  LOAD_STR                 'cinematique'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE    22  'to 22'

 L.  42       208  JUMP_BACK            22  'to 22'
              210  POP_BLOCK        
            212_0  COME_FROM_LOOP       12  '12'
            212_1  COME_FROM            10  '10'

Parse error at or near `POP_BLOCK' instruction at offset 210

    def _api_request(self, url, request_path):
        display_id = self._match_idurl
        request = sanitized_Request(('http://api.nowness.com/api/' + request_path % display_id),
          headers={'X-Nowness-Language': 'zh-cn' if 'cn.nowness.com' in url else 'en-us'})
        return (
         display_id, self._download_jsonrequestdisplay_id)


class NownessIE(NownessBaseIE):
    IE_NAME = 'nowness'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/(?:story|(?:series|category)/[^/]+)/(?P<id>[^/]+?)(?:$|[?#])'
    _TESTS = [
     {'url':'https://www.nowness.com/story/candor-the-art-of-gesticulation', 
      'md5':'068bc0202558c2e391924cb8cc470676', 
      'info_dict':{'id':'2520295746001', 
       'ext':'mp4', 
       'title':'Candor: The Art of Gesticulation', 
       'description':'Candor: The Art of Gesticulation', 
       'thumbnail':'re:^https?://.*\\.jpg', 
       'timestamp':1446745676, 
       'upload_date':'20151105', 
       'uploader_id':'2385340575001'}, 
      'add_ie':[
       'BrightcoveNew']},
     {'url':'https://cn.nowness.com/story/kasper-bjorke-ft-jaakko-eino-kalevi-tnr', 
      'md5':'e79cf125e387216f86b2e0a5b5c63aa3', 
      'info_dict':{'id':'3716354522001', 
       'ext':'mp4', 
       'title':'Kasper Bjørke ft. Jaakko Eino Kalevi: TNR', 
       'description':'Kasper Bjørke ft. Jaakko Eino Kalevi: TNR', 
       'thumbnail':'re:^https?://.*\\.jpg', 
       'timestamp':1407315371, 
       'upload_date':'20140806', 
       'uploader_id':'2385340575001'}, 
      'add_ie':[
       'BrightcoveNew']},
     {'url':'https://www.nowness.com/series/nowness-picks/jean-luc-godard-supercut', 
      'md5':'9a5a6a8edf806407e411296ab6bc2a49', 
      'info_dict':{'id':'130020913', 
       'ext':'mp4', 
       'title':'Bleu, Blanc, Rouge - A Godard Supercut', 
       'description':'md5:f0ea5f1857dffca02dbd37875d742cec', 
       'thumbnail':'re:^https?://.*\\.jpg', 
       'upload_date':'20150607', 
       'uploader':'Cinema Sem Lei', 
       'uploader_id':'cinemasemlei'}, 
      'add_ie':[
       'Vimeo']}]

    def _real_extract(self, url):
        _, post = self._api_requesturl'post/getBySlug/%s'
        return self._extract_url_resultpost


class NownessPlaylistIE(NownessBaseIE):
    IE_NAME = 'nowness:playlist'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/playlist/(?P<id>\\d+)'
    _TEST = {'url':'https://www.nowness.com/playlist/3286/i-guess-thats-why-they-call-it-the-blues', 
     'info_dict':{'id': '3286'}, 
     'playlist_mincount':8}

    def _real_extract(self, url):
        playlist_id, playlist = self._api_requesturl'post?PlaylistId=%s'
        entries = [self._extract_url_resultitem for item in playlist['items']]
        return self.playlist_resultentriesplaylist_id


class NownessSeriesIE(NownessBaseIE):
    IE_NAME = 'nowness:series'
    _VALID_URL = 'https?://(?:(?:www|cn)\\.)?nowness\\.com/series/(?P<id>[^/]+?)(?:$|[?#])'
    _TEST = {'url':'https://www.nowness.com/series/60-seconds', 
     'info_dict':{'id':'60', 
      'title':'60 Seconds', 
      'description':'One-minute wisdom in a new NOWNESS series'}, 
     'playlist_mincount':4}

    def _real_extract(self, url):
        display_id, series = self._api_requesturl'series/getBySlug/%s'
        entries = [self._extract_url_resultpost for post in series['posts']]
        series_title = None
        series_description = None
        translations = series.get'translations'[]
        if translations:
            series_title = translations[0].get'title' or translations[0]['seoTitle']
            series_description = translations[0].get'seoDescription'
        return self.playlist_result(entries, compat_str(series['id']), series_title, series_description)