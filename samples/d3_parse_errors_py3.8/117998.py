# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\context.py
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
import discord.abc, discord.utils

class Context(discord.abc.Messageable):
    __doc__ = 'Represents the context in which a command is being invoked under.\n\n    This class contains a lot of meta data to help you understand more about\n    the invocation context. This class is not created manually and is instead\n    passed around to commands as the first parameter.\n\n    This class implements the :class:`~discord.abc.Messageable` ABC.\n\n    Attributes\n    -----------\n    message: :class:`.Message`\n        The message that triggered the command being executed.\n    bot: :class:`.Bot`\n        The bot that contains the command being executed.\n    args: :class:`list`\n        The list of transformed arguments that were passed into the command.\n        If this is accessed during the :func:`on_command_error` event\n        then this list could be incomplete.\n    kwargs: :class:`dict`\n        A dictionary of transformed arguments that were passed into the command.\n        Similar to :attr:`args`\\, if this is accessed in the\n        :func:`on_command_error` event then this dict could be incomplete.\n    prefix: :class:`str`\n        The prefix that was used to invoke the command.\n    command\n        The command (i.e. :class:`.Command` or its subclasses) that is being\n        invoked currently.\n    invoked_with: :class:`str`\n        The command name that triggered this invocation. Useful for finding out\n        which alias called the command.\n    invoked_subcommand\n        The subcommand (i.e. :class:`.Command` or its subclasses) that was\n        invoked. If no valid subcommand was invoked then this is equal to\n        ``None``.\n    subcommand_passed: Optional[:class:`str`]\n        The string that was attempted to call a subcommand. This does not have\n        to point to a valid registered subcommand and could just point to a\n        nonsense string. If nothing was passed to attempt a call to a\n        subcommand then this is set to ``None``.\n    command_failed: :class:`bool`\n        A boolean that indicates if the command failed to be parsed, checked,\n        or invoked.\n    '

    def __init__(self, **attrs):
        self.message = attrs.pop('message', None)
        self.bot = attrs.pop('bot', None)
        self.args = attrs.pop('args', [])
        self.kwargs = attrs.pop('kwargs', {})
        self.prefix = attrs.pop('prefix')
        self.command = attrs.pop('command', None)
        self.view = attrs.pop('view', None)
        self.invoked_with = attrs.pop('invoked_with', None)
        self.invoked_subcommand = attrs.pop('invoked_subcommand', None)
        self.subcommand_passed = attrs.pop('subcommand_passed', None)
        self.command_failed = attrs.pop('command_failed', False)
        self._state = self.message._state

    async def invoke(self, *args, **kwargs):
        r"""|coro|

        Calls a command with the arguments given.

        This is useful if you want to just call the callback that a
        :class:`.Command` holds internally.

        .. note::

            This does not handle converters, checks, cooldowns, pre-invoke,
            or after-invoke hooks in any matter. It calls the internal callback
            directly as-if it was a regular function.

            You must take care in passing the proper arguments when
            using this function.

        .. warning::

            The first parameter passed **must** be the command being invoked.

        Parameters
        -----------
        command: :class:`.Command`
            A command or subclass of a command that is going to be called.
        \*args
            The arguments to to use.
        \*\*kwargs
            The keyword arguments to use.
        """
        try:
            command = args[0]
        except IndexError:
            raise TypeError('Missing command to invoke.') from None
        else:
            arguments = []
            if command.cog is not None:
                arguments.append(command.cog)
            else:
                arguments.append(self)
                arguments.extend(args[1:])
                ret = await (command.callback)(*arguments, **kwargs)
                return ret

    async def reinvoke(self, *, call_hooks=False, restart=True):
        """|coro|

        Calls the command again.

        This is similar to :meth:`~.Context.invoke` except that it bypasses
        checks, cooldowns, and error handlers.

        .. note::

            If you want to bypass :exc:`.UserInputError` derived exceptions,
            it is recommended to use the regular :meth:`~.Context.invoke`
            as it will work more naturally. After all, this will end up
            using the old arguments the user has used and will thus just
            fail again.

        Parameters
        ------------
        call_hooks: :class:`bool`
            Whether to call the before and after invoke hooks.
        restart: :class:`bool`
            Whether to start the call chain from the very beginning
            or where we left off (i.e. the command that caused the error).
            The default is to start where we left off.
        """
        cmd = self.command
        view = self.view
        if cmd is None:
            raise ValueError('This context is not valid.')
        index, previous = view.index, view.previous
        invoked_with = self.invoked_with
        invoked_subcommand = self.invoked_subcommand
        subcommand_passed = self.subcommand_passed
        if restart:
            to_call = cmd.root_parent or cmd
            view.index = len(self.prefix)
            view.previous = 0
            view.get_word()
        else:
            to_call = cmd
        try:
            await to_call.reinvoke(self, call_hooks=call_hooks)
        finally:
            self.command = cmd
            view.index = index
            view.previous = previous
            self.invoked_with = invoked_with
            self.invoked_subcommand = invoked_subcommand
            self.subcommand_passed = subcommand_passed

    @property
    def valid(self):
        """Checks if the invocation context is valid to be invoked with."""
        return self.prefix is not None and self.command is not None

    async def _get_channel(self):
        return self.channel

    @property
    def cog(self):
        """Returns the cog associated with this context's command. None if it does not exist."""
        if self.command is None:
            return
        return self.command.cog

    @discord.utils.cached_property
    def guild(self):
        """Returns the guild associated with this context's command. None if not available."""
        return self.message.guild

    @discord.utils.cached_property
    def channel(self):
        """Returns the channel associated with this context's command. Shorthand for :attr:`.Message.channel`."""
        return self.message.channel

    @discord.utils.cached_property
    def author(self):
        """Returns the author associated with this context's command. Shorthand for :attr:`.Message.author`"""
        return self.message.author

    @discord.utils.cached_property
    def me(self):
        """Similar to :attr:`.Guild.me` except it may return the :class:`.ClientUser` in private message contexts."""
        if self.guild is not None:
            return self.guild.me
        return self.bot.user

    @property
    def voice_client(self):
        r"""Optional[:class:`.VoiceClient`]: A shortcut to :attr:`.Guild.voice_client`\, if applicable."""
        g = self.guild
        if g:
            return g.voice_client

    async def send_help--- This code section failed: ---

 L. 261         0  LOAD_CONST               1
                2  LOAD_CONST               ('Group', 'Command', 'wrap_callback')
                4  IMPORT_NAME              core
                6  IMPORT_FROM              Group
                8  STORE_FAST               'Group'
               10  IMPORT_FROM              Command
               12  STORE_FAST               'Command'
               14  IMPORT_FROM              wrap_callback
               16  STORE_FAST               'wrap_callback'
               18  POP_TOP          

 L. 262        20  LOAD_CONST               1
               22  LOAD_CONST               ('CommandError',)
               24  IMPORT_NAME              errors
               26  IMPORT_FROM              CommandError
               28  STORE_FAST               'CommandError'
               30  POP_TOP          

 L. 264        32  LOAD_FAST                'self'
               34  LOAD_ATTR                bot
               36  STORE_FAST               'bot'

 L. 265        38  LOAD_FAST                'bot'
               40  LOAD_ATTR                help_command
               42  STORE_FAST               'cmd'

 L. 267        44  LOAD_FAST                'cmd'
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 268        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 270        56  LOAD_FAST                'cmd'
               58  LOAD_METHOD              copy
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'cmd'

 L. 271        64  LOAD_FAST                'self'
               66  LOAD_FAST                'cmd'
               68  STORE_ATTR               context

 L. 272        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'args'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               0
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   194  'to 194'

 L. 273        82  LOAD_FAST                'cmd'
               84  LOAD_METHOD              prepare_help_command
               86  LOAD_FAST                'self'
               88  LOAD_CONST               None
               90  CALL_METHOD_2         2  ''
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  POP_TOP          

 L. 274       100  LOAD_FAST                'cmd'
              102  LOAD_METHOD              get_bot_mapping
              104  CALL_METHOD_0         0  ''
              106  STORE_FAST               'mapping'

 L. 275       108  LOAD_FAST                'wrap_callback'
              110  LOAD_FAST                'cmd'
              112  LOAD_ATTR                send_bot_help
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'injected'

 L. 276       118  SETUP_FINALLY       136  'to 136'

 L. 277       120  LOAD_FAST                'injected'
              122  LOAD_FAST                'mapping'
              124  CALL_FUNCTION_1       1  ''
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  POP_BLOCK        
              134  RETURN_VALUE     
            136_0  COME_FROM_FINALLY   118  '118'

 L. 278       136  DUP_TOP          
              138  LOAD_FAST                'CommandError'
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   192  'to 192'
              144  POP_TOP          
              146  STORE_FAST               'e'
              148  POP_TOP          
              150  SETUP_FINALLY       180  'to 180'

 L. 279       152  LOAD_FAST                'cmd'
              154  LOAD_METHOD              on_help_command_error
              156  LOAD_FAST                'self'
              158  LOAD_FAST                'e'
              160  CALL_METHOD_2         2  ''
              162  GET_AWAITABLE    
              164  LOAD_CONST               None
              166  YIELD_FROM       
              168  POP_TOP          

 L. 280       170  POP_BLOCK        
              172  POP_EXCEPT       
              174  CALL_FINALLY        180  'to 180'
              176  LOAD_CONST               None
              178  RETURN_VALUE     
            180_0  COME_FROM           174  '174'
            180_1  COME_FROM_FINALLY   150  '150'
              180  LOAD_CONST               None
              182  STORE_FAST               'e'
              184  DELETE_FAST              'e'
              186  END_FINALLY      
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           142  '142'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM            80  '80'

 L. 282       194  LOAD_FAST                'args'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  STORE_FAST               'entity'

 L. 283       202  LOAD_FAST                'entity'
              204  LOAD_CONST               None
              206  COMPARE_OP               is
              208  POP_JUMP_IF_FALSE   214  'to 214'

 L. 284       210  LOAD_CONST               None
              212  RETURN_VALUE     
            214_0  COME_FROM           208  '208'

 L. 286       214  LOAD_GLOBAL              isinstance
              216  LOAD_FAST                'entity'
              218  LOAD_GLOBAL              str
              220  CALL_FUNCTION_2       2  ''
              222  POP_JUMP_IF_FALSE   244  'to 244'

 L. 287       224  LOAD_FAST                'bot'
              226  LOAD_METHOD              get_cog
              228  LOAD_FAST                'entity'
              230  CALL_METHOD_1         1  ''
              232  JUMP_IF_TRUE_OR_POP   242  'to 242'
              234  LOAD_FAST                'bot'
              236  LOAD_METHOD              get_command
              238  LOAD_FAST                'entity'
              240  CALL_METHOD_1         1  ''
            242_0  COME_FROM           232  '232'
              242  STORE_FAST               'entity'
            244_0  COME_FROM           222  '222'

 L. 289       244  SETUP_FINALLY       256  'to 256'

 L. 290       246  LOAD_FAST                'entity'
              248  LOAD_ATTR                qualified_name
              250  STORE_FAST               'qualified_name'
              252  POP_BLOCK        
              254  JUMP_FORWARD        280  'to 280'
            256_0  COME_FROM_FINALLY   244  '244'

 L. 291       256  DUP_TOP          
              258  LOAD_GLOBAL              AttributeError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   278  'to 278'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 293       272  POP_EXCEPT       
              274  LOAD_CONST               None
              276  RETURN_VALUE     
            278_0  COME_FROM           262  '262'
              278  END_FINALLY      
            280_0  COME_FROM           254  '254'

 L. 295       280  LOAD_FAST                'cmd'
              282  LOAD_METHOD              prepare_help_command
              284  LOAD_FAST                'self'
              286  LOAD_FAST                'entity'
              288  LOAD_ATTR                qualified_name
              290  CALL_METHOD_2         2  ''
              292  GET_AWAITABLE    
              294  LOAD_CONST               None
              296  YIELD_FROM       
              298  POP_TOP          

 L. 297       300  SETUP_FINALLY       426  'to 426'

 L. 298       302  LOAD_GLOBAL              hasattr
              304  LOAD_FAST                'entity'
              306  LOAD_STR                 '__cog_commands__'
              308  CALL_FUNCTION_2       2  ''
          310_312  POP_JUMP_IF_FALSE   340  'to 340'

 L. 299       314  LOAD_FAST                'wrap_callback'
              316  LOAD_FAST                'cmd'
              318  LOAD_ATTR                send_cog_help
              320  CALL_FUNCTION_1       1  ''
              322  STORE_FAST               'injected'

 L. 300       324  LOAD_FAST                'injected'
              326  LOAD_FAST                'entity'
              328  CALL_FUNCTION_1       1  ''
              330  GET_AWAITABLE    
              332  LOAD_CONST               None
              334  YIELD_FROM       
              336  POP_BLOCK        
              338  RETURN_VALUE     
            340_0  COME_FROM           310  '310'

 L. 301       340  LOAD_GLOBAL              isinstance
              342  LOAD_FAST                'entity'
              344  LOAD_FAST                'Group'
              346  CALL_FUNCTION_2       2  ''
          348_350  POP_JUMP_IF_FALSE   378  'to 378'

 L. 302       352  LOAD_FAST                'wrap_callback'
              354  LOAD_FAST                'cmd'
              356  LOAD_ATTR                send_group_help
              358  CALL_FUNCTION_1       1  ''
              360  STORE_FAST               'injected'

 L. 303       362  LOAD_FAST                'injected'
              364  LOAD_FAST                'entity'
              366  CALL_FUNCTION_1       1  ''
              368  GET_AWAITABLE    
              370  LOAD_CONST               None
              372  YIELD_FROM       
              374  POP_BLOCK        
              376  RETURN_VALUE     
            378_0  COME_FROM           348  '348'

 L. 304       378  LOAD_GLOBAL              isinstance
              380  LOAD_FAST                'entity'
              382  LOAD_FAST                'Command'
              384  CALL_FUNCTION_2       2  ''
          386_388  POP_JUMP_IF_FALSE   416  'to 416'

 L. 305       390  LOAD_FAST                'wrap_callback'
              392  LOAD_FAST                'cmd'
              394  LOAD_ATTR                send_command_help
              396  CALL_FUNCTION_1       1  ''
              398  STORE_FAST               'injected'

 L. 306       400  LOAD_FAST                'injected'
              402  LOAD_FAST                'entity'
              404  CALL_FUNCTION_1       1  ''
              406  GET_AWAITABLE    
              408  LOAD_CONST               None
              410  YIELD_FROM       
              412  POP_BLOCK        
              414  RETURN_VALUE     
            416_0  COME_FROM           386  '386'

 L. 308       416  POP_BLOCK        
              418  LOAD_CONST               None
              420  RETURN_VALUE     
              422  POP_BLOCK        
              424  JUMP_FORWARD        480  'to 480'
            426_0  COME_FROM_FINALLY   300  '300'

 L. 309       426  DUP_TOP          
              428  LOAD_FAST                'CommandError'
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   478  'to 478'
              436  POP_TOP          
              438  STORE_FAST               'e'
              440  POP_TOP          
              442  SETUP_FINALLY       466  'to 466'

 L. 310       444  LOAD_FAST                'cmd'
              446  LOAD_METHOD              on_help_command_error
              448  LOAD_FAST                'self'
              450  LOAD_FAST                'e'
              452  CALL_METHOD_2         2  ''
              454  GET_AWAITABLE    
              456  LOAD_CONST               None
              458  YIELD_FROM       
              460  POP_TOP          
              462  POP_BLOCK        
              464  BEGIN_FINALLY    
            466_0  COME_FROM_FINALLY   442  '442'
              466  LOAD_CONST               None
              468  STORE_FAST               'e'
              470  DELETE_FAST              'e'
              472  END_FINALLY      
              474  POP_EXCEPT       
              476  JUMP_FORWARD        480  'to 480'
            478_0  COME_FROM           432  '432'
              478  END_FINALLY      
            480_0  COME_FROM           476  '476'
            480_1  COME_FROM           424  '424'

Parse error at or near `POP_EXCEPT' instruction at offset 172