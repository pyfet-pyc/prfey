# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bs4\element.py
__license__ = 'MIT'
try:
    from collections.abc import Callable
except ImportError as e:
    try:
        from collections import Callable
    finally:
        e = None
        del e

else:
    import re, sys, warnings
    try:
        import soupsieve
    except ImportError as e:
        try:
            soupsieve = None
            warnings.warn('The soupsieve package is not installed. CSS selectors cannot be used.')
        finally:
            e = None
            del e

    else:
        from bs4.formatter import Formatter, HTMLFormatter, XMLFormatter
        DEFAULT_OUTPUT_ENCODING = 'utf-8'
        PY3K = sys.version_info[0] > 2
        nonwhitespace_re = re.compile('\\S+')
        whitespace_re = re.compile('\\s+')

        def _alias(attr):
            """Alias one attribute name to another for backward compatibility"""

            @property
            def alias(self):
                return getattr(self, attr)

            @alias.setter
            def alias(self):
                return setattr(self, attr)

            return alias


        PYTHON_SPECIFIC_ENCODINGS = set([
         'idna',
         'mbcs',
         'oem',
         'palmos',
         'punycode',
         'raw_unicode_escape',
         'undefined',
         'unicode_escape',
         'raw-unicode-escape',
         'unicode-escape',
         'string-escape',
         'string_escape'])

        class NamespacedAttribute(str):
            __doc__ = "A namespaced string (e.g. 'xml:lang') that remembers the namespace\n    ('xml') and the name ('lang') that were used to create it.\n    "

            def __new__(cls, prefix, name=None, namespace=None):
                if not name:
                    name = None
                if name is None:
                    obj = str.__new__(cls, prefix)
                elif prefix is None:
                    obj = str.__new__(cls, name)
                else:
                    obj = str.__new__(cls, prefix + ':' + name)
                obj.prefix = prefix
                obj.name = name
                obj.namespace = namespace
                return obj


        class AttributeValueWithCharsetSubstitution(str):
            __doc__ = 'A stand-in object for a character encoding specified in HTML.'


        class CharsetMetaAttributeValue(AttributeValueWithCharsetSubstitution):
            __doc__ = 'A generic stand-in for the value of a meta tag\'s \'charset\' attribute.\n\n    When Beautiful Soup parses the markup \'<meta charset="utf8">\', the\n    value of the \'charset\' attribute will be one of these objects.\n    '

            def __new__(cls, original_value):
                obj = str.__new__(cls, original_value)
                obj.original_value = original_value
                return obj

            def encode(self, encoding):
                """When an HTML document is being encoded to a given encoding, the
        value of a meta tag's 'charset' is the name of the encoding.
        """
                if encoding in PYTHON_SPECIFIC_ENCODINGS:
                    return ''
                return encoding


        class ContentMetaAttributeValue(AttributeValueWithCharsetSubstitution):
            __doc__ = 'A generic stand-in for the value of a meta tag\'s \'content\' attribute.\n\n    When Beautiful Soup parses the markup:\n     <meta http-equiv="content-type" content="text/html; charset=utf8">\n\n    The value of the \'content\' attribute will be one of these objects.\n    '
            CHARSET_RE = re.compile('((^|;)\\s*charset=)([^;]*)', re.M)

            def __new__(cls, original_value):
                match = cls.CHARSET_RE.search(original_value)
                if match is None:
                    return str.__new__(str, original_value)
                obj = str.__new__(cls, original_value)
                obj.original_value = original_value
                return obj

            def encode(self, encoding):
                if encoding in PYTHON_SPECIFIC_ENCODINGS:
                    return ''

                def rewrite(match):
                    return match.group(1) + encoding

                return self.CHARSET_RE.sub(rewrite, self.original_value)


        class PageElement(object):
            __doc__ = 'Contains the navigational information for some part of the page:\n    that is, its current location in the parse tree.\n\n    NavigableString, Tag, etc. are all subclasses of PageElement.\n    '

            def setup(self, parent=None, previous_element=None, next_element=None, previous_sibling=None, next_sibling=None):
                """Sets up the initial relations between this element and
        other elements.

        :param parent: The parent of this element.

        :param previous_element: The element parsed immediately before
            this one.
        
        :param next_element: The element parsed immediately before
            this one.

        :param previous_sibling: The most recently encountered element
            on the same level of the parse tree as this one.

        :param previous_sibling: The next element to be encountered
            on the same level of the parse tree as this one.
        """
                self.parent = parent
                self.previous_element = previous_element
                if previous_element is not None:
                    self.previous_element.next_element = self
                self.next_element = next_element
                if self.next_element is not None:
                    self.next_element.previous_element = self
                self.next_sibling = next_sibling
                if self.next_sibling is not None:
                    self.next_sibling.previous_sibling = self
                if previous_sibling is None:
                    if self.parent is not None:
                        if self.parent.contents:
                            previous_sibling = self.parent.contents[(-1)]
                self.previous_sibling = previous_sibling
                if previous_sibling is not None:
                    self.previous_sibling.next_sibling = self

            def format_string(self, s, formatter):
                """Format the given string using the given formatter.

        :param s: A string.
        :param formatter: A Formatter object, or a string naming one of the standard formatters.
        """
                if formatter is None:
                    return s
                if not isinstance(formatter, Formatter):
                    formatter = self.formatter_for_name(formatter)
                output = formatter.substitute(s)
                return output

            def formatter_for_name(self, formatter):
                """Look up or create a Formatter for the given identifier,
        if necessary.

        :param formatter: Can be a Formatter object (used as-is), a
            function (used as the entity substitution hook for an
            XMLFormatter or HTMLFormatter), or a string (used to look
            up an XMLFormatter or HTMLFormatter in the appropriate
            registry.
        """
                if isinstance(formatter, Formatter):
                    return formatter
                if self._is_xml:
                    c = XMLFormatter
                else:
                    c = HTMLFormatter
                if isinstance(formatter, Callable):
                    return c(entity_substitution=formatter)
                return c.REGISTRY[formatter]

            @property
            def _is_xml(self):
                """Is this element part of an XML tree or an HTML tree?

        This is used in formatter_for_name, when deciding whether an
        XMLFormatter or HTMLFormatter is more appropriate. It can be
        inefficient, but it should be called very rarely.
        """
                if self.known_xml is not None:
                    return self.known_xml
                if self.parent is None:
                    return getattr(self, 'is_xml', False)
                return self.parent._is_xml

            nextSibling = _alias('next_sibling')
            previousSibling = _alias('previous_sibling')

            def replace_with(self, replace_with):
                """Replace this PageElement with another one, keeping the rest of the
        tree the same.
        
        :param replace_with: A PageElement.
        :return: `self`, no longer part of the tree.
        """
                if self.parent is None:
                    raise ValueError('Cannot replace one element with another when the element to be replaced is not part of a tree.')
                if replace_with is self:
                    return
                if replace_with is self.parent:
                    raise ValueError('Cannot replace a Tag with its parent.')
                old_parent = self.parent
                my_index = self.parent.index(self)
                self.extract(_self_index=my_index)
                old_parent.insert(my_index, replace_with)
                return self

            replaceWith = replace_with

            def unwrap(self):
                """Replace this PageElement with its contents.

        :return: `self`, no longer part of the tree.
        """
                my_parent = self.parent
                if self.parent is None:
                    raise ValueError('Cannot replace an element with its contents when thatelement is not part of a tree.')
                my_index = self.parent.index(self)
                self.extract(_self_index=my_index)
                for child in reversed(self.contents[:]):
                    my_parent.insert(my_index, child)
                else:
                    return self

            replace_with_children = unwrap
            replaceWithChildren = unwrap

            def wrap(self, wrap_inside):
                """Wrap this PageElement inside another one.

        :param wrap_inside: A PageElement.
        :return: `wrap_inside`, occupying the position in the tree that used
           to be occupied by `self`, and with `self` inside it.
        """
                me = self.replace_with(wrap_inside)
                wrap_inside.append(me)
                return wrap_inside

            def extract(self, _self_index=None):
                """Destructively rips this element out of the tree.

        :param _self_index: The location of this element in its parent's
           .contents, if known. Passing this in allows for a performance
           optimization.

        :return: `self`, no longer part of the tree.
        """
                if self.parent is not None:
                    if _self_index is None:
                        _self_index = self.parent.index(self)
                    del self.parent.contents[_self_index]
                last_child = self._last_descendant()
                next_element = last_child.next_element
                if self.previous_element is not None:
                    if self.previous_element is not next_element:
                        self.previous_element.next_element = next_element
                if next_element is not None:
                    if next_element is not self.previous_element:
                        next_element.previous_element = self.previous_element
                self.previous_element = None
                last_child.next_element = None
                self.parent = None
                if self.previous_sibling is not None:
                    if self.previous_sibling is not self.next_sibling:
                        self.previous_sibling.next_sibling = self.next_sibling
                if self.next_sibling is not None:
                    if self.next_sibling is not self.previous_sibling:
                        self.next_sibling.previous_sibling = self.previous_sibling
                self.previous_sibling = self.next_sibling = None
                return self

            def _last_descendant(self, is_initialized=True, accept_self=True):
                """Finds the last element beneath this object to be parsed.

        :param is_initialized: Has `setup` been called on this PageElement
            yet?
        :param accept_self: Is `self` an acceptable answer to the question?
        """
                if is_initialized and self.next_sibling is not None:
                    last_child = self.next_sibling.previous_element
                else:
                    last_child = self
                    while isinstance(last_child, Tag):
                        if last_child.contents:
                            last_child = last_child.contents[(-1)]

                if not accept_self:
                    if last_child is self:
                        last_child = None
                return last_child

            _lastRecursiveChild = _last_descendant

            def insert--- This code section failed: ---

 L. 375         0  LOAD_FAST                'new_child'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 376         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Cannot insert None into a tag.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 377        16  LOAD_FAST                'new_child'
               18  LOAD_FAST                'self'
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 378        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'Cannot insert a tag into itself.'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L. 379        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'new_child'
               36  LOAD_GLOBAL              str
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    60  'to 60'

 L. 380        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'new_child'
               46  LOAD_GLOBAL              NavigableString
               48  CALL_FUNCTION_2       2  ''

 L. 379        50  POP_JUMP_IF_TRUE     60  'to 60'

 L. 381        52  LOAD_GLOBAL              NavigableString
               54  LOAD_FAST                'new_child'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'new_child'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            40  '40'

 L. 383        60  LOAD_CONST               0
               62  LOAD_CONST               ('BeautifulSoup',)
               64  IMPORT_NAME              bs4
               66  IMPORT_FROM              BeautifulSoup
               68  STORE_FAST               'BeautifulSoup'
               70  POP_TOP          

 L. 384        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'new_child'
               76  LOAD_FAST                'BeautifulSoup'
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_FALSE   122  'to 122'

 L. 387        82  LOAD_GLOBAL              list
               84  LOAD_FAST                'new_child'
               86  LOAD_ATTR                contents
               88  CALL_FUNCTION_1       1  ''
               90  GET_ITER         
             92_0  COME_FROM           116  '116'
               92  FOR_ITER            118  'to 118'
               94  STORE_FAST               'subchild'

 L. 388        96  LOAD_FAST                'self'
               98  LOAD_METHOD              insert
              100  LOAD_FAST                'position'
              102  LOAD_FAST                'subchild'
              104  CALL_METHOD_2         2  ''
              106  POP_TOP          

 L. 389       108  LOAD_FAST                'position'
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  STORE_FAST               'position'
              116  JUMP_BACK            92  'to 92'
            118_0  COME_FROM            92  '92'

 L. 390       118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            80  '80'

 L. 391       122  LOAD_GLOBAL              min
              124  LOAD_FAST                'position'
              126  LOAD_GLOBAL              len
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                contents
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_2       2  ''
              136  STORE_FAST               'position'

 L. 392       138  LOAD_GLOBAL              hasattr
              140  LOAD_FAST                'new_child'
              142  LOAD_STR                 'parent'
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   202  'to 202'
              148  LOAD_FAST                'new_child'
              150  LOAD_ATTR                parent
              152  LOAD_CONST               None
              154  COMPARE_OP               is-not
              156  POP_JUMP_IF_FALSE   202  'to 202'

 L. 395       158  LOAD_FAST                'new_child'
              160  LOAD_ATTR                parent
              162  LOAD_FAST                'self'
              164  COMPARE_OP               is
              166  POP_JUMP_IF_FALSE   194  'to 194'

 L. 396       168  LOAD_FAST                'self'
              170  LOAD_METHOD              index
              172  LOAD_FAST                'new_child'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'current_index'

 L. 397       178  LOAD_FAST                'current_index'
              180  LOAD_FAST                'position'
              182  COMPARE_OP               <
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 402       186  LOAD_FAST                'position'
              188  LOAD_CONST               1
              190  INPLACE_SUBTRACT 
              192  STORE_FAST               'position'
            194_0  COME_FROM           184  '184'
            194_1  COME_FROM           166  '166'

 L. 403       194  LOAD_FAST                'new_child'
              196  LOAD_METHOD              extract
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
            202_0  COME_FROM           156  '156'
            202_1  COME_FROM           146  '146'

 L. 405       202  LOAD_FAST                'self'
              204  LOAD_FAST                'new_child'
              206  STORE_ATTR               parent

 L. 406       208  LOAD_CONST               None
              210  STORE_FAST               'previous_child'

 L. 407       212  LOAD_FAST                'position'
              214  LOAD_CONST               0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   234  'to 234'

 L. 408       220  LOAD_CONST               None
              222  LOAD_FAST                'new_child'
              224  STORE_ATTR               previous_sibling

 L. 409       226  LOAD_FAST                'self'
              228  LOAD_FAST                'new_child'
              230  STORE_ATTR               previous_element
              232  JUMP_FORWARD        274  'to 274'
            234_0  COME_FROM           218  '218'

 L. 411       234  LOAD_FAST                'self'
              236  LOAD_ATTR                contents
              238  LOAD_FAST                'position'
              240  LOAD_CONST               1
              242  BINARY_SUBTRACT  
              244  BINARY_SUBSCR    
              246  STORE_FAST               'previous_child'

 L. 412       248  LOAD_FAST                'previous_child'
              250  LOAD_FAST                'new_child'
              252  STORE_ATTR               previous_sibling

 L. 413       254  LOAD_FAST                'new_child'
              256  LOAD_FAST                'new_child'
              258  LOAD_ATTR                previous_sibling
              260  STORE_ATTR               next_sibling

 L. 414       262  LOAD_FAST                'previous_child'
              264  LOAD_METHOD              _last_descendant
              266  LOAD_CONST               False
              268  CALL_METHOD_1         1  ''
              270  LOAD_FAST                'new_child'
              272  STORE_ATTR               previous_element
            274_0  COME_FROM           232  '232'

 L. 415       274  LOAD_FAST                'new_child'
              276  LOAD_ATTR                previous_element
              278  LOAD_CONST               None
              280  COMPARE_OP               is-not
          282_284  POP_JUMP_IF_FALSE   294  'to 294'

 L. 416       286  LOAD_FAST                'new_child'
              288  LOAD_FAST                'new_child'
              290  LOAD_ATTR                previous_element
              292  STORE_ATTR               next_element
            294_0  COME_FROM           282  '282'

 L. 418       294  LOAD_FAST                'new_child'
              296  LOAD_METHOD              _last_descendant
              298  LOAD_CONST               False
              300  CALL_METHOD_1         1  ''
              302  STORE_FAST               'new_childs_last_element'

 L. 420       304  LOAD_FAST                'position'
              306  LOAD_GLOBAL              len
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                contents
              312  CALL_FUNCTION_1       1  ''
              314  COMPARE_OP               >=
          316_318  POP_JUMP_IF_FALSE   410  'to 410'

 L. 421       320  LOAD_CONST               None
              322  LOAD_FAST                'new_child'
              324  STORE_ATTR               next_sibling

 L. 423       326  LOAD_FAST                'self'
              328  STORE_FAST               'parent'

 L. 424       330  LOAD_CONST               None
              332  STORE_FAST               'parents_next_sibling'
            334_0  COME_FROM           380  '380'
            334_1  COME_FROM           372  '372'

 L. 425       334  LOAD_FAST                'parents_next_sibling'
              336  LOAD_CONST               None
              338  COMPARE_OP               is
          340_342  POP_JUMP_IF_FALSE   384  'to 384'
              344  LOAD_FAST                'parent'
              346  LOAD_CONST               None
              348  COMPARE_OP               is-not
          350_352  POP_JUMP_IF_FALSE   384  'to 384'

 L. 426       354  LOAD_FAST                'parent'
              356  LOAD_ATTR                next_sibling
              358  STORE_FAST               'parents_next_sibling'

 L. 427       360  LOAD_FAST                'parent'
              362  LOAD_ATTR                parent
              364  STORE_FAST               'parent'

 L. 428       366  LOAD_FAST                'parents_next_sibling'
              368  LOAD_CONST               None
              370  COMPARE_OP               is-not
          372_374  POP_JUMP_IF_FALSE_BACK   334  'to 334'

 L. 430   376_378  JUMP_FORWARD        384  'to 384'
          380_382  JUMP_BACK           334  'to 334'
            384_0  COME_FROM           376  '376'
            384_1  COME_FROM           350  '350'
            384_2  COME_FROM           340  '340'

 L. 431       384  LOAD_FAST                'parents_next_sibling'
              386  LOAD_CONST               None
              388  COMPARE_OP               is-not
          390_392  POP_JUMP_IF_FALSE   402  'to 402'

 L. 432       394  LOAD_FAST                'parents_next_sibling'
              396  LOAD_FAST                'new_childs_last_element'
              398  STORE_ATTR               next_element
              400  JUMP_FORWARD        408  'to 408'
            402_0  COME_FROM           390  '390'

 L. 436       402  LOAD_CONST               None
              404  LOAD_FAST                'new_childs_last_element'
              406  STORE_ATTR               next_element
            408_0  COME_FROM           400  '400'
              408  JUMP_FORWARD        452  'to 452'
            410_0  COME_FROM           316  '316'

 L. 438       410  LOAD_FAST                'self'
              412  LOAD_ATTR                contents
              414  LOAD_FAST                'position'
              416  BINARY_SUBSCR    
              418  STORE_FAST               'next_child'

 L. 439       420  LOAD_FAST                'next_child'
              422  LOAD_FAST                'new_child'
              424  STORE_ATTR               next_sibling

 L. 440       426  LOAD_FAST                'new_child'
              428  LOAD_ATTR                next_sibling
              430  LOAD_CONST               None
              432  COMPARE_OP               is-not
          434_436  POP_JUMP_IF_FALSE   446  'to 446'

 L. 441       438  LOAD_FAST                'new_child'
              440  LOAD_FAST                'new_child'
              442  LOAD_ATTR                next_sibling
              444  STORE_ATTR               previous_sibling
            446_0  COME_FROM           434  '434'

 L. 442       446  LOAD_FAST                'next_child'
              448  LOAD_FAST                'new_childs_last_element'
              450  STORE_ATTR               next_element
            452_0  COME_FROM           408  '408'

 L. 444       452  LOAD_FAST                'new_childs_last_element'
              454  LOAD_ATTR                next_element
              456  LOAD_CONST               None
              458  COMPARE_OP               is-not
          460_462  POP_JUMP_IF_FALSE   472  'to 472'

 L. 445       464  LOAD_FAST                'new_childs_last_element'
              466  LOAD_FAST                'new_childs_last_element'
              468  LOAD_ATTR                next_element
              470  STORE_ATTR               previous_element
            472_0  COME_FROM           460  '460'

 L. 446       472  LOAD_FAST                'self'
              474  LOAD_ATTR                contents
              476  LOAD_METHOD              insert
              478  LOAD_FAST                'position'
              480  LOAD_FAST                'new_child'
              482  CALL_METHOD_2         2  ''
              484  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 380_382

            def append(self, tag):
                """Appends the given PageElement to the contents of this one.

        :param tag: A PageElement.
        """
                self.insert(len(self.contents), tag)

            def extend(self, tags):
                """Appends the given PageElements to this one's contents.

        :param tags: A list of PageElements.
        """
                for tag in tags:
                    self.append(tag)

            def insert_before(self, *args):
                """Makes the given element(s) the immediate predecessor of this one.

        All the elements will have the same parent, and the given elements
        will be immediately before this one.

        :param args: One or more PageElements.
        """
                parent = self.parent
                if parent is None:
                    raise ValueError("Element has no parent, so 'before' has no meaning.")
                if any((x is self for x in args)):
                    raise ValueError("Can't insert an element before itself.")
                for predecessor in args:
                    if isinstance(predecessor, PageElement):
                        predecessor.extract()
                    else:
                        index = parent.index(self)
                        parent.insert(index, predecessor)

            def insert_after(self, *args):
                """Makes the given element(s) the immediate successor of this one.

        The elements will have the same parent, and the given elements
        will be immediately after this one.

        :param args: One or more PageElements.
        """
                parent = self.parent
                if parent is None:
                    raise ValueError("Element has no parent, so 'after' has no meaning.")
                if any((x is self for x in args)):
                    raise ValueError("Can't insert an element after itself.")
                offset = 0
                for successor in args:
                    if isinstance(successor, PageElement):
                        successor.extract()
                    else:
                        index = parent.index(self)
                        parent.insert(index + 1 + offset, successor)
                        offset += 1

            def find_next(self, name=None, attrs={}, text=None, **kwargs):
                """Find the first PageElement that matches the given criteria and
        appears later in the document than this PageElement.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return (self._find_one)((self.find_all_next), name, attrs, text, **kwargs)

            findNext = find_next

            def find_all_next(self, name=None, attrs={}, text=None, limit=None, **kwargs):
                """Find all PageElements that match the given criteria and appear
        later in the document than this PageElement.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet containing PageElements.
        """
                return (self._find_all)(name, attrs, text, limit, (self.next_elements), **kwargs)

            findAllNext = find_all_next

            def find_next_sibling(self, name=None, attrs={}, text=None, **kwargs):
                """Find the closest sibling to this PageElement that matches the
        given criteria and appears later in the document.

        All find_* methods take a common set of arguments. See the
        online documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return (self._find_one)((self.find_next_siblings), name, attrs, text, **kwargs)

            findNextSibling = find_next_sibling

            def find_next_siblings(self, name=None, attrs={}, text=None, limit=None, **kwargs):
                """Find all siblings of this PageElement that match the given criteria
        and appear later in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
                return (self._find_all)(name, attrs, text, limit, 
                 (self.next_siblings), **kwargs)

            findNextSiblings = find_next_siblings
            fetchNextSiblings = find_next_siblings

            def find_previous(self, name=None, attrs={}, text=None, **kwargs):
                """Look backwards in the document from this PageElement and find the
        first PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return (self._find_one)(
                 (self.find_all_previous), name, attrs, text, **kwargs)

            findPrevious = find_previous

            def find_all_previous(self, name=None, attrs={}, text=None, limit=None, **kwargs):
                """Look backwards in the document from this PageElement and find all
        PageElements that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
                return (self._find_all)(name, attrs, text, limit, (self.previous_elements), **kwargs)

            findAllPrevious = find_all_previous
            fetchPrevious = find_all_previous

            def find_previous_sibling(self, name=None, attrs={}, text=None, **kwargs):
                """Returns the closest sibling to this PageElement that matches the
        given criteria and appears earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return (self._find_one)((self.find_previous_siblings), name, attrs, text, **kwargs)

            findPreviousSibling = find_previous_sibling

            def find_previous_siblings(self, name=None, attrs={}, text=None, limit=None, **kwargs):
                """Returns all siblings to this PageElement that match the
        given criteria and appear earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
                return (self._find_all)(name, attrs, text, limit, 
                 (self.previous_siblings), **kwargs)

            findPreviousSiblings = find_previous_siblings
            fetchPreviousSiblings = find_previous_siblings

            def find_parent(self, name=None, attrs={}, **kwargs):
                """Find the closest parent of this PageElement that matches the given
        criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :kwargs: A dictionary of filters on attribute values.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                r = None
                l = (self.find_parents)(name, attrs, 1, **kwargs)
                if l:
                    r = l[0]
                return r

            findParent = find_parent

            def find_parents(self, name=None, attrs={}, limit=None, **kwargs):
                """Find all parents of this PageElement that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return (self._find_all)(name, attrs, None, limit, (self.parents), **kwargs)

            findParents = find_parents
            fetchParents = find_parents

            @property
            def next(self):
                """The PageElement, if any, that was parsed just after this one.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return self.next_element

            @property
            def previous(self):
                """The PageElement, if any, that was parsed just before this one.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                return self.previous_element

            def _find_one(self, method, name, attrs, text, **kwargs):
                r = None
                l = method(name, attrs, text, 1, **kwargs)
                if l:
                    r = l[0]
                return r

            def _find_all--- This code section failed: ---

 L. 736         0  LOAD_FAST                'text'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    30  'to 30'
                8  LOAD_STR                 'string'
               10  LOAD_FAST                'kwargs'
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    30  'to 30'

 L. 737        16  LOAD_FAST                'kwargs'
               18  LOAD_STR                 'string'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'text'

 L. 738        24  LOAD_FAST                'kwargs'
               26  LOAD_STR                 'string'
               28  DELETE_SUBSCR    
             30_0  COME_FROM            14  '14'
             30_1  COME_FROM             6  '6'

 L. 740        30  LOAD_GLOBAL              isinstance
               32  LOAD_DEREF               'name'
               34  LOAD_GLOBAL              SoupStrainer
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 741        40  LOAD_DEREF               'name'
               42  STORE_FAST               'strainer'
               44  JUMP_FORWARD         62  'to 62'
             46_0  COME_FROM            38  '38'

 L. 743        46  LOAD_GLOBAL              SoupStrainer
               48  LOAD_DEREF               'name'
               50  LOAD_FAST                'attrs'
               52  LOAD_FAST                'text'
               54  BUILD_TUPLE_3         3 
               56  LOAD_FAST                'kwargs'
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  STORE_FAST               'strainer'
             62_0  COME_FROM            44  '44'

 L. 745        62  LOAD_FAST                'text'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE   204  'to 204'
               70  LOAD_FAST                'limit'
               72  POP_JUMP_IF_TRUE    204  'to 204'
               74  LOAD_FAST                'attrs'
               76  POP_JUMP_IF_TRUE    204  'to 204'
               78  LOAD_FAST                'kwargs'
               80  POP_JUMP_IF_TRUE    204  'to 204'

 L. 746        82  LOAD_DEREF               'name'
               84  LOAD_CONST               True
               86  COMPARE_OP               is
               88  POP_JUMP_IF_TRUE     98  'to 98'
               90  LOAD_DEREF               'name'
               92  LOAD_CONST               None
               94  COMPARE_OP               is
               96  POP_JUMP_IF_FALSE   122  'to 122'
             98_0  COME_FROM            88  '88'

 L. 748        98  LOAD_GENEXPR             '<code_object <genexpr>>'
              100  LOAD_STR                 'PageElement._find_all.<locals>.<genexpr>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              104  LOAD_FAST                'generator'
              106  GET_ITER         
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'result'

 L. 750       112  LOAD_GLOBAL              ResultSet
              114  LOAD_FAST                'strainer'
              116  LOAD_FAST                'result'
              118  CALL_FUNCTION_2       2  ''
              120  RETURN_VALUE     
            122_0  COME_FROM            96  '96'

 L. 751       122  LOAD_GLOBAL              isinstance
              124  LOAD_DEREF               'name'
              126  LOAD_GLOBAL              str
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_FALSE   204  'to 204'

 L. 753       132  LOAD_DEREF               'name'
              134  LOAD_METHOD              count
              136  LOAD_STR                 ':'
              138  CALL_METHOD_1         1  ''
              140  LOAD_CONST               1
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 757       146  LOAD_DEREF               'name'
              148  LOAD_METHOD              split
              150  LOAD_STR                 ':'
              152  LOAD_CONST               1
              154  CALL_METHOD_2         2  ''
              156  UNPACK_SEQUENCE_2     2 
              158  STORE_DEREF              'prefix'
              160  STORE_DEREF              'local_name'
              162  JUMP_FORWARD        172  'to 172'
            164_0  COME_FROM           144  '144'

 L. 759       164  LOAD_CONST               None
              166  STORE_DEREF              'prefix'

 L. 760       168  LOAD_DEREF               'name'
              170  STORE_DEREF              'local_name'
            172_0  COME_FROM           162  '162'

 L. 761       172  LOAD_CLOSURE             'local_name'
              174  LOAD_CLOSURE             'name'
              176  LOAD_CLOSURE             'prefix'
              178  BUILD_TUPLE_3         3 
              180  LOAD_GENEXPR             '<code_object <genexpr>>'
              182  LOAD_STR                 'PageElement._find_all.<locals>.<genexpr>'
              184  MAKE_FUNCTION_8          'closure'
              186  LOAD_FAST                'generator'
              188  GET_ITER         
              190  CALL_FUNCTION_1       1  ''
              192  STORE_FAST               'result'

 L. 770       194  LOAD_GLOBAL              ResultSet
              196  LOAD_FAST                'strainer'
              198  LOAD_FAST                'result'
              200  CALL_FUNCTION_2       2  ''
              202  RETURN_VALUE     
            204_0  COME_FROM           130  '130'
            204_1  COME_FROM            80  '80'
            204_2  COME_FROM            76  '76'
            204_3  COME_FROM            72  '72'
            204_4  COME_FROM            68  '68'

 L. 771       204  LOAD_GLOBAL              ResultSet
              206  LOAD_FAST                'strainer'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'results'
            212_0  COME_FROM           300  '300'
            212_1  COME_FROM           294  '294'
            212_2  COME_FROM           282  '282'
            212_3  COME_FROM           268  '268'
            212_4  COME_FROM           254  '254'

 L. 773       212  SETUP_FINALLY       226  'to 226'

 L. 774       214  LOAD_GLOBAL              next
              216  LOAD_FAST                'generator'
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'i'
              222  POP_BLOCK        
              224  JUMP_FORWARD        252  'to 252'
            226_0  COME_FROM_FINALLY   212  '212'

 L. 775       226  DUP_TOP          
              228  LOAD_GLOBAL              StopIteration
              230  COMPARE_OP               exception-match
              232  POP_JUMP_IF_FALSE   250  'to 250'
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L. 776       240  POP_EXCEPT       
          242_244  BREAK_LOOP          302  'to 302'
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           232  '232'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           224  '224'

 L. 777       252  LOAD_FAST                'i'
              254  POP_JUMP_IF_FALSE_BACK   212  'to 212'

 L. 778       256  LOAD_FAST                'strainer'
              258  LOAD_METHOD              search
              260  LOAD_FAST                'i'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'found'

 L. 779       266  LOAD_FAST                'found'
              268  POP_JUMP_IF_FALSE_BACK   212  'to 212'

 L. 780       270  LOAD_FAST                'results'
              272  LOAD_METHOD              append
              274  LOAD_FAST                'found'
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          

 L. 781       280  LOAD_FAST                'limit'
              282  POP_JUMP_IF_FALSE_BACK   212  'to 212'
              284  LOAD_GLOBAL              len
              286  LOAD_FAST                'results'
              288  CALL_FUNCTION_1       1  ''
              290  LOAD_FAST                'limit'
              292  COMPARE_OP               >=
              294  POP_JUMP_IF_FALSE_BACK   212  'to 212'

 L. 782   296_298  JUMP_FORWARD        302  'to 302'
              300  JUMP_BACK           212  'to 212'
            302_0  COME_FROM           296  '296'
            302_1  COME_FROM           242  '242'

 L. 783       302  LOAD_FAST                'results'
              304  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 300

            @property
            def next_elements(self):
                """All PageElements that were parsed after this one.

        :yield: A sequence of PageElements.
        """
                i = self.next_element
                while True:
                    if i is not None:
                        yield i
                        i = i.next_element

            @property
            def next_siblings(self):
                """All PageElements that are siblings of this one but were parsed
        later.

        :yield: A sequence of PageElements.
        """
                i = self.next_sibling
                while True:
                    if i is not None:
                        yield i
                        i = i.next_sibling

            @property
            def previous_elements(self):
                """All PageElements that were parsed before this one.

        :yield: A sequence of PageElements.
        """
                i = self.previous_element
                while True:
                    if i is not None:
                        yield i
                        i = i.previous_element

            @property
            def previous_siblings(self):
                """All PageElements that are siblings of this one but were parsed
        earlier.

        :yield: A sequence of PageElements.
        """
                i = self.previous_sibling
                while True:
                    if i is not None:
                        yield i
                        i = i.previous_sibling

            @property
            def parents(self):
                """All PageElements that are parents of this PageElement.

        :yield: A sequence of PageElements.
        """
                i = self.parent
                while True:
                    if i is not None:
                        yield i
                        i = i.parent

            @property
            def decomposed(self):
                """Check whether a PageElement has been decomposed.

        :rtype: bool
        """
                return getattr(self, '_decomposed', False) or False

            def nextGenerator(self):
                return self.next_elements

            def nextSiblingGenerator(self):
                return self.next_siblings

            def previousGenerator(self):
                return self.previous_elements

            def previousSiblingGenerator(self):
                return self.previous_siblings

            def parentGenerator(self):
                return self.parents


        class NavigableString(str, PageElement):
            __doc__ = 'A Python Unicode string that is part of a parse tree.\n\n    When Beautiful Soup parses the markup <b>penguin</b>, it will\n    create a NavigableString for the string "penguin".\n    '
            PREFIX = ''
            SUFFIX = ''
            known_xml = None

            def __new__(cls, value):
                """Create a new NavigableString.

        When unpickling a NavigableString, this method is called with
        the string in DEFAULT_OUTPUT_ENCODING. That encoding needs to be
        passed in to the superclass's __new__ or the superclass won't know
        how to handle non-ASCII characters.
        """
                if isinstance(value, str):
                    u = str.__new__(cls, value)
                else:
                    u = str.__new__(cls, value, DEFAULT_OUTPUT_ENCODING)
                u.setup()
                return u

            def __copy__(self):
                """A copy of a NavigableString has the same contents and class
        as the original, but it is not connected to the parse tree.
        """
                return type(self)(self)

            def __getnewargs__(self):
                return (
                 str(self),)

            def __getattr__(self, attr):
                """text.string gives you text. This is for backwards
        compatibility for Navigable*String, but for CData* it lets you
        get the string without the CData wrapper."""
                if attr == 'string':
                    return self
                raise AttributeError("'%s' object has no attribute '%s'" % (
                 self.__class__.__name__, attr))

            def output_ready(self, formatter='minimal'):
                """Run the string through the provided formatter.

        :param formatter: A Formatter object, or a string naming one of the standard formatters.
        """
                output = self.format_string(self, formatter)
                return self.PREFIX + output + self.SUFFIX

            @property
            def name(self):
                """Since a NavigableString is not a Tag, it has no .name.

        This property is implemented so that code like this doesn't crash
        when run on a mixture of Tag and NavigableString objects:
            [x.name for x in tag.children]
        """
                pass

            @name.setter
            def name(self, name):
                """Prevent NavigableString.name from ever being set."""
                raise AttributeError('A NavigableString cannot be given a name.')


        class PreformattedString(NavigableString):
            __doc__ = 'A NavigableString not subject to the normal formatting rules.\n\n    This is an abstract class used for special kinds of strings such\n    as comments (the Comment class) and CDATA blocks (the CData\n    class).\n    '
            PREFIX = ''
            SUFFIX = ''

            def output_ready(self, formatter=None):
                """Make this string ready for output by adding any subclass-specific
            prefix or suffix.

        :param formatter: A Formatter object, or a string naming one
            of the standard formatters. The string will be passed into the
            Formatter, but only to trigger any side effects: the return
            value is ignored.

        :return: The string, with any subclass-specific prefix and
           suffix added on.
        """
                if formatter is not None:
                    ignore = self.format_string(self, formatter)
                return self.PREFIX + self + self.SUFFIX


        class CData(PreformattedString):
            __doc__ = 'A CDATA block.'
            PREFIX = '<![CDATA['
            SUFFIX = ']]>'


        class ProcessingInstruction(PreformattedString):
            __doc__ = 'A SGML processing instruction.'
            PREFIX = '<?'
            SUFFIX = '>'


        class XMLProcessingInstruction(ProcessingInstruction):
            __doc__ = 'An XML processing instruction.'
            PREFIX = '<?'
            SUFFIX = '?>'


        class Comment(PreformattedString):
            __doc__ = 'An HTML or XML comment.'
            PREFIX = '<!--'
            SUFFIX = '-->'


        class Declaration(PreformattedString):
            __doc__ = 'An XML declaration.'
            PREFIX = '<?'
            SUFFIX = '?>'


        class Doctype(PreformattedString):
            __doc__ = 'A document type declaration.'

            @classmethod
            def for_name_and_ids(cls, name, pub_id, system_id):
                """Generate an appropriate document type declaration for a given
        public ID and system ID.

        :param name: The name of the document's root element, e.g. 'html'.
        :param pub_id: The Formal Public Identifier for this document type,
            e.g. '-//W3C//DTD XHTML 1.1//EN'
        :param system_id: The system identifier for this document type,
            e.g. 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'

        :return: A Doctype.
        """
                value = name or ''
                if pub_id is not None:
                    value += ' PUBLIC "%s"' % pub_id
                    if system_id is not None:
                        value += ' "%s"' % system_id
                elif system_id is not None:
                    value += ' SYSTEM "%s"' % system_id
                return Doctype(value)

            PREFIX = '<!DOCTYPE '
            SUFFIX = '>\n'


        class Stylesheet(NavigableString):
            __doc__ = 'A NavigableString representing an stylesheet (probably\n    CSS).\n\n    Used to distinguish embedded stylesheets from textual content.\n    '


        class Script(NavigableString):
            __doc__ = 'A NavigableString representing an executable script (probably\n    Javascript).\n\n    Used to distinguish executable code from textual content.\n    '


        class TemplateString(NavigableString):
            __doc__ = 'A NavigableString representing a string found inside an HTML\n    template embedded in a larger document.\n\n    Used to distinguish such strings from the main body of the document.\n    '


        class Tag(PageElement):
            __doc__ = 'Represents an HTML or XML tag that is part of a parse tree, along\n    with its attributes and contents.\n\n    When Beautiful Soup parses the markup <b>penguin</b>, it will\n    create a Tag object representing the <b> tag.\n    '

            def __init__(self, parser=None, builder=None, name=None, namespace=None, prefix=None, attrs=None, parent=None, previous=None, is_xml=None, sourceline=None, sourcepos=None, can_be_empty_element=None, cdata_list_attributes=None, preserve_whitespace_tags=None):
                """Basic constructor.

        :param parser: A BeautifulSoup object.
        :param builder: A TreeBuilder.
        :param name: The name of the tag.
        :param namespace: The URI of this Tag's XML namespace, if any.
        :param prefix: The prefix for this Tag's XML namespace, if any.
        :param attrs: A dictionary of this Tag's attribute values.
        :param parent: The PageElement to use as this Tag's parent.
        :param previous: The PageElement that was parsed immediately before
            this tag.
        :param is_xml: If True, this is an XML tag. Otherwise, this is an
            HTML tag.
        :param sourceline: The line number where this tag was found in its
            source document.
        :param sourcepos: The character position within `sourceline` where this
            tag was found.
        :param can_be_empty_element: If True, this tag should be
            represented as <tag/>. If False, this tag should be represented
            as <tag></tag>.
        :param cdata_list_attributes: A list of attributes whose values should
            be treated as CDATA if they ever show up on this tag.
        :param preserve_whitespace_tags: A list of tag names whose contents
            should have their whitespace preserved.
        """
                if parser is None:
                    self.parser_class = None
                else:
                    self.parser_class = parser.__class__
                if name is None:
                    raise ValueError("No value provided for new tag's name.")
                self.name = name
                self.namespace = namespace
                self.prefix = prefix
                if not builder or builder.store_line_numbers:
                    if sourceline is not None or (sourcepos is not None):
                        self.sourceline = sourceline
                        self.sourcepos = sourcepos
                    if attrs is None:
                        attrs = {}
                    elif attrs:
                        if builder is not None and builder.cdata_list_attributes:
                            attrs = builder._replace_cdata_list_attribute_values(self.name, attrs)
                        else:
                            attrs = dict(attrs)
                    else:
                        attrs = dict(attrs)
                    if builder:
                        self.known_xml = builder.is_xml
                    else:
                        self.known_xml = is_xml
                    self.attrs = attrs
                    self.contents = []
                    self.setup(parent, previous)
                    self.hidden = False
                if builder is None:
                    self.can_be_empty_element = can_be_empty_element
                    self.cdata_list_attributes = cdata_list_attributes
                    self.preserve_whitespace_tags = preserve_whitespace_tags
                else:
                    builder.set_up_substitutions(self)
                    self.can_be_empty_element = builder.can_be_empty_element(name)
                    self.cdata_list_attributes = builder.cdata_list_attributes
                    self.preserve_whitespace_tags = builder.preserve_whitespace_tags

            parserClass = _alias('parser_class')

            def __copy__(self):
                """A copy of a Tag is a new Tag, unconnected to the parse tree.
        Its contents are a copy of the old Tag's contents.
        """
                clone = type(self)(None,
                  (self.builder), (self.name), (self.namespace), (self.prefix),
                  (self.attrs), is_xml=(self._is_xml), sourceline=(self.sourceline),
                  sourcepos=(self.sourcepos),
                  can_be_empty_element=(self.can_be_empty_element),
                  cdata_list_attributes=(self.cdata_list_attributes),
                  preserve_whitespace_tags=(self.preserve_whitespace_tags))
                for attr in ('can_be_empty_element', 'hidden'):
                    setattr(clone, attr, getattr(self, attr))
                else:
                    for child in self.contents:
                        clone.append(child.__copy__())
                    else:
                        return clone

            @property
            def is_empty_element(self):
                """Is this tag an empty-element tag? (aka a self-closing tag)

        A tag that has contents is never an empty-element tag.

        A tag that has no contents may or may not be an empty-element
        tag. It depends on the builder used to create the tag. If the
        builder has a designated list of empty-element tags, then only
        a tag whose name shows up in that list is considered an
        empty-element tag.

        If the builder has no designated list of empty-element tags,
        then any tag with no contents is an empty-element tag.
        """
                return len(self.contents) == 0 and self.can_be_empty_element

            isSelfClosing = is_empty_element

            @property
            def string(self):
                """Convenience property to get the single string within this
        PageElement.

        TODO It might make sense to have NavigableString.string return
        itself.

        :return: If this element has a single string child, return
         value is that string. If this element has one child tag,
         return value is the 'string' attribute of the child tag,
         recursively. If this element is itself a string, has no
         children, or has more than one child, return value is None.
        """
                if len(self.contents) != 1:
                    return
                child = self.contents[0]
                if isinstance(child, NavigableString):
                    return child
                return child.string

            @string.setter
            def string(self, string):
                """Replace this PageElement's contents with `string`."""
                self.clear()
                self.append(string.__class__(string))

            def _all_strings--- This code section failed: ---

 L.1238         0  LOAD_FAST                'self'
                2  LOAD_ATTR                descendants
                4  GET_ITER         
              6_0  COME_FROM            82  '82'
              6_1  COME_FROM            74  '74'
              6_2  COME_FROM            48  '48'
              6_3  COME_FROM            26  '26'
                6  FOR_ITER             84  'to 84'
                8  STORE_FAST               'descendant'

 L.1240        10  LOAD_FAST                'types'
               12  LOAD_CONST               None
               14  COMPARE_OP               is

 L.1239        16  POP_JUMP_IF_FALSE    28  'to 28'

 L.1240        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'descendant'
               22  LOAD_GLOBAL              NavigableString
               24  CALL_FUNCTION_2       2  ''

 L.1239        26  POP_JUMP_IF_FALSE_BACK     6  'to 6'
             28_0  COME_FROM            16  '16'

 L.1242        28  LOAD_FAST                'types'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not

 L.1239        34  POP_JUMP_IF_FALSE    50  'to 50'

 L.1242        36  LOAD_GLOBAL              type
               38  LOAD_FAST                'descendant'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_FAST                'types'
               44  COMPARE_OP               not-in

 L.1239        46  POP_JUMP_IF_FALSE    50  'to 50'

 L.1243        48  JUMP_BACK             6  'to 6'
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            34  '34'

 L.1244        50  LOAD_FAST                'strip'
               52  POP_JUMP_IF_FALSE    76  'to 76'

 L.1245        54  LOAD_FAST                'descendant'
               56  LOAD_METHOD              strip
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'descendant'

 L.1246        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'descendant'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               0
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    76  'to 76'

 L.1247        74  JUMP_BACK             6  'to 6'
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            52  '52'

 L.1248        76  LOAD_FAST                'descendant'
               78  YIELD_VALUE      
               80  POP_TOP          
               82  JUMP_BACK             6  'to 6'
             84_0  COME_FROM             6  '6'

Parse error at or near `JUMP_BACK' instruction at offset 82

            strings = property(_all_strings)

            @property
            def stripped_strings(self):
                """Yield all strings in the document, stripping them first.

        :yield: A sequence of stripped strings.
        """
                for string in self._all_strings(True):
                    yield string

            def get_text(self, separator='', strip=False, types=(
 NavigableString, CData)):
                """Get all child strings, concatenated using the given separator.

        :param separator: Strings will be concatenated using this separator.

        :param strip: If True, strings will be stripped before being
            concatenated.

        :types: A tuple of NavigableString subclasses. Any strings of
            a subclass not found in this list will be ignored. By
            default, this means only NavigableString and CData objects
            will be considered. So no comments, processing instructions,
            stylesheets, etc.

        :return: A string.
        """
                return separator.join([s for s in self._all_strings(strip,
                  types=types)])

            getText = get_text
            text = property(get_text)

            def decompose(self):
                """Recursively destroys this PageElement and its children.

        This element will be removed from the tree and wiped out; so
        will everything beneath it.

        The behavior of a decomposed PageElement is undefined and you
        should never use one for anything, but if you need to _check_
        whether an element has been decomposed, you can use the
        `decomposed` property.
        """
                self.extract()
                i = self
                while True:
                    if i is not None:
                        n = i.next_element
                        i.__dict__.clear()
                        i.contents = []
                        i._decomposed = True
                        i = n

            def clear(self, decompose=False):
                """Wipe out all children of this PageElement by calling extract()
           on them.

        :param decompose: If this is True, decompose() (a more
            destructive method) will be called instead of extract().
        """
                if decompose:
                    for element in self.contents[:]:
                        if isinstance(element, Tag):
                            element.decompose()
                        else:
                            element.extract()

                else:
                    for element in self.contents[:]:
                        element.extract()

            def smooth(self):
                """Smooth out this element's children by consolidating consecutive
        strings.

        This makes pretty-printed output look more natural following a
        lot of operations that modified the tree.
        """
                marked = []
                for i, a in enumerate(self.contents):
                    if isinstance(a, Tag):
                        a.smooth()
                    if i == len(self.contents) - 1:
                        pass
                    else:
                        b = self.contents[(i + 1)]
                        if isinstance(a, NavigableString):
                            if isinstance(b, NavigableString):
                                if not isinstance(a, PreformattedString):
                                    if not isinstance(b, PreformattedString):
                                        marked.append(i)
                else:
                    for i in reversed(marked):
                        a = self.contents[i]
                        b = self.contents[(i + 1)]
                        b.extract()
                        n = NavigableString(a + b)
                        a.replace_with(n)

            def index(self, element):
                """Find the index of a child by identity, not value.

        Avoids issues with tag.contents.index(element) getting the
        index of equal elements.

        :param element: Look for this PageElement in `self.contents`.
        """
                for i, child in enumerate(self.contents):
                    if child is element:
                        return i
                else:
                    raise ValueError('Tag.index: element not in tag')

            def get(self, key, default=None):
                """Returns the value of the 'key' attribute for the tag, or
        the value given for 'default' if it doesn't have that
        attribute."""
                return self.attrs.get(key, default)

            def get_attribute_list(self, key, default=None):
                """The same as get(), but always returns a list.

        :param key: The attribute to look for.
        :param default: Use this value if the attribute is not present
            on this PageElement.
        :return: A list of values, probably containing only a single
            value.
        """
                value = self.get(key, default)
                if not isinstance(value, list):
                    value = [
                     value]
                return value

            def has_attr(self, key):
                """Does this PageElement have an attribute with the given name?"""
                return key in self.attrs

            def __hash__(self):
                return str(self).__hash__()

            def __getitem__(self, key):
                """tag[key] returns the value of the 'key' attribute for the Tag,
        and throws an exception if it's not there."""
                return self.attrs[key]

            def __iter__(self):
                """Iterating over a Tag iterates over its contents."""
                return iter(self.contents)

            def __len__(self):
                """The length of a Tag is the length of its list of contents."""
                return len(self.contents)

            def __contains__(self, x):
                return x in self.contents

            def __bool__(self):
                """A tag is non-None even if it has no contents."""
                return True

            def __setitem__(self, key, value):
                """Setting tag[key] sets the value of the 'key' attribute for the
        tag."""
                self.attrs[key] = value

            def __delitem__(self, key):
                """Deleting tag[key] deletes all 'key' attributes for the tag."""
                self.attrs.pop(key, None)

            def __call__(self, *args, **kwargs):
                """Calling a Tag like a function is the same as calling its
        find_all() method. Eg. tag('a') returns a list of all the A tags
        found within this tag."""
                return (self.find_all)(*args, **kwargs)

            def __getattr__(self, tag):
                """Calling tag.subtag is the same as calling tag.find(name="subtag")"""
                if len(tag) > 3:
                    if tag.endswith('Tag'):
                        tag_name = tag[:-3]
                        warnings.warn('.%(name)sTag is deprecated, use .find("%(name)s") instead. If you really were looking for a tag called %(name)sTag, use .find("%(name)sTag")' % dict(name=tag_name))
                        return self.find(tag_name)
                if not tag.startswith('__'):
                    if not tag == 'contents':
                        return self.find(tag)
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, tag))

            def __eq__(self, other):
                """Returns true iff this Tag has the same name, the same attributes,
        and the same contents (recursively) as `other`."""
                if self is other:
                    return True
                if hasattr(other, 'name'):
                    if hasattr(other, 'attrs'):
                        if not hasattr(other, 'contents') or self.name != other.name or self.attrs != other.attrs or len(self) != len(other):
                            return False
                for i, my_child in enumerate(self.contents):
                    if my_child != other.contents[i]:
                        return False
                else:
                    return True

            def __ne__(self, other):
                """Returns true iff this Tag is not identical to `other`,
        as defined in __eq__."""
                return not self == other

            def __repr__(self, encoding='unicode-escape'):
                """Renders this PageElement as a string.

        :param encoding: The encoding to use (Python 2 only).
        :return: Under Python 2, a bytestring; under Python 3,
            a Unicode string.
        """
                if PY3K:
                    return self.decode()
                return self.encode(encoding)

            def __unicode__(self):
                """Renders this PageElement as a Unicode string."""
                return self.decode()

            def __str__(self):
                """Renders this PageElement as a generic string.

        :return: Under Python 2, a UTF-8 bytestring; under Python 3,
            a Unicode string.        
        """
                if PY3K:
                    return self.decode()
                return self.encode()

            if PY3K:
                __str__ = __repr__ = __unicode__

            def encode(self, encoding=DEFAULT_OUTPUT_ENCODING, indent_level=None, formatter='minimal', errors='xmlcharrefreplace'):
                """Render a bytestring representation of this PageElement and its
        contents.

        :param encoding: The destination encoding.
        :param indent_level: Each line of the rendering will be
            indented this many spaces. Used internally in
            recursive calls while pretty-printing.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :param errors: An error handling strategy such as
            'xmlcharrefreplace'. This value is passed along into
            encode() and its value should be one of the constants
            defined by Python.
        :return: A bytestring.

        """
                u = self.decode(indent_level, encoding, formatter)
                return u.encode(encoding, errors)

            def decode(self, indent_level=None, eventual_encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
                """Render a Unicode representation of this PageElement and its
        contents.

        :param indent_level: Each line of the rendering will be
             indented this many spaces. Used internally in
             recursive calls while pretty-printing.
        :param eventual_encoding: The tag is destined to be
            encoded into this encoding. This method is _not_
            responsible for performing that encoding. This information
            is passed in so that it can be substituted in if the
            document contains a <META> tag that mentions the document's
            encoding.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        """
                if not isinstance(formatter, Formatter):
                    formatter = self.formatter_for_name(formatter)
                attributes = formatter.attributes(self)
                attrs = []
                for key, val in attributes:
                    if val is None:
                        decoded = key
                    else:
                        if isinstance(val, list) or isinstance(val, tuple):
                            val = ' '.join(val)
                        elif not isinstance(val, str):
                            val = str(val)
                        elif isinstance(val, AttributeValueWithCharsetSubstitution):
                            if eventual_encoding is not None:
                                val = val.encode(eventual_encoding)
                        text = formatter.attribute_value(val)
                        decoded = str(key) + '=' + formatter.quoted_attribute_value(text)
                    attrs.append(decoded)
                else:
                    close = ''
                    closeTag = ''
                    prefix = ''
                    if self.prefix:
                        prefix = self.prefix + ':'
                    if self.is_empty_element:
                        close = formatter.void_element_close_prefix or ''
                    else:
                        closeTag = '</%s%s>' % (prefix, self.name)
                    pretty_print = self._should_pretty_print(indent_level)
                    space = ''
                    indent_space = ''
                    if indent_level is not None:
                        indent_space = ' ' * (indent_level - 1)
                    if pretty_print:
                        space = indent_space
                        indent_contents = indent_level + 1
                    else:
                        indent_contents = None
                    contents = self.decode_contents(indent_contents, eventual_encoding, formatter)
                    if self.hidden:
                        s = contents
                    else:
                        s = []
                        attribute_string = ''
                        if attrs:
                            attribute_string = ' ' + ' '.join(attrs)
                        if indent_level is not None:
                            s.append(indent_space)
                        s.append('<%s%s%s%s>' % (
                         prefix, self.name, attribute_string, close))
                        if pretty_print:
                            s.append('\n')
                        s.append(contents)
                        if pretty_print:
                            if contents:
                                if contents[(-1)] != '\n':
                                    s.append('\n')
                        if pretty_print:
                            if closeTag:
                                s.append(space)
                        s.append(closeTag)
                        if indent_level is not None:
                            if closeTag:
                                if self.next_sibling:
                                    s.append('\n')
                        s = ''.join(s)
                    return s

            def _should_pretty_print(self, indent_level):
                """Should this tag be pretty-printed?

        Most of them should, but some (such as <pre> in HTML
        documents) should not.
        """
                return (indent_level is not None) and ((not self.preserve_whitespace_tags) or (self.name not in self.preserve_whitespace_tags))

            def prettify(self, encoding=None, formatter='minimal'):
                """Pretty-print this PageElement as a string.

        :param encoding: The eventual encoding of the string. If this is None,
            a Unicode string will be returned.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :return: A Unicode string (if encoding==None) or a bytestring 
            (otherwise).
        """
                if encoding is None:
                    return self.decode(True, formatter=formatter)
                return self.encode(encoding, True, formatter=formatter)

            def decode_contents(self, indent_level=None, eventual_encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
                """Renders the contents of this tag as a Unicode string.

        :param indent_level: Each line of the rendering will be
           indented this many spaces. Used internally in
           recursive calls while pretty-printing.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. decode_contents() is _not_
           responsible for performing that encoding. This information
           is passed in so that it can be substituted in if the
           document contains a <META> tag that mentions the document's
           encoding.

        :param formatter: A Formatter object, or a string naming one of
            the standard Formatters.
        """
                if not isinstance(formatter, Formatter):
                    formatter = self.formatter_for_name(formatter)
                pretty_print = indent_level is not None
                s = []
                for c in self:
                    text = None
                    if isinstance(c, NavigableString):
                        text = c.output_ready(formatter)
                    elif isinstance(c, Tag):
                        s.append(c.decode(indent_level, eventual_encoding, formatter))
                    preserve_whitespace = self.preserve_whitespace_tags and self.name in self.preserve_whitespace_tags
                    if not text or indent_level:
                        if not preserve_whitespace:
                            text = text.strip()
                        if text:
                            if pretty_print:
                                if not preserve_whitespace:
                                    s.append(' ' * (indent_level - 1))
                                s.append(text)
                                if pretty_print:
                                    if not preserve_whitespace:
                                        s.append('\n')
                else:
                    return ''.join(s)

            def encode_contents(self, indent_level=None, encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
                """Renders the contents of this PageElement as a bytestring.

        :param indent_level: Each line of the rendering will be
           indented this many spaces. Used internally in
           recursive calls while pretty-printing.

        :param eventual_encoding: The bytestring will be in this encoding.

        :param formatter: A Formatter object, or a string naming one of
            the standard Formatters.

        :return: A bytestring.
        """
                contents = self.decode_contents(indent_level, encoding, formatter)
                return contents.encode(encoding)

            def renderContents(self, encoding=DEFAULT_OUTPUT_ENCODING, prettyPrint=False, indentLevel=0):
                """Deprecated method for BS3 compatibility."""
                if not prettyPrint:
                    indentLevel = None
                return self.encode_contents(indent_level=indentLevel,
                  encoding=encoding)

            def find(self, name=None, attrs={}, recursive=True, text=None, **kwargs):
                """Look in the children of this PageElement and find the first
        PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
                r = None
                l = (self.find_all)(name, attrs, recursive, text, 1, **kwargs)
                if l:
                    r = l[0]
                return r

            findChild = find

            def find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs):
                """Look in the children of this PageElement and find all
        PageElements that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find_all() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
                generator = self.descendants
                if not recursive:
                    generator = self.children
                return (self._find_all)(name, attrs, text, limit, generator, **kwargs)

            findAll = find_all
            findChildren = find_all

            @property
            def children(self):
                """Iterate over all direct children of this PageElement.

        :yield: A sequence of PageElements.
        """
                return iter(self.contents)

            @property
            def descendants(self):
                """Iterate over all children of this PageElement in a
        breadth-first sequence.

        :yield: A sequence of PageElements.
        """
                if not len(self.contents):
                    return
                stopNode = self._last_descendant().next_element
                current = self.contents[0]
                while True:
                    if current is not stopNode:
                        yield current
                        current = current.next_element

            def select_one(self, selector, namespaces=None, **kwargs):
                """Perform a CSS selection operation on the current element.

        :param selector: A CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param kwargs: Keyword arguments to be passed into SoupSieve's 
           soupsieve.select() method.

        :return: A Tag.
        :rtype: bs4.element.Tag
        """
                value = (self.select)(selector, namespaces, 1, **kwargs)
                if value:
                    return value[0]

            def select(self, selector, namespaces=None, limit=None, **kwargs):
                """Perform a CSS selection operation on the current element.

        This uses the SoupSieve library.

        :param selector: A string containing a CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param limit: After finding this number of results, stop looking.

        :param kwargs: Keyword arguments to be passed into SoupSieve's 
           soupsieve.select() method.

        :return: A ResultSet of Tags.
        :rtype: bs4.element.ResultSet
        """
                if namespaces is None:
                    namespaces = self._namespaces
                if limit is None:
                    limit = 0
                if soupsieve is None:
                    raise NotImplementedError('Cannot execute CSS selectors because the soupsieve package is not installed.')
                results = (soupsieve.select)(selector, self, namespaces, limit, **kwargs)
                return ResultSet(None, results)

            def childGenerator(self):
                """Deprecated generator."""
                return self.children

            def recursiveChildGenerator(self):
                """Deprecated generator."""
                return self.descendants

            def has_key(self, key):
                """Deprecated method. This was kind of misleading because has_key()
        (attributes) was different from __in__ (contents).

        has_key() is gone in Python 3, anyway.
        """
                warnings.warn('has_key is deprecated. Use has_attr("%s") instead.' % key)
                return self.has_attr(key)


        class SoupStrainer(object):
            __doc__ = 'Encapsulates a number of ways of matching a markup element (tag or\n    string).\n\n    This is primarily used to underpin the find_* methods, but you can\n    create one yourself and pass it in as `parse_only` to the\n    `BeautifulSoup` constructor, to parse a subset of a large\n    document.\n    '

            def __init__(self, name=None, attrs={}, text=None, **kwargs):
                """Constructor.

        The SoupStrainer constructor takes the same arguments passed
        into the find_* methods. See the online documentation for
        detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param text: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        """
                self.name = self._normalize_search_value(name)
                if not isinstance(attrs, dict):
                    kwargs['class'] = attrs
                    attrs = None
                if 'class_' in kwargs:
                    kwargs['class'] = kwargs['class_']
                    del kwargs['class_']
                if kwargs:
                    if attrs:
                        attrs = attrs.copy()
                        attrs.update(kwargs)
                    else:
                        attrs = kwargs
                normalized_attrs = {}
                for key, value in list(attrs.items()):
                    normalized_attrs[key] = self._normalize_search_value(value)
                else:
                    self.attrs = normalized_attrs
                    self.text = self._normalize_search_value(text)

            def _normalize_search_value(self, value):
                if not isinstance(value, str):
                    if isinstance(value, Callable) or (hasattr(value, 'match') or isinstance(value, bool) or value is None):
                        return value
                    if isinstance(value, bytes):
                        return value.decode('utf8')
                    if hasattr(value, '__iter__'):
                        new_value = []
                        for v in value:
                            if hasattr(v, '__iter__'):
                                if not isinstance(v, bytes):
                                    if not isinstance(v, str):
                                        new_value.append(v)
                                new_value.append(self._normalize_search_value(v))
                        else:
                            return new_value

                    return str(str(value))

            def __str__(self):
                """A human-readable representation of this SoupStrainer."""
                if self.text:
                    return self.text
                return '%s|%s' % (self.name, self.attrs)

            def search_tag(self, markup_name=None, markup_attrs={}):
                """Check whether a Tag with the given name and attributes would
        match this SoupStrainer.

        Used prospectively to decide whether to even bother creating a Tag
        object.

        :param markup_name: A tag name as found in some markup.
        :param markup_attrs: A dictionary of attributes as found in some markup.

        :return: True if the prospective tag would match this SoupStrainer;
            False otherwise.
        """
                found = None
                markup = None
                if isinstance(markup_name, Tag):
                    markup = markup_name
                    markup_attrs = markup
                call_function_with_tag_data = isinstance(self.name, Callable) and not isinstance(markup_name, Tag)
                if self.name and not call_function_with_tag_data:
                    if not (markup and self._matches(markup, self.name)):
                        if markup or (self._matches(markup_name, self.name)):
                            if call_function_with_tag_data:
                                match = self.name(markup_name, markup_attrs)
                            else:
                                match = True
                                markup_attr_map = None
                            for attr, match_against in list(self.attrs.items()):
                                if not markup_attr_map:
                                    if hasattr(markup_attrs, 'get'):
                                        markup_attr_map = markup_attrs
                                else:
                                    pass
                                markup_attr_map = {}
                                for k, v in markup_attrs:
                                    markup_attr_map[k] = v
                                else:
                                    attr_value = markup_attr_map.get(attr)
                                    if not self._matches(attr_value, match_against):
                                        match = False
                                        break

                            else:
                                if match:
                                    if markup:
                                        found = markup
                                    else:
                                        found = markup_name

                        if not found or self.text:
                            if not self._matches(found.string, self.text):
                                found = None
                    return found

            searchTag = search_tag

            def search(self, markup):
                """Find all items in `markup` that match this SoupStrainer.

        Used by the core _find_all() method, which is ultimately
        called by all find_* methods.

        :param markup: A PageElement or a list of them.
        """
                found = None
                if hasattr(markup, '__iter__') and not isinstance(markup, (Tag, str)):
                    for element in markup:
                        if isinstance(element, NavigableString):
                            if self.search(element):
                                found = element
                                break

                elif isinstance(markup, Tag):
                    if not self.text or self.name or self.attrs:
                        found = self.search_tag(markup)
                elif isinstance(markup, NavigableString) or isinstance(markup, str):
                    if not self.name:
                        if not self.attrs or self._matches(markup, self.text):
                            found = markup
                else:
                    raise Exception("I don't know how to match against a %s" % markup.__class__)
                return found

            def _matches(self, markup, match_against, already_tried=None):
                result = False
                if isinstance(markup, list) or (isinstance(markup, tuple)):
                    for item in markup:
                        if self._matches(item, match_against):
                            return True
                    else:
                        if self._matches(' '.join(markup), match_against):
                            return True
                        return False

                if match_against is True:
                    return markup is not None
                if isinstance(match_against, Callable):
                    return match_against(markup)
                original_markup = markup
                if isinstance(markup, Tag):
                    markup = markup.name
                markup = self._normalize_search_value(markup)
                if markup is None:
                    return not match_against
                if hasattr(match_against, '__iter__') and not isinstance(match_against, str):
                    if not already_tried:
                        already_tried = set()
                    for item in match_against:
                        if item.__hash__:
                            key = item
                        else:
                            key = id(item)
                        if key in already_tried:
                            continue
                        else:
                            already_tried.add(key)
                            if self._matches(original_markup, item, already_tried):
                                return True
                            return False

                    match = False
                    if not match:
                        if isinstance(match_against, str):
                            match = markup == match_against
                    if not match:
                        if hasattr(match_against, 'search'):
                            return match_against.search(markup)
                    if not match:
                        if isinstance(original_markup, Tag):
                            if original_markup.prefix:
                                return self._matches(original_markup.prefix + ':' + original_markup.name, match_against)
                    return match


        class ResultSet(list):
            __doc__ = 'A ResultSet is just a list that keeps track of the SoupStrainer\n    that created it.'

            def __init__(self, source, result=()):
                """Constructor.

        :param source: A SoupStrainer.
        :param result: A list of PageElements.
        """
                super(ResultSet, self).__init__(result)
                self.source = source

            def __getattr__(self, key):
                """Raise a helpful exception to explain a common code fix."""
                raise AttributeError("ResultSet object has no attribute '%s'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?" % key)