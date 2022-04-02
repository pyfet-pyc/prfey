# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\activity.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import datetime
from .asset import Asset
from .enums import ActivityType, try_enum
from .colour import Colour
from .partial_emoji import PartialEmoji
from .utils import _get_as_snowflake
__all__ = ('BaseActivity', 'Activity', 'Streaming', 'Game', 'Spotify', 'CustomActivity')

class BaseActivity:
    __doc__ = 'The base activity that all user-settable activities inherit from.\n    A user-settable activity is one that can be used in :meth:`Client.change_presence`.\n\n    The following types currently count as user-settable:\n\n    - :class:`Activity`\n    - :class:`Game`\n    - :class:`Streaming`\n    - :class:`CustomActivity`\n\n    Note that although these types are considered user-settable by the library,\n    Discord typically ignores certain combinations of activity depending on\n    what is currently set. This behaviour may change in the future so there are\n    no guarantees on whether Discord will actually let you set these types.\n\n    .. versionadded:: 1.3\n    '
    __slots__ = ('_created_at', )

    def __init__(self, **kwargs):
        self._created_at = kwargs.pop('created_at', None)

    @property
    def created_at(self):
        """Optional[:class:`datetime.datetime`]: When the user started doing this activity in UTC.

        .. versionadded:: 1.3
        """
        if self._created_at is not None:
            return datetime.datetime.utcfromtimestamp(self._created_at / 1000)


class Activity(BaseActivity):
    __doc__ = 'Represents an activity in Discord.\n\n    This could be an activity such as streaming, playing, listening\n    or watching.\n\n    For memory optimisation purposes, some activities are offered in slimmed\n    down versions:\n\n    - :class:`Game`\n    - :class:`Streaming`\n\n    Attributes\n    ------------\n    application_id: :class:`int`\n        The application ID of the game.\n    name: :class:`str`\n        The name of the activity.\n    url: :class:`str`\n        A stream URL that the activity could be doing.\n    type: :class:`ActivityType`\n        The type of activity currently being done.\n    state: :class:`str`\n        The user\'s current state. For example, "In Game".\n    details: :class:`str`\n        The detail of the user\'s current activity.\n    timestamps: :class:`dict`\n        A dictionary of timestamps. It contains the following optional keys:\n\n        - ``start``: Corresponds to when the user started doing the\n          activity in milliseconds since Unix epoch.\n        - ``end``: Corresponds to when the user will finish doing the\n          activity in milliseconds since Unix epoch.\n\n    assets: :class:`dict`\n        A dictionary representing the images and their hover text of an activity.\n        It contains the following optional keys:\n\n        - ``large_image``: A string representing the ID for the large image asset.\n        - ``large_text``: A string representing the text when hovering over the large image asset.\n        - ``small_image``: A string representing the ID for the small image asset.\n        - ``small_text``: A string representing the text when hovering over the small image asset.\n\n    party: :class:`dict`\n        A dictionary representing the activity party. It contains the following optional keys:\n\n        - ``id``: A string representing the party ID.\n        - ``size``: A list of up to two integer elements denoting (current_size, maximum_size).\n    emoji: Optional[:class:`PartialEmoji`]\n        The emoji that belongs to this activity.\n    '
    __slots__ = ('state', 'details', '_created_at', 'timestamps', 'assets', 'party',
                 'flags', 'sync_id', 'session_id', 'type', 'name', 'url', 'application_id',
                 'emoji')

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        self.state = kwargs.pop('state', None)
        self.details = kwargs.pop('details', None)
        self.timestamps = kwargs.pop('timestamps', {})
        self.assets = kwargs.pop('assets', {})
        self.party = kwargs.pop('party', {})
        self.application_id = _get_as_snowflake(kwargs, 'application_id')
        self.name = kwargs.pop('name', None)
        self.url = kwargs.pop('url', None)
        self.flags = kwargs.pop('flags', 0)
        self.sync_id = kwargs.pop('sync_id', None)
        self.session_id = kwargs.pop('session_id', None)
        self.type = try_enum(ActivityType, kwargs.pop('type', -1))
        emoji = kwargs.pop('emoji', None)
        if emoji is not None:
            self.emoji = PartialEmoji.from_dict(emoji)
        else:
            self.emoji = None

    def __repr__(self):
        attrs = ('type', 'name', 'url', 'details', 'application_id', 'session_id',
                 'emoji')
        mapped = ' '.join(('%s=%r' % (attr, getattr(self, attr)) for attr in attrs))
        return '<Activity %s>' % mapped

    def to_dict--- This code section failed: ---

 L. 211         0  BUILD_MAP_0           0 
                2  STORE_FAST               'ret'

 L. 212         4  LOAD_FAST                'self'
                6  LOAD_ATTR                __slots__
                8  GET_ITER         
             10_0  COME_FROM            68  '68'
             10_1  COME_FROM            58  '58'
             10_2  COME_FROM            34  '34'
               10  FOR_ITER             70  'to 70'
               12  STORE_FAST               'attr'

 L. 213        14  LOAD_GLOBAL              getattr
               16  LOAD_FAST                'self'
               18  LOAD_FAST                'attr'
               20  LOAD_CONST               None
               22  CALL_FUNCTION_3       3  ''
               24  STORE_FAST               'value'

 L. 214        26  LOAD_FAST                'value'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    36  'to 36'

 L. 215        34  JUMP_BACK            10  'to 10'
             36_0  COME_FROM            32  '32'

 L. 217        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'value'
               40  LOAD_GLOBAL              dict
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'value'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_CONST               0
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    60  'to 60'

 L. 218        58  JUMP_BACK            10  'to 10'
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            44  '44'

 L. 220        60  LOAD_FAST                'value'
               62  LOAD_FAST                'ret'
               64  LOAD_FAST                'attr'
               66  STORE_SUBSCR     
               68  JUMP_BACK            10  'to 10'
             70_0  COME_FROM            10  '10'

 L. 221        70  LOAD_GLOBAL              int
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                type
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_FAST                'ret'
               80  LOAD_STR                 'type'
               82  STORE_SUBSCR     

 L. 222        84  LOAD_FAST                'self'
               86  LOAD_ATTR                emoji
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 223        90  LOAD_FAST                'self'
               92  LOAD_ATTR                emoji
               94  LOAD_METHOD              to_dict
               96  CALL_METHOD_0         0  ''
               98  LOAD_FAST                'ret'
              100  LOAD_STR                 'emoji'
              102  STORE_SUBSCR     
            104_0  COME_FROM            88  '88'

 L. 224       104  LOAD_FAST                'ret'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 70

    @property
    def start--- This code section failed: ---

 L. 229         0  SETUP_FINALLY        26  'to 26'

 L. 230         2  LOAD_GLOBAL              datetime
                4  LOAD_ATTR                datetime
                6  LOAD_METHOD              utcfromtimestamp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                timestamps
               12  LOAD_STR                 'start'
               14  BINARY_SUBSCR    
               16  LOAD_CONST               1000
               18  BINARY_TRUE_DIVIDE
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 231        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 232        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 42

    @property
    def end--- This code section failed: ---

 L. 237         0  SETUP_FINALLY        26  'to 26'

 L. 238         2  LOAD_GLOBAL              datetime
                4  LOAD_ATTR                datetime
                6  LOAD_METHOD              utcfromtimestamp
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                timestamps
               12  LOAD_STR                 'end'
               14  BINARY_SUBSCR    
               16  LOAD_CONST               1000
               18  BINARY_TRUE_DIVIDE
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 239        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 240        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 42

    @property
    def large_image_url(self):
        """Optional[:class:`str`]: Returns a URL pointing to the large image asset of this activity if applicable."""
        if self.application_id is None:
            return
        try:
            large_image = self.assets['large_image']
        except KeyError:
            return
        else:
            return Asset.BASE + '/app-assets/{0}/{1}.png'.format(self.application_id, large_image)

    @property
    def small_image_url(self):
        """Optional[:class:`str`]: Returns a URL pointing to the small image asset of this activity if applicable."""
        if self.application_id is None:
            return
        try:
            small_image = self.assets['small_image']
        except KeyError:
            return
        else:
            return Asset.BASE + '/app-assets/{0}/{1}.png'.format(self.application_id, small_image)

    @property
    def large_image_text(self):
        """Optional[:class:`str`]: Returns the large image asset hover text of this activity if applicable."""
        return self.assets.get('large_text', None)

    @property
    def small_image_text(self):
        """Optional[:class:`str`]: Returns the small image asset hover text of this activity if applicable."""
        return self.assets.get('small_text', None)


class Game(BaseActivity):
    __doc__ = "A slimmed down version of :class:`Activity` that represents a Discord game.\n\n    This is typically displayed via **Playing** on the official Discord client.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two games are equal.\n\n        .. describe:: x != y\n\n            Checks if two games are not equal.\n\n        .. describe:: hash(x)\n\n            Returns the game's hash.\n\n        .. describe:: str(x)\n\n            Returns the game's name.\n\n    Parameters\n    -----------\n    name: :class:`str`\n        The game's name.\n    start: Optional[:class:`datetime.datetime`]\n        A naive UTC timestamp representing when the game started. Keyword-only parameter. Ignored for bots.\n    end: Optional[:class:`datetime.datetime`]\n        A naive UTC timestamp representing when the game ends. Keyword-only parameter. Ignored for bots.\n\n    Attributes\n    -----------\n    name: :class:`str`\n        The game's name.\n    "
    __slots__ = ('name', '_end', '_start')

    def __init__(self, name, **extra):
        (super().__init__)(**extra)
        self.name = name
        try:
            timestamps = extra['timestamps']
        except KeyError:
            self._extract_timestamp(extra, 'start')
            self._extract_timestamp(extra, 'end')
        else:
            self._start = timestamps.get('start', 0)
            self._end = timestamps.get('end', 0)

    def _extract_timestamp(self, data, key):
        try:
            dt = data[key]
        except KeyError:
            setattr(self, '_' + key, 0)
        else:
            setattr(self, '_' + key, dt.timestamp * 1000.0)

    @property
    def type(self):
        """Returns the game's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.playing`.
        """
        return ActivityType.playing

    @property
    def start(self):
        """Optional[:class:`datetime.datetime`]: When the user started playing this game in UTC, if applicable."""
        if self._start:
            return datetime.datetime.utcfromtimestamp(self._start / 1000)

    @property
    def end(self):
        """Optional[:class:`datetime.datetime`]: When the user will stop playing this game in UTC, if applicable."""
        if self._end:
            return datetime.datetime.utcfromtimestamp(self._end / 1000)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '<Game name={0.name!r}>'.format(self)

    def to_dict(self):
        timestamps = {}
        if self._start:
            timestamps['start'] = self._start
        if self._end:
            timestamps['end'] = self._end
        return {'type':ActivityType.playing.value, 
         'name':str(self.name), 
         'timestamps':timestamps}

    def __eq__(self, other):
        return isinstance(other, Game) and other.name == self.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)


class Streaming(BaseActivity):
    __doc__ = "A slimmed down version of :class:`Activity` that represents a Discord streaming status.\n\n    This is typically displayed via **Streaming** on the official Discord client.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two streams are equal.\n\n        .. describe:: x != y\n\n            Checks if two streams are not equal.\n\n        .. describe:: hash(x)\n\n            Returns the stream's hash.\n\n        .. describe:: str(x)\n\n            Returns the stream's name.\n\n    Attributes\n    -----------\n    platform: :class:`str`\n        Where the user is streaming from (ie. YouTube, Twitch).\n\n        .. versionadded:: 1.3\n\n    name: Optional[:class:`str`]\n        The stream's name.\n    details: Optional[:class:`str`]\n        Same as :attr:`name`\n    game: Optional[:class:`str`]\n        The game being streamed.\n\n        .. versionadded:: 1.3\n\n    url: :class:`str`\n        The stream's URL.\n    assets: :class:`dict`\n        A dictionary comprising of similar keys than those in :attr:`Activity.assets`.\n    "
    __slots__ = ('platform', 'name', 'game', 'url', 'details', 'assets')

    def __init__(self, *, name, url, **extra):
        (super().__init__)(**extra)
        self.platform = name
        self.name = extra.pop('details', name)
        self.game = extra.pop('state', None)
        self.url = url
        self.details = extra.pop('details', self.name)
        self.assets = extra.pop('assets', {})

    @property
    def type(self):
        """Returns the game's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.streaming`.
        """
        return ActivityType.streaming

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '<Streaming name={0.name!r}>'.format(self)

    @property
    def twitch_name(self):
        """Optional[:class:`str`]: If provided, the twitch name of the user streaming.

        This corresponds to the ``large_image`` key of the :attr:`Streaming.assets`
        dictionary if it starts with ``twitch:``. Typically set by the Discord client.
        """
        try:
            name = self.assets['large_image']
        except KeyError:
            return
        else:
            if name[:7] == 'twitch:':
                return name[7:]
            return

    def to_dict(self):
        ret = {'type':ActivityType.streaming.value, 
         'name':str(self.name), 
         'url':str(self.url), 
         'assets':self.assets}
        if self.details:
            ret['details'] = self.details
        return ret

    def __eq__(self, other):
        return isinstance(other, Streaming) and other.name == self.name and other.url == self.url

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)


class Spotify:
    __doc__ = "Represents a Spotify listening activity from Discord. This is a special case of\n    :class:`Activity` that makes it easier to work with the Spotify integration.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two activities are equal.\n\n        .. describe:: x != y\n\n            Checks if two activities are not equal.\n\n        .. describe:: hash(x)\n\n            Returns the activity's hash.\n\n        .. describe:: str(x)\n\n            Returns the string 'Spotify'.\n    "
    __slots__ = ('_state', '_details', '_timestamps', '_assets', '_party', '_sync_id',
                 '_session_id', '_created_at')

    def __init__(self, **data):
        self._state = data.pop('state', None)
        self._details = data.pop('details', None)
        self._timestamps = data.pop('timestamps', {})
        self._assets = data.pop('assets', {})
        self._party = data.pop('party', {})
        self._sync_id = data.pop('sync_id')
        self._session_id = data.pop('session_id')
        self._created_at = data.pop('created_at', None)

    @property
    def type(self):
        """Returns the activity's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.listening`.
        """
        return ActivityType.listening

    @property
    def created_at(self):
        """Optional[:class:`datetime.datetime`]: When the user started listening in UTC.

        .. versionadded:: 1.3
        """
        if self._created_at is not None:
            return datetime.datetime.utcfromtimestamp(self._created_at / 1000)

    @property
    def colour(self):
        """Returns the Spotify integration colour, as a :class:`Colour`.

        There is an alias for this named :meth:`color`"""
        return Colour(1947988)

    @property
    def color(self):
        """Returns the Spotify integration colour, as a :class:`Colour`.

        There is an alias for this named :meth:`colour`"""
        return self.colour

    def to_dict(self):
        return {'flags':48, 
         'name':'Spotify', 
         'assets':self._assets, 
         'party':self._party, 
         'sync_id':self._sync_id, 
         'session_id':self._session_id, 
         'timestamps':self._timestamps, 
         'details':self._details, 
         'state':self._state}

    @property
    def name(self):
        """:class:`str`: The activity's name. This will always return "Spotify"."""
        return 'Spotify'

    def __eq__(self, other):
        return isinstance(other, Spotify) and other._session_id == self._session_id and other._sync_id == self._sync_id and other.start == self.start

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._session_id)

    def __str__(self):
        return 'Spotify'

    def __repr__(self):
        return '<Spotify title={0.title!r} artist={0.artist!r} track_id={0.track_id!r}>'.format(self)

    @property
    def title(self):
        """:class:`str`: The title of the song being played."""
        return self._details

    @property
    def artists(self):
        """List[:class:`str`]: The artists of the song being played."""
        return self._state.split('; ')

    @property
    def artist(self):
        """:class:`str`: The artist of the song being played.

        This does not attempt to split the artist information into
        multiple artists. Useful if there's only a single artist.
        """
        return self._state

    @property
    def album(self):
        """:class:`str`: The album that the song being played belongs to."""
        return self._assets.get('large_text', '')

    @property
    def album_cover_url(self):
        """:class:`str`: The album cover image URL from Spotify's CDN."""
        large_image = self._assets.get('large_image', '')
        if large_image[:8] != 'spotify:':
            return ''
        album_image_id = large_image[8:]
        return 'https://i.scdn.co/image/' + album_image_id

    @property
    def track_id(self):
        """:class:`str`: The track ID used by Spotify to identify this song."""
        return self._sync_id

    @property
    def start(self):
        """:class:`datetime.datetime`: When the user started playing this song in UTC."""
        return datetime.datetime.utcfromtimestamp(self._timestamps['start'] / 1000)

    @property
    def end(self):
        """:class:`datetime.datetime`: When the user will stop playing this song in UTC."""
        return datetime.datetime.utcfromtimestamp(self._timestamps['end'] / 1000)

    @property
    def duration(self):
        """:class:`datetime.timedelta`: The duration of the song being played."""
        return self.end - self.start

    @property
    def party_id(self):
        """:class:`str`: The party ID of the listening party."""
        return self._party.get('id', '')


class CustomActivity(BaseActivity):
    __doc__ = "Represents a Custom activity from Discord.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two activities are equal.\n\n        .. describe:: x != y\n\n            Checks if two activities are not equal.\n\n        .. describe:: hash(x)\n\n            Returns the activity's hash.\n\n        .. describe:: str(x)\n\n            Returns the custom status text.\n\n    .. versionadded:: 1.3\n\n    Attributes\n    -----------\n    name: Optional[:class:`str`]\n        The custom activity's name.\n    emoji: Optional[:class:`PartialEmoji`]\n        The emoji to pass to the activity, if any.\n    "
    __slots__ = ('name', 'emoji', 'state')

    def __init__(self, name, *, emoji=None, **extra):
        self.name = name
        self.state = extra.pop('state', None)
        if self.name == 'Custom Status':
            self.name = self.state
        if emoji is None:
            self.emoji = emoji
        else:
            self.emoji = PartialEmoji.from_dict(emoji)

    @property
    def type(self):
        """Returns the activity's type. This is for compatibility with :class:`Activity`.

        It always returns :attr:`ActivityType.custom`.
        """
        return ActivityType.custom

    def to_dict(self):
        if self.name == self.state:
            o = {'type':ActivityType.custom.value,  'state':self.name, 
             'name':'Custom Status'}
        else:
            o = {'type':ActivityType.custom.value,  'name':self.name}
        if self.emoji:
            o['emoji'] = self.emoji.to_dict
        return o

    def __eq__(self, other):
        return isinstance(other, CustomActivity) and other.name == self.name and other.emoji == self.emoji

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, str(self.emoji)))

    def __str__(self):
        if self.emoji:
            if self.name:
                return '%s %s' % (self.emoji, self.name)
            return str(self.emoji)
        return str(self.name)

    def __repr__(self):
        return '<CustomActivity name={0.name!r} emoji={0.emoji!r}>'.format(self)


def create_activity(data):
    if not data:
        return
    game_type = try_enum(ActivityType, data.get('type', -1))
    if game_type is ActivityType.playing:
        if 'application_id' in data or ('session_id' in data):
            return Activity(**data)
        return Game(**data)
    if game_type is ActivityType.custom:
        try:
            name = data.pop('name')
        except KeyError:
            return Activity(**data)
        else:
            return CustomActivity(name=name, **data)
    else:
        if game_type is ActivityType.streaming:
            if 'url' in data:
                return Streaming(**data)
            return Activity(**data)
        if game_type is ActivityType.listening:
            if 'sync_id' in data:
                if 'session_id' in data:
                    return Spotify(**data)
    return Activity(**data)