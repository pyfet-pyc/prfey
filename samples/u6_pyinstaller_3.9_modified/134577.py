# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: dhooks\embed.py
import datetime
from typing import Union

class Embed:
    __doc__ = '\n    Class that represents a discord embed.\n\n    Parameters\n    -----------\n    \\*\\*title: str, optional\n        Defaults to :class:`None`.\n        The title of the embed.\n\n    \\*\\*description: str, optional\n        Defaults to :class:`None`.\n        The description of the embed.\n\n    \\*\\*url: str, optional\n        URL of the embed. It requires :attr:`title` to be set.\n\n    \\*\\*timestamp: str, optional\n        ``ISO 8601`` timestamp of the embed. If set to a "now",\n        the current time is set as the timestamp.\n        \n    \\*\\*color: int (or hex), optional\n        Color of the embed.\n        \n    \\*\\*image_url: str, optional\n        URL of the image.\n        \n    \\*\\*thumbnail_url: str, optional\n        URL of the thumbnail.\n        \n    '
    __slots__ = ('color', 'title', 'url', 'author', 'description', 'fields', 'image',
                 'thumbnail', 'footer', 'timestamp')

    def __init__--- This code section failed: ---

 L.  47         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'color'
                6  CALL_METHOD_1         1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               color

 L.  48        12  LOAD_FAST                'kwargs'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'title'
               18  CALL_METHOD_1         1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               title

 L.  49        24  LOAD_FAST                'kwargs'
               26  LOAD_METHOD              get
               28  LOAD_STR                 'url'
               30  CALL_METHOD_1         1  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               url

 L.  50        36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              get
               40  LOAD_STR                 'description'
               42  CALL_METHOD_1         1  ''
               44  LOAD_FAST                'self'
               46  STORE_ATTR               description

 L.  52        48  LOAD_FAST                'kwargs'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'timestamp'
               54  CALL_METHOD_1         1  ''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               timestamp

 L.  53        60  LOAD_FAST                'self'
               62  LOAD_ATTR                timestamp
               64  LOAD_STR                 'now'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L.  54        70  LOAD_GLOBAL              str
               72  LOAD_GLOBAL              datetime
               74  LOAD_ATTR                datetime
               76  LOAD_METHOD              utcnow
               78  CALL_METHOD_0         0  ''
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               timestamp
             86_0  COME_FROM            68  '68'

 L.  56        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               author

 L.  57        92  LOAD_CONST               None
               94  LOAD_FAST                'self'
               96  STORE_ATTR               thumbnail

 L.  58        98  LOAD_CONST               None
              100  LOAD_FAST                'self'
              102  STORE_ATTR               image

 L.  59       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               footer

 L.  60       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               fields

 L.  62       116  LOAD_FAST                'kwargs'
              118  LOAD_METHOD              get
              120  LOAD_STR                 'image_url'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'image_url'

 L.  63       126  LOAD_FAST                'image_url'
              128  LOAD_CONST               None
              130  <117>                 1  ''
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L.  64       134  LOAD_FAST                'self'
              136  LOAD_METHOD              set_image
              138  LOAD_FAST                'image_url'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           132  '132'

 L.  66       144  LOAD_FAST                'kwargs'
              146  LOAD_METHOD              get
              148  LOAD_STR                 'thumbnail_url'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'thumbnail_url'

 L.  67       154  LOAD_FAST                'thumbnail_url'
              156  LOAD_CONST               None
              158  <117>                 1  ''
              160  POP_JUMP_IF_FALSE   172  'to 172'

 L.  68       162  LOAD_FAST                'self'
              164  LOAD_METHOD              set_thumbnail
              166  LOAD_FAST                'thumbnail_url'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           160  '160'

Parse error at or near `<117>' instruction at offset 130

    def del_field(self, index: int) -> None:
        """
        Deletes a field by index.

        Parameters
        ----------
        index: int
            Index of the field to delete.

        """
        self.fields.popindex

    def set_title(self, title: str, url: str=None) -> None:
        """
        Sets the title of the embed.

        Parameters
        ----------
        title: str
            Title of the embed.

        url: str or None, optional
            URL hyperlink of the title.

        """
        self.title = title
        self.url = url

    def set_timestamp(self, time: Union[(str, datetime.datetime)]=None, now: bool=False) -> None:
        """
        Sets the timestamp of the embed.

        Parameters
        ----------
        time: str or :class:`datetime.datetime`
            The ``ISO 8601`` timestamp from the embed.

        now: bool
            Defaults to :class:`False`.
            If set to :class:`True` the current time is used for the timestamp.

        """
        if now:
            self.timestamp = str(datetime.datetime.utcnow)
        else:
            self.timestamp = str(time)

    def add_field(self, name: str, value: str, inline: bool=True) -> None:
        """
        Adds an embed field.

        Parameters
        ----------
        name: str
            Name attribute of the embed field.

        value: str
            Value attribute of the embed field.

        inline: bool
            Defaults to :class:`True`.
            Whether or not the embed should be inline.

        """
        field = {'name':name, 
         'value':value, 
         'inline':inline}
        self.fields.appendfield

    def set_author(self, name: str, icon_url: str=None, url: str=None) -> None:
        """
        Sets the author of the embed.

        Parameters
        ----------
        name: str
            The author's name.

        icon_url: str, optional
            URL for the author's icon.

        url: str, optional
            URL hyperlink for the author.

        """
        self.author = {'name':name, 
         'icon_url':icon_url, 
         'url':url}

    def set_thumbnail(self, url: str) -> None:
        """
        Sets the thumbnail of the embed.

        Parameters
        ----------
        url: str
            URL of the thumbnail.

        """
        self.thumbnail = {'url': url}

    def set_image(self, url: str) -> None:
        """
        Sets the image of the embed.

        Parameters
        ----------
        url: str
            URL of the image.

        """
        self.image = {'url': url}

    def set_footer(self, text: str, icon_url: str=None) -> None:
        """
        Sets the footer of the embed.

        Parameters
        ----------
        text: str
            The footer text.

        icon_url: str, optional
            URL for the icon in the footer.

        """
        self.footer = {'text':text, 
         'icon_url':icon_url}

    def to_dict--- This code section failed: ---

 L. 211         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'Embed.to_dict.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L. 213        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                __slots__

 L. 211        14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1