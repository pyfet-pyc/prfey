# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\state.py
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
import asyncio
from collections import deque, namedtuple, OrderedDict
import copy, datetime, itertools, logging, math, weakref, inspect, gc
from .guild import Guild
from .activity import BaseActivity
from .user import User, ClientUser
from .emoji import Emoji
from .partial_emoji import PartialEmoji
from .message import Message
from .relationship import Relationship
from .channel import *
from .raw_models import *
from .member import Member
from .role import Role
from .enums import ChannelType, try_enum, Status, Enum
from . import utils
from .embeds import Embed
from .object import Object
from .invite import Invite

class ListenerType(Enum):
    chunk = 0
    query_members = 1


Listener = namedtuple('Listener', ('type', 'future', 'predicate'))
log = logging.getLogger(__name__)
ReadyState = namedtuple('ReadyState', ('launch', 'guilds'))

class ConnectionState:

    def __init__(self, *, dispatch, chunker, handlers, syncer, http, loop, **options):
        self.loop = loop
        self.http = http
        self.max_messages = options.get('max_messages', 1000)
        if self.max_messages is not None:
            if self.max_messages <= 0:
                self.max_messages = 1000
        self.dispatch = dispatch
        self.chunker = chunker
        self.syncer = syncer
        self.is_bot = None
        self.handlers = handlers
        self.shard_count = None
        self._ready_task = None
        self._fetch_offline = options.get('fetch_offline_members', True)
        self.heartbeat_timeout = options.get('heartbeat_timeout', 60.0)
        self.guild_subscriptions = options.get('guild_subscriptions', True)
        self._cache_members = self._fetch_offline or self.guild_subscriptions
        self._listeners = []
        activity = options.get('activity', None)
        if activity:
            if not isinstance(activity, BaseActivity):
                raise TypeError('activity parameter must derive from BaseActivity.')
            activity = activity.to_dict()
        status = options.get('status', None)
        if status:
            if status is Status.offline:
                status = 'invisible'
            else:
                status = str(status)
        self._activity = activity
        self._status = status
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse_'):
                parsers[attr[6:].upper()] = func
        else:
            self.clear()

    def clear(self):
        self.user = None
        self._users = weakref.WeakValueDictionary()
        self._emojis = {}
        self._calls = {}
        self._guilds = {}
        self._voice_clients = {}
        self._private_channels = OrderedDict()
        self._private_channels_by_user = {}
        self._messages = self.max_messages and deque(maxlen=(self.max_messages))
        gc.collect()

    def process_listeners(self, listener_type, argument, result):
        removed = []
        for i, listener in enumerate(self._listeners):
            if listener.type != listener_type:
                pass
            else:
                future = listener.future
                if future.cancelled():
                    removed.append(i)
        else:
            try:
                passed = listener.predicate(argument)
            except Exception as exc:
                try:
                    future.set_exception(exc)
                    removed.append(i)
                finally:
                    exc = None
                    del exc

            else:
                if passed:
                    future.set_result(result)
                    removed.append(i)
                    if listener.type == ListenerType.chunk:
                        break
                for index in reversed(removed):
                    del self._listeners[index]

    def call_handlers(self, key, *args, **kwargs):
        try:
            func = self.handlers[key]
        except KeyError:
            pass
        else:
            func(*args, **kwargs)

    @property
    def self_id(self):
        u = self.user
        if u:
            return u.id

    @property
    def voice_clients(self):
        return list(self._voice_clients.values())

    def _get_voice_client(self, guild_id):
        return self._voice_clients.get(guild_id)

    def _add_voice_client(self, guild_id, voice):
        self._voice_clients[guild_id] = voice

    def _remove_voice_client(self, guild_id):
        self._voice_clients.pop(guild_id, None)

    def _update_references(self, ws):
        for vc in self.voice_clients:
            vc.main_ws = ws

    def store_user(self, data):
        user_id = int(data['id'])
        try:
            return self._users[user_id]
        except KeyError:
            user = User(state=self, data=data)
            if user.discriminator != '0000':
                self._users[user_id] = user
            return user

    def get_user(self, id):
        return self._users.get(id)

    def store_emoji(self, guild, data):
        emoji_id = int(data['id'])
        self._emojis[emoji_id] = emoji = Emoji(guild=guild, state=self, data=data)
        return emoji

    @property
    def guilds(self):
        return list(self._guilds.values())

    def _get_guild(self, guild_id):
        return self._guilds.get(guild_id)

    def _add_guild(self, guild):
        self._guilds[guild.id] = guild

    def _remove_guild(self, guild):
        self._guilds.pop(guild.id, None)
        for emoji in guild.emojis:
            self._emojis.pop(emoji.id, None)
        else:
            del guild
            gc.collect()

    @property
    def emojis(self):
        return list(self._emojis.values())

    def get_emoji(self, emoji_id):
        return self._emojis.get(emoji_id)

    @property
    def private_channels(self):
        return list(self._private_channels.values())

    def _get_private_channel(self, channel_id):
        try:
            value = self._private_channels[channel_id]
        except KeyError:
            return
        else:
            self._private_channels.move_to_end(channel_id)
            return value

    def _get_private_channel_by_user(self, user_id):
        return self._private_channels_by_user.get(user_id)

    def _add_private_channel(self, channel):
        channel_id = channel.id
        self._private_channels[channel_id] = channel
        if self.is_bot:
            if len(self._private_channels) > 128:
                _, to_remove = self._private_channels.popitem(last=False)
                if isinstance(to_remove, DMChannel):
                    self._private_channels_by_user.pop(to_remove.recipient.id, None)
        if isinstance(channel, DMChannel):
            self._private_channels_by_user[channel.recipient.id] = channel

    def add_dm_channel(self, data):
        channel = DMChannel(me=(self.user), state=self, data=data)
        self._add_private_channel(channel)
        return channel

    def _remove_private_channel(self, channel):
        self._private_channels.pop(channel.id, None)
        if isinstance(channel, DMChannel):
            self._private_channels_by_user.pop(channel.recipient.id, None)

    def _get_message(self, msg_id):
        if self._messages:
            return utils.find(lambda m: m.id == msg_id, reversed(self._messages))

    def _add_guild_from_data(self, guild):
        guild = Guild(data=guild, state=self)
        self._add_guild(guild)
        return guild

    def chunks_needed(self, guild):
        for _ in range(math.ceil(guild._member_count / 1000)):
            yield self.receive_chunk(guild.id)

    def _get_guild_channel(self, data):
        channel_id = int(data['channel_id'])
        try:
            guild = self._get_guild(int(data['guild_id']))
        except KeyError:
            channel = self.get_channel(channel_id)
            guild = None
        else:
            channel = guild and guild.get_channel(channel_id)
        return (
         channel or Object(id=channel_id), guild)

    async def request_offline_members(self, guilds):
        chunks = []
        for guild in guilds:
            chunks.extend(self.chunks_needed(guild))
        else:
            splits = [guilds[i:i + 75] for i in range(0, len(guilds), 75)]
            for split in splits:
                await self.chunker(split)
            else:
                if chunks:
                    try:
                        await utils.sane_wait_for(chunks, timeout=(len(chunks) * 30.0))
                    except asyncio.TimeoutError:
                        log.info('Somehow timed out waiting for chunks.')

    async def query_members(self, guild, query, limit, cache):
        guild_id = guild.id
        ws = self._get_websocket(guild_id)
        if ws is None:
            raise RuntimeError('Somehow do not have a websocket for this guild_id')
        future = self.receive_member_query(guild_id, query)
        try:
            await ws.request_chunks(guild_id, query, limit)
            members = await asyncio.wait_for(future, timeout=5.0)
            if cache:
                for member in members:
                    guild._add_member(member)

            return members
        except asyncio.TimeoutError:
            log.info('Timed out waiting for chunks with query %r and limit %d for guild_id %d', query, limit, guild_id)
            raise

    async def _delay_ready(self):
        try:
            try:
                launch = self._ready_state.launch
                if self.is_bot:
                    while True:
                        try:
                            await asyncio.wait_for((launch.wait()), timeout=2.0)
                        except asyncio.TimeoutError:
                            break
                        else:
                            launch.clear()

                    guilds = next(zip(*self._ready_state.guilds), [])
                    if self._fetch_offline:
                        await self.request_offline_members(guilds)
                    for guild, unavailable in self._ready_state.guilds:
                        if unavailable is False:
                            self.dispatch('guild_available', guild)
                        else:
                            self.dispatch('guild_join', guild)

                try:
                    del self._ready_state
                except AttributeError:
                    pass
                else:
                    if not self.is_bot:
                        log.info('Requesting GUILD_SYNC for %s guilds', len(self.guilds))
                        await self.syncer([s.id for s in self.guilds])
            except asyncio.CancelledError:
                pass
            else:
                self.call_handlers('ready')
                self.dispatch('ready')
        finally:
            self._ready_task = None

    def parse_ready--- This code section failed: ---

 L. 384         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ready_task
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 385        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _ready_task
               14  LOAD_METHOD              cancel
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          
             20_0  COME_FROM             8  '8'

 L. 387        20  LOAD_GLOBAL              ReadyState
               22  LOAD_GLOBAL              asyncio
               24  LOAD_METHOD              Event
               26  CALL_METHOD_0         0  ''
               28  BUILD_LIST_0          0 
               30  LOAD_CONST               ('launch', 'guilds')
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _ready_state

 L. 388        38  LOAD_FAST                'self'
               40  LOAD_METHOD              clear
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L. 389        46  LOAD_GLOBAL              ClientUser
               48  LOAD_FAST                'self'
               50  LOAD_FAST                'data'
               52  LOAD_STR                 'user'
               54  BINARY_SUBSCR    
               56  LOAD_CONST               ('state', 'data')
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  DUP_TOP          
               62  LOAD_FAST                'self'
               64  STORE_ATTR               user
               66  STORE_FAST               'user'

 L. 390        68  LOAD_FAST                'user'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _users
               74  LOAD_FAST                'user'
               76  LOAD_ATTR                id
               78  STORE_SUBSCR     

 L. 392        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _ready_state
               84  LOAD_ATTR                guilds
               86  STORE_FAST               'guilds'

 L. 393        88  LOAD_FAST                'data'
               90  LOAD_STR                 'guilds'
               92  BINARY_SUBSCR    
               94  GET_ITER         
             96_0  COME_FROM           144  '144'
             96_1  COME_FROM           126  '126'
               96  FOR_ITER            146  'to 146'
               98  STORE_FAST               'guild_data'

 L. 394       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _add_guild_from_data
              104  LOAD_FAST                'guild_data'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'guild'

 L. 395       110  LOAD_FAST                'self'
              112  LOAD_ATTR                is_bot
              114  POP_JUMP_IF_TRUE    122  'to 122'
              116  LOAD_FAST                'guild'
              118  LOAD_ATTR                unavailable
              120  POP_JUMP_IF_FALSE   128  'to 128'
            122_0  COME_FROM           114  '114'
              122  LOAD_FAST                'guild'
              124  LOAD_ATTR                large
              126  POP_JUMP_IF_FALSE_BACK    96  'to 96'
            128_0  COME_FROM           120  '120'

 L. 396       128  LOAD_FAST                'guilds'
              130  LOAD_METHOD              append
              132  LOAD_FAST                'guild'
              134  LOAD_FAST                'guild'
              136  LOAD_ATTR                unavailable
              138  BUILD_TUPLE_2         2 
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK            96  'to 96'
            146_0  COME_FROM            96  '96'

 L. 398       146  LOAD_FAST                'data'
              148  LOAD_METHOD              get
              150  LOAD_STR                 'relationships'
              152  BUILD_LIST_0          0 
              154  CALL_METHOD_2         2  ''
              156  GET_ITER         
            158_0  COME_FROM           222  '222'
            158_1  COME_FROM           200  '200'
            158_2  COME_FROM           196  '196'
              158  FOR_ITER            224  'to 224'
              160  STORE_FAST               'relationship'

 L. 399       162  SETUP_FINALLY       180  'to 180'

 L. 400       164  LOAD_GLOBAL              int
              166  LOAD_FAST                'relationship'
              168  LOAD_STR                 'id'
              170  BINARY_SUBSCR    
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'r_id'
              176  POP_BLOCK        
              178  JUMP_FORWARD        204  'to 204'
            180_0  COME_FROM_FINALLY   162  '162'

 L. 401       180  DUP_TOP          
              182  LOAD_GLOBAL              KeyError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   202  'to 202'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 402       194  POP_EXCEPT       
              196  JUMP_BACK           158  'to 158'
              198  POP_EXCEPT       
              200  JUMP_BACK           158  'to 158'
            202_0  COME_FROM           186  '186'
              202  END_FINALLY      
            204_0  COME_FROM           178  '178'

 L. 404       204  LOAD_GLOBAL              Relationship
              206  LOAD_FAST                'self'
              208  LOAD_FAST                'relationship'
              210  LOAD_CONST               ('state', 'data')
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  LOAD_FAST                'user'
              216  LOAD_ATTR                _relationships
              218  LOAD_FAST                'r_id'
              220  STORE_SUBSCR     
              222  JUMP_BACK           158  'to 158'
            224_0  COME_FROM           158  '158'

 L. 406       224  LOAD_FAST                'data'
              226  LOAD_METHOD              get
              228  LOAD_STR                 'private_channels'
              230  BUILD_LIST_0          0 
              232  CALL_METHOD_2         2  ''
              234  GET_ITER         
            236_0  COME_FROM           276  '276'
              236  FOR_ITER            278  'to 278'
              238  STORE_FAST               'pm'

 L. 407       240  LOAD_GLOBAL              _channel_factory
              242  LOAD_FAST                'pm'
              244  LOAD_STR                 'type'
              246  BINARY_SUBSCR    
              248  CALL_FUNCTION_1       1  ''
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'factory'
              254  STORE_FAST               '_'

 L. 408       256  LOAD_FAST                'self'
              258  LOAD_METHOD              _add_private_channel
              260  LOAD_FAST                'factory'
              262  LOAD_FAST                'user'
              264  LOAD_FAST                'pm'
              266  LOAD_FAST                'self'
              268  LOAD_CONST               ('me', 'data', 'state')
              270  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK           236  'to 236'
            278_0  COME_FROM           236  '236'

 L. 410       278  LOAD_FAST                'self'
              280  LOAD_METHOD              dispatch
              282  LOAD_STR                 'connect'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 411       288  LOAD_GLOBAL              asyncio
              290  LOAD_ATTR                ensure_future
              292  LOAD_FAST                'self'
              294  LOAD_METHOD              _delay_ready
              296  CALL_METHOD_0         0  ''
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                loop
              302  LOAD_CONST               ('loop',)
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              306  LOAD_FAST                'self'
              308  STORE_ATTR               _ready_task

Parse error at or near `JUMP_BACK' instruction at offset 200

    def parse_resumed(self, data):
        self.dispatch('resumed')

    def parse_message_create(self, data):
        channel, _ = self._get_guild_channel(data)
        message = Message(channel=channel, data=data, state=self)
        self.dispatch('message', message)
        if self._messages is not None:
            self._messages.append(message)
        if channel:
            if channel.__class__ is TextChannel:
                channel.last_message_id = message.id

    def parse_message_delete(self, data):
        raw = RawMessageDeleteEvent(data)
        found = self._get_message(raw.message_id)
        raw.cached_message = found
        self.dispatch('raw_message_delete', raw)
        if self._messages is not None:
            if found is not None:
                self.dispatch('message_delete', found)
                self._messages.remove(found)

    def parse_message_delete_bulk(self, data):
        raw = RawBulkMessageDeleteEvent(data)
        if self._messages:
            found_messages = [message for message in self._messages if message.id in raw.message_ids]
        else:
            found_messages = []
        raw.cached_messages = found_messages
        self.dispatch('raw_bulk_message_delete', raw)
        if found_messages:
            self.dispatch('bulk_message_delete', found_messages)
            for msg in found_messages:
                self._messages.remove(msg)

    def parse_message_update(self, data):
        raw = RawMessageUpdateEvent(data)
        message = self._get_message(raw.message_id)
        if message is not None:
            older_message = copy.copy(message)
            raw.cached_message = older_message
            self.dispatch('raw_message_edit', raw)
            message._update(data)
            self.dispatch('message_edit', older_message, message)
        else:
            self.dispatch('raw_message_edit', raw)

    def parse_message_reaction_add(self, data):
        emoji = data['emoji']
        emoji_id = utils._get_as_snowflake(emoji, 'id')
        emoji = PartialEmoji.with_state(self, animated=(emoji.get('animated', False)), id=emoji_id, name=(emoji['name']))
        raw = RawReactionActionEvent(data, emoji, 'REACTION_ADD')
        member_data = data.get('member')
        if member_data:
            guild = self._get_guild(raw.guild_id)
            raw.member = Member(data=member_data, guild=guild, state=self)
        else:
            raw.member = None
        self.dispatch('raw_reaction_add', raw)
        message = self._get_message(raw.message_id)
        if message is not None:
            emoji = self._upgrade_partial_emoji(emoji)
            reaction = message._add_reaction(data, emoji, raw.user_id)
            user = raw.member or self._get_reaction_user(message.channel, raw.user_id)
            if user:
                self.dispatch('reaction_add', reaction, user)

    def parse_message_reaction_remove_all(self, data):
        raw = RawReactionClearEvent(data)
        self.dispatch('raw_reaction_clear', raw)
        message = self._get_message(raw.message_id)
        if message is not None:
            old_reactions = message.reactions.copy()
            message.reactions.clear()
            self.dispatch('reaction_clear', message, old_reactions)

    def parse_message_reaction_remove(self, data):
        emoji = data['emoji']
        emoji_id = utils._get_as_snowflake(emoji, 'id')
        emoji = PartialEmoji.with_state(self, animated=(emoji.get('animated', False)), id=emoji_id, name=(emoji['name']))
        raw = RawReactionActionEvent(data, emoji, 'REACTION_REMOVE')
        self.dispatch('raw_reaction_remove', raw)
        message = self._get_message(raw.message_id)
        if message is not None:
            emoji = self._upgrade_partial_emoji(emoji)
            try:
                reaction = message._remove_reaction(data, emoji, raw.user_id)
            except (AttributeError, ValueError):
                pass
            else:
                user = self._get_reaction_user(message.channel, raw.user_id)
                if user:
                    self.dispatch('reaction_remove', reaction, user)

    def parse_message_reaction_remove_emoji(self, data):
        emoji = data['emoji']
        emoji_id = utils._get_as_snowflake(emoji, 'id')
        emoji = PartialEmoji.with_state(self, animated=(emoji.get('animated', False)), id=emoji_id, name=(emoji['name']))
        raw = RawReactionClearEmojiEvent(data, emoji)
        self.dispatch('raw_reaction_clear_emoji', raw)
        message = self._get_message(raw.message_id)
        if message is not None:
            try:
                reaction = message._clear_emoji(emoji)
            except (AttributeError, ValueError):
                pass
            else:
                if reaction:
                    self.dispatch('reaction_clear_emoji', reaction)

    def parse_presence_update(self, data):
        guild_id = utils._get_as_snowflake(data, 'guild_id')
        guild = self._get_guild(guild_id)
        if guild is None:
            log.warning('PRESENCE_UPDATE referencing an unknown guild ID: %s. Discarding.', guild_id)
            return
        user = data['user']
        member_id = int(user['id'])
        member = guild.get_member(member_id)
        if member is None:
            if 'username' not in user:
                return
            member, old_member = Member._from_presence_update(guild=guild, data=data, state=self)
            guild._add_member(member)
        else:
            old_member = Member._copy(member)
            user_update = member._presence_update(data=data, user=user)
            if user_update:
                self.dispatch('user_update', user_update[0], user_update[1])
        self.dispatch('member_update', old_member, member)

    def parse_user_update(self, data):
        self.user._update(data)

    def parse_invite_create(self, data):
        invite = Invite.from_gateway(state=self, data=data)
        self.dispatch('invite_create', invite)

    def parse_invite_delete(self, data):
        invite = Invite.from_gateway(state=self, data=data)
        self.dispatch('invite_delete', invite)

    def parse_channel_delete(self, data):
        guild = self._get_guild(utils._get_as_snowflake(data, 'guild_id'))
        channel_id = int(data['id'])
        if guild is not None:
            channel = guild.get_channel(channel_id)
            if channel is not None:
                guild._remove_channel(channel)
                self.dispatch('guild_channel_delete', channel)
        else:
            channel = self._get_private_channel(channel_id)
            if channel is not None:
                self._remove_private_channel(channel)
                self.dispatch('private_channel_delete', channel)

    def parse_channel_update(self, data):
        channel_type = try_enum(ChannelType, data.get('type'))
        channel_id = int(data['id'])
        if channel_type is ChannelType.group:
            channel = self._get_private_channel(channel_id)
            old_channel = copy.copy(channel)
            channel._update_group(data)
            self.dispatch('private_channel_update', old_channel, channel)
            return
        guild_id = utils._get_as_snowflake(data, 'guild_id')
        guild = self._get_guild(guild_id)
        if guild is not None:
            channel = guild.get_channel(channel_id)
            if channel is not None:
                old_channel = copy.copy(channel)
                channel._update(guild, data)
                self.dispatch('guild_channel_update', old_channel, channel)
            else:
                log.warning('CHANNEL_UPDATE referencing an unknown channel ID: %s. Discarding.', channel_id)
        else:
            log.warning('CHANNEL_UPDATE referencing an unknown guild ID: %s. Discarding.', guild_id)

    def parse_channel_create(self, data):
        factory, ch_type = _channel_factory(data['type'])
        if factory is None:
            log.warning('CHANNEL_CREATE referencing an unknown channel type %s. Discarding.', data['type'])
            return
        channel = None
        if ch_type in (ChannelType.group, ChannelType.private):
            channel_id = int(data['id'])
            if self._get_private_channel(channel_id) is None:
                channel = factory(me=(self.user), data=data, state=self)
                self._add_private_channel(channel)
                self.dispatch('private_channel_create', channel)
        else:
            guild_id = utils._get_as_snowflake(data, 'guild_id')
            guild = self._get_guild(guild_id)
            if guild is not None:
                channel = factory(guild=guild, state=self, data=data)
                guild._add_channel(channel)
                self.dispatch('guild_channel_create', channel)
            else:
                log.warning('CHANNEL_CREATE referencing an unknown guild ID: %s. Discarding.', guild_id)
                return

    def parse_channel_pins_update(self, data):
        channel_id = int(data['channel_id'])
        channel = self.get_channel(channel_id)
        if channel is None:
            log.warning('CHANNEL_PINS_UPDATE referencing an unknown channel ID: %s. Discarding.', channel_id)
            return
        last_pin = utils.parse_time(data['last_pin_timestamp']) if data['last_pin_timestamp'] else None
        try:
            channel.guild
        except AttributeError:
            self.dispatch('private_channel_pins_update', channel, last_pin)
        else:
            self.dispatch('guild_channel_pins_update', channel, last_pin)

    def parse_channel_recipient_add(self, data):
        channel = self._get_private_channel(int(data['channel_id']))
        user = self.store_user(data['user'])
        channel.recipients.append(user)
        self.dispatch('group_join', channel, user)

    def parse_channel_recipient_remove(self, data):
        channel = self._get_private_channel(int(data['channel_id']))
        user = self.store_user(data['user'])
        try:
            channel.recipients.remove(user)
        except ValueError:
            pass
        else:
            self.dispatch('group_remove', channel, user)

    def parse_guild_member_add(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is None:
            log.warning('GUILD_MEMBER_ADD referencing an unknown guild ID: %s. Discarding.', data['guild_id'])
            return
        member = Member(guild=guild, data=data, state=self)
        if self._cache_members:
            guild._add_member(member)
        guild._member_count += 1
        self.dispatch('member_join', member)

    def parse_guild_member_remove(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            user_id = int(data['user']['id'])
            member = guild.get_member(user_id)
            if member is not None:
                guild._remove_member(member)
                guild._member_count -= 1
                self.dispatch('member_remove', member)
        else:
            log.warning('GUILD_MEMBER_REMOVE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])

    def parse_guild_member_update(self, data):
        guild = self._get_guild(int(data['guild_id']))
        user = data['user']
        user_id = int(user['id'])
        if guild is None:
            log.warning('GUILD_MEMBER_UPDATE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])
            return
        member = guild.get_member(user_id)
        if member is not None:
            old_member = copy.copy(member)
            member._update(data)
            self.dispatch('member_update', old_member, member)
        else:
            log.warning('GUILD_MEMBER_UPDATE referencing an unknown member ID: %s. Discarding.', user_id)

    def parse_guild_emojis_update(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is None:
            log.warning('GUILD_EMOJIS_UPDATE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])
            return
        before_emojis = guild.emojis
        for emoji in before_emojis:
            self._emojis.pop(emoji.id, None)
        else:
            guild.emojis = tuple(map(lambda d: self.store_emoji(guild, d), data['emojis']))
            self.dispatch('guild_emojis_update', guild, before_emojis, guild.emojis)

    def _get_create_guild(self, data):
        if data.get('unavailable') is False:
            guild = self._get_guild(int(data['id']))
            if guild is not None:
                guild.unavailable = False
                guild._from_data(data)
                return guild
        return self._add_guild_from_data(data)

    async def _chunk_and_dispatch(self, guild, unavailable):
        chunks = list(self.chunks_needed(guild))
        await self.chunker(guild)
        if chunks:
            try:
                await utils.sane_wait_for(chunks, timeout=(len(chunks)))
            except asyncio.TimeoutError:
                log.info('Somehow timed out waiting for chunks.')

        if unavailable is False:
            self.dispatch('guild_available', guild)
        else:
            self.dispatch('guild_join', guild)

    def parse_guild_create(self, data):
        unavailable = data.get('unavailable')
        if unavailable is True:
            return
        guild = self._get_create_guild(data)
        if guild.large:
            if unavailable is False:
                try:
                    state = self._ready_state
                    state.launch.set()
                    state.guilds.append((guild, unavailable))
                except AttributeError:
                    pass
                else:
                    return
                if self._fetch_offline:
                    asyncio.ensure_future((self._chunk_and_dispatch(guild, unavailable)), loop=(self.loop))
                    return
        if unavailable is False:
            self.dispatch('guild_available', guild)
        else:
            self.dispatch('guild_join', guild)

    def parse_guild_sync(self, data):
        guild = self._get_guild(int(data['id']))
        guild._sync(data)

    def parse_guild_update(self, data):
        guild = self._get_guild(int(data['id']))
        if guild is not None:
            old_guild = copy.copy(guild)
            guild._from_data(data)
            self.dispatch('guild_update', old_guild, guild)
        else:
            log.warning('GUILD_UPDATE referencing an unknown guild ID: %s. Discarding.', data['id'])

    def parse_guild_delete(self, data):
        guild = self._get_guild(int(data['id']))
        if guild is None:
            log.warning('GUILD_DELETE referencing an unknown guild ID: %s. Discarding.', data['id'])
            return
        if data.get('unavailable', False):
            if guild is not None:
                guild.unavailable = True
                self.dispatch('guild_unavailable', guild)
                return
        if self._messages is not None:
            self._messages = deque((msg for msg in self._messages if msg.guild != guild), maxlen=(self.max_messages))
        self._remove_guild(guild)
        self.dispatch('guild_remove', guild)

    def parse_guild_ban_add(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            try:
                user = User(data=(data['user']), state=self)
            except KeyError:
                pass
            else:
                member = guild.get_member(user.id) or user
                self.dispatch('member_ban', guild, member)

    def parse_guild_ban_remove(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            if 'user' in data:
                user = self.store_user(data['user'])
                self.dispatch('member_unban', guild, user)

    def parse_guild_role_create(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is None:
            log.warning('GUILD_ROLE_CREATE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])
            return
        role_data = data['role']
        role = Role(guild=guild, data=role_data, state=self)
        guild._add_role(role)
        self.dispatch('guild_role_create', role)

    def parse_guild_role_delete(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            role_id = int(data['role_id'])
            try:
                role = guild._remove_role(role_id)
            except KeyError:
                return
            else:
                self.dispatch('guild_role_delete', role)
        else:
            log.warning('GUILD_ROLE_DELETE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])

    def parse_guild_role_update(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            role_data = data['role']
            role_id = int(role_data['id'])
            role = guild.get_role(role_id)
            if role is not None:
                old_role = copy.copy(role)
                role._update(role_data)
                self.dispatch('guild_role_update', old_role, role)
        else:
            log.warning('GUILD_ROLE_UPDATE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])

    def parse_guild_members_chunk(self, data):
        guild_id = int(data['guild_id'])
        guild = self._get_guild(guild_id)
        members = [Member(guild=guild, data=member, state=self) for member in data.get('members', [])]
        log.info('Processed a chunk for %s members in guild ID %s.', len(members), guild_id)
        if self._cache_members:
            for member in members:
                existing = guild.get_member(member.id)
                if not existing is None:
                    if existing.joined_at is None:
                        pass
                guild._add_member(member)

        self.process_listeners(ListenerType.chunk, guild, len(members))
        names = [x.name.lower() for x in members]
        self.process_listeners(ListenerType.query_members, (guild_id, names), members)

    def parse_guild_integrations_update(self, data):
        guild = self._get_guild(int(data['guild_id']))
        if guild is not None:
            self.dispatch('guild_integrations_update', guild)
        else:
            log.warning('GUILD_INTEGRATIONS_UPDATE referencing an unknown guild ID: %s. Discarding.', data['guild_id'])

    def parse_webhooks_update(self, data):
        channel = self.get_channel(int(data['channel_id']))
        if channel is not None:
            self.dispatch('webhooks_update', channel)
        else:
            log.warning('WEBHOOKS_UPDATE referencing an unknown channel ID: %s. Discarding.', data['channel_id'])

    def parse_voice_state_update(self, data):
        guild = self._get_guild(utils._get_as_snowflake(data, 'guild_id'))
        channel_id = utils._get_as_snowflake(data, 'channel_id')
        if guild is not None:
            if int(data['user_id']) == self.user.id:
                voice = self._get_voice_client(guild.id)
                if voice is not None:
                    ch = guild.get_channel(channel_id)
                    if ch is not None:
                        voice.channel = ch
            member, before, after = guild._update_voice_state(data, channel_id)
            if member is not None:
                self.dispatch('voice_state_update', member, before, after)
            else:
                log.warning('VOICE_STATE_UPDATE referencing an unknown member ID: %s. Discarding.', data['user_id'])
        else:
            call = self._calls.get(channel_id)
            if call is not None:
                call._update_voice_state(data)

    def parse_voice_server_update(self, data):
        try:
            key_id = int(data['guild_id'])
        except KeyError:
            key_id = int(data['channel_id'])
        else:
            vc = self._get_voice_client(key_id)
            if vc is not None:
                asyncio.ensure_future(vc._create_socket(key_id, data))

    def parse_typing_start(self, data):
        channel, guild = self._get_guild_channel(data)
        if channel is not None:
            member = None
            user_id = utils._get_as_snowflake(data, 'user_id')
            if isinstance(channel, DMChannel):
                member = channel.recipient
            elif isinstance(channel, TextChannel) and guild is not None:
                member = guild.get_member(user_id)
            elif isinstance(channel, GroupChannel):
                member = utils.find(lambda x: x.id == user_id, channel.recipients)
            if member is not None:
                timestamp = datetime.datetime.utcfromtimestamp(data.get('timestamp'))
                self.dispatch('typing', channel, member, timestamp)

    def parse_relationship_add(self, data):
        key = int(data['id'])
        old = self.user.get_relationship(key)
        new = Relationship(state=self, data=data)
        self.user._relationships[key] = new
        if old is not None:
            self.dispatch('relationship_update', old, new)
        else:
            self.dispatch('relationship_add', new)

    def parse_relationship_remove(self, data):
        key = int(data['id'])
        try:
            old = self.user._relationships.pop(key)
        except KeyError:
            pass
        else:
            self.dispatch('relationship_remove', old)

    def _get_reaction_user(self, channel, user_id):
        if isinstance(channel, TextChannel):
            return channel.guild.get_member(user_id)
        return self.get_user(user_id)

    def get_reaction_emoji(self, data):
        emoji_id = utils._get_as_snowflake(data, 'id')
        if not emoji_id:
            return data['name']
        try:
            return self._emojis[emoji_id]
        except KeyError:
            return PartialEmoji(animated=(data.get('animated', False)), id=emoji_id, name=(data['name']))

    def _upgrade_partial_emoji(self, emoji):
        emoji_id = emoji.id
        if not emoji_id:
            return emoji.name
        try:
            return self._emojis[emoji_id]
        except KeyError:
            return emoji

    def get_channel(self, id):
        if id is None:
            return
        pm = self._get_private_channel(id)
        if pm is not None:
            return pm
        for guild in self.guilds:
            channel = guild.get_channel(id)
            if channel is not None:
                return channel

    def create_message(self, *, channel, data):
        return Message(state=self, channel=channel, data=data)

    def receive_chunk(self, guild_id):
        future = self.loop.create_future()
        listener = Listener(ListenerType.chunk, future, lambda s: s.id == guild_id)
        self._listeners.append(listener)
        return future

    def receive_member_query(self, guild_id, query):

        def predicate(args, *, guild_id=guild_id, query=query.lower()):
            request_guild_id, names = args
            return request_guild_id == guild_id and all((n.startswith(query) for n in names))

        future = self.loop.create_future()
        listener = Listener(ListenerType.query_members, future, predicate)
        self._listeners.append(listener)
        return future


class AutoShardedConnectionState(ConnectionState):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._ready_task = None
        self.shard_ids = ()

    async def request_offline_members(self, guilds, *, shard_id):
        chunks = []
        for guild in guilds:
            chunks.extend(self.chunks_needed(guild))
        else:
            splits = [guilds[i:i + 75] for i in range(0, len(guilds), 75)]
            for split in splits:
                await self.chunker(split, shard_id=shard_id)
            else:
                if chunks:
                    try:
                        await utils.sane_wait_for(chunks, timeout=(len(chunks) * 30.0))
                    except asyncio.TimeoutError:
                        log.info('Somehow timed out waiting for chunks.')

    async def _delay_ready(self):
        launch = self._ready_state.launch
        while True:
            try:
                await asyncio.wait_for((launch.wait()), timeout=(2.0 * len(self.shard_ids)))
            except asyncio.TimeoutError:
                break
            else:
                launch.clear()

        guilds = sorted((self._ready_state.guilds), key=(lambda g: g[0].shard_id))
        for shard_id, sub_guilds_info in itertools.groupby(guilds, key=(lambda g: g[0].shard_id)):
            sub_guilds, sub_available = zip(*sub_guilds_info)
            if self._fetch_offline:
                await self.request_offline_members(sub_guilds, shard_id=shard_id)
            else:
                for guild, unavailable in zip(sub_guilds, sub_available):
                    if unavailable is False:
                        self.dispatch('guild_available', guild)
                    else:
                        self.dispatch('guild_join', guild)
                else:
                    self.dispatch('shard_ready', shard_id)

        else:
            try:
                del self._ready_state
            except AttributeError:
                pass
            else:
                self._ready_task = None
                self.call_handlers('ready')
                self.dispatch('ready')

    def parse_ready(self, data):
        if not hasattr(self, '_ready_state'):
            self._ready_state = ReadyState(launch=(asyncio.Event()), guilds=[])
        self.user = user = ClientUser(state=self, data=(data['user']))
        self._users[user.id] = user
        guilds = self._ready_state.guilds
        for guild_data in data['guilds']:
            guild = self._add_guild_from_data(guild_data)
            if guild.large:
                guilds.append((guild, guild.unavailable))
        else:
            for pm in data.get('private_channels', []):
                factory, _ = _channel_factory(pm['type'])
                self._add_private_channel(factory(me=user, data=pm, state=self))
            else:
                self.dispatch('connect')
                if self._ready_task is None:
                    self._ready_task = asyncio.ensure_future((self._delay_ready()), loop=(self.loop))