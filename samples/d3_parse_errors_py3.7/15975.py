# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\bbc.py
from __future__ import unicode_literals
import itertools, re
from .common import InfoExtractor
from ..utils import clean_html, dict_get, ExtractorError, float_or_none, get_element_by_class, int_or_none, js_to_json, parse_duration, parse_iso8601, try_get, unescapeHTML, url_or_none, urlencode_postdata, urljoin
from ..compat import compat_etree_Element, compat_HTTPError, compat_urlparse

class BBCCoUkIE(InfoExtractor):
    IE_NAME = 'bbc.co.uk'
    IE_DESC = 'BBC iPlayer'
    _ID_REGEX = '(?:[pbm][\\da-z]{7}|w[\\da-z]{7,14})'
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?bbc\\.co\\.uk/\n                        (?:\n                            programmes/(?!articles/)|\n                            iplayer(?:/[^/]+)?/(?:episode/|playlist/)|\n                            music/(?:clips|audiovideo/popular)[/#]|\n                            radio/player/|\n                            sounds/play/|\n                            events/[^/]+/play/[^/]+/\n                        )\n                        (?P<id>%s)(?!/(?:episodes|broadcasts|clips))\n                    ' % _ID_REGEX
    _LOGIN_URL = 'https://account.bbc.com/signin'
    _NETRC_MACHINE = 'bbc'
    _MEDIA_SELECTOR_URL_TEMPL = 'https://open.live.bbc.co.uk/mediaselector/6/select/version/2.0/mediaset/%s/vpid/%s'
    _MEDIA_SETS = [
     'iptv-all',
     'pc']
    _EMP_PLAYLIST_NS = 'http://bbc.co.uk/2008/emp/playlist'
    _TESTS = [
     {'url':'http://www.bbc.co.uk/programmes/b039g8p7', 
      'info_dict':{'id':'b039d07m', 
       'ext':'flv', 
       'title':'Kaleidoscope, Leonard Cohen', 
       'description':'The Canadian poet and songwriter reflects on his musical career.'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.co.uk/iplayer/episode/b00yng5w/The_Man_in_Black_Series_3_The_Printed_Name/', 
      'info_dict':{'id':'b00yng1d', 
       'ext':'flv', 
       'title':'The Man in Black: Series 3: The Printed Name', 
       'description':"Mark Gatiss introduces Nicholas Pierpan's chilling tale of a writer's devilish pact with a mysterious man. Stars Ewan Bailey.", 
       'duration':1800}, 
      'params':{'skip_download': True}, 
      'skip':'Episode is no longer available on BBC iPlayer Radio'},
     {'url':'http://www.bbc.co.uk/iplayer/episode/b03vhd1f/The_Voice_UK_Series_3_Blind_Auditions_5/', 
      'info_dict':{'id':'b00yng1d', 
       'ext':'flv', 
       'title':'The Voice UK: Series 3: Blind Auditions 5', 
       'description':'Emma Willis and Marvin Humes present the fifth set of blind auditions in the singing competition, as the coaches continue to build their teams based on voice alone.', 
       'duration':5100}, 
      'params':{'skip_download': True}, 
      'skip':'Currently BBC iPlayer TV programmes are available to play in the UK only'},
     {'url':'http://www.bbc.co.uk/iplayer/episode/p026c7jt/tomorrows-worlds-the-unearthly-history-of-science-fiction-2-invasion', 
      'info_dict':{'id':'b03k3pb7', 
       'ext':'flv', 
       'title':"Tomorrow's Worlds: The Unearthly History of Science Fiction", 
       'description':'2. Invasion', 
       'duration':3600}, 
      'params':{'skip_download': True}, 
      'skip':'Currently BBC iPlayer TV programmes are available to play in the UK only'},
     {'url':'http://www.bbc.co.uk/programmes/b04v20dw', 
      'info_dict':{'id':'b04v209v', 
       'ext':'flv', 
       'title':'Pete Tong, The Essential New Tune Special', 
       'description':"Pete has a very special mix - all of 2014's Essential New Tunes!", 
       'duration':10800}, 
      'params':{'skip_download': True}, 
      'skip':'Episode is no longer available on BBC iPlayer Radio'},
     {'url':'http://www.bbc.co.uk/music/clips/p022h44b', 
      'note':'Audio', 
      'info_dict':{'id':'p022h44j', 
       'ext':'flv', 
       'title':'BBC Proms Music Guides, Rachmaninov: Symphonic Dances', 
       'description':"In this Proms Music Guide, Andrew McGregor looks at Rachmaninov's Symphonic Dances.", 
       'duration':227}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.co.uk/music/clips/p025c0zz', 
      'note':'Video', 
      'info_dict':{'id':'p025c103', 
       'ext':'flv', 
       'title':'Reading and Leeds Festival, 2014, Rae Morris - Closer (Live on BBC Three)', 
       'description':'Rae Morris performs Closer for BBC Three at Reading 2014', 
       'duration':226}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.co.uk/iplayer/episode/b054fn09/ad/natural-world-20152016-2-super-powered-owls', 
      'info_dict':{'id':'p02n76xf', 
       'ext':'flv', 
       'title':'Natural World, 2015-2016: 2. Super Powered Owls', 
       'description':'md5:e4db5c937d0e95a7c6b5e654d429183d', 
       'duration':3540}, 
      'params':{'skip_download': True}, 
      'skip':'geolocation'},
     {'url':'http://www.bbc.co.uk/iplayer/episode/b05zmgwn/royal-academy-summer-exhibition', 
      'info_dict':{'id':'b05zmgw1', 
       'ext':'flv', 
       'description':'Kirsty Wark and Morgan Quaintance visit the Royal Academy as it prepares for its annual artistic extravaganza, meeting people who have come together to make the show unique.', 
       'title':'Royal Academy Summer Exhibition', 
       'duration':3540}, 
      'params':{'skip_download': True}, 
      'skip':'geolocation'},
     {'url':'http://www.bbc.co.uk/programmes/b06rkn85', 
      'info_dict':{'id':'b06rkms3', 
       'ext':'flv', 
       'title':"Best of the Mini-Mixes 2015: Part 3, Annie Mac's Friday Night - BBC Radio 1", 
       'description':"Annie has part three in the Best of the Mini-Mixes 2015, plus the year's Most Played!"}, 
      'params':{'skip_download': True}, 
      'skip':"Now it's really geo-restricted"},
     {'url':'http://www.bbc.co.uk/programmes/p028bfkf/player', 
      'info_dict':{'id':'p028bfkj', 
       'ext':'flv', 
       'title':'Extract from BBC documentary Look Stranger - Giant Leeks and Magic Brews', 
       'description':'Extract from BBC documentary Look Stranger - Giant Leeks and Magic Brews'}, 
      'params':{'skip_download': True}},
     {'url':'https://www.bbc.co.uk/sounds/play/m0007jzb', 
      'note':'Audio', 
      'info_dict':{'id':'m0007jz9', 
       'ext':'mp4', 
       'title':'BBC Proms, 2019, Prom 34: West–Eastern Divan Orchestra', 
       'description':'Live BBC Proms. West–Eastern Divan Orchestra with Daniel Barenboim and Martha Argerich.', 
       'duration':9840}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.co.uk/iplayer/playlist/p01dvks4', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/music/clips#p02frcc3', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/iplayer/cbeebies/episode/b0480276/bing-14-atchoo', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/radio/player/p03cchwf', 
      'only_matching':True},
     {'url':'https://www.bbc.co.uk/music/audiovideo/popular#p055bc55', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/programmes/w3csv1y9', 
      'only_matching':True},
     {'url':'https://www.bbc.co.uk/programmes/m00005xn', 
      'only_matching':True},
     {'url':'https://www.bbc.co.uk/programmes/w172w4dww1jqt5s', 
      'only_matching':True}]

    def _login(self):
        username, password = self._get_login_info()
        if username is None:
            return
        login_page = self._download_webpage(self._LOGIN_URL, None, 'Downloading signin page')
        login_form = self._hidden_inputs(login_page)
        login_form.update({'username':username, 
         'password':password})
        post_url = urljoin(self._LOGIN_URL, self._search_regex('<form[^>]+action=(["\\\'])(?P<url>.+?)\\1',
          login_page, 'post url',
          default=(self._LOGIN_URL), group='url'))
        response, urlh = self._download_webpage_handle(post_url,
          None, 'Logging in', data=(urlencode_postdata(login_form)), headers={'Referer': self._LOGIN_URL})
        if self._LOGIN_URL in urlh.geturl():
            error = clean_html(get_element_by_class('form-message', response))
            if error:
                raise ExtractorError(('Unable to login: %s' % error),
                  expected=True)
            raise ExtractorError('Unable to log in')

    def _real_initialize(self):
        self._login()

    class MediaSelectionError(Exception):

        def __init__(self, id):
            self.id = id

    def _extract_asx_playlist(self, connection, programme_id):
        asx = self._download_xml(connection.get('href'), programme_id, 'Downloading ASX playlist')
        return [ref.get('href') for ref in asx.findall('./Entry/ref')]

    def _extract_items(self, playlist):
        return playlist.findall('./{%s}item' % self._EMP_PLAYLIST_NS)

    def _extract_medias(self, media_selection):
        error = media_selection.get('result')
        if error:
            raise BBCCoUkIE.MediaSelectionError(error)
        return media_selection.get('media') or []

    def _extract_connections(self, media):
        return media.get('connection') or []

    def _get_subtitles(self, media, programme_id):
        subtitles = {}
        for connection in self._extract_connections(media):
            cc_url = url_or_none(connection.get('href'))
            if not cc_url:
                continue
            else:
                captions = self._download_xml(cc_url,
                  programme_id, 'Downloading captions', fatal=False)
            if not isinstance(captions, compat_etree_Element):
                continue
            else:
                subtitles['en'] = [
                 {'url':connection.get('href'), 
                  'ext':'ttml'}]
            break

        return subtitles

    def _raise_extractor_error(self, media_selection_error):
        raise ExtractorError(('%s returned error: %s' % (self.IE_NAME, media_selection_error.id)),
          expected=True)

    def _download_media_selector(self, programme_id):
        last_exception = None
        for media_set in self._MEDIA_SETS:
            try:
                return self._download_media_selector_url(self._MEDIA_SELECTOR_URL_TEMPL % (media_set, programme_id), programme_id)
            except BBCCoUkIE.MediaSelectionError as e:
                try:
                    if e.id in ('notukerror', 'geolocation', 'selectionunavailable'):
                        last_exception = e
                        continue
                    else:
                        self._raise_extractor_error(e)
                finally:
                    e = None
                    del e

        self._raise_extractor_error(last_exception)

    def _download_media_selector_url(self, url, programme_id=None):
        media_selection = self._download_json(url,
          programme_id, 'Downloading media selection JSON', expected_status=(403, 404))
        return self._process_media_selector(media_selection, programme_id)

    def _process_media_selector--- This code section failed: ---

 L. 356         0  BUILD_LIST_0          0 
                2  STORE_FAST               'formats'

 L. 357         4  LOAD_CONST               None
                6  STORE_FAST               'subtitles'

 L. 358         8  BUILD_LIST_0          0 
               10  STORE_FAST               'urls'

 L. 360     12_14  SETUP_LOOP          652  'to 652'
               16  LOAD_FAST                'self'
               18  LOAD_METHOD              _extract_medias
               20  LOAD_FAST                'media_selection'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  GET_ITER         
             26_0  COME_FROM           648  '648'
             26_1  COME_FROM           634  '634'
             26_2  COME_FROM           626  '626'
            26_28  FOR_ITER            650  'to 650'
               30  STORE_FAST               'media'

 L. 361        32  LOAD_FAST                'media'
               34  LOAD_METHOD              get
               36  LOAD_STR                 'kind'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  STORE_FAST               'kind'

 L. 362        42  LOAD_FAST                'kind'
               44  LOAD_CONST               ('video', 'audio')
               46  COMPARE_OP               in
            48_50  POP_JUMP_IF_FALSE   628  'to 628'

 L. 363        52  LOAD_GLOBAL              int_or_none
               54  LOAD_FAST                'media'
               56  LOAD_METHOD              get
               58  LOAD_STR                 'bitrate'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'bitrate'

 L. 364        66  LOAD_FAST                'media'
               68  LOAD_METHOD              get
               70  LOAD_STR                 'encoding'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  STORE_FAST               'encoding'

 L. 365        76  LOAD_GLOBAL              int_or_none
               78  LOAD_FAST                'media'
               80  LOAD_METHOD              get
               82  LOAD_STR                 'width'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'width'

 L. 366        90  LOAD_GLOBAL              int_or_none
               92  LOAD_FAST                'media'
               94  LOAD_METHOD              get
               96  LOAD_STR                 'height'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  STORE_FAST               'height'

 L. 367       104  LOAD_GLOBAL              int_or_none
              106  LOAD_FAST                'media'
              108  LOAD_METHOD              get
              110  LOAD_STR                 'media_file_size'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  STORE_FAST               'file_size'

 L. 368   118_120  SETUP_LOOP          648  'to 648'
              122  LOAD_FAST                'self'
              124  LOAD_METHOD              _extract_connections
              126  LOAD_FAST                'media'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  GET_ITER         
            132_0  COME_FROM           622  '622'
            132_1  COME_FROM           610  '610'
            132_2  COME_FROM           518  '518'
            132_3  COME_FROM           400  '400'
            132_4  COME_FROM           364  '364'
            132_5  COME_FROM           324  '324'
            132_6  COME_FROM           288  '288'
            132_7  COME_FROM           156  '156'
          132_134  FOR_ITER            624  'to 624'
              136  STORE_FAST               'connection'

 L. 369       138  LOAD_FAST                'connection'
              140  LOAD_METHOD              get
              142  LOAD_STR                 'href'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  STORE_FAST               'href'

 L. 370       148  LOAD_FAST                'href'
              150  LOAD_FAST                'urls'
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   158  'to 158'

 L. 371       156  CONTINUE            132  'to 132'
            158_0  COME_FROM           154  '154'

 L. 372       158  LOAD_FAST                'href'
              160  POP_JUMP_IF_FALSE   172  'to 172'

 L. 373       162  LOAD_FAST                'urls'
              164  LOAD_METHOD              append
              166  LOAD_FAST                'href'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  POP_TOP          
            172_0  COME_FROM           160  '160'

 L. 374       172  LOAD_FAST                'connection'
              174  LOAD_METHOD              get
              176  LOAD_STR                 'kind'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'conn_kind'

 L. 375       182  LOAD_FAST                'connection'
              184  LOAD_METHOD              get
              186  LOAD_STR                 'protocol'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  STORE_FAST               'protocol'

 L. 376       192  LOAD_FAST                'connection'
              194  LOAD_METHOD              get
              196  LOAD_STR                 'supplier'
              198  CALL_METHOD_1         1  '1 positional argument'
              200  STORE_FAST               'supplier'

 L. 377       202  LOAD_FAST                'connection'
              204  LOAD_METHOD              get
              206  LOAD_STR                 'transferFormat'
              208  CALL_METHOD_1         1  '1 positional argument'
              210  STORE_FAST               'transfer_format'

 L. 378       212  LOAD_FAST                'supplier'
              214  JUMP_IF_TRUE_OR_POP   222  'to 222'
              216  LOAD_FAST                'conn_kind'
              218  JUMP_IF_TRUE_OR_POP   222  'to 222'
              220  LOAD_FAST                'protocol'
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           214  '214'
              222  STORE_FAST               'format_id'

 L. 380       224  LOAD_FAST                'supplier'
              226  LOAD_STR                 'asx'
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   290  'to 290'

 L. 381       234  SETUP_LOOP          288  'to 288'
              236  LOAD_GLOBAL              enumerate
              238  LOAD_FAST                'self'
              240  LOAD_METHOD              _extract_asx_playlist
              242  LOAD_FAST                'connection'
              244  LOAD_FAST                'programme_id'
              246  CALL_METHOD_2         2  '2 positional arguments'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  GET_ITER         
            252_0  COME_FROM           284  '284'
              252  FOR_ITER            286  'to 286'
              254  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST               'i'
              258  STORE_FAST               'ref'

 L. 382       260  LOAD_FAST                'formats'
              262  LOAD_METHOD              append

 L. 383       264  LOAD_FAST                'ref'

 L. 384       266  LOAD_STR                 'ref%s_%s'
              268  LOAD_FAST                'i'
              270  LOAD_FAST                'format_id'
              272  BUILD_TUPLE_2         2 
              274  BINARY_MODULO    
              276  LOAD_CONST               ('url', 'format_id')
              278  BUILD_CONST_KEY_MAP_2     2 
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
              284  JUMP_BACK           252  'to 252'
              286  POP_BLOCK        
            288_0  COME_FROM_LOOP      234  '234'
              288  JUMP_BACK           132  'to 132'
            290_0  COME_FROM           230  '230'

 L. 386       290  LOAD_FAST                'transfer_format'
              292  LOAD_STR                 'dash'
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   326  'to 326'

 L. 387       300  LOAD_FAST                'formats'
              302  LOAD_METHOD              extend
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                _extract_mpd_formats

 L. 388       308  LOAD_FAST                'href'
              310  LOAD_FAST                'programme_id'
              312  LOAD_FAST                'format_id'
              314  LOAD_CONST               False
              316  LOAD_CONST               ('mpd_id', 'fatal')
              318  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          
              324  JUMP_BACK           132  'to 132'
            326_0  COME_FROM           296  '296'

 L. 389       326  LOAD_FAST                'transfer_format'
              328  LOAD_STR                 'hls'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   366  'to 366'

 L. 390       336  LOAD_FAST                'formats'
              338  LOAD_METHOD              extend
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                _extract_m3u8_formats

 L. 391       344  LOAD_FAST                'href'
              346  LOAD_FAST                'programme_id'
              348  LOAD_STR                 'mp4'
              350  LOAD_STR                 'm3u8_native'

 L. 392       352  LOAD_FAST                'format_id'
              354  LOAD_CONST               False
              356  LOAD_CONST               ('ext', 'entry_protocol', 'm3u8_id', 'fatal')
              358  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  POP_TOP          
              364  JUMP_BACK           132  'to 132'
            366_0  COME_FROM           332  '332'

 L. 393       366  LOAD_FAST                'transfer_format'
              368  LOAD_STR                 'hds'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   402  'to 402'

 L. 394       376  LOAD_FAST                'formats'
              378  LOAD_METHOD              extend
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                _extract_f4m_formats

 L. 395       384  LOAD_FAST                'href'
              386  LOAD_FAST                'programme_id'
              388  LOAD_FAST                'format_id'
              390  LOAD_CONST               False
              392  LOAD_CONST               ('f4m_id', 'fatal')
              394  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              396  CALL_METHOD_1         1  '1 positional argument'
              398  POP_TOP          
              400  JUMP_BACK           132  'to 132'
            402_0  COME_FROM           372  '372'

 L. 397       402  LOAD_FAST                'supplier'
          404_406  POP_JUMP_IF_TRUE    426  'to 426'
              408  LOAD_FAST                'bitrate'
          410_412  POP_JUMP_IF_FALSE   426  'to 426'

 L. 398       414  LOAD_FAST                'format_id'
              416  LOAD_STR                 '-%d'
              418  LOAD_FAST                'bitrate'
              420  BINARY_MODULO    
              422  INPLACE_ADD      
              424  STORE_FAST               'format_id'
            426_0  COME_FROM           410  '410'
            426_1  COME_FROM           404  '404'

 L. 400       426  LOAD_FAST                'format_id'

 L. 401       428  LOAD_FAST                'file_size'
              430  LOAD_CONST               ('format_id', 'filesize')
              432  BUILD_CONST_KEY_MAP_2     2 
              434  STORE_FAST               'fmt'

 L. 403       436  LOAD_FAST                'kind'
              438  LOAD_STR                 'video'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   468  'to 468'

 L. 404       446  LOAD_FAST                'fmt'
              448  LOAD_METHOD              update

 L. 405       450  LOAD_FAST                'width'

 L. 406       452  LOAD_FAST                'height'

 L. 407       454  LOAD_FAST                'bitrate'

 L. 408       456  LOAD_FAST                'encoding'
              458  LOAD_CONST               ('width', 'height', 'tbr', 'vcodec')
              460  BUILD_CONST_KEY_MAP_4     4 
              462  CALL_METHOD_1         1  '1 positional argument'
              464  POP_TOP          
              466  JUMP_FORWARD        486  'to 486'
            468_0  COME_FROM           442  '442'

 L. 411       468  LOAD_FAST                'fmt'
              470  LOAD_METHOD              update

 L. 412       472  LOAD_FAST                'bitrate'

 L. 413       474  LOAD_FAST                'encoding'

 L. 414       476  LOAD_STR                 'none'
              478  LOAD_CONST               ('abr', 'acodec', 'vcodec')
              480  BUILD_CONST_KEY_MAP_3     3 
              482  CALL_METHOD_1         1  '1 positional argument'
              484  POP_TOP          
            486_0  COME_FROM           466  '466'

 L. 416       486  LOAD_FAST                'protocol'
              488  LOAD_CONST               ('http', 'https')
              490  COMPARE_OP               in
          492_494  POP_JUMP_IF_FALSE   512  'to 512'

 L. 418       496  LOAD_FAST                'fmt'
              498  LOAD_METHOD              update

 L. 419       500  LOAD_STR                 'url'
              502  LOAD_FAST                'href'
              504  BUILD_MAP_1           1 
              506  CALL_METHOD_1         1  '1 positional argument'
              508  POP_TOP          
              510  JUMP_FORWARD        612  'to 612'
            512_0  COME_FROM           492  '492'

 L. 421       512  LOAD_FAST                'protocol'
              514  LOAD_STR                 'rtmp'
              516  COMPARE_OP               ==
              518  POP_JUMP_IF_FALSE_BACK   132  'to 132'

 L. 422       520  LOAD_FAST                'connection'
              522  LOAD_METHOD              get
              524  LOAD_STR                 'application'
              526  LOAD_STR                 'ondemand'
              528  CALL_METHOD_2         2  '2 positional arguments'
              530  STORE_FAST               'application'

 L. 423       532  LOAD_FAST                'connection'
              534  LOAD_METHOD              get
              536  LOAD_STR                 'authString'
              538  CALL_METHOD_1         1  '1 positional argument'
              540  STORE_FAST               'auth_string'

 L. 424       542  LOAD_FAST                'connection'
              544  LOAD_METHOD              get
              546  LOAD_STR                 'identifier'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  STORE_FAST               'identifier'

 L. 425       552  LOAD_FAST                'connection'
              554  LOAD_METHOD              get
              556  LOAD_STR                 'server'
              558  CALL_METHOD_1         1  '1 positional argument'
              560  STORE_FAST               'server'

 L. 426       562  LOAD_FAST                'fmt'
              564  LOAD_METHOD              update

 L. 427       566  LOAD_STR                 '%s://%s/%s?%s'
              568  LOAD_FAST                'protocol'
              570  LOAD_FAST                'server'
              572  LOAD_FAST                'application'
              574  LOAD_FAST                'auth_string'
              576  BUILD_TUPLE_4         4 
              578  BINARY_MODULO    

 L. 428       580  LOAD_FAST                'identifier'

 L. 429       582  LOAD_STR                 '%s?%s'
              584  LOAD_FAST                'application'
              586  LOAD_FAST                'auth_string'
              588  BUILD_TUPLE_2         2 
              590  BINARY_MODULO    

 L. 430       592  LOAD_STR                 'http://www.bbc.co.uk'

 L. 431       594  LOAD_STR                 'http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf'

 L. 432       596  LOAD_CONST               False

 L. 433       598  LOAD_STR                 'flv'
              600  LOAD_CONST               ('url', 'play_path', 'app', 'page_url', 'player_url', 'rtmp_live', 'ext')
              602  BUILD_CONST_KEY_MAP_7     7 
              604  CALL_METHOD_1         1  '1 positional argument'
              606  POP_TOP          
              608  JUMP_FORWARD        612  'to 612'

 L. 436       610  CONTINUE            132  'to 132'
            612_0  COME_FROM           608  '608'
            612_1  COME_FROM           510  '510'

 L. 437       612  LOAD_FAST                'formats'
              614  LOAD_METHOD              append
              616  LOAD_FAST                'fmt'
              618  CALL_METHOD_1         1  '1 positional argument'
              620  POP_TOP          
              622  JUMP_BACK           132  'to 132'
              624  POP_BLOCK        
              626  JUMP_BACK            26  'to 26'
            628_0  COME_FROM            48  '48'

 L. 438       628  LOAD_FAST                'kind'
              630  LOAD_STR                 'captions'
              632  COMPARE_OP               ==
              634  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 439       636  LOAD_FAST                'self'
              638  LOAD_METHOD              extract_subtitles
              640  LOAD_FAST                'media'
              642  LOAD_FAST                'programme_id'
              644  CALL_METHOD_2         2  '2 positional arguments'
              646  STORE_FAST               'subtitles'
            648_0  COME_FROM_LOOP      118  '118'
              648  JUMP_BACK            26  'to 26'
              650  POP_BLOCK        
            652_0  COME_FROM_LOOP       12  '12'

 L. 440       652  LOAD_FAST                'formats'
              654  LOAD_FAST                'subtitles'
              656  BUILD_TUPLE_2         2 
              658  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 610

    def _download_playlist(self, playlist_id):
        try:
            playlist = self._download_json('http://www.bbc.co.uk/programmes/%s/playlist.json' % playlist_id, playlist_id, 'Downloading playlist JSON')
            version = playlist.get('defaultAvailableVersion')
            if version:
                smp_config = version['smpConfig']
                title = smp_config['title']
                description = smp_config['summary']
                for item in smp_config['items']:
                    kind = item['kind']
                    if kind not in ('programme', 'radioProgramme'):
                        continue
                    else:
                        programme_id = item.get('vpid')
                        duration = int_or_none(item.get('duration'))
                        formats, subtitles = self._download_media_selector(programme_id)

                return (
                 programme_id, title, description, duration, formats, subtitles)
        except ExtractorError as ee:
            try:
                if not (isinstance(ee.cause, compat_HTTPError) and ee.cause.code == 404):
                    raise
            finally:
                ee = None
                del ee

        return self._process_legacy_playlist(playlist_id)

    def _process_legacy_playlist_url(self, url, display_id):
        playlist = self._download_legacy_playlist_url(url, display_id)
        return self._extract_from_legacy_playlist(playlist, display_id)

    def _process_legacy_playlist(self, playlist_id):
        return self._process_legacy_playlist_url('http://www.bbc.co.uk/iplayer/playlist/%s' % playlist_id, playlist_id)

    def _download_legacy_playlist_url(self, url, playlist_id=None):
        return self._download_xml(url, playlist_id, 'Downloading legacy playlist XML')

    def _extract_from_legacy_playlist(self, playlist, playlist_id):
        no_items = playlist.find('./{%s}noItems' % self._EMP_PLAYLIST_NS)
        if no_items is not None:
            reason = no_items.get('reason')
            if reason == 'preAvailability':
                msg = 'Episode %s is not yet available' % playlist_id
            elif reason == 'postAvailability':
                msg = 'Episode %s is no longer available' % playlist_id
            elif reason == 'noMedia':
                msg = 'Episode %s is not currently available' % playlist_id
            else:
                msg = 'Episode %s is not available: %s' % (playlist_id, reason)
            raise ExtractorError(msg, expected=True)
        for item in self._extract_items(playlist):
            kind = item.get('kind')
            if kind not in ('programme', 'radioProgramme'):
                continue
            else:
                title = playlist.find('./{%s}title' % self._EMP_PLAYLIST_NS).text
                description_el = playlist.find('./{%s}summary' % self._EMP_PLAYLIST_NS)
                description = description_el.text if description_el is not None else None

                def get_programme_id(item):

                    def get_from_attributes(item):
                        for p in ('identifier', 'group'):
                            value = item.get(p)
                            if value:
                                if re.match('^[pb][\\da-z]{7}$', value):
                                    return value

                    get_from_attributes(item)
                    mediator = item.find('./{%s}mediator' % self._EMP_PLAYLIST_NS)
                    if mediator is not None:
                        return get_from_attributes(mediator)

                programme_id = get_programme_id(item)
                duration = int_or_none(item.get('duration'))
            if programme_id:
                formats, subtitles = self._download_media_selector(programme_id)
            else:
                formats, subtitles = self._process_media_selector(item, playlist_id)
                programme_id = playlist_id

        return (programme_id, title, description, duration, formats, subtitles)

    def _real_extract(self, url):
        group_id = self._match_id(url)
        webpage = self._download_webpage(url, group_id, 'Downloading video page')
        error = self._search_regex('<div\\b[^>]+\\bclass=["\\\'](?:smp|playout)__message delta["\\\'][^>]*>\\s*([^<]+?)\\s*<',
          webpage,
          'error', default=None)
        if error:
            raise ExtractorError(error, expected=True)
        programme_id = None
        duration = None
        tviplayer = self._search_regex('mediator\\.bind\\(({.+?})\\s*,\\s*document\\.getElementById',
          webpage,
          'player', default=None)
        if tviplayer:
            player = self._parse_json(tviplayer, group_id).get('player', {})
            duration = int_or_none(player.get('duration'))
            programme_id = player.get('vpid')
        if not programme_id:
            programme_id = self._search_regex(('"vpid"\\s*:\\s*"(%s)"' % self._ID_REGEX),
              webpage, 'vpid', fatal=False, default=None)
        if programme_id:
            formats, subtitles = self._download_media_selector(programme_id)
            title = self._og_search_title(webpage, default=None) or self._html_search_regex(('<h2[^>]+id="parent-title"[^>]*>(.+?)</h2>',
                                                                                             '<div[^>]+class="info"[^>]*>\\s*<h1>(.+?)</h1>'), webpage, 'title')
            description = self._search_regex(('<p class="[^"]*medium-description[^"]*">([^<]+)</p>',
                                              '<div[^>]+class="info_+synopsis"[^>]*>([^<]+)</div>'),
              webpage,
              'description', default=None)
            if not description:
                description = self._html_search_meta('description', webpage)
        else:
            programme_id, title, description, duration, formats, subtitles = self._download_playlist(group_id)
        self._sort_formats(formats)
        return {'id':programme_id, 
         'title':title, 
         'description':description, 
         'thumbnail':self._og_search_thumbnail(webpage, default=None), 
         'duration':duration, 
         'formats':formats, 
         'subtitles':subtitles}


class BBCIE(BBCCoUkIE):
    IE_NAME = 'bbc'
    IE_DESC = 'BBC'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.(?:com|co\\.uk)/(?:[^/]+/)+(?P<id>[^/#?]+)'
    _MEDIA_SETS = [
     'mobile-tablet-main',
     'pc']
    _TESTS = [
     {'url':'http://www.bbc.com/news/world-europe-32668511', 
      'info_dict':{'id':'world-europe-32668511', 
       'title':'Russia stages massive WW2 parade', 
       'description':'md5:00ff61976f6081841f759a08bf78cc9c'}, 
      'playlist_count':2},
     {'url':'http://www.bbc.com/news/business-28299555', 
      'info_dict':{'id':'business-28299555', 
       'title':'Farnborough Airshow: Video highlights', 
       'description':'BBC reports and video highlights at the Farnborough Airshow.'}, 
      'playlist_count':9, 
      'skip':'Save time'},
     {'url':'http://www.bbc.co.uk/blogs/adamcurtis/entries/3662a707-0af9-3149-963f-47bea720b460', 
      'info_dict':{'id':'3662a707-0af9-3149-963f-47bea720b460', 
       'title':'BUGGER'}, 
      'playlist_count':18},
     {'url':'http://www.bbc.com/news/world-europe-32041533', 
      'info_dict':{'id':'p02mprgb', 
       'ext':'mp4', 
       'title':'Aerial footage showed the site of the crash in the Alps - courtesy BFM TV', 
       'description':'md5:2868290467291b37feda7863f7a83f54', 
       'duration':47, 
       'timestamp':1427219242, 
       'upload_date':'20150324'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/turkce/haberler/2015/06/150615_telabyad_kentin_cogu', 
      'info_dict':{'id':'150615_telabyad_kentin_cogu', 
       'ext':'mp4', 
       'title':"YPG: Tel Abyad'ın tamamı kontrolümüzde", 
       'description':'md5:33a4805a855c9baf7115fcbde57e7025', 
       'timestamp':1434397334, 
       'upload_date':'20150615'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/mundo/video_fotos/2015/06/150619_video_honduras_militares_hospitales_corrupcion_aw', 
      'info_dict':{'id':'150619_video_honduras_militares_hospitales_corrupcion_aw', 
       'ext':'mp4', 
       'title':'Honduras militariza sus hospitales por nuevo escándalo de corrupción', 
       'description':'md5:1525f17448c4ee262b64b8f0c9ce66c8', 
       'timestamp':1434713142, 
       'upload_date':'20150619'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/news/video_and_audio/must_see/33376376', 
      'info_dict':{'id':'p02w6qjc', 
       'ext':'mp4', 
       'title':'Judge Mindy Glazer: "I\'m sorry to see you here... I always wondered what happened to you"', 
       'duration':56, 
       'description':'Judge Mindy Glazer: "I\'m sorry to see you here... I always wondered what happened to you"'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/travel/story/20150625-sri-lankas-spicy-secret', 
      'info_dict':{'id':'p02q6gc4', 
       'ext':'flv', 
       'title':'Sri Lanka’s spicy secret', 
       'description':'As a new train line to Jaffna opens up the country’s north, travellers can experience a truly distinct slice of Tamil culture.', 
       'timestamp':1437674293, 
       'upload_date':'20150723'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/autos/story/20130513-hyundais-rock-star', 
      'info_dict':{'id':'p018zqqg', 
       'ext':'mp4', 
       'title':'Hyundai Santa Fe Sport: Rock star', 
       'description':'md5:b042a26142c4154a6e472933cf20793d', 
       'timestamp':1415867444, 
       'upload_date':'20141113'}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.co.uk/sport/live/olympics/36895975', 
      'info_dict':{'id':'p041vhd0', 
       'ext':'mp4', 
       'title':"Nigeria v Japan - Men's First Round", 
       'description':'Live coverage of the first round from Group B at the Amazonia Arena.', 
       'duration':7980, 
       'uploader':'BBC Sport', 
       'uploader_id':'bbc_sport'}, 
      'params':{'skip_download': True}, 
      'skip':'Georestricted to UK'},
     {'url':'http://www.bbc.com/sport/0/football/33653409', 
      'info_dict':{'id':'p02xycnp', 
       'ext':'mp4', 
       'title':'Transfers: Cristiano Ronaldo to Man Utd, Arsenal to spend?', 
       'description':"BBC Sport's David Ornstein has the latest transfer gossip, including rumours of a Manchester United return for Cristiano Ronaldo.", 
       'duration':140}, 
      'params':{'skip_download': True}},
     {'url':'http://www.bbc.com/sport/0/football/34475836', 
      'info_dict':{'id':'34475836', 
       'title':'Jurgen Klopp: Furious football from a witty and winning coach', 
       'description':'Fast-paced football, wit, wisdom and a ready smile - why Liverpool fans should come to love new boss Jurgen Klopp.'}, 
      'playlist_count':3},
     {'url':'http://www.bbc.co.uk/schoolreport/35744779', 
      'info_dict':{'id':'35744779', 
       'title':'School which breaks down barriers in Jerusalem'}, 
      'playlist_count':1},
     {'url':'http://www.bbc.com/weather/features/33601775', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/news/science-environment-33661876', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/sport/rowing/35908187', 
      'only_matching':True},
     {'url':'https://www.bbc.co.uk/bbcthree/clip/73d0bbd0-abc3-4cea-b3c0-cdae21905eb1', 
      'info_dict':{'id':'p06556y7', 
       'ext':'mp4', 
       'title':'Transfers: Cristiano Ronaldo to Man Utd, Arsenal to spend?', 
       'description':'md5:4b7dfd063d5a789a1512e99662be3ddd'}, 
      'params':{'skip_download': True}},
     {'url':'https://www.bbc.co.uk/radio/play/b0b9z4yl', 
      'info_dict':{'id':'b0b9z4vz', 
       'ext':'mp4', 
       'title':'Prom 6: An American in Paris and Turangalila', 
       'description':'md5:51cf7d6f5c8553f197e58203bc78dff8', 
       'uploader':'Radio 3', 
       'uploader_id':'bbc_radio_three'}},
     {'url':'http://www.bbc.co.uk/learningenglish/chinese/features/lingohack/ep-181227', 
      'info_dict':{'id':'p06w9tws', 
       'ext':'mp4', 
       'title':'md5:2fabf12a726603193a2879a055f72514', 
       'description':'Learn English words and phrases from this story'}, 
      'add_ie':[
       BBCCoUkIE.ie_key()]}]

    @classmethod
    def suitable(cls, url):
        EXCLUDE_IE = (BBCCoUkIE, BBCCoUkArticleIE, BBCCoUkIPlayerPlaylistIE, BBCCoUkPlaylistIE)
        if any((ie.suitable(url) for ie in EXCLUDE_IE)):
            return False
        return super(BBCIE, cls).suitable(url)

    def _extract_from_media_meta(self, media_meta, video_id):
        source_files = media_meta.get('sourceFiles')
        if source_files:
            return (
             [{'url':f['url'],  'format_id':format_id,  'ext':f.get('encoding'),  'tbr':float_or_none(f.get('bitrate'), 1000),  'filesize':int_or_none(f.get('filesize'))} for format_id, f in source_files.items() if f.get('url')], [])
        programme_id = media_meta.get('externalId')
        if programme_id:
            return self._download_media_selector(programme_id)
        href = media_meta.get('href')
        if href:
            playlist = self._download_legacy_playlist_url(href)
            _, _, _, _, formats, subtitles = self._extract_from_legacy_playlist(playlist, video_id)
            return (
             formats, subtitles)
        return ([], [])

    def _extract_from_playlist_sxml(self, url, playlist_id, timestamp):
        programme_id, title, description, duration, formats, subtitles = self._process_legacy_playlist_url(url, playlist_id)
        self._sort_formats(formats)
        return {'id':programme_id, 
         'title':title, 
         'description':description, 
         'duration':duration, 
         'timestamp':timestamp, 
         'formats':formats, 
         'subtitles':subtitles}

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)
        json_ld_info = self._search_json_ld(webpage, playlist_id, default={})
        timestamp = json_ld_info.get('timestamp')
        playlist_title = json_ld_info.get('title')
        if not playlist_title:
            playlist_title = self._og_search_title(webpage,
              default=None) or self._html_search_regex('<title>(.+?)</title>',
              webpage, 'playlist title', default=None)
            if playlist_title:
                playlist_title = re.sub('(.+)\\s*-\\s*BBC.*?$', '\\1', playlist_title).strip()
        playlist_description = json_ld_info.get('description') or self._og_search_description(webpage, default=None)
        if not timestamp:
            timestamp = parse_iso8601(self._search_regex([
             '<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
             'itemprop="datePublished"[^>]+datetime="([^"]+)"',
             '"datePublished":\\s*"([^"]+)'],
              webpage,
              'date', default=None))
        entries = []
        playlists = re.findall('<param[^>]+name="playlist"[^>]+value="([^"]+)"', webpage)
        playlists.extend(re.findall('data-media-id="([^"]+/playlist\\.sxml)"', webpage))
        if playlists:
            entries = [self._extract_from_playlist_sxml(playlist_url, playlist_id, timestamp) for playlist_url in playlists]
        data_playables = re.findall('data-playable=(["\\\'])({.+?})\\1', webpage)
        if data_playables:
            for _, data_playable_json in data_playables:
                data_playable = self._parse_json((unescapeHTML(data_playable_json)),
                  playlist_id, fatal=False)
                if not data_playable:
                    continue
                else:
                    settings = data_playable.get('settings', {})
                if settings:
                    playlist_object = settings.get('playlistObject', {})
                if playlist_object:
                    items = playlist_object.get('items')
                    if items and isinstance(items, list):
                        title = playlist_object['title']
                        description = playlist_object.get('summary')
                        duration = int_or_none(items[0].get('duration'))
                        programme_id = items[0].get('vpid')
                        formats, subtitles = self._download_media_selector(programme_id)
                        self._sort_formats(formats)
                        entries.append({'id':programme_id, 
                         'title':title, 
                         'description':description, 
                         'timestamp':timestamp, 
                         'duration':duration, 
                         'formats':formats, 
                         'subtitles':subtitles})
                    else:
                        playlist = data_playable.get('otherSettings', {}).get('playlist', {})
                        if playlist:
                            entry = None
                            for key in ('streaming', 'progressiveDownload'):
                                playlist_url = playlist.get('%sUrl' % key)
                                if not playlist_url:
                                    continue
                                try:
                                    info = self._extract_from_playlist_sxml(playlist_url, playlist_id, timestamp)
                                    if not entry:
                                        entry = info
                                    else:
                                        entry['title'] = info['title']
                                        entry['formats'].extend(info['formats'])
                                except Exception as e:
                                    try:
                                        if isinstance(e.cause, compat_HTTPError):
                                            if e.cause.code == 500:
                                                continue
                                        raise
                                    finally:
                                        e = None
                                        del e

                            if entry:
                                self._sort_formats(entry['formats'])
                                entries.append(entry)

        if entries:
            return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)
        group_id = self._search_regex(('<div[^>]+\\bclass=["\\\']video["\\\'][^>]+\\bdata-pid=["\\\'](%s)' % self._ID_REGEX),
          webpage,
          'group id', default=None)
        if group_id:
            return self.url_result(('https://www.bbc.co.uk/programmes/%s' % group_id),
              ie=(BBCCoUkIE.ie_key()))
        programme_id = self._search_regex([
         'data-(?:video-player|media)-vpid="(%s)"' % self._ID_REGEX,
         '<param[^>]+name="externalIdentifier"[^>]+value="(%s)"' % self._ID_REGEX,
         'videoId\\s*:\\s*["\\\'](%s)["\\\']' % self._ID_REGEX],
          webpage,
          'vpid', default=None)
        if programme_id:
            formats, subtitles = self._download_media_selector(programme_id)
            self._sort_formats(formats)
            digital_data = self._parse_json(self._search_regex('var\\s+digitalData\\s*=\\s*({.+?});?\\n',
              webpage, 'digital data', default='{}'),
              programme_id,
              fatal=False)
            page_info = digital_data.get('page', {}).get('pageInfo', {})
            title = page_info.get('pageName') or self._og_search_title(webpage)
            description = page_info.get('description') or self._og_search_description(webpage)
            timestamp = parse_iso8601(page_info.get('publicationDate')) or timestamp
            return {'id':programme_id, 
             'title':title, 
             'description':description, 
             'timestamp':timestamp, 
             'formats':formats, 
             'subtitles':subtitles}
        morph_payload = self._parse_json(self._search_regex('Morph\\.setPayload\\([^,]+,\\s*({.+?})\\);',
          webpage,
          'morph payload', default='{}'),
          playlist_id,
          fatal=False)
        if morph_payload:
            components = try_get(morph_payload, lambda x: x['body']['components'], list) or []
            for component in components:
                if not isinstance(component, dict):
                    continue
                else:
                    lead_media = try_get(component, lambda x: x['props']['leadMedia'], dict)
                if not lead_media:
                    continue
                else:
                    identifiers = lead_media.get('identifiers')
                if identifiers:
                    if not isinstance(identifiers, dict):
                        continue
                    else:
                        programme_id = identifiers.get('vpid') or identifiers.get('playablePid')
                    if not programme_id:
                        continue
                    else:
                        title = lead_media.get('title') or self._og_search_title(webpage)
                        formats, subtitles = self._download_media_selector(programme_id)
                        self._sort_formats(formats)
                        description = lead_media.get('summary')
                        uploader = lead_media.get('masterBrand')
                        uploader_id = lead_media.get('mid')
                        duration = None
                        duration_d = lead_media.get('duration')
                        if isinstance(duration_d, dict):
                            duration = parse_duration(dict_get(duration_d, ('rawDuration',
                                                                            'formattedDuration',
                                                                            'spokenDuration')))
                    return {'id':programme_id,  'title':title, 
                     'description':description, 
                     'duration':duration, 
                     'uploader':uploader, 
                     'uploader_id':uploader_id, 
                     'formats':formats, 
                     'subtitles':subtitles}

        preload_state = self._parse_json(self._search_regex('window\\.__PRELOADED_STATE__\\s*=\\s*({.+?});',
          webpage, 'preload state',
          default='{}'),
          playlist_id, fatal=False)
        if preload_state:
            current_programme = preload_state.get('programmes', {}).get('current') or {}
            programme_id = current_programme.get('id')
            if not current_programme and programme_id or current_programme.get('type') == 'playable_item':
                title = current_programme.get('titles', {}).get('tertiary') or playlist_title
                formats, subtitles = self._download_media_selector(programme_id)
                self._sort_formats(formats)
                synopses = current_programme.get('synopses') or {}
                network = current_programme.get('network') or {}
                duration = int_or_none(current_programme.get('duration', {}).get('value'))
                thumbnail = None
                image_url = current_programme.get('image_url')
                if image_url:
                    thumbnail = image_url.replace('{recipe}', '1920x1920')
                return {'id':programme_id, 
                 'title':title, 
                 'description':dict_get(synopses, ('long', 'medium', 'short')), 
                 'thumbnail':thumbnail, 
                 'duration':duration, 
                 'uploader':network.get('short_title'), 
                 'uploader_id':network.get('id'), 
                 'formats':formats, 
                 'subtitles':subtitles}
        bbc3_config = self._parse_json(self._search_regex('(?s)bbcthreeConfig\\s*=\\s*({.+?})\\s*;\\s*<',
          webpage, 'bbcthree config',
          default='{}'),
          playlist_id,
          transform_source=js_to_json, fatal=False) or {}
        payload = bbc3_config.get('payload') or {}
        if payload:
            clip = payload.get('currentClip') or {}
            clip_vpid = clip.get('vpid')
            clip_title = clip.get('title')
            if clip_vpid:
                if clip_title:
                    formats, subtitles = self._download_media_selector(clip_vpid)
                    self._sort_formats(formats)
                    return {'id':clip_vpid, 
                     'title':clip_title, 
                     'thumbnail':dict_get(clip, ('poster', 'imageUrl')), 
                     'description':clip.get('description'), 
                     'duration':parse_duration(clip.get('duration')), 
                     'formats':formats, 
                     'subtitles':subtitles}
            bbc3_playlist = try_get(payload, lambda x: x['content']['bbcMedia']['playlist'], dict)
            if bbc3_playlist:
                playlist_title = bbc3_playlist.get('title') or playlist_title
                thumbnail = bbc3_playlist.get('holdingImageURL')
                entries = []
                for bbc3_item in bbc3_playlist['items']:
                    programme_id = bbc3_item.get('versionID')
                    if not programme_id:
                        continue
                    else:
                        formats, subtitles = self._download_media_selector(programme_id)
                        self._sort_formats(formats)
                        entries.append({'id':programme_id, 
                         'title':playlist_title, 
                         'thumbnail':thumbnail, 
                         'timestamp':timestamp, 
                         'formats':formats, 
                         'subtitles':subtitles})

                return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)
        initial_data = self._parse_json(self._search_regex('window\\.__INITIAL_DATA__\\s*=\\s*({.+?});',
          webpage, 'preload state',
          default='{}'),
          playlist_id, fatal=False)
        if initial_data:

            def parse_media(media):
                if not media:
                    return
                for item in try_get(media, lambda x: x['media']['items'], list) or []:
                    item_id = item.get('id')
                    item_title = item.get('title')
                    if item_id:
                        if not item_title:
                            continue
                        else:
                            formats, subtitles = self._download_media_selector(item_id)
                            self._sort_formats(formats)
                            entries.append({'id':item_id, 
                             'title':item_title, 
                             'thumbnail':item.get('holdingImageUrl'), 
                             'formats':formats, 
                             'subtitles':subtitles})

            for resp in (initial_data.get('data') or {}).values():
                name = resp.get('name')
                if name == 'media-experience':
                    parse_media(try_get(resp, lambda x: x['data']['initialItem']['mediaItem'], dict))
                if name == 'article':
                    for block in try_get(resp, lambda x: x['data']['blocks'], list) or []:
                        if block.get('type') != 'media':
                            continue
                        else:
                            parse_media(block.get('model'))

            return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)

        def extract_all(pattern):
            return list(filter(None, map(lambda s: self._parse_json(s, playlist_id, fatal=False), re.findall(pattern, webpage))))

        EMBED_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/(?:[^/]+/)+%s(?:\\b[^"]+)?' % self._ID_REGEX
        entries = []
        for match in extract_all('new\\s+SMP\\(({.+?})\\)'):
            embed_url = match.get('playerSettings', {}).get('externalEmbedUrl')
            if embed_url:
                if re.match(EMBED_URL, embed_url):
                    entries.append(embed_url)

        entries.extend(re.findall('setPlaylist\\("(%s)"\\)' % EMBED_URL, webpage))
        if entries:
            return self.playlist_result([self.url_result(entry_, 'BBCCoUk') for entry_ in entries], playlist_id, playlist_title, playlist_description)
        medias = extract_all("data-media-meta='({[^']+})'")
        if not medias:
            media_asset = self._search_regex('mediaAssetPage\\.init\\(\\s*({.+?}), "/',
              webpage,
              'media asset', default=None)
            if media_asset:
                media_asset_page = self._parse_json(media_asset, playlist_id, fatal=False)
                medias = []
                for video in media_asset_page.get('videos', {}).values():
                    medias.extend(video.values())

        if not medias:
            vxp_playlist = self._parse_json(self._search_regex('<script[^>]+class="vxp-playlist-data"[^>]+type="application/json"[^>]*>([^<]+)</script>', webpage, 'playlist data'), playlist_id)
            playlist_medias = []
            for item in vxp_playlist:
                media = item.get('media')
                if not media:
                    continue
                else:
                    playlist_medias.append(media)
                if item.get('advert', {}).get('assetId') == playlist_id:
                    medias = [
                     media]
                    break

            if not medias:
                medias = playlist_medias
            entries = []
            for num, media_meta in enumerate(medias, start=1):
                formats, subtitles = self._extract_from_media_meta(media_meta, playlist_id)
                if not formats:
                    continue
                else:
                    self._sort_formats(formats)
                    video_id = media_meta.get('externalId')
                    if not video_id:
                        video_id = playlist_id if len(medias) == 1 else '%s-%s' % (playlist_id, num)
                    title = media_meta.get('caption')
                    if not title:
                        title = playlist_title if len(medias) == 1 else '%s - Video %s' % (playlist_title, num)
                    duration = int_or_none(media_meta.get('durationInSeconds')) or parse_duration(media_meta.get('duration'))
                    images = []
                    for image in media_meta.get('images', {}).values():
                        images.extend(image.values())

                    if 'image' in media_meta:
                        images.append(media_meta['image'])
                    thumbnails = [{'url':image.get('href'),  'width':int_or_none(image.get('width')),  'height':int_or_none(image.get('height'))} for image in images]
                    entries.append({'id':video_id, 
                     'title':title, 
                     'thumbnails':thumbnails, 
                     'duration':duration, 
                     'timestamp':timestamp, 
                     'formats':formats, 
                     'subtitles':subtitles})

            return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)


class BBCCoUkArticleIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/articles/(?P<id>[a-zA-Z0-9]+)'
    IE_NAME = 'bbc.co.uk:article'
    IE_DESC = 'BBC articles'
    _TEST = {'url':'http://www.bbc.co.uk/programmes/articles/3jNQLTMrPlYGTBn0WV6M2MS/not-your-typical-role-model-ada-lovelace-the-19th-century-programmer', 
     'info_dict':{'id':'3jNQLTMrPlYGTBn0WV6M2MS', 
      'title':'Calculating Ada: The Countess of Computing - Not your typical role model: Ada Lovelace the 19th century programmer - BBC Four', 
      'description':'Hannah Fry reveals some of her surprising discoveries about Ada Lovelace during filming.'}, 
     'playlist_count':4, 
     'add_ie':[
      'BBCCoUk']}

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)
        title = self._og_search_title(webpage)
        description = self._og_search_description(webpage).strip()
        entries = [self.url_result(programme_url) for programme_url in re.findall('<div[^>]+typeof="Clip"[^>]+resource="([^"]+)"', webpage)]
        return self.playlist_result(entries, playlist_id, title, description)


class BBCCoUkPlaylistBaseIE(InfoExtractor):

    def _entries(self, webpage, url, playlist_id):
        single_page = 'page' in compat_urlparse.parse_qs(compat_urlparse.urlparse(url).query)
        for page_num in itertools.count(2):
            for video_id in re.findall(self._VIDEO_ID_TEMPLATE % BBCCoUkIE._ID_REGEX, webpage):
                yield self.url_result(self._URL_TEMPLATE % video_id, BBCCoUkIE.ie_key())

            if single_page:
                return
            next_page = self._search_regex('<li[^>]+class=(["\\\'])pagination_+next\\1[^>]*><a[^>]+href=(["\\\'])(?P<url>(?:(?!\\2).)+)\\2',
              webpage,
              'next page url', default=None, group='url')
            if not next_page:
                break
            else:
                webpage = self._download_webpage(compat_urlparse.urljoin(url, next_page), playlist_id, 'Downloading page %d' % page_num, page_num)

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)
        title, description = self._extract_title_and_description(webpage)
        return self.playlist_result(self._entries(webpage, url, playlist_id), playlist_id, title, description)


class BBCCoUkIPlayerPlaylistIE(BBCCoUkPlaylistBaseIE):
    IE_NAME = 'bbc.co.uk:iplayer:playlist'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/iplayer/(?:episodes|group)/(?P<id>%s)' % BBCCoUkIE._ID_REGEX
    _URL_TEMPLATE = 'http://www.bbc.co.uk/iplayer/episode/%s'
    _VIDEO_ID_TEMPLATE = 'data-ip-id=["\\\'](%s)'
    _TESTS = [
     {'url':'http://www.bbc.co.uk/iplayer/episodes/b05rcz9v', 
      'info_dict':{'id':'b05rcz9v', 
       'title':'The Disappearance', 
       'description':'French thriller serial about a missing teenager.'}, 
      'playlist_mincount':6, 
      'skip':'This programme is not currently available on BBC iPlayer'},
     {'url':'http://www.bbc.co.uk/iplayer/group/p02tcc32', 
      'info_dict':{'id':'p02tcc32', 
       'title':'Bohemian Icons', 
       'description':'md5:683e901041b2fe9ba596f2ab04c4dbe7'}, 
      'playlist_mincount':10}]

    def _extract_title_and_description(self, webpage):
        title = self._search_regex('<h1>([^<]+)</h1>', webpage, 'title', fatal=False)
        description = self._search_regex('<p[^>]+class=(["\\\'])subtitle\\1[^>]*>(?P<value>[^<]+)</p>',
          webpage,
          'description', fatal=False, group='value')
        return (
         title, description)


class BBCCoUkPlaylistIE(BBCCoUkPlaylistBaseIE):
    IE_NAME = 'bbc.co.uk:playlist'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/programmes/(?P<id>%s)/(?:episodes|broadcasts|clips)' % BBCCoUkIE._ID_REGEX
    _URL_TEMPLATE = 'http://www.bbc.co.uk/programmes/%s'
    _VIDEO_ID_TEMPLATE = 'data-pid=["\\\'](%s)'
    _TESTS = [
     {'url':'http://www.bbc.co.uk/programmes/b05rcz9v/clips', 
      'info_dict':{'id':'b05rcz9v', 
       'title':'The Disappearance - Clips - BBC Four', 
       'description':'French thriller serial about a missing teenager.'}, 
      'playlist_mincount':7},
     {'url':'http://www.bbc.co.uk/programmes/b00mfl7n/clips?page=1', 
      'info_dict':{'id':'b00mfl7n', 
       'title':'Frozen Planet - Clips - BBC One', 
       'description':'md5:65dcbf591ae628dafe32aa6c4a4a0d8c'}, 
      'playlist_mincount':24},
     {'url':'http://www.bbc.co.uk/programmes/b00mfl7n/clips', 
      'info_dict':{'id':'b00mfl7n', 
       'title':'Frozen Planet - Clips - BBC One', 
       'description':'md5:65dcbf591ae628dafe32aa6c4a4a0d8c'}, 
      'playlist_mincount':142},
     {'url':'http://www.bbc.co.uk/programmes/b05rcz9v/broadcasts/2016/06', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/programmes/b05rcz9v/clips', 
      'only_matching':True},
     {'url':'http://www.bbc.co.uk/programmes/b055jkys/episodes/player', 
      'only_matching':True}]

    def _extract_title_and_description(self, webpage):
        title = self._og_search_title(webpage, fatal=False)
        description = self._og_search_description(webpage)
        return (
         title, description)