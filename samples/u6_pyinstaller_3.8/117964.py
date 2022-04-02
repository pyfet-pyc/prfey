# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\enums.py
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
import types
from collections import namedtuple
__all__ = ('Enum', 'ChannelType', 'MessageType', 'VoiceRegion', 'SpeakingState', 'VerificationLevel',
           'ContentFilter', 'Status', 'DefaultAvatar', 'RelationshipType', 'AuditLogAction',
           'AuditLogActionCategory', 'UserFlags', 'ActivityType', 'HypeSquadHouse',
           'NotificationLevel', 'PremiumType', 'UserContentFilter', 'FriendFlags',
           'TeamMembershipState', 'Theme', 'WebhookType')

def _create_value_cls(name):
    cls = namedtuple('_EnumValue_' + name, 'name value')
    cls.__repr__ = lambda self: '<%s.%s: %r>' % (name, self.name, self.value)
    cls.__str__ = lambda self: '%s.%s' % (name, self.name)
    return cls


def _is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class EnumMeta(type):

    def __new__(cls, name, bases, attrs):
        value_mapping = {}
        member_mapping = {}
        member_names = []
        value_cls = _create_value_cls(name)
        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == '_' and not is_descriptor:
                pass
            elif isinstance(value, classmethod):
                pass
            elif is_descriptor:
                setattr(value_cls, key, value)
                del attrs[key]
            else:
                try:
                    new_value = value_mapping[value]
                except KeyError:
                    new_value = value_cls(name=key, value=value)
                    value_mapping[value] = new_value
                    member_names.append(key)
                else:
                    member_mapping[key] = new_value
                    attrs[key] = new_value
        else:
            attrs['_enum_value_map_'] = value_mapping
            attrs['_enum_member_map_'] = member_mapping
            attrs['_enum_member_names_'] = member_names
            actual_cls = super().__new__(cls, name, bases, attrs)
            value_cls._actual_enum_cls_ = actual_cls
            return actual_cls

    def __iter__(cls):
        return (cls._enum_member_map_[name] for name in cls._enum_member_names_)

    def __reversed__(cls):
        return (cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_))

    def __len__(cls):
        return len(cls._enum_member_names_)

    def __repr__(cls):
        return '<enum %r>' % cls.__name__

    @property
    def __members__(cls):
        return types.MappingProxyType(cls._enum_member_map_)

    def __call__--- This code section failed: ---

 L. 119         0  SETUP_FINALLY        14  'to 14'

 L. 120         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _enum_value_map_
                6  LOAD_FAST                'value'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 121        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  LOAD_GLOBAL              TypeError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    54  'to 54'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 122        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 '%r is not a valid %s'
               36  LOAD_FAST                'value'
               38  LOAD_FAST                'cls'
               40  LOAD_ATTR                __name__
               42  BUILD_TUPLE_2         2 
               44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            24  '24'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'

Parse error at or near `POP_TOP' instruction at offset 28

    def __getitem__(cls, key):
        return cls._enum_member_map_[key]

    def __setattr__(cls, name, value):
        raise TypeError('Enums are immutable.')

    def __delattr__(cls, attr):
        raise TypeError('Enums are immutable')

    def __instancecheck__--- This code section failed: ---

 L. 136         0  SETUP_FINALLY        14  'to 14'

 L. 137         2  LOAD_FAST                'instance'
                4  LOAD_ATTR                _actual_enum_cls_
                6  LOAD_FAST                'self'
                8  COMPARE_OP               is
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 138        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 139        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


class Enum(metaclass=EnumMeta):

    @classmethod
    def try_value--- This code section failed: ---

 L. 144         0  SETUP_FINALLY        14  'to 14'

 L. 145         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _enum_value_map_
                6  LOAD_FAST                'value'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 146        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  LOAD_GLOBAL              TypeError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    40  'to 40'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 147        32  LOAD_FAST                'value'
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'
               40  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28


class ChannelType(Enum):
    text = 0
    private = 1
    voice = 2
    group = 3
    category = 4
    news = 5
    store = 6

    def __str__(self):
        return self.name


class MessageType(Enum):
    default = 0
    recipient_add = 1
    recipient_remove = 2
    call = 3
    channel_name_change = 4
    channel_icon_change = 5
    pins_add = 6
    new_member = 7
    premium_guild_subscription = 8
    premium_guild_tier_1 = 9
    premium_guild_tier_2 = 10
    premium_guild_tier_3 = 11
    channel_follow_add = 12


class VoiceRegion(Enum):
    us_west = 'us-west'
    us_east = 'us-east'
    us_south = 'us-south'
    us_central = 'us-central'
    eu_west = 'eu-west'
    eu_central = 'eu-central'
    singapore = 'singapore'
    london = 'london'
    sydney = 'sydney'
    amsterdam = 'amsterdam'
    frankfurt = 'frankfurt'
    brazil = 'brazil'
    hongkong = 'hongkong'
    russia = 'russia'
    japan = 'japan'
    southafrica = 'southafrica'
    india = 'india'
    europe = 'europe'
    dubai = 'dubai'
    vip_us_east = 'vip-us-east'
    vip_us_west = 'vip-us-west'
    vip_amsterdam = 'vip-amsterdam'

    def __str__(self):
        return self.value


class SpeakingState(Enum):
    none = 0
    voice = 1
    soundshare = 2
    priority = 4

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


class VerificationLevel(Enum):
    none = 0
    low = 1
    medium = 2
    high = 3
    table_flip = 3
    extreme = 4
    double_table_flip = 4

    def __str__(self):
        return self.name


class ContentFilter(Enum):
    disabled = 0
    no_role = 1
    all_members = 2

    def __str__(self):
        return self.name


class UserContentFilter(Enum):
    disabled = 0
    friends = 1
    all_messages = 2


class FriendFlags(Enum):
    noone = 0
    mutual_guilds = 1
    mutual_friends = 2
    guild_and_friends = 3
    everyone = 4


class Theme(Enum):
    light = 'light'
    dark = 'dark'


class Status(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    do_not_disturb = 'dnd'
    invisible = 'invisible'

    def __str__(self):
        return self.value


class DefaultAvatar(Enum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4

    def __str__(self):
        return self.name


class RelationshipType(Enum):
    friend = 1
    blocked = 2
    incoming_request = 3
    outgoing_request = 4


class NotificationLevel(Enum):
    all_messages = 0
    only_mentions = 1


class AuditLogActionCategory(Enum):
    create = 1
    delete = 2
    update = 3


class AuditLogAction(Enum):
    guild_update = 1
    channel_create = 10
    channel_update = 11
    channel_delete = 12
    overwrite_create = 13
    overwrite_update = 14
    overwrite_delete = 15
    kick = 20
    member_prune = 21
    ban = 22
    unban = 23
    member_update = 24
    member_role_update = 25
    member_move = 26
    member_disconnect = 27
    bot_add = 28
    role_create = 30
    role_update = 31
    role_delete = 32
    invite_create = 40
    invite_update = 41
    invite_delete = 42
    webhook_create = 50
    webhook_update = 51
    webhook_delete = 52
    emoji_create = 60
    emoji_update = 61
    emoji_delete = 62
    message_delete = 72
    message_bulk_delete = 73
    message_pin = 74
    message_unpin = 75
    integration_create = 80
    integration_update = 81
    integration_delete = 82

    @property
    def category(self):
        lookup = {AuditLogAction.guild_update: AuditLogActionCategory.update, 
         AuditLogAction.channel_create: AuditLogActionCategory.create, 
         AuditLogAction.channel_update: AuditLogActionCategory.update, 
         AuditLogAction.channel_delete: AuditLogActionCategory.delete, 
         AuditLogAction.overwrite_create: AuditLogActionCategory.create, 
         AuditLogAction.overwrite_update: AuditLogActionCategory.update, 
         AuditLogAction.overwrite_delete: AuditLogActionCategory.delete, 
         AuditLogAction.kick: None, 
         AuditLogAction.member_prune: None, 
         AuditLogAction.ban: None, 
         AuditLogAction.unban: None, 
         AuditLogAction.member_update: AuditLogActionCategory.update, 
         AuditLogAction.member_role_update: AuditLogActionCategory.update, 
         AuditLogAction.member_move: None, 
         AuditLogAction.member_disconnect: None, 
         AuditLogAction.bot_add: None, 
         AuditLogAction.role_create: AuditLogActionCategory.create, 
         AuditLogAction.role_update: AuditLogActionCategory.update, 
         AuditLogAction.role_delete: AuditLogActionCategory.delete, 
         AuditLogAction.invite_create: AuditLogActionCategory.create, 
         AuditLogAction.invite_update: AuditLogActionCategory.update, 
         AuditLogAction.invite_delete: AuditLogActionCategory.delete, 
         AuditLogAction.webhook_create: AuditLogActionCategory.create, 
         AuditLogAction.webhook_update: AuditLogActionCategory.update, 
         AuditLogAction.webhook_delete: AuditLogActionCategory.delete, 
         AuditLogAction.emoji_create: AuditLogActionCategory.create, 
         AuditLogAction.emoji_update: AuditLogActionCategory.update, 
         AuditLogAction.emoji_delete: AuditLogActionCategory.delete, 
         AuditLogAction.message_delete: AuditLogActionCategory.delete, 
         AuditLogAction.message_bulk_delete: AuditLogActionCategory.delete, 
         AuditLogAction.message_pin: None, 
         AuditLogAction.message_unpin: None, 
         AuditLogAction.integration_create: AuditLogActionCategory.create, 
         AuditLogAction.integration_update: AuditLogActionCategory.update, 
         AuditLogAction.integration_delete: AuditLogActionCategory.delete}
        return lookup[self]

    @property
    def target_type(self):
        v = self.value
        if v == -1:
            return 'all'
        if v < 10:
            return 'guild'
        if v < 20:
            return 'channel'
        if v < 30:
            return 'user'
        if v < 40:
            return 'role'
        if v < 50:
            return 'invite'
        if v < 60:
            return 'webhook'
        if v < 70:
            return 'emoji'
        if v < 80:
            return 'message'
        if v < 90:
            return 'integration'


class UserFlags(Enum):
    staff = 1
    partner = 2
    hypesquad = 4
    bug_hunter = 8
    hypesquad_bravery = 64
    hypesquad_brilliance = 128
    hypesquad_balance = 256
    early_supporter = 512
    team_user = 1024
    system = 4096


class ActivityType(Enum):
    unknown = -1
    playing = 0
    streaming = 1
    listening = 2
    watching = 3
    custom = 4

    def __int__(self):
        return self.value


class HypeSquadHouse(Enum):
    bravery = 1
    brilliance = 2
    balance = 3


class PremiumType(Enum):
    nitro_classic = 1
    nitro = 2


class TeamMembershipState(Enum):
    invited = 1
    accepted = 2


class WebhookType(Enum):
    incoming = 1
    channel_follower = 2


def try_enum--- This code section failed: ---

 L. 437         0  SETUP_FINALLY        14  'to 14'

 L. 438         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _enum_value_map_
                6  LOAD_FAST                'val'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 439        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  LOAD_GLOBAL              TypeError
               20  LOAD_GLOBAL              AttributeError
               22  BUILD_TUPLE_3         3 
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 440        34  LOAD_FAST                'val'
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30