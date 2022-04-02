# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\permissions.py
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
from .flags import BaseFlags, flag_value, fill_with_flags
__all__ = ('Permissions', 'PermissionOverwrite')

class permission_alias(flag_value):
    pass


def make_permission_alias(alias):

    def decorator(func):
        ret = permission_alias(func)
        ret.alias = alias
        return ret

    return decorator


@fill_with_flags()
class Permissions(BaseFlags):
    __doc__ = "Wraps up the Discord permission value.\n\n    The properties provided are two way. You can set and retrieve individual\n    bits using the properties as if they were regular bools. This allows\n    you to edit permissions.\n\n    .. versionchanged:: 1.3\n        You can now use keyword arguments to initialize :class:`Permissions`\n        similar to :meth:`update`.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two permissions are equal.\n        .. describe:: x != y\n\n            Checks if two permissions are not equal.\n        .. describe:: x <= y\n\n            Checks if a permission is a subset of another permission.\n        .. describe:: x >= y\n\n            Checks if a permission is a superset of another permission.\n        .. describe:: x < y\n\n             Checks if a permission is a strict subset of another permission.\n        .. describe:: x > y\n\n             Checks if a permission is a strict superset of another permission.\n        .. describe:: hash(x)\n\n               Return the permission's hash.\n        .. describe:: iter(x)\n\n               Returns an iterator of ``(perm, value)`` pairs. This allows it\n               to be, for example, constructed as a dict or a list of pairs.\n               Note that aliases are not shown.\n\n    Attributes\n    -----------\n    value\n        The raw value. This value is a bit array field of a 53-bit integer\n        representing the currently available permissions. You should query\n        permissions via the properties rather than using this raw value.\n    "
    __slots__ = ()

    def __init__(self, permissions=0, **kwargs):
        if not isinstance(permissions, int):
            raise TypeError('Expected int parameter, received %s instead.' % permissions.__class__.__name__)
        self.value = permissions
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError('%r is not a valid permission name.' % key)
            else:
                setattr(self, key, value)

    def is_subset(self, other):
        """Returns ``True`` if self has the same or fewer permissions as other."""
        if isinstance(other, Permissions):
            return self.value & other.value == self.value
        raise TypeError('cannot compare {} with {}'.format(self.__class__.__name__, other.__class__.__name__))

    def is_superset(self, other):
        """Returns ``True`` if self has the same or more permissions as other."""
        if isinstance(other, Permissions):
            return self.value | other.value == self.value
        raise TypeError('cannot compare {} with {}'.format(self.__class__.__name__, other.__class__.__name__))

    def is_strict_subset(self, other):
        """Returns ``True`` if the permissions on other are a strict subset of those on self."""
        return self.is_subset(other) and self != other

    def is_strict_superset(self, other):
        """Returns ``True`` if the permissions on other are a strict superset of those on self."""
        return self.is_superset(other) and self != other

    __le__ = is_subset
    __ge__ = is_superset
    __lt__ = is_strict_subset
    __gt__ = is_strict_superset

    def __iter__(self):
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, permission_alias):
                pass
            else:
                if isinstance(value, flag_value):
                    yield (
                     name, self._has_flag(value.flag))

    @classmethod
    def none(cls):
        """A factory method that creates a :class:`Permissions` with all
        permissions set to ``False``."""
        return cls(0)

    @classmethod
    def all(cls):
        """A factory method that creates a :class:`Permissions` with all
        permissions set to True."""
        return cls(2147483647)

    @classmethod
    def all_channel(cls):
        """A :class:`Permissions` with all channel-specific permissions set to
        ``True`` and the guild-specific ones set to ``False``. The guild-specific
        permissions are currently:

        - manage_guild
        - kick_members
        - ban_members
        - administrator
        - change_nickname
        - manage_nicknames
        """
        return cls(871890001)

    @classmethod
    def general(cls):
        """A factory method that creates a :class:`Permissions` with all
        "General" permissions from the official Discord UI set to ``True``."""
        return cls(2080899263)

    @classmethod
    def text(cls):
        """A factory method that creates a :class:`Permissions` with all
        "Text" permissions from the official Discord UI set to ``True``."""
        return cls(523328)

    @classmethod
    def voice(cls):
        """A factory method that creates a :class:`Permissions` with all
        "Voice" permissions from the official Discord UI set to ``True``."""
        return cls(66061056)

    def update(self, **kwargs):
        r"""Bulk updates this permission object.

        Allows you to set multiple attributes by using keyword
        arguments. The names must be equivalent to the properties
        listed. Extraneous key/value pairs will be silently ignored.

        Parameters
        ------------
        \*\*kwargs
            A list of key/value pairs to bulk update permissions with.
        """
        for key, value in kwargs.items():
            if key in self.VALID_FLAGS:
                setattr(self, key, value)

    def handle_overwrite(self, allow, deny):
        self.value = self.value & ~deny | allow

    @flag_value
    def create_instant_invite(self):
        """:class:`bool`: Returns ``True`` if the user can create instant invites."""
        return 1

    @flag_value
    def kick_members(self):
        """:class:`bool`: Returns ``True`` if the user can kick users from the guild."""
        return 2

    @flag_value
    def ban_members(self):
        """:class:`bool`: Returns ``True`` if a user can ban users from the guild."""
        return 4

    @flag_value
    def administrator(self):
        """:class:`bool`: Returns ``True`` if a user is an administrator. This role overrides all other permissions.

        This also bypasses all channel-specific overrides.
        """
        return 8

    @flag_value
    def manage_channels(self):
        """:class:`bool`: Returns ``True`` if a user can edit, delete, or create channels in the guild.

        This also corresponds to the "Manage Channel" channel-specific override."""
        return 16

    @flag_value
    def manage_guild(self):
        """:class:`bool`: Returns ``True`` if a user can edit guild properties."""
        return 32

    @flag_value
    def add_reactions(self):
        """:class:`bool`: Returns ``True`` if a user can add reactions to messages."""
        return 64

    @flag_value
    def view_audit_log(self):
        """:class:`bool`: Returns ``True`` if a user can view the guild's audit log."""
        return 128

    @flag_value
    def priority_speaker(self):
        """:class:`bool`: Returns ``True`` if a user can be more easily heard while talking."""
        return 256

    @flag_value
    def stream(self):
        """:class:`bool`: Returns ``True`` if a user can stream in a voice channel."""
        return 512

    @flag_value
    def read_messages(self):
        """:class:`bool`: Returns ``True`` if a user can read messages from all or specific text channels."""
        return 1024

    @make_permission_alias('read_messages')
    def view_channel(self):
        """:class:`bool`: An alias for :attr:`read_messages`.

        .. versionadded:: 1.3
        """
        return 1024

    @flag_value
    def send_messages(self):
        """:class:`bool`: Returns ``True`` if a user can send messages from all or specific text channels."""
        return 2048

    @flag_value
    def send_tts_messages(self):
        """:class:`bool`: Returns ``True`` if a user can send TTS messages from all or specific text channels."""
        return 4096

    @flag_value
    def manage_messages(self):
        """:class:`bool`: Returns ``True`` if a user can delete or pin messages in a text channel.

        .. note::

            Note that there are currently no ways to edit other people's messages.
        """
        return 8192

    @flag_value
    def embed_links(self):
        """:class:`bool`: Returns ``True`` if a user's messages will automatically be embedded by Discord."""
        return 16384

    @flag_value
    def attach_files(self):
        """:class:`bool`: Returns ``True`` if a user can send files in their messages."""
        return 32768

    @flag_value
    def read_message_history(self):
        """:class:`bool`: Returns ``True`` if a user can read a text channel's previous messages."""
        return 65536

    @flag_value
    def mention_everyone(self):
        """:class:`bool`: Returns ``True`` if a user's @everyone or @here will mention everyone in the text channel."""
        return 131072

    @flag_value
    def external_emojis(self):
        """:class:`bool`: Returns ``True`` if a user can use emojis from other guilds."""
        return 262144

    @make_permission_alias('external_emojis')
    def use_external_emojis(self):
        """:class:`bool`: An alias for :attr:`external_emojis`.

        .. versionadded:: 1.3
        """
        return 262144

    @flag_value
    def view_guild_insights(self):
        """:class:`bool`: Returns ``True`` if a user can view the guild's insights.

        .. versionadded:: 1.3
        """
        return 524288

    @flag_value
    def connect(self):
        """:class:`bool`: Returns ``True`` if a user can connect to a voice channel."""
        return 1048576

    @flag_value
    def speak(self):
        """:class:`bool`: Returns ``True`` if a user can speak in a voice channel."""
        return 2097152

    @flag_value
    def mute_members(self):
        """:class:`bool`: Returns ``True`` if a user can mute other users."""
        return 4194304

    @flag_value
    def deafen_members(self):
        """:class:`bool`: Returns ``True`` if a user can deafen other users."""
        return 8388608

    @flag_value
    def move_members(self):
        """:class:`bool`: Returns ``True`` if a user can move users between other voice channels."""
        return 16777216

    @flag_value
    def use_voice_activation(self):
        """:class:`bool`: Returns ``True`` if a user can use voice activation in voice channels."""
        return 33554432

    @flag_value
    def change_nickname(self):
        """:class:`bool`: Returns ``True`` if a user can change their nickname in the guild."""
        return 67108864

    @flag_value
    def manage_nicknames(self):
        """:class:`bool`: Returns ``True`` if a user can change other user's nickname in the guild."""
        return 134217728

    @flag_value
    def manage_roles(self):
        """:class:`bool`: Returns ``True`` if a user can create or edit roles less than their role's position.

        This also corresponds to the "Manage Permissions" channel-specific override.
        """
        return 268435456

    @make_permission_alias('manage_roles')
    def manage_permissions(self):
        """:class:`bool`: An alias for :attr:`manage_roles`.

        .. versionadded:: 1.3
        """
        return 268435456

    @flag_value
    def manage_webhooks(self):
        """:class:`bool`: Returns ``True`` if a user can create, edit, or delete webhooks."""
        return 536870912

    @flag_value
    def manage_emojis(self):
        """:class:`bool`: Returns ``True`` if a user can create, edit, or delete emojis."""
        return 1073741824


def augment_from_permissions--- This code section failed: ---

 L. 419         0  LOAD_GLOBAL              set
                2  LOAD_GLOBAL              Permissions
                4  LOAD_ATTR                VALID_FLAGS
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'cls'
               10  STORE_ATTR               VALID_NAMES

 L. 420        12  LOAD_GLOBAL              set
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'aliases'

 L. 423        18  LOAD_GLOBAL              Permissions
               20  LOAD_ATTR                __dict__
               22  LOAD_METHOD              items
               24  CALL_METHOD_0         0  ''
               26  GET_ITER         
             28_0  COME_FROM           128  '128'
             28_1  COME_FROM            80  '80'
             28_2  COME_FROM            72  '72'
               28  FOR_ITER            130  'to 130'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'name'
               34  STORE_FAST               'value'

 L. 424        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'value'
               40  LOAD_GLOBAL              permission_alias
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    64  'to 64'

 L. 425        46  LOAD_FAST                'value'
               48  LOAD_ATTR                alias
               50  STORE_FAST               'key'

 L. 426        52  LOAD_FAST                'aliases'
               54  LOAD_METHOD              add
               56  LOAD_FAST                'name'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_FORWARD         82  'to 82'
             64_0  COME_FROM            44  '44'

 L. 427        64  LOAD_GLOBAL              isinstance
               66  LOAD_FAST                'value'
               68  LOAD_GLOBAL              flag_value
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L. 428        74  LOAD_FAST                'name'
               76  STORE_FAST               'key'
               78  JUMP_FORWARD         82  'to 82'

 L. 430        80  JUMP_BACK            28  'to 28'
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            62  '62'

 L. 433        82  LOAD_FAST                'key'
               84  BUILD_TUPLE_1         1 
               86  LOAD_CODE                <code_object getter>
               88  LOAD_STR                 'augment_from_permissions.<locals>.getter'
               90  MAKE_FUNCTION_1          'default'
               92  STORE_FAST               'getter'

 L. 435        94  LOAD_FAST                'key'
               96  BUILD_TUPLE_1         1 
               98  LOAD_CODE                <code_object setter>
              100  LOAD_STR                 'augment_from_permissions.<locals>.setter'
              102  MAKE_FUNCTION_1          'default'
              104  STORE_FAST               'setter'

 L. 438       106  LOAD_GLOBAL              property
              108  LOAD_FAST                'getter'
              110  LOAD_FAST                'setter'
              112  CALL_FUNCTION_2       2  ''
              114  STORE_FAST               'prop'

 L. 439       116  LOAD_GLOBAL              setattr
              118  LOAD_FAST                'cls'
              120  LOAD_FAST                'name'
              122  LOAD_FAST                'prop'
              124  CALL_FUNCTION_3       3  ''
              126  POP_TOP          
              128  JUMP_BACK            28  'to 28'
            130_0  COME_FROM            28  '28'

 L. 441       130  LOAD_FAST                'cls'
              132  LOAD_ATTR                VALID_NAMES
              134  LOAD_FAST                'aliases'
              136  BINARY_SUBTRACT  
              138  LOAD_FAST                'cls'
              140  STORE_ATTR               PURE_FLAGS

 L. 442       142  LOAD_FAST                'cls'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 80


@augment_from_permissions
class PermissionOverwrite:
    __doc__ = 'A type that is used to represent a channel specific permission.\n\n    Unlike a regular :class:`Permissions`\\, the default value of a\n    permission is equivalent to ``None`` and not ``False``. Setting\n    a value to ``False`` is **explicitly** denying that permission,\n    while setting a value to ``True`` is **explicitly** allowing\n    that permission.\n\n    The values supported by this are the same as :class:`Permissions`\n    with the added possibility of it being set to ``None``.\n\n    .. container:: operations\n\n        .. describe:: x == y\n\n            Checks if two overwrites are equal.\n        .. describe:: x != y\n\n            Checks if two overwrites are not equal.\n        .. describe:: iter(x)\n\n           Returns an iterator of ``(perm, value)`` pairs. This allows it\n           to be, for example, constructed as a dict or a list of pairs.\n           Note that aliases are not shown.\n\n    Parameters\n    -----------\n    \\*\\*kwargs\n        Set the value of permissions by their name.\n    '
    __slots__ = ('_values', )

    def __init__(self, **kwargs):
        self._values = {}
        for key, value in kwargs.items():
            if key not in self.VALID_NAMES:
                raise ValueError('no permission called {0}.'.format(key))
            else:
                setattr(self, key, value)

    def __eq__(self, other):
        return isinstance(other, PermissionOverwrite) and self._values == other._values

    def _set(self, key, value):
        if value not in (True, None, False):
            raise TypeError('Expected bool or NoneType, received {0.__class__.__name__}'.format(value))
        self._values[key] = value

    def pair(self):
        """Returns the (allow, deny) pair from this overwrite.

        The value of these pairs is :class:`Permissions`.
        """
        allow = Permissions.none()
        deny = Permissions.none()
        for key, value in self._values.items():
            if value is True:
                setattr(allow, key, True)
            else:
                if value is False:
                    setattr(deny, key, True)
        else:
            return (
             allow, deny)

    @classmethod
    def from_pair(cls, allow, deny):
        """Creates an overwrite from an allow/deny pair of :class:`Permissions`."""
        ret = cls()
        for key, value in allow:
            if value is True:
                setattr(ret, key, True)
        else:
            for key, value in deny:
                if value is True:
                    setattr(ret, key, False)
            else:
                return ret

    def is_empty(self):
        """Checks if the permission overwrite is currently empty.

        An empty permission overwrite is one that has no overwrites set
        to ``True`` or ``False``.
        """
        return all((x is None for x in self._values.values()))

    def update(self, **kwargs):
        r"""Bulk updates this permission overwrite object.

        Allows you to set multiple attributes by using keyword
        arguments. The names must be equivalent to the properties
        listed. Extraneous key/value pairs will be silently ignored.

        Parameters
        ------------
        \*\*kwargs
            A list of key/value pairs to bulk update with.
        """
        for key, value in kwargs.items():
            if key not in self.VALID_NAMES:
                pass
            else:
                setattr(self, key, value)

    def __iter__(self):
        for key in self.PURE_FLAGS:
            yield (
             key, self._values.get(key))