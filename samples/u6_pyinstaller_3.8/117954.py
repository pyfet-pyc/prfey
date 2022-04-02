# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\asset.py
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
import io
from .errors import DiscordException
from .errors import InvalidArgument
from . import utils
VALID_STATIC_FORMATS = frozenset({'jpeg', 'jpg', 'webp', 'png'})
VALID_AVATAR_FORMATS = VALID_STATIC_FORMATS | {'gif'}

class Asset:
    __doc__ = "Represents a CDN asset on Discord.\n\n    .. container:: operations\n\n        .. describe:: str(x)\n\n            Returns the URL of the CDN asset.\n\n        .. describe:: len(x)\n\n            Returns the length of the CDN asset's URL.\n\n        .. describe:: bool(x)\n\n            Checks if the Asset has a URL.\n\n        .. describe:: x == y\n\n            Checks if the asset is equal to another asset.\n\n        .. describe:: x != y\n\n            Checks if the asset is not equal to another asset.\n\n        .. describe:: hash(x)\n\n            Returns the hash of the asset.\n    "
    __slots__ = ('_state', '_url')
    BASE = 'https://cdn.discordapp.com'

    def __init__(self, state, url=None):
        self._state = state
        self._url = url

    @classmethod
    def _from_avatar(cls, state, user, *, format=None, static_format='webp', size=1024):
        if not utils.valid_icon_size(size):
            raise InvalidArgument('size must be a power of 2 between 16 and 4096')
        else:
            if format is not None:
                if format not in VALID_AVATAR_FORMATS:
                    raise InvalidArgument('format must be None or one of {}'.format(VALID_AVATAR_FORMATS))
            if format == 'gif' and not user.is_avatar_animated():
                raise InvalidArgument('non animated avatars do not support gif format')
        if static_format not in VALID_STATIC_FORMATS:
            raise InvalidArgument('static_format must be one of {}'.format(VALID_STATIC_FORMATS))
        if user.avatar is None:
            return user.default_avatar_url
        if format is None:
            format = 'gif' if user.is_avatar_animated() else static_format
        return cls(state, '/avatars/{0.id}/{0.avatar}.{1}?size={2}'.format(user, format, size))

    @classmethod
    def _from_icon(cls, state, object, path):
        if object.icon is None:
            return cls(state)
        url = '/{0}-icons/{1.id}/{1.icon}.jpg'.format(path, object)
        return cls(state, url)

    @classmethod
    def _from_cover_image(cls, state, obj):
        if obj.cover_image is None:
            return cls(state)
        url = '/app-assets/{0.id}/store/{0.cover_image}.jpg'.format(obj)
        return cls(state, url)

    @classmethod
    def _from_guild_image(cls, state, id, hash, key, *, format='webp', size=1024):
        if not utils.valid_icon_size(size):
            raise InvalidArgument('size must be a power of 2 between 16 and 4096')
        if format not in VALID_STATIC_FORMATS:
            raise InvalidArgument('format must be one of {}'.format(VALID_STATIC_FORMATS))
        if hash is None:
            return cls(state)
        url = '/{key}/{0}/{1}.{2}?size={3}'
        return cls(state, url.format(id, hash, format, size, key=key))

    @classmethod
    def _from_guild_icon(cls, state, guild, *, format=None, static_format='webp', size=1024):
        if not utils.valid_icon_size(size):
            raise InvalidArgument('size must be a power of 2 between 16 and 4096')
        else:
            if format is not None:
                if format not in VALID_AVATAR_FORMATS:
                    raise InvalidArgument('format must be one of {}'.format(VALID_AVATAR_FORMATS))
            if format == 'gif' and not guild.is_icon_animated():
                raise InvalidArgument('non animated guild icons do not support gif format')
        if static_format not in VALID_STATIC_FORMATS:
            raise InvalidArgument('static_format must be one of {}'.format(VALID_STATIC_FORMATS))
        if guild.icon is None:
            return cls(state)
        if format is None:
            format = 'gif' if guild.is_icon_animated() else static_format
        return cls(state, '/icons/{0.id}/{0.icon}.{1}?size={2}'.format(guild, format, size))

    def __str__(self):
        if self._url is not None:
            return self.BASE + self._url
        return ''

    def __len__(self):
        if self._url:
            return len(self.BASE + self._url)
        return 0

    def __bool__(self):
        return self._url is not None

    def __repr__(self):
        return '<Asset url={0._url!r}>'.format(self)

    def __eq__(self, other):
        return isinstance(other, Asset) and self._url == other._url

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._url)

    async def read(self):
        """|coro|

        Retrieves the content of this asset as a :class:`bytes` object.

        .. warning::

            :class:`PartialEmoji` won't have a connection state if user created,
            and a URL won't be present if a custom image isn't associated with
            the asset, e.g. a guild with no custom icon.

        .. versionadded:: 1.1

        Raises
        ------
        DiscordException
            There was no valid URL or internal connection state.
        HTTPException
            Downloading the asset failed.
        NotFound
            The asset was deleted.

        Returns
        -------
        :class:`bytes`
            The content of the asset.
        """
        if not self._url:
            raise DiscordException('Invalid asset (no URL provided)')
        if self._state is None:
            raise DiscordException('Invalid state (no ConnectionState provided)')
        return await self._state.http.get_from_cdn(self.BASE + self._url)

    async def save--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_METHOD              read
                4  CALL_METHOD_0         0  ''
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'data'

 L. 226        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'fp'
               18  LOAD_GLOBAL              io
               20  LOAD_ATTR                IOBase
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    62  'to 62'
               26  LOAD_FAST                'fp'
               28  LOAD_METHOD              writable
               30  CALL_METHOD_0         0  ''
               32  POP_JUMP_IF_FALSE    62  'to 62'

 L. 227        34  LOAD_FAST                'fp'
               36  LOAD_METHOD              write
               38  LOAD_FAST                'data'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'written'

 L. 228        44  LOAD_FAST                'seek_begin'
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L. 229        48  LOAD_FAST                'fp'
               50  LOAD_METHOD              seek
               52  LOAD_CONST               0
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
             58_0  COME_FROM            46  '46'

 L. 230        58  LOAD_FAST                'written'
               60  RETURN_VALUE     
             62_0  COME_FROM            32  '32'
             62_1  COME_FROM            24  '24'

 L. 232        62  LOAD_GLOBAL              open
               64  LOAD_FAST                'fp'
               66  LOAD_STR                 'wb'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH           96  'to 96'
               72  STORE_FAST               'f'

 L. 233        74  LOAD_FAST                'f'
               76  LOAD_METHOD              write
               78  LOAD_FAST                'data'
               80  CALL_METHOD_1         1  ''
               82  POP_BLOCK        
               84  ROT_TWO          
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  POP_FINALLY           0  ''
               94  RETURN_VALUE     
             96_0  COME_FROM_WITH       70  '70'
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 84