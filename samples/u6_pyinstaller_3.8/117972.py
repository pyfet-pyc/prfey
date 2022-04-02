# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\iterators.py
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
import asyncio, datetime
from .errors import NoMoreItems
from .utils import DISCORD_EPOCH, time_snowflake, maybe_coroutine
from .object import Object
from .audit_logs import AuditLogEntry
OLDEST_OBJECT = Object(id=0)

class _AsyncIterator:
    __slots__ = ()

    def get(self, **attrs):

        def predicate(elem):
            for attr, val in attrs.items():
                nested = attr.split('__')
                obj = elem
                for attribute in nested:
                    obj = getattr(obj, attribute)

                if obj != val:
                    return False
                return True

        return self.find(predicate)

    async def find(self, predicate):
        while True:
            try:
                elem = await self.next()
            except NoMoreItems:
                return
            else:
                ret = await maybe_coroutine(predicate, elem)
                if ret:
                    return elem

    def map(self, func):
        return _MappedAsyncIterator(self, func)

    def filter(self, predicate):
        return _FilteredAsyncIterator(self, predicate)

    async def flatten(self):
        ret = []
        while True:
            try:
                item = await self.next()
            except NoMoreItems:
                return ret
            else:
                ret.append(item)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            msg = await self.next()
        except NoMoreItems:
            raise StopAsyncIteration()
        else:
            return msg


def _identity(x):
    return x


class _MappedAsyncIterator(_AsyncIterator):

    def __init__(self, iterator, func):
        self.iterator = iterator
        self.func = func

    async def next(self):
        item = await self.iterator.next()
        return await maybe_coroutine(self.func, item)


class _FilteredAsyncIterator(_AsyncIterator):

    def __init__(self, iterator, predicate):
        self.iterator = iterator
        if predicate is None:
            predicate = _identity
        self.predicate = predicate

    async def next(self):
        getter = self.iterator.next
        pred = self.predicate
        while True:
            item = await getter()
            ret = await maybe_coroutine(pred, item)
            if ret:
                return item


class ReactionIterator(_AsyncIterator):

    def __init__(self, message, emoji, limit=100, after=None):
        self.message = message
        self.limit = limit
        self.after = after
        state = message._state
        self.getter = state.http.get_reaction_users
        self.state = state
        self.emoji = emoji
        self.guild = message.guild
        self.channel_id = message.channel.id
        self.users = asyncio.Queue()

    async def next--- This code section failed: ---

 L. 138         0  LOAD_FAST                'self'
                2  LOAD_ATTR                users
                4  LOAD_METHOD              empty
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 139        10  LOAD_FAST                'self'
               12  LOAD_METHOD              fill_users
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 141        24  SETUP_FINALLY        38  'to 38'

 L. 142        26  LOAD_FAST                'self'
               28  LOAD_ATTR                users
               30  LOAD_METHOD              get_nowait
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 143        38  DUP_TOP          
               40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                QueueEmpty
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 144        54  LOAD_GLOBAL              NoMoreItems
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            46  '46'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 50

    async def fill_users(self):
        from .user import User
        if self.limit > 0:
            retrieve = self.limit if self.limit <= 100 else 100
            after = self.after.id if self.after else None
            data = await self.getter((self.channel_id), (self.message.id), (self.emoji), retrieve, after=after)
            if data:
                self.limit -= retrieve
                self.after = Object(id=(int(data[(-1)]['id'])))
            if self.guild is None:
                for element in reversed(data):
                    await self.users.put(User(state=(self.state), data=element))

            else:
                for element in reversed(data):
                    member_id = int(element['id'])
                    member = self.guild.get_member(member_id)
                    if member is not None:
                        await self.users.put(member)
                    else:
                        await self.users.put(User(state=(self.state), data=element))


class HistoryIterator(_AsyncIterator):
    __doc__ = "Iterator for receiving a channel's message history.\n\n    The messages endpoint has two behaviours we care about here:\n    If `before` is specified, the messages endpoint returns the `limit`\n    newest messages before `before`, sorted with newest first. For filling over\n    100 messages, update the `before` parameter to the oldest message received.\n    Messages will be returned in order by time.\n    If `after` is specified, it returns the `limit` oldest messages after\n    `after`, sorted with newest first. For filling over 100 messages, update the\n    `after` parameter to the newest message received. If messages are not\n    reversed, they will be out of order (99-0, 199-100, so on)\n\n    A note that if both before and after are specified, before is ignored by the\n    messages endpoint.\n\n    Parameters\n    -----------\n    messageable: :class:`abc.Messageable`\n        Messageable class to retrieve message history from.\n    limit: :class:`int`\n        Maximum number of messages to retrieve\n    before: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]\n        Message before which all messages must be.\n    after: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]\n        Message after which all messages must be.\n    around: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]\n        Message around which all messages must be. Limit max 101. Note that if\n        limit is an even number, this will return at most limit+1 messages.\n    oldest_first: Optional[:class:`bool`]\n        If set to ``True``, return messages in oldest->newest order. Defaults to\n        True if ``after`` is specified, otherwise ``False``.\n    "

    def __init__(self, messageable, limit, before=None, after=None, around=None, oldest_first=None):
        if isinstance(before, datetime.datetime):
            before = Object(id=time_snowflake(before, high=False))
        elif isinstance(after, datetime.datetime):
            after = Object(id=time_snowflake(after, high=True))
        elif isinstance(around, datetime.datetime):
            around = Object(id=(time_snowflake(around)))
        else:
            if oldest_first is None:
                self.reverse = after is not None
            else:
                self.reverse = oldest_first
            self.messageable = messageable
            self.limit = limit
            self.before = before
            self.after = after or OLDEST_OBJECT
            self.around = around
            self._filter = None
            self.state = self.messageable._state
            self.logs_from = self.state.http.logs_from
            self.messages = asyncio.Queue()
            if self.around:
                if self.limit is None:
                    raise ValueError('history does not support around with limit=None')
                if self.limit > 101:
                    raise ValueError('history max limit 101 when specifying around parameter')
                else:
                    if self.limit == 101:
                        self.limit = 100
                    else:
                        if self.limit == 1:
                            raise ValueError('Use fetch_message.')
                        self._retrieve_messages = self._retrieve_messages_around_strategy
                        if self.before and self.after:
                            self._filter = lambda m: self.after.id < int(m['id']) < self.before.id
                        else:
                            if self.before:
                                self._filter = lambda m: int(m['id']) < self.before.id
                            else:
                                if self.after:
                                    self._filter = lambda m: self.after.id < int(m['id'])
            else:
                if self.reverse:
                    self._retrieve_messages = self._retrieve_messages_after_strategy
                    if self.before:
                        self._filter = lambda m: int(m['id']) < self.before.id
                else:
                    self._retrieve_messages = self._retrieve_messages_before_strategy
            if self.after:
                if self.after != OLDEST_OBJECT:
                    self._filter = lambda m: int(m['id']) > self.after.id

    async def next--- This code section failed: ---

 L. 261         0  LOAD_FAST                'self'
                2  LOAD_ATTR                messages
                4  LOAD_METHOD              empty
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 262        10  LOAD_FAST                'self'
               12  LOAD_METHOD              fill_messages
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 264        24  SETUP_FINALLY        38  'to 38'

 L. 265        26  LOAD_FAST                'self'
               28  LOAD_ATTR                messages
               30  LOAD_METHOD              get_nowait
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 266        38  DUP_TOP          
               40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                QueueEmpty
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 267        54  LOAD_GLOBAL              NoMoreItems
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            46  '46'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 50

    def _get_retrieve(self):
        l = self.limit
        if l is None:
            r = 100
        else:
            if l <= 100:
                r = l
            else:
                r = 100
        self.retrieve = r
        return r > 0

    async def flatten(self):
        result = []
        channel = await self.messageable._get_channel()
        self.channel = channel
        while self._get_retrieve():
            data = await self._retrieve_messages(self.retrieve)
            if len(data) < 100:
                self.limit = 0
            if self.reverse:
                data = reversed(data)
            if self._filter:
                data = filter(self._filter, data)
            for element in data:
                result.append(self.state.create_message(channel=channel, data=element))

        return result

    async def fill_messages(self):
        if not hasattr(self, 'channel'):
            channel = await self.messageable._get_channel()
            self.channel = channel
        if self._get_retrieve():
            data = await self._retrieve_messages(self.retrieve)
            if len(data) < 100:
                self.limit = 0
            if self.reverse:
                data = reversed(data)
            if self._filter:
                data = filter(self._filter, data)
            channel = self.channel
            for element in data:
                await self.messages.put(self.state.create_message(channel=channel, data=element))

    async def _retrieve_messages(self, retrieve):
        """Retrieve messages and update next parameters."""
        pass

    async def _retrieve_messages_before_strategy(self, retrieve):
        """Retrieve messages using before parameter."""
        before = self.before.id if self.before else None
        data = await self.logs_from((self.channel.id), retrieve, before=before)
        if len(data):
            if self.limit is not None:
                self.limit -= retrieve
            self.before = Object(id=(int(data[(-1)]['id'])))
        return data

    async def _retrieve_messages_after_strategy(self, retrieve):
        """Retrieve messages using after parameter."""
        after = self.after.id if self.after else None
        data = await self.logs_from((self.channel.id), retrieve, after=after)
        if len(data):
            if self.limit is not None:
                self.limit -= retrieve
            self.after = Object(id=(int(data[0]['id'])))
        return data

    async def _retrieve_messages_around_strategy(self, retrieve):
        """Retrieve messages using around parameter."""
        if self.around:
            around = self.around.id if self.around else None
            data = await self.logs_from((self.channel.id), retrieve, around=around)
            self.around = None
            return data
        return []


class AuditLogIterator(_AsyncIterator):

    def __init__(self, guild, limit=None, before=None, after=None, oldest_first=None, user_id=None, action_type=None):
        if isinstance(before, datetime.datetime):
            before = Object(id=time_snowflake(before, high=False))
        elif isinstance(after, datetime.datetime):
            after = Object(id=time_snowflake(after, high=True))
        else:
            if oldest_first is None:
                self.reverse = after is not None
            else:
                self.reverse = oldest_first
            self.guild = guild
            self.loop = guild._state.loop
            self.request = guild._state.http.get_audit_logs
            self.limit = limit
            self.before = before
            self.user_id = user_id
            self.action_type = action_type
            self.after = OLDEST_OBJECT
            self._users = {}
            self._state = guild._state
            self._filter = None
            self.entries = asyncio.Queue()
            if self.reverse:
                self._strategy = self._after_strategy
                if self.before:
                    self._filter = lambda m: int(m['id']) < self.before.id
            else:
                self._strategy = self._before_strategy
            if self.after:
                if self.after != OLDEST_OBJECT:
                    self._filter = lambda m: int(m['id']) > self.after.id

    async def _before_strategy(self, retrieve):
        before = self.before.id if self.before else None
        data = await self.request((self.guild.id), limit=retrieve, user_id=(self.user_id), action_type=(self.action_type),
          before=before)
        entries = data.get('audit_log_entries', [])
        if len(data):
            if entries:
                if self.limit is not None:
                    self.limit -= retrieve
                self.before = Object(id=(int(entries[(-1)]['id'])))
        return (
         data.get('users', []), entries)

    async def _after_strategy(self, retrieve):
        after = self.after.id if self.after else None
        data = await self.request((self.guild.id), limit=retrieve, user_id=(self.user_id), action_type=(self.action_type),
          after=after)
        entries = data.get('audit_log_entries', [])
        if len(data):
            if entries:
                if self.limit is not None:
                    self.limit -= retrieve
                self.after = Object(id=(int(entries[0]['id'])))
        return (
         data.get('users', []), entries)

    async def next--- This code section failed: ---

 L. 417         0  LOAD_FAST                'self'
                2  LOAD_ATTR                entries
                4  LOAD_METHOD              empty
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 418        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _fill
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 420        24  SETUP_FINALLY        38  'to 38'

 L. 421        26  LOAD_FAST                'self'
               28  LOAD_ATTR                entries
               30  LOAD_METHOD              get_nowait
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 422        38  DUP_TOP          
               40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                QueueEmpty
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 423        54  LOAD_GLOBAL              NoMoreItems
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            46  '46'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 50

    def _get_retrieve(self):
        l = self.limit
        if l is None:
            r = 100
        else:
            if l <= 100:
                r = l
            else:
                r = 100
        self.retrieve = r
        return r > 0

    async def _fill(self):
        from .user import User
        if self._get_retrieve():
            users, data = await self._strategy(self.retrieve)
            if len(data) < 100:
                self.limit = 0
            if self.reverse:
                data = reversed(data)
            if self._filter:
                data = filter(self._filter, data)
            for user in users:
                u = User(data=user, state=(self._state))
                self._users[u.id] = u
            else:
                for element in data:
                    if element['action_type'] is None:
                        pass
                    else:
                        await self.entries.put(AuditLogEntry(data=element, users=(self._users), guild=(self.guild)))


class GuildIterator(_AsyncIterator):
    __doc__ = "Iterator for receiving the client's guilds.\n\n    The guilds endpoint has the same two behaviours as described\n    in :class:`HistoryIterator`:\n    If `before` is specified, the guilds endpoint returns the `limit`\n    newest guilds before `before`, sorted with newest first. For filling over\n    100 guilds, update the `before` parameter to the oldest guild received.\n    Guilds will be returned in order by time.\n    If `after` is specified, it returns the `limit` oldest guilds after `after`,\n    sorted with newest first. For filling over 100 guilds, update the `after`\n    parameter to the newest guild received, If guilds are not reversed, they\n    will be out of order (99-0, 199-100, so on)\n\n    Not that if both before and after are specified, before is ignored by the\n    guilds endpoint.\n\n    Parameters\n    -----------\n    bot: :class:`discord.Client`\n        The client to retrieve the guilds from.\n    limit: :class:`int`\n        Maximum number of guilds to retrieve.\n    before: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]\n        Object before which all guilds must be.\n    after: Optional[Union[:class:`abc.Snowflake`, :class:`datetime.datetime`]]\n        Object after which all guilds must be.\n    "

    def __init__(self, bot, limit, before=None, after=None):
        if isinstance(before, datetime.datetime):
            before = Object(id=time_snowflake(before, high=False))
        else:
            if isinstance(after, datetime.datetime):
                after = Object(id=time_snowflake(after, high=True))
            self.bot = bot
            self.limit = limit
            self.before = before
            self.after = after
            self._filter = None
            self.state = self.bot._connection
            self.get_guilds = self.bot.http.get_guilds
            self.guilds = asyncio.Queue()
            if self.before and self.after:
                self._retrieve_guilds = self._retrieve_guilds_before_strategy
                self._filter = lambda m: int(m['id']) > self.after.id
            else:
                if self.after:
                    self._retrieve_guilds = self._retrieve_guilds_after_strategy
                else:
                    self._retrieve_guilds = self._retrieve_guilds_before_strategy

    async def next--- This code section failed: ---

 L. 517         0  LOAD_FAST                'self'
                2  LOAD_ATTR                guilds
                4  LOAD_METHOD              empty
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 518        10  LOAD_FAST                'self'
               12  LOAD_METHOD              fill_guilds
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 520        24  SETUP_FINALLY        38  'to 38'

 L. 521        26  LOAD_FAST                'self'
               28  LOAD_ATTR                guilds
               30  LOAD_METHOD              get_nowait
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 522        38  DUP_TOP          
               40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                QueueEmpty
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 523        54  LOAD_GLOBAL              NoMoreItems
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            46  '46'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 50

    def _get_retrieve(self):
        l = self.limit
        if l is None:
            r = 100
        else:
            if l <= 100:
                r = l
            else:
                r = 100
        self.retrieve = r
        return r > 0

    def create_guild(self, data):
        from .guild import Guild
        return Guild(state=(self.state), data=data)

    async def flatten(self):
        result = []
        while self._get_retrieve():
            data = await self._retrieve_guilds(self.retrieve)
            if len(data) < 100:
                self.limit = 0
            if self._filter:
                data = filter(self._filter, data)
            for element in data:
                result.append(self.create_guild(element))

        return result

    async def fill_guilds(self):
        if self._get_retrieve():
            data = await self._retrieve_guilds(self.retrieve)
            if self.limit is None or len(data) < 100:
                self.limit = 0
            if self._filter:
                data = filter(self._filter, data)
            for element in data:
                await self.guilds.put(self.create_guild(element))

    async def _retrieve_guilds(self, retrieve):
        """Retrieve guilds and update next parameters."""
        pass

    async def _retrieve_guilds_before_strategy(self, retrieve):
        """Retrieve guilds using before parameter."""
        before = self.before.id if self.before else None
        data = await self.get_guilds(retrieve, before=before)
        if len(data):
            if self.limit is not None:
                self.limit -= retrieve
            self.before = Object(id=(int(data[(-1)]['id'])))
        return data

    async def _retrieve_guilds_after_strategy(self, retrieve):
        """Retrieve guilds using after parameter."""
        after = self.after.id if self.after else None
        data = await self.get_guilds(retrieve, after=after)
        if len(data):
            if self.limit is not None:
                self.limit -= retrieve
            self.after = Object(id=(int(data[0]['id'])))
        return data


class MemberIterator(_AsyncIterator):

    def __init__(self, guild, limit=1000, after=None):
        if isinstance(after, datetime.datetime):
            after = Object(id=time_snowflake(after, high=True))
        self.guild = guild
        self.limit = limit
        self.after = after or OLDEST_OBJECT
        self.state = self.guild._state
        self.get_members = self.state.http.get_members
        self.members = asyncio.Queue()

    async def next--- This code section failed: ---

 L. 606         0  LOAD_FAST                'self'
                2  LOAD_ATTR                members
                4  LOAD_METHOD              empty
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 607        10  LOAD_FAST                'self'
               12  LOAD_METHOD              fill_members
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

 L. 609        24  SETUP_FINALLY        38  'to 38'

 L. 610        26  LOAD_FAST                'self'
               28  LOAD_ATTR                members
               30  LOAD_METHOD              get_nowait
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    24  '24'

 L. 611        38  DUP_TOP          
               40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                QueueEmpty
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 612        54  LOAD_GLOBAL              NoMoreItems
               56  CALL_FUNCTION_0       0  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            46  '46'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 50

    def _get_retrieve(self):
        l = self.limit
        if l is None:
            r = 1000
        else:
            if l <= 1000:
                r = l
            else:
                r = 1000
        self.retrieve = r
        return r > 0

    async def fill_members(self):
        if self._get_retrieve():
            after = self.after.id if self.after else None
            data = await self.get_members(self.guild.id, self.retrieve, after)
            if not data:
                return
            if len(data) < 1000:
                self.limit = 0
            self.after = Object(id=(int(data[(-1)]['user']['id'])))
            for element in reversed(data):
                await self.members.put(self.create_member(element))

    def create_member(self, data):
        from .member import Member
        return Member(data=data, guild=(self.guild), state=(self.state))