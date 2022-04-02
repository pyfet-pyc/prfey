# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\embeds.py
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
import datetime
from . import utils
from .colour import Colour

class _EmptyEmbed:

    def __bool__(self):
        return False

    def __repr__(self):
        return 'Embed.Empty'

    def __len__(self):
        return 0


EmptyEmbed = _EmptyEmbed()

class EmbedProxy:

    def __init__(self, layer):
        self.__dict__.update(layer)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return 'EmbedProxy(%s)' % ', '.join(('%s=%r' % (k, v) for k, v in self.__dict__.items() if not k.startswith('_')))

    def __getattr__(self, attr):
        return EmptyEmbed


class Embed:
    __doc__ = 'Represents a Discord embed.\n\n    .. container:: operations\n\n        .. describe:: len(x)\n\n            Returns the total size of the embed.\n            Useful for checking if it\'s within the 6000 character limit.\n\n    Certain properties return an ``EmbedProxy``, a type\n    that acts similar to a regular :class:`dict` except using dotted access,\n    e.g. ``embed.author.icon_url``. If the attribute\n    is invalid or empty, then a special sentinel value is returned,\n    :attr:`Embed.Empty`.\n\n    For ease of use, all parameters that expect a :class:`str` are implicitly\n    casted to :class:`str` for you.\n\n    Attributes\n    -----------\n    title: :class:`str`\n        The title of the embed.\n        This can be set during initialisation.\n    type: :class:`str`\n        The type of embed. Usually "rich".\n        This can be set during initialisation.\n    description: :class:`str`\n        The description of the embed.\n        This can be set during initialisation.\n    url: :class:`str`\n        The URL of the embed.\n        This can be set during initialisation.\n    timestamp: :class:`datetime.datetime`\n        The timestamp of the embed content. This could be a naive or aware datetime.\n    colour: Union[:class:`Colour`, :class:`int`]\n        The colour code of the embed. Aliased to ``color`` as well.\n        This can be set during initialisation.\n    Empty\n        A special sentinel value used by ``EmbedProxy`` and this class\n        to denote that the value or attribute is empty.\n    '
    __slots__ = ('title', 'url', 'type', '_timestamp', '_colour', '_footer', '_image',
                 '_thumbnail', '_video', '_provider', '_author', '_fields', 'description')
    Empty = EmptyEmbed

    def __init__(self, **kwargs):
        try:
            colour = kwargs['colour']
        except KeyError:
            colour = kwargs.get('color', EmptyEmbed)
        else:
            self.colour = colour
            self.title = kwargs.get('title', EmptyEmbed)
            self.type = kwargs.get('type', 'rich')
            self.url = kwargs.get('url', EmptyEmbed)
            self.description = kwargs.get('description', EmptyEmbed)
            try:
                timestamp = kwargs['timestamp']
            except KeyError:
                pass
            else:
                self.timestamp = timestamp

    @classmethod
    def from_dict--- This code section failed: ---

 L. 143         0  LOAD_FAST                'cls'
                2  LOAD_METHOD              __new__
                4  LOAD_FAST                'cls'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'self'

 L. 147        10  LOAD_FAST                'data'
               12  LOAD_METHOD              get
               14  LOAD_STR                 'title'
               16  LOAD_GLOBAL              EmptyEmbed
               18  CALL_METHOD_2         2  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               title

 L. 148        24  LOAD_FAST                'data'
               26  LOAD_METHOD              get
               28  LOAD_STR                 'type'
               30  LOAD_GLOBAL              EmptyEmbed
               32  CALL_METHOD_2         2  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               type

 L. 149        38  LOAD_FAST                'data'
               40  LOAD_METHOD              get
               42  LOAD_STR                 'description'
               44  LOAD_GLOBAL              EmptyEmbed
               46  CALL_METHOD_2         2  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               description

 L. 150        52  LOAD_FAST                'data'
               54  LOAD_METHOD              get
               56  LOAD_STR                 'url'
               58  LOAD_GLOBAL              EmptyEmbed
               60  CALL_METHOD_2         2  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               url

 L. 154        66  SETUP_FINALLY        88  'to 88'

 L. 155        68  LOAD_GLOBAL              Colour
               70  LOAD_FAST                'data'
               72  LOAD_STR                 'color'
               74  BINARY_SUBSCR    
               76  LOAD_CONST               ('value',)
               78  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _colour
               84  POP_BLOCK        
               86  JUMP_FORWARD        108  'to 108'
             88_0  COME_FROM_FINALLY    66  '66'

 L. 156        88  DUP_TOP          
               90  LOAD_GLOBAL              KeyError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   106  'to 106'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 157       102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            94  '94'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            86  '86'

 L. 159       108  SETUP_FINALLY       130  'to 130'

 L. 160       110  LOAD_GLOBAL              utils
              112  LOAD_METHOD              parse_time
              114  LOAD_FAST                'data'
              116  LOAD_STR                 'timestamp'
              118  BINARY_SUBSCR    
              120  CALL_METHOD_1         1  ''
              122  LOAD_FAST                'self'
              124  STORE_ATTR               _timestamp
              126  POP_BLOCK        
              128  JUMP_FORWARD        150  'to 150'
            130_0  COME_FROM_FINALLY   108  '108'

 L. 161       130  DUP_TOP          
              132  LOAD_GLOBAL              KeyError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   148  'to 148'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 162       144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           136  '136'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM           128  '128'

 L. 164       150  LOAD_CONST               ('thumbnail', 'video', 'provider', 'author', 'fields', 'image', 'footer')
              152  GET_ITER         
              154  FOR_ITER            214  'to 214'
              156  STORE_FAST               'attr'

 L. 165       158  SETUP_FINALLY       172  'to 172'

 L. 166       160  LOAD_FAST                'data'
              162  LOAD_FAST                'attr'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'value'
              168  POP_BLOCK        
              170  JUMP_FORWARD        196  'to 196'
            172_0  COME_FROM_FINALLY   158  '158'

 L. 167       172  DUP_TOP          
              174  LOAD_GLOBAL              KeyError
              176  COMPARE_OP               exception-match
              178  POP_JUMP_IF_FALSE   194  'to 194'
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          

 L. 168       186  POP_EXCEPT       
              188  JUMP_BACK           154  'to 154'
              190  POP_EXCEPT       
              192  JUMP_BACK           154  'to 154'
            194_0  COME_FROM           178  '178'
              194  END_FINALLY      
            196_0  COME_FROM           170  '170'

 L. 170       196  LOAD_GLOBAL              setattr
              198  LOAD_FAST                'self'
              200  LOAD_STR                 '_'
              202  LOAD_FAST                'attr'
              204  BINARY_ADD       
              206  LOAD_FAST                'value'
              208  CALL_FUNCTION_3       3  ''
              210  POP_TOP          
              212  JUMP_BACK           154  'to 154'

 L. 172       214  LOAD_FAST                'self'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 190

    def copy(self):
        """Returns a shallow copy of the embed."""
        return Embed.from_dict(self.to_dict())

    def __len__(self):
        total = len(self.title) + len(self.description)
        for field in getattrself'_fields'[]:
            total += len(field['name']) + len(field['value'])
        else:
            try:
                footer = self._footer
            except AttributeError:
                pass
            else:
                total += len(footer['text'])
            try:
                author = self._author
            except AttributeError:
                pass
            else:
                total += len(author['name'])
            return total

    @property
    def colour(self):
        return getattrself'_colour'EmptyEmbed

    @colour.setter
    def colour(self, value):
        if isinstance(value, (Colour, _EmptyEmbed)):
            self._colour = value
        else:
            if isinstance(value, int):
                self._colour = Colour(value=value)
            else:
                raise TypeError('Expected discord.Colour, int, or Embed.Empty but received %s instead.' % value.__class__.__name__)

    color = colour

    @property
    def timestamp(self):
        return getattrself'_timestamp'EmptyEmbed

    @timestamp.setter
    def timestamp(self, value):
        if isinstance(value, (datetime.datetime, _EmptyEmbed)):
            self._timestamp = value
        else:
            raise TypeError('Expected datetime.datetime or Embed.Empty received %s instead' % value.__class__.__name__)

    @property
    def footer(self):
        """Returns an ``EmbedProxy`` denoting the footer contents.

        See :meth:`set_footer` for possible values you can access.

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_footer'{})

    def set_footer(self, *, text=EmptyEmbed, icon_url=EmptyEmbed):
        """Sets the footer for the embed content.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        text: :class:`str`
            The footer text.
        icon_url: :class:`str`
            The URL of the footer icon. Only HTTP(S) is supported.
        """
        self._footer = {}
        if text is not EmptyEmbed:
            self._footer['text'] = str(text)
        if icon_url is not EmptyEmbed:
            self._footer['icon_url'] = str(icon_url)
        return self

    @property
    def image(self):
        """Returns an ``EmbedProxy`` denoting the image contents.

        Possible attributes you can access are:

        - ``url``
        - ``proxy_url``
        - ``width``
        - ``height``

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_image'{})

    def set_image(self, *, url):
        """Sets the image for the embed content.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        url: :class:`str`
            The source URL for the image. Only HTTP(S) is supported.
        """
        self._image = {'url': str(url)}
        return self

    @property
    def thumbnail(self):
        """Returns an ``EmbedProxy`` denoting the thumbnail contents.

        Possible attributes you can access are:

        - ``url``
        - ``proxy_url``
        - ``width``
        - ``height``

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_thumbnail'{})

    def set_thumbnail(self, *, url):
        """Sets the thumbnail for the embed content.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        url: :class:`str`
            The source URL for the thumbnail. Only HTTP(S) is supported.
        """
        self._thumbnail = {'url': str(url)}
        return self

    @property
    def video(self):
        """Returns an ``EmbedProxy`` denoting the video contents.

        Possible attributes include:

        - ``url`` for the video URL.
        - ``height`` for the video height.
        - ``width`` for the video width.

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_video'{})

    @property
    def provider(self):
        """Returns an ``EmbedProxy`` denoting the provider contents.

        The only attributes that might be accessed are ``name`` and ``url``.

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_provider'{})

    @property
    def author(self):
        """Returns an ``EmbedProxy`` denoting the author contents.

        See :meth:`set_author` for possible values you can access.

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return EmbedProxy(getattrself'_author'{})

    def set_author(self, *, name, url=EmptyEmbed, icon_url=EmptyEmbed):
        """Sets the author for the embed content.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        name: :class:`str`
            The name of the author.
        url: :class:`str`
            The URL for the author.
        icon_url: :class:`str`
            The URL of the author icon. Only HTTP(S) is supported.
        """
        self._author = {'name': str(name)}
        if url is not EmptyEmbed:
            self._author['url'] = str(url)
        if icon_url is not EmptyEmbed:
            self._author['icon_url'] = str(icon_url)
        return self

    @property
    def fields(self):
        """Returns a :class:`list` of ``EmbedProxy`` denoting the field contents.

        See :meth:`add_field` for possible values you can access.

        If the attribute has no value then :attr:`Empty` is returned.
        """
        return [EmbedProxy(d) for d in getattrself'_fields'[]]

    def add_field(self, *, name, value, inline=True):
        """Adds a field to the embed object.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        name: :class:`str`
            The name of the field.
        value: :class:`str`
            The value of the field.
        inline: :class:`bool`
            Whether the field should be displayed inline.
        """
        field = {'inline':inline, 
         'name':str(name), 
         'value':str(value)}
        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [
             field]
        else:
            return self

    def insert_field_at(self, index, *, name, value, inline=True):
        """Inserts a field before a specified index to the embed.

        This function returns the class instance to allow for fluent-style
        chaining.

        .. versionadded:: 1.2

        Parameters
        -----------
        index: :class:`int`
            The index of where to insert the field.
        name: :class:`str`
            The name of the field.
        value: :class:`str`
            The value of the field.
        inline: :class:`bool`
            Whether the field should be displayed inline.
        """
        field = {'inline':inline, 
         'name':str(name), 
         'value':str(value)}
        try:
            self._fields.insert(index, field)
        except AttributeError:
            self._fields = [
             field]
        else:
            return self

    def clear_fields(self):
        """Removes all fields from this embed."""
        try:
            self._fields.clear()
        except AttributeError:
            self._fields = []

    def remove_field(self, index):
        """Removes a field at a specified index.

        If the index is invalid or out of bounds then the error is
        silently swallowed.

        .. note::

            When deleting a field by index, the index of the other fields
            shift to fill the gap just like a regular list.

        Parameters
        -----------
        index: :class:`int`
            The index of the field to remove.
        """
        try:
            del self._fields[index]
        except (AttributeError, IndexError):
            pass

    def set_field_at(self, index, *, name, value, inline=True):
        """Modifies a field to the embed object.

        The index must point to a valid pre-existing field.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        index: :class:`int`
            The index of the field to modify.
        name: :class:`str`
            The name of the field.
        value: :class:`str`
            The value of the field.
        inline: :class:`bool`
            Whether the field should be displayed inline.

        Raises
        -------
        IndexError
            An invalid index was provided.
        """
        try:
            field = self._fields[index]
        except (TypeError, IndexError, AttributeError):
            raise IndexError('field index out of range')
        else:
            field['name'] = str(name)
            field['value'] = str(value)
            field['inline'] = inline
            return self

    def to_dict--- This code section failed: ---

 L. 525         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'Embed.to_dict.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L. 527        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                __slots__

 L. 525        14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'result'

 L. 533        20  SETUP_FINALLY        36  'to 36'

 L. 534        22  LOAD_FAST                'result'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'colour'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'colour'
               32  POP_BLOCK        
               34  JUMP_FORWARD         56  'to 56'
             36_0  COME_FROM_FINALLY    20  '20'

 L. 535        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    54  'to 54'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 536        50  POP_EXCEPT       
               52  JUMP_FORWARD         70  'to 70'
             54_0  COME_FROM            42  '42'
               54  END_FINALLY      
             56_0  COME_FROM            34  '34'

 L. 538        56  LOAD_FAST                'colour'
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 539        60  LOAD_FAST                'colour'
               62  LOAD_ATTR                value
               64  LOAD_FAST                'result'
               66  LOAD_STR                 'color'
               68  STORE_SUBSCR     
             70_0  COME_FROM            58  '58'
             70_1  COME_FROM            52  '52'

 L. 541        70  SETUP_FINALLY        86  'to 86'

 L. 542        72  LOAD_FAST                'result'
               74  LOAD_METHOD              pop
               76  LOAD_STR                 'timestamp'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'timestamp'
               82  POP_BLOCK        
               84  JUMP_FORWARD        106  'to 106'
             86_0  COME_FROM_FINALLY    70  '70'

 L. 543        86  DUP_TOP          
               88  LOAD_GLOBAL              KeyError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   104  'to 104'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 544       100  POP_EXCEPT       
              102  JUMP_FORWARD        166  'to 166'
            104_0  COME_FROM            92  '92'
              104  END_FINALLY      
            106_0  COME_FROM            84  '84'

 L. 546       106  LOAD_FAST                'timestamp'
              108  POP_JUMP_IF_FALSE   166  'to 166'

 L. 547       110  LOAD_FAST                'timestamp'
              112  LOAD_ATTR                tzinfo
              114  POP_JUMP_IF_FALSE   142  'to 142'

 L. 548       116  LOAD_FAST                'timestamp'
              118  LOAD_ATTR                astimezone
              120  LOAD_GLOBAL              datetime
              122  LOAD_ATTR                timezone
              124  LOAD_ATTR                utc
              126  LOAD_CONST               ('tz',)
              128  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              130  LOAD_METHOD              isoformat
              132  CALL_METHOD_0         0  ''
              134  LOAD_FAST                'result'
              136  LOAD_STR                 'timestamp'
              138  STORE_SUBSCR     
              140  JUMP_FORWARD        166  'to 166'
            142_0  COME_FROM           114  '114'

 L. 550       142  LOAD_FAST                'timestamp'
              144  LOAD_ATTR                replace
              146  LOAD_GLOBAL              datetime
              148  LOAD_ATTR                timezone
              150  LOAD_ATTR                utc
              152  LOAD_CONST               ('tzinfo',)
              154  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              156  LOAD_METHOD              isoformat
              158  CALL_METHOD_0         0  ''
              160  LOAD_FAST                'result'
              162  LOAD_STR                 'timestamp'
              164  STORE_SUBSCR     
            166_0  COME_FROM           140  '140'
            166_1  COME_FROM           108  '108'
            166_2  COME_FROM           102  '102'

 L. 553       166  LOAD_DEREF               'self'
              168  LOAD_ATTR                type
              170  POP_JUMP_IF_FALSE   182  'to 182'

 L. 554       172  LOAD_DEREF               'self'
              174  LOAD_ATTR                type
              176  LOAD_FAST                'result'
              178  LOAD_STR                 'type'
              180  STORE_SUBSCR     
            182_0  COME_FROM           170  '170'

 L. 556       182  LOAD_DEREF               'self'
              184  LOAD_ATTR                description
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 557       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                description
              192  LOAD_FAST                'result'
              194  LOAD_STR                 'description'
              196  STORE_SUBSCR     
            198_0  COME_FROM           186  '186'

 L. 559       198  LOAD_DEREF               'self'
              200  LOAD_ATTR                url
              202  POP_JUMP_IF_FALSE   214  'to 214'

 L. 560       204  LOAD_DEREF               'self'
              206  LOAD_ATTR                url
              208  LOAD_FAST                'result'
              210  LOAD_STR                 'url'
              212  STORE_SUBSCR     
            214_0  COME_FROM           202  '202'

 L. 562       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                title
              218  POP_JUMP_IF_FALSE   230  'to 230'

 L. 563       220  LOAD_DEREF               'self'
              222  LOAD_ATTR                title
              224  LOAD_FAST                'result'
              226  LOAD_STR                 'title'
              228  STORE_SUBSCR     
            230_0  COME_FROM           218  '218'

 L. 565       230  LOAD_FAST                'result'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1