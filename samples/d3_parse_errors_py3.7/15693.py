# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\extractor\gfycat.py
"""Extractors for https://gfycat.com/"""
from .common import Extractor, Message
from .. import text, exception
from ..cache import cache

class GfycatExtractor(Extractor):
    __doc__ = 'Base class for gfycat extractors'
    category = 'gfycat'
    filename_fmt = '{category}_{gfyName}{title:?_//}.{extension}'
    archive_fmt = '{gfyName}'
    root = 'https://gfycat.com'

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.key = match.group(1).lower()
        self.formats = (self.config('format', 'mp4'), 'mp4', 'webm', 'gif')

    def items(self):
        metadata = self.metadata()
        for gfycat in self.gfycats():
            if 'gfyName' not in gfycat:
                self.log.warning("Skipping '%s' (malformed)", gfycat['gfyId'])
                continue
            else:
                url = self._select_format(gfycat)
                gfycat.update(metadata)
                gfycat['date'] = text.parse_timestamp(gfycat.get('createDate'))
                yield (Message.Directory, gfycat)
                yield (Message.Url, url, gfycat)

    def _select_format(self, gfyitem):
        for fmt in self.formats:
            key = fmt + 'Url'
            if key in gfyitem:
                url = gfyitem[key]
                if url.startswith('http:'):
                    url = 'https' + url[4:]
                else:
                    gfyitem['extension'] = url.rpartition('.')[2]
                    return url

        gfyitem['extension'] = ''
        return ''

    def metadata(self):
        return {}

    def gfycats(self):
        return ()


class GfycatUserExtractor(GfycatExtractor):
    __doc__ = 'Extractor for gfycat user profiles'
    subcategory = 'user'
    directory_fmt = ('{category}', '{username|userName}')
    pattern = '(?:https?://)?gfycat\\.com/@([^/?#]+)'
    test = ('https://gfycat.com/@gretta',
     {'pattern':'https://giant\\.gfycat\\.com/[A-Za-z]+\\.mp4', 
      'count':'>= 100'})

    def gfycats(self):
        return GfycatAPI(self).user(self.key)


class GfycatSearchExtractor(GfycatExtractor):
    __doc__ = 'Extractor for gfycat search results'
    subcategory = 'search'
    directory_fmt = ('{category}', 'Search', '{search}')
    pattern = '(?:https?://)?gfycat\\.com/gifs/search/([^/?#]+)'
    test = ('https://gfycat.com/gifs/search/funny+animals',
     {'pattern':'https://\\w+\\.gfycat\\.com/[A-Za-z]+\\.mp4', 
      'archive':False, 
      'range':'100-300', 
      'count':'> 200'})

    def metadata(self):
        self.key = text.unquote(self.key).replace('+', ' ')
        return {'search': self.key}

    def gfycats(self):
        return GfycatAPI(self).search(self.key)


class GfycatImageExtractor(GfycatExtractor):
    __doc__ = 'Extractor for individual images from gfycat.com'
    subcategory = 'image'
    pattern = '(?:https?://)?(?:\\w+\\.)?gfycat\\.com/(?:gifs/detail/|\\w+/)?([A-Za-z]{8,})'
    test = (
     (
      'https://gfycat.com/GrayGenerousCowrie',
      {'url':'e0b5e1d7223108249b15c3c7898dd358dbfae045', 
       'content':'5786028e04b155baa20b87c5f4f77453cd5edc37', 
       'keyword':{'gfyId':'graygenerouscowrie', 
        'gfyName':'GrayGenerousCowrie', 
        'gfyNumber':'755075459', 
        'title':"Bottom's up", 
        'username':'jackson3oh3', 
        'createDate':1495884169, 
        'date':'dt:2017-05-27 11:22:49', 
        'md5':'a4796e05b0db9ba9ce5140145cd318aa', 
        'width':400, 
        'height':224, 
        'frameRate':23.0, 
        'numFrames':158.0, 
        'views':int}}),
     (
      'https://thumbs.gfycat.com/SillyLameIsabellinewheatear-size_restricted.gif',
      {'url': '13b32e6cc169d086577d7dd3fd36ee6cdbc02726'}),
     (
      'https://gfycat.com/detail/UnequaledHastyAnkole?tagname=aww',
      {'url': 'e24c9f69897fd223343782425a429c5cab6a768e'}),
     (
      'https://www.gfycat.com/foolishforkedabyssiniancat',
      {'pattern': 'https://redgifs.com/watch/foolishforkedabyssiniancat'}),
     (
      'https://gfycat.com/illexcitablehairstreak',
      {'count': 0}),
     'https://gfycat.com/gifs/detail/UnequaledHastyAnkole',
     'https://gfycat.com/ifr/UnequaledHastyAnkole',
     'https://gfycat.com/ru/UnequaledHastyAnkole')

    def items(self):
        try:
            gfycat = GfycatAPI(self).gfycat(self.key)
        except exception.HttpError:
            from .redgifs import RedgifsImageExtractor
            url = 'https://redgifs.com/watch/' + self.key
            data = {'_extractor': RedgifsImageExtractor}
            yield (Message.Queue, url, data)
        else:
            if 'gfyName' not in gfycat:
                self.log.warning("Skipping '%s' (malformed)", gfycat['gfyId'])
                return
            url = self._select_format(gfycat)
            gfycat['date'] = text.parse_timestamp(gfycat.get('createDate'))
            yield (Message.Directory, gfycat)
            yield (Message.Url, url, gfycat)


class GfycatAPI:
    API_ROOT = 'https://api.gfycat.com'
    ACCESS_KEY = 'Anr96uuqt9EdamSCwK4txKPjMsf2M95Rfa5FLLhPFucu8H5HTzeutyAa'

    def __init__(self, extractor):
        self.extractor = extractor
        self.headers = {}

    def gfycat(self, gfycat_id):
        endpoint = '/v1/gfycats/' + gfycat_id
        return self._call(endpoint)['gfyItem']

    def user(self, user):
        endpoint = '/v1/users/{}/gfycats'.format(user.lower())
        params = {'count': 100}
        return self._pagination(endpoint, params)

    def search(self, query):
        endpoint = '/v1/gfycats/search'
        params = {'search_text':query,  'count':150}
        return self._pagination(endpoint, params)

    @cache(keyarg=1, maxage=3600)
    def _authenticate_impl(self, category):
        url = 'https://weblogin.' + category + '.com/oauth/webtoken'
        data = {'access_key': self.ACCESS_KEY}
        headers = {'Referer':self.extractor.root + '/',  'Origin':self.extractor.root}
        response = self.extractor.request(url,
          method='POST', headers=headers, json=data)
        return 'Bearer ' + response.json()['access_token']

    def _call(self, endpoint, params=None):
        url = self.API_ROOT + endpoint
        self.headers['Authorization'] = self._authenticate_impl(self.extractor.category)
        return self.extractor.request(url,
          params=params, headers=(self.headers)).json()

    def _pagination--- This code section failed: ---

 L. 196         0  SETUP_LOOP          122  'to 122'
              2_0  COME_FROM           118  '118'

 L. 197         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _call
                6  LOAD_FAST                'endpoint'
                8  LOAD_FAST                'params'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  STORE_FAST               'data'

 L. 198        14  LOAD_FAST                'data'
               16  LOAD_STR                 'gfycats'
               18  BINARY_SUBSCR    
               20  STORE_FAST               'gfycats'

 L. 200        22  SETUP_LOOP           70  'to 70'
               24  LOAD_FAST                'gfycats'
               26  GET_ITER         
             28_0  COME_FROM            66  '66'
               28  FOR_ITER             68  'to 68'
               30  STORE_FAST               'gfycat'

 L. 201        32  LOAD_STR                 'gfyName'
               34  LOAD_FAST                'gfycat'
               36  COMPARE_OP               not-in
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L. 202        40  LOAD_FAST                'gfycat'
               42  LOAD_METHOD              update
               44  LOAD_FAST                'self'
               46  LOAD_METHOD              gfycat
               48  LOAD_FAST                'gfycat'
               50  LOAD_STR                 'gfyId'
               52  BINARY_SUBSCR    
               54  CALL_METHOD_1         1  '1 positional argument'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_TOP          
             60_0  COME_FROM            38  '38'

 L. 203        60  LOAD_FAST                'gfycat'
               62  YIELD_VALUE      
               64  POP_TOP          
               66  JUMP_BACK            28  'to 28'
               68  POP_BLOCK        
             70_0  COME_FROM_LOOP       22  '22'

 L. 205        70  LOAD_STR                 'found'
               72  LOAD_FAST                'data'
               74  COMPARE_OP               not-in
               76  POP_JUMP_IF_FALSE    94  'to 94'
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'gfycats'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  LOAD_FAST                'params'
               86  LOAD_STR                 'count'
               88  BINARY_SUBSCR    
               90  COMPARE_OP               <
               92  POP_JUMP_IF_TRUE    102  'to 102'
             94_0  COME_FROM            76  '76'

 L. 206        94  LOAD_FAST                'data'
               96  LOAD_STR                 'gfycats'
               98  BINARY_SUBSCR    
              100  POP_JUMP_IF_TRUE    106  'to 106'
            102_0  COME_FROM            92  '92'

 L. 207       102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 208       106  LOAD_FAST                'data'
              108  LOAD_STR                 'cursor'
              110  BINARY_SUBSCR    
              112  LOAD_FAST                'params'
              114  LOAD_STR                 'cursor'
              116  STORE_SUBSCR     
              118  JUMP_BACK             2  'to 2'
              120  POP_BLOCK        
            122_0  COME_FROM_LOOP        0  '0'

Parse error at or near `LOAD_FAST' instruction at offset 106