# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\extractor\twitter.py
"""Extractors for https://twitter.com/"""
from .common import Extractor, Message
from .. import text, util, exception
from ..cache import cache
import json
BASE_PATTERN = '(?:https?://)?(?:www\\.|mobile\\.)?(?:twitter\\.com|nitter\\.net)'

class TwitterExtractor(Extractor):
    __doc__ = 'Base class for twitter extractors'
    category = 'twitter'
    directory_fmt = ('{category}', '{user[name]}')
    filename_fmt = '{tweet_id}_{num}.{extension}'
    archive_fmt = '{tweet_id}_{retweet_id}_{num}'
    cookiedomain = '.twitter.com'
    root = 'https://twitter.com'

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.user = match.group(1)
        self.retweets = self.config('retweets', True)
        self.replies = self.config('replies', True)
        self.twitpic = self.config('twitpic', False)
        self.quoted = self.config('quoted', True)
        self.videos = self.config('videos', True)
        self.cards = self.config('cards', False)
        self._user_cache = {}

    def items(self):
        self.login()
        metadata = self.metadata()
        yield (Message.Version, 1)
        for tweet in self.tweets():
            if not self.retweets:
                if 'retweeted_status_id_str' in tweet:
                    self.log.debug('Skipping %s (retweet)', tweet['id_str'])
                    continue
            if not self.replies:
                if 'in_reply_to_user_id_str' in tweet:
                    self.log.debug('Skipping %s (reply)', tweet['id_str'])
                    continue
            if not self.quoted:
                if 'quoted' in tweet:
                    self.log.debug('Skipping %s (quoted tweet)', tweet['id_str'])
                    continue
            files = []
            if 'extended_entities' in tweet:
                self._extract_media(tweet, files)
            else:
                if 'card' in tweet:
                    if self.cards:
                        self._extract_card(tweet, files)
                if self.twitpic:
                    self._extract_twitpic(tweet, files)
            if not files:
                continue
            else:
                tdata = self._transform_tweet(tweet)
                tdata.update(metadata)
                yield (Message.Directory, tdata)
                for tdata['num'], file in enumerate(files, 1):
                    file.update(tdata)
                    url = file.pop('url')
                    if 'extension' not in file:
                        text.nameext_from_url(url, file)
                    else:
                        yield (
                         Message.Url, url, file)

    def _extract_media(self, tweet, files):
        for media in tweet['extended_entities']['media']:
            width = media['original_info'].get('width', 0)
            height = media['original_info'].get('height', 0)
            if 'video_info' in media:
                if self.videos == 'ytdl':
                    files.append({'url':'ytdl:{}/i/web/status/{}'.format(self.root, tweet['id_str']), 
                     'width':width, 
                     'height':height, 
                     'extension':None})
                elif self.videos:
                    video_info = media['video_info']
                    variant = max((video_info['variants']),
                      key=(lambda v: v.get('bitrate', 0)))
                    files.append({'url':variant['url'], 
                     'width':width, 
                     'height':height, 
                     'bitrate':variant.get('bitrate', 0), 
                     'duration':video_info.get('duration_millis', 0) / 1000})
            else:
                if 'media_url_https' in media:
                    url = media['media_url_https']
                    base, _, fmt = url.rpartition('.')
                    base += '?format=' + fmt + '&name='
                    files.append(text.nameext_from_url(url, {'url':base + 'orig', 
                     'width':width, 
                     'height':height, 
                     '_fallback':self._image_fallback(base, url)}))
                else:
                    files.append({'url': media['media_url']})

    @staticmethod
    def _image_fallback(base, url):
        url += ':'
        yield url + 'orig'
        for size in ('large', 'medium', 'small'):
            yield base + size
            yield url + size

    def _extract_card(self, tweet, files):
        card = tweet['card']
        if card['name'] in ('summary', 'summary_large_image'):
            bvals = card['binding_values']
            for prefix in ('photo_image_full_size_', 'summary_photo_image_', 'thumbnail_image_'):
                for size in ('original', 'x_large', 'large', 'small'):
                    key = prefix + size
                    if key in bvals:
                        files.append(bvals[key]['image_value'])
                        return

        else:
            url = 'ytdl:{}/i/web/status/{}'.format(self.root, tweet['id_str'])
            files.append({'url': url})

    def _extract_twitpic(self, tweet, files):
        for url in tweet['entities'].get('urls', ()):
            url = url['expanded_url']
            if '//twitpic.com/' in url:
                if '/photos/' not in url:
                    response = self.request(url, fatal=False)
                    if response.status_code >= 400:
                        continue
                    else:
                        url = text.extract(response.text, 'name="twitter:image" value="', '"')[0]
                    if url:
                        files.append({'url': url})

    def _transform_tweet(self, tweet):
        entities = tweet['entities']
        tdata = {'tweet_id':text.parse_int(tweet['id_str']), 
         'retweet_id':text.parse_int(tweet.get('retweeted_status_id_str')), 
         'quote_id':text.parse_int(tweet.get('quoted_status_id_str')), 
         'reply_id':text.parse_int(tweet.get('in_reply_to_status_id_str')), 
         'date':text.parse_datetime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y'), 
         'user':self._transform_user(tweet['user']), 
         'lang':tweet['lang'], 
         'content':tweet['full_text'], 
         'favorite_count':tweet['favorite_count'], 
         'quote_count':tweet['quote_count'], 
         'reply_count':tweet['reply_count'], 
         'retweet_count':tweet['retweet_count']}
        hashtags = entities.get('hashtags')
        if hashtags:
            tdata['hashtags'] = [t['text'] for t in hashtags]
        mentions = entities.get('user_mentions')
        if mentions:
            tdata['mentions'] = [{'id':text.parse_int(u['id_str']),  'name':u['screen_name'],  'nick':u['name']} for u in mentions]
        if 'in_reply_to_screen_name' in tweet:
            tdata['reply_to'] = tweet['in_reply_to_screen_name']
        if 'author' in tweet:
            tdata['author'] = self._transform_user(tweet['author'])
        else:
            tdata['author'] = tdata['user']
        return tdata

    def _transform_user(self, user):
        uid = user['id_str']
        cache = self._user_cache
        if uid not in cache:
            cache[uid] = {'id':text.parse_int(uid),  'name':user['screen_name'], 
             'nick':user['name'], 
             'description':user['description'], 
             'location':user['location'], 
             'date':text.parse_datetime(user['created_at'], '%a %b %d %H:%M:%S %z %Y'), 
             'verified':user.get('verified', False), 
             'profile_banner':user.get('profile_banner_url', ''), 
             'profile_image':user.get('profile_image_url_https', '').replace('_normal.', '.'), 
             'favourites_count':user['favourites_count'], 
             'followers_count':user['followers_count'], 
             'friends_count':user['friends_count'], 
             'listed_count':user['listed_count'], 
             'media_count':user['media_count'], 
             'statuses_count':user['statuses_count']}
        return cache[uid]

    def metadata(self):
        """Return general metadata"""
        return {}

    def tweets(self):
        """Yield all relevant tweet objects"""
        pass

    def login(self):
        username, password = self._get_auth_info()
        if username:
            self._update_cookies(self._login_impl(username, password))

    @cache(maxage=31104000, keyarg=1)
    def _login_impl(self, username, password):
        self.log.info('Logging in as %s', username)
        token = util.generate_csrf_token()
        self.session.cookies.clear()
        self.request(self.root + '/login')
        url = self.root + '/sessions'
        cookies = {'_mb_tk': token}
        data = {'redirect_after_login':'/', 
         'remember_me':'1', 
         'authenticity_token':token, 
         'wfa':'1', 
         'ui_metrics':'{}', 
         'session[username_or_email]':username, 
         'session[password]':password}
        response = self.request(url,
          method='POST', cookies=cookies, data=data)
        cookies = {cookie.name:cookie.value for cookie in self.session.cookies}
        if '/error' in response.url or ('auth_token' not in cookies):
            raise exception.AuthenticationError()
        return cookies


class TwitterTimelineExtractor(TwitterExtractor):
    __doc__ = "Extractor for all images from a user's timeline"
    subcategory = 'timeline'
    pattern = BASE_PATTERN + '/(?!search)(?:([^/?#]+)/?(?:$|[?#])|intent/user\\?user_id=(\\d+))'
    test = (
     (
      'https://twitter.com/supernaturepics',
      {'range':'1-40', 
       'url':'c570ac1aae38ed1463be726cc46f31cac3d82a40'}),
     'https://mobile.twitter.com/supernaturepics?p=i',
     'https://www.twitter.com/id:2976459548',
     'https://twitter.com/intent/user?user_id=2976459548')

    def __init__(self, match):
        TwitterExtractor.__init__(self, match)
        uid = match.group(2)
        if uid:
            self.user = 'id:' + uid

    def tweets(self):
        return TwitterAPI(self).timeline_profile(self.user)


class TwitterMediaExtractor(TwitterExtractor):
    __doc__ = "Extractor for all images from a user's Media Tweets"
    subcategory = 'media'
    pattern = BASE_PATTERN + '/(?!search)([^/?#]+)/media(?!\\w)'
    test = (
     (
      'https://twitter.com/supernaturepics/media',
      {'range':'1-40', 
       'url':'c570ac1aae38ed1463be726cc46f31cac3d82a40'}),
     'https://mobile.twitter.com/supernaturepics/media#t',
     'https://www.twitter.com/id:2976459548/media')

    def tweets(self):
        return TwitterAPI(self).timeline_media(self.user)


class TwitterLikesExtractor(TwitterExtractor):
    __doc__ = 'Extractor for liked tweets'
    subcategory = 'likes'
    pattern = BASE_PATTERN + '/(?!search)([^/?#]+)/likes(?!\\w)'
    test = ('https://twitter.com/supernaturepics/likes', )

    def tweets(self):
        return TwitterAPI(self).timeline_favorites(self.user)


class TwitterBookmarkExtractor(TwitterExtractor):
    __doc__ = 'Extractor for bookmarked tweets'
    subcategory = 'bookmark'
    pattern = BASE_PATTERN + '/i/bookmarks()'
    test = ('https://twitter.com/i/bookmarks', )

    def tweets(self):
        return TwitterAPI(self).timeline_bookmark()


class TwitterListExtractor(TwitterExtractor):
    __doc__ = 'Extractor for Twitter lists'
    subcategory = 'list'
    pattern = BASE_PATTERN + '/i/lists/(\\d+)/?$'
    test = ('https://twitter.com/i/lists/784214683683127296',
     {'range':'1-40', 
      'count':40, 
      'archive':False})

    def tweets(self):
        return TwitterAPI(self).timeline_list(self.user)


class TwitterListMembersExtractor(TwitterExtractor):
    __doc__ = 'Extractor for members of a Twitter list'
    subcategory = 'list-members'
    pattern = BASE_PATTERN + '/i/lists/(\\d+)/members'
    test = ('https://twitter.com/i/lists/784214683683127296/members', )

    def items(self):
        self.login()
        for user in TwitterAPI(self).list_members(self.user):
            user['_extractor'] = TwitterTimelineExtractor
            url = '{}/intent/user?user_id={}'.format(self.root, user['rest_id'])
            yield (Message.Queue, url, user)


class TwitterSearchExtractor(TwitterExtractor):
    __doc__ = 'Extractor for all images from a search timeline'
    subcategory = 'search'
    directory_fmt = ('{category}', 'Search', '{search}')
    pattern = BASE_PATTERN + '/search/?\\?(?:[^&#]+&)*q=([^&#]+)'
    test = ('https://twitter.com/search?q=nature',
     {'range':'1-40', 
      'count':40, 
      'archive':False})

    def metadata(self):
        return {'search': text.unquote(self.user)}

    def tweets(self):
        return TwitterAPI(self).search(text.unquote(self.user))


class TwitterTweetExtractor(TwitterExtractor):
    __doc__ = 'Extractor for images from individual tweets'
    subcategory = 'tweet'
    pattern = BASE_PATTERN + '/([^/?#]+|i/web)/status/(\\d+)'
    test = (
     (
      'https://twitter.com/supernaturepics/status/604341487988576256',
      {'url':'88a40f7d25529c2501c46f2218f9e0de9aa634b4', 
       'content':'ab05e1d8d21f8d43496df284d31e8b362cd3bcab'}),
     (
      'https://twitter.com/perrypumas/status/894001459754180609',
      {'url': '3a2a43dc5fb79dd5432c701d8e55e87c4e551f47'}),
     (
      'https://twitter.com/perrypumas/status/1065692031626829824',
      {'pattern': 'https://video.twimg.com/ext_tw_video/.+\\.mp4\\?tag=5'}),
     (
      'https://twitter.com/playpokemon/status/1263832915173048321',
      {'keyword': {'content': 're:Gear up for #PokemonSwordShieldEX with special Mystery Gifts! \n\nYou’ll be able to receive four Galarian form Pokémon with Hidden Abilities, plus some very useful items. It’s our \\(Mystery\\) Gift to you, Trainers! \n\n❓🎁➡️ '}}),
     (
      'https://twitter.com/i/web/status/1170041925560258560',
      {'pattern': 'https://pbs.twimg.com/media/EDzS7VrU0AAFL4_'}),
     (
      'https://twitter.com/i/web/status/1170041925560258560',
      {'options':(('replies', False), ), 
       'count':0}),
     (
      'https://twitter.com/StobiesGalaxy/status/1270755918330896395',
      {'pattern':'https://pbs\\.twimg\\.com/media/Ea[KG].+=jpg', 
       'count':8}),
     (
      'https://twitter.com/StobiesGalaxy/status/1270755918330896395',
      {'options':(('quoted', False), ), 
       'pattern':'https://pbs\\.twimg\\.com/media/EaK.+=jpg', 
       'count':4}),
     (
      'https://twitter.com/i/web/status/112900228289540096',
      {'options':(('twitpic', True), ), 
       'pattern':'https://\\w+.cloudfront.net/photos/large/\\d+.jpg', 
       'count':3}),
     (
      'https://nitter.net/ed1conf/status/1163841619336007680',
      {'url':'4a9ea898b14d3c112f98562d0df75c9785e239d9', 
       'content':'f29501e44d88437fe460f5c927b7543fda0f6e34'}),
     (
      'https://twitter.com/billboard/status/1306599586602135555',
      {'options':(('cards', True), ), 
       'pattern':'https://pbs.twimg.com/card_img/\\d+/'}),
     (
      'https://twitter.com/jessica_3978/status/1296304589591810048',
      {'options':(('retweets', 'original'), ), 
       'count':2, 
       'keyword':{'tweet_id':1296296016002547713, 
        'date':'dt:2020-08-20 04:00:28'}}))

    def __init__(self, match):
        TwitterExtractor.__init__(self, match)
        self.tweet_id = match.group(2)

    def tweets(self):
        return TwitterAPI(self).tweet(self.tweet_id)


class TwitterAPI:

    def __init__(self, extractor):
        self.extractor = extractor
        self.root = 'https://twitter.com/i/api'
        self.headers = {'authorization':'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA', 
         'x-guest-token':None, 
         'x-twitter-auth-type':None, 
         'x-twitter-client-language':'en', 
         'x-twitter-active-user':'yes', 
         'x-csrf-token':None, 
         'Referer':'https://twitter.com/'}
        self.params = {'include_profile_interstitial_type':'1', 
         'include_blocking':'1', 
         'include_blocked_by':'1', 
         'include_followed_by':'1', 
         'include_want_retweets':'1', 
         'include_mute_edge':'1', 
         'include_can_dm':'1', 
         'include_can_media_tag':'1', 
         'skip_status':'1', 
         'cards_platform':'Web-12', 
         'include_cards':'1', 
         'include_ext_alt_text':'true', 
         'include_quote_count':'true', 
         'include_reply_count':'1', 
         'tweet_mode':'extended', 
         'include_entities':'true', 
         'include_user_entities':'true', 
         'include_ext_media_color':'true', 
         'include_ext_media_availability':'true', 
         'send_error_codes':'true', 
         'simple_quoted_tweet':'true', 
         'count':'100', 
         'cursor':None, 
         'ext':'mediaStats,highlightedLabel'}
        cookies = self.extractor.session.cookies
        cookiedomain = '.twitter.com'
        csrf_token = cookies.get('ct0', domain=cookiedomain)
        if not csrf_token:
            csrf_token = util.generate_csrf_token()
            cookies.set('ct0', csrf_token, domain=cookiedomain)
        self.headers['x-csrf-token'] = csrf_token
        if cookies.get('auth_token', domain=cookiedomain):
            self.headers['x-twitter-auth-type'] = 'OAuth2Session'
        else:
            guest_token = self._guest_token()
            cookies.set('gt', guest_token, domain=cookiedomain)
            self.headers['x-guest-token'] = guest_token

    def tweet(self, tweet_id):
        endpoint = '/2/timeline/conversation/{}.json'.format(tweet_id)
        tweets = []
        for tweet in self._pagination(endpoint):
            if not tweet['id_str'] == tweet_id:
                if tweet.get('_retweet_id_str') == tweet_id:
                    pass
            tweets.append(tweet)
            if 'quoted_status_id_str' in tweet:
                tweet_id = tweet['quoted_status_id_str']
            else:
                break

        return tweets

    def timeline_profile(self, screen_name):
        user_id = self._user_id_by_screen_name(screen_name)
        endpoint = '/2/timeline/profile/{}.json'.format(user_id)
        params = self.params.copy()
        params['include_tweet_replies'] = 'false'
        return self._pagination(endpoint, params)

    def timeline_media(self, screen_name):
        user_id = self._user_id_by_screen_name(screen_name)
        endpoint = '/2/timeline/media/{}.json'.format(user_id)
        return self._pagination(endpoint)

    def timeline_favorites(self, screen_name):
        user_id = self._user_id_by_screen_name(screen_name)
        endpoint = '/2/timeline/favorites/{}.json'.format(user_id)
        params = self.params.copy()
        params['sorted_by_time'] = 'true'
        return self._pagination(endpoint)

    def timeline_bookmark(self):
        endpoint = '/2/timeline/bookmark.json'
        return self._pagination(endpoint)

    def timeline_list(self, list_id):
        endpoint = '/2/timeline/list.json'
        params = self.params.copy()
        params['list_id'] = list_id
        params['ranking_mode'] = 'reverse_chronological'
        return self._pagination(endpoint, params)

    def search(self, query):
        endpoint = '/2/search/adaptive.json'
        params = self.params.copy()
        params['q'] = query
        params['tweet_search_mode'] = 'live'
        params['query_source'] = 'typed_query'
        params['pc'] = '1'
        params['spelling_corrections'] = '1'
        return self._pagination(endpoint, params)

    def list_members(self, list_id):
        endpoint = '/graphql/3pV4YlpljXUTFAa1jVNWQw/ListMembers'
        variables = {'listId':list_id, 
         'count':20, 
         'withTweetResult':False, 
         'withUserResult':False}
        return self._pagination_members(endpoint, variables)

    def list_by_rest_id(self, list_id):
        endpoint = '/graphql/EhaI2uiCBJI97e28GN8WjQ/ListByRestId'
        params = {'variables': '{"listId":"' + list_id + '","withUserResult":false}'}
        try:
            return self._call(endpoint, params)['data']['list']
        except KeyError:
            raise exception.NotFoundError('list')

    def user_by_screen_name(self, screen_name):
        endpoint = '/graphql/ZRnOhhXPwue_JGILb9TNug/UserByScreenName'
        params = {'variables': '{"screen_name":"' + screen_name + '","withHighlightedLabel":true}'}
        try:
            return self._call(endpoint, params)['data']['user']
        except KeyError:
            raise exception.NotFoundError('user')

    def _user_id_by_screen_name(self, screen_name):
        if screen_name.startswith('id:'):
            return screen_name[3:]
        return self.user_by_screen_name(screen_name)['rest_id']

    @cache(maxage=3600)
    def _guest_token(self):
        root = 'https://api.twitter.com'
        endpoint = '/1.1/guest/activate.json'
        return self._call(endpoint, None, root, 'POST')['guest_token']

    def _call(self, endpoint, params, root=None, method='GET'):
        if root is None:
            root = self.root
        response = self.extractor.request((root + endpoint),
          method=method, params=params, headers=(self.headers),
          fatal=None)
        csrf_token = response.cookies.get('ct0')
        if csrf_token:
            self.headers['x-csrf-token'] = csrf_token
        if response.status_code < 400:
            return response.json()
        if response.status_code == 429:
            until = response.headers.get('x-rate-limit-reset')
            self.extractor.wait(until=until, seconds=(None if until else 60))
            return self._call(endpoint, params, method)
        try:
            msg = ', '.join(('"' + error['message'] + '"' for error in response.json()['errors']))
        except Exception:
            msg = response.text

        raise exception.StopExtraction('%s %s (%s)', response.status_code, response.reason, msg)

    def _pagination(self, endpoint, params=None):
        if params is None:
            params = self.params.copy()
        original_retweets = self.extractor.retweets == 'original'
        pinned_tweet = True
        while True:
            cursor = tweet = None
            data = self._call(endpoint, params)
            instr = data['timeline']['instructions']
            if not instr:
                return
            else:
                tweet_ids = []
                tweets = data['globalObjects']['tweets']
                users = data['globalObjects']['users']
                if pinned_tweet:
                    if 'pinEntry' in instr[(-1)]:
                        tweet_ids.append(instr[(-1)]['pinEntry']['entry']['content']['item']['content']['tweet']['id'])
                    pinned_tweet = False
                for entry in instr[0]['addEntries']['entries']:
                    entry_startswith = entry['entryId'].startswith
                    if entry_startswith(('tweet-', 'sq-I-t-')):
                        tweet_ids.append(entry['content']['item']['content']['tweet']['id'])
                    else:
                        if entry_startswith('homeConversation-'):
                            tweet_ids.extend(entry['content']['timelineModule']['metadata']['conversationMetadata']['allTweetIds'][::-1])
                    if entry_startswith(('cursor-bottom-', 'sq-cursor-bottom')):
                        cursor = entry['content']['operation']['cursor']
                        if not cursor.get('stopOnEmptyResponse'):
                            tweet = True
                        else:
                            cursor = cursor['value']

                for tweet_id in tweet_ids:
                    try:
                        tweet = tweets[tweet_id]
                    except KeyError:
                        self.extractor.log.debug('Skipping %s (deleted)', tweet_id)
                        continue

                    if 'retweeted_status_id_str' in tweet:
                        retweet = tweets.get(tweet['retweeted_status_id_str'])
                        if original_retweets:
                            if not retweet:
                                continue
                            else:
                                retweet['_retweet_id_str'] = tweet['id_str']
                                tweet = retweet
                        elif retweet:
                            tweet['author'] = users[retweet['user_id_str']]
                    tweet['user'] = users[tweet['user_id_str']]
                    yield tweet
                    if 'quoted_status_id_str' in tweet:
                        quoted = tweets.get(tweet['quoted_status_id_str'])
                        if quoted:
                            quoted['author'] = users[quoted['user_id_str']]
                            quoted['user'] = tweet['user']
                            quoted['quoted'] = True
                            yield quoted

                if 'replaceEntry' in instr[(-1)]:
                    cursor = instr[(-1)]['replaceEntry']['entry']['content']['operation']['cursor']['value']
                if not (cursor and tweet):
                    return
                params['cursor'] = cursor

    def _pagination_members--- This code section failed: ---

 L. 727       0_2  SETUP_LOOP          262  'to 262'
              4_0  COME_FROM           258  '258'

 L. 728         4  LOAD_CONST               None
                6  DUP_TOP          
                8  STORE_FAST               'cursor'
               10  DUP_TOP          
               12  STORE_FAST               'entry'
               14  STORE_FAST               'stop'

 L. 729        16  LOAD_STR                 'variables'
               18  LOAD_GLOBAL              json
               20  LOAD_METHOD              dumps
               22  LOAD_FAST                'variables'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  BUILD_MAP_1           1 
               28  STORE_FAST               'params'

 L. 730        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _call
               34  LOAD_FAST                'endpoint'
               36  LOAD_FAST                'params'
               38  CALL_METHOD_2         2  '2 positional arguments'
               40  STORE_FAST               'data'

 L. 732        42  SETUP_EXCEPT         72  'to 72'

 L. 733        44  LOAD_FAST                'data'
               46  LOAD_STR                 'data'
               48  BINARY_SUBSCR    
               50  LOAD_STR                 'list'
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'members_timeline'
               56  BINARY_SUBSCR    

 L. 734        58  LOAD_STR                 'timeline'
               60  BINARY_SUBSCR    
               62  LOAD_STR                 'instructions'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'instructions'
               68  POP_BLOCK        
               70  JUMP_FORWARD        100  'to 100'
             72_0  COME_FROM_EXCEPT     42  '42'

 L. 735        72  DUP_TOP          
               74  LOAD_GLOBAL              KeyError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    98  'to 98'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 736        86  LOAD_GLOBAL              exception
               88  LOAD_METHOD              AuthorizationError
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  RAISE_VARARGS_1       1  'exception instance'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            78  '78'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            70  '70'

 L. 738       100  SETUP_LOOP          234  'to 234'
              102  LOAD_FAST                'instructions'
              104  GET_ITER         
            106_0  COME_FROM           230  '230'
            106_1  COME_FROM           224  '224'
            106_2  COME_FROM           212  '212'
            106_3  COME_FROM           200  '200'
              106  FOR_ITER            232  'to 232'
              108  STORE_FAST               'instr'

 L. 739       110  LOAD_FAST                'instr'
              112  LOAD_STR                 'type'
              114  BINARY_SUBSCR    
              116  LOAD_STR                 'TimelineAddEntries'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   202  'to 202'

 L. 740       122  SETUP_LOOP          230  'to 230'
              124  LOAD_FAST                'instr'
              126  LOAD_STR                 'entries'
              128  BINARY_SUBSCR    
              130  GET_ITER         
            132_0  COME_FROM           196  '196'
            132_1  COME_FROM           182  '182'
            132_2  COME_FROM           168  '168'
              132  FOR_ITER            198  'to 198'
              134  STORE_FAST               'entry'

 L. 741       136  LOAD_FAST                'entry'
              138  LOAD_STR                 'entryId'
              140  BINARY_SUBSCR    
              142  LOAD_METHOD              startswith
              144  LOAD_STR                 'user-'
              146  CALL_METHOD_1         1  '1 positional argument'
              148  POP_JUMP_IF_FALSE   170  'to 170'

 L. 742       150  LOAD_FAST                'entry'
              152  LOAD_STR                 'content'
              154  BINARY_SUBSCR    
              156  LOAD_STR                 'itemContent'
              158  BINARY_SUBSCR    
              160  LOAD_STR                 'user'
              162  BINARY_SUBSCR    
              164  YIELD_VALUE      
              166  POP_TOP          
              168  JUMP_BACK           132  'to 132'
            170_0  COME_FROM           148  '148'

 L. 743       170  LOAD_FAST                'entry'
              172  LOAD_STR                 'entryId'
              174  BINARY_SUBSCR    
              176  LOAD_METHOD              startswith
              178  LOAD_STR                 'cursor-bottom-'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_JUMP_IF_FALSE_BACK   132  'to 132'

 L. 744       184  LOAD_FAST                'entry'
              186  LOAD_STR                 'content'
              188  BINARY_SUBSCR    
              190  LOAD_STR                 'value'
              192  BINARY_SUBSCR    
              194  STORE_FAST               'cursor'
              196  JUMP_BACK           132  'to 132'
              198  POP_BLOCK        
              200  JUMP_BACK           106  'to 106'
            202_0  COME_FROM           120  '120'

 L. 745       202  LOAD_FAST                'instr'
              204  LOAD_STR                 'type'
              206  BINARY_SUBSCR    
              208  LOAD_STR                 'TimelineTerminateTimeline'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 746       214  LOAD_FAST                'instr'
              216  LOAD_STR                 'direction'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'Bottom'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 747       226  LOAD_CONST               True
              228  STORE_FAST               'stop'
            230_0  COME_FROM_LOOP      122  '122'
              230  JUMP_BACK           106  'to 106'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP      100  '100'

 L. 749       234  LOAD_FAST                'stop'
              236  POP_JUMP_IF_TRUE    246  'to 246'
              238  LOAD_FAST                'cursor'
              240  POP_JUMP_IF_FALSE   246  'to 246'
              242  LOAD_FAST                'entry'
              244  POP_JUMP_IF_TRUE    250  'to 250'
            246_0  COME_FROM           240  '240'
            246_1  COME_FROM           236  '236'

 L. 750       246  LOAD_CONST               None
              248  RETURN_VALUE     
            250_0  COME_FROM           244  '244'

 L. 751       250  LOAD_FAST                'cursor'
              252  LOAD_FAST                'variables'
              254  LOAD_STR                 'cursor'
              256  STORE_SUBSCR     
              258  JUMP_BACK             4  'to 4'
              260  POP_BLOCK        
            262_0  COME_FROM_LOOP        0  '0'

Parse error at or near `POP_BLOCK' instruction at offset 260