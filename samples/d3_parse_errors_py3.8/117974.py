# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\message.py
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
import asyncio, datetime, re, io
from . import utils
from .reaction import Reaction
from .emoji import Emoji
from .partial_emoji import PartialEmoji
from .calls import CallMessage
from .enums import MessageType, try_enum
from .errors import InvalidArgument, ClientException, HTTPException
from .embeds import Embed
from .member import Member
from .flags import MessageFlags
from .file import File
from .utils import escape_mentions
from .guild import Guild

class Attachment:
    __doc__ = "Represents an attachment from Discord.\n\n    Attributes\n    ------------\n    id: :class:`int`\n        The attachment ID.\n    size: :class:`int`\n        The attachment size in bytes.\n    height: Optional[:class:`int`]\n        The attachment's height, in pixels. Only applicable to images and videos.\n    width: Optional[:class:`int`]\n        The attachment's width, in pixels. Only applicable to images and videos.\n    filename: :class:`str`\n        The attachment's filename.\n    url: :class:`str`\n        The attachment URL. If the message this attachment was attached\n        to is deleted, then this will 404.\n    proxy_url: :class:`str`\n        The proxy URL. This is a cached version of the :attr:`~Attachment.url` in the\n        case of images. When the message is deleted, this URL might be valid for a few\n        minutes or not valid at all.\n    "
    __slots__ = ('id', 'size', 'height', 'width', 'filename', 'url', 'proxy_url', '_http')

    def __init__(self, *, data, state):
        self.id = int(data['id'])
        self.size = data['size']
        self.height = data.get('height')
        self.width = data.get('width')
        self.filename = data['filename']
        self.url = data.get('url')
        self.proxy_url = data.get('proxy_url')
        self._http = state.http

    def is_spoiler(self):
        """:class:`bool`: Whether this attachment contains a spoiler."""
        return self.filename.startswith('SPOILER_')

    def __repr__(self):
        return '<Attachment id={0.id} filename={0.filename!r} url={0.url!r}>'.format(self)

    async def save(self, fp, *, seek_begin=True, use_cached=False):
        """|coro|

        Saves this attachment into a file-like object.

        Parameters
        -----------
        fp: Union[:class:`io.BufferedIOBase`, :class:`os.PathLike`]
            The file-like object to save this attachment to or the filename
            to use. If a filename is passed then a file is created with that
            filename and used instead.
        seek_begin: :class:`bool`
            Whether to seek to the beginning of the file after saving is
            successfully done.
        use_cached: :class:`bool`
            Whether to use :attr:`proxy_url` rather than :attr:`url` when downloading
            the attachment. This will allow attachments to be saved after deletion
            more often, compared to the regular URL which is generally deleted right
            after the message is deleted. Note that this can still fail to download
            deleted attachments if too much time has passed and it does not work
            on some types of attachments.

        Raises
        --------
        HTTPException
            Saving the attachment failed.
        NotFound
            The attachment was deleted.

        Returns
        --------
        :class:`int`
            The number of bytes written.
        """
        data = await self.read(use_cached=use_cached)
        if isinstance(fp, io.IOBase):
            if fp.writable():
                written = fp.write(data)
                if seek_begin:
                    fp.seek(0)
                return written
        with open(fp, 'wb') as f:
            return f.write(data)

    async def read(self, *, use_cached=False):
        """|coro|

        Retrieves the content of this attachment as a :class:`bytes` object.

        .. versionadded:: 1.1

        Parameters
        -----------
        use_cached: :class:`bool`
            Whether to use :attr:`proxy_url` rather than :attr:`url` when downloading
            the attachment. This will allow attachments to be saved after deletion
            more often, compared to the regular URL which is generally deleted right
            after the message is deleted. Note that this can still fail to download
            deleted attachments if too much time has passed and it does not work
            on some types of attachments.

        Raises
        ------
        HTTPException
            Downloading the attachment failed.
        Forbidden
            You do not have permissions to access this attachment
        NotFound
            The attachment was deleted.

        Returns
        -------
        :class:`bytes`
            The contents of the attachment.
        """
        url = self.proxy_url if use_cached else self.url
        data = await self._http.get_from_cdn(url)
        return data

    async def to_file(self):
        """|coro|

        Converts the attachment into a :class:`File` suitable for sending via
        :meth:`abc.Messageable.send`.

        .. versionadded:: 1.3

        Raises
        ------
        HTTPException
            Downloading the attachment failed.
        Forbidden
            You do not have permissions to access this attachment
        NotFound
            The attachment was deleted.

        Returns
        -------
        :class:`File`
            The attachment as a file suitable for sending.
        """
        data = await self.read()
        return File((io.BytesIO(data)), filename=(self.filename))


def flatten_handlers(cls):
    prefix = len('_handle_')
    cls._HANDLERS = {value:key[prefix:] for key, value in cls.__dict__.items() if key.startswith('_handle_')}
    cls._CACHED_SLOTS = [attr for attr in cls.__slots__ if attr.startswith('_cs_')]
    return cls


@flatten_handlers
class Message:
    __doc__ = "Represents a message from Discord.\n\n    There should be no need to create one of these manually.\n\n    Attributes\n    -----------\n    tts: :class:`bool`\n        Specifies if the message was done with text-to-speech.\n        This can only be accurately received in :func:`on_message` due to\n        a discord limitation.\n    type: :class:`MessageType`\n        The type of message. In most cases this should not be checked, but it is helpful\n        in cases where it might be a system message for :attr:`system_content`.\n    author: :class:`abc.User`\n        A :class:`Member` that sent the message. If :attr:`channel` is a\n        private channel or the user has the left the guild, then it is a :class:`User` instead.\n    content: :class:`str`\n        The actual contents of the message.\n    nonce\n        The value used by the discord guild and the client to verify that the message is successfully sent.\n        This is typically non-important.\n    embeds: List[:class:`Embed`]\n        A list of embeds the message has.\n    channel: Union[:class:`abc.Messageable`]\n        The :class:`TextChannel` that the message was sent from.\n        Could be a :class:`DMChannel` or :class:`GroupChannel` if it's a private message.\n    call: Optional[:class:`CallMessage`]\n        The call that the message refers to. This is only applicable to messages of type\n        :attr:`MessageType.call`.\n    mention_everyone: :class:`bool`\n        Specifies if the message mentions everyone.\n\n        .. note::\n\n            This does not check if the ``@everyone`` or the ``@here`` text is in the message itself.\n            Rather this boolean indicates if either the ``@everyone`` or the ``@here`` text is in the message\n            **and** it did end up mentioning.\n    mentions: List[:class:`abc.User`]\n        A list of :class:`Member` that were mentioned. If the message is in a private message\n        then the list will be of :class:`User` instead. For messages that are not of type\n        :attr:`MessageType.default`\\, this array can be used to aid in system messages.\n        For more information, see :attr:`system_content`.\n\n        .. warning::\n\n            The order of the mentions list is not in any particular order so you should\n            not rely on it. This is a discord limitation, not one with the library.\n    channel_mentions: List[:class:`abc.GuildChannel`]\n        A list of :class:`abc.GuildChannel` that were mentioned. If the message is in a private message\n        then the list is always empty.\n    role_mentions: List[:class:`Role`]\n        A list of :class:`Role` that were mentioned. If the message is in a private message\n        then the list is always empty.\n    id: :class:`int`\n        The message ID.\n    webhook_id: Optional[:class:`int`]\n        If this message was sent by a webhook, then this is the webhook ID's that sent this\n        message.\n    attachments: List[:class:`Attachment`]\n        A list of attachments given to a message.\n    pinned: :class:`bool`\n        Specifies if the message is currently pinned.\n    flags: :class:`MessageFlags`\n        Extra features of the message.\n\n        .. versionadded:: 1.3\n\n    reactions : List[:class:`Reaction`]\n        Reactions to a message. Reactions can be either custom emoji or standard unicode emoji.\n    activity: Optional[:class:`dict`]\n        The activity associated with this message. Sent with Rich-Presence related messages that for\n        example, request joining, spectating, or listening to or with another member.\n\n        It is a dictionary with the following optional keys:\n\n        - ``type``: An integer denoting the type of message activity being requested.\n        - ``party_id``: The party ID associated with the party.\n    application: Optional[:class:`dict`]\n        The rich presence enabled application associated with this message.\n\n        It is a dictionary with the following keys:\n\n        - ``id``: A string representing the application's ID.\n        - ``name``: A string representing the application's name.\n        - ``description``: A string representing the application's description.\n        - ``icon``: A string representing the icon ID of the application.\n        - ``cover_image``: A string representing the embed's image asset ID.\n    "
    __slots__ = ('_edited_timestamp', 'tts', 'content', 'channel', 'webhook_id', 'mention_everyone',
                 'embeds', 'id', 'mentions', 'author', '_cs_channel_mentions', '_cs_raw_mentions',
                 'attachments', '_cs_clean_content', '_cs_raw_channel_mentions',
                 'nonce', 'pinned', 'role_mentions', '_cs_raw_role_mentions', 'type',
                 'call', 'flags', '_cs_system_content', '_cs_guild', '_state', 'reactions',
                 'application', 'activity')

    def __init__--- This code section failed: ---

 L. 307         0  LOAD_FAST                'state'
                2  LOAD_DEREF               'self'
                4  STORE_ATTR               _state

 L. 308         6  LOAD_GLOBAL              int
                8  LOAD_FAST                'data'
               10  LOAD_STR                 'id'
               12  BINARY_SUBSCR    
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_DEREF               'self'
               18  STORE_ATTR               id

 L. 309        20  LOAD_GLOBAL              utils
               22  LOAD_METHOD              _get_as_snowflake
               24  LOAD_FAST                'data'
               26  LOAD_STR                 'webhook_id'
               28  CALL_METHOD_2         2  ''
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               webhook_id

 L. 310        34  LOAD_CLOSURE             'self'
               36  BUILD_TUPLE_1         1 
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'Message.__init__.<locals>.<listcomp>'
               42  MAKE_FUNCTION_8          'closure'
               44  LOAD_FAST                'data'
               46  LOAD_METHOD              get
               48  LOAD_STR                 'reactions'
               50  BUILD_LIST_0          0 
               52  CALL_METHOD_2         2  ''
               54  GET_ITER         
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_DEREF               'self'
               60  STORE_ATTR               reactions

 L. 311        62  LOAD_CLOSURE             'self'
               64  BUILD_TUPLE_1         1 
               66  LOAD_LISTCOMP            '<code_object <listcomp>>'
               68  LOAD_STR                 'Message.__init__.<locals>.<listcomp>'
               70  MAKE_FUNCTION_8          'closure'
               72  LOAD_FAST                'data'
               74  LOAD_STR                 'attachments'
               76  BINARY_SUBSCR    
               78  GET_ITER         
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_DEREF               'self'
               84  STORE_ATTR               attachments

 L. 312        86  LOAD_LISTCOMP            '<code_object <listcomp>>'
               88  LOAD_STR                 'Message.__init__.<locals>.<listcomp>'
               90  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               92  LOAD_FAST                'data'
               94  LOAD_STR                 'embeds'
               96  BINARY_SUBSCR    
               98  GET_ITER         
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_DEREF               'self'
              104  STORE_ATTR               embeds

 L. 313       106  LOAD_FAST                'data'
              108  LOAD_METHOD              get
              110  LOAD_STR                 'application'
              112  CALL_METHOD_1         1  ''
              114  LOAD_DEREF               'self'
              116  STORE_ATTR               application

 L. 314       118  LOAD_FAST                'data'
              120  LOAD_METHOD              get
              122  LOAD_STR                 'activity'
              124  CALL_METHOD_1         1  ''
              126  LOAD_DEREF               'self'
              128  STORE_ATTR               activity

 L. 315       130  LOAD_FAST                'channel'
              132  LOAD_DEREF               'self'
              134  STORE_ATTR               channel

 L. 316       136  LOAD_GLOBAL              utils
              138  LOAD_METHOD              parse_time
              140  LOAD_FAST                'data'
              142  LOAD_STR                 'edited_timestamp'
              144  BINARY_SUBSCR    
              146  CALL_METHOD_1         1  ''
              148  LOAD_DEREF               'self'
              150  STORE_ATTR               _edited_timestamp

 L. 317       152  LOAD_GLOBAL              try_enum
              154  LOAD_GLOBAL              MessageType
              156  LOAD_FAST                'data'
              158  LOAD_STR                 'type'
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_2       2  ''
              164  LOAD_DEREF               'self'
              166  STORE_ATTR               type

 L. 318       168  LOAD_FAST                'data'
              170  LOAD_STR                 'pinned'
              172  BINARY_SUBSCR    
              174  LOAD_DEREF               'self'
              176  STORE_ATTR               pinned

 L. 319       178  LOAD_GLOBAL              MessageFlags
              180  LOAD_METHOD              _from_value
              182  LOAD_FAST                'data'
              184  LOAD_METHOD              get
              186  LOAD_STR                 'flags'
              188  LOAD_CONST               0
              190  CALL_METHOD_2         2  ''
              192  CALL_METHOD_1         1  ''
              194  LOAD_DEREF               'self'
              196  STORE_ATTR               flags

 L. 320       198  LOAD_FAST                'data'
              200  LOAD_STR                 'mention_everyone'
              202  BINARY_SUBSCR    
              204  LOAD_DEREF               'self'
              206  STORE_ATTR               mention_everyone

 L. 321       208  LOAD_FAST                'data'
              210  LOAD_STR                 'tts'
              212  BINARY_SUBSCR    
              214  LOAD_DEREF               'self'
              216  STORE_ATTR               tts

 L. 322       218  LOAD_FAST                'data'
              220  LOAD_STR                 'content'
              222  BINARY_SUBSCR    
              224  LOAD_DEREF               'self'
              226  STORE_ATTR               content

 L. 323       228  LOAD_FAST                'data'
              230  LOAD_METHOD              get
              232  LOAD_STR                 'nonce'
              234  CALL_METHOD_1         1  ''
              236  LOAD_DEREF               'self'
              238  STORE_ATTR               nonce

 L. 325       240  LOAD_CONST               ('author', 'member', 'mentions', 'mention_roles', 'call', 'flags')
              242  GET_ITER         
            244_0  COME_FROM           302  '302'
            244_1  COME_FROM           298  '298'
            244_2  COME_FROM           294  '294'
            244_3  COME_FROM           274  '274'
              244  FOR_ITER            304  'to 304'
              246  STORE_FAST               'handler'

 L. 326       248  SETUP_FINALLY       276  'to 276'

 L. 327       250  LOAD_GLOBAL              getattr
              252  LOAD_DEREF               'self'
              254  LOAD_STR                 '_handle_%s'
              256  LOAD_FAST                'handler'
              258  BINARY_MODULO    
              260  CALL_FUNCTION_2       2  ''
              262  LOAD_FAST                'data'
              264  LOAD_FAST                'handler'
              266  BINARY_SUBSCR    
              268  CALL_FUNCTION_1       1  ''
              270  POP_TOP          
              272  POP_BLOCK        
              274  JUMP_BACK           244  'to 244'
            276_0  COME_FROM_FINALLY   248  '248'

 L. 328       276  DUP_TOP          
              278  LOAD_GLOBAL              KeyError
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   300  'to 300'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L. 329       292  POP_EXCEPT       
              294  JUMP_BACK           244  'to 244'
              296  POP_EXCEPT       
              298  JUMP_BACK           244  'to 244'
            300_0  COME_FROM           282  '282'
              300  END_FINALLY      
              302  JUMP_BACK           244  'to 244'
            304_0  COME_FROM           244  '244'

Parse error at or near `JUMP_BACK' instruction at offset 298

    def __repr__(self):
        return '<Message id={0.id} channel={0.channel!r} type={0.type!r} author={0.author!r} flags={0.flags!r}>'.format(self)

    def _try_patch(self, data, key, transform=None):
        try:
            value = data[key]
        except KeyError:
            pass
        else:
            if transform is None:
                setattr(self, key, value)
            else:
                setattr(self, key, transform(value))

    def _add_reaction(self, data, emoji, user_id):
        reaction = utils.find(lambda r: r.emoji == emoji)self.reactions
        is_me = data['me'] = user_id == self._state.self_id
        if reaction is None:
            reaction = Reaction(message=self, data=data, emoji=emoji)
            self.reactions.append(reaction)
        else:
            reaction.count += 1
            if is_me:
                reaction.me = is_me
        return reaction

    def _remove_reaction(self, data, emoji, user_id):
        reaction = utils.find(lambda r: r.emoji == emoji)self.reactions
        if reaction is None:
            raise ValueError('Emoji already removed?')
        reaction.count -= 1
        if user_id == self._state.self_id:
            reaction.me = False
        if reaction.count == 0:
            self.reactions.remove(reaction)
        return reaction

    def _clear_emoji--- This code section failed: ---

 L. 379         0  LOAD_GLOBAL              str
                2  LOAD_FAST                'emoji'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'to_check'

 L. 380         8  LOAD_GLOBAL              enumerate
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                reactions
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
             18_0  COME_FROM            44  '44'
             18_1  COME_FROM            38  '38'
               18  FOR_ITER             46  'to 46'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'index'
               24  STORE_FAST               'reaction'

 L. 381        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'reaction'
               30  LOAD_ATTR                emoji
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'to_check'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 382        40  POP_TOP          
               42  BREAK_LOOP           50  'to 50'
               44  JUMP_BACK            18  'to 18'
             46_0  COME_FROM            18  '18'

 L. 385        46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            42  '42'

 L. 387        50  LOAD_FAST                'self'
               52  LOAD_ATTR                reactions
               54  LOAD_FAST                'index'
               56  DELETE_SUBSCR    

 L. 388        58  LOAD_FAST                'reaction'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 60

    def _update--- This code section failed: ---

 L. 391         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _HANDLERS
                4  STORE_FAST               'handlers'

 L. 392         6  LOAD_FAST                'data'
                8  LOAD_METHOD              items
               10  CALL_METHOD_0         0  ''
               12  GET_ITER         
             14_0  COME_FROM            70  '70'
             14_1  COME_FROM            56  '56'
             14_2  COME_FROM            52  '52'
               14  FOR_ITER             72  'to 72'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'key'
               20  STORE_FAST               'value'

 L. 393        22  SETUP_FINALLY        36  'to 36'

 L. 394        24  LOAD_FAST                'handlers'
               26  LOAD_FAST                'key'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'handler'
               32  POP_BLOCK        
               34  JUMP_FORWARD         60  'to 60'
             36_0  COME_FROM_FINALLY    22  '22'

 L. 395        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 396        50  POP_EXCEPT       
               52  JUMP_BACK            14  'to 14'
               54  POP_EXCEPT       
               56  JUMP_BACK            14  'to 14'
             58_0  COME_FROM            42  '42'
               58  END_FINALLY      
             60_0  COME_FROM            34  '34'

 L. 398        60  LOAD_FAST                'handler'
               62  LOAD_FAST                'self'
               64  LOAD_FAST                'value'
               66  CALL_FUNCTION_2       2  ''
               68  POP_TOP          
               70  JUMP_BACK            14  'to 14'
             72_0  COME_FROM            14  '14'

 L. 401        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _CACHED_SLOTS
               76  GET_ITER         
             78_0  COME_FROM           118  '118'
             78_1  COME_FROM           114  '114'
             78_2  COME_FROM            96  '96'
               78  FOR_ITER            120  'to 120'
               80  STORE_FAST               'attr'

 L. 402        82  SETUP_FINALLY        98  'to 98'

 L. 403        84  LOAD_GLOBAL              delattr
               86  LOAD_FAST                'self'
               88  LOAD_FAST                'attr'
               90  CALL_FUNCTION_2       2  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  JUMP_BACK            78  'to 78'
             98_0  COME_FROM_FINALLY    82  '82'

 L. 404        98  DUP_TOP          
              100  LOAD_GLOBAL              AttributeError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   116  'to 116'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 405       112  POP_EXCEPT       
              114  JUMP_BACK            78  'to 78'
            116_0  COME_FROM           104  '104'
              116  END_FINALLY      
              118  JUMP_BACK            78  'to 78'
            120_0  COME_FROM            78  '78'

Parse error at or near `JUMP_BACK' instruction at offset 56

    def _handle_edited_timestamp(self, value):
        self._edited_timestamp = utils.parse_time(value)

    def _handle_pinned(self, value):
        self.pinned = value

    def _handle_flags(self, value):
        self.flags = MessageFlags._from_value(value)

    def _handle_application(self, value):
        self.application = value

    def _handle_activity(self, value):
        self.activity = value

    def _handle_mention_everyone(self, value):
        self.mention_everyone = value

    def _handle_tts(self, value):
        self.tts = value

    def _handle_type(self, value):
        self.type = try_enum(MessageType, value)

    def _handle_content(self, value):
        self.content = value

    def _handle_attachments(self, value):
        self.attachments = [Attachment(data=a, state=(self._state)) for a in value]

    def _handle_embeds(self, value):
        self.embeds = [Embed.from_dict(data) for data in value]

    def _handle_nonce(self, value):
        self.nonce = value

    def _handle_author(self, author):
        self.author = self._state.store_user(author)
        if isinstance(self.guild, Guild):
            found = self.guild.get_member(self.author.id)
            if found is not None:
                self.author = found

    def _handle_member(self, member):
        author = self.author
        try:
            if author.joined_at is None:
                author.joined_at = utils.parse_time(member.get('joined_at'))
        except AttributeError:
            self.author = Member._from_message(message=self, data=member)

    def _handle_mentions(self, mentions):
        self.mentions = r = []
        guild = self.guild
        state = self._state
        if not isinstance(guild, Guild):
            self.mentions = [state.store_user(m) for m in mentions]
            return
        for mention in filter(None, mentions):
            id_search = int(mention['id'])
            member = guild.get_member(id_search)
            if member is not None:
                r.append(member)
            else:
                r.append(Member._try_upgrade(data=mention, guild=guild, state=state))

    def _handle_mention_roles(self, role_mentions):
        self.role_mentions = []
        if isinstance(self.guild, Guild):
            for role_id in map(int, role_mentions):
                role = self.guild.get_role(role_id)
                if role is not None:
                    self.role_mentions.append(role)

    def _handle_call(self, call):
        if call is None or (self.type is not MessageType.call):
            self.call = None
            return
        participants = []
        for uid in map(int, call.get'participants'[]):
            if uid == self.author.id:
                participants.append(self.author)
            else:
                user = utils.find(lambda u: u.id == uid)self.mentions
                if user is not None:
                    participants.append(user)
        else:
            call['participants'] = participants
            self.call = CallMessage(message=self, **call)

    @utils.cached_slot_property('_cs_guild')
    def guild(self):
        """Optional[:class:`Guild`]: The guild that the message belongs to, if applicable."""
        return getattr(self.channel, 'guild', None)

    @utils.cached_slot_property('_cs_raw_mentions')
    def raw_mentions(self):
        """List[:class:`int`]: A property that returns an array of user IDs matched with
        the syntax of ``<@user_id>`` in the message content.

        This allows you to receive the user IDs of mentioned users
        even in a private message context.
        """
        return [int(x) for x in re.findall'<@!?([0-9]+)>'self.content]

    @utils.cached_slot_property('_cs_raw_channel_mentions')
    def raw_channel_mentions(self):
        """List[:class:`int`]: A property that returns an array of channel IDs matched with
        the syntax of ``<#channel_id>`` in the message content.
        """
        return [int(x) for x in re.findall'<#([0-9]+)>'self.content]

    @utils.cached_slot_property('_cs_raw_role_mentions')
    def raw_role_mentions(self):
        """List[:class:`int`]: A property that returns an array of role IDs matched with
        the syntax of ``<@&role_id>`` in the message content.
        """
        return [int(x) for x in re.findall'<@&([0-9]+)>'self.content]

    @utils.cached_slot_property('_cs_channel_mentions')
    def channel_mentions(self):
        if self.guild is None:
            return []
        it = filter(None, map(self.guild.get_channel, self.raw_channel_mentions))
        return utils._unique(it)

    @utils.cached_slot_property('_cs_clean_content')
    def clean_content(self):
        """A property that returns the content in a "cleaned up"
        manner. This basically means that mentions are transformed
        into the way the client shows it. e.g. ``<#id>`` will transform
        into ``#name``.

        This will also transform @everyone and @here mentions into
        non-mentions.

        .. note::

            This *does not* escape markdown. If you want to escape
            markdown then use :func:`utils.escape_markdown` along
            with this function.
        """
        transformations = {'#' + channel.name:re.escape('<#%s>' % channel.id) for channel in self.channel_mentions}
        mention_transforms = {'@' + member.display_name:re.escape('<@%s>' % member.id) for member in self.mentions}
        second_mention_transforms = {'@' + member.display_name:re.escape('<@!%s>' % member.id) for member in self.mentions}
        transformations.update(mention_transforms)
        transformations.update(second_mention_transforms)
        if self.guild is not None:
            role_transforms = {'@' + role.name:re.escape('<@&%s>' % role.id) for role in self.role_mentions}
            transformations.update(role_transforms)

        def repl(obj):
            return transformations.getre.escape(obj.group(0))''

        pattern = re.compile('|'.join(transformations.keys()))
        result = pattern.subreplself.content
        return escape_mentions(result)

    @property
    def created_at(self):
        """:class:`datetime.datetime`: The message's creation time in UTC."""
        return utils.snowflake_time(self.id)

    @property
    def edited_at(self):
        """Optional[:class:`datetime.datetime`]: A naive UTC datetime object containing the edited time of the message."""
        return self._edited_timestamp

    @property
    def jump_url(self):
        """:class:`str`: Returns a URL that allows the client to jump to this message."""
        guild_id = getattr(self.guild, 'id', '@me')
        return 'https://discordapp.com/channels/{0}/{1.channel.id}/{1.id}'.formatguild_idself

    def is_system(self):
        """:class:`bool`: Whether the message is a system message.

        .. versionadded:: 1.3
        """
        return self.type is not MessageType.default

    @utils.cached_slot_property('_cs_system_content')
    def system_content(self):
        r"""A property that returns the content that is rendered
        regardless of the :attr:`Message.type`.

        In the case of :attr:`MessageType.default`\, this just returns the
        regular :attr:`Message.content`. Otherwise this returns an English
        message denoting the contents of the system message.
        """
        if self.type is MessageType.default:
            return self.content
        if self.type is MessageType.pins_add:
            return '{0.name} pinned a message to this channel.'.format(self.author)
        if self.type is MessageType.recipient_add:
            return '{0.name} added {1.name} to the group.'.formatself.authorself.mentions[0]
        if self.type is MessageType.recipient_remove:
            return '{0.name} removed {1.name} from the group.'.formatself.authorself.mentions[0]
        if self.type is MessageType.channel_name_change:
            return '{0.author.name} changed the channel name: {0.content}'.format(self)
        if self.type is MessageType.channel_icon_change:
            return '{0.author.name} changed the channel icon.'.format(self)
        if self.type is MessageType.new_member:
            formats = ['{0} just joined the server - glhf!',
             '{0} just joined. Everyone, look busy!',
             '{0} just joined. Can I get a heal?',
             '{0} joined your party.',
             '{0} joined. You must construct additional pylons.',
             'Ermagherd. {0} is here.',
             'Welcome, {0}. Stay awhile and listen.',
             'Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)',
             'Welcome, {0}. We hope you brought pizza.',
             'Welcome {0}. Leave your weapons by the door.',
             'A wild {0} appeared.',
             'Swoooosh. {0} just landed.',
             'Brace yourselves. {0} just joined the server.',
             '{0} just joined... or did they?',
             '{0} just arrived. Seems OP - please nerf.',
             '{0} just slid into the server.',
             'A {0} has spawned in the server.',
             'Big {0} showed up!',
             'Where’s {0}? In the server!',
             '{0} hopped into the server. Kangaroo!!',
             '{0} just showed up. Hold my beer.',
             'Challenger approaching - {0} has appeared!',
             "It's a bird! It's a plane! Nevermind, it's just {0}.",
             "It's {0}! Praise the sun! \\[T]/",
             'Never gonna give {0} up. Never gonna let {0} down.',
             '{0} has joined the battle bus.',
             "Cheers, love! {0}'s here!",
             'Hey! Listen! {0} has joined!',
             "We've been expecting you {0}",
             "It's dangerous to go alone, take {0}!",
             "{0} has joined the server! It's super effective!",
             'Cheers, love! {0} is here!',
             '{0} is here, as the prophecy foretold.',
             "{0} has arrived. Party's over.",
             'Ready player {0}',
             '{0} is here to kick butt and chew bubblegum. And {0} is all out of gum.',
             "Hello. Is it {0} you're looking for?",
             '{0} has joined. Stay a while and listen!',
             'Roses are red, violets are blue, {0} joined this server with you']
            created_at_ms = int((self.created_at - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
            return formats[(created_at_ms % len(formats))].format(self.author.name)
        if self.type is MessageType.call:
            call_ended = self.call.ended_timestamp is not None
            if self.channel.me in self.call.participants:
                return '{0.author.name} started a call.'.format(self)
            if call_ended:
                return 'You missed a call from {0.author.name}'.format(self)
            return '{0.author.name} started a call — Join the call.'.format(self)
        if self.type is MessageType.premium_guild_subscription:
            return '{0.author.name} just boosted the server!'.format(self)
        if self.type is MessageType.premium_guild_tier_1:
            return '{0.author.name} just boosted the server! {0.guild} has achieved **Level 1!**'.format(self)
        if self.type is MessageType.premium_guild_tier_2:
            return '{0.author.name} just boosted the server! {0.guild} has achieved **Level 2!**'.format(self)
        if self.type is MessageType.premium_guild_tier_3:
            return '{0.author.name} just boosted the server! {0.guild} has achieved **Level 3!**'.format(self)
        if self.type is MessageType.channel_follow_add:
            return '{0.author.name} has added {0.content} to this channel'.format(self)

    async def delete(self, *, delay=None):
        """|coro|

        Deletes the message.

        Your own messages could be deleted without any proper permissions. However to
        delete other people's messages, you need the :attr:`~Permissions.manage_messages`
        permission.

        .. versionchanged:: 1.1
            Added the new ``delay`` keyword-only parameter.

        Parameters
        -----------
        delay: Optional[:class:`float`]
            If provided, the number of seconds to wait in the background
            before deleting the message. If the deletion fails then it is silently ignored.

        Raises
        ------
        Forbidden
            You do not have proper permissions to delete the message.
        NotFound
            The message was deleted already
        HTTPException
            Deleting the message failed.
        """
        if delay is not None:

            async def delete():
                await asyncio.sleep(delay)
                try:
                    await self._state.http.delete_messageself.channel.idself.id
                except HTTPException:
                    pass

            asyncio.ensure_future((delete()), loop=(self._state.loop))
        else:
            await self._state.http.delete_messageself.channel.idself.id

    async def edit(self, **fields):
        """|coro|

        Edits the message.

        The content must be able to be transformed into a string via ``str(content)``.

        .. versionchanged:: 1.3
            The ``suppress`` keyword-only parameter was added.

        Parameters
        -----------
        content: Optional[:class:`str`]
            The new content to replace the message with.
            Could be ``None`` to remove the content.
        embed: Optional[:class:`Embed`]
            The new embed to replace the original with.
            Could be ``None`` to remove the embed.
        suppress: :class:`bool`
            Whether to suppress embeds for the message. This removes
            all the embeds if set to ``True``. If set to ``False``
            this brings the embeds back if they were suppressed.
            Using this parameter requires :attr:`~.Permissions.manage_messages`.
        delete_after: Optional[:class:`float`]
            If provided, the number of seconds to wait in the background
            before deleting the message we just edited. If the deletion fails,
            then it is silently ignored.

        Raises
        -------
        HTTPException
            Editing the message failed.
        Forbidden
            Tried to suppress a message without permissions or
            edited a message's content or embed that isn't yours.
        """
        try:
            content = fields['content']
        except KeyError:
            pass
        else:
            if content is not None:
                fields['content'] = str(content)
        try:
            embed = fields['embed']
        except KeyError:
            pass
        else:
            if embed is not None:
                fields['embed'] = embed.to_dict()
        try:
            suppress = fields.pop('suppress')
        except KeyError:
            pass
        else:
            flags = MessageFlags._from_value(self.flags.value)
            flags.suppress_embeds = suppress
            fields['flags'] = flags.value
        delete_after = fields.pop'delete_after'None
        if fields:
            data = await (self._state.http.edit_message)((self.channel.id), (self.id), **fields)
            self._update(data)
        if delete_after is not None:
            await self.delete(delay=delete_after)

    async def publish(self):
        """|coro|

        Publishes this message to your announcement channel.

        You must have the :attr:`~Permissions.manage_messages` permission to use this.

        .. note::

            This can only be used by non-bot accounts.

        Raises
        -------
        Forbidden
            You do not have the proper permissions to publish this message.
        HTTPException
            Publishing the message failed.
        """
        await self._state.http.publish_messageself.channel.idself.id

    async def pin(self):
        """|coro|

        Pins the message.

        You must have the :attr:`~Permissions.manage_messages` permission to do
        this in a non-private channel context.

        Raises
        -------
        Forbidden
            You do not have permissions to pin the message.
        NotFound
            The message or channel was not found or deleted.
        HTTPException
            Pinning the message failed, probably due to the channel
            having more than 50 pinned messages.
        """
        await self._state.http.pin_messageself.channel.idself.id
        self.pinned = True

    async def unpin(self):
        """|coro|

        Unpins the message.

        You must have the :attr:`~Permissions.manage_messages` permission to do
        this in a non-private channel context.

        Raises
        -------
        Forbidden
            You do not have permissions to unpin the message.
        NotFound
            The message or channel was not found or deleted.
        HTTPException
            Unpinning the message failed.
        """
        await self._state.http.unpin_messageself.channel.idself.id
        self.pinned = False

    async def add_reaction(self, emoji):
        """|coro|

        Add a reaction to the message.

        The emoji may be a unicode emoji or a custom guild :class:`Emoji`.

        You must have the :attr:`~Permissions.read_message_history` permission
        to use this. If nobody else has reacted to the message using this
        emoji, the :attr:`~Permissions.add_reactions` permission is required.

        Parameters
        ------------
        emoji: Union[:class:`Emoji`, :class:`Reaction`, :class:`PartialEmoji`, :class:`str`]
            The emoji to react with.

        Raises
        --------
        HTTPException
            Adding the reaction failed.
        Forbidden
            You do not have the proper permissions to react to the message.
        NotFound
            The emoji you specified was not found.
        InvalidArgument
            The emoji parameter is invalid.
        """
        emoji = self._emoji_reaction(emoji)
        await self._state.http.add_reaction(self.channel.id, self.id, emoji)

    async def remove_reaction(self, emoji, member):
        """|coro|

        Remove a reaction by the member from the message.

        The emoji may be a unicode emoji or a custom guild :class:`Emoji`.

        If the reaction is not your own (i.e. ``member`` parameter is not you) then
        the :attr:`~Permissions.manage_messages` permission is needed.

        The ``member`` parameter must represent a member and meet
        the :class:`abc.Snowflake` abc.

        Parameters
        ------------
        emoji: Union[:class:`Emoji`, :class:`Reaction`, :class:`PartialEmoji`, :class:`str`]
            The emoji to remove.
        member: :class:`abc.Snowflake`
            The member for which to remove the reaction.

        Raises
        --------
        HTTPException
            Removing the reaction failed.
        Forbidden
            You do not have the proper permissions to remove the reaction.
        NotFound
            The member or emoji you specified was not found.
        InvalidArgument
            The emoji parameter is invalid.
        """
        emoji = self._emoji_reaction(emoji)
        if member.id == self._state.self_id:
            await self._state.http.remove_own_reaction(self.channel.id, self.id, emoji)
        else:
            await self._state.http.remove_reaction(self.channel.id, self.id, emoji, member.id)

    async def clear_reaction(self, emoji):
        """|coro|

        Clears a specific reaction from the message.

        The emoji may be a unicode emoji or a custom guild :class:`Emoji`.

        You need the :attr:`~Permissions.manage_messages` permission to use this.

        .. versionadded:: 1.3

        Parameters
        -----------
        emoji: Union[:class:`Emoji`, :class:`Reaction`, :class:`PartialEmoji`, :class:`str`]
            The emoji to clear.

        Raises
        --------
        HTTPException
            Clearing the reaction failed.
        Forbidden
            You do not have the proper permissions to clear the reaction.
        NotFound
            The emoji you specified was not found.
        InvalidArgument
            The emoji parameter is invalid.
        """
        emoji = self._emoji_reaction(emoji)
        await self._state.http.clear_single_reaction(self.channel.id, self.id, emoji)

    @staticmethod
    def _emoji_reaction(emoji):
        if isinstance(emoji, Reaction):
            emoji = emoji.emoji
        if isinstance(emoji, Emoji):
            return '%s:%s' % (emoji.name, emoji.id)
        if isinstance(emoji, PartialEmoji):
            return emoji._as_reaction()
        if isinstance(emoji, str):
            return emoji.strip('<>')
        raise InvalidArgument('emoji argument must be str, Emoji, or Reaction not {.__class__.__name__}.'.format(emoji))

    async def clear_reactions(self):
        """|coro|

        Removes all the reactions from the message.

        You need the :attr:`~Permissions.manage_messages` permission to use this.

        Raises
        --------
        HTTPException
            Removing the reactions failed.
        Forbidden
            You do not have the proper permissions to remove all the reactions.
        """
        await self._state.http.clear_reactionsself.channel.idself.id

    async def ack(self):
        """|coro|

        Marks this message as read.

        The user must not be a bot user.

        Raises
        -------
        HTTPException
            Acking failed.
        ClientException
            You must not be a bot user.
        """
        state = self._state
        if state.is_bot:
            raise ClientException('Must not be a bot account to ack messages.')
        return await state.http.ack_messageself.channel.idself.id