# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\client.py
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
from collections import namedtuple
import logging, signal, sys, traceback, aiohttp, websockets
from .user import User, Profile
from .asset import Asset
from .invite import Invite
from .widget import Widget
from .guild import Guild
from .channel import _channel_factory
from .enums import ChannelType
from .member import Member
from .errors import *
from .enums import Status, VoiceRegion
from .gateway import *
from .activity import BaseActivity, create_activity
from .voice_client import VoiceClient
from .http import HTTPClient
from .state import ConnectionState
from . import utils
from .object import Object
from .backoff import ExponentialBackoff
from .webhook import Webhook
from .iterators import GuildIterator
from .appinfo import AppInfo
log = logging.getLogger(__name__)

def _cancel_tasks(loop):
    try:
        task_retriever = asyncio.Task.all_tasks
    except AttributeError:
        task_retriever = asyncio.all_tasks
    else:
        tasks = {t for t in task_retriever(loop=loop) if not t.done() if not t.done()}
        if not tasks:
            return
        log.info('Cleaning up after %d tasks.', len(tasks))
        for task in tasks:
            task.cancel()
        else:
            loop.run_until_complete((asyncio.gather)(*tasks, **{'return_exceptions': True}))
            log.info('All tasks finished cancelling.')
            for task in tasks:
                if task.cancelled():
                    pass
                elif task.exception() is not None:
                    loop.call_exception_handler({'message':'Unhandled exception during Client.run shutdown.', 
                     'exception':task.exception(), 
                     'task':task})


def _cleanup_loop(loop):
    try:
        _cancel_tasks(loop)
        if sys.version_info >= (3, 6):
            loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        log.info('Closing the event loop.')
        loop.close()


class _ClientEventTask(asyncio.Task):

    def __init__(self, original_coro, event_name, coro, *, loop):
        super().__init__(coro, loop=loop)
        self._ClientEventTask__event_name = event_name
        self._ClientEventTask__original_coro = original_coro

    def __repr__(self):
        info = [
         (
          'state', self._state.lower()),
         (
          'event', self._ClientEventTask__event_name),
         (
          'coro', repr(self._ClientEventTask__original_coro))]
        if self._exception is not None:
            info.append(('exception', repr(self._exception)))
        return '<ClientEventTask {}>'.format(' '.join(('%s=%s' % t for t in info)))


class Client:
    __doc__ = "Represents a client connection that connects to Discord.\n    This class is used to interact with the Discord WebSocket and API.\n\n    A number of options can be passed to the :class:`Client`.\n\n    Parameters\n    -----------\n    max_messages: Optional[:class:`int`]\n        The maximum number of messages to store in the internal message cache.\n        This defaults to 1000. Passing in ``None`` disables the message cache.\n\n        .. versionchanged:: 1.3\n            Allow disabling the message cache and change the default size to 1000.\n    loop: Optional[:class:`asyncio.AbstractEventLoop`]\n        The :class:`asyncio.AbstractEventLoop` to use for asynchronous operations.\n        Defaults to ``None``, in which case the default event loop is used via\n        :func:`asyncio.get_event_loop()`.\n    connector: :class:`aiohttp.BaseConnector`\n        The connector to use for connection pooling.\n    proxy: Optional[:class:`str`]\n        Proxy URL.\n    proxy_auth: Optional[:class:`aiohttp.BasicAuth`]\n        An object that represents proxy HTTP Basic Authorization.\n    shard_id: Optional[:class:`int`]\n        Integer starting at 0 and less than :attr:`.shard_count`.\n    shard_count: Optional[:class:`int`]\n        The total number of shards.\n    fetch_offline_members: :class:`bool`\n        Indicates if :func:`.on_ready` should be delayed to fetch all offline\n        members from the guilds the bot belongs to. If this is ``False``\\, then\n        no offline members are received and :meth:`request_offline_members`\n        must be used to fetch the offline members of the guild.\n    status: Optional[:class:`.Status`]\n        A status to start your presence with upon logging on to Discord.\n    activity: Optional[:class:`.BaseActivity`]\n        An activity to start your presence with upon logging on to Discord.\n    heartbeat_timeout: :class:`float`\n        The maximum numbers of seconds before timing out and restarting the\n        WebSocket in the case of not receiving a HEARTBEAT_ACK. Useful if\n        processing the initial packets take too long to the point of disconnecting\n        you. The default timeout is 60 seconds.\n    guild_subscriptions: :class:`bool`\n        Whether to dispatching of presence or typing events. Defaults to ``True``.\n\n        .. versionadded:: 1.3\n\n        .. warning::\n\n            If this is set to ``False`` then the following features will be disabled:\n\n                - No user related updates (:func:`on_user_update` will not dispatch)\n                - All member related events will be disabled.\n                    - :func:`on_member_update`\n                    - :func:`on_member_join`\n                    - :func:`on_member_remove`\n\n                - Typing events will be disabled (:func:`on_typing`).\n                - If ``fetch_offline_members`` is set to ``False`` then the user cache will not exist.\n                  This makes it difficult or impossible to do many things, for example:\n\n                    - Computing permissions\n                    - Querying members in a voice channel via :attr:`VoiceChannel.members` will be empty.\n                    - Most forms of receiving :class:`Member` will be\n                      receiving :class:`User` instead, except for message events.\n                    - :attr:`Guild.owner` will usually resolve to ``None``.\n                    - :meth:`Guild.get_member` will usually be unavailable.\n                    - Anything that involves using :class:`Member`.\n                    - :attr:`users` will not be as populated.\n                    - etc.\n\n            In short, this makes it so the only member you can reliably query is the\n            message author. Useful for bots that do not require any state.\n    assume_unsync_clock: :class:`bool`\n        Whether to assume the system clock is unsynced. This applies to the ratelimit handling\n        code. If this is set to ``True``, the default, then the library uses the time to reset\n        a rate limit bucket given by Discord. If this is ``False`` then your system clock is\n        used to calculate how long to sleep for. If this is set to ``False`` it is recommended to\n        sync your system clock to Google's NTP server.\n\n        .. versionadded:: 1.3\n\n    Attributes\n    -----------\n    ws\n        The websocket gateway the client is currently connected to. Could be ``None``.\n    loop: :class:`asyncio.AbstractEventLoop`\n        The event loop that the client uses for HTTP requests and websocket operations.\n    "

    def __init__(self, *, loop=None, **options):
        self.ws = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._listeners = {}
        self.shard_id = options.get('shard_id')
        self.shard_count = options.get('shard_count')
        connector = options.pop('connector', None)
        proxy = options.pop('proxy', None)
        proxy_auth = options.pop('proxy_auth', None)
        unsync_clock = options.pop('assume_unsync_clock', True)
        self.http = HTTPClient(connector, proxy=proxy, proxy_auth=proxy_auth, unsync_clock=unsync_clock, loop=(self.loop))
        self._handlers = {'ready': self._handle_ready}
        self._connection = ConnectionState(dispatch=self.dispatch, chunker=self._chunker, handlers=self._handlers, syncer=self._syncer, 
         http=self.http, loop=self.loop, **options)
        self._connection.shard_count = self.shard_count
        self._closed = False
        self._ready = asyncio.Event()
        self._connection._get_websocket = lambda g: self.ws
        if VoiceClient.warn_nacl:
            VoiceClient.warn_nacl = False
            log.warning('PyNaCl is not installed, voice will NOT be supported')

    async def _syncer(self, guilds):
        await self.ws.request_sync(guilds)

    async def _chunker(self, guild):
        try:
            guild_id = guild.id
        except AttributeError:
            guild_id = [s.id for s in guild]
        else:
            payload = {'op':8, 
             'd':{'guild_id':guild_id, 
              'query':'', 
              'limit':0}}
            await self.ws.send_as_json(payload)

    def _handle_ready(self):
        self._ready.set()

    @property
    def latency(self):
        """:class:`float`: Measures latency between a HEARTBEAT and a HEARTBEAT_ACK in seconds.

        This could be referred to as the Discord WebSocket protocol latency.
        """
        ws = self.ws
        if not ws:
            return float('nan')
        return ws.latency

    @property
    def user(self):
        """Optional[:class:`.ClientUser`]: Represents the connected client. None if not logged in."""
        return self._connection.user

    @property
    def guilds(self):
        """List[:class:`.Guild`]: The guilds that the connected client is a member of."""
        return self._connection.guilds

    @property
    def emojis(self):
        """List[:class:`.Emoji`]: The emojis that the connected client has."""
        return self._connection.emojis

    @property
    def cached_messages(self):
        """Sequence[:class:`.Message`]: Read-only list of messages the connected client has cached.

        .. versionadded:: 1.1
        """
        return utils.SequenceProxy(self._connection._messages or [])

    @property
    def private_channels(self):
        """List[:class:`.abc.PrivateChannel`]: The private channels that the connected client is participating on.

        .. note::

            This returns only up to 128 most recent private channels due to an internal working
            on how Discord deals with private channels.
        """
        return self._connection.private_channels

    @property
    def voice_clients(self):
        """List[:class:`.VoiceClient`]: Represents a list of voice connections."""
        return self._connection.voice_clients

    def is_ready(self):
        """Specifies if the client's internal cache is ready for use."""
        return self._ready.is_set()

    async def _run_event(self, coro, event_name, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await (self.on_error)(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass

    def _schedule_event(self, coro, event_name, *args, **kwargs):
        wrapped = (self._run_event)(coro, event_name, *args, **kwargs)
        return _ClientEventTask(original_coro=coro, event_name=event_name, coro=wrapped, loop=(self.loop))

    def dispatch(self, event, *args, **kwargs):
        log.debug('Dispatching event %s', event)
        method = 'on_' + event
        listeners = self._listeners.get(event)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
            else:
                try:
                    result = condition(*args)
                except Exception as exc:
                    try:
                        future.set_exception(exc)
                        removed.append(i)
                    finally:
                        exc = None
                        del exc

                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        else:
                            if len(args) == 1:
                                future.set_result(args[0])
                            else:
                                future.set_result(args)
                        removed.append(i)
                    if len(removed) == len(listeners):
                        self._listeners.pop(event)
                    else:
                        for idx in reversed(removed):
                            del listeners[idx]

        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            (self._schedule_event)(coro, method, *args, **kwargs)

    async def on_error(self, event_method, *args, **kwargs):
        """|coro|

        The default error handler provided by the client.

        By default this prints to :data:`sys.stderr` however it could be
        overridden to have a different implementation.
        Check :func:`~discord.on_error` for more details.
        """
        print(('Ignoring exception in {}'.format(event_method)), file=(sys.stderr))
        traceback.print_exc()

    async def request_offline_members(self, *guilds):
        r"""|coro|

        Requests previously offline members from the guild to be filled up
        into the :attr:`.Guild.members` cache. This function is usually not
        called. It should only be used if you have the ``fetch_offline_members``
        parameter set to ``False``.

        When the client logs on and connects to the websocket, Discord does
        not provide the library with offline members if the number of members
        in the guild is larger than 250. You can check if a guild is large
        if :attr:`.Guild.large` is ``True``.

        Parameters
        -----------
        \*guilds: :class:`.Guild`
            An argument list of guilds to request offline members for.

        Raises
        -------
        :exc:`.InvalidArgument`
            If any guild is unavailable or not large in the collection.
        """
        if any((not g.large or g.unavailable for g in guilds)):
            raise InvalidArgument('An unavailable or non-large guild was passed.')
        await self._connection.request_offline_members(guilds)

    async def login(self, token, *, bot=True):
        """|coro|

        Logs in the client with the specified credentials.

        This function can be used in two different ways.

        .. warning::

            Logging on with a user token is against the Discord
            `Terms of Service <https://support.discordapp.com/hc/en-us/articles/115002192352>`_
            and doing so might potentially get your account banned.
            Use this at your own risk.

        Parameters
        -----------
        token: :class:`str`
            The authentication token. Do not prefix this token with
            anything as the library will do it for you.
        bot: :class:`bool`
            Keyword argument that specifies if the account logging on is a bot
            token or not.

        Raises
        ------
        :exc:`.LoginFailure`
            The wrong credentials are passed.
        :exc:`.HTTPException`
            An unknown HTTP related error occurred,
            usually when it isn't 200 or the known incorrect credentials
            passing status code.
        """
        log.info('logging in using static token')
        await self.http.static_login((token.strip()), bot=bot)
        self._connection.is_bot = bot

    async def logout(self):
        """|coro|

        Logs out of Discord and closes all connections.

        .. note::

            This is just an alias to :meth:`close`. If you want
            to do extraneous cleanup when subclassing, it is suggested
            to override :meth:`close` instead.
        """
        await self.close()

    async def _connect(self):
        coro = DiscordWebSocket.from_client(self, shard_id=(self.shard_id))
        self.ws = await asyncio.wait_for(coro, timeout=180.0)
        while True:
            try:
                await self.ws.poll_event()
            except ResumeWebSocket:
                log.info('Got a request to RESUME the websocket.')
                self.dispatch('disconnect')
                coro = DiscordWebSocket.from_client(self, shard_id=(self.shard_id), session=(self.ws.session_id), sequence=(self.ws.sequence),
                  resume=True)
                self.ws = await asyncio.wait_for(coro, timeout=180.0)

    async def connect--- This code section failed: ---

 L. 496         0  LOAD_GLOBAL              ExponentialBackoff
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'backoff'

 L. 497         6  LOAD_FAST                'self'
                8  LOAD_METHOD              is_closed
               10  CALL_METHOD_0         0  ''
               12  POP_JUMP_IF_TRUE    244  'to 244'

 L. 498        14  SETUP_FINALLY        34  'to 34'

 L. 499        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _connect
               20  CALL_METHOD_0         0  ''
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  POP_TOP          
               30  POP_BLOCK        
               32  JUMP_BACK             6  'to 6'
             34_0  COME_FROM_FINALLY    14  '14'

 L. 500        34  DUP_TOP          
               36  LOAD_GLOBAL              OSError

 L. 501        38  LOAD_GLOBAL              HTTPException

 L. 502        40  LOAD_GLOBAL              GatewayNotFound

 L. 503        42  LOAD_GLOBAL              ConnectionClosed

 L. 504        44  LOAD_GLOBAL              aiohttp
               46  LOAD_ATTR                ClientError

 L. 505        48  LOAD_GLOBAL              asyncio
               50  LOAD_ATTR                TimeoutError

 L. 506        52  LOAD_GLOBAL              websockets
               54  LOAD_ATTR                InvalidHandshake

 L. 507        56  LOAD_GLOBAL              websockets
               58  LOAD_ATTR                WebSocketProtocolError

 L. 500        60  BUILD_TUPLE_8         8 
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   240  'to 240'
               66  POP_TOP          
               68  STORE_FAST               'exc'
               70  POP_TOP          
               72  SETUP_FINALLY       228  'to 228'

 L. 509        74  LOAD_FAST                'self'
               76  LOAD_METHOD              dispatch
               78  LOAD_STR                 'disconnect'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 510        84  LOAD_FAST                'reconnect'
               86  POP_JUMP_IF_TRUE    134  'to 134'

 L. 511        88  LOAD_FAST                'self'
               90  LOAD_METHOD              close
               92  CALL_METHOD_0         0  ''
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  POP_TOP          

 L. 512       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'exc'
              106  LOAD_GLOBAL              ConnectionClosed
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   132  'to 132'
              112  LOAD_FAST                'exc'
              114  LOAD_ATTR                code
              116  LOAD_CONST               1000
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 514       122  POP_BLOCK        
              124  POP_EXCEPT       
              126  CALL_FINALLY        228  'to 228'
              128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM           120  '120'
            132_1  COME_FROM           110  '110'

 L. 515       132  RAISE_VARARGS_0       0  'reraise'
            134_0  COME_FROM            86  '86'

 L. 517       134  LOAD_FAST                'self'
              136  LOAD_METHOD              is_closed
              138  CALL_METHOD_0         0  ''
              140  POP_JUMP_IF_FALSE   152  'to 152'

 L. 518       142  POP_BLOCK        
              144  POP_EXCEPT       
              146  CALL_FINALLY        228  'to 228'
              148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM           140  '140'

 L. 524       152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'exc'
              156  LOAD_GLOBAL              ConnectionClosed
              158  CALL_FUNCTION_2       2  ''
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L. 525       162  LOAD_FAST                'exc'
              164  LOAD_ATTR                code
              166  LOAD_CONST               1000
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   188  'to 188'

 L. 526       172  LOAD_FAST                'self'
              174  LOAD_METHOD              close
              176  CALL_METHOD_0         0  ''
              178  GET_AWAITABLE    
              180  LOAD_CONST               None
              182  YIELD_FROM       
              184  POP_TOP          

 L. 527       186  RAISE_VARARGS_0       0  'reraise'
            188_0  COME_FROM           170  '170'
            188_1  COME_FROM           160  '160'

 L. 529       188  LOAD_FAST                'backoff'
              190  LOAD_METHOD              delay
              192  CALL_METHOD_0         0  ''
              194  STORE_FAST               'retry'

 L. 530       196  LOAD_GLOBAL              log
              198  LOAD_METHOD              exception
              200  LOAD_STR                 'Attempting a reconnect in %.2fs'
              202  LOAD_FAST                'retry'
              204  CALL_METHOD_2         2  ''
              206  POP_TOP          

 L. 531       208  LOAD_GLOBAL              asyncio
              210  LOAD_METHOD              sleep
              212  LOAD_FAST                'retry'
              214  CALL_METHOD_1         1  ''
              216  GET_AWAITABLE    
              218  LOAD_CONST               None
              220  YIELD_FROM       
              222  POP_TOP          
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM           146  '146'
            228_1  COME_FROM           126  '126'
            228_2  COME_FROM_FINALLY    72  '72'
              228  LOAD_CONST               None
              230  STORE_FAST               'exc'
              232  DELETE_FAST              'exc'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_BACK             6  'to 6'
            240_0  COME_FROM            64  '64'
              240  END_FINALLY      
              242  JUMP_BACK             6  'to 6'
            244_0  COME_FROM            12  '12'

Parse error at or near `POP_EXCEPT' instruction at offset 124

    async def close(self):
        """|coro|

        Closes the connection to Discord.
        """
        if self._closed:
            return
        await self.http.close()
        self._closed = True
        for voice in self.voice_clients:
            try:
                await voice.disconnect()
            except Exception:
                pass

        else:
            if self.ws is not None:
                if self.ws.open:
                    await self.ws.close(code=1000)
            self._ready.clear()

    def clear(self):
        """Clears the internal state of the bot.

        After this, the bot can be considered "re-opened", i.e. :meth:`is_closed`
        and :meth:`is_ready` both return ``False`` along with the bot's internal
        cache cleared.
        """
        self._closed = False
        self._ready.clear()
        self._connection.clear()
        self.http.recreate()

    async def start(self, *args, **kwargs):
        """|coro|

        A shorthand coroutine for :meth:`login` + :meth:`connect`.

        Raises
        -------
        TypeError
            An unexpected keyword argument was received.
        """
        bot = kwargs.pop('bot', True)
        reconnect = kwargs.pop('reconnect', True)
        if kwargs:
            raise TypeError('unexpected keyword argument(s) %s' % list(kwargs.keys()))
        await (self.login)(*args, **{'bot': bot})
        await self.connect(reconnect=reconnect)

    def run(self, *args, **kwargs):
        """A blocking call that abstracts away the event loop
        initialisation from you.

        If you want more control over the event loop then this
        function should not be used. Use :meth:`start` coroutine
        or :meth:`connect` + :meth:`login`.

        Roughly Equivalent to: ::

            try:
                loop.run_until_complete(start(*args, **kwargs))
            except KeyboardInterrupt:
                loop.run_until_complete(logout())
                # cancel all tasks lingering
            finally:
                loop.close()

        .. warning::

            This function must be the last function to call due to the fact that it
            is blocking. That means that registration of events or anything being
            called after this function call will not execute until it returns.
        """
        loop = self.loop
        try:
            loop.add_signal_handler(signal.SIGINT, lambda : loop.stop())
            loop.add_signal_handler(signal.SIGTERM, lambda : loop.stop())
        except NotImplementedError:
            pass
        else:

            async def runner():
                try:
                    await (self.start)(*args, **kwargs)
                finally:
                    await self.close()

            def stop_loop_on_completion(f):
                loop.stop()

            future = asyncio.ensure_future((runner()), loop=loop)
            future.add_done_callback(stop_loop_on_completion)
            try:
                try:
                    loop.run_forever()
                except KeyboardInterrupt:
                    log.info('Received signal to terminate bot and event loop.')

            finally:
                future.remove_done_callback(stop_loop_on_completion)
                log.info('Cleaning up tasks.')
                _cleanup_loop(loop)

            if not future.cancelled():
                return future.result()

    def is_closed(self):
        """Indicates if the websocket connection is closed."""
        return self._closed

    @property
    def activity(self):
        """Optional[:class:`.BaseActivity`]: The activity being used upon
        logging in.
        """
        return create_activity(self._connection._activity)

    @activity.setter
    def activity(self, value):
        if value is None:
            self._connection._activity = None
        else:
            if isinstance(value, BaseActivity):
                self._connection._activity = value.to_dict()
            else:
                raise TypeError('activity must derive from BaseActivity.')

    @property
    def users(self):
        """List[:class:`~discord.User`]: Returns a list of all the users the bot can see."""
        return list(self._connection._users.values())

    def get_channel(self, id):
        """Returns a channel with the given ID.

        Parameters
        -----------
        id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[Union[:class:`.abc.GuildChannel`, :class:`.abc.PrivateChannel`]]
            The returned channel or ``None`` if not found.
        """
        return self._connection.get_channel(id)

    def get_guild(self, id):
        """Returns a guild with the given ID.

        Parameters
        -----------
        id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[:class:`.Guild`]
            The guild or ``None`` if not found.
        """
        return self._connection._get_guild(id)

    def get_user(self, id):
        """Returns a user with the given ID.

        Parameters
        -----------
        id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[:class:`~discord.User`]
            The user or ``None`` if not found.
        """
        return self._connection.get_user(id)

    def get_emoji(self, id):
        """Returns an emoji with the given ID.

        Parameters
        -----------
        id: :class:`int`
            The ID to search for.

        Returns
        --------
        Optional[:class:`.Emoji`]
            The custom emoji or ``None`` if not found.
        """
        return self._connection.get_emoji(id)

    def get_all_channels(self):
        """A generator that retrieves every :class:`.abc.GuildChannel` the client can 'access'.

        This is equivalent to: ::

            for guild in client.guilds:
                for channel in guild.channels:
                    yield channel

        .. note::

            Just because you receive a :class:`.abc.GuildChannel` does not mean that
            you can communicate in said channel. :meth:`.abc.GuildChannel.permissions_for` should
            be used for that.
        """
        for guild in self.guilds:
            for channel in guild.channels:
                (yield channel)

    def get_all_members(self):
        """Returns a generator with every :class:`.Member` the client can see.

        This is equivalent to: ::

            for guild in client.guilds:
                for member in guild.members:
                    yield member
        """
        for guild in self.guilds:
            for member in guild.members:
                (yield member)

    async def wait_until_ready(self):
        """|coro|

        Waits until the client's internal cache is all ready.
        """
        await self._ready.wait()

    def wait_for(self, event, *, check=None, timeout=None):
        """|coro|

        Waits for a WebSocket event to be dispatched.

        This could be used to wait for a user to reply to a message,
        or to react to a message, or to edit a message in a self-contained
        way.

        The ``timeout`` parameter is passed onto :func:`asyncio.wait_for`. By default,
        it does not timeout. Note that this does propagate the
        :exc:`asyncio.TimeoutError` for you in case of timeout and is provided for
        ease of use.

        In case the event returns multiple arguments, a :class:`tuple` containing those
        arguments is returned instead. Please check the
        :ref:`documentation <discord-api-events>` for a list of events and their
        parameters.

        This function returns the **first event that meets the requirements**.

        Examples
        ---------

        Waiting for a user reply: ::

            @client.event
            async def on_message(message):
                if message.content.startswith('$greet'):
                    channel = message.channel
                    await channel.send('Say hello!')

                    def check(m):
                        return m.content == 'hello' and m.channel == channel

                    msg = await client.wait_for('message', check=check)
                    await channel.send('Hello {.author}!'.format(msg))

        Waiting for a thumbs up reaction from the message author: ::

            @client.event
            async def on_message(message):
                if message.content.startswith('$thumb'):
                    channel = message.channel
                    await channel.send('Send me that 👍 reaction, mate')

                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) == '👍'

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await channel.send('👎')
                    else:
                        await channel.send('👍')

        Parameters
        ------------
        event: :class:`str`
            The event name, similar to the :ref:`event reference <discord-api-events>`,
            but without the ``on_`` prefix, to wait for.
        check: Optional[Callable[..., :class:`bool`]]
            A predicate to check what to wait for. The arguments must meet the
            parameters of the event being waited for.
        timeout: Optional[:class:`float`]
            The number of seconds to wait before timing out and raising
            :exc:`asyncio.TimeoutError`.

        Raises
        -------
        asyncio.TimeoutError
            If a timeout is provided and it was reached.

        Returns
        --------
        Any
            Returns no arguments, a single argument, or a :class:`tuple` of multiple
            arguments that mirrors the parameters passed in the
            :ref:`event reference <discord-api-events>`.
        """
        future = self.loop.create_future()
        if check is None:

            def _check(*args):
                return True

            check = _check
        ev = event.lower()
        try:
            listeners = self._listeners[ev]
        except KeyError:
            listeners = []
            self._listeners[ev] = listeners
        else:
            listeners.append((future, check))
            return asyncio.wait_for(future, timeout)

    def event(self, coro):
        """A decorator that registers an event to listen to.

        You can find more info about the events on the :ref:`documentation below <discord-api-events>`.

        The events must be a :ref:`coroutine <coroutine>`, if not, :exc:`TypeError` is raised.

        Example
        ---------

        .. code-block:: python3

            @client.event
            async def on_ready():
                print('Ready!')

        Raises
        --------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')
        setattr(self, coro.__name__, coro)
        log.debug('%s has successfully been registered as an event', coro.__name__)
        return coro

    async def change_presence(self, *, activity=None, status=None, afk=False):
        """|coro|

        Changes the client's presence.

        Example
        ---------

        .. code-block:: python3

            game = discord.Game("with the API")
            await client.change_presence(status=discord.Status.idle, activity=game)

        Parameters
        ----------
        activity: Optional[:class:`.BaseActivity`]
            The activity being done. ``None`` if no currently active activity is done.
        status: Optional[:class:`.Status`]
            Indicates what status to change to. If ``None``, then
            :attr:`.Status.online` is used.
        afk: Optional[:class:`bool`]
            Indicates if you are going AFK. This allows the discord
            client to know how to handle push notifications better
            for you in case you are actually idle and not lying.

        Raises
        ------
        :exc:`.InvalidArgument`
            If the ``activity`` parameter is not the proper type.
        """
        if status is None:
            status = 'online'
            status_enum = Status.online
        else:
            if status is Status.offline:
                status = 'invisible'
                status_enum = Status.offline
            else:
                status_enum = status
                status = str(status)
        await self.ws.change_presence(activity=activity, status=status, afk=afk)
        for guild in self._connection.guilds:
            me = guild.me
            if me is None:
                pass
            else:
                if activity is not None:
                    me.activities = (
                     activity,)
                me.status = status_enum

    def fetch_guilds(self, *, limit=100, before=None, after=None):
        """|coro|

        Retrieves an :class:`.AsyncIterator` that enables receiving your guilds.

        .. note::

            Using this, you will only receive :attr:`.Guild.owner`, :attr:`.Guild.icon`,
            :attr:`.Guild.id`, and :attr:`.Guild.name` per :class:`.Guild`.

        .. note::

            This method is an API call. For general usage, consider :attr:`guilds` instead.

        Examples
        ---------

        Usage ::

            async for guild in client.fetch_guilds(limit=150):
                print(guild.name)

        Flattening into a list ::

            guilds = await client.fetch_guilds(limit=150).flatten()
            # guilds is now a list of Guild...

        All parameters are optional.

        Parameters
        -----------
        limit: Optional[:class:`int`]
            The number of guilds to retrieve.
            If ``None``, it retrieves every guild you have access to. Note, however,
            that this would make it a slow operation.
            Defaults to 100.
        before: Union[:class:`.abc.Snowflake`, :class:`datetime.datetime`]
            Retrieves guilds before this date or object.
            If a date is provided it must be a timezone-naive datetime representing UTC time.
        after: Union[:class:`.abc.Snowflake`, :class:`datetime.datetime`]
            Retrieve guilds after this date or object.
            If a date is provided it must be a timezone-naive datetime representing UTC time.

        Raises
        ------
        :exc:`.HTTPException`
            Getting the guilds failed.

        Yields
        --------
        :class:`.Guild`
            The guild with the guild data parsed.
        """
        return GuildIterator(self, limit=limit, before=before, after=after)

    async def fetch_guild(self, guild_id):
        """|coro|

        Retrieves a :class:`.Guild` from an ID.

        .. note::

            Using this, you will **not** receive :attr:`.Guild.channels`, :attr:`.Guild.members`,
            :attr:`.Member.activity` and :attr:`.Member.voice` per :class:`.Member`.

        .. note::

            This method is an API call. For general usage, consider :meth:`get_guild` instead.

        Parameters
        -----------
        guild_id: :class:`int`
            The guild's ID to fetch from.

        Raises
        ------
        :exc:`.Forbidden`
            You do not have access to the guild.
        :exc:`.HTTPException`
            Getting the guild failed.

        Returns
        --------
        :class:`.Guild`
            The guild from the ID.
        """
        data = await self.http.get_guild(guild_id)
        return Guild(data=data, state=(self._connection))

    async def create_guild(self, name, region=None, icon=None):
        """|coro|

        Creates a :class:`.Guild`.

        Bot accounts in more than 10 guilds are not allowed to create guilds.

        Parameters
        ----------
        name: :class:`str`
            The name of the guild.
        region: :class:`.VoiceRegion`
            The region for the voice communication server.
            Defaults to :attr:`.VoiceRegion.us_west`.
        icon: :class:`bytes`
            The :term:`py:bytes-like object` representing the icon. See :meth:`.ClientUser.edit`
            for more details on what is expected.

        Raises
        ------
        :exc:`.HTTPException`
            Guild creation failed.
        :exc:`.InvalidArgument`
            Invalid icon image format given. Must be PNG or JPG.

        Returns
        -------
        :class:`.Guild`
            The guild created. This is not the same guild that is
            added to cache.
        """
        if icon is not None:
            icon = utils._bytes_to_base64_data(icon)
        elif region is None:
            region = VoiceRegion.us_west.value
        else:
            region = region.value
        data = await self.http.create_guild(name, region, icon)
        return Guild(data=data, state=(self._connection))

    async def fetch_invite(self, url, *, with_counts=True):
        """|coro|

        Gets an :class:`.Invite` from a discord.gg URL or ID.

        .. note::

            If the invite is for a guild you have not joined, the guild and channel
            attributes of the returned :class:`.Invite` will be :class:`.PartialInviteGuild` and
            :class:`PartialInviteChannel` respectively.

        Parameters
        -----------
        url: :class:`str`
            The Discord invite ID or URL (must be a discord.gg URL).
        with_counts: :class:`bool`
            Whether to include count information in the invite. This fills the
            :attr:`.Invite.approximate_member_count` and :attr:`.Invite.approximate_presence_count`
            fields.

        Raises
        -------
        :exc:`.NotFound`
            The invite has expired or is invalid.
        :exc:`.HTTPException`
            Getting the invite failed.

        Returns
        --------
        :class:`.Invite`
            The invite from the URL/ID.
        """
        invite_id = utils.resolve_invite(url)
        data = await self.http.get_invite(invite_id, with_counts=with_counts)
        return Invite.from_incomplete(state=(self._connection), data=data)

    async def delete_invite(self, invite):
        """|coro|

        Revokes an :class:`.Invite`, URL, or ID to an invite.

        You must have the :attr:`~.Permissions.manage_channels` permission in
        the associated guild to do this.

        Parameters
        ----------
        invite: Union[:class:`.Invite`, :class:`str`]
            The invite to revoke.

        Raises
        -------
        :exc:`.Forbidden`
            You do not have permissions to revoke invites.
        :exc:`.NotFound`
            The invite is invalid or expired.
        :exc:`.HTTPException`
            Revoking the invite failed.
        """
        invite_id = utils.resolve_invite(invite)
        await self.http.delete_invite(invite_id)

    async def fetch_widget(self, guild_id):
        """|coro|

        Gets a :class:`.Widget` from a guild ID.

        .. note::

            The guild must have the widget enabled to get this information.

        Parameters
        -----------
        guild_id: :class:`int`
            The ID of the guild.

        Raises
        -------
        :exc:`.Forbidden`
            The widget for this guild is disabled.
        :exc:`.HTTPException`
            Retrieving the widget failed.

        Returns
        --------
        :class:`.Widget`
            The guild's widget.
        """
        data = await self.http.get_widget(guild_id)
        return Widget(state=(self._connection), data=data)

    async def application_info(self):
        """|coro|

        Retrieves the bot's application information.

        Raises
        -------
        :exc:`.HTTPException`
            Retrieving the information failed somehow.

        Returns
        --------
        :class:`.AppInfo`
            The bot's application information.
        """
        data = await self.http.application_info()
        if 'rpc_origins' not in data:
            data['rpc_origins'] = None
        return AppInfo(self._connection, data)

    async def fetch_user(self, user_id):
        """|coro|

        Retrieves a :class:`~discord.User` based on their ID. This can only
        be used by bot accounts. You do not have to share any guilds
        with the user to get this information, however many operations
        do require that you do.

        .. note::

            This method is an API call. For general usage, consider :meth:`get_user` instead.

        Parameters
        -----------
        user_id: :class:`int`
            The user's ID to fetch from.

        Raises
        -------
        :exc:`.NotFound`
            A user with this ID does not exist.
        :exc:`.HTTPException`
            Fetching the user failed.

        Returns
        --------
        :class:`~discord.User`
            The user you requested.
        """
        data = await self.http.get_user(user_id)
        return User(state=(self._connection), data=data)

    async def fetch_user_profile(self, user_id):
        """|coro|

        Gets an arbitrary user's profile.

        .. note::

            This can only be used by non-bot accounts.

        Parameters
        ------------
        user_id: :class:`int`
            The ID of the user to fetch their profile for.

        Raises
        -------
        :exc:`.Forbidden`
            Not allowed to fetch profiles.
        :exc:`.HTTPException`
            Fetching the profile failed.

        Returns
        --------
        :class:`.Profile`
            The profile of the user.
        """
        state = self._connection
        data = await self.http.get_user_profile(user_id)

        def transform(d):
            return state._get_guild(int(d['id']))

        since = data.get('premium_since')
        mutual_guilds = list(filter(None, map(transform, data.get('mutual_guilds', []))))
        user = data['user']
        return Profile(flags=(user.get('flags', 0)), premium_since=(utils.parse_time(since)),
          mutual_guilds=mutual_guilds,
          user=User(data=user, state=state),
          connected_accounts=(data['connected_accounts']))

    async def fetch_channel(self, channel_id):
        """|coro|

        Retrieves a :class:`.abc.GuildChannel` or :class:`.abc.PrivateChannel` with the specified ID.

        .. note::

            This method is an API call. For general usage, consider :meth:`get_channel` instead.

        .. versionadded:: 1.2

        Raises
        -------
        :exc:`.InvalidData`
            An unknown channel type was received from Discord.
        :exc:`.HTTPException`
            Retrieving the channel failed.
        :exc:`.NotFound`
            Invalid Channel ID.
        :exc:`.Forbidden`
            You do not have permission to fetch this channel.

        Returns
        --------
        Union[:class:`.abc.GuildChannel`, :class:`.abc.PrivateChannel`]
            The channel from the ID.
        """
        data = await self.http.get_channel(channel_id)
        factory, ch_type = _channel_factory(data['type'])
        if factory is None:
            raise InvalidData('Unknown channel type {type} for channel ID {id}.'.format_map(data))
        elif ch_type in (ChannelType.group, ChannelType.private):
            channel = factory(me=(self.user), data=data, state=(self._connection))
        else:
            guild_id = int(data['guild_id'])
            guild = self.get_guild(guild_id) or Object(id=guild_id)
            channel = factory(guild=guild, state=(self._connection), data=data)
        return channel

    async def fetch_webhook(self, webhook_id):
        """|coro|

        Retrieves a :class:`.Webhook` with the specified ID.

        Raises
        --------
        :exc:`.HTTPException`
            Retrieving the webhook failed.
        :exc:`.NotFound`
            Invalid webhook ID.
        :exc:`.Forbidden`
            You do not have permission to fetch this webhook.

        Returns
        ---------
        :class:`.Webhook`
            The webhook you requested.
        """
        data = await self.http.get_webhook(webhook_id)
        return Webhook.from_state(data, state=(self._connection))