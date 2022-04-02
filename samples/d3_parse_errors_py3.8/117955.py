# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\audit_logs.py
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
from . import utils, enums
from .object import Object
from .permissions import PermissionOverwrite, Permissions
from .colour import Colour
from .invite import Invite

def _transform_verification_level(entry, data):
    return enums.try_enum(enums.VerificationLevel, data)


def _transform_default_notifications(entry, data):
    return enums.try_enum(enums.NotificationLevel, data)


def _transform_explicit_content_filter(entry, data):
    return enums.try_enum(enums.ContentFilter, data)


def _transform_permissions(entry, data):
    return Permissions(data)


def _transform_color(entry, data):
    return Colour(data)


def _transform_snowflake(entry, data):
    return int(data)


def _transform_channel(entry, data):
    if data is None:
        return
    channel = entry.guild.get_channel(int(data)) or Object(id=data)
    return channel


def _transform_owner_id(entry, data):
    if data is None:
        return
    return entry._get_member(int(data))


def _transform_inviter_id(entry, data):
    if data is None:
        return
    return entry._get_member(int(data))


def _transform_overwrites(entry, data):
    overwrites = []
    for elem in data:
        allow = Permissions(elem['allow'])
        deny = Permissions(elem['deny'])
        ow = PermissionOverwrite.from_pair(allow, deny)
        ow_type = elem['type']
        ow_id = int(elem['id'])
        if ow_type == 'role':
            target = entry.guild.get_role(ow_id)
        else:
            target = entry._get_member(ow_id)
        if target is None:
            target = Object(id=ow_id)
        else:
            overwrites.append((target, ow))
    else:
        return overwrites


class AuditLogDiff:

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__.items())

    def __repr__(self):
        values = ' '.join(('%s=%r' % item for item in self.__dict__.items()))
        return '<AuditLogDiff %s>' % values


class AuditLogChanges:
    TRANSFORMERS = {'verification_level':(
      None, _transform_verification_level), 
     'explicit_content_filter':(
      None, _transform_explicit_content_filter), 
     'allow':(
      None, _transform_permissions), 
     'deny':(
      None, _transform_permissions), 
     'permissions':(
      None, _transform_permissions), 
     'id':(
      None, _transform_snowflake), 
     'color':(
      'colour', _transform_color), 
     'owner_id':(
      'owner', _transform_owner_id), 
     'inviter_id':(
      'inviter', _transform_inviter_id), 
     'channel_id':(
      'channel', _transform_channel), 
     'afk_channel_id':(
      'afk_channel', _transform_channel), 
     'system_channel_id':(
      'system_channel', _transform_channel), 
     'widget_channel_id':(
      'widget_channel', _transform_channel), 
     'permission_overwrites':(
      'overwrites', _transform_overwrites), 
     'splash_hash':('splash', None), 
     'icon_hash':('icon', None), 
     'avatar_hash':('avatar', None), 
     'rate_limit_per_user':('slowmode_delay', None), 
     'default_message_notifications':(
      'default_notifications', _transform_default_notifications)}

    def __init__--- This code section failed: ---

 L. 123         0  LOAD_GLOBAL              AuditLogDiff
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_FAST                'self'
                6  STORE_ATTR               before

 L. 124         8  LOAD_GLOBAL              AuditLogDiff
               10  CALL_FUNCTION_0       0  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               after

 L. 126        16  LOAD_FAST                'data'
               18  GET_ITER         
             20_0  COME_FROM           266  '266'
             20_1  COME_FROM           100  '100'
             20_2  COME_FROM            64  '64'
               20  FOR_ITER            268  'to 268'
               22  STORE_FAST               'elem'

 L. 127        24  LOAD_FAST                'elem'
               26  LOAD_STR                 'key'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'attr'

 L. 130        32  LOAD_FAST                'attr'
               34  LOAD_STR                 '$add'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    68  'to 68'

 L. 131        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _handle_role
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                before
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                after
               52  LOAD_FAST                'entry'
               54  LOAD_FAST                'elem'
               56  LOAD_STR                 'new_value'
               58  BINARY_SUBSCR    
               60  CALL_METHOD_4         4  ''
               62  POP_TOP          

 L. 132        64  JUMP_BACK            20  'to 20'
               66  BREAK_LOOP          102  'to 102'
             68_0  COME_FROM            38  '38'

 L. 133        68  LOAD_FAST                'attr'
               70  LOAD_STR                 '$remove'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   102  'to 102'

 L. 134        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _handle_role
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                after
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                before
               88  LOAD_FAST                'entry'
               90  LOAD_FAST                'elem'
               92  LOAD_STR                 'new_value'
               94  BINARY_SUBSCR    
               96  CALL_METHOD_4         4  ''
               98  POP_TOP          

 L. 135       100  JUMP_BACK            20  'to 20'
            102_0  COME_FROM            74  '74'
            102_1  COME_FROM            66  '66'

 L. 137       102  LOAD_FAST                'self'
              104  LOAD_ATTR                TRANSFORMERS
              106  LOAD_METHOD              get
              108  LOAD_FAST                'attr'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'transformer'

 L. 138       114  LOAD_FAST                'transformer'
              116  POP_JUMP_IF_FALSE   134  'to 134'

 L. 139       118  LOAD_FAST                'transformer'
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'key'
              124  STORE_FAST               'transformer'

 L. 140       126  LOAD_FAST                'key'
              128  POP_JUMP_IF_FALSE   134  'to 134'

 L. 141       130  LOAD_FAST                'key'
              132  STORE_FAST               'attr'
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM           116  '116'

 L. 143       134  SETUP_FINALLY       148  'to 148'

 L. 144       136  LOAD_FAST                'elem'
              138  LOAD_STR                 'old_value'
              140  BINARY_SUBSCR    
              142  STORE_FAST               'before'
              144  POP_BLOCK        
              146  JUMP_FORWARD        172  'to 172'
            148_0  COME_FROM_FINALLY   134  '134'

 L. 145       148  DUP_TOP          
              150  LOAD_GLOBAL              KeyError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   170  'to 170'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 146       162  LOAD_CONST               None
              164  STORE_FAST               'before'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        186  'to 186'
            170_0  COME_FROM           154  '154'
              170  END_FINALLY      
            172_0  COME_FROM           146  '146'

 L. 148       172  LOAD_FAST                'transformer'
              174  POP_JUMP_IF_FALSE   186  'to 186'

 L. 149       176  LOAD_FAST                'transformer'
              178  LOAD_FAST                'entry'
              180  LOAD_FAST                'before'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'before'
            186_0  COME_FROM           174  '174'
            186_1  COME_FROM           168  '168'

 L. 151       186  LOAD_GLOBAL              setattr
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                before
              192  LOAD_FAST                'attr'
              194  LOAD_FAST                'before'
              196  CALL_FUNCTION_3       3  ''
              198  POP_TOP          

 L. 153       200  SETUP_FINALLY       214  'to 214'

 L. 154       202  LOAD_FAST                'elem'
              204  LOAD_STR                 'new_value'
              206  BINARY_SUBSCR    
              208  STORE_FAST               'after'
              210  POP_BLOCK        
              212  JUMP_FORWARD        238  'to 238'
            214_0  COME_FROM_FINALLY   200  '200'

 L. 155       214  DUP_TOP          
              216  LOAD_GLOBAL              KeyError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   236  'to 236'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 156       228  LOAD_CONST               None
              230  STORE_FAST               'after'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        252  'to 252'
            236_0  COME_FROM           220  '220'
              236  END_FINALLY      
            238_0  COME_FROM           212  '212'

 L. 158       238  LOAD_FAST                'transformer'
              240  POP_JUMP_IF_FALSE   252  'to 252'

 L. 159       242  LOAD_FAST                'transformer'
              244  LOAD_FAST                'entry'
              246  LOAD_FAST                'after'
              248  CALL_FUNCTION_2       2  ''
              250  STORE_FAST               'after'
            252_0  COME_FROM           240  '240'
            252_1  COME_FROM           234  '234'

 L. 161       252  LOAD_GLOBAL              setattr
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                after
              258  LOAD_FAST                'attr'
              260  LOAD_FAST                'after'
              262  CALL_FUNCTION_3       3  ''
              264  POP_TOP          
              266  JUMP_BACK            20  'to 20'
            268_0  COME_FROM            20  '20'

 L. 164       268  LOAD_GLOBAL              hasattr
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                after
              274  LOAD_STR                 'colour'
              276  CALL_FUNCTION_2       2  ''
          278_280  POP_JUMP_IF_FALSE   306  'to 306'

 L. 165       282  LOAD_FAST                'self'
              284  LOAD_ATTR                after
              286  LOAD_ATTR                colour
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                after
              292  STORE_ATTR               color

 L. 166       294  LOAD_FAST                'self'
              296  LOAD_ATTR                before
              298  LOAD_ATTR                colour
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                before
              304  STORE_ATTR               color
            306_0  COME_FROM           278  '278'

Parse error at or near `LOAD_GLOBAL' instruction at offset 268

    def __repr__(self):
        return '<AuditLogChanges before=%r after=%r>' % (self.before, self.after)

    def _handle_role(self, first, second, entry, elem):
        if not hasattr(first, 'roles'):
            setattrfirst'roles'[]
        data = []
        g = entry.guild
        for e in elem:
            role_id = int(e['id'])
            role = g.get_role(role_id)
            if role is None:
                role = Object(id=role_id)
                role.name = e['name']
            else:
                data.append(role)
        else:
            setattrsecond'roles'data


class AuditLogEntry:
    __doc__ = "Represents an Audit Log entry.\n\n    You retrieve these via :meth:`Guild.audit_logs`.\n\n    Attributes\n    -----------\n    action: :class:`AuditLogAction`\n        The action that was done.\n    user: :class:`abc.User`\n        The user who initiated this action. Usually a :class:`Member`\\, unless gone\n        then it's a :class:`User`.\n    id: :class:`int`\n        The entry ID.\n    target: Any\n        The target that got changed. The exact type of this depends on\n        the action being done.\n    reason: Optional[:class:`str`]\n        The reason this action was done.\n    extra: Any\n        Extra information that this entry has that might be useful.\n        For most actions, this is ``None``. However in some cases it\n        contains extra information. See :class:`AuditLogAction` for\n        which actions have this field filled out.\n    "

    def __init__(self, *, users, data, guild):
        self._state = guild._state
        self.guild = guild
        self._users = users
        self._from_data(data)

    def _from_data(self, data):
        self.action = enums.try_enum(enums.AuditLogAction, data['action_type'])
        self.id = int(data['id'])
        self.reason = data.get('reason')
        self.extra = data.get('options')
        if isinstance(self.action, enums.AuditLogAction):
            if self.extra:
                if self.action is enums.AuditLogAction.member_prune:
                    self.extra = type'_AuditLogProxy'(){int(v):k for k, v in self.extra.items()}
                elif self.action is enums.AuditLogAction.member_move or self.action is enums.AuditLogAction.message_delete:
                    channel_id = int(self.extra['channel_id'])
                    elems = {'count':int(self.extra['count']), 
                     'channel':self.guild.get_channel(channel_id) or Object(id=channel_id)}
                    self.extra = type'_AuditLogProxy'()elems
                elif self.action is enums.AuditLogAction.member_disconnect:
                    elems = {'count': int(self.extra['count'])}
                    self.extra = type'_AuditLogProxy'()elems
                elif self.action.name.endswith('pin'):
                    channel_id = int(self.extra['channel_id'])
                    message_id = int(self.extra['message_id'])
                    elems = {'channel':self.guild.get_channel(channel_id) or Object(id=channel_id), 
                     'message_id':message_id}
                    self.extra = type'_AuditLogProxy'()elems
                elif self.action.name.startswith('overwrite_'):
                    instance_id = int(self.extra['id'])
                    the_type = self.extra.get('type')
                    if the_type == 'member':
                        self.extra = self._get_member(instance_id)
                    else:
                        role = self.guild.get_role(instance_id)
                        if role is None:
                            role = Object(id=instance_id)
                            role.name = self.extra.get('role_name')
                        self.extra = role
        self._changes = data.get('changes', [])
        self.user = self._get_member(utils._get_as_snowflake(data, 'user_id'))
        self._target_id = utils._get_as_snowflake(data, 'target_id')

    def _get_member(self, user_id):
        return self.guild.get_member(user_id) or self._users.get(user_id)

    def __repr__(self):
        return '<AuditLogEntry id={0.id} action={0.action} user={0.user!r}>'.format(self)

    @utils.cached_property
    def created_at(self):
        """:class:`datetime.datetime`: Returns the entry's creation time in UTC."""
        return utils.snowflake_time(self.id)

    @utils.cached_property
    def target(self):
        try:
            converter = getattr(self, '_convert_target_' + self.action.target_type)
        except AttributeError:
            return Object(id=(self._target_id))
        else:
            return converter(self._target_id)

    @utils.cached_property
    def category(self):
        """Optional[:class:`AuditLogActionCategory`]: The category of the action, if applicable."""
        return self.action.category

    @utils.cached_property
    def changes(self):
        """:class:`AuditLogChanges`: The list of changes this entry has."""
        obj = AuditLogChanges(self, self._changes)
        del self._changes
        return obj

    @utils.cached_property
    def before(self):
        """:class:`AuditLogDiff`: The target's prior state."""
        return self.changes.before

    @utils.cached_property
    def after(self):
        """:class:`AuditLogDiff`: The target's subsequent state."""
        return self.changes.after

    def _convert_target_guild(self, target_id):
        return self.guild

    def _convert_target_channel(self, target_id):
        ch = self.guild.get_channel(target_id)
        if ch is None:
            return Object(id=target_id)
        return ch

    def _convert_target_user(self, target_id):
        return self._get_member(target_id)

    def _convert_target_role(self, target_id):
        role = self.guild.get_role(target_id)
        if role is None:
            return Object(id=target_id)
        return role

    def _convert_target_invite(self, target_id):
        changeset = self.before if self.action is enums.AuditLogAction.invite_delete else self.after
        fake_payload = {'max_age':changeset.max_age, 
         'max_uses':changeset.max_uses, 
         'code':changeset.code, 
         'temporary':changeset.temporary, 
         'channel':changeset.channel, 
         'uses':changeset.uses, 
         'guild':self.guild}
        obj = Invite(state=(self._state), data=fake_payload)
        try:
            obj.inviter = changeset.inviter
        except AttributeError:
            pass
        else:
            return obj

    def _convert_target_emoji(self, target_id):
        return self._state.get_emoji(target_id) or Object(id=target_id)

    def _convert_target_message(self, target_id):
        return self._get_member(target_id)