# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\animeondemand.py
from __future__ import unicode_literals
import re
from .common import InfoExtractor
from ..compat import compat_str
from ..utils import determine_ext, extract_attributes, ExtractorError, url_or_none, urlencode_postdata, urljoin

class AnimeOnDemandIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?anime-on-demand\\.de/anime/(?P<id>\\d+)'
    _LOGIN_URL = 'https://www.anime-on-demand.de/users/sign_in'
    _APPLY_HTML5_URL = 'https://www.anime-on-demand.de/html5apply'
    _NETRC_MACHINE = 'animeondemand'
    _GEO_COUNTRIES = [
     'AT', 'CH', 'DE', 'LI', 'LU']
    _TESTS = [
     {'url':'https://www.anime-on-demand.de/anime/161', 
      'info_dict':{'id':'161', 
       'title':'Grimgar, Ashes and Illusions (OmU)', 
       'description':'md5:6681ce3c07c7189d255ac6ab23812d31'}, 
      'playlist_mincount':4},
     {'url':'https://www.anime-on-demand.de/anime/39', 
      'only_matching':True},
     {'url':'https://www.anime-on-demand.de/anime/162', 
      'only_matching':True},
     {'url':'https://www.anime-on-demand.de/anime/169', 
      'only_matching':True},
     {'url':'https://www.anime-on-demand.de/anime/185', 
      'only_matching':True},
     {'url':'https://www.anime-on-demand.de/anime/12', 
      'only_matching':True}]

    def _login(self):
        username, password = self._get_login_info()
        if username is None:
            return
        login_page = self._download_webpage(self._LOGIN_URL, None, 'Downloading login page')
        if '>Our licensing terms allow the distribution of animes only to German-speaking countries of Europe' in login_page:
            self.raise_geo_restricted('%s is only available in German-speaking countries of Europe' % self.IE_NAME)
        login_form = self._form_hidden_inputs('new_user', login_page)
        login_form.update({'user[login]':username, 
         'user[password]':password})
        post_url = self._search_regex('<form[^>]+action=(["\\\'])(?P<url>.+?)\\1',
          login_page, 'post url',
          default=(self._LOGIN_URL), group='url')
        if not post_url.startswith('http'):
            post_url = urljoin(self._LOGIN_URL, post_url)
        response = self._download_webpage(post_url,
          None, 'Logging in', data=(urlencode_postdata(login_form)),
          headers={'Referer': self._LOGIN_URL})
        if all((p not in response for p in ('>Logout<', 'href="/users/sign_out"'))):
            error = self._search_regex('<p[^>]+\\bclass=(["\\\'])(?:(?!\\1).)*\\balert\\b(?:(?!\\1).)*\\1[^>]*>(?P<error>.+?)</p>',
              response,
              'error', default=None, group='error')
            if error:
                raise ExtractorError(('Unable to login: %s' % error), expected=True)
            raise ExtractorError('Unable to log in')

    def _real_initialize(self):
        self._login()

    def _real_extract(self, url):
        anime_id = self._match_id(url)
        webpage = self._download_webpage(url, anime_id)
        if 'data-playlist=' not in webpage:
            self._download_webpage(self._APPLY_HTML5_URL, anime_id, 'Activating HTML5 beta', 'Unable to apply HTML5 beta')
            webpage = self._download_webpage(url, anime_id)
        csrf_token = self._html_search_meta('csrf-token',
          webpage, 'csrf token', fatal=True)
        anime_title = self._html_search_regex('(?s)<h1[^>]+itemprop="name"[^>]*>(.+?)</h1>', webpage, 'anime name')
        anime_description = self._html_search_regex('(?s)<div[^>]+itemprop="description"[^>]*>(.+?)</div>',
          webpage,
          'anime description', default=None)

        def extract_info--- This code section failed: ---

 L. 120         0  LOAD_CONST               None
                2  BUILD_LIST_1          1 
                4  LOAD_CONST               2
                6  BINARY_MULTIPLY  
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'title'
               12  STORE_FAST               'description'

 L. 121        14  BUILD_LIST_0          0 
               16  STORE_FAST               'formats'

 L. 123     18_20  SETUP_LOOP          788  'to 788'
               22  LOAD_GLOBAL              re
               24  LOAD_METHOD              findall

 L. 124        26  LOAD_STR                 '<input[^>]+class=["\\\'].*?streamstarter[^>]+>'
               28  LOAD_FAST                'html'
               30  CALL_METHOD_2         2  '2 positional arguments'
               32  GET_ITER         
             34_0  COME_FROM           784  '784'
             34_1  COME_FROM           126  '126'
            34_36  FOR_ITER            786  'to 786'
               38  STORE_FAST               'input_'

 L. 125        40  LOAD_GLOBAL              extract_attributes
               42  LOAD_FAST                'input_'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'attributes'

 L. 126        48  LOAD_FAST                'attributes'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'data-dialog-header'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  STORE_FAST               'title'

 L. 127        58  BUILD_LIST_0          0 
               60  STORE_FAST               'playlist_urls'

 L. 128        62  SETUP_LOOP          122  'to 122'
               64  LOAD_CONST               ('data-playlist', 'data-otherplaylist', 'data-stream')
               66  GET_ITER         
             68_0  COME_FROM           118  '118'
             68_1  COME_FROM           102  '102'
             68_2  COME_FROM            90  '90'
               68  FOR_ITER            120  'to 120'
               70  STORE_FAST               'playlist_key'

 L. 129        72  LOAD_FAST                'attributes'
               74  LOAD_METHOD              get
               76  LOAD_FAST                'playlist_key'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  STORE_FAST               'playlist_url'

 L. 130        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'playlist_url'
               86  LOAD_GLOBAL              compat_str
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  POP_JUMP_IF_FALSE_BACK    68  'to 68'
               92  LOAD_GLOBAL              re
               94  LOAD_METHOD              match

 L. 131        96  LOAD_STR                 '/?[\\da-zA-Z]+'
               98  LOAD_FAST                'playlist_url'
              100  CALL_METHOD_2         2  '2 positional arguments'
              102  POP_JUMP_IF_FALSE_BACK    68  'to 68'

 L. 132       104  LOAD_FAST                'playlist_urls'
              106  LOAD_METHOD              append
              108  LOAD_FAST                'attributes'
              110  LOAD_FAST                'playlist_key'
              112  BINARY_SUBSCR    
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_TOP          
              118  JUMP_BACK            68  'to 68'
              120  POP_BLOCK        
            122_0  COME_FROM_LOOP       62  '62'

 L. 133       122  LOAD_FAST                'playlist_urls'
              124  POP_JUMP_IF_TRUE    128  'to 128'

 L. 134       126  CONTINUE             34  'to 34'
            128_0  COME_FROM           124  '124'

 L. 136       128  LOAD_FAST                'attributes'
              130  LOAD_METHOD              get
              132  LOAD_STR                 'data-lang'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  STORE_FAST               'lang'

 L. 137       138  LOAD_FAST                'attributes'
              140  LOAD_METHOD              get
              142  LOAD_STR                 'value'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  STORE_FAST               'lang_note'

 L. 139   148_150  SETUP_LOOP          784  'to 784'
              152  LOAD_FAST                'playlist_urls'
              154  GET_ITER         
            156_0  COME_FROM           780  '780'
            156_1  COME_FROM           502  '502'
            156_2  COME_FROM           476  '476'
            156_3  COME_FROM           462  '462'
            156_4  COME_FROM           436  '436'
            156_5  COME_FROM           350  '350'
          156_158  FOR_ITER            782  'to 782'
              160  STORE_FAST               'playlist_url'

 L. 140       162  LOAD_DEREF               'self'
              164  LOAD_ATTR                _search_regex

 L. 141       166  LOAD_STR                 'videomaterialurl/\\d+/([^/]+)/'

 L. 142       168  LOAD_FAST                'playlist_url'
              170  LOAD_STR                 'media kind'
              172  LOAD_CONST               None
              174  LOAD_CONST               ('default',)
              176  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              178  STORE_FAST               'kind'

 L. 143       180  BUILD_LIST_0          0 
              182  STORE_FAST               'format_id_list'

 L. 144       184  LOAD_FAST                'lang'
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 145       188  LOAD_FAST                'format_id_list'
              190  LOAD_METHOD              append
              192  LOAD_FAST                'lang'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          
            198_0  COME_FROM           186  '186'

 L. 146       198  LOAD_FAST                'kind'
              200  POP_JUMP_IF_FALSE   212  'to 212'

 L. 147       202  LOAD_FAST                'format_id_list'
              204  LOAD_METHOD              append
              206  LOAD_FAST                'kind'
              208  CALL_METHOD_1         1  '1 positional argument'
              210  POP_TOP          
            212_0  COME_FROM           200  '200'

 L. 148       212  LOAD_FAST                'format_id_list'
              214  POP_JUMP_IF_TRUE    238  'to 238'
              216  LOAD_FAST                'num'
              218  LOAD_CONST               None
              220  COMPARE_OP               is-not
              222  POP_JUMP_IF_FALSE   238  'to 238'

 L. 149       224  LOAD_FAST                'format_id_list'
              226  LOAD_METHOD              append
              228  LOAD_GLOBAL              compat_str
              230  LOAD_FAST                'num'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  POP_TOP          
            238_0  COME_FROM           222  '222'
            238_1  COME_FROM           214  '214'

 L. 150       238  LOAD_STR                 '-'
              240  LOAD_METHOD              join
              242  LOAD_FAST                'format_id_list'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  STORE_FAST               'format_id'

 L. 151       248  LOAD_STR                 ', '
              250  LOAD_METHOD              join
              252  LOAD_GLOBAL              filter
              254  LOAD_CONST               None
              256  LOAD_FAST                'kind'
              258  LOAD_FAST                'lang_note'
              260  BUILD_TUPLE_2         2 
              262  CALL_FUNCTION_2       2  '2 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               'format_note'

 L. 152       268  BUILD_LIST_0          0 
              270  STORE_FAST               'item_id_list'

 L. 153       272  LOAD_FAST                'format_id'
          274_276  POP_JUMP_IF_FALSE   288  'to 288'

 L. 154       278  LOAD_FAST                'item_id_list'
              280  LOAD_METHOD              append
              282  LOAD_FAST                'format_id'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  POP_TOP          
            288_0  COME_FROM           274  '274'

 L. 155       288  LOAD_FAST                'item_id_list'
              290  LOAD_METHOD              append
              292  LOAD_STR                 'videomaterial'
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          

 L. 156       298  LOAD_DEREF               'self'
              300  LOAD_ATTR                _download_json

 L. 157       302  LOAD_GLOBAL              urljoin
              304  LOAD_DEREF               'url'
              306  LOAD_FAST                'playlist_url'
              308  CALL_FUNCTION_2       2  '2 positional arguments'
              310  LOAD_FAST                'video_id'

 L. 158       312  LOAD_STR                 'Downloading %s JSON'
              314  LOAD_STR                 ' '
              316  LOAD_METHOD              join
              318  LOAD_FAST                'item_id_list'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  BINARY_MODULO    

 L. 160       324  LOAD_STR                 'XMLHttpRequest'

 L. 161       326  LOAD_DEREF               'csrf_token'

 L. 162       328  LOAD_DEREF               'url'

 L. 163       330  LOAD_STR                 'application/json, text/javascript, */*; q=0.01'
              332  LOAD_CONST               ('X-Requested-With', 'X-CSRF-Token', 'Referer', 'Accept')
              334  BUILD_CONST_KEY_MAP_4     4 

 L. 164       336  LOAD_CONST               False
              338  LOAD_CONST               ('headers', 'fatal')
              340  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              342  STORE_FAST               'playlist'

 L. 165       344  LOAD_FAST                'playlist'
          346_348  POP_JUMP_IF_TRUE    352  'to 352'

 L. 166       350  CONTINUE            156  'to 156'
            352_0  COME_FROM           346  '346'

 L. 167       352  LOAD_GLOBAL              url_or_none
              354  LOAD_FAST                'playlist'
              356  LOAD_METHOD              get
              358  LOAD_STR                 'streamurl'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  STORE_FAST               'stream_url'

 L. 168       366  LOAD_FAST                'stream_url'
          368_370  POP_JUMP_IF_FALSE   438  'to 438'

 L. 169       372  LOAD_GLOBAL              re
              374  LOAD_METHOD              search

 L. 170       376  LOAD_STR                 '^(?P<url>rtmpe?://(?P<host>[^/]+)/(?P<app>.+/))(?P<playpath>mp[34]:.+)'

 L. 171       378  LOAD_FAST                'stream_url'
              380  CALL_METHOD_2         2  '2 positional arguments'
              382  STORE_FAST               'rtmp'

 L. 172       384  LOAD_FAST                'rtmp'
          386_388  POP_JUMP_IF_FALSE   438  'to 438'

 L. 173       390  LOAD_FAST                'formats'
              392  LOAD_METHOD              append

 L. 174       394  LOAD_FAST                'rtmp'
              396  LOAD_METHOD              group
              398  LOAD_STR                 'url'
              400  CALL_METHOD_1         1  '1 positional argument'

 L. 175       402  LOAD_FAST                'rtmp'
              404  LOAD_METHOD              group
              406  LOAD_STR                 'app'
              408  CALL_METHOD_1         1  '1 positional argument'

 L. 176       410  LOAD_FAST                'rtmp'
              412  LOAD_METHOD              group
              414  LOAD_STR                 'playpath'
              416  CALL_METHOD_1         1  '1 positional argument'

 L. 177       418  LOAD_DEREF               'url'

 L. 178       420  LOAD_STR                 'https://www.anime-on-demand.de/assets/jwplayer.flash-55abfb34080700304d49125ce9ffb4a6.swf'

 L. 179       422  LOAD_CONST               True

 L. 180       424  LOAD_STR                 'rtmp'

 L. 181       426  LOAD_STR                 'flv'
              428  LOAD_CONST               ('url', 'app', 'play_path', 'page_url', 'player_url', 'rtmp_real_time', 'format_id', 'ext')
              430  BUILD_CONST_KEY_MAP_8     8 
              432  CALL_METHOD_1         1  '1 positional argument'
              434  POP_TOP          

 L. 183       436  CONTINUE            156  'to 156'
            438_0  COME_FROM           386  '386'
            438_1  COME_FROM           368  '368'

 L. 184       438  LOAD_FAST                'playlist'
              440  LOAD_METHOD              get
              442  LOAD_STR                 'startvideo'
              444  LOAD_CONST               0
              446  CALL_METHOD_2         2  '2 positional arguments'
              448  STORE_FAST               'start_video'

 L. 185       450  LOAD_FAST                'playlist'
              452  LOAD_METHOD              get
              454  LOAD_STR                 'playlist'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  STORE_FAST               'playlist'

 L. 186       460  LOAD_FAST                'playlist'
              462  POP_JUMP_IF_FALSE_BACK   156  'to 156'
              464  LOAD_GLOBAL              isinstance
              466  LOAD_FAST                'playlist'
              468  LOAD_GLOBAL              list
              470  CALL_FUNCTION_2       2  '2 positional arguments'
          472_474  POP_JUMP_IF_TRUE    478  'to 478'

 L. 187       476  CONTINUE            156  'to 156'
            478_0  COME_FROM           472  '472'

 L. 188       478  LOAD_FAST                'playlist'
              480  LOAD_FAST                'start_video'
              482  BINARY_SUBSCR    
              484  STORE_FAST               'playlist'

 L. 189       486  LOAD_FAST                'playlist'
              488  LOAD_METHOD              get
              490  LOAD_STR                 'title'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  STORE_FAST               'title'

 L. 190       496  LOAD_FAST                'title'
          498_500  POP_JUMP_IF_TRUE    504  'to 504'

 L. 191       502  CONTINUE            156  'to 156'
            504_0  COME_FROM           498  '498'

 L. 192       504  LOAD_FAST                'playlist'
              506  LOAD_METHOD              get
              508  LOAD_STR                 'description'
              510  CALL_METHOD_1         1  '1 positional argument'
              512  STORE_FAST               'description'

 L. 193   514_516  SETUP_LOOP          780  'to 780'
              518  LOAD_FAST                'playlist'
              520  LOAD_METHOD              get
              522  LOAD_STR                 'sources'
              524  BUILD_LIST_0          0 
              526  CALL_METHOD_2         2  '2 positional arguments'
              528  GET_ITER         
            530_0  COME_FROM           774  '774'
            530_1  COME_FROM           728  '728'
            530_2  COME_FROM           704  '704'
            530_3  COME_FROM           700  '700'
            530_4  COME_FROM           690  '690'
            530_5  COME_FROM           550  '550'
              530  FOR_ITER            778  'to 778'
              532  STORE_FAST               'source'

 L. 194       534  LOAD_FAST                'source'
              536  LOAD_METHOD              get
              538  LOAD_STR                 'file'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  STORE_FAST               'file_'

 L. 195       544  LOAD_FAST                'file_'
          546_548  POP_JUMP_IF_TRUE    554  'to 554'

 L. 196   550_552  CONTINUE            530  'to 530'
            554_0  COME_FROM           546  '546'

 L. 197       554  LOAD_GLOBAL              determine_ext
              556  LOAD_FAST                'file_'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  STORE_FAST               'ext'

 L. 198       562  LOAD_FAST                'lang'
              564  LOAD_FAST                'kind'
              566  BUILD_LIST_2          2 
              568  STORE_FAST               'format_id_list'

 L. 199       570  LOAD_FAST                'ext'
              572  LOAD_STR                 'm3u8'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   592  'to 592'

 L. 200       580  LOAD_FAST                'format_id_list'
              582  LOAD_METHOD              append
              584  LOAD_STR                 'hls'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  POP_TOP          
              590  JUMP_FORWARD        628  'to 628'
            592_0  COME_FROM           576  '576'

 L. 201       592  LOAD_FAST                'source'
              594  LOAD_METHOD              get
              596  LOAD_STR                 'type'
              598  CALL_METHOD_1         1  '1 positional argument'
              600  LOAD_STR                 'video/dash'
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_TRUE    618  'to 618'
              608  LOAD_FAST                'ext'
              610  LOAD_STR                 'mpd'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   628  'to 628'
            618_0  COME_FROM           604  '604'

 L. 202       618  LOAD_FAST                'format_id_list'
              620  LOAD_METHOD              append
              622  LOAD_STR                 'dash'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  POP_TOP          
            628_0  COME_FROM           614  '614'
            628_1  COME_FROM           590  '590'

 L. 203       628  LOAD_STR                 '-'
              630  LOAD_METHOD              join
              632  LOAD_GLOBAL              filter
              634  LOAD_CONST               None
              636  LOAD_FAST                'format_id_list'
              638  CALL_FUNCTION_2       2  '2 positional arguments'
              640  CALL_METHOD_1         1  '1 positional argument'
              642  STORE_FAST               'format_id'

 L. 204       644  LOAD_FAST                'ext'
              646  LOAD_STR                 'm3u8'
              648  COMPARE_OP               ==
          650_652  POP_JUMP_IF_FALSE   678  'to 678'

 L. 205       654  LOAD_DEREF               'self'
              656  LOAD_ATTR                _extract_m3u8_formats

 L. 206       658  LOAD_FAST                'file_'
              660  LOAD_FAST                'video_id'
              662  LOAD_STR                 'mp4'

 L. 207       664  LOAD_STR                 'm3u8_native'
              666  LOAD_FAST                'format_id'
              668  LOAD_CONST               False
              670  LOAD_CONST               ('entry_protocol', 'm3u8_id', 'fatal')
              672  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              674  STORE_FAST               'file_formats'
              676  JUMP_FORWARD        732  'to 732'
            678_0  COME_FROM           650  '650'

 L. 208       678  LOAD_FAST                'source'
              680  LOAD_METHOD              get
              682  LOAD_STR                 'type'
              684  CALL_METHOD_1         1  '1 positional argument'
              686  LOAD_STR                 'video/dash'
              688  COMPARE_OP               ==
          690_692  POP_JUMP_IF_TRUE_BACK   530  'to 530'
              694  LOAD_FAST                'ext'
              696  LOAD_STR                 'mpd'
              698  COMPARE_OP               ==
          700_702  POP_JUMP_IF_FALSE_BACK   530  'to 530'

 L. 209   704_706  CONTINUE            530  'to 530'

 L. 210       708  LOAD_DEREF               'self'
              710  LOAD_ATTR                _extract_mpd_formats

 L. 211       712  LOAD_FAST                'file_'
              714  LOAD_FAST                'video_id'
              716  LOAD_FAST                'format_id'
              718  LOAD_CONST               False
              720  LOAD_CONST               ('mpd_id', 'fatal')
              722  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              724  STORE_FAST               'file_formats'
              726  JUMP_FORWARD        732  'to 732'

 L. 213   728_730  CONTINUE            530  'to 530'
            732_0  COME_FROM           726  '726'
            732_1  COME_FROM           676  '676'

 L. 214       732  SETUP_LOOP          764  'to 764'
              734  LOAD_FAST                'file_formats'
              736  GET_ITER         
            738_0  COME_FROM           758  '758'
              738  FOR_ITER            762  'to 762'
              740  STORE_FAST               'f'

 L. 215       742  LOAD_FAST                'f'
              744  LOAD_METHOD              update

 L. 216       746  LOAD_FAST                'lang'

 L. 217       748  LOAD_FAST                'format_note'
              750  LOAD_CONST               ('language', 'format_note')
              752  BUILD_CONST_KEY_MAP_2     2 
              754  CALL_METHOD_1         1  '1 positional argument'
              756  POP_TOP          
          758_760  JUMP_BACK           738  'to 738'
              762  POP_BLOCK        
            764_0  COME_FROM_LOOP      732  '732'

 L. 219       764  LOAD_FAST                'formats'
              766  LOAD_METHOD              extend
              768  LOAD_FAST                'file_formats'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  POP_TOP          
          774_776  JUMP_BACK           530  'to 530'
              778  POP_BLOCK        
            780_0  COME_FROM_LOOP      514  '514'
              780  JUMP_BACK           156  'to 156'
              782  POP_BLOCK        
            784_0  COME_FROM_LOOP      148  '148'
              784  JUMP_BACK            34  'to 34'
              786  POP_BLOCK        
            788_0  COME_FROM_LOOP       18  '18'

 L. 222       788  LOAD_FAST                'title'

 L. 223       790  LOAD_FAST                'description'

 L. 224       792  LOAD_FAST                'formats'
              794  LOAD_CONST               ('title', 'description', 'formats')
              796  BUILD_CONST_KEY_MAP_3     3 
              798  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 726

        def extract_entries(html, video_id, common_info, num=None):
            info = extract_info(html, video_id, num)
            if info['formats']:
                self._sort_formats(info['formats'])
                f = common_info.copy()
                f.update(info)
                yield f
            if not info['formats']:
                m = re.search('data-dialog-header=(["\\\'])(?P<title>.+?)\\1[^>]+href=(["\\\'])(?P<href>.+?)\\3[^>]*>(?P<kind>Teaser|Trailer)<', html)
                if m:
                    f = common_info.copy()
                    f.update({'id':'%s-%s' % (f['id'], m.group('kind').lower()), 
                     'title':m.group('title'), 
                     'url':urljoin(url, m.group('href'))})
                    yield f

        def extract_episodes(html):
            for num, episode_html in enumerate(re.findall('(?s)<h3[^>]+class="episodebox-title".+?>Episodeninhalt<', html), 1):
                episodebox_title = self._search_regex(('class="episodebox-title"[^>]+title=(["\\\'])(?P<title>.+?)\\1',
                                                       'class="episodebox-title"[^>]+>(?P<title>.+?)<'),
                  episode_html,
                  'episodebox title', default=None, group='title')
                if not episodebox_title:
                    continue
                else:
                    episode_number = int(self._search_regex('(?:Episode|Film)\\s*(\\d+)',
                      episodebox_title,
                      'episode number', default=num))
                    episode_title = self._search_regex('(?:Episode|Film)\\s*\\d+\\s*-\\s*(.+)',
                      episodebox_title,
                      'episode title', default=None)
                    video_id = 'episode-%d' % episode_number
                    common_info = {'id':video_id, 
                     'series':anime_title, 
                     'episode':episode_title, 
                     'episode_number':episode_number}
                    for e in extract_entries(episode_html, video_id, common_info):
                        yield e

        def extract_film(html, video_id):
            common_info = {'id':anime_id, 
             'title':anime_title, 
             'description':anime_description}
            for e in extract_entries(html, video_id, common_info):
                yield e

        def entries():
            has_episodes = False
            for e in extract_episodes(webpage):
                has_episodes = True
                yield e

            if not has_episodes:
                for e in extract_film(webpage, anime_id):
                    yield e

        return self.playlist_result(entries(), anime_id, anime_title, anime_description)