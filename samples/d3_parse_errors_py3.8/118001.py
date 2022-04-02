# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\core.py
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
import asyncio, functools, inspect, typing, datetime, discord
from .errors import *
from .cooldowns import Cooldown, BucketType, CooldownMapping, MaxConcurrency
from . import converter as converters
from ._types import _BaseCommand
from .cog import Cog
__all__ = ('Command', 'Group', 'GroupMixin', 'command', 'group', 'has_role', 'has_permissions',
           'has_any_role', 'check', 'check_any', 'bot_has_role', 'bot_has_permissions',
           'bot_has_any_role', 'cooldown', 'max_concurrency', 'dm_only', 'guild_only',
           'is_owner', 'is_nsfw', 'has_guild_permissions', 'bot_has_guild_permissions')

def wrap_callback(coro):

    @functools.wraps(coro)
    async def wrapped(*args, **kwargs):
        try:
            ret = await coro(*args, **kwargs)
        except CommandError:
            raise
        except asyncio.CancelledError:
            return
        except Exception as exc:
            try:
                raise CommandInvokeError(exc) from exc
            finally:
                exc = None
                del exc

        else:
            return ret

    return wrapped


def hooked_wrapped_callback(command, ctx, coro):

    @functools.wraps(coro)
    async def wrapped--- This code section failed: ---

 L.  82         0  SETUP_FINALLY       136  'to 136'
                2  SETUP_FINALLY        24  'to 24'

 L.  83         4  LOAD_DEREF               'coro'
                6  LOAD_FAST                'args'
                8  LOAD_FAST                'kwargs'
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  STORE_FAST               'ret'
               20  POP_BLOCK        
               22  JUMP_FORWARD        132  'to 132'
             24_0  COME_FROM_FINALLY     2  '2'

 L.  84        24  DUP_TOP          
               26  LOAD_GLOBAL              CommandError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    50  'to 50'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  85        38  LOAD_CONST               True
               40  LOAD_DEREF               'ctx'
               42  STORE_ATTR               command_failed

 L.  86        44  RAISE_VARARGS_0       0  'reraise'
               46  POP_EXCEPT       
               48  JUMP_FORWARD        132  'to 132'
             50_0  COME_FROM            30  '30'

 L.  87        50  DUP_TOP          
               52  LOAD_GLOBAL              asyncio
               54  LOAD_ATTR                CancelledError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    82  'to 82'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  88        66  LOAD_CONST               True
               68  LOAD_DEREF               'ctx'
               70  STORE_ATTR               command_failed

 L.  89        72  POP_EXCEPT       
               74  POP_BLOCK        
               76  CALL_FINALLY        136  'to 136'
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            58  '58'

 L.  90        82  DUP_TOP          
               84  LOAD_GLOBAL              Exception
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   130  'to 130'
               90  POP_TOP          
               92  STORE_FAST               'exc'
               94  POP_TOP          
               96  SETUP_FINALLY       118  'to 118'

 L.  91        98  LOAD_CONST               True
              100  LOAD_DEREF               'ctx'
              102  STORE_ATTR               command_failed

 L.  92       104  LOAD_GLOBAL              CommandInvokeError
              106  LOAD_FAST                'exc'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'exc'
              112  RAISE_VARARGS_2       2  'exception instance with __cause__'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY    96  '96'
              118  LOAD_CONST               None
              120  STORE_FAST               'exc'
              122  DELETE_FAST              'exc'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM            88  '88'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            48  '48'
            132_2  COME_FROM            22  '22'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM            76  '76'
            136_1  COME_FROM_FINALLY     0  '0'

 L.  94       136  LOAD_DEREF               'command'
              138  LOAD_ATTR                _max_concurrency
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L.  95       146  LOAD_DEREF               'command'
              148  LOAD_ATTR                _max_concurrency
              150  LOAD_METHOD              release
              152  LOAD_DEREF               'ctx'
              154  CALL_METHOD_1         1  ''
              156  GET_AWAITABLE    
              158  LOAD_CONST               None
              160  YIELD_FROM       
              162  POP_TOP          
            164_0  COME_FROM           144  '144'

 L.  97       164  LOAD_DEREF               'command'
              166  LOAD_METHOD              call_after_hooks
              168  LOAD_DEREF               'ctx'
              170  CALL_METHOD_1         1  ''
              172  GET_AWAITABLE    
              174  LOAD_CONST               None
              176  YIELD_FROM       
              178  POP_TOP          
              180  END_FINALLY      

 L.  98       182  LOAD_FAST                'ret'
              184  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 74

    return wrapped


def _convert_to_bool(argument):
    lowered = argument.lower()
    if lowered in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
        return True
    if lowered in ('no', 'n', 'false', 'f', '0', 'disable', 'off'):
        return False
    raise BadArgument(lowered + ' is not a recognised boolean option')


class _CaseInsensitiveDict(dict):

    def __contains__(self, k):
        return super().__contains__(k.casefold())

    def __delitem__(self, k):
        return super().__delitem__(k.casefold())

    def __getitem__(self, k):
        return super().__getitem__(k.casefold())

    def get(self, k, default=None):
        return super().get(k.casefold(), default)

    def pop(self, k, default=None):
        return super().pop(k.casefold(), default)

    def __setitem__(self, k, v):
        super().__setitem__(k.casefold(), v)


class Command(_BaseCommand):
    __doc__ = "A class that implements the protocol for a bot text command.\n\n    These are not created manually, instead they are created via the\n    decorator or functional interface.\n\n    Attributes\n    -----------\n    name: :class:`str`\n        The name of the command.\n    callback: :ref:`coroutine <coroutine>`\n        The coroutine that is executed when the command is called.\n    help: :class:`str`\n        The long help text for the command.\n    brief: :class:`str`\n        The short help text for the command. If this is not specified\n        then the first line of the long help text is used instead.\n    usage: :class:`str`\n        A replacement for arguments in the default help text.\n    aliases: :class:`list`\n        The list of aliases the command can be invoked under.\n    enabled: :class:`bool`\n        A boolean that indicates if the command is currently enabled.\n        If the command is invoked while it is disabled, then\n        :exc:`.DisabledCommand` is raised to the :func:`.on_command_error`\n        event. Defaults to ``True``.\n    parent: Optional[:class:`Command`]\n        The parent command that this command belongs to. ``None`` if there\n        isn't one.\n    cog: Optional[:class:`Cog`]\n        The cog that this command belongs to. ``None`` if there isn't one.\n    checks: List[Callable[..., :class:`bool`]]\n        A list of predicates that verifies if the command could be executed\n        with the given :class:`.Context` as the sole parameter. If an exception\n        is necessary to be thrown to signal failure, then one inherited from\n        :exc:`.CommandError` should be used. Note that if the checks fail then\n        :exc:`.CheckFailure` exception is raised to the :func:`.on_command_error`\n        event.\n    description: :class:`str`\n        The message prefixed into the default help command.\n    hidden: :class:`bool`\n        If ``True``\\, the default help command does not show this in the\n        help output.\n    rest_is_raw: :class:`bool`\n        If ``False`` and a keyword-only argument is provided then the keyword\n        only argument is stripped and handled as if it was a regular argument\n        that handles :exc:`.MissingRequiredArgument` and default values in a\n        regular matter rather than passing the rest completely raw. If ``True``\n        then the keyword-only argument will pass in the rest of the arguments\n        in a completely raw matter. Defaults to ``False``.\n    invoked_subcommand: Optional[:class:`Command`]\n        The subcommand that was invoked, if any.\n    ignore_extra: :class:`bool`\n        If ``True``\\, ignores extraneous strings passed to a command if all its\n        requirements are met (e.g. ``?foo a b c`` when only expecting ``a``\n        and ``b``). Otherwise :func:`.on_command_error` and local error handlers\n        are called with :exc:`.TooManyArguments`. Defaults to ``True``.\n    cooldown_after_parsing: :class:`bool`\n        If ``True``\\, cooldown processing is done after argument parsing,\n        which calls converters. If ``False`` then cooldown processing is done\n        first and then the converters are called second. Defaults to ``False``.\n    "

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.__original_kwargs__ = kwargs.copy()
        return self

    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')
        self.name = name = kwargs.get('name') or func.__name__
        if not isinstance(name, str):
            raise TypeError('Name of a command must be a string.')
        self.callback = func
        self.enabled = kwargs.get('enabled', True)
        help_doc = kwargs.get('help')
        if help_doc is not None:
            help_doc = inspect.cleandoc(help_doc)
        else:
            help_doc = inspect.getdoc(func)
            if isinstance(help_doc, bytes):
                help_doc = help_doc.decode('utf-8')
        self.help = help_doc
        self.brief = kwargs.get('brief')
        self.usage = kwargs.get('usage')
        self.rest_is_raw = kwargs.get('rest_is_raw', False)
        self.aliases = kwargs.get('aliases', [])
        if not isinstance(self.aliases, (list, tuple)):
            raise TypeError('Aliases of a command must be a list of strings.')
        self.description = inspect.cleandoc(kwargs.get('description', ''))
        self.hidden = kwargs.get('hidden', False)
        try:
            try:
                checks = func.__commands_checks__
                checks.reverse()
            except AttributeError:
                checks = kwargs.get('checks', [])

        finally:
            self.checks = checks

        try:
            try:
                cooldown = func.__commands_cooldown__
            except AttributeError:
                cooldown = kwargs.get('cooldown')

        finally:
            self._buckets = CooldownMapping(cooldown)

        try:
            try:
                max_concurrency = func.__commands_max_concurrency__
            except AttributeError:
                max_concurrency = kwargs.get('max_concurrency')

        finally:
            self._max_concurrency = max_concurrency

        self.ignore_extra = kwargs.get('ignore_extra', True)
        self.cooldown_after_parsing = kwargs.get('cooldown_after_parsing', False)
        self.cog = None
        parent = kwargs.get('parent')
        self.parent = parent if isinstance(parent, _BaseCommand) else None
        self._before_invoke = None
        self._after_invoke = None

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, function):
        self._callback = function
        self.module = function.__module__
        signature = inspect.signature(function)
        self.params = signature.parameters.copy()
        for key, value in self.params.items():
            if isinstance(value.annotation, str):
                self.params[key] = value = value.replace(annotation=(eval(value.annotation, function.__globals__)))
            if value.annotation is converters.Greedy:
                raise TypeError('Unparameterized Greedy[...] is disallowed in signature.')

    def add_check(self, func):
        """Adds a check to the command.

        This is the non-decorator interface to :func:`.check`.

        .. versionadded:: 1.3

        Parameters
        -----------
        func
            The function that will be used as a check.
        """
        self.checks.append(func)

    def remove_check(self, func):
        """Removes a check from the command.

        This function is idempotent and will not raise an exception
        if the function is not in the command's checks.

        .. versionadded:: 1.3

        Parameters
        -----------
        func
            The function to remove from the checks.
        """
        try:
            self.checks.remove(func)
        except ValueError:
            pass

    def update(self, **kwargs):
        """Updates :class:`Command` instance with updated attribute.

        This works similarly to the :func:`.command` decorator in terms
        of parameters in that they are passed to the :class:`Command` or
        subclass constructors, sans the name and callback.
        """
        (self.__init__)((self.callback), **)

    async def __call__(self, *args, **kwargs):
        """|coro|

        Calls the internal callback that the command holds.

        .. note::

            This bypasses all mechanisms -- including checks, converters,
            invoke hooks, cooldowns, etc. You must take care to pass
            the proper arguments and types to this function.

        .. versionadded:: 1.3
        """
        if self.cog is not None:
            return await (self.callback)(self.cog, *args, **kwargs)
        return await (self.callback)(*args, **kwargs)

    def _ensure_assignment_on_copy(self, other):
        other._before_invoke = self._before_invoke
        other._after_invoke = self._after_invoke
        if self.checks != other.checks:
            other.checks = self.checks.copy()
        if self._buckets.valid:
            if not other._buckets.valid:
                other._buckets = self._buckets.copy()
            if self._max_concurrency != other._max_concurrency:
                other._max_concurrency = self._max_concurrency.copy()
        try:
            other.on_error = self.on_error
        except AttributeError:
            pass
        else:
            return other

    def copy(self):
        """Creates a copy of this command."""
        ret = (self.__class__)((self.callback), **self.__original_kwargs__)
        return self._ensure_assignment_on_copy(ret)

    def _update_copy(self, kwargs):
        if kwargs:
            kw = kwargs.copy()
            kw.update(self.__original_kwargs__)
            copy = (self.__class__)((self.callback), **kw)
            return self._ensure_assignment_on_copy(copy)
        return self.copy()

    async def dispatch_error(self, ctx, error):
        ctx.command_failed = True
        cog = self.cog
        try:
            coro = self.on_error
        except AttributeError:
            pass
        else:
            injected = wrap_callback(coro)
            if cog is not None:
                await injected(cog, ctx, error)
            else:
                await injected(ctx, error)
        try:
            if cog is not None:
                local = Cog._get_overridden_method(cog.cog_command_error)
                if local is not None:
                    wrapped = wrap_callback(local)
                    await wrapped(ctx, error)
        finally:
            ctx.bot.dispatch('command_error', ctx, error)

    async def _actual_conversion--- This code section failed: ---

 L. 410         0  LOAD_FAST                'converter'
                2  LOAD_GLOBAL              bool
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 411         8  LOAD_GLOBAL              _convert_to_bool
               10  LOAD_FAST                'argument'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 413        16  SETUP_FINALLY        28  'to 28'

 L. 414        18  LOAD_FAST                'converter'
               20  LOAD_ATTR                __module__
               22  STORE_FAST               'module'
               24  POP_BLOCK        
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM_FINALLY    16  '16'

 L. 415        28  DUP_TOP          
               30  LOAD_GLOBAL              AttributeError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 416        42  POP_EXCEPT       
               44  JUMP_FORWARD         94  'to 94'
             46_0  COME_FROM            34  '34'
               46  END_FINALLY      
             48_0  COME_FROM            26  '26'

 L. 418        48  LOAD_FAST                'module'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE    94  'to 94'
               56  LOAD_FAST                'module'
               58  LOAD_METHOD              startswith
               60  LOAD_STR                 'discord.'
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_FALSE    94  'to 94'
               66  LOAD_FAST                'module'
               68  LOAD_METHOD              endswith
               70  LOAD_STR                 'converter'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_TRUE     94  'to 94'

 L. 419        76  LOAD_GLOBAL              getattr
               78  LOAD_GLOBAL              converters
               80  LOAD_FAST                'converter'
               82  LOAD_ATTR                __name__
               84  LOAD_STR                 'Converter'
               86  BINARY_ADD       
               88  LOAD_FAST                'converter'
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'converter'
             94_0  COME_FROM            74  '74'
             94_1  COME_FROM            64  '64'
             94_2  COME_FROM            54  '54'
             94_3  COME_FROM            44  '44'

 L. 421        94  SETUP_FINALLY       242  'to 242'

 L. 422        96  LOAD_GLOBAL              inspect
               98  LOAD_METHOD              isclass
              100  LOAD_FAST                'converter'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   202  'to 202'

 L. 423       106  LOAD_GLOBAL              issubclass
              108  LOAD_FAST                'converter'
              110  LOAD_GLOBAL              converters
              112  LOAD_ATTR                Converter
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   148  'to 148'

 L. 424       118  LOAD_FAST                'converter'
              120  CALL_FUNCTION_0       0  ''
              122  STORE_FAST               'instance'

 L. 425       124  LOAD_FAST                'instance'
              126  LOAD_METHOD              convert
              128  LOAD_FAST                'ctx'
              130  LOAD_FAST                'argument'
              132  CALL_METHOD_2         2  ''
              134  GET_AWAITABLE    
              136  LOAD_CONST               None
              138  YIELD_FROM       
              140  STORE_FAST               'ret'

 L. 426       142  LOAD_FAST                'ret'
              144  POP_BLOCK        
              146  RETURN_VALUE     
            148_0  COME_FROM           116  '116'

 L. 428       148  LOAD_GLOBAL              getattr
              150  LOAD_FAST                'converter'
              152  LOAD_STR                 'convert'
              154  LOAD_CONST               None
              156  CALL_FUNCTION_3       3  ''
              158  STORE_FAST               'method'

 L. 429       160  LOAD_FAST                'method'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   238  'to 238'
              168  LOAD_GLOBAL              inspect
              170  LOAD_METHOD              ismethod
              172  LOAD_FAST                'method'
              174  CALL_METHOD_1         1  ''
              176  POP_JUMP_IF_FALSE   238  'to 238'

 L. 430       178  LOAD_FAST                'method'
              180  LOAD_FAST                'ctx'
              182  LOAD_FAST                'argument'
              184  CALL_FUNCTION_2       2  ''
              186  GET_AWAITABLE    
              188  LOAD_CONST               None
              190  YIELD_FROM       
              192  STORE_FAST               'ret'

 L. 431       194  LOAD_FAST                'ret'
              196  POP_BLOCK        
              198  RETURN_VALUE     
              200  JUMP_FORWARD        238  'to 238'
            202_0  COME_FROM           104  '104'

 L. 432       202  LOAD_GLOBAL              isinstance
              204  LOAD_FAST                'converter'
              206  LOAD_GLOBAL              converters
              208  LOAD_ATTR                Converter
              210  CALL_FUNCTION_2       2  ''
              212  POP_JUMP_IF_FALSE   238  'to 238'

 L. 433       214  LOAD_FAST                'converter'
              216  LOAD_METHOD              convert
              218  LOAD_FAST                'ctx'
              220  LOAD_FAST                'argument'
              222  CALL_METHOD_2         2  ''
              224  GET_AWAITABLE    
              226  LOAD_CONST               None
              228  YIELD_FROM       
              230  STORE_FAST               'ret'

 L. 434       232  LOAD_FAST                'ret'
              234  POP_BLOCK        
              236  RETURN_VALUE     
            238_0  COME_FROM           212  '212'
            238_1  COME_FROM           200  '200'
            238_2  COME_FROM           176  '176'
            238_3  COME_FROM           166  '166'
              238  POP_BLOCK        
              240  JUMP_FORWARD        312  'to 312'
            242_0  COME_FROM_FINALLY    94  '94'

 L. 435       242  DUP_TOP          
              244  LOAD_GLOBAL              CommandError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   264  'to 264'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 436       258  RAISE_VARARGS_0       0  'reraise'
              260  POP_EXCEPT       
              262  JUMP_FORWARD        312  'to 312'
            264_0  COME_FROM           248  '248'

 L. 437       264  DUP_TOP          
              266  LOAD_GLOBAL              Exception
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   310  'to 310'
              274  POP_TOP          
              276  STORE_FAST               'exc'
              278  POP_TOP          
              280  SETUP_FINALLY       298  'to 298'

 L. 438       282  LOAD_GLOBAL              ConversionError
              284  LOAD_FAST                'converter'
              286  LOAD_FAST                'exc'
              288  CALL_FUNCTION_2       2  ''
              290  LOAD_FAST                'exc'
              292  RAISE_VARARGS_2       2  'exception instance with __cause__'
              294  POP_BLOCK        
              296  BEGIN_FINALLY    
            298_0  COME_FROM_FINALLY   280  '280'
              298  LOAD_CONST               None
              300  STORE_FAST               'exc'
              302  DELETE_FAST              'exc'
              304  END_FINALLY      
              306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           270  '270'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           262  '262'
            312_2  COME_FROM           240  '240'

 L. 440       312  SETUP_FINALLY       324  'to 324'

 L. 441       314  LOAD_FAST                'converter'
              316  LOAD_FAST                'argument'
              318  CALL_FUNCTION_1       1  ''
              320  POP_BLOCK        
              322  RETURN_VALUE     
            324_0  COME_FROM_FINALLY   312  '312'

 L. 442       324  DUP_TOP          
              326  LOAD_GLOBAL              CommandError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   346  'to 346'
              334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L. 443       340  RAISE_VARARGS_0       0  'reraise'
              342  POP_EXCEPT       
              344  JUMP_FORWARD        444  'to 444'
            346_0  COME_FROM           330  '330'

 L. 444       346  DUP_TOP          
              348  LOAD_GLOBAL              Exception
              350  COMPARE_OP               exception-match
          352_354  POP_JUMP_IF_FALSE   442  'to 442'
              356  POP_TOP          
              358  STORE_FAST               'exc'
              360  POP_TOP          
              362  SETUP_FINALLY       430  'to 430'

 L. 445       364  SETUP_FINALLY       376  'to 376'

 L. 446       366  LOAD_FAST                'converter'
              368  LOAD_ATTR                __name__
              370  STORE_FAST               'name'
              372  POP_BLOCK        
              374  JUMP_FORWARD        406  'to 406'
            376_0  COME_FROM_FINALLY   364  '364'

 L. 447       376  DUP_TOP          
              378  LOAD_GLOBAL              AttributeError
              380  COMPARE_OP               exception-match
          382_384  POP_JUMP_IF_FALSE   404  'to 404'
              386  POP_TOP          
              388  POP_TOP          
              390  POP_TOP          

 L. 448       392  LOAD_FAST                'converter'
              394  LOAD_ATTR                __class__
              396  LOAD_ATTR                __name__
              398  STORE_FAST               'name'
              400  POP_EXCEPT       
              402  JUMP_FORWARD        406  'to 406'
            404_0  COME_FROM           382  '382'
              404  END_FINALLY      
            406_0  COME_FROM           402  '402'
            406_1  COME_FROM           374  '374'

 L. 450       406  LOAD_GLOBAL              BadArgument
              408  LOAD_STR                 'Converting to "{}" failed for parameter "{}".'
              410  LOAD_METHOD              format
              412  LOAD_FAST                'name'
              414  LOAD_FAST                'param'
              416  LOAD_ATTR                name
              418  CALL_METHOD_2         2  ''
              420  CALL_FUNCTION_1       1  ''
              422  LOAD_FAST                'exc'
              424  RAISE_VARARGS_2       2  'exception instance with __cause__'
              426  POP_BLOCK        
              428  BEGIN_FINALLY    
            430_0  COME_FROM_FINALLY   362  '362'
              430  LOAD_CONST               None
              432  STORE_FAST               'exc'
              434  DELETE_FAST              'exc'
              436  END_FINALLY      
              438  POP_EXCEPT       
              440  JUMP_FORWARD        444  'to 444'
            442_0  COME_FROM           352  '352'
              442  END_FINALLY      
            444_0  COME_FROM           440  '440'
            444_1  COME_FROM           344  '344'

Parse error at or near `DUP_TOP' instruction at offset 346

    async def do_conversion(self, ctx, converter, argument, param):
        try:
            origin = converter.__origin__
        except AttributeError:
            pass
        else:
            if origin is typing.Union:
                errors = []
                _NoneType = type(None)
                for conv in converter.__args__:
                    if conv is _NoneType:
                        if param.kind != param.VAR_POSITIONAL:
                            ctx.view.undo()
                            return None if param.default is param.empty else param.default
                    try:
                        value = await self._actual_conversion(ctx, conv, argument, param)
                    except CommandError as exc:
                        try:
                            errors.append(exc)
                        finally:
                            exc = None
                            del exc

                    else:
                        return value
                else:
                    raise BadUnionArgument(param, converter.__args__, errors)

        return await self._actual_conversion(ctx, converter, argument, param)

    def _get_converter(self, param):
        converter = param.annotation
        if converter is param.empty:
            if param.default is not param.empty:
                converter = str if param.default is None else type(param.default)
            else:
                converter = str
        return converter

    async def transform(self, ctx, param):
        required = param.default is param.empty
        converter = self._get_converter(param)
        consume_rest_is_special = param.kind == param.KEYWORD_ONLY and not self.rest_is_raw
        view = ctx.view
        view.skip_ws()
        if type(converter) is converters._Greedy:
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                return await self._transform_greedy_pos(ctx, param, required, converter.converter)
            if param.kind == param.VAR_POSITIONAL:
                return await self._transform_greedy_var_pos(ctx, param, converter.converter)
            converter = converter.converter
        if view.eof:
            if param.kind == param.VAR_POSITIONAL:
                raise RuntimeError()
            if required:
                if self._is_typing_optional(param.annotation):
                    return
                raise MissingRequiredArgument(param)
            return param.default
        previous = view.index
        if consume_rest_is_special:
            argument = view.read_rest().strip()
        else:
            argument = view.get_quoted_word()
        view.previous = previous
        return await self.do_conversion(ctx, converter, argument, param)

    async def _transform_greedy_pos(self, ctx, param, required, converter):
        view = ctx.view
        result = []
        while True:
            if not view.eof:
                previous = view.index
                view.skip_ws()
                try:
                    argument = view.get_quoted_word()
                    value = await self.do_conversion(ctx, converter, argument, param)
                except (CommandError, ArgumentParsingError):
                    view.index = previous
                    break
                else:
                    result.append(value)

        if not result:
            if not required:
                return param.default
            return result

    async def _transform_greedy_var_pos(self, ctx, param, converter):
        view = ctx.view
        previous = view.index
        try:
            argument = view.get_quoted_word()
            value = await self.do_conversion(ctx, converter, argument, param)
        except (CommandError, ArgumentParsingError):
            view.index = previous
            raise RuntimeError() from None
        else:
            return value

    @property
    def clean_params(self):
        """Retrieves the parameter OrderedDict without the context or self parameters.

        Useful for inspecting signature.
        """
        result = self.params.copy()
        if self.cog is not None:
            result.popitem(last=False)
        try:
            result.popitem(last=False)
        except Exception:
            raise ValueError('Missing context parameter') from None
        else:
            return result

    @property
    def full_parent_name(self):
        """:class:`str`: Retrieves the fully qualified parent command name.

        This the base command name required to execute it. For example,
        in ``?one two three`` the parent name would be ``one two``.
        """
        entries = []
        command = self
        while True:
            if command.parent is not None:
                command = command.parent
                entries.append(command.name)

        return ' '.join(reversed(entries))

    @property
    def parents(self):
        """:class:`Command`: Retrieves the parents of this command.

        If the command has no parents then it returns an empty :class:`list`.

        For example in commands ``?a b c test``, the parents are ``[c, b, a]``.

        .. versionadded:: 1.1
        """
        entries = []
        command = self
        while True:
            if command.parent is not None:
                command = command.parent
                entries.append(command)

        return entries

    @property
    def root_parent(self):
        """Retrieves the root parent of this command.

        If the command has no parents then it returns ``None``.

        For example in commands ``?a b c test``, the root parent is ``a``.
        """
        if not self.parent:
            return
        return self.parents[(-1)]

    @property
    def qualified_name(self):
        """:class:`str`: Retrieves the fully qualified command name.

        This is the full parent name with the command name as well.
        For example, in ``?one two three`` the qualified name would be
        ``one two three``.
        """
        parent = self.full_parent_name
        if parent:
            return parent + ' ' + self.name
        return self.name

    def __str__(self):
        return self.qualified_name

    async def _parse_arguments--- This code section failed: ---

 L. 644         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cog
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    16  'to 16'
               10  LOAD_FAST                'ctx'
               12  BUILD_LIST_1          1 
               14  JUMP_FORWARD         24  'to 24'
             16_0  COME_FROM             8  '8'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                cog
               20  LOAD_FAST                'ctx'
               22  BUILD_LIST_2          2 
             24_0  COME_FROM            14  '14'
               24  LOAD_FAST                'ctx'
               26  STORE_ATTR               args

 L. 645        28  BUILD_MAP_0           0 
               30  LOAD_FAST                'ctx'
               32  STORE_ATTR               kwargs

 L. 646        34  LOAD_FAST                'ctx'
               36  LOAD_ATTR                args
               38  STORE_FAST               'args'

 L. 647        40  LOAD_FAST                'ctx'
               42  LOAD_ATTR                kwargs
               44  STORE_FAST               'kwargs'

 L. 649        46  LOAD_FAST                'ctx'
               48  LOAD_ATTR                view
               50  STORE_FAST               'view'

 L. 650        52  LOAD_GLOBAL              iter
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                params
               58  LOAD_METHOD              items
               60  CALL_METHOD_0         0  ''
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'iterator'

 L. 652        66  LOAD_FAST                'self'
               68  LOAD_ATTR                cog
               70  LOAD_CONST               None
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_FALSE   130  'to 130'

 L. 655        76  SETUP_FINALLY        90  'to 90'

 L. 656        78  LOAD_GLOBAL              next
               80  LOAD_FAST                'iterator'
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_FORWARD        130  'to 130'
             90_0  COME_FROM_FINALLY    76  '76'

 L. 657        90  DUP_TOP          
               92  LOAD_GLOBAL              StopIteration
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   128  'to 128'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 658       104  LOAD_STR                 'Callback for {0.name} command is missing "self" parameter.'
              106  STORE_FAST               'fmt'

 L. 659       108  LOAD_GLOBAL              discord
              110  LOAD_METHOD              ClientException
              112  LOAD_FAST                'fmt'
              114  LOAD_METHOD              format
              116  LOAD_FAST                'self'
              118  CALL_METHOD_1         1  ''
              120  CALL_METHOD_1         1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            96  '96'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            88  '88'
            130_2  COME_FROM            74  '74'

 L. 662       130  SETUP_FINALLY       144  'to 144'

 L. 663       132  LOAD_GLOBAL              next
              134  LOAD_FAST                'iterator'
              136  CALL_FUNCTION_1       1  ''
              138  POP_TOP          
              140  POP_BLOCK        
              142  JUMP_FORWARD        184  'to 184'
            144_0  COME_FROM_FINALLY   130  '130'

 L. 664       144  DUP_TOP          
              146  LOAD_GLOBAL              StopIteration
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   182  'to 182'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 665       158  LOAD_STR                 'Callback for {0.name} command is missing "ctx" parameter.'
              160  STORE_FAST               'fmt'

 L. 666       162  LOAD_GLOBAL              discord
              164  LOAD_METHOD              ClientException
              166  LOAD_FAST                'fmt'
              168  LOAD_METHOD              format
              170  LOAD_FAST                'self'
              172  CALL_METHOD_1         1  ''
              174  CALL_METHOD_1         1  ''
              176  RAISE_VARARGS_1       1  'exception instance'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           150  '150'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           142  '142'

 L. 668       184  LOAD_FAST                'iterator'
              186  GET_ITER         
            188_0  COME_FROM           418  '418'
            188_1  COME_FROM           406  '406'
            188_2  COME_FROM           352  '352'
            188_3  COME_FROM           346  '346'
            188_4  COME_FROM           334  '334'
            188_5  COME_FROM           236  '236'
              188  FOR_ITER            420  'to 420'
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'name'
              194  STORE_FAST               'param'

 L. 669       196  LOAD_FAST                'param'
              198  LOAD_ATTR                kind
              200  LOAD_FAST                'param'
              202  LOAD_ATTR                POSITIONAL_OR_KEYWORD
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   238  'to 238'

 L. 670       208  LOAD_FAST                'self'
              210  LOAD_METHOD              transform
              212  LOAD_FAST                'ctx'
              214  LOAD_FAST                'param'
              216  CALL_METHOD_2         2  ''
              218  GET_AWAITABLE    
              220  LOAD_CONST               None
              222  YIELD_FROM       
              224  STORE_FAST               'transformed'

 L. 671       226  LOAD_FAST                'args'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'transformed'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_BACK           188  'to 188'
            238_0  COME_FROM           206  '206'

 L. 672       238  LOAD_FAST                'param'
              240  LOAD_ATTR                kind
              242  LOAD_FAST                'param'
              244  LOAD_ATTR                KEYWORD_ONLY
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   336  'to 336'

 L. 674       252  LOAD_FAST                'self'
              254  LOAD_ATTR                rest_is_raw
          256_258  POP_JUMP_IF_FALSE   306  'to 306'

 L. 675       260  LOAD_FAST                'self'
              262  LOAD_METHOD              _get_converter
              264  LOAD_FAST                'param'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'converter'

 L. 676       270  LOAD_FAST                'view'
              272  LOAD_METHOD              read_rest
              274  CALL_METHOD_0         0  ''
              276  STORE_FAST               'argument'

 L. 677       278  LOAD_FAST                'self'
              280  LOAD_METHOD              do_conversion
              282  LOAD_FAST                'ctx'
              284  LOAD_FAST                'converter'
              286  LOAD_FAST                'argument'
              288  LOAD_FAST                'param'
              290  CALL_METHOD_4         4  ''
              292  GET_AWAITABLE    
              294  LOAD_CONST               None
              296  YIELD_FROM       
              298  LOAD_FAST                'kwargs'
              300  LOAD_FAST                'name'
              302  STORE_SUBSCR     
              304  JUMP_FORWARD        328  'to 328'
            306_0  COME_FROM           256  '256'

 L. 679       306  LOAD_FAST                'self'
              308  LOAD_METHOD              transform
              310  LOAD_FAST                'ctx'
              312  LOAD_FAST                'param'
              314  CALL_METHOD_2         2  ''
              316  GET_AWAITABLE    
              318  LOAD_CONST               None
              320  YIELD_FROM       
              322  LOAD_FAST                'kwargs'
              324  LOAD_FAST                'name'
              326  STORE_SUBSCR     
            328_0  COME_FROM           304  '304'

 L. 680       328  POP_TOP          
          330_332  BREAK_LOOP          420  'to 420'
              334  JUMP_BACK           188  'to 188'
            336_0  COME_FROM           248  '248'

 L. 681       336  LOAD_FAST                'param'
              338  LOAD_ATTR                kind
              340  LOAD_FAST                'param'
              342  LOAD_ATTR                VAR_POSITIONAL
              344  COMPARE_OP               ==
              346  POP_JUMP_IF_FALSE_BACK   188  'to 188'
            348_0  COME_FROM           414  '414'
            348_1  COME_FROM           410  '410'
            348_2  COME_FROM           386  '386'

 L. 682       348  LOAD_FAST                'view'
              350  LOAD_ATTR                eof
              352  POP_JUMP_IF_TRUE_BACK   188  'to 188'

 L. 683       354  SETUP_FINALLY       388  'to 388'

 L. 684       356  LOAD_FAST                'self'
              358  LOAD_METHOD              transform
              360  LOAD_FAST                'ctx'
              362  LOAD_FAST                'param'
              364  CALL_METHOD_2         2  ''
              366  GET_AWAITABLE    
              368  LOAD_CONST               None
              370  YIELD_FROM       
              372  STORE_FAST               'transformed'

 L. 685       374  LOAD_FAST                'args'
              376  LOAD_METHOD              append
              378  LOAD_FAST                'transformed'
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
              384  POP_BLOCK        
              386  JUMP_BACK           348  'to 348'
            388_0  COME_FROM_FINALLY   354  '354'

 L. 686       388  DUP_TOP          
              390  LOAD_GLOBAL              RuntimeError
              392  COMPARE_OP               exception-match
          394_396  POP_JUMP_IF_FALSE   412  'to 412'
              398  POP_TOP          
              400  POP_TOP          
              402  POP_TOP          

 L. 687       404  POP_EXCEPT       
              406  JUMP_BACK           188  'to 188'
              408  POP_EXCEPT       
              410  JUMP_BACK           348  'to 348'
            412_0  COME_FROM           394  '394'
              412  END_FINALLY      
          414_416  JUMP_BACK           348  'to 348'
              418  JUMP_BACK           188  'to 188'
            420_0  COME_FROM           330  '330'
            420_1  COME_FROM           188  '188'

 L. 689       420  LOAD_FAST                'self'
              422  LOAD_ATTR                ignore_extra
          424_426  POP_JUMP_IF_TRUE    450  'to 450'

 L. 690       428  LOAD_FAST                'view'
              430  LOAD_ATTR                eof
          432_434  POP_JUMP_IF_TRUE    450  'to 450'

 L. 691       436  LOAD_GLOBAL              TooManyArguments
              438  LOAD_STR                 'Too many arguments passed to '
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                qualified_name
              444  BINARY_ADD       
              446  CALL_FUNCTION_1       1  ''
              448  RAISE_VARARGS_1       1  'exception instance'
            450_0  COME_FROM           432  '432'
            450_1  COME_FROM           424  '424'

Parse error at or near `JUMP_BACK' instruction at offset 410

    async def call_before_hooks(self, ctx):
        cog = self.cog
        if self._before_invoke is not None:
            if cog is None:
                await self._before_invoke(ctx)
            else:
                await self._before_invoke(cog, ctx)
        if cog is not None:
            hook = Cog._get_overridden_method(cog.cog_before_invoke)
            if hook is not None:
                await hook(ctx)
        hook = ctx.bot._before_invoke
        if hook is not None:
            await hook(ctx)

    async def call_after_hooks(self, ctx):
        cog = self.cog
        if self._after_invoke is not None:
            if cog is None:
                await self._after_invoke(ctx)
            else:
                await self._after_invoke(cog, ctx)
        if cog is not None:
            hook = Cog._get_overridden_method(cog.cog_after_invoke)
            if hook is not None:
                await hook(ctx)
        hook = ctx.bot._after_invoke
        if hook is not None:
            await hook(ctx)

    def _prepare_cooldowns(self, ctx):
        if self._buckets.valid:
            current = ctx.message.created_at.replace(tzinfo=(datetime.timezone.utc)).timestamp()
            bucket = self._buckets.get_bucket(ctx.message, current)
            retry_after = bucket.update_rate_limit(current)
            if retry_after:
                raise CommandOnCooldown(bucket, retry_after)

    async def prepare(self, ctx):
        ctx.command = self
        if not await self.can_run(ctx):
            raise CheckFailure('The check functions for command {0.qualified_name} failed.'.format(self))
        if self.cooldown_after_parsing:
            await self._parse_arguments(ctx)
            self._prepare_cooldowns(ctx)
        else:
            self._prepare_cooldowns(ctx)
            await self._parse_arguments(ctx)
        if self._max_concurrency is not None:
            await self._max_concurrency.acquire(ctx)
        await self.call_before_hooks(ctx)

    def is_on_cooldown(self, ctx):
        """Checks whether the command is currently on cooldown.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to use when checking the commands cooldown status.

        Returns
        --------
        :class:`bool`
            A boolean indicating if the command is on cooldown.
        """
        if not self._buckets.valid:
            return False
        bucket = self._buckets.get_bucket(ctx.message)
        return bucket.get_tokens() == 0

    def reset_cooldown(self, ctx):
        """Resets the cooldown on this command.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to reset the cooldown under.
        """
        if self._buckets.valid:
            bucket = self._buckets.get_bucket(ctx.message)
            bucket.reset()

    async def invoke(self, ctx):
        await self.prepare(ctx)
        ctx.invoked_subcommand = None
        injected = hooked_wrapped_callback(self, ctx, self.callback)
        await injected(*ctx.args, **ctx.kwargs)

    async def reinvoke(self, ctx, *, call_hooks=False):
        ctx.command = self
        await self._parse_arguments(ctx)
        if call_hooks:
            await self.call_before_hooks(ctx)
        ctx.invoked_subcommand = None
        try:
            try:
                await (self.callback)(*ctx.args, **ctx.kwargs)
            except:
                ctx.command_failed = True
                raise

        finally:
            if call_hooks:
                await self.call_after_hooks(ctx)

    def error(self, coro):
        """A decorator that registers a coroutine as a local error handler.

        A local error handler is an :func:`.on_command_error` event limited to
        a single command. However, the :func:`.on_command_error` is still
        invoked afterwards as the catch-all.

        Parameters
        -----------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register as the local error handler.

        Raises
        -------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The error handler must be a coroutine.')
        self.on_error = coro
        return coro

    def before_invoke(self, coro):
        """A decorator that registers a coroutine as a pre-invoke hook.

        A pre-invoke hook is called directly before the command is
        called. This makes it a useful function to set up database
        connections or any type of set up required.

        This pre-invoke hook takes a sole parameter, a :class:`.Context`.

        See :meth:`.Bot.before_invoke` for more info.

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
        """A decorator that registers a coroutine as a post-invoke hook.

        A post-invoke hook is called directly after the command is
        called. This makes it a useful function to clean-up database
        connections or any type of clean up required.

        This post-invoke hook takes a sole parameter, a :class:`.Context`.

        See :meth:`.Bot.after_invoke` for more info.

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

    @property
    def cog_name(self):
        """:class:`str`: The name of the cog this command belongs to. None otherwise."""
        if self.cog is not None:
            return type(self.cog).__cog_name__

    @property
    def short_doc(self):
        """:class:`str`: Gets the "short" documentation of a command.

        By default, this is the :attr:`brief` attribute.
        If that lookup leads to an empty string then the first line of the
        :attr:`help` attribute is used instead.
        """
        if self.brief is not None:
            return self.brief
        if self.help is not None:
            return self.help.split('\n', 1)[0]
        return ''

    def _is_typing_optional(self, annotation):
        try:
            origin = annotation.__origin__
        except AttributeError:
            return False
        else:
            if origin is not typing.Union:
                return False
            else:
                return annotation.__args__[(-1)] is type(None)

    @property
    def signature--- This code section failed: ---

 L. 927         0  LOAD_FAST                'self'
                2  LOAD_ATTR                usage
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 928        10  LOAD_FAST                'self'
               12  LOAD_ATTR                usage
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 931        16  LOAD_FAST                'self'
               18  LOAD_ATTR                clean_params
               20  STORE_FAST               'params'

 L. 932        22  LOAD_FAST                'params'
               24  POP_JUMP_IF_TRUE     30  'to 30'

 L. 933        26  LOAD_STR                 ''
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 935        30  BUILD_LIST_0          0 
               32  STORE_FAST               'result'

 L. 936        34  LOAD_FAST                'params'
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''
               40  GET_ITER         
             42_0  COME_FROM           256  '256'
             42_1  COME_FROM           240  '240'
             42_2  COME_FROM           212  '212'
             42_3  COME_FROM           192  '192'
             42_4  COME_FROM           164  '164'
             42_5  COME_FROM           146  '146'
               42  FOR_ITER            258  'to 258'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'name'
               48  STORE_FAST               'param'

 L. 937        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'param'
               54  LOAD_ATTR                annotation
               56  LOAD_GLOBAL              converters
               58  LOAD_ATTR                _Greedy
               60  CALL_FUNCTION_2       2  ''
               62  STORE_FAST               'greedy'

 L. 939        64  LOAD_FAST                'param'
               66  LOAD_ATTR                default
               68  LOAD_FAST                'param'
               70  LOAD_ATTR                empty
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_FALSE   166  'to 166'

 L. 942        76  LOAD_GLOBAL              isinstance
               78  LOAD_FAST                'param'
               80  LOAD_ATTR                default
               82  LOAD_GLOBAL              str
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE    94  'to 94'
               88  LOAD_FAST                'param'
               90  LOAD_ATTR                default
               92  JUMP_FORWARD        102  'to 102'
             94_0  COME_FROM            86  '86'
               94  LOAD_FAST                'param'
               96  LOAD_ATTR                default
               98  LOAD_CONST               None
              100  COMPARE_OP               is-not
            102_0  COME_FROM            92  '92'
              102  STORE_FAST               'should_print'

 L. 943       104  LOAD_FAST                'should_print'
              106  POP_JUMP_IF_FALSE   150  'to 150'

 L. 944       108  LOAD_FAST                'result'
              110  LOAD_METHOD              append
              112  LOAD_FAST                'greedy'
              114  POP_JUMP_IF_TRUE    130  'to 130'
              116  LOAD_STR                 '[%s=%s]'
              118  LOAD_FAST                'name'
              120  LOAD_FAST                'param'
              122  LOAD_ATTR                default
              124  BUILD_TUPLE_2         2 
              126  BINARY_MODULO    
              128  JUMP_FORWARD        142  'to 142'
            130_0  COME_FROM           114  '114'

 L. 945       130  LOAD_STR                 '[%s=%s]...'
              132  LOAD_FAST                'name'
              134  LOAD_FAST                'param'
              136  LOAD_ATTR                default
              138  BUILD_TUPLE_2         2 
              140  BINARY_MODULO    
            142_0  COME_FROM           128  '128'

 L. 944       142  CALL_METHOD_1         1  ''
              144  POP_TOP          

 L. 946       146  JUMP_BACK            42  'to 42'
              148  BREAK_LOOP          164  'to 164'
            150_0  COME_FROM           106  '106'

 L. 948       150  LOAD_FAST                'result'
              152  LOAD_METHOD              append
              154  LOAD_STR                 '[%s]'
              156  LOAD_FAST                'name'
              158  BINARY_MODULO    
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           148  '148'
              164  JUMP_BACK            42  'to 42'
            166_0  COME_FROM            74  '74'

 L. 950       166  LOAD_FAST                'param'
              168  LOAD_ATTR                kind
              170  LOAD_FAST                'param'
              172  LOAD_ATTR                VAR_POSITIONAL
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   194  'to 194'

 L. 951       178  LOAD_FAST                'result'
              180  LOAD_METHOD              append
              182  LOAD_STR                 '[%s...]'
              184  LOAD_FAST                'name'
              186  BINARY_MODULO    
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
              192  JUMP_BACK            42  'to 42'
            194_0  COME_FROM           176  '176'

 L. 952       194  LOAD_FAST                'greedy'
              196  POP_JUMP_IF_FALSE   214  'to 214'

 L. 953       198  LOAD_FAST                'result'
              200  LOAD_METHOD              append
              202  LOAD_STR                 '[%s]...'
              204  LOAD_FAST                'name'
              206  BINARY_MODULO    
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  JUMP_BACK            42  'to 42'
            214_0  COME_FROM           196  '196'

 L. 954       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _is_typing_optional
              218  LOAD_FAST                'param'
              220  LOAD_ATTR                annotation
              222  CALL_METHOD_1         1  ''
              224  POP_JUMP_IF_FALSE   242  'to 242'

 L. 955       226  LOAD_FAST                'result'
              228  LOAD_METHOD              append
              230  LOAD_STR                 '[%s]'
              232  LOAD_FAST                'name'
              234  BINARY_MODULO    
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
              240  JUMP_BACK            42  'to 42'
            242_0  COME_FROM           224  '224'

 L. 957       242  LOAD_FAST                'result'
              244  LOAD_METHOD              append
              246  LOAD_STR                 '<%s>'
              248  LOAD_FAST                'name'
              250  BINARY_MODULO    
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  JUMP_BACK            42  'to 42'
            258_0  COME_FROM            42  '42'

 L. 959       258  LOAD_STR                 ' '
              260  LOAD_METHOD              join
              262  LOAD_FAST                'result'
              264  CALL_METHOD_1         1  ''
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 166_0

    async def can_run--- This code section failed: ---

 L. 988         0  LOAD_FAST                'self'
                2  LOAD_ATTR                enabled
                4  POP_JUMP_IF_TRUE     20  'to 20'

 L. 989         6  LOAD_GLOBAL              DisabledCommand
                8  LOAD_STR                 '{0.name} command is disabled'
               10  LOAD_METHOD              format
               12  LOAD_FAST                'self'
               14  CALL_METHOD_1         1  ''
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             4  '4'

 L. 991        20  LOAD_DEREF               'ctx'
               22  LOAD_ATTR                command
               24  STORE_FAST               'original'

 L. 992        26  LOAD_FAST                'self'
               28  LOAD_DEREF               'ctx'
               30  STORE_ATTR               command

 L. 994        32  SETUP_FINALLY       186  'to 186'

 L. 995        34  LOAD_DEREF               'ctx'
               36  LOAD_ATTR                bot
               38  LOAD_METHOD              can_run
               40  LOAD_DEREF               'ctx'
               42  CALL_METHOD_1         1  ''
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  POP_JUMP_IF_TRUE     66  'to 66'

 L. 996        52  LOAD_GLOBAL              CheckFailure
               54  LOAD_STR                 'The global check functions for command {0.qualified_name} failed.'
               56  LOAD_METHOD              format
               58  LOAD_FAST                'self'
               60  CALL_METHOD_1         1  ''
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            50  '50'

 L. 998        66  LOAD_FAST                'self'
               68  LOAD_ATTR                cog
               70  STORE_FAST               'cog'

 L. 999        72  LOAD_FAST                'cog'
               74  LOAD_CONST               None
               76  COMPARE_OP               is-not
               78  POP_JUMP_IF_FALSE   132  'to 132'

 L.1000        80  LOAD_GLOBAL              Cog
               82  LOAD_METHOD              _get_overridden_method
               84  LOAD_FAST                'cog'
               86  LOAD_ATTR                cog_check
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'local_check'

 L.1001        92  LOAD_FAST                'local_check'
               94  LOAD_CONST               None
               96  COMPARE_OP               is-not
               98  POP_JUMP_IF_FALSE   132  'to 132'

 L.1002       100  LOAD_GLOBAL              discord
              102  LOAD_ATTR                utils
              104  LOAD_METHOD              maybe_coroutine
              106  LOAD_FAST                'local_check'
              108  LOAD_DEREF               'ctx'
              110  CALL_METHOD_2         2  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  STORE_FAST               'ret'

 L.1003       120  LOAD_FAST                'ret'
              122  POP_JUMP_IF_TRUE    132  'to 132'

 L.1004       124  POP_BLOCK        
              126  CALL_FINALLY        186  'to 186'
              128  LOAD_CONST               False
              130  RETURN_VALUE     
            132_0  COME_FROM           122  '122'
            132_1  COME_FROM            98  '98'
            132_2  COME_FROM            78  '78'

 L.1006       132  LOAD_FAST                'self'
              134  LOAD_ATTR                checks
              136  STORE_FAST               'predicates'

 L.1007       138  LOAD_FAST                'predicates'
              140  POP_JUMP_IF_TRUE    150  'to 150'

 L.1009       142  POP_BLOCK        
              144  CALL_FINALLY        186  'to 186'
              146  LOAD_CONST               True
              148  RETURN_VALUE     
            150_0  COME_FROM           140  '140'

 L.1011       150  LOAD_GLOBAL              discord
              152  LOAD_ATTR                utils
              154  LOAD_METHOD              async_all
              156  LOAD_CLOSURE             'ctx'
              158  BUILD_TUPLE_1         1 
              160  LOAD_GENEXPR             '<code_object <genexpr>>'
              162  LOAD_STR                 'Command.can_run.<locals>.<genexpr>'
              164  MAKE_FUNCTION_8          'closure'
              166  LOAD_FAST                'predicates'
              168  GET_ITER         
              170  CALL_FUNCTION_1       1  ''
              172  CALL_METHOD_1         1  ''
              174  GET_AWAITABLE    
              176  LOAD_CONST               None
              178  YIELD_FROM       
              180  POP_BLOCK        
              182  CALL_FINALLY        186  'to 186'
              184  RETURN_VALUE     
            186_0  COME_FROM           182  '182'
            186_1  COME_FROM           144  '144'
            186_2  COME_FROM           126  '126'
            186_3  COME_FROM_FINALLY    32  '32'

 L.1013       186  LOAD_FAST                'original'
              188  LOAD_DEREF               'ctx'
              190  STORE_ATTR               command
              192  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 126


class GroupMixin:
    __doc__ = 'A mixin that implements common functionality for classes that behave\n    similar to :class:`.Group` and are allowed to register commands.\n\n    Attributes\n    -----------\n    all_commands: :class:`dict`\n        A mapping of command name to :class:`.Command` or subclass\n        objects.\n    case_insensitive: :class:`bool`\n        Whether the commands should be case insensitive. Defaults to ``False``.\n    '

    def __init__(self, *args, **kwargs):
        case_insensitive = kwargs.get('case_insensitive', False)
        self.all_commands = _CaseInsensitiveDict() if case_insensitive else {}
        self.case_insensitive = case_insensitive
        (super().__init__)(*args, **kwargs)

    @property
    def commands(self):
        """Set[:class:`.Command`]: A unique set of commands without aliases that are registered."""
        return set(self.all_commands.values())

    def recursively_remove_all_commands(self):
        for command in self.all_commands.copy().values():
            if isinstance(command, GroupMixin):
                command.recursively_remove_all_commands()
            else:
                self.remove_command(command.name)

    def add_command(self, command):
        """Adds a :class:`.Command` or its subclasses into the internal list
        of commands.

        This is usually not called, instead the :meth:`~.GroupMixin.command` or
        :meth:`~.GroupMixin.group` shortcut decorators are used instead.

        Parameters
        -----------
        command: :class:`Command`
            The command to add.

        Raises
        -------
        :exc:`.ClientException`
            If the command is already registered.
        TypeError
            If the command passed is not a subclass of :class:`.Command`.
        """
        if not isinstance(command, Command):
            raise TypeError('The command passed must be a subclass of Command')
        if isinstance(self, Command):
            command.parent = self
        if command.name in self.all_commands:
            raise discord.ClientException('Command {0.name} is already registered.'.format(command))
        self.all_commands[command.name] = command
        for alias in command.aliases:
            if alias in self.all_commands:
                raise discord.ClientException('The alias {} is already an existing command or alias.'.format(alias))
            else:
                self.all_commands[alias] = command

    def remove_command(self, name):
        """Remove a :class:`.Command` or subclasses from the internal list
        of commands.

        This could also be used as a way to remove aliases.

        Parameters
        -----------
        name: :class:`str`
            The name of the command to remove.

        Returns
        --------
        :class:`.Command` or subclass
            The command that was removed. If the name is not valid then
            `None` is returned instead.
        """
        command = self.all_commands.pop(name, None)
        if command is None:
            return
        if name in command.aliases:
            return command
        for alias in command.aliases:
            self.all_commands.pop(alias, None)
        else:
            return command

    def walk_commands(self):
        """An iterator that recursively walks through all commands and subcommands."""
        for command in tuple(self.all_commands.values()):
            yield command
            if isinstance(command, GroupMixin):
                yield from command.walk_commands()

    def get_command(self, name):
        """Get a :class:`.Command` or subclasses from the internal list
        of commands.

        This could also be used as a way to get aliases.

        The name could be fully qualified (e.g. ``'foo bar'``) will get
        the subcommand ``bar`` of the group command ``foo``. If a
        subcommand is not found then ``None`` is returned just as usual.

        Parameters
        -----------
        name: :class:`str`
            The name of the command to get.

        Returns
        --------
        :class:`Command` or subclass
            The command that was requested. If not found, returns ``None``.
        """
        if ' ' not in name:
            return self.all_commands.get(name)
        names = name.split()
        obj = self.all_commands.get(names[0])
        if not isinstance(obj, GroupMixin):
            return obj
        for name in names[1:]:
            try:
                obj = obj.all_commands[name]
            except (AttributeError, KeyError):
                return None

        else:
            return obj

    def command(self, *args, **kwargs):
        """A shortcut decorator that invokes :func:`.command` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.
        """

        def decorator(func):
            kwargs.setdefault('parent', self)
            result = command(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator

    def group(self, *args, **kwargs):
        """A shortcut decorator that invokes :func:`.group` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.
        """

        def decorator(func):
            kwargs.setdefault('parent', self)
            result = group(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator


class Group(GroupMixin, Command):
    __doc__ = "A class that implements a grouping protocol for commands to be\n    executed as subcommands.\n\n    This class is a subclass of :class:`.Command` and thus all options\n    valid in :class:`.Command` are valid in here as well.\n\n    Attributes\n    -----------\n    invoke_without_command: Optional[:class:`bool`]\n        Indicates if the group callback should begin parsing and\n        invocation only if no subcommand was found. Useful for\n        making it an error handling function to tell the user that\n        no subcommand was found or to have different functionality\n        in case no subcommand was found. If this is ``False``, then\n        the group callback will always be invoked first. This means\n        that the checks and the parsing dictated by its parameters\n        will be executed. Defaults to ``False``.\n    case_insensitive: Optional[:class:`bool`]\n        Indicates if the group's commands should be case insensitive.\n        Defaults to ``False``.\n    "

    def __init__(self, *args, **attrs):
        self.invoke_without_command = attrs.pop('invoke_without_command', False)
        (super().__init__)(*args, **attrs)

    def copy(self):
        ret = super().copy()
        for cmd in self.commands:
            ret.add_command(cmd.copy())
        else:
            return ret

    async def invoke(self, ctx):
        ctx.invoked_subcommand = None
        early_invoke = not self.invoke_without_command
        if early_invoke:
            await self.prepare(ctx)
        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()
        if trigger:
            ctx.subcommand_passed = trigger
            ctx.invoked_subcommand = self.all_commands.get(trigger, None)
        if early_invoke:
            injected = hooked_wrapped_callback(self, ctx, self.callback)
            await injected(*ctx.args, **ctx.kwargs)
        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.invoke(ctx)
        elif not early_invoke:
            view.index = previous
            view.previous = previous
            await super().invoke(ctx)

    async def reinvoke(self, ctx, *, call_hooks=False):
        ctx.invoked_subcommand = None
        early_invoke = not self.invoke_without_command
        if early_invoke:
            ctx.command = self
            await self._parse_arguments(ctx)
            if call_hooks:
                await self.call_before_hooks(ctx)
        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()
        if trigger:
            ctx.subcommand_passed = trigger
            ctx.invoked_subcommand = self.all_commands.get(trigger, None)
        if early_invoke:
            try:
                try:
                    await (self.callback)(*ctx.args, **ctx.kwargs)
                except:
                    ctx.command_failed = True
                    raise

            finally:
                if call_hooks:
                    await self.call_after_hooks(ctx)

        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.reinvoke(ctx, call_hooks=call_hooks)
        elif not early_invoke:
            view.index = previous
            view.previous = previous
            await super().reinvoke(ctx, call_hooks=call_hooks)


def command(name=None, cls=None, **attrs):
    """A decorator that transforms a function into a :class:`.Command`
    or if called with :func:`.group`, :class:`.Group`.

    By default the ``help`` attribute is received automatically from the
    docstring of the function and is cleaned up with the use of
    ``inspect.cleandoc``. If the docstring is ``bytes``, then it is decoded
    into :class:`str` using utf-8 encoding.

    All checks added using the :func:`.check` & co. decorators are added into
    the function. There is no way to supply your own checks through this
    decorator.

    Parameters
    -----------
    name: :class:`str`
        The name to create the command with. By default this uses the
        function name unchanged.
    cls
        The class to construct with. By default this is :class:`.Command`.
        You usually do not change this.
    attrs
        Keyword arguments to pass into the construction of the class denoted
        by ``cls``.

    Raises
    -------
    TypeError
        If the function is not a coroutine or is already a command.
    """
    if cls is None:
        cls = Command

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return cls(func, name=name, **attrs)

    return decorator


def group(name=None, **attrs):
    """A decorator that transforms a function into a :class:`.Group`.

    This is similar to the :func:`.command` decorator but the ``cls``
    parameter is set to :class:`Group` by default.

    .. versionchanged:: 1.1
        The ``cls`` parameter can now be passed.
    """
    attrs.setdefault('cls', Group)
    return command(name=name, **attrs)


def check(predicate):
    r"""A decorator that adds a check to the :class:`.Command` or its
    subclasses. These checks could be accessed via :attr:`.Command.checks`.

    These checks should be predicates that take in a single parameter taking
    a :class:`.Context`. If the check returns a ``False``\-like value then
    during invocation a :exc:`.CheckFailure` exception is raised and sent to
    the :func:`.on_command_error` event.

    If an exception should be thrown in the predicate then it should be a
    subclass of :exc:`.CommandError`. Any exception not subclassed from it
    will be propagated while those subclassed will be sent to
    :func:`.on_command_error`.

    A special attribute named ``predicate`` is bound to the value
    returned by this decorator to retrieve the predicate passed to the
    decorator. This allows the following introspection and chaining to be done:

    .. code-block:: python3

        def owner_or_permissions(**perms):
            original = commands.has_permissions(**perms).predicate
            async def extended_check(ctx):
                if ctx.guild is None:
                    return False
                return ctx.guild.owner_id == ctx.author.id or await original(ctx)
            return commands.check(extended_check)

    .. note::

        The function returned by ``predicate`` is **always** a coroutine,
        even if the original function was not a coroutine.

    .. versionchanged:: 1.3
        The ``predicate`` attribute was added.

    Examples
    ---------

    Creating a basic check to see if the command invoker is you.

    .. code-block:: python3

        def check_if_it_is_me(ctx):
            return ctx.message.author.id == 85309593344815104

        @bot.command()
        @commands.check(check_if_it_is_me)
        async def only_for_me(ctx):
            await ctx.send('I know you!')

    Transforming common checks into its own decorator:

    .. code-block:: python3

        def is_me():
            def predicate(ctx):
                return ctx.message.author.id == 85309593344815104
            return commands.check(predicate)

        @bot.command()
        @is_me()
        async def only_me(ctx):
            await ctx.send('Only you!')

    Parameters
    -----------
    predicate: Callable[[:class:`Context`], :class:`bool`]
        The predicate to check if the command should be invoked.
    """

    def decorator(func):
        if isinstance(func, Command):
            func.checks.append(predicate)
        else:
            if not hasattr(func, '__commands_checks__'):
                func.__commands_checks__ = []
            func.__commands_checks__.append(predicate)
        return func

    if inspect.iscoroutinefunction(predicate):
        decorator.predicate = predicate
    else:

        @functools.wraps(predicate)
        async def wrapper(ctx):
            return predicate(ctx)

        decorator.predicate = wrapper
    return decorator


def check_any(*checks):
    r"""A :func:`check` that is added that checks if any of the checks passed
    will pass, i.e. using logical OR.

    If all checks fail then :exc:`.CheckAnyFailure` is raised to signal the failure.
    It inherits from :exc:`.CheckFailure`.

    .. note::

        The ``predicate`` attribute for this function **is** a coroutine.

    .. versionadded:: 1.3

    Parameters
    ------------
    \*checks: Callable[[:class:`Context`], :class:`bool`]
        An argument list of checks that have been decorated with
        the :func:`check` decorator.

    Raises
    -------
    TypeError
        A check passed has not been decorated with the :func:`check`
        decorator.

    Examples
    ---------

    Creating a basic check to see if it's the bot owner or
    the server owner:

    .. code-block:: python3

        def is_guild_owner():
            def predicate(ctx):
                return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
            return commands.check(predicate)

        @bot.command()
        @commands.check_any(commands.is_owner(), is_guild_owner())
        async def only_for_owners(ctx):
            await ctx.send('Hello mister owner!')
    """
    unwrapped = []
    for wrapped in checks:
        try:
            pred = wrapped.predicate
        except AttributeError:
            raise TypeError('%r must be wrapped by commands.check decorator' % wrapped) from None
        else:
            unwrapped.append(pred)
    else:

        async def predicate(ctx):
            errors = []
            for func in unwrapped:
                try:
                    value = await func(ctx)
                except CheckFailure as e:
                    try:
                        errors.append(e)
                    finally:
                        e = None
                        del e

                else:
                    if value:
                        return True
            else:
                raise CheckAnyFailure(unwrapped, errors)

        return check(predicate)


def has_role(item):
    """A :func:`.check` that is added that checks if the member invoking the
    command has the role specified via the name or ID specified.

    If a string is specified, you must give the exact name of the role, including
    caps and spelling.

    If an integer is specified, you must give the exact snowflake ID of the role.

    If the message is invoked in a private message context then the check will
    return ``False``.

    This check raises one of two special exceptions, :exc:`.MissingRole` if the user
    is missing a role, or :exc:`.NoPrivateMessage` if it is used in a private message.
    Both inherit from :exc:`.CheckFailure`.

    .. versionchanged:: 1.1

        Raise :exc:`.MissingRole` or :exc:`.NoPrivateMessage`
        instead of generic :exc:`.CheckFailure`

    Parameters
    -----------
    item: Union[:class:`int`, :class:`str`]
        The name or ID of the role to check.
    """

    def predicate(ctx):
        if not isinstance(ctx.channel, discord.abc.GuildChannel):
            raise NoPrivateMessage()
        if isinstance(item, int):
            role = discord.utils.get((ctx.author.roles), id=item)
        else:
            role = discord.utils.get((ctx.author.roles), name=item)
        if role is None:
            raise MissingRole(item)
        return True

    return check(predicate)


def has_any_role(*items):
    r"""A :func:`.check` that is added that checks if the member invoking the
    command has **any** of the roles specified. This means that if they have
    one out of the three roles specified, then this check will return `True`.

    Similar to :func:`.has_role`\, the names or IDs passed in must be exact.

    This check raises one of two special exceptions, :exc:`.MissingAnyRole` if the user
    is missing all roles, or :exc:`.NoPrivateMessage` if it is used in a private message.
    Both inherit from :exc:`.CheckFailure`.

    .. versionchanged:: 1.1

        Raise :exc:`.MissingAnyRole` or :exc:`.NoPrivateMessage`
        instead of generic :exc:`.CheckFailure`

    Parameters
    -----------
    items: List[Union[:class:`str`, :class:`int`]]
        An argument list of names or IDs to check that the member has roles wise.

    Example
    --------

    .. code-block:: python3

        @bot.command()
        @commands.has_any_role('Library Devs', 'Moderators', 492212595072434186)
        async def cool(ctx):
            await ctx.send('You are cool indeed')
    """

    def predicate(ctx):
        if not isinstance(ctx.channel, discord.abc.GuildChannel):
            raise NoPrivateMessage()
        getter = functools.partial(discord.utils.get, ctx.author.roles)
        if any(((getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None) for item in items)):
            return True
        raise MissingAnyRole(items)

    return check(predicate)


def bot_has_role(item):
    """Similar to :func:`.has_role` except checks if the bot itself has the
    role.

    This check raises one of two special exceptions, :exc:`.BotMissingRole` if the bot
    is missing the role, or :exc:`.NoPrivateMessage` if it is used in a private message.
    Both inherit from :exc:`.CheckFailure`.

    .. versionchanged:: 1.1

        Raise :exc:`.BotMissingRole` or :exc:`.NoPrivateMessage`
        instead of generic :exc:`.CheckFailure`
    """

    def predicate(ctx):
        ch = ctx.channel
        if not isinstance(ch, discord.abc.GuildChannel):
            raise NoPrivateMessage()
        me = ch.guild.me
        if isinstance(item, int):
            role = discord.utils.get((me.roles), id=item)
        else:
            role = discord.utils.get((me.roles), name=item)
        if role is None:
            raise BotMissingRole(item)
        return True

    return check(predicate)


def bot_has_any_role(*items):
    """Similar to :func:`.has_any_role` except checks if the bot itself has
    any of the roles listed.

    This check raises one of two special exceptions, :exc:`.BotMissingAnyRole` if the bot
    is missing all roles, or :exc:`.NoPrivateMessage` if it is used in a private message.
    Both inherit from :exc:`.CheckFailure`.

    .. versionchanged:: 1.1

        Raise :exc:`.BotMissingAnyRole` or :exc:`.NoPrivateMessage`
        instead of generic checkfailure
    """

    def predicate(ctx):
        ch = ctx.channel
        if not isinstance(ch, discord.abc.GuildChannel):
            raise NoPrivateMessage()
        me = ch.guild.me
        getter = functools.partial(discord.utils.get, me.roles)
        if any(((getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None) for item in items)):
            return True
        raise BotMissingAnyRole(items)

    return check(predicate)


def has_permissions(**perms):
    """A :func:`.check` that is added that checks if the member has all of
    the permissions necessary.

    Note that this check operates on the current channel permissions, not the
    guild wide permissions.

    The permissions passed in must be exactly like the properties shown under
    :class:`.discord.Permissions`.

    This check raises a special exception, :exc:`.MissingPermissions`
    that is inherited from :exc:`.CheckFailure`.

    Parameters
    ------------
    perms
        An argument list of permissions to check for.

    Example
    ---------

    .. code-block:: python3

        @bot.command()
        @commands.has_permissions(manage_messages=True)
        async def test(ctx):
            await ctx.send('You can manage messages.')

    """
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % ', '.join(invalid))

    def predicate(ctx):
        ch = ctx.channel
        permissions = ch.permissions_for(ctx.author)
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise MissingPermissions(missing)

    return check(predicate)


def bot_has_permissions(**perms):
    """Similar to :func:`.has_permissions` except checks if the bot itself has
    the permissions listed.

    This check raises a special exception, :exc:`.BotMissingPermissions`
    that is inherited from :exc:`.CheckFailure`.
    """
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % ', '.join(invalid))

    def predicate(ctx):
        guild = ctx.guild
        me = guild.me if guild is not None else ctx.bot.user
        permissions = ctx.channel.permissions_for(me)
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise BotMissingPermissions(missing)

    return check(predicate)


def has_guild_permissions(**perms):
    """Similar to :func:`.has_permissions`, but operates on guild wide
    permissions instead of the current channel permissions.

    If this check is called in a DM context, it will raise an
    exception, :exc:`.NoPrivateMessage`.

    .. versionadded:: 1.3
    """
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % ', '.join(invalid))

    def predicate(ctx):
        if not ctx.guild:
            raise NoPrivateMessage
        permissions = ctx.author.guild_permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise MissingPermissions(missing)

    return check(predicate)


def bot_has_guild_permissions(**perms):
    """Similar to :func:`.has_guild_permissions`, but checks the bot
    members guild permissions.

    .. versionadded:: 1.3
    """
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError('Invalid permission(s): %s' % ', '.join(invalid))

    def predicate(ctx):
        if not ctx.guild:
            raise NoPrivateMessage
        permissions = ctx.me.guild_permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise BotMissingPermissions(missing)

    return check(predicate)


def dm_only():
    """A :func:`.check` that indicates this command must only be used in a
    DM context. Only private messages are allowed when
    using the command.

    This check raises a special exception, :exc:`.PrivateMessageOnly`
    that is inherited from :exc:`.CheckFailure`.

    .. versionadded:: 1.1
    """

    def predicate(ctx):
        if ctx.guild is not None:
            raise PrivateMessageOnly()
        return True

    return check(predicate)


def guild_only():
    """A :func:`.check` that indicates this command must only be used in a
    guild context only. Basically, no private messages are allowed when
    using the command.

    This check raises a special exception, :exc:`.NoPrivateMessage`
    that is inherited from :exc:`.CheckFailure`.
    """

    def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return True

    return check(predicate)


def is_owner():
    """A :func:`.check` that checks if the person invoking this command is the
    owner of the bot.

    This is powered by :meth:`.Bot.is_owner`.

    This check raises a special exception, :exc:`.NotOwner` that is derived
    from :exc:`.CheckFailure`.
    """

    async def predicate(ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise NotOwner('You do not own this bot.')
        return True

    return check(predicate)


def is_nsfw():
    """A :func:`.check` that checks if the channel is a NSFW channel.

    This check raises a special exception, :exc:`.NSFWChannelRequired`
    that is derived from :exc:`.CheckFailure`.

    .. versionchanged:: 1.1

        Raise :exc:`.NSFWChannelRequired` instead of generic :exc:`.CheckFailure`.
        DM channels will also now pass this check.
    """

    def pred(ctx):
        ch = ctx.channel
        if ctx.guild is None or (isinstance(ch, discord.TextChannel) and ch.is_nsfw()):
            return True
        raise NSFWChannelRequired(ch)

    return check(pred)


def cooldown(rate, per, type=BucketType.default):
    """A decorator that adds a cooldown to a :class:`.Command`
    or its subclasses.

    A cooldown allows a command to only be used a specific amount
    of times in a specific time frame. These cooldowns can be based
    either on a per-guild, per-channel, per-user, per-role or global basis.
    Denoted by the third argument of ``type`` which must be of enum
    type :class:`.BucketType`.

    If a cooldown is triggered, then :exc:`.CommandOnCooldown` is triggered in
    :func:`.on_command_error` and the local error handler.

    A command can only have a single cooldown.

    Parameters
    ------------
    rate: :class:`int`
        The number of times a command can be used before triggering a cooldown.
    per: :class:`float`
        The amount of seconds to wait for a cooldown when it's been triggered.
    type: :class:`.BucketType`
        The type of cooldown to have.
    """

    def decorator(func):
        if isinstance(func, Command):
            func._buckets = CooldownMapping(Cooldown(rate, per, type))
        else:
            func.__commands_cooldown__ = Cooldown(rate, per, type)
        return func

    return decorator


def max_concurrency(number, per=BucketType.default, *, wait=False):
    """A decorator that adds a maximum concurrency to a :class:`.Command` or its subclasses.

    This enables you to only allow a certain number of command invocations at the same time,
    for example if a command takes too long or if only one user can use it at a time. This
    differs from a cooldown in that there is no set waiting period or token bucket -- only
    a set number of people can run the command.

    .. versionadded:: 1.3

    Parameters
    -------------
    number: :class:`int`
        The maximum number of invocations of this command that can be running at the same time.
    per: :class:`.BucketType`
        The bucket that this concurrency is based on, e.g. ``BucketType.guild`` would allow
        it to be used up to ``number`` times per guild.
    wait: :class:`bool`
        Whether the command should wait for the queue to be over. If this is set to ``False``
        then instead of waiting until the command can run again, the command raises
        :exc:`.MaxConcurrencyReached` to its error handler. If this is set to ``True``
        then the command waits until it can be executed.
    """

    def decorator(func):
        value = MaxConcurrency(number, per=per, wait=wait)
        if isinstance(func, Command):
            func._max_concurrency = value
        else:
            func.__commands_max_concurrency__ = value
        return func

    return decorator