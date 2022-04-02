# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\cog.py
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
import inspect, copy
from ._types import _BaseCommand
__all__ = ('CogMeta', 'Cog')

class CogMeta(type):
    __doc__ = "A metaclass for defining a cog.\n\n    Note that you should probably not use this directly. It is exposed\n    purely for documentation purposes along with making custom metaclasses to intermix\n    with other metaclasses such as the :class:`abc.ABCMeta` metaclass.\n\n    For example, to create an abstract cog mixin class, the following would be done.\n\n    .. code-block:: python3\n\n        import abc\n\n        class CogABCMeta(commands.CogMeta, abc.ABCMeta):\n            pass\n\n        class SomeMixin(metaclass=abc.ABCMeta):\n            pass\n\n        class SomeCogMixin(SomeMixin, commands.Cog, metaclass=CogABCMeta):\n            pass\n\n    .. note::\n\n        When passing an attribute of a metaclass that is documented below, note\n        that you must pass it as a keyword-only argument to the class creation\n        like the following example:\n\n        .. code-block:: python3\n\n            class MyCog(commands.Cog, name='My Cog'):\n                pass\n\n    Attributes\n    -----------\n    name: :class:`str`\n        The cog name. By default, it is the name of the class with no modification.\n    command_attrs: :class:`dict`\n        A list of attributes to apply to every command inside this cog. The dictionary\n        is passed into the :class:`Command` (or its subclass) options at ``__init__``.\n        If you specify attributes inside the command attribute in the class, it will\n        override the one specified inside this attribute. For example:\n\n        .. code-block:: python3\n\n            class MyCog(commands.Cog, command_attrs=dict(hidden=True)):\n                @commands.command()\n                async def foo(self, ctx):\n                    pass # hidden -> True\n\n                @commands.command(hidden=False)\n                async def bar(self, ctx):\n                    pass # hidden -> False\n    "

    def __new__--- This code section failed: ---

 L.  92         0  LOAD_FAST                'args'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'name'
                6  STORE_FAST               'bases'
                8  STORE_FAST               'attrs'

 L.  93        10  LOAD_FAST                'kwargs'
               12  LOAD_METHOD              pop
               14  LOAD_STR                 'name'
               16  LOAD_FAST                'name'
               18  CALL_METHOD_2         2  ''
               20  LOAD_FAST                'attrs'
               22  LOAD_STR                 '__cog_name__'
               24  STORE_SUBSCR     

 L.  94        26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              pop
               30  LOAD_STR                 'command_attrs'
               32  BUILD_MAP_0           0 
               34  CALL_METHOD_2         2  ''
               36  DUP_TOP          
               38  LOAD_FAST                'attrs'
               40  LOAD_STR                 '__cog_settings__'
               42  STORE_SUBSCR     
               44  STORE_FAST               'command_attrs'

 L.  96        46  BUILD_MAP_0           0 
               48  STORE_FAST               'commands'

 L.  97        50  BUILD_MAP_0           0 
               52  STORE_FAST               'listeners'

 L.  98        54  LOAD_STR                 'Commands or listeners must not start with cog_ or bot_ (in method {0.__name__}.{1})'
               56  STORE_FAST               'no_bot_cog'

 L. 100        58  LOAD_GLOBAL              super
               60  CALL_FUNCTION_0       0  ''
               62  LOAD_ATTR                __new__
               64  LOAD_FAST                'cls'
               66  LOAD_FAST                'name'
               68  LOAD_FAST                'bases'
               70  LOAD_FAST                'attrs'
               72  BUILD_TUPLE_4         4 
               74  LOAD_FAST                'kwargs'
               76  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               78  STORE_FAST               'new_cls'

 L. 101        80  LOAD_GLOBAL              reversed
               82  LOAD_FAST                'new_cls'
               84  LOAD_ATTR                __mro__
               86  CALL_FUNCTION_1       1  ''
               88  GET_ITER         
             90_0  COME_FROM           316  '316'
               90  FOR_ITER            318  'to 318'
               92  STORE_FAST               'base'

 L. 102        94  LOAD_FAST                'base'
               96  LOAD_ATTR                __dict__
               98  LOAD_METHOD              items
              100  CALL_METHOD_0         0  ''
              102  GET_ITER         
            104_0  COME_FROM           314  '314'
            104_1  COME_FROM           274  '274'
            104_2  COME_FROM           270  '270'
            104_3  COME_FROM           234  '234'
            104_4  COME_FROM           224  '224'
              104  FOR_ITER            316  'to 316'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'elem'
              110  STORE_FAST               'value'

 L. 103       112  LOAD_FAST                'elem'
              114  LOAD_FAST                'commands'
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   126  'to 126'

 L. 104       120  LOAD_FAST                'commands'
              122  LOAD_FAST                'elem'
              124  DELETE_SUBSCR    
            126_0  COME_FROM           118  '118'

 L. 105       126  LOAD_FAST                'elem'
              128  LOAD_FAST                'listeners'
              130  COMPARE_OP               in
              132  POP_JUMP_IF_FALSE   140  'to 140'

 L. 106       134  LOAD_FAST                'listeners'
              136  LOAD_FAST                'elem'
              138  DELETE_SUBSCR    
            140_0  COME_FROM           132  '132'

 L. 108       140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'value'
              144  LOAD_GLOBAL              staticmethod
              146  CALL_FUNCTION_2       2  ''
              148  STORE_FAST               'is_static_method'

 L. 109       150  LOAD_FAST                'is_static_method'
              152  POP_JUMP_IF_FALSE   160  'to 160'

 L. 110       154  LOAD_FAST                'value'
              156  LOAD_ATTR                __func__
              158  STORE_FAST               'value'
            160_0  COME_FROM           152  '152'

 L. 111       160  LOAD_GLOBAL              isinstance
              162  LOAD_FAST                'value'
              164  LOAD_GLOBAL              _BaseCommand
              166  CALL_FUNCTION_2       2  ''
              168  POP_JUMP_IF_FALSE   226  'to 226'

 L. 112       170  LOAD_FAST                'is_static_method'
              172  POP_JUMP_IF_FALSE   190  'to 190'

 L. 113       174  LOAD_GLOBAL              TypeError
              176  LOAD_STR                 'Command in method {0}.{1!r} must not be staticmethod.'
              178  LOAD_METHOD              format
              180  LOAD_FAST                'base'
              182  LOAD_FAST                'elem'
              184  CALL_METHOD_2         2  ''
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'
            190_0  COME_FROM           172  '172'

 L. 114       190  LOAD_FAST                'elem'
              192  LOAD_METHOD              startswith
              194  LOAD_CONST               ('cog_', 'bot_')
              196  CALL_METHOD_1         1  ''
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L. 115       200  LOAD_GLOBAL              TypeError
              202  LOAD_FAST                'no_bot_cog'
              204  LOAD_METHOD              format
              206  LOAD_FAST                'base'
              208  LOAD_FAST                'elem'
              210  CALL_METHOD_2         2  ''
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           198  '198'

 L. 116       216  LOAD_FAST                'value'
              218  LOAD_FAST                'commands'
              220  LOAD_FAST                'elem'
              222  STORE_SUBSCR     
              224  JUMP_BACK           104  'to 104'
            226_0  COME_FROM           168  '168'

 L. 117       226  LOAD_GLOBAL              inspect
              228  LOAD_METHOD              iscoroutinefunction
              230  LOAD_FAST                'value'
              232  CALL_METHOD_1         1  ''
              234  POP_JUMP_IF_FALSE_BACK   104  'to 104'

 L. 118       236  SETUP_FINALLY       252  'to 252'

 L. 119       238  LOAD_GLOBAL              getattr
              240  LOAD_FAST                'value'
              242  LOAD_STR                 '__cog_listener__'
              244  CALL_FUNCTION_2       2  ''
              246  STORE_FAST               'is_listener'
              248  POP_BLOCK        
              250  JUMP_FORWARD        278  'to 278'
            252_0  COME_FROM_FINALLY   236  '236'

 L. 120       252  DUP_TOP          
              254  LOAD_GLOBAL              AttributeError
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   276  'to 276'
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 121       268  POP_EXCEPT       
              270  JUMP_BACK           104  'to 104'
              272  POP_EXCEPT       
              274  JUMP_BACK           104  'to 104'
            276_0  COME_FROM           258  '258'
              276  END_FINALLY      
            278_0  COME_FROM           250  '250'

 L. 123       278  LOAD_FAST                'elem'
              280  LOAD_METHOD              startswith
              282  LOAD_CONST               ('cog_', 'bot_')
              284  CALL_METHOD_1         1  ''
          286_288  POP_JUMP_IF_FALSE   306  'to 306'

 L. 124       290  LOAD_GLOBAL              TypeError
              292  LOAD_FAST                'no_bot_cog'
              294  LOAD_METHOD              format
              296  LOAD_FAST                'base'
              298  LOAD_FAST                'elem'
              300  CALL_METHOD_2         2  ''
              302  CALL_FUNCTION_1       1  ''
              304  RAISE_VARARGS_1       1  'exception instance'
            306_0  COME_FROM           286  '286'

 L. 125       306  LOAD_FAST                'value'
              308  LOAD_FAST                'listeners'
              310  LOAD_FAST                'elem'
              312  STORE_SUBSCR     
              314  JUMP_BACK           104  'to 104'
            316_0  COME_FROM           104  '104'
              316  JUMP_BACK            90  'to 90'
            318_0  COME_FROM            90  '90'

 L. 127       318  LOAD_GLOBAL              list
              320  LOAD_FAST                'commands'
              322  LOAD_METHOD              values
              324  CALL_METHOD_0         0  ''
              326  CALL_FUNCTION_1       1  ''
              328  LOAD_FAST                'new_cls'
              330  STORE_ATTR               __cog_commands__

 L. 129       332  BUILD_LIST_0          0 
              334  STORE_FAST               'listeners_as_list'

 L. 130       336  LOAD_FAST                'listeners'
              338  LOAD_METHOD              values
              340  CALL_METHOD_0         0  ''
              342  GET_ITER         
            344_0  COME_FROM           378  '378'
              344  FOR_ITER            382  'to 382'
              346  STORE_FAST               'listener'

 L. 131       348  LOAD_FAST                'listener'
              350  LOAD_ATTR                __cog_listener_names__
              352  GET_ITER         
            354_0  COME_FROM           374  '374'
              354  FOR_ITER            378  'to 378'
              356  STORE_FAST               'listener_name'

 L. 134       358  LOAD_FAST                'listeners_as_list'
              360  LOAD_METHOD              append
              362  LOAD_FAST                'listener_name'
              364  LOAD_FAST                'listener'
              366  LOAD_ATTR                __name__
              368  BUILD_TUPLE_2         2 
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
          374_376  JUMP_BACK           354  'to 354'
            378_0  COME_FROM           354  '354'
          378_380  JUMP_BACK           344  'to 344'
            382_0  COME_FROM           344  '344'

 L. 136       382  LOAD_FAST                'listeners_as_list'
              384  LOAD_FAST                'new_cls'
              386  STORE_ATTR               __cog_listeners__

 L. 137       388  LOAD_FAST                'new_cls'
              390  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 274

    def __init__(self, *args, **kwargs):
        (super.__init__)(*args)

    @classmethod
    def qualified_name(cls):
        return cls.__cog_name__


def _cog_special_method(func):
    func.__cog_special_method__ = None
    return func


class Cog(metaclass=CogMeta):
    __doc__ = 'The base class that all cogs must inherit from.\n\n    A cog is a collection of commands, listeners, and optional state to\n    help group commands together. More information on them can be found on\n    the :ref:`ext_commands_cogs` page.\n\n    When inheriting from this class, the options shown in :class:`CogMeta`\n    are equally valid here.\n    '

    def __new__(cls, *args, **kwargs):
        self = super.__new__cls
        cmd_attrs = cls.__cog_settings__
        self.__cog_commands__ = tuple((c._update_copycmd_attrs for c in cls.__cog_commands__))
        lookup = {cmd:cmd.qualified_name for cmd in self.__cog_commands__}
        for command in self.__cog_commands__:
            setattr(self, command.callback.__name__, command)
            parent = command.parent
            if parent is not None:
                parent = lookup[parent.qualified_name]
                removed = parent.remove_commandcommand.name
                parent.add_commandcommand
        else:
            return self

    def get_commands(self):
        r"""Returns a :class:`list` of :class:`.Command`\s that are
        defined inside this cog.

        .. note::

            This does not include subcommands.
        """
        return [c for c in self.__cog_commands__ if c.parent is None]

    @property
    def qualified_name(self):
        """:class:`str`: Returns the cog's specified name, not the class name."""
        return self.__cog_name__

    @property
    def description(self):
        """:class:`str`: Returns the cog's description, typically the cleaned docstring."""
        try:
            return self.__cog_cleaned_doc__
        except AttributeError:
            self.__cog_cleaned_doc__ = cleaned = inspect.getdocself
            return cleaned

    def walk_commands(self):
        """An iterator that recursively walks through this cog's commands and subcommands."""
        from .core import GroupMixin
        for command in self.__cog_commands__:
            if command.parent is None:
                yield command
                if isinstancecommandGroupMixin:
                    yield from command.walk_commands

    def get_listeners(self):
        """Returns a :class:`list` of (name, function) listener pairs that are defined in this cog."""
        return [(name, getattrselfmethod_name) for name, method_name in self.__cog_listeners__]

    @classmethod
    def _get_overridden_method(cls, method):
        """Return None if the method is not overridden. Otherwise returns the overridden method."""
        return getattr(method.__func__, '__cog_special_method__', method)

    @classmethod
    def listener(cls, name=None):
        """A decorator that marks a function as a listener.

        This is the cog equivalent of :meth:`.Bot.listen`.

        Parameters
        ------------
        name: :class:`str`
            The name of the event being listened to. If not provided, it
            defaults to the function's name.

        Raises
        --------
        TypeError
            The function is not a coroutine function or a string was not passed as
            the name.
        """
        if name is not None:
            if not isinstancenamestr:
                raise TypeError('Cog.listener expected str but received {0.__class__.__name__!r} instead.'.formatname)

            def decorator(func):
                actual = func
                if isinstanceactualstaticmethod:
                    actual = actual.__func__
                if not inspect.iscoroutinefunctionactual:
                    raise TypeError('Listener function must be a coroutine function.')
                actual.__cog_listener__ = True
                to_assign = name or actual.__name__
                try:
                    actual.__cog_listener_names__.appendto_assign
                except AttributeError:
                    actual.__cog_listener_names__ = [
                     to_assign]
                else:
                    return func

            return decorator

    @_cog_special_method
    def cog_unload(self):
        """A special method that is called when the cog gets removed.

        This function **cannot** be a coroutine. It must be a regular
        function.

        Subclasses must replace this if they want special unloading behaviour.
        """
        pass

    @_cog_special_method
    def bot_check_once(self, ctx):
        """A special method that registers as a :meth:`.Bot.check_once`
        check.

        This function **can** be a coroutine and must take a sole parameter,
        ``ctx``, to represent the :class:`.Context`.
        """
        return True

    @_cog_special_method
    def bot_check(self, ctx):
        """A special method that registers as a :meth:`.Bot.check`
        check.

        This function **can** be a coroutine and must take a sole parameter,
        ``ctx``, to represent the :class:`.Context`.
        """
        return True

    @_cog_special_method
    def cog_check(self, ctx):
        """A special method that registers as a :func:`commands.check`
        for every command and subcommand in this cog.

        This function **can** be a coroutine and must take a sole parameter,
        ``ctx``, to represent the :class:`.Context`.
        """
        return True

    @_cog_special_method
    def cog_command_error(self, ctx, error):
        """A special method that is called whenever an error
        is dispatched inside this cog.

        This is similar to :func:`.on_command_error` except only applying
        to the commands inside this cog.

        This function **can** be a coroutine.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context where the error happened.
        error: :class:`CommandError`
            The error that happened.
        """
        pass

    @_cog_special_method
    async def cog_before_invoke(self, ctx):
        """A special method that acts as a cog local pre-invoke hook.

        This is similar to :meth:`.Command.before_invoke`.

        This **must** be a coroutine.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context.
        """
        pass

    @_cog_special_method
    async def cog_after_invoke(self, ctx):
        """A special method that acts as a cog local post-invoke hook.

        This is similar to :meth:`.Command.after_invoke`.

        This **must** be a coroutine.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context.
        """
        pass

    def _inject(self, bot):
        cls = self.__class__
        for index, command in enumerate(self.__cog_commands__):
            command.cog = self
            if command.parent is None:
                try:
                    bot.add_commandcommand
                except Exception as e:
                    try:
                        for to_undo in self.__cog_commands__[:index]:
                            bot.remove_commandto_undo
                        else:
                            raise e

                    finally:
                        e = None
                        del e

        else:
            if cls.bot_check is not Cog.bot_check:
                bot.add_checkself.bot_check
            if cls.bot_check_once is not Cog.bot_check_once:
                bot.add_check((self.bot_check_once), call_once=True)
            for name, method_name in self.__cog_listeners__:
                bot.add_listenergetattrselfmethod_namename
            else:
                return self

    def _eject(self, bot):
        cls = self.__class__
        try:
            for command in self.__cog_commands__:
                if command.parent is None:
                    bot.remove_commandcommand.name
            else:
                for _, method_name in self.__cog_listeners__:
                    bot.remove_listenergetattrselfmethod_name
                else:
                    if cls.bot_check is not Cog.bot_check:
                        bot.remove_checkself.bot_check
                    if cls.bot_check_once is not Cog.bot_check_once:
                        bot.remove_check((self.bot_check_once), call_once=True)

        finally:
            self.cog_unload