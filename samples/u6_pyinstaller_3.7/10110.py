# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\tvnow.py
from __future__ import unicode_literals
import re
from .common import InfoExtractor
from ..compat import compat_str
from ..utils import ExtractorError, int_or_none, parse_iso8601, parse_duration, str_or_none, update_url_query, urljoin

class TVNowBaseIE(InfoExtractor):
    _VIDEO_FIELDS = ('id', 'title', 'free', 'geoblocked', 'articleLong', 'articleShort',
                     'broadcastStartDate', 'isDrm', 'duration', 'season', 'episode',
                     'manifest.dashclear', 'manifest.hlsclear', 'manifest.smoothclear',
                     'format.title', 'format.defaultImage169Format', 'format.defaultImage169Logo')

    def _call_api(self, path, video_id, query):
        return self._download_json(('https://api.tvnow.de/v3/' + path),
          video_id, query=query)

    def _extract_video(self, info, display_id):
        video_id = compat_str(info['id'])
        title = info['title']
        paths = []
        for manifest_url in (info.get('manifest') or {}).values():
            if not manifest_url:
                continue
            manifest_url = update_url_query(manifest_url, {'filter': ''})
            path = self._search_regex('https?://[^/]+/(.+?)\\.ism/', manifest_url, 'path')
            if path in paths:
                continue
            paths.append(path)

            def url_repl(proto, suffix):
                return re.sub('(?:hls|dash|hss)([.-])', proto + '\\1', re.sub('\\.ism/(?:[^.]*\\.(?:m3u8|mpd)|[Mm]anifest)', '.ism/' + suffix, manifest_url))

            def make_urls(proto, suffix):
                urls = [
                 url_repl(proto, suffix)]
                hd_url = urls[0].replace('/manifest/', '/ngvod/')
                if hd_url != urls[0]:
                    urls.append(hd_url)
                return urls

            for man_url in make_urls('dash', '.mpd'):
                formats = self._extract_mpd_formats(man_url,
                  video_id, mpd_id='dash', fatal=False)

            for man_url in make_urls('hss', 'Manifest'):
                formats.extend(self._extract_ism_formats(man_url,
                  video_id, ism_id='mss', fatal=False))

            for man_url in make_urls('hls', '.m3u8'):
                formats.extend(self._extract_m3u8_formats(man_url,
                  video_id, 'mp4', 'm3u8_native', m3u8_id='hls', fatal=False))

            if formats:
                break
        else:
            if info.get('isDrm'):
                raise ExtractorError(('Video %s is DRM protected' % video_id),
                  expected=True)
            else:
                if info.get('geoblocked'):
                    raise self.raise_geo_restricted()
                raise info.get('free', True) or ExtractorError(('Video %s is not available for free' % video_id),
                  expected=True)

        self._sort_formats(formats)
        description = info.get('articleLong') or info.get('articleShort')
        timestamp = parse_iso8601(info.get('broadcastStartDate'), ' ')
        duration = parse_duration(info.get('duration'))
        f = info.get('format', {})
        thumbnails = [
         {'url': 'https://aistvnow-a.akamaihd.net/tvnow/movie/%s' % video_id}]
        thumbnail = f.get('defaultImage169Format') or f.get('defaultImage169Logo')
        if thumbnail:
            thumbnails.append({'url': thumbnail})
        return {'id':video_id, 
         'display_id':display_id, 
         'title':title, 
         'description':description, 
         'thumbnails':thumbnails, 
         'timestamp':timestamp, 
         'duration':duration, 
         'series':f.get('title'), 
         'season_number':int_or_none(info.get('season')), 
         'episode_number':int_or_none(info.get('episode')), 
         'episode':title, 
         'formats':formats}


class TVNowIE(TVNowBaseIE):
    _VALID_URL = '(?x)\n                    https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/(?P<station>[^/]+)/\n                        (?P<show_id>[^/]+)/\n                        (?!(?:list|jahr)(?:/|$))(?P<id>[^/?\\#&]+)\n                    '

    @classmethod
    def suitable--- This code section failed: ---

 L. 121         0  LOAD_GLOBAL              TVNowNewIE
                2  LOAD_METHOD              suitable
                4  LOAD_FAST                'url'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_TRUE     40  'to 40'
               10  LOAD_GLOBAL              TVNowSeasonIE
               12  LOAD_METHOD              suitable
               14  LOAD_FAST                'url'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_TRUE     40  'to 40'
               20  LOAD_GLOBAL              TVNowAnnualIE
               22  LOAD_METHOD              suitable
               24  LOAD_FAST                'url'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_JUMP_IF_TRUE     40  'to 40'
               30  LOAD_GLOBAL              TVNowShowIE
               32  LOAD_METHOD              suitable
               34  LOAD_FAST                'url'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_FALSE    44  'to 44'
             40_0  COME_FROM            28  '28'
             40_1  COME_FROM            18  '18'
             40_2  COME_FROM             8  '8'
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 122        44  LOAD_GLOBAL              super
               46  LOAD_GLOBAL              TVNowIE
               48  LOAD_FAST                'cls'
               50  CALL_FUNCTION_2       2  '2 positional arguments'
               52  LOAD_METHOD              suitable
               54  LOAD_FAST                'url'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 58

    _TESTS = [
     {'url':'https://www.tvnow.de/rtl2/grip-das-motormagazin/der-neue-porsche-911-gt-3/player', 
      'info_dict':{'id':'331082', 
       'display_id':'grip-das-motormagazin/der-neue-porsche-911-gt-3', 
       'ext':'mp4', 
       'title':'Der neue Porsche 911 GT 3', 
       'description':'md5:6143220c661f9b0aae73b245e5d898bb', 
       'timestamp':1495994400, 
       'upload_date':'20170528', 
       'duration':5283, 
       'series':'GRIP - Das Motormagazin', 
       'season_number':14, 
       'episode_number':405, 
       'episode':'Der neue Porsche 911 GT 3'}},
     {'url':'https://www.tvnow.de/rtl2/armes-deutschland/episode-0008/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/nitro/alarm-fuer-cobra-11-die-autobahnpolizei/auf-eigene-faust-pilot/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/superrtl/die-lustigsten-schlamassel-der-welt/u-a-ketchup-effekt/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/ntv/startup-news/goetter-in-weiss/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/vox/auto-mobil/neues-vom-automobilmarkt-2017-11-19-17-00-00/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/rtlplus/op-ruft-dr-bruckner/die-vernaehte-frau/player', 
      'only_matching':True},
     {'url':'https://www.tvnow.de/rtl2/grip-das-motormagazin/der-neue-porsche-911-gt-3', 
      'only_matching':True}]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        display_id = '%s/%s' % mobj.group(2, 3)
        info = self._call_api(('movies/' + display_id),
          display_id, query={'fields': ','.join(self._VIDEO_FIELDS)})
        return self._extract_video(info, display_id)


class TVNowNewIE(InfoExtractor):
    _VALID_URL = '(?x)\n                    (?P<base_url>https?://\n                        (?:www\\.)?tvnow\\.(?:de|at|ch)/\n                        (?:shows|serien))/\n                        (?P<show>[^/]+)-\\d+/\n                        [^/]+/\n                        episode-\\d+-(?P<episode>[^/?$&]+)-(?P<id>\\d+)\n                    '
    _TESTS = [
     {'url':'https://www.tvnow.de/shows/grip-das-motormagazin-1669/2017-05/episode-405-der-neue-porsche-911-gt-3-331082', 
      'only_matching':True}]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        base_url = re.sub('(?:shows|serien)', '_', mobj.group('base_url'))
        show, episode = mobj.group('show', 'episode')
        return self.url_result(('%s/%s/%s' % (base_url, show, episode)),
          ie=(TVNowIE.ie_key()),
          video_id=(mobj.group('id')))


class TVNowNewBaseIE(InfoExtractor):

    def _call_api(self, path, video_id, query={}):
        result = self._download_json(('https://apigw.tvnow.de/module/' + path),
          video_id, query=query)
        error = result.get('error')
        if error:
            raise ExtractorError(('%s said: %s' % (self.IE_NAME, error)),
              expected=True)
        return result


class TVNowListBaseIE(TVNowNewBaseIE):
    _SHOW_VALID_URL = '(?x)\n                    (?P<base_url>\n                        https?://\n                            (?:www\\.)?tvnow\\.(?:de|at|ch)/(?:shows|serien)/\n                            [^/?#&]+-(?P<show_id>\\d+)\n                    )\n                    '

    @classmethod
    def suitable(cls, url):
        if TVNowNewIE.suitable(url):
            return False
        return super(TVNowListBaseIE, cls).suitable(url)

    def _extract_items(self, url, show_id, list_id, query):
        items = self._call_api(('teaserrow/format/episode/' + show_id),
          list_id, query=query)['items']
        entries = []
        for item in items:
            if not isinstance(item, dict):
                continue
            item_url = urljoin(url, item.get('url'))
            if not item_url:
                continue
            video_id = str_or_none(item.get('id') or item.get('videoId'))
            item_title = item.get('subheadline') or item.get('text')
            entries.append(self.url_result(item_url,
              ie=(TVNowNewIE.ie_key()), video_id=video_id, video_title=item_title))

        return self.playlist_result(entries, '%s/%s' % (show_id, list_id))


class TVNowSeasonIE(TVNowListBaseIE):
    _VALID_URL = '%s/staffel-(?P<id>\\d+)' % TVNowListBaseIE._SHOW_VALID_URL
    _TESTS = [
     {'url':'https://www.tvnow.de/serien/alarm-fuer-cobra-11-die-autobahnpolizei-1815/staffel-13', 
      'info_dict':{'id': '1815/13'}, 
      'playlist_mincount':22}]

    def _real_extract(self, url):
        _, show_id, season_id = re.match(self._VALID_URL, url).groups()
        return self._extract_items(url, show_id, season_id, {'season': season_id})


class TVNowAnnualIE(TVNowListBaseIE):
    _VALID_URL = '%s/(?P<year>\\d{4})-(?P<month>\\d{2})' % TVNowListBaseIE._SHOW_VALID_URL
    _TESTS = [
     {'url':'https://www.tvnow.de/shows/grip-das-motormagazin-1669/2017-05', 
      'info_dict':{'id': '1669/2017-05'}, 
      'playlist_mincount':2}]

    def _real_extract(self, url):
        _, show_id, year, month = re.match(self._VALID_URL, url).groups()
        return self._extract_items(url, show_id, '%s-%s' % (year, month), {'year':int(year), 
         'month':int(month)})


class TVNowShowIE(TVNowListBaseIE):
    _VALID_URL = TVNowListBaseIE._SHOW_VALID_URL
    _TESTS = [
     {'url':'https://www.tvnow.de/shows/grip-das-motormagazin-1669', 
      'info_dict':{'id': '1669'}, 
      'playlist_mincount':73},
     {'url':'https://www.tvnow.de/shows/armes-deutschland-11471', 
      'info_dict':{'id': '11471'}, 
      'playlist_mincount':3}]

    @classmethod
    def suitable(cls, url):
        if TVNowNewIE.suitable(url) or TVNowSeasonIE.suitable(url) or TVNowAnnualIE.suitable(url):
            return False
        return super(TVNowShowIE, cls).suitable(url)

    def _real_extract(self, url):
        base_url, show_id = re.match(self._VALID_URL, url).groups()
        result = self._call_api('teaserrow/format/navigation/' + show_id, show_id)
        items = result['items']
        entries = []
        navigation = result.get('navigationType')
        if navigation == 'annual':
            for item in items:
                if not isinstance(item, dict):
                    continue
                year = int_or_none(item.get('year'))
                if year is None:
                    continue
                months = item.get('months')
                if not isinstance(months, list):
                    continue
                for month_dict in months:
                    if isinstance(month_dict, dict):
                        if not month_dict:
                            continue
                        month_number = int_or_none(list(month_dict.keys())[0])
                        if month_number is None:
                            continue
                        entries.append(self.url_result(('%s/%04d-%02d' % (base_url, year, month_number)),
                          ie=(TVNowAnnualIE.ie_key())))

        else:
            if navigation == 'season':
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    season_number = int_or_none(item.get('season'))
                    if season_number is None:
                        continue
                    entries.append(self.url_result(('%s/staffel-%d' % (base_url, season_number)),
                      ie=(TVNowSeasonIE.ie_key())))

            else:
                raise ExtractorError('Unknown navigationType')
        return self.playlist_result(entries, show_id)