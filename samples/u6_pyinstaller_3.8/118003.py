# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\help.py
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
import itertools, copy, functools, inspect, re, discord.utils
from .core import Group, Command
from .errors import CommandError
__all__ = ('Paginator', 'HelpCommand', 'DefaultHelpCommand', 'MinimalHelpCommand')

class Paginator:
    __doc__ = 'A class that aids in paginating code blocks for Discord messages.\n\n    .. container:: operations\n\n        .. describe:: len(x)\n\n            Returns the total number of characters in the paginator.\n\n    Attributes\n    -----------\n    prefix: :class:`str`\n        The prefix inserted to every page. e.g. three backticks.\n    suffix: :class:`str`\n        The suffix appended at the end of every page. e.g. three backticks.\n    max_size: :class:`int`\n        The maximum amount of codepoints allowed in a page.\n    '

    def __init__(self, prefix='```', suffix='```', max_size=2000):
        self.prefix = prefix
        self.suffix = suffix
        self.max_size = max_size
        self.clear()

    def clear(self):
        """Clears the paginator to have no pages."""
        if self.prefix is not None:
            self._current_page = [
             self.prefix]
            self._count = len(self.prefix) + 1
        else:
            self._current_page = []
            self._count = 0
        self._pages = []

    @property
    def _prefix_len(self):
        if self.prefix:
            return len(self.prefix)
        return 0

    @property
    def _suffix_len(self):
        if self.suffix:
            return len(self.suffix)
        return 0

    def add_line(self, line='', *, empty=False):
        """Adds a line to the current page.

        If the line exceeds the :attr:`max_size` then an exception
        is raised.

        Parameters
        -----------
        line: :class:`str`
            The line to add.
        empty: :class:`bool`
            Indicates if another empty line should be added.

        Raises
        ------
        RuntimeError
            The line was too big for the current :attr:`max_size`.
        """
        max_page_size = self.max_size - self._prefix_len - self._suffix_len - 2
        if len(line) > max_page_size:
            raise RuntimeError('Line exceeds maximum page size %s' % max_page_size)
        if self._count + len(line) + 1 > self.max_size - self._suffix_len:
            self.close_page()
        self._count += len(line) + 1
        self._current_page.append(line)
        if empty:
            self._current_page.append('')
            self._count += 1

    def close_page(self):
        """Prematurely terminate a page."""
        if self.suffix is not None:
            self._current_page.append(self.suffix)
        else:
            self._pages.append('\n'.join(self._current_page))
            if self.prefix is not None:
                self._current_page = [
                 self.prefix]
                self._count = len(self.prefix) + 1
            else:
                self._current_page = []
            self._count = 0

    def __len__(self):
        total = sum((len(p) for p in self._pages))
        return total + self._count

    @property
    def pages(self):
        """Returns the rendered list of pages."""
        if len(self._current_page) > (0 if self.prefix is None else 1):
            self.close_page()
        return self._pages

    def __repr__(self):
        fmt = '<Paginator prefix: {0.prefix} suffix: {0.suffix} max_size: {0.max_size} count: {0._count}>'
        return fmt.format(self)


def _not_overriden(f):
    f.__help_command_not_overriden__ = True
    return f


class _HelpCommandImpl(Command):

    def __init__(self, inject, *args, **kwargs):
        (super().__init__)(inject.command_callback, *args, **kwargs)
        self._original = inject
        self._injected = inject

    async def prepare(self, ctx):
        self._injected = injected = self._original.copy()
        injected.context = ctx
        self.callback = injected.command_callback
        on_error = injected.on_help_command_error
        if not hasattr(on_error, '__help_command_not_overriden__'):
            if self.cog is not None:
                self.on_error = self._on_error_cog_implementation
            else:
                self.on_error = on_error
        await super().prepare(ctx)

    async def _parse_arguments(self, ctx):
        original_cog = self.cog
        self.cog = None
        try:
            await super()._parse_arguments(ctx)
        finally:
            self.cog = original_cog

    async def _on_error_cog_implementation(self, dummy, ctx, error):
        await self._injected.on_help_command_error(ctx, error)

    @property
    def clean_params(self):
        result = self.params.copy()
        try:
            result.popitem(last=False)
        except Exception:
            raise ValueError('Missing context parameter') from None
        else:
            return result

    def _inject_into_cog(self, cog):

        def wrapped_get_commands(*, _original=cog.get_commands):
            ret = _original()
            ret.append(self)
            return ret

        def wrapped_walk_commands(*, _original=cog.walk_commands):
            (yield from _original())
            (yield self)

        functools.update_wrapper(wrapped_get_commands, cog.get_commands)
        functools.update_wrapper(wrapped_walk_commands, cog.walk_commands)
        cog.get_commands = wrapped_get_commands
        cog.walk_commands = wrapped_walk_commands
        self.cog = cog

    def _eject_cog(self):
        if self.cog is None:
            return
        cog = self.cog
        cog.get_commands = cog.get_commands.__wrapped__
        cog.walk_commands = cog.walk_commands.__wrapped__
        self.cog = None


class HelpCommand:
    __doc__ = 'The base implementation for help command formatting.\n\n    .. note::\n\n        Internally instances of this class are deep copied every time\n        the command itself is invoked to prevent a race condition\n        mentioned in :issue:`2123`.\n\n        This means that relying on the state of this class to be\n        the same between command invocations would not work as expected.\n\n    Attributes\n    ------------\n    context: Optional[:class:`Context`]\n        The context that invoked this help formatter. This is generally set after\n        the help command assigned, :func:`command_callback`\\, has been called.\n    show_hidden: :class:`bool`\n        Specifies if hidden commands should be shown in the output.\n        Defaults to ``False``.\n    verify_checks: :class:`bool`\n        Specifies if commands should have their :attr:`.Command.checks` called\n        and verified. Defaults to ``True``.\n    command_attrs: :class:`dict`\n        A dictionary of options to pass in for the construction of the help command.\n        This allows you to change the command behaviour without actually changing\n        the implementation of the command. The attributes will be the same as the\n        ones passed in the :class:`.Command` constructor.\n    '
    MENTION_TRANSFORMS = {'@everyone':'@\u200beveryone', 
     '@here':'@\u200bhere', 
     '<@!?[0-9]{17,22}>':'@deleted-user', 
     '<@&[0-9]{17,22}>':'@deleted-role'}
    MENTION_PATTERN = re.compile('|'.join(MENTION_TRANSFORMS.keys()))

    def __new__--- This code section failed: ---

 L. 291         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __new__
                6  LOAD_FAST                'cls'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'self'

 L. 297        12  LOAD_GLOBAL              copy
               14  LOAD_ATTR                deepcopy
               16  STORE_DEREF              'deepcopy'

 L. 298        18  LOAD_CLOSURE             'deepcopy'
               20  BUILD_TUPLE_1         1 
               22  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               24  LOAD_STR                 'HelpCommand.__new__.<locals>.<dictcomp>'
               26  MAKE_FUNCTION_8          'closure'

 L. 300        28  LOAD_FAST                'kwargs'
               30  LOAD_METHOD              items
               32  CALL_METHOD_0         0  ''

 L. 298        34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_FAST                'self'
               40  STORE_ATTR               __original_kwargs__

 L. 302        42  LOAD_DEREF               'deepcopy'
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               __original_args__

 L. 303        52  LOAD_FAST                'self'
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 22

    def __init__(self, **options):
        self.show_hidden = options.pop('show_hidden', False)
        self.verify_checks = options.pop('verify_checks', True)
        self.command_attrs = attrs = options.pop('command_attrs', {})
        attrs.setdefault('name', 'help')
        attrs.setdefault('help', 'Shows this message')
        self.context = None
        self._command_impl = None

    def copy(self):
        obj = (self.__class__)(*self.__original_args__, **self.__original_kwargs__)
        obj._command_impl = self._command_impl
        return obj

    def _add_to_bot(self, bot):
        command = _HelpCommandImpl(self, **self.command_attrs)
        bot.add_command(command)
        self._command_impl = command

    def _remove_from_bot(self, bot):
        bot.remove_command(self._command_impl.name)
        self._command_impl._eject_cog()
        self._command_impl = None

    def get_bot_mapping(self):
        """Retrieves the bot mapping passed to :meth:`send_bot_help`."""
        bot = self.context.bot
        mapping = {cog.get_commands():cog for cog in bot.cogs.values()}
        mapping[None] = [c for c in bot.all_commands.values() if c.cog is None]
        return mapping

    @property
    def clean_prefix(self):
        """The cleaned up invoke prefix. i.e. mentions are ``@name`` instead of ``<@id>``."""
        user = self.context.guild.me if self.context.guild else self.context.bot.user
        pattern = re.compile('<@!?%s>' % user.id)
        return pattern.sub('@%s' % user.display_name, self.context.prefix)

    @property
    def invoked_with(self):
        """Similar to :attr:`Context.invoked_with` except properly handles
        the case where :meth:`Context.send_help` is used.

        If the help command was used regularly then this returns
        the :attr:`Context.invoked_with` attribute. Otherwise, if
        it the help command was called using :meth:`Context.send_help`
        then it returns the internal command name of the help command.

        Returns
        ---------
        :class:`str`
            The command name that triggered this invocation.
        """
        command_name = self._command_impl.name
        ctx = self.context
        if ctx is None or ctx.command is None or ctx.command.qualified_name != command_name:
            return command_name
        return ctx.invoked_with

    def get_command_signature(self, command):
        """Retrieves the signature portion of the help page.

        Parameters
        ------------
        command: :class:`Command`
            The command to get the signature of.

        Returns
        --------
        :class:`str`
            The signature for the command.
        """
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = '[%s|%s]' % (command.name, aliases)
            if parent:
                fmt = parent + ' ' + fmt
            alias = fmt
        else:
            alias = command.name if not parent else parent + ' ' + command.name
        return '%s%s %s' % (self.clean_prefix, alias, command.signature)

    def remove_mentions(self, string):
        """Removes mentions from the string to prevent abuse.

        This includes ``@everyone``, ``@here``, member mentions and role mentions.
        """

        def replace(obj, *, transforms=self.MENTION_TRANSFORMS):
            return transforms.get(obj.group(0), '@invalid')

        return self.MENTION_PATTERN.sub(replace, string)

    @property
    def cog(self):
        """A property for retrieving or setting the cog for the help command.

        When a cog is set for the help command, it is as-if the help command
        belongs to that cog. All cog special methods will apply to the help
        command and it will be automatically unset on unload.

        To unbind the cog from the help command, you can set it to ``None``.

        Returns
        --------
        Optional[:class:`Cog`]
            The cog that is currently set for the help command.
        """
        return self._command_impl.cog

    @cog.setter
    def cog(self, cog):
        self._command_impl._eject_cog()
        if cog is not None:
            self._command_impl._inject_into_cog(cog)

    def command_not_found(self, string):
        """|maybecoro|

        A method called when a command is not found in the help command.
        This is useful to override for i18n.

        Defaults to ``No command called {0} found.``

        Parameters
        ------------
        string: :class:`str`
            The string that contains the invalid command. Note that this has
            had mentions removed to prevent abuse.

        Returns
        ---------
        :class:`str`
            The string to use when a command has not been found.
        """
        return 'No command called "{}" found.'.format(string)

    def subcommand_not_found(self, command, string):
        """|maybecoro|

        A method called when a command did not have a subcommand requested in the help command.
        This is useful to override for i18n.

        Defaults to either:

        - ``'Command "{command.qualified_name}" has no subcommands.'``
            - If there is no subcommand in the ``command`` parameter.
        - ``'Command "{command.qualified_name}" has no subcommand named {string}'``
            - If the ``command`` parameter has subcommands but not one named ``string``.

        Parameters
        ------------
        command: :class:`Command`
            The command that did not have the subcommand requested.
        string: :class:`str`
            The string that contains the invalid subcommand. Note that this has
            had mentions removed to prevent abuse.

        Returns
        ---------
        :class:`str`
            The string to use when the command did not have the subcommand requested.
        """
        if isinstance(command, Group):
            if len(command.all_commands) > 0:
                return 'Command "{0.qualified_name}" has no subcommand named {1}'.format(command, string)
        return 'Command "{0.qualified_name}" has no subcommands.'.format(command)

    async def filter_commands(self, commands, *, sort=False, key=None):
        """|coro|

        Returns a filtered list of commands and optionally sorts them.

        This takes into account the :attr:`verify_checks` and :attr:`show_hidden`
        attributes.

        Parameters
        ------------
        commands: Iterable[:class:`Command`]
            An iterable of commands that are getting filtered.
        sort: :class:`bool`
            Whether to sort the result.
        key: Optional[Callable[:class:`Command`, Any]]
            An optional key function to pass to :func:`py:sorted` that
            takes a :class:`Command` as its sole parameter. If ``sort`` is
            passed as ``True`` then this will default as the command name.

        Returns
        ---------
        List[:class:`Command`]
            A list of commands that passed the filter.
        """
        if sort:
            if key is None:
                key = lambda c: c.name
        iterator = commands if self.show_hidden else filter(lambda c: not c.hidden, commands)
        if not self.verify_checks:
            if sort:
                return sorted(iterator, key=key)
            return list(iterator)

        async def predicate--- This code section failed: ---

 L. 522         0  SETUP_FINALLY        22  'to 22'

 L. 523         2  LOAD_FAST                'cmd'
                4  LOAD_METHOD              can_run
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                context
               10  CALL_METHOD_1         1  ''
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 524        22  DUP_TOP          
               24  LOAD_GLOBAL              CommandError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    42  'to 42'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 525        36  POP_EXCEPT       
               38  LOAD_CONST               False
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 32

        ret = []
        for cmd in iterator:
            valid = await predicate(cmd)
            if valid:
                ret.append(cmd)
            if sort:
                ret.sort(key=key)
            return ret

    def get_max_size(self, commands):
        """Returns the largest name length of the specified command list.

        Parameters
        ------------
        commands: Sequence[:class:`Command`]
            A sequence of commands to check for the largest size.

        Returns
        --------
        :class:`int`
            The maximum width of the commands.
        """
        as_lengths = (discord.utils._string_width(c.name) for c in commands)
        return max(as_lengths, default=0)

    def get_destination(self):
        """Returns the :class:`~discord.abc.Messageable` where the help command will be output.

        You can override this method to customise the behaviour.

        By default this returns the context's channel.
        """
        return self.context.channel

    async def send_error_message(self, error):
        """|coro|

        Handles the implementation when an error happens in the help command.
        For example, the result of :meth:`command_not_found` or
        :meth:`command_has_no_subcommand_found` will be passed here.

        You can override this method to customise the behaviour.

        By default, this sends the error message to the destination
        specified by :meth:`get_destination`.

        .. note::

            You can access the invocation context with :attr:`HelpCommand.context`.

        Parameters
        ------------
        error: :class:`str`
            The error message to display to the user. Note that this has
            had mentions removed to prevent abuse.
        """
        destination = self.get_destination()
        await destination.send(error)

    @_not_overriden
    async def on_help_command_error(self, ctx, error):
        """|coro|

        The help command's error handler, as specified by :ref:`ext_commands_error_handler`.

        Useful to override if you need some specific behaviour when the error handler
        is called.

        By default this method does nothing and just propagates to the default
        error handlers.

        Parameters
        ------------
        ctx: :class:`Context`
            The invocation context.
        error: :class:`CommandError`
            The error that was raised.
        """
        pass

    async def send_bot_help(self, mapping):
        """|coro|

        Handles the implementation of the bot command page in the help command.
        This function is called when the help command is called with no arguments.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method. Well behaved subclasses
        should use :meth:`get_destination` to know where to send, as this is a customisation
        point for other users.

        You can override this method to customise the behaviour.

        .. note::

            You can access the invocation context with :attr:`HelpCommand.context`.

            Also, the commands in the mapping are not filtered. To do the filtering
            you will have to call :meth:`filter_commands` yourself.

        Parameters
        ------------
        mapping: Mapping[Optional[:class:`Cog`], List[:class:`Command`]]
            A mapping of cogs to commands that have been requested by the user for help.
            The key of the mapping is the :class:`~.commands.Cog` that the command belongs to, or
            ``None`` if there isn't one, and the value is a list of commands that belongs to that cog.
        """
        pass

    async def send_cog_help(self, cog):
        """|coro|

        Handles the implementation of the cog page in the help command.
        This function is called when the help command is called with a cog as the argument.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method. Well behaved subclasses
        should use :meth:`get_destination` to know where to send, as this is a customisation
        point for other users.

        You can override this method to customise the behaviour.

        .. note::

            You can access the invocation context with :attr:`HelpCommand.context`.

            To get the commands that belong to this cog see :meth:`Cog.get_commands`.
            The commands returned not filtered. To do the filtering you will have to call
            :meth:`filter_commands` yourself.

        Parameters
        -----------
        cog: :class:`Cog`
            The cog that was requested for help.
        """
        pass

    async def send_group_help(self, group):
        """|coro|

        Handles the implementation of the group page in the help command.
        This function is called when the help command is called with a group as the argument.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method. Well behaved subclasses
        should use :meth:`get_destination` to know where to send, as this is a customisation
        point for other users.

        You can override this method to customise the behaviour.

        .. note::

            You can access the invocation context with :attr:`HelpCommand.context`.

            To get the commands that belong to this group without aliases see
            :attr:`Group.commands`. The commands returned not filtered. To do the
            filtering you will have to call :meth:`filter_commands` yourself.

        Parameters
        -----------
        group: :class:`Group`
            The group that was requested for help.
        """
        pass

    async def send_command_help(self, command):
        """|coro|

        Handles the implementation of the single command page in the help command.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method. Well behaved subclasses
        should use :meth:`get_destination` to know where to send, as this is a customisation
        point for other users.

        You can override this method to customise the behaviour.

        .. note::

            You can access the invocation context with :attr:`HelpCommand.context`.

        .. admonition:: Showing Help
            :class: helpful

            There are certain attributes and methods that are helpful for a help command
            to show such as the following:

            - :attr:`Command.help`
            - :attr:`Command.brief`
            - :attr:`Command.short_doc`
            - :attr:`Command.description`
            - :meth:`get_command_signature`

            There are more than just these attributes but feel free to play around with
            these to help you get started to get the output that you want.

        Parameters
        -----------
        command: :class:`Command`
            The command that was requested for help.
        """
        pass

    async def prepare_help_command(self, ctx, command=None):
        """|coro|

        A low level method that can be used to prepare the help command
        before it does anything. For example, if you need to prepare
        some state in your subclass before the command does its processing
        then this would be the place to do it.

        The default implementation does nothing.

        .. note::

            This is called *inside* the help command callback body. So all
            the usual rules that happen inside apply here as well.

        Parameters
        -----------
        ctx: :class:`Context`
            The invocation context.
        command: Optional[:class:`str`]
            The argument passed to the help command.
        """
        pass

    async def command_callback--- This code section failed: ---

 L. 778         0  LOAD_FAST                'self'
                2  LOAD_METHOD              prepare_help_command
                4  LOAD_FAST                'ctx'
                6  LOAD_FAST                'command'
                8  CALL_METHOD_2         2  ''
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  POP_TOP          

 L. 779        18  LOAD_FAST                'ctx'
               20  LOAD_ATTR                bot
               22  STORE_FAST               'bot'

 L. 781        24  LOAD_FAST                'command'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 782        32  LOAD_FAST                'self'
               34  LOAD_METHOD              get_bot_mapping
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'mapping'

 L. 783        40  LOAD_FAST                'self'
               42  LOAD_METHOD              send_bot_help
               44  LOAD_FAST                'mapping'
               46  CALL_METHOD_1         1  ''
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  RETURN_VALUE     
             56_0  COME_FROM            30  '30'

 L. 786        56  LOAD_FAST                'bot'
               58  LOAD_METHOD              get_cog
               60  LOAD_FAST                'command'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'cog'

 L. 787        66  LOAD_FAST                'cog'
               68  LOAD_CONST               None
               70  COMPARE_OP               is-not
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 788        74  LOAD_FAST                'self'
               76  LOAD_METHOD              send_cog_help
               78  LOAD_FAST                'cog'
               80  CALL_METHOD_1         1  ''
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  RETURN_VALUE     
             90_0  COME_FROM            72  '72'

 L. 790        90  LOAD_GLOBAL              discord
               92  LOAD_ATTR                utils
               94  LOAD_ATTR                maybe_coroutine
               96  STORE_FAST               'maybe_coro'

 L. 796        98  LOAD_FAST                'command'
              100  LOAD_METHOD              split
              102  LOAD_STR                 ' '
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'keys'

 L. 797       108  LOAD_FAST                'bot'
              110  LOAD_ATTR                all_commands
              112  LOAD_METHOD              get
              114  LOAD_FAST                'keys'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'cmd'

 L. 798       124  LOAD_FAST                'cmd'
              126  LOAD_CONST               None
              128  COMPARE_OP               is
              130  POP_JUMP_IF_FALSE   176  'to 176'

 L. 799       132  LOAD_FAST                'maybe_coro'
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                command_not_found
              138  LOAD_FAST                'self'
              140  LOAD_METHOD              remove_mentions
              142  LOAD_FAST                'keys'
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  CALL_METHOD_1         1  ''
              150  CALL_FUNCTION_2       2  ''
              152  GET_AWAITABLE    
              154  LOAD_CONST               None
              156  YIELD_FROM       
              158  STORE_FAST               'string'

 L. 800       160  LOAD_FAST                'self'
              162  LOAD_METHOD              send_error_message
              164  LOAD_FAST                'string'
              166  CALL_METHOD_1         1  ''
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  RETURN_VALUE     
            176_0  COME_FROM           130  '130'

 L. 802       176  LOAD_FAST                'keys'
              178  LOAD_CONST               1
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  BINARY_SUBSCR    
              186  GET_ITER         
              188  FOR_ITER            340  'to 340'
              190  STORE_FAST               'key'

 L. 803       192  SETUP_FINALLY       210  'to 210'

 L. 804       194  LOAD_FAST                'cmd'
              196  LOAD_ATTR                all_commands
              198  LOAD_METHOD              get
              200  LOAD_FAST                'key'
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'found'
              206  POP_BLOCK        
              208  JUMP_FORWARD        278  'to 278'
            210_0  COME_FROM_FINALLY   192  '192'

 L. 805       210  DUP_TOP          
              212  LOAD_GLOBAL              AttributeError
              214  COMPARE_OP               exception-match
          216_218  POP_JUMP_IF_FALSE   276  'to 276'
              220  POP_TOP          
              222  POP_TOP          
              224  POP_TOP          

 L. 806       226  LOAD_FAST                'maybe_coro'
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                subcommand_not_found
              232  LOAD_FAST                'cmd'
              234  LOAD_FAST                'self'
              236  LOAD_METHOD              remove_mentions
              238  LOAD_FAST                'key'
              240  CALL_METHOD_1         1  ''
              242  CALL_FUNCTION_3       3  ''
              244  GET_AWAITABLE    
              246  LOAD_CONST               None
              248  YIELD_FROM       
              250  STORE_FAST               'string'

 L. 807       252  LOAD_FAST                'self'
              254  LOAD_METHOD              send_error_message
              256  LOAD_FAST                'string'
              258  CALL_METHOD_1         1  ''
              260  GET_AWAITABLE    
              262  LOAD_CONST               None
              264  YIELD_FROM       
              266  ROT_FOUR         
              268  POP_EXCEPT       
              270  ROT_TWO          
              272  POP_TOP          
              274  RETURN_VALUE     
            276_0  COME_FROM           216  '216'
              276  END_FINALLY      
            278_0  COME_FROM           208  '208'

 L. 809       278  LOAD_FAST                'found'
              280  LOAD_CONST               None
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_FALSE   334  'to 334'

 L. 810       288  LOAD_FAST                'maybe_coro'
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                subcommand_not_found
              294  LOAD_FAST                'cmd'
              296  LOAD_FAST                'self'
              298  LOAD_METHOD              remove_mentions
              300  LOAD_FAST                'key'
              302  CALL_METHOD_1         1  ''
              304  CALL_FUNCTION_3       3  ''
              306  GET_AWAITABLE    
              308  LOAD_CONST               None
              310  YIELD_FROM       
              312  STORE_FAST               'string'

 L. 811       314  LOAD_FAST                'self'
              316  LOAD_METHOD              send_error_message
              318  LOAD_FAST                'string'
              320  CALL_METHOD_1         1  ''
              322  GET_AWAITABLE    
              324  LOAD_CONST               None
              326  YIELD_FROM       
              328  ROT_TWO          
              330  POP_TOP          
              332  RETURN_VALUE     
            334_0  COME_FROM           284  '284'

 L. 812       334  LOAD_FAST                'found'
              336  STORE_FAST               'cmd'
              338  JUMP_BACK           188  'to 188'

 L. 814       340  LOAD_GLOBAL              isinstance
              342  LOAD_FAST                'cmd'
              344  LOAD_GLOBAL              Group
              346  CALL_FUNCTION_2       2  ''
          348_350  POP_JUMP_IF_FALSE   368  'to 368'

 L. 815       352  LOAD_FAST                'self'
              354  LOAD_METHOD              send_group_help
              356  LOAD_FAST                'cmd'
              358  CALL_METHOD_1         1  ''
              360  GET_AWAITABLE    
              362  LOAD_CONST               None
              364  YIELD_FROM       
              366  RETURN_VALUE     
            368_0  COME_FROM           348  '348'

 L. 817       368  LOAD_FAST                'self'
              370  LOAD_METHOD              send_command_help
              372  LOAD_FAST                'cmd'
              374  CALL_METHOD_1         1  ''
              376  GET_AWAITABLE    
              378  LOAD_CONST               None
              380  YIELD_FROM       
              382  RETURN_VALUE     

Parse error at or near `ROT_TWO' instruction at offset 270


class DefaultHelpCommand(HelpCommand):
    __doc__ = 'The implementation of the default help command.\n\n    This inherits from :class:`HelpCommand`.\n\n    It extends it with the following attributes.\n\n    Attributes\n    ------------\n    width: :class:`int`\n        The maximum number of characters that fit in a line.\n        Defaults to 80.\n    sort_commands: :class:`bool`\n        Whether to sort the commands in the output alphabetically. Defaults to ``True``.\n    dm_help: Optional[:class:`bool`]\n        A tribool that indicates if the help command should DM the user instead of\n        sending it to the channel it received it from. If the boolean is set to\n        ``True``, then all help output is DM\'d. If ``False``, none of the help\n        output is DM\'d. If ``None``, then the bot will only DM when the help\n        message becomes too long (dictated by more than :attr:`dm_help_threshold` characters).\n        Defaults to ``False``.\n    dm_help_threshold: Optional[:class:`int`]\n        The number of characters the paginator must accumulate before getting DM\'d to the\n        user if :attr:`dm_help` is set to ``None``. Defaults to 1000.\n    indent: :class:`int`\n        How much to indent the commands from a heading. Defaults to ``2``.\n    commands_heading: :class:`str`\n        The command list\'s heading string used when the help command is invoked with a category name.\n        Useful for i18n. Defaults to ``"Commands:"``\n    no_category: :class:`str`\n        The string used when there is a command which does not belong to any category(cog).\n        Useful for i18n. Defaults to ``"No Category"``\n    paginator: :class:`Paginator`\n        The paginator used to paginate the help command output.\n    '

    def __init__(self, **options):
        self.width = options.pop('width', 80)
        self.indent = options.pop('indent', 2)
        self.sort_commands = options.pop('sort_commands', True)
        self.dm_help = options.pop('dm_help', False)
        self.dm_help_threshold = options.pop('dm_help_threshold', 1000)
        self.commands_heading = options.pop('commands_heading', 'Commands:')
        self.no_category = options.pop('no_category', 'No Category')
        self.paginator = options.pop('paginator', None)
        if self.paginator is None:
            self.paginator = Paginator()
        (super().__init__)(**options)

    def shorten_text(self, text):
        """Shortens text to fit into the :attr:`width`."""
        if len(text) > self.width:
            return text[:self.width - 3] + '...'
        return text

    def get_ending_note(self):
        """Returns help command's ending note. This is mainly useful to override for i18n purposes."""
        command_name = self.invoked_with
        return 'Type {0}{1} command for more info on a command.\nYou can also type {0}{1} category for more info on a category.'.format(self.clean_prefix, command_name)

    def add_indented_commands(self, commands, *, heading, max_size=None):
        """Indents a list of commands after the specified heading.

        The formatting is added to the :attr:`paginator`.

        The default implementation is the command name indented by
        :attr:`indent` spaces, padded to ``max_size`` followed by
        the command's :attr:`Command.short_doc` and then shortened
        to fit into the :attr:`width`.

        Parameters
        -----------
        commands: Sequence[:class:`Command`]
            A list of commands to indent for output.
        heading: :class:`str`
            The heading to add to the output. This is only added
            if the list of commands is greater than 0.
        max_size: Optional[:class:`int`]
            The max size to use for the gap between indents.
            If unspecified, calls :meth:`get_max_size` on the
            commands parameter.
        """
        if not commands:
            return
        self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)
        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = '{0}{1:<{width}} {2}'.format((self.indent * ' '), name, (command.short_doc), width=width)
            self.paginator.add_line(self.shorten_text(entry))

    async def send_pages(self):
        """A helper utility to send the page output from :attr:`paginator` to the destination."""
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)

    def add_command_formatting(self, command):
        """A utility function to format the non-indented block of commands and groups.

        Parameters
        ------------
        command: :class:`Command`
            The command to format.
        """
        if command.description:
            self.paginator.add_line((command.description), empty=True)
        signature = self.get_command_signature(command)
        self.paginator.add_line(signature, empty=True)
        if command.help:
            try:
                self.paginator.add_line((command.help), empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                else:
                    self.paginator.add_line()

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        if self.dm_help is None:
            if len(self.paginator) > self.dm_help_threshold:
                return ctx.author
        return ctx.channel

    async def prepare_help_command(self, ctx, command):
        self.paginator.clear()
        await super().prepare_help_command(ctx, command)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        if bot.description:
            self.paginator.add_line((bot.description), empty=True)
        no_category = '\u200b{0.no_category}:'.format(self)

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            if cog is not None:
                return cog.qualified_name + ':'
            return no_category

        filtered = await self.filter_commands((bot.commands), sort=True, key=get_category)
        max_size = self.get_max_size(filtered)
        to_iterate = itertools.groupby(filtered, key=get_category)
        for category, commands in to_iterate:
            commands = sorted(commands, key=(lambda c: c.name)) if self.sort_commands else list(commands)
            self.add_indented_commands(commands, heading=category, max_size=max_size)
        else:
            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)
            await self.send_pages()

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()

    async def send_group_help(self, group):
        self.add_command_formatting(group)
        filtered = await self.filter_commands((group.commands), sort=(self.sort_commands))
        self.add_indented_commands(filtered, heading=(self.commands_heading))
        if filtered:
            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)
        await self.send_pages()

    async def send_cog_help(self, cog):
        if cog.description:
            self.paginator.add_line((cog.description), empty=True)
        filtered = await self.filter_commands((cog.get_commands()), sort=(self.sort_commands))
        self.add_indented_commands(filtered, heading=(self.commands_heading))
        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)
        await self.send_pages()


class MinimalHelpCommand(HelpCommand):
    __doc__ = 'An implementation of a help command with minimal output.\n\n    This inherits from :class:`HelpCommand`.\n\n    Attributes\n    ------------\n    sort_commands: :class:`bool`\n        Whether to sort the commands in the output alphabetically. Defaults to ``True``.\n    commands_heading: :class:`str`\n        The command list\'s heading string used when the help command is invoked with a category name.\n        Useful for i18n. Defaults to ``"Commands"``\n    aliases_heading: :class:`str`\n        The alias list\'s heading string used to list the aliases of the command. Useful for i18n.\n        Defaults to ``"Aliases:"``.\n    dm_help: Optional[:class:`bool`]\n        A tribool that indicates if the help command should DM the user instead of\n        sending it to the channel it received it from. If the boolean is set to\n        ``True``, then all help output is DM\'d. If ``False``, none of the help\n        output is DM\'d. If ``None``, then the bot will only DM when the help\n        message becomes too long (dictated by more than :attr:`dm_help_threshold` characters).\n        Defaults to ``False``.\n    dm_help_threshold: Optional[:class:`int`]\n        The number of characters the paginator must accumulate before getting DM\'d to the\n        user if :attr:`dm_help` is set to ``None``. Defaults to 1000.\n    no_category: :class:`str`\n        The string used when there is a command which does not belong to any category(cog).\n        Useful for i18n. Defaults to ``"No Category"``\n    paginator: :class:`Paginator`\n        The paginator used to paginate the help command output.\n    '

    def __init__(self, **options):
        self.sort_commands = options.pop('sort_commands', True)
        self.commands_heading = options.pop('commands_heading', 'Commands')
        self.dm_help = options.pop('dm_help', False)
        self.dm_help_threshold = options.pop('dm_help_threshold', 1000)
        self.aliases_heading = options.pop('aliases_heading', 'Aliases:')
        self.no_category = options.pop('no_category', 'No Category')
        self.paginator = options.pop('paginator', None)
        if self.paginator is None:
            self.paginator = Paginator(suffix=None, prefix=None)
        (super().__init__)(**options)

    async def send_pages(self):
        """A helper utility to send the page output from :attr:`paginator` to the destination."""
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)

    def get_opening_note(self):
        """Returns help command's opening note. This is mainly useful to override for i18n purposes.

        The default implementation returns ::

            Use `{prefix}{command_name} [command]` for more info on a command.
            You can also use `{prefix}{command_name} [category]` for more info on a category.

        """
        command_name = self.invoked_with
        return 'Use `{0}{1} [command]` for more info on a command.\nYou can also use `{0}{1} [category]` for more info on a category.'.format(self.clean_prefix, command_name)

    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    def get_ending_note(self):
        """Return the help command's ending note. This is mainly useful to override for i18n purposes.

        The default implementation does nothing.
        """
        pass

    def add_bot_commands_formatting(self, commands, heading):
        """Adds the minified bot heading with commands to the output.

        The formatting should be added to the :attr:`paginator`.

        The default implementation is a bold underline heading followed
        by commands separated by an EN SPACE (U+2002) in the next line.

        Parameters
        -----------
        commands: Sequence[:class:`Command`]
            A list of commands that belong to the heading.
        heading: :class:`str`
            The heading to add to the line.
        """
        if commands:
            joined = '\u2002'.join((c.name for c in commands))
            self.paginator.add_line('__**%s**__' % heading)
            self.paginator.add_line(joined)

    def add_subcommand_formatting(self, command):
        """Adds formatting information on a subcommand.

        The formatting should be added to the :attr:`paginator`.

        The default implementation is the prefix and the :attr:`Command.qualified_name`
        optionally followed by an En dash and the command's :attr:`Command.short_doc`.

        Parameters
        -----------
        command: :class:`Command`
            The command to show information of.
        """
        fmt = '{0}{1} – {2}' if command.short_doc else '{0}{1}'
        self.paginator.add_line(fmt.format(self.clean_prefix, command.qualified_name, command.short_doc))

    def add_aliases_formatting(self, aliases):
        """Adds the formatting information on a command's aliases.

        The formatting should be added to the :attr:`paginator`.

        The default implementation is the :attr:`aliases_heading` bolded
        followed by a comma separated list of aliases.

        This is not called if there are no aliases to format.

        Parameters
        -----------
        aliases: Sequence[:class:`str`]
            A list of aliases to format.
        """
        self.paginator.add_line(('**%s** %s' % (self.aliases_heading, ', '.join(aliases))), empty=True)

    def add_command_formatting(self, command):
        """A utility function to format commands and groups.

        Parameters
        ------------
        command: :class:`Command`
            The command to format.
        """
        if command.description:
            self.paginator.add_line((command.description), empty=True)
        else:
            signature = self.get_command_signature(command)
            if command.aliases:
                self.paginator.add_line(signature)
                self.add_aliases_formatting(command.aliases)
            else:
                self.paginator.add_line(signature, empty=True)
        if command.help:
            try:
                self.paginator.add_line((command.help), empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                else:
                    self.paginator.add_line()

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        if self.dm_help is None:
            if len(self.paginator) > self.dm_help_threshold:
                return ctx.author
        return ctx.channel

    async def prepare_help_command(self, ctx, command):
        self.paginator.clear()
        await super().prepare_help_command(ctx, command)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        if bot.description:
            self.paginator.add_line((bot.description), empty=True)
        note = self.get_opening_note()
        if note:
            self.paginator.add_line(note, empty=True)
        no_category = '\u200b{0.no_category}'.format(self)

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            if cog is not None:
                return cog.qualified_name
            return no_category

        filtered = await self.filter_commands((bot.commands), sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)
        for category, commands in to_iterate:
            commands = sorted(commands, key=(lambda c: c.name)) if self.sort_commands else list(commands)
            self.add_bot_commands_formatting(commands, category)
        else:
            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)
            await self.send_pages()

    async def send_cog_help(self, cog):
        bot = self.context.bot
        if bot.description:
            self.paginator.add_line((bot.description), empty=True)
        note = self.get_opening_note()
        if note:
            self.paginator.add_line(note, empty=True)
        if cog.description:
            self.paginator.add_line((cog.description), empty=True)
        filtered = await self.filter_commands((cog.get_commands()), sort=(self.sort_commands))
        if filtered:
            self.paginator.add_line('**%s %s**' % (cog.qualified_name, self.commands_heading))
            for command in filtered:
                self.add_subcommand_formatting(command)
            else:
                note = self.get_ending_note()
                if note:
                    self.paginator.add_line()
                    self.paginator.add_line(note)

        await self.send_pages()

    async def send_group_help(self, group):
        self.add_command_formatting(group)
        filtered = await self.filter_commands((group.commands), sort=(self.sort_commands))
        if filtered:
            note = self.get_opening_note()
            if note:
                self.paginator.add_line(note, empty=True)
            self.paginator.add_line('**%s**' % self.commands_heading)
            for command in filtered:
                self.add_subcommand_formatting(command)
            else:
                note = self.get_ending_note()
                if note:
                    self.paginator.add_line()
                    self.paginator.add_line(note)

        await self.send_pages()

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()