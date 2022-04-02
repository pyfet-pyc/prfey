# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\errors.py
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
from discord.errors import DiscordException
__all__ = ('CommandError', 'MissingRequiredArgument', 'BadArgument', 'PrivateMessageOnly',
           'NoPrivateMessage', 'CheckFailure', 'CheckAnyFailure', 'CommandNotFound',
           'DisabledCommand', 'CommandInvokeError', 'TooManyArguments', 'UserInputError',
           'CommandOnCooldown', 'MaxConcurrencyReached', 'NotOwner', 'MissingRole',
           'BotMissingRole', 'MissingAnyRole', 'BotMissingAnyRole', 'MissingPermissions',
           'BotMissingPermissions', 'NSFWChannelRequired', 'ConversionError', 'BadUnionArgument',
           'ArgumentParsingError', 'UnexpectedQuoteError', 'InvalidEndOfQuotedStringError',
           'ExpectedClosingQuoteError', 'ExtensionError', 'ExtensionAlreadyLoaded',
           'ExtensionNotLoaded', 'NoEntryPointError', 'ExtensionFailed', 'ExtensionNotFound')

class CommandError(DiscordException):
    __doc__ = 'The base exception type for all command related errors.\n\n    This inherits from :exc:`discord.DiscordException`.\n\n    This exception and exceptions inherited from it are handled\n    in a special way as they are caught and passed into a special event\n    from :class:`.Bot`\\, :func:`on_command_error`.\n    '

    def __init__(self, message=None, *args):
        if message is not None:
            m = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')
            (super().__init__)(m, *args)
        else:
            (super().__init__)(*args)


class ConversionError(CommandError):
    __doc__ = 'Exception raised when a Converter class raises non-CommandError.\n\n    This inherits from :exc:`CommandError`.\n\n    Attributes\n    ----------\n    converter: :class:`discord.ext.commands.Converter`\n        The converter that failed.\n    original\n        The original exception that was raised. You can also get this via\n        the ``__cause__`` attribute.\n    '

    def __init__(self, converter, original):
        self.converter = converter
        self.original = original


class UserInputError(CommandError):
    __doc__ = 'The base exception type for errors that involve errors\n    regarding user input.\n\n    This inherits from :exc:`CommandError`.\n    '


class CommandNotFound(CommandError):
    __doc__ = 'Exception raised when a command is attempted to be invoked\n    but no command under that name is found.\n\n    This is not raised for invalid subcommands, rather just the\n    initial main command that is attempted to be invoked.\n\n    This inherits from :exc:`CommandError`.\n    '


class MissingRequiredArgument(UserInputError):
    __doc__ = 'Exception raised when parsing a command and a parameter\n    that is required is not encountered.\n\n    This inherits from :exc:`UserInputError`\n\n    Attributes\n    -----------\n    param: :class:`inspect.Parameter`\n        The argument that is missing.\n    '

    def __init__(self, param):
        self.param = param
        super().__init__('{0.name} is a required argument that is missing.'.format(param))


class TooManyArguments(UserInputError):
    __doc__ = 'Exception raised when the command was passed too many arguments and its\n    :attr:`.Command.ignore_extra` attribute was not set to ``True``.\n\n    This inherits from :exc:`UserInputError`\n    '


class BadArgument(UserInputError):
    __doc__ = 'Exception raised when a parsing or conversion failure is encountered\n    on an argument to pass into a command.\n\n    This inherits from :exc:`UserInputError`\n    '


class CheckFailure(CommandError):
    __doc__ = 'Exception raised when the predicates in :attr:`.Command.checks` have failed.\n\n    This inherits from :exc:`CommandError`\n    '


class CheckAnyFailure(CheckFailure):
    __doc__ = 'Exception raised when all predicates in :func:`check_any` fail.\n\n    This inherits from :exc:`CheckFailure`.\n\n    .. versionadded:: 1.3\n\n    Attributes\n    ------------\n    errors: List[:class:`CheckFailure`]\n        A list of errors that were caught during execution.\n    checks: List[Callable[[:class:`Context`], :class:`bool`]]\n        A list of check predicates that failed.\n    '

    def __init__(self, checks, errors):
        self.checks = checks
        self.errors = errors
        super().__init__('You do not have permission to run this command.')


class PrivateMessageOnly(CheckFailure):
    __doc__ = 'Exception raised when an operation does not work outside of private\n    message contexts.\n\n    This inherits from :exc:`CheckFailure`\n    '

    def __init__(self, message=None):
        super().__init__(message or 'This command can only be used in private messages.')


class NoPrivateMessage(CheckFailure):
    __doc__ = 'Exception raised when an operation does not work in private message\n    contexts.\n\n    This inherits from :exc:`CheckFailure`\n    '

    def __init__(self, message=None):
        super().__init__(message or 'This command cannot be used in private messages.')


class NotOwner(CheckFailure):
    __doc__ = 'Exception raised when the message author is not the owner of the bot.\n\n    This inherits from :exc:`CheckFailure`\n    '


class DisabledCommand(CommandError):
    __doc__ = 'Exception raised when the command being invoked is disabled.\n\n    This inherits from :exc:`CommandError`\n    '


class CommandInvokeError(CommandError):
    __doc__ = 'Exception raised when the command being invoked raised an exception.\n\n    This inherits from :exc:`CommandError`\n\n    Attributes\n    -----------\n    original\n        The original exception that was raised. You can also get this via\n        the ``__cause__`` attribute.\n    '

    def __init__(self, e):
        self.original = e
        super().__init__('Command raised an exception: {0.__class__.__name__}: {0}'.format(e))


class CommandOnCooldown(CommandError):
    __doc__ = 'Exception raised when the command being invoked is on cooldown.\n\n    This inherits from :exc:`CommandError`\n\n    Attributes\n    -----------\n    cooldown: Cooldown\n        A class with attributes ``rate``, ``per``, and ``type`` similar to\n        the :func:`.cooldown` decorator.\n    retry_after: :class:`float`\n        The amount of seconds to wait before you can retry again.\n    '

    def __init__(self, cooldown, retry_after):
        self.cooldown = cooldown
        self.retry_after = retry_after
        super().__init__('You are on cooldown. Try again in {:.2f}s'.format(retry_after))


class MaxConcurrencyReached(CommandError):
    __doc__ = 'Exception raised when the command being invoked has reached its maximum concurrency.\n\n    This inherits from :exc:`CommandError`.\n\n    Attributes\n    ------------\n    number: :class:`int`\n        The maximum number of concurrent invokers allowed.\n    per: :class:`BucketType`\n        The bucket type passed to the :func:`.max_concurrency` decorator.\n    '

    def __init__(self, number, per):
        self.number = number
        self.per = per
        name = per.name
        suffix = 'per %s' % name if per.name != 'default' else 'globally'
        plural = '%s times %s' if number > 1 else '%s time %s'
        fmt = plural % (number, suffix)
        super().__init__('Too many people using this command. It can only be used {} concurrently.'.format(fmt))


class MissingRole(CheckFailure):
    __doc__ = 'Exception raised when the command invoker lacks a role to run a command.\n\n    This inherits from :exc:`CheckFailure`\n\n    .. versionadded:: 1.1\n\n    Attributes\n    -----------\n    missing_role: Union[:class:`str`, :class:`int`]\n        The required role that is missing.\n        This is the parameter passed to :func:`~.commands.has_role`.\n    '

    def __init__(self, missing_role):
        self.missing_role = missing_role
        message = 'Role {0!r} is required to run this command.'.format(missing_role)
        super().__init__(message)


class BotMissingRole(CheckFailure):
    __doc__ = "Exception raised when the bot's member lacks a role to run a command.\n\n    This inherits from :exc:`CheckFailure`\n\n    .. versionadded:: 1.1\n\n    Attributes\n    -----------\n    missing_role: Union[:class:`str`, :class:`int`]\n        The required role that is missing.\n        This is the parameter passed to :func:`~.commands.has_role`.\n    "

    def __init__(self, missing_role):
        self.missing_role = missing_role
        message = 'Bot requires the role {0!r} to run this command'.format(missing_role)
        super().__init__(message)


class MissingAnyRole(CheckFailure):
    __doc__ = 'Exception raised when the command invoker lacks any of\n    the roles specified to run a command.\n\n    This inherits from :exc:`CheckFailure`\n\n    .. versionadded:: 1.1\n\n    Attributes\n    -----------\n    missing_roles: List[Union[:class:`str`, :class:`int`]]\n        The roles that the invoker is missing.\n        These are the parameters passed to :func:`~.commands.has_any_role`.\n    '

    def __init__(self, missing_roles):
        self.missing_roles = missing_roles
        missing = ["'{}'".format(role) for role in missing_roles]
        if len(missing) > 2:
            fmt = '{}, or {}'.format(', '.join(missing[:-1]), missing[(-1)])
        else:
            fmt = ' or '.join(missing)
        message = 'You are missing at least one of the required roles: {}'.format(fmt)
        super().__init__(message)


class BotMissingAnyRole(CheckFailure):
    __doc__ = "Exception raised when the bot's member lacks any of\n    the roles specified to run a command.\n\n    This inherits from :exc:`CheckFailure`\n\n    .. versionadded:: 1.1\n\n    Attributes\n    -----------\n    missing_roles: List[Union[:class:`str`, :class:`int`]]\n        The roles that the bot's member is missing.\n        These are the parameters passed to :func:`~.commands.has_any_role`.\n\n    "

    def __init__(self, missing_roles):
        self.missing_roles = missing_roles
        missing = ["'{}'".format(role) for role in missing_roles]
        if len(missing) > 2:
            fmt = '{}, or {}'.format(', '.join(missing[:-1]), missing[(-1)])
        else:
            fmt = ' or '.join(missing)
        message = 'Bot is missing at least one of the required roles: {}'.format(fmt)
        super().__init__(message)


class NSFWChannelRequired(CheckFailure):
    __doc__ = 'Exception raised when a channel does not have the required NSFW setting.\n\n    This inherits from :exc:`CheckFailure`.\n\n    .. versionadded:: 1.1\n\n    Parameters\n    -----------\n    channel: :class:`discord.abc.GuildChannel`\n        The channel that does not have NSFW enabled.\n    '

    def __init__(self, channel):
        self.channel = channel
        super().__init__("Channel '{}' needs to be NSFW for this command to work.".format(channel))


class MissingPermissions(CheckFailure):
    __doc__ = 'Exception raised when the command invoker lacks permissions to run a\n    command.\n\n    This inherits from :exc:`CheckFailure`\n\n    Attributes\n    -----------\n    missing_perms: :class:`list`\n        The required permissions that are missing.\n    '

    def __init__(self, missing_perms, *args):
        self.missing_perms = missing_perms
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format(', '.join(missing[:-1]), missing[(-1)])
        else:
            fmt = ' and '.join(missing)
        message = 'You are missing {} permission(s) to run this command.'.format(fmt)
        (super().__init__)(message, *args)


class BotMissingPermissions(CheckFailure):
    __doc__ = "Exception raised when the bot's member lacks permissions to run a\n    command.\n\n    This inherits from :exc:`CheckFailure`\n\n    Attributes\n    -----------\n    missing_perms: :class:`list`\n        The required permissions that are missing.\n    "

    def __init__(self, missing_perms, *args):
        self.missing_perms = missing_perms
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format(', '.join(missing[:-1]), missing[(-1)])
        else:
            fmt = ' and '.join(missing)
        message = 'Bot requires {} permission(s) to run this command.'.format(fmt)
        (super().__init__)(message, *args)


class BadUnionArgument(UserInputError):
    __doc__ = 'Exception raised when a :data:`typing.Union` converter fails for all\n    its associated types.\n\n    This inherits from :exc:`UserInputError`\n\n    Attributes\n    -----------\n    param: :class:`inspect.Parameter`\n        The parameter that failed being converted.\n    converters: Tuple[Type, ...]\n        A tuple of converters attempted in conversion, in order of failure.\n    errors: List[:class:`CommandError`]\n        A list of errors that were caught from failing the conversion.\n    '

    def __init__(self, param, converters, errors):
        self.param = param
        self.converters = converters
        self.errors = errors

        def _get_name--- This code section failed: ---

 L. 441         0  SETUP_FINALLY        10  'to 10'

 L. 442         2  LOAD_FAST                'x'
                4  LOAD_ATTR                __name__
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 443        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    36  'to 36'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 444        24  LOAD_FAST                'x'
               26  LOAD_ATTR                __class__
               28  LOAD_ATTR                __name__
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
             36_0  COME_FROM            16  '16'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 20

        to_string = [_get_name(x) for x in converters]
        if len(to_string) > 2:
            fmt = '{}, or {}'.format(', '.join(to_string[:-1]), to_string[(-1)])
        else:
            fmt = ' or '.join(to_string)
        super().__init__('Could not convert "{0.name}" into {1}.'.format(param, fmt))


class ArgumentParsingError(UserInputError):
    __doc__ = "An exception raised when the parser fails to parse a user's input.\n\n    This inherits from :exc:`UserInputError`.\n\n    There are child classes that implement more granular parsing errors for\n    i18n purposes.\n    "


class UnexpectedQuoteError(ArgumentParsingError):
    __doc__ = 'An exception raised when the parser encounters a quote mark inside a non-quoted string.\n\n    This inherits from :exc:`ArgumentParsingError`.\n\n    Attributes\n    ------------\n    quote: :class:`str`\n        The quote mark that was found inside the non-quoted string.\n    '

    def __init__(self, quote):
        self.quote = quote
        super().__init__('Unexpected quote mark, {0!r}, in non-quoted string'.format(quote))


class InvalidEndOfQuotedStringError(ArgumentParsingError):
    __doc__ = 'An exception raised when a space is expected after the closing quote in a string\n    but a different character is found.\n\n    This inherits from :exc:`ArgumentParsingError`.\n\n    Attributes\n    -----------\n    char: :class:`str`\n        The character found instead of the expected string.\n    '

    def __init__(self, char):
        self.char = char
        super().__init__('Expected space after closing quotation but received {0!r}'.format(char))


class ExpectedClosingQuoteError(ArgumentParsingError):
    __doc__ = 'An exception raised when a quote character is expected but not found.\n\n    This inherits from :exc:`ArgumentParsingError`.\n\n    Attributes\n    -----------\n    close_quote: :class:`str`\n        The quote character expected.\n    '

    def __init__(self, close_quote):
        self.close_quote = close_quote
        super().__init__('Expected closing {}.'.format(close_quote))


class ExtensionError(DiscordException):
    __doc__ = 'Base exception for extension related errors.\n\n    This inherits from :exc:`~discord.DiscordException`.\n\n    Attributes\n    ------------\n    name: :class:`str`\n        The extension that had an error.\n    '

    def __init__(self, message=None, *args, name):
        self.name = name
        message = message or 'Extension {!r} had an error.'.format(name)
        m = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')
        (super().__init__)(m, *args)


class ExtensionAlreadyLoaded(ExtensionError):
    __doc__ = 'An exception raised when an extension has already been loaded.\n\n    This inherits from :exc:`ExtensionError`\n    '

    def __init__(self, name):
        super().__init__(('Extension {!r} is already loaded.'.format(name)), name=name)


class ExtensionNotLoaded(ExtensionError):
    __doc__ = 'An exception raised when an extension was not loaded.\n\n    This inherits from :exc:`ExtensionError`\n    '

    def __init__(self, name):
        super().__init__(('Extension {!r} has not been loaded.'.format(name)), name=name)


class NoEntryPointError(ExtensionError):
    __doc__ = 'An exception raised when an extension does not have a ``setup`` entry point function.\n\n    This inherits from :exc:`ExtensionError`\n    '

    def __init__(self, name):
        super().__init__(("Extension {!r} has no 'setup' function.".format(name)), name=name)


class ExtensionFailed(ExtensionError):
    __doc__ = 'An exception raised when an extension failed to load during execution of the module or ``setup`` entry point.\n\n    This inherits from :exc:`ExtensionError`\n\n    Attributes\n    -----------\n    name: :class:`str`\n        The extension that had the error.\n    original: :exc:`Exception`\n        The original exception that was raised. You can also get this via\n        the ``__cause__`` attribute.\n    '

    def __init__(self, name, original):
        self.original = original
        fmt = 'Extension {0!r} raised an error: {1.__class__.__name__}: {1}'
        super().__init__((fmt.format(name, original)), name=name)


class ExtensionNotFound(ExtensionError):
    __doc__ = 'An exception raised when an extension is not found.\n\n    This inherits from :exc:`ExtensionError`\n\n    .. versionchanged:: 1.3\n        Made the ``original`` attribute always None.\n\n    Attributes\n    -----------\n    name: :class:`str`\n        The extension that had the error.\n    original: :class:`NoneType`\n        Always ``None`` for backwards compatibility.\n    '

    def __init__(self, name, original=None):
        self.original = None
        fmt = 'Extension {0!r} could not be loaded.'
        super().__init__((fmt.format(name)), name=name)