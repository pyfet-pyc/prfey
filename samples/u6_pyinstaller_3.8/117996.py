# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\bot.py
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
import asyncio, collections, inspect, importlib.util, sys, traceback, re, types, discord
from .core import GroupMixin, Command
from .view import StringView
from .context import Context
from . import errors
from .help import HelpCommand, DefaultHelpCommand
from .cog import Cog

def when_mentioned(bot, msg):
    """A callable that implements a command prefix equivalent to being mentioned.

    These are meant to be passed into the :attr:`.Bot.command_prefix` attribute.
    """
    return [
     bot.user.mention + ' ', '<@!%s> ' % bot.user.id]


def when_mentioned_or(*prefixes):
    """A callable that implements when mentioned or other prefixes provided.

    These are meant to be passed into the :attr:`.Bot.command_prefix` attribute.

    Example
    --------

    .. code-block:: python3

        bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))

    .. note::

        This callable returns another callable, so if this is done inside a custom
        callable, you must call the returned callable, for example:

        .. code-block:: python3

            async def get_prefix(bot, message):
                extras = await prefixes_for(message.guild) # returns a list
                return commands.when_mentioned_or(*extras)(bot, message)

    See Also
    ----------
    :func:`.when_mentioned`
    """

    def inner(bot, msg):
        r = list(prefixes)
        r = when_mentioned(bot, msg) + r
        return r

    return inner


def _is_submodule(parent, child):
    return parent == child or child.startswith(parent + '.')


class _DefaultRepr:

    def __repr__(self):
        return '<default-help-command>'


_default = _DefaultRepr()

class BotBase(GroupMixin):

    def __init__(self, command_prefix, help_command=_default, description=None, **options):
        (super().__init__)(**options)
        self.command_prefix = command_prefix
        self.extra_events = {}
        self._BotBase__cogs = {}
        self._BotBase__extensions = {}
        self._checks = []
        self._check_once = []
        self._before_invoke = None
        self._after_invoke = None
        self._help_command = None
        self.description = inspect.cleandoc(description) if description else ''
        self.owner_id = options.get('owner_id')
        self.owner_ids = options.get('owner_ids', set())
        if self.owner_id:
            if self.owner_ids:
                raise TypeError('Both owner_id and owner_ids are set.')
        if self.owner_ids:
            if not isinstance(self.owner_ids, collections.abc.Collection):
                raise TypeError('owner_ids must be a collection not {0.__class__!r}'.format(self.owner_ids))
        else:
            if options.pop('self_bot', False):
                self._skip_check = lambda x, y: x != y
            else:
                self._skip_check = lambda x, y: x == y
            if help_command is _default:
                self.help_command = DefaultHelpCommand()
            else:
                self.help_command = help_command

    def dispatch(self, event_name, *args, **kwargs):
        (super().dispatch)(event_name, *args, **kwargs)
        ev = 'on_' + event_name
        for event in self.extra_events.get(ev, []):
            (self._schedule_event)(event, ev, *args, **kwargs)

    async def close(self):
        for extension in tuple(self._BotBase__extensions):
            try:
                self.unload_extension(extension)
            except Exception:
                pass

        else:
            for cog in tuple(self._BotBase__cogs):
                try:
                    self.remove_cog(cog)
                except Exception:
                    pass

            else:
                await super().close()

    async def on_command_error(self, context, exception):
        """|coro|

        The default command error handler provided by the bot.

        By default this prints to :data:`sys.stderr` however it could be
        overridden to have a different implementation.

        This only fires if you do not specify any listeners for command error.
        """
        if self.extra_events.get('on_command_error', None):
            return
        else:
            if hasattr(context.command, 'on_error'):
                return
            cog = context.cog
            if cog and Cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        print(('Ignoring exception in command {}:'.format(context.command)), file=(sys.stderr))
        traceback.print_exception((type(exception)), exception, (exception.__traceback__), file=(sys.stderr))

    def check(self, func):
        r"""A decorator that adds a global check to the bot.

        A global check is similar to a :func:`.check` that is applied
        on a per command basis except it is run before any command checks
        have been verified and applies to every command the bot has.

        .. note::

            This function can either be a regular function or a coroutine.

        Similar to a command :func:`.check`\, this takes a single parameter
        of type :class:`.Context` and can only raise exceptions inherited from
        :exc:`.CommandError`.

        Example
        ---------

        .. code-block:: python3

            @bot.check
            def check_commands(ctx):
                return ctx.command.qualified_name in allowed_commands

        """
        self.add_check(func)
        return func

    def add_check(self, func, *, call_once=False):
        """Adds a global check to the bot.

        This is the non-decorator interface to :meth:`.check`
        and :meth:`.check_once`.

        Parameters
        -----------
        func
            The function that was used as a global check.
        call_once: :class:`bool`
            If the function should only be called once per
            :meth:`Command.invoke` call.
        """
        if call_once:
            self._check_once.append(func)
        else:
            self._checks.append(func)

    def remove_check(self, func, *, call_once=False):
        """Removes a global check from the bot.

        This function is idempotent and will not raise an exception
        if the function is not in the global checks.

        Parameters
        -----------
        func
            The function to remove from the global checks.
        call_once: :class:`bool`
            If the function was added with ``call_once=True`` in
            the :meth:`.Bot.add_check` call or using :meth:`.check_once`.
        """
        l = self._check_once if call_once else self._checks
        try:
            l.remove(func)
        except ValueError:
            pass

    def check_once(self, func):
        r"""A decorator that adds a "call once" global check to the bot.

        Unlike regular global checks, this one is called only once
        per :meth:`Command.invoke` call.

        Regular global checks are called whenever a command is called
        or :meth:`.Command.can_run` is called. This type of check
        bypasses that and ensures that it's called only once, even inside
        the default help command.

        .. note::

            This function can either be a regular function or a coroutine.

        Similar to a command :func:`.check`\, this takes a single parameter
        of type :class:`.Context` and can only raise exceptions inherited from
        :exc:`.CommandError`.

        Example
        ---------

        .. code-block:: python3

            @bot.check_once
            def whitelist(ctx):
                return ctx.message.author.id in my_whitelist

        """
        self.add_check(func, call_once=True)
        return func

    async def can_run(self, ctx, *, call_once=False):
        data = self._check_once if call_once else self._checks
        if len(data) == 0:
            return True
        return await discord.utils.async_all((f(ctx) for f in data))

    async def is_owner(self, user):
        """|coro|

        Checks if a :class:`~discord.User` or :class:`~discord.Member` is the owner of
        this bot.

        If an :attr:`owner_id` is not set, it is fetched automatically
        through the use of :meth:`~.Bot.application_info`.

        .. versionchanged:: 1.3
            The function also checks if the application is team-owned if
            :attr:`owner_ids` is not set.

        Parameters
        -----------
        user: :class:`.abc.User`
            The user to check for.

        Returns
        --------
        :class:`bool`
            Whether the user is the owner.
        """
        if self.owner_id:
            return user.id == self.owner_id
        if self.owner_ids:
            return user.id in self.owner_ids
        app = await self.application_info()
        if app.team:
            self.owner_ids = ids = {m.id for m in app.team.members}
            return user.id in ids
        self.owner_id = owner_id = app.owner.id
        return user.id == owner_id

    def before_invoke(self, coro):
        """A decorator that registers a coroutine as a pre-invoke hook.

        A pre-invoke hook is called directly before the command is
        called. This makes it a useful function to set up database
        connections or any type of set up required.

        This pre-invoke hook takes a sole parameter, a :class:`.Context`.

        .. note::

            The :meth:`~.Bot.before_invoke` and :meth:`~.Bot.after_invoke` hooks are
            only called if all checks and argument parsing procedures pass
            without error. If any check or argument parsing procedures fail
            then the hooks are not called.

        Parameters
        -----------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register as the pre-invoke hook.

        Raises
        -------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The pre-invoke hook must be a coroutine.')
        self._before_invoke = coro
        return coro

    def after_invoke(self, coro):
        r"""A decorator that registers a coroutine as a post-invoke hook.

        A post-invoke hook is called directly after the command is
        called. This makes it a useful function to clean-up database
        connections or any type of clean up required.

        This post-invoke hook takes a sole parameter, a :class:`.Context`.

        .. note::

            Similar to :meth:`~.Bot.before_invoke`\, this is not called unless
            checks and argument parsing procedures succeed. This hook is,
            however, **always** called regardless of the internal command
            callback raising an error (i.e. :exc:`.CommandInvokeError`\).
            This makes it ideal for clean-up scenarios.

        Parameters
        -----------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register as the post-invoke hook.

        Raises
        -------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The post-invoke hook must be a coroutine.')
        self._after_invoke = coro
        return coro

    def add_listener(self, func, name=None):
        """The non decorator alternative to :meth:`.listen`.

        Parameters
        -----------
        func: :ref:`coroutine <coroutine>`
            The function to call.
        name: Optional[:class:`str`]
            The name of the event to listen for. Defaults to ``func.__name__``.

        Example
        --------

        .. code-block:: python3

            async def on_ready(): pass
            async def my_message(message): pass

            bot.add_listener(on_ready)
            bot.add_listener(my_message, 'on_message')

        """
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Listeners must be coroutines')
        elif name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [
             func]

    def remove_listener(self, func, name=None):
        """Removes a listener from the pool of listeners.

        Parameters
        -----------
        func
            The function that was used as a listener to remove.
        name: :class:`str`
            The name of the event we want to remove. Defaults to
            ``func.__name__``.
        """
        name = func.__name__ if name is None else name
        if name in self.extra_events:
            try:
                self.extra_events[name].remove(func)
            except ValueError:
                pass

    def listen(self, name=None):
        """A decorator that registers another function as an external
        event listener. Basically this allows you to listen to multiple
        events from different places e.g. such as :func:`.on_ready`

        The functions being listened to must be a :ref:`coroutine <coroutine>`.

        Example
        --------

        .. code-block:: python3

            @bot.listen()
            async def on_message(message):
                print('one')

            # in some other file...

            @bot.listen('on_message')
            async def my_message(message):
                print('two')

        Would print one and two in an unspecified order.

        Raises
        -------
        TypeError
            The function being listened to is not a coroutine.
        """

        def decorator(func):
            self.add_listener(func, name)
            return func

        return decorator

    def add_cog(self, cog):
        """Adds a "cog" to the bot.

        A cog is a class that has its own event listeners and commands.

        Parameters
        -----------
        cog: :class:`.Cog`
            The cog to register to the bot.

        Raises
        -------
        TypeError
            The cog does not inherit from :class:`.Cog`.
        CommandError
            An error happened during loading.
        """
        if not isinstance(cog, Cog):
            raise TypeError('cogs must derive from Cog')
        cog = cog._inject(self)
        self._BotBase__cogs[cog.__cog_name__] = cog

    def get_cog(self, name):
        """Gets the cog instance requested.

        If the cog is not found, ``None`` is returned instead.

        Parameters
        -----------
        name: :class:`str`
            The name of the cog you are requesting.
            This is equivalent to the name passed via keyword
            argument in class creation or the class name if unspecified.
        """
        return self._BotBase__cogs.get(name)

    def remove_cog(self, name):
        """Removes a cog from the bot.

        All registered commands and event listeners that the
        cog has registered will be removed as well.

        If no cog is found then this method has no effect.

        Parameters
        -----------
        name: :class:`str`
            The name of the cog to remove.
        """
        cog = self._BotBase__cogs.pop(name, None)
        if cog is None:
            return
        help_command = self._help_command
        if help_command:
            if help_command.cog is cog:
                help_command.cog = None
        cog._eject(self)

    @property
    def cogs(self):
        """Mapping[:class:`str`, :class:`Cog`]: A read-only mapping of cog name to cog."""
        return types.MappingProxyType(self._BotBase__cogs)

    def _remove_module_references(self, name):
        for cogname, cog in self._BotBase__cogs.copy().items():
            if _is_submodule(name, cog.__module__):
                self.remove_cog(cogname)
        else:
            for cmd in self.all_commands.copy().values():
                if cmd.module is not None:
                    if _is_submodule(name, cmd.module):
                        if isinstance(cmd, GroupMixin):
                            cmd.recursively_remove_all_commands()
                    self.remove_command(cmd.name)
            else:
                for event_list in self.extra_events.copy().values():
                    remove = []
                    for index, event in enumerate(event_list):
                        if event.__module__ is not None and _is_submodule(name, event.__module__):
                            remove.append(index)

                else:
                    for index in reversed(remove):
                        del event_list[index]

    def _call_module_finalizers(self, lib, key):
        try:
            try:
                func = getattr(lib, 'teardown')
            except AttributeError:
                pass

            try:
                func(self)
            except Exception:
                pass

        finally:
            self._BotBase__extensions.pop(key, None)
            sys.modules.pop(key, None)
            name = lib.__name__
            for module in list(sys.modules.keys()):
                if _is_submodule(name, module):
                    del sys.modules[module]

    def _load_from_module_spec(self, spec, key):
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            try:
                del sys.modules[key]
                raise errors.ExtensionFailed(key, e) from e
            finally:
                e = None
                del e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise errors.NoEntryPointError(key)
        else:
            try:
                setup(self)
            except Exception as e:
                try:
                    del sys.modules[key]
                    self._remove_module_references(lib.__name__)
                    self._call_module_finalizers(lib, key)
                    raise errors.ExtensionFailed(key, e) from e
                finally:
                    e = None
                    del e

            else:
                self._BotBase__extensions[key] = lib

    def load_extension(self, name):
        """Loads an extension.

        An extension is a python module that contains commands, cogs, or
        listeners.

        An extension must have a global function, ``setup`` defined as
        the entry point on what to do when the extension is loaded. This entry
        point must have a single argument, the ``bot``.

        Parameters
        ------------
        name: :class:`str`
            The extension name to load. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.

        Raises
        --------
        ExtensionNotFound
            The extension could not be imported.
        ExtensionAlreadyLoaded
            The extension is already loaded.
        NoEntryPointError
            The extension does not have a setup function.
        ExtensionFailed
            The extension or its setup function had an execution error.
        """
        if name in self._BotBase__extensions:
            raise errors.ExtensionAlreadyLoaded(name)
        spec = importlib.util.find_spec(name)
        if spec is None:
            raise errors.ExtensionNotFound(name)
        self._load_from_module_spec(spec, name)

    def unload_extension(self, name):
        """Unloads an extension.

        When the extension is unloaded, all commands, listeners, and cogs are
        removed from the bot and the module is un-imported.

        The extension can provide an optional global function, ``teardown``,
        to do miscellaneous clean-up if necessary. This function takes a single
        parameter, the ``bot``, similar to ``setup`` from
        :meth:`~.Bot.load_extension`.

        Parameters
        ------------
        name: :class:`str`
            The extension name to unload. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.

        Raises
        -------
        ExtensionNotLoaded
            The extension was not loaded.
        """
        lib = self._BotBase__extensions.get(name)
        if lib is None:
            raise errors.ExtensionNotLoaded(name)
        self._remove_module_references(lib.__name__)
        self._call_module_finalizers(lib, name)

    def reload_extension--- This code section failed: ---

 L. 713         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _BotBase__extensions
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_DEREF              'lib'

 L. 714        12  LOAD_DEREF               'lib'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 715        20  LOAD_GLOBAL              errors
               22  LOAD_METHOD              ExtensionNotLoaded
               24  LOAD_FAST                'name'
               26  CALL_METHOD_1         1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            18  '18'

 L. 718        30  LOAD_CLOSURE             'lib'
               32  BUILD_TUPLE_1         1 
               34  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               36  LOAD_STR                 'BotBase.reload_extension.<locals>.<dictcomp>'
               38  MAKE_FUNCTION_8          'closure'

 L. 720        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                modules
               44  LOAD_METHOD              items
               46  CALL_METHOD_0         0  ''

 L. 718        48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'modules'

 L. 724        54  SETUP_FINALLY        94  'to 94'

 L. 726        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _remove_module_references
               60  LOAD_DEREF               'lib'
               62  LOAD_ATTR                __name__
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 727        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _call_module_finalizers
               72  LOAD_DEREF               'lib'
               74  LOAD_FAST                'name'
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          

 L. 728        80  LOAD_FAST                'self'
               82  LOAD_METHOD              load_extension
               84  LOAD_FAST                'name'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  JUMP_FORWARD        162  'to 162'
             94_0  COME_FROM_FINALLY    54  '54'

 L. 729        94  DUP_TOP          
               96  LOAD_GLOBAL              Exception
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   160  'to 160'
              102  POP_TOP          
              104  STORE_FAST               'e'
              106  POP_TOP          
              108  SETUP_FINALLY       148  'to 148'

 L. 733       110  LOAD_DEREF               'lib'
              112  LOAD_METHOD              setup
              114  LOAD_FAST                'self'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 734       120  LOAD_DEREF               'lib'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                _BotBase__extensions
              126  LOAD_FAST                'name'
              128  STORE_SUBSCR     

 L. 737       130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                modules
              134  LOAD_METHOD              update
              136  LOAD_FAST                'modules'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 738       142  RAISE_VARARGS_0       0  'reraise'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM_FINALLY   108  '108'
              148  LOAD_CONST               None
              150  STORE_FAST               'e'
              152  DELETE_FAST              'e'
              154  END_FINALLY      
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           100  '100'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM            92  '92'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 34

    @property
    def extensions(self):
        """Mapping[:class:`str`, :class:`py:types.ModuleType`]: A read-only mapping of extension name to extension."""
        return types.MappingProxyType(self._BotBase__extensions)

    @property
    def help_command(self):
        return self._help_command

    @help_command.setter
    def help_command(self, value):
        if value is not None:
            if not isinstance(value, HelpCommand):
                raise TypeError('help_command must be a subclass of HelpCommand')
            if self._help_command is not None:
                self._help_command._remove_from_bot(self)
            self._help_command = value
            value._add_to_bot(self)
        else:
            if self._help_command is not None:
                self._help_command._remove_from_bot(self)
                self._help_command = None
            else:
                self._help_command = None

    async def get_prefix(self, message):
        """|coro|

        Retrieves the prefix the bot is listening to
        with the message as a context.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message context to get the prefix of.

        Returns
        --------
        Union[List[:class:`str`], :class:`str`]
            A list of prefixes or a single prefix that the bot is
            listening for.
        """
        prefix = ret = self.command_prefix
        if callable(prefix):
            ret = await discord.utils.maybe_coroutine(prefix, self, message)
        if not isinstance(ret, str):
            try:
                ret = list(ret)
            except TypeError:
                if isinstance(ret, collections.abc.Iterable):
                    raise
                raise TypeError('command_prefix must be plain string, iterable of strings, or callable returning either of these, not {}'.format(ret.__class__.__name__))
            else:
                if not ret:
                    raise ValueError('Iterable command_prefix must contain at least one prefix')
        return ret

    async def get_context(self, message, *, cls=Context):
        r"""|coro|

        Returns the invocation context from the message.

        This is a more low-level counter-part for :meth:`.process_commands`
        to allow users more fine grained control over the processing.

        The returned context is not guaranteed to be a valid invocation
        context, :attr:`.Context.valid` must be checked to make sure it is.
        If the context is not valid then it is not a valid candidate to be
        invoked under :meth:`~.Bot.invoke`.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to get the invocation context from.
        cls
            The factory class that will be used to create the context.
            By default, this is :class:`.Context`. Should a custom
            class be provided, it must be similar enough to :class:`.Context`\'s
            interface.

        Returns
        --------
        :class:`.Context`
            The invocation context. The type of this can change via the
            ``cls`` parameter.
        """
        view = StringView(message.content)
        ctx = cls(prefix=None, view=view, bot=self, message=message)
        if self._skip_check(message.author.id, self.user.id):
            return ctx
        prefix = await self.get_prefix(message)
        invoked_prefix = prefix
        if isinstance(prefix, str):
            return view.skip_string(prefix) or ctx
        else:
            try:
                if message.content.startswith(tuple(prefix)):
                    invoked_prefix = discord.utils.find(view.skip_string, prefix)
                else:
                    return ctx
            except TypeError:
                if not isinstance(prefix, list):
                    raise TypeError('get_prefix must return either a string or a list of string, not {}'.format(prefix.__class__.__name__))
                for value in prefix:
                    if not isinstance(value, str):
                        raise TypeError('Iterable command_prefix or list returned from get_prefix must contain only strings, not {}'.format(value.__class__.__name__))
                else:
                    raise

            else:
                invoker = view.get_word()
                ctx.invoked_with = invoker
                ctx.prefix = invoked_prefix
                ctx.command = self.all_commands.get(invoker)
                return ctx

    async def invoke(self, ctx):
        """|coro|

        Invokes the command given under the invocation context and
        handles all the internal event dispatch mechanisms.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to invoke.
        """
        if ctx.command is not None:
            self.dispatch('command', ctx)
            try:
                if await self.can_run(ctx, call_once=True):
                    await ctx.command.invoke(ctx)
            except errors.CommandError as exc:
                try:
                    await ctx.command.dispatch_error(ctx, exc)
                finally:
                    exc = None
                    del exc

            else:
                self.dispatch('command_completion', ctx)
        else:
            if ctx.invoked_with:
                exc = errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
                self.dispatch('command_error', ctx, exc)

    async def process_commands(self, message):
        """|coro|

        This function processes the commands that have been registered
        to the bot and other groups. Without this coroutine, none of the
        commands will be triggered.

        By default, this coroutine is called inside the :func:`.on_message`
        event. If you choose to override the :func:`.on_message` event, then
        you should invoke this coroutine as well.

        This is built using other low level tools, and is equivalent to a
        call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.

        This also checks if the message's author is a bot and doesn't
        call :meth:`~.Bot.get_context` or :meth:`~.Bot.invoke` if so.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to process commands for.
        """
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_message(self, message):
        await self.process_commands(message)


class Bot(BotBase, discord.Client):
    __doc__ = 'Represents a discord bot.\n\n    This class is a subclass of :class:`discord.Client` and as a result\n    anything that you can do with a :class:`discord.Client` you can do with\n    this bot.\n\n    This class also subclasses :class:`.GroupMixin` to provide the functionality\n    to manage commands.\n\n    Attributes\n    -----------\n    command_prefix\n        The command prefix is what the message content must contain initially\n        to have a command invoked. This prefix could either be a string to\n        indicate what the prefix should be, or a callable that takes in the bot\n        as its first parameter and :class:`discord.Message` as its second\n        parameter and returns the prefix. This is to facilitate "dynamic"\n        command prefixes. This callable can be either a regular function or\n        a coroutine.\n\n        An empty string as the prefix always matches, enabling prefix-less\n        command invocation. While this may be useful in DMs it should be avoided\n        in servers, as it\'s likely to cause performance issues and unintended\n        command invocations.\n\n        The command prefix could also be an iterable of strings indicating that\n        multiple checks for the prefix should be used and the first one to\n        match will be the invocation prefix. You can get this prefix via\n        :attr:`.Context.prefix`. To avoid confusion empty iterables are not\n        allowed.\n\n        .. note::\n\n            When passing multiple prefixes be careful to not pass a prefix\n            that matches a longer prefix occurring later in the sequence.  For\n            example, if the command prefix is ``(\'!\', \'!?\')``  the ``\'!?\'``\n            prefix will never be matched to any message as the previous one\n            matches messages starting with ``!?``. This is especially important\n            when passing an empty string, it should always be last as no prefix\n            after it will be matched.\n    case_insensitive: :class:`bool`\n        Whether the commands should be case insensitive. Defaults to ``False``. This\n        attribute does not carry over to groups. You must set it to every group if\n        you require group commands to be case insensitive as well.\n    description: :class:`str`\n        The content prefixed into the default help message.\n    self_bot: :class:`bool`\n        If ``True``, the bot will only listen to commands invoked by itself rather\n        than ignoring itself. If ``False`` (the default) then the bot will ignore\n        itself. This cannot be changed once initialised.\n    help_command: Optional[:class:`.HelpCommand`]\n        The help command implementation to use. This can be dynamically\n        set at runtime. To remove the help command pass ``None``. For more\n        information on implementing a help command, see :ref:`ext_commands_help_command`.\n    owner_id: Optional[:class:`int`]\n        The user ID that owns the bot. If this is not set and is then queried via\n        :meth:`.is_owner` then it is fetched automatically using\n        :meth:`~.Bot.application_info`.\n    owner_ids: Optional[Collection[:class:`int`]]\n        The user IDs that owns the bot. This is similar to `owner_id`.\n        If this is not set and the application is team based, then it is\n        fetched automatically using :meth:`~.Bot.application_info`.\n        For performance reasons it is recommended to use a :class:`set`\n        for the collection. You cannot set both `owner_id` and `owner_ids`.\n\n        .. versionadded:: 1.3\n    '


class AutoShardedBot(BotBase, discord.AutoShardedClient):
    __doc__ = 'This is similar to :class:`.Bot` except that it is inherited from\n    :class:`discord.AutoShardedClient` instead.\n    '