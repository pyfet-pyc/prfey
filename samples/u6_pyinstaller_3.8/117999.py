# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\converter.py
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
import re, inspect, discord
from .errors import BadArgument, NoPrivateMessage
__all__ = ('Converter', 'MemberConverter', 'UserConverter', 'MessageConverter', 'TextChannelConverter',
           'InviteConverter', 'RoleConverter', 'GameConverter', 'ColourConverter',
           'VoiceChannelConverter', 'EmojiConverter', 'PartialEmojiConverter', 'CategoryChannelConverter',
           'IDConverter', 'clean_content', 'Greedy')

def _get_from_guilds(bot, getter, argument):
    result = None
    for guild in bot.guilds:
        result = getattr(guild, getter)(argument)
        if result:
            return result
        return result


_utils_get = discord.utils.get

class Converter:
    __doc__ = 'The base class of custom converters that require the :class:`.Context`\n    to be passed to be useful.\n\n    This allows you to implement converters that function similar to the\n    special cased ``discord`` classes.\n\n    Classes that derive from this should override the :meth:`~.Converter.convert`\n    method to do its conversion logic. This method must be a :ref:`coroutine <coroutine>`.\n    '

    async def convert(self, ctx, argument):
        """|coro|

        The method to override to do conversion logic.

        If an error is found while converting, it is recommended to
        raise a :exc:`.CommandError` derived exception as it will
        properly propagate to the error handlers.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context that the argument is being used in.
        argument: :class:`str`
            The argument that is being converted.
        """
        raise NotImplementedError('Derived classes need to implement this.')


class IDConverter(Converter):

    def __init__(self):
        self._id_regex = re.compile('([0-9]{15,21})$')
        super().__init__()

    def _get_id_match(self, argument):
        return self._id_regex.match(argument)


class MemberConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.Member`.\n\n    All lookups are via the local guild. If in a DM context, then the lookup\n    is done by the global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name#discrim\n    4. Lookup by name\n    5. Lookup by nickname\n    '

    async def convert(self, ctx, argument):
        bot = ctx.bot
        match = self._get_id_match(argument) or re.match('<@!?([0-9]+)>$', argument)
        guild = ctx.guild
        result = None
        if match is None:
            if guild:
                result = guild.get_member_named(argument)
            else:
                result = _get_from_guilds(bot, 'get_member_named', argument)
        else:
            user_id = int(match.group(1))
            if guild:
                result = guild.get_member(user_id) or _utils_get((ctx.message.mentions), id=user_id)
            else:
                result = _get_from_guilds(bot, 'get_member', user_id)
        if result is None:
            raise BadArgument('Member "{}" not found'.format(argument))
        return result


class UserConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.User`.\n\n    All lookups are via the global user cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name#discrim\n    4. Lookup by name\n    '

    async def convert(self, ctx, argument):
        match = self._get_id_match(argument) or re.match('<@!?([0-9]+)>$', argument)
        result = None
        state = ctx._state
        if match is not None:
            user_id = int(match.group(1))
            result = ctx.bot.get_user(user_id) or _utils_get((ctx.message.mentions), id=user_id)
        else:
            arg = argument
            if arg[0] == '@':
                arg = arg[1:]
            if len(arg) > 5:
                if arg[(-5)] == '#':
                    discrim = arg[-4:]
                    name = arg[:-5]
                    predicate = lambda u: u.name == name and u.discriminator == discrim
                    result = discord.utils.find(predicate, state._users.values())
                    if result is not None:
                        return result
            predicate = lambda u: u.name == arg
            result = discord.utils.find(predicate, state._users.values())
        if result is None:
            raise BadArgument('User "{}" not found'.format(argument))
        return result


class MessageConverter(Converter):
    __doc__ = 'Converts to a :class:`discord.Message`.\n\n    .. versionadded:: 1.1\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by "{channel ID}-{message ID}" (retrieved by shift-clicking on "Copy ID")\n    2. Lookup by message ID (the message **must** be in the context channel)\n    3. Lookup by message URL\n    '

    async def convert--- This code section failed: ---

 L. 195         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              compile
                4  LOAD_STR                 '^(?:(?P<channel_id>[0-9]{15,21})-)?(?P<message_id>[0-9]{15,21})$'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'id_regex'

 L. 196        10  LOAD_GLOBAL              re
               12  LOAD_METHOD              compile

 L. 197        14  LOAD_STR                 '^https?://(?:(ptb|canary)\\.)?discordapp\\.com/channels/(?:([0-9]{15,21})|(@me))/(?P<channel_id>[0-9]{15,21})/(?P<message_id>[0-9]{15,21})/?$'

 L. 196        16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'link_regex'

 L. 201        20  LOAD_FAST                'id_regex'
               22  LOAD_METHOD              match
               24  LOAD_FAST                'argument'
               26  CALL_METHOD_1         1  ''
               28  JUMP_IF_TRUE_OR_POP    38  'to 38'
               30  LOAD_FAST                'link_regex'
               32  LOAD_METHOD              match
               34  LOAD_FAST                'argument'
               36  CALL_METHOD_1         1  ''
             38_0  COME_FROM            28  '28'
               38  STORE_FAST               'match'

 L. 202        40  LOAD_FAST                'match'
               42  POP_JUMP_IF_TRUE     60  'to 60'

 L. 203        44  LOAD_GLOBAL              BadArgument
               46  LOAD_STR                 'Message "{msg}" not found.'
               48  LOAD_ATTR                format
               50  LOAD_FAST                'argument'
               52  LOAD_CONST               ('msg',)
               54  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            42  '42'

 L. 204        60  LOAD_GLOBAL              int
               62  LOAD_FAST                'match'
               64  LOAD_METHOD              group
               66  LOAD_STR                 'message_id'
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'message_id'

 L. 205        74  LOAD_FAST                'match'
               76  LOAD_METHOD              group
               78  LOAD_STR                 'channel_id'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'channel_id'

 L. 206        84  LOAD_FAST                'ctx'
               86  LOAD_ATTR                bot
               88  LOAD_ATTR                _connection
               90  LOAD_METHOD              _get_message
               92  LOAD_FAST                'message_id'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'message'

 L. 207        98  LOAD_FAST                'message'
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 208       102  LOAD_FAST                'message'
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 209       106  LOAD_FAST                'channel_id'
              108  POP_JUMP_IF_FALSE   126  'to 126'
              110  LOAD_FAST                'ctx'
              112  LOAD_ATTR                bot
              114  LOAD_METHOD              get_channel
              116  LOAD_GLOBAL              int
              118  LOAD_FAST                'channel_id'
              120  CALL_FUNCTION_1       1  ''
              122  CALL_METHOD_1         1  ''
              124  JUMP_FORWARD        130  'to 130'
            126_0  COME_FROM           108  '108'
              126  LOAD_FAST                'ctx'
              128  LOAD_ATTR                channel
            130_0  COME_FROM           124  '124'
              130  STORE_FAST               'channel'

 L. 210       132  LOAD_FAST                'channel'
              134  POP_JUMP_IF_TRUE    152  'to 152'

 L. 211       136  LOAD_GLOBAL              BadArgument
              138  LOAD_STR                 'Channel "{channel}" not found.'
              140  LOAD_ATTR                format
              142  LOAD_FAST                'channel_id'
              144  LOAD_CONST               ('channel',)
              146  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           134  '134'

 L. 212       152  SETUP_FINALLY       172  'to 172'

 L. 213       154  LOAD_FAST                'channel'
              156  LOAD_METHOD              fetch_message
              158  LOAD_FAST                'message_id'
              160  CALL_METHOD_1         1  ''
              162  GET_AWAITABLE    
              164  LOAD_CONST               None
              166  YIELD_FROM       
              168  POP_BLOCK        
              170  RETURN_VALUE     
            172_0  COME_FROM_FINALLY   152  '152'

 L. 214       172  DUP_TOP          
              174  LOAD_GLOBAL              discord
              176  LOAD_ATTR                NotFound
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   208  'to 208'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 215       188  LOAD_GLOBAL              BadArgument
              190  LOAD_STR                 'Message "{msg}" not found.'
              192  LOAD_ATTR                format
              194  LOAD_FAST                'argument'
              196  LOAD_CONST               ('msg',)
              198  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              200  CALL_FUNCTION_1       1  ''
              202  RAISE_VARARGS_1       1  'exception instance'
              204  POP_EXCEPT       
              206  JUMP_FORWARD        248  'to 248'
            208_0  COME_FROM           180  '180'

 L. 216       208  DUP_TOP          
              210  LOAD_GLOBAL              discord
              212  LOAD_ATTR                Forbidden
              214  COMPARE_OP               exception-match
              216  POP_JUMP_IF_FALSE   246  'to 246'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L. 217       224  LOAD_GLOBAL              BadArgument
              226  LOAD_STR                 "Can't read messages in {channel}"
              228  LOAD_ATTR                format
              230  LOAD_FAST                'channel'
              232  LOAD_ATTR                mention
              234  LOAD_CONST               ('channel',)
              236  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              238  CALL_FUNCTION_1       1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           216  '216'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           206  '206'

Parse error at or near `POP_TOP' instruction at offset 184


class TextChannelConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.TextChannel`.\n\n    All lookups are via the local guild. If in a DM context, then the lookup\n    is done by the global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name\n    '

    async def convert(self, ctx, argument):
        bot = ctx.bot
        match = self._get_id_match(argument) or re.match('<#([0-9]+)>$', argument)
        result = None
        guild = ctx.guild
        if match is None:
            if guild:
                result = discord.utils.get((guild.text_channels), name=argument)
            else:

                def check(c):
                    return isinstance(c, discord.TextChannel) and c.name == argument

                result = discord.utils.find(check, bot.get_all_channels())
        else:
            channel_id = int(match.group(1))
            if guild:
                result = guild.get_channel(channel_id)
            else:
                result = _get_from_guilds(bot, 'get_channel', channel_id)
        if not isinstance(result, discord.TextChannel):
            raise BadArgument('Channel "{}" not found.'.format(argument))
        return result


class VoiceChannelConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.VoiceChannel`.\n\n    All lookups are via the local guild. If in a DM context, then the lookup\n    is done by the global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name\n    '

    async def convert(self, ctx, argument):
        bot = ctx.bot
        match = self._get_id_match(argument) or re.match('<#([0-9]+)>$', argument)
        result = None
        guild = ctx.guild
        if match is None:
            if guild:
                result = discord.utils.get((guild.voice_channels), name=argument)
            else:

                def check(c):
                    return isinstance(c, discord.VoiceChannel) and c.name == argument

                result = discord.utils.find(check, bot.get_all_channels())
        else:
            channel_id = int(match.group(1))
            if guild:
                result = guild.get_channel(channel_id)
            else:
                result = _get_from_guilds(bot, 'get_channel', channel_id)
        if not isinstance(result, discord.VoiceChannel):
            raise BadArgument('Channel "{}" not found.'.format(argument))
        return result


class CategoryChannelConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.CategoryChannel`.\n\n    All lookups are via the local guild. If in a DM context, then the lookup\n    is done by the global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name\n    '

    async def convert(self, ctx, argument):
        bot = ctx.bot
        match = self._get_id_match(argument) or re.match('<#([0-9]+)>$', argument)
        result = None
        guild = ctx.guild
        if match is None:
            if guild:
                result = discord.utils.get((guild.categories), name=argument)
            else:

                def check(c):
                    return isinstance(c, discord.CategoryChannel) and c.name == argument

                result = discord.utils.find(check, bot.get_all_channels())
        else:
            channel_id = int(match.group(1))
            if guild:
                result = guild.get_channel(channel_id)
            else:
                result = _get_from_guilds(bot, 'get_channel', channel_id)
        if not isinstance(result, discord.CategoryChannel):
            raise BadArgument('Channel "{}" not found.'.format(argument))
        return result


class ColourConverter(Converter):
    __doc__ = 'Converts to a :class:`~discord.Colour`.\n\n    The following formats are accepted:\n\n    - ``0x<hex>``\n    - ``#<hex>``\n    - ``0x#<hex>``\n    - Any of the ``classmethod`` in :class:`Colour`\n\n        - The ``_`` in the name can be optionally replaced with spaces.\n    '

    async def convert--- This code section failed: ---

 L. 348         0  LOAD_FAST                'argument'
                2  LOAD_METHOD              replace
                4  LOAD_STR                 '0x'
                6  LOAD_STR                 ''
                8  CALL_METHOD_2         2  ''
               10  LOAD_METHOD              lower
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'arg'

 L. 350        16  LOAD_FAST                'arg'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_STR                 '#'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 351        28  LOAD_FAST                'arg'
               30  LOAD_CONST               1
               32  LOAD_CONST               None
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  STORE_FAST               'arg'
             40_0  COME_FROM            26  '26'

 L. 352        40  SETUP_FINALLY       104  'to 104'

 L. 353        42  LOAD_GLOBAL              int
               44  LOAD_FAST                'arg'
               46  LOAD_CONST               16
               48  LOAD_CONST               ('base',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  STORE_FAST               'value'

 L. 354        54  LOAD_CONST               0
               56  LOAD_FAST                'value'
               58  DUP_TOP          
               60  ROT_THREE        
               62  COMPARE_OP               <=
               64  POP_JUMP_IF_FALSE    74  'to 74'
               66  LOAD_CONST               16777215
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_TRUE     90  'to 90'
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            64  '64'
               74  POP_TOP          
             76_0  COME_FROM            72  '72'

 L. 355        76  LOAD_GLOBAL              BadArgument
               78  LOAD_STR                 'Colour "{}" is invalid.'
               80  LOAD_METHOD              format
               82  LOAD_FAST                'arg'
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            70  '70'

 L. 356        90  LOAD_GLOBAL              discord
               92  LOAD_ATTR                Colour
               94  LOAD_FAST                'value'
               96  LOAD_CONST               ('value',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  POP_BLOCK        
              102  RETURN_VALUE     
            104_0  COME_FROM_FINALLY    40  '40'

 L. 357       104  DUP_TOP          
              106  LOAD_GLOBAL              ValueError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   196  'to 196'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 358       118  LOAD_FAST                'arg'
              120  LOAD_METHOD              replace
              122  LOAD_STR                 ' '
              124  LOAD_STR                 '_'
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'arg'

 L. 359       130  LOAD_GLOBAL              getattr
              132  LOAD_GLOBAL              discord
              134  LOAD_ATTR                Colour
              136  LOAD_FAST                'arg'
              138  LOAD_CONST               None
              140  CALL_FUNCTION_3       3  ''
              142  STORE_FAST               'method'

 L. 360       144  LOAD_FAST                'arg'
              146  LOAD_METHOD              startswith
              148  LOAD_STR                 'from_'
              150  CALL_METHOD_1         1  ''
              152  POP_JUMP_IF_TRUE    172  'to 172'
              154  LOAD_FAST                'method'
              156  LOAD_CONST               None
              158  COMPARE_OP               is
              160  POP_JUMP_IF_TRUE    172  'to 172'
              162  LOAD_GLOBAL              inspect
              164  LOAD_METHOD              ismethod
              166  LOAD_FAST                'method'
              168  CALL_METHOD_1         1  ''
              170  POP_JUMP_IF_TRUE    186  'to 186'
            172_0  COME_FROM           160  '160'
            172_1  COME_FROM           152  '152'

 L. 361       172  LOAD_GLOBAL              BadArgument
              174  LOAD_STR                 'Colour "{}" is invalid.'
              176  LOAD_METHOD              format
              178  LOAD_FAST                'arg'
              180  CALL_METHOD_1         1  ''
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           170  '170'

 L. 362       186  LOAD_FAST                'method'
              188  CALL_FUNCTION_0       0  ''
              190  ROT_FOUR         
              192  POP_EXCEPT       
              194  RETURN_VALUE     
            196_0  COME_FROM           110  '110'
              196  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 114


class RoleConverter(IDConverter):
    __doc__ = 'Converts to a :class:`~discord.Role`.\n\n    All lookups are via the local guild. If in a DM context, then the lookup\n    is done by the global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by mention.\n    3. Lookup by name\n    '

    async def convert(self, ctx, argument):
        guild = ctx.guild
        if not guild:
            raise NoPrivateMessage()
        else:
            match = self._get_id_match(argument) or re.match('<@&([0-9]+)>$', argument)
            if match:
                result = guild.get_role(int(match.group(1)))
            else:
                result = discord.utils.get((guild._roles.values()), name=argument)
        if result is None:
            raise BadArgument('Role "{}" not found.'.format(argument))
        return result


class GameConverter(Converter):
    __doc__ = 'Converts to :class:`~discord.Game`.'

    async def convert(self, ctx, argument):
        return discord.Game(name=argument)


class InviteConverter(Converter):
    __doc__ = 'Converts to a :class:`~discord.Invite`.\n\n    This is done via an HTTP request using :meth:`.Bot.fetch_invite`.\n    '

    async def convert(self, ctx, argument):
        try:
            invite = await ctx.bot.fetch_invite(argument)
            return invite
            except Exception as exc:
            try:
                raise BadArgument('Invite is invalid or expired') from exc
            finally:
                exc = None
                del exc


class EmojiConverter(IDConverter):
    __doc__ = "Converts to a :class:`~discord.Emoji`.\n\n    All lookups are done for the local guild first, if available. If that lookup\n    fails, then it checks the client's global cache.\n\n    The lookup strategy is as follows (in order):\n\n    1. Lookup by ID.\n    2. Lookup by extracting ID from the emoji.\n    3. Lookup by name\n    "

    async def convert(self, ctx, argument):
        match = self._get_id_match(argument) or re.match('<a?:[a-zA-Z0-9\\_]+:([0-9]+)>$', argument)
        result = None
        bot = ctx.bot
        guild = ctx.guild
        if match is None:
            if guild:
                result = discord.utils.get((guild.emojis), name=argument)
            if result is None:
                result = discord.utils.get((bot.emojis), name=argument)
        else:
            emoji_id = int(match.group(1))
            if guild:
                result = discord.utils.get((guild.emojis), id=emoji_id)
            if result is None:
                result = discord.utils.get((bot.emojis), id=emoji_id)
        if result is None:
            raise BadArgument('Emoji "{}" not found.'.format(argument))
        return result


class PartialEmojiConverter(Converter):
    __doc__ = 'Converts to a :class:`~discord.PartialEmoji`.\n\n    This is done by extracting the animated flag, name and ID from the emoji.\n    '

    async def convert(self, ctx, argument):
        match = re.match('<(a?):([a-zA-Z0-9\\_]+):([0-9]+)>$', argument)
        if match:
            emoji_animated = bool(match.group(1))
            emoji_name = match.group(2)
            emoji_id = int(match.group(3))
            return discord.PartialEmoji.with_state((ctx.bot._connection), animated=emoji_animated, name=emoji_name, id=emoji_id)
        raise BadArgument('Couldn\'t convert "{}" to PartialEmoji.'.format(argument))


class clean_content(Converter):
    __doc__ = 'Converts the argument to mention scrubbed version of\n    said content.\n\n    This behaves similarly to :attr:`~discord.Message.clean_content`.\n\n    Attributes\n    ------------\n    fix_channel_mentions: :class:`bool`\n        Whether to clean channel mentions.\n    use_nicknames: :class:`bool`\n        Whether to use nicknames when transforming mentions.\n    escape_markdown: :class:`bool`\n        Whether to also escape special markdown characters.\n    '

    def __init__(self, *, fix_channel_mentions=False, use_nicknames=True, escape_markdown=False):
        self.fix_channel_mentions = fix_channel_mentions
        self.use_nicknames = use_nicknames
        self.escape_markdown = escape_markdown

    async def convert(self, ctx, argument):
        message = ctx.message
        transformations = {}
        if self.fix_channel_mentions:
            if ctx.guild:

                def resolve_channel(id, *, _get=ctx.guild.get_channel):
                    ch = _get(id)
                    return ('<#%s>' % id, '#' + ch.name if ch else '#deleted-channel')

                transformations.update((resolve_channel(channel) for channel in message.raw_channel_mentions))
        if self.use_nicknames and ctx.guild:

            def resolve_member(id, *, _get=ctx.guild.get_member):
                m = _get(id)
                if m:
                    return '@' + m.display_name
                return '@deleted-user'

        else:

            def resolve_member(id, *, _get=ctx.bot.get_user):
                m = _get(id)
                if m:
                    return '@' + m.name
                return '@deleted-user'

        transformations.update(((
         '<@%s>' % member_id, resolve_member(member_id)) for member_id in message.raw_mentions))
        transformations.update(((
         '<@!%s>' % member_id, resolve_member(member_id)) for member_id in message.raw_mentions))
        if ctx.guild:

            def resolve_role(_id, *, _find=ctx.guild.get_role):
                r = _find(_id)
                if r:
                    return '@' + r.name
                return '@deleted-role'

            transformations.update(((
             '<@&%s>' % role_id, resolve_role(role_id)) for role_id in message.raw_role_mentions))

        def repl(obj):
            return transformations.get(obj.group(0), '')

        pattern = re.compile('|'.join(transformations.keys()))
        result = pattern.sub(repl, argument)
        if self.escape_markdown:
            result = discord.utils.escape_markdown(result)
        return discord.utils.escape_mentions(result)


class _Greedy:
    __slots__ = ('converter', )

    def __init__(self, *, converter=None):
        self.converter = converter

    def __getitem__(self, params):
        if not isinstance(params, tuple):
            params = (
             params,)
        else:
            if len(params) != 1:
                raise TypeError('Greedy[...] only takes a single argument')
            converter = params[0]
            if not callable(converter):
                if not isinstance(converter, Converter):
                    if not hasattr(converter, '__origin__'):
                        raise TypeError('Greedy[...] expects a type or a Converter instance.')
        if converter is str or converter is type(None) or converter is _Greedy:
            raise TypeError('Greedy[%s] is invalid.' % converter.__name__)
        return self.__class__(converter=converter)


Greedy = _Greedy()